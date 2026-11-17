import React from 'react';
import { rnd, clamp } from '../lib/anim';
import { INK } from '../theme';

/** Effects. Time `a` = seconds since the effect started (element in-time). Origin = source point. */
export const Fx: React.FC<{ kind: string; a: number; t: number; seed: string; size?: number; dir?: number; color?: string; w?: number; h?: number; count?: number }> = ({ kind, a, t, seed, size = 1, dir = -90, color, w = 2000, h = 1200, count }) => {
  switch (kind) {
    case 'smoke': {
      // rising column of puffs, continuous
      const n = count ?? 14;
      return (
        <g transform={`scale(${size})`}>
          {Array.from({ length: n }, (_, i) => {
            const life = 4;
            const k = ((t + (i * life) / n) % life) / life;
            const x = Math.sin(k * 3 + rnd(seed, i) * 6) * 20 + k * 120 * Math.cos((dir * Math.PI) / 180 + Math.PI / 2) * 0 + k * 60;
            const y = -k * 380;
            const r = 26 + k * 70;
            return <circle key={i} cx={x} cy={y} r={r} fill={color ?? (k < 0.15 ? '#3a3632' : '#55504a')} opacity={(1 - k) * 0.75} />;
          })}
        </g>
      );
    }
    case 'fire': {
      const fl = (i: number) => 1 + Math.sin(t * 14 + i * 2) * 0.12 + Math.sin(t * 9.3 + i) * 0.08;
      return (
        <g transform={`scale(${size})`}>
          <ellipse cx={0} cy={-30} rx={140} ry={90} fill="#ff9a3a" opacity={0.18} />
          {[-40, 0, 40].map((x, i) => (
            <g key={i} transform={`translate(${x} 0) scale(${fl(i)} ${fl(i + 3)})`}>
              <path d="M0 -130 Q40 -60 30 -20 Q20 10 0 10 Q-20 10 -30 -20 Q-40 -60 0 -130 Z" fill="#e8552a" />
              <path d="M0 -90 Q22 -44 16 -16 Q10 4 0 4 Q-10 4 -16 -16 Q-22 -44 0 -90 Z" fill="#ffb43a" />
              <path d="M0 -50 Q10 -26 7 -10 Q4 0 0 0 Q-4 0 -7 -10 Q-10 -26 0 -50 Z" fill="#fff0a0" />
            </g>
          ))}
        </g>
      );
    }
    case 'shellburst': {
      // WW1 shell landing in soft ground: a flash, then a tall column of earth that rises, spreads and falls back
      if (a < 0 || a > 2.6) return null;
      const up = clamp(a / 0.45);
      const fall = clamp((a - 0.6) / 1.6);
      const hgt = 420 * (1 - Math.pow(1 - up, 3)) * (1 - fall * 0.55);
      return (
        <g transform={`scale(${size})`}>
          {a < 0.1 ? <circle r={200} fill="#fff4c0" opacity={1 - a / 0.1} /> : null}
          {a < 0.3 ? <ellipse cy={-20} rx={120} ry={70} fill="#ffb347" opacity={1 - a / 0.3} /> : null}
          <path d={`M-70 0 Q-60 ${-hgt * 0.6} ${-110 - fall * 60} ${-hgt} Q0 ${-hgt - 60} ${110 + fall * 60} ${-hgt} Q60 ${-hgt * 0.6} 70 0 Z`} fill="#4a3a2c" opacity={clamp(1 - fall)} />
          {Array.from({ length: 14 }, (_, i) => {
            const ang = -Math.PI / 2 + (rnd(seed, i) - 0.5) * 1.6;
            const v = 500 + rnd(seed, i, 'v') * 400;
            const x = Math.cos(ang) * v * a;
            const y = Math.sin(ang) * v * a + 900 * a * a;
            return y < 20 ? <circle key={i} cx={x} cy={y} r={8 + rnd(seed, i, 'r') * 14} fill="#3a2e24" /> : null;
          })}
          <g opacity={clamp(a / 0.4) * clamp(1 - (a - 0.8) / 1.8) * 0.7}>
            {Array.from({ length: 6 }, (_, i) => (
              <circle key={'s' + i} cx={(rnd(seed, i, 'sx') - 0.5) * 220 + a * 30} cy={-hgt * 0.7 - a * 60 - i * 20} r={(50 + i * 12) * (0.4 + a * 0.5)} fill="#5e554c" />
            ))}
          </g>
        </g>
      );
    }
    case 'explosion':
    case 'impact': {
      if (a < 0 || a > 2.2) return null;
      const k = clamp(a / 0.35);
      const fade = clamp(1 - (a - 0.3) / 1.6);
      return (
        <g transform={`scale(${size})`}>
          {a < 0.12 ? <circle r={260} fill="#fff8d0" opacity={1 - a / 0.12} /> : null}
          <circle r={40 + k * 140} fill="#ffcf5a" opacity={(1 - k) * 0.9} />
          {Array.from({ length: 12 }, (_, i) => {
            const ang = rnd(seed, i) * Math.PI * 2;
            const d = (30 + rnd(seed, i, 'd') * 120) * clamp(a / 0.5);
            const r = (40 + rnd(seed, i, 'r') * 50) * (0.6 + clamp(a / 0.6) * 0.6);
            return <circle key={i} cx={Math.cos(ang) * d} cy={Math.sin(ang) * d * 0.7 - a * 60} r={r} fill={a < 0.4 ? '#f08a3a' : '#4a4540'} opacity={fade * 0.85} />;
          })}
          {Array.from({ length: 10 }, (_, i) => {
            const ang = rnd(seed, i, 'a') * Math.PI * 2;
            const d = 300 * clamp(a / 0.8);
            return <rect key={'d' + i} x={Math.cos(ang) * d} y={Math.sin(ang) * d - 0} width={10} height={10} fill={INK} opacity={clamp(1 - a)} transform={`rotate(${a * 300 + i * 40} ${Math.cos(ang) * d} ${Math.sin(ang) * d})`} />;
          })}
        </g>
      );
    }
    case 'muzzle':
    case 'flash': {
      const period = 0.5 + rnd(seed) * 0.4;
      const ph = (a + rnd(seed, 'p') * period) % period;
      if (ph > 0.08) return null;
      return (
        <g transform={`rotate(${dir + 90}) scale(${size})`}>
          <path d="M0 0 L60 -14 L110 0 L60 14 Z" fill="#ffe28a" />
          <circle r={26} fill="#fff6c8" />
        </g>
      );
    }
    case 'tracer': {
      const period = 0.35;
      return (
        <g transform={`rotate(${dir})`}>
          {Array.from({ length: 4 }, (_, i) => {
            const k = ((a + i * period) % (period * 4)) / (period * 4);
            return <line key={i} x1={k * 1200} x2={k * 1200 + 60} y1={0} y2={0} stroke="#ffd36a" strokeWidth={4} opacity={0.9} />;
          })}
        </g>
      );
    }
    case 'searchlight': {
      const ang = Math.sin(t * 0.5 + rnd(seed) * 6) * 25 + dir + 90;
      return (
        <g transform={`rotate(${ang}) scale(${size})`}>
          <path d="M0 0 L-70 -1100 L70 -1100 Z" fill="#fff8d0" opacity={0.22} />
          <circle r={12} fill="#fff8d0" />
        </g>
      );
    }
    case 'rain':
    case 'snow': {
      const n = count ?? (kind === 'rain' ? 140 : 110);
      return (
        <g>
          {Array.from({ length: n }, (_, i) => {
            const sp = kind === 'rain' ? 900 : 70 + rnd(seed, i, 's') * 60;
            const x0 = rnd(seed, i) * w - w / 2;
            const y = (((rnd(seed, i, 'y') * h + t * sp) % h) + h) % h - h / 2;
            const x = x0 + (kind === 'rain' ? y * 0.25 : Math.sin(t + i) * 20);
            return kind === 'rain'
              ? <line key={i} x1={x} y1={y} x2={x + 8} y2={y + 34} stroke="#cfe2ef" strokeWidth={2.5} opacity={0.6} />
              : <circle key={i} cx={x} cy={y} r={2 + rnd(seed, i, 'r') * 4} fill="#fff" opacity={0.85} />;
          })}
        </g>
      );
    }
    case 'sparks': {
      return (
        <g>
          {Array.from({ length: 16 }, (_, i) => {
            const life = 0.7;
            const k = ((t + (i * life) / 16) % life) / life;
            const ang = -Math.PI / 2 + (rnd(seed, i) - 0.5) * 2.4;
            return <circle key={i} cx={Math.cos(ang) * k * 160} cy={Math.sin(ang) * k * 160 + k * k * 120} r={3.5 * (1 - k) + 1} fill={k < 0.4 ? '#fff6c8' : '#ffb43a'} />;
          })}
          <circle r={18 + Math.sin(t * 40) * 4} fill="#d8f0ff" opacity={0.85} />
        </g>
      );
    }
    case 'dust': {
      return (
        <g transform={`scale(${size})`}>
          {Array.from({ length: 8 }, (_, i) => {
            const k = ((t * 0.8 + i / 8) % 1);
            return <circle key={i} cx={-k * 220 - rnd(seed, i) * 40} cy={-k * 40} r={20 + k * 40} fill={color ?? '#c9b48a'} opacity={(1 - k) * 0.5} />;
          })}
        </g>
      );
    }
    case 'splash': {
      if (a < 0 || a > 1.8) return null;
      const k = clamp(a / 1.2);
      return (
        <g transform={`scale(${size})`}>
          <path d={`M-60 0 Q-40 ${-260 * Math.sin(k * Math.PI)} 0 ${-300 * Math.sin(k * Math.PI)} Q40 ${-260 * Math.sin(k * Math.PI)} 60 0 Z`} fill="#e8f4fa" opacity={1 - k * 0.7} stroke="#9fc4d8" strokeWidth={4} />
        </g>
      );
    }
    case 'wake': {
      return (
        <g>
          {Array.from({ length: 6 }, (_, i) => {
            const k = ((t * 0.6 + i / 6) % 1);
            return <path key={i} d={`M${-k * 600} ${-k * 30} q-60 ${10 + k * 20} -120 ${0}`} stroke="#fff" strokeWidth={6 - k * 4} opacity={1 - k} fill="none" />;
          })}
        </g>
      );
    }
    case 'fireworks': {
      return (
        <g>
          {Array.from({ length: 5 }, (_, j) => {
            const life = 2.2;
            const k = ((t + j * 0.47) % life) / life;
            const cx = (rnd(seed, j) - 0.5) * 1400, cy = -200 - rnd(seed, j, 'y') * 300;
            return (
              <g key={j}>
                {Array.from({ length: 14 }, (_, i) => {
                  const ang = (i / 14) * Math.PI * 2;
                  return <circle key={i} cx={cx + Math.cos(ang) * k * 160} cy={cy + Math.sin(ang) * k * 160 + k * k * 60} r={5} fill={['#ffd36a', '#ff7a6a', '#9ad8ff'][j % 3]} opacity={1 - k} />;
                })}
              </g>
            );
          })}
        </g>
      );
    }
    case 'speedlines': {
      return (
        <g>
          {Array.from({ length: 24 }, (_, i) => {
            const y = (rnd(seed, i) - 0.5) * h;
            const x = ((rnd(seed, i, 'x') * w - t * 2400) % w + w) % w - w / 2;
            return <line key={i} x1={x} x2={x + 200} y1={y} y2={y} stroke="#fff" strokeWidth={3} opacity={0.5} />;
          })}
        </g>
      );
    }
    case 'question':
    case 'exclaim': {
      const s = 1 + Math.sin(t * 6) * 0.06;
      return <text transform={`scale(${s * size})`} textAnchor="middle" fontSize={120} fontWeight={900} fontFamily="Arial Black, sans-serif" fill={color ?? '#c8352b'} stroke={INK} strokeWidth={5} paintOrder="stroke">{kind === 'question' ? '?' : '!'}</text>;
    }
    default:
      return null;
  }
};
