"""Ataques básicos com animação própria, lote zj: Zero, Agente 47, Gordon Freeman, Hellboy, Yor, Kaneki, Shadow e Chun-Li.

O Z-Buster do Zero (o tiro em meia-lua carregado), o tiro abafado do silenciador do Agente 47 com o código de barras, o
tiro do Gordon com o lambda laranja, o revólver gigante do Hellboy com a fumaça, e os chutes que dividiam o mesmo
"chute": o salto agulha da Yor com as rosas, o chute do Kaneki com o olho vermelho e a kagune, o chute do caos do
Shadow com os riscos vermelhos, e o Chute Relâmpago da Chun-Li, com as pernas em leque.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, vazio
from .basicos_a import _elipse_pts, _pe_simples, _zigue
from .basicos_u import _anel, _estrela_de_contato, _riscos
from .basicos_x import _gotas
from .basicos_zi import _bala, _boca


def _chute(T, t, chega=0.22, esc=1.15, de=(-0.95, 0.55), ang0=-0.6):
    """O pé subindo em arco até o alvo (como o chute de base); devolve (pé, arco do rastro, x, y, vis)."""
    u = ease_in(rel(t, 0.0, chega), 1.4)
    caminho = lambda uu: (de[0] + (0.05 - de[0]) * uu, de[1] - de[1] * math.sin(math.pi * 0.5 * uu))
    px, py = caminho(u)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, chega + 0.2, chega + 0.36))
    pe = T.polys([(_pe_simples(px, py, esc, ang0 * (1 - u)), 1.0)], 0.006) * vis
    arco = T.polyline([caminho(max(0.0, u - 0.05 * k)) for k in range(10)], 0.06) * (1 - rel(t, chega, chega + 0.2)) * 0.7 if u > 0.02 else T.zero()
    return pe, arco, px, py, vis


# ------------------------------------------------------------------ Zero
def z_buster_carregado(T, t, rng):
    """Zero: o Z-Buster carrega um instante (o brilho girando no cano) e solta o tiro em meia-lua de plasma, que bate
    e estoura em anéis."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    kc = janela(t, 0.0, 0.04) * (1 - rel(t, 0.12, 0.16))
    carga = (T.gauss(-0.85, 0, 0.06) * 1.3 + T.ring(0.1 - 0.05 * rel(t, 0.0, 0.14), 0.012, -0.85, 0.0)) * kc
    u = rel(t, 0.14, 0.28)
    tiro = T.zero()
    if 0 < u < 1:
        x = -0.85 + 0.85 * u
        tiro = T.arc_band(0.16, 0.08, -1.3, 1.3, cx=x - 0.12, cy=0.0, crescente=True) * 1.3 + T.tapered([(x - 0.4, 0, x, 0, 0.7)], 0.1)
    aneis = _anel(T, t, 0.28, 0.6, 0.08, 0.45, 0.05) + _anel(T, t, 0.34, 0.66, 0.08, 0.35, 0.03)
    est = _estrela_de_contato(T, t, 0.28, 0.22, 8, 0.32)
    G += (carga + tiro + aneis + est) * env
    H += (carga * 1.2 + tiro * 0.8 + aneis * 0.5 + est) * env
    return G, H


# ------------------------------------------------------------------ Agente 47
def tiro_silencioso_47(T, t, rng):
    """Agente 47: um tiro abafado de silenciador (quase sem clarão, só o sopro de ar), certeiro, e o código de barras
    da nuca dele aparece por um instante no acerto, frio."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sopro = T.gauss(-0.85, 0, 0.06, 0.04) * pulso(t, 0.02, 0.18) * 0.6
    bala = _bala(T, t, 0.04, 0.14, larg=0.025, rastro=0.25)
    kb = pulso(t, 0.2, 0.6)
    barras = T.zero()
    if kb > 0:
        q = np.random.default_rng(47)
        x = -0.2
        segs = []
        while x < 0.2:
            w = q.choice([0.008, 0.016, 0.024])
            segs.append((x, -0.12, x, 0.12, 1.0))
            x += w * 2.2
        barras = T.lines(segs, 0.012) * kb
    est = _estrela_de_contato(T, t, 0.18, 0.14, 4, 0.25)
    G += (sopro + bala * 1.2 + barras * 0.9 + est) * env
    H += (sopro * 0.3 + bala + barras * 0.9 + est) * env
    return G, H


# ------------------------------------------------------------------ Gordon Freeman
def tiro_lambda_gordon(T, t, rng):
    """Gordon Freeman: o tiro de pistola e, no acerto, o lambda laranja (o símbolo da resistência) aparece com as
    faíscas da roupa HEV."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    bala = _bala(T, t, 0.02, 0.12)
    boca = _boca(T, t, 0.0)
    kl = pulso(t, 0.16, 0.6)
    lam = T.zero()
    if kl > 0:
        s = 0.22 * back(rel(t, 0.16, 0.28), 2.0)
        lam = T.lines([(-0.5 * s, 0.8 * s, 0.05 * s, -0.1 * s, 1.0), (-0.3 * s, -0.8 * s, 0.6 * s, 0.8 * s, 1.0)], 0.04 * s / 0.22) * kl
        lam += T.ring(s * 1.15, 0.012) * kl
    faiscas = _riscos(T, t, 0.16, 0.3, 8, 0.1, 0.4, 0.016, 53, 0.0, TAU)
    G += (bala * 1.3 + boca + lam * 1.2 + faiscas) * env
    H += (bala * 1.2 + boca + lam * 0.9 + faiscas * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Hellboy
def samaritano_hellboy(T, t, rng):
    """Hellboy: o Samaritano, o revólver enorme, dá um tiro com um clarão gordo e um coice que levanta fumaça; a bala
    grossa estoura no alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    boca = _boca(T, t, 0.02, tam=0.55) + T.gauss(-0.85, 0, 0.08) * pulso(t, 0.02, 0.14)
    bala = _bala(T, t, 0.04, 0.12, larg=0.06, rastro=0.45)
    fumaca = T.zero()
    kf = pulso(t, 0.06, 0.7)
    if kf > 0:
        for k in range(5):
            u = rel(t, 0.06, 0.7)
            fumaca += T.gauss(-0.85 + 0.04 * k, -0.06 - 0.25 * u * (k + 1) / 5, 0.05 + 0.03 * k)
        fumaca *= kf * 0.5
    bum = T.polys([(estrela(0, 0, 0.3 * pulso(t, 0.16, 0.45) + 0.01, 0.3, 9, 0.45), 1.0)], 0.006) * pulso(t, 0.16, 0.45)
    G += (boca + bala * 1.3 + fumaca + bum * 1.2) * env
    H += (boca * 1.2 + bala * 1.1 + fumaca * 0.3 + bum) * env
    return G, H


# ------------------------------------------------------------------ Yor
def chute_espinho_yor(T, t, rng):
    """Yor: o chute alto com o salto agulha (a ponta fina brilhando como uma lâmina) e, no acerto, as pétalas de rosa
    vermelha espalhando (a Princesa dos Espinhos)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    pe, arco, px, py, vis = _chute(T, t, 0.2, 1.1)
    salto = T.polys([(lamina(px - 0.18, py + 0.06, px - 0.3, py + 0.24, 0.02), 1.0)], 0.002) * vis
    petalas = T.zero()
    q = np.random.default_rng(67)
    for j in range(9):
        a = q.uniform(-math.pi, math.pi)
        u = rel(t, 0.2 + q.uniform(0, 0.06), 0.8)
        if 0 < u < 1:
            d = 0.12 + 0.4 * ease_out(u, 2)
            petalas += T.polys([(_elipse_pts(math.cos(a) * d, math.sin(a) * d + 0.25 * u * u, 0.045, 0.025, a + u * 5, 10), 1.0)], 0.003) * (1 - u)
    est = _estrela_de_contato(T, t, 0.2, 0.22, 6, 0.32)
    G += (pe * 1.1 + arco + salto * 1.3 + petalas * 1.2 + est) * env
    H += (pe * 0.5 + salto * 1.2 + petalas * 0.6 + est) * env
    return G, H


# ------------------------------------------------------------------ Kaneki
def chute_ghoul_kaneki(T, t, rng):
    """Kaneki: o olho vermelho de ghoul acende (com as veias), o chute vem forte, e uma ponta da kagune vermelha
    desce junto no acerto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    ko = pulso(t, 0.0, 0.3)
    olho = (T.gauss(-0.6, -0.55, 0.035) * 1.5 + T.lines([(-0.6, -0.55, -0.72, -0.62, 1), (-0.6, -0.55, -0.7, -0.47, 1)], 0.008)) * ko
    pe, arco, px, py, vis = _chute(T, t, 0.22, 1.15)
    kk = rel(t, 0.18, 0.3)
    kagune = T.zero()
    if kk > 0:
        pts = [(-0.7 + 0.7 * s * ease_out(kk, 2), -0.75 + 0.75 * s * ease_out(kk, 2) + 0.08 * math.sin(s * 6)) for s in np.linspace(0, 1, 16)]
        kagune = T.polyline(pts, 0.06) * (1 - rel(t, 0.45, 0.65))
    est = _estrela_de_contato(T, t, 0.22, 0.26, 7, 0.32)
    G += (olho + pe * 1.1 + arco + kagune * 1.1 + est) * env
    H += (olho * 1.4 + pe * 0.5 + kagune * 0.6 + est) * env
    return G, H


# ------------------------------------------------------------------ Shadow
def chute_do_caos_shadow(T, t, rng):
    """Shadow: ele vem girando (a bola de espinhos com os riscos vermelhos) e solta o chute de lado, e a energia do caos
    estala em raios no acerto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    u = ease_in(rel(t, 0.0, 0.2), 1.4)
    px = -0.9 + 0.75 * u
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.22, 0.3))
    bola = T.zero()
    if vis > 0:
        a = t * 40
        bola = T.polys([(estrela(px, 0.0, 0.16, a, 7, 0.65), 1.0)], 0.004) * vis
        bola += T.arc_band(0.12, 0.03, a, a + 2.0, cx=px, cy=0.0) * vis
    pe = T.polys([(_pe_simples(-0.15, 0.0, 1.1, 0.0), 1.0)], 0.006) * janela(t, 0.2, 0.24) * (1 - rel(t, 0.4, 0.5))
    raios = T.zero()
    kr = pulso(t, 0.22, 0.5)
    if kr > 0:
        for j in range(5):
            a = j * TAU / 5 + 0.4
            raios += T.polyline(_zigue(0, 0, math.cos(a) * 0.4, math.sin(a) * 0.4, 5, 0.04), 0.014)
        raios *= kr
    est = _estrela_de_contato(T, t, 0.22, 0.22, 6, 0.32)
    G += (bola * 1.1 + pe * 1.1 + raios * 1.2 + est) * env
    H += (bola * 0.5 + pe * 0.5 + raios * 0.8 + est) * env
    return G, H


# ------------------------------------------------------------------ Chun-Li
def chute_relampago_chunli(T, t, rng):
    """Chun-Li: o Chute Relâmpago, dezenas de chutes por segundo: as pernas aparecem em leque, várias de uma vez, e os
    acertos estouram rápidos em sequência."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    pernas = T.zero()
    k = janela(t, 0.04, 0.1) * (1 - rel(t, 0.5, 0.62))
    if k > 0:
        for j in range(6):
            fase = (t * 18 + j * 0.37) % 1
            ang = -0.6 + 1.2 * (j / 5) + 0.1 * math.sin(t * 60 + j)
            ca, sa = math.cos(ang), math.sin(ang)
            alcance = 0.35 + 0.25 * fase
            pernas += T.polys([(_pe_simples(-0.6 + ca * alcance, sa * alcance * 0.6, 0.9, ang), 1.0)], 0.008) * (0.4 + 0.6 * (1 - fase))
        pernas *= k
    estouros = T.zero()
    for j in range(5):
        t0 = 0.1 + 0.07 * j
        estouros += T.polys([(estrela(0.08 * math.sin(j * 2.1), 0.1 * math.cos(j * 1.7), 0.14 * pulso(t, t0, t0 + 0.15) + 0.005, j, 6, 0.4), 1.0)], 0.003) * pulso(t, t0, t0 + 0.15)
    G += (pernas * 1.0 + estouros * 1.2) * env
    H += (pernas * 0.4 + estouros) * env
    return G, H


REGISTRO = [
    ("z_buster_carregado", z_buster_carregado, GRANDE, "básico do Zero: o Z-Buster carregado em meia-lua", False),
    ("tiro_silencioso_47", tiro_silencioso_47, GRANDE, "básico do Agente 47: o tiro silencioso e o código de barras", False),
    ("tiro_lambda_gordon", tiro_lambda_gordon, GRANDE, "básico do Gordon Freeman: o tiro e o lambda", False),
    ("samaritano_hellboy", samaritano_hellboy, GRANDE, "básico do Hellboy: o revólver Samaritano e a fumaça", False),
    ("chute_espinho_yor", chute_espinho_yor, GRANDE, "básico da Yor: o salto agulha e as pétalas de rosa", False),
    ("chute_ghoul_kaneki", chute_ghoul_kaneki, GRANDE, "básico do Kaneki: o olho de ghoul e a kagune", False),
    ("chute_do_caos_shadow", chute_do_caos_shadow, GRANDE, "básico do Shadow: girando e o chute com raios do caos", False),
    ("chute_relampago_chunli", chute_relampago_chunli, GRANDE, "básico da Chun-Li: o Chute Relâmpago com as pernas em leque", False),
]
