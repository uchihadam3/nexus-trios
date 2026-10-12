"""Os sons da rodada 33 das habilidades próprias (veja tools/vfx/familias_v2/rodada33.py)."""
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


def _estica(rng, seg, f0, f1, g=0.04):
    """O som de borracha esticando (o "boing" que escorrega no tom)."""
    n = n_de(seg)
    t = _t(n)
    return seno(varre(f0, f1, n), n) * (1 + 0.5 * np.sin(2 * math.pi * 22 * t)) * env(n, 0.01, seg * 0.7) * g


def _gelo(rng, n_cristais=6, g=0.03):
    """Os cristais de gelo estalando (os "tinc" agudos)."""
    x = _z(0.6)
    q = np.random.default_rng(9)
    for k in range(n_cristais):
        poe(x, _sino(rng, q.uniform(2500, 4500), 0.2, g, CRISTAL), 0.06 * k)
        poe(x, estalo(rng, n_de(0.02), 3000, 9000, 0.004) * 0.4, 0.06 * k)
    return x


# ------------------------------------------------------------------ Sr. Incrível

def forca_bruta(rng, v):
    """Sr. Incrível: as mãos apertando (o esforço) e o metal amassando."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.3, 200, 2000, 0.8, 1.3, 0.4), 0.0)
    poe(x, _baque(110, 50, 0.4, 0.8, 2.4), 0.33)
    n = n_de(0.5)
    poe(x, satura(passa(rosa(rng, n), 300, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 18 * _t(n)) ** 2), 3) * env(n, 0.02, 0.45) * 0.25, 0.38)
    poe(x, _sino(rng, 220, 0.6, 0.04, METAL), 0.4)
    return reverb(x, 0.5, 0.25)


def segurar_o_impacto(rng, v):
    """Sr. Incrível: o corpo firme (o grunhido) e os golpes batendo e voltando."""
    x = _z(2.1)
    n = n_de(0.4)
    poe(x, satura(seno(varre(110, 90, n), n) + passa(rosa(rng, n), 100, 1000, 2) * 0.5, 3) * env(n, 0.05, 0.3) * 0.06, 0.0)
    for k in range(3):
        poe(x, _baque(140, 70, 0.2, 0.55), 0.53 + 0.1 * k)
        poe(x, _sino(rng, 523, 0.3, 0.025, METAL), 0.53 + 0.1 * k)
    poe(x, _acorde((196, 247, 294), 0.8, 0.03, 0.05, 0.6), 0.3)
    return reverb(x, 0.6, 0.3)


def incrivel_preparo(rng, v):
    """Sr. Incrível (Preparo): os punhos fechados e o tema dos heróis (os metais graves)."""
    x = _z(1.4)
    for k, f in enumerate((147, 147, 175, 196)):
        n = n_de(0.2)
        poe(x, satura(seno(f, n) + seno(f * 2, n) * 0.4, 2) * env(n, 0.01, 0.17) * 0.05, 0.22 * k)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 80, 600, 2) * sobe_e_some(n, 0.7, 1.2) * 0.15, 0.0)
    return reverb(x, 0.5, 0.25)


def golpe_do_incrivel(rng, v):
    """Sr. Incrível: o punho gigante descendo e o chão tremendo."""
    x = _z(2.3)
    poe(x, _whoosh(rng, 0.35, 120, 2000, 0.9, 1.3, 0.55), 0.0)
    poe(x, _baque(45, 18, 1.0, 1.0, 3.2), 0.3)
    poe(x, _explosao(rng, 0.9, 45), 0.3)
    poe(x, _acorde((147, 196, 233), 0.8, 0.04, 0.02, 0.6), 0.35)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Mulher-Elástica

def alcance_elastico(rng, v):
    """Mulher-Elástica: o braço esticando (o "boing" comprido) e o escudo no aliado."""
    x = _z(1.9)
    poe(x, _estica(rng, 0.4, 200, 600, 0.045), 0.0)
    poe(x, _estica(rng, 0.25, 600, 250, 0.035), 0.65)
    poe(x, _brilho(rng, 0.6, 1175, 0.03, CRISTAL), 0.35)
    poe(x, _sino(rng, 880, 0.5, 0.03, SINO), 0.35)
    return reverb(x, 0.5, 0.25)


def escudo_flexivel(rng, v):
    """Mulher-Elástica: a borracha abrindo como paraquedas e os golpes quicando nela."""
    x = _z(2.0)
    poe(x, _estica(rng, 0.35, 150, 400, 0.05), 0.0)
    for k in range(4):
        poe(x, _estica(rng, 0.12, 300, 500, 0.03), 0.53 + 0.1 * k)
        poe(x, _baque(200, 120, 0.06, 0.2), 0.53 + 0.1 * k)
    return reverb(x, 0.4, 0.2)


def elastica_preparo(rng, v):
    """Mulher-Elástica (Preparo): os braços enrolando como mola."""
    x = _z(1.4)
    for k in range(4):
        poe(x, _estica(rng, 0.2, 250 + 30 * k, 350 + 40 * k, 0.03), 0.25 * k)
    return reverb(x, 0.4, 0.2)


def resgate_elastico(rng, v):
    """Mulher-Elástica: o braço que estica, agarra (o "plec") e puxa de volta, e o acorde de cura."""
    x = _z(2.0)
    poe(x, _estica(rng, 0.3, 200, 650, 0.045), 0.0)
    poe(x, estalo(rng, n_de(0.04), 1000, 4000, 0.008), 0.32)
    poe(x, _estica(rng, 0.25, 650, 200, 0.045), 0.35)
    poe(x, _acorde((392, 494, 587, 784), 1.0, 0.035, 0.05, 0.8), 0.6)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Gelado

def rampa_de_gelo(rng, v):
    """Gelado: a rampa congelando no ar, o deslize do patim e o impacto."""
    x = _z(1.9)
    poe(x, _gelo(rng, 6, 0.025), 0.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 3000, 10000, 2) * env(n, 0.05, 0.3) * 0.3, 0.05)
    poe(x, _baque(140, 60, 0.3, 0.6), 0.4)
    poe(x, _sino(rng, 3136, 0.4, 0.03, CRISTAL), 0.4)
    return reverb(x, 0.6, 0.3)


def parede_congelada(rng, v):
    """Gelado: a parede de gelo subindo do chão (o rachar e os cristais)."""
    x = _z(2.0)
    n = n_de(0.4)
    poe(x, satura(passa(rosa(rng, n), 200, 3000, 2), 2) * env(n, 0.02, 0.35) * 0.3, 0.05)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.006) * 0.6, 0.05 + 0.04 * k)
    poe(x, _gelo(rng, 6, 0.025), 0.3)
    poe(x, _baque(90, 40, 0.4, 0.6), 0.1)
    return reverb(x, 0.6, 0.3)


def frozone_preparo(rng, v):
    """Gelado (Preparo): o frio nas mãos (o sopro gelado e os cristais girando)."""
    x = _z(1.4)
    poe(x, _sopro(rng, 1.0, 1500, 7000, 0.15, 0.5), 0.0)
    poe(x, graos(rng, n_de(1.0), 25, 0.0, 0.95, 3000, 9000, 0.003) * 0.3, 0.0)
    return reverb(x, 0.6, 0.3)


def cade_meu_supertraje(rng, v):
    """Gelado: "Cadê meu supertraje?!" — a nevasca uivando e os rivais congelando."""
    x = _z(2.3)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.4, 0.0)
    poe(x, seno(varre(700, 500, n), n) * sobe_e_some(n, 0.4, 1.2) * 0.015, 0.0)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.06), 1000, 6000, 0.01) * 0.7, 0.5 + 0.05 * k)
        poe(x, _sino(rng, 2637 + 200 * k, 0.5, 0.025, CRISTAL), 0.5 + 0.05 * k)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Korra

def dobra_de_fogo(rng, v):
    """Korra: os chutes de fogo em arco (o "fuuum" em sequência)."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.3, 300, 3000, 0.6, 1.3, 0.4), 0.05 + 0.13 * k)
        poe(x, _fogo(rng, 0.4, 0.25, 0.2), 0.05 + 0.13 * k)
        poe(x, _baque(140, 70, 0.15, 0.35), 0.38 + 0.1 * k)
    return reverb(x, 0.5, 0.25)


def dobra_de_terra(rng, v):
    """Korra: as colunas de pedra subindo do chão e a rocha lançada."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _baque(80 + 15 * k, 40, 0.3, 0.6, 2.4), 0.05 + 0.07 * k)
        poe(x, satura(passa(rosa(rng, n_de(0.15)), 100, 1500, 2), 2) * env(n_de(0.15), 0.005, 0.12) * 0.35, 0.05 + 0.07 * k)
    poe(x, _whoosh(rng, 0.25, 150, 1500, 0.8, 1.3, 0.4), 0.3)
    poe(x, _baque(70, 30, 0.6, 0.9, 2.8), 0.55)
    q = np.random.default_rng(4)
    for k in range(5):
        poe(x, _baque(q.uniform(180, 300), 100, 0.06, 0.2), 0.6 + q.uniform(0, 0.3))
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Zuko

def chicote_de_fogo(rng, v):
    """Zuko: o chicote de fogo ondulando e o estalo."""
    x = _z(1.8)
    n = n_de(0.4)
    poe(x, _fogo(rng, 0.4, 0.3, 0.6), 0.0)
    poe(x, _whoosh(rng, 0.35, 400, 4000, 0.7, 1.3, 0.35), 0.0)
    poe(x, estalo(rng, n_de(0.04), 1500, 7000, 0.006) * 1.0, 0.38)
    poe(x, _baque(150, 70, 0.2, 0.45), 0.4)
    return reverb(x, 0.4, 0.2)


def redirecionar_relampago(rng, v):
    """Zuko: o raio chegando, o zumbido passando pelo corpo e o raio saindo de volta."""
    x = _z(2.0)
    poe(x, _trovao(rng, 0.35, 0.35), 0.0)
    n = n_de(0.3)
    t = _t(n)
    poe(x, seno(varre(200, 500, n), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 60 * t)) * env(n, 0.03, 0.2) * 0.04, 0.2)
    poe(x, _trovao(rng, 0.5, 0.5), 0.45)
    poe(x, _baque(120, 50, 0.3, 0.6), 0.5)
    return reverb(x, 0.6, 0.3)


def zuko_preparo(rng, v):
    """Zuko (Preparo): as duas espadas dao cruzadas (o raspar do metal em laço)."""
    x = _z(1.4)
    for k in range(2):
        n = n_de(0.35)
        poe(x, passa(rosa(rng, n), 3000, 10000, 2) * env(n, 0.05, 0.25) * 0.15, 0.1 + 0.5 * k)
        poe(x, _sino(rng, 2349, 0.4, 0.02, METAL), 0.3 + 0.5 * k)
    return reverb(x, 0.5, 0.25)


def dois_espadachins(rng, v):
    """Zuko: as duas espadas cortando em X e as faíscas."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.15, 2500, 11000, 0.8, 1.3, 0.5), 0.05)
    poe(x, _whoosh(rng, 0.15, 2500, 11000, 0.8, 1.3, 0.5), 0.12)
    poe(x, _sino(rng, 2093, 0.5, 0.05, METAL), 0.3)
    poe(x, _sino(rng, 2489, 0.5, 0.04, METAL), 0.33)
    poe(x, _baque(130, 55, 0.3, 0.6), 0.32)
    poe(x, graos(rng, n_de(0.4), 20, 0.0, 0.8, 3000, 9000, 0.003) * 0.35, 0.35)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Azula

def relampago_de_azula(rng, v):
    """Azula: o relâmpago saindo dos dedos (o estalo seco e o trovão)."""
    x = _z(2.0)
    n = n_de(0.2)
    poe(x, seno(varre(400, 2000, n), n) * env(n, 0.15, 0.03) * 0.04, 0.0)
    poe(x, estalo(rng, n_de(0.05), 2000, 9000, 0.006) * 1.2, 0.17)
    poe(x, _trovao(rng, 0.8, 0.6), 0.17)
    return reverb(x, 0.6, 0.3)


def azula_preparo(rng, v):
    """Azula (Preparo): a chama azul girando nos dedos e os estalos elétricos."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, _fogo(rng, 1.0, 0.18, 0.5) * 0.8, 0.0)
    for k in range(10):
        poe(x, estalo(rng, n_de(0.015), 3000, 9000, 0.003) * 0.4, 0.09 * k)
    poe(x, seno(varre(600, 900, n), n) * sobe_e_some(n, 0.7, 1.2) * 0.015, 0.0)
    return reverb(x, 0.5, 0.25)


def precisao_cruel(rng, v):
    """Azula: a linha de fogo azul num instante (o silvo fino) e a explosão num ponto só."""
    x = _z(2.0)
    poe(x, _piu(3000, 5000, 0.2, 0.025), 0.0)
    poe(x, _whoosh(rng, 0.2, 3000, 12000, 0.8, 1.3, 0.4), 0.05)
    poe(x, _baque(90, 35, 0.6, 0.9, 2.8), 0.25)
    poe(x, _explosao(rng, 0.6, 70), 0.25)
    poe(x, _fogo(rng, 0.6, 0.25, 0.1), 0.28)
    poe(x, _brilho(rng, 0.5, 1568, 0.025, CRISTAL), 0.3)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "forca-bruta": (forca_bruta, "Sr. Incrível: a força bruta"),
    "segurar-o-impacto": (segurar_o_impacto, "Sr. Incrível: segurar o impacto"),
    "incrivel-preparo": (incrivel_preparo, "Sr. Incrível: os punhos (Preparo)"),
    "golpe-do-incrivel": (golpe_do_incrivel, "Sr. Incrível: o golpe do Incrível"),
    "alcance-elastico": (alcance_elastico, "Mulher-Elástica: o alcance elástico"),
    "escudo-flexivel": (escudo_flexivel, "Mulher-Elástica: o escudo flexível"),
    "elastica-preparo": (elastica_preparo, "Mulher-Elástica: a mola (Preparo)"),
    "resgate-elastico": (resgate_elastico, "Mulher-Elástica: o resgate"),
    "rampa-de-gelo": (rampa_de_gelo, "Gelado: a rampa de gelo"),
    "parede-congelada": (parede_congelada, "Gelado: a parede congelada"),
    "frozone-preparo": (frozone_preparo, "Gelado: as mãos geladas (Preparo)"),
    "cade-meu-supertraje": (cade_meu_supertraje, "Gelado: Cadê meu supertraje?"),
    "dobra-de-fogo": (dobra_de_fogo, "Korra: a dobra de fogo"),
    "dobra-de-terra": (dobra_de_terra, "Korra: a dobra de terra"),
    "chicote-de-fogo": (chicote_de_fogo, "Zuko: o chicote de fogo"),
    "redirecionar-relampago": (redirecionar_relampago, "Zuko: redirecionar o relâmpago"),
    "zuko-preparo": (zuko_preparo, "Zuko: as espadas cruzadas (Preparo)"),
    "dois-espadachins": (dois_espadachins, "Zuko: dois espadachins"),
    "relampago-de-azula": (relampago_de_azula, "Azula: o relâmpago"),
    "azula-preparo": (azula_preparo, "Azula: a chama azul nos dedos (Preparo)"),
    "precisao-cruel": (precisao_cruel, "Azula: a precisão cruel"),
}
