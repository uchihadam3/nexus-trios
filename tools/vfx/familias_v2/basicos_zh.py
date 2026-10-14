"""Ataques básicos com animação própria, lote zh: Finn, Mestre Splinter, She-Ra, Wolverine, Deadpool, Demolidor, Loki e
Pain.

A espada do herói do Finn com as estrelinhas de desenho animado, as três batidinhas da bengala e o rabo do Splinter, a
Espada da Proteção da She-Ra com a joia brilhando, as três garras de adamantium do Wolverine, as katanas e o balão de
piada do Deadpool, o bastão que quica e o sentido de radar do Demolidor, a adaga e as cópias de ilusão do Loki e a
haste negra com os anéis do Rinnegan do Pain.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_u import _anel, _estrela_de_contato, _riscos
from .basicos_ze import _arco_de_corte


# ------------------------------------------------------------------ Finn
def espada_do_heroi_finn(T, t, rng):
    """Finn: a espada dourada num golpe de cima, todo animado, e o acerto solta estrelinhas redondas de desenho e um
    "pow" em forma de nuvem."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    rastro, fio, ah = _arco_de_corte(T, t, 0.0, 0.2, -2.3, 0.5, 0.52, 0.14)
    ca, sa = math.cos(ah), math.sin(ah)
    espada = T.polys([(lamina(ca * 0.12, sa * 0.12, ca * 0.68, sa * 0.68, 0.045), 1.0)], 0.002) * (1 - rel(t, 0.22, 0.3))
    kp = pulso(t, 0.2, 0.5)
    pow_ = T.zero()
    if kp > 0:
        r = 0.22 * back(rel(t, 0.2, 0.3), 2.2)
        pts = [((r + 0.04 * (j % 2)) * math.cos(a), (r + 0.04 * (j % 2)) * math.sin(a) * 0.8) for j, a in enumerate(np.linspace(0, TAU, 17))]
        pow_ = T.polys([(pts, 1.0)], 0.004) * kp
    estrelas = T.zero()
    for j in range(5):
        a = -0.3 + j * 1.3
        u = rel(t, 0.22, 0.6)
        if 0 < u < 1:
            d = 0.25 + 0.3 * ease_out(u, 2)
            estrelas += T.polys([(estrela(math.cos(a) * d, math.sin(a) * d, 0.06 * (1 - u * 0.5), u * 3, 5, 0.5), 1.0)], 0.002) * (1 - u)
    G += (T.glow(rastro, 1.0, 0.7, 0.03) + fio + espada * 1.2 + pow_ + estrelas * 1.2) * env
    H += (fio * 1.4 + espada + pow_ * 0.6 + estrelas) * env
    return G, H


# ------------------------------------------------------------------ Mestre Splinter
def bengala_do_mestre(T, t, rng):
    """Mestre Splinter: três batidinhas rápidas e precisas da bengala de madeira (pá, pá, pá), e o rabo de rato dá a
    última chicotada em curva."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    bengala = T.zero()
    toques = T.zero()
    for j, t0 in enumerate((0.0, 0.1, 0.2)):
        u = rel(t, t0, t0 + 0.08)
        volta = rel(t, t0 + 0.08, t0 + 0.12)
        if 0 < u and volta < 1:
            y = -0.15 + 0.15 * j
            px = -0.6 + 0.5 * ease_in(u, 1.5) - 0.3 * volta
            bengala += T.lines([(px - 0.6, y + 0.1, px, y, 1.0)], 0.05) + T.gauss(px, y, 0.04) * 0.8
        toques += T.ring(0.1 + 0.18 * rel(t, t0 + 0.08, t0 + 0.25), 0.025, -0.1, -0.15 + 0.15 * j) * pulso(t, t0 + 0.08, t0 + 0.25)
    rabo = T.zero()
    kr = rel(t, 0.3, 0.45)
    if 0 < kr and t < 0.7:
        pts = [(-0.7 + 0.8 * s, 0.35 - 0.25 * math.sin(math.pi * s * ease_out(kr, 2))) for s in np.linspace(0, ease_out(kr, 2), 18)]
        rabo = T.polyline(pts, 0.025) * (1 - rel(t, 0.5, 0.7))
    est = _estrela_de_contato(T, t, 0.38, 0.2, 6, 0.32)
    G += (bengala * 1.0 + toques + rabo + est) * env
    H += (bengala * 0.5 + toques * 0.8 + rabo * 0.4 + est) * env
    return G, H


# ------------------------------------------------------------------ She-Ra
def espada_da_protecao_shera(T, t, rng):
    """She-Ra: a Espada da Proteção num corte largo e brilhante, e a joia do punho acende como uma estrela no acerto,
    soltando um arco de luz em leque."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    rastro, fio, ah = _arco_de_corte(T, t, 0.0, 0.22, -2.6, 0.7, 0.58, 0.15)
    ca, sa = math.cos(ah), math.sin(ah)
    espada = T.polys([(lamina(ca * 0.15, sa * 0.15, ca * 0.75, sa * 0.75, 0.05), 1.0)], 0.002) * (1 - rel(t, 0.24, 0.32))
    joia = T.polys([(estrela(0, 0, 0.12 * pulso(t, 0.2, 0.5) + 0.005, 0.0, 4, 0.4), 1.0)], 0.003) * pulso(t, 0.2, 0.5) * 1.3
    leque = T.zero()
    kl = pulso(t, 0.22, 0.6)
    if kl > 0:
        r = 0.25 + 0.35 * rel(t, 0.22, 0.6)
        leque = sum(T.arc_band(r + 0.05 * j, 0.03, -2.6 + 0.2 * j, -0.6 - 0.2 * j, crescente=True) for j in range(3)) * kl
    G += (T.glow(rastro, 1.0, 0.8, 0.03) + fio + espada * 1.2 + joia + leque) * env
    H += (fio * 1.4 + espada + joia * 1.4 + leque * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Wolverine
def garras_de_adamantium(T, t, rng):
    """Wolverine: o punho vem com as três garras de adamantium (o "snikt" com o brilho metálico na saída) e rasga o
    alvo deixando três riscos paralelos e fundos."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vem = ease_in(rel(t, 0.0, 0.18), 1.5)
    volta = ease_out(rel(t, 0.3, 0.6), 2)
    px = -0.95 + 0.7 * vem - 0.3 * volta
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.46, 0.6))
    punho = T.polys([(_elipse_pts(px, 0.0, 0.1, 0.12, 0.0, 14), 1.0), ([(px - 0.55, -0.08), (px - 0.05, -0.1), (px - 0.05, 0.1), (px - 0.55, 0.08)], 0.8)], 0.003)
    garras = T.polys([(lamina(px + 0.05, -0.07 + 0.07 * k, px + 0.42, -0.1 + 0.1 * k, 0.018), 1.0) for k in range(3)], 0.002)
    corpo = np.clip(punho + garras, 0, 1) * vis
    snikt = T.flare(px + 0.4, -0.12, 0.3, 0.3, 0.01) * pulso(t, 0.02, 0.12) * 1.2
    riscos = T.zero()
    kr = rel(t, 0.18, 0.26)
    if kr > 0:
        riscos = T.polys([(lamina(-0.35, -0.45 + 0.18 * k, 0.35, -0.05 + 0.18 * k, 0.035, ease_out(kr, 2.5), rel(t, 0.45, 0.7)), 1.0) for k in range(3)], 0.002)
    G += (corpo * 1.1 + snikt + T.glow(riscos, 1.1, 0.7, 0.02)) * env
    H += (corpo * 0.4 + garras * vis * 1.2 + snikt * 1.2 + riscos * 1.5) * env
    return G, H


# ------------------------------------------------------------------ Deadpool
def katanas_e_piadas(T, t, rng):
    """Deadpool: as duas katanas cortam em tesoura, e um balão de fala aparece em cima com a piada (os risquinhos de
    texto pulando dentro dele)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    cortes = T.zero()
    for j, (x1, y1, x2, y2) in enumerate(((-0.55, -0.4, 0.55, 0.2), (-0.55, 0.4, 0.55, -0.2))):
        k = rel(t, 0.0 + 0.06 * j, 0.12 + 0.06 * j)
        if k > 0:
            cortes += T.polys([(lamina(x1, y1, x2, y2, 0.04, ease_out(k, 2.5), rel(t, 0.3, 0.5)), 1.0)], 0.002)
    kb = pulso(t, 0.2, 0.8)
    balao = T.zero()
    texto = T.zero()
    if kb > 0:
        s = back(rel(t, 0.2, 0.32), 2.2)
        cx, cy = 0.35, -0.55
        balao = T.polys([(_elipse_pts(cx, cy, 0.26 * s + 0.01, 0.14 * s + 0.01, 0.0, 20), 1.0), ([(cx - 0.1 * s, cy + 0.1 * s), (cx - 0.18 * s, cy + 0.25 * s), (cx - 0.02 * s, cy + 0.12 * s)], 1.0)], 0.003) * kb
        balao -= T.polys([(_elipse_pts(cx, cy, 0.22 * s, 0.1 * s, 0.0, 20), 1.0)], 0.003) * kb * 0.85
        balao = np.clip(balao, 0, 1)
        pula = 0.015 * math.sin(t * 50)
        texto = T.lines([(cx - 0.14 + 0.07 * k, cy - 0.02 + pula * (1 if k % 2 else -1), cx - 0.09 + 0.07 * k, cy - 0.02, 1.0) for k in range(4)], 0.018) * kb * s
    G += (T.glow(cortes, 1.1, 0.7, 0.02) + balao + texto) * env
    H += (cortes * 1.5 + balao * 0.5 + texto * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Demolidor
def bastao_de_ricochete(T, t, rng):
    """Demolidor: o bastão vem girando, bate no alvo, quica para cima e volta; o sentido de radar desenha os anéis de
    eco em volta do alvo (como ele "vê" o mundo)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    pos = None
    if t < 0.2:
        u = ease_in(rel(t, 0.0, 0.2), 1.4)
        pos = (-0.95 + 0.95 * u, -0.1 + 0.1 * u)
    elif t < 0.5:
        u = rel(t, 0.2, 0.5)
        pos = (0.0 - 0.6 * u, -0.6 * math.sin(math.pi * u))
    bastao = T.zero()
    if pos:
        a = t * 30
        bastao = T.lines([(pos[0] - math.cos(a) * 0.18, pos[1] - math.sin(a) * 0.18, pos[0] + math.cos(a) * 0.18, pos[1] + math.sin(a) * 0.18, 1.0)], 0.055)
    ecos = T.zero()
    for j in range(3):
        ecos += _anel(T, t, 0.18 + 0.08 * j, 0.6 + 0.08 * j, 0.1, 0.6, 0.02)
    est = _estrela_de_contato(T, t, 0.2, 0.22, 6, 0.32)
    G += (bastao * 1.1 + ecos * 0.9 + est) * env
    H += (bastao * 0.6 + ecos * 0.4 + est) * env
    return G, H


# ------------------------------------------------------------------ Loki
def adaga_das_ilusoes(T, t, rng):
    """Loki: três Lokis de ilusão aparecem em volta do alvo, cada um com uma adaga; dois somem em fumaça verde e o de
    verdade crava a adaga."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    copias = T.zero()
    for j, a in enumerate((-2.4, -0.7, 1.6)):
        cx, cy = math.cos(a) * 0.55, math.sin(a) * 0.45
        some = 1 - rel(t, 0.18, 0.3) if j < 2 else 1 - rel(t, 0.3, 0.42)
        k = janela(t, 0.0 + 0.03 * j, 0.08 + 0.03 * j) * some
        if k > 0:
            copias += T.polys([(_elipse_pts(cx, cy, 0.07, 0.18, 0.0, 14), 1.0), (_elipse_pts(cx, cy - 0.22, 0.06, 0.06, 0.0, 10), 1.0)], 0.01) * k * 0.6
    fumaca = T.zero()
    kf = pulso(t, 0.18, 0.55)
    if kf > 0:
        for a in (-2.4, -0.7):
            cx, cy = math.cos(a) * 0.55, math.sin(a) * 0.45
            fumaca += T.gauss(cx, cy - 0.1 * rel(t, 0.18, 0.55), 0.12)
        fumaca *= kf * 0.5
    kd = rel(t, 0.22, 0.3)
    adaga = T.zero()
    if kd > 0 and t < 0.5:
        x0, y0 = math.cos(1.6) * 0.55, math.sin(1.6) * 0.45
        adaga = T.polys([(lamina(x0, y0, x0 * (1 - ease_out(kd, 2)), y0 * (1 - ease_out(kd, 2)) + 0.001, 0.035), 1.0)], 0.002) * (1 - rel(t, 0.38, 0.5))
    est = _estrela_de_contato(T, t, 0.3, 0.2, 6, 0.32)
    G += (copias + fumaca + adaga * 1.3 + est) * env
    H += (copias * 0.3 + fumaca * 0.2 + adaga * 1.3 + est) * env
    return G, H


# ------------------------------------------------------------------ Pain
def haste_negra_pain(T, t, rng):
    """Pain: a haste negra de chakra voa reta e crava no alvo, e os anéis do Rinnegan se abrem em volta, concêntricos e
    frios."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    vem = ease_in(rel(t, 0.0, 0.16), 1.6)
    px = -0.95 + 0.85 * vem
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.55, 0.7))
    haste = T.polys([(lamina(px - 0.6, 0.0, px + 0.1, 0.0, 0.03), 1.0)], 0.002) * vis
    farpas = T.lines([(px - 0.3 - 0.12 * k, 0.0, px - 0.36 - 0.12 * k, 0.06 * (1 if k % 2 else -1), 1.0) for k in range(3)], 0.01) * vis
    aneis = T.zero()
    for j in range(4):
        aneis += _anel(T, t, 0.16 + 0.05 * j, 0.7, 0.05 + 0.1 * j, 0.15 + 0.12 * j, 0.012) * 1.5
    est = _estrela_de_contato(T, t, 0.16, 0.2, 4, 0.25)
    G += (haste * 1.1 + farpas + aneis + est) * env
    H += (haste * 0.6 + farpas * 0.4 + aneis * 0.7 + est) * env
    return G, H


REGISTRO = [
    ("espada_do_heroi_finn", espada_do_heroi_finn, GRANDE, "básico do Finn: a espada dourada e as estrelinhas de desenho", False),
    ("bengala_do_mestre", bengala_do_mestre, GRANDE, "básico do Mestre Splinter: três batidinhas da bengala e o rabo", False),
    ("espada_da_protecao_shera", espada_da_protecao_shera, GRANDE, "básico da She-Ra: a Espada da Proteção e a joia", False),
    ("garras_de_adamantium", garras_de_adamantium, GRANDE, "básico do Wolverine: as três garras e os riscos fundos", False),
    ("katanas_e_piadas", katanas_e_piadas, GRANDE, "básico do Deadpool: as katanas em tesoura e o balão de piada", False),
    ("bastao_de_ricochete", bastao_de_ricochete, GRANDE, "básico do Demolidor: o bastão que quica e os ecos do radar", False),
    ("adaga_das_ilusoes", adaga_das_ilusoes, GRANDE, "básico do Loki: as cópias de ilusão e a adaga de verdade", False),
    ("haste_negra_pain", haste_negra_pain, GRANDE, "básico do Pain: a haste negra e os anéis do Rinnegan", False),
]
