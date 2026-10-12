"""Os sons da rodada 6: Yuji, Megumi, Nobara, Sukuna e Ichigo (veja tools/vfx/familias_v2/rodada06.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z
from som import METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _crack(rng, g=0.6):
    """O estalo de raio curto: o "crack" seco e o chiado elétrico."""
    n = n_de(0.35)
    y = np.zeros(n)
    x = estalo(rng, n_de(0.03), 2000, 9000) * 1.2
    y[: len(x)] += x
    y += passa(rosa(rng, n), 1500, 8000, 2) * env(n, 0.002, 0.25) * 0.4
    return y * g


def _lamina(rng, seg=0.3, f0=2600, g=0.6):
    """O "shhing" de uma lâmina: o ar cortado agudo e o tinido."""
    n = n_de(seg)
    x = passa(rosa(rng, n), 2000, 11000, 2) * sobe_e_some(n, 0.2, 1.6) * 0.6
    x += modal(n, f0, rng=rng, **METAL) * env(n, 0.001, seg * 0.7) * 0.12
    return x * g


def _gorgolejo(rng, g=0.3):
    n = n_de(0.18)
    return (passa(rosa(rng, n), 90, 700, 2) * 0.7 + seno(varre(260, 80, n, 1.0), n) * 0.5) * env(n, 0.004, 0.14) * g


def _rugido(rng, seg, f0, g=0.4, aspereza=3.0):
    """Um rugido grave e áspero: o ruído grave modulado e saturado."""
    n = n_de(seg)
    t = _t(n)
    base = passa(rosa(rng, n), 50, 900, 2) * (0.55 + 0.45 * np.sin(2 * math.pi * f0 * t))
    voz = seno(varre(f0 * 3.2, f0 * 2.2, n, 1.0), n) * 0.35
    return satura(base + voz, aspereza) * sobe_e_some(n, 0.35, 1.3) * g


# =================================================================== Yuji
def vontade_indomavel(rng, v):
    """A Vontade Indomável: o zumbido do Preparo do rival (o tom que gira), o punho chegando (o ar
    rasgado subindo), o vidro do Preparo trincando e estourando em cacos, e o baque fundo do soco."""
    x = _z(1.6)
    n = n_de(0.4)
    poe(x, seno(220 + 30 * np.sin(2 * math.pi * 7 * _t(n)), n) * sobe_e_some(n, 0.7, 1.2) * 0.08, 0.0)
    poe(x, _whoosh(rng, 0.32, 300, 1800, 0.85, 1.6, 0.7), 0.12)
    poe(x, baque(n_de(0.5), 95, 40, 0.18, 0.6) * 0.9, 0.42)
    poe(x, B.soco_pesado(rng, v)[: n_de(0.4)] * 0.6, 0.42)
    poe(x, modal(n_de(0.6), 2300, rng=rng, **VIDRO) * env(n_de(0.6), 0.001, 0.35) * 0.18, 0.44)
    poe(x, graos(rng, n_de(0.7), 34, 0.0, 0.6, 2500, 9000, 0.006, 0.6) * 0.35, 0.46)
    return reverb(x, 0.45, 0.22)


# =================================================================== Megumi
def nue(rng, v):
    """O Nue: duas batidas de asa enormes (o "vuf" grave que pulsa), o pio agudo da coruja e três
    raios caindo, um depois do outro, com o chiado elétrico."""
    x = _z(1.9)
    for k in range(2):
        n = n_de(0.32)
        asa = passa(rosa(rng, n), 120, 1400, 2) * sobe_e_some(n, 0.45, 1.5) * 0.6
        poe(x, asa, 0.0 + 0.24 * k)
    m = n_de(0.38)
    t = _t(m)
    pio = seno(varre(1500, 900, m, 0.8) * (1 + 0.02 * np.sin(2 * math.pi * 30 * t)), m) * sobe_e_some(m, 0.25, 1.4) * 0.12
    poe(x, pio + seno(varre(3000, 1800, m, 0.8), m) * sobe_e_some(m, 0.25, 1.4) * 0.03, 0.18)
    for k in range(3):
        poe(x, _crack(rng, 0.7), 0.55 + 0.22 * k)
        poe(x, baque(n_de(0.3), 70, 40, 0.12, 0.3) * 0.35, 0.56 + 0.22 * k)
    return reverb(x, 0.55, 0.28)


def jardim_das_sombras(rng, v):
    """O Jardim das Sombras: a poça de sombra borbulhando (o líquido grosso), o arrasto das mãos
    subindo (o sopro que sobe) e o aperto (o rangido e o baque surdo)."""
    x = _z(1.8)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 40, 400, 2) * sobe_e_some(n, 0.3, 1.2) * 0.4, 0.0)
    for k in range(7):
        poe(x, _gorgolejo(rng, 0.22), 0.05 + 0.09 * k)
    poe(x, _whoosh(rng, 0.5, 120, 700, 0.8, 1.4, 0.5), 0.3)
    m = n_de(0.35)
    rangido = satura(seno(varre(160, 120, m, 1.0) * (1 + 0.1 * np.sign(np.sin(2 * math.pi * 38 * _t(m)))), m), 2) * env(m, 0.01, 0.3) * 0.1
    poe(x, rangido, 0.85)
    poe(x, baque(n_de(0.4), 60, 34, 0.2, 0.2) * 0.7, 0.9)
    return reverb(x, 0.55, 0.3)


# =================================================================== Nobara
def _cravo(rng, g=0.6, f0=1900):
    """O prego cravando: o "tchac" metálico curto e a madeira/carne surda."""
    n = n_de(0.3)
    y = modal(n, f0, rng=rng, **METAL) * env(n, 0.001, 0.12) * 0.35
    y += passa(rosa(rng, n), 200, 2500, 2) * env(n, 0.001, 0.05) * 0.6
    y += baque(n, 140, 80, 0.06, 0.5) * 0.3
    return y * g


def pregos_amaldicoados(rng, v):
    """Os três pregos: cada um assobia no ar e crava (o metal), um depois do outro; depois o zumbido
    da energia amaldiçoada enrolando."""
    x = _z(1.6)
    for k in range(3):
        poe(x, _whoosh(rng, 0.22, 2400, 4800, 0.8, 1.3, 0.25), 0.0 + 0.04 * k)
        poe(x, _cravo(rng, 0.7, 1800 + 200 * k), 0.24 + 0.05 * k)
    n = n_de(0.7)
    t = _t(n)
    zumbido = (seno(146, n) + seno(149.5, n) * 0.8 + seno(292, n) * 0.3) * (0.6 + 0.4 * np.sin(2 * math.pi * 5 * t))
    poe(x, zumbido * sobe_e_some(n, 0.4, 1.3) * 0.08, 0.45)
    poe(x, passa(rosa(rng, n), 1000, 4000, 2) * sobe_e_some(n, 0.4, 1.3) * 0.08, 0.45)
    return reverb(x, 0.45, 0.22)


def ressonancia_amaldicoada(rng, v):
    """A Ressonância: a martelada no prego (o metal e a madeira do boneco), e o "uuuum" da ressonância
    que sai em ondas (o tom grave batendo, três vezes)."""
    x = _z(2.0)
    poe(x, _cravo(rng, 1.0, 1500), 0.25)
    poe(x, baque(n_de(0.3), 180, 110, 0.07, 0.6) * 0.5, 0.25)
    for k in range(3):
        n = n_de(0.8)
        t = _t(n)
        onda = (seno(98, n) + seno(101, n) + seno(196, n) * 0.4) * (0.6 + 0.4 * np.sin(2 * math.pi * 9 * t)) * env(n, 0.01, 0.6)
        poe(x, onda * 0.13, 0.32 + 0.14 * k)
        poe(x, _whoosh(rng, 0.3, 400, 1600, 0.3, 1.5, 0.18), 0.32 + 0.14 * k)
    return reverb(x, 0.6, 0.3)


def grampo_de_cabelo(rng, v):
    """O Grampo: os pregos piscando (os bipes agudos acelerando) e as cinco explosões em sequência,
    a última maior."""
    x = _z(1.8)
    for k in range(5):
        n = n_de(0.05)
        poe(x, seno(2600, n) * env(n, 0.001, 0.04) * 0.08, 0.02 + 0.06 * k)
    for k in range(5):
        boom = B.explosao(rng, v)
        g = 0.5 if k < 4 else 0.95
        poe(x, boom[: n_de(0.5 if k < 4 else 0.9)] * g, 0.36 + 0.09 * k)
        poe(x, estalo(rng, n_de(0.02), 1500, 7000) * 0.5, 0.36 + 0.09 * k)
    poe(x, graos(rng, n_de(0.6), 20, 0.0, 0.5, 2000, 7000, 0.006, 0.5) * 0.2, 0.75)
    return reverb(x, 0.5, 0.25)


# =================================================================== Sukuna
def cleave(rng, v):
    """O Cleave: o tom fino da medida (subindo, tenso), um silêncio curto, e o corte único — longo,
    limpo, com o tinido do aço e a carne partindo."""
    x = _z(1.6)
    n = n_de(0.55)
    poe(x, seno(varre(1800, 3200, n, 1.3), n) * sobe_e_some(n, 0.9, 1.1) * 0.05, 0.0)
    poe(x, _lamina(rng, 0.55, 3100, 1.0), 0.62)
    poe(x, _whoosh(rng, 0.35, 900, 4200, 0.3, 1.4, 0.5), 0.6)
    m = n_de(0.3)
    poe(x, passa(rosa(rng, m), 150, 1500, 2) * env(m, 0.002, 0.15) * 0.5 + baque(m, 90, 50, 0.08, 0.2) * 0.4, 0.7)
    return reverb(x, 0.5, 0.25)


def santuario_preparo(rng, v):
    """O Preparo do Santuário: as mãos batendo no selo, o drone grave do domínio crescendo e o coro
    sombrio das bocas (o "aaah" sem palavras)."""
    x = _z(1.4)
    poe(x, passa(rosa(rng, n_de(0.06)), 800, 4000, 2) * env(n_de(0.06), 0.001, 0.04) * 0.6, 0.0)
    n = n_de(1.3)
    t = _t(n)
    drone = (seno(55, n) + seno(82.5, n) * 0.6 + seno(110.4, n) * 0.4) * (0.7 + 0.3 * np.sin(2 * math.pi * 1.5 * t))
    poe(x, drone * sobe_e_some(n, 0.7, 1.1) * 0.18, 0.05)
    coro = sum(passa(rosa(rng, n), f * 0.9, f * 1.1, 2) for f in (650, 1080, 2650)) * sobe_e_some(n, 0.7, 1.2) * 0.12
    poe(x, coro, 0.1)
    return reverb(x, 0.65, 0.35)


def santuario_maligno(rng, v):
    """O Santuário Maligno: o domínio fecha (o baque fundo), e dezenas de cortes ao mesmo tempo — uma
    chuva de "shings" curtos por mais de um segundo — e o estrondo final."""
    x = _z(2.2)
    poe(x, baque(n_de(0.8), 50, 28, 0.4, 0.4) * 0.8, 0.0)
    poe(x, passa(rosa(rng, n_de(1.6)), 40, 300, 2) * sobe_e_some(n_de(1.6), 0.5, 1.2) * 0.3, 0.05)
    sub = np.random.default_rng(66)
    for _ in range(38):
        em = 0.2 + sub.uniform(0, 1.15)
        poe(x, _lamina(rng, sub.uniform(0.08, 0.18), sub.uniform(2200, 4200), sub.uniform(0.15, 0.4)), em)
    poe(x, B.explosao(rng, v)[: n_de(0.8)] * 0.6, 1.45)
    return reverb(x, 0.6, 0.3)


# =================================================================== Ichigo
def mascara_hollow(rng, v):
    """A Máscara Hollow: a pressão escura subindo (o vento grave ao contrário), o rugido distorcido
    do Hollow quando a máscara fecha, e o estouro da pressão espiritual em dois anéis."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 60, 1200, 2) * (np.linspace(0, 1, n) ** 2) * 0.5, 0.0)
    poe(x, _rugido(rng, 0.9, 38, 0.55, 4.0), 0.42)
    poe(x, baque(n_de(0.5), 70, 35, 0.25, 0.3) * 0.7, 0.85)
    poe(x, baque(n_de(0.5), 60, 30, 0.25, 0.2) * 0.5, 1.0)
    poe(x, _whoosh(rng, 0.5, 200, 900, 0.2, 1.3, 0.35), 0.86)
    return reverb(x, 0.55, 0.3)


def bankai_preparo(rng, v):
    """O Preparo do Bankai: o redemoinho da pressão espiritual — o vento que gira e sobe de tom, com
    o zumbido grave por baixo."""
    x = _z(1.3)
    n = n_de(1.2)
    t = _t(n)
    vento = passa(rosa(rng, n), 200, 2500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * (3 + 6 * t) * t))
    poe(x, vento * sobe_e_some(n, 0.75, 1.1) * 0.45, 0.0)
    poe(x, seno(varre(70, 110, n, 1.0), n) * sobe_e_some(n, 0.75, 1.1) * 0.15, 0.0)
    return reverb(x, 0.5, 0.3)


def bankai_ichigo(rng, v):
    """O Getsuga do Bankai: a lâmina girando (o "vum" grave), a meia-lua avançando (o rugido do ar
    que cresce), o corte (o estalo e o aço) e o estrondo com a cauda grave."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.4, 150, 600, 0.6, 1.5, 0.5), 0.0)
    n = n_de(0.55)
    poe(x, passa(rosa(rng, n), 100, 3000, 2) * (np.linspace(0, 1, n) ** 1.6) * 0.6, 0.15)
    poe(x, _lamina(rng, 0.45, 2000, 0.9), 0.68)
    poe(x, estalo(rng, n_de(0.03), 1500, 8000) * 0.7, 0.68)
    poe(x, baque(n_de(0.9), 60, 28, 0.45, 0.5) * 0.9, 0.7)
    poe(x, passa(rosa(rng, n_de(0.8)), 40, 400, 2) * env(n_de(0.8), 0.01, 0.6) * 0.35, 0.72)
    return reverb(x, 0.55, 0.3)


SONS: dict = {
    "vontade-indomavel": (vontade_indomavel, "Yuji: o Preparo do rival estoura com o soco"),
    "nue": (nue, "Megumi: as asas do Nue, o pio e os três raios"),
    "jardim-das-sombras": (jardim_das_sombras, "Megumi: a poça de sombra e as mãos que apertam"),
    "pregos-amaldicoados": (pregos_amaldicoados, "Nobara: três pregos cravando"),
    "ressonancia-amaldicoada": (ressonancia_amaldicoada, "Nobara: a martelada e a ressonância"),
    "grampo-de-cabelo": (grampo_de_cabelo, "Nobara: os pregos explodindo em sequência"),
    "cleave": (cleave, "Sukuna: a medida e o corte único"),
    "santuario-preparo": (santuario_preparo, "Sukuna: o selo e o domínio crescendo (antes do golpe)"),
    "santuario-maligno": (santuario_maligno, "Sukuna: a chuva de cortes do Santuário"),
    "mascara-hollow": (mascara_hollow, "Ichigo: o rugido do Hollow e a pressão"),
    "bankai-preparo": (bankai_preparo, "Ichigo: o redemoinho do Bankai (antes do golpe)"),
    "bankai-ichigo": (bankai_ichigo, "Ichigo: o Getsuga do Bankai"),
}
