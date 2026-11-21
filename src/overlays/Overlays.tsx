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
  const bare = style === 'plain' || style === 'map' || style === 'chalk';
  const font = bare ? FONT.hand : FONT.cond;
  const wgt = bare ? 400 : 700;
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
      <g transform={`rotate(${rotate})`} style={bare ? undefined : shadow}>
        {bare ? null : <rect x={-w / 2} y={0} width={w} height={h} rx={4} fill={bg} stroke={INK} strokeWidth={3.5} />}
        {lines.map((l, i) => (
          <text key={i} x={0} y={size * 0.98 + 8 + i * size * 1.12} textAnchor="middle" fontFamily={font} fontWeight={wgt} fontSize={size} fill={style === 'map' ? INK : style === 'chalk' ? (color ? col(color) : '#eef3ea') : fg} opacity={style === 'chalk' ? 0.9 : undefined}
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


/** Documentary place/time tag (top-left wooden plank): "SPA, BELGIUM · 29 SEPTEMBER 1918". `a` = seconds since it appeared
 *  (negative = not yet); a tag carried over from the previous scene is passed a large `a` so it does not re-animate. */
export const PlaceTag: React.FC<{ text: string; a: number }> = ({ text, a }) => {
  if (a < 0) return null;
  const k = easeFn('out', clamp(a / 0.5));
  const w = text.length * 15.5 + 96;
  return (
    <g transform={`translate(${34 - (1 - k) * 40} 34)`} opacity={k}>
      <rect x={0} y={0} width={w} height={44} rx={3} fill="#5b3b22" stroke="#2c1b0e" strokeWidth={3} />
      <rect x={4} y={4} width={w - 8} height={36} rx={2} fill="none" stroke="#c8a067" strokeOpacity={0.45} strokeWidth={1.5} />
      <circle cx={22} cy={22} r={5} fill="#c8a067" />
      <text x={40} y={30} fontFamily={FONT.title} fontWeight={700} fontSize={21} letterSpacing={2.2} fill="#f0dfbd">{text.toUpperCase()}</text>
    </g>
  );
};

type CapWord = { w: string; t: number; accent?: boolean };
/** Kinetic caption for the film's key questions: words appear as they are spoken (0.2 s fade), accent words in amber. */
export const KineticCaption: React.FC<{ words: CapWord[]; a: number; out?: number; y?: number; size?: number }> = ({ words, a, out, y = 968, size = 40 }) => {
  const vis = words.filter((w) => a >= w.t);
  if (!vis.length) return null;
  const fade = out !== undefined ? clamp(1 - (a - out) / 0.4) : 1;
  if (fade <= 0) return null;
  // wrap into lines of ~44 characters (all words, so lines never jump as words arrive)
  const lines: CapWord[][] = [[]];
  let len = 0;
  for (const w of words) {
    if (len + w.w.length > 44 && lines[lines.length - 1].length) { lines.push([]); len = 0; }
    lines[lines.length - 1].push(w);
    len += w.w.length + 1;
  }
  return (
    <g opacity={fade}>
      <defs>
        <linearGradient id="capfade" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0" stopColor="#000" stopOpacity={0} />
          <stop offset="1" stopColor="#000" stopOpacity={0.62} />
        </linearGradient>
      </defs>
      <rect x={0} y={y - 150 - (lines.length - 1) * size * 1.2} width={1920} height={1080 - y + 150 + (lines.length - 1) * size * 1.2} fill="url(#capfade)" />
      {lines.map((ln, li) => {
        const yy = y - (lines.length - 1 - li) * size * 1.2;
        // the whole line is laid out once (all words), unspoken words are transparent: nothing shifts as words arrive
        return (
          <text key={li} x={960} y={yy} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={size} letterSpacing={1}
                style={{ paintOrder: 'stroke' }} stroke="#000" strokeOpacity={0.25} strokeWidth={3}>
            {ln.map((w, wi) => (
              <tspan key={wi} fill={w.accent ? '#f0a838' : '#f6efe2'} fillOpacity={clamp((a - w.t) / 0.2)} strokeOpacity={0.25 * clamp((a - w.t) / 0.2)}>
                {(wi ? ' ' : '') + w.w.toUpperCase()}
              </tspan>
            ))}
          </text>
        );
      })}
    </g>
  );
};

/** Statistic / fact card: small top line, big engraved capitals, a book-serif sub-line ("70–85 MILLION DEAD / most of them civilians"). */
export const StatCard: React.FC<{ top?: string; title: string; sub?: string; a: number; out?: number; y?: number; align?: 'center' | 'left' }> = ({ top, title, sub, a, out, y = 820, align = 'center' }) => {
  if (a < 0) return null;
  const k = easeFn('out', clamp(a / 0.6));
  const fade = out !== undefined ? clamp(1 - (a - out) / 0.4) : 1;
  const x = align === 'center' ? 960 : 90;
  const anchor = align === 'center' ? 'middle' : 'start';
  return (
    <g opacity={k * fade} transform={`translate(0 ${(1 - k) * 12})`}>
      {align === 'center' ? (
        <rect x={0} y={y - 150} width={1920} height={300} fill="url(#statfade)" />
      ) : null}
      <defs>
        <radialGradient id="statfade" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0" stopColor="#000" stopOpacity={0.45} />
          <stop offset="1" stopColor="#000" stopOpacity={0} />
        </radialGradient>
      </defs>
      {top ? <text x={x} y={y - 72} textAnchor={anchor} fontFamily={FONT.title} fontWeight={700} fontSize={20} letterSpacing={4} fill="#f3e6c8" opacity={0.9}>{top.toUpperCase()}</text> : null}
      <text x={x} y={y} textAnchor={anchor} fontFamily={FONT.title} fontWeight={700} fontSize={68} letterSpacing={3} fill="#fbf2dc">{title.toUpperCase()}</text>
      {sub ? <text x={x} y={y + 44} textAnchor={anchor} fontFamily={FONT.book} fontWeight={600} fontStyle="italic" fontSize={30} fill="#efe2c4" opacity={0.92}>{sub}</text> : null}
    </g>
  );
};

/** Paper note pinned top-right: a quote or the key line of a document, typed line by line ("FIGHT ON. NEVER SURRENDER."). */
export const NoteCard: React.FC<{ kicker?: string; lines: string[]; a: number; speed?: number; x?: number; y?: number; accentLast?: boolean }> = ({ kicker, lines, a, speed = 28, x = 1380, y = 120, accentLast }) => {
  if (a < 0) return null;
  const k = easeFn('out', clamp(a / 0.35));
  const w = Math.max(360, Math.max(...lines.map((l) => l.length)) * 17 + 60);
  const h = 70 + lines.length * 38;
  let budget = Math.max(0, (a - 0.25) * speed);
  return (
    <g transform={`translate(${Math.min(x, 1880 - w)} ${y}) rotate(1.2) scale(${0.96 + 0.04 * k})`} opacity={k}>
      <rect x={6} y={8} width={w} height={h} fill="#000" opacity={0.25} />
      <rect x={0} y={0} width={w} height={h} fill="#f2ead6" stroke="#6b5d48" strokeWidth={2} />
      {kicker ? <text x={24} y={34} fontFamily={FONT.title} fontWeight={700} fontSize={15} letterSpacing={2.5} fill="#7d6a52">{kicker.toUpperCase()}</text> : null}
      {lines.map((l, i) => {
        const n = Math.min(l.length, Math.floor(budget));
        budget -= l.length;
        const red = accentLast && i === lines.length - 1;
        return n > 0 ? <text key={i} x={24} y={(kicker ? 70 : 48) + i * 38} fontFamily={FONT.cond} fontWeight={700} fontSize={28} fill={red ? '#b03a2e' : '#2a2622'}>{l.slice(0, n).toUpperCase()}</text> : null;
      })}
    </g>
  );
};


/** Looking through binoculars: black frame with two round lenses (the scene shows through), slight sway. */
export const BinocularView: React.FC<{ a: number; t: number }> = ({ a, t }) => {
  const k = clamp(a / 0.4);
  const sx = Math.sin(t * 0.9) * 6, sy = Math.cos(t * 0.7) * 4;
  return (
    <g opacity={k}>
      <defs>
        <mask id="binomask">
          <rect x={0} y={0} width={1920} height={1080} fill="#fff" />
          <circle cx={700 + sx} cy={540 + sy} r={430} fill="#000" />
          <circle cx={1220 + sx} cy={540 + sy} r={430} fill="#000" />
        </mask>
        <radialGradient id="binovig" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0.75" stopColor="#000" stopOpacity={0} />
          <stop offset="1" stopColor="#000" stopOpacity={0.7} />
        </radialGradient>
      </defs>
      <circle cx={700 + sx} cy={540 + sy} r={430} fill="url(#binovig)" />
      <circle cx={1220 + sx} cy={540 + sy} r={430} fill="url(#binovig)" />
      <rect x={-20} y={-20} width={1960} height={1120} fill="#050505" mask="url(#binomask)" />
    </g>
  );
};
