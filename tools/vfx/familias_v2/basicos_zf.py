"""Ataques básicos com animação própria, lote zf: Ezio, Scorpion, Sora, 2B, Malenia, Ryu Hayabusa, Príncipe da Pérsia e
Hiei.

Mais oito que dividiam o mesmo corte: a lâmina oculta que salta do pulso do Ezio, a lança de corrente do Scorpion que
crava e puxa, a Keyblade do Sora com a coroa de brilho, a katana branca da 2B que se desfaz em quadradinhos, a
lâmina da Malenia com a flor escarlate abrindo, o corte com imagens repetidas do Hayabusa, a adaga do Príncipe com a
areia do tempo voltando e os cortes invisíveis do Hiei com a chama negra.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_u import _anel, _estrela_de_contato, _riscos
from .basicos_x import _gotas
from .basicos_ze import _arco_de_corte


# ------------------------------------------------------------------ Ezio
def lamina_do_credo_ezio(T, t, rng):
    """Ezio: o braço avança, a lâmina oculta salta do pulso num estalo e crava no alvo; o símbolo da Irmandade (a
    ponta em A) brilha um instante no acerto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vem = ease_in(rel(t, 0.0, 0.16), 1.6)
    volta = ease_out(rel(t, 0.3, 0.6), 2)
    px = -0.9 + 0.75 * vem - 0.3 * volta
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.5, 0.62))
    braco = T.polys([([(px - 0.6, -0.07), (px, -0.06), (px, 0.06), (px - 0.6, 0.07)], 0.8)], 0.003)
    sai = ease_out(rel(t, 0.12, 0.18), 3)
    lam = T.polys([(lamina(px, 0.0, px + 0.05 + 0.3 * sai, 0.0, 0.03), 1.0)], 0.002) if sai > 0 else T.zero()
    corpo = np.clip(braco + lam, 0, 1) * vis
    clique = T.flare(px, 0.0, 0.25, 0.0, 0.01) * pulso(t, 0.12, 0.22)
    ka = pulso(t, 0.2, 0.55)
    simbolo = T.zero()
    if ka > 0:
        s = 0.22 * back(rel(t, 0.2, 0.32), 2.0)
        simbolo = T.polys([([(0, -s), (s * 0.75, s * 0.8), (s * 0.35, s * 0.8), (0, 0), (-s * 0.35, s * 0.8), (-s * 0.75, s * 0.8)], 1.0)], 0.004) * ka
    est = _estrela_de_contato(T, t, 0.18, 0.2, 6, 0.3)
    G += (corpo * 1.1 + clique + simbolo * 0.9 + est) * env
    H += (corpo * 0.5 + lam * vis * 1.2 + clique * 1.2 + simbolo * 0.8 + est) * env
    return G, H


# ------------------------------------------------------------------ Scorpion
def lanca_corrente_scorpion(T, t, rng):
    """Scorpion: a lança de corrente voa da esquerda com os elos estalando, crava no alvo, e a corrente estica e puxa
    de volta (o "Venha cá!"), com uma lufada de fogo no fim."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vai = ease_in(rel(t, 0.0, 0.16), 1.4)
    puxa = ease_in(rel(t, 0.3, 0.48), 1.6)
    px = -1.0 + 1.0 * vai - 0.9 * puxa
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.46, 0.52))
    ponta = T.polys([([(px + 0.12, 0.0), (px - 0.02, -0.07), (px + 0.01, 0.0), (px - 0.02, 0.07)], 1.0)], 0.002) * vis
    elos = T.zero()
    if vis > 0:
        estica = 1 - 0.5 * pulso(t, 0.2, 0.32)
        pts = [(-1.0 + (px + 1.0) * s, 0.04 * math.sin(s * 18) * estica) for s in np.linspace(0, 1, 30)]
        elos = T.polyline(pts, 0.016) * vis
        elos += T.splats([(x, y, 0.6) for x, y in pts[::3]], 0.012) * vis
    # as labaredas no alvo quando a lança crava e puxa (o fogo do Netherrealm)
    fogo = T.zero()
    kf = pulso(t, 0.18, 0.62)
    if kf > 0:
        formas = []
        for k in range(7):
            x = -0.3 + 0.1 * k
            alt = (0.22 + 0.12 * math.sin(t * 35 + k * 1.7)) * kf
            larg = 0.06
            formas.append(([(x - larg, 0.2), (x - larg * 0.4, 0.2 - alt * 0.6), (x + 0.02 * math.sin(t * 50 + k), 0.2 - alt), (x + larg * 0.5, 0.2 - alt * 0.5), (x + larg, 0.2)], 1.0))
        fogo = T.polys(formas, 0.008) * kf
    est = _estrela_de_contato(T, t, 0.16, 0.22, 6, 0.32)
    G += (ponta * 1.2 + elos * 1.0 + fogo + est) * env
    H += (ponta * 1.0 + elos * 0.5 + fogo * 0.6 + est) * env
    return G, H


# ------------------------------------------------------------------ Sora
def keyblade_sora(T, t, rng):
    """Sora: a Keyblade (o cabo em coroa e o dente de chave na ponta) gira num golpe largo e o acerto solta a coroa
    de brilho e estrelinhas, leve e alegre."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    rastro, fio, ah = _arco_de_corte(T, t, 0.0, 0.22, -2.4, 0.6, 0.55, 0.13)
    vis = 1 - rel(t, 0.24, 0.32)
    ca, sa = math.cos(ah), math.sin(ah)
    haste = T.lines([(ca * 0.1, sa * 0.1, ca * 0.75, sa * 0.75, 1.0)], 0.03) * vis
    nx, ny = -sa, ca
    dente = T.polys([([(ca * 0.75, sa * 0.75), (ca * 0.75 + nx * 0.14, sa * 0.75 + ny * 0.14), (ca * 0.66 + nx * 0.14, sa * 0.66 + ny * 0.14),
                       (ca * 0.66 + nx * 0.07, sa * 0.66 + ny * 0.07), (ca * 0.62, sa * 0.62)], 1.0)], 0.002) * vis
    kc = pulso(t, 0.2, 0.55)
    coroa = T.zero()
    if kc > 0:
        s = 0.2 * back(rel(t, 0.2, 0.32), 2.2)
        coroa = T.polys([([(-s, s * 0.5), (-s, -s * 0.2), (-s * 0.5, s * 0.1), (0, -s * 0.6), (s * 0.5, s * 0.1), (s, -s * 0.2), (s, s * 0.5)], 1.0)], 0.003) * kc
    estrelas = T.zero()
    q = np.random.default_rng(13)
    for j in range(6):
        a = q.uniform(0, TAU)
        u = rel(t, 0.22 + 0.02 * j, 0.65)
        if 0 < u < 1:
            r = 0.15 + 0.4 * ease_out(u, 2)
            estrelas += T.polys([(estrela(math.cos(a) * r, math.sin(a) * r, 0.05 * (1 - u), a, 5, 0.45), 1.0)], 0.002)
    G += (T.glow(rastro, 1.0, 0.7, 0.03) + fio + haste * 1.2 + dente * 1.2 + coroa * 1.1 + estrelas * 1.2) * env
    H += (fio * 1.4 + haste + dente + coroa * 0.9 + estrelas) * env
    return G, H


# ------------------------------------------------------------------ 2B
def katana_da_2b(T, t, rng):
    """2B: a katana branca corta em linha reta e fina, e o rastro se desfaz em quadradinhos que sobem (como uma tela
    que se desmancha), com o círculo do sistema de mira apertando no alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    k = rel(t, 0.02, 0.16)
    lam = T.zero()
    if k > 0:
        lam = T.polys([(lamina(-0.8, -0.35, 0.8, 0.35, 0.03, ease_out(k, 3), rel(t, 0.22, 0.42)), 1.0)], 0.002)
    mira = T.zero()
    km = janela(t, 0.0, 0.06) * (1 - rel(t, 0.2, 0.3))
    if km > 0:
        r = 0.45 - 0.2 * rel(t, 0.0, 0.18)
        mira = (T.ring(r, 0.012) + T.lines([(-r - 0.08, 0, -r + 0.05, 0, 1), (r - 0.05, 0, r + 0.08, 0, 1), (0, -r - 0.08, 0, -r + 0.05, 1), (0, r - 0.05, 0, r + 0.08, 1)], 0.012)) * km
    pixels = T.zero()
    q = np.random.default_rng(29)
    for j in range(16):
        s = q.uniform(0, 1)
        x0, y0 = -0.8 + 1.6 * s, -0.35 + 0.7 * s
        u = rel(t, 0.2 + 0.2 * s, 0.75)
        if 0 < u < 1:
            x, y, l = x0 + q.uniform(-0.05, 0.05), y0 - 0.35 * u, 0.025 * (1 - u * 0.6)
            pixels += T.polys([([(x - l, y - l), (x + l, y - l), (x + l, y + l), (x - l, y + l)], 1.0)], 0.001) * (1 - u)
    G += (T.glow(lam, 1.2, 0.8, 0.02) + mira * 0.8 + pixels * 1.2) * env
    H += (lam * 1.6 + mira * 0.4 + pixels * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Malenia
def flor_escarlate_malenia(T, t, rng):
    """Malenia: três cortes rápidos e leves da lâmina de Miquella (a dança da garça), e no alvo uma flor escarlate
    abre as pétalas e solta o pó vermelho da podridão."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    cortes = T.zero()
    for j, (t0, a) in enumerate(((0.0, -0.5), (0.08, 0.6), (0.16, -0.1))):
        k = rel(t, t0, t0 + 0.08)
        if k > 0:
            ca, sa = math.cos(a), math.sin(a)
            cortes += T.polys([(lamina(-ca * 0.6, -sa * 0.6, ca * 0.6, sa * 0.6, 0.03, ease_out(k, 2.5), rel(t, t0 + 0.12, t0 + 0.3)), 1.0)], 0.002)
    kf = rel(t, 0.24, 0.42)
    flor = T.zero()
    if kf > 0:
        abre = ease_out(kf, 2) * apaga(t, 0.6, 0.9)
        formas = []
        for j in range(6):
            a = j * TAU / 6 + 0.3
            formas.append((_elipse_pts(math.cos(a) * 0.12 * abre, math.sin(a) * 0.12 * abre, 0.12 * abre + 0.005, 0.05 * abre + 0.003, a, 12), 1.0))
        flor = T.polys(formas, 0.004)
        flor += T.gauss(0, 0, 0.05) * abre
    po = _gotas(T, t, 0.32, 0.55, 22, 61, tam=0.018, cai=-0.25, alcance=0.5)
    G += (T.glow(cortes, 1.1, 0.7, 0.02) + flor * 1.2 + po * 1.1) * env
    H += (cortes * 1.4 + flor * 0.6 + po * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Ryu Hayabusa
def corte_izuna_hayabusa(T, t, rng):
    """Ryu Hayabusa: o ninja passa num corte tão rápido que deixa três imagens repetidas dele (os vultos), e o alvo
    leva o corte em zigue-zague com a fumaça roxa do ninja."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vultos = T.zero()
    for j in range(3):
        u = rel(t, 0.0 + 0.04 * j, 0.2 + 0.04 * j)
        if 0 < u < 1:
            x = -0.9 + 1.8 * ease_out(u, 2)
            vultos += T.polys([(_elipse_pts(x, 0.0, 0.07, 0.22, 0.0, 14), 1.0)], 0.01) * (1 - u) * (0.7 - 0.2 * j)
    zz = T.zero()
    k = rel(t, 0.12, 0.22)
    if k > 0:
        pts = [(-0.55, -0.35), (0.25, -0.15), (-0.3, 0.1), (0.55, 0.3)]
        segs = []
        for a, b in zip(pts, pts[1:]):
            segs.append((lamina(a[0], a[1], b[0], b[1], 0.025, ease_out(k, 2.5), rel(t, 0.32, 0.5)), 1.0))
        zz = T.polys(segs, 0.002)
    fumaca = T.zero()
    kf = pulso(t, 0.3, 0.75)
    if kf > 0:
        for j in range(6):
            a = j * TAU / 6
            r = 0.2 + 0.25 * rel(t, 0.3, 0.75)
            fumaca += T.gauss(math.cos(a) * r, math.sin(a) * r * 0.7 - 0.1 * rel(t, 0.3, 0.75), 0.09)
        fumaca *= kf * 0.55
    G += (vultos * 0.8 + T.glow(zz, 1.1, 0.7, 0.02) + fumaca) * env
    H += (vultos * 0.3 + zz * 1.5 + fumaca * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Príncipe da Pérsia
def adaga_de_areia_principe(T, t, rng):
    """Príncipe da Pérsia: a Adaga do Tempo corta em arco curto e a areia dourada escorre do corte, gira num redemoinho
    e volta para trás como o tempo voltando."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    rastro, fio, ah = _arco_de_corte(T, t, 0.0, 0.18, -2.2, 0.4, 0.45, 0.1, some=(0.28, 0.5))
    ca, sa = math.cos(ah), math.sin(ah)
    adaga = T.polys([(lamina(ca * 0.15, sa * 0.15, ca * 0.6, sa * 0.6, 0.035), 1.0)], 0.002) * (1 - rel(t, 0.2, 0.28))
    areia = T.zero()
    q = np.random.default_rng(37)
    pts = []
    for j in range(28):
        a0 = q.uniform(0, TAU)
        u = rel(t, 0.18 + q.uniform(0, 0.1), 0.85)
        if 0 < u < 1:
            r = 0.45 * (1 - ease_in(u, 1.4)) + 0.05
            a = a0 - 6.0 * u
            pts.append((math.cos(a) * r, math.sin(a) * r * 0.7, (1 - u) * 0.9))
    if pts:
        areia = T.splats(pts, 0.016)
    ampulheta = T.zero()
    kh = pulso(t, 0.5, 0.85)
    if kh > 0:
        s = 0.12
        ampulheta = T.polyline([(-s, -s * 1.4), (s, -s * 1.4), (-s, s * 1.4), (s, s * 1.4), (-s, -s * 1.4)], 0.012) * kh
    G += (T.glow(rastro, 1.0, 0.7, 0.03) + fio + adaga * 1.2 + areia * 1.3 + ampulheta) * env
    H += (fio * 1.4 + adaga + areia * 0.7 + ampulheta * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Hiei
def corte_negro_hiei(T, t, rng):
    """Hiei: rápido demais para ver: o terceiro olho (o Jagan) pisca, e o alvo aparece já cortado por vários riscos
    finos ao mesmo tempo, com chamas negras pequenas lambendo os cortes."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    ko = pulso(t, 0.0, 0.18)
    olho = T.zero()
    if ko > 0:
        olho = T.polys([(_elipse_pts(0.0, -0.55, 0.12, 0.05 * ko + 0.005, 0.0, 16), 1.0)], 0.003) * ko
        olho += T.gauss(0.0, -0.55, 0.025) * ko * 1.5
    cortes = T.zero()
    kc = rel(t, 0.16, 0.2)
    if kc > 0:
        q = np.random.default_rng(83)
        formas = []
        for j in range(6):
            a = q.uniform(-1.2, 1.2) + (math.pi if j % 2 else 0)
            c = q.uniform(0.3, 0.5)
            ox, oy = q.uniform(-0.1, 0.1), q.uniform(-0.12, 0.12)
            formas.append((lamina(ox - math.cos(a) * c, oy - math.sin(a) * c, ox + math.cos(a) * c, oy + math.sin(a) * c, 0.02, 1.0, rel(t, 0.36 + 0.03 * j, 0.6)), 1.0))
        cortes = T.polys(formas, 0.002) * kc
    chamas = T.zero()
    kch = pulso(t, 0.2, 0.7)
    if kch > 0:
        for j in range(5):
            x = -0.3 + 0.15 * j
            alt = 0.12 + 0.06 * math.sin(t * 40 + j)
            chamas += T.polys([([(x - 0.04, 0.1), (x, 0.1 - alt), (x + 0.04, 0.1)], 1.0)], 0.01)
        chamas *= kch
    G += (olho + T.glow(cortes, 1.1, 0.7, 0.02) + chamas * 0.9) * env
    H += (olho * 1.4 + cortes * 1.5 + chamas * 0.3) * env
    return G, H


REGISTRO = [
    ("lamina_do_credo_ezio", lamina_do_credo_ezio, GRANDE, "básico do Ezio: a lâmina oculta saltando do pulso", False),
    ("lanca_corrente_scorpion", lanca_corrente_scorpion, GRANDE, "básico do Scorpion: a lança de corrente que crava e puxa", False),
    ("keyblade_sora", keyblade_sora, GRANDE, "básico do Sora: a Keyblade e a coroa de brilho", False),
    ("katana_da_2b", katana_da_2b, GRANDE, "básico da 2B: a katana branca e os quadradinhos se desfazendo", False),
    ("flor_escarlate_malenia", flor_escarlate_malenia, GRANDE, "básico da Malenia: três cortes e a flor escarlate", False),
    ("corte_izuna_hayabusa", corte_izuna_hayabusa, GRANDE, "básico do Hayabusa: os vultos e o corte em zigue-zague", False),
    ("adaga_de_areia_principe", adaga_de_areia_principe, GRANDE, "básico do Príncipe da Pérsia: a adaga e a areia do tempo", False),
    ("corte_negro_hiei", corte_negro_hiei, GRANDE, "básico do Hiei: o Jagan e os cortes invisíveis com chama negra", False),
]
