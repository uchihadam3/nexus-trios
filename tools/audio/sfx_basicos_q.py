"""Sons dos ataques básicos, lote q (veja tools/vfx/familias_v2/basicos_q.py).

Os bipes do HUD e a espingarda do T-800, os servos e a Auto-9 do RoboCop, o fuzil do Rambo, o estalo do chicote
do Indy, o pirata cambaleando, o feitiço do Harry, a maldição do Voldemort, o cajado do Gandalf, a cauda e o
rugido do Godzilla, o peito e os punhos do Kong, o tapa e o arroto do Shrek, o cristal da Elsa, o fogo verde da
Malévola, o "plim" do Gênio com a mola e o rosnado do Scar.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_k import _acerto, _mola, _splash
from sfx_basicos_l import _estrelinhas
from sfx_basicos_m import _zap
from sfx_basicos_o import _fogo, _voz
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _tiro(rng, g=0.7, grave=1.0):
    n = n_de(0.35)
    return satura(baque(n, 150 * grave, 60, 0.07, 1.0) * 0.8 + passa(rosa(rng, n), 400, 9000, 2) * env(n, 0.0005, 0.05) * 1.1, 1.6) * g


def _bip(f, seg=0.05, g=0.06):
    n = n_de(seg)
    return seno(f, n) * env(n, 0.002, seg * 0.8) * g


def _cartucho(rng, g=0.08):
    return modal(n_de(0.2), 3400, rng=rng, **METAL) * env(n_de(0.2), 0.0005, 0.06) * g


def tiro_do_exterminador(rng, v):
    """O T-800: os bipes do HUD lendo o alvo e o estrondo da espingarda, com o "tchac-tchac" de engatilhar."""
    x = _z(1.3)
    for k in range(4):
        poe(x, _bip(1200 + 200 * k, 0.04, 0.05), 0.02 + 0.06 * k)
    poe(x, _tiro(rng, 1.0, 0.7), 0.3)
    poe(x, passa(rosa(rng, n_de(0.4)), 300, 6000, 2) * env(n_de(0.4), 0.001, 0.2) * 0.3, 0.3)
    for t0 in (0.7, 0.8):
        poe(x, modal(n_de(0.1), 1300, rng=rng, **METAL) * env(n_de(0.1), 0.0005, 0.03) * 0.3 + estalo(rng, n_de(0.1), 1000, 5000, 0.005) * 0.4, t0)
    return reverb(x, 0.5, 0.22)


def auto9(rng, v):
    """A Auto-9 do RoboCop: os servos do braço (o zumbido mecânico), a mira travando e a rajada de três."""
    x = _z(1.2)
    n = n_de(0.25)
    poe(x, seno(varre(300, 500, n, 1.0), n) * sobe_e_some(n, 0.6, 1.3) * 0.05 + passa(rosa(rng, n), 1500, 5000, 2) * sobe_e_some(n, 0.6, 1.3) * 0.08, 0.0)
    poe(x, _bip(1800, 0.06, 0.06), 0.22)
    for k in range(3):
        poe(x, _tiro(rng, 0.6), 0.3 + 0.07 * k)
        poe(x, _cartucho(rng), 0.55 + 0.07 * k)
    return reverb(x, 0.45, 0.2)


def rajada_de_fuzil(rng, v):
    """O fuzil do Rambo: a rajada longa e contínua (dez tiros colados) e a chuva de cartuchos."""
    x = _z(1.3)
    for k in range(10):
        poe(x, _tiro(rng, 0.55, 1.1), 0.05 + 0.05 * k)
        poe(x, _cartucho(rng, 0.05), 0.3 + 0.05 * k)
    return reverb(x, 0.5, 0.22)


def chicote_de_indy(rng, v):
    """O Indiana Jones: o estalo do chicote (o "CRACK" agudo) e o soco de cinema, cheio."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.18, 800, 3500, 0.8, 1.2, 0.35), 0.0)
    poe(x, estalo(rng, n_de(0.04), 2500, 10000, 0.005) * 1.1, 0.18)
    poe(x, _whoosh(rng, 0.15, 400, 2000, 0.85, 1.3, 0.4), 0.33)
    poe(x, _acerto(rng, 1.1, 110), 0.47)
    return reverb(x, 0.4, 0.2)


def espada_pirata(rng, v):
    """O Jack Sparrow: dois cortes de sabre meio tortos (o "shing" que oscila), o "hic" cambaleante e a bússola
    girando (o tique rápido)."""
    x = _z(1.3)
    for t0 in (0.12, 0.4):
        poe(x, _whoosh(rng, 0.2, 700, 3500, 0.7, 1.3, 0.35), t0 - 0.06)
        poe(x, B._lamina_curta(rng, n_de(0.2), 2600) * env(n_de(0.2), 0.001, 0.07) * 0.18, t0)
        poe(x, _acerto(rng, 0.5, 140), t0 + 0.03)
    poe(x, _voz(rng, 0.08, 500, 650, 0.04, 2, 10), 0.28)
    for k in range(6):
        poe(x, modal(n_de(0.03), 3000, rng=rng, **METAL) * env(n_de(0.03), 0.0005, 0.01) * 0.08, 0.6 + 0.04 * k)
    return reverb(x, 0.45, 0.22)


def expelliarmus(rng, v):
    """O feitiço do Harry: o brilho da varinha, o jato vermelho chiando e o estouro."""
    x = _z(1.2)
    poe(x, _brilho(rng, 0.3, 1760, 0.08, CRISTAL), 0.0)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * sobe_e_some(n, 0.7, 1.3) * 0.3 + seno(varre(700, 1400, n, 1.0), n) * sobe_e_some(n, 0.7, 1.3) * 0.05, 0.12)
    poe(x, baque(n_de(0.3), 120, 60, 0.08, 0.6) * 0.5, 0.34)
    poe(x, passa(rosa(rng, n_de(0.3)), 800, 8000, 2) * env(n_de(0.3), 0.001, 0.12) * 0.35, 0.34)
    return reverb(x, 0.5, 0.25)


def avada_verde(rng, v):
    """A maldição do Voldemort: o jato verde (o rugido elétrico e grave), o impacto seco e o sibilo da serpente na
    Marca Negra."""
    x = _z(1.4)
    n = n_de(0.35)
    poe(x, satura(passa(rosa(rng, n), 300, 4000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 40 * _t(n))), 2.5) * sobe_e_some(n, 0.4, 1.2) * 0.35, 0.05)
    poe(x, baque(n_de(0.5), 70, 35, 0.18, 0.8) * 0.8, 0.22)
    m = n_de(0.6)
    poe(x, passa(rosa(rng, m), 4000, 10000, 2) * sobe_e_some(m, 0.3, 1.3) * 0.2, 0.5)
    return reverb(x, 0.6, 0.3)


def cajado_branco(rng, v):
    """O cajado do Gandalf: o cajado erguido, a batida forte no chão (o "TUM" de pedra) e a luz branca (o acorde
    claro) com as rachaduras."""
    x = _z(1.4)
    poe(x, _whoosh(rng, 0.25, 300, 1000, 0.85, 1.3, 0.35), 0.08)
    poe(x, baque(n_de(0.6), 70, 30, 0.22, 1.0) * 1.0, 0.3)
    poe(x, graos(rng, n_de(0.5), 30, 0.0, 0.45, 600, 3500, 0.01) * 0.4, 0.32)
    n = n_de(0.9)
    for f in (392, 587, 784):
        poe(x, seno(f, n) * sobe_e_some(n, 0.15, 1.4) * 0.035, 0.32)
    return reverb(x, 0.65, 0.3)


def cauda_de_godzilla(rng, v):
    """A cauda do Godzilla: o rugido monstruoso, a cauda varrendo (o vento enorme) e a pancada que treme tudo."""
    x = _z(1.6)
    poe(x, _voz(rng, 0.6, 260, 160, 0.14, 4, 20), 0.0)
    poe(x, _whoosh(rng, 0.4, 150, 900, 0.85, 1.3, 0.6), 0.05)
    poe(x, baque(n_de(0.7), 55, 25, 0.3, 1.0) * 1.0, 0.35)
    poe(x, _acerto(rng, 0.9, 80), 0.35)
    return reverb(x, 0.7, 0.32)


def soco_de_kong(rng, v):
    """O Kong: o peito batendo (três "BUM" ocos), o rugido e os dois punhos martelando o chão."""
    x = _z(1.5)
    for k in range(3):
        poe(x, passa(baque(n_de(0.2), 90, 60, 0.07, 0.2), None, 1200, 2) * 0.6, 0.0 + 0.09 * k)
    poe(x, _voz(rng, 0.3, 180, 130, 0.1, 4, 25), 0.2)
    poe(x, baque(n_de(0.6), 60, 28, 0.25, 1.0) * 1.0, 0.42)
    poe(x, _acerto(rng, 1.0, 85), 0.42)
    return reverb(x, 0.6, 0.28)


def tapa_de_ogro(rng, v):
    """O tapa do Shrek: o tapão estalado e cheio, a lama espirrando e o arroto grave."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.25, 400, 1500, 0.85, 1.3, 0.4), 0.02)
    poe(x, B._tapa(rng, n_de(0.12), 700, 4000, 0.03) * 1.3, 0.27)
    poe(x, B._carne(rng, n_de(0.12), 0.04, 2.4) * 0.8, 0.27)
    poe(x, _splash(rng, 0.35, 0.35, 200, 2500), 0.29)
    poe(x, _voz(rng, 0.35, 95, 80, 0.1, 5, 30), 0.55)
    return reverb(x, 0.4, 0.2)


def floco_de_elsa(rng, v):
    """O floco da Elsa: o cristal se formando (os tinidos que sobem, mágicos), o vento gelado e o floco estourando
    em cristais."""
    x = _z(1.3)
    for k, f in enumerate((1568, 1976, 2349, 2637)):
        poe(x, _brilho(rng, 0.4, f, 0.06, CRISTAL), 0.0 + 0.05 * k)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.6, 1.3) * 0.2, 0.18)
    for k in range(6):
        poe(x, _brilho(rng, 0.3, 2800 + 300 * k, 0.05, VIDRO), 0.42 + 0.03 * k)
    poe(x, _acerto(rng, 0.35, 160), 0.42)
    return reverb(x, 0.55, 0.28)


def raio_de_malevola(rng, v):
    """O raio da Malévola: o orbe acendendo (o tom sombrio), o fogo verde rugindo e os espinhos rompendo o chão."""
    x = _z(1.4)
    n = n_de(0.4)
    poe(x, (seno(110, n) + seno(117, n)) * sobe_e_some(n, 0.5, 1.3) * 0.06, 0.0)
    poe(x, _fogo(rng, 0.45, 0.4), 0.12)
    for k in range(7):
        poe(x, passa(baque(n_de(0.1), 200, 120, 0.03, 0.4), None, 3000, 2) * 0.25 + estalo(rng, n_de(0.1), 1000, 5000, 0.006) * 0.25, 0.35 + 0.04 * k)
    return reverb(x, 0.55, 0.25)


def estalo_do_genio(rng, v):
    """O estalo do Gênio: o estalo de dedos, o "puf" de fumaça com o "plim", a mola esticando (o "boing") e a luva
    acertando."""
    x = _z(1.3)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.005) * 0.9, 0.0)
    poe(x, passa(rosa(rng, n_de(0.25)), 300, 3000, 2) * env(n_de(0.25), 0.003, 0.12) * 0.4, 0.05)
    _estrelinhas(rng, 0.08, x, 0.06)
    poe(x, _mola(0.5, 260, 0.5, 13, 0.22), 0.2)
    poe(x, _acerto(rng, 0.9, 110), 0.33)
    return reverb(x, 0.4, 0.2)


def patada_de_scar(rng, v):
    """A patada do Scar: o rosnado baixo e traiçoeiro, as garras rasgando e o fogo crepitando."""
    x = _z(1.3)
    poe(x, _voz(rng, 0.4, 110, 90, 0.1, 4, 28), 0.0)
    for k in range(3):
        n = n_de(0.1)
        poe(x, passa(rosa(rng, n), 2000, 8000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.35, 0.12 + 0.025 * k)
    poe(x, _acerto(rng, 0.7, 130), 0.14)
    poe(x, graos(rng, n_de(0.5), 25, 0.0, 0.45, 1500, 6000, 0.004) * 0.3, 0.3)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "tiro-do-exterminador": (tiro_do_exterminador, "básico do T-800: o HUD e a espingarda"),
    "auto9": (auto9, "básico do RoboCop: os servos e a rajada de três"),
    "rajada-de-fuzil": (rajada_de_fuzil, "básico do Rambo: a rajada de fuzil"),
    "chicote-de-indy": (chicote_de_indy, "básico do Indy: o chicote e o soco"),
    "espada-pirata": (espada_pirata, "básico do Jack Sparrow: os cortes e a bússola"),
    "expelliarmus": (expelliarmus, "básico do Harry: o feitiço vermelho"),
    "avada-verde": (avada_verde, "básico do Voldemort: o jato verde e o sibilo"),
    "cajado-branco": (cajado_branco, "básico do Gandalf: o cajado no chão e a luz"),
    "cauda-de-godzilla": (cauda_de_godzilla, "básico do Godzilla: o rugido e a cauda"),
    "soco-de-kong": (soco_de_kong, "básico do Kong: o peito e os punhos"),
    "tapa-de-ogro": (tapa_de_ogro, "básico do Shrek: o tapa e o arroto"),
    "floco-de-elsa": (floco_de_elsa, "básico da Elsa: o cristal e o estouro"),
    "raio-de-malevola": (raio_de_malevola, "básico da Malévola: o fogo verde e os espinhos"),
    "estalo-do-genio": (estalo_do_genio, "básico do Gênio: o estalo e a mola"),
    "patada-de-scar": (patada_de_scar, "básico do Scar: o rosnado e as garras"),
}
