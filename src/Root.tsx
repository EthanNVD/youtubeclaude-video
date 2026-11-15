import React from 'react';
import { Composition, Still } from 'remotion';
import { Gallery } from './dev/Gallery';
import { Video, type VideoProps } from './Video';
import { Thumbnail, type ThumbProps } from './Thumbnail';
import type { Plan } from './types';

const emptyPlan: Plan = {
  meta: { title: 'empty', duration: 4 },
  scenes: [{ id: 's1', start: 0, end: 4, type: 'title', title: 'Load a plan with --props' }],
};

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="Video"
      component={Video}
      width={1920}
      height={1080}
      fps={24}
      durationInFrames={96}
      defaultProps={{ plan: emptyPlan }}
      calculateMetadata={({ props }) => {
        const fps = props.plan.meta.fps ?? 24;
        const end = Math.max(props.plan.meta.duration, ...props.plan.scenes.map((s) => s.end));
        return { fps, durationInFrames: Math.max(1, Math.round(end * fps)), width: props.plan.meta.width ?? 1920, height: props.plan.meta.height ?? 1080 };
      }}
    />
    <Still id="Thumb" component={Thumbnail} width={1280} height={720} defaultProps={{ thumb: { panels: emptyPlan.scenes } }} />
    <Composition id="Gallery" component={Gallery} width={1920} height={1080} fps={24} durationInFrames={48} defaultProps={{}} />
  </>
);
