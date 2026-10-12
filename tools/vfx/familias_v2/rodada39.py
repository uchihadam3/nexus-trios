"""Rodada 39 das habilidades próprias: Hera Venenosa, Homem de Gelo, Gengar, Tenshinhan, Deidara e Violeta.

Hera Venenosa
- beijo_venenoso: os lábios soprando o beijo e os coraçõezinhos verdes de veneno no rival (Envenenado).
- raizes_estranguladoras: as raízes saindo do chão e se enrolando no rival (Preso e Envenenado).
- hera_preparo: o Preparo do Jardim tóxico — a flor abrindo e soltando os esporos (laço).
- jardim_toxico: as flores gigantes brotando nos rivais, a nuvem de esporos e as pétalas curando o trio (Envenenado e Vida).

Homem de Gelo
- rajada_congelante: o jato de gelo com a neve voando no rival (Lento).
- muralha_de_gelo: a muralha de gelo levantando na frente do trio (Barreira e Escudo).
- iceman_preparo: o Preparo da Era glacial — o corpo virando gelo, os cristais crescendo (laço).
- era_glacial: as geleiras pontudas brotando em todos e congelando (Congelado).

Gengar
- hipnose_gengar: os olhos em espiral roxa e o "Zzz" no rival (Dormindo).
- bola_sombria: a bola de sombra roxa com os fiapos escuros (Amaldiçoado).
- gengar_preparo: o Preparo do Comedor de sonhos — o sorriso enorme e os olhos vermelhos na sombra (laço).
- comedor_de_sonhos: a bolha de sonho saindo do rival e sendo sugada pelo Gengar (dano e Vida).

Tenshinhan
- taiyoken_tenshinhan: as mãos na testa e o clarão do Sol cegando todos (Cego).
- golpe_de_quatro_bracos: os quatro punhos acertando juntos (Exposto).
- tenshinhan_preparo: o Preparo do Kikoho — as mãos em triângulo juntando energia (laço).
- kikoho: o triângulo de energia caindo e o buraco em triângulo no chão (dano nele também).

Deidara
- aranhas_de_argila: as aranhinhas de argila correndo até o rival e grudando (Marca explosiva).
- passaro_de_argila: o pássaro de argila passando e soltando as bombinhas em todos (Exposto).
- deidara_preparo: o Preparo do C4 Karura — a argila sendo moldada pelas bocas das mãos (laço).
- c4_karura: a nuvem de minibombas invisíveis e o "Katsu!" estourando por dentro em todos (Marca explosiva).

Violeta
- campo_de_forca: a bolha roxa de campo de força cobrindo o trio (Barreira e Escudo).
- invisibilidade_violeta: o contorno sumindo em pontinhos (Esquiva).
- violeta_preparo: o Preparo da Esfera de força — as mãos estendidas formando a esfera (laço).
- esfera_de_forca: a esfera de força roxa rolando e prendendo o rival dentro (Preso).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (CORACAO, anel, cheio, circulo, clarao, converge, estouro, estrela_pts, flor, icone, onda_no_chao, particulas, poe, raios,
                         surge)


def _cristal(cx, cy, s, ang):
    pts = [(0, -1), (0.3, 0), (0, 1), (-0.3, 0)]
    c, sn = math.cos(ang), math.sin(ang)
    return [(cx + s * (x * c - y * sn), cy + s * (x * sn + y * c)) for x, y in pts]


def _zzz(T, cx, cy, s, k):
    G = 0.0
    for j in range(3):
        x, y, z = cx + 0.08 * j * s * 6, cy - 0.08 * j * s * 6, s * (0.6 + 0.25 * j)
        G = G + T.lines([(x - z, y - z, x + z, y - z, 1.0), (x + z, y - z, x - z, y + z, 1.0), (x - z, y + z, x + z, y + z, 1.0)], z * 0.25) * k * 1.3
    return G


def _espiral(T, cx, cy, r, gira, k, w=0.015):
    pts = [(cx + r * (a / 12) * math.cos(a + gira), cy + r * (a / 12) * math.sin(a + gira)) for a in np.linspace(0.3, 12, 50)]
    return T.polyline(pts, w) * k * 1.3


# ------------------------------------------------------------------ Hera Venenosa

_LABIOS = [(-1, 0), (-0.5, -0.45), (0, -0.2), (0.5, -0.45), (1, 0), (0.5, 0.45), (0, 0.55), (-0.5, 0.45)]


def beijo_venenoso(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.4, 0.5))
    if s > 0:
        g, h = icone(T, poe(_LABIOS, -0.55, -0.05, 0.2 * s), 1.2, 0.6)
        G, H = G + g, H + h
    for j in range(5):
        u = rel(t, 0.15 + 0.05 * j, 0.6 + 0.05 * j)
        if 0 < u < 1:
            x = -0.45 + 1.0 * u
            y = -0.05 + 0.12 * math.sin(u * 8 + j) - 0.05 * j * (1 - u)
            g2, h2 = cheio(T, poe(CORACAO, x, y, 0.08 + 0.03 * (j % 2)), (1 - rel(u, 0.85, 1)) * 1.3)
            G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.55, 0.72, 0.55, 0.0, 0.6)
    G, H = G + g3, H + h3
    k = pulso(t, 0.6, 1.0)
    q = np.random.default_rng(5)
    for _ in range(10):
        a = q.uniform(0, TAU)
        r = 0.08 + 0.2 * q.uniform(0, 1)
        G += T.gauss(0.55 + r * math.cos(a), r * math.sin(a) - 0.1 * rel(t, 0.6, 1.0), 0.02) * k * 1.0
    return G * env, H * env


def _raiz(T, x0, y0, alto, sobe, enrola, lado, k):
    pts = []
    for v in np.linspace(0, 1, 24):
        if v > sobe:
            break
        y = y0 - alto * v
        x = x0 + lado * 0.05 * math.sin(v * 7) + (0.12 * math.cos(v * TAU * 2 * enrola + lado) * v * enrola)
        pts.append((x, y))
    if len(pts) < 2:
        return 0.0
    return T.polyline(pts, 0.022) * k * 1.3


def raizes_estranguladoras(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = ease_out(rel(t, 0.0, 0.45), 2)
    enrola = ease_in(rel(t, 0.3, 0.7), 1.5)
    k = 1 - rel(t, 0.88, 1)
    for j, lado in enumerate((-1, 1, -1, 1)):
        G += _raiz(T, 0.45 + 0.07 * (j - 1.5), 0.35, 0.6, sobe, enrola, lado, k)
    G += onda_no_chao(T, t, 0.0, 0.5, 0.5, 0.35, 1.2)
    m = pulso(t, 0.6, 1.0)
    for j in range(6):
        u = ((t * 1.5) + j / 6) % 1
        G += T.gauss(0.45 + 0.15 * math.sin(j * 2), 0.0 - 0.3 * u, 0.018) * m * (1 - u) * 1.2
    return G * env, H * env


def hera_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    g, h = icone(T, poe(flor(6, 1.0, 0.3), 0, 0, 0.18 * (0.9 + 0.1 * b), t), 1.1, 0.5)
    G, H = G + g, H + h
    H += T.gauss(0, 0, 0.04) * (1.2 + b)
    for j in range(6):
        u = ((t * 1.3) + j / 6) % 1
        a = TAU * j / 6 + 0.5
        G += T.gauss(0.2 * u * math.cos(a) * 2, 0.2 * u * math.sin(a) * 2 - 0.1 * u, 0.018) * (1 - u) * 1.3
    return G, H


def jardim_toxico(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        s = surge(t, 0.1 + 0.07 * j, 0.35 + 0.07 * j) * (1 - rel(t, 0.85, 1))
        if s > 0:
            G += T.lines([(x, 0.35, x, 0.35 - 0.25 * s, 1.0)], 0.02) * 1.1
            g, h = icone(T, poe(flor(7, 1.0, 0.3), x, 0.08 - 0.05 * s, 0.17 * s, t * 0.5 + j), 1.2, 0.5)
            G, H = G + g, H + h
    k = pulso(t, 0.35, 0.95)
    q = np.random.default_rng(8)
    pts = [(q.uniform(-0.8, 0.8), q.uniform(-0.45, 0.2) - 0.2 * rel(t, 0.35, 1.0), k * q.uniform(0.3, 0.8)) for _ in range(40)]
    G += T.splats(pts, 0.045) * 0.6
    for j in range(8):
        u = rel(t, 0.5 + 0.03 * j, 0.95)
        if 0 < u < 1:
            x = -0.8 + 0.2 * j
            g2, h2 = cheio(T, poe(CORACAO, x, -0.6 + 0.2 * u, 0.03), (1 - u) * 1.3)
            G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Homem de Gelo

def rajada_congelante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.05, 0.6)
    if k > 0:
        G += T.tapered([(-0.7, 0.0, 0.55, 0.0, 1.0)], 0.09 * k + 0.01) * 1.2
        H += T.lines([(-0.7, 0.0, 0.55, 0.0, 1.0)], 0.012) * k * 1.4
        q = np.random.default_rng(int(t * 25))
        for _ in range(16):
            x = q.uniform(-0.6, 0.6)
            G += T.gauss(x, q.normal(0, 0.08), 0.014) * k * 1.3
    g, h = clarao(T, t, 0.25, 0.5, 0.55, 0.0, 0.8)
    G, H = G + g, H + h
    s = surge(t, 0.35, 0.55) * (1 - rel(t, 0.88, 1))
    if s > 0:
        for j in range(5):
            a = TAU * j / 5 + 0.3
            g2, h2 = icone(T, _cristal(0.55 + 0.1 * math.cos(a), 0.1 * math.sin(a), 0.07 * s, a + math.pi / 2), 1.1, 0.5)
            G, H = G + g2, H + h2
    return G * env, H * env


def muralha_de_gelo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    sobe = ease_out(rel(t, 0.0, 0.4), 2.5)
    k = 1 - rel(t, 0.85, 1)
    if sobe > 0 and k > 0:
        q = np.random.default_rng(3)
        x0 = 0.75
        for j in range(5):
            y = 0.35 - 0.16 * j * sobe
            larg = 0.12
            bloco = [(x0 - larg, y), (x0 + larg, y - 0.02), (x0 + larg * 0.95, y - 0.16 * sobe), (x0 - larg * 0.9, y - 0.15 * sobe)]
            g, h = icone(T, bloco, k * 1.1, 0.45)
            G, H = G + g, H + h
            H += T.gauss(x0 - 0.05, y - 0.1 * sobe, 0.012) * k * 1.4 * q.uniform(0.5, 1)
    for x in (-0.55, 0.0, 0.55):
        m = surge(t, 0.35, 0.55) * k
        if m > 0:
            G += T.arc_band(0.2 * m, 0.03, -2.6, -0.5, 1.0, 0, x, 0.3, 0.0) * 1.1
    G += particulas(T, t, 0.2, 0.9, 16, 4, 0.75, 0.0, 0.2, 0.5, 0.011)
    return G * env, H * env


def iceman_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.gauss(0, 0.0, 0.12, 0.25) * 0.6
    for j in range(10):
        a = TAU * j / 10
        cresce = 0.6 + 0.4 * ((t * 1.5 + j / 10) % 1)
        g, h = icone(T, _cristal(0.22 * math.cos(a), 0.3 * math.sin(a), 0.06 * cresce, a + math.pi / 2), 1.0, 0.5)
        G, H = G + g, H + h
    H += T.gauss(0, -0.15, 0.03) * (1.2 + 0.6 * math.sin(t * 9))
    return G, H


def era_glacial(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(6)
    for j in range(13):
        x = -0.9 + 0.15 * j
        a0 = 0.05 + 0.03 * j
        sobe = ease_out(rel(t, a0, a0 + 0.2), 3)
        k = 1 - rel(t, 0.85, 1)
        if sobe > 0 and k > 0:
            alto = q.uniform(0.3, 0.65) * sobe
            pts = [(x - 0.07, 0.35), (x - 0.03, 0.35 - alto * 0.7), (x + 0.01, 0.35 - alto), (x + 0.07, 0.35)]
            g, h = icone(T, pts, k * 1.1, 0.5)
            G, H = G + g, H + h
            H += T.gauss(x + 0.01, 0.35 - alto, 0.012) * k * 1.4
    G += onda_no_chao(T, t, 0.05, 0.6, 1.0, 0.35, 1.5)
    for x in (-0.55, 0.0, 0.55):
        g2, h2 = clarao(T, t, 0.4, 0.6, x, 0.05, 0.5)
        G, H = G + g2, H + h2
    G += particulas(T, t, 0.3, 1.0, 24, 7, 0, -0.1, 0.9, 0.4, 0.011)
    return G * env, H * env


# ------------------------------------------------------------------ Gengar

def hipnose_gengar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.75, 0.9))
    if s > 0:
        for lado in (-1, 1):
            G += _espiral(T, -0.5 + lado * 0.13, -0.15, 0.1 * s, t * 10 * lado, 1.0, 0.012)
    for j in range(4):
        u = rel(t, 0.15 + 0.08 * j, 0.6 + 0.08 * j)
        if 0 < u < 1:
            G += T.ring(0.06 + 0.15 * u, 0.012, -0.5 + 1.0 * u, -0.15 + 0.15 * u, 1.0) * (1 - u) * 1.2
    m = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += _zzz(T, 0.55, -0.25, 0.04 * m, 1.0)
    G += T.gauss(0.5, 0.05, 0.18) * pulso(t, 0.5, 1.0) * 0.4
    return G * env, H * env


def bola_sombria(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.1, 0.5), 1.4)
    k = 1 - rel(t, 0.5, 0.58)
    cresce = ease_out(rel(t, 0.0, 0.2), 2)
    if k > 0 and cresce > 0:
        x = -0.6 + 1.15 * u
        r = 0.13 * cresce
        G += T.gauss(x, 0.0, r) * k * 1.3
        G += T.ring(r, 0.02, x, 0.0) * k * 1.2
        H += T.gauss(x, 0.0, r * 0.3) * k * 0.8
        q = np.random.default_rng(int(t * 30))
        for _ in range(5):
            a = q.uniform(0, TAU)
            G += T.polyline(jagged(q, x + r * math.cos(a), r * math.sin(a), x + 1.8 * r * math.cos(a), 1.8 * r * math.sin(a), 3, 0.3), 0.008) * k * 1.2
        G += T.tapered([(x - 0.35, 0.0, x - r, 0.0, 1.0)], r * 0.8) * k * 0.6
    g, h = clarao(T, t, 0.48, 0.68, 0.55, 0.0, 1.2, 1.3)
    G, H = G + g, H + h
    G += estouro(T, t, 0.5, 0.95, 14, 5, 0.55, 0.0, 0.5, 0.013)
    m = pulso(t, 0.55, 1.0)
    for j in range(5):
        v = ((t * 1.2) + j / 5) % 1
        G += T.gauss(0.55 + 0.1 * math.sin(j * 3 + t * 4), -0.05 - 0.35 * v, 0.03 + 0.02 * v) * m * (1 - v) * 0.8
    return G * env, H * env


def gengar_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.gauss(0, 0.0, 0.3, 0.25) * 0.4
    pis = 1.0 if (t * 2) % 1 > 0.1 else 0.3
    for lado in (-1, 1):
        olho = [(lado * 0.12 + 0.07 * math.cos(a), -0.1 + 0.035 * math.sin(a) - lado * 0.01 * math.cos(a)) for a in np.linspace(0, TAU, 14, endpoint=False)]
        g, h = cheio(T, olho, 1.3 * pis)
        G, H = G + g, H + h * 2
    sorriso = [(0.22 * math.cos(a), 0.0 + 0.12 * math.sin(a)) for a in np.linspace(0.15, math.pi - 0.15, 20)]
    G += T.polyline(sorriso, 0.02) * 1.3
    dentes = [(-0.18 + 0.06 * m, 0.03 + 0.02 * math.sin(m), -0.18 + 0.06 * m, 0.07, 1.0) for m in range(7)]
    G += T.lines(dentes, 0.008) * 1.2
    return G, H


def comedor_de_sonhos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.05, 0.3)
    u = ease_in(rel(t, 0.35, 0.75), 1.6)
    k = 1 - rel(t, 0.72, 0.8)
    if s > 0 and k > 0:
        x = 0.5 + (-0.55 - 0.5) * u
        y = -0.35 + 0.2 * u - 0.1 * math.sin(math.pi * u)
        r = 0.14 * s * (1 - 0.6 * u)
        G += T.ring(r, 0.015, x, y) * k * 1.3
        G += T.gauss(x, y, r * 0.8) * k * 0.6
        g, h = cheio(T, poe(estrela_pts(5, 0.45), x - r * 0.2, y, r * 0.35, t * 3), k * 1.2)
        G, H = G + g, H + h
        for m in range(3):
            G += T.ring(0.02 + 0.01 * m, 0.006, 0.5 - 0.04 * m * (1 - u), -0.1 - 0.06 * m, 1.0) * k * (1 - u) * 1.0
    G += converge(T, t, 0.4, 0.85, 14, 3, -0.55, -0.15, 0.4)
    g2, h2 = clarao(T, t, 0.72, 0.88, -0.55, -0.15, 0.8)
    G, H = G + g2, H + h2
    w = rel(t, 0.75, 1.0)
    if 0 < w < 1:
        G += T.ring(0.05 + 0.4 * ease_out(w, 2), 0.03 * (1 - 0.5 * w), -0.55, -0.15) * (1 - w) * 1.2
    G += T.gauss(0.5, 0.05, 0.15) * pulso(t, 0.0, 0.5) * 0.5
    return G * env, H * env


# ------------------------------------------------------------------ Tenshinhan

def taiyoken_tenshinhan(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.3, 0.4))
    if s > 0:
        for lado in (-1, 1):
            G += T.gauss(-0.6 + lado * 0.08, -0.3, 0.04, 0.07) * s * 1.1
    k = pulso(t, 0.25, 0.75)
    if k > 0:
        G += T.gauss(-0.6, -0.3, 0.5 * k + 0.02) * k * 1.4
        H += T.gauss(-0.6, -0.3, 0.12 * k + 0.01) * k * 2.0
        for j in range(16):
            a = TAU * j / 16 + t
            G += T.tapered([(-0.6, -0.3, -0.6 + 1.6 * math.cos(a), -0.3 + 1.0 * math.sin(a), 1.0)], 0.03) * k * 0.5
    g, h = clarao(T, t, 0.25, 0.55, -0.6, -0.3, 1.8, 1.8)
    G, H = G + g, H + h
    for x in (-0.55, 0.0, 0.55):
        m = pulso(t, 0.55, 1.0)
        G += T.lines([(x + 0.25 - 0.08, -0.1, x + 0.25 + 0.08, -0.1, 1.0)], 0.02) * m * 1.2
    return G * env, H * env


def golpe_de_quatro_bracos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.05, 0.3), 2)
    k = 1 - rel(t, 0.45, 0.6)
    if k > 0:
        for j, dy in enumerate((-0.24, -0.08, 0.08, 0.24)):
            x = -0.55 + 0.85 * u + 0.04 * (j % 2)
            P, nos = _punho(T, x, dy, 1.7, 0)
            G += P * 0.9 * k
            H += nos * 0.35 * k
            G += T.tapered([(x - 0.4, dy, x - 0.1, dy, 1.0)], 0.05) * k * 0.6
    g, h = clarao(T, t, 0.28, 0.5, 0.5, 0.0, 1.3, 1.4)
    G, H = G + g, H + h
    for j, dy in enumerate((-0.24, -0.08, 0.08, 0.24)):
        g2, h2 = clarao(T, t, 0.28 + 0.02 * j, 0.42 + 0.02 * j, 0.5, dy, 0.35)
        G, H = G + g2, H + h2
    G += estouro(T, t, 0.3, 0.8, 14, 4, 0.5, 0.0, 0.5, 0.013)
    return G * env, H * env


def _triangulo(cx, cy, s, inverte=False):
    sg = -1 if inverte else 1
    return [(cx, cy - sg * s), (cx + s * 0.95, cy + sg * s * 0.6), (cx - s * 0.95, cy + sg * s * 0.6)]


def tenshinhan_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    tri = _triangulo(0, 0, 0.2)
    G += T.polyline(tri + [tri[0]], 0.03) * 1.2
    G += T.gauss(0, 0.03, 0.08 + 0.03 * b) * (1.0 + 0.5 * b)
    H += T.gauss(0, 0.03, 0.04) * (1.4 + b)
    G += converge(T, (t * 2) % 1, 0.0, 1.0, 10, int(t * 2), 0, 0.03, 0.4)
    return G, H


def kikoho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    desce = ease_in(rel(t, 0.0, 0.35), 2)
    k = 1 - rel(t, 0.45, 0.6)
    if k > 0:
        cy = -0.9 + 1.0 * desce
        s = 0.25 + 0.15 * desce
        tri = _triangulo(0.45, cy, s, True)
        g, h = icone(T, tri, k * 1.3, 0.6)
        G, H = G + g, H + h
        G += T.polys([([(0.45 - s * 0.95, cy - 0.6 * s), (0.45 + s * 0.95, cy - 0.6 * s), (0.45 + 0.4 * s, -1.0), (0.45 - 0.4 * s, -1.0)], 1.0)], 0.04) * k * 0.4
    g2, h2 = clarao(T, t, 0.32, 0.55, 0.45, 0.15, 1.6, 1.6)
    G, H = G + g2, H + h2
    m = surge(t, 0.4, 0.6) * (1 - rel(t, 0.85, 1))
    if m > 0:
        tri2 = [(x, 0.3 + (y - 0.3) * 0.35) for x, y in _triangulo(0.45, 0.3, 0.35 * m, True)]
        G += T.polyline(tri2 + [tri2[0]], 0.025) * 1.3
    G += onda_no_chao(T, t, 0.35, 0.95, 1.0, 0.35, 1.7)
    G += estouro(T, t, 0.35, 0.95, 18, 6, 0.45, 0.15, 0.7, 0.014)
    G += T.gauss(-0.6, 0.05, 0.12) * pulso(t, 0.5, 0.8) * 0.6
    return G * env, H * env


# ------------------------------------------------------------------ Deidara

def _aranha(T, cx, cy, s, t, k):
    g, h = cheio(T, poe(circulo(12), cx, cy, s), k * 1.2)
    pernas = []
    for lado in (-1, 1):
        for m in range(4):
            a = lado * (0.5 + 0.5 * m) + 0.15 * math.sin(t * 40 + m)
            pernas.append((cx, cy, cx + lado * s * 2.2 * abs(math.cos(a)), cy - s * 1.6 * math.sin(a) * lado * 0.6 + s * 0.6, 1.0))
    return g + T.lines(pernas, s * 0.18) * k * 1.2, h


def aranhas_de_argila(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(5):
        a0 = 0.03 * j
        u = ease_out(rel(t, a0, a0 + 0.45), 1.3)
        if u > 0:
            x = -0.7 + (0.4 + 0.07 * (j - 2) + 0.7) * u
            y = 0.3 - 0.3 * u + 0.06 * (j - 2) * u
            g, h = _aranha(T, x, y, 0.06, t + j, 1 - rel(t, 0.85, 1))
            G, H = G + g, H + h
    m = surge(t, 0.5, 0.7) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.18 * m, 0.015, 0.4, 0.0) * 1.2
        G += T.ring(0.1 * m, 0.01, 0.4, 0.0) * (0.6 + 0.4 * math.sin(t * 30)) * 1.2
    return G * env, H * env


_PASSARO = [(1.0, 0), (0.5, -0.15), (0.1, -0.9), (-0.15, -0.2), (-0.8, -0.1), (-1.0, 0.2), (-0.6, 0.15), (-0.15, 0.2), (0.1, 0.9), (0.5, 0.15)]


def passaro_de_argila(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.6)
    if 0 < u < 1:
        x = -0.95 + 1.9 * u
        bat = math.sin(t * 25) * 0.3
        pts = [(px, py * (1 + bat)) for px, py in _PASSARO]
        g, h = icone(T, poe(pts, x, -0.5, 0.26), 1.2, 0.5)
        G, H = G + g, H + h
    for j, xb in enumerate((-0.55, 0.0, 0.55)):
        solta = (xb + 0.95) / 1.9 * 0.6
        w = rel(t, solta, solta + 0.2)
        if 0 < w < 1:
            G += T.gauss(xb, -0.45 + 0.5 * ease_in(w, 2), 0.03) * 1.4
        g2, h2 = clarao(T, t, solta + 0.2, solta + 0.38, xb, 0.05, 0.7)
        G, H = G + g2, H + h2
        G += estouro(T, t, solta + 0.2, solta + 0.5, 10, j, xb, 0.05, 0.35, 0.012)
    return G * env, H * env


def deidara_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        cx = lado * 0.22
        G += T.gauss(cx, 0.05, 0.09, 0.07) * 0.9
        abre = 0.02 + 0.02 * abs(math.sin(t * 12 + lado))
        G += T.lines([(cx - 0.05, 0.05 - abre, cx + 0.05, 0.05 - abre, 1.0), (cx - 0.05, 0.05 + abre, cx + 0.05, 0.05 + abre, 1.0)], 0.01) * 1.4
    molda = 0.5 + 0.5 * math.sin(t * TAU * 1.5)
    pts = [(0.08 * (1 + 0.2 * molda) * math.cos(a), -0.15 + 0.06 * (1 - 0.2 * molda) * math.sin(a)) for a in np.linspace(0, TAU, 16, endpoint=False)]
    g, h = icone(T, pts, 1.2, 0.6)
    return G + g, H + h


def c4_karura(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(11)
    espalha = ease_out(rel(t, 0.0, 0.45), 2)
    k = pulso(t, 0.0, 0.6)
    pts = [(q.normal(0.0, 0.45) * espalha, -0.3 + q.normal(0, 0.25) * espalha + 0.2 * espalha, k * q.uniform(0.4, 1.0)) for _ in range(140)]
    G += T.splats(pts, 0.007) * 1.4
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        for m in range(4):
            a0 = 0.55 + 0.04 * m + 0.03 * j
            dx, dy = 0.08 * math.cos(m * 2.1 + j), 0.08 * math.sin(m * 2.1 + j)
            g, h = clarao(T, t, a0, a0 + 0.14, x + dx, 0.0 + dy, 0.35)
            G, H = G + g, H + h
        G += T.gauss(x, 0.0, 0.14) * pulso(t, 0.55, 0.85) * 0.7
    G += estouro(T, t, 0.6, 0.98, 18, 8, 0.0, 0.0, 0.8, 0.012)
    return G * env, H * env


# ------------------------------------------------------------------ Violeta

def campo_de_forca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2.5) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.arc_band(0.85 * s, 0.035, math.pi, TAU, 0.6, 0, 0.0, 0.35, 0.0) * 1.3
        G += T.gauss(0.0, 0.1, 0.75 * s, 0.35 * s) * 0.3
        brilho = pulso(t, 0.2, 0.6)
        G += T.arc_band(0.85 * s, 0.015, math.pi + 0.3, math.pi + 1.0, 0.6, 0, 0.0, 0.35, 0.0) * brilho * 1.5
        q = np.random.default_rng(int(t * 8))
        for _ in range(3):
            a = q.uniform(math.pi, TAU)
            H += T.gauss(0.85 * s * math.cos(a), 0.35 + 0.85 * 0.6 * s * math.sin(a), 0.02) * 1.0
    return G * env, H * env


def invisibilidade_violeta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    some = rel(t, 0.1, 0.7)
    q = np.random.default_rng(3)
    pts = []
    for _ in range(80):
        a = q.uniform(0, TAU)
        r = q.uniform(0.0, 1.0)
        x, y = 0.12 * r * math.cos(a), -0.05 + 0.3 * r * math.sin(a)
        vivo = 1.0 if q.uniform(0, 1) > some else 0.0
        pts.append((x + 0.15 * some * q.normal(), y - 0.2 * some * q.uniform(0, 1), vivo * (1 - rel(t, 0.85, 1))))
    G += T.splats(pts, 0.012) * 1.3
    G += T.ring(0.25, 0.012, 0.0, -0.05, 0.5) * pulso(t, 0.0, 0.6) * 1.0
    G += anel(T, t, 0.3, 0.8, 0.1, 0.5, 0.025, 0.0)
    return G * env, H * env


def violeta_preparo(T, t, rng):
    G, H = vazio(T)
    for lado in (-1, 1):
        G += T.gauss(lado * 0.3, 0.1, 0.05) * 1.0
        G += T.lines([(lado * 0.3, 0.1, lado * 0.17, 0.0, 1.0)], 0.012) * 0.8
    cresce = 0.1 + 0.05 * math.sin(t * TAU * 2)
    G += T.ring(cresce, 0.025, 0, 0.0) * 1.3
    G += T.gauss(0, 0, cresce * 0.8) * 0.6
    H += T.gauss(-cresce * 0.3, -cresce * 0.3, 0.02) * 1.5
    return G, H


def esfera_de_forca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.4), 1.5)
    k = 1 - rel(t, 0.88, 1)
    x = -0.6 + 1.05 * min(1, u)
    r = 0.12 + 0.08 * ease_out(rel(t, 0.38, 0.55), 2)
    G += T.ring(r, 0.03, x, 0.05) * k * 1.3
    G += T.gauss(x, 0.05, r * 0.85) * k * 0.4
    a = t * 12
    G += T.arc_band(r * 0.75, 0.012, a, a + 1.2, 1.0, 0, x, 0.05, 0.0) * k * 1.2
    H += T.gauss(x - r * 0.4, 0.05 - r * 0.4, 0.02) * k * 1.5
    if u < 1:
        G += T.tapered([(x - 0.35, 0.05, x - r, 0.05, 1.0)], 0.06) * k * 0.6
    g, h = clarao(T, t, 0.38, 0.55, 0.45, 0.05, 1.0)
    G, H = G + g, H + h
    m = pulso(t, 0.5, 1.0)
    if m > 0:
        G += T.gauss(0.45, 0.05, 0.07, 0.12) * m * 0.8
    return G * env, H * env


REGISTRO = [
    ("beijo_venenoso", beijo_venenoso, GRANDE, "Hera Venenosa · os lábios e os corações de veneno", False),
    ("raizes_estranguladoras", raizes_estranguladoras, GRANDE, "Hera Venenosa · as raízes se enrolando", False),
    ("hera_preparo", hera_preparo, MEDIA, "Hera Venenosa · a flor soltando esporos (Preparo, laço)", True),
    ("jardim_toxico", jardim_toxico, GRANDE, "Hera Venenosa · as flores gigantes e os esporos", False),
    ("rajada_congelante", rajada_congelante, GRANDE, "Homem de Gelo · o jato de gelo e a neve", False),
    ("muralha_de_gelo", muralha_de_gelo, GRANDE, "Homem de Gelo · a muralha de gelo na frente do trio", False),
    ("iceman_preparo", iceman_preparo, MEDIA, "Homem de Gelo · os cristais crescendo (Preparo, laço)", True),
    ("era_glacial", era_glacial, GRANDE, "Homem de Gelo · as geleiras pontudas em todos", False),
    ("hipnose_gengar", hipnose_gengar, GRANDE, "Gengar · os olhos em espiral e o Zzz", False),
    ("bola_sombria", bola_sombria, GRANDE, "Gengar · a bola de sombra", False),
    ("gengar_preparo", gengar_preparo, MEDIA, "Gengar · o sorriso e os olhos vermelhos (Preparo, laço)", True),
    ("comedor_de_sonhos", comedor_de_sonhos, GRANDE, "Gengar · a bolha de sonho sugada", False),
    ("taiyoken_tenshinhan", taiyoken_tenshinhan, GRANDE, "Tenshinhan · o clarão do Sol", False),
    ("golpe_de_quatro_bracos", golpe_de_quatro_bracos, GRANDE, "Tenshinhan · os quatro punhos juntos", False),
    ("tenshinhan_preparo", tenshinhan_preparo, MEDIA, "Tenshinhan · as mãos em triângulo (Preparo, laço)", True),
    ("kikoho", kikoho, GRANDE, "Tenshinhan · o triângulo de energia caindo", False),
    ("aranhas_de_argila", aranhas_de_argila, GRANDE, "Deidara · as aranhinhas de argila", False),
    ("passaro_de_argila", passaro_de_argila, GRANDE, "Deidara · o pássaro soltando as bombinhas", False),
    ("deidara_preparo", deidara_preparo, MEDIA, "Deidara · as bocas das mãos moldando (Preparo, laço)", True),
    ("c4_karura", c4_karura, GRANDE, "Deidara · a nuvem de minibombas e o Katsu!", False),
    ("campo_de_forca", campo_de_forca, GRANDE, "Violeta · a bolha roxa no trio", False),
    ("invisibilidade_violeta", invisibilidade_violeta, GRANDE, "Violeta · o contorno sumindo em pontinhos", False),
    ("violeta_preparo", violeta_preparo, MEDIA, "Violeta · as mãos formando a esfera (Preparo, laço)", True),
    ("esfera_de_forca", esfera_de_forca, GRANDE, "Violeta · a esfera rolando e prendendo", False),
]
