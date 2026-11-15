import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import type { CastMember, Scene } from './types';
import { SceneView, TINTS } from './scene/SceneView';
import { C, FONT, INK, col } from './theme';
import { DateBadge } from './overlays/Overlays';

/**
 * YouTube thumbnail (1280x720 output, 1920x1080 design space).
 * panels: 1 (hero) or 2/3 side-by-side scenes (split before/after, triptych of numbers).
 * texts: huge outlined words (Anton) — 2-4 words, one accent color, never a copy of the title.
 */
export type ThumbText = { text: string; x?: number; y?: number; size?: number; color?: string; accent?: string; accentColor?: string; rotate?: number; anchor?: 'start' | 'middle' | 'end'; box?: string; font?: string };
export type ThumbSpec = { panels: (Scene & { at?: number })[]; texts?: ThumbText[]; divider?: string; vignette?: boolean };
export type ThumbProps = { thumb: ThumbSpec; cast?: Record<string, CastMember> };

const BigText: React.FC<{ tt: ThumbText }> = ({ tt }) => {
  const size = tt.size ?? 190;
  const words = tt.text.split(' ');
  const fill = col(tt.color, '#fff');
  const acc = col(tt.accentColor, C.yellow);
  const accSet = new Set((tt.accent ?? '').toUpperCase().split(' ').filter(Boolean));
  const font = tt.font === 'comic' ? FONT.comic : tt.font === 'hand' ? FONT.hand : FONT.heavy;
  const anchor = tt.anchor ?? 'middle';
  const content = words.map((w, i) => (
    <tspan key={i} fill={accSet.has(w.toUpperCase().replace(/[^\p{L}\p{N}]/gu, '')) ? acc : fill}>{w + (i < words.length - 1 ? ' ' : '')}</tspan>
  ));
  const approxW = tt.text.length * size * 0.5;
  const bx = anchor === 'middle' ? -approxW / 2 - 30 : anchor === 'end' ? -approxW - 30 : -30;
  return (
    <g transform={`translate(${tt.x ?? 960} ${tt.y ?? 900}) rotate(${tt.rotate ?? 0})`}>
      {tt.box ? <rect x={bx} y={-size * 0.95} width={approxW + 60} height={size * 1.15} fill={col(tt.box)} stroke={INK} strokeWidth={8} /> : null}
      <text textAnchor={anchor} fontFamily={font} fontSize={size} stroke="#000" strokeOpacity={0.35} strokeWidth={size / 4.2} strokeLinejoin="round" paintOrder="stroke" transform="translate(8 10)">{content}</text>
      <text textAnchor={anchor} fontFamily={font} fontSize={size} stroke={INK} strokeWidth={size / 5.5} strokeLinejoin="round" paintOrder="stroke" letterSpacing={1}>{content}</text>
    </g>
  );
};

export const Thumbnail: React.FC<ThumbProps> = ({ thumb, cast }) => {
  const n = thumb.panels.length;
  const w = 100 / n;
  return (
    <AbsoluteFill style={{ background: '#111' }}>
      {thumb.panels.map((p, i) => (
        <AbsoluteFill key={i} style={{ clipPath: `inset(0 ${100 - (i + 1) * w}% 0 ${i * w}%)`, filter: p.tint ? TINTS[p.tint] : 'saturate(1.25) contrast(1.06)' }}>
          <div style={{ position: 'absolute', inset: 0, transform: n > 1 ? `translateX(${(i + 0.5) * w - 50}%)` : undefined }}>
            <SceneView scene={n > 1 ? { ...p, date: undefined, clock: undefined } : p} t={p.at ?? 2.5} cast={cast} />
          </div>
        </AbsoluteFill>
      ))}
      {n > 1
        ? Array.from({ length: n - 1 }, (_, i) => (
            <div key={i} style={{ position: 'absolute', top: 0, bottom: 0, left: `calc(${(i + 1) * w}% - 6px)`, width: 12, background: thumb.divider ?? '#fff', boxShadow: '0 0 0 4px #2a2622' }} />
          ))
        : null}
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(0,0,0,0.35) 100%)' }} />
      <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{ position: 'absolute', inset: 0 }}>
        {n > 1 ? thumb.panels.map((p, i) => (p.date ? <g key={'d' + i} transform={`translate(${(i * 1920) / n} 0) scale(1.35)`}><DateBadge text={p.date} a={5} x={30} y={30} /></g> : null)) : null}
        {(thumb.texts ?? []).map((tt, i) => <BigText key={i} tt={tt} />)}
      </svg>
      <AbsoluteFill style={{ mixBlendMode: 'multiply', opacity: 0.15 }}>
        <Img src={staticFile('textures/grain.png')} style={{ width: '100%', height: '100%' }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
