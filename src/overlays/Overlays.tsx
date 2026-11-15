import React from 'react';
import { C, INK, FONT, PAPER, col } from '../theme';
import { clamp, easeFn } from '../lib/anim';

const shadow = { filter: 'drop-shadow(4px 5px 0 rgba(0,0,0,0.25))' } as const;

/** Paper date tag, top-left (the channel's "27 MAY 1940"). a = seconds since shown. */
export const DateBadge: React.FC<{ text: string; a: number; x?: number; y?: number; right?: boolean }> = ({ text, a, x, y = 46, right }) => {
  const k = easeFn('out', clamp(a / 0.45));
  const w = Math.max(160, text.length * 25 + 50);
  const X = x ?? (right ? 1920 - 46 - w : 46);
  return (
    <g transform={`translate(${X + (right ? 1 : -1) * (1 - k) * (w + 80)} ${y}) rotate(${right ? 0.8 : -0.8})`} style={shadow}>
      <rect width={w} height={78} rx={3} fill={PAPER} stroke="#5a5048" strokeWidth={4} />
      <rect x={6} y={6} width={w - 12} height={66} fill="none" stroke="#5a5048" strokeOpacity={0.35} strokeWidth={2} />
      <text x={w / 2} y={54} textAnchor="middle" fontFamily={FONT.hand} fontSize={44} fill={INK} letterSpacing={1}>{text}</text>
    </g>
  );
};

export const NameCard: React.FC<{ name: string; role?: string; a: number; x?: number; y?: number }> = ({ name, role, a, x = 70, y = 860 }) => {
  const k = easeFn('out', clamp(a / 0.5));
  const w = Math.max(name.length * 30 + 60, (role?.length ?? 0) * 19 + 60);
  return (
    <g transform={`translate(${x - (1 - k) * 700} ${y})`} style={shadow}>
      <rect width={w} height={role ? 126 : 82} fill="#fbf6e8" stroke={INK} strokeWidth={4} />
      <rect width={14} height={role ? 126 : 82} fill={C.red} />
      <text x={34} y={58} fontFamily={FONT.cond} fontWeight={700} fontSize={50} fill={C.redDark} letterSpacing={0.5}>{name.toUpperCase()}</text>
      {role ? <text x={36} y={104} fontFamily={FONT.hand} fontSize={34} fill={INK}>{role}</text> : null}
    </g>
  );
};

/** Label tag; optional leader line to (tx,ty) in the same coordinate space. */
export const Label: React.FC<{ text: string; style?: string; size?: number; color?: string; tx?: number; ty?: number; dx?: number; dy?: number; rotate?: number; maxW?: number }> = ({ text, style = 'tag', size = 40, color, tx, ty, rotate = 0 }) => {
  const lines = String(text).split('\n');
  const font = style === 'plain' || style === 'map' ? FONT.hand : FONT.cond;
  const wgt = style === 'plain' || style === 'map' ? 400 : 700;
  const cw = font === FONT.cond ? 0.52 : 0.5;
  const w = Math.max(...lines.map((l) => l.length)) * size * cw + 36;
  const h = lines.length * size * 1.12 + 22;
  const bg = style === 'red' ? C.red : style === 'dark' ? '#23211e' : style === 'green' ? '#2f7a3a' : style === 'yellow' ? C.yellow : PAPER;
  const fg = style === 'red' || style === 'dark' || style === 'green' ? '#fff' : color ? col(color) : INK;
  return (
    <g>
      {tx !== undefined && ty !== undefined ? (
        <g>
          <line x1={0} y1={h / 2} x2={tx} y2={ty} stroke={INK} strokeWidth={4} />
          <circle cx={tx} cy={ty} r={7} fill={INK} />
        </g>
      ) : null}
      <g transform={`rotate(${rotate})`} style={style === 'plain' || style === 'map' ? undefined : shadow}>
        {style === 'plain' || style === 'map' ? null : <rect x={-w / 2} y={0} width={w} height={h} rx={4} fill={bg} stroke={INK} strokeWidth={3.5} />}
        {lines.map((l, i) => (
          <text key={i} x={0} y={size * 0.98 + 8 + i * size * 1.12} textAnchor="middle" fontFamily={font} fontWeight={wgt} fontSize={size} fill={style === 'map' ? INK : fg}
            stroke={style === 'plain' || style === 'map' ? '#fbf8f0' : undefined} strokeWidth={style === 'plain' || style === 'map' ? size / 7 : undefined} paintOrder="stroke" letterSpacing={style === 'map' ? 2 : 0.5}>
            {style === 'map' ? l.toUpperCase() : l}
          </text>
        ))}
      </g>
    </g>
  );
};

export const Stamp: React.FC<{ text: string; color?: string; size?: number; rotate?: number }> = ({ text, color = C.red, size = 90, rotate = -12 }) => {
  const c = col(color);
  const w = text.length * size * 0.6 + 60;
  const h = size * 1.35;
  return (
    <g transform={`rotate(${rotate})`} opacity={0.92}>
      <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={10} fill="none" stroke={c} strokeWidth={10} />
      <rect x={-w / 2 + 12} y={-h / 2 + 12} width={w - 24} height={h - 24} rx={6} fill="none" stroke={c} strokeWidth={3} />
      <text x={0} y={size * 0.36} textAnchor="middle" fontFamily={FONT.heavy} fontSize={size} fill={c} letterSpacing={4}>{text.toUpperCase()}</text>
    </g>
  );
};

/** Speech/thought bubble; origin = tail tip (speaker's mouth). Box drawn above-right (or left with side=-1). */
export const Bubble: React.FC<{ text: string; thought?: boolean; side?: number; size?: number; a: number }> = ({ text, thought, side = 1, size = 38, a }) => {
  const lines = String(text).split('\n');
  const w = Math.max(...lines.map((l) => l.length)) * size * 0.5 + 60;
  const h = lines.length * size * 1.15 + 34;
  const bx = side > 0 ? 30 : -30 - w;
  const by = -h - 70;
  const k = clamp(a / 0.25);
  return (
    <g transform={`scale(${0.6 + 0.4 * easeFn('back', k)})`} opacity={k}>
      {thought ? (
        <>
          <circle cx={side * 14} cy={-20} r={8} fill="#fff" stroke={INK} strokeWidth={3} />
          <circle cx={side * 26} cy={-46} r={13} fill="#fff" stroke={INK} strokeWidth={3} />
          <ellipse cx={bx + w / 2} cy={by + h / 2} rx={w / 2 + 26} ry={h / 2 + 16} fill="#fff" stroke={INK} strokeWidth={4} />
        </>
      ) : (
        <>
          <rect x={bx} y={by} width={w} height={h} rx={h / 2.2} fill="#fff" stroke={INK} strokeWidth={4} />
          <path d={`M${side > 0 ? bx + 40 : bx + w - 40} ${by + h - 3} L0 0 L${side > 0 ? bx + 90 : bx + w - 90} ${by + h - 3} Z`} fill="#fff" stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <path d={`M${side > 0 ? bx + 42 : bx + w - 42} ${by + h - 4} L${side > 0 ? bx + 88 : bx + w - 88} ${by + h - 4}`} stroke="#fff" strokeWidth={6} />
        </>
      )}
      {lines.map((l, i) => (
        <text key={i} x={bx + w / 2} y={by + 22 + size * 0.95 + i * size * 1.15} textAnchor="middle" fontFamily={FONT.hand} fontSize={size} fill={INK}>{l}</text>
      ))}
    </g>
  );
};

/** Big kinetic headline (intro / verdict / myth). */
export const Headline: React.FC<{ text: string; size?: number; color?: string; accent?: string; a: number; font?: string }> = ({ text, size = 130, color = '#fff', accent, a, font }) => {
  const words = String(text).split(' ');
  return (
    <g>
      <text textAnchor="middle" fontFamily={font === 'hand' ? FONT.hand : FONT.heavy} fontSize={size} stroke={INK} strokeWidth={size / 7} paintOrder="stroke" strokeLinejoin="round" letterSpacing={2}>
        {words.map((w, i) => {
          const k = clamp((a - i * 0.12) / 0.25);
          const isAcc = accent && w.replace(/[^\p{L}\p{N}]/gu, '').toUpperCase() === accent.toUpperCase();
          return (
            <tspan key={i} fill={isAcc ? C.yellow : col(color, '#fff')} opacity={k}>{w + (i < words.length - 1 ? ' ' : '')}</tspan>
          );
        })}
      </text>
    </g>
  );
};

export const Counter: React.FC<{ from?: number; to: number; a: number; dur?: number; size?: number; prefix?: string; suffix?: string; color?: string; decimals?: number }> = ({ from = 0, to, a, dur = 1.5, size = 110, prefix = '', suffix = '', color, decimals = 0 }) => {
  const v = from + (to - from) * easeFn('out', clamp(a / dur));
  const s = v.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  return <text textAnchor="middle" fontFamily={FONT.heavy} fontSize={size} fill={col(color, '#fff')} stroke={INK} strokeWidth={size / 8} paintOrder="stroke">{prefix + s + suffix}</text>;
};

/** Paper document with progressive text (typewriter). style: telegram | letter | order | newspaper | book | blackboard | note */
export const Document: React.FC<{ style?: string; title?: string; lines?: string[]; a: number; speed?: number; w?: number; h?: number; stamp?: string; size?: number }> = ({ style = 'letter', title, lines = [], a, speed = 28, w = 760, h = 520, stamp, size }) => {
  const total = lines.join('').length;
  let budget = Math.floor(a * speed);
  const bg = style === 'telegram' ? '#efe2b0' : style === 'blackboard' ? '#2f4a3a' : style === 'newspaper' ? '#ece6d6' : PAPER;
  const fg = style === 'blackboard' ? '#eef3ea' : INK;
  const font = style === 'telegram' || style === 'order' ? FONT.mono : style === 'blackboard' || style === 'letter' || style === 'note' ? FONT.hand : FONT.serif;
  const fs = size ?? (style === 'newspaper' ? 36 : style === 'telegram' || style === 'order' ? 40 : 44);
  return (
    <g>
      <g transform={`rotate(${style === 'blackboard' ? 0 : -1.2})`}>
        <rect x={-w / 2 + 10} y={-h / 2 + 12} width={w} height={h} fill="#000" opacity={0.25} />
        <rect x={-w / 2} y={-h / 2} width={w} height={h} fill={bg} stroke={style === 'blackboard' ? '#6b4a2a' : INK} strokeWidth={style === 'blackboard' ? 16 : 4} />
        {title ? (
          <g>
            <text x={0} y={-h / 2 + (style === 'newspaper' ? 86 : 70)} textAnchor="middle" fontFamily={style === 'newspaper' ? FONT.serif : style === 'blackboard' ? FONT.hand : FONT.cond} fontWeight={style === 'newspaper' ? 900 : 700} fontSize={style === 'newspaper' ? 72 : 46} fill={fg}>{title}</text>
            <line x1={-w / 2 + 30} x2={w / 2 - 30} y1={-h / 2 + (style === 'newspaper' ? 110 : 92)} y2={-h / 2 + (style === 'newspaper' ? 110 : 92)} stroke={fg} strokeWidth={style === 'newspaper' ? 5 : 2} />
          </g>
        ) : null}
        {lines.map((l, i) => {
          const show = l.slice(0, Math.max(0, budget));
          budget -= l.length;
          return (
            <text key={i} x={fs >= 80 ? 0 : -w / 2 + 40} textAnchor={fs >= 80 ? 'middle' : 'start'} y={-h / 2 + (title ? (style === 'newspaper' ? 130 : 112) : 30) + fs * 1.05 + i * fs * 1.35} fontFamily={font} fontSize={fs} fontWeight={style === 'order' ? 600 : 400} fill={fg}>
              {show}
              {show.length < l.length && show.length > 0 && style !== 'blackboard' ? '▌' : ''}
            </text>
          );
        })}
        {stamp && a * speed > total + 8 ? <g transform={`translate(${w / 2 - 170} ${h / 2 - 90})`}><Stamp text={stamp} size={56} /></g> : null}
      </g>
    </g>
  );
};
