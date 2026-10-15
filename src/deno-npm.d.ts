/*
 * O servidor (supabase/functions, em Deno) importa o Supabase como "npm:@supabase/supabase-js@…". Os testes que rodam
 * o juiz do PvP aqui (tests/pvp-servidor.test.ts) trazem esse arquivo para o TypeScript do jogo: o mesmo pacote,
 * pelo nome que o Node conhece.
 */
declare module 'npm:@supabase/supabase-js@2.117.2' {
  export * from '@supabase/supabase-js';
}
