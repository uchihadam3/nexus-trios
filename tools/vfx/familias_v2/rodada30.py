"""Rodada 30 das habilidades próprias: Hellboy, Pica-Pau, Pernalonga, Ben 10, Samurai Jack, He-Man e Popeye.

Hellboy
- teimosia: os chifres serrados acendem e a casca de pedra cobre o corpo (Escudo e Fortalecido).
- hellboy_preparo: o Preparo da Pancada final — a Mão da Perdição erguida, brilhando com as runas (laço).
- pancada_final: a mão de pedra desce num soco enorme que racha o chão (Preso e Exposto).

Pica-Pau
- risada_irritante: a risada "ha-ha-ha-HA-ha" em notas pulando sobre o rival (Confuso e Enfraquecido).
- confusao_total: o redemoinho de penas e estrelinhas em todos (Confuso e Lento).

Pernalonga
- buraco_de_coelho: o buraco no chão, a terra pulando e o coelho saindo do outro lado (Acelerado e Esquiva).
- disfarce_pernalonga: a fumaça de troca de roupa com a peruca e o batom (Confuso).
- que_que_ha_velhinho: a cenoura mordida e a bigorna caindo no rival (Exposto).

Ben 10
- chama_ben10: o alien de fogo soltando as bolas de fogo em todos (Queimando).
- ben10_preparo: o Preparo do XLR8 — o Omnitrix girando com a luz verde (laço).
- xlr8: o borrão azul do alien veloz em zigue-zague e o impacto (Fortalecido).

Samurai Jack
- katana_magica: o corte limpo com o brilho dourado da espada mágica (Marcado e Exposto).
- postura_serena: o samurai em meditação, as folhas caindo e a luz calma (Protegido, Fortalecido e Purificar).
- jack_preparo: o Preparo do Corte decisivo — a mão na empunhadura e o vento parado (laço).
- corte_decisivo: o corte num instante: a linha que corta a tela e o rival cai depois (Preparo interrompido).

He-Man
- espada_do_poder: a Espada do Poder erguida com os raios e o golpe (Fortalecido).
- heman_preparo: o Preparo do Golpe de Grayskull — a espada no alto puxando os raios do céu (laço).
- golpe_de_grayskull: o castelo de Grayskull ao fundo e o golpe enorme da espada (Exposto).

Popeye
- lata_de_espinafre: a lata espremida, o espinafre voando para a boca e o músculo inchando (Fortalecido e energia).
- furacao_de_socos: o braço girando como hélice e os socos em sequência (Exposto).
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (AMPULHETA, CHAMA, ESPADA, FOLHA, NOTA, PENA, anel, aura, cheio, chuva, clarao, converge, corte, estouro, estrela_pts,
                         icone, onda_no_chao, particulas, poe, raios, runas, surge)


def _circ(n=24):
    return [(math.cos(TAU * k / n), math.sin(TAU * k / n)) for k in range(n)]


def _raio(T, t, x0, y0, x1, y1, k, w=0.02, seed=0):
    q = np.random.default_rng(int(t * 30) + seed)
    bolt = jagged(q, x0, y0, x1, y1, 5, 0.08)
    return T.polyline(bolt, w) * k * 1.4, T.polyline(bolt, w * 0.35) * k * 1.5


# ------------------------------------------------------------------ Hellboy

def teimosia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        G += T.gauss(lado * 0.14, -0.45, 0.06 * s + 0.001, 0.04 * s + 0.001) * 1.5
        H += T.gauss(lado * 0.14, -0.45, 0.025 * s + 0.001) * 2.0 * s
    cobre = ease_out(rel(t, 0.25, 0.65), 2)
    q = np.random.default_rng(3)
    for j in range(12):
        a = TAU * j / 12
        k = 1.0 if j / 12 < cobre else 0.0
        if k:
            placa = poe([(-1, -0.6), (1, -0.8), (0.9, 0.7), (-0.8, 0.6)], 0.32 * math.cos(a), 0.05 + 0.42 * math.sin(a), 0.07, a + q.uniform(-0.3, 0.3))
            g, h = icone(T, placa, (1 - rel(t, 0.88, 1)) * 1.0, 0.6)
            G, H = G + g, H + h
    g2, h2 = aura(T, t, 0.4, 1.0, 0.42, 0.05, 0.7)
    return (G + g2) * env, (H + h2) * env


def hellboy_preparo(T, t, rng):
    G, H = vazio(T)
    P, nos = _punho(T, 0.1, -0.2, 3.0, -math.pi / 2)
    G += P * 0.9
    H += nos * 0.4
    g, h = runas(T, (t * 0.5) % 1, 0.0, 1.0, 0.35, 8, -0.2, 1.0, 1.5)
    return G + g * 0.8, H + h


def pancada_final(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    desce = ease_in(rel(t, 0.0, 0.3), 2.5)
    k = 1 - rel(t, 0.5, 0.65)
    if k > 0:
        P, nos = _punho(T, 0.3, -0.75 + 0.95 * desce, 3.4, math.pi / 2)
        G += P * 0.95 * k
        H += nos * 0.5 * k
    g, h = clarao(T, t, 0.28, 0.5, 0.3, 0.3, 1.3, 1.5)
    G, H = G + g, H + h
    G += onda_no_chao(T, t, 0.28, 0.9, 1.0, 0.35, 1.8)
    q = np.random.default_rng(5)
    r = ease_out(rel(t, 0.3, 0.6), 2)
    for j in range(6):
        a = math.pi * j / 5
        pts = [(0.3, 0.35)] + [(0.3 + 0.8 * r * v * math.cos(a) + q.normal(0, 0.02), 0.35 + 0.12 * r * v * math.sin(a)) for v in (0.33, 0.66, 1.0)]
        G += T.polyline(pts, 0.015) * (1 - rel(t, 0.85, 1)) * 1.3
    return G * env, H * env


# ------------------------------------------------------------------ Pica-Pau

def risada_irritante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(5):
        u = rel(t, 0.06 * j, 0.5 + 0.06 * j)
        if 0 < u < 1:
            x = -0.5 + 0.25 * j
            y = -0.2 - 0.25 * abs(math.sin(u * 8)) - 0.15 * u
            g, h = cheio(T, poe(NOTA, x, y, 0.14 * (1.3 if j == 3 else 1.0)), (1 - rel(u, 0.75, 1)) * 1.3)
            G, H = G + g, H + h
    for j in range(4):
        a = t * 10 + TAU * j / 4
        kk = pulso(t, 0.4, 1.0)
        g2, h2 = cheio(T, poe(estrela_pts(5, 0.45), 0.55 + 0.15 * math.cos(a), -0.3 + 0.06 * math.sin(a), 0.04), kk * 1.3)
        G, H = G + g2, H + h2
    return G * env, H * env


def confusao_total(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(4)
    for j in range(14):
        a = q.uniform(0, TAU) + t * 8
        r = 0.2 + 0.5 * ease_out(rel(t, 0.0, 0.5)) * q.uniform(0.5, 1)
        g, h = icone(T, poe(PENA, r * math.cos(a), r * 0.6 * math.sin(a), 0.06, a), pulso(t, 0.0, 0.95) * 1.1, 0.6)
        G, H = G + g, H + h
    for x in (-0.55, 0.0, 0.55):
        for j in range(3):
            a = t * 9 + TAU * j / 3
            g2, h2 = cheio(T, poe(estrela_pts(5, 0.45), x + 0.12 * math.cos(a), -0.3 + 0.05 * math.sin(a), 0.035), pulso(t, 0.4, 1.0) * 1.3)
            G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Pernalonga

def buraco_de_coelho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for x, a, b in ((-0.5, 0.0, 0.5), (0.5, 0.35, 0.9)):
        k = pulso(t, a, b)
        if k > 0:
            G += T.ring(0.15, 0.04, x, 0.3, 0.35) * k * 1.3
            G += T.gauss(x, 0.3, 0.12, 0.04) * k * 0.8
    q = np.random.default_rng(6)
    for j in range(10):
        u = rel(t, 0.05, 0.4)
        if 0 < u < 1:
            G += T.gauss(-0.5 + q.normal(0, 0.1), 0.3 - 0.3 * math.sin(math.pi * u) * q.uniform(0.5, 1), 0.02) * (1 - u) * 1.3
    u = rel(t, 0.45, 0.8)
    if 0 < u < 1:
        y = 0.3 - 0.35 * math.sin(math.pi * u)
        for lado in (-1, 1):
            G += T.gauss(0.5 + lado * 0.04, y - 0.12, 0.02, 0.07) * 1.3
        G += T.gauss(0.5, y, 0.06) * 1.0
    return G * env, H * env


def disfarce_pernalonga(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    q = np.random.default_rng(3)
    k = pulso(t, 0.0, 0.6)
    pts = [(q.normal(0, 0.2), q.normal(0, 0.18), k * q.uniform(0.4, 0.9)) for _ in range(30)]
    G += T.splats(pts, 0.08) * 0.8
    s = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if s > 0:
        peruca = [(0.22 * s * math.cos(a), -0.1 + 0.2 * s * math.sin(a) * (1 if math.sin(a) < 0 else 0.4)) for a in np.linspace(0, TAU, 24, endpoint=False)]
        g, h = icone(T, peruca, 1.0, 0.45)
        G, H = G + g, H + h
        for lado in (-1, 1):
            G += T.ring(0.04, 0.008, lado * 0.06 * s, -0.08) * 1.2
        g2, h2 = cheio(T, poe([(-1, 0), (0, -0.4), (1, 0), (0, 0.4)], 0, 0.04, 0.06 * s), 1.4)
        G, H = G + g2, H + h2
    for j in range(3):
        a = t * 9 + TAU * j / 3
        G += T.ring(0.03, 0.008, 0.6 + 0.1 * math.cos(a), -0.3 + 0.04 * math.sin(a)) * pulso(t, 0.6, 1.0) * 1.2
    return G * env, H * env


def que_que_ha_velhinho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.2) * (1 - rel(t, 0.4, 0.5))
    if s > 0:
        cenoura = [(-0.5, -0.3), (-0.42, -0.36), (-0.2, 0.05), (-0.28, 0.08)]
        g, h = icone(T, [(x, y) for x, y in cenoura], s * 1.2, 0.6)
        G, H = G + g, H + h
        G += T.lines([(-0.46, -0.33, -0.5, -0.45, 1.0), (-0.46, -0.33, -0.42, -0.46, 1.0)], 0.012) * s * 1.2
    u = ease_in(rel(t, 0.25, 0.55), 2.2)
    k = 1 - rel(t, 0.7, 0.85)
    if u > 0 and k > 0:
        y = -0.9 + 0.95 * u
        bigorna = [(0.3, y - 0.08), (0.75, y - 0.08), (0.7, y), (0.62, y), (0.62, y + 0.08), (0.72, y + 0.12), (0.33, y + 0.12), (0.43, y + 0.08),
                   (0.43, y), (0.35, y)]
        g2, h2 = icone(T, bigorna, k * 1.2, 0.6)
        G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.53, 0.7, 0.52, 0.1, 1.0)
    G, H = G + g3, H + h3
    for j in range(5):
        a = TAU * j / 5 + t * 9
        g4, h4 = cheio(T, poe(estrela_pts(5, 0.45), 0.52 + 0.18 * math.cos(a), -0.15 + 0.06 * math.sin(a), 0.04), pulso(t, 0.6, 1.0) * 1.3)
        G, H = G + g4, H + h4
    return G * env, H * env


# ------------------------------------------------------------------ Ben 10

def chama_ben10(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j, (x, y) in enumerate(((-0.5, 0.1), (0.05, -0.15), (0.55, 0.1))):
        u = rel(t, 0.08 * j, 0.45 + 0.08 * j)
        if 0 < u < 1:
            px = -0.8 + (x + 0.8) * u
            py = 0.0 + (y - 0.0) * u - 0.2 * math.sin(math.pi * u)
            g, h = icone(T, poe(CHAMA, px, py, 0.2, math.pi / 2), 1.3, 0.6)
            G, H = G + g, H + h * 1.5
        g2, h2 = clarao(T, t, 0.43 + 0.08 * j, 0.6 + 0.08 * j, x, y, 0.6)
        G, H = G + g2, H + h2
        for m in range(4):
            kk = pulso(t, 0.45 + 0.08 * j, 0.95)
            g3, h3 = icone(T, poe(CHAMA, x - 0.15 + 0.1 * m, y + 0.05, 0.09 * kk), kk, 0.6)
            G, H = G + g3, H + h3
    return G * env, H * env


def ben10_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.ring(0.25, 0.04, 0, 0) * 1.2
    g, h = cheio(T, poe(AMPULHETA, 0, 0, 0.16, t * 4), 1.3)
    G, H = G + g, H + h * (1.5 + 0.5 * math.sin(t * 10))
    G += T.gauss(0, 0, 0.3) * (0.3 + 0.2 * math.sin(t * 10))
    return G, H


def xlr8(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    pontos = [(-0.75, 0.15), (-0.35, -0.2), (0.0, 0.2), (0.3, -0.15), (0.6, 0.05)]
    u = rel(t, 0.0, 0.45)
    if u > 0:
        total = ease_out(u, 2) * (len(pontos) - 1)
        for i in range(len(pontos) - 1):
            if i > total:
                break
            f = min(1.0, total - i)
            (x0, y0), (x1, y1) = pontos[i], pontos[i + 1]
            G += T.tapered([(x0, y0, x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, 1.0)], 0.06) * (1 - rel(t, 0.6, 0.85)) * 1.2
            H += T.lines([(x0, y0, x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, 1.0)], 0.01) * (1 - rel(t, 0.6, 0.85))
    g, h = clarao(T, t, 0.42, 0.62, 0.6, 0.05, 1.1)
    G, H = G + g, H + h
    G += estouro(T, t, 0.42, 0.8, 14, 4, 0.6, 0.05, 0.5, 0.014)
    return G * env, H * env


# ------------------------------------------------------------------ Samurai Jack

def katana_magica(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    g, h = corte(T, t, 0.05, 0.35, 0.25, 1.7, 0.09, 0.0, 0.0)
    G, H = G + g * 1.3, H + h
    brilho = pulso(t, 0.25, 0.7)
    G += T.lines([(-0.85, 0.2, 0.85, -0.2, 1.0)], 0.006) * brilho * 1.4
    H += T.gauss(0.5 - 1.0 * rel(t, 0.25, 0.6), -0.12 + 0.25 * rel(t, 0.25, 0.6), 0.04) * brilho * 2
    m = surge(t, 0.45, 0.65) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.ring(0.15 * m, 0.015, 0.5, -0.1) * 1.3 + T.ring(0.07 * m, 0.012, 0.5, -0.1) * 1.3
    return G * env, H * env


def postura_serena(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    g, h = aura(T, t, 0.0, 1.0, 0.38, 0.0, 0.9)
    G, H = G + g, H + h
    g2, h2 = chuva(T, t, 0.0, 1.0, FOLHA, 10, 4, 0.05, -0.8, 0.4, 0.7, 2.0, 1.1)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.2, 0.9, 0.15, 0.6, 0.025, 0.1, 3.0, 1.2)
    G += particulas(T, t, 0.3, 1.0, 20, 6, 0, 0, 0.4, 0.4, 0.012)
    return G * env, H * env


def jack_preparo(T, t, rng):
    G, H = vazio(T)
    G += T.lines([(-0.35, 0.05, 0.35, 0.05, 1.0)], 0.03) * 0.9
    G += T.lines([(0.15, -0.02, 0.15, 0.12, 1.0)], 0.03) * 1.0
    H += T.gauss(-0.1, 0.05, 0.02) * (1.2 + 0.6 * math.sin(t * 6))
    for j in range(3):
        y = -0.3 + 0.12 * j
        G += T.lines([(-0.5, y, 0.5, y, 1.0)], 0.004) * (0.4 + 0.2 * math.sin(t * 3 + j))
    return G, H


def corte_decisivo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    linha = pulso(t, 0.05, 0.55)
    if linha > 0:
        G += T.lines([(-1.0, 0.1, 1.0, -0.05, 1.0)], 0.03) * linha * 1.5
        H += T.lines([(-1.0, 0.1, 1.0, -0.05, 1.0)], 0.01) * linha * 1.5
    g, h = clarao(T, t, 0.05, 0.25, 0.5, 0.0, 0.9)
    G, H = G + g, H + h
    cai = rel(t, 0.5, 0.95)
    if 0 < cai < 1:
        q = np.random.default_rng(3)
        for j in range(8):
            x = 0.3 + q.uniform(0, 0.4)
            G += T.gauss(x, 0.0 + 0.4 * cai * cai, 0.03) * (1 - cai) * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ He-Man

def espada_do_poder(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.45, 0.6))
    if s > 0:
        g, h = icone(T, poe(ESPADA, -0.3, -0.25, 0.5 * s, 0), 1.2, 0.5)
        G, H = G + g, H + h
        for j in range(3):
            g2, h2 = _raio(T, t, -0.3, -0.75, -0.3 + (j - 1) * 0.3, -1.0, s, 0.012, j)
            G, H = G + g2, H + h2
    g3, h3 = corte(T, t, 0.4, 0.7, 0.8, 1.4, 0.09, 0.3, 0.0)
    G, H = G + g3 * 1.2, H + h3
    g4, h4 = clarao(T, t, 0.45, 0.65, 0.35, 0.0, 0.9)
    return (G + g4) * env, (H + h4) * env


def heman_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(ESPADA, 0, -0.05, 0.55, 0), 1.1, 0.5)
    G, H = G + g, H + h
    for j in range(2):
        g2, h2 = _raio(T, t, 0, -0.6, (j - 0.5) * 0.5, -1.0, 0.8, 0.012, j)
        G, H = G + g2, H + h2
    H += T.gauss(0, -0.6, 0.04) * (1.5 + 0.5 * math.sin(t * 10))
    return G, H


def golpe_de_grayskull(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.6, 0.8))
    if s > 0:
        castelo = [(-0.9, 0.4), (-0.9, -0.2), (-0.8, -0.2), (-0.8, -0.35), (-0.7, -0.35), (-0.7, -0.2), (-0.55, -0.2), (-0.55, -0.5), (-0.45, -0.5),
                   (-0.45, -0.2), (-0.3, -0.2), (-0.3, -0.35), (-0.2, -0.35), (-0.2, 0.4)]
        G += T.polyline(castelo, 0.015) * s * 1.0
        G += T.gauss(-0.6, 0.0, 0.05) * s * 0.8 + T.gauss(-0.45, 0.0, 0.05) * s * 0.8
    desce = ease_in(rel(t, 0.25, 0.5), 2)
    k = 1 - rel(t, 0.6, 0.75)
    if desce > 0 and k > 0:
        g, h = icone(T, poe(ESPADA, 0.35, -0.55 + 0.6 * desce, 0.6, -0.5 + 1.0 * desce), k * 1.2, 0.5)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.48, 0.7, 0.4, 0.2, 1.4, 1.5)
    G, H = G + g2, H + h2
    G += onda_no_chao(T, t, 0.48, 0.9, 0.95, 0.35, 1.6)
    return G * env, H * env


# ------------------------------------------------------------------ Popeye

def lata_de_espinafre(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    aperta = ease_in(rel(t, 0.1, 0.3), 2)
    s = 1 - rel(t, 0.4, 0.5)
    if s > 0:
        w = 0.12 * (1 - 0.6 * aperta)
        g, h = icone(T, [(-w, -0.1), (w, -0.1), (w, 0.15), (-w, 0.15)], s * 1.1, 0.5)
        G, H = G + g, H + h
    u = rel(t, 0.25, 0.5)
    if 0 < u < 1:
        for j in range(8):
            v = (u + j / 8) % 1
            G += T.gauss(0.0 + 0.1 * math.sin(v * 6 + j), -0.1 - 0.3 * v, 0.03) * (1 - v) * 1.4
    m = ease_out(rel(t, 0.5, 0.75), 2) * (1 - rel(t, 0.88, 1))
    if m > 0:
        G += T.gauss(0.3, 0.0, 0.12 + 0.12 * m, 0.1 + 0.08 * m) * 1.1
        G += T.ring(0.15 + 0.15 * m, 0.025, 0.3, 0.0, 0.7) * 1.2
        g2, h2 = icone(T, poe([(0, -1), (0.2, -0.2), (1, 0), (0.2, 0.2), (0, 1), (-0.2, 0.2), (-1, 0), (-0.2, -0.2)], 0.3, 0.0, 0.08 * m), 1.0, 0.6)
        G, H = G + g2, H + h2
    G += anel(T, t, 0.5, 0.95, 0.1, 0.6, 0.03, 0.0)
    return G * env, H * env


def furacao_de_socos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    gira = pulso(t, 0.0, 0.5)
    if gira > 0:
        a = t * 40
        G += T.arc_band(0.22, 0.05, a, a + 4.5, 1.0, 0, -0.45, 0.0, 1.0) * gira * 1.3
        P, _ = _punho(T, -0.45 + 0.22 * math.cos(a), 0.22 * math.sin(a), 1.2, a)
        G += P * 0.6 * gira
    for j in range(6):
        a0 = 0.35 + 0.06 * j
        k = pulso(t, a0, a0 + 0.12)
        if k > 0:
            P, nos = _punho(T, 0.2 + 0.1 * (j % 2), -0.15 + 0.1 * (j % 3), 1.8, 0)
            G += P * 0.9 * k
            H += nos * 0.4 * k
        g, h = clarao(T, t, a0 + 0.04, a0 + 0.14, 0.45, -0.1 + 0.08 * (j % 3), 0.4)
        G, H = G + g, H + h
    return G * env, H * env


REGISTRO = [
    ("teimosia", teimosia, GRANDE, "Hellboy · os chifres e a casca de pedra", False),
    ("hellboy_preparo", hellboy_preparo, MEDIA, "Hellboy · a Mão da Perdição erguida (Preparo, laço)", True),
    ("pancada_final", pancada_final, GRANDE, "Hellboy · o soco de pedra que racha o chão", False),
    ("risada_irritante", risada_irritante, GRANDE, "Pica-Pau · as notas da risada", False),
    ("confusao_total", confusao_total, GRANDE, "Pica-Pau · as penas e as estrelinhas", False),
    ("buraco_de_coelho", buraco_de_coelho, GRANDE, "Pernalonga · o buraco e a terra", False),
    ("disfarce_pernalonga", disfarce_pernalonga, GRANDE, "Pernalonga · a fumaça e a peruca", False),
    ("que_que_ha_velhinho", que_que_ha_velhinho, GRANDE, "Pernalonga · a cenoura e a bigorna", False),
    ("chama_ben10", chama_ben10, GRANDE, "Ben 10 · as bolas de fogo do Chama", False),
    ("ben10_preparo", ben10_preparo, MEDIA, "Ben 10 · o Omnitrix girando (Preparo, laço)", True),
    ("xlr8", xlr8, GRANDE, "Ben 10 · o borrão do XLR8", False),
    ("katana_magica", katana_magica, GRANDE, "Samurai Jack · o corte dourado", False),
    ("postura_serena", postura_serena, GRANDE, "Samurai Jack · a meditação e as folhas", False),
    ("jack_preparo", jack_preparo, MEDIA, "Samurai Jack · a mão na empunhadura (Preparo, laço)", True),
    ("corte_decisivo", corte_decisivo, GRANDE, "Samurai Jack · o corte num instante", False),
    ("espada_do_poder", espada_do_poder, GRANDE, "He-Man · a espada e os raios", False),
    ("heman_preparo", heman_preparo, MEDIA, "He-Man · a espada puxando os raios (Preparo, laço)", True),
    ("golpe_de_grayskull", golpe_de_grayskull, GRANDE, "He-Man · Grayskull e o golpe", False),
    ("lata_de_espinafre", lata_de_espinafre, GRANDE, "Popeye · a lata e o músculo", False),
    ("furacao_de_socos", furacao_de_socos, GRANDE, "Popeye · o braço-hélice e os socos", False),
]
