// Render helper around @remotion/renderer.
//   node tools/render.mjs stills <plan.json> <outDir> [--at scene|mid|all] [--scenes s1,s2] [--scale 0.5]
//   node tools/render.mjs video  <plan.json> <out.mp4> [--from 0 --to 60] [--concurrency 6]
//   node tools/render.mjs thumb  <thumbs.json> <outDir>     (thumbs.json = {cast, thumbs:[ThumbSpec...]}; thumb.image = AI art to put the headline on)
//   node tools/render.mjs refs   <refs.json> <out.png>      (character reference sheet: {names, cast})
import { bundle } from '@remotion/bundler';
import { renderStill, renderMedia, selectComposition } from '@remotion/renderer';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { existsSync, rmSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import os from 'node:os';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
// keep Remotion's temp files (bundle, frames) on the project drive and clean them up afterwards
const cacheDir = path.join(root, '.cache', 'tmp');
await mkdir(cacheDir, { recursive: true });
process.env.TEMP = cacheDir;
process.env.TMP = cacheDir;
process.env.TMPDIR = cacheDir;
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
const bundleDir = path.join(root, '.cache', 'bundle-' + process.pid);
const serveUrl = await bundle({ entryPoint: path.join(root, 'src/index.ts'), publicDir: path.join(root, 'public'), outDir: bundleDir, onProgress: () => {} });
process.on('exit', () => {
  try { rmSync(bundleDir, { recursive: true, force: true }); } catch {}
});
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
    const thumb = { ...json.thumbs[i] };
    if (thumb.image && !String(thumb.image).startsWith('data:')) {
      // AI-generated art from the user: embed it so the headline can be composited on top
      const imgPath = path.isAbsolute(thumb.image) ? thumb.image : path.join(opt('base', path.dirname(input)), thumb.image);
      if (!existsSync(imgPath)) {
        log(`thumb ${i + 1}: image ${imgPath} not found — drawing the engine draft instead`);
        delete thumb.image;
      } else {
        const ext = path.extname(imgPath).slice(1).toLowerCase().replace('jpg', 'jpeg');
        thumb.image = `data:image/${ext};base64,` + (await readFile(imgPath)).toString('base64');
      }
    }
    const inputProps = { thumb, cast: json.cast };
    const comp = await selectComposition({ serveUrl, id: 'Thumb', inputProps, ...browserOpts });
    await renderStill({ composition: comp, serveUrl, inputProps, output: file, imageFormat: 'png', ...browserOpts });
    log(file);
  }
} else if (op === 'refs') {
  // character reference sheet for image models: each character in 3 expressions
  const names = json.names.flatMap((n) => [n, n, n]);
  const inputProps = { names, cast: json.cast, exprs: ['neutral', 'smug', 'panic'], poses: ['idle', 'cross', 'head'], scale: 1.05, cols: 6, labels: true };
  const comp = await selectComposition({ serveUrl, id: 'Gallery', inputProps, ...browserOpts });
  await renderStill({ composition: comp, serveUrl, inputProps, output: out, imageFormat: 'png', ...browserOpts });
  log(out);
} else {
  console.error('unknown op', op);
  process.exit(1);
}
if (!existsSync(out)) process.exit(1);
