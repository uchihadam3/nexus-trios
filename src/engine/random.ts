export function random(state:{rng:number}):number {
  state.rng=(Math.imul(state.rng,1664525)+1013904223)>>>0;
  return state.rng/4294967296;
}
export function shuffle<T>(items:T[],state:{rng:number}):T[] {
  const copy=[...items];
  for(let i=copy.length-1;i>0;i--){const j=Math.floor(random(state)*(i+1));[copy[i],copy[j]]=[copy[j],copy[i]];}
  return copy;
}
