"""Os sons da rodada 42 das habilidades próprias (veja tools/vfx/familias_v2/rodada42.py)."""
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


def _corte(rng, g=0.5):
    return _whoosh(rng, 0.12, 3000, 12000, 0.6, 1.3, g)


# ------------------------------------------------------------------ Zoro

def oni_giri(rng, v):
    """Zoro: "Oni Giri!" — as três espadas cortando juntas e o tinido."""
    x = _z(1.9)
    for k in range(3):
        poe(x, _corte(rng, 0.45), 0.08 + 0.02 * k)
    for k, f in enumerate((1760, 2093, 2349)):
        poe(x, _sino(rng, f, 0.5, 0.035, METAL), 0.3 + 0.02 * k)
    poe(x, _baque(140, 60, 0.3, 0.55), 0.3)
    return reverb(x, 0.6, 0.3)


def tatsumaki_zoro(rng, v):
    """Zoro: o tornado de cortes (o vento girando e as lâminas tinindo)."""
    x = _z(2.1)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 500, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 9 * _t(n)) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.35, 0.0)
    for k in range(6):
        poe(x, _corte(rng, 0.25), 0.2 + 0.08 * k)
        poe(x, _sino(rng, 1760 + 100 * (k % 3), 0.2, 0.015, METAL), 0.24 + 0.08 * k)
    return reverb(x, 0.6, 0.3)


def zoro_preparo(rng, v):
    """Zoro (Preparo): a aura do Asura (o zumbido grave e as lâminas vibrando em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(varre(65, 80, n), n) + seno(97, n) * 0.4, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.05, 0.0)
    for k in range(3):
        poe(x, _sino(rng, 2637, 0.3, 0.01, METAL), 0.3 * k)
    return reverb(x, 0.7, 0.35)


def asura(rng, v):
    """Zoro: "Asura!" — os nove cortes de uma vez e o silêncio antes do estrondo."""
    x = _z(2.4)
    n = n_de(0.35)
    poe(x, satura(seno(55, n), 2) * env(n, 0.1, 0.2) * 0.05, 0.0)
    for k in range(9):
        poe(x, _corte(rng, 0.25), 0.35 + 0.015 * k)
    poe(x, _baque(55, 22, 0.9, 1.0, 3.0), 0.5)
    poe(x, _explosao(rng, 0.7, 55), 0.5)
    poe(x, _sino(rng, 1760, 1.0, 0.05, METAL), 0.5)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Nami

def bola_de_trovao(rng, v):
    """Nami: a nuvenzinha crescendo (o ronco) e o raio caindo no rival."""
    x = _z(1.9)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 60, 400, 2) * sobe_e_some(n, 0.7, 1.2) * 0.3, 0.0)
    poe(x, _trovao(rng, 0.5, 0.45), 0.35)
    return reverb(x, 0.6, 0.3)


def miragem(rng, v):
    """Nami: a miragem (o ar tremendo, o som ondulado) e as cópias aparecendo."""
    x = _z(2.0)
    n = n_de(0.9)
    t = _t(n)
    poe(x, (seno(700 + 80 * np.sin(2 * math.pi * 6 * t), n) + seno(1050 + 120 * np.sin(2 * math.pi * 5 * t), n) * 0.5) * sobe_e_some(n, 0.3, 1.2) * 0.02, 0.0)
    for k in range(4):
        poe(x, _piu(900 + 100 * k, 1300 + 100 * k, 0.08, 0.02), 0.2 + 0.08 * k)
    return reverb(x, 0.7, 0.35)


def nami_preparo(rng, v):
    """Nami (Preparo): o bastão de clima girando e as bolhas de clima estalando."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 500, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * _t(n)) ** 2) * sobe_e_some(n, 0.5, 1.2) * 0.2, 0.0)
    for k in range(3):
        poe(x, _piu(600, 1000, 0.05, 0.02), 0.3 * k + 0.1)
    return reverb(x, 0.5, 0.25)


def tempo_do_trovao(rng, v):
    """Nami: "Tempo do trovão!" — a nuvem negra roncando e os raios caindo em todos."""
    x = _z(2.4)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 40, 400, 2) * sobe_e_some(n, 0.7, 1.2) * 0.45, 0.0)
    for k in range(3):
        poe(x, _trovao(rng, 0.6, 0.45), 0.35 + 0.08 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Sanji

def concasser(rng, v):
    """Sanji: "Concasser!" — o chute descendo como machado e o chão rachando."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.3, 200, 3000, 0.9, 1.3, 0.5), 0.0)
    poe(x, _baque(60, 22, 0.8, 1.0, 3.0), 0.3)
    poe(x, estalo(rng, n_de(0.08), 300, 3000, 0.02) * 0.7, 0.3)
    return reverb(x, 0.6, 0.3)


def diable_jambe(rng, v):
    """Sanji: "Diable Jambe!" — a perna girando em brasa e o chute pegando fogo."""
    x = _z(2.0)
    n = n_de(0.55)
    poe(x, passa(rosa(rng, n), 300, 4000, 2) * (0.4 + 0.6 * np.sin(2 * math.pi * 11 * _t(n)) ** 2) * env(n, 0.02, 0.4) * 0.3, 0.0)
    poe(x, _fogo(rng, 0.6, 0.25, 0.4), 0.0)
    poe(x, _baque(110, 45, 0.4, 0.8, 2.6), 0.62)
    poe(x, _fogo(rng, 0.4, 0.2, 0.1), 0.62)
    return reverb(x, 0.5, 0.25)


def sanji_preparo(rng, v):
    """Sanji (Preparo): o isqueiro, o cigarro e a chama crescendo na perna (em laço)."""
    x = _z(1.4)
    poe(x, estalo(rng, n_de(0.03), 2000, 6000, 0.005), 0.0)
    poe(x, _fogo(rng, 1.0, 0.18, 0.6), 0.05)
    return reverb(x, 0.5, 0.25)


def hell_memories(rng, v):
    """Sanji: "Hell Memories!" — as chamas do inferno explodindo em todos."""
    x = _z(2.4)
    n = n_de(0.3)
    poe(x, seno(varre(150, 500, n), n) * env(n, 0.25, 0.04) * 0.04, 0.0)
    poe(x, _baque(50, 20, 1.0, 1.0, 3.2), 0.3)
    poe(x, _explosao(rng, 0.9, 50), 0.3)
    poe(x, _fogo(rng, 1.0, 0.35, 0.15), 0.32)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Chopper

def tratamento_de_campo(rng, v):
    """Chopper: a maleta abrindo ("clic"), o curativo e a cura."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.006), 0.05)
    poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.006), 0.12)
    poe(x, passa(rosa(rng, n_de(0.2)), 2000, 7000, 2) * env(n_de(0.2), 0.01, 0.15) * 0.2, 0.35)
    poe(x, _acorde((523, 659, 784), 0.8, 0.03, 0.05, 0.6), 0.45)
    return reverb(x, 0.5, 0.25)


def rumble_ball(rng, v):
    """Chopper: a Rumble Ball engolida ("glup") e o corpo inchando de força."""
    x = _z(2.0)
    poe(x, _piu(400, 200, 0.12, 0.05), 0.25)
    n = n_de(0.5)
    poe(x, satura(seno(varre(100, 200, n), n), 2.5) * env(n, 0.2, 0.25) * 0.06, 0.32)
    poe(x, _baque(90, 40, 0.4, 0.6), 0.6)
    return reverb(x, 0.5, 0.25)


def chopper_preparo(rng, v):
    """Chopper (Preparo): o coração batendo forte com a Rumble Ball (em laço)."""
    x = _z(1.4)
    for k in range(3):
        poe(x, _baque(70, 40, 0.15, 0.4), 0.35 * k)
        poe(x, _baque(80, 45, 0.12, 0.3), 0.35 * k + 0.12)
    return reverb(x, 0.4, 0.2)


def monster_point(rng, v):
    """Chopper: o monstro gigante (o rugido) e o soco enorme."""
    x = _z(2.3)
    n = n_de(0.45)
    poe(x, satura(seno(varre(110, 75, n), n) + passa(rosa(rng, n), 80, 900, 2) * 0.6, 4) * env(n, 0.05, 0.35) * 0.07, 0.0)
    poe(x, _whoosh(rng, 0.25, 150, 2000, 0.9, 1.3, 0.5), 0.25)
    poe(x, _baque(45, 18, 1.1, 1.0, 3.2), 0.42)
    poe(x, _explosao(rng, 0.7, 45), 0.42)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Nero

def red_queen(rng, v):
    """Nero: a Red Queen acelerando ("vrum-vrum") e o corte em chamas."""
    x = _z(2.0)
    n = n_de(0.3)
    t = _t(n)
    poe(x, satura(seno(varre(80, 160, n), n) * (0.5 + 0.5 * np.sin(2 * math.pi * 25 * t)), 4) * env(n, 0.01, 0.25) * 0.06, 0.0)
    poe(x, _whoosh(rng, 0.2, 1500, 9000, 0.8, 1.3, 0.5), 0.15)
    poe(x, _fogo(rng, 0.4, 0.22, 0.2), 0.2)
    poe(x, _baque(140, 60, 0.3, 0.55), 0.38)
    return reverb(x, 0.5, 0.25)


def devil_bringer(rng, v):
    """Nero: o braço do diabo esticando (o zumbido fantasma) e puxando o rival."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, seno(varre(200, 600, n), n) * env(n, 0.02, 0.2) * 0.04, 0.0)
    poe(x, _sopro(rng, 0.3, 500, 3000, 0.15, 0.5), 0.0)
    poe(x, _baque(150, 70, 0.2, 0.45), 0.28)
    n = n_de(0.35)
    poe(x, seno(varre(600, 200, n), n) * env(n, 0.02, 0.3) * 0.04, 0.4)
    return reverb(x, 0.6, 0.3)


def nero_preparo(rng, v):
    """Nero (Preparo): a Red Queen roncando parada (o motor em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(90, n) * (0.5 + 0.5 * np.sin(2 * math.pi * 22 * t)), 4) * (0.6 + 0.4 * np.sin(2 * math.pi * 2 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.05, 0.0)
    poe(x, _fogo(rng, 1.0, 0.12, 0.5), 0.0)
    return reverb(x, 0.4, 0.2)


def showdown(rng, v):
    """Nero: os cortes e tiros da Blue Rose em sequência e o golpe final."""
    x = _z(2.3)
    for k in range(6):
        if k % 2 == 0:
            poe(x, _corte(rng, 0.35), 0.03 + 0.07 * k)
        else:
            poe(x, estalo(rng, n_de(0.04), 800, 6000, 0.01) * 1.3, 0.03 + 0.07 * k)
            poe(x, _baque(200, 100, 0.06, 0.3), 0.03 + 0.07 * k)
    poe(x, _whoosh(rng, 0.25, 800, 9000, 0.85, 1.3, 0.55), 0.5)
    poe(x, _baque(60, 24, 0.8, 1.0, 3.0), 0.6)
    poe(x, _explosao(rng, 0.6, 60), 0.6)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ L

def investigacao(rng, v):
    """L: a investigação (o tique da lupa e as pistas se ligando em notas suaves)."""
    x = _z(2.0)
    for k, f in enumerate((659, 784, 988, 1175)):
        poe(x, _sino(rng, f, 0.3, 0.02, CRISTAL), 0.4 + 0.06 * k)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 2000, 6000, 2) * env(n, 0.05, 0.4) * 0.08, 0.0)
    poe(x, _sino(rng, 1568, 0.5, 0.03, SINO), 0.65)
    return reverb(x, 0.6, 0.3)


def armadilha_logica(rng, v):
    """L: o tabuleiro se fechando (os cliques de peças) e a dúvida do rival."""
    x = _z(2.0)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.005) * 0.7, 0.06 * k)
        poe(x, _baque(400, 300, 0.03, 0.15), 0.06 * k)
    poe(x, _piu(700, 500, 0.15, 0.025), 0.55)
    poe(x, _piu(600, 750, 0.12, 0.025), 0.7)
    return reverb(x, 0.5, 0.25)


def l_preparo(rng, v):
    """L (Preparo): os cubos de açúcar empilhando (os "tic" em laço)."""
    x = _z(1.4)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.015), 3000, 8000, 0.003) * 0.6, 0.2 * k)
        poe(x, _sino(rng, 2349 + 100 * k, 0.1, 0.008, CRISTAL), 0.2 * k)
    return reverb(x, 0.4, 0.2)


def caso_resolvido(rng, v):
    """L: as pistas convergindo e o acorde de "caso resolvido"."""
    x = _z(2.2)
    for k in range(8):
        poe(x, _piu(400 + 80 * k, 600 + 80 * k, 0.06, 0.015), 0.05 + 0.04 * k)
    poe(x, _baque(110, 45, 0.4, 0.7), 0.42)
    poe(x, _acorde((294, 370, 440, 587), 1.0, 0.04, 0.02, 0.8), 0.5)
    poe(x, _sino(rng, 1175, 0.7, 0.04, SINO), 0.5)
    return reverb(x, 0.7, 0.35)


SONS: dict = {
    "oni-giri": (oni_giri, "Zoro: Oni Giri"),
    "tatsumaki-zoro": (tatsumaki_zoro, "Zoro: Tatsumaki"),
    "zoro-preparo": (zoro_preparo, "Zoro: a aura do Asura (Preparo)"),
    "asura": (asura, "Zoro: Asura"),
    "bola-de-trovao": (bola_de_trovao, "Nami: a bola de trovão"),
    "miragem": (miragem, "Nami: a miragem"),
    "nami-preparo": (nami_preparo, "Nami: o bastão de clima (Preparo)"),
    "tempo-do-trovao": (tempo_do_trovao, "Nami: o tempo do trovão"),
    "concasser": (concasser, "Sanji: Concasser"),
    "diable-jambe": (diable_jambe, "Sanji: Diable Jambe"),
    "sanji-preparo": (sanji_preparo, "Sanji: a perna pegando fogo (Preparo)"),
    "hell-memories": (hell_memories, "Sanji: Hell Memories"),
    "tratamento-de-campo": (tratamento_de_campo, "Chopper: o tratamento de campo"),
    "rumble-ball": (rumble_ball, "Chopper: a Rumble Ball"),
    "chopper-preparo": (chopper_preparo, "Chopper: o coração forte (Preparo)"),
    "monster-point": (monster_point, "Chopper: Monster Point"),
    "red-queen": (red_queen, "Nero: Red Queen"),
    "devil-bringer": (devil_bringer, "Nero: Devil Bringer"),
    "nero-preparo": (nero_preparo, "Nero: a Red Queen roncando (Preparo)"),
    "showdown": (showdown, "Nero: Showdown"),
    "investigacao": (investigacao, "L: a investigação"),
    "armadilha-logica": (armadilha_logica, "L: a armadilha lógica"),
    "l-preparo": (l_preparo, "L: os cubos de açúcar (Preparo)"),
    "caso-resolvido": (caso_resolvido, "L: caso resolvido"),
}
