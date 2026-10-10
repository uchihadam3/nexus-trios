import { Lightbulb,Lock } from 'lucide-react';
import { CUSTO_DAS_DICAS,formatarPontos } from '../engine/pontos';
import { META_DAS_DICAS } from '../lib/dicas-liberadas';

/*
 * O botão das Dicas de trio, na escolha do trio.
 *
 * Pedidos do jogador: fica "no lugar que tava, nos personagens"; trancado até
 * META_DAS_DICAS pontos numa jornada (src/lib/dicas-liberadas.ts); e "se a
 * pessoa ligar e desligar, fala que ele ainda está sendo usado": ligou uma vez,
 * a jornada inteira paga −10 mil por luta, mesmo desligando depois — por isso
 * espiar a melhor escolha e desligar não adianta.
 */
export function BotaoDicas({ligado,liberado,usado=false,desativado=false,onMudar}:{ligado:boolean;liberado:boolean;/** a jornada já usou as Dicas */usado?:boolean;desativado?:boolean;onMudar:(ligar:boolean)=>void}){
  if(!liberado)return <button className="dv-dicas trancado" role="switch" aria-checked={false} aria-disabled="true" disabled>
    <span className="dv-dicas-lampada"><Lock size={18}/></span>
    <span className="dv-dicas-texto"><b>DICAS DE TRIO</b><small>libera ao fazer <em>{formatarPontos(META_DAS_DICAS)} pontos</em> com um trio</small></span>
    <span className="dv-dicas-chave" aria-hidden><i/></span>
  </button>;
  return <button className={`dv-dicas ${ligado?'ligado':''}`} role="switch" aria-checked={ligado} onClick={()=>onMudar(!ligado)} disabled={desativado}>
    <span className="dv-dicas-lampada"><Lightbulb size={20}/></span>
    <span className="dv-dicas-texto"><b>DICAS DE TRIO</b><small>{ligado?<>ligadas · <em>−{formatarPontos(CUSTO_DAS_DICAS)} por luta</em></>:usado?<>desligadas, mas já usadas nesta jornada · <em>ainda conta −{formatarPontos(CUSTO_DAS_DICAS)} por luta</em></>:'desligadas · pontos cheios'}</small></span>
    <span className="dv-dicas-chave" aria-hidden><i/></span>
  </button>;
}
