import {describe,it,expect,afterEach} from 'vitest';
import {characters} from '../src/data/characters';
import {createBattle,applyEffects} from '../src/engine/battle';
import {journeyObjectives,achievements,masteryChallenges,emptyProgress,emptyTally,tallyEvents,battleDelta,recordProgress,refreshPeriods} from '../src/engine/progression';
import {summarizeBattle} from '../src/engine/run-summary';
import {loadProfile} from '../src/lib/storage';

afterEach(()=>{delete (globalThis as {localStorage?:unknown}).localStorage});
describe('progressão local',()=>{
  it('migra o perfil antigo sem apagar recordes',()=>{
    const memory=new Map([['nexus-v1-profile',JSON.stringify({journeys:9,victories:2,best:10,wins:37,champion:['goku','vegeta','pikachu']})]]);
    (globalThis as {localStorage?:unknown}).localStorage={getItem:(key:string)=>memory.get(key)??null};
    const p=loadProfile();expect(p.journeys).toBe(9);expect(p.best).toBe(10);expect(p.champion).toEqual(['goku','vegeta','pikachu']);expect(p.progress.xp).toBe(0);
    expect(p.progress.daily.items).toHaveLength(3);expect(p.progress.weekly.items).toHaveLength(4);
  });
  it('gera só objetivos possíveis e reproduz a mesma escolha pela seed',()=>{
    const team=['goku','light','saitama'],goals=journeyObjectives(team,42);
    expect(goals).toEqual(journeyObjectives(team,42));expect(goals).toHaveLength(3);
    expect(goals.map(x=>x.id)).not.toContain('journey-heal');
    expect(goals.map(x=>x.id)).not.toContain('journey-interrupt');
  });
  it('conta eventos uma vez, libera conquistas uma vez e rastreia as três etapas para 250',()=>{
    const b=createBattle(['goku','captain','pikachu'],['vegeta','raven','hulk'],11),source=b.fighters[0],enemy=b.fighters[3];
    source.skills[0].uses=1;source.skills[2].uses=2;
    applyEffects(b,source,[enemy],[{kind:'status',status:'exposed',value:.2,duration:5}]);
    const tally=tallyEvents(emptyTally(),b.events);expect(tallyEvents(tally,b.events)).toEqual(tally);
    const summary=summarizeBattle(0,b),delta=battleDelta(summary,b,tally,[],['goku','captain','pikachu']);
    const first=recordProgress(emptyProgress(),delta,b,['goku','captain','pikachu']);
    expect(first.mastery.goku.level).toBe(2);expect(first.mastery.goku.skills).toEqual([1,0,2]);
    expect(first.seen).toHaveLength(3);expect(new Set(first.unlocked).size).toBe(first.unlocked.length);
    const second=recordProgress(first,delta,b,['goku','captain','pikachu']);
    expect(second.mastery.goku.skills).toEqual([2,0,4]);expect(new Set(second.unlocked).size).toBe(second.unlocked.length);
    expect(achievements).toHaveLength(50);
    expect(characters).toHaveLength(250);
    expect(characters.every(c=>masteryChallenges(c.id).length===3&&masteryChallenges(c.id).every(text=>text.includes(c.skills[0].name)||text.includes(c.skills[2].name)||text.includes(c.name)))).toBe(true);
  });
  it('reinicia períodos em UTC e preserva progresso no reload',()=>{
    const p=refreshPeriods(emptyProgress(),new Date('2026-10-07T12:00:00Z'));
    p.daily.items[0].progress=1;
    expect(refreshPeriods(p,new Date('2026-10-07T23:59:59Z')).daily.items[0].progress).toBe(1);
    expect(refreshPeriods(p,new Date('2026-10-08T00:00:00Z')).daily.items[0].progress).toBe(0);
    expect(refreshPeriods(p,new Date('2026-10-08T00:00:00Z')).weekly.items).toEqual(p.weekly.items);
  });
});
