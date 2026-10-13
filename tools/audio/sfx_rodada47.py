"""Os sons da rodada 47 das habilidades próprias (veja tools/vfx/familias_v2/rodada47.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _choque(rng, seg, g=0.3, f0=1500, f1=7000):
    n = n_de(seg)
    t = _t(n)
    corte = (np.sin(2 * math.pi * 55 * t) > 0.2).astype(float)
    return satura(passa(rosa(rng, n), f0, f1, 2) * corte, 3) * env(n, 0.005, seg * 0.5) * g


def _agua(rng, seg, g=0.3, f0=300, f1=4000):
    """A água correndo (o chiado ondulado)."""
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), f0, f1, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 5 * t + np.sin(2 * math.pi * 1.3 * t) * 2)) * sobe_e_some(n, 0.3, 1.2) * g


def _squish(rng, seg=0.2, g=0.3):
    """A carne molhada se mexendo."""
    n = n_de(seg)
    t = _t(n)
    return satura(passa(rosa(rng, n), 150, 1500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 18 * t) ** 2), 2) * env(n, 0.02, seg * 0.7) * g


def _fogo(rng, seg, g=0.3):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 200, 3000, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 11 * t)) * sobe_e_some(n, 0.2, 1.2) * g


# ------------------------------------------------------------------ Nêmesis

def tentaculo_do_nemesis(rng, v):
    """Nêmesis: o tentáculo saindo (o estalo molhado) e apertando o rival."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.3, 200, 2500, 0.8, 1.3, 0.4), 0.0)
    poe(x, _squish(rng, 0.25, 0.4), 0.25)
    for k in range(3):
        poe(x, _squish(rng, 0.15, 0.25), 0.45 + 0.12 * k)
    poe(x, _baque(140, 60, 0.25, 0.45), 0.3)
    return reverb(x, 0.6, 0.3)


def lanca_foguetes(rng, v):
    """Nêmesis: o disparo do lança-foguetes, o foguete chiando e o bipe da carga."""
    x = _z(2.1)
    poe(x, _baque(80, 40, 0.3, 0.7, 2.5), 0.05)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 800, 6000, 2) * env(n, 0.02, 0.3) * 0.4, 0.06)
    poe(x, _explosao(rng, 0.4, 80), 0.36)
    for k in range(4):
        poe(x, _piu(1500, 1500, 0.06, 0.022), 0.6 + 0.14 * k)
    return reverb(x, 0.6, 0.3)


def nemesis_preparo(rng, v):
    """Nêmesis (Preparo): o rosnado "S.T.A.R.S." e os passos pesados (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, satura(seno(varre(70, 60, n), n) + passa(rosa(rng, n), 60, 500, 2) * 0.8, 4) * sobe_e_some(n, 0.4, 1.2) * 0.05, 0.0)
    for k in range(2):
        poe(x, _baque(50, 25, 0.35, 0.9, 2.8), 0.5 * k)
    return reverb(x, 0.6, 0.3)


def perseguicao_sem_fim(rng, v):
    """Nêmesis: os passos chegando cada vez mais perto e o soco enorme."""
    x = _z(2.3)
    for k in range(4):
        poe(x, _baque(55, 25, 0.3, 0.5 + 0.12 * k, 2.6), 0.05 + 0.1 * k)
    poe(x, _whoosh(rng, 0.15, 200, 2500, 0.8, 1.3, 0.45), 0.38)
    poe(x, _baque(38, 15, 1.2, 1.0, 3.4), 0.52)
    poe(x, _explosao(rng, 0.7, 40), 0.52)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Zeus

def raio_do_olimpo(rng, v):
    """Zeus: o raio arremessado (o zumbido) e o estalo do trovão no rival."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, seno(varre(400, 1200, n), n) * env(n, 0.25, 0.05) * 0.02, 0.0)
    poe(x, _whoosh(rng, 0.25, 1500, 8000, 0.8, 1.3, 0.35), 0.05)
    poe(x, _choque(rng, 0.35, 0.35), 0.28)
    poe(x, _trovao(rng, 0.9, 0.7), 0.3)
    return reverb(x, 0.7, 0.35)


def egide(rng, v):
    """Zeus: a Égide surgindo (o gongo de bronze) e as cúpulas fechando no trio."""
    x = _z(2.2)
    poe(x, _sino(rng, 196, 1.2, 0.06, METAL), 0.0)
    poe(x, _sino(rng, 294, 1.0, 0.03, METAL), 0.02)
    for k in range(3):
        n = n_de(0.3)
        poe(x, seno(varre(250 + 50 * k, 500 + 50 * k, n), n) * env(n, 0.2, 0.08) * 0.02, 0.25 + 0.05 * k)
    poe(x, _brilho(rng, 0.6, 1568, 0.015, CRISTAL), 0.5)
    return reverb(x, 0.8, 0.4)


def zeus_preparo(rng, v):
    """Zeus (Preparo): a tempestade se juntando — o trovão distante e o vento (em laço)."""
    x = _z(1.4)
    poe(x, _sopro(rng, 1.0, 100, 800, 0.15, 0.5), 0.0)
    poe(x, _trovao(rng, 0.8, 0.25), 0.3)
    poe(x, _choque(rng, 0.06, 0.1), 0.3)
    return reverb(x, 0.8, 0.4)


def furia_de_zeus(rng, v):
    """Zeus: os raios caindo seguidos e o trovão enorme."""
    x = _z(2.4)
    poe(x, _sopro(rng, 0.4, 100, 1000, 0.2, 0.6), 0.0)
    for k in range(4):
        poe(x, _choque(rng, 0.15, 0.32, 1000, 8000), 0.25 + 0.1 * k)
        poe(x, _baque(80, 30, 0.3, 0.6, 2.6), 0.25 + 0.1 * k)
    poe(x, _trovao(rng, 1.6, 1.0), 0.3)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Poseidon

def tridente_de_poseidon(rng, v):
    """Poseidon: a estocada do tridente e o jato de água espirrando."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 600, 5000, 0.85, 1.3, 0.45), 0.0)
    poe(x, _agua(rng, 0.4, 0.4, 600, 6000), 0.1)
    poe(x, _baque(130, 55, 0.3, 0.6), 0.27)
    poe(x, _sino(rng, 1047, 0.4, 0.02, METAL), 0.27)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * env(n, 0.01, 0.35) * 0.3, 0.3)
    return reverb(x, 0.6, 0.3)


def correnteza(rng, v):
    """Poseidon: a correnteza passando e os redemoinhos girando nos rivais."""
    x = _z(2.2)
    poe(x, _agua(rng, 0.8, 0.45), 0.0)
    for k in range(3):
        n = n_de(0.5)
        t = _t(n)
        poe(x, passa(rosa(rng, n), 200, 2000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * (8 + 2 * k) * t) ** 2) * env(n, 0.1, 0.35) * 0.3, 0.35 + 0.06 * k)
    return reverb(x, 0.7, 0.35)


def poseidon_preparo(rng, v):
    """Poseidon (Preparo): a água subindo em espiral (o borbulhar em laço)."""
    x = _z(1.4)
    poe(x, _agua(rng, 1.0, 0.18, 400, 3000), 0.0)
    q = np.random.default_rng(7)
    for k in range(6):
        f = q.uniform(400, 900)
        poe(x, _piu(f, f * 1.7, 0.04, 0.012), 0.15 * k)
    return reverb(x, 0.6, 0.3)


def maremoto(rng, v):
    """Poseidon: a onda gigante se erguendo (o rugido do mar) e quebrando em todos."""
    x = _z(2.5)
    n = n_de(0.7)
    poe(x, passa(rosa(rng, n), 80, 1500, 2) * sobe_e_some(n, 0.8, 1.5) * 0.5, 0.0)
    poe(x, _baque(45, 18, 1.0, 1.0, 3.0), 0.6)
    n2 = n_de(1.0)
    poe(x, passa(rosa(rng, n2), 300, 7000, 2) * env(n2, 0.02, 0.8) * 0.55, 0.6)
    poe(x, _agua(rng, 0.8, 0.3, 1000, 6000), 0.75)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Atena

def escudo_de_atena(rng, v):
    """Atena: os escudos de bronze surgindo um por um ("tóin") e o brilho."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _sino(rng, 523 + 66 * k, 0.6, 0.04, METAL), 0.05 + 0.07 * k)
        poe(x, _baque(200, 120, 0.1, 0.25), 0.05 + 0.07 * k)
    poe(x, _brilho(rng, 0.6, 1760, 0.015, CRISTAL), 0.4)
    return reverb(x, 0.7, 0.35)


def lanca_da_sabedoria(rng, v):
    """Atena: a estocada da lança dourada e as folhas voando."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.22, 1500, 9000, 0.85, 1.3, 0.45), 0.0)
    poe(x, _baque(140, 60, 0.3, 0.55), 0.22)
    poe(x, _sino(rng, 1319, 0.5, 0.025, METAL), 0.22)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * env(n, 0.05, 0.4) * 0.12, 0.28)
    return reverb(x, 0.5, 0.25)


def estrategia_divina(rng, v):
    """Atena: o pio da coruja, as asas abrindo e o acorde da estratégia ligando o trio."""
    x = _z(2.2)
    for k in range(2):
        n = n_de(0.2)
        poe(x, seno(varre(520, 440, n), n) * env(n, 0.03, 0.15) * 0.025, 0.05 + 0.25 * k)
    poe(x, _sopro(rng, 0.3, 300, 2000, 0.2, 0.4), 0.15)
    poe(x, _acorde((440, 554, 659, 880), 0.9, 0.022), 0.4)
    for k in range(3):
        poe(x, _sino(rng, 1319 + 220 * k, 0.3, 0.012, CRISTAL), 0.55 + 0.05 * k)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Ares

def espada_da_guerra(rng, v):
    """Ares: o corte pesado da espada larga e as brasas estalando."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.32, 400, 5000, 0.85, 1.3, 0.55), 0.0)
    poe(x, _baque(100, 40, 0.5, 0.8, 2.6), 0.3)
    poe(x, _sino(rng, 880, 0.5, 0.03, METAL), 0.3)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.02), 1500, 6000, 0.004) * 0.3, 0.35 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


def grito_de_batalha_ares(rng, v):
    """Ares: o grito de guerra em coro e os tambores."""
    x = _z(2.2)
    n = n_de(0.8)
    coro = sum(satura(seno(varre(f, f * 0.95, n), n), 3) for f in (110, 138, 165)) + passa(rosa(rng, n), 200, 2000, 2) * 0.6
    poe(x, coro * env(n, 0.05, 0.4) * 0.03, 0.05)
    for k in range(3):
        poe(x, _baque(70, 35, 0.25, 0.7, 2.4), 0.3 + 0.15 * k)
    return reverb(x, 0.8, 0.4)


def ares_preparo(rng, v):
    """Ares (Preparo): a espada arrastando no chão (o raspar com faíscas em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, satura(passa(rosa(rng, n), 1500, 6000, 2), 2) * sobe_e_some(n, 0.3, 1.2) * 0.15, 0.0)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.015), 3000, 9000, 0.003) * 0.3, 0.15 * k + 0.05)
    return reverb(x, 0.5, 0.25)


def massacre_de_ares(rng, v):
    """Ares: o salto, a espada cravando no chão e a terra rachando."""
    x = _z(2.4)
    poe(x, _whoosh(rng, 0.35, 200, 3000, 0.8, 1.3, 0.45), 0.0)
    poe(x, _baque(40, 15, 1.2, 1.0, 3.4), 0.35)
    poe(x, _explosao(rng, 0.8, 40), 0.35)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.05), 150, 2500, 0.015) * 0.6, 0.38 + 0.05 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Apolo

def flecha_de_sol(rng, v):
    """Apolo: a corda do arco, a flecha de sol zunindo e o clarão."""
    x = _z(1.9)
    n = n_de(0.2)
    poe(x, seno(varre(220, 190, n), n) * env(n, 0.002, 0.18) * 0.04, 0.05)
    poe(x, _whoosh(rng, 0.25, 2000, 10000, 0.8, 1.3, 0.35), 0.08)
    poe(x, _acorde((784, 988, 1175, 1568), 0.6, 0.025), 0.3)
    poe(x, _baque(150, 70, 0.2, 0.45), 0.3)
    return reverb(x, 0.6, 0.3)


def cura_de_apolo(rng, v):
    """Apolo: a lira tocando e a luz morna descendo."""
    x = _z(2.2)
    for k, f in enumerate((523, 659, 784, 1047, 784, 1047)):
        poe(x, _sino(rng, f, 0.6, 0.025, SINO), 0.12 * k)
    poe(x, _brilho(rng, 0.9, 1319, 0.015, CRISTAL), 0.3)
    return reverb(x, 0.8, 0.4)


def apolo_preparo(rng, v):
    """Apolo (Preparo): o sol nascendo (o coro luminoso em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(392, n) + seno(587, n) * 0.6 + seno(784, n) * 0.3) * (0.7 + 0.3 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.02, 0.0)
    return reverb(x, 0.8, 0.4)


def carruagem_do_sol(rng, v):
    """Apolo: o sol em chamas passando ("vruuum") e o fogo chovendo nos rivais."""
    x = _z(2.4)
    poe(x, _fogo(rng, 0.8, 0.45), 0.0)
    poe(x, _whoosh(rng, 0.7, 150, 3000, 0.5, 1.3, 0.5), 0.0)
    for k in range(3):
        poe(x, _baque(110, 45, 0.3, 0.55), 0.45 + 0.08 * k)
    poe(x, _fogo(rng, 0.6, 0.3), 0.55)
    return reverb(x, 0.7, 0.35)


SONS: dict = {
    "tentaculo-do-nemesis": (tentaculo_do_nemesis, "Nêmesis: o tentáculo"),
    "lanca-foguetes": (lanca_foguetes, "Nêmesis: o lança-foguetes"),
    "nemesis-preparo": (nemesis_preparo, "Nêmesis: o rosnado e os passos (Preparo)"),
    "perseguicao-sem-fim": (perseguicao_sem_fim, "Nêmesis: a perseguição sem fim"),
    "raio-do-olimpo": (raio_do_olimpo, "Zeus: o raio do Olimpo"),
    "egide": (egide, "Zeus: a Égide"),
    "zeus-preparo": (zeus_preparo, "Zeus: a tempestade se juntando (Preparo)"),
    "furia-de-zeus": (furia_de_zeus, "Zeus: a fúria de Zeus"),
    "tridente-de-poseidon": (tridente_de_poseidon, "Poseidon: o tridente"),
    "correnteza": (correnteza, "Poseidon: a correnteza"),
    "poseidon-preparo": (poseidon_preparo, "Poseidon: a água subindo (Preparo)"),
    "maremoto": (maremoto, "Poseidon: o maremoto"),
    "escudo-de-atena": (escudo_de_atena, "Atena: o escudo de Atena"),
    "lanca-da-sabedoria": (lanca_da_sabedoria, "Atena: a lança da sabedoria"),
    "estrategia-divina": (estrategia_divina, "Atena: a estratégia divina"),
    "espada-da-guerra": (espada_da_guerra, "Ares: a espada da guerra"),
    "grito-de-batalha-ares": (grito_de_batalha_ares, "Ares: o grito de batalha"),
    "ares-preparo": (ares_preparo, "Ares: a espada arrastando (Preparo)"),
    "massacre-de-ares": (massacre_de_ares, "Ares: o massacre"),
    "flecha-de-sol": (flecha_de_sol, "Apolo: a flecha de sol"),
    "cura-de-apolo": (cura_de_apolo, "Apolo: a cura de Apolo"),
    "apolo-preparo": (apolo_preparo, "Apolo: o sol nascendo (Preparo)"),
    "carruagem-do-sol": (carruagem_do_sol, "Apolo: a carruagem do sol"),
}
