"""Ataques básicos com animação própria, lote n (personagens novos).

Asa Noturna, Dipper, Mabel, Yennefer, Nêmesis, Zeus, Poseidon, Atena, Ares, Apolo, Ártemis, Hermes, Afrodite,
Medusa e Cronos: os dois bastões elétricos, a lanternada com o cone de luz, o gancho da Mabel com o brilho, a
faísca arcana girando, o soco do Nêmesis com os tentáculos, o raio de Zeus em forma de raio, os três jatos
do tridente, o escudo de Atena, a lança de Ares com a fúria vermelha, o raio do sol de Apolo, a flecha de
prata com a lua, o chute de sandália alada, o beijo soprado com os corações, o bote da serpente que
petrifica e o relógio que anda para trás.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .basicos_a import _PUNHO, _move, _punho
from .basicos_k import _borda, _contorno, _estouro, _folha, _gira, _gotas
from .basicos_l import _estrelinhas, _sapato
from .basicos_m import _flecha


def _coracao(cx, cy, r, n=28):
    pts = []
    for k in range(n):
        a = TAU * k / n
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x * r / 17, cy + y * r / 17))
    return pts


# ================================================================== Asa Noturna
def bastoes_eletricos(T, t, rng):
    """Os bastões do Asa Noturna: os dois bastões curtos batem alternados (um de cima, um de baixo), cada um com a
    carga elétrica azul estalando no acerto."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    for k, (t0, lado) in enumerate(((0.0, -1), (0.18, 1))):
        u = ease_out(rel(t, t0, t0 + 0.2), 2.5)
        if u <= 0 or t > t0 + 0.4:
            continue
        ang = lado * (1.6 - 1.5 * u)
        px, py = -0.4, 0.3 * lado
        tip = (px + 0.45 * math.cos(ang - lado * 0.0), py - lado * 0.45 * math.sin(abs(ang)))
        tip = (px + 0.45 * math.cos(-lado * (1.6 - 1.5 * u)), py + 0.45 * math.sin(-lado * (1.6 - 1.5 * u)))
        some = 1 - rel(t, t0 + 0.25, t0 + 0.4)
        G += T.lines([(px, py, tip[0], tip[1], 1.0)], 0.035) * 1.2 * some
        G += T.arc_band(0.45, 0.03, -lado * 1.6, -lado * (1.6 - 1.5 * u), cx=px, cy=py, taper=0.7) * 0.6 * some
        H += T.gauss(tip[0], tip[1], 0.03) * 1.2 * some
        b = rel(t, t0 + 0.18, t0 + 0.4)
        if 0 < b < 1:
            q = np.random.default_rng(int(t * 40) % 7 + k)
            for j in range(4):
                a = TAU * j / 4 + t * 8
                G += T.polyline(jagged(q, 0.0, 0.0, 0.3 * math.cos(a), 0.3 * math.sin(a), 4, 0.45), 0.01) * (1 - b) * 1.3
            H += T.flare(0, 0, 0.3 * (1 - b) + 0.01, 0.4 * k, 0.012) * (1 - b) * 1.4
    return G * env, H * env


# ================================================================== Dipper
def lanternada(T, t, rng):
    """A lanternada do Dipper: o facho da lanterna varre a arena (o cone de luz), acha o rival e ele leva a pancada
    com a própria lanterna (o "tonc" e as estrelinhas)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    varre = rel(t, 0.0, 0.3)
    if t < 0.5:
        ang = -0.6 + 0.6 * ease_out(varre, 2)
        ox, oy = -0.85, 0.15
        cone = [(ox, oy), (ox + 1.4 * math.cos(ang - 0.2), oy + 1.4 * math.sin(ang - 0.2)), (ox + 1.4 * math.cos(ang + 0.2), oy + 1.4 * math.sin(ang + 0.2))]
        C = T.polys([(cone, 1.0)])
        G += T.blur(C, 0.02) * 0.35 * (1 - rel(t, 0.35, 0.5))
        H += T.gauss(ox, oy, 0.04) * 1.2 * (1 - rel(t, 0.35, 0.5))
        G += T.lines(_contorno(_gira([(-0.12, -0.04), (0.04, -0.04), (0.08, -0.07), (0.08, 0.07), (0.04, 0.04), (-0.12, 0.04)], ang, ox - 0.05, oy)), 0.012)
    g, h = _estouro(T, t, 0.35, 0.62, 0, -0.05, 0.3, 8, 4)
    G += g
    H += h
    G += _estrelinhas(T, t, 0.38, 0.55, 0, -0.3, 4, 0.3, 6)
    return G * env, H * env


# ================================================================== Mabel
def gancho_de_mabel(T, t, rng):
    """O gancho da Mabel: a arma de gancho dispara a garra de três pontas na corda (o fio ondulando), engancha no
    rival e puxa com um tranco, soltando o glitter brilhante."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vai = ease_out(rel(t, 0.0, 0.25), 2)
    puxa = ease_in(rel(t, 0.35, 0.55), 2)
    if vai > 0 and t < 0.7:
        x = -0.85 + 0.85 * vai - 0.25 * puxa
        pts = [(-0.85 + (x + 0.85) * u, 0.06 * math.sin(TAU * u * 3 + t * 30) * (1 - vai * 0.8)) for u in np.linspace(0, 1, 30)]
        G += T.polyline(pts, 0.01) * 1.1 * (1 - rel(t, 0.55, 0.7))
        garra = []
        for a in (-0.8, 0.0, 0.8):
            garra.append((x, 0, x + 0.1 * math.cos(a), 0.1 * math.sin(a), 1.0))
            garra.append((x + 0.1 * math.cos(a), 0.1 * math.sin(a), x + 0.07 * math.cos(a) - 0.03, 0.1 * math.sin(a) + 0.04 * (1 if a >= 0 else -1), 1.0))
        G += T.lines(garra, 0.016) * 1.3 * (1 - rel(t, 0.55, 0.7))
    g, h = _estouro(T, t, 0.25, 0.5, 0, 0, 0.25, 7, 8, 0.015)
    G += g * 0.8
    H += h * 0.8
    brilho = rel(t, 0.3, 0.95)
    if 0 < brilho < 1:
        q = np.random.default_rng(12)
        shapes = []
        for _ in range(14):
            a = q.uniform(0, TAU)
            d = 0.5 * ease_out(brilho, 2) * q.uniform(0.3, 1)
            shapes.append((estrela(d * math.cos(a), d * math.sin(a) + 0.2 * brilho, 0.03, brilho * 6, 4, 0.35), 1 - brilho))
        G += T.polys(shapes) * 1.2
    return G * env, H * env


# ================================================================== Yennefer
def faisca_arcana(T, t, rng):
    """A faísca arcana da Yennefer: a centelha violeta se forma girando na ponta dos dedos (dois fios enrolados),
    dispara rodopiando e estoura no rival numa estrela de oito pontas."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    voa = ease_in(rel(t, 0.12, 0.35), 1.6)
    x = -0.75 + 0.75 * voa
    if t < 0.4:
        pts = []
        for k in range(2):
            for j in range(16):
                a = TAU * (j / 16) + t * 30 + k * math.pi
                pts.append((x + 0.08 * math.cos(a) - 0.12 * j / 16, 0.08 * math.sin(a) * (1 - j / 16), 1 - j / 16))
        G += T.splats(pts, 0.014) * 1.3
        H += T.gauss(x, 0, 0.03) * 1.5
    bum = rel(t, 0.35, 0.75)
    if 0 < bum < 1:
        E = T.polys([(estrela(0, 0, 0.1 + 0.3 * ease_out(bum, 3), bum * 2, 8, 0.35), 1.0)])
        G += _borda(T, E, 0.008) * (1 - bum) * 1.5
        H += T.gauss(0, 0, 0.06) * (1 - bum) ** 2 * 1.6
        G += T.ring(0.08 + 0.3 * ease_out(bum, 2), 0.02, 0, 0) * (1 - bum)
    return G * env, H * env


# ================================================================== Nêmesis
def soco_do_nemesis(T, t, rng):
    """O soco do Nêmesis: o punho enorme vem pesado, com os tentáculos se contorcendo em volta do braço, e esmaga o
    rival num baque grande."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vai = ease_in(rel(t, 0.0, 0.3), 2)
    if t < 0.5:
        x = -0.85 + 0.75 * vai
        P, nos = _punho(T, x, 0.0, 2.4)
        G += P * 0.6 + _borda(T, P, 0.008) * 1.3
        H += nos * 0.4
        for k in range(4):
            pts = []
            for j in range(16):
                u = j / 15
                pts.append((x - 0.25 - 0.5 * u, (k - 1.5) * 0.08 + 0.08 * math.sin(TAU * u * 1.5 + t * 25 + k)))
            G += T.polyline(pts, 0.016) * 1.0
    g, h = _estouro(T, t, 0.3, 0.65, 0.05, 0, 0.45, 12, 5, 0.026)
    G += g * 1.1
    H += h
    return G * env, H * env


# ================================================================== Zeus
def _raio_de_zeus(cx, cy, s, ang):
    pts = [(-0.35, -0.03), (0.0, -0.06), (-0.05, -0.14), (0.38, 0.03), (0.02, 0.06), (0.07, 0.14)]
    return _gira([(x * s, y * s) for x, y in pts], ang, cx, cy)


def faisca_de_zeus(T, t, rng):
    """A faísca de Zeus: o raio de ouro em forma de raio (o desenho clássico, em zigue-zague) é arremessado da
    esquerda, crava no rival e solta os estalos elétricos em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    voa = ease_in(rel(t, 0.0, 0.25), 1.6)
    if t < 0.4:
        x = -0.8 + 0.8 * voa
        R = T.polys([(_raio_de_zeus(x, -0.05 * (1 - voa), 0.8, 0.15 * (1 - voa)), 1.0)])
        G += R * 1.0 + _borda(T, R, 0.006) * 1.0 + T.blur(R, 0.02) * 0.5
        H += R * 0.5
    g, h = _estouro(T, t, 0.25, 0.55, 0.1, 0, 0.35, 10, 9)
    G += g
    H += h
    choque = pulso(t, 0.28, 0.75)
    if choque > 0:
        q = np.random.default_rng(int(t * 40) % 6 + 10)
        for k in range(5):
            a = TAU * k / 5 + 0.4
            G += T.polyline(jagged(q, 0.1 + 0.1 * math.cos(a), 0.1 * math.sin(a), 0.1 + 0.45 * math.cos(a), 0.45 * math.sin(a), 5, 0.4), 0.011) * choque * 1.2
    return G * env, H * env


# ================================================================== Poseidon
def jato_do_tridente(T, t, rng):
    """O jato do tridente: o tridente aponta (o cabo e as três pontas) e de cada ponta sai um jato de água que se
    junta no rival e espirra."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    tx, ty = -0.6, 0.0
    if t < 0.6:
        some = 1 - rel(t, 0.45, 0.6)
        segs = [(tx - 0.4, ty, tx, ty, 1.0), (tx, ty - 0.12, tx, ty + 0.12, 1.0)]
        for dy in (-0.12, 0.0, 0.12):
            segs.append((tx, ty + dy, tx + 0.15, ty + dy, 1.0))
        G += T.lines(segs, 0.022) * 1.2 * some
    jato = ease_out(rel(t, 0.1, 0.3), 2)
    some = 1 - rel(t, 0.4, 0.58)
    if jato > 0 and some > 0:
        for dy in (-0.12, 0.0, 0.12):
            pts = [(tx + 0.15 + (0.6 - 0.15) * u * jato / max(jato, 1e-3) * jato, ty + dy * (1 - u) + 0.02 * math.sin(u * 20 + t * 30)) for u in np.linspace(0, 1, 20)]
            W = T.polyline(pts, 0.03)
            G += (W * 0.7 + _borda(T, W, 0.006) * 1.0) * some
    G += _gotas(T, t, 0.3, 0.5, 0.0, 0.0, 20, 0.55, 15, 0, TAU, 0.018, 0.35) * 1.3
    g, h = _estouro(T, t, 0.3, 0.55, 0, 0, 0.25, 6, 3, 0.014)
    G += g * 0.6
    H += h * 0.6
    return G * env, H * env


# ================================================================== Atena
def escudada_de_atena(T, t, rng):
    """A escudada de Atena: o escudo redondo (a borda, o anel e o umbo no meio) avança e bate de frente no rival,
    soltando a onda e o brilho na borda."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.28), 2)
    if t < 0.5:
        x = -0.75 + 0.6 * vem
        some = 1 - rel(t, 0.38, 0.5)
        E = T.ring(0.3, 0.025, x, 0, squash=1.0) * 1.2 + T.ring(0.2, 0.012, x, 0) * 0.8 + T.gauss(x, 0, 0.04) * 1.0
        segs = []
        for k in range(8):
            a = TAU * k / 8
            segs.append((x + 0.06 * math.cos(a), 0.06 * math.sin(a), x + 0.2 * math.cos(a), 0.2 * math.sin(a), 0.6))
        G += (E + T.lines(segs, 0.008)) * some
        H += T.arc_band(0.3, 0.02, -2.4, -1.4, cx=x, cy=0, taper=0.0) * some
    onda = rel(t, 0.28, 0.75)
    if 0 < onda < 1:
        G += T.ring(0.15 + 0.6 * ease_out(onda, 2), 0.04, 0.05, 0) * (1 - onda) * 1.3
        H += T.gauss(0.05, 0, 0.1) * (1 - onda) ** 2 * 1.6
    return G * env, H * env


# ================================================================== Ares
def lanca_de_ares(T, t, rng):
    """A lança de Ares: a fúria vermelha acende em chamas em volta da lança, e a estocada atravessa reta e longa no
    rival, com o rastro de guerra."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vai = ease_in(rel(t, 0.08, 0.28), 2.5)
    if t < 0.55:
        tip = -0.5 + 0.65 * vai
        some = 1 - rel(t, 0.4, 0.55)
        G += T.lines([(tip - 0.9, 0.0, tip - 0.15, 0.0, 1.0)], 0.022) * 1.1 * some
        P = T.polys([(lamina(tip - 0.2, 0.0, tip, 0.0, 0.05), 1.0)])
        G += (P * 1.3 + _borda(T, P, 0.005)) * some
        q = np.random.default_rng(int(t * 40) % 9)
        chamas = [(lamina(tip - 0.8 + 0.12 * k, q.uniform(-0.04, 0.04), tip - 0.95 + 0.12 * k, -0.12 - 0.08 * q.uniform(), 0.03), 1.0) for k in range(6)]
        G += T.polys(chamas) * 0.8 * some * pulso(t, 0.0, 0.5)
    g, h = _estouro(T, t, 0.28, 0.6, 0.15, 0, 0.35, 10, 11)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Apolo
def raio_de_apolo(T, t, rng):
    """O raio de luz de Apolo: o disco do sol se acende (com os raios em volta girando), e um feixe dourado sai dele
    reto até o rival, que se ilumina num clarão."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    sol = pulso(t, 0.0, 0.6)
    sx, sy = -0.7, -0.35
    if sol > 0:
        G += T.gauss(sx, sy, 0.08) * sol * 1.2 + T.ring(0.1, 0.012, sx, sy) * sol
        raios = [(sx + 0.13 * math.cos(TAU * k / 12 + t * 3), sy + 0.13 * math.sin(TAU * k / 12 + t * 3),
                  sx + 0.22 * math.cos(TAU * k / 12 + t * 3), sy + 0.22 * math.sin(TAU * k / 12 + t * 3), 1.0) for k in range(12)]
        G += T.tapered(raios, 0.016) * sol
        H += T.gauss(sx, sy, 0.04) * sol * 1.3
    feixe = rel(t, 0.15, 0.55)
    if 0 < feixe < 1:
        vai = min(1, feixe * 4)
        x1, y1 = sx + (0.0 - sx) * vai, sy + (0.0 - sy) * vai
        R = T.lines([(sx, sy, x1, y1, 1.0)], 0.035)
        G += (T.blur(R, 0.015) * 0.9 + R * 0.6) * (1 - feixe * 0.6)
        H += T.lines([(sx, sy, x1, y1, 1.0)], 0.01) * (1 - feixe * 0.6)
    g, h = _estouro(T, t, 0.25, 0.65, 0, 0, 0.35, 12, 13)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Ártemis
def flecha_lunar(T, t, rng):
    """A flecha de prata de Ártemis: a lua crescente brilha atrás do arco, a flecha prateada voa deixando o rastro de
    luar (os pontinhos frios) e crava no rival com a meia-lua acendendo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    lua = pulso(t, 0.0, 0.5)
    if lua > 0:
        L = T.arc_band(0.18, 0.06, 1.8, 1.8 + 3.0, cx=-0.75, cy=-0.1, crescente=True)
        G += (L * 0.9 + T.blur(L, 0.02) * 0.4) * lua
    voa = ease_in(rel(t, 0.05, 0.28), 1.3)
    if t < 0.55:
        x = -0.75 + 0.8 * voa
        G += T.lines(_flecha(x, 0.0, 0.0, 0.45), 0.012) * 1.3 * (1 - rel(t, 0.42, 0.55))
        pts = [(-0.75 + (x + 0.75) * u, 0.02 * math.sin(u * 25), 0.6 * u) for u in np.linspace(0, 1, 14)]
        G += T.splats(pts, 0.014) * (1 - rel(t, 0.35, 0.55))
    marca = pulso(t, 0.28, 0.9)
    if marca > 0:
        G += T.arc_band(0.14, 0.04, 1.8, 4.8, cx=0.05, cy=0.0, crescente=True) * marca * 1.2
    g, h = _estouro(T, t, 0.28, 0.55, 0.05, 0, 0.25, 8, 17, 0.014)
    G += g * 0.8
    H += h * 0.8
    return G * env, H * env


# ================================================================== Hermes
def chute_alado(T, t, rng):
    """O chute veloz de Hermes: a sandália com as asinhas batendo vem num risco de velocidade e acerta o rival, com as
    penas soltas no ar."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.22), 1.5)
    if t < 0.45:
        x = -0.9 + 0.82 * vem
        S = T.polys([(_sapato(x, 0.0, 2.0, 0.0), 1.0)])
        G += S * 0.7 + _borda(T, S, 0.006) * 1.2
        bate = 0.5 + 0.5 * math.sin(t * 70)
        asa = [(x - 0.12, -0.06), (x - 0.25, -0.16 - 0.08 * bate), (x - 0.3, -0.1), (x - 0.22, -0.06)]
        G += T.polys([(asa, 1.0)]) * 1.0 + T.lines(_contorno(asa), 0.008) * 0.8
        G += T.tapered([(x - 0.6, 0.02 * k, x - 0.15, 0.02 * k, 0.7) for k in (-3, 0, 3)], 0.016)
    g, h = _estouro(T, t, 0.22, 0.5, 0.1, 0, 0.3, 9, 19)
    G += g
    H += h
    penas = rel(t, 0.25, 0.95)
    if 0 < penas < 1:
        q = np.random.default_rng(21)
        shapes = [(_folha(q.uniform(-0.3, 0.3), -0.2 + 0.5 * penas + q.uniform(-0.1, 0.1), 0.04, penas * 3 + q.uniform(0, 6)), 1 - penas) for _ in range(5)]
        G += T.polys(shapes) * 0.9
    return G * env, H * env


# ================================================================== Afrodite
def beijo_soprado(T, t, rng):
    """O beijo soprado de Afrodite: os lábios aparecem e sopram, e os coraçõezinhos flutuam ondulando até o rival,
    onde estouram em brilhos (o encanto)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    labios = pulso(t, 0.0, 0.35)
    if labios > 0:
        cima = [(-0.75 + 0.1 * math.cos(a), -0.1 + 0.04 * math.sin(a) - 0.02 * abs(math.cos(a * 2))) for a in np.linspace(math.pi, TAU, 12)]
        baixo = [(-0.75 + 0.1 * math.cos(a), -0.1 + 0.05 * math.sin(a)) for a in np.linspace(0, math.pi, 12)]
        G += (T.polyline(cima, 0.014) + T.polyline(baixo, 0.014)) * labios * 1.2
    for k in range(4):
        t0 = 0.08 + 0.06 * k
        u = rel(t, t0, t0 + 0.4)
        if 0 < u < 1:
            x = -0.65 + 0.65 * u
            y = -0.1 * (1 - u) + 0.08 * math.sin(u * 9 + k)
            C = T.polys([(_coracao(x, y, 0.06 + 0.02 * (k % 2)), 1.0)])
            G += C * 0.6 + _borda(T, C, 0.006) * 1.2
    G += _estrelinhas(T, t, 0.45, 0.5, 0, 0, 7, 0.35, 23)
    H += T.gauss(0, 0, 0.08) * pulso(t, 0.45, 0.75) * 1.2
    return G * env, H * env


# ================================================================== Medusa
def bote_da_medusa(T, t, rng):
    """O bote da Medusa: a serpente do cabelo dá o bote serpenteando (o corpo em S e a cabeça com as presas), morde o
    rival e a pedra começa a tomar conta dele (as rachaduras cinzas que se espalham)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    bote = ease_out(rel(t, 0.0, 0.25), 2.5)
    if bote > 0 and t < 0.55:
        some = 1 - rel(t, 0.4, 0.55)
        pts = []
        for j in range(30):
            u = j / 29 * bote
            pts.append((-0.85 + 0.8 * u, 0.15 * math.sin(TAU * u * 1.5) * (1 - u)))
        G += T.polyline(pts, 0.035) * 0.6 * some + _borda(T, T.polyline(pts, 0.035), 0.006) * 1.0 * some
        hx, hy = pts[-1]
        cab = [(hx + 0.12, hy), (hx + 0.02, hy - 0.06), (hx - 0.06, hy - 0.04), (hx - 0.06, hy + 0.04), (hx + 0.02, hy + 0.06)]
        G += T.polys([(cab, 1.0)]) * 1.1 * some
        G += T.lines([(hx + 0.06, hy - 0.04, hx + 0.08, hy + 0.02, 1.0), (hx + 0.06, hy + 0.04, hx + 0.08, hy - 0.02, 1.0)], 0.008) * some
    pedra = rel(t, 0.3, 1.0)
    if pedra > 0:
        q = np.random.default_rng(29)
        for k in range(8):
            a = TAU * k / 8 + 0.2
            G += T.polyline(jagged(q, 0.0, 0.0, 0.45 * ease_out(pedra, 2) * math.cos(a), 0.45 * ease_out(pedra, 2) * math.sin(a), 5, 0.35), 0.012) * (1 - rel(t, 0.8, 1.0)) * 1.1
        G += T.gauss(0, 0, 0.3) * pedra * 0.25 * (1 - rel(t, 0.8, 1))
    g, h = _estouro(T, t, 0.24, 0.5, 0, 0, 0.2, 6, 31, 0.014)
    G += g * 0.7
    H += h * 0.7
    return G * env, H * env


# ================================================================== Cronos
def toque_do_tempo(T, t, rng):
    """O toque do tempo de Cronos: o relógio aparece em cima do rival (o mostrador com as marcas das horas) e os
    ponteiros giram depressa para trás, a areia do tempo escorre e o toque pesa nele."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    rel_ = back(rel(t, 0.0, 0.25), 1.4) * (1 - rel(t, 0.8, 0.95))
    if rel_ > 0:
        r = 0.4 * rel_
        G += T.ring(r, 0.02, 0, 0) * 1.2 + T.ring(r * 0.92, 0.008, 0, 0) * 0.6
        marcas = []
        for k in range(12):
            a = TAU * k / 12
            marcas.append((0.82 * r * math.cos(a), 0.82 * r * math.sin(a), 0.9 * r * math.cos(a), 0.9 * r * math.sin(a), 1.0))
        G += T.lines(marcas, 0.012) * 1.1
        gira = -TAU * 3 * ease_out(rel(t, 0.15, 0.8), 1.5)
        G += T.lines([(0, 0, 0.75 * r * math.cos(gira - math.pi / 2), 0.75 * r * math.sin(gira - math.pi / 2), 1.0),
                      (0, 0, 0.5 * r * math.cos(gira / 12 - math.pi / 2 + 1), 0.5 * r * math.sin(gira / 12 - math.pi / 2 + 1), 1.0)], 0.018) * 1.3
        H += T.gauss(0, 0, 0.025) * 1.2
    areia = rel(t, 0.3, 1.0)
    if 0 < areia < 1:
        q = np.random.default_rng(33)
        pts = []
        for _ in range(30):
            f = (areia * 1.5 + q.uniform(0, 1)) % 1
            pts.append((q.uniform(-0.3, 0.3), 0.1 + 0.6 * f, (1 - f) * 0.8))
        G += T.splats(pts, 0.01) * 1.2
    H += T.gauss(0, 0, 0.12) * pulso(t, 0.5, 0.75) * 1.0
    return G * env, H * env


REGISTRO = [
    ("bastoes_eletricos", bastoes_eletricos, GRANDE, "Básico do Asa Noturna: os dois bastões elétricos", False),
    ("lanternada", lanternada, GRANDE, "Básico do Dipper: o facho da lanterna e a pancada", False),
    ("gancho_de_mabel", gancho_de_mabel, GRANDE, "Básico da Mabel: o gancho e o glitter", False),
    ("faisca_arcana", faisca_arcana, GRANDE, "Básico da Yennefer: a centelha violeta", False),
    ("soco_do_nemesis", soco_do_nemesis, GRANDE, "Básico do Nêmesis: o punho com tentáculos", False),
    ("faisca_de_zeus", faisca_de_zeus, GRANDE, "Básico de Zeus: o raio arremessado", False),
    ("jato_do_tridente", jato_do_tridente, GRANDE, "Básico de Poseidon: os três jatos do tridente", False),
    ("escudada_de_atena", escudada_de_atena, GRANDE, "Básico de Atena: o escudo batendo", False),
    ("lanca_de_ares", lanca_de_ares, GRANDE, "Básico de Ares: a lança e a fúria", False),
    ("raio_de_apolo", raio_de_apolo, GRANDE, "Básico de Apolo: o sol e o feixe dourado", False),
    ("flecha_lunar", flecha_lunar, GRANDE, "Básico de Ártemis: a lua e a flecha de prata", False),
    ("chute_alado", chute_alado, GRANDE, "Básico de Hermes: a sandália alada", False),
    ("beijo_soprado", beijo_soprado, GRANDE, "Básico de Afrodite: os lábios e os corações", False),
    ("bote_da_medusa", bote_da_medusa, GRANDE, "Básico da Medusa: o bote e a pedra", False),
    ("toque_do_tempo", toque_do_tempo, GRANDE, "Básico de Cronos: o relógio para trás e a areia", False),
]
