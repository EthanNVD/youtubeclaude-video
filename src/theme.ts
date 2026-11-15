import { loadFont as loadHand } from '@remotion/google-fonts/PatrickHand';
import { loadFont as loadAnton } from '@remotion/google-fonts/Anton';
import { loadFont as loadOswald } from '@remotion/google-fonts/Oswald';
import { loadFont as loadMono } from '@remotion/google-fonts/IBMPlexMono';
import { loadFont as loadSerif } from '@remotion/google-fonts/PlayfairDisplay';
import { loadFont as loadBangers } from '@remotion/google-fonts/Bangers';
import { loadFont as loadBaloo } from '@remotion/google-fonts/Baloo2';

const subsets: ('latin' | 'latin-ext' | 'vietnamese')[] = ['latin', 'latin-ext', 'vietnamese'];
export const FONT = {
  hand: loadHand('normal', { weights: ['400'], subsets }).fontFamily,
  heavy: loadAnton('normal', { weights: ['400'], subsets }).fontFamily,
  cond: loadOswald('normal', { weights: ['400', '600', '700'], subsets }).fontFamily,
  mono: loadMono('normal', { weights: ['400', '600'], subsets }).fontFamily,
  serif: loadSerif('normal', { weights: ['700', '900'], subsets }).fontFamily,
  comic: loadBangers('normal', { weights: ['400'], subsets }).fontFamily,
  round: loadBaloo('normal', { weights: ['800'], subsets }).fontFamily,
};

export const INK = '#2a2622';
export const LINE = 4;
export const SKIN = '#f6dcc4';
export const PAPER = '#f4ecd8';

export const C = {
  red: '#c8352b',
  redDark: '#8f1f19',
  yellow: '#f2c230',
  blue: '#3a6ea5',
  navy: '#22324d',
  green: '#4f7a3a',
  grey: '#8b8f93',
  white: '#fbf8f0',
  black: '#1d1b19',
  sea: '#5b8fb0',
  seaDeep: '#3d6d8f',
  sky: '#a9d3ea',
  skyTop: '#6fb3dc',
  grass: '#9cb85a',
  dirt: '#b9925f',
  wood: '#8a5a33',
  woodLight: '#b27a47',
  wall: '#d9c7a1',
  snow: '#eef2f5',
};

/** Nation palette: map fill, uniform, flag colors, marking. */
export type Nation = {
  name: string;
  map: string;
  /** strong color for bars / counters / icons (map color can be pale) */
  ui?: string;
  uniform: string;
  uniformDark: string;
  navy: string;
  flag: string[]; // stripes or special
  flagKind: 'h3' | 'v3' | 'sun' | 'star' | 'uk' | 'us' | 'plain' | 'cross' | 'h2';
  mark: 'cross' | 'star' | 'whitestar' | 'roundel' | 'sun' | 'none';
};

export const NATIONS: Record<string, Nation> = {
  GER: { name: 'Germany', map: '#7f8890', ui: '#55606a', uniform: '#6b7059', uniformDark: '#4c5040', navy: '#2b3440', flag: ['#1b1b1b', '#d42a20', '#f2c230'], flagKind: 'h3', mark: 'cross' },
  GERI: { name: 'German Empire', map: '#7f8890', uniform: '#77796a', uniformDark: '#55574a', navy: '#2b3440', flag: ['#1b1b1b', '#ffffff', '#d42a20'], flagKind: 'h3', mark: 'cross' },
  USSR: { name: 'Soviet Union', map: '#c8352b', uniform: '#7d7a4b', uniformDark: '#5a5735', navy: '#1f2a44', flag: ['#c8352b'], flagKind: 'star', mark: 'star' },
  RUS: { name: 'Russia', map: '#4f7a3a', uniform: '#5f6a45', uniformDark: '#434b30', navy: '#1f2a44', flag: ['#ffffff', '#2f56a6', '#d52b1e'], flagKind: 'h3', mark: 'none' },
  USA: { name: 'United States', map: '#3a6ea5', uniform: '#6e6a45', uniformDark: '#4f4c30', navy: '#1f2f4a', flag: ['#b22234', '#ffffff', '#3c3b6e'], flagKind: 'us', mark: 'whitestar' },
  UK: { name: 'United Kingdom', map: '#d98c8c', ui: '#b5463f', uniform: '#8a7a52', uniformDark: '#665a3a', navy: '#1b2740', flag: ['#012169', '#ffffff', '#c8102e'], flagKind: 'uk', mark: 'roundel' },
  JPN: { name: 'Japan', map: '#e7a596', ui: '#cf3a2e', uniform: '#8d8152', uniformDark: '#6a603a', navy: '#22263a', flag: ['#ffffff', '#bc002d'], flagKind: 'sun', mark: 'sun' },
  FRA: { name: 'France', map: '#5b7fbf', uniform: '#7b7350', uniformDark: '#5b5438', navy: '#1e2b4a', flag: ['#0055a4', '#ffffff', '#ef4135'], flagKind: 'v3', mark: 'roundel' },
  ITA: { name: 'Italy', map: '#7aa36a', uniform: '#7a7a5c', uniformDark: '#5a5a42', navy: '#23304a', flag: ['#009246', '#ffffff', '#ce2b37'], flagKind: 'v3', mark: 'none' },
  POL: { name: 'Poland', map: '#e8a0a8', uniform: '#73714f', uniformDark: '#555338', navy: '#1e2a44', flag: ['#ffffff', '#dc143c'], flagKind: 'h2', mark: 'none' },
  CHN: { name: 'China', map: '#e6b85c', uniform: '#5d6b7a', uniformDark: '#434e5a', navy: '#1f2a44', flag: ['#fe0000', '#000095'], flagKind: 'plain', mark: 'none' },
  FIN: { name: 'Finland', map: '#9fc3e6', uniform: '#77786a', uniformDark: '#55564a', navy: '#1f2a44', flag: ['#ffffff', '#003580'], flagKind: 'cross', mark: 'none' },
  ROM: { name: 'Romania', map: '#d9c35b', uniform: '#7b7650', uniformDark: '#5b5638', navy: '#1f2a44', flag: ['#002b7f', '#fcd116', '#ce1126'], flagKind: 'v3', mark: 'none' },
  HUN: { name: 'Hungary', map: '#9bbf8a', uniform: '#7a7550', uniformDark: '#5a5538', navy: '#1f2a44', flag: ['#ce2939', '#ffffff', '#477050'], flagKind: 'h3', mark: 'none' },
  NED: { name: 'Netherlands', map: '#f0a050', uniform: '#6f735a', uniformDark: '#505340', navy: '#1f2a44', flag: ['#ae1c28', '#ffffff', '#21468b'], flagKind: 'h3', mark: 'none' },
  BEL: { name: 'Belgium', map: '#e0cf6a', uniform: '#7a7552', uniformDark: '#5a5538', navy: '#1f2a44', flag: ['#000000', '#fdda24', '#ef3340'], flagKind: 'v3', mark: 'none' },
  AUS: { name: 'Austria-Hungary', map: '#e3c46a', uniform: '#7d93a8', uniformDark: '#5d7184', navy: '#1f2a44', flag: ['#ed2939', '#ffffff', '#ed2939'], flagKind: 'h3', mark: 'none' },
  OTT: { name: 'Ottoman Empire', map: '#5f9e7c', uniform: '#8a7d55', uniformDark: '#665c3c', navy: '#1f2a44', flag: ['#e30a17'], flagKind: 'plain', mark: 'none' },
  VN: { name: 'Vietnam', map: '#d64a3a', uniform: '#6d7a4a', uniformDark: '#4d5732', navy: '#1f2a44', flag: ['#da251d'], flagKind: 'star', mark: 'star' },
  SPQR: { name: 'Rome', map: '#9a3b3b', uniform: '#a8322c', uniformDark: '#7a221e', navy: '#2a2a2a', flag: ['#9a3b3b'], flagKind: 'plain', mark: 'none' },
  CARTH: { name: 'Carthage', map: '#7a5aa0', uniform: '#5f4b80', uniformDark: '#463860', navy: '#2a2a2a', flag: ['#7a5aa0'], flagKind: 'plain', mark: 'none' },
  NEUTRAL: { name: 'Neutral', map: '#d8ccb0', uniform: '#6f6f6f', uniformDark: '#505050', navy: '#2a2a2a', flag: ['#cccccc'], flagKind: 'plain', mark: 'none' },
};

export const nation = (k?: string): Nation => NATIONS[(k ?? 'NEUTRAL').toUpperCase()] ?? NATIONS.NEUTRAL;
export const uiColor = (k?: string) => { const n = nation(k); return n.ui ?? n.map; };

/** color: nation key (e.g. "GER") or literal css color */
export const col = (c: unknown, fallback = INK): string => {
  if (typeof c !== 'string' || !c) return fallback;
  const n = NATIONS[c.toUpperCase()];
  if (n) return n.map;
  return (C as Record<string, string>)[c] ?? c;
};
