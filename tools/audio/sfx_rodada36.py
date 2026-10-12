"""Os sons da rodada 36 das habilidades próprias (veja tools/vfx/familias_v2/rodada36.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _estrelinhas(rng, x, em, n=3):
    for k in range(n):
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.02, CRISTAL), em + 0.07 * k)


def _ronco(rng, seg, f0=120, f1=90, g=0.06):
    """O ronco de porco/javali (o grunhido rouco)."""
    n = n_de(seg)
    t = _t(n)
    return satura(seno(varre(f0, f1, n), n) * (0.5 + 0.5 * np.sin(2 * math.pi * 30 * t)) + passa(rosa(rng, n), 100, 1500, 2) * 0.6, 4) * env(n, 0.02, seg * 0.7) * g


def _risada_ma(rng, seg=0.8, f=180, g=0.05):
    """A risada malvada ("nhá-há-há"): os pulsos graves que descem."""
    x = _z(seg + 0.2)
    for k in range(5):
        n = n_de(0.12)
        poe(x, satura(seno(varre(f * (1.2 - 0.06 * k), f * (1.0 - 0.06 * k), n), n) + 0.3 * seno(f * 3, n), 3) * env(n, 0.01, 0.1) * g, 0.14 * k)
    return x


# ------------------------------------------------------------------ Bebop

def investida_de_javali(rng, v):
    """Bebop: o ronco, os cascos correndo e o tranco."""
    x = _z(1.9)
    poe(x, _ronco(rng, 0.3), 0.0)
    for k in range(6):
        poe(x, _baque(160 + 20 * (k % 2), 90, 0.06, 0.25), 0.05 + 0.04 * k)
    poe(x, _baque(80, 30, 0.6, 0.9, 2.8), 0.3)
    poe(x, estalo(rng, n_de(0.05), 500, 3000, 0.012), 0.3)
    return reverb(x, 0.5, 0.25)


def pancada_do_bebop(rng, v):
    """Bebop: o soco pesado e as placas de metal encaixando no corpo."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.25, 200, 2500, 0.85, 1.3, 0.5), 0.0)
    poe(x, _baque(80, 30, 0.6, 0.9, 2.8), 0.22)
    for k in range(6):
        poe(x, _sino(rng, 660 + 80 * k, 0.25, 0.025, METAL), 0.4 + 0.04 * k)
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.004) * 0.5, 0.4 + 0.04 * k)
    return reverb(x, 0.5, 0.25)


def bebop_preparo(rng, v):
    """Bebop (Preparo): o bufo pelo nariz e as patadas no chão."""
    x = _z(1.4)
    for k in range(2):
        poe(x, passa(rosa(rng, n_de(0.2)), 300, 3000, 2) * env(n_de(0.2), 0.01, 0.15) * 0.3, 0.5 * k)
        poe(x, _baque(110, 50, 0.15, 0.4), 0.25 + 0.5 * k)
    poe(x, _ronco(rng, 0.25, 110, 90, 0.04), 0.1)
    return reverb(x, 0.4, 0.2)


def atropelo(rng, v):
    """Bebop: a manada de pisadas atravessando todos e o chão tremendo."""
    x = _z(2.2)
    for k in range(14):
        poe(x, _baque(100 + 15 * (k % 3), 45, 0.12, 0.45, 2.4), 0.05 * k)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 60, 600, 2) * sobe_e_some(n, 0.4, 1.2) * 0.5, 0.0)
    poe(x, _ronco(rng, 0.4, 130, 90, 0.05), 0.2)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Esqueleto

def maldicao_do_esqueleto(rng, v):
    """Esqueleto: a risada malvada, a caveira de fumaça e as correntes de runas."""
    x = _z(2.1)
    poe(x, _risada_ma(rng, 0.8, 200, 0.045), 0.0)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * sobe_e_some(n, 0.3, 1.2) * 0.25, 0.1)
    for k in range(5):
        poe(x, _sino(rng, 300 + 50 * k, 0.3, 0.02, METAL), 0.4 + 0.07 * k)
    return reverb(x, 0.7, 0.35)


def esqueleto_preparo(rng, v):
    """Esqueleto (Preparo): o Cajado da Caveira zumbindo (o acorde sombrio pulsando)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(73, n) + seno(110, n) * 0.5 + seno(156, n) * 0.4) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.05, 0.0)
    poe(x, graos(rng, n, 15, 0.0, 0.95, 1500, 5000, 0.003) * 0.25, 0.0)
    return reverb(x, 0.7, 0.35)


def dominio_de_snake_mountain(rng, v):
    """Esqueleto: a montanha da serpente (o sibilo da cobra) e os raios caindo em todos."""
    x = _z(2.4)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 4000, 10000, 2) * env(n, 0.05, 0.4) * 0.25, 0.0)
    poe(x, _acorde((55, 82, 104), 1.0, 0.05, 0.1, 0.8), 0.0)
    for k in range(3):
        poe(x, _trovao(rng, 0.5, 0.4), 0.38 + 0.08 * k)
    poe(x, _risada_ma(rng, 0.8, 160, 0.04), 0.8)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ She-Ra

def espada_protetora(rng, v):
    """She-Ra: a Espada da Proteção brilhando e o corte dourado."""
    x = _z(1.9)
    poe(x, _brilho(rng, 0.4, 1568, 0.035, CRISTAL), 0.0)
    poe(x, _whoosh(rng, 0.2, 1500, 9000, 0.8, 1.3, 0.5), 0.3)
    poe(x, _sino(rng, 1319, 0.6, 0.05, METAL), 0.4)
    poe(x, _baque(140, 60, 0.25, 0.5), 0.42)
    return reverb(x, 0.6, 0.3)


def pela_honra_de_grayskull(rng, v):
    """She-Ra: "Pela honra de Grayskull!" — o coro luminoso e o escudo no trio."""
    x = _z(2.4)
    poe(x, _acorde((262, 330, 392, 523, 659), 1.4, 0.04, 0.15, 1.0), 0.0)
    poe(x, graos(rng, n_de(1.0), 40, 0.0, 0.9, 3000, 9000, 0.003) * 0.3, 0.1)
    poe(x, _sino(rng, 1047, 1.0, 0.04, SINO), 0.4)
    poe(x, _brilho(rng, 0.8, 2093, 0.03, CRISTAL), 0.45)
    return reverb(x, 0.9, 0.45)


def shera_preparo(rng, v):
    """She-Ra (Preparo): a espada no alto e as faíscas girando (o brilho em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, (seno(784, n) + seno(1175, n) * 0.5) * sobe_e_some(n, 0.7, 1.2) * 0.02, 0.0)
    poe(x, graos(rng, n, 30, 0.0, 0.95, 3000, 10000, 0.003) * 0.3, 0.0)
    return reverb(x, 0.6, 0.3)


def golpe_da_princesa(rng, v):
    """She-Ra: o voo com as asas (o bater e o vento) e o chute."""
    x = _z(2.0)
    for k in range(2):
        poe(x, _sopro(rng, 0.2, 300, 2500, 0.2, 0.3), 0.12 * k)
    poe(x, _whoosh(rng, 0.3, 400, 5000, 0.85, 1.4, 0.5), 0.05)
    poe(x, _baque(100, 40, 0.5, 0.9, 2.6), 0.33)
    poe(x, _brilho(rng, 0.5, 1568, 0.03, CRISTAL), 0.38)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Lion-O

def visao_alem_do_alcance(rng, v):
    """Lion-O: "Espada de Augúrio, dá-me visão além do alcance!" — o olho acendendo e o feixe."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, seno(varre(300, 1200, n), n) * env(n, 0.25, 0.04) * 0.04, 0.0)
    poe(x, _acorde((220, 277, 330), 0.6, 0.03, 0.05, 0.5), 0.0)
    n = n_de(0.45)
    poe(x, satura(seno(varre(1000, 700, n), n), 2) * env(n, 0.01, 0.4) * 0.04, 0.25)
    poe(x, _baque(130, 55, 0.3, 0.6), 0.3)
    return reverb(x, 0.6, 0.3)


def liono_preparo(rng, v):
    """Lion-O (Preparo): a espada crescendo (o tom que sobe) e o rugido baixo."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, seno(varre(200, 500, n), n) * sobe_e_some(n, 0.8, 1.2) * 0.03, 0.0)
    poe(x, satura(passa(rosa(rng, n), 80, 600, 2), 2) * sobe_e_some(n, 0.6, 1.2) * 0.2, 0.0)
    return reverb(x, 0.6, 0.3)


def thunder_thunder(rng, v):
    """Lion-O: "Thunder, Thunder, ThunderCats, HOOO!" — a fanfarra, os raios e o golpe."""
    x = _z(2.4)
    for k, f in enumerate((262, 262, 392, 523)):
        n = n_de(0.12 if k < 3 else 0.4)
        poe(x, satura(seno(f, n) + seno(f * 1.5, n) * 0.4, 2) * env(n, 0.01, 0.1 if k < 3 else 0.35) * 0.045, 0.1 * k)
    for k in range(3):
        poe(x, _trovao(rng, 0.4, 0.4), 0.3 + 0.06 * k)
    poe(x, _baque(55, 22, 0.9, 1.0, 3.2), 0.42)
    poe(x, _explosao(rng, 0.8, 55), 0.42)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Cheetara

def bastao_giratorio(rng, v):
    """Cheetara: o bastão girando ("vuvuvu") e as batidas."""
    x = _z(1.9)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 16 * _t(n)) ** 2) * env(n, 0.02, 0.4) * 0.3, 0.0)
    for k in range(4):
        poe(x, _baque(200, 110, 0.08, 0.35), 0.25 + 0.1 * k)
        poe(x, estalo(rng, n_de(0.03), 1200, 5000, 0.006) * 0.6, 0.25 + 0.1 * k)
    return reverb(x, 0.4, 0.2)


def corrida_felina(rng, v):
    """Cheetara: a corrida em supervelocidade (o "zuuum") passando por todos."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.45, 800, 10000, 0.6, 1.4, 0.6), 0.0)
    for k in range(3):
        poe(x, _baque(150, 70, 0.15, 0.35), 0.12 + 0.1 * k)
    poe(x, passa(rosa(rng, n_de(0.5)), 200, 2000, 2) * env(n_de(0.5), 0.05, 0.4) * 0.2, 0.3)
    return reverb(x, 0.4, 0.2)


def cheetara_preparo(rng, v):
    """Cheetara (Preparo): o bastão estendendo (o "clique-clique") e o foco."""
    x = _z(1.4)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.02), 1500, 6000, 0.004) * 0.6, 0.05 + 0.08 * k)
    n = n_de(0.9)
    poe(x, seno(1400, n) * sobe_e_some(n, 0.6, 1.0) * 0.01, 0.2)
    return reverb(x, 0.5, 0.25)


def golpe_certeiro_cheetara(rng, v):
    """Cheetara: a estocada num instante e o "TOC" certeiro."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.15, 2000, 10000, 0.8, 1.3, 0.5), 0.0)
    poe(x, _baque(300, 160, 0.08, 0.5), 0.18)
    poe(x, estalo(rng, n_de(0.04), 1500, 6000, 0.008) * 1.2, 0.18)
    poe(x, _sino(rng, 2349, 0.5, 0.03, CRISTAL), 0.2)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Homer

def barriga_de_aco(rng, v):
    """Homer: a barrigada ("BLOMP") e a energia guardando (o tom que sobe)."""
    x = _z(1.9)
    n = n_de(0.3)
    poe(x, seno(varre(90, 60, n), n) * env(n, 0.01, 0.25) * 0.12, 0.2)
    poe(x, _baque(100, 50, 0.3, 0.7, 2.2), 0.22)
    n = n_de(0.4)
    poe(x, seno(varre(300, 900, n), n) * env(n, 0.05, 0.1) * 0.03, 0.5)
    return reverb(x, 0.4, 0.2)


def rosquinha(rng, v):
    """Homer: "Hmmm... rosquinha" (o "hmmm" grave), a mordida e a vida voltando."""
    x = _z(2.1)
    n = n_de(0.6)
    t = _t(n)
    poe(x, satura(seno(140 + 10 * np.sin(2 * math.pi * 4 * t), n), 2) * env(n, 0.08, 0.3) * 0.04, 0.0)
    poe(x, estalo(rng, n_de(0.05), 600, 3000, 0.01), 0.4)
    poe(x, _baque(220, 140, 0.06, 0.25), 0.4)
    poe(x, _acorde((392, 494, 587), 0.8, 0.03, 0.05, 0.6), 0.55)
    return reverb(x, 0.5, 0.25)


def homer_preparo(rng, v):
    """Homer (Preparo): a energia pulsando e o resmungo bravo."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(220, n) * (0.5 + 0.5 * np.sin(2 * math.pi * 2 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.03, 0.0)
    for k in range(2):
        poe(x, passa(rosa(rng, n_de(0.2)), 2000, 7000, 2) * env(n_de(0.2), 0.01, 0.15) * 0.15, 0.3 + 0.4 * k)
    return reverb(x, 0.4, 0.2)


def d_oh(rng, v):
    """Homer: "D'oh!" (o grito curto e grave) e a energia solta no rival."""
    x = _z(2.2)
    n = n_de(0.25)
    poe(x, satura(seno(varre(260, 180, n), n) + 0.4 * seno(varre(520, 360, n), n), 3) * env(n, 0.01, 0.2) * 0.06, 0.0)
    poe(x, _whoosh(rng, 0.25, 300, 4000, 0.8, 1.4, 0.5), 0.3)
    poe(x, _baque(60, 25, 0.9, 1.0, 3.0), 0.5)
    poe(x, _explosao(rng, 0.8, 60), 0.5)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Bart

def provocacao_do_bart(rng, v):
    """Bart: o spray pichando ("pssst") e a risada de moleque."""
    x = _z(2.0)
    for k in range(4):
        n = n_de(0.12)
        poe(x, passa(rosa(rng, n), 4000, 11000, 2) * env(n, 0.005, 0.1) * 0.25, 0.08 + 0.12 * k)
    for k in range(3):
        n = n_de(0.08)
        poe(x, satura(seno(varre(700, 600, n), n), 2) * env(n, 0.005, 0.07) * 0.035, 0.65 + 0.1 * k)
    return reverb(x, 0.4, 0.2)


def travessura_maxima(rng, v):
    """Bart: as bombinhas estourando em fila e a explosão final."""
    x = _z(2.2)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.04), 800, 6000, 0.008) * 1.2, 0.15 + 0.06 * k)
        poe(x, _baque(300, 180, 0.05, 0.3), 0.15 + 0.06 * k)
    poe(x, _baque(60, 25, 0.8, 1.0, 3.0), 0.5)
    poe(x, _explosao(rng, 0.9, 60), 0.5)
    _estrelinhas(rng, x, 0.8)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "investida-de-javali": (investida_de_javali, "Bebop: a investida de javali"),
    "pancada-do-bebop": (pancada_do_bebop, "Bebop: a pancada"),
    "bebop-preparo": (bebop_preparo, "Bebop: o bufo (Preparo)"),
    "atropelo": (atropelo, "Bebop: o atropelo"),
    "maldicao-do-esqueleto": (maldicao_do_esqueleto, "Esqueleto: a maldição"),
    "esqueleto-preparo": (esqueleto_preparo, "Esqueleto: o Cajado da Caveira (Preparo)"),
    "dominio-de-snake-mountain": (dominio_de_snake_mountain, "Esqueleto: o Domínio de Snake Mountain"),
    "espada-protetora": (espada_protetora, "She-Ra: a Espada Protetora"),
    "pela-honra-de-grayskull": (pela_honra_de_grayskull, "She-Ra: Pela honra de Grayskull"),
    "shera-preparo": (shera_preparo, "She-Ra: a espada no alto (Preparo)"),
    "golpe-da-princesa": (golpe_da_princesa, "She-Ra: o golpe da Princesa"),
    "visao-alem-do-alcance": (visao_alem_do_alcance, "Lion-O: Visão além do alcance"),
    "liono-preparo": (liono_preparo, "Lion-O: a espada crescendo (Preparo)"),
    "thunder-thunder": (thunder_thunder, "Lion-O: Thunder, Thunder!"),
    "bastao-giratorio": (bastao_giratorio, "Cheetara: o bastão giratório"),
    "corrida-felina": (corrida_felina, "Cheetara: a corrida felina"),
    "cheetara-preparo": (cheetara_preparo, "Cheetara: o bastão estendido (Preparo)"),
    "golpe-certeiro-cheetara": (golpe_certeiro_cheetara, "Cheetara: o golpe certeiro"),
    "barriga-de-aco": (barriga_de_aco, "Homer: a barriga de aço"),
    "rosquinha": (rosquinha, "Homer: a rosquinha"),
    "homer-preparo": (homer_preparo, "Homer: a energia pulsando (Preparo)"),
    "d-oh": (d_oh, "Homer: D'oh!"),
    "provocacao-do-bart": (provocacao_do_bart, "Bart: a provocação"),
    "travessura-maxima": (travessura_maxima, "Bart: a travessura máxima"),
}
