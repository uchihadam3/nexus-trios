import { Lightbulb,Lock } from 'lucide-react';
import { CUSTO_DAS_DICAS,formatarPontos } from '../engine/pontos';
import { META_DAS_DICAS } from '../lib/dicas-liberadas';

/*
 * O botão das Dicas de trio fica na tela inicial, antes da jornada começar.
 *
 * Pedido do jogador: "a pessoa consegue clicar no botão de dica, ver quem é o
 * melhor… aí ela desliga e escolhe ele. O botão de dica tinha que estar na tela
 * anterior". A escolha vale para a jornada inteira: na escolha do trio não dá
 * mais para ligar nem desligar (src/screens/DraftScreen.tsx só mostra o aviso).
 * Trancado até META_DAS_DICAS pontos numa jornada (src/lib/dicas-liberadas.ts).
 */
export function BotaoDicas({ligado,liberado,onMudar}:{ligado:boolean;liberado:boolean;onMudar:(ligar:boolean)=>void}){
  if(!liberado)return <button className="dv-dicas trancado" role="switch" aria-checked={false} aria-disabled="true" disabled>
    <span className="dv-dicas-lampada"><Lock size={18}/></span>
    <span className="dv-dicas-texto"><b>DICAS DE TRIO</b><small>libera ao fazer <em>{formatarPontos(META_DAS_DICAS)} pontos</em> com um trio</small></span>
    <span className="dv-dicas-chave" aria-hidden><i/></span>
  </button>;
  return <button className={`dv-dicas ${ligado?'ligado':''}`} role="switch" aria-checked={ligado} onClick={()=>onMudar(!ligado)}>
    <span className="dv-dicas-lampada"><Lightbulb size={20}/></span>
    <span className="dv-dicas-texto"><b>DICAS DE TRIO</b><small>{ligado?<>ligadas · <em>−{formatarPontos(CUSTO_DAS_DICAS)} por luta</em></>:'desligadas · pontos cheios'}</small></span>
    <span className="dv-dicas-chave" aria-hidden><i/></span>
  </button>;
}
