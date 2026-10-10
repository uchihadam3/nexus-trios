"""Os sons da rodada 4: Ravena, Thanos, Gohan, Freeza e Itachi (veja tools/vfx/familias_v2/rodada04.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z
from som import SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, serra_suave, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _coro(f0, n, gs=(0.1, 0.07, 0.05), desafina=0.004):
    """Um acorde de vozes graves, levemente desafinado (o canto)."""
    t = _t(n)
    x = np.zeros(n)
    for k, g in enumerate(gs):
        f = f0 * (1, 1.5, 2.0)[k]
        x += (seno(f * (1 + desafina * np.sin(2 * math.pi * (3 + k) * t)), n) + seno(f * (1 - desafina), n) * 0.7) * g
    return x


def _zumbido(rng, seg, f=80.0, g=1.0):
    n = n_de(seg)
    t = _t(n)
    z = serra_suave(f * (1 + 0.01 * np.sin(2 * math.pi * 7 * t)), n, 10) * 0.5
    return (passa(satura(z, 1.8), None, 2800, 2) * 0.6 + passa(rosa(rng, n), 2500, 9000, 2) * 0.1) * g


# =================================================================== Ravena
def azarath_canto(rng, v):
    """O canto: "Azarath… Metrion… Zinthos" — três sílabas de coro grave, uma após a outra, e o ar
    escuro girando."""
    x = _z(1.6)
    for k, f in enumerate((110, 98, 131)):
        n = n_de(0.42)
        poe(x, passa(_coro(f, n), 60, 1800, 2) * env(n, 0.06, 0.32), 0.45 * k)
    n = n_de(1.5)
    poe(x, passa(rosa(rng, n), 100, 900, 2) * sobe_e_some(n, 0.6, 1.4) * 0.3, 0.0)
    return reverb(x, 0.65, 0.35, 4500)


def azarath_metrion(rng, v):
    """Os tentáculos negros agarrando (o "shhhk" úmido de vários lados), o aperto grave e a alma estourando
    num eco."""
    x = _z(1.8)
    for k in range(6):
        poe(x, _whoosh(rng, 0.18, 150, 900, 0.7, g=0.3), 0.04 * k)
    n = n_de(0.5)
    poe(x, seno(varre(90, 55, n, 1.0), n) * env(n, 0.02, 0.45) * 0.3, 0.32)
    poe(x, B.explosao(rng, v) * 0.5, 0.55)
    poe(x, B.interrupcao(rng, v) * 0.3, 0.6)
    return reverb(x, 0.7, 0.35, 4000)


def manto_de_sombras(rng, v):
    """O Manto de sombras: o pano escuro se fechando (o "fuuump" abafado), o coro baixinho e a cura
    tilintando."""
    x = _z(1.7)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 100, 1200, 2) * env(n, 0.05, 0.35) * 0.6, 0.0)
    m = n_de(1.2)
    poe(x, passa(_coro(147, m, (0.06, 0.04, 0.03)), 80, 1500, 2) * sobe_e_some(m, 0.3, 1.4), 0.15)
    poe(x, B.cura(rng, v) * 0.35, 0.35)
    return reverb(x, 0.6, 0.3, 5000)


# =================================================================== Thanos
def joia_do_tempo(rng, v):
    """A Joia do Tempo: o "uóóóm" que desacelera (o som esticando e descendo), o tique que fica mais
    lento e a areia chiando, e o golpe cortado."""
    x = _z(2.0)
    n = n_de(1.6)
    t = _t(n)
    poe(x, seno(varre(520, 130, n, 0.6), n) * sobe_e_some(n, 0.15, 1.5) * 0.12, 0.0)
    tq, passo = 0.1, 0.1
    while tq < 1.6:
        b = n_de(0.03)
        poe(x, estalo(rng, b, 2500, 7000, 0.003) * 0.25, tq)
        tq += passo
        passo *= 1.35
    poe(x, graos(rng, n_de(1.5), 120, 0.0, 1.5, 4000, 10000, 0.003, 0.8) * 0.12, 0.2)
    poe(x, B.interrupcao(rng, v) * 0.35, 0.25)
    return reverb(x, 0.6, 0.3, 6000)


def manopla_joias(rng, v):
    """O Preparo do Equilíbrio: seis notas de cristal acendendo uma por uma (cada joia), o zumbido de
    poder crescendo por baixo."""
    x = _z(1.8)
    for k, f in enumerate((523, 587, 659, 784, 880, 1047)):
        poe(x, _brilho(rng, 0.5, f, 0.1), 0.2 * k)
    n = n_de(1.6)
    t = _t(n)
    poe(x, _zumbido(rng, 1.6, 55, 0.4) * (t / t[-1]) ** 1.5, 0.1)
    return reverb(x, 0.55, 0.28, 6000)


def estalo_thanos(rng, v):
    """O Equilíbrio: o ESTALO seco dos dedos, um silêncio, e o pó se desfazendo (o chiado de areia que
    leva o vento embora)."""
    x = _z(2.2)
    poe(x, estalo(rng, n_de(0.06), 800, 6000, 0.012) * 1.5, 0.0)
    poe(x, baque(n_de(0.4), 70, 40, 0.15, 0.6) * 0.5, 0.0)
    n = n_de(1.6)
    t = _t(n)
    po = passa(rosa(rng, n), 2500, 9000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.35
    vento = passa(rosa(rng, n), 300, 2000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 0.8 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.3
    poe(x, po + vento, 0.35)
    return reverb(x, 0.6, 0.3, 6000)


# =================================================================== Gohan
def masenko_carga(rng, v):
    """O Masenko juntando: o zumbido agudo subindo entre as mãos e os estalos de energia."""
    n = n_de(0.7)
    t = _t(n)
    x = _z(0.8)
    poe(x, seno(varre(300, 1300, n, 1.3), n) * (t / t[-1]) * 0.12 + _zumbido(rng, 0.7, 90, 0.3) * (t / t[-1]), 0.0)
    for _ in range(5):
        poe(x, estalo(rng, n_de(0.03), 2000, 8000, 0.006) * 0.25, rng.uniform(0.1, 0.65))
    return reverb(x, 0.4, 0.2, 7000)


def masenko(rng, v):
    """O Masenko no rival: o disparo rugindo curto e a explosão amarela."""
    x = _z(1.5)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 300, 5000, 2) * env(n, 0.005, 0.28) * 0.6, 0.0)
    poe(x, B.explosao(rng, v) * 0.8, 0.12)
    return reverb(x, 0.5, 0.25, 6500)


def aura_besta(rng, v):
    """O Preparo do Despertar: a aura explodindo para cima (o rugido do ar), o grito crescendo e os
    estalos roxos."""
    x = _z(1.8)
    n = n_de(1.6)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 150, 3000, 2) * (t / t[-1]) ** 1.2 * 0.7, 0.0)
    f = varre(160, 300, n, 1.0)
    grito = (seno(f, n) * 0.3 + seno(f * 2, n) * 0.15 + seno(f * 3, n) * 0.08) * (0.7 + 0.3 * rng.uniform(size=n)) * sobe_e_some(n, 0.8, 1.0)
    poe(x, passa(grito, 100, 2500, 2) * 0.5, 0.0)
    for _ in range(6):
        poe(x, estalo(rng, n_de(0.04), 1500, 8000, 0.008) * 0.3, rng.uniform(0.2, 1.5))
    return reverb(x, 0.55, 0.28, 5500)


def despertar_gohan(rng, v):
    """O soco desperto: o ar rasgado, o soco pesadíssimo com o estrondo e o chão rachando."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.12, 600, 4000, 0.8, g=0.6), 0.0)
    poe(x, B.soco_pesado(rng, v) * 1.2, 0.1)
    poe(x, baque(n_de(0.9), 60, 25, 0.3, 0.8) * 1.2, 0.1)
    poe(x, B.terremoto(rng, v) * 0.5, 0.15)
    return reverb(x, 0.55, 0.28, 5000)


# =================================================================== Freeza
def crueldade_freeza(rng, v):
    """Crueldade calculada: a pressão invisível (o zumbido grave que aperta e sobe), o rangido e a
    pancada quando solta."""
    x = _z(1.7)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(varre(60, 140, n, 1.4), n) * sobe_e_some(n, 0.85, 1.0) * 0.3 + passa(rosa(rng, n), 200, 1500, 2) * (t / t[-1]) * 0.2, 0.0)
    poe(x, B.soco_pesado(rng, v) * 0.9, 1.0)
    poe(x, baque(n_de(0.5), 80, 35, 0.15, 0.5) * 0.6, 1.0)
    return reverb(x, 0.5, 0.25, 5500)


def raio_mortal_saida(rng, v):
    """O Raio mortal saindo do dedo: o "tsiiu" agudíssimo e fino."""
    n = n_de(0.35)
    x = seno(varre(4200, 2600, n, 1.0), n) * env(n, 0.002, 0.3) * 0.18 + passa(rosa(rng, n), 5000, 11000, 2) * env(n, 0.002, 0.15) * 0.15
    return reverb(x, 0.3, 0.15, 9000)


def raio_mortal(rng, v):
    """O Raio mortal no rival: o furo seco (o "tchk") e o chiado do raio atravessando."""
    x = _z(1.0)
    poe(x, estalo(rng, n_de(0.05), 1500, 9000, 0.008) * 1.0, 0.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 3000, 10000, 2) * env(n, 0.003, 0.35) * 0.35, 0.0)
    poe(x, baque(n_de(0.2), 140, 70, 0.05, 0.4) * 0.4, 0.0)
    return reverb(x, 0.35, 0.18, 8000)


def bola_da_morte_carga(rng, v):
    """A Bola da Morte crescendo: o rugido de fogo inchando, grave, e a risada fria de três notas."""
    x = _z(1.6)
    n = n_de(1.4)
    t = _t(n)
    poe(x, (passa(rosa(rng, n), 60, 1500, 2) * 0.8 + seno(varre(45, 90, n, 1.0), n) * 0.3) * (t / t[-1]) ** 1.2, 0.0)
    for k, f in enumerate((440, 415, 392)):
        m = n_de(0.12)
        poe(x, seno(f, m) * env(m, 0.005, 0.1) * 0.06, 0.9 + 0.13 * k)
    return reverb(x, 0.55, 0.28, 5000)


def bola_da_morte(rng, v):
    """A Bola da Morte no rival: a explosão enorme e longa, o fogo rugindo e o eco."""
    x = _z(2.4)
    poe(x, B.explosao(rng, v) * 1.1, 0.0)
    poe(x, B.fogo(rng, v) * 0.6, 0.1)
    poe(x, baque(n_de(1.2), 50, 22, 0.4, 0.9) * 1.2, 0.0)
    return reverb(x, 0.7, 0.35, 4500)


# =================================================================== Itachi
def tsukuyomi(rng, v):
    """O Tsukuyomi: o som de olho girando (o "vuíííum" que entorta), o mundo afundando num tom grave
    invertido e o silêncio pesado do sono."""
    x = _z(2.0)
    n = n_de(0.5)
    poe(x, seno(varre(900, 300, n, 1.0) * (1 + 0.05 * np.sin(2 * math.pi * 9 * _t(n))), n) * env(n, 0.01, 0.45) * 0.15, 0.0)
    m = n_de(1.6)
    t = _t(m)
    poe(x, (seno(55, m) * 0.3 + seno(82.5, m) * 0.15) * sobe_e_some(m, 0.3, 1.4) * (1 + 0.2 * np.sin(2 * math.pi * 0.5 * t)), 0.2)
    poe(x, passa(rosa(rng, m), 80, 600, 2) * sobe_e_some(m, 0.3, 1.4) * 0.25, 0.2)
    return reverb(x, 0.75, 0.4, 3500)


SONS: dict = {
    "azarath-canto": (azarath_canto, "Ravena: o canto do Azarath (Preparo)"),
    "azarath-metrion": (azarath_metrion, "Azarath Metrion Zinthos: os tentáculos e a alma"),
    "manto-de-sombras": (manto_de_sombras, "Manto de sombras: o pano escuro e a cura"),
    "joia-do-tempo": (joia_do_tempo, "Joia do Tempo: o som esticando e a areia"),
    "manopla-joias": (manopla_joias, "Equilíbrio: as seis joias acendendo (Preparo)"),
    "estalo-thanos": (estalo_thanos, "Equilíbrio: o estalo e o pó"),
    "masenko-carga": (masenko_carga, "Masenko: a energia juntando"),
    "masenko": (masenko, "Masenko: o disparo e a explosão"),
    "aura-besta": (aura_besta, "Despertar: a aura explodindo (Preparo)"),
    "despertar-gohan": (despertar_gohan, "Despertar: o soco desperto"),
    "crueldade-freeza": (crueldade_freeza, "Crueldade calculada: a pressão e a pancada"),
    "raio-mortal-saida": (raio_mortal_saida, "Raio mortal: o raio fino saindo"),
    "raio-mortal": (raio_mortal, "Raio mortal: o furo"),
    "bola-da-morte-carga": (bola_da_morte_carga, "Forma final: a Bola da Morte crescendo"),
    "bola-da-morte": (bola_da_morte, "Forma final: a explosão enorme"),
    "tsukuyomi": (tsukuyomi, "Tsukuyomi: o olho girando e o mundo afundando"),
}
