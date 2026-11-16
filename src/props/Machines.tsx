import React from 'react';
import { INK, nation } from '../theme';
import { Mark } from './Vehicles';

/**
 * Soft-skins, aircraft and ships drawn with volume (same finish as Tanks.tsx):
 * - every body has a vertical light→dark gradient (lit top, shaded belly);
 * - wheels have tyres, hubs and bolts and turn with the distance travelled;
 * - aircraft: two-tone camouflage per nation, framed canopy with glint, spinning propeller disc;
 * - ships: sheer line, waterline boot-topping, layered superstructure, turrets, funnels with smoke, bow wave + wake.
 * Side view facing right; origin = ground/waterline contact centre (aircraft: fuselage centre).
 */

const shade = (hex: string, k: number) => {
  const m = hex.replace('#', '');
  if (m.length !== 6) return hex;
  const n = parseInt(m, 16);
  const f = (v: number) => Math.max(0, Math.min(255, Math.round(k < 0 ? v * (1 + k) : v + (255 - v) * k)));
  return '#' + ((1 << 24) | (f((n >> 16) & 255) << 16) | (f((n >> 8) & 255) << 8) | f(n & 255)).toString(16).slice(1);
};

/** vertical volume gradient (objectBoundingBox): lit top, base, dark bottom. Same id for same colour → safe to repeat. */
const gid = (c: string, k = 'v') => `${k}_${c.replace('#', '')}`;
const VGrad: React.FC<{ c: string; k?: string; lift?: number; drop?: number }> = ({ c, k = 'v', lift = 0.22, drop = -0.3 }) => (
  <linearGradient id={gid(c, k)} x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stopColor={shade(c, lift)} />
    <stop offset="0.42" stopColor={c} />
    <stop offset="1" stopColor={shade(c, drop)} />
  </linearGradient>
);
const fillOf = (c: string, k = 'v') => `url(#${gid(c, k)})`;
const GLASS = '#9fc0cc';

const Wheel: React.FC<{ x: number; y: number; r: number; rot: number; hub?: string }> = ({ x, y, r, rot, hub = '#5e5c50' }) => (
  <g transform={`translate(${x} ${y})`}>
    <circle r={r} fill="#24221f" stroke={INK} strokeWidth={3} />
    <g transform={`rotate(${rot})`}>
      <circle r={r - 3.5} fill="none" stroke="#3b3833" strokeWidth={3.2} strokeDasharray="4 4.5" />
      <circle r={r * 0.56} fill={hub} stroke={INK} strokeWidth={2.5} />
      {Array.from({ length: 5 }, (_, i) => {
        const a = (i / 5) * Math.PI * 2;
        return <circle key={i} cx={Math.cos(a) * r * 0.34} cy={Math.sin(a) * r * 0.34} r={Math.max(1.4, r * 0.06)} fill={shade(hub, -0.45)} />;
      })}
      <circle r={r * 0.15} fill={shade(hub, -0.35)} />
    </g>
    <path d={`M${-r * 0.42} ${-r * 0.3} A${r * 0.52} ${r * 0.52} 0 0 1 ${r * 0.3} ${-r * 0.44}`} stroke="#fff" strokeOpacity={0.25} strokeWidth={2.5} fill="none" strokeLinecap="round" />
  </g>
);

/** exhaust puffs trailing behind a moving vehicle */
const Exhaust: React.FC<{ x: number; y: number; t: number; on: boolean; c?: string }> = ({ x, y, t, on, c = '#8d8a82' }) =>
  on ? (
    <g>
      {[0, 1, 2, 3].map((i) => {
        const k = (t * 1.6 + i / 4) % 1;
        return <circle key={i} cx={x - k * 70} cy={y - k * 26} r={5 + k * 14} fill={c} opacity={0.4 * (1 - k)} />;
      })}
    </g>
  ) : null;

/** dust kicked up by wheels */
const Dust: React.FC<{ x: number; t: number; on: boolean; w?: number }> = ({ x, t, on, w = 1 }) =>
  on ? (
    <g>
      {[0, 1, 2].map((i) => {
        const k = (t * 1.3 + i / 3) % 1;
        return <ellipse key={i} cx={x - k * 90 * w} cy={-8 - k * 18} rx={(12 + k * 26) * w} ry={(6 + k * 10) * w} fill="#b8a684" opacity={0.35 * (1 - k)} />;
      })}
    </g>
  ) : null;

const Head: React.FC<{ x: number; y: number; helmet: string; t: number; i?: number }> = ({ x, y, helmet, t, i = 0 }) => (
  <g transform={`translate(${x} ${y + Math.sin(t * 7 + i) * 0.8})`}>
    <rect x={-11} y={2} width={22} height={18} rx={6} fill={shade(helmet, -0.1)} stroke={INK} strokeWidth={2.5} />
    <circle cx={0} cy={-6} r={11} fill="#f2d5bf" stroke={INK} strokeWidth={2.5} />
    <path d="M-15 -8 Q-14 -24 0 -24 Q14 -24 15 -8 Z" fill={helmet} stroke={INK} strokeWidth={2.5} strokeLinejoin="round" />
  </g>
);

type MP = { type: string; nationKey?: string; color?: string; t: number; travel: number; moving: boolean; damaged?: boolean; crew?: boolean };

// ---------------------------------------------------------------- ground vehicles
const Truck: React.FC<MP> = ({ nationKey, color, t, travel, moving, damaged }) => {
  const n = nation(nationKey);
  const body = color ?? n.uniform;
  const canvas = shade(body, 0.12);
  const ger = nationKey === 'GER' || nationKey === 'GERI';
  const rot = (travel / 26) * (180 / Math.PI);
  const bob = moving ? Math.sin(travel / 11) * 1.3 : 0;
  return (
    <g>
      <defs>
        <VGrad c={body} />
        <VGrad c={canvas} k="c" lift={0.28} drop={-0.22} />
        <VGrad c={shade(body, -0.08)} />
      </defs>
      <ellipse cx={0} cy={4} rx={215} ry={9} fill="#000" opacity={0.2} />
      <Dust x={-170} t={t} on={moving} />
      <Exhaust x={-214} y={-60} t={t} on={moving} />
      <g transform={`translate(0 ${bob})`}>
        <rect x={-206} y={-64} width={398} height={12} rx={3} fill="#2b2926" stroke={INK} strokeWidth={3} />
        {/* cargo bed: wooden sides + canvas tilt on hoops */}
        <path d="M-208 -62 V-112 H30 V-62 Z" fill={fillOf(shade(body, -0.08))} stroke={INK} strokeWidth={4} />
        {[-176, -136, -96, -56, -16].map((x) => <path key={x} d={`M${x} -110 V-64`} stroke={INK} strokeOpacity={0.22} strokeWidth={2.5} />)}
        <path d="M-208 -96 H30" stroke={INK} strokeOpacity={0.25} strokeWidth={2.5} />
        <path d="M-212 -110 V-176 Q-212 -196 -192 -197 H14 Q34 -196 34 -176 V-110 Z" fill={fillOf(canvas, 'c')} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
        {[-150, -92, -34].map((x) => <path key={x} d={`M${x} -196 Q${x + 4} -152 ${x} -112`} stroke={INK} strokeOpacity={0.28} strokeWidth={3} fill="none" />)}
        <path d="M-206 -186 Q-90 -192 28 -186" stroke="#fff" strokeOpacity={0.22} strokeWidth={6} fill="none" strokeLinecap="round" />
        <path d="M-210 -116 H32" stroke={INK} strokeWidth={2} strokeDasharray="5 9" opacity={0.5} />
        {/* cab + bonnet */}
        <path d={ger ? 'M34 -62 V-150 Q36 -168 56 -168 H100 Q112 -164 118 -128 L170 -122 Q192 -118 194 -96 V-62 Z' : 'M34 -62 V-160 Q34 -168 42 -168 H104 L118 -124 L180 -118 Q192 -116 192 -104 V-62 Z'} fill={fillOf(body)} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
        <path d={ger ? 'M50 -158 H98 Q106 -150 110 -128 H50 Z' : 'M48 -158 H100 L110 -128 H48 Z'} fill={GLASS} stroke={INK} strokeWidth={3} strokeLinejoin="round" />
        <path d="M60 -134 L80 -154 M74 -134 L88 -148" stroke="#fff" strokeOpacity={0.55} strokeWidth={3} strokeLinecap="round" />
        <path d="M44 -124 V-66 M112 -122 V-66" stroke={INK} strokeOpacity={0.35} strokeWidth={2.5} />
        <path d="M120 -122 L180 -116" stroke="#fff" strokeOpacity={0.25} strokeWidth={4} strokeLinecap="round" />
        {[130, 142, 154, 166].map((x) => <path key={x} d={`M${x} -112 V-88`} stroke={INK} strokeOpacity={0.3} strokeWidth={2} />)}
        <rect x={186} y={-114} width={10} height={48} rx={2} fill="#2b2926" stroke={INK} strokeWidth={2.5} />
        <circle cx={178} cy={-104} r={8} fill="#e9e2c6" stroke={INK} strokeWidth={2.5} />
        <rect x={176} y={-68} width={26} height={10} rx={2} fill="#2b2926" stroke={INK} strokeWidth={2.5} />
        {/* fenders over the wheels */}
        <path d="M84 -52 Q88 -86 122 -88 Q156 -86 160 -52" fill={fillOf(body)} stroke={INK} strokeWidth={4} />
        <rect x={-190} y={-70} width={134} height={10} rx={3} fill={shade(body, -0.25)} stroke={INK} strokeWidth={3} />
        <rect x={-30} y={-58} width={44} height={18} rx={8} fill={shade(body, -0.2)} stroke={INK} strokeWidth={2.5} />
        <Wheel x={-150} y={-26} r={26} rot={rot} />
        <Wheel x={-92} y={-26} r={26} rot={rot} />
        <Wheel x={122} y={-26} r={26} rot={rot} />
        <Mark nationKey={nationKey} x={76} y={-96} s={0.8} />
        {damaged ? <path d="M-150 -180 l30 40 l-14 6 l36 46" stroke={INK} strokeWidth={4} fill="none" /> : null}
      </g>
    </g>
  );
};

const Jeep: React.FC<MP> = ({ nationKey, color, t, travel, moving, crew }) => {
  const n = nation(nationKey);
  const body = color ?? n.uniform;
  const ger = nationKey === 'GER' || nationKey === 'GERI';
  const rot = (travel / 24) * (180 / Math.PI);
  const bob = moving ? Math.sin(travel / 9) * 1.6 : 0;
  const helmet = n.uniformDark;
  return (
    <g>
      <defs><VGrad c={body} /></defs>
      <ellipse cx={0} cy={4} rx={140} ry={8} fill="#000" opacity={0.2} />
      <Dust x={-100} t={t} on={moving} w={0.8} />
      <Exhaust x={-128} y={-40} t={t} on={moving} />
      <g transform={`translate(0 ${bob})`}>
        {ger ? (
          // Kübelwagen: slab sides, ribbed panels, folded hood
          <g>
            <path d="M-122 -40 L-128 -86 L-40 -92 L52 -92 L110 -84 L134 -60 L130 -40 Z" fill={fillOf(body)} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
            {[-100, -80, -60].map((x) => <path key={x} d={`M${x} -84 V-48`} stroke={INK} strokeOpacity={0.25} strokeWidth={2.5} />)}
            <path d="M-120 -96 Q-110 -110 -80 -108 L-60 -94 Z" fill={shade(body, -0.3)} stroke={INK} strokeWidth={3} />
            <path d="M36 -92 L26 -132 H34 L46 -92" fill="none" stroke={INK} strokeWidth={4} />
            <path d="M30 -128 L40 -96" stroke={GLASS} strokeWidth={6} opacity={0.7} />
          </g>
        ) : (
          // Willys jeep: low tub, door cut-out, flat bonnet, spare wheel on the back
          <g>
            <Wheel x={-128} y={-64} r={20} rot={0} />
            <path d="M-120 -40 V-86 Q-120 -92 -112 -92 H-36 Q-30 -72 -14 -72 H34 Q40 -90 50 -92 H122 Q132 -90 134 -78 V-40 Z" fill={fillOf(body)} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
            <path d="M54 -90 H124" stroke="#fff" strokeOpacity={0.25} strokeWidth={4} strokeLinecap="round" />
            {[110, 118, 126].map((x) => <path key={x} d={`M${x} -84 V-58`} stroke={INK} strokeOpacity={0.3} strokeWidth={2.5} />)}
            <path d="M44 -92 L32 -142 H40 L52 -92" fill="none" stroke={INK} strokeWidth={4} strokeLinejoin="round" />
            <path d="M38 -138 L48 -96" stroke={GLASS} strokeWidth={6} opacity={0.6} />
            <path d="M58 -54 Q66 -74 92 -74 Q118 -74 126 -54" fill="none" stroke={INK} strokeWidth={4} />
            <circle cx={130} cy={-74} r={6} fill="#e9e2c6" stroke={INK} strokeWidth={2} />
          </g>
        )}
        <rect x={-70} y={-118} width={12} height={30} rx={3} fill={shade(body, -0.3)} stroke={INK} strokeWidth={2.5} />
        {crew ? <><Head x={-6} y={-110} helmet={helmet} t={t} /><Head x={-62} y={-112} helmet={helmet} t={t} i={2} /></> : null}
        <Wheel x={-72} y={-24} r={24} rot={rot} />
        <Wheel x={84} y={-24} r={24} rot={rot} />
        <Mark nationKey={nationKey} x={-90} y={-64} s={0.7} />
      </g>
    </g>
  );
};

const Halftrack: React.FC<MP> = ({ nationKey, color, t, travel, moving, damaged, crew }) => {
  const n = nation(nationKey);
  const body = color ?? n.uniform;
  const ger = nationKey === 'GER' || nationKey === 'GERI';
  const rot = (travel / 18) * (180 / Math.PI);
  const frot = (travel / 30) * (180 / Math.PI);
  const bob = moving ? Math.sin(travel / 13) * 1.2 : 0;
  const link = -(travel % 14);
  return (
    <g>
      <defs><VGrad c={body} /></defs>
      <ellipse cx={0} cy={4} rx={200} ry={9} fill="#000" opacity={0.2} />
      <Dust x={-160} t={t} on={moving} />
      <Exhaust x={-196} y={-60} t={t} on={moving} />
      {/* track unit */}
      <path d="M-170 -2 Q-196 -2 -196 -26 Q-196 -50 -170 -50 H10 Q30 -50 30 -26 Q30 -2 10 -2 Z" fill="#2a2724" stroke={INK} strokeWidth={4} />
      <path d="M-170 -2 Q-196 -2 -196 -26 Q-196 -50 -170 -50 H10 Q30 -50 30 -26 Q30 -2 10 -2 Z" fill="none" stroke="#4a4640" strokeWidth={4} strokeDasharray="7 7" strokeDashoffset={link} />
      {[-150, -110, -70, -30].map((x) => <Wheel key={x} x={x} y={-24} r={17} rot={rot} hub={shade(body, -0.1)} />)}
      <Wheel x={10} y={-26} r={14} rot={rot} hub="#3a3833" />
      <Wheel x={-176} y={-26} r={13} rot={rot} hub="#3a3833" />
      <g transform={`translate(0 ${bob})`}>
        <path d={ger ? 'M-196 -46 L-184 -104 L40 -116 L84 -100 L168 -86 L182 -56 L-196 -46 Z' : 'M-190 -46 V-108 H44 L60 -102 L116 -100 Q156 -98 176 -84 L182 -50 Z'} fill={fillOf(body)} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
        <path d={ger ? 'M-182 -100 L40 -112 L80 -98' : 'M-186 -104 H44'} stroke="#fff" strokeOpacity={0.28} strokeWidth={5} fill="none" strokeLinecap="round" />
        <path d={ger ? 'M-186 -76 L60 -84' : 'M-186 -80 H40'} stroke={INK} strokeOpacity={0.3} strokeWidth={2.5} />
        {ger ? [-150, -100, -50].map((x) => <rect key={x} x={x} y={-72} width={40} height={18} rx={2} fill={shade(body, -0.12)} stroke={INK} strokeWidth={2.5} />) : <rect x={-40} y={-98} width={60} height={46} rx={3} fill="none" stroke={INK} strokeOpacity={0.4} strokeWidth={2.5} />}
        <path d="M66 -96 L80 -122 H96 L104 -100" fill={GLASS} stroke={INK} strokeWidth={3} opacity={0.85} />
        {!ger ? <rect x={176} y={-76} width={22} height={30} rx={8} fill="#3a3833" stroke={INK} strokeWidth={3} /> : null}
        <circle cx={168} cy={-82} r={7} fill="#e9e2c6" stroke={INK} strokeWidth={2.5} />
        {/* machine gun on its mount */}
        <path d="M-40 -110 V-132" stroke="#2b2926" strokeWidth={6} />
        <path d="M-52 -136 L30 -142" stroke="#2b2926" strokeWidth={7} strokeLinecap="round" />
        {crew ? <><Head x={-110} y={-124} helmet={n.uniformDark} t={t} /><Head x={-58} y={-128} helmet={n.uniformDark} t={t} i={3} /></> : null}
        <path d="M90 -54 Q96 -86 130 -88 Q162 -86 168 -54" fill={fillOf(body)} stroke={INK} strokeWidth={4} />
        <Wheel x={128} y={-30} r={30} rot={frot} />
        <Mark nationKey={nationKey} x={-120} y={-80} s={0.95} />
        {damaged ? <path d="M-40 -100 l20 30 l-10 10 l30 20" stroke={INK} strokeWidth={4} fill="none" /> : null}
      </g>
    </g>
  );
};

const FieldGun: React.FC<MP> = ({ nationKey, color, t }) => {
  const n = nation(nationKey);
  const body = color ?? n.uniform;
  const recoil = 0;
  void t;
  return (
    <g>
      <defs><VGrad c={body} /><VGrad c={shade(body, -0.15)} /><VGrad c="#4b4b44" /></defs>
      <ellipse cx={-40} cy={4} rx={150} ry={8} fill="#000" opacity={0.2} />
      {/* split trail to the ground */}
      <path d="M-20 -40 L-180 -4 L-176 6 L-12 -28 Z" fill={fillOf(shade(body, -0.15))} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      <path d="M-182 -6 l-10 8 h26 z" fill="#2b2926" stroke={INK} strokeWidth={2.5} />
      {/* barrel with recoil cylinder */}
      <g transform={`translate(${-recoil} 0) rotate(-14 0 -66)`}>
        <rect x={-30} y={-76} width={130} height={16} rx={4} fill={fillOf(body)} stroke={INK} strokeWidth={3.5} />
        <rect x={-36} y={-72} width={250} height={11} rx={3} fill={fillOf('#4b4b44')} stroke={INK} strokeWidth={3.5} />
        <rect x={208} y={-74} width={16} height={15} rx={3} fill="#3b3b35" stroke={INK} strokeWidth={3} />
      </g>
      {/* shield */}
      <path d="M-8 -104 L40 -112 L46 -44 L-4 -38 Z" fill={fillOf(body)} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      <path d="M0 -98 L36 -104" stroke="#fff" strokeOpacity={0.3} strokeWidth={4} />
      <Wheel x={10} y={-34} r={34} rot={0} hub={shade(body, -0.05)} />
    </g>
  );
};

// ---------------------------------------------------------------- aircraft
type AirLook = { top: string; belly: string; nose?: string; spinner: string; band?: string };
const airLook = (nationKey?: string, color?: string): AirLook => {
  if (color) return { top: color, belly: shade(color, 0.35), spinner: shade(color, -0.3) };
  switch (nationKey) {
    case 'UK': return { top: '#5f6a45', belly: '#b9b9a6', spinner: '#2b2926', band: '#c9c3a0' };
    case 'USA': return { top: '#b9bdc1', belly: '#d2d5d8', nose: '#5f6a45', spinner: '#c8352b' };
    case 'GER': case 'GERI': return { top: '#6f7a72', belly: '#a9bccb', nose: '#d6b23a', spinner: '#2b2926' };
    case 'JPN': return { top: '#cfc9ad', belly: '#d9d4bd', nose: '#2b2926', spinner: '#6b5a3a' };
    case 'USSR': return { top: '#5a6a40', belly: '#a8bccb', spinner: '#c8352b' };
    case 'ITA': return { top: '#b59a64', belly: '#b8b9b0', spinner: '#2b2926' };
    default: return { top: '#7a8a9a', belly: '#b9c4cc', spinner: '#2b2926' };
  }
};

const Prop: React.FC<{ x: number; y: number; r: number; t: number; c: string }> = ({ x, y, r, t, c }) => (
  <g transform={`translate(${x} ${y})`}>
    <ellipse rx={5} ry={r} fill="#6a6660" opacity={0.28} />
    <path d={`M0 0 L${Math.sin(t * 60) * 3} ${-r * Math.cos(t * 60)}`} stroke="#3a3833" strokeWidth={5} opacity={0.35} strokeLinecap="round" />
    <path d="M-8 -9 Q10 -10 14 0 Q10 10 -8 9 Z" fill={c} stroke={INK} strokeWidth={2.5} />
  </g>
);

const Canopy: React.FC<{ d: string; frames: string }> = ({ d, frames }) => (
  <g>
    <path d={d} fill={GLASS} stroke={INK} strokeWidth={3} strokeLinejoin="round" />
    <path d={frames} stroke={INK} strokeWidth={2.2} opacity={0.75} fill="none" />
  </g>
);

const Fighter: React.FC<MP> = ({ nationKey, color, t }) => {
  const L = airLook(nationKey, color);
  const uk = nationKey === 'UK';
  const ger = nationKey === 'GER' || nationKey === 'GERI';
  // fuselage: nose right
  const fus = 'M-150 -12 Q-154 -22 -138 -24 L60 -30 Q120 -30 146 -14 Q150 -4 146 6 Q118 14 60 14 L-130 4 Q-152 2 -150 -12 Z';
  return (
    <g>
      <defs><VGrad c={L.top} k="t" lift={0.25} drop={-0.15} /></defs>
      {/* far wing hint */}
      <path d="M-10 -14 L70 -18 L86 -30 L4 -26 Z" fill={shade(L.top, -0.3)} stroke={INK} strokeWidth={2.5} strokeLinejoin="round" />
      {/* tail fin + tailplane */}
      <path d={ger ? 'M-130 -20 L-148 -64 L-118 -64 L-100 -26 Z' : uk ? 'M-128 -22 Q-150 -66 -122 -66 Q-104 -62 -98 -26 Z' : 'M-130 -22 L-146 -70 Q-124 -72 -112 -60 L-96 -26 Z'} fill={fillOf(L.top, 't')} stroke={INK} strokeWidth={3.5} strokeLinejoin="round" />
      <path d="M-148 -4 L-108 -6 L-122 10 L-152 8 Z" fill={shade(L.top, -0.12)} stroke={INK} strokeWidth={3} strokeLinejoin="round" />
      {/* body: top colour + belly colour */}
      <path d={fus} fill={L.belly} stroke={INK} strokeWidth={4} />
      <path d="M-148 -12 Q-152 -22 -138 -24 L60 -30 Q120 -30 146 -14 L140 -6 Q100 -6 60 -4 L-140 -4 Z" fill={fillOf(L.top, 't')} />
      <path d={fus} fill="none" stroke={INK} strokeWidth={4} />
      {L.band ? <rect x={-112} y={-26} width={14} height={30} fill={L.band} opacity={0.9} /> : null}
      {L.nose ? <path d="M112 -26 Q132 -24 146 -14 Q150 -4 146 6 Q130 12 112 12 Z" fill={L.nose} stroke={INK} strokeWidth={3} /> : null}
      {/* panel lines + exhausts */}
      <path d="M-40 -28 V10 M40 -30 V12 M100 -28 V10" stroke={INK} strokeOpacity={0.22} strokeWidth={2} />
      {[78, 90, 102].map((x) => <rect key={x} x={x} y={-16} width={8} height={5} rx={2} fill="#2b2926" />)}
      <Canopy d={ger ? 'M-6 -28 L4 -46 H44 L58 -30 Z' : 'M-14 -28 Q4 -54 34 -50 Q52 -46 60 -30 Z'} frames={ger ? 'M14 -46 V-29 M30 -46 V-29' : 'M18 -50 L14 -29 M40 -48 L42 -30'} />
      <path d="M2 -40 Q12 -48 24 -48" stroke="#fff" strokeOpacity={0.7} strokeWidth={3} fill="none" strokeLinecap="round" />
      {/* near wing (seen from slightly below) */}
      <path d={uk ? 'M-40 2 Q20 -2 70 4 Q76 12 58 20 Q0 54 -64 50 Q-82 46 -70 34 Z' : 'M-36 2 L74 4 Q80 12 62 18 L-48 50 Q-70 54 -66 40 Z'} fill={fillOf(L.top, 't')} stroke={INK} strokeWidth={3.5} strokeLinejoin="round" />
      <path d={uk ? 'M-30 6 Q20 4 64 8' : 'M-30 6 L66 8'} stroke="#fff" strokeOpacity={0.25} strokeWidth={4} fill="none" />
      <Mark nationKey={nationKey} x={-62} y={-10} s={0.95} />
      <Mark nationKey={nationKey} x={-6} y={32} s={0.75} />
      <Prop x={152} y={-4} r={40} t={t} c={L.spinner} />
    </g>
  );
};

const Stuka: React.FC<MP> = ({ nationKey, color, t }) => {
  const L = airLook(nationKey ?? 'GER', color);
  return (
    <g>
      <defs><VGrad c={L.top} k="t" lift={0.25} drop={-0.15} /></defs>
      <path d="M-136 -20 L-150 -66 L-118 -66 L-104 -26 Z" fill={fillOf(L.top, 't')} stroke={INK} strokeWidth={3.5} strokeLinejoin="round" />
      <path d="M-150 -4 L-108 -6 L-122 10 L-152 8 Z" fill={shade(L.top, -0.12)} stroke={INK} strokeWidth={3} />
      <path d="M-148 -10 Q-150 -22 -132 -24 L70 -30 Q120 -28 144 -14 Q148 -2 142 8 Q110 16 60 16 L-130 6 Q-150 4 -148 -10 Z" fill={fillOf(L.top, 't')} stroke={INK} strokeWidth={4} />
      <path d="M-140 0 L130 4 Q120 14 60 16 L-130 6 Z" fill={L.belly} opacity={0.9} />
      <Canopy d="M-50 -26 L-40 -48 H50 L64 -30 Z" frames="M-20 -48 V-27 M8 -48 V-28 M34 -48 V-29" />
      {/* inverted gull wing */}
      <path d="M-30 6 L20 30 L80 22 L86 30 L22 44 L-44 14 Z" fill={fillOf(L.top, 't')} stroke={INK} strokeWidth={3.5} strokeLinejoin="round" />
      {/* fixed spatted undercarriage */}
      <path d="M40 14 L52 64" stroke="#3b3b35" strokeWidth={8} />
      <path d="M38 50 Q52 42 66 52 L62 78 Q50 84 40 76 Z" fill={fillOf(L.top, 't')} stroke={INK} strokeWidth={3.5} />
      <path d="M100 -26 Q130 -22 144 -14 Q148 -2 142 8 Q124 14 100 14 Z" fill={L.nose ?? L.top} stroke={INK} strokeWidth={3} />
      <Mark nationKey={nationKey ?? 'GER'} x={-70} y={-8} s={0.9} />
      <Prop x={150} y={-3} r={42} t={t} c={L.spinner} />
    </g>
  );
};

const Bomber: React.FC<MP> = ({ nationKey, color, t }) => {
  const L = airLook(nationKey, color);
  const uk = nationKey === 'UK';
  const top = uk ? '#4f5a3c' : nationKey === 'USA' ? '#6a7050' : L.top;
  const belly = uk ? '#232220' : L.belly;
  const ger = nationKey === 'GER' || nationKey === 'GERI';
  return (
    <g>
      <defs><VGrad c={top} k="t" lift={0.25} drop={-0.15} /></defs>
      {/* far wing + far engines */}
      <path d="M-20 -24 L120 -30 L136 -44 L-4 -40 Z" fill={shade(top, -0.3)} stroke={INK} strokeWidth={3} strokeLinejoin="round" />
      {/* tall fin(s) */}
      {uk ? (
        <g>
          <path d="M-232 -24 Q-250 -92 -226 -96 Q-208 -96 -204 -30 Z" fill={fillOf(top, 't')} stroke={INK} strokeWidth={4} />
        </g>
      ) : (
        <path d={ger ? 'M-224 -26 L-246 -84 L-214 -86 L-196 -30 Z' : 'M-226 -26 Q-240 -110 -206 -110 Q-170 -60 -130 -34 Z'} fill={fillOf(top, 't')} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      )}
      <path d="M-246 -6 L-180 -8 L-196 14 L-250 10 Z" fill={shade(top, -0.12)} stroke={INK} strokeWidth={3} />
      {/* fuselage */}
      <path d="M-248 -14 Q-252 -28 -232 -30 L170 -40 Q234 -38 256 -16 Q260 0 250 10 Q220 22 160 22 L-226 8 Q-250 6 -248 -14 Z" fill={belly} stroke={INK} strokeWidth={4.5} />
      <path d="M-246 -14 Q-252 -28 -232 -30 L170 -40 Q234 -38 256 -16 L250 -6 Q190 -8 160 -8 L-236 -6 Z" fill={fillOf(top, 't')} />
      <path d="M-248 -14 Q-252 -28 -232 -30 L170 -40 Q234 -38 256 -16 Q260 0 250 10 Q220 22 160 22 L-226 8 Q-250 6 -248 -14 Z" fill="none" stroke={INK} strokeWidth={4.5} />
      {/* glazed nose / cockpit / turrets */}
      <path d={ger ? 'M200 -38 Q250 -36 258 -14 Q260 4 250 12 Q230 18 206 18 Z' : 'M226 -34 Q252 -26 256 -14 Q258 0 250 8 L228 10 Z'} fill={GLASS} stroke={INK} strokeWidth={3} />
      <path d={ger ? 'M220 -36 V16 M238 -30 V14' : 'M240 -28 V8'} stroke={INK} strokeWidth={2} opacity={0.6} />
      {!ger ? <Canopy d="M150 -40 Q164 -58 196 -56 Q212 -52 218 -40 Z" frames="M172 -56 V-40 M194 -55 V-40" /> : null}
      <path d="M40 -40 Q50 -62 74 -60 Q90 -58 94 -40 Z" fill={GLASS} stroke={INK} strokeWidth={3} />
      <path d="M60 -56 L92 -66" stroke="#2b2926" strokeWidth={5} strokeLinecap="round" />
      <rect x={-120} y={-30} width={24} height={16} rx={4} fill={GLASS} stroke={INK} strokeWidth={2.5} />
      <path d="M-120 -38 V16 M0 -40 V20 M120 -40 V22" stroke={INK} strokeOpacity={0.2} strokeWidth={2} />
      {/* near wing + two near engines */}
      <path d="M-40 6 L150 10 Q160 18 140 26 L-40 74 Q-68 80 -62 62 Z" fill={fillOf(top, 't')} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      {[[110, 16], [20, 42]].map(([x, y], i) => (
        <g key={i}>
          <path d={`M${x - 40} ${y - 4} H${x + 22} Q${x + 34} ${y + 4} ${x + 22} ${y + 12} H${x - 40} Z`} fill={fillOf(top, 't')} stroke={INK} strokeWidth={3.5} />
          <Prop x={x + 34} y={y + 4} r={30} t={t + i * 0.13} c={L.spinner} />
        </g>
      ))}
      <Mark nationKey={nationKey} x={-150} y={-14} s={1.1} />
      <Mark nationKey={nationKey} x={30} y={58} s={0.8} />
    </g>
  );
};

const Dakota: React.FC<MP> = ({ nationKey, color, t }) => {
  const skin = color ?? (nationKey === 'UK' ? '#6b7258' : '#6f7552');
  const belly = shade(skin, 0.25);
  const fus = 'M-300 -18 Q-310 -40 -270 -44 L180 -50 Q260 -46 300 -20 Q296 6 200 12 L-250 6 Q-296 4 -300 -18 Z';
  return (
    <g>
      <defs><VGrad c={skin} k="t" lift={0.25} drop={-0.15} /></defs>
      <path d="M-20 -30 L130 -36 L146 -50 L-6 -46 Z" fill={shade(skin, -0.3)} stroke={INK} strokeWidth={3} />
      <path d="M-280 -40 Q-320 -122 -282 -124 L-262 -122 L-220 -44 Z" fill={fillOf(skin, 't')} stroke={INK} strokeWidth={4.5} strokeLinejoin="round" />
      <path d="M-300 -30 L-354 -24 L-346 -12 L-300 -10 Z" fill={shade(skin, -0.1)} stroke={INK} strokeWidth={3.5} />
      <path d={fus} fill={belly} stroke={INK} strokeWidth={5} />
      <path d="M-298 -18 Q-310 -40 -270 -44 L180 -50 Q260 -46 300 -20 L292 -12 Q240 -16 180 -14 L-290 -10 Z" fill={fillOf(skin, 't')} />
      <path d={fus} fill="none" stroke={INK} strokeWidth={5} />
      <Canopy d="M226 -42 Q250 -56 278 -34 L262 -30 Z" frames="M246 -46 L250 -32" />
      {[-180, -130, -80, -30, 20, 70, 120].map((x) => <rect key={x} x={x} y={-36} width={22} height={16} rx={5} fill={GLASS} stroke={INK} strokeWidth={2} />)}
      <rect x={-210} y={-40} width={42} height={42} rx={3} fill="none" stroke={INK} strokeWidth={3} opacity={0.7} />
      {/* invasion stripes on the rear fuselage */}
      {[0, 1, 2, 3, 4].map((i) => <rect key={i} x={-260 + i * 12} y={-42} width={12} height={46} fill={i % 2 ? INK : '#ece6d2'} opacity={0.85} />)}
      {/* near wing with engine nacelle */}
      <path d="M-70 -2 L110 2 Q122 10 100 18 L-90 70 Q-120 76 -112 56 Z" fill={fillOf(skin, 't')} stroke={INK} strokeWidth={4.5} strokeLinejoin="round" />
      {[0, 1, 2, 3, 4].map((i) => <path key={i} d={`M${-60 + i * 10} 0 L${-100 + i * 10} 62`} stroke={i % 2 ? INK : '#ece6d2'} strokeWidth={10} opacity={0.8} />)}
      <path d="M-10 4 H64 Q80 12 64 22 H-10 Z" fill={fillOf(skin, 't')} stroke={INK} strokeWidth={3.5} />
      <Prop x={80} y={13} r={38} t={t} c="#2b2926" />
      <Mark nationKey={nationKey} x={-110} y={-18} s={1.25} />
    </g>
  );
};

const Glider: React.FC<MP> = ({ nationKey, color, damaged }) => {
  const skin = color ?? '#6b7258';
  const fus = 'M-280 -10 Q-290 -36 -250 -40 L210 -46 Q270 -44 290 -22 Q280 4 200 10 L-240 8 Q-276 8 -280 -10 Z';
  return (
    <g>
      <defs><VGrad c={skin} k="t" lift={0.25} drop={-0.18} /></defs>
      <path d="M-262 -36 Q-302 -118 -270 -120 L-246 -118 L-210 -40 Z" fill={fillOf(skin, 't')} stroke={INK} strokeWidth={4.5} strokeLinejoin="round" />
      <path d={fus} fill={fillOf(skin, 't')} stroke={INK} strokeWidth={5} />
      {/* high wing on the roof + struts */}
      <path d="M-150 -42 Q-150 -60 -120 -60 L160 -66 Q182 -64 182 -54 L170 -48 L-140 -42 Z" fill={fillOf(skin, 't')} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      <path d="M-120 -58 L160 -63" stroke="#fff" strokeOpacity={0.3} strokeWidth={4} />
      <Canopy d="M220 -40 Q246 -60 276 -32 Z" frames="M246 -48 L250 -32" />
      {[-160, -100, -40, 20, 80, 140].map((x) => <circle key={x} cx={x} cy={-18} r={8} fill={GLASS} stroke={INK} strokeWidth={2} />)}
      {[0, 1, 2, 3, 4].map((i) => <rect key={i} x={-230 + i * 12} y={-40} width={12} height={46} fill={i % 2 ? INK : '#ece6d2'} opacity={0.85} />)}
      <path d="M-200 -40 L-200 8 M180 -46 L180 10" stroke={INK} strokeWidth={2} opacity={0.4} />
      <Mark nationKey={nationKey} x={-130} y={-18} s={1.1} />
      {damaged ? <path d="M200 10 L260 34 L220 30 Z" fill={skin} stroke={INK} strokeWidth={3} /> : null}
    </g>
  );
};

// ---------------------------------------------------------------- ships
const Smoke: React.FC<{ x: number; y: number; t: number; c?: string; n?: number }> = ({ x, y, t, c = '#5d5a55', n = 4 }) => (
  <g>
    {Array.from({ length: n }, (_, i) => {
      const k = (t * 0.35 + i / n) % 1;
      return <circle key={i} cx={x - k * 160} cy={y - k * 70} r={14 + k * 34} fill={c} opacity={0.45 * (1 - k)} />;
    })}
  </g>
);

const Wake: React.FC<{ bow: number; stern: number; t: number }> = ({ bow, stern, t }) => (
  <g>
    <path d={`M${bow - 30} 0 q${36 + Math.sin(t * 3) * 6} 4 ${64} 22`} stroke="#fff" strokeWidth={7} strokeLinecap="round" fill="none" opacity={0.8} />
    <path d={`M${bow - 50} 8 q46 2 90 22`} stroke="#fff" strokeWidth={4} strokeLinecap="round" fill="none" opacity={0.6} />
    <path d={`M${stern + 20} 6 Q${stern - 90} ${10 + Math.sin(t * 2) * 4} ${stern - 260} 4`} stroke="#fff" strokeWidth={9} strokeLinecap="round" fill="none" opacity={0.5} />
    <path d={`M${stern + 10} 14 Q${stern - 120} ${20 + Math.sin(t * 2.4) * 3} ${stern - 320} 16`} stroke="#fff" strokeWidth={5} strokeLinecap="round" fill="none" opacity={0.35} />
  </g>
);

const Turret: React.FC<{ x: number; y: number; dir: number; guns: number; s?: number; c: string }> = ({ x, y, dir, guns, s = 1, c }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    {Array.from({ length: guns }, (_, i) => (
      <path key={i} d={`M${dir * 20} ${-22 + i * 6} L${dir * 128} ${-30 + i * 6}`} stroke={INK} strokeWidth={9} strokeLinecap="round" />
    ))}
    {Array.from({ length: guns }, (_, i) => (
      <path key={'g' + i} d={`M${dir * 20} ${-22 + i * 6} L${dir * 126} ${-30 + i * 6}`} stroke={shade(c, -0.25)} strokeWidth={4.5} strokeLinecap="round" />
    ))}
    <path d={`M${-44} 0 L${-38} -30 Q0 -40 38 -30 L44 0 Z`} fill={fillOf(c)} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
  </g>
);

const Warship: React.FC<MP & { cls: 'battleship' | 'cruiser' | 'destroyer' }> = ({ nationKey, color, t, damaged, cls }) => {
  const hull = color ?? (nationKey === 'JPN' ? '#6e7276' : nationKey === 'GER' || nationKey === 'GERI' ? '#7f868c' : '#76808a');
  const deck = shade(hull, 0.12);
  const s = cls === 'battleship' ? 1 : cls === 'cruiser' ? 0.82 : 0.62;
  const guns = cls === 'destroyer' ? 2 : cls === 'cruiser' ? 3 : 3;
  return (
    <g transform={`scale(${s})`}>
      <defs><VGrad c={hull} /><VGrad c={deck} /></defs>
      <Wake bow={520} stern={-470} t={t} />
      {/* hull with sheer: bow rises, boot-topping at the waterline */}
      <path d="M-480 -46 Q0 -40 440 -56 L530 -78 L470 30 L-440 30 Q-474 20 -480 -46 Z" fill={fillOf(hull)} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
      <path d="M-466 14 L478 14 L470 30 L-440 30 Q-460 26 -466 14 Z" fill="#7a2f26" opacity={0.9} />
      <path d="M-476 -40 Q0 -34 440 -50" stroke="#fff" strokeOpacity={0.3} strokeWidth={4} fill="none" />
      {Array.from({ length: 18 }, (_, i) => <circle key={i} cx={-400 + i * 46} cy={-14} r={3.6} fill="#2b2926" opacity={0.8} />)}
      <path d="M470 -60 l14 12 l-6 14" stroke={INK} strokeWidth={4} fill="none" />
      {/* superstructure: stacked blocks, bridge windows, tripod mast */}
      <path d="M-210 -44 V-104 H130 V-44 Z" fill={fillOf(deck)} stroke={INK} strokeWidth={4} />
      <path d="M-150 -104 V-150 H70 V-104 Z" fill={fillOf(deck)} stroke={INK} strokeWidth={4} />
      <path d="M-20 -150 V-212 H60 L72 -190 V-150 Z" fill={fillOf(deck)} stroke={INK} strokeWidth={4} />
      {[0, 1, 2, 3].map((i) => <rect key={i} x={-12 + i * 18} y={-202} width={12} height={10} fill={GLASS} stroke={INK} strokeWidth={1.5} />)}
      {Array.from({ length: 8 }, (_, i) => <rect key={i} x={-196 + i * 40} y={-90} width={18} height={10} rx={2} fill="#3a3f45" />)}
      <path d="M20 -212 L20 -320 M-6 -212 L20 -300 M46 -212 L20 -300 M0 -286 H40 M6 -262 H34" stroke={INK} strokeWidth={5} fill="none" />
      <rect x={10} y={-334} width={20} height={14} fill="#3a3f45" stroke={INK} strokeWidth={2} />
      {/* funnels with smoke */}
      {(cls === 'destroyer' ? [-90] : [-110, -60]).map((x) => (
        <g key={x}>
          <Smoke x={x + 20} y={-200} t={t + x * 0.01} />
          <path d={`M${x} -104 L${x + 6} -196 H${x + 40} L${x + 44} -104 Z`} fill={fillOf(deck)} stroke={INK} strokeWidth={4} />
          <rect x={x + 4} y={-204} width={40} height={10} fill="#2b2926" stroke={INK} strokeWidth={2.5} />
        </g>
      ))}
      {/* main turrets fore and aft + secondaries */}
      <Turret x={250} y={-48} dir={1} guns={guns} c={deck} />
      <Turret x={340} y={-58} dir={1} guns={guns} s={0.9} c={deck} />
      <Turret x={-300} y={-44} dir={-1} guns={guns} c={deck} />
      {cls !== 'destroyer' ? <Turret x={-390} y={-46} dir={-1} guns={guns} s={0.9} c={deck} /> : null}
      {[-170, -120, 90].map((x) => <rect key={x} x={x} y={-118} width={26} height={14} rx={4} fill={deck} stroke={INK} strokeWidth={2.5} />)}
      {nationKey ? <g transform="translate(-440 -110)"><path d="M0 60 V0" stroke={INK} strokeWidth={3} /><rect x={0} y={0} width={40} height={26} fill={nation(nationKey).flag[0]} stroke={INK} strokeWidth={2} /></g> : null}
      {damaged ? <Smoke x={60} y={-80} t={t} c="#2b2926" n={5} /> : null}
    </g>
  );
};

const Cargo: React.FC<MP> = ({ color, t, damaged }) => {
  const hull = color ?? '#3d434a';
  const house = '#e7e0cf';
  return (
    <g>
      <defs><VGrad c={hull} /><VGrad c={house} lift={0.1} drop={-0.18} /></defs>
      <Wake bow={430} stern={-400} t={t} />
      <path d="M-420 -64 Q0 -56 400 -72 L440 -86 L392 30 L-394 30 Q-420 10 -420 -64 Z" fill={fillOf(hull)} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
      <path d="M-404 12 L410 12 L392 30 L-394 30 Z" fill="#8a3a2a" />
      <path d="M-416 -58 Q0 -50 400 -66" stroke="#fff" strokeOpacity={0.25} strokeWidth={4} fill="none" />
      {/* midship house + funnel */}
      <path d="M-40 -60 V-150 H110 V-60 Z" fill={fillOf(house)} stroke={INK} strokeWidth={4} />
      <path d="M-20 -150 V-184 H90 V-150 Z" fill={fillOf(house)} stroke={INK} strokeWidth={4} />
      {Array.from({ length: 5 }, (_, i) => <rect key={i} x={-28 + i * 26} y={-176} width={14} height={10} fill={GLASS} stroke={INK} strokeWidth={1.5} />)}
      {Array.from({ length: 6 }, (_, i) => <circle key={i} cx={-24 + i * 24} cy={-110} r={4} fill="#3a3f45" />)}
      <Smoke x={30} y={-236} t={t} />
      <path d="M14 -184 L18 -232 H50 L54 -184 Z" fill="#2b2926" stroke={INK} strokeWidth={4} />
      <rect x={17} y={-222} width={36} height={8} fill="#b8322a" />
      {/* masts with cargo booms + deck cargo */}
      {[-260, 240].map((x) => (
        <g key={x}>
          <path d={`M${x} -62 V-230 M${x} -200 L${x + (x < 0 ? 90 : -90)} -90`} stroke={INK} strokeWidth={5} />
          <path d={`M${x - 14} -200 H${x + 14}`} stroke={INK} strokeWidth={5} />
        </g>
      ))}
      {[-360, -300, -200, -140, 160, 220, 300].map((x, i) => (
        <rect key={x} x={x} y={-64 - 32 - (i % 2) * 8} width={50} height={32 + (i % 2) * 8} fill={['#7a6a48', '#5a6a4a', '#8a5a3a'][i % 3]} stroke={INK} strokeWidth={3} />
      ))}
      {damaged ? <Smoke x={-120} y={-100} t={t} c="#2b2926" n={5} /> : null}
    </g>
  );
};

const Submarine: React.FC<MP> = ({ color, t }) => {
  const hull = color ?? '#5d666e';
  return (
    <g>
      <defs><VGrad c={hull} /></defs>
      <Wake bow={380} stern={-340} t={t} />
      <path d="M-360 -4 Q-372 -28 -322 -32 L300 -36 Q372 -30 386 -6 Q370 20 300 22 L-320 20 Q-366 18 -360 -4 Z" fill={fillOf(hull)} stroke={INK} strokeWidth={5} />
      <path d="M-300 -32 H280" stroke="#fff" strokeOpacity={0.3} strokeWidth={4} />
      <path d="M-200 -10 Q0 4 240 -10" stroke={INK} strokeOpacity={0.3} strokeWidth={3} fill="none" />
      {/* conning tower with railing */}
      <path d="M-70 -34 L-56 -104 H66 L96 -70 L104 -36 Z" fill={fillOf(hull)} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      <path d="M-60 -100 H62" stroke="#fff" strokeOpacity={0.3} strokeWidth={4} />
      <path d="M-100 -36 V-62 H-62" stroke={INK} strokeWidth={3} fill="none" />
      <path d="M10 -104 V-160 M30 -104 V-140" stroke={INK} strokeWidth={5} />
      {/* deck gun + net cutter + hydroplane */}
      <path d="M140 -36 V-56 M126 -60 L210 -66" stroke={INK} strokeWidth={7} strokeLinecap="round" />
      <path d="M300 -36 L360 -64" stroke={INK} strokeWidth={4} />
      <path d="M350 6 l30 6 l-26 4 z" fill={hull} stroke={INK} strokeWidth={3} />
    </g>
  );
};

const Rowboat: React.FC<MP> = ({ color, t }) => {
  const wood = color ?? '#8a5a33';
  return (
    <g>
      <defs><VGrad c={wood} /></defs>
      <path d={`M-140 -10 q70 ${4 + Math.sin(t * 2) * 2} 140 0`} stroke="#fff" strokeWidth={4} opacity={0.5} fill="none" />
      <path d="M-124 -24 L132 -30 Q122 6 96 18 L-96 18 Q-118 8 -124 -24 Z" fill={fillOf(wood)} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      <path d="M-118 -10 Q0 -6 124 -16 M-108 4 Q0 8 112 -2" stroke={INK} strokeOpacity={0.3} strokeWidth={2.5} fill="none" />
      <path d="M0 -26 V-150 L78 -40 Z" fill="#efe6d2" stroke={INK} strokeWidth={3} strokeLinejoin="round" />
      <path d="M0 -26 V-150" stroke={INK} strokeWidth={4} />
    </g>
  );
};

export const MACHINE_TYPES = new Set(['truck', 'jeep', 'car', 'halftrack', 'artillery', 'gun', 'fighter', 'plane', 'divebomber', 'bomber', 'dakota', 'transport', 'glider', 'battleship', 'cruiser', 'destroyer', 'cargo', 'freighter', 'submarine', 'uboat', 'boat']);

export const Machine: React.FC<MP> = (p) => {
  switch (p.type) {
    case 'truck': return <Truck {...p} />;
    case 'jeep':
    case 'car': return <Jeep {...p} />;
    case 'halftrack': return <Halftrack {...p} />;
    case 'artillery':
    case 'gun': return <FieldGun {...p} />;
    case 'fighter':
    case 'plane': return <Fighter {...p} />;
    case 'divebomber': return p.nationKey === 'GER' || p.nationKey === 'GERI' || !p.nationKey ? <Stuka {...p} /> : <Fighter {...p} />;
    case 'bomber': return <Bomber {...p} />;
    case 'dakota':
    case 'transport': return <Dakota {...p} />;
    case 'glider': return <Glider {...p} />;
    case 'battleship':
    case 'cruiser':
    case 'destroyer': return <Warship {...p} cls={p.type as 'battleship' | 'cruiser' | 'destroyer'} />;
    case 'cargo':
    case 'freighter': return <Cargo {...p} />;
    case 'submarine':
    case 'uboat': return <Submarine {...p} />;
    case 'boat': return <Rowboat {...p} />;
    default: return null;
  }
};
