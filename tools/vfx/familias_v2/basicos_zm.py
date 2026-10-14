"""Ataques básicos com animação própria, lote zm: Frieren, Gambit, Aang, Pernalonga, Salsicha, Pateta, Yugi e Kaiba.

O cajado da Frieren com o círculo mágico e o raio da Zoltraak, o bastão do Gambit carregado de energia cinética rosa, o
bastão do Aang com o redemoinho de ar, a cenoura do Pernalonga com a mordida, os tapas desesperados do Salsicha com as
gotas de suor, a trombada desastrada do Pateta com as estrelinhas, a carta do Yugi com o Olho de Hórus e a carta do
Kaiba com o brilho azul do Dragão Branco.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_d import _desenha_carta
from .basicos_u import _anel, _estrela_de_contato, _riscos
from .basicos_x import _gotas


# ------------------------------------------------------------------ Frieren
def zoltraak_frieren(T, t, rng):
    """Frieren: a ponta do cajado abre um círculo mágico de runas, e dele sai a Zoltraak, o raio fino e branco de
    magia que mata demônios, reto e certeiro."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    kc = janela(t, 0.0, 0.08) * (1 - rel(t, 0.42, 0.55))
    cx, cy = -0.75, 0.0
    circulo = T.zero()
    if kc > 0:
        r = 0.16
        circulo = (T.ring(r, 0.012, cx, cy, 0.4) + T.ring(r * 0.7, 0.01, cx, cy, 0.4)) * kc
        runas = [(cx + math.cos(a + t * 6) * r * 0.85 * 0.4, cy + math.sin(a + t * 6) * r * 0.85, 0.7) for a in np.linspace(0, TAU, 9)[:-1]]
        circulo += T.splats(runas, 0.01) * kc
    p = ease_out(rel(t, 0.14, 0.22), 2)
    raio = T.zero()
    if p > 0:
        k = 1 - rel(t, 0.36, 0.48)
        x = cx + (0.0 - cx) * p
        raio = (T.lines([(cx, cy, x, 0.0, 1.0)], 0.035) + T.lines([(cx, cy, x, 0.0, 1.0)], 0.012)) * k
    est = _estrela_de_contato(T, t, 0.22, 0.2, 4, 0.25)
    G += (circulo * 1.2 + T.glow(raio, 1.0, 0.7, 0.02) + est) * env
    H += (circulo * 0.8 + raio * 1.5 + est) * env
    return G, H


# ------------------------------------------------------------------ Gambit
def bastao_cinetico_gambit(T, t, rng):
    """Gambit: o bastão retrátil gira na mão já brilhando com a energia cinética rosa, bate no alvo e a energia
    explode em faíscas e no anel."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    gira = ease_out(rel(t, 0.0, 0.22), 1.5) * TAU * 1.5
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.26, 0.36))
    cx = -0.45 + 0.3 * ease_in(rel(t, 0.0, 0.22), 1.5)
    bastao = T.lines([(cx - math.cos(gira) * 0.32, -math.sin(gira) * 0.32, cx + math.cos(gira) * 0.32, math.sin(gira) * 0.32, 1.0)], 0.035) * vis
    brilho = T.ring(0.32, 0.02, cx, 0.0) * vis * 0.35 + T.gauss(cx + math.cos(gira) * 0.32, math.sin(gira) * 0.32, 0.04) * vis
    bum = T.polys([(estrela(0, 0, 0.3 * pulso(t, 0.22, 0.5) + 0.01, 0.2, 10, 0.4), 1.0)], 0.006) * pulso(t, 0.22, 0.5)
    faiscas = _riscos(T, t, 0.22, 0.32, 10, 0.12, 0.5, 0.018, 61, 0.0, TAU)
    anel = _anel(T, t, 0.22, 0.6, 0.1, 0.5, 0.05)
    G += (bastao * 1.1 + brilho + bum * 1.2 + faiscas + anel) * env
    H += (bastao * 0.6 + brilho * 0.8 + bum + faiscas * 0.8 + anel * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Aang
def bastao_de_ar_aang(T, t, rng):
    """Aang: o bastão de dobra de ar gira e solta um redemoinho de vento em espiral, com as setas azuis do vento
    empurrando o alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    a = t * 25
    kb = janela(t, 0.0, 0.05) * (1 - rel(t, 0.24, 0.34))
    bastao = T.lines([(-0.7 - math.cos(a) * 0.25, -math.sin(a) * 0.25, -0.7 + math.cos(a) * 0.25, math.sin(a) * 0.25, 1.0)], 0.03) * kb
    redemoinho = T.zero()
    kr = pulso(t, 0.08, 0.6)
    if kr > 0:
        for j in range(3):
            pts = [(-0.3 + 0.35 * s * rel(t, 0.08, 0.3) + math.cos(s * 10 + t * 20 + j * 2) * 0.12 * (1 - s * 0.5),
                    math.sin(s * 10 + t * 20 + j * 2) * 0.12 * (1 - s * 0.5)) for s in np.linspace(0, 1, 30)]
            redemoinho += T.polyline(pts, 0.02)
        redemoinho *= kr
    setas = T.zero()
    for j in range(3):
        u = rel(t, 0.2 + 0.04 * j, 0.55 + 0.04 * j)
        if 0 < u < 1:
            x, y = -0.1 + 0.5 * u, -0.2 + 0.2 * j
            setas += T.polyline([(x - 0.08, y - 0.06), (x, y), (x - 0.08, y + 0.06)], 0.02) * (1 - u)
    G += (bastao + redemoinho * 1.1 + setas) * env
    H += (bastao * 0.5 + redemoinho * 0.6 + setas * 0.7) * env
    return G, H


# ------------------------------------------------------------------ Pernalonga
def cenoura_do_pernalonga(T, t, rng):
    """Pernalonga: a cenoura vem numa pancada de desenho (bonk!) e ele dá uma mordida nela no fim (o "nhac" com os
    pedacinhos voando)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = ease_in(rel(t, 0.0, 0.18), 1.5)
    px = -0.85 + 0.75 * u
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.5, 0.62))
    cenoura = T.polys([([(px + 0.12, 0.0), (px - 0.25, -0.07), (px - 0.25, 0.07)], 1.0)], 0.003) * vis
    folhas = T.lines([(px - 0.25, 0.0, px - 0.38, -0.08, 1), (px - 0.25, 0.0, px - 0.4, 0.0, 1), (px - 0.25, 0.0, px - 0.38, 0.08, 1)], 0.018) * vis
    bonk = T.polys([(estrela(0.05, 0, 0.2 * pulso(t, 0.18, 0.4) + 0.01, 0.4, 7, 0.5), 1.0)], 0.004) * pulso(t, 0.18, 0.4)
    pedacos = _gotas(T, t, 0.42, 0.4, 7, 89, tam=0.018, cai=0.6, alcance=0.25)
    G += (cenoura * 1.1 + folhas + bonk * 1.2 + pedacos) * env
    H += (cenoura * 0.5 + folhas * 0.4 + bonk + pedacos * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Salsicha
def tapas_desesperados(T, t, rng):
    """Salsicha: os braços se agitam em pânico, uma chuva de tapinhas sem mira, e as gotas de suor voam para todo
    lado (Zoinks!)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    tapas = T.zero()
    for j in range(6):
        t0 = 0.02 + 0.05 * j
        k = pulso(t, t0, t0 + 0.09)
        if k > 0:
            a = j * 2.3
            x, y = 0.2 * math.cos(a), 0.2 * math.sin(a)
            tapas += T.polys([(_elipse_pts(x, y, 0.13, 0.1, a, 14), 1.0)], 0.004) * k
            tapas += T.polys([(estrela(x, y, 0.15 * k, a, 6, 0.45), 1.0)], 0.002) * k
    suor = _gotas(T, t, 0.05, 0.5, 14, 101, tam=0.022, cai=0.6, alcance=0.55, a0=-3.1, a1=0.0)
    G += (tapas * 1.1 + suor * 1.1) * env
    H += (tapas * 0.7 + suor * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Pateta
def trombada_do_pateta(T, t, rng):
    """Pateta: ele vem tropeçando e dá uma trombada desastrada com o corpo todo, e as estrelinhas giram em volta do
    alvo (e o chapéu sai voando)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = ease_in(rel(t, 0.0, 0.2), 1.8)
    px = -0.9 + 0.75 * u
    py = 0.05 * math.sin(t * 40) * (1 - u)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.25, 0.35))
    corpo = T.polys([(_elipse_pts(px, py, 0.18, 0.24, 0.3 * math.sin(t * 30), 18), 1.0)], 0.008) * vis
    bum = T.polys([(estrela(0, 0, 0.32 * pulso(t, 0.2, 0.45) + 0.01, 0.2, 9, 0.45), 1.0)], 0.006) * pulso(t, 0.2, 0.45)
    estrelinhas = T.zero()
    kk = pulso(t, 0.25, 0.85)
    if kk > 0:
        for j in range(4):
            a = t * 9 + j * TAU / 4
            estrelinhas += T.polys([(estrela(math.cos(a) * 0.22, -0.35 + math.sin(a) * 0.07, 0.04, a, 5, 0.45), 1.0)], 0.002)
        estrelinhas *= kk
    chapeu = T.zero()
    uc = rel(t, 0.2, 0.75)
    if 0 < uc < 1:
        cx, cy = 0.1 + 0.3 * uc, -0.3 - 0.4 * uc + 0.5 * uc * uc
        chapeu = T.polys([([(cx - 0.08, cy + 0.04), (cx, cy - 0.12), (cx + 0.08, cy + 0.04)], 1.0)], 0.004) * (1 - uc)
    G += (corpo * 0.9 + bum * 1.2 + estrelinhas * 1.2 + chapeu) * env
    H += (corpo * 0.3 + bum + estrelinhas + chapeu * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Yugi
def carta_do_rei_dos_jogos(T, t, rng):
    """Yugi: a carta voa girando e crava no alvo, e o Olho de Hórus do Enigma do Milênio acende dourado por um
    instante atrás dela."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = rel(t, 0.0, 0.18)
    carta = T.zero()
    if u < 1 or t < 0.45:
        x = -0.85 + 0.85 * ease_in(min(u, 1), 1.2)
        gira = math.cos(t * 30) if u < 1 else 1.0
        corpo, linhas = _desenha_carta(T, x, 0.0, max(0.15, abs(gira)), 0.0, 0.32, 0.22)
        carta = (corpo + linhas) * (1 - rel(t, 0.35, 0.45))
    ko = pulso(t, 0.18, 0.62)
    olho = T.zero()
    if ko > 0:
        s = 0.28 * back(rel(t, 0.18, 0.3), 1.8)
        olho = T.polys([(_elipse_pts(0, -0.05, s, s * 0.62, 0.0, 24), 1.0)], 0.004) - T.polys([(_elipse_pts(0, -0.05, s * 0.78, s * 0.42, 0.0, 24), 1.0)], 0.004)
        olho = np.clip(olho, 0, 1) + T.polys([(_elipse_pts(0, -0.05, s * 0.28, s * 0.28, 0.0, 16), 1.0)], 0.003)
        olho += T.lines([(0, s * 0.35, 0, s * 0.9, 1), (0.1 * s, s * 0.35, 0.4 * s, s * 0.8, 1)], 0.016)
        olho = olho * ko
    G += (carta * 1.1 + olho * 1.2) * env
    H += (carta * 0.6 + olho * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Kaiba
def carta_do_dragao_branco(T, t, rng):
    """Kaiba: a carta é lançada com força, e no acerto o brilho azul-branco do Dragão Branco de Olhos Azuis abre como
    asas de luz atrás do alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = rel(t, 0.0, 0.14)
    carta = T.zero()
    if t < 0.4:
        x = -0.85 + 0.85 * ease_in(min(u, 1), 1.4)
        corpo, linhas = _desenha_carta(T, x, 0.0, 1.0, 0.25 * (1 - min(u, 1)), 0.32, 0.22)
        carta = (corpo + linhas) * (1 - rel(t, 0.3, 0.4))
    ka = pulso(t, 0.14, 0.7)
    asas = T.zero()
    if ka > 0:
        abre = ease_out(rel(t, 0.14, 0.4), 2)
        for lado in (-1, 1):
            pts = [(0, 0), (lado * 0.25 * abre, -0.35 * abre), (lado * 0.55 * abre, -0.3 * abre), (lado * 0.4 * abre, -0.1 * abre),
                   (lado * 0.6 * abre, 0.0), (lado * 0.35 * abre, 0.08 * abre)]
            asas += T.polys([(pts, 1.0)], 0.01)
        asas *= ka
    est = _estrela_de_contato(T, t, 0.14, 0.22, 4, 0.3)
    G += (carta * 1.1 + asas * 0.9 + est) * env
    H += (carta * 0.6 + asas * 0.5 + est) * env
    return G, H


REGISTRO = [
    ("zoltraak_frieren", zoltraak_frieren, GRANDE, "básico da Frieren: o círculo mágico e o raio da Zoltraak", False),
    ("bastao_cinetico_gambit", bastao_cinetico_gambit, GRANDE, "básico do Gambit: o bastão com energia cinética", False),
    ("bastao_de_ar_aang", bastao_de_ar_aang, GRANDE, "básico do Aang: o bastão e o redemoinho de ar", False),
    ("cenoura_do_pernalonga", cenoura_do_pernalonga, GRANDE, "básico do Pernalonga: a cenoura e a mordida", False),
    ("tapas_desesperados", tapas_desesperados, GRANDE, "básico do Salsicha: os tapas em pânico e o suor", False),
    ("trombada_do_pateta", trombada_do_pateta, GRANDE, "básico do Pateta: a trombada e as estrelinhas", False),
    ("carta_do_rei_dos_jogos", carta_do_rei_dos_jogos, GRANDE, "básico do Yugi: a carta e o Olho de Hórus", False),
    ("carta_do_dragao_branco", carta_do_dragao_branco, GRANDE, "básico do Kaiba: a carta e as asas do Dragão Branco", False),
]
