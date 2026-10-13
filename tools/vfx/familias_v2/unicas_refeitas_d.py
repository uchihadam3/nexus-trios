"""Mecânicas únicas refeitas, lote d: o impacto conta o nome da mecânica.

- mu_strix (Loid): o dossiê da Operação Strix abrindo e as três barras de Carga subindo;
- mu_faca (Leon): a faca girando e o corte em X;
- mu_terreno (Lara): a armadilha de laço fechando no chão e prendendo;
- mu_inibidores (Shadow): os anéis inibidores voando dos pulsos e a aura do Chaos explodindo;
- mu_cogumelo (Mario): o Super Cogumelo pulando e o "crescer" em degraus;
- mu_banana (Donkey Kong): a casca de banana girando e caindo no chão, o escorregão;
- mu_kuririn_nao (Kuririn): a explosão vermelha e as auras de raiva subindo nos aliados;
- mu_evoluiu (Garou): as escamas de monstro cobrindo e a seta de evolução;
- mu_improviso (Michelangelo): os nunchakus girando e os números sorteados pulando;
- mu_scooby_lanche (Scooby): o biscoito em forma de osso mordido e os farelos;
- mu_desastrado (Pateta): o tombo — estrelas de tontura e o "bonk";
- mu_infinito (Buzz): o voo com o rastro em arco e o "ao infinito";
- mu_achatado (Tom): o Tom achatado que estoura de volta para a forma, com molas;
- mu_goool (Casey Jones): o taco de hóquei rodando e a pancada com o disco.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, pulso, rel, vazio


def _oval(cx, cy, rx, ry, n=24, rot=0.0):
    c, s = math.cos(rot), math.sin(rot)
    out = []
    for k in range(n):
        a = TAU * k / n
        x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out


def _contorno(T, pts, larg):
    return T.lines([(*a, *b, 1) for a, b in zip(pts, pts[1:] + pts[:1])], larg)


class _Escala:
    """Uma Tela que desenha tudo `k` vezes maior (coordenadas e larguras), para aumentar um desenho inteiro."""

    def __init__(self, T, k):
        self.T, self.k = T, k

    def __getattr__(self, nome):
        return getattr(self.T, nome)

    def gauss(self, cx, cy, sx, sy=None):
        k = self.k
        return self.T.gauss(cx * k, cy * k, sx * k, None if sy is None else sy * k)

    def ring(self, radius, width, cx=0, cy=0, squash=1.0):
        k = self.k
        return self.T.ring(radius * k, width * k, cx * k, cy * k, squash)

    def splats(self, points, sigma):
        return self.T.splats([(x * self.k, y * self.k, w) for x, y, w in points], sigma * self.k)

    def lines(self, segs, width, blur=0.0):
        k = self.k
        return self.T.lines([(a * k, b * k, c * k, d * k, w) for a, b, c, d, w in segs], width * k, blur)

    def tapered(self, segs, width):
        k = self.k
        return self.T.tapered([(a * k, b * k, c * k, d * k, w) for a, b, c, d, w in segs], width * k)

    def polyline(self, pts, width, w=1.0, blur=0.0):
        return self.T.polyline([(x * self.k, y * self.k) for x, y in pts], width * self.k, w, blur)

    def polys(self, shapes, blur=0.0):
        return self.T.polys([([(x * self.k, y * self.k) for x, y in pts], w) for pts, w in shapes], blur)


def _maior(fn, T, t, rng, k):
    return fn(_Escala(T, k), t, rng)


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def strix(T, t, rng):
    return _maior(_strix, T, t, rng, 1.4)


def _strix(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2)
    # a pasta abrindo: duas folhas que giram para os lados
    for s in (-1, 1):
        ang = s * 0.9 * abre
        folha = _gira([(0, -0.3), (s * 0.34, -0.3), (s * 0.34, 0.24), (0, 0.24)], ang * 0.25)
        G += T.polys([(folha, 1.0)], 0.004) * 0.35 * (1 - rel(t, 0.75, 0.92))
        G += _contorno(T, folha, 0.012) * (1 - rel(t, 0.75, 0.92))
    # o carimbo "STRIX": uma coruja estilizada (dois olhos e o bico)
    carimbo = pulso(t, 0.18, 0.55)
    for s in (-1, 1):
        G += T.ring(0.06, 0.016, cx=s * 0.08, cy=-0.12) * carimbo * 1.2
    G += T.polys([([(-0.03, -0.06), (0.03, -0.06), (0, 0.0)], 1.0)]) * carimbo
    # três barras de Carga subindo
    sobe = ease_out(rel(t, 0.35, 0.8), 2)
    for k, x in enumerate((-0.2, 0.0, 0.2)):
        h = 0.08 + 0.32 * sobe * (0.8 + 0.1 * k)
        G += T.polys([([(x - 0.045, 0.32), (x + 0.045, 0.32), (x + 0.045, 0.32 - h), (x - 0.045, 0.32 - h)], 1.0)]) * 0.9
        H += T.gauss(x, 0.32 - h, 0.03) * sobe * 1.3
    return G * env, H * env


def faca(T, t, rng):
    return _maior(_faca, T, t, rng, 1.3)


def _faca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    gira = ease_out(rel(t, 0.0, 0.4), 2)
    ang = TAU * 1.5 * gira
    lamina = _gira([(-0.02, -0.3), (0.05, -0.05), (0.02, 0.06), (-0.02, 0.06)], ang)
    cabo = _gira([(-0.03, 0.06), (0.03, 0.06), (0.03, 0.22), (-0.03, 0.22)], ang)
    G += T.polys([(lamina, 1.0)], 0.003) * 1.2 * (1 - rel(t, 0.4, 0.5))
    G += T.polys([(cabo, 1.0)], 0.003) * 0.5 * (1 - rel(t, 0.4, 0.5))
    H += T.polys([(lamina, 1.0)], 0.004) * 0.6 * (1 - rel(t, 0.4, 0.5))
    # dois cortes em X
    for k, (a0, a1) in enumerate(((-0.45, 0.45), (0.45, -0.45))):
        c = rel(t, 0.4 + 0.12 * k, 0.55 + 0.12 * k)
        if c <= 0:
            continue
        x0, y0, x1, y1 = -0.4, a0, -0.4 + 0.8 * ease_out(c, 2), a0 + (a1 - a0) * ease_out(c, 2)
        G += T.tapered([(x0, y0, x1, y1, 1)], 0.04) * 1.4 * (1 - rel(t, 0.75, 0.95))
        H += T.lines([(x0, y0, x1, y1, 1)], 0.008) * 1.2 * (1 - rel(t, 0.75, 0.95))
    return G * env, H * env


def terreno(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    # o laço no chão (elipse achatada) que fecha e puxa para cima
    fecha = ease_in(rel(t, 0.1, 0.5), 2)
    r = 0.42 * (1 - 0.55 * fecha)
    G += T.ring(r, 0.022, cy=0.25, squash=2.8) * 1.1
    # folhas e terra levantando quando a armadilha dispara
    sobe = rel(t, 0.45, 0.9)
    if sobe > 0:
        q = np.random.default_rng(31)
        pts = []
        for _ in range(16):
            a = q.uniform(0, TAU)
            d = q.uniform(0.05, 0.3)
            pts.append((d * math.cos(a), 0.25 - 0.5 * ease_out(sobe, 2) * q.uniform(0.5, 1.0), 1.0))
        G += T.splats(pts, 0.02) * (1 - sobe) * 1.2
    # a corda esticando para cima, prendendo
    corda = rel(t, 0.45, 0.65)
    G += T.lines([(0, 0.25, 0, 0.25 - 0.7 * corda, 1)], 0.014) * (1 - rel(t, 0.8, 0.95)) * 1.1
    H += T.gauss(0, 0.25, 0.08) * pulso(t, 0.4, 0.7) * 1.5
    return G * env, H * env


def inibidores(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    # os dois anéis dourados voando para fora
    voa = ease_out(rel(t, 0.0, 0.45), 2)
    for s in (-1, 1):
        cx, cy = s * (0.18 + 0.45 * voa), 0.1 - 0.35 * voa
        G += T.ring(0.07, 0.02, cx=cx, cy=cy, squash=2.0) * (1 - rel(t, 0.4, 0.6)) * 1.3
        H += T.gauss(cx, cy, 0.04) * (1 - voa) * 0.8
    # a aura do Chaos explodindo em espinhos (Shadow: vermelho e preto)
    aura = rel(t, 0.25, 0.9)
    if aura > 0:
        for k in range(10):
            a = TAU * k / 10 + 0.3
            L = 0.15 + 0.4 * ease_out(aura, 2) * (0.8 + 0.2 * math.sin(k * 2.1))
            G += T.tapered([(L * math.cos(a), L * math.sin(a), 0.06 * math.cos(a), 0.06 * math.sin(a), 1)], 0.05) * (1 - rel(t, 0.7, 0.95)) * 1.2
        G += T.ring(0.1 + 0.4 * aura, 0.03) * (1 - aura) * 1.2
        H += T.gauss(0, 0, 0.12) * pulso(t, 0.25, 0.8) * 1.6
    return G * env, H * env


def cogumelo(T, t, rng):
    return _maior(_cogumelo, T, t, rng, 1.6)


def _cogumelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    pula = rel(t, 0.0, 0.45)
    y = -0.05 - 0.3 * math.sin(math.pi * pula)
    chapeu = [(x, y - 0.04 - 0.12 * math.sqrt(max(0.0, 1 - (x / 0.2) ** 2))) for x in np.linspace(-0.2, 0.2, 14)]
    chapeu = chapeu + [(0.2, y), (-0.2, y)]
    G += T.polys([(chapeu, 1.0)], 0.004) * (1 - rel(t, 0.45, 0.55)) * 1.0
    G += T.polys([([(-0.09, y), (0.09, y), (0.08, y + 0.14), (-0.08, y + 0.14)], 1.0)], 0.004) * 0.6 * (1 - rel(t, 0.45, 0.55))
    for dx in (-0.1, 0.0, 0.1):
        G += T.gauss(dx, y - 0.09, 0.025) * -0.6 * (1 - rel(t, 0.45, 0.55))
    # crescer em degraus (pequeno → grande, como no jogo)
    cresce = rel(t, 0.45, 0.85)
    if cresce > 0:
        degrau = [0.15, 0.25, 0.18, 0.32, 0.42][min(4, int(cresce * 5))]
        G += T.ring(degrau, 0.03) * (1 - rel(t, 0.8, 0.95)) * 1.3
        H += T.gauss(0, 0, degrau * 0.6) * (1 - cresce) * 1.2
        G += sum(T.polys([(estrela(0.4 * math.cos(a), 0.4 * math.sin(a), 0.05), 1.0)]) for a in (0.5, 2.3, 4.0)) * pulso(t, 0.6, 0.95)
    return G * env, H * env


def banana(T, t, rng):
    return _maior(_banana, T, t, rng, 1.35)


def _banana(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    voa = rel(t, 0.0, 0.5)
    cx, cy = -0.35 + 0.35 * voa, -0.3 + 0.55 * ease_in(voa, 2)
    ang = TAU * 1.2 * voa
    casca = []
    for k in range(3):
        a = ang + TAU * k / 3
        casca.append([(cx, cy), (cx + 0.16 * math.cos(a - 0.25), cy + 0.16 * math.sin(a - 0.25)), (cx + 0.2 * math.cos(a), cy + 0.2 * math.sin(a)), (cx + 0.16 * math.cos(a + 0.25), cy + 0.16 * math.sin(a + 0.25))])
    G += T.polys([(c, 1.0) for c in casca], 0.004) * 1.1
    # o escorregão: o risco no chão e as gotinhas de susto
    esc = rel(t, 0.5, 0.8)
    if esc > 0:
        G += T.tapered([(-0.05, 0.27, -0.05 + 0.45 * ease_out(esc, 2), 0.27, 1)], 0.03) * (1 - rel(t, 0.8, 0.95)) * 1.3
        gotas = [(0.1 + 0.06 * k, 0.05 - 0.12 * esc - 0.04 * k, 1.0) for k in range(3)]
        G += T.splats(gotas, 0.025) * (1 - esc) * 1.2
        H += T.gauss(0.15, 0.27, 0.06) * pulso(t, 0.5, 0.75) * 1.5
    return G * env, H * env


def kuririn_nao(T, t, rng):
    return _maior(_kuririn_nao, T, t, rng, 1.45)


def _kuririn_nao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    bum = rel(t, 0.0, 0.4)
    G += T.ring(0.08 + 0.4 * ease_out(bum, 2), 0.06 * (1 - bum) + 0.01) * (1 - bum) * 1.6
    H += T.gauss(0, 0, 0.18 * ease_out(bum, 2) + 0.02) * (1 - bum) * 2.2
    # as auras de raiva subindo (chamas em pé)
    raiva = rel(t, 0.3, 0.95)
    if raiva > 0:
        for x in (-0.3, 0.0, 0.3):
            for k in range(4):
                fase = (raiva * 2 + k * 0.25) % 1
                y = 0.3 - 0.6 * fase
                G += T.tapered([(x, y - 0.12, x + 0.05 * math.sin(k * 3 + fase * 6), y + 0.08, 1)], 0.05) * (1 - fase) * 0.9
            H += T.gauss(x, 0.1, 0.06) * pulso(t, 0.35, 0.95) * 0.8
    return G * env, H * env


def evoluiu(T, t, rng):
    return _maior(_evoluiu, T, t, rng, 1.3)


def _evoluiu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cobre = ease_out(rel(t, 0.0, 0.6), 2)
    # escamas em fileiras, aparecendo de baixo para cima
    for lin in range(4):
        for col in range(5):
            y = 0.3 - 0.16 * lin
            x = -0.32 + 0.16 * col + (0.08 if lin % 2 else 0)
            if cobre < (lin + col * 0.2) / 5:
                continue
            escama = [(x - 0.07, y), (x, y - 0.1), (x + 0.07, y), (x, y + 0.03)]
            G += _contorno(T, escama, 0.01) * 0.9 + T.polys([(escama, 1.0)], 0.003) * 0.25
    # a seta de evolução subindo
    seta = rel(t, 0.45, 0.85)
    if seta > 0:
        y = 0.2 - 0.5 * ease_out(seta, 2)
        G += T.polys([([(-0.1, y + 0.05), (0, y - 0.08), (0.1, y + 0.05)], 1.0)]) * 1.4 * (1 - rel(t, 0.8, 0.95))
        G += T.lines([(0, y + 0.05, 0, y + 0.25, 1)], 0.03) * (1 - rel(t, 0.8, 0.95))
        H += T.gauss(0, y, 0.05) * 1.4 * (1 - seta)
    return G * env, H * env


def improviso(T, t, rng):
    return _maior(_improviso, T, t, rng, 1.25)


def _improviso(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    gira = TAU * 2.5 * ease_out(rel(t, 0.0, 0.6), 1.5)
    for s in (0, math.pi):
        a = gira + s
        p1 = (0.08 * math.cos(a), 0.08 * math.sin(a))
        p2 = (0.34 * math.cos(a), 0.34 * math.sin(a))
        G += T.lines([(*p1, *p2, 1)], 0.04) * (1 - rel(t, 0.6, 0.7)) * 1.1
    G += T.lines([(0.08 * math.cos(gira), 0.08 * math.sin(gira), 0.08 * math.cos(gira + math.pi), 0.08 * math.sin(gira + math.pi), 1)], 0.01) * (1 - rel(t, 0.6, 0.7))
    G += T.ring(0.34, 0.01) * 0.4 * (1 - rel(t, 0.55, 0.7))
    # o número sorteado: dados pulando (½ a 2×)
    sai = rel(t, 0.5, 0.95)
    if sai > 0:
        for k, x in enumerate((-0.22, 0.0, 0.22)):
            y = -0.05 - 0.25 * math.sin(math.pi * min(1, sai * 1.3 - k * 0.1))
            dado = [(x - 0.07, y - 0.07), (x + 0.07, y - 0.07), (x + 0.07, y + 0.07), (x - 0.07, y + 0.07)]
            G += _contorno(T, dado, 0.012) * (1 - rel(t, 0.85, 0.98)) * 1.1
            for p in range(k + 1):
                G += T.gauss(x - 0.03 + 0.03 * p, y - 0.03 + 0.03 * p, 0.012) * 1.2
    return G * env, H * env


def scooby_lanche(T, t, rng):
    return _maior(_scooby_lanche, T, t, rng, 1.5)


def _scooby_lanche(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    surge = ease_out(rel(t, 0.0, 0.25), 2)
    s = 0.5 + 0.5 * surge
    osso = [(-0.22 * s, -0.04 * s), (0.22 * s, -0.04 * s), (0.22 * s, 0.04 * s), (-0.22 * s, 0.04 * s)]
    morde = rel(t, 0.35, 0.6)
    G += T.polys([(osso, 1.0)], 0.004) * 1.0 * (1 - rel(t, 0.6, 0.7))
    for x in (-0.22, 0.22):
        for y in (-0.05, 0.05):
            G += T.gauss(x * s, y * s, 0.045 * s) * 1.4 * (1 - (morde if x > 0 else 0)) * (1 - rel(t, 0.6, 0.7))
    # a mordida: semicírculo apagando a ponta
    G += T.gauss(0.22 * s, 0, 0.07) * -2.5 * morde
    # farelos voando e corações (coragem)
    far = rel(t, 0.45, 0.95)
    if far > 0:
        q = np.random.default_rng(9)
        pts = [(0.2 + q.uniform(-0.05, 0.4) * ease_out(far, 2), q.uniform(-0.3, 0.2) + 0.2 * far, 1.0) for _ in range(10)]
        G += T.splats(pts, 0.018) * (1 - far) * 1.2
        H += T.gauss(0, -0.25 * far, 0.05) * pulso(t, 0.5, 0.95) * 1.2
    return np.clip(G, 0, None) * env, H * env


def desastrado(T, t, rng):
    return _maior(_desastrado, T, t, rng, 1.3)


def _desastrado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    # o "bonk": estrela de impacto grande
    bonk = pulso(t, 0.0, 0.35)
    G += T.polys([(estrela(0, 0, 0.32 * bonk + 0.02, 0.2, 8, 0.45), 1.0)], 0.004) * bonk * 1.3
    H += T.gauss(0, 0, 0.1) * bonk * 1.8
    # estrelinhas de tontura girando em volta da cabeça
    tonto = rel(t, 0.25, 0.95)
    if tonto > 0:
        for k in range(5):
            a = TAU * k / 5 + TAU * 1.5 * tonto
            cx, cy = 0.3 * math.cos(a), -0.2 + 0.1 * math.sin(a)
            G += T.polys([(estrela(cx, cy, 0.05, a), 1.0)]) * (1 - rel(t, 0.8, 0.95)) * 1.2
        G += T.ring(0.3, 0.008, cy=-0.2, squash=3.0) * 0.5 * (1 - rel(t, 0.8, 0.95))
    return G * env, H * env


def infinito(T, t, rng):
    return _maior(_infinito, T, t, rng, 1.3)


def _infinito(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    voa = ease_out(rel(t, 0.0, 0.6), 2)
    # o rastro do voo desenhando o símbolo do infinito
    pts = []
    for k in range(int(4 + 60 * voa)):
        u = TAU * k / 64
        d = 1 + math.sin(u) ** 2
        pts.append((0.38 * math.cos(u) / d, 0.38 * math.sin(u) * math.cos(u) / d))
    if len(pts) > 1:
        G += T.polyline(pts, 0.03) * (1 - rel(t, 0.75, 0.95)) * 1.1
        hx, hy = pts[-1]
        H += T.gauss(hx, hy, 0.04) * 1.8 * (1 - rel(t, 0.6, 0.8))
        G += T.polys([(estrela(hx, hy, 0.06), 1.0)]) * (1 - rel(t, 0.6, 0.8))
    # o brilho de "ao infinito e além"
    G += T.flare(0, 0, 0.5 * pulso(t, 0.55, 0.95) + 0.002, 0.0, 0.01) * 0.9
    return G * env, H * env


def achatado(T, t, rng):
    return _maior(_achatado, T, t, rng, 1.2)


def _achatado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    # achatado como panqueca → estoura de volta (sy cresce, sx volta)
    volta = rel(t, 0.25, 0.55)
    sx = 0.4 - 0.2 * ease_out(volta, 3)
    sy = 0.04 + 0.26 * ease_out(volta, 3) * (1 + 0.2 * math.sin(volta * 12) * (1 - volta))
    corpo = _oval(0, 0.25 - sy, sx, sy)
    G += T.polys([(corpo, 1.0)], 0.004) * 0.35 * (1 - rel(t, 0.75, 0.9))
    G += _contorno(T, corpo, 0.014) * (1 - rel(t, 0.75, 0.9))
    # orelhas de gato
    for s in (-1, 1):
        G += T.polys([([(s * sx * 0.3, 0.25 - 2 * sy), (s * sx * 0.6, 0.25 - 2 * sy - 0.1 * volta), (s * sx * 0.75, 0.25 - 1.7 * sy)], 1.0)]) * (1 - rel(t, 0.75, 0.9))
    # as molas do "boing"
    mola = pulso(t, 0.4, 0.8)
    for s in (-1, 1):
        pts = [(s * (0.42 + 0.03 * math.sin(k * 1.6)), 0.25 - 0.05 * k) for k in range(9)]
        G += T.polyline(pts, 0.012) * mola * 1.1
    H += T.gauss(0, 0.05, 0.1) * pulso(t, 0.45, 0.75) * 1.4
    return G * env, H * env


def goool(T, t, rng):
    return _maior(_goool, T, t, rng, 1.4)


def _goool(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    gira = ease_in(rel(t, 0.0, 0.4), 2)
    ang = -2.2 + 2.6 * gira
    cabo = (0.4 * math.cos(ang), 0.4 * math.sin(ang))
    pa = (cabo[0] + 0.14 * math.cos(ang + 1.3), cabo[1] + 0.14 * math.sin(ang + 1.3))
    G += T.lines([(0, 0, *cabo, 1), (*cabo, *pa, 1)], 0.035) * (1 - rel(t, 0.55, 0.7)) * 1.2
    for k in range(1, 4):
        a2 = ang - 0.2 * k
        G += T.lines([(0, 0, 0.4 * math.cos(a2), 0.4 * math.sin(a2), 1)], 0.02) * (0.3 / k) * gira * (1 - rel(t, 0.4, 0.5))
    # a pancada: o disco voando e o estalo
    pan = rel(t, 0.4, 0.85)
    if pan > 0:
        x = 0.1 + 0.4 * ease_out(pan, 2)
        G += T.ring(0.05, 0.03, cx=x, cy=0.05, squash=2.0) * 1.3 * (1 - rel(t, 0.75, 0.9))
        G += T.tapered([(x - 0.3, 0.05, x - 0.05, 0.05, 1)], 0.03) * (1 - pan)
        G += T.polys([(estrela(0.05, 0.05, 0.2 * pulso(t, 0.4, 0.6) + 0.01, 0.0, 6), 1.0)]) * pulso(t, 0.4, 0.6) * 1.3
        H += T.gauss(0.05, 0.05, 0.07) * pulso(t, 0.4, 0.6) * 1.8
    return G * env, H * env


REGISTRO = [
    ("mu_strix", strix, GRANDE, "Loid · o dossiê da Operação Strix e a Carga subindo", False),
    ("mu_faca", faca, GRANDE, "Leon · a faca girando e o corte em X", False),
    ("mu_terreno", terreno, GRANDE, "Lara · o laço da armadilha fechando e prendendo", False),
    ("mu_inibidores", inibidores, GRANDE, "Shadow · os anéis inibidores voando e a aura explodindo", False),
    ("mu_cogumelo", cogumelo, GRANDE, "Mario · o Super Cogumelo pulando e o crescer em degraus", False),
    ("mu_banana", banana, GRANDE, "Donkey Kong · a casca de banana caindo e o escorregão", False),
    ("mu_kuririn_nao", kuririn_nao, GRANDE, "Kuririn · a explosão e as auras de raiva dos aliados", False),
    ("mu_evoluiu", evoluiu, GRANDE, "Garou · as escamas cobrindo e a seta de evolução", False),
    ("mu_improviso", improviso, GRANDE, "Michelangelo · os nunchakus girando e os dados do dano", False),
    ("mu_scooby_lanche", scooby_lanche, GRANDE, "Scooby · o biscoito mordido e os farelos", False),
    ("mu_desastrado", desastrado, GRANDE, "Pateta · o bonk e as estrelas de tontura", False),
    ("mu_infinito", infinito, GRANDE, "Buzz · o rastro do voo desenhando o infinito", False),
    ("mu_achatado", achatado, GRANDE, "Tom · achatado que volta à forma com molas", False),
    ("mu_goool", goool, GRANDE, "Casey Jones · o taco rodando e a pancada com o disco", False),
]
