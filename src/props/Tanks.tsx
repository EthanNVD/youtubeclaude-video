import React from 'react';
import { INK, nation } from '../theme';
import { Mark } from './Vehicles';

/**
 * Armour drawn with volume, after the reference channel:
 * - lit top and darker sides;
 * - a track run whose links move with the distance travelled;
 * - drive sprocket, idler, hubcap road wheels, return rollers;
 * - a turret with mantlet and barrel, stowage, small markings, mud on the lower hull.
 * Side view facing right; origin = ground contact centre; length ≈ 360 px at scale 1.
 */
type Spec = {
  hull: string; // hull colour override
  wheels: number; // road wheels
  wheelR: number;
  hullTop: number; // y of hull roof
  glacis: number; // front slope length
  turret: [number, number, number, number]; // x, w, h, roof slope
  gun: number; // barrel length
  muzzle: boolean;
  bogies?: boolean; // Sherman-style bogie units
  boxy?: boolean; // Tiger / Panzer IV slab sides
  schurzen?: boolean;
};
const SPECS: Record<string, Spec> = {
  tank: { hull: '', wheels: 5, wheelR: 22, hullTop: -112, glacis: 70, turret: [-40, 150, 52, 18], gun: 170, muzzle: false },
  sherman: { hull: '', wheels: 6, wheelR: 18, hullTop: -118, glacis: 80, turret: [-30, 140, 56, 26], gun: 150, muzzle: false, bogies: true },
  panzer4: { hull: '', wheels: 8, wheelR: 15, hullTop: -108, glacis: 30, turret: [-50, 150, 50, 10], gun: 190, muzzle: true, boxy: true, schurzen: true },
  tiger: { hull: '', wheels: 8, wheelR: 24, hullTop: -122, glacis: 26, turret: [-70, 190, 62, 6], gun: 230, muzzle: true, boxy: true },
  t34: { hull: '', wheels: 5, wheelR: 26, hullTop: -106, glacis: 92, turret: [-20, 140, 48, 30], gun: 170, muzzle: false },
  panther: { hull: '', wheels: 8, wheelR: 22, hullTop: -116, glacis: 96, turret: [-60, 160, 52, 22], gun: 250, muzzle: true },
  stug: { hull: '', wheels: 6, wheelR: 18, hullTop: -100, glacis: 40, turret: [-10, 0, 0, 0], gun: 160, muzzle: true, boxy: true },
};

const shade = (hex: string, k: number) => {
  const n = parseInt(hex.replace('#', ''), 16);
  const f = (v: number) => Math.max(0, Math.min(255, Math.round(k < 0 ? v * (1 + k) : v + (255 - v) * k)));
  return '#' + ((1 << 24) | (f((n >> 16) & 255) << 16) | (f((n >> 8) & 255) << 8) | f(n & 255)).toString(16).slice(1);
};

export const TANK_TYPES = Object.keys(SPECS);

export const Tank: React.FC<{ type: string; nationKey?: string; color?: string; travel: number; moving: boolean; t: number; damaged?: boolean; crew?: boolean }> = ({ type, nationKey, color, travel, moving, t, damaged, crew }) => {
  const S = SPECS[type] ?? SPECS.tank;
  const n = nation(nationKey);
  const base = color ?? (S.hull || n.uniform);
  const top = shade(base, 0.22), side = base, low = shade(base, -0.28);
  const L = 175; // half length of the track run
  const tY = -16, tR = 26; // track run centre-line, end radius
  const bob = moving ? Math.sin(travel / 18) * 1.4 : 0;
  const link = (travel * 1.0) % 16;
  const wheelRot = (travel / S.wheelR) * (180 / Math.PI);
  const wx = Array.from({ length: S.wheels }, (_, i) => -L + 46 + (i * (2 * L - 92)) / (S.wheels - 1));
  const [tx, tw, th, ts] = S.turret;
  const hullFront = L + 18;
  const hullBack = -L - 14;
  const hullD = `M${hullBack} ${tY - 30} L${hullBack + 6} ${S.hullTop + 14} Q${hullBack + 10} ${S.hullTop} ${hullBack + 30} ${S.hullTop} L${hullFront - S.glacis} ${S.hullTop} L${hullFront} ${tY - 40} L${hullFront - 10} ${tY - 26} Z`;
  return (
    <g>
      <ellipse cx={0} cy={4} rx={L + 30} ry={10} fill="#000" opacity={0.2} />
      <g transform={`translate(0 ${bob})`}>
        {/* hull */}
        <path d={hullD} fill={side} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
        <path d={`M${hullBack + 30} ${S.hullTop} L${hullFront - S.glacis} ${S.hullTop} L${hullFront - S.glacis + 8} ${S.hullTop + 10} L${hullBack + 26} ${S.hullTop + 10} Z`} fill={top} opacity={0.9} />
        <path d={`M${hullFront - S.glacis} ${S.hullTop} L${hullFront} ${tY - 40}`} stroke={top} strokeWidth={6} opacity={0.7} />
        {S.boxy ? <path d={`M${hullBack + 20} ${S.hullTop + 30} H${hullFront - 30}`} stroke={low} strokeWidth={3} /> : null}
        {/* stowage + tools */}
        <rect x={hullBack + 34} y={S.hullTop + 16} width={60} height={22} rx={3} fill={low} stroke={INK} strokeWidth={2.5} />
        <path d={`M${hullBack + 110} ${S.hullTop + 24} h90`} stroke="#6b4a2a" strokeWidth={5} strokeLinecap="round" />
        {/* turret */}
        {tw > 0 ? (
          <g>
            <path d={`M${tx} ${S.hullTop} L${tx + 8} ${S.hullTop - th} L${tx + tw - ts} ${S.hullTop - th} Q${tx + tw} ${S.hullTop - th + 4} ${tx + tw + 6} ${S.hullTop - th / 2} L${tx + tw} ${S.hullTop} Z`}
              fill={side} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
            <path d={`M${tx + 10} ${S.hullTop - th + 4} H${tx + tw - ts - 4}`} stroke={top} strokeWidth={8} strokeLinecap="round" opacity={0.8} />
            <rect x={tx + 24} y={S.hullTop - th - 14} width={34} height={14} rx={6} fill={side} stroke={INK} strokeWidth={3} />
            {crew ? (
              <g transform={`translate(${tx + 41} ${S.hullTop - th - 16})`}>
                <rect x={-11} y={-14} width={22} height={18} rx={6} fill="#6b6a4a" stroke={INK} strokeWidth={2.5} />
                <circle cx={0} cy={-26} r={13} fill="#f6dcc4" stroke={INK} strokeWidth={2.5} />
                <path d="M-14 -30 Q0 -46 14 -30 Z" fill="#1b1b1b" stroke={INK} strokeWidth={2} />
              </g>
            ) : null}
            {/* mantlet + barrel */}
            <rect x={tx + tw - 2} y={S.hullTop - th / 2 - 14} width={22} height={28} rx={6} fill={low} stroke={INK} strokeWidth={3} />
            <rect x={tx + tw + 18} y={S.hullTop - th / 2 - 6} width={S.gun} height={12} rx={4} fill={side} stroke={INK} strokeWidth={3} />
            {S.muzzle ? <rect x={tx + tw + 18 + S.gun - 6} y={S.hullTop - th / 2 - 10} width={20} height={20} rx={3} fill={low} stroke={INK} strokeWidth={3} /> : null}
            <g transform={`translate(${tx + tw * 0.45} ${S.hullTop - th * 0.5})`}><Mark nationKey={nationKey} x={0} y={0} s={1.1} /></g>
          </g>
        ) : (
          <g>
            {/* casemate (StuG) */}
            <path d={`M${-60} ${S.hullTop} L${-50} ${S.hullTop - 40} L${80} ${S.hullTop - 40} L${110} ${S.hullTop} Z`} fill={side} stroke={INK} strokeWidth={4} />
            <rect x={108} y={S.hullTop - 26} width={S.gun} height={12} rx={4} fill={side} stroke={INK} strokeWidth={3} />
            <rect x={108 + S.gun - 6} y={S.hullTop - 30} width={20} height={20} rx={3} fill={low} stroke={INK} strokeWidth={3} />
            <g transform={`translate(10 ${S.hullTop - 20})`}><Mark nationKey={nationKey} x={0} y={0} s={1} /></g>
          </g>
        )}
        {S.schurzen ? (
          <g>
            {Array.from({ length: 6 }, (_, i) => <rect key={i} x={-L + i * 58} y={S.hullTop + 34} width={56} height={44} fill={shade(base, -0.1)} stroke={INK} strokeWidth={2.5} />)}
          </g>
        ) : null}
        {damaged ? <path d={`M${tx + 30} ${S.hullTop - th + 10} l18 24 l-10 8 l26 18`} stroke={INK} strokeWidth={4} fill="none" /> : null}
      </g>
      {/* track run with moving links */}
      <rect x={-L - tR} y={tY - tR} width={2 * L + 2 * tR} height={2 * tR} rx={tR} fill="#2c2b27" stroke={INK} strokeWidth={4} />
      <rect x={-L - tR + 5} y={tY - tR + 5} width={2 * L + 2 * tR - 10} height={2 * tR - 10} rx={tR - 5} fill="none" stroke="#4a4842" strokeWidth={5}
        strokeDasharray="8 8" strokeDashoffset={-link} />
      {/* drive sprocket (front) + idler (back) */}
      <g transform={`translate(${L - 6} ${tY - 6}) rotate(${wheelRot})`}>
        <circle r={20} fill="#4a4842" stroke={INK} strokeWidth={3} />
        {Array.from({ length: 8 }, (_, i) => <rect key={i} x={-3} y={-24} width={6} height={8} fill="#4a4842" stroke={INK} strokeWidth={1.5} transform={`rotate(${i * 45})`} />)}
        <circle r={7} fill="#2c2b27" />
      </g>
      <g transform={`translate(${-L + 4} ${tY - 6}) rotate(${wheelRot})`}>
        <circle r={18} fill="#4a4842" stroke={INK} strokeWidth={3} />
        <path d="M-12 0 H12 M0 -12 V12" stroke="#2c2b27" strokeWidth={3} />
      </g>
      {/* road wheels with hubcaps */}
      {S.schurzen ? null : wx.map((x, i) => (
        <g key={i} transform={`translate(${x} ${tY + 4}) rotate(${wheelRot})`}>
          <circle r={S.wheelR} fill="#3d3c36" stroke={INK} strokeWidth={3} />
          <circle r={S.wheelR * 0.6} fill={shade(base, -0.1)} stroke={INK} strokeWidth={2} />
          <circle r={S.wheelR * 0.2} fill={low} />
          <line x1={0} y1={-S.wheelR * 0.6} x2={0} y2={-S.wheelR * 0.25} stroke={INK} strokeWidth={2} />
        </g>
      ))}
      {S.bogies ? [0, 1, 2].map((i) => <rect key={i} x={wx[i * 2] - 6} y={tY - 30} width={wx[i * 2 + 1] - wx[i * 2] + 12} height={14} rx={5} fill={low} stroke={INK} strokeWidth={2.5} />) : null}
      {/* mud on the lower run */}
      <path d={`M${-L - 18} ${tY + 12} Q${-L / 2} ${tY + 2} 0 ${tY + 10} T${L + 18} ${tY + 8}`} stroke="#6b5a40" strokeWidth={6} opacity={0.5} fill="none" />
      {/* exhaust + dust while moving */}
      {moving ? (
        <g>
          {[0, 1, 2].map((i) => {
            const q = ((t * 1.3 + i / 3) % 1);
            return <circle key={'e' + i} cx={hullBack - 10 - q * 90} cy={S.hullTop + 10 - q * 60} r={10 + q * 22} fill="#8a8680" opacity={0.35 * (1 - q)} />;
          })}
          {[0, 1, 2, 3].map((i) => {
            const q = ((t * 1.8 + i / 4) % 1);
            return <ellipse key={'d' + i} cx={-L - 20 - q * 140} cy={-6 - q * 24} rx={18 + q * 40} ry={10 + q * 16} fill="#c8b89a" opacity={0.4 * (1 - q)} />;
          })}
        </g>
      ) : null}
    </g>
  );
};
