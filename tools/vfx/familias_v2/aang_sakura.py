"""As habilidades do Aang e da Sakura, desenhadas para eles.

Aang
- bola_de_ar: a Rajada de ar voando — uma bola de vento em espiral, com as
  linhas de ar girando e o rastro (laço, viagem).
- rajada_aang: o vento estourando no rival — os anéis de ar abrindo, as linhas
  em redemoinho e a poeira levada.
- dobra_de_agua: no aliado, o chicote de água dá a volta nele e fecha numa
  bolha que protege, com as gotas e o brilho.
- avatar_brilho: o Estado Avatar acendendo — as setas brilhando e os quatro
  elementos girando em volta dele (ar, água, fogo e pedra) (Preparo, laço).
- avatar_aang: o Estado Avatar no campo dos rivais — o tornado gigante com os
  quatro elementos rodando nele, varrendo tudo.

Sakura
- controle_de_chakra: o chakra se juntando nela com precisão — os anéis
  apertando, o losango e o brilho no punho.
- forca_monstruosa: o soco que racha o chão — o punho, o clarão, as fendas
  correndo, os blocos de pedra subindo e as pétalas de cerejeira.
- byakugou_selo: o selo em losango acendendo na testa e as marcas se
  espalhando (Preparo, laço).
- byakugou_cura: a luz verde da cura subindo nos aliados com o losango e as
  pétalas.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _espiral_de_vento(T, cx, cy, r, giro, n_bracos=3, larg=0.02, voltas=0.9, sq=1.0):
    """Linhas de vento em espiral (braços que se enrolam para o centro)."""
    m = T.zero()
    for b in range(n_bracos):
        pts = []
        for k in range(30):
            f = k / 29
            a = giro + TAU * b / n_bracos + TAU * voltas * f
            rr = r * (0.2 + 0.8 * f)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * sq))
        m += T.polyline(pts, larg)
    return m


def _petala(cx, cy, r, ang):
    """Uma pétala de cerejeira: gota com o entalhe na ponta."""
    pts = []
    for k in range(13):
        f = k / 12
        a = math.pi * f
        rr = r * math.sin(a) ** 0.8
        pts.append((r * 1.6 * (f - 0.5), rr * 0.6 * (1 if k % 12 else 0.6)))
    pts += [(r * 0.8, 0.0), (r * 0.55, -0.12 * r)]
    pts = pts + [(x, -y) for x, y in reversed(pts[:-2])]
    return _gira(pts, ang, cx, cy)


def _losango(cx, cy, r):
    return [(cx, cy - r), (cx + r * 0.7, cy), (cx, cy + r), (cx - r * 0.7, cy)]


# =================================================================== Aang
def bola_de_ar(T, t, rng):
    """A Rajada de ar voando para +x: a bola de vento em espiral, girando rápido, as linhas de ar em
    volta e o rastro que se desfaz."""
    G, H = vazio(T)
    cx = 0.3
    E = _espiral_de_vento(T, cx, 0, 0.28, -TAU * t * 2, 3, 0.022, 1.1)
    nucleo = T.gauss(cx, 0, 0.1)
    rastro = T.zero()
    for y in (-0.15, 0.0, 0.15):
        pts = [(cx - 0.2 - 0.75 * f, y * (1 + f) + 0.05 * math.sin(TAU * (f * 1.5 - t * 3))) for f in np.linspace(0, 1, 18)]
        rastro += T.polyline(pts, 0.014) * 0.7
    rastro *= np.clip((T.U + 0.6) / 0.8, 0, 1)
    G += E * 1.1 + T.blur(E, 0.02) * 0.5 + nucleo * 0.9 + rastro * 0.8
    H += E * 0.35 + nucleo * 0.6
    return G, H


def rajada_aang(T, t, rng):
    """O vento estourando no rival: os anéis de ar abrindo um atrás do outro, o redemoinho girando
    no lugar, as linhas de vento passando para +x e a poeira levada."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    aneis = T.zero()
    for j in range(3):
        f = rel(t, 0.08 * j, 0.08 * j + 0.5)
        if 0 < f < 1:
            aneis += T.ring(0.1 + 0.75 * ease_out(f, 2), 0.035 * (1 - f) + 0.008) * (1 - f)
    rede = _espiral_de_vento(T, 0, 0, 0.45 * ease_out(rel(t, 0.0, 0.3), 2) + 0.01, -TAU * t * 1.5, 4, 0.016, 0.8) * pulso(t, 0.0, 0.8)
    linhas = T.tapered([(-0.6 + 1.4 * rel(t, 0.05, 0.6), y, -0.1 + 1.4 * rel(t, 0.05, 0.6), y * 0.8, 1.0) for y in (-0.3, -0.1, 0.12, 0.32)], 0.025) * pulso(t, 0.05, 0.7)
    sub = np.random.default_rng(11)
    po = T.splats([(sub.normal(0, 0.2) + 0.7 * rel(t, 0.1, 1.0), sub.normal(0.2, 0.15), 0.8) for _ in range(10)], 0.05) * pulso(t, 0.1, 1.0) * 0.4
    k = pulso(t, 0.0, 0.3)
    G += (aneis * 1.2 + rede * 0.9 + linhas * 0.8 + po + T.gauss(0, 0, 0.18) * k) * env
    H += (aneis * 0.4 + rede * 0.3 + T.gauss(0, 0, 0.1) * k * 0.8) * env
    return G, H


def dobra_de_agua(T, t, rng):
    """A Dobra de água no aliado: o chicote de água vem de −x, dá a volta nele girando e fecha numa
    bolha que fica brilhando, com as gotas espirrando."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    volta = ease_out(rel(t, 0.0, 0.45), 1.6)
    chicote = T.zero()
    if volta > 0:
        a1 = math.pi + TAU * 1.1 * volta
        chicote = T.arc_band(0.5, 0.06, math.pi * 0.9, a1, 1.0, 0.0, 0, 0, 0.6)
        cauda = T.tapered([(-1.0, 0.1, -0.5, 0.0, 1.0)], 0.1) * (1 - rel(t, 0.15, 0.35))
        chicote = chicote * (1 - rel(t, 0.45, 0.6)) + cauda
    bolha = (T.ring(0.55, 0.04) * 1.0 + np.clip(1 - T.RAD / 0.55, 0, 1) ** 0.5 * (T.RAD < 0.55) * 0.2) * rel(t, 0.4, 0.55)
    reflexo = T.arc_band(0.45, 0.025, math.pi * 1.1, math.pi * 1.45, 1.0, 0.0) * rel(t, 0.45, 0.6)
    ondas = T.ring(0.55 + 0.03 * math.sin(TAU * t * 4), 0.015) * rel(t, 0.5, 0.6) * 0.5
    sub = np.random.default_rng(19)
    gotas = []
    for _ in range(18):
        a = sub.uniform(0, TAU)
        f = rel(t, 0.4, 0.85)
        d = 0.55 + 0.35 * ease_out(f, 2) * sub.uniform(0.3, 1)
        gotas.append((d * math.cos(a), d * math.sin(a) + 0.3 * f * f, pulso(t, 0.4, 0.85) * sub.uniform(0.4, 1)))
    respira = 0.85 + 0.15 * math.sin(TAU * t * 3)
    G += (chicote * 1.2 + (bolha + reflexo * 0.9 + ondas) * respira + T.splats(gotas, 0.012) * 1.1) * env
    H += (chicote * 0.5 + reflexo * 0.8 + bolha * 0.2) * env
    return G, H


def _quatro_elementos(T, t, r, sq=0.5, tam=1.0):
    """Ar, água, fogo e pedra girando em volta de um centro: um redemoinho, uma gota, uma chama e um
    bloco."""
    G = T.zero()
    for j in range(4):
        a = TAU * (t * 0.6 + j / 4)
        x, y = r * math.cos(a), r * math.sin(a) * sq
        if j == 0:
            G += _espiral_de_vento(T, x, y, 0.09 * tam, -TAU * t * 3, 3, 0.01, 0.9)
        elif j == 1:
            G += T.polys([([(x, y - 0.1 * tam), (x + 0.06 * tam, y + 0.02), (x, y + 0.07 * tam), (x - 0.06 * tam, y + 0.02)], 1.0)], 0.01)
        elif j == 2:
            G += T.polys([(estrela(x, y, 0.08 * tam, -math.pi / 2, 3, 0.45), 1.0)], 0.012) + T.gauss(x, y + 0.02, 0.05 * tam) * 0.6
        else:
            G += T.polys([(_gira([(-0.06, -0.05), (0.06, -0.06), (0.07, 0.05), (-0.05, 0.06)], a, x, y), 1.0)], 0.004) if tam >= 1 else T.zero()
    return G


def avatar_brilho(T, t, rng):
    """O Estado Avatar acendendo no Preparo: as setas de ar brilhando (uma na testa, as dos braços),
    o brilho branco dos olhos e os quatro elementos girando em volta dele."""
    G, H = vazio(T)
    pul = 0.8 + 0.2 * math.sin(TAU * t * 4)
    setas = T.polys([([(-0.05, -0.35), (0.05, -0.35), (0.05, -0.15), (0.11, -0.15), (0.0, 0.02), (-0.11, -0.15), (-0.05, -0.15)], 1.0)], 0.006)
    olhos = T.gauss(-0.08, -0.05, 0.03) + T.gauss(0.08, -0.05, 0.03)
    E = _quatro_elementos(T, t, 0.62, 0.5)
    aura = T.gauss(0, 0, 0.35) * 0.4 * pul
    G += setas * 1.2 * pul + olhos * 1.6 * pul + E * 1.1 + aura
    H += setas * 0.8 * pul + olhos * 1.8 * pul + E * 0.3
    return G, H


def avatar_aang(T, t, rng):
    """O Estado Avatar no campo dos rivais: o tornado gigante subindo do chão (linhas de vento
    girando, mais largo em cima), os quatro elementos rodando dentro dele, a poeira e o clarão."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sobe = ease_out(rel(t, 0.0, 0.35), 2)
    tornado = T.zero()
    for j in range(9):
        y = 0.55 - 1.3 * sobe * (j / 8)
        r = 0.18 + 0.55 * (j / 8)
        fase = TAU * (t * 1.8 + j * 0.13)
        tornado += T.arc_band(r, 0.025, fase, fase + 3.6, 0.25, 0.0, 0.05 * math.sin(TAU * t + j), y, 0.8)
    tornado *= 1 - rel(t, 0.75, 0.95)
    E = _quatro_elementos(T, t * 2.0, 0.55, 0.3, 1.4) * pulso(t, 0.15, 0.85)
    k = pulso(t, 0.2, 0.55)
    clarao = T.gauss(0, 0, 0.4) * k * 1.0
    sub = np.random.default_rng(29)
    po = T.splats([(sub.normal(0, 0.45), 0.45 - 0.3 * rel(t, 0.1, 1.0) * sub.uniform(0.3, 1), 0.8) for _ in range(14)], 0.08) * pulso(t, 0.1, 1.0) * 0.45
    G += (tornado * 1.1 + T.blur(tornado, 0.02) * 0.5 + E * 1.2 + clarao + po) * env
    H += (tornado * 0.35 + E * 0.4 + clarao * 0.8) * env
    return G, H


# =================================================================== Sakura
def controle_de_chakra(T, t, rng):
    """O Controle de chakra: os anéis de chakra apertando nela com precisão (de fora para dentro), o
    losango acendendo no meio e o brilho que fica no punho."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    aneis = T.zero()
    for j in range(4):
        f = rel(t, 0.06 * j, 0.06 * j + 0.45)
        if 0 < f < 1:
            aneis += T.ring(0.8 * (1 - ease_in(f, 1.5)) + 0.08, 0.02) * (0.4 + 0.6 * f)
    L = T.polys([(_losango(0, 0, 0.16 * ease_out(rel(t, 0.3, 0.5), 2) + 1e-3), 1.0)], 0.004) * pulso(t, 0.3, 0.9)
    k = pulso(t, 0.35, 0.8)
    punho = T.gauss(0, 0, 0.12) * k * 1.4 + T.flare(0, 0, 0.8 * k + 1e-3, 0.4, 0.012) * k
    sub = np.random.default_rng(37)
    fa = T.splats([(0.6 * math.cos(a) * (1 - rel(t, 0, 0.5)), 0.6 * math.sin(a) * (1 - rel(t, 0, 0.5)), 0.8) for a in sub.uniform(0, TAU, 16)], 0.014) * (1 - rel(t, 0.45, 0.55))
    G += (aneis * 1.2 + L * 1.2 + punho + fa) * env
    H += (aneis * 0.4 + L * 0.8 + punho * 1.1) * env
    return G, H


def forca_monstruosa(T, t, rng):
    """A Força monstruosa: o punho dela entra (de −x), o clarão, o chão racha em fendas que correm
    para os lados, os blocos de pedra sobem girando e as pétalas de cerejeira voam."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    entra = ease_in(rel(t, 0.0, 0.14), 1.6)
    punho = T.gauss(-0.9 + 0.9 * entra, 0.0, 0.11, 0.09) * (1 - rel(t, 0.15, 0.3))
    risco = T.tapered([(-1.0, 0, -0.9 + 0.9 * entra, 0, 1.0)], 0.1) * (1 - rel(t, 0.14, 0.28))
    k = pulso(t, 0.12, 0.45)
    clarao = T.gauss(0, 0, 0.26) * k * 1.8 + T.flare(0, 0, 1.3 * k + 1e-3, 0.0, 0.01) * k
    q = np.random.default_rng(41)
    fendas = T.zero()
    if t > 0.12:
        cresce = ease_out(rel(t, 0.12, 0.35), 2)
        for j in range(8):
            a = TAU * j / 8 + q.uniform(-0.2, 0.2)
            comp = 0.9 * cresce * q.uniform(0.6, 1)
            fendas += T.polyline(jagged(q, 0, 0.3, comp * math.cos(a), 0.3 + comp * math.sin(a) * 0.35, 4, 0.25), 0.014)
        fendas *= 1 - rel(t, 0.7, 0.95)
    blocos = []
    for j in range(8):
        a = -math.pi / 2 + q.normal(0, 0.8)
        f = rel(t, 0.14, 0.85)
        d = 0.75 * ease_out(f, 2) * q.uniform(0.4, 1)
        x, y = d * math.cos(a), d * math.sin(a) + 0.6 * f * f + 0.2
        s = 0.06 * q.uniform(0.7, 1.3)
        blocos.append((_gira([(-s, -s), (s, -s * 0.8), (s * 0.9, s), (-s, s * 0.9)], 4 * f + j, x, y), pulso(t, 0.14, 0.9)))
    B = T.polys(blocos, 0.003)
    petalas = []
    for j in range(10):
        a = q.uniform(0, TAU)
        f = rel(t, 0.2, 1.0)
        d = 0.25 + 0.6 * ease_out(f, 1.5) * q.uniform(0.4, 1)
        petalas.append((_petala(d * math.cos(a), d * math.sin(a) - 0.2 * f, 0.045, a + 3 * f), pulso(t, 0.2, 1.0) * 0.8))
    P = T.polys(petalas, 0.003)
    G += (punho * 1.4 + risco * 0.6 + clarao + fendas * 1.2 + B * 1.0 + P * 0.9) * env
    H += (punho * 1.0 + clarao * 1.1 + fendas * 0.6 + B * 0.2) * env
    return G, H


def byakugou_selo(T, t, rng):
    """O Byakugou no Preparo: o losango acendendo na testa e as marcas escuras se espalhando em
    linhas a partir dele, pulsando, com o chakra subindo."""
    G, H = vazio(T)
    pul = 0.8 + 0.2 * math.sin(TAU * t * 3)
    L = T.polys([(_losango(0, -0.2, 0.09), 1.0)], 0.004)
    marcas = T.zero()
    for j in range(6):
        a = TAU * j / 6 + 0.3
        comp = 0.25 + 0.35 * ((t * 1.5 + j * 0.2) % 1)
        pts = [(0, -0.2), (comp * 0.5 * math.cos(a), -0.2 + comp * 0.5 * math.sin(a) + 0.04), (comp * math.cos(a), -0.2 + comp * math.sin(a))]
        marcas += T.polyline(pts, 0.012)
    sub = np.random.default_rng(43)
    sobe = T.splats([(sub.normal(0, 0.3), 0.6 - 1.2 * ((sub.uniform() + t) % 1), sub.uniform(0.3, 0.9)) for _ in range(20)], 0.014)
    G += L * 1.5 * pul + T.gauss(0, -0.2, 0.12) * pul + marcas * 0.9 + sobe
    H += L * 1.2 * pul + marcas * 0.4
    return G, H


def byakugou_cura(T, t, rng):
    """A cura do Byakugou nos aliados: a coluna de luz verde subindo, o losango aparecendo no alto,
    as pétalas girando para cima e o anel no chão."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    sobe = ease_out(rel(t, 0.0, 0.35), 2)
    coluna = np.exp(-(T.U / 0.3) ** 2) * np.clip((0.55 - T.V) / 1.2, 0, 1) * (T.V > 0.55 - 1.3 * sobe) * 0.7
    anel = T.ring(0.55, 0.035, 0, 0.5, 3.2) * pulso(t, 0.0, 0.85)
    L = T.polys([(_losango(0, -0.55, 0.1 * back(rel(t, 0.3, 0.55), 1.5) + 1e-3), 1.0)], 0.004) * pulso(t, 0.3, 0.95)
    sub = np.random.default_rng(47)
    petalas = []
    for j in range(12):
        f = (sub.uniform() + t * 0.9) % 1
        a = TAU * (sub.uniform() + t * 0.5)
        r = 0.3 + 0.15 * sub.uniform()
        petalas.append((_petala(r * math.cos(a), 0.5 - 1.2 * f, 0.04, a), (1 - f) * rel(t, 0.15, 0.3)))
    P = T.polys(petalas, 0.003)
    cruzes = T.zero()
    for j, x in enumerate((-0.4, 0.4)):
        y = 0.3 - 0.8 * ((t * 1.2 + j * 0.5) % 1)
        cruzes += T.lines([(x - 0.06, y, x + 0.06, y, 1.0), (x, y - 0.06, x, y + 0.06, 1.0)], 0.02)
    G += (coluna + anel * 1.1 + L * 1.3 + P * 0.9 + cruzes * 0.8 * rel(t, 0.2, 0.35)) * env
    H += (coluna * 0.4 + L * 1.0 + anel * 0.3) * env
    return G, H


REGISTRO = [
    ("bola_de_ar", bola_de_ar, MEDIA, "Aang · a Rajada de ar voando em espiral (laço)", True),
    ("rajada_aang", rajada_aang, GRANDE, "Aang · o vento estourando no rival", False),
    ("dobra_de_agua", dobra_de_agua, GRANDE, "Aang · o chicote de água fecha a bolha no aliado", False),
    ("avatar_brilho", avatar_brilho, MEDIA, "Aang · as setas acendendo e os quatro elementos (laço)", True),
    ("avatar_aang", avatar_aang, GRANDE, "Aang · o tornado do Estado Avatar com os quatro elementos", False),
    ("controle_de_chakra", controle_de_chakra, GRANDE, "Sakura · o chakra apertando no punho", False),
    ("forca_monstruosa", forca_monstruosa, GRANDE, "Sakura · o soco que racha o chão, com as pétalas", False),
    ("byakugou_selo", byakugou_selo, MEDIA, "Sakura · o selo do Byakugou acendendo (laço)", True),
    ("byakugou_cura", byakugou_cura, GRANDE, "Sakura · a luz verde da cura com o losango e as pétalas", False),
]
