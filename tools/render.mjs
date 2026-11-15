// Render helper around @remotion/renderer.
//   node tools/render.mjs stills <plan.json> <outDir> [--at scene|mid|all] [--scenes s1,s2] [--scale 0.5]
//   node tools/render.mjs video  <plan.json> <out.mp4> [--from 0 --to 60] [--concurrency 6]
//   node tools/render.mjs thumb  <thumbs.json> <outDir>     (thumbs.json = {cast, thumbs:[ThumbSpec...]})
import { bundle } from '@remotion/bundler';
import { renderStill, renderMedia, selectComposition } from '@remotion/renderer';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import os from 'node:os';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const [op, input, out] = args;
const opt = (k, d) => {
  const i = args.indexOf('--' + k);
  return i >= 0 ? args[i + 1] : d;
};
if (!op || !input || !out) {
  console.error('usage: node tools/render.mjs stills|video|thumb <input.json> <out>');
  process.exit(1);
}

const log = (...a) => console.log('[render]', ...a);
const serveUrl = await bundle({ entryPoint: path.join(root, 'src/index.ts'), publicDir: path.join(root, 'public'), onProgress: () => {} });
log('bundled');
const json = JSON.parse(await readFile(input, 'utf8'));
const browserOpts = { chromiumOptions: { gl: 'angle' } };

if (op === 'stills') {
  const plan = json;
  const comp = await selectComposition({ serveUrl, id: 'Video', inputProps: { plan }, ...browserOpts });
  await mkdir(out, { recursive: true });
  const which = opt('scenes', '');
  const at = opt('at', 'mid');
  const scale = Number(opt('scale', '0.5'));
  const list = plan.scenes.filter((s) => !which || which.split(',').includes(s.id));
  const jobs = [];
  for (const s of list) {
    const ts = at === 'all' ? [s.start + 0.6, (s.start + s.end) / 2, s.end - 0.3] : at === 'end' ? [s.end - 0.3] : [s.start + Math.min(2.5, (s.end - s.start) * 0.6)];
    for (const T of ts) jobs.push({ s, T });
  }
  const conc = Number(opt('concurrency', String(Math.max(2, Math.min(6, os.cpus().length - 2)))));
  let idx = 0;
  const files = [];
  const worker = async () => {
    while (idx < jobs.length) {
      const { s, T } = jobs[idx++];
      const frame = Math.min(comp.durationInFrames - 1, Math.round(T * comp.fps));
      const file = path.join(out, `${s.id}_${String(frame).padStart(6, '0')}.jpg`);
      await renderStill({ composition: comp, serveUrl, inputProps: { plan }, frame, output: file, imageFormat: 'jpeg', jpegQuality: 85, scale, ...browserOpts });
      files.push({ file, scene: s.id, t: T, beat: s.beat ?? '' });
      log(path.basename(file));
    }
  };
  await Promise.all(Array.from({ length: conc }, worker));
  files.sort((a, b) => a.t - b.t);
  await writeFile(path.join(out, 'index.json'), JSON.stringify(files, null, 1));
  log('stills done', files.length);
} else if (op === 'video') {
  const plan = json;
  const comp = await selectComposition({ serveUrl, id: 'Video', inputProps: { plan }, ...browserOpts });
  const from = opt('from', null), to = opt('to', null);
  const frameRange = from !== null ? [Math.round(Number(from) * comp.fps), Math.min(comp.durationInFrames - 1, Math.round(Number(to ?? from + 10) * comp.fps) - 1)] : null;
  let last = -1;
  await renderMedia({
    composition: comp,
    serveUrl,
    codec: 'h264',
    outputLocation: out,
    inputProps: { plan },
    muted: true,
    crf: Number(opt('crf', '20')),
    x264Preset: opt('preset', 'medium'),
    pixelFormat: 'yuv420p',
    imageFormat: 'jpeg',
    jpegQuality: 90,
    concurrency: Number(opt('concurrency', String(Math.max(2, os.cpus().length - 2)))),
    frameRange,
    onProgress: ({ progress }) => {
      const p = Math.floor(progress * 100);
      if (p !== last && p % 2 === 0) {
        last = p;
        log(`video ${p}%`);
      }
    },
    ...browserOpts,
  });
  log('video done', out);
} else if (op === 'thumb') {
  await mkdir(out, { recursive: true });
  for (let i = 0; i < json.thumbs.length; i++) {
    const file = path.join(out, `thumb_${i + 1}.png`);
    const inputProps = { thumb: json.thumbs[i], cast: json.cast };
    const comp = await selectComposition({ serveUrl, id: 'Thumb', inputProps, ...browserOpts });
    await renderStill({ composition: comp, serveUrl, inputProps, output: file, imageFormat: 'png', ...browserOpts });
    log(file);
  }
} else {
  console.error('unknown op', op);
  process.exit(1);
}
if (!existsSync(out)) process.exit(1);
