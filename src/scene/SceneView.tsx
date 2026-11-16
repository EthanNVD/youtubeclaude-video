import React from 'react';
import type { CameraKey, CastMember, LonLat, Scene } from '../types';
import { resolveKeys, rnd, clamp, easeFn, partialPolyline } from '../lib/anim';
import { SetBackground } from '../sets/Sets';
import { Foreground } from '../sets/Rich';
import { MapLayer, makeProjection, PaperOverlay } from '../map/MapLayer';
import { ElementView, type Ctx } from './Elements';
import { DateBadge } from '../overlays/Overlays';
import { FONT, INK, C } from '../theme';

const HUD_KINDS = new Set(['date', 'namecard']);

export const cameraAt = (keys: CameraKey[] | undefined, t: number, base: Record<string, unknown>) =>
  resolveKeys(base, (keys ?? []) as never, t) as { x: number; y: number; zoom: number; rotate?: number; center?: LonLat; shake?: number; span?: number };

export const TINTS: Record<string, string> = {
  sepia: 'sepia(0.85) saturate(0.8) contrast(0.95)',
  grey: 'grayscale(0.85) brightness(0.92)',
  cold: 'saturate(0.7) hue-rotate(-12deg) brightness(0.95)',
  warm: 'sepia(0.25) saturate(1.1)',
  night: 'brightness(0.6) saturate(0.7) hue-rotate(-15deg)',
  red: 'sepia(0.4) saturate(2) hue-rotate(-30deg)',
};

/** One scene rendered at scene-local time t (seconds). Draws into a 1920x1080 SVG. */
export const SceneView: React.FC<{ scene: Scene; t: number; cast?: Record<string, CastMember> }> = ({ scene, t, cast }) => {
  const dur = scene.end - scene.start;
  const els = scene.elements ?? [];
  let proj: Ctx['proj'];
  let world: React.ReactNode;
  let camT = '';
  let dofDef: React.ReactNode = null;

  if (scene.type === 'map' && scene.map) {
    const cam = scene.camera
      ? cameraAt(scene.camera, t, { center: scene.map.center, zoom: 1, span: scene.map.span })
      : { center: scene.map.center, zoom: 1 + 0.035 * (t / Math.max(1, dur)), span: scene.map.span };
    let center = (cam.center ?? scene.map.center) as LonLat;
    // map.follow = index of a route/arrow element: the camera rides along with its tip (reference: "the camera follows the ship")
    const fi = (scene.map as { follow?: number }).follow;
    const fel = fi !== undefined ? els[fi] : undefined;
    if (fel && Array.isArray(fel.path)) {
      const keyed = resolveKeys(fel, fel.keys, t) as typeof fel;
      const a = t - (fel.in ?? 0);
      const r = fel.enter === 'draw' ? easeFn('inOut', clamp(a / ((fel.dur as number) ?? 1.2))) : (keyed.progress as number) ?? 1;
      const tip = partialPolyline(fel.path as [number, number][], r).tip as [number, number];
      const lead = clamp(t / 0.9);
      center = [center[0] + (tip[0] - center[0]) * lead, center[1] + (tip[1] - center[1]) * lead];
    }
    proj = makeProjection(center, (cam.span as number) ?? scene.map.span, cam.zoom ?? 1);
    world = <MapLayer spec={scene.map} proj={proj} t={t} />;
  } else if (scene.type === 'title' || scene.type === 'chapter') {
    world = <ChapterCard scene={scene} t={t} />;
  } else {
    // no camera keys -> a slow, gentle push-in so the frame is never dead (reference style: 3-6 % over the shot)
    const drift = !scene.camera && scene.set?.kind !== 'paper' && scene.set?.kind !== 'studio' && (scene.set?.drift as number) !== 0;
    const dz = (scene.set?.drift as number) ?? 0.045;
    const cam = drift
      ? { x: 960 + (scene.set?.driftX as number ?? 0) * (t / Math.max(1, dur)), y: 540, zoom: 1 + dz * (t / Math.max(1, dur)), rotate: 0, shake: 0 }
      : cameraAt(scene.camera, t, { x: 960, y: 540, zoom: 1, rotate: 0, shake: 0 });
    const sh = cam.shake ?? 0;
    const jx = sh ? (rnd(Math.floor(t * 24), 'x') - 0.5) * sh * 2 : 0;
    const jy = sh ? (rnd(Math.floor(t * 24), 'y') - 0.5) * sh * 2 : 0;
    camT = `translate(${960 + jx} ${540 + jy}) scale(${cam.zoom}) rotate(${cam.rotate ?? 0}) translate(${-cam.x} ${-cam.y})`;
    // depth of field: the set is softly blurred so actors and props read sharp in front of it
    const flat = ['paper', 'studio', 'void', 'dark', 'memorial'].includes(scene.set?.kind ?? '');
    const dof = (scene.set?.dof as number) ?? (flat ? 0 : 1.6);
    world = scene.set ? (
      <g filter={dof > 0 ? `url(#dof_${scene.id})` : undefined}>
        <SetBackground {...scene.set} t={t} />
      </g>
    ) : <rect x={-240} y={-160} width={2400} height={1400} fill="#e6dcc4" />;
    dofDef = dof > 0 ? (
      <filter id={`dof_${scene.id}`} x="-5%" y="-5%" width="110%" height="110%">
        <feGaussianBlur stdDeviation={dof} />
      </filter>
    ) : null;
  }

  const ctx: Ctx = { t, dur, cast, proj, sceneId: scene.id };
  const worldEls = els.map((el, i) => ({ el, i })).filter(({ el }) => !el.hud && !HUD_KINDS.has(el.kind));
  const hudEls = els.map((el, i) => ({ el, i })).filter(({ el }) => el.hud || HUD_KINDS.has(el.kind));
  const weather = scene.set?.weather as string | undefined;

  const lbRaw = scene.letterbox;
  const lb = !!lbRaw;
  const lbH = lb ? 118 * clamp(t / 0.45, 0, 1) ** 0.6 : 0;
  const lbText = typeof lbRaw === 'string' ? lbRaw : lb ? [scene.date, scene.place].filter(Boolean).join(' — ').toUpperCase() : '';
  return (
    <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{ position: 'absolute', inset: 0 }}>
      <defs>
        {dofDef}
        <linearGradient id="flagshade" x1="0" x2="1">
          <stop offset="0" stopColor="#000" stopOpacity={0} />
          <stop offset="0.3" stopColor="#000" stopOpacity={0.5} />
          <stop offset="0.55" stopColor="#fff" stopOpacity={0.4} />
          <stop offset="0.8" stopColor="#000" stopOpacity={0.5} />
          <stop offset="1" stopColor="#000" stopOpacity={0} />
        </linearGradient>
      </defs>
      <g transform={camT || undefined}>
        {world}
        {worldEls.map(({ el, i }) => <ElementView key={i} el={el} ctx={ctx} index={i} />)}
        {scene.set?.fg ? <g transform={`translate(${(960 - ((cameraAt(scene.camera, t, { x: 960 }) as { x: number }).x ?? 960)) * 0.25} 0)`}><Foreground kind={scene.set.fg as string} t={t} side={scene.set.fgSide as string} /></g> : null}
      </g>
      {scene.type === 'map' && scene.map && (scene.map as { paper?: boolean }).paper !== false && scene.map.style !== 'poster' && scene.map.style !== 'dark' ? <PaperOverlay /> : null}
      {weather === 'rain' || weather === 'snow' ? (
        <g transform="translate(960 540)">
          <ElementView el={{ kind: 'fx', type: weather, enter: 'none' }} ctx={ctx} index={999} />
        </g>
      ) : null}
      {hudEls.map(({ el, i }) => <ElementView key={'h' + i} el={el} ctx={ctx} index={i} />)}
      {lb ? (
        // cinema bars for dramatised moments; the caption replaces the date/place badges
        <g>
          <rect x={0} y={-10} width={1920} height={10 + lbH} fill="#0b0a09" />
          <rect x={0} y={1080 - lbH} width={1920} height={lbH + 10} fill="#0b0a09" />
          {lbText ? (
            <text x={960} y={1080 - lbH / 2 + 12} textAnchor="middle" fontFamily={FONT.mono} fontWeight={700} fontSize={34} letterSpacing={6} fill="#efe6d2" opacity={clamp((t - 0.3) / 0.5, 0, 1)}>{lbText}</text>
          ) : null}
        </g>
      ) : (
        <>
          {scene.date ? <DateBadge text={scene.date} a={t} /> : null}
          {scene.clock ? <DateBadge text={scene.clock} a={t} right /> : null}
          {scene.place ? <DateBadge text={scene.place} a={t - 0.2} y={scene.date ? 140 : 46} /> : null}
        </>
      )}
    </svg>
  );
};

const ChapterCard: React.FC<{ scene: Scene; t: number }> = ({ scene, t }) => {
  const k = Math.min(1, t / 0.6);
  return (
    <g>
      <rect x={-240} y={-160} width={2400} height={1400} fill="#1e1c1a" />
      <rect x={260} y={330} width={1400} height={420} fill="#efe4c8" stroke={INK} strokeWidth={8} transform={`rotate(-1 960 540)`} />
      <rect x={260} y={330} width={30} height={420} fill={C.red} transform={`rotate(-1 960 540)`} />
      {scene.subtitle ? <text x={960} y={450} textAnchor="middle" fontFamily={FONT.hand} fontSize={54} fill="#6a5a48" opacity={k}>{scene.subtitle}</text> : null}
      <text x={960} y={scene.subtitle ? 600 : 570} textAnchor="middle" fontFamily={FONT.heavy} fontSize={(scene.title?.length ?? 0) > 22 ? 96 : 124} fill={INK} opacity={k} letterSpacing={2}>{(scene.title ?? '').toUpperCase()}</text>
    </g>
  );
};
