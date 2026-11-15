import React from 'react';
import { INK, SKIN, nation } from '../theme';
import { rnd, clamp } from '../lib/anim';

/**
 * Chibi puppet in the channel style: big head (~45% of height), dot/lid eyes, thin curved limbs,
 * identity from hair / moustache / hat / uniform. Origin = between the feet. Height ≈ 305 px at scale 1.
 */
export type CharSpec = {
  nation?: string;
  outfit?: string; // tunic | suit | navy | navywhite | coat | sailor | civil | dress | party | armor | robe | pilot
  color?: string; // jacket color override
  pants?: string;
  skin?: string;
  hair?: string; // side | back | bald | baldtop | short | part | curly | bun | long | messy | none
  hairColor?: string;
  facial?: string; // toothbrush | walrus | pencil | handlebar | beard | goatee | stubble | none
  hat?: string; // peaked | garrison | helmet_de | helmet_us | helmet_uk | helmet_su | helmet_jp | navy | navy_white | beret | bicorne | kepi | ushanka | fedora | tophat | pith | sailor | pilot | roman | crown | none
  hatColor?: string;
  badge?: string; // hat badge color
  glasses?: string; // round | pince | sun | none
  extra?: string[]; // cigar pipe medals armband epaulettes tie bowtie scarf monocle wrinkles jowls blush
  eyes?: string; // dot | lid | big
  build?: number; // 0.85 thin .. 1.3 fat
  age?: number; // 0 young .. 1 old (wrinkles, grey)
  female?: boolean;
};

export type CharState = {
  pose?: string;
  expr?: string;
  talk?: boolean;
  walk?: number; // walk phase speed (set automatically when moving)
  look?: number; // -1 left .. 1 right (pupil offset)
  view?: 'front' | 'back';
  seated?: boolean;
  holds?: string;
};

const Lw = 4;

// 2-bone IK: returns elbow given shoulder, hand target, lengths, bend direction (+1 outward/down)
function ik(sx: number, sy: number, hx: number, hy: number, l1: number, l2: number, bend: number) {
  let dx = hx - sx, dy = hy - sy;
  let d = Math.hypot(dx, dy);
  const max = l1 + l2 - 0.5;
  if (d > max) {
    dx *= max / d;
    dy *= max / d;
    hx = sx + dx;
    hy = sy + dy;
    d = max;
  }
  const a = (l1 * l1 - l2 * l2 + d * d) / (2 * d);
  const h = Math.sqrt(Math.max(0, l1 * l1 - a * a));
  const mx = sx + (dx * a) / d, my = sy + (dy * a) / d;
  const ex = mx + (bend * h * -dy) / d, ey = my + (bend * h * dx) / d;
  return { ex, ey, hx, hy };
}

type Pose = { r: [number, number]; l: [number, number]; rb?: number; lb?: number };
// hand targets for the character's screen-right (r) and screen-left (l) arm, in body coords
const POSES: Record<string, Pose> = {
  idle: { r: [50, -82], l: [-50, -82] },
  hips: { r: [30, -96], l: [-30, -96], rb: -1, lb: 1 },
  point: { r: [118, -172], l: [-50, -82] },
  pointL: { r: [50, -82], l: [-118, -172] },
  pointUp: { r: [70, -250], l: [-50, -82] },
  raise: { r: [80, -238], l: [-50, -82] },
  cheer: { r: [84, -236], l: [-84, -236] },
  chin: { r: [12, -168], l: [-24, -118], rb: -1, lb: 1 },
  head: { r: [66, -236], l: [-66, -236] },
  face: { r: [26, -212], l: [-26, -212], rb: 1, lb: -1 },
  cross: { r: [-26, -126], l: [26, -122], rb: 1, lb: -1 },
  hold: { r: [20, -118], l: [-20, -118], rb: 1, lb: -1 },
  holdUp: { r: [30, -190], l: [-30, -190], rb: 1, lb: -1 },
  talk: { r: [72, -140], l: [-50, -82] },
  talk2: { r: [72, -140], l: [-72, -140] },
  shrug: { r: [84, -128], l: [-84, -128], rb: 1, lb: -1 },
  salute: { r: [52, -262], l: [-50, -82], rb: 1 },
  phone: { r: [60, -222], l: [-50, -82], rb: 1 },
  binoculars: { r: [22, -228], l: [-22, -228], rb: 1, lb: -1 },
  wave: { r: [76, -240], l: [-50, -82] },
  write: { r: [24, -104], l: [-30, -110], rb: 1, lb: -1 },
  fist: { r: [44, -150], l: [-44, -150], rb: 1, lb: -1 },
  slam: { r: [64, -92], l: [-50, -82] },
  present: { r: [110, -130], l: [-50, -82] },
  cower: { r: [34, -208], l: [-34, -208], rb: 1, lb: -1 },
  wipe: { r: [-8, -262], l: [-50, -82], rb: 1 },
};

const shade = (hex: string, k: number) => {
  const m = hex.replace('#', '');
  if (m.length !== 6) return hex;
  const n = parseInt(m, 16);
  const f = (v: number) => Math.round(clamp(k < 0 ? v * (1 + k) : v + (255 - v) * k, 0, 255));
  const r = f((n >> 16) & 255), g = f((n >> 8) & 255), b = f(n & 255);
  return '#' + ((1 << 24) | (r << 16) | (g << 8) | b).toString(16).slice(1);
};

export const Character: React.FC<{ spec: CharSpec; state: CharState; t: number; seed?: string }> = ({ spec, state, t, seed = 'c' }) => {
  const nat = nation(spec.nation);
  const outfit = spec.outfit ?? 'tunic';
  const jacket = spec.color ?? (outfit === 'navy' ? nat.navy : outfit === 'navywhite' || outfit === 'sailor' ? '#f3f1ea' : outfit === 'suit' ? '#3b3a3f' : outfit === 'civil' ? '#c9b48a' : outfit === 'party' ? '#8a6a3e' : nat.uniform);
  const pants = spec.pants ?? (outfit === 'navywhite' || outfit === 'sailor' ? '#f3f1ea' : outfit === 'suit' || outfit === 'navy' ? shade(jacket, -0.15) : outfit === 'civil' ? '#5a5048' : shade(jacket, -0.22));
  const skin = spec.skin ?? SKIN;
  const hairC = spec.hairColor ?? ((spec.age ?? 0) > 0.7 ? '#c9c4bc' : '#3a2e26');
  const build = spec.build ?? 1;
  const extra = new Set(spec.extra ?? []);
  const expr = state.expr ?? 'neutral';
  const pose = POSES[state.pose ?? 'idle'] ?? POSES.idle;
  const back = state.view === 'back';

  // --- motion ---
  const walking = (state.walk ?? 0) > 0;
  const ph = t * 7.5 + rnd(seed) * 6;
  const bob = walking ? Math.abs(Math.sin(ph)) * -5 : Math.sin(t * 1.6 + rnd(seed, 1) * 6) * 1.2;
  const breathe = 1 + Math.sin(t * 1.6 + rnd(seed, 2) * 6) * 0.008;
  // blink: every ~3-5 s for 0.12 s
  const bp = 3.2 + rnd(seed, 3) * 2;
  const blink = (t + rnd(seed, 4) * bp) % bp < 0.12;
  const talkOpen = state.talk ? (Math.sin(t * 17 + rnd(seed, 5)) * 0.5 + 0.5) * (Math.sin(t * 5.3) * 0.3 + 0.7) : 0;
  const look = (state.look ?? 0) * 4;

  const hy = -242 + bob; // head center
  const shY = -160 + bob * 0.6;
  const shX = 33 * build;
  const hipY = -86;
  const L1 = 44, L2 = 42;

  // arms
  let [rx, ry] = pose.r;
  let [lx, ly] = pose.l;
  if (walking) {
    const s = Math.sin(ph);
    if (state.pose === undefined || state.pose === 'idle') {
      rx = 46; ry = -84 - s * 10; lx = -46; ly = -84 + s * 10;
      rx += s * 14; lx += s * 14;
    }
  }
  if (state.pose === 'wave') rx += Math.sin(t * 9) * 16;
  if (state.pose === 'write') { rx += Math.sin(t * 11) * 6; ry += Math.cos(t * 7) * 3; }
  if (state.pose === 'talk' || state.pose === 'talk2') { ry += Math.sin(t * 3.1 + 1) * 6; rx += Math.sin(t * 2.3) * 4; }
  if (state.pose === 'fist') { const k = Math.abs(Math.sin(t * 6)) * 10; ry -= k; ly -= k; }
  const R = ik(shX, shY, rx * build ** 0.3, ry + bob * 0.6, L1, L2, -(pose.rb ?? 1));
  const Lf = ik(-shX, shY, lx * build ** 0.3, ly + bob * 0.6, L1, L2, pose.lb ?? 1);

  // legs
  const legSw = walking ? Math.sin(ph) * 16 : 0;
  const legW = 16;
  const seated = state.seated;

  const sleeve = jacket;
  const sleeveDark = shade(jacket, -0.25);

  const arm = (side: number, e: { ex: number; ey: number; hx: number; hy: number }) => {
    const d = `M${side * shX} ${shY + 4} L${e.ex} ${e.ey} L${e.hx} ${e.hy}`;
    return (
      <g key={side}>
        <path d={d} stroke={INK} strokeWidth={21} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d={d} stroke={sleeve} strokeWidth={13} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        {/* cuff */}
        <circle cx={e.hx} cy={e.hy} r={11} fill={skin} stroke={INK} strokeWidth={Lw} />
      </g>
    );
  };

  const torsoW = 36 * build;
  const torso = `M${-shX - 2} ${shY - 2} Q0 ${shY - 12} ${shX + 2} ${shY - 2} L${torsoW + 2} ${hipY + 4} Q0 ${hipY + 12} ${-torsoW - 2} ${hipY + 4} Z`;

  const legs = seated ? (
    <g>
      {[-1, 1].map((s) => (
        <g key={s}>
          <path d={`M${s * 15} ${hipY} L${s * 22} ${hipY + 20} L${s * 22} ${hipY + 48}`} stroke={INK} strokeWidth={legW + 8} fill="none" strokeLinecap="round" strokeLinejoin="round" />
          <path d={`M${s * 15} ${hipY} L${s * 22} ${hipY + 20} L${s * 22} ${hipY + 48}`} stroke={pants} strokeWidth={legW} fill="none" strokeLinecap="round" strokeLinejoin="round" />
          <ellipse cx={s * 25} cy={hipY + 52} rx={15} ry={9} fill="#2b2522" stroke={INK} strokeWidth={3} />
        </g>
      ))}
    </g>
  ) : (
    <g>
      {[-1, 1].map((s) => {
        const sw = s * legSw;
        const lift = walking ? Math.max(0, Math.sin(ph * 1 + (s > 0 ? 0 : Math.PI))) * -8 : 0;
        const fx = s * 15 + sw, fy = -8 + lift;
        const knee = `M${s * 14} ${hipY} Q${s * 16 + sw * 0.4} ${-44} ${fx} ${fy}`;
        const boot = outfit === 'suit' || outfit === 'civil' || outfit === 'dress' ? '#2a2420' : '#2b2522';
        return (
          <g key={s}>
            <path d={knee} stroke={INK} strokeWidth={legW + 8} fill="none" strokeLinecap="round" />
            <path d={knee} stroke={pants} strokeWidth={legW} fill="none" strokeLinecap="round" />
            {outfit === 'tunic' || outfit === 'coat' || outfit === 'pilot' ? (
              <path d={`M${fx - 9} ${fy - 26} L${fx + 9} ${fy - 26} L${fx + 9} ${fy} L${fx - 9} ${fy} Z`} fill={boot} stroke={INK} strokeWidth={3} />
            ) : null}
            <ellipse cx={fx + s * 6} cy={fy + 2} rx={17} ry={9} fill={boot} stroke={INK} strokeWidth={3} />
          </g>
        );
      })}
    </g>
  );

  // ---------- body ----------
  const body = (
    <g transform={`translate(0 ${bob * 0.6}) scale(${breathe} 1)`}>
      {outfit === 'coat' ? (
        <path d={`M${-shX - 4} ${shY - 2} Q0 ${shY - 12} ${shX + 4} ${shY - 2} L${torsoW + 14} ${-34} Q0 ${-26} ${-torsoW - 14} ${-34} Z`} fill={jacket} stroke={INK} strokeWidth={Lw} />
      ) : null}
      {outfit === 'dress' ? (
        <path d={`M${-shX} ${shY} L${shX} ${shY} L${torsoW + 24} ${-30} Q0 ${-22} ${-torsoW - 24} ${-30} Z`} fill={jacket} stroke={INK} strokeWidth={Lw} />
      ) : null}
      <path d={torso} fill={jacket} stroke={INK} strokeWidth={Lw} strokeLinejoin="round" />
      {/* side shade */}
      <path d={`M${shX - 8} ${shY + 4} L${torsoW - 4} ${hipY + 2} L${torsoW + 1} ${hipY + 4} L${shX + 1} ${shY}`} fill={sleeveDark} opacity={0.45} />
      {back ? null : <Outfit outfit={outfit} jacket={jacket} shY={shY} hipY={hipY} w={torsoW} nat={spec.nation} extra={extra} />}
      {extra.has('armband') ? (
        <g>
          <path d={`M${shX - 2} ${shY + 24} l14 4 l-3 14 l-14 -4 z`} fill="#c8352b" stroke={INK} strokeWidth={2.5} />
          <circle cx={shX + 3} cy={shY + 33} r={4.2} fill="#fff" />
        </g>
      ) : null}
    </g>
  );

  return (
    <g>
      <ellipse cx={0} cy={2} rx={58 * build} ry={10} fill="#000" opacity={0.16} />
      {legs}
      {body}
      {back ? null : null}
      <Head spec={spec} expr={expr} blink={blink} talk={talkOpen} look={look} hy={hy} hairC={hairC} skin={skin} back={back} extra={extra} t={t} seed={seed} />
      {back ? null : (
        <>
          {arm(-1, Lf)}
          {arm(1, R)}
        </>
      )}
      {back ? (
        <>
          {arm(-1, Lf)}
          {arm(1, R)}
        </>
      ) : null}
    </g>
  );
};

const Outfit: React.FC<{ outfit: string; jacket: string; shY: number; hipY: number; w: number; nat?: string; extra: Set<string> }> = ({ outfit, jacket, shY, hipY, w, extra }) => {
  const dark = shade(jacket, -0.3);
  const btn = outfit === 'navy' ? '#e3b94a' : outfit === 'navywhite' ? '#d9b44a' : shade(jacket, -0.45);
  switch (outfit) {
    case 'suit':
      return (
        <g>
          <path d={`M-14 ${shY - 4} L0 ${shY + 34} L14 ${shY - 4} Z`} fill="#f4f1ea" stroke={INK} strokeWidth={3} />
          {extra.has('bowtie') ? (
            <path d={`M-12 ${shY + 2} L0 ${shY + 7} L12 ${shY + 2} L12 ${shY + 14} L0 ${shY + 9} L-12 ${shY + 14} Z`} fill="#8b1d24" stroke={INK} strokeWidth={2.5} />
          ) : (
            <path d={`M-5 ${shY + 2} L5 ${shY + 2} L7 ${shY + 34} L0 ${shY + 42} L-7 ${shY + 34} Z`} fill={extra.has('redtie') ? '#a8262a' : '#3c4a6b'} stroke={INK} strokeWidth={2.5} />
          )}
          <path d={`M-18 ${shY - 4} L-2 ${shY + 44} M18 ${shY - 4} L2 ${shY + 44}`} stroke={INK} strokeWidth={3} />
          <circle cx={0} cy={shY + 56} r={3} fill={INK} />
        </g>
      );
    case 'navy':
    case 'navywhite':
      return (
        <g>
          <path d={`M-12 ${shY - 4} L0 ${shY + 20} L12 ${shY - 4}`} fill="#f4f1ea" stroke={INK} strokeWidth={3} />
          {outfit === 'navy' ? <path d={`M-4 ${shY + 2} L4 ${shY + 2} L5 ${shY + 22} L-5 ${shY + 22} Z`} fill="#1b1b1b" /> : null}
          {[0, 1, 2].map((i) => (
            <g key={i}>
              <circle cx={-11} cy={shY + 30 + i * 18} r={3.4} fill={btn} stroke={INK} strokeWidth={1.5} />
              <circle cx={11} cy={shY + 30 + i * 18} r={3.4} fill={btn} stroke={INK} strokeWidth={1.5} />
            </g>
          ))}
          {outfit === 'navywhite' ? (
            <path d={`M-26 ${shY + 4} l12 0 M14 ${shY + 4} l12 0`} stroke="#2a3550" strokeWidth={5} />
          ) : (
            <path d={`M${-w + 4} ${hipY - 8} l14 0 M${w - 18} ${hipY - 8} l14 0`} stroke="#e3b94a" strokeWidth={3} />
          )}
        </g>
      );
    case 'sailor':
      return (
        <g>
          <path d={`M-30 ${shY - 2} L30 ${shY - 2} L22 ${shY + 22} L0 ${shY + 38} L-22 ${shY + 22} Z`} fill="#2c3f6b" stroke={INK} strokeWidth={3} />
          <path d={`M-24 ${shY + 18} L0 ${shY + 33} L24 ${shY + 18}`} stroke="#fff" strokeWidth={2.5} fill="none" />
          <path d={`M-6 ${shY + 34} L0 ${shY + 48} L6 ${shY + 34} Z`} fill="#1b1b1b" />
        </g>
      );
    case 'civil':
      return (
        <g>
          <path d={`M-12 ${shY - 4} L0 ${shY + 12} L12 ${shY - 4}`} fill="none" stroke={INK} strokeWidth={3} />
          <path d={`M0 ${shY + 12} L0 ${hipY}`} stroke={dark} strokeWidth={2} />
          {[0, 1, 2].map((i) => <circle key={i} cx={4} cy={shY + 24 + i * 16} r={2.4} fill={dark} />)}
        </g>
      );
    case 'dress':
    case 'robe':
      return <path d={`M-10 ${shY - 4} Q0 ${shY + 12} 10 ${shY - 4}`} fill="none" stroke={INK} strokeWidth={3} />;
    case 'armor':
      return (
        <g>
          {[0, 1, 2, 3].map((i) => <path key={i} d={`M${-w + 2} ${shY + 18 + i * 15} Q0 ${shY + 26 + i * 15} ${w - 2} ${shY + 18 + i * 15}`} stroke={INK} strokeWidth={2.5} fill="none" />)}
        </g>
      );
    default: {
      // military tunic: collar, buttons, pockets, belt
      const party = outfit === 'party';
      return (
        <g>
          <path d={`M-16 ${shY - 4} L0 ${shY + 22} L16 ${shY - 4}`} fill={party ? '#f0ece2' : shade(jacket, -0.1)} stroke={INK} strokeWidth={3} />
          {party || extra.has('tie') ? <path d={`M-4 ${shY + 4} L4 ${shY + 4} L5 ${shY + 22} L0 ${shY + 26} L-5 ${shY + 22} Z`} fill="#3a2b22" /> : null}
          <path d={`M-16 ${shY - 2} l-8 8 l8 4 z M16 ${shY - 2} l8 8 l-8 4 z`} fill={dark} stroke={INK} strokeWidth={2} />
          {[0, 1, 2, 3].map((i) => <circle key={i} cx={0} cy={shY + 30 + i * 13} r={2.8} fill={btn} />)}
          <path d={`M-28 ${shY + 30} h18 v12 h-18 z M10 ${shY + 30} h18 v12 h-18 z`} fill="none" stroke={dark} strokeWidth={2.5} />
          <path d={`M${-w - 1} ${hipY - 12} L${w + 1} ${hipY - 12}`} stroke="#3a2b22" strokeWidth={8} />
          <rect x={-7} y={hipY - 17} width={14} height={10} rx={2} fill="#c9a24a" stroke={INK} strokeWidth={1.5} />
          {extra.has('medals') ? (
            <g>
              {[0, 1, 2].map((i) => (
                <g key={i}>
                  <rect x={-30 + i * 7} y={shY + 14} width={6} height={9} fill={['#c8352b', '#3a6ea5', '#e3b94a'][i]} />
                  <circle cx={-27 + i * 7} cy={shY + 27} r={3.5} fill="#e3b94a" stroke={INK} strokeWidth={1} />
                </g>
              ))}
            </g>
          ) : null}
          {extra.has('epaulettes') ? <path d={`M-40 ${shY - 2} h16 M24 ${shY - 2} h16`} stroke="#e3b94a" strokeWidth={6} strokeLinecap="round" /> : null}
          {extra.has('ironcross') ? <path d={`M-4 ${shY + 2} h8 v-0 M0 ${shY - 2} v8`} stroke="#1b1b1b" strokeWidth={4} /> : null}
          {extra.has('star') ? <circle cx={-20} cy={shY + 20} r={5} fill="#e3b94a" stroke={INK} strokeWidth={1.5} /> : null}
        </g>
      );
    }
  }
};

const Head: React.FC<{
  spec: CharSpec; expr: string; blink: boolean; talk: number; look: number; hy: number; hairC: string; skin: string; back: boolean; extra: Set<string>; t: number; seed: string;
}> = ({ spec, expr, blink, talk, look, hy, hairC, skin, back, extra, t }) => {
  const rx = 68, ry = 63;
  const jowl = extra.has('jowls') || (spec.build ?? 1) > 1.15;
  const age = spec.age ?? 0.3;
  const face = jowl
    ? `M${-rx} ${hy - 6} C${-rx} ${hy - 106} ${rx} ${hy - 106} ${rx} ${hy - 6} C${rx + 4} ${hy + 62} ${-rx - 4} ${hy + 62} ${-rx} ${hy - 6} Z`
    : `M${-rx} ${hy} C${-rx} ${hy - 98} ${rx} ${hy - 98} ${rx} ${hy} C${rx} ${hy + 60} ${-rx} ${hy + 60} ${-rx} ${hy} Z`;
  const hat = spec.hat ?? 'none';
  const hatC = spec.hatColor ?? nation(spec.nation).uniform;

  if (back) {
    return (
      <g>
        <path d={face} fill={hat === 'pilot' ? '#7a4a2a' : hairC} stroke={INK} strokeWidth={Lw} />
        <ellipse cx={-rx + 2} cy={hy + 4} rx={8} ry={13} fill={skin} stroke={INK} strokeWidth={3} />
        <ellipse cx={rx - 2} cy={hy + 4} rx={8} ry={13} fill={skin} stroke={INK} strokeWidth={3} />
        <Hat kind={hat} color={hatC} hy={hy} badge={spec.badge} nationKey={spec.nation} back />
      </g>
    );
  }

  const eyeY = hy - 4;
  const ex = 24;
  const eyesKind = spec.eyes ?? 'dot';
  const sweat = expr === 'worried' || expr === 'sweat' || expr === 'panic' || expr === 'nervous';
  const browY = eyeY - 22 + (expr === 'shocked' || expr === 'panic' ? -8 : 0);
  const browC = hairC === '#c9c4bc' ? '#9a948c' : hairC;
  const brow = (s: number) => {
    let a = 0; // tilt: positive = inner end down (angry)
    if (expr === 'angry' || expr === 'determined' || expr === 'smug') a = 8;
    if (expr === 'worried' || expr === 'sad' || expr === 'cry' || expr === 'panic' || expr === 'nervous' || expr === 'sweat') a = -9;
    const ix = s * 8, ox = s * 38;
    return <path key={s} d={`M${ix} ${browY + a} Q${s * 23} ${browY - 5} ${ox} ${browY - a * 0.4}`} stroke={browC} strokeWidth={extra.has('thickbrows') ? 8 : 5} fill="none" strokeLinecap="round" />;
  };
  const eye = (s: number) => {
    const x = s * ex + look;
    if (blink || expr === 'happy' || expr === 'laugh') return <path key={s} d={`M${x - 9} ${eyeY + (expr === 'happy' || expr === 'laugh' ? 3 : 0)} Q${x} ${eyeY - (expr === 'happy' || expr === 'laugh' ? 9 : -3)} ${x + 9} ${eyeY + (expr === 'happy' || expr === 'laugh' ? 3 : 0)}`} stroke={INK} strokeWidth={4} fill="none" strokeLinecap="round" />;
    if (expr === 'cry' || expr === 'sad') return <path key={s} d={`M${x - 9} ${eyeY} Q${x} ${eyeY + 6} ${x + 9} ${eyeY}`} stroke={INK} strokeWidth={4} fill="none" strokeLinecap="round" />;
    if (expr === 'shocked' || expr === 'panic' || eyesKind === 'big')
      return (
        <g key={s}>
          <ellipse cx={x} cy={eyeY} rx={12} ry={14} fill="#fff" stroke={INK} strokeWidth={3} />
          <circle cx={x + look * 0.6} cy={eyeY + 1} r={expr === 'panic' ? 3.5 : 5} fill={INK} />
        </g>
      );
    if (eyesKind === 'lid' || expr === 'smug' || expr === 'tired')
      return (
        <g key={s}>
          <path d={`M${x - 11} ${eyeY - 1} Q${x} ${eyeY - 7} ${x + 11} ${eyeY - 1}`} stroke={INK} strokeWidth={4} fill="none" strokeLinecap="round" />
          <path d={`M${x - 7} ${eyeY + 1} Q${x} ${eyeY + 5} ${x + 7} ${eyeY + 1}`} stroke={INK} strokeWidth={3.5} fill="none" strokeLinecap="round" />
        </g>
      );
    return <ellipse key={s} cx={x} cy={eyeY} rx={expr === 'angry' ? 5 : 5.5} ry={expr === 'angry' ? 5 : 7} fill={INK} />;
  };

  const my = hy + 33;
  let mouth: React.ReactNode;
  const open = Math.max(talk, expr === 'shocked' || expr === 'panic' || expr === 'shout' || expr === 'laugh' ? 1 : 0);
  if (open > 0.15) {
    const h = 4 + open * (expr === 'shout' || expr === 'panic' ? 16 : 10);
    mouth = (
      <g>
        <ellipse cx={0} cy={my + 2} rx={expr === 'shocked' ? 8 : 11} ry={h} fill="#6b2a26" stroke={INK} strokeWidth={3} />
        <ellipse cx={0} cy={my + 2 + h * 0.5} rx={6} ry={Math.max(1, h * 0.35)} fill="#d9787a" />
      </g>
    );
  } else if (expr === 'happy' || expr === 'smile' || expr === 'smug') {
    mouth = <path d={`M-14 ${my - 2} Q0 ${my + (expr === 'smug' ? 5 : 11)} 14 ${my - (expr === 'smug' ? 6 : 2)}`} stroke={INK} strokeWidth={4} fill="none" strokeLinecap="round" />;
  } else if (expr === 'angry' || expr === 'determined') {
    mouth = expr === 'angry' ? (
      <g>
        <rect x={-13} y={my - 4} width={26} height={11} rx={3} fill="#fff" stroke={INK} strokeWidth={3} />
        <path d={`M-13 ${my + 1.5} h26`} stroke={INK} strokeWidth={1.5} />
      </g>
    ) : <path d={`M-12 ${my} h24`} stroke={INK} strokeWidth={4} strokeLinecap="round" />;
  } else if (expr === 'sad' || expr === 'cry' || expr === 'worried' || expr === 'nervous') {
    mouth = expr === 'nervous'
      ? <path d={`M-14 ${my} q4 -5 8 0 q4 5 8 0 q4 -5 8 0`} stroke={INK} strokeWidth={3.5} fill="none" strokeLinecap="round" />
      : <path d={`M-12 ${my + 4} Q0 ${my - 6} 12 ${my + 4}`} stroke={INK} strokeWidth={4} fill="none" strokeLinecap="round" />;
  } else {
    mouth = <path d={`M-9 ${my} Q0 ${my + 3} 9 ${my}`} stroke={INK} strokeWidth={3.5} fill="none" strokeLinecap="round" />;
  }

  const redFace = expr === 'angry' || expr === 'rage';
  return (
    <g>
      {/* ears */}
      <ellipse cx={-rx + 1} cy={hy + 2} rx={9} ry={14} fill={skin} stroke={INK} strokeWidth={3} />
      <ellipse cx={rx - 1} cy={hy + 2} rx={9} ry={14} fill={skin} stroke={INK} strokeWidth={3} />
      <path d={face} fill={skin} stroke={INK} strokeWidth={Lw} />
      {redFace ? <path d={face} fill="#e0504a" opacity={0.28} /> : null}
      {/* chin shade */}
      <path d={`M${-rx + 14} ${hy + 32} Q0 ${hy + 62} ${rx - 14} ${hy + 32} Q0 ${hy + 52} ${-rx + 14} ${hy + 32}`} fill="#e6bfa2" opacity={0.6} />
      {extra.has('stubble') || spec.facial === 'stubble' ? <path d={`M${-rx + 12} ${hy + 24} Q0 ${hy + 66} ${rx - 12} ${hy + 24} Q0 ${hy + 46} ${-rx + 12} ${hy + 24}`} fill="#8c7f72" opacity={0.35} /> : null}
      {extra.has('blush') || expr === 'happy' || expr === 'smile' ? (
        <>
          <ellipse cx={-40} cy={hy + 14} rx={10} ry={6} fill="#ef8f8f" opacity={0.45} />
          <ellipse cx={40} cy={hy + 14} rx={10} ry={6} fill="#ef8f8f" opacity={0.45} />
        </>
      ) : null}
      {age > 0.55 || extra.has('wrinkles') ? (
        <g stroke="#b88f74" strokeWidth={2.5} fill="none" strokeLinecap="round">
          <path d={`M-18 ${hy - 44} q18 -5 36 0`} />
          <path d={`M-14 ${hy - 37} q14 -4 28 0`} />
          <path d={`M-36 ${eyeY + 12} q5 3 10 0 M26 ${eyeY + 12} q5 3 10 0`} />
          <path d={`M-22 ${my - 10} q-6 6 -4 12 M22 ${my - 10} q6 6 4 12`} />
        </g>
      ) : null}
      <Hair kind={spec.hair ?? 'short'} color={hairC} hy={hy} rx={rx} hat={hat} />
      {[-1, 1].map(brow)}
      {[-1, 1].map(eye)}
      {/* nose */}
      <path d={`M-3 ${hy + 8} q4 5 8 0`} stroke="#b88f74" strokeWidth={3} fill="none" strokeLinecap="round" />
      <Facial kind={spec.facial ?? 'none'} color={hairC === '#c9c4bc' ? '#a29c94' : hairC} my={my} />
      {mouth}
      {spec.glasses && spec.glasses !== 'none' ? <Glasses kind={spec.glasses} eyeY={eyeY} ex={ex} /> : null}
      {extra.has('monocle') ? <circle cx={ex} cy={eyeY} r={13} fill="#dfeff7" opacity={0.6} stroke={INK} strokeWidth={2.5} /> : null}
      {extra.has('cigar') ? (
        <g>
          <path d={`M14 ${my + 2} l42 8`} stroke={INK} strokeWidth={10} strokeLinecap="round" />
          <path d={`M14 ${my + 2} l42 8`} stroke="#7a4a28" strokeWidth={6} strokeLinecap="round" />
          <circle cx={57} cy={my + 10} r={3} fill="#f08a3a" />
          <circle cx={64 + Math.sin(t * 2) * 3} cy={my - 8 - ((t * 20) % 30)} r={4 + ((t * 20) % 30) / 8} fill="#ddd" opacity={0.6 - ((t * 20) % 30) / 60} />
        </g>
      ) : null}
      {extra.has('pipe') ? <path d={`M10 ${my + 4} q20 6 30 0 v-14 h12 v18 q-4 8 -14 6`} fill="#5a3a22" stroke={INK} strokeWidth={3} /> : null}
      {extra.has('cigarette') ? <path d={`M12 ${my + 2} l46 -10`} stroke="#1b1b1b" strokeWidth={4} /> : null}
      {sweat ? <Sweat hy={hy} t={t} /> : null}
      {expr === 'cry' ? (
        <g fill="#7cc4f0" stroke={INK} strokeWidth={2}>
          <path d={`M${-ex - 4} ${eyeY + 6} q-6 ${14 + ((t * 30) % 20)} 0 ${18 + ((t * 30) % 20)} q6 -4 0 ${-18 - ((t * 30) % 20)}`} />
          <path d={`M${ex + 4} ${eyeY + 6} q-6 ${14 + ((t * 30 + 9) % 20)} 0 ${18 + ((t * 30 + 9) % 20)} q6 -4 0 ${-18 - ((t * 30 + 9) % 20)}`} />
        </g>
      ) : null}
      <Hat kind={hat} color={hatC} hy={hy} badge={spec.badge} nationKey={spec.nation} />
      {expr === 'angry' || expr === 'rage' ? <path d={`M${rx - 18} ${hy - 62} l10 -6 m-4 14 l12 -2 m-20 -16 l2 -12`} stroke="#c8352b" strokeWidth={4} strokeLinecap="round" /> : null}
    </g>
  );
};

const Sweat: React.FC<{ hy: number; t: number }> = ({ hy, t }) => {
  const k = (t * 0.9) % 1;
  return (
    <g>
      <path d={`M78 ${hy - 50} q-11 18 0 24 q11 -6 0 -24`} fill="#8fd0f5" stroke={INK} strokeWidth={2.5} />
      <path d={`M-74 ${hy - 30 + k * 30} q-8 13 0 18 q8 -5 0 -18`} fill="#8fd0f5" stroke={INK} strokeWidth={2.5} opacity={1 - k} />
    </g>
  );
};

const Hair: React.FC<{ kind: string; color: string; hy: number; rx: number; hat: string }> = ({ kind, color, hy, rx, hat }) => {
  const top = hy - 72;
  const covered = hat !== 'none' && hat !== 'beret' && hat !== 'garrison';
  switch (kind) {
    case 'none':
      return null;
    case 'bald':
    case 'baldtop':
      return (
        <g fill={color} stroke={INK} strokeWidth={3}>
          <path d={`M${-rx + 1} ${hy - 4} q-2 -26 14 -36 q-2 16 2 36 z`} />
          <path d={`M${rx - 1} ${hy - 4} q2 -26 -14 -36 q2 16 -2 36 z`} />
          {kind === 'baldtop' ? <path d={`M-14 ${top - 1} q14 -6 28 0`} fill="none" strokeWidth={2.5} stroke={color} /> : null}
          {kind === 'bald' ? <ellipse cx={-22} cy={top + 10} rx={14} ry={6} fill="#fff" stroke="none" opacity={0.45} /> : null}
        </g>
      );
    case 'side':
      // dark cap of hair with a heavy fringe swept to one side
      return (
        <g>
          <path d={`M${-rx} ${hy - 2} C${-rx - 4} ${hy - 104} ${rx + 4} ${hy - 104} ${rx} ${hy - 2} C${rx - 6} ${hy - 30} ${rx - 14} ${hy - 38} ${rx - 22} ${hy - 44} L${-30} ${hy - 22} C${-46} ${hy - 30} ${-rx + 6} ${hy - 30} ${-rx} ${hy - 2} Z`} fill={color} stroke={INK} strokeWidth={Lw} />
          <path d={`M${rx - 8} ${hy - 50} C${30} ${hy - 44} ${-6} ${hy - 30} ${-34} ${hy - 12} C${-30} ${hy - 30} ${-14} ${hy - 50} ${8} ${hy - 62} Z`} fill={color} stroke={INK} strokeWidth={3} strokeLinejoin="round" />
          <path d={`M${-10} ${hy - 70} Q${20} ${hy - 66} ${rx - 24} ${hy - 52}`} stroke="#fff" strokeOpacity={0.25} strokeWidth={4} fill="none" />
        </g>
      );
    case 'back':
      return (
        <g>
          <path d={`M${-rx - 2} ${hy - 4} C${-rx - 6} ${hy - 108} ${rx + 6} ${hy - 108} ${rx + 2} ${hy - 4} C${rx - 6} ${hy - 40} ${rx - 16} ${hy - 50} 0 ${hy - 50} C${-rx + 16} ${hy - 50} ${-rx + 6} ${hy - 40} ${-rx - 2} ${hy - 4} Z`} fill={color} stroke={INK} strokeWidth={Lw} />
          <path d={`M-30 ${hy - 70} q30 -10 60 0 M-40 ${hy - 60} q40 -12 80 0`} stroke="#fff" strokeOpacity={0.22} strokeWidth={3} fill="none" />
        </g>
      );
    case 'part':
      return (
        <path d={`M${-rx} ${hy - 4} C${-rx - 4} ${hy - 106} ${rx + 4} ${hy - 106} ${rx} ${hy - 4} C${rx - 4} ${hy - 34} ${rx - 12} ${hy - 44} ${-12} ${hy - 48} L${-20} ${hy - 62} C${-34} ${hy - 44} ${-rx + 4} ${hy - 34} ${-rx} ${hy - 4} Z`} fill={color} stroke={INK} strokeWidth={Lw} />
      );
    case 'curly':
      return (
        <g fill={color} stroke={INK} strokeWidth={3}>
          {[-56, -34, -12, 12, 34, 56].map((x, i) => <circle key={i} cx={x} cy={top + 8 + Math.abs(x) * 0.35} r={17} />)}
        </g>
      );
    case 'bun':
    case 'long':
      return (
        <g>
          {kind === 'long' ? <path d={`M${-rx - 6} ${hy - 10} Q${-rx - 14} ${hy + 60} ${-rx + 10} ${hy + 70} L${rx - 10} ${hy + 70} Q${rx + 14} ${hy + 60} ${rx + 6} ${hy - 10} Z`} fill={color} stroke={INK} strokeWidth={Lw} /> : <circle cx={0} cy={top - 12} r={20} fill={color} stroke={INK} strokeWidth={Lw} />}
          <path d={`M${-rx} ${hy - 4} C${-rx - 4} ${hy - 106} ${rx + 4} ${hy - 106} ${rx} ${hy - 4} C${rx - 10} ${hy - 40} ${10} ${hy - 50} 0 ${hy - 46} C${-10} ${hy - 50} ${-rx + 10} ${hy - 40} ${-rx} ${hy - 4} Z`} fill={color} stroke={INK} strokeWidth={Lw} />
        </g>
      );
    case 'messy':
      return <path d={`M${-rx} ${hy - 6} l4 -40 l10 8 l6 -30 l12 16 l10 -24 l12 18 l12 -20 l8 20 l14 -12 l2 30 l12 -4 l-6 36 Q0 ${hy - 46} ${-rx} ${hy - 6} Z`} fill={color} stroke={INK} strokeWidth={Lw} strokeLinejoin="round" />;
    default: // short
      if (covered) return <path d={`M${-rx + 2} ${hy - 6} q4 -24 16 -30 L${-rx + 16} ${hy - 4} Z M${rx - 2} ${hy - 6} q-4 -24 -16 -30 L${rx - 16} ${hy - 4} Z`} fill={color} stroke={INK} strokeWidth={3} />;
      return <path d={`M${-rx} ${hy - 6} C${-rx - 4} ${hy - 106} ${rx + 4} ${hy - 106} ${rx} ${hy - 6} C${rx - 8} ${hy - 38} ${rx - 20} ${hy - 44} 0 ${hy - 44} C${-rx + 20} ${hy - 44} ${-rx + 8} ${hy - 38} ${-rx} ${hy - 6} Z`} fill={color} stroke={INK} strokeWidth={Lw} />;
  }
};

const Facial: React.FC<{ kind: string; color: string; my: number }> = ({ kind, color, my }) => {
  const y = my - 9;
  switch (kind) {
    case 'toothbrush':
      return <rect x={-10} y={y - 6} width={20} height={11} rx={2} fill={color} stroke={INK} strokeWidth={2} />;
    case 'walrus':
      return <path d={`M-34 ${y + 10} Q-26 ${y - 12} 0 ${y - 4} Q26 ${y - 12} 34 ${y + 10} Q20 ${y + 2} 0 ${y + 6} Q-20 ${y + 2} -34 ${y + 10} Z`} fill={color} stroke={INK} strokeWidth={2.5} />;
    case 'pencil':
      return <path d={`M-16 ${y + 2} Q0 ${y - 4} 16 ${y + 2}`} stroke={color} strokeWidth={4} fill="none" strokeLinecap="round" />;
    case 'handlebar':
      return <path d={`M0 ${y} Q-20 ${y - 6} -30 ${y + 2} q-6 -10 2 -14 M0 ${y} Q20 ${y - 6} 30 ${y + 2} q6 -10 -2 -14`} stroke={color} strokeWidth={6} fill="none" strokeLinecap="round" />;
    case 'beard':
      return <path d={`M-60 ${y - 16} Q-58 ${y + 44} 0 ${y + 52} Q58 ${y + 44} 60 ${y - 16} Q46 ${y + 18} 20 ${y + 2} Q0 ${y - 4} -20 ${y + 2} Q-46 ${y + 18} -60 ${y - 16} Z`} fill={color} stroke={INK} strokeWidth={3} />;
    case 'goatee':
      return <path d={`M-10 ${y + 22} Q0 ${y + 44} 10 ${y + 22} Z M-18 ${y + 2} Q0 ${y - 6} 18 ${y + 2}`} fill={color} stroke={color} strokeWidth={4} />;
    default:
      return null;
  }
};

const Glasses: React.FC<{ kind: string; eyeY: number; ex: number }> = ({ kind, eyeY, ex }) => {
  if (kind === 'sun')
    return (
      <g>
        <path d={`M${-ex - 18} ${eyeY - 9} h34 l-4 18 h-26 z M${ex - 16} ${eyeY - 9} h34 l-4 18 h-26 z`} fill="#1b1b1b" stroke={INK} strokeWidth={2} />
        <path d={`M-2 ${eyeY - 6} h4`} stroke={INK} strokeWidth={3} />
      </g>
    );
  const r = kind === 'pince' ? 11 : 15;
  return (
    <g fill="#e8f4fa" fillOpacity={0.35} stroke={INK} strokeWidth={3}>
      <circle cx={-ex} cy={eyeY} r={r} />
      <circle cx={ex} cy={eyeY} r={r} />
      <path d={`M${-ex + r} ${eyeY - 2} Q0 ${eyeY - 8} ${ex - r} ${eyeY - 2}`} fill="none" />
      {kind === 'round' ? <path d={`M${-ex - r} ${eyeY - 2} l-24 -4 M${ex + r} ${eyeY - 2} l24 -4`} fill="none" /> : null}
    </g>
  );
};

export const Hat: React.FC<{ kind: string; color: string; hy: number; badge?: string; nationKey?: string; back?: boolean }> = ({ kind, color, hy, badge, nationKey, back }) => {
  const top = hy - 70;
  const dark = shade(color, -0.35);
  const nat = nation(nationKey);
  const b = badge ?? (nat.mark === 'star' ? '#c8352b' : nat.mark === 'whitestar' ? '#e3b94a' : '#d9c27a');
  const emblem = (x: number, y: number, s = 1) =>
    back ? null : nat.mark === 'star' ? (
      <path transform={`translate(${x} ${y}) scale(${s})`} d="M0 -10 L2.9 -3.1 L10 -3.1 L4.3 1.2 L6.5 8.1 L0 3.8 L-6.5 8.1 L-4.3 1.2 L-10 -3.1 L-2.9 -3.1 Z" fill="#c8352b" stroke={INK} strokeWidth={1.2} />
    ) : nat.mark === 'sun' ? (
      <path transform={`translate(${x} ${y}) scale(${s})`} d="M0 -9 L2.6 -2.8 L9 -2.8 L3.9 1.1 L5.8 7.3 L0 3.4 L-5.8 7.3 L-3.9 1.1 L-9 -2.8 L-2.6 -2.8 Z" fill="#e3b94a" stroke={INK} strokeWidth={1.2} />
    ) : (
      <ellipse cx={x} cy={y} rx={9 * s} ry={6 * s} fill={b} stroke={INK} strokeWidth={1.5} />
    );
  switch (kind) {
    case 'peaked':
    case 'navy':
    case 'navy_white': {
      const crown = kind === 'navy_white' ? '#f6f4ee' : kind === 'navy' ? '#1d2436' : color;
      const band = kind === 'peaked' ? (nat.mark === 'star' ? '#c8352b' : dark) : '#141414';
      return (
        <g>
          <path d={`M-80 ${top + 6} Q-84 ${top - 30} 0 ${top - 34} Q84 ${top - 30} 80 ${top + 6} Q0 ${top + 22} -80 ${top + 6} Z`} fill={crown} stroke={INK} strokeWidth={Lw} />
          <path d={`M-64 ${top + 4} L64 ${top + 4} L62 ${top + 24} Q0 ${top + 34} -62 ${top + 24} Z`} fill={band} stroke={INK} strokeWidth={Lw} />
          {back ? null : <path d={`M-58 ${top + 24} Q0 ${top + 50} 58 ${top + 24} Q0 ${top + 34} -58 ${top + 24} Z`} fill="#1b1b1b" stroke={INK} strokeWidth={3} />}
          {kind !== 'peaked' && !back ? <path d={`M-12 ${top + 2} l12 -12 l12 12 l-12 8 z`} fill="#e3b94a" stroke={INK} strokeWidth={1.5} /> : emblem(0, top + 13, 1)}
          {kind === 'peaked' && !back ? <path d={`M-22 ${top - 4} Q0 ${top - 16} 22 ${top - 4}`} stroke="#d9c27a" strokeWidth={3} fill="none" /> : null}
        </g>
      );
    }
    case 'garrison':
      return (
        <g>
          <path d={`M-58 ${top + 14} L-40 ${top - 18} L52 ${top - 12} L60 ${top + 14} Z`} fill={color} stroke={INK} strokeWidth={Lw} strokeLinejoin="round" />
          <path d={`M-58 ${top + 14} L60 ${top + 14} L58 ${top + 2} L-56 ${top + 2} Z`} fill={dark} stroke={INK} strokeWidth={3} />
          {emblem(-24, top - 2, 0.8)}
        </g>
      );
    case 'helmet_de':
      return (
        <g>
          <path d={`M-74 ${top + 34} Q-86 ${top + 40} -88 ${top + 54} L-70 ${top + 48} L-70 ${top + 10} C-70 ${top - 50} 70 ${top - 50} 70 ${top + 10} L70 ${top + 48} L88 ${top + 54} Q86 ${top + 40} 74 ${top + 34} Z`} fill={color} stroke={INK} strokeWidth={Lw} strokeLinejoin="round" />
          <path d={`M-70 ${top + 22} Q0 ${top + 36} 70 ${top + 22}`} stroke={dark} strokeWidth={3} fill="none" />
          <path d={`M-40 ${top - 20} Q-10 ${top - 34} 20 ${top - 30}`} stroke="#fff" strokeOpacity={0.25} strokeWidth={6} fill="none" strokeLinecap="round" />
        </g>
      );
    case 'helmet_us':
    case 'helmet_su':
    case 'helmet_jp':
      return (
        <g>
          <path d={`M-80 ${top + 30} C-80 ${top - 52} 80 ${top - 52} 80 ${top + 30} Q0 ${top + 42} -80 ${top + 30} Z`} fill={color} stroke={INK} strokeWidth={Lw} />
          <path d={`M-84 ${top + 30} Q0 ${top + 46} 84 ${top + 30}`} stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" />
          {kind === 'helmet_su' ? <path d={`M0 ${top - 34} v20`} stroke={dark} strokeWidth={4} /> : null}
          {kind === 'helmet_us' ? <path d={`M-76 ${top + 4} Q0 ${top - 6} 76 ${top + 4}`} stroke={dark} strokeWidth={2} strokeDasharray="6 6" fill="none" /> : null}
          {kind !== 'helmet_us' ? emblem(0, top - 4, 1.1) : null}
          <path d={`M-44 ${top - 18} Q-14 ${top - 34} 18 ${top - 30}`} stroke="#fff" strokeOpacity={0.22} strokeWidth={6} fill="none" strokeLinecap="round" />
        </g>
      );
    case 'helmet_uk':
      return (
        <g>
          <path d={`M-104 ${top + 20} Q0 ${top + 46} 104 ${top + 20} Q0 ${top + 30} -104 ${top + 20} Z`} fill={color} stroke={INK} strokeWidth={Lw} />
          <path d={`M-58 ${top + 22} C-58 ${top - 40} 58 ${top - 40} 58 ${top + 22} Z`} fill={color} stroke={INK} strokeWidth={Lw} />
        </g>
      );
    case 'beret':
      return (
        <g>
          <path d={`M-74 ${top + 6} Q-90 ${top - 30} -10 ${top - 34} Q80 ${top - 36} 70 ${top + 2} Q0 ${top + 18} -74 ${top + 6} Z`} fill={color} stroke={INK} strokeWidth={Lw} />
          {emblem(34, top - 4, 0.8)}
        </g>
      );
    case 'kepi':
      return (
        <g>
          <path d={`M-50 ${top + 14} L-46 ${top - 34} Q0 ${top - 42} 46 ${top - 34} L50 ${top + 14} Z`} fill={color} stroke={INK} strokeWidth={Lw} />
          <path d={`M-50 ${top + 2} h100 v12 h-100 z`} fill={dark} stroke={INK} strokeWidth={3} />
          <path d={`M-48 ${top + 14} Q0 ${top + 40} 48 ${top + 14} Z`} fill="#1b1b1b" stroke={INK} strokeWidth={3} />
          <path d={`M-30 ${top - 20} h60`} stroke="#e3b94a" strokeWidth={3} />
        </g>
      );
    case 'bicorne':
      return (
        <g>
          <path d={`M-118 ${top + 18} Q-40 ${top - 58} 0 ${top - 50} Q40 ${top - 58} 118 ${top + 18} Q0 ${top - 6} -118 ${top + 18} Z`} fill="#1b1b1b" stroke={INK} strokeWidth={Lw} />
          <circle cx={30} cy={top - 18} r={10} fill="#0055a4" stroke="#fff" strokeWidth={3} />
        </g>
      );
    case 'ushanka':
      return (
        <g>
          <path d={`M-80 ${top + 50} L-80 ${top + 6} C-80 ${top - 46} 80 ${top - 46} 80 ${top + 6} L80 ${top + 50} L64 ${top + 50} L64 ${top + 14} L-64 ${top + 14} L-64 ${top + 50} Z`} fill="#6b5a46" stroke={INK} strokeWidth={Lw} />
          <path d={`M-72 ${top + 16} Q0 ${top - 4} 72 ${top + 16} L72 ${top - 6} Q0 ${top - 26} -72 ${top - 6} Z`} fill="#8a7860" stroke={INK} strokeWidth={3} />
          {emblem(0, top + 4, 0.9)}
        </g>
      );
    case 'fedora':
      return (
        <g>
          <path d={`M-100 ${top + 18} Q0 ${top + 38} 100 ${top + 18} Q0 ${top + 4} -100 ${top + 18} Z`} fill={color} stroke={INK} strokeWidth={Lw} />
          <path d={`M-56 ${top + 16} L-50 ${top - 30} Q0 ${top - 18} 50 ${top - 30} L56 ${top + 16} Z`} fill={color} stroke={INK} strokeWidth={Lw} />
          <path d={`M-56 ${top + 4} h112 v12 h-112 z`} fill="#1b1b1b" />
        </g>
      );
    case 'tophat':
      return (
        <g>
          <path d={`M-90 ${top + 14} Q0 ${top + 32} 90 ${top + 14} Q0 ${top} -90 ${top + 14} Z`} fill="#1b1b1b" stroke={INK} strokeWidth={Lw} />
          <rect x={-54} y={top - 76} width={108} height={92} rx={6} fill="#1b1b1b" stroke={INK} strokeWidth={Lw} />
          <rect x={-54} y={top - 4} width={108} height={12} fill="#5a1d1d" />
        </g>
      );
    case 'pith':
      return (
        <g>
          <path d={`M-102 ${top + 24} Q0 ${top + 46} 102 ${top + 24} Q0 ${top + 12} -102 ${top + 24} Z`} fill="#e6d9b0" stroke={INK} strokeWidth={Lw} />
          <path d={`M-66 ${top + 22} C-66 ${top - 54} 66 ${top - 54} 66 ${top + 22} Z`} fill="#e6d9b0" stroke={INK} strokeWidth={Lw} />
        </g>
      );
    case 'sailor':
      return (
        <g>
          <path d={`M-66 ${top + 12} Q-70 ${top - 28} 0 ${top - 30} Q70 ${top - 28} 66 ${top + 12} Q0 ${top + 22} -66 ${top + 12} Z`} fill="#f6f4ee" stroke={INK} strokeWidth={Lw} />
          <path d={`M-62 ${top + 10} Q0 ${top + 20} 62 ${top + 10}`} stroke="#2c3f6b" strokeWidth={4} fill="none" />
        </g>
      );
    case 'pilot':
      return (
        <g>
          <path d={`M-74 ${top + 60} L-74 ${top + 6} C-74 ${top - 46} 74 ${top - 46} 74 ${top + 6} L74 ${top + 60} Q60 ${top + 66} 58 ${top + 50} L58 ${top + 20} L-58 ${top + 20} L-58 ${top + 50} Q-60 ${top + 66} -74 ${top + 60} Z`} fill="#7a4a2a" stroke={INK} strokeWidth={Lw} />
          {back ? null : (
            <g>
              <path d={`M-70 ${top + 4} Q0 ${top - 14} 70 ${top + 4}`} stroke="#3a2a1a" strokeWidth={8} fill="none" />
              <circle cx={-24} cy={top - 4} r={15} fill="#a9d3ea" stroke={INK} strokeWidth={4} />
              <circle cx={24} cy={top - 4} r={15} fill="#a9d3ea" stroke={INK} strokeWidth={4} />
            </g>
          )}
          {back ? <path d={`M-70 ${top + 4} Q0 ${top - 14} 70 ${top + 4}`} stroke="#3a2a1a" strokeWidth={8} fill="none" /> : null}
        </g>
      );
    case 'roman':
      return (
        <g>
          <path d={`M-72 ${top + 40} L-72 ${top + 4} C-72 ${top - 48} 72 ${top - 48} 72 ${top + 4} L72 ${top + 40} L58 ${top + 40} L58 ${top + 14} L-58 ${top + 14} L-58 ${top + 40} Z`} fill="#c9a24a" stroke={INK} strokeWidth={Lw} />
          <path d={`M-10 ${top - 40} Q0 ${top - 90} 60 ${top - 70} Q40 ${top - 50} 10 ${top - 40} Z`} fill="#c8352b" stroke={INK} strokeWidth={3} />
        </g>
      );
    case 'crown':
      return <path d={`M-56 ${top + 8} L-60 ${top - 36} L-30 ${top - 14} L0 ${top - 44} L30 ${top - 14} L60 ${top - 36} L56 ${top + 8} Z`} fill="#e3b94a" stroke={INK} strokeWidth={Lw} strokeLinejoin="round" />;
    case 'conical':
      return <path d={`M-110 ${top + 24} L0 ${top - 50} L110 ${top + 24} Q0 ${top + 34} -110 ${top + 24} Z`} fill="#d8c48a" stroke={INK} strokeWidth={Lw} strokeLinejoin="round" />;
    case 'pith_vn':
      return (
        <g>
          <path d={`M-98 ${top + 22} Q0 ${top + 42} 98 ${top + 22} Q0 ${top + 10} -98 ${top + 22} Z`} fill="#7d8a4a" stroke={INK} strokeWidth={Lw} />
          <path d={`M-64 ${top + 20} C-64 ${top - 50} 64 ${top - 50} 64 ${top + 20} Z`} fill="#7d8a4a" stroke={INK} strokeWidth={Lw} />
          {emblem(0, top - 6, 1)}
        </g>
      );
    default:
      return null;
  }
};
