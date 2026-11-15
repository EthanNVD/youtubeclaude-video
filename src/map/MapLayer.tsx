import React, { useEffect, useState } from 'react';
import { continueRender, delayRender, staticFile } from 'remotion';
import { geoMercator, geoPath, geoArea, geoCentroid, type GeoProjection } from 'd3-geo';
import type { MapSpec, LonLat } from '../types';
import { col, FONT, INK } from '../theme';

type Feature = { type: 'Feature'; properties: { name: string; subject?: string; part?: string }; geometry: { type: string; coordinates: unknown } };
type FC = { type: 'FeatureCollection'; features: Feature[] };
type Prepared = { fc: FC; centroids: Map<string, LonLat> };

const cache = new Map<string, Prepared>();
const pending = new Map<string, Promise<Prepared>>();

const load = (era: string): Promise<Prepared> => {
  if (cache.has(era)) return Promise.resolve(cache.get(era)!);
  if (!pending.has(era)) {
    pending.set(
      era,
      fetch(staticFile(`maps/world_${era}.json`))
        .then((r) => r.json())
        .then((fc: FC) => {
          // rewind any polygon that d3 would read as covering most of the sphere (polar / mis-wound rings)
          for (const f of fc.features) {
            const g = f.geometry as { type: string; coordinates: number[][][] | number[][][][] };
            if (g.type === 'Polygon') {
              if (geoArea(g as unknown as GeoJSON.Polygon) > 2 * Math.PI) g.coordinates = (g.coordinates as number[][][]).map((r) => [...r].reverse());
            } else if (g.type === 'MultiPolygon') {
              g.coordinates = (g.coordinates as number[][][][]).map((poly) =>
                geoArea({ type: 'Polygon', coordinates: poly } as unknown as GeoJSON.Polygon) > 2 * Math.PI ? poly.map((r) => [...r].reverse()) : poly,
              );
            }
          }
          // label anchor = centroid of each polity's largest polygon
          const best = new Map<string, { area: number; c: LonLat }>();
          for (const f of fc.features) {
            const n = f.properties.name;
            if (!n) continue;
            const polys = f.geometry.type === 'MultiPolygon' ? (f.geometry.coordinates as unknown[]) : [f.geometry.coordinates];
            for (const p of polys) {
              const g = { type: 'Polygon', coordinates: p } as unknown as GeoJSON.Polygon;
              const a = geoArea(g);
              if (a > 2 * Math.PI) continue; // inverted ring guard
              const cur = best.get(n);
              if (!cur || a > cur.area) best.set(n, { area: a, c: geoCentroid(g) as LonLat });
            }
          }
          const prepared = { fc, centroids: new Map([...best].map(([k, v]) => [k, v.c])) };
          cache.set(era, prepared);
          return prepared;
        }),
    );
  }
  return pending.get(era)!;
};

export const useMapData = (era: string) => {
  const [data, setData] = useState<Prepared | null>(cache.get(era) ?? null);
  const [handle] = useState(() => (cache.has(era) ? null : delayRender('map ' + era)));
  useEffect(() => {
    if (cache.has(era)) {
      setData(cache.get(era)!);
      if (handle !== null) continueRender(handle);
      return;
    }
    load(era)
      .then((d) => {
        setData(d);
        if (handle !== null) continueRender(handle);
      })
      .catch((e) => {
        console.error(e);
        if (handle !== null) continueRender(handle);
      });
  }, [era, handle]);
  return data;
};

export const makeProjection = (center: LonLat, span: number, zoom: number): GeoProjection => {
  const k = 1920 / ((span * Math.PI) / 180);
  return geoMercator()
    .rotate([-center[0], 0])
    .center([0, center[1]])
    .scale(k * zoom)
    .translate([960, 540])
    .clipExtent([
      [-300, -300],
      [2220, 1380],
    ]);
};

const STYLES: Record<string, { ocean: string; land: string; border: string; coast: string; label: string }> = {
  paper: { ocean: '#a9cfdc', land: '#efe5c9', border: '#a8957a', coast: '#5f879a', label: '#4a4038' },
  snow: { ocean: '#9fb8c6', land: '#f1f3f2', border: '#a9b2b8', coast: '#6e8796', label: '#3e4a52' },
  dark: { ocean: '#1d2a38', land: '#3a3f44', border: '#59606a', coast: '#0f1820', label: '#d8d2c4' },
  sepia: { ocean: '#c9b48e', land: '#ecdcb8', border: '#a88e66', coast: '#7a6446', label: '#4a3a28' },
  war: { ocean: '#8fb6c9', land: '#e8dcc0', border: '#9a8a6a', coast: '#4f7486', label: '#3a3028' },
};

export const MapLayer: React.FC<{ spec: MapSpec; proj: GeoProjection; t: number }> = ({ spec, proj }) => {
  const data = useMapData(spec.era ?? '1938');
  const st = STYLES[spec.style ?? 'paper'] ?? STYLES.paper;
  const ocean = spec.ocean ?? st.ocean;
  const land = spec.land ?? st.land;
  const path = geoPath(proj);
  const colors = spec.colors ?? {};
  // allow matching by exact name or "contains" key with prefix "~"
  const fillFor = (name: string) => {
    if (colors[name]) return col(colors[name]);
    for (const [k, v] of Object.entries(colors)) if (k.startsWith('~') && name.toLowerCase().includes(k.slice(1).toLowerCase())) return col(v);
    return land;
  };
  const labels = spec.labels === true ? Object.keys(colors).filter((k) => !k.startsWith('~')) : Array.isArray(spec.labels) ? spec.labels : [];
  return (
    <g>
      <rect x={-300} y={-300} width={2520} height={1680} fill={ocean} />
      {/* subtle sea lines */}
      {Array.from({ length: 30 }, (_, i) => <line key={i} x1={-300} x2={2220} y1={-200 + i * 50} y2={-200 + i * 50} stroke="#fff" strokeOpacity={0.05} strokeWidth={2} />)}
      {data ? (
        <g>
          {/* coast glow */}
          <g>
            {data.fc.features.map((f, i) => {
              const d = path(f as unknown as GeoJSON.Feature);
              return d ? <path key={'g' + i} d={d} fill="none" stroke="#fff" strokeOpacity={0.35} strokeWidth={9} strokeLinejoin="round" /> : null;
            })}
          </g>
          {data.fc.features.map((f, i) => {
            const d = path(f as unknown as GeoJSON.Feature);
            if (!d) return null;
            return <path key={i} d={d} fill={fillFor(f.properties.name)} stroke={st.border} strokeWidth={1.6} strokeLinejoin="round" />;
          })}
          {labels.map((n) => {
            const c = data.centroids.get(n);
            if (!c) return null;
            const p = proj(c);
            if (!p) return null;
            return (
              <text key={n} x={p[0]} y={p[1]} textAnchor="middle" fontFamily={FONT.hand} fontSize={34} letterSpacing={3} fill={st.label} opacity={0.85} stroke="#fff" strokeOpacity={0.4} strokeWidth={4} paintOrder="stroke">
                {(spec as { labelNames?: Record<string, string> }).labelNames?.[n] ?? n.toUpperCase()}
              </text>
            );
          })}
        </g>
      ) : null}
      {spec.grid ? <path d={path({ type: 'MultiLineString', coordinates: Array.from({ length: 36 }, (_, i) => [[-180 + i * 10, -80], [-180 + i * 10, 80]]) } as GeoJSON.MultiLineString) ?? ''} stroke={INK} strokeOpacity={0.08} fill="none" /> : null}
    </g>
  );
};
