"""Os sons da rodada 44 das habilidades próprias (veja tools/vfx/familias_v2/rodada44.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _estrelinhas(rng, x, em, n=3):
    for k in range(n):
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.02, CRISTAL), em + 0.07 * k)


def _petalas(rng, seg, g=0.3):
    """O farfalhar de mil pétalas-lâmina (o chiado fino que corre)."""
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 3000, 11000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 7 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * g


# ------------------------------------------------------------------ Byakuya

def senbonzakura(rng, v):
    """Byakuya: "Espalhe-se, Senbonzakura." — a lâmina virando mil pétalas que cortam."""
    x = _z(2.1)
    poe(x, _sino(rng, 1319, 0.8, 0.04, METAL), 0.0)
    poe(x, _petalas(rng, 0.9, 0.35), 0.05)
    for k in range(6):
        poe(x, graos(rng, n_de(0.08), 6, 0.0, 0.9, 4000, 10000, 0.002) * 0.3, 0.3 + 0.08 * k)
    return reverb(x, 0.7, 0.35)


def danku(rng, v):
    """Byakuya: Danku — a parede de luz subindo (o tom firme e o tinido)."""
    x = _z(2.0)
    n = n_de(0.4)
    poe(x, seno(varre(300, 600, n), n) * env(n, 0.3, 0.05) * 0.03, 0.0)
    poe(x, _sino(rng, 988, 1.0, 0.04, SINO), 0.35)
    poe(x, _brilho(rng, 0.6, 1568, 0.02, CRISTAL), 0.4)
    return reverb(x, 0.8, 0.4)


def byakuya_preparo(rng, v):
    """Byakuya (Preparo): a espada se desfazendo em pétalas (o farfalhar em laço)."""
    x = _z(1.4)
    poe(x, _petalas(rng, 1.0, 0.18), 0.0)
    n = n_de(1.0)
    poe(x, seno(659, n) * sobe_e_some(n, 0.6, 1.2) * 0.01, 0.0)
    return reverb(x, 0.7, 0.35)


def senkei(rng, v):
    """Byakuya: Senkei — as mil espadas formando o círculo e cortando juntas."""
    x = _z(2.4)
    for k in range(12):
        poe(x, _sino(rng, 1760 + 60 * (k % 6), 0.2, 0.012, METAL), 0.035 * k)
    n = n_de(0.3)
    poe(x, seno(55, n) * env(n, 0.1, 0.15) * 0.04, 0.45)
    for k in range(5):
        poe(x, _whoosh(rng, 0.12, 3000, 12000, 0.6, 1.3, 0.35), 0.6 + 0.03 * k)
    poe(x, _baque(70, 28, 0.6, 0.9, 2.8), 0.65)
    poe(x, _petalas(rng, 0.6, 0.25), 0.68)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Kitana

def leque_cortante(rng, v):
    """Kitana: o leque de aço abrindo ("chac") e o corte."""
    x = _z(1.8)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.02), 2000, 7000, 0.004) * 0.6, 0.02 * k)
    poe(x, _sino(rng, 2093, 0.4, 0.03, METAL), 0.05)
    poe(x, _whoosh(rng, 0.2, 2000, 10000, 0.8, 1.3, 0.5), 0.15)
    poe(x, _baque(150, 70, 0.2, 0.45), 0.38)
    return reverb(x, 0.5, 0.25)


def rajada_de_leque(rng, v):
    """Kitana: o abano do leque e o redemoinho de vento no rival."""
    x = _z(2.0)
    poe(x, _sopro(rng, 0.3, 300, 3000, 0.25, 0.4), 0.0)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 500, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 12 * _t(n)) ** 2) * env(n, 0.05, 0.4) * 0.3, 0.2)
    poe(x, _baque(170, 80, 0.15, 0.35), 0.7)
    return reverb(x, 0.5, 0.25)


def kitana_preparo(rng, v):
    """Kitana (Preparo): os dois leques abertos e cruzados (o tinido em laço)."""
    x = _z(1.4)
    for k in range(2):
        poe(x, _sino(rng, 2349, 0.4, 0.02, METAL), 0.5 * k)
        poe(x, _sino(rng, 2637, 0.4, 0.015, METAL), 0.5 * k + 0.05)
    return reverb(x, 0.6, 0.3)


def fatality_do_leque(rng, v):
    """Kitana: o leque girando como serra (o zunido) e cortando o rival."""
    x = _z(2.1)
    n = n_de(0.45)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2000, 9000, 2) * (0.4 + 0.6 * np.sin(2 * math.pi * 30 * t) ** 2) * env(n, 0.02, 0.1) * 0.35, 0.0)
    for k in range(4):
        poe(x, _whoosh(rng, 0.1, 3000, 12000, 0.6, 1.3, 0.35), 0.4 + 0.04 * k)
        poe(x, _sino(rng, 1760 + 150 * k, 0.2, 0.02, METAL), 0.42 + 0.04 * k)
    poe(x, _baque(90, 35, 0.5, 0.8, 2.6), 0.45)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Shao Kahn

def martelo_de_guerra(rng, v):
    """Shao Kahn: o martelo de guerra descendo e o estrondo."""
    x = _z(2.2)
    poe(x, _whoosh(rng, 0.35, 120, 1500, 0.9, 1.3, 0.55), 0.0)
    poe(x, _baque(45, 18, 1.0, 1.0, 3.2), 0.33)
    poe(x, _sino(rng, 165, 1.0, 0.06, METAL), 0.33)
    poe(x, _explosao(rng, 0.6, 45), 0.33)
    return reverb(x, 0.7, 0.35)


def provocacao_de_kahn(rng, v):
    """Shao Kahn: "Você é fraco!" — a risada grave e arrogante em ondas."""
    x = _z(2.1)
    for k in range(4):
        n = n_de(0.14)
        poe(x, satura(seno(varre(140 - 6 * k, 115 - 6 * k, n), n) + passa(rosa(rng, n), 100, 1200, 2) * 0.5, 4) * env(n, 0.01, 0.12) * 0.06, 0.17 * k)
    n = n_de(0.8)
    poe(x, seno(varre(70, 55, n), n) * sobe_e_some(n, 0.3, 1.2) * 0.05, 0.2)
    return reverb(x, 0.8, 0.4)


def kahn_preparo(rng, v):
    """Shao Kahn (Preparo): a lança erguida brilhando (o zumbido sombrio em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(82, n) + seno(123, n) * 0.5, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 2 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.045, 0.0)
    poe(x, _sino(rng, 1319, 0.5, 0.015, METAL), 0.3)
    return reverb(x, 0.6, 0.3)


def lanca_de_kahn(rng, v):
    """Shao Kahn: a lança voando (o silvo) e atravessando o rival."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.3, 1000, 8000, 0.9, 1.3, 0.55), 0.0)
    poe(x, _baque(110, 45, 0.4, 0.8, 2.6), 0.27)
    poe(x, estalo(rng, n_de(0.06), 800, 5000, 0.012), 0.27)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Snorlax

def pancada_snorlax(rng, v):
    """Snorlax: a barrigona balançando ("blob-blob") e a pancada pesada."""
    x = _z(1.9)
    for k in range(2):
        n = n_de(0.15)
        poe(x, seno(varre(90, 60, n), n) * env(n, 0.01, 0.12) * 0.1, 0.05 + 0.15 * k)
    poe(x, _baque(70, 28, 0.6, 0.9, 2.6), 0.38)
    return reverb(x, 0.5, 0.25)


def descansar(rng, v):
    """Snorlax: o ronco profundo ("rrrooonc") e a cura borbulhando."""
    x = _z(2.3)
    for k in range(2):
        n = n_de(0.6)
        t = _t(n)
        poe(x, passa(rosa(rng, n), 60, 500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 25 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.45, 0.8 * k)
    q = np.random.default_rng(4)
    for k in range(6):
        f = q.uniform(500, 900)
        poe(x, _piu(f, f * 1.6, 0.04, 0.02), 0.3 + 0.2 * k)
    return reverb(x, 0.5, 0.25)


def snorlax_preparo(rng, v):
    """Snorlax (Preparo): o corpo quicando ("boing-boing" grave em laço)."""
    x = _z(1.4)
    for k in range(2):
        n = n_de(0.3)
        poe(x, seno(varre(120, 70, n), n) * env(n, 0.01, 0.25) * 0.08, 0.66 * k)
        poe(x, _baque(80, 40, 0.2, 0.4), 0.66 * k + 0.25)
    return reverb(x, 0.4, 0.2)


def giga_impacto(rng, v):
    """Snorlax: Giga Impacto — o corpanzil caindo e o chão tremendo enorme."""
    x = _z(2.4)
    poe(x, _whoosh(rng, 0.4, 80, 1200, 0.9, 1.3, 0.55), 0.0)
    poe(x, _baque(35, 14, 1.3, 1.0, 3.5), 0.4)
    poe(x, _explosao(rng, 1.0, 35), 0.4)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 30, 250, 2) * sobe_e_some(n, 0.1, 1.2) * 0.6, 0.42)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Patrick

def abraco_esmagador(rng, v):
    """Patrick: o abraço apertado (o "squish" e o "Eu te amo!") e os corações."""
    x = _z(1.9)
    n = n_de(0.5)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 12 * t) ** 2) * env(n, 0.05, 0.4) * 0.35, 0.3)
    poe(x, _baque(150, 80, 0.2, 0.5), 0.3)
    for k, f in enumerate((523, 659, 784)):
        poe(x, _sino(rng, f, 0.3, 0.02, CRISTAL), 0.5 + 0.08 * k)
    return reverb(x, 0.4, 0.2)


def debaixo_da_pedra(rng, v):
    """Patrick: a pedra levantando (o ranger) e caindo de volta ("TUM")."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, satura(passa(rosa(rng, n), 80, 800, 2), 2) * env(n, 0.05, 0.2) * 0.3, 0.0)
    poe(x, _baque(70, 30, 0.6, 0.9, 2.6), 0.55)
    poe(x, estalo(rng, n_de(0.06), 200, 2000, 0.015) * 0.6, 0.55)
    return reverb(x, 0.5, 0.25)


def patrick_preparo(rng, v):
    """Patrick (Preparo): o pensamento vazio (o ventinho e o "hmmm" em laço)."""
    x = _z(1.4)
    poe(x, _sopro(rng, 1.0, 400, 2000, 0.08, 0.5), 0.0)
    n = n_de(0.8)
    poe(x, satura(seno(150, n), 2) * env(n, 0.1, 0.4) * 0.025, 0.2)
    return reverb(x, 0.4, 0.2)


def isso_e_burrice(rng, v):
    """Patrick: as besteiras voando (os sons malucos) e todo mundo confuso."""
    x = _z(2.2)
    q = np.random.default_rng(6)
    for k in range(8):
        f0 = q.uniform(300, 1200)
        poe(x, _piu(f0, f0 * q.uniform(0.5, 2.0), 0.12, 0.03), 0.07 * k)
    poe(x, _baque(150, 70, 0.2, 0.4), 0.45)
    _estrelinhas(rng, x, 0.55, 4)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Flecha

def soco_veloz(rng, v):
    """Flecha: os socos supersônicos ("tatatatá") e o estouro do som."""
    x = _z(1.8)
    for k in range(8):
        poe(x, _baque(200 + 30 * (k % 3), 100, 0.05, 0.3), 0.06 + 0.04 * k)
    poe(x, _whoosh(rng, 0.15, 2000, 12000, 0.5, 1.4, 0.4), 0.02)
    poe(x, estalo(rng, n_de(0.05), 500, 6000, 0.01) * 1.0, 0.18)
    return reverb(x, 0.4, 0.2)


def corrida_na_agua(rng, v):
    """Flecha: correndo por cima da água (os respingos rapidíssimos)."""
    x = _z(2.0)
    for k in range(14):
        n = n_de(0.05)
        poe(x, passa(rosa(rng, n), 1500, 8000, 2) * env(n, 0.003, 0.04) * 0.3, 0.05 * k)
    poe(x, _whoosh(rng, 0.7, 1000, 8000, 0.5, 1.4, 0.4), 0.0)
    return reverb(x, 0.4, 0.2)


def furacao_flecha(rng, v):
    """Flecha: correndo em círculo até virar furacão (o vento girando forte)."""
    x = _z(2.3)
    n = n_de(0.9)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 4000, 2) * (0.4 + 0.6 * np.sin(2 * math.pi * 6 * t) ** 2) * sobe_e_some(n, 0.4, 1.2) * 0.45, 0.0)
    for k in range(6):
        poe(x, _whoosh(rng, 0.1, 1500, 8000, 0.5, 1.4, 0.25), 0.05 + 0.08 * k)
    for k in range(3):
        poe(x, _baque(150, 70, 0.12, 0.3), 0.4 + 0.08 * k)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "senbonzakura": (senbonzakura, "Byakuya: Senbonzakura"),
    "danku": (danku, "Byakuya: Danku"),
    "byakuya-preparo": (byakuya_preparo, "Byakuya: a espada virando pétalas (Preparo)"),
    "senkei": (senkei, "Byakuya: Senkei"),
    "leque-cortante": (leque_cortante, "Kitana: o leque cortante"),
    "rajada-de-leque": (rajada_de_leque, "Kitana: a rajada de leque"),
    "kitana-preparo": (kitana_preparo, "Kitana: os leques cruzados (Preparo)"),
    "fatality-do-leque": (fatality_do_leque, "Kitana: a fatality do leque"),
    "martelo-de-guerra": (martelo_de_guerra, "Shao Kahn: o martelo de guerra"),
    "provocacao-de-kahn": (provocacao_de_kahn, "Shao Kahn: a provocação"),
    "kahn-preparo": (kahn_preparo, "Shao Kahn: a lança erguida (Preparo)"),
    "lanca-de-kahn": (lanca_de_kahn, "Shao Kahn: a lança de Kahn"),
    "pancada-snorlax": (pancada_snorlax, "Snorlax: a pancada"),
    "descansar": (descansar, "Snorlax: descansar"),
    "snorlax-preparo": (snorlax_preparo, "Snorlax: o corpo quicando (Preparo)"),
    "giga-impacto": (giga_impacto, "Snorlax: Giga Impacto"),
    "abraco-esmagador": (abraco_esmagador, "Patrick: o abraço esmagador"),
    "debaixo-da-pedra": (debaixo_da_pedra, "Patrick: debaixo da pedra"),
    "patrick-preparo": (patrick_preparo, "Patrick: o pensamento vazio (Preparo)"),
    "isso-e-burrice": (isso_e_burrice, "Patrick: Isso é burrice"),
    "soco-veloz": (soco_veloz, "Flecha: o soco veloz"),
    "corrida-na-agua": (corrida_na_agua, "Flecha: a corrida na água"),
    "furacao-flecha": (furacao_flecha, "Flecha: o furacão"),
}
