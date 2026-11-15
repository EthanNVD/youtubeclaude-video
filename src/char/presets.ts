import type { CharSpec } from './Character';

/**
 * Reusable cast. Leaders are caricatures recognisable by hair / moustache / hat / glasses — no portraits.
 * Use in plan.cast: { "stalin": { "preset": "stalin" } } or override any field.
 */
export const PRESETS: Record<string, CharSpec> = {
  // ---- WW2 Germany ----
  hitler: { nation: 'GER', outfit: 'party', hair: 'side', facial: 'toothbrush', extra: ['armband', 'ironcross'], age: 0.45 },
  hitler_uniform: { nation: 'GER', outfit: 'tunic', color: '#6e6a58', hair: 'side', facial: 'toothbrush', extra: ['ironcross'], age: 0.5 },
  goering: { nation: 'GER', outfit: 'tunic', color: '#9aa3a8', hat: 'peaked', hatColor: '#9aa3a8', hair: 'short', build: 1.35, extra: ['medals', 'jowls'], age: 0.5 },
  himmler: { nation: 'GER', outfit: 'tunic', color: '#3a3a3a', hair: 'short', glasses: 'round', age: 0.4 },
  rommel: { nation: 'GER', outfit: 'tunic', hat: 'peaked', hair: 'short', extra: ['medals'], age: 0.5 },
  guderian: { nation: 'GER', outfit: 'tunic', hat: 'peaked', hair: 'short', extra: ['medals'], age: 0.55 },
  manstein: { nation: 'GER', outfit: 'tunic', hat: 'peaked', hair: 'short', age: 0.6, extra: ['medals'] },
  paulus: { nation: 'GER', outfit: 'coat', hat: 'peaked', hair: 'short', facial: 'stubble', age: 0.6 },
  halder: { nation: 'GER', outfit: 'tunic', hair: 'short', glasses: 'pince', age: 0.65, hairColor: '#c9c4bc' },
  goebbels: { nation: 'GER', outfit: 'suit', hair: 'back', build: 0.88, age: 0.4 },
  german_officer: { nation: 'GER', outfit: 'tunic', hat: 'peaked', hair: 'short', age: 0.45 },
  german_soldier: { nation: 'GER', outfit: 'tunic', hat: 'helmet_de', hair: 'short', age: 0.2 },
  german_tanker: { nation: 'GER', outfit: 'tunic', color: '#2d2d2d', hat: 'garrison', hatColor: '#2d2d2d', hair: 'short', age: 0.2 },
  german_pilot: { nation: 'GER', outfit: 'pilot', color: '#5a4a3a', hat: 'pilot', age: 0.25 },
  uboat_captain: { nation: 'GER', outfit: 'navy', hat: 'navy_white', facial: 'beard', hairColor: '#4a3a2a', age: 0.35 },
  // ---- USSR ----
  stalin: { nation: 'USSR', outfit: 'tunic', color: '#8c8a66', hair: 'back', hairColor: '#4a4038', facial: 'walrus', extra: ['star', 'thickbrows'], age: 0.65 },
  zhukov: { nation: 'USSR', outfit: 'tunic', hat: 'peaked', hair: 'short', build: 1.15, extra: ['medals', 'epaulettes'], age: 0.5 },
  molotov: { nation: 'USSR', outfit: 'suit', hair: 'part', facial: 'pencil', glasses: 'pince', age: 0.5 },
  beria: { nation: 'USSR', outfit: 'suit', hair: 'bald', glasses: 'pince', age: 0.5 },
  khrushchev: { nation: 'USSR', outfit: 'suit', hair: 'bald', build: 1.2, age: 0.6 },
  soviet_officer: { nation: 'USSR', outfit: 'tunic', hat: 'peaked', hair: 'short', age: 0.45 },
  soviet_soldier: { nation: 'USSR', outfit: 'tunic', hat: 'helmet_su', hair: 'short', age: 0.2 },
  soviet_winter: { nation: 'USSR', outfit: 'coat', color: '#eceee9', hat: 'ushanka', hair: 'short', age: 0.25 },
  // ---- UK ----
  churchill: { nation: 'UK', outfit: 'suit', color: '#2f3036', hair: 'bald', hairColor: '#c9b8a0', extra: ['cigar', 'bowtie', 'jowls'], build: 1.25, age: 0.7 },
  chamberlain: { nation: 'UK', outfit: 'suit', hair: 'part', hairColor: '#cfc8bd', facial: 'pencil', age: 0.8, build: 0.9 },
  halifax: { nation: 'UK', outfit: 'suit', hair: 'bald', age: 0.7, build: 0.95 },
  montgomery: { nation: 'UK', outfit: 'tunic', hat: 'beret', hatColor: '#1b1b1b', facial: 'pencil', build: 0.9, age: 0.6 },
  british_soldier: { nation: 'UK', outfit: 'tunic', hat: 'helmet_uk', hair: 'short', age: 0.2 },
  raf_pilot: { nation: 'UK', outfit: 'pilot', color: '#5e6f86', hat: 'pilot', facial: 'handlebar', age: 0.25 },
  // ---- USA ----
  roosevelt: { nation: 'USA', outfit: 'suit', color: '#55575c', hair: 'part', hairColor: '#b9b2a6', glasses: 'pince', extra: ['cigarette'], age: 0.65 },
  truman: { nation: 'USA', outfit: 'suit', hair: 'part', hairColor: '#b9b2a6', glasses: 'round', age: 0.65 },
  eisenhower: { nation: 'USA', outfit: 'tunic', hair: 'bald', extra: ['medals'], age: 0.55 },
  macarthur: { nation: 'USA', outfit: 'tunic', color: '#b7a77c', hat: 'peaked', glasses: 'sun', extra: ['pipe'], age: 0.65 },
  patton: { nation: 'USA', outfit: 'tunic', hat: 'helmet_us', extra: ['medals'], age: 0.6 },
  nimitz: { nation: 'USA', outfit: 'navy', hat: 'navy_white', hair: 'short', hairColor: '#e8e4dc', age: 0.65 },
  american_soldier: { nation: 'USA', outfit: 'tunic', hat: 'helmet_us', hair: 'short', age: 0.2 },
  american_sailor: { nation: 'USA', outfit: 'sailor', hat: 'sailor', age: 0.15 },
  american_pilot: { nation: 'USA', outfit: 'pilot', color: '#7a5a3a', hat: 'pilot', age: 0.25 },
  us_navy_officer: { nation: 'USA', outfit: 'navywhite', hat: 'navy_white', age: 0.45 },
  // ---- Japan ----
  hirohito: { nation: 'JPN', outfit: 'tunic', hat: 'peaked', glasses: 'round', facial: 'pencil', build: 0.9, age: 0.4 },
  tojo: { nation: 'JPN', outfit: 'tunic', hair: 'bald', glasses: 'round', facial: 'toothbrush', age: 0.6 },
  yamamoto: { nation: 'JPN', outfit: 'navywhite', hat: 'navy_white', hair: 'short', age: 0.6 },
  nagumo: { nation: 'JPN', outfit: 'navy', hat: 'navy', hair: 'short', facial: 'pencil', age: 0.6 },
  japanese_officer: { nation: 'JPN', outfit: 'tunic', hat: 'peaked', hair: 'short', age: 0.45 },
  japanese_soldier: { nation: 'JPN', outfit: 'tunic', hat: 'helmet_jp', hair: 'short', age: 0.2 },
  japanese_pilot: { nation: 'JPN', outfit: 'pilot', color: '#6a5a3a', hat: 'pilot', age: 0.2 },
  japanese_sailor: { nation: 'JPN', outfit: 'sailor', hat: 'sailor', age: 0.2 },
  // ---- France / Italy / others ----
  de_gaulle: { nation: 'FRA', outfit: 'tunic', hat: 'kepi', hatColor: '#3b4a6b', build: 0.9, facial: 'pencil', age: 0.5 },
  petain: { nation: 'FRA', outfit: 'tunic', hat: 'kepi', hatColor: '#3b4a6b', facial: 'walrus', hairColor: '#e8e4dc', age: 0.9, extra: ['medals'] },
  gamelin: { nation: 'FRA', outfit: 'tunic', hat: 'kepi', hatColor: '#3b4a6b', facial: 'walrus', hairColor: '#e8e4dc', age: 0.8 },
  french_soldier: { nation: 'FRA', outfit: 'coat', hat: 'helmet_uk', hatColor: '#6a6d55', age: 0.2 },
  mussolini: { nation: 'ITA', outfit: 'tunic', color: '#2a2a2a', hair: 'bald', build: 1.15, extra: ['jowls'], age: 0.55 },
  italian_soldier: { nation: 'ITA', outfit: 'tunic', hat: 'helmet_us', hair: 'short', age: 0.2 },
  mannerheim: { nation: 'FIN', outfit: 'tunic', hat: 'peaked', facial: 'pencil', age: 0.85, extra: ['medals'] },
  finnish_soldier: { nation: 'FIN', outfit: 'coat', color: '#f0f2ef', hat: 'ushanka', age: 0.2 },
  chiang: { nation: 'CHN', outfit: 'tunic', hair: 'bald', facial: 'pencil', age: 0.5 },
  polish_soldier: { nation: 'POL', outfit: 'tunic', hat: 'helmet_us', age: 0.2 },
  // ---- WW1 / Napoleonic / ancient / Vietnam ----
  kaiser: { nation: 'GERI', outfit: 'tunic', hat: 'peaked', facial: 'handlebar', extra: ['medals'], age: 0.55 },
  ww1_german: { nation: 'GERI', outfit: 'tunic', hat: 'helmet_de', age: 0.2 },
  ww1_british: { nation: 'UK', outfit: 'tunic', hat: 'helmet_uk', facial: 'handlebar', age: 0.2 },
  ww1_french: { nation: 'FRA', outfit: 'coat', color: '#7f97b8', hat: 'helmet_uk', hatColor: '#7f97b8', age: 0.2 },
  napoleon: { nation: 'FRA', outfit: 'coat', color: '#2a3550', hat: 'bicorne', hair: 'short', extra: ['epaulettes'], age: 0.4 },
  wellington: { nation: 'UK', outfit: 'coat', color: '#2b2b2b', hat: 'bicorne', hair: 'curly', age: 0.5 },
  kutuzov: { nation: 'RUS', outfit: 'coat', hat: 'peaked', hair: 'bald', build: 1.25, extra: ['medals', 'jowls'], age: 0.85 },
  hannibal: { nation: 'CARTH', outfit: 'armor', color: '#7a5aa0', facial: 'beard', hair: 'curly', age: 0.4 },
  roman_legionary: { nation: 'SPQR', outfit: 'armor', color: '#a8322c', hat: 'roman', age: 0.2 },
  caesar: { nation: 'SPQR', outfit: 'robe', color: '#f1ece0', hair: 'short', age: 0.6 },
  vn_soldier: { nation: 'VN', outfit: 'tunic', hat: 'pith_vn', age: 0.2 },
  vn_peasant: { nation: 'VN', outfit: 'civil', color: '#3a3a3a', hat: 'conical', age: 0.3 },
  // ---- civilians / presenters ----
  civilian_man: { outfit: 'civil', hair: 'short', age: 0.4 },
  civilian_woman: { outfit: 'dress', color: '#7a8fb0', hair: 'bun', female: true, age: 0.35, extra: ['blush'] },
  worker: { outfit: 'civil', color: '#5b6f8a', hat: 'garrison', hatColor: '#4a4a4a', age: 0.35 },
  diplomat: { outfit: 'suit', hair: 'part', age: 0.55, extra: ['tie'] },
  reporter: { outfit: 'suit', color: '#6b5a46', hat: 'fedora', hatColor: '#6b5a46', age: 0.35 },
  narrator_archivist: { outfit: 'suit', color: '#5a4636', hair: 'baldtop', hairColor: '#cfc8bd', glasses: 'round', age: 0.75, extra: ['bowtie'] },
  narrator_accountant: { outfit: 'suit', color: '#3f5a4a', hair: 'part', glasses: 'round', facial: 'pencil', age: 0.55, extra: ['tie'] },
};

export const resolveCast = (cast: Record<string, { preset?: string } & Record<string, unknown>> | undefined, who: string, inline?: Record<string, unknown>): CharSpec => {
  const m = cast?.[who];
  const presetName = (m?.preset as string | undefined) ?? (PRESETS[who] ? who : undefined);
  const base = presetName ? PRESETS[presetName] ?? {} : {};
  const { preset: _p, name: _n, ...rest } = (m ?? {}) as Record<string, unknown>;
  return { ...base, ...(rest as CharSpec), ...((inline ?? {}) as CharSpec) };
};
