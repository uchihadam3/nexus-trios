"""Rodada 8 das Mecânicas únicas ativando como habilidade: Pateta, Stitch, Buzz, Woody, Sr. Incrível,
Mulher-Elástica, Korra, Zuko, Toph, Iroh, Patolino, Taz, Coiote, Papa-Léguas, Marvin, Tom, Jerry, Pantera
Cor-de-Rosa, Shredder, Splinter, Krang, Casey Jones, Bebop, Esqueleto, She-Ra e Lion-O.

- desastrado: a poeira do tombo e as estrelinhas girando na cabeça.
- destruir: o escudo do rival se parte em pedaços e as garrinhas riscam.
- infinito: as asas abrem, o laser acende e o jato risca o céu.
- cordinha: a cordinha volta para o peito, o chapéu e a estrela de xerife.
- arremesso_carro: o carro voa em arco e esmaga.
- estica: o corpo estica como mola, absorve e volta.
- estado_avatar: os quatro elementos giram em volta e os olhos acendem.
- redirecionado: o raio entra, contorna o corpo e volta para quem lançou.
- terremoto: as pedras sobem do chão e as rachaduras correm.
- dragao_oeste: o sopro de fogo do Dragão do Oeste se abre em leque.
- temporada: o tiro de espingarda, a fumaça e o bico girando.
- furacao: o furacão da Tasmânia gira com os detritos.
- acme: a bigorna ACME cai do céu e levanta a poeira.
- poeira: a nuvem de poeira do Papa-Léguas e as linhas de velocidade.
- kaboom: o Modulador carrega e o KABOOM sacode a tela.
- achatado: a frigideira acerta, as estrelas saem e a onda achata.
- tombo: o queijo, a marreta e a pancada no grandão.
- diamante: o diamante rosa sai de um e voa para o outro, com as pegadas.
- garras_aco: as três garras de aço cortam e o sangue escorre.
- contra_golpe: o bastão gira, apara e devolve o golpe.
- android: o cérebro do Krang mexe os tentáculos dentro da cúpula.
- goool: o taco gira e o disco voa até o alvo.
- desprevenido: a investida com as presas e a poeira.
- nyeh: o cajado do carneiro-caveira acende roxo e solta raios.
- espada_muda: a espada vira escudo, vira laço, vira espada.
- instinto: o Olho de Thundera brilha e solta os raios.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .unicas_kit import (CHAMA, CORACAO, DIAMANTE, ESCUDO, ESPADA, GOTA, anel, aura, cheio, chuva, circulo, clarao, converge,
                         corte, estouro, estrela_pts, icone, onda_no_chao, orbita, particulas, poe, raios, surge, voa)


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def _poeira(T, t, a, b, cx, cy, n, seed, alcance=0.4, sigma=0.06):
    u = rel(t, a, b)
    if not 0 < u < 1:
        return 0.0
    q = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        ang = q.uniform(math.pi, TAU) if q.uniform() < 0.7 else q.uniform(0, math.pi)
        d = alcance * ease_out(u) * q.uniform(0.4, 1)
        pts.append((cx + d * math.cos(ang), cy + d * math.sin(ang) * 0.5, (1 - u) * q.uniform(0.4, 1)))
    return T.splats(pts, sigma) * 0.8


def desastrado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = clarao(T, t, 0.0, 0.2, 0, 0.2, 0.6)
    G, H = G + g, H + h
    G += _poeira(T, t, 0.0, 0.6, 0, 0.3, 30, 3, 0.5)
    k = pulso(t, 0.15, 1.0)
    for j in range(4):
        a = TAU * j / 4 + t * 10
        g, h = cheio(T, poe(estrela_pts(5, 0.45), 0.3 * math.cos(a), -0.45 + 0.1 * math.sin(a), 0.07, a), k * 1.3)
        G, H = G + g, H + h * 2
    G += T.ring(0.3, 0.012, 0, -0.45, 3.0) * k * 0.7
    return G * env, H * env


def destruir(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    quebra = rel(t, 0.3, 0.8)
    if quebra <= 0:
        G += T.ring(0.42, 0.04, 0, 0) * surge(t, 0.0, 0.2) * 1.2 + T.gauss(0, 0, 0.35) * 0.2
    else:
        q = np.random.default_rng(5)
        for j in range(12):
            a = TAU * j / 12 + q.uniform(-0.1, 0.1)
            d = 0.42 + 0.4 * ease_out(quebra)
            caco = poe([(-1, -0.3), (1, -0.4), (0.8, 0.4), (-0.9, 0.3)], d * math.cos(a), d * math.sin(a) + 0.3 * quebra * quebra, 0.07, a + math.pi / 2 + quebra * 4)
            g, h = icone(T, caco, 1 - quebra, 0.5)
            G, H = G + g, H + h
    for j in range(4):
        g, h = corte(T, t, 0.15 + 0.05 * j, 0.35 + 0.05 * j, 0.9 + 0.35 * (j % 2), 0.5, 0.05, -0.15 + 0.1 * j, -0.05)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.3, 0.5, 0, 0, 0.8)
    return (G + g) * env, (H + h) * env


def infinito(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 3)
    k = 1 - rel(t, 0.55, 0.7)
    if abre > 0 and k > 0:
        for lado in (-1, 1):
            asa = [(lado * 0.08, -0.15), (lado * (0.08 + 0.55 * abre), -0.05), (lado * (0.08 + 0.5 * abre), 0.05), (lado * 0.08, 0.05)]
            g, h = icone(T, asa, k * 1.2, 0.4)
            G, H = G + g, H + h
            H += T.gauss(lado * (0.08 + 0.48 * abre), -0.02, 0.02) * k * 2 * (int(t * 20) % 2)
    laser = pulso(t, 0.3, 0.55)
    if laser > 0:
        G += T.lines([(0.1, -0.15, 0.95, -0.25, 1.0)], 0.02) * laser * 1.3
        H += T.lines([(0.1, -0.15, 0.95, -0.25, 1.0)], 0.007) * laser * 1.5
    u = ease_in(rel(t, 0.5, 0.9), 1.5)
    if 0 < u < 1:
        y = 0.2 - 1.2 * u
        G += T.tapered([(0, 0.3, 0, y, 1.0)], 0.1) * 0.9 + T.gauss(0, y, 0.07)
        G += particulas(T, t, 0.5, 0.9, 20, 9, 0, 0.3, 0.15, -0.1)
    return G * env, H * env


def cordinha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    volta = ease_in(rel(t, 0.0, 0.3), 2)
    if t < 0.4:
        x0, y0 = 0.6 * (1 - volta), 0.2 * (1 - volta)
        G += T.lines([(0, 0, x0, y0, 1.0)], 0.012) * 1.2 + T.ring(0.05, 0.015, x0, y0) * 1.3
    s = surge(t, 0.25, 0.5) * (1 - rel(t, 0.85, 1))
    if s > 0:
        aba = [(-0.32 * s, -0.4), (0.32 * s, -0.4), (0.25 * s, -0.36), (-0.25 * s, -0.36)]
        copa = [(-0.15 * s, -0.4), (-0.17 * s, -0.4 - 0.2 * s), (-0.05 * s, -0.4 - 0.14 * s), (0.05 * s, -0.4 - 0.14 * s), (0.17 * s, -0.4 - 0.2 * s), (0.15 * s, -0.4)]
        g, h = icone(T, aba, 1.2, 0.45)
        G, H = G + g, H + h
        g, h = icone(T, [(x, -0.4 + (y + 0.4) * 1.0) for x, y in copa], 1.1, 0.4)
        G, H = G + g, H + h
        g, h = cheio(T, poe(estrela_pts(5, 0.45), 0, 0.1, 0.18 * s, -math.pi / 2), 1.3)
        G, H = G + g + T.gauss(0, 0.1, 0.18) * s * 0.4, H + h * 2
    G += anel(T, t, 0.4, 0.8, 0.05, 0.5, 0.03, 0.1)
    return G * env, H * env


def arremesso_carro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.5)
    if u < 1:
        x, y = -0.75 + 0.8 * u, 0.1 - 0.7 * math.sin(math.pi * u)
        ang = u * 2.5
        carro = poe([(-1, 0.15), (-0.95, -0.15), (-0.5, -0.2), (-0.3, -0.5), (0.4, -0.5), (0.6, -0.2), (1, -0.15), (1, 0.15)], x, y, 0.32, ang)
        g, h = icone(T, carro, 1.2, 0.45)
        G, H = G + g, H + h
        for wx in (-0.55, 0.55):
            cx, cy = poe([(wx, 0.18)], x, y, 0.32, ang)[0]
            G += T.ring(0.055, 0.016, cx, cy) * 1.2
    g, h = clarao(T, t, 0.48, 0.7, 0.05, 0.1, 1.1, 1.5)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.5, 0.9, 0.85, 0.3) + estouro(T, t, 0.5, 0.85, 18, 7, 0.05, 0.1, 0.7)
    return G * env, H * env


def estica(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = pulso(t, 0.0, 0.85)
    estica_ = 0.3 + 0.55 * abs(math.sin(math.pi * rel(t, 0.1, 0.8) * 1.5)) * (1 - rel(t, 0.6, 0.8))
    pts = [(-estica_ + 2 * estica_ * v, 0.12 * math.sin(v * TAU * 5)) for v in np.linspace(0, 1, 60)]
    G += T.polyline(pts, 0.03) * k * 1.3
    H += T.polyline(pts, 0.01) * k * 0.6
    for lado in (-1, 1):
        G += T.gauss(lado * estica_, 0, 0.06) * k * 1.2
    G += anel(T, t, 0.55, 0.85, 0.1, 0.55, 0.03)
    g, h = clarao(T, t, 0.25, 0.4, 0.6, 0, 0.5)
    return (G + g) * env, (H + h) * env


def estado_avatar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.85, 1)
    for j in range(4):
        a = TAU * j / 4 + t * 7
        x, y = 0.55 * s * math.cos(a), -0.05 + 0.55 * s * math.sin(a) * 0.5
        if j == 0:
            g, h = icone(T, poe(GOTA, x, y, 0.14 * s), k * 1.3, 0.5)
        elif j == 1:
            g, h = icone(T, poe(CHAMA, x, y, 0.15 * s), k * 1.3, 0.5)
        elif j == 2:
            g, h = icone(T, poe([(-1, -1), (1, -1), (1, 1), (-1, 1)], x, y, 0.09 * s, a), k * 1.3, 0.5)
        else:
            g, h = 0.0, 0.0
            G += T.polyline(_espiral(x, y, 0.01, 0.12 * s, 1.5, t * 20), 0.022) * k * 1.3
        G, H = G + g, H + h
    olhos = pulso(t, 0.25, 1.0)
    for lado in (-1, 1):
        H += T.gauss(lado * 0.06, -0.35, 0.025, 0.012) * olhos * 2.5
        G += T.gauss(lado * 0.06, -0.35, 0.06, 0.03) * olhos
    G += T.polys([([(0, -0.6), (0.04, -0.48), (-0.04, -0.48)], 1.0)]) * olhos * 1.2
    g, h = aura(T, t, 0.2, 1.0, 0.35, -0.05, 1.0)
    return (G + g) * env, (H + h) * env


def redirecionado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.0, 0.8)
    if 0 < u < 1:
        caminho = [(-1.0 + 0.7 * v, -0.05) for v in np.linspace(0, 1, 6)] + \
                  [(-0.3 + 0.3 * math.cos(math.pi - a), -0.05 + 0.3 * math.sin(math.pi - a) * -1) for a in np.linspace(0, TAU * 0.95, 14)] + \
                  [(-0.3 - 0.7 * v, -0.15 - 0.1 * v) for v in np.linspace(0, 1, 6)]
        n = len(caminho)
        ini, fim = int(max(0, u - 0.35) * n), max(2, int(u * n))
        trecho = caminho[ini:fim]
        if len(trecho) >= 2:
            q = np.random.default_rng(int(t * 30) % 5 + 1)
            torto = [(x + q.normal(0, 0.02), y + q.normal(0, 0.02)) for x, y in trecho]
            G += T.polyline(torto, 0.045) * 1.5
            H += T.polyline(torto, 0.015) * 1.6
            H += T.gauss(trecho[-1][0], trecho[-1][1], 0.04) * 1.5
    for j in range(2):
        g, h = icone(T, poe(CHAMA, -0.3 + (0.2 if j else -0.2), 0.25, 0.1), pulso(t, 0.3, 0.8), 0.6)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.75, 0.95, -0.95, -0.25, 0.6)
    return (G + g) * env, (H + h) * env


def terremoto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(13)
    for j in range(6):
        x = -0.6 + 0.24 * j + q.uniform(-0.05, 0.05)
        sobe = ease_out(rel(t, 0.1 + 0.05 * j, 0.4 + 0.05 * j), 2.5) * (1 - rel(t, 0.75, 0.95))
        if sobe > 0:
            alt = q.uniform(0.25, 0.5) * sobe
            pedra = [(x - 0.08, 0.38), (x - 0.06, 0.38 - alt * 0.8), (x, 0.38 - alt), (x + 0.07, 0.38 - alt * 0.7), (x + 0.09, 0.38)]
            g, h = icone(T, pedra, 1.1, 0.5)
            G, H = G + g, H + h
    racha = rel(t, 0.0, 0.4)
    if racha > 0:
        for j in range(5):
            a = math.pi * (0.1 + 0.8 * j / 4)
            G += T.polyline(jagged(q, 0, 0.4, 0.8 * racha * math.cos(a), 0.4 + 0.12 * racha * math.sin(a), 3, 0.3), 0.012) * (1 - rel(t, 0.85, 1)) * 1.2
    G += onda_no_chao(T, t, 0.0, 0.5, 0.9, 0.4) + onda_no_chao(T, t, 0.2, 0.7, 0.9, 0.4)
    G += particulas(T, t, 0.2, 0.9, 30, 5, 0, 0.3, 0.6, 0.4, 0.02)
    return G * env, H * env


def dragao_oeste(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = rel(t, 0.05, 0.95)
    if u > 0:
        q = np.random.default_rng(7)
        for j in range(40):
            v = (u * 1.4 + j / 40) % 1
            if v > ease_out(min(1, u * 2)):
                continue
            ang = q.uniform(-0.45, 0.45) * v
            d = -0.6 + 1.5 * v
            x, y = d, -0.05 + d * 0 + math.tan(ang) * (d + 0.6)
            g, h = icone(T, poe(CHAMA, x, y, 0.05 + 0.12 * v, math.pi / 2 + ang), (1 - v) * (1 - rel(u, 0.85, 1)) * 1.2, 0.6)
            G, H = G + g, H + h
        G += T.gauss(-0.6, -0.05, 0.08) * pulso(t, 0.05, 0.8) * 1.4
        H += T.gauss(-0.6, -0.05, 0.04) * pulso(t, 0.05, 0.8) * 1.5
    return G * env, H * env


def temporada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    g, h = clarao(T, t, 0.0, 0.2, -0.3, -0.1, 0.8, 1.3)
    G, H = G + g, H + h
    fumo = rel(t, 0.05, 0.7)
    if 0 < fumo < 1:
        G += T.ring(0.05 + 0.25 * ease_out(fumo), 0.04, -0.3, -0.1 - 0.15 * fumo) * (1 - fumo) * 1.1
        G += T.gauss(-0.3, -0.1 - 0.15 * fumo, 0.1 + 0.15 * fumo) * (1 - fumo) * 0.5
    gira = rel(t, 0.25, 0.9)
    if 0 < gira < 1:
        a = gira * 18
        bico = poe([(0, -0.08), (0.35, 0.0), (0, 0.08)], 0.2, 0.05, 1.0, a)
        g, h = icone(T, bico, (1 - rel(gira, 0.8, 1)) * 1.2, 0.5)
        G, H = G + g, H + h
        G += T.polyline(_espiral(0.2, -0.35, 0.01, 0.12, 2.5, t * 12), 0.014) * (1 - gira) * 1.2
    return G * env, H * env


def furacao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = pulso(t, 0.0, 0.9)
    for j in range(9):
        y = 0.4 - 0.1 * j
        r = 0.12 + 0.045 * j
        G += T.arc_band(r, 0.03, t * 25 + j, t * 25 + j + 4.5, 0.3, 0.0, 0.03 * math.sin(t * 15 + j * 0.6), y, 1.0) * k * 1.2
    q = np.random.default_rng(int(t * 10))
    pts = []
    for j in range(20):
        a = q.uniform(0, TAU) + t * 25
        y = q.uniform(-0.45, 0.4)
        r = 0.12 + 0.045 * (0.4 - y) / 0.1
        pts.append((r * math.cos(a), y + r * 0.3 * math.sin(a), 0.8))
    G += T.splats(pts, 0.018) * k
    G += _poeira(T, t, 0.0, 0.9, 0, 0.42, 30, 9, 0.6, 0.05)
    return G * env, H * env


def acme(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_in(rel(t, 0.0, 0.45), 2.2)
    if t < 0.75:
        y = -1.0 + 1.3 * u
        bigorna = [(-0.3, y - 0.1), (0.35, y - 0.1), (0.2, y), (0.1, y), (0.12, y + 0.12), (0.22, y + 0.18), (-0.22, y + 0.18), (-0.12, y + 0.12),
                   (-0.1, y), (-0.3, y - 0.02)]
        g, h = icone(T, bigorna, (1 - rel(t, 0.6, 0.75)) * 1.2, 0.5)
        G, H = G + g, H + h
        if u < 1:
            G += T.lines([(-0.2, y - 0.25, -0.2, y - 0.5, 1.0), (0.2, y - 0.25, 0.2, y - 0.45, 1.0)], 0.01) * 0.8
    g, h = clarao(T, t, 0.43, 0.62, 0, 0.35, 0.9, 1.3)
    G, H = G + g, H + h
    G += _poeira(T, t, 0.45, 1.0, 0, 0.35, 40, 3, 0.6) + onda_no_chao(T, t, 0.45, 0.85, 0.8, 0.38)
    return G * env, H * env


def poeira(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.3)
    if 0 < u < 1:
        x = -1.0 + 2.2 * u
        G += T.gauss(x, 0.1, 0.06) * 1.3
        for j in range(6):
            G += T.lines([(x - 0.15 - 0.4 * (1 - u), -0.1 + 0.06 * j, x - 0.15, -0.1 + 0.06 * j, 1.0)], 0.01) * 0.9
    q = np.random.default_rng(3)
    pts = []
    for j in range(60):
        x0 = q.uniform(-1.0, 1.0)
        a0 = (x0 + 1.0) / 2.2 * 0.3
        v = rel(t, a0, a0 + 0.7)
        if 0 < v < 1:
            pts.append((x0 + q.normal(0, 0.05), 0.1 - 0.3 * v * q.uniform(0.3, 1), (1 - v) * q.uniform(0.4, 1)))
    if pts:
        G += T.splats(pts, 0.07) * 0.7
    return G * env, H * env


def kaboom(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    carga = ease_in(rel(t, 0.0, 0.45), 1.5)
    if t < 0.5:
        G += T.ring(0.12, 0.025, -0.5, -0.1) * 1.2 + T.gauss(-0.5, -0.1, 0.05 + 0.07 * carga) * (0.5 + carga)
        G += T.lines([(-0.5, -0.1, -0.5 + 0.25, -0.1 - 0.15, 1.0)], 0.02)
        G += converge(T, t, 0.0, 0.45, 16, 3, -0.5, -0.1, 0.4)
    g, h = clarao(T, t, 0.45, 0.7, 0.1, 0.0, 1.4, 2.0)
    G, H = G + g, H + h
    G += anel(T, t, 0.45, 0.95, 0.1, 1.0, 0.07) + anel(T, t, 0.5, 0.98, 0.1, 0.75, 0.04)
    G += estouro(T, t, 0.45, 0.9, 26, 11, 0.1, 0.0, 0.95, 0.016)
    G += particulas(T, t, 0.5, 1.0, 40, 13, 0.1, 0, 0.6, 0.3, 0.025)
    return G * env, H * env


def achatado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_in(rel(t, 0.0, 0.3), 2)
    if t < 0.45:
        ang = -1.6 + 1.6 * u
        cx, cy = 0.4, -0.55
        px, py = cx + 0.55 * math.cos(ang + math.pi / 2), cy + 0.55 * math.sin(ang + math.pi / 2)
        G += T.lines([(cx, cy, px, py, 1.0)], 0.035) * (1 - rel(t, 0.35, 0.45))
        G += T.ring(0.13, 0.03, px + 0.1 * math.cos(ang + math.pi / 2), py + 0.1 * math.sin(ang + math.pi / 2)) * 1.2 * (1 - rel(t, 0.35, 0.45))
    g, h = clarao(T, t, 0.28, 0.48, 0, -0.1, 0.9, 1.3)
    G, H = G + g, H + h
    acha = rel(t, 0.3, 0.7)
    if 0 < acha < 1:
        G += T.gauss(0, 0.2, 0.4 * ease_out(acha), 0.04) * (1 - acha) * 1.4
    for j in range(4):
        a = TAU * j / 4 + t * 12
        k = pulso(t, 0.35, 1.0)
        g, h = cheio(T, poe(estrela_pts(5, 0.45), 0.3 * math.cos(a), -0.3 + 0.08 * math.sin(a), 0.06), k * 1.2)
        G, H = G + g, H + h * 2
    return G * env, H * env


def tombo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.4, 0.5))
    if s > 0:
        queijo = [(-0.38 * s, 0.15), (0.38 * s, 0.15), (0.38 * s, -0.08), (-0.38 * s, -0.3)]
        g, h = icone(T, [(x - 0.4, y) for x, y in queijo], 1.2, 0.5)
        G, H = G + g, H + h
        for dx, dy in ((-0.1, 0.0), (0.08, 0.04), (0.0, -0.08)):
            G += T.ring(0.04 * s, 0.012, -0.4 + dx * s * 1.5, dy * 1.5) * 1.2
    u = ease_in(rel(t, 0.35, 0.55), 2)
    k = 1 - rel(t, 0.7, 0.8)
    if u > 0 and k > 0:
        ang = -2.0 + 1.6 * u
        cx, cy = 0.15, 0.25
        hx, hy = cx + 0.6 * math.cos(ang), cy + 0.6 * math.sin(ang)
        G += T.lines([(cx, cy, hx, hy, 1.0)], 0.045) * k
        g, h = icone(T, poe([(-1, -0.6), (1, -0.6), (1, 0.6), (-1, 0.6)], hx, hy, 0.2, ang + math.pi / 2), k * 1.2, 0.5)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.53, 0.75, 0.55, -0.2, 1.1, 1.5)
    G += anel(T, t, 0.55, 0.9, 0.05, 0.6, 0.05, -0.2) + estouro(T, t, 0.55, 0.9, 16, 3, 0.55, -0.2, 0.5)
    return (G + g) * env, (H + h) * env


def diamante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.15, 0.7)
    x0, x1 = 0.5, -0.5
    x = x0 + (x1 - x0) * ease_in(u, 1.4) if u > 0 else x0
    y = -0.2 - 0.35 * math.sin(math.pi * u)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.85, 1))
    g, h = cheio(T, poe(DIAMANTE, x, y, 0.22 * s), 1.4)
    G, H = G + g + T.gauss(x, y, 0.12) * 0.6 * s, H + h * 2
    G += T.flare(x, y, 0.3 * s + 0.01, 0.3, 0.01) * s * pulso(t, 0.0, 1.0)
    for j in range(5):
        k = pulso(t, 0.2 + 0.1 * j, 0.6 + 0.08 * j)
        if k > 0:
            px = 0.45 - 0.22 * j
            py = 0.35 + (0.05 if j % 2 else -0.03)
            G += T.gauss(px, py, 0.05) * k * 1.3
            for d in range(3):
                G += T.gauss(px - 0.05 + 0.05 * d, py - 0.085, 0.02) * k * 1.3
    return G * env, H * env


def garras_aco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for j in range(3):
        g, h = corte(T, t, 0.05 + 0.04 * j, 0.35 + 0.04 * j, 1.1, 1.1, 0.07, -0.18 + 0.16 * j, 0.0, 0.1)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.3, 0.5, 0, 0, 0.7)
    G, H = G + g, H + h
    for j in range(5):
        u = rel(t, 0.4 + 0.05 * j, 0.95)
        if 0 < u < 1:
            x = -0.25 + 0.12 * j
            g2, h2 = cheio(T, poe(GOTA, x, -0.1 + 0.5 * ease_in(u, 1.5), 0.035), (1 - rel(u, 0.8, 1)) * 1.1)
            G, H = G + g2, H + h2
    return G * env, H * env


def contra_golpe(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = 1 - rel(t, 0.45, 0.55)
    if k > 0:
        a = t * 22
        G += T.lines([(-0.45 * math.cos(a), -0.45 * math.sin(a) * 0.6, 0.45 * math.cos(a), 0.45 * math.sin(a) * 0.6, 1.0)], 0.035) * k * 1.2
        for r in range(1, 4):
            aa = a - 0.25 * r
            G += T.lines([(-0.45 * math.cos(aa), -0.45 * math.sin(aa) * 0.6, 0.45 * math.cos(aa), 0.45 * math.sin(aa) * 0.6, 1.0)], 0.03) * k * 0.25 / r
    g, h = clarao(T, t, 0.35, 0.5, 0.35, -0.05, 0.7)
    G, H = G + g, H + h
    u = ease_out(rel(t, 0.5, 0.75), 2)
    if 0 < u < 1:
        G += T.tapered([(0.0, 0.0, 0.9 * u, -0.05, 1.0)], 0.08) * (1 - rel(u, 0.7, 1)) * 1.3
    g, h = clarao(T, t, 0.68, 0.88, 0.85, -0.05, 0.8, 1.2)
    return (G + g) * env, (H + h) * env


def android(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        s = s * 1.5
        G += T.ring(0.3 * s, 0.025, 0, 0.0) * 1.2 + T.gauss(0, 0, 0.25 * s) * 0.2
        cerebro = [(0.15 * s * (1 + 0.1 * math.sin(6 * a + t * 15)) * math.cos(a), -0.03 + 0.11 * s * (1 + 0.1 * math.sin(6 * a + t * 15)) * math.sin(a)) for a in np.linspace(0, TAU, 30, endpoint=False)]
        g, h = icone(T, cerebro, 1.2, 0.5)
        G, H = G + g, H + h
        G += T.polyline([(-0.1 * s, -0.05), (-0.03 * s, -0.08), (0.03 * s, -0.02), (0.1 * s, -0.06)], 0.01) * 1.0
        for j in range(3):
            pts = [((-0.06 + 0.06 * j) * s + 0.03 * math.sin(v * 8 + t * 20 + j), 0.08 + 0.15 * v * s) for v in np.linspace(0, 1, 8)]
            G += T.polyline(pts, 0.015) * 1.1
        olhos = (int(t * 12) % 2)
        for lado in (-1, 1):
            H += T.gauss(lado * 0.05 * s, -0.03, 0.012) * olhos * 2
    return G * env, H * env


def goool(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.35, 0.45)
    if u > 0 and k > 0:
        ang = -2.4 + 2.0 * u
        cx, cy = -0.4, -0.3
        px, py = cx + 0.55 * math.cos(ang), cy + 0.55 * math.sin(ang)
        G += T.lines([(cx, cy, px, py, 1.0)], 0.03) * k
        G += T.lines([(px, py, px + 0.15 * math.cos(ang + 1.3), py + 0.15 * math.sin(ang + 1.3), 1.0)], 0.04) * k
    v = rel(t, 0.3, 0.55)
    if 0 < v < 1:
        x = -0.4 + 1.2 * ease_in(v, 1.3)
        G += T.gauss(x, 0.1, 0.05, 0.025) * 1.5 + T.tapered([(x - 0.4, 0.1, x, 0.1, 1.0)], 0.04)
    g, h = clarao(T, t, 0.52, 0.72, 0.6, 0.1, 0.8, 1.3)
    G += anel(T, t, 0.53, 0.85, 0.05, 0.5, 0.04, 0.1) + estouro(T, t, 0.53, 0.85, 14, 3, 0.6, 0.1, 0.4)
    return (G + g) * env, (H + h) * env


def desprevenido(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_in(rel(t, 0.0, 0.4), 1.6)
    if t < 0.5:
        x = -0.9 + 1.0 * u
        for lado in (-1, 1):
            presa = [(x + 0.25 * v, lado * (0.05 + 0.15 * v - 0.12 * v * v)) for v in np.linspace(0, 1, 10)]
            G += T.polyline(presa, 0.03 * (1 - 0.0)) * 1.3
        G += _poeira(T, t, 0.0, 0.5, x - 0.1, 0.25, 20, 5, 0.3, 0.05)
    g, h = clarao(T, t, 0.38, 0.6, 0.25, 0.0, 1.0, 1.4)
    G += anel(T, t, 0.4, 0.8, 0.05, 0.65, 0.05) + estouro(T, t, 0.4, 0.8, 16, 9, 0.25, 0.0, 0.6)
    return (G + g) * env, (H + h) * env


def nyeh(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        G += T.lines([(0, -0.1, 0, 0.6, 1.0)], 0.03) * s
        cranio = [(0.14 * s * math.cos(a), -0.3 + 0.13 * s * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)]
        g, h = icone(T, cranio, 1.2, 0.4)
        G, H = G + g, H + h
        for lado in (-1, 1):
            chifre = [(lado * (0.1 + 0.15 * v) * s, -0.3 + (-0.1 + 0.25 * v * v) * s - 0.05 * math.sin(v * 3) * s) for v in np.linspace(0, 1, 10)]
            G += T.polyline(chifre, 0.03 * s) * 1.3
            H += T.gauss(lado * 0.05 * s, -0.3, 0.02) * 2 * s
    G += raios(T, t, 0.25, 0.9, 4, 7, 0, -0.3, 0.55)
    g, h = aura(T, t, 0.1, 1.0, 0.3, -0.3)
    return (G + g) * env, (H + h) * env


def espada_muda(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    fases = [(0.0, 0.3), (0.3, 0.6), (0.6, 0.95)]
    for j, (a, b) in enumerate(fases):
        k = pulso(t, a, b)
        if k <= 0:
            continue
        if j == 0:
            g, h = icone(T, poe(ESPADA, 0, 0, 0.45 * k), k * 1.2, 0.45)
        elif j == 1:
            g, h = icone(T, poe(ESCUDO, 0, 0, 0.35 * k), k * 1.2, 0.4)
        else:
            G += T.ring(0.3 * k, 0.03, 0, 0) * k * 1.3
            G += T.polyline([(-0.3 * k, 0), (-0.8, 0.2)], 0.02) * k
            g, h = 0.0, 0.0
        G, H = G + g, H + h
        G += T.gauss(0, 0, 0.3) * k * 0.3
    for j in range(2):
        g, h = cheio(T, poe(estrela_pts(4, 0.3), 0.3, -0.4, 0.12 * pulso(t, 0.28 + 0.3 * j, 0.36 + 0.3 * j)), 1.5)
        G, H = G + g, H + h * 2
    return G * env, H * env


def instinto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        G += T.ring(0.28 * s, 0.035, 0, -0.15, 1.5) * 1.3 + T.gauss(0, -0.15, 0.22 * s, 0.15 * s) * 0.5
        gato = [(-0.15 * s, -0.08), (-0.18 * s, -0.25), (-0.08 * s, -0.17), (0.08 * s, -0.17), (0.18 * s, -0.25), (0.15 * s, -0.08), (0, 0.0)]
        g, h = icone(T, gato, 1.3, 0.6)
        G, H = G + g, H + h
    raios_ = pulso(t, 0.35, 0.95)
    if raios_ > 0:
        segs = [(0, -0.15, 0.95 * math.cos(-math.pi / 2 + (j - 3) * 0.3), -0.15 + 0.95 * math.sin(-math.pi / 2 + (j - 3) * 0.3), 1.0) for j in range(7)]
        G += T.tapered([(x2, y2, x1, y1, w) for x1, y1, x2, y2, w in segs], 0.08) * raios_ * 0.8
    return G * env, H * env


REGISTRO = [
    ("mu_desastrado", desastrado, GRANDE, "Pateta · o tombo e as estrelinhas", False),
    ("mu_destruir", destruir, GRANDE, "Stitch · o escudo partido e as garrinhas", False),
    ("mu_infinito", infinito, GRANDE, "Buzz · as asas, o laser e o voo", False),
    ("mu_cordinha", cordinha, GRANDE, "Woody · a cordinha, o chapéu e a estrela", False),
    ("mu_arremesso_carro", arremesso_carro, GRANDE, "Sr. Incrível · o carro arremessado", False),
    ("mu_estica", estica, GRANDE, "Mulher-Elástica · o corpo que estica", False),
    ("mu_estado_avatar", estado_avatar, GRANDE, "Korra · os quatro elementos do Estado Avatar", False),
    ("mu_redirecionado", redirecionado, GRANDE, "Zuko · o raio redirecionado", False),
    ("mu_terremoto", terremoto, GRANDE, "Toph · as pedras e o terremoto", False),
    ("mu_dragao_oeste", dragao_oeste, GRANDE, "Iroh · o sopro do Dragão do Oeste", False),
    ("mu_temporada", temporada, GRANDE, "Patolino · o tiro e o bico girando", False),
    ("mu_furacao", furacao, GRANDE, "Taz · o furacão", False),
    ("mu_acme", acme, GRANDE, "Coiote · a bigorna ACME", False),
    ("mu_poeira", poeira, GRANDE, "Papa-Léguas · a poeira", False),
    ("mu_kaboom", kaboom, GRANDE, "Marvin · o KABOOM", False),
    ("mu_achatado", achatado, GRANDE, "Tom · a frigideira e o achatado", False),
    ("mu_tombo", tombo, GRANDE, "Jerry · o queijo e a marreta", False),
    ("mu_diamante", diamante, GRANDE, "Pantera Cor-de-Rosa · o diamante roubado", False),
    ("mu_garras_aco", garras_aco, GRANDE, "Shredder · as garras de aço", False),
    ("mu_contra_golpe", contra_golpe, GRANDE, "Splinter · o contra-golpe", False),
    ("mu_android", android, GRANDE, "Krang · o cérebro na cúpula", False),
    ("mu_goool", goool, GRANDE, "Casey Jones · o taco e o disco", False),
    ("mu_desprevenido", desprevenido, GRANDE, "Bebop · a investida", False),
    ("mu_nyeh", nyeh, GRANDE, "Esqueleto · o cajado do carneiro", False),
    ("mu_espada_muda", espada_muda, GRANDE, "She-Ra · a espada que muda", False),
    ("mu_instinto", instinto, GRANDE, "Lion-O · o Olho de Thundera", False),
]
