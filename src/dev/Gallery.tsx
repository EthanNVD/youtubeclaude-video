import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { Character } from '../char/Character';
import { PRESETS } from '../char/presets';

/** Dev contact sheet of presets / poses / expressions. props: {names?: string[], pose?, expr?} */
export const Gallery: React.FC<{ names?: string[]; poses?: string[]; exprs?: string[] }> = ({ names, poses, exprs }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const list = names ?? Object.keys(PRESETS).slice(0, 18);
  const cols = 6;
  return (
    <AbsoluteFill style={{ background: '#e9dfc7' }}>
      <svg viewBox="0 0 1920 1080" width={1920} height={1080}>
        {list.map((n, i) => {
          const x = 160 + (i % cols) * 320;
          const y = 470 + Math.floor(i / cols) * 520;
          return (
            <g key={n + i} transform={`translate(${x} ${y}) scale(1.15)`}>
              <Character spec={PRESETS[n] ?? {}} state={{ pose: poses?.[i % poses.length], expr: exprs?.[i % exprs.length] }} t={t} seed={n} />
              <text y={40} textAnchor="middle" fontSize={22} fontFamily="sans-serif">{n}</text>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
