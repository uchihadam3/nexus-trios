"""Os sons da rodada 23 das habilidades próprias (veja tools/vfx/familias_v2/rodada23.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _fogo(rng, seg, g=0.3, pico=0.2):
    n = n_de(seg)
    return satura(passa(rosa(rng, n), 150, 3500, 2), 2.5) * sobe_e_some(n, pico, 1.3) * g


def _grito(rng, f0, f1, seg, g=0.07):
    n = n_de(seg)
    t = _t(n)
    return satura(seno(varre(f0, f1, n) * (1 + 0.03 * np.sin(2 * math.pi * 25 * t)), n) + passa(rosa(rng, n), 300, 2500, 2) * 0.4, 2.5) * env(n, 0.01, seg * 0.7) * g


def _eletrico(rng, seg, g=0.4):
    return graos(rng, n_de(seg), int(80 * seg), 0.0, 0.95, 2500, 10000, 0.0015) * g


# ------------------------------------------------------------------ Liu Kang

def bola_de_fogo_liukang(rng, v):
    """Liu Kang: o grito Shaolin, a bola de fogo voando e a explosão."""
    x = _z(1.9)
    poe(x, _grito(rng, 320, 260, 0.2, 0.05), 0.0)
    poe(x, _fogo(rng, 0.5, 0.3, 0.3), 0.1)
    poe(x, _baque(140, 60, 0.3, 0.6), 0.58)
    poe(x, _fogo(rng, 0.5, 0.25, 0.1), 0.6)
    return reverb(x, 0.5, 0.25)


def liukang_preparo(rng, v):
    """Liu Kang (Preparo): o fogo girando em espiral (o rugido que sobe)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 200, 3000, 2), 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 5 * t)) * sobe_e_some(n, 0.8, 1.2) * 0.25, 0.0)
    return reverb(x, 0.5, 0.25)


def dragao_flamejante(rng, v):
    """Liu Kang: o rugido do dragão de fogo e a mordida."""
    x = _z(2.2)
    n = n_de(0.9)
    t = _t(n)
    poe(x, satura(seno(varre(160, 90, n) * (1 + 0.05 * np.sin(2 * math.pi * 22 * t)), n) + passa(rosa(rng, n), 200, 3000, 2) * 0.8, 3) * env(n, 0.05, 0.7) * 0.09, 0.0)
    poe(x, _fogo(rng, 0.9, 0.35, 0.4), 0.1)
    poe(x, _explosao(rng, 0.8, 0.6), 0.55)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Raiden

def raio_celeste(rng, v):
    """Raiden: três raios caindo do céu, um depois do outro."""
    x = _z(2.0)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.05), 2000, 9000, 0.01), 0.1 + 0.12 * k)
        poe(x, _eletrico(rng, 0.25, 0.35), 0.1 + 0.12 * k)
    poe(x, _trovao(rng, 0.8, 0.4), 0.15)
    return reverb(x, 0.6, 0.3)


def barreira_eletrica(rng, v):
    """Raiden: a cúpula elétrica se fechando (o zumbido) e as faíscas."""
    x = _z(2.0)
    n = n_de(1.2)
    t = _t(n)
    poe(x, satura(seno(120, n) + seno(240, n) * 0.4, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 8 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.05, 0.0)
    poe(x, _eletrico(rng, 1.0, 0.3), 0.1)
    poe(x, _acorde((294, 370, 440, 587), 0.8, 0.035, 0.1, 0.6), 0.3)
    return reverb(x, 0.6, 0.3)


def raidenmk_preparo(rng, v):
    """Raiden (Preparo): os olhos acendendo e as faíscas estalando."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, seno(varre(400, 900, n), n) * sobe_e_some(n, 0.7, 1.2) * 0.03, 0.0)
    poe(x, _eletrico(rng, 1.0, 0.25), 0.0)
    return reverb(x, 0.5, 0.25)


def trovao_dos_deuses(rng, v):
    """Raiden: a tempestade inteira descendo (os raios e o trovão enorme)."""
    x = _z(2.4)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.05), 2000, 9000, 0.01), 0.2 + 0.04 * k)
    poe(x, _eletrico(rng, 0.6, 0.45), 0.2)
    poe(x, _trovao(rng, 1.4, 0.7), 0.25)
    poe(x, _baque(60, 30, 0.6, 0.8, 2.6), 0.28)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Jin

def postura_mishima(rng, v):
    """Jin: a guarda (o "kiai" curto) e o brilho de foco."""
    x = _z(1.8)
    poe(x, _grito(rng, 300, 260, 0.15, 0.05), 0.0)
    poe(x, _whoosh(rng, 0.2, 500, 3000, 0.6, 1.4, 0.3), 0.05)
    poe(x, _acorde((330, 415, 494), 0.7, 0.035, 0.05, 0.5), 0.2)
    return reverb(x, 0.5, 0.25)


def contra_ataque(rng, v):
    """Jin: o aparo (o estalo) e o chute de volta."""
    x = _z(1.8)
    poe(x, estalo(rng, n_de(0.04), 2000, 8000, 0.006), 0.05)
    poe(x, _sino(rng, 2400, 0.3, 0.04, METAL), 0.05)
    poe(x, _whoosh(rng, 0.2, 600, 4000, 0.7, 1.4, 0.45), 0.3)
    poe(x, _baque(140, 60, 0.35, 0.7, 2.4), 0.5)
    return reverb(x, 0.5, 0.25)


def gene_do_diabo(rng, v):
    """Jin: as asas negras abrindo, o rosnado do Devil e o raio da testa."""
    x = _z(2.1)
    poe(x, _whoosh(rng, 0.4, 200, 2000, 0.5, 1.4, 0.5), 0.0)
    poe(x, _grito(rng, 110, 85, 0.5, 0.08), 0.1)
    n = n_de(0.35)
    poe(x, (seno(varre(1200, 800, n), n) * 0.04 + passa(rosa(rng, n), 3000, 9000, 2) * 0.15) * env(n, 0.005, 0.3), 0.4)
    poe(x, _eletrico(rng, 0.3, 0.3), 0.6)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Kazuya

def pisao_demoniaco(rng, v):
    """Kazuya: o pisão pesado e os raios roxos estalando."""
    x = _z(1.9)
    poe(x, _baque(60, 28, 0.6, 0.9, 3.0), 0.15)
    poe(x, _eletrico(rng, 0.5, 0.4), 0.17)
    poe(x, _trovao(rng, 0.6, 0.3), 0.2)
    return reverb(x, 0.6, 0.3)


def raio_do_diabo(rng, v):
    """Kazuya: o olho da testa acendendo e o laser roxo."""
    x = _z(1.8)
    poe(x, seno(varre(400, 1600, n_de(0.2)), n_de(0.2)) * env(n_de(0.2), 0.01, 0.15) * 0.04, 0.0)
    n = n_de(0.45)
    poe(x, (satura(seno(varre(900, 600, n), n), 2) * 0.04 + passa(rosa(rng, n), 2000, 8000, 2) * 0.15) * env(n, 0.005, 0.35), 0.15)
    poe(x, _baque(150, 70, 0.2, 0.4), 0.45)
    return reverb(x, 0.5, 0.25)


def kazuya_preparo(rng, v):
    """Kazuya (Preparo): os raios roxos subindo pelo corpo (o zumbido que cresce)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, satura(seno(varre(80, 160, n), n), 2.5) * sobe_e_some(n, 0.8, 1.2) * 0.07, 0.0)
    poe(x, _eletrico(rng, 1.0, 0.25), 0.0)
    return reverb(x, 0.5, 0.25)


def forma_devil(rng, v):
    """Kazuya: as asas do Devil (o bater enorme), o rugido e o golpe que queima."""
    x = _z(2.2)
    poe(x, _whoosh(rng, 0.4, 150, 2000, 0.5, 1.4, 0.55), 0.0)
    poe(x, _grito(rng, 100, 75, 0.6, 0.09), 0.1)
    poe(x, _explosao(rng, 0.9, 0.6), 0.25)
    poe(x, _whoosh(rng, 0.2, 800, 5000, 0.7, 1.4, 0.4), 0.45)
    poe(x, _fogo(rng, 0.5, 0.25, 0.1), 0.55)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Sora

def cura_sora(rng, v):
    """Sora: o feitiço Cura (o arpejo verde de Kingdom Hearts) e as folhas."""
    x = _z(2.0)
    for k, f in enumerate((523, 659, 784, 1047, 1319)):
        poe(x, _sino(rng, f, 0.5, 0.04, CRISTAL), 0.05 + 0.07 * k)
    poe(x, _acorde((523, 659, 784), 0.9, 0.035, 0.1, 0.6), 0.35)
    poe(x, _sopro(rng, 0.7, 1500, 6000, 0.12, 0.4), 0.3)
    return reverb(x, 0.7, 0.35)


def sora_preparo(rng, v):
    """Sora (Preparo): a chave-espada girando (o zunido) e o brilho da coroa."""
    x = _z(1.4)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 10 * t) ** 2) * env(n, 0.05, 0.6) * 0.15, 0.0)
    poe(x, _sino(rng, 1568, 0.6, 0.04, CRISTAL), 0.3)
    return reverb(x, 0.6, 0.3)


def forma_final(rng, v):
    """Sora: a Forma final (o acorde heroico que sobe) e as chaves flutuando."""
    x = _z(2.2)
    poe(x, _brilho(rng, 0.9, 2093, 0.05, CRISTAL), 0.0)
    for k, f in enumerate((392, 494, 587, 784)):
        poe(x, _sino(rng, f, 0.6, 0.04, SINO), 0.1 + 0.1 * k)
    poe(x, _acorde((392, 494, 587, 784, 988), 1.2, 0.05, 0.05, 0.9), 0.45)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ 2B

def lamina_virtuosa(rng, v):
    """2B: o giro da espada (o corte que roda) e o golpe final."""
    x = _z(1.9)
    n = n_de(0.55)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2000, 9000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t) ** 2) * env(n, 0.01, 0.45) * 0.3, 0.0)
    poe(x, _sino(rng, 3200, 0.4, 0.05, METAL), 0.45)
    poe(x, _baque(170, 80, 0.2, 0.4), 0.48)
    return reverb(x, 0.6, 0.3)


def apoio_do_pod(rng, v):
    """2B: o Pod disparando a rajada (os tiros de energia em sequência)."""
    x = _z(1.9)
    for k in range(9):
        n = n_de(0.08)
        poe(x, (seno(varre(1800, 900, n), n) * 0.03 + passa(rosa(rng, n), 3000, 9000, 2) * 0.1) * env(n, 0.002, 0.06), 0.15 + 0.05 * k)
    for k in range(3):
        poe(x, _baque(200, 100, 0.12, 0.3), 0.45 + 0.15 * k)
    return reverb(x, 0.5, 0.25)


def modo_berserk(rng, v):
    """2B: a viseira caindo (o clique), a aura vermelha e o golpe pesado da espada grande."""
    x = _z(2.1)
    poe(x, estalo(rng, n_de(0.03), 1000, 4000, 0.006), 0.05)
    n = n_de(0.6)
    poe(x, satura(seno(varre(80, 120, n), n), 2.5) * sobe_e_some(n, 0.7, 1.2) * 0.07, 0.0)
    poe(x, _whoosh(rng, 0.3, 300, 3000, 0.8, 1.3, 0.5), 0.3)
    poe(x, _baque(60, 28, 0.6, 1.0, 3.0), 0.5)
    poe(x, _sino(rng, 700, 0.5, 0.05, METAL), 0.5)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "bola-de-fogo-liukang": (bola_de_fogo_liukang, "Liu Kang: a bola de fogo"),
    "liukang-preparo": (liukang_preparo, "Liu Kang: o fogo em espiral (Preparo)"),
    "dragao-flamejante": (dragao_flamejante, "Liu Kang: o dragão flamejante"),
    "raio-celeste": (raio_celeste, "Raiden: o raio celeste"),
    "barreira-eletrica": (barreira_eletrica, "Raiden: a barreira elétrica"),
    "raidenmk-preparo": (raidenmk_preparo, "Raiden: os olhos (Preparo)"),
    "trovao-dos-deuses": (trovao_dos_deuses, "Raiden: o trovão dos deuses"),
    "postura-mishima": (postura_mishima, "Jin: a postura Mishima"),
    "contra-ataque": (contra_ataque, "Jin: o contra-ataque"),
    "gene-do-diabo": (gene_do_diabo, "Jin: o Gene do Diabo"),
    "pisao-demoniaco": (pisao_demoniaco, "Kazuya: o pisão demoníaco"),
    "raio-do-diabo": (raio_do_diabo, "Kazuya: o raio do diabo"),
    "kazuya-preparo": (kazuya_preparo, "Kazuya: os raios (Preparo)"),
    "forma-devil": (forma_devil, "Kazuya: a Forma Devil"),
    "cura-sora": (cura_sora, "Sora: Cura"),
    "sora-preparo": (sora_preparo, "Sora: a chave girando (Preparo)"),
    "forma-final": (forma_final, "Sora: a Forma final"),
    "lamina-virtuosa": (lamina_virtuosa, "2B: a lâmina virtuosa"),
    "apoio-do-pod": (apoio_do_pod, "2B: o apoio do Pod"),
    "modo-berserk": (modo_berserk, "2B: o modo berserk"),
}
