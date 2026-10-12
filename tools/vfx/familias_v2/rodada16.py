"""Rodada 16 das habilidades próprias: Ultron, Duende Verde, Surfista Prateado, Galactus e Senhor das Estrelas.

Ultron
- analise_preditiva: o olho vermelho de varredura abre sobre o rival, os colchetes de mira travam, as linhas de
  dados correm pelo contorno dele e as setas de Enfraquecido descem.
- drones_de_defesa: três drones triangulares saem voando até os aliados e abrem cada um um escudo de hexágonos;
  um deles dispara o raio no rival.
- ultron_preparo: o Preparo da Evolução autônoma — o rosto de metal do Ultron (o queixo pontudo, os olhos e a
  boca acesos em vermelho) com os circuitos pulsando em volta (laço).
- evolucao_autonoma: os circuitos vermelhos se reescrevem (as trilhas que mudam de caminho), o raio sai do peito
  e corta o Preparo do rival em pedaços.

Duende Verde
- bomba_abobora: a bomba de abóbora com a cara recortada voa em arco, ri (a boca acesa) e explode em verde e
  laranja, com a fumaça que cega.
- gas_do_duende: as nuvens de gás verde rolam por cima dos rivais com as caras assustadoras se formando nelas
  (Confuso e Envenenado).
- duende_preparo: o Preparo da Prancha armadilhada — o planador de asas de morcego pairando com os jatos
  acesos embaixo (laço).
- prancha_armadilhada: o planador vem em rasante, as lâminas saem das asas, corta o rival e a carga explode.

Surfista Prateado
- rajada_cosmica: o raio prateado sai da mão cheio de estrelinhas, e a marca cósmica fica no rival.
- transmutacao_estelar: as partículas prateadas giram e viram uma casca brilhante em cada aliado, com o rastro
  que os empurra para a frente (Escudo e adianta a vez).
- surfista_preparo: o Preparo do Surfe dimensional — a prancha prateada com o rastro cósmico ondulando e a
  aura das estrelas (laço).
- surfe_dimensional: a prancha atravessa o campo rasgando o espaço (a fenda brilhante que fica atrás dela) e
  acerta o rival em cheio.

Galactus
- dreno_planetario: o rival vira um planeta (o globo com os anéis de órbita) e a energia dele sobe em espiral
  até a mão enorme do Galactus, que se fecha.
- rajada_do_poder_cosmico: o elmo do Galactus (as duas abas altas e a fenda dos olhos) surge no alto e o Poder
  Cósmico desce em colunas largas sobre os rivais.
- devorador_preparo: o Preparo do Toque do Devorador — as mãos enormes do Galactus abertas sobre o campo e a
  energia sendo sugada para o centro (laço).

Senhor das Estrelas
- plano_improvisado: a fita cassete gira (os dois carretéis), as notas de música saem e as setas de Acelerado
  sobem no trio; o tiro rápido acerta o rival.
- danca_de_distracao: a pista de dança acende em quadrados coloridos, as notas pulam e os rivais ficam
  tontos, olhando a dança (Confuso).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .rodada13 import _borda, _contorno, _gira, _setas_para_baixo


def _hexagono(cx, cy, r, ang=0.0):
    return [(cx + r * math.cos(ang + TAU * k / 6), cy + r * math.sin(ang + TAU * k / 6)) for k in range(6)]


def _escudo_hex(T, cx, cy, r, u):
    """O escudo de hexágonos: a bolha com as células acendendo do centro para fora."""
    linhas = []
    for k in range(7):
        if k == 0:
            hx, hy = cx, cy
        else:
            a = TAU * (k - 1) / 6
            hx, hy = cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a)
        if k == 0 or u > 0.3 + 0.1 * k:
            linhas += _contorno(_hexagono(hx, hy, r * 0.3, math.pi / 6))
    return T.ring(r, 0.02, cx, cy) * 1.2 + T.lines(linhas, 0.008)


# =================================================================== Ultron
def analise_preditiva(T, t, rng):
    """A análise preditiva: o olho vermelho de varredura abre sobre o rival, os colchetes de mira fecham e travam, as
    linhas de dados correm pelo contorno dele e as setas de Enfraquecido descem."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.2), 3)
    if abre > 0:
        ey = -0.55
        olho = [(0.3 * math.cos(a), ey + 0.12 * abre * math.sin(a)) for a in np.linspace(0, TAU, 40)]
        G += T.polyline(olho, 0.014) * (1 - rel(t, 0.75, 0.9)) * 1.2
        ix = 0.08 * math.sin(t * 6)
        G += T.ring(0.06 * abre + 0.005, 0.012, ix, ey) * 1.3 + T.gauss(ix, ey, 0.03 * abre + 0.005) * 0.9
        H += T.gauss(ix, ey, 0.04 * abre + 0.005) * 1.8
        var = (t * 1.5) % 1
        G += T.lines([(-0.45, -0.4 + 0.8 * var, 0.45, -0.4 + 0.8 * var, 1.0)], 0.01) * (1 - rel(t, 0.5, 0.65)) * 1.2
    trava = ease_out(rel(t, 0.15, 0.35), 3)
    if trava > 0 and t < 0.85:
        s = 0.5 - 0.22 * trava
        for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            G += T.lines([(sx * s, sy * s, sx * s - sx * 0.1, sy * s, 1.0), (sx * s, sy * s, sx * s, sy * s - sy * 0.1, 1.0)], 0.016) * 1.3
        if trava >= 1:
            H += T.ring(0.06, 0.01, 0, 0) * pulso(t, 0.35, 0.6) * 1.5
    dados = pulso(t, 0.3, 0.8)
    if dados > 0:
        q = np.random.default_rng(5)
        for k in range(8):
            y = -0.3 + 0.08 * k
            x0 = -0.3 + 0.6 * ((t * 2 + q.uniform(0, 1)) % 1)
            G += T.lines([(x0, y, x0 + q.uniform(0.04, 0.12), y, 1.0)], 0.008) * dados
    seta = rel(t, 0.55, 0.95)
    if 0 < seta < 1:
        G += _setas_para_baixo(T, seta, xs=(-0.3, 0.3), y0=0.0) * 1.1
    return G * env, H * env


def _drone(T, cx, cy, s, ang):
    tri = _gira([(0.07 * s, 0), (-0.05 * s, -0.045 * s), (-0.03 * s, 0), (-0.05 * s, 0.045 * s)], ang, cx, cy)
    D = T.polys([(tri, 1.0)])
    return D * 0.6 + _borda(T, D, 0.005) * 1.2, T.gauss(cx, cy, 0.015 * s)


def drones_de_defesa(T, t, rng):
    """Os drones de defesa: três drones triangulares saem voando do Ultron até cada aliado e abrem um escudo de
    hexágonos em volta dele; um dos drones dispara o raio vermelho no rival."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    alvos = [(-0.55, 0.25), (0.0, 0.3), (0.55, 0.25)]
    for k, (x, y) in enumerate(alvos):
        u = ease_out(rel(t, 0.03 * k, 0.3 + 0.03 * k), 2.5)
        if 0 < u and t < 0.85:
            dx, dy = 0.0 + (x - 0.0) * u, -0.6 + (y - 0.25 - (-0.6)) * u
            g, h = _drone(T, dx, dy, 1.5, math.atan2(y - 0.25 + 0.6, x) if u < 1 else t * 4)
            G += g * (1 - rel(t, 0.75, 0.85))
            H += h * 1.5
        abre = ease_out(rel(t, 0.3 + 0.03 * k, 0.55 + 0.03 * k), 3)
        if abre > 0:
            G += _escudo_hex(T, x, y, 0.22 * abre, abre) * (1 - rel(t, 0.8, 0.95))
    raio = pulso(t, 0.35, 0.6)
    if raio > 0:
        R = T.lines([(0.0, -0.05, 0.0, -0.7, 1.0)], 0.025)
        G += (R + T.blur(R, 0.02) * 0.5) * raio
        H += T.lines([(0.0, -0.05, 0.0, -0.7, 1.0)], 0.008) * raio * 1.4 + T.gauss(0, -0.7, 0.05) * raio * 1.5
    return G * env, H * env


def _rosto_ultron(T, cx, cy, s, brilho):
    rosto = [(cx - 0.18 * s, cy - 0.2 * s), (cx + 0.18 * s, cy - 0.2 * s), (cx + 0.2 * s, cy + 0.02 * s), (cx + 0.08 * s, cy + 0.28 * s),
             (cx, cy + 0.32 * s), (cx - 0.08 * s, cy + 0.28 * s), (cx - 0.2 * s, cy + 0.02 * s)]
    G = T.lines(_contorno(rosto), 0.013 * s)
    G = G + T.lines([(cx - 0.18 * s, cy - 0.2 * s, cx - 0.1 * s, cy - 0.32 * s, 1.0), (cx + 0.18 * s, cy - 0.2 * s, cx + 0.1 * s, cy - 0.32 * s, 1.0), (cx - 0.1 * s, cy - 0.32 * s, cx + 0.1 * s, cy - 0.32 * s, 1.0)], 0.01 * s)
    olhos = T.polys([(lamina(cx - 0.15 * s, cy - 0.07 * s, cx - 0.03 * s, cy - 0.03 * s, 0.045 * s), 1.0), (lamina(cx + 0.15 * s, cy - 0.07 * s, cx + 0.03 * s, cy - 0.03 * s, 0.045 * s), 1.0)])
    boca = T.lines([(cx - 0.08 * s, cy + 0.15 * s, cx + 0.08 * s, cy + 0.15 * s, 1.0)], 0.01 * s)
    return G * 0.9 + (olhos + boca) * 0.8, (olhos * 1.5 + boca) * brilho


def ultron_preparo(T, t, rng):
    """O Preparo da Evolução autônoma: o rosto de metal do Ultron com os olhos e a boca acesos e os circuitos
    correndo em volta até ele, pulsando (laço)."""
    G, H = vazio(T)
    b = 0.7 + 0.3 * math.sin(TAU * t * 2)
    g, h = _rosto_ultron(T, 0, -0.05, 1.6, b)
    G += g
    H += h
    for k in range(8):
        a = TAU * k / 8 + 0.2
        r0, r1 = 0.62, 0.42
        x0, y0 = r0 * math.cos(a), r0 * math.sin(a) * 0.9
        xm, ym = r1 * math.cos(a), r0 * math.sin(a) * 0.9
        x1, y1 = r1 * math.cos(a), r1 * math.sin(a) * 0.9
        G += T.lines([(x0, y0, xm, ym, 1.0), (xm, ym, x1, y1, 1.0)], 0.007) * 0.9
        u = (t * 2 + k / 8) % 1
        px = x0 + (xm - x0) * min(1, u * 2) + (x1 - xm) * max(0, u * 2 - 1)
        py = y0 + (ym - y0) * min(1, u * 2) + (y1 - ym) * max(0, u * 2 - 1)
        H += T.gauss(px, py, 0.018) * 1.2
    return G, H


def evolucao_autonoma(T, t, rng):
    """A evolução autônoma: os circuitos vermelhos se reescrevem em volta do Ultron (as trilhas trocando de caminho),
    o raio sai do peito, corta o Preparo do rival (o anel que quebra em pedaços) e o rival é empurrado."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    reescreve = pulso(t, 0.0, 0.35)
    if reescreve > 0:
        q = np.random.default_rng(int(t * 14) % 6 + 20)
        for k in range(10):
            y = -0.4 + 0.08 * k
            x0 = -0.95 + q.uniform(0, 0.1)
            x1 = -0.55 + q.uniform(-0.05, 0.05)
            ym = y + q.choice([-0.04, 0.04])
            G += T.lines([(x0, y, (x0 + x1) / 2, y, 1.0), ((x0 + x1) / 2, y, (x0 + x1) / 2, ym, 1.0), ((x0 + x1) / 2, ym, x1, ym, 1.0)], 0.007) * reescreve
        H += T.gauss(-0.7, 0.0, 0.06) * reescreve * 1.5
    vai = ease_out(rel(t, 0.25, 0.35), 2)
    some = 1 - rel(t, 0.5, 0.62)
    if vai > 0 and some > 0:
        x = -0.7 + 0.7 * vai
        R = T.lines([(-0.7, 0.0, x, 0.0, 1.0)], 0.045)
        G += (R * 0.9 + T.blur(R, 0.03) * 0.6) * some
        H += T.lines([(-0.7, 0.0, x, 0.0, 1.0)], 0.012) * some * 1.4
    quebra = rel(t, 0.35, 0.7)
    if 0 < quebra < 1:
        for k in range(8):
            a0 = TAU * k / 8
            d = 0.22 + 0.3 * ease_out(quebra, 2)
            G += T.arc_band(d, 0.025, a0, a0 + 0.55, cx=0, cy=0, taper=0.5) * (1 - quebra) * 1.3
        H += T.gauss(0, 0, 0.09) * (1 - quebra) ** 2 * 1.8
    return G * env, H * env


# =================================================================== Duende Verde
def _abobora(T, cx, cy, r, ang, riso):
    """A bomba de abóbora: o corpo redondo de gomos, o cabinho e a cara recortada acesa."""
    corpo = T.polys([([(cx + r * 1.1 * math.cos(a), cy + r * 0.9 * math.sin(a)) for a in np.linspace(0, TAU, 28, endpoint=False)], 1.0)])
    gomos = T.lines([(cx + r * 0.45 * k, cy - r * 0.85, cx + r * 0.55 * k, cy + r * 0.85, 0.6) for k in (-1, 0, 1)], 0.006)
    G = corpo * 0.4 + _borda(T, corpo, 0.006) * 1.2 + gomos * 0.6 + T.lines([(cx, cy - r * 0.9, cx + r * 0.2, cy - r * 1.3, 1.0)], 0.012)
    olhos = T.polys([(_gira([(-0.04, 0.03), (0.04, 0.03), (0.0, -0.04)], 0, cx + s * r * 0.45, cy - r * 0.2), 1.0) for s in (-1, 1)])
    boca = T.polys([([(cx - r * 0.55, cy + r * 0.2), (cx - r * 0.25, cy + r * 0.4 * riso + r * 0.3), (cx, cy + r * 0.25), (cx + r * 0.25, cy + r * 0.4 * riso + r * 0.3), (cx + r * 0.55, cy + r * 0.2), (cx, cy + r * 0.6)], 1.0)])
    return G, (olhos + boca) * 1.4


def bomba_abobora(T, t, rng):
    """A bomba abóbora: a abóbora com a cara recortada voa girando em arco, a boca acende rindo e ela explode em
    verde e laranja, com a fumaça escura que cega e prende."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    voa = rel(t, 0.0, 0.38)
    if 0 < voa < 1:
        x = -0.85 + 0.85 * voa
        y = -0.45 * math.sin(math.pi * voa)
        g, h = _abobora(T, x, y, 0.17, t * 10, abs(math.sin(t * 30)))
        G += g
        H += h
    bum = rel(t, 0.36, 0.8)
    if 0 < bum < 1:
        e = ease_out(bum, 3)
        H += T.gauss(0, 0, 0.1 + 0.25 * e) * (1 - bum) ** 2 * 2.2
        G += T.ring(0.08 + 0.45 * e, 0.04, 0, 0) * (1 - bum) * 1.3
        q = np.random.default_rng(31)
        pts = [(0.5 * e * math.cos(a) * q.uniform(0.5, 1), 0.4 * e * math.sin(a) * q.uniform(0.5, 1) - 0.1 * bum, 1 - bum) for a in np.linspace(0, TAU, 14, endpoint=False)]
        G += T.splats(pts, 0.06) * 0.7
    fumo = pulso(t, 0.55, 1.0)
    if fumo > 0:
        q = np.random.default_rng(33)
        pts = [(q.uniform(-0.3, 0.3), q.uniform(-0.25, 0.15) - 0.1 * t, q.uniform(0.4, 1)) for _ in range(16)]
        F = np.clip(T.splats(pts, 0.07), 0, 1)
        G += (F * 0.3 + _borda(T, F, 0.015) * 0.8) * fumo
    return G * env, H * env


def gas_do_duende(T, t, rng):
    """O gás do Duende: as nuvens de gás verde rolam por cima dos três rivais, as caras assustadoras (os olhos
    vazados e a boca torta) se formam nelas, e o veneno pinga (Confuso e Envenenado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    rola = ease_out(rel(t, 0.0, 0.4), 2)
    some = 1 - rel(t, 0.75, 0.95)
    if rola > 0:
        q = np.random.default_rng(41)
        pts = []
        for k in range(40):
            x = -1.0 + (q.uniform(0, 2.0)) * rola
            pts.append((x, q.uniform(-0.35, 0.25) + 0.05 * math.sin(t * 5 + k), q.uniform(0.5, 1)))
        N = np.zeros_like(T.zero())
        for x, y, s in pts:
            N = np.maximum(N, T.gauss(x, y, 0.06 + 0.06 * s))
        N = np.clip(N * 1.5, 0, 1)
        G += (N * 0.35 + _borda(T, N, 0.02) * 1.1) * some
    caras = pulso(t, 0.35, 0.9)
    if caras > 0:
        for k, x in enumerate((-0.5, 0.0, 0.5)):
            y = -0.1 + 0.03 * math.sin(t * 8 + k)
            olhos = T.splats([(x - 0.06, y - 0.03, 1.0), (x + 0.06, y - 0.03, 1.0)], 0.025)
            boca = T.polyline([(x - 0.07, y + 0.08), (x - 0.02, y + 0.05), (x + 0.02, y + 0.1), (x + 0.07, y + 0.06)], 0.012)
            G += np.clip((T.gauss(x, y, 0.13) * 0.4 - olhos * 0.4), 0, 1) * caras + boca * caras
            H += olhos * caras * 0.6
    pinga = rel(t, 0.4, 1.0)
    if 0 < pinga < 1:
        q = np.random.default_rng(43)
        for k in range(8):
            x = q.uniform(-0.7, 0.7)
            y = 0.15 + 0.4 * ((pinga * 2 + q.uniform(0, 1)) % 1)
            G += T.gauss(x, y, 0.015) * (1 - pinga)
    return G * env, H * env


def _planador(T, cx, cy, s, ang=0.0):
    """O planador do Duende: as asas de morcego (as pontas recortadas) e o corpo no meio."""
    asa = []
    for lado in (-1, 1):
        asa += [(0.0, -0.02), (lado * 0.12, -0.05), (lado * 0.3, -0.02), (lado * 0.26, 0.03), (lado * 0.2, 0.0), (lado * 0.15, 0.04), (lado * 0.08, 0.01), (0.0, 0.04)]
    pts = _gira([(x * s, y * s) for x, y in asa], ang, cx, cy)
    return T.polys([(pts[:8], 1.0), (pts[8:], 1.0)])


def duende_preparo(T, t, rng):
    """O Preparo da Prancha armadilhada: o planador de asas de morcego pairando, balançando, com os dois jatos
    acesos embaixo e a fumaça saindo (laço)."""
    G, H = vazio(T)
    y = -0.05 + 0.04 * math.sin(TAU * t * 2)
    P = _planador(T, 0, y, 2.2, 0.06 * math.sin(TAU * t))
    G += P * 0.5 + _borda(T, P, 0.006) * 1.4
    for lado in (-1, 1):
        jx = 0.12 * lado
        chama = [(jx + 0.03 * math.sin(t * 40 + k), y + 0.1 + 0.06 * k, 1 - k / 5) for k in range(5)]
        H += T.splats(chama, 0.03) * 1.3
    q = np.random.default_rng(51)
    pts = [(0.12 * (1 if k % 2 else -1) + q.uniform(-0.05, 0.05), y + 0.4 + ((t + k / 10) % 1) * 0.3, 1 - ((t + k / 10) % 1)) for k in range(10)]
    G += T.splats(pts, 0.04) * 0.5
    return G, H


def prancha_armadilhada(T, t, rng):
    """A prancha armadilhada: o planador vem em rasante, as lâminas saem das pontas das asas, cortam o rival em
    linha e a carga de baixo explode (Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    vem = ease_in(rel(t, 0.0, 0.35), 1.6)
    if 0 < vem and t < 0.45:
        x = -0.95 + 1.3 * vem
        y = -0.25 + 0.25 * vem
        P = _planador(T, x, y, 1.8, 0.2)
        G += P * 0.5 + _borda(T, P, 0.006) * 1.4
        lam = ease_out(rel(t, 0.15, 0.25), 3)
        for lado in (-1, 1):
            bx, by = x + lado * 0.5, y - 0.02 + lado * 0.1
            G += T.polys([(lamina(bx - lado * 0.04, by, bx + lado * 0.12 * lam, by + 0.01, 0.02), 1.0)]) * 1.3
        G += T.tapered([(x - 0.5, y, x - 0.15, y, 1.0)], 0.02) * 0.6
        H += T.splats([(x - 0.06, y + 0.05, 1.0), (x + 0.06, y + 0.05, 1.0)], 0.02)
    corte = rel(t, 0.25, 0.5)
    if 0 < corte < 1:
        L = T.polys([(lamina(-0.4, -0.15, 0.4, 0.15, 0.03, prog=min(1, corte * 3), inicio=corte), 1.0)])
        G += L * 1.4
        H += L * 0.6
    bum = rel(t, 0.42, 0.85)
    if 0 < bum < 1:
        e = ease_out(bum, 3)
        H += T.gauss(0, 0.05, 0.1 + 0.2 * e) * (1 - bum) ** 2 * 2.0
        G += T.ring(0.08 + 0.4 * e, 0.04, 0, 0.05) * (1 - bum) * 1.2
        raios = [(0.06 * math.cos(a), 0.05 + 0.06 * math.sin(a), (0.2 + 0.4 * e) * math.cos(a), 0.05 + (0.2 + 0.4 * e) * math.sin(a), 1 - bum) for a in np.linspace(0, TAU, 12, endpoint=False)]
        G += T.tapered(raios, 0.025)
    return G * env, H * env


# =================================================================== Surfista Prateado
def _brilhos(T, t, x0, y0, x1, y1, n, seed, sobe=0.0):
    q = np.random.default_rng(seed)
    shapes = []
    for _ in range(n):
        u = q.uniform(0, 1)
        x = x0 + (x1 - x0) * u + q.uniform(-0.05, 0.05)
        y = y0 + (y1 - y0) * u + q.uniform(-0.06, 0.06) - sobe
        r = 0.02 + 0.02 * abs(math.sin(t * 20 + u * 9))
        shapes.append((estrela(x, y, r, t * 3, 4, 0.3), 1.0))
    return T.polys(shapes)


def rajada_cosmica(T, t, rng):
    """A rajada cósmica: o raio prateado sai da mão, cheio de estrelinhas piscando dentro, e a marca cósmica (a
    estrela de quatro pontas) fica no rival."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    vai = ease_out(rel(t, 0.05, 0.22), 2)
    some = 1 - rel(t, 0.45, 0.6)
    if vai > 0 and some > 0:
        x = -0.85 + 0.85 * vai
        R = T.lines([(-0.85, 0.0, x, 0.0, 1.0)], 0.04)
        G += (R * 0.9 + T.blur(R, 0.03) * 0.6) * some
        H += T.lines([(-0.85, 0.0, x, 0.0, 1.0)], 0.01) * some * 1.4
        G += _brilhos(T, t, -0.85, 0.0, x, 0.0, 12, 61) * some
    H += T.gauss(-0.85, 0.0, 0.05) * pulso(t, 0.0, 0.35) * 1.5
    marca = pulso(t, 0.3, 1.0)
    if marca > 0:
        M = T.polys([(estrela(0, 0, 0.2 * marca + 0.05, t * 2, 4, 0.25), 1.0)])
        G += M * 0.5 * marca + _borda(T, M, 0.006) * marca * 1.3
        H += T.gauss(0, 0, 0.05) * marca * 1.2
    return G * env, H * env


def transmutacao_estelar(T, t, rng):
    """A transmutação estelar: as partículas prateadas giram em volta de cada aliado e viram uma casca brilhante
    (o Escudo), e o rastro estelar empurra o trio para a frente (adianta a vez)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for k, (x, y) in enumerate(((-0.55, 0.2), (0.0, 0.25), (0.55, 0.2))):
        gira = rel(t, 0.0 + 0.04 * k, 0.4 + 0.04 * k)
        if 0 < gira < 1:
            q = np.random.default_rng(71 + k)
            pts = []
            for j in range(16):
                a = q.uniform(0, TAU) + t * 8
                r = 0.35 * (1 - ease_in(gira, 1.5)) + 0.18
                pts.append((x + r * math.cos(a), y + r * 0.8 * math.sin(a), 1.0))
            H += T.splats(pts, 0.012) * 1.2
            G += T.splats(pts, 0.016) * 1.1
        casca = pulso(t, 0.35 + 0.04 * k, 1.0)
        if casca > 0:
            G += T.ring(0.18, 0.02, x, y, squash=1.1) * casca * 1.2 + T.gauss(x, y - 0.06, 0.08) * casca * 0.3
            for j in range(3):
                u = (t * 2.5 + j / 3) % 1
                G += T.tapered([(x - 0.3 + 0.2 * u, y + 0.1 - 0.1 * j, x - 0.15 + 0.2 * u, y + 0.1 - 0.1 * j, 1.0)], 0.01) * casca * (1 - u)
    return G * env, H * env


def _prancha(T, cx, cy, s, ang):
    pts = [(cx + 0.28 * s * math.cos(a) * math.cos(ang) - 0.05 * s * math.sin(a) * math.sin(ang),
            cy + 0.28 * s * math.cos(a) * math.sin(ang) + 0.05 * s * math.sin(a) * math.cos(ang)) for a in np.linspace(0, TAU, 30, endpoint=False)]
    P = T.polys([(pts, 1.0)])
    return P


def surfista_preparo(T, t, rng):
    """O Preparo do Surfe dimensional: a prancha prateada parada no ar, ondulando de leve, com o rastro cósmico
    ondulado atrás e as estrelas girando em volta (laço)."""
    G, H = vazio(T)
    y = 0.15 + 0.03 * math.sin(TAU * t * 2)
    P = _prancha(T, 0, y, 1.6, -0.1 + 0.05 * math.sin(TAU * t))
    G += P * 0.5 + _borda(T, P, 0.006) * 1.4
    H += T.lines([(-0.35, y + 0.02, 0.35, y - 0.04, 1.0)], 0.008) * 0.8
    for k in range(3):
        pts = [(-0.4 - 0.45 * u, y + 0.03 * k - 0.03 + 0.05 * math.sin(u * 10 - t * TAU * 2 + k)) for u in np.linspace(0, 1, 20)]
        G += T.polyline(pts, 0.01) * (0.8 - 0.2 * k)
    for k in range(6):
        a = TAU * k / 6 + TAU * t / 2
        G += T.polys([(estrela(0.55 * math.cos(a), y - 0.15 + 0.35 * math.sin(a), 0.035, t * 4, 4, 0.3), 1.0)]) * 0.9
    return G, H


def surfe_dimensional(T, t, rng):
    """O surfe dimensional: a prancha atravessa o campo rasgando o espaço — a fenda brilhante que fica atrás dela,
    com as estrelas escapando — e acerta o rival em cheio, que fica Lento."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    vai = ease_in(rel(t, 0.0, 0.3), 1.5)
    if t < 0.5:
        x = -0.95 + 0.95 * vai
        b = 1 - rel(t, 0.35, 0.5)
        P = _prancha(T, x, 0.05, 1.3, -0.08)
        G += (P * 0.5 + _borda(T, P, 0.006) * 1.4) * b
        fenda = T.polys([(lamina(-0.95, 0.07, x - 0.2, 0.06, 0.04), 1.0)])
        G += fenda * 0.8 * b
        H += T.lines([(-0.95, 0.07, x - 0.2, 0.06, 1.0)], 0.006) * b * 1.5
        G += _brilhos(T, t, -0.95, 0.07, x - 0.2, 0.06, 10, 81, 0.08 * t) * b
    g = rel(t, 0.3, 0.65)
    if 0 < g < 1:
        e = ease_out(g, 3)
        H += T.gauss(0, 0.05, 0.08 + 0.15 * e) * (1 - g) ** 2 * 2.0
        G += T.ring(0.08 + 0.4 * e, 0.035, 0, 0.05, squash=1.4) * (1 - g) * 1.3
    lento = pulso(t, 0.55, 1.0)
    if lento > 0:
        G += T.arc_band(0.22, 0.02, t * 2, t * 2 + 4.5, cx=0, cy=0.05, squash=0.6, taper=0.5) * lento
    return G * env, H * env


# =================================================================== Galactus
def _mao(T, cx, cy, s, fecha):
    """A mão enorme vista de frente, os dedos dobrando conforme `fecha`."""
    palma = T.polys([([(cx - 0.18 * s, cy), (cx + 0.18 * s, cy), (cx + 0.15 * s, cy - 0.22 * s), (cx - 0.15 * s, cy - 0.22 * s)], 1.0)])
    dedos = []
    for k in range(4):
        x = cx + (-0.135 + 0.09 * k) * s
        L = (0.2 + 0.03 * (k in (1, 2))) * s * (1 - 0.6 * fecha)
        dedos.append((lamina(x, cy, x, cy + L, 0.035 * s), 1.0))
    dedos.append((lamina(cx - 0.18 * s, cy - 0.12 * s, cx - 0.3 * s + 0.12 * s * fecha, cy + 0.02 * s, 0.035 * s), 1.0))
    D = T.polys(dedos)
    M = np.clip(palma + D, 0, 1)
    return M * 0.35 + _borda(T, M, 0.008) * 1.3


def dreno_planetario(T, t, rng):
    """O dreno planetário: o rival vira um planeta (o globo com os anéis de órbita), a energia dele sobe em espiral
    até a mão enorme do Galactus lá em cima, que se fecha guardando a força (Roubo de vida)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    planeta = pulso(t, 0.0, 0.9)
    if planeta > 0:
        G += T.ring(0.18, 0.015, 0, 0.25) * planeta + T.ring(0.3, 0.01, 0, 0.25, squash=3.5) * planeta
        G += T.lines([(-0.17, 0.2, 0.17, 0.2, 0.6), (-0.15, 0.32, 0.15, 0.32, 0.6)], 0.006) * planeta
    sobe = rel(t, 0.15, 0.8)
    if 0 < sobe < 1:
        for k in range(3):
            pts = []
            for j in range(30):
                u = j / 29 * min(1, sobe * 1.4)
                a = u * TAU * 2 + k * TAU / 3 + t * 4
                r = 0.18 * (1 - u)
                pts.append((r * math.cos(a), 0.25 - 0.85 * u))
            G += T.polyline(pts, 0.012) * (1 - rel(t, 0.7, 0.85))
        H += T.splats([(0.1 * math.cos(t * 8 + k), 0.25 - 0.85 * ((sobe * 1.4 + k / 5) % 1), 1.0) for k in range(5)], 0.02) * 1.2
    mao = pulso(t, 0.05, 1.0)
    if mao > 0:
        G += _mao(T, 0, -0.62, 1.6, ease_in(rel(t, 0.6, 0.85), 2)) * mao
        H += T.gauss(0, -0.65, 0.08) * pulso(t, 0.6, 0.95) * 1.5
    return G * env, H * env


def _elmo_galactus(T, cx, cy, s):
    """O elmo do Galactus: a frente larga, as duas abas altas dos lados e a fenda dos olhos."""
    frente = [(cx - 0.22 * s, cy + 0.2 * s), (cx - 0.24 * s, cy - 0.1 * s), (cx - 0.12 * s, cy - 0.2 * s), (cx + 0.12 * s, cy - 0.2 * s),
              (cx + 0.24 * s, cy - 0.1 * s), (cx + 0.22 * s, cy + 0.2 * s)]
    linhas = _contorno(frente)
    for lado in (-1, 1):
        linhas += _contorno([(cx + lado * 0.22 * s, cy - 0.05 * s), (cx + lado * 0.42 * s, cy - 0.5 * s), (cx + lado * 0.32 * s, cy - 0.55 * s), (cx + lado * 0.18 * s, cy - 0.15 * s)])
    linhas += [(cx - 0.14 * s, cy - 0.02 * s, cx + 0.14 * s, cy - 0.02 * s, 1.0), (cx, cy - 0.2 * s, cx, cy - 0.06 * s, 0.7)]
    return T.lines(linhas, 0.012 * s)


def rajada_do_poder_cosmico(T, t, rng):
    """A rajada do Poder Cósmico: o elmo do Galactus surge enorme no alto, os olhos acendem e o Poder Cósmico desce
    em colunas largas sobre os rivais (Enfraquecido), enquanto o trio dele ganha o brilho do Escudo."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    surge = ease_out(rel(t, 0.0, 0.25), 2.5)
    b = 1 - rel(t, 0.7, 0.88)
    if surge > 0:
        G += _elmo_galactus(T, 0, -0.55 + 0.1 * (1 - surge), 1.3) * surge * b
        H += T.lines([(-0.18, -0.58, 0.18, -0.58, 1.0)], 0.012) * pulso(t, 0.15, 0.6) * 1.5
    for k, x in enumerate((-0.5, 0.0, 0.5)):
        u = rel(t, 0.25 + 0.05 * k, 0.65 + 0.05 * k)
        if 0 < u < 1:
            desce = ease_in(min(1, u * 3), 2)
            y1 = -0.4 + 0.75 * desce
            C = T.lines([(x, -0.4, x, y1, 1.0)], 0.07 * (1 - u) + 0.025)
            G += C * 0.8 + T.blur(C, 0.03) * 0.5
            H += T.lines([(x, -0.4, x, y1, 1.0)], 0.012) * (1 - u) * 1.4
            if desce >= 1:
                G += _setas_para_baixo(T, u, xs=(x,), y0=0.1) * 0.8
    return G * env, H * env


def devorador_preparo(T, t, rng):
    """O Preparo do Toque do Devorador: as duas mãos enormes do Galactus abertas sobre o campo e a energia de tudo
    sendo sugada para o centro entre elas, em espiral (laço)."""
    G, H = vazio(T)
    for lado in (-1, 1):
        G += _mao(T, lado * 0.45, -0.25, 1.2, 0.1 + 0.1 * math.sin(TAU * t)) * 0.9
    q = np.random.default_rng(91)
    pts = []
    for k in range(24):
        u = (t + q.uniform(0, 1)) % 1
        a = q.uniform(0, TAU) + u * 3
        r = 0.7 * (1 - u)
        pts.append((r * math.cos(a), 0.05 + r * 0.7 * math.sin(a), u))
    H += T.splats(pts, 0.015) * 1.3
    G += T.splats(pts, 0.02) * 1.0
    H += T.gauss(0, 0.05, 0.06) * (0.7 + 0.3 * math.sin(TAU * t * 2)) * 1.2
    return G, H


# =================================================================== Senhor das Estrelas
def _nota(T, cx, cy, s):
    """A nota musical: a cabeça cheia, a haste e a bandeirinha."""
    cab = T.gauss(cx, cy, 0.025 * s, 0.02 * s)
    haste = T.lines([(cx + 0.022 * s, cy, cx + 0.022 * s, cy - 0.1 * s, 1.0), (cx + 0.022 * s, cy - 0.1 * s, cx + 0.06 * s, cy - 0.07 * s, 1.0)], 0.008 * s)
    return np.clip(cab * 1.5 + haste, 0, 1)


def plano_improvisado(T, t, rng):
    """O plano improvisado: a fita cassete aparece com os dois carretéis girando, as notas de música saem, o trio
    ganha as setas de Acelerado e adianta a vez, e um tiro rápido de blaster acerta o rival."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    fita = pulso(t, 0.0, 0.7)
    if fita > 0:
        cx, cy = -0.6, -0.4
        G += T.lines(_contorno([(cx - 0.2, cy - 0.12), (cx + 0.2, cy - 0.12), (cx + 0.2, cy + 0.12), (cx - 0.2, cy + 0.12)]), 0.012) * fita
        for lado in (-1, 1):
            rx = cx + lado * 0.09
            G += T.ring(0.045, 0.01, rx, cy) * fita
            G += T.lines([(rx, cy, rx + 0.045 * math.cos(t * 20 + j * 2.1), cy + 0.045 * math.sin(t * 20 + j * 2.1), 1.0) for j in range(3)], 0.006) * fita
        for k in range(4):
            u = (t * 1.5 + k / 4) % 1
            G += _nota(T, cx + 0.25 + 0.4 * u, cy - 0.1 - 0.15 * math.sin(u * TAU) - 0.1 * u, 1.3) * (1 - u) * fita
    for k, x in enumerate((-0.5, 0.0, 0.5)):
        c = pulso(t, 0.3 + 0.05 * k, 0.8 + 0.05 * k)
        if c > 0:
            y = 0.4 - 0.25 * rel(t, 0.3 + 0.05 * k, 0.8 + 0.05 * k)
            G += T.lines([(x - 0.06, y + 0.05, x, y - 0.01, 1.0), (x + 0.06, y + 0.05, x, y - 0.01, 1.0), (x, y + 0.12, x, y, 1.0)], 0.014) * c
    tiro = rel(t, 0.15, 0.3)
    if 0 < tiro < 1:
        x = -0.4 + 0.8 * tiro
        H += T.tapered([(x - 0.2, -0.05, x, -0.05, 1.0)], 0.03) * 1.4
        G += T.tapered([(x - 0.25, -0.05, x, -0.05, 1.0)], 0.04) * 1.1
    g = pulso(t, 0.28, 0.5)
    H += T.gauss(0.4, -0.05, 0.05) * g * 1.6
    return G * env, H * env


def danca_de_distracao(T, t, rng):
    """A dança de distração: a pista de dança acende em quadrados piscando, as notas pulam no ritmo e os rivais
    ficam tontos olhando a dança (as espirais nos olhos — Confuso)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    pista = pulso(t, 0.0, 0.95)
    if pista > 0:
        bate = int(t * 8)
        shapes = []
        for i in range(6):
            for j in range(3):
                x = -0.75 + 0.3 * i
                y = 0.25 + 0.13 * j
                pts = [(x - 0.13 + 0.06 * (j - 1) * 0.3, y - 0.055), (x + 0.13, y - 0.055), (x + 0.13, y + 0.055), (x - 0.13, y + 0.055)]
                acende = ((i * 7 + j * 3 + bate) % 4 == 0)
                shapes.append((pts, 1.0 if acende else 0.2))
        P = T.polys(shapes)
        G += P * pista * 0.7
        H += P * pista * 0.3
    for k in range(6):
        u = (t * 2 + k / 6) % 1
        x = -0.7 + 0.28 * k
        y = 0.1 - 0.3 * abs(math.sin(math.pi * u * 2))
        G += _nota(T, x, y, 1.4) * pista
    tonto = pulso(t, 0.3, 1.0)
    if tonto > 0:
        for k, x in enumerate((-0.5, 0.0, 0.5)):
            for lado in (-1, 1):
                ex, ey = x + lado * 0.05, -0.4
                pts = [(ex + 0.03 * (j / 20) * math.cos(t * 25 + TAU * 2 * j / 20), ey + 0.03 * (j / 20) * math.sin(t * 25 + TAU * 2 * j / 20)) for j in range(21)]
                G += T.polyline(pts, 0.008) * tonto * 1.2
    return G * env, H * env


REGISTRO = [
    ("analise_preditiva", analise_preditiva, GRANDE, "Ultron · o olho de varredura, a mira e os dados", False),
    ("drones_de_defesa", drones_de_defesa, GRANDE, "Ultron · os drones e os escudos de hexágonos", False),
    ("ultron_preparo", ultron_preparo, MEDIA, "Ultron · o rosto de metal e os circuitos (Preparo, laço)", True),
    ("evolucao_autonoma", evolucao_autonoma, GRANDE, "Ultron · os circuitos reescritos e o raio que corta", False),
    ("bomba_abobora", bomba_abobora, GRANDE, "Duende Verde · a abóbora rindo e a explosão", False),
    ("gas_do_duende", gas_do_duende, GRANDE, "Duende Verde · o gás verde com as caras", False),
    ("duende_preparo", duende_preparo, MEDIA, "Duende Verde · o planador pairando (Preparo, laço)", True),
    ("prancha_armadilhada", prancha_armadilhada, GRANDE, "Duende Verde · o rasante com as lâminas e a carga", False),
    ("rajada_cosmica", rajada_cosmica, GRANDE, "Surfista Prateado · o raio prateado e a marca", False),
    ("transmutacao_estelar", transmutacao_estelar, GRANDE, "Surfista Prateado · as cascas brilhantes no trio", False),
    ("surfista_preparo", surfista_preparo, MEDIA, "Surfista Prateado · a prancha e o rastro (Preparo, laço)", True),
    ("surfe_dimensional", surfe_dimensional, GRANDE, "Surfista Prateado · a prancha rasgando o espaço", False),
    ("dreno_planetario", dreno_planetario, GRANDE, "Galactus · o planeta e a mão que suga", False),
    ("rajada_do_poder_cosmico", rajada_do_poder_cosmico, GRANDE, "Galactus · o elmo e as colunas cósmicas", False),
    ("devorador_preparo", devorador_preparo, MEDIA, "Galactus · as mãos e a energia sugada (Preparo, laço)", True),
    ("plano_improvisado", plano_improvisado, GRANDE, "Senhor das Estrelas · a fita, as notas e o tiro", False),
    ("danca_de_distracao", danca_de_distracao, GRANDE, "Senhor das Estrelas · a pista de dança e os tontos", False),
]
