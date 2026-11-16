import React from 'react';
import { INK, nation, C } from '../theme';
import { Tank } from './Tanks';
import { Machine, MACHINE_TYPES } from './Machines';

/** Nation marking on a hull. */
export const Mark: React.FC<{ nationKey?: string; x: number; y: number; s?: number }> = ({ nationKey, x, y, s = 1 }) => {
  const m = nation(nationKey).mark;
  const g = (c: React.ReactNode) => <g transform={`translate(${x} ${y}) scale(${s})`}>{c}</g>;
  switch (m) {
    case 'cross':
      return g(<path d="M-4 -14 h8 v10 h10 v8 h-10 v10 h-8 v-10 h-10 v-8 h10 z" fill="#1b1b1b" stroke="#fff" strokeWidth={3} />);
    case 'star':
      return g(<path d="M0 -14 L4 -4.3 L14 -4.3 L6 1.7 L9 11.3 L0 5.3 L-9 11.3 L-6 1.7 L-14 -4.3 L-4 -4.3 Z" fill="#c8352b" stroke="#fff" strokeWidth={1.5} />);
    case 'whitestar':
      return g(<g><circle r={15} fill="#1f3a6b" /><path d="M0 -13 L3.8 -4 L13 -4 L5.6 1.6 L8.4 10.6 L0 5 L-8.4 10.6 L-5.6 1.6 L-13 -4 L-3.8 -4 Z" fill="#fff" /></g>);
    case 'roundel':
      return g(<g><circle r={15} fill="#1f3a6b" /><circle r={10} fill="#fff" /><circle r={5} fill="#c8352b" /></g>);
    case 'sun':
      return g(<circle r={14} fill="#bc002d" stroke="#fff" strokeWidth={3} />);
    default:
      return null;
  }
};

const shadeV = (hex: string) => {
  const n = parseInt(hex.replace('#', ''), 16);
  const f = (v: number) => Math.round(v * 0.8);
  return '#' + ((1 << 24) | (f((n >> 16) & 255) << 16) | (f((n >> 8) & 255) << 8) | f(n & 255)).toString(16).slice(1);
};

/** Vehicles in side view, facing right. Origin = ground contact center. `burning`/`damaged` add states. */
export const Vehicle: React.FC<{ type: string; nationKey?: string; t: number; color?: string; moving?: boolean; damaged?: boolean; prop?: boolean; travel?: number; crew?: boolean }> = ({ type, nationKey, t, color, moving, damaged, travel, crew }) => {
  const n = nation(nationKey);
  const body = color ?? n.uniform;
  const dark = n.uniformDark;
  // wheels turn with the distance travelled (falls back to time when no distance is known)
  const wheelRot = travel !== undefined ? (travel / 22) * (180 / Math.PI) : moving ? t * 360 : 0;
  const Wheel = ({ x, y, r }: { x: number; y: number; r: number }) => (
    <g transform={`translate(${x} ${y}) rotate(${wheelRot})`}>
      <circle r={r} fill="#2a2a2a" stroke={INK} strokeWidth={3} />
      <circle r={r * 0.45} fill="#777" stroke={INK} strokeWidth={2} />
      <line x1={-r * 0.45} x2={r * 0.45} stroke={INK} strokeWidth={2} />
    </g>
  );
  const jig = moving ? Math.sin(t * 30) * 1.2 : 0;
  // volume redraws (Machines.tsx); the old flat drawings stay reachable as '<type>_flat'
  if (MACHINE_TYPES.has(type)) return <Machine type={type} nationKey={nationKey} color={color} t={t} travel={travel ?? (moving ? t * 140 : 0)} moving={!!moving} damaged={damaged} crew={crew} />;
  const ft = type.endsWith('_flat') && type !== 'tank_flat' ? type.slice(0, -5) : type;
  switch (ft) {
    case 'sherman':
    case 'panzer4':
    case 'tiger':
    case 't34':
    case 'panther':
    case 'stug':
    case 'tank': {
      return <Tank type={type} nationKey={nationKey} color={color} travel={travel ?? (moving ? t * 120 : 0)} moving={!!moving} t={t} damaged={damaged} crew={crew} />;
    }
    case 'tank_flat': {
      return (
        <g transform={`translate(0 ${jig})`}>
          <path d="M-170 -20 Q-180 -60 -140 -66 H150 Q180 -60 170 -20 Q150 0 120 0 H-120 Q-150 0 -170 -20 Z" fill="#3a3a36" stroke={INK} strokeWidth={4} />
          {[-120, -70, -20, 30, 80, 128].map((x) => <Wheel key={x} x={x} y={-28} r={20} />)}
          <path d="M-160 -66 L-130 -110 H140 L170 -66 Z" fill={body} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <path d="M-70 -110 L-50 -160 H70 L90 -110 Z" fill={body} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <rect x={86} y={-146} width={170} height={14} rx={4} fill={dark} stroke={INK} strokeWidth={3} />
          <path d="M-150 -76 H160" stroke={dark} strokeWidth={4} />
          <Mark nationKey={nationKey} x={10} y={-134} s={1.2} />
          {damaged ? <path d="M-40 -150 l20 30 l-10 10 l30 20" stroke={INK} strokeWidth={4} fill="none" /> : null}
        </g>
      );
    }
    case 'truck': {
      return (
        <g transform={`translate(0 ${jig})`}>
          <path d="M-200 -50 V-180 H40 V-50 Z" fill={dark} stroke={INK} strokeWidth={4} />
          {[-160, -110, -60, -10].map((x) => <path key={x} d={`M${x} -180 V-50`} stroke={INK} strokeOpacity={0.3} strokeWidth={3} />)}
          <path d="M40 -50 V-150 H130 L170 -100 V-50 Z" fill={body} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <path d="M60 -140 H120 L148 -104 H60 Z" fill="#9fc4d8" stroke={INK} strokeWidth={3} />
          <rect x={-210} y={-56} width={390} height={18} fill="#2a2a2a" stroke={INK} strokeWidth={3} />
          <Wheel x={-140} y={-26} r={26} />
          <Wheel x={-80} y={-26} r={26} />
          <Wheel x={110} y={-26} r={26} />
          <Mark nationKey={nationKey} x={95} y={-80} s={0.9} />
        </g>
      );
    }
    case 'car':
    case 'jeep': {
      return (
        <g transform={`translate(0 ${jig})`}>
          <path d="M-120 -40 V-80 H-40 L-10 -120 H60 L90 -80 H130 V-40 Z" fill={body} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <Wheel x={-70} y={-24} r={24} />
          <Wheel x={80} y={-24} r={24} />
          <Mark nationKey={nationKey} x={0} y={-60} s={0.8} />
        </g>
      );
    }
    case 'artillery':
    case 'gun': {
      return (
        <g>
          <path d="M-20 -60 L180 -120" stroke="#3a3a36" strokeWidth={18} strokeLinecap="round" />
          <path d="M-60 -40 L40 -40 L30 -80 L-40 -80 Z" fill={body} stroke={INK} strokeWidth={4} />
          <path d="M-40 -40 L-160 0 M-20 -40 L-120 0" stroke={dark} strokeWidth={10} strokeLinecap="round" />
          <Wheel x={0} y={-30} r={32} />
        </g>
      );
    }
    case 'train':
    case 'locomotive': {
      return (
        <g transform={`translate(0 ${jig})`}>
          <rect x={-140} y={-170} width={180} height={130} fill="#2f2f33" stroke={INK} strokeWidth={4} />
          <rect x={-120} y={-150} width={60} height={50} fill="#9fc4d8" stroke={INK} strokeWidth={3} />
          <path d="M40 -140 H200 Q230 -120 220 -40 H40 Z" fill="#3a3a40" stroke={INK} strokeWidth={4} />
          <rect x={150} y={-200} width={36} height={60} fill="#2a2a2a" stroke={INK} strokeWidth={3} />
          <path d="M220 -40 L250 -10 H210 Z" fill="#c8352b" stroke={INK} strokeWidth={3} />
          {[-100, -30, 60, 130, 190].map((x) => <Wheel key={x} x={x} y={-24} r={x > 0 && x < 140 ? 30 : 22} />)}
          {moving ? [0, 1, 2].map((i) => {
            const k = ((t * 1.4 + i / 3) % 1);
            return <circle key={i} cx={168 - k * 160} cy={-210 - k * 90} r={18 + k * 40} fill="#e4e4e4" opacity={0.8 - k * 0.8} />;
          }) : null}
        </g>
      );
    }
    case 'wagon':
    case 'traincar': {
      return (
        <g transform={`translate(0 ${jig})`}>
          <rect x={-170} y={-160} width={340} height={120} fill={color ?? '#8a4a32'} stroke={INK} strokeWidth={4} />
          {[-120, -40, 40, 120].map((x) => <path key={x} d={`M${x} -160 V-40`} stroke={INK} strokeOpacity={0.3} strokeWidth={3} />)}
          <Wheel x={-110} y={-24} r={22} />
          <Wheel x={110} y={-24} r={22} />
        </g>
      );
    }
    case 'horse':
    case 'cart': {
      const leg = moving ? Math.sin(t * 9) * 14 : 0;
      return (
        <g>
          {type === 'cart' ? (
            <g>
              <path d="M-260 -60 H-80 V-120 H-260 Z" fill="#8a5a33" stroke={INK} strokeWidth={4} />
              <Wheel x={-170} y={-40} r={40} />
              <path d="M-80 -90 L-10 -100" stroke="#5a3a22" strokeWidth={6} />
            </g>
          ) : null}
          <path d={`M-20 -100 l${-leg} 100 M10 -100 l${leg} 100 M80 -100 l${leg} 100 M110 -100 l${-leg} 100`} stroke="#5a3a26" strokeWidth={12} strokeLinecap="round" />
          <ellipse cx={45} cy={-120} rx={90} ry={44} fill="#8a5a3a" stroke={INK} strokeWidth={4} />
          <path d="M110 -140 L160 -210 L200 -200 L190 -170 L140 -120 Z" fill="#8a5a3a" stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <path d="M150 -205 L130 -150" stroke="#3a2a1a" strokeWidth={10} />
          <circle cx={178} cy={-196} r={4} fill={INK} />
          <path d="M-44 -130 q-30 20 -24 60" stroke="#3a2a1a" strokeWidth={10} fill="none" strokeLinecap="round" />
        </g>
      );
    }
    case 'fighter':
    case 'plane':
    case 'bomber':
    case 'divebomber': {
      const big = type === 'bomber';
      const L = big ? 1.6 : 1;
      const prop = (t * 40) % 2 > 1;
      return (
        <g transform={`scale(${L})`}>
          <path d="M-130 -10 Q-140 -24 -120 -26 L90 -30 Q140 -24 150 -8 Q140 8 90 10 L-110 6 Z" fill={color ?? (nationKey === 'JPN' ? '#d9d4c0' : nationKey === 'USA' ? '#7a8a9a' : body)} stroke={INK} strokeWidth={4} />
          <path d="M-120 -24 L-150 -70 L-118 -70 L-90 -26 Z" fill={color ?? body} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <path d="M-20 -4 L-60 40 L10 40 L30 -4 Z" fill={dark} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <path d="M40 -30 Q60 -56 92 -30 Z" fill="#9fc4d8" stroke={INK} strokeWidth={3} />
          {big ? <path d="M-20 -30 Q0 -50 20 -30 Z M-80 -26 Q-64 -44 -50 -26" fill="#9fc4d8" stroke={INK} strokeWidth={3} /> : null}
          <rect x={150} y={-14} width={10} height={14} fill="#333" />
          <ellipse cx={162} cy={-7} rx={4} ry={prop ? 40 : 10} fill="#555" opacity={prop ? 0.4 : 0.9} />
          <Mark nationKey={nationKey} x={-60} y={-8} s={1} />
        </g>
      );
    }
    case 'carrier': {
      const hull = color ?? '#6b7480';
      const jp = nationKey === 'JPN';
      return (
        <g>
          {/* hull with flare, waterline and hangar openings */}
          <path d="M-560 -44 L600 -44 L540 30 Q500 46 440 48 L-460 48 Q-520 40 -540 10 Z" fill={hull} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
          <path d="M-540 18 L560 18" stroke="#000" strokeOpacity={0.25} strokeWidth={6} />
          <path d="M-520 34 Q0 44 520 34 L470 48 L-460 48 Z" fill="#8a2a24" opacity={0.85} />
          {Array.from({ length: 9 }, (_, i) => <rect key={i} x={-430 + i * 100} y={-32} width={70} height={30} rx={4} fill="#3a4048" stroke={INK} strokeWidth={2.5} />)}
          {Array.from({ length: 22 }, (_, i) => <circle key={i} cx={-470 + i * 46} cy={6} r={4.5} fill="#2a2a2a" />)}
          {/* overhanging flight deck with supports */}
          {Array.from({ length: 12 }, (_, i) => <path key={i} d={`M${-520 + i * 96} -44 L${-500 + i * 96} -62`} stroke={INK} strokeWidth={4} />)}
          <rect x={-600} y={-80} width={1220} height={22} fill="#9a7b52" stroke={INK} strokeWidth={4} />
          <path d="M-590 -69 H610" stroke="#f2efe6" strokeOpacity={0.6} strokeWidth={3} strokeDasharray="34 22" />
          {jp ? <ellipse cx={-380} cy={-72} rx={46} ry={8} fill="#bc002d" /> : <text x={-420} y={-62} fontFamily="sans-serif" fontWeight={900} fontSize={22} fill="#f2efe6" opacity={0.8}>CV</text>}
          {/* parked planes on deck */}
          {[-470, -300, -140, 380, 470].map((x, i) => (
            <g key={i} transform={`translate(${x} -84)`}>
              <path d="M-26 0 L22 0 L30 -8 L-20 -10 Z" fill={jp ? '#c9c4a8' : '#5a7088'} stroke={INK} strokeWidth={2} />
              <path d="M-4 -6 L-14 -18 L8 -18 L6 -6 Z" fill={jp ? '#b9b49a' : '#4a6078'} stroke={INK} strokeWidth={1.5} />
            </g>
          ))}
          {/* island: bridge, mast, funnel */}
          <g transform={jp ? 'translate(-120 0)' : 'translate(0 0)'}>
            <path d="M150 -80 V-170 H290 V-80 Z" fill={hull} stroke={INK} strokeWidth={4} />
            <rect x={160} y={-200} width={120} height={32} fill="#5a636c" stroke={INK} strokeWidth={3} />
            {[0, 1, 2, 3].map((i) => <rect key={i} x={168 + i * 28} y={-194} width={20} height={14} fill="#9fd0e8" stroke={INK} strokeWidth={1.5} />)}
            <path d="M200 -200 V-280 M176 -258 H224 M184 -236 H216" stroke={INK} strokeWidth={5} />
            <path d="M240 -168 L250 -232 H296 L290 -168 Z" fill="#4a535c" stroke={INK} strokeWidth={4} />
            <rect x={248} y={-242} width={50} height={12} fill="#1b1b1b" />
          </g>
          {/* bow wave + wake */}
          <path d={`M560 26 q${30 + Math.sin(t * 3) * 6} 10 ${50} 30 M548 40 q40 4 80 20`} stroke="#fff" strokeWidth={6} strokeLinecap="round" fill="none" opacity={0.8} />
          <path d={`M-470 46 Q-560 ${50 + Math.sin(t * 2) * 4} -680 44`} stroke="#fff" strokeWidth={8} strokeLinecap="round" fill="none" opacity={0.6} />
          {nationKey ? <g transform={jp ? 'translate(80 -280)' : 'translate(200 -280)'}><rect x={0} y={-30} width={46} height={30} fill={jp ? '#fff' : nation(nationKey).flag[0]} stroke={INK} strokeWidth={2} />{jp ? <circle cx={23} cy={-15} r={9} fill="#bc002d" /> : null}</g> : null}
        </g>
      );
    }
    case 'battleship':
    case 'destroyer':
    case 'cruiser': {
      const s = type === 'battleship' ? 1 : type === 'cruiser' ? 0.8 : 0.6;
      return (
        <g transform={`scale(${s})`}>
          <path d="M-480 -40 L500 -40 L440 40 L-450 40 Z" fill={color ?? '#7a828c'} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
          <path d="M-200 -40 V-110 H120 V-40 Z" fill={color ?? '#7a828c'} stroke={INK} strokeWidth={4} />
          <path d="M-60 -110 V-200 H20 V-110 Z" fill="#8a929c" stroke={INK} strokeWidth={4} />
          <rect x={-30} y={-250} width={24} height={50} fill="#5a5a5a" stroke={INK} strokeWidth={3} />
          {[-360, -280, 240, 330].map((x, i) => (
            <g key={x}>
              <rect x={x - 40} y={-80} width={80} height={40} rx={8} fill="#6a727c" stroke={INK} strokeWidth={4} />
              <path d={`M${x} -64 L${x + (i < 2 ? -120 : 120)} -74`} stroke={INK} strokeWidth={8} />
            </g>
          ))}
        </g>
      );
    }
    case 'cargo':
    case 'freighter': {
      return (
        <g>
          <path d="M-420 -60 L420 -60 L380 40 L-390 40 Z" fill={color ?? '#4a5a6a'} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
          <path d="M-420 -60 L420 -60 L414 -40 L-416 -40 Z" fill={C.red} />
          <path d="M160 -60 V-160 H280 V-60 Z" fill="#e9e1cf" stroke={INK} strokeWidth={4} />
          <rect x={200} y={-210} width={40} height={50} fill="#2a2a2a" stroke={INK} strokeWidth={3} />
          {[-300, -180, -60].map((x) => <rect key={x} x={x - 50} y={-120} width={100} height={60} fill={['#b88a52', '#8a4a32', '#4f7a3a'][(x / 120 + 3) % 3 | 0]} stroke={INK} strokeWidth={3} />)}
        </g>
      );
    }
    case 'submarine':
    case 'uboat': {
      return (
        <g>
          <path d="M-360 0 Q-380 -30 -320 -36 L300 -40 Q380 -30 380 0 Q360 24 300 26 L-320 24 Q-370 20 -360 0 Z" fill={color ?? '#5a636c'} stroke={INK} strokeWidth={5} />
          <path d="M-40 -40 L-20 -110 H80 L100 -40 Z" fill={color ?? '#5a636c'} stroke={INK} strokeWidth={4} />
          <path d="M40 -110 V-160" stroke={INK} strokeWidth={5} />
          <path d="M-200 -36 L-170 -60 H-130" stroke={INK} strokeWidth={6} fill="none" />
        </g>
      );
    }
    case 'dakota':
    case 'transport': {
      // C-47 Dakota troop carrier, side view facing right
      const spin = (t * 40) % 2 > 1;
      const skin = color ?? (nationKey === 'UK' ? '#6b7258' : '#6f7552');
      return (
        <g>
          <path d="M-300 -18 Q-310 -40 -270 -44 L180 -50 Q260 -46 300 -20 Q290 6 200 12 L-250 6 Q-296 4 -300 -18 Z" fill={skin} stroke={INK} strokeWidth={5} />
          <path d="M-280 -40 L-320 -120 L-270 -120 L-220 -44 Z" fill={skin} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
          <path d="M-300 -30 L-350 -24 L-300 -14 Z" fill={skin} stroke={INK} strokeWidth={4} />
          <path d="M-60 -6 L-140 60 L60 60 L80 -6 Z" fill={shadeV(skin)} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <path d="M230 -40 Q250 -60 280 -34 Z" fill="#9fc4d8" stroke={INK} strokeWidth={3} />
          {[-180, -130, -80, -30, 20, 70, 120].map((x) => <rect key={x} x={x} y={-36} width={22} height={16} rx={4} fill="#9fc4d8" stroke={INK} strokeWidth={2} />)}
          <rect x={-200} y={-40} width={44} height={42} fill="none" stroke={INK} strokeWidth={3} />
          <path d="M-60 -2 L-60 -36 M80 -2 L80 -36" stroke="#e9e4cf" strokeWidth={9} opacity={0.85} />
          <path d="M-60 -2 L-60 -36 M80 -2 L80 -36" stroke={INK} strokeWidth={9} strokeDasharray="9 9" opacity={0.7} />
          <rect x={0} y={-8} width={50} height={22} rx={8} fill="#4a4e40" stroke={INK} strokeWidth={3} />
          <ellipse cx={52} cy={3} rx={4} ry={spin ? 44 : 12} fill="#555" opacity={spin ? 0.35 : 0.9} />
          <Mark nationKey={nationKey} x={-120} y={-16} s={1.3} />
        </g>
      );
    }
    case 'glider': {
      // Horsa glider (British) / Waco (US): long slab fuselage, high wing, no engine
      const skin = color ?? '#6b7258';
      return (
        <g>
          <path d="M-280 -10 Q-290 -36 -250 -40 L210 -46 Q270 -44 290 -22 Q280 4 200 10 L-240 8 Q-276 8 -280 -10 Z" fill={skin} stroke={INK} strokeWidth={5} />
          <path d="M-260 -36 L-300 -116 L-250 -116 L-210 -40 Z" fill={skin} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
          <path d="M-120 -46 L-160 -58 L120 -62 L140 -48 Z" fill={shadeV(skin)} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <path d="M220 -40 Q246 -58 274 -32 Z" fill="#9fc4d8" stroke={INK} strokeWidth={3} />
          {[-160, -100, -40, 20, 80, 140].map((x) => <circle key={x} cx={x} cy={-22} r={8} fill="#9fc4d8" stroke={INK} strokeWidth={2} />)}
          <path d="M-200 -40 L-200 8 M180 -46 L180 10" stroke={INK} strokeWidth={2} opacity={0.4} />
          <path d="M-30 -20 L-30 6 M70 -20 L70 6" stroke="#e9e4cf" strokeWidth={8} opacity={0.85} />
          <path d="M-30 -20 L-30 6 M70 -20 L70 6" stroke={INK} strokeWidth={8} strokeDasharray="8 8" opacity={0.7} />
          <Mark nationKey={nationKey} x={-150} y={-60} s={1.1} />
          {damaged ? <path d="M200 10 L260 34 L220 30 Z" fill={skin} stroke={INK} strokeWidth={3} /> : null}
        </g>
      );
    }
    case 'halftrack': {
      // armoured half-track / recce vehicle (no insignia beyond the plain cross mark)
      return (
        <g transform={`translate(0 ${jig})`}>
          <path d="M-170 -24 Q-176 -54 -140 -58 H20 V-24 Z" fill="#3a3a36" stroke={INK} strokeWidth={4} />
          {[-140, -100, -60, -20].map((x) => <Wheel key={x} x={x} y={-28} r={18} />)}
          <Wheel x={120} y={-30} r={30} />
          <path d="M-180 -58 L-160 -110 H60 L110 -84 L170 -78 L176 -40 L-180 -40 Z" fill={color ?? body} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <path d="M-150 -96 H40" stroke={dark} strokeWidth={4} />
          <rect x={-40} y={-128} width={14} height={22} fill="#2a2a2a" />
          <path d="M-33 -126 L30 -136" stroke="#2a2a2a" strokeWidth={6} />
          <Mark nationKey={nationKey} x={-60} y={-70} s={1} />
          {damaged ? <path d="M-40 -100 l20 30 l-10 10 l30 20" stroke={INK} strokeWidth={4} fill="none" /> : null}
        </g>
      );
    }
    case 'assaultboat': {
      // flat canvas-and-plywood assault boat seen from the side, paddlers inside
      return (
        <g>
          <path d="M-150 -26 L150 -26 L130 10 L-140 10 Z" fill={color ?? '#6f6a4a'} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <path d="M-150 -26 L150 -26" stroke="#4a4630" strokeWidth={6} />
          {[-100, -40, 20, 80].map((x, i) => (
            <g key={x}>
              <circle cx={x} cy={-50} r={16} fill="#6b7a4a" stroke={INK} strokeWidth={3} />
              <rect x={x - 14} y={-44} width={28} height={20} rx={6} fill="#6f7552" stroke={INK} strokeWidth={3} />
              <path d={`M${x + 6} -34 L${x + 30 + Math.sin(t * 6 + i) * 14} ${16 + Math.cos(t * 6 + i) * 6}`} stroke="#8a5a33" strokeWidth={5} strokeLinecap="round" />
            </g>
          ))}
        </g>
      );
    }
    case 'boat': {
      return (
        <g>
          <path d="M-120 -20 L120 -20 L90 20 L-100 20 Z" fill={color ?? '#8a5a33'} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <path d="M0 -20 V-140 L70 -40 Z" fill="#f4ecd8" stroke={INK} strokeWidth={3} />
        </g>
      );
    }
    default:
      return <rect x={-60} y={-60} width={120} height={60} fill={body} stroke={INK} strokeWidth={3} />;
  }
};
