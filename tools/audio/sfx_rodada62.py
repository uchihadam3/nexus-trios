"""Os sons da rodada 62 das habilidades próprias (veja tools/vfx/familias_v2/rodada62.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _sss(rng, seg, g=0.25):
    """O chiado do Creeper ("sssss")."""
    n = n_de(seg)
    return passa(rosa(rng, n), 4000, 11000, 2) * sobe_e_some(n, 0.7, 1.2) * g


def _quadrada(f, seg, g=0.03):
    """A onda quadrada dos jogos antigos (o som de 8 bits)."""
    n = n_de(seg)
    return np.sign(seno(f, n)) * env(n, 0.002, seg * 0.8) * g


def _waka(rng, vezes, g=0.03):
    x = _z(0.12 * vezes + 0.1)
    for k in range(vezes):
        n = n_de(0.1)
        f = varre(450, 250, n) if k % 2 == 0 else varre(250, 450, n)
        poe(x, np.sign(seno(f, n)) * env(n, 0.003, 0.08) * g, 0.12 * k)
    return x


def _tiro(rng, g=0.5, grave=160):
    n = n_de(0.35)
    return (satura(passa(rosa(rng, n), 300, 8000, 2) * env(n, 0.001, 0.06), 3) * 0.8 + satura(seno(varre(grave, 60, n), n), 2) * env(n, 0.001, 0.1) * 0.5) * g


# ------------------------------------------------------------------ Creeper

def chiado_creeper(rng, v):
    """Creeper: "SSSSSS..." e a marca piscando no rival."""
    x = _z(2.0)
    poe(x, _sss(rng, 0.8, 0.3), 0.0)
    for k in range(4):
        poe(x, _piu(1200, 1200, 0.05, 0.01), 0.6 + 0.12 * k)
    return reverb(x, 0.6, 0.3)


def camuflagem_verde(rng, v):
    """Creeper: o mato balançando e o Creeper sumindo."""
    x = _z(1.9)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 7 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.15, 0.05)
    poe(x, _piu(900, 400, 0.4, 0.012), 0.4)
    return reverb(x, 0.6, 0.3)


def creeper_preparo(rng, v):
    """Creeper (Preparo): o chiado crescendo sem parar (em laço)."""
    x = _z(1.4)
    poe(x, _sss(rng, 1.2, 0.22), 0.0)
    return reverb(x, 0.5, 0.25)


def explosao_creeper(rng, v):
    """Creeper: o chiado, o silêncio e a EXPLOSÃO de blocos."""
    x = _z(2.7)
    poe(x, _sss(rng, 0.28, 0.25), 0.0)
    poe(x, _baque(28, 10, 1.6, 1.0, 4.0), 0.27)
    poe(x, _explosao(rng, 1.0, 30), 0.27)
    for k in range(10):
        poe(x, _quadrada(200 + 30 * k, 0.04, 0.012), 0.35 + 0.04 * k)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Pac-Man

def comer_pacman(rng, v):
    """Pac-Man: "waka-waka-waka" e a mordida."""
    x = _z(1.9)
    poe(x, _waka(rng, 4, 0.03), 0.0)
    poe(x, _quadrada(180, 0.12, 0.04), 0.35)
    for k in range(4):
        poe(x, _quadrada(600 + 150 * k, 0.05, 0.02), 0.5 + 0.06 * k)
    return reverb(x, 0.4, 0.2)


def pilula_de_poder(rng, v):
    """Pac-Man: a pílula de poder (a sirene subindo e descendo dos fantasmas azuis)."""
    x = _z(2.0)
    poe(x, _quadrada(300, 0.12, 0.04), 0.0)
    n = n_de(1.2)
    t = _t(n)
    f = 400 + 250 * np.abs(np.sin(2 * math.pi * 3 * t))
    poe(x, np.sign(np.sin(2 * math.pi * np.cumsum(f) / 48000)) * sobe_e_some(n, 0.3, 1.2) * 0.025, 0.2)
    return reverb(x, 0.4, 0.2)


def pacman_preparo(rng, v):
    """Pac-Man (Preparo): comendo as bolinhas no labirinto ("waka-waka" em laço)."""
    x = _z(1.4)
    poe(x, _waka(rng, 10, 0.022), 0.05)
    return reverb(x, 0.4, 0.2)


def comer_fantasma(rng, v):
    """Pac-Man: o "nhac" no fantasma e os olhinhos voltando para casa ("piu-piu")."""
    x = _z(2.0)
    poe(x, _waka(rng, 3, 0.03), 0.05)
    n = n_de(0.3)
    poe(x, np.sign(seno(varre(200, 1200, n), n)) * env(n, 0.005, 0.25) * 0.03, 0.42)
    for k in range(5):
        poe(x, _quadrada(900 + 100 * k, 0.04, 0.012), 0.75 + 0.05 * k)
    return reverb(x, 0.4, 0.2)


# ------------------------------------------------------------------ Crash

def giro_crash(rng, v):
    """Crash: o giro ("vrrrrr") batendo em todos e as caixas quebrando."""
    x = _z(2.1)
    n = n_de(0.9)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 18 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.3, 0.0)
    for k in range(3):
        poe(x, _baque(140, 70, 0.15, 0.5), 0.15 + 0.2 * k)
        poe(x, estalo(rng, n_de(0.04), 500, 4000, 0.01) * 0.4, 0.15 + 0.2 * k)
    return reverb(x, 0.5, 0.25)


def aku_aku_mascara(rng, v):
    """Crash: "OOGA BOOGA!" — a máscara Aku Aku chegando com o tambor tribal."""
    x = _z(2.0)
    for k in range(4):
        poe(x, _baque(110 if k % 2 == 0 else 160, 70, 0.12, 0.5, 1.8), 0.05 + 0.12 * k)
    n = n_de(0.5)
    t = _t(n)
    poe(x, satura(seno(varre(180, 120, n), n) * (1 + 0.3 * np.sin(2 * math.pi * 6 * t)), 3) * env(n, 0.05, 0.3) * 0.03, 0.55)
    poe(x, _brilho(rng, 0.5, 1319, 0.025, CRISTAL), 0.6)
    return reverb(x, 0.7, 0.35)


def caixa_de_nitro(rng, v):
    """Crash: a caixa de Nitro quicando ("tic-tic") e a explosão verde."""
    x = _z(2.2)
    for k in range(3):
        poe(x, _baque(300, 200, 0.06, 0.25, 1.5), 0.1 + 0.1 * k)
    poe(x, _baque(40, 15, 1.0, 1.0, 3.4), 0.4)
    poe(x, _explosao(rng, 0.8, 40), 0.4)
    for k in range(3):
        poe(x, _piu(1500, 1500, 0.04, 0.012), 0.65 + 0.12 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Arthur Morgan

def dead_eye_arthur(rng, v):
    """Arthur Morgan: o Dead Eye (o tempo desacelerando, o coração batendo e as marcas)."""
    x = _z(2.2)
    n = n_de(0.6)
    poe(x, seno(varre(600, 150, n), n) * env(n, 0.05, 0.5) * 0.03, 0.0)
    for k in range(3):
        poe(x, _baque(55, 35, 0.15, 0.4), 0.15 + 0.35 * k)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 2000, 6000, 0.004) * 0.5, 0.2 + 0.1 * k)
    return reverb(x, 1.0, 0.5)


def laco_arthur(rng, v):
    """Arthur Morgan: o laço girando ("vum-vum"), voando e apertando o rival."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 300, 2500, 0.6, 1.3, 0.35), 0.0 + 0.1 * k)
    poe(x, _whoosh(rng, 0.3, 400, 3000, 0.7, 1.3, 0.4), 0.25)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 300, 2000, 2) * env(n, 0.01, 0.2) * 0.2, 0.5)
    return reverb(x, 0.6, 0.3)


def arthur_preparo(rng, v):
    """Arthur Morgan (Preparo): o cão do revólver armando e o tambor girando (em laço)."""
    x = _z(1.4)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.005) * 0.4, 0.1 + 0.45 * k)
        for j in range(3):
            poe(x, estalo(rng, n_de(0.015), 3000, 8000, 0.002) * 0.15, 0.2 + 0.45 * k + 0.04 * j)
    return reverb(x, 0.6, 0.3)


def revolver_arthur(rng, v):
    """Arthur Morgan: os quatro tiros do revólver em sequência e o eco do faroeste."""
    x = _z(2.4)
    for k in range(4):
        poe(x, _tiro(rng, 0.5, 170), 0.22 + 0.1 * k)
    return reverb(x, 1.2, 0.55)


# ------------------------------------------------------------------ Ellie

def canivete_ellie(rng, v):
    """Ellie: o canivete abrindo ("click") e os três cortes rápidos."""
    x = _z(1.9)
    poe(x, estalo(rng, n_de(0.03), 2000, 7000, 0.005) * 0.5, 0.05)
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 1500, 8000, 0.6, 1.3, 0.35), 0.15 + 0.15 * k)
        poe(x, _baque(150, 80, 0.1, 0.3), 0.22 + 0.15 * k)
    return reverb(x, 0.5, 0.25)


def furtividade_ellie(rng, v):
    """Ellie: o silêncio, a respiração contida e o mato mexendo (o modo escuta)."""
    x = _z(2.0)
    poe(x, _sopro(rng, 0.6, 300, 1500, 0.08, 0.4), 0.05)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.06, 0.2)
    for k in range(3):
        n = n_de(0.4)
        poe(x, seno(220, n) * env(n, 0.1, 0.25) * 0.012, 0.3 + 0.12 * k)
    return reverb(x, 0.8, 0.4)


def ellie_preparo(rng, v):
    """Ellie (Preparo): a corda do arco esticando (o rangido baixo em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(130 + 40 * t, n) * (0.5 + 0.5 * np.sin(2 * math.pi * 12 * t)) * sobe_e_some(n, 0.7, 1.2) * 0.012, 0.1)
    return reverb(x, 0.5, 0.25)


def arco_silencioso(rng, v):
    """Ellie: a corda soltando ("tunk") e a flecha acertando em silêncio."""
    x = _z(1.9)
    n = n_de(0.15)
    poe(x, seno(varre(160, 120, n), n) * env(n, 0.001, 0.12) * 0.05, 0.28)
    poe(x, _whoosh(rng, 0.2, 2000, 7000, 0.8, 1.3, 0.25), 0.3)
    poe(x, _baque(140, 70, 0.15, 0.4), 0.5)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Sans

def ossos_sans(rng, v):
    """Sans: os ossos subindo do chão em fileira ("tok-tok-tok") e o tema dele."""
    x = _z(2.1)
    for k in range(7):
        poe(x, _baque(500, 300, 0.05, 0.25, 1.5), 0.1 + 0.08 * k)
    for k, f in enumerate((294, 294, 587, 440)):
        poe(x, _quadrada(f, 0.1, 0.015), 0.1 + 0.13 * k)
    return reverb(x, 0.5, 0.25)


def desviar_sans(rng, v):
    """Sans: o deslize para o lado ("vush") e o golpe errando."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.2, 800, 4000, 0.6, 1.3, 0.35), 0.1)
    poe(x, _whoosh(rng, 0.25, 200, 2000, 0.6, 1.3, 0.4), 0.3)
    poe(x, _quadrada(587, 0.08, 0.012), 0.55)
    poe(x, _quadrada(440, 0.12, 0.012), 0.64)
    return reverb(x, 0.5, 0.25)


def sans_preparo(rng, v):
    """Sans (Preparo): o olho azul acendendo e o Gaster Blaster carregando (em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, seno(220 + 200 * t, n) * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(n, 0.7, 1.2) * 0.015, 0.0)
    poe(x, _quadrada(587, 0.08, 0.01), 0.2)
    return reverb(x, 0.6, 0.3)


def gaster_blaster(rng, v):
    """Sans: as caveiras abrindo a boca e o raio do Gaster Blaster em todos."""
    x = _z(2.6)
    for k in range(2):
        n = n_de(0.3)
        poe(x, seno(varre(200, 900, n), n) * env(n, 0.25, 0.05) * 0.02, 0.0 + 0.08 * k)
    n = n_de(0.9)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 300, 6000, 2) + seno(110, n) * 0.5, 3) * (0.8 + 0.2 * np.sin(2 * math.pi * 30 * t)) * env(n, 0.03, 0.5) * 0.35, 0.42)
    poe(x, _baque(40, 15, 0.8, 0.8, 3.0), 0.45)
    return reverb(x, 0.9, 0.45)


SONS: dict = {
    "chiado-creeper": (chiado_creeper, "Creeper: chiado"),
    "camuflagem-verde": (camuflagem_verde, "Creeper: camuflagem verde"),
    "creeper-preparo": (creeper_preparo, "Creeper: o chiado crescendo (Preparo)"),
    "explosao-creeper": (explosao_creeper, "Creeper: explosão"),
    "comer-pacman": (comer_pacman, "Pac-Man: comer"),
    "pilula-de-poder": (pilula_de_poder, "Pac-Man: pílula de poder"),
    "pacman-preparo": (pacman_preparo, "Pac-Man: o labirinto (Preparo)"),
    "comer-fantasma": (comer_fantasma, "Pac-Man: comer fantasma"),
    "giro-crash": (giro_crash, "Crash: giro"),
    "aku-aku-mascara": (aku_aku_mascara, "Crash: Aku Aku"),
    "caixa-de-nitro": (caixa_de_nitro, "Crash: caixa de nitro"),
    "dead-eye-arthur": (dead_eye_arthur, "Arthur Morgan: Dead Eye"),
    "laco-arthur": (laco_arthur, "Arthur Morgan: laço"),
    "arthur-preparo": (arthur_preparo, "Arthur Morgan: o revólver armando (Preparo)"),
    "revolver-arthur": (revolver_arthur, "Arthur Morgan: revólver"),
    "canivete-ellie": (canivete_ellie, "Ellie: canivete"),
    "furtividade-ellie": (furtividade_ellie, "Ellie: furtividade"),
    "ellie-preparo": (ellie_preparo, "Ellie: o arco esticando (Preparo)"),
    "arco-silencioso": (arco_silencioso, "Ellie: arco silencioso"),
    "ossos-sans": (ossos_sans, "Sans: ossos"),
    "desviar-sans": (desviar_sans, "Sans: desviar"),
    "sans-preparo": (sans_preparo, "Sans: o olho azul (Preparo)"),
    "gaster-blaster": (gaster_blaster, "Sans: Gaster Blaster"),
}
