"""O Hulk: o soco, as três habilidades e a fúria, desenhados para ele.

Pedido do jogador: "o Hulk tem que ser mais forte… colocar coisas mais
interessantes pra ele… faz as três skills dele também, as animações, os áudios,
tudo próprio dele".

- soco_do_hulk: o punho enorme entrando (de −x), o estalo e a onda de choque que
  se abre para os lados (o soco largo pega quem está perto do alvo).
- hulk_esmaga: os dois punhos descem juntos do alto no rival, o chão racha numa
  cratera, as pedras voam, a poeira sobe e as estrelinhas giram (Paralisado).
- grito_hulk: o rugido saindo dele — os arcos de som abrindo para a frente (nele).
- rugido_do_hulk: as ondas do rugido chegando no rival, que treme, com a poeira
  arrastada e as setas para baixo (Enfraquecido).
- furia_hulk: a fúria nele — a aura verde subindo como fogo, os raios de raiva,
  o vapor e as setas para cima (Fortalecido e Acelerado).
- mais_forte_ainda: o gancho de baixo para cima no rival, a onda que sobe e o
  clarão.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, pulso, rel, vazio


def _quadro(t, seed=0):
    return np.random.default_rng(seed + int(t * 997) % 9973)


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _punho(cx, cy, esc, ang=0.0):
    """Um punho fechado visto de lado: o bloco dos dedos com os nós e o polegar por baixo
    (apontando para +x antes de girar)."""
    pts = [(-0.55, -0.42), (-0.1, -0.5), (0.18, -0.46), (0.36, -0.36), (0.46, -0.18), (0.48, 0.05),
           (0.42, 0.24), (0.28, 0.36), (0.02, 0.42), (-0.2, 0.44), (-0.4, 0.36), (-0.55, 0.2)]
    return _gira([(x * esc, y * esc) for x, y in pts], ang, cx, cy)


def _nos(cx, cy, esc, ang=0.0):
    """As linhas entre os dedos (para o punho não virar uma bola)."""
    segs = []
    for y in (-0.22, 0.02, 0.24):
        a = _gira([(0.12 * esc, y * esc), (0.44 * esc, y * esc * 0.9)], ang, cx, cy)
        segs.append((a[0][0], a[0][1], a[1][0], a[1][1], 1.0))
    return segs


def _pedras(T, t, seed, n, ini, alcance=0.85, gravidade=0.7, tam=0.016):
    sub = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        a = -math.pi / 2 + sub.normal(0, 0.9)
        f = rel(t, ini, ini + 0.7)
        d = alcance * ease_out(f, 2) * sub.uniform(0.3, 1)
        x, y = d * math.cos(a), d * math.sin(a) * 0.8 + gravidade * f * f
        pts.append((x, y, pulso(t, ini, ini + 0.75) * sub.uniform(0.4, 1)))
    return T.splats(pts, tam)


# ------------------------------------------------------------------ o soco
def soco_do_hulk(T, t, rng):
    """O soco do Hulk: o punho grande entra de −x, para no rival com um estalo, e a onda de choque
    abre para os lados (achatada), levantando poeira — o soco largo pega quem está perto."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    entra = ease_in(rel(t, 0.0, 0.16), 1.8)
    px = -1.1 + 0.95 * entra
    some = 1 - rel(t, 0.25, 0.42)
    P = T.polys([(_punho(px, 0.0, 0.42), 1.0)], 0.005) * some
    N = T.lines(_nos(px, 0.0, 0.42), 0.012) * some
    rastro = T.tapered([(px - 0.9, y, px - 0.15, y * 0.8, 1.0) for y in (-0.14, 0.0, 0.14)], 0.04) * (1 - rel(t, 0.16, 0.3))
    k = pulso(t, 0.14, 0.45)
    clarao = T.gauss(0.05, 0, 0.2) * k * 1.6 + T.flare(0.05, 0, 1.1 * k + 1e-3, 0.0, 0.012) * k
    onda = T.ring(0.15 + 0.85 * ease_out(rel(t, 0.15, 0.6), 2), 0.045, 0.05, 0.05, 2.4) * pulso(t, 0.15, 0.7)
    po = T.splats([(np.random.default_rng(j).normal(0, 0.35), 0.25 - 0.25 * rel(t, 0.3, 1.0), 0.8) for j in range(10)], 0.08) * pulso(t, 0.25, 1.0) * 0.4
    G += (np.clip(P - N * 0.8, 0, None) * 1.05 + rastro * 0.6 + clarao + onda * 1.1 + po + _pedras(T, t, 7, 14, 0.15, 0.6, 0.5, 0.013)) * env
    H += (P * 0.25 + clarao * 1.1 + onda * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Esmagar
def hulk_esmaga(T, t, rng):
    """Esmagar: os dois punhos juntos descem do alto (girados para baixo), batem no rival, o chão
    racha numa cratera achatada, as pedras voam, a poeira sobe e três estrelinhas giram em volta da
    cabeça dele (Paralisado)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    desce = ease_in(rel(t, 0.0, 0.22), 2.2)
    py = -1.15 + 1.15 * desce
    some = 1 - rel(t, 0.3, 0.45)
    punhos = T.polys([(_punho(-0.2, py, 0.45, math.pi / 2), 1.0), (_punho(0.2, py, 0.45, math.pi / 2), 1.0)], 0.005) * some
    nos = (T.lines(_nos(-0.2, py, 0.45, math.pi / 2), 0.012) + T.lines(_nos(0.2, py, 0.45, math.pi / 2), 0.012)) * some
    risco = T.tapered([(x, py - 0.9, x, py - 0.2, 1.0) for x in (-0.35, -0.2, 0.0, 0.2, 0.35)], 0.04) * (1 - rel(t, 0.2, 0.32))
    bate = 0.22
    k = pulso(t, bate, bate + 0.4)
    clarao = T.gauss(0, 0.15, 0.3, 0.2) * k * 1.8 + T.flare(0, 0.2, 1.4 * k + 1e-3, 0.0, 0.01) * k
    cratera = T.ring(0.2 + 0.7 * ease_out(rel(t, bate, bate + 0.45), 2), 0.05, 0, 0.42, 3.2) * pulso(t, bate, bate + 0.6)
    q = np.random.default_rng(29)
    rachas = T.zero()
    if t > bate:
        cresce = ease_out(rel(t, bate, bate + 0.25), 2)
        for j in range(7):
            a = math.pi * (j + 0.5) / 7
            comp = 0.75 * cresce * q.uniform(0.6, 1)
            pts = jagged(q, 0, 0.42, comp * math.cos(a) * 1.2, 0.42 + comp * math.sin(a) * 0.3 * (1 if j % 2 else -0.4), 4, 0.25)
            rachas += T.polyline(pts, 0.012)
        rachas *= 1 - rel(t, 0.7, 0.95)
    po = T.splats([(q.normal(0, 0.45), 0.35 - 0.45 * rel(t, bate, 1.0) * q.uniform(0.4, 1), 0.8) for _ in range(14)], 0.09) * pulso(t, bate, 1.0) * 0.5
    # as estrelinhas do Paralisado girando em volta da cabeça
    tonto = T.zero()
    vivo = rel(t, 0.4, 0.5) * (1 - rel(t, 0.85, 0.97))
    if vivo > 0:
        for j in range(3):
            a = TAU * (t * 1.6 + j / 3)
            tonto += T.polys([(estrela(0.32 * math.cos(a), -0.55 + 0.08 * math.sin(a), 0.07, a, 5, 0.45), 1.0)], 0.004)
    G += (np.clip(punhos - nos * 0.8, 0, None) * 1.05 + risco * 0.6 + clarao + cratera * 1.1 + rachas * 1.2 + po + _pedras(T, t, 31, 22, bate, 0.95, 0.9, 0.018) * 1.1 + tonto * vivo * 1.3) * env
    H += (punhos * 0.25 + clarao * 1.1 + cratera * 0.4 + rachas * 0.6 + tonto * vivo * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Rugido
def grito_hulk(T, t, rng):
    """O rugido saindo do Hulk: os arcos de som abrindo para a frente (+x), um atrás do outro, e o
    ar tremendo perto da boca."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    arcos = T.zero()
    for j in range(5):
        f = rel(t, 0.08 * j, 0.08 * j + 0.55)
        if f <= 0 or f >= 1:
            continue
        r = 0.12 + 0.8 * ease_out(f, 1.6)
        arcos += T.arc_band(r, 0.035 * (1 - 0.5 * f) + 0.01, -0.85, 0.85, 1.0, 0.0, -0.3, 0, 1.0, True) * (1 - f)
    boca = T.gauss(-0.3, 0, 0.12) * pulso(t, 0.0, 0.7)
    q = _quadro(t, 41)
    linhas = T.tapered([(-0.2, y, -0.2 + q.uniform(0.3, 0.6), y * 1.4, 1.0) for y in q.normal(0, 0.15, 6)], 0.015) * pulso(t, 0.0, 0.7)
    G += (arcos * 1.3 + T.blur(arcos, 0.02) * 0.6 + boca + linhas * 0.6) * env
    H += (arcos * 0.5 + boca * 0.8) * env
    return G, H


def rugido_do_hulk(T, t, rng):
    """As ondas do rugido chegando no rival (vêm de −x): ele treme (as linhas de tremor dos lados), a
    poeira é arrastada para trás e as setas para baixo descem (Enfraquecido)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    ondas = T.zero()
    for j in range(4):
        f = rel(t, 0.1 * j, 0.1 * j + 0.45)
        if f <= 0 or f >= 1:
            continue
        x = -0.9 + 1.2 * f
        ondas += T.arc_band(0.55, 0.035, -0.9, 0.9, 1.0, 0.0, x - 0.55, 0, 1.0, True) * (1 - f)
    treme = pulso(t, 0.15, 0.8)
    tremor = T.zero()
    for s in (-1, 1):
        for j in range(3):
            x = s * (0.36 + 0.06 * j) + 0.02 * math.sin(TAU * t * 14 + j)
            tremor += T.lines([(x, -0.2 + 0.05 * j, x + 0.04 * s, 0.2 - 0.05 * j, 1.0)], 0.012)
    tremor *= treme
    po = T.splats([(-0.2 + 0.9 * rel(t, 0.2, 1.0) * np.random.default_rng(j).uniform(0.4, 1), np.random.default_rng(j + 9).normal(0.25, 0.12), 0.8) for j in range(10)], 0.06) * pulso(t, 0.2, 1.0) * 0.45
    setas = T.zero()
    vivo = pulso(t, 0.35, 0.95)
    for j, x in enumerate((-0.18, 0.0, 0.18)):
        y = -0.3 + 0.5 * ((t * 1.2 + j * 0.3) % 1)
        setas += T.polys([([(x - 0.05, y - 0.05), (x + 0.05, y - 0.05), (x + 0.05, y + 0.02), (x + 0.1, y + 0.02), (x, y + 0.12), (x - 0.1, y + 0.02), (x - 0.05, y + 0.02)], 1.0)], 0.004)
    G += (ondas * 1.3 + T.blur(ondas, 0.02) * 0.5 + tremor * 1.1 + po + setas * vivo * 0.9) * env
    H += (ondas * 0.5 + tremor * 0.6 + setas * vivo * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Mais forte ainda
def furia_hulk(T, t, rng):
    """A fúria do Hulk: a aura verde subindo dele como fogo (o ruído correndo para cima), os raios
    curtos de raiva estalando, o vapor saindo e as setas para cima (Fortalecido e Acelerado)."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1) * min(1.0, rel(t, 0.0, 0.12) * 1.5 + 0.2)
    base = 0.62
    up = base - T.V
    env_x = np.exp(-(T.U / (0.42 + 0.1 * np.clip(up, 0, 1))) ** 2)
    n = np.roll(T.noise(np.random.default_rng(51), 0.05, 3), -int((t * 1.4 % 1) * T.H), axis=0)
    corpo = np.clip(1 - up / 1.35, 0, 1) * (up > -0.05)
    aura = np.clip(env_x * corpo * (1.3 + 0.55 * n) - 0.45, 0, 1)
    borda = np.clip(aura - T.blur(aura, 0.02) * 0.9, 0, 1) * 2
    q = _quadro(t, 53)
    raios = T.zero()
    for _ in range(3):
        a = q.uniform(0, TAU)
        r0 = q.uniform(0.2, 0.35)
        raios += T.polyline(jagged(q, r0 * math.cos(a), r0 * math.sin(a), (r0 + 0.3) * math.cos(a), (r0 + 0.3) * math.sin(a), 3, 0.35), 0.01)
    sub = np.random.default_rng(55)
    vapor = T.splats([(sub.normal(0, 0.25), -0.2 - 0.8 * ((sub.uniform() + t * 0.7) % 1), 0.7 * sub.uniform(0.4, 1)) for _ in range(12)], 0.06) * 0.4
    setas = T.zero()
    for j, x in enumerate((-0.55, 0.55)):
        y = 0.4 - 0.9 * ((t * 1.1 + j * 0.5) % 1)
        setas += T.polys([([(x - 0.05, y + 0.05), (x + 0.05, y + 0.05), (x + 0.05, y - 0.02), (x + 0.1, y - 0.02), (x, y - 0.12), (x - 0.1, y - 0.02), (x - 0.05, y - 0.02)], 1.0)], 0.004)
    G += (aura * 0.9 + borda * 0.6 + raios * 1.2 + vapor + setas * 0.9) * env
    H += (aura ** 3 * 0.5 + raios * 0.8) * env
    return G, H


def mais_forte_ainda(T, t, rng):
    """O gancho de baixo para cima: o punho sobe de baixo do rival, bate com o clarão, a onda sobe
    em leque (o rival é jogado para o alto) e os riscos de velocidade para cima."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    sobe = ease_in(rel(t, 0.0, 0.2), 1.8)
    py = 1.0 - 1.05 * sobe
    some = 1 - rel(t, 0.28, 0.42)
    P = T.polys([(_punho(0.0, py, 0.42, -math.pi / 2), 1.0)], 0.005) * some
    N = T.lines(_nos(0.0, py, 0.42, -math.pi / 2), 0.012) * some
    k = pulso(t, 0.18, 0.5)
    clarao = T.gauss(0, -0.05, 0.22) * k * 1.8 + T.flare(0, -0.05, 1.2 * k + 1e-3, 0.0, 0.012) * k
    leque = T.zero()
    for j in range(4):
        f = rel(t, 0.18 + 0.05 * j, 0.6 + 0.05 * j)
        if f <= 0 or f >= 1:
            continue
        leque += T.arc_band(0.2 + 0.7 * ease_out(f, 2), 0.03, -math.pi / 2 - 0.9, -math.pi / 2 + 0.9, 1.0, 0.0, 0, 0.1, 1.0, True) * (1 - f)
    riscos = T.tapered([(x, 0.5, x * 0.8, -0.6 - 0.3 * rel(t, 0.2, 0.5), 1.0) for x in (-0.3, -0.12, 0.12, 0.3)], 0.025) * pulso(t, 0.2, 0.6)
    G += (np.clip(P - N * 0.8, 0, None) * 1.05 + clarao + leque * 1.2 + riscos * 0.7 + _pedras(T, t, 61, 12, 0.2, 0.7, 0.6, 0.013)) * env
    H += (P * 0.25 + clarao * 1.1 + leque * 0.4) * env
    return G, H


REGISTRO = [
    ("soco_do_hulk", soco_do_hulk, GRANDE, "Hulk · o soco enorme e a onda de choque para os lados", False),
    ("hulk_esmaga", hulk_esmaga, GRANDE, "Hulk · Esmagar: os dois punhos do alto, a cratera e as estrelinhas", False),
    ("grito_hulk", grito_hulk, MEDIA, "Hulk · o rugido saindo dele em arcos", False),
    ("rugido_do_hulk", rugido_do_hulk, GRANDE, "Hulk · as ondas do rugido chegando, o rival treme", False),
    ("furia_hulk", furia_hulk, GRANDE, "Hulk · a fúria: aura verde, raios e vapor", False),
    ("mais_forte_ainda", mais_forte_ainda, GRANDE, "Hulk · Mais forte ainda: o gancho de baixo para cima", False),
]
