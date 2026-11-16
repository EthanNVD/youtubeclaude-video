import React from 'react';
import { C, INK, FONT } from '../theme';
import { rnd } from '../lib/anim';
import { Vehicle } from '../props/Vehicles';
import { Flag } from '../props/Props';
import { Tree } from './Sets';

/**
 * Detailed "lived-in" locations + a lighting pass and foreground layer used by every set.
 * Canvas: x -240..2160, y -160..1240, actors stand on y = ground (default 900).
 * Everything idles: water rolls, lamps sway, dust floats in light, smoke drifts, flags and windsocks wave.
 */
const X0 = -240, Y0 = -160, W = 2400, H = 1400;
type P = { kind: string; t: number; time?: string; [k: string]: unknown };

export const RICH_SETS = new Set(['workshop', 'board', 'archbridge', 'river', 'polder', 'cabin', 'heath', 'hotel', 'garden', 'bridge', 'deck', 'flightdeck', 'hangar', 'radio', 'tent', 'airfield', 'corridor', 'parliament', 'cell', 'train_interior', 'cockpit']);

const SKY: Record<string, [string, string]> = {
  day: ['#6fb3dc', '#d7ecf4'],
  dusk: ['#4d4f86', '#f3a76a'],
  dawn: ['#7a8fc0', '#f6c99a'],
  night: ['#0d1830', '#2a3b60'],
  storm: ['#58626d', '#9aa4ab'],
};
const SkyG: React.FC<{ id: string; time?: string; y1?: number; y2?: number }> = ({ id, time = 'day', y1 = Y0, y2 = 700 }) => {
  const [a, b] = SKY[time] ?? SKY.day;
  return (
    <g>
      <defs>
        <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={a} />
          <stop offset="1" stopColor={b} />
        </linearGradient>
      </defs>
      <rect x={X0} y={y1} width={W} height={y2 - y1} fill={`url(#${id})`} />
    </g>
  );
};
const Puff: React.FC<{ x: number; y: number; s: number; c?: string }> = ({ x, y, s, c = '#fdfdfb' }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M-120 30 Q-130 -10 -90 -14 Q-80 -60 -30 -50 Q-10 -90 40 -66 Q90 -80 100 -30 Q140 -24 130 30 Z" fill={c} />
    <path d="M-120 30 Q0 44 130 30 Q0 18 -120 30 Z" fill="#dfe6ea" opacity={0.8} />
  </g>
);
const Drift: React.FC<{ t: number; n: number; y: number; h: number; seed: string; c?: string; sp?: number }> = ({ t, n, y, h, seed, c, sp = 8 }) => (
  <g>
    {Array.from({ length: n }, (_, i) => {
      const x = ((X0 + rnd(seed, i) * W + t * (sp + rnd(seed, i, 'v') * sp)) % W + W) % W + X0;
      return <Puff key={i} x={x} y={y + rnd(seed, i, 'y') * h} s={0.45 + rnd(seed, i, 's') * 0.8} c={c} />;
    })}
  </g>
);
const Waves: React.FC<{ y: number; y2: number; t: number; n?: number; seed?: string; op?: number }> = ({ y, y2, t, n = 40, seed = 'w', op = 0.3 }) => (
  <g>
    {Array.from({ length: n }, (_, i) => {
      const k = rnd(seed, i);
      const yy = y + 6 + k * k * (y2 - y - 6);
      const kk = (yy - y) / (y2 - y);
      const x = ((X0 + rnd(seed, i, 'x') * W + t * (8 + kk * 26)) % W + W) % W + X0;
      const len = 18 + kk * 90;
      return <path key={i} d={`M${x} ${yy} q${len / 2} ${-4 - kk * 6} ${len} 0`} stroke="#fff" strokeOpacity={op * (0.6 + 0.4 * Math.sin(t * 2 + i))} strokeWidth={1.5 + kk * 3} fill="none" strokeLinecap="round" />;
    })}
  </g>
);
const Bricks: React.FC<{ x: number; y: number; w: number; h: number; c: string; seed: string }> = ({ x, y, w, h, c, seed }) => {
  const rows = Math.floor(h / 26);
  return (
    <g>
      <rect x={x} y={y} width={w} height={h} fill={c} />
      {Array.from({ length: rows }, (_, r) => (
        <g key={r}>
          <line x1={x} x2={x + w} y1={y + r * 26} y2={y + r * 26} stroke="#000" strokeOpacity={0.16} strokeWidth={2} />
          {Array.from({ length: Math.ceil(w / 64) + 1 }, (_, i) => {
            const bx = x + i * 64 + (r % 2) * 32;
            return bx < x + w ? (
              <g key={i}>
                <line x1={bx} x2={bx} y1={y + r * 26} y2={y + r * 26 + 26} stroke="#000" strokeOpacity={0.14} strokeWidth={2} />
                {rnd(seed, r, i) > 0.82 ? <rect x={bx + 4} y={y + r * 26 + 4} width={54} height={18} fill="#000" opacity={0.07} /> : null}
              </g>
            ) : null;
          })}
        </g>
      ))}
    </g>
  );
};
const Dust: React.FC<{ t: number; x: number; y: number; w: number; h: number; n?: number; seed?: string; c?: string }> = ({ t, x, y, w, h, n = 26, seed = 'd', c = '#fff8dc' }) => (
  <g>
    {Array.from({ length: n }, (_, i) => {
      const px = x + ((rnd(seed, i) * w + Math.sin(t * 0.4 + i) * 30 + t * 6) % w + w) % w;
      const py = y + ((rnd(seed, i, 'y') * h - t * (4 + rnd(seed, i, 'v') * 8)) % h + h) % h;
      return <circle key={i} cx={px} cy={py} r={1.5 + rnd(seed, i, 'r') * 2.5} fill={c} opacity={0.25 + 0.35 * Math.abs(Math.sin(t * 0.8 + i))} />;
    })}
  </g>
);
const Lantern: React.FC<{ x: number; y: number; t: number; len?: number; swing?: number }> = ({ x, y, t, len = 220, swing = 3 }) => {
  const a = Math.sin(t * 1.3) * swing;
  return (
    <g transform={`translate(${x} ${y}) rotate(${a})`}>
      <line x1={0} y1={0} x2={0} y2={len} stroke={INK} strokeWidth={3} />
      <path d={`M-40 ${len + 40} L-22 ${len} L22 ${len} L40 ${len + 40} Z`} fill="#3d4a3f" stroke={INK} strokeWidth={4} />
      <ellipse cx={0} cy={len + 42} rx={18} ry={7} fill="#fff1a8" />
      <path d={`M-40 ${len + 40} L-330 ${len + 760} L330 ${len + 760} L40 ${len + 40} Z`} fill="#fff3c0" opacity={0.11} />
    </g>
  );
};
const Rivets: React.FC<{ x: number; y: number; w: number; n: number }> = ({ x, y, w, n }) => (
  <g>{Array.from({ length: n }, (_, i) => <circle key={i} cx={x + (i * w) / (n - 1)} cy={y} r={3} fill="#000" opacity={0.22} />)}</g>
);
/** Parked aircraft standing on its gear; (x, y) = ground under the wheels. */
const Plane: React.FC<{ x: number; y: number; s: number; t: number; nation?: string; type?: string; flip?: boolean; spin?: boolean }> = ({ x, y, s, t, nation, type = 'divebomber', flip, spin }) => (
  <g transform={`translate(${x} ${y}) scale(${flip ? -s : s} ${s})`}>
    <ellipse cx={0} cy={0} rx={150} ry={12} fill="#000" opacity={0.18} />
    <path d="M40 -60 L30 -16 M-10 -60 L-14 -16" stroke={INK} strokeWidth={7} />
    <circle cx={30} cy={-14} r={14} fill="#2a2a2a" stroke={INK} strokeWidth={3} />
    <circle cx={-14} cy={-14} r={14} fill="#2a2a2a" stroke={INK} strokeWidth={3} />
    <path d="M-120 -78 L-128 -40" stroke={INK} strokeWidth={5} />
    <circle cx={-128} cy={-36} r={7} fill="#2a2a2a" />
    <g transform={`translate(0 -78) rotate(-6)`}>
      <Vehicle type={type} nationKey={nation} t={spin ? t : 0} />
    </g>
  </g>
);
const DeckCrew: React.FC<{ x: number; y: number; s: number; t: number; c: string; i: number }> = ({ x, y, s, t, c, i }) => {
  const step = Math.sin(t * 6 + i) * 4;
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <path d={`M-6 0 L-4 -26 M6 0 L4 -26`} stroke={INK} strokeWidth={6} strokeLinecap="round" transform={`rotate(${step} 0 -26)`} />
      <rect x={-11} y={-56} width={22} height={32} rx={8} fill={c} stroke={INK} strokeWidth={3} />
      <circle cx={0} cy={-68} r={13} fill="#f6dcc4" stroke={INK} strokeWidth={3} />
      <path d="M-13 -72 Q0 -86 13 -72 Z" fill={c} stroke={INK} strokeWidth={2.5} />
    </g>
  );
};

const Garden: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  return (
    <g>
      <SkyG id="sky_g" time={p.time} y2={g} />
      <Drift t={t} n={6} y={-60} h={220} seed="gc" />
      {/* trees beyond the wall */}
      {[[980, 0.9], [1230, 1.1], [1520, 0.85], [1840, 1.05], [2060, 0.9]].map(([x, s], i) => (
        <g key={i} transform={`translate(${x} ${g - 290}) scale(${s}) rotate(${Math.sin(t * 0.7 + i) * 1.2})`}>
          <rect x={-9} y={-40} width={18} height={60} fill="#6b4a32" />
          <circle cx={0} cy={-110} r={70} fill="#5d8f45" stroke={INK} strokeWidth={3} />
          <circle cx={-46} cy={-70} r={44} fill="#5d8f45" stroke={INK} strokeWidth={3} />
          <circle cx={44} cy={-76} r={48} fill="#5d8f45" stroke={INK} strokeWidth={3} />
          <circle cx={-14} cy={-130} r={30} fill="#78ab5a" />
        </g>
      ))}
      {/* house facade on the left */}
      <Bricks x={X0} y={-160} w={820} h={g - 120 + 160} c="#a9553e" seed="hb" />
      <rect x={X0} y={-160} width={820} height={g - 120 + 160} fill="none" stroke={INK} strokeWidth={4} />
      {[[-150, 60], [130, 60], [-150, 420], [380, 60]].map(([x, y], i) => (
        <g key={i}>
          <rect x={x} y={y} width={170} height={250} fill="#f2ecdf" stroke={INK} strokeWidth={4} />
          <rect x={x + 12} y={y + 12} width={146} height={226} fill="#9cc6dc" />
          <path d={`M${x + 85} ${y + 12} V${y + 238} M${x + 12} ${y + 90} H${x + 158} M${x + 12} ${y + 165} H${x + 158}`} stroke="#f2ecdf" strokeWidth={7} />
          <path d={`M${x + 20} ${y + 30} l40 0 l-30 60`} stroke="#fff" strokeOpacity={0.4} strokeWidth={6} fill="none" />
          <rect x={x - 10} y={y + 250} width={190} height={16} fill="#e9e1cf" stroke={INK} strokeWidth={3} />
        </g>
      ))}
      {/* front door */}
      <g transform={`translate(330 ${g - 120})`}>
        <rect x={-90} y={-420} width={180} height={420} fill="#efe7d6" stroke={INK} strokeWidth={4} />
        <rect x={-66} y={-396} width={132} height={396} fill="#24473a" stroke={INK} strokeWidth={4} />
        <rect x={-48} y={-370} width={96} height={150} fill="none" stroke="#000" strokeOpacity={0.25} strokeWidth={4} />
        <rect x={-48} y={-190} width={96} height={150} fill="none" stroke="#000" strokeOpacity={0.25} strokeWidth={4} />
        <circle cx={0} cy={-230} r={9} fill="#d9b44a" stroke={INK} strokeWidth={2} />
        <rect x={-110} y={-6} width={220} height={22} fill="#cfc6b4" stroke={INK} strokeWidth={3} />
      </g>
      {/* garden wall with ivy and hedge */}
      <Bricks x={580} y={g - 330} w={1580} h={210} c="#b4644a" seed="gw" />
      <rect x={580} y={g - 342} width={1580} height={18} fill="#cfc0a8" stroke={INK} strokeWidth={3} />
      {Array.from({ length: 9 }, (_, i) => (
        <path key={i} d={`M${640 + i * 170} ${g - 324} q${20 + rnd('iv', i) * 30} 60 ${-10} ${110 + rnd('iv2', i) * 60}`} stroke="#3f6b3a" strokeWidth={14} fill="none" strokeLinecap="round" opacity={0.85} />
      ))}
      {Array.from({ length: 12 }, (_, i) => {
        const x = 600 + i * 140;
        return (
          <g key={i}>
            <ellipse cx={x} cy={g - 150} rx={92} ry={70} fill="#4c7d3e" stroke={INK} strokeWidth={3} />
            <ellipse cx={x - 20} cy={g - 176} rx={40} ry={24} fill="#6a9a50" />
            {Array.from({ length: 5 }, (_, j) => (
              <circle key={j} cx={x - 60 + rnd('fl', i, j) * 120} cy={g - 190 + rnd('fy', i, j) * 70} r={7} fill={j % 2 ? '#d8423a' : '#e85a50'} stroke={INK} strokeWidth={1.5} />
            ))}
          </g>
        );
      })}
      {/* lawn + gravel path */}
      <rect x={X0} y={g - 120} width={W} height={H} fill="#8fbe5a" />
      {Array.from({ length: 80 }, (_, i) => <path key={i} d={`M${X0 + rnd('gr', i) * W} ${g - 110 + rnd('gy', i) * 60} l4 -12 l4 12`} stroke="#6f9a44" strokeWidth={3} fill="none" />)}
      <path d={`M${X0} ${g - 50} H${X0 + W} V${g + 60} H${X0} Z`} fill="#d8c8a2" />
      <path d={`M${X0} ${g - 50} H${X0 + W}`} stroke="#000" strokeOpacity={0.12} strokeWidth={6} />
      {Array.from({ length: 40 }, (_, i) => <ellipse key={i} cx={X0 + rnd('pb', i) * W} cy={g - 30 + rnd('pby', i) * 80} rx={6 + rnd('pbr', i) * 6} ry={4} fill="#9a9590" stroke={INK} strokeWidth={1.5} />)}
      <rect x={X0} y={g + 60} width={W} height={H} fill="#7fae4c" />
      {/* bench + pot */}
      <g transform={`translate(1520 ${g - 70})`}>
        <rect x={-110} y={-70} width={220} height={18} fill="#8a5a33" stroke={INK} strokeWidth={3} />
        <rect x={-110} y={-40} width={220} height={16} fill="#8a5a33" stroke={INK} strokeWidth={3} />
        <rect x={-100} y={-24} width={14} height={50} fill="#5a3a22" stroke={INK} strokeWidth={2} />
        <rect x={86} y={-24} width={14} height={50} fill="#5a3a22" stroke={INK} strokeWidth={2} />
      </g>
      <g transform={`translate(560 ${g - 60})`}>
        <path d="M-40 -60 L40 -60 L30 0 L-30 0 Z" fill="#b8724a" stroke={INK} strokeWidth={3} />
        <ellipse cx={0} cy={-80} rx={46} ry={30} fill="#4f8a3a" stroke={INK} strokeWidth={3} />
      </g>
      {/* a bird crossing now and then */}
      {(() => {
        const k = (t * 0.12) % 1;
        return <path d={`M${X0 + k * W} ${120 + Math.sin(t) * 20} q10 -10 20 0 q10 -10 20 0`} stroke={INK} strokeWidth={3} fill="none" />;
      })()}
    </g>
  );
};

const Bridge: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const roll = Math.sin(t * 0.55) * 2.2;
  const steel = (p.wall as string) ?? '#6f7b74';
  return (
    <g>
      {/* outside: sea + sky rolling behind the windows */}
      <g transform={`rotate(${roll} 960 420)`}>
        <SkyG id="sky_b" time={p.time} y1={-400} y2={460} />
        <Drift t={t} n={5} y={0} h={200} seed="bc" c={p.time === 'night' ? '#3a4a6a' : undefined} />
        <rect x={-600} y={440} width={3200} height={500} fill={p.time === 'night' ? '#14263d' : '#3f78a3'} />
        <Waves y={440} y2={700} t={t} seed="bw" />
        {p.convoy ? [300, 900, 1500].map((x, i) => <g key={i} transform={`translate(${x + ((t * 6) % 200)} 452) scale(0.16)`}><Vehicle type={i === 1 ? 'carrier' : 'destroyer'} nationKey={p.nation as string} t={t} /></g>) : null}
      </g>
      {/* wall with window band */}
      <path d={`M${X0} ${Y0} H${X0 + W} V${g - 120} H${X0} Z M${X0 + 100} 140 V520 H${X0 + W - 100} V140 Z`} fill={steel} fillRule="evenodd" />
      {Array.from({ length: 6 }, (_, i) => <rect key={i} x={X0 + 100 + i * 366} y={130} width={36} height={400} fill={steel} stroke={INK} strokeWidth={4} />)}
      <rect x={X0 + 100} y={130} width={W - 200} height={400} fill="none" stroke={INK} strokeWidth={5} />
      <rect x={X0} y={520} width={W} height={26} fill="#5a655f" stroke={INK} strokeWidth={4} />
      <Rivets x={X0 + 40} y={90} w={W - 80} n={40} />
      <Rivets x={X0 + 40} y={600} w={W - 80} n={40} />
      {/* overhead pipes */}
      <path d={`M${X0} 30 H${X0 + W} M${X0} 62 H${X0 + W}`} stroke="#8a948e" strokeWidth={20} />
      <path d={`M${X0} 30 H${X0 + W} M${X0} 62 H${X0 + W}`} stroke={INK} strokeWidth={24} strokeOpacity={0.25} fill="none" />
      {/* instruments */}
      <g transform={`translate(1480 ${g - 120})`}>
        <rect x={-50} y={-250} width={100} height={250} fill="#4c5651" stroke={INK} strokeWidth={4} />
        <circle cx={0} cy={-300} r={64} fill="#c9a24a" stroke={INK} strokeWidth={5} />
        <circle cx={0} cy={-300} r={50} fill="#f4ecd8" stroke={INK} strokeWidth={3} />
        <path d="M-40 -300 H40 M0 -340 V-260" stroke={INK} strokeWidth={2} opacity={0.4} />
        <line x1={0} y1={-300} x2={Math.cos(t * 0.3) * 40} y2={-300 - Math.sin(t * 0.3) * 40} stroke={C.red} strokeWidth={5} strokeLinecap="round" />
        <text x={0} y={-180} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={22} fill="#e9dfc7">TELEGRAPH</text>
      </g>
      {/* ship's wheel */}
      <g transform={`translate(560 ${g - 300}) rotate(${Math.sin(t * 0.5) * 8})`}>
        {Array.from({ length: 8 }, (_, i) => <line key={i} x1={0} y1={0} x2={Math.cos((i * Math.PI) / 4) * 130} y2={Math.sin((i * Math.PI) / 4) * 130} stroke="#7a4a28" strokeWidth={14} strokeLinecap="round" />)}
        <circle r={100} fill="none" stroke="#8a5a33" strokeWidth={20} />
        <circle r={100} fill="none" stroke={INK} strokeWidth={26} strokeOpacity={0.3} />
        <circle r={22} fill="#c9a24a" stroke={INK} strokeWidth={4} />
      </g>
      <rect x={520} y={g - 300} width={80} height={180} fill="#4c5651" stroke={INK} strokeWidth={4} />
      {/* voice pipes */}
      {[860, 920].map((x, i) => <path key={i} d={`M${x} ${g - 120} V${g - 330} q0 -30 30 -30`} stroke="#b88a3a" strokeWidth={18} fill="none" />)}
      <rect x={X0} y={g - 120} width={W} height={H} fill="#55605a" />
      {Array.from({ length: 14 }, (_, i) => <line key={i} x1={X0 + i * 190} y1={g - 120} x2={X0 + i * 190 - 160} y2={Y0 + H} stroke="#000" strokeOpacity={0.15} strokeWidth={4} />)}
      <rect x={X0} y={g - 128} width={W} height={10} fill="#000" opacity={0.2} />
      {p.nation ? <g transform={`translate(1880 160)`}><Flag nation={p.nation as string} w={150} h={100} t={t} /></g> : null}
    </g>
  );
};

const FlightDeck: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const nat = (p.nation as string) ?? 'USA';
  const hz = 560;
  const planes = (p.planes as number) ?? 4;
  return (
    <g>
      <SkyG id="sky_d" time={p.time} y2={hz + 10} />
      <Drift t={t} n={6} y={-40} h={260} seed="dc" />
      <rect x={X0} y={hz} width={W} height={260} fill={p.time === 'night' ? '#14263d' : '#3f78a3'} />
      <Waves y={hz} y2={hz + 220} t={t} seed="dw" n={30} />
      {p.escort !== false ? <g transform={`translate(${200 + ((t * 4) % 300)} ${hz + 12}) scale(0.14)`}><Vehicle type="destroyer" nationKey={nat} t={t} /></g> : null}
      {/* flight deck in perspective */}
      <path d={`M${X0} ${g - 140} L${X0 + W} ${g - 140} L${X0 + W} ${Y0 + H} L${X0} ${Y0 + H} Z`} fill="#9a7b52" />
      <path d={`M${X0} ${g - 140} H${X0 + W}`} stroke={INK} strokeWidth={6} />
      {Array.from({ length: 40 }, (_, i) => <line key={i} x1={X0 + i * 60} y1={g - 140} x2={960 + (X0 + i * 60 - 960) * 2.6} y2={Y0 + H} stroke="#000" strokeOpacity={0.12} strokeWidth={3} />)}
      {[g - 100, g - 40, g + 40, g + 140].map((y, i) => <line key={i} x1={X0} y1={y} x2={X0 + W} y2={y} stroke="#000" strokeOpacity={0.1} strokeWidth={3} />)}
      <path d={`M${X0} ${g + 10} H${X0 + W}`} stroke="#f2efe6" strokeWidth={10} strokeDasharray="70 50" opacity={0.85} />
      {nat === 'JPN' ? <ellipse cx={1100} cy={g + 160} rx={260} ry={70} fill="#bc002d" opacity={0.9} /> : null}
      {/* island superstructure */}
      <g transform={`translate(1720 ${g - 140})`}>
        <path d="M-160 0 V-300 H140 V0 Z" fill="#7a828c" stroke={INK} strokeWidth={5} />
        <rect x={-150} y={-280} width={280} height={44} fill="#55606a" stroke={INK} strokeWidth={3} />
        {Array.from({ length: 6 }, (_, i) => <rect key={i} x={-140 + i * 46} y={-272} width={34} height={26} fill="#9fd0e8" stroke={INK} strokeWidth={2} />)}
        <path d="M-60 -300 V-520 M-110 -470 H-10 M-90 -420 H-30" stroke={INK} strokeWidth={8} />
        <rect x={30} y={-420} width={90} height={120} fill="#5a636c" stroke={INK} strokeWidth={4} />
        {Array.from({ length: 4 }, (_, i) => {
          const k = ((t * 0.5 + i / 4) % 1);
          return <circle key={i} cx={75 + k * 80} cy={-430 - k * 220} r={26 + k * 50} fill="#4a4846" opacity={0.45 * (1 - k)} />;
        })}
        <g transform="translate(-60 -520)"><Flag nation={nat} w={90} h={60} t={t} /></g>
        <rect x={-110} y={-200} width={70} height={110} rx={6} fill="#4c565f" stroke={INK} strokeWidth={3} />
      </g>
      {/* parked aircraft + crew */}
      {Array.from({ length: planes }, (_, i) => <Plane key={i} x={-80 + i * 430} y={g - 128} s={0.95} t={t} nation={nat} type={i % 2 ? 'fighter' : 'divebomber'} spin={i === 0} />)}
      {Array.from({ length: 5 }, (_, i) => (
        <DeckCrew key={i} x={60 + i * 380 + Math.sin(t * 0.8 + i) * 40} y={g - 112} s={1.5} t={t} c={['#e8c43a', '#c8352b', '#3a6ea5', '#f2efe6', '#5a9a4a'][i]} i={i} />
      ))}
    </g>
  );
};

const Hangar: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const nat = (p.nation as string) ?? 'JPN';
  return (
    <g>
      <rect x={X0} y={Y0} width={W} height={H} fill="#4a524f" />
      {/* open side: daylight + sea */}
      <rect x={1500} y={120} width={700} height={g - 260} fill="#a8d0e6" />
      <rect x={1500} y={g - 360} width={700} height={220} fill="#3f78a3" />
      <Waves y={g - 360} y2={g - 140} t={t} seed="hw" n={14} />
      <rect x={1500} y={120} width={700} height={g - 260} fill="none" stroke={INK} strokeWidth={6} />
      <path d={`M1500 120 L1180 ${g - 120} H1500 Z`} fill="#fff6d8" opacity={0.1} />
      {/* beams */}
      {Array.from({ length: 9 }, (_, i) => (
        <g key={i}>
          <rect x={X0 + i * 300} y={Y0} width={40} height={g - 120 - Y0} fill="#3c4441" stroke={INK} strokeWidth={3} />
          <Rivets x={X0 + i * 300 + 20} y={100} w={1} n={2} />
        </g>
      ))}
      <rect x={X0} y={40} width={W} height={50} fill="#3c4441" stroke={INK} strokeWidth={3} />
      {[300, 960, 1600].map((x, i) => <Lantern key={i} x={x} y={90} t={t + i} len={60} swing={1.5} />)}
      <Dust t={t} x={600} y={200} w={720} h={600} seed="hd" />
      {/* floor */}
      <rect x={X0} y={g - 120} width={W} height={H} fill="#5f6763" />
      {Array.from({ length: 14 }, (_, i) => <line key={i} x1={X0 + i * 190} y1={g - 120} x2={X0 + i * 190 - 200} y2={Y0 + H} stroke="#000" strokeOpacity={0.15} strokeWidth={4} />)}
      <path d={`M${X0} ${g + 60} H${X0 + W}`} stroke="#e3c84a" strokeWidth={8} strokeDasharray="60 40" opacity={0.7} />
      {/* aircraft + bomb carts */}
      <Plane x={250} y={g - 120} s={1.25} t={t} nation={nat} type="divebomber" />
      <Plane x={1260} y={g - 128} s={1.1} t={t} nation={nat} type="fighter" flip />
      {[700, 860].map((x, i) => (
        <g key={i} transform={`translate(${x} ${g - 40})`}>
          <rect x={-70} y={-20} width={140} height={16} fill="#3a3a3a" stroke={INK} strokeWidth={3} />
          <circle cx={-50} cy={0} r={12} fill="#2a2a2a" stroke={INK} strokeWidth={3} />
          <circle cx={50} cy={0} r={12} fill="#2a2a2a" stroke={INK} strokeWidth={3} />
          <path d="M-60 -48 Q-60 -70 -20 -70 H40 L70 -59 L40 -48 Z" fill="#4f5a3a" stroke={INK} strokeWidth={3} />
          <path d="M-36 -70 V-48" stroke="#e3c84a" strokeWidth={4} />
        </g>
      ))}
      {/* fuel hose */}
      <path d={`M${X0} ${g - 20} Q300 ${g + 40} 520 ${g - 10} T980 ${g + 20}`} stroke="#2a2a2a" strokeWidth={12} fill="none" />
    </g>
  );
};

const Radio: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const wall = (p.wall as string) ?? '#5d6b62';
  return (
    <g>
      <rect x={X0} y={Y0} width={W} height={g - 120 - Y0} fill={wall} />
      {Array.from({ length: 12 }, (_, i) => <rect key={i} x={X0 + i * 200} y={Y0} width={6} height={g - 120 - Y0} fill="#000" opacity={0.08} />)}
      {/* radio racks */}
      {[200, 560, 1340, 1700].map((x, i) => (
        <g key={i} transform={`translate(${x} ${g - 120})`}>
          <rect x={-150} y={-560} width={300} height={560} fill="#3d4642" stroke={INK} strokeWidth={4} />
          {[0, 1, 2].map((r) => (
            <g key={r}>
              <rect x={-130} y={-540 + r * 175} width={260} height={150} fill="#2c3330" stroke={INK} strokeWidth={3} />
              {[0, 1, 2].map((d) => <g key={d}><circle cx={-80 + d * 80} cy={-490 + r * 175} r={22} fill="#e9dfc7" stroke={INK} strokeWidth={3} /><line x1={-80 + d * 80} y1={-490 + r * 175} x2={-80 + d * 80 + Math.cos(t * 0.7 + d + r + i) * 16} y2={-490 + r * 175 + Math.sin(t * 0.7 + d + r + i) * 16} stroke={C.red} strokeWidth={3} /></g>)}
              {[0, 1, 2, 3, 4].map((l) => <circle key={l} cx={-100 + l * 50} cy={-425 + r * 175} r={7} fill={Math.sin(t * (3 + l) + i * 2 + r) > 0.2 ? ['#7ce07a', '#f2c230', '#e85a50'][l % 3] : '#3a3a3a'} />)}
            </g>
          ))}
        </g>
      ))}
      {/* pinned messages */}
      {Array.from({ length: 7 }, (_, i) => (
        <g key={i} transform={`translate(${880 + (i % 4) * 110} ${160 + Math.floor(i / 4) * 140}) rotate(${(rnd('pm', i) - 0.5) * 10})`}>
          <rect x={-44} y={-54} width={88} height={108} fill="#f4ecd8" stroke={INK} strokeWidth={2.5} />
          {[0, 1, 2, 3].map((l) => <line key={l} x1={-32} x2={32} y1={-34 + l * 18} y2={-34 + l * 18} stroke={INK} strokeOpacity={0.4} strokeWidth={2} />)}
          <circle cx={0} cy={-48} r={6} fill={C.red} stroke={INK} strokeWidth={1.5} />
        </g>
      ))}
      <Lantern x={960} y={Y0} t={t} len={300} swing={1} />
      <Dust t={t} x={700} y={300} w={520} h={560} seed="rd" />
      <rect x={X0} y={g - 120} width={W} height={H} fill="#4a3f36" />
      <rect x={X0} y={g - 128} width={W} height={10} fill="#000" opacity={0.25} />
      {/* operator desk */}
      {p.desk !== false ? (
        <g>
          <rect x={560} y={g - 80} width={800} height={30} fill="#7a5a3a" stroke={INK} strokeWidth={4} />
          <rect x={580} y={g - 50} width={760} height={260} fill="#5a3e28" stroke={INK} strokeWidth={4} />
          <path d={`M700 ${g - 80} q30 -60 60 0`} stroke={INK} strokeWidth={6} fill="none" />
          <circle cx={700} cy={g - 82} r={14} fill="#3a3a3a" />
          <circle cx={760} cy={g - 82} r={14} fill="#3a3a3a" />
          <rect x={1100} y={g - 130} width={160} height={50} rx={6} fill="#2c3330" stroke={INK} strokeWidth={3} />
          <path d={`M1110 ${g - 110} h${20 + ((t * 40) % 120)}`} stroke="#7ce07a" strokeWidth={3} />
        </g>
      ) : null}
    </g>
  );
};

const Tent: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const canvas = (p.wall as string) ?? '#b3a27a';
  return (
    <g>
      <rect x={X0} y={Y0} width={W} height={H} fill={canvas} />
      {/* sloping roof seams */}
      {Array.from({ length: 9 }, (_, i) => <path key={i} d={`M${960} ${-140} L${X0 + i * 300} ${g - 120}`} stroke="#000" strokeOpacity={0.1} strokeWidth={6} />)}
      <path d={`M${X0} ${-160} L960 -140 L${X0 + W} -160 V60 Q960 120 ${X0} 60 Z`} fill="#000" opacity={0.12} />
      {/* open flap: outside view */}
      <path d={`M1560 ${g - 120} L1660 200 L1880 200 L1980 ${g - 120} Z`} fill={(p.outside as string) === 'snow' ? '#eef2f4' : '#a7c37a'} />
      <path d={`M1560 ${g - 120} L1660 200 L1880 200 L1980 ${g - 120}`} fill="none" stroke={INK} strokeWidth={5} />
      <path d={`M1660 200 L1560 ${g - 120} L1640 ${g - 120} Z`} fill={canvas} stroke={INK} strokeWidth={3} />
      <Lantern x={760} y={-140} t={t} len={160} swing={4} />
      {/* crates + map table */}
      {[[260, 0], [380, -90], [150, -90]].map(([x, dy], i) => (
        <g key={i} transform={`translate(${x} ${g - 120 + dy})`}>
          <rect x={-60} y={-90} width={120} height={90} fill="#8a6a3e" stroke={INK} strokeWidth={4} />
          <path d="M-60 -90 L60 0 M60 -90 L-60 0" stroke="#000" strokeOpacity={0.2} strokeWidth={4} />
        </g>
      ))}
      <rect x={X0} y={g - 120} width={W} height={H} fill="#7a6a4a" />
      {Array.from({ length: 30 }, (_, i) => <ellipse key={i} cx={X0 + rnd('tg', i) * W} cy={g - 90 + rnd('tgy', i) * 300} rx={30} ry={6} fill="#000" opacity={0.06} />)}
      {p.desk !== false ? (
        <g>
          <rect x={560} y={g - 70} width={800} height={26} fill="#8a6a3e" stroke={INK} strokeWidth={4} />
          <rect x={600} y={g - 92} width={720} height={24} fill="#e8dcb8" stroke={INK} strokeWidth={3} transform={`skewX(-8)`} />
          <path d={`M600 ${g - 44} L620 ${g + 120} M1320 ${g - 44} L1300 ${g + 120}`} stroke="#5a3e22" strokeWidth={14} />
        </g>
      ) : null}
    </g>
  );
};

const Airfield: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const nat = (p.nation as string) ?? 'USA';
  const hz = 620;
  return (
    <g>
      <SkyG id="sky_a" time={p.time} y2={hz + 10} />
      <Drift t={t} n={6} y={-40} h={260} seed="ac" />
      <path d={`M${X0} ${hz} Q400 ${hz - 50} 900 ${hz - 10} T${X0 + W} ${hz - 20} V${hz + 40} H${X0} Z`} fill="#8aa36a" />
      <rect x={X0} y={hz} width={W} height={H} fill="#a4bf6a" />
      {/* hangars + tower */}
      {[-60, 380].map((x, i) => (
        <g key={i} transform={`translate(${x} ${hz + 40})`}>
          <path d="M0 0 V-120 Q190 -260 380 -120 V0 Z" fill="#8a929a" stroke={INK} strokeWidth={4} />
          <rect x={90} y={-100} width={200} height={100} fill="#3a3f44" stroke={INK} strokeWidth={3} />
          {Array.from({ length: 7 }, (_, j) => <path key={j} d={`M${50 + j * 45} -150 V0`} stroke="#000" strokeOpacity={0.12} strokeWidth={3} />)}
        </g>
      ))}
      <g transform={`translate(1700 ${hz + 40})`}>
        <rect x={-30} y={-260} width={60} height={260} fill="#d8d0c0" stroke={INK} strokeWidth={4} />
        <rect x={-70} y={-330} width={140} height={74} fill="#a8b0b8" stroke={INK} strokeWidth={4} />
        <rect x={-60} y={-320} width={120} height={36} fill="#9fd0e8" stroke={INK} strokeWidth={2} />
        <g transform="translate(0 -330)"><line x1={0} y1={0} x2={0} y2={-80} stroke={INK} strokeWidth={4} /><g transform="translate(2 -80)"><Flag nation={nat} w={80} h={54} t={t} /></g></g>
      </g>
      {/* windsock */}
      <g transform={`translate(1300 ${hz + 30})`}>
        <line x1={0} y1={0} x2={0} y2={-160} stroke={INK} strokeWidth={5} />
        <path d={`M0 -160 L90 ${-150 + Math.sin(t * 3) * 6} L88 ${-128 + Math.sin(t * 3) * 6} L0 -132 Z`} fill="#e86a3a" stroke={INK} strokeWidth={3} />
        <path d={`M30 -156 V-130 M60 ${-153 + Math.sin(t * 3) * 4} V${-129 + Math.sin(t * 3) * 4}`} stroke="#fff" strokeWidth={6} />
      </g>
      {/* runway */}
      <path d={`M${X0} ${g - 90} H${X0 + W} V${g + 120} H${X0} Z`} fill="#6a6a66" />
      <path d={`M${X0} ${g + 14} H${X0 + W}`} stroke="#f2efe6" strokeWidth={10} strokeDasharray="90 70" />
      <path d={`M${X0} ${g - 90} H${X0 + W} M${X0} ${g + 120} H${X0 + W}`} stroke={INK} strokeWidth={4} />
      {(p.planes as number) !== 0 ? <Plane x={1100} y={g - 70} s={1.0} t={t} nation={nat} type="fighter" spin /> : null}
    </g>
  );
};

const Corridor: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const wall = (p.wall as string) ?? '#d6c9a8';
  return (
    <g>
      <rect x={X0} y={Y0} width={W} height={H} fill={wall} />
      {/* receding corridor in the middle */}
      <path d={`M700 ${g - 120} L860 520 H1060 L1220 ${g - 120} Z`} fill="#8a6a4a" />
      <path d={`M700 ${Y0} L860 200 H1060 L1220 ${Y0} Z`} fill="#f0e8d6" opacity={0.6} />
      <rect x={860} y={200} width={200} height={320} fill="#c9b892" stroke={INK} strokeWidth={4} />
      <rect x={910} y={260} width={100} height={260} fill="#5a3e28" stroke={INK} strokeWidth={3} />
      <path d={`M700 ${Y0} L860 200 M1220 ${Y0} L1060 200 M700 ${g - 120} L860 520 M1220 ${g - 120} L1060 520`} stroke={INK} strokeWidth={4} />
      {[0.3, 0.55, 0.75].map((k, i) => {
        const y1 = Y0 + (200 - Y0) * k, y2 = g - 120 + (520 - (g - 120)) * k;
        return <path key={i} d={`M${700 + 160 * k} ${y1} V${y2} M${1220 - 160 * k} ${y1} V${y2}`} stroke="#000" strokeOpacity={0.2} strokeWidth={6} />;
      })}
      {/* doors on the near walls */}
      {[260, 1660].map((x, i) => (
        <g key={i}>
          <rect x={x - 120} y={g - 520} width={240} height={400} fill="#6b4a32" stroke={INK} strokeWidth={5} />
          <rect x={x - 90} y={g - 490} width={180} height={150} fill="#9fc4d8" stroke={INK} strokeWidth={3} opacity={0.8} />
          <text x={x} y={g - 400} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={30} fill={INK} opacity={0.7}>{((p.doors as string[]) ?? ['ROOM 40', 'NO ENTRY'])[i]}</text>
          <circle cx={x + 80} cy={g - 300} r={9} fill="#d9b44a" stroke={INK} strokeWidth={2} />
        </g>
      ))}
      {[480, 960, 1440].map((x, i) => <Lantern key={i} x={x} y={Y0} t={t + i} len={140} swing={0.6} />)}
      <rect x={X0} y={g - 120} width={W} height={H} fill="#7a5a3a" />
      <path d={`M700 ${g - 120} L860 520 H1060 L1220 ${g - 120} Z`} fill="#000" opacity={0.08} />
      <rect x={X0} y={g - 128} width={W} height={10} fill="#000" opacity={0.2} />
      <path d={`M${X0} ${g - 20} H${X0 + W} V${g + 70} H${X0} Z`} fill="#8a2a2a" opacity={0.85} />
    </g>
  );
};

const Parliament: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const bench = (p.bench as string) ?? '#2f6b3a';
  return (
    <g>
      <rect x={X0} y={Y0} width={W} height={H} fill="#8a6a44" />
      {Array.from({ length: 13 }, (_, i) => (
        <g key={i}>
          <rect x={X0 + i * 200} y={Y0} width={180} height={g - 340 - Y0} fill="#9a7a50" stroke="#000" strokeOpacity={0.2} strokeWidth={4} />
          <path d={`M${X0 + 20 + i * 200} ${80} q70 -80 140 0 v200 h-140 z`} fill="#c9e0ea" stroke={INK} strokeWidth={3} opacity={0.75} />
        </g>
      ))}
      <rect x={X0} y={g - 380} width={W} height={40} fill="#5a3e22" stroke={INK} strokeWidth={3} />
      {/* tiers of benches with silhouettes */}
      {[0, 1, 2].map((r) => (
        <g key={r}>
          {Array.from({ length: 22 }, (_, i) => {
            const x = X0 + 40 + i * 110 + (r % 2) * 55;
            const y = g - 330 + r * 70;
            const nod = Math.sin(t * 2 + i * 1.7 + r) * 2;
            return (
              <g key={i} opacity={0.9 - r * 0.1}>
                <circle cx={x} cy={y - 26 + nod} r={22} fill="#3a3431" />
                <rect x={x - 26} y={y - 8} width={52} height={40} rx={10} fill="#2c2826" />
              </g>
            );
          })}
          <rect x={X0} y={g - 300 + r * 70} width={W} height={40} fill={bench} stroke={INK} strokeWidth={3} />
        </g>
      ))}
      <rect x={X0} y={g - 120} width={W} height={H} fill="#5a3e28" />
      <rect x={760} y={g - 150} width={400} height={60} fill="#7a5a3a" stroke={INK} strokeWidth={4} />
    </g>
  );
};

const Cell: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  return (
    <g>
      <rect x={X0} y={Y0} width={W} height={H} fill="#8d8a80" />
      {Array.from({ length: 30 }, (_, i) => <rect key={i} x={X0 + (i % 6) * 420 + ((Math.floor(i / 6)) % 2) * 210} y={Y0 + Math.floor(i / 6) * 180} width={400} height={170} fill="none" stroke="#000" strokeOpacity={0.1} strokeWidth={4} />)}
      <rect x={880} y={120} width={180} height={140} fill="#bfe0ef" stroke={INK} strokeWidth={5} />
      {[0, 1, 2, 3].map((i) => <line key={i} x1={900 + i * 46} x2={900 + i * 46} y1={120} y2={260} stroke="#3a3a3a" strokeWidth={10} />)}
      <path d={`M880 260 L640 ${g - 120} H1420 L1060 260 Z`} fill="#fff8dc" opacity={0.13} />
      <Dust t={t} x={700} y={300} w={600} h={460} seed="cd" />
      <rect x={X0} y={g - 120} width={W} height={H} fill="#6e6a62" />
      <rect x={1380} y={g - 210} width={500} height={60} fill="#7a6a5a" stroke={INK} strokeWidth={4} />
      <rect x={1380} y={g - 150} width={20} height={70} fill="#4a3a2a" />
      <rect x={1860} y={g - 150} width={20} height={70} fill="#4a3a2a" />
      {p.bars ? Array.from({ length: 14 }, (_, i) => <rect key={i} x={X0 + 40 + i * 180} y={Y0} width={22} height={H} fill="#3a3a3a" stroke={INK} strokeWidth={3} />) : null}
    </g>
  );
};

const TrainInterior: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const sway = Math.sin(t * 7) * 1.5;
  return (
    <g>
      {/* landscape rushing past */}
      <g>
        <SkyG id="sky_t" time={p.time} y1={Y0} y2={560} />
        <rect x={X0} y={460} width={W} height={200} fill={(p.outside as string) === 'snow' ? '#eef2f4' : '#8fae6a'} />
        {Array.from({ length: 12 }, (_, i) => {
          const x = ((X0 + i * 260 - t * 900) % W + W) % W + X0;
          return <g key={i} transform={`translate(${x} 470)`}><line x1={0} y1={0} x2={0} y2={-120} stroke="#5a4030" strokeWidth={6} /><line x1={-26} y1={-110} x2={26} y2={-110} stroke="#5a4030" strokeWidth={5} /></g>;
        })}
      </g>
      <g transform={`translate(0 ${sway})`}>
        <path d={`M${X0} ${Y0} H${X0 + W} V${g - 120} H${X0} Z ${[0, 1, 2, 3].map((i) => `M${-60 + i * 560} 140 h420 v360 h-420 z`).join(' ')}`} fill="#7a4a2e" fillRule="evenodd" />
        {[0, 1, 2, 3].map((i) => <rect key={i} x={-60 + i * 560} y={140} width={420} height={360} rx={30} fill="none" stroke="#c9a24a" strokeWidth={10} />)}
        <rect x={X0} y={560} width={W} height={260} fill="#6a3e26" />
        {Array.from({ length: 6 }, (_, i) => (
          <g key={i} transform={`translate(${-100 + i * 440} ${g - 120})`}>
            <rect x={-150} y={-300} width={300} height={200} rx={20} fill="#4a6a5a" stroke={INK} strokeWidth={4} />
            <rect x={-150} y={-110} width={300} height={70} rx={10} fill="#3f5a4a" stroke={INK} strokeWidth={4} />
          </g>
        ))}
        <rect x={X0} y={60} width={W} height={20} fill="#c9a24a" stroke={INK} strokeWidth={3} />
      </g>
      <rect x={X0} y={g - 120} width={W} height={H} fill="#5a4a3a" />
    </g>
  );
};

const Cockpit: React.FC<P> = (p) => {
  const t = p.t;
  const bank = Math.sin(t * 0.6) * 4 + ((p.bank as number) ?? 0);
  return (
    <g>
      <g transform={`rotate(${bank} 960 540)`}>
        <SkyG id="sky_c" time={p.time} y1={-700} y2={620} />
        <Drift t={t * 6} n={8} y={-100} h={600} seed="cc" sp={40} />
        <rect x={-800} y={600} width={3600} height={900} fill={(p.below as string) === 'land' ? '#8fae6a' : '#3f78a3'} />
        <Waves y={610} y2={1300} t={t * 3} seed="cw" n={30} />
      </g>
      {/* canopy frame + dashboard */}
      <path d={`M${X0} ${Y0} H${X0 + W} V1240 H${X0} Z M200 80 Q960 -40 1720 80 L1820 700 H100 Z`} fill="#3a3f3a" fillRule="evenodd" />
      <path d="M960 -20 V700" stroke="#3a3f3a" strokeWidth={30} />
      <path d={`M${X0} 720 Q960 640 ${X0 + W} 720 V1240 H${X0} Z`} fill="#2c302c" stroke={INK} strokeWidth={6} />
      {[560, 760, 1160, 1360].map((x, i) => (
        <g key={i} transform={`translate(${x} 840)`}>
          <circle r={70} fill="#1b1d1b" stroke="#8a8a80" strokeWidth={6} />
          <line x1={0} y1={0} x2={Math.cos(t * (0.5 + i * 0.3) + i) * 52} y2={Math.sin(t * (0.5 + i * 0.3) + i) * 52} stroke="#f2efe6" strokeWidth={5} strokeLinecap="round" />
        </g>
      ))}
      <circle cx={960} cy={840} r={80} fill="#1b1d1b" stroke="#8a8a80" strokeWidth={6} />
      <path d={`M890 ${840 + bank * 2} H1030`} stroke="#e3c84a" strokeWidth={6} />
    </g>
  );
};


const Poplar: React.FC<{ x: number; y: number; s?: number; t: number }> = ({ x, y, s = 1, t }) => (
  <g transform={`translate(${x} ${y}) scale(${s}) rotate(${Math.sin(t * 0.9 + x) * 1.5})`}>
    <rect x={-5} y={-30} width={10} height={30} fill="#5a4030" />
    <ellipse cx={0} cy={-110} rx={26} ry={90} fill="#4f7a3a" stroke={INK} strokeWidth={3} />
    <ellipse cx={-6} cy={-130} rx={10} ry={40} fill="#6a9a50" />
  </g>
);
const HouseRow: React.FC<{ x: number; y: number; n: number; t: number; burning?: boolean; seed: string; dir?: number }> = ({ x, y, n, t, burning, seed, dir = 1 }) => (
  <g>
    {Array.from({ length: n }, (_, i) => {
      const w = 150 + rnd(seed, i) * 60, h = 190 + rnd(seed, i, 'h') * 90;
      const hx = x + dir * i * 170;
      const wall = ['#b4644a', '#c98f62', '#a9553e', '#d6c9a8'][i % 4];
      const fire = burning && rnd(seed, i, 'f') > 0.4;
      return (
        <g key={i}>
          <rect x={hx - w / 2} y={y - h} width={w} height={h} fill={wall} stroke={INK} strokeWidth={3} />
          <path d={`M${hx - w / 2 - 10} ${y - h} L${hx} ${y - h - 70} L${hx + w / 2 + 10} ${y - h} Z`} fill={burning ? '#3a3431' : '#6a4a3a'} stroke={INK} strokeWidth={3} />
          {[0, 1].map((r) => [0, 1].map((c) => <rect key={`${r}${c}`} x={hx - w / 2 + 22 + c * (w / 2 - 6)} y={y - h + 30 + r * 80} width={w / 2 - 40} height={50} fill={fire ? '#f08a3a' : burning ? '#2a2422' : '#9fc4d8'} stroke={INK} strokeWidth={2.5} />))}
          {fire ? (
            <g>
              <path d={`M${hx - 30} ${y - h - 10} q${10 + Math.sin(t * 9 + i) * 6} -60 30 -90 q10 40 30 50 q10 -30 20 -50 q10 50 -10 90 Z`} fill="#f08a3a" opacity={0.95} />
              {[0, 1, 2].map((k) => {
                const q = (t * 0.5 + k / 3 + rnd(seed, i, 'k')) % 1;
                return <circle key={k} cx={hx + q * 120} cy={y - h - 60 - q * 300} r={30 + q * 60} fill="#3a3632" opacity={0.55 * (1 - q)} />;
              })}
            </g>
          ) : null}
        </g>
      );
    })}
  </g>
);

const ArchBridge: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const time = (p.time as string) ?? 'dusk';
  const deckY = 540, x1 = -200, x2 = 2100, a1 = 260, a2 = 1660, apex = 120;
  const archY = (x: number) => deckY - (deckY - apex) * (1 - ((x - (a1 + a2) / 2) / ((a2 - a1) / 2)) ** 2);
  const water = time === 'night' ? '#14263d' : time === 'dusk' ? '#5a6f8a' : '#4f7fa3';
  return (
    <g>
      <SkyG id="sky_ab" time={time} y2={deckY + 40} />
      {time !== 'night' ? <Drift t={t} n={5} y={-60} h={200} seed="abc" c={time === 'dusk' ? '#f3c9a8' : undefined} /> : null}
      <rect x={X0} y={deckY + 20} width={W} height={300} fill={water} />
      <Waves y={deckY + 30} y2={deckY + 290} t={t} seed="abw" n={22} op={0.22} />
      {/* far bank */}
      <rect x={X0} y={deckY + 6} width={W} height={26} fill="#6f8a4a" />
      {/* arch + hangers */}
      <path d={`M${a1} ${deckY} Q${(a1 + a2) / 2} ${2 * apex - deckY} ${a2} ${deckY}`} stroke="#5d6b70" strokeWidth={36} fill="none" />
      <path d={`M${a1} ${deckY} Q${(a1 + a2) / 2} ${2 * apex - deckY} ${a2} ${deckY}`} stroke={INK} strokeWidth={42} fill="none" opacity={0.25} />
      <path d={`M${a1 + 60} ${deckY} Q${(a1 + a2) / 2} ${2 * apex - deckY + 90} ${a2 - 60} ${deckY}`} stroke="#6f7d82" strokeWidth={16} fill="none" />
      {Array.from({ length: 17 }, (_, i) => {
        const x = a1 + 60 + (i * (a2 - a1 - 120)) / 16;
        return <line key={i} x1={x} y1={archY(x) + 14} x2={x} y2={deckY} stroke="#4f5b60" strokeWidth={6} />;
      })}
      {/* deck + piers */}
      <rect x={x1} y={deckY - 14} width={x2 - x1} height={30} fill="#7a868a" stroke={INK} strokeWidth={4} />
      <path d={`M${x1} ${deckY - 22} H${x2}`} stroke={INK} strokeWidth={3} />
      {Array.from({ length: 46 }, (_, i) => <line key={i} x1={x1 + i * 50} y1={deckY - 22} x2={x1 + i * 50} y2={deckY - 14} stroke={INK} strokeWidth={2} />)}
      {[a1, a2].map((x) => <rect key={x} x={x - 40} y={deckY + 14} width={80} height={140} fill="#9a9488" stroke={INK} strokeWidth={4} />)}
      {/* near bank: embankment, houses, ramp road */}
      <path d={`M${X0} ${deckY + 260} Q960 ${deckY + 220} ${X0 + W} ${deckY + 260} V${Y0 + H} H${X0} Z`} fill={time === 'night' ? '#3a3f3a' : '#7a8a5a'} />
      <HouseRow x={-120} y={g - 120} n={4} t={t} burning={!!p.burning} seed="hrL" />
      <HouseRow x={2060} y={g - 120} n={4} t={t} burning={!!p.burning} seed="hrR" dir={-1} />
      <path d={`M560 ${Y0 + H} L860 ${deckY + 30} H1060 L1360 ${Y0 + H} Z`} fill="#8a8478" />
      <path d={`M960 ${deckY + 40} V${Y0 + H}`} stroke="#fff" strokeWidth={6} strokeDasharray="40 40" opacity={0.5} />
      <rect x={X0} y={g - 120} width={W} height={Y0 + H - g + 120} fill={time === 'night' ? '#3d3a36' : '#8a8478'} opacity={0.92} />
      <path d={`M${X0} ${g - 120} H${X0 + W}`} stroke={INK} strokeWidth={4} opacity={0.4} />
      {p.label ? <g transform="translate(960 70)"><rect x={-260} y={-34} width={520} height={60} rx={6} fill="#fbf8f0" stroke={INK} strokeWidth={4} /><text y={10} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={36} fill={INK}>{(p.label as string).toUpperCase()}</text></g> : null}
    </g>
  );
};

const River: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const time = (p.time as string) ?? 'day';
  const fb = 470;
  return (
    <g>
      <SkyG id="sky_rv" time={time} y2={fb + 20} />
      <Drift t={t} n={5} y={-80} h={220} seed="rvc" />
      {/* far bank: dyke, trees, distant bridge */}
      <rect x={X0} y={fb - 40} width={W} height={60} fill="#7f9a52" />
      <path d={`M${X0} ${fb - 30} H${X0 + W}`} stroke="#5f7a3a" strokeWidth={14} />
      {Array.from({ length: 16 }, (_, i) => <Poplar key={i} x={X0 + 80 + i * 160 + rnd('rp', i) * 60} y={fb - 34} s={0.55} t={t} />)}
      {p.bridges !== false ? (
        <g opacity={0.85}>
          <path d={`M1500 ${fb - 50} Q1760 ${fb - 190} 2020 ${fb - 50}`} stroke="#5d6b70" strokeWidth={12} fill="none" />
          <rect x={1400} y={fb - 56} width={760} height={12} fill="#7a868a" stroke={INK} strokeWidth={3} />
        </g>
      ) : null}
      <rect x={X0} y={fb + 10} width={W} height={g - fb - 70} fill={time === 'night' ? '#14263d' : '#4a7a9c'} />
      <Waves y={fb + 14} y2={g - 70} t={t * 2.2} seed="rvw" n={46} op={0.3} />
      {/* current streaks */}
      {Array.from({ length: 10 }, (_, i) => {
        const x = ((X0 + rnd('cs', i) * W + t * 140) % W + W) % W + X0;
        const y = fb + 40 + rnd('csy', i) * (g - fb - 150);
        return <path key={i} d={`M${x} ${y} h120`} stroke="#fff" strokeOpacity={0.18} strokeWidth={4} strokeLinecap="round" />;
      })}
      {/* near bank */}
      <path d={`M${X0} ${g - 70} Q960 ${g - 110} ${X0 + W} ${g - 70} V${Y0 + H} H${X0} Z`} fill="#c9b48a" />
      <path d={`M${X0} ${g - 70} Q960 ${g - 110} ${X0 + W} ${g - 70}`} stroke={INK} strokeWidth={4} fill="none" opacity={0.4} />
      {Array.from({ length: 30 }, (_, i) => <ellipse key={i} cx={X0 + rnd('rb', i) * W} cy={g - 40 + rnd('rby', i) * 250} rx={14} ry={5} fill="#000" opacity={0.08} />)}
    </g>
  );
};

const Polder: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const time = (p.time as string) ?? 'day';
  const dykeY = (p.dyke as number) ?? 620;
  return (
    <g>
      <SkyG id="sky_pd" time={time} y2={dykeY + 40} />
      <Drift t={t} n={7} y={-80} h={260} seed="pdc" />
      <rect x={X0} y={dykeY - 10} width={W} height={H} fill="#8fae5a" />
      {/* windmill */}
      <g transform={`translate(1820 ${dykeY - 10})`}>
        <path d="M-40 0 L-26 -170 H26 L40 0 Z" fill="#7a5a3a" stroke={INK} strokeWidth={4} />
        <path d="M-30 -170 Q0 -210 30 -170 Z" fill="#5a3e28" stroke={INK} strokeWidth={4} />
        <g transform={`translate(0 -176) rotate(${t * 20})`}>
          {[0, 90, 180, 270].map((a) => <g key={a} transform={`rotate(${a})`}><rect x={-6} y={-150} width={12} height={150} fill="#e9e1cf" stroke={INK} strokeWidth={3} /><rect x={6} y={-140} width={30} height={110} fill="none" stroke={INK} strokeWidth={2} /></g>)}
        </g>
      </g>
      {[200, 340, 480, 1150, 1290].map((x, i) => <Poplar key={i} x={x} y={dykeY - 6} s={0.8} t={t} />)}
      {/* the raised road on its dyke */}
      <path d={`M${X0} ${dykeY + 40} L${X0} ${dykeY - 14} H${X0 + W} V${dykeY + 40} Z`} fill="#6f8a4a" />
      <rect x={X0} y={dykeY - 30} width={W} height={18} fill="#9a9488" stroke={INK} strokeWidth={3} />
      {/* ditches + fields toward the viewer */}
      {Array.from({ length: 9 }, (_, i) => <path key={i} d={`M${X0} ${dykeY + 80 + i * i * 8} H${X0 + W}`} stroke="#5b86a8" strokeWidth={4 + i} opacity={0.55} />)}
      {Array.from({ length: 12 }, (_, i) => <line key={i} x1={960 + (i - 6) * 60} y1={dykeY + 50} x2={960 + (i - 6) * 420} y2={Y0 + H} stroke="#5b86a8" strokeWidth={6} opacity={0.35} />)}
      <rect x={X0} y={g - 120} width={W} height={H} fill="#7fa04e" />
      {Array.from({ length: 60 }, (_, i) => <path key={i} d={`M${X0 + rnd('pg', i) * W} ${g - 110 + rnd('pgy', i) * 300} l4 -12 l4 12`} stroke="#5f8a3a" strokeWidth={3} fill="none" />)}
    </g>
  );
};

const Cabin: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const light = p.jumplight as string | undefined;
  const sway = Math.sin(t * 1.4) * 2;
  return (
    <g transform={`rotate(${sway * 0.4} 960 540)`}>
      <rect x={X0} y={Y0} width={W} height={H} fill="#5f6650" />
      {/* ribs */}
      {Array.from({ length: 12 }, (_, i) => <path key={i} d={`M${X0 + i * 220} ${g - 120} Q${X0 + i * 220} ${-40} ${X0 + i * 220 + 40} ${-160}`} stroke="#4c5240" strokeWidth={22} fill="none" />)}
      {/* round windows with passing clouds */}
      {Array.from({ length: 6 }, (_, i) => {
        const cx = 120 + i * 340;
        return (
          <g key={i}>
            <circle cx={cx} cy={300} r={58} fill="#9fd0ea" stroke={INK} strokeWidth={6} />
            <circle cx={cx + ((t * 120 + i * 50) % 160) - 80} cy={310} r={26} fill="#fff" opacity={0.85} />
            <circle cx={cx} cy={300} r={58} fill="none" stroke="#8a8f7a" strokeWidth={12} />
          </g>
        );
      })}
      {/* benches */}
      <rect x={X0} y={g - 260} width={W} height={36} fill="#7a6a4a" stroke={INK} strokeWidth={4} />
      <rect x={X0} y={g - 120} width={W} height={H} fill="#4c5240" />
      {Array.from({ length: 20 }, (_, i) => <line key={i} x1={X0 + i * 130} y1={g - 120} x2={X0 + i * 130 - 100} y2={Y0 + H} stroke="#000" strokeOpacity={0.15} strokeWidth={4} />)}
      <path d={`M${X0} ${-60} H${X0 + W}`} stroke="#c9c2a8" strokeWidth={6} />
      {light ? (
        <g transform="translate(1900 120)">
          <rect x={-40} y={-30} width={80} height={60} rx={10} fill="#2a2a2a" stroke={INK} strokeWidth={4} />
          <circle r={20} fill={light === 'green' ? '#5ae07a' : '#e8463a'} />
          <circle r={70} fill={light === 'green' ? '#5ae07a' : '#e8463a'} opacity={0.15 + 0.1 * Math.sin(t * 6)} />
        </g>
      ) : null}
      {light === 'red' ? <rect x={X0} y={Y0} width={W} height={H} fill="#c8352b" opacity={0.08} /> : null}
    </g>
  );
};

const Heath: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const hz = 600;
  return (
    <g>
      <SkyG id="sky_ht" time={p.time} y2={hz + 20} />
      <Drift t={t} n={6} y={-60} h={240} seed="htc" />
      {Array.from({ length: 30 }, (_, i) => <Tree key={i} x={X0 + i * 90 + rnd('ht', i) * 40} y={hz + 10} s={0.55 + rnd('hs', i) * 0.25} kind="pine" />)}
      <rect x={X0} y={hz} width={W} height={H} fill="#9a8a5a" />
      {Array.from({ length: 90 }, (_, i) => <ellipse key={i} cx={X0 + rnd('hh', i) * W} cy={hz + 20 + rnd('hy', i) * (Y0 + H - hz)} rx={30 + rnd('hr', i) * 40} ry={10} fill={i % 3 ? '#8a6a7a' : '#7a8a4a'} opacity={0.5} />)}
      {p.panels !== false ? [[600, hz + 140], [1300, hz + 200]].map(([x, y], i) => <rect key={i} x={x} y={y} width={120} height={30} fill={i ? '#e8463a' : '#f2c230'} stroke={INK} strokeWidth={3} transform={`skewX(-20)`} />) : null}
      <rect x={X0} y={g - 120} width={W} height={H} fill="#8f7f52" opacity={0.6} />
    </g>
  );
};

const Hotel: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  return (
    <g>
      <SkyG id="sky_hl" time={p.time} y2={g} />
      <Drift t={t} n={5} y={-80} h={200} seed="hlc" />
      {Array.from({ length: 10 }, (_, i) => <Tree key={i} x={X0 + i * 260 + 60} y={g - 230} s={1.2 + rnd('hlt', i) * 0.4} kind="round" />)}
      <g transform={`translate(960 ${g - 120})`}>
        <rect x={-560} y={-520} width={1120} height={520} fill="#f2ecdf" stroke={INK} strokeWidth={5} />
        <path d="M-600 -520 L0 -660 L600 -520 Z" fill="#7a4a3a" stroke={INK} strokeWidth={5} />
        {[0, 1].map((r) => Array.from({ length: 7 }, (_, c) => <rect key={`${r}${c}`} x={-500 + c * 150} y={-470 + r * 190} width={90} height={120} fill="#9fc4d8" stroke={INK} strokeWidth={3} />))}
        <rect x={-600} y={-150} width={1200} height={22} fill="#e9e1cf" stroke={INK} strokeWidth={4} />
        {Array.from({ length: 9 }, (_, i) => <rect key={i} x={-580 + i * 145} y={-128} width={14} height={128} fill="#e9e1cf" stroke={INK} strokeWidth={3} />)}
        <rect x={-260} y={-610} width={520} height={60} rx={6} fill="#24473a" stroke={INK} strokeWidth={4} />
        <text y={-568} textAnchor="middle" fontFamily={FONT.serif} fontWeight={900} fontSize={40} fill="#e9d9a8" letterSpacing={4}>{((p.name as string) ?? 'HOTEL').toUpperCase()}</text>
      </g>
      <rect x={X0} y={g - 120} width={W} height={H} fill="#8fbe5a" />
      <path d={`M${X0} ${g - 50} H${X0 + W} V${g + 60} H${X0} Z`} fill="#d8c8a2" />
    </g>
  );
};


/** a warm wooden workroom: plank wall, pinned papers, shelf, hanging lamp, desk edge. The home of the physical devices. */
const Workshop: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 940;
  const desk = p.desk !== false;
  return (
    <g>
      <defs>
        <linearGradient id="ws_wall" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#5b3f29" />
          <stop offset="0.6" stopColor="#71503a" />
          <stop offset="1" stopColor="#4a3322" />
        </linearGradient>
        <linearGradient id="ws_desk" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#8d5f3a" />
          <stop offset="0.12" stopColor="#6e4527" />
          <stop offset="1" stopColor="#3f2716" />
        </linearGradient>
      </defs>
      <rect x={X0} y={Y0} width={W} height={H} fill="url(#ws_wall)" />
      {/* vertical planks with seams, grain and nail heads */}
      {Array.from({ length: 21 }, (_, i) => {
        const x = X0 + i * 120;
        const tone = rnd('wsp', i) * 0.12 - 0.06;
        return (
          <g key={i}>
            <rect x={x} y={Y0} width={120} height={H} fill={tone > 0 ? '#fff' : '#000'} opacity={Math.abs(tone)} />
            <path d={`M${x} ${Y0} V${Y0 + H}`} stroke="#2e1d12" strokeWidth={4} opacity={0.7} />
            {[0, 1, 2].map((k) => (
              <path key={k} d={`M${x + 22 + k * 34 + rnd('wsg', i, k) * 10} ${Y0} q${8 - rnd('wsq', i, k) * 16} ${H / 2} 0 ${H}`} stroke="#3a2516" strokeWidth={1.6} opacity={0.35} fill="none" />
            ))}
            <circle cx={x + 60} cy={60} r={4} fill="#2a2018" />
            <circle cx={x + 60} cy={720} r={4} fill="#2a2018" />
          </g>
        );
      })}
      {/* shelf with jars and box files, top right */}
      <rect x={1560} y={250} width={520} height={18} fill="#8d5f3a" stroke={INK} strokeWidth={4} />
      {[1590, 1650, 1710].map((x, i) => <rect key={x} x={x} y={130} width={50} height={120} rx={4} fill={['#7a2e26', '#3e4f63', '#6b6a3e'][i]} stroke={INK} strokeWidth={3} />)}
      {[1800, 1880].map((x) => <path key={x} d={`M${x} 250 v-70 q0 -14 14 -14 h30 q14 0 14 14 v70 Z`} fill="#c8d6d4" opacity={0.85} stroke={INK} strokeWidth={3} />)}
      {/* pinned sketch + clipboard */}
      <g transform="translate(-60 160) rotate(-3)">
        <rect width={260} height={190} fill="#efe6d0" stroke={INK} strokeWidth={3} />
        <path d="M24 140 Q80 60 130 110 T236 60" stroke="#7a5a3a" strokeWidth={3} fill="none" />
        <circle cx={130} cy={8} r={7} fill="#b8322a" stroke={INK} strokeWidth={2} />
      </g>
      <g transform="translate(1900 420) rotate(4)">
        <rect width={170} height={230} rx={6} fill="#a87a4a" stroke={INK} strokeWidth={3} />
        <rect x={14} y={28} width={142} height={186} fill="#f1e9d4" />
        {[0, 1, 2, 3, 4].map((k) => <path key={k} d={`M28 ${64 + k * 30} h${90 + (k % 2) * 20}`} stroke="#6a6a6a" strokeWidth={3} />)}
        <rect x={56} y={12} width={58} height={24} rx={4} fill="#9a9a9a" stroke={INK} strokeWidth={2.5} />
      </g>
      <Lantern x={960} y={Y0} t={t} len={170} swing={1.5} />
      <Dust t={t} x={600} y={200} w={720} h={700} n={22} seed="ws" />
      {desk ? (
        <g>
          <rect x={X0} y={g} width={W} height={1240 - g + 20} fill="url(#ws_desk)" />
          <path d={`M${X0} ${g} H${X0 + W}`} stroke="#b07a4a" strokeWidth={5} />
          <path d={`M${X0} ${g + 4} H${X0 + W}`} stroke={INK} strokeWidth={3} opacity={0.6} />
        </g>
      ) : null}
    </g>
  );
};

export const RichSet: React.FC<P> = (p) => {
  switch (p.kind) {
    case 'workshop':
    case 'board': return <Workshop {...p} />;
    case 'archbridge': return <ArchBridge {...p} />;
    case 'river': return <River {...p} />;
    case 'polder': return <Polder {...p} />;
    case 'cabin': return <Cabin {...p} />;
    case 'heath': return <Heath {...p} />;
    case 'hotel': return <Hotel {...p} />;
    case 'garden': return <Garden {...p} />;
    case 'bridge': return <Bridge {...p} />;
    case 'deck':
    case 'flightdeck': return <FlightDeck {...p} />;
    case 'hangar': return <Hangar {...p} />;
    case 'radio': return <Radio {...p} />;
    case 'tent': return <Tent {...p} />;
    case 'airfield': return <Airfield {...p} />;
    case 'corridor': return <Corridor {...p} />;
    case 'parliament': return <Parliament {...p} />;
    case 'cell': return <Cell {...p} />;
    case 'train_interior': return <TrainInterior {...p} />;
    case 'cockpit': return <Cockpit {...p} />;
    default: return null;
  }
};

// ---------------- lighting pass ----------------
const INTERIOR = new Set(['office', 'study', 'cabinet', 'conference', 'warroom', 'bunker', 'codebreak', 'classroom', 'kitchen', 'home', 'factory', 'bridge', 'hangar', 'radio', 'tent', 'corridor', 'parliament', 'cell', 'train_interior']);
const WINDOWED = new Set(['office', 'study', 'cabinet', 'conference', 'kitchen', 'home']);
const LAMPLIT = new Set(['warroom', 'bunker', 'codebreak', 'classroom']);

/** Soft light and shadow over the set (under the actors): corner falloff, window shafts with dust, lamp dust, floor contact. */
export const Lighting: React.FC<P> = (p) => {
  const t = p.t, g = (p.ground as number) ?? 900;
  const mode = (p.light as string) ?? (INTERIOR.has(p.kind) ? 'room' : 'out');
  if (mode === 'none') return null;
  const night = p.time === 'night';
  const id = 'lt_' + p.kind;
  return (
    <g style={{ pointerEvents: 'none' }}>
      <defs>
        <radialGradient id={id} cx="0.5" cy="0.42" r="0.75">
          <stop offset="0.45" stopColor="#000" stopOpacity={0} />
          <stop offset="1" stopColor={night ? '#050a1a' : '#1a120a'} stopOpacity={mode === 'room' ? 0.42 : 0.22} />
        </radialGradient>
        <linearGradient id={id + 'f'} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#000" stopOpacity={0.22} />
          <stop offset="1" stopColor="#000" stopOpacity={0} />
        </linearGradient>
      </defs>
      {mode === 'room' ? <rect x={X0} y={g - 120} width={W} height={60} fill={`url(#${id}f)`} /> : null}
      {mode === 'room' && WINDOWED.has(p.kind) && !night ? (
        <g>
          <path d={`M1180 140 L1510 140 L1300 ${g + 200} L760 ${g + 200} Z`} fill="#fff6d8" opacity={0.13} />
          <Dust t={t} x={820} y={220} w={560} h={g - 200} seed="wd" />
        </g>
      ) : null}
      {mode === 'room' && LAMPLIT.has(p.kind) ? <Dust t={t} x={720} y={260} w={500} h={g - 300} seed="ld" c="#fff3c0" /> : null}
      {p.kind === 'sea' || p.kind === 'ocean' ? <ellipse cx={1500} cy={620} rx={600} ry={90} fill="#fff" opacity={0.1 + 0.04 * Math.sin(t * 1.3)} /> : null}
      <rect x={X0} y={Y0} width={W} height={H} fill={`url(#${id})`} />
    </g>
  );
};

// ---------------- foreground layer (drawn over the actors) ----------------
export const Foreground: React.FC<{ kind: string; t: number; side?: string }> = ({ kind, t, side = 'both' }) => {
  const L = side === 'both' || side === 'left', R = side === 'both' || side === 'right';
  const sway = Math.sin(t * 0.9) * 2;
  switch (kind) {
    case 'plant':
      return (
        <g opacity={0.95}>
          {L ? <g transform={`translate(-60 1180) rotate(${sway})`}>{[-50, -25, 0, 25, 50].map((a, i) => <path key={i} transform={`rotate(${a})`} d="M0 0 Q-60 -260 0 -460 Q60 -260 0 0" fill={i % 2 ? '#2f4f2a' : '#3c6334'} stroke={INK} strokeWidth={4} />)}</g> : null}
          {R ? <g transform={`translate(1990 1200) rotate(${-sway})`}>{[-40, -15, 15, 40].map((a, i) => <path key={i} transform={`rotate(${a})`} d="M0 0 Q-50 -220 0 -400 Q50 -220 0 0" fill={i % 2 ? '#2f4f2a' : '#3c6334'} stroke={INK} strokeWidth={4} />)}</g> : null}
        </g>
      );
    case 'curtain':
      return (
        <g>
          {L ? <path d={`M-240 -160 H${120 + sway * 4} Q60 400 ${150 + sway * 3} 1240 H-240 Z`} fill="#5a1d1d" stroke={INK} strokeWidth={5} /> : null}
          {R ? <path d={`M2160 -160 H${1800 - sway * 4} Q1860 400 ${1770 - sway * 3} 1240 H2160 Z`} fill="#5a1d1d" stroke={INK} strokeWidth={5} /> : null}
        </g>
      );
    case 'rail':
      return (
        <g>
          <rect x={-240} y={1000} width={2400} height={22} fill="#7a828c" stroke={INK} strokeWidth={4} />
          <rect x={-240} y={1070} width={2400} height={16} fill="#7a828c" stroke={INK} strokeWidth={4} />
          {Array.from({ length: 14 }, (_, i) => <rect key={i} x={-200 + i * 180} y={1000} width={18} height={240} fill="#6a727c" stroke={INK} strokeWidth={3} />)}
        </g>
      );
    case 'grass':
      return (
        <g>
          {Array.from({ length: 70 }, (_, i) => {
            const x = -240 + i * 36 + rnd('fg', i) * 20;
            const h = 60 + rnd('fgh', i) * 90;
            const b = Math.sin(t * 1.4 + i * 0.5) * 8;
            return <path key={i} d={`M${x} 1240 Q${x + b} ${1240 - h / 2} ${x + b * 2} ${1240 - h} Q${x + 6 + b} ${1240 - h / 2} ${x + 14} 1240 Z`} fill={i % 3 ? '#4f7a3a' : '#3f6b30'} />;
          })}
        </g>
      );
    case 'sandbags':
      return (
        <g>
          {Array.from({ length: 24 }, (_, i) => {
            const row = Math.floor(i / 12), x = -240 + (i % 12) * 210 + row * 105;
            return <ellipse key={i} cx={x} cy={1150 - row * 60} rx={115} ry={42} fill={row ? '#b5a27a' : '#a8956c'} stroke={INK} strokeWidth={4} />;
          })}
        </g>
      );
    case 'officedesk':
    case 'frontdesk':
      return (
        <g>
          <rect x={410} y={840} width={1100} height={34} fill="#b27a47" stroke={INK} strokeWidth={4} />
          <rect x={420} y={874} width={1080} height={380} fill="#8a5a33" stroke={INK} strokeWidth={4} />
          <rect x={460} y={910} width={1000} height={6} fill="#000" opacity={0.15} />
          {[0, 1].map((i) => <g key={i}><rect x={480 + i * 760} y={930} width={200} height={70} fill="#7a4e2c" stroke={INK} strokeWidth={3} /><circle cx={580 + i * 760} cy={965} r={7} fill="#d9b44a" /></g>)}
        </g>
      );
    case 'desk':
      return (
        <g>
          <rect x={-240} y={1060} width={2400} height={200} fill="#5a3a22" stroke={INK} strokeWidth={6} />
          <rect x={-240} y={1060} width={2400} height={18} fill="#7a5a3a" />
        </g>
      );
    case 'doorframe':
      return (
        <g fill="#3a2a1e" stroke={INK} strokeWidth={6}>
          {L ? <rect x={-240} y={-160} width={300} height={1400} /> : null}
          {R ? <rect x={1860} y={-160} width={300} height={1400} /> : null}
          <rect x={-240} y={-160} width={2400} height={170} />
        </g>
      );
    case 'branches':
      return (
        <g transform={`rotate(${sway * 0.6} 0 -160)`}>
          <path d="M-240 -60 Q200 -40 520 60 M120 -40 Q200 40 160 140 M330 10 Q400 90 380 170" stroke="#3a2e22" strokeWidth={22} fill="none" strokeLinecap="round" />
          {Array.from({ length: 16 }, (_, i) => <ellipse key={i} cx={-160 + rnd('br', i) * 700} cy={-40 + rnd('bry', i) * 200} rx={46} ry={22} transform={`rotate(${rnd('bra', i) * 180} ${-160 + rnd('br', i) * 700} ${-40 + rnd('bry', i) * 200})`} fill={i % 2 ? '#3c6334' : '#4f7a3a'} />)}
        </g>
      );
    case 'barbed':
      return (
        <g stroke="#2a2a2a" strokeWidth={4} fill="none">
          {Array.from({ length: 8 }, (_, i) => <path key={i} d={`M${-240 + i * 320} 1180 L${-240 + i * 320} 1000`} strokeWidth={14} />)}
          {[1030, 1080, 1130].map((y, j) => <path key={j} d={`M-240 ${y} ${Array.from({ length: 60 }, (_, i) => `L${-240 + i * 42} ${y + (i % 2 ? 10 : -10)}`).join(' ')}`} />)}
        </g>
      );
    default:
      return null;
  }
};
