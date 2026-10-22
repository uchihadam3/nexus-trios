import { Languages } from 'lucide-react';
import { IDIOMA, INGLES_LIBERADO, trocarIdioma, type Idioma } from '../i18n/idioma';

/* Português ou English (nos Ajustes e na tela de login). Os nomes ficam sempre no próprio idioma, para quem não lê o outro. */
const OPCOES: readonly (readonly [Idioma, string, string])[] = [['pt', 'Português', 'BR'], ['en', 'English', 'EN']];

export function TrocaDeIdioma({ compacta = false }: { compacta?: boolean }) {
  if (!INGLES_LIBERADO && IDIOMA !== 'en') return null;
  return <div className={`troca-idioma ${compacta ? 'compacta' : ''}`} role="group" aria-label="Idioma / Language">
    <Languages size={16} aria-hidden />
    {OPCOES.map(([id, nome, sigla]) => <button key={id} type="button" className={IDIOMA === id ? 'ativo' : ''} aria-pressed={IDIOMA === id}
      onClick={() => { if (IDIOMA !== id) trocarIdioma(id); }}><b>{sigla}</b>{!compacta && <span>{nome}</span>}</button>)}
  </div>;
}
