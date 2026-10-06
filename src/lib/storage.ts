import type { Battle } from '../engine/types';
import type { Draft, Encounter } from '../engine/campaign';
import { byId } from '../data/characters';
import { PRESENTATION as P } from '../presentation/config';
import type { PresentationCheckpoint } from '../presentation/director';
import type { RunBattleSummary,RunSynergyEvent } from '../engine/run-summary';
export interface Settings {volume:number;musicVolume:number;effectsVolume:number;effects:boolean;speed:1|2;numbers:boolean;reducedMotion:boolean;auto:boolean;explanations:'normal'|'detailed'|'off'}
export interface Run {seed:number;team:string[];encounters:Encounter[];index:number;stage:'draft'|'battle'|'result';draft:Draft;battle:Battle|null;recorded:boolean;presentation?:PresentationCheckpoint;summaries?:RunBattleSummary[];battleSynergies?:RunSynergyEvent[]}
export interface Profile {journeys:number;victories:number;best:number;wins:number;champion?:string[]}
export const defaults:Settings={volume:P.audio.master,musicVolume:P.audio.music,effectsVolume:P.audio.effects,effects:true,speed:1,numbers:false,reducedMotion:typeof matchMedia!=='undefined'&&matchMedia('(prefers-reduced-motion: reduce)').matches,auto:false,explanations:'normal'};
const prefix='nexus-v1-';
export let storageAvailable=true;
function read(key:string):unknown{try{return JSON.parse(localStorage.getItem(prefix+key)??'null');}catch{return null;}}
export function save(key:string,value:unknown){try{localStorage.setItem(prefix+key,JSON.stringify(value));storageAvailable=true;}catch{storageAvailable=false;}}
export function loadSettings():Settings{const raw=read('settings');if(!raw||typeof raw!=='object')return defaults;const x=raw as Partial<Settings>;return {volume:typeof x.volume==='number'?Math.max(0,Math.min(100,x.volume)):P.audio.master,musicVolume:typeof x.musicVolume==='number'?Math.max(0,Math.min(100,x.musicVolume)):P.audio.music,effectsVolume:typeof x.effectsVolume==='number'?Math.max(0,Math.min(100,x.effectsVolume)):P.audio.effects,effects:typeof x.effects==='boolean'?x.effects:true,speed:x.speed===2?2:1,numbers:x.numbers===true,reducedMotion:typeof x.reducedMotion==='boolean'?x.reducedMotion:defaults.reducedMotion,auto:x.auto===true,explanations:x.explanations==='detailed'||x.explanations==='off'?x.explanations:'normal'};}
export function loadProfile():Profile{const p=read('profile') as Profile|null;return p&&['journeys','victories','best','wins'].every(k=>typeof p[k as keyof Profile]==='number')?p:{journeys:0,victories:0,best:0,wins:0};}
export function loadRun():Run|null{const r=read('run') as Run|null;if(!r||!['draft','battle','result'].includes(r.stage)||!Array.isArray(r.team)||r.team.some(id=>!byId[id])||!Array.isArray(r.encounters)||r.encounters.length!==10||!r.draft||!Number.isInteger(r.index)||r.index<0||r.index>9)return null;if(r.stage!=='draft'&&(!r.battle||r.battle.version!==1||r.battle.fighters.length!==6))return null;if(r.battle){for(const f of r.battle.fighters){if(f.characterId!=='light')continue;f.discovered??={};for(const [uid,value] of Object.entries(f.investigation)){const target=r.battle.fighters.find(x=>x.uid===uid);if(value>=100&&target&&!f.discovered[uid])f.discovered[uid]=byId[target.characterId].deathNoteCompatible?'vulnerable':'immune';}}}return r;}
export function resetStorage(){try{['settings','profile','run'].forEach(key=>localStorage.removeItem(prefix+key));localStorage.removeItem('nexus-battle-guide-v1');}catch{storageAvailable=false;}}
