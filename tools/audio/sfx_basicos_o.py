"""Sons dos ataques básicos, lote o (veja tools/vfx/familias_v2/basicos_o.py).

O soco divino com o eco, o cetro e o tilintar da balança, o raio do sol que queima, o vento de areia, o bater
da asa, o grito do falcão, o rugido da leoa com o fogo, a lança rúnica, a mordida e a corrente partindo, o
frio da morte, o machado do Jason com o "ki-ki-ki ma-ma-ma", as lâminas raspando do Freddy, as notas agudas
do Myers, a risada do Chucky e a gargalhada do Pennywise com o balão.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_k import _acerto, _mola, _splash
from sfx_basicos_l import _estrelinhas
from sfx_basicos_m import _zap
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _fogo(rng, seg, g=0.3):
    n = n_de(seg)
    x = passa(rosa(rng, n), 150, 3500, 2) * (0.6 + 0.4 * np.abs(np.sin(2 * math.pi * 5 * _t(n))))
    x += graos(rng, n, int(seg * 40), 0.0, seg, 1500, 6000, 0.004) * 0.6
    return x * sobe_e_some(n, 0.35, 1.3) * g


def _voz(rng, seg, f0, f1, g=0.05, aspereza=2.5, trem=6.0):
    """Uma "voz" sintética: o tom que varia, saturado e filtrado (grito, rugido, risada)."""
    n = n_de(seg)
    t = _t(n)
    f = varre(f0, f1, n, 1.0) * (1 + 0.04 * np.sin(2 * math.pi * trem * t))
    x = satura(np.sin(2 * math.pi * np.cumsum(f) / SR), aspereza) * (0.6 + 0.4 * passa(rosa(rng, n), 100, 2000, 2) * 3)
    return passa(x, 150, 4000, 2) * sobe_e_some(n, 0.3, 1.3) * g


def soco_de_hercules(rng, v):
    """O soco de Hércules: o punho rasgando o ar, o impacto enorme e as duas ondas com eco de templo."""
    x = _z(1.4)
    poe(x, _whoosh(rng, 0.3, 250, 1500, 0.85, 1.3, 0.55), 0.0)
    poe(x, baque(n_de(0.6), 65, 30, 0.22, 1.0) * 0.9, 0.28)
    poe(x, _acerto(rng, 1.0, 95), 0.28)
    poe(x, passa(baque(n_de(0.4), 80, 40, 0.15, 0.2), None, 800, 2) * 0.4, 0.38)
    return reverb(x, 0.65, 0.3)


def cetro_de_anubis(rng, v):
    """O cetro de Anúbis: o golpe do cetro, e a balança do julgamento (os dois pratos tilintando e pendendo)."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.28, 400, 1800, 0.85, 1.3, 0.45), 0.0)
    poe(x, _acerto(rng, 0.8, 120), 0.26)
    poe(x, modal(n_de(0.6), 1400, rng=rng, **SINO) * env(n_de(0.6), 0.001, 0.3) * 0.12, 0.42)
    poe(x, modal(n_de(0.6), 1250, rng=rng, **SINO) * env(n_de(0.6), 0.001, 0.3) * 0.1, 0.62)
    n = n_de(0.6)
    poe(x, seno(73, n) * sobe_e_some(n, 0.3, 1.3) * 0.1, 0.45)
    return reverb(x, 0.6, 0.3)


def disco_solar(rng, v):
    """O raio de Rá: o disco acendendo (o acorde quente), o raio queimando (o chiado ardente) e o fogo pegando."""
    x = _z(1.3)
    n = n_de(0.4)
    for f in (220, 330, 440):
        poe(x, seno(f, n) * sobe_e_some(n, 0.3, 1.3) * 0.04, 0.0)
    m = n_de(0.35)
    poe(x, passa(rosa(rng, m), 1500, 8000, 2) * sobe_e_some(m, 0.2, 1.3) * 0.25, 0.18)
    poe(x, _acerto(rng, 0.5, 140), 0.25)
    poe(x, _fogo(rng, 0.7, 0.3), 0.3)
    return reverb(x, 0.5, 0.25)


def cetro_de_set(rng, v):
    """O golpe de Set: o cetro batendo e o redemoinho de areia uivando e arranhando."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.25, 400, 1500, 0.85, 1.3, 0.4), 0.0)
    poe(x, _acerto(rng, 0.6, 130), 0.22)
    n = n_de(0.85)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 400, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.4, 1.3) * 0.35, 0.15)
    poe(x, graos(rng, n, 120, 0.0, 0.8, 2500, 9000, 0.002) * 0.25, 0.15)
    return reverb(x, 0.5, 0.22)


def asas_de_isis(rng, v):
    """A asa de Ísis: o bater grande de asa (o "fwump" de penas), o golpe e as penas caindo com o brilho."""
    x = _z(1.3)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * sobe_e_some(n, 0.6, 1.3) * 0.5, 0.05)
    poe(x, _acerto(rng, 0.5, 140), 0.28)
    for k, f in enumerate((1568, 1976, 2349)):
        poe(x, _brilho(rng, 0.5, f, 0.05, SINO), 0.4 + 0.1 * k)
    return reverb(x, 0.55, 0.28)


def garra_do_falcao(rng, v):
    """As garras de Hórus: o grito agudo do falcão mergulhando, o vento da descida e as garras agarrando."""
    x = _z(1.2)
    poe(x, _voz(rng, 0.35, 2600, 1800, 0.05, 1.8, 18), 0.0)
    poe(x, _whoosh(rng, 0.3, 1500, 600, 0.8, 1.3, 0.4), 0.02)
    poe(x, _acerto(rng, 0.8, 130, 1500, 6000), 0.3)
    poe(x, graos(rng, n_de(0.3), 15, 0.0, 0.25, 2000, 7000, 0.004) * 0.25, 0.32)
    return reverb(x, 0.45, 0.22)


def garra_da_leoa(rng, v):
    """A patada de Sekhmet: o rugido da leoa, as unhas rasgando e o fogo acendendo nos riscos."""
    x = _z(1.3)
    poe(x, _voz(rng, 0.45, 160, 110, 0.12, 4, 25), 0.0)
    for k in range(4):
        n = n_de(0.1)
        poe(x, passa(rosa(rng, n), 2000, 8000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.35, 0.1 + 0.02 * k)
    poe(x, _acerto(rng, 0.6, 130), 0.12)
    poe(x, _fogo(rng, 0.7, 0.3), 0.2)
    return reverb(x, 0.45, 0.22)


def gungnir(rng, v):
    """A Gungnir: a lança voando com o zumbido rúnico (o tom grave e o brilho), o "TCHAK" cravando e as runas
    acendendo (o acorde antigo)."""
    x = _z(1.3)
    n = n_de(0.3)
    poe(x, seno(varre(110, 165, n, 1.0), n) * sobe_e_some(n, 0.7, 1.3) * 0.1 + passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.7, 1.3) * 0.2, 0.0)
    poe(x, B._lamina_curta(rng, n_de(0.25), 2000) * env(n_de(0.25), 0.001, 0.08) * 0.2, 0.25)
    poe(x, _acerto(rng, 0.9, 110), 0.25)
    m = n_de(0.7)
    poe(x, (seno(147, m) + seno(220, m) * 0.6 + seno(294, m) * 0.4) * sobe_e_some(m, 0.2, 1.4) * 0.05, 0.3)
    return reverb(x, 0.6, 0.3)


def dentada_de_fenrir(rng, v):
    """A dentada de Fenrir: o rosnado grave do lobo, a mandíbula fechando (o "CLACK" de dentes) e a corrente
    estourando (os elos tinindo)."""
    x = _z(1.3)
    poe(x, _voz(rng, 0.35, 85, 70, 0.14, 4, 30), 0.0)
    poe(x, estalo(rng, n_de(0.04), 1000, 6000, 0.008) * 1.0, 0.27)
    poe(x, _acerto(rng, 0.9, 100), 0.27)
    for k in range(5):
        poe(x, modal(n_de(0.25), 1800 + 260 * k, rng=rng, **METAL) * env(n_de(0.25), 0.0005, 0.08) * 0.12, 0.3 + 0.05 * k)
    return reverb(x, 0.45, 0.22)


def toque_de_hel(rng, v):
    """O toque de Hel: os ossos dos dedos estalando, o vento frio da morte e o gelo se formando (os tinidos
    finos), com o gemido baixo."""
    x = _z(1.4)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.003) * 0.4, 0.05 + 0.06 * k)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 300, 2000, 2) * sobe_e_some(n, 0.4, 1.3) * 0.25, 0.2)
    for k in range(5):
        poe(x, _brilho(rng, 0.4, 2800 + 300 * k, 0.04, VIDRO), 0.32 + 0.05 * k)
    poe(x, _voz(rng, 0.6, 220, 180, 0.03, 1.5, 4), 0.35)
    return reverb(x, 0.6, 0.3)


def machadada(rng, v):
    """A machadada do Jason: o sussurro "ki-ki-ki, ma-ma-ma" (os chiados curtos ecoando), o machado subindo e o
    baque surdo e pesado."""
    x = _z(1.4)
    for k in range(6):
        n = n_de(0.06)
        poe(x, passa(rosa(rng, n), 3000 if k < 3 else 1500, 9000 if k < 3 else 5000, 2) * env(n, 0.003, 0.04) * 0.25, 0.0 + 0.06 * k)
    poe(x, _whoosh(rng, 0.25, 300, 1400, 0.85, 1.3, 0.5), 0.2)
    poe(x, baque(n_de(0.45), 80, 40, 0.15, 0.6) * 0.9, 0.37)
    poe(x, _acerto(rng, 0.8, 100), 0.37)
    return reverb(x, 0.6, 0.25)


def garra_de_freddy(rng, v):
    """A luva do Freddy: as lâminas raspando metal com metal (o rangido agudo), o corte e a cantiga distorcida do
    pesadelo ao fundo."""
    x = _z(1.3)
    n = n_de(0.3)
    t = _t(n)
    poe(x, (seno(3200 + 300 * np.sin(2 * math.pi * 11 * t), n) * 0.3 + passa(rosa(rng, n), 3000, 9000, 2)) * sobe_e_some(n, 0.6, 1.3) * 0.15, 0.0)
    for k in range(4):
        poe(x, B._lamina_curta(rng, n_de(0.2), 2800 + 200 * k) * env(n_de(0.2), 0.001, 0.07) * 0.12, 0.15 + 0.015 * k)
    poe(x, _acerto(rng, 0.6, 140, 2000, 7000), 0.16)
    for k, f in enumerate((660, 784, 660, 523)):
        m = n_de(0.18)
        poe(x, seno(f * (1 + 0.02 * np.sin(2 * math.pi * 5 * _t(m))), m) * env(m, 0.01, 0.12) * 0.03, 0.5 + 0.15 * k)
    return reverb(x, 0.65, 0.32)


def facada_de_myers(rng, v):
    """A facada do Myers: as notas agudas da música do Halloween (o padrão 5 por 4 no piano), a faca brilhando e
    a facada certeira."""
    x = _z(1.3)
    for k, f in enumerate((1175, 784, 784, 1175, 784)):
        m = n_de(0.12)
        poe(x, modal(m, f, rng=rng, razoes=[1.0, 2.0, 3.0], quedas=[0.12, 0.08, 0.05], ganhos=[1, 0.3, 0.15]) * 0.07, 0.0 + 0.07 * k)
    poe(x, _brilho(rng, 0.3, 3500, 0.05, VIDRO), 0.12)
    poe(x, _whoosh(rng, 0.2, 1500, 600, 0.8, 1.3, 0.35), 0.25)
    poe(x, _acerto(rng, 0.8, 130, 900, 4500), 0.4)
    return reverb(x, 0.55, 0.25)


def facadinha_do_chucky(rng, v):
    """As facadinhas do Chucky: a risadinha maníaca aguda ("hihihi") e as quatro facadinhas rápidas."""
    x = _z(1.2)
    for k in range(5):
        poe(x, _voz(rng, 0.07, 900 + 60 * (k % 2), 800, 0.05, 2, 20), 0.0 + 0.08 * k)
    for k in range(4):
        poe(x, _acerto(rng, 0.45, 160, 1200, 5000), 0.1 + 0.12 * k)
    return reverb(x, 0.4, 0.2)


def mordida_de_pennywise(rng, v):
    """A mordida do Pennywise: a gargalhada distorcida, a boca se abrindo (o rangido molhado), o "CHOMP" e o balão
    flutuando (o rangido de borracha)."""
    x = _z(1.5)
    for k in range(4):
        poe(x, _voz(rng, 0.1, 500 - 30 * k, 420, 0.06, 3, 12), 0.0 + 0.1 * k)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 200, 2000, 2) * sobe_e_some(n, 0.5, 1.3) * 0.3, 0.1)
    poe(x, estalo(rng, n_de(0.04), 800, 5000, 0.01) * 1.0, 0.46)
    poe(x, _acerto(rng, 0.9, 100), 0.46)
    m = n_de(0.2)
    poe(x, seno(varre(700, 900, m, 1.0) * (1 + 0.03 * np.sin(2 * math.pi * 40 * _t(m))), m) * env(m, 0.01, 0.12) * 0.04, 0.75)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "soco-de-hercules": (soco_de_hercules, "básico de Hércules: o soco divino"),
    "cetro-de-anubis": (cetro_de_anubis, "básico de Anúbis: o cetro e a balança"),
    "disco-solar": (disco_solar, "básico de Rá: o sol e o fogo"),
    "cetro-de-set": (cetro_de_set, "básico de Set: a areia girando"),
    "asas-de-isis": (asas_de_isis, "básico de Ísis: a asa e as penas"),
    "garra-do-falcao": (garra_do_falcao, "básico de Hórus: o falcão mergulhando"),
    "garra-da-leoa": (garra_da_leoa, "básico de Sekhmet: o rugido e o fogo"),
    "gungnir": (gungnir, "básico de Odin: a lança rúnica"),
    "dentada-de-fenrir": (dentada_de_fenrir, "básico de Fenrir: a mordida e a corrente"),
    "toque-de-hel": (toque_de_hel, "básico de Hel: os ossos e o frio"),
    "machadada": (machadada, "básico do Jason: o sussurro e o machado"),
    "garra-de-freddy": (garra_de_freddy, "básico do Freddy: as lâminas e a cantiga"),
    "facada-de-myers": (facada_de_myers, "básico do Myers: as notas e a facada"),
    "facadinha-do-chucky": (facadinha_do_chucky, "básico do Chucky: a risadinha e as facadas"),
    "mordida-de-pennywise": (mordida_de_pennywise, "básico do Pennywise: a gargalhada e o chomp"),
}
