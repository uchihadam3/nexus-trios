export type Side = 'player' | 'enemy';
export type StatusId = 'exposed' | 'paralyzed' | 'protected' | 'marked' | 'slow' | 'haste' | 'confused' | 'rooted' | 'regen' | 'burning' | 'electric' | 'silenced' | 'strengthened' | 'weakened' | 'provoked' | 'vampirism' | 'reflect' | 'thorns' | 'poison' | 'bleed' | 'cursed' | 'frozen' | 'sleep' | 'blind' | 'barrier';
export type Topic = 'time' | 'action' | 'dealt' | 'received' | 'allyHurt' | 'enemyHurt' | 'interrupt' | 'status' | 'negativeStatus' | 'protected' | 'enemyCast' | 'survived' | 'losing' | 'winning';
/** `allyFallen`: o aliado caído que ainda pode ser levantado (Reviver). */
export type Target = 'enemyWeak' | 'enemyStrong' | 'enemyCast' | 'investigated' | 'allyWeak' | 'self' | 'allEnemies' | 'allAllies' | 'randomEnemy' | 'allyFallen';
export type TargetIntent = 'offense'|'finisher'|'interrupt'|'control'|'heal'|'protect'|'buff'|'investigate';
export type Visual = 'beam' | 'bolt' | 'slash' | 'web' | 'shield' | 'wave' | 'psychic' | 'impact';
/** `revive`: levanta um aliado caído com `value` (fração) da Vida — uma vez por luta para quem levanta, e cada lutador só volta uma vez. */
export type Effect = { kind: 'damage' | 'heal' | 'shield' | 'investigate' | 'deathnote' | 'charge' | 'shift' | 'revive' | 'lifesteal' | 'cleanse' | 'dispel'; value: number; target?: Target } | {kind:'store';value:number;cap:number;target?:Target} | {kind:'release';multiplier:number;target?:Target} | {kind:'status';status:StatusId;value:number;duration:number;target?:Target} | {kind:'interrupt';value:number;mode:'cancel'|'delay'|'reduce';target?:Target};
export interface ChargeRule { on: Topic; amount: number }
export interface Skill {
  id:string; name:string; icon:Visual; description:string; chargeText:string; charge:ChargeRule[];
  condition:'always'|'injured'|'enemyCast'|'threatened'|'investigated'|'vulnerable'|'storedEnergy';
  requiresSkills?:number[];
  target:Target; effects:Effect[]; preparation:number; cooldown:number; priority:number;
}
export interface Trait {name:string;description:string; on:Topic; cooldown:number; effects:Effect[]; target:Target}
export interface Character {
  id:string; name:string; universe:string; portrait:string; color:string; symbol:string; idea:string; vulnerability:string; intelligence?:number;
  hp:number; interval:number; basic:{name:string;effects:Effect[];visual:Visual;target:Target};
  trait:Trait; skills:[Skill,Skill,Skill]; tags:string[]; power:number; deathNoteCompatible:boolean;
  /** Renascer: ao cair, volta sozinho com `vida` (fração) da Vida depois de `atraso` segundos — uma vez por luta. A Death Note impede. */
  renascer?:{vida:number;atraso:number};
}
export interface Status {id:StatusId;remaining:number;intensity:number;source:string;duration?:number}
export interface Shield {amount:number;remaining:number;source:string}
export interface SkillState {charge:number;cooldown:number;executing:number;uses:number;readySince?:number|null}
export interface Fighter {
  uid:string;characterId:string;side:Side;slot:number;hp:number;maxHp:number;action:number;
  skills:SkillState[];statuses:Status[];shields:Shield[];
  cast:null|{skill:number;elapsed:number;duration:number;targets:string[]};
  investigation:Record<string,number>;discovered?:Record<string,'vulnerable'|'immune'>;traitTimer:number;
  storedEnergy:number;
  /** Renascer: segundos até voltar (enquanto caído). */
  renascendo?:number;
  /** Já voltou uma vez (renasceu ou foi levantado): não volta de novo. */
  voltou?:boolean;
  /** Já levantou um aliado nesta luta (Reviver é uma vez por luta). */
  reviveu?:boolean;
  stats:{damage:number;healing:number;protection:number;interrupts:number;skills:number;kills:number;
    /** Feitos que não viram número na tela (para os pontos): segundos de Status ruim no rival e bom no trio, ação adiantada/atrasada, Carga dada a aliados. Opcionais: lutas salvas antes não têm. */
    debuffs?:number;buffs?:number;tempo?:number;carga?:number;
    /** Aliados levantados (Reviver). */
    revives?:number};
}
export interface BattleEvent {id:number;time:number;kind:'basic'|'skill'|'cast'|'damage'|'heal'|'shield'|'status'|'interrupt'|'ko'|'synergy'|'charge'|'tempo'|'turn'|'ready'|'block'|'discovery'|'revive'|'cleanse'|'dispel'|'miss'|'resist';source:string;target?:string;skill?:number;label:string;value?:number;visual?:Visual;status?:StatusId;attacker?:string;
  /** Purificar/Dissipar: os Status que saíram, na ordem. */
  removidos?:StatusId[]}
export interface TargetDecision {time:number;actor:string;intent:TargetIntent;target:string;score:number;reasons:string[]}
export interface SkillDecision {time:number;actor:string;intelligence:number;candidates:{skill:string;score:number;target?:string;reasons:string[]}[];chosen:string}
export interface Battle {
  version:1;seed:number;rng:number;time:number;fighters:Fighter[];dominion:number;momentum:number;events:BattleEvent[];nextEvent:number;
  winner:Side|null;reason:string;finished:boolean;turns:number;lastLead:Side|null;
  /** Viradas a favor do trio do jogador (as que contam pontos, como no ranking). */
  viradasDoTrio?:number;
  /** Optional for backward compatibility with battles saved by earlier builds. */
  targetMemory?:Record<string,{target:string;time:number}>;
  targetLog?:TargetDecision[];
  decisionLog?:SkillDecision[];
}
