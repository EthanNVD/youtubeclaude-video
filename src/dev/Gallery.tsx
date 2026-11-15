import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { Character } from '../char/Character';
import { PRESETS, resolveCast } from '../char/presets';

/** Dev contact sheet of presets / poses / expressions. props: {names?: string[], pose?, expr?} */
export const Gallery: React.FC<{ names?: string[]; poses?: string[]; exprs?: string[]; walk?: boolean[]; talk?: boolean; scale?: number; cols?: number; dt?: number; run?: boolean; cast?: Record<string, { preset?: string } & Record<string, unknown>> }> = ({ names, poses, exprs, walk, talk, scale = 1.15, cols: colsP, dt = 0, run, cast }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const list = names ?? Object.keys(PRESETS).slice(0, 18);
  const cols = colsP ?? 6;
  return (
    <AbsoluteFill style={{ background: '#e9dfc7' }}>
      <svg viewBox="0 0 1920 1080" width={1920} height={1080}>
        {list.map((n, i) => {
          const cw = 1920 / cols;
          const x = cw / 2 + (i % cols) * cw;
          const y = 120 + 330 * scale + Math.floor(i / cols) * (340 * scale + 60);
          return (
            <g key={n + i} transform={`translate(${x} ${y}) scale(${scale})`}>
              <Character spec={cast ? resolveCast(cast, n) : PRESETS[n] ?? {}} state={{ pose: poses?.[i % poses.length], expr: exprs?.[i % exprs.length], walk: walk?.[i % walk.length] ? 1 : 0, run, talk }} t={t + i * dt} seed={dt ? 'same' : n} />
              <text y={40} textAnchor="middle" fontSize={22} fontFamily="sans-serif">{n}</text>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
