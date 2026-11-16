import type { Ease, ElementBase, Key } from '../types';

export const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

export const easeFn = (e: Ease | undefined, x: number): number => {
  x = clamp(x);
  switch (e) {
    case 'linear':
      return x;
    case 'in':
      return x * x * x;
    case 'out':
      return 1 - Math.pow(1 - x, 3);
    case 'back': {
      const c = 1.70158;
      return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2);
    }
    case 'step':
      return x < 1 ? 0 : 1;
    case 'drive': {
      // trapezoid speed profile: accelerate over the first 25 %, cruise, brake over the last 25 %
      const A = 0.25, vmax = 1 / (1 - A);
      if (x < A) return 0.5 * vmax * (x * x) / A;
      if (x > 1 - A) return 1 - 0.5 * vmax * ((1 - x) * (1 - x)) / A;
      return vmax * (x - A / 2);
    }
    default:
      return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  }
};

/** Damped spring 0->1 over `dur` seconds (closed form, small overshoot). */
export const spring01 = (t: number, dur = 0.5, bounce = 0.25) => {
  if (t <= 0) return 0;
  if (t >= dur * 2) return 1;
  const w = (2 * Math.PI) / dur;
  const z = 1 - bounce;
  return 1 - Math.exp(-z * w * t * 0.9) * Math.cos(w * t * 0.75);
};

/** Deterministic pseudo-random in [0,1) from any seed values. */
export const rnd = (...seed: (number | string)[]) => {
  let h = 2166136261;
  for (const s of seed) {
    const str = String(s);
    for (let i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
  }
  h ^= h >>> 13;
  h = Math.imul(h, 0x5bd1e995);
  h ^= h >>> 15;
  return (h >>> 0) / 4294967296;
};

/** Resolve an element's props at scene time t using its keyframes. */
export function resolveKeys<T extends Record<string, unknown>>(base: T, keys: Key[] | undefined, t: number): T {
  if (!keys || keys.length === 0) return base;
  const out: Record<string, unknown> = { ...base };
  const sorted = [...keys].sort((a, b) => a.t - b.t);
  // collect every animated prop
  const props = new Set<string>();
  for (const k of sorted) for (const p of Object.keys(k)) if (p !== 't' && p !== 'ease') props.add(p);
  for (const p of props) {
    // previous value: from base, then keys in order
    let prevT = -Infinity;
    let prevV: unknown = base[p];
    let next: Key | undefined;
    for (const k of sorted) {
      if (!(p in k)) continue;
      if (k.t <= t) {
        prevT = k.t;
        prevV = k[p];
      } else {
        next = k;
        break;
      }
    }
    const isArr = (v: unknown): v is number[] => Array.isArray(v) && v.every((x) => typeof x === 'number');
    if (next && isArr(next[p]) && isArr(prevV) && (next[p] as number[]).length === prevV.length) {
      const from = prevT === -Infinity ? 0 : prevT;
      const dur = (next.dur as number | undefined) ?? next.t - from;
      const start = next.t - dur;
      const k = t >= start ? easeFn(next.ease, (t - start) / Math.max(1e-6, dur)) : 0;
      out[p] = prevV.map((v, i) => lerp(v, (next![p] as number[])[i], k));
    } else if (next && typeof next[p] === 'number' && typeof prevV === 'number') {
      // tween from previous key (or from base value starting at the key before) toward next
      const from = prevT === -Infinity ? 0 : prevT;
      const dur = (next.dur as number | undefined) ?? next.t - from;
      const start = next.t - dur;
      if (t >= start) out[p] = lerp(prevV, next[p] as number, easeFn(next.ease, (t - start) / Math.max(1e-6, dur)));
      else out[p] = prevV;
    } else if (prevV !== undefined) out[p] = prevV;
  }
  return out as T;
}

/** Enter/exit envelope: returns {o: opacity, s: scale, dx, dy, r: reveal 0..1}. */
export function envelope(el: ElementBase, t: number, sceneDur: number) {
  const tin = el.in ?? 0;
  const tout = el.out ?? sceneDur + 10;
  const res = { o: 1, s: 1, dx: 0, dy: 0, r: 1, visible: true };
  if (t < tin || t > tout + 0.6) return { ...res, visible: false, o: 0 };
  const a = t - tin;
  const enter = el.enter ?? 'pop';
  const D = 0.45;
  switch (enter) {
    case 'none':
      break;
    case 'fade':
      res.o = clamp(a / D);
      break;
    case 'pop':
      res.s = spring01(a, 0.45, 0.3);
      res.o = clamp(a / 0.12);
      break;
    case 'stamp': {
      const k = clamp(a / 0.18);
      res.s = a < 0.18 ? lerp(2.2, 1, easeFn('in', k)) : 1 + 0.04 * Math.exp(-(a - 0.18) * 12) * Math.sin((a - 0.18) * 40);
      res.o = clamp(a / 0.08);
      break;
    }
    case 'drop':
      res.dy = -260 * (1 - easeFn('out', clamp(a / 0.5)));
      res.o = clamp(a / 0.15);
      break;
    case 'rise':
      res.dy = 80 * (1 - easeFn('out', clamp(a / D)));
      res.o = clamp(a / D);
      break;
    case 'slideL':
      res.dx = -500 * (1 - easeFn('out', clamp(a / 0.6)));
      res.o = clamp(a / 0.2);
      break;
    case 'slideR':
      res.dx = 500 * (1 - easeFn('out', clamp(a / 0.6)));
      res.o = clamp(a / 0.2);
      break;
    case 'grow':
      res.s = easeFn('out', clamp(a / D));
      res.o = clamp(a / 0.1);
      break;
    case 'draw':
      res.r = easeFn('inOut', clamp(a / ((el.dur as number) ?? 1.2)));
      break;
  }
  if (t > tout) {
    const b = clamp((t - tout) / 0.35);
    const ex = el.exit ?? 'fade';
    if (ex === 'none') return { ...res, visible: false, o: 0 };
    res.o *= 1 - b;
    if (ex === 'pop' || ex === 'grow') res.s *= 1 - easeFn('in', b);
    if (ex === 'drop') res.dy += 300 * easeFn('in', b);
    if (ex === 'rise') res.dy -= 120 * b;
    if (ex === 'slideL') res.dx -= 600 * easeFn('in', b);
    if (ex === 'slideR') res.dx += 600 * easeFn('in', b);
  }
  return res;
}

/** Points along a polyline for a fraction r (0..1) of its length. Returns partial path + tip + tangent angle. */
export function partialPolyline(pts: [number, number][], r: number) {
  if (pts.length < 2) return { pts, tip: pts[0] ?? [0, 0], angle: 0 };
  const segs: number[] = [];
  let total = 0;
  for (let i = 1; i < pts.length; i++) {
    const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    segs.push(d);
    total += d;
  }
  let want = total * clamp(r);
  const out: [number, number][] = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    const d = segs[i - 1];
    if (want >= d) {
      out.push(pts[i]);
      want -= d;
    } else {
      const k = d === 0 ? 0 : want / d;
      out.push([lerp(pts[i - 1][0], pts[i][0], k), lerp(pts[i - 1][1], pts[i][1], k)]);
      break;
    }
  }
  const a = out[Math.max(0, out.length - 2)];
  const b = out[out.length - 1];
  return { pts: out, tip: b, angle: Math.atan2(b[1] - a[1], b[0] - a[0]), total };
}

/** Smooth a sparse polyline with Catmull-Rom into many points. */
export function smoothPath(pts: [number, number][], steps = 12): [number, number][] {
  if (pts.length < 3) {
    if (pts.length === 2) {
      const out: [number, number][] = [];
      for (let i = 0; i <= steps; i++) out.push([lerp(pts[0][0], pts[1][0], i / steps), lerp(pts[0][1], pts[1][1], i / steps)]);
      return out;
    }
    return pts;
  }
  const out: [number, number][] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    for (let s = 0; s < steps; s++) {
      const t = s / steps, t2 = t * t, t3 = t2 * t;
      const f = (a: number, b: number, c: number, d: number) =>
        0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t2 + (-a + 3 * b - 3 * c + d) * t3);
      out.push([f(p0[0], p1[0], p2[0], p3[0]), f(p0[1], p1[1], p2[1], p3[1])]);
    }
  }
  out.push(pts[pts.length - 1]);
  return out;
}

export const toD = (pts: [number, number][]) => pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join('');
