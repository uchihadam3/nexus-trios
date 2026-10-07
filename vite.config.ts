import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const base = process.env.VITE_DEPLOY_BASE ?? '/';

export default defineConfig({
  base,
  plugins: [react()],
  build: { target: 'es2022', emptyOutDir: true },
  /*
   * O limite padrão do Vitest é de 5 segundos, pensado para testes de unidade.
   * Boa parte desta suíte joga batalhas de verdade — mil jornadas, as 52
   * conquistas verificadas jogando, a direção de apresentação quadro a quadro
   * — e várias passam de 3 segundos nesta máquina.
   *
   * Num runner mais lento isso vira falha de tempo, e foi o que derrubou um
   * deploy: o teste que prova que toda conquista é alcançável rodou em 2,8 s
   * aqui e estourou os 5 s no CI. Cortar cenários resolveria o relógio e
   * estragaria a cobertura, que é justamente o ponto desses testes.
   */
  test: { testTimeout: 30000 },
});
