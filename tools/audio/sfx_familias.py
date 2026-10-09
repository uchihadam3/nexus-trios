"""
Um som próprio para cada família nova de efeito visual (tools/vfx/familias_v2).

Mesmo método da biblioteca da parte 6: camadas (transiente, corpo, cauda),
4 versões por arquivo, volume pela prioridade da mixagem. Cada receita foi
pensada junto do desenho: o "bonk" tem a mola, a fênix tem o grito, o relógio
tem o tique-taque que trava, a Hipnose tem o tremolo que gira.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from som import (CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, graos, modal, n_de, passa, poe, reverb,
                 rosa, ruido, satura, seno, sobe_e_some, varre)

nota = B.nota


def _z(seg):
    return np.zeros(n_de(seg))


def _corta(x, seg):
    n = n_de(seg)
    return x[:n] if len(x) >= n else np.concatenate([x, np.zeros(n - len(x))])


def _whoosh(rng, seg, f0, f1, pico=0.7, forma=1.4, g=0.8):
    n = n_de(seg)
    return assobio(rng, n, f0, f1, 1.2, 0.45) * sobe_e_some(n, pico, forma) * g


def _tom(f0, f1, seg, queda, g=0.3, forma=1.0):
    n = n_de(seg)
    return seno(varre(f0, f1, n, forma), n) * env(n, 0.002, queda) * g


def _brilho(rng, seg, f0, g=0.2, tipo=CRISTAL):
    n = n_de(seg)
    return modal(n, f0, rng=rng, **tipo) * env(n, 0.001, seg * 0.5) * g


# ================================================================== corpo
def chute_voador(rng, v):
    x = _z(0.6)
    poe(x, _whoosh(rng, 0.22, 400, 4000, 0.85), 0)
    poe(x, B.soco_pesado(rng, v), 0.2, 0.9)
    poe(x, estalo(rng, n_de(0.08), 2000, 8000, 0.006), 0.2, 0.6)
    return x


def chute_giratorio(rng, v):
    x = _z(0.7)
    for k in range(2):
        poe(x, _whoosh(rng, 0.18, 600 + 300 * k, 2600, 0.6, g=0.6), k * 0.14)
    poe(x, B.soco_leve(rng, v), 0.3, 1.0)
    poe(x, passa(rosa(rng, n_de(0.3)), 200, 1500, 2) * env(n_de(0.3), 0.01, 0.12) * 0.3, 0.32)
    return x



def pow_cartoon(rng, v):
    x = _z(0.6)
    poe(x, B.soco_pesado(rng, v), 0, 0.9)
    poe(x, satura(passa(ruido(rng, n_de(0.12)), 500, 4000, 2) * env(n_de(0.12), 0.001, 0.04), 3) * 0.8, 0)
    poe(x, _tom(nota(74), nota(86), 0.18, 0.12, 0.2), 0.05)
    return reverb(x, 0.3, 0.15)



def investida(rng, v):
    x = _z(0.8)
    n = n_de(0.3)
    poe(x, assobio(rng, n, 200, 2500, 0.8, 0.5) * sobe_e_some(n, 0.95, 1.2) * 0.9, 0)
    poe(x, B.soco_pesado(rng, v), 0.26, 1.1)
    poe(x, graos(rng, n_de(0.4), 14, 0.0, 0.2, 800, 4000, 0.006) * 0.3, 0.28)
    return x


def punho_gigante(rng, v):
    x = _z(1.0)
    poe(x, _tom(nota(40), nota(52), 0.35, 0.3, 0.35), 0)
    poe(x, _whoosh(rng, 0.32, 150, 1800, 0.95, g=0.7), 0)
    poe(x, B.esmagar(rng, v), 0.3, 1.0)
    return x


def soco_serio(rng, v):
    x = _z(1.5)
    poe(x, B.soco_leve(rng, v), 0, 0.6)
    n = n_de(1.4)
    vento = assobio(rng, n, 5000, 120, 0.5, 0.6) * env(n, 0.01, 0.6) * 1.1
    poe(x, vento, 0.05)
    poe(x, baque(n_de(1.0), 50, 25, 0.5, 0.4) * 1.2, 0.05)
    return reverb(x, 0.8, 0.3, 4000)


def faisca_negra(rng, v):
    x = _z(0.8)
    poe(x, B.soco_pesado(rng, v), 0, 1.0)
    n = n_de(0.6)
    crep = graos(rng, n, 40, 0.0, 0.35, 2500, 9000, 0.003) * 0.5
    zumbido = satura(seno(varre(110, 60, n, 0.6), n), 4) * env(n, 0.002, 0.2) * 0.3
    poe(x, crep + zumbido, 0.02)
    return reverb(x, 0.4, 0.2)


def chicote(rng, v):
    x = _z(0.6)
    poe(x, _whoosh(rng, 0.25, 300, 6000, 0.9, 2.0, 0.6), 0)
    n = n_de(0.15)
    crack = passa(ruido(rng, n), 2000, 10000, 2) * env(n, 0.0003, 0.008) * 1.4 + baque(n, 900, 400, 0.01, 0.6) * 0.3
    poe(x, crack, 0.24)
    return reverb(x, 0.5, 0.25)


def garras(rng, v):
    x = _z(0.6)
    for k in range(3):
        n = n_de(0.16)
        r = passa(ruido(rng, n), 1500, 7000, 2) * env(n, 0.002, 0.05) * 0.7
        r += modal(n, rng.uniform(2200, 3000), rng=rng, **METAL) * env(n, 0.001, 0.06) * 0.15
        poe(x, r, k * 0.05)
    poe(x, baque(n_de(0.2), 120, 60, 0.05, 0.2) * 0.5, 0.02)
    return reverb(x, 0.3, 0.15)


def mordida(rng, v):
    x = _z(0.5)
    poe(x, _whoosh(rng, 0.12, 800, 2500, 0.5, g=0.4), 0)
    n = n_de(0.2)
    chomp = baque(n, 200, 90, 0.05, 0.6) * 0.7 + satura(passa(ruido(rng, n), 400, 3000, 2) * env(n, 0.001, 0.03), 3) * 0.7
    poe(x, chomp, 0.1)
    poe(x, graos(rng, n_de(0.2), 6, 0.0, 0.08, 2000, 6000, 0.004) * 0.4, 0.12)
    return reverb(x, 0.2, 0.1)


def bastao(rng, v):
    x = _z(0.6)
    poe(x, _whoosh(rng, 0.28, 300, 1600, 0.85, 1.6, 0.8), 0)
    n = n_de(0.3)
    toc = baque(n, 260, 140, 0.06, 0.5) * 0.7 + modal(n, rng.uniform(500, 700), rng=rng, razoes=[1, 2.6, 4.1], quedas=[0.08, 0.05, 0.03]) * 0.25
    poe(x, toc, 0.26)
    return reverb(x, 0.3, 0.15)


def tentaculos(rng, v):
    x = _z(0.9)
    for k in range(4):
        n = n_de(0.25)
        slosh = passa(rosa(rng, n), 150, 900, 2) * sobe_e_some(n, 0.4, 1.5) * 0.6
        poe(x, slosh, k * 0.08)
    poe(x, B.soco_leve(rng, v), 0.32, 0.8)
    poe(x, satura(passa(ruido(rng, n_de(0.4)), 80, 400, 2) * env(n_de(0.4), 0.02, 0.15), 2) * 0.4, 0.3)
    return reverb(x, 0.35, 0.2, 3000)


def pisao(rng, v):
    x = B.terremoto(rng, v)[: n_de(1.0)] * 0.6
    poe(x, baque(n_de(0.6), 65, 30, 0.2, 0.5) * 1.2, 0)
    poe(x, graos(rng, n_de(0.8), 30, 0.02, 0.5, 600, 3500, 0.006) * 0.35, 0)
    return x


def esticar(rng, v):
    x = _z(0.9)
    poe(x, _tom(200, 900, 0.25, 0.2, 0.25, 0.6), 0)
    poe(x, B.soco_leve(rng, v), 0.2, 1.0)
    t = np.arange(n_de(0.4)) / SR
    boing = np.sin(2 * math.pi * (240 + 80 * np.sin(2 * math.pi * 12 * t)) * t) * np.exp(-t / 0.15) * 0.3
    poe(x, boing, 0.45)
    return reverb(x, 0.2, 0.12)


# ================================================================== cortes
def corte_vertical(rng, v):
    x = B.corte(rng, v)
    poe(x, baque(n_de(0.2), 140, 70, 0.04, 0.2) * 0.4, 0.12)
    return x



def mil_cortes(rng, v):
    x = _z(1.1)
    for k in range(10):
        n = n_de(0.08)
        poe(x, passa(ruido(rng, n), 3000, 11000, 2) * env(n, 0.0005, 0.015) * 0.5 + modal(n, rng.uniform(2500, 4000), rng=rng, **METAL) * env(n, 0.001, 0.04) * 0.12, 0.03 + k * 0.055)
    poe(x, B.corte_pesado(rng, v), 0.62, 0.9)
    return x


def foice(rng, v):
    x = _z(1.0)
    n = n_de(0.45)
    poe(x, assobio(rng, n, 200, 1400, 1.0, 0.5) * sobe_e_some(n, 0.7, 1.5) * 0.9, 0)
    poe(x, B.corte(rng, v), 0.3, 0.7)
    poe(x, B.sombra(rng, v)[: n_de(0.6)] * 0.4, 0.3)
    return x


def espadao(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.3, 200, 1800, 0.85, g=1.0), 0)
    poe(x, B.corte_pesado(rng, v), 0.2, 0.8)
    poe(x, B.esmagar(rng, v)[: n_de(0.8)] * 0.6, 0.24)
    return x


def lamina_de_fogo(rng, v):
    x = B.corte(rng, v)
    x = np.concatenate([x, np.zeros(n_de(0.4))])
    poe(x, B.fogo(rng, v)[: n_de(0.7)] * 0.6, 0.1)
    return x


def lamina_eletrica(rng, v):
    x = B.corte(rng, v)
    x = np.concatenate([x, np.zeros(n_de(0.3))])
    poe(x, graos(rng, n_de(0.5), 30, 0, 0.3, 3000, 10000, 0.002) * 0.6, 0.1)
    n = n_de(0.4)
    poe(x, satura(seno(varre(120, 120, n), n), 6) * env(n, 0.002, 0.12) * 0.2, 0.1)
    return x


def lamina_sombria(rng, v):
    x = B.corte(rng, v)
    x = np.concatenate([x, np.zeros(n_de(0.5))])
    n = n_de(0.7)
    poe(x, passa(rosa(rng, n), 80, 600, 2) * env(n, 0.05, 0.3) * 0.6 + _tom(nota(40), nota(34), 0.7, 0.4, 0.2), 0.1)
    return reverb(x, 0.6, 0.3, 2500)


def motosserra(rng, v):
    n = n_de(0.9)
    t = np.arange(n) / SR
    motor = satura(np.sign(np.sin(2 * math.pi * (95 + 25 * np.sin(2 * math.pi * 3 * t)) * t)) * 0.5 + passa(ruido(rng, n), 800, 5000, 2) * 0.4, 2)
    x = passa(motor, 100, 6000, 2) * env(n, 0.02, 0.4, segura=0.4) * 0.6
    x += graos(rng, n, 50, 0.05, 0.6, 3000, 9000, 0.002) * 0.4
    return x


def lamina_de_agua(rng, v):
    x = B.corte(rng, v)
    x = np.concatenate([x, np.zeros(n_de(0.4))])
    poe(x, B.agua(rng, v)[: n_de(0.7)] * 0.6, 0.08)
    return x


def disco(rng, v):
    n = n_de(0.6)
    t = np.arange(n) / SR
    zumbido = assobio(rng, n, 900, 1600, 1.0, 0.3) * (0.6 + 0.4 * np.sin(2 * math.pi * 18 * t)) * sobe_e_some(n, 0.6, 1.4) * 0.6
    return zumbido + modal(n, 1300, rng=rng, **METAL) * env(n, 0.001, 0.3) * 0.06


def ricochete(rng, v):
    x = _z(0.8)
    n = n_de(0.7)
    poe(x, modal(n, rng.uniform(900, 1100), rng=rng, **METAL) * env(n, 0.0005, 0.4) * 0.5, 0)
    poe(x, estalo(rng, n_de(0.08), 2000, 9000, 0.005) * 0.7, 0)
    poe(x, _tom(2500, 600, 0.25, 0.2, 0.18), 0.05)
    return reverb(x, 0.4, 0.2)


def florete(rng, v):
    x = _z(0.9)
    for k in range(5):
        n = n_de(0.12)
        poe(x, assobio(rng, n, 2000, 7000, 1.5, 0.35) * sobe_e_some(n, 0.8, 1.5) * 0.4 + modal(n, rng.uniform(3500, 4500), rng=rng, **METAL) * env(n, 0.001, 0.05) * 0.15, k * 0.11)
    return reverb(x, 0.25, 0.15)


# ================================================================== projéteis
def flecha(rng, v):
    x = _z(0.7)
    n = n_de(0.25)
    corda = seno(varre(220, 180, n), n) * env(n, 0.001, 0.08) * 0.35 + estalo(rng, n, 500, 3000, 0.004) * 0.4
    poe(x, corda, 0)
    poe(x, _whoosh(rng, 0.25, 2000, 5000, 0.5, g=0.4), 0.05)
    return x


def cravar(rng, v):
    n = n_de(0.4)
    x = baque(n, 400, 180, 0.03, 0.6) * 0.6 + estalo(rng, n, 800, 4000, 0.008) * 0.6
    t = np.arange(n) / SR
    x += np.sin(2 * math.pi * 140 * t) * np.exp(-t / 0.15) * (0.5 + 0.5 * np.sin(2 * math.pi * 30 * t)) * 0.25
    return reverb(x, 0.2, 0.1)


def tiro_preciso(rng, v):
    x = _z(0.9)
    n = n_de(0.2)
    poe(x, estalo(rng, n, 2000, 6000, 0.003) * 0.4, 0)
    poe(x, estalo(rng, n, 2000, 6000, 0.003) * 0.4, 0.08)
    poe(x, B.tiro(rng, v), 0.25, 1.1)
    return reverb(x, 0.6, 0.3, 5000)


def espingarda(rng, v):
    x = _z(0.9)
    n = n_de(0.6)
    poe(x, satura(passa(ruido(rng, n), 200, 3000, 2) * env(n, 0.001, 0.08), 3) * 0.9 + baque(n, 90, 45, 0.12, 0.6), 0)
    poe(x, graos(rng, n_de(0.4), 9, 0.04, 0.12, 1500, 6000, 0.005) * 0.6, 0.02)
    return reverb(x, 0.6, 0.25, 4000)


def teia(rng, v):
    x = _z(0.6)
    n = n_de(0.15)
    poe(x, passa(ruido(rng, n), 2500, 8000, 2) * env(n, 0.001, 0.05) * 0.6, 0)
    m = n_de(0.3)
    splat = passa(ruido(rng, m), 300, 2500, 2) * env(m, 0.001, 0.06) * 0.7 + _tom(400, 200, 0.3, 0.08, 0.2)
    poe(x, splat, 0.18)
    return x


def bolhas(rng, v):
    x = _z(0.9)
    for k in range(9):
        f = rng.uniform(500, 1400)
        n = n_de(0.08)
        poe(x, seno(varre(f, f * 2.2, n, 0.5), n) * env(n, 0.002, 0.03) * 0.3, rng.uniform(0, 0.7))
    return reverb(x, 0.3, 0.2)


def cartas(rng, v):
    x = _z(1.0)
    for k in range(4):
        n = n_de(0.06)
        poe(x, passa(ruido(rng, n), 2000, 8000, 2) * env(n, 0.001, 0.015) * 0.5, k * 0.04)
    for k in range(5):
        poe(x, B.explosao(rng, v)[: n_de(0.35)] * 0.35, 0.35 + k * 0.05)
    return x


def facas(rng, v):
    x = _z(0.6)
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 2500, 6000, 0.5, g=0.35), k * 0.05)
        poe(x, cravar(rng, v)[: n_de(0.2)] * 0.6, 0.12 + k * 0.05)
    return x


def foguete(rng, v):
    x = _z(1.4)
    n = n_de(0.5)
    poe(x, passa(ruido(rng, n), 200, 3000, 2) * sobe_e_some(n, 0.6, 1.2) * 0.7, 0)
    poe(x, B.explosao(rng, v), 0.45, 1.1)
    poe(x, baque(n_de(0.8), 50, 25, 0.35, 0.3) * 0.8, 0.45)
    return x


def bomba(rng, v):
    x = _z(1.2)
    n = n_de(0.4)
    poe(x, graos(rng, n, 40, 0, 0.38, 3000, 9000, 0.002) * 0.4, 0)
    poe(x, B.explosao(rng, v), 0.38, 1.0)
    poe(x, _tom(nota(60), nota(55), 0.3, 0.2, 0.1), 0.45)
    return x


def canhao(rng, v):
    x = _z(1.3)
    poe(x, baque(n_de(0.5), 70, 35, 0.15, 0.6) * 0.8, 0)
    poe(x, _whoosh(rng, 0.3, 1200, 300, 0.4, g=0.5), 0.05)
    poe(x, B.explosao(rng, v), 0.32, 1.1)
    return x


def gas(rng, v):
    n = n_de(1.1)
    x = passa(rosa(rng, n), 600, 6000, 2) * env(n, 0.05, 0.5) * 0.5
    t = np.arange(n) / SR
    x *= 0.7 + 0.3 * np.sin(2 * math.pi * 4 * t)
    x += graos(rng, n, 12, 0.1, 0.9, 300, 900, 0.02) * 0.3
    return reverb(x, 0.4, 0.2)


def laser(rng, v):
    n = n_de(0.5)
    x = seno(varre(2400, 1800, n, 0.7), n) * env(n, 0.003, 0.3) * 0.25
    x += seno(varre(2410, 1810, n, 0.7), n) * env(n, 0.003, 0.3) * 0.2
    x += passa(ruido(rng, n), 4000, 10000, 2) * env(n, 0.002, 0.05) * 0.3
    t = np.arange(n_de(0.4)) / SR
    chiado = passa(ruido(rng, len(t)), 1500, 6000, 2) * np.exp(-t / 0.2) * 0.25
    poe(x, chiado, 0.1)
    return x


# ================================================================== energia
def hadouken(rng, v):
    x = _z(0.9)
    poe(x, _tom(nota(48), nota(60), 0.15, 0.1, 0.3), 0)
    poe(x, B.disparo(rng, v), 0.05, 0.8)
    poe(x, B.impacto_energia(rng, v), 0.35, 0.9)
    return x



def canhao_de_energia(rng, v):
    x = _z(1.3)
    n = n_de(1.0)
    poe(x, satura(seno(varre(60, 90, n, 0.5), n), 4) * env(n, 0.01, 0.6, segura=0.4) * 0.5 + B.feixe(rng, v)[:n] * 0.6, 0)
    poe(x, B.explosao(rng, v)[: n_de(0.5)] * 0.7, 0.8)
    return x



def buraco_negro(rng, v):
    n = n_de(1.4)
    x = assobio(rng, n, 4000, 80, 0.6, 0.6) * env(n, 0.05, 0.7) * 0.7
    x += satura(seno(varre(70, 30, n, 0.8), n), 3) * env(n, 0.05, 0.8) * 0.5
    x += _corta(_tom(nota(40), nota(28), 1.4, 0.8, 0.2), 1.4)
    return reverb(x, 0.8, 0.3, 2000)


def gravidade(rng, v):
    n = n_de(1.1)
    t = np.arange(n) / SR
    x = satura(seno(varre(80, 40, n, 0.7), n), 3) * env(n, 0.03, 0.6) * (0.7 + 0.3 * np.sin(2 * math.pi * 6 * t)) * 0.6
    poe(x, baque(n_de(0.6), 55, 28, 0.3, 0.3) * 1.0, 0.15)
    return reverb(x, 0.6, 0.2, 2500)


def cosmico(rng, v):
    n = n_de(1.3)
    x = np.zeros(n)
    for k, m in enumerate((60, 67, 72, 79)):
        poe(x, modal(n_de(1.0), nota(m), rng=rng, **SINO) * env(n_de(1.0), 0.05, 0.6) * 0.12, k * 0.06)
    x += passa(rosa(rng, n), 2000, 9000, 2) * env(n, 0.1, 0.6) * 0.15
    poe(x, B.impacto_energia(rng, v)[: n_de(0.4)] * 0.6, 0.2)
    return reverb(x, 0.85, 0.4, 7000)


def chuva_de_meteoros(rng, v):
    x = _z(1.3)
    for k in range(8):
        poe(x, _whoosh(rng, 0.14, 4000, 800, 0.8, g=0.35), k * 0.06)
        poe(x, B.explosao(rng, v)[: n_de(0.3)] * 0.3, k * 0.06 + 0.13)
    return x


def supernova(rng, v):
    x = _z(1.6)
    n = n_de(0.5)
    poe(x, assobio(rng, n, 200, 6000, 1.5, 0.5) * sobe_e_some(n, 0.95, 1.2) * 0.6, 0)
    poe(x, B.explosao(rng, v), 0.45, 1.2)
    poe(x, modal(n_de(1.0), nota(84), rng=rng, **SINO) * env(n_de(1.0), 0.01, 0.6) * 0.2, 0.45)
    return reverb(x, 0.8, 0.3)


def pulso_emp(rng, v):
    n = n_de(0.8)
    t = np.arange(n) / SR
    x = np.sign(np.sin(2 * math.pi * varre(800, 60, n, 0.6).cumsum() / SR)) * env(n, 0.001, 0.25) * 0.25
    x += graos(rng, n, 30, 0.0, 0.5, 2000, 8000, 0.002) * 0.5
    x *= (np.sin(2 * math.pi * 40 * t) > -0.3)
    return reverb(x, 0.3, 0.2)


def pilar(rng, v):
    n = n_de(1.3)
    x = assobio(rng, n, 150, 5000, 0.7, 0.5) * env(n, 0.05, 0.6) * 0.8
    x += satura(seno(varre(70, 120, n, 0.6), n), 3) * env(n, 0.03, 0.6) * 0.35
    poe(x, baque(n_de(0.5), 70, 35, 0.2, 0.3) * 0.8, 0)
    return reverb(x, 0.7, 0.3)


def transformacao_v2(rng, v):
    x = _z(1.8)
    n = n_de(1.2)
    t = np.arange(n) / SR
    rugido = satura(passa(rosa(rng, n), 100, 1200, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 7 * t)), 2) * env(n, 0.1, 0.5, segura=0.4) * 0.7
    poe(x, rugido + B.carga_grande(rng, v)[:n] * 0.5, 0)
    poe(x, B.explosao(rng, v)[: n_de(0.6)] * 0.9, 1.0)
    return x


def atracao(rng, v):
    n = n_de(1.0)
    x = assobio(rng, n, 6000, 300, 0.5, 0.5) * env(n, 0.02, 0.6) * 0.8
    x += _corta(_tom(nota(76), nota(52), 1.0, 0.6, 0.18, 0.5), 1.0)
    poe(x, baque(n_de(0.3), 140, 60, 0.05, 0.3) * 0.5, 0.75)
    return reverb(x, 0.5, 0.25)


def repulsao(rng, v):
    x = _z(1.1)
    poe(x, _tom(nota(84), nota(96), 0.12, 0.08, 0.25), 0)
    poe(x, B.explosao(rng, v), 0.12, 1.0)
    poe(x, assobio(rng, n_de(0.8), 300, 6000, 0.5, 0.5) * env(n_de(0.8), 0.005, 0.3) * 0.6, 0.12)
    return x


def dominio(rng, v):
    n = n_de(1.6)
    x = np.zeros(n)
    for k, m in enumerate((48, 55, 60, 63, 67)):
        poe(x, seno(nota(m), n_de(1.4)) * env(n_de(1.4), 0.2, 0.9) * 0.08, k * 0.04)
    x += assobio(rng, n, 8000, 200, 0.6, 0.5) * env(n, 0.05, 0.6) * 0.4
    poe(x, baque(n_de(0.4), 60, 30, 0.2, 0.2) * 0.8, 0)
    return reverb(x, 0.9, 0.45, 6000)


def plasma(rng, v):
    n = n_de(0.9)
    t = np.arange(n) / SR
    x = satura(seno(180 + 40 * np.sin(2 * math.pi * 9 * t), n), 5) * env(n, 0.01, 0.4, segura=0.3) * 0.3
    x += graos(rng, n, 40, 0, 0.7, 2000, 9000, 0.002) * 0.5
    return reverb(x, 0.35, 0.2)


def desintegrar(rng, v):
    n = n_de(1.3)
    x = graos(rng, n, 140, 0.05, 1.0, 3000, 11000, 0.003) * 0.6 * np.linspace(1, 0.2, n)
    x += assobio(rng, n, 1500, 9000, 0.6, 0.4) * env(n, 0.05, 0.6) * 0.4
    poe(x, _tom(nota(72), nota(60), 0.4, 0.3, 0.15), 0)
    return reverb(x, 0.6, 0.3, 8000)


# ================================================================== elementos
def labareda(rng, v):
    x = _z(1.2)
    poe(x, assobio(rng, n_de(0.4), 200, 2000, 0.6, 0.6) * env(n_de(0.4), 0.005, 0.3) * 0.7, 0)
    poe(x, B.fogo(rng, v), 0.02, 1.1)
    poe(x, baque(n_de(0.4), 80, 40, 0.15, 0.3) * 0.6, 0)
    return x


def sopro_de_fogo(rng, v):
    n = n_de(1.1)
    x = passa(rosa(rng, n), 150, 3500, 2) * env(n, 0.05, 0.5, segura=0.4) * 0.8
    x += graos(rng, n, 50, 0.05, 0.9, 1500, 6000, 0.003) * 0.3
    return reverb(x, 0.4, 0.2, 4000)


def fenix(rng, v):
    x = _z(1.4)
    n = n_de(0.7)
    t = np.arange(n) / SR
    grito = seno(varre(nota(84), nota(90), n, 0.4) * (1 + 0.02 * np.sin(2 * math.pi * 9 * t)), n) * env(n, 0.05, 0.4) * 0.25
    grito += seno(varre(nota(91), nota(97), n, 0.4), n) * env(n, 0.05, 0.3) * 0.1
    poe(x, grito, 0)
    poe(x, B.fogo(rng, v), 0.2, 0.9)
    poe(x, _whoosh(rng, 0.4, 300, 2500, 0.6, g=0.6), 0.1)
    return reverb(x, 0.6, 0.3)


def chama_negra(rng, v):
    n = n_de(1.3)
    x = passa(B.fogo(rng, v), None, 1200) * 1.2
    x = _corta(x, 1.3)
    x += passa(rosa(rng, n), 50, 300, 2) * env(n, 0.1, 0.7) * 0.5 + _corta(_tom(nota(36), nota(33), 1.3, 0.8, 0.2), 1.3)
    return reverb(x, 0.6, 0.3, 1800)


def dragao(rng, v):
    x = _z(1.6)
    n = n_de(0.9)
    t = np.arange(n) / SR
    rugido = satura(passa(rosa(rng, n), 120, 1500, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 13 * t)), 2.5) * sobe_e_some(n, 0.5, 1.4) * 0.8
    poe(x, rugido, 0)
    poe(x, B.explosao(rng, v)[: n_de(0.7)] * 0.8, 0.6)
    return reverb(x, 0.6, 0.25)


def nevasca(rng, v):
    n = n_de(1.3)
    t = np.arange(n) / SR
    x = assobio(rng, n, 2500, 1200, 1.0, 0.6) * (0.6 + 0.4 * np.sin(2 * math.pi * 2.5 * t)) * env(n, 0.1, 0.6, segura=0.3) * 0.8
    x += graos(rng, n, 50, 0.1, 1.1, 5000, 11000, 0.002) * 0.3
    poe(x, B.gelo(rng, v)[: n_de(0.5)] * 0.4, 0.3)
    return reverb(x, 0.6, 0.3, 7000)


def bloco_de_gelo(rng, v):
    x = _z(1.1)
    for k in range(4):
        poe(x, modal(n_de(0.4), rng.uniform(1500, 2500), rng=rng, **VIDRO) * env(n_de(0.4), 0.001, 0.2) * 0.25, k * 0.06)
    poe(x, baque(n_de(0.4), 160, 80, 0.08, 0.3) * 0.5, 0.25)
    poe(x, graos(rng, n_de(0.6), 15, 0.3, 0.5, 2500, 8000, 0.004) * 0.4, 0.2)
    return reverb(x, 0.4, 0.2, 7000)


def espinho_de_gelo(rng, v):
    x = _z(1.0)
    for k in range(5):
        poe(x, B.gelo(rng, v)[: n_de(0.3)] * 0.35 + estalo(rng, n_de(0.3), 1500, 7000, 0.006) * 0.4, k * 0.05)
    poe(x, baque(n_de(0.5), 120, 55, 0.1, 0.3) * 0.6, 0)
    return x


def tempestade(rng, v):
    x = _z(1.6)
    n = n_de(1.5)
    poe(x, passa(rosa(rng, n), 40, 200, 2) * env(n, 0.2, 0.8) * 0.6, 0)
    for k, a in enumerate((0.15, 0.38, 0.6)):
        poe(x, B.raio(rng, v)[: n_de(0.6)] * (0.7 + 0.15 * k), a * 1.4)
    return reverb(x, 0.8, 0.3, 4000)


def raio_em_cadeia(rng, v):
    x = _z(1.1)
    for k in range(3):
        poe(x, B.raio(rng, v)[: n_de(0.35)] * 0.6, k * 0.13)
        poe(x, _tom(nota(84 + 3 * k), nota(80 + 3 * k), 0.15, 0.08, 0.12), k * 0.13 + 0.05)
    return x



def tsunami(rng, v):
    n = n_de(1.6)
    x = passa(rosa(rng, n), 60, 2500, 2) * sobe_e_some(n, 0.55, 1.4) * 1.0
    poe(x, B.agua(rng, v) * 0.9, 0.7)
    poe(x, baque(n_de(0.6), 60, 30, 0.3, 0.2) * 0.7, 0.8)
    return reverb(x, 0.7, 0.3, 3500)


def jato_dagua(rng, v):
    n = n_de(0.9)
    t = np.arange(n) / SR
    x = passa(ruido(rng, n), 800, 6000, 2) * env(n, 0.02, 0.4, segura=0.4) * 0.5 * (0.8 + 0.2 * np.sin(2 * math.pi * 17 * t))
    x += graos(rng, n, 30, 0.1, 0.8, 600, 2000, 0.01) * 0.3
    return x


def areia(rng, v):
    n = n_de(1.3)
    x = passa(ruido(rng, n), 1500, 9000, 2) * sobe_e_some(n, 0.6, 1.3) * 0.6
    x += graos(rng, n, 120, 0.0, 1.2, 3000, 10000, 0.002) * 0.4
    poe(x, baque(n_de(0.4), 90, 45, 0.15, 0.2) * 0.6, 0.85)
    return reverb(x, 0.4, 0.2)


def espinhos_de_terra(rng, v):
    x = _z(1.1)
    for k in range(6):
        poe(x, B.terra(rng, v)[: n_de(0.35)] * 0.5, k * 0.05)
    poe(x, B.terremoto(rng, v)[: n_de(0.9)] * 0.4, 0)
    return x


def metal(rng, v):
    x = _z(1.1)
    for k in range(4):
        poe(x, modal(n_de(0.5), rng.uniform(200, 400), rng=rng, **METAL) * env(n_de(0.5), 0.001, 0.25) * 0.4 + estalo(rng, n_de(0.5), 800, 4000, 0.01) * 0.3, k * 0.08)
    poe(x, _tom(150, 90, 0.5, 0.2, 0.3), 0.3)
    return reverb(x, 0.5, 0.25)


def tornado(rng, v):
    n = n_de(1.4)
    t = np.arange(n) / SR
    x = assobio(rng, n, 400, 1800, 1.0, 0.5) * (0.6 + 0.4 * np.sin(2 * math.pi * 5 * t)) * env(n, 0.1, 0.6, segura=0.3) * 1.0
    x += graos(rng, n, 30, 0.1, 1.2, 500, 3000, 0.008) * 0.3
    return reverb(x, 0.5, 0.25)


def rajada_de_ar(rng, v):
    x = _z(0.9)
    for k in range(3):
        poe(x, _whoosh(rng, 0.35, 300, 2500, 0.5, g=0.6), k * 0.08)
    poe(x, baque(n_de(0.3), 120, 60, 0.06, 0.2) * 0.4, 0.3)
    return reverb(x, 0.4, 0.2)


def vinhas(rng, v):
    n = n_de(1.2)
    x = np.zeros(n)
    for k in range(18):
        m = n_de(0.06)
        poe(x, passa(ruido(rng, m), 600, 3000, 2) * env(m, 0.005, 0.03) * 0.5, rng.uniform(0, 0.8))
    x += passa(rosa(rng, n), 150, 800, 2) * sobe_e_some(n, 0.5, 1.4) * 0.4
    poe(x, B.prisao(rng, v)[: n_de(0.5)] * 0.4, 0.6)
    return reverb(x, 0.35, 0.2)


def petalas(rng, v):
    n = n_de(1.2)
    x = assobio(rng, n, 2000, 4000, 1.0, 0.4) * sobe_e_some(n, 0.4, 1.4) * 0.4
    for k, m in enumerate((79, 83, 86, 91)):
        poe(x, _brilho(rng, 0.5, nota(m), 0.12, SINO), 0.05 + k * 0.08)
    return reverb(x, 0.6, 0.35, 8000)


def enxame(rng, v):
    n = n_de(1.3)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for k in range(6):
        f = rng.uniform(180, 320)
        x += np.sin(2 * math.pi * f * t + 3 * np.sin(2 * math.pi * rng.uniform(15, 30) * t)) * 0.08
    x = satura(x, 2) * env(n, 0.1, 0.6, segura=0.4)
    return passa(x, 120, 4000)


def acido(rng, v):
    n = n_de(1.1)
    x = passa(ruido(rng, n), 1200, 7000, 2) * env(n, 0.02, 0.5) * 0.4
    for k in range(14):
        m = n_de(0.05)
        f = rng.uniform(400, 1000)
        poe(x, seno(varre(f, f * 1.8, m), m) * env(m, 0.002, 0.02) * 0.25, rng.uniform(0, 0.9))
    poe(x, passa(ruido(rng, n_de(0.2)), 300, 2000, 2) * env(n_de(0.2), 0.001, 0.05) * 0.6, 0)
    return reverb(x, 0.3, 0.2)


def sangue(rng, v):
    x = _z(0.9)
    n = n_de(0.3)
    poe(x, satura(passa(ruido(rng, n), 200, 2000, 2) * env(n, 0.001, 0.05), 2.5) * 0.8 + baque(n, 110, 55, 0.06, 0.3) * 0.5, 0)
    for k in range(6):
        m = n_de(0.08)
        poe(x, passa(ruido(rng, m), 300, 1500, 2) * env(m, 0.002, 0.02) * 0.4, 0.15 + rng.uniform(0, 0.5))
    return reverb(x, 0.3, 0.15)


def radiacao(rng, v):
    n = n_de(1.3)
    x = np.zeros(n)
    for k in range(60):
        m = n_de(0.004)
        poe(x, ruido(rng, m) * 0.5, rng.uniform(0, 1.25))
    t = np.arange(n) / SR
    x += seno(np.full(n, 60.0), n) * 0.0 + satura(seno(np.full(n, 120.0), n), 3) * env(n, 0.1, 0.6, segura=0.4) * 0.15 * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * t))
    return reverb(x, 0.3, 0.2)


def lua(rng, v):
    n = n_de(1.4)
    x = np.zeros(n)
    for k, m in enumerate((69, 76, 81)):
        poe(x, modal(n_de(1.2), nota(m), rng=rng, **CRISTAL) * env(n_de(1.2), 0.08, 0.7) * 0.15, k * 0.1)
    x += assobio(rng, n, 3000, 6000, 1.0, 0.3) * env(n, 0.2, 0.6) * 0.15
    return reverb(x, 0.85, 0.4, 8000)


def raio_divino(rng, v):
    x = _z(1.3)
    poe(x, _tom(nota(96), nota(96), 0.15, 0.1, 0.12), 0)
    n = n_de(1.0)
    coro = sum(seno(nota(m) * (1 + 0.003 * np.sin(np.arange(n) / SR * 2 * math.pi * 5)), n) for m in (72, 76, 79, 84)) * env(n, 0.03, 0.6) * 0.07
    poe(x, coro, 0.12)
    poe(x, B.luz(rng, v)[: n_de(0.8)] * 0.7, 0.12)
    poe(x, baque(n_de(0.4), 90, 45, 0.15, 0.3) * 0.6, 0.15)
    return reverb(x, 0.8, 0.35)


def rugido(rng, v):
    n = n_de(1.1)
    t = np.arange(n) / SR
    x = satura(passa(rosa(rng, n), 80, 1400, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 23 * t)), 3) * sobe_e_some(n, 0.25, 1.3) * 1.0
    x += seno(varre(110, 70, n, 0.6), n) * env(n, 0.05, 0.6) * 0.3
    return reverb(x, 0.6, 0.25)


# ================================================================== magia
def olho(rng, v):
    n = n_de(1.2)
    x = _corta(_tom(nota(48), nota(55), 0.4, 0.3, 0.3), 1.2)
    poe(x, B.psiquico(rng, v)[: n_de(0.9)] * 0.6, 0.2)
    poe(x, _brilho(rng, 0.4, nota(88), 0.12), 0.25)
    return reverb(x, 0.6, 0.3)


def hipnose(rng, v):
    n = n_de(1.3)
    t = np.arange(n) / SR
    x = (seno(np.full(n, nota(69)), n) + seno(np.full(n, nota(69) * 1.012), n)) * env(n, 0.1, 0.6, segura=0.4) * 0.12
    x *= 0.6 + 0.4 * np.sin(2 * math.pi * 6 * t)
    x += seno(varre(nota(81), nota(69), n, 0.5), n) * env(n, 0.1, 0.6) * 0.08
    return reverb(x, 0.7, 0.35)


def relogio(rng, v):
    x = _z(1.3)
    for k in range(10):
        m = n_de(0.05)
        poe(x, modal(m, 3000 if k % 2 else 2400, rng=rng, razoes=[1, 2.4], quedas=[0.01, 0.006]) * 0.4, 0.06 + k * 0.05 * (1 - k * 0.04))
    poe(x, modal(n_de(1.0), nota(72), rng=rng, **SINO) * env(n_de(1.0), 0.001, 0.6) * 0.3, 0.6)
    poe(x, assobio(rng, n_de(0.5), 3000, 300, 0.6, 0.5) * env(n_de(0.5), 0.01, 0.3) * 0.4, 0.62)
    return reverb(x, 0.6, 0.3)


def runas(rng, v):
    x = _z(1.3)
    for k, m in enumerate((62, 65, 69, 72, 74, 77, 81, 84)):
        poe(x, _brilho(rng, 0.4, nota(m), 0.1, SINO), 0.1 + k * 0.06)
    poe(x, passa(rosa(rng, n_de(1.0)), 100, 600, 2) * env(n_de(1.0), 0.2, 0.5) * 0.3, 0)
    return reverb(x, 0.7, 0.35)


def sarcofago(rng, v):
    x = _z(1.3)
    for k in range(3):
        poe(x, baque(n_de(0.3), 90, 45, 0.1, 0.5) * 0.6 + estalo(rng, n_de(0.3), 600, 3000, 0.01) * 0.3, k * 0.1)
    poe(x, B.sombra(rng, v)[: n_de(0.6)] * 0.5, 0.4)
    poe(x, B.explosao(rng, v)[: n_de(0.5)] * 0.5, 0.65)
    return x


def encanto(rng, v):
    x = _z(1.2)
    for k, m in enumerate((84, 88, 91, 96, 91, 88, 96, 100)):
        poe(x, _brilho(rng, 0.35, nota(m), 0.1, SINO), 0.05 + k * 0.06)
    poe(x, _brilho(rng, 0.6, nota(96), 0.18, CRISTAL), 0.55)
    return reverb(x, 0.7, 0.35, 9000)


def caveira(rng, v):
    n = n_de(1.3)
    x = passa(rosa(rng, n), 100, 1200, 2) * sobe_e_some(n, 0.35, 1.3) * 0.6
    x += _corta(_tom(nota(45), nota(38), 1.0, 0.6, 0.2), 1.3)
    t = np.arange(n) / SR
    riso = np.zeros(n)
    for k in range(5):
        m = n_de(0.08)
        poe(riso, seno(varre(nota(57), nota(52), m), m) * env(m, 0.005, 0.04) * 0.15, 0.3 + k * 0.1)
    return reverb(x + riso, 0.7, 0.35, 2500)


def clones(rng, v):
    x = _z(1.1)
    for k in range(5):
        m = n_de(0.15)
        poe(x, passa(ruido(rng, m), 1500, 7000, 2) * sobe_e_some(m, 0.3, 2) * 0.4 + _tom(nota(76 + k * 2), nota(80 + k * 2), 0.15, 0.06, 0.08), k * 0.05)
    for k in range(5):
        poe(x, passa(rosa(rng, n_de(0.2)), 400, 3000, 2) * env(n_de(0.2), 0.005, 0.06) * 0.3, 0.55 + k * 0.08)
    return reverb(x, 0.4, 0.2)


def teleporte(rng, v):
    x = _z(1.0)
    poe(x, _tom(nota(84), nota(60), 0.25, 0.2, 0.25, 0.4), 0)
    poe(x, assobio(rng, n_de(0.25), 6000, 600, 0.6, 0.4) * env(n_de(0.25), 0.005, 0.15) * 0.5, 0)
    poe(x, _tom(nota(60), nota(84), 0.2, 0.15, 0.25, 0.6), 0.35)
    poe(x, estalo(rng, n_de(0.1), 1500, 8000, 0.006) * 0.6, 0.35)
    return reverb(x, 0.5, 0.25)


def fenda(rng, v):
    n = n_de(1.3)
    x = np.zeros(n)
    poe(x, passa(ruido(rng, n_de(0.2)), 1000, 9000, 2) * env(n_de(0.2), 0.001, 0.08) * 0.7, 0)
    x += B.portal(rng, v)[:n] * 0.6 if len(B.portal(rng, v)) >= n else _corta(B.portal(rng, v), 1.3) * 0.6
    x += passa(rosa(rng, n), 40, 250, 2) * env(n, 0.1, 0.6) * 0.4
    return reverb(x, 0.7, 0.3, 3000)


def sorte(rng, v):
    x = _z(1.1)
    for k in range(7):
        m = n_de(0.06)
        poe(x, baque(m, 600, 300, 0.01, 0.6) * 0.3 + estalo(rng, m, 1500, 5000, 0.005) * 0.3, k * 0.07 * (1 - k * 0.05))
    for k, mm in enumerate((72, 76, 79, 84)):
        poe(x, _brilho(rng, 0.3, nota(mm), 0.12, SINO), 0.55 + k * 0.06)
    return reverb(x, 0.4, 0.2)


def confete(rng, v):
    x = _z(1.1)
    n = n_de(0.15)
    poe(x, baque(n, 300, 150, 0.03, 0.8) * 0.5 + passa(ruido(rng, n), 1000, 6000, 2) * env(n, 0.001, 0.03) * 0.6, 0)
    poe(x, graos(rng, n_de(0.9), 60, 0.05, 0.8, 2500, 9000, 0.004) * 0.35, 0)
    for k, mm in enumerate((79, 83, 86, 91)):
        poe(x, _brilho(rng, 0.25, nota(mm), 0.08, SINO), 0.08 + k * 0.05)
    return reverb(x, 0.4, 0.2)


def confusao(rng, v):
    n = n_de(1.2)
    t = np.arange(n) / SR
    x = np.sin(2 * math.pi * np.cumsum(500 + 250 * np.sin(2 * math.pi * 3 * t)) / SR) * env(n, 0.05, 0.6) * 0.15
    for k in range(4):
        poe(x, _brilho(rng, 0.25, nota(84 + (k % 2) * 5), 0.08, SINO), 0.1 + k * 0.18)
    return reverb(x, 0.5, 0.25)


def clarao_solar(rng, v):
    n = n_de(1.0)
    x = assobio(rng, n, 2000, 9000, 0.3, 0.5) * env(n, 0.001, 0.4) * 0.6
    x += modal(n, nota(96), rng=rng, **CRISTAL) * env(n, 0.001, 0.5) * 0.2
    x += estalo(rng, n, 2000, 10000, 0.01) * 0.5
    return reverb(x, 0.6, 0.35, 10000)


def pentagrama(rng, v):
    x = _z(1.4)
    n = n_de(0.6)
    poe(x, passa(ruido(rng, n), 800, 4000, 2) * env(n, 0.01, 0.3) * 0.3, 0)
    for k, m in enumerate((38, 44, 50)):
        poe(x, satura(seno(np.full(n_de(1.0), nota(m)), n_de(1.0)), 2) * env(n_de(1.0), 0.1, 0.5) * 0.12, 0.1 + k * 0.1)
    poe(x, B.fogo(rng, v)[: n_de(0.8)] * 0.6, 0.45)
    return reverb(x, 0.7, 0.3, 3000)


def invocacao(rng, v):
    x = _z(1.5)
    poe(x, B.selo(rng, v)[: n_de(0.7)] * 0.6, 0)
    n = n_de(0.8)
    poe(x, assobio(rng, n, 150, 3000, 0.6, 0.5) * sobe_e_some(n, 0.7, 1.4) * 0.7, 0.3)
    poe(x, baque(n_de(0.5), 80, 40, 0.2, 0.3) * 0.7, 0.85)
    return x


def lua_vermelha(rng, v):
    n = n_de(1.6)
    x = np.zeros(n)
    for k, m in enumerate((45, 48, 52, 57)):
        poe(x, seno(np.full(n_de(1.4), nota(m)), n_de(1.4)) * env(n_de(1.4), 0.3, 0.8) * 0.09, k * 0.05)
    x += passa(rosa(rng, n), 60, 400, 2) * env(n, 0.2, 0.8) * 0.4
    poe(x, B.maldicao(rng, v)[: n_de(0.8)] * 0.5, 0.3)
    return reverb(x, 0.9, 0.4, 2500)


def susanoo(rng, v):
    x = _z(1.6)
    n = n_de(1.2)
    t = np.arange(n) / SR
    corpo = satura(passa(rosa(rng, n), 60, 900, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 4 * t)), 2) * sobe_e_some(n, 0.6, 1.4) * 0.7
    poe(x, corpo, 0)
    poe(x, B.fogo(rng, v)[: n_de(0.9)] * 0.4, 0.1)
    poe(x, baque(n_de(0.6), 60, 30, 0.3, 0.3), 0.6)
    return reverb(x, 0.7, 0.3)


def asa_negra(rng, v):
    x = _z(1.3)
    for k in range(3):
        poe(x, passa(rosa(rng, n_de(0.3)), 200, 2000, 2) * sobe_e_some(n_de(0.3), 0.4, 1.5) * 0.6, k * 0.12)
    poe(x, B.corte(rng, v) * 0.6, 0.3)
    poe(x, _corta(_tom(nota(50), nota(43), 0.9, 0.5, 0.15), 0.9), 0.3)
    return reverb(x, 0.7, 0.35, 3000)


# ================================================================== apoio
def cura_em_area(rng, v):
    x = _z(1.5)
    for k, m in enumerate((72, 76, 79, 84, 88)):
        poe(x, modal(n_de(1.0), nota(m), rng=rng, **SINO) * env(n_de(1.0), 0.01, 0.6) * 0.12, k * 0.08)
    poe(x, assobio(rng, n_de(1.0), 1500, 5000, 0.8, 0.4) * env(n_de(1.0), 0.1, 0.5) * 0.25, 0)
    return reverb(x, 0.8, 0.4, 9000)


def regeneracao(rng, v):
    n = n_de(1.4)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for k in range(10):
        poe(x, _brilho(rng, 0.3, nota(rng.choice([76, 79, 81, 84, 88])), 0.07, SINO), k * 0.12)
    x += seno(np.full(n, nota(64)), n) * env(n, 0.2, 0.8, segura=0.3) * 0.06 * (0.7 + 0.3 * np.sin(2 * math.pi * 2 * t))
    return reverb(x, 0.7, 0.35, 8000)


def grito_de_guerra(rng, v):
    x = _z(1.3)
    n = n_de(0.8)
    t = np.arange(n) / SR
    voz = satura(passa(rosa(rng, n), 200, 2500, 2) * (0.8 + 0.2 * np.sin(2 * math.pi * 30 * t)), 2) * sobe_e_some(n, 0.25, 1.2) * 0.6
    poe(x, voz, 0)
    for k, m in enumerate((60, 64, 67, 72)):
        poe(x, satura(seno(np.full(n_de(0.5), nota(m)), n_de(0.5)), 1.5) * env(n_de(0.5), 0.01, 0.3) * 0.1, 0.25 + k * 0.07)
    return reverb(x, 0.6, 0.3)


def velocidade(rng, v):
    x = _z(0.9)
    for k in range(4):
        poe(x, _whoosh(rng, 0.15, 1500, 6000, 0.6, g=0.4), k * 0.08)
    poe(x, _tom(nota(72), nota(84), 0.3, 0.2, 0.12), 0.1)
    return reverb(x, 0.4, 0.2)


def escudo_tech(rng, v):
    x = _z(1.1)
    for k in range(8):
        poe(x, seno(np.full(n_de(0.05), 1800 + 150 * k), n_de(0.05)) * env(n_de(0.05), 0.001, 0.02) * 0.15, k * 0.04)
    n = n_de(0.8)
    poe(x, satura(seno(np.full(n, 110.0), n), 3) * env(n, 0.05, 0.4) * 0.15 + passa(ruido(rng, n), 3000, 8000, 2) * env(n, 0.05, 0.3) * 0.1, 0.3)
    return reverb(x, 0.4, 0.2)


def barreira_magica(rng, v):
    x = _z(1.4)
    poe(x, B.escudo(rng, v)[: n_de(0.8)] * 0.6, 0)
    for k, m in enumerate((67, 74, 79)):
        poe(x, modal(n_de(1.0), nota(m), rng=rng, **CRISTAL) * env(n_de(1.0), 0.05, 0.6) * 0.12, 0.1 + k * 0.1)
    return reverb(x, 0.7, 0.35)



def armadura(rng, v):
    x = _z(1.1)
    for k in range(5):
        poe(x, modal(n_de(0.25), rng.uniform(400, 600) * (1 + k * 0.1), rng=rng, **METAL) * env(n_de(0.25), 0.001, 0.1) * 0.25 + baque(n_de(0.25), 200, 100, 0.03, 0.4) * 0.3, k * 0.07)
    poe(x, _brilho(rng, 0.5, nota(91), 0.1, CRISTAL), 0.45)
    return reverb(x, 0.4, 0.2)


def resgate(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.35, 3000, 400, 0.6, g=0.6), 0)
    poe(x, _whoosh(rng, 0.3, 400, 3000, 0.4, g=0.5), 0.35)
    for k, m in enumerate((76, 81, 84)):
        poe(x, _brilho(rng, 0.4, nota(m), 0.1, SINO), 0.4 + k * 0.06)
    return reverb(x, 0.5, 0.25)


def bencao(rng, v):
    n = n_de(1.6)
    x = np.zeros(n)
    coro = sum(seno(np.full(n_de(1.4), nota(m)) * (1 + 0.004 * np.sin(np.arange(n_de(1.4)) / SR * 2 * math.pi * (4 + k))), n_de(1.4)) for k, m in enumerate((72, 76, 79))) * env(n_de(1.4), 0.3, 0.8) * 0.07
    poe(x, coro, 0)
    for k in range(5):
        poe(x, _brilho(rng, 0.4, nota(rng.choice([88, 91, 96])), 0.06, SINO), 0.2 + k * 0.2)
    return reverb(x, 0.85, 0.4, 9000)


def lanche(rng, v):
    x = _z(1.1)
    n = n_de(0.12)
    poe(x, satura(passa(ruido(rng, n), 800, 5000, 2) * env(n, 0.001, 0.03), 2) * 0.6, 0)
    poe(x, satura(passa(ruido(rng, n), 800, 5000, 2) * env(n, 0.001, 0.03), 2) * 0.5, 0.15)
    for k, m in enumerate((72, 76, 79, 84)):
        poe(x, seno(np.full(n_de(0.15), nota(m)), n_de(0.15)) * env(n_de(0.15), 0.005, 0.08) * 0.15, 0.35 + k * 0.08)
    return reverb(x, 0.3, 0.15)


def purificacao(rng, v):
    x = _z(1.3)
    poe(x, assobio(rng, n_de(0.8), 6000, 1500, 0.8, 0.4) * sobe_e_some(n_de(0.8), 0.4, 1.4) * 0.5, 0)
    for k, m in enumerate((84, 88, 91, 96)):
        poe(x, _brilho(rng, 0.5, nota(m), 0.1, CRISTAL), 0.1 + k * 0.1)
    return reverb(x, 0.8, 0.4, 10000)


def enfraquecimento(rng, v):
    x = _z(1.2)
    for k, m in enumerate((67, 63, 60, 55)):
        poe(x, satura(seno(varre(nota(m), nota(m - 1), n_de(0.3)), n_de(0.3)), 1.5) * env(n_de(0.3), 0.01, 0.15) * 0.15, k * 0.12)
    poe(x, passa(rosa(rng, n_de(1.0)), 80, 500, 2) * env(n_de(1.0), 0.05, 0.5) * 0.3, 0)
    return reverb(x, 0.5, 0.25, 2500)


def lentidao(rng, v):
    n = n_de(1.4)
    x = np.zeros(n)
    for k in range(4):
        poe(x, modal(n_de(0.4), 1200, rng=rng, razoes=[1, 2.4], quedas=[0.05, 0.03]) * 0.25, 0.1 + k * 0.28 * (1 + k * 0.15))
    x += passa(ruido(rng, n), 2500, 7000, 2) * env(n, 0.2, 0.6, segura=0.3) * 0.08
    x += seno(varre(nota(60), nota(48), n, 0.5), n) * env(n, 0.1, 0.8) * 0.12
    return reverb(x, 0.5, 0.25)


def marca(rng, v):
    x = _z(0.9)
    poe(x, seno(varre(1500, 1500, n_de(0.25)), n_de(0.25)) * env(n_de(0.25), 0.005, 0.1) * 0.12, 0)
    poe(x, seno(varre(2000, 2000, n_de(0.1)), n_de(0.1)) * env(n_de(0.1), 0.002, 0.05) * 0.15, 0.25)
    poe(x, baque(n_de(0.25), 300, 150, 0.03, 0.8) * 0.4 + estalo(rng, n_de(0.25), 2000, 8000, 0.004) * 0.5, 0.32)
    return reverb(x, 0.3, 0.15)


def silencio(rng, v):
    x = _z(1.0)
    n = n_de(0.3)
    poe(x, seno(np.full(n, nota(76)), n) * env(n, 0.01, 0.15) * 0.15, 0)
    poe(x, passa(ruido(rng, n_de(0.08)), 2000, 9000, 2) * env(n_de(0.08), 0.001, 0.01) * 0.8, 0.28)
    poe(x, passa(rosa(rng, n_de(0.6)), 60, 300, 2) * env(n_de(0.6), 0.05, 0.3) * 0.2, 0.3)
    return x


def medo(rng, v):
    n = n_de(1.4)
    t = np.arange(n) / SR
    x = (seno(np.full(n, nota(62)), n) + seno(np.full(n, nota(63)), n)) * env(n, 0.2, 0.7, segura=0.3) * 0.08
    x += passa(rosa(rng, n), 100, 600, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 1.5 * t)) * env(n, 0.1, 0.7) * 0.3
    poe(x, _tom(nota(84), nota(72), 0.3, 0.2, 0.08), 0.6)
    return reverb(x, 0.8, 0.4, 3000)


def exposto(rng, v):
    x = _z(1.0)
    for k in range(4):
        poe(x, modal(n_de(0.3), rng.uniform(2000, 3500), rng=rng, **VIDRO) * env(n_de(0.3), 0.001, 0.12) * 0.2, 0.1 + k * 0.03)
    poe(x, estalo(rng, n_de(0.2), 1500, 9000, 0.02) * 0.6, 0.1)
    poe(x, graos(rng, n_de(0.6), 20, 0.0, 0.5, 2000, 8000, 0.004) * 0.35, 0.3)
    return reverb(x, 0.4, 0.2)


def estrela_invencivel(rng, v):
    x = _z(1.4)
    escala = (72, 76, 79, 84, 79, 84, 88, 91)
    for k, m in enumerate(escala):
        poe(x, satura(seno(np.full(n_de(0.12), nota(m)), n_de(0.12)), 1.5) * env(n_de(0.12), 0.003, 0.06) * 0.14, k * 0.09)
    poe(x, graos(rng, n_de(1.2), 40, 0.0, 1.0, 4000, 10000, 0.003) * 0.3, 0)
    return reverb(x, 0.4, 0.2)



def _tilim(rng, seg=0.06, lo=2200, hi=7000):
    """Um elo batendo no outro: poucos parciais altos e inarmônicos, bem curtos."""
    n = n_de(seg)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for _ in range(5):
        x += np.sin(2 * math.pi * rng.uniform(lo, hi) * t + rng.uniform(0, 6)) * np.exp(-t / rng.uniform(0.008, 0.025))
    return x / 5 ** 0.5 + passa(ruido(rng, n), 3000, 9000, 2) * env(n, 0.0002, 0.003) * 0.6


def corrente(rng, v):
    """Corrente: o chacoalhar dos elos voando, o "zip" passando, e o aperto em volta do alvo."""
    x = _z(1.1)
    voa = n_de(0.5)
    poe(x, assobio(rng, voa, 600, 3500, 1.2, 0.5) * sobe_e_some(voa, 0.7, 1.4) * 0.35, 0)
    for _ in range(46):                                                        # elos chacoalhando no voo
        poe(x, _tilim(rng) * rng.uniform(0.08, 0.22), rng.uniform(0.0, 0.5) ** 0.8)
    for _ in range(28):                                                        # enrolando e apertando
        poe(x, _tilim(rng, 0.08, 1500, 5000) * rng.uniform(0.15, 0.32), 0.5 + rng.uniform(0, 0.16))
    poe(x, B._placa_de_metal(rng, n_de(0.3), 300, 4000, 30, 0.06) * 0.35 + B._baque_seco(rng, n_de(0.3), 110, 0.05) * 0.5, 0.62)
    return reverb(x, 0.3, 0.14)


# ================================================================== golpes icônicos (sons de verdade)
def _faiscas(rng, n, taxa0, taxa1, lo=1500, hi=11000, forca=1.0):
    """Estalos de arco elétrico: impulsos em tempos aleatórios, com força de cauda longa
    (a maioria fraca, de vez em quando um estalo bem forte), como faísca de verdade."""
    x = np.zeros(n)
    dur = n / SR
    t = 0.0
    while True:
        taxa = taxa0 + (taxa1 - taxa0) * (t / dur)
        t += rng.exponential(1 / max(taxa, 1.0))
        if t >= dur:
            break
        i = int(t * SR)
        m = min(n - i, max(8, int(rng.uniform(0.0002, 0.0025) * SR)))
        a = min(1.0, 0.05 + rng.pareto(2.2) * 0.25) * rng.choice((-1.0, 1.0)) * forca
        x[i:i + m] += a * rng.standard_normal(m) * np.exp(-np.arange(m) / (m * 0.3))
    return passa(x, lo, hi, 2)


def _zumbido_de_arco(rng, n, f=118.0):
    """O zumbido do arco: dente-de-serra áspero que acende e apaga (cintila) o tempo todo."""
    t = np.arange(n) / SR
    deriva = passa(ruido(rng, n), None, 12, 1)
    deriva /= np.abs(deriva).max() + 1e-9
    fase = 2 * math.pi * np.cumsum(f * (1 + 0.04 * deriva)) / SR
    serra = sum(np.sin(k * fase) / k for k in range(1, 18))
    cint = passa(ruido(rng, n), None, 40, 2)
    cint = np.clip(cint / (np.abs(cint).max() + 1e-9) * 1.8 + 0.35, 0, 1)
    return passa(satura(serra * cint * 1.4, 3.5), 150, 7000, 2) * (0.8 + 0.2 * np.sin(2 * math.pi * 7 * t))


def _piados(rng, n, quantos, inicio=0.0, fim=1.0, lo=2600, hi=5200, g=0.1):
    """O "canto de mil pássaros": guinchos agudos e curtos, com vibrato rápido e FM áspera."""
    x = np.zeros(n)
    for _ in range(quantos):
        f = rng.uniform(lo, hi)
        m = n_de(rng.uniform(0.02, 0.06))
        tt = np.arange(m) / SR
        freq = f * (1 + 0.25 * tt / tt[-1]) * (1 + 0.04 * np.sin(2 * math.pi * rng.uniform(60, 120) * tt))
        s = np.sin(2 * math.pi * np.cumsum(freq) / SR)
        poe(x, satura(s, 2.5) * env(m, 0.002, m / SR * 0.5) * g * rng.uniform(0.5, 1.0), rng.uniform(inicio, fim) * n / SR)
    return x


def chidori_carga(rng, v):
    """Antes do golpe: a mão acende, as faíscas e os piados vão engrossando até a investida."""
    n = n_de(0.9)
    sobe = np.linspace(0, 1, n) ** 1.3
    x = _faiscas(rng, n, 150, 1400) * (0.35 + 0.65 * sobe) * 0.9
    x += _zumbido_de_arco(rng, n, 120) * sobe * 0.28
    x += _piados(rng, n, 70, 0.1, 1.0, g=0.08) * (0.3 + 0.7 * sobe)
    poe(x, assobio(rng, n_de(0.25), 300, 3000, 1.3, 0.5) * sobe_e_some(n_de(0.25), 0.9, 1.2) * 0.6, 0.65)   # a investida
    return reverb(x, 0.3, 0.15)


def chidori(rng, v):
    """O impacto: descarga num estouro de faíscas, o "tzzak" caindo de tom, o soco, e o chiado morrendo."""
    x = _z(0.95)
    n = n_de(0.95)
    descarga = _faiscas(rng, n_de(0.12), 4000, 2500, 800, 12000, 1.6)
    poe(x, descarga, 0)
    zap = satura(seno(varre(3200, 180, n_de(0.16), 1.6), n_de(0.16)), 4) * env(n_de(0.16), 0.0005, 0.08) * 0.45
    poe(x, passa(zap, 150, 9000, 2), 0)
    poe(x, B.soco_pesado(rng, v)[: n_de(0.35)] * 0.7, 0.005)
    resto = np.linspace(1, 0, n) ** 2
    x += _faiscas(rng, n, 900, 30, forca=0.7) * resto * 0.8
    x += _zumbido_de_arco(rng, n, 112) * env(n, 0.002, 0.25) * 0.3
    x += _piados(rng, n, 25, 0.0, 0.5, g=0.06) * resto
    return reverb(x, 0.35, 0.18)


def _giro(rng, n, rot0, rot1, centro=1500.0):
    """Vento girando numa esfera: três faixas de ar que sobem e descem defasadas
    no ritmo da rotação, então o som "roda" (o whirr do Rasengan)."""
    rot = varre(rot0, rot1, n, 0.8)
    fase = 2 * math.pi * np.cumsum(rot) / SR
    a = passa(rosa(rng, n), centro * 0.6, centro * 1.5, 2)
    b = passa(rosa(rng, n), centro * 1.6, centro * 3.6, 2) * 0.7
    c = passa(rosa(rng, n), 180, 650, 2) * 0.9
    return a * (0.5 + 0.5 * np.sin(fase)) + b * (0.5 + 0.5 * np.sin(fase + 2.1)) + c * (0.55 + 0.45 * np.sin(fase + 4.2))


def esfera_espiral_carga(rng, v):
    """Antes do golpe: a esfera se forma na mão girando cada vez mais rápido, com um assobio subindo."""
    n = n_de(0.9)
    sobe = np.linspace(0, 1, n) ** 1.2
    x = _giro(rng, n, 6, 34) * (0.25 + 0.75 * sobe) * 1.3
    giro = seno(varre(260, 820, n, 0.9), n)
    x += (giro + 0.3 * seno(varre(520, 1640, n, 0.9), n)) * sobe ** 1.5 * 0.08
    x += satura(seno(varre(70, 95, n), n), 2.5) * sobe * 0.12
    return reverb(x, 0.35, 0.15)


def esfera_espiral(rng, v):
    """O impacto: a esfera "fura" o alvo moendo (o ar raspando em espiral) e explode para fora."""
    x = _z(1.1)
    m = n_de(0.38)
    moer = _giro(rng, m, 38, 52, 1200) * 1.4
    moer += satura(passa(ruido(rng, m), 300, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 46 * np.arange(m) / SR)), 3) * 0.4
    moer *= env(m, 0.002, 0.3, segura=0.6)
    poe(x, moer, 0)
    poe(x, B.soco_pesado(rng, v)[: n_de(0.3)] * 0.6, 0)
    m = n_de(0.75)
    estouro = passa(rosa(rng, m), 40, 3500, 2) * env(m, 0.002, 0.3) * 1.1
    estouro += satura(seno(varre(85, 38, m, 1.5), m), 3) * env(m, 0.002, 0.25) * 0.6
    estouro += assobio(rng, m, 2500, 300, 1.4, 0.5) * env(m, 0.005, 0.35) * 0.5     # o ar sendo jogado para fora
    estouro += graos(rng, m, 22, 0.05, 0.6, 600, 4000, 0.006) * 0.3
    poe(x, estouro, 0.3)
    return reverb(x, 0.5, 0.22, 5000)


def kamehameha_carga(rng, v):
    """Ka-me-ha-me...: a energia junta nas mãos, um zumbido que sobe com brilho pulsando cada vez mais rápido."""
    n = n_de(0.85)
    t = np.arange(n) / SR
    sobe = np.linspace(0, 1, n) ** 1.4
    pulso = 0.6 + 0.4 * np.sin(2 * math.pi * np.cumsum(varre(5, 22, n)) / SR)
    x = satura(seno(varre(110, 230, n, 0.8), n), 2.5) * sobe * 0.25
    x += (seno(varre(440, 1100, n, 0.8), n) + 0.5 * seno(varre(660, 1650, n, 0.8), n)) * sobe ** 1.6 * pulso * 0.06
    x += assobio(rng, n, 3000, 600, 0.7, 0.5) * sobe * 0.45                    # o ar sendo puxado para as mãos
    x += _faiscas(rng, n, 30, 300, 3000, 11000, 0.5) * sobe * 0.5
    x *= 0.85 + 0.15 * np.sin(2 * math.pi * 3 * t)
    return reverb(x, 0.45, 0.2)


def kamehameha_feixe(rng, v):
    """...HA!: o feixe sai rugindo. Um estouro, depois um rugido grosso e contínuo até chegar."""
    n = n_de(1.0)
    t = np.arange(n) / SR
    corpo = env(n, 0.004, 0.5, segura=0.55)
    ronco = passa(rosa(rng, n), 40, 900, 2) * 1.4 + passa(ruido(rng, n), 900, 6000, 2) * 0.35
    ronco *= 0.85 + 0.15 * np.sin(2 * math.pi * 17 * t + 2 * np.sin(2 * math.pi * 3 * t))
    x = ronco * corpo
    x += satura(seno(np.full(n, 62.0) * (1 + 0.02 * np.sin(2 * math.pi * 5 * t)), n), 3.5) * corpo * 0.35
    x += seno(varre(1200, 900, n), n) * corpo * 0.04
    m = n_de(0.15)
    poe(x, satura(passa(ruido(rng, m), 200, 5000, 2) * env(m, 0.0005, 0.05), 3) * 0.9, 0)    # o "HA!"
    return reverb(x, 0.5, 0.2, 5000)


def kamehameha(rng, v):
    """O feixe chega: explosão de energia com o ar fervendo depois."""
    x = _z(1.3)
    poe(x, B.explosao(rng, v) * 0.95, 0)
    n = n_de(0.9)
    poe(x, _faiscas(rng, n, 400, 20, 2000, 10000, 0.5) * np.linspace(1, 0, n) * 0.5, 0.05)
    poe(x, passa(rosa(rng, n), 60, 1200, 2) * env(n, 0.002, 0.45) * 0.6, 0)
    return reverb(x, 0.6, 0.25)


def _madeira_oca(rng, n, f0):
    """Pancada em madeira oca (o malho de desenho): poucos modos da madeira, curtos, com o corpo ressoando."""
    t = np.arange(n) / SR
    x = np.zeros(n)
    for r, q, g in ((1.0, 0.11, 1.0), (2.63, 0.05, 0.55), (4.1, 0.03, 0.35), (5.9, 0.02, 0.22), (8.3, 0.012, 0.15)):
        x += np.sin(2 * math.pi * f0 * r * rng.uniform(0.985, 1.015) * t) * np.exp(-t / q) * g
    return x + passa(ruido(rng, n), 800, 5000, 2) * env(n, 0.0003, 0.008) * 0.8


def marretada_giro(rng, v):
    """Antes do golpe: a marreta sobe (apito de desenho subindo) e desce num "fuuum" pesado."""
    x = _z(0.75)
    n = n_de(0.38)
    t = np.arange(n) / SR
    apito = np.sin(2 * math.pi * np.cumsum(varre(500, 1500, n, 1.1) * (1 + 0.012 * np.sin(2 * math.pi * 7 * t))) / SR)
    poe(x, apito * env(n, 0.03, 0.3, segura=0.6) * 0.18, 0)
    poe(x, _whoosh(rng, 0.32, 1600, 220, 0.75, 1.5, 1.0), 0.4)
    return reverb(x, 0.25, 0.1)


def marretada(rng, v):
    """A marretada de desenho: BONK oco de madeira, o peso, o achatamento e a mola "doing" no fim."""
    x = _z(1.15)
    n = n_de(0.5)
    poe(x, _madeira_oca(rng, n, rng.uniform(150, 175)) * 0.75, 0)
    poe(x, B.esmagar(rng, v)[: n_de(0.6)] * 0.65, 0)
    m = n_de(0.08)
    poe(x, satura(passa(ruido(rng, m), 300, 1800, 2) * env(m, 0.001, 0.03), 3) * 0.5, 0.005)        # o "esmagou"
    m = n_de(0.62)
    tt = np.arange(m) / SR
    f = 190 * (1 + 0.18 * np.sin(2 * math.pi * 16 * tt) * np.exp(-tt / 0.35))
    doing = np.sin(2 * math.pi * np.cumsum(f) / SR) + 0.35 * np.sin(4 * math.pi * np.cumsum(f) / SR)
    poe(x, doing * env(m, 0.004, 0.3) * 0.22, 0.12)
    for k in range(3):                                                                              # passarinhos tontos
        m = n_de(0.09)
        tt = np.arange(m) / SR
        piu = np.sin(2 * math.pi * np.cumsum(varre(2600, 3600, m, 0.6) * (1 + 0.06 * np.sin(2 * math.pi * 45 * tt))) / SR)
        poe(x, piu * env(m, 0.004, 0.04) * 0.06, 0.5 + k * 0.13)
    return reverb(x, 0.3, 0.14)


def bonk(rng, v):
    """Pancada de desenho na cabeça: "bonk" de madeira leve e a mola balançando."""
    x = _z(0.8)
    poe(x, _madeira_oca(rng, n_de(0.35), rng.uniform(260, 300)) * 0.7, 0)
    poe(x, B.soco_leve(rng, v) * 0.6, 0)
    m = n_de(0.5)
    tt = np.arange(m) / SR
    f = 300 * (1 + 0.15 * np.sin(2 * math.pi * 13 * tt) * np.exp(-tt / 0.25))
    poe(x, np.sin(2 * math.pi * np.cumsum(f) / SR) * env(m, 0.004, 0.25) * 0.2, 0.06)
    return reverb(x, 0.25, 0.12)


def martelo(rng, v):
    """Martelo de guerra: o ar pesado, a pancada que esmaga e o clangor curto da cabeça de metal."""
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.15, 1800, 300, 0.5), 0)
    poe(x, B.esmagar(rng, v), 0.13, 0.85)
    poe(x, B._placa_de_metal(rng, n_de(0.5), 120, 3000, 60, 0.12) * 0.45, 0.13)
    return x


def escudo_fisico(rng, v):
    """Ergue o escudo de mão: o ar do braço, o escudo encaixando com um "tonc" metálico abafado."""
    x = _z(0.9)
    poe(x, _whoosh(rng, 0.2, 500, 2000, 0.6, g=0.3), 0)
    poe(x, B.bloqueio(rng, v) * 0.9, 0.2)
    poe(x, passa(rosa(rng, n_de(0.3)), 80, 400, 2) * env(n_de(0.3), 0.002, 0.08) * 0.4, 0.2)
    return x


def iaido(rng, v):
    """Saque rápido: a lâmina deslizando na bainha, o "shing" curto e o corte."""
    x = _z(1.0)
    n = n_de(0.18)
    poe(x, passa(ruido(rng, n), 3000, 10000, 2) * sobe_e_some(n, 0.8, 1.5) * 0.4, 0)
    poe(x, B._lamina_curta(rng, n_de(0.3), rng.uniform(2800, 3400)) * 0.3, 0.17)
    poe(x, B.corte_pesado(rng, v), 0.38, 0.9)
    return x



# ================================================================== reviver e renascer
def ressurreicao(rng, v):
    """Reviver: o ar se abre (descida de luz), um coro sobe, sinos em cascata e um brilho
    com batida de coração no instante em que o aliado se levanta."""
    x = _z(2.0)
    n = n_de(0.55)
    poe(x, assobio(rng, n, 6000, 1800, 0.9, 0.35) * sobe_e_some(n, 0.8, 1.2) * 0.35, 0)
    m = n_de(1.5)
    tt = np.arange(m) / SR
    coro = sum(seno(np.full(m, nota(mm)) * (1 + 0.004 * np.sin(2 * math.pi * (4.3 + 0.6 * k) * tt)), m) for k, mm in enumerate((67, 72, 76, 79)))
    poe(x, coro * env(m, 0.45, 0.9) * 0.06, 0.15)
    for k, mm in enumerate((79, 84, 88, 91, 96)):
        poe(x, modal(n_de(1.1), nota(mm), rng=rng, **SINO) * env(n_de(1.1), 0.005, 0.7) * 0.11, 0.35 + k * 0.07)
    batida = seno(varre(nota(40), nota(33), n_de(0.25), 1.5), n_de(0.25)) * env(n_de(0.25), 0.003, 0.12) * 0.5
    poe(x, batida, 0.62)
    poe(x, batida * 0.7, 0.82)
    poe(x, _brilho(rng, 0.9, nota(100), 0.12, CRISTAL), 0.62)
    return reverb(x, 0.9, 0.42, 9000)


# ================================================================== provocar
def provocar(rng, v):
    """Provocar: duas batidas de peito, um brado de metal rouco (como uma corneta de guerra
    desafinada) e o eco de um escudo batido — o rival vira a cabeça na hora."""
    x = _z(1.4)
    for k, t0 in enumerate((0.0, 0.16)):
        poe(x, baque(n_de(0.22), 120 - 10 * k, 55, 0.1, 0.5) * (0.75 + 0.15 * k), t0)
    n = n_de(0.62)
    t = np.arange(n) / SR
    vib = 1 + 0.012 * np.sin(2 * math.pi * 6.5 * t)
    f = varre(nota(50), nota(55), n, 2.5) * vib
    brado = sum(seno(f * h, n) / h ** 0.8 for h in (1, 2, 3, 4, 5, 6))
    brado = satura(passa(brado, 180, 3200) * 1.6, 2.2) * env(n, 0.03, 0.3, segura=0.18) * 0.22
    quinta = satura(sum(seno(f * 1.5 * h, n) / h for h in (1, 2, 3)), 1.8) * env(n, 0.05, 0.25, segura=0.12) * 0.08
    poe(x, brado + quinta, 0.3)
    poe(x, passa(rosa(rng, n_de(0.5)), 300, 2500) * env(n_de(0.5), 0.02, 0.18) * 0.08, 0.3)
    poe(x, modal(n_de(0.9), nota(64), rng=rng, **METAL) * env(n_de(0.9), 0.002, 0.35) * 0.14, 0.34)
    return reverb(x, 0.5, 0.3, 7000)


# ================================================================== refletir, espinhos, vampirismo
def sono(rng, v):
    """Sono: uma caixinha de música desce três notas devagar e um sopro morno embala."""
    x = _z(1.6)
    for k, m in enumerate((84, 79, 76, 72)):
        poe(x, modal(n_de(0.9), nota(m), rng=rng, **SINO) * env(n_de(0.9), 0.004, 0.5) * (0.12 - 0.015 * k), 0.05 + 0.22 * k)
    n = n_de(1.1)
    poe(x, passa(rosa(rng, n), 200, 1200) * sobe_e_some(n, 0.5, 1.6) * 0.08, 0.1)
    return reverb(x, 0.9, 0.4, 7000)


def cegueira(rng, v):
    """Cego: estalo de flash e um zumbido agudo que fica no ouvido e some."""
    x = _z(1.2)
    poe(x, estalo(rng, n_de(0.04), 2000, 12000, 0.006) * 0.6, 0.0)
    poe(x, passa(ruido(rng, n_de(0.12)), 3000, 12000) * env(n_de(0.12), 0.001, 0.05) * 0.4, 0.0)
    n = n_de(0.9)
    poe(x, seno(np.full(n, 4200.0), n) * env(n, 0.01, 0.4) * 0.05, 0.03)
    return reverb(x, 0.5, 0.25, 12000)


def errou(rng, v):
    """Errou: o golpe passa longe — um assobio que cruza e some, sem impacto."""
    x = _z(0.5)
    n = n_de(0.32)
    poe(x, assobio(rng, n, 900, 3200, 0.8, 0.6) * sobe_e_some(n, 0.4, 1.0) * 0.3, 0.0)
    return reverb(x, 0.3, 0.15, 9000)


def barreira_anula(rng, v):
    """Barreira: o debuff bate na cúpula e se desfaz — um tinido claro e um eco curto."""
    x = _z(0.9)
    poe(x, modal(n_de(0.7), nota(91), rng=rng, **CRISTAL) * env(n_de(0.7), 0.001, 0.3) * 0.18, 0.0)
    poe(x, modal(n_de(0.5), nota(98), rng=rng, **VIDRO) * env(n_de(0.5), 0.001, 0.2) * 0.08, 0.04)
    poe(x, baque(n_de(0.1), 300, 180, 0.04, 0.5) * 0.2, 0.0)
    return reverb(x, 0.6, 0.3, 11000)


def dissipar(rng, v):
    """Dissipar: um zumbido mágico que segura a nota, racha (estalos de vidro) e se desfaz num
    sopro que desce."""
    x = _z(1.2)
    n = n_de(0.35)
    t = np.arange(n) / SR
    zumbe = sum(seno(np.full(n, nota(m)) * (1 + 0.006 * np.sin(2 * math.pi * 7 * t)), n) for m in (76, 83)) * env(n, 0.03, 0.2, segura=0.12) * 0.07
    poe(x, zumbe, 0.0)
    for k in range(5):
        poe(x, modal(n_de(0.3), nota(88 + 2 * k), rng=rng, **VIDRO) * env(n_de(0.3), 0.001, 0.12) * (0.12 - 0.015 * k), 0.24 + 0.035 * k)
        poe(x, estalo(rng, n_de(0.02), 2500, 9000, 0.003) * 0.25, 0.24 + 0.035 * k)
    m = n_de(0.6)
    poe(x, assobio(rng, m, 7000, 1500, 0.8, 0.4) * sobe_e_some(m, 0.2, 1.4) * 0.14, 0.32)
    return reverb(x, 0.7, 0.32, 9000)


def reflexo(rng, v):
    """Refletir: o golpe bate num espelho (tinido de vidro com brilho) e volta num assobio que sobe."""
    x = _z(1.1)
    poe(x, modal(n_de(0.8), nota(86), rng=rng, **VIDRO) * env(n_de(0.8), 0.001, 0.4) * 0.2, 0.0)
    poe(x, modal(n_de(0.6), nota(93), rng=rng, **CRISTAL) * env(n_de(0.6), 0.001, 0.3) * 0.1, 0.01)
    poe(x, baque(n_de(0.12), 260, 140, 0.05, 0.6) * 0.3, 0.0)
    n = n_de(0.35)
    volta = seno(varre(nota(70), nota(96), n, 1.6), n) * env(n, 0.02, 0.18) * 0.12
    poe(x, volta + assobio(rng, n, 2500, 9000, 0.7, 0.5) * sobe_e_some(n, 0.3, 0.9) * 0.12, 0.06)
    return reverb(x, 0.6, 0.3, 10000)


def espinhos(rng, v):
    """Espinhos: madeira estalando enquanto as pontas brotam, e furadas curtas e secas."""
    x = _z(0.9)
    for k in range(7):
        poe(x, estalo(rng, n_de(0.025), 900, 5000, 0.004) * (0.4 - 0.03 * k), 0.012 * k + rng.uniform(0, 0.008))
    for k in range(3):
        n = n_de(0.09)
        fura = passa(ruido(rng, n), 1800, 7000) * env(n, 0.001, 0.025) * 0.35
        fura += seno(varre(nota(76), nota(64), n, 2), n) * env(n, 0.001, 0.03) * 0.12
        poe(x, fura, 0.07 + 0.06 * k)
    poe(x, baque(n_de(0.16), 180, 90, 0.06, 0.5) * 0.25, 0.05)
    return reverb(x, 0.35, 0.18, 8000)


def vampirismo(rng, v):
    """Vampirismo: uma sucção úmida que puxa para dentro, um gole grave e duas batidas de coração."""
    x = _z(1.3)
    n = n_de(0.45)
    puxa = passa(rosa(rng, n), 300, 1800) * sobe_e_some(n, 0.75, 1.5) * 0.3
    puxa *= 1 + 0.5 * np.sin(2 * math.pi * 18 * np.arange(n) / SR)
    poe(x, puxa, 0.0)
    gole = seno(varre(nota(48), nota(40), n_de(0.18), 1.4), n_de(0.18)) * env(n_de(0.18), 0.01, 0.08) * 0.35
    poe(x, gole, 0.36)
    batida = seno(varre(nota(40), nota(33), n_de(0.22), 1.5), n_de(0.22)) * env(n_de(0.22), 0.003, 0.1) * 0.5
    poe(x, batida, 0.55)
    poe(x, batida * 0.7, 0.75)
    return reverb(x, 0.55, 0.3, 6000)


def renascer(rng, v):
    """Renascer: brasas estalando que se juntam, o fogo sobe num rugido, a fênix grita e as asas batem."""
    x = _z(2.0)
    for k in range(16):
        poe(x, estalo(rng, n_de(0.03), 1500, 7000, 0.004) * (0.2 + 0.03 * k), 0.02 * k + rng.uniform(0, 0.02))
    poe(x, _whoosh(rng, 0.5, 200, 3000, 0.9, 1.6, 0.8), 0.1)
    poe(x, B.fogo(rng, v), 0.45, 1.0)
    n = n_de(0.75)
    t = np.arange(n) / SR
    grito = seno(varre(nota(82), nota(92), n, 0.35) * (1 + 0.025 * np.sin(2 * math.pi * 8 * t)), n) * env(n, 0.04, 0.45) * 0.24
    grito += seno(varre(nota(89), nota(99), n, 0.35), n) * env(n, 0.04, 0.35) * 0.09
    poe(x, grito, 0.55)
    for k in range(2):
        poe(x, _whoosh(rng, 0.28, 180, 1400, 0.4, 1.2, 0.7), 0.75 + k * 0.32)
    poe(x, passa(rosa(rng, n_de(0.6)), 40, 220, 2) * env(n_de(0.6), 0.01, 0.35) * 0.5, 0.45)
    return reverb(x, 0.7, 0.32, 6000)


def brasas_renascendo(rng, v):
    """Renascendo: estalos fracos de brasa e um sopro baixo, à espera."""
    x = _z(1.0)
    for k in range(9):
        poe(x, estalo(rng, n_de(0.025), 1200, 6000, 0.004) * rng.uniform(0.08, 0.18), rng.uniform(0, 0.9))
    n = n_de(1.0)
    x += passa(rosa(rng, n), 80, 500, 2) * sobe_e_some(n, 0.5, 1.0) * 0.08
    return reverb(x, 0.4, 0.2, 5000)

SONS_NOVOS = {
    nome.replace("_", "-"): (fn, "família " + nome.replace("_", " "))
    for nome, fn in list(globals().items())
    if callable(fn) and not nome.startswith("_") and fn.__module__ == __name__ and nome not in ("nota",)
}
# volume pela prioridade: habilidades no nível dos golpes; apoio e status mais baixos
_BAIXO = {"brasas-renascendo", "cura-em-area", "regeneracao", "grito-de-guerra", "velocidade", "escudo-tech", "barreira-magica", "armadura", "resgate",
          "bencao", "lanche", "purificacao", "enfraquecimento", "lentidao", "marca", "silencio", "medo", "exposto", "hipnose",
          "encanto", "runas", "lua", "petalas", "regeneracao", "confusao", "estrela-invencivel", "disco", "flecha"}
_ALTO = {"sono", "cegueira", "errou", "barreira-anula", "dissipar", "reflexo", "espinhos", "vampirismo", "provocar", "renascer", "ressurreicao", "soco-serio", "supernova", "kamehameha", "canhao-de-energia", "foguete", "tempestade", "punho-gigante", "pisao",
         "martelo", "espadao", "buraco-negro", "tsunami", "transformacao-v2", "dragao", "susanoo", "dominio"}
_ANTES = {"chidori-carga": "faíscas do Chidori", "esfera-espiral-carga": "a esfera girando", "kamehameha-carga": "carga do Kamehameha",
          "kamehameha-feixe": "o feixe saindo", "marretada-giro": "a marreta subindo"}
for _k, _d in _ANTES.items():
    SONS_NOVOS[_k] = (SONS_NOVOS[_k][0], _d)
_ALTO |= {"marretada", "kamehameha-feixe"}
ALVO_NOVO = {k: (-23 if k in _BAIXO else -15 if k in _ALTO else -18) for k in SONS_NOVOS}
