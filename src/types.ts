// Plan schema: the JSON Claude writes from the SRT. See .claude/skills/srt-history-video/references/plan-schema.md

export type Num = number;
export type LonLat = [number, number];

/** A keyframe: any element prop may appear; numbers are eased between keys, other values switch at `t`. */
export type Key = { t: number; ease?: Ease } & Record<string, unknown>;
export type Ease = 'linear' | 'in' | 'out' | 'inOut' | 'back' | 'step' | 'drive';

export type Enter = 'none' | 'pop' | 'fade' | 'drop' | 'rise' | 'slideL' | 'slideR' | 'grow' | 'stamp' | 'draw';

export type ElementBase = {
  kind: string;
  id?: string;
  /** stage px (1920x1080 frame at camera zoom 1, origin top-left) */
  x?: number;
  y?: number;
  /** map coordinate instead of x/y (map scenes only) */
  at?: LonLat;
  scale?: number;
  rotate?: number;
  flip?: boolean;
  opacity?: number;
  /** seconds relative to scene start */
  in?: number;
  out?: number;
  enter?: Enter;
  exit?: Enter;
  /** draw above camera (screen-fixed HUD) */
  hud?: boolean;
  keys?: Key[];
  [k: string]: unknown;
};

export type CameraKey = { t: number; x?: number; y?: number; zoom?: number; rotate?: number; center?: LonLat; ease?: Ease; shake?: number };

export type MapSpec = {
  /** historical basemap year: bc323 bc200 bc1 100 400 800 1100 1200 1279 1400 1492 1600 1700 1715 1783 1800 1815 1880 1914 1920 1938 1945 1960 1994 2010 */
  era?: string;
  center: LonLat;
  /** degrees of longitude visible across the frame at zoom 1 */
  span: number;
  /** country/polity name (as in basemap) -> color or nation key */
  colors?: Record<string, string>;
  /** names to label automatically at their centroid */
  labels?: string[] | boolean;
  land?: string;
  ocean?: string;
  /** snow | paper | dark | sepia */
  style?: string;
  grid?: boolean;
};

export type Scene = {
  id: string;
  start: number;
  end: number;
  /** what the narration says here (for review only) */
  beat?: string;
  type: 'stage' | 'map' | 'title' | 'chapter';
  set?: SetSpec;
  map?: MapSpec;
  camera?: CameraKey[];
  elements?: ElementBase[];
  date?: string;
  clock?: string;
  /** cinema bars (true, or the caption for the bottom bar, e.g. "DRAMATISED — ARNHEM, 19 SEPT 1944") */
  letterbox?: boolean | string;
  /** depth model: actors/vehicles without a scale are sized by their ground y (see src/lib/depth.ts) */
  world?: { horizon?: number; y?: number; scale?: number; vehicles?: number };
  place?: string;
  transition?: 'cut' | 'fade' | 'dip' | 'wipe' | 'flash';
  /** tints: sepia (counterfactual/past), night, cold, warm, grey (grief) */
  tint?: string;
  sfx?: SfxCue[];
  ambience?: string | null;
  title?: string;
  subtitle?: string;
};

export type SetSpec = { kind: string; time?: 'day' | 'dusk' | 'night' | 'dawn'; weather?: string; [k: string]: unknown };
export type SfxCue = { t: number; id: string; vol?: number; dur?: number };

export type CastMember = { preset?: string; name?: string; [k: string]: unknown };

export type Plan = {
  meta: {
    title: string;
    lang?: string;
    fps?: number;
    width?: number;
    height?: number;
    duration: number;
    voice?: string;
    /** 0..1 film grain/paper texture */
    grain?: number;
    grade?: string;
  };
  cast?: Record<string, CastMember>;
  scenes: Scene[];
};
