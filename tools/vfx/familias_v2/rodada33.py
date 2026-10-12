"""Rodada 33 das habilidades próprias: Sr. Incrível, Mulher-Elástica, Gelado, Korra, Zuko e Azula.

Sr. Incrível
- forca_bruta: as duas mãos enormes apertando o rival como uma prensa, o metal amassando (Preso).
- segurar_o_impacto: o símbolo dos Incríveis enorme na frente do trio e o impacto batendo e voltando (Escudo, Protegido e Provocado).
- incrivel_preparo: o Preparo do Golpe do Incrível — os punhos fechados e o símbolo pulsando (laço).
- golpe_do_incrivel: o punho gigante descendo do alto e a onda com o símbolo (Preso).

Mulher-Elástica
- alcance_elastico: o braço comprido se esticando em curva até o aliado e virando escudo (Escudo).
- escudo_flexivel: o corpo esticado como um paraquedas de borracha, balançando por cima do aliado (Protegido).
- elastica_preparo: o Preparo do Resgate — os braços enrolando como mola (laço).
- resgate_elastico: o braço que estica, agarra o aliado e puxa de volta, com o coração e o escudo (Vida, Escudo e Acelerado).

Gelado
- rampa_de_gelo: a rampa de gelo se desenhando no ar, o deslize e o impacto (Lento).
- parede_congelada: a parede de gelo subindo do chão em frente aos rivais, com as pontas (Lento e Espinhos).
- frozone_preparo: o Preparo do "Cadê meu supertraje?" — as mãos geladas e os cristais girando (laço).
- cade_meu_supertraje: a nevasca varrendo e os rivais virando blocos de gelo (Lento e Congelado).

Korra
- dobra_de_fogo: os chutes de fogo em arco varrendo todos os rivais (Queimando).
- dobra_de_terra: as colunas de pedra saindo do chão embaixo do rival e a rocha lançada (Acelerado e Fortalecido).

Zuko
- chicote_de_fogo: o chicote de fogo longo estalando no rival.
- redirecionar_relampago: o raio entrando por uma mão, o caminho pelo corpo e saindo pela outra (Interrompe, Eletrificado, Queimando e Refletir).
- zuko_preparo: o Preparo dos Dois espadachins — as duas espadas dao cruzadas (laço).
- dois_espadachins: o X das duas espadas e as faíscas (Paralisado).

Azula
- relampago_de_azula: o relâmpago azul-branco saindo dos dedos (Eletrificado e Paralisado).
- azula_preparo: o Preparo da Precisão cruel — os dedos girando a chama azul e os estalos (laço).
- precisao_cruel: a linha fina de fogo azul que acerta num ponto só e explode (Silenciado).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, CORACAO, ESPADA, anel, aura, cheio, clarao, corte, estouro, icone, onda_no_chao, particulas, poe, raios,
                         surge)


def _logo_incrivel(T, cx, cy, s, k):
    """O símbolo dos Incríveis: o círculo com o "i" dentro."""
    if k <= 0:
        return 0.0, 0.0
    G = T.ring(s, s * 0.14, cx, cy) * k * 1.3
    G = G + T.ring(s * 0.75, s * 0.05, cx, cy) * k * 0.8
    g, h = cheio(T, [(cx - s * 0.12, cy - s * 0.25), (cx + s * 0.12, cy - s * 0.25), (cx + s * 0.12, cy + s * 0.55), (cx - s * 0.12, cy + s * 0.55)], k * 1.3)
    G = G + g + T.gauss(cx, cy - s * 0.48, s * 0.12) * k * 1.6
    return G, h


def _raio(T, t, x0, y0, x1, y1, k, w=0.016, seed=0, desvio=0.1):
    q = np.random.default_rng(int(t * 30) + seed)
    bolt = jagged(q, x0, y0, x1, y1, 6, desvio)
    return T.polyline(bolt, w) * k * 1.4, T.polyline(bolt, w * 0.35) * k * 1.6


def _cristal(cx, cy, s, ang):
    pts = [(0, -1), (0.3, 0), (0, 1), (-0.3, 0)]
    c, sn = math.cos(ang), math.sin(ang)
    return [(cx + s * (x * c - y * sn), cy + s * (x * sn + y * c)) for x, y in pts]


def _pedra(cx, cy, r, giro):
    q = np.random.default_rng(17)
    rr = [q.uniform(0.75, 1.0) for _ in range(8)]
    return [(cx + math.cos(giro + TAU * j / 8) * r * rr[j], cy + math.sin(giro + TAU * j / 8) * r * rr[j] * 0.85) for j in range(8)]


# ------------------------------------------------------------------ Sr. Incrível

def forca_bruta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    fecha = ease_in(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.7, 0.85)
    if k > 0:
        for lado in (-1, 1):
            x = 0.35 + lado * (0.6 - 0.42 * fecha)
            P, nos = _punho(T, x, 0.0, 2.6, math.pi if lado > 0 else 0)
            G += P * 0.95 * k
            H += nos * 0.4 * k
    g, h = clarao(T, t, 0.33, 0.55, 0.35, 0.0, 1.1, 1.3)
    G, H = G + g, H + h
    amassa = pulso(t, 0.35, 0.9)
    if amassa > 0:
        q = np.random.default_rng(3)
        for j in range(6):
            y = -0.2 + 0.08 * j
            pts = [(0.35 + (m - 3) * 0.04, y + q.normal(0, 0.015)) for m in range(7)]
            G += T.polyline(pts, 0.008) * amassa * 1.0
    G += estouro(T, t, 0.35, 0.8, 12, 4, 0.35, 0.0, 0.4, 0.013)
    return G * env, H * env


def segurar_o_impacto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.8, 0.95))
    g, h = _logo_incrivel(T, 0.2, -0.1, 0.25 * s, 1.0 if s > 0 else 0)
    G, H = G + g, H + h
    for j in range(3):
        u = rel(t, 0.3 + 0.1 * j, 0.55 + 0.1 * j)
        if 0 < u < 1:
            x = 0.9 - 0.45 * ease_in(u, 2)
            G += T.tapered([(x + 0.25, -0.1 + 0.15 * (j - 1), x, -0.1 + 0.1 * (j - 1), 1.0)], 0.05) * 1.2
        g2, h2 = clarao(T, t, 0.53 + 0.1 * j, 0.68 + 0.1 * j, 0.45, -0.1 + 0.1 * (j - 1), 0.5)
        G, H = G + g2, H + h2
    for x in (-0.55, 0.0, 0.55):
        k = pulso(t, 0.35, 1.0)
        G += T.arc_band(0.22, 0.03, -1.2, 1.2, 1.0, 0, x, 0.1, 0.0) * k * 1.1
    G += anel(T, t, 0.3, 0.8, 0.1, 0.6, 0.03, -0.1)
    return G * env, H * env


def incrivel_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    for lado in (-1, 1):
        P, nos = _punho(T, lado * 0.3, 0.15, 1.8 * (1 + 0.06 * b), -math.pi / 2)
        G += P * 0.9
        H += nos * 0.35
    g, h = _logo_incrivel(T, 0, -0.25, 0.16 * (1 + 0.1 * b), 1.0 + 0.3 * b)
    G += T.gauss(0, -0.25, 0.3) * (0.3 + 0.2 * b)
    return G + g, H + h


def golpe_do_incrivel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    desce = ease_in(rel(t, 0.0, 0.32), 2.4)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        P, nos = _punho(T, 0.3, -0.85 + 0.95 * desce, 3.6, math.pi / 2)
        G += P * 0.95 * k
        H += nos * 0.5 * k
        G += T.tapered([(0.3, -1.0, 0.3, -0.95 + 0.85 * desce, 1.0)], 0.1) * k * 0.5
    g, h = clarao(T, t, 0.3, 0.52, 0.3, 0.2, 1.4, 1.5)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.3, 0.9, 1.0, 0.35, 1.8)
    s = surge(t, 0.35, 0.55) * (1 - rel(t, 0.8, 0.95))
    g2, h2 = _logo_incrivel(T, 0.3, -0.25, 0.2 * s, 1.0 if s > 0 else 0)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.32, 0.85, 16, 5, 0.3, 0.2, 0.6, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Mulher-Elástica

def _braco(T, pts, w, k):
    return T.polyline(pts, w) * k * 1.2 + T.polyline(pts, w * 0.3) * k * 0.6


def alcance_elastico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.35), 2)
    volta = rel(t, 0.65, 0.85)
    if u > 0 and volta < 1:
        alcance = u * (1 - volta)
        n = 30
        pts = [(-0.7 + 1.3 * alcance * m / n, 0.05 - 0.35 * math.sin(math.pi * m / n) * alcance + 0.03 * math.sin(m * 0.9 + t * 20)) for m in range(n + 1)]
        G += _braco(T, pts, 0.035, 1.0)
        x, y = pts[-1]
        G += T.gauss(x, y, 0.05) * 1.2
    s = surge(t, 0.35, 0.55) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.arc_band(0.3 * s, 0.04, -1.3, 1.3, 1.0, 0, 0.6, 0.05, 0.0) * 1.3
        G += T.gauss(0.6, 0.05, 0.25 * s) * 0.4
    g, h = clarao(T, t, 0.33, 0.5, 0.6, 0.05, 0.6)
    return (G + g) * env, (H + h) * env


def escudo_flexivel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.85, 1))
    if s > 0:
        balanca = 0.06 * math.sin(t * 14) * (1 - rel(t, 0.3, 0.9))
        pts = [(0.5 * s * math.cos(a), -0.15 - (0.3 + balanca) * s * math.sin(a)) for a in np.linspace(0, math.pi, 30)]
        pts += [(-0.5 * s + 1.0 * s * m / 8, -0.15 + 0.04 * math.sin(m * math.pi)) for m in range(9)][::-1]
        g, h = icone(T, pts, 1.1, 0.4)
        G, H = G + g, H + h
        for lado in (-1, 1):
            G += T.lines([(lado * 0.5 * s, -0.15, lado * 0.15, 0.3, 1.0)], 0.012) * 0.9
    for j in range(4):
        u = rel(t, 0.35 + 0.1 * j, 0.55 + 0.1 * j)
        if 0 < u < 1:
            x = -0.3 + 0.2 * j
            G += T.gauss(x, -0.9 + 0.5 * u, 0.025) * 1.2
            g2, h2 = clarao(T, t, 0.53 + 0.1 * j, 0.63 + 0.1 * j, x, -0.45, 0.35)
            G, H = G + g2, H + h2
    g3, h3 = aura(T, t, 0.3, 1.0, 0.3, 0.05, 0.7)
    return (G + g3) * env, (H + h3) * env


def elastica_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        pts = []
        for m in range(40):
            v = m / 39
            a = v * TAU * 3 + t * TAU * 2 * lado
            pts.append((lado * (0.1 + 0.45 * v), -0.05 + 0.16 * math.sin(a)))
        G += _braco(T, pts, 0.035, 1.1)
    G += T.gauss(0, 0, 0.2) * (0.4 + 0.2 * math.sin(t * 8))
    return G, H


def resgate_elastico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    vai = ease_out(rel(t, 0.0, 0.3), 2)
    volta = ease_in(rel(t, 0.35, 0.6), 2)
    alcance = vai * (1 - volta)
    if alcance > 0.02:
        n = 30
        pts = [(-0.6 + 1.2 * alcance * m / n, 0.0 - 0.25 * math.sin(math.pi * m / n) * alcance) for m in range(n + 1)]
        G += _braco(T, pts, 0.035, 1.0)
        x, y = pts[-1]
        G += T.gauss(x, y, 0.07) * 1.1
    if volta > 0:
        x = 0.6 - 1.0 * volta
        G += T.gauss(x, 0.0, 0.1) * (1 - rel(t, 0.6, 0.75)) * 0.9
    s = surge(t, 0.58, 0.78) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g, h = icone(T, poe(CORACAO, -0.4, -0.35, 0.11 * s), 1.3, 0.5)
        G, H = G + g, H + h
        G += T.ring(0.28 * s, 0.03, -0.4, 0.0) * 1.2
    g2, h2 = aura(T, t, 0.55, 1.0, 0.35, 0.0, 0.8)
    G += particulas(T, t, 0.6, 1.0, 14, 4, -0.4, 0.1, 0.25, 0.5, 0.012)
    return (G + g2) * env, (H + h2) * env


# ------------------------------------------------------------------ Gelado

def rampa_de_gelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_out(rel(t, 0.0, 0.4), 1.6)
    k = 1 - rel(t, 0.75, 0.92)
    if u > 0 and k > 0:
        n = 24
        pts = [(-0.8 + 1.35 * u * m / n, 0.1 - 0.45 * math.sin(math.pi * u * m / n * 0.9)) for m in range(n + 1)]
        G += T.polyline(pts, 0.04) * k * 1.0
        G += T.polyline([(x, y + 0.035) for x, y in pts], 0.01) * k * 1.3
        H += T.polyline(pts, 0.008) * k * 0.8
        q = np.random.default_rng(5)
        for m in range(0, n + 1, 3):
            x, y = pts[m]
            g, h = cheio(T, _cristal(x, y + 0.06, 0.035, q.uniform(-0.4, 0.4)), k * 1.1)
            G, H = G + g, H + h
        x, y = pts[-1]
        G += T.gauss(x, y - 0.04, 0.06) * k * 1.0
    g2, h2 = clarao(T, t, 0.38, 0.58, 0.55, 0.0, 0.9)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.4, 0.85, 12, 3, 0.55, 0.0, 0.4, 0.012)
    return G * env, H * env


def parede_congelada(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = ease_out(rel(t, 0.05, 0.4), 2.5)
    k = 1 - rel(t, 0.8, 0.95)
    if sobe > 0 and k > 0:
        q = np.random.default_rng(8)
        for j in range(11):
            x = -0.85 + 0.17 * j
            alto = q.uniform(0.35, 0.65) * sobe
            pts = [(x - 0.08, 0.35), (x - 0.05, 0.35 - alto * 0.8), (x, 0.35 - alto), (x + 0.05, 0.35 - alto * 0.85), (x + 0.08, 0.35)]
            g, h = icone(T, pts, k * 1.1, 0.5)
            G, H = G + g, H + h
            H += T.gauss(x, 0.35 - alto, 0.015) * k * 1.4
    G += onda_no_chao(T, t, 0.05, 0.6, 1.0, 0.35, 1.4)
    for x in (-0.55, 0.0, 0.55):
        g2, h2 = clarao(T, t, 0.35, 0.55, x, 0.0, 0.45)
        G, H = G + g2, H + h2
    G += particulas(T, t, 0.3, 1.0, 20, 6, 0, 0.0, 0.8, 0.5, 0.011)
    return G * env, H * env


def frozone_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(8):
        a = TAU * j / 8 + t * TAU
        r = 0.36
        g, h = icone(T, _cristal(r * math.cos(a), r * 0.6 * math.sin(a), 0.1, a), 1.2, 0.6)
        G, H = G + g, H + h
    for lado in (-1, 1):
        G += T.gauss(lado * 0.12, 0.0, 0.07) * (0.9 + 0.3 * math.sin(t * 10 + lado))
        H += T.gauss(lado * 0.12, 0.0, 0.025) * 1.3
    G += T.gauss(0, 0, 0.35) * 0.3
    return G, H


def cade_meu_supertraje(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(11)
    k = pulso(t, 0.0, 0.7)
    for j in range(40):
        y0 = q.uniform(-0.6, 0.4)
        v = q.uniform(1.4, 2.4)
        x = ((q.uniform(0, 1) + t * v) % 1.6) - 0.8
        G += T.lines([(x - 0.08, y0 - 0.02, x, y0, 1.0)], 0.006) * k * 1.2
    G += T.gauss(0, 0.0, 0.9, 0.5) * k * 0.4
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        s = surge(t, 0.45 + 0.05 * j, 0.65 + 0.05 * j) * (1 - rel(t, 0.88, 1))
        if s > 0:
            bloco = [(x - 0.17 * s, -0.25), (x + 0.15 * s, -0.28), (x + 0.18 * s, 0.32), (x - 0.15 * s, 0.33)]
            g, h = icone(T, bloco, 1.1, 0.4)
            G, H = G + g, H + h
            G += T.lines([(x - 0.08 * s, -0.15, x + 0.02 * s, 0.0, 1.0), (x + 0.06 * s, 0.05, x + 0.1 * s, 0.2, 1.0)], 0.008) * 1.2
        g2, h2 = clarao(T, t, 0.5 + 0.05 * j, 0.66 + 0.05 * j, x, 0.0, 0.5)
        G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Korra

def dobra_de_fogo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(3):
        u = rel(t, 0.05 + 0.13 * j, 0.45 + 0.13 * j)
        if 0 < u < 1:
            a1 = -2.6 + 2.2 * ease_out(u, 1.5)
            G += T.arc_band(0.6, 0.11, a1 - 1.4, a1, 1.0, 0, -0.1, 0.25 - 0.05 * j, 1.0) * (1 - rel(u, 0.7, 1)) * 1.3
            H += T.arc_band(0.6, 0.03, a1 - 0.8, a1, 1.0, 0, -0.1, 0.25 - 0.05 * j, 1.0) * (1 - rel(u, 0.7, 1)) * 1.2
    for j, x in enumerate((-0.5, 0.05, 0.6)):
        g, h = clarao(T, t, 0.35 + 0.1 * j, 0.5 + 0.1 * j, x, 0.0, 0.5)
        G, H = G + g, H + h
        for m in range(3):
            kk = pulso(t, 0.4 + 0.1 * j, 1.0)
            g2, h2 = icone(T, poe(CHAMA, x - 0.08 + 0.08 * m, 0.08, 0.07 * kk), kk, 0.6)
            G, H = G + g2, H + h2
    return G * env, H * env


def dobra_de_terra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j, (x, a0) in enumerate(((0.35, 0.05), (0.5, 0.12), (0.65, 0.19))):
        sobe = ease_out(rel(t, a0, a0 + 0.2), 3)
        k = 1 - rel(t, 0.75, 0.9)
        if sobe > 0 and k > 0:
            alto = (0.35 + 0.1 * (j % 2)) * sobe
            g, h = icone(T, [(x - 0.07, 0.35), (x - 0.06, 0.35 - alto), (x + 0.06, 0.35 - alto - 0.03), (x + 0.07, 0.35)], k * 1.1, 0.5)
            G, H = G + g, H + h
    u = rel(t, 0.3, 0.6)
    if 0 < u < 1:
        x = -0.7 + 1.2 * ease_in(u, 1.5)
        g2, h2 = icone(T, _pedra(x, -0.05 - 0.15 * math.sin(math.pi * u), 0.12, u * 6), 1.2, 0.5)
        G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.55, 0.72, 0.5, -0.05, 0.9)
    G, H = G + g3, H + h3
    G += onda_no_chao(T, t, 0.05, 0.6, 0.6, 0.35, 1.3)
    G += estouro(T, t, 0.55, 0.95, 14, 6, 0.5, -0.05, 0.45, 0.016)
    return G * env, H * env


# ------------------------------------------------------------------ Zuko

def chicote_de_fogo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.45)
    if 0 < u < 1:
        n = 32
        cab = ease_out(u, 1.5)
        pts = []
        for m in range(n + 1):
            v = cab * m / n
            onda = 0.25 * math.sin(math.pi * v) * math.sin(v * 7 - u * 10) * (1 - u)
            pts.append((-0.75 + 1.35 * v, -0.15 * math.sin(math.pi * v) + onda))
        G += T.polyline(pts, 0.06) * (1 - rel(u, 0.8, 1)) * 1.3
        H += T.polyline(pts, 0.016) * (1 - rel(u, 0.8, 1)) * 1.2
        x, y = pts[-1]
        g, h = icone(T, poe(CHAMA, x, y, 0.14, math.pi / 2), 1.3, 0.6)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.38, 0.6, 0.6, 0.0, 1.0)
    G, H = G + g2, H + h2
    G += estouro(T, t, 0.4, 0.85, 12, 4, 0.6, 0.0, 0.4, 0.012)
    return G * env, H * env


def redirecionar_relampago(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k1 = pulso(t, 0.0, 0.3)
    if k1 > 0:
        g, h = _raio(T, t, -0.95, -0.6, -0.2, -0.15, k1, 0.016, 1)
        G, H = G + g, H + h
    u = rel(t, 0.2, 0.5)
    if 0 < u < 1:
        pts = [(-0.2 + 0.4 * v, -0.15 + 0.25 * math.sin(math.pi * v)) for v in np.linspace(0, u, 16)]
        G += T.polyline(pts, 0.02) * 1.3
        H += T.polyline(pts, 0.006) * 1.4
    G += T.gauss(-0.2, -0.15, 0.04) * pulso(t, 0.1, 0.4) * 1.4
    k2 = pulso(t, 0.45, 0.75)
    if k2 > 0:
        g2, h2 = _raio(T, t, 0.2, -0.15, 0.65, 0.0, k2, 0.02, 2)
        G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.5, 0.72, 0.65, 0.0, 1.0)
    G, H = G + g3, H + h3
    G += raios(T, t, 0.5, 0.85, 5, 3, 0.65, 0.0, 0.3, 0.009)
    return G * env, H * env


def zuko_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    for lado in (-1, 1):
        g, h = icone(T, poe(ESPADA, lado * 0.08, -0.05, 0.42, lado * 0.5), 1.1, 0.5)
        G, H = G + g, H + h
    H += T.gauss(0, -0.12, 0.03) * (1.3 + 0.7 * b)
    G += T.gauss(0, -0.12, 0.2) * (0.3 + 0.2 * b)
    return G, H


def dois_espadachins(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = corte(T, t, 0.05, 0.35, 0.75, 1.3, 0.08, 0.35, 0.0)
    G, H = G + g * 1.3, H + h
    g2, h2 = corte(T, t, 0.12, 0.42, -0.75, 1.3, 0.08, 0.35, 0.0)
    G, H = G + g2 * 1.3, H + h2
    g3, h3 = clarao(T, t, 0.3, 0.5, 0.35, 0.0, 1.2, 1.3)
    G, H = G + g3, H + h3
    q = np.random.default_rng(6)
    for j in range(14):
        a = q.uniform(0, TAU)
        w = rel(t, 0.32, 0.8)
        if 0 < w < 1:
            r = q.uniform(0.2, 0.55) * ease_out(w)
            x, y = 0.35 + r * math.cos(a), r * math.sin(a) + 0.2 * w * w
            G += T.lines([(x, y, x - 0.03 * math.cos(a), y - 0.03 * math.sin(a), 1.0)], 0.007) * (1 - w) * 1.5
    G += raios(T, t, 0.4, 0.6, 3, 5, 0.35, 0.0, 0.25, 0.008)
    return G * env, H * env


# ------------------------------------------------------------------ Azula

def relampago_de_azula(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    G += T.gauss(-0.6, 0.0, 0.05 + 0.05 * rel(t, 0.0, 0.2)) * pulso(t, 0.0, 0.3) * 1.5
    k = pulso(t, 0.15, 0.7)
    if k > 0:
        for j in range(2):
            g, h = _raio(T, t, -0.6, 0.0, 0.6, 0.0, k, 0.022 if j == 0 else 0.01, j * 7, 0.15)
            G, H = G + g, H + h
        G += T.gauss(0, 0, 0.6, 0.12) * k * 0.4
    g2, h2 = clarao(T, t, 0.2, 0.55, 0.6, 0.0, 1.2, 1.4)
    G, H = G + g2, H + h2
    G += raios(T, t, 0.2, 0.8, 6, 9, 0.6, 0.0, 0.35, 0.01)
    return G * env, H * env


def azula_preparo(T, t, rng):
    G, H = vazio(T)
    a = t * TAU * 2
    for j in range(2):
        x, y = 0.1 * math.cos(a + math.pi * j), -0.1 + 0.1 * math.sin(a + math.pi * j)
        g, h = icone(T, poe(CHAMA, x, y, 0.09), 1.3, 0.6)
        G, H = G + g, H + h * 1.5
    G += T.ring(0.12, 0.012, 0, -0.1) * 1.0
    g2, h2 = _raio(T, t, -0.25, -0.1, 0.25, -0.1, 0.5 + 0.5 * math.sin(t * 30), 0.008, 3, 0.1)
    G += T.gauss(0, -0.1, 0.25) * (0.35 + 0.15 * math.sin(t * 10))
    return G + g2 * 0.7, H + h2 * 0.7


def precisao_cruel(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.25), 2)
    if 0 < u < 1 or pulso(t, 0.2, 0.45) > 0:
        xe = -0.8 + 1.35 * min(1, u)
        k = 1 - rel(t, 0.35, 0.5)
        G += T.tapered([(-0.8, -0.05, xe, 0.0, 1.0)], 0.025) * k * 1.4
        H += T.lines([(-0.8, -0.05, xe, 0.0, 1.0)], 0.006) * k * 1.6
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.3, 0.4))
    if s > 0:
        G += T.ring(0.12 * (2 - s), 0.01, 0.55, 0.0) * 1.3
    g, h = clarao(T, t, 0.25, 0.5, 0.55, 0.0, 1.5, 1.5)
    G, H = G + g, H + h
    for j in range(8):
        a = TAU * j / 8
        w = rel(t, 0.28, 0.85)
        if 0 < w < 1:
            r = 0.05 + 0.4 * ease_out(w, 2)
            g2, h2 = icone(T, poe(CHAMA, 0.55 + r * math.cos(a), r * math.sin(a), 0.07 * (1 - w) + 0.01, a + math.pi / 2), 1.2, 0.6)
            G, H = G + g2, H + h2
    u2 = rel(t, 0.3, 0.75)
    if 0 < u2 < 1:
        G += T.ring(0.05 + 0.5 * ease_out(u2, 2), 0.03 * (1 - 0.5 * u2), 0.55, 0.0) * (1 - u2) * 1.3
    return G * env, H * env


REGISTRO = [
    ("forca_bruta", forca_bruta, GRANDE, "Sr. Incrível · as mãos apertando como prensa", False),
    ("segurar_o_impacto", segurar_o_impacto, GRANDE, "Sr. Incrível · o símbolo na frente do trio", False),
    ("incrivel_preparo", incrivel_preparo, MEDIA, "Sr. Incrível · os punhos e o símbolo (Preparo, laço)", True),
    ("golpe_do_incrivel", golpe_do_incrivel, GRANDE, "Sr. Incrível · o punho gigante e o símbolo", False),
    ("alcance_elastico", alcance_elastico, GRANDE, "Mulher-Elástica · o braço esticando até o aliado", False),
    ("escudo_flexivel", escudo_flexivel, GRANDE, "Mulher-Elástica · o paraquedas de borracha", False),
    ("elastica_preparo", elastica_preparo, MEDIA, "Mulher-Elástica · os braços como mola (Preparo, laço)", True),
    ("resgate_elastico", resgate_elastico, GRANDE, "Mulher-Elástica · o braço que agarra e puxa", False),
    ("rampa_de_gelo", rampa_de_gelo, GRANDE, "Gelado · a rampa de gelo no ar", False),
    ("parede_congelada", parede_congelada, GRANDE, "Gelado · a parede de gelo subindo", False),
    ("frozone_preparo", frozone_preparo, MEDIA, "Gelado · as mãos geladas e os cristais (Preparo, laço)", True),
    ("cade_meu_supertraje", cade_meu_supertraje, GRANDE, "Gelado · a nevasca e os blocos de gelo", False),
    ("dobra_de_fogo", dobra_de_fogo, GRANDE, "Korra · os chutes de fogo em arco", False),
    ("dobra_de_terra", dobra_de_terra, GRANDE, "Korra · as colunas de pedra e a rocha", False),
    ("chicote_de_fogo", chicote_de_fogo, GRANDE, "Zuko · o chicote de fogo", False),
    ("redirecionar_relampago", redirecionar_relampago, GRANDE, "Zuko · o raio entrando e saindo pelas mãos", False),
    ("zuko_preparo", zuko_preparo, MEDIA, "Zuko · as duas espadas cruzadas (Preparo, laço)", True),
    ("dois_espadachins", dois_espadachins, GRANDE, "Zuko · o X das duas espadas", False),
    ("relampago_de_azula", relampago_de_azula, GRANDE, "Azula · o relâmpago azul dos dedos", False),
    ("azula_preparo", azula_preparo, MEDIA, "Azula · a chama azul girando nos dedos (Preparo, laço)", True),
    ("precisao_cruel", precisao_cruel, GRANDE, "Azula · a linha de fogo azul num ponto só", False),
]
