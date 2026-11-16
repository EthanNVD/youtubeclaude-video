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

type PhysFeature = { properties: { k: string; name: string; rank: number }; geometry: { type: string; coordinates: unknown } };
let physCache: PhysFeature[] | null = null;
let physPending: Promise<PhysFeature[]> | null = null;
const loadPhys = () => {
  if (physCache) return Promise.resolve(physCache);
  if (!physPending) physPending = fetch(staticFile('maps/physical.json')).then((r) => r.json()).then((d: { features: PhysFeature[] }) => (physCache = d.features));
  return physPending;
};
const usePhysical = (on: boolean) => {
  const [data, setData] = useState<PhysFeature[] | null>(physCache);
  const [handle] = useState(() => (on && !physCache ? delayRender('physical map') : null));
  useEffect(() => {
    if (!on) return;
    loadPhys()
      .then((d) => {
        setData(d);
        if (handle !== null) continueRender(handle);
      })
      .catch((e) => {
        console.error(e);
        if (handle !== null) continueRender(handle);
      });
  }, [on, handle]);
  return data;
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
  paper: { ocean: '#b7d0cf', land: '#ecdcb6', border: '#9a8664', coast: '#4f6f78', label: '#4a4038' },
  old: { ocean: '#b3c9c3', land: '#e6d3a8', border: '#8a7656', coast: '#46625f', label: '#3e3428' },
  snow: { ocean: '#9fb8c6', land: '#f1f3f2', border: '#a9b2b8', coast: '#6e8796', label: '#3e4a52' },
  dark: { ocean: '#1d2a38', land: '#3a3f44', border: '#59606a', coast: '#0f1820', label: '#d8d2c4' },
  sepia: { ocean: '#c9b48e', land: '#ecdcb8', border: '#a88e66', coast: '#7a6446', label: '#4a3a28' },
  war: { ocean: '#8fb6c9', land: '#e8dcc0', border: '#9a8a6a', coast: '#4f7486', label: '#3a3028' },
  // thumbnail look: saturated poster map, bright sea, white borders
  poster: { ocean: '#2f7fc1', land: '#f2cf5b', border: '#ffffff', coast: '#1d4f80', label: '#1b1b1b' },
};

export const MapLayer: React.FC<{ spec: MapSpec; proj: GeoProjection; t: number }> = ({ spec, proj }) => {
  const data = useMapData(spec.era ?? '1938');
  const sp = spec as MapSpec & { rivers?: boolean; riverLabels?: boolean; paper?: boolean; graticule?: boolean; ripples?: boolean };
  const styleName = spec.style ?? 'paper';
  const physicalOn = sp.rivers !== false && styleName !== 'poster';
  const phys = usePhysical(physicalOn);
  const st = STYLES[styleName] ?? STYLES.paper;
  const ocean = spec.ocean ?? st.ocean;
  const land = spec.land ?? st.land;
  const path = geoPath(proj);
  const colors = spec.colors ?? {};
  const fillFor = (name: string) => {
    if (colors[name]) return col(colors[name]);
    for (const [k, v] of Object.entries(colors)) if (k.startsWith('~') && name.toLowerCase().includes(k.slice(1).toLowerCase())) return col(v);
    return land;
  };
  const labels = spec.labels === true ? Object.keys(colors).filter((k) => !k.startsWith('~')) : Array.isArray(spec.labels) ? spec.labels : [];
  // visible span in degrees (for detail level)
  const p0 = proj.invert?.([0, 540]), p1 = proj.invert?.([1920, 540]);
  const spanDeg = p0 && p1 ? Math.abs(p1[0] - p0[0]) : 20;
  const maxRank = spanDeg > 30 ? 4 : spanDeg > 12 ? 6 : spanDeg > 4 ? 8 : 9;
  const riverW = spanDeg > 30 ? 2 : spanDeg > 8 ? 3 : 4.5;
  const paper = sp.paper !== false && styleName !== 'poster' && styleName !== 'dark';
  // river labels: one per named river, placed at the longest on-screen segment, rotated along it
  const riverLabels: { x: number; y: number; a: number; name: string }[] = [];
  if (phys && sp.riverLabels !== false && physicalOn) {
    const seen = new Set<string>();
    for (const f of phys) {
      if (f.properties.k !== 'river' || !f.properties.name || f.properties.rank > Math.min(maxRank, 7) || seen.has(f.properties.name)) continue;
      const lines = (f.geometry.type === 'MultiLineString' ? f.geometry.coordinates : [f.geometry.coordinates]) as number[][][];
      let best: { x: number; y: number; a: number; len: number } | null = null;
      for (const ln of lines) {
        for (let i = 0; i + 1 < ln.length; i++) {
          const a = proj(ln[i] as [number, number]), b = proj(ln[i + 1] as [number, number]);
          if (!a || !b) continue;
          const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
          if (mx < 120 || mx > 1800 || my < 160 || my > 940) continue;
          const len = Math.hypot(b[0] - a[0], b[1] - a[1]);
          if (!best || len > best.len) {
            let ang = (Math.atan2(b[1] - a[1], b[0] - a[0]) * 180) / Math.PI;
            if (ang > 90) ang -= 180;
            if (ang < -90) ang += 180;
            best = { x: mx, y: my, a: ang, len };
          }
        }
      }
      if (best && best.len > 18 && riverLabels.length < 9) {
        seen.add(f.properties.name);
        riverLabels.push({ x: best.x, y: best.y, a: best.a, name: f.properties.name });
      }
    }
  }
  const grat: number[] = [];
  if (sp.graticule !== false && paper) {
    const step = spanDeg > 40 ? 10 : spanDeg > 10 ? 5 : spanDeg > 3 ? 1 : 0.5;
    const pl = proj.invert?.([0, 0]), pb = proj.invert?.([0, 1080]);
    if (pl && pb) for (let lat = Math.ceil(pb[1] / step) * step; lat <= pl[1]; lat += step) grat.push(lat);
  }
  return (
    <g>
      <rect x={-300} y={-300} width={2520} height={1680} fill={ocean} />
      {data ? (
        <g>
          {/* coastal ripples (parallel bands along every coast, like an engraved chart) */}
          {sp.ripples !== false && styleName !== 'poster'
            ? [44, 30, 16].map((w, k) => (
                <g key={'rip' + k}>
                  {data.fc.features.map((f, i) => {
                    const d = path(f as unknown as GeoJSON.Feature);
                    return d ? <path key={i} d={d} fill="none" stroke={k === 2 ? '#ffffff' : st.coast} strokeOpacity={k === 2 ? 0.35 : 0.08 + k * 0.03} strokeWidth={w} strokeLinejoin="round" /> : null;
                  })}
                </g>
              ))
            : null}
          {data.fc.features.map((f, i) => {
            const d = path(f as unknown as GeoJSON.Feature);
            if (!d) return null;
            return <path key={i} d={d} fill={fillFor(f.properties.name)} stroke={styleName === 'poster' ? st.border : st.border} strokeWidth={styleName === 'poster' ? 3.2 : 1.8} strokeLinejoin="round" />;
          })}
          {/* inked coastline on top of the land fills */}
          {styleName !== 'poster'
            ? data.fc.features.map((f, i) => {
                const d = path(f as unknown as GeoJSON.Feature);
                return d ? <path key={'c' + i} d={d} fill="none" stroke={INK} strokeOpacity={0.55} strokeWidth={2.4} strokeLinejoin="round" /> : null;
              })
            : null}
          {/* physical layer: lakes + rivers */}
          {phys
            ? phys.map((f, i) => {
                if (f.properties.rank > maxRank) return null;
                const d = path(f.geometry as unknown as GeoJSON.Geometry);
                if (!d) return null;
                return f.properties.k === 'lake' ? (
                  <path key={'p' + i} d={d} fill={ocean} stroke={INK} strokeOpacity={0.4} strokeWidth={1.5} />
                ) : (
                  <path key={'p' + i} d={d} fill="none" stroke="#5f8fa8" strokeWidth={f.properties.rank <= 4 ? riverW * 1.3 : riverW} strokeLinecap="round" strokeLinejoin="round" opacity={0.9} />
                );
              })
            : null}
          {riverLabels.map((r, i) => (
            <text key={'rl' + i} transform={`translate(${r.x} ${r.y - 10}) rotate(${r.a})`} textAnchor="middle" fontFamily={FONT.serif} fontStyle="italic" fontSize={30} fill="#3f6d86" stroke={land} strokeWidth={5} paintOrder="stroke" opacity={0.95}>{r.name}</text>
          ))}
          {labels.map((n) => {
            const c = data.centroids.get(n);
            if (!c) return null;
            const p = proj(c);
            if (!p) return null;
            return (
              <text key={n} x={p[0]} y={p[1]} textAnchor="middle" fontFamily={FONT.cond} fontWeight={600} fontSize={34} letterSpacing={6} fill={st.label} opacity={0.75} stroke="#fff" strokeOpacity={0.35} strokeWidth={4} paintOrder="stroke">
                {(spec as { labelNames?: Record<string, string> }).labelNames?.[n] ?? n.toUpperCase()}
              </text>
            );
          })}
        </g>
      ) : null}
      {/* graticule: faint parallels with degree tags at the left edge */}
      {grat.map((lat) => {
        const a = proj([proj.invert?.([0, 540])?.[0] ?? 0, lat]);
        if (!a) return null;
        return (
          <g key={'g' + lat} opacity={0.35}>
            <line x1={-300} x2={2220} y1={a[1]} y2={a[1]} stroke={INK} strokeWidth={1.2} strokeDasharray="2 10" />
            <text x={40} y={a[1] - 6} fontFamily={FONT.serif} fontSize={22} fill={INK}>{`${Math.round(lat * 10) / 10}°`}</text>
          </g>
        );
      })}
      {spec.grid ? <path d={path({ type: 'MultiLineString', coordinates: Array.from({ length: 36 }, (_, i) => [[-180 + i * 10, -80], [-180 + i * 10, 80]]) } as GeoJSON.MultiLineString) ?? ''} stroke={INK} strokeOpacity={0.08} fill="none" /> : null}
    </g>
  );
};

/** Old-paper finish drawn on top of the map (screen space): fold creases, stains, edge darkening. */
export const PaperOverlay: React.FC = () => (
  <g style={{ pointerEvents: 'none' }}>
    <defs>
      <radialGradient id="paper_stain" cx="0.3" cy="0.7" r="0.5">
        <stop offset="0" stopColor="#7a5a2a" stopOpacity={0.1} />
        <stop offset="1" stopColor="#7a5a2a" stopOpacity={0} />
      </radialGradient>
      <linearGradient id="fold_v" x1="0" x2="1">
        <stop offset="0" stopColor="#000" stopOpacity={0} />
        <stop offset="0.48" stopColor="#000" stopOpacity={0.1} />
        <stop offset="0.5" stopColor="#fff" stopOpacity={0.22} />
        <stop offset="0.53" stopColor="#000" stopOpacity={0} />
      </linearGradient>
      <linearGradient id="fold_h" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0" stopColor="#000" stopOpacity={0} />
        <stop offset="0.48" stopColor="#000" stopOpacity={0.09} />
        <stop offset="0.5" stopColor="#fff" stopOpacity={0.2} />
        <stop offset="0.53" stopColor="#000" stopOpacity={0} />
      </linearGradient>
    </defs>
    {[640, 1280].map((x) => <rect key={x} x={x - 30} y={0} width={60} height={1080} fill="url(#fold_v)" />)}
    <rect x={0} y={510} width={1920} height={60} fill="url(#fold_h)" />
    <rect x={0} y={0} width={1920} height={1080} fill="url(#paper_stain)" />
    <ellipse cx={1500} cy={260} rx={260} ry={160} fill="#7a5a2a" opacity={0.04} />
  </g>
);
