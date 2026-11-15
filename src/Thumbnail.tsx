import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import type { CastMember, ElementBase, Scene } from './types';
import { SceneView, TINTS } from './scene/SceneView';
import { ElementView, type Ctx } from './scene/Elements';
import { C, FONT, INK, col } from './theme';

/**
 * YouTube thumbnail (1280x720 output, 1920x1080 design space) built like the reference channel's:
 *  - panels: 1 (hero / versus), 2 (before→after split, vertical or diagonal) or 3 (triptych) scenes;
 *  - overlay: elements in full-frame coordinates on top of every panel (giant busts that cross the split,
 *    arrows, red rings, labels, name plates, big sweat drops, pointing hands, torn-paper bands);
 *  - texts: 2–4 huge words, white + one accent colour, heavy black outline + drop shadow; auto-fit to maxWidth;
 *  - grade: punchy saturation/contrast like the reference AI-painted thumbnails.
 */
export type ThumbText = {
  text: string; x?: number; y?: number; size?: number; color?: string; accent?: string; accentColor?: string; rotate?: number;
  anchor?: 'start' | 'middle' | 'end'; box?: string; plate?: string; font?: string; maxWidth?: number; outline?: number; shadow?: boolean;
};
export type ThumbSpec = {
  panels: (Scene & { at?: number })[];
  split?: 'vertical' | 'diagonal';
  overlay?: ElementBase[];
  texts?: ThumbText[];
  divider?: string;
  grade?: 'punch' | 'soft' | 'none';
  at?: number;
  /** AI-generated art (data URL or path resolved by render.mjs): replaces the panels; texts/overlay go on top */
  image?: string;
  /** elements to draw on top of the AI image (normally none: the art already has them) */
  imageOverlay?: ElementBase[];
};
export type ThumbProps = { thumb: ThumbSpec; cast?: Record<string, CastMember> };

const CHAR_W: Record<string, number> = { heavy: 0.44, round: 0.6, comic: 0.47, hand: 0.48 };

const BigText: React.FC<{ tt: ThumbText }> = ({ tt }) => {
  const size = tt.size ?? 190;
  const words = tt.text.split(' ');
  const fill = col(tt.color, '#fff');
  const acc = col(tt.accentColor, C.yellow);
  const accSet = new Set((tt.accent ?? '').toUpperCase().split(' ').filter(Boolean).map((w) => w.replace(/[^\p{L}\p{N}]/gu, '')));
  const fk = tt.font === 'round' ? 'round' : tt.font === 'comic' ? 'comic' : tt.font === 'hand' ? 'hand' : 'heavy';
  const font = fk === 'round' ? FONT.round : fk === 'comic' ? FONT.comic : fk === 'hand' ? FONT.hand : FONT.heavy;
  const weight = fk === 'round' ? 800 : 400;
  const anchor = tt.anchor ?? 'middle';
  const content = words.map((w, i) => (
    <tspan key={i} fill={accSet.has(w.toUpperCase().replace(/[^\p{L}\p{N}]/gu, '')) ? acc : fill}>{w + (i < words.length - 1 ? ' ' : '')}</tspan>
  ));
  const approxW = tt.text.length * size * CHAR_W[fk];
  const fitW = tt.maxWidth && approxW > tt.maxWidth ? tt.maxWidth : undefined;
  const w = fitW ?? approxW;
  const bx = anchor === 'middle' ? -w / 2 - 34 : anchor === 'end' ? -w - 34 : -34;
  const ow = size * (tt.outline ?? 0.19);
  const fitProps = fitW ? { textLength: fitW, lengthAdjust: 'spacingAndGlyphs' as const } : {};
  const capTop = -size * (fk === 'round' ? 0.78 : 0.86);
  return (
    <g transform={`translate(${tt.x ?? 960} ${tt.y ?? 900}) rotate(${tt.rotate ?? 0})`}>
      {tt.box ? <rect x={bx} y={capTop - 22} width={w + 68} height={-capTop + 50} fill={col(tt.box)} stroke={INK} strokeWidth={8} /> : null}
      {tt.plate ? (
        <g>
          <rect x={bx + 8} y={capTop - 18} width={w + 68} height={-capTop + 46} rx={18} fill="#000" opacity={0.35} />
          <rect x={bx} y={capTop - 26} width={w + 68} height={-capTop + 46} rx={18} fill={col(tt.plate)} stroke="#fff" strokeWidth={10} />
          <rect x={bx} y={capTop - 26} width={w + 68} height={-capTop + 46} rx={18} fill="none" stroke={INK} strokeWidth={4} />
        </g>
      ) : null}
      {tt.shadow === false ? null : (
        <text textAnchor={anchor} fontFamily={font} fontWeight={weight} fontSize={size} stroke="#000" strokeOpacity={0.45} strokeWidth={ow * 1.25} strokeLinejoin="round" paintOrder="stroke" fill="#000" fillOpacity={0.45} transform={`translate(${size * 0.05} ${size * 0.07})`} {...fitProps}>{tt.text}</text>
      )}
      <text textAnchor={anchor} fontFamily={font} fontWeight={weight} fontSize={size} stroke={tt.plate ? 'none' : INK} strokeWidth={ow} strokeLinejoin="round" paintOrder="stroke" {...fitProps}>{content}</text>
    </g>
  );
};

/** Black box with white condensed text — the reference channel's date tag on thumbnails. */
const DateTag: React.FC<{ text: string; x: number; y: number; size?: number }> = ({ text, x, y, size = 70 }) => {
  const w = text.length * size * 0.5 + 50;
  return (
    <g transform={`translate(${x} ${y})`}>
      <rect x={6} y={8} width={w} height={size * 1.3} fill="#000" opacity={0.35} />
      <rect x={0} y={0} width={w} height={size * 1.3} fill="#141414" stroke="#fff" strokeWidth={5} />
      <text x={w / 2} y={size * 1.0} textAnchor="middle" fontFamily={FONT.heavy} fontSize={size} fill="#fff" letterSpacing={1}>{text.toUpperCase()}</text>
    </g>
  );
};

const GRADES: Record<string, string> = {
  punch: 'saturate(1.38) contrast(1.12) brightness(1.03)',
  soft: 'saturate(1.15) contrast(1.04)',
  none: 'none',
};

export const Thumbnail: React.FC<ThumbProps> = ({ thumb, cast }) => {
  const n = thumb.image ? 0 : (thumb.panels ?? []).length;
  const w = 100 / n;
  const diag = n === 2 && thumb.split === 'diagonal';
  const grade = GRADES[thumb.grade ?? 'punch'];
  const clipFor = (i: number) => {
    if (diag) return i === 0 ? 'polygon(0 0, 58% 0, 42% 100%, 0 100%)' : 'polygon(58% 0, 100% 0, 100% 100%, 42% 100%)';
    return `inset(0 ${100 - (i + 1) * w}% 0 ${i * w}%)`;
  };
  const tOver = thumb.at ?? 2.5;
  const ctx: Ctx = { t: tOver, dur: 10, cast, sceneId: 'thumb' };
  return (
    <AbsoluteFill style={{ background: '#111' }}>
      {thumb.image ? <Img src={thumb.image} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover' }} /> : null}
      {(thumb.image ? [] : thumb.panels ?? []).map((p, i) => (
        <AbsoluteFill key={i} style={{ clipPath: clipFor(i), filter: p.tint ? `${TINTS[p.tint]} ${grade === 'none' ? '' : grade}` : grade }}>
          <div style={{ position: 'absolute', inset: 0, transform: n > 1 ? `translateX(${(i + 0.5) * w - 50}%)` : undefined }}>
            <SceneView scene={n > 1 ? { ...p, date: undefined, clock: undefined } : p} t={p.at ?? 2.5} cast={cast} />
          </div>
        </AbsoluteFill>
      ))}
      {thumb.image ? null : <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 58%, rgba(0,0,0,0.38) 100%)' }} />}
      <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{ position: 'absolute', inset: 0, filter: thumb.image ? undefined : grade }}>
        {diag ? (
          <g>
            <line x1={1920 * 0.58} y1={-10} x2={1920 * 0.42} y2={1090} stroke={INK} strokeWidth={26} />
            <line x1={1920 * 0.58} y1={-10} x2={1920 * 0.42} y2={1090} stroke={thumb.divider ?? '#fff'} strokeWidth={14} />
          </g>
        ) : n > 1 ? (
          Array.from({ length: n - 1 }, (_, i) => (
            <g key={i}>
              <rect x={((i + 1) * 1920) / n - 13} y={0} width={26} height={1080} fill={INK} />
              <rect x={((i + 1) * 1920) / n - 7} y={0} width={14} height={1080} fill={thumb.divider ?? '#fff'} />
            </g>
          ))
        ) : null}
        {(thumb.image ? thumb.imageOverlay ?? [] : thumb.overlay ?? []).map((el, i) => <ElementView key={'o' + i} el={{ in: -5, ...el }} ctx={ctx} index={i} />)}
        {n > 1 ? (thumb.panels ?? []).map((p, i) => (p.date ? <DateTag key={'d' + i} text={p.date} x={(i * 1920) / n + (diag && i === 1 ? 300 : 0) + 40} y={40} /> : null)) : null}
        {(thumb.texts ?? []).map((tt, i) => <BigText key={i} tt={tt} />)}
      </svg>
      {thumb.image ? null : (
        <AbsoluteFill style={{ mixBlendMode: 'multiply', opacity: 0.1 }}>
          <Img src={staticFile('textures/grain.png')} style={{ width: '100%', height: '100%' }} />
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
