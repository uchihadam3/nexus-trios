"""Ataques básicos com animação própria, lote ze: Tanjiro, Ichigo, Aizen, Levi, Blade, Sephiroth, Vergil e Raiden.

Todos dividiam o mesmo "corte"; agora cada espada conta quem a usa: a onda da Respiração da Água do Tanjiro, a
lâmina larga da Zangetsu do Ichigo com a meia-lua escura, o espelho que trinca na Kyoka Suigetsu do Aizen, as duas
lâminas girando do Levi, a espada de prata e o sangue do Blade, a Masamune comprida e as penas negras do Sephiroth, o
saque da Yamato do Vergil com os cortes no ar e a lâmina de alta frequência do Raiden, vermelha de quente.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, girado, janela, lamina, pulso, rel, vazio
from .basicos_a import _elipse_pts, _zigue
from .basicos_u import _anel, _estrela_de_contato, _riscos
from .basicos_x import _gotas


def _arco_de_corte(T, t, t0, t1, a0, a1, r, larg, cx=0.0, cy=0.0, squash=1.0, rot=0.0, some=(0.3, 0.6)):
    """O rastro em meia-lua de uma lâmina que passa de a0 até a1; devolve (rastro, fio, ângulo da cabeça)."""
    p = ease_out(rel(t, t0, t1), 2.2)
    sai = apaga(t, *some)
    fim = a0 + (a1 - a0) * p + (0.01 if a1 > a0 else -0.01)
    rastro = T.arc_band(r, larg, a0, fim, squash, rot, cx, cy, crescente=True) * sai
    fio = T.arc_band(r + larg * 0.25, larg * 0.3, a0, fim, squash, rot, cx, cy, crescente=True) * sai
    return rastro, fio, a0 + (a1 - a0) * p


# ------------------------------------------------------------------ Tanjiro
def corte_da_agua_tanjiro(T, t, rng):
    """Tanjiro: o corte da Respiração da Água, uma onda azul que acompanha a lâmina em arco, com a crista enrolando
    como numa gravura japonesa, e as gotas espirrando no acerto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    rastro, fio, ah = _arco_de_corte(T, t, 0.0, 0.24, -2.6, 0.7, 0.58, 0.16)
    onda = T.zero()
    k = janela(t, 0.04, 0.1) * apaga(t, 0.3, 0.52)
    if k > 0:
        pts = []
        for s in np.linspace(0, 1, 30):
            a = -2.6 + (ah + 2.6) * s
            rr = 0.66 + 0.05 * math.sin(s * 14 - t * 30)
            pts.append((math.cos(a) * rr, math.sin(a) * rr))
        onda = T.polyline(pts, 0.03) * k
        # a crista enrolando na cabeça da onda
        cx, cy = math.cos(ah) * 0.68, math.sin(ah) * 0.68
        crista = [(cx + 0.09 * math.cos(b) * (1 - b / 9), cy + 0.09 * math.sin(b) * (1 - b / 9)) for b in np.linspace(0, 7, 18)]
        onda += T.polyline(crista, 0.025) * k
    gotas = _gotas(T, t, 0.22, 0.45, 16, 31, tam=0.026, cai=0.5, alcance=0.55)
    est = _estrela_de_contato(T, t, 0.22, 0.26, 6, 0.35)
    G += (T.glow(rastro, 1.0, 0.8, 0.03) + fio * 1.1 + onda * 1.3 + gotas * 1.2 + est) * env
    H += (fio * 1.6 + rastro * 0.25 + onda * 0.7 + gotas * 0.9 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Ichigo
def corte_da_zangetsu(T, t, rng):
    """Ichigo: a Zangetsu, a lâmina larga sem guarda, desce na diagonal e o corte deixa uma meia-lua grossa de energia
    escura com a borda serrilhada (o Getsuga em miniatura)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    p = ease_out(rel(t, 0.0, 0.22), 2.4)
    ang = -2.2 + 2.6 * p
    vis = 1 - rel(t, 0.24, 0.34)
    ca, sa = math.cos(ang), math.sin(ang)
    nx, ny = -sa, ca
    base = (ca * 0.12, sa * 0.12)
    ponta = (ca * 0.86, sa * 0.86)
    larg = 0.085
    cutelo = [(base[0] + nx * larg, base[1] + ny * larg), (ponta[0] + nx * larg, ponta[1] + ny * larg), (ponta[0] - nx * larg * 0.2, ponta[1] - ny * larg * 0.2),
              (base[0] - nx * larg, base[1] - ny * larg)]
    espada = T.polys([(cutelo, 1.0)], 0.003) * vis
    cabo = T.lines([(base[0], base[1], -ca * 0.08, -sa * 0.08, 1.0)], 0.03) * vis
    lua = T.arc_band(0.6, 0.24, -2.2, ang + 0.01, cx=0.0, cy=0.0, crescente=True) * apaga(t, 0.35, 0.68)
    borda = T.zero()
    kb = janela(t, 0.08, 0.14) * apaga(t, 0.35, 0.68)
    if kb > 0:
        pts = [(math.cos(a) * (0.75 + 0.04 * (j % 2)), math.sin(a) * (0.75 + 0.04 * (j % 2))) for j, a in enumerate(np.linspace(-2.2, ang, 22))]
        borda = T.polyline(pts, 0.02) * kb
    est = _estrela_de_contato(T, t, 0.22, 0.3, 8, 0.32)
    G += (T.glow(lua, 1.1, 1.0, 0.04) + espada * 1.2 + cabo * 0.8 + borda * 1.2 + est) * env
    H += (lua * 0.35 + espada * 1.1 + borda * 1.0 + est * 1.0) * env
    return G, H


# ------------------------------------------------------------------ Aizen
def espelho_partido_aizen(T, t, rng):
    """Aizen: a Kyoka Suigetsu. O alvo vira um reflexo num espelho, o espelho trinca em teia, e o corte de verdade vem
    por trás da ilusão, uma linha fina e calma que atravessa tudo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    km = janela(t, 0.0, 0.08) * (1 - rel(t, 0.3, 0.42))
    espelho = T.ring(0.5, 0.02, squash=1.0) * km * 0.9
    reflexo = T.gauss(0, 0, 0.3) * km * 0.25
    trinca = T.zero()
    kt = rel(t, 0.12, 0.24)
    if kt > 0 and t < 0.6:
        q = np.random.default_rng(17)
        segs = []
        for j in range(9):
            a = j * TAU / 9 + q.uniform(-0.2, 0.2)
            r = 0.5 * ease_out(kt, 2)
            segs.append((0.0, 0.0, math.cos(a) * r, math.sin(a) * r, 1.0))
        for rr in (0.18, 0.34):
            pts = [(math.cos(a) * rr * ease_out(kt, 2), math.sin(a) * rr * ease_out(kt, 2)) for a in np.linspace(0, TAU, 10)]
            segs += [(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], 0.7) for k in range(9)]
        trinca = T.lines(segs, 0.012) * (1 - rel(t, 0.42, 0.6))
    # os cacos caindo depois que o espelho quebra
    cacos = _gotas(T, t, 0.3, 0.45, 14, 23, tam=0.03, cai=0.7, alcance=0.45)
    kc = rel(t, 0.3, 0.42)
    corte = T.zero()
    if kc > 0:
        corte = T.polys([(lamina(-0.75, 0.42, 0.75, -0.42, 0.035, ease_out(kc, 3), rel(t, 0.5, 0.72)), 1.0)], 0.003)
    est = _estrela_de_contato(T, t, 0.38, 0.2, 4, 0.2, dur=0.25)
    G += (espelho + reflexo + trinca * 1.3 + cacos * 0.9 + T.glow(corte, 1.2, 0.8, 0.03) + est) * env
    H += (espelho * 0.5 + trinca * 1.0 + cacos * 0.6 + corte * 1.6 + est) * env
    return G, H


# ------------------------------------------------------------------ Levi
def laminas_giratorias_levi(T, t, rng):
    """Levi: chega pelo cabo do equipamento de manobra, gira como um pião com as duas lâminas abertas e corta em
    círculos rápidos, deixando dois anéis de corte em volta do alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    cabo = T.zero()
    kc = janela(t, 0.0, 0.04) * (1 - rel(t, 0.12, 0.2))
    if kc > 0:
        cabo = T.lines([(-0.95, -0.7, -0.05, -0.02, 1.0), (-0.95, 0.65, -0.05, 0.02, 0.7)], 0.01) * kc
    gira = ease_out(rel(t, 0.06, 0.45), 1.6)
    vis = janela(t, 0.06, 0.1) * (1 - rel(t, 0.45, 0.55))
    laminas = T.zero()
    if vis > 0:
        ang = gira * TAU * 2.5
        formas = []
        for s in (0, math.pi):
            a = ang + s
            formas.append((lamina(math.cos(a) * 0.1, math.sin(a) * 0.1 * 0.6, math.cos(a) * 0.55, math.sin(a) * 0.55 * 0.6, 0.04), 1.0))
        laminas = T.polys(formas, 0.003) * vis
    aneis = T.zero()
    for j, (t0, r) in enumerate(((0.14, 0.5), (0.26, 0.42))):
        k = pulso(t, t0, t0 + 0.35)
        if k > 0:
            aneis += T.arc_band(r, 0.08, 0.0, TAU * ease_out(rel(t, t0, t0 + 0.12), 2) - 0.05, squash=0.6, crescente=True) * k
    riscos = _riscos(T, t, 0.2, 0.3, 8, 0.15, 0.5, 0.016, 41, 0.0, TAU)
    G += (cabo + laminas * 1.3 + T.glow(aneis, 1.0, 0.7, 0.03) + riscos) * env
    H += (cabo * 0.6 + laminas * 1.2 + aneis * 0.6 + riscos * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Blade
def corte_de_prata_blade(T, t, rng):
    """Blade: a espada de prata com o cabo de caveira corta em X, rápido e seco, e o acerto espirra sangue escuro
    em gotas grossas que caem (o caçador de vampiros)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    cortes = T.zero()
    for j, (t0, x1, y1, x2, y2) in enumerate(((0.0, -0.6, -0.55, 0.6, 0.5), (0.14, -0.6, 0.55, 0.6, -0.5))):
        k = rel(t, t0, t0 + 0.12)
        if k > 0:
            cortes += T.polys([(lamina(x1, y1, x2, y2, 0.06, ease_out(k, 2.5), rel(t, t0 + 0.2, t0 + 0.45)), 1.0)], 0.003)
    kesp = janela(t, 0.14, 0.2) * (1 - rel(t, 0.26, 0.34))
    espada = T.polys([(lamina(0.6, -0.5, 0.95, -0.82, 0.03), 1.0)], 0.002) * kesp
    caveira = T.gauss(0.55, -0.45, 0.035) * kesp
    sangue = _gotas(T, t, 0.22, 0.55, 18, 57, tam=0.034, cai=0.8, alcance=0.5, a0=-3.0, a1=0.2)
    est = _estrela_de_contato(T, t, 0.22, 0.24, 6, 0.3)
    G += (T.glow(cortes, 1.1, 0.7, 0.025) + espada * 1.2 + sangue * 1.3 + est) * env
    H += (cortes * 1.4 + espada * 1.0 + caveira * 1.5 + sangue * 0.3 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Sephiroth
def masamune_sephiroth(T, t, rng):
    """Sephiroth: a Masamune, comprida demais, atravessa a tela inteira num corte reto e frio, e as penas negras da
    asa única caem devagar balançando."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = rel(t, 0.0, 0.16)
    lam = T.zero()
    if k > 0:
        lam = T.polys([(lamina(-1.0, 0.18, 1.0, -0.12, 0.026, ease_out(k, 3.2), rel(t, 0.3, 0.55)), 1.0)], 0.002)
    brilho = T.flare(0.2, 0.02, 0.6, -0.15, 0.01) * pulso(t, 0.14, 0.4) * 1.3
    penas = T.zero()
    q = np.random.default_rng(71)
    for j in range(7):
        x0, y0, atraso = q.uniform(-0.7, 0.7), q.uniform(-0.75, -0.35), q.uniform(0.0, 0.25)
        u = rel(t, 0.15 + atraso, 0.95)
        if 0 < u < 1:
            x = x0 + 0.08 * math.sin(u * 9 + j)
            y = y0 + 0.9 * u
            a = 0.6 * math.sin(u * 9 + j) + math.pi / 2
            penas += T.polys([(_elipse_pts(x, y, 0.06, 0.018, a, 10), 1.0)], 0.003) * (1 - u)
    est = _estrela_de_contato(T, t, 0.16, 0.2, 4, 0.25, ang=-0.15, dur=0.3)
    G += (T.glow(lam, 1.2, 0.8, 0.02) + brilho + penas * 0.9 + est) * env
    H += (lam * 1.6 + brilho * 1.2 + penas * 0.2 + est) * env
    return G, H


# ------------------------------------------------------------------ Vergil
def corte_da_yamato(T, t, rng):
    """Vergil: o saque da Yamato, rápido demais para ver: um clarão na bainha, um instante parado, e então vários
    cortes finos e retos aparecem no ar em volta do alvo de uma vez (o Corte do Julgamento em miniatura)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    saque = T.flare(-0.7, 0.3, 0.7, 0.0, 0.008) * pulso(t, 0.0, 0.14) * 1.4
    linha = T.zero()
    kl = rel(t, 0.02, 0.1)
    if 0 < kl and t < 0.2:
        linha = T.polys([(lamina(-0.75, 0.3, 0.6, -0.1, 0.02, ease_out(kl, 3)), 1.0)], 0.002) * (1 - rel(t, 0.12, 0.2))
    cortes = T.zero()
    kc = rel(t, 0.22, 0.3)
    if kc > 0:
        q = np.random.default_rng(91)
        formas = []
        for j in range(7):
            a = q.uniform(0, math.pi)
            ox, oy = q.uniform(-0.15, 0.15), q.uniform(-0.15, 0.15)
            c = q.uniform(0.35, 0.6)
            formas.append((lamina(ox - math.cos(a) * c, oy - math.sin(a) * c, ox + math.cos(a) * c, oy + math.sin(a) * c, 0.018,
                                  ease_out(min(1, kc * (1 + j * 0.15)), 3), rel(t, 0.42 + j * 0.02, 0.7)), 1.0))
        cortes = T.polys(formas, 0.002)
    distorce = T.ring(0.3 + 0.2 * rel(t, 0.22, 0.6), 0.03) * pulso(t, 0.22, 0.6)
    G += (saque + linha + T.glow(cortes, 1.2, 0.8, 0.02) + distorce * 0.8) * env
    H += (saque * 1.2 + linha * 1.4 + cortes * 1.6 + distorce * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Raiden
def lamina_hf_raiden(T, t, rng):
    """Raiden: a lâmina de alta frequência vermelha de quente corta na horizontal, deixando o fio incandescente, os
    raios saltando da lâmina e as faíscas do metal cortado (o Zandatsu)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    rastro, fio, ah = _arco_de_corte(T, t, 0.0, 0.2, -2.9, -0.2, 0.55, 0.12, squash=0.55, some=(0.32, 0.62))
    ca, sa = math.cos(ah), math.sin(ah) * 0.55
    vis = 1 - rel(t, 0.22, 0.3)
    espada = T.polys([(lamina(ca * 0.15, sa * 0.15, ca * 0.85, sa * 0.85, 0.03), 1.0)], 0.002) * vis
    raios = T.zero()
    kr = janela(t, 0.04, 0.08) * (1 - rel(t, 0.3, 0.45))
    if kr > 0:
        for j in range(3):
            x0 = ca * (0.3 + 0.2 * j)
            y0 = sa * (0.3 + 0.2 * j)
            raios += T.polyline(_zigue(x0, y0, x0 + 0.08, y0 - 0.25, 5, 0.04, 1 if j % 2 else -1), 0.012)
        raios *= kr
    faiscas = _riscos(T, t, 0.2, 0.35, 12, 0.1, 0.55, 0.018, 77, -0.6, 3.7)
    est = _estrela_de_contato(T, t, 0.2, 0.26, 8, 0.3)
    G += (T.glow(rastro, 1.1, 0.8, 0.03) + fio * 1.2 + espada * 1.3 + raios * 1.3 + faiscas * 1.2 + est) * env
    H += (fio * 1.8 + rastro * 0.5 + espada * 1.5 + raios * 1.0 + faiscas * 1.0 + est) * env
    return G, H


REGISTRO = [
    ("corte_da_agua_tanjiro", corte_da_agua_tanjiro, GRANDE, "básico do Tanjiro: o corte da Respiração da Água com a onda", False),
    ("corte_da_zangetsu", corte_da_zangetsu, GRANDE, "básico do Ichigo: a Zangetsu larga e a meia-lua escura", False),
    ("espelho_partido_aizen", espelho_partido_aizen, GRANDE, "básico do Aizen: o espelho que trinca e o corte por trás da ilusão", False),
    ("laminas_giratorias_levi", laminas_giratorias_levi, GRANDE, "básico do Levi: o cabo de manobra e as duas lâminas girando", False),
    ("corte_de_prata_blade", corte_de_prata_blade, GRANDE, "básico do Blade: a espada de prata em X e o sangue", False),
    ("masamune_sephiroth", masamune_sephiroth, GRANDE, "básico do Sephiroth: a Masamune comprida e as penas negras", False),
    ("corte_da_yamato", corte_da_yamato, GRANDE, "básico do Vergil: o saque da Yamato e os cortes no ar", False),
    ("lamina_hf_raiden", lamina_hf_raiden, GRANDE, "básico do Raiden: a lâmina de alta frequência e os raios", False),
]
