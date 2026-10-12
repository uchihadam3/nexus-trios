"""Os sons da rodada 26 das habilidades próprias (veja tools/vfx/familias_v2/rodada26.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada08 import _corrente
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _gosma(rng, seg, g=0.06):
    n = n_de(seg)
    t = _t(n)
    return seno(varre(180, 120, n) * (1 + 0.15 * np.sin(2 * math.pi * 11 * t)), n) * env(n, 0.02, seg * 0.8) * g


# ------------------------------------------------------------------ Majin Boo

def raio_de_doce(rng, v):
    """Boo: o raio da antena (o "piu" bobo que ondula) e o "plim" do doce."""
    x = _z(1.9)
    n = n_de(0.4)
    t = _t(n)
    poe(x, seno(900 * (1 + 0.2 * np.sin(2 * math.pi * 18 * t)), n) * env(n, 0.01, 0.35) * 0.04, 0.05)
    poe(x, _piu(600, 1400, 0.1, 0.05), 0.45)
    poe(x, _sino(rng, 1568, 0.4, 0.04, CRISTAL), 0.5)
    return reverb(x, 0.5, 0.25)


def absorcao_boo(rng, v):
    """Boo: a gosma rosa sugada (os sons molhados) e a força crescendo."""
    x = _z(2.0)
    for k in range(5):
        poe(x, _gosma(rng, 0.2, 0.05), 0.05 + 0.1 * k)
    n = n_de(0.7)
    poe(x, satura(seno(varre(100, 160, n), n), 2) * sobe_e_some(n, 0.6, 1.2) * 0.06, 0.4)
    for k in range(3):
        poe(x, _piu(500 + 100 * k, 800 + 100 * k, 0.05, 0.03), 0.6 + 0.08 * k)
    return reverb(x, 0.5, 0.25)


def boo_preparo(rng, v):
    """Boo (Preparo): o corpo borbulhando (as bolhas)."""
    x = _z(1.4)
    q = np.random.default_rng(3)
    for k in range(8):
        poe(x, _piu(q.uniform(300, 600), q.uniform(600, 900), 0.05, 0.03), 0.1 * k + q.uniform(0, 0.05))
    poe(x, _gosma(rng, 0.9, 0.03), 0.0)
    return reverb(x, 0.5, 0.25)


def regeneracao_total(rng, v):
    """Boo: as gotas se juntando (o som molhado ao contrário) e o soco elástico."""
    x = _z(2.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * np.linspace(0.1, 1, n) ** 2 * 0.3, 0.0)
    poe(x, _gosma(rng, 0.3, 0.06), 0.3)
    m = n_de(0.25)
    poe(x, seno(varre(200, 500, m), m) * env(m, 0.01, 0.2) * 0.05, 0.4)
    poe(x, _baque(110, 50, 0.4, 0.8, 2.6), 0.58)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Shiryu

def escudo_do_dragao(rng, v):
    """Shiryu: o escudo do dragão erguido (o metal pesado) e o golpe refletido."""
    x = _z(1.9)
    poe(x, _baque(140, 80, 0.2, 0.4), 0.1)
    poe(x, _sino(rng, 600, 1.0, 0.08, METAL), 0.1)
    poe(x, _sino(rng, 1200, 0.6, 0.04, METAL), 0.12)
    poe(x, estalo(rng, n_de(0.04), 2000, 8000, 0.006), 0.48)
    poe(x, _whoosh(rng, 0.2, 1500, 6000, 0.4, 1.4, 0.35), 0.5)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Shun

def corrente_nebular(rng, v):
    """Shun: a corrente girando em espiral e prendendo todos."""
    x = _z(2.0)
    poe(x, _corrente(rng, 0.8, 16, 0.35), 0.0)
    for k in range(3):
        poe(x, _sino(rng, 2600 + 300 * k, 0.3, 0.035, METAL), 0.5 + 0.08 * k)
    return reverb(x, 0.6, 0.3)


def tempestade_nebular(rng, v):
    """Shun: o vento rosa da Tempestade Nebular girando em volta do trio."""
    x = _z(2.1)
    n = n_de(1.3)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 5 * t) ** 2) * sobe_e_some(n, 0.4, 1.2) * 0.35, 0.0)
    poe(x, _acorde((392, 494, 587, 784), 1.0, 0.035, 0.1, 0.8), 0.3)
    return reverb(x, 0.7, 0.35)


def corrente_interceptadora(rng, v):
    """Shun: a corrente disparando reta e cortando o Preparo."""
    x = _z(1.9)
    poe(x, _corrente(rng, 0.3, 8, 0.35), 0.0)
    poe(x, _whoosh(rng, 0.2, 2000, 9000, 0.7, 1.3, 0.35), 0.0)
    poe(x, estalo(rng, n_de(0.04), 2000, 8000, 0.006), 0.28)
    poe(x, _sino(rng, 2200, 0.5, 0.05, VIDRO), 0.28)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Saga

def explosao_galactica(rng, v):
    """Saga: as galáxias girando (o coro cósmico) e a colisão enorme."""
    x = _z(2.4)
    n = n_de(0.5)
    poe(x, (seno(varre(150, 400, n), n) * 0.05 + passa(rosa(rng, n), 600, 4000, 2) * 0.15) * sobe_e_some(n, 0.9, 1.0), 0.0)
    poe(x, _explosao(rng, 1.4, 0.9), 0.42)
    poe(x, _acorde((110, 165, 220, 330, 440), 1.4, 0.05, 0.01, 1.0), 0.42)
    poe(x, _brilho(rng, 1.0, 1760, 0.04, CRISTAL), 0.5)
    return reverb(x, 0.8, 0.4)


def outra_dimensao(rng, v):
    """Saga: o espaço rasgando (o som que racha e puxa) e o rival sumindo."""
    x = _z(2.1)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 1000, 8000, 2) * env(n, 0.005, 0.3) * 0.3, 0.0)
    m = n_de(0.8)
    poe(x, seno(varre(400, 80, m, 0.7), m) * env(m, 0.02, 0.7) * 0.05, 0.25)
    poe(x, _sopro(rng, 0.7, 200, 1500, 0.3, 0.7), 0.3)
    return reverb(x, 0.9, 0.45)


def sata_imperial(rng, v):
    """Saga: o dedo apontado e o raio que domina a mente (o tom que gira)."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, (seno(varre(800, 1600, n), n) * 0.04 + passa(rosa(rng, n), 3000, 9000, 2) * 0.12) * env(n, 0.005, 0.25), 0.3)
    m = n_de(0.8)
    t = _t(m)
    poe(x, seno(500 * (1 + 0.15 * np.sin(2 * math.pi * 4 * t)), m) * env(m, 0.05, 0.6) * 0.04, 0.55)
    poe(x, _acorde((147, 175, 220), 0.7, 0.04, 0.05, 0.5), 0.55)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Camus

def po_de_diamante(rng, v):
    """Camus: o Pó de Diamante (os cristais tilintando em rajada)."""
    x = _z(1.9)
    poe(x, _sopro(rng, 0.6, 2500, 9000, 0.2, 0.3), 0.0)
    q = np.random.default_rng(4)
    for k in range(14):
        poe(x, _sino(rng, q.uniform(2500, 4500), 0.2, 0.02, CRISTAL), q.uniform(0.05, 0.6))
    poe(x, graos(rng, n_de(0.3), 30, 0.0, 0.8, 4000, 11000, 0.002) * 0.3, 0.45)
    return reverb(x, 0.7, 0.35)


def circulo_polar(rng, v):
    """Camus: os cristais fechando em anel (o gelo rangendo)."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 2500, 8000, 2) * sobe_e_some(n, 0.9, 1.0) * 0.25, 0.0)
    for k in range(6):
        poe(x, _sino(rng, 2200 + 200 * k, 0.25, 0.03, VIDRO), 0.3 + 0.03 * k)
    poe(x, _baque(200, 120, 0.15, 0.3), 0.45)
    return reverb(x, 0.6, 0.3)


def camus_preparo(rng, v):
    """Camus (Preparo): o frio girando entre as mãos (o vento gelado)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2000, 8000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.7, 1.2) * 0.2, 0.0)
    poe(x, _sino(rng, 2637, 0.4, 0.03, CRISTAL), 0.4)
    return reverb(x, 0.6, 0.3)


def aurora_de_camus(rng, v):
    """Camus: a Execução Aurora (o frio absoluto derramando) e os cristais subindo."""
    x = _z(2.3)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 1500, 9000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.35, 0.15)
    poe(x, _acorde((294, 370, 440, 587), 1.2, 0.04, 0.1, 0.9), 0.15)
    for k in range(7):
        poe(x, _sino(rng, 1800 + 250 * k, 0.4, 0.035, VIDRO), 0.5 + 0.03 * k)
        poe(x, estalo(rng, n_de(0.03), 2000, 8000, 0.005) * 0.4, 0.5 + 0.03 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Hades

def elisios(rng, v):
    """Hades: os Elísios (o coro frio e distante) e as flores."""
    x = _z(2.2)
    poe(x, _acorde((220, 277, 330, 440), 1.6, 0.04, 0.3, 1.0), 0.0)
    for k in range(5):
        poe(x, _sino(rng, 1319 + 100 * k, 0.4, 0.025, CRISTAL), 0.2 + 0.1 * k)
    for k in range(3):
        poe(x, _baque(150, 90, 0.12, 0.25), 0.5 + 0.08 * k)
    return reverb(x, 0.9, 0.45)


def sono_eterno(rng, v):
    """Hades: a névoa do sono (o sopro baixo) e a canção de ninar que some."""
    x = _z(2.2)
    poe(x, _sopro(rng, 1.2, 200, 1500, 0.25, 0.4), 0.0)
    for k, f in enumerate((392, 330, 294, 262)):
        poe(x, _sino(rng, f, 0.6, 0.035 - 0.005 * k, SINO), 0.3 + 0.2 * k)
    return reverb(x, 0.9, 0.45)


def hades_preparo(rng, v):
    """Hades (Preparo): a espada erguida e as almas gemendo."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(varre(300, 260, n) * (1 + 0.04 * np.sin(2 * math.pi * 4 * t)), n) * sobe_e_some(n, 0.5, 1.2) * 0.04, 0.0)
    poe(x, satura(seno(55, n), 2) * sobe_e_some(n, 0.6, 1.2) * 0.05, 0.0)
    return reverb(x, 0.8, 0.4)


def juizo_dos_mortos(rng, v):
    """Hades: a espada descendo, o trovão e as almas caindo."""
    x = _z(2.4)
    poe(x, _whoosh(rng, 0.25, 200, 3000, 0.9, 1.3, 0.5), 0.0)
    poe(x, _baque(55, 25, 0.8, 1.0, 3.0), 0.22)
    poe(x, _trovao(rng, 1.0, 0.5), 0.22)
    for k in range(5):
        n = n_de(0.4)
        poe(x, seno(varre(700 - 50 * k, 300, n), n) * env(n, 0.02, 0.35) * 0.025, 0.35 + 0.08 * k)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Minato

def hiraishin(rng, v):
    """Minato: o Hiraishin (o estalo de sumir e aparecer, com o raio)."""
    x = _z(1.8)
    poe(x, estalo(rng, n_de(0.04), 2000, 9000, 0.006), 0.12)
    poe(x, graos(rng, n_de(0.25), 30, 0.0, 0.9, 3000, 10000, 0.002) * 0.4, 0.15)
    poe(x, _whoosh(rng, 0.15, 3000, 12000, 0.5, 1.3, 0.35), 0.15)
    poe(x, estalo(rng, n_de(0.04), 2000, 9000, 0.006), 0.32)
    return reverb(x, 0.5, 0.25)


def marca_voadora(rng, v):
    """Minato: as três kunais cravando e o Minato aparecendo em cada uma."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.1, 2000, 9000, 0.5, 1.4, 0.25), 0.03 * k)
        poe(x, _baque(250, 140, 0.08, 0.25), 0.2 + 0.03 * k)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 2000, 9000, 0.005), 0.32 + 0.12 * k)
        poe(x, _whoosh(rng, 0.12, 1000, 6000, 0.6, 1.4, 0.35), 0.34 + 0.12 * k)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "raio-de-doce": (raio_de_doce, "Boo: o raio de doce"),
    "absorcao-boo": (absorcao_boo, "Boo: a absorção"),
    "boo-preparo": (boo_preparo, "Boo: o corpo borbulhando (Preparo)"),
    "regeneracao-total": (regeneracao_total, "Boo: a regeneração total"),
    "escudo-do-dragao": (escudo_do_dragao, "Shiryu: o escudo do dragão"),
    "corrente-nebular": (corrente_nebular, "Shun: a corrente nebular"),
    "tempestade-nebular": (tempestade_nebular, "Shun: a tempestade nebular"),
    "corrente-interceptadora": (corrente_interceptadora, "Shun: a corrente interceptadora"),
    "explosao-galactica": (explosao_galactica, "Saga: a Explosão Galáctica"),
    "outra-dimensao": (outra_dimensao, "Saga: Outra Dimensão"),
    "sata-imperial": (sata_imperial, "Saga: Satã Imperial"),
    "po-de-diamante": (po_de_diamante, "Camus: o Pó de Diamante"),
    "circulo-polar": (circulo_polar, "Camus: o Círculo Polar"),
    "camus-preparo": (camus_preparo, "Camus: o frio (Preparo)"),
    "aurora-de-camus": (aurora_de_camus, "Camus: a Execução Aurora"),
    "elisios": (elisios, "Hades: Elísios"),
    "sono-eterno": (sono_eterno, "Hades: o sono eterno"),
    "hades-preparo": (hades_preparo, "Hades: a espada (Preparo)"),
    "juizo-dos-mortos": (juizo_dos_mortos, "Hades: o juízo dos mortos"),
    "hiraishin": (hiraishin, "Minato: Hiraishin"),
    "marca-voadora": (marca_voadora, "Minato: a marca voadora"),
}
