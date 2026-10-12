"""Rodada 6 das habilidades próprias: Yuji, Megumi, Nobara, Sukuna (Jujutsu Kaisen) e Ichigo (Bleach).

Yuji
- vontade_indomavel: a Vontade Indomável — o círculo do Preparo do rival (o anel com as runas)
  aparece, o punho chega com o rastro de energia amaldiçoada, o anel trinca em rachaduras e
  estoura em cacos que voam.

Megumi
- nue: o Nue — as duas asas enormes da coruja se abrem por cima (as penas em leque), e os raios
  descem em três pontos, um depois do outro, com o anel elétrico no chão.
- jardim_das_sombras: o Jardim das Sombras — o chão vira uma poça preta que ondula, as mãos de
  sombra sobem da poça e fecham em volta do rival.

Nobara
- pregos_amaldicoados: três pregos voam em leque, cravam no rival um depois do outro (a cabeça do
  prego acende) e a energia amaldiçoada sai em fios que prendem.
- ressonancia_amaldicoada: a Ressonância — o boneco de palha no centro, o prego cravado no peito
  dele, e a onda de ressonância sai em anéis com espinhos.
- grampo_de_cabelo: o Grampo — os pregos cravados piscam e explodem em sequência, cada um com o
  clarão em estrela e os estilhaços.

Sukuna
- cleave: o Cleave — as marcas de medida cercam o alvo (os colchetes que fecham), e um corte só,
  enorme, atravessa; o rastro se abre em duas metades.
- santuario_preparo: o Preparo do Santuário — as mãos fazem o selo e o santuário (o telhado
  curvo e as bocas) se forma por cima, pulsando (laço).
- santuario_maligno: o Santuário Maligno — o santuário ao fundo e os cortes enchem a área toda,
  dezenas, de todos os ângulos, ao mesmo tempo.

Ichigo
- mascara_hollow: a Máscara Hollow — a máscara branca se forma (a meia-lua do rosto, os olhos e as
  listras vermelhas), e a pressão espiritual preta e vermelha explode em volta.
- bankai_preparo: o Preparo do Bankai — o redemoinho da pressão espiritual subindo em espiral (laço).
- bankai_ichigo: o Getsuga Tenshou do Bankai — a meia-lua preta com a borda vermelha, enorme,
  avança e corta, e o rastro preto fica no ar.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _estilhacos(T, t, seed, n, t0, alcance=0.8, larg=0.02, cx=0.0, cy=0.0, gravidade=0.25):
    """Cacos triangulares que voam do centro, girando e caindo."""
    sub = np.random.default_rng(seed)
    shapes = []
    tt = rel(t, t0, 1.0)
    if tt <= 0:
        return T.zero()
    for _ in range(n):
        a = sub.uniform(0, TAU)
        v = sub.uniform(0.4, 1.0) * alcance
        d = v * ease_out(tt, 1.8)
        x, y = cx + d * math.cos(a), cy + d * math.sin(a) + gravidade * tt * tt
        r = larg * sub.uniform(0.7, 1.6)
        g = sub.uniform(0, TAU) + tt * sub.uniform(-8, 8)
        tri = [(x + r * math.cos(g), y + r * math.sin(g)), (x + r * 0.6 * math.cos(g + 2.3), y + r * 0.6 * math.sin(g + 2.3)),
               (x + r * 0.8 * math.cos(g + 4.1), y + r * 0.8 * math.sin(g + 4.1))]
        shapes.append((tri, (1 - tt) ** 1.2))
    return T.polys(shapes)


def _raio(T, q, x1, y1, x2, y2, larg=0.012, depth=4, rough=0.3):
    return T.polyline(jagged(q, x1, y1, x2, y2, depth, rough), larg)


# =================================================================== Yuji
def vontade_indomavel(T, t, rng):
    """O anel do Preparo do rival (com as marquinhas de runa girando), o punho chega com o rastro de
    energia, o anel trinca de dentro para fora e estoura em cacos; o clarão do soco fica no centro."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    gira = t * 2.5
    antes = 1 - rel(t, 0.32, 0.4)
    anel = T.ring(0.5, 0.025) * 0.9
    marcas = T.zero()
    for k in range(12):
        a = gira + TAU * k / 12
        x, y = 0.5 * math.cos(a), 0.5 * math.sin(a)
        marcas += T.lines([(x * 0.9, y * 0.9, x * 1.1, y * 1.1, 1.0)], 0.014)
    G += (anel + marcas * 0.8) * antes * (0.5 + 0.5 * rel(t, 0.0, 0.15))
    # o punho: o rastro de energia amaldiçoada vindo de baixo à esquerda
    chega = ease_in(rel(t, 0.12, 0.34), 2)
    if 0 < chega < 1 or 0.12 < t < 0.36:
        hx, hy = -0.85 + 0.85 * chega, 0.55 - 0.55 * chega
        rastro = T.tapered([(hx - 0.55, hy + 0.35, hx, hy, 1.0), (hx - 0.45, hy + 0.42, hx - 0.02, hy + 0.05, 0.6),
                            (hx - 0.5, hy + 0.25, hx + 0.02, hy - 0.04, 0.6)], 0.16)
        G += T.blur(rastro, 0.02) * 1.2 + rastro * 0.8
        H += rastro * 0.5 + T.gauss(hx, hy, 0.1) * 1.6
        G += T.gauss(hx, hy, 0.14) * 1.2
    # as rachaduras no anel e o estouro
    trinca = rel(t, 0.34, 0.5)
    if trinca > 0:
        q = np.random.default_rng(61)
        for k in range(7):
            a = TAU * k / 7 + 0.3
            comp = 0.15 + 0.5 * trinca
            G += _raio(T, q, 0.04 * math.cos(a), 0.04 * math.sin(a), comp * math.cos(a), comp * math.sin(a), 0.012, 3, 0.4) * (1 - rel(t, 0.5, 0.7)) * 1.3
    G += _estilhacos(T, t, 66, 26, 0.42, 0.95, 0.035) * 1.2 * env
    choque = rel(t, 0.36, 0.75)
    G += T.ring(0.15 + 0.75 * ease_out(choque, 2), 0.05) * (1 - choque) * 1.2 * (t > 0.36)
    clarao = pulso(t, 0.33, 0.62)
    G += T.gauss(0, 0, 0.18) * clarao * 1.6
    H += (T.gauss(0, 0, 0.07) * clarao * 2 + T.flare(0, 0, 0.9 * clarao + 0.01, 0.4, 0.02) * clarao) * env
    return G * env, H


# =================================================================== Megumi
def _asa(lado, abre, larg=0.95):
    """Uma asa de penas em leque (lado 1 = direita), saindo do ombro da coruja."""
    penas = []
    for k in range(7):
        u = k / 6
        a = (-0.15 - 1.1 * u) * abre if lado == 1 else math.pi + (0.15 + 1.1 * u) * abre
        comp = larg * (1 - 0.35 * u)
        x0, y0 = 0.08 * lado, -0.38
        penas.append(lamina(x0, y0, x0 + comp * math.cos(a), y0 + comp * math.sin(a) * 0.85 + 0.12 * u, 0.085 - 0.035 * u))
    return penas


def nue(T, t, rng):
    """O Nue: as asas da coruja se abrem por cima (as penas em leque, com o corpo e os olhos), e os
    raios caem em três pontos, um depois do outro, cada um com o anel elétrico no chão."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    abre = back(rel(t, 0.0, 0.3), 1.4)
    some = 1 - 0.6 * rel(t, 0.55, 0.85)
    penas = [(p, 1.0) for lado in (1, -1) for p in _asa(lado, abre)]
    asas = T.polys(penas) if abre > 0.02 else T.zero()
    corpo = T.gauss(0, -0.38, 0.07, 0.1) * min(1, abre * 2)
    olhos = (T.gauss(-0.03, -0.42, 0.012) + T.gauss(0.03, -0.42, 0.012)) * pulso(t, 0.1, 0.9)
    G += (np.clip(asas, 0, 1) * 0.55 + T.blur(asas, 0.02) * 0.4 + corpo) * some
    H += (np.clip(asas - T.blur(asas, 0.01), 0, 1) * 0.6 * abre + olhos * 2) * some
    for k, x in enumerate((-0.5, 0.1, 0.55)):
        t0 = 0.28 + 0.12 * k
        cai = pulso(t, t0, t0 + 0.25)
        if cai <= 0:
            continue
        q = np.random.default_rng(70 + k + int(t * 30))
        bolt = _raio(T, q, x * 0.3, -0.3, x, 0.45, 0.014, 5, 0.35)
        G += (bolt * 1.4 + T.blur(bolt, 0.025) * 0.8) * cai
        H += bolt * cai * 1.2
        anel = rel(t, t0 + 0.03, t0 + 0.4)
        G += T.ring(0.05 + 0.25 * anel, 0.02, x, 0.47, squash=3.0) * (1 - anel) * 1.4 * (t > t0)
        G += T.gauss(x, 0.47, 0.1, 0.04) * cai
    return G * env, H * env


def jardim_das_sombras(T, t, rng):
    """O Jardim das Sombras: a poça preta abre no chão com as ondas, as mãos de sombra sobem (dedos
    abertos) e se fecham em volta do rival; o contorno da poça brilha, o miolo fica escuro."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    abre = ease_out(rel(t, 0.0, 0.35), 2)
    poca = T.gauss(0, 0.42, 0.62 * abre + 0.01, 0.16 * abre + 0.005)
    borda = np.clip(T.ring(0.6 * abre, 0.03, 0, 0.42, squash=3.6) * abre, 0, 1)
    ondas = T.zero()
    for k in range(3):
        u = (t * 1.4 + k / 3) % 1
        ondas += T.ring(0.15 + 0.55 * u * abre, 0.012, 0, 0.42, squash=3.6) * (1 - u) * abre
    G += borda * 1.1 + ondas * 0.6 + poca * 0.25
    H += borda * 0.3
    # as mãos: cinco, sobem da poça e fecham para o centro
    sobe = ease_out(rel(t, 0.2, 0.55), 2)
    fecha = ease_in(rel(t, 0.5, 0.72), 2)
    maos = T.zero()
    for k, bx in enumerate((-0.45, -0.22, 0.0, 0.22, 0.45)):
        if sobe <= 0:
            break
        alt = (0.55 + 0.15 * math.cos(k)) * sobe
        topo_x = bx * (1 - 0.75 * fecha)
        topo_y = 0.4 - alt
        braco = []
        for u in np.linspace(0, 1, 14):
            x = bx + (topo_x - bx) * u ** 1.5 + 0.05 * math.sin(u * 7 + k * 1.3 + t * 9) * (1 - u)
            braco.append((x, 0.42 - alt * u))
        maos += T.polyline(braco, 0.065 - 0.02 * 0)
        maos += T.gauss(topo_x, topo_y, 0.05, 0.045) * 1.2
        ang = math.atan2(topo_y - braco[-3][1], topo_x - braco[-3][0])
        for d in range(5):
            a = ang + (-0.9 + 0.45 * d) * (1 - 0.55 * fecha)
            m1 = (topo_x + 0.09 * math.cos(a), topo_y + 0.09 * math.sin(a))
            m2 = (m1[0] + 0.08 * math.cos(a + 0.5 * fecha + 0.2), m1[1] + 0.08 * math.sin(a + 0.5 * fecha + 0.2))
            maos += T.polyline([(topo_x, topo_y), m1, m2], 0.024)
    G += (T.blur(maos, 0.015) * 1.4 + maos * 0.5) * (1 - rel(t, 0.72, 0.9))
    aperta = pulso(t, 0.62, 0.95)
    G += T.ring(0.2 - 0.08 * aperta, 0.03, 0, -0.05) * aperta * 1.2
    # o escuro: o miolo da poça e das mãos tira luz (sombra de verdade, não brilho)
    G -= (poca * 0.35 + np.clip(maos, 0, 1) * 0.25) * abre
    return G * env, H * env


# =================================================================== Nobara
def _prego(x, y, ang, comp=0.32, larg=0.03):
    """O prego: a haste fina e a cabeça larga (em pé na direção `ang`, ponta para frente)."""
    c, s = math.cos(ang), math.sin(ang)
    nx, ny = -s, c
    haste = [(x + c * comp, y + s * comp), (x + nx * larg * 0.45, y + ny * larg * 0.45), (x - nx * larg * 0.45, y - ny * larg * 0.45)]
    cabeca = [(x + nx * larg * 1.4, y + ny * larg * 1.4), (x + nx * larg * 1.4 - c * 0.025, y + ny * larg * 1.4 - s * 0.025),
              (x - nx * larg * 1.4 - c * 0.025, y - ny * larg * 1.4 - s * 0.025), (x - nx * larg * 1.4, y - ny * larg * 1.4)]
    return [(haste, 1.0), (cabeca, 1.0)]


def pregos_amaldicoados(T, t, rng):
    """Três pregos voam em leque e cravam no rival, um depois do outro; a cabeça de cada um acende e
    a energia amaldiçoada sai em fios que se enrolam no corpo (o Preso)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    destinos = ((-0.12, -0.15), (0.08, 0.02), (-0.04, 0.2))
    for k, (dx, dy) in enumerate(destinos):
        t0 = 0.04 * k
        voa = ease_in(rel(t, t0, t0 + 0.28), 1.6)
        ox, oy = -0.95, -0.55 + 0.45 * k
        x, y = ox + (dx - ox) * voa, oy + (dy - oy) * voa
        ang = math.atan2(dy - oy, dx - ox)
        cravou = t > t0 + 0.28
        recua = 0.12 if cravou else 0.0
        P = T.polys(_prego(x - math.cos(ang) * (0.24 - recua), y - math.sin(ang) * (0.24 - recua), ang))
        G += P * 1.1 + T.blur(P, 0.015) * 0.5
        if not cravou:
            G += T.tapered([(x - math.cos(ang) * 0.45, y - math.sin(ang) * 0.45, x - math.cos(ang) * 0.2, y - math.sin(ang) * 0.2, 0.7)], 0.03) * voa
        acende = pulso(t, t0 + 0.28, t0 + 0.6)
        cx, cy = x - math.cos(ang) * (0.24 - recua), y - math.sin(ang) * (0.24 - recua)
        G += T.gauss(cx, cy, 0.05) * acende * 1.6
        H += (T.gauss(cx, cy, 0.025) * 1.5 + T.flare(cx, cy, 0.4 * acende + 0.01, 0.6, 0.02)) * acende
    fios = rel(t, 0.38, 0.75)
    if fios > 0:
        for k in range(3):
            pts = []
            for u in np.linspace(0, fios, 30):
                a = TAU * (u * 1.6 + k / 3)
                r = 0.42 - 0.1 * u
                pts.append((r * math.cos(a), 0.02 + r * math.sin(a) * 0.55))
            G += T.polyline(pts, 0.014) * 1.0 * (1 - rel(t, 0.75, 0.95))
    return G * env, H * env


def _boneco(T, cx, cy, s=1.0):
    """O boneco de palha: a cabeça amarrada, os braços abertos e as pernas, de fios trançados."""
    segs = [(cx, cy - 0.28 * s, cx, cy + 0.14 * s, 1.0),
            (cx - 0.22 * s, cy - 0.08 * s, cx + 0.22 * s, cy - 0.08 * s, 1.0),
            (cx, cy + 0.14 * s, cx - 0.13 * s, cy + 0.36 * s, 1.0),
            (cx, cy + 0.14 * s, cx + 0.13 * s, cy + 0.36 * s, 1.0)]
    corpo = T.lines(segs, 0.05) + T.gauss(cx, cy - 0.3 * s, 0.06 * s, 0.07 * s) * 1.5
    palha = T.lines([(cx - 0.24 * s, cy - 0.12 * s, cx - 0.3 * s, cy - 0.06 * s, 0.7), (cx + 0.24 * s, cy - 0.12 * s, cx + 0.3 * s, cy - 0.06 * s, 0.7),
                     (cx - 0.05 * s, cy - 0.38 * s, cx - 0.09 * s, cy - 0.45 * s, 0.7), (cx + 0.05 * s, cy - 0.38 * s, cx + 0.09 * s, cy - 0.45 * s, 0.7)], 0.012)
    return np.clip(corpo, 0, 1), palha


def ressonancia_amaldicoada(T, t, rng):
    """A Ressonância: o boneco de palha aparece, o martelo crava o prego no peito dele (o clarão), e a
    onda de ressonância sai em anéis com espinhos, um atrás do outro, até a borda (em todos)."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    surge = ease_out(rel(t, 0.0, 0.2), 2)
    corpo, palha = _boneco(T, 0, 0.0, 0.9)
    G += (corpo * 0.8 + palha * 0.8 + T.blur(corpo, 0.02) * 0.4) * surge * (1 - 0.5 * rel(t, 0.6, 0.9))
    crava = ease_in(rel(t, 0.15, 0.28), 2)
    if t < 0.4:
        P = T.polys(_prego(0.42 - 0.35 * crava, -0.07, math.pi, 0.22, 0.02))
        G += P * 1.2
    batida = pulso(t, 0.27, 0.45)
    G += T.gauss(0.07, -0.07, 0.08) * batida * 2
    H += (T.flare(0.07, -0.07, 0.8 * batida + 0.01, 0.2, 0.02) + T.gauss(0.07, -0.07, 0.03) * 2) * batida
    for k in range(3):
        t0 = 0.3 + 0.12 * k
        u = rel(t, t0, t0 + 0.5)
        if u <= 0 or u >= 1:
            continue
        r = 0.12 + 0.85 * ease_out(u, 1.5)
        G += T.ring(r, 0.03) * (1 - u) * 1.3
        espinhos = []
        for j in range(16):
            a = TAU * j / 16 + k * 0.2
            espinhos.append((r * math.cos(a), r * math.sin(a), (r + 0.07) * math.cos(a), (r + 0.07) * math.sin(a), 1 - u))
        G += T.tapered(espinhos, 0.04) * 1.1
    return G * env, H * env


def grampo_de_cabelo(T, t, rng):
    """O Grampo: os pregos espalhados pelo rival piscam (o aviso), e explodem em sequência, cada um com
    o clarão em estrela, o anel e os estilhaços; a última explosão é a maior."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    pos = ((-0.3, -0.2), (0.25, -0.25), (-0.15, 0.2), (0.3, 0.15), (0.0, -0.02))
    pisca = 0.5 + 0.5 * math.sin(t * 60) if t < 0.3 else 1.0
    for k, (x, y) in enumerate(pos):
        t0 = 0.3 + 0.08 * k
        antes = 1 - rel(t, t0, t0 + 0.02)
        P = T.polys(_prego(x - 0.06, y - 0.06, math.pi / 4, 0.12, 0.014))
        G += (P * 0.9 + T.gauss(x, y, 0.025) * pisca * 1.2) * antes
        boom = rel(t, t0, t0 + 0.35)
        if 0 < boom < 1:
            grande = 1.5 if k == len(pos) - 1 else 1.0
            G += T.gauss(x, y, 0.12 * grande * (0.4 + boom)) * (1 - boom) * 1.6
            G += T.ring(0.05 + 0.3 * grande * ease_out(boom, 2), 0.025, x, y) * (1 - boom) * 1.2
            H += T.polys([(estrela(x, y, 0.22 * grande * (1 - 0.5 * boom), k * 0.4, 6, 0.25), 1.0)], 0.01) * (1 - boom) * 1.4
    G += _estilhacos(T, t, 91, 30, 0.32, 0.85, 0.022, gravidade=0.35) * 1.1
    return G * env, H * env


# =================================================================== Sukuna
def cleave(T, t, rng):
    """O Cleave: quatro colchetes de medida fecham no alvo (o golpe calcula a força pela resistência),
    um traço fino risca a diagonal, e o corte enorme sai num só movimento; as duas bordas do rastro
    se afastam (o alvo partido) e o sangue espirra pela linha."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    fecha = ease_out(rel(t, 0.0, 0.3), 2.2)
    some_med = 1 - rel(t, 0.38, 0.48)
    r = 0.75 - 0.35 * fecha
    segs = []
    for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        cx, cy = sx * r, sy * r
        segs += [(cx, cy, cx - sx * 0.14, cy, 1.0), (cx, cy, cx, cy - sy * 0.14, 1.0)]
    G += T.lines(segs, 0.018) * fecha * some_med * 1.1
    a = -0.7
    risca = rel(t, 0.25, 0.38)
    if 0 < risca and t < 0.42:
        G += T.polyline([(-0.9 * math.cos(a), -0.9 * math.sin(a)), (-0.9 * math.cos(a) + 1.8 * math.cos(a) * risca, -0.9 * math.sin(a) + 1.8 * math.sin(a) * risca)], 0.006) * 1.2
    corta = ease_out(rel(t, 0.4, 0.5), 2)
    abre = ease_out(rel(t, 0.5, 0.8), 2)
    if corta > 0:
        x1, y1, x2, y2 = -0.95 * math.cos(a), -0.95 * math.sin(a), 0.95 * math.cos(a), 0.95 * math.sin(a)
        nx, ny = -math.sin(a), math.cos(a)
        for lado in (1, -1):
            off = lado * 0.06 * abre
            L = T.polys([(lamina(x1 + nx * off, y1 + ny * off, x2 + nx * off, y2 + ny * off, 0.08 * (1 - 0.5 * abre), corta, rel(t, 0.55, 0.9)), 1.0)])
            G += L * 1.3 + T.blur(L, 0.02) * 0.7
            H += L * 0.9
        sub = np.random.default_rng(13)
        gotas = []
        for _ in range(22):
            u = sub.uniform(-0.7, 0.7)
            d = abre * sub.uniform(0.05, 0.35) * (1 if sub.uniform() > 0.5 else -1)
            gotas.append((u * math.cos(a) + nx * d, u * math.sin(a) + ny * d + 0.2 * abre * abre, (1 - abre) * sub.uniform(0.4, 1)))
        G += T.splats(gotas, 0.012) * 1.2
    flash = pulso(t, 0.4, 0.6)
    H += T.flare(0, 0, 1.2 * flash + 0.01, a, 0.012) * flash
    return G * env, H * env


def _santuario(T, cx, cy, s, abre):
    """A silhueta do Santuário: o telhado curvo de templo (as pontas para cima), as colunas e as
    bocas abertas com dentes nas laterais."""
    w = 0.7 * s
    telhado = [(cx - w * 1.15, cy - 0.32 * s + 0.08 * s), (cx - w * 0.9, cy - 0.36 * s), (cx - w * 0.4, cy - 0.5 * s),
               (cx, cy - 0.58 * s), (cx + w * 0.4, cy - 0.5 * s), (cx + w * 0.9, cy - 0.36 * s), (cx + w * 1.15, cy - 0.32 * s + 0.08 * s),
               (cx + w, cy - 0.3 * s), (cx - w, cy - 0.3 * s)]
    shapes = [(telhado, 1.0)]
    for k in (-0.75, -0.25, 0.25, 0.75):
        x = cx + w * k
        shapes.append(([(x - 0.025 * s, cy - 0.3 * s), (x + 0.025 * s, cy - 0.3 * s), (x + 0.025 * s, cy + 0.25 * s), (x - 0.025 * s, cy + 0.25 * s)], 0.8))
    F = T.polys(shapes) * abre
    bocas = T.zero()
    for lado in (-1, 1):
        bx, by = cx + lado * w * 0.5, cy - 0.05 * s
        ab = 0.07 * s * abre
        dentes = [(bx - 0.12 * s, by), (bx - 0.08 * s, by - ab), (bx - 0.04 * s, by), (bx, by - ab), (bx + 0.04 * s, by), (bx + 0.08 * s, by - ab), (bx + 0.12 * s, by),
                  (bx + 0.08 * s, by + ab), (bx + 0.04 * s, by), (bx, by + ab), (bx - 0.04 * s, by), (bx - 0.08 * s, by + ab)]
        bocas += T.polys([(dentes, 1.0)])
    return F, bocas


def santuario_preparo(T, t, rng):
    """O Preparo do Santuário: as mãos no selo (as linhas se cruzando no centro) e o santuário se
    formando por cima, pulsando, com as bocas abrindo e fechando (laço)."""
    G, H = vazio(T)
    bate = 0.5 + 0.5 * math.sin(TAU * t)
    F, bocas = _santuario(T, 0, 0.1, 0.9, 0.6 + 0.4 * bate)
    G += (np.clip(F, 0, 1) * 0.35 + T.blur(F, 0.03) * 0.4 + bocas * 0.8) * (0.7 + 0.3 * bate)
    H += np.clip(F - T.blur(F, 0.008), 0, 1) * 0.5
    selo = T.lines([(-0.12, 0.45, 0.12, 0.3, 1.0), (0.12, 0.45, -0.12, 0.3, 1.0), (0, 0.48, 0, 0.27, 1.0)], 0.02)
    G += selo * 1.2 + T.gauss(0, 0.38, 0.08) * (0.6 + 0.4 * bate)
    H += selo * 0.5
    return G, H


def santuario_maligno(T, t, rng):
    """O Santuário Maligno: o santuário sobe ao fundo, e os cortes enchem a área toda de uma vez —
    dezenas, de todos os ângulos, em ondas, sem parar; no fim o clarão e o santuário somem."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    sobe = ease_out(rel(t, 0.0, 0.25), 2)
    F, bocas = _santuario(T, 0, -0.1 + 0.15 * (1 - sobe), 1.0, sobe)
    G += (np.clip(F, 0, 1) * 0.3 + bocas * 0.7) * sobe * (1 - rel(t, 0.7, 0.95))
    sub = np.random.default_rng(31)
    for k in range(46):
        t0 = 0.18 + sub.uniform(0, 0.55)
        u = rel(t, t0, t0 + 0.12)
        if u <= 0 or rel(t, t0, t0 + 0.3) >= 1:
            continue
        a = sub.uniform(0, math.pi)
        cx, cy = sub.uniform(-0.7, 0.7), sub.uniform(-0.6, 0.65)
        comp = sub.uniform(0.25, 0.6)
        x1, y1 = cx - comp * math.cos(a), cy - comp * math.sin(a)
        x2, y2 = cx + comp * math.cos(a), cy + comp * math.sin(a)
        L = T.polys([(lamina(x1, y1, x2, y2, 0.025, ease_out(u, 2), rel(t, t0 + 0.08, t0 + 0.3)), 1.0)])
        G += L * 1.3
        H += L * 0.6
    G += T.gauss(0, 0.1, 0.6, 0.55) * pulso(t, 0.2, 0.9) * 0.25
    H += T.gauss(0, 0.1, 0.25) * pulso(t, 0.7, 0.95) * 1.2
    return G * env, H * env


# =================================================================== Ichigo
def _mascara(T, s, forma):
    """A máscara Hollow: o rosto em gota (mais largo em cima), os dois olhos escuros e as listras
    vermelhas do lado esquerdo."""
    pts = []
    for a in np.linspace(0, TAU, 40, endpoint=False):
        x = 0.3 * s * math.cos(a)
        y = 0.38 * s * math.sin(a) * (1.0 if math.sin(a) < 0 else 1.15)
        pts.append((x * (1 - 0.25 * max(0, math.sin(a))), y - 0.05 * s))
    rosto = T.polys([(pts, 1.0)]) * forma
    olhos = T.polys([([(-0.17 * s, -0.1 * s), (-0.04 * s, -0.08 * s), (-0.05 * s, -0.02 * s), (-0.16 * s, -0.04 * s)], 1.0),
                     ([(0.17 * s, -0.1 * s), (0.04 * s, -0.08 * s), (0.05 * s, -0.02 * s), (0.16 * s, -0.04 * s)], 1.0)]) * forma
    listras = T.zero()
    for k in range(3):
        y = -0.32 * s + 0.11 * k * s
        listras += T.lines([(-0.08 * s, y, -0.27 * s, y + 0.18 * s, 1.0)], 0.03 * s)
    dentes = T.lines([(x * s, 0.18 * s, x * s, 0.26 * s, 1.0) for x in np.linspace(-0.14, 0.14, 7)], 0.012) * forma
    return rosto, olhos, listras * forma, dentes


def mascara_hollow(T, t, rng):
    """A Máscara Hollow: a pressão escura sobe em labaredas em volta, a máscara branca se forma de
    cima para baixo (o rosto, os olhos pretos, os dentes) com as listras vermelhas, e a pressão
    espiritual estoura num anel duplo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    forma = ease_out(rel(t, 0.1, 0.45), 2)
    rosto, olhos, listras, dentes = _mascara(T, 1.0, forma)
    revela = np.clip((T.V + 0.45 - 0.9 * forma) * -12 + 1, 0, 1)
    G += T.blur(rosto, 0.03) * 0.5 + listras * 1.2 * revela
    H += (rosto * revela * 0.9 + dentes * 0.4) * (1 - 0.3 * rel(t, 0.6, 0.9))
    H -= olhos * 1.2
    G -= olhos * 0.4
    sub = np.random.default_rng(44)
    chamas = T.zero()
    for k in range(14):
        a = TAU * k / 14 + sub.uniform(-0.2, 0.2)
        fase = (t * 2 + sub.uniform()) % 1
        r0 = 0.42 + 0.1 * fase
        chamas += T.tapered([(r0 * math.cos(a), r0 * math.sin(a), (r0 + 0.25) * math.cos(a), (r0 + 0.25) * math.sin(a) - 0.1 * fase, 1 - fase)], 0.08)
    G += T.blur(chamas, 0.02) * pulso(t, 0.0, 0.95) * 1.1
    estoura = rel(t, 0.45, 0.85)
    for k, atraso in enumerate((0.0, 0.08)):
        u = rel(t, 0.45 + atraso, 0.85 + atraso)
        G += T.ring(0.35 + 0.6 * ease_out(u, 2), 0.04 - 0.015 * k) * (1 - u) * 1.3 * (u > 0)
    H += T.gauss(0, 0, 0.5) * pulso(t, 0.42, 0.6) * 0.3 * (estoura > 0)
    return G * env, H * env


def bankai_preparo(T, t, rng):
    """O Preparo do Bankai: a pressão espiritual sobe girando em espiral em volta do corpo, as
    faixas escuras e as bordas vermelhas, e o brilho no centro (laço)."""
    G, H = vazio(T)
    for k in range(4):
        pts = []
        for u in np.linspace(0, 1, 40):
            a = TAU * (u * 1.5 + t + k / 4)
            r = 0.55 * (1 - 0.6 * u)
            pts.append((r * math.cos(a), 0.55 - 1.1 * u + 0.12 * math.sin(a)))
        F = T.polyline(pts, 0.045)
        G += T.blur(F, 0.02) * 0.9 + F * 0.4
    G += T.gauss(0, 0.1, 0.18, 0.4) * (0.7 + 0.3 * math.sin(TAU * t * 2))
    H += T.gauss(0, 0.1, 0.06, 0.25) * 0.8
    G -= T.gauss(0, 0.1, 0.08, 0.3) * 0.4
    return G, H


def bankai_ichigo(T, t, rng):
    """O Getsuga Tenshou do Bankai: a meia-lua enorme preta com a borda vermelha avança de baixo
    para cima em diagonal, corta o alvo (o clarão) e o rastro preto fica no ar, desfiando."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    vem = ease_out(rel(t, 0.05, 0.42), 2)
    cx, cy = -0.6 + 0.6 * vem, 0.45 - 0.45 * vem
    lua = T.arc_band(0.62, 0.22, -2.4, 0.5, rot=0.15, cx=cx - 0.25, cy=cy + 0.1, crescente=True) * (1 - rel(t, 0.55, 0.85))
    cheio = np.clip(lua * 3, 0, 1)
    borda = np.clip(cheio - np.clip(T.blur(cheio, 0.014) * 1.6 - 0.6, 0, 1), 0, 1)
    G += borda * 2.4 + T.blur(cheio, 0.06) * 0.5 + cheio * 0.35
    H += borda * 0.35
    corta = pulso(t, 0.38, 0.6)
    H += T.flare(0, 0, 1.1 * corta + 0.01, -0.6, 0.015) * corta
    G += T.gauss(0, 0, 0.15) * corta * 1.4
    rastro = T.zero()
    sub = np.random.default_rng(55)
    fica = rel(t, 0.45, 1.0)
    for k in range(18):
        a = sub.uniform(-2.2, 0.3)
        r = 0.62 + sub.uniform(-0.12, 0.12)
        x, y = r * math.cos(a) - 0.25, r * math.sin(a) + 0.1
        rastro += T.tapered([(x, y, x + 0.08, y - 0.15 * fica - 0.05, 1.0)], 0.03)
    G += rastro * (1 - fica) * 0.8 * (t > 0.45)
    return G * env, H * env


REGISTRO = [
    ("vontade_indomavel", vontade_indomavel, GRANDE, "Yuji · o anel do Preparo trinca e estoura com o soco", False),
    ("nue", nue, GRANDE, "Megumi · as asas do Nue e os raios em três pontos", False),
    ("jardim_das_sombras", jardim_das_sombras, GRANDE, "Megumi · a poça de sombra e as mãos que fecham", False),
    ("pregos_amaldicoados", pregos_amaldicoados, GRANDE, "Nobara · três pregos cravam e a energia prende", False),
    ("ressonancia_amaldicoada", ressonancia_amaldicoada, GRANDE, "Nobara · o boneco de palha e os anéis de ressonância", False),
    ("grampo_de_cabelo", grampo_de_cabelo, GRANDE, "Nobara · os pregos explodem em sequência", False),
    ("cleave", cleave, GRANDE, "Sukuna · a medida e o corte único que parte o alvo", False),
    ("santuario_preparo", santuario_preparo, MEDIA, "Sukuna · o selo e o santuário se formando (Preparo, laço)", True),
    ("santuario_maligno", santuario_maligno, GRANDE, "Sukuna · o santuário e os cortes em toda a área", False),
    ("mascara_hollow", mascara_hollow, GRANDE, "Ichigo · a máscara Hollow e a pressão espiritual", False),
    ("bankai_preparo", bankai_preparo, MEDIA, "Ichigo · a pressão do Bankai em espiral (Preparo, laço)", True),
    ("bankai_ichigo", bankai_ichigo, GRANDE, "Ichigo · o Getsuga preto de borda vermelha", False),
]
