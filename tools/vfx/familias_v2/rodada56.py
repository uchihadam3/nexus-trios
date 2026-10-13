"""Rodada 56 das habilidades próprias: Gênio, Scar, Jack Esqueleto, Úrsula, Deku e All Might.

Gênio
- primeiro_desejo: a lâmpada, a fumaça azul subindo em espiral e as estrelinhas correndo no trio (Acelerado).
- segundo_desejo: a fumaça virando dois braços musculosos e o escudo dourado no trio (Fortalecido e Escudo).
- genio_preparo: o Preparo do Poder cósmico — a lâmpada sendo esfregada e a fumaça girando (laço).
- poder_cosmico: o punho azul gigante saindo da fumaça e as estrelas girando na cabeça do rival (Confuso).

Scar
- hienas: três hienas correndo com os olhos acesos e as risadas, e a tontura nos rivais (Confuso).
- garras_de_leao: as garras cruzando em X no rival mais ferido.
- scar_preparo: o Preparo do Longa vida ao rei — os olhos verdes no escuro e a cicatriz no olho (laço).
- longa_vida_ao_rei: a pata com as garras de fora, a coroa partindo e o rival caindo no desfiladeiro.

Jack Esqueleto
- susto: a cara de caveira pulando na frente do rival e o "BU!" (Confuso e Enfraquecido).
- fogo_de_abobora: a abóbora acesa voando e o fogo verde no rival (Queimando).
- jack_esqueleto_preparo: o Preparo da Noite das bruxas — a lua cheia, a cara de Jack e os morcegos (laço).
- noite_das_bruxas: a lua subindo, a revoada de morcegos e as abóboras sorrindo em todos os rivais (Confuso).

Úrsula
- roubar_a_voz: a concha dourada puxando a voz (a bolinha de luz e as notas) do rival (Silenciado).
- tentaculos_de_ursula: os tentáculos com ventosas subindo do chão e enrolando o rival (Preso).
- ursula_preparo: o Preparo do Tridente — o tridente brilhando e as duas moreias girando (laço).
- tridente_da_bruxa: o tridente erguido, o redemoinho e a onda gigante em todos os rivais (Enfraquecido).

Deku
- delaware_smash: o peteleco e a pressão do ar em cone até o rival; o dedo racha (o dano no próprio Deku).
- full_cowl_corpo: os raios verdes correndo pelo corpo e as linhas de velocidade (Acelerado e Fortalecido).
- deku_preparo: o Preparo do United States of Smash — o braço carregando raios verdes e as veias vermelhas (laço).
- united_states_of_smash_deku: o punho gigante com raios verdes, o tornado de ar e o braço rachando.

All Might
- texas_smash: o soco reto e a rajada de vento que empurra o rival (atrasa o Preparo).
- estou_aqui: as duas mechas, o sorriso e o sol dourado; as marcas de provocação nos rivais (Provocado e Protegido).
- allmight_preparo: o Preparo do United States of Smash — as mechas e a aura dourada do One For All (laço).
- united_states_of_smash_allmight: o punho caindo do alto, as listras e as estrelas e o tornado subindo.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CHAMA, COROA, ESCUDO, NOTA, anel, clarao, corte, estouro, icone, onda_no_chao, particulas, poe,
                         surge, estrela_pts)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


ESTRELA = estrela_pts(5, 0.45)

# a lâmpada mágica (deitada, o bico para a direita)
_LAMPADA = [(-0.9, 0.2), (-0.75, -0.1), (-0.4, -0.25), (0.0, -0.25), (0.35, -0.12), (0.7, -0.35), (1.0, -0.4), (0.8, -0.2),
            (0.5, 0.15), (0.2, 0.35), (-0.5, 0.35), (-0.85, 0.32)]
_TAMPA = [(-0.25, -0.25), (-0.15, -0.45), (0.0, -0.52), (0.15, -0.45), (0.25, -0.25)]


def _lampada(T, x, y, s, k, brilho=0.0):
    g, h = icone(T, poe(_LAMPADA, x, y, s), k * 1.2, 0.55)
    g2, h2 = icone(T, poe(_TAMPA, x, y, s), k * 1.1, 0.6)
    G = g + g2 + T.lines([(x - s * 0.6, y + s * 0.42, x + s * 0.3, y + s * 0.42, 1.0)], s * 0.05) * k
    H = h + h2 + T.gauss(x + s * 0.95, y - s * 0.4, s * 0.12) * k * brilho * 1.5
    return G, H


def _fumaca(T, x0, y0, x1, y1, t, k, w=0.05, voltas=1.5):
    """A fumaça do Gênio: uma faixa grossa em espiral subindo de (x0, y0) até (x1, y1)."""
    pts = []
    for u in np.linspace(0, 1, 40):
        r = 0.04 + 0.12 * u
        a = TAU * voltas * u + t * 6
        pts.append((x0 + (x1 - x0) * u + r * math.cos(a), y0 + (y1 - y0) * u + r * math.sin(a) * 0.5))
    G = T.polyline(pts, w) * k * 0.7 + T.polyline(pts, w * 0.35) * k * 0.9
    return G


def _hiena(T, x, y, s, k, t, olho=1.0):
    """Hiena correndo de perfil (cabeça para a direita): o corpo baixo, a juba eriçada, as orelhas e os olhos acesos."""
    passo = math.sin(t * 40) * 0.12
    corpo = [(-0.9, -0.1), (-0.5, -0.35), (0.0, -0.4), (0.35, -0.5), (0.55, -0.75), (0.65, -0.55), (0.8, -0.7), (0.82, -0.45),
             (1.1, -0.3), (1.05, -0.15), (0.7, -0.1), (0.4, 0.05), (-0.6, 0.1), (-0.95, 0.0)]
    g, h = icone(T, poe(corpo, x, y, s), k * 1.1, 0.5)
    pernas = [(x - s * 0.5, y + s * 0.05, x - s * (0.6 + passo), y + s * 0.55, 1.0), (x - s * 0.3, y + s * 0.05, x - s * (0.2 - passo), y + s * 0.55, 1.0),
              (x + s * 0.3, y, x + s * (0.4 + passo), y + s * 0.55, 1.0), (x + s * 0.5, y, x + s * (0.65 - passo), y + s * 0.55, 1.0)]
    G = g + T.lines(pernas, s * 0.07) * k * 1.1
    juba = [(x + s * (-0.4 + 0.15 * j), y - s * 0.35, x + s * (-0.45 + 0.15 * j), y - s * 0.55, 1.0) for j in range(5)]
    G += T.lines(juba, s * 0.035) * k
    H = h + T.gauss(x + s * 0.85, y - s * 0.38, s * 0.06) * k * olho * 2.0
    return G, H


def _caveira(T, x, y, s, k, boca=1.0):
    """A cara de Jack: a cabeça redonda, os olhos fundos, o nariz e o sorriso costurado de canto a canto."""
    G = T.ring(s, s * 0.06, x, y, 0.9) * k * 1.3 + T.gauss(x, y, s * 0.7, s * 0.8) * k * 0.25
    H = 0.0
    for lado in (-1, 1):
        olho = [(x + lado * s * 0.42 + s * 0.22 * math.cos(a), y - s * 0.15 + s * 0.28 * math.sin(a)) for a in np.linspace(0, TAU, 14, endpoint=False)]
        g, h = icone(T, olho, k * 1.2, 0.85)
        G, H = G + g, H + h
    G += T.lines([(x - s * 0.05, y + s * 0.15, x, y + s * 0.08, 1.0), (x, y + s * 0.08, x + s * 0.05, y + s * 0.15, 1.0)], s * 0.04) * k
    pts = [(x - s * 0.7 + s * 1.4 * u, y + s * (0.35 + 0.2 * boca * math.sin(math.pi * u))) for u in np.linspace(0, 1, 16)]
    G += T.polyline(pts, s * 0.05) * k * 1.2
    pontos = [(x - s * 0.6 + s * 1.2 * j / 6, y + s * (0.35 + 0.2 * boca * math.sin(math.pi * (0.08 + 0.84 * j / 6)))) for j in range(7)]
    G += T.lines([(px, py - s * 0.08, px, py + s * 0.08, 1.0) for px, py in pontos], s * 0.025) * k
    return G, H


def _abobora(T, x, y, s, k, fogo=1.0):
    """A abóbora de Halloween acesa por dentro: os gomos, o cabinho e a cara entalhada."""
    G = 0.0
    for d in (-0.5, 0.0, 0.5):
        G += T.ring(s * (0.55 if d else 0.6), s * 0.05, x + d * s * 0.6, y, 1.15) * k * 0.9
    G += T.lines([(x, y - s * 0.55, x + s * 0.1, y - s * 0.8, 1.0)], s * 0.08) * k * 1.2
    G += T.gauss(x, y, s * 0.6, s * 0.5) * k * 0.35 * fogo
    H = 0.0
    for lado in (-1, 1):
        g, h = icone(T, [(x + lado * s * 0.45, y - s * 0.05), (x + lado * s * 0.2, y - s * 0.05), (x + lado * s * 0.32, y - s * 0.3)], k * fogo * 1.4, 1.0)
        G, H = G + g, H + h
    boca = [(x - s * 0.5, y + s * 0.15), (x - s * 0.3, y + s * 0.3), (x - s * 0.15, y + s * 0.2), (x, y + s * 0.35), (x + s * 0.15, y + s * 0.2),
            (x + s * 0.3, y + s * 0.3), (x + s * 0.5, y + s * 0.15), (x, y + s * 0.45)]
    g, h = icone(T, boca, k * fogo * 1.4, 1.0)
    return G + g, H + h + T.gauss(x, y + s * 0.1, s * 0.25) * k * fogo


def _morcego(T, x, y, s, k, bate):
    a = 0.3 + 0.5 * bate
    pts = [(0, -0.15), (0.35, -0.35 - a * 0.4), (0.6, -0.2 - a * 0.5), (1.0, -0.4 - a * 0.3), (0.8, 0.0), (0.55, -0.05), (0.35, 0.15),
           (0.15, 0.05), (0, 0.25), (-0.15, 0.05), (-0.35, 0.15), (-0.55, -0.05), (-0.8, 0.0), (-1.0, -0.4 - a * 0.3), (-0.6, -0.2 - a * 0.5),
           (-0.35, -0.35 - a * 0.4)]
    return icone(T, poe(pts, x, y, s), k * 1.2, 0.8)


def _tentaculo(T, x0, y0, x1, y1, fase, k, w=0.045, ventosas=True):
    """Um tentáculo que ondula de (x0, y0) até a ponta (x1, y1), afinando, com as ventosas de um lado."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) + 1e-6
    nx, ny = -dy / L, dx / L
    pts = []
    for u in np.linspace(0, 1, 24):
        o = 0.08 * math.sin(math.pi * 2.2 * u + fase) * u
        pts.append((x0 + dx * u + nx * o, y0 + dy * u + ny * o))
    segs = [(a[0], a[1], b[0], b[1], 1.0 - 0.7 * i / len(pts)) for i, (a, b) in enumerate(zip(pts, pts[1:]))]
    G = T.lines(segs, w) * k * 0.8
    G += T.tapered([(pts[-1][0], pts[-1][1], pts[0][0], pts[0][1], 1.0)], w * 0.4) * k * 0.4
    H = 0.0
    if ventosas:
        sp = [(px + nx * w * 0.6, py + ny * w * 0.6, 1.0 - 0.6 * i / 24) for i, (px, py) in enumerate(pts[2:-3:2])]
        H = T.splats(sp, w * 0.22) * k * 1.4
    return G, H


def _tridente(T, x, y, s, k, ang=-math.pi / 2):
    c, sn = math.cos(ang), math.sin(ang)
    px, py = -sn, c
    hx, hy = x + c * s, y + sn * s
    G = T.lines([(x, y, hx, hy, 1.0)], s * 0.045) * k * 1.2
    segs = [(hx - px * s * 0.25, hy - py * s * 0.25, hx + px * s * 0.25, hy + py * s * 0.25, 1.0)]
    for d in (-0.25, 0.0, 0.25):
        segs.append((hx + px * s * d, hy + py * s * d, hx + px * s * d + c * s * 0.3, hy + py * s * d + sn * s * 0.3, 1.0))
    G += T.lines(segs, s * 0.04) * k * 1.3
    H = sum(T.gauss(hx + px * s * d + c * s * 0.3, hy + py * s * d + sn * s * 0.3, s * 0.04) for d in (-0.25, 0.0, 0.25)) * k * 1.5
    return G, H


def _concha(T, x, y, s, k, luz=0.0):
    """A concha dourada do colar (o caracol em espiral)."""
    pts = [(x + s * (0.15 + 0.85 * u) * math.cos(TAU * 1.6 * u), y + s * (0.15 + 0.85 * u) * math.sin(TAU * 1.6 * u)) for u in np.linspace(0, 1, 40)]
    G = T.polyline(pts, s * 0.08) * k * 1.2 + T.gauss(x, y, s * 0.8) * k * 0.25
    return G, T.gauss(x, y, s * 0.25) * k * (0.6 + 1.2 * luz)


def _mao_peteleco(T, x, y, s, k, solta):
    """A mão do Deku de lado: o punho fechado e o dedo médio dobrado preso no polegar (solta = 1 é o dedo esticado)."""
    G = T.polys([([(x - s * 0.5, y - s * 0.3), (x + s * 0.1, y - s * 0.35), (x + s * 0.2, y + s * 0.3), (x - s * 0.5, y + s * 0.3)], 1.0)], 0.004) * k * 0.6
    if solta < 1:
        G += T.ring(s * 0.16, s * 0.05, x + s * 0.3, y - s * 0.1) * k * 1.2
    else:
        G += T.lines([(x + s * 0.1, y - s * 0.15, x + s * 0.7, y - s * 0.2, 1.0)], s * 0.1) * k * 1.3
    return G


def _mechas(T, x, y, s, k):
    """As duas mechas do All Might em V."""
    G, H = 0.0, 0.0
    for lado in (-1, 1):
        pts = [(x + lado * s * 0.1, y), (x + lado * s * 0.5, y - s * 0.9), (x + lado * s * 0.25, y - s * 0.05)]
        g, h = icone(T, pts, k * 1.3, 0.7)
        G, H = G + g, H + h
    return G, H


def _listras(T, x0, y0, x1, y1, n, k, w=0.035):
    segs = []
    for j in range(n):
        o = (j - (n - 1) / 2) * w * 2.4
        segs.append((x0, y0 + o, x1, y1 + o, 1.0 if j % 2 == 0 else 0.45))
    return T.lines(segs, w) * k


# ------------------------------------------------------------------ Gênio

def primeiro_desejo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.75, 0.9))
    if k > 0:
        g, h = _lampada(T, -0.6, 0.3, 0.3, k, pulso(t, 0.05, 0.4))
        G, H = G + g, H + h
    sobe = ease_out(rel(t, 0.1, 0.45), 2)
    kf = 1 - rel(t, 0.6, 0.85)
    if sobe > 0 and kf > 0:
        G += _fumaca(T, -0.36, 0.22, -0.36 + 0.3 * sobe, 0.22 - 0.7 * sobe, t, kf, 0.06)
        H += T.gauss(-0.36 + 0.3 * sobe, 0.22 - 0.7 * sobe, 0.06) * kf * 1.2
    # o "1" de luz no alto da fumaça
    m = pulso(t, 0.35, 0.6)
    if m > 0:
        H += T.lines([(-0.06, -0.62, -0.06, -0.38, 1.0), (-0.12, -0.56, -0.06, -0.62, 1.0)], 0.018) * m * 1.6
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        u = rel(t, 0.45 + 0.05 * i, 0.85 + 0.05 * i)
        if 0 < u < 1:
            for j in range(3):
                y = 0.15 - 0.18 * j
                G += T.tapered([(cx - 0.35 + 0.5 * u, y, cx - 0.1 + 0.5 * u, y, 0.9)], 0.02) * (1 - u) * 1.2
            g, h = icone(T, poe(ESTRELA, cx + 0.1 * u, -0.25 - 0.2 * u, 0.06 * (1 - u) + 0.02, t * 6), (1 - u) * 1.3, 0.8)
            G, H = G + g, H + h
    G += particulas(T, t, 0.4, 1.0, 16, 561, 0.0, -0.1, 0.6, 0.4, 0.012)
    return G * env, H * env


def segundo_desejo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.7, 0.85))
    if k > 0:
        g, h = _lampada(T, -0.6, 0.3, 0.3, k, pulso(t, 0.05, 0.4))
        G, H = G + g, H + h
    sobe = ease_out(rel(t, 0.1, 0.4), 2)
    kf = 1 - rel(t, 0.55, 0.8)
    if sobe > 0 and kf > 0:
        G += _fumaca(T, -0.36, 0.22, -0.2, 0.22 - 0.55 * sobe, t, kf, 0.07)
        # os dois braços azuis dobrados (o "bíceps" do desejo)
        for lado in (-1, 1):
            bx, by = -0.2 + lado * 0.25 * sobe, -0.33
            P, nos = _punho(T, bx + lado * 0.1, by - 0.2 * sobe, 1.3 * sobe + 0.01, -lado * 1.2)
            G += P * kf * 0.9
            G += T.lines([(-0.2, -0.3, bx, by, 1.0), (bx, by, bx + lado * 0.1, by - 0.2 * sobe, 1.0)], 0.04) * kf * sobe
    m = pulso(t, 0.3, 0.55)
    if m > 0:
        H += T.lines([(-0.24, -0.72, -0.24, -0.5, 1.0), (-0.16, -0.72, -0.16, -0.5, 1.0)], 0.018) * m * 1.6
    e = surge(t, 0.4, 0.62) * (1 - rel(t, 0.85, 1))
    if e > 0:
        for cx in (-0.45, 0.0, 0.45):
            g, h = icone(T, poe(ESCUDO, cx, 0.0, 0.18 * e), 1.1, 0.4)
            G, H = G + g, H + h
            G += T.ring(0.28 * e, 0.014, cx, 0.0) * 0.9
            H += T.flare(cx, -0.1, 0.12 * e + 0.01, 0.3, 0.012) * pulso(t, 0.42, 0.7)
    G += anel(T, t, 0.42, 0.85, 0.1, 0.9, 0.03, 0.05, 2.5, 1.3)
    G += particulas(T, t, 0.45, 1.0, 18, 562, 0.0, 0.0, 0.65, 0.35, 0.012)
    return G * env, H * env


def genio_preparo(T, t, rng):
    G, H = vazio(T)
    esfrega = math.sin(t * TAU * 3)
    g, h = _lampada(T, -0.1, 0.25, 0.28, 1.0, 0.6 + 0.4 * abs(esfrega))
    G, H = G + g, H + h
    # a mão esfregando a lâmpada
    G += T.gauss(-0.15 + 0.15 * esfrega, 0.05, 0.07, 0.04) * 0.9
    G += _fumaca(T, 0.17, 0.13, 0.25, -0.5, t, 0.8, 0.05, 2.0)
    for j in range(4):
        a = TAU * j / 4 + t * TAU
        g, h = icone(T, poe(ESTRELA, 0.25 + 0.3 * math.cos(a), -0.45 + 0.12 * math.sin(a), 0.045, a), 1.0, 0.8)
        G, H = G + g, H + h
    return G, H


def poder_cosmico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    k = 1 - rel(t, 0.6, 0.75)
    G += _fumaca(T, -0.7, 0.2, -0.45, -0.1, t, k * pulso(t, 0.0, 0.7), 0.08, 1.2)
    u = ease_in(rel(t, 0.12, 0.35), 2.2)
    if u > 0 and k > 0:
        x = -0.45 + 0.75 * u
        P, nos = _punho(T, x, -0.05, 3.0, 0)
        G += P * k * 1.1
        H += nos * 0.6 * k
        G += T.tapered([(-0.9, -0.05, x - 0.2, -0.05, 1.0)], 0.16) * k * 0.6
        for j in range(5):
            a = TAU * j / 5 + t * 8
            g, h = icone(T, poe(ESTRELA, x - 0.25 + 0.12 * math.cos(a), -0.05 + 0.15 * math.sin(a), 0.035, a), k, 0.8)
            G, H = G + g, H + h
    g, h = clarao(T, t, 0.33, 0.58, 0.45, -0.05, 1.8, 1.6)
    G, H = G + g, H + h
    G += anel(T, t, 0.34, 0.75, 0.05, 0.8, 0.05, -0.05, 1.0, 1.5)
    G += estouro(T, t, 0.34, 0.85, 18, 563, 0.45, -0.05, 0.7, 0.015)
    c = pulso(t, 0.5, 1.0)
    if c > 0:
        for j in range(4):
            a = TAU * j / 4 + t * 10
            g, h = icone(T, poe(ESTRELA, 0.45 + 0.17 * math.cos(a), -0.45 + 0.06 * math.sin(a), 0.05, a), c * 1.2, 0.9)
            G, H = G + g, H + h
        G += T.ring(0.17, 0.01, 0.45, -0.45, 2.6) * c * 0.8
    return G * env, H * env


# ------------------------------------------------------------------ Scar

def hienas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(3):
        u = ease_in(rel(t, 0.0 + 0.08 * j, 0.55 + 0.08 * j), 1.3)
        if 0 < u < 1:
            x, y = -1.0 + 1.75 * u, 0.28 - 0.28 * j + 0.03 * math.sin(t * 40 + j)
            g, h = _hiena(T, x, y, 0.21, 1 - rel(u, 0.85, 1), t + j)
            G, H = G + g, H + h
            G += T.lines([(x - 0.3 - 0.1 * q, y - 0.05 + 0.05 * q, x - 0.15 - 0.1 * q, y - 0.05 + 0.05 * q, 0.7) for q in range(2)], 0.008) * (1 - u)
            # a risada ("ha ha"): pulinhos de luz saindo da boca
            for q in range(2):
                r = (t * 3 + q / 2 + j / 3) % 1
                H += T.gauss(x + 0.15 + 0.1 * r, y - 0.12 - 0.15 * r, 0.012) * (1 - r) * 1.5
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = clarao(T, t, 0.5 + 0.04 * i, 0.68 + 0.04 * i, cx + 0.1, 0.0, 0.6, 0.9)
        G, H = G + g, H + h
        c = pulso(t, 0.55, 1.0)
        if c > 0:
            pts = [(cx + 0.03 * u2 * 5 * math.cos(-t * 10 + u2 * 9) * 0.2 + 0.12 * u2 * math.cos(-t * 10 + u2 * 9), -0.35 + 0.06 * u2 * math.sin(-t * 10 + u2 * 9))
                   for u2 in np.linspace(0.05, 1, 26)]
            G += T.polyline(pts, 0.012) * c * 1.3
    return G * env, H * env


def garras_de_leao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for i, ang in enumerate((0.75, 2.4)):
        a0 = 0.08 + 0.18 * i
        for j in range(3):
            o = (j - 1) * 0.09
            g, h = corte(T, t, a0 + 0.02 * j, a0 + 0.3 + 0.02 * j, ang, 0.85, 0.04, 0.45 + o * math.sin(ang), 0.0 - o * math.cos(ang), 0.06)
            G, H = G + g, H + h
        g, h = clarao(T, t, a0 + 0.08, a0 + 0.3, 0.45, 0.0, 0.9, 1.0)
        G, H = G + g, H + h
    marca = pulso(t, 0.4, 1.0)
    if marca > 0:
        for ang in (0.75, 2.4):
            for j in range(3):
                o = (j - 1) * 0.09
                c, s = math.cos(ang), math.sin(ang)
                cx, cy = 0.45 + o * s, -o * c
                G += T.lines([(cx - c * 0.3, cy - s * 0.3, cx + c * 0.3, cy + s * 0.3, 1.0)], 0.01) * marca * 0.9
    G += estouro(T, t, 0.3, 0.75, 12, 564, 0.45, 0.0, 0.5, 0.012)
    return G * env, H * env


def scar_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.gauss(0.0, -0.05, 0.4, 0.3) * 0.25
    pisca = 1.0 if (t * 2) % 1 > 0.08 else 0.1
    for lado in (-1, 1):
        olho = [(lado * 0.17 + 0.11 * math.cos(a), -0.1 + 0.045 * math.sin(a) - 0.02 * lado * math.cos(a)) for a in np.linspace(0, TAU, 16, endpoint=False)]
        g, h = icone(T, olho, pisca * 1.4, 0.9)
        G, H = G + g, H + h
        H += T.lines([(lado * 0.17, -0.14, lado * 0.17, -0.06, 1.0)], 0.01) * pisca * 1.2
    # a cicatriz cortando o olho esquerdo
    G += T.lines([(-0.12, -0.3, -0.22, 0.08, 1.0)], 0.014) * 1.3
    # a juba escura em volta
    G += T.arc_band(0.38, 0.05, math.pi * 1.05, math.pi * 1.95, 1.0, 0, 0.0, 0.05, 0.0) * (0.8 + 0.2 * math.sin(t * TAU))
    return G, H


def longa_vida_ao_rei(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    # a coroa sobre o rival, que parte ao meio
    k = surge(t, 0.0, 0.2)
    parte = ease_out(rel(t, 0.4, 0.7), 2)
    kc = k * (1 - rel(t, 0.7, 0.85))
    if kc > 0:
        for lado in (-1, 1):
            meia = [(px, py) for px, py in COROA if (px <= 0.05 if lado < 0 else px >= -0.05)]
            g, h = icone(T, poe(meia, 0.45 + lado * 0.12 * parte, -0.5 + 0.25 * parte, 0.24, lado * 0.5 * parte), kc * 1.2, 0.6)
            G, H = G + g, H + h
    # a pata descendo com as garras de fora
    u = ease_in(rel(t, 0.15, 0.4), 2)
    kp = 1 - rel(t, 0.55, 0.65)
    if u > 0 and kp > 0:
        x, y = 0.05 + 0.3 * u, -0.6 + 0.55 * u
        G += T.gauss(x, y, 0.13, 0.1) * kp * 0.8
        for j in range(4):
            gx = x - 0.12 + 0.08 * j
            G += T.tapered([(gx, y + 0.02, gx + 0.04, y + 0.16, 1.0)], 0.018) * kp * 1.4
    for j in range(3):
        g, h = corte(T, t, 0.38 + 0.02 * j, 0.62 + 0.02 * j, 1.2, 1.0, 0.06, 0.45 + 0.1 * (j - 1), 0.0, 0.05)
        G, H = G + g, H + h
    g, h = clarao(T, t, 0.38, 0.62, 0.45, 0.0, 1.6, 1.5)
    G, H = G + g, H + h
    # o rival caindo (o rastro descendo) e a poeira do desfiladeiro
    q = rel(t, 0.55, 0.9)
    if 0 < q < 1:
        G += T.tapered([(0.45, 0.0, 0.45, 0.1 + 0.6 * ease_in(q), 1.0)], 0.06) * (1 - q) * 1.0
    G += onda_no_chao(T, t, 0.6, 1.0, 0.8, 0.4, 1.3)
    G += particulas(T, t, 0.6, 1.0, 20, 565, 0.45, 0.4, 0.4, 0.4, 0.016)
    return G * env, H * env


# ------------------------------------------------------------------ Jack Esqueleto

def susto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.12, 0.3) * (1 - rel(t, 0.6, 0.75))
    if s > 0:
        g, h = _caveira(T, 0.35, -0.05, 0.25 * s, 1.0, 1.0 + 0.3 * math.sin(t * 30))
        G, H = G + g, H + h
    # o "BU!": as ondas do grito
    for j in range(3):
        u = rel(t, 0.25 + 0.06 * j, 0.6 + 0.06 * j)
        if 0 < u < 1:
            G += T.arc_band(0.15 + 0.45 * u, 0.03 * (1 - 0.5 * u), -0.7, 0.7, 1.0, 0, 0.35, -0.05, 0.0) * (1 - u) * 1.3
    G += T.tapered([(0.1, -0.05, -0.3, -0.05, 0.0)], 0.02) * pulso(t, 0.0, 0.2)
    g, h = clarao(T, t, 0.25, 0.45, 0.5, -0.05, 0.9, 1.0)
    G, H = G + g, H + h
    c = pulso(t, 0.55, 1.0)
    if c > 0:
        pts = [(0.5 + 0.13 * u2 * math.cos(-t * 9 + u2 * 9), -0.45 + 0.06 * u2 * math.sin(-t * 9 + u2 * 9)) for u2 in np.linspace(0.05, 1, 28)]
        G += T.polyline(pts, 0.014) * c * 1.4
        # o rival encolhendo (Enfraquecido): a seta para baixo
        G += T.lines([(0.75, -0.25, 0.75, 0.0, 1.0), (0.7, -0.06, 0.75, 0.0, 1.0), (0.8, -0.06, 0.75, 0.0, 1.0)], 0.014) * c * 1.2
    return G * env, H * env


def fogo_de_abobora(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.05, 0.4)
    if 0 < u < 1:
        e = ease_in(u, 1.4)
        x, y = -0.5 + 0.95 * e, -0.05 - 0.25 * math.sin(math.pi * e)
        g, h = _abobora(T, x, y, 0.22, 1.0, 0.8 + 0.2 * math.sin(t * 40))
        G, H = G + g, H + h
        for j in range(4):
            r = j / 4
            ex = -0.5 + 0.95 * max(0, e - 0.08 * (j + 1))
            ey = -0.05 - 0.25 * math.sin(math.pi * max(0, e - 0.08 * (j + 1)))
            g2, h2 = icone(T, poe(CHAMA, ex, ey, 0.06 * (1 - r), -math.pi / 2), (1 - r) * 0.9, 0.7)
            G, H = G + g2, H + h2
    g, h = clarao(T, t, 0.38, 0.6, 0.45, -0.05, 1.4, 1.4)
    G, H = G + g, H + h
    G += estouro(T, t, 0.38, 0.8, 14, 566, 0.45, -0.05, 0.55, 0.014)
    q = pulso(t, 0.45, 1.0)
    if q > 0:
        for j in range(4):
            fx = 0.3 + 0.1 * j
            g, h = icone(T, poe(CHAMA, fx, 0.15 - 0.05 * (j % 2), 0.08 + 0.02 * math.sin(t * 25 + j)), q * 1.1, 0.6)
            G, H = G + g, H + h
    G += particulas(T, t, 0.4, 1.0, 14, 567, 0.45, 0.0, 0.25, 0.5, 0.012)
    return G * env, H * env


def jack_esqueleto_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.ring(0.38, 0.02, 0.0, -0.05) * 0.7 + T.gauss(0.0, -0.05, 0.36) * 0.25
    g, h = _caveira(T, 0.0, -0.05, 0.2, 1.0, 1.0 + 0.2 * math.sin(t * TAU * 2))
    G, H = G + g, H + h
    for j in range(3):
        a = TAU * j / 3 + t * TAU
        g, h = _morcego(T, 0.5 * math.cos(a), -0.05 + 0.25 * math.sin(a), 0.07, 1.0, abs(math.sin(t * TAU * 4 + j)))
        G, H = G + g, H + h
    return G, H


def noite_das_bruxas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    lua = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.8, 0.95))
    if lua > 0:
        G += T.gauss(-0.55, -0.55 + 0.1 * (1 - lua), 0.17) * lua * 0.9 + T.ring(0.17, 0.012, -0.55, -0.55 + 0.1 * (1 - lua)) * lua
        g, h = _caveira(T, -0.55, -0.55 + 0.1 * (1 - lua), 0.1, lua * 0.8)
        G, H = G + g, H + h
    q = np.random.default_rng(568)
    for j in range(10):
        atraso, y0, vel = q.uniform(0, 0.3), q.uniform(-0.6, 0.15), q.uniform(0.9, 1.2)
        u = rel(t, 0.2 + atraso, 0.75 + atraso)
        if 0 < u < 1:
            x = -0.9 + 1.8 * ease_in(u, 1.2) * vel
            g, h = _morcego(T, x, y0 + 0.08 * math.sin(u * 12 + j), 0.06, 1 - rel(u, 0.8, 1), abs(math.sin(t * 30 + j)))
            G, H = G + g, H + h
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        s = surge(t, 0.45 + 0.05 * i, 0.65 + 0.05 * i) * (1 - rel(t, 0.85, 0.97))
        if s > 0:
            g, h = _abobora(T, cx + 0.05, 0.25, 0.1 * s, 1.0, 1.0)
            G, H = G + g, H + h
        g, h = clarao(T, t, 0.5 + 0.05 * i, 0.68 + 0.05 * i, cx, 0.0, 0.7, 0.9)
        G, H = G + g, H + h
        c = pulso(t, 0.6, 1.0)
        if c > 0:
            pts = [(cx + 0.11 * u2 * math.cos(-t * 9 + u2 * 9 + i), -0.35 + 0.05 * u2 * math.sin(-t * 9 + u2 * 9 + i)) for u2 in np.linspace(0.05, 1, 24)]
            G += T.polyline(pts, 0.012) * c * 1.3
    return G * env, H * env


# ------------------------------------------------------------------ Úrsula

def roubar_a_voz(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.2) * (1 - rel(t, 0.85, 0.97))
    puxa = rel(t, 0.3, 0.75)
    if k > 0:
        g, h = _concha(T, -0.55, -0.1, 0.22, k, pulso(t, 0.65, 0.95))
        G, H = G + g, H + h
    # a mão de Úrsula (o gesto) puxando: os fios de luz do rival até a concha
    fio = pulso(t, 0.15, 0.8)
    if fio > 0:
        pts = [(0.45 - 0.95 * u, -0.15 - 0.15 * math.sin(math.pi * u) + 0.02 * math.sin(u * 20 + t * 20)) for u in np.linspace(0, 1, 30)]
        G += T.polyline(pts, 0.012) * fio * 1.0
    if 0 < puxa < 1:
        e = ease_in(puxa, 1.5)
        x, y = 0.45 - 0.95 * e, -0.15 - 0.15 * math.sin(math.pi * e)
        G += T.gauss(x, y, 0.05) * 1.2
        H += T.gauss(x, y, 0.02) * 2.0
        for j in range(3):
            r = ((t * 2.5) + j / 3) % 1
            g, h = icone(T, poe(NOTA, x + 0.12 + 0.12 * r, y - 0.08 - 0.1 * r + 0.04 * j, 0.1 * (1 - 0.5 * r)), (1 - r) * 1.2, 0.8)
            G, H = G + g, H + h
    # o rival sem voz: a boca riscada (Silenciado)
    m = pulso(t, 0.6, 1.0)
    if m > 0:
        G += T.ring(0.09, 0.012, 0.45, -0.35) * m * 1.2
        G += T.lines([(0.38, -0.42, 0.52, -0.28, 1.0)], 0.014) * m * 1.3
    G += particulas(T, t, 0.65, 1.0, 12, 569, -0.5, -0.1, 0.12, 0.3, 0.01)
    return G * env, H * env


def tentaculos_de_ursula(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    G += onda_no_chao(T, t, 0.0, 0.4, 0.5, 0.38, 1.2)
    sobe = ease_out(rel(t, 0.08, 0.45), 2)
    k = 1 - rel(t, 0.85, 0.97)
    if sobe > 0 and k > 0:
        for j, (bx, ang0) in enumerate(((0.15, -1.1), (0.75, -2.0), (0.3, -1.4), (0.62, -1.75))):
            topo = 0.38 - 0.7 * sobe
            # a ponta se enrola no rival (x 0.45) depois de subir
            enrola = rel(t, 0.4, 0.7)
            tx = bx + (0.45 - bx) * enrola + 0.12 * math.cos(t * 5 + j) * enrola
            g, h = _tentaculo(T, bx, 0.38, tx, topo + 0.1 * j * (1 - enrola), t * 4 + j, k, 0.04 - 0.004 * j)
            G, H = G + g, H + h
    m = pulso(t, 0.5, 1.0)
    if m > 0:
        G += T.ring(0.2, 0.025, 0.45, -0.05, 2.2) * m * 1.0 + T.ring(0.2, 0.025, 0.45, -0.25, 2.2) * m * 0.8
    g, h = clarao(T, t, 0.42, 0.62, 0.45, -0.1, 0.8, 0.9)
    G, H = G + g, H + h
    return G * env, H * env


def ursula_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _tridente(T, 0.0, 0.45, 0.8, 1.0 + 0.2 * math.sin(t * TAU * 2))
    G, H = G + g, H + h
    G += T.gauss(0.0, -0.45, 0.2) * 0.4
    for j in range(2):
        a0 = t * TAU + math.pi * j
        pts = [(0.3 * math.cos(a0 - u * 2.2), -0.05 + 0.3 * math.sin(a0 - u * 2.2) * 0.6 + 0.02 * math.sin(u * 25)) for u in np.linspace(0, 1, 24)]
        segs = [(a[0], a[1], b[0], b[1], 1.0 - 0.8 * i / 24) for i, (a, b) in enumerate(zip(pts, pts[1:]))]
        G += T.lines(segs, 0.022) * 1.1
        H += T.gauss(pts[0][0], pts[0][1], 0.015) * 1.8
    return G, H


def tridente_da_bruxa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    k = surge(t, 0.0, 0.25) * (1 - rel(t, 0.6, 0.75))
    if k > 0:
        g, h = _tridente(T, -0.55, 0.3, 0.75, k)
        G, H = G + g, H + h
    # o redemoinho em volta da ponta
    r = pulso(t, 0.1, 0.55)
    if r > 0:
        for j in range(3):
            G += T.arc_band(0.12 + 0.07 * j, 0.02, t * 10 + j, t * 10 + j + 3.5, 0.5, 0, -0.55, -0.5, 1.0) * r * 1.2
    # a onda gigante varrendo todos os rivais
    u = rel(t, 0.35, 0.8)
    if 0 < u < 1:
        x = -0.6 + 1.5 * ease_out(u, 1.5)
        crista = [(x - 0.6 + 0.6 * v, 0.38 - 0.55 * math.sin(math.pi * v * 0.85) * (1 - 0.3 * u)) for v in np.linspace(0, 1, 30)]
        G += T.polyline(crista, 0.05) * (1 - u) * 1.2
        G += T.polys([(crista + [(x, 0.4), (x - 0.6, 0.4)], 1.0)], 0.01) * (1 - u) * 0.35
        for j in range(5):
            H += T.gauss(crista[-3 - 3 * j][0], crista[-3 - 3 * j][1] - 0.03, 0.015) * (1 - u) * 1.4
    for i, cx in enumerate((-0.45, 0.0, 0.45)):
        g, h = clarao(T, t, 0.5 + 0.06 * i, 0.7 + 0.06 * i, cx, 0.0, 0.7, 0.9)
        G, H = G + g, H + h
        m = pulso(t, 0.6, 1.0)
        if m > 0:
            G += T.lines([(cx + 0.15, -0.3, cx + 0.15, -0.1, 1.0), (cx + 0.1, -0.16, cx + 0.15, -0.1, 1.0), (cx + 0.2, -0.16, cx + 0.15, -0.1, 1.0)], 0.012) * m * 1.2
    G += particulas(T, t, 0.5, 1.0, 22, 570, 0.2, 0.2, 0.7, 0.5, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Deku

def delaware_smash(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = surge(t, 0.0, 0.15) * (1 - rel(t, 0.6, 0.75))
    solta = 1.0 if t > 0.2 else 0.0
    if k > 0:
        G += _mao_peteleco(T, -0.65, -0.05, 0.4, k, solta)
        G += T.gauss(-0.55, -0.07, 0.12) * pulso(t, 0.0, 0.25) * 0.8
        # os raios verdes no dedo antes do peteleco
        G += _zap(T, 571 + int(t * 30), -0.6, -0.1, -0.45, -0.1, 0.008, 3, 0.4) * pulso(t, 0.0, 0.22) * 1.3
    # a pressão do ar em cone
    for j in range(5):
        u = rel(t, 0.2 + 0.03 * j, 0.55 + 0.03 * j)
        if 0 < u < 1:
            x = -0.4 + 0.85 * ease_out(u, 1.5)
            G += T.arc_band(0.08 + 0.25 * u, 0.025 * (1 - 0.4 * u), -0.8, 0.8, 0.7, 0, x - 0.1 - 0.25 * u, -0.05, 0.0) * (1 - u) * 1.3
    G += T.tapered([(-0.4, -0.05, 0.4, -0.05, 1.0)], 0.08) * pulso(t, 0.2, 0.45) * 0.6
    g, h = clarao(T, t, 0.35, 0.55, 0.45, -0.05, 1.3, 1.3)
    G, H = G + g, H + h
    G += estouro(T, t, 0.36, 0.8, 14, 572, 0.45, -0.05, 0.55, 0.013)
    # o dedo do Deku rachando (o dano em si mesmo)
    r = pulso(t, 0.35, 0.9)
    if r > 0:
        for j in range(3):
            G += _zap(T, 573 + j, -0.38, -0.27, -0.38 + 0.06 * (j - 1), -0.15, 0.007, 3, 0.4) * r * 1.2
        H += T.gauss(-0.38, -0.25, 0.02) * r * 1.2
    return G * env, H * env


def full_cowl_corpo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 1.0)
    G += T.gauss(0.0, 0.0, 0.22, 0.38) * k * 0.4
    q = np.random.default_rng(574 + int(t * 30))
    for _ in range(6):
        x0, y0 = q.uniform(-0.15, 0.15), q.uniform(-0.4, 0.35)
        G += T.polyline(jagged(q, x0, y0, x0 + q.uniform(-0.18, 0.18), y0 + q.uniform(-0.18, 0.18), 3, 0.4), 0.009) * k * 1.4
    # as veias de luz (o padrão do Full Cowl)
    for lado in (-1, 1):
        pts = [(lado * (0.05 + 0.06 * math.sin(u * 7)), -0.38 + 0.75 * u) for u in np.linspace(0, 1, 20)]
        H += T.polyline(pts, 0.006) * k * 1.1
    G += anel(T, t, 0.0, 0.45, 0.1, 0.6, 0.03, 0.0, 1.0, 1.2)
    # as linhas de velocidade (Acelerado)
    v = pulso(t, 0.3, 1.0)
    if v > 0:
        for j in range(5):
            y = -0.35 + 0.17 * j
            o = ((t * 3) + j * 0.37) % 1
            G += T.tapered([(-0.8 + 0.4 * o, y, -0.35 + 0.4 * o, y, 0.8)], 0.015) * v * 1.1
    G += particulas(T, t, 0.1, 1.0, 16, 575, 0.0, 0.1, 0.25, 0.6, 0.011)
    return G * env, H * env


def deku_preparo(T, t, rng):
    G, H = vazio(T)
    P, nos = _punho(T, 0.15, -0.1, 2.0, -0.4)
    G += P * (0.8 + 0.2 * math.sin(t * TAU * 3))
    H += nos * 0.6
    G += T.lines([(-0.45, 0.25, 0.05, 0.0, 1.0)], 0.05) * 0.8
    q = np.random.default_rng(576 + int(t * 20))
    for _ in range(4):
        x0 = q.uniform(-0.4, 0.15)
        y0 = 0.25 - 0.5 * (x0 + 0.45) * 0.5
        G += T.polyline(jagged(q, x0, y0, x0 + q.uniform(0.05, 0.15), y0 + q.uniform(-0.15, 0.15), 3, 0.4), 0.008) * 1.4
    # as veias vermelhas: o brilho no braço que vai rachar
    H += T.lines([(-0.35, 0.2, -0.15, 0.1, 1.0), (-0.15, 0.1, 0.0, 0.05, 1.0)], 0.006) * (0.6 + 0.4 * math.sin(t * TAU * 2))
    return G, H


def united_states_of_smash_deku(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    u = ease_in(rel(t, 0.08, 0.35), 2.3)
    k = 1 - rel(t, 0.55, 0.68)
    if u > 0 and k > 0:
        x = -0.55 + 0.85 * u
        P, nos = _punho(T, x, -0.05, 3.6, 0)
        G += P * k
        H += nos * 0.6 * k
        q = np.random.default_rng(577 + int(t * 30))
        for _ in range(5):
            G += T.polyline(jagged(q, x - 0.2, -0.05 + q.uniform(-0.15, 0.15), x + 0.15, -0.05 + q.uniform(-0.25, 0.25), 3, 0.4), 0.01) * k * 1.4
        G += T.tapered([(-1.0, -0.05, x - 0.25, -0.05, 1.0)], 0.15) * k * 0.6
    g, h = clarao(T, t, 0.33, 0.6, 0.45, -0.05, 2.0, 1.8)
    G, H = G + g, H + h
    for j in range(3):
        G += anel(T, t, 0.34 + 0.06 * j, 0.85 + 0.04 * j, 0.05, 0.9 - 0.15 * j, 0.05, -0.05, 1.0, 1.5)
    # o tornado de ar subindo depois do soco
    w = pulso(t, 0.4, 1.0)
    if w > 0:
        for j in range(6):
            y = 0.35 - 0.15 * j
            G += T.arc_band(0.08 + 0.04 * j, 0.022, t * 12 + j, t * 12 + j + 4.0, 0.35, 0, 0.45, y, 1.0) * w * 1.2
    G += estouro(T, t, 0.34, 0.85, 20, 578, 0.45, -0.05, 0.75, 0.016)
    # o braço do Deku rachando
    r = pulso(t, 0.4, 0.95)
    if r > 0:
        for j in range(4):
            G += _zap(T, 579 + j, -0.62, -0.1 + 0.05 * j, -0.42, -0.12 + 0.07 * j, 0.008, 3, 0.5) * r * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ All Might

def texas_smash(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.25), 2)
    k = 1 - rel(t, 0.45, 0.55)
    if u > 0 and k > 0:
        P, nos = _punho(T, -0.55 + 0.35 * u, -0.05, 2.2, 0)
        G += P * k
        H += nos * 0.5 * k
    # a rajada de vento reta (os rastros em espiral horizontal)
    v = rel(t, 0.2, 0.6)
    if 0 < v < 1:
        for j in range(4):
            y = -0.05 + 0.06 * math.sin(v * 20 + j * 1.6)
            G += T.tapered([(-0.3, -0.05, -0.3 + 0.95 * ease_out(v), y, 0.9)], 0.03 + 0.01 * j) * (1 - v) * 1.0
    G += T.tapered([(-0.3, -0.05, 0.6, -0.05, 1.0)], 0.12) * pulso(t, 0.2, 0.45) * 0.5
    g, h = clarao(T, t, 0.3, 0.5, 0.45, -0.05, 1.2, 1.2)
    G, H = G + g, H + h
    # o rival empurrado para trás (o Preparo atrasado)
    e = rel(t, 0.35, 0.7)
    if 0 < e < 1:
        G += T.arc_band(0.2, 0.025, -0.9, 0.9, 1.0, 0, 0.45 + 0.25 * e, -0.05, 0.0) * (1 - e) * 1.3
        G += T.lines([(0.55 + 0.2 * e + 0.1 * j, -0.2 + 0.15 * j, 0.7 + 0.2 * e + 0.1 * j, -0.2 + 0.15 * j, 0.7) for j in range(3)], 0.01) * (1 - e)
    G += estouro(T, t, 0.3, 0.7, 12, 580, 0.45, -0.05, 0.45, 0.012)
    return G * env, H * env


def estou_aqui(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.8, 0.95))
    if s > 0:
        g, h = _mechas(T, -0.55, -0.25, 0.3 * s, 1.0)
        G, H = G + g, H + h
        # o sorriso largo
        pts = [(-0.55 - 0.12 + 0.24 * u, -0.1 + 0.05 * math.sin(math.pi * u)) for u in np.linspace(0, 1, 12)]
        G += T.polyline(pts, 0.012) * s * 1.3
        H += T.lines([(-0.62 + 0.04 * j, -0.09, -0.62 + 0.04 * j, -0.06, 1.0) for j in range(5)], 0.004) * s
    # o sol dourado atrás dele
    sol = pulso(t, 0.1, 0.8)
    if sol > 0:
        segs = [(-0.55 + 0.2 * math.cos(a), -0.15 + 0.2 * math.sin(a), -0.55 + 0.45 * math.cos(a), -0.15 + 0.45 * math.sin(a), 0.8) for a in np.linspace(0, TAU, 16, endpoint=False)]
        G += T.tapered(segs, 0.025) * sol * 0.8
        G += T.gauss(-0.55, -0.15, 0.25) * sol * 0.4
    g, h = clarao(T, t, 0.15, 0.4, -0.55, -0.2, 1.0, 1.0)
    G, H = G + g, H + h
    # o escudo dele (Protegido)
    p = surge(t, 0.35, 0.55) * (1 - rel(t, 0.85, 1))
    if p > 0:
        G += T.ring(0.33 * p, 0.018, -0.55, -0.05, 0.9) * 1.2
    # a provocação nos rivais: os "!" vermelhos e as setas apontando para ele
    for i, cx in enumerate((-0.05, 0.25, 0.55)):
        m = surge(t, 0.4 + 0.05 * i, 0.58 + 0.05 * i) * (1 - rel(t, 0.85, 1))
        if m > 0:
            G += T.lines([(cx, -0.5, cx, -0.36, 1.0)], 0.022 * m) * 1.3
            H += T.gauss(cx, -0.3, 0.015) * m * 1.8
            G += T.tapered([(cx + 0.05, -0.05, cx - 0.15, -0.05, 0.8)], 0.02) * m * 0.8
    G += anel(T, t, 0.15, 0.6, 0.1, 0.9, 0.035, -0.15, 1.0, 1.3)
    return G * env, H * env


def allmight_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _mechas(T, 0.0, -0.15, 0.3, 1.0 + 0.2 * math.sin(t * TAU * 2))
    G, H = G + g, H + h
    G += T.gauss(0.0, 0.0, 0.3, 0.4) * (0.4 + 0.15 * math.sin(t * TAU * 3))
    for j in range(6):
        a = TAU * j / 6 + t * TAU
        g, h = icone(T, poe(CHAMA, 0.32 * math.cos(a), 0.05 + 0.32 * math.sin(a) * 0.6, 0.06, 0), 0.9, 0.6)
        G, H = G + g, H + h
    return G, H


def united_states_of_smash_allmight(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.93, 1)
    # as listras e as estrelas atrás dele (a bandeira em luz)
    b = pulso(t, 0.0, 0.5)
    if b > 0:
        G += _listras(T, -0.9, -0.35, -0.1, -0.35, 5, b * 0.7, 0.03)
        for j in range(3):
            g, h = icone(T, poe(ESTRELA, -0.8 + 0.12 * j, -0.62, 0.04), b, 0.9)
            G, H = G + g, H + h
    # o punho caindo do alto em diagonal
    u = ease_in(rel(t, 0.1, 0.38), 2.3)
    k = 1 - rel(t, 0.55, 0.68)
    if u > 0 and k > 0:
        x, y = -0.2 + 0.65 * u, -0.85 + 0.85 * u
        P, nos = _punho(T, x, y, 3.6, 0.9)
        G += P * k
        H += nos * 0.6 * k
        G += T.tapered([(-0.6, -1.0, x - 0.1, y - 0.15, 1.0)], 0.16) * k * 0.6
    g, h = clarao(T, t, 0.36, 0.62, 0.45, 0.0, 2.1, 1.9)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.37, 0.95, 1.0, 0.38, 1.8)
    G += anel(T, t, 0.37, 0.85, 0.05, 0.85, 0.05, 0.0, 1.0, 1.5)
    # o tornado subindo do chão (o ar que sobe depois do soco)
    w = pulso(t, 0.45, 1.0)
    if w > 0:
        for j in range(7):
            y = 0.35 - 0.16 * j
            G += T.arc_band(0.1 + 0.05 * j, 0.024, -t * 12 + j, -t * 12 + j + 4.0, 0.35, 0, 0.45, y, 1.0) * w * 1.2
    G += estouro(T, t, 0.37, 0.85, 22, 581, 0.45, 0.0, 0.8, 0.016)
    G += particulas(T, t, 0.45, 1.0, 24, 582, 0.45, 0.3, 0.5, 0.9, 0.013)
    return G * env, H * env


REGISTRO = [
    ("primeiro_desejo", primeiro_desejo, GRANDE, "Gênio · a lâmpada e a fumaça correndo no trio", False),
    ("segundo_desejo", segundo_desejo, GRANDE, "Gênio · os braços de fumaça e os escudos", False),
    ("genio_preparo", genio_preparo, MEDIA, "Gênio · a lâmpada sendo esfregada (Preparo, laço)", True),
    ("poder_cosmico", poder_cosmico, GRANDE, "Gênio · o punho azul gigante e as estrelas", False),
    ("hienas", hienas, GRANDE, "Scar · as três hienas correndo", False),
    ("garras_de_leao", garras_de_leao, GRANDE, "Scar · as garras em X", False),
    ("scar_preparo", scar_preparo, MEDIA, "Scar · os olhos verdes e a cicatriz (Preparo, laço)", True),
    ("longa_vida_ao_rei", longa_vida_ao_rei, GRANDE, "Scar · a pata, a coroa partida e a queda", False),
    ("susto", susto, GRANDE, "Jack Esqueleto · a caveira e o BU!", False),
    ("fogo_de_abobora", fogo_de_abobora, GRANDE, "Jack Esqueleto · a abóbora acesa voando", False),
    ("jack_esqueleto_preparo", jack_esqueleto_preparo, MEDIA, "Jack Esqueleto · a lua, a caveira e os morcegos (Preparo, laço)", True),
    ("noite_das_bruxas", noite_das_bruxas, GRANDE, "Jack Esqueleto · a lua, os morcegos e as abóboras", False),
    ("roubar_a_voz", roubar_a_voz, GRANDE, "Úrsula · a concha puxando a voz", False),
    ("tentaculos_de_ursula", tentaculos_de_ursula, GRANDE, "Úrsula · os tentáculos enrolando", False),
    ("ursula_preparo", ursula_preparo, MEDIA, "Úrsula · o tridente e as moreias (Preparo, laço)", True),
    ("tridente_da_bruxa", tridente_da_bruxa, GRANDE, "Úrsula · o redemoinho e a onda gigante", False),
    ("delaware_smash", delaware_smash, GRANDE, "Deku · o peteleco e a pressão do ar", False),
    ("full_cowl_corpo", full_cowl_corpo, GRANDE, "Deku · os raios verdes pelo corpo", False),
    ("deku_preparo", deku_preparo, MEDIA, "Deku · o braço carregando raios (Preparo, laço)", True),
    ("united_states_of_smash_deku", united_states_of_smash_deku, GRANDE, "Deku · o punho de raios e o tornado", False),
    ("texas_smash", texas_smash, GRANDE, "All Might · o soco e a rajada reta", False),
    ("estou_aqui", estou_aqui, GRANDE, "All Might · as mechas, o sorriso e o sol", False),
    ("allmight_preparo", allmight_preparo, MEDIA, "All Might · as mechas e a aura dourada (Preparo, laço)", True),
    ("united_states_of_smash_allmight", united_states_of_smash_allmight, GRANDE, "All Might · o punho do alto, as listras e o tornado", False),
]
