"""Os sons da rodada 12: Kaiba, Pantera Negra, Feiticeira Escarlate, Visão e Homem-Formiga (veja
tools/vfx/familias_v2/rodada12.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _rugido(rng, seg, f0=110, f1=70, g=0.3):
    """O rugido de dragão: o tom grave áspero que treme, com o sopro rasgado por cima."""
    n = n_de(seg)
    t = _t(n)
    f = np.linspace(f0, f1, n) * (1 + 0.04 * np.sin(2 * math.pi * 9 * t))
    voz = satura(np.sin(2 * math.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.abs(np.sin(2 * math.pi * 31 * t))), 4)
    sopro = passa(rosa(rng, n), 300, 3000, 2) * 0.5
    return passa(voz * 0.7 + sopro, 70, 4000, 2) * sobe_e_some(n, 0.3, 1.3) * g


def _zumbido(n, f, g=0.1, trem=6.0):
    t = _t(n)
    return (seno(f, n) + seno(f * 2.01, n) * 0.4) * (0.7 + 0.3 * np.sin(2 * math.pi * trem * t)) * g


def _fio_magico(rng, seg, f0, f1, g=0.1):
    """O fio de magia do caos: o tom que ondula e o chiado sedoso."""
    n = n_de(seg)
    t = _t(n)
    f = varre(f0, f1, n, 1.0) * (1 + 0.06 * np.sin(2 * math.pi * 7 * t))
    return (np.sin(2 * math.pi * np.cumsum(f) / SR) * 0.6 + passa(rosa(rng, n), 2000, 7000, 2) * 0.5) * sobe_e_some(n, 0.4, 1.3) * g


def _bip(f, seg=0.05, g=0.08):
    n = n_de(seg)
    return seno(f, n) * env(n, 0.002, seg * 0.8) * g


# =================================================================== Kaiba
def ultimate_preparo(rng, v):
    """O Preparo do Ultimate Burst: as três bocas carregando (três zumbidos subindo em acorde) e o rosnado baixo
    do Dragão Supremo."""
    x = _z(1.4)
    n = n_de(1.2)
    for k, f in enumerate((220, 277, 330)):
        poe(x, seno(varre(f * 0.7, f, n, 0.8), n) * sobe_e_some(n, 0.8, 1.2) * 0.05, 0.03 * k)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.8, 1.3) * 0.12, 0.0)
    poe(x, _rugido(rng, 0.9, 90, 70, 0.22), 0.15)
    return reverb(x, 0.5, 0.25)


def explosao_ultimate(rng, v):
    """O Ultimate Burst: o rugido triplo, os três raios rasgando juntos (o chiado elétrico forte), a explosão
    branca enorme (o estrondo com a cauda longa) e o crepitar das brasas."""
    x = _z(2.2)
    for k in range(3):
        poe(x, _rugido(rng, 0.4, 150 - 15 * k, 100, 0.2), 0.02 * k)
    n = n_de(0.4)
    poe(x, satura(passa(rosa(rng, n), 800, 8000, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 60 * _t(n))), 2) * sobe_e_some(n, 0.6, 1.2) * 0.5, 0.05)
    poe(x, _whoosh(rng, 0.3, 500, 3000, 0.9, 1.4, 0.4), 0.05)
    poe(x, baque(n_de(1.0), 60, 30, 0.4, 0.8) * 1.0, 0.25)
    m = n_de(1.2)
    poe(x, passa(rosa(rng, m), 40, 2000, 2) * env(m, 0.003, 0.6) * 0.7, 0.25)
    poe(x, graos(rng, n_de(1.0), 40, 0.0, 0.9, 1500, 6000, 0.005) * 0.3, 0.55)
    return reverb(x, 0.7, 0.32)


# =================================================================== Pantera Negra
def habito_cinetico(rng, v):
    """O hábito de vibranium: a malha acendendo (o zumbido roxo subindo), os quatro golpes absorvidos (o baque
    abafado e o "vuum" que corre pela malha a cada um) e a casca fechando (o tom cheio e firme)."""
    x = _z(1.7)
    n = n_de(0.4)
    poe(x, seno(varre(180, 360, n, 1.0), n) * sobe_e_some(n, 0.7, 1.3) * 0.06, 0.0)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * sobe_e_some(n, 0.7, 1.3) * 0.1, 0.0)
    for k, t0 in enumerate((0.15, 0.25, 0.35, 0.45)):
        poe(x, passa(baque(n_de(0.2), 140, 80, 0.05, 0.4), None, 1500, 2) * 0.4, t0)
        m = n_de(0.3)
        poe(x, seno(varre(500 + 60 * k, 180, m, 1.0), m) * env(m, 0.005, 0.22) * 0.08, t0 + 0.02)
    m = n_de(0.8)
    poe(x, _zumbido(m, 147, 0.08) * sobe_e_some(m, 0.15, 1.4), 0.6)
    poe(x, _brilho(rng, 0.6, 880, 0.08, CRISTAL), 0.6)
    return reverb(x, 0.45, 0.22)


def vibranio_preparo(rng, v):
    """O Preparo da Descarga real: a energia sendo puxada (os "vuu" que sobem, rápidos, vindo de todos os
    lados) e o zumbido do peito crescendo."""
    x = _z(1.4)
    for k in range(7):
        m = n_de(0.18)
        poe(x, seno(varre(300 + 40 * k, 700 + 40 * k, m, 1.0), m) * sobe_e_some(m, 0.8, 1.3) * 0.05, 0.05 + 0.14 * k)
    n = n_de(1.2)
    poe(x, _zumbido(n, 98, 0.1, 8) * sobe_e_some(n, 0.9, 1.1), 0.0)
    poe(x, passa(rosa(rng, n), 300, 1500, 2) * sobe_e_some(n, 0.9, 1.2) * 0.12, 0.0)
    return reverb(x, 0.45, 0.22)


def descarga_real(rng, v):
    """A Descarga real: a energia se apertando (o som sugado ao contrário, subindo), um instante de silêncio, e
    a explosão roxa (o estrondo grave com o "vwoom" que se espalha) com os cacos tinindo."""
    x = _z(2.0)
    n = n_de(0.32)
    poe(x, passa(rosa(rng, n), 200, 4000, 2) * (np.linspace(0, 1, n) ** 2) * 0.5, 0.0)
    poe(x, seno(varre(150, 600, n, 2.0), n) * (np.linspace(0, 1, n) ** 2) * 0.08, 0.0)
    poe(x, baque(n_de(0.9), 55, 28, 0.32, 0.9) * 1.0, 0.33)
    m = n_de(0.9)
    poe(x, seno(varre(220, 70, m, 0.7), m) * env(m, 0.002, 0.5) * 0.18, 0.33)
    poe(x, passa(rosa(rng, m), 60, 1800, 2) * env(m, 0.002, 0.4) * 0.5, 0.33)
    for k in range(6):
        poe(x, _brilho(rng, 0.3, 1800 + 230 * k, 0.05, VIDRO), 0.42 + 0.05 * k)
    return reverb(x, 0.6, 0.3)


# =================================================================== Feiticeira Escarlate
def hex_de_probabilidade(rng, v):
    """O hex: os fios saindo da mão (os sussurros ondulantes, em três vozes), o redemoinho girando (o "uuu" que
    gira e aperta) e o sinal acendendo (o acorde estranho, meio desafinado), com o tilintar tonto."""
    x = _z(1.8)
    for k in range(3):
        poe(x, _fio_magico(rng, 0.5, 600 + 150 * k, 900 + 100 * k, 0.07), 0.02 * k)
    n = n_de(0.7)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 400, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * (3 + 6 * t) * t)) * sobe_e_some(n, 0.6, 1.2) * 0.25, 0.25)
    m = n_de(0.8)
    poe(x, (seno(392, m) + seno(415, m) * 0.7 + seno(587, m) * 0.5) * env(m, 0.01, 0.5) * 0.06, 0.42)
    for k in range(5):
        poe(x, _brilho(rng, 0.25, 2200 + 300 * ((k * 3) % 5), 0.04, SINO), 0.65 + 0.06 * k)
    return reverb(x, 0.55, 0.3)


def telecinese_escarlate(rng, v):
    """A telecinese: as faixas chegando (os "fwum" que se fecham), o aperto (o grave que treme e range) e o
    Preparo empurrado para trás (o tom que desce, como uma fita voltando)."""
    x = _z(1.7)
    for k in range(4):
        poe(x, _whoosh(rng, 0.25, 400, 1400, 0.8, 1.4, 0.3), 0.05 * k)
    n = n_de(0.45)
    t = _t(n)
    poe(x, satura(seno(70 + 8 * np.sin(2 * math.pi * 14 * t), n), 3) * sobe_e_some(n, 0.4, 1.2) * 0.18, 0.35)
    poe(x, graos(rng, n, 25, 0.0, 0.4, 300, 1500, 0.01) * 0.25, 0.35)
    m = n_de(0.4)
    poe(x, seno(varre(900, 300, m, 1.0), m) * env(m, 0.01, 0.3) * 0.06, 0.45)
    poe(x, passa(rosa(rng, m), 1500, 5000, 2) * sobe_e_some(m, 0.3, 1.2) * 0.1, 0.45)
    return reverb(x, 0.5, 0.25)


def caos_preparo(rng, v):
    """O Preparo da Distorção: a tiara acendendo (o sino grave) e os fios girando nas mãos (os sussurros que
    sobem e descem, em volta)."""
    x = _z(1.4)
    poe(x, _brilho(rng, 1.1, 330, 0.12, SINO), 0.0)
    for k in range(4):
        poe(x, _fio_magico(rng, 0.45, 500 + 100 * (k % 2), 800 - 100 * (k % 2), 0.06), 0.1 + 0.22 * k)
    n = n_de(1.2)
    poe(x, seno(55, n) * sobe_e_some(n, 0.6, 1.2) * 0.1, 0.0)
    return reverb(x, 0.55, 0.3)


def distorcao_do_caos(rng, v):
    """A Distorção do caos: a onda rolando (o rugido de vento vermelho com as vozes), o espaço entortando (o tom
    que entorta, desafinando para cima e para baixo) e a realidade trincando (os vidros quebrando espalhados)."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.5, 300, 1500, 0.7, 1.3, 0.6), 0.0)
    for k in range(3):
        poe(x, _fio_magico(rng, 0.5, 400 + 200 * k, 700 + 150 * k, 0.05), 0.05 * k)
    n = n_de(0.9)
    t = _t(n)
    f = 180 * (1 + 0.25 * np.sin(2 * math.pi * 3.5 * t) * np.linspace(0, 1, n))
    poe(x, satura(np.sin(2 * math.pi * np.cumsum(f) / SR), 2) * sobe_e_some(n, 0.3, 1.3) * 0.12, 0.3)
    poe(x, baque(n_de(0.6), 70, 35, 0.22, 0.4) * 0.6, 0.3)
    for k in range(7):
        poe(x, modal(n_de(0.35), 2500 + 400 * k, rng=rng, desafina=0.05, **VIDRO) * env(n_de(0.35), 0.0005, 0.15) * 0.06, 0.45 + 0.07 * k)
        poe(x, estalo(rng, n_de(0.02), 3000, 9000) * 0.2, 0.45 + 0.07 * k)
    return reverb(x, 0.65, 0.32)


# =================================================================== Visão
def faseamento(rng, v):
    """O faseamento: o corpo mudando de densidade (o tom oco que se desdobra em eco e fica fantasma), a
    varredura (o chiado que passa) e o golpe atravessando sem acertar (o "fwoosh" que passa limpo)."""
    x = _z(1.6)
    n = n_de(1.0)
    base = seno(varre(400, 260, n, 1.0), n) * sobe_e_some(n, 0.25, 1.4) * 0.08
    for k in range(3):
        poe(x, base * (0.8 ** k), 0.0 + 0.06 * k)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.5, 1.3) * 0.08, 0.05)
    poe(x, _whoosh(rng, 0.35, 800, 2500, 0.5, 1.3, 0.45), 0.35)
    poe(x, _brilho(rng, 0.6, 1400, 0.05, CRISTAL), 0.0)
    return reverb(x, 0.55, 0.3)


def raio_solar(rng, v):
    """O raio solar: a Joia da Mente acendendo (o tinido limpo que sobe), o raio saindo (o zumbido quente e
    grosso que ferve) e a explosão de sol no rival (o estouro brilhante)."""
    x = _z(1.7)
    poe(x, _brilho(rng, 0.5, 1760, 0.12, CRISTAL), 0.0)
    m = n_de(0.2)
    poe(x, seno(varre(800, 1600, m, 1.0), m) * sobe_e_some(m, 0.8, 1.3) * 0.06, 0.0)
    n = n_de(0.45)
    t = _t(n)
    zum = (satura(seno(160, n), 2.5) * 0.5 + passa(rosa(rng, n), 600, 5000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 40 * t))) * sobe_e_some(n, 0.2, 1.3)
    poe(x, zum * 0.35, 0.15)
    poe(x, baque(n_de(0.4), 110, 55, 0.12, 0.6) * 0.6, 0.27)
    poe(x, passa(rosa(rng, n_de(0.5)), 1500, 9000, 2) * env(n_de(0.5), 0.001, 0.25) * 0.3, 0.27)
    return reverb(x, 0.5, 0.25)


def computacao_preparo(rng, v):
    """O Preparo da Computação: os circuitos girando (os bipes rápidos em padrão) e o zumbido digital baixo."""
    x = _z(1.4)
    n = n_de(1.2)
    poe(x, _zumbido(n, 110, 0.07, 12) * sobe_e_some(n, 0.5, 1.1), 0.0)
    padrao = (1568, 1175, 1760, 1319, 2093, 1568, 1175, 1976)
    for k in range(16):
        poe(x, _bip(padrao[k % 8], 0.035, 0.05), 0.05 + 0.07 * k)
    return reverb(x, 0.35, 0.18)


def computacao_sintetica(rng, v):
    """A computação sintética: a grade varrendo (o chiado de leitura e os bipes subindo), a trajetória calculada
    (os pontinhos em sequência), o raio exato (o "tsiu" fino e seco) e o anel do Preparo quebrando (o vidro que
    se parte e cai)."""
    x = _z(1.8)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 4000, 10000, 2) * sobe_e_some(n, 0.5, 1.2) * 0.1, 0.0)
    for k in range(6):
        poe(x, _bip(900 + 180 * k, 0.03, 0.06), 0.02 + 0.05 * k)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.02), 3000, 9000, 0.003) * 0.25, 0.15 + 0.03 * k)
    m = n_de(0.15)
    poe(x, seno(varre(3500, 1200, m, 1.0), m) * env(m, 0.001, 0.12) * 0.1, 0.42)
    poe(x, estalo(rng, n_de(0.03), 2000, 8000) * 0.5, 0.45)
    q = n_de(0.6)
    poe(x, modal(q, 2100, rng=rng, desafina=0.03, **VIDRO) * env(q, 0.0005, 0.25) * 0.18, 0.47)
    poe(x, graos(rng, n_de(0.5), 8, 0.05, 0.45, 2500, 8000, 0.006) * 0.3, 0.55)
    return reverb(x, 0.4, 0.2)


# =================================================================== Homem-Formiga
def encolhimento(rng, v):
    """O encolhimento: o som do traje encolhendo (o tom que sobe rápido até sumir, com o chiado Pym), o
    zigue-zague (os "zip" agudos curtos de um lado para o outro) e os golpes rápidos e pequenos (os estalos
    secos em rajada)."""
    x = _z(1.6)
    n = n_de(0.3)
    poe(x, seno(varre(300, 2400, n, 2.0), n) * sobe_e_some(n, 0.85, 1.3) * 0.08, 0.0)
    poe(x, passa(rosa(rng, n), 3000, 10000, 2) * sobe_e_some(n, 0.8, 1.3) * 0.15, 0.0)
    poe(x, _brilho(rng, 0.3, 3200, 0.06, CRISTAL), 0.28)
    for k in range(6):
        m = n_de(0.04)
        poe(x, seno(varre(2400 if k % 2 else 3000, 1800, m, 1.0), m) * env(m, 0.002, 0.03) * 0.06, 0.3 + 0.03 * k)
    for k in range(5):
        poe(x, baque(n_de(0.1), 240, 140, 0.025, 0.7) * 0.3, 0.48 + 0.05 * k)
        poe(x, estalo(rng, n_de(0.02), 2500, 9000, 0.004) * 0.35, 0.48 + 0.05 * k)
    m = n_de(0.5)
    poe(x, seno(varre(500, 250, m, 0.7), m) * sobe_e_some(m, 0.2, 1.3) * 0.04, 0.8)
    return reverb(x, 0.4, 0.2)


SONS: dict = {
    "ultimate-preparo": (ultimate_preparo, "Kaiba: as três bocas carregando (antes do golpe)"),
    "explosao-ultimate": (explosao_ultimate, "Kaiba: o rugido triplo, os raios e a explosão"),
    "habito-cinetico": (habito_cinetico, "Pantera Negra: a malha absorvendo os golpes"),
    "vibranio-preparo": (vibranio_preparo, "Pantera Negra: a energia indo para o peito (antes do golpe)"),
    "descarga-real": (descarga_real, "Pantera Negra: a energia apertando e explodindo"),
    "hex-de-probabilidade": (hex_de_probabilidade, "Feiticeira: os fios, o redemoinho e o sinal"),
    "telecinese-escarlate": (telecinese_escarlate, "Feiticeira: as faixas agarrando e apertando"),
    "caos-preparo": (caos_preparo, "Feiticeira: a tiara e os fios (antes do golpe)"),
    "distorcao-do-caos": (distorcao_do_caos, "Feiticeira: a onda do caos e a realidade trincando"),
    "faseamento": (faseamento, "Visão: o corpo fantasma e o golpe atravessando"),
    "raio-solar": (raio_solar, "Visão: a Joia da Mente e o raio solar"),
    "computacao-preparo": (computacao_preparo, "Visão: os circuitos girando (antes do golpe)"),
    "computacao-sintetica": (computacao_sintetica, "Visão: o cálculo, o raio exato e o anel quebrando"),
    "encolhimento": (encolhimento, "Homem-Formiga: encolhendo, o zigue-zague e os golpes"),
}
