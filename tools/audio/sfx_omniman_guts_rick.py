"""Os sons do Omni-Man, do Guts e do Rick Sanchez (veja tools/vfx/familias_v2/omniman_guts_rick.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, nota
from som import SR, baque, env, estalo, graos, n_de, passa, poe, reverb, rosa, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _estrondo_sonico(rng, g=1.0):
    """O estrondo sônico: o estalo seco e o "BUUM" grave que rola."""
    x = _z(1.0)
    poe(x, estalo(rng, n_de(0.04), 300, 6000, 0.008) * 1.0, 0.0)
    poe(x, baque(n_de(0.8), 60, 25, 0.3, 0.8) * 1.2, 0.0)
    n = n_de(0.7)
    poe(x, passa(rosa(rng, n), 30, 300, 2) * env(n, 0.005, 0.6) * 0.8, 0.0)
    return x * g


# =================================================================== Omni-Man
def golpe_viltrumita(rng, v):
    """O Golpe viltrumita: o ar cortado, o soco que estoura com o estrondo e o chão rachando."""
    x = _z(1.5)
    poe(x, _whoosh(rng, 0.15, 500, 2500, 0.9, g=0.6), 0.0)
    poe(x, B.soco_pesado(rng, v) * 1.1, 0.12)
    poe(x, _estrondo_sonico(rng, 0.6), 0.12)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.05), 300, 2500, 0.02) * 0.3, 0.22 + 0.05 * k)
    return reverb(x, 0.45, 0.22, 5500)


def voo_de_impacto(rng, v):
    """O Voo de impacto: o rugido do vento subindo de tom enquanto ele desce, o estrondo sônico e o
    soco no fim."""
    x = _z(1.8)
    n = n_de(0.55)
    t = _t(n)
    vento = passa(rosa(rng, n), 200, 3000, 2) * (t / t[-1]) ** 1.5 * 0.9
    poe(x, vento, 0.0)
    poe(x, seno(varre(200, 700, n, 1.0), n) * (t / t[-1]) ** 2 * 0.1, 0.0)
    poe(x, _estrondo_sonico(rng, 1.0), 0.5)
    poe(x, B.soco_pesado(rng, v) * 0.9, 0.52)
    return reverb(x, 0.5, 0.25, 5000)


def sem_piedade(rng, v):
    """Sem piedade: seis socos pesados um atrás do outro, cada vez mais fortes, e o último com o
    estrondo."""
    x = _z(1.9)
    for k in range(6):
        poe(x, B.soco_pesado(rng, v) * (0.55 + 0.07 * k), 0.07 * k * 1.4)
    poe(x, _estrondo_sonico(rng, 0.9), 0.62)
    poe(x, B.soco_pesado(rng, v) * 1.1, 0.62)
    return reverb(x, 0.45, 0.22, 5500)


# =================================================================== Guts
def matadora_guts(rng, v):
    """A Matadora de Dragões: o ferro enorme cortando o ar devagar (o "vuuum" grave), o golpe que
    bate como uma pancada e corta junto, e o metal tremendo."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.35, 150, 900, 0.6, g=0.9), 0.0)
    poe(x, B.corte_pesado(rng, v) * 1.0, 0.3)
    poe(x, baque(n_de(0.6), 80, 35, 0.2, 0.7) * 1.0, 0.3)
    n = n_de(0.9)
    t = _t(n)
    metal = (seno(140, n) * 0.5 + seno(311, n) * 0.3 + seno(587, n) * 0.15) * np.exp(-t * 4) * (1 + 0.3 * np.sin(2 * math.pi * 7 * t))
    poe(x, metal * 0.25, 0.32)
    return reverb(x, 0.5, 0.25, 5000)


def armadura_berserker(rng, v):
    """A Armadura Berserker: as placas de metal fechando (os estalos metálicos em sequência), o rosnado
    grave e a respiração da besta."""
    x = _z(1.9)
    for k in range(8):
        m = n_de(0.12)
        tt = _t(m)
        clang = (seno(400 + 60 * k, m) * 0.4 + seno(1100 + 90 * k, m) * 0.2) * np.exp(-tt * 30)
        poe(x, clang * 0.35 + estalo(rng, m, 1500, 6000, 0.01)[:m] * 0.2, 0.06 * k)
    n = n_de(1.3)
    t = _t(n)
    f = 70 * (1 + 0.04 * np.sin(2 * math.pi * 5 * t))
    rosnado = (seno(f, n) * 0.3 + seno(f * 2, n) * 0.15) * (0.7 + 0.3 * rng.uniform(size=n)) * sobe_e_some(n, 0.4, 1.2)
    poe(x, passa(rosnado, 50, 900, 2) * 0.9, 0.5)
    return reverb(x, 0.5, 0.25, 4500)


def ultimo_esforco(rng, v):
    """O Último esforço: o grito de guerra (o tom rasgado subindo), a lâmina caindo e o chão
    afundando."""
    x = _z(2.0)
    n = n_de(0.45)
    t = _t(n)
    f = varre(150, 260, n, 1.0)
    grito = (seno(f, n) * 0.3 + seno(f * 2, n) * 0.15 + seno(f * 3, n) * 0.08) * (0.7 + 0.3 * rng.uniform(size=n)) * env(n, 0.03, 0.3)
    poe(x, passa(grito, 80, 2000, 2) * 0.8, 0.0)
    poe(x, _whoosh(rng, 0.2, 200, 1200, 0.9, g=0.8), 0.3)
    poe(x, B.corte_pesado(rng, v) * 1.0, 0.45)
    poe(x, B.terremoto(rng, v) * 0.6, 0.47)
    poe(x, baque(n_de(0.9), 55, 22, 0.35, 0.9) * 1.2, 0.45)
    _ = t
    return reverb(x, 0.55, 0.28, 5000)


# =================================================================== Rick
def pistola_de_portal(rng, v):
    """A Pistola de portal no rival: o portal abrindo (o "vrrr" líquido que gira), o estouro saindo
    dele e o portal fechando com um "flup"."""
    x = _z(1.5)
    m = n_de(0.8)
    t = _t(m)
    gira = passa(rosa(rng, m), 200, 2500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 14 * t)) * sobe_e_some(m, 0.2, 1.3) * 0.5
    gira += seno(varre(180, 120, m, 1.0) * (1 + 0.05 * np.sin(2 * math.pi * 6 * t)), m) * sobe_e_some(m, 0.2, 1.3) * 0.15
    poe(x, gira, 0.0)
    poe(x, B.explosao(rng, v) * 0.55, 0.25)
    n = n_de(0.15)
    poe(x, seno(varre(300, 900, n, 1.0), n) * env(n, 0.003, 0.12) * 0.2, 0.75)
    return reverb(x, 0.45, 0.22, 6500)


def invencao_improvisada(rng, v):
    """A Invenção improvisada: o aparelho apitando cada vez mais rápido, a explosão esquisita (com
    um tom que entorta) e os pedaços de metal caindo."""
    x = _z(2.1)
    for k in range(6):
        m = n_de(0.05)
        poe(x, seno(2200, m) * env(m, 0.002, 0.04) * 0.15, 0.2 * (1 - k / 7) * k * 0.6)
    poe(x, B.explosao(rng, v) * 0.9, 0.55)
    n = n_de(0.9)
    t = _t(n)
    poe(x, seno(400 * (1 + 0.3 * np.sin(2 * math.pi * 3 * t)), n) * env(n, 0.01, 0.8) * 0.1, 0.6)
    for k in range(7):
        m = n_de(0.1)
        tt = _t(m)
        poe(x, seno(rng.uniform(800, 2000), m) * np.exp(-tt * 40) * 0.15, 0.9 + 0.1 * k + rng.uniform(0, 0.05))
    return reverb(x, 0.5, 0.25, 6000)


def plano_b_carga(rng, v):
    """O Plano B saindo: o canhão carregando (o zumbido que sobe rápido) e o disparo de plasma
    rugindo."""
    x = _z(1.3)
    n = n_de(0.4)
    poe(x, seno(varre(200, 1600, n, 1.4), n) * sobe_e_some(n, 0.9, 1.0) * 0.15, 0.0)
    m = n_de(0.85)
    t = _t(m)
    feixe = passa(rosa(rng, m), 150, 3500, 2) * (0.8 + 0.2 * np.sin(2 * math.pi * 12 * t)) * 0.7 + seno(90, m) * 0.12
    poe(x, feixe * sobe_e_some(m, 0.05, 1.2), 0.38)
    poe(x, graos(rng, m, 30, 0.0, 0.8, 2000, 8000, 0.003, 0.8) * 0.3, 0.38)
    return reverb(x, 0.45, 0.22, 6000)


def plano_b(rng, v):
    """O Plano B no rival: a explosão enorme do plasma, os estalos elétricos e o golpe cortado."""
    x = _z(1.6)
    poe(x, B.explosao(rng, v) * 1.0, 0.0)
    poe(x, B.interrupcao(rng, v) * 0.4, 0.05)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.05), 2000, 8000, 0.01) * 0.3, 0.05 + 0.07 * k + rng.uniform(0, 0.03))
    return reverb(x, 0.55, 0.28, 6000)


# =================================================================== Ciclope
def laser_curto(rng, v):
    """O Ricochete óptico saindo: o "pew" curto do laser deixando o visor."""
    m = n_de(0.25)
    x = seno(varre(1900, 800, m, 1.0), m) * env(m, 0.002, 0.2) * 0.25 + passa(rosa(rng, m), 2000, 8000, 2) * env(m, 0.002, 0.08) * 0.15
    return reverb(x, 0.3, 0.15, 8000)


SONS: dict = {
    "golpe-viltrumita": (golpe_viltrumita, "Golpe viltrumita: o soco e o estrondo"),
    "voo-de-impacto": (voo_de_impacto, "Voo de impacto: a descida supersônica e o estrondo"),
    "sem-piedade": (sem_piedade, "Sem piedade: a surra"),
    "matadora-guts": (matadora_guts, "Matadora de Dragões: o ferro enorme"),
    "armadura-berserker": (armadura_berserker, "Armadura Berserker: as placas fechando e o rosnado"),
    "ultimo-esforco": (ultimo_esforco, "Último esforço: o grito e o golpe que afunda o chão"),
    "pistola-de-portal": (pistola_de_portal, "Pistola de portal: o tiro e o portal"),
    "invencao-improvisada": (invencao_improvisada, "Invenção improvisada: o apito e a explosão esquisita"),
    "plano-b-carga": (plano_b_carga, "Plano B: o canhão carregando e disparando"),
    "plano-b": (plano_b, "Plano B: a explosão do plasma"),
    "laser-curto": (laser_curto, "Ricochete óptico: o laser curto saindo"),
}
