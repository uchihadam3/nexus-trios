"""Os sons da rodada 19: Ganondorf, Samus Aran, Dante, Vergil e Bayonetta (veja
tools/vfx/familias_v2/rodada19.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada14 import _trovao
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _coro_sombrio(n, f, g=0.05):
    """O acorde grave e menor do rei das trevas, pulsando devagar."""
    t = _t(n)
    return (seno(f, n) + seno(f * 1.19, n) * 0.7 + seno(f * 1.5, n) * 0.5 + seno(f * 0.5, n) * 0.6) * (0.75 + 0.25 * np.sin(2 * math.pi * 1.8 * t)) * g


def _tiro(rng, g=0.5):
    """O tiro de pistola: o estampido seco com o estalo agudo."""
    n = n_de(0.18)
    return (satura(baque(n, 220, 90, 0.03, 1.0), 2.5) * 0.6 + estalo(rng, n, 2000, 9000, 0.008) * 0.7) * g


def _corte_fino(rng, seg=0.18, g=0.3):
    """O corte de katana: o assobio curtíssimo e muito agudo."""
    n = n_de(seg)
    return passa(rosa(rng, n), 4000, 14000, 2) * sobe_e_some(n, 0.25, 3.0) * g


# =================================================================== Ganondorf
def poder_da_triade(rng, v):
    """O poder da Tríade: o acorde dourado do triângulo, a sombra descendo grave e o escudo fechando."""
    x = _z(1.8)
    m = n_de(0.9)
    poe(x, (seno(330, m) + seno(415, m) * 0.7 + seno(494, m) * 0.5) * env(m, 0.02, 0.5) * 0.05, 0.0)
    poe(x, modal(n_de(0.6), 988, rng=rng, **SINO) * env(n_de(0.6), 0.002, 0.3) * 0.08, 0.05)
    n = n_de(0.5)
    poe(x, seno(varre(220, 70, n, 1.2), n) * sobe_e_some(n, 0.5, 1.5) * 0.18, 0.2)
    poe(x, passa(rosa(rng, n), 60, 400, 2) * sobe_e_some(n, 0.5, 1.5) * 0.3, 0.2)
    poe(x, satura(baque(n_de(0.35), 90, 45, 0.1, 0.5), 1.5) * 0.4, 0.5)
    poe(x, modal(n_de(0.8), 523, rng=rng, **METAL) * env(n_de(0.8), 0.002, 0.4) * 0.07, 0.55)
    return reverb(x, 0.7, 0.35)


def ganondorf_preparo(rng, v):
    """O Preparo do Juízo do Rei: o coro sombrio crescendo e as faíscas de trevas estalando no punho."""
    x = _z(1.6)
    n = n_de(1.4)
    poe(x, _coro_sombrio(n, 98, 0.05) * sobe_e_some(n, 0.8, 1.2), 0.0)
    poe(x, graos(rng, n, 30, 0.1, 1.3, 2000, 7000, 0.004) * 0.25, 0.0)
    poe(x, passa(rosa(rng, n), 40, 200, 2) * sobe_e_some(n, 0.85, 1.4) * 0.25, 0.0)
    return reverb(x, 0.7, 0.35)


def juizo_do_rei(rng, v):
    """O juízo do rei: as três colunas de trevas caindo (três trovões graves em sequência) e o selo que cala (o
    gongo abafado)."""
    x = _z(2.2)
    for k in range(3):
        poe(x, _trovao(rng, 1.0, 0.6), 0.05 + 0.08 * k)
        poe(x, satura(baque(n_de(0.5), 60, 28, 0.2, 1.0), 1.8) * 0.45, 0.2 + 0.08 * k)
    n = n_de(1.0)
    poe(x, _coro_sombrio(n, 73, 0.05) * env(n, 0.02, 0.6), 0.25)
    poe(x, modal(n_de(1.0), 180, rng=rng, **METAL) * env(n_de(1.0), 0.003, 0.4) * 0.12, 0.7)
    return reverb(x, 0.8, 0.35)


# =================================================================== Samus
def trava_de_mira(rng, v):
    """A trava de mira: os bipes do visor apertando o passo e o tom de trava no fim."""
    x = _z(1.2)
    for k, t0 in enumerate((0.0, 0.12, 0.22, 0.3, 0.36, 0.41)):
        m = n_de(0.05)
        poe(x, seno(1600 + 80 * k, m) * env(m, 0.002, 0.03) * 0.06, t0)
    m = n_de(0.35)
    poe(x, (seno(2100, m) + seno(3150, m) * 0.4) * env(m, 0.003, 0.25) * 0.07, 0.5)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 2000, 8000, 2) * sobe_e_some(n, 0.5, 2.0) * 0.06, 0.3)
    return reverb(x, 0.3, 0.15)


def missil_de_contencao(rng, v):
    """O míssil de contenção: o disparo, o chiado do foguete cruzando, a explosão e o zumbido do campo lento."""
    x = _z(1.8)
    poe(x, satura(baque(n_de(0.25), 160, 70, 0.06, 0.8), 2.0) * 0.4, 0.0)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * sobe_e_some(n, 0.8, 1.2) * 0.3, 0.02)
    m = n_de(0.7)
    poe(x, satura(passa(rosa(rng, m), 40, 3000, 2) * env(m, 0.002, 0.35), 2.0) * 0.7, 0.3)
    poe(x, satura(baque(n_de(0.5), 70, 30, 0.18, 1.0), 2.0) * 0.6, 0.3)
    k = n_de(0.8)
    poe(x, seno(varre(500, 300, k, 1.0), k) * env(k, 0.05, 0.5) * 0.05, 0.6)
    return reverb(x, 0.5, 0.25)


def samus_preparo(rng, v):
    """O Preparo do Charge Beam: o canhão carregando — o zumbido que sobe e o brilho que pulsa."""
    x = _z(1.6)
    n = n_de(1.4)
    t = _t(n)
    poe(x, seno(varre(180, 720, n, 0.8), n) * (0.7 + 0.3 * np.sin(2 * math.pi * 14 * t)) * sobe_e_some(n, 0.9, 1.0) * 0.08, 0.0)
    poe(x, graos(rng, n, 25, 0.0, 1.3, 3000, 9000, 0.003) * 0.15, 0.0)
    return reverb(x, 0.4, 0.2)


def charge_beam(rng, v):
    """O Charge Beam: o disparo pesado da bola carregada, o rugido do tiro cruzando e o impacto com a onda."""
    x = _z(1.8)
    poe(x, satura(baque(n_de(0.3), 140, 50, 0.1, 1.0), 2.2) * 0.6, 0.0)
    n = n_de(0.3)
    poe(x, (seno(varre(900, 400, n, 1.0), n) * 0.1 + passa(rosa(rng, n), 300, 4000, 2) * 0.3) * sobe_e_some(n, 0.6, 1.2), 0.02)
    m = n_de(0.9)
    poe(x, satura(passa(rosa(rng, m), 30, 2500, 2) * env(m, 0.002, 0.45), 2.2) * 0.75, 0.28)
    poe(x, satura(baque(n_de(0.6), 55, 25, 0.25, 1.0), 2.0) * 0.6, 0.28)
    poe(x, _brilho(rng, 0.6, 1320, 0.05, CRISTAL), 0.3)
    return reverb(x, 0.6, 0.3)


# =================================================================== Dante
def ebony_e_ivory(rng, v):
    """Ebony e Ivory: a saraivada das duas pistolas alternando, os ricochetes e o estalo final."""
    x = _z(1.4)
    for k in range(14):
        poe(x, _tiro(rng, 0.38 if k % 2 == 0 else 0.33), 0.03 + 0.045 * k)
    for k in range(4):
        m = n_de(0.25)
        poe(x, seno(varre(3200, 1800, m, 1.0), m) * env(m, 0.002, 0.15) * 0.025, 0.2 + 0.12 * k)
    return reverb(x, 0.4, 0.2)


def dante_preparo(rng, v):
    """O Preparo do Devil Trigger: a eletricidade vermelha estalando e o rosnado grave de demônio crescendo."""
    x = _z(1.6)
    n = n_de(1.4)
    t = _t(n)
    poe(x, satura(seno(varre(55, 75, n, 1.0), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 9 * t)), 2.5) * sobe_e_some(n, 0.85, 1.2) * 0.12, 0.0)
    poe(x, graos(rng, n, 35, 0.0, 1.3, 2500, 9000, 0.003) * 0.3, 0.0)
    return reverb(x, 0.6, 0.3)


def devil_trigger(rng, v):
    """O Devil Trigger: o rugido da transformação (as asas abrindo), o Stinger atravessando e a explosão."""
    x = _z(2.0)
    n = n_de(0.5)
    poe(x, satura(seno(varre(70, 140, n, 1.0), n), 3.0) * sobe_e_some(n, 0.6, 1.2) * 0.2, 0.0)
    poe(x, passa(rosa(rng, n), 200, 2000, 2) * sobe_e_some(n, 0.6, 1.2) * 0.3, 0.0)
    poe(x, _whoosh(rng, 0.25, 400, 3000, 0.8, 1.3, 0.4), 0.22)
    poe(x, modal(n_de(0.4), 1400, rng=rng, **METAL) * env(n_de(0.4), 0.001, 0.15) * 0.15, 0.42)
    m = n_de(0.8)
    poe(x, satura(passa(rosa(rng, m), 40, 3000, 2) * env(m, 0.002, 0.4), 2.0) * 0.7, 0.44)
    poe(x, satura(baque(n_de(0.5), 65, 28, 0.2, 1.0), 2.0) * 0.55, 0.44)
    return reverb(x, 0.6, 0.3)


# =================================================================== Vergil
def yamato(rng, v):
    """A Yamato: o clique da bainha, o silêncio, a chuva de cortes finos e as espadas espectrais cravando."""
    x = _z(1.6)
    poe(x, modal(n_de(0.15), 2600, rng=rng, **METAL) * env(n_de(0.15), 0.0005, 0.04) * 0.15, 0.0)
    for k in range(6):
        poe(x, _corte_fino(rng, 0.15, 0.28), 0.15 + 0.05 * k)
    for k in range(5):
        poe(x, _brilho(rng, 0.4, 1760 * (1.12 ** k), 0.04, VIDRO), 0.48 + 0.03 * k)
    return reverb(x, 0.5, 0.25)


def vergil_preparo(rng, v):
    """O Preparo do Judgement Cut End: a lâmina saindo devagar da bainha (o raspar metálico) e o zumbido frio das
    espadas espectrais."""
    x = _z(1.6)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.7, 1.5) * 0.1, 0.0)
    poe(x, modal(n_de(1.0), 1480, rng=rng, **METAL) * env(n_de(1.0), 0.05, 0.6) * 0.04, 0.0)
    m = n_de(1.3)
    poe(x, (seno(880, m) + seno(1320, m) * 0.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * _t(m))) * sobe_e_some(m, 0.7, 1.2) * 0.025, 0.1)
    return reverb(x, 0.6, 0.3)


def judgement_cut_end(rng, v):
    """O Judgement Cut End: o silêncio, dezenas de cortes de uma vez e o espaço se quebrando como vidro."""
    x = _z(2.0)
    for k in range(16):
        poe(x, _corte_fino(rng, 0.12, 0.18), 0.02 + 0.015 * k)
    m = n_de(1.0)
    poe(x, modal(m, 1600, rng=rng, **VIDRO) * env(m, 0.0005, 0.4) * 0.25, 0.45)
    poe(x, graos(rng, n_de(0.9), 60, 0.0, 0.8, 2500, 11000, 0.006) * 0.45, 0.45)
    poe(x, satura(baque(n_de(0.5), 80, 35, 0.15, 0.8), 1.6) * 0.45, 0.45)
    return reverb(x, 0.7, 0.35)


# =================================================================== Bayonetta
def danca_da_bruxa(rng, v):
    """A dança da bruxa: três chutes em giro (o vento e o baque), os tiros dos saltos e o farfalhar das
    borboletas."""
    x = _z(1.5)
    for k in range(3):
        poe(x, _whoosh(rng, 0.2, 400, 2500, 0.6, 1.3, 0.35), 0.0 + 0.13 * k)
        poe(x, satura(baque(n_de(0.2), 130, 70, 0.05, 0.6), 1.6) * 0.35, 0.15 + 0.13 * k)
        poe(x, _tiro(rng, 0.18), 0.17 + 0.13 * k)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * (0.4 + 0.6 * np.abs(np.sin(2 * math.pi * 8 * _t(n)))) * sobe_e_some(n, 0.3, 1.2) * 0.08, 0.4)
    return reverb(x, 0.5, 0.25)


def witch_time(rng, v):
    """O Witch Time: o tique-taque do relógio que vai desacelerando e o "vuum" grave de tempo lento passando."""
    x = _z(2.0)
    t0, passo = 0.0, 0.06
    for k in range(9):
        poe(x, modal(n_de(0.12), 2400 if k % 2 == 0 else 2000, rng=rng, **METAL) * env(n_de(0.12), 0.0005, 0.03) * 0.09, t0)
        t0 += passo
        passo *= 1.25
    n = n_de(1.0)
    poe(x, seno(varre(400, 120, n, 1.2), n) * sobe_e_some(n, 0.3, 1.5) * 0.1, 0.3)
    poe(x, passa(rosa(rng, n), 100, 900, 2) * sobe_e_some(n, 0.3, 1.5) * 0.2, 0.3)
    return reverb(x, 0.8, 0.4)


SONS: dict = {
    "poder-da-triade": (poder_da_triade, "Ganondorf: o acorde da Força, a sombra e o escudo"),
    "ganondorf-preparo": (ganondorf_preparo, "Ganondorf: o coro sombrio no punho (antes do golpe)"),
    "juizo-do-rei": (juizo_do_rei, "Ganondorf: as três colunas de trevas e o gongo"),
    "trava-de-mira": (trava_de_mira, "Samus: os bipes do visor e a trava"),
    "missil-de-contencao": (missil_de_contencao, "Samus: o míssil e a explosão"),
    "samus-preparo": (samus_preparo, "Samus: o canhão carregando (antes do golpe)"),
    "charge-beam": (charge_beam, "Samus: o tiro carregado e o impacto"),
    "ebony-e-ivory": (ebony_e_ivory, "Dante: a saraivada das duas pistolas"),
    "dante-preparo": (dante_preparo, "Dante: a eletricidade e o rosnado (antes do golpe)"),
    "devil-trigger": (devil_trigger, "Dante: o rugido, o Stinger e a explosão"),
    "yamato": (yamato, "Vergil: o clique da bainha e os cortes"),
    "vergil-preparo": (vergil_preparo, "Vergil: a lâmina saindo da bainha (antes do golpe)"),
    "judgement-cut-end": (judgement_cut_end, "Vergil: os cortes e o vidro se partindo"),
    "danca-da-bruxa": (danca_da_bruxa, "Bayonetta: os chutes, os tiros e as borboletas"),
    "witch-time": (witch_time, "Bayonetta: o relógio desacelerando"),
}
