"""Os sons da rodada 31 das habilidades próprias (veja tools/vfx/familias_v2/rodada31.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _servo(rng, seg, f0, f1, g=0.05):
    """O motor de robô (a transformação dos Transformers): o zumbido serrilhado que sobe."""
    n = n_de(seg)
    return satura(seno(varre(f0, f1, n), n) + seno(varre(f0 * 2.02, f1 * 2.02, n), n) * 0.5, 3) * env(n, 0.01, seg * 0.6) * g


# ------------------------------------------------------------------ Optimus Prime

def escudo_de_energon(rng, v):
    """Optimus: as placas do escudo encaixando (os cliques metálicos) e o zumbido azul."""
    x = _z(1.9)
    for k in range(7):
        poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.006) * 0.5, 0.04 * k)
        poe(x, _sino(rng, 880 + 110 * k, 0.25, 0.015, METAL), 0.04 * k)
    n = n_de(1.0)
    poe(x, (seno(220, n) + seno(331, n) * 0.5) * sobe_e_some(n, 0.3, 1.2) * 0.035, 0.3)
    poe(x, _brilho(rng, 0.6, 1568, 0.03, CRISTAL), 0.4)
    return reverb(x, 0.5, 0.25)


def rifle_ion(rng, v):
    """Optimus: o rifle carregando (o tom que sobe) e o tiro de íons."""
    x = _z(1.8)
    n = n_de(0.3)
    poe(x, seno(varre(400, 2400, n), n) * env(n, 0.2, 0.05) * 0.04, 0.0)
    n = n_de(0.45)
    t = _t(n)
    poe(x, satura(seno(varre(900, 600, n), n) + passa(rosa(rng, n), 1000, 8000, 2) * 0.5, 3) * (0.7 + 0.3 * np.sin(2 * math.pi * 40 * t)) * env(n, 0.005, 0.4) * 0.08, 0.28)
    poe(x, _baque(160, 70, 0.25, 0.5), 0.33)
    return reverb(x, 0.5, 0.25)


def optimus_preparo(rng, v):
    """Optimus (Preparo): a Matriz da Liderança pulsando (o acorde grave e o brilho)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(110, n) + seno(165, n) * 0.6 + seno(220, n) * 0.3) * (0.7 + 0.3 * np.sin(2 * math.pi * 2 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.05, 0.0)
    poe(x, _brilho(rng, 0.8, 1319, 0.02, CRISTAL), 0.2)
    return reverb(x, 0.7, 0.35)


def autobots_avante(rng, v):
    """Optimus: "Autobots, avante!" — o som da transformação e a fanfarra."""
    x = _z(2.3)
    poe(x, _servo(rng, 0.4, 150, 500, 0.05), 0.0)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.03), 1200, 5000, 0.006) * 0.5, 0.05 + 0.07 * k)
    poe(x, _acorde((196, 262, 330, 392), 1.1, 0.05, 0.04, 0.8), 0.35)
    poe(x, _whoosh(rng, 0.5, 300, 3000, 0.6, 1.4, 0.4), 0.35)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Salsicha

def fuga_desesperada(rng, v):
    """Salsicha: "Zoinks!" e as pernas girando (o batuque rápido dos pés)."""
    x = _z(1.9)
    poe(x, _piu(700, 1200, 0.12, 0.05), 0.0)
    poe(x, _piu(1200, 900, 0.1, 0.04), 0.12)
    for k in range(16):
        poe(x, _baque(200 + 30 * (k % 2), 120, 0.05, 0.18), 0.2 + 0.035 * k)
    poe(x, _whoosh(rng, 0.4, 600, 4000, 0.5, 1.4, 0.4), 0.3)
    return reverb(x, 0.4, 0.2)


def sanduiche_gigante(rng, v):
    """Salsicha: as camadas do sanduíche caindo uma em cima da outra (os "plof") e a mordida."""
    x = _z(2.0)
    for k in range(7):
        poe(x, _baque(300 - 20 * k, 180, 0.08, 0.3), 0.15 + 0.05 * k)
    poe(x, _piu(500, 900, 0.1, 0.04), 0.5)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.04), 600, 3000, 0.008) * 0.6, 0.65 + 0.08 * k)
    poe(x, _brilho(rng, 0.5, 1047, 0.03, CRISTAL), 0.8)
    return reverb(x, 0.4, 0.2)


def correria(rng, v):
    """Salsicha: a correria em desenho (o batuque dos pés, o vento e os "vups")."""
    x = _z(2.0)
    for k in range(20):
        poe(x, _baque(220 + 25 * (k % 2), 130, 0.05, 0.18), 0.03 * k)
    poe(x, _whoosh(rng, 0.6, 400, 5000, 0.5, 1.4, 0.5), 0.0)
    poe(x, _piu(1500, 600, 0.25, 0.04), 0.6)
    return reverb(x, 0.4, 0.2)


# ------------------------------------------------------------------ Bob Esponja

def espremer(rng, v):
    """Bob Esponja: a esponja espremida (o "squish"), a água esguichando e as bolhas."""
    x = _z(2.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 14 * _t(n)) ** 2) * env(n, 0.05, 0.3) * 0.35, 0.0)
    poe(x, passa(rosa(rng, n_de(0.3)), 2000, 9000, 2) * env(n_de(0.3), 0.005, 0.25) * 0.3, 0.2)
    q = np.random.default_rng(3)
    for k in range(7):
        f = q.uniform(500, 1100)
        poe(x, _piu(f, f * 1.8, 0.05, 0.03), 0.45 + 0.05 * k)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Scooby-Doo

def tropeco(rng, v):
    """Scooby: o tropeço (o "uou-uou"), o rolamento e o tombo."""
    x = _z(1.9)
    poe(x, _piu(500, 300, 0.15, 0.05), 0.0)
    poe(x, _piu(450, 250, 0.2, 0.05), 0.15)
    for k in range(5):
        poe(x, _baque(180, 100, 0.06, 0.2), 0.1 + 0.08 * k)
    poe(x, _baque(120, 50, 0.35, 0.6, 2.2), 0.5)
    for k in range(3):
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.02, CRISTAL), 0.6 + 0.07 * k)
    return reverb(x, 0.4, 0.2)


def biscoito_scooby(rng, v):
    """Scooby: o biscoito jogado para o alto (o assobio), o "nhac" e o "Scooby-Dooby-Doo"."""
    x = _z(2.0)
    poe(x, _piu(500, 1400, 0.3, 0.04), 0.0)
    poe(x, _piu(1400, 600, 0.2, 0.04), 0.3)
    poe(x, estalo(rng, n_de(0.05), 600, 3000, 0.01), 0.5)
    for k, f in enumerate((392, 440, 494, 587)):
        n = n_de(0.12 if k < 3 else 0.35)
        poe(x, seno(f, n) * env(n, 0.01, 0.1 if k < 3 else 0.3) * 0.04, 0.6 + 0.1 * k)
    return reverb(x, 0.5, 0.25)


def scooby_preparo(rng, v):
    """Scooby (Preparo): o tremor de medo (os dentes batendo e o "rrr")."""
    x = _z(1.4)
    for k in range(18):
        poe(x, estalo(rng, n_de(0.015), 1500, 5000, 0.003) * 0.35, 0.05 * k)
    n = n_de(0.9)
    poe(x, seno(varre(220, 180, n), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 20 * _t(n))) * sobe_e_some(n, 0.5, 1.2) * 0.03, 0.05)
    return reverb(x, 0.4, 0.2)


def sorte_de_cachorro(rng, v):
    """Scooby: a sequência de acidentes — o barril rolando e as caixas caindo."""
    x = _z(2.2)
    n = n_de(0.55)
    poe(x, passa(rosa(rng, n), 80, 800, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 9 * _t(n)) ** 2) * env(n, 0.02, 0.4) * 0.4, 0.0)
    for k in range(3):
        poe(x, _piu(1200, 400, 0.18, 0.025), 0.28 + 0.1 * k)
        poe(x, _baque(170, 70, 0.3, 0.55), 0.5 + 0.1 * k)
        poe(x, estalo(rng, n_de(0.05), 500, 3000, 0.01) * 0.6, 0.5 + 0.1 * k)
    for k in range(3):
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.02, CRISTAL), 0.85 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Finn

def espada_de_sangue(rng, v):
    """Finn: a espada do demônio (o corte com o tom sombrio) e as gotas."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.2, 1500, 9000, 0.8, 1.3, 0.55), 0.05)
    poe(x, _sino(rng, 311, 0.8, 0.05, METAL), 0.2)
    q = np.random.default_rng(5)
    for k in range(5):
        poe(x, _piu(q.uniform(700, 1000), 300, 0.05, 0.02), 0.4 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


def punho_heroico(rng, v):
    """Finn: o soco do herói e as estrelinhas."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.25, 400, 4000, 0.8, 1.4, 0.5), 0.0)
    poe(x, _baque(120, 55, 0.35, 0.8, 2.4), 0.28)
    poe(x, _brilho(rng, 0.5, 1760, 0.035, CRISTAL), 0.32)
    return reverb(x, 0.5, 0.25)


def finn_preparo(rng, v):
    """Finn (Preparo): a espada no alto e as faíscas coloridas (o brilho subindo)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, seno(varre(500, 900, n), n) * sobe_e_some(n, 0.7, 1.2) * 0.025, 0.0)
    poe(x, graos(rng, n, 25, 0.0, 0.95, 2000, 9000, 0.003) * 0.3, 0.0)
    return reverb(x, 0.6, 0.3)


def matematico(rng, v):
    """Finn: "Matemático!" — o corte, a explosão e a cascata de notas brilhantes."""
    x = _z(2.3)
    poe(x, _whoosh(rng, 0.2, 1000, 8000, 0.8, 1.3, 0.5), 0.0)
    poe(x, _baque(80, 35, 0.6, 0.8, 2.6), 0.22)
    poe(x, _explosao(rng, 0.6, 70), 0.22)
    for k, f in enumerate((523, 659, 784, 1047, 1319, 1568)):
        poe(x, _sino(rng, f, 0.4, 0.025, CRISTAL), 0.3 + 0.05 * k)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Megatron

def canhao_de_fusao(rng, v):
    """Megatron: o canhão de fusão carregando e o feixe roxo varrendo os rivais."""
    x = _z(2.1)
    n = n_de(0.25)
    poe(x, seno(varre(150, 900, n), n) * env(n, 0.2, 0.04) * 0.05, 0.0)
    n = n_de(0.5)
    t = _t(n)
    poe(x, satura(seno(varre(180, 120, n), n) + passa(rosa(rng, n), 200, 4000, 2) * 0.6, 3.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 30 * t)) * env(n, 0.01, 0.45) * 0.09, 0.22)
    for k in range(3):
        poe(x, _baque(110, 50, 0.3, 0.5), 0.3 + 0.12 * k)
    return reverb(x, 0.6, 0.3)


def dominio_decepticon(rng, v):
    """Megatron: o símbolo descendo (o rugido metálico) e o esmagamento."""
    x = _z(2.0)
    poe(x, _servo(rng, 0.35, 300, 90, 0.05), 0.0)
    poe(x, _baque(55, 22, 0.8, 1.0, 3.0), 0.33)
    poe(x, _sino(rng, 147, 1.0, 0.06, METAL), 0.33)
    q = np.random.default_rng(6)
    for k in range(5):
        poe(x, _baque(q.uniform(160, 260), 90, 0.08, 0.2), 0.45 + q.uniform(0, 0.3))
    return reverb(x, 0.6, 0.3)


def megatron_preparo(rng, v):
    """Megatron (Preparo): o canhão de fusão carregando (o zumbido roxo pulsando)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(varre(70, 110, n), n) + seno(varre(140, 220, n), n) * 0.5, 2.5) * (0.6 + 0.4 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.7, 1.2) * 0.06, 0.0)
    poe(x, graos(rng, n, 20, 0.0, 0.95, 1500, 6000, 0.003) * 0.25, 0.0)
    return reverb(x, 0.6, 0.3)


def rendicao_decepticon(rng, v):
    """Megatron: "Ajoelhem-se!" — a onda roxa esmagando todos contra o chão."""
    x = _z(2.4)
    poe(x, _acorde((65, 98, 117), 1.0, 0.05, 0.05, 0.8), 0.0)
    poe(x, _whoosh(rng, 0.3, 120, 1500, 0.9, 1.3, 0.5), 0.2)
    poe(x, _baque(45, 18, 1.0, 1.0, 3.2), 0.48)
    poe(x, _explosao(rng, 0.8, 45), 0.48)
    poe(x, _sopro(rng, 0.8, 100, 800, 0.2, 0.2), 0.55)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Docinho

def soco_relampago(rng, v):
    """Docinho: o voo num piscar (o "zuuum") e o soco."""
    x = _z(1.7)
    poe(x, _whoosh(rng, 0.18, 1500, 10000, 0.6, 1.4, 0.5), 0.0)
    poe(x, _baque(130, 55, 0.35, 0.8, 2.4), 0.18)
    poe(x, estalo(rng, n_de(0.04), 1000, 5000, 0.01) * 0.6, 0.18)
    return reverb(x, 0.4, 0.2)


def sequencia_furiosa(rng, v):
    """Docinho: os socos em sequência, de vários lados."""
    x = _z(1.9)
    for k in range(7):
        poe(x, _whoosh(rng, 0.06, 1500, 7000, 0.6, 1.4, 0.25), 0.05 + 0.1 * k)
        poe(x, _baque(150 + 15 * (k % 3), 65, 0.12, 0.5), 0.13 + 0.1 * k)
    return reverb(x, 0.4, 0.2)


def explosao_verde(rng, v):
    """Docinho: a energia verde crescendo e estourando em todos."""
    x = _z(2.2)
    n = n_de(0.4)
    poe(x, seno(varre(200, 1200, n), n) * env(n, 0.35, 0.03) * 0.05, 0.0)
    poe(x, _baque(60, 25, 0.8, 1.0, 3.0), 0.38)
    poe(x, _explosao(rng, 0.9, 55), 0.38)
    poe(x, _brilho(rng, 0.6, 1175, 0.03, CRISTAL), 0.45)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "escudo-de-energon": (escudo_de_energon, "Optimus Prime: o escudo de energon"),
    "rifle-ion": (rifle_ion, "Optimus Prime: o rifle íon"),
    "optimus-preparo": (optimus_preparo, "Optimus Prime: a Matriz (Preparo)"),
    "autobots-avante": (autobots_avante, "Optimus Prime: Autobots, avante"),
    "fuga-desesperada": (fuga_desesperada, "Salsicha: a fuga desesperada"),
    "sanduiche-gigante": (sanduiche_gigante, "Salsicha: o sanduíche gigante"),
    "correria": (correria, "Salsicha: a correria"),
    "espremer": (espremer, "Bob Esponja: espremer"),
    "tropeco": (tropeco, "Scooby-Doo: o tropeço"),
    "biscoito-scooby": (biscoito_scooby, "Scooby-Doo: o Biscoito Scooby"),
    "scooby-preparo": (scooby_preparo, "Scooby-Doo: o medo (Preparo)"),
    "sorte-de-cachorro": (sorte_de_cachorro, "Scooby-Doo: a sorte de cachorro"),
    "espada-de-sangue": (espada_de_sangue, "Finn: a espada de sangue"),
    "punho-heroico": (punho_heroico, "Finn: o punho heroico"),
    "finn-preparo": (finn_preparo, "Finn: a espada no alto (Preparo)"),
    "matematico": (matematico, "Finn: Matemático!"),
    "canhao-de-fusao": (canhao_de_fusao, "Megatron: o canhão de fusão"),
    "dominio-decepticon": (dominio_decepticon, "Megatron: o domínio Decepticon"),
    "megatron-preparo": (megatron_preparo, "Megatron: o canhão carregando (Preparo)"),
    "rendicao-decepticon": (rendicao_decepticon, "Megatron: a rendição"),
    "soco-relampago": (soco_relampago, "Docinho: o soco relâmpago"),
    "sequencia-furiosa": (sequencia_furiosa, "Docinho: a sequência furiosa"),
    "explosao-verde": (explosao_verde, "Docinho: a explosão verde"),
}
