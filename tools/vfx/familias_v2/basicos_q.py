"""Ataques básicos com animação própria, lote q (personagens novos).

T-800, RoboCop, Rambo, Indiana Jones, Jack Sparrow, Harry Potter, Voldemort, Gandalf, Godzilla, King Kong,
Shrek, Elsa, Malévola, Gênio e Scar: a mira vermelha do exterminador e a espingarda, a rajada de três da Auto-9
com a grade da mira, o fuzil em rajada com os cartuchos, o chicote do Indy e o soco, os cortes tortos do pirata
com a bússola, o feitiço vermelho do Harry, a maldição verde do Voldemort com a Marca, o cajado do Gandalf
batendo no chão, a cauda com as placas do Godzilla, os punhos do Kong, o tapa do Shrek com a lama, o floco de
neve da Elsa, o fogo verde da Malévola, o estalo do Gênio com a luva de boxe e a patada do Scar.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .basicos_a import _PUNHO, _move, _punho
from .basicos_k import _borda, _contorno, _estouro, _folha, _gira, _gotas
from .basicos_l import _estrelinhas
from .basicos_n import _coracao
from .rodada13 import _caveira, _chamas


def _tracos(T, t, t0, cano, alvo, larg=0.014):
    v = rel(t, t0, t0 + 0.06)
    if v <= 0 or t > t0 + 0.2:
        return T.zero()
    x = cano[0] + (alvo[0] - cano[0]) * min(1, v)
    y = cano[1] + (alvo[1] - cano[1]) * min(1, v)
    return T.tapered([(cano[0], cano[1], x, y, 1.0)], larg) * (1 - rel(t, t0 + 0.06, t0 + 0.2))


def _cartucho(T, t, t0, cano, lado=1):
    u = rel(t, t0, t0 + 0.45)
    if u <= 0 or u >= 1:
        return T.zero()
    cx = cano[0] + 0.05 + 0.18 * u
    cy = cano[1] - 0.3 * math.sin(math.pi * u) * lado + 0.35 * u
    return T.polys([(_gira([(-0.015, -0.007), (0.015, -0.007), (0.015, 0.007), (-0.015, 0.007)], u * 12, cx, cy), 1.0)]) * (1 - u)


# ================================================================== T-800
def tiro_do_exterminador(T, t, rng):
    """O tiro do T-800: a visão vermelha do exterminador (as linhas de varredura, a caixa que trava no rival e as
    barrinhas de leitura), e a espingarda dispara o leque de chumbo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    hud = pulso(t, 0.0, 0.6)
    if hud > 0:
        trava = ease_out(rel(t, 0.0, 0.25), 2.5)
        r = 0.55 - 0.3 * trava
        G += T.lines(_contorno([(-r, -r), (r, -r), (r, r), (-r, r)]), 0.012) * hud * 1.2
        linhas = (0.5 + 0.5 * np.sin(T.V * 90 + t * 30)) * ((np.abs(T.U) < 0.8) & (np.abs(T.V) < 0.6))
        G += linhas * hud * 0.12
        barras = [(-0.85, -0.5 + 0.06 * k, -0.85 + 0.1 + 0.15 * ((k * 7) % 5) / 5, -0.5 + 0.06 * k, 1.0) for k in range(5)]
        G += T.lines(barras, 0.01) * hud
    cano = (-0.85, 0.1)
    c = pulso(t, 0.3, 0.42)
    H += (T.flare(cano[0], cano[1], 0.4 * c + 0.01, 0, 0.016) + T.gauss(cano[0], cano[1], 0.07) * c) * c * 1.4
    q = np.random.default_rng(3)
    for k in range(9):
        alvo = (q.uniform(-0.12, 0.12), q.uniform(-0.18, 0.18))
        G += _tracos(T, t, 0.31, cano, alvo, 0.01) * 1.2
        b = rel(t, 0.36, 0.6)
        if 0 < b < 1:
            H += T.gauss(alvo[0], alvo[1], 0.02) * (1 - b) ** 2 * 1.5
    g, h = _estouro(T, t, 0.36, 0.65, 0, 0, 0.32, 9, 5)
    G += g
    H += h * 0.7
    G += _cartucho(T, t, 0.4, cano) * 1.2
    return G * env, H * env


# ================================================================== RoboCop
def auto9(T, t, rng):
    """A Auto-9 do RoboCop: a grade da mira robótica desce sobre o rival (as linhas cruzadas e o quadrado que pisca)
    e a pistola dispara a rajada de três, certinha, no mesmo ponto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    grade = pulso(t, 0.0, 0.55)
    if grade > 0:
        desce = ease_out(rel(t, 0.0, 0.25), 2)
        segs = []
        for k in range(5):
            y = -0.4 + 0.2 * k * desce
            segs.append((-0.4, y, 0.4, y, 0.5))
            x = -0.4 + 0.2 * k
            segs.append((x, -0.4, x, -0.4 + 0.8 * desce, 0.5))
        G += T.lines(segs, 0.008) * grade
        pisca = 1.0 if int(t * 20) % 2 else 0.4
        G += T.lines(_contorno([(-0.1, -0.1), (0.1, -0.1), (0.1, 0.1), (-0.1, 0.1)]), 0.016) * grade * pisca * 1.3
    cano = (-0.85, -0.02)
    for k in range(3):
        t0 = 0.3 + 0.07 * k
        c = pulso(t, t0, t0 + 0.06)
        H += T.flare(cano[0], cano[1], 0.3 * c + 0.01, 0, 0.012) * c * 1.4
        G += _tracos(T, t, t0, cano, (0.0, 0.0), 0.016) * 1.3
        G += _cartucho(T, t, t0, cano) * 1.1
    g, h = _estouro(T, t, 0.35, 0.7, 0, 0, 0.28, 8, 7)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Rambo
def rajada_de_fuzil(T, t, rng):
    """A rajada do Rambo: o fuzil cospe fogo sem parar (o clarão piscando no cano), os traçantes riscam a arena em
    leque, os acertos estouram no rival e os cartuchos caem em cascata."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    cano = (-0.85, 0.05)
    q = np.random.default_rng(9)
    for k in range(10):
        t0 = 0.05 + 0.05 * k
        alvo = (q.uniform(-0.15, 0.2), q.uniform(-0.25, 0.25))
        c = pulso(t, t0, t0 + 0.04)
        H += T.flare(cano[0], cano[1], 0.3 * c + 0.01, q.uniform(-0.3, 0.3), 0.012) * c * 1.4
        G += _tracos(T, t, t0, cano, alvo, 0.012) * 1.2
        b = rel(t, t0 + 0.05, t0 + 0.25)
        if 0 < b < 1:
            H += T.gauss(alvo[0], alvo[1], 0.025) * (1 - b) ** 2 * 1.6
        G += _cartucho(T, t, t0, cano) * 0.9
    fum = rel(t, 0.1, 1.0)
    if 0 < fum < 1:
        pts = [(cano[0] + 0.1 + 0.2 * fum, cano[1] - 0.2 * fum + 0.05 * k, (1 - fum) * 0.4) for k in range(5)]
        G += T.splats(pts, 0.06) * 0.6
    return G * env, H * env


# ================================================================== Indiana Jones
def chicote_de_indy(T, t, rng):
    """O ataque do Indiana Jones: o chicote estala na frente (a curva longa que se estica e quebra na ponta com o
    estalo) e logo em seguida o soco direto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    chic = ease_out(rel(t, 0.0, 0.22), 2)
    if chic > 0 and t < 0.4:
        pts = []
        for j in range(36):
            u = j / 35 * chic
            pts.append((-0.95 + 1.05 * u, -0.35 * math.sin(math.pi * u) + 0.12 * math.sin(TAU * u * 2.5 + t * 40) * (1 - u)))
        G += T.polyline(pts, 0.014) * 1.3 * (1 - rel(t, 0.28, 0.4))
        H += T.flare(pts[-1][0], pts[-1][1], 0.3 * pulso(t, 0.17, 0.3) + 0.01, 0.4, 0.01) * pulso(t, 0.17, 0.3) * 1.3
    vai = ease_in(rel(t, 0.3, 0.48), 2)
    if vai > 0 and t < 0.65:
        x = -0.8 + 0.72 * vai
        P, nos = _punho(T, x, 0.05, 1.6)
        G += (P * 0.6 + _borda(T, P, 0.006) * 1.1) * (1 - rel(t, 0.55, 0.65))
        H += nos * 0.4
    g, h = _estouro(T, t, 0.47, 0.75, 0.05, 0.05, 0.35, 9, 11)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Jack Sparrow
def espada_pirata(T, t, rng):
    """O golpe do Jack Sparrow: dois cortes tortos e desengonçados (o sabre balança meio bêbado, num arco que
    ondula) e a bússola que não aponta para o norte gira doida no canto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    for k, (a0, a1, t0) in enumerate(((-2.6, -0.5, 0.05), (2.2, 0.3, 0.32))):
        u = ease_out(rel(t, t0, t0 + 0.2), 2)
        if u <= 0 or t > t0 + 0.35:
            continue
        some = 1 - rel(t, t0 + 0.2, t0 + 0.35)
        cab = a0 + (a1 - a0) * u
        A = T.arc_band(0.5 + 0.06 * math.sin(t * 25), 0.07, a0, cab, cx=-0.2, cy=0.05 + 0.04 * math.sin(t * 18), crescente=True)
        G += (A * 1.3 + T.blur(A, 0.02) * 0.4) * some
        g, h = _estouro(T, t, t0 + 0.15, t0 + 0.4, 0.15, 0.0, 0.25, 8, 13 + k, 0.014)
        G += g * 0.8
        H += h * 0.7
    bus = pulso(t, 0.0, 0.9)
    if bus > 0:
        cx, cy = -0.7, -0.6
        G += T.ring(0.1, 0.012, cx, cy) * bus * 1.1
        a = t * 25 + 3 * math.sin(t * 7)
        G += T.polys([(_gira([(0, -0.08), (0.02, 0), (0, 0.08), (-0.02, 0)], a, cx, cy), 1.0)]) * bus * 1.2
    return G * env, H * env


# ================================================================== Harry Potter
def expelliarmus(T, t, rng):
    """O feitiço do Harry: a ponta da varinha acende, o raio vermelho dispara com as faíscas soltando atrás, e
    estoura no rival; a cicatriz em raio pisca um instante."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    ponta = (-0.8, 0.05)
    G += T.lines([(ponta[0] - 0.25, ponta[1] + 0.12, ponta[0], ponta[1], 1.0)], 0.018) * pulso(t, 0.0, 0.5) * 1.1
    H += T.gauss(ponta[0], ponta[1], 0.03) * pulso(t, 0.0, 0.3) * 1.6
    voa = ease_in(rel(t, 0.15, 0.35), 1.4)
    if 0 < voa and t < 0.5:
        x = ponta[0] + (0.0 - ponta[0]) * voa
        y = ponta[1] * (1 - voa)
        G += T.tapered([(ponta[0], ponta[1], x, y, 1.0)], 0.045) * 1.2 * (1 - rel(t, 0.38, 0.5))
        H += T.gauss(x, y, 0.04) * 1.6
        q = np.random.default_rng(int(t * 40) % 9)
        pts = [(ponta[0] + (x - ponta[0]) * q.uniform(0, 1), y + q.uniform(-0.08, 0.08), q.uniform(0.4, 1)) for _ in range(12)]
        G += T.splats(pts, 0.012) * 1.2
    g, h = _estouro(T, t, 0.34, 0.65, 0, 0, 0.35, 10, 15)
    G += g
    H += h
    cic = pulso(t, 0.0, 0.25)
    if cic > 0:
        G += T.polyline([(-0.6, -0.65), (-0.53, -0.6), (-0.58, -0.56), (-0.5, -0.5)], 0.012) * cic * 1.3
    return G * env, H * env


# ================================================================== Voldemort
def avada_verde(T, t, rng):
    """O feitiço do Voldemort: o jato verde, retorcido e cheio de estalos, sai da varinha e acerta o rival; a fumaça
    sobe e forma por um instante a Marca Negra (a caveira com a serpente saindo da boca)."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    ponta = (-0.8, 0.1)
    vai = ease_out(rel(t, 0.05, 0.22), 2)
    some = 1 - rel(t, 0.35, 0.5)
    if vai > 0 and some > 0:
        q = np.random.default_rng(int(t * 50) % 13)
        for k in range(2):
            R = T.polyline(jagged(q, ponta[0], ponta[1], ponta[0] + (0.0 - ponta[0]) * vai, ponta[1] * (1 - vai), 5, 0.12), 0.022 - 0.008 * k)
            G += R * 1.3 * some + T.blur(R, 0.02) * 0.6 * some
            H += R * 0.6 * some
    g, h = _estouro(T, t, 0.22, 0.5, 0, 0, 0.3, 9, 17)
    G += g
    H += h
    marca = pulso(t, 0.4, 1.0)
    if marca > 0:
        sobe = rel(t, 0.4, 1.0)
        linhas, _ = _caveira(0.0, -0.45 - 0.1 * sobe, 0.6, dentes_longos=False)
        G += T.lines(linhas, 0.012) * marca * 1.1
        pts = [(0.0 + 0.12 * math.sin(u * 9), -0.3 - 0.1 * sobe + 0.35 * u) for u in np.linspace(0, 1, 24)]
        G += T.polyline(pts, 0.014) * marca * 1.1
        q = np.random.default_rng(19)
        fum = [(q.uniform(-0.25, 0.25), -0.4 + q.uniform(-0.2, 0.3) - 0.15 * sobe, 0.4 * marca) for _ in range(12)]
        G += T.splats(fum, 0.06) * 0.5
    return G * env, H * env


# ================================================================== Gandalf
def cajado_branco(T, t, rng):
    """O cajado do Gandalf: o cajado sobe e bate com força no chão em frente ao rival, a luz branca explode do ponto
    em anel e as rachaduras correm pelo chão."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    desce = ease_in(rel(t, 0.1, 0.32), 2.5)
    if t < 0.55:
        y = 0.3 - 0.5 * (1 - desce)
        G += T.lines([(-0.05, y - 0.9, -0.05, y, 1.0)], 0.024) * 1.1 * (1 - rel(t, 0.42, 0.55))
        H += T.gauss(-0.05, y - 0.9, 0.04) * (0.5 + pulso(t, 0.05, 0.35)) * 1.3
    bate = rel(t, 0.3, 0.85)
    if 0 < bate < 1:
        b = ease_out(bate, 2.5)
        H += T.gauss(-0.05, 0.3, 0.1 + 0.15 * b) * (1 - bate) ** 2 * 2.2 + T.flare(-0.05, 0.3, 0.9 * (1 - bate), 0, 0.016) * (1 - bate)
        G += T.ring(0.1 + 0.8 * b, 0.04, -0.05, 0.3, squash=2.5) * (1 - bate) * 1.4
        G += T.ring(0.05 + 0.5 * b, 0.03, -0.05, 0.3) * (1 - bate)
        q = np.random.default_rng(21)
        for k in range(6):
            a = math.pi * (k + 0.5) / 6
            G += T.polyline(jagged(q, -0.05, 0.3, -0.05 + 0.7 * b * math.cos(a), 0.3 + 0.12 * b * math.sin(a), 4, 0.3), 0.01) * (1 - rel(t, 0.75, 1)) * 1.2
    return G * env, H * env


# ================================================================== Godzilla
def cauda_de_godzilla(T, t, rng):
    """A cauda do Godzilla: a cauda gigante varre a arena num arco largo, com as placas dorsais pontudas acendendo em
    azul atômico, bate no rival e a onda de choque sai."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    gira = ease_out(rel(t, 0.0, 0.35), 2)
    if gira > 0 and t < 0.6:
        some = 1 - rel(t, 0.42, 0.6)
        a1 = -2.9 + 2.9 * gira
        cx, cy = -0.3, 0.55
        A = T.arc_band(0.75, 0.13, a1 - 1.6, a1, cx=cx, cy=cy, taper=0.7)
        G += (A * 0.6 + _borda(T, A, 0.01) * 1.2) * some
        placas = []
        for k in range(7):
            a = a1 - 1.5 * k / 7
            r0 = 0.75 - 0.08
            x, y = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
            nx, ny = math.cos(a), math.sin(a)
            tx, ty = -ny, nx
            tam = 0.09 * (1 - k / 9)
            placas.append(([(x + tx * tam * 0.6, y + ty * tam * 0.6), (x - tx * tam * 0.6, y - ty * tam * 0.6), (x - nx * tam * 1.4, y - ny * tam * 1.4)], 1.0))
        Pl = T.polys(placas)
        G += Pl * 1.2 * some
        H += Pl * 0.6 * some
    g, h = _estouro(T, t, 0.32, 0.7, 0.1, 0, 0.45, 12, 23, 0.026)
    G += g * 1.1
    H += h
    return G * env, H * env


# ================================================================== King Kong
def soco_de_kong(T, t, rng):
    """O ataque do Kong: ele bate no peito (os anéis de vibração), junta os dois punhos enormes no alto e martela o
    rival de cima, com o chão tremendo."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    for k in range(3):
        u = rel(t, 0.03 * k * 2, 0.06 * k + 0.2)
        if 0 < u < 1:
            G += T.ring(0.08 + 0.2 * u, 0.02, -0.65, 0.2) * (1 - u) * 1.1
    desce = ease_in(rel(t, 0.25, 0.42), 2.5)
    if 0.15 < t < 0.6:
        y = -0.8 + 0.75 * desce
        for lado in (-1, 1):
            P, nos = _punho(T, 0.09 * lado, y, 2.0, math.pi / 2)
            G += (P * 0.6 + _borda(T, P, 0.007) * 1.2) * (1 - rel(t, 0.5, 0.6))
        if desce < 1:
            G += T.tapered([(0, y - 0.5, 0, y - 0.1, 0.7)], 0.08) * 0.5
    bate = rel(t, 0.42, 0.85)
    if 0 < bate < 1:
        b = ease_out(bate, 2.5)
        H += T.gauss(0, 0.05, 0.12) * (1 - bate) ** 2 * 2.0
        G += T.ring(0.1 + 0.8 * b, 0.05, 0, 0.3, squash=2.6) * (1 - bate) * 1.4
        q = np.random.default_rng(25)
        pts = [(q.uniform(-0.6, 0.6) * b, 0.3 - q.uniform(0, 0.3) * b, (1 - bate) * 0.6) for _ in range(14)]
        G += T.splats(pts, 0.05) * 0.8
    return G * env, H * env


# ================================================================== Shrek
def tapa_de_ogro(T, t, rng):
    """O tapa do Shrek: a mão enorme de ogro vem de lado e estala no rival, a lama do pântano espirra e sobe a
    nuvenzinha verde do arroto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vem = ease_in(rel(t, 0.0, 0.28), 2)
    if t < 0.45:
        x = -0.9 + 0.85 * vem
        pts = [(-0.14, 0.1), (-0.14, -0.06), (-0.1, -0.1), (-0.07, -0.26), (-0.02, -0.26), (0.0, -0.1), (0.03, -0.28), (0.08, -0.28),
               (0.09, -0.08), (0.13, -0.22), (0.17, -0.2), (0.15, 0.0), (0.2, -0.06), (0.22, 0.0), (0.14, 0.12), (0.0, 0.16)]
        M = T.polys([(_gira([(px * 1.7, py * 1.7) for px, py in pts], 0.3 - 0.4 * vem, x, 0.0), 1.0)])
        G += M * 0.5 + _borda(T, M, 0.009) * 1.4
    g, h = _estouro(T, t, 0.27, 0.55, 0.05, 0, 0.35, 9, 27)
    G += g
    H += h
    G += _gotas(T, t, 0.28, 0.6, 0.05, 0.0, 18, 0.55, 29, -2.9, 0.3, 0.03, 0.5) * 1.1
    arroto = rel(t, 0.45, 1.0)
    if 0 < arroto < 1:
        q = np.random.default_rng(31)
        pts = [(-0.55 + q.uniform(-0.1, 0.1) + 0.2 * arroto, -0.35 - 0.25 * arroto + q.uniform(-0.05, 0.05), math.sin(math.pi * arroto) * 0.6) for _ in range(8)]
        G += T.splats(pts, 0.06) * 0.8
    return G * env, H * env


# ================================================================== Elsa
def _floco(cx, cy, r, ang):
    """O floco de neve de seis braços, com os galhinhos em cada um."""
    segs = []
    for k in range(6):
        a = ang + TAU * k / 6
        ux, uy = math.cos(a), math.sin(a)
        segs.append((cx, cy, cx + r * ux, cy + r * uy, 1.0))
        for f, l in ((0.45, 0.3), (0.72, 0.22)):
            bx, by = cx + r * f * ux, cy + r * f * uy
            for lado in (-1, 1):
                b = a + lado * 0.7
                segs.append((bx, by, bx + r * l * math.cos(b), by + r * l * math.sin(b), 0.9))
    return segs


def floco_de_elsa(T, t, rng):
    """O floco de gelo da Elsa: o floco de neve de seis braços (com os galhinhos) se forma girando na mão, voa
    rodopiando até o rival e explode em cristais e brilho frio."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    forma = back(rel(t, 0.0, 0.2), 1.4)
    voa = ease_in(rel(t, 0.2, 0.42), 1.4)
    if forma > 0 and t < 0.48:
        x = -0.7 + 0.7 * voa
        F = T.lines(_floco(x, 0.0, 0.3 * forma, t * 10), 0.02)
        G += F * 1.3 + T.blur(F, 0.015) * 0.5
        H += T.gauss(x, 0, 0.03) * 1.2
        if voa > 0:
            pts = [(x - 0.3 * u, 0.05 * math.sin(u * 12 + t * 20), 1 - u) for u in np.linspace(0, 1, 10)]
            G += T.splats(pts, 0.012) * 0.8
    bum = rel(t, 0.42, 0.85)
    if 0 < bum < 1:
        b = ease_out(bum, 2.5)
        shapes = []
        for k in range(8):
            a = TAU * k / 8
            r = 0.12 + 0.3 * b
            shapes.append((_gira([(0, -0.07), (0.02, 0), (0, 0.07), (-0.02, 0)], a + math.pi / 2, r * math.cos(a), r * math.sin(a)), 1 - bum))
        G += T.polys(shapes) * 1.3
        H += T.gauss(0, 0, 0.1) * (1 - bum) ** 2 * 1.8
        G += T.ring(0.08 + 0.4 * b, 0.025, 0, 0) * (1 - bum)
    return G * env, H * env


# ================================================================== Malévola
def raio_de_malevola(T, t, rng):
    """O raio verde da Malévola: o orbe do cajado acende, o fogo verde sai num jato que se contorce em chamas, e no
    rival brotam os espinhos negros."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    orbe = (-0.75, -0.25)
    G += T.lines([(orbe[0], orbe[1] + 0.05, orbe[0] - 0.05, orbe[1] + 0.8, 1.0)], 0.02) * pulso(t, 0.0, 0.6)
    H += T.gauss(orbe[0], orbe[1], 0.05) * pulso(t, 0.0, 0.5) * 1.5
    G += T.ring(0.06, 0.012, orbe[0], orbe[1]) * pulso(t, 0.0, 0.6)
    vai = ease_out(rel(t, 0.12, 0.32), 2)
    some = 1 - rel(t, 0.4, 0.55)
    if vai > 0 and some > 0:
        x1, y1 = orbe[0] + (0.0 - orbe[0]) * vai, orbe[1] * (1 - vai)
        ang = math.atan2(y1 - orbe[1], x1 - orbe[0])
        dist = math.hypot(x1 - orbe[0], y1 - orbe[1])
        F = _chamas(T, t, (orbe[0] + x1) / 2, (orbe[1] + y1) / 2, dist / 2, 0.15, 7, 33, ang + math.pi / 2)
        G += (F * 0.9 + T.blur(F, 0.02) * 0.5) * some
        G += T.lines([(orbe[0], orbe[1], x1, y1, 1.0)], 0.03) * some * 0.8
        H += T.lines([(orbe[0], orbe[1], x1, y1, 1.0)], 0.01) * some
    espinhos = rel(t, 0.32, 1.0)
    if espinhos > 0:
        shapes = []
        for k in range(7):
            a = -math.pi / 2 + (k - 3) * 0.35
            sobe = back(rel(espinhos, 0.04 * k, 0.4 + 0.04 * k), 1.5) * (1 - rel(t, 0.8, 1))
            if sobe <= 0:
                continue
            bx = (k - 3) * 0.1
            shapes.append(([(bx - 0.04, 0.35), (bx + 0.04, 0.35), (bx + 0.3 * sobe * math.cos(a) * 0.4, 0.35 + 0.5 * sobe * math.sin(a))], 1.0))
        if shapes:
            E = T.polys(shapes)
            G += E * 0.8 + _borda(T, E, 0.005) * 1.0
    return G * env, H * env


# ================================================================== Gênio
def estalo_do_genio(T, t, rng):
    """O estalo do Gênio: o estalo de dedos solta a fumacinha mágica com as estrelinhas, e dela pula uma luva de boxe
    gigante na ponta de uma mola que acerta o rival — e volta."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    estalo = pulso(t, 0.0, 0.2)
    H += T.flare(-0.7, -0.35, 0.25 * estalo + 0.01, 0.4, 0.01) * estalo * 1.4
    fum = rel(t, 0.05, 0.6)
    if 0 < fum < 1:
        q = np.random.default_rng(35)
        pts = [(-0.6 + q.uniform(-0.15, 0.15) * (0.5 + fum), -0.2 + q.uniform(-0.12, 0.12) * (0.5 + fum), (1 - fum) * 0.7) for _ in range(12)]
        G += T.splats(pts, 0.07) * 0.8
        G += _estrelinhas(T, t, 0.05, 0.55, -0.6, -0.2, 5, 0.3, 37)
    mola = ease_out(rel(t, 0.18, 0.35), 3) * (1 - ease_in(rel(t, 0.55, 0.8), 2))
    if mola > 0.02:
        x0, x1 = -0.55, -0.55 + 0.5 * mola
        pts = [(x0 + (x1 - x0) * u, -0.2 + 0.2 * u + 0.05 * math.sin(u * TAU * 6)) for u in np.linspace(0, 1, 40)]
        G += T.polyline(pts, 0.012) * 1.2
        P, nos = _punho(T, x1 + 0.12, 0.0, 2.2)
        G += P * 0.6 + _borda(T, P, 0.008) * 1.3
        H += nos * 0.5
    g, h = _estouro(T, t, 0.33, 0.6, 0.1, 0, 0.35, 10, 39)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Scar
def patada_de_scar(T, t, rng):
    """A patada do Scar: a pata do leão vem de cima com as garras de fora, rasga o rival em três riscos curvos e
    soltam-se as faíscas verdes do fogo da savana."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    for k in range(3):
        t0 = 0.1 + 0.025 * k
        p = ease_out(rel(t, t0, t0 + 0.14), 3)
        ini = rel(t, t0 + 0.2, t0 + 0.5)
        if p > 0 and ini < 1:
            dx = (k - 1) * 0.13
            L = T.arc_band(0.75, 0.04, -1.9, -1.9 + 1.0 * p, cx=0.45 + dx, cy=0.6, crescente=True)
            G += L * 1.4 * (1 - ini)
            H += L * 0.5 * (1 - ini)
    vem = ease_in(rel(t, 0.0, 0.14), 2)
    if t < 0.3:
        px, py = 0.4 - 0.35 * vem, -0.8 + 0.6 * vem
        G += T.gauss(px, py, 0.1) * 0.7 * (1 - rel(t, 0.2, 0.3))
        for k in range(3):
            G += T.polys([(_gira([(0, 0), (0.03, 0.02), (0.0, 0.1)], -0.4 + 0.4 * k, px - 0.08 + 0.08 * k, py + 0.06), 1.0)]) * (1 - rel(t, 0.2, 0.3))
    G += _gotas(T, t, 0.25, 0.6, 0.0, 0.0, 14, 0.5, 41, -2.6, -0.4, 0.012, -0.3) * 1.2
    return G * env, H * env


REGISTRO = [
    ("tiro_do_exterminador", tiro_do_exterminador, GRANDE, "Básico do T-800: a mira vermelha e a espingarda", False),
    ("auto9", auto9, GRANDE, "Básico do RoboCop: a grade da mira e a rajada de três", False),
    ("rajada_de_fuzil", rajada_de_fuzil, GRANDE, "Básico do Rambo: a rajada e os cartuchos", False),
    ("chicote_de_indy", chicote_de_indy, GRANDE, "Básico do Indiana Jones: o chicote e o soco", False),
    ("espada_pirata", espada_pirata, GRANDE, "Básico do Jack Sparrow: os cortes tortos e a bússola", False),
    ("expelliarmus", expelliarmus, GRANDE, "Básico do Harry: o feitiço vermelho", False),
    ("avada_verde", avada_verde, GRANDE, "Básico do Voldemort: o jato verde e a Marca", False),
    ("cajado_branco", cajado_branco, GRANDE, "Básico do Gandalf: o cajado no chão e a luz", False),
    ("cauda_de_godzilla", cauda_de_godzilla, GRANDE, "Básico do Godzilla: a cauda com as placas", False),
    ("soco_de_kong", soco_de_kong, GRANDE, "Básico do Kong: o peito e os punhos de cima", False),
    ("tapa_de_ogro", tapa_de_ogro, GRANDE, "Básico do Shrek: o tapa, a lama e o arroto", False),
    ("floco_de_elsa", floco_de_elsa, GRANDE, "Básico da Elsa: o floco de neve girando", False),
    ("raio_de_malevola", raio_de_malevola, GRANDE, "Básico da Malévola: o fogo verde e os espinhos", False),
    ("estalo_do_genio", estalo_do_genio, GRANDE, "Básico do Gênio: o estalo e a luva de boxe", False),
    ("patada_de_scar", patada_de_scar, GRANDE, "Básico do Scar: a patada com as garras", False),
]
