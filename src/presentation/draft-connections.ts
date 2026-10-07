import type { Character,Effect,Target } from '../engine/types';

const aid=(effect:Effect)=>effect.kind==='charge'?'acelera habilidades':effect.kind==='heal'?'recupera Vida':effect.kind==='shield'?'oferece Escudo':effect.kind==='status'&&effect.status==='haste'?'acelera ataques':effect.kind==='status'&&effect.status==='protected'?'reduz dano recebido':effect.kind==='status'&&effect.status==='regen'?'regenera Vida':effect.kind==='status'&&effect.status==='strengthened'?'aumenta dano':null;
export function draftConnection(candidate:Character,team:Character[]):string|null{
  if(!team.length)return null;
  for(const from of [candidate,...team]){
    const receivers=from.id===candidate.id?team:[candidate];
    const effects:{effect:Effect;target:Target}[]=[...from.skills.flatMap(s=>s.effects.map(effect=>({effect,target:effect.target??s.target}))),...from.trait.effects.map(effect=>({effect,target:effect.target??from.trait.target}))];
    for(const {effect,target} of effects){
      const help=aid(effect);
      /*
       * Quem recebe, dito com precisão.
       *
       * Um efeito que mira `allAllies` alcança o trio inteiro, mas a frase
       * nomeava só o primeiro aliado da lista — verdade pela metade, e a
       * metade que some é justamente o que torna a conexão boa.
       */
      if(help&&['allAllies','allyWeak'].includes(target)){
        const quem=target==='allAllies'?'o trio todo':receivers[0]!.name;
        return `${from.name} ${target==='allyWeak'?'pode ajudar':'ajuda'} ${quem}: ${help}`;
      }
    }
  }
  return null;
}
