import React from 'react';
import { INK, FONT } from '../theme';
import { rnd } from '../lib/anim';
import { Flag } from '../props/Props';

/**
 * Set KIT: places assembled from modules instead of fixed backgrounds, so every film can build the rooms and streets its
 * story needs (a turnip-winter kitchen, a ration office, a dugout, a bakery with empty shelves, a snowy street with a queue).
 *
 *   {"kind": "room", "style": "kitchen", "items": ["shelf:empty", "window:snow_street", "clock", "stove"], "light": "candle", "poor": true}
 *   {"kind": "town", "style": "german", "buildings": ["house", "shop:bakery", "tenement", "church"], "items": ["lamppost", "poster"], "ground": "snow"}
 *
 * Everything has a default: {"kind": "room", "style": "kitchen"} alone is a finished kitchen. Modules are laid out left to
 * right along the back wall / the street unless an item gives its own x. The writer-facing vocabulary is generated from the
 * tables below into recipes/STAGECRAFT.md (tools/catalog.py) — keep the comments on each entry short and concrete.
 */
type P = { kind: string; t: number; time?: string; [k: string]: unknown };
type Item = { item: string; x?: number; w?: number; [k: string]: unknown };

const X0 = -240, Y0 = -160, W = 2400, H = 1400;
const SKY: Record<string, [string, string]> = { day: ['#9fcbe3', '#dcecf0'], dawn: ['#c9a6c8', '#f6cf9e'], dusk: ['#6a5a8a', '#f0a070'], night: ['#0d1730', '#26385a'] };
const dark = (hex: string, k: number) => {
  const n = parseInt(hex.slice(1), 16);
  const f = (v: number) => Math.max(0, Math.min(255, Math.round(v * (1 + k))));
  return '#' + [f(n >> 16), f((n >> 8) & 255), f(n & 255)].map((v) => v.toString(16).padStart(2, '0')).join('');
};
const asItem = (it: unknown): Item => {
  if (typeof it === 'string') {
    const [item, arg, arg2] = it.split(':');
    return { item, arg, arg2 };
  }
  const o = { ...(it as Item) };
  if (o.item && o.item.includes(':')) { const [item, arg, arg2] = o.item.split(':'); return { ...o, item, arg: o.arg ?? arg, arg2: o.arg2 ?? arg2 }; }
  return o;
};

// =====================================================================================================================
// ROOM
// =====================================================================================================================
/** room styles: wall, floor and the modules a room of that kind has by default */
export const ROOM_STYLES: Record<string, { wall: string; color: string; floor: string; floorColor: string; items: string[]; light: string; beams?: boolean; poor?: boolean; doc: string }> = {
  kitchen: { wall: 'plaster', color: '#e2cf9e', floor: 'boards', floorColor: '#8a6a4a', items: ['shelf:jars', 'window', 'clock', 'stove'], light: 'window', doc: 'family kitchen: jar shelf, window, clock, iron stove' },
  tenement: { wall: 'plaster', color: '#cdbf9f', floor: 'boards', floorColor: '#6e5a44', items: ['hooks', 'window:small', 'bed', 'stove'], light: 'candle', poor: true, doc: 'one-room flat of the poor: cracked plaster, bed, small stove' },
  parlour: { wall: 'paper', color: '#b99a80', floor: 'carpet', floorColor: '#6a3e32', items: ['photos', 'window', 'portrait', 'clock'], light: 'lamp', doc: 'middle-class sitting room: wallpaper, portrait, photos' },
  farmhouse: { wall: 'plank', color: '#9a7350', floor: 'earth', floorColor: '#7a6248', items: ['shelf:plates', 'fireplace', 'window:small', 'sacks'], light: 'fire', beams: true, doc: 'farm kitchen: hearth fire, beams, sacks' },
  shop: { wall: 'plank', color: '#b99568', floor: 'boards', floorColor: '#7a5a3a', items: ['shelf:tins', 'sign', 'shelf:jars', 'sacks'], light: 'window', doc: 'grocer: shelves behind the counter (add a counter thing)' },
  bakery: { wall: 'tile', color: '#e9e2cf', floor: 'tile', floorColor: '#b8ab92', items: ['shelf:bread', 'oven', 'shelf:bread'], light: 'fire', doc: 'bakery: bread shelves and a brick oven' },
  office: { wall: 'paper', color: '#cdb98f', floor: 'boards', floorColor: '#6b4a32', items: ['cabinet', 'map', 'window', 'portrait'], light: 'window', doc: 'official office: map, cabinet, window' },
  ministry: { wall: 'panel', color: '#d8c8a0', floor: 'parquet', floorColor: '#7a5434', items: ['window:tall', 'portrait', 'clock', 'window:tall'], light: 'window', doc: 'grand government room: tall windows, portrait (add flag:<NATION> for a flag)' },
  admiralty: { wall: 'panel', color: '#c9c2a8', floor: 'parquet', floorColor: '#6a4a30', items: ['clock', 'map:sea', 'window:tall:sea'], light: 'window', doc: 'naval staff room: big sea chart, window on the sea' },
  food_office: { wall: 'paper', color: '#d4c7a2', floor: 'boards', floorColor: '#75583c', items: ['poster', 'drawers', 'clock', 'window'], light: 'window', doc: 'ration office: posters, filing drawers, clock' },
  ward: { wall: 'tile', color: '#e8ece6', floor: 'tile', floorColor: '#c9cfc6', items: ['window', 'beds', 'window'], light: 'window', doc: 'hospital ward: white tiles, row of beds' },
  barracks: { wall: 'plank', color: '#a98a62', floor: 'boards', floorColor: '#6e5a44', items: ['bunk', 'rifles', 'stove', 'bunk'], light: 'lamp', beams: true, doc: 'soldiers barracks: bunks, rifle rack, stove' },
  dugout: { wall: 'timber', color: '#6b5236', floor: 'duckboard', floorColor: '#4a3a2a', items: ['shelf:tins', 'map', 'bunk'], light: 'lantern', beams: true, doc: 'trench dugout: timber walls, duckboards, lantern' },
  cellar: { wall: 'stone', color: '#8f877a', floor: 'stone', floorColor: '#6a645a', items: ['barrels', 'arch', 'crates'], light: 'candle', doc: 'stone cellar / shelter: arch, barrels, candlelight' },
  warehouse: { wall: 'brick', color: '#9a5a44', floor: 'stone', floorColor: '#7a7266', items: ['sacks', 'door', 'crates', 'barrels'], light: 'window', doc: 'dock warehouse: sacks, crates, barrels, big door' },
  classroom: { wall: 'plaster', color: '#e6dcc0', floor: 'boards', floorColor: '#7a5a3a', items: ['map', 'blackboard', 'window'], light: 'window', doc: 'school room: blackboard, map' },
  church: { wall: 'stone', color: '#cfc6b4', floor: 'stone', floorColor: '#9a9284', items: ['stained', 'crucifix', 'stained'], light: 'candle', doc: 'church: stained glass, cross, candles' },
  tavern: { wall: 'plank', color: '#8a6038', floor: 'boards', floorColor: '#5a3e28', items: ['shelf:bottles', 'barrels', 'poster', 'window:small'], light: 'lamp', beams: true, doc: 'inn / bar: bottles, barrels, beams' },
};

/** room modules (back wall or standing on the floor against it) */
export const ROOM_ITEMS: Record<string, { w: number; doc: string }> = {
  window: { w: 330, doc: 'window:<view> view = street, snow_street, field, sea, harbor, city, ruins, garden, front, sky; window:small / window:tall' },
  door: { w: 220, doc: 'door (door:open shows the light outside)' },
  shelf: { w: 330, doc: 'wall shelf: shelf:jars | tins | bottles | books | bread | plates | empty (bare boards = scarcity)' },
  cupboard: { w: 260, doc: 'kitchen dresser with plates' },
  cabinet: { w: 230, doc: 'filing cabinet' },
  drawers: { w: 380, doc: 'wall of labelled drawers (archive / ration office)' },
  stove: { w: 250, doc: 'iron kitchen stove with a pot and a flue pipe (glows)' },
  fireplace: { w: 330, doc: 'hearth with a fire and a mantel' },
  oven: { w: 360, doc: 'brick baker\'s oven with fire' },
  bed: { w: 430, doc: 'iron bed with a blanket' },
  beds: { w: 980, doc: 'a row of three hospital beds' },
  bunk: { w: 320, doc: 'two-tier bunk' },
  clock: { w: 130, doc: 'wall clock (clock:HH:MM)' },
  portrait: { w: 210, doc: 'framed portrait (portrait:<nation> shows a flag)' },
  map: { w: 580, doc: 'wall map (map:sea = sea chart)' },
  poster: { w: 200, doc: 'printed notice; text from the item {"item": "poster", "text": "BREAD CARD"}' },
  flag: { w: 190, doc: 'flag on a pole (flag:<nation>; default the film side)' },
  calendar: { w: 150, doc: 'wall calendar; {"item": "calendar", "text": "1917"}' },
  photos: { w: 210, doc: 'family photos in frames' },
  crucifix: { w: 100, doc: 'a cross on the wall' },
  mirror: { w: 150, doc: 'small mirror' },
  hooks: { w: 230, doc: 'coat hooks with coats and a cap' },
  lamp: { w: 140, doc: 'hanging lamp from the ceiling (lights a pool)' },
  barrels: { w: 300, doc: 'stacked barrels' },
  crates: { w: 300, doc: 'stacked crates (crates:<stencil text>)' },
  sacks: { w: 300, doc: 'stacked grain sacks' },
  rifles: { w: 250, doc: 'rifle rack' },
  blackboard: { w: 620, doc: 'blackboard; {"item": "blackboard", "text": "1914"}' },
  sink: { w: 260, doc: 'stone sink with a hand pump' },
  cradle: { w: 230, doc: 'wooden cradle' },
  arch: { w: 380, doc: 'brick arch opening into darkness' },
  stained: { w: 250, doc: 'stained-glass window' },
  sign: { w: 480, doc: 'shop sign board; {"item": "sign", "text": "KOLONIALWAREN"}' },
  radio: { w: 180, doc: 'wireless set on a bracket' },
  pipes: { w: 0, doc: 'exposed pipes along the wall (cellar, factory office)' },
};

const WALL_BASE = 780;
const FLOOR_Y = WALL_BASE + 22; // where floor-standing modules stand

const layout = (items: Item[], x0 = 130, x1 = 1790) => {
  const ws = items.map((it) => (it.w as number) ?? ROOM_ITEMS[it.item]?.w ?? 200);
  const free = items.filter((it) => it.x === undefined && ws[items.indexOf(it)] > 0);
  const total = free.reduce((s, it) => s + ws[items.indexOf(it)], 0);
  const gap = Math.max(16, (x1 - x0 - total) / (free.length + 1));
  let x = x0 + gap;
  return items.map((it, i) => {
    if (it.x !== undefined) return it.x as number;
    if (ws[i] === 0) return 960;
    const cx = x + ws[i] / 2;
    x += ws[i] + gap;
    return cx;
  });
};

// ---------- the view through a window ----------
export const View: React.FC<{ view: string; x: number; y: number; w: number; h: number; time: string; weather?: string; t: number; id: string }> = ({ view, x, y, w, h, time, weather, t, id }) => {
  const [s0, s1] = SKY[time] ?? SKY.day;
  const night = time === 'night';
  const snowy = weather === 'snow' || view.startsWith('snow');
  const v = view.replace(/^snow_/, '').replace(/^rain_/, '');
  const base = y + h;
  const opp = night ? '#2a3448' : snowy ? '#a9a49a' : '#b49a7a';
  return (
    <g>
      <defs>
        <clipPath id={id}><rect x={x} y={y} width={w} height={h} /></clipPath>
        <linearGradient id={id + 'g'} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={s0} /><stop offset="1" stopColor={s1} /></linearGradient>
      </defs>
      <g clipPath={`url(#${id})`}>
        <rect x={x} y={y} width={w} height={h} fill={`url(#${id}g)`} />
        {night && v !== 'front' ? <circle cx={x + w * 0.72} cy={y + h * 0.2} r={12} fill="#f4f0d8" /> : null}
        {v === 'street' || v === 'city' || v === 'ruins' ? (
          <g>
            {Array.from({ length: 4 }, (_, i) => {
              const bx = x - 20 + i * (w / 3), bh = h * (0.45 + rnd(id, i) * 0.3), bw = w / 3 - 8;
              const ruin = v === 'ruins';
              return (
                <g key={i}>
                  <path d={ruin ? `M${bx} ${base} V${base - bh + 20} l${bw * 0.3} -20 l${bw * 0.2} 34 l${bw * 0.3} -26 l${bw * 0.2} 30 V${base} Z` : `M${bx} ${base} V${base - bh} l${bw / 2} -${v === 'street' ? 30 : 0} l${bw / 2} ${v === 'street' ? 30 : 0} V${base} Z`} fill={i % 2 ? opp : dark(opp, -0.08)} stroke={INK} strokeWidth={2} />
                  {snowy && !ruin ? <path d={`M${bx} ${base - bh} l${bw / 2} -30 l${bw / 2} 30 l-6 8 l${-bw / 2 + 6} -28 l${-bw / 2 + 6} 28 Z`} fill="#f2f4f6" /> : null}
                  {Array.from({ length: 4 }, (_, k) => <rect key={k} x={bx + 10 + (k % 2) * (bw / 2)} y={base - bh + 24 + Math.floor(k / 2) * 46} width={bw / 2 - 22} height={24} fill={night && rnd(id, i * 7 + k) > 0.5 ? '#f6d77a' : night ? '#1c2438' : '#7f9fb0'} />)}
                </g>
              );
            })}
            {snowy ? <rect x={x} y={base - 16} width={w} height={16} fill="#eef1f3" /> : null}
            {v === 'ruins' ? <path d={`M${x + w * 0.3} ${base - h * 0.5} q-20 -60 10 -110 q30 -40 0 -90`} stroke="#6a6a6a" strokeWidth={26} opacity={0.35} fill="none" strokeLinecap="round" /> : null}
          </g>
        ) : null}
        {v === 'field' || v === 'garden' || v === 'front' ? (
          <g>
            <path d={`M${x} ${y + h * 0.62} Q${x + w * 0.4} ${y + h * 0.5} ${x + w} ${y + h * 0.6} V${base} H${x} Z`} fill={snowy ? '#e8ecee' : night ? '#22303a' : v === 'front' ? '#7a6a52' : '#8db86a'} />
            <path d={`M${x} ${y + h * 0.78} Q${x + w * 0.6} ${y + h * 0.7} ${x + w} ${y + h * 0.8} V${base} H${x} Z`} fill={snowy ? '#dfe4e7' : night ? '#1a242c' : v === 'front' ? '#6a5a44' : '#76a458'} />
            {v === 'garden' ? [0.2, 0.7].map((k, i) => <g key={i}><rect x={x + w * k - 4} y={y + h * 0.45} width={8} height={h * 0.3} fill="#5a3e2a" /><circle cx={x + w * k} cy={y + h * 0.42} r={w * 0.12} fill={snowy ? '#e8ecee' : '#4f7a3a'} stroke={INK} strokeWidth={2} /></g>) : null}
            {v === 'front' ? [0.25, 0.6, 0.85].map((k, i) => { const f = Math.max(0, Math.sin(t * 2.3 + i * 2.1)) ** 8; return <circle key={i} cx={x + w * k} cy={y + h * 0.6} r={20 + f * 30} fill="#ffd27a" opacity={(night ? 0.6 : 0.25) * f} />; }) : null}
          </g>
        ) : null}
        {v === 'sea' || v === 'harbor' ? (
          <g>
            <rect x={x} y={y + h * 0.55} width={w} height={h * 0.45} fill={night ? '#16283e' : '#4f86a8'} />
            {Array.from({ length: 6 }, (_, i) => <path key={i} d={`M${x + ((rnd(id, i) * w + t * 8) % w)} ${y + h * (0.6 + i * 0.06)} q12 -4 24 0`} stroke="#fff" strokeOpacity={0.4} strokeWidth={2} fill="none" />)}
            <g transform={`translate(${x + ((t * 6 + w * 0.3) % (w + 120)) - 60} ${y + h * 0.55})`}>
              <path d="M-40 0 L40 0 L32 10 L-34 10 Z M-14 0 V-16 H10 V0 M-2 -16 V-28" fill="#3a3f48" stroke="#3a3f48" strokeWidth={3} />
            </g>
            {v === 'harbor' ? <path d={`M${x + w * 0.15} ${y + h * 0.55} V${y + h * 0.18} L${x + w * 0.42} ${y + h * 0.24} M${x + w * 0.15} ${y + h * 0.3} L${x + w * 0.3} ${y + h * 0.55}`} stroke={INK} strokeWidth={5} fill="none" /> : null}
          </g>
        ) : null}
        {snowy ? Array.from({ length: 22 }, (_, i) => {
          const fx = x + ((rnd(id + 's', i) * w + Math.sin(t * 0.8 + i) * 12) % w);
          const fy = y + ((rnd(id + 'y', i) * h + t * (26 + rnd(id, i) * 20)) % h);
          return <circle key={i} cx={fx} cy={fy} r={2.4 + rnd(id, i + 9) * 2} fill="#fff" opacity={0.9} />;
        }) : null}
        {weather === 'rain' || view.startsWith('rain') ? Array.from({ length: 16 }, (_, i) => {
          const fx = x + ((rnd(id + 'r', i) * w) % w), fy = y + ((rnd(id + 'q', i) * h + t * 400) % h);
          return <line key={i} x1={fx} y1={fy} x2={fx - 6} y2={fy + 22} stroke="#dfe8f0" strokeWidth={2} opacity={0.7} />;
        }) : null}
      </g>
    </g>
  );
};

const WindowM: React.FC<{ x: number; y: number; w: number; h: number; view: string; time: string; weather?: string; t: number; id: string; curtains?: string; frost?: boolean }> = ({ x, y, w, h, view, time, weather, t, id, curtains, frost }) => (
  <g>
    <rect x={x - 14} y={y - 14} width={w + 28} height={h + 28} fill="#5a4030" stroke={INK} strokeWidth={4} />
    <View view={view} x={x} y={y} w={w} h={h} time={time} weather={weather} t={t} id={id} />
    {frost ? <path d={`M${x} ${y + h} q${w * 0.2} -40 ${w * 0.3} 0 M${x + w} ${y + h} q${-w * 0.25} -50 ${-w * 0.35} 0 M${x} ${y} q30 30 0 60`} stroke="#ffffff" strokeWidth={10} opacity={0.6} fill="none" strokeLinecap="round" /> : null}
    <path d={`M${x + w / 2} ${y} V${y + h} M${x} ${y + h * 0.42} H${x + w}`} stroke="#efe6d2" strokeWidth={9} />
    <rect x={x} y={y} width={w} height={h} fill="none" stroke="#efe6d2" strokeWidth={10} />
    <rect x={x - 22} y={y + h + 10} width={w + 44} height={18} fill="#cdbb9a" stroke={INK} strokeWidth={3} />
    {curtains ? (
      <g fill={curtains} stroke={INK} strokeWidth={3}>
        <path d={`M${x - 40} ${y - 30} H${x + 22} Q${x + 6} ${y + h * 0.5} ${x + 26} ${y + h + 26} H${x - 40} Z`} />
        <path d={`M${x + w + 40} ${y - 30} H${x + w - 22} Q${x + w - 6} ${y + h * 0.5} ${x + w - 26} ${y + h + 26} H${x + w + 40} Z`} />
        <rect x={x - 50} y={y - 40} width={w + 100} height={14} fill="#6a4a2a" />
      </g>
    ) : null}
  </g>
);

const Shelf: React.FC<{ x: number; y: number; w: number; what: string; seed: string }> = ({ x, y, w, what, seed }) => {
  const rows = [0, 1];
  const L = x - w / 2;
  const thing = (k: number, cx: number, by: number) => {
    const r = rnd(seed, k);
    switch (what) {
      case 'jars': return <g key={k}><rect x={cx - 16} y={by - 44 - r * 10} width={32} height={44 + r * 10} rx={6} fill={['#c98a42', '#9a5a3a', '#d9c49a', '#8a9a5a'][k % 4]} stroke={INK} strokeWidth={2.5} /><rect x={cx - 18} y={by - 52 - r * 10} width={36} height={10} fill="#e9dcc2" stroke={INK} strokeWidth={2} /></g>;
      case 'tins': return <g key={k}><rect x={cx - 15} y={by - 38} width={30} height={38} fill={['#b8392e', '#3a6a8a', '#d9b35a', '#5a7a4a'][k % 4]} stroke={INK} strokeWidth={2.5} /><rect x={cx - 15} y={by - 28} width={30} height={12} fill="#f2ead8" /></g>;
      case 'bottles': return <path key={k} d={`M${cx - 11} ${by} V${by - 40} Q${cx - 11} ${by - 50} ${cx - 4} ${by - 54} V${by - 68} H${cx + 4} V${by - 54} Q${cx + 11} ${by - 50} ${cx + 11} ${by - 40} V${by} Z`} fill={['#3f6a3a', '#6a3a2a', '#8a8a4a'][k % 3]} stroke={INK} strokeWidth={2.5} />;
      case 'books': return <rect key={k} x={cx - 12} y={by - 60 + r * 12} width={22} height={60 - r * 12} fill={['#8b2e2e', '#2e4a6b', '#4f6b3a', '#a8873a'][k % 4]} stroke={INK} strokeWidth={2} />;
      case 'bread': return <path key={k} d={`M${cx - 30} ${by} Q${cx - 32} ${by - 26} ${cx} ${by - 28} Q${cx + 32} ${by - 26} ${cx + 30} ${by} Z`} fill="#c98a42" stroke={INK} strokeWidth={2.5} />;
      case 'plates': return <g key={k}><ellipse cx={cx} cy={by - 30} rx={26} ry={30} fill="#f2ede2" stroke={INK} strokeWidth={2.5} /><ellipse cx={cx} cy={by - 30} rx={14} ry={16} fill="none" stroke="#6a8ab0" strokeWidth={2} /></g>;
      case 'sacks': return <path key={k} d={`M${cx - 26} ${by} Q${cx - 34} ${by - 40} ${cx - 14} ${by - 52} L${cx + 14} ${by - 52} Q${cx + 34} ${by - 40} ${cx + 26} ${by} Z`} fill="#cdb892" stroke={INK} strokeWidth={2.5} />;
      default: return null;
    }
  };
  const per = what === 'empty' ? 0 : what === 'bread' ? Math.floor(w / 74) : what === 'plates' ? Math.floor(w / 62) : what === 'sacks' ? Math.floor(w / 70) : Math.floor(w / 44);
  return (
    <g>
      {rows.map((r) => {
        const by = y + r * 120;
        return (
          <g key={r}>
            {Array.from({ length: per }, (_, i) => (what === 'empty' && i > 0) || rnd(seed, r * 31 + i) < (what === 'jars' ? 0.18 : 0.06) ? null : thing(r * 31 + i, L + 30 + i * ((w - 60) / Math.max(1, per - 1)), by))}
            <rect x={L} y={by} width={w} height={14} fill="#7a5232" stroke={INK} strokeWidth={3} />
            <path d={`M${L + 20} ${by + 14} l14 26 M${L + w - 20} ${by + 14} l-14 26`} stroke={INK} strokeWidth={5} />
          </g>
        );
      })}
      {what === 'empty' ? <path d={`M${L + 40} ${y - 4} q30 -6 60 0 M${L + w - 90} ${y + 116} q20 -4 40 0`} stroke="#8a7a62" strokeWidth={3} fill="none" opacity={0.6} /> : null}
    </g>
  );
};

const Bricks2: React.FC<{ x: number; y: number; w: number; h: number; c: string; seed: string; rowH?: number }> = ({ x, y, w, h, c, seed, rowH = 34 }) => {
  const rows = Math.ceil(h / rowH);
  return (
    <g>
      <rect x={x} y={y} width={w} height={h} fill={dark(c, -0.25)} />
      {Array.from({ length: rows }, (_, r) => Array.from({ length: Math.ceil(w / 76) + 1 }, (_, i) => (
        <rect key={r * 999 + i} x={x + i * 76 - (r % 2) * 38} y={y + r * rowH + 2} width={72} height={rowH - 4} fill={dark(c, (rnd(seed, r * 97 + i) - 0.5) * 0.16)} />
      )))}
    </g>
  );
};

const RoomWall: React.FC<{ type: string; color: string; poor?: boolean; seed: string }> = ({ type, color, poor, seed }) => {
  const h = WALL_BASE - Y0;
  let body: React.ReactNode = null;
  switch (type) {
    case 'brick': body = <Bricks2 x={X0} y={Y0} w={W} h={h} c={color} seed={seed} />; break;
    case 'stone': body = (
      <g>
        <rect x={X0} y={Y0} width={W} height={h} fill={dark(color, -0.3)} />
        {Array.from({ length: Math.ceil(h / 70) }, (_, r) => {
          let x = X0 - rnd(seed, r) * 80;
          const out: React.ReactNode[] = [];
          for (let i = 0; x < X0 + W; i++) {
            const bw = 90 + rnd(seed, r * 53 + i) * 110;
            out.push(<rect key={i} x={x + 3} y={Y0 + r * 70 + 3} width={bw - 6} height={64} rx={12} fill={dark(color, (rnd(seed, r * 71 + i) - 0.5) * 0.18)} />);
            x += bw;
          }
          return <g key={r}>{out}</g>;
        })}
      </g>
    ); break;
    case 'plank': body = (
      <g>
        <rect x={X0} y={Y0} width={W} height={h} fill={color} />
        {Array.from({ length: 30 }, (_, i) => <g key={i}><line x1={X0 + i * 84} y1={Y0} x2={X0 + i * 84} y2={WALL_BASE} stroke="#000" opacity={0.18} strokeWidth={4} />{rnd(seed, i) > 0.6 ? <ellipse cx={X0 + i * 84 + 40} cy={Y0 + 200 + rnd(seed, i + 5) * 600} rx={7} ry={11} fill="#000" opacity={0.12} /> : null}</g>)}
      </g>
    ); break;
    case 'timber': body = (
      <g>
        <rect x={X0} y={Y0} width={W} height={h} fill={dark(color, -0.2)} />
        {Array.from({ length: Math.ceil(h / 62) }, (_, r) => <rect key={r} x={X0} y={Y0 + r * 62 + 3} width={W} height={56} rx={22} fill={dark(color, (rnd(seed, r) - 0.5) * 0.2)} stroke={INK} strokeWidth={2} strokeOpacity={0.4} />)}
        {[-80, 520, 1400, 2000].map((x, i) => <rect key={i} x={x} y={Y0} width={46} height={h} fill={dark(color, -0.32)} stroke={INK} strokeWidth={3} />)}
      </g>
    ); break;
    case 'tile': body = (
      <g>
        <rect x={X0} y={Y0} width={W} height={h} fill={color} />
        <rect x={X0} y={WALL_BASE - 360} width={W} height={360} fill="#f4f4ee" />
        {Array.from({ length: 9 }, (_, r) => <line key={'r' + r} x1={X0} y1={WALL_BASE - 360 + r * 40} x2={X0 + W} y2={WALL_BASE - 360 + r * 40} stroke="#9aa6a8" strokeWidth={2} />)}
        {Array.from({ length: 60 }, (_, i) => <line key={'c' + i} x1={X0 + i * 40} y1={WALL_BASE - 360} x2={X0 + i * 40} y2={WALL_BASE} stroke="#9aa6a8" strokeWidth={2} />)}
        <rect x={X0} y={WALL_BASE - 366} width={W} height={10} fill="#6a8a8a" />
      </g>
    ); break;
    case 'paper': body = (
      <g>
        <rect x={X0} y={Y0} width={W} height={h} fill={color} />
        {Array.from({ length: 40 }, (_, i) => <line key={i} x1={X0 + i * 60} y1={Y0} x2={X0 + i * 60} y2={WALL_BASE} stroke="#000" opacity={0.05} strokeWidth={14} />)}
        {Array.from({ length: 160 }, (_, i) => <path key={'m' + i} transform={`translate(${X0 + 30 + (i % 40) * 60} ${Y0 + 60 + Math.floor(i / 40) * 190 + (i % 2) * 95})`} d="M0 -9 L6 0 L0 9 L-6 0 Z" fill="#fff" opacity={0.18} />)}
        <rect x={X0} y={WALL_BASE - 250} width={W} height={12} fill="#6a4a30" />
      </g>
    ); break;
    case 'panel': body = (
      <g>
        <rect x={X0} y={Y0} width={W} height={h} fill={color} />
        <rect x={X0} y={WALL_BASE - 280} width={W} height={280} fill="#7a5a3a" />
        {Array.from({ length: 16 }, (_, i) => <rect key={i} x={X0 + 30 + i * 160} y={WALL_BASE - 250} width={120} height={210} fill="none" stroke="#000" opacity={0.15} strokeWidth={5} />)}
        <rect x={X0} y={WALL_BASE - 290} width={W} height={14} fill="#000" opacity={0.2} />
        <rect x={X0} y={Y0} width={W} height={60} fill="#000" opacity={0.06} />
      </g>
    ); break;
    case 'concrete': body = (
      <g>
        <rect x={X0} y={Y0} width={W} height={h} fill={color} />
        {Array.from({ length: 8 }, (_, r) => <line key={r} x1={X0} y1={Y0 + r * 120} x2={X0 + W} y2={Y0 + r * 120} stroke="#000" opacity={0.08} strokeWidth={3} />)}
      </g>
    ); break;
    default: body = (
      <g>
        <rect x={X0} y={Y0} width={W} height={h} fill={color} />
        {Array.from({ length: 7 }, (_, i) => <ellipse key={i} cx={X0 + rnd(seed, i) * W} cy={Y0 + 200 + rnd(seed, i + 3) * 500} rx={220} ry={120} fill="#000" opacity={0.035} />)}
      </g>
    );
  }
  return (
    <g>
      {body}
      {poor ? (
        <g>
          {[0, 1, 2].map((i) => {
            const cx = X0 + 300 + rnd(seed + 'p', i) * 1900, cy = Y0 + 300 + rnd(seed + 'q', i) * 420;
            return (
              <g key={i}>
                <path d={`M${cx - 70} ${cy} q20 -50 70 -40 q60 -10 70 30 q10 50 -40 60 q-60 20 -100 -50 Z`} fill={dark(color, -0.12)} stroke={INK} strokeWidth={2.5} />
                {[0, 1, 2].map((k) => <rect key={k} x={cx - 50 + k * 34 - (k % 2) * 10} y={cy - 20 + (k % 2) * 22} width={30} height={16} fill="#a8624a" opacity={0.7} />)}
              </g>
            );
          })}
          <path d={`M${X0 + 900} ${Y0 + 160} l30 60 l-20 40 l40 70 l-10 50 M${X0 + 1700} ${WALL_BASE - 60} l-30 -60 l20 -50 l-30 -40`} stroke={INK} strokeWidth={3} fill="none" opacity={0.55} />
          <ellipse cx={X0 + 500} cy={Y0 + 160} rx={160} ry={60} fill="#7a6a3a" opacity={0.12} />
        </g>
      ) : null}
      <rect x={X0} y={WALL_BASE - 24} width={W} height={24} fill="#4a3424" />
    </g>
  );
};

const RoomFloor: React.FC<{ type: string; color: string; seed: string }> = ({ type, color, seed }) => {
  const y = WALL_BASE, h = Y0 + H - y;
  let pattern: React.ReactNode = null;
  if (type === 'boards' || type === 'duckboard') pattern = Array.from({ length: 24 }, (_, i) => <line key={i} x1={X0 + i * 110} y1={y} x2={X0 + i * 110 - 180} y2={Y0 + H} stroke="#000" opacity={type === 'duckboard' ? 0.3 : 0.1} strokeWidth={type === 'duckboard' ? 12 : 4} />);
  if (type === 'tile') pattern = Array.from({ length: 10 * 30 }, (_, i) => { const r = Math.floor(i / 30), c = i % 30; return (r + c) % 2 ? <rect key={i} x={X0 + c * 90 - r * 14} y={y + r * 48} width={90} height={48} fill="#000" opacity={0.08} /> : null; });
  if (type === 'stone') pattern = Array.from({ length: 7 }, (_, r) => Array.from({ length: 16 }, (_, c) => <rect key={r * 99 + c} x={X0 + c * 170 - (r % 2) * 80 + rnd(seed, r * 9 + c) * 10} y={y + 6 + r * 66} width={162} height={58} rx={10} fill="#000" opacity={0.04 + rnd(seed, r * 13 + c) * 0.05} />));
  if (type === 'parquet') pattern = Array.from({ length: 60 }, (_, i) => <line key={i} x1={X0 + i * 60} y1={y} x2={X0 + i * 60 + (i % 2 ? 40 : -40)} y2={Y0 + H} stroke="#000" opacity={0.1} strokeWidth={3} />);
  if (type === 'earth') pattern = Array.from({ length: 40 }, (_, i) => <ellipse key={i} cx={X0 + rnd(seed, i) * W} cy={y + 20 + rnd(seed, i + 40) * (h - 40)} rx={10 + rnd(seed, i) * 18} ry={4} fill="#000" opacity={0.12} />);
  return (
    <g>
      <rect x={X0} y={y} width={W} height={h} fill={color} />
      {pattern}
      {type === 'carpet' ? <g><rect x={420} y={y + 90} width={1080} height={260} rx={10} fill="#8a2e2e" stroke={INK} strokeWidth={4} /><rect x={450} y={y + 112} width={1020} height={216} rx={8} fill="none" stroke="#d9b35a" strokeWidth={6} /></g> : null}
      <rect x={X0} y={y} width={W} height={10} fill="#000" opacity={0.18} />
    </g>
  );
};

const RoomItem: React.FC<{ it: Item; x: number; p: P; i: number; nationKey?: string }> = ({ it, x, p, i, nationKey }) => {
  const t = p.t, time = (p.time as string) ?? 'day', night = time === 'night';
  const arg = (it.arg as string) ?? '';
  const seed = 'ri' + i;
  const text = it.text as string | undefined;
  switch (it.item) {
    case 'window': {
      const sized = arg === 'small' || arg === 'tall';
      const size = sized ? arg : ((it.size as string) ?? '');
      const small = size === 'small', tall = size === 'tall';
      const view = (it.view as string) || (sized ? (it.arg2 as string) : arg) || (p.view as string) || 'street';
      const w = small ? 210 : tall ? 250 : 300, h = small ? 240 : tall ? 500 : 340, y = tall ? 110 : small ? 250 : 170;
      return <WindowM x={x - w / 2} y={y} w={w} h={h} view={view} time={time} weather={p.weather as string} t={t} id={`kw${i}_${String(p.style ?? 'r')}`} curtains={(it.curtains as string) ?? (p.poor ? undefined : '#8a3a2e')} frost={p.weather === 'snow' || p.cold === true} />;
    }
    case 'door': {
      const open = arg === 'open' || it.open === true;
      return (
        <g>
          <rect x={x - 110} y={WALL_BASE - 430} width={220} height={430} fill="#4a3424" stroke={INK} strokeWidth={4} />
          {open ? <g><rect x={x - 96} y={WALL_BASE - 418} width={192} height={418} fill={night ? '#1c2438' : '#f3e6c0'} /><path d={`M${x - 96} ${WALL_BASE - 418} L${x - 160} ${WALL_BASE - 440} L${x - 160} ${WALL_BASE + 30} L${x - 96} ${WALL_BASE}`} fill="#7a5232" stroke={INK} strokeWidth={4} /></g> : (
            <g><rect x={x - 96} y={WALL_BASE - 418} width={192} height={418} fill="#7a5232" stroke={INK} strokeWidth={3} /><rect x={x - 76} y={WALL_BASE - 396} width={152} height={160} fill="none" stroke="#000" opacity={0.2} strokeWidth={5} /><rect x={x - 76} y={WALL_BASE - 210} width={152} height={180} fill="none" stroke="#000" opacity={0.2} strokeWidth={5} /><circle cx={x + 70} cy={WALL_BASE - 210} r={9} fill="#d9b35a" stroke={INK} strokeWidth={2} /></g>
          )}
        </g>
      );
    }
    case 'shelf': return <Shelf x={x} y={300} w={300} what={arg || (it.what as string) || 'jars'} seed={seed} />;
    case 'cupboard': return (
      <g>
        <rect x={x - 120} y={FLOOR_Y - 420} width={240} height={420} fill="#7a5232" stroke={INK} strokeWidth={4} />
        <Shelf x={x} y={FLOOR_Y - 300} w={200} what="plates" seed={seed} />
        <rect x={x - 110} y={FLOOR_Y - 150} width={220} height={140} fill="#6a4428" stroke={INK} strokeWidth={3} />
        <path d={`M${x} ${FLOOR_Y - 150} V${FLOOR_Y - 10}`} stroke={INK} strokeWidth={3} />
      </g>
    );
    case 'cabinet': return (
      <g>
        <rect x={x - 105} y={FLOOR_Y - 380} width={210} height={380} fill="#7a7468" stroke={INK} strokeWidth={4} />
        {[0, 1, 2, 3].map((r) => <g key={r}><rect x={x - 90} y={FLOOR_Y - 366 + r * 92} width={180} height={80} fill="#8a8478" stroke={INK} strokeWidth={3} /><rect x={x - 22} y={FLOOR_Y - 336 + r * 92} width={44} height={10} rx={4} fill="#d9c49a" stroke={INK} strokeWidth={2} /></g>)}
      </g>
    );
    case 'drawers': {
      const labels = (it.labels as string[]) ?? [];
      return (
        <g>
          <rect x={x - 180} y={170} width={360} height={440} fill="#6a4428" stroke={INK} strokeWidth={4} />
          {Array.from({ length: 24 }, (_, k) => { const r = Math.floor(k / 4), c = k % 4; return <g key={k}><rect x={x - 168 + c * 86} y={182 + r * 70} width={78} height={60} fill="#8a5a36" stroke={INK} strokeWidth={2.5} /><rect x={x - 156 + c * 86} y={190 + r * 70} width={54} height={18} fill="#f2ead8" stroke={INK} strokeWidth={1.5} />{labels[k] ? <text x={x - 129 + c * 86} y={204 + r * 70} textAnchor="middle" fontFamily={FONT.cond} fontSize={13} fontWeight={700} fill={INK}>{labels[k]}</text> : null}<circle cx={x - 129 + c * 86} cy={226 + r * 70} r={5} fill="#d9c49a" stroke={INK} strokeWidth={1.5} /></g>; })}
        </g>
      );
    }
    case 'stove': {
      const glow = 0.55 + 0.25 * Math.sin(t * 6.3) + 0.1 * Math.sin(t * 11);
      const cold = arg === 'cold' || p.cold === true;
      return (
        <g>
          <rect x={x - 18} y={-160} width={36} height={FLOOR_Y - 380 + 160} fill="#3a3a3a" stroke={INK} strokeWidth={4} />
          <rect x={x - 115} y={FLOOR_Y - 250} width={230} height={250} rx={10} fill="#3c3c40" stroke={INK} strokeWidth={5} />
          <rect x={x - 125} y={FLOOR_Y - 262} width={250} height={22} fill="#2a2a2e" stroke={INK} strokeWidth={4} />
          <rect x={x - 70} y={FLOOR_Y - 190} width={140} height={90} rx={8} fill={cold ? '#2a2a2a' : '#ff8a2a'} opacity={cold ? 1 : glow} stroke={INK} strokeWidth={4} />
          {cold ? null : <ellipse cx={x} cy={FLOOR_Y - 130} rx={120} ry={60} fill="#ffb060" opacity={0.15 * glow} />}
          <path d={`M${x - 70} ${FLOOR_Y - 150} H${x + 70}`} stroke={INK} strokeWidth={4} />
          <path d={`M${x - 100} ${FLOOR_Y} v18 M${x + 100} ${FLOOR_Y} v18`} stroke={INK} strokeWidth={8} />
        </g>
      );
    }
    case 'fireplace': {
      const f = 1 + Math.sin(t * 9) * 0.08 + Math.sin(t * 5.2) * 0.06;
      return (
        <g>
          <rect x={x - 165} y={FLOOR_Y - 330} width={330} height={330} fill="#8a7a6a" stroke={INK} strokeWidth={4} />
          <rect x={x - 190} y={FLOOR_Y - 350} width={380} height={30} fill="#5a3e2a" stroke={INK} strokeWidth={4} />
          <path d={`M${x - 110} ${FLOOR_Y} V${FLOOR_Y - 200} Q${x} ${FLOOR_Y - 270} ${x + 110} ${FLOOR_Y - 200} V${FLOOR_Y} Z`} fill="#1a1410" stroke={INK} strokeWidth={4} />
          <g transform={`translate(${x} ${FLOOR_Y - 10}) scale(1 ${f})`}>
            <path d="M-70 0 Q-80 -60 -40 -100 Q-30 -60 -10 -70 Q0 -130 30 -150 Q30 -90 60 -80 Q90 -40 70 0 Z" fill="#f08a2a" />
            <path d="M-40 0 Q-46 -40 -20 -60 Q-10 -30 6 -40 Q14 -80 34 -90 Q36 -40 46 0 Z" fill="#ffd25a" />
          </g>
          <ellipse cx={x} cy={FLOOR_Y + 30} rx={260} ry={60} fill="#ffb060" opacity={0.12 * f} />
        </g>
      );
    }
    case 'oven': {
      const f = 0.6 + 0.3 * Math.sin(t * 7);
      return (
        <g>
          <Bricks2 x={x - 180} y={FLOOR_Y - 440} w={360} h={440} c="#a8624a" seed={seed} />
          <rect x={x - 180} y={FLOOR_Y - 440} width={360} height={440} fill="none" stroke={INK} strokeWidth={4} />
          <path d={`M${x - 100} ${FLOOR_Y - 120} V${FLOOR_Y - 220} Q${x} ${FLOOR_Y - 300} ${x + 100} ${FLOOR_Y - 220} V${FLOOR_Y - 120} Z`} fill="#ff9a3a" opacity={f} stroke={INK} strokeWidth={5} />
          <rect x={x - 200} y={FLOOR_Y - 130} width={400} height={20} fill="#6a6a6a" stroke={INK} strokeWidth={3} />
        </g>
      );
    }
    case 'bed': return (
      <g>
        <path d={`M${x - 200} ${FLOOR_Y} V${FLOOR_Y - 240} M${x + 200} ${FLOOR_Y} V${FLOOR_Y - 160}`} stroke="#3a3a3a" strokeWidth={10} />
        <rect x={x - 200} y={FLOOR_Y - 140} width={400} height={64} rx={14} fill={(it.color as string) ?? '#7a8a9a'} stroke={INK} strokeWidth={4} />
        <rect x={x - 190} y={FLOOR_Y - 168} width={110} height={40} rx={16} fill="#f2ede2" stroke={INK} strokeWidth={3} />
        <path d={`M${x - 70} ${FLOOR_Y - 140} Q${x + 60} ${FLOOR_Y - 170} ${x + 196} ${FLOOR_Y - 140}`} fill="none" stroke="#000" opacity={0.2} strokeWidth={4} />
      </g>
    );
    case 'beds': return (
      <g>
        {[-1, 0, 1].map((k) => (
          <g key={k}>
            <path d={`M${x + k * 330 - 140} ${FLOOR_Y} V${FLOOR_Y - 200} M${x + k * 330 + 140} ${FLOOR_Y} V${FLOOR_Y - 140}`} stroke="#d8dcdc" strokeWidth={9} />
            <rect x={x + k * 330 - 140} y={FLOOR_Y - 120} width={280} height={56} rx={10} fill="#e8ece8" stroke={INK} strokeWidth={4} />
            <rect x={x + k * 330 - 136} y={FLOOR_Y - 146} width={80} height={32} rx={12} fill="#fbfbf6" stroke={INK} strokeWidth={3} />
            <rect x={x + k * 330 - 60} y={FLOOR_Y - 122} width={196} height={12} fill="#7a9ab0" opacity={0.6} />
          </g>
        ))}
      </g>
    );
    case 'bunk': return (
      <g>
        <path d={`M${x - 150} ${FLOOR_Y} V${FLOOR_Y - 420} M${x + 150} ${FLOOR_Y} V${FLOOR_Y - 420}`} stroke="#5a3e2a" strokeWidth={14} />
        {[0, 1].map((r) => <g key={r}><rect x={x - 150} y={FLOOR_Y - 120 - r * 210} width={300} height={34} fill="#6a5a44" stroke={INK} strokeWidth={4} /><rect x={x - 140} y={FLOOR_Y - 140 - r * 210} width={280} height={22} rx={8} fill="#8a8a6a" stroke={INK} strokeWidth={3} /></g>)}
      </g>
    );
    case 'clock': return <ClockFace x={x} y={240} t={t} at={arg} />;
    case 'portrait': return (
      <g transform={`translate(${x} 320)`}>
        <rect x={-92} y={-112} width={184} height={224} fill="#b8892e" stroke={INK} strokeWidth={4} />
        <rect x={-76} y={-96} width={152} height={192} fill={arg ? '#ddd' : '#5a4a3a'} stroke={INK} strokeWidth={2} />
        {arg ? <g transform="translate(-66 -60)"><Flag nation={arg} w={132} h={88} t={0} still /></g> : <g><circle cx={0} cy={-14} r={40} fill="#e8d2b8" /><path d="M-62 96 Q0 6 62 96" fill="#2a2a2a" /></g>}
      </g>
    );
    case 'map': {
      const sea = arg === 'sea';
      return (
        <g transform={`translate(${x} 360)`}>
          <rect x={-280} y={-180} width={560} height={360} fill={sea ? '#bcd6e4' : '#cfe1e8'} stroke={INK} strokeWidth={5} />
          <path d="M-240 -110 q60 -30 120 0 t110 30 q40 50 -10 90 t-120 20 q-60 -20 -90 -80 z M60 -60 q50 -40 120 -20 q40 40 10 100 q-60 40 -110 0 z" fill="#e8dcb8" stroke="#8a7a5a" strokeWidth={3} />
          {sea ? <path d="M-200 120 L-40 -20 L120 60 M-120 -150 L60 -140" stroke="#b8392e" strokeWidth={5} strokeDasharray="12 10" fill="none" /> : <path d="M-160 10 Q0 -60 110 20" stroke="#b8392e" strokeWidth={6} fill="none" strokeDasharray="14 10" />}
          {[0, 1, 2, 3].map((k) => <circle key={k} cx={-200 + k * 130} cy={-160} r={7} fill="#b8392e" stroke={INK} strokeWidth={2} />)}
        </g>
      );
    }
    case 'poster': return (
      <g transform={`translate(${x} 400) rotate(${(rnd(seed, 1) - 0.5) * 4})`}>
        <rect x={-88} y={-120} width={176} height={240} fill="#efe3c2" stroke={INK} strokeWidth={4} />
        <rect x={-72} y={-102} width={144} height={60} fill={(it.color as string) ?? '#b8392e'} />
        <text x={0} y={-62} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={text && text.length > 9 ? 17 : 24} fill="#f7efe0">{(text ?? 'NOTICE').toUpperCase()}</text>
        {[0, 1, 2, 3, 4].map((k) => <rect key={k} x={-66} y={-20 + k * 22} width={k === 4 ? 70 : 132} height={8} fill={INK} opacity={0.5} />)}
      </g>
    );
    case 'flag': return <g transform={`translate(${x - 30} 160)`}><rect x={-6} y={0} width={10} height={FLOOR_Y - 160} fill="#6a4a2a" stroke={INK} strokeWidth={3} /><g transform="translate(4 10)"><Flag nation={arg || nationKey || 'GER'} w={150} h={100} t={t} /></g></g>;
    case 'calendar': return (
      <g transform={`translate(${x} 330)`}>
        <rect x={-66} y={-90} width={132} height={180} fill="#f7f2e4" stroke={INK} strokeWidth={4} />
        <rect x={-66} y={-90} width={132} height={44} fill="#b8392e" stroke={INK} strokeWidth={3} />
        <text x={0} y={-58} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={26} fill="#fff">{text ?? '1917'}</text>
        {Array.from({ length: 20 }, (_, k) => <rect key={k} x={-56 + (k % 5) * 23} y={-34 + Math.floor(k / 5) * 28} width={16} height={16} fill={k < 9 ? INK : '#d8d0bc'} opacity={k < 9 ? 0.35 : 1} />)}
      </g>
    );
    case 'photos': return <g>{[[-60, 300, 70, 90], [30, 290, 80, 100], [-20, 410, 90, 70]].map(([dx, y, w, h], k) => <g key={k}><rect x={x + dx - w / 2} y={y - h / 2} width={w} height={h} fill="#3a2a1a" stroke={INK} strokeWidth={3} /><rect x={x + dx - w / 2 + 8} y={y - h / 2 + 8} width={w - 16} height={h - 16} fill="#c9b892" /><circle cx={x + dx} cy={y - 4} r={12} fill="#6a5a4a" /></g>)}</g>;
    case 'crucifix': return <g transform={`translate(${x} 300)`}><rect x={-9} y={-70} width={18} height={150} fill="#5a3e2a" stroke={INK} strokeWidth={3} /><rect x={-48} y={-40} width={96} height={18} fill="#5a3e2a" stroke={INK} strokeWidth={3} /></g>;
    case 'mirror': return <g transform={`translate(${x} 330)`}><ellipse rx={56} ry={74} fill="#8a6a3a" stroke={INK} strokeWidth={4} /><ellipse rx={44} ry={62} fill="#cfe0e6" /><path d="M-20 -30 L10 -50" stroke="#fff" strokeWidth={6} opacity={0.7} /></g>;
    case 'hooks': return (
      <g>
        <rect x={x - 110} y={330} width={220} height={18} fill="#5a3e2a" stroke={INK} strokeWidth={3} />
        <path d={`M${x - 80} 348 Q${x - 110} 470 ${x - 60} 560 L${x - 20} 560 Q${x - 10} 450 ${x - 50} 348 Z`} fill="#5a5a62" stroke={INK} strokeWidth={3} />
        <path d={`M${x + 20} 348 Q${x - 6} 440 ${x + 30} 500 L${x + 70} 500 Q${x + 90} 430 ${x + 56} 348 Z`} fill="#7a5a3c" stroke={INK} strokeWidth={3} />
        <ellipse cx={x + 86} cy={348} rx={30} ry={12} fill="#3a3a3a" stroke={INK} strokeWidth={3} />
      </g>
    );
    case 'lamp': {
      const on = arg !== 'off';
      return (
        <g transform={`translate(${x} 200)`}>
          <line x1={0} y1={-400} x2={0} y2={-40} stroke={INK} strokeWidth={3} />
          <path d="M-56 0 L-28 -44 L28 -44 L56 0 Z" fill="#3f5a4a" stroke={INK} strokeWidth={4} />
          {on ? <ellipse cx={0} cy={4} rx={24} ry={8} fill="#fff4b0" /> : null}
        </g>
      );
    }
    case 'barrels': return <g>{[[-80, 0], [80, 0], [0, -150]].map(([dx, dy], k) => <g key={k} transform={`translate(${x + dx} ${FLOOR_Y + dy})`}><path d="M-64 0 Q-74 -75 -64 -150 H64 Q74 -75 64 0 Z" fill="#8a5a32" stroke={INK} strokeWidth={4} /><path d="M-70 -40 H70 M-70 -110 H70" stroke="#3a3a3a" strokeWidth={8} /></g>)}</g>;
    case 'crates': return <g>{[[-80, 0, 150], [80, 0, 150], [-10, -150, 140]].map(([dx, dy, s], k) => <g key={k} transform={`translate(${x + dx} ${FLOOR_Y + dy})`}><rect x={-s / 2} y={-s} width={s} height={s} fill="#b88a52" stroke={INK} strokeWidth={4} /><path d={`M${-s / 2} ${-s} L${s / 2} 0 M${-s / 2} 0 L${s / 2} ${-s}`} stroke="#8a6232" strokeWidth={6} />{arg && k < 2 ? <text x={0} y={-s / 2 + 8} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={22} fill={INK}>{arg.toUpperCase()}</text> : null}</g>)}</g>;
    case 'sacks': return <g>{[[-90, 0], [10, 0], [100, 0], [-40, -90], [56, -88]].map(([dx, dy], k) => <path key={k} transform={`translate(${x + dx} ${FLOOR_Y + dy})`} d="M-54 0 Q-66 -60 -40 -92 Q0 -104 40 -92 Q66 -60 54 0 Z" fill={k % 2 ? '#cdb892' : '#bfa87e'} stroke={INK} strokeWidth={4} />)}</g>;
    case 'rifles': return (
      <g>
        <rect x={x - 120} y={FLOOR_Y - 60} width={240} height={30} fill="#5a3e2a" stroke={INK} strokeWidth={3} />
        <rect x={x - 120} y={FLOOR_Y - 300} width={240} height={22} fill="#5a3e2a" stroke={INK} strokeWidth={3} />
        {[0, 1, 2, 3, 4].map((k) => <path key={k} d={`M${x - 96 + k * 48} ${FLOOR_Y - 40} V${FLOOR_Y - 360}`} stroke="#3a2a1a" strokeWidth={12} strokeLinecap="round" />)}
      </g>
    );
    case 'blackboard': return (
      <g transform={`translate(${x} 360)`}>
        <rect x={-300} y={-170} width={600} height={340} fill="#2f3f36" stroke="#6a4a2a" strokeWidth={16} />
        {text ? <text x={0} y={20} textAnchor="middle" fontFamily={FONT.hand} fontSize={70} fill="#f2f2ea" opacity={0.92}>{text}</text> : <path d="M-220 -60 q60 -20 120 0 M-220 0 q100 -10 200 0 M-220 60 q50 -10 100 0" stroke="#f2f2ea" strokeWidth={5} opacity={0.6} fill="none" />}
      </g>
    );
    case 'sink': return (
      <g>
        <rect x={x - 120} y={FLOOR_Y - 230} width={240} height={70} fill="#a8a49a" stroke={INK} strokeWidth={4} />
        <rect x={x - 100} y={FLOOR_Y - 160} width={20} height={160} fill="#6a6a6a" /><rect x={x + 80} y={FLOOR_Y - 160} width={20} height={160} fill="#6a6a6a" />
        <path d={`M${x + 60} ${FLOOR_Y - 230} V${FLOOR_Y - 330} H${x + 10} M${x + 60} ${FLOOR_Y - 330} l40 -30`} stroke="#4a5a5a" strokeWidth={12} fill="none" strokeLinecap="round" />
      </g>
    );
    case 'cradle': return <g transform={`translate(${x} ${FLOOR_Y})`}><path d="M-100 -40 Q0 20 100 -40" stroke="#5a3e2a" strokeWidth={10} fill="none" /><path d="M-90 -50 H90 V-140 H-90 Z" fill="#8a5a32" stroke={INK} strokeWidth={4} /><rect x={-80} y={-150} width={160} height={24} rx={10} fill="#e9e2d0" stroke={INK} strokeWidth={3} /></g>;
    case 'arch': return (
      <g>
        <Bricks2 x={x - 190} y={WALL_BASE - 470} w={380} h={470} c="#9a6a4a" seed={seed} />
        <path d={`M${x - 130} ${WALL_BASE} V${WALL_BASE - 280} Q${x} ${WALL_BASE - 430} ${x + 130} ${WALL_BASE - 280} V${WALL_BASE} Z`} fill="#141010" stroke={INK} strokeWidth={5} />
      </g>
    );
    case 'stained': return (
      <g>
        <path d={`M${x - 110} 600 V230 Q${x} 90 ${x + 110} 230 V600 Z`} fill="#3a2a2a" stroke={INK} strokeWidth={5} />
        {Array.from({ length: 12 }, (_, k) => <rect key={k} x={x - 96 + (k % 3) * 64} y={240 + Math.floor(k / 3) * 88} width={60} height={84} fill={['#b8392e', '#3a6aa8', '#d9b35a', '#4f8a4a'][(k * 7) % 4]} opacity={0.85} />)}
        <path d={`M${x - 96} 236 Q${x} 110 ${x + 96} 236 Z`} fill="#d9b35a" opacity={0.8} />
      </g>
    );
    case 'sign': return (
      <g transform={`translate(${x} 150)`}>
        <rect x={-230} y={-40} width={460} height={80} fill="#2a3a2a" stroke={INK} strokeWidth={5} />
        <text x={0} y={16} textAnchor="middle" fontFamily={FONT.title} fontWeight={700} fontSize={text && text.length > 14 ? 30 : 40} fill="#e8d6a0" letterSpacing={3}>{(text ?? 'GROCER').toUpperCase()}</text>
      </g>
    );
    case 'radio': return <g transform={`translate(${x} 420)`}><rect x={-70} y={-60} width={140} height={110} rx={10} fill="#5a4030" stroke={INK} strokeWidth={4} /><circle cx={-24} cy={-6} r={26} fill="#c9b892" stroke={INK} strokeWidth={3} /><circle cx={36} cy={-20} r={10} fill="#d9c49a" stroke={INK} strokeWidth={2} /><circle cx={36} cy={16} r={10} fill="#d9c49a" stroke={INK} strokeWidth={2} /><rect x={-80} y={50} width={160} height={14} fill="#4a3424" /></g>;
    case 'pipes': return <g>{[120, 160].map((y, k) => <rect key={k} x={X0} y={y} width={W} height={20} fill={k ? '#6a6a6a' : '#8a5a3a'} stroke={INK} strokeWidth={3} />)}</g>;
    default: return null;
  }
};

const ClockFace: React.FC<{ x: number; y: number; t: number; at?: string }> = ({ x, y, t, at }) => {
  let h = 10, m = 10 + t * 0.5;
  if (at && /\d+:\d+/.test(at)) { const [hh, mm] = at.split(':').map(Number); h = hh; m = mm + t / 60; }
  const ma = (m / 60) * 360, ha = ((h % 12) / 12) * 360 + (m / 60) * 30;
  return (
    <g transform={`translate(${x} ${y})`}>
      <circle r={50} fill="#fbf8f0" stroke={INK} strokeWidth={5} />
      <circle r={42} fill="none" stroke="#8a6a4a" strokeWidth={2} />
      {Array.from({ length: 12 }, (_, i) => <line key={i} x1={0} y1={-40} x2={0} y2={-33} stroke={INK} strokeWidth={3} transform={`rotate(${i * 30})`} />)}
      <line x1={0} y1={0} x2={0} y2={-24} stroke={INK} strokeWidth={5} strokeLinecap="round" transform={`rotate(${ha})`} />
      <line x1={0} y1={0} x2={0} y2={-38} stroke={INK} strokeWidth={3} strokeLinecap="round" transform={`rotate(${ma})`} />
      <circle r={4} fill={INK} />
    </g>
  );
};

/** light sources of a room: window shafts, lamp/candle/lantern pools, fire glow, darkness at night */
const RoomLight: React.FC<{ light: string; items: Item[]; xs: number[]; p: P }> = ({ light, items, xs, p }) => {
  const t = p.t, night = p.time === 'night', dusk = p.time === 'dusk';
  const id = 'rl_' + String(p.style ?? 'room');
  const wins = items.map((it, i) => (it.item === 'window' || it.item === 'stained' ? xs[i] : null)).filter((x): x is number => x !== null);
  const lamps = items.map((it, i) => (it.item === 'lamp' ? xs[i] : null)).filter((x): x is number => x !== null);
  const fires = items.map((it, i) => (['stove', 'fireplace', 'oven'].includes(it.item) && it.arg !== 'cold' ? xs[i] : null)).filter((x): x is number => x !== null);
  const flick = 1 + Math.sin(t * 8.3) * 0.05 + Math.sin(t * 13.1) * 0.03;
  const dim = light === 'candle' || light === 'lantern' || light === 'dim' || night;
  const pool = light === 'candle' || light === 'lantern' ? ((p.lightX as number) ?? 960) : null;
  return (
    <g style={{ pointerEvents: 'none' }}>
      <defs>
        <radialGradient id={id + 'p'} cx="0.5" cy="0.5" r="0.5"><stop offset="0" stopColor="#ffd88a" stopOpacity={0.34} /><stop offset="1" stopColor="#ffd88a" stopOpacity={0} /></radialGradient>
        <radialGradient id={id + 'v'} cx="0.5" cy="0.5" r="0.62"><stop offset="0.35" stopColor="#000" stopOpacity={0} /><stop offset="1" stopColor={night ? '#040814' : '#120a04'} stopOpacity={dim ? 0.78 : 0.4} /></radialGradient>
      </defs>
      {!night && !dim ? wins.map((x, i) => <path key={i} d={`M${x - 150} 170 L${x + 150} 170 L${x + 20 + (x - 960) * -0.3} 1100 L${x - 420 + (x - 960) * -0.3} 1100 Z`} fill={dusk ? '#ffb070' : '#fff6d8'} opacity={0.12} />) : null}
      {lamps.map((x, i) => <g key={i}><path d={`M${x - 56} 200 L${x - 330} 1100 L${x + 330} 1100 L${x + 56} 200 Z`} fill="#fff1b8" opacity={0.1 * flick} /><ellipse cx={x} cy={1000} rx={420} ry={110} fill={`url(#${id}p)`} /></g>)}
      {fires.map((x, i) => <ellipse key={i} cx={x} cy={680} rx={520 * flick} ry={420 * flick} fill={`url(#${id}p)`} />)}
      {pool !== null ? <ellipse cx={pool} cy={720} rx={760 * flick} ry={560 * flick} fill={`url(#${id}p)`} /> : null}
      {dim ? <rect x={X0} y={Y0} width={W} height={H} fill={night ? '#0a1230' : '#1a1008'} opacity={night ? 0.32 : 0.22} /> : null}
      <rect x={X0} y={Y0} width={W} height={H} fill={`url(#${id}v)`} />
    </g>
  );
};

export const RoomKit: React.FC<P> = (p) => {
  const st = ROOM_STYLES[(p.style as string) ?? 'kitchen'] ?? ROOM_STYLES.kitchen;
  const items = ((p.items as unknown[]) ?? st.items).map(asItem);
  const xs = layout(items);
  const seed = 'room' + String(p.style ?? '') + String(p.seed ?? '');
  const light = (p.light as string) ?? st.light;
  const nationKey = (p.nation as string) ?? undefined;
  return (
    <g>
      <RoomWall type={(p.wall as string) ?? st.wall} color={(p.wallColor as string) ?? st.color} poor={(p.poor as boolean) ?? st.poor} seed={seed} />
      <RoomFloor type={(p.floor as string) ?? st.floor} color={(p.floorColor as string) ?? st.floorColor} seed={seed} />
      {items.map((it, i) => <RoomItem key={i} it={it} x={xs[i]} p={p} i={i} nationKey={nationKey} />)}
      {(p.beams as boolean) ?? st.beams ? (
        <g>
          <rect x={X0} y={Y0} width={W} height={120} fill="#3a2818" />
          {Array.from({ length: 14 }, (_, i) => <rect key={i} x={X0 + 40 + i * 180} y={Y0} width={70} height={150} fill="#4a3424" stroke={INK} strokeWidth={3} />)}
          <rect x={X0} y={Y0 + 120} width={W} height={46} fill="#5a3e2a" stroke={INK} strokeWidth={4} />
          {[60, 1860].map((x, i) => <rect key={'p' + i} x={x - 30} y={Y0 + 160} width={60} height={WALL_BASE - Y0 - 160} fill="#5a3e2a" stroke={INK} strokeWidth={4} />)}
        </g>
      ) : null}
      <RoomLight light={light} items={items} xs={xs} p={p} />
    </g>
  );
};

// =====================================================================================================================
// TOWN (a street of facades)
// =====================================================================================================================
const SIGNS: Record<string, Record<string, string>> = {
  german: { bakery: 'BÄCKEREI', butcher: 'METZGEREI', grocer: 'KOLONIALWAREN', townhall: 'RATHAUS', post: 'POST', cafe: 'CAFÉ', office: 'LEBENSMITTELAMT', shop: 'KAUFHAUS', bank: 'BANK', station: 'BAHNHOF' },
  austrian: { bakery: 'BÄCKEREI', butcher: 'FLEISCHHAUER', grocer: 'GREISLER', townhall: 'RATHAUS', post: 'POST', cafe: 'KAFFEEHAUS', office: 'ERNÄHRUNGSAMT', shop: 'WARENHAUS', bank: 'BANK', station: 'BAHNHOF' },
  french: { bakery: 'BOULANGERIE', butcher: 'BOUCHERIE', grocer: 'ÉPICERIE', townhall: 'MAIRIE', post: 'POSTES', cafe: 'CAFÉ', office: 'RAVITAILLEMENT', shop: 'MAGASIN', bank: 'BANQUE', station: 'GARE' },
  english: { bakery: 'BAKER', butcher: 'BUTCHER', grocer: 'GROCER', townhall: 'TOWN HALL', post: 'POST OFFICE', cafe: 'TEA ROOM', office: 'FOOD OFFICE', shop: 'DRAPER', bank: 'BANK', station: 'STATION' },
  russian: { bakery: 'ХЛѢБЪ', butcher: 'МЯСО', grocer: 'БАКАЛЕЯ', townhall: 'УПРАВА', post: 'ПОЧТА', cafe: 'ТРАКТИРЪ', office: 'ПРОДОВОЛЬСТВІЕ', shop: 'ЛАВКА', bank: 'БАНКЪ', station: 'ВОКЗАЛЪ' },
  dutch: { bakery: 'BAKKERIJ', butcher: 'SLAGERIJ', grocer: 'KRUIDENIER', townhall: 'STADHUIS', post: 'POSTKANTOOR', cafe: 'CAFÉ', office: 'DISTRIBUTIEDIENST', shop: 'WINKEL', bank: 'BANK', station: 'STATION' },
};
/** town styles: palette, roofs, half-timbering, sign language */
export const TOWN_STYLES: Record<string, { walls: string[]; roof: string; timber?: boolean; brick?: boolean; lang: string; buildings: string[]; back: string; doc: string }> = {
  german: { walls: ['#e3d6b8', '#d9c7a0', '#c98f62', '#e8dcc6', '#b9a27a'], roof: '#8a4a3a', timber: true, lang: 'german', buildings: ['house', 'shop:bakery', 'tenement', 'shop:grocer', 'church'], back: 'spire', doc: 'German town: half-timbered houses, red roofs, German shop signs' },
  austrian: { walls: ['#efe3c0', '#e8d8a8', '#d9c49a', '#f0e6cc'], roof: '#6a4a3a', lang: 'austrian', buildings: ['tenement', 'shop:cafe', 'tenement', 'shop:bakery'], back: 'city', doc: 'Vienna-style street: pale stucco blocks, Austrian signs' },
  french: { walls: ['#e8dcc0', '#d9c49a', '#c9b28a', '#e0cfa8'], roof: '#6a7a8a', lang: 'french', buildings: ['house', 'shop:bakery', 'house', 'shop:cafe', 'townhall'], back: 'hills', doc: 'French town: pale stone, slate roofs, French signs' },
  english: { walls: ['#a86a52', '#b9785a', '#9a5a48', '#c9a27a'], roof: '#4a4a52', brick: true, lang: 'english', buildings: ['tenement', 'shop:grocer', 'house', 'shop:butcher', 'post'], back: 'chimneys', doc: 'British street: brick terraces, chimney pots, English signs' },
  russian: { walls: ['#d9b77a', '#a8b8a0', '#c9a0a0', '#e3d6b8'], roof: '#5a7a5a', lang: 'russian', buildings: ['house', 'shop:bakery', 'tenement', 'church'], back: 'spire', doc: 'Russian town: painted stucco, green roofs, Cyrillic signs' },
  dutch: { walls: ['#9a5a48', '#a86a52', '#7a4a3a', '#b9785a'], roof: '#3a3a3a', brick: true, lang: 'dutch', buildings: ['house', 'shop:grocer', 'house', 'house', 'shop:bakery'], back: 'none', doc: 'Dutch street: narrow brick gables, Dutch signs (neutral 1914-18)' },
  industrial: { walls: ['#8a6a5a', '#7a5a4a', '#9a7a62'], roof: '#3a3a3a', brick: true, lang: 'german', buildings: ['tenement', 'factory', 'tenement', 'shop:grocer'], back: 'chimneys', doc: 'factory district: brick tenements and a smoking works' },
  village: { walls: ['#e8dcc6', '#d9c7a0', '#c9b28a'], roof: '#7a5a3a', timber: true, lang: 'german', buildings: ['house', 'house', 'church', 'house'], back: 'hills', doc: 'village street: low houses, church, fields behind' },
};
export const TOWN_BUILDINGS: Record<string, { w: number; h: number; doc: string }> = {
  house: { w: 330, h: 380, doc: 'gabled house (half-timbered in german/village style)' },
  tenement: { w: 380, h: 560, doc: 'four-storey apartment block' },
  shop: { w: 400, h: 440, doc: 'shop:<bakery|butcher|grocer|cafe|post|bank|office> with sign, awning and display window ({"item": "shop:bakery", "goods": "empty"}; goods = bread | meat | veg | turnips | tins | empty)' },
  church: { w: 420, h: 760, doc: 'church with a tower and clock' },
  townhall: { w: 500, h: 540, doc: 'town hall with columns, flag and clock' },
  factory: { w: 600, h: 440, doc: 'works with sawtooth roof and smoking chimneys' },
  office: { w: 440, h: 500, doc: 'official building with a sign (ration office, ministry)' },
  post: { w: 380, h: 460, doc: 'post office' },
  ruin: { w: 340, h: 340, doc: 'shelled ruin with empty windows' },
  station: { w: 560, h: 460, doc: 'railway station front with a big clock' },
};
export const TOWN_ITEMS: Record<string, { doc: string }> = {
  lamppost: { doc: 'gas street lamp (lit at night)' },
  poster: { doc: 'poster on a wall: {"item": "poster", "text": "BROTKARTE"}' },
  cart: { doc: 'hand cart' },
  bench: { doc: 'street bench' },
  pump: { doc: 'water pump' },
  barrels: { doc: 'barrels by a door' },
  crates: { doc: 'crates by a door' },
  sandbags: { doc: 'sandbag wall' },
  tree: { doc: 'street tree (bare in winter)' },
  pole: { doc: 'telegraph pole with wires' },
  snowbank: { doc: 'heap of shovelled snow' },
  banner: { doc: 'flags hanging from the facades (banner:<nation>)' },
  rope: { doc: 'queue barrier rope on posts' },
};

const SKYLINE: React.FC<{ kind: string; y: number; time: string }> = ({ kind, y, time }) => {
  const c = time === 'night' ? '#1c2436' : time === 'dusk' ? '#8a6a7a' : '#a9b4b8';
  if (kind === 'none') return null;
  if (kind === 'hills') return <path d={`M${X0} ${y} Q300 ${y - 120} 700 ${y - 60} T1500 ${y - 90} T2200 ${y - 40} V${y + 60} H${X0} Z`} fill={time === 'night' ? '#1a2630' : '#9ab08a'} />;
  return (
    <g fill={c}>
      {Array.from({ length: 14 }, (_, i) => <rect key={i} x={X0 + i * 180} y={y - 90 - rnd('sk', i) * 110} width={170} height={200} />)}
      {kind === 'spire' ? <path d={`M1320 ${y} V${y - 260} L1350 ${y - 420} L1380 ${y - 260} V${y} Z`} /> : null}
      {kind === 'chimneys' ? [300, 520, 1460, 1700].map((x, i) => <g key={i}><rect x={x} y={y - 330 - i * 20} width={36} height={340} /><path d={`M${x + 18} ${y - 340 - i * 20} q-30 -60 20 -110 q50 -40 10 -100`} stroke={time === 'night' ? '#2a3040' : '#8a8a8a'} strokeWidth={34} fill="none" opacity={0.45} strokeLinecap="round" /></g>) : null}
      {kind === 'city' ? <path d={`M600 ${y} V${y - 220} Q680 ${y - 330} 760 ${y - 220} V${y} Z`} /> : null}
    </g>
  );
};

const Facade: React.FC<{ b: Item; x: number; w: number; h: number; base: number; st: (typeof TOWN_STYLES)[string]; time: string; snow: boolean; t: number; i: number }> = ({ b, x, w, h, base, st, time, snow, t, i }) => {
  const night = time === 'night';
  const kind = b.item, arg = (b.arg as string) ?? '';
  const wall = (b.color as string) ?? st.walls[i % st.walls.length];
  const L = x - w / 2, top = base - h;
  const lang = SIGNS[st.lang] ?? SIGNS.english;
  const winFill = (k: number) => (night ? (rnd('tw' + i, k) > 0.45 ? '#f6d77a' : '#1c2438') : '#8fb0c2');
  const windows = (rows: number, cols: number, y0: number, y1: number, ww = 46, wh = 66) => Array.from({ length: rows * cols }, (_, k) => {
    const r = Math.floor(k / cols), c = k % cols;
    const cx = L + (c + 0.5) * (w / cols), cy = y0 + (r + 0.5) * ((y1 - y0) / rows);
    return (
      <g key={'w' + k}>
        <rect x={cx - ww / 2} y={cy - wh / 2} width={ww} height={wh} fill={winFill(k)} stroke={INK} strokeWidth={3} />
        <path d={`M${cx} ${cy - wh / 2} V${cy + wh / 2} M${cx - ww / 2} ${cy - 4} H${cx + ww / 2}`} stroke="#efe6d2" strokeWidth={3} />
        <rect x={cx - ww / 2 - 5} y={cy + wh / 2} width={ww + 10} height={7} fill={snow ? '#f2f4f6' : '#cdbb9a'} stroke={INK} strokeWidth={2} />
      </g>
    );
  });
  const brickWall = st.brick ? <Bricks2 x={L} y={top} w={w} h={h} c={wall} seed={'fb' + i} rowH={30} /> : <rect x={L} y={top} width={w} height={h} fill={wall} />;
  const outline = <rect x={L} y={top} width={w} height={h} fill="none" stroke={INK} strokeWidth={4} />;
  const gable = (rh: number) => (
    <g>
      <path d={`M${L - 16} ${top + 4} L${x} ${top - rh} L${L + w + 16} ${top + 4} Z`} fill={snow ? '#f2f4f6' : st.roof} stroke={INK} strokeWidth={4} />
      {snow ? null : Array.from({ length: 5 }, (_, k) => <path key={k} d={`M${L - 10 + k * 12} ${top - k * (rh / 6)} H${L + w + 10 - k * 12}`} stroke="#000" opacity={0.1} strokeWidth={3} />)}
      {!st.brick && st.timber ? null : <rect x={x + w * 0.22} y={top - rh * 0.75} width={26} height={rh * 0.5} fill={dark(wall, -0.3)} stroke={INK} strokeWidth={3} />}
    </g>
  );
  const timber = st.timber ? <path d={`M${L} ${top + h * 0.42} H${L + w} M${L + w * 0.33} ${top} V${top + h * 0.42} M${L + w * 0.66} ${top} V${top + h * 0.42} M${L} ${top} L${L + w * 0.33} ${top + h * 0.42} M${L + w} ${top} L${L + w * 0.66} ${top + h * 0.42}`} stroke="#4a3424" strokeWidth={9} /> : null;
  const door = (dx: number, dw = 70, dh = 130) => <g><rect x={x + dx - dw / 2} y={base - dh} width={dw} height={dh} fill="#5a3e2a" stroke={INK} strokeWidth={3} /><circle cx={x + dx + dw / 2 - 12} cy={base - dh / 2} r={4} fill="#d9b35a" /></g>;
  const signBoard = (text: string, y: number, wBoard = w - 50) => (
    <g>
      <rect x={x - wBoard / 2} y={y - 26} width={wBoard} height={52} fill="#2a3a2a" stroke={INK} strokeWidth={4} />
      <text x={x} y={y + 12} textAnchor="middle" fontFamily={FONT.title} fontWeight={700} fontSize={Math.min(34, (wBoard - 30) / Math.max(4, text.length) * 1.55)} fill="#e8d6a0" letterSpacing={2}>{text}</text>
    </g>
  );
  switch (kind) {
    case 'house': return <g>{brickWall}{timber}{outline}{gable(120)}{windows(2, 2, top + 20, base - 150, 52, 70)}{door(0)}</g>;
    case 'tenement': return (
      <g>{brickWall}{outline}
        <rect x={L - 12} y={top - 22} width={w + 24} height={26} fill={dark(wall, -0.2)} stroke={INK} strokeWidth={4} />
        {windows(4, 3, top + 16, base - 120)}{door(0, 80, 120)}
      </g>
    );
    case 'shop': {
      const what = arg || 'grocer';
      const goods = (b.goods as string) ?? (what === 'bakery' ? 'bread' : what === 'butcher' ? 'meat' : what === 'grocer' ? 'tins' : what === 'cafe' ? 'cups' : 'none');
      const text = ((b.text as string) ?? lang[what] ?? what).toUpperCase();
      const dwY = base - 200, dwH = 150;
      const awning = (b.awning as string) ?? ['#b8392e', '#2f6b3a', '#3a5a8a', '#a8873a'][i % 4];
      return (
        <g>{brickWall}{timber}{outline}{gable(100)}
          {windows(1, 3, top + 20, base - 250, 46, 60)}
          {signBoard(text, base - 238)}
          <rect x={L + 24} y={dwY} width={w - 140} height={dwH} fill={night ? '#3a3220' : '#d8e4e6'} stroke={INK} strokeWidth={4} />
          {goods === 'bread' ? Array.from({ length: 6 }, (_, k) => <path key={k} d={`M${L + 50 + k * 40} ${dwY + 120} q-4 -26 18 -28 q22 2 18 28 Z`} fill="#c98a42" stroke={INK} strokeWidth={2} />) : null}
          {goods === 'turnips' || goods === 'veg' ? Array.from({ length: 7 }, (_, k) => <g key={k}><circle cx={L + 50 + k * 34} cy={dwY + 118 - (k % 2) * 16} r={15} fill={goods === 'turnips' ? '#efe6d6' : '#d98a3a'} stroke={INK} strokeWidth={2} />{goods === 'turnips' ? <path d={`M${L + 40 + k * 34} ${dwY + 112 - (k % 2) * 16} q10 -10 20 0`} fill="#9a5a9a" /> : null}</g>) : null}
          {goods === 'meat' ? Array.from({ length: 4 }, (_, k) => <path key={k} d={`M${L + 60 + k * 60} ${dwY + 10} v16 q-16 30 0 60 q16 -30 0 -60`} fill="#b84a4a" stroke={INK} strokeWidth={2} />) : null}
          {goods === 'tins' ? Array.from({ length: 8 }, (_, k) => <rect key={k} x={L + 42 + k * 30} y={dwY + 96 - (k % 2) * 36} width={24} height={30} fill={['#b8392e', '#3a6a8a', '#d9b35a'][k % 3]} stroke={INK} strokeWidth={2} />) : null}
          {goods === 'empty' ? <g><rect x={L + 40} y={dwY + 110} width={w - 172} height={8} fill="#8a6a4a" /><g transform={`translate(${L + 60 + (w - 140) / 2} ${dwY + 70}) rotate(-6)`}><rect x={-60} y={-22} width={120} height={44} fill="#f7f0de" stroke={INK} strokeWidth={2.5} /><text y={8} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={st.lang === 'german' || st.lang === 'austrian' ? 15 : 17} fill="#b8392e">{st.lang === 'german' || st.lang === 'austrian' ? 'AUSVERKAUFT' : st.lang === 'french' ? 'ÉPUISÉ' : 'SOLD OUT'}</text></g></g> : null}
          <path d={`M${L + 24} ${dwY + dwH * 0.5} H${L + w - 116}`} stroke="#efe6d2" strokeWidth={4} />
          {door(w / 2 - 66, 74, 150)}
          <path d={`M${L + 10} ${dwY - 8} L${L + w - 10} ${dwY - 8} L${L + w + 10} ${dwY + 34} L${L - 10} ${dwY + 34} Z`} fill={awning} stroke={INK} strokeWidth={4} />
          {Array.from({ length: Math.floor(w / 44) }, (_, k) => k % 2 ? <path key={k} d={`M${L + 10 + k * 44} ${dwY - 8} h44 l4 42 h-52 Z`} fill="#f2ead8" opacity={0.9} /> : null)}
          {snow ? <path d={`M${L + 10} ${dwY - 10} H${L + w - 10} l-8 -10 H${L + 18} Z`} fill="#f2f4f6" /> : null}
        </g>
      );
    }
    case 'church': {
      const tw = w * 0.38;
      return (
        <g>
          <rect x={L} y={base - h * 0.5} width={w} height={h * 0.5} fill={wall} stroke={INK} strokeWidth={4} />
          <path d={`M${L - 14} ${base - h * 0.5 + 4} L${x - tw / 2} ${base - h * 0.66} L${x + tw / 2} ${base - h * 0.66} L${L + w + 14} ${base - h * 0.5 + 4} Z`} fill={snow ? '#f2f4f6' : st.roof} stroke={INK} strokeWidth={4} />
          <rect x={x - tw / 2} y={top + h * 0.2} width={tw} height={h * 0.8} fill={dark(wall, -0.06)} stroke={INK} strokeWidth={4} />
          <path d={`M${x - tw / 2 - 10} ${top + h * 0.2} L${x} ${top - 40} L${x + tw / 2 + 10} ${top + h * 0.2} Z`} fill={snow ? '#f2f4f6' : '#4a6a5a'} stroke={INK} strokeWidth={4} />
          <path d={`M${x} ${top - 40} V${top - 90} M${x - 16} ${top - 72} H${x + 16}`} stroke={INK} strokeWidth={6} />
          <ClockFace x={x} y={top + h * 0.3} t={t} />
          <path d={`M${x - 34} ${base} V${base - 130} Q${x} ${base - 180} ${x + 34} ${base - 130} V${base} Z`} fill="#4a3424" stroke={INK} strokeWidth={4} />
          {[-1, 1].map((s) => <path key={s} d={`M${x + s * (tw / 2 + 60) - 22} ${base - 120} V${base - 220} Q${x + s * (tw / 2 + 60)} ${base - 250} ${x + s * (tw / 2 + 60) + 22} ${base - 220} V${base - 120} Z`} fill={night ? '#f6d77a' : '#5a6a8a'} stroke={INK} strokeWidth={3} />)}
        </g>
      );
    }
    case 'townhall': case 'office': case 'post': case 'station': {
      const label = ((b.text as string) ?? lang[kind] ?? kind).toUpperCase();
      return (
        <g>{brickWall}{outline}
          <path d={`M${L - 16} ${top + 4} L${x} ${top - 80} L${L + w + 16} ${top + 4} Z`} fill={dark(wall, -0.12)} stroke={INK} strokeWidth={4} />
          {kind === 'townhall' || kind === 'station' ? <ClockFace x={x} y={top - 22} t={t} /> : null}
          {windows(2, 4, top + 20, base - 180, 44, 74)}
          {signBoard(label, base - 166, Math.min(w - 40, 60 + label.length * 22))}
          {kind === 'townhall' ? [-1, -0.33, 0.33, 1].map((k, j) => <rect key={j} x={x + k * (w / 2 - 50) - 14} y={base - 130} width={28} height={130} fill="#efe6d2" stroke={INK} strokeWidth={3} />) : null}
          {door(0, 100, 130)}
          {kind === 'townhall' && b.flag !== false ? <g transform={`translate(${x + w / 2 - 70} ${top - 10})`}><rect x={-4} y={-120} width={8} height={130} fill="#6a4a2a" /><g transform="translate(4 -116)"><Flag nation={(b.nation as string) ?? 'GER'} w={90} h={60} t={t} /></g></g> : null}
        </g>
      );
    }
    case 'factory': return (
      <g>
        {[0.2, 0.75].map((k, j) => { const cx = L + w * k; return <g key={j}><rect x={cx - 22} y={top - 260} width={44} height={270} fill="#7a4a3a" stroke={INK} strokeWidth={4} /><path d={`M${cx} ${top - 270} q-${40 + Math.sin(t * 0.7 + j) * 10} -70 10 -130 q60 -50 20 -120`} stroke={night ? '#30343e' : '#8a8a8a'} strokeWidth={46} fill="none" opacity={0.5} strokeLinecap="round" /></g>; })}
        {brickWall}{outline}
        <path d={`M${L} ${top} ${Array.from({ length: 5 }, (_, k) => `L${L + (k + 0.5) * (w / 5)} ${top - 60} L${L + (k + 1) * (w / 5)} ${top}`).join(' ')} Z`} fill={st.roof} stroke={INK} strokeWidth={4} />
        {windows(2, 5, top + 30, base - 130, 70, 80)}
        <rect x={x - 80} y={base - 150} width={160} height={150} fill="#4a3424" stroke={INK} strokeWidth={4} />
      </g>
    );
    case 'ruin': return (
      <g>
        <path d={`M${L} ${base} V${top + 60} l${w * 0.18} -50 l${w * 0.14} 70 l${w * 0.2} -90 l${w * 0.22} 110 l${w * 0.26} -30 V${base} Z`} fill={wall} stroke={INK} strokeWidth={4} />
        {[0, 1, 2].map((k) => <rect key={k} x={L + 40 + k * (w / 3)} y={base - 200} width={50} height={70} fill="#1a1410" stroke={INK} strokeWidth={3} />)}
        {Array.from({ length: 7 }, (_, k) => <path key={'r' + k} d={`M${L + rnd('ru' + i, k) * w} ${base} l26 -30 l34 10 l18 20 z`} fill={dark(wall, -0.2)} stroke={INK} strokeWidth={2} />)}
      </g>
    );
    default: return null;
  }
};

const StreetItem: React.FC<{ it: Item; x: number; base: number; time: string; snow: boolean; t: number; i: number; nationKey?: string }> = ({ it, x, base, time, snow, t, i, nationKey }) => {
  const night = time === 'night';
  const arg = (it.arg as string) ?? '';
  const y = (it.y as number) ?? base + 120;
  switch (it.item) {
    case 'lamppost': return (
      <g>
        {night ? <ellipse cx={x} cy={y - 330} rx={170} ry={170} fill="#ffd88a" opacity={0.16} /> : null}
        <rect x={x - 7} y={y - 330} width={14} height={330} fill="#2a3030" stroke={INK} strokeWidth={3} />
        <path d={`M${x - 26} ${y - 330} L${x - 18} ${y - 380} H${x + 18} L${x + 26} ${y - 330} Z`} fill={night ? '#ffe49a' : '#cfe0e6'} stroke={INK} strokeWidth={4} />
        <path d={`M${x - 30} ${y - 384} H${x + 30} L${x} ${y - 406} Z`} fill="#2a3030" stroke={INK} strokeWidth={3} />
      </g>
    );
    case 'poster': return (
      <g transform={`translate(${x} ${base - 280}) rotate(${(rnd('sp', i) - 0.5) * 5})`}>
        <rect x={-62} y={-86} width={124} height={172} fill="#efe3c2" stroke={INK} strokeWidth={3} />
        <rect x={-52} y={-74} width={104} height={44} fill={(it.color as string) ?? '#b8392e'} />
        <text x={0} y={-44} textAnchor="middle" fontFamily={FONT.cond} fontWeight={700} fontSize={((it.text as string) ?? '').length > 9 ? 13 : 18} fill="#f7efe0">{((it.text as string) ?? 'BEKANNTMACHUNG').toUpperCase()}</text>
        {[0, 1, 2, 3].map((k) => <rect key={k} x={-48} y={-14 + k * 18} width={k === 3 ? 50 : 96} height={6} fill={INK} opacity={0.5} />)}
      </g>
    );
    case 'cart': return (
      <g transform={`translate(${x} ${y})`}>
        <path d="M-120 -90 H120 L110 -40 H-110 Z" fill="#8a5a32" stroke={INK} strokeWidth={4} />
        <path d="M120 -70 L220 -40" stroke="#5a3e2a" strokeWidth={10} strokeLinecap="round" />
        {[-70, 70].map((dx) => <g key={dx}><circle cx={dx} cy={-34} r={34} fill="none" stroke="#3a2a1a" strokeWidth={8} /><path d={`M${dx - 34} -34 H${dx + 34} M${dx} -68 V0`} stroke="#3a2a1a" strokeWidth={4} /></g>)}
        {snow ? <path d="M-118 -92 q60 -16 236 0 Z" fill="#f2f4f6" /> : null}
      </g>
    );
    case 'bench': return <g transform={`translate(${x} ${y})`}><rect x={-120} y={-70} width={240} height={18} fill="#7a5232" stroke={INK} strokeWidth={3} /><rect x={-120} y={-120} width={240} height={16} fill="#7a5232" stroke={INK} strokeWidth={3} /><path d="M-100 -52 V0 M100 -52 V0" stroke="#2a2a2a" strokeWidth={8} /></g>;
    case 'pump': return <g transform={`translate(${x} ${y})`}><rect x={-22} y={-200} width={44} height={200} fill="#3a5a4a" stroke={INK} strokeWidth={4} /><path d="M22 -150 h40 v26 M-22 -180 L-90 -220" stroke="#3a5a4a" strokeWidth={12} fill="none" strokeLinecap="round" /><ellipse cx={0} cy={0} rx={70} ry={16} fill="#6a6a6a" stroke={INK} strokeWidth={3} /></g>;
    case 'barrels': return <g>{[-50, 50].map((dx, k) => <g key={k} transform={`translate(${x + dx} ${y})`}><path d="M-44 0 Q-52 -55 -44 -110 H44 Q52 -55 44 0 Z" fill="#8a5a32" stroke={INK} strokeWidth={4} /><path d="M-48 -30 H48 M-48 -80 H48" stroke="#3a3a3a" strokeWidth={6} /></g>)}</g>;
    case 'crates': return <g>{[[-60, 0], [60, 0], [0, -110]].map(([dx, dy], k) => <g key={k} transform={`translate(${x + dx} ${y + dy})`}><rect x={-55} y={-110} width={110} height={110} fill="#b88a52" stroke={INK} strokeWidth={4} /><path d="M-55 -110 L55 0 M-55 0 L55 -110" stroke="#8a6232" strokeWidth={5} /></g>)}</g>;
    case 'sandbags': return <g transform={`translate(${x} ${y})`}>{Array.from({ length: 11 }, (_, k) => { const r = k < 5 ? 0 : k < 9 ? 1 : 2; const c = k < 5 ? k : k < 9 ? k - 5 : k - 9; return <rect key={k} x={-160 + c * 66 + r * 33} y={-44 - r * 40} width={64} height={40} rx={16} fill="#bfa87e" stroke={INK} strokeWidth={3} />; })}</g>;
    case 'tree': return (
      <g transform={`translate(${x} ${y})`}>
        <path d="M-12 0 V-220 M0 -160 L-70 -260 M0 -190 L60 -300 M-4 -230 L-20 -330 M-40 -210 L-110 -230" stroke="#4a3424" strokeWidth={16} strokeLinecap="round" />
        {snow ? <path d="M-70 -262 l-6 -6 M60 -302 l6 -6" stroke="#fff" strokeWidth={14} strokeLinecap="round" /> : time === 'day' && !snow && it.arg !== 'bare' ? <circle cx={0} cy={-280} r={110} fill="#4f7a3a" stroke={INK} strokeWidth={4} /> : null}
      </g>
    );
    case 'pole': return <g><rect x={x - 8} y={base - 520} width={16} height={520 + 120} fill="#5a3e2a" stroke={INK} strokeWidth={3} /><path d={`M${x - 50} ${base - 500} H${x + 50}`} stroke="#5a3e2a" strokeWidth={10} /><path d={`M${X0} ${base - 470} Q${x - 500} ${base - 430} ${x - 46} ${base - 504} M${x + 46} ${base - 504} Q${x + 600} ${base - 430} ${X0 + W} ${base - 470}`} stroke={INK} strokeWidth={2} fill="none" /></g>;
    case 'snowbank': return <path d={`M${x - 200} ${y} q40 -70 120 -60 q60 -40 120 0 q60 -10 80 60 Z`} fill="#eef1f3" stroke="#9aa6b0" strokeWidth={3} />;
    case 'banner': return <g>{[0, 1, 2].map((k) => <g key={k} transform={`translate(${x - 300 + k * 300} ${base - 420})`}><rect x={-3} y={0} width={6} height={30} fill="#5a3e2a" /><g transform="translate(-40 20)"><Flag nation={arg || nationKey || 'GER'} w={80} h={120} t={t + k} /></g></g>)}</g>;
    case 'rope': return <g>{[-1, 0, 1].map((k) => <g key={k}><rect x={x + k * 160 - 6} y={y - 110} width={12} height={110} fill="#8a7a4a" stroke={INK} strokeWidth={2} /><ellipse cx={x + k * 160} cy={y} rx={22} ry={7} fill="#5a5040" /></g>)}<path d={`M${x - 160} ${y - 100} Q${x - 80} ${y - 70} ${x} ${y - 100} Q${x + 80} ${y - 70} ${x + 160} ${y - 100}`} stroke="#8a2a2a" strokeWidth={7} fill="none" /></g>;
    default: return null;
  }
};

export const TownKit: React.FC<P> = (p) => {
  const st = TOWN_STYLES[(p.style as string) ?? 'german'] ?? TOWN_STYLES.german;
  const time = (p.time as string) ?? 'day', t = p.t;
  const snow = p.weather === 'snow' || p.ground === 'snow';
  const base = 760;
  const [s0, s1] = SKY[time] ?? SKY.day;
  const bs = ((p.buildings as unknown[]) ?? st.buildings).map(asItem);
  const ws = bs.map((b) => (b.w as number) ?? TOWN_BUILDINGS[b.item]?.w ?? 360);
  const hs = bs.map((b, k) => (b.h as number) ?? (TOWN_BUILDINGS[b.item]?.h ?? 420) * (0.9 + rnd('th' + String(p.seed ?? ''), k) * 0.2));
  // buildings stand shoulder to shoulder across the canvas; a narrow alley gap now and then
  const total = ws.reduce((s, w) => s + w, 0) + (bs.length - 1) * 18;
  let x = 960 - total / 2;
  const xs = ws.map((w) => { const cx = x + w / 2; x += w + 18; return cx; });
  const items = ((p.items as unknown[]) ?? ['lamppost']).map(asItem);
  const ixs = items.map((it, k) => (it.x as number) ?? 260 + ((k + 0.5) * 1400) / items.length);
  const ground = (p.ground as string) ?? (snow ? 'snow' : 'cobbles');
  const gc = ground === 'snow' ? '#e6eaec' : ground === 'mud' ? '#6a5a44' : ground === 'dirt' ? '#a08a62' : time === 'night' ? '#3a3a40' : '#8a8478';
  return (
    <g>
      <defs><linearGradient id="townsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={s0} /><stop offset="1" stopColor={s1} /></linearGradient></defs>
      <rect x={X0} y={Y0} width={W} height={base - Y0} fill="url(#townsky)" />
      {time === 'night' ? Array.from({ length: 40 }, (_, k) => <circle key={k} cx={X0 + rnd('st', k) * W} cy={Y0 + rnd('sy', k) * 500} r={1.6} fill="#fff" opacity={0.6} />) : null}
      <SKYLINE kind={(p.back as string) ?? st.back} y={base - 120} time={time} />
      {/* wall filling the gaps between the buildings */}
      <rect x={X0} y={base - 260} width={W} height={260} fill={dark(st.walls[0], -0.25)} />
      {bs.map((b, k) => <Facade key={k} b={b} x={xs[k]} w={ws[k]} h={hs[k]} base={base} st={st} time={time} snow={snow} t={t} i={k} />)}
      {/* pavement and street */}
      <rect x={X0} y={base} width={W} height={46} fill={ground === 'snow' ? '#f2f4f6' : '#a9a49a'} stroke={INK} strokeWidth={3} />
      <rect x={X0} y={base + 46} width={W} height={Y0 + H - base - 46} fill={gc} />
      {ground === 'cobbles' ? Array.from({ length: 13 * 34 }, (_, k) => { const r = Math.floor(k / 34), c = k % 34; return <rect key={k} x={X0 + c * 72 - (r % 2) * 36} y={base + 52 + r * 36} width={66} height={30} rx={9} fill="#000" opacity={0.06 + rnd('cb', k) * 0.05} />; }) : null}
      {ground === 'snow' ? Array.from({ length: 12 }, (_, k) => <path key={k} d={`M${X0 + rnd('tr', k) * W} ${base + 70 + rnd('tq', k) * 380} q40 -6 80 0`} stroke="#b8c4cc" strokeWidth={5} fill="none" opacity={0.7} />) : null}
      {ground === 'mud' || p.weather === 'rain' ? Array.from({ length: 6 }, (_, k) => <ellipse key={k} cx={X0 + 200 + rnd('pd', k) * (W - 400)} cy={base + 120 + rnd('pq', k) * 300} rx={90 + rnd('pr', k) * 60} ry={14} fill={time === 'night' ? '#2a3448' : '#9ab0c0'} opacity={0.5} />) : null}
      {items.map((it, k) => <StreetItem key={k} it={it} x={ixs[k]} base={base} time={time} snow={snow} t={t} i={k} nationKey={p.nation as string} />)}
      {time === 'night' ? <rect x={X0} y={Y0} width={W} height={H} fill="#081025" opacity={0.22} /> : null}
    </g>
  );
};
