"""Ataques básicos com animação própria, lote p (personagens novos).

Ghostface, Leatherface, Pinhead, Samara, Valak, Drácula, Xenomorfo, Predador, Darth Vader, Yoda, Luke,
Palpatine, Neo, Agente Smith e John Wick: a máscara que surge atrás e a facada, a motosserra balançando
doida, as correntes com ganchos e o cubo, a estática da TV e os cabelos, a cruz invertida e as unhas, o
bando de morcegos e a mordida, a boca interna do Alien e o ácido, a mira de três pontos e as lâminas do
pulso, o sabre vermelho, a bengala do Yoda, o sabre verde em X, o raio da Força, a chuva de código e o
soco em câmera lenta, as cópias do Smith com o glitch e os dois tiros do John Wick.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .basicos_a import _PUNHO, _move, _punho
from .basicos_k import _borda, _contorno, _estouro, _folha, _gira, _gotas
from .basicos_l import _estrelinhas
from .rodada10 import _barra_de_serra


def _morcego(cx, cy, s, bate):
    """O morcego de frente: o corpinho e as duas asas recortadas, batendo."""
    h = 0.12 * bate
    pts = [(0, -0.03), (0.06, -0.06 - h), (0.12, -0.02 - h), (0.2, -0.08 - h), (0.17, 0.02), (0.1, 0.0), (0.05, 0.05), (0, 0.03),
           (-0.05, 0.05), (-0.1, 0.0), (-0.17, 0.02), (-0.2, -0.08 - h), (-0.12, -0.02 - h), (-0.06, -0.06 - h)]
    return [(cx + x * s, cy + y * s) for x, y in pts]


def _sabre(T, x1, y1, x2, y2, larg=0.03):
    """O sabre de luz: o núcleo branco fino e o brilho largo em volta."""
    nucleo = T.lines([(x1, y1, x2, y2, 1.0)], larg * 0.45)
    brilho = T.lines([(x1, y1, x2, y2, 1.0)], larg)
    return T.blur(brilho, 0.02) * 1.1 + brilho * 0.6, nucleo


# ================================================================== Ghostface
def golpe_por_tras(T, t, rng):
    """O golpe por trás do Ghostface: a máscara branca comprida surge atrás do rival (os olhos e a boca em grito,
    caídos), e a faca entra pelas costas com o brilho; a máscara some."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    surge = back(rel(t, 0.0, 0.3), 1.2) * (1 - rel(t, 0.6, 0.85))
    if surge > 0:
        cx, cy, s = 0.3, -0.15, 1.5 * surge
        rosto = [(cx + 0.16 * s * math.cos(a), cy + 0.3 * s * math.sin(a) * (1.15 if math.sin(a) > 0 else 1)) for a in np.linspace(0, TAU, 28, endpoint=False)]
        segs = _contorno(rosto)
        for lado in (-1, 1):
            olho = [(cx + lado * 0.07 * s + 0.04 * s * math.cos(a), cy - 0.06 * s + 0.07 * s * math.sin(a)) for a in np.linspace(0, TAU, 12, endpoint=False)]
            segs += _contorno(_gira([(x - cx, y - cy) for x, y in olho], -lado * 0.25, cx, cy))
        boca = [(cx + 0.035 * s * math.cos(a), cy + 0.15 * s + 0.08 * s * math.sin(a)) for a in np.linspace(0, TAU, 14, endpoint=False)]
        segs += _contorno(boca)
        M = T.lines(segs, 0.018)
        G += M * 1.3 + T.blur(T.polys([(rosto, 1.0)]), 0.03) * 0.25 * surge
    facada = ease_in(rel(t, 0.3, 0.45), 2)
    if facada > 0 and t < 0.7:
        tip = (0.45 - 0.4 * facada, 0.05)
        L = T.polys([(lamina(tip[0] + 0.4, 0.05, tip[0], tip[1], 0.04), 1.0)])
        G += (L * 1.1 + _borda(T, L, 0.005)) * (1 - rel(t, 0.55, 0.7))
        G += T.lines([(tip[0] + 0.4, 0.05, tip[0] + 0.55, 0.05, 1.0)], 0.035) * (1 - rel(t, 0.55, 0.7))
    g, h = _estouro(T, t, 0.44, 0.75, 0.05, 0.05, 0.28, 8, 3)
    G += g
    H += h
    G += _gotas(T, t, 0.45, 0.5, 0.05, 0.05, 10, 0.35, 5, -2.8, -0.3, 0.015, 0.4)
    return G * env, H * env


# ================================================================== Leatherface
def serra_eletrica(T, t, rng):
    """A serra do Leatherface: a motosserra balança doida de um lado para o outro (duas varridas largas, os
    dentes correndo), a fumaça do escapamento sobe e as lascas voam do corte."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    for k, (t0, a0, a1) in enumerate(((0.0, -2.6, -0.5), (0.3, 0.6, 2.7))):
        u = ease_out(rel(t, t0, t0 + 0.25), 1.8)
        if u <= 0 or t > t0 + 0.35:
            continue
        a = a0 + (a1 - a0) * u
        px, py = -0.35 if k == 0 else 0.35, 0.3
        x2, y2 = px + 0.75 * math.cos(a), py + 0.75 * math.sin(a)
        some = 1 - rel(t, t0 + 0.25, t0 + 0.35)
        B = _barra_de_serra(T, px, py, x2, y2, 0.06, t * 25)
        G += (B * 1.2 + T.blur(B, 0.015) * 0.4) * some
        G += T.arc_band(0.75, 0.05, a0, a, cx=px, cy=py, taper=0.7) * 0.5 * some
    fumaca = rel(t, 0.0, 1.0)
    q = np.random.default_rng(3)
    pts = [(-0.7 + 0.1 * math.sin(t * 10 + k), 0.5 - 0.7 * ((fumaca + k / 8) % 1), 0.5 * (1 - ((fumaca + k / 8) % 1))) for k in range(8)]
    G += T.splats(pts, 0.06) * 0.6
    for t0 in (0.15, 0.45):
        g, h = _estouro(T, t, t0, t0 + 0.3, 0, 0, 0.3, 9, int(t0 * 100))
        G += g * 0.8
        H += h * 0.7
        G += _gotas(T, t, t0, 0.45, 0, 0, 12, 0.5, int(t0 * 100) + 1, 0, TAU, 0.014, 0.4)
    return G * env, H * env


# ================================================================== Pinhead
def ganchos_de_corrente(T, t, rng):
    """Os ganchos do Pinhead: o cubo da Configuração do Lamento brilha no alto, e as correntes saem do escuro de
    vários lados com os ganchos na ponta, fisgam o rival e esticam."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    cubo = pulso(t, 0.0, 0.7)
    if cubo > 0:
        cx, cy, s = 0.0, -0.7, 0.1
        frente = [(cx - s, cy - s), (cx + s, cy - s), (cx + s, cy + s), (cx - s, cy + s)]
        tras = [(x + 0.05, y - 0.05) for x, y in frente]
        segs = _contorno(frente) + _contorno(tras) + [(frente[i][0], frente[i][1], tras[i][0], tras[i][1], 1.0) for i in range(4)]
        segs += [(cx - s, cy, cx + s, cy, 0.6), (cx, cy - s, cx, cy + s, 0.6)]
        G += T.lines(segs, 0.01) * cubo * 1.3
        H += T.gauss(cx, cy, 0.04) * cubo * 1.2
    for k, (ox, oy) in enumerate(((-1.0, -0.6), (1.0, -0.5), (-0.9, 0.7), (0.95, 0.65), (0.0, -1.0))):
        t0 = 0.15 + 0.04 * k
        vai = ease_out(rel(t, t0, t0 + 0.18), 2)
        if vai <= 0:
            continue
        estica = 1 + 0.08 * pulso(t, 0.4, 0.8)
        tx, ty = ox + (0.0 - ox) * vai * 0.85 / estica, oy + (0.0 - oy) * vai * 0.85 / estica
        pts = [(ox + (tx - ox) * u, oy + (ty - oy) * u + 0.03 * math.sin(u * 30)) for u in np.linspace(0, 1, 18)]
        G += T.polyline(pts, 0.012) * 1.1 * (1 - rel(t, 0.8, 0.95))
        ang = math.atan2(ty - oy, tx - ox)
        gancho = [_gira([(0, 0), (0.06, 0.0)], ang, tx, ty), _gira([(0.06, 0.0), (0.05, 0.05), (0.02, 0.05)], ang, tx, ty)]
        for g in gancho:
            G += T.polyline(g, 0.014) * 1.3 * (1 - rel(t, 0.8, 0.95))
    g, h = _estouro(T, t, 0.3, 0.6, 0, 0, 0.22, 7, 9, 0.014)
    G += g * 0.7
    H += h * 0.7
    G += _gotas(T, t, 0.35, 0.5, 0, 0, 10, 0.35, 11, 0, TAU, 0.013, 0.4)
    return G * env, H * env


# ================================================================== Samara
def toque_de_samara(T, t, rng):
    """O toque da Samara: a tela de TV com chuvisco (o quadro com as linhas e o ruído), os cabelos molhados escorrem
    na frente, e a mão sai da estática e toca o rival — o anel do poço fecha em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    tv = pulso(t, 0.0, 0.7)
    if tv > 0:
        q = np.random.default_rng(int(t * 60) % 13)
        ruido = (q.random((T.H, T.W)) > 0.6).astype(np.float32)
        quadro = ((np.abs(T.U + 0.45) < 0.35) & (np.abs(T.V) < 0.3)).astype(np.float32)
        linhas = 0.5 + 0.5 * np.sin(T.V * 120 + t * 40)
        G += ruido * quadro * linhas * tv * 0.35
        G += T.lines(_contorno([(-0.8, -0.3), (-0.1, -0.3), (-0.1, 0.3), (-0.8, 0.3)]), 0.012) * tv
        for k in range(6):
            x = -0.6 + 0.08 * k
            pts = [(x + 0.02 * math.sin(u * 12 + k), -0.3 + 0.55 * u * ease_out(rel(t, 0.05, 0.4), 2)) for u in np.linspace(0, 1, 14)]
            G += T.polyline(pts, 0.008) * tv * 0.9
    mao = ease_out(rel(t, 0.3, 0.5), 2)
    if mao > 0 and t < 0.8:
        px = -0.3 + 0.3 * mao
        segs = [(px - 0.3, 0.02, px, 0.0, 1.0)]
        for k in range(4):
            a = -0.4 + 0.27 * k
            segs.append((px, 0.0, px + 0.14 * math.cos(a), 0.14 * math.sin(a), 1.0))
        G += T.lines(segs, 0.016) * 1.1 * (1 - rel(t, 0.65, 0.8))
    anel = rel(t, 0.45, 1.0)
    if 0 < anel < 1:
        r = 0.5 - 0.15 * ease_out(anel, 2)
        G += T.ring(r, 0.03, 0.1, 0.0) * math.sin(math.pi * anel) * 1.2
        G += T.ring(r * 0.88, 0.012, 0.1, 0.0) * math.sin(math.pi * anel) * 0.8
    return G * env, H * env


# ================================================================== Valak
def garra_de_valak(T, t, rng):
    """A garra da Valak: a cruz invertida aparece no escuro e gira de ponta-cabeça, os olhos amarelos acendem, e as
    unhas compridas rasgam o rival em três riscos."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    cruz = pulso(t, 0.0, 0.55)
    if cruz > 0:
        ang = math.pi * ease_out(rel(t, 0.0, 0.3), 2)
        segs = [_gira([(0, -0.25), (0, 0.25)], ang, 0.0, -0.35), _gira([(-0.12, 0.08), (0.12, 0.08)], ang, 0.0, -0.35)]
        for sgm in segs:
            G += T.polyline(sgm, 0.03) * cruz * 1.2
    olhos = pulso(t, 0.15, 0.6)
    H += T.splats([(-0.08, -0.05, 1.0), (0.08, -0.05, 1.0)], 0.02) * olhos * 1.6
    for k in range(3):
        t0 = 0.32 + 0.03 * k
        p = ease_out(rel(t, t0, t0 + 0.12), 3)
        ini = rel(t, t0 + 0.2, t0 + 0.5)
        if p > 0 and ini < 1:
            dx = (k - 1) * 0.14
            L = T.polys([(lamina(dx + 0.2, -0.45, dx - 0.2, 0.45, 0.03, prog=p, inicio=ini), 1.0)])
            G += L * 1.4
            H += L * 0.5
    return G * env, H * env


# ================================================================== Drácula
def mordida_de_dracula(T, t, rng):
    """A mordida do Drácula: o bando de morcegos sai voando da capa (batendo as asas) e envolve o rival, e no meio
    deles as presas cravam; o sangue escorre."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    q = np.random.default_rng(15)
    shapes = []
    for k in range(9):
        t0 = 0.02 * k
        u = rel(t, t0, t0 + 0.45)
        if u <= 0 or u >= 1:
            continue
        a0 = q.uniform(0, TAU)
        orbita = ease_out(u, 2)
        x = -0.85 * (1 - orbita) + 0.35 * orbita * math.cos(a0 + u * 6)
        y = q.uniform(-0.3, 0.3) * (1 - orbita) + 0.25 * orbita * math.sin(a0 + u * 6)
        bate = 0.5 + 0.5 * math.sin(t * 60 + k)
        shapes.append((_morcego(x, y, 0.7 + 0.3 * q.uniform(), bate), 1 - rel(u, 0.75, 1)))
    if shapes:
        M = T.polys(shapes)
        G += M * 0.6 + _borda(T, M, 0.005) * 1.1
    presas = pulso(t, 0.35, 0.75)
    if presas > 0:
        fecha = ease_in(rel(t, 0.35, 0.45), 2)
        sh = []
        for lado in (-1, 1):
            x = 0.08 * lado
            sh.append(([(x - 0.035, -0.12 - 0.12 * (1 - fecha)), (x + 0.035, -0.12 - 0.12 * (1 - fecha)), (x, 0.02 - 0.12 * (1 - fecha))], 1.0))
        G += T.polys(sh) * presas * 1.3
    g, h = _estouro(T, t, 0.42, 0.7, 0, 0, 0.22, 7, 17, 0.014)
    G += g * 0.8
    H += h * 0.7
    G += _gotas(T, t, 0.45, 0.5, 0, 0.0, 10, 0.25, 19, 1.2, 1.9, 0.014, 0.6)
    return G * env, H * env


# ================================================================== Xenomorfo
def garra_xenomorfa(T, t, rng):
    """O ataque do Xenomorfo: a cabeça comprida avança, a boca se abre e a boca interna dispara com os dentinhos
    cravando no rival; o ácido espirra e chia."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vem = ease_out(rel(t, 0.0, 0.25), 2)
    if t < 0.6:
        some = 1 - rel(t, 0.45, 0.6)
        hx = -0.75 + 0.25 * vem
        cab = [(hx - 0.45, -0.12), (hx - 0.1, -0.12), (hx + 0.12, -0.04), (hx + 0.14, 0.02), (hx + 0.05, 0.06), (hx - 0.2, 0.08), (hx - 0.45, 0.04)]
        G += T.lines(_contorno(cab), 0.014) * 1.2 * some
        dispara = ease_out(rel(t, 0.25, 0.38), 3) * (1 - ease_in(rel(t, 0.45, 0.6), 2))
        if dispara > 0:
            x2 = hx + 0.14 + (0.0 - hx - 0.14) * dispara
            G += T.lines([(hx + 0.1, 0.01, x2, 0.01, 1.0)], 0.03) * 1.1
            dentes = [([(x2 - 0.02, -0.04), (x2 + 0.03, -0.01), (x2 - 0.02, -0.0)], 1.0), ([(x2 - 0.02, 0.06), (x2 + 0.03, 0.03), (x2 - 0.02, 0.02)], 1.0)]
            G += T.polys(dentes) * 1.3
    g, h = _estouro(T, t, 0.36, 0.65, 0.0, 0.0, 0.25, 8, 21)
    G += g
    H += h
    acido = rel(t, 0.38, 1.0)
    if 0 < acido < 1:
        G += _gotas(T, t, 0.38, 0.5, 0, 0, 14, 0.45, 23, -2.9, -0.2, 0.016, 0.6) * 1.2
        q = np.random.default_rng(int(t * 20) % 5)
        fum = [(q.uniform(-0.3, 0.3), 0.3 - 0.4 * acido + q.uniform(-0.05, 0.05), (1 - acido) * 0.5) for _ in range(8)]
        G += T.splats(fum, 0.04) * 0.6
    return G * env, H * env


# ================================================================== Predador
def laminas_de_pulso(T, t, rng):
    """O ataque do Predador: os três pontinhos do laser da mira formam o triângulo no rival, a camuflagem tremula
    (o contorno ondulado que aparece), e as duas lâminas do pulso cortam em X."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    mira = pulso(t, 0.0, 0.45)
    if mira > 0:
        junta = ease_out(rel(t, 0.0, 0.25), 2)
        pts = [(0.25 * (1 - junta) * math.cos(a) + 0.05 * math.cos(a), 0.25 * (1 - junta) * math.sin(a) + 0.05 * math.sin(a), 1.0) for a in (-math.pi / 2, math.pi / 6, 5 * math.pi / 6)]
        H += T.splats(pts, 0.014) * mira * 1.8
        G += T.splats(pts, 0.03) * mira * 0.8
    camuf = pulso(t, 0.15, 0.55)
    if camuf > 0:
        A = T.ring(0.35, 0.012, -0.55, 0.0, squash=0.5)
        du = 0.03 * np.sin(T.V * 40 + t * 50)
        G += T.warp(A, du, du * 0) * camuf * 0.8
    for k, (ang, t0) in enumerate(((0.7, 0.35), (-0.7, 0.4))):
        p = ease_out(rel(t, t0, t0 + 0.1), 3)
        ini = rel(t, t0 + 0.15, t0 + 0.45)
        if p > 0 and ini < 1:
            ux, uy = math.cos(ang), math.sin(ang)
            for dd in (-0.04, 0.04):
                nx, ny = -uy * dd, ux * dd
                L = T.polys([(lamina(-0.5 * ux + nx, -0.5 * uy + ny, 0.5 * ux + nx, 0.5 * uy + ny, 0.02, prog=p, inicio=ini), 1.0)])
                G += L * 1.4
                H += L * 0.5
    g, h = _estouro(T, t, 0.38, 0.65, 0, 0, 0.25, 8, 25, 0.015)
    G += g * 0.8
    H += h * 0.8
    return G * env, H * env


# ================================================================== Darth Vader
def sabre_vermelho(T, t, rng):
    """O sabre do Vader: o sabre vermelho acende (a lâmina saindo do cabo) e desce num golpe pesado e lento em arco,
    deixando o rastro de luz; o rival leva o corte com o chiado de faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    acende = ease_out(rel(t, 0.0, 0.15), 2)
    gira = ease_in(rel(t, 0.15, 0.45), 1.6)
    if acende > 0 and t < 0.65:
        some = 1 - rel(t, 0.5, 0.65)
        ang = -2.2 + 2.3 * gira
        px, py = -0.4, 0.35
        comp = 0.85 * acende
        x2, y2 = px + comp * math.cos(ang), py + comp * math.sin(ang)
        g_, n_ = _sabre(T, px, py, x2, y2, 0.05)
        G += g_ * some
        H += n_ * 1.4 * some
        G += T.lines([(px, py, px - 0.12 * math.cos(ang), py - 0.12 * math.sin(ang), 1.0)], 0.04) * 0.8 * some
        if gira > 0:
            G += T.arc_band(0.6, 0.12, -2.2, ang, cx=px, cy=py, taper=0.5) * 0.5 * some
    g, h = _estouro(T, t, 0.4, 0.7, 0.05, -0.05, 0.3, 10, 27, 0.014)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Yoda
def bengala_de_yoda(T, t, rng):
    """A bengala do Yoda: o mestre pulinha dando cambalhotas (os arcos rápidos), cutuca o rival com a bengala em dois
    toques secos, e um empurrãozinho da Força ondula."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    for k in range(3):
        u = rel(t, 0.06 * k, 0.06 * k + 0.2)
        if 0 < u < 1:
            cx = -0.7 + 0.25 * k
            G += T.arc_band(0.2, 0.04, -math.pi, -math.pi + TAU * 0.9 * u, cx=cx, cy=0.15 - 0.25 * math.sin(math.pi * u), taper=0.7) * (1 - u * 0.5) * 1.3
    for k, t0 in enumerate((0.25, 0.38)):
        u = rel(t, t0, t0 + 0.12)
        if 0 < u < 1:
            tip = (-0.05 + 0.08 * math.sin(math.pi * u), 0.05 * k)
            G += T.lines([(tip[0] - 0.55, tip[1] + 0.25, tip[0], tip[1], 1.0)], 0.03) * 1.3
        b = rel(t, t0 + 0.06, t0 + 0.25)
        if 0 < b < 1:
            H += T.flare(0.0, 0.05 * k, 0.35 * (1 - b) + 0.01, k, 0.012) * (1 - b) * 1.4
            G += T.ring(0.04 + 0.2 * b, 0.018, 0.0, 0.05 * k) * (1 - b) * 1.2
    forca = rel(t, 0.45, 0.85)
    if 0 < forca < 1:
        A = T.arc_band(0.15 + 0.5 * forca, 0.05, -1.0, 1.0, cx=-0.25, cy=0.05, taper=0.0)
        G += A * (1 - forca) * 1.4 + T.blur(A, 0.02) * (1 - forca) * 0.5
    return G * env, H * env


# ================================================================== Luke
def sabre_verde(T, t, rng):
    """O sabre do Luke: o sabre verde acende e dá dois cortes rápidos em X, um de cada lado, com o rastro de luz."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    for k, (a0, a1, px, t0) in enumerate(((-2.4, -0.4, -0.35, 0.05), (2.4, 0.4, -0.35, 0.28))):
        u = ease_out(rel(t, t0, t0 + 0.2), 2.4)
        if u <= 0 or t > t0 + 0.35:
            continue
        some = 1 - rel(t, t0 + 0.2, t0 + 0.35)
        ang = a0 + (a1 - a0) * u
        py = 0.0
        x2, y2 = px + 0.7 * math.cos(ang), py + 0.7 * math.sin(ang)
        g_, n_ = _sabre(T, px, py, x2, y2, 0.04)
        G += g_ * some
        H += n_ * 1.4 * some
        G += T.arc_band(0.55, 0.09, a0, ang, cx=px, cy=py, taper=0.5) * 0.45 * some
        g, h = _estouro(T, t, t0 + 0.15, t0 + 0.4, 0.15, 0.0, 0.25, 8, 29 + k, 0.013)
        G += g * 0.8
        H += h * 0.8
    return G * env, H * env


# ================================================================== Palpatine
def raio_da_forca(T, t, rng):
    """A faísca da Força do Palpatine: dos dedos saem vários raios ramificados e contínuos, tremendo sem parar até o
    rival, que fica envolto nos estalos."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    ativo = pulso(t, 0.05, 0.75)
    if ativo > 0:
        q = np.random.default_rng(int(t * 45) % 17)
        vai = ease_out(rel(t, 0.05, 0.2), 2)
        for k in range(4):
            oy = -0.08 + 0.05 * k
            xa, ya = -0.85, oy
            xb, yb = -0.85 + 0.85 * vai, 0.08 * (k - 1.5)
            R = T.polyline(jagged(q, xa, ya, xb, yb, 5, 0.16), 0.013)
            G += R * ativo * 1.3 + T.blur(R, 0.015) * ativo * 0.5
            H += R * ativo * 0.6
            if k % 2 == 0:
                mx, my = (xa + xb) / 2, (ya + yb) / 2
                G += T.polyline(jagged(q, mx, my, mx + 0.18, my + 0.18 * (1 if k else -1), 3, 0.3), 0.009) * ativo
        H += T.gauss(-0.85, 0.0, 0.04) * ativo * 1.3
    envolve = pulso(t, 0.2, 0.85)
    if envolve > 0:
        q = np.random.default_rng(int(t * 40) % 7 + 30)
        for k in range(4):
            a = TAU * k / 4 + t * 8
            G += T.polyline(jagged(q, 0.15 * math.cos(a), 0.15 * math.sin(a), 0.35 * math.cos(a + 0.6), 0.35 * math.sin(a + 0.6), 3, 0.3), 0.011) * envolve * 1.2
        H += T.gauss(0, 0, 0.1) * envolve * 0.8
    return G * env, H * env


# ================================================================== Neo
def soco_de_neo(T, t, rng):
    """O soco do Neo: a chuva de código verde cai em colunas, o tempo desacelera (os anéis de distorção que se abrem
    devagar em volta do punho) e o soco acerta com a onda de choque."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    chuva = pulso(t, 0.0, 0.85)
    if chuva > 0:
        q = np.random.default_rng(37)
        pts = []
        for c in range(14):
            x = -0.9 + 1.8 * c / 13 + q.uniform(-0.03, 0.03)
            vel = q.uniform(0.6, 1.2)
            y0 = q.uniform(0, 1)
            for j in range(6):
                y = -1.0 + 2.0 * ((t * vel + y0 + j * 0.05) % 1)
                pts.append((x, y, (1 - j / 6) * 0.7))
        G += T.splats(pts, 0.009) * chuva * 1.2
    vai = ease_in(rel(t, 0.1, 0.45), 1.3)
    if t < 0.6:
        x = -0.75 + 0.7 * vai
        P, nos = _punho(T, x, 0.0, 1.5)
        G += P * 0.6 + _borda(T, P, 0.006) * 1.0
        for k in range(3):
            u = (t * 1.2 + k / 3) % 1
            G += T.ring(0.08 + 0.25 * u, 0.008, x - 0.05, 0.0, squash=1.0 / 0.6) * (1 - u) * 0.9
    g, h = _estouro(T, t, 0.45, 0.8, 0.05, 0, 0.4, 10, 39)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Agente Smith
def soco_do_agente(T, t, rng):
    """O soco do Agente Smith: as cópias dele aparecem lado a lado (os punhos repetidos), o glitch digital pisca em
    quadradinhos, e todas socam juntas o rival."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vai = ease_in(rel(t, 0.1, 0.35), 2)
    if t < 0.55:
        some = 1 - rel(t, 0.42, 0.55)
        for k, dy in enumerate((-0.3, 0.0, 0.3)):
            x = -0.8 + 0.72 * vai - 0.05 * abs(dy)
            P, nos = _punho(T, x, dy * (1 - 0.6 * vai), 1.3)
            G += (P * 0.5 + _borda(T, P, 0.006) * 1.0) * some * (1.0 if k == 1 else 0.6)
    glitch = pulso(t, 0.0, 0.7)
    if glitch > 0:
        q = np.random.default_rng(int(t * 30) % 11)
        shapes = []
        for _ in range(10):
            cx, cy = q.uniform(-0.8, 0.3), q.uniform(-0.5, 0.5)
            w, h = q.uniform(0.03, 0.12), q.uniform(0.01, 0.04)
            shapes.append(([(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy + h), (cx - w, cy + h)], q.uniform(0.3, 1)))
        G += T.polys(shapes) * glitch * 0.7
    g, h = _estouro(T, t, 0.35, 0.65, 0.05, 0, 0.38, 10, 41)
    G += g
    H += h
    return G * env, H * env


# ================================================================== John Wick
def tiro_de_john_wick(T, t, rng):
    """Os tiros do John Wick: o "double tap" — dois disparos colados (dois clarões no cano, dois traços) no peito,
    e o terceiro, de precisão; os cartuchos saltam brilhando."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    cano = (-0.85, -0.05)
    for k, (t0, alvo) in enumerate(((0.05, (0.0, 0.08)), (0.12, (0.03, 0.04)), (0.35, (0.0, -0.22)))):
        c = pulso(t, t0, t0 + 0.08)
        H += T.flare(cano[0], cano[1], 0.35 * c + 0.01, 0, 0.014) * c * 1.5 + T.gauss(cano[0], cano[1], 0.05) * c * 1.2
        v = rel(t, t0, t0 + 0.06)
        if 0 < v and t < t0 + 0.2:
            x = cano[0] + (alvo[0] - cano[0]) * min(1, v)
            y = cano[1] + (alvo[1] - cano[1]) * min(1, v)
            G += T.tapered([(cano[0], cano[1], x, y, 1.0)], 0.022) * (1 - rel(t, t0 + 0.06, t0 + 0.2)) * 1.5
        b = rel(t, t0 + 0.05, t0 + 0.3)
        if 0 < b < 1:
            H += T.gauss(alvo[0], alvo[1], 0.04) * (1 - b) ** 2 * 2.0 + T.flare(alvo[0], alvo[1], 0.25 * (1 - b) + 0.01, 0.3, 0.01) * (1 - b)
            G += T.ring(0.03 + 0.16 * b, 0.016, alvo[0], alvo[1]) * (1 - b) * 1.3
        cart = rel(t, t0 + 0.02, t0 + 0.5)
        if 0 < cart < 1:
            cx = cano[0] + 0.05 + 0.15 * cart
            cy = cano[1] - 0.3 * math.sin(math.pi * cart) + 0.3 * cart
            G += T.polys([(_gira([(-0.015, -0.007), (0.015, -0.007), (0.015, 0.007), (-0.015, 0.007)], cart * 12, cx, cy), 1.0)]) * (1 - cart) * 1.2
    g, h = _estouro(T, t, 0.4, 0.7, 0.0, -0.1, 0.25, 8, 43, 0.014)
    G += g * 0.7
    H += h * 0.6
    return G * env, H * env


REGISTRO = [
    ("golpe_por_tras", golpe_por_tras, GRANDE, "Básico do Ghostface: a máscara atrás e a facada", False),
    ("serra_eletrica", serra_eletrica, GRANDE, "Básico do Leatherface: a motosserra balançando", False),
    ("ganchos_de_corrente", ganchos_de_corrente, GRANDE, "Básico do Pinhead: o cubo e as correntes com ganchos", False),
    ("toque_de_samara", toque_de_samara, GRANDE, "Básico da Samara: a estática, os cabelos e a mão", False),
    ("garra_de_valak", garra_de_valak, GRANDE, "Básico da Valak: a cruz invertida e as unhas", False),
    ("mordida_de_dracula", mordida_de_dracula, GRANDE, "Básico do Drácula: os morcegos e as presas", False),
    ("garra_xenomorfa", garra_xenomorfa, GRANDE, "Básico do Xenomorfo: a boca interna e o ácido", False),
    ("laminas_de_pulso", laminas_de_pulso, GRANDE, "Básico do Predador: a mira de três pontos e as lâminas", False),
    ("sabre_vermelho", sabre_vermelho, GRANDE, "Básico do Vader: o sabre vermelho descendo", False),
    ("bengala_de_yoda", bengala_de_yoda, GRANDE, "Básico do Yoda: as cambalhotas e a bengala", False),
    ("sabre_verde", sabre_verde, GRANDE, "Básico do Luke: o sabre verde em X", False),
    ("raio_da_forca", raio_da_forca, GRANDE, "Básico do Palpatine: o raio da Força", False),
    ("soco_de_neo", soco_de_neo, GRANDE, "Básico do Neo: o código e o soco em câmera lenta", False),
    ("soco_do_agente", soco_do_agente, GRANDE, "Básico do Smith: as cópias e o glitch", False),
    ("tiro_de_john_wick", tiro_de_john_wick, GRANDE, "Básico do John Wick: o double tap e o terceiro", False),
]
