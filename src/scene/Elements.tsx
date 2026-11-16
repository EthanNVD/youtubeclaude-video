import React from 'react';
import type { GeoProjection } from 'd3-geo';
import type { CastMember, ElementBase, LonLat } from '../types';
import { envelope, resolveKeys, smoothPath, partialPolyline, toD, clamp, easeFn, rnd } from '../lib/anim';
import { Character } from '../char/Character';
import { resolveCast } from '../char/presets';
import { Prop, Flag } from '../props/Props';
import { Vehicle } from '../props/Vehicles';
import { Fx } from '../fx/Fx';
import { Label, Stamp, Bubble, Headline, Counter, Document, NameCard, DateBadge } from '../overlays/Overlays';
import { ScaleDevice, MeterDevice, BarsDevice, ScoreDevice, RoadDevice, RankingDevice, TimelineDevice, LedgerDevice } from '../devices/Devices';
import { C, INK, FONT, col, nation, uiColor } from '../theme';

export type Ctx = { t: number; dur: number; cast?: Record<string, CastMember>; proj?: GeoProjection; sceneId: string };

const P = (ctx: Ctx, at?: LonLat): [number, number] | null => {
  if (!at || !ctx.proj) return null;
  const p = ctx.proj(at);
  return p ? [p[0], p[1]] : null;
};

/** Thick arrow with a triangular head that travels with the drawn tip. */
export const Arrow: React.FC<{ pts: [number, number][]; r: number; color?: string; width?: number; dashed?: boolean; head?: boolean; outline?: string; curve?: boolean }> = ({ pts, r, color = C.red, width = 24, dashed, head = true, outline = INK, curve = true }) => {
  const sm = curve ? smoothPath(pts, 16) : pts;
  const full = partialPolyline(sm, 1);
  const L = full.total ?? 0;
  if (L <= 0 || r <= 0) return null;
  const headLen = head ? width * 2.1 : 0;
  const tipD = L * r;
  const body = partialPolyline(sm, Math.max(0, (tipD - headLen * 0.75) / L));
  const tip = partialPolyline(sm, tipD / L);
  const ang = tip.angle;
  const hw = width * 1.6;
  const tx = tip.tip[0], ty = tip.tip[1];
  const bx = tx - Math.cos(ang) * headLen, by = ty - Math.sin(ang) * headLen;
  const nx = -Math.sin(ang), ny = Math.cos(ang);
  const headD = `M${tx} ${ty} L${bx + nx * hw} ${by + ny * hw} L${bx - nx * hw} ${by - ny * hw} Z`;
  const d = toD(body.pts);
  const c = col(color);
  return (
    <g>
      <path d={d} stroke={outline} strokeWidth={width + 9} fill="none" strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dashed ? `${width * 1.4} ${width * 1.1}` : undefined} />
      <path d={d} stroke={c} strokeWidth={width} fill="none" strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dashed ? `${width * 1.4} ${width * 1.1}` : undefined} />
      <path d={d} stroke="#fff" strokeOpacity={0.25} strokeWidth={width * 0.25} fill="none" strokeLinecap="round" transform={`translate(${-width * 0.15} ${-width * 0.15})`} />
      {head && tipD > headLen * 0.5 ? <path d={headD} fill={c} stroke={outline} strokeWidth={4.5} strokeLinejoin="round" /> : null}
    </g>
  );
};

/** NATO-style unit counter for maps. */
const Unit: React.FC<{ type?: string; nationKey?: string; label?: string; color?: string; size?: number }> = ({ type = 'inf', nationKey, label, color, size = 1 }) => {
  const c = col(color, uiColor(nationKey));
  const w = 74, h = 50;
  let sym: React.ReactNode = null;
  if (type === 'inf') sym = <path d={`M${-w / 2 + 8} ${-h / 2 + 8} L${w / 2 - 8} ${h / 2 - 8} M${w / 2 - 8} ${-h / 2 + 8} L${-w / 2 + 8} ${h / 2 - 8}`} stroke={INK} strokeWidth={4} />;
  else if (type === 'armor') sym = <rect x={-22} y={-11} width={44} height={22} rx={11} fill="none" stroke={INK} strokeWidth={4} />;
  else if (type === 'art') sym = <circle r={8} fill={INK} />;
  else if (type === 'cav') sym = <path d={`M${-w / 2 + 8} ${h / 2 - 8} L${w / 2 - 8} ${-h / 2 + 8}`} stroke={INK} strokeWidth={4} />;
  else if (type === 'hq') sym = <path d={`M${-w / 2} 0 H${w / 2}`} stroke={INK} strokeWidth={3} />;
  return (
    <g transform={`scale(${size})`}>
      <rect x={-w / 2} y={-h / 2} width={w} height={h} fill={c} stroke={INK} strokeWidth={4} />
      <rect x={-w / 2 + 5} y={-h / 2 + 5} width={w - 10} height={h - 10} fill="none" stroke="#fff" strokeOpacity={0.6} strokeWidth={2} />
      {sym}
      {label ? <text y={h / 2 + 34} textAnchor="middle" fontFamily={FONT.hand} fontSize={30} fill={INK} stroke="#fff" strokeWidth={6} paintOrder="stroke">{label}</text> : null}
    </g>
  );
};

/** Top-down ship / plane icons for maps. */
const MapIcon: React.FC<{ type: string; nationKey?: string; color?: string; size?: number; label?: string; t: number; burning?: boolean }> = ({ type, nationKey, color, size = 1, label, t, burning }) => {
  const c = col(color, uiColor(nationKey));
  return (
    <g transform={`scale(${size})`}>
      {type === 'carrier' ? (
        <g>
          <path d="M-70 -14 H60 L76 0 L60 14 H-70 Z" fill="#8a7a5a" stroke={INK} strokeWidth={4} />
          <rect x={10} y={-22} width={18} height={9} fill={c} stroke={INK} strokeWidth={3} />
          <path d="M-60 0 H50" stroke="#fff" strokeOpacity={0.5} strokeWidth={2} strokeDasharray="8 6" />
        </g>
      ) : type === 'plane' ? (
        <path d="M0 -30 L6 -10 L36 0 L6 6 L4 22 L12 28 L-12 28 L-4 22 L-6 6 L-36 0 L-6 -10 Z" fill={c} stroke={INK} strokeWidth={3} transform="rotate(90)" />
      ) : type === 'sub' ? (
        <path d="M-50 0 Q-50 -10 -30 -10 H40 Q56 -8 56 0 Q56 8 40 10 H-30 Q-50 10 -50 0 Z M0 -10 v-10 h12 v10" fill={c} stroke={INK} strokeWidth={3} />
      ) : (
        <path d="M-56 -11 H44 L62 0 L44 11 H-56 Z" fill={c} stroke={INK} strokeWidth={4} />
      )}
      {burning ? (
        <g>
          <circle cx={0} cy={-6} r={16 + Math.sin(t * 12) * 3} fill="#f08a3a" opacity={0.9} />
          {[0, 1, 2, 3].map((i) => {
            const k = ((t * 0.8 + i / 4) % 1);
            return <circle key={i} cx={k * 40} cy={-10 - k * 90} r={10 + k * 22} fill="#3a3632" opacity={0.7 * (1 - k)} />;
          })}
        </g>
      ) : null}
      {label ? <text y={44} textAnchor="middle" fontFamily={FONT.hand} fontSize={28} fill={INK} stroke="#fff" strokeWidth={6} paintOrder="stroke">{label}</text> : null}
    </g>
  );
};

export const ElementView: React.FC<{ el: ElementBase; ctx: Ctx; index: number }> = ({ el, ctx, index }) => {
  const { t, dur } = ctx;
  const env = envelope(el, t, dur);
  if (!env.visible) return null;
  // vehicles move with a physical speed profile unless a key says otherwise
  const keysUsed = el.kind === 'vehicle' && el.keys ? el.keys.map((kk) => (('x' in kk || 'at' in kk) && !kk.ease ? { ...kk, ease: 'drive' as const } : kk)) : el.keys;
  const e = resolveKeys(el, keysUsed, t) as ElementBase;
  const a = t - (el.in ?? 0);
  const seed = ctx.sceneId + ':' + (el.id ?? index);

  // position (map coordinates take precedence)
  let x = (e.x as number) ?? 960, y = (e.y as number) ?? 540;
  const pp = P(ctx, e.at as LonLat | undefined);
  if (pp) [x, y] = pp;
  const s = ((e.scale as number) ?? 1) * env.s;
  const rot = (e.rotate as number) ?? 0;
  const flip = e.flip ? -1 : 1;
  const tr = `translate(${x + env.dx} ${y + env.dy}) rotate(${rot}) scale(${s * flip} ${s})`;
  const op = env.o * ((e.opacity as number) ?? 1);

  const k = e.kind;
  let body: React.ReactNode = null;
  switch (k) {
    case 'actor': {
      const who = (e.who as string) ?? 'civilian_man';
      const spec = resolveCast(ctx.cast as never, who, (e.look_ as Record<string, unknown>) ?? undefined);
      // auto-walk when x/at changes over time; direction + run from the speed
      let walk = 0, dir = 1, run = false;
      if (el.keys?.some((kk) => 'x' in kk || 'at' in kk)) {
        const e2 = resolveKeys(el, el.keys, t + 0.08) as ElementBase;
        let dx = ((e2.x as number) ?? x) - ((e.x as number) ?? x);
        if (e2.at && e.at && ctx.proj) {
          const p1 = ctx.proj(e.at as LonLat), p2 = ctx.proj(e2.at as LonLat);
          if (p1 && p2) dx = p2[0] - p1[0];
        }
        if (Math.abs(dx) > 0.4) {
          walk = 1;
          dir = Math.sign(dx) * flip;
          run = Math.abs(dx) / 0.08 / Math.max(0.2, (e.scale as number) ?? 1) > 330;
        }
      }
      if (e.walk === true) { walk = 1; dir = ((e.dir as number) ?? 1); }
      if (e.run === true) { walk = 1; run = true; dir = ((e.dir as number) ?? dir); }
      // pose blending: find the last pose change at or before t
      let pose = (el.pose as string) ?? 'idle', prevPose = pose, tChange = -99;
      for (const kk of [...(el.keys ?? [])].sort((a, b) => a.t - b.t)) {
        if (kk.t > t) break;
        if (typeof kk.pose === 'string' && kk.pose !== pose) { prevPose = pose; pose = kk.pose; tChange = kk.t; }
      }
      const poseK = clamp((t - tChange) / ((e.poseDur as number) ?? 0.42), 0, 1);
      const holdScale: Record<string, number> = { holdUp: 0.75, hold: 0.6, carry: 0.7, write: 0.5, phone: 0.45, show: 0.6, drink: 0.4, smoke: 0.35 };
      const held = e.holds
        ? {
            node: <Prop item={e.holds as string} t={t} text={e.holdsText as string} nationKey={spec.nation} />,
            scale: (e.holdsScale as number) ?? holdScale[pose] ?? 0.5,
            rotate: pose === 'phone' ? -30 : (e.holdsRotate as number) ?? 0,
            dy: pose === 'holdUp' ? -95 : pose === 'hold' || pose === 'carry' ? 4 : 0,
            grip: ({ paper: 52, telegram: 98, folder: 118, book: 68, crate: 58, document: 98, newspaper: 98, map: 110 } as Record<string, number>)[e.holds as string],
          }
        : undefined;
      body = (
        <g>
          <Character
            spec={spec}
            state={{ pose, prevPose, poseK, expr: e.expr as string, talk: !!e.talk, look: e.look as number, view: e.view as 'front' | 'back', seated: !!e.seated, kneel: !!e.kneel, walk, run, dir, headMove: e.headMove as string }}
            t={t}
            seed={seed}
            held={held}
          />
          {e.tag ? (
            <g transform="translate(0 30)">
              <rect x={-((e.tag as string).length * 11 + 20)} y={0} width={(e.tag as string).length * 22 + 40} height={40} fill="#fbf6e8" stroke={INK} strokeWidth={3} />
              <text y={30} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={26} fill={INK}>{(e.tag as string).toUpperCase()}</text>
            </g>
          ) : null}
        </g>
      );
      break;
    }
    case 'crowd': {
      const n = (e.count as number) ?? 8;
      const list = (e.who as string | string[]) ?? 'civilian_man';
      body = (
        <g>
          {Array.from({ length: n }, (_, i) => {
            const w = Array.isArray(list) ? list[i % list.length] : list;
            const spec = resolveCast(ctx.cast as never, w);
            const cx = (i - (n - 1) / 2) * ((e.spacing as number) ?? 110);
            const row = i % 2;
            return (
              <g key={i} transform={`translate(${cx} ${row * 26}) scale(${row ? 0.92 : 1})`}>
                <Character spec={spec} state={{ pose: (e.pose as string) ?? 'idle', expr: (e.expr as string) ?? 'neutral', walk: e.walk ? 1 : 0, dir: (e.dir as number) ?? 1, talk: !!e.talk }} t={t + i * 0.37} seed={seed + i} />
              </g>
            );
          })}
        </g>
      );
      break;
    }
    case 'prop':
      body = <Prop item={(e.item as string) ?? 'paper'} t={t} color={e.color as string} text={e.text as string} value={e.value as number} nationKey={e.nation as string} on={!!e.on} />;
      break;
    case 'flag':
      body = <Flag nation={(e.nation as string) ?? 'NEUTRAL'} w={(e.w as number) ?? 180} h={(e.h as number) ?? 120} t={t} still={!!e.still} />;
      break;
    case 'vehicle': {
      let moving = !!e.moving;
      let travel: number | undefined;
      if (el.keys?.some((kk) => 'x' in kk || 'at' in kk)) {
        const e2 = resolveKeys(el, keysUsed, t + 0.08) as ElementBase;
        if (Math.abs(((e2.x as number) ?? 0) - ((e.x as number) ?? 0)) > 0.3) moving = true;
        // distance travelled in the vehicle's own drawing units (drives wheel and track animation)
        travel = Math.abs(((e.x as number) ?? 0) - ((el.x as number) ?? 0)) / Math.max(0.05, (e.scale as number) ?? 1);
      } else if (moving) travel = t * 140;
      body = (
        <g>
          <Vehicle type={(e.type as string) ?? 'tank'} nationKey={e.nation as string} t={t} color={e.color as string} moving={moving} damaged={!!e.damaged} travel={travel} crew={!!e.crew} />
          {e.burning ? <g transform="translate(0 -80)"><Fx kind="fire" a={a} t={t} seed={seed} size={0.8} /><g transform="translate(20 -60)"><Fx kind="smoke" a={a} t={t} seed={seed} size={1} /></g></g> : null}
        </g>
      );
      break;
    }
    case 'fx':
      body = <Fx kind={(e.type as string) ?? 'smoke'} a={a} t={t} seed={seed} size={1} dir={e.dir as number} color={e.color as string} count={e.count as number} />;
      break;
    case 'label':
      body = <Label text={String(e.text ?? '')} style={e.style as string} size={e.size as number} color={e.color as string} tx={e.tx as number} ty={e.ty as number} rotate={e.tilt as number} />;
      break;
    case 'stamp':
      return (
        <g transform={`translate(${x} ${y}) scale(${s})`} opacity={op}>
          <Stamp text={String(e.text ?? '')} color={e.color as string} size={e.size as number} rotate={e.tilt as number} />
        </g>
      );
    case 'bubble':
      body = <Bubble text={String(e.text ?? '')} thought={!!e.thought} side={(e.side as number) ?? 1} size={e.size as number} a={a} />;
      break;
    case 'headline':
    case 'text':
      body = <Headline text={String(e.text ?? '')} size={e.size as number} color={e.color as string} accent={e.accent as string} a={a} font={e.font as string} />;
      break;
    case 'counter':
      body = <Counter from={e.from as number} to={(e.to as number) ?? 0} a={a} dur={e.dur as number} size={e.size as number} prefix={e.prefix as string} suffix={e.suffix as string} color={e.color as string} decimals={e.decimals as number} />;
      break;
    case 'document':
      body = <Document style={e.style as string} title={e.title as string} lines={e.lines as string[]} a={a} speed={e.speed as number} w={e.w as number} h={e.h as number} stamp={e.stamp as string} size={e.size as number} />;
      break;
    case 'namecard':
      return <g opacity={op}><NameCard name={String(e.name ?? e.text ?? '')} role={e.role as string} a={a} x={e.x as number} y={e.y as number} /></g>;
    case 'date':
      return <g opacity={op}><DateBadge text={String(e.text ?? '')} a={a} x={e.x as number} y={e.y as number} right={!!e.right} /></g>;
    case 'panel': {
      const w = (e.w as number) ?? 960, h = (e.h as number) ?? 1080;
      body = (
        <g>
          <rect x={0} y={0} width={w} height={h} fill={col(e.color, '#e9dfc4')} />
          {e.nation ? <rect x={0} y={0} width={w} height={h} fill={nation(e.nation as string).map} opacity={0.85} /> : null}
          {e.border !== false ? <rect x={0} y={0} width={w} height={h} fill="none" stroke={INK} strokeWidth={8} /> : null}
        </g>
      );
      return <g transform={`translate(${x - ((e.w as number) ?? 960) / 2} ${y - ((e.h as number) ?? 1080) / 2})`} opacity={op}>{body}</g>;
    }
    case 'shape': {
      const sh = (e.shape as string) ?? 'circle';
      const fill = col(e.fill ?? e.color, 'none');
      const stroke = col(e.stroke, INK);
      const sw = (e.strokeWidth as number) ?? 6;
      body = sh === 'rect' ? <rect x={-((e.w as number) ?? 200) / 2} y={-((e.h as number) ?? 120) / 2} width={(e.w as number) ?? 200} height={(e.h as number) ?? 120} rx={(e.rx as number) ?? 0} fill={fill} stroke={stroke} strokeWidth={sw} />
        : sh === 'ring' ? <circle r={((e.r as number) ?? 120) * (el.enter === 'draw' ? 1 : 1)} fill="none" stroke={col(e.color, C.red)} strokeWidth={sw} strokeDasharray={el.enter === 'draw' ? `${env.r * 2 * Math.PI * ((e.r as number) ?? 120)} 9999` : undefined} />
        : sh === 'cross' ? <path d="M-80 -80 L80 80 M80 -80 L-80 80" stroke={col(e.color, C.red)} strokeWidth={sw * 3} strokeLinecap="round" />
        : sh === 'check' ? <path d="M-80 0 L-20 60 L90 -70" stroke={col(e.color, C.green)} strokeWidth={sw * 3} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        : <circle r={(e.r as number) ?? 60} fill={fill} stroke={stroke} strokeWidth={sw} />;
      break;
    }
    case 'arrow': {
      const raw = (e.path as (number[])[]) ?? [];
      const pts: [number, number][] = ctx.proj && !e.screen ? raw.map((q) => P(ctx, q as LonLat) ?? [0, 0]) : raw.map((q) => [q[0], q[1]]);
      const r = el.enter === 'draw' || el.enter === undefined ? (e.progress as number) ?? env.r : (e.progress as number) ?? 1;
      return (
        <g opacity={op}>
          <Arrow pts={pts} r={el.enter === undefined && e.progress === undefined ? easeFn('inOut', clamp(a / ((e.dur as number) ?? 1.4))) : r} color={e.color as string} width={e.width as number} dashed={!!e.dashed} head={e.head !== false} />
          {e.label ? (() => {
            const mid = pts[Math.floor(pts.length / 2)] ?? [0, 0];
            return <g transform={`translate(${mid[0]} ${mid[1] - 60})`}><Label text={String(e.label)} style="plain" size={38} /></g>;
          })() : null}
        </g>
      );
    }
    case 'line':
    case 'route':
    case 'front': {
      const raw = (e.path as (number[])[]) ?? [];
      const pts: [number, number][] = ctx.proj && !e.screen ? raw.map((q) => P(ctx, q as LonLat) ?? [0, 0]) : raw.map((q) => [q[0], q[1]]);
      const sm = smoothPath(pts, 10);
      const r = el.enter === 'draw' ? env.r : (e.progress as number) ?? 1;
      const part = partialPolyline(sm, r);
      const c = col(e.color, k === 'front' ? C.red : INK);
      return (
        <g opacity={op}>
          {k === 'front' ? <path d={toD(part.pts)} stroke={INK} strokeWidth={((e.width as number) ?? 10) + 6} fill="none" strokeLinecap="round" /> : null}
          <path d={toD(part.pts)} stroke={c} strokeWidth={(e.width as number) ?? (k === 'route' ? 6 : 10)} fill="none" strokeLinecap="round" strokeDasharray={k === 'route' || e.dashed ? '18 14' : undefined} />
          {e.icon ? (
            <g transform={`translate(${part.tip[0]} ${part.tip[1]}) rotate(${(part.angle * 180) / Math.PI})`}>
              <MapIcon type={e.icon as string} nationKey={e.nation as string} t={t} size={(e.iconSize as number) ?? 0.8} />
            </g>
          ) : null}
        </g>
      );
    }
    case 'region':
    case 'pocket': {
      const raw = (e.polygon as (number[])[]) ?? [];
      const pts: [number, number][] = ctx.proj && !e.screen ? raw.map((q) => P(ctx, q as LonLat) ?? [0, 0]) : raw.map((q) => [q[0], q[1]]);
      const sm = smoothPath([...pts, pts[0]], 10);
      const c = col(e.color, k === 'pocket' ? C.red : C.grey);
      const glow = k === 'pocket' ? 0.5 + 0.5 * Math.sin(t * 4) : 0;
      return (
        <g opacity={op}>
          <path d={toD(sm) + 'Z'} fill={c} fillOpacity={(e.fillOpacity as number) ?? 0.35} stroke={k === 'pocket' ? '#fff' : c} strokeWidth={k === 'pocket' ? 6 : 4} strokeDasharray={e.dashed ? '16 12' : undefined} />
          {k === 'pocket' ? <path d={toD(sm) + 'Z'} fill="none" stroke={c} strokeWidth={14} strokeOpacity={0.3 + glow * 0.3} /> : null}
        </g>
      );
    }
    case 'city': {
      const capital = !!e.capital;
      const side = (e.side as string) ?? 'right';
      const size = (e.size as number) ?? 26;
      const name = String(e.name ?? e.text ?? '');
      const tag = !!e.tag;
      const lx = side === 'left' ? -14 : side === 'top' || side === 'bottom' ? 0 : 14;
      const ly = side === 'top' ? -18 : side === 'bottom' ? size + 12 : size * 0.36;
      const anchor = side === 'left' ? 'end' : side === 'right' ? 'start' : 'middle';
      const font = e.font === 'hand' ? FONT.hand : FONT.cond;
      const label = (tag || e.upper !== false) && e.font !== 'hand' ? name.toUpperCase() : name;
      const tw = label.length * size * 0.62 + size * 0.9;
      const tx = anchor === 'start' ? lx - size * 0.3 : anchor === 'end' ? lx - tw + size * 0.3 : -tw / 2;
      body = (
        <g>
          {capital ? <path d="M0 -12 L3.5 -4 L12 -4 L5 1.5 L7.5 10 L0 5 L-7.5 10 L-5 1.5 L-12 -4 L-3.5 -4 Z" fill={C.red} stroke={INK} strokeWidth={2.4} /> : <circle r={6.5} fill={INK} stroke="#f4ecd8" strokeWidth={2.5} />}
          {tag ? (
            <g>
              <rect x={tx + 3} y={ly - size * 0.95 + 4} width={tw} height={size * 1.35} fill="#000" opacity={0.22} />
              <rect x={tx} y={ly - size * 0.95} width={tw} height={size * 1.35} fill="#f6f1e4" stroke={INK} strokeWidth={2.5} />
            </g>
          ) : null}
          <text x={tag ? tx + tw / 2 : lx} y={ly} textAnchor={tag ? 'middle' : anchor} fontFamily={font} fontWeight={600} fontSize={size} letterSpacing={tag ? 2 : 3} fill={INK} stroke={tag ? 'none' : '#efe4c8'} strokeOpacity={0.7} strokeWidth={5} paintOrder="stroke">{label}</text>
        </g>
      );
      break;
    }
    case 'unit':
      body = <Unit type={e.type as string} nationKey={e.nation as string} label={e.label as string} color={e.color as string} />;
      break;
    case 'icon':
    case 'ship':
      body = <MapIcon type={(e.type as string) ?? 'ship'} nationKey={e.nation as string} color={e.color as string} label={e.label as string} t={t} burning={!!e.burning} />;
      break;
    case 'legend': {
      // map legend box: flag + name rows (bottom-left by default, hud)
      const items = (e.items as { nation?: string; label: string; color?: string }[]) ?? [];
      const w = Math.max(...items.map((it) => it.label.length * 17 + 110), 220);
      const h = 30 + items.length * 46;
      body = (
        <g>
          <rect x={4} y={6} width={w} height={h} rx={6} fill="#000" opacity={0.18} />
          <rect x={0} y={0} width={w} height={h} rx={6} fill="#f4ecd8" stroke={INK} strokeWidth={4} />
          {items.map((it, i) => (
            <g key={i} transform={`translate(18 ${18 + i * 46})`}>
              {it.nation ? <Flag nation={it.nation} w={54} h={36} t={t} still /> : <rect width={54} height={36} fill={col(it.color, C.grey)} stroke={INK} strokeWidth={2} />}
              <text x={70} y={28} fontFamily={FONT.cond} fontWeight={700} fontSize={28} fill={INK}>{it.label.toUpperCase()}</text>
            </g>
          ))}
        </g>
      );
      break;
    }
    case 'blocks': {
      // quantity as objects: a grid of small division blocks + optional "≈160" tag
      const n = (e.count as number) ?? 20, cols = (e.cols as number) ?? Math.ceil(Math.sqrt(n * 1.6));
      const c = col(e.color, uiColor(e.nation as string));
      const sz = (e.size as number) ?? 16;
      const rows = Math.ceil(n / cols);
      const shown = Math.min(n, Math.floor(n * clamp(a / ((e.dur as number) ?? 1.2))));
      body = (
        <g transform={`translate(${(-cols * (sz + 3)) / 2} ${(-rows * (sz + 3)) / 2})`}>
          {Array.from({ length: shown }, (_, i) => (
            <rect key={i} x={(i % cols) * (sz + 3)} y={Math.floor(i / cols) * (sz + 3)} width={sz} height={sz} rx={2} fill={c} stroke={INK} strokeWidth={1.6} />
          ))}
          {e.label ? (
            <g transform={`translate(${cols * (sz + 3) + 16} ${(rows * (sz + 3)) / 2 - 24})`}>
              <rect width={String(e.label).length * 22 + 30} height={48} rx={4} fill="#f4ecd8" stroke={INK} strokeWidth={3} />
              <text x={15} y={35} fontFamily={FONT.heavy} fontSize={34} fill={INK}>{String(e.label)}</text>
            </g>
          ) : null}
        </g>
      );
      break;
    }
    case 'paras': {
      // parachutists drifting down under round canopies (count, spread px, fall px, dur s, color)
      const n = (e.count as number) ?? 12, spread = (e.spread as number) ?? 1400, fall = (e.fall as number) ?? 700, pd = (e.pdur as number) ?? 6;
      const canopy = col(e.color, '#e9e4cf');
      body = (
        <g>
          {Array.from({ length: n }, (_, i) => {
            const delay = rnd(seed, i, 'd') * pd * 0.6;
            if (a < delay) return null;
            const k = clamp((a - delay) / pd);
            const px = (rnd(seed, i) - 0.5) * spread + Math.sin(t * 0.8 + i) * 20 + k * 80;
            const py = -fall / 2 + k * fall + rnd(seed, i, 'y') * 120;
            const sc = 0.6 + rnd(seed, i, 's') * 0.5;
            const sway = Math.sin(t * 1.6 + i) * 6;
            return (
              <g key={i} transform={`translate(${px} ${py}) scale(${sc}) rotate(${sway})`}>
                <path d="M-60 -60 Q0 -130 60 -60 Q30 -70 0 -66 Q-30 -70 -60 -60 Z" fill={i % 5 === 0 ? '#c9a24a' : canopy} stroke={INK} strokeWidth={4} />
                <path d="M-58 -60 L-6 0 M58 -60 L6 0 M0 -66 L0 0" stroke={INK} strokeWidth={2} />
                <circle cx={0} cy={6} r={9} fill="#6b7a4a" stroke={INK} strokeWidth={3} />
                <rect x={-8} y={14} width={16} height={22} rx={5} fill="#7a7254" stroke={INK} strokeWidth={3} />
                <path d="M-4 36 L-6 52 M4 36 L6 52" stroke={INK} strokeWidth={5} strokeLinecap="round" />
              </g>
            );
          })}
        </g>
      );
      break;
    }
    case 'torn': {
      // torn-paper band (thumbnail text background): coloured sheet with a white ragged border
      const tw = (e.w as number) ?? 900, th = (e.h as number) ?? 300;
      const rag = (w2: number, h2: number, k: string, amp: number) => {
        const pts: string[] = [];
        const nx = 28, ny = 10;
        for (let i = 0; i <= nx; i++) pts.push(`${-w2 / 2 + (i * w2) / nx} ${-h2 / 2 + (rnd(k, 't', i) - 0.5) * amp}`);
        for (let i = 0; i <= ny; i++) pts.push(`${w2 / 2 + (rnd(k, 'r', i) - 0.5) * amp} ${-h2 / 2 + (i * h2) / ny}`);
        for (let i = nx; i >= 0; i--) pts.push(`${-w2 / 2 + (i * w2) / nx} ${h2 / 2 + (rnd(k, 'b', i) - 0.5) * amp}`);
        for (let i = ny; i >= 0; i--) pts.push(`${-w2 / 2 + (rnd(k, 'l', i) - 0.5) * amp} ${-h2 / 2 + (i * h2) / ny}`);
        return 'M' + pts.join(' L') + ' Z';
      };
      body = (
        <g>
          <path d={rag(tw + 10, th + 10, seed + 'o', 40)} fill="#000" opacity={0.3} transform="translate(10 14)" />
          <path d={rag(tw + 36, th + 36, seed + 'w', 34)} fill="#fbf8f0" />
          <path d={rag(tw, th, seed + 'c', 26)} fill={col(e.color, C.red)} />
        </g>
      );
      break;
    }
    case 'drop': {
      // big cartoon sweat / tear drop
      const sz = (e.size as number) ?? 1;
      const fall = e.falling ? ((t * 0.8) % 1) * 60 : 0;
      body = (
        <g transform={`translate(0 ${fall}) scale(${sz})`} opacity={e.falling ? 1 - ((t * 0.8) % 1) * 0.6 : 1}>
          <path d="M0 -60 Q-34 -6 -34 16 A34 34 0 0 0 34 16 Q34 -6 0 -60 Z" fill={col(e.color, '#6fc3f2')} stroke={INK} strokeWidth={6} strokeLinejoin="round" />
          <path d="M-14 4 Q-16 20 -4 28" stroke="#fff" strokeWidth={7} fill="none" strokeLinecap="round" opacity={0.85} />
        </g>
      );
      break;
    }
    case 'hand': {
      // giant pointing hand with a sleeve: points to +x (use rotate / flip)
      const sl = col(e.sleeve, '#2f3036'), sk = col(e.skin, '#f6dcc4');
      body = (
        <g>
          <path d="M-900 -46 L-60 -46 L-60 46 L-900 46 Z" fill={sl} stroke={INK} strokeWidth={7} />
          <path d="M-80 -54 H-40 V54 H-80 Z" fill="#f2efe6" stroke={INK} strokeWidth={6} />
          <path d="M-42 -40 Q20 -52 60 -36 L190 -38 Q214 -36 214 -18 Q214 0 190 0 L96 2 Q104 22 92 40 Q60 62 -10 54 Q-46 48 -42 20 Z" fill={sk} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
          <path d="M30 2 Q60 6 92 4 M24 26 Q56 30 86 24" stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />
          <path d="M-10 -40 Q10 -70 46 -60 Q60 -50 50 -36" fill={sk} stroke={INK} strokeWidth={6} />
        </g>
      );
      break;
    }
    case 'glow': {
      const gid = 'glow_' + seed.replace(/[^a-z0-9]/gi, '');
      body = (
        <g>
          <defs>
            <radialGradient id={gid}>
              <stop offset="0" stopColor={col(e.color, '#fff3c0')} stopOpacity={(e.strength as number) ?? 0.85} />
              <stop offset="1" stopColor={col(e.color, '#fff3c0')} stopOpacity={0} />
            </radialGradient>
          </defs>
          <circle r={(e.r as number) ?? 500} fill={`url(#${gid})`} />
        </g>
      );
      break;
    }
    case 'burst':
      body = <Fx kind="explosion" a={a} t={t} seed={seed} size={(e.size as number) ?? 0.5} />;
      break;
    case 'ring': {
      // radius in km on maps, px on stage
      let rpx = (e.r as number) ?? 100;
      if (ctx.proj && e.at && e.km) {
        const q = P(ctx, [(e.at as number[])[0], (e.at as number[])[1] + (e.km as number) / 111]);
        if (q) rpx = Math.abs(q[1] - y);
      }
      return (
        <g transform={`translate(${x} ${y})`} opacity={op}>
          <circle r={rpx * env.s} fill={col(e.fill, 'none')} fillOpacity={0.15} stroke={col(e.color, C.red)} strokeWidth={(e.width as number) ?? 6} strokeDasharray={e.dashed !== false ? '20 14' : undefined} />
        </g>
      );
    }
    case 'scale':
      body = <ScaleDevice t={t} left={e.left as string} right={e.right as string} leftNation={e.leftNation as string} rightNation={e.rightNation as string} items={e.items as never} title={e.title as string} tilt={e.tilt as number} />;
      break;
    case 'meter':
      body = <MeterDevice t={t} value={e.value as number} left={e.left as string} right={e.right as string} title={e.title as string} leftColor={e.leftColor as string} rightColor={e.rightColor as string} />;
      break;
    case 'bars':
      body = <BarsDevice t={t} items={e.items as never} max={e.max as number} unit={e.unit as string} title={e.title as string} width={e.width as number} />;
      break;
    case 'score':
    case 'scoreboard':
      body = <ScoreDevice t={t} sides={e.sides as never} title={e.title as string} scores={e.scores as number[]} />;
      break;
    case 'road':
      body = <RoadDevice t={t} progress={e.progress as number} exits={e.exits as never} towns={e.towns as never} vehicle={e.vehicle as string} nation={e.nation as string} length={e.length as number} color={e.color as string} sea={!!e.sea} polder={!!e.polder} vehicles={e.vehicles as number} time={e.time as string} />;
      break;
    case 'ranking':
      body = <RankingDevice t={t} items={e.items as never} highlight={e.highlight as number} title={e.title as string} />;
      break;
    case 'timeline':
      body = <TimelineDevice t={t} items={e.items as never} cursor={e.cursor as number} width={e.width as number} start={e.start as string} end={e.end as string} />;
      break;
    case 'ledger':
      body = <LedgerDevice t={t} columns={e.columns as never} />;
      break;
    default:
      body = <text fontSize={30} fill="red">{`?${k}`}</text>;
  }
  return (
    <g transform={tr} opacity={op}>
      {body}
    </g>
  );
};
