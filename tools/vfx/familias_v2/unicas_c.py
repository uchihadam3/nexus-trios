"""Rodada 2 das Mecânicas únicas ativando como habilidade: Doutor Estranho, Flash, Mulher-Maravilha, Homem de
Ferro, Capitão América, Deadpool, Thanos, Gohan, Piccolo, Freeza, Kakashi, Tanjiro, Nezuko, Zenitsu, Inosuke,
Muzan, Yuji, Megumi, Nobara e Sukuna.

- portal: o anel de faíscas do Doutor Estranho abre girando, soltando faíscas pela tangente.
- rastro_flash: os riscos de velocidade cruzam a tela e o emblema do raio acende no círculo.
- laco: o Laço da verdade dourado gira no ar, desce e aperta em volta do rival.
- unibeam: o reator acende no peito, puxa a energia e solta o feixe.
- lider: o escudo de estrela sobe e as três setas sobem pelos aliados.
- fator_cura: as duas katanas cruzam e as cruzes de cura sobem enquanto a ferida pulsa.
- joia: a Joia do Infinito se forma e encaixa no arco das seis.
- estalo: as seis joias acendem, o estalo clareia e o pó se desfaz ao vento.
- potencial: a aura afiada explode em pontas, com os raios em volta (o potencial despertado).
- treino: a capa pesada cai no chão com poeira, e o ki verde sobe no aluno.
- sofrimento: a Supernova cresce no alto e as esferas de energia orbitam.
- copia: o pergaminho desenrola e os traços do jutsu copiado aparecem.
- fio: o fio vermelho da abertura liga até o alvo e o corte d'água passa por ele.
- sangue: as chamas rosadas do Sangue explosivo abrem em flor e as gotas espirram.
- zzz: os "Z" sobem e o relâmpago amarelo cruza (Primeira postura).
- juntas: as juntas estalam e se soltam: os ossos saem do lugar e as correntes partem.
- bracos: os braços-chicote saem para todo lado, curvos.
- black_flash: o Black Flash — o raio vermelho e negro que racha o espaço.
- mahoraga: a roda de oito cabos gira um dente (a adaptação).
- boneca: a boneca de palha, o prego e a martelada que ressoa.
- santuario: o telhado do Santuário sobe atrás e os cortes chovem por toda parte.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .unicas_kit import (CARTA, CHAMA, ESCUDO, ESPADA, GEMA, GOTA, OSSO, RAIO, SETA, anel, aura, cheio, chuva, circulo,
                         clarao, converge, corte, estouro, estrela_pts, icone, onda_no_chao, orbita, particulas, poe, raios,
                         runas, surge)


def portal(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.35), 2.5)
    if abre > 0:
        r = 0.5 * abre
        q = np.random.default_rng(5)
        segs = []
        for j in range(130):
            a = q.uniform(0, TAU) + t * 9
            rr = r * q.uniform(0.9, 1.1)
            x, y = rr * math.cos(a), rr * math.sin(a)
            c = q.uniform(0.08, 0.2)
            segs.append((x + c * math.sin(a), y - c * math.cos(a), x, y, q.uniform(0.5, 1)))
        G += T.tapered(segs, 0.022) * 1.5 + T.ring(r, 0.03, 0, 0) * 0.9
        H += T.ring(r, 0.008, 0, 0) * 1.1
        G += T.gauss(0, 0, r * 0.7) * 0.25 * abre
        # as faíscas que escapam pela tangente
        u = (t * 3) % 1
        fs = []
        for j in range(16):
            a = TAU * j / 16 + t * 9
            x, y = r * math.cos(a), r * math.sin(a)
            fs.append((x, y, x + 0.18 * u * math.sin(a) + 0.05 * u * math.cos(a), y - 0.18 * u * math.cos(a) + 0.05 * u * math.sin(a), 1 - u))
        G += T.tapered(fs, 0.016) * 1.3
    g, h = runas(T, t, 0.1, 0.95, 0.32, 10, 0, 1.0, -2.0)
    return (G + g * 0.35) * env, (H + h) * env


def rastro_flash(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    q = np.random.default_rng(3)
    segs = []
    for j in range(16):
        y = q.uniform(-0.6, 0.6)
        ini = q.uniform(0, 0.4)
        u = rel(t, ini, ini + 0.35)
        if 0 < u < 1:
            x = -1.1 + 2.4 * ease_in(u, 1.3)
            segs.append((x - 0.6, y, x, y, 1 - 0.5 * u))
    G += T.tapered(segs, 0.022) * 1.2
    for j in range(3):
        u = rel(t, 0.1 + 0.15 * j, 0.45 + 0.15 * j)
        if 0 < u < 1:
            x = -1 + 2.2 * u
            G += T.polyline(jagged(q, x - 0.5, 0.05 * (j - 1), x, 0.05 * (j - 1), 4, 0.2), 0.012) * (1 - u) * 1.3
    s = surge(t, 0.3, 0.55) * (1 - rel(t, 0.85, 1))
    if s > 0:
        G += T.ring(0.3 * s, 0.03, 0, 0) * 1.3 + T.gauss(0, 0, 0.26 * s) * 0.35
        g, h = cheio(T, poe(RAIO, 0, 0, 0.24 * s, 0.35), 1.2)
        G, H = G + g, H + h * 2
    g, h = clarao(T, t, 0.3, 0.55, tam=0.7)
    return (G + g) * env, (H + h) * env


def laco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    gira = rel(t, 0.0, 0.45)
    if gira < 1:
        # o laço girando no alto, a corda vindo da esquerda
        r = 0.32
        cy = -0.55 + 0.1 * gira
        G += T.ring(r, 0.025, 0, cy, 2.6) * 1.3
        a = t * 20
        G += T.polyline([(-1.0, 0.1), (-0.6, -0.1), (r * math.cos(a), cy + r * math.sin(a) / 2.6)], 0.02) * 1.0
    aperta = rel(t, 0.4, 0.75)
    if aperta > 0:
        r = 0.55 - 0.25 * ease_out(aperta, 3)
        G += T.ring(r, 0.03, 0, 0.05, 1.8) * 1.4 + T.ring(r * 0.94, 0.012, 0, 0.05, 1.8) * 0.8
        H += T.ring(r, 0.01, 0, 0.05, 1.8) * 1.2
        # o trançado da corda
        segs = []
        for j in range(28):
            a = TAU * j / 28
            x, y = r * math.cos(a), 0.05 + r * math.sin(a) / 1.8
            segs.append((x - 0.02, y - 0.02, x + 0.02, y + 0.02, 1.0))
        G += T.lines(segs, 0.008) * 0.8
        G += T.polyline([(-1.0, 0.0), (-r, 0.05)], 0.02) * 1.0
    g, h = clarao(T, t, 0.68, 0.9, 0, 0.05, 0.6)
    G += particulas(T, t, 0.6, 1.0, 22, 8, 0, 0.05, 0.35, 0.3)
    return (G + g) * env, (H + h) * env


def unibeam(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    carga = ease_in(rel(t, 0.0, 0.4), 1.5)
    cx, cy = -0.5, 0.0
    if t < 0.5:
        G += T.ring(0.09 + 0.03 * carga, 0.02, cx, cy) * 1.4 + T.gauss(cx, cy, 0.05 + 0.08 * carga) * (0.5 + carga)
        H += T.gauss(cx, cy, 0.035 + 0.03 * carga) * (0.8 + carga)
        tri = [(cx, cy - 0.06), (cx + 0.052, cy + 0.03), (cx - 0.052, cy + 0.03)]
        G += T.polyline(tri + [tri[0]], 0.01) * 1.2
    G += converge(T, t, 0.0, 0.42, 18, 4, cx, cy, 0.5)
    feixe = rel(t, 0.4, 0.95)
    if 0 < feixe < 1:
        k = (1 - rel(feixe, 0.6, 1)) * ease_out(rel(feixe, 0, 0.15), 2)
        larg = 0.09 + 0.03 * math.sin(t * 60)
        G += T.gauss(0.25, 0, 0.75, larg * 1.6) * k * 1.4
        H += T.gauss(0.25, 0, 0.75, larg * 0.6) * k * 2.2
        G += T.ring(0.14, 0.03, cx, cy) * k
        H += T.gauss(cx, cy, 0.09) * k * 1.6
    return G * env, H * env


def lider(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    s = surge(t, 0.0, 0.3)
    if s > 0:
        k = 1 - rel(t, 0.55, 0.75)
        r = 0.3 * s
        for j, rr in enumerate((1.0, 0.78, 0.56)):
            G += T.ring(r * rr, 0.035 * s, 0, -0.1) * (1.3 if j % 2 == 0 else 0.7) * k
        g, h = cheio(T, poe(estrela_pts(5, 0.42), 0, -0.1, r * 0.4), 1.2 * k)
        G, H = G + g, H + h * 2 + T.gauss(0, -0.1, r * 0.3) * 0.5 * k
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        u = rel(t, 0.5 + 0.06 * j, 0.95)
        if 0 < u < 1:
            y = 0.45 - 0.8 * ease_out(u, 2)
            for d in range(2):
                g, h = icone(T, poe(SETA, x, y + 0.17 * d, 0.17, -math.pi / 2), (1 - u) * (1 - 0.4 * d) * 1.5, 0.6)
                G, H = G + g, H + h
    return G * env, H * env


def fator_cura(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.5, 0.7))
    for lado in (-1, 1):
        g, h = icone(T, poe(ESPADA, 0, 0, 0.45 * max(s, 0.01), lado * math.pi / 4), s)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.2, 0.42, tam=0.6)
    G, H = G + g, H + h
    for j in range(3):
        G += anel(T, t, 0.4 + 0.15 * j, 0.7 + 0.15 * j, 0.05, 0.4, 0.03)
    q = np.random.default_rng(12)
    for j in range(8):
        u = rel(t, 0.45 + 0.04 * j, 0.85 + 0.03 * j)
        if 0 < u < 1:
            x, y = q.uniform(-0.35, 0.35), 0.35 - 0.75 * u
            G += T.lines([(x - 0.04, y, x + 0.04, y, 1.0), (x, y - 0.04, x, y + 0.04, 1.0)], 0.018) * (1 - u) * 1.3
    return G * env, H * env


def _arco_de_joias(T, cx, cy, r, acesas, brilho=1.0):
    G, H = 0.0, 0.0
    for j in range(6):
        a = math.pi + math.pi * (j + 0.5) / 6
        x, y = cx + r * math.cos(a), cy + r * math.sin(a) * 0.8
        if j < acesas:
            g, h = cheio(T, poe(GEMA, x, y, 0.05), brilho)
            G, H = G + g + T.gauss(x, y, 0.05) * 0.5 * brilho, H + h
        else:
            G = G + T.ring(0.035, 0.008, x, y) * 0.6
    return G, H


def joia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    G += converge(T, t, 0.0, 0.4, 20, 9, 0, -0.1, 0.6)
    s = surge(t, 0.25, 0.45)
    voa = ease_in(rel(t, 0.5, 0.75), 2)
    x, y = 0.0, -0.1 + 0.42 * voa
    if s > 0 and voa < 1:
        g, h = cheio(T, poe(GEMA, x, y, 0.12 * s * (1 - 0.6 * voa)), 1.3)
        G, H = G + g + T.gauss(x, y, 0.12) * 0.6, H + h * 2
    if t > 0.3:
        k = rel(t, 0.3, 0.45)
        acesas = 3 + (1 if voa >= 1 else 0)
        g, h = _arco_de_joias(T, 0, 0.55, 0.42, acesas, k)
        G, H = G + g, H + h
        G += T.ring(0.42, 0.012, 0, 0.55, 1.25) * 0 + 0
    g, h = clarao(T, t, 0.72, 0.9, 0, 0.32, 0.5)
    return (G + g) * env, (H + h) * env


def estalo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = rel(t, 0.0, 0.25) * (1 - rel(t, 0.5, 0.6))
    if k > 0:
        g, h = _arco_de_joias(T, 0, 0.1, 0.4, 6, k * 1.4)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.28, 0.5, 0, -0.1, 1.2, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.3, 0.8, 0.05, 0.95, 0.05)
    # o pó: os grãos que se soltam e voam para a direita
    u = rel(t, 0.45, 1.0)
    if 0 < u < 1:
        q = np.random.default_rng(31)
        pts = []
        for _ in range(140):
            x0, y0 = q.uniform(-0.45, 0.45), q.uniform(-0.5, 0.45)
            atraso = (x0 + 0.45) / 0.9 * 0.4
            v = max(0, u - atraso)
            pts.append((x0 + 0.9 * v + 0.1 * math.sin(y0 * 9 + v * 6), y0 - 0.3 * v, (1 - v) * 0.8 if v > 0 else 0.15))
        G += T.splats(pts, 0.012) * 1.2
    return G * env, H * env


def potencial(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    s = ease_out(rel(t, 0.0, 0.3), 2.2)
    if s > 0:
        pontas = estrela_pts(14, 0.55)
        for j in range(2):
            ang = 0.15 * math.sin(t * 40 + j) + j * 0.22
            g, h = icone(T, poe(pontas, 0, 0, (0.55 - 0.15 * j) * s * (1 + 0.04 * math.sin(t * 70)), ang), (1 - rel(t, 0.7, 1)) * (1 - 0.3 * j))
            G, H = G + g, H + h
        G += T.gauss(0, 0, 0.3 * s) * 0.6
    G += raios(T, t, 0.15, 0.9, 4, 7, 0, 0, 0.6)
    g, h = clarao(T, t, 0.0, 0.25, tam=1.0, forca=1.4)
    G += anel(T, t, 0.05, 0.5, 0.1, 0.9, 0.05)
    G += particulas(T, t, 0.2, 0.9, 30, 3, 0, 0.3, 0.45, 0.8)
    return (G + g) * env, (H + h) * env


def treino(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cai = ease_in(rel(t, 0.0, 0.3), 2.2)
    if t < 0.75:
        y = -0.85 + 1.05 * cai
        capa = [(-0.1, y - 0.32), (0.1, y - 0.32), (0.2, y - 0.26)] + [(0.2 + 0.18 * v, y - 0.26 + 0.52 * v) for v in (0.3, 0.6, 1.0)] + \
               [(0.38 - 0.76 * v, y + 0.26 + 0.04 * math.sin(v * 12)) for v in np.linspace(0, 1, 9)] + [(-0.2 - 0.18 * v, y - 0.26 + 0.52 * v) for v in (1.0, 0.6, 0.3)] + [(-0.2, y - 0.26)]
        g, h = icone(T, capa, 1 - rel(t, 0.55, 0.75), 0.5)
        G, H = G + g, H + h
        G += T.lines([(-0.22, y - 0.25, -0.34, y - 0.38, 1.0), (0.22, y - 0.25, 0.34, y - 0.38, 1.0)], 0.012) * (1 - rel(t, 0.55, 0.75))
    G += onda_no_chao(T, t, 0.3, 0.75, 0.85, 0.42)
    q = np.random.default_rng(4)
    u = rel(t, 0.3, 0.8)
    if 0 < u < 1:
        pts = [(q.uniform(-0.6, 0.6), 0.42 - 0.25 * u * q.uniform(0.5, 1.2), (1 - u) * q.uniform(0.4, 1)) for _ in range(40)]
        G += T.splats(pts, 0.035) * 0.8
    G += particulas(T, t, 0.45, 1.0, 26, 9, 0, 0.1, 0.35, 0.7)
    g, h = aura(T, t, 0.45, 1.0, 0.36, 0.0, 1.0)
    return (G + g) * env, (H + h) * env


def sofrimento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cresce = ease_out(rel(t, 0.0, 0.5), 1.8)
    if cresce > 0:
        r = 0.04 + 0.2 * cresce
        G += T.gauss(0, -0.5, r) * 1.3 + T.ring(r * 1.1, 0.02, 0, -0.5) * 1.2
        H += T.gauss(0, -0.5, r * 0.5) * 1.6
        G += converge(T, t, 0.0, 0.5, 14, 2, 0, -0.5, 0.45)
    g, h = orbita(T, t, circulo(14, 1.0), 5, 0.45, 7, 0.05 * rel(t, 0.2, 0.4), 0, 0.1, 0.4, 1 - rel(t, 0.8, 1))
    G, H = G + g, H + h
    for j in range(5):
        a = TAU * j / 5 + 7 * t
        x, y = 0.45 * math.cos(a), 0.1 + 0.45 * math.sin(a) * 0.4
        H += T.gauss(x, y, 0.025) * rel(t, 0.2, 0.4) * (1 - rel(t, 0.8, 1)) * 1.5
    # a cauda que chicoteia
    u = rel(t, 0.35, 0.75)
    if 0 < u < 1:
        pts = [(-0.5 + 1.0 * v, 0.3 + 0.15 * math.sin(v * 6 + u * 10)) for v in np.linspace(0, ease_out(u), 14)]
        G += T.polyline(pts, 0.03) * (1 - u) * 1.2
    return G * env, H * env


def copia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.35), 2.5)
    if abre > 0:
        w = 0.7 * abre
        papel = [(-w, -0.18), (w, -0.18), (w, 0.18), (-w, 0.18)]
        g, h = icone(T, papel, 1 - rel(t, 0.8, 1), 0.25)
        G, H = G + g, H + h
        for x in (-w, w):
            G += T.lines([(x, -0.24, x, 0.24, 1.0)], 0.04) * 1.1
    q = np.random.default_rng(15)
    segs = []
    for j in range(10):
        u = rel(t, 0.3 + 0.05 * j, 0.38 + 0.05 * j)
        if u > 0:
            x = -0.5 + 0.11 * j
            for _ in range(3):
                y0 = q.uniform(-0.12, 0.08)
                segs.append((x + q.uniform(-0.03, 0.0), y0, x + q.uniform(0.0, 0.03) * u, y0 + 0.07 * u, 1.0))
    if segs:
        G += T.lines(segs, 0.012) * (1 - rel(t, 0.8, 1)) * 1.2
        H += T.lines(segs, 0.005) * (1 - rel(t, 0.8, 1))
    G += particulas(T, t, 0.55, 1.0, 20, 6, 0, 0, 0.5, 0.4)
    return G * env, H * env


def fio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_out(rel(t, 0.0, 0.35), 2)
    if u > 0:
        pts = [(-0.9 + 1.4 * v, 0.02 * math.sin(v * 14 + t * 30)) for v in np.linspace(0, u, 30)]
        k = 1 - rel(t, 0.55, 0.75)
        G += T.polyline(pts, 0.02) * 1.6 * k
        H += T.polyline(pts, 0.007) * 1.5 * k
        H += T.gauss(pts[-1][0], 0, 0.04) * k * 1.5
    g, h = corte(T, t, 0.45, 0.75, -0.35, 1.5, 0.09, 0.1, 0, 0.12)
    G, H = G + g, H + h
    v = rel(t, 0.5, 0.95)
    if 0 < v < 1:
        q = np.random.default_rng(2)
        pts = [(0.1 + 0.6 * (j / 20 - 0.5) + 0.05 * v, -0.2 + 0.4 * (j / 20) + q.normal(0, 0.03) + 0.2 * v * v, (1 - v)) for j in range(20)]
        G += T.splats(pts, 0.02) * 1.1
    G += anel(T, t, 0.45, 0.8, 0.05, 0.5, 0.03, 0, 2.0)
    return G * env, H * env


def sangue(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = ease_out(rel(t, 0.05, 0.45), 2)
    if s > 0:
        k = 1 - rel(t, 0.7, 1)
        for j in range(8):
            a = TAU * j / 8 + 0.2 * math.sin(t * 20 + j)
            r = 0.3 * s
            g, h = icone(T, poe(CHAMA, r * math.cos(a), r * math.sin(a), 0.16 * s * (1 + 0.1 * math.sin(t * 50 + j)), a + math.pi / 2), k)
            G, H = G + g, H + h
        G += T.gauss(0, 0, 0.18 * s) * k * 0.8
        H += T.gauss(0, 0, 0.07 * s) * k * 1.3
    g, h = clarao(T, t, 0.0, 0.2, tam=0.6)
    G, H = G + g, H + h
    q = np.random.default_rng(23)
    for j in range(10):
        u = rel(t, 0.1, 0.75)
        if 0 < u < 1:
            a = q.uniform(0, TAU)
            d = 0.65 * ease_out(u) * q.uniform(0.6, 1)
            gg, hh = cheio(T, poe(GOTA, d * math.cos(a), d * math.sin(a) + 0.3 * u * u, 0.035, a + math.pi / 2), 1 - u)
            G, H = G + gg, H + hh
    return G * env, H * env


def _z(cx, cy, s):
    return [(cx - s, cy - s), (cx + s, cy - s), (cx - s, cy + s), (cx + s, cy + s)]


def zzz(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for j in range(3):
        u = rel(t, 0.0 + 0.1 * j, 0.45 + 0.1 * j)
        if 0 < u < 1:
            s = 0.08 + 0.04 * j
            G += T.polyline(_z(0.1 + 0.16 * j + 0.05 * math.sin(u * 6), -0.15 - 0.45 * u - 0.12 * j, s), 0.026) * (1 - u) * 1.6
    corre = rel(t, 0.4, 0.62)
    if 0 < corre < 1:
        q = np.random.default_rng(int(t * 40) % 5 + 1)
        x = -1 + 2.2 * ease_in(corre, 1.2)
        raio = jagged(q, -1.0, 0.05, x, 0.0, 5, 0.12)
        G += T.polyline(raio, 0.05) * 1.6 + T.gauss(x, 0, 0.12) * 1.2
        H += T.polyline(raio, 0.016) * 1.8
    g, h = clarao(T, t, 0.55, 0.8, 0.25, 0, 1.0, 1.3)
    G += raios(T, t, 0.55, 0.85, 5, 11, 0.25, 0, 0.45)
    return (G + g) * env, (H + h) * env


def juntas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    # as correntes que partem
    k = 1 - rel(t, 0.25, 0.35)
    if k > 0:
        for j in range(7):
            x = -0.6 + 0.2 * j
            G += T.ring(0.05, 0.01, x, 0.0, 1.8 if j % 2 else 0.6) * k
    g, h = clarao(T, t, 0.25, 0.45, 0, 0, 0.6)
    G, H = G + g, H + h
    q = np.random.default_rng(6)
    for j in range(4):
        u = rel(t, 0.3, 0.75)
        if 0 < u < 1:
            a = TAU * j / 4 + 0.6
            d = 0.35 * ease_out(u)
            g, h = icone(T, poe(OSSO, d * math.cos(a), d * math.sin(a), 0.16, a + u * 3), 1 - rel(u, 0.7, 1))
            G, H = G + g, H + h
    G += estouro(T, t, 0.25, 0.6, 14, 3, 0, 0, 0.6)
    for lado in (-1, 1):
        u = rel(t, 0.55, 0.9)
        if 0 < u < 1:
            ang = lado * (0.6 - 1.2 * ease_out(u))
            pts = jagged(q, 0, 0.1, 0.55 * math.sin(ang), 0.1 - 0.55 * math.cos(ang), 4, 0.15)
            G += T.polyline(pts, 0.03) * (1 - u) * 1.2
    return G * env, H * env


def bracos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for j in range(9):
        a = TAU * j / 9 + 0.3
        u = rel(t, 0.05 + 0.03 * j, 0.5 + 0.03 * j)
        if 0 < u:
            k = 1 - rel(t, 0.75, 1)
            comp = 0.75 * ease_out(u, 2.5)
            pts = []
            for v in np.linspace(0, 1, 16):
                d = comp * v
                aa = a + 0.6 * math.sin(v * 3 + t * 8 + j) * v
                pts.append((d * math.cos(aa), d * math.sin(aa)))
            G += T.polyline(pts, 0.035 * (1 - 0.3 * u)) * k * 1.1
            H += T.gauss(pts[-1][0], pts[-1][1], 0.025) * k
    g, h = aura(T, t, 0.0, 0.8, 0.22)
    return (G + g) * env, (H + h) * env


def black_flash(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    G += converge(T, t, 0.0, 0.25, 12, 3, 0, 0, 0.5, 0.015)
    k = pulso(t, 0.22, 0.75)
    if k > 0:
        q = np.random.default_rng(int(t * 30) % 6 + 2)
        for j in range(7):
            a = q.uniform(0, TAU)
            pts = jagged(q, 0, 0, 0.85 * math.cos(a), 0.85 * math.sin(a), 5, 0.35)
            G += T.polyline(pts, 0.03) * k * 1.4
            H += T.polyline(pts, 0.008) * k * 1.2
        G += T.ring(0.2, 0.06, 0, 0) * k * 1.2
    g, h = clarao(T, t, 0.22, 0.45, tam=1.1, forca=1.6)
    G += anel(T, t, 0.25, 0.7, 0.1, 0.8, 0.05)
    return (G + g) * env, (H + h) * env


def mahoraga(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3)
    if s > 0:
        k = 1 - rel(t, 0.82, 1)
        cy = -0.15
        clique = ease_out(rel(t, 0.45, 0.6), 4)
        ang0 = TAU / 8 * clique
        r = 0.38 * s
        G += T.ring(r, 0.03, 0, cy) * 1.4 * k + T.ring(0.08 * s, 0.03, 0, cy) * 1.2 * k
        segs = []
        for j in range(8):
            a = ang0 + TAU * j / 8
            segs.append((0.08 * s * math.cos(a), cy + 0.08 * s * math.sin(a), (r + 0.12 * s) * math.cos(a), cy + (r + 0.12 * s) * math.sin(a), 1.0))
            H += T.gauss((r + 0.14 * s) * math.cos(a), cy + (r + 0.14 * s) * math.sin(a), 0.03) * k
            G += T.gauss((r + 0.14 * s) * math.cos(a), cy + (r + 0.14 * s) * math.sin(a), 0.045) * k
        G += T.lines(segs, 0.022) * 1.2 * k
    g, h = clarao(T, t, 0.5, 0.7, 0, -0.15, 0.6)
    G += anel(T, t, 0.5, 0.85, 0.2, 0.8, 0.03, -0.15)
    return (G + g) * env, (H + h) * env


def boneca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 1))
    if s > 0:
        corpo = [(0, -0.35), (0.08, -0.3), (0.06, -0.2), (0.25, -0.15), (0.22, -0.08), (0.07, -0.1), (0.1, 0.12), (0.16, 0.35),
                 (0.07, 0.35), (0, 0.15), (-0.07, 0.35), (-0.16, 0.35), (-0.1, 0.12), (-0.07, -0.1), (-0.22, -0.08), (-0.25, -0.15),
                 (-0.06, -0.2), (-0.08, -0.3)]
        g, h = icone(T, poe(corpo, 0, 0, s * 1.1), 1.0, 0.4)
        G, H = G + g, H + h
        G += T.lines([(-0.08, 0.0, 0.08, 0.0, 1.0), (-0.08, 0.05, 0.08, 0.05, 1.0)], 0.008) * s
    u = ease_in(rel(t, 0.2, 0.45), 2)
    if 0 < u and t < 0.8:
        x = 0.9 - 0.9 * u
        G += T.lines([(x, -0.05, x + 0.35, -0.05, 1.0)], 0.02) * 1.4 + T.lines([(x + 0.35, -0.1, x + 0.35, 0.0, 1.0)], 0.04)
    g, h = clarao(T, t, 0.45, 0.65, 0, -0.05, 0.9, 1.5)
    G, H = G + g, H + h
    for j in range(3):
        G += anel(T, t, 0.45 + 0.1 * j, 0.85 + 0.05 * j, 0.05, 0.6, 0.025, -0.05)
    return G * env, H * env


def santuario(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    sobe = ease_out(rel(t, 0.0, 0.35), 2.2)
    if sobe > 0:
        k = (1 - rel(t, 0.8, 1)) * 0.9
        y = 0.2 - 0.75 * sobe
        telhado = [(-0.85, y + 0.05), (-0.6, y - 0.05), (-0.35, y - 0.18), (0.35, y - 0.18), (0.6, y - 0.05), (0.85, y + 0.05),
                   (0.5, y + 0.02), (-0.5, y + 0.02)]
        g, h = icone(T, telhado, k, 0.3)
        G, H = G + g, H + h
        G += T.lines([(-0.4, y + 0.02, -0.4, y + 0.5, 1.0), (0.4, y + 0.02, 0.4, y + 0.5, 1.0), (-0.15, y + 0.02, -0.15, y + 0.4, 1.0),
                      (0.15, y + 0.02, 0.15, y + 0.4, 1.0)], 0.02) * k
        # a boca aberta do santuário
        G += T.polyline([(-0.25, y + 0.12), (0, y + 0.22), (0.25, y + 0.12)], 0.015) * k
    q = np.random.default_rng(17)
    for j in range(16):
        a0 = 0.25 + 0.04 * j
        g, h = corte(T, t, a0, a0 + 0.18, q.uniform(0, math.pi), q.uniform(0.6, 1.1), 0.075, q.uniform(-0.55, 0.55), q.uniform(-0.3, 0.45))
        G, H = G + g, H + h
    return G * env, H * env


REGISTRO = [
    ("mu_portal", portal, GRANDE, "Doutor Estranho · o anel de faíscas do portal girando", False),
    ("mu_rastro_flash", rastro_flash, GRANDE, "Flash · os riscos de velocidade e o emblema do raio", False),
    ("mu_laco", laco, GRANDE, "Mulher-Maravilha · o Laço da verdade apertando", False),
    ("mu_unibeam", unibeam, GRANDE, "Homem de Ferro · o reator carregando e o Unibeam", False),
    ("mu_lider", lider, GRANDE, "Capitão América · o escudo de estrela e as setas", False),
    ("mu_fator_cura", fator_cura, GRANDE, "Deadpool · as katanas cruzadas e as cruzes de cura", False),
    ("mu_joia", joia, GRANDE, "Thanos · a Joia do Infinito encaixando", False),
    ("mu_estalo", estalo, GRANDE, "Thanos · o estalo e o pó ao vento", False),
    ("mu_potencial", potencial, GRANDE, "Gohan · a aura afiada do potencial despertado", False),
    ("mu_treino", treino, GRANDE, "Piccolo · a capa pesada caindo e o ki do aluno", False),
    ("mu_sofrimento", sofrimento, GRANDE, "Freeza · a Supernova crescendo e as esferas", False),
    ("mu_copia", copia, GRANDE, "Kakashi · o pergaminho do jutsu copiado", False),
    ("mu_fio", fio, GRANDE, "Tanjiro · o fio vermelho da abertura e o corte d'água", False),
    ("mu_sangue", sangue, GRANDE, "Nezuko · as chamas rosadas do Sangue explosivo", False),
    ("mu_zzz", zzz, GRANDE, "Zenitsu · os Z e o relâmpago da Primeira postura", False),
    ("mu_juntas", juntas, GRANDE, "Inosuke · as juntas soltando e as correntes partindo", False),
    ("mu_bracos", bracos, GRANDE, "Muzan · os braços-chicote para todo lado", False),
    ("mu_black_flash", black_flash, GRANDE, "Yuji · o Black Flash rachando o espaço", False),
    ("mu_mahoraga", mahoraga, GRANDE, "Megumi · a roda de Mahoraga girando um dente", False),
    ("mu_boneca", boneca, GRANDE, "Nobara · a boneca de palha, o prego e a martelada", False),
    ("mu_santuario", santuario, GRANDE, "Sukuna · o Santuário malevolente e os cortes", False),
]
