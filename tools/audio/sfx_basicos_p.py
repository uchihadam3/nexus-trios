"""Sons dos ataques básicos, lote p (veja tools/vfx/familias_v2/basicos_p.py).

O telefone e a facada do Ghostface, o ronco da motosserra do Leatherface, as correntes e o cubo do Pinhead,
o chiado da TV da Samara, o sussurro e as unhas da Valak, os morcegos do Drácula, o chiado do Alien e o ácido,
os cliques do Predador, o sabre do Vader com a respiração, a bengala do Yoda, o sabre do Luke, o raio da
Força, o "whoosh" em câmera lenta do Neo, o glitch do Smith e o double tap do John Wick.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_k import _acerto, _splash
from sfx_basicos_l import _estrelinhas
from sfx_basicos_m import _zap
from sfx_basicos_o import _voz
from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada10 import _motor
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _sabre(rng, seg, f=90.0, g=0.3, mexe=0.0):
    """O zumbido do sabre de luz: o tom grave com o "hum" que pulsa e o chiado fino, que sobe ao mexer."""
    n = n_de(seg)
    t = _t(n)
    ff = f * (1 + mexe * np.sin(math.pi * t / seg))
    hum = satura(np.sin(2 * math.pi * np.cumsum(ff) / SR) + 0.5 * np.sin(2 * math.pi * np.cumsum(ff * 2.02) / SR), 2)
    return (passa(hum, 60, 3000, 2) * (0.8 + 0.2 * np.sin(2 * math.pi * 7 * t)) + passa(rosa(rng, n), 3000, 9000, 2) * 0.15) * sobe_e_some(n, 0.3, 1.3) * g


def _tiro(rng, g=0.7):
    n = n_de(0.3)
    return satura(baque(n, 160, 70, 0.06, 1.0) * 0.8 + passa(rosa(rng, n), 500, 9000, 2) * env(n, 0.0005, 0.04) * 1.1, 1.6) * g


def golpe_por_tras(rng, v):
    """O golpe por trás: o toque de telefone abafado ("trim-trim"), o sopro da máscara surgindo e a facada."""
    x = _z(1.2)
    for k in range(2):
        n = n_de(0.12)
        t = _t(n)
        poe(x, seno(1800, n) * (np.sin(2 * math.pi * 20 * t) > 0) * env(n, 0.005, 0.1) * 0.05, 0.0 + 0.16 * k)
    poe(x, _whoosh(rng, 0.3, 1200, 400, 0.4, 1.3, 0.3), 0.15)
    poe(x, _whoosh(rng, 0.12, 900, 4000, 0.8, 1.2, 0.35), 0.32)
    poe(x, _acerto(rng, 0.8, 140, 900, 4500), 0.44)
    return reverb(x, 0.5, 0.25)


def serra_eletrica(rng, v):
    """A serra do Leatherface: o motor roncando alto o tempo todo e as duas mordidas da serra cortando."""
    x = _z(1.3)
    poe(x, _motor(rng, 1.1, 50, 70, 0.5), 0.0)
    for t0 in (0.15, 0.45):
        n = n_de(0.2)
        poe(x, satura(passa(rosa(rng, n), 300, 4000, 2) * (0.5 + 0.5 * np.sign(np.sin(2 * math.pi * 70 * _t(n)))), 3) * sobe_e_some(n, 0.3, 1.3) * 0.4, t0)
        poe(x, _acerto(rng, 0.5, 130), t0)
    return reverb(x, 0.4, 0.2)


def ganchos_de_corrente(rng, v):
    """Os ganchos do Pinhead: o cubo girando (o clique-clique do mecanismo e o sino grave), as correntes chicoteando
    e os ganchos fisgando."""
    x = _z(1.3)
    for k in range(5):
        poe(x, modal(n_de(0.06), 2400 + 200 * k, rng=rng, **METAL) * env(n_de(0.06), 0.0005, 0.02) * 0.15, 0.02 + 0.05 * k)
    poe(x, _brilho(rng, 1.0, 147, 0.15, SINO), 0.1)
    for k in range(5):
        n = n_de(0.15)
        poe(x, passa(rosa(rng, n), 1500, 7000, 2) * np.abs(np.sin(2 * math.pi * 40 * _t(n))) * env(n, 0.002, 0.1) * 0.25, 0.15 + 0.04 * k)
        poe(x, modal(n_de(0.15), 1600 + 150 * k, rng=rng, **METAL) * env(n_de(0.15), 0.0005, 0.05) * 0.12, 0.3 + 0.04 * k)
    poe(x, _acerto(rng, 0.5, 140, 900, 4500), 0.32)
    return reverb(x, 0.6, 0.3)


def toque_de_samara(rng, v):
    """O toque da Samara: o chiado da TV fora do ar, o estalo de articulação (os "crec" dela andando torta), a mão
    tocando e o eco do poço."""
    x = _z(1.4)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 1500, 10000, 2) * sobe_e_some(n, 0.3, 1.3) * 0.3, 0.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.03), 800, 4000, 0.006) * 0.4, 0.15 + 0.08 * k)
    poe(x, passa(B._baque_seco(rng, n_de(0.2), 110, 0.05), None, 1200, 2) * 0.6, 0.45)
    m = n_de(0.7)
    poe(x, (seno(varre(220, 200, m, 1.0), m) + seno(varre(233, 210, m, 1.0), m)) * sobe_e_some(m, 0.3, 1.3) * 0.04, 0.5)
    return reverb(x, 0.75, 0.38)


def garra_de_valak(rng, v):
    """A garra da Valak: o sussurro rouco e grave, a cruz virando (o rangido) e as unhas rasgando."""
    x = _z(1.3)
    poe(x, _voz(rng, 0.5, 120, 90, 0.08, 4, 8), 0.0)
    n = n_de(0.25)
    poe(x, seno(varre(300, 180, n, 1.0) * (1 + 0.05 * np.sin(2 * math.pi * 30 * _t(n))), n) * sobe_e_some(n, 0.5, 1.3) * 0.04, 0.05)
    for k in range(3):
        m = n_de(0.1)
        poe(x, passa(rosa(rng, m), 2000, 8000, 2) * sobe_e_some(m, 0.3, 1.2) * 0.35, 0.33 + 0.03 * k)
    poe(x, _acerto(rng, 0.6, 140, 1500, 6000), 0.34)
    return reverb(x, 0.65, 0.32)


def mordida_de_dracula(rng, v):
    """A mordida do Drácula: o bando de morcegos (os guinchos agudos e o bater de asas) e a mordida molhada."""
    x = _z(1.3)
    n = n_de(0.45)
    poe(x, passa(rosa(rng, n), 1000, 5000, 2) * np.abs(np.sin(2 * math.pi * 22 * _t(n))) * sobe_e_some(n, 0.5, 1.3) * 0.3, 0.0)
    for k in range(6):
        m = n_de(0.05)
        poe(x, seno(varre(5000 + 400 * (k % 3), 3800, m, 1.0), m) * env(m, 0.002, 0.04) * 0.025, 0.04 + 0.06 * k)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.006) * 0.7, 0.42)
    poe(x, _acerto(rng, 0.5, 150), 0.42)
    poe(x, _splash(rng, 0.3, 0.2, 200, 2000), 0.46)
    return reverb(x, 0.55, 0.28)


def garra_xenomorfa(rng, v):
    """O ataque do Alien: o chiado sibilante, a boca interna disparando (o "tchak" molhado) e o ácido chiando no
    chão."""
    x = _z(1.3)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 2500, 9000, 2) * sobe_e_some(n, 0.6, 1.3) * 0.3 + _voz(rng, 0.35, 700, 600, 0.03, 3, 30), 0.0)
    poe(x, estalo(rng, n_de(0.04), 800, 5000, 0.008) * 0.9, 0.36)
    poe(x, _acerto(rng, 0.8, 130), 0.36)
    m = n_de(0.6)
    poe(x, passa(rosa(rng, m), 3000, 10000, 2) * sobe_e_some(m, 0.2, 1.3) * 0.2 + graos(rng, m, 40, 0.0, 0.55, 3000, 9000, 0.003) * 0.25, 0.42)
    return reverb(x, 0.5, 0.25)


def laminas_de_pulso(rng, v):
    """O ataque do Predador: o clique-clique gutural, o zumbido da mira, a camuflagem cintilando e as lâminas
    saindo e cortando."""
    x = _z(1.2)
    for k in range(6):
        m = n_de(0.03)
        poe(x, passa(baque(m, 300, 200, 0.01, 0.6), None, 3000, 2) * 0.2, 0.0 + 0.035 * k)
    n = n_de(0.3)
    poe(x, seno(2800, n) * sobe_e_some(n, 0.2, 1.3) * 0.02, 0.1)
    poe(x, modal(n_de(0.15), 2200, rng=rng, **METAL) * env(n_de(0.15), 0.0005, 0.05) * 0.25, 0.3)
    for t0 in (0.35, 0.4):
        poe(x, B._lamina_curta(rng, n_de(0.2), 3000) * env(n_de(0.2), 0.001, 0.07) * 0.2, t0)
    poe(x, _acerto(rng, 0.7, 140, 1500, 6000), 0.38)
    return reverb(x, 0.45, 0.22)


def sabre_vermelho(rng, v):
    """O sabre do Vader: o "pshhh-vummm" do sabre acendendo, a respiração mecânica, o golpe pesado (o zumbido que
    sobe ao mexer) e o chiado do corte."""
    x = _z(1.4)
    poe(x, passa(rosa(rng, n_de(0.15)), 1000, 6000, 2) * env(n_de(0.15), 0.003, 0.1) * 0.3, 0.0)
    poe(x, _sabre(rng, 1.0, 85, 0.3, 0.3), 0.05)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 300, 2000, 2) * (0.4 + 0.6 * np.abs(np.sin(2 * math.pi * 1.5 * _t(n)))) * sobe_e_some(n, 0.5, 1.3) * 0.12, 0.0)
    poe(x, _acerto(rng, 0.8, 120), 0.42)
    poe(x, graos(rng, n_de(0.3), 20, 0.0, 0.25, 2500, 9000, 0.003) * 0.35, 0.42)
    return reverb(x, 0.5, 0.25)


def bengala_de_yoda(rng, v):
    """A bengala do Yoda: os pulinhos (os "fwip" curtos e agudos), os dois toques de madeira e o empurrão da Força."""
    x = _z(1.2)
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 1500, 4000, 0.6, 1.2, 0.25), 0.02 + 0.06 * k)
    for t0 in (0.31, 0.44):
        n = n_de(0.1)
        poe(x, modal(n, 900, rng=rng, razoes=[1.0, 2.5, 4.2], quedas=[0.04, 0.03, 0.02], ganhos=[1, 0.4, 0.2]) * 0.4 + B._tapa(rng, n, 1200, 5000, 0.008) * 0.6, t0)
    m = n_de(0.45)
    poe(x, passa(rosa(rng, m), 150, 900, 2) * sobe_e_some(m, 0.3, 1.3) * 0.3 + seno(varre(140, 100, m, 1.0), m) * sobe_e_some(m, 0.3, 1.3) * 0.06, 0.48)
    return reverb(x, 0.45, 0.22)


def sabre_verde(rng, v):
    """O sabre do Luke: o sabre acendendo e os dois cortes rápidos (o zumbido que passa e volta)."""
    x = _z(1.2)
    poe(x, passa(rosa(rng, n_de(0.12)), 1000, 6000, 2) * env(n_de(0.12), 0.003, 0.08) * 0.25, 0.0)
    poe(x, _sabre(rng, 0.9, 110, 0.25, 0.4), 0.03)
    for t0 in (0.2, 0.43):
        poe(x, _whoosh(rng, 0.15, 800, 3500, 0.7, 1.2, 0.3), t0 - 0.08)
        poe(x, _acerto(rng, 0.5, 140), t0)
    return reverb(x, 0.45, 0.22)


def raio_da_forca(rng, v):
    """O raio da Força: a eletricidade crepitando contínua, forte e chiada, e a risada rouca do Imperador."""
    x = _z(1.4)
    n = n_de(0.8)
    t = _t(n)
    pisca = (np.sin(2 * math.pi * 33 * t + 3 * np.sin(2 * math.pi * 5 * t)) > 0).astype(float) * 0.6 + 0.4
    poe(x, satura(passa(rosa(rng, n), 800, 9000, 2) * pisca, 3) * sobe_e_some(n, 0.2, 1.2) * 0.4, 0.05)
    poe(x, graos(rng, n, 80, 0.0, 0.75, 2000, 9000, 0.003) * 0.3, 0.05)
    for k in range(3):
        poe(x, _voz(rng, 0.09, 260 - 15 * k, 220, 0.04, 4, 20), 0.6 + 0.11 * k)
    return reverb(x, 0.55, 0.25)


def soco_de_neo(rng, v):
    """O soco do Neo: o tempo desacelerando (o "vwoooom" grave que estica), o punho atravessando em câmera lenta e o
    impacto pesado que volta à velocidade normal."""
    x = _z(1.4)
    n = n_de(0.5)
    poe(x, seno(varre(400, 80, n, 0.6), n) * sobe_e_some(n, 0.4, 1.3) * 0.12, 0.05)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * sobe_e_some(n, 0.5, 1.3) * 0.25, 0.1)
    for k in range(3):
        poe(x, seno(varre(1600 - 300 * k, 800, n_de(0.1), 1.0), n_de(0.1)) * env(n_de(0.1), 0.005, 0.08) * 0.03, 0.15 + 0.1 * k)
    poe(x, baque(n_de(0.5), 75, 35, 0.18, 0.9) * 0.9, 0.45)
    poe(x, _acerto(rng, 0.9, 100), 0.45)
    return reverb(x, 0.55, 0.28)


def soco_do_agente(rng, v):
    """O soco do Smith: o glitch digital (os pedacinhos de som cortados e repetidos) e os vários socos juntos."""
    x = _z(1.2)
    for k in range(8):
        n = n_de(0.03)
        poe(x, seno(400 + 300 * (k % 4), n) * env(n, 0.001, 0.02) * 0.08 + passa(rosa(rng, n), 2000, 8000, 2) * env(n, 0.001, 0.02) * 0.2, 0.0 + 0.035 * k)
    for k in range(3):
        poe(x, _acerto(rng, 0.6, 115 + 10 * k), 0.35 + 0.015 * k)
    return reverb(x, 0.35, 0.18)


def tiro_de_john_wick(rng, v):
    """Os tiros do John Wick: o "bang-bang" colado do double tap, o terceiro de precisão e os cartuchos tilintando."""
    x = _z(1.3)
    for t0 in (0.05, 0.12, 0.35):
        poe(x, _tiro(rng, 0.75), t0)
        for k in range(1):
            poe(x, modal(n_de(0.2), 3600, rng=rng, **METAL) * env(n_de(0.2), 0.0005, 0.06) * 0.1, t0 + 0.3)
    poe(x, _acerto(rng, 0.5, 150), 0.18)
    poe(x, _acerto(rng, 0.6, 140), 0.42)
    return reverb(x, 0.5, 0.22)


SONS: dict = {
    "golpe-por-tras": (golpe_por_tras, "básico do Ghostface: o telefone e a facada"),
    "serra-eletrica": (serra_eletrica, "básico do Leatherface: a motosserra"),
    "ganchos-de-corrente": (ganchos_de_corrente, "básico do Pinhead: o cubo e as correntes"),
    "toque-de-samara": (toque_de_samara, "básico da Samara: a TV e o toque"),
    "garra-de-valak": (garra_de_valak, "básico da Valak: o sussurro e as unhas"),
    "mordida-de-dracula": (mordida_de_dracula, "básico do Drácula: os morcegos e a mordida"),
    "garra-xenomorfa": (garra_xenomorfa, "básico do Xenomorfo: o chiado e o ácido"),
    "laminas-de-pulso": (laminas_de_pulso, "básico do Predador: os cliques e as lâminas"),
    "sabre-vermelho": (sabre_vermelho, "básico do Vader: o sabre e a respiração"),
    "bengala-de-yoda": (bengala_de_yoda, "básico do Yoda: os pulinhos e a bengala"),
    "sabre-verde": (sabre_verde, "básico do Luke: o sabre verde"),
    "raio-da-forca": (raio_da_forca, "básico do Palpatine: o raio e a risada"),
    "soco-de-neo": (soco_de_neo, "básico do Neo: a câmera lenta e o soco"),
    "soco-do-agente": (soco_do_agente, "básico do Smith: o glitch e os socos"),
    "tiro-de-john-wick": (tiro_de_john_wick, "básico do John Wick: o double tap"),
}
