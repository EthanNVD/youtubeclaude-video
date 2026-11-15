import React from 'react';
import { C, INK, FONT, nation, PAPER } from '../theme';
import { clamp, rnd } from '../lib/anim';

/** Flag (waving unless still). Origin = top-left of the cloth. */
export const Flag: React.FC<{ nation: string; w?: number; h?: number; t: number; still?: boolean }> = ({ nation: k, w = 160, h = 106, t, still }) => {
  const n = nation(k);
  const id = 'fl' + k + Math.round(w);
  const wave = still ? 0 : 6;
  const d = `M0 0 Q${w / 4} ${-wave * Math.sin(t * 3)} ${w / 2} 0 T${w} 0 V${h} Q${(3 * w) / 4} ${h + wave * Math.sin(t * 3 + 1)} ${w / 2} ${h} T0 ${h} Z`;
  const f = n.flag;
  let inner: React.ReactNode;
  switch (n.flagKind) {
    case 'h3':
      inner = f.map((c, i) => <rect key={i} x={0} y={(h / 3) * i} width={w} height={h / 3 + 1} fill={c} />);
      break;
    case 'h2':
      inner = f.map((c, i) => <rect key={i} x={0} y={(h / 2) * i} width={w} height={h / 2 + 1} fill={c} />);
      break;
    case 'v3':
      inner = f.map((c, i) => <rect key={i} x={(w / 3) * i} y={0} width={w / 3 + 1} height={h} fill={c} />);
      break;
    case 'sun':
      inner = (
        <>
          <rect width={w} height={h} fill="#fff" />
          <circle cx={w / 2} cy={h / 2} r={h * 0.3} fill={f[1]} />
        </>
      );
      break;
    case 'star':
      inner = (
        <>
          <rect width={w} height={h} fill={f[0]} />
          <path transform={`translate(${k.toUpperCase() === 'VN' ? w / 2 : w * 0.18} ${h * (k.toUpperCase() === 'VN' ? 0.5 : 0.24)}) scale(${h / (k.toUpperCase() === 'VN' ? 40 : 110)})`} d="M0 -10 L2.9 -3.1 L10 -3.1 L4.3 1.2 L6.5 8.1 L0 3.8 L-6.5 8.1 L-4.3 1.2 L-10 -3.1 L-2.9 -3.1 Z" fill="#f2c230" />
          {k.toUpperCase() !== 'VN' ? <path d={`M${w * 0.12} ${h * 0.42} q${w * 0.05} ${h * 0.12} ${w * 0.12} ${h * 0.02}`} stroke="#f2c230" strokeWidth={h * 0.04} fill="none" /> : null}
        </>
      );
      break;
    case 'us':
      inner = (
        <>
          {Array.from({ length: 7 }, (_, i) => <rect key={i} x={0} y={(h / 6.5) * i} width={w} height={h / 13} fill="#b22234" />)}
          <rect width={w} height={h} fill="#fff" opacity={0} />
          {Array.from({ length: 6 }, (_, i) => <rect key={'w' + i} x={0} y={(h / 6.5) * i + h / 13} width={w} height={h / 13} fill="#fff" />)}
          <rect width={w * 0.42} height={h * 0.54} fill="#3c3b6e" />
          {Array.from({ length: 12 }, (_, i) => <circle key={'s' + i} cx={w * 0.05 + (i % 4) * w * 0.1} cy={h * 0.09 + Math.floor(i / 4) * h * 0.17} r={h * 0.025} fill="#fff" />)}
        </>
      );
      break;
    case 'uk':
      inner = (
        <>
          <rect width={w} height={h} fill="#012169" />
          <path d={`M0 0 L${w} ${h} M${w} 0 L0 ${h}`} stroke="#fff" strokeWidth={h * 0.2} />
          <path d={`M0 0 L${w} ${h} M${w} 0 L0 ${h}`} stroke="#c8102e" strokeWidth={h * 0.07} />
          <path d={`M${w / 2} 0 V${h} M0 ${h / 2} H${w}`} stroke="#fff" strokeWidth={h * 0.32} />
          <path d={`M${w / 2} 0 V${h} M0 ${h / 2} H${w}`} stroke="#c8102e" strokeWidth={h * 0.18} />
        </>
      );
      break;
    case 'cross':
      inner = (
        <>
          <rect width={w} height={h} fill={f[0]} />
          <path d={`M${w * 0.36} 0 V${h} M0 ${h / 2} H${w}`} stroke={f[1]} strokeWidth={h * 0.26} />
        </>
      );
      break;
    default:
      inner = <rect width={w} height={h} fill={f[0]} />;
  }
  return (
    <g>
      <defs>
        <clipPath id={id}>
          <path d={d} />
        </clipPath>
      </defs>
      <g clipPath={`url(#${id})`}>{inner}</g>
      {!still ? <path d={d} fill="url(#flagshade)" opacity={0.25} /> : null}
      <path d={d} fill="none" stroke={INK} strokeWidth={3} />
    </g>
  );
};

const Paper: React.FC<{ w: number; h: number; c?: string; lines?: number }> = ({ w, h, c = PAPER, lines = 5 }) => (
  <g>
    <rect x={-w / 2 + 6} y={-h / 2 + 6} width={w} height={h} fill="#000" opacity={0.15} />
    <rect x={-w / 2} y={-h / 2} width={w} height={h} fill={c} stroke={INK} strokeWidth={3} />
    {Array.from({ length: lines }, (_, i) => <line key={i} x1={-w / 2 + 14} x2={w / 2 - 14 - (i === lines - 1 ? w * 0.3 : 0)} y1={-h / 2 + 24 + i * ((h - 40) / lines)} y2={-h / 2 + 24 + i * ((h - 40) / lines)} stroke="#8a8070" strokeWidth={3} />)}
  </g>
);

/** Generic prop library. Origin is roughly the prop's center (or base for standing objects). */
export const Prop: React.FC<{ item: string; t: number; color?: string; text?: string; value?: number; nationKey?: string; on?: boolean }> = ({ item, t, color, text, value, nationKey, on }) => {
  switch (item) {
    case 'paper':
      return <Paper w={110} h={140} />;
    case 'telegram':
      return (
        <g>
          <Paper w={200} h={130} c="#efe2b0" lines={4} />
          <text x={-86} y={-44} fontFamily={FONT.mono} fontSize={16} fontWeight={600} fill={INK}>{text ?? 'TELEGRAM'}</text>
        </g>
      );
    case 'folder':
      return (
        <g>
          <path d="M-120 -80 h80 l14 14 h146 v146 h-240 z" fill={color ?? '#c9a96a'} stroke={INK} strokeWidth={4} />
          <text x={0} y={10} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={26} fill={INK}>{text ?? 'TOP SECRET'}</text>
          <rect x={-90} y={30} width={180} height={4} fill={INK} opacity={0.4} />
        </g>
      );
    case 'book':
      return (
        <g>
          <rect x={-70} y={-95} width={140} height={190} rx={6} fill={color ?? '#7a2a2a'} stroke={INK} strokeWidth={4} />
          <rect x={-58} y={-95} width={10} height={190} fill="#000" opacity={0.2} />
          <text x={6} y={-30} textAnchor="middle" fontFamily={FONT.serif} fontWeight={900} fontSize={20} fill="#f0d98a">{text ?? ''}</text>
        </g>
      );
    case 'phone':
      return (
        <g>
          <rect x={-40} y={-10} width={80} height={44} rx={8} fill="#1d1d1d" stroke={INK} strokeWidth={3} />
          <circle cx={0} cy={12} r={14} fill="#eee" stroke={INK} strokeWidth={2} />
          <path d="M-46 -18 q0 -26 46 -26 q46 0 46 26 l-14 6 l-8 -10 h-48 l-8 10 z" fill="#1d1d1d" stroke={INK} strokeWidth={3} />
          {on ? <g stroke={C.red} strokeWidth={4} strokeLinecap="round">{[0, 1, 2].map((i) => <path key={i} d={`M${54 + i * 10} -40 l10 -10`} opacity={(Math.sin(t * 20 + i) + 1) / 2} />)}</g> : null}
        </g>
      );
    case 'radio':
      return (
        <g>
          <rect x={-90} y={-60} width={180} height={110} rx={10} fill="#6b4428" stroke={INK} strokeWidth={4} />
          <circle cx={-40} cy={-5} r={34} fill="#d9c49a" stroke={INK} strokeWidth={3} />
          {Array.from({ length: 5 }, (_, i) => <line key={i} x1={-66} x2={-14} y1={-25 + i * 10} y2={-25 + i * 10} stroke="#8a6a4a" strokeWidth={2} />)}
          <rect x={20} y={-30} width={54} height={24} fill="#f2e6b0" stroke={INK} strokeWidth={2} />
          <circle cx={30} cy={22} r={9} fill="#2a2a2a" />
          <circle cx={62} cy={22} r={9} fill="#2a2a2a" />
          {on ? <path d="M90 -60 q20 20 0 40 M104 -70 q30 30 0 60" stroke={INK} strokeWidth={3} fill="none" opacity={0.5 + 0.5 * Math.sin(t * 8)} /> : null}
        </g>
      );
    case 'stopwatch': {
      const a = ((value ?? t * 6) % 60) * 6;
      return (
        <g>
          <rect x={-12} y={-112} width={24} height={20} fill="#c9a24a" stroke={INK} strokeWidth={3} />
          <circle cy={-118} r={10} fill="none" stroke="#c9a24a" strokeWidth={6} />
          <circle r={92} fill="#c9a24a" stroke={INK} strokeWidth={5} />
          <circle r={78} fill="#fbf8f0" stroke={INK} strokeWidth={3} />
          {Array.from({ length: 12 }, (_, i) => <line key={i} y1={-70} y2={-58} stroke={INK} strokeWidth={4} transform={`rotate(${i * 30})`} />)}
          <line y2={-66} stroke={C.red} strokeWidth={4} strokeLinecap="round" transform={`rotate(${a})`} />
          <circle r={6} fill={INK} />
        </g>
      );
    }
    case 'clock':
      return (
        <g>
          <circle r={70} fill="#fbf8f0" stroke={INK} strokeWidth={6} />
          {Array.from({ length: 12 }, (_, i) => <line key={i} y1={-60} y2={-50} stroke={INK} strokeWidth={4} transform={`rotate(${i * 30})`} />)}
          <line y2={-34} stroke={INK} strokeWidth={6} strokeLinecap="round" transform={`rotate(${(value ?? 0) * 30})`} />
          <line y2={-54} stroke={INK} strokeWidth={4} strokeLinecap="round" transform={`rotate(${((value ?? 0) % 1) * 360 + t * 6})`} />
        </g>
      );
    case 'candle': {
      const fl = 1 + Math.sin(t * 13) * 0.08 + Math.sin(t * 7.3) * 0.05;
      return (
        <g>
          <ellipse cx={0} cy={-150} rx={120} ry={120} fill="#ffcf6a" opacity={0.12} />
          <rect x={-22} y={-120} width={44} height={120} fill="#f2ead4" stroke={INK} strokeWidth={3} />
          <line x1={0} y1={-120} x2={0} y2={-132} stroke={INK} strokeWidth={3} />
          <path transform={`translate(0 -132) scale(1 ${fl})`} d="M0 -46 Q16 -16 8 -4 Q0 4 -8 -4 Q-16 -16 0 -46 Z" fill="#ffb43a" />
          <path transform={`translate(0 -132) scale(1 ${fl})`} d="M0 -28 Q7 -10 3 -4 Q0 0 -3 -4 Q-7 -10 0 -28 Z" fill="#fff3b0" />
        </g>
      );
    }
    case 'helmet':
      return (
        <g>
          <path d="M-80 10 C-80 -80 80 -80 80 10 Z" fill={color ?? nation(nationKey).uniform} stroke={INK} strokeWidth={4} />
          <path d="M-90 10 Q0 30 90 10" stroke={INK} strokeWidth={8} fill="none" strokeLinecap="round" />
        </g>
      );
    case 'crate':
      return (
        <g>
          <rect x={-60} y={-90} width={120} height={90} fill="#b88a52" stroke={INK} strokeWidth={4} />
          <path d="M-60 -90 L60 0 M60 -90 L-60 0" stroke="#8a6232" strokeWidth={6} />
          {text ? <text x={0} y={-38} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={20} fill={INK}>{text}</text> : null}
        </g>
      );
    case 'barrel':
      return (
        <g>
          <rect x={-40} y={-110} width={80} height={110} rx={10} fill={color ?? '#3a3a3a'} stroke={INK} strokeWidth={4} />
          <path d="M-40 -80 h80 M-40 -30 h80" stroke="#000" opacity={0.35} strokeWidth={6} />
          {text ? <text x={0} y={-50} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={22} fill="#f2c230">{text}</text> : null}
        </g>
      );
    case 'bomb':
      return (
        <g>
          <ellipse cx={0} cy={0} rx={70} ry={26} fill="#4a4f45" stroke={INK} strokeWidth={4} />
          <path d="M60 0 l40 -22 v44 z" fill="#4a4f45" stroke={INK} strokeWidth={4} />
          <path d="M-20 -24 v48" stroke="#c8352b" strokeWidth={6} />
        </g>
      );
    case 'shell':
      return (
        <g>
          <path d="M-16 0 V-80 Q0 -120 16 -80 V0 Z" fill="#c9a24a" stroke={INK} strokeWidth={3} />
          <rect x={-18} y={-10} width={36} height={12} fill="#a8822a" stroke={INK} strokeWidth={3} />
        </g>
      );
    case 'binoculars':
      return (
        <g fill="#2a2a2a" stroke={INK} strokeWidth={3}>
          <rect x={-40} y={-24} width={32} height={48} rx={8} />
          <rect x={8} y={-24} width={32} height={48} rx={8} />
          <rect x={-10} y={-10} width={20} height={14} />
        </g>
      );
    case 'globe':
      return (
        <g>
          <path d="M0 110 V150 M-50 150 H50" stroke="#7a5a3a" strokeWidth={10} />
          <circle r={110} fill="#8fc0dc" stroke={INK} strokeWidth={5} />
          <path d="M-70 -50 q40 -30 80 0 q20 40 -20 70 q-40 10 -60 -20 z M30 20 q40 -10 60 30 q-20 40 -50 30 z" fill="#c9b47a" stroke="#7a6a4a" strokeWidth={3} />
          <path d="M0 -110 A110 110 0 0 1 0 110" fill="none" stroke="#6a5a3a" strokeWidth={6} transform="rotate(20)" />
        </g>
      );
    case 'hourglass': {
      const k = clamp(value ?? (t % 10) / 10);
      return (
        <g>
          <rect x={-70} y={-130} width={140} height={16} fill={C.wood} stroke={INK} strokeWidth={3} />
          <rect x={-70} y={114} width={140} height={16} fill={C.wood} stroke={INK} strokeWidth={3} />
          <path d="M-50 -114 H50 Q50 -40 6 0 Q50 40 50 114 H-50 Q-50 40 -6 0 Q-50 -40 -50 -114 Z" fill="#e8f4fa" fillOpacity={0.5} stroke={INK} strokeWidth={4} />
          <path d={`M${-44 * (1 - k)} ${-100 + 90 * k} H${44 * (1 - k)} L6 -4 H-6 Z`} fill="#e3c070" />
          <path d={`M-46 110 H46 Q${40 - 30 * (1 - k)} ${110 - 90 * k} 0 ${110 - 100 * k} Q${-40 + 30 * (1 - k)} ${110 - 90 * k} -46 110 Z`} fill="#e3c070" />
        </g>
      );
    }
    case 'medal':
      return (
        <g>
          <path d="M-20 -80 L0 -30 L20 -80 Z" fill="#c8352b" stroke={INK} strokeWidth={3} />
          <circle cy={0} r={36} fill="#e3b94a" stroke={INK} strokeWidth={4} />
          <circle cy={0} r={24} fill="none" stroke="#a8822a" strokeWidth={3} />
        </g>
      );
    case 'cigar':
      return <rect x={-50} y={-8} width={100} height={16} rx={8} fill="#7a4a28" stroke={INK} strokeWidth={3} />;
    case 'typewriter':
      return (
        <g>
          <rect x={-120} y={-40} width={240} height={80} rx={14} fill="#2a2a2a" stroke={INK} strokeWidth={4} />
          <rect x={-100} y={-100} width={200} height={70} fill={PAPER} stroke={INK} strokeWidth={3} />
          {Array.from({ length: 18 }, (_, i) => <circle key={i} cx={-90 + (i % 9) * 22} cy={4 + Math.floor(i / 9) * 20} r={7} fill="#ddd" stroke={INK} strokeWidth={2} />)}
        </g>
      );
    case 'microphone':
      return (
        <g>
          <line x1={0} y1={0} x2={0} y2={-180} stroke="#555" strokeWidth={8} />
          <rect x={-22} y={-240} width={44} height={70} rx={20} fill="#8a8a8a" stroke={INK} strokeWidth={4} />
          <path d="M-60 0 h120" stroke="#555" strokeWidth={10} />
        </g>
      );
    case 'sign':
    case 'exit':
      return (
        <g>
          <line x1={0} y1={0} x2={0} y2={-150} stroke="#6a5a4a" strokeWidth={10} />
          <rect x={-110} y={-220} width={220} height={74} rx={8} fill={item === 'exit' ? '#2f7a3a' : color ?? '#e9dfc4'} stroke={INK} strokeWidth={4} />
          <text x={0} y={-172} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={item === 'exit' ? 26 : 30} fill={item === 'exit' ? '#fff' : INK}>{text ?? 'EXIT'}</text>
        </g>
      );
    case 'flag':
      return (
        <g>
          <line x1={0} y1={0} x2={0} y2={-260} stroke="#7a5a3a" strokeWidth={8} />
          <g transform="translate(4 -256)"><Flag nation={nationKey ?? 'NEUTRAL'} w={150} h={100} t={t} /></g>
        </g>
      );
    case 'ledger': {
      return (
        <g>
          <path d="M-260 -150 Q-130 -175 0 -150 Q130 -175 260 -150 V160 Q130 135 0 160 Q-130 135 -260 160 Z" fill="#f4ecd8" stroke={INK} strokeWidth={5} />
          <line x1={0} y1={-150} x2={0} y2={160} stroke="#b9a98a" strokeWidth={4} />
          {Array.from({ length: 9 }, (_, i) => <line key={i} x1={-240} x2={240} y1={-110 + i * 30} y2={-110 + i * 30} stroke="#c9d6e0" strokeWidth={2} />)}
        </g>
      );
    }
    case 'coins':
      return (
        <g>
          {Array.from({ length: Math.round(value ?? 5) }, (_, i) => <ellipse key={i} cx={0} cy={-i * 10} rx={40} ry={12} fill="#e3b94a" stroke={INK} strokeWidth={3} />)}
        </g>
      );
    case 'oil':
      return (
        <g>
          <path d="M-50 0 L0 -220 L50 0 M-30 -80 h60 M-40 -40 h80 M-20 -140 h40" stroke="#3a3a3a" strokeWidth={8} fill="none" strokeLinejoin="round" />
          <rect x={-60} y={-10} width={120} height={20} fill="#3a3a3a" />
        </g>
      );
    case 'factory':
      return (
        <g>
          <path d="M-120 0 V-90 L-80 -120 V-90 L-40 -120 V-90 L0 -120 V-90 H40 V-200 H70 V-90 H120 V0 Z" fill={color ?? '#9a6a52'} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          {[-90, -50, -10].map((x) => <rect key={x} x={x} y={-60} width={24} height={24} fill="#f2d77a" stroke={INK} strokeWidth={2} />)}
          <circle cx={56 + Math.sin(t) * 6} cy={-230 - ((t * 30) % 40)} r={14 + ((t * 30) % 40) / 4} fill="#aaa" opacity={0.6 - ((t * 30) % 40) / 80} />
        </g>
      );
    case 'chair':
      return (
        <g fill={C.wood} stroke={INK} strokeWidth={4}>
          <rect x={-50} y={-210} width={100} height={130} rx={10} />
          <rect x={-60} y={-90} width={120} height={20} />
          <path d="M-50 -70 V0 M50 -70 V0" />
        </g>
      );
    case 'table':
      return (
        <g fill={C.woodLight} stroke={INK} strokeWidth={4}>
          <rect x={-200} y={-120} width={400} height={24} />
          <path d="M-180 -96 V0 M180 -96 V0" strokeWidth={14} />
        </g>
      );
    case 'pen':
      return <path d="M0 0 L-12 -90 L-4 -96 L8 -2 Z" fill="#2a2a2a" stroke={INK} strokeWidth={2} />;
    case 'skull':
      return (
        <g>
          <circle cy={-40} r={44} fill="#f0ead8" stroke={INK} strokeWidth={4} />
          <rect x={-24} y={-10} width={48} height={24} rx={6} fill="#f0ead8" stroke={INK} strokeWidth={4} />
          <circle cx={-16} cy={-42} r={11} fill={INK} />
          <circle cx={16} cy={-42} r={11} fill={INK} />
        </g>
      );
    case 'cross':
    case 'grave':
      return (
        <g>
          <path d="M-8 0 V-120 M-40 -90 H24" stroke="#f0ead8" strokeWidth={14} strokeLinecap="round" />
          <path d="M-8 0 V-120 M-40 -90 H24" stroke={INK} strokeWidth={3} fill="none" strokeOpacity={0.3} />
        </g>
      );
    case 'rifle':
      return (
        <g>
          <path d="M-110 0 L60 -8 L70 4 L-20 10 L-60 30 L-110 20 Z" fill="#6b4a32" stroke={INK} strokeWidth={3} />
          <path d="M40 -6 L150 -10" stroke="#2a2a2a" strokeWidth={8} />
        </g>
      );
    default:
      return (
        <g>
          <rect x={-40} y={-40} width={80} height={80} fill={color ?? '#ccc'} stroke={INK} strokeWidth={3} />
          <text textAnchor="middle" y={6} fontSize={16} fontFamily={FONT.cond}>{item}</text>
        </g>
      );
  }
};

export const randomSeed = rnd;
