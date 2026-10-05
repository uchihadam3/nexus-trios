import { mkdir,readdir,unlink,writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { characters } from '../../src/data/characters';
import { skillArtSlug,skillArtPath } from '../../src/data/skill-art';

const root=resolve('public/assets/skills');
const palettes:Record<string,[string,string]>={
  energy:['#f7cc72','#fd7a5c'],electric:['#f4ef86','#6ad8ff'],physical:['#f5c681','#f57976'],
  shield:['#8ee4d7','#65a6ff'],heal:['#a6f0bc','#6ad8ff'],psychic:['#d8b8ff','#88a9ff'],
  magic:['#cfadff','#69d9da'],dark:['#d2b1ff','#846af0'],slash:['#ffc37d','#fa718f'],
  prison:['#84e3df','#82a4ff'],buff:['#f3d47f','#a6efb5'],debuff:['#f69a94','#b995f2'],
  speed:['#91e8f3','#ffdb8a'],note:['#f2cf8c','#f3849d'],area:['#bdadff','#78d3e9'],
};
const clean=(s:string)=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
function family(name:string,description:string){
  const s=clean(`${name} ${description}`);
  if(/death note|sentenca|investig|observ|analise|plano|estrateg|leitura|sharingan|sharingan|contramed|informacao/.test(s))return 'note';
  if(/raio|eletric|relamp|trov|choque|chidori|pika|faísca|faísc|flash/.test(s))return 'electric';
  if(/cura|cura|recuper|cura|regen|regener|vida/.test(s))return 'heal';
  if(/escud|protec|barreira|muralha|defesa|infinito|guard|bloque/.test(s))return 'shield';
  if(/pris|prend|teia|armad|algema|campo|raiz|gravit|laço|laco|ancora|âncora/.test(s))return 'prison';
  if(/sombra|sombr|escura|sombr|void|vazio|alma|raven|dark/.test(s))return 'dark';
  if(/corte|golpe|soco|lâmina|lamina|espada|garras|batarang|slash|impact|giro/.test(s))return 'slash';
  if(/aceler|veloc|rápid|rapid|haste|passo|fuga|impulso|gear/.test(s))return 'speed';
  if(/fortal|poder|força|forca|cresce|kaioken|manto|buff|aument/.test(s))return 'buff';
  if(/enfraq|marc|expost|queim|lento|confus|silenc|debilit|control|paralis/.test(s))return 'debuff';
  if(/dominio|magia|jutsu|feiti|místico|mistic|portal|dimens|tempo|encant/.test(s))return 'magic';
  if(/psiqu|mente|mental|ilusão|ilusao|telepat|telecines|gravidade|genjutsu/.test(s))return 'psychic';
  if(/onda|raio|energia|beam|explos|canhao|canhão|kamehameha|galick|unibeam|rajada|laser|flash final/.test(s))return 'energy';
  if(/todos|área|area|equipe|trio|campo|onda|explosão|explosao/.test(s))return 'area';
  return 'physical';
}
const art:Record<string,string>={
  energy:`<path d="M52 12 32 48l15-3-5 37 25-45-17 4 8-29Z" fill="url(#g)" stroke="url(#g)" stroke-linejoin="round"/><path d="M18 33 30 40M72 55 83 62M64 18l8-7"/>`,
  electric:`<path d="m55 11-25 37 17-1-8 39 34-48-19 3 8-30Z" fill="url(#g)" stroke="url(#g)" stroke-linejoin="round"/><path d="m17 53 8-4m47-27 8-5M20 29l6 4"/>`,
  physical:`<path d="m48 13 8 22 24-8-14 20 18 16-25-3-9 24-7-24-25 4 17-18-15-19 24 9 4-23Z" fill="url(#g)" stroke="url(#g)" stroke-linejoin="round"/><circle cx="48" cy="49" r="8"/>`,
  shield:`<path d="m48 12 27 10v21c0 18-11 31-27 41-16-10-27-23-27-41V22l27-10Z" fill="url(#g)" fill-opacity=".18" stroke="url(#g)" stroke-width="4"/><path d="m34 47 10 10 19-22"/>`,
  heal:`<circle cx="48" cy="48" r="30" fill="url(#g)" fill-opacity=".14" stroke="url(#g)" stroke-width="3"/><path d="M48 28v40M28 48h40" stroke-width="8" stroke-linecap="round"/><path d="M17 24q11-14 25-12m29 68q11-6 15-19"/>`,
  psychic:`<path d="M13 48q35-36 70 0-35 36-70 0Z" fill="url(#g)" fill-opacity=".16" stroke="url(#g)" stroke-width="3"/><circle cx="48" cy="48" r="13" fill="url(#g)"/><circle cx="48" cy="48" r="5" fill="#101522"/><path d="M48 12v8m0 56v8M12 48h8m56 0h8"/>`,
  magic:`<circle cx="48" cy="48" r="31" stroke="url(#g)" stroke-dasharray="3 5"/><circle cx="48" cy="48" r="20" stroke="url(#g)"/><path d="m48 27 18 21-18 21-18-21 18-21Z" fill="url(#g)" fill-opacity=".22"/><circle cx="48" cy="48" r="5" fill="url(#g)"/>`,
  dark:`<circle cx="48" cy="48" r="29" fill="url(#g)" fill-opacity=".2" stroke="url(#g)" stroke-width="3"/><path d="M61 21C39 26 31 46 39 65c5 11 16 13 24 9-20 16-48 2-48-23 0-25 24-43 46-30Z" fill="url(#g)"/><path d="m69 25 3-7m8 24 7-2M21 69l-6 5"/>`,
  slash:`<path d="M17 70Q41 48 78 19M15 81Q48 57 84 28" stroke="url(#g)" stroke-width="5" stroke-linecap="round"/><path d="m24 53-7-2m19-8-4-8m44-15 2-8"/>`,
  prison:`<path d="m48 12 29 17v34L48 80 19 63V29l29-17Z" fill="url(#g)" fill-opacity=".1" stroke="url(#g)" stroke-width="3"/><path d="M32 21v54M47 14v67M62 21v54M21 37h54M21 54h54"/><circle cx="48" cy="47" r="9" fill="#111625" stroke="url(#g)"/>`,
  buff:`<path d="M21 66Q21 28 56 28h13l-9-10 7-7 22 22-22 22-7-7 9-9H56Q34 39 34 62v5Z" fill="url(#g)" fill-opacity=".23" stroke="url(#g)" stroke-width="3"/><path d="M30 78h38"/>`,
  debuff:`<path d="m48 13 28 48H20l28-48Z" fill="url(#g)" fill-opacity=".19" stroke="url(#g)" stroke-width="3"/><path d="M48 31v15m0 8v1" stroke-width="5" stroke-linecap="round"/><path d="M17 73h62"/>`,
  speed:`<path d="M55 14 28 50h19l-5 32 28-43H51l4-25Z" fill="url(#g)" stroke="url(#g)" stroke-linejoin="round"/><path d="M14 35h16M10 49h13m-8 14h17"/>`,
  note:`<path d="M26 14h34l12 12v55H26V14Z" fill="url(#g)" fill-opacity=".16" stroke="url(#g)" stroke-width="3"/><path d="M60 14v15h13M35 42h27M35 52h27M35 62h18"/><path d="m59 67 4 4 8-10" stroke-width="3"/>`,
  area:`<circle cx="48" cy="48" r="32" stroke="url(#g)" stroke-width="3"/><circle cx="48" cy="48" r="21" stroke="url(#g)" stroke-dasharray="2 4"/><circle cx="48" cy="48" r="8" fill="url(#g)"/><path d="M48 8v12m0 56v12M8 48h12m56 0h12"/>`,
};
function hash(value:string){let h=0;for(const ch of value)h=(h*33+ch.charCodeAt(0))>>>0;return h;}
function svgFor(id:string,name:string,description:string){
  const kind=family(name,description),[a,b]=palettes[kind],h=hash(id),rotate=h%24-12,scale=.95+(h%8)*.012;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" fill="none" stroke-linecap="round" stroke-linejoin="round"><defs><linearGradient id="g" x1="15" y1="12" x2="81" y2="84" gradientUnits="userSpaceOnUse"><stop stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient><radialGradient id="bg"><stop stop-color="${a}" stop-opacity=".14"/><stop offset="1" stop-color="#101522" stop-opacity=".92"/></radialGradient></defs><rect x="5" y="5" width="86" height="86" rx="24" fill="url(#bg)" stroke="#ffffff" stroke-opacity=".12"/><path d="M48 9v4M48 83v4M9 48h4m70 0h4" stroke="#dce8ff" stroke-opacity=".36"/><g transform="rotate(${rotate} 48 48) scale(${scale})" transform-origin="48 48" stroke-width="2.5" stroke="url(#g)">${art[kind]}</g><circle cx="77" cy="20" r="2" fill="${b}"/><circle cx="18" cy="75" r="1.6" fill="${a}" opacity=".7"/></svg>`;
}
await mkdir(root,{recursive:true});
for(const file of await readdir(root))if(file.endsWith('.svg'))await unlink(resolve(root,file));
const skills=characters.flatMap(character=>character.skills.map(skill=>({id:skill.id,name:skill.name,description:skill.description,character:character.id})));
for(const skill of skills)await writeFile(resolve(root,`${skillArtSlug(skill.id)}.svg`),svgFor(skill.id,skill.name,skill.description));
await writeFile(resolve(root,'manifest.json'),JSON.stringify({count:skills.length,skills:skills.map(skill=>({id:skill.id,character:skill.character,name:skill.name,path:skillArtPath(skill.id)}))},null,2)+'\n');
console.info(`Gerados ${skills.length} ícones de habilidades em ${root}`);
