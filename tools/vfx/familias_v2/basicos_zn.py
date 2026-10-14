"""Ataques básicos com animação própria, lote zn: Donkey Kong, Omni-Man, Mulher-Elástica, Mumm-Ra, Kakashi, Rukia,
Surfista Prateado, Coragem e Papa-Léguas.

O último lote dos básicos repetidos: o tapão de gorila com a banana voando do Donkey Kong, a pancada viltrumita que
racha o ar do Omni-Man, o braço que estica em mola da Mulher-Elástica, o raio vermelho do ankh do Mumm-Ra, a kunai
com o Sharingan girando do Kakashi, a dança da lua branca da Rukia que congela o chão, o raio cósmico da prancha do
Surfista Prateado, a mordida tremendo de medo do Coragem e a poeira do "bip-bip" do Papa-Léguas.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, vazio
from .basicos_a import _elipse_pts, _zigue
from .basicos_u import _anel, _estrela_de_contato, _riscos
from .basicos_w import _soco
from .basicos_x import _gotas
from .basicos_zl import _feixe


# ------------------------------------------------------------------ Donkey Kong
def tapa_de_gorila_dk(T, t, rng):
    """Donkey Kong: a mão enorme de gorila desce num tapão de cima, o chão treme em ondas, e uma banana sai voando
    girando."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    u = ease_in(rel(t, 0.0, 0.2), 1.6)
    py = -0.8 + 0.75 * u
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.36, 0.48))
    mao = T.polys([(_elipse_pts(0.0, py, 0.3, 0.16, 0.0, 22), 1.0)] + [(_elipse_pts(-0.2 + 0.13 * k, py + 0.14, 0.05, 0.07, 0.0, 10), 1.0) for k in range(4)], 0.005) * vis
    ondas = _anel(T, t, 0.2, 0.55, 0.1, 0.6, 0.05, 2.5, 0.0, 0.1) + _anel(T, t, 0.28, 0.65, 0.1, 0.5, 0.04, 2.5, 0.0, 0.1)
    ub = rel(t, 0.22, 0.85)
    banana = T.zero()
    if 0 < ub < 1:
        cx, cy = 0.2 + 0.35 * ub, -0.1 - 0.6 * ub + 0.6 * ub * ub
        banana = T.arc_band(0.09, 0.035, 0.3 + ub * 10, 2.4 + ub * 10, cx=cx, cy=cy, crescente=True) * (1 - ub)
    est = _estrela_de_contato(T, t, 0.2, 0.3, 8, 0.32)
    G += (mao * 1.0 + ondas + banana * 1.4 + est) * env
    H += (mao * 0.4 + ondas * 0.5 + banana + est) * env
    return G, H


# ------------------------------------------------------------------ Omni-Man
def pancada_viltrumita(T, t, rng):
    """Omni-Man: um soco tão forte que o ar racha em volta do punho (o anel de choque supersônico) antes mesmo de
    acertar, e o acerto espirra sangue."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.16, 0.2, 1.2, 'nu')
    cone = T.zero()
    kc = janela(t, 0.04, 0.08) * (1 - rel(t, 0.16, 0.22))
    if kc > 0:
        cone = T.ring(0.16, 0.025, px + 0.1, 0.0, 0.45) * kc + T.ring(0.24, 0.015, px - 0.05, 0.0, 0.45) * kc * 0.6
    onda = _anel(T, t, 0.16, 0.55, 0.12, 0.7, 0.07)
    sangue = _gotas(T, t, 0.16, 0.5, 16, 131, tam=0.026, cai=0.6, alcance=0.55, a0=-1.2, a1=1.2)
    est = _estrela_de_contato(T, t, 0.16, 0.34, 10, 0.3)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.4 + cone * 1.2 + onda + sangue + est) * env
    H += (corpo * 0.3 + (d + B) * 0.7 + cone + onda * 0.5 + sangue * 0.3 + est) * env
    return G, H


# ------------------------------------------------------------------ Mulher-Elástica
def tapa_elastico(T, t, rng):
    """Mulher-Elástica: o braço estica como uma mola comprida, ondulando, dá o tapa e volta encolhendo num "boing"."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    vai = ease_out(rel(t, 0.0, 0.16), 2)
    volta = ease_in(rel(t, 0.3, 0.5), 1.6)
    alc = vai * (1 - volta)
    braco = T.zero()
    mao = T.zero()
    if alc > 0.02:
        x1 = -0.95 + 0.95 * alc
        pts = [(-0.95 + (x1 + 0.95) * s, 0.06 * math.sin(s * 14 + t * 30) * (1 - alc * 0.6)) for s in np.linspace(0, 1, 30)]
        braco = T.polyline(pts, 0.05)
        mao = T.polys([(_elipse_pts(x1, 0.0, 0.08, 0.1, 0.0, 14), 1.0)], 0.004)
    tapa = T.polys([(estrela(0.0, 0.0, 0.2 * pulso(t, 0.16, 0.38) + 0.01, 0.4, 7, 0.5), 1.0)], 0.004) * pulso(t, 0.16, 0.38)
    boing = T.zero()
    kb = pulso(t, 0.45, 0.7)
    if kb > 0:
        boing = T.polyline([(-0.85 + 0.03 * math.sin(s * 25), -0.2 + 0.4 * s) for s in np.linspace(0, 1, 20)], 0.015) * kb
    G += (braco * 1.0 + mao * 1.1 + tapa * 1.2 + boing) * env
    H += (braco * 0.4 + mao * 0.6 + tapa + boing * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Mumm-Ra
def raio_do_ankh(T, t, rng):
    """Mumm-Ra: o ankh (a cruz egípcia com a alça) aparece brilhando em vermelho-escuro, e dele sai o raio das trevas
    retorcido até o alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    ka = janela(t, 0.0, 0.08) * (1 - rel(t, 0.4, 0.55))
    cx, cy = -0.75, -0.05
    ankh = (T.ring(0.07, 0.018, cx, cy - 0.1, 0.8) + T.lines([(cx, cy - 0.03, cx, cy + 0.22, 1.0), (cx - 0.09, cy + 0.03, cx + 0.09, cy + 0.03, 1.0)], 0.025)) * ka
    raio = T.zero()
    kr = rel(t, 0.12, 0.22)
    if kr > 0 and t < 0.5:
        x1 = cx + (0.0 - cx) * ease_out(kr, 2)
        raio = T.polyline(_zigue(cx + 0.05, cy, x1, 0.0, 8, 0.05, math.sin(t * 40)), 0.03) * (1 - rel(t, 0.38, 0.5))
    trevas = T.gauss(0, 0, 0.18) * pulso(t, 0.22, 0.6) * 0.8
    G += (ankh * 1.2 + raio * 1.2 + trevas) * env
    H += (ankh * 0.9 + raio * 0.8 + trevas * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Kakashi
def kunai_do_sharingan(T, t, rng):
    """Kakashi: o Sharingan gira (as três vírgulas em volta da pupila) e a kunai voa direto no ponto que ele já leu."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    ko = janela(t, 0.0, 0.06) * (1 - rel(t, 0.3, 0.42))
    cx, cy = -0.7, -0.5
    olho = T.zero()
    if ko > 0:
        olho = T.ring(0.16, 0.02, cx, cy) * ko + T.gauss(cx, cy, 0.04) * ko
        for k in range(3):
            a = t * 12 + k * TAU / 3
            olho += T.polys([(_elipse_pts(cx + math.cos(a) * 0.1, cy + math.sin(a) * 0.1, 0.035, 0.024, a + 1.2, 8), 1.0)], 0.002) * ko
    u = rel(t, 0.12, 0.26)
    kunai = T.zero()
    if 0 < u < 1 or (1 <= u and t < 0.5):
        x = -0.85 + 0.85 * ease_in(min(u, 1), 1.3)
        kunai = (T.polys([([(x + 0.22, 0.0), (x - 0.03, -0.07), (x - 0.03, 0.07)], 1.0)], 0.002) + T.lines([(x - 0.03, 0, x - 0.25, 0, 1)], 0.025)
                 + T.ring(0.045, 0.013, x - 0.3, 0.0) + T.tapered([(x - 0.6, 0.0, x - 0.3, 0.0, 0.6)], 0.04)) * (1 - rel(t, 0.38, 0.5))
    est = _estrela_de_contato(T, t, 0.26, 0.2, 6, 0.3)
    G += (olho * 1.2 + kunai * 1.2 + est) * env
    H += (olho * 1.0 + kunai * 0.9 + est) * env
    return G, H


# ------------------------------------------------------------------ Rukia
def danca_da_lua_branca(T, t, rng):
    """Rukia: a Sode no Shirayuki desenha um círculo no chão em volta do alvo e uma coluna de gelo branco sobe dele
    (a primeira dança, Tsukishiro)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    p = ease_out(rel(t, 0.0, 0.2), 2)
    circulo = T.arc_band(0.38, 0.03, -1.6, -1.6 + TAU * p + 0.01, squash=0.35, cy=0.3) * (1 - rel(t, 0.55, 0.75))
    kc = rel(t, 0.2, 0.34)
    coluna = T.zero()
    if kc > 0:
        alt = 0.9 * ease_out(kc, 2)
        coluna = T.polys([([(-0.3, 0.3), (-0.26, 0.3 - alt), (0.26, 0.3 - alt), (0.3, 0.3)], 1.0)], 0.02) * (1 - rel(t, 0.55, 0.8)) * 0.7
        coluna += T.lines([(-0.15 + 0.1 * k, 0.3, -0.15 + 0.1 * k, 0.3 - alt, 0.5) for k in range(4)], 0.01) * (1 - rel(t, 0.55, 0.8))
    flocos = _gotas(T, t, 0.3, 0.5, 14, 139, tam=0.015, cai=-0.3, alcance=0.4)
    G += (circulo * 1.2 + coluna + flocos) * env
    H += (circulo * 0.8 + coluna * 0.8 + flocos * 0.7) * env
    return G, H


# ------------------------------------------------------------------ Surfista Prateado
def raio_da_prancha(T, t, rng):
    """Surfista Prateado: ele passa deslizando na prancha (o rastro prateado) e solta o raio cósmico da mão, que acerta
    em estrelas."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = rel(t, 0.0, 0.3)
    prancha = T.zero()
    if 0 < u < 1:
        x = -0.95 + 0.6 * ease_out(u, 1.5)
        prancha = T.polys([(_elipse_pts(x, -0.55, 0.16, 0.035, -0.1, 16), 1.0)], 0.003) + T.tapered([(x - 0.5, -0.5, x - 0.15, -0.55, 0.7)], 0.03)
        prancha *= (1 - rel(t, 0.4, 0.55))
    feixe = _feixe(T, t, 0.14, 0.24, -0.45, -0.5, 0.0, 0.0, 0.05)
    estrelas = T.zero()
    for j in range(5):
        a = j * TAU / 5 + 0.3
        u2 = rel(t, 0.24, 0.6)
        if 0 < u2 < 1:
            d = 0.12 + 0.3 * ease_out(u2, 2)
            estrelas += T.polys([(estrela(math.cos(a) * d, math.sin(a) * d, 0.05 * (1 - u2), a, 4, 0.35), 1.0)], 0.002)
    G += (prancha * 1.1 + T.glow(feixe, 1.0, 0.7, 0.02) + estrelas * 1.2) * env
    H += (prancha * 0.7 + feixe * 1.3 + estrelas) * env
    return G, H


# ------------------------------------------------------------------ Coragem
def mordida_corajosa(T, t, rng):
    """Coragem: ele vem tremendo inteiro de medo (o corpo vibrando), fecha os olhos e morde mesmo assim; os dentinhos
    fecham com as gotas de suor voando."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    treme = 0.03 * math.sin(t * 90)
    u = ease_in(rel(t, 0.0, 0.2), 1.4)
    px = -0.85 + 0.7 * u + treme
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.3, 0.42))
    corpo = T.polys([(_elipse_pts(px, 0.0, 0.2, 0.24, 0.0, 16), 1.0)], 0.006) * vis
    fecha = ease_out(rel(t, 0.16, 0.24), 3)
    dentes = T.zero()
    kd = janela(t, 0.14, 0.18) * (1 - rel(t, 0.45, 0.6))
    if kd > 0:
        for lado in (-1, 1):
            y = lado * (0.28 - 0.22 * fecha)
            dentes += T.polys([([(-0.24 + 0.12 * k, y), (-0.18 + 0.12 * k, y - lado * 0.12), (-0.12 + 0.12 * k, y)], 1.0) for k in range(4)], 0.002)
        dentes *= kd
    suor = _gotas(T, t, 0.0, 0.5, 10, 149, tam=0.02, cai=0.5, alcance=0.35, a0=-3.0, a1=-0.2)
    G += (corpo * 0.9 + dentes * 1.3 + suor) * env
    H += (corpo * 0.3 + dentes + suor * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Papa-Léguas
def poeira_do_papaleguas(T, t, rng):
    """Papa-Léguas: passa como um borrão (bip-bip!), dá a bicada no caminho e deixa só a nuvem de poeira e as linhas
    de velocidade para trás."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = rel(t, 0.0, 0.16)
    borrao = T.zero()
    if 0 < u < 1:
        x = -0.95 + 1.9 * u
        borrao = T.polys([(_elipse_pts(x, 0.0, 0.18, 0.08, 0.0, 16), 1.0)], 0.02) * 0.8
        borrao += T.lines([(x - 0.6, -0.08 + 0.08 * k, x - 0.15, -0.08 + 0.08 * k, 1.0) for k in range(3)], 0.012)
    bicada = T.polys([(estrela(0, 0, 0.16 * pulso(t, 0.08, 0.3) + 0.01, 0.0, 4, 0.3), 1.0)], 0.003) * pulso(t, 0.08, 0.3)
    poeira = T.zero()
    kp = pulso(t, 0.1, 0.85)
    if kp > 0:
        for k in range(6):
            poeira += T.gauss(-0.1 + 0.15 * k * rel(t, 0.1, 0.5), 0.1 - 0.05 * k * rel(t, 0.1, 0.85), 0.07 + 0.015 * k)
        poeira *= kp * 0.55
    G += (borrao + bicada * 1.2 + poeira) * env
    H += (borrao * 0.5 + bicada + poeira * 0.3) * env
    return G, H


REGISTRO = [
    ("tapa_de_gorila_dk", tapa_de_gorila_dk, GRANDE, "básico do Donkey Kong: o tapão de gorila e a banana", False),
    ("pancada_viltrumita", pancada_viltrumita, GRANDE, "básico do Omni-Man: o soco que racha o ar", False),
    ("tapa_elastico", tapa_elastico, GRANDE, "básico da Mulher-Elástica: o braço em mola e o boing", False),
    ("raio_do_ankh", raio_do_ankh, GRANDE, "básico do Mumm-Ra: o ankh e o raio das trevas", False),
    ("kunai_do_sharingan", kunai_do_sharingan, GRANDE, "básico do Kakashi: o Sharingan girando e a kunai", False),
    ("danca_da_lua_branca", danca_da_lua_branca, GRANDE, "básico da Rukia: o círculo e a coluna de gelo branco", False),
    ("raio_da_prancha", raio_da_prancha, GRANDE, "básico do Surfista Prateado: a prancha e o raio cósmico", False),
    ("mordida_corajosa", mordida_corajosa, GRANDE, "básico do Coragem: tremendo de medo e mordendo mesmo assim", False),
    ("poeira_do_papaleguas", poeira_do_papaleguas, GRANDE, "básico do Papa-Léguas: o borrão, a bicada e a poeira", False),
]
