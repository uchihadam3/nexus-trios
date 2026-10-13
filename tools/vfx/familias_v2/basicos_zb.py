"""Ataques básicos com animação própria, lote zb: Invencível, Raphael, Pica-Pau, Ben 10, He-Man, Popeye, Bob Esponja e
Megatron.

Golpes simples, cada um do personagem: o Invencível chegando voando num soco com o cone de estrondo sônico, o punho de
três dedos do Raphael segurando o sai pelo cabo, o tapa de desenho do Pica-Pau que deixa a marca da mão, o soco do
Ben 10 com o Omnitrix piscando verde no pulso, o soco do He-Man com a braçadeira de Eternia e os raios de poder, o
antebraço gigante do Popeye com a âncora tatuada girando no soco, o soquinho quadrado e furadinho do Bob Esponja com
as bolhas, e o punho enorme de metal do Megatron com as placas pontudas e o brilho de energon.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, janela, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_u import _anel, _antebraco, _estrela_de_contato, _mao, _pts, _riscos, _vai_e_volta
from .basicos_w import _soco
from .basicos_x import _gotas


# ------------------------------------------------------------------ Invencível
def soco_do_invencivel(T, t, rng):
    """Invencível: ele chega voando rápido demais, o punho na frente, e o cone do estrondo sônico se abre atrás no
    instante do soco; o alvo leva o impacto com respingos."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.16, 0.2, 1.1, 'luva', faixa=(0.0, 0.1))
    cone = T.zero()
    kc = pulso(t, 0.08, 0.36)
    if kc > 0:
        for k in range(3):
            r = 0.2 + 0.1 * k + 0.25 * rel(t, 0.08, 0.36)
            cone += T.arc_band(r, 0.025, 2.3, 4.0, 1.0, 0.0, px - 0.2, 0.0, 1.0, True)
        cone *= kc
    rastro = T.zero()
    if vis > 0.05:
        rastro = T.tapered([(px - 1.2, 0.0, px - 0.3, 0.0, 1.0)], 0.14) * (1 - rel(t, 0.12, 0.26)) * 0.6
    t0 = 0.16
    respingo = _gotas(T, t, t0, 0.5, 12, 8, tam=0.03, cai=0.5, alcance=0.55, a0=-1.2, a1=1.2)
    est = _estrela_de_contato(T, t, t0, 0.34, 8, 0.34, 0.1, 0.3)
    onda = _anel(T, t, t0, t0 + 0.4, 0.12, 0.6, 0.05, 1.2)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + cone * 1.3 + rastro + respingo * 1.3 + est + onda) * env
    H += (corpo * 0.3 + (d + B) * 0.8 + cone * 0.7 + rastro * 0.4 + respingo * 0.3 + est * 0.9 + onda * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Raphael
def soco_de_sai_raphael(T, t, rng):
    """Raphael: o punho verde de três dedos fechado no cabo do sai (as duas pontas laterais e a lâmina para trás
    aparecem) acerta com o cabo, num soco bravo com riscos de raiva."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    px = _vai_e_volta(t, 0.2, recua=0.2)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.46, 0.62))
    e = 1.1
    punho = T.polys([(_elipse_pts(px, 0.0, 0.13 * e, 0.15 * e, 0.0, 18), 1.0)] +
                    [(_elipse_pts(px + 0.1 * e, (-0.09 + 0.09 * k) * e, 0.07 * e, 0.045 * e, 0.0, 12), 1.0) for k in range(3)], 0.003)
    sai = T.polys([([(px - 0.05, -0.02), (px - 0.6, -0.015), (px - 0.62, 0.0), (px - 0.6, 0.015), (px - 0.05, 0.02)], 1.0)], 0.003)
    guarda = T.polyline([(px - 0.02, -0.26), (px - 0.12, -0.18), (px - 0.12, 0.18), (px - 0.02, 0.26)], 0.022)
    corpo = np.clip(punho + sai, 0, 1) * vis
    faixa = T.polyline([(px - 0.14, -0.14), (px - 0.14, 0.14)], 0.035) * vis
    t0 = 0.2
    raiva = _riscos(T, t, t0, 0.32, 8, 0.2, 0.5, 0.026, 31, 0.0, TAU)
    est = _estrela_de_contato(T, t, t0, 0.3, 6, 0.3, 0.3, 0.28)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + guarda * vis * 1.2 + raiva * 1.2 + est) * env
    H += (corpo * 0.3 + faixa * 0.9 + guarda * vis * 0.8 + raiva * 0.8 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Pica-Pau
_MAO_ABERTA = [(-0.12, -0.1), (0.06, -0.12), (0.1, -0.22), (0.15, -0.21), (0.14, -0.1), (0.22, -0.13), (0.25, -0.09),
               (0.18, -0.03), (0.27, -0.02), (0.27, 0.03), (0.18, 0.05), (0.24, 0.1), (0.2, 0.14), (0.06, 0.1), (-0.12, 0.1)]


def tapa_do_picapau(T, t, rng):
    """Pica-Pau: a mão de desenho vem aberta num tapa estalado e, quando sai, fica a marca vermelha da mão no alvo,
    com estrelinhas e passarinhos rodando em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    u = ease_in(rel(t, 0.0, 0.16), 1.5)
    px = -0.95 + 0.85 * u - 0.6 * ease_in(rel(t, 0.26, 0.42), 1.5)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.38, 0.46))
    mao = T.polys([(_pts(_MAO_ABERTA, px, 0.0, 1.3), 1.0)], 0.003) * vis
    t0 = 0.16
    km = janela(t, t0 + 0.08, t0 + 0.12) * apaga(t, 0.65, 0.88)
    marca = T.zero()
    if km > 0:
        cheio = T.polys([(_pts(_MAO_ABERTA, 0.0, 0.0, 1.0, 0.0), 1.0)], 0.003)
        marca = np.clip(cheio - T.blur(cheio, 0.012) * 0.6, 0, 1) * km
    gira = T.zero()
    kg = janela(t, t0 + 0.1, t0 + 0.16) * apaga(t, 0.7, 0.9)
    if kg > 0:
        for k in range(4):
            a = t * 9 + TAU * k / 4
            gira += T.polys([(estrela(0.3 * math.cos(a), -0.35 + 0.08 * math.sin(a), 0.05, a, 5, 0.45), 1.0)], 0.002)
        gira *= kg
    estalo = _estrela_de_contato(T, t, t0, 0.3, 8, 0.35, 0.0, 0.22)
    G += (mao * 1.1 + T.blur(mao, 0.02) * 0.35 + marca * 1.3 + gira * 1.3 + estalo) * env
    H += (mao * 0.4 + marca * 0.6 + gira * 1.0 + estalo) * env
    return G, H


# ------------------------------------------------------------------ Ben 10
def soco_do_omnitrix(T, t, rng):
    """Ben 10: o soco de garoto com o Omnitrix no pulso (o mostrador redondo com a ampulheta) piscando verde no
    caminho, e o acerto com um estalo verde de energia alienígena."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.2, 0.18, 1.05)
    cx = px - 0.2
    relogio = T.zero()
    if vis > 0.05:
        relogio = T.polys([(_elipse_pts(cx, 0.0, 0.08, 0.11, 0.0, 18), 1.0)], 0.003) * vis
    pisca = (0.6 + 0.4 * math.sin(t * 40)) * vis
    ampulheta = T.polys([([(cx - 0.035, -0.07), (cx + 0.035, -0.07), (cx, 0.0)], 1.0), ([(cx - 0.035, 0.07), (cx + 0.035, 0.07), (cx, 0.0)], 1.0)], 0.002) * pisca
    t0 = 0.2
    verde = T.zero()
    kv = pulso(t, t0, t0 + 0.4)
    if kv > 0:
        for j in range(5):
            a = TAU * j / 5 + 0.3
            verde += T.polyline(jagged(np.random.default_rng(int(t * 25) + j), 0.05 * math.cos(a), 0.05 * math.sin(a), 0.4 * math.cos(a), 0.4 * math.sin(a), 3, 0.2), 0.02)
        verde *= kv
    est = _estrela_de_contato(T, t, t0, 0.28, 8, 0.38)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + relogio * 1.2 + verde * 1.4 + est) * env
    H += (corpo * 0.3 + d * 0.8 + ampulheta * 2.0 + T.gauss(cx, 0.0, 0.05) * pisca * 1.2 + verde * 1.0 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ He-Man
def soco_de_eternia(T, t, rng):
    """He-Man: o braço musculoso com a braçadeira de Eternia (as tachas) vem num soco largo; o poder de Grayskull
    brilha em raios atrás do punho e o acerto abre um sol de raios dourados."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.22, 0.16, 1.2, comp=0.5, larg=0.13, faixa=(0.3, 0.14))
    tachas = T.zero()
    if vis > 0.05:
        x0 = px - (0.08 + 0.3 * 0.42) * 1.2 - 0.07
        tachas = sum(T.gauss(x0, y, 0.016) for y in (-0.1, 0.0, 0.1)) * vis
    raios_atras = T.zero()
    kr = pulso(t, 0.05, 0.3) * vis
    if kr > 0:
        for j in range(6):
            a = math.pi + (j - 2.5) * 0.25
            raios_atras += T.tapered([(px - 0.25 + 0.5 * math.cos(a), 0.5 * math.sin(a), px - 0.25 + 0.15 * math.cos(a), 0.15 * math.sin(a), 1.0)], 0.03)
        raios_atras *= kr
    t0 = 0.22
    sol = T.zero()
    ks = pulso(t, t0, t0 + 0.45)
    if ks > 0:
        segs = []
        for j in range(12):
            a = TAU * j / 12 + t
            comp = 0.4 + 0.12 * (j % 2)
            segs.append((0.1 * math.cos(a), 0.1 * math.sin(a), comp * math.cos(a), comp * math.sin(a), 1.0))
        sol = T.tapered([(x2, y2, x1, y1, w) for x1, y1, x2, y2, w in segs], 0.05) * ks
    clarao = T.gauss(0, 0, 0.18) * pulso(t, t0, t0 + 0.2) * 2.0
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + raios_atras * 1.2 + sol * 1.3 + clarao) * env
    H += (corpo * 0.3 + (d + B) * 0.7 + tachas * 1.6 + raios_atras * 0.6 + sol * 0.7 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Popeye
_ANCORA = [(0.0, -0.3), (0.0, 0.22)]


def soco_da_ancora_popeye(T, t, rng):
    """Popeye: o antebraço gigante (bem mais largo que o punho) com a âncora tatuada vem num soco girado, de moinho, e
    o acerto solta estrelas de desenho e um anel cheio."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = ease_in(rel(t, 0.0, 0.24), 1.6)
    ang = -1.6 * (1 - u)
    raio = 0.5 * (1 - u)
    px = -0.15 - 0.5 * (1 - u) + raio * math.cos(ang) * 0.3 - 0.18 * ease_out(rel(t, 0.32, 0.62), 2)
    py = raio * math.sin(ang)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.5, 0.66))
    M, d = _mao(T, px, py, 0.95)
    braco = T.polys([(_pts([(-0.1, -0.12), (-0.3, -0.24), (-0.58, -0.24), (-0.62, 0.0), (-0.58, 0.24), (-0.3, 0.24), (-0.1, 0.12)], px, py, 1.0), 0.85)], 0.004)
    corpo = np.clip(M + braco, 0, 1) * vis
    ax, ay = px - 0.38, py
    ancora = (T.polyline([(ax, ay - 0.13), (ax, ay + 0.1)], 0.016) + T.polyline([(ax - 0.07, ay - 0.07), (ax + 0.07, ay - 0.07)], 0.014)
              + T.arc_band(0.09, 0.016, 0.2, 2.94, 1.0, 0.0, ax, ay + 0.02, 1.0, False) + T.ring(0.025, 0.012, ax, ay - 0.16)) * vis
    t0 = 0.24
    estrelas = T.zero()
    ke = pulso(t, t0, t0 + 0.5)
    if ke > 0:
        for k in range(5):
            a = TAU * k / 5 + t * 4
            dd = 0.3 + 0.1 * rel(t, t0, t0 + 0.5)
            estrelas += T.polys([(estrela(dd * math.cos(a), dd * math.sin(a), 0.07, a, 5, 0.45), 1.0)], 0.002)
        estrelas *= ke
    est = _estrela_de_contato(T, t, t0, 0.34, 8, 0.36)
    onda = _anel(T, t, t0, t0 + 0.4, 0.12, 0.55, 0.06, 1.2)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + estrelas * 1.4 + est + onda) * env
    H += (corpo * 0.3 + d * vis * 0.7 + ancora * 1.4 + estrelas * 1.0 + est * 0.9 + onda * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Bob Esponja
def soquinho_de_esponja(T, t, rng):
    """Bob Esponja: o bracinho fino com o punho quadrado e cheio de furinhos dá um soquinho de karatê e o acerto solta
    um monte de bolhas redondas que sobem."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    px = _vai_e_volta(t, 0.2, -0.9, -0.14, 0.24)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.44, 0.6))
    quad = T.polys([([(px - 0.16, -0.19), (px + 0.18, -0.19), (px + 0.18, 0.19), (px - 0.16, 0.19)], 1.0)], 0.003)
    braco = T.polys([([(px - 0.12, -0.03), (px - 0.6, -0.03), (px - 0.6, 0.03), (px - 0.12, 0.03)], 0.9)], 0.003)
    corpo = np.clip(quad + braco, 0, 1) * vis
    furos = sum(T.gauss(px + dx, dy, 0.022) for dx, dy in [(-0.07, -0.1), (0.09, -0.06), (0.0, 0.09), (0.11, 0.11), (-0.09, 0.04)]) * vis
    t0 = 0.2
    u = rel(t, t0, t0 + 0.7)
    bolhas = T.zero()
    if 0 < u < 1:
        q = np.random.default_rng(87)
        for _ in range(10):
            a = q.uniform(-2.6, 0.4)
            dd = q.uniform(0.1, 0.4) * ease_out(min(1, u * 1.6), 2)
            r = q.uniform(0.03, 0.07)
            bolhas += T.ring(r, 0.012, dd * math.cos(a) + 0.04 * math.sin(u * 10 + a), dd * math.sin(a) - 0.4 * u) + T.gauss(dd * math.cos(a) - r * 0.4, dd * math.sin(a) - 0.4 * u - r * 0.4, r * 0.2) * 0.8
        bolhas *= (1 - u ** 2)
    est = _estrela_de_contato(T, t, t0, 0.24, 6, 0.4)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 - furos * 0.5 + bolhas * 1.4 + est) * env
    H += (corpo * 0.3 + bolhas * 0.9 + est * 0.9) * env
    return np.clip(G, 0, None), H


# ------------------------------------------------------------------ Megatron
def soco_decepticon(T, t, rng):
    """Megatron: o punho enorme de metal de Cybertron, em placas pontudas, vem pesado com o brilho de energon nas
    juntas; o acerto solta lascas pontudas de metal e faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    vem = ease_in(rel(t, 0.0, 0.26), 1.9)
    px = -1.0 + 0.86 * vem - 0.16 * ease_out(rel(t, 0.34, 0.66), 2)
    vis = janela(t, 0.0, 0.05) * (1 - rel(t, 0.52, 0.68))
    M, d = _mao(T, px, 0.0, 1.35, 'armadura')
    pontas = T.polys([([(px - 0.2, -0.2), (px - 0.12, -0.34), (px - 0.04, -0.2)], 1.0), ([(px - 0.4, -0.17), (px - 0.32, -0.3), (px - 0.24, -0.17)], 1.0)], 0.003)
    A = T.polys([([(px - 0.17, -0.17), (px - 0.65, -0.16), (px - 0.65, 0.16), (px - 0.17, 0.17)], 0.85)], 0.004)
    corpo = np.clip(M + pontas + A, 0, 1) * vis
    energon = sum(T.gauss(px + dx, dy, 0.022) for dx, dy in [(-0.3, 0.0), (-0.5, 0.0), (0.05, 0.0)]) * vis * (0.8 + 0.3 * math.sin(t * 30))
    t0 = 0.26
    u = rel(t, t0, t0 + 0.55)
    lascas = T.zero()
    if 0 < u < 1:
        q = np.random.default_rng(42)
        polys = []
        for _ in range(9):
            a = q.uniform(-2.5, 2.5)
            dd = q.uniform(0.2, 0.6) * ease_out(u, 1.7)
            polys.append((_pts([(-1, -0.25), (1, 0), (-1, 0.25)], dd * math.cos(a), dd * math.sin(a) + 0.35 * u * u, q.uniform(0.05, 0.08), a), 1 - u))
        lascas = T.polys(polys, 0.002)
    faiscas = _riscos(T, t, t0, 0.35, 10, 0.12, 0.5, 0.022, 67, 0.0, TAU)
    est = _estrela_de_contato(T, t, t0, 0.36, 6, 0.25, 0.0, 0.32)
    clarao = T.gauss(0, 0, 0.18) * pulso(t, t0, t0 + 0.2) * 2.0
    G += (corpo * 1.0 + T.blur(corpo, 0.025) * 0.4 + lascas * 1.4 + faiscas * 1.3 + est + clarao) * env
    H += (corpo * 0.25 + d * vis * 0.7 + energon * 1.8 + lascas * 0.8 + faiscas * 0.9 + est * 0.9 + clarao * 1.1) * env
    return G, H


REGISTRO = [
    ("soco_do_invencivel", soco_do_invencivel, GRANDE, "básico do Invencível: o soco voando e o cone do estrondo sônico", False),
    ("soco_de_sai_raphael", soco_de_sai_raphael, GRANDE, "básico do Raphael: o punho de três dedos com o sai", False),
    ("tapa_do_picapau", tapa_do_picapau, GRANDE, "básico do Pica-Pau: o tapa de desenho e a marca da mão", False),
    ("soco_do_omnitrix", soco_do_omnitrix, GRANDE, "básico do Ben 10: o Omnitrix piscando e o estalo verde", False),
    ("soco_de_eternia", soco_de_eternia, GRANDE, "básico do He-Man: a braçadeira de Eternia e o sol de raios", False),
    ("soco_da_ancora_popeye", soco_da_ancora_popeye, GRANDE, "básico do Popeye: o antebraço com a âncora e as estrelas", False),
    ("soquinho_de_esponja", soquinho_de_esponja, GRANDE, "básico do Bob Esponja: o punho quadrado furadinho e as bolhas", False),
    ("soco_decepticon", soco_decepticon, GRANDE, "básico do Megatron: o punho de metal pontudo e o energon", False),
]
