import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import type { Plan, Scene } from './types';
import { SceneView, TINTS } from './scene/SceneView';
import { clamp, easeFn } from './lib/anim';

export type VideoProps = { plan: Plan };

const TD = 0.5; // transition duration (s)

const findScene = (scenes: Scene[], T: number) => {
  let lo = 0, hi = scenes.length - 1, ans = 0;
  while (lo <= hi) {
    const m = (lo + hi) >> 1;
    if (scenes[m].start <= T) {
      ans = m;
      lo = m + 1;
    } else hi = m - 1;
  }
  return ans;
};

const Layer: React.FC<{ scene: Scene; t: number; plan: Plan; style?: React.CSSProperties }> = ({ scene, t, plan, style }) => (
  <AbsoluteFill style={{ filter: scene.tint ? TINTS[scene.tint] : undefined, ...style }}>
    <SceneView scene={scene} t={t} cast={plan.cast} />
  </AbsoluteFill>
);

export const Video: React.FC<VideoProps> = ({ plan }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const T = frame / fps;
  const scenes = plan.scenes;
  if (!scenes.length) return <AbsoluteFill style={{ background: '#222' }} />;
  const i = findScene(scenes, T);
  const sc = scenes[i];
  const t = T - sc.start;
  const prev = i > 0 ? scenes[i - 1] : null;
  const tr = sc.transition ?? 'cut';
  const inTr = prev && tr !== 'cut' && t < TD;
  const k = clamp(t / TD);
  const grain = plan.meta.grain ?? 0.5;

  let content: React.ReactNode;
  if (inTr && prev && (tr === 'fade' || tr === 'wipe')) {
    content = (
      <>
        <Layer scene={prev} t={T - prev.start} plan={plan} />
        <Layer scene={sc} t={t} plan={plan} style={tr === 'fade' ? { opacity: easeFn('inOut', k) } : { clipPath: `inset(0 ${(1 - easeFn('inOut', k)) * 100}% 0 0)` }} />
      </>
    );
  } else if (inTr && prev && tr === 'dip') {
    content = (
      <>
        {k < 0.5 ? <Layer scene={prev} t={T - prev.start} plan={plan} /> : <Layer scene={sc} t={t} plan={plan} />}
        <AbsoluteFill style={{ background: '#000', opacity: 1 - Math.abs(k - 0.5) * 2 }} />
      </>
    );
  } else {
    content = <Layer scene={sc} t={t} plan={plan} />;
  }

  return (
    <AbsoluteFill style={{ background: '#111' }}>
      {content}
      {tr === 'flash' && t < 0.25 ? <AbsoluteFill style={{ background: '#fff', opacity: 1 - t / 0.25 }} /> : null}
      {grain > 0 ? (
        <AbsoluteFill style={{ mixBlendMode: 'multiply', opacity: grain * 0.55, pointerEvents: 'none' }}>
          <Img src={staticFile('textures/grain.png')} style={{ width: '120%', height: '120%', transform: `translate(${-((frame * 37) % 100) / 10}%, ${-((frame * 53) % 100) / 10}%)` }} />
        </AbsoluteFill>
      ) : null}
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 62%, rgba(0,0,0,0.28) 100%)', pointerEvents: 'none' }} />
    </AbsoluteFill>
  );
};
