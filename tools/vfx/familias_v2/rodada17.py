"""Rodada 17 das habilidades próprias: Groot, Rocket Raccoon, Aquaman, Lanterna Verde e Ciborgue.

Groot
- muralha_de_galhos: os galhos sobem do chão em volta do aliado e se trançam numa muralha, com as folhas e os
  espinhos (Escudo e Espinhos).
- eu_sou_groot: as raízes correm pelo chão até cada aliado e brotam em ramos que os cobrem, com as florzinhas e
  as folhas caindo (Escudo e Regeneração).
- groot_preparo: o Preparo das Raízes de captura — os braços de galho fincados no chão e as raízes pulsando por
  baixo (laço).
- raizes_de_captura: as raízes rompem o chão debaixo do rival e o enlaçam, apertando (Preso).

Rocket Raccoon
- armadilha_explosiva: a minazinha com a luz piscando cai rolando perto do rival, apita e explode em fumaça
  colorida que deixa tonto, e o contador da Bomba fica nele.
- missil_caseiro: o míssil remendado (o corpo torto, as aletas e a fita) sai fazendo zigue-zague, soltando
  fumaça, e explode.
- rocket_preparo: o Preparo do Arsenal pesado — o canhão enorme montando peça por peça, com as luzes carregando
  (laço).

Aquaman
- mare_puxante: a onda sobe atrás dos rivais e os puxa de volta (as linhas de corrente), e a água vira uma
  bolha protetora no trio dele.
- aquaman_preparo: o Preparo do Comando dos mares — o tridente erguido com a água subindo em espiral e as
  silhuetas dos tubarões rondando (laço).
- comando_dos_mares: a onda gigante se levanta e quebra sobre os rivais, com os tubarões saltando na crista e a
  espuma explodindo.

Lanterna Verde
- escudo_de_vontade: o anel brilha e o construto de escudo (a placa com o símbolo da lanterna) se monta na
  frente do aliado, com a barreira por cima.
- punho_esmeralda: o punho verde gigante de construto voa até o rival, soca e vira uma jaula que o prende
  (Preso, e o Preparo é cancelado).
- lanterna_preparo: o Preparo do Construto adaptável — a lanterna de força com a chama verde e o anel brilhando,
  as linhas de construto se formando em volta (laço).
- construto_adaptavel: o construto muda de forma no ar (um martelo, depois uma lâmina, depois um míssil) e acerta
  o rival com o último.

Ciborgue
- varredura_tatica: o olho vermelho cibernético dispara a grade de varredura no rival, os números correm e o
  alvo é marcado.
- ciborgue_preparo: o Preparo da Adaptação de sistema — o braço se transformando em canhão (as placas abrindo e
  as luzes azuis), com a barra de carga enchendo (laço).
- adaptacao_de_sistema: o pulso azul de interferência sai do braço, o Preparo do rival trava em estática (a
  imagem que falha) e o golpe de energia acerta em cheio.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .rodada13 import _borda, _contorno, _gira


def _folha(cx, cy, tam, ang):
    dx, dy = math.cos(ang) * tam, math.sin(ang) * tam
    return lamina(cx - dx, cy - dy, cx + dx, cy + dy, tam * 0.45)


def _galho(pts, w0, w1):
    """O galho afinando da base até a ponta (uma faixa de largura variável)."""
    esq, dir_ = [], []
    for k, (x, y) in enumerate(pts):
        u = k / max(1, len(pts) - 1)
        if k < len(pts) - 1:
            dx, dy = pts[k + 1][0] - x, pts[k + 1][1] - y
        else:
            dx, dy = x - pts[k - 1][0], y - pts[k - 1][1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = w0 + (w1 - w0) * u
        esq.append((x + nx * w, y + ny * w))
        dir_.append((x - nx * w, y - ny * w))
    return esq + dir_[::-1]


# =================================================================== Groot
def muralha_de_galhos(T, t, rng):
    """A muralha de galhos: os galhos sobem do chão em volta do aliado e se trançam por cima dele numa muralha, com
    as folhas brotando e os espinhos saindo das bordas (Escudo e Espinhos)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    sobe = ease_out(rel(t, 0.0, 0.45), 2)
    if sobe > 0:
        shapes = []
        for k in range(7):
            x0 = -0.45 + 0.15 * k
            lado = 1 if k < 3 else (-1 if k > 3 else 0)
            pts = []
            for j in range(12):
                u = j / 11 * sobe
                pts.append((x0 + lado * 0.25 * math.sin(u * math.pi * 0.9) * u + 0.04 * math.sin(u * 8 + k), 0.45 - 0.85 * u))
            shapes.append((_galho(pts, 0.03, 0.008), 1.0))
        Gh = T.polys(shapes)
        G += Gh * 0.45 + _borda(T, Gh, 0.006) * 1.3
    folhas = rel(t, 0.3, 0.7)
    if folhas > 0:
        q = np.random.default_rng(3)
        shapes = []
        for k in range(14):
            x, y = q.uniform(-0.45, 0.45), q.uniform(-0.4, 0.3)
            shapes.append((_folha(x, y, 0.035 * min(1, folhas * 2), q.uniform(0, TAU)), 1.0))
        G += T.polys(shapes) * 0.9
    espinhos = pulso(t, 0.45, 1.0)
    if espinhos > 0:
        linhas = []
        for k in range(10):
            a = -math.pi + math.pi * k / 9
            x, y = 0.48 * math.cos(a), 0.05 + 0.48 * math.sin(a)
            linhas.append((x, y, x + 0.09 * math.cos(a), y + 0.09 * math.sin(a), 1.0))
        G += T.tapered(linhas, 0.02) * espinhos * 1.2
    return G * env, H * env


def eu_sou_groot(T, t, rng):
    """Eu sou Groot: as raízes correm pelo chão a partir do Groot até cada aliado e brotam em ramos que os cobrem,
    com as florzinhas abrindo e as folhas caindo devagar (Escudo e Regeneração)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    corre = ease_out(rel(t, 0.0, 0.35), 2)
    aliados = [(-0.55, 0.3), (0.0, 0.32), (0.55, 0.3)]
    if corre > 0:
        for k, (x, y) in enumerate(aliados):
            pts = [(-0.85 + (x + 0.85) * u * corre, 0.48 + 0.03 * math.sin(u * 14 + k)) for u in np.linspace(0, 1, 20)]
            G += T.polyline(pts, 0.014) * (1 - rel(t, 0.7, 0.85)) * 1.1
    brota = ease_out(rel(t, 0.3, 0.6), 2.5)
    if brota > 0:
        for k, (x, y) in enumerate(aliados):
            shapes = []
            for lado in (-1, 1):
                pts = [(x + lado * 0.18 * math.sin(u * math.pi * 0.8), y + 0.18 - 0.4 * u * brota) for u in np.linspace(0, 1, 10)]
                shapes.append((_galho(pts, 0.022, 0.006), 1.0))
            Gh = T.polys(shapes)
            G += Gh * 0.45 + _borda(T, Gh, 0.006) * 1.2
            for j in range(3):
                fx, fy = x + 0.12 * math.cos(j * 2.1 + k), y - 0.12 + 0.06 * math.sin(j * 2.1)
                G += T.polys([(estrela(fx, fy, 0.035 * brota, 0.3, 5, 0.5), 1.0)]) * 0.9
                H += T.gauss(fx, fy, 0.012) * brota
    cai = rel(t, 0.4, 1.0)
    if 0 < cai < 1:
        q = np.random.default_rng(13)
        shapes = []
        for k in range(10):
            x = q.uniform(-0.8, 0.8) + 0.05 * math.sin(cai * 8 + k)
            y = -0.5 + 0.9 * ((cai + q.uniform(0, 1)) % 1)
            shapes.append((_folha(x, y, 0.03, cai * 6 + k), 1 - cai))
        G += T.polys(shapes) * 0.8
    return G * env, H * env


def groot_preparo(T, t, rng):
    """O Preparo das Raízes de captura: os dois braços de galho fincados no chão e as raízes pulsando por baixo da
    terra, espalhando (laço)."""
    G, H = vazio(T)
    shapes = []
    for lado in (-1, 1):
        pts = [(lado * (0.12 + 0.3 * u), -0.3 + 0.75 * u + 0.04 * math.sin(u * 6)) for u in np.linspace(0, 1, 12)]
        shapes.append((_galho(pts, 0.04, 0.02), 1.0))
    Gh = T.polys(shapes)
    G += Gh * 0.5 + _borda(T, Gh, 0.007) * 1.3
    for k in range(6):
        a = math.pi * (0.1 + 0.8 * k / 5)
        pul = (t * 2 + k / 6) % 1
        pts = [(0.4 * u * math.cos(a) * 1.8, 0.48 + 0.12 * u * math.sin(a) + 0.02 * math.sin(u * 12)) for u in np.linspace(0, 1, 14)]
        G += T.polyline(pts, 0.01) * 0.9
        H += T.gauss(0.4 * pul * math.cos(a) * 1.8, 0.48 + 0.12 * pul * math.sin(a), 0.02) * 1.2
    return G, H


def raizes_de_captura(T, t, rng):
    """As raízes de captura: o chão racha debaixo do rival, as raízes rompem para cima e o enlaçam em espiral,
    apertando (Preso)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    racha = pulso(t, 0.0, 0.5)
    if racha > 0:
        q = np.random.default_rng(23)
        for k in range(5):
            a = math.pi * (0.05 + 0.9 * k / 4)
            G += T.polyline(jagged(q, 0, 0.45, 0.45 * math.cos(a) * 1.4, 0.45 + 0.08 * math.sin(a), 4, 0.25), 0.012) * racha
    sobe = ease_out(rel(t, 0.15, 0.5), 2.2)
    if sobe > 0:
        shapes = []
        for k in range(4):
            fase = k * TAU / 4
            pts = []
            for j in range(18):
                u = j / 17 * sobe
                a = fase + u * TAU * 1.3
                pts.append((0.22 * math.cos(a) * (1 - 0.3 * u), 0.45 - 0.75 * u))
            shapes.append((_galho(pts, 0.035, 0.01), 1.0))
        Gh = T.polys(shapes)
        aperta = pulso(t, 0.45, 0.75)
        G += Gh * 0.45 + _borda(T, Gh, 0.006) * 1.3 + T.ring(0.2, 0.02, 0, 0.0, squash=2.5) * aperta
    g = pulso(t, 0.4, 0.7)
    H += T.gauss(0, 0.05, 0.1) * g * 1.0
    return G * env, H * env


# =================================================================== Rocket Raccoon
def armadilha_explosiva(T, t, rng):
    """A armadilha explosiva: a minazinha redonda com a luz vermelha cai rolando perto do rival, apita piscando cada
    vez mais rápido e explode em fumaça colorida que deixa tonto; o contador da Bomba fica nele."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    rola = rel(t, 0.0, 0.3)
    if t < 0.5:
        x = -0.7 + 0.6 * ease_out(rola, 2)
        y = 0.25 - 0.3 * math.sin(math.pi * min(1, rola * 1.3)) * (1 - rola)
        M = T.polys([([(x + 0.11 * math.cos(a), y + 0.07 * math.sin(a)) for a in np.linspace(0, TAU, 24, endpoint=False)], 1.0)])
        G += M * 0.4 + _borda(T, M, 0.006) * 1.3 + T.lines([(x - 0.11, y, x + 0.11, y, 1.0)], 0.01) + T.lines(_contorno([(x - 0.04, y - 0.12), (x + 0.04, y - 0.12), (x + 0.04, y - 0.07), (x - 0.04, y - 0.07)]), 0.008)
        pisca = 0.5 + 0.5 * math.cos(t * (20 + 120 * rel(t, 0.2, 0.45)))
        H += T.gauss(x, y - 0.1, 0.03) * pisca * 2.0
    bum = rel(t, 0.45, 0.85)
    if 0 < bum < 1:
        e = ease_out(bum, 3)
        H += T.gauss(-0.1, 0.25, 0.1 + 0.2 * e) * (1 - bum) ** 2 * 2.0
        q = np.random.default_rng(31)
        pts = [(-0.1 + 0.5 * e * math.cos(a) * q.uniform(0.5, 1), 0.25 + 0.35 * e * math.sin(a) * q.uniform(0.5, 1) - 0.15 * bum, 1 - bum) for a in np.linspace(0, TAU, 16, endpoint=False)]
        F = np.clip(T.splats(pts, 0.07), 0, 1)
        G += F * 0.5 + _borda(T, F, 0.015) * 1.0
    conta = pulso(t, 0.6, 1.0)
    if conta > 0:
        G += T.ring(0.09, 0.012, 0.0, -0.35) * conta + T.lines([(0, -0.35, 0, -0.41, 1.0), (0, -0.35, 0.04, -0.33, 1.0)], 0.01) * conta
        H += T.gauss(0.0, -0.44, 0.015) * conta * (0.5 + 0.5 * math.cos(t * 30))
    return G * env, H * env


def _missil(T, cx, cy, s, ang):
    corpo = _gira([(-0.12 * s, -0.03 * s), (0.08 * s, -0.035 * s), (0.14 * s, 0.0), (0.08 * s, 0.03 * s), (-0.12 * s, 0.035 * s)], ang, cx, cy)
    aletas = [_gira([(-0.12 * s, lado * 0.035 * s), (-0.17 * s, lado * 0.08 * s), (-0.08 * s, lado * 0.03 * s)], ang, cx, cy) for lado in (-1, 1)]
    P = T.polys([(corpo, 1.0)] + [(a, 1.0) for a in aletas])
    fita = T.lines([(*_gira([(-0.02 * s, -0.04 * s)], ang, cx, cy)[0], *_gira([(0.01 * s, 0.04 * s)], ang, cx, cy)[0], 1.0)], 0.01 * s)
    return P * 0.5 + _borda(T, P, 0.005) * 1.3 + fita * 0.8


def missil_caseiro(T, t, rng):
    """O míssil caseiro: o míssil remendado (corpo torto, aletas e a fita no meio) sai fazendo zigue-zague, soltando
    a fumaça e as faíscas, e explode no rival."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    voa = rel(t, 0.05, 0.42)
    if 0 < voa < 1:
        u = ease_in(voa, 1.3)
        x = -0.85 + 0.85 * u
        y = 0.12 * math.sin(u * TAU * 1.5) * (1 - u)
        dy = 0.12 * TAU * 1.5 * math.cos(u * TAU * 1.5) * (1 - u) - 0.12 * math.sin(u * TAU * 1.5)
        ang = math.atan2(dy, 0.85)
        G += _missil(T, x, y, 1.4, ang)
        H += T.gauss(x - 0.2 * math.cos(ang), y - 0.2 * math.sin(ang), 0.03) * 1.6
        rastro = []
        for k in range(12):
            uu = max(0, u - 0.04 * (k + 1))
            rastro.append((-0.85 + 0.85 * uu, 0.12 * math.sin(uu * TAU * 1.5) * (1 - uu), (1 - k / 12) * 0.8))
        G += T.splats(rastro, 0.03) * 0.6
    bum = rel(t, 0.4, 0.82)
    if 0 < bum < 1:
        e = ease_out(bum, 3)
        H += T.gauss(0, 0, 0.1 + 0.25 * e) * (1 - bum) ** 2 * 2.2
        G += T.ring(0.08 + 0.45 * e, 0.04, 0, 0) * (1 - bum) * 1.3
        raios = [(0.06 * math.cos(a), 0.06 * math.sin(a), (0.25 + 0.45 * e) * math.cos(a), (0.25 + 0.45 * e) * math.sin(a), 1 - bum) for a in np.linspace(0, TAU, 14, endpoint=False)]
        G += T.tapered(raios, 0.025)
    return G * env, H * env


def rocket_preparo(T, t, rng):
    """O Preparo do Arsenal pesado: o canhão enorme montando peça por peça (os canos, o carregador e a mira
    encaixando) com as luzes de carga enchendo (laço)."""
    G, H = vazio(T)
    pecas = [([(-0.45, -0.05), (0.3, -0.05), (0.3, 0.08), (-0.45, 0.08)], 0.0),
             ([(0.3, -0.03), (0.55, -0.03), (0.55, 0.0), (0.3, 0.0)], 0.15),
             ([(0.3, 0.03), (0.55, 0.03), (0.55, 0.06), (0.3, 0.06)], 0.25),
             ([(-0.2, 0.08), (-0.05, 0.08), (-0.08, 0.3), (-0.18, 0.3)], 0.35),
             ([(-0.1, -0.05), (0.1, -0.05), (0.06, -0.15), (-0.06, -0.15)], 0.45)]
    for pts, t0 in pecas:
        u = ease_out(rel(t, t0, t0 + 0.2), 3)
        if u > 0:
            off = 0.15 * (1 - u)
            P = T.polys([([(x, y - off) for x, y in pts], 1.0)])
            G += P * 0.4 + _borda(T, P, 0.006) * 1.3
    for k in range(5):
        cheio = rel(t, 0.5 + 0.08 * k, 0.55 + 0.08 * k)
        H += T.gauss(-0.38 + 0.12 * k, 0.015, 0.018) * (0.25 + 0.75 * cheio) * 1.3
    return G, H


# =================================================================== Aquaman
def mare_puxante(T, t, rng):
    """A maré puxante: a onda sobe atrás dos rivais e os puxa para trás (as linhas da corrente indo para longe), e
    a água vira uma bolha protetora em volta do trio do Aquaman (Enfraquecido e Escudo)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    sobe = ease_out(rel(t, 0.0, 0.35), 2)
    b = 1 - rel(t, 0.6, 0.8)
    if sobe > 0:
        pts = [(x, -0.75 + 0.35 * (1 - sobe) + 0.05 * math.sin(x * 9 + t * 12)) for x in np.linspace(-1, 1, 40)]
        crista = T.polyline(pts, 0.03)
        G += (crista * 1.1 + T.blur(crista, 0.03) * 0.5) * b
        q = np.random.default_rng(41)
        G += T.splats([(q.uniform(-1, 1), pts[0][1] - 0.03 + q.uniform(-0.04, 0.02), q.uniform(0.4, 1)) for _ in range(25)], 0.012) * b
    puxa = pulso(t, 0.2, 0.75)
    if puxa > 0:
        for k in range(8):
            x = -0.8 + 0.23 * k
            u = (t * 2 + k / 8) % 1
            G += T.tapered([(x, -0.1 - 0.4 * u + 0.15, x, -0.1 - 0.4 * u, 1.0)], 0.012) * puxa * (1 - u)
    bolha = pulso(t, 0.45, 1.0)
    if bolha > 0:
        for x in (-0.55, 0.0, 0.55):
            G += T.ring(0.17, 0.02, x, 0.45) * bolha * 1.1 + T.gauss(x - 0.05, 0.4, 0.03) * bolha * 0.5
            H += T.arc_band(0.14, 0.012, -2.5, -1.6, cx=x, cy=0.45) * bolha
    return G * env, H * env


def _tridente(T, cx, cy, s, ang):
    pts = []
    haste = [(0, 0.45 * s), (0, -0.22 * s)]
    linhas = [(*_gira([haste[0]], ang, cx, cy)[0], *_gira([haste[1]], ang, cx, cy)[0], 1.0)]
    for dx in (-0.08, 0.0, 0.08):
        a, b_ = _gira([(dx * s, -0.12 * s), (dx * s, -0.32 * s)], ang, cx, cy)
        linhas.append((*a, *b_, 1.0))
    a, b_ = _gira([(-0.08 * s, -0.12 * s), (0.08 * s, -0.12 * s)], ang, cx, cy)
    linhas.append((*a, *b_, 1.0))
    return T.lines(linhas, 0.016 * s), pts


def aquaman_preparo(T, t, rng):
    """O Preparo do Comando dos mares: o tridente erguido, a água subindo em espiral em volta dele e as silhuetas
    dos tubarões rondando embaixo (laço)."""
    G, H = vazio(T)
    tr, _ = _tridente(T, 0, 0.0, 1.3, 0.0)
    G += tr * 1.2
    H += T.gauss(0, -0.38, 0.05) * (0.6 + 0.4 * math.sin(TAU * t * 2))
    for k in range(2):
        pts = [(0.3 * math.cos(u * TAU * 2 + t * TAU + k * math.pi) * (1 - 0.3 * u), 0.5 - 0.9 * u) for u in np.linspace(0, 1, 40)]
        G += T.polyline(pts, 0.014) * 0.9
    for k in range(2):
        a = t * TAU + k * math.pi
        sx, sy = 0.55 * math.cos(a), 0.45 + 0.08 * math.sin(a)
        dirx = -math.sin(a)
        corpo = [(sx - 0.12 * dirx, sy), (sx + 0.12 * dirx, sy - 0.01), (sx + 0.02 * dirx, sy - 0.08), (sx - 0.02 * dirx, sy - 0.02)]
        G += T.polys([(corpo, 1.0)]) * 0.6
    return G, H


def comando_dos_mares(T, t, rng):
    """O comando dos mares: a onda gigante se levanta atrás dos rivais, enrola a crista com os tubarões saltando
    dentro dela e quebra por cima de todos, explodindo em espuma (Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    ergue = ease_out(rel(t, 0.0, 0.35), 2)
    quebra = ease_in(rel(t, 0.35, 0.55), 2)
    if ergue > 0 and t < 0.65:
        b = 1 - rel(t, 0.55, 0.65)
        topo = -0.2 - 0.6 * ergue + 0.5 * quebra
        pts = [(x, topo + 0.15 * (x + 1) * 0.5 * (1 - quebra) + 0.04 * math.sin(x * 7 + t * 10)) for x in np.linspace(-1, 1, 50)]
        crista = T.polyline(pts, 0.04)
        corpo = T.polys([(pts + [(1, 0.6), (-1, 0.6)], 1.0)])
        G += (corpo * 0.25 + crista * 1.1 + T.blur(crista, 0.03) * 0.5) * b
        enrola = [(0.55 + 0.15 * math.cos(a), topo + 0.12 + 0.15 * math.sin(a)) for a in np.linspace(-math.pi / 2, math.pi * 1.2, 20)]
        G += T.polyline(enrola, 0.02) * b * (1 - quebra)
        for k in range(2):
            sx = -0.4 + 0.6 * k + 0.1 * math.sin(t * 6 + k)
            sy = topo + 0.05
            tub = [(sx - 0.12, sy + 0.02), (sx + 0.1, sy - 0.02), (sx + 0.14, sy + 0.01), (sx + 0.02, sy + 0.04), (sx, sy - 0.08), (sx - 0.04, sy + 0.03)]
            G += T.polys([(tub, 1.0)]) * b * 0.8
    espuma = rel(t, 0.5, 0.9)
    if 0 < espuma < 1:
        q = np.random.default_rng(51)
        pts = []
        for _ in range(60):
            x = q.uniform(-1, 1)
            d = q.uniform(0.05, 0.5) * ease_out(espuma, 2)
            pts.append((x + q.uniform(-0.1, 0.1), 0.1 - d + 0.5 * espuma * espuma, (1 - espuma) * q.uniform(0.5, 1)))
        G += T.splats(pts, 0.022)
        H += T.gauss(0, 0.05, 0.3, 0.08) * (1 - espuma) ** 2 * 1.2
    return G * env, H * env


# =================================================================== Lanterna Verde
def _simbolo_lanterna(T, cx, cy, r):
    """O símbolo da Tropa: o círculo com as duas barras, em cima e embaixo."""
    G = T.ring(r, r * 0.18, cx, cy)
    G = G + T.lines([(cx - r * 1.1, cy - r * 0.95, cx + r * 1.1, cy - r * 0.95, 1.0), (cx - r * 1.1, cy + r * 0.95, cx + r * 1.1, cy + r * 0.95, 1.0)], r * 0.18)
    return G


def escudo_de_vontade(T, t, rng):
    """O escudo de vontade: o anel brilha, as linhas verdes do construto correm e montam a placa do escudo na frente
    do aliado, com o símbolo da Tropa no meio e a barreira por cima (Escudo, Protegido e Barreira)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    anel = pulso(t, 0.0, 0.35)
    H += T.gauss(-0.75, 0.1, 0.04) * anel * 1.8
    G += T.ring(0.05, 0.012, -0.75, 0.1) * anel
    monta = ease_out(rel(t, 0.1, 0.45), 2.5)
    if monta > 0:
        placa = [(-0.3, -0.35), (0.3, -0.35), (0.35, 0.05), (0.0, 0.42), (-0.35, 0.05)]
        borda = _contorno(placa)
        n = max(1, int(len(borda) * monta + 0.999))
        G += T.lines(borda[:n], 0.02) * 1.3
        if monta >= 1:
            P = T.polys([(placa, 1.0)])
            b = 1 - rel(t, 0.8, 0.95)
            G += P * 0.25 * b + _simbolo_lanterna(T, 0.0, -0.02, 0.1) * b
            H += P * 0.1 * b
        for k in range(4):
            u = (t * 3 + k / 4) % 1
            G += T.gauss(-0.75 + 0.75 * u, 0.1 - 0.1 * u, 0.012) * (1 - u) * monta
    barreira = pulso(t, 0.5, 1.0)
    if barreira > 0:
        G += T.arc_band(0.5, 0.02, -2.6, -0.5, cx=0, cy=0.1, crescente=True) * barreira * 1.2
    return G * env, H * env


def _punho_construto(T, cx, cy, s):
    palma = [(cx - 0.12 * s, cy - 0.1 * s), (cx + 0.08 * s, cy - 0.11 * s), (cx + 0.14 * s, cy - 0.05 * s), (cx + 0.14 * s, cy + 0.06 * s), (cx + 0.08 * s, cy + 0.11 * s), (cx - 0.12 * s, cy + 0.1 * s)]
    linhas = _contorno(palma)
    for k in range(3):
        y = cy + (-0.06 + 0.06 * k) * s
        linhas.append((cx + 0.04 * s, y, cx + 0.14 * s, y, 0.8))
    linhas.append((cx - 0.12 * s, cy - 0.05 * s, cx - 0.3 * s, cy - 0.05 * s, 0.8))
    linhas.append((cx - 0.12 * s, cy + 0.05 * s, cx - 0.3 * s, cy + 0.05 * s, 0.8))
    return T.lines(linhas, 0.012 * s), T.polys([(palma, 1.0)])


def punho_esmeralda(T, t, rng):
    """O punho esmeralda: o punho gigante de construto (só as linhas verdes acesas) voa até o rival, soca, e as
    linhas viram as barras de uma jaula que o prende (Preso; o Preparo é cancelado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    vai = ease_in(rel(t, 0.0, 0.3), 2)
    if t < 0.42:
        x = -0.8 + 0.7 * vai
        L, P = _punho_construto(T, x, 0.0, 2.0)
        b = 1 - rel(t, 0.32, 0.42)
        G += (L * 1.2 + P * 0.2) * b
        H += L * 0.4 * b
    g = pulso(t, 0.28, 0.5)
    H += T.gauss(0, 0, 0.1) * g * 1.8
    jaula = ease_out(rel(t, 0.38, 0.6), 3)
    if jaula > 0:
        barras = [(-0.22 + 0.11 * k, -0.35 * jaula, -0.22 + 0.11 * k, 0.35 * jaula, 1.0) for k in range(5)]
        barras += [(-0.25, -0.35 * jaula, 0.25, -0.35 * jaula, 1.0), (-0.25, 0.35 * jaula, 0.25, 0.35 * jaula, 1.0)]
        G += T.lines(barras, 0.016) * 1.2 * (1 - rel(t, 0.85, 0.95))
    return G * env, H * env


def lanterna_preparo(T, t, rng):
    """O Preparo do Construto adaptável: a lanterna de força (a cúpula, as barras e a chama verde dentro) e o anel
    brilhando, com as linhas de construto se formando em volta (laço)."""
    G, H = vazio(T)
    corpo = [(-0.12, -0.2), (0.12, -0.2), (0.16, 0.2), (-0.16, 0.2)]
    G += T.lines(_contorno(corpo), 0.014) + T.lines([(-0.18, -0.25, 0.18, -0.25, 1.0), (-0.2, 0.25, 0.2, 0.25, 1.0), (0, -0.25, 0, -0.33, 1.0)], 0.016)
    ch = 0.7 + 0.3 * math.sin(TAU * t * 3)
    H += T.gauss(0, 0.02, 0.06 * ch, 0.1 * ch) * 1.6
    G += T.gauss(0, 0.02, 0.05, 0.09) * ch * 0.8
    for k in range(4):
        a = TAU * t / 2 + TAU * k / 4
        x, y = 0.45 * math.cos(a), 0.4 * math.sin(a)
        u = (t * 2 + k / 4) % 1
        G += T.lines(_contorno(_gira([(-0.06, -0.06), (0.06, -0.06), (0.06, 0.06), (-0.06, 0.06)], a, x, y))[:max(1, int(4 * u + 1))], 0.008)
    return G, H


def construto_adaptavel(T, t, rng):
    """O construto adaptável: o construto verde muda de forma no ar — um martelo, depois uma lâmina, depois um
    míssil — e acerta o rival com o último (Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cx = -0.4
    S = 2.0
    def forma(pts_, extra, w=0.02):
        return T.lines(_contorno([(cx + (x - cx) * S, y * S) for x, y in pts_]) + [(cx + (a - cx) * S, b * S, cx + (c - cx) * S, d * S, e) for a, b, c, d, e in extra], w)
    f1 = pulso(t, 0.0, 0.2)
    if f1 > 0:
        G += forma([(cx - 0.15, -0.12), (cx + 0.15, -0.12), (cx + 0.15, 0.02), (cx - 0.15, 0.02)], [(cx, 0.02, cx, 0.2, 1.0)]) * f1 * 1.3
    f2 = pulso(t, 0.15, 0.35)
    if f2 > 0:
        G += forma([(cx - 0.2, 0.0), (cx + 0.15, -0.04), (cx + 0.25, 0.0), (cx + 0.15, 0.04)], [(cx - 0.2, 0.0, cx - 0.3, 0.0, 1.0), (cx - 0.2, -0.06, cx - 0.2, 0.06, 1.0)]) * f2 * 1.3
    voa = rel(t, 0.3, 0.5)
    if 0 < voa < 1:
        x = (0.0 - cx) * ease_in(voa, 1.5)
        pts_ = [(cx - 0.15, -0.04), (cx + 0.08, -0.04), (cx + 0.15, 0.0), (cx + 0.08, 0.04), (cx - 0.15, 0.04)]
        M = T.lines(_contorno([(cx + (px - cx) * S + x, py * S) for px, py in pts_]) + [(cx + x - 0.3, 0.08, cx + x - 0.4, 0.18, 1.0), (cx + x - 0.3, -0.08, cx + x - 0.4, -0.18, 1.0)], 0.02)
        G += M * 1.3
        H += T.gauss(cx + x - 0.35, 0, 0.04) * 1.5
    for k in range(3):
        H += T.gauss(cx, 0.0, 0.05) * pulso(t, 0.13 + 0.15 * k, 0.2 + 0.15 * k) * 1.4
    bum = rel(t, 0.48, 0.85)
    if 0 < bum < 1:
        e = ease_out(bum, 3)
        H += T.gauss(0, 0, 0.1 + 0.2 * e) * (1 - bum) ** 2 * 2.0
        G += T.ring(0.08 + 0.4 * e, 0.035, 0, 0) * (1 - bum) * 1.3
        G += T.lines(_contorno([(0.2 * e * math.cos(a), 0.2 * e * math.sin(a)) for a in np.linspace(0, TAU, 6, endpoint=False)]), 0.01) * (1 - bum)
    return G * env, H * env


# =================================================================== Ciborgue
def varredura_tatica(T, t, rng):
    """A varredura tática: o olho vermelho cibernético acende, dispara o leque da varredura até o rival, a grade
    passa por ele com os números correndo e a marca de alvo trava (Marcado e Enfraquecido)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    ox, oy = -0.75, -0.2
    olho = pulso(t, 0.0, 0.7)
    H += T.gauss(ox, oy, 0.03) * olho * 2.0
    G += T.ring(0.05, 0.012, ox, oy) * olho
    leque = pulso(t, 0.1, 0.55)
    if leque > 0:
        G += T.lines([(ox, oy, 0.0, -0.35, 1.0), (ox, oy, 0.0, 0.35, 1.0)], 0.008) * leque
        y = -0.35 + 0.7 * ((t * 2) % 1)
        G += T.lines([(ox, oy, 0.0, y, 1.0)], 0.014) * leque * 1.2
        H += T.lines([(-0.3, y, 0.3, y, 1.0)], 0.01) * leque
    grade = pulso(t, 0.25, 0.8)
    if grade > 0:
        linhas = [(-0.3 + 0.1 * k, -0.35, -0.3 + 0.1 * k, 0.35, 0.4) for k in range(7)] + [(-0.3, -0.35 + 0.1 * k, 0.3, -0.35 + 0.1 * k, 0.4) for k in range(8)]
        G += T.lines(linhas, 0.005) * grade
        q = np.random.default_rng(int(t * 10) % 5 + 60)
        for k in range(6):
            x, y = q.uniform(-0.3, 0.3), q.uniform(-0.3, 0.3)
            G += T.lines([(x, y, x + 0.05, y, 1.0)], 0.008) * grade
    trava = pulso(t, 0.5, 1.0)
    if trava > 0:
        G += T.ring(0.15, 0.012, 0, 0) * trava + T.lines([(0.15, 0, 0.25, 0, 1.0), (-0.15, 0, -0.25, 0, 1.0), (0, 0.15, 0, 0.25, 1.0), (0, -0.15, 0, -0.25, 1.0)], 0.012) * trava
    return G * env, H * env


def ciborgue_preparo(T, t, rng):
    """O Preparo da Adaptação de sistema: o braço se transformando em canhão (as placas abrindo em volta do cano e
    as luzes azuis acendendo) com a barra de carga enchendo (laço)."""
    G, H = vazio(T)
    abre = 0.5 + 0.5 * math.sin(TAU * t)
    braco = [(-0.45, -0.08), (0.2, -0.08), (0.2, 0.08), (-0.45, 0.08)]
    G += T.lines(_contorno(braco), 0.014) + T.ring(0.08, 0.014, 0.28, 0.0)
    for lado in (-1, 1):
        placa = _gira([(0.0, 0.0), (0.18, 0.0), (0.16, 0.05), (0.0, 0.05)], lado * (0.3 + 0.4 * abre), 0.05, lado * 0.08)
        G += T.lines(_contorno(placa), 0.01)
    for k in range(4):
        H += T.gauss(-0.35 + 0.15 * k, 0.0, 0.015) * (0.4 + 0.6 * ((t * 4 - k) % 4 < 1)) * 1.4
    barra = (t % 1)
    G += T.lines(_contorno([(-0.4, 0.25), (0.2, 0.25), (0.2, 0.3), (-0.4, 0.3)]), 0.006)
    H += T.lines([(-0.39, 0.275, -0.39 + 0.58 * barra, 0.275, 1.0)], 0.018) * 0.9
    return G, H


def adaptacao_de_sistema(T, t, rng):
    """A adaptação de sistema: o pulso azul de interferência sai do braço em anéis, o Preparo do rival trava em
    estática (as faixas que falham e pulam) e o golpe de energia acerta em cheio."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for k in range(3):
        u = rel(t, 0.05 * k, 0.3 + 0.05 * k)
        if 0 < u < 1:
            x = -0.8 + 0.8 * u
            G += T.ring(0.08 + 0.1 * u, 0.015, x, 0.0, squash=0.6) * (1 - u) * 1.2
    estatica = pulso(t, 0.25, 0.6)
    if estatica > 0:
        q = np.random.default_rng(int(t * 30) % 9 + 70)
        for k in range(10):
            y = -0.3 + 0.06 * k
            off = q.uniform(-0.08, 0.08)
            G += T.lines([(-0.25 + off, y, 0.25 + off, y, 1.0)], 0.01) * estatica * q.uniform(0.4, 1)
    raio = pulso(t, 0.45, 0.7)
    if raio > 0:
        R = T.lines([(-0.85, 0.0, 0.0, 0.0, 1.0)], 0.05)
        G += (R * 0.8 + T.blur(R, 0.03) * 0.6) * raio
        H += T.lines([(-0.85, 0.0, 0.0, 0.0, 1.0)], 0.012) * raio * 1.4 + T.gauss(0, 0, 0.1) * raio * 1.5
    bum = rel(t, 0.55, 0.9)
    if 0 < bum < 1:
        e = ease_out(bum, 3)
        G += T.ring(0.08 + 0.4 * e, 0.035, 0, 0) * (1 - bum) * 1.3
        raios = [(0.06 * math.cos(a), 0.06 * math.sin(a), (0.2 + 0.4 * e) * math.cos(a), (0.2 + 0.4 * e) * math.sin(a), 1 - bum) for a in np.linspace(0, TAU, 12, endpoint=False)]
        G += T.tapered(raios, 0.022)
    return G * env, H * env


REGISTRO = [
    ("muralha_de_galhos", muralha_de_galhos, GRANDE, "Groot · os galhos trançados, as folhas e os espinhos", False),
    ("eu_sou_groot", eu_sou_groot, GRANDE, "Groot · as raízes até o trio e os ramos com flores", False),
    ("groot_preparo", groot_preparo, MEDIA, "Groot · os braços fincados e as raízes (Preparo, laço)", True),
    ("raizes_de_captura", raizes_de_captura, GRANDE, "Groot · as raízes rompendo o chão e enlaçando", False),
    ("armadilha_explosiva", armadilha_explosiva, GRANDE, "Rocket · a minazinha piscando e a fumaça colorida", False),
    ("missil_caseiro", missil_caseiro, GRANDE, "Rocket · o míssil remendado em zigue-zague", False),
    ("rocket_preparo", rocket_preparo, MEDIA, "Rocket · o canhão montando peça por peça (Preparo, laço)", True),
    ("mare_puxante", mare_puxante, GRANDE, "Aquaman · a onda que puxa e as bolhas no trio", False),
    ("aquaman_preparo", aquaman_preparo, MEDIA, "Aquaman · o tridente, a água e os tubarões (Preparo, laço)", True),
    ("comando_dos_mares", comando_dos_mares, GRANDE, "Aquaman · a onda gigante com os tubarões quebrando", False),
    ("escudo_de_vontade", escudo_de_vontade, GRANDE, "Lanterna Verde · o construto de escudo com o símbolo", False),
    ("punho_esmeralda", punho_esmeralda, GRANDE, "Lanterna Verde · o punho de construto e a jaula", False),
    ("lanterna_preparo", lanterna_preparo, MEDIA, "Lanterna Verde · a lanterna e o anel (Preparo, laço)", True),
    ("construto_adaptavel", construto_adaptavel, GRANDE, "Lanterna Verde · o martelo, a lâmina e o míssil", False),
    ("varredura_tatica", varredura_tatica, GRANDE, "Ciborgue · o olho, a varredura e a grade", False),
    ("ciborgue_preparo", ciborgue_preparo, MEDIA, "Ciborgue · o braço virando canhão (Preparo, laço)", True),
    ("adaptacao_de_sistema", adaptacao_de_sistema, GRANDE, "Ciborgue · o pulso, a estática e o raio", False),
]
