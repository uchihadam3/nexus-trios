"""Sons dos ataques básicos, lote i (veja tools/vfx/familias_v2/basicos_i.py).

Cada som segue o desenho da folha: as duas estocadas de metal dos sais, o
"vuvuvu" dos nunchakus com duas pancadas de madeira, a britadeira da bicada, o
"zwip" do Omnitrix antes do golpe, a manivela do Popeye, o machado de energon,
o "tchop" com bolhas, o laço girando e apertando, o jato de fogo azul, o
assobio da bigorna caindo e o CLANG, o BONG da frigideira, a pancada com magia
sinistra do Cajado da Caveira e o corte com brilho da Espada de Augúrio.
Tudo sintetizado, sem vozes nem trechos de músicas.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _madeira_oca, _tom, _whoosh, _z, nota  # noqa: F401
from som import (CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, graos, modal, n_de, passa, poe,  # noqa: F401
                 reverb, rosa, ruido, satura, seno, sobe_e_some, varre)


def _t(n):
    return np.arange(n) / SR


def _bloop(rng, seg=0.05, f0=500.0, f1=1500.0, g=0.3):
    """Bolha estourando: um "blup" curto com o tom subindo depressa."""
    n = n_de(seg)
    return seno(varre(f0, f1, n, 1.6), n) * env(n, 0.002, seg * 0.35) * g


def _catraca(rng, seg, taxa0, taxa1, lo=1800, hi=6500, g=0.4):
    """Cliques de catraca/manivela com a frequência dos cliques indo de taxa0 a taxa1."""
    n = n_de(seg)
    x = np.zeros(n)
    tt = 0.0
    while tt < seg:
        m = n_de(0.012)
        clic = passa(ruido(rng, m), lo, hi, 2) * env(m, 0.0002, 0.0025) + np.sin(2 * math.pi * rng.uniform(2200, 2600) * _t(m)) * np.exp(-_t(m) / 0.004) * 0.4
        poe(x, clic * rng.uniform(0.7, 1.0), tt)
        taxa = taxa0 + (taxa1 - taxa0) * tt / seg
        tt += max(0.012, 1.0 / max(taxa, 1.0))
    return x * g


# ------------------------------------------------------------------ Raphael: Sais
def sais(rng, v):
    """Duas estocadas: o ar cortado e o "tchink" metálico do garfo entrando, uma depois da outra."""
    x = _z(0.85)
    for k, t0 in enumerate((0.0, 0.29)):
        poe(x, assobio(rng, n_de(0.09), 1600, 7000, 2.0, 0.35) * sobe_e_some(n_de(0.09), 0.9, 1.2) * 0.7, t0)
        m = n_de(0.3)
        tchink = modal(m, rng.uniform(1900, 2200) * (1.12 if k else 1.0), rng=rng, **METAL) * env(m, 0.0005, 0.07) * 0.35
        tchink += B._lamina_curta(rng, m, 3200 + 300 * k) * 0.3
        tchink += B._tapa(rng, m, 1800, 7500, 0.008) * 0.9 + B._carne(rng, m, 0.03, 2.4) * 0.6
        poe(x, tchink, t0 + 0.075)
        poe(x, modal(n_de(0.18), rng.uniform(4200, 4800), rng=rng, **METAL) * env(n_de(0.18), 0.0005, 0.03) * 0.12, t0 + 0.09)
    return reverb(x, 0.3, 0.14, 7000)


# ------------------------------------------------------------------ Michelangelo: Nunchakus
def _vuvu(rng, seg, rot0, rot1, g=0.8):
    """O giro do nunchaku: um sopro que pulsa a cada volta ("vu-vu-vu")."""
    n = n_de(seg)
    fase = 2 * math.pi * np.cumsum(varre(rot0, rot1, n, 1.0)) / SR
    pulsos = (0.5 + 0.5 * np.sin(fase)) ** 3
    ar = passa(rosa(rng, n), 300, 2400, 2) * 0.8 + passa(ruido(rng, n), 2000, 5000, 2) * 0.15
    return ar * pulsos * sobe_e_some(n, 0.8, 1.2) * g


def nunchakus(rng, v):
    """"Vuvuvu" do giro, TOC de madeira, mais uma volta, TOC de novo."""
    x = _z(0.95)
    poe(x, _vuvu(rng, 0.27, 11, 17, 1.4), 0.0)
    for t0, f in ((0.25, 820), (0.47, 900)):
        m = n_de(0.32)
        toc = _madeira_oca(rng, m, f * rng.uniform(0.97, 1.03)) * 0.7 + B._baque_seco(rng, m, 120, 0.05) * 0.5 + B._tapa(rng, m, 1500, 6000, 0.006) * 0.7
        poe(x, toc, t0)
    poe(x, _vuvu(rng, 0.2, 15, 19, 1.0), 0.29)
    poe(x, _tilim_corrente(rng) * 0.25, 0.27)
    poe(x, _tilim_corrente(rng) * 0.2, 0.5)
    return reverb(x, 0.25, 0.12)


def _tilim_corrente(rng):
    n = n_de(0.08)
    t = _t(n)
    y = sum(np.sin(2 * math.pi * rng.uniform(3000, 6500) * t) * np.exp(-t / rng.uniform(0.006, 0.018)) for _ in range(4))
    return y / 2


# ------------------------------------------------------------------ Pica-Pau / Patolino: Bicada
def bicada(rng, v):
    """Bicadas rapidíssimas em madeira (a britadeira), com as lascas caindo no fim."""
    x = _z(0.85)
    taxa = rng.uniform(16, 19)
    t0 = 0.0
    k = 0
    while t0 < 0.56:
        m = n_de(0.07)
        f = rng.uniform(1050, 1250) * (1.0 + 0.04 * math.sin(k * 1.7))
        toc = _madeira_oca(rng, m, f) * 0.55 + passa(ruido(rng, m), 1500, 6500, 2) * env(m, 0.0002, 0.004) * 0.9
        toc += B._baque_seco(rng, m, 180, 0.015) * 0.25
        poe(x, toc * rng.uniform(0.8, 1.0), t0)
        t0 += 1.0 / taxa * rng.uniform(0.9, 1.1)
        k += 1
    poe(x, graos(rng, n_de(0.35), 16, 0.0, 0.3, 1200, 5000, 0.006) * 0.25, 0.5)
    return reverb(x, 0.2, 0.1)


# ------------------------------------------------------------------ Ben 10: Golpe alienígena
def golpe_alienigena(rng, v):
    """O "zwip" do Omnitrix (tom que sobe girando com brilho), o clarão e o golpe pesado do alien."""
    x = _z(1.0)
    n = n_de(0.3)
    t = _t(n)
    f = varre(260, 2200, n, 0.9)
    zwip = seno(f * (1 + 0.08 * np.sin(2 * math.pi * 38 * t)), n) + 0.5 * seno(f * 1.5, n) + 0.3 * seno(f * 2.01, n)
    zwip = satura(zwip * 0.6, 1.6) * sobe_e_some(n, 0.75, 1.3) * 0.32
    poe(x, zwip, 0.0)
    poe(x, assobio(rng, n, 500, 6000, 0.9, 0.45) * sobe_e_some(n, 0.85, 1.4) * 0.35, 0.0)
    m = n_de(0.5)
    clarao = passa(rosa(rng, m), 800, 9000, 2) * env(m, 0.002, 0.12) * 0.5
    clarao += modal(m, rng.uniform(1400, 1600), rng=rng, **CRISTAL) * env(m, 0.001, 0.2) * 0.12
    clarao += satura(seno(varre(90, 55, m, 1.2), m), 2.5) * env(m, 0.002, 0.15) * 0.3
    poe(x, clarao, 0.24)
    poe(x, assobio(rng, n_de(0.12), 400, 3000, 1.6, 0.4) * sobe_e_some(n_de(0.12), 0.9, 1.2) * 0.6, 0.27)
    poe(x, B.soco_pesado(rng, v) * 1.05, 0.36)
    return reverb(x, 0.4, 0.18)


# ------------------------------------------------------------------ Popeye: Soco de marinheiro
def soco_de_marinheiro(rng, v):
    """Manivela cômica: catraca acelerando e o apito subindo, o soco sai com um "pow" e as estrelinhas."""
    x = _z(1.15)
    poe(x, _catraca(rng, 0.38, 9, 32, g=0.75), 0.0)
    n = n_de(0.4)
    t = _t(n)
    apito = np.sin(2 * math.pi * np.cumsum(varre(380, 1250, n, 0.9) * (1 + 0.015 * np.sin(2 * math.pi * 8 * t))) / SR)
    poe(x, apito * sobe_e_some(n, 0.9, 1.4) * 0.22, 0.0)
    poe(x, _whoosh(rng, 0.1, 600, 3000, 0.85, g=0.7), 0.33)
    poe(x, B.soco_pesado(rng, v) * 1.0, 0.4)
    m = n_de(0.12)
    poe(x, satura(passa(ruido(rng, m), 500, 4000, 2) * env(m, 0.001, 0.04), 3) * 0.6, 0.4)
    poe(x, _tom(nota(72), nota(84), 0.16, 0.1, 0.16), 0.43)
    for k, nt in enumerate((88, 91, 95)):
        poe(x, _brilho(rng, 0.3, nota(nt), 0.09, SINO), 0.5 + 0.07 * k)
    return reverb(x, 0.3, 0.14)


# ------------------------------------------------------------------ Optimus: Machado de energon
def machado_de_energon(rng, v):
    """O zumbido de energia subindo com o machado, o arco pesado e o corte que crava com descarga."""
    x = _z(1.1)
    n = n_de(0.32)
    t = _t(n)
    f = varre(70, 110, n, 0.8)
    zum = satura(sum(seno(f * k * (1 + 0.003 * k), n) / k for k in range(1, 7)) * 0.7, 2.2) * (0.8 + 0.2 * np.sin(2 * math.pi * 14 * t))
    zum += seno(varre(700, 1400, n, 0.9), n) * 0.12
    poe(x, passa(zum, 60, 5000, 2) * sobe_e_some(n, 0.9, 1.3) * 0.35, 0.0)
    poe(x, _whoosh(rng, 0.24, 1600, 200, 0.75, 1.5, 0.9), 0.08)
    poe(x, B.corte_pesado(rng, v)[n_de(0.16):] * 1.0, 0.25)
    poe(x, B.esmagar(rng, v)[: n_de(0.5)] * 0.55, 0.25)
    m = n_de(0.6)
    descarga = passa(rosa(rng, m), 1500, 9000, 2) * env(m, 0.001, 0.08) * 0.4
    descarga += satura(seno(varre(1800, 120, m, 1.4), m), 3) * env(m, 0.001, 0.12) * 0.22
    descarga += graos(rng, m, 26, 0.0, 0.4, 2500, 10000, 0.003) * 0.3
    poe(x, descarga, 0.25)
    poe(x, B._placa_de_metal(rng, n_de(0.5), 140, 2500, 40, 0.15) * 0.3, 0.25)
    return reverb(x, 0.45, 0.2, 5500)


# ------------------------------------------------------------------ Bob Esponja: Karatê
def karate(rng, v):
    """O "tchop" seco da mão em faca, e as bolhas estourando em sequência."""
    x = _z(1.05)
    poe(x, assobio(rng, n_de(0.16), 900, 6500, 1.8, 0.4) * sobe_e_some(n_de(0.16), 0.9, 1.4) * 0.75, 0.0)
    m = n_de(0.3)
    tchop = B._tapa(rng, m, 1600, 7000, 0.01) * 1.3 + B._carne(rng, m, 0.03, 2.6) * 0.8 + B._baque_seco(rng, m, 130, 0.05) * 0.5
    tchop += _madeira_oca(rng, m, rng.uniform(420, 480)) * 0.3
    poe(x, tchop, 0.15)
    tempos = sorted(rng.uniform(0.3, 0.85, 8))
    for k, tb in enumerate(tempos):
        f0 = rng.uniform(380, 750)
        poe(x, _bloop(rng, rng.uniform(0.04, 0.07), f0, f0 * rng.uniform(2.2, 3.2), rng.uniform(0.28, 0.42)), tb)
        poe(x, estalo(rng, n_de(0.02), 2500, 9000, 0.002) * 0.12, tb + 0.002)
    return reverb(x, 0.35, 0.18)


# ------------------------------------------------------------------ Woody: Laço
def laco(rng, v):
    """A corda girando no alto (vuu-vuu), o arremesso, e o puxão: a corda estica e range apertando."""
    x = _z(1.05)
    poe(x, _vuvu(rng, 0.32, 6, 8, 1.2), 0.0)
    poe(x, assobio(rng, n_de(0.2), 700, 3200, 1.2, 0.45) * sobe_e_some(n_de(0.2), 0.6, 1.3) * 0.6, 0.24)
    m = n_de(0.1)
    poe(x, passa(rosa(rng, m), 300, 2500, 2) * env(m, 0.005, 0.04) * 0.35, 0.4)        # a laçada cai
    m = n_de(0.14)
    t = _t(m)
    estica = seno(varre(160, 95, m, 1.4), m) * env(m, 0.001, 0.06) * 0.5 + B._tapa(rng, m, 600, 3000, 0.008) * 0.9
    poe(x, satura(estica, 2.0), 0.5)                                               # o puxão: "tchuc" da corda esticando
    m = n_de(0.3)
    t = _t(m)
    trem = (0.5 + 0.5 * np.sign(np.sin(2 * math.pi * varre(70, 40, m, 1.0) * t))) * passa(ruido(rng, m), 400, 3000, 2)
    poe(x, trem * env(m, 0.01, 0.12) * 0.35, 0.52)                                  # a corda rangendo ao apertar
    poe(x, B._baque_seco(rng, n_de(0.25), 110, 0.05) * 0.45, 0.5)
    return reverb(x, 0.25, 0.12)


# ------------------------------------------------------------------ Azula: Fogo azul
def fogo_azul(rng, v):
    """Fogo de alta pressão: ignição seca, o jato chiando forte e reto, e as labaredas no alvo."""
    x = _z(1.05)
    n = n_de(0.62)
    t = _t(n)
    jato = passa(ruido(rng, n), 2200, 9000, 2) * 0.55 + passa(rosa(rng, n), 300, 2200, 2) * 0.8
    jato *= (1 + 0.15 * np.sin(2 * math.pi * 23 * t) * passa(ruido(rng, n), None, 30, 1) * 8)
    corpo = env(n, 0.006, 0.22, segura=0.32)
    poe(x, satura(jato * corpo, 1.5) * 0.75, 0.0)
    poe(x, passa(rosa(rng, n), 40, 220, 2) * corpo * 0.6, 0.0)
    m = n_de(0.08)
    poe(x, satura(passa(ruido(rng, m), 800, 6000, 2) * env(m, 0.0005, 0.02), 2.5) * 0.7, 0.0)   # ignição
    poe(x, B.fogo(rng, v) * 0.7, 0.1)
    poe(x, graos(rng, n_de(0.7), 40, 0.0, 0.6, 2500, 10000, 0.0025, 0.7) * 0.3, 0.12)
    m = n_de(0.4)
    poe(x, passa(rosa(rng, m), 80, 1200, 2) * env(m, 0.004, 0.14) * 0.55, 0.12)                  # "fuum" no alvo
    return reverb(x, 0.4, 0.18)


# ------------------------------------------------------------------ Coiote: Bigorna ACME
def bigorna(rng, v):
    """O assobio da queda descendo, o CLANG da bigorna esmagando e a poeira assentando."""
    x = _z(1.4)
    n = n_de(0.38)
    t = _t(n)
    f = varre(2100, 520, n, 1.0) * (1 + 0.012 * np.sin(2 * math.pi * 7 * t))
    queda = seno(f, n) * env(n, 0.03, 0.4, segura=0.3) * 0.22 + seno(f * 2, n) * env(n, 0.03, 0.4, segura=0.3) * 0.03
    poe(x, queda, 0.0)
    batida = 0.3
    m = n_de(0.9)
    clang = B._placa_de_metal(rng, m, 230, 5200, 60, 0.35) * 0.55
    clang += modal(m, rng.uniform(260, 290), rng=rng, **METAL) * env(m, 0.0005, 0.3) * 0.35
    clang += B._tapa(rng, m, 1800, 9000, 0.006) * 1.0
    poe(x, clang, batida)
    poe(x, B.esmagar(rng, v) * 0.85, batida)
    m = n_de(0.8)
    poeira = passa(rosa(rng, m), 120, 1600, 2) * env(m, 0.03, 0.3) * 0.45 + graos(rng, m, 30, 0.05, 0.6, 900, 4500, 0.006) * 0.25
    poe(x, poeira, batida + 0.03)
    return reverb(x, 0.5, 0.2, 5000)


# ------------------------------------------------------------------ Tom: Frigideira
def frigideira(rng, v):
    """O balanço da frigideira e o BONG oco de metal que fica vibrando (com o "uá-uá" da panela tremendo)."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.2, 500, 2600, 0.85, g=0.7), 0.0)
    m = n_de(1.05)
    t = _t(m)
    f0 = rng.uniform(330, 370)
    vib = 1 + 0.012 * np.sin(2 * math.pi * 9 * t) * np.exp(-t / 0.5)
    bong = np.zeros(m)
    for r, q, g in ((1.0, 0.55, 1.0), (1.47, 0.4, 0.55), (2.09, 0.3, 0.42), (2.56, 0.22, 0.3), (3.9, 0.12, 0.2), (5.3, 0.08, 0.12)):
        bong += np.sin(2 * math.pi * np.cumsum(f0 * r * vib) / SR) * np.exp(-t / q) * g
    bong *= 0.75 + 0.25 * np.sin(2 * math.pi * 6 * t + 0.5)                       # a panela tremendo
    poe(x, bong * 0.4, 0.17)
    poe(x, B._tapa(rng, n_de(0.1), 1500, 7000, 0.006) * 0.9 + B._baque_seco(rng, n_de(0.1), 140, 0.03) * 0.6, 0.17)
    for k in range(3):                                                              # passarinhos/estrelinhas
        mm = n_de(0.08)
        tt = _t(mm)
        piu = np.sin(2 * math.pi * np.cumsum(varre(2700, 3600, mm, 0.6) * (1 + 0.05 * np.sin(2 * math.pi * 45 * tt))) / SR)
        poe(x, piu * env(mm, 0.004, 0.035) * 0.05, 0.55 + 0.12 * k)
    return reverb(x, 0.35, 0.15)


# ------------------------------------------------------------------ Esqueleto: Cajado da Caveira
def cajado_da_caveira(rng, v):
    """A pancada seca de osso e cajado, e a magia sinistra: acorde menor grave vibrando, sopro e cintilas descendo."""
    x = _z(1.25)
    poe(x, _whoosh(rng, 0.22, 1400, 250, 0.8, 1.5, 0.8), 0.0)
    m = n_de(0.4)
    poe(x, B.soco_pesado(rng, v)[:m] * 0.8 + _madeira_oca(rng, m, rng.uniform(280, 320)) * 0.45, 0.2)
    n = n_de(0.95)
    t = _t(n)
    trem = 0.7 + 0.3 * np.sin(2 * math.pi * 7 * t)
    acorde = sum(seno(nota(nt) * (1 + 0.004 * np.sin(2 * math.pi * 5 * t + nt)), n) for nt in (45, 48, 51, 57)) * 0.12
    acorde = satura(acorde * 1.5, 1.8) * trem * sobe_e_some(n, 0.25, 1.4)
    poe(x, passa(acorde, 70, 3000, 2) * 0.8, 0.24)
    sopro = assobio(rng, n, 900, 300, 1.0, 0.5) * sobe_e_some(n, 0.3, 1.2) * 0.35
    poe(x, sopro, 0.24)
    for k in range(9):
        poe(x, _brilho(rng, 0.25, nota(96 - 2 * k + rng.uniform(-0.3, 0.3)), 0.05, CRISTAL), 0.3 + 0.065 * k)
    return reverb(x, 0.6, 0.28, 5000)


# ------------------------------------------------------------------ Lion-O: Espada de Augúrio
def espada_de_augurio(rng, v):
    """O corte da espada ("shiiing") e o brilho do Olho: um clarão cristalino que sobe em três notas."""
    x = _z(1.3)
    poe(x, assobio(rng, n_de(0.18), 900, 7000, 1.4, 0.4) * sobe_e_some(n_de(0.18), 0.85, 1.3) * 0.8, 0.0)
    poe(x, B.corte_pesado(rng, v)[n_de(0.16):] * 0.9, 0.13)
    m = n_de(0.5)
    poe(x, B._lamina_curta(rng, m, 3000) * env(m, 0.001, 0.2) * 0.35, 0.13)
    for k, nt in enumerate((79, 86, 91)):
        poe(x, _brilho(rng, 0.7, nota(nt), 0.13, CRISTAL), 0.3 + 0.07 * k)
    n = n_de(0.5)
    poe(x, seno(varre(3000, 6000, n, 0.8), n) * sobe_e_some(n, 0.3, 1.3) * 0.05, 0.3)
    poe(x, passa(rosa(rng, n), 4000, 11000, 2) * sobe_e_some(n, 0.2, 1.4) * 0.12, 0.3)
    return reverb(x, 0.55, 0.25, 8000)


# nome do arquivo (com hífen) → (função, descrição)
SONS: dict = {
    "sais": (sais, "básico do Raphael: duas estocadas metálicas dos sais"),
    "nunchakus": (nunchakus, "básico do Michelangelo: giro \"vuvuvu\" e dois golpes de madeira"),
    "bicada": (bicada, "básico do Pica-Pau e do Patolino: bicadas rapidíssimas em madeira"),
    "golpe-alienigena": (golpe_alienigena, "básico do Ben 10: \"zwip\" do Omnitrix e o golpe do alien"),
    "soco-de-marinheiro": (soco_de_marinheiro, "básico do Popeye: manivela cômica e o soco com estrelinhas"),
    "machado-de-energon": (machado_de_energon, "básico do Optimus: zumbido de energia e corte pesado"),
    "karate": (karate, "básico do Bob Esponja: \"tchop\" e bolhas estourando"),
    "laco": (laco, "básico do Woody: corda girando, arremesso e puxão"),
    "fogo-azul": (fogo_azul, "básico da Azula: jato de fogo de alta pressão"),
    "bigorna": (bigorna, "básico do Coiote: assobio da queda, CLANG e poeira"),
    "frigideira": (frigideira, "básico do Tom: frigideira BONG vibrando"),
    "cajado-da-caveira": (cajado_da_caveira, "básico do Esqueleto: pancada do cajado e magia sinistra"),
    "espada-de-augurio": (espada_de_augurio, "básico do Lion-O: corte da espada e o brilho do Olho"),
}
