import type { StatusId } from '../engine/types';
/*
 * O tom mora aqui, junto do Status.
 *
 * Antes existiam duas listas: `positiveStatuses` na apresentação e
 * `negativeStatuses` no motor, em arquivos diferentes, nenhuma derivada da
 * outra. Enquanto as duas estiverem corretas ninguém percebe; no dia em que um
 * Status novo entrar numa e não na outra, elas discordam em silêncio — e quem
 * depende disso para decidir em quem um efeito cai erra sem avisar.
 *
 * Uma lista só, no lugar onde o Status é definido.
 */
/** Eletrificado: cada golpe recebido tira (intensidade × isto) da barra de ação de quem está eletrificado. */
export const CHOQUE_DO_ELETRIFICADO=.6;
export const statuses: Record<StatusId,{name:string;color:string;stack:'refresh'|'add';cap:number;tone:'positivo'|'negativo';description:string}> = {
  exposed:{name:'Exposto',color:'#ff9475',stack:'add',cap:.65,tone:'negativo',description:'Recebe mais dano.'},
  paralyzed:{name:'Paralisado',color:'#f5d36c',stack:'refresh',cap:1,tone:'negativo',description:'Não age nem avança preparações.'},
  protected:{name:'Protegido',color:'#81dccc',stack:'refresh',cap:.7,tone:'positivo',description:'Reduz dano e resiste a interrupções.'},
  marked:{name:'Marcado',color:'#fd939b',stack:'refresh',cap:.4,tone:'negativo',description:'Os rivais miram nele: o trio inteiro foca no marcado.'},
  slow:{name:'Lento',color:'#9da4c9',stack:'refresh',cap:.65,tone:'negativo',description:'Quem tem Lento demora mais para dar o próximo golpe e para preparar as habilidades.'},
  haste:{name:'Acelerado',color:'#d2f66b',stack:'refresh',cap:.8,tone:'positivo',description:'Quem tem Acelerado dá o próximo golpe e prepara as habilidades mais rápido.'},
  confused:{name:'Confuso',color:'#dba0fa',stack:'refresh',cap:1,tone:'negativo',description:'Pode errar a ação normal e atingir a si mesmo.'},
  rooted:{name:'Preso',color:'#e0e2e6',stack:'refresh',cap:.65,tone:'negativo',description:'Quem tem Preso demora mais para dar o próximo golpe e para preparar as habilidades. Vale junto com Lento: quem tem os dois fica ainda mais lento.'},
  regen:{name:'Regeneração',color:'#a1e992',stack:'refresh',cap:25,tone:'positivo',description:'Recupera Vida por segundo. Não soma: vale a mais forte.'},
  burning:{name:'Queimando',color:'#fb986e',stack:'add',cap:30,tone:'negativo',description:'Perde Vida por segundo.'},
  electric:{name:'Eletrificado',color:'#f9df7c',stack:'add',cap:.35,tone:'negativo',description:'Choque: cada golpe recebido atrasa a próxima ação.'},
  silenced:{name:'Silenciado',color:'#b6a3d7',stack:'refresh',cap:1,tone:'negativo',description:'Não inicia habilidades; preparações em andamento continuam.'},
  strengthened:{name:'Fortalecido',color:'#e2f391',stack:'add',cap:.8,tone:'positivo',description:'Causa mais dano.'},
  weakened:{name:'Enfraquecido',color:'#bca4cf',stack:'refresh',cap:.6,tone:'negativo',description:'Causa menos dano.'},
  provoked:{name:'Provocado',color:'#ff7a52',stack:'refresh',cap:1,tone:'negativo',description:'Só consegue mirar em quem provocou: o ataque básico e as habilidades de um alvo só vão nele.'},
  vampirism:{name:'Vampirismo',color:'#e0546f',stack:'refresh',cap:.6,tone:'positivo',description:'Cada golpe de quem tem Vampirismo cura parte do dano que ele causa.'},
  reflect:{name:'Refletir',color:'#9fdcff',stack:'refresh',cap:.6,tone:'positivo',description:'Devolve parte do dano de cada golpe recebido para quem bateu.'},
  thorns:{name:'Espinhos',color:'#a6d36a',stack:'add',cap:60,tone:'positivo',description:'Quem bate em quem tem Espinhos leva um dano fixo a cada golpe.'},
  poison:{name:'Envenenado',color:'#8fd14f',stack:'add',cap:30,tone:'negativo',description:'Perde Vida por segundo, e o veneno passa por Escudo e Protegido.'},
  bleed:{name:'Sangrando',color:'#e0485a',stack:'add',cap:60,tone:'negativo',description:'Cada ação dele (ataque básico ou habilidade) custa Vida.'},
  cursed:{name:'Amaldiçoado',color:'#9b6bd6',stack:'refresh',cap:.6,tone:'negativo',description:'Recebe menos cura e menos Escudo.'},
  frozen:{name:'Congelado',color:'#9fe3ff',stack:'refresh',cap:.6,tone:'negativo',description:'Não age; o próximo golpe quebra o gelo e causa mais dano.'},
  sleep:{name:'Dormindo',color:'#b7b6f2',stack:'refresh',cap:1,tone:'negativo',description:'Não age até o sono acabar ou até levar um golpe.'},
  blind:{name:'Cego',color:'#d8d2b0',stack:'refresh',cap:.6,tone:'negativo',description:'Pode errar o ataque básico.'},
  barrier:{name:'Barreira',color:'#f5e7a1',stack:'add',cap:3,tone:'positivo',description:'Anula os próximos debuffs que receberia.'},
  evasion:{name:'Esquiva',color:'#c8f7ff',stack:'refresh',cap:.6,tone:'positivo',description:'Chance de escapar do golpe inteiro de um rival: dano e debuffs.'},
  bomb:{name:'Marca explosiva',color:'#ff9d3c',stack:'add',cap:400,tone:'negativo',description:'Explode quando o tempo acaba e causa o dano guardado. Aplicar de novo soma.'},
};
