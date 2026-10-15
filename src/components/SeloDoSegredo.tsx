import type { LucideIcon } from 'lucide-react';
import { Globe, HeartPulse, ShieldCheck, Target, TrendingUp, Zap } from 'lucide-react';
import type { SegredoId, QualLuta } from '../engine/segredos';

/* O ícone de cada segredo (src/engine/segredos.ts), o mesmo no Livro, no aviso de descoberta e na trilha. */
export const ICONE_DO_SEGREDO: Record<SegredoId, LucideIcon> = {
  'sem-baixas': ShieldCheck,
  classico: Globe,
  intacto: HeartPulse,
  virada: TrendingUp,
  relampago: Zap,
  davi: Target,
};
/** O que o segredo libera, curto: para os selos. */
export const NOME_DA_LUTA: Record<QualLuta, string> = { estrela: 'Luta ★', onze: 'Luta 11' };
export const ONDE_FICA: Record<QualLuta, string> = { estrela: 'entre a 5 e a 6', onze: 'depois da 10' };
