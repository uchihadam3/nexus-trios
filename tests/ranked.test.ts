import {describe,expect,it} from 'vitest';
import {characters} from '../src/data/characters';
import {generateCampaign} from '../src/engine/campaign';
import {replayRanked,rosterFingerprint,runDigest} from '../src/engine/ranked';

describe('replay compartilhado da ranqueada',()=>{
  const seed=56789,banned=new Set(generateCampaign(seed).flatMap(x=>x.team));
  const team=characters.map(c=>c.id).filter(id=>!banned.has(id)).slice(0,3);
  it('reproduz pontuação e resultados sem depender do estado da tela',()=>{
    const first=replayRanked(team,seed),second=replayRanked(team,seed);
    expect(first).toEqual(second);
    expect(first.score).toBeGreaterThanOrEqual(first.encountersCleared*1_000_000);
    expect(first.score).toBeLessThan((first.encountersCleared+1)*1_000_000);
    expect(first.summaries.length).toBe(first.encountersCleared+(first.encountersCleared===10?0:1));
    expect(rosterFingerprint()).toMatch(/^fnv1a-[0-9a-f]{8}$/);
  });
  it('liga o digest ao run_id, trio, seed e sequência de resultados',async()=>{
    const outcomes=replayRanked(team,seed).summaries.map(s=>s.won);
    const digest=await runDigest('run-a',team,seed,outcomes);
    expect(digest).toMatch(/^[0-9a-f]{64}$/);
    expect(await runDigest('run-a',team,seed,outcomes)).toBe(digest);
    expect(await runDigest('run-b',team,seed,outcomes)).not.toBe(digest);
    expect(await runDigest('run-a',team,seed,[...outcomes,!outcomes.at(-1)])).not.toBe(digest);
  });
  it('recusa trio repetido e integrantes de rivais',()=>{
    expect(()=>replayRanked([team[0],team[0],team[1]],seed)).toThrow();
    expect(()=>replayRanked([generateCampaign(seed)[0].team[0],team[1],team[2]],seed)).toThrow();
  });
});
