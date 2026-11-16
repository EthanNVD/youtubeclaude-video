import React from 'react';
import { C, INK, FONT, PAPER, col, uiColor } from '../theme';
import { clamp, easeFn, spring01, lerp } from '../lib/anim';
import { Flag } from '../props/Props';
import { Vehicle } from '../props/Vehicles';

/**
 * "Storytelling devices": the recurring, scored visual spine of a video (the channel's scale / EXIT road /
 * war meter / ledger / workbench ranking). Each is one element with timed sub-events.
 * Times inside `items` (`in`) are seconds relative to the scene start, like element times.
 */

type Item = { label?: string; value?: number; side?: string; in?: number; color?: string; icon?: string; sub?: string; nation?: string; at?: number; taken?: boolean };

// ---------- Scale (balance) ----------
export const ScaleDevice: React.FC<{ t: number; left?: string; right?: string; leftNation?: string; rightNation?: string; items?: Item[]; title?: string; tilt?: number }> = ({ t, left, right, leftNation, rightNation, items = [], title, tilt }) => {
  let L = 0, R = 0;
  let lastIn = -1;
  for (const it of items) if ((it.in ?? 0) <= t) { if (it.side === 'R' || it.side === 'right') R += it.value ?? 1; else L += it.value ?? 1; lastIn = Math.max(lastIn, it.in ?? 0); }
  const target = tilt ?? clamp((R - L) / Math.max(4, L + R) * 22, -16, 16);
  // spring toward target after each change
  const settle = lastIn < 0 ? 1 : spring01(t - lastIn, 0.9, 0.35);
  let prevL = 0, prevR = 0;
  for (const it of items) if ((it.in ?? 0) < lastIn) { if (it.side === 'R' || it.side === 'right') prevR += it.value ?? 1; else prevL += it.value ?? 1; }
  const prev = tilt ?? clamp((prevR - prevL) / Math.max(4, prevL + prevR) * 22, -16, 16);
  const ang = lerp(prev, target, settle);
  const rad = (ang * Math.PI) / 180;
  const arm = 420;
  const lx = -arm * Math.cos(rad), ly = -arm * Math.sin(rad);
  const rx = arm * Math.cos(rad), ry = arm * Math.sin(rad);
  const pan = (x: number, y: number, side: 'L' | 'R', nat?: string, label?: string) => {
    const mine = items.filter((it) => ((it.side === 'R' || it.side === 'right') ? 'R' : 'L') === side && (it.in ?? 0) <= t);
    return (
      <g transform={`translate(${x} ${y - 300})`}>
        <path d="M0 0 L-150 230 M0 0 L150 230" stroke="#6a5a3a" strokeWidth={4} />
        <circle r={10} fill="#c9a24a" stroke={INK} strokeWidth={3} />
        <path d="M-180 230 H180 Q170 280 0 284 Q-170 280 -180 230 Z" fill="#c9a24a" stroke={INK} strokeWidth={5} />
        {mine.map((it, i) => {
          const a = t - (it.in ?? 0);
          const drop = -200 * (1 - easeFn('out', clamp(a / 0.45)));
          const row = Math.floor(i / 3), c = i % 3;
          const bx = -110 + c * 110, by = 180 - row * 74 + drop;
          return (
            <g key={i} transform={`translate(${bx} ${by})`} opacity={clamp(a / 0.15)}>
              <path d="M-48 50 L-40 0 H40 L48 50 Z" fill={col(it.color, '#4a4a4a')} stroke={INK} strokeWidth={3.5} />
              <rect x={-14} y={-12} width={28} height={14} rx={4} fill={col(it.color, '#4a4a4a')} stroke={INK} strokeWidth={3} />
              <text y={34} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={20} fill="#fff">{(it.label ?? '').toUpperCase()}</text>
            </g>
          );
        })}
        {nat ? <g transform="translate(-60 300)"><Flag nation={nat} w={120} h={80} t={t} /></g> : null}
        {label ? <text y={nat ? 430 : 340} textAnchor="middle" fontFamily={FONT.hand} fontSize={46} fill={INK}>{label}</text> : null}
      </g>
    );
  };
  return (
    <g>
      <path d="M-160 330 H160 L120 290 H-120 Z" fill={C.wood} stroke={INK} strokeWidth={5} />
      <rect x={-16} y={-60} width={32} height={360} fill="#8a6a3a" stroke={INK} strokeWidth={5} />
      <g>
        <line x1={lx} y1={ly - 60} x2={rx} y2={ry - 60} stroke={INK} strokeWidth={26} strokeLinecap="round" />
        <line x1={lx} y1={ly - 60} x2={rx} y2={ry - 60} stroke="#c9a24a" strokeWidth={16} strokeLinecap="round" />
      </g>
      <circle cy={-60} r={22} fill="#c9a24a" stroke={INK} strokeWidth={5} />
      <path d={`M0 -84 L-12 -130 H12 Z`} fill="#c9a24a" stroke={INK} strokeWidth={4} transform={`rotate(${ang} 0 -60)`} />
      {pan(lx, ly + 240, 'L', leftNation, left)}
      {pan(rx, ry + 240, 'R', rightNation, right)}
      {title ? <text y={420} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={44} fill={INK}>{title}</text> : null}
    </g>
  );
};

// ---------- Meter (gauge) ----------
export const MeterDevice: React.FC<{ t: number; value?: number; left?: string; right?: string; title?: string; leftColor?: string; rightColor?: string }> = ({ value = 0, left, right, title, leftColor = C.blue, rightColor = C.red }) => {
  const v = clamp(value, -1, 1);
  const ang = v * 80;
  const R = 300;
  const arc = (a0: number, a1: number) => {
    const p = (a: number) => [Math.sin((a * Math.PI) / 180) * R, -Math.cos((a * Math.PI) / 180) * R];
    const [x0, y0] = p(a0), [x1, y1] = p(a1);
    return `M${x0} ${y0} A${R} ${R} 0 0 1 ${x1} ${y1}`;
  };
  return (
    <g>
      <path d={`M${-R - 50} 40 A${R + 50} ${R + 50} 0 0 1 ${R + 50} 40 Z`} fill={PAPER} stroke={INK} strokeWidth={6} />
      <path d={arc(-80, -5)} stroke={col(leftColor)} strokeWidth={56} fill="none" />
      <path d={arc(5, 80)} stroke={col(rightColor)} strokeWidth={56} fill="none" />
      <path d={arc(-5, 5)} stroke="#bbb" strokeWidth={56} fill="none" />
      {Array.from({ length: 17 }, (_, i) => <line key={i} y1={-R + 40} y2={-R + 62} stroke={INK} strokeWidth={4} transform={`rotate(${-80 + i * 10})`} />)}
      <g transform={`rotate(${ang})`}>
        <path d={`M-14 0 L0 ${-R + 30} L14 0 Z`} fill={INK} />
      </g>
      <circle r={30} fill="#c9a24a" stroke={INK} strokeWidth={5} />
      {left ? <text x={-R + 10} y={100} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={40} fill={col(leftColor)}>{left}</text> : null}
      {right ? <text x={R - 10} y={100} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={40} fill={col(rightColor)}>{right}</text> : null}
      {title ? <text y={-R - 80} textAnchor="middle" fontFamily={FONT.heavy} fontSize={64} fill={INK}>{title}</text> : null}
    </g>
  );
};

// ---------- Bars ----------
export const BarsDevice: React.FC<{ t: number; items?: Item[]; max?: number; unit?: string; title?: string; width?: number; vertical?: boolean }> = ({ t, items = [], max, unit = '', title, width = 1100 }) => {
  const m = max ?? Math.max(1, ...items.map((i) => i.value ?? 0));
  const rowH = Math.min(130, 560 / Math.max(1, items.length));
  return (
    <g>
      {title ? <text x={0} y={-50} textAnchor="middle" fontFamily={FONT.heavy} fontSize={60} fill={INK}>{title}</text> : null}
      {items.map((it, i) => {
        const a = t - (it.in ?? 0);
        if (a < 0) return null;
        const k = easeFn('out', clamp(a / 1.2));
        const v = (it.value ?? 0) * k;
        const bw = (v / m) * width;
        const y = i * rowH;
        const c = it.nation ? uiColor(it.nation) : col(it.color, C.red);
        return (
          <g key={i} transform={`translate(${-width / 2} ${y})`} opacity={clamp(a / 0.2)}>
            {it.nation ? <g transform={`translate(-140 ${rowH * 0.12})`}><Flag nation={it.nation} w={110} h={rowH * 0.62} t={t} still /></g> : null}
            <text x={-20} y={rowH * 0.5} textAnchor="end" fontFamily={FONT.cond} fontWeight={700} fontSize={Math.min(40, rowH * 0.36)} fill={INK} dominantBaseline="middle">{it.nation ? '' : it.label}</text>
            <rect x={0} y={rowH * 0.12} width={Math.max(4, bw)} height={rowH * 0.62} fill={c} stroke={INK} strokeWidth={4} />
            <text x={bw + 18} y={rowH * 0.5} fontFamily={FONT.heavy} fontSize={Math.min(52, rowH * 0.46)} fill={INK} dominantBaseline="middle">{Math.round(v).toLocaleString('en-US') + unit}</text>
            {it.nation && it.label ? <text x={12} y={rowH * 0.5} fontFamily={FONT.cond} fontWeight={700} fontSize={Math.min(34, rowH * 0.3)} fill="#fff" dominantBaseline="middle">{it.label}</text> : null}
          </g>
        );
      })}
    </g>
  );
};

// ---------- Scoreboard (two or more sides) ----------
export const ScoreDevice: React.FC<{ t: number; sides?: { nation?: string; label?: string; score?: number; color?: string }[]; title?: string; scores?: number[] }> = ({ t, sides = [], title, scores }) => {
  const w = 230;
  return (
    <g>
      <rect x={-(sides.length * w) / 2 - 20} y={title ? -70 : -20} width={sides.length * w + 40} height={title ? 250 : 200} rx={10} fill="#23211e" stroke={INK} strokeWidth={5} />
      {title ? <text y={-24} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={34} fill="#e9dfc4" letterSpacing={3}>{title}</text> : null}
      {sides.map((s, i) => {
        const x = -(sides.length * w) / 2 + i * w + w / 2;
        const sc = scores?.[i] ?? s.score ?? 0;
        return (
          <g key={i} transform={`translate(${x} 0)`}>
            {s.nation ? <g transform="translate(-45 0)"><Flag nation={s.nation} w={90} h={60} t={t} still /></g> : null}
            <text y={s.nation ? 92 : 60} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={30} fill="#e9dfc4">{(s.label ?? '').toUpperCase()}</text>
            <text y={160} textAnchor="middle" fontFamily={FONT.heavy} fontSize={76} fill={col(s.color, C.yellow)}>{Math.round(sc)}</text>
          </g>
        );
      })}
    </g>
  );
};

// ---------- Road with EXITs ----------
// A self-contained, scrolling world (draw it on a plain set):
// - sky, far forest (parallax 0.12), poplar row (0.45) and fields;
// - the road with verges, fence posts and kilometre stones at road speed (1.0).
// Exits sit ABOVE the road as real slip roads with a gantry sign; town boards stand on the near verge, so they never collide.
// progress 0..1 = how far along `length` the convoy (fixed at screen x 660) has driven.
type RoadExit = Item & { painted?: string; num?: string; paintIn?: number };
const PAINT: Record<string, [string, string, string]> = {
  allied: ['#2f5d9a', '#fff', 'ALLIED EXIT'],
  german: ['#5a6066', '#fff', 'GERMAN EXIT'],
  blank: ['#f4f1ea', INK, ''],
};
export const RoadDevice: React.FC<{ t: number; progress?: number; exits?: RoadExit[]; towns?: Item[]; vehicle?: string; nation?: string; length?: number; color?: string; sea?: boolean; polder?: boolean; vehicles?: number; time?: string }> = ({ t, progress = 0, exits = [], towns = [], vehicle = 'tank', nation: nat, length = 24000, vehicles = 1, time = 'day' }) => {
  const vx = progress * length;
  const night = time === 'night';
  const W = 2800; // drawn width (local x -1400..1400)
  const wrap = (x: number, period: number) => ((x % period) + period) % period;
  const sky = night ? ['#1b2740', '#3a4a66'] : time === 'dusk' ? ['#6b6f96', '#f0b88a'] : ['#8fbfdc', '#e4eef0'];
  const asphalt = '#8c8478';
  const VEH_X = -300; // convoy position (screen x 660 when the element sits at x 960)
  // far forest strip (repeats every 600 px)
  const forest = (off: number, y: number, h: number, c: string, seed: number) => (
    <g transform={`translate(${-wrap(off, 600) - 1400} 0)`}>
      {Array.from({ length: 6 }, (_, k) => (
        <g key={k} transform={`translate(${k * 600} 0)`}>
          {Array.from({ length: 14 }, (_, i) => {
            const x = i * 43 + ((i * 37 + seed) % 17);
            const hh = h * (0.7 + (((i * 53 + seed) % 10) / 30));
            return <path key={i} d={`M${x - 16} ${y} L${x} ${y - hh} L${x + 16} ${y} Z`} fill={c} />;
          })}
        </g>
      ))}
    </g>
  );
  return (
    <g>
      {/* sky + far world (slow parallax) */}
      <defs>
        <linearGradient id="road_sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={sky[0]} />
          <stop offset="1" stopColor={sky[1]} />
        </linearGradient>
      </defs>
      <rect x={-1400} y={-900} width={W} height={760} fill="url(#road_sky)" />
      {[0, 1, 2, 3].map((i) => {
        const cx = wrap(-vx * 0.05 + i * 700 + t * 6, 2800) - 1400;
        return <ellipse key={i} cx={cx} cy={-720 + (i % 2) * 70} rx={130} ry={34} fill="#fff" opacity={night ? 0.12 : 0.75} />;
      })}
      <rect x={-1400} y={-150} width={W} height={900} fill={night ? '#3d4a3a' : '#8fae5a'} />
      <g opacity={0.55}>{forest(vx * 0.12, -150, 80, night ? '#2a3a32' : '#6f8f78', 7)}</g>
      <g>{forest(vx * 0.2, -140, 60, night ? '#24322a' : '#557a5c', 3)}</g>
      {/* field bands */}
      {[-120, -95, -70].map((y, i) => <rect key={i} x={-1400} y={y} width={W} height={10} fill="#000" opacity={0.04 + i * 0.01} />)}
      {/* poplar row behind the road (mid parallax) */}
      <g transform={`translate(${-wrap(vx * 0.45, 260) - 1400} 0)`}>
        {Array.from({ length: 13 }, (_, i) => (
          <g key={i} transform={`translate(${i * 260} -60)`}>
            <rect x={-4} y={-20} width={8} height={22} fill="#5a4030" />
            <ellipse cx={0} cy={-70} rx={20} ry={58} fill={night ? '#2f4a32' : '#4f7a3a'} stroke={INK} strokeWidth={2.5} />
          </g>
        ))}
      </g>
      {/* everything at road speed */}
      <g transform={`translate(${-vx} 0)`}>
        {/* exits (above the road): slip road + gantry sign */}
        {exits.map((e, i) => {
          const x = (e.at ?? (i + 1) / (exits.length + 1)) * length;
          if (Math.abs(x - vx) > 2200) return null;
          const painted = e.painted && e.painted !== 'none' && t >= (e.paintIn ?? 0) ? e.painted : undefined;
          const pk = painted ? clamp((t - (e.paintIn ?? 0)) / 0.6) : 0;
          const [pc, tc, head] = painted ? PAINT[painted] ?? PAINT.allied : ['#2f7a3a', '#fff', 'EXIT'];
          const lit = !!painted && pk > 0.5;
          const sx = x - 60; // sign centre
          return (
            <g key={i}>
              {/* slip road leaving the carriageway and receding toward the horizon */}
              <path d={`M${x - 140} -26 L${x + 40} -26 L${x + 230} -138 L${x + 200} -142 Z`} fill={asphalt} stroke={INK} strokeWidth={3} strokeLinejoin="round" />
              <path d={`M${x - 60} -26 L${x + 215} -140`} stroke="#fff" strokeWidth={3} strokeDasharray="14 12" opacity={0.6} />
              {/* gantry */}
              <path d={`M${sx - 150} -30 V-200 M${sx + 150} -30 V-200`} stroke="#5a5a52" strokeWidth={8} />
              <g transform={`translate(${sx} -270)`}>
                <rect x={-190} y={-64} width={380} height={128} rx={10} fill="#2f7a3a" stroke={INK} strokeWidth={4} />
                {painted ? <rect x={-190} y={-64} width={380 * pk} height={128} rx={10} fill={pc} stroke={INK} strokeWidth={4} /> : null}
                <rect x={-180} y={-54} width={360} height={108} rx={7} fill="none" stroke={lit ? tc : '#fff'} strokeOpacity={0.7} strokeWidth={3} />
                {painted === 'blank' && pk >= 1 ? (
                  <text y={20} textAnchor="middle" fontFamily={FONT.heavy} fontSize={60} fill="#c9c2b0">?</text>
                ) : (
                  <g>
                    <text y={-22} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={22} fill={lit ? tc : '#fff'} letterSpacing={3}>{lit ? head : 'EXIT'}</text>
                    <text y={12} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={Math.min(32, 640 / Math.max(10, (e.label ?? '').length))} fill={lit ? tc : '#fff'}>{(e.label ?? '').toUpperCase()}</text>
                    {e.sub ? <text y={42} textAnchor="middle" fontFamily={FONT.hand} fontSize={24} fill={lit ? tc : '#e9f2e4'}>{e.sub}</text> : null}
                  </g>
                )}
                {painted && painted !== 'blank' && e.num && pk >= 1 ? (
                  <g transform="translate(178 -60)">
                    <circle r={30} fill={C.yellow} stroke={INK} strokeWidth={4} />
                    <text y={11} textAnchor="middle" fontFamily={FONT.heavy} fontSize={30} fill={INK}>{e.num}</text>
                  </g>
                ) : null}
              </g>
            </g>
          );
        })}
        {/* road */}
        <rect x={vx - 1500} y={-30} width={3000} height={60} fill={asphalt} />
        <path d={`M${vx - 1500} -30 H${vx + 1500} M${vx - 1500} 30 H${vx + 1500}`} stroke={INK} strokeWidth={4} />
        {Array.from({ length: 22 }, (_, i) => {
          const x = Math.floor((vx - 1500) / 160) * 160 + i * 160;
          return <rect key={i} x={x} y={-3} width={80} height={6} fill="#fff" opacity={0.75} />;
        })}
        {/* near verge: fence posts + kilometre stones */}
        <rect x={vx - 1500} y={30} width={3000} height={40} fill={night ? '#34402f' : '#7a9a4a'} />
        {Array.from({ length: 14 }, (_, i) => {
          const x = Math.floor((vx - 1500) / 240) * 240 + i * 240;
          return <rect key={i} x={x} y={48} width={8} height={40} fill="#6a5040" stroke={INK} strokeWidth={2} />;
        })}
        <path d={`M${vx - 1500} 62 H${vx + 1500}`} stroke="#6a5040" strokeWidth={3} />
        {/* town boards on the near verge */}
        {towns.map((tw, i) => {
          const x = (tw.at ?? 0) * length;
          if (Math.abs(x - vx) > 2200) return null;
          return (
            <g key={'t' + i} transform={`translate(${x} 60)`}>
              <line x1={0} y1={0} x2={0} y2={70} stroke="#5a5a52" strokeWidth={6} />
              <rect x={-120} y={-58} width={240} height={58} rx={5} fill="#f4f1ea" stroke={INK} strokeWidth={4} />
              <rect x={-112} y={-50} width={224} height={42} rx={3} fill="none" stroke={C.red} strokeWidth={4} />
              <text y={-17} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={Math.min(30, 380 / Math.max(6, (tw.label ?? '').length))} fill={INK}>{(tw.label ?? '').toUpperCase()}</text>
            </g>
          );
        })}
      </g>
      {/* foreground field below the verge */}
      <rect x={-1400} y={70} width={W} height={700} fill={night ? '#2f3a2b' : '#86a650'} />
      {Array.from({ length: 6 }, (_, i) => <path key={i} d={`M-1400 ${110 + i * i * 14} H1400`} stroke="#5b86a8" strokeWidth={3 + i} opacity={0.35} />)}
      {/* convoy (fixed on screen, the world scrolls past) */}
      {Array.from({ length: Math.max(1, vehicles) }, (_, i) => (
        <g key={'v' + i} transform={`translate(${VEH_X - i * 290} 6) scale(0.62)`}>
          <Vehicle type={vehicle} nationKey={nat} t={t + i * 0.3} moving={progress > 0} travel={vx / 0.62} />
        </g>
      ))}
    </g>
  );
};

// ---------- Ranking list (No.10 -> No.1) ----------
export const RankingDevice: React.FC<{ t: number; items?: Item[]; highlight?: number; title?: string }> = ({ t, items = [], highlight, title }) => {
  const rowH = Math.min(96, 760 / Math.max(1, items.length));
  return (
    <g>
      {title ? <text y={-40} textAnchor="middle" fontFamily={FONT.heavy} fontSize={60} fill={INK}>{title}</text> : null}
      {items.map((it, i) => {
        const a = t - (it.in ?? 0);
        const shown = a >= 0;
        const hi = highlight === i;
        return (
          <g key={i} transform={`translate(-560 ${i * rowH}) translate(${shown ? 0 : 0} 0)`}>
            <rect width={1120} height={rowH - 12} rx={8} fill={hi ? C.yellow : shown ? PAPER : '#d6ccb4'} stroke={INK} strokeWidth={4} opacity={shown ? 1 : 0.55} />
            <rect width={130} height={rowH - 12} rx={8} fill={hi ? C.red : '#23211e'} stroke={INK} strokeWidth={4} />
            <text x={65} y={(rowH - 12) / 2} textAnchor="middle" dominantBaseline="middle" fontFamily={FONT.heavy} fontSize={rowH * 0.48} fill="#fff">{it.label?.match(/^\S+/) && it.sub !== undefined ? '' : ''}{`No.${items.length - i}`.replace('No.', 'No.')}</text>
            <text x={160} y={(rowH - 12) / 2} dominantBaseline="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={rowH * 0.42} fill={INK} opacity={shown ? clamp(a / 0.3) : 0}>{shown ? it.label : ''}</text>
            {it.sub && shown ? <text x={1100} y={(rowH - 12) / 2} textAnchor="end" dominantBaseline="middle" fontFamily={FONT.hand} fontSize={rowH * 0.36} fill={INK}>{it.sub}</text> : null}
            {!shown ? <text x={160} y={(rowH - 12) / 2} dominantBaseline="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={rowH * 0.42} fill="#9a917e">? ? ?</text> : null}
          </g>
        );
      })}
    </g>
  );
};

// ---------- Timeline ----------
export const TimelineDevice: React.FC<{ t: number; items?: Item[]; cursor?: number; width?: number; start?: string; end?: string }> = ({ t, items = [], cursor, width = 1600, start, end }) => {
  return (
    <g>
      <line x1={-width / 2} x2={width / 2} stroke={INK} strokeWidth={10} strokeLinecap="round" />
      {start ? <text x={-width / 2} y={70} textAnchor="middle" fontFamily={FONT.hand} fontSize={40} fill={INK}>{start}</text> : null}
      {end ? <text x={width / 2} y={70} textAnchor="middle" fontFamily={FONT.hand} fontSize={40} fill={INK}>{end}</text> : null}
      {items.map((it, i) => {
        const a = t - (it.in ?? 0);
        if (a < 0) return null;
        const x = -width / 2 + (it.at ?? i / Math.max(1, items.length - 1)) * width;
        const up = i % 2 === 0;
        const k = easeFn('back', clamp(a / 0.4));
        return (
          <g key={i} transform={`translate(${x} 0)`}>
            <circle r={16 * k} fill={col(it.color, C.red)} stroke={INK} strokeWidth={4} />
            <line y1={up ? -20 : 20} y2={(up ? -90 : 90) * k} stroke={INK} strokeWidth={3} />
            <g transform={`translate(0 ${up ? -110 : 110}) scale(${k})`}>
              <text y={up ? -36 : 20} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={30} fill={C.redDark}>{it.sub ?? ''}</text>
              <text y={up ? 0 : 56} textAnchor="middle" fontFamily={FONT.hand} fontSize={36} fill={INK}>{it.label}</text>
            </g>
          </g>
        );
      })}
      {cursor !== undefined ? <path transform={`translate(${-width / 2 + clamp(cursor) * width} -30)`} d="M-16 -30 H16 L0 0 Z" fill={C.red} stroke={INK} strokeWidth={3} /> : null}
    </g>
  );
};

// ---------- Ledger: two columns of handwritten entries with tallies ----------
export const LedgerDevice: React.FC<{ t: number; columns?: { title: string; nation?: string; entries?: Item[] }[] }> = ({ t, columns = [] }) => {
  const W = 1300, H = 760;
  return (
    <g>
      <path d={`M${-W / 2} ${-H / 2} Q${-W / 4} ${-H / 2 - 30} 0 ${-H / 2} Q${W / 4} ${-H / 2 - 30} ${W / 2} ${-H / 2} V${H / 2} Q${W / 4} ${H / 2 - 30} 0 ${H / 2} Q${-W / 4} ${H / 2 - 30} ${-W / 2} ${H / 2} Z`} fill="#f4ecd8" stroke={INK} strokeWidth={6} />
      <line x1={0} y1={-H / 2} x2={0} y2={H / 2} stroke="#b9a98a" strokeWidth={6} />
      {Array.from({ length: 12 }, (_, i) => <line key={i} x1={-W / 2 + 30} x2={W / 2 - 30} y1={-H / 2 + 120 + i * 52} y2={-H / 2 + 120 + i * 52} stroke="#c9d6e0" strokeWidth={2} />)}
      {columns.slice(0, 2).map((c, ci) => {
        const x0 = ci === 0 ? -W / 2 + 50 : 50;
        const shown = (c.entries ?? []).filter((e) => (e.in ?? 0) <= t);
        return (
          <g key={ci}>
            {c.nation ? <g transform={`translate(${x0} ${-H / 2 + 30})`}><Flag nation={c.nation} w={80} h={54} t={t} still /></g> : null}
            <text x={x0 + (c.nation ? 100 : 0)} y={-H / 2 + 74} fontFamily={FONT.cond} fontWeight={700} fontSize={48} fill={INK}>{c.title.toUpperCase()}</text>
            <text x={x0 + 520} y={-H / 2 + 74} textAnchor="end" fontFamily={FONT.heavy} fontSize={60} fill={C.red}>{shown.reduce((s, e) => s + (e.value ?? 1), 0)}</text>
            {(c.entries ?? []).map((e, i) => {
              const a = t - (e.in ?? 0);
              if (a < 0) return null;
              const text = (e.label ?? '');
              const n = Math.floor(clamp(a / Math.max(0.6, text.length * 0.045)) * text.length);
              return <text key={i} x={x0} y={-H / 2 + 160 + i * 52} fontFamily={FONT.hand} fontSize={38} fill={e.taken === false ? '#9a917e' : INK} textDecoration={e.taken === false ? 'line-through' : undefined}>{'✗ '.slice(0, 0) + text.slice(0, n)}</text>;
            })}
          </g>
        );
      })}
    </g>
  );
};
