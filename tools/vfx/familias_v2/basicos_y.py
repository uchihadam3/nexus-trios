"""Ataques básicos com animação própria, lote y: Ultron, Duende Verde, Galactus, Groot, Aquaman, Lanterna Verde,
Ciborgue e Shazam.

Golpes simples, cada um do personagem: o punho cromado do Ultron com o núcleo vermelho e as trilhas de circuito
correndo no alvo, a luva roxa de barbatanas do Duende Verde com a fumaça verde, o punho gigante do Galactus com as
estrelas em volta, o punho de madeira do Groot soltando lascas e folhas, o soco do Aquaman com a água espirrando,
o anel do Lanterna Verde que vira uma luva gigante de luz, o braço cibernético do Ciborgue com os quadradinhos de
dado e o soco do Shazam com o raio do emblema.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, janela, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_u import _anel, _antebraco, _estrela_de_contato, _mao, _pts, _riscos, _vai_e_volta
from .basicos_w import _soco
from .basicos_x import _gotas


# ------------------------------------------------------------------ Ultron
def soco_de_metal_ultron(T, t, rng):
    """Ultron: o punho cromado em placas com o núcleo vermelho aceso no dorso; o acerto espalha trilhas de
    circuito em ângulos retos que correm pelo alvo e apagam."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.22, 0.16, 1.1, 'armadura')
    nucleo = T.gauss(px - 0.05, 0.0, 0.035) * vis * (1 + 0.3 * math.sin(t * 30))
    t0 = 0.22
    trilhas = T.zero()
    u = rel(t, t0, t0 + 0.45)
    if 0 < u < 1:
        q = np.random.default_rng(12)
        for k in range(7):
            a = TAU * k / 7 + 0.3
            x, y = 0.05 * math.cos(a), 0.05 * math.sin(a)
            pts = [(x, y)]
            for s in range(4):
                if s % 2 == 0:
                    x += math.copysign(q.uniform(0.08, 0.14), math.cos(a))
                else:
                    y += math.copysign(q.uniform(0.06, 0.12), math.sin(a))
                pts.append((x, y))
            n = max(2, int(len(pts) * min(1, u * 2.5)))
            trilhas += T.polyline(pts[:n], 0.016) + T.gauss(pts[n - 1][0], pts[n - 1][1], 0.02) * 1.5
        trilhas *= (1 - u)
    est = _estrela_de_contato(T, t, t0, 0.28, 6, 0.3, 0.0, 0.28)
    clarao = T.gauss(0, 0, 0.15) * pulso(t, t0, t0 + 0.16) * 2.0
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + trilhas * 1.4 + est + clarao + nucleo) * env
    H += (corpo * 0.35 + d * 0.8 + nucleo * 2.0 + trilhas * 1.0 + est * 0.9 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Duende Verde
def soco_do_duende(T, t, rng):
    """Duende Verde: a luva roxa com as barbatanas pontudas no punho vem num soco esquisito, girando um pouco, e o
    acerto solta uma baforada de fumaça verde com faíscas, como as bombas dele em miniatura."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    u = ease_in(rel(t, 0.0, 0.22), 1.6)
    px = -0.95 + 0.81 * u - 0.2 * ease_out(rel(t, 0.3, 0.62), 2)
    ang = 0.5 * (1 - u)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.48, 0.64))
    M, d = _mao(T, px, 0.0, 1.1, 'luva')
    A, _ = _antebraco(T, px, 0.0, 1.1, 0.44, 0.1)
    barbatanas = T.polys([(_pts([(-0.2, -0.16), (-0.32, -0.32), (-0.3, -0.15)], px, 0.0, 1.1, ang), 1.0),
                          (_pts([(-0.32, -0.15), (-0.44, -0.3), (-0.42, -0.14)], px, 0.0, 1.1, ang), 1.0)], 0.003)
    corpo = np.clip(M + A + barbatanas, 0, 1) * vis
    t0 = 0.22
    q = np.random.default_rng(5)
    fum = T.zero()
    vida = janela(t, t0, t0 + 0.05) * apaga(t, t0 + 0.22, 0.8)
    if vida > 0:
        cresce = ease_out(rel(t, t0, 0.9), 2)
        for k in range(8):
            a = q.uniform(0, TAU)
            dd = q.uniform(0.05, 0.3) * (0.5 + cresce)
            fum += T.gauss(dd * math.cos(a), dd * math.sin(a) - 0.1 * cresce, 0.08 + 0.06 * cresce)
        fum *= vida
    faiscas = _riscos(T, t, t0, 0.35, 10, 0.15, 0.5, 0.022, 9, 0.0, TAU)
    est = _estrela_de_contato(T, t, t0, 0.26, 7, 0.36, 0.3, 0.28)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + fum * 0.5 + faiscas * 1.3 + est) * env
    H += (corpo * 0.3 + d * vis * 0.6 + fum * 0.3 + faiscas * 0.9 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Galactus
def pancada_colossal_galactus(T, t, rng):
    """Galactus: um punho gigante, maior que o alvo, vem devagar com estrelinhas cósmicas cintilando em volta e
    esmaga com um anel largo de energia que leva poeira de estrela junto."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    vem = ease_in(rel(t, 0.0, 0.34), 2.2)
    px = -1.2 + 1.0 * vem - 0.18 * ease_out(rel(t, 0.42, 0.75), 2)
    vis = janela(t, 0.0, 0.06) * (1 - rel(t, 0.58, 0.74))
    M, d = _mao(T, px, 0.0, 1.9)
    A, B = _antebraco(T, px, 0.0, 1.9, 0.5, 0.12, (0.2, 0.08))
    corpo = np.clip(M + A, 0, 1) * vis
    estrelas = T.zero()
    q = np.random.default_rng(23)
    for k in range(10):
        x = px - 0.6 + q.uniform(-0.2, 0.6)
        y = q.uniform(-0.6, 0.6)
        brilho = max(0.0, math.sin(t * 20 + k * 1.7))
        estrelas += T.polys([(estrela(x, y, 0.065 * brilho + 0.005, 0.3, 4, 0.25), 1.0)], 0.002) * brilho
    estrelas *= vis
    t0 = 0.34
    onda = _anel(T, t, t0, t0 + 0.55, 0.2, 0.9, 0.09, 1.2)
    poeira = _gotas(T, t, t0, 0.55, 18, 27, tam=0.016, cai=0.0, alcance=0.8, a0=0.0, a1=TAU)
    clarao = T.gauss(0, 0, 0.26) * pulso(t, t0, t0 + 0.24) * 2.0
    G += (corpo * 1.0 + T.blur(corpo, 0.03) * 0.4 + estrelas * 1.4 + onda * 1.3 + poeira * 1.4 + clarao) * env
    H += (corpo * 0.25 + (d + B) * vis * 0.6 + estrelas * 1.6 + onda * 0.45 + poeira * 1.0 + clarao * 1.1) * env
    return G, H


# ------------------------------------------------------------------ Groot
def soco_de_madeira_groot(T, t, rng):
    """Groot: o punho de madeira, com os veios do tronco no braço, cresce um pouco no caminho (galhos esticando) e
    o acerto solta lascas de madeira e folhinhas que caem girando."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    u = ease_in(rel(t, 0.0, 0.24), 1.5)
    px = -0.95 + 0.82 * u - 0.18 * ease_out(rel(t, 0.32, 0.64), 2)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.5, 0.66))
    M, d = _mao(T, px, 0.0, 1.1)
    comp = 0.4 + 0.25 * u
    A, _ = _antebraco(T, px, 0.0, 1.1, comp, 0.11)
    corpo = np.clip(M + A, 0, 1) * vis
    veios = T.zero()
    if vis > 0.05:
        for k in range(3):
            y = -0.06 + 0.06 * k
            pts = [(px - 0.12 - s * comp * 1.0, y + 0.015 * math.sin(s * 14 + k)) for s in np.linspace(0, 0.9, 10)]
            veios += T.polyline(pts, 0.008)
        veios *= vis
    galho = T.zero()
    if vis > 0.05:
        galho = (T.polyline([(px - 0.3, -0.12), (px - 0.36, -0.25), (px - 0.3, -0.32)], 0.014)
                 + T.polys([(_elipse_pts(px - 0.29, -0.34, 0.045, 0.022, -0.6, 10), 1.0)], 0.002)) * vis
    t0 = 0.24
    u2 = rel(t, t0, t0 + 0.65)
    lascas = T.zero()
    folhas = T.zero()
    if 0 < u2 < 1:
        q = np.random.default_rng(81)
        segs, polys = [], []
        for _ in range(9):
            a = q.uniform(-2.4, 1.2)
            dd = q.uniform(0.2, 0.6) * ease_out(u2, 1.8)
            x, y = dd * math.cos(a), dd * math.sin(a) + 0.4 * u2 * u2
            rot = a + u2 * 6
            segs.append((x - 0.05 * math.cos(rot), y - 0.05 * math.sin(rot), x + 0.05 * math.cos(rot), y + 0.05 * math.sin(rot), 1 - u2))
        for _ in range(5):
            a = q.uniform(-2.6, -0.4)
            dd = q.uniform(0.25, 0.55) * ease_out(u2, 1.6)
            x, y = dd * math.cos(a) + 0.08 * math.sin(u2 * 9), dd * math.sin(a) + 0.5 * u2 * u2
            polys.append((_elipse_pts(x, y, 0.065, 0.03, u2 * 7 + a, 10), 1 - u2))
        lascas = T.tapered(segs, 0.022)
        folhas = T.polys(polys, 0.002)
    est = _estrela_de_contato(T, t, t0, 0.3, 7, 0.36, 0.2, 0.3)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + galho * 1.2 + lascas * 1.4 + folhas * 1.3 + est) * env
    H += (corpo * 0.25 + d * 0.5 + veios * 1.1 + galho * 0.6 + lascas * 0.8 + folhas * 0.7 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Aquaman
def soco_da_mare(T, t, rng):
    """Aquaman: o soco vem arrastando uma faixa de água que espirra e, no acerto, a água estoura em coroa
    (respingos subindo e caindo) com um anel de onda."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.22, 0.16, 1.1)
    rastro = T.zero()
    if vis > 0.05:
        pts = [(px - 0.2 - 0.7 * s, 0.04 * math.sin(s * 10 - t * 30)) for s in np.linspace(0, 1, 16)]
        rastro = T.polyline(pts, 0.06) * (1 - rel(t, 0.2, 0.36))
        rastro += _gotas(T, t, 0.05, 0.3, 8, 3, tam=0.02, cai=0.3, alcance=0.25, a0=2.3, a1=4.0) * 0.8
    t0 = 0.22
    coroa = T.zero()
    kc = pulso(t, t0, t0 + 0.45)
    if kc > 0:
        uu = rel(t, t0, t0 + 0.45)
        segs = []
        for j in range(9):
            a = -math.pi * (0.1 + 0.8 * j / 8)
            h = 0.5 * math.sin(math.pi * min(1, uu * 1.5))
            x0 = 0.32 * math.cos(a) * (0.6 + uu)
            segs.append((x0, 0.05, x0 * 1.1, 0.05 - h * (0.6 + 0.4 * math.sin(j)), 1.0))
        coroa = T.tapered(segs, 0.055) * kc
    respingos = _gotas(T, t, t0 + 0.05, 0.55, 14, 19, tam=0.028, cai=0.6, alcance=0.5, a0=-2.8, a1=-0.3)
    onda = _anel(T, t, t0, t0 + 0.5, 0.12, 0.62, 0.05, 1.8)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + rastro * 1.1 + coroa * 1.3 + respingos * 1.4 + onda * 1.2) * env
    H += (corpo * 0.3 + d * 0.8 + rastro * 0.5 + coroa * 0.8 + respingos * 0.8 + onda * 0.45) * env
    return G, H


# ------------------------------------------------------------------ Lanterna Verde
def soco_de_construto(T, t, rng):
    """Lanterna Verde: o anel no dedo acende e, em volta do punho, a luz desenha uma luva de boxe gigante (o
    construto, só o contorno brilhante) que acerta o alvo e se desfaz em fagulhas."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.24, 0.14, 1.0)
    anel = T.ring(0.035, 0.014, px + 0.09, -0.06) * vis * pulso(t, 0.0, 0.5) * 1.5
    luva = T.zero()
    forma = janela(t, 0.06, 0.18) * (1 - rel(t, 0.38, 0.5))
    if forma > 0:
        cx = px + 0.12
        luvag = [(_elipse_pts(cx, 0.0, 0.3, 0.26, 0.0, 24), 1.0), (_pts([(-0.2, -0.16), (-0.5, -0.14), (-0.5, 0.14), (-0.2, 0.16)], cx, 0.0, 1.0), 1.0),
                 (_elipse_pts(cx + 0.05, -0.24, 0.14, 0.07, -0.4, 16), 1.0)]
        cheio = T.polys(luvag, 0.004)
        luva = np.clip(T.blur(cheio, 0.012) * 2.2 - cheio * 1.5, 0, 1) * forma + cheio * forma * 0.18
    t0 = 0.24
    fagulhas = _riscos(T, t, t0 + 0.12, 0.4, 12, 0.2, 0.6, 0.022, 44, 0.0, TAU)
    est = _estrela_de_contato(T, t, t0, 0.34, 8, 0.4, 0.0, 0.32)
    clarao = T.gauss(0, 0, 0.18) * pulso(t, t0, t0 + 0.2) * 1.8
    G += (corpo * 0.9 + luva * 1.5 + T.blur(luva, 0.025) * 0.5 + anel + fagulhas * 1.2 + est + clarao) * env
    H += (corpo * 0.25 + d * 0.5 + luva * 0.8 + anel * 1.5 + fagulhas * 0.8 + est * 0.9 + clarao * 1.1) * env
    return G, H


# ------------------------------------------------------------------ Ciborgue
def soco_cibernetico(T, t, rng):
    """Ciborgue: o braço de metal com as linhas de circuito acesas e a luz azul nos nós dos dedos dá um soco seco;
    no acerto, quadradinhos de dado (pixels) saltam do alvo e se apagam."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.22, 0.16, 1.1, 'armadura')
    circuito = T.zero()
    if vis > 0.05:
        circuito = T.polyline([(px - 0.48, 0.06), (px - 0.36, 0.06), (px - 0.32, -0.05), (px - 0.2, -0.05), (px - 0.16, 0.04)], 0.012) * vis
    luz = T.gauss(px + 0.17, 0.0, 0.04, 0.12) * vis * pulso(t, 0.05, 0.4) * 1.6
    t0 = 0.22
    u = rel(t, t0, t0 + 0.55)
    pixels = T.zero()
    if 0 < u < 1:
        q = np.random.default_rng(37)
        polys = []
        for _ in range(14):
            a = q.uniform(-2.5, 2.5)
            dd = q.uniform(0.15, 0.6) * ease_out(u, 1.8)
            x, y = dd * math.cos(a), dd * math.sin(a)
            s = q.uniform(0.025, 0.045) * (1 - 0.5 * u)
            if q.uniform() < 0.8 or u < 0.5:
                polys.append(([(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)], 1 - u))
        pixels = T.polys(polys, 0.002)
    est = _estrela_de_contato(T, t, t0, 0.28, 4, 0.2, 0.785, 0.26)
    onda = _anel(T, t, t0, t0 + 0.4, 0.1, 0.5, 0.04, 1.0)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + pixels * 1.4 + est + onda + luz) * env
    H += (corpo * 0.3 + d * 0.8 + circuito * 1.4 + luz * 1.6 + pixels * 0.9 + est * 0.9 + onda * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Shazam
_RAIO = [(-0.05, -0.32), (0.12, -0.32), (0.02, -0.06), (0.14, -0.06), (-0.1, 0.34), (-0.02, 0.04), (-0.14, 0.04)]


def soco_relampago_shazam(T, t, rng):
    """Shazam: um soco cheio de herói e, no acerto, o raio do emblema dele estoura brilhante no ponto do golpe,
    com faíscas curtas saindo pelas pontas."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.2, 0.18, 1.1, 'luva', faixa=(0.0, 0.08))
    t0 = 0.2
    k = pulso(t, t0, t0 + 0.55)
    raio = T.zero()
    if k > 0:
        raio = T.polys([(_pts(_RAIO, 0.02, 0.0, 0.7 + 0.5 * k), 1.0)], 0.004) * k
    faiscas = T.zero()
    kf = pulso(t, t0, t0 + 0.32)
    if kf > 0:
        for (x, y, a) in [(0.08, -0.25, -1.2), (-0.08, 0.26, 2.0), (0.12, 0.0, 0.2)]:
            faiscas += T.polyline(jagged(np.random.default_rng(int(t * 30) + int(x * 100)), x, y, x + 0.25 * math.cos(a), y + 0.25 * math.sin(a), 3, 0.2), 0.018)
        faiscas *= kf
    onda = _anel(T, t, t0, t0 + 0.42, 0.12, 0.58, 0.045, 1.2)
    clarao = T.gauss(0, 0, 0.17) * pulso(t, t0, t0 + 0.18) * 2.0
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + raio * 1.3 + T.blur(raio, 0.03) * 0.6 + faiscas * 1.4 + onda + clarao) * env
    H += (corpo * 0.3 + (d + B) * 0.8 + raio * 1.1 + faiscas * 1.0 + onda * 0.4 + clarao * 1.2) * env
    return G, H


REGISTRO = [
    ("soco_de_metal_ultron", soco_de_metal_ultron, GRANDE, "básico do Ultron: punho cromado, núcleo vermelho e trilhas de circuito", False),
    ("soco_do_duende", soco_do_duende, GRANDE, "básico do Duende Verde: luva de barbatanas e fumaça verde", False),
    ("pancada_colossal_galactus", pancada_colossal_galactus, GRANDE, "básico do Galactus: punho gigante e estrelas cósmicas", False),
    ("soco_de_madeira_groot", soco_de_madeira_groot, GRANDE, "básico do Groot: punho de madeira, lascas e folhas", False),
    ("soco_da_mare", soco_da_mare, GRANDE, "básico do Aquaman: a faixa de água e a coroa de respingos", False),
    ("soco_de_construto", soco_de_construto, GRANDE, "básico do Lanterna Verde: a luva gigante de luz do anel", False),
    ("soco_cibernetico", soco_cibernetico, GRANDE, "básico do Ciborgue: braço de circuito e os pixels saltando", False),
    ("soco_relampago_shazam", soco_relampago_shazam, GRANDE, "básico do Shazam: o soco e o raio do emblema", False),
]
