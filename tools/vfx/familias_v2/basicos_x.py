"""Ataques básicos com animação própria, lote x: DIO, Giorno, Denji, Power, Homem-Formiga, Motoqueiro Fantasma,
Vampira e Venom.

Golpes simples, cada um do personagem: a mão do DIO apertando o rival e puxando as gotas de sangue (o Toque
vampírico), o soco do Giorno que faz brotar folhas e flores no ponto do golpe, o soco do Denji com os dentes da
serra correndo no antebraço e o sangue espirrando, o punho da Power com espinhos de sangue, o punho minúsculo do
Homem-Formiga que fica gigante no último instante, o punho de osso em chamas do Motoqueiro, a luva verde da
Vampira com a força que ela pegou emprestada e a patada do Venom com o simbionte grudando.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, janela, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_u import _anel, _antebraco, _estrela_de_contato, _mao, _pts, _riscos, _vai_e_volta
from .basicos_w import _soco


def _gotas(T, t, t0, dur, n, seed, de=None, para=(0.0, 0.0), tam=0.03, cai=0.4, alcance=0.5, a0=-2.2, a1=2.2):
    """Gotas espirrando (de=None: saem do centro e caem) ou voando de `de` para `para`."""
    u = rel(t, t0, t0 + dur)
    if u <= 0 or u >= 1:
        return T.zero()
    q = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        if de is None:
            a = q.uniform(a0, a1)
            d = q.uniform(0.25, 1.0) * alcance * ease_out(u, 2)
            pts.append((d * math.cos(a), d * math.sin(a) + cai * u * u, (1 - u) * q.uniform(0.6, 1.1)))
        else:
            atraso = q.uniform(0, 0.4)
            v = min(1, max(0, (u - atraso) / 0.6))
            ox, oy = de[0] + q.uniform(-0.25, 0.25), de[1] + q.uniform(-0.25, 0.25)
            pts.append((ox + (para[0] - ox) * ease_in(v, 1.6), oy + (para[1] - oy) * ease_in(v, 1.6), (1 - v) * 0.9 if v > 0 else 0.6))
    return T.splats(pts, tam)


# ------------------------------------------------------------------ DIO
_GARRA_ABERTA = [(-0.14, -0.12), (0.0, -0.13), (0.06, -0.2), (0.12, -0.21), (0.1, -0.13), (0.2, -0.14), (0.26, -0.1),
                 (0.18, -0.05), (0.28, -0.03), (0.3, 0.02), (0.18, 0.03), (0.24, 0.08), (0.2, 0.12), (0.06, 0.08), (-0.14, 0.1)]


def toque_vampirico_dio(T, t, rng):
    """DIO: a mão aberta, dedos em garra, crava no rival e aperta; as gotas de sangue saem do alvo e correm para
    a mão, que brilha mais a cada gota (o vampiro se alimentando)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    u = ease_in(rel(t, 0.0, 0.2), 1.5)
    px = -0.92 + 0.72 * u - 0.3 * ease_out(rel(t, 0.62, 0.84), 2)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.68, 0.84))
    aperta = pulso(t, 0.2, 0.62) * 0.08
    mao = T.polys([(_pts(_GARRA_ABERTA, px, 0.0, 1.25 - aperta), 1.0)], 0.004)
    A, B = _antebraco(T, px, 0.0, 1.2, 0.42, 0.1, (0.0, 0.08))
    corpo = np.clip(mao + A, 0, 1) * vis
    t0 = 0.2
    cravou = T.zero()
    kc = pulso(t, t0, t0 + 0.4)
    if kc > 0:
        for (dx, dy) in [(0.15, -0.22), (0.3, -0.16), (0.36, -0.03), (0.3, 0.1)]:
            cravou += T.gauss(px + dx, dy, 0.025)
        cravou *= kc
    gotas = _gotas(T, t, t0 + 0.04, 0.5, 14, 33, de=(0.15, 0.05), para=(px + 0.05, 0.0), tam=0.03)
    brilho = T.gauss(px + 0.05, 0.0, 0.14) * janela(t, 0.3, 0.55) * (1 - rel(t, 0.6, 0.75)) * 1.3
    est = _estrela_de_contato(T, t, t0, 0.22, 8, 0.4)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + gotas * 1.6 + brilho + est) * env
    H += (corpo * 0.3 + B * 0.8 + cravou * 1.6 + gotas * 0.6 + brilho * 0.6 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Giorno
def _flor(T, cx, cy, r, ang=0.0, n=5):
    petalas = [(_elipse_pts(cx + r * 0.6 * math.cos(ang + TAU * k / n), cy + r * 0.6 * math.sin(ang + TAU * k / n), r * 0.55, r * 0.3, ang + TAU * k / n, 10), 1.0)
               for k in range(n)]
    return T.polys(petalas, 0.003), T.gauss(cx, cy, r * 0.28)


def soco_da_vida_giorno(T, t, rng):
    """Giorno: um soco limpo e, no ponto do golpe, a vida brota: um broto sobe enrolando, abre folhas e duas
    flores de cinco pétalas (o Gold Experience dando vida até ao ar)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.2, 0.2, 1.05)
    t0 = 0.2
    est = _estrela_de_contato(T, t, t0, 0.26, 8, 0.4)
    cresce = ease_out(rel(t, t0 + 0.05, t0 + 0.4), 2)
    vida = janela(t, t0 + 0.05, t0 + 0.1) * apaga(t, 0.72, 0.92)
    planta = T.zero()
    flores_g, flores_h = T.zero(), T.zero()
    if cresce > 0 and vida > 0:
        pts = [(0.1 * math.sin(s * 7) * s, 0.15 - 0.7 * s * cresce) for s in np.linspace(0, 1, 18)]
        planta += T.polyline(pts, 0.028)
        for (s, lado) in [(0.35, 1), (0.6, -1)]:
            x, y = pts[int(s * 17)]
            planta += T.polys([(_elipse_pts(x + lado * 0.1 * cresce, y, 0.1 * cresce + 0.005, 0.042 * cresce + 0.003, lado * 0.5, 10), 1.0)], 0.003)
        abre = ease_out(rel(t, t0 + 0.25, t0 + 0.45), 2)
        if abre > 0:
            for (cx, cy, r, a) in [(pts[-1][0], pts[-1][1], 0.16, 0.3), (0.26, -0.14, 0.12, 1.0)]:
                g, h = _flor(T, cx, cy, r * abre, a + t * 2)
                flores_g += g
                flores_h += h
        planta *= vida
        flores_g *= vida
        flores_h *= vida
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + est + planta * 1.3 + flores_g * 1.3) * env
    H += (corpo * 0.3 + d * 0.8 + est * 0.9 + planta * 0.4 + flores_g * 0.5 + flores_h * 2.0) * env
    return G, H


# ------------------------------------------------------------------ Denji
def soco_serrilhado(T, t, rng):
    """Denji: um soco de briga com os dentes da serra correndo pela beirada do antebraço e, no acerto, o sangue
    espirrando em gotas grossas que caem."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.2, 0.18, 1.1)
    dentes = T.zero()
    if vis > 0.05:
        polys = []
        corre = (t * 6) % 1
        for k in range(7):
            x = px - 0.12 - 0.06 * ((k + corre) % 7)
            polys.append(([(x - 0.025, -0.13), (x + 0.025, -0.13), (x, -0.2)], 1.0))
        dentes = T.polys(polys, 0.003) * vis
    t0 = 0.2
    sangue = _gotas(T, t, t0, 0.6, 16, 47, tam=0.034, cai=0.55, alcance=0.55, a0=-2.4, a1=1.0)
    mancha = T.gauss(0, 0, 0.1) * pulso(t, t0, t0 + 0.3) * 1.5
    est = _estrela_de_contato(T, t, t0, 0.3, 7, 0.32, 0.2, 0.3)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + dentes * 1.3 + sangue * 1.5 + mancha + est) * env
    H += (corpo * 0.3 + d * 0.8 + dentes * 1.2 + sangue * 0.35 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Power
def punho_de_sangue_power(T, t, rng):
    """Power: o sangue sobe do braço e endurece em espinhos nos nós dos dedos; o soco crava com os espinhos e o
    sangue estoura em volta em gotas que caem."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    corpo, d, _, px, vis = _soco(T, t, 0.22, 0.18, 1.1)
    forma = janela(t, 0.04, 0.18)
    espinhos = T.zero()
    if forma > 0:
        polys = []
        for k in range(4):
            y = (-0.13 + 0.087 * k) * 1.1
            comp = 0.14 * forma
            polys.append(([(px + 0.15, y - 0.03), (px + 0.15, y + 0.03), (px + 0.15 + comp, y)], 1.0))
        polys.append(([(px - 0.02, -0.17), (px + 0.06, -0.17), (px + 0.02, -0.17 - 0.12 * forma)], 1.0))
        espinhos = T.polys(polys, 0.003) * vis
    escorre = T.zero()
    if vis > 0.05:
        for k in range(3):
            fase = (t * 2.5 + k / 3) % 1
            escorre += T.gauss(px - 0.25 - 0.1 * k, 0.12 + 0.25 * fase, 0.022) * (1 - fase)
        escorre *= vis
    t0 = 0.22
    sangue = _gotas(T, t, t0, 0.6, 18, 52, tam=0.032, cai=0.5, alcance=0.6, a0=0.0, a1=TAU)
    est = _estrela_de_contato(T, t, t0, 0.34, 6, 0.25, 0.3, 0.3)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + espinhos * 1.4 + escorre * 1.3 + sangue * 1.5 + est) * env
    H += (corpo * 0.3 + d * 0.6 + espinhos * 1.1 + escorre * 0.3 + sangue * 0.3 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Homem-Formiga
def soco_formiga(T, t, rng):
    """Homem-Formiga: um punho do tamanho de uma formiga atravessa a tela rapidinho e, no último instante, cresce
    para um soco gigante (o "crescer" das partículas Pym), estourando com um anel enorme."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    u = ease_in(rel(t, 0.0, 0.22), 1.3)
    px = -0.95 + 0.82 * u - 0.15 * ease_out(rel(t, 0.32, 0.62), 2)
    cresce = ease_out(rel(t, 0.15, 0.24), 2.5)
    esc = 0.25 + 1.05 * cresce
    vis = janela(t, 0.0, 0.03) * (1 - rel(t, 0.5, 0.66))
    M, d = _mao(T, px, 0.0, esc)
    A, B = _antebraco(T, px, 0.0, esc, 0.42, 0.11)
    corpo = np.clip(M + A, 0, 1) * vis
    # os anéis do capacete encolhendo/crescendo e as partículas Pym em volta do punho
    pym = T.zero()
    kp = pulso(t, 0.1, 0.32)
    if kp > 0:
        for k in range(3):
            pym += T.ring(0.05 + 0.1 * k * esc, 0.012, px, 0.0, 1.0)
        pym *= kp
    rastro = T.zero()
    if 0.02 < u < 1 and cresce < 0.5:
        rastro = T.tapered([(px - 0.35, 0.0, px - 0.03, 0.0, 1.0)], 0.03) * (1 - cresce * 2)
    t0 = 0.24
    onda = _anel(T, t, t0, t0 + 0.5, 0.15, 0.8, 0.06, 1.3)
    est = _estrela_de_contato(T, t, t0, 0.42, 8, 0.4, 0.1, 0.36)
    clarao = T.gauss(0, 0, 0.2) * pulso(t, t0, t0 + 0.2) * 2.0
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + pym * 1.4 + rastro * 1.2 + onda * 1.3 + est * 1.1 + clarao) * env
    H += (corpo * 0.3 + d * vis * 0.7 + pym * 1.0 + rastro * 0.8 + onda * 0.4 + est + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Motoqueiro Fantasma
def soco_de_osso_em_chamas(T, t, rng):
    """Motoqueiro Fantasma: o punho é só osso (os quatro dedos em falanges e os ossos do antebraço) envolto em
    fogo do inferno que sobe em línguas; o acerto espalha brasas que sobem."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    px = _vai_e_volta(t, 0.22, recua=0.18)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.48, 0.64))
    e = 1.15
    ossos = []
    for k in range(4):
        y = (-0.12 + 0.08 * k) * e
        ossos += [(px - 0.05 * e, y, px + 0.06 * e, y - 0.01, 1.0), (px + 0.07 * e, y - 0.01, px + 0.14 * e, y + 0.02, 1.0)]
    ossos += [(px - 0.12 * e, -0.06 * e, px - 0.5 * e, -0.05 * e, 1.0), (px - 0.12 * e, 0.06 * e, px - 0.5 * e, 0.07 * e, 1.0)]
    O = T.lines(ossos, 0.032 * e) + T.gauss(px - 0.08 * e, 0.0, 0.07, 0.11) * 1.2
    juntas = sum(T.gauss(px + dx * e, (-0.12 + 0.08 * k) * e, 0.016) for k in range(4) for dx in (0.06, 0.14))
    corpo = np.clip(O, 0, 1) * vis
    fogo = T.zero()
    if vis > 0.05:
        segs = []
        for j in range(12):
            x0 = px - 0.5 + 0.055 * j
            alto = 0.13 + 0.08 * math.sin(t * 36 + j * 1.9)
            segs.append((x0, -0.12, x0 - 0.08, -0.12 - alto, 1.0))
        fogo = T.tapered(segs, 0.05) * vis
    t0 = 0.22
    brasas = _gotas(T, t, t0, 0.65, 16, 66, tam=0.022, cai=-0.5, alcance=0.5, a0=-3.0, a1=0.2)
    est = _estrela_de_contato(T, t, t0, 0.3, 8, 0.38, 0.2, 0.3)
    clarao = T.gauss(0, 0, 0.17) * pulso(t, t0, t0 + 0.2) * 1.8
    G += (corpo * 1.0 + fogo * 1.3 + T.blur(fogo, 0.02) * 0.5 + brasas * 1.5 + est + clarao) * env
    H += (corpo * 0.9 + juntas * vis * 1.5 + fogo * 0.35 + brasas * 0.9 + est * 0.9 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Vampira
def soco_de_luva_da_vampira(T, t, rng):
    """Vampira: a luva comprida de couro (o punho sem pele à mostra) chega voando num soco com a força que ela
    pegou emprestada, deixando o rastro de voo, e o acerto abre dois anéis de choque, um em cima do outro."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.2, 0.16, 1.1, 'luva', comp=0.6, larg=0.1, faixa=(0.62, 0.08))
    voo = T.zero()
    if vis > 0.05:
        voo = T.tapered([(px - 1.2, -0.02, px - 0.5, 0.0, 1.0), (px - 1.0, 0.1, px - 0.55, 0.08, 0.6)], 0.09) * (1 - rel(t, 0.16, 0.3))
    t0 = 0.2
    aneis = _anel(T, t, t0, t0 + 0.45, 0.12, 0.7, 0.06, 1.3) + _anel(T, t, t0 + 0.07, t0 + 0.5, 0.08, 0.5, 0.04, 1.3)
    est = _estrela_de_contato(T, t, t0, 0.36, 8, 0.36, 0.0, 0.32)
    clarao = T.gauss(0, 0, 0.18) * pulso(t, t0, t0 + 0.18) * 2.1
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + voo * 0.8 + aneis * 1.3 + est * 1.1 + clarao) * env
    H += (corpo * 0.35 + (d + B) * 0.8 + voo * 0.4 + aneis * 0.45 + est + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Venom
_PATA = [(-0.18, -0.14), (0.02, -0.16), (0.12, -0.24), (0.16, -0.2), (0.14, -0.12), (0.24, -0.14), (0.28, -0.08),
         (0.2, -0.04), (0.3, 0.0), (0.28, 0.06), (0.18, 0.06), (0.24, 0.12), (0.18, 0.16), (0.04, 0.14), (-0.18, 0.14)]


def patada_simbionte(T, t, rng):
    """Venom: a mão preta enorme do simbionte, com garras, vem num tapa pesado de cima; no acerto o simbionte
    gruda: fios pegajosos se esticam entre a pata e o alvo e respingos de gosma voam."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    u = ease_in(rel(t, 0.0, 0.24), 1.8)
    px, py = -0.92 + 0.78 * u - 0.32 * ease_out(rel(t, 0.36, 0.7), 2), -0.3 + 0.3 * u
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.62, 0.78))
    pata = T.polys([(_pts(_PATA, px, py, 1.35, 0.3 * (1 - u)), 1.0)], 0.004)
    braco = T.polys([(_pts([(-0.16, -0.13), (-0.62, -0.15), (-0.62, 0.15), (-0.16, 0.13)], px, py, 1.35, 0.3 * (1 - u)), 0.8)], 0.006)
    corpo = np.clip(pata + braco, 0, 1) * vis
    garras = T.zero()
    if vis > 0.05:
        for (dx, dy) in [(0.12, -0.24), (0.24, -0.14), (0.3, 0.0), (0.24, 0.12)]:
            x, y = _pts([(dx, dy)], px, py, 1.35, 0.3 * (1 - u))[0]
            garras += T.gauss(x, y, 0.02)
        garras *= vis
    t0 = 0.24
    fios = T.zero()
    kf = janela(t, t0 + 0.12, t0 + 0.18) * (1 - rel(t, t0 + 0.35, t0 + 0.5))
    if kf > 0:
        segs = []
        for k in range(4):
            y0 = -0.12 + 0.08 * k
            meio = 0.05 * math.sin(k * 2 + t * 10)
            segs += [(px + 0.1, py + y0, (px + 0.1) / 2, y0 * 0.5 + meio, 0.7), ((px + 0.1) / 2, y0 * 0.5 + meio, 0.05, y0 * 0.4, 0.7)]
        fios = T.lines(segs, 0.016) * kf
    gosma = _gotas(T, t, t0, 0.55, 12, 71, tam=0.036, cai=0.45, alcance=0.55, a0=-2.6, a1=1.4)
    est = _estrela_de_contato(T, t, t0, 0.34, 7, 0.32, 0.3, 0.32)
    G += (corpo * 1.0 + T.blur(corpo, 0.025) * 0.4 + fios * 1.3 + gosma * 1.5 + est) * env
    H += (corpo * 0.15 + garras * 1.6 + fios * 0.5 + gosma * 0.3 + est * 0.9) * env
    return G, H


REGISTRO = [
    ("toque_vampirico_dio", toque_vampirico_dio, GRANDE, "básico do DIO: a mão em garra que crava e puxa o sangue", False),
    ("soco_da_vida_giorno", soco_da_vida_giorno, GRANDE, "básico do Giorno: o soco e a planta com flores brotando", False),
    ("soco_serrilhado", soco_serrilhado, GRANDE, "básico do Denji: os dentes da serra no braço e o sangue espirrando", False),
    ("punho_de_sangue_power", punho_de_sangue_power, GRANDE, "básico da Power: espinhos de sangue nos nós dos dedos", False),
    ("soco_formiga", soco_formiga, GRANDE, "básico do Homem-Formiga: o punho minúsculo que fica gigante", False),
    ("soco_de_osso_em_chamas", soco_de_osso_em_chamas, GRANDE, "básico do Motoqueiro Fantasma: punho de osso em chamas e brasas", False),
    ("soco_de_luva_da_vampira", soco_de_luva_da_vampira, GRANDE, "básico da Vampira: a luva comprida, o rastro de voo e os dois anéis", False),
    ("patada_simbionte", patada_simbionte, GRANDE, "básico do Venom: a pata com garras e os fios de gosma", False),
]
