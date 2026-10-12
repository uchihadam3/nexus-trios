"""Rodada 12 das Mecânicas únicas ativando como habilidade: Asa Noturna, Dipper, Mabel, Yennefer, Nemesis, Zeus,
Poseidon, Atena, Ares, Apolo, Ártemis, Hermes, Afrodite, Medusa, Cronos, Hércules, Anúbis, Rá, Set, Odin, Fenrir, Hel,
Freddy Krueger, Michael Myers, Chucky e Pennywise.

- desequilibrio: os dois bastões giram e o pássaro azul abre as asas.
- diario: o diário abre, as páginas brilham e o pinheiro aparece.
- alegria: o brilho, a estrela cadente e o arco-íris da Mabel.
- caos: a magia do caos roxa em espiral e a estrela de obsidiana.
- stars: o lança-foguetes dispara, o foguete explode e os tentáculos saem.
- raio_olimpo: o raio de Zeus cai como uma lança do céu.
- abalador: o tridente bate e as ondas se espalham.
- sabedoria: os olhos da coruja acendem e os ramos de oliveira giram.
- mais_guerra: a lança e o escudo de bronze com as chamas vermelhas.
- flechas_sol: o disco do sol com os raios e a flecha dourada.
- flecha_certeira: o arco da lua, a flecha prateada e o alvo.
- mensageiro: a sandália alada, o caduceu e as linhas de velocidade.
- discordia: o pomo dourado rola e os corações se partem.
- virou_pedra: as cobras do cabelo se mexem e o olhar petrifica.
- tempo_voltou: os ponteiros giram para trás e a ampulheta vira.
- trabalhos: a clava e os doze trabalhos acendendo em volta.
- alma_pesada: a balança pesa o coração contra a pena.
- ciclo_sol: o disco de Rá gira entre o dia e a noite.
- tempestade_areia: as faixas de areia giram com os detritos.
- corvos_odin: os dois corvos voam em volta e a lança Gungnir brilha.
- gleipnir: as correntes arrebentam e o uivo sai em ondas.
- morto_vivo: as chamas verdes sobem e a mão de osso sai do chão.
- sonho: a luva de lâminas corta e as espirais do pesadelo giram.
- vitima: a faca desce e a respiração pesada embaça.
- damballa: o círculo de vodu e os raios caindo.
- come_medo: o balão vermelho sobe e as luzes mortas acendem.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .unicas_kit import (AMPULHETA, ASA, CORACAO, ESCUDO, ESPADA, FOLHA, LUA, PENA, RAIO, SETA, anel, aura, cheio, chuva,
                         circulo, clarao, converge, corte, estouro, estrela_pts, flor, icone, onda_no_chao, orbita, particulas,
                         poe, raios, surge, voa)


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def _passaro(cx, cy, s, bate, ang=0.0):
    return poe([(-1, -0.5 * bate), (-0.3, 0), (0, -0.2), (0.3, 0), (1, -0.5 * bate), (0.2, 0.25), (-0.2, 0.25)], cx, cy, s, ang)


def desequilibrio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.5, 0.6)
    for lado in (-1, 1):
        a = t * 22 * lado
        cx = lado * 0.3
        G += T.lines([(cx - 0.22 * math.cos(a), -0.05 - 0.22 * math.sin(a), cx + 0.22 * math.cos(a), -0.05 + 0.22 * math.sin(a), 1.0)], 0.035) * k * 1.2
    s = surge(t, 0.45, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g, h = cheio(T, _passaro(0, -0.1, 0.45 * s, 1.0), 1.3)
        G, H = G + g + T.gauss(0, -0.1, 0.25 * s) * 0.4, H + h * 1.5
    return G * env, H * env


def diario(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.35), 2.5)
    k = 1 - rel(t, 0.85, 1)
    for lado in (-1, 1):
        pagina = [(0, 0.2), (lado * 0.38 * abre, 0.17), (lado * 0.38 * abre, -0.25), (0, -0.22)]
        g, h = icone(T, pagina, k, 0.35)
        G, H = G + g, H + h
    if abre > 0.5:
        G += T.gauss(0, -0.02, 0.2, 0.15) * (abre - 0.5) * 1.2 * k
        segs = [(lado * 0.07, -0.15 + 0.06 * m, lado * 0.3, -0.15 + 0.06 * m, 1.0) for lado in (-1, 1) for m in range(5)]
        G += T.lines(segs, 0.006) * k
    s = surge(t, 0.4, 0.65) * k
    if s > 0:
        arvore = [(0, -0.75), (0.12 * s, -0.55), (0.06 * s, -0.55), (0.15 * s, -0.4), (-0.15 * s, -0.4), (-0.06 * s, -0.55), (-0.12 * s, -0.55)]
        g, h = cheio(T, [(x, -0.4 + (y + 0.4) * s) for x, y in arvore], 1.3)
        G, H = G + g, H + h
    G += particulas(T, t, 0.3, 1.0, 26, 3, 0, 0, 0.35, 0.4)
    return G * env, H * env


def alegria(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    arco = ease_out(rel(t, 0.1, 0.5), 2) * (1 - rel(t, 0.85, 1))
    for j in range(4):
        G += T.arc_band(0.5 - 0.06 * j, 0.025, math.pi, math.pi + math.pi * arco, 1.0, 0.0, 0, 0.35, 0.0) * (1.2 - 0.15 * j)
    u = rel(t, 0.0, 0.4)
    if 0 < u < 1:
        x, y = 0.8 - 1.2 * u, -0.7 + 0.4 * u
        g, h = cheio(T, poe(estrela_pts(5, 0.45), x, y, 0.08), 1.4)
        G, H = G + g + T.tapered([(x + 0.4, y - 0.13, x, y, 1.0)], 0.06), H + h * 2
    G += particulas(T, t, 0.2, 1.0, 50, 7, 0, 0, 0.55, 0.3, 0.012)
    s = surge(t, 0.45, 0.7) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g, h = cheio(T, poe(CORACAO, 0, 0.05, 0.15 * s), 1.3)
        G, H = G + g, H + h
    return G * env, H * env


def caos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    for j in range(3):
        pts = _espiral(0, 0, 0.05, 0.55 * ease_out(rel(t, 0.0, 0.5)), 1.5, TAU * j / 3 - t * 8)
        G += T.polyline(pts, 0.022) * k * 1.1
    s = surge(t, 0.3, 0.55) * k
    if s > 0:
        g, h = cheio(T, poe(estrela_pts(8, 0.5), 0, 0, 0.12 * s, t * 2), 1.3)
        G, H = G + g, H + h * 2
    G += raios(T, t, 0.4, 0.9, 4, 7, 0, 0, 0.55)
    g, h = clarao(T, t, 0.55, 0.75, 0, 0, 0.8)
    return (G + g) * env, (H + h) * env


def stars(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = clarao(T, t, 0.0, 0.15, -0.7, 0, 0.5)
    G, H = G + g, H + h
    u = rel(t, 0.05, 0.4)
    if 0 < u < 1:
        x = -0.7 + 1.1 * ease_in(u, 1.4)
        G += T.polys([([(x + 0.08, 0), (x - 0.04, -0.03), (x - 0.04, 0.03)], 1.0)]) * 1.4 + T.tapered([(x - 0.4, 0, x - 0.04, 0, 0.9)], 0.05)
        G += particulas(T, (t - 0.05) / 0.35 * 0.6, 0, 0.6, 14, 3, x - 0.2, 0, 0.1, 0.1, 0.02)
    g, h = clarao(T, t, 0.38, 0.6, 0.4, 0, 1.1, 1.5)
    G, H = G + g, H + h
    G += anel(T, t, 0.4, 0.8, 0.05, 0.55, 0.05, 0, 1.0) * 0 + estouro(T, t, 0.4, 0.8, 18, 3, 0.4, 0, 0.5)
    for j in range(4):
        u2 = ease_out(rel(t, 0.5 + 0.04 * j, 0.85), 2)
        if u2 > 0:
            a = -math.pi / 2 + (j - 1.5) * 0.5
            pts = [(0.4 + 0.6 * v * u2 * math.cos(a + 0.4 * math.sin(v * 5)), 0.3 + 0.7 * v * u2 * math.sin(a)) for v in np.linspace(0, 1, 12)]
            G += T.polyline(pts, 0.045) * (1 - rel(t, 0.85, 1)) * 1.1
    return G * env, H * env


def raio_olimpo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_in(rel(t, 0.0, 0.35), 2.2)
    if t < 0.5:
        y = -1.1 + 1.1 * u
        g, h = cheio(T, poe(RAIO, 0.05, y, 0.32), 1.4 * (1 - rel(t, 0.38, 0.5)))
        G, H = G + g + T.gauss(0.05, y, 0.2) * 0.8, H + h * 2
        G += T.tapered([(0.15, y - 0.8, 0.05, y - 0.2, 0.8)], 0.15) * (1 - rel(t, 0.38, 0.5))
    g, h = clarao(T, t, 0.33, 0.55, 0.05, 0.2, 1.4, 1.8)
    G, H = G + g, H + h
    G += raios(T, t, 0.35, 0.8, 6, 3, 0.05, 0.2, 0.7) + onda_no_chao(T, t, 0.35, 0.8, 0.9, 0.35)
    return G * env, H * env


def abalador(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    desce = ease_in(rel(t, 0.0, 0.3), 2.5)
    k = 1 - rel(t, 0.55, 0.7)
    if k > 0:
        y = -0.6 + 0.6 * desce
        G += T.lines([(0, y - 0.2, 0, y + 0.4, 1.0)], 0.03) * k * 1.2
        G += T.polyline([(-0.15, y - 0.35), (-0.15, y - 0.15), (0.15, y - 0.15), (0.15, y - 0.35)], 0.03) * k * 1.2
        G += T.lines([(0, y - 0.15, 0, y - 0.4, 1.0)], 0.03) * k * 1.2
        for x in (-0.15, 0, 0.15):
            g, h = cheio(T, [(x - 0.03, y - 0.33 - 0.07 * (x == 0)), (x + 0.03, y - 0.33 - 0.07 * (x == 0)), (x, y - 0.43 - 0.07 * (x == 0))], k * 1.3)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.28, 0.45, 0, 0.3, 0.9)
    G, H = G + g, H + h
    for j in range(3):
        G += anel(T, t, 0.3 + 0.12 * j, 0.85 + 0.05 * j, 0.1, 0.95, 0.04, 0.35, 2.8)
    G += particulas(T, t, 0.3, 0.9, 30, 5, 0, 0.3, 0.5, 0.4, 0.02)
    return G * env, H * env


def sabedoria(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        for lado in (-1, 1):
            G += T.ring(0.11 * s, 0.025, lado * 0.15, -0.2) * 1.3
            H += T.gauss(lado * 0.15, -0.2, 0.04 * s) * 1.8
        g, h = cheio(T, [(-0.04 * s, -0.12), (0.04 * s, -0.12), (0, -0.02)], 1.2)
        G, H = G + g, H + h
        G += T.polyline([(-0.3 * s, -0.38), (-0.15 * s, -0.33), (0, -0.36), (0.15 * s, -0.33), (0.3 * s, -0.38)], 0.02) * 1.0
    k = pulso(t, 0.3, 1.0)
    for j in range(8):
        a = TAU * j / 8 + t * 3
        g, h = icone(T, poe(FOLHA, 0.5 * math.cos(a), 0.0 + 0.5 * math.sin(a) * 0.6, 0.06, a), k, 0.5)
        G, H = G + g, H + h
    return G * env, H * env


def mais_guerra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        G += T.ring(0.28 * s, 0.04, 0.05, 0.0) * 1.2 + T.ring(0.12 * s, 0.03, 0.05, 0.0) + T.gauss(0.05, 0, 0.2 * s) * 0.3
        G += T.lines([(-0.45, 0.45, 0.4, -0.55, 1.0)], 0.03) * s * 1.1
        g, h = cheio(T, poe([(0, -1), (0.4, 0), (0, 0.5), (-0.4, 0)], 0.4, -0.55, 0.12, math.pi / 4 + 0.4), s * 1.3)
        G, H = G + g, H + h
    fogo = pulso(t, 0.3, 1.0)
    if fogo > 0:
        for j in range(9):
            x = -0.4 + 0.1 * j
            alt = (0.35 + 0.15 * math.sin(j * 1.9 + t * 20)) * fogo
            G += T.polys([(lamina(x, 0.4, x, 0.4 - alt, 0.06), 1.0)]) * 0.7
    return G * env, H * env


def flechas_sol(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        G += T.gauss(0, -0.35, 0.12 * s) * 1.3 + T.ring(0.14 * s, 0.02, 0, -0.35) * 1.2
        H += T.gauss(0, -0.35, 0.06 * s) * 1.5
        segs = []
        for j in range(12):
            a = TAU * j / 12 + t
            segs.append((0.18 * s * math.cos(a), -0.35 + 0.18 * s * math.sin(a), 0.3 * s * math.cos(a), -0.35 + 0.3 * s * math.sin(a), 1.0))
        G += T.tapered(segs, 0.04) * 1.1
    u = rel(t, 0.3, 0.6)
    if 0 < u < 1:
        x = -0.8 + 1.4 * ease_in(u, 1.3)
        G += T.lines([(x - 0.45, 0.1, x, 0.1, 1.0)], 0.03) * 1.3 + T.tapered([(x - 0.7, 0.1, x, 0.1, 0.6)], 0.06)
        g, h = cheio(T, [(x + 0.16, 0.1), (x, 0.03), (x, 0.17)], 1.4)
        G, H = G + g, H + h
    for j in range(5):
        v = rel(t, 0.55 + 0.05 * j, 0.95)
        if 0 < v < 1:
            x, y = -0.3 + 0.15 * j, 0.3 - 0.4 * v
            G += T.lines([(x - 0.035, y, x + 0.035, y, 1.0), (x, y - 0.035, x, y + 0.035, 1.0)], 0.016) * (1 - v) * 1.2
    return G * env, H * env


def flecha_certeira(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.45, 0.55))
    if s > 0:
        g, h = icone(T, poe(LUA, -0.5, 0, 0.3 * s, math.pi), 1.2, 0.5)
        G, H = G + g, H + h
        puxa = ease_out(rel(t, 0.1, 0.35), 2)
        G += T.polyline([(-0.5 + 0.3 * math.cos(2.2) * s, -0.3 * s * 0.85), (-0.5 - 0.15 * puxa, 0), (-0.5 + 0.3 * math.cos(2.2) * s, 0.3 * s * 0.85)], 0.008) * 1.1
    u = rel(t, 0.38, 0.6)
    if 0 < u < 1:
        x = -0.5 + 1.1 * ease_in(u, 1.3)
        G += T.lines([(x - 0.35, 0, x, 0, 1.0)], 0.016) * 1.3 + T.tapered([(x - 0.6, 0, x, 0, 0.6)], 0.04)
        g, h = cheio(T, [(x + 0.1, 0), (x, -0.04), (x, 0.04)], 1.4)
        G, H = G + g, H + h
    alvo = pulso(t, 0.3, 1.0)
    for r in (0.06, 0.12, 0.18):
        G += T.ring(r, 0.012, 0.6, 0) * alvo * 1.2
    g, h = clarao(T, t, 0.58, 0.75, 0.6, 0, 0.5)
    return (G + g) * env, (H + h) * env


def mensageiro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        G += T.lines([(0, -0.5, 0, 0.35, 1.0)], 0.025) * s * 1.1
        for lado in (-1, 1):
            pts = [(lado * 0.1 * math.sin(v * TAU * 1.5), -0.4 + 0.7 * v) for v in np.linspace(0, 1, 24)]
            G += T.polyline(pts, 0.016) * s
            asa = [(lado * x * 0.3, -0.5 + y * 0.25) for x, y in ASA]
            g, h = icone(T, asa, s, 0.5)
            G, H = G + g, H + h
        H += T.gauss(0, -0.52, 0.03) * s * 1.5
    q = np.random.default_rng(3)
    segs = []
    for j in range(10):
        y = q.uniform(-0.5, 0.4)
        x = ((t * 3 + q.uniform(0, 1)) % 1) * 2 - 1
        segs.append((x - 0.35, y, x, y, 0.7))
    G += T.tapered(segs, 0.02) * pulso(t, 0.1, 0.9)
    return G * env, H * env


def discordia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.5)
    if u < 1:
        x, y = -0.7 + 0.7 * u, 0.25 - 0.4 * abs(math.sin(math.pi * u * 2)) * (1 - u)
        G += T.gauss(x, y, 0.16) * 1.3 + T.ring(0.16, 0.025, x, y) * 1.1
        H += T.gauss(x - 0.03, y - 0.03, 0.03) * 1.5
        G += T.lines([(x, y - 0.1, x + 0.02, y - 0.16, 1.0)], 0.012)
        g, h = icone(T, poe(FOLHA, x + 0.06, y - 0.15, 0.04, 1.2), 1.0, 0.5)
        G, H = G + g, H + h
    for j, cx in enumerate((-0.3, 0.3)):
        parte = rel(t, 0.5, 0.9)
        s = surge(t, 0.45, 0.6) * (1 - rel(t, 0.88, 1))
        if s > 0:
            for lado in (-1, 1):
                metade = [(x, y) for x, y in CORACAO if (x <= 0.02 if lado < 0 else x >= -0.02)]
                g, h = cheio(T, poe(metade, cx + lado * 0.07 * parte, -0.35 + 0.1 * parte, 0.2 * s, lado * 0.3 * parte), 1.3)
                G, H = G + g, H + h
    return G * env, H * env


def virou_pedra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.85, 1))
    for j in range(8):
        a = -math.pi + math.pi * (j + 0.5) / 8
        pts = [(0.6 * v * s * math.cos(a) + 0.06 * math.sin(v * 10 + t * 20 + j), -0.05 + 0.6 * v * s * math.sin(a) * 0.9) for v in np.linspace(0.2, 1, 12)]
        G += T.polyline(pts, 0.04) * 1.2
        H += T.gauss(pts[-1][0], pts[-1][1], 0.018) * s
    olhar = pulso(t, 0.35, 0.8)
    if olhar > 0:
        for lado in (-1, 1):
            H += T.gauss(lado * 0.07, -0.2, 0.03, 0.015) * olhar * 2.5
        G += T.polys([([(-0.1, -0.2), (0.9, -0.45), (0.9, 0.05), (0.1, -0.2)], 1.0)], 0.03) * olhar * 0.5
    q = np.random.default_rng(7)
    racha = rel(t, 0.55, 0.85)
    if racha > 0:
        for j in range(5):
            a = q.uniform(0, TAU)
            G += T.polyline(jagged(q, 0.6, -0.2, 0.6 + 0.25 * racha * math.cos(a), -0.2 + 0.25 * racha * math.sin(a), 3, 0.3), 0.012) * (1 - rel(t, 0.88, 1)) * 1.2
    return G * env, H * env


def tempo_voltou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        r = 0.4 * s
        G += T.ring(r, 0.03, 0, 0) * 1.3
        segs = [(r * 0.85 * math.cos(TAU * j / 12), r * 0.85 * math.sin(TAU * j / 12), r * 0.97 * math.cos(TAU * j / 12), r * 0.97 * math.sin(TAU * j / 12), 1.0) for j in range(12)]
        G += T.lines(segs, 0.012)
        a = -math.pi / 2 - t * 25
        G += T.lines([(0, 0, r * 0.75 * math.cos(a), r * 0.75 * math.sin(a), 1.0), (0, 0, r * 0.45 * math.cos(a / 12), r * 0.45 * math.sin(a / 12), 1.0)], 0.025) * 1.3
        for j in range(3):
            aa = a + 0.3 * (j + 1)
            G += T.lines([(0, 0, r * 0.75 * math.cos(aa), r * 0.75 * math.sin(aa), 1.0)], 0.02) * 0.3 / (j + 1)
    vira = ease_in(rel(t, 0.4, 0.7), 2) * math.pi
    k = pulso(t, 0.35, 1.0)
    g, h = icone(T, poe(AMPULHETA, 0.0, 0.0, 0.15, vira), k * 1.1, 0.4)
    G, H = G + g, H + h
    return G * env, H * env


def trabalhos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    for j in range(12):
        a = -math.pi / 2 + TAU * j / 12
        aceso = rel(t, 0.05 + 0.04 * j, 0.1 + 0.04 * j)
        x, y = 0.48 * math.cos(a), 0.48 * math.sin(a)
        G += T.ring(0.035, 0.01, x, y) * k
        H += T.gauss(x, y, 0.02) * aceso * k * 1.5
        G += T.gauss(x, y, 0.04) * aceso * k
    s = surge(t, 0.0, 0.3) * k
    if s > 0:
        clava = [(-0.05, 0.3), (0.05, 0.3), (0.12, -0.15), (0.1, -0.3), (0, -0.35), (-0.1, -0.3), (-0.12, -0.15)]
        g, h = icone(T, poe(clava, 0, 0, s, 0.3), 1.2, 0.45)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.55, 0.75, 0, 0, 0.8)
    return (G + g) * env, (H + h) * env


def alma_pesada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    pende = 0.25 * math.sin(math.pi * rel(t, 0.3, 0.8)) * 0.6 + 0.1 * rel(t, 0.3, 0.8)
    if s > 0:
        G += T.lines([(0, -0.5, 0, 0.35, 1.0), (-0.2, 0.35, 0.2, 0.35, 1.0)], 0.025) * s * 1.1
        ang = pende
        xl, yl = -0.5 * math.cos(ang), -0.45 - 0.5 * math.sin(ang)
        xr, yr = 0.5 * math.cos(ang), -0.45 + 0.5 * math.sin(ang)
        G += T.lines([(xl, yl, xr, yr, 1.0)], 0.02) * s * 1.2
        for px, py in ((xl, yl), (xr, yr)):
            G += T.lines([(px, py, px - 0.1, py + 0.2, 1.0), (px, py, px + 0.1, py + 0.2, 1.0)], 0.008) * s
            G += T.arc_band(0.1, 0.012, 0.0, math.pi, 1.0, 0.0, px, py + 0.2, 0.0) * s
        g, h = cheio(T, poe(CORACAO, xl, yl + 0.18, 0.12), s * 1.3)
        G, H = G + g, H + h
        g, h = icone(T, poe(PENA, xr, yr + 0.12, 0.13, 0.3), s * 1.3, 0.5)
        G, H = G + g, H + h
    return G * env, H * env


def ciclo_sol(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        r = 0.3 * s
        G += T.ring(r, 0.04, 0, -0.1) * 1.3
        dia = 0.5 + 0.5 * math.cos(t * 6)
        G += T.gauss(0, -0.1, r * 0.75) * (0.3 + 0.9 * dia)
        H += T.gauss(0, -0.1, r * 0.35) * (0.4 + 1.2 * dia)
        G += T.arc_band(r * 1.25, 0.035, t * 6, t * 6 + math.pi, 1.0, 0.0, 0, -0.1, 0.0) * 1.1
        cobra = [(0.03 * math.sin(v * 8), -0.1 - r - 0.15 * v) for v in np.linspace(0, 1, 10)]
        G += T.polyline(cobra, 0.025) * 1.1
    return G * env, H * env


def tempestade_areia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.9)
    for j in range(5):
        r = 0.2 + 0.1 * j
        G += T.arc_band(r, 0.04, t * (10 - j) + j, t * (10 - j) + j + 3.5, 1.6, 0.0, 0, 0, 1.0) * k * 0.9
    q = np.random.default_rng(int(t * 12))
    pts = []
    for _ in range(60):
        a = q.uniform(0, TAU) + t * 8
        r = q.uniform(0.15, 0.7)
        pts.append((r * math.cos(a), r * math.sin(a) / 1.6, q.uniform(0.3, 1)))
    G += T.splats(pts, 0.012) * k * 1.1
    return G * env, H * env


def corvos_odin(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    for j in range(2):
        a = t * 7 + math.pi * j
        x, y = 0.5 * math.cos(a), -0.1 + 0.3 * math.sin(a)
        g, h = cheio(T, _passaro(x, y, 0.24, math.sin(t * 40 + j), 0), k * 1.2)
        G, H = G + g, H + h
        H += T.gauss(x + 0.03, y - 0.02, 0.008) * k * 2
    s = surge(t, 0.3, 0.55) * k
    if s > 0:
        G += T.lines([(0, 0.45, 0, -0.35 * s - 0.05, 1.0)], 0.025) * 1.2
        g, h = cheio(T, [(0, -0.35 * s - 0.25), (0.06, -0.35 * s - 0.08), (-0.06, -0.35 * s - 0.08)], 1.4)
        G, H = G + g, H + h * 2
        G += T.flare(0, -0.35 * s - 0.2, 0.4 * s + 0.01, 0.4, 0.01) * pulso(t, 0.5, 0.8)
    return G * env, H * env


def gleipnir(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    quebra = rel(t, 0.25, 0.5)
    q = np.random.default_rng(5)
    for lado in (-1, 1):
        for j in range(6):
            x0 = lado * (0.1 + 0.1 * j)
            if quebra <= 0:
                G += T.ring(0.04, 0.012, x0, 0.0, 1.6 if j % 2 else 0.6) * 1.2
            else:
                d = 0.5 * ease_out(quebra)
                G += T.ring(0.04, 0.012, x0 + lado * d * (j + 1) / 6, 0.4 * quebra * quebra + q.uniform(-0.1, 0.1) * quebra, 1.6 if j % 2 else 0.6) * (1 - quebra) * 1.2
    g, h = clarao(T, t, 0.22, 0.4, 0, 0, 0.8)
    G, H = G + g, H + h
    for j in range(5):
        u = rel(t, 0.35 + 0.08 * j, 0.8 + 0.06 * j)
        if 0 < u < 1:
            G += T.arc_band(0.1 + 0.8 * u, 0.04 * (1 - u) + 0.01, -2.3, -0.84, 1.0, 0.0, 0, -0.2, 0.0) * (1 - u) * 1.4
    return G * env, H * env


def morto_vivo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    fogo = pulso(t, 0.0, 0.95)
    if fogo > 0:
        for j in range(8):
            x = -0.35 + 0.1 * j
            alt = (0.4 + 0.15 * math.sin(j * 2.1 + t * 18)) * fogo
            G += T.polys([(lamina(x, 0.4, x + 0.03 * math.sin(t * 10 + j), 0.4 - alt, 0.05), 1.0)]) * 0.7
    sobe = ease_out(rel(t, 0.25, 0.6), 2) * (1 - rel(t, 0.85, 1))
    if sobe > 0:
        y = 0.4 - 0.45 * sobe
        segs = [(0, 0.4, 0, y, 1.0)]
        for j in range(4):
            a = -math.pi / 2 + (j - 1.5) * 0.35
            segs.append((0, y, 0.15 * math.cos(a) * sobe, y + 0.15 * math.sin(a) * sobe, 1.0))
            segs.append((0.15 * math.cos(a) * sobe, y + 0.15 * math.sin(a) * sobe, 0.22 * math.cos(a - 0.3) * sobe, y + 0.22 * math.sin(a - 0.3) * sobe, 1.0))
        G += T.lines(segs, 0.025) * 1.3
        H += T.lines(segs, 0.008) * 0.7
    G += particulas(T, t, 0.1, 1.0, 30, 9, 0, 0.3, 0.4, 0.7, 0.014)
    return G * env, H * env


def sonho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.95)
    for j in range(3):
        pts = _espiral(-0.4 + 0.4 * j, -0.35 + 0.1 * (j % 2), 0.01, 0.12, 2, t * 8 + j)
        G += T.polyline(pts, 0.012) * k * 0.9
    for j in range(4):
        g, h = corte(T, t, 0.3 + 0.02 * j, 0.6 + 0.02 * j, 0.9, 1.1, 0.05, -0.15 + 0.1 * j, 0.1, 0.1)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.55, 0.75, 0, 0.1, 0.6)
    return (G + g) * env, (H + h) * env


def vitima(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_in(rel(t, 0.1, 0.4), 2.5)
    k = 1 - rel(t, 0.6, 0.75)
    if k > 0:
        y = -0.8 + 0.7 * u
        faca = [(0, y + 0.5), (0.1, y), (0.1, y - 0.1), (-0.06, y - 0.1), (-0.06, y)]
        g, h = icone(T, faca, k * 1.3, 0.5)
        G, H = G + g, H + h
        G += T.lines([(0.02, y - 0.1, 0.02, y - 0.45, 1.0)], 0.08) * k
        H += T.gauss(0.03, y + 0.2, 0.02) * k * 2
    g, h = clarao(T, t, 0.38, 0.55, 0, 0.0, 0.6)
    G, H = G + g, H + h
    for j in range(2):
        v = rel(t, 0.3 + 0.3 * j, 0.7 + 0.3 * j)
        if 0 < v < 1:
            G += T.gauss(-0.3 + 0.1 * v, -0.4, 0.08 + 0.15 * v, 0.06 + 0.08 * v) * (1 - v) * 0.8
    return G * env, H * env


def damballa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.85, 1))
    G += T.ring(0.5 * s, 0.02, 0, 0.3, 3.0) * 1.2 + T.ring(0.4 * s, 0.01, 0, 0.3, 3.0) * 0.8
    for j in range(6):
        a = TAU * j / 6 + t
        G += T.lines([(0.45 * s * math.cos(a), 0.3 + 0.15 * s * math.sin(a), 0.4 * s * math.cos(a + 1), 0.3 + 0.13 * s * math.sin(a + 1), 1.0)], 0.01) * s
    r = pulso(t, 0.3, 0.8)
    if r > 0:
        q = np.random.default_rng(int(t * 30) % 5 + 1)
        for _ in range(3):
            bolt = jagged(q, q.uniform(-0.5, 0.5), -1.0, q.uniform(-0.2, 0.2), 0.25, 5, 0.25)
            G += T.polyline(bolt, 0.025) * r * 1.3
            H += T.polyline(bolt, 0.008) * r * 1.3
    g, h = clarao(T, t, 0.4, 0.6, 0, 0.25, 0.9)
    return (G + g) * env, (H + h) * env


def come_medo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    sobe = ease_in(rel(t, 0.0, 0.8), 1.2)
    k = 1 - rel(t, 0.85, 1)
    x, y = 0.25 + 0.05 * math.sin(t * 6), 0.3 - 0.9 * sobe
    balao = [(x + 0.17 * math.cos(a), y + 0.21 * math.sin(a) * (1.05 if math.sin(a) > 0 else 1)) for a in np.linspace(0, TAU, 24, endpoint=False)]
    g, h = icone(T, balao, k * 1.3, 0.55)
    G, H = G + g, H + h
    H += T.gauss(x - 0.04, y - 0.05, 0.02) * k * 1.5
    G += T.polyline([(x, y + 0.22), (x - 0.03, y + 0.4), (x + 0.02, y + 0.6)], 0.012) * k
    luzes = pulso(t, 0.3, 1.0)
    for j in range(3):
        a = TAU * j / 3 + t * 4
        lx, ly = -0.25 + 0.15 * math.cos(a), -0.1 + 0.15 * math.sin(a)
        H += T.gauss(lx, ly, 0.03) * luzes * 2
        G += T.gauss(lx, ly, 0.07) * luzes * 1.1
    sorri = surge(t, 0.4, 0.65) * k
    if sorri > 0:
        boca = [(-0.25 + 0.2 * sorri * math.cos(a), 0.2 + 0.08 * sorri * math.sin(a)) for a in np.linspace(0.1, math.pi - 0.1, 14)]
        G += T.polyline(boca, 0.02) * 1.3
    return G * env, H * env


REGISTRO = [
    ("mu_desequilibrio", desequilibrio, GRANDE, "Asa Noturna · os bastões e o pássaro azul", False),
    ("mu_diario", diario, GRANDE, "Dipper · o diário e o pinheiro", False),
    ("mu_alegria", alegria, GRANDE, "Mabel · a estrela cadente e o arco-íris", False),
    ("mu_caos", caos, GRANDE, "Yennefer · a magia do caos", False),
    ("mu_stars", stars, GRANDE, "Nemesis · o foguete e os tentáculos", False),
    ("mu_raio_olimpo", raio_olimpo, GRANDE, "Zeus · o raio do Olimpo", False),
    ("mu_abalador", abalador, GRANDE, "Poseidon · o tridente e as ondas", False),
    ("mu_sabedoria", sabedoria, GRANDE, "Atena · a coruja e os ramos de oliveira", False),
    ("mu_mais_guerra", mais_guerra, GRANDE, "Ares · a lança, o escudo e as chamas", False),
    ("mu_flechas_sol", flechas_sol, GRANDE, "Apolo · o sol e a flecha dourada", False),
    ("mu_flecha_certeira", flecha_certeira, GRANDE, "Ártemis · o arco da lua e o alvo", False),
    ("mu_mensageiro", mensageiro, GRANDE, "Hermes · o caduceu e a velocidade", False),
    ("mu_discordia", discordia, GRANDE, "Afrodite · o pomo da discórdia", False),
    ("mu_virou_pedra", virou_pedra, GRANDE, "Medusa · as cobras e o olhar de pedra", False),
    ("mu_tempo_voltou", tempo_voltou, GRANDE, "Cronos · o relógio voltando", False),
    ("mu_trabalhos", trabalhos, GRANDE, "Hércules · a clava e os doze trabalhos", False),
    ("mu_alma_pesada", alma_pesada, GRANDE, "Anúbis · a balança do coração e da pena", False),
    ("mu_ciclo_sol", ciclo_sol, GRANDE, "Rá · o disco do sol", False),
    ("mu_tempestade_areia", tempestade_areia, GRANDE, "Set · a tempestade de areia", False),
    ("mu_corvos_odin", corvos_odin, GRANDE, "Odin · os corvos e a Gungnir", False),
    ("mu_gleipnir", gleipnir, GRANDE, "Fenrir · as correntes quebrando e o uivo", False),
    ("mu_morto_vivo", morto_vivo, GRANDE, "Hel · as chamas verdes e a mão de osso", False),
    ("mu_sonho", sonho, GRANDE, "Freddy · a luva de lâminas e o pesadelo", False),
    ("mu_vitima", vitima, GRANDE, "Michael Myers · a faca e a respiração", False),
    ("mu_damballa", damballa, GRANDE, "Chucky · o vodu e os raios", False),
    ("mu_come_medo", come_medo, GRANDE, "Pennywise · o balão e as luzes mortas", False),
]
