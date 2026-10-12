"""Rodada 19 das habilidades próprias: Ganondorf, Samus Aran, Dante, Vergil e Bayonetta.

Ganondorf
- poder_da_triade: o triângulo da Força (o de cima da Triforce) acende dourado sobre os rivais, a sombra desce
  sobre eles com as setas de fraqueza, e o escudo escuro e dourado fecha em volta do trio.
- ganondorf_preparo: o Preparo do Juízo do Rei — a energia de trevas girando no punho fechado, com o triângulo
  da Força pulsando atrás (laço).
- juizo_do_rei: as colunas de trevas descem do alto sobre os rivais, com os raios roxos e o selo que cala
  (Silenciado) no fim.

Samus Aran
- trava_de_mira: a mira do visor: os quatro cantos fecham no rival, o retículo gira e trava, a linha de
  varredura passa e o alvo pisca (Marcado e Exposto).
- missil_de_contencao: o míssil cruza o campo com a fumaça, explode laranja no rival e o anel azul de lentidão
  fica em volta (o Preparo atrasado e o Lento).
- samus_preparo: o Preparo do Charge Beam — a bola de energia crescendo na boca do canhão, com as partículas
  sendo sugadas e os anéis (laço).
- charge_beam: a bola carregada voa enorme com o rastro grosso, e o impacto explode com a onda.

Dante
- ebony_e_ivory: as duas pistolas, uma de cada lado, em saraivada: os riscos dos tiros se cruzando, os clarões
  das bocas e as faíscas nos rivais (Exposto).
- dante_preparo: o Preparo do Devil Trigger — os raios vermelhos em volta e as asas de demônio piscando (laço).
- devil_trigger: a forma de demônio: as asas vermelhas se abrem, o Stinger atravessa o rival e explode em
  vermelho.

Vergil
- yamato: o saque-relâmpago: o clarão, os cortes finos aparecem depois, um a um, e as espadas espectrais azuis
  cravam em volta do rival (Marcado e Exposto).
- vergil_preparo: o Preparo do Judgement Cut End — a bainha da Yamato e as espadas espectrais girando devagar
  (laço).
- judgement_cut_end: dezenas de cortes finos cobrem o campo de uma vez e o espaço se parte em cacos.

Bayonetta
- danca_da_bruxa: os chutes em giro com os arcos de rastro e as borboletas roxas (Acelerado).
- witch_time: o relógio roxo aparece, os ponteiros desaceleram e a onda de tempo lento passa pelos rivais.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .rodada13 import _borda, _gira


def _tri(cx, cy, r, ang=-math.pi / 2):
    """Triângulo equilátero de raio r (a ponta para cima por padrão)."""
    return [(cx + r * math.cos(ang + TAU * k / 3), cy + r * math.sin(ang + TAU * k / 3)) for k in range(3)]


def _setas_baixo(T, u, xs=(-0.45, 0.45), y0=-0.1):
    segs = []
    for x in xs:
        y = y0 + 0.25 * u
        segs += [(x - 0.06, y - 0.05, x, y + 0.01, 1.0), (x + 0.06, y - 0.05, x, y + 0.01, 1.0), (x, y - 0.12, x, y, 1.0)]
    return T.lines(segs, 0.014)


def _selo_silencio(T, cx, cy, r):
    """O selo que cala: o círculo com o risco atravessado."""
    a = math.pi / 4
    return T.ring(r, 0.012, cx, cy) + T.lines([(cx - r * math.cos(a), cy - r * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a), 1.0)], 0.014)


# =================================================================== Ganondorf
def poder_da_triade(T, t, rng):
    """O poder da Tríade: o triângulo da Força acende dourado no alto, a sombra desce sobre os rivais com as setas
    de fraqueza (Enfraquecido), e o escudo escuro e dourado fecha em volta (Escudo no trio)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    acende = ease_out(rel(t, 0.0, 0.25), 2.5)
    if acende > 0:
        b = 1 - rel(t, 0.7, 0.9)
        P = T.polys([(_tri(0, -0.42, 0.26 * (0.6 + 0.4 * acende)), 1.0)])
        G += (P * 0.45 + _borda(T, P, 0.008) * 1.5) * acende * b
        H += _borda(T, P, 0.006) * acende * b * (0.7 + 0.3 * math.sin(t * 30))
        G += T.gauss(0, -0.4, 0.25) * acende * b * 0.25
    desce = rel(t, 0.2, 0.6)
    if 0 < desce < 1:
        y = -0.4 + 0.5 * ease_in(desce, 1.5)
        S = T.gauss(0, y, 0.6, 0.08) * (1 - desce)
        G += S * 0.6
        q = np.random.default_rng(int(t * 18) % 5 + 3)
        for k in range(4):
            x0 = -0.6 + 0.4 * k
            G += T.polyline(jagged(q, x0, -0.4, x0 + 0.05, y + 0.1, 3, 0.3), 0.01) * (1 - desce) * 0.8
    fraco = pulso(t, 0.4, 0.9)
    if fraco > 0:
        G += _setas_baixo(T, rel(t, 0.4, 0.9)) * fraco
    fecha = ease_out(rel(t, 0.5, 0.75), 3)
    if fecha > 0:
        b = 1 - rel(t, 0.85, 0.98)
        G += T.ring(0.42 * fecha, 0.03, 0, 0.1) * b * 1.2 + T.ring(0.36 * fecha, 0.012, 0, 0.1) * b * 0.6
        for k in range(3):
            a = TAU * k / 3 - math.pi / 2 + t * 2
            P = T.polys([(_tri(0.42 * fecha * math.cos(a), 0.1 + 0.42 * fecha * math.sin(a), 0.05), 1.0)])
            H += P * b
    return G * env, H * env


def ganondorf_preparo(T, t, rng):
    """O Preparo do Juízo do Rei: a energia de trevas girando no punho fechado, o triângulo da Força pulsando atrás
    e as faíscas roxas subindo (laço)."""
    G, H = vazio(T)
    p = 0.6 + 0.4 * math.sin(TAU * t * 2)
    Tr = T.polys([(_tri(0, -0.05, 0.42), 1.0)])
    G += _borda(T, Tr, 0.01) * 0.7 * p + Tr * 0.08
    P, nos = _punho(T, 0.0, 0.05, 1.6, -math.pi / 2)
    G += P * 0.35 + _borda(T, P, 0.008) * 0.9
    H += nos * 0.6
    for k in range(3):
        a0 = TAU * t + TAU * k / 3
        G += T.arc_band(0.3, 0.03, a0, a0 + 1.6, cx=0, cy=0.05, squash=1.0) * 0.9
    q = np.random.default_rng(int(t * 12) % 6 + 2)
    pts = [(q.uniform(-0.4, 0.4), 0.4 - ((t * 1.5 + q.uniform(0, 1)) % 1) * 0.8, q.uniform(0.4, 1)) for _ in range(14)]
    H += T.splats(pts, 0.012) * 0.8
    return G, H


def juizo_do_rei(T, t, rng):
    """O juízo do rei: as colunas de trevas descem do alto sobre os rivais com os raios roxos, a onda escura
    explode embaixo e o selo que cala aparece (Silenciado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for k, x in enumerate((-0.5, 0.0, 0.5)):
        cai = rel(t, 0.05 + 0.06 * k, 0.22 + 0.06 * k)
        some = 1 - rel(t, 0.5 + 0.04 * k, 0.75 + 0.04 * k)
        if cai > 0 and some > 0:
            fundo = -1.0 + 1.1 * ease_in(cai, 1.6)
            G += T.polys([([(x - 0.09, -1.0), (x + 0.09, -1.0), (x + 0.06, fundo), (x - 0.06, fundo)], 1.0)], 0.02) * some * 0.9
            H += T.lines([(x, -1.0, x, fundo, 1.0)], 0.02) * some * 0.8
            q = np.random.default_rng(int(t * 20) % 7 + k)
            G += T.polyline(jagged(q, x, -1.0, x + 0.02, fundo, 4, 0.25), 0.01) * some * 1.2
            if cai >= 1:
                g = rel(t, 0.22 + 0.06 * k, 0.55 + 0.06 * k)
                G += T.ring(0.05 + 0.25 * ease_out(g, 3), 0.025, x, 0.1, 2.2) * (1 - g) * 1.3
                H += T.gauss(x, 0.1, 0.07) * (1 - g) * 1.2
    selo = pulso(t, 0.55, 1.0)
    if selo > 0:
        G += _selo_silencio(T, 0, -0.35, 0.12) * selo * 1.2
    return G * env, H * env


# =================================================================== Samus
def trava_de_mira(T, t, rng):
    """A trava de mira: os quatro cantos fecham no rival, o retículo gira e trava, a varredura passa e o alvo
    pisca (Marcado e Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    fecha = ease_out(rel(t, 0.0, 0.35), 3)
    d = 0.75 - 0.4 * fecha
    c = 0.12
    segs = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * d, sy * d * 0.9
            segs += [(x, y, x - sx * c, y, 1.0), (x, y, x, y - sy * c, 1.0)]
    G += T.lines(segs, 0.016) * 1.2
    gira = rel(t, 0.15, 0.5)
    if gira > 0:
        a = (1 - ease_out(gira, 3)) * math.pi
        R = T.ring(0.2, 0.01, 0, 0)
        cruz = [_gira([(0.12, 0), (0.3, 0)], a + math.pi * k / 2) for k in range(4)]
        G += (R + sum(T.lines([(p[0][0], p[0][1], p[1][0], p[1][1], 1.0)], 0.012) for p in cruz)) * min(1, gira * 3)
    varre = rel(t, 0.3, 0.6)
    if 0 < varre < 1:
        y = -0.4 + 0.8 * varre
        G += T.lines([(-0.4, y, 0.4, y, 1.0)], 0.01) * 1.2 + T.gauss(0, y, 0.4, 0.02) * 0.4
    trava = pulso(t, 0.5, 1.0)
    if trava > 0:
        pisca = 1.0 if int(t * 14) % 2 == 0 else 0.4
        H += T.gauss(0, 0, 0.05) * trava * pisca * 1.5
        G += T.ring(0.08, 0.012, 0, 0) * trava * pisca * 1.2
    return G * env, H * env


def missil_de_contencao(T, t, rng):
    """O míssil de contenção: o míssil cruza com a fumaça, explode laranja no rival e o anel azul de lentidão fica
    em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    voa = rel(t, 0.0, 0.3)
    if voa < 1:
        x = -0.9 + 0.9 * ease_in(voa, 1.4)
        corpo = [(x - 0.3, -0.04), (x - 0.06, -0.04), (x, 0.0), (x - 0.06, 0.04), (x - 0.3, 0.04)]
        aletas = [[(x - 0.3, -0.04), (x - 0.22, -0.04), (x - 0.34, -0.1)], [(x - 0.3, 0.04), (x - 0.22, 0.04), (x - 0.34, 0.1)]]
        C = T.polys([(corpo, 1.0)] + [(a, 0.8) for a in aletas])
        G += C * 0.7 + _borda(T, C, 0.006) * 1.3
        H += T.gauss(x - 0.33, 0.0, 0.04) * 1.8 + T.gauss(x - 0.03, 0.0, 0.02) * 0.8
        q = np.random.default_rng(5)
        pts = [(x - 0.36 - q.uniform(0, 0.6), q.normal(0, 0.035), q.uniform(0.3, 0.8)) for _ in range(28)]
        G += T.splats(pts, 0.035) * 0.7
    boom = rel(t, 0.3, 0.7)
    if boom > 0:
        g = ease_out(boom, 2.5)
        G += T.gauss(0, 0, 0.1 + 0.25 * g) * (1 - boom) * 1.4
        H += T.gauss(0, 0, 0.06 + 0.1 * g) * (1 - boom) * 1.8
        G += T.ring(0.08 + 0.4 * g, 0.03, 0, 0) * (1 - boom)
        q = np.random.default_rng(11)
        segs = []
        for _ in range(12):
            a = q.uniform(0, TAU)
            r0, r1 = 0.1 + 0.2 * g, 0.18 + 0.45 * g
            segs.append((r0 * math.cos(a), r0 * math.sin(a), r1 * math.cos(a), r1 * math.sin(a), 1.0))
        G += T.tapered(segs, 0.02) * (1 - boom)
    lento = pulso(t, 0.55, 1.0)
    if lento > 0:
        G += T.ring(0.3, 0.018, 0, 0.05, 2.0) * lento
        for k in range(6):
            a = TAU * k / 6 + t * 1.5
            H += T.gauss(0.3 * math.cos(a), 0.05 + 0.15 * math.sin(a), 0.015) * lento
    return G * env, H * env


def samus_preparo(T, t, rng):
    """O Preparo do Charge Beam: a bola de energia crescendo, as partículas sendo sugadas e os anéis (laço)."""
    G, H = vazio(T)
    p = 0.5 + 0.5 * math.sin(TAU * t * 3)
    G += T.gauss(0, 0, 0.12 + 0.02 * p) * 1.2
    H += T.gauss(0, 0, 0.06 + 0.015 * p) * 1.6
    for k in range(2):
        r = 0.45 - ((t * 1.6 + k * 0.5) % 1) * 0.35
        G += T.ring(r, 0.012, 0, 0) * (1 - abs(r - 0.28) / 0.2) * 0.8
    q = np.random.default_rng(7)
    segs = []
    for _ in range(14):
        a = q.uniform(0, TAU)
        f = (t * 2 + q.uniform(0, 1)) % 1
        r = 0.6 - 0.45 * f
        segs.append((1.15 * r * math.cos(a), 1.15 * r * math.sin(a), r * math.cos(a), r * math.sin(a), 1 - f))
    G += T.tapered(segs, 0.012) * 0.9
    return G, H


def charge_beam(T, t, rng):
    """O Charge Beam: a bola carregada voa enorme com o rastro grosso e o impacto explode com a onda."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    voa = rel(t, 0.0, 0.28)
    if voa < 1:
        x = -0.9 + 0.9 * ease_in(voa, 1.5)
        G += T.gauss(x, 0, 0.11) * 1.3 + T.tapered([(x - 0.7, 0, x, 0, 1.0)], 0.18) * 0.6
        H += T.gauss(x, 0, 0.06) * 1.8
    bate = rel(t, 0.28, 0.75)
    if bate > 0:
        g = ease_out(bate, 3)
        G += T.gauss(0, 0, 0.12 + 0.35 * g) * (1 - bate) * 1.6
        H += T.gauss(0, 0, 0.08 + 0.15 * g) * (1 - bate) * 2.0
        G += T.ring(0.1 + 0.6 * g, 0.04, 0, 0) * (1 - bate) * 1.2 + T.ring(0.05 + 0.4 * g, 0.02, 0, 0) * (1 - bate)
        if bate < 0.98:
            G += (T.flare(0, 0, 0.9 * (1 - bate), 0, 0.012) + T.flare(0, 0, 0.6 * (1 - bate), math.pi / 4, 0.012)) * 1.2
    return G * env, H * env


# =================================================================== Dante
def ebony_e_ivory(T, t, rng):
    """Ebony e Ivory: as duas pistolas em saraivada, uma de cada lado: os riscos dos tiros se cruzando, os clarões
    das bocas e as faíscas nos rivais (Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    q = np.random.default_rng(3)
    for k in range(14):
        t0 = 0.03 + 0.045 * k
        u = rel(t, t0, t0 + 0.12)
        if 0 < u < 1:
            lado = -1 if k % 2 == 0 else 1
            sx, sy = lado * 0.68, -0.5 + q.uniform(-0.08, 0.08)
            tx, ty = q.uniform(-0.4, 0.4), q.uniform(-0.05, 0.25)
            hx, hy = sx + (tx - sx) * ease_in(u, 1.2), sy + (ty - sy) * ease_in(u, 1.2)
            cx, cy = sx + (tx - sx) * max(0, u - 0.35), sy + (ty - sy) * max(0, u - 0.35)
            G += T.tapered([(cx, cy, hx, hy, 1.0)], 0.026) * 1.6
            H += T.tapered([(cx, cy, hx, hy, 1.0)], 0.01) * 1.4
            if u < 0.4:
                G += T.flare(sx, sy, 0.22 * (1 - u / 0.4), 0.3 * lado, 0.03) * 1.4
                H += T.gauss(sx, sy, 0.05) * (1 - u / 0.4) * 1.8
            if u > 0.8:
                G += T.flare(tx, ty, 0.2, q.uniform(0, 1), 0.025) * 1.4
                H += T.gauss(tx, ty, 0.03) * 1.6
    exp = pulso(t, 0.55, 1.0)
    if exp > 0:
        G += T.ring(0.38, 0.012, 0, 0.08, 2.4) * exp * 0.8
    return G * env, H * env


def _asa(cx, cy, s, lado):
    """Asa de demônio: as pontas recortadas como de morcego."""
    pts = [(cx, cy), (cx + lado * 0.15 * s, cy - 0.25 * s), (cx + lado * 0.45 * s, cy - 0.35 * s), (cx + lado * 0.5 * s, cy - 0.05 * s),
           (cx + lado * 0.38 * s, cy + 0.02 * s), (cx + lado * 0.32 * s, cy + 0.15 * s), (cx + lado * 0.2 * s, cy + 0.08 * s),
           (cx + lado * 0.12 * s, cy + 0.18 * s)]
    return pts


def dante_preparo(T, t, rng):
    """O Preparo do Devil Trigger: os raios vermelhos em volta e as asas de demônio piscando (laço)."""
    G, H = vazio(T)
    pisca = 0.5 + 0.5 * math.sin(TAU * t * 2.5)
    for lado in (-1, 1):
        A = T.polys([(_asa(0, 0.0, 1.2, lado), 1.0)])
        G += (A * 0.15 + _borda(T, A, 0.008) * 1.0) * pisca
    q = np.random.default_rng(int(t * 15) % 6 + 4)
    for k in range(3):
        a = q.uniform(0, TAU)
        G += T.polyline(jagged(q, 0.15 * math.cos(a), 0.15 * math.sin(a), 0.5 * math.cos(a), 0.5 * math.sin(a), 3, 0.3), 0.01) * 1.1
    G += T.gauss(0, 0, 0.18) * 0.35
    H += T.gauss(0, 0, 0.07) * (0.6 + 0.4 * pisca)
    return G, H


def devil_trigger(T, t, rng):
    """O Devil Trigger: as asas vermelhas se abrem, o Stinger atravessa o rival como uma estocada e explode."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2.5)
    if abre > 0:
        b = 1 - rel(t, 0.55, 0.8)
        for lado in (-1, 1):
            A = T.polys([(_asa(-0.35, -0.1, 1.3 * abre, lado), 1.0)])
            G += (A * 0.2 + _borda(T, A, 0.008) * 1.2) * b
    sting = rel(t, 0.25, 0.45)
    if 0 < sting < 1:
        x = -0.8 + 1.4 * ease_in(sting, 1.3)
        G += T.polys([(lamina(x - 0.5, 0, x, 0, 0.05), 1.0)]) * 1.2 + rastro(T, x)
        H += T.lines([(x - 0.3, 0, x, 0, 1.0)], 0.012) * 1.6
    boom = rel(t, 0.42, 0.85)
    if boom > 0:
        g = ease_out(boom, 3)
        G += T.gauss(0, 0, 0.1 + 0.3 * g) * (1 - boom) * 1.5 + T.ring(0.1 + 0.5 * g, 0.035, 0, 0) * (1 - boom) * 1.2
        H += T.gauss(0, 0, 0.07 + 0.1 * g) * (1 - boom) * 1.8
        q = np.random.default_rng(13)
        segs = [(0, 0, (0.25 + 0.4 * g) * math.cos(a), (0.25 + 0.4 * g) * math.sin(a), 1.0) for a in q.uniform(0, TAU, 10)]
        G += T.tapered(segs, 0.025) * (1 - boom)
    return G * env, H * env


def rastro(T, x):
    """O rastro da estocada: as linhas de velocidade atrás da ponta."""
    return T.tapered([(x - 0.9, dy, x - 0.25, dy, 0.6) for dy in (-0.07, 0.07)], 0.015)


# =================================================================== Vergil
def _espada_espectral(cx, cy, ang, s=1.0):
    """A espada espectral do Vergil: a lâmina fina com a guarda curta."""
    lam = _gira([(-0.02 * s, 0), (0, -0.28 * s), (0.02 * s, 0)], ang, cx, cy)
    guarda = _gira([(-0.06 * s, 0.0), (0.06 * s, 0.0)], ang, cx, cy)
    cabo = _gira([(0, 0), (0, 0.07 * s)], ang, cx, cy)
    return lam, guarda, cabo


def yamato(T, t, rng):
    """A Yamato: o clarão do saque, os cortes finos que aparecem depois, um a um, e as espadas espectrais azuis
    cravando em volta do rival (Marcado e Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    flash = pulso(t, 0.0, 0.15)
    if flash > 0:
        H += T.lines([(-0.9, 0.0, 0.9, 0.0, 1.0)], 0.008) * flash * 2
        G += T.gauss(0, 0, 0.6, 0.03) * flash
    q = np.random.default_rng(17)
    for k in range(6):
        t0 = 0.15 + 0.05 * k
        u = rel(t, t0, t0 + 0.08)
        if u > 0:
            a = q.uniform(-1.2, 1.2)
            c, s = math.cos(a), math.sin(a)
            b = 1 - rel(t, t0 + 0.25, t0 + 0.4)
            G += T.polys([(lamina(-0.5 * c, -0.5 * s, 0.5 * c, 0.5 * s, 0.012, u), 1.0)]) * b * 1.4
            H += T.lines([(-0.4 * c * u, -0.4 * s * u, 0.4 * c * u, 0.4 * s * u, 1.0)], 0.004) * b * 1.5
    crava = rel(t, 0.45, 0.65)
    if crava > 0:
        b = 1 - rel(t, 0.85, 0.98)
        for k in range(5):
            a = TAU * k / 5 - math.pi / 2
            r = 0.55 - 0.2 * ease_out(crava, 3)
            cx, cy = r * math.cos(a), r * math.sin(a) * 0.8
            lam, guarda, cabo = _espada_espectral(cx, cy, a - math.pi / 2, 1.1)
            G += (T.polys([(lam, 1.0)]) * 0.9 + T.lines([(guarda[0][0], guarda[0][1], guarda[1][0], guarda[1][1], 1.0)], 0.012)) * b
            H += T.polys([(lam, 1.0)]) * b * 0.4
    return G * env, H * env


def vergil_preparo(T, t, rng):
    """O Preparo do Judgement Cut End: a bainha da Yamato no centro e as espadas espectrais girando devagar
    (laço)."""
    G, H = vazio(T)
    bainha = lamina(-0.35, 0.15, 0.35, -0.05, 0.025)
    G += T.polys([(bainha, 1.0)]) * 0.5 + _borda(T, T.polys([(bainha, 1.0)]), 0.006) * 0.8
    H += T.gauss(-0.32, 0.14, 0.03) * (0.6 + 0.4 * math.sin(TAU * t * 2))
    for k in range(6):
        a = TAU * t / 2 + TAU * k / 6
        cx, cy = 0.5 * math.cos(a), 0.35 * math.sin(a)
        lam, guarda, _ = _espada_espectral(cx, cy, a + math.pi, 0.8)
        G += T.polys([(lam, 1.0)]) * 0.8 + T.lines([(guarda[0][0], guarda[0][1], guarda[1][0], guarda[1][1], 1.0)], 0.01) * 0.8
        H += T.polys([(lam, 1.0)]) * 0.3
    return G, H


def judgement_cut_end(T, t, rng):
    """O Judgement Cut End: dezenas de cortes finos cobrem o campo de uma vez e o espaço se parte em cacos."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(23)
    cortes = [(q.uniform(-0.8, 0.8), q.uniform(-0.6, 0.6), q.uniform(0, math.pi), q.uniform(0.25, 0.6), q.uniform(0.02, 0.25)) for _ in range(26)]
    for cx, cy, a, L, t0 in cortes:
        u = rel(t, t0, t0 + 0.05)
        if u > 0:
            b = 1 - rel(t, 0.45, 0.6)
            c, s = math.cos(a) * L, math.sin(a) * L
            G += T.lines([(cx - c * u, cy - s * u, cx + c * u, cy + s * u, 1.0)], 0.006) * b * 1.3
            H += T.lines([(cx - c * u * 0.6, cy - s * u * 0.6, cx + c * u * 0.6, cy + s * u * 0.6, 1.0)], 0.003) * b * 1.2
    quebra = rel(t, 0.45, 0.95)
    if quebra > 0:
        g = ease_out(quebra, 2)
        H += T.gauss(0, 0, 0.5) * pulso(t, 0.43, 0.6) * 1.2
        q2 = np.random.default_rng(29)
        shapes = []
        for _ in range(18):
            a = q2.uniform(0, TAU)
            r = q2.uniform(0.1, 0.6) + 0.35 * g
            cx, cy = r * math.cos(a), r * math.sin(a) + 0.4 * g * g
            shapes.append((_gira([(0, -0.05), (0.04, 0.03), (-0.04, 0.04)], a + 4 * g, cx, cy), 1.0))
        P = T.polys(shapes)
        G += (P * 0.4 + _borda(T, P, 0.005) * 1.2) * (1 - quebra)
    return G * env, H * env


# =================================================================== Bayonetta
def _borboleta(T, cx, cy, s, bate):
    asa = lambda lado, dy, r: [(cx, cy), (cx + lado * r * s * bate, cy + dy * s - 0.04 * s), (cx + lado * r * s * bate * 0.8, cy + dy * s + 0.04 * s)]
    return T.polys([(asa(l, dy, r), 1.0) for l in (-1, 1) for dy, r in ((-0.03, 0.08), (0.04, 0.06))])


def danca_da_bruxa(T, t, rng):
    """A dança da bruxa: os chutes em giro com os arcos de rastro, os tiros dos saltos e as borboletas roxas
    subindo (Acelerado)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k in range(3):
        t0 = 0.0 + 0.13 * k
        u = rel(t, t0, t0 + 0.22)
        if 0 < u < 1:
            a0 = -math.pi + 0.9 * k
            G += T.arc_band(0.38 - 0.05 * k, 0.07, a0, a0 + 3.6 * ease_out(u, 2), cx=0, cy=0.05, squash=1.3, crescente=True) * (1 - u) * 1.4
            hx = 0.35 * math.cos(a0 + 3.6 * ease_out(u, 2))
            hy = 0.05 + 0.35 / 1.3 * math.sin(a0 + 3.6 * ease_out(u, 2))
            H += T.gauss(hx, hy, 0.03) * (1 - u) * 1.6
    for k in range(5):
        t0 = 0.35 + 0.06 * k
        u = rel(t, t0, t0 + 0.6)
        if 0 < u < 1:
            x = -0.45 + 0.22 * k + 0.05 * math.sin(u * 12 + k)
            y = 0.25 - 0.7 * u
            bate = 0.4 + 0.6 * abs(math.sin(u * 30 + k))
            G += _borboleta(T, x, y, 1.0, bate) * (1 - u) * 1.1
            H += T.gauss(x, y, 0.015) * (1 - u)
    return G * env, H * env


def witch_time(T, t, rng):
    """O Witch Time: o relógio roxo aparece, os ponteiros correm e desaceleram, e a onda de tempo lento passa pelos
    rivais deixando os ecos parados."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    surge = ease_out(rel(t, 0.0, 0.25), 3)
    if surge > 0:
        b = 1 - rel(t, 0.75, 0.95)
        r = 0.42 * surge
        G += T.ring(r, 0.02, 0, 0) * b * 1.2 + T.ring(r * 0.85, 0.008, 0, 0) * b * 0.7
        marcas = [(r * 0.78 * math.cos(TAU * k / 12), r * 0.78 * math.sin(TAU * k / 12), r * 0.9 * math.cos(TAU * k / 12), r * 0.9 * math.sin(TAU * k / 12), 1.0) for k in range(12)]
        G += T.lines(marcas, 0.01) * b
        # os ponteiros: rápidos no começo, quase parados no fim (o tempo freando)
        giro = 9 * (1 - (1 - min(1, t / 0.7)) ** 3)
        for comp, vel, larg in ((0.75, 1.0, 0.014), (0.5, 0.25, 0.02)):
            a = -math.pi / 2 + giro * vel
            G += T.lines([(0, 0, r * comp * math.cos(a), r * comp * math.sin(a), 1.0)], larg) * b * 1.2
        H += T.gauss(0, 0, 0.03) * b * 1.2
    onda = rel(t, 0.3, 0.8)
    if 0 < onda < 1:
        g = ease_out(onda, 2)
        G += T.ring(0.2 + 0.7 * g, 0.05, 0, 0) * (1 - onda) * 0.9
        G += T.gauss(0, 0, 0.9) * (1 - onda) * 0.15
    ecos = pulso(t, 0.45, 1.0)
    if ecos > 0:
        for k, x in enumerate((-0.55, 0.55)):
            for e in range(3):
                G += T.ring(0.09, 0.008, x - 0.04 * e, 0.25) * ecos * (0.8 - 0.25 * e)
    return G * env, H * env


REGISTRO = [
    ("poder_da_triade", poder_da_triade, GRANDE, "Ganondorf · o triângulo da Força, a sombra e o escudo", False),
    ("ganondorf_preparo", ganondorf_preparo, MEDIA, "Ganondorf · o punho de trevas e a Força (Preparo, laço)", True),
    ("juizo_do_rei", juizo_do_rei, GRANDE, "Ganondorf · as colunas de trevas e o selo que cala", False),
    ("trava_de_mira", trava_de_mira, GRANDE, "Samus · a mira do visor travando", False),
    ("missil_de_contencao", missil_de_contencao, GRANDE, "Samus · o míssil, a explosão e o anel de lentidão", False),
    ("samus_preparo", samus_preparo, MEDIA, "Samus · o canhão carregando (Preparo, laço)", True),
    ("charge_beam", charge_beam, GRANDE, "Samus · a bola carregada e o impacto", False),
    ("ebony_e_ivory", ebony_e_ivory, GRANDE, "Dante · a saraivada das duas pistolas", False),
    ("dante_preparo", dante_preparo, MEDIA, "Dante · os raios e as asas de demônio (Preparo, laço)", True),
    ("devil_trigger", devil_trigger, GRANDE, "Dante · as asas, o Stinger e a explosão", False),
    ("yamato", yamato, GRANDE, "Vergil · o saque, os cortes e as espadas espectrais", False),
    ("vergil_preparo", vergil_preparo, MEDIA, "Vergil · a bainha e as espadas girando (Preparo, laço)", True),
    ("judgement_cut_end", judgement_cut_end, GRANDE, "Vergil · os cortes no campo inteiro e os cacos", False),
    ("danca_da_bruxa", danca_da_bruxa, GRANDE, "Bayonetta · os chutes em giro e as borboletas", False),
    ("witch_time", witch_time, GRANDE, "Bayonetta · o relógio roxo e a onda de tempo lento", False),
]
