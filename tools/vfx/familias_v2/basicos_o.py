"""Ataques básicos com animação própria, lote o (personagens novos).

Hércules, Anúbis, Rá, Set, Ísis, Hórus, Sekhmet, Odin, Fenrir, Hel, Jason, Freddy, Michael Myers, Chucky e
Pennywise: o soco divino com as folhas de louro, o cetro e a balança do julgamento, o Olho de Rá no disco que
queima, o redemoinho de areia de Set, a asa de penas de Ísis, as garras do falcão, a patada em chamas da
leoa, a Gungnir com as runas, a mordida de Fenrir rompendo a corrente, a mão de osso de Hel e o frio, o
machado do Jason, a luva de lâminas do Freddy, a faca erguida do Myers, as facadinhas frenéticas do Chucky e
a boca de dentes do Pennywise com as luzes mortas e o balão.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .basicos_a import _PUNHO, _move, _punho
from .basicos_k import _borda, _contorno, _estouro, _folha, _gira, _gotas
from .basicos_l import _estrelinhas


def _olho_de_horus(cx, cy, s):
    """O olho egípcio: a amêndoa, a pupila, a sobrancelha e os traços de baixo (a lágrima e a espiral)."""
    amendoa = [(cx + 0.2 * s * math.cos(a), cy + 0.08 * s * math.sin(a)) for a in np.linspace(0, TAU, 20, endpoint=False)]
    segs = _contorno(amendoa)
    segs.append((cx - 0.2 * s, cy - 0.16 * s, cx + 0.22 * s, cy - 0.14 * s, 1.0))
    segs.append((cx - 0.02 * s, cy + 0.08 * s, cx - 0.05 * s, cy + 0.26 * s, 1.0))
    espiral = [(cx + 0.05 * s + 0.07 * s * u * math.cos(5 * u), cy + 0.08 * s + 0.18 * s * u + 0.03 * s * math.sin(5 * u)) for u in np.linspace(0, 1, 10)]
    for k in range(len(espiral) - 1):
        segs.append((espiral[k][0], espiral[k][1], espiral[k + 1][0], espiral[k + 1][1], 1.0))
    return segs, (cx, cy)


# ================================================================== Hércules
def soco_de_hercules(T, t, rng):
    """O soco de Hércules: o punho com o brilho dourado da força divina vem pesado, o impacto solta duas ondas de
    choque e as folhas de louro voam."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vai = ease_in(rel(t, 0.0, 0.28), 2)
    if t < 0.45:
        x = -0.85 + 0.75 * vai
        P, nos = _punho(T, x, 0.0, 2.2)
        G += P * 0.6 + _borda(T, P, 0.008) * 1.3 + T.gauss(x, 0, 0.2) * 0.4
        H += nos * 0.5
    for k in range(2):
        u = rel(t, 0.28 + 0.08 * k, 0.75 + 0.08 * k)
        if 0 < u < 1:
            G += T.ring(0.1 + 0.7 * ease_out(u, 2), 0.04, 0.05, 0) * (1 - u) * 1.3
    H += T.gauss(0.05, 0, 0.12) * pulso(t, 0.27, 0.45) * 2.0
    folhas = rel(t, 0.3, 0.95)
    if 0 < folhas < 1:
        q = np.random.default_rng(3)
        shapes = []
        for _ in range(10):
            a = q.uniform(0, TAU)
            d = 0.6 * ease_out(folhas, 2) * q.uniform(0.4, 1)
            shapes.append((_folha(d * math.cos(a), d * math.sin(a) + 0.2 * folhas ** 2, 0.045, a + folhas * 4), 1 - folhas))
        G += T.polys(shapes) * 1.1
    return G * env, H * env


# ================================================================== Anúbis
def cetro_de_anubis(T, t, rng):
    """O golpe de Anúbis: o cetro (o cabo comprido com a cabeça de chacal em cima) varre e bate, e a balança do
    julgamento aparece em cima do rival, pendendo para o lado do castigo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    gira = ease_out(rel(t, 0.0, 0.28), 2.2)
    if t < 0.5:
        ang = -2.3 + 2.0 * gira
        px, py = -0.6, 0.4
        tip = (px + 0.85 * math.cos(ang), py + 0.85 * math.sin(ang))
        G += T.lines([(px, py, tip[0], tip[1], 1.0)], 0.022) * 1.1 * (1 - rel(t, 0.38, 0.5))
        cab = _gira([(0, 0), (0.08, -0.03), (0.13, 0.0), (0.06, 0.03)], ang, tip[0], tip[1])
        G += T.polys([(cab, 1.0)]) * 1.2 * (1 - rel(t, 0.38, 0.5))
        G += T.arc_band(0.85, 0.03, -2.3, ang, cx=px, cy=py, taper=0.7) * 0.5
    g, h = _estouro(T, t, 0.26, 0.55, 0.05, 0.05, 0.3, 8, 5)
    G += g
    H += h
    balanca = pulso(t, 0.35, 1.0)
    if balanca > 0:
        inc = 0.25 * ease_out(rel(t, 0.4, 0.7), 2)
        cx, cy = 0.0, -0.5
        segs = [(cx, cy - 0.12, cx, cy + 0.02, 1.0),
                (cx - 0.25 * math.cos(inc), cy - 0.25 * math.sin(inc), cx + 0.25 * math.cos(inc), cy + 0.25 * math.sin(inc), 1.0)]
        for lado in (-1, 1):
            ex, ey = cx + lado * 0.25 * math.cos(inc), cy + lado * 0.25 * math.sin(inc)
            segs += [(ex, ey, ex - 0.06, ey + 0.1, 0.7), (ex, ey, ex + 0.06, ey + 0.1, 0.7), (ex - 0.07, ey + 0.1, ex + 0.07, ey + 0.1, 1.0)]
        G += T.lines(segs, 0.012) * balanca * 1.2
    return G * env, H * env


# ================================================================== Rá
def disco_solar(T, t, rng):
    """O raio de sol de Rá: o disco solar com o Olho de Rá desenhado nele acende no alto, e o olho dispara o raio que
    queima o rival (as chamas sobem nele)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    disco = back(rel(t, 0.0, 0.2), 1.3) * (1 - rel(t, 0.6, 0.8))
    cx, cy = -0.55, -0.45
    if disco > 0:
        G += T.ring(0.2 * disco, 0.02, cx, cy) * 1.2 + T.gauss(cx, cy, 0.15 * disco) * 0.4
        segs, _ = _olho_de_horus(cx, cy, 0.7 * disco)
        G += T.lines(segs, 0.01) * 1.2
        H += T.gauss(cx, cy, 0.03) * disco * 1.4
    raio = rel(t, 0.18, 0.55)
    if 0 < raio < 1:
        vai = min(1, raio * 4)
        x1, y1 = cx + (0.05 - cx) * vai, cy + (0.0 - cy) * vai
        R = T.lines([(cx, cy, x1, y1, 1.0)], 0.04)
        G += (T.blur(R, 0.015) * 0.9 + R * 0.6) * (1 - raio * 0.5)
        H += T.lines([(cx, cy, x1, y1, 1.0)], 0.012) * (1 - raio * 0.5)
    queima = rel(t, 0.3, 1.0)
    if 0 < queima < 1:
        q = np.random.default_rng(int(t * 30) % 7)
        chamas = [(lamina(0.05 + (k - 2.5) * 0.08, 0.25, 0.05 + (k - 2.5) * 0.06 + q.uniform(-0.03, 0.03), 0.25 - (0.2 + 0.15 * q.uniform()) * math.sin(math.pi * queima), 0.04), 1.0) for k in range(6)]
        F = T.polys(chamas)
        G += F * 0.8 + T.blur(F, 0.015) * 0.5
    g, h = _estouro(T, t, 0.25, 0.55, 0.05, 0, 0.25, 8, 7, 0.016)
    G += g * 0.8
    H += h * 0.8
    return G * env, H * env


# ================================================================== Set
def cetro_de_set(T, t, rng):
    """O golpe de Set: o cetro varre e levanta um redemoinho de areia que gira em volta do rival, arranhando, e a
    poeira assenta."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    gira = ease_out(rel(t, 0.0, 0.25), 2)
    if t < 0.45:
        ang = -2.5 + 2.2 * gira
        px, py = -0.6, 0.35
        tip = (px + 0.8 * math.cos(ang), py + 0.8 * math.sin(ang))
        G += T.lines([(px, py, tip[0], tip[1], 1.0)], 0.022) * 1.1
        G += T.lines([(tip[0], tip[1], tip[0] + 0.08 * math.cos(ang + 1.0), tip[1] + 0.08 * math.sin(ang + 1.0), 1.0)], 0.02)
    areia = rel(t, 0.15, 0.95)
    if 0 < areia < 1:
        q = np.random.default_rng(9)
        pts = []
        for k in range(90):
            fase = q.uniform(0, TAU)
            alt = q.uniform(-0.5, 0.45)
            r = 0.15 + 0.3 * (alt + 0.5) * (0.5 + 0.5 * ease_out(areia, 2))
            a = fase + areia * 12 * (1 - 0.3 * (alt + 0.5))
            pts.append((r * math.cos(a), alt + 0.04 * r * math.sin(a), math.sin(math.pi * areia) * q.uniform(0.4, 1)))
        G += T.splats(pts, 0.012) * 1.2
    g, h = _estouro(T, t, 0.22, 0.5, 0, 0, 0.25, 7, 11, 0.015)
    G += g * 0.8
    H += h * 0.7
    return G * env, H * env


# ================================================================== Ísis
def asas_de_isis(T, t, rng):
    """A asa de Ísis: a asa de penas compridas se abre e varre o rival de lado, e as penas douradas se soltam e caem
    devagar."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2)
    if t < 0.55:
        some = 1 - rel(t, 0.4, 0.55)
        base = (-0.7, -0.1)
        shapes = []
        for k in range(8):
            a = -0.9 + 1.3 * abre * k / 7 - 0.3
            L = 0.4 + 0.08 * k
            tip = (base[0] + L * math.cos(a), base[1] + L * math.sin(a))
            shapes.append((lamina(base[0], base[1], tip[0], tip[1], 0.05), 1.0))
        A = T.polys(shapes)
        G += (A * 0.5 + _borda(T, A, 0.006) * 1.3) * some
        G += T.arc_band(0.75, 0.04, -1.2, -1.2 + 1.4 * abre, cx=base[0], cy=base[1], taper=0.6) * 0.5 * some
    g, h = _estouro(T, t, 0.28, 0.55, 0.05, 0, 0.28, 8, 13, 0.016)
    G += g * 0.8
    H += h * 0.7
    penas = rel(t, 0.3, 1.0)
    if 0 < penas < 1:
        q = np.random.default_rng(15)
        shapes = []
        for _ in range(8):
            x0 = q.uniform(-0.5, 0.5)
            y = -0.3 + 0.8 * penas + q.uniform(-0.1, 0.1)
            shapes.append((_folha(x0 + 0.08 * math.sin(penas * 8 + x0 * 5), y, 0.05, math.pi / 2 + 0.6 * math.sin(penas * 6 + x0)), 1 - penas))
        G += T.polys(shapes)
    return G * env, H * env


# ================================================================== Hórus
def garra_do_falcao(T, t, rng):
    """As garras de Hórus: o falcão mergulha de cima com as três garras curvas abertas, agarra o rival (as garras
    fecham) e as penas voam."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    desce = ease_in(rel(t, 0.0, 0.28), 2)
    fecha = ease_out(rel(t, 0.26, 0.4), 2)
    if t < 0.6:
        some = 1 - rel(t, 0.45, 0.6)
        cx, cy = 0.35 - 0.35 * desce, -0.9 + 0.75 * desce
        segs = []
        for k, a in enumerate((-0.6, 0.0, 0.6)):
            aa = math.pi / 2 + a * (1 - 0.6 * fecha)
            p1 = (cx + 0.3 * math.cos(aa), cy + 0.3 * math.sin(aa))
            p2 = (p1[0] - 0.12 * math.sin(aa) * (1 if a <= 0 else -1) * 0.5, p1[1] + 0.12)
            segs += [(cx, cy, p1[0], p1[1], 1.0), (p1[0], p1[1], p2[0], p2[1], 1.0)]
        G += T.lines(segs, 0.03) * 1.3 * some
        if desce < 1:
            G += T.tapered([(cx + 0.25, cy - 0.5, cx, cy - 0.05, 0.7)], 0.03)
    g, h = _estouro(T, t, 0.3, 0.6, 0, 0, 0.3, 8, 17)
    G += g
    H += h
    penas = rel(t, 0.32, 0.95)
    if 0 < penas < 1:
        q = np.random.default_rng(19)
        shapes = [(_folha(q.uniform(-0.4, 0.4) * (0.5 + penas), q.uniform(-0.3, 0.1) + 0.3 * penas, 0.045, q.uniform(0, 6) + penas * 4), 1 - penas) for _ in range(7)]
        G += T.polys(shapes)
    return G * env, H * env


# ================================================================== Sekhmet
def garra_da_leoa(T, t, rng):
    """A patada de Sekhmet: a pata da leoa rasga em quatro riscos curvos, cada um pegando fogo, e as brasas sobem."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    for k in range(4):
        t0 = 0.08 + 0.02 * k
        p = ease_out(rel(t, t0, t0 + 0.12), 3)
        ini = rel(t, t0 + 0.2, t0 + 0.55)
        if p > 0 and ini < 1:
            dx = (k - 1.5) * 0.12
            L = T.arc_band(0.6, 0.035, -2.2 + 0.1 * k, -2.2 + 0.1 * k + 1.3 * p, cx=0.25 + dx, cy=0.4, crescente=True)
            G += L * 1.4 * (1 - ini)
            H += L * 0.5 * (1 - ini)
    fogo = pulso(t, 0.15, 0.85)
    if fogo > 0:
        q = np.random.default_rng(int(t * 30) % 8)
        chamas = [(lamina(-0.2 + 0.12 * k, 0.1 + 0.05 * q.uniform(), -0.2 + 0.12 * k + q.uniform(-0.04, 0.04), -0.15 - 0.12 * q.uniform(), 0.035), 1.0) for k in range(5)]
        F = T.polys(chamas)
        G += (F * 0.7 + T.blur(F, 0.015) * 0.5) * fogo
    G += _gotas(T, t, 0.3, 0.6, 0.0, 0.0, 14, 0.5, 21, -2.6, -0.5, 0.012, -0.3) * 1.3
    return G * env, H * env


# ================================================================== Odin
def gungnir(T, t, rng):
    """A Gungnir de Odin: a lança voa reta com as runas acesas ao longo do cabo, crava no rival e o círculo de runas se
    abre em volta do ponto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    voa = ease_in(rel(t, 0.0, 0.25), 1.5)
    if t < 0.55:
        tip = -0.9 + 0.95 * voa
        some = 1 - rel(t, 0.42, 0.55)
        G += T.lines([(tip - 0.8, 0.0, tip - 0.15, 0.0, 1.0)], 0.02) * 1.1 * some
        P = T.polys([(lamina(tip - 0.2, 0.0, tip, 0.0, 0.05), 1.0)])
        G += (P * 1.2 + _borda(T, P, 0.005)) * some
        runas = []
        for k in range(5):
            rx = tip - 0.7 + 0.12 * k
            runas += [(rx, -0.04, rx, 0.04, 1.0), (rx, -0.04, rx + 0.04, 0.0, 1.0)]
        H += T.lines(runas, 0.008) * some
    circulo = rel(t, 0.25, 0.9)
    if 0 < circulo < 1:
        r = 0.15 + 0.25 * ease_out(circulo, 2)
        G += T.ring(r, 0.015, 0.05, 0) * (1 - circulo) * 1.2 + T.ring(r * 0.8, 0.01, 0.05, 0) * (1 - circulo)
        runas = []
        for k in range(10):
            a = TAU * k / 10 + circulo
            x, y = 0.05 + r * 0.9 * math.cos(a), r * 0.9 * math.sin(a)
            runas += [(x, y - 0.025, x, y + 0.025, 1 - circulo), (x, y - 0.025, x + 0.02, y, 1 - circulo)]
        G += T.lines(runas, 0.008) * 1.2
    g, h = _estouro(T, t, 0.25, 0.55, 0.05, 0, 0.25, 8, 23, 0.016)
    G += g * 0.8
    H += h * 0.8
    return G * env, H * env


# ================================================================== Fenrir
def dentada_de_fenrir(T, t, rng):
    """A dentada de Fenrir: as duas fileiras de dentes do lobo gigante se fecham no rival com força, e os elos da
    corrente que o prendia se partem e voam."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    fecha = ease_in(rel(t, 0.0, 0.28), 2.5)
    if t < 0.55:
        abre = 0.45 * (1 - fecha)
        shapes = []
        for k in range(7):
            x = -0.36 + 0.12 * k
            h = 0.14 if k in (1, 5) else 0.08
            shapes.append(([(x - 0.045, -0.05 - abre), (x + 0.045, -0.05 - abre), (x, -0.05 - abre + h)], 1.0))
            shapes.append(([(x - 0.045, 0.05 + abre), (x + 0.045, 0.05 + abre), (x, 0.05 + abre - h)], 1.0))
        D = T.polys(shapes)
        G += (D * 0.7 + _borda(T, D, 0.005) * 1.2) * (1 - rel(t, 0.42, 0.55))
        G += (T.arc_band(0.45, 0.025, 3.6, 5.8, squash=0.45, cx=0, cy=-0.02 - abre) + T.arc_band(0.45, 0.025, 0.5, 2.6, squash=0.45, cx=0, cy=0.02 + abre)) * 0.8 * (1 - rel(t, 0.42, 0.55))
    g, h = _estouro(T, t, 0.27, 0.55, 0, 0, 0.3, 9, 25)
    G += g
    H += h
    elos = rel(t, 0.3, 0.9)
    if 0 < elos < 1:
        q = np.random.default_rng(27)
        segs = []
        for _ in range(6):
            a = q.uniform(0, TAU)
            d = 0.2 + 0.5 * ease_out(elos, 2)
            cx, cy = d * math.cos(a), d * math.sin(a) + 0.3 * elos ** 2
            elo = [(cx + 0.05 * math.cos(b), cy + 0.03 * math.sin(b)) for b in np.linspace(0, TAU, 10, endpoint=False)]
            segs += _contorno(_gira([(x - cx, y - cy) for x, y in elo], elos * 6 + a, cx, cy), 1 - elos)
        G += T.lines(segs, 0.01) * 1.3
    return G * env, H * env


# ================================================================== Hel
def toque_de_hel(T, t, rng):
    """O toque gelado de Hel: a mão meio de osso (os dedos finos e as juntas) estende e toca o rival, e o frio da morte se
    espalha nele em cristais e névoa escura."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    estende = ease_out(rel(t, 0.0, 0.3), 2)
    if t < 0.6:
        some = 1 - rel(t, 0.45, 0.6)
        px = -0.85 + 0.5 * estende
        segs = [(px - 0.5, 0.08, px, 0.0, 1.0), (px - 0.5, -0.04, px, -0.04, 0.8)]
        juntas = [(px, 0.0, 1.0)]
        for k in range(4):
            a = -0.45 + 0.3 * k
            j1 = (px + 0.24 * math.cos(a), 0.24 * math.sin(a))
            j2 = (j1[0] + 0.18 * math.cos(a * 0.5), j1[1] + 0.18 * math.sin(a * 0.5))
            segs += [(px, 0.0, j1[0], j1[1], 1.0), (j1[0], j1[1], j2[0], j2[1], 1.0)]
            juntas += [(j1[0], j1[1], 1.0), (j2[0], j2[1], 0.8)]
        G += T.lines(segs, 0.022) * 1.2 * some
        H += T.splats(juntas, 0.016) * some
    gelo = rel(t, 0.28, 1.0)
    if 0 < gelo < 1:
        shapes = []
        for k in range(7):
            a = TAU * k / 7 + 0.3
            r = 0.15 + 0.15 * (k % 2)
            g = ease_out(min(1, gelo * 2), 2)
            cx, cy = 0.05 + r * g * math.cos(a), r * g * math.sin(a)
            shapes.append((_gira([(0, -0.07 * g), (0.025 * g, 0), (0, 0.07 * g), (-0.025 * g, 0)], a + math.pi / 2, cx, cy), 1.0))
        C = T.polys(shapes)
        G += (_borda(T, C, 0.005) * 1.3 + C * 0.3) * (1 - rel(t, 0.8, 1.0))
        G += T.gauss(0.05, 0, 0.35, 0.25) * math.sin(math.pi * gelo) * 0.35
    return G * env, H * env


# ================================================================== Jason
def machadada(T, t, rng):
    """A machadada do Jason: o machado sobe devagar (a cabeça larga com o fio) e desce de uma vez, cravando no rival
    com o baque surdo; o brilho fica no fio."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    sobe = ease_out(rel(t, 0.0, 0.25), 2)
    desce = ease_in(rel(t, 0.25, 0.38), 3)
    if t < 0.55:
        ang = -math.pi / 2 - 0.8 * sobe + 1.7 * desce
        px, py = -0.4, 0.5
        cx, cy = px + 0.7 * math.cos(ang), py + 0.7 * math.sin(ang)
        G += T.lines([(px, py, cx, cy, 1.0)], 0.028) * 1.1 * (1 - rel(t, 0.45, 0.55))
        cab = _gira([(0.0, -0.06), (0.16, -0.14), (0.2, 0.0), (0.16, 0.14), (0.0, 0.06)], ang + math.pi / 2, cx, cy)
        C = T.polys([(cab, 1.0)])
        G += (C * 0.7 + _borda(T, C, 0.007) * 1.3) * (1 - rel(t, 0.45, 0.55))
    g, h = _estouro(T, t, 0.37, 0.7, 0.05, 0.0, 0.35, 10, 29)
    G += g
    H += h
    G += _gotas(T, t, 0.4, 0.5, 0.05, 0.0, 12, 0.45, 31, -2.8, -0.3, 0.016, 0.4)
    return G * env, H * env


# ================================================================== Freddy
def garra_de_freddy(T, t, rng):
    """A luva do Freddy: as quatro lâminas compridas dos dedos raspam o rival em quatro riscos finos e paralelos, com
    as faíscas do metal e a imagem tremendo de pesadelo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    p = ease_out(rel(t, 0.1, 0.3), 2.5)
    ini = rel(t, 0.35, 0.7)
    if p > 0 and ini < 1:
        treme = 0.02 * math.sin(t * 70)
        L = T.zero()
        for k in range(4):
            dy = (k - 1.5) * 0.1
            L += T.polys([(lamina(-0.6, -0.4 + dy + treme, 0.6, 0.25 + dy, 0.022, prog=p, inicio=ini), 1.0)])
        G += L * 1.4
        H += L * 0.6
    faisca = rel(t, 0.15, 0.6)
    if 0 < faisca < 1:
        q = np.random.default_rng(int(t * 40) % 6)
        segs = []
        for _ in range(10):
            x0 = q.uniform(-0.4, 0.4)
            a = q.uniform(-2.8, -0.3)
            segs.append((x0, -0.1 + 0.5 * x0, x0 + 0.15 * math.cos(a), -0.1 + 0.5 * x0 + 0.15 * math.sin(a), 1.0))
        G += T.tapered(segs, 0.01) * (1 - faisca) * 1.2
    sonho = pulso(t, 0.3, 0.95)
    if sonho > 0:
        A = T.ring(0.4, 0.015, 0, 0)
        du = 0.04 * np.sin(T.V * 25 + t * 30) * sonho
        G += T.warp(A, du, du * 0) * sonho * 0.8
    return G * env, H * env


# ================================================================== Michael Myers
def facada_de_myers(T, t, rng):
    """A facada do Michael Myers: a faca de cozinha erguida (a lâmina larga e o cabo) brilha no alto, desce devagar e
    certeira, e crava no rival; o brilho frio fica na lâmina."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    desce = ease_in(rel(t, 0.15, 0.42), 2.2)
    if t < 0.62:
        some = 1 - rel(t, 0.5, 0.62)
        tip_y = -0.45 + 0.5 * desce
        tip = (0.05, tip_y)
        base = (0.05, tip_y - 0.5)
        L = T.polys([([(base[0] - 0.08, base[1]), (base[0] + 0.04, base[1]), (tip[0] + 0.01, tip[1]), (base[0] - 0.08, base[1] + 0.4)], 1.0)])
        G += (L * 0.8 + _borda(T, L, 0.005) * 1.2) * some
        G += T.lines([(base[0] - 0.02, base[1] - 0.25, base[0] - 0.02, base[1], 1.0)], 0.05) * 0.9 * some
        brilho = pulso(t, 0.05, 0.3)
        H += T.flare(base[0] + 0.02, base[1] + 0.15, 0.25 * brilho + 0.01, 0.785, 0.008) * brilho * 1.3
    g, h = _estouro(T, t, 0.4, 0.75, 0.05, 0.0, 0.3, 8, 33)
    G += g
    H += h
    G += _gotas(T, t, 0.42, 0.5, 0.05, 0.0, 10, 0.4, 35, -2.8, -0.3, 0.015, 0.4)
    return G * env, H * env


# ================================================================== Chucky
def facadinha_do_chucky(T, t, rng):
    """As facadinhas do Chucky: a faquinha pequena entra de baixo, frenética, quatro vezes seguidas em lugares
    diferentes (tremendo), cada uma com o estalinho, e as gotas pulam."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    for k in range(4):
        t0 = 0.05 + 0.12 * k
        u = rel(t, t0, t0 + 0.1)
        if 0 < u < 1:
            x = -0.15 + 0.1 * math.sin(k * 2.3)
            y0 = 0.6
            tip_y = 0.6 - 0.55 * math.sin(math.pi * u)
            L = T.polys([(lamina(x - 0.08, y0 + 0.1, x + 0.03 * math.sin(t * 90), tip_y - 0.1, 0.04), 1.0)])
            G += L * 1.3
        b = rel(t, t0 + 0.05, t0 + 0.18)
        if 0 < b < 1:
            bx, by = -0.15 + 0.1 * math.sin(k * 2.3), 0.05
            H += T.flare(bx, by, 0.15 * (1 - b) + 0.01, k, 0.008) * (1 - b) * 1.3
            G += T.ring(0.02 + 0.08 * b, 0.01, bx, by) * (1 - b)
    G += _gotas(T, t, 0.2, 0.6, -0.1, 0.05, 14, 0.4, 37, -2.8, -0.3, 0.013, 0.4)
    return G * env, H * env


# ================================================================== Pennywise
def mordida_de_pennywise(T, t, rng):
    """A mordida do Pennywise: a boca se abre enorme em volta do rival com as fileiras de dentes em círculo (uma dentro da
    outra), as luzes mortas brilham lá no fundo, a boca fecha, e o balão vermelho sobe."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    abre = back(rel(t, 0.0, 0.25), 1.3)
    fecha = ease_in(rel(t, 0.35, 0.5), 2.5)
    r_ext = 0.55 * abre * (1 - 0.8 * fecha)
    if r_ext > 0.03 and t < 0.6:
        shapes = []
        for camada, (rr, n) in enumerate(((1.0, 14), (0.72, 11), (0.48, 8))):
            r = r_ext * rr
            for k in range(n):
                a = TAU * k / n + camada * 0.2
                base1 = (r * math.cos(a - 0.12), r * math.sin(a - 0.12) * 0.85)
                base2 = (r * math.cos(a + 0.12), r * math.sin(a + 0.12) * 0.85)
                ponta = (r * 0.75 * math.cos(a), r * 0.75 * math.sin(a) * 0.85)
                shapes.append(([base1, base2, ponta], 1.0))
        D = T.polys(shapes)
        G += D * 0.6 + _borda(T, D, 0.005) * 1.2
        G += T.ring(r_ext * 1.05, 0.02, 0, 0, squash=1 / 0.85) * 0.8
    luzes = pulso(t, 0.1, 0.45)
    if luzes > 0:
        pts = [(0.05 * math.cos(TAU * k / 3 + t * 6), 0.05 * math.sin(TAU * k / 3 + t * 6), 1.0) for k in range(3)]
        H += T.splats(pts, 0.025) * luzes * 1.8
        G += T.gauss(0, 0, 0.12) * luzes * 0.6
    g, h = _estouro(T, t, 0.45, 0.7, 0, 0, 0.3, 9, 39)
    G += g
    H += h
    balao = rel(t, 0.5, 1.0)
    if 0 < balao < 1:
        bx, by = 0.45 + 0.05 * math.sin(balao * 6), 0.3 - 0.9 * balao
        G += T.ring(0.08, 0.012, bx, by, squash=0.85) * 1.2 + T.gauss(bx, by, 0.06) * 0.4
        G += T.polyline([(bx, by + 0.1), (bx + 0.02 * math.sin(t * 12), by + 0.2), (bx, by + 0.32)], 0.006) * 0.9
        H += T.gauss(bx - 0.025, by - 0.03, 0.012) * 0.8
    return G * env, H * env


REGISTRO = [
    ("soco_de_hercules", soco_de_hercules, GRANDE, "Básico de Hércules: o soco divino e o louro", False),
    ("cetro_de_anubis", cetro_de_anubis, GRANDE, "Básico de Anúbis: o cetro e a balança", False),
    ("disco_solar", disco_solar, GRANDE, "Básico de Rá: o Olho no disco e o raio que queima", False),
    ("cetro_de_set", cetro_de_set, GRANDE, "Básico de Set: o cetro e o redemoinho de areia", False),
    ("asas_de_isis", asas_de_isis, GRANDE, "Básico de Ísis: a asa e as penas douradas", False),
    ("garra_do_falcao", garra_do_falcao, GRANDE, "Básico de Hórus: as garras do falcão", False),
    ("garra_da_leoa", garra_da_leoa, GRANDE, "Básico de Sekhmet: a patada em chamas", False),
    ("gungnir", gungnir, GRANDE, "Básico de Odin: a Gungnir e as runas", False),
    ("dentada_de_fenrir", dentada_de_fenrir, GRANDE, "Básico de Fenrir: a dentada e a corrente partida", False),
    ("toque_de_hel", toque_de_hel, GRANDE, "Básico de Hel: a mão de osso e o gelo", False),
    ("machadada", machadada, GRANDE, "Básico do Jason: o machado descendo", False),
    ("garra_de_freddy", garra_de_freddy, GRANDE, "Básico do Freddy: as quatro lâminas", False),
    ("facada_de_myers", facada_de_myers, GRANDE, "Básico do Myers: a faca erguida", False),
    ("facadinha_do_chucky", facadinha_do_chucky, GRANDE, "Básico do Chucky: as facadinhas frenéticas", False),
    ("mordida_de_pennywise", mordida_de_pennywise, GRANDE, "Básico do Pennywise: a boca de dentes e o balão", False),
]
