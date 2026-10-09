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
  marked:{name:'Marcado',color:'#fd939b',stack:'refresh',cap:.4,tone:'negativo',description:'Os rivais miram nele, e os golpes nele atravessam escudo.'},
  slow:{name:'Lento',color:'#9da4c9',stack:'refresh',cap:.65,tone:'negativo',description:'Quem tem Lento demora mais para dar o próximo golpe e para preparar as habilidades.'},
  haste:{name:'Acelerado',color:'#d2f66b',stack:'refresh',cap:.8,tone:'positivo',description:'Quem tem Acelerado dá o próximo golpe e prepara as habilidades mais rápido.'},
  confused:{name:'Confuso',color:'#dba0fa',stack:'refresh',cap:1,tone:'negativo',description:'Pode errar a ação normal e atingir a si mesmo.'},
  rooted:{name:'Preso',color:'#e0e2e6',stack:'refresh',cap:.65,tone:'negativo',description:'Quem tem Preso demora mais para dar o próximo golpe e para preparar as habilidades. Vale junto com Lento: quem tem os dois fica ainda mais lento.'},
  regen:{name:'Regeneração',color:'#a1e992',stack:'add',cap:25,tone:'positivo',description:'Recupera Vida por segundo.'},
  burning:{name:'Queimando',color:'#fb986e',stack:'add',cap:30,tone:'negativo',description:'Perde Vida por segundo.'},
  electric:{name:'Eletrificado',color:'#f9df7c',stack:'add',cap:.35,tone:'negativo',description:'Choque: cada golpe recebido atrasa a próxima ação.'},
  silenced:{name:'Silenciado',color:'#b6a3d7',stack:'refresh',cap:1,tone:'negativo',description:'Não inicia habilidades; preparações em andamento continuam.'},
  strengthened:{name:'Fortalecido',color:'#e2f391',stack:'add',cap:.8,tone:'positivo',description:'Causa mais dano.'},
  weakened:{name:'Enfraquecido',color:'#bca4cf',stack:'refresh',cap:.6,tone:'negativo',description:'Causa menos dano.'},
};
