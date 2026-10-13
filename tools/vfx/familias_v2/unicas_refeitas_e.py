"""Mecânicas únicas refeitas, lote e: o impacto conta o nome da mecânica.

- mu_tranquilizante (Solid Snake): o dardo entrando e os "Z" do sono subindo;
- mu_contra_golpe (Mestre Splinter): o bastão varrendo e a seta do contra-golpe voltando;
- mu_nao_fui (Bart): a seta da culpa apontando para o lado e as exclamações;
- mu_galo (Peter Griffin): a nuvem de briga de desenho, com estrelas e pernas;
- mu_chantagem (Cartman): o envelope da chantagem e o cadeado fechando;
- mu_formula (Plankton): o frasco sugando as gotas de Carga;
- mu_robo_quebrou (Macaco Louco): a cúpula do robô rachando em pedaços;
- mu_penny (Bugiganga): o livro-computador da Penny com a mira travando;
- mu_kikoho (Tenshinhan): o triângulo das mãos e o Kikoho esmagando para baixo;
- mu_parry (Ken Masters): o lampejo azul do parry e a chama subindo do troco;
- mu_penhasco (Heihachi): a beira do penhasco quebrando e a queda;
- mu_estica_jake (Jake): o corpo esticando num arco por cima do trio;
- mu_sempre_junto (Robin): os dois pássaros-rangues chegando juntos;
- mu_coragem_luigi (Luigi): a chama verde da coragem e o boné com o L.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, pulso, rel, vazio
from .unicas_refeitas_d import _contorno, _gira, _maior, _oval


def _z(x, y, s):
    return [(x - s, y - s), (x + s, y - s), (x - s, y + s), (x + s, y + s)]


def tranquilizante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    entra = ease_in(rel(t, 0.0, 0.25), 2)
    x = -0.55 + 0.5 * entra
    G += T.lines([(x - 0.18, -0.02, x, 0.0, 1)], 0.012) * (1 - rel(t, 0.3, 0.4)) * 1.2
    G += T.polys([([(x - 0.2, -0.05), (x - 0.15, 0.0), (x - 0.2, 0.05)], 1.0)]) * (1 - rel(t, 0.3, 0.4))
    H += T.gauss(x, 0, 0.02) * (1 - rel(t, 0.3, 0.4)) * 1.5
    G += T.ring(0.06 + 0.2 * rel(t, 0.22, 0.4), 0.02) * pulso(t, 0.22, 0.42) * 1.2
    dorme = rel(t, 0.35, 0.95)
    for k in range(3):
        f = (dorme * 1.4 - k * 0.22)
        if f <= 0 or f > 1:
            continue
        s = 0.04 + 0.03 * k
        zx, zy = 0.08 + 0.12 * k + 0.05 * math.sin(f * 6), -0.05 - 0.45 * f
        G += T.polyline(_z(zx, zy, s), 0.014) * (1 - f) * 1.3
    return G * env, H * env


def contra_golpe(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    varre = ease_out(rel(t, 0.0, 0.35), 2)
    if varre > 0:
        G += T.arc_band(0.36, 0.035, -2.6, -2.6 + 2.6 * varre, crescente=True) * (1 - rel(t, 0.35, 0.5)) * 1.3
        a = -2.6 + 2.6 * varre
        G += T.lines([(0, 0, 0.42 * math.cos(a), 0.42 * math.sin(a), 1)], 0.025) * (1 - rel(t, 0.35, 0.5))
    choque = pulso(t, 0.3, 0.55)
    G += T.polys([(estrela(0.0, 0.0, 0.22 * choque + 0.01, 0.3, 6), 1.0)]) * choque * 1.3
    H += T.gauss(0, 0, 0.08) * choque * 1.6
    volta = rel(t, 0.45, 0.9)
    if volta > 0:
        pts = [(0.4 * math.cos(math.pi * u), -0.1 - 0.25 * math.sin(math.pi * u)) for u in np.linspace(0, ease_out(volta, 2), 16)]
        G += T.polyline(pts, 0.03) * (1 - rel(t, 0.8, 0.95)) * 1.1
        hx, hy = pts[-1]
        G += T.polys([([(hx - 0.06, hy - 0.06), (hx + 0.06, hy - 0.02), (hx - 0.02, hy + 0.07)], 1.0)]) * (1 - rel(t, 0.8, 0.95)) * 1.2
    return G * env, H * env


def nao_fui(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    gira = ease_out(rel(t, 0.05, 0.5), 3)
    a = -math.pi / 2 + (math.pi / 2 + 0.2) * gira
    ponta = (0.38 * math.cos(a), 0.38 * math.sin(a))
    G += T.lines([(0, 0, *ponta, 1)], 0.04) * 1.1
    seta = _gira([(0.0, -0.08), (0.12, 0.0), (0.0, 0.08)], a, *ponta)
    G += T.polys([(seta, 1.0)], 0.003) * 1.3
    H += T.gauss(*ponta, 0.05) * gira * 1.2
    for k, (x, y) in enumerate(((-0.25, -0.25), (-0.35, -0.05), (-0.22, 0.18))):
        f = pulso(t, 0.25 + 0.1 * k, 0.8)
        G += T.lines([(x, y - 0.08, x, y + 0.02, 1)], 0.025) * f * 1.2
        G += T.gauss(x, y + 0.07, 0.018) * f * 1.6
    return G * env, H * env


def galo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    briga = rel(t, 0.0, 0.9)
    q = np.random.default_rng(int(t * 30) % 7 + 1)
    for k in range(9):
        a = TAU * k / 9 + t * 3
        r = 0.24 + 0.04 * math.sin(k * 2 + t * 20)
        G += T.gauss(r * math.cos(a), r * math.sin(a) * 0.8, 0.09) * 0.55 * pulso(t, 0.0, 0.85)
    G += T.gauss(0, 0, 0.22) * 0.35 * pulso(t, 0.0, 0.85)
    for k in range(4):
        a = q.uniform(0, TAU)
        G += T.lines([(0.2 * math.cos(a), 0.2 * math.sin(a), 0.45 * math.cos(a), 0.45 * math.sin(a), 1)], 0.025) * pulso(t, 0.05, 0.8)
    for k in range(3):
        a = TAU * k / 3 + t * 9
        G += T.polys([(estrela(0.35 * math.cos(a), 0.3 * math.sin(a), 0.06, a), 1.0)]) * briga * (1 - rel(t, 0.8, 0.95)) * 1.3
    H += T.gauss(0, 0, 0.1) * pulso(t, 0.1, 0.8) * 1.2
    return G * env, H * env


def chantagem(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    surge = ease_out(rel(t, 0.0, 0.3), 2)
    s = 0.5 + 0.5 * surge
    env_pts = [(-0.3 * s, -0.2 * s), (0.3 * s, -0.2 * s), (0.3 * s, 0.2 * s), (-0.3 * s, 0.2 * s)]
    G += T.polys([(env_pts, 1.0)], 0.004) * 0.35 + _contorno(T, env_pts, 0.014)
    G += T.lines([(-0.3 * s, -0.2 * s, 0, 0.02 * s, 1), (0, 0.02 * s, 0.3 * s, -0.2 * s, 1)], 0.012)
    fecha = ease_out(rel(t, 0.4, 0.7), 2)
    if fecha > 0:
        cy = 0.28
        G += T.polys([([(-0.1, cy), (0.1, cy), (0.1, cy + 0.14), (-0.1, cy + 0.14)], 1.0)], 0.003) * 1.2
        arco = [(0.065 * math.cos(u), cy - 0.02 - 0.06 * fecha - 0.07 * math.sin(u)) for u in np.linspace(0, math.pi, 12)]
        G += T.polyline(arco, 0.022) * 1.1
        H += T.gauss(0, cy + 0.07, 0.04) * pulso(t, 0.6, 0.85) * 1.6
    return G * env, H * env


def formula(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    frasco = [(-0.36, -0.05), (-0.24, -0.05), (-0.2, 0.25), (-0.4, 0.25)]
    G += _contorno(T, frasco, 0.014) * 1.1
    G += T.lines([(-0.33, -0.05, -0.33, -0.18, 1), (-0.27, -0.05, -0.27, -0.18, 1)], 0.012)
    enche = rel(t, 0.2, 0.9)
    G += T.polys([([(-0.39, 0.25), (-0.21, 0.25), (-0.215 - 0.02 * enche, 0.25 - 0.25 * enche), (-0.385 + 0.02 * enche, 0.25 - 0.25 * enche)], 1.0)]) * 0.8
    gotas = []
    for k in range(10):
        f = (t * 1.6 + k * 0.1) % 1
        if t < 0.1 or t > 0.85:
            continue
        gotas.append((0.4 - 0.7 * f, -0.12 + 0.12 * math.sin(f * math.pi * 2 + k), 1.0))
    G += T.splats(gotas, 0.025) * 1.2
    H += T.splats(gotas, 0.012) * 0.8
    G += T.ring(0.08, 0.02, cx=0.42, cy=-0.1) * pulso(t, 0.0, 0.8)
    return G * env, H * env


def robo_quebrou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cupula = [(0.36 * math.cos(u), 0.15 - 0.36 * math.sin(u)) for u in np.linspace(0, math.pi, 18)]
    racha = rel(t, 0.1, 0.4)
    if t < 0.45:
        G += T.polyline(cupula, 0.025) * 1.1
        G += T.lines([(0, -0.21, 0.04, -0.1, 1), (0.04, -0.1, -0.03, 0.0, 1), (-0.03, 0.0, 0.05, 0.12, 1)], 0.014) * racha * 1.3
    voa = rel(t, 0.42, 0.95)
    if voa > 0:
        q = np.random.default_rng(5)
        for k in range(8):
            a = math.pi * (k + 0.5) / 8
            d = 0.36 + 0.5 * ease_out(voa, 2)
            cx, cy = d * math.cos(a), 0.15 - d * math.sin(a) + 0.4 * voa * voa
            pedaco = _gira([(-0.06, -0.02), (0.06, -0.03), (0.04, 0.03), (-0.05, 0.03)], q.uniform(0, TAU) + voa * 6, cx, cy)
            G += T.polys([(pedaco, 1.0)], 0.003) * (1 - voa) * 1.2
        H += T.gauss(0, 0, 0.15) * pulso(t, 0.4, 0.65) * 1.6
    return G * env, H * env


def penny(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2)
    tela = [(-0.28, -0.22 * abre), (0.28, -0.22 * abre), (0.28, 0.12), (-0.28, 0.12)]
    G += T.polys([(tela, 1.0)], 0.004) * 0.3 + _contorno(T, tela, 0.014)
    G += T.lines([(-0.32, 0.12, 0.32, 0.12, 1)], 0.02)
    mira = rel(t, 0.3, 0.75)
    if mira > 0:
        r = 0.12 * (1.6 - 0.6 * ease_out(mira, 2))
        G += T.ring(r, 0.012, cy=-0.05) * 1.2
        G += T.lines([(-r - 0.04, -0.05, -r + 0.04, -0.05, 1), (r - 0.04, -0.05, r + 0.04, -0.05, 1), (0, -0.05 - r - 0.04, 0, -0.05 - r + 0.04, 1)], 0.012) * 1.2
    certo = pulso(t, 0.7, 0.98)
    G += T.polyline([(-0.06, -0.06), (-0.01, -0.0), (0.08, -0.12)], 0.025) * certo * 1.4
    H += T.gauss(0, -0.05, 0.05) * certo * 1.5
    return G * env, H * env


def kikoho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    forma = ease_out(rel(t, 0.0, 0.35), 2)
    s = 0.1 + 0.3 * forma
    tri = [(0, -s), (s * 0.95, s * 0.6), (-s * 0.95, s * 0.6)]
    G += _contorno(T, tri, 0.02) * 1.2 * (1 - rel(t, 0.55, 0.7))
    G += T.polys([(tri, 1.0)], 0.004) * 0.3 * (1 - rel(t, 0.55, 0.7))
    H += T.gauss(0, 0, 0.05) * forma * 1.2
    esmaga = rel(t, 0.45, 0.9)
    if esmaga > 0:
        y = -0.4 + 0.75 * ease_in(esmaga, 2)
        bloco = [(-0.4, y - 0.08), (0.4, y - 0.08), (0.45, y + 0.04), (-0.45, y + 0.04)]
        G += T.polys([(bloco, 1.0)], 0.006) * 0.9 * (1 - rel(t, 0.85, 0.97))
        G += T.ring(0.15 + 0.35 * esmaga, 0.03, cy=0.35, squash=3.0) * pulso(t, 0.7, 0.95) * 1.3
        H += T.gauss(0, 0.35, 0.12) * pulso(t, 0.7, 0.95) * 1.6
    return G * env, H * env


def parry(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    flash = pulso(t, 0.0, 0.3)
    G += T.polys([([(-0.03, -0.42), (0.03, -0.42), (0.06, 0.42), (-0.06, 0.42)], 1.0)], 0.01) * flash * 1.6
    H += T.gauss(0, 0, 0.06, 0.3) * flash * 2.0
    for k in range(2):
        r = 0.12 + 0.35 * rel(t, 0.05 + 0.08 * k, 0.4 + 0.08 * k)
        hexa = [(r * math.cos(TAU * j / 6 + 0.5), r * math.sin(TAU * j / 6 + 0.5)) for j in range(6)]
        G += _contorno(T, hexa, 0.014) * pulso(t, 0.05 + 0.08 * k, 0.5) * 1.1
    sobe = rel(t, 0.4, 0.9)
    if sobe > 0:
        for k in range(7):
            f = (sobe * 1.5 + k * 0.14) % 1
            x = 0.2 + 0.05 * math.sin(k * 2.4 + f * 8)
            y = 0.35 - 0.8 * f
            G += T.tapered([(x + 0.02, y - 0.08, x, y + 0.1, 1)], 0.06) * (1 - f) * 1.1
        H += T.gauss(0.2, -0.05, 0.08) * pulso(t, 0.45, 0.9) * 1.4
    return G * env, H * env


def penhasco(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    G += T.lines([(-0.5, 0.05, 0.05, 0.05, 1), (0.05, 0.05, 0.05, 0.5, 1)], 0.025) * (1 - rel(t, 0.8, 0.95))
    quebra = rel(t, 0.15, 0.4)
    G += T.lines([(-0.08, 0.05, -0.02, 0.13, 1), (-0.02, 0.13, -0.1, 0.22, 1)], 0.012) * quebra * 1.2
    cai = rel(t, 0.35, 0.95)
    if cai > 0:
        y = 0.05 + 0.7 * ease_in(cai, 2)
        G += T.polys([([(0.1, y - 0.08), (0.2, y), (0.12, y + 0.08), (0.02, y)], 1.0)]) * (1 - cai) * 1.2
        G += T.lines([(0.32, -0.25 + 0.4 * cai, 0.32, 0.05 + 0.4 * cai, 1)], 0.03) * (1 - rel(t, 0.7, 0.9)) * 1.1
        G += T.polys([([(0.24, 0.05 + 0.4 * cai), (0.4, 0.05 + 0.4 * cai), (0.32, 0.16 + 0.4 * cai)], 1.0)]) * (1 - rel(t, 0.7, 0.9)) * 1.2
        q = np.random.default_rng(3)
        G += T.splats([(q.uniform(-0.05, 0.25), 0.05 + 0.6 * cai * q.uniform(0.5, 1), 1.0) for _ in range(8)], 0.015) * (1 - cai)
    return G * env, H * env


def estica_jake(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    estica = ease_out(rel(t, 0.0, 0.55), 2)
    pts = []
    for u in np.linspace(0, estica, 30):
        a = math.pi * (1 - u)
        r = 0.42 + 0.02 * math.sin(u * 30)
        pts.append((r * math.cos(a), 0.25 - r * math.sin(a) * 0.9))
    if len(pts) > 1:
        G += T.polyline(pts, 0.07) * 0.55
        G += T.polyline(pts, 0.025) * 1.0
        H += T.gauss(*pts[-1], 0.05) * (1 - rel(t, 0.5, 0.7)) * 1.4
    protege = pulso(t, 0.5, 0.95)
    for x in (-0.25, 0.0, 0.25):
        G += T.ring(0.07, 0.012, cx=x, cy=0.2) * protege
    return G * env, H * env


def _passarangue(cx, cy, s, ang):
    asa = [(-s, -0.3 * s), (0, 0.15 * s), (s, -0.3 * s), (0.55 * s, 0.35 * s), (0, 0.05 * s), (-0.55 * s, 0.35 * s)]
    return _gira(asa, ang, cx, cy)


def sempre_junto(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    chega = ease_out(rel(t, 0.0, 0.5), 2)
    for s in (-1, 1):
        cx = s * (0.55 - 0.5 * chega)
        cy = -0.2 + 0.2 * chega
        G += T.polys([(_passarangue(cx, cy, 0.1, TAU * 1.5 * chega * s), 1.0)], 0.003) * (1 - rel(t, 0.5, 0.6)) * 1.3
        G += T.tapered([(cx + s * 0.25, cy - 0.06, cx, cy, 1)], 0.03) * (1 - chega) * 0.8
    choque = pulso(t, 0.45, 0.8)
    G += T.polys([(estrela(0, 0, 0.25 * choque + 0.01, 0.2, 8), 1.0)]) * choque * 1.3
    H += T.gauss(0, 0, 0.08) * choque * 1.8
    return G * env, H * env


def coragem_luigi(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    surge = ease_out(rel(t, 0.0, 0.3), 2)
    G += T.ring(0.16 * surge + 0.01, 0.022, cy=-0.05) * 1.2
    G += T.polyline([(-0.05, -0.13), (-0.05, 0.03), (0.06, 0.03)], 0.03) * surge * 1.3
    chama = rel(t, 0.2, 0.95)
    if chama > 0:
        for k in range(9):
            f = (chama * 1.6 + k * 0.11) % 1
            a = TAU * k / 9
            x = 0.3 * math.cos(a) * (1 - 0.3 * f)
            y = 0.25 - 0.6 * f + 0.05 * math.sin(a)
            G += T.tapered([(x + 0.02 * math.sin(f * 9), y - 0.1, x, y + 0.08, 1)], 0.06) * (1 - f) * 1.0
        H += T.gauss(0, 0, 0.15) * pulso(t, 0.25, 0.9) * 1.2
    return G * env, H * env


REGISTRO = [
    ("mu_tranquilizante", lambda T, t, r: _maior(tranquilizante, T, t, r, 1.3), GRANDE, "Solid Snake · o dardo e os Z do sono subindo", False),
    ("mu_contra_golpe", lambda T, t, r: _maior(contra_golpe, T, t, r, 1.25), GRANDE, "Mestre Splinter · o bastão varrendo e a seta do contra-golpe", False),
    ("mu_nao_fui", lambda T, t, r: _maior(nao_fui, T, t, r, 1.3), GRANDE, "Bart · a seta da culpa apontando para o lado", False),
    ("mu_galo", lambda T, t, r: _maior(galo, T, t, r, 1.3), GRANDE, "Peter Griffin · a nuvem de briga com estrelas", False),
    ("mu_chantagem", lambda T, t, r: _maior(chantagem, T, t, r, 1.3), GRANDE, "Cartman · o envelope da chantagem e o cadeado fechando", False),
    ("mu_formula", lambda T, t, r: _maior(formula, T, t, r, 1.3), GRANDE, "Plankton · o frasco sugando as gotas de Carga", False),
    ("mu_robo_quebrou", lambda T, t, r: _maior(robo_quebrou, T, t, r, 1.25), GRANDE, "Macaco Louco · a cúpula do robô rachando em pedaços", False),
    ("mu_penny", lambda T, t, r: _maior(penny, T, t, r, 1.35), GRANDE, "Bugiganga · o livro-computador da Penny e a mira", False),
    ("mu_kikoho", lambda T, t, r: _maior(kikoho, T, t, r, 1.2), GRANDE, "Tenshinhan · o triângulo e o Kikoho esmagando", False),
    ("mu_parry", lambda T, t, r: _maior(parry, T, t, r, 1.25), GRANDE, "Ken Masters · o lampejo azul do parry e a chama do troco", False),
    ("mu_penhasco", lambda T, t, r: _maior(penhasco, T, t, r, 1.2), GRANDE, "Heihachi · a beira do penhasco quebrando e a queda", False),
    ("mu_estica_jake", lambda T, t, r: _maior(estica_jake, T, t, r, 1.2), GRANDE, "Jake · o corpo esticando em arco por cima do trio", False),
    ("mu_sempre_junto", lambda T, t, r: _maior(sempre_junto, T, t, r, 1.25), GRANDE, "Robin · os dois pássaros-rangues chegando juntos", False),
    ("mu_coragem_luigi", lambda T, t, r: _maior(coragem_luigi, T, t, r, 1.3), GRANDE, "Luigi · a chama verde da coragem e o boné com L", False),
]
