/**
 * Depth model for stage scenes: a ground plane seen by a camera.
 *
 * A scene may declare `world: { horizon, y, scale, vehicles }`:
 *   - horizon: screen y of the horizon (defaults per set kind, see SET_HORIZON);
 *   - y, scale: the reference person — an actor whose feet are at `y` has scale `scale` (default 900 / 1.45);
 *   - vehicles: global multiplier on vehicle sizes (default 1; stylisation knob).
 * Then every actor / vehicle / crowd WITHOUT an explicit `scale` is sized from its ground y:
 *   personScale(y) = scale * (y - horizon) / (refY - horizon)
 * and a vehicle gets the size it should have next to a person standing at the same y (VEH table).
 * Keyframing y therefore makes things grow as they come toward the camera.
 */

/** actor height (head top → feet) in px at scale 1 */
export const PERSON_H = 300;

/**
 * Vehicle drawings at scale 1 (measured from renders) and their target size in PERSON HEIGHTS.
 * Ground vehicles are matched by height, aircraft and boats by length. Not real-world exact:
 * vehicles are ~25 % compressed so chibi people still read next to them, but the proportions stay believable.
 */
export const VEH: Record<string, { h: number; L: number; by: 'h' | 'L'; target: number }> = {
  sherman: { h: 203, L: 481, by: 'h', target: 1.15 },
  tank: { h: 193, L: 501, by: 'h', target: 1.12 },
  tank_flat: { h: 193, L: 501, by: 'h', target: 1.12 },
  tiger: { h: 213, L: 585, by: 'h', target: 1.22 },
  panther: { h: 197, L: 585, by: 'h', target: 1.18 },
  panzer4: { h: 187, L: 525, by: 'h', target: 1.08 },
  t34: { h: 185, L: 511, by: 'h', target: 1.05 },
  stug: { h: 156, L: 485, by: 'h', target: 0.9 },
  markiv: { h: 222, L: 568, by: 'h', target: 1.3 },
  renault: { h: 196, L: 290, by: 'h', target: 1.1 },
  halftrack: { h: 158, L: 397, by: 'h', target: 0.98 },
  truck: { h: 211, L: 425, by: 'h', target: 1.32 },
  jeep: { h: 155, L: 287, by: 'h', target: 0.82 },
  car: { h: 155, L: 287, by: 'h', target: 0.85 },
  artillery: { h: 140, L: 414, by: 'h', target: 0.78 },
  gun: { h: 140, L: 414, by: 'h', target: 0.78 },
  train: { h: 209, L: 395, by: 'h', target: 1.8 },
  locomotive: { h: 209, L: 395, by: 'h', target: 1.8 },
  wagon: { h: 209, L: 395, by: 'h', target: 1.7 },
  traincar: { h: 209, L: 395, by: 'h', target: 1.7 },
  horse: { h: 217, L: 275, by: 'h', target: 1.05 },
  cart: { h: 217, L: 462, by: 'h', target: 1.05 },
  fighter: { h: 120, L: 320, by: 'L', target: 3.6 },
  plane: { h: 120, L: 320, by: 'L', target: 3.6 },
  divebomber: { h: 120, L: 320, by: 'L', target: 4.0 },
  bomber: { h: 175, L: 509, by: 'L', target: 7.0 },
  dakota: { h: 199, L: 656, by: 'L', target: 7.0 },
  transport: { h: 199, L: 656, by: 'L', target: 7.0 },
  glider: { h: 135, L: 576, by: 'L', target: 7.0 },
  boat: { h: 171, L: 259, by: 'L', target: 2.4 },
  assaultboat: { h: 91, L: 302, by: 'L', target: 2.6 },
};

/** where the ground meets the sky in each set (screen y at camera zoom 1) */
export const SET_HORIZON: Record<string, number> = {
  field: 600, countryside: 600, steppe: 600, snow: 600, desert: 600, mud: 600,
  polder: 620, heath: 600, airfield: 620, river: 470, beach: 520, sea: 560, ocean: 560,
  harbor: 560, dock: 560, railway: 640, station: 640, trench: 420, nomansland: 560, jungle: 500,
  city: 760, street: 760, ruins: 760, archbridge: 560, garden: 600, hotel: 640,
};

/** effects that happen ON the ground at their y: in a `world` scene they are sorted with people (a burst behind a man
 *  is drawn behind him) and sized by depth: native size at the world's reference y, smaller further back */
export const GROUND_FX = new Set(['shellburst', 'explosion', 'impact', 'dust', 'smoke', 'fire', 'splash']);

export type World = { horizon?: number; y?: number; scale?: number; vehicles?: number };
export type WorldCtx = { horizon: number; y: number; scale: number; vehicles: number };

export const resolveWorld = (w: World | undefined, set?: { kind?: string; horizon?: unknown; dyke?: unknown }): WorldCtx | undefined => {
  if (!w) return undefined;
  const kind = set?.kind ?? '';
  const hz = w.horizon ?? (typeof set?.horizon === 'number' ? set.horizon : typeof set?.dyke === 'number' ? set.dyke : SET_HORIZON[kind] ?? 560);
  return { horizon: hz, y: w.y ?? 900, scale: w.scale ?? 1.45, vehicles: w.vehicles ?? 1 };
};

/** actor scale for feet at screen y */
export const personScaleAt = (w: WorldCtx, y: number) => Math.max(0.03, (w.scale * (y - w.horizon)) / Math.max(1, w.y - w.horizon));

/** vehicle scale that matches a person of scale `ps` standing at the same depth */
export const vehicleScaleFor = (type: string, ps: number, mult = 1) => {
  const v = VEH[type];
  if (!v) return ps * 0.6 * mult;
  const native = v.by === 'h' ? v.h : v.L;
  return ((v.target * PERSON_H * ps) / native) * mult;
};
