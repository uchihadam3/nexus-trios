"""Os sons da rodada 51 das habilidades próprias (veja tools/vfx/familias_v2/rodada51.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _rasgo(rng, seg=0.09, g=0.3):
    n = n_de(seg)
    return satura(passa(rosa(rng, n), 1200, 9000, 2), 2) * env(n, 0.004, seg * 0.85) * g


def _riso(rng, f0, n_ha, passo, g=0.025):
    """A risada ("ha-ha-ha") com a voz rouca."""
    x = _z(n_ha * passo + 0.3)
    for k in range(n_ha):
        n = n_de(passo * 0.8)
        f = f0 * (1 - 0.04 * k)
        poe(x, satura(seno(varre(f * 1.1, f, n), n) + passa(rosa(rng, n), 300, 2500, 2) * 0.5, 3) * env(n, 0.01, passo * 0.6) * g, k * passo)
    return x


def _motor(rng, seg, f0=45, f1=70, g=0.06):
    """O motor da motosserra (o ronco de dois tempos)."""
    n = n_de(seg)
    t = _t(n)
    f = f0 + (f1 - f0) * np.clip(t / max(seg * 0.4, 1e-3), 0, 1)
    ph = 2 * math.pi * np.cumsum(f) / 44100
    pulso_ = (np.sin(ph) > 0.3).astype(float)
    return satura(passa(rosa(rng, n), 100, 3000, 2) * pulso_ + seno(f * 2, n) * 0.3, 4) * sobe_e_some(n, 0.1, 1.2) * g


def _corrente(rng, n_elos, passo, g=0.012):
    x = _z(n_elos * passo + 0.3)
    q = np.random.default_rng(13)
    for k in range(n_elos):
        poe(x, _sino(rng, q.uniform(2200, 3200), 0.12, g, METAL), k * passo)
        poe(x, estalo(rng, n_de(0.01), 2000, 7000, 0.002) * 0.25, k * passo)
    return x


def _estatica(rng, seg, g=0.2):
    n = n_de(seg)
    return passa(rosa(rng, n), 500, 11000, 2) * sobe_e_some(n, 0.1, 1.2) * g


# ------------------------------------------------------------------ Chucky

def facada_do_chucky(rng, v):
    """Chucky: o pulinho do boneco e as três facadas rápidas."""
    x = _z(1.8)
    poe(x, _piu(400, 900, 0.12, 0.02), 0.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.1, 1500, 8000, 0.7, 1.3, 0.3), 0.2 + 0.09 * k)
        poe(x, _baque(170, 80, 0.12, 0.35), 0.26 + 0.09 * k)
        poe(x, _rasgo(rng, 0.08, 0.22), 0.26 + 0.09 * k)
    return reverb(x, 0.4, 0.2)


def risada_do_chucky(rng, v):
    """Chucky: a risada maníaca "HA HA HA" ecoando."""
    x = _z(2.2)
    poe(x, _riso(rng, 420, 6, 0.11, 0.03), 0.05)
    return reverb(x, 0.8, 0.4)


def chucky_preparo(rng, v):
    """Chucky (Preparo): o feitiço de vodu sussurrado e a vela tremendo (em laço)."""
    x = _z(1.4)
    for k in range(4):
        n = n_de(0.15)
        poe(x, passa(rosa(rng, n), 800, 4000, 2) * env(n, 0.03, 0.1) * 0.15, 0.25 * k)
    n2 = n_de(1.0)
    poe(x, (seno(110, n2) + seno(117, n2)) * sobe_e_some(n2, 0.5, 1.2) * 0.012, 0.0)
    return reverb(x, 0.8, 0.4)


def vodu(rng, v):
    """Chucky: o alfinete entrando no boneco ("tic") e a dor atravessando o rival."""
    x = _z(2.2)
    poe(x, _sino(rng, 2637, 0.3, 0.02, METAL), 0.3)
    poe(x, estalo(rng, n_de(0.02), 2000, 8000, 0.004) * 0.8, 0.3)
    n = n_de(0.3)
    poe(x, seno(varre(300, 900, n), n) * env(n, 0.02, 0.25) * 0.025, 0.35)
    poe(x, _baque(80, 30, 0.6, 0.9, 2.8), 0.47)
    poe(x, _riso(rng, 380, 3, 0.12, 0.02), 0.6)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Pennywise

def baloes_vermelhos(rng, v):
    """Pennywise: os balões flutuando (o rangido de borracha) e estourando ("POP")."""
    x = _z(2.2)
    for k in range(3):
        n = n_de(0.2)
        poe(x, seno(varre(600 + 100 * k, 900 + 100 * k, n), n) * env(n, 0.05, 0.15) * 0.008, 0.1 + 0.12 * k)
    for k in range(2):
        poe(x, estalo(rng, n_de(0.04), 500, 6000, 0.01) * 1.3, 0.68 + 0.08 * k)
        poe(x, _baque(200, 120, 0.08, 0.3), 0.68 + 0.08 * k)
    poe(x, _riso(rng, 300, 3, 0.13, 0.015), 0.9)
    return reverb(x, 0.8, 0.4)


def luzes_da_morte(rng, v):
    """Pennywise: as luzes girando na boca (o zumbido hipnótico) e o transe."""
    x = _z(2.4)
    n = n_de(1.2)
    t = _t(n)
    poe(x, (seno(220, n) + seno(222.5, n) + seno(330, n) * 0.5) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.02, 0.0)
    for k in range(3):
        poe(x, _sino(rng, 1480 + 120 * k, 0.4, 0.012, CRISTAL), 0.45 + 0.08 * k)
    return reverb(x, 0.9, 0.45)


def pennywise_preparo(rng, v):
    """Pennywise (Preparo): a melodia de circo desafinada (em laço)."""
    x = _z(1.4)
    for k, f in enumerate((523, 494, 523, 466)):
        poe(x, _sino(rng, f, 0.3, 0.015, SINO), 0.25 * k)
    n = n_de(1.0)
    poe(x, seno(98, n) * sobe_e_some(n, 0.5, 1.2) * 0.012, 0.0)
    return reverb(x, 0.7, 0.35)


def medo_puro(rng, v):
    """Pennywise: a boca abrindo (o rugido distorcido) e fechando no rival."""
    x = _z(2.3)
    n = n_de(0.5)
    poe(x, satura(seno(varre(200, 70, n), n) + passa(rosa(rng, n), 100, 2000, 2) * 1.0, 5) * env(n, 0.05, 0.35) * 0.06, 0.05)
    poe(x, estalo(rng, n_de(0.05), 600, 4000, 0.012) * 1.3, 0.46)
    poe(x, _baque(60, 22, 0.8, 1.0, 3.0), 0.46)
    poe(x, _explosao(rng, 0.4, 60), 0.46)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Ghostface

def ligacao_do_ghostface(rng, v):
    """Ghostface: o telefone tocando e a voz distorcida ("qual seu filme de terror favorito?")."""
    x = _z(2.2)
    for k in range(2):
        n = n_de(0.25)
        t = _t(n)
        poe(x, (seno(440, n) + seno(480, n)) * (np.sin(2 * math.pi * 20 * t) > 0) * env(n, 0.01, 0.05) * 0.015, 0.05 + 0.35 * k)
    n2 = n_de(0.6)
    poe(x, satura(seno(varre(90, 80, n2), n2) + passa(rosa(rng, n2), 200, 1500, 2) * 0.6, 4) * env(n2, 0.05, 0.4) * 0.04, 0.7)
    return reverb(x, 0.6, 0.3)


def facada_do_ghostface(rng, v):
    """Ghostface: o vulto surgindo atrás e a facada."""
    x = _z(1.9)
    poe(x, _sopro(rng, 0.25, 500, 3000, 0.18, 0.3), 0.0)
    poe(x, _whoosh(rng, 0.15, 1500, 9000, 0.7, 1.3, 0.4), 0.25)
    poe(x, _baque(110, 45, 0.35, 0.7, 2.5), 0.33)
    poe(x, _rasgo(rng, 0.12, 0.3), 0.33)
    return reverb(x, 0.6, 0.3)


def ghostface_preparo(rng, v):
    """Ghostface (Preparo): a respiração pela máscara e o manto (em laço)."""
    x = _z(1.4)
    for k in range(2):
        n = n_de(0.45)
        poe(x, passa(rosa(rng, n), 300, 1800, 2) * sobe_e_some(n, 0.5, 1.3) * 0.28, 0.6 * k)
    poe(x, _sopro(rng, 0.6, 200, 1500, 0.08, 0.5), 0.3)
    return reverb(x, 0.6, 0.3)


def grito_final(rng, v):
    """Ghostface: o grito da máscara e as facadas em sequência."""
    x = _z(2.3)
    n = n_de(0.5)
    poe(x, satura(seno(varre(700, 900, n), n) + passa(rosa(rng, n), 800, 5000, 2) * 0.7, 3) * env(n, 0.02, 0.4) * 0.03, 0.0)
    for k in range(4):
        poe(x, _whoosh(rng, 0.12, 1500, 9000, 0.7, 1.3, 0.3), 0.32 + 0.08 * k)
        poe(x, _baque(140, 55, 0.2, 0.5), 0.38 + 0.08 * k)
        poe(x, _rasgo(rng, 0.08, 0.22), 0.38 + 0.08 * k)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Leatherface

def motosserra_de_leatherface(rng, v):
    """Leatherface: a motosserra roncando e cortando o rival."""
    x = _z(2.2)
    poe(x, _motor(rng, 1.0, 40, 75, 0.06), 0.0)
    n = n_de(0.4)
    poe(x, satura(passa(rosa(rng, n), 1500, 8000, 2), 3) * env(n, 0.02, 0.3) * 0.25, 0.32)
    poe(x, _baque(130, 55, 0.3, 0.5), 0.32)
    return reverb(x, 0.5, 0.25)


def danca_da_serra(rng, v):
    """Leatherface: a serra girando no ar (o ronco indo e voltando)."""
    x = _z(2.3)
    m = _motor(rng, 1.1, 55, 70, 0.06)
    t = _t(len(m))
    poe(x, m * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)), 0.0)
    for k in range(3):
        poe(x, _rasgo(rng, 0.12, 0.25), 0.3 + 0.1 * k)
    return reverb(x, 0.6, 0.3)


def leatherface_preparo(rng, v):
    """Leatherface (Preparo): a motosserra acelerando parada (em laço)."""
    x = _z(1.4)
    m = _motor(rng, 1.0, 40, 60, 0.05)
    t = _t(len(m))
    poe(x, m * (0.7 + 0.3 * np.sin(2 * math.pi * 2 * t)), 0.0)
    return reverb(x, 0.5, 0.25)


def massacre_da_serra(rng, v):
    """Leatherface: a serra acelerando ao máximo e descendo em cheio."""
    x = _z(2.4)
    poe(x, _motor(rng, 1.2, 50, 90, 0.07), 0.0)
    n = n_de(0.5)
    poe(x, satura(passa(rosa(rng, n), 1500, 9000, 2), 3) * env(n, 0.02, 0.4) * 0.3, 0.33)
    poe(x, _baque(60, 22, 0.8, 1.0, 3.0), 0.34)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Pinhead

def correntes_com_ganchos(rng, v):
    """Pinhead: as correntes saindo do escuro e os ganchos fisgando."""
    x = _z(2.3)
    poe(x, _corrente(rng, 14, 0.03, 0.012), 0.05)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 800, 5000, 0.008) * 0.8, 0.35 + 0.06 * k)
        poe(x, _baque(150, 70, 0.15, 0.35), 0.35 + 0.06 * k)
    n = n_de(1.0)
    poe(x, (seno(73, n) + seno(77.8, n)) * sobe_e_some(n, 0.3, 1.2) * 0.025, 0.2)
    return reverb(x, 0.9, 0.45)


def dor_e_prazer(rng, v):
    """Pinhead: a voz grave ("dor e prazer...") e a corrente puxando o rival."""
    x = _z(2.2)
    n = n_de(0.8)
    poe(x, satura(seno(varre(85, 75, n), n) + passa(rosa(rng, n), 100, 1000, 2) * 0.5, 3) * env(n, 0.1, 0.4) * 0.035, 0.0)
    poe(x, _corrente(rng, 8, 0.03, 0.012), 0.25)
    poe(x, estalo(rng, n_de(0.03), 800, 5000, 0.008) * 0.9, 0.42)
    poe(x, _baque(110, 45, 0.3, 0.55), 0.42)
    return reverb(x, 0.9, 0.45)


def pinhead_preparo(rng, v):
    """Pinhead (Preparo): a caixa girando (os cliques do mecanismo e o sino distante em laço)."""
    x = _z(1.4)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.012), 2000, 8000, 0.002) * 0.5, 0.2 * k)
    poe(x, _sino(rng, 196, 1.0, 0.02, SINO), 0.1)
    return reverb(x, 0.9, 0.45)


def caixa_de_lemarchand(rng, v):
    """Pinhead: a caixa abrindo (o sino do inferno), as correntes e o silêncio."""
    x = _z(2.5)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.012), 2000, 8000, 0.002) * 0.6, 0.05 * k)
    poe(x, _sino(rng, 147, 1.6, 0.06, SINO), 0.2)
    poe(x, _corrente(rng, 16, 0.025, 0.012), 0.3)
    for k in range(3):
        poe(x, _baque(150, 70, 0.15, 0.35), 0.4 + 0.05 * k)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Samara

def maldicao_de_sete_dias(rng, v):
    """Samara: o anel acendendo e o telefone sussurrando "sete dias"."""
    x = _z(2.3)
    n = n_de(0.6)
    poe(x, (seno(varre(150, 300, n), n) + seno(varre(159, 318, n), n)) * env(n, 0.4, 0.15) * 0.02, 0.0)
    n2 = n_de(0.5)
    poe(x, passa(rosa(rng, n2), 1000, 5000, 2) * env(n2, 0.05, 0.4) * 0.15, 0.4)
    poe(x, _sino(rng, 1245, 0.6, 0.02, CRISTAL), 0.5)
    return reverb(x, 0.9, 0.45)


def estatica_de_samara(rng, v):
    """Samara: a TV chiando forte e a estática passando pelos rivais."""
    x = _z(2.2)
    poe(x, _estatica(rng, 0.9, 0.3), 0.1)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 1000, 8000, 0.006) * 0.6, 0.5 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


def samara_preparo(rng, v):
    """Samara (Preparo): a água pingando no poço (em laço)."""
    x = _z(1.4)
    for k in range(2):
        poe(x, _piu(1200, 600, 0.06, 0.02), 0.5 * k + 0.2)
        poe(x, _sino(rng, 880, 0.4, 0.008, SINO), 0.5 * k + 0.21)
    n = n_de(1.0)
    poe(x, (seno(110, n) + seno(116.5, n)) * sobe_e_some(n, 0.5, 1.2) * 0.01, 0.0)
    return reverb(x, 1.0, 0.5)


def sai_da_tv(rng, v):
    """Samara: a estática, a mão saindo da tela e o golpe."""
    x = _z(2.4)
    poe(x, _estatica(rng, 0.6, 0.25), 0.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.025), 300, 3000, 0.006) * 0.4, 0.25 + 0.06 * k)
    n = n_de(0.4)
    poe(x, (seno(varre(100, 70, n), n) + seno(varre(106, 74, n), n)) * env(n, 0.1, 0.3) * 0.025, 0.3)
    poe(x, _baque(60, 22, 0.8, 1.0, 3.0), 0.47)
    poe(x, _explosao(rng, 0.4, 60), 0.47)
    return reverb(x, 0.8, 0.4)


SONS: dict = {
    "facada-do-chucky": (facada_do_chucky, "Chucky: a facada"),
    "risada-do-chucky": (risada_do_chucky, "Chucky: a risada"),
    "chucky-preparo": (chucky_preparo, "Chucky: o feitiço de vodu (Preparo)"),
    "vodu": (vodu, "Chucky: o vodu"),
    "baloes-vermelhos": (baloes_vermelhos, "Pennywise: os balões vermelhos"),
    "luzes-da-morte": (luzes_da_morte, "Pennywise: as luzes da morte"),
    "pennywise-preparo": (pennywise_preparo, "Pennywise: a melodia de circo (Preparo)"),
    "medo-puro": (medo_puro, "Pennywise: o medo puro"),
    "ligacao-do-ghostface": (ligacao_do_ghostface, "Ghostface: a ligação"),
    "facada-do-ghostface": (facada_do_ghostface, "Ghostface: a facada"),
    "ghostface-preparo": (ghostface_preparo, "Ghostface: a respiração (Preparo)"),
    "grito-final": (grito_final, "Ghostface: o grito final"),
    "motosserra-de-leatherface": (motosserra_de_leatherface, "Leatherface: a motosserra"),
    "danca-da-serra": (danca_da_serra, "Leatherface: a dança da serra"),
    "leatherface-preparo": (leatherface_preparo, "Leatherface: a serra acelerando (Preparo)"),
    "massacre-da-serra": (massacre_da_serra, "Leatherface: o massacre"),
    "correntes-com-ganchos": (correntes_com_ganchos, "Pinhead: as correntes com ganchos"),
    "dor-e-prazer": (dor_e_prazer, "Pinhead: dor e prazer"),
    "pinhead-preparo": (pinhead_preparo, "Pinhead: a caixa girando (Preparo)"),
    "caixa-de-lemarchand": (caixa_de_lemarchand, "Pinhead: a caixa de Lemarchand"),
    "maldicao-de-sete-dias": (maldicao_de_sete_dias, "Samara: a maldição de sete dias"),
    "estatica-de-samara": (estatica_de_samara, "Samara: a estática"),
    "samara-preparo": (samara_preparo, "Samara: a água no poço (Preparo)"),
    "sai-da-tv": (sai_da_tv, "Samara: sai da TV"),
}
