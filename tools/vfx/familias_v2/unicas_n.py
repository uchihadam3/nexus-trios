"""Rodada 13 das Mecânicas únicas ativando como habilidade: Ghostface, Leatherface, Pinhead, Samara, Valak, Drácula,
Xenomorfo, Predador, Darth Vader, Yoda, Luke, Palpatine, Neo, Agente Smith, John Wick, T-800, RoboCop, Indiana Jones,
Jack Sparrow, Harry Potter, Voldemort e Gandalf.

- outro_ghostface: as duas máscaras aparecem e as facas cortam juntas.
- corte_fundo: a motosserra ronca de lado, solta a fumaça e corta.
- caixa: a caixa do lamento gira, abre e solta as correntes com ganchos.
- sete_dias: a TV com chiado mostra o anel e os cabelos saem da tela.
- atras: a silhueta de freira surge atrás com os olhos acesos e a cruz invertida.
- nevoa: a névoa vermelha sobe e os morcegos se espalham.
- cria: o ovo abre em quatro pétalas e a mandíbula de dentro ataca.
- trofeu: os três pontos vermelhos da mira e a camuflagem que tremula.
- estrangulamento: a mão fecha no ar e o rival é erguido pelo pescoço.
- equilibrio: o sabre verde gira e as duas metades da Força se equilibram.
- nova_esperanca: os dois sóis no horizonte e o sabre verde erguido.
- relampago_cadeia: o relâmpago da Força sai das mãos e pula de rival em rival.
- desviou: as balas desaceleram com as ondas e o código verde cai.
- mais_smith: os óculos escuros e as cópias que se multiplicam.
- recarregou: o pente entra, os tiros e as cápsulas voando.
- exterminador: o olho vermelho, o quadro de mira e o crânio de metal.
- corpo_metal: o visor varre e as placas de metal brilham.
- desarmado: o chicote estala, enrola e arranca, e o chapéu.
- parlay: a bússola gira e as moedas do tesouro saltam.
- golpe_voltou: a cúpula dourada segura o raio verde e devolve.
- horcrux: o medalhão racha e a fumaça escura escapa.
- o_branco: o cajado erguido e a luz branca enorme.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .rodada13 import _borda
from .unicas_b import _silhueta
from .unicas_kit import (CRUZ, DIAMANTE, ESPADA, GEMA, GOTA, MOEDA, RAIO, SETA, anel, aura, cheio, chuva, circulo, clarao,
                         converge, corte, estouro, estrela_pts, icone, onda_no_chao, orbita, particulas, poe, raios, surge, voa)


def _mascara_ghost(cx, cy, s):
    face = [(cx + 0.18 * s * math.cos(a), cy + 0.3 * s * math.sin(a) * (1.15 if math.sin(a) > 0 else 1)) for a in np.linspace(0, TAU, 28, endpoint=False)]
    return face


def outro_ghostface(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j, (cx, a0) in enumerate(((-0.3, 0.0), (0.3, 0.15))):
        s = surge(t, a0, a0 + 0.25) * (1 - rel(t, 0.8, 0.95))
        if s > 0:
            g, h = icone(T, _mascara_ghost(cx, -0.15, s), 1.2, 0.45)
            G, H = G + g, H + h
            for lado in (-1, 1):
                olho = [(cx + lado * 0.07 * s + 0.04 * s * math.cos(a), -0.2 * s - 0.05 + 0.06 * s * math.sin(a) + lado * 0.0) for a in np.linspace(0, TAU, 12, endpoint=False)]
                G += T.polyline(olho + [olho[0]], 0.012) * 1.1
            boca = [(cx + 0.04 * s * math.cos(a), -0.15 + 0.08 * s + 0.09 * s * math.sin(a)) for a in np.linspace(0, TAU, 12, endpoint=False)]
            G += T.polyline(boca + [boca[0]], 0.012) * 1.1
    for j, ang in enumerate((1.0, -1.0)):
        g, h = corte(T, t, 0.4 + 0.05 * j, 0.7 + 0.05 * j, ang, 1.2, 0.08, 0, 0.1)
        G, H = G + g, H + h
    return G * env, H * env


def corte_fundo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.7, 0.85)
    vib = 0.01 * math.sin(t * 150)
    if k > 0:
        x0 = -0.9 + 0.5 * u
        corpo = [(x0 - 0.25, -0.18 + vib), (x0 + 0.05, -0.18 + vib), (x0 + 0.05, 0.18 + vib), (x0 - 0.25, 0.18 + vib)]
        g, h = icone(T, corpo, k * 1.1, 0.45)
        G, H = G + g, H + h
        x1 = x0 + 0.75
        G += T.polys([([(x0 + 0.05, -0.09 + vib), (x1, -0.09 + vib), (x1 + 0.09, 0.0 + vib), (x1, 0.09 + vib), (x0 + 0.05, 0.09 + vib)], 1.0)]) * k * 0.8
        dentes = []
        for m in range(14):
            v = (m / 14 + t * 8) % 1
            px = x0 + 0.05 + (x1 - x0 - 0.05) * v
            dentes += [(px, -0.09 + vib, px + 0.03, -0.14 + vib, 1.0), (px, 0.09 + vib, px + 0.03, 0.14 + vib, 1.0)]
        G += T.lines(dentes, 0.016) * k * 1.3
        for j in range(3):
            fumo = (t * 2 + j / 3) % 1
            G += T.gauss(x0 - 0.2 - 0.1 * fumo, -0.15 - 0.3 * fumo, 0.05 + 0.08 * fumo) * (1 - fumo) * k * 0.6
    q = np.random.default_rng(5)
    v = rel(t, 0.35, 0.9)
    if 0 < v < 1:
        for j in range(8):
            a = q.uniform(-1.2, 1.2) - math.pi / 2
            d = 0.5 * ease_out(v)
            g2, h2 = cheio(T, poe(GOTA, 0.25 + d * math.cos(a) * 0.6, d * math.sin(a) + 0.4 * v * v, 0.04, a + math.pi / 2), 1 - v)
            G, H = G + g2, H + h2
    return G * env, H * env


def caixa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    gira = t * 6
    abre = ease_out(rel(t, 0.3, 0.55), 2)
    k = 1 - rel(t, 0.85, 1)
    s = surge(t, 0.0, 0.25)
    if s > 0:
        lado = 0.18 * s
        for j in range(2 if abre > 0 else 1):
            off = 0.06 * abre * (1 if j else -1)
            quad = poe([(-1, -1), (1, -1), (1, 1), (-1, 1)], off, -0.05 + off, lado, gira * (0.3 if j else 0.3) + j * math.pi / 4)
            g, h = icone(T, quad, k * 1.1, 0.4)
            G, H = G + g, H + h
            G += T.polyline(_padrao(off, -0.05 + off, lado * 0.7, gira * 0.3 + j * math.pi / 4), 0.008) * k
    if abre > 0:
        for j in range(6):
            a = TAU * j / 6 + 0.3
            d = 0.75 * ease_out(rel(t, 0.4, 0.7), 2)
            x, y = d * math.cos(a), -0.05 + d * math.sin(a)
            for m in range(8):
                v = m / 8
                G += T.ring(0.015, 0.006, x * v, -0.05 + (y + 0.05) * v, 1.5 if m % 2 else 0.6) * k
            G += T.polyline([(x, y), (x + 0.05 * math.cos(a + 1.5), y + 0.05 * math.sin(a + 1.5)), (x + 0.02 * math.cos(a + 2.5), y + 0.02 * math.sin(a + 2.5))], 0.015) * k * 1.3
    return G * env, H * env


def _padrao(cx, cy, s, ang):
    return poe([(-1, 0), (0, -1), (1, 0), (0, 1), (-1, 0)], cx, cy, s, ang)


def sete_dias(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.85, 1))
    if s > 0:
        w, h0 = 0.4 * s, 0.3 * s
        tela = [(-w, -h0 - 0.1), (w, -h0 - 0.1), (w, h0 - 0.1), (-w, h0 - 0.1)]
        g, h = icone(T, tela, 1.1, 0.25)
        G, H = G + g, H + h
        q = np.random.default_rng(int(t * 30))
        segs = [(-w * 0.9, -0.1 + q.uniform(-h0, h0) * 0.9, -w * 0.9 + q.uniform(0.1, 0.5) * w * 2, -0.1 + q.uniform(-h0, h0) * 0.9, q.uniform(0.3, 1)) for _ in range(20)]
        G += T.lines(segs, 0.006) * (1 - rel(t, 0.35, 0.5)) * 1.2
        anel_ = rel(t, 0.35, 0.6)
        G += T.ring(0.15 * s, 0.03, 0, -0.1) * anel_ * 1.4
        H += T.ring(0.15 * s, 0.01, 0, -0.1) * anel_
    cabelo = rel(t, 0.55, 0.95)
    if 0 < cabelo < 1:
        for j in range(8):
            x0 = -0.25 + 0.07 * j
            pts = [(x0 + 0.04 * math.sin(v * 6 + j), 0.2 + 0.5 * v * ease_out(cabelo)) for v in np.linspace(0, 1, 10)]
            G += T.polyline(pts, 0.012) * (1 - rel(t, 0.88, 1)) * 1.1
    return G * env, H * env


def atras(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    surge_ = ease_out(rel(t, 0.05, 0.4), 2) * (1 - rel(t, 0.85, 1))
    if surge_ > 0:
        capuz = [(0, -0.6), (0.18, -0.45), (0.25, 0.0), (0.35, 0.45), (-0.35, 0.45), (-0.25, 0.0), (-0.18, -0.45)]
        P = T.polys([([(x * surge_, y) for x, y in capuz], 1.0)])
        G += (P * 0.25 + _borda(T, P, 0.008) * 1.2) * surge_
        rosto = [(0.09 * math.cos(a), -0.35 + 0.12 * math.sin(a)) for a in np.linspace(0, TAU, 16, endpoint=False)]
        G += T.polyline(rosto + [rosto[0]], 0.012) * surge_
    olhos = pulso(t, 0.3, 1.0)
    for lado in (-1, 1):
        H += T.gauss(lado * 0.04, -0.38, 0.015) * olhos * 2.5
        G += T.gauss(lado * 0.04, -0.38, 0.04) * olhos * 1.3
    cruz = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if cruz > 0:
        g, h = cheio(T, poe(CRUZ, 0, 0.15, 0.1 * cruz, math.pi), 1.2)
        G += T.lines([(0, 0.0, 0, 0.3, 1.0), (-0.06, 0.22, 0.06, 0.22, 1.0)], 0.025) * cruz * 1.3
    return G * env, H * env


def _morcego(cx, cy, s, bate):
    return poe([(-1, -0.3 * bate), (-0.7, -0.1), (-0.5, -0.35 * bate), (-0.3, -0.05), (0, -0.2), (0.3, -0.05), (0.5, -0.35 * bate), (0.7, -0.1), (1, -0.3 * bate),
                (0.6, 0.2), (0.3, 0.1), (0, 0.25), (-0.3, 0.1), (-0.6, 0.2)], cx, cy, s)


def nevoa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(3)
    sobe = rel(t, 0.0, 0.9)
    pts = [(q.normal(0, 0.25), 0.3 - 0.4 * sobe * q.uniform(0.5, 1) + q.normal(0, 0.08), (1 - rel(sobe, 0.7, 1)) * q.uniform(0.3, 1)) for _ in range(40)]
    G += T.splats(pts, 0.07) * 0.6
    for j in range(7):
        a = q.uniform(0, TAU)
        u = rel(t, 0.2 + 0.03 * j, 0.85)
        if 0 < u < 1:
            d = 0.75 * ease_out(u)
            g, h = cheio(T, _morcego(d * math.cos(a), -0.1 + d * math.sin(a) * 0.7, 0.15, math.sin(t * 40 + j)), (1 - rel(u, 0.85, 1)) * 1.3)
            G, H = G + g, H + h
    return G * env, H * env


def cria(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25)
    abre = ease_out(rel(t, 0.3, 0.55), 2)
    k = 1 - rel(t, 0.85, 1)
    if s > 0:
        for j in range(4):
            a = -math.pi / 2 + (j - 1.5) * 0.4 * (1 + 1.6 * abre)
            petala = poe([(0, 0), (0.08, -0.12), (0, -0.28), (-0.08, -0.12)], 0, 0.15, s * 1.1, a + math.pi / 2)
            g, h = icone(T, petala, k * 1.1, 0.4)
            G, H = G + g, H + h
        ovo = [(0.15 * s * math.cos(a), 0.25 + 0.12 * s * math.sin(a)) for a in np.linspace(0, math.pi, 12)]
        g, h = icone(T, ovo + [(-0.15 * s, 0.25)], k, 0.4)
        G, H = G + g, H + h
    ataque = ease_out(rel(t, 0.55, 0.7), 3) * (1 - rel(t, 0.8, 0.9))
    if ataque > 0:
        y = 0.15 - 0.6 * ataque
        G += T.lines([(0, 0.15, 0, y, 1.0)], 0.04) * 1.2
        for lado in (-1, 1):
            G += T.lines([(0, y, lado * 0.06, y - 0.06, 1.0)], 0.02) * 1.3
        H += T.gauss(0, y, 0.03) * 1.5
    return G * env, H * env


def trofeu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = pulso(t, 0.0, 0.95)
    for j in range(5):
        x = -0.4 + 0.2 * j
        pts = [(x + 0.03 * math.sin(v * 12 + t * 25 + j), -0.5 + 1.0 * v) for v in np.linspace(0, 1, 20)]
        G += T.polyline(pts, 0.008) * k * 0.6
    fecha = ease_out(rel(t, 0.2, 0.55), 2)
    r = 0.4 - 0.25 * fecha
    for j in range(3):
        a = -math.pi / 2 + TAU * j / 3 + t * 2
        x, y = r * 0.3 * math.cos(a) * 1.5, -0.05 + r * 0.3 * math.sin(a) * 1.5
        H += T.gauss(x, y, 0.02) * k * 2.5
        G += T.gauss(x, y, 0.05) * k * 1.2
        G += T.lines([(x, y, x + 0.9 * math.cos(a), y + 0.9 * math.sin(a), 1.0)], 0.006) * k * 0.6 * (1 - fecha)
    g, h = clarao(T, t, 0.6, 0.8, 0, -0.05, 0.6)
    return (G + g) * env, (H + h) * env


def estrangulamento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    fecha = ease_in(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.5, 0.6)
    if k > 0:
        for j in range(4):
            y = -0.1 + 0.07 * j
            G += T.polyline([(-0.75, y), (-0.6 + 0.1 * fecha, y - 0.02), (-0.55 + 0.05 * fecha, y + 0.04 * fecha)], 0.025) * k * 1.1
        G += T.polyline([(-0.75, 0.15), (-0.65, 0.12 - 0.05 * fecha)], 0.03) * k
    sobe = ease_out(rel(t, 0.3, 0.7), 2)
    kk = 1 - rel(t, 0.85, 1)
    if t > 0.25:
        y = -0.25 * sobe
        G += T.ring(0.14, 0.035, 0.3, -0.25 + y, 2.2) * kk * 1.4 * (0.8 + 0.2 * math.sin(t * 40))
        H += T.ring(0.09, 0.008, 0.3, -0.25 + y, 2.2) * kk
        G += T.gauss(0.3, -0.25 + y, 0.15) * kk * 0.4
    g, h = aura(T, t, 0.3, 1.0, 0.3, -0.3, 0.6)
    return (G + g) * env, (H + h) * env


def equilibrio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    a = t * 15
    G += T.lines([(-0.35 * math.cos(a), -0.35 * math.sin(a), 0.35 * math.cos(a), 0.35 * math.sin(a), 1.0)], 0.05) * pulso(t, 0.0, 0.5) * 1.1
    H += T.lines([(-0.35 * math.cos(a), -0.35 * math.sin(a), 0.35 * math.cos(a), 0.35 * math.sin(a), 1.0)], 0.015) * pulso(t, 0.0, 0.5)
    s = ease_out(rel(t, 0.35, 0.65), 2) * k
    if s > 0:
        r = 0.35 * s
        G += T.ring(r, 0.025, 0, 0) * 1.3
        metade = [(0, -r)] + [(r * 0.5 * math.cos(b), -r * 0.5 + r * 0.5 * math.sin(b)) for b in np.linspace(-math.pi / 2, math.pi / 2, 10)] + \
                 [(-r * 0.5 * math.cos(b), r * 0.5 + r * 0.5 * math.sin(b)) for b in np.linspace(-math.pi / 2, math.pi / 2, 10)] + \
                 [(r * math.cos(b), r * math.sin(b)) for b in np.linspace(math.pi / 2, 3 * math.pi / 2, 16)]
        g, h = cheio(T, poe(metade, 0, 0, 1.0, t * 3), 0.9)
        G, H = G + g, H + h
    return G * env, H * env


def nova_esperanca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.4), 2) * (1 - rel(t, 0.85, 1))
    for j, (x, r) in enumerate(((-0.25, 0.12), (0.1, 0.08))):
        y = 0.35 - 0.2 * s
        G += T.gauss(x, y, r * s + 0.001) * 1.3
        H += T.gauss(x, y, r * 0.5 * s + 0.001) * 1.5
    G += T.lines([(-0.9, 0.38, 0.9, 0.38, 1.0)], 0.01) * s
    sabre = ease_out(rel(t, 0.4, 0.7), 2) * (1 - rel(t, 0.85, 1))
    if sabre > 0:
        G += T.lines([(0.4, 0.2, 0.4, 0.2 - 0.75 * sabre, 1.0)], 0.06) * 1.2
        H += T.lines([(0.4, 0.2, 0.4, 0.2 - 0.75 * sabre, 1.0)], 0.02) * 1.4
    return G * env, H * env


def relampago_cadeia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(int(t * 35) % 6 + 1)
    pontos = [(-0.6, 0.0), (0.1, -0.35), (0.5, 0.05), (0.15, 0.4)]
    for j in range(3):
        k = pulso(t, 0.1 + 0.15 * j, 0.6 + 0.12 * j)
        if k > 0:
            (x1, y1), (x2, y2) = pontos[j], pontos[j + 1]
            for _ in range(2):
                bolt = jagged(q, x1, y1, x2, y2, 5, 0.3)
                G += T.polyline(bolt, 0.02) * k * 1.4
                H += T.polyline(bolt, 0.006) * k
            G += T.gauss(x2, y2, 0.1) * k
    G += T.gauss(-0.6, 0, 0.08) * pulso(t, 0.0, 0.8) * 1.3
    return G * env, H * env


def desviou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(7)
    k = pulso(t, 0.0, 0.95)
    segs = []
    for j in range(16):
        x = -0.8 + 0.1 * j + q.uniform(-0.03, 0.03)
        y0 = ((t * (0.8 + q.uniform(0, 0.6)) + q.uniform(0, 1)) % 1) * 2 - 1
        segs.append((x, y0 - 0.15, x, y0, 1.0))
    G += T.lines(segs, 0.006) * k * 0.7
    for j in range(3):
        u = rel(t, 0.1 + 0.08 * j, 0.95)
        if 0 < u < 1:
            y = -0.3 + 0.3 * j
            x = 0.9 - 1.6 * (1 - (1 - u) ** 3) * 0.6
            g, h = cheio(T, poe([(1, 0), (0.5, -0.4), (-1, -0.4), (-1, 0.4), (0.5, 0.4)], -x, y, 0.06), 1.2)
            G, H = G + g, H + h
            for r in range(3):
                G += T.ring(0.05 + 0.04 * r, 0.006, -x + 0.15 + 0.12 * r, y, 0.4) * (1 - r / 3) * 0.8
    return G * env, H * env


def mais_smith(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.4, 0.5))
    if s > 0:
        for lado in (-1, 1):
            lente = [(lado * 0.12 * s + 0.1 * s * math.cos(a), -0.3 + 0.055 * s * math.sin(a)) for a in np.linspace(0, TAU, 16, endpoint=False)]
            g, h = cheio(T, lente, 1.2)
            G, H = G + g, H + h
        G += T.lines([(-0.03 * s, -0.3, 0.03 * s, -0.3, 1.0)], 0.015) * s
    for j in range(4):
        u = ease_out(rel(t, 0.35 + 0.08 * j, 0.6 + 0.08 * j), 2)
        if u > 0:
            x = (-0.55 + 0.37 * j) * u
            S = T.polys([(_silhueta(x, 0.08, 0.9), 1.0)])
            G += (S * 0.3 + _borda(T, S, 0.007) * 1.1) * (1 - rel(t, 0.85, 1))
    return G * env, H * env


def recarregou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    entra = ease_in(rel(t, 0.0, 0.25), 2)
    k = 1 - rel(t, 0.35, 0.45)
    if k > 0:
        y = 0.5 - 0.4 * entra
        g, h = icone(T, [(-0.09, y - 0.28), (0.09, y - 0.28), (0.12, y + 0.28), (-0.06, y + 0.28)], k * 1.2, 0.5)
        G, H = G + g, H + h
    for j in range(3):
        a0 = 0.35 + 0.12 * j
        g2, h2 = clarao(T, t, a0, a0 + 0.12, 0.35, -0.05 + 0.1 * (j - 1), 0.7, 1.3)
        G, H = G + g2, H + h2
        u = rel(t, a0, a0 + 0.4)
        if 0 < u < 1:
            x, y = 0.1 - 0.25 * u, -0.1 - 0.3 * math.sin(math.pi * u) + 0.3 * u * u
            g3, h3 = cheio(T, poe([(-1, -0.4), (1, -0.4), (1, 0.4), (-1, 0.4)], x, y, 0.06, u * 12), 1.3)
            G, H = G + g3, H + h3
    return G * env, H * env


def exterminador(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        cranio = [(0.2 * s * math.cos(a), -0.2 + 0.25 * s * math.sin(a)) for a in np.linspace(math.pi * 0.9, math.pi * 2.1, 16)] + [(0.12 * s, 0.1), (-0.12 * s, 0.1)]
        G += T.polyline(cranio + [cranio[0]], 0.016) * 1.1
        G += T.lines([(-0.1 * s, 0.05, 0.1 * s, 0.05, 1.0)] + [(-0.1 * s + 0.04 * s * m, 0.02, -0.1 * s + 0.04 * s * m, 0.08, 1.0) for m in range(6)], 0.008) * 0.9
        H += T.gauss(0.08 * s, -0.22, 0.035) * 2.5
        G += T.gauss(0.08 * s, -0.22, 0.08) * 1.3
    caixa = ease_out(rel(t, 0.3, 0.55), 3) * (1 - rel(t, 0.85, 1))
    if caixa > 0:
        w = 0.6 - 0.25 * caixa
        segs = []
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            segs += [(sx * w, sy * w - 0.1, sx * w - sx * 0.12, sy * w - 0.1, 1.0), (sx * w, sy * w - 0.1, sx * w, sy * w - sy * 0.12 - 0.1, 1.0)]
        G += T.lines(segs, 0.015) * 1.3
    return G * env, H * env


def corpo_metal(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        visor = [(-0.42 * s, -0.45), (0.42 * s, -0.45), (0.36 * s, -0.32), (-0.36 * s, -0.32)]
        g, h = icone(T, visor, 1.2, 0.5)
        G, H = G + g, H + h
        scan = -0.36 * s + 0.72 * s * ((t * 2.5) % 1)
        H += T.gauss(scan, -0.39, 0.03, 0.04) * 2.2
    for j in range(4):
        brilho = pulso(t, 0.3 + 0.1 * j, 0.55 + 0.1 * j)
        if brilho > 0:
            x, y = (-0.25, 0.25, -0.2, 0.2)[j], (-0.05, -0.05, 0.3, 0.3)[j]
            placa = [(x - 0.2, y - 0.15), (x + 0.2, y - 0.15), (x + 0.17, y + 0.15), (x - 0.17, y + 0.15)]
            g, h = icone(T, placa, 0.8, 0.3)
            G, H = G + g, H + h
            G += T.lines([(x - 0.1, y + 0.05, x + 0.05, y - 0.08, 1.0)], 0.02) * brilho * 1.4
    return G * env, H * env


def desarmado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.6, 0.75)
    if u > 0 and k > 0:
        pts = [(-0.7 + 1.2 * v * u, -0.1 + 0.15 * math.sin(v * 7 - t * 25) * v) for v in np.linspace(0, 1, 30)]
        G += T.polyline(pts, 0.028) * k * 1.4
        if u >= 1:
            G += T.ring(0.06, 0.015, 0.5, -0.1, 1.2) * k
    g, h = clarao(T, t, 0.28, 0.42, 0.5, -0.1, 0.6)
    G, H = G + g, H + h
    arranca = ease_out(rel(t, 0.4, 0.8), 2)
    if 0 < arranca < 1:
        g2, h2 = cheio(T, poe(ESPADA, 0.5 - 0.6 * arranca, -0.1 - 0.4 * math.sin(math.pi * arranca), 0.15, arranca * 8), 1.2)
        G, H = G + g2, H + h2
    s = surge(t, 0.5, 0.75) * (1 - rel(t, 0.88, 1))
    if s > 0:
        aba = [(-0.3 * s, -0.5), (0.3 * s, -0.5), (0.2 * s, -0.46), (-0.2 * s, -0.46)]
        copa = [(-0.15 * s, -0.5), (-0.13 * s, -0.66), (0, -0.62), (0.13 * s, -0.66), (0.15 * s, -0.5)]
        for p in (aba, copa):
            g3, h3 = icone(T, p, 1.1, 0.45)
            G, H = G + g3, H + h3
    return G * env, H * env


def parlay(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.85, 1))
    if s > 0:
        r = 0.42 * s
        G += T.ring(r, 0.04, 0, -0.1) * 1.3
        for j in range(4):
            a = TAU * j / 4
            G += T.lines([(r * 0.75 * math.cos(a), -0.1 + r * 0.75 * math.sin(a), r * 0.9 * math.cos(a), -0.1 + r * 0.9 * math.sin(a), 1.0)], 0.015)
        gira = t * 20 * (1 - rel(t, 0.3, 0.6)) + 1.0
        agulha = poe([(0, -1), (0.15, 0), (0, 0.3), (-0.15, 0)], 0, -0.1, r * 0.75, gira)
        g, h = cheio(T, agulha, 1.3)
        G, H = G + g, H + h
    for j in range(6):
        u = rel(t, 0.45 + 0.04 * j, 0.95)
        if 0 < u < 1:
            a = -math.pi / 2 + (j - 2.5) * 0.35
            x, y = 0.5 * u * math.cos(a), 0.3 + 0.5 * u * math.sin(a) + 0.6 * u * u
            G += T.ring(0.06, 0.018, x, y, 1 / max(0.2, abs(math.cos(t * 15 + j)))) * (1 - u) * 1.4
    return G * env, H * env


def golpe_voltou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.25), 2.5) * (1 - rel(t, 0.85, 1))
    if s > 0:
        G += T.arc_band(0.4 * s, 0.035, math.pi, TAU, 1.0, 0.0, 0, 0.3, 0.0) * 1.3 + T.gauss(0, 0.1, 0.3 * s, 0.25 * s) * 0.3
        g, h = cheio(T, poe(RAIO, 0, -0.1, 0.1 * s, 0.25), 1.2)
        G, H = G + g, H + h
    vai = rel(t, 0.2, 0.45)
    volta = rel(t, 0.45, 0.75)
    if 0 < vai < 1:
        x = 0.9 - 0.5 * vai
        G += T.tapered([(x + 0.4, -0.05, x, -0.05, 1.0)], 0.06) * 1.2
    g, h = clarao(T, t, 0.42, 0.55, 0.4, -0.05, 0.7)
    G, H = G + g, H + h
    if 0 < volta < 1:
        x = 0.4 + 0.6 * volta
        G += T.tapered([(x - 0.4, -0.05, x, -0.05, 1.0)], 0.07) * 1.3
        H += T.gauss(x, -0.05, 0.03) * 1.5
    return G * env, H * env


def horcrux(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.25)
    racha = rel(t, 0.3, 0.6)
    q = np.random.default_rng(11)
    if s > 0 and racha < 1:
        medalhao = [(0.24 * s * math.cos(a), -0.05 + 0.32 * s * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)]
        if racha <= 0:
            g, h = icone(T, medalhao, 1.2, 0.45)
            G, H = G + g, H + h
            G += T.polyline([(-0.06, -0.12), (0.0, -0.02), (0.06, -0.12)], 0.015)
        else:
            for j in range(6):
                a = TAU * j / 6
                d = 0.4 * racha
                caco = poe([(-1, -0.6), (1, -0.8), (0.3, 1)], d * math.cos(a), -0.05 + d * math.sin(a), 0.07, a + racha * 5)
                g, h = icone(T, caco, 1 - racha, 0.5)
                G, H = G + g, H + h
    fumo = rel(t, 0.3, 1.0)
    if 0 < fumo < 1:
        for j in range(4):
            pts = [(0.15 * math.sin(v * 5 + j * 1.5 + t * 3) * v, -0.05 - 0.7 * v * fumo, (1 - v) * (1 - fumo)) for v in np.linspace(0, 1, 12)]
            G += T.splats(pts, 0.06) * 0.8
    g, h = clarao(T, t, 0.3, 0.45, 0, -0.05, 0.7)
    return (G + g) * env, (H + h) * env


def o_branco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = ease_out(rel(t, 0.0, 0.3), 2)
    k = 1 - rel(t, 0.85, 1)
    G += T.lines([(0.15, 0.4, 0.15, 0.4 - 0.9 * sobe, 1.0)], 0.03) * k * 1.1
    topo = (0.15, 0.4 - 0.9 * sobe)
    G += T.gauss(topo[0], topo[1], 0.06) * k * 1.3
    H += T.gauss(topo[0], topo[1], 0.03) * k * 1.6
    luz = pulso(t, 0.3, 0.95)
    if luz > 0:
        G += T.gauss(topo[0], topo[1], 0.5) * luz * 0.8
        H += T.gauss(topo[0], topo[1], 0.2) * luz * 1.0
        segs = [(topo[0], topo[1], topo[0] + 1.0 * math.cos(TAU * j / 16 + t), topo[1] + 1.0 * math.sin(TAU * j / 16 + t), 1.0) for j in range(16)]
        G += T.tapered([(x2, y2, x1, y1, w) for x1, y1, x2, y2, w in segs], 0.06) * luz * 0.6
    g, h = clarao(T, t, 0.3, 0.5, topo[0], topo[1], 1.2, 1.5)
    return (G + g) * env, (H + h) * env


REGISTRO = [
    ("mu_outro_ghostface", outro_ghostface, GRANDE, "Ghostface · as duas máscaras e as facas", False),
    ("mu_corte_fundo", corte_fundo, GRANDE, "Leatherface · a motosserra roncando", False),
    ("mu_caixa", caixa, GRANDE, "Pinhead · a caixa e as correntes de gancho", False),
    ("mu_sete_dias", sete_dias, GRANDE, "Samara · a TV, o anel e os cabelos", False),
    ("mu_atras", atras, GRANDE, "Valak · a silhueta atrás de você", False),
    ("mu_nevoa", nevoa, GRANDE, "Drácula · a névoa e os morcegos", False),
    ("mu_cria", cria, GRANDE, "Xenomorfo · o ovo abrindo e a mandíbula", False),
    ("mu_trofeu", trofeu, GRANDE, "Predador · a mira de três pontos e a camuflagem", False),
    ("mu_estrangulamento", estrangulamento, GRANDE, "Darth Vader · o estrangulamento da Força", False),
    ("mu_equilibrio", equilibrio, GRANDE, "Yoda · o sabre e o equilíbrio da Força", False),
    ("mu_nova_esperanca", nova_esperanca, GRANDE, "Luke · os dois sóis e o sabre", False),
    ("mu_relampago_cadeia", relampago_cadeia, GRANDE, "Palpatine · o relâmpago em cadeia", False),
    ("mu_desviou", desviou, GRANDE, "Neo · as balas lentas e o código", False),
    ("mu_mais_smith", mais_smith, GRANDE, "Agente Smith · os óculos e as cópias", False),
    ("mu_recarregou", recarregou, GRANDE, "John Wick · a recarga e os tiros", False),
    ("mu_exterminador", exterminador, GRANDE, "T-800 · o olho vermelho e a mira", False),
    ("mu_corpo_metal", corpo_metal, GRANDE, "RoboCop · o visor e as placas", False),
    ("mu_desarmado", desarmado, GRANDE, "Indiana Jones · o chicote e o chapéu", False),
    ("mu_parlay", parlay, GRANDE, "Jack Sparrow · a bússola e as moedas", False),
    ("mu_golpe_voltou", golpe_voltou, GRANDE, "Harry Potter · a proteção que devolve", False),
    ("mu_horcrux", horcrux, GRANDE, "Voldemort · a Horcrux destruída", False),
    ("mu_o_branco", o_branco, GRANDE, "Gandalf · o cajado e a luz branca", False),
]
