import { readdirSync,readFileSync,writeFileSync } from 'node:fs';
const base=process.env.VITE_DEPLOY_BASE??'/';
if(base==='/')process.exit(0);
const walk=dir=>readdirSync(dir,{withFileTypes:true}).filter(e=>!e.name.startsWith('.')).flatMap(e=>e.isDirectory()?walk(`${dir}/${e.name}`):[`${dir}/${e.name}`]);
for(const file of walk('dist')){
  if(!/\.(html|js|css|json|webmanifest|svg|txt)$/.test(file)||file.endsWith('/sw.js'))continue;
  const source=readFileSync(file,'utf8');
  const updated=source.replace(/(?<![\w:.-])\/assets\//g,`${base}assets/`);
  if(updated!==source)writeFileSync(file,updated);
}
