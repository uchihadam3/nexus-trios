"""Os sons da rodada 39 das habilidades próprias (veja tools/vfx/familias_v2/rodada39.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _gelo(rng, n_cristais=6, g=0.03):
    x = _z(0.6)
    q = np.random.default_rng(9)
    for k in range(n_cristais):
        poe(x, _sino(rng, q.uniform(2500, 4500), 0.2, g, CRISTAL), 0.06 * k)
        poe(x, estalo(rng, n_de(0.02), 3000, 9000, 0.004) * 0.4, 0.06 * k)
    return x


def _borbulha(rng, seg, g=0.03, seed=3):
    x = _z(seg + 0.2)
    q = np.random.default_rng(seed)
    for k in range(int(seg * 14)):
        f = q.uniform(300, 800)
        poe(x, _piu(f, f * 1.6, 0.04, g), k / 14)
    return x


# ------------------------------------------------------------------ Hera Venenosa

def beijo_venenoso(rng, v):
    """Hera: o beijo soprado ("muah") e o veneno chiando no rival."""
    x = _z(2.0)
    n = n_de(0.15)
    poe(x, passa(rosa(rng, n), 1000, 5000, 2) * env(n, 0.005, 0.12) * 0.3, 0.05)
    poe(x, _piu(600, 900, 0.1, 0.03), 0.12)
    poe(x, _sopro(rng, 0.4, 800, 4000, 0.12, 0.3), 0.15)
    poe(x, _borbulha(rng, 0.5, 0.02), 0.6)
    return reverb(x, 0.6, 0.3)


def raizes_estranguladoras(rng, v):
    """Hera: as raízes rompendo o chão e apertando (o rangido de madeira)."""
    x = _z(2.0)
    for k in range(4):
        poe(x, satura(passa(rosa(rng, n_de(0.12)), 100, 1200, 2), 2) * env(n_de(0.12), 0.005, 0.1) * 0.35, 0.05 * k)
    n = n_de(0.6)
    t = _t(n)
    poe(x, satura(seno(varre(180, 120, n), n) * (0.5 + 0.5 * np.sin(2 * math.pi * 22 * t)), 3) * env(n, 0.05, 0.4) * 0.04, 0.35)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.03), 500, 3000, 0.008) * 0.6, 0.4 + 0.1 * k)
    return reverb(x, 0.5, 0.25)


def hera_preparo(rng, v):
    """Hera (Preparo): a flor abrindo e os esporos soltando (o sopro em laço)."""
    x = _z(1.4)
    poe(x, _sopro(rng, 1.0, 600, 4000, 0.12, 0.5), 0.0)
    poe(x, graos(rng, n_de(1.0), 20, 0.0, 0.95, 2000, 6000, 0.003) * 0.25, 0.0)
    n = n_de(1.0)
    poe(x, seno(varre(400, 600, n), n) * sobe_e_some(n, 0.6, 1.2) * 0.012, 0.0)
    return reverb(x, 0.6, 0.3)


def jardim_toxico(rng, v):
    """Hera: as flores brotando (os "pops"), a nuvem de esporos e a cura do trio."""
    x = _z(2.3)
    for k in range(3):
        poe(x, _piu(300 + 60 * k, 700 + 60 * k, 0.12, 0.035), 0.1 + 0.07 * k)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 500, 4000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.3, 0.35)
    poe(x, _borbulha(rng, 0.5, 0.018, 5), 0.4)
    poe(x, _acorde((349, 440, 523), 0.8, 0.03, 0.05, 0.6), 0.6)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Homem de Gelo

def rajada_congelante(rng, v):
    """Homem de Gelo: o jato de gelo chiando e os cristais formando no rival."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 2500, 10000, 2) * env(n, 0.02, 0.35) * 0.35, 0.05)
    poe(x, _gelo(rng, 5, 0.03), 0.35)
    poe(x, _baque(150, 70, 0.2, 0.4), 0.3)
    return reverb(x, 0.6, 0.3)


def muralha_de_gelo(rng, v):
    """Homem de Gelo: a muralha subindo bloco por bloco (os estalos de gelo)."""
    x = _z(2.0)
    for k in range(5):
        poe(x, _baque(140 + 20 * k, 80, 0.12, 0.4), 0.06 * k)
        poe(x, estalo(rng, n_de(0.04), 1500, 7000, 0.008) * 0.7, 0.06 * k)
        poe(x, _sino(rng, 2349 + 200 * k, 0.3, 0.02, CRISTAL), 0.06 * k + 0.02)
    poe(x, _brilho(rng, 0.6, 1568, 0.025, CRISTAL), 0.4)
    return reverb(x, 0.7, 0.35)


def iceman_preparo(rng, v):
    """Homem de Gelo (Preparo): o corpo virando gelo (o estalar contínuo e o frio)."""
    x = _z(1.4)
    for k in range(12):
        poe(x, estalo(rng, n_de(0.02), 3000, 9000, 0.004) * 0.35, 0.08 * k)
    poe(x, _sopro(rng, 1.0, 2000, 8000, 0.1, 0.5), 0.0)
    return reverb(x, 0.6, 0.3)


def era_glacial(rng, v):
    """Homem de Gelo: as geleiras brotando em fila (o rachar enorme) e o vento gelado."""
    x = _z(2.4)
    for k in range(10):
        poe(x, satura(passa(rosa(rng, n_de(0.08)), 300, 4000, 2), 2) * env(n_de(0.08), 0.003, 0.07) * 0.35, 0.05 + 0.03 * k)
        poe(x, _sino(rng, 2093 + 150 * (k % 5), 0.25, 0.015, CRISTAL), 0.05 + 0.03 * k)
    poe(x, _baque(70, 30, 0.6, 0.8, 2.6), 0.2)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 800, 6000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.25, 0.4)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Gengar

def hipnose_gengar(rng, v):
    """Gengar: a hipnose (o tom ondulante que gira) e o ronco do rival dormindo."""
    x = _z(2.0)
    n = n_de(0.6)
    t = _t(n)
    poe(x, seno(500 + 150 * np.sin(2 * math.pi * 4 * t), n) * env(n, 0.05, 0.3) * 0.03, 0.0)
    poe(x, seno(750 + 225 * np.sin(2 * math.pi * 4 * t + 1), n) * env(n, 0.05, 0.3) * 0.015, 0.0)
    for k in range(2):
        n = n_de(0.4)
        poe(x, passa(rosa(rng, n), 100, 900, 2) * sobe_e_some(n, 0.5, 1.2) * 0.2, 0.6 + 0.5 * k)
    return reverb(x, 0.6, 0.3)


def bola_sombria(rng, v):
    """Gengar: a bola de sombra crescendo (o zumbido grave) e estourando."""
    x = _z(2.0)
    n = n_de(0.5)
    t = _t(n)
    poe(x, satura(seno(varre(60, 110, n), n) + passa(rosa(rng, n), 80, 600, 2) * 0.5, 3) * (0.6 + 0.4 * np.sin(2 * math.pi * 14 * t)) * sobe_e_some(n, 0.8, 1.2) * 0.07, 0.0)
    poe(x, _baque(70, 28, 0.6, 0.8, 2.6), 0.48)
    poe(x, _explosao(rng, 0.5, 60), 0.48)
    return reverb(x, 0.7, 0.35)


def gengar_preparo(rng, v):
    """Gengar (Preparo): a risadinha "gen-gar" na sombra e o arrepio."""
    x = _z(1.4)
    for k in range(4):
        n = n_de(0.09)
        poe(x, satura(seno(varre(380, 300, n), n), 3) * env(n, 0.005, 0.07) * 0.035, 0.1 + 0.12 * k)
    n = n_de(1.0)
    poe(x, seno(varre(1200, 1000, n), n) * (0.5 + 0.5 * np.sin(2 * math.pi * 7 * _t(n))) * sobe_e_some(n, 0.5, 1.2) * 0.01, 0.0)
    return reverb(x, 0.6, 0.3)


def comedor_de_sonhos(rng, v):
    """Gengar: a bolha de sonho sendo sugada (o "slurp" que sobe) e a vida voltando."""
    x = _z(2.2)
    poe(x, _sino(rng, 1568, 0.6, 0.03, CRISTAL), 0.05)
    n = n_de(0.45)
    poe(x, (passa(rosa(rng, n), 500, 3000, 2) * 0.4 + seno(varre(300, 900, n), n) * 0.5) * env(n, 0.3, 0.1) * 0.12, 0.35)
    poe(x, _piu(400, 200, 0.12, 0.04), 0.78)
    poe(x, _acorde((233, 277, 349), 0.7, 0.03, 0.05, 0.5), 0.82)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Tenshinhan

def taiyoken_tenshinhan(rng, v):
    """Tenshinhan: "Taiyoken!" — o clarão do Sol (o brilho estridente que estoura)."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, seno(varre(400, 2400, n), n) * env(n, 0.25, 0.03) * 0.04, 0.0)
    poe(x, passa(rosa(rng, n_de(0.6)), 3000, 12000, 2) * env(n_de(0.6), 0.005, 0.5) * 0.35, 0.25)
    poe(x, _acorde((1047, 1319, 1568, 2093), 0.8, 0.03, 0.005, 0.7), 0.25)
    return reverb(x, 0.7, 0.35)


def golpe_de_quatro_bracos(rng, v):
    """Tenshinhan: os quatro braços golpeando juntos (o impacto quádruplo)."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 300, 3000, 0.8, 1.3, 0.5), 0.05)
    for k in range(4):
        poe(x, _baque(130 + 15 * k, 55, 0.25, 0.45), 0.28 + 0.02 * k)
    poe(x, estalo(rng, n_de(0.05), 800, 4000, 0.012), 0.28)
    return reverb(x, 0.5, 0.25)


def tenshinhan_preparo(rng, v):
    """Tenshinhan (Preparo): as mãos em triângulo juntando o ki (o zumbido que pulsa)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(varre(110, 160, n), n) + seno(varre(220, 320, n), n) * 0.4, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.7, 1.2) * 0.05, 0.0)
    poe(x, graos(rng, n, 20, 0.0, 0.95, 2000, 7000, 0.003) * 0.25, 0.0)
    return reverb(x, 0.6, 0.3)


def kikoho(rng, v):
    """Tenshinhan: "Kikoho!" — o triângulo de energia caindo e o buraco no chão."""
    x = _z(2.4)
    n = n_de(0.35)
    poe(x, satura(seno(varre(300, 120, n), n), 3) * env(n, 0.02, 0.3) * 0.06, 0.0)
    poe(x, _whoosh(rng, 0.35, 150, 3000, 0.9, 1.3, 0.55), 0.0)
    poe(x, _baque(45, 18, 1.0, 1.0, 3.2), 0.33)
    poe(x, _explosao(rng, 1.0, 45), 0.33)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Deidara

def aranhas_de_argila(rng, v):
    """Deidara: as aranhinhas de argila correndo (os passinhos) e grudando no rival."""
    x = _z(2.0)
    q = np.random.default_rng(4)
    for k in range(24):
        poe(x, estalo(rng, n_de(0.012), 2000, 7000, 0.003) * 0.35, 0.02 * k + q.uniform(0, 0.01))
    poe(x, _baque(300, 200, 0.05, 0.25), 0.48)
    for k in range(4):
        n = n_de(0.05)
        poe(x, seno(1500, n) * env(n, 0.003, 0.04) * 0.025, 0.55 + 0.1 * k)
    return reverb(x, 0.4, 0.2)


def passaro_de_argila(rng, v):
    """Deidara: o pássaro batendo as asas e as bombinhas caindo e estourando."""
    x = _z(2.2)
    for k in range(5):
        poe(x, _sopro(rng, 0.12, 300, 2500, 0.15, 0.3), 0.12 * k)
    for k in range(3):
        poe(x, _piu(1400, 500, 0.18, 0.02), 0.15 + 0.2 * k)
        poe(x, _baque(100, 40, 0.3, 0.6), 0.35 + 0.2 * k)
        poe(x, _explosao(rng, 0.35, 70), 0.35 + 0.2 * k)
    return reverb(x, 0.6, 0.3)


def deidara_preparo(rng, v):
    """Deidara (Preparo): as bocas das mãos mastigando a argila (o "nhac-nhac" molhado)."""
    x = _z(1.4)
    for k in range(8):
        n = n_de(0.06)
        poe(x, passa(rosa(rng, n), 300, 2000, 2) * env(n, 0.005, 0.05) * 0.3, 0.12 * k)
    return reverb(x, 0.4, 0.2)


def c4_karura(rng, v):
    """Deidara: o silêncio das minibombas espalhando e o "Katsu!" estourando por dentro."""
    x = _z(2.4)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 5000, 12000, 2) * sobe_e_some(n, 0.5, 1.2) * 0.12, 0.0)
    n = n_de(0.12)
    poe(x, satura(seno(varre(500, 400, n), n), 3) * env(n, 0.005, 0.1) * 0.05, 0.48)
    q = np.random.default_rng(6)
    for k in range(10):
        poe(x, estalo(rng, n_de(0.04), 500, 5000, 0.01) * 1.0, 0.55 + q.uniform(0, 0.25))
    poe(x, _baque(70, 30, 0.6, 0.8, 2.6), 0.58)
    poe(x, _explosao(rng, 0.6, 60), 0.6)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Violeta

def campo_de_forca(rng, v):
    """Violeta: o campo de força abrindo (o zumbido roxo que se estende) sobre o trio."""
    x = _z(2.1)
    n = n_de(0.8)
    t = _t(n)
    poe(x, (seno(varre(150, 300, n), n) + seno(varre(225, 450, n), n) * 0.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 12 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.04, 0.0)
    poe(x, _sino(rng, 784, 0.8, 0.035, METAL), 0.3)
    poe(x, _brilho(rng, 0.6, 1175, 0.025, CRISTAL), 0.35)
    return reverb(x, 0.7, 0.35)


def invisibilidade_violeta(rng, v):
    """Violeta: sumindo (o brilho que se desfaz em pontinhos)."""
    x = _z(1.9)
    n = n_de(0.6)
    poe(x, seno(varre(1200, 300, n), n) * env(n, 0.02, 0.5) * 0.02, 0.1)
    poe(x, graos(rng, n, 40, 0.0, 0.9, 3000, 10000, 0.003)[::-1] * 0.3, 0.1)
    return reverb(x, 0.6, 0.3)


def violeta_preparo(rng, v):
    """Violeta (Preparo): as mãos formando a esfera (o zumbido crescendo em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(varre(200, 400, n), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.7, 1.2) * 0.03, 0.0)
    return reverb(x, 0.5, 0.25)


def esfera_de_forca(rng, v):
    """Violeta: a esfera rolando (o ronco abafado) e fechando o rival dentro."""
    x = _z(2.0)
    n = n_de(0.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 100, 800, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 10 * t) ** 2) * env(n, 0.02, 0.3) * 0.35, 0.0)
    poe(x, _baque(110, 45, 0.4, 0.7), 0.38)
    poe(x, _sino(rng, 523, 0.8, 0.04, METAL), 0.4)
    n = n_de(0.5)
    poe(x, seno(220, n) * env(n, 0.05, 0.4) * 0.025, 0.45)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "beijo-venenoso": (beijo_venenoso, "Hera Venenosa: o beijo venenoso"),
    "raizes-estranguladoras": (raizes_estranguladoras, "Hera Venenosa: as raízes estranguladoras"),
    "hera-preparo": (hera_preparo, "Hera Venenosa: a flor abrindo (Preparo)"),
    "jardim-toxico": (jardim_toxico, "Hera Venenosa: o jardim tóxico"),
    "rajada-congelante": (rajada_congelante, "Homem de Gelo: a rajada congelante"),
    "muralha-de-gelo": (muralha_de_gelo, "Homem de Gelo: a muralha de gelo"),
    "iceman-preparo": (iceman_preparo, "Homem de Gelo: o corpo virando gelo (Preparo)"),
    "era-glacial": (era_glacial, "Homem de Gelo: a era glacial"),
    "hipnose-gengar": (hipnose_gengar, "Gengar: a hipnose"),
    "bola-sombria": (bola_sombria, "Gengar: a bola sombria"),
    "gengar-preparo": (gengar_preparo, "Gengar: a risadinha na sombra (Preparo)"),
    "comedor-de-sonhos": (comedor_de_sonhos, "Gengar: o comedor de sonhos"),
    "taiyoken-tenshinhan": (taiyoken_tenshinhan, "Tenshinhan: Taiyoken"),
    "golpe-de-quatro-bracos": (golpe_de_quatro_bracos, "Tenshinhan: o golpe de quatro braços"),
    "tenshinhan-preparo": (tenshinhan_preparo, "Tenshinhan: as mãos em triângulo (Preparo)"),
    "kikoho": (kikoho, "Tenshinhan: Kikoho"),
    "aranhas-de-argila": (aranhas_de_argila, "Deidara: as aranhas de argila"),
    "passaro-de-argila": (passaro_de_argila, "Deidara: o pássaro de argila"),
    "deidara-preparo": (deidara_preparo, "Deidara: a argila sendo moldada (Preparo)"),
    "c4-karura": (c4_karura, "Deidara: C4 Karura"),
    "campo-de-forca": (campo_de_forca, "Violeta: o campo de força"),
    "invisibilidade-violeta": (invisibilidade_violeta, "Violeta: a invisibilidade"),
    "violeta-preparo": (violeta_preparo, "Violeta: as mãos formando a esfera (Preparo)"),
    "esfera-de-forca": (esfera_de_forca, "Violeta: a esfera de força"),
}
