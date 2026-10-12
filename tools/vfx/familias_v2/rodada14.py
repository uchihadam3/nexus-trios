"""Rodada 14 das habilidades próprias: Cavaleiro da Lua, Tempestade, Jean Grey, Vampira e Gambit (Marvel).

Cavaleiro da Lua
- manto_lunar: a capa branca se abre como asas com a lua crescente atrás; o rival é envolvido pelas faixas
  do manto e fica tonto (as espirais), e o olho de Khonshu o marca.
- crescente_de_prata: três dardos em meia-lua giram em leque até o rival e estouram em prata; um crescente
  fino protege o Cavaleiro.
- khonshu_preparo: o Preparo do Julgamento — as fases da lua girando em volta (nova → cheia) e o ankh no
  meio pulsando (laço).
- julgamento_de_khonshu: a lua cheia gigante com o crânio de pássaro de Khonshu surge, e as colunas de luar
  descem sobre o rival com os hieróglifos girando no chão.

Tempestade
- rajada_de_vento: as correntes de vento atravessam da esquerda para a direita em faixas curvas, com folhas
  e poeira, e os redemoinhos pequenos ficam (Lento).
- relampago_em_cadeia: o raio cai do alto no primeiro ponto e salta de um em um, ramificando, e cada ponto
  estala.
- tempestade_preparo: o Preparo do Olho da tempestade — os olhos brancos acesos, as nuvens girando em
  espiral em volta e os raios pequenos dentro (laço).
- olho_da_tempestade: o anel de nuvens gira com o olho calmo no meio, os raios descem do anel no rival e o
  vento corre em volta.

Jean Grey
- escudo_mental: a cúpula rosa de força psíquica se forma com as ondas de pensamento subindo, e o hexágono
  da mente brilha em volta do aliado.
- muralha_telecinetica: a parede telecinética translúcida se ergue na frente do aliado, as ondas correm
  nela e os destroços param no ar presos pelo contorno rosa.
- fenix_preparo: o Preparo da Fênix — o fogo sobe em volta e desenha as asas abertas, e os olhos acendem
  (laço).
- fenix_desperta: a ave de fogo abre as asas gigantes e mergulha, e a explosão de chamas varre o campo; os
  choques travam todo mundo (Paralisado).

Vampira
- forca_roubada: ela voa (as linhas de velocidade) e dá o soco carregado com a força roubada (a aura
  verde-amarela), e o Preparo do rival quebra em cacos.
- memoria_preparo: o Preparo da Memória emprestada — a mecha branca no cabelo e os fragmentos de memória
  (os poderes dos outros) girando em volta (laço).
- memoria_emprestada: os fragmentos dos poderes copiados piscam um atrás do outro (as garras, o raio, o
  gelo) e se juntam num golpe só.

Gambit
- carta_carregada: a carta de baralho (o naipe de copas) brilha rosa de energia cinética, voa girando, gruda
  no rival e fica tiquetaqueando (Bomba).
- baralho_explosivo: o leque de cinco cartas sai da mão, se abre no ar e as cartas explodem em fila no
  rival.
- gambit_preparo: o Preparo do Bastão cinético — as cartas sendo embaralhadas (a cascata entre as mãos), uma
  a uma acendendo, e os olhos vermelhos (laço).
- bastao_cinetico: o bastão carregado gira, bate no chão e a onda cinética corre, detonando as cartas
  espalhadas em volta do rival.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .rodada13 import _borda, _chamas, _contorno, _gira


def _crescente(cx, cy, r, ang=0.0, espessura=0.55, n=26):
    """A meia-lua: o arco de fora e o de dentro deslocado, as duas pontas finas."""
    fora = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(-math.pi / 2, math.pi / 2, n)]
    dentro = [(cx + r * (1 - espessura) * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(math.pi / 2, -math.pi / 2, n)]
    return _gira([(x - cx, y - cy) for x, y in fora + dentro], ang, cx, cy)


def _espiral(cx, cy, r, voltas, fase, n=40):
    return [(cx + r * (j / n) * math.cos(fase + TAU * voltas * j / n), cy + r * (j / n) * math.sin(fase + TAU * voltas * j / n) * 0.7) for j in range(n + 1)]


# =================================================================== Cavaleiro da Lua
def manto_lunar(T, t, rng):
    """O manto lunar: atrás do Cavaleiro sobe a lua crescente grande, o capuz pontudo aparece e a capa branca se abre
    como duas asas recortadas; as faixas do manto voam e se enrolam no rival, que fica tonto (as espirais
    girando em volta da cabeça), e o olho de Khonshu o marca."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = ease_out(rel(t, 0.0, 0.25), 3)
    some = 1 - rel(t, 0.38, 0.52)
    if abre > 0 and some > 0:
        cx, cy = -0.6, 0.05
        L = T.polys([(_crescente(cx + 0.05, cy - 0.15, 0.42, math.pi + 0.3, 0.45), 1.0)])
        G += L * 0.35 * some + _borda(T, L, 0.01) * 0.9 * some
        H += L * 0.25 * some
        for lado in (-1, 1):
            asa = [(cx + 0.04 * lado, cy - 0.12)]
            for j in range(9):
                u = j / 8
                a = -math.pi / 2 + lado * (0.25 + 1.75 * u * abre)
                r = 0.48 * abre * (0.55 + 0.45 * math.sin(math.pi * u * 0.9))
                asa.append((cx + r * math.cos(a), cy + r * math.sin(a) + 0.1 * u))
                if j < 8:
                    a2 = -math.pi / 2 + lado * (0.25 + 1.75 * (u + 0.0625) * abre)
                    r2 = r * 0.82
                    asa.append((cx + r2 * math.cos(a2), cy + r2 * math.sin(a2) + 0.1 * u))
            asa.append((cx + 0.04 * lado, cy + 0.32))
            A = T.polys([(asa, 1.0)])
            G += (A * 0.3 + _borda(T, A, 0.007) * 1.5) * some
        capuz = [(cx, cy - 0.32), (cx + 0.08, cy - 0.12), (cx + 0.06, cy + 0.0), (cx - 0.06, cy + 0.0), (cx - 0.08, cy - 0.12)]
        C = T.polys([(capuz, 1.0)])
        G += (C * 0.8 + _borda(T, C, 0.006) * 0.8) * some
        H += T.splats([(cx - 0.025, cy - 0.1, 1.0), (cx + 0.025, cy - 0.1, 1.0)], 0.012) * some * 1.6
    faixa = rel(t, 0.18, 0.5)
    if 0 < faixa and t < 0.62:
        b = 1 - rel(t, 0.5, 0.62)
        for k in range(3):
            pts = []
            for j in range(36):
                u = j / 35 * ease_out(min(1, faixa), 2)
                if u < 0.7:
                    x = -0.5 + 0.5 * u / 0.7
                    y = -0.2 + 0.2 * k + 0.1 * math.sin(u * 10 + k + t * 10)
                else:
                    a = (u - 0.7) * 26 + k * 2.1
                    x, y = 0.24 * math.cos(a), 0.05 + 0.3 * (u - 0.7) * math.sin(a) + 0.08 * (k - 1)
                pts.append((x, y))
            F = T.polyline(pts, 0.03)
            G += (F * 0.5 + _borda(T, F, 0.005) * 1.3) * b
    tonto = rel(t, 0.42, 1.0)
    if 0 < tonto < 1:
        bb = math.sin(math.pi * tonto)
        for k in range(3):
            a0 = t * 10 + TAU * k / 3
            ex, ey = 0.26 * math.cos(a0), -0.38 + 0.07 * math.sin(a0)
            G += T.polyline(_espiral(ex, ey, 0.09, 2, t * 20), 0.013) * bb * 1.3
        olho = [(-0.2, 0.06, 0.0, -0.02, 1.0), (0.0, -0.02, 0.2, 0.06, 1.0), (-0.2, 0.06, 0.0, 0.13, 1.0), (0.0, 0.13, 0.2, 0.06, 1.0),
                (-0.03, 0.13, -0.08, 0.3, 1.0), (0.06, 0.12, 0.17, 0.28, 1.0), (0.17, 0.28, 0.2, 0.22, 1.0)]
        G += T.lines(olho, 0.016) * bb * 1.3
        H += T.gauss(0.0, 0.055, 0.04) * bb * 1.6
    return G * env, H * env


def crescente_de_prata(T, t, rng):
    """O crescente de prata: três dardos em meia-lua giram em leque até o rival e estouram em prata, um atrás do
    outro; no fim um crescente fino brilha na frente do Cavaleiro (Protegido)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k in range(3):
        t0 = 0.05 + 0.07 * k
        u = rel(t, t0, t0 + 0.25)
        if 0 < u < 1:
            e = ease_in(u, 1.3)
            arco = (k - 1) * 0.35
            x = -0.85 + 0.85 * e
            y = arco * math.sin(math.pi * e)
            D = T.polys([(_crescente(x, y, 0.19, t * 40 + k, 0.45), 1.0)])
            G += D * 1.0 + _borda(T, D, 0.006) * 0.8
            H += D * 0.6
            rastro = [(-0.85 + 0.85 * ease_in(max(0, u - 0.06 * j), 1.3), arco * math.sin(math.pi * ease_in(max(0, u - 0.06 * j), 1.3)), 0.5 * (1 - j / 5)) for j in range(1, 5)]
            H += T.splats(rastro, 0.02) * 0.6
        b = rel(t, t0 + 0.25, t0 + 0.5)
        if 0 < b < 1:
            r = 0.05 + 0.28 * ease_out(b, 3)
            G += T.ring(r, 0.02, 0.03 * (k - 1), 0.04 * (k - 1)) * (1 - b) * 1.2
            H += T.flare(0.03 * (k - 1), 0.04 * (k - 1), 0.5 * (1 - b) + 0.01, 0.785, 0.01) * (1 - b) * 1.2
    prot = pulso(t, 0.55, 1.0)
    if prot > 0:
        P = T.polys([(_crescente(-0.6, 0.0, 0.32, 0.0, 0.3), 1.0)])
        G += _borda(T, P, 0.008) * prot * 1.3
        H += P * prot * 0.2
    return G * env, H * env


def _ankh(cx, cy, s):
    laco = [(cx + 0.07 * s * math.cos(a), cy - 0.15 * s + 0.1 * s * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)]
    return _contorno(laco) + [(cx, cy - 0.05 * s, cx, cy + 0.3 * s, 1.0), (cx - 0.15 * s, cy, cx + 0.15 * s, cy, 1.0)]


def khonshu_preparo(T, t, rng):
    """O Preparo do Julgamento de Khonshu: as oito fases da lua giram em volta (da nova à cheia) e o ankh no meio
    pulsa prateado (laço)."""
    G, H = vazio(T)
    giro = TAU * t / 4
    for k in range(8):
        a = giro + TAU * k / 8
        x, y = 0.55 * math.cos(a), 0.55 * math.sin(a) * 0.9
        fase = k / 7
        G += T.ring(0.11, 0.01, x, y) * 0.8
        if fase > 0.05:
            cheia = T.polys([([(x + 0.1 * math.cos(b), y + 0.1 * math.sin(b)) for b in np.linspace(0, TAU, 24, endpoint=False)], 1.0)]) if fase > 0.9 else T.polys([(_crescente(x, y, 0.1, 0.0, 0.15 + 0.8 * fase), 1.0)])
            G += cheia * (0.6 + 0.5 * fase)
            H += cheia * 0.5 * fase
    bate = 0.7 + 0.3 * math.sin(TAU * t * 2)
    A = T.lines(_ankh(0, 0.05, 1.3), 0.02)
    G += A * 1.2 * bate + T.blur(A, 0.03) * 0.6
    H += A * 0.5 * bate
    return G, H


def julgamento_de_khonshu(T, t, rng):
    """O Julgamento de Khonshu: a lua cheia gigante sobe com o crânio de pássaro de Khonshu dentro (o bico comprido
    e as órbitas), as colunas de luar descem sobre o rival e os hieróglifos giram no chão (Enfraquecido)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    sobe = ease_out(rel(t, 0.0, 0.3), 2.5)
    lua = 1 - rel(t, 0.65, 0.88)
    if sobe > 0:
        ly = -0.9 + 0.45 * sobe
        G += T.ring(0.32, 0.02, 0, ly) * lua * 1.1 + T.gauss(0, ly, 0.28) * lua * 0.25
        H += T.gauss(0, ly, 0.2) * lua * 0.35
        cranio = [(0.0 - 0.14, ly - 0.05), (-0.05, ly - 0.15), (0.08, ly - 0.12), (0.14, ly - 0.02), (0.1, ly + 0.08), (0.42, ly + 0.2), (0.06, ly + 0.14), (-0.1, ly + 0.08)]
        G += T.lines(_contorno(cranio), 0.014) * lua * 1.3
        H += T.splats([(0.02, ly - 0.04, 1.0)], 0.03) * lua * 1.5
    cai = rel(t, 0.28, 0.75)
    if 0 < cai < 1:
        for k, x in enumerate((-0.35, 0.0, 0.35)):
            u = rel(cai, 0.08 * k, 0.6 + 0.08 * k)
            if 0 < u < 1:
                desce = ease_in(min(1, u * 3), 2)
                y1 = -0.5 + 0.95 * desce
                C = T.lines([(x, -0.5, x, y1, 1.0)], 0.06 * (1 - u) + 0.02)
                G += C * 0.8 + T.blur(C, 0.03) * 0.6
                H += T.lines([(x, -0.5, x, y1, 1.0)], 0.012) * (1 - u) * 1.5
                if desce >= 1:
                    G += T.ring(0.05 + 0.2 * u, 0.02, x, 0.45, squash=3.0) * (1 - u) * 1.3
    hiero = pulso(t, 0.3, 0.95)
    if hiero > 0:
        G += T.ring(0.6, 0.012, 0, 0.45, squash=3.5) * hiero
        simbolos = []
        for k in range(10):
            a = t * 2 + TAU * k / 10
            x, y = 0.6 * math.cos(a), 0.45 + 0.6 * math.sin(a) / 3.5
            s = 0.035
            if k % 3 == 0:
                simbolos += [(x - s, y, x + s, y, 1.0), (x, y - s, x, y + s, 1.0)]
            elif k % 3 == 1:
                simbolos += _contorno([(x - s, y + s), (x, y - s), (x + s, y + s)])
            else:
                simbolos += [(x - s, y - s, x - s, y + s, 1.0), (x - s, y + s, x + s, y + s, 1.0)]
        G += T.lines(simbolos, 0.008) * hiero * 1.1
    return G * env, H * env


# =================================================================== Tempestade
def rajada_de_vento(T, t, rng):
    """A rajada de vento: as correntes de ar atravessam o campo em faixas curvas da esquerda para a direita, com as
    folhas e a poeira levadas junto, e ficam os redemoinhos pequenos girando (Lento)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k in range(6):
        t0 = 0.03 * k
        u = rel(t, t0, t0 + 0.45)
        if 0 < u < 1:
            y = -0.5 + 0.2 * k
            cab = -1.0 + 2.2 * ease_out(u, 1.6)
            cau = cab - 0.7
            pts = [(cau + (cab - cau) * j / 20, y + 0.06 * math.sin((cau + (cab - cau) * j / 20) * 5 + k)) for j in range(21)]
            G += T.polyline(pts, 0.012 + 0.006 * (k % 2)) * math.sin(math.pi * u) * 1.2
    q = np.random.default_rng(7)
    u = rel(t, 0.05, 0.7)
    if 0 < u < 1:
        shapes = []
        for k in range(9):
            x = -1.0 + 2.2 * ease_out(min(1, u * q.uniform(0.9, 1.3)), 1.5)
            y = q.uniform(-0.5, 0.5) + 0.08 * math.sin(u * 10 + k)
            shapes.append((lamina(x - 0.04, y, x + 0.04, y + 0.01, 0.025), math.sin(math.pi * u)))
        G += T.polys(shapes) * 0.9
        H += T.splats([(-1.0 + 2.2 * ease_out(min(1, u * q.uniform(0.8, 1.2)), 1.5), q.uniform(-0.5, 0.5), 0.5) for _ in range(20)], 0.01) * math.sin(math.pi * u)
    fica = pulso(t, 0.4, 1.0)
    if fica > 0:
        for k, (x, y) in enumerate(((-0.35, 0.3), (0.0, 0.32), (0.35, 0.3))):
            G += T.arc_band(0.1, 0.02, t * 12 + k, t * 12 + k + 4.2, squash=0.5, cx=x, cy=y, taper=0.6) * fica * 1.1
    return G * env, H * env


def relampago_em_cadeia(T, t, rng):
    """O relâmpago em cadeia: o raio cai do alto no primeiro rival e salta de um em um (os três pontos),
    ramificando, cada ponto estalando com o clarão (Lento)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    pontos = [(-0.45, 0.15), (0.05, -0.1), (0.5, 0.15)]
    q = np.random.default_rng(int(t * 24) % 9 + 11)
    cai = rel(t, 0.05, 0.12)
    if cai > 0 and t < 0.5:
        a = pontos[0]
        R = T.polyline(jagged(q, a[0] - 0.1, -1.0, a[0], -1.0 + (a[1] + 1.0) * min(1, cai), 5, 0.16), 0.016)
        G += (R * 1.4 + T.blur(R, 0.02) * 0.8) * (1 - rel(t, 0.3, 0.5))
        H += R * 0.7
    for k in range(2):
        t0 = 0.14 + 0.1 * k
        u = rel(t, t0, t0 + 0.06)
        if u > 0 and t < 0.6:
            a, b = pontos[k], pontos[k + 1]
            x = a[0] + (b[0] - a[0]) * min(1, u)
            y = a[1] + (b[1] - a[1]) * min(1, u)
            R = T.polyline(jagged(q, a[0], a[1], x, y, 5, 0.2), 0.014)
            some = 1 - rel(t, t0 + 0.2, t0 + 0.4)
            G += (R * 1.4 + T.blur(R, 0.02) * 0.8) * some
            H += R * 0.7 * some
            if u >= 1:
                for j in range(2):
                    m = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                    G += T.polyline(jagged(q, m[0], m[1], m[0] + q.uniform(-0.2, 0.2), m[1] + q.uniform(0.1, 0.3), 3, 0.3), 0.007) * some
    for k, (px, py) in enumerate(pontos):
        c = pulso(t, 0.1 + 0.1 * k, 0.4 + 0.1 * k)
        if c > 0:
            H += T.gauss(px, py, 0.06) * c * 1.8 + T.flare(px, py, 0.5 * c, 0.3, 0.01) * c
            G += T.ring(0.08 + 0.15 * c, 0.015, px, py) * c
    return G * env, H * env


def _nuvens(T, cx, cy, r0, r1, n, seed, giro, sq=0.45, bracos=0, aperta=1.0):
    """Os tufos de nuvem de tempestade: muitos tufos redondos de tamanhos diferentes num anel (r0→r1) ou em bracos
    de espiral; o miolo fica escuro e só o contorno de cada tufo brilha."""
    q = np.random.default_rng(seed)
    pts = []
    for k in range(n):
        u = q.uniform(0, 1)
        r = r0 + (r1 - r0) * u
        if bracos:
            a = giro + TAU * (k % bracos) / bracos + aperta * 3.0 * u
        else:
            a = giro + q.uniform(0, TAU)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * sq, q.uniform(0.05, 0.11)))
    N = T.zero()
    for x, y, sg in pts:
        N = np.maximum(N, T.gauss(x, y, sg))
    N = np.clip(N * 1.6, 0, 1)
    return N * (0.75 + 0.25 * np.clip(T.noise(np.random.default_rng(seed), 0.25, 2) + 0.5, 0, 1))


def tempestade_preparo(T, t, rng):
    """O Preparo do Olho da tempestade: os olhos brancos acesos, as nuvens girando em espiral em volta e os raios
    curtos piscando dentro delas (laço)."""
    G, H = vazio(T)
    giro = TAU * t / 2
    N = _nuvens(T, 0, -0.05, 0.18, 0.75, 80, 21, giro, 0.55, 3)
    G += N * 0.3 + _borda(T, N, 0.02) * 1.5
    for lado in (-1, 1):
        H += T.gauss(0.07 * lado, -0.05, 0.025) * 1.8 + T.lines([(0.07 * lado - 0.05, -0.05, 0.07 * lado + 0.05, -0.05, 1.0)], 0.008) * 1.2
    q = np.random.default_rng(int(t * 12) % 7 + 30)
    if (t * 6) % 1 < 0.4:
        a = q.uniform(0, TAU)
        x, y = 0.5 * math.cos(a), -0.1 + 0.22 * math.sin(a)
        R = T.polyline(jagged(q, x, y, x + q.uniform(-0.15, 0.15), y + 0.25, 4, 0.3), 0.01)
        G += R * 1.3
        H += R * 0.8
    return G, H


def olho_da_tempestade(T, t, rng):
    """O olho da tempestade: o anel de nuvens gira com o olho calmo e claro no meio, os raios descem do anel sobre
    o rival em sequência e o vento corre em volta (Eletrificado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    forma = ease_out(rel(t, 0.0, 0.3), 2)
    giro = t * 6
    if forma > 0:
        N = _nuvens(T, 0, -0.55, 0.28 * forma + 0.02, 0.85 * forma + 0.05, 110, 41, giro, 0.42, 4, 0.6)
        b = 1 - rel(t, 0.75, 0.9)
        G += (N * 0.3 + _borda(T, N, 0.02) * 1.5) * b
        H += T.gauss(0, -0.55, 0.08 * forma) * 0.5
    q = np.random.default_rng(int(t * 20) % 9 + 50)
    for k in range(5):
        t0 = 0.3 + 0.07 * k
        u = rel(t, t0, t0 + 0.15)
        if 0 < u < 1:
            a = TAU * k / 5 + 0.4
            x0 = 0.5 * math.cos(a)
            alvo = (0.12 * math.cos(a * 2), 0.05)
            R = T.polyline(jagged(q, x0, -0.55 + 0.2 * math.sin(a), alvo[0], alvo[1], 5, 0.18), 0.016)
            G += (R * 1.4 + T.blur(R, 0.02) * 0.7) * (1 - u)
            H += R * 0.8 * (1 - u) + T.gauss(alvo[0], alvo[1], 0.07) * (1 - u) * 1.3
    vento = pulso(t, 0.25, 0.95)
    if vento > 0:
        for k in range(3):
            G += T.arc_band(0.35 + 0.1 * k, 0.025, giro + k * 2, giro + k * 2 + 2.2, squash=0.4, cx=0, cy=0.15, taper=0.5) * vento * 0.9
    return G * env, H * env


# =================================================================== Jean Grey
def _hexagono(cx, cy, r, ang=0.0):
    return [(cx + r * math.cos(ang + TAU * k / 6), cy + r * math.sin(ang + TAU * k / 6)) for k in range(6)]


def escudo_mental(T, t, rng):
    """O escudo mental: as ondas de pensamento sobem da cabeça do aliado, a cúpula rosa de força psíquica se fecha
    em volta dele com os hexágonos da mente brilhando e pulsa uma vez (Protegido + escudo)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    ondas = rel(t, 0.0, 0.5)
    if 0 < ondas < 1:
        for k in range(3):
            u = rel(ondas, 0.15 * k, 0.6 + 0.15 * k)
            if 0 < u < 1:
                G += T.arc_band(0.08 + 0.3 * u, 0.02, -math.pi * 0.85, -math.pi * 0.15, cx=0, cy=-0.25, crescente=True) * (1 - u) * 1.3
    fecha = ease_out(rel(t, 0.2, 0.5), 3)
    if fecha > 0:
        r = 0.55
        D = T.arc_band(r, 0.035, math.pi, math.pi + math.pi * fecha, cx=0, cy=0.3, taper=0.2) + T.arc_band(r, 0.035, 0.0, -math.pi * fecha, cx=0, cy=0.3, taper=0.2)
        b = 1 - rel(t, 0.8, 0.95)
        G += D * 1.2 * b
        dentro = T.gauss(0, 0.05, 0.4) * fecha * 0.25 * b
        G += dentro
        shapes = []
        for k in range(9):
            a = math.pi + math.pi * (k + 0.5) / 9
            if (k + 0.5) / 9 <= fecha:
                shapes += _contorno(_hexagono(0.42 * math.cos(a), 0.3 + 0.42 * math.sin(a), 0.07, 0.0))
        G += T.lines(shapes, 0.008) * b * 0.9
    pulsa = pulso(t, 0.5, 0.75)
    H += T.ring(0.55 + 0.1 * pulsa, 0.03, 0, 0.3) * pulsa * 0.8
    return G * env, H * env


def muralha_telecinetica(T, t, rng):
    """A muralha telecinética: a parede translúcida se ergue na frente do aliado (de baixo para cima), as ondas
    rosa correm nela e os destroços que vinham param no ar presos pelo contorno, tremendo (Protegido + escudo)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sobe = ease_out(rel(t, 0.0, 0.3), 3)
    b = 1 - rel(t, 0.8, 0.95)
    if sobe > 0:
        x = 0.35
        topo = 0.55 - 1.25 * sobe
        P = T.polys([([(x - 0.09, 0.55), (x + 0.09, 0.55), (x + 0.06, topo), (x - 0.06, topo)], 1.0)])
        G += (P * 0.3 + _borda(T, P, 0.01) * 1.4) * b
        for k in range(4):
            y = 0.5 - ((t * 1.6 + k / 4) % 1) * (0.5 - topo)
            G += T.ring(0.08, 0.008, x, y, squash=0.6) * P * 2.5 * b
        H += T.lines([(x, 0.5, x, topo, 1.0)], 0.01) * b * 0.8
    para = rel(t, 0.15, 0.4)
    if para > 0:
        q = np.random.default_rng(61)
        for k in range(5):
            y = -0.35 + 0.18 * k
            x = 0.9 - 0.45 * ease_out(min(1, para * q.uniform(1.0, 1.5)), 3)
            tr = 0.008 * math.sin(t * 60 + k) * (para >= 1)
            pedra = _gira([(q.uniform(0.03, 0.06) * math.cos(a), q.uniform(0.03, 0.06) * math.sin(a)) for a in np.linspace(0, TAU, 6, endpoint=False)], k + t, x + tr, y)
            S = T.polys([(pedra, 1.0)])
            G += (S * 0.5 + _borda(T, S, 0.005)) * b
            if para >= 1:
                G += T.lines(_contorno(_gira([(0.09 * math.cos(a), 0.09 * math.sin(a)) for a in np.linspace(0, TAU, 10, endpoint=False)], 0, x, y)), 0.006) * b * 0.9
    return G * env, H * env


def _asas(T, t, cx, cy, abre, escala, seed):
    """As asas da Fênix: as penas de fogo em leque dos dois lados, cada pena uma língua de chama."""
    G = T.zero()
    for lado in (-1, 1):
        for k in range(7):
            a = -math.pi / 2 + lado * (0.35 + 1.25 * abre * k / 6)
            L = escala * (0.45 + 0.35 * math.sin(math.pi * (k + 1) / 8))
            F = _chamas(T, t, cx + lado * 0.05 * escala, cy, 0.02 * escala, L, 2, seed + k + (lado > 0) * 10, a)
            G += F
    return G


def fenix_preparo(T, t, rng):
    """O Preparo da Fênix: o fogo sobe em volta da Jean e desenha as asas abertas da ave, e os olhos acendem
    (laço)."""
    G, H = vazio(T)
    abre = 0.75 + 0.25 * math.sin(TAU * t)
    A = _asas(T, t, 0, 0.0, abre, 1.0, 70)
    G += A * 0.6 + _borda(T, np.clip(A, 0, 1), 0.01) * 1.0
    C = _chamas(T, t, 0, 0.45, 0.25, 0.4, 6, 80)
    G += C * 0.5
    for lado in (-1, 1):
        H += T.gauss(0.06 * lado, -0.05, 0.02) * 1.6
    H += T.gauss(0, 0, 0.1) * 0.5 * abre
    return G, H


def fenix_desperta(T, t, rng):
    """A Fênix desperta: a ave de fogo abre as asas gigantes no alto e mergulha, a explosão de chamas varre o campo
    em leque e os choques psíquicos travam todo mundo (Paralisado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.25), 2.5)
    desce = ease_in(rel(t, 0.25, 0.42), 2)
    if abre > 0 and t < 0.5:
        cy = -0.45 + 0.45 * desce
        esc = 1.2 - 0.4 * desce
        A = _asas(T, t, 0, cy, abre, esc, 90)
        some = 1 - rel(t, 0.42, 0.5)
        G += (A * 0.6 + _borda(T, np.clip(A, 0, 1), 0.012) * 1.1) * some
        corpo = [(0, cy - 0.12 * esc), (0.05 * esc, cy), (0, cy + 0.25 * esc), (-0.05 * esc, cy)]
        G += T.polys([(corpo, 1.0)]) * some * 0.9
        H += T.gauss(0, cy, 0.08) * some * 1.4
    bum = rel(t, 0.4, 0.92)
    if 0 < bum < 1:
        e = ease_out(bum, 3)
        for k in range(14):
            a = -math.pi + math.pi * k / 13
            F = _chamas(T, t, 0.0, 0.1, 0.025, 0.2 + 0.7 * e, 2, 100 + k, a)
            G += F * (1 - bum) * 0.9
        G += T.ring(0.1 + 0.8 * e, 0.04, 0, 0.1, squash=1.6) * (1 - bum) * 1.3
        H += T.gauss(0, 0.05, 0.15 + 0.2 * e) * (1 - bum) ** 2 * 2.0
    trava = pulso(t, 0.6, 1.0)
    if trava > 0:
        q = np.random.default_rng(int(t * 25) % 6 + 110)
        for x in (-0.45, 0.0, 0.45):
            G += T.ring(0.12, 0.01, x, 0.1) * trava * 0.9
            G += T.polyline(jagged(q, x - 0.1, 0.0, x + 0.1, 0.2, 4, 0.4), 0.01) * trava * 1.1
    return G * env, H * env


# =================================================================== Vampira
def forca_roubada(T, t, rng):
    """A força roubada: a Vampira chega voando (as linhas de velocidade) com o punho envolto na aura verde-amarela da
    força roubada, acerta em cheio e o Preparo do rival quebra em cacos."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    vai = ease_in(rel(t, 0.0, 0.25), 2)
    if t < 0.4:
        some = 1 - rel(t, 0.3, 0.4)
        x = -0.85 + 0.75 * vai
        for k in range(6):
            y = -0.15 + 0.06 * k
            G += T.tapered([(x - 0.5, y, x - 0.12, y, 1.0)], 0.012) * some * 0.8
        aura = T.gauss(x, 0, 0.1) * 0.8 + T.ring(0.12 + 0.02 * math.sin(t * 50), 0.02, x, 0)
        G += aura * some
        H += T.gauss(x, 0, 0.06) * some * 1.2
        punho = [(x - 0.08, -0.06), (x + 0.07, -0.07), (x + 0.1, 0.0), (x + 0.07, 0.07), (x - 0.08, 0.06)]
        P = T.polys([(punho, 1.0)])
        G += (P * 0.6 + _borda(T, P, 0.006) * 1.3) * some
    bate = rel(t, 0.25, 0.6)
    if 0 < bate < 1:
        e = ease_out(bate, 3)
        H += T.gauss(0, 0, 0.08 + 0.1 * e) * (1 - bate) ** 2 * 2.0
        G += T.ring(0.08 + 0.4 * e, 0.03, 0, 0) * (1 - bate) * 1.3
        q = np.random.default_rng(71)
        cacos = []
        for k in range(10):
            a = q.uniform(0, TAU)
            d = 0.1 + 0.45 * e * q.uniform(0.6, 1)
            cx, cy = d * math.cos(a), d * math.sin(a) - 0.2 + 0.4 * bate * bate
            cacos.append((_gira([(-0.035, -0.02), (0.04, -0.01), (0.0, 0.035)], a + bate * 6, cx, cy), 1 - bate))
        G += T.polys(cacos) * 1.1
    return G * env, H * env


def memoria_preparo(T, t, rng):
    """O Preparo da Memória emprestada: a mecha branca do cabelo brilha e os fragmentos de memória (os cacos com os
    poderes dos outros dentro: a garra, o raio, o floco) giram em volta dela (laço)."""
    G, H = vazio(T)
    mecha = [(-0.08 + 0.02 * math.sin(t * TAU + j * 0.4), -0.45 + 0.07 * j) for j in range(8)]
    G += T.polyline(mecha, 0.03) * 1.1
    H += T.polyline(mecha, 0.012) * (0.6 + 0.4 * math.sin(TAU * t * 2))
    for k in range(3):
        a = TAU * t / 3 + TAU * k / 3
        x, y = 0.5 * math.cos(a), 0.05 + 0.32 * math.sin(a)
        caco = _gira([(-0.12, -0.1), (0.1, -0.12), (0.13, 0.08), (-0.08, 0.12)], a * 0.3, x, y)
        G += T.lines(_contorno(caco), 0.01) * 1.1
        if k == 0:
            G += T.lines([(x - 0.05 + 0.04 * j, y - 0.07, x - 0.03 + 0.04 * j, y + 0.07, 1.0) for j in range(3)], 0.008)
        elif k == 1:
            G += T.polyline([(x - 0.04, y - 0.08), (x + 0.02, y - 0.01), (x - 0.02, y + 0.01), (x + 0.04, y + 0.08)], 0.009)
        else:
            G += T.lines([(x + 0.07 * math.cos(b), y + 0.07 * math.sin(b), x - 0.07 * math.cos(b), y - 0.07 * math.sin(b), 1.0) for b in (0, 1.05, 2.1)], 0.007)
        H += T.gauss(x, y, 0.05) * 0.35
    return G, H


def memoria_emprestada(T, t, rng):
    """A memória emprestada: os poderes copiados piscam um atrás do outro no rival (as três garras, o raio e o gelo)
    e se juntam num golpe só, com a aura verde subindo nela (Fortalecido)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(int(t * 24) % 7 + 120)
    g = pulso(t, 0.05, 0.28)
    if g > 0:
        for k in range(3):
            p = ease_out(rel(t, 0.05 + 0.02 * k, 0.17 + 0.02 * k), 3)
            ini = rel(t, 0.18, 0.28)
            if p > 0 and ini < 1:
                L = T.polys([(lamina(-0.3 + 0.12 * k, -0.35, 0.0 + 0.12 * k, 0.3, 0.025, prog=p, inicio=ini), 1.0)])
                G += L * 1.4
                H += L * 0.5
    r = pulso(t, 0.22, 0.42)
    if r > 0:
        R = T.polyline(jagged(q, -0.1, -0.8, 0.0, 0.0, 5, 0.18), 0.016)
        G += (R * 1.4 + T.blur(R, 0.02) * 0.7) * r
        H += R * r * 0.9
    gelo = pulso(t, 0.38, 0.6)
    if gelo > 0:
        shapes = []
        for k in range(7):
            a = TAU * k / 7
            shapes.append((_gira([(0, -0.03), (0.22 * gelo, 0), (0, 0.03)], a), 1.0))
        P = T.polys(shapes)
        G += P * 0.6 * gelo + _borda(T, P, 0.006) * gelo * 1.3
    junta = rel(t, 0.55, 0.9)
    if 0 < junta < 1:
        e = ease_out(junta, 3)
        G += T.ring(0.05 + 0.5 * e, 0.035, 0, 0) * (1 - junta) * 1.3
        H += T.gauss(0, 0, 0.08 + 0.15 * e) * (1 - junta) ** 2 * 2.0
        raios = [(0.06 * math.cos(a), 0.06 * math.sin(a), (0.25 + 0.5 * e) * math.cos(a), (0.25 + 0.5 * e) * math.sin(a), 1 - junta) for a in np.linspace(0, TAU, 12, endpoint=False)]
        G += T.tapered(raios, 0.025)
    aura = pulso(t, 0.6, 1.0)
    if aura > 0:
        A = _chamas(T, t, -0.7, 0.35, 0.12, 0.45, 5, 130)
        G += A * aura * 0.7
    return G * env, H * env


# =================================================================== Gambit
def _carta(cx, cy, s, ang):
    return _gira([(-0.055 * s, -0.08 * s), (0.055 * s, -0.08 * s), (0.055 * s, 0.08 * s), (-0.055 * s, 0.08 * s)], ang, cx, cy)


def _copas(cx, cy, s, ang):
    pts = []
    for a in np.linspace(0, TAU, 30, endpoint=False):
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((x * s / 17, y * s / 17))
    return _gira(pts, ang, cx, cy)


def _desenha_carta(T, cx, cy, s, ang, brilho=1.0):
    """A carta carregada: o contorno branco, o naipe de copas no meio e o brilho rosa de energia cinética."""
    C = T.polys([(_carta(cx, cy, s, ang), 1.0)])
    G = C * 0.35 + _borda(T, C, 0.006) * 1.3
    G += T.polys([(_copas(cx, cy, 0.03 * s, ang), 1.0)]) * 0.9
    H = T.gauss(cx, cy, 0.07 * s) * 0.9 * brilho + _borda(T, C, 0.012) * 0.6 * brilho
    return G, H


def carta_carregada(T, t, rng):
    """A carta carregada: a carta acende rosa na mão (a energia cinética tremendo em volta), voa girando, gruda no
    rival e fica tiquetaqueando com os pulsos (Marcado + Bomba)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    carga = pulso(t, 0.0, 0.25)
    if carga > 0:
        g, h = _desenha_carta(T, -0.72, 0.0, 2.0, 0.3, carga * 1.5)
        G += g * carga
        H += h * carga
        q = np.random.default_rng(int(t * 30) % 7 + 140)
        for k in range(4):
            a = q.uniform(0, TAU)
            G += T.polyline(jagged(q, -0.75 + 0.1 * math.cos(a), 0.1 * math.sin(a), -0.75 + 0.2 * math.cos(a), 0.2 * math.sin(a), 3, 0.4), 0.007) * carga
    voa = rel(t, 0.2, 0.38)
    if 0 < voa < 1:
        x = -0.75 + 0.75 * ease_in(voa, 1.3)
        g, h = _desenha_carta(T, x, -0.05 * math.sin(math.pi * voa), 1.9, t * 30, 1.2)
        G += g
        H += h
        H += T.tapered([(x - 0.35, 0, x - 0.05, 0, 1.0)], 0.02) * 0.8
    if t >= 0.38:
        tic = 0.5 + 0.5 * math.cos(TAU * (t - 0.38) * 6)
        b = 1 - rel(t, 0.85, 0.95)
        g, h = _desenha_carta(T, 0.02, 0.0, 1.9, 0.4, tic * 1.5)
        G += g * b
        H += h * b
        G += T.ring(0.2 + 0.1 * ((t * 6) % 1), 0.012, 0.02, 0) * (1 - (t * 6) % 1) * b
    return G * env, H * env


def baralho_explosivo(T, t, rng):
    """O baralho explosivo: o leque de cinco cartas sai da mão, se abre no ar em arco e as cartas explodem em fila
    no rival, cada uma num estouro rosa (Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for k in range(5):
        t0 = 0.05 + 0.03 * k
        u = rel(t, t0, t0 + 0.28)
        alvo = (-0.15 + 0.075 * k, -0.1 + 0.05 * k)
        if 0 < u < 1:
            e = ease_in(u, 1.2)
            leque = (k - 2) * 0.3
            x = -0.8 + (alvo[0] + 0.8) * e
            y = alvo[1] * e + leque * math.sin(math.pi * e) * 0.6
            g, h = _desenha_carta(T, x, y, 1.6, leque + t * 18, 1.0)
            G += g
            H += h
        b = rel(t, t0 + 0.28, t0 + 0.55)
        if 0 < b < 1:
            e = ease_out(b, 3)
            G += T.ring(0.04 + 0.2 * e, 0.025, alvo[0], alvo[1]) * (1 - b) * 1.2
            H += T.gauss(alvo[0], alvo[1], 0.05 + 0.08 * e) * (1 - b) ** 2 * 2.0
            raios = [(alvo[0] + 0.04 * math.cos(a), alvo[1] + 0.04 * math.sin(a), alvo[0] + (0.1 + 0.15 * e) * math.cos(a), alvo[1] + (0.1 + 0.15 * e) * math.sin(a), 1 - b) for a in np.linspace(0, TAU, 8, endpoint=False)]
            G += T.tapered(raios, 0.016)
    return G * env, H * env


def gambit_preparo(T, t, rng):
    """O Preparo do Bastão cinético: as cartas sendo embaralhadas em cascata de uma mão para a outra, cada uma
    acendendo rosa na passagem, e os olhos vermelhos brilhando em cima (laço)."""
    G, H = vazio(T)
    for k in range(8):
        u = (t * 2 + k / 8) % 1
        x = -0.3 + 0.6 * u
        y = 0.15 - 0.3 * math.sin(math.pi * u)
        g, h = _desenha_carta(T, x, y, 1.4, -0.6 + 1.2 * u, math.sin(math.pi * u))
        G += g * 0.9
        H += h * 0.8
    for lado in (-1, 1):
        H += T.gauss(0.07 * lado, -0.4, 0.022) * 1.8
        G += T.gauss(0.07 * lado, -0.4, 0.035) * 0.5
    return G, H


def bastao_cinetico(T, t, rng):
    """O bastão cinético: o bastão carregado gira no alto (o disco de brilho rosa), desce e bate no chão; a onda
    cinética corre pelo chão e detona as cartas espalhadas em volta do rival (Lento)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    gira = pulso(t, 0.0, 0.32)
    if gira > 0:
        a = t * 40
        cx, cy = -0.3, -0.45
        G += T.lines([(cx - 0.35 * math.cos(a), cy - 0.35 * math.sin(a) * 0.4, cx + 0.35 * math.cos(a), cy + 0.35 * math.sin(a) * 0.4, 1.0)], 0.022) * gira * 1.2
        G += T.ring(0.35, 0.03, cx, cy, squash=2.5) * gira * 0.6
        H += T.gauss(cx + 0.35 * math.cos(a), cy + 0.14 * math.sin(a), 0.03) * gira * 1.4 + T.gauss(cx - 0.35 * math.cos(a), cy - 0.14 * math.sin(a), 0.03) * gira * 1.4
    desce = rel(t, 0.25, 0.35)
    if 0 < desce < 1:
        a = -1.2 + 1.2 * ease_in(desce, 2)
        G += T.lines([(-0.3, 0.45, -0.3 + 0.9 * math.cos(a - 1.57 + 1.57), 0.45 + 0.9 * math.sin(a), 1.0)], 0.022) * 1.2
    chao = rel(t, 0.33, 0.8)
    if 0 < chao < 1:
        e = ease_out(chao, 2)
        G += T.ring(0.05 + 0.8 * e, 0.02, -0.1, 0.45, squash=4.0) * (1 - chao) * 1.4
        H += T.gauss(-0.1, 0.45, 0.06) * (1 - chao) * 1.5
    cartas = [(-0.5, 0.0), (-0.2, -0.25), (0.15, 0.15), (0.4, -0.2), (0.55, 0.2)]
    for k, (x, y) in enumerate(cartas):
        tb = 0.4 + 0.06 * k
        if t < tb:
            g, h = _desenha_carta(T, x, y, 1.4, k * 0.8, 0.5 + 0.5 * math.sin(t * 30 + k))
            G += g * min(1, t * 6)
            H += h * min(1, t * 6)
        b = rel(t, tb, tb + 0.3)
        if 0 < b < 1:
            e = ease_out(b, 3)
            G += T.ring(0.04 + 0.22 * e, 0.025, x, y) * (1 - b) * 1.2
            H += T.gauss(x, y, 0.05 + 0.1 * e) * (1 - b) ** 2 * 2.0
    return G * env, H * env


REGISTRO = [
    ("manto_lunar", manto_lunar, GRANDE, "Cavaleiro da Lua · a capa, as faixas e o olho de Khonshu", False),
    ("crescente_de_prata", crescente_de_prata, GRANDE, "Cavaleiro da Lua · os três dardos em meia-lua", False),
    ("khonshu_preparo", khonshu_preparo, MEDIA, "Cavaleiro da Lua · as fases da lua e o ankh (Preparo, laço)", True),
    ("julgamento_de_khonshu", julgamento_de_khonshu, GRANDE, "Cavaleiro da Lua · a lua, Khonshu e as colunas de luar", False),
    ("rajada_de_vento", rajada_de_vento, GRANDE, "Tempestade · as correntes de vento e os redemoinhos", False),
    ("relampago_em_cadeia", relampago_em_cadeia, GRANDE, "Tempestade · o raio saltando de um em um", False),
    ("tempestade_preparo", tempestade_preparo, MEDIA, "Tempestade · os olhos brancos e as nuvens (Preparo, laço)", True),
    ("olho_da_tempestade", olho_da_tempestade, GRANDE, "Tempestade · o anel de nuvens e os raios", False),
    ("escudo_mental", escudo_mental, GRANDE, "Jean Grey · a cúpula psíquica e os hexágonos", False),
    ("muralha_telecinetica", muralha_telecinetica, GRANDE, "Jean Grey · a parede e os destroços parados", False),
    ("fenix_preparo", fenix_preparo, MEDIA, "Jean Grey · as asas de fogo (Preparo, laço)", True),
    ("fenix_desperta", fenix_desperta, GRANDE, "Jean Grey · a Fênix mergulha e a explosão", False),
    ("forca_roubada", forca_roubada, GRANDE, "Vampira · o soco com a força roubada", False),
    ("memoria_preparo", memoria_preparo, MEDIA, "Vampira · a mecha branca e as memórias (Preparo, laço)", True),
    ("memoria_emprestada", memoria_emprestada, GRANDE, "Vampira · os poderes copiados em fila", False),
    ("carta_carregada", carta_carregada, GRANDE, "Gambit · a carta carregada que gruda", False),
    ("baralho_explosivo", baralho_explosivo, GRANDE, "Gambit · o leque de cartas que explode", False),
    ("gambit_preparo", gambit_preparo, MEDIA, "Gambit · as cartas embaralhando (Preparo, laço)", True),
    ("bastao_cinetico", bastao_cinetico, GRANDE, "Gambit · o bastão, a onda e as cartas detonando", False),
]
