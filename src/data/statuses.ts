import type { StatusId } from '../engine/types';
export const statuses: Record<StatusId,{name:string;color:string;stack:'refresh'|'add';cap:number;description:string}> = {
  exposed:{name:'Exposto',color:'#ff9475',stack:'add',cap:.65,description:'Recebe mais dano.'},
  paralyzed:{name:'Paralisado',color:'#f5d36c',stack:'refresh',cap:1,description:'Não age nem avança preparações.'},
  protected:{name:'Protegido',color:'#81dccc',stack:'refresh',cap:.7,description:'Reduz dano e resiste a interrupções.'},
  marked:{name:'Marcado',color:'#fd939b',stack:'refresh',cap:.4,description:'Recebe dano adicional e atenção dos inimigos.'},
  slow:{name:'Lento',color:'#9da4c9',stack:'refresh',cap:.65,description:'O círculo de ação e as preparações avançam mais devagar.'},
  haste:{name:'Acelerado',color:'#d2f66b',stack:'refresh',cap:.8,description:'Ações normais e preparações mais rápidas.'},
  confused:{name:'Confuso',color:'#dba0fa',stack:'refresh',cap:1,description:'Pode errar a ação normal e atingir a si mesmo.'},
  rooted:{name:'Preso',color:'#e0e2e6',stack:'refresh',cap:.65,description:'Ataca e prepara habilidades mais devagar. Acumula separadamente com Lento.'},
  regen:{name:'Regeneração',color:'#a1e992',stack:'add',cap:25,description:'Recupera Vida por segundo.'},
  burning:{name:'Queimando',color:'#fb986e',stack:'add',cap:30,description:'Perde Vida por segundo.'},
  electric:{name:'Eletrificado',color:'#f9df7c',stack:'add',cap:.35,description:'Recebe dano adicional.'},
  silenced:{name:'Silenciado',color:'#b6a3d7',stack:'refresh',cap:1,description:'Não inicia habilidades; preparações em andamento continuam.'},
  strengthened:{name:'Fortalecido',color:'#e2f391',stack:'add',cap:.8,description:'Causa mais dano.'},
  weakened:{name:'Enfraquecido',color:'#bca4cf',stack:'refresh',cap:.6,description:'Causa menos dano.'},
};
