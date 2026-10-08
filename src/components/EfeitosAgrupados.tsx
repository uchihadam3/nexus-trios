/*
 * Os efeitos de uma habilidade, desenhados por alvo.
 *
 * Um componente só, para a ficha completa e o inspetor da batalha. Antes
 * cada tela desenhava a lista do seu jeito, e foi assim que as duas chegaram
 * a mostrar a mesma habilidade com textos diferentes.
 *
 * O desenho dá peso a cada peça da linha em vez de tratar a frase inteira no
 * mesmo tom: o nome (Status ou efeito) forte, o que ele faz normal, como
 * acumula e quanto dura discretos. É a diferença entre ler e escanear.
 */
import type { GrupoDeEfeitos } from '../engine/skill-descriptions';
import { ComTermos } from './Termos';

/* "12 s", "7,5 s". É a duração, e vai para a direita, como etiqueta. */
const ehDuracao = (t: string): boolean => /^\d[\d.,]* s$/.test(t);
const ehAcumulo = (t: string): boolean => t.startsWith('soma ');

export function EfeitosAgrupados({ grupos }: { grupos: GrupoDeEfeitos[] }) {
  return <div className="efeitos-agrupados">
    {grupos.map((grupo, i) => <section key={i} className="grupo-efeitos">
      {grupo.titulo && <h4 className="grupo-alvo">{grupo.titulo}</h4>}
      <ul>
        {grupo.linhas.map((linha, j) => {
          const [nome, ...resto] = linha.partes;
          const duracao = resto.length > 0 && ehDuracao(resto[resto.length - 1]) ? resto[resto.length - 1] : null;
          const meio = duracao ? resto.slice(0, -1) : resto;
          return <li key={j}>
            <span className="efeito-corpo">
              <b><ComTermos texto={nome}/></b>
              {meio.map((parte, k) => <span key={k} className={ehAcumulo(parte) ? 'efeito-acumulo' : 'efeito-detalhe'}><ComTermos texto={parte}/></span>)}
            </span>
            {duracao && <span className="efeito-duracao">{duracao}</span>}
          </li>;
        })}
      </ul>
    </section>)}
  </div>;
}
