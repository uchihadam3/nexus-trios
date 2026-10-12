"""Os sons da rodada 13 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_n.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada08 import _corrente
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def outro_ghostface(rng, v):
    """Ghostface: a voz no telefone (o tom distorcido), e as duas facas."""
    x = _z(1.9)
    n = n_de(0.5)
    t = _t(n)
    poe(x, satura(seno(varre(150, 120, n) * (1 + 0.1 * np.sin(2 * math.pi * 50 * t)), n), 4) * env(n, 0.03, 0.35) * 0.05, 0.05)
    for k in range(2):
        poe(x, _whoosh(rng, 0.15, 2500, 10000, 0.5, 1.4, 0.6), 0.75 + 0.06 * k)
        poe(x, _sino(rng, 3200 + 300 * k, 0.3, 0.04, METAL), 0.8 + 0.06 * k)
    return reverb(x, 0.6, 0.3)


def corte_fundo(rng, v):
    """Leatherface: a motosserra roncando alto e o corte."""
    x = _z(2.0)
    n = n_de(1.6)
    t = _t(n)
    f = 55 + 25 * np.clip(t / 0.4, 0, 1) + 6 * np.sin(2 * math.pi * 9 * t)
    serra = np.sign(np.sin(2 * math.pi * np.cumsum(f) / 44100))
    poe(x, satura(serra * 0.5 + passa(rosa(rng, n), 600, 6000, 2) * 0.6, 3) * env(n, 0.02, 1.0, segura=0.5) * 0.12, 0.0)
    m = n_de(0.4)
    poe(x, passa(rosa(rng, m), 200, 1500, 2) * env(m, 0.01, 0.25) * 0.4, 0.7)
    return reverb(x, 0.4, 0.2)


def caixa(rng, v):
    """Pinhead: a caixa girando (os cliques do mecanismo), abrindo (o sino) e as correntes saindo."""
    x = _z(2.2)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.005) * 0.5, 0.04 * k)
    poe(x, _sino(rng, 220, 1.4, 0.15, SINO), 0.55)
    for k in range(3):
        poe(x, _corrente(rng, 0.4, 8, 0.3), 0.75 + 0.08 * k)
    return reverb(x, 0.8, 0.4)


def sete_dias(rng, v):
    """Samara: o chiado da TV, o anel (o tom grave) e o rangido quando ela sai da tela."""
    x = _z(2.2)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 1500, 9000, 2) * env(n, 0.01, 0.6, segura=0.4) * 0.3, 0.0)
    poe(x, (seno(98, n_de(1.0)) + seno(104, n_de(1.0))) * env(n_de(1.0), 0.05, 0.6) * 0.08, 0.7)
    m = n_de(0.8)
    t = _t(m)
    poe(x, satura(seno(varre(180, 120, m) * (1 + 0.15 * np.sin(2 * math.pi * 45 * t)), m), 3) * env(m, 0.05, 0.5) * 0.04, 1.2)
    return reverb(x, 0.8, 0.4)


def atras(rng, v):
    """Valak: o silêncio, o sussurro atrás e o grito de susto."""
    x = _z(2.0)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * sobe_e_some(n, 0.6, 1.3) * 0.15, 0.0)
    m = n_de(0.6)
    t = _t(m)
    poe(x, satura(seno(varre(1200, 700, m) * (1 + 0.05 * np.sin(2 * math.pi * 30 * t)), m) + passa(rosa(rng, m), 1000, 5000, 2) * 0.6, 3) * env(m, 0.005, 0.4) * 0.05, 0.85)
    poe(x, _baque(80, 30, 0.4, 0.6, 2.4), 0.85)
    return reverb(x, 0.8, 0.4)


def nevoa(rng, v):
    """Drácula: a névoa subindo e os morcegos batendo as asas e guinchando."""
    x = _z(2.0)
    n = n_de(1.4)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * sobe_e_some(n, 0.4, 1.2) * 0.3, 0.0)
    q = np.random.default_rng(5)
    for k in range(10):
        poe(x, passa(rosa(rng, n_de(0.05)), 1000, 4000, 2) * env(n_de(0.05), 0.003, 0.03) * 0.3, 0.3 + q.uniform(0, 0.8))
    for k in range(5):
        poe(x, _piu(5000 + 500 * k, 6500, 0.05, 0.02), 0.4 + 0.15 * k)
    return reverb(x, 0.7, 0.35)


def cria(rng, v):
    """Xenomorfo: o ovo abrindo (o som molhado) e o ataque da mandíbula interna (o estalo e o sibilo)."""
    x = _z(1.9)
    for k in range(4):
        n = n_de(0.2)
        poe(x, passa(rosa(rng, n), 200, 1500, 2) * env(n, 0.02, 0.12) * 0.35, 0.3 + 0.07 * k)
    poe(x, estalo(rng, n_de(0.04), 1000, 5000, 0.008), 0.85)
    poe(x, _baque(200, 100, 0.15, 0.5), 0.85)
    m = n_de(0.6)
    poe(x, passa(rosa(rng, m), 3000, 9000, 2) * sobe_e_some(m, 0.1, 1.4) * 0.3, 0.9)
    return reverb(x, 0.6, 0.3)


def trofeu(rng, v):
    """Predador: os estalos da camuflagem e a mira de três pontos travando."""
    x = _z(1.9)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.03), 600, 3000, 0.01) * 0.4, 0.04 * k)
    n = n_de(0.8)
    t = _t(n)
    poe(x, seno(1800 * (1 + 0.02 * np.sin(2 * math.pi * 10 * t)), n) * env(n, 0.02, 0.6) * 0.03, 0.3)
    for k in range(3):
        poe(x, seno(2400, n_de(0.05)) * env(n_de(0.05), 0.003, 0.04) * 0.04, 1.0 + 0.08 * k)
    return reverb(x, 0.5, 0.25)


def estrangulamento(rng, v):
    """Darth Vader: a respiração mecânica e o estrangulamento (o tom que aperta)."""
    x = _z(2.2)
    for k in range(2):
        n = n_de(0.5)
        poe(x, passa(rosa(rng, n), 300, 2000, 2) * sobe_e_some(n, 0.4, 1.3) * 0.3, 0.05 + 0.6 * k)
    m = n_de(1.0)
    t = _t(m)
    poe(x, satura(seno(varre(120, 200, m), m), 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 6 * t)) * env(m, 0.1, 0.6) * 0.05, 0.5)
    poe(x, (seno(98, m) + seno(117, m) * 0.6) * env(m, 0.1, 0.6) * 0.05, 0.5)
    return reverb(x, 0.6, 0.3)


def equilibrio(rng, v):
    """Yoda: o sabre girando (o zumbido que roda) e o equilíbrio da Força (o acorde calmo)."""
    x = _z(2.1)
    n = n_de(0.7)
    t = _t(n)
    poe(x, (satura(seno(110 + 30 * np.sin(2 * math.pi * 8 * t), n), 2) * 0.08 + passa(rosa(rng, n), 800, 3000, 2) * 0.1) * env(n, 0.02, 0.5), 0.0)
    poe(x, _acorde((294, 370, 440, 587), 1.3, 0.04, 0.2, 0.8), 0.6)
    return reverb(x, 0.8, 0.4)


def nova_esperanca(rng, v):
    """Luke: os dois sóis (o tema que sobe) e o sabre acendendo."""
    x = _z(2.2)
    for k, f in enumerate((392, 523, 587, 659, 784)):
        n = n_de(0.25 if k < 4 else 0.7)
        poe(x, (seno(f, n) + seno(f * 1.5, n) * 0.3) * env(n, 0.02, 0.2 if k < 4 else 0.5) * 0.045, 0.1 * k)
    m = n_de(0.6)
    poe(x, (satura(seno(varre(60, 110, m), m), 2) * 0.1 + passa(rosa(rng, m), 1000, 4000, 2) * 0.1) * env(m, 0.005, 0.4), 0.85)
    return reverb(x, 0.7, 0.35)


def relampago_cadeia(rng, v):
    """Palpatine: o relâmpago da Força saindo das mãos e pulando de um rival a outro."""
    x = _z(2.0)
    n = n_de(1.3)
    poe(x, graos(rng, n, 200, 0.0, 0.95, 2000, 10000, 0.0012) * 0.5, 0.0)
    poe(x, satura(seno(80, n) + seno(160, n) * 0.5, 2.5) * env(n, 0.02, 0.8, segura=0.3) * 0.08, 0.0)
    for k in range(3):
        poe(x, _trovao(rng, 0.4, 0.3), 0.2 + 0.25 * k)
    return reverb(x, 0.6, 0.3)


def desviou(rng, v):
    """Neo: o tempo desacelerando (o som esticando) e as balas passando (os assobios lentos)."""
    x = _z(2.1)
    n = n_de(1.5)
    t = _t(n)
    poe(x, seno(varre(400, 120, n, 0.6), n) * sobe_e_some(n, 0.3, 1.2) * 0.05, 0.0)
    for k in range(3):
        m = n_de(0.6)
        poe(x, (passa(rosa(rng, m), 400, 2000, 2) * 0.3 + seno(varre(800, 400, m), m) * 0.03) * sobe_e_some(m, 0.5, 1.2), 0.2 + 0.2 * k)
    return reverb(x, 0.7, 0.35)


def mais_smith(rng, v):
    """Agente Smith: "Mais um" — as cópias surgindo (o eco que se multiplica)."""
    x = _z(2.1)
    for k in range(4):
        n = n_de(0.3)
        poe(x, satura(seno(varre(160, 150, n), n), 1.4) * env(n, 0.02, 0.2) * (0.06 - 0.01 * k), 0.1 + 0.25 * k)
        poe(x, _baque(300, 150, 0.08, 0.15), 0.75 + 0.12 * k)
    return reverb(x, 0.6, 0.3)


def recarregou(rng, v):
    """John Wick: o pente entrando (o clique duplo) e os três tiros precisos."""
    x = _z(1.9)
    poe(x, estalo(rng, n_de(0.04), 1200, 4000, 0.006), 0.2)
    poe(x, estalo(rng, n_de(0.04), 1800, 6000, 0.006), 0.32)
    for k in range(3):
        n = n_de(0.25)
        poe(x, satura(passa(rosa(rng, n), 300, 8000, 2) * env(n, 0.0005, 0.05), 2.5) * 0.7, 0.65 + 0.22 * k)
        poe(x, _baque(170, 80, 0.2, 0.3), 0.65 + 0.22 * k)
        poe(x, _sino(rng, 4000, 0.15, 0.02, METAL), 0.75 + 0.22 * k)
    return reverb(x, 0.4, 0.2)


def exterminador(rng, v):
    """T-800: o olho ligando (o zumbido eletrônico) e o alvo travado."""
    x = _z(2.0)
    n = n_de(0.6)
    poe(x, seno(varre(200, 900, n), n) * env(n, 0.02, 0.4) * 0.05, 0.0)
    m = n_de(1.2)
    t = _t(m)
    poe(x, _quadrada(120, m) * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * t)) * env(m, 0.02, 0.8) * 0.015, 0.4)
    for k in range(2):
        poe(x, seno(1500, n_de(0.08)) * env(n_de(0.08), 0.003, 0.06) * 0.05, 0.9 + 0.12 * k)
    return reverb(x, 0.4, 0.2)


def corpo_metal(rng, v):
    """RoboCop: os passos de metal (o servo e o baque) e o visor varrendo."""
    x = _z(2.0)
    for k in range(2):
        n = n_de(0.3)
        poe(x, seno(varre(300, 500, n), n) * env(n, 0.01, 0.2) * 0.04, 0.05 + 0.4 * k)
        poe(x, _baque(110, 55, 0.3, 0.6, 2.2), 0.3 + 0.4 * k)
        poe(x, _sino(rng, 600, 0.3, 0.05, METAL), 0.3 + 0.4 * k)
    m = n_de(0.6)
    poe(x, seno(varre(800, 1600, m), m) * sobe_e_some(m, 0.5, 1.2) * 0.03, 1.0)
    return reverb(x, 0.4, 0.2)


def desarmado(rng, v):
    """Indiana Jones: o chicote estalando, enrolando e arrancando a arma, e o tema de aventura."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.3, 500, 4000, 0.8, 1.4, 0.4), 0.0)
    poe(x, estalo(rng, n_de(0.05), 2000, 9000, 0.008) * 1.2, 0.3)
    poe(x, _whoosh(rng, 0.25, 600, 3000, 0.6, 1.4, 0.35), 0.45)
    for k, f in enumerate((330, 349, 392, 523)):
        n = n_de(0.15 if k < 3 else 0.5)
        poe(x, (seno(f, n) + seno(f * 2, n) * 0.3) * env(n, 0.01, 0.12 if k < 3 else 0.4) * 0.045, 0.9 + 0.12 * k)
    return reverb(x, 0.5, 0.25)


def parlay(rng, v):
    """Jack Sparrow: "Parlay!" (o tom esperto), a bússola girando e as moedas."""
    x = _z(2.0)
    poe(x, _piu(400, 600, 0.15, 0.05), 0.0)
    poe(x, _piu(600, 450, 0.2, 0.05), 0.15)
    n = n_de(0.7)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2000, 6000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 15 * t) ** 2) * env(n, 0.01, 0.5) * 0.2, 0.3)
    for k in range(6):
        poe(x, _sino(rng, 2600 + 200 * (k % 3), 0.25, 0.03, METAL), 0.9 + 0.06 * k)
    return reverb(x, 0.5, 0.25)


def golpe_voltou(rng, v):
    """Harry Potter: a proteção da mãe (o acorde dourado) segurando e devolvendo o feitiço."""
    x = _z(2.0)
    poe(x, _acorde((392, 494, 587, 784), 1.2, 0.045, 0.02, 0.7), 0.0)
    n = n_de(0.4)
    poe(x, (seno(varre(1200, 900, n), n) * 0.04 + passa(rosa(rng, n), 1500, 6000, 2) * 0.2) * env(n, 0.01, 0.3), 0.35)
    poe(x, _baque(200, 100, 0.2, 0.4), 0.82)
    m = n_de(0.4)
    poe(x, (seno(varre(900, 1300, m), m) * 0.04 + passa(rosa(rng, m), 1500, 6000, 2) * 0.2) * env(m, 0.01, 0.3), 0.85)
    return reverb(x, 0.7, 0.35)


def horcrux(rng, v):
    """Voldemort: a Horcrux rachando (o estalo) e o grito da alma escapando."""
    x = _z(2.2)
    poe(x, estalo(rng, n_de(0.06), 1000, 7000, 0.015), 0.55)
    poe(x, _sino(rng, 1200, 0.5, 0.06, METAL), 0.55)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(varre(900, 300, n) * (1 + 0.05 * np.sin(2 * math.pi * 12 * t)), n), 2) * env(n, 0.02, 0.6) * 0.04, 0.6)
    poe(x, passa(rosa(rng, n), 200, 2000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.3, 0.6)
    return reverb(x, 0.8, 0.4)


def o_branco(rng, v):
    """Gandalf: o cajado batendo no chão e a luz branca (o coro enorme)."""
    x = _z(2.4)
    poe(x, _baque(120, 60, 0.4, 0.8, 2.0), 0.3)
    poe(x, _acorde((262, 330, 392, 523, 659, 784), 1.8, 0.06, 0.1, 1.0), 0.35)
    poe(x, _brilho(rng, 1.0, 2093, 0.05, CRISTAL), 0.4)
    poe(x, _sopro(rng, 1.4, 2000, 8000, 0.12, 0.3), 0.4)
    return reverb(x, 0.9, 0.45)


SONS: dict = {
    "mu-outro-ghostface": (outro_ghostface, "Ghostface: o outro Ghostface"),
    "mu-corte-fundo": (corte_fundo, "Leatherface: a motosserra"),
    "mu-caixa": (caixa, "Pinhead: a caixa se abre"),
    "mu-sete-dias": (sete_dias, "Samara: sete dias"),
    "mu-atras": (atras, "Valak: atrás de você"),
    "mu-nevoa": (nevoa, "Drácula: a névoa"),
    "mu-cria": (cria, "Xenomorfo: a cria"),
    "mu-trofeu": (trofeu, "Predador: a mira"),
    "mu-estrangulamento": (estrangulamento, "Darth Vader: o estrangulamento"),
    "mu-equilibrio": (equilibrio, "Yoda: o equilíbrio"),
    "mu-nova-esperanca": (nova_esperanca, "Luke: a nova esperança"),
    "mu-relampago-cadeia": (relampago_cadeia, "Palpatine: o relâmpago"),
    "mu-desviou": (desviou, "Neo: desviou"),
    "mu-mais-smith": (mais_smith, "Agente Smith: mais um"),
    "mu-recarregou": (recarregou, "John Wick: recarregou"),
    "mu-exterminador": (exterminador, "T-800: o exterminador"),
    "mu-corpo-metal": (corpo_metal, "RoboCop: o corpo de metal"),
    "mu-desarmado": (desarmado, "Indiana Jones: o chicote"),
    "mu-parlay": (parlay, "Jack Sparrow: Parlay"),
    "mu-golpe-voltou": (golpe_voltou, "Harry Potter: a proteção"),
    "mu-horcrux": (horcrux, "Voldemort: a Horcrux"),
    "mu-o-branco": (o_branco, "Gandalf: o Branco"),
}
