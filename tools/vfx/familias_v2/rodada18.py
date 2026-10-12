"""Rodada 18 das habilidades próprias: Shazam, Tifa Lockhart, Sephiroth, Link e Zelda.

Shazam
- raio_magico: o raio mágico desce do céu num zigue-zague grosso dourado, bate no rival com o símbolo do raio
  piscando, e o Shazam fica Fortalecido (a aura dourada).
- forca_de_hercules: o punho dourado ergue o escudo de força em volta do aliado, com os músculos de luz (os
  arcos dourados que pulsam) e as setas de força.
- shazam_preparo: o Preparo da Sabedoria de Salomão — as seis letras S-H-A-Z-A-M girando em volta, cada uma
  acendendo, com as faíscas (laço).
- sabedoria_de_salomao: o pergaminho de luz se abre, a runa da sabedoria acerta o rival e o Preparo dele quebra
  em pedaços dourados.

Tifa Lockhart
- golpe_de_abertura: dois jabs rápidos e o gancho, e a guarda do rival trinca (o escudo que racha).
- chuva_de_socos: os punhos em sequência, um atrás do outro, com as imagens de rastro e os estouros pequenos.
- tifa_preparo: o Preparo da Explosão final — os punhos de luva com a energia vermelha subindo e o chão
  tremendo em volta (laço).
- explosao_final: o soco final no chão, a coluna de energia sobe e a onda vermelha e dourada explode em volta.

Sephiroth
- corte_sombrio: o corte longuíssimo e escuro da Masamune atravessa o rival, e as penas negras caem.
- sephiroth_preparo: o Preparo do Heartless Angel — a asa negra única se abre e as penas caem devagar
  (laço).
- heartless_angel: o céu escurece, a asa enorme se abre no alto e a luz é drenada de todos os rivais em
  colunas roxas, deixando todos à beira da queda.

Link
- escudo_hyliano: o Escudo Hyliano (a forma com a Triforce e a ave) aparece, desvia o golpe com as faíscas, e o
  Link contra-ataca.
- link_preparo: o Preparo do Golpe giratório — a espada carregando com as faíscas subindo pela lâmina (laço).
- golpe_giratorio: o giro de 360° com o rastro azul da espada em volta, e o estouro de energia no fim.

Zelda
- selo_da_luz: o círculo de luz com a Triforce aparece debaixo do rival e o prende, com o clarão que cega.
- barreira_sagrada: o cristal de diamante do Amor de Nayru se forma em volta de cada aliado, girando e
  brilhando.
- zelda_preparo: o Preparo da Flecha de Luz — o arco de luz se forma e a flecha brilhante acende (laço).
- flecha_de_luz: a flecha de luz cruza o campo, acerta, e o selo sagrado cala o rival (Silenciado).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .rodada13 import _borda, _contorno, _gira


def _raio_simbolo(cx, cy, s):
    """O raio do peito do Shazam: o zigue-zague de três segmentos."""
    return [(cx - 0.05 * s, cy - 0.2 * s), (cx + 0.08 * s, cy - 0.2 * s), (cx + 0.0, cy - 0.02 * s), (cx + 0.09 * s, cy - 0.02 * s),
            (cx - 0.06 * s, cy + 0.22 * s), (cx - 0.01 * s, cy + 0.04 * s), (cx - 0.1 * s, cy + 0.04 * s)]


def _triforce(T, cx, cy, s):
    tri = lambda x, y, r: [(x, y - r), (x + r * 0.866, y + r * 0.5), (x - r * 0.866, y + r * 0.5)]
    r = 0.1 * s
    shapes = [(tri(cx, cy - r * 0.5, r), 1.0), (tri(cx - r * 0.866, cy + r, r), 1.0), (tri(cx + r * 0.866, cy + r, r), 1.0)]
    return T.polys(shapes)


# =================================================================== Shazam
def raio_magico(T, t, rng):
    """O raio mágico: o raio desce do céu em zigue-zague grosso e dourado, bate no rival com o símbolo do raio
    piscando, e o Shazam fica Fortalecido."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(int(t * 20) % 7 + 1)
    cai = rel(t, 0.1, 0.2)
    some = 1 - rel(t, 0.35, 0.55)
    if cai > 0 and some > 0:
        R = T.polyline(jagged(q, -0.1, -1.0, 0.0, -1.0 + 1.0 * min(1, cai), 4, 0.22), 0.04)
        G += (R * 1.2 + T.blur(R, 0.03) * 0.7) * some
        H += T.polyline(jagged(q, -0.1, -1.0, 0.0, -1.0 + 1.0 * min(1, cai), 4, 0.22), 0.012) * some * 1.5
    simb = pulso(t, 0.2, 0.75)
    if simb > 0:
        S = T.polys([(_raio_simbolo(0, 0, 1.4), 1.0)])
        G += (S * 0.6 + _borda(T, S, 0.006) * 1.3) * simb
        H += S * simb * (0.6 + 0.4 * math.cos(t * 40))
    g = rel(t, 0.18, 0.5)
    if 0 < g < 1:
        G += T.ring(0.08 + 0.35 * ease_out(g, 3), 0.035, 0, 0) * (1 - g) * 1.2
    aura = pulso(t, 0.5, 1.0)
    if aura > 0:
        G += T.ring(0.18, 0.02, -0.75, 0.1) * aura + T.gauss(-0.75, 0.1, 0.12) * aura * 0.3
    return G * env, H * env


def forca_de_hercules(T, t, rng):
    """A força de Hércules: o punho dourado enorme se ergue, os músculos de luz pulsam (os arcos dourados) e o
    escudo de força fecha em volta do aliado, com as setas de força subindo (Escudo, Protegido e Fortalecido)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    ergue = ease_out(rel(t, 0.0, 0.3), 2.5)
    if ergue > 0 and t < 0.6:
        b = 1 - rel(t, 0.45, 0.6)
        P, nos = _punho(T, 0.0, 0.45 - 0.55 * ergue, 2.4, -math.pi / 2)
        G += (P * 0.5 + _borda(T, P, 0.008) * 1.4) * b
        H += nos * b
    pulsa = pulso(t, 0.25, 0.7)
    if pulsa > 0:
        for k in range(3):
            G += T.arc_band(0.25 + 0.08 * k, 0.025, -2.6 + 0.2 * k, -0.5 - 0.2 * k, cx=0, cy=0.1, crescente=True) * pulsa * (1 - 0.2 * k)
    fecha = ease_out(rel(t, 0.45, 0.7), 3)
    if fecha > 0:
        G += T.ring(0.4 * fecha, 0.03, 0, 0.1) * (1 - rel(t, 0.85, 0.98)) * 1.2
        H += T.gauss(0, 0.1, 0.25 * fecha) * 0.2
        for x in (-0.2, 0.2):
            y = 0.25 - 0.25 * rel(t, 0.5, 0.9)
            G += T.lines([(x - 0.06, y + 0.05, x, y - 0.01, 1.0), (x + 0.06, y + 0.05, x, y - 0.01, 1.0), (x, y + 0.12, x, y, 1.0)], 0.014) * fecha
    return G * env, H * env


def _letra(cx, cy, s, ch):
    """As letras de SHAZAM em traços retos."""
    w, h = 0.05 * s, 0.08 * s
    L = {
        'S': [(cx + w, cy - h, cx - w, cy - h), (cx - w, cy - h, cx - w, cy), (cx - w, cy, cx + w, cy), (cx + w, cy, cx + w, cy + h), (cx + w, cy + h, cx - w, cy + h)],
        'H': [(cx - w, cy - h, cx - w, cy + h), (cx + w, cy - h, cx + w, cy + h), (cx - w, cy, cx + w, cy)],
        'A': [(cx - w, cy + h, cx, cy - h), (cx, cy - h, cx + w, cy + h), (cx - w * 0.5, cy + h * 0.2, cx + w * 0.5, cy + h * 0.2)],
        'Z': [(cx - w, cy - h, cx + w, cy - h), (cx + w, cy - h, cx - w, cy + h), (cx - w, cy + h, cx + w, cy + h)],
        'M': [(cx - w, cy + h, cx - w, cy - h), (cx - w, cy - h, cx, cy), (cx, cy, cx + w, cy - h), (cx + w, cy - h, cx + w, cy + h)],
    }[ch]
    return [(a, b, c, d, 1.0) for a, b, c, d in L]


def shazam_preparo(T, t, rng):
    """O Preparo da Sabedoria de Salomão: as seis letras S-H-A-Z-A-M girando em volta, cada uma acendendo por vez,
    com as faíscas do raio pulando entre elas (laço)."""
    G, H = vazio(T)
    for k, ch in enumerate('SHAZAM'):
        a = TAU * t / 3 + TAU * k / 6 - math.pi / 2
        x, y = 0.5 * math.cos(a), 0.05 + 0.42 * math.sin(a)
        acesa = 1.0 if int(t * 6) % 6 == k else 0.4
        Lt = T.lines(_letra(x, y, 1.6, ch), 0.014)
        G += Lt * (0.6 + 0.6 * acesa)
        H += Lt * acesa * 0.8
    q = np.random.default_rng(int(t * 12) % 5 + 9)
    a = q.uniform(0, TAU)
    x0, y0 = 0.5 * math.cos(a), 0.05 + 0.42 * math.sin(a)
    G += T.polyline(jagged(q, x0, y0, 0.0, 0.05, 3, 0.3), 0.01) * 1.2
    H += T.gauss(0, 0.05, 0.07) * (0.6 + 0.4 * math.sin(TAU * t * 2))
    return G, H


def sabedoria_de_salomao(T, t, rng):
    """A sabedoria de Salomão: o pergaminho de luz se abre (as duas pontas enroladas indo para os lados), a runa da
    sabedoria voa e acerta o rival, e o Preparo dele quebra em pedaços dourados."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.25), 2.5)
    if abre > 0 and t < 0.6:
        b = 1 - rel(t, 0.45, 0.6)
        cx, cy, w = -0.6, -0.1, 0.28 * abre
        G += T.lines(_contorno([(cx - w, cy - 0.15), (cx + w, cy - 0.15), (cx + w, cy + 0.15), (cx - w, cy + 0.15)]), 0.01) * b
        G += (T.ring(0.035, 0.012, cx - w, cy - 0.15) + T.ring(0.035, 0.012, cx + w, cy - 0.15) + T.ring(0.035, 0.012, cx - w, cy + 0.15) + T.ring(0.035, 0.012, cx + w, cy + 0.15)) * b
        for k in range(3):
            G += T.lines([(cx - w * 0.7, cy - 0.07 + 0.07 * k, cx + w * 0.7, cy - 0.07 + 0.07 * k, 0.6)], 0.006) * b * abre
        H += T.gauss(cx, cy, 0.15 * abre, 0.1) * 0.4 * b
    voa = rel(t, 0.25, 0.45)
    if 0 < voa < 1:
        x = -0.6 + 0.6 * ease_in(voa, 1.5)
        E = T.polys([(estrela(x, -0.1 + 0.1 * voa, 0.08, t * 10, 6, 0.4), 1.0)])
        G += E * 1.1
        H += E * 0.8
    quebra = rel(t, 0.42, 0.8)
    if 0 < quebra < 1:
        q = np.random.default_rng(13)
        cacos = [(_gira([(-0.04, -0.02), (0.045, -0.01), (0.0, 0.035)], q.uniform(0, 6) + quebra * 6, q.uniform(-0.1, 0.1) + 0.5 * quebra * math.cos(a), q.uniform(-0.1, 0.1) + 0.4 * quebra * math.sin(a) + 0.2 * quebra * quebra), 1 - quebra) for a in q.uniform(0, TAU, 12)]
        G += T.polys(cacos) * 1.2
        H += T.gauss(0, 0, 0.08) * (1 - quebra) ** 2 * 1.8
        G += T.ring(0.08 + 0.35 * ease_out(quebra, 3), 0.03, 0, 0) * (1 - quebra)
    return G * env, H * env


# =================================================================== Tifa
def _estouro_pequeno(T, t, t0, cx, cy, r=0.18):
    u = rel(t, t0, t0 + 0.2)
    if u <= 0 or u >= 1:
        return T.zero(), T.zero()
    e = ease_out(u, 3)
    G = T.ring(0.03 + r * e, 0.02, cx, cy) * (1 - u) * 1.2
    G = G + T.tapered([(cx + 0.03 * math.cos(a), cy + 0.03 * math.sin(a), cx + (0.08 + r * e) * math.cos(a), cy + (0.08 + r * e) * math.sin(a), 1 - u) for a in np.linspace(0, TAU, 8, endpoint=False)], 0.016)
    return G, T.gauss(cx, cy, 0.05) * (1 - u) ** 2 * 1.6


def golpe_de_abertura(T, t, rng):
    """O golpe de abertura: dois jabs rápidos e o gancho de baixo, e a guarda do rival trinca (o escudo que racha
    em linhas) — Exposto."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    golpes = ((0.08, -0.1, 0.0), (0.18, 0.08, 0.0), (0.3, 0.0, -0.9))
    for k, (t0, y, ang) in enumerate(golpes):
        vai = ease_in(rel(t, t0 - 0.08, t0), 2)
        volta = rel(t, t0 + 0.02, t0 + 0.12)
        if vai > 0 and volta < 1:
            x = -0.6 + 0.5 * vai - 0.2 * volta
            yy = y + (0.25 * (1 - vai) if ang else 0)
            P, nos = _punho(T, x, yy, 1.5, ang)
            G += (P * 0.5 + _borda(T, P, 0.006) * 1.3) * (1 - volta)
            H += nos * (1 - volta) * 0.8
        g, h = _estouro_pequeno(T, t, t0, 0.0, y * 0.5)
        G += g
        H += h
    trinca = pulso(t, 0.32, 0.9)
    if trinca > 0:
        q = np.random.default_rng(23)
        G += T.arc_band(0.3, 0.04, -1.2, 1.2, cx=-0.1, cy=0.0, crescente=True) * trinca * 1.2
        for k in range(6):
            a = -1.1 + 0.44 * k
            x0, y0 = 0.05, 0.0
            x1, y1 = -0.1 + 0.34 * math.cos(a), 0.34 * math.sin(a)
            R = T.polyline(jagged(q, x0, y0, x1, y1, 3, 0.35), 0.012)
            G += R * trinca * 1.4
            H += R * trinca * 0.6
        H += T.gauss(0.05, 0.0, 0.05) * trinca * 1.2
    return G * env, H * env


def chuva_de_socos(T, t, rng):
    """A chuva de socos: os punhos vêm em sequência, um atrás do outro em alturas diferentes, com as imagens de rastro
    e um estouro pequeno em cada; no fim ela fica Acelerada."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(31)
    for k in range(8):
        t0 = 0.06 + 0.06 * k
        y = q.uniform(-0.25, 0.25)
        vai = ease_in(rel(t, t0 - 0.06, t0), 2)
        volta = rel(t, t0 + 0.01, t0 + 0.08)
        if vai > 0 and volta < 1:
            x = -0.55 + 0.45 * vai
            P, nos = _punho(T, x, y, 1.3)
            G += (P * 0.4 + _borda(T, P, 0.006) * 1.2) * (1 - volta)
            for j in range(3):
                G += T.tapered([(x - 0.35 - 0.05 * j, y + 0.04 * (j - 1), x - 0.15, y + 0.04 * (j - 1), 1.0)], 0.01) * (1 - volta) * 0.6
        g, h = _estouro_pequeno(T, t, t0, 0.0, y * 0.6, 0.13)
        G += g
        H += h
    rapida = pulso(t, 0.55, 1.0)
    if rapida > 0:
        for k in range(3):
            u = (t * 3 + k / 3) % 1
            G += T.tapered([(-0.6 - 0.2 * u, 0.3 - 0.1 * k, -0.4 - 0.2 * u, 0.3 - 0.1 * k, 1.0)], 0.012) * rapida * (1 - u)
    return G * env, H * env


def tifa_preparo(T, t, rng):
    """O Preparo da Explosão final: os dois punhos de luva fechados com a energia vermelha subindo em volta e o chão
    tremendo em ondas (laço)."""
    G, H = vazio(T)
    for lado in (-1, 1):
        P, nos = _punho(T, 0.3 * lado, 0.0 + 0.02 * math.sin(TAU * t * 4 + lado), 1.6, -math.pi / 2 + 0.25 * lado)
        G += P * 0.5 + _borda(T, P, 0.007) * 1.3
        H += nos * 0.8
    for k in range(10):
        u = (t + k / 10) % 1
        x = 0.4 * math.sin(k * 2.3)
        H += T.gauss(x * (1 - 0.3 * u), 0.45 - 0.8 * u, 0.02) * (1 - u) * 1.2
    for k in range(2):
        u = (t * 2 + k / 2) % 1
        G += T.ring(0.15 + 0.4 * u, 0.012, 0, 0.45, squash=4.0) * (1 - u)
    return G, H


def explosao_final(T, t, rng):
    """A explosão final: o soco no chão, a coluna de energia sobe do ponto do impacto e a onda vermelha e dourada
    explode em volta, jogando os destroços (Paralisado)."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    desce = ease_in(rel(t, 0.0, 0.2), 2)
    if t < 0.3:
        P, nos = _punho(T, 0.0, -0.6 + 0.9 * desce, 2.2, math.pi / 2)
        G += (P * 0.5 + _borda(T, P, 0.007) * 1.4) * (1 - rel(t, 0.22, 0.3))
        H += nos
    coluna = pulso(t, 0.2, 0.75)
    if coluna > 0:
        C = T.lines([(0, 0.4, 0, -1.0, 1.0)], 0.1 * coluna + 0.02)
        G += C * 0.7 + T.blur(C, 0.04) * 0.6
        H += T.lines([(0, 0.4, 0, -1.0, 1.0)], 0.03 * coluna) * 1.4
    onda = rel(t, 0.22, 0.85)
    if 0 < onda < 1:
        e = ease_out(onda, 3)
        G += T.ring(0.1 + 0.9 * e, 0.06 * (1 - onda) + 0.015, 0, 0.3, squash=2.2) * (1 - onda) * 1.4
        H += T.gauss(0, 0.3, 0.2 + 0.3 * e, 0.06 + 0.08 * e) * (1 - onda) ** 2 * 1.8
        q = np.random.default_rng(41)
        pedras = [(_gira([(-0.03, -0.02), (0.03, -0.02), (0.02, 0.025)], q.uniform(0, 6) + onda * 8, 0.8 * e * math.cos(a), 0.3 - 0.5 * e * abs(math.sin(a)) + 0.5 * onda * onda), 1 - onda) for a in q.uniform(-math.pi, 0, 14)]
        G += T.polys(pedras) * 1.1
    return G * env, H * env


# =================================================================== Sephiroth
def _pena(cx, cy, tam, ang):
    dx, dy = math.cos(ang) * tam, math.sin(ang) * tam
    return lamina(cx - dx, cy - dy, cx + dx, cy + dy, tam * 0.35)


def _penas(T, t, t0, n, seed, x0=-0.8, x1=0.8, y0=-0.6):
    u = rel(t, t0, 1.0)
    if u <= 0:
        return T.zero()
    q = np.random.default_rng(seed)
    shapes = []
    for _ in range(n):
        f = (u * q.uniform(0.6, 1.0) + q.uniform(0, 0.3)) % 1
        x = q.uniform(x0, x1) + 0.08 * math.sin(f * 8 + q.uniform(0, 6))
        y = y0 + 1.2 * f
        shapes.append((_pena(x, y, 0.05, 1.2 + 0.6 * math.sin(f * 6)), math.sin(math.pi * f)))
    return T.polys(shapes)


def corte_sombrio(T, t, rng):
    """O corte sombrio: a Masamune risca um corte longuíssimo e escuro que atravessa o rival de ponta a ponta, o
    rastro fica tremendo e as penas negras caem (Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    p = ease_out(rel(t, 0.08, 0.22), 3)
    ini = rel(t, 0.25, 0.55)
    if p > 0 and ini < 1:
        L = T.polys([(lamina(-1.0, -0.35, 1.0, 0.3, 0.035, prog=p, inicio=ini), 1.0)])
        G += L * 1.4 + T.blur(L, 0.03) * 0.6
        H += T.polys([(lamina(-1.0, -0.35, 1.0, 0.3, 0.012, prog=p, inicio=ini), 1.0)]) * 1.3
        for k in range(4):
            dy = 0.05 * (k - 1.5)
            G += T.polys([(lamina(-1.0, -0.35 + dy, 1.0, 0.3 + dy, 0.008, prog=p, inicio=min(1, ini + 0.1 * k)), 1.0)]) * 0.4
    G += _penas(T, t, 0.25, 12, 51) * 0.9
    return G * env, H * env


def _asa(T, cx, cy, s, abre, lado=-1):
    """A asa negra única: as penas longas em leque, presas num ponto."""
    shapes = []
    for k in range(9):
        a = -math.pi / 2 + lado * (0.25 + 1.35 * abre * k / 8)
        L = s * (0.35 + 0.35 * math.sin(math.pi * (k + 1) / 10))
        x1, y1 = cx + L * math.cos(a), cy + L * math.sin(a)
        shapes.append((lamina(cx, cy, x1, y1, s * 0.05), 1.0))
    return T.polys(shapes)


def sephiroth_preparo(T, t, rng):
    """O Preparo do Heartless Angel: a asa negra única se abre devagar sobre o ombro e as penas caem em volta
    (laço)."""
    G, H = vazio(T)
    abre = 0.7 + 0.3 * math.sin(TAU * t)
    A = _asa(T, 0.1, 0.1, 1.4, abre, -1)
    G += A * 0.45 + _borda(T, A, 0.007) * 1.3
    G += _penas(T, (t % 1) * 0.99 + 0.001, 0.0, 10, 61, -0.7, 0.5, -0.5) * 0.8
    H += T.gauss(0.1, 0.1, 0.05) * 0.6
    return G, H


def heartless_angel(T, t, rng):
    """O Heartless Angel: o céu escurece (o véu escuro descendo), a asa enorme se abre no alto, e a luz é drenada de
    todos os rivais em colunas roxas que sobem até ela, deixando todos à beira da queda (Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    asa = ease_out(rel(t, 0.05, 0.35), 2.5)
    b = 1 - rel(t, 0.75, 0.9)
    if asa > 0:
        A = _asa(T, 0.45, -0.1, 1.7, asa, -1)
        G += (A * 0.4 + _borda(T, A, 0.008) * 1.3) * b
    for k, x in enumerate((-0.5, 0.0, 0.5)):
        u = rel(t, 0.3 + 0.05 * k, 0.75 + 0.05 * k)
        if 0 < u < 1:
            sobe = ease_out(min(1, u * 2), 2)
            C = T.lines([(x, 0.45, x, 0.45 - 0.6 * sobe, 1.0)], 0.05 * (1 - u) + 0.015)
            G += C * 0.8 + T.blur(C, 0.03) * 0.5
            H += T.splats([(x + 0.04 * math.sin(t * 20 + j), 0.45 - 0.6 * ((u * 1.5 + j / 6) % 1), 0.8) for j in range(6)], 0.015) * (1 - u)
            G += T.ring(0.15 * (1 - u) + 0.05, 0.015, x, 0.45, squash=2.0) * (1 - u)
    G += _penas(T, t, 0.4, 16, 71) * b
    return G * env, H * env


# =================================================================== Link
def _escudo_hyliano(cx, cy, s):
    meia = [(0.0, -0.22), (0.15, -0.2), (0.17, 0.0), (0.12, 0.15), (0.0, 0.25)]
    return [(cx + x * s, cy + y * s) for x, y in meia] + [(cx - x * s, cy + y * s) for x, y in reversed(meia[1:-1])]


def escudo_hyliano(T, t, rng):
    """O escudo hyliano: o Escudo Hyliano (a forma de gota invertida com a Triforce em cima e a ave vermelha
    no meio) aparece, o golpe bate nele e espirra faíscas, e o Link contra-ataca com o corte."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    surge = ease_out(rel(t, 0.0, 0.2), 3)
    b = 1 - rel(t, 0.65, 0.8)
    if surge > 0:
        E = T.polys([(_escudo_hyliano(-0.55, 0.05, 1.6 * surge), 1.0)])
        G += (E * 0.35 + _borda(T, E, 0.008) * 1.4) * b
        G += _triforce(T, -0.55, -0.15 * surge, 0.6 * surge) * b * 0.9
        ave = [(-0.55, 0.08), (-0.45, 0.02), (-0.5, 0.12), (-0.55, 0.2), (-0.6, 0.12), (-0.65, 0.02)]
        G += T.lines(_contorno(ave), 0.008) * b * surge
    bate = pulso(t, 0.25, 0.5)
    if bate > 0:
        q = np.random.default_rng(81)
        pts = [(-0.3 + 0.25 * bate * math.cos(a), 0.0 + 0.25 * bate * math.sin(a), 1.0) for a in q.uniform(-1.2, 1.2, 14)]
        S = T.splats(pts, 0.014)
        G += S * 1.3 + T.tapered([(-0.3, 0.0, -0.3 + 0.3 * bate * math.cos(a), 0.3 * bate * math.sin(a), 1 - bate) for a in q.uniform(-1.0, 1.0, 6)], 0.01)
        H += S * 1.5 + T.flare(-0.3, 0.0, 0.4 * bate, 0.3, 0.012) * bate
    p = ease_out(rel(t, 0.45, 0.58), 3)
    ini = rel(t, 0.6, 0.8)
    if p > 0 and ini < 1:
        L = T.polys([(lamina(-0.25, 0.4, 0.55, -0.4, 0.045, prog=p, inicio=ini), 1.0)])
        G += L * 1.4
        H += L * 0.5
    return G * env, H * env


def _espada(cx, cy, s, ang):
    return _gira([(0.0, -0.02 * s), (0.4 * s, -0.015 * s), (0.45 * s, 0.0), (0.4 * s, 0.015 * s), (0.0, 0.02 * s)], ang, cx, cy)


def link_preparo(T, t, rng):
    """O Preparo do Golpe giratório: a espada erguida carregando, as faíscas subindo pela lâmina e o brilho na
    ponta crescendo (laço)."""
    G, H = vazio(T)
    S = T.polys([(_espada(0.0, 0.45, 2.1, -math.pi / 2 - 0.2), 1.0)])
    G += S * 0.6 + _borda(T, S, 0.006) * 1.3
    G += T.lines([(-0.1, 0.45, 0.1, 0.47, 1.0)], 0.025)
    carga = (t * 2) % 1
    tip = (0.95 * math.cos(-math.pi / 2 - 0.2), 0.45 + 0.95 * math.sin(-math.pi / 2 - 0.2))
    G += T.ring(0.25 - 0.2 * carga, 0.012, tip[0], tip[1]) * carga
    H += T.gauss(tip[0], tip[1], 0.03 + 0.05 * carga) * 1.6
    for k in range(6):
        u = (t * 3 + k / 6) % 1
        x = 0.0 + (tip[0] - 0.0) * u + 0.04 * math.sin(k * 3)
        y = 0.45 + (tip[1] - 0.45) * u
        H += T.gauss(x, y, 0.012) * (1 - u) * 1.3
    return G, H


def golpe_giratorio(T, t, rng):
    """O golpe giratório: o Link gira 360° com a espada (o rastro azul em volta dele inteiro), acertando todo mundo
    ao redor, e o estouro de energia no fim (Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    gira = ease_out(rel(t, 0.05, 0.4), 2)
    some = 1 - rel(t, 0.45, 0.65)
    if gira > 0 and some > 0:
        a1 = -math.pi / 2 + TAU * gira
        A = T.arc_band(0.55, 0.07, a1 - min(TAU * 0.95, TAU * gira), a1, squash=0.5, cx=0, cy=0.15, taper=0.5)
        G += (A * 1.3 + T.blur(A, 0.03) * 0.5) * some
        H += A * 0.6 * some
        S = T.polys([(_espada(0.0, 0.15, 1.3, a1), 1.0)])
        G += S * some
    bum = rel(t, 0.4, 0.8)
    if 0 < bum < 1:
        e = ease_out(bum, 3)
        G += T.ring(0.2 + 0.7 * e, 0.04, 0, 0.15, squash=2.0) * (1 - bum) * 1.3
        H += T.gauss(0, 0.15, 0.15 + 0.2 * e, 0.08) * (1 - bum) ** 2 * 1.5
    return G * env, H * env


# =================================================================== Zelda
def selo_da_luz(T, t, rng):
    """O selo da luz: o círculo de luz com a Triforce aparece debaixo do rival, as faixas de luz sobem e o prendem,
    e o clarão o deixa Cego (Preso e Cego)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2.5)
    b = 1 - rel(t, 0.8, 0.95)
    if abre > 0:
        G += (T.ring(0.5 * abre, 0.015, 0, 0.35, squash=3.0) + T.ring(0.4 * abre, 0.01, 0, 0.35, squash=3.0)) * b * 1.2
        tri = _triforce(T, 0, 0.35, 1.4 * abre)
        G += np.clip(tri, 0, 1) * 0.5 * b
    sobe = pulso(t, 0.25, 0.85)
    if sobe > 0:
        for k in range(6):
            a = TAU * k / 6 + t * 2
            x = 0.4 * math.cos(a)
            G += T.lines([(x, 0.35 + 0.1 * math.sin(a), x * 0.4, -0.2, 1.0)], 0.01) * sobe
    flash = pulso(t, 0.35, 0.6)
    H += T.gauss(0, -0.05, 0.12) * flash * 2.0 + T.flare(0, -0.05, 0.6 * flash, 0.785, 0.012) * flash
    return G * env, H * env


def _diamante(cx, cy, r, ang):
    return _gira([(0, -r), (r * 0.7, 0), (0, r), (-r * 0.7, 0)], ang, cx, cy)


def barreira_sagrada(T, t, rng):
    """A barreira sagrada: o cristal de diamante do Amor de Nayru se forma em volta de cada aliado, girando e
    brilhando nas facetas, e os Status ruins saem (Escudo, Protegido e Purificar)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for k, (x, y) in enumerate(((-0.55, 0.25), (0.0, 0.3), (0.55, 0.25))):
        forma = ease_out(rel(t, 0.05 + 0.05 * k, 0.35 + 0.05 * k), 3)
        if forma > 0:
            b = 1 - rel(t, 0.85, 0.98)
            D = _diamante(x, y, 0.28 * forma, 0.15 * math.sin(t * 6))
            G += T.lines(_contorno(D), 0.016) * b * 1.2
            G += T.lines([(D[0][0], D[0][1], D[2][0], D[2][1], 0.5), (D[1][0], D[1][1], D[3][0], D[3][1], 0.5)], 0.006) * b
            G += T.polys([(D, 1.0)]) * 0.15 * b
            fx = x + 0.12 * math.cos(t * 9 + k)
            H += T.flare(fx, y - 0.1, 0.25 * forma, 0.785, 0.01) * b * 0.8
    sai = pulso(t, 0.5, 0.95)
    if sai > 0:
        for x in (-0.55, 0.0, 0.55):
            u = rel(t, 0.5, 0.95)
            G += T.splats([(x + 0.1 * math.cos(j * 2.1), 0.25 - 0.3 * u - 0.05 * j, 0.6) for j in range(4)], 0.014) * sai
    return G * env, H * env


def _arco(T, cx, cy, s, puxa):
    arco = [(cx + 0.09 * s * math.cos(a), cy + 0.3 * s * math.sin(a)) for a in np.linspace(-math.pi / 2, math.pi / 2, 20)]
    G = T.polyline(arco, 0.014 * s)
    corda_x = cx - 0.12 * s * puxa
    G = G + T.lines([(arco[0][0], arco[0][1], corda_x, cy, 0.7), (arco[-1][0], arco[-1][1], corda_x, cy, 0.7)], 0.006 * s)
    return G, corda_x


def zelda_preparo(T, t, rng):
    """O Preparo da Flecha de Luz: o arco de luz se forma, a corda é puxada e a flecha brilhante acende, com o brilho
    na ponta crescendo (laço)."""
    G, H = vazio(T)
    puxa = 0.5 + 0.5 * math.sin(TAU * t)
    A, cx = _arco(T, 0.0, 0.0, 1.6, puxa)
    G += A * 1.1
    G += T.lines([(cx, 0.0, 0.45, 0.0, 1.0)], 0.014) * 1.4 + T.lines([(0.45, 0.0, 0.38, -0.04, 1.0), (0.45, 0.0, 0.38, 0.04, 1.0)], 0.012) * 1.3
    H += T.gauss(0.45, 0.0, 0.03 + 0.03 * puxa) * 1.8 + T.flare(0.45, 0.0, 0.3 * puxa + 0.05, 0, 0.012) * 0.8
    return G, H


def flecha_de_luz(T, t, rng):
    """A flecha de luz: a flecha brilhante sai do arco, cruza o campo deixando o rastro de luz, acerta o rival
    com o clarão em cruz, e o selo de silêncio (o círculo cortado) fica nele."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    arco = pulso(t, 0.0, 0.3)
    if arco > 0:
        A, _ = _arco(T, -0.8, 0.0, 1.2, 1 - rel(t, 0.1, 0.18))
        G += A * arco
    voa = rel(t, 0.12, 0.3)
    if 0 < voa < 1:
        x = -0.75 + 0.75 * ease_in(voa, 1.3)
        G += T.tapered([(x - 0.5, 0.0, x, 0.0, 1.0)], 0.04) * 1.6 + T.gauss(x, 0.0, 0.05) * 0.8
        H += T.lines([(x - 0.1, 0.0, x, 0.0, 1.0)], 0.01) * 1.5 + T.gauss(x, 0.0, 0.04) * 1.5
    g = pulso(t, 0.28, 0.55)
    H += T.flare(0, 0, 0.7 * g, 0, 0.012) * g * 1.4 + T.gauss(0, 0, 0.1) * g * 1.4
    G += (T.flare(0, 0, 0.6 * g, 0, 0.014) + T.flare(0, 0, 0.35 * g, math.pi / 2, 0.014)) * g * 1.2
    b = rel(t, 0.28, 0.6)
    if 0 < b < 1:
        G += T.ring(0.05 + 0.3 * ease_out(b, 3), 0.025, 0, 0) * (1 - b) * 1.2
    selo = pulso(t, 0.45, 1.0)
    if selo > 0:
        G += T.ring(0.13, 0.015, 0, -0.35) * selo + T.lines([(-0.09, -0.26, 0.09, -0.44, 1.0)], 0.015) * selo
    return G * env, H * env


REGISTRO = [
    ("raio_magico", raio_magico, GRANDE, "Shazam · o raio dourado e o símbolo", False),
    ("forca_de_hercules", forca_de_hercules, GRANDE, "Shazam · o punho dourado e o escudo de força", False),
    ("shazam_preparo", shazam_preparo, MEDIA, "Shazam · as letras S-H-A-Z-A-M (Preparo, laço)", True),
    ("sabedoria_de_salomao", sabedoria_de_salomao, GRANDE, "Shazam · o pergaminho e o Preparo quebrando", False),
    ("golpe_de_abertura", golpe_de_abertura, GRANDE, "Tifa · os jabs, o gancho e a guarda trincando", False),
    ("chuva_de_socos", chuva_de_socos, GRANDE, "Tifa · a sequência de socos com rastro", False),
    ("tifa_preparo", tifa_preparo, MEDIA, "Tifa · os punhos e a energia subindo (Preparo, laço)", True),
    ("explosao_final", explosao_final, GRANDE, "Tifa · o soco no chão, a coluna e a onda", False),
    ("corte_sombrio", corte_sombrio, GRANDE, "Sephiroth · o corte longuíssimo e as penas", False),
    ("sephiroth_preparo", sephiroth_preparo, MEDIA, "Sephiroth · a asa negra única (Preparo, laço)", True),
    ("heartless_angel", heartless_angel, GRANDE, "Sephiroth · a asa enorme e a luz drenada", False),
    ("escudo_hyliano", escudo_hyliano, GRANDE, "Link · o Escudo Hyliano, as faíscas e o corte", False),
    ("link_preparo", link_preparo, MEDIA, "Link · a espada carregando (Preparo, laço)", True),
    ("golpe_giratorio", golpe_giratorio, GRANDE, "Link · o giro de 360° e o estouro", False),
    ("selo_da_luz", selo_da_luz, GRANDE, "Zelda · o círculo com a Triforce e o clarão", False),
    ("barreira_sagrada", barreira_sagrada, GRANDE, "Zelda · os cristais de diamante no trio", False),
    ("zelda_preparo", zelda_preparo, MEDIA, "Zelda · o arco de luz e a flecha (Preparo, laço)", True),
    ("flecha_de_luz", flecha_de_luz, GRANDE, "Zelda · a flecha de luz e o selo de silêncio", False),
]
