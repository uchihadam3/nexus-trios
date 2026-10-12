"""Rodada 20 das habilidades próprias: Master Chief, Doom Slayer, Solid Snake, Raiden (Metal Gear) e Leon S. Kennedy.

Master Chief
- escudo_de_energia: a bolha do escudo dourado se fecha em volta do aliado, com o padrão de hexágonos piscando
  (Escudo e Protegido).
- fogo_de_supressao: a rajada do fuzil: os riscos dos tiros num cone apertado, o clarão da boca e os impactos, com
  as setas de fraqueza (Enfraquecido).
- masterchief_preparo: o Preparo da Posição firme — o anel do escudo enchendo e os hexágonos acendendo (laço).
- posicao_firme: o pisão no chão: o escudo dourado brilha e a onda de choque varre os rivais (Lento).

Doom Slayer
- avanco_brutal: a investida com as linhas de velocidade e o soco brutal que explode em vermelho, prendendo o
  rival.
- blindagem_de_combate: as placas da armadura encaixam uma a uma em volta, com o brilho verde (Escudo e
  Fortalecido).
- doomslayer_preparo: o Preparo da Onda sísmica — o punho em chamas carregando, com as runas girando no chão
  (laço).
- onda_sismica: o soco no chão: as rachaduras correm, a onda de fogo e as pedras sobem (Paralisado).

Solid Snake
- camuflagem: a caixa de papelão cai, a camuflagem óptica tremula em faixas e o tiro sai do esconderijo
  (Protegido e Acelerado).
- tiro_de_flanco: a mira laser vermelha cruza o campo, o tiro com silenciador e o impacto (Exposto).

Raiden (Metal Gear)
- corte_em_sequencia: os cortes da lâmina de alta frequência em sequência rápida, com as imagens de rastro azuis.
- raiden_preparo: o Preparo do Zandatsu — o Modo lâmina: a grade azul do tempo lento e a lâmina vibrando (laço).
- zandatsu: o plano do corte varre o campo, dezenas de cortes precisos e a explosão elétrica (Paralisado).

Leon S. Kennedy
- mira_firme: o ponto do laser dança, para na cabeça e a mira trava (Marcado e o Preparo atrasado).
- tiro_na_cabeca: o tiro cruza, o clarão na altura da cabeça e o rival cambaleia (Lento).
- leon_preparo: o Preparo da Faca de combate — a faca sendo sacada com o brilho na lâmina (laço).
- faca_de_combate: os dois cortes em X da faca, a faísca do aparo e o Preparo do rival quebrando.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .rodada13 import _borda, _gira


def _hexagono(cx, cy, r, ang=0.0):
    return [(cx + r * math.cos(ang + TAU * k / 6), cy + r * math.sin(ang + TAU * k / 6)) for k in range(6)]


def _favo(T, r_bolha, cx=0.0, cy=0.0, lado=0.07, acesas=None):
    """O padrão de hexágonos do escudo: os contornos dos favos dentro do círculo."""
    segs = []
    h = lado * math.sqrt(3)
    linha = 0
    y = cy - r_bolha
    while y <= cy + r_bolha:
        x0 = cx - r_bolha + (lado * 1.5 if linha % 2 else 0)
        x = x0
        while x <= cx + r_bolha:
            if math.hypot(x - cx, y - cy) < r_bolha * 0.92 and (acesas is None or acesas(x, y)):
                pts = _hexagono(x, y, lado * 0.95)
                segs += [(pts[k][0], pts[k][1], pts[(k + 1) % 6][0], pts[(k + 1) % 6][1], 1.0) for k in range(6)]
            x += lado * 3
        y += h / 2
        linha += 1
    return T.lines(segs, 0.006) if segs else T.zero()


def _setas_baixo(T, u, xs=(-0.45, 0.45), y0=-0.1):
    segs = []
    for x in xs:
        y = y0 + 0.25 * u
        segs += [(x - 0.06, y - 0.05, x, y + 0.01, 1.0), (x + 0.06, y - 0.05, x, y + 0.01, 1.0), (x, y - 0.12, x, y, 1.0)]
    return T.lines(segs, 0.014)


# =================================================================== Master Chief
def escudo_de_energia(T, t, rng):
    """O escudo de energia: a bolha dourada fecha em volta do aliado, os hexágonos piscam e o escudo assenta."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    fecha = ease_out(rel(t, 0.0, 0.35), 3)
    if fecha > 0:
        r = 0.45 * fecha
        G += T.ring(r, 0.03, 0, 0.05) * 1.2 + T.gauss(0, 0.05, r * 0.9) * 0.12
        q = np.random.default_rng(int(t * 10) % 7 + 1)
        semente = q.uniform(0, 100)
        G += _favo(T, r, 0, 0.05, 0.065, lambda x, y: (math.sin(x * 37 + y * 23 + semente) > 0.2)) * (0.5 + 0.5 * pulso(t, 0.1, 0.6))
    choque = pulso(t, 0.3, 0.5)
    if choque > 0:
        H += T.ring(0.45, 0.02, 0, 0.05) * choque * 1.5
    return G * env, H * env


def fogo_de_supressao(T, t, rng):
    """O fogo de supressão: a rajada do fuzil num cone apertado, o clarão da boca, os impactos e as setas de
    fraqueza."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    q = np.random.default_rng(31)
    for k in range(14):
        t0 = 0.02 + 0.03 * k
        u = rel(t, t0, t0 + 0.09)
        if 0 < u < 1:
            sy = -0.1 + q.uniform(-0.03, 0.03)
            ty = q.uniform(-0.15, 0.15)
            hx = -0.7 + 0.72 * ease_in(u, 1.1)
            cx = -0.7 + 0.72 * max(0, u - 0.45)
            hy, cy = sy + (ty - sy) * u, sy + (ty - sy) * max(0, u - 0.4)
            G += T.tapered([(cx, cy, hx, hy, 1.0)], 0.034) * 1.7
            H += T.tapered([(cx, cy, hx, hy, 1.0)], 0.013) * 1.5
            if u > 0.85:
                G += T.flare(0.02, ty, 0.14, q.uniform(0, 1), 0.03)
                H += T.gauss(0.02, ty, 0.025) * 1.2
    boca = pulso(t, 0.0, 0.48) * (0.6 + 0.4 * math.sin(t * 90))
    if boca > 0:
        G += T.flare(-0.7, -0.1, 0.3, 0, 0.03) * boca * 1.3
        H += T.gauss(-0.7, -0.1, 0.06) * boca * 1.6
    fraco = pulso(t, 0.45, 1.0)
    if fraco > 0:
        G += _setas_baixo(T, rel(t, 0.45, 1.0), xs=(-0.2, 0.2)) * fraco
    return G * env, H * env


def masterchief_preparo(T, t, rng):
    """O Preparo da Posição firme: o anel do escudo enchendo em volta e os hexágonos acendendo por vez (laço)."""
    G, H = vazio(T)
    enche = (t * 1.2) % 1
    G += T.arc_band(0.42, 0.03, -math.pi / 2, -math.pi / 2 + TAU * max(0.05, enche), cx=0, cy=0, taper=0.0) * 1.1
    G += T.ring(0.42, 0.008, 0, 0) * 0.35
    k0 = int(t * 8) % 7
    G += _favo(T, 0.36, 0, 0, 0.07, lambda x, y: (int((x + 1) * 7 + (y + 1) * 5) % 7) == k0) * 1.0
    G += _favo(T, 0.36, 0, 0, 0.07) * 0.2
    H += T.gauss(0, 0, 0.08) * (0.4 + 0.3 * math.sin(TAU * t * 3))
    return G, H


def posicao_firme(T, t, rng):
    """A posição firme: o pisão no chão, o escudo dourado brilha e a onda de choque varre os rivais (Lento)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    pisa = pulso(t, 0.05, 0.35)
    if pisa > 0:
        H += T.gauss(0, 0.3, 0.12, 0.04) * pisa * 1.6
        G += T.ring(0.3, 0.03, 0, 0.0) * pisa
    onda = rel(t, 0.1, 0.7)
    if 0 < onda < 1:
        g = ease_out(onda, 2.5)
        G += T.ring(0.1 + 0.9 * g, 0.05, 0, 0.3, 2.6) * (1 - onda) * 1.5
        G += T.ring(0.05 + 0.7 * g, 0.025, 0, 0.3, 2.6) * (1 - onda)
        q = np.random.default_rng(4)
        pts = [((0.1 + 0.9 * g) * math.cos(a), 0.3 + (0.1 + 0.9 * g) * math.sin(a) / 2.6 - 0.1 * g, (1 - onda)) for a in q.uniform(0, TAU, 30)]
        G += T.splats(pts, 0.025) * 0.8
    lento = pulso(t, 0.5, 1.0)
    if lento > 0:
        for x in (-0.5, 0.0, 0.5):
            G += T.ring(0.1, 0.01, x, -0.1) * lento + T.lines([(x, -0.1, x, -0.17, 1.0), (x, -0.1, x + 0.05, -0.1, 1.0)], 0.01) * lento
    return G * env, H * env


# =================================================================== Doom Slayer
def avanco_brutal(T, t, rng):
    """O avanço brutal: a investida com as linhas de velocidade e o soco brutal que explode em vermelho, com os
    grilhões de luz prendendo o rival."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    vem = rel(t, 0.0, 0.25)
    if vem < 1:
        x = -0.8 + 0.7 * ease_in(vem, 1.5)
        P, nos = _punho(T, x, 0.0, 1.6, 0.0)
        G += P * 0.5 + _borda(T, P, 0.008) * 1.2
        H += nos
        G += T.tapered([(x - 0.8, dy, x - 0.25, dy, 0.7) for dy in (-0.12, 0.0, 0.12)], 0.02)
    boom = rel(t, 0.25, 0.65)
    if boom > 0:
        g = ease_out(boom, 3)
        G += T.gauss(0.05, 0, 0.1 + 0.25 * g) * (1 - boom) * 1.6
        H += T.gauss(0.05, 0, 0.06 + 0.08 * g) * (1 - boom) * 1.8
        q = np.random.default_rng(8)
        segs = [(0.05, 0, 0.05 + (0.2 + 0.4 * g) * math.cos(a), (0.2 + 0.4 * g) * math.sin(a), 1.0) for a in q.uniform(-1.2, 1.2, 12)]
        G += T.tapered(segs, 0.03) * (1 - boom) * 1.2
    preso = pulso(t, 0.45, 1.0)
    if preso > 0:
        for k in range(2):
            y = -0.08 + 0.16 * k
            elos = [(x, y + 0.02 * math.sin(x * 30)) for x in np.linspace(-0.3, 0.4, 12)]
            G += T.polyline(elos, 0.012) * preso
    return G * env, H * env


def blindagem_de_combate(T, t, rng):
    """A blindagem de combate: as placas da armadura encaixam uma a uma em volta, com o brilho verde, e a força
    sobe (Escudo e Fortalecido)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k in range(6):
        a = TAU * k / 6 - math.pi / 2
        t0 = 0.04 * k
        u = ease_out(rel(t, t0, t0 + 0.2), 3)
        if u > 0:
            r = 0.75 - 0.33 * u
            cx, cy = r * math.cos(a), r * math.sin(a)
            placa = _gira([(-0.1, -0.05), (0.1, -0.05), (0.08, 0.06), (-0.08, 0.06)], a + math.pi / 2, cx, cy)
            P = T.polys([(placa, 1.0)])
            G += P * 0.5 + _borda(T, P, 0.006) * 1.2
            if u > 0.95:
                H += T.gauss(cx, cy, 0.04) * pulso(t, t0 + 0.18, t0 + 0.4) * 1.4
    brilho = pulso(t, 0.3, 0.9)
    if brilho > 0:
        G += T.ring(0.42, 0.02, 0, 0) * brilho
        for x in (-0.2, 0.2):
            y = 0.2 - 0.3 * rel(t, 0.4, 0.9)
            G += T.lines([(x - 0.06, y + 0.05, x, y - 0.01, 1.0), (x + 0.06, y + 0.05, x, y - 0.01, 1.0), (x, y + 0.12, x, y, 1.0)], 0.014) * brilho
    return G * env, H * env


def doomslayer_preparo(T, t, rng):
    """O Preparo da Onda sísmica: o punho em chamas carregando no alto, com as runas girando no chão (laço)."""
    G, H = vazio(T)
    P, nos = _punho(T, 0.0, -0.15, 1.5, math.pi / 2)
    G += P * 0.4 + _borda(T, P, 0.008)
    H += nos * 0.7
    q = np.random.default_rng(int(t * 14) % 6 + 3)
    pts = [(q.uniform(-0.15, 0.15), -0.15 - ((t * 2 + q.uniform(0, 1)) % 1) * 0.35, q.uniform(0.4, 1)) for _ in range(16)]
    H += T.splats(pts, 0.018) * 0.9
    G += T.splats(pts, 0.03) * 0.6
    for k in range(6):
        a = TAU * t / 2 + TAU * k / 6
        x, y = 0.4 * math.cos(a), 0.35 + 0.1 * math.sin(a)
        G += T.lines([(x - 0.03, y - 0.02, x + 0.03, y + 0.02, 1.0), (x - 0.03, y + 0.02, x + 0.03, y - 0.02, 1.0)], 0.01) * 0.9
    G += T.ring(0.4, 0.01, 0, 0.35, 4.0) * 0.6
    return G, H


def onda_sismica(T, t, rng):
    """A onda sísmica: o soco no chão, as rachaduras correm para os lados, a onda de fogo e as pedras subindo
    (Paralisado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    bate = pulso(t, 0.0, 0.25)
    H += T.gauss(0, 0.25, 0.15, 0.06) * bate * 1.8
    corre = rel(t, 0.05, 0.4)
    if corre > 0:
        b = 1 - rel(t, 0.7, 0.95)
        q = np.random.default_rng(12)
        for lado in (-1, 1):
            for k in range(2):
                fim = 0.1 + 0.8 * ease_out(corre, 2)
                G += T.polyline(jagged(q, 0, 0.25, lado * fim, 0.25 + (k - 0.5) * 0.12 * fim, 4, 0.2), 0.012) * b * 1.3
    fogo = rel(t, 0.15, 0.75)
    if 0 < fogo < 1:
        g = ease_out(fogo, 2)
        for lado in (-1, 1):
            x = lado * (0.1 + 0.75 * g)
            G += T.gauss(x, 0.15, 0.08, 0.14) * (1 - fogo) * 1.4
            H += T.gauss(x, 0.18, 0.04, 0.07) * (1 - fogo) * 1.3
    pedras = rel(t, 0.15, 0.7)
    if 0 < pedras < 1:
        q = np.random.default_rng(5)
        shapes = []
        for _ in range(10):
            x0 = q.uniform(-0.7, 0.7)
            y = 0.25 - 0.5 * math.sin(math.pi * pedras) * q.uniform(0.4, 1)
            shapes.append((_gira([(-0.03, -0.02), (0.03, -0.03), (0.035, 0.02), (-0.02, 0.03)], pedras * 6 + x0, x0, y), 1.0))
        G += T.polys(shapes) * (1 - pedras) * 1.1
    para = pulso(t, 0.5, 1.0)
    if para > 0:
        q = np.random.default_rng(int(t * 25) % 5)
        for x in (-0.5, 0.0, 0.5):
            G += T.polyline(jagged(q, x - 0.08, -0.2, x + 0.08, -0.25, 3, 0.4), 0.008) * para
    return G * env, H * env


# =================================================================== Solid Snake
def camuflagem(T, t, rng):
    """A camuflagem: a caixa de papelão cai, a camuflagem óptica tremula em faixas e o tiro sai do esconderijo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    cai = ease_in(rel(t, 0.0, 0.18), 2)
    some = 1 - rel(t, 0.45, 0.65)
    if cai > 0 and some > 0:
        y = -0.6 + 0.65 * cai
        caixa = [(-0.22, y - 0.14), (0.22, y - 0.14), (0.22, y + 0.14), (-0.22, y + 0.14)]
        P = T.polys([(caixa, 1.0)])
        G += (P * 0.35 + _borda(T, P, 0.007) * 1.2) * some
        G += T.lines([(-0.22, y - 0.14, -0.3, y - 0.22, 1.0), (0.22, y - 0.14, 0.3, y - 0.22, 1.0), (0, y - 0.14, 0, y + 0.14, 0.6)], 0.01) * some
    faixa = pulso(t, 0.4, 0.9)
    if faixa > 0:
        for k in range(7):
            y = -0.3 + 0.1 * k + 0.02 * math.sin(t * 40 + k)
            dx = 0.04 * math.sin(t * 30 + k * 2)
            G += T.lines([(-0.25 + dx, y, 0.25 + dx, y, 1.0)], 0.012) * faixa * (0.5 + 0.5 * ((k + int(t * 20)) % 2))
    tiro = pulso(t, 0.6, 0.8)
    if tiro > 0:
        G += T.flare(0.3, -0.05, 0.2, 0, 0.03) * tiro + T.tapered([(0.3, -0.05, 0.9, -0.1, 1.0)], 0.015) * tiro
        H += T.gauss(0.3, -0.05, 0.04) * tiro * 1.5
    return G * env, H * env


def tiro_de_flanco(T, t, rng):
    """O tiro de flanco: a mira laser vermelha cruza o campo e para no rival, o tiro com silenciador e o
    impacto (Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    mira = rel(t, 0.0, 0.3)
    if t < 0.45:
        ty = 0.3 * (1 - ease_out(mira, 3)) * math.sin(t * 25)
        G += T.lines([(-0.95, -0.3, 0.0, ty, 1.0)], 0.011) * 1.6 + T.blur(T.lines([(-0.95, -0.3, 0.0, ty, 1.0)], 0.011), 0.02) * 0.8
        H += T.gauss(0.0, ty, 0.02) * 1.6
    tiro = rel(t, 0.38, 0.48)
    if 0 < tiro < 1:
        x = -0.95 + 0.95 * tiro
        G += T.tapered([(x - 0.3, -0.3 + 0.3 * max(0, tiro - 0.3), x, -0.3 + 0.3 * tiro, 1.0)], 0.02) * 1.5
    bate = rel(t, 0.46, 0.85)
    if bate > 0:
        g = ease_out(bate, 3)
        G += T.flare(0, 0, 0.35 * (1 - bate) + 0.05, 0.4, 0.02) * (1 - bate) * 1.4 + T.ring(0.05 + 0.25 * g, 0.02, 0, 0) * (1 - bate)
        H += T.gauss(0, 0, 0.04) * (1 - bate) * 2
    exposto = pulso(t, 0.6, 1.0)
    if exposto > 0:
        G += T.ring(0.18, 0.01, 0, 0) * exposto + T.lines([(-0.24, 0, -0.14, 0, 1.0), (0.14, 0, 0.24, 0, 1.0), (0, -0.24, 0, -0.14, 1.0), (0, 0.14, 0, 0.24, 1.0)], 0.01) * exposto
    return G * env, H * env


# =================================================================== Raiden (Metal Gear)
def corte_em_sequencia(T, t, rng):
    """O corte em sequência: os cortes da lâmina de alta frequência em sequência rápida, com as imagens de rastro
    e as faíscas elétricas (Acelerado)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    q = np.random.default_rng(41)
    for k in range(7):
        t0 = 0.03 + 0.06 * k
        u = rel(t, t0, t0 + 0.1)
        if u > 0:
            b = 1 - rel(t, t0 + 0.12, t0 + 0.3)
            if b <= 0:
                continue
            a = q.uniform(-math.pi, math.pi)
            c, s = math.cos(a) * 0.55, math.sin(a) * 0.55
            G += T.polys([(lamina(-c, -s, c, s, 0.03, u), 1.0)]) * b * 1.3
            H += T.lines([(-c * u, -s * u, c * u, s * u, 1.0)], 0.005) * b * 1.4
            qq = np.random.default_rng(k + int(t * 30))
            G += T.polyline(jagged(qq, 0, 0, 0.25 * c, 0.25 * s, 3, 0.4), 0.006) * b * 0.8
    return G * env, H * env


def raiden_preparo(T, t, rng):
    """O Preparo do Zandatsu: o Modo lâmina — a grade azul do tempo lento e a lâmina vibrando com a eletricidade
    (laço)."""
    G, H = vazio(T)
    segs = []
    for k in range(-4, 5):
        segs += [(k * 0.12, -0.5, k * 0.12, 0.5, 0.5), (-0.5, k * 0.12, 0.5, k * 0.12, 0.5)]
    G += T.lines(segs, 0.004) * (0.4 + 0.2 * math.sin(TAU * t * 2))
    vib = 0.01 * math.sin(t * 120)
    lam = lamina(-0.4, 0.2 + vib, 0.4, -0.2 + vib, 0.03)
    G += T.polys([(lam, 1.0)]) * 1.0
    H += T.lines([(-0.35, 0.18 + vib, 0.35, -0.18 + vib, 1.0)], 0.006) * 1.2
    q = np.random.default_rng(int(t * 16) % 7 + 1)
    for _ in range(2):
        x = q.uniform(-0.3, 0.3)
        G += T.polyline(jagged(q, x, -0.15 * x / 0.3 * 0.5, x + 0.1, 0.1, 3, 0.4), 0.006) * 0.9
    return G, H


def zandatsu(T, t, rng):
    """O Zandatsu: o plano do corte varre o campo, dezenas de cortes precisos aparecem e a explosão elétrica
    estoura (Paralisado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    varre = rel(t, 0.0, 0.2)
    if 0 < varre < 1:
        x = -1 + 2 * varre
        G += T.gauss(x, 0, 0.03, 0.9) * 1.2
        H += T.lines([(x, -0.9, x, 0.9, 1.0)], 0.006) * 1.5
    q = np.random.default_rng(53)
    for k in range(18):
        t0 = 0.12 + 0.012 * k
        u = rel(t, t0, t0 + 0.05)
        if u > 0:
            b = 1 - rel(t, 0.42, 0.55)
            a = q.uniform(0, math.pi)
            cx, cy = q.uniform(-0.5, 0.5), q.uniform(-0.3, 0.3)
            c, s = math.cos(a) * 0.35, math.sin(a) * 0.35
            G += T.lines([(cx - c * u, cy - s * u, cx + c * u, cy + s * u, 1.0)], 0.006) * b * 1.3
    boom = rel(t, 0.45, 0.9)
    if boom > 0:
        g = ease_out(boom, 3)
        G += T.gauss(0, 0, 0.15 + 0.4 * g) * (1 - boom) * 1.3 + T.ring(0.1 + 0.7 * g, 0.03, 0, 0) * (1 - boom)
        H += T.gauss(0, 0, 0.08 + 0.1 * g) * (1 - boom) * 1.6
        qq = np.random.default_rng(int(t * 25) % 6 + 2)
        for k in range(6):
            a = TAU * k / 6 + 0.3
            G += T.polyline(jagged(qq, 0, 0, (0.3 + 0.4 * g) * math.cos(a), (0.3 + 0.4 * g) * math.sin(a), 3, 0.35), 0.008) * (1 - boom) * 1.2
    return G * env, H * env


# =================================================================== Leon S. Kennedy
def mira_firme(T, t, rng):
    """A mira firme: o ponto do laser dança, para na cabeça do rival e a mira trava (Marcado, Preparo atrasado)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    para = ease_out(rel(t, 0.0, 0.45), 2.5)
    x = 0.25 * (1 - para) * math.sin(t * 17)
    y = -0.25 + 0.2 * (1 - para) * math.cos(t * 13)
    G += T.lines([(-0.95, 0.3, x, y, 1.0)], 0.005) * 0.9
    H += T.gauss(x, y, 0.025) * 1.8
    G += T.gauss(x, y, 0.06) * 0.6
    trava = pulso(t, 0.45, 1.0)
    if trava > 0:
        r = 0.16 + 0.1 * (1 - rel(t, 0.45, 0.6))
        G += T.ring(r, 0.012, 0, -0.25) * trava * 1.2
        G += T.lines([(-r - 0.06, -0.25, -r + 0.03, -0.25, 1.0), (r - 0.03, -0.25, r + 0.06, -0.25, 1.0), (0, -0.25 - r - 0.06, 0, -0.25 - r + 0.03, 1.0), (0, -0.25 + r - 0.03, 0, -0.25 + r + 0.06, 1.0)], 0.01) * trava
        atraso = pulso(t, 0.6, 1.0)
        G += T.arc_band(0.28, 0.02, -math.pi / 2, -math.pi / 2 - 2.0 * rel(t, 0.6, 1.0), cx=0, cy=0.2, taper=0.0) * atraso
    return G * env, H * env


def tiro_na_cabeca(T, t, rng):
    """O tiro na cabeça: o tiro cruza, o clarão na altura da cabeça e o rival cambaleia, com o anel de lentidão."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    voa = rel(t, 0.05, 0.2)
    if 0 < voa < 1:
        x = -0.9 + 0.9 * voa
        G += T.tapered([(x - 0.4, -0.25, x, -0.25, 1.0)], 0.022) * 1.5
        H += T.gauss(x, -0.25, 0.02) * 1.5
    if t < 0.12:
        G += T.flare(-0.9, -0.25, 0.25, 0, 0.03) * (1 - t / 0.12)
    bate = rel(t, 0.2, 0.55)
    if bate > 0:
        g = ease_out(bate, 3)
        G += T.flare(0, -0.25, 0.45 * (1 - bate) + 0.02, 0.3, 0.02) * (1 - bate) * 1.6
        H += T.gauss(0, -0.25, 0.04) * (1 - bate) * 2
        q = np.random.default_rng(9)
        segs = [(0, -0.25, (0.1 + 0.25 * g) * math.cos(a), -0.25 + (0.1 + 0.25 * g) * math.sin(a), 1.0) for a in q.uniform(-0.8, 0.8, 7)]
        G += T.tapered(segs, 0.018) * (1 - bate)
    zonzo = pulso(t, 0.45, 1.0)
    if zonzo > 0:
        for k in range(3):
            a = TAU * k / 3 + t * 8
            G += T.gauss(0.18 * math.cos(a), -0.42 + 0.05 * math.sin(a), 0.018) * zonzo * 1.4
        G += T.ring(0.3, 0.015, 0, 0.1, 2.0) * zonzo
    return G * env, H * env


def leon_preparo(T, t, rng):
    """O Preparo da Faca de combate: a faca sendo sacada, com o brilho que corre pela lâmina (laço)."""
    G, H = vazio(T)
    lam = [(-0.05, 0.2), (0.25, -0.15), (0.3, -0.25), (0.22, -0.18), (-0.02, 0.24)]
    cabo = [(-0.05, 0.2), (-0.02, 0.24), (-0.18, 0.4), (-0.22, 0.36)]
    L = T.polys([(lam, 1.0)])
    G += L * 0.6 + _borda(T, L, 0.006) * 1.2 + T.polys([(cabo, 0.6)]) * 0.5
    u = (t * 1.5) % 1
    x, y = -0.05 + 0.33 * u, 0.2 - 0.43 * u
    H += T.gauss(x, y, 0.03) * 1.8
    G += T.flare(x, y, 0.15, 0.6, 0.03) * 0.8
    return G, H


def faca_de_combate(T, t, rng):
    """A faca de combate: os dois cortes em X, a faísca do aparo e o Preparo do rival quebrando em cacos."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for k, (a, t0) in enumerate(((0.7, 0.0), (-0.7, 0.12))):
        u = rel(t, t0, t0 + 0.12)
        if u > 0:
            b = 1 - rel(t, t0 + 0.25, t0 + 0.5)
            c, s = math.cos(a) * 0.5, math.sin(a) * 0.5
            G += T.polys([(lamina(-c, -s, c, s, 0.05, u), 1.0)]) * b * 1.4
            H += T.lines([(-c * u * 0.8, -s * u * 0.8, c * u * 0.8, s * u * 0.8, 1.0)], 0.006) * b * 1.4
    faisca = pulso(t, 0.22, 0.45)
    if faisca > 0:
        G += T.flare(0, 0, 0.35, 0.3, 0.02) * faisca * 1.4
        H += T.gauss(0, 0, 0.04) * faisca * 2
    quebra = rel(t, 0.35, 0.9)
    if quebra > 0:
        q = np.random.default_rng(19)
        shapes = []
        for _ in range(10):
            a = q.uniform(0, TAU)
            r = 0.15 + 0.4 * ease_out(quebra, 2)
            cx, cy = r * math.cos(a), -0.3 + r * math.sin(a) * 0.6 + 0.3 * quebra * quebra
            shapes.append((_gira([(0, -0.035), (0.03, 0.02), (-0.03, 0.025)], a + 5 * quebra, cx, cy), 1.0))
        G += T.polys(shapes) * (1 - quebra) * 1.2
    return G * env, H * env


REGISTRO = [
    ("escudo_de_energia", escudo_de_energia, GRANDE, "Master Chief · a bolha dourada de hexágonos", False),
    ("fogo_de_supressao", fogo_de_supressao, GRANDE, "Master Chief · a rajada do fuzil e as setas", False),
    ("masterchief_preparo", masterchief_preparo, MEDIA, "Master Chief · o escudo enchendo (Preparo, laço)", True),
    ("posicao_firme", posicao_firme, GRANDE, "Master Chief · o pisão e a onda de choque", False),
    ("avanco_brutal", avanco_brutal, GRANDE, "Doom Slayer · a investida e o soco brutal", False),
    ("blindagem_de_combate", blindagem_de_combate, GRANDE, "Doom Slayer · as placas da armadura encaixando", False),
    ("doomslayer_preparo", doomslayer_preparo, MEDIA, "Doom Slayer · o punho em chamas e as runas (Preparo, laço)", True),
    ("onda_sismica", onda_sismica, GRANDE, "Doom Slayer · as rachaduras, o fogo e as pedras", False),
    ("camuflagem", camuflagem, GRANDE, "Snake · a caixa, a camuflagem e o tiro", False),
    ("tiro_de_flanco", tiro_de_flanco, GRANDE, "Snake · a mira laser e o tiro silenciado", False),
    ("corte_em_sequencia", corte_em_sequencia, GRANDE, "Raiden · os cortes em sequência", False),
    ("raiden_preparo", raiden_preparo, MEDIA, "Raiden · o Modo lâmina (Preparo, laço)", True),
    ("zandatsu", zandatsu, GRANDE, "Raiden · o plano do corte e a explosão elétrica", False),
    ("mira_firme", mira_firme, GRANDE, "Leon · o laser e a mira travando", False),
    ("tiro_na_cabeca", tiro_na_cabeca, GRANDE, "Leon · o tiro na cabeça e o rival zonzo", False),
    ("leon_preparo", leon_preparo, MEDIA, "Leon · a faca sacada (Preparo, laço)", True),
    ("faca_de_combate", faca_de_combate, GRANDE, "Leon · os cortes em X e o Preparo quebrando", False),
]
