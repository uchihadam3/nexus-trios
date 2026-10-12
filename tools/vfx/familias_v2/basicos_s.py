"""Ataques básicos com animação própria, lote s (personagens novos).

Asta, Rem, Kirito, Spike, Vash, Senku, Hinata, Jiraiya, Tsunade, Sailor Mars, Steven, Garnet, Johnny Bravo,
Dexter e Aku: a espada larga de antimagia com os fiapos negros, a maça de espinhos girando na corrente, os dois
cortes em X do Kirito, o chute de Jeet Kune Do com a fumaça, o tiro do Vash e a pena, o frasco que estoura em
reação, a palma suave com os pontos de chakra, as agulhas de cabelo do Jiraiya, o soco que racha o chão da
Tsunade, o pergaminho que pega fogo, o escudo rosa do Steven, as manoplas da Garnet, o brilho do Johnny Bravo, a
arma de raio do Dexter e os olhos de laser do Aku.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .basicos_a import _PUNHO, _move, _punho
from .basicos_k import _borda, _contorno, _estouro, _folha, _gira, _gotas
from .basicos_l import _estrelinhas, _sapato
from .rodada13 import _chamas


# ================================================================== Asta
def espada_anti_magia(T, t, rng):
    """A espada do Asta: a espada larga e pesada (a lâmina grossa e reta) desce com os fiapos negros da antimagia
    saindo dela, e o corte arrebenta no rival."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    desce = ease_in(rel(t, 0.05, 0.32), 2)
    if t < 0.55:
        some = 1 - rel(t, 0.42, 0.55)
        ang = -2.3 + 1.9 * desce
        px, py = -0.4, 0.4
        L = 0.95
        tip = (px + L * math.cos(ang), py + L * math.sin(ang))
        nx, ny = -math.sin(ang), math.cos(ang)
        w = 0.09
        lam = [(px + nx * w, py + ny * w), (tip[0] + nx * w * 0.8, tip[1] + ny * w * 0.8), (tip[0], tip[1]), (tip[0] - nx * w * 0.8, tip[1] - ny * w * 0.8), (px - nx * w, py - ny * w)]
        E = T.polys([(lam, 1.0)])
        G += (E * 0.45 + _borda(T, E, 0.008) * 1.3) * some
        q = np.random.default_rng(int(t * 30) % 7)
        for k in range(6):
            u = q.uniform(0.2, 1)
            bx, by = px + L * u * math.cos(ang), py + L * u * math.sin(ang)
            pts = [(bx + 0.15 * s * nx + 0.03 * math.sin(s * 12 + t * 30), by + 0.15 * s * ny - 0.1 * s) for s in np.linspace(0, 1, 8)]
            G += T.polyline(pts, 0.012) * some * 0.9
    g, h = _estouro(T, t, 0.3, 0.65, 0.1, -0.05, 0.4, 11, 3)
    G += g
    H += h * 0.6
    return G * env, H * env


# ================================================================== Rem
def maca_de_rem(T, t, rng):
    """A maça da Rem: a bola de espinhos gira na ponta da corrente (o arco do giro e a corrente esticada) e esmaga o
    rival."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    gira = rel(t, 0.0, 0.4)
    if t < 0.55:
        some = 1 - rel(t, 0.45, 0.55)
        a = -math.pi * 0.9 + TAU * 1.1 * ease_in(gira, 1.4)
        px, py = -0.55, 0.15
        r = 0.55
        bx, by = px + r * math.cos(a), py + r * math.sin(a) * 0.8
        elos = [(px + (bx - px) * u, py + (by - py) * u) for u in np.linspace(0, 1, 10)]
        G += T.lines([(elos[i][0], elos[i][1], elos[i + 1][0], elos[i + 1][1], 1.0) for i in range(0, 9, 1)], 0.01) * some
        G += T.splats([(x, y, 0.8) for x, y in elos], 0.012) * some
        bola = T.ring(0.07, 0.02, bx, by) + T.gauss(bx, by, 0.05) * 0.5
        esp = T.polys([(estrela(bx, by, 0.13, a * 2, 8, 0.55), 1.0)])
        G += (bola + _borda(T, esp, 0.006) * 1.2) * some
        G += T.arc_band(r, 0.04, a - 1.4, a, squash=0.8, cx=px, cy=py, taper=0.6) * 0.5 * some
    g, h = _estouro(T, t, 0.4, 0.75, 0.0, 0.05, 0.4, 11, 5)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Kirito
def espadas_duplas(T, t, rng):
    """As duas espadas do Kirito: dois cortes rápidos que se cruzam em X, um de cada espada, com os clarões no cruzamento."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    for k, (x1, y1, x2, y2, t0) in enumerate(((-0.6, -0.55, 0.6, 0.5, 0.08), (0.6, -0.55, -0.6, 0.5, 0.18))):
        p = ease_out(rel(t, t0, t0 + 0.1), 3)
        ini = rel(t, t0 + 0.12, t0 + 0.4)
        if p > 0 and ini < 1:
            L = T.polys([(lamina(x1, y1, x2, y2, 0.045, prog=p, inicio=ini), 1.0)])
            G += L * 1.4 + T.blur(L, 0.02) * 0.6
            H += L * 0.6
    cruz = pulso(t, 0.22, 0.55)
    H += T.flare(0, 0, 0.6 * cruz + 0.01, 0.0, 0.014) * cruz * 1.4 + T.flare(0, 0, 0.4 * cruz + 0.01, 0.785, 0.01) * cruz
    g, h = _estouro(T, t, 0.24, 0.55, 0, 0, 0.3, 10, 7, 0.016)
    G += g * 0.8
    H += h * 0.6
    return G * env, H * env


# ================================================================== Spike
def chute_de_spike(T, t, rng):
    """O chute do Spike: a postura relaxada de Jeet Kune Do (a mão chamando), o chute rápido e fluido em arco com o
    sapato acertando, e a fumaça do cigarro desenhando a voltinha."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    chama = pulso(t, 0.0, 0.2)
    if chama > 0:
        G += T.lines([(-0.75, -0.2, -0.65, -0.25, 1.0), (-0.65, -0.25, -0.6, -0.2, 1.0)], 0.012) * chama * 1.1
    gira = ease_out(rel(t, 0.15, 0.38), 2.5)
    if gira > 0 and t < 0.55:
        some = 1 - rel(t, 0.4, 0.55)
        a1 = math.pi - 0.3 + 2.0 * gira
        A = T.arc_band(0.55, 0.05, a1 - 1.6, a1, squash=0.6, cx=-0.05, cy=0.25, crescente=True)
        G += (A * 1.2 + T.blur(A, 0.02) * 0.4) * some
        sx, sy = -0.05 + 0.55 * math.cos(a1), 0.25 + 0.33 * math.sin(a1)
        G += T.polys([(_sapato(sx, sy, 1.5, a1 + math.pi / 2), 1.0)]) * some * 1.1
    g, h = _estouro(T, t, 0.36, 0.65, 0.05, 0, 0.3, 9, 9)
    G += g
    H += h
    fumo = rel(t, 0.0, 1.0)
    pts = []
    for j in range(30):
        u = j / 29
        a = TAU * 1.5 * u + t * 2
        pts.append((-0.7 + 0.06 * math.cos(a) + 0.08 * u, -0.3 - 0.45 * u * fumo + 0.05 * math.sin(a), (1 - u) * (1 - fumo) * 0.7))
    G += T.splats(pts, 0.022) * 0.9
    return G * env, H * env


# ================================================================== Vash
def tiro_de_vash(T, t, rng):
    """O tiro do Vash: o revólver gira no dedo (o rodopio de brilho), dispara certeiro no rival — sem matar, só tirando
    a arma da mão — e uma pena branca cai devagar."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    gira = pulso(t, 0.0, 0.25)
    if gira > 0:
        G += T.arc_band(0.15, 0.035, t * 40, t * 40 + 4.5, cx=-0.75, cy=0.05, taper=0.5) * gira * 1.4
        H += T.gauss(-0.75, 0.05, 0.03) * gira
    cano = (-0.8, 0.05)
    c = pulso(t, 0.25, 0.35)
    H += T.flare(cano[0], cano[1], 0.3 * c + 0.01, 0, 0.012) * c * 1.4
    v = rel(t, 0.25, 0.33)
    if 0 < v and t < 0.5:
        x = cano[0] + (0.0 - cano[0]) * min(1, v)
        G += T.tapered([(cano[0], cano[1], x, cano[1] * (1 - min(1, v)), 1.0)], 0.028) * (1 - rel(t, 0.33, 0.5)) * 1.5
    g, h = _estouro(T, t, 0.32, 0.6, 0, 0, 0.35, 9, 11)
    G += g
    H += h
    pena = rel(t, 0.35, 1.0)
    if 0 < pena < 1:
        x = 0.25 + 0.1 * math.sin(pena * 7)
        y = -0.6 + 0.9 * pena
        P = T.polys([(_folha(x, y, 0.12, math.pi / 2 + 0.5 * math.sin(pena * 7)), 1.0)])
        G += (P * 0.7 + _borda(T, P, 0.005)) * (1 - rel(t, 0.85, 1.0))
    return G * env, H * env


# ================================================================== Senku
def frasco_de_senku(T, t, rng):
    """O frasco do Senku: o frasco de laboratório (o fundo redondo e o gargalo) voa girando em arco, quebra no rival e a
    reação química ferve em bolhas e fumaça — "dez bilhões por cento"."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    voa = rel(t, 0.0, 0.32)
    if voa < 1:
        x = -0.85 + 0.85 * voa
        y = -0.5 * math.sin(math.pi * voa)
        ang = voa * 8
        corpo = T.ring(0.11, 0.02, x, y)
        gar = _gira([(0, -0.11), (0, -0.25)], ang, x, y)
        G += corpo * 1.3 + T.polyline(gar, 0.024) * 1.3 + T.gauss(x, y + 0.03, 0.06) * 0.6
    quebra = rel(t, 0.32, 0.6)
    if 0 < quebra < 1:
        q = np.random.default_rng(13)
        cacos = []
        for _ in range(8):
            a = q.uniform(0, TAU)
            d = 0.35 * ease_out(quebra, 2) * q.uniform(0.5, 1)
            cacos += _contorno(_gira([(0, -0.02), (0.02, 0.02), (-0.02, 0.01)], quebra * 8 + a, d * math.cos(a), d * math.sin(a)), 1 - quebra)
        G += T.lines(cacos, 0.008) * 1.2
        H += T.gauss(0, 0, 0.06) * (1 - quebra) ** 2 * 1.5
    reacao = rel(t, 0.35, 1.0)
    if 0 < reacao < 1:
        q = np.random.default_rng(15)
        for k in range(10):
            f = (reacao * 1.5 + q.uniform(0, 1)) % 1
            bx = q.uniform(-0.3, 0.3)
            G += T.ring(0.02 + 0.03 * f, 0.007, bx, 0.15 - 0.6 * f) * (1 - f) * math.sin(math.pi * reacao) * 1.2
        fum = [(q.uniform(-0.3, 0.3), -0.1 - 0.4 * reacao + q.uniform(-0.1, 0.1), math.sin(math.pi * reacao) * 0.5) for _ in range(10)]
        G += T.splats(fum, 0.06) * 0.6
    return G * env, H * env


# ================================================================== Hinata
def palma_gentil(T, t, rng):
    """A palma da Hinata: o Byakugan acende (as veias em volta do olho), a palma aberta avança suave e acerta, e os pontos
    de chakra do rival se apagam um a um (as faíscas pequenas em pontos)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    olho = pulso(t, 0.0, 0.35)
    if olho > 0:
        q = np.random.default_rng(17)
        for k in range(5):
            a = TAU * k / 5 + 0.3
            G += T.polyline(jagged(q, -0.65 + 0.07 * math.cos(a), -0.5 + 0.07 * math.sin(a), -0.65 + 0.25 * math.cos(a), -0.5 + 0.25 * math.sin(a), 3, 0.3), 0.011) * olho * 1.2
        H += T.gauss(-0.65, -0.5, 0.035) * olho * 1.5 + T.ring(0.06, 0.01, -0.65, -0.5) * olho
    vai = ease_out(rel(t, 0.1, 0.35), 2)
    if vai > 0 and t < 0.55:
        x = -0.75 + 0.65 * vai
        pts = [(-0.12, 0.1), (-0.12, -0.06), (-0.06, -0.08), (-0.04, -0.22), (0.0, -0.08), (0.03, -0.24), (0.06, -0.08), (0.1, -0.2),
               (0.12, -0.04), (0.16, -0.1), (0.15, 0.04), (0.08, 0.12)]
        M = T.polys([([(x + px * 1.4, py * 1.4) for px, py in pts], 1.0)])
        G += (M * 0.4 + _borda(T, M, 0.007) * 1.3) * (1 - rel(t, 0.45, 0.55))
        G += T.gauss(x + 0.02, 0, 0.12) * 0.4 * vai
    pontos = rel(t, 0.35, 0.9)
    if 0 < pontos < 1:
        for k, (px, py) in enumerate(((0.05, -0.2), (-0.05, -0.05), (0.08, 0.08), (0.0, 0.22), (0.12, -0.1))):
            b = rel(pontos, 0.12 * k, 0.12 * k + 0.4)
            if 0 < b < 1:
                H += T.flare(px, py, 0.2 * (1 - b) + 0.01, k, 0.009) * (1 - b) * 1.5
                G += T.ring(0.03 + 0.1 * b, 0.012, px, py) * (1 - b) * 1.2
    return G * env, H * env


# ================================================================== Jiraiya
def agulhas_de_cabelo(T, t, rng):
    """O ataque do Jiraiya: a cabeleira branca vira um leque de agulhas duras que disparam juntas da esquerda, cravam
    no rival, e o soco fecha o golpe."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vai = ease_in(rel(t, 0.05, 0.25), 1.5)
    if vai > 0 and t < 0.5:
        some = 1 - rel(t, 0.35, 0.5)
        segs = []
        for k in range(9):
            a = (k - 4) * 0.08
            x0 = -0.85 + 0.75 * vai
            segs.append((x0 - 0.4 * math.cos(a), -0.4 * math.sin(a) + a * 1.2, x0, a * 1.2, 1.0))
        G += T.tapered(segs, 0.022) * 1.3 * some
    for k in range(5):
        b = rel(t, 0.25 + 0.02 * k, 0.45 + 0.02 * k)
        if 0 < b < 1:
            y = (k - 2) * 0.18
            H += T.gauss(-0.05, y, 0.03) * (1 - b) * 1.5
    soco = ease_in(rel(t, 0.38, 0.52), 2)
    if soco > 0 and t < 0.7:
        x = -0.6 + 0.52 * soco
        P, nos = _punho(T, x, 0.05, 1.5)
        G += (P * 0.6 + _borda(T, P, 0.006) * 1.0) * (1 - rel(t, 0.6, 0.7))
    g, h = _estouro(T, t, 0.52, 0.8, 0.05, 0.05, 0.35, 9, 19)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Tsunade
def soco_de_tsunade(T, t, rng):
    """O soco da Tsunade: o losango do Byakugou brilha na testa, o punho carregado de chakra desce no rival e o chão se
    abre numa cratera de rachaduras enormes."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    marca = pulso(t, 0.0, 0.3)
    if marca > 0:
        G += T.polys([([(-0.7, -0.62), (-0.66, -0.56), (-0.7, -0.5), (-0.74, -0.56)], 1.0)]) * marca * 1.3
        H += T.gauss(-0.7, -0.56, 0.02) * marca * 1.4
    desce = ease_in(rel(t, 0.12, 0.32), 2.5)
    if t < 0.5:
        y = -0.8 + 0.85 * desce
        P, nos = _punho(T, 0.0, y, 2.2, math.pi / 2)
        G += P * 0.6 + _borda(T, P, 0.007) * 1.3 + T.gauss(0, y, 0.15) * 0.3
    bate = rel(t, 0.32, 0.9)
    if 0 < bate < 1:
        b = ease_out(bate, 2.5)
        H += T.gauss(0, 0.15, 0.12) * (1 - bate) ** 2 * 2.0
        G += T.ring(0.1 + 0.7 * b, 0.04, 0, 0.3, squash=2.4) * (1 - bate) * 1.3
        q = np.random.default_rng(21)
        for k in range(9):
            a = math.pi * (k + 0.5) / 9
            G += T.polyline(jagged(q, 0, 0.3, 0.9 * b * math.cos(a) * (1 if k % 2 else 0.8), 0.3 + 0.25 * b * math.sin(a), 4, 0.25), 0.014) * (1 - rel(t, 0.8, 1.0)) * 1.2
        pts = [(q.uniform(-0.6, 0.6) * b, 0.3 - q.uniform(0, 0.5) * b, (1 - bate) * 0.7) for _ in range(14)]
        G += T.splats(pts, 0.03) * 1.0
    return G * env, H * env


# ================================================================== Sailor Mars
def pergaminho_de_fogo(T, t, rng):
    """O pergaminho da Sailor Mars: o ofuda (a tira de papel com o selo escrito) voa até o rival, gruda nele, o selo
    brilha — "Akuryō Taisan!" — e o papel pega fogo."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    voa = ease_out(rel(t, 0.0, 0.3), 2)
    if t < 0.7:
        x = -0.85 + 0.85 * voa
        ang = 0.6 * (1 - voa) + 0.1 * math.sin(t * 20) * (1 - voa)
        papel = _gira([(-0.06, -0.18), (0.06, -0.18), (0.06, 0.18), (-0.06, 0.18)], ang, x, 0.0)
        some = 1 - rel(t, 0.5, 0.7)
        G += T.lines(_contorno(papel), 0.012) * 1.2 * some
        selo = _gira([(0, -0.12), (0, 0.1)], ang, x, 0.0)
        G += T.polyline(selo, 0.01) * some
        G += T.lines([(*_gira([(-0.04, -0.05)], ang, x, 0)[0], *_gira([(0.04, -0.05)], ang, x, 0)[0], 1.0),
                      (*_gira([(-0.04, 0.03)], ang, x, 0)[0], *_gira([(0.04, 0.05)], ang, x, 0)[0], 1.0)], 0.008) * some
        H += T.gauss(x, 0.0, 0.04) * pulso(t, 0.3, 0.5) * 1.4
    fogo = rel(t, 0.42, 1.0)
    if 0 < fogo < 1:
        F = _chamas(T, t, 0.0, 0.2, 0.18, 0.5 * math.sin(math.pi * fogo), 7, 23)
        G += F * 0.9 + T.blur(F, 0.02) * 0.5
        H += F * 0.3
    return G * env, H * env


# ================================================================== Steven
def escudo_rosa(T, t, rng):
    """O escudo do Steven: o escudo redondo cor-de-rosa com a rosa em espiral no meio aparece no braço e bate de frente no
    rival, soltando a onda."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    forma = back(rel(t, 0.0, 0.2), 1.5)
    vem = ease_in(rel(t, 0.2, 0.38), 2)
    if forma > 0 and t < 0.55:
        x = -0.65 + 0.55 * vem
        r = 0.28 * forma
        some = 1 - rel(t, 0.45, 0.55)
        G += (T.ring(r, 0.025, x, 0) * 1.2 + T.ring(r * 0.85, 0.01, x, 0) * 0.6) * some
        esp = [(x + r * 0.5 * u * math.cos(u * 12), r * 0.5 * u * math.sin(u * 12)) for u in np.linspace(0, 1, 30)]
        G += T.polyline(esp, 0.012) * some * 1.1
        for k in range(5):
            a = TAU * k / 5
            G += T.polys([(_folha(x + r * 0.62 * math.cos(a), r * 0.62 * math.sin(a), 0.04 * forma, a), 1.0)]) * some * 0.8
    onda = rel(t, 0.36, 0.8)
    if 0 < onda < 1:
        G += T.ring(0.15 + 0.5 * ease_out(onda, 2), 0.035, 0.05, 0) * (1 - onda) * 1.2
        H += T.gauss(0.05, 0, 0.1) * (1 - onda) ** 2 * 1.5
    return G * env, H * env


# ================================================================== Garnet
def manopla_de_garnet(T, t, rng):
    """O soco da Garnet: as duas manoplas enormes (os punhos grandes e quadrados com as juntas marcadas) socam juntas,
    uma colada na outra, e o impacto sai em dobro."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    for k, (dy, t0) in enumerate(((-0.14, 0.05), (0.14, 0.13))):
        vai = ease_in(rel(t, t0, t0 + 0.22), 2.2)
        if t > t0 + 0.42:
            continue
        x = -0.85 + 0.75 * vai
        luva = [(x - 0.15, dy - 0.12), (x + 0.1, dy - 0.13), (x + 0.16, dy - 0.07), (x + 0.16, dy + 0.07), (x + 0.1, dy + 0.13), (x - 0.15, dy + 0.12)]
        M = T.polys([(luva, 1.0)])
        some = 1 - rel(t, t0 + 0.3, t0 + 0.42)
        G += (M * 0.6 + _borda(T, M, 0.008) * 1.3) * some
        G += T.lines([(x + 0.1, dy - 0.1 + 0.07 * j, x + 0.16, dy - 0.1 + 0.07 * j, 1.0) for j in range(4)], 0.008) * some
        g, h = _estouro(T, t, t0 + 0.2, t0 + 0.5, 0.05, dy, 0.32, 9, 25 + k)
        G += g
        H += h * 0.8
    return G * env, H * env


# ================================================================== Johnny Bravo
def soco_de_johnny(T, t, rng):
    """O soco do Johnny Bravo: o brilho nos óculos escuros ("ping!"), os riscos de pose do muque, e o soco convencido
    que acerta com o "hoo-ha"."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    brilho = pulso(t, 0.0, 0.25)
    if brilho > 0:
        G += T.lines([(-0.85, -0.5, -0.6, -0.5, 1.0)], 0.03) * brilho * 0.7
        H += T.flare(-0.62, -0.52, 0.25 * brilho + 0.01, 0.785, 0.01) * brilho * 1.6
    pose = pulso(t, 0.05, 0.4)
    if pose > 0:
        G += T.lines([(-0.95 + 0.06 * k, -0.15 - 0.05 * (k % 2), -0.9 + 0.06 * k, -0.25, 1.0) for k in range(4)], 0.01) * pose
    vai = ease_in(rel(t, 0.2, 0.4), 2)
    if vai > 0 and t < 0.6:
        x = -0.8 + 0.72 * vai
        P, nos = _punho(T, x, 0.05, 1.7)
        G += (P * 0.6 + _borda(T, P, 0.007) * 1.1) * (1 - rel(t, 0.5, 0.6))
    g, h = _estouro(T, t, 0.4, 0.7, 0.05, 0.05, 0.35, 9, 29)
    G += g
    H += h
    G += _estrelinhas(T, t, 0.45, 0.5, 0.05, -0.2, 5, 0.3, 31) * 1.1
    return G * env, H * env


# ================================================================== Dexter
def raio_de_dexter(T, t, rng):
    """A arma de raio do Dexter: o aparelhinho do laboratório carrega (os anéis no cano), solta o raio em zigue-zague
    com os anéis de energia viajando e o rival leva o choque científico."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    cano = (-0.8, 0.0)
    carga = pulso(t, 0.0, 0.3)
    for k in range(3):
        G += T.ring(0.05 + 0.03 * k, 0.008, cano[0] - 0.05 * k, cano[1], squash=0.5) * carga * 1.1
    vai = ease_out(rel(t, 0.2, 0.4), 2)
    some = 1 - rel(t, 0.45, 0.6)
    if vai > 0 and some > 0:
        pts = []
        for j in range(20):
            u = j / 19 * vai
            pts.append((cano[0] + 0.8 * u, 0.06 * (1 if j % 2 else -1) * (0 < j < 19)))
        G += T.polyline(pts, 0.016) * some * 1.3
        for k in range(3):
            u = (t * 3 + k / 3) % 1 * vai
            G += T.ring(0.05, 0.008, cano[0] + 0.8 * u, 0.0, squash=0.5) * some
    g, h = _estouro(T, t, 0.38, 0.65, 0, 0, 0.3, 9, 33)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Aku
def raio_de_aku(T, t, rng):
    """Os olhos do Aku: o rosto escuro com as sobrancelhas de fogo verde acende, os dois olhos disparam os lasers juntos
    e o rival leva a rajada."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    rosto = pulso(t, 0.0, 0.65)
    olhos = ((-0.75, -0.3), (-0.6, -0.3))
    if rosto > 0:
        for k, (ox, oy) in enumerate(olhos):
            F = _chamas(T, t, ox, oy - 0.06, 0.06, 0.18, 3, 35 + k)
            G += F * rosto * 0.9
        H += T.splats([(x, y, 1.0) for x, y in olhos], 0.02) * rosto * 1.6
    vai = ease_out(rel(t, 0.18, 0.3), 2)
    some = 1 - rel(t, 0.45, 0.6)
    if vai > 0 and some > 0:
        for k, (ox, oy) in enumerate(olhos):
            alvo = (-0.04 + 0.08 * k, 0.0)
            x = ox + (alvo[0] - ox) * vai
            y = oy + (alvo[1] - oy) * vai
            R = T.lines([(ox, oy, x, y, 1.0)], 0.025)
            G += (R * 1.2 + T.blur(R, 0.015) * 0.6) * some
            H += T.lines([(ox, oy, x, y, 1.0)], 0.008) * some
    g, h = _estouro(T, t, 0.28, 0.6, 0, 0, 0.32, 10, 37)
    G += g
    H += h
    return G * env, H * env


REGISTRO = [
    ("espada_anti_magia", espada_anti_magia, GRANDE, "Básico do Asta: a espada larga e a antimagia", False),
    ("maca_de_rem", maca_de_rem, GRANDE, "Básico da Rem: a maça girando na corrente", False),
    ("espadas_duplas", espadas_duplas, GRANDE, "Básico do Kirito: os dois cortes em X", False),
    ("chute_de_spike", chute_de_spike, GRANDE, "Básico do Spike: o chute fluido e a fumaça", False),
    ("tiro_de_vash", tiro_de_vash, GRANDE, "Básico do Vash: o tiro e a pena", False),
    ("frasco_de_senku", frasco_de_senku, GRANDE, "Básico do Senku: o frasco e a reação", False),
    ("palma_gentil", palma_gentil, GRANDE, "Básico da Hinata: o Byakugan e a palma", False),
    ("agulhas_de_cabelo", agulhas_de_cabelo, GRANDE, "Básico do Jiraiya: as agulhas de cabelo e o soco", False),
    ("soco_de_tsunade", soco_de_tsunade, GRANDE, "Básico da Tsunade: o soco que racha o chão", False),
    ("pergaminho_de_fogo", pergaminho_de_fogo, GRANDE, "Básico da Sailor Mars: o ofuda e o fogo", False),
    ("escudo_rosa", escudo_rosa, GRANDE, "Básico do Steven: o escudo com a rosa", False),
    ("manopla_de_garnet", manopla_de_garnet, GRANDE, "Básico da Garnet: as duas manoplas", False),
    ("soco_de_johnny", soco_de_johnny, GRANDE, "Básico do Johnny Bravo: o brilho e o soco", False),
    ("raio_de_dexter", raio_de_dexter, GRANDE, "Básico do Dexter: a arma de raio", False),
    ("raio_de_aku", raio_de_aku, GRANDE, "Básico do Aku: os olhos de laser", False),
]
