// Tactical judgment. This value never changes a character's raw damage, Condition, charge, or speed.
const explicit:Record<string,number>={
  batman:99,light:98,aizen:98,doctordoom:98,professorx:97,ironman:96,kakashi:95,ultron:95,
  strange:93,vision:92,magneto:92,loid:92,frieren:91,itachi:91,griffith:90,kaiba:90,makima:90,
  piccolo:89,roy:89,yugi:88,greenlantern:88,cyclops:87,jeangrey:87,thanos:86,frieza:86,
  flash:85,gojo:85,sasuke:84,raven:84,hisoka:84,kurapika:89,levi:82,giorno:88,captain:82,
  superman:78,spiderman:78,wonderwoman:81,thor:76,vegeta:72,megumi:82,killua:80,edward:78,
  loki:86,gambit:82,cyborg:84,aquaman:75,captainmarvel:78,blackpanther:88,antman:83,
  naruto:68,sakura:73,tanjiro:65,muzan:78,ichigo:64,mikasa:67,jotaro:76,dio:74,jinwoo:76,
  storm:78,shazam:62,pikachu:67,wolverine:53,gohan:72,alphonse:69,eren:55,gon:57,kaneki:63,
  yor:70,starlord:78,moonknight:73,blade:72,scarletwitch:82,silversurfer:84,groot:56,
  luffy:47,deadpool:61,nezuko:49,yuji:55,nobara:61,sukuna:75,rukia:74,denji:44,anya:72,
  rogue:65,venom:48,carnage:39,greengoblin:86,ghostrider:47,
  saitama:22,hulk:34,inosuke:28,zenitsu:38,power:31,kenpachi:36,guts:43,
};
const strategicTags=new Set(['plan','tactician','investigator','control','psychic','support','protector']);
const impulsiveTags=new Set(['surge','berserker','predator','gamble','revenant']);
export function intelligenceFor(id:string,tags:string[]):number{
  const direct=explicit[id];
  if(direct!==undefined)return direct;
  let score=58;
  for(const tag of tags){
    if(strategicTags.has(tag))score+=tag==='plan'||tag==='tactician'||tag==='investigator'?7:4;
    if(impulsiveTags.has(tag))score-=tag==='berserker'||tag==='surge'?7:4;
  }
  return Math.max(40,Math.min(88,Math.round(score)));
}
