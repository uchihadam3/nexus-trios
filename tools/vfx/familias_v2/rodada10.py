"""Rodada 10 das habilidades próprias: Denji, Power, Makima (Chainsaw Man), Frieren e Anya (Spy x Family).

Denji
- puxar_a_corda: a cordinha do peito é puxada (o fio e a argola esticando), o motor pega (a
  fumaça saindo em baforadas) e a lâmina da motosserra salta girando com os dentes.
- frenesi_de_sangue: três barras de motosserra (com os dentes correndo na borda) cortam em
  sequência, e o sangue espirra em arco a cada uma.

Power
- lanca_de_sangue: as gotas de sangue se juntam no ar numa lança comprida e pontuda, que dispara e
  crava, espirrando.
- power_preparo: o Preparo do Prêmio — o sangue girando em volta e os dois chifres se formando no
  alto (laço).
- premio_de_sangue: a coroa de espinhos de sangue explode do chão em volta do rival, e as gotas
  caem; o rival gira tonto (a espiral).

Makima
- olhar_de_comando: o olho da Makima se abre grande, com os anéis concêntricos na íris, e a ordem
  sai em anéis até o rival.
- corrente_de_obediencia: a guia fina chega até o rival e a coleira (o anel com as tachas) se fecha
  no pescoço; o "X" do silêncio acende.
- controle_total: o "bang" — o dedo aponta (o clarão na ponta), e a pressão invisível esmaga o
  rival de cima: as linhas descem e apertam, a cratera abre.

Frieren
- analise_de_mana: o círculo mágico com dois anéis de runas girando ao contrário, o feixe que
  varre o rival, e a chama de mana dele aparece; os buffs saem voando em faíscas.
- frieren_preparo: o Preparo da Magia — três círculos mágicos empilhados girando (laço).
- magia_preparada: os círculos mágicos se abrem no ar em volta (um depois do outro) e disparam
  juntos feixes finos que convergem no rival.

Anya
- leitura_mental: as ondas da telepatia saem de cima, o balão de pensamento com o "?" aparece
  sobre o rival, e as estrelinhas giram (Confuso).
- alerta_urgente: os "!" pulam em volta do aliado e uma bolha-escudo redonda com estrelinhas se
  fecha nele.
- plano_secreto: o plano se desenha em linhas tracejadas (as setas e os círculos), e o carimbo
  de "X" bate no meio.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _respingos(T, t, seed, n, t0, cx, cy, alcance=0.5, ang0=0.0, ang1=TAU, tam=0.014):
    sub = np.random.default_rng(seed)
    pts = []
    u = rel(t, t0, t0 + 0.5)
    if u <= 0 or u >= 1:
        return T.zero()
    for _ in range(n):
        a = sub.uniform(ang0, ang1)
        d = sub.uniform(0.3, 1.0) * alcance * ease_out(u, 2)
        pts.append((cx + d * math.cos(a), cy + d * math.sin(a) + 0.3 * u * u, (1 - u) * sub.uniform(0.5, 1)))
    return T.splats(pts, tam)


def _barra_de_serra(T, x1, y1, x2, y2, larg, fase, prog=1.0):
    """A barra da motosserra: o retângulo comprido com os dentes triangulares correndo pela borda."""
    dx, dy = x2 - x1, y2 - y1
    comp = math.hypot(dx, dy) or 1
    ux, uy = dx / comp, dy / comp
    nx, ny = -uy, ux
    L = comp * prog
    corpo = [(x1 + nx * larg, y1 + ny * larg), (x1 + ux * L + nx * larg, y1 + uy * L + ny * larg),
             (x1 + ux * L - nx * larg, y1 + uy * L - ny * larg), (x1 - nx * larg, y1 - ny * larg)]
    dentes = []
    passo = 0.06
    k0 = (fase % 1) * passo
    d = k0
    while d < L:
        for lado in (1, -1):
            bx, by = x1 + ux * d + nx * larg * lado, y1 + uy * d + ny * larg * lado
            dentes.append(([(bx, by), (bx + ux * passo * 0.6, by + uy * passo * 0.6), (bx + nx * larg * 0.7 * lado + ux * passo * 0.1, by + ny * larg * 0.7 * lado + uy * passo * 0.1)], 1.0))
        d += passo
    return T.polys([(corpo, 0.6)] + dentes)


# =================================================================== Denji
def puxar_a_corda(T, t, rng):
    """A cordinha do peito é puxada para fora (o fio esticando com a argola na ponta), o motor pega (as
    baforadas de fumaça) e a lâmina da motosserra salta da cabeça, girando, com os dentes."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    puxa = ease_out(rel(t, 0.0, 0.25), 2) * (1 - 0.6 * ease_in(rel(t, 0.25, 0.35), 2))
    ax, ay = -0.05 + 0.8 * puxa, 0.2 + 0.2 * puxa
    G += T.polyline([(-0.05, 0.2), ((ax - 0.05) / 2, 0.26 + 0.06 * math.sin(t * 40)), (ax, ay)], 0.022) * 1.3 * (1 - rel(t, 0.35, 0.45))
    G += T.ring(0.07, 0.02, ax + 0.05, ay) * 1.3 * (1 - rel(t, 0.35, 0.45))
    sub = np.random.default_rng(5)
    fumaca = []
    for k in range(4):
        t0 = 0.28 + 0.07 * k
        f = rel(t, t0, t0 + 0.45)
        if 0 < f < 1:
            for _ in range(4):
                fumaca.append((0.3 + 0.4 * f + sub.uniform(-0.05, 0.05), -0.05 - 0.25 * f + sub.uniform(-0.05, 0.05), (1 - f) * 0.7))
    G += T.splats(fumaca, 0.06) * 0.7
    salta = back(rel(t, 0.3, 0.5), 1.4)
    if salta > 0:
        gira = t * 30
        B = _barra_de_serra(T, -0.15, 0.1, -0.15 + 0.1 * salta, 0.1 - 0.95 * salta, 0.09, gira)
        G += B * 1.1 + T.blur(B, 0.015) * 0.4
        H += np.clip(B - T.blur(B, 0.004), 0, 1) * 0.5
        G += T.gauss(-0.15, 0.1, 0.12) * pulso(t, 0.3, 0.55) * 1.4
    return G * env, H * env


def frenesi_de_sangue(T, t, rng):
    """O frenesi: três barras de motosserra cortam em sequência, em ângulos diferentes (os dentes
    correndo na borda), e a cada corte o sangue espirra em arco."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cortes = ((-0.8, -0.55, 0.75, 0.4, 0.0), (0.8, -0.6, -0.7, 0.5, 0.18), (-0.85, 0.15, 0.85, -0.1, 0.36))
    for k, (x1, y1, x2, y2, t0) in enumerate(cortes):
        p = ease_out(rel(t, t0, t0 + 0.14), 2)
        some = 1 - rel(t, t0 + 0.18, t0 + 0.35)
        if p <= 0 or some <= 0:
            continue
        B = _barra_de_serra(T, x1, y1, x2, y2, 0.05, t * 25 + k, p)
        G += (B * 1.2 + T.blur(B, 0.02) * 0.5) * some
        H += B * 0.4 * some
        ang = math.atan2(y2 - y1, x2 - x1)
        G += _respingos(T, t, 40 + k, 18, t0 + 0.08, (x1 + x2) / 2, (y1 + y2) / 2, 0.5, ang - 1.9, ang - 1.2) * 1.2
    return G * env, H * env


# =================================================================== Power
def lanca_de_sangue(T, t, rng):
    """As gotas de sangue se juntam no ar (vêm de volta para uma linha), formam a lança comprida de
    ponta afiada, que dispara para o rival e crava, espirrando."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    junta = ease_out(rel(t, 0.0, 0.3), 2)
    sub = np.random.default_rng(8)
    gotas = []
    for _ in range(26):
        u = sub.uniform(0, 1)
        alvo = (-0.85 + 0.65 * u, -0.45 + 0.1 * u)
        ox, oy = alvo[0] + sub.uniform(-0.4, 0.4), alvo[1] + sub.uniform(-0.4, 0.4)
        gotas.append((ox + (alvo[0] - ox) * junta, oy + (alvo[1] - oy) * junta, 1 - junta * 0.7))
    if t < 0.4:
        G += T.splats(gotas, 0.018) * 1.1
    forma = rel(t, 0.25, 0.35)
    voa = ease_in(rel(t, 0.38, 0.55), 2)
    if forma > 0 and t < 0.75:
        dx, dy = 0.85 * voa, 0.42 * voa
        L = T.polys([(lamina(-0.95 + dx, -0.48 + dy, 0.05 + dx, -0.3 + dy, 0.075 * forma), 1.0)])
        G += L * 1.4 + T.blur(L, 0.02) * 0.5
        H += np.clip(L - T.blur(L, 0.006), 0, 1) * 0.6
    G += _respingos(T, t, 9, 22, 0.55, 0.7, 0.1, 0.6, -2.6, -0.5) * 1.3
    H += T.gauss(0.72, 0.1, 0.05) * pulso(t, 0.53, 0.75) * 1.5
    return G * env, H * env


def _chifres(T, cx, cy, s):
    shapes = []
    for lado in (-1, 1):
        pts = [(cx + lado * 0.08 * s, cy), (cx + lado * 0.2 * s, cy - 0.15 * s), (cx + lado * 0.16 * s, cy - 0.32 * s), (cx + lado * 0.12 * s, cy - 0.14 * s), (cx + lado * 0.04 * s, cy - 0.02 * s)]
        shapes.append((pts, 1.0))
    return T.polys(shapes)


def power_preparo(T, t, rng):
    """O Preparo do Prêmio de sangue: o sangue gira em volta em gotas e os dois chifres se formam no alto
    (laço)."""
    G, H = vazio(T)
    pts = [(0.4 * math.cos(TAU * (t + k / 14)), 0.1 + 0.3 * math.sin(TAU * (t + k / 14)), 0.8) for k in range(14)]
    G += T.splats(pts, 0.025) * 1.2
    C = _chifres(T, 0, -0.25, 1.4)
    G += C * (0.8 + 0.2 * math.sin(TAU * t * 2)) + T.blur(C, 0.02) * 0.4
    H += np.clip(C - T.blur(C, 0.005), 0, 1) * 0.5
    return G, H


def premio_de_sangue(T, t, rng):
    """O Prêmio de sangue: a coroa de espinhos de sangue explode do chão em volta do rival (de fora para
    dentro), as gotas caem, e ele gira tonto (a espiral de estrelinhas)."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    shapes = []
    for k in range(12):
        a = TAU * k / 12
        t0 = 0.05 + 0.02 * k
        sobe = back(rel(t, t0, t0 + 0.2), 1.6) * (1 - rel(t, 0.6, 0.85))
        if sobe <= 0:
            continue
        bx, by = 0.55 * math.cos(a), 0.35 + 0.2 * math.sin(a)
        alt = (0.35 + 0.15 * (k % 3) / 2) * sobe
        shapes.append(([(bx - 0.05, by), (bx + 0.05, by), (bx - 0.02 * math.cos(a), by - alt)], 1.0))
    if shapes:
        E = T.polys(shapes)
        G += E * 1.1 + T.blur(E, 0.02) * 0.5
        H += np.clip(E - T.blur(E, 0.005), 0, 1) * 0.5
    G += _respingos(T, t, 77, 30, 0.2, 0.0, 0.2, 0.7) * 1.1
    tonto = pulso(t, 0.35, 1.0)
    if tonto > 0:
        estrelas = []
        for k in range(5):
            a = TAU * (k / 5 + t * 1.5)
            estrelas.append((estrela(0.25 * math.cos(a), -0.35 + 0.08 * math.sin(a), 0.045, a, 5, 0.45), 1.0))
        G += T.polys(estrelas) * tonto * 1.1
    return G * env, H * env


# =================================================================== Makima
def _olho_makima(T, cx, cy, larg, abre, aneis=4):
    pts = [(cx + larg * math.cos(a), cy + larg * 0.45 * abre * math.sin(a)) for a in np.linspace(0, TAU, 40, endpoint=False)]
    O = T.polys([(pts, 1.0)])
    iris = T.zero()
    for k in range(aneis):
        iris += T.ring(larg * (0.12 + 0.09 * k) * min(1, abre * 1.5), larg * 0.012, cx, cy)
    return O, iris * O


def olhar_de_comando(T, t, rng):
    """O olho da Makima se abre grande no alto, com os anéis concêntricos na íris acendendo um a um, e a
    ordem sai em anéis que chegam ao rival e o prendem (Lento)."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    abre = back(rel(t, 0.0, 0.3), 1.2)
    O, iris = _olho_makima(T, 0, -0.35, 0.6, max(0.02, abre * 1.3))
    borda = np.clip(O - T.blur(O, 0.01) * 1.1, 0, 1)
    G += borda * 1.2 + iris * 1.6 + O * 0.1
    H += iris * 0.7 * pulso(t, 0.15, 0.95)
    for k in range(3):
        u = rel(t, 0.35 + 0.1 * k, 0.75 + 0.1 * k)
        if 0 < u < 1:
            G += T.ring(0.05 + 0.4 * u, 0.02, 0, -0.35 + 0.55 * u, squash=1.5) * (1 - u) * 1.2
    prende = pulso(t, 0.6, 1.0)
    G += T.ring(0.25, 0.015, 0, 0.2) * prende * 1.2
    return G * env, H * env


def corrente_de_obediencia(T, t, rng):
    """A guia fina chega até o rival vinda de cima, a coleira (o anel com as tachas) se fecha em volta do
    pescoço com um estalo, e o "X" do silêncio acende."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    vem = ease_out(rel(t, 0.0, 0.3), 2)
    G += T.polyline([(-0.6, -0.95), (-0.6 + 0.6 * vem, -0.95 + 0.7 * vem)], 0.022) * 1.2 * (1 - rel(t, 0.8, 0.95))
    fecha = back(rel(t, 0.25, 0.45), 1.6)
    if fecha > 0:
        r = 0.55 - 0.2 * fecha
        G += T.ring(r, 0.05, 0, -0.25, squash=2.2) * 1.2 * (1 - rel(t, 0.8, 0.95))
        tachas = [(r * math.cos(a), -0.25 + r * math.sin(a) / 2.2, 1.0) for a in np.linspace(0, TAU, 10, endpoint=False)]
        G += T.splats(tachas, 0.022) * 1.3 * (1 - rel(t, 0.8, 0.95))
    estalo = pulso(t, 0.4, 0.55)
    H += T.flare(0, -0.25, 0.5 * estalo + 0.01, 0, 0.02) * estalo
    x = pulso(t, 0.5, 1.0)
    G += T.lines([(-0.15, 0.05, 0.15, 0.35, 1.0), (-0.15, 0.35, 0.15, 0.05, 1.0)], 0.03) * x * 1.2
    return G * env, H * env


def controle_total(T, t, rng):
    """O "bang": o dedo aponta da esquerda (o clarão na ponta do dedo), e a pressão invisível esmaga o
    rival de cima — as linhas descem e apertam para dentro, e a cratera abre no chão."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    dedo = pulso(t, 0.0, 0.3)
    G += T.polys([(lamina(-0.95, 0.0, -0.6, -0.02, 0.05), 1.0)]) * dedo * 1.0
    H += (T.gauss(-0.6, -0.02, 0.04) * 1.5 + T.flare(-0.6, -0.02, 0.4 * dedo + 0.01, 0, 0.02)) * dedo
    aperta = ease_in(rel(t, 0.25, 0.5), 2)
    if 0 < aperta and t < 0.75:
        segs = []
        for k in range(9):
            x = -0.5 + 0.125 * k
            y0 = -0.95 + 0.6 * aperta
            segs.append((x * (1 - 0.4 * aperta), y0 - 0.3, x * (1 - 0.6 * aperta), y0 + 0.15, 1.0))
        G += T.tapered(segs, 0.03) * 1.2
    esmaga = rel(t, 0.5, 0.95)
    if esmaga > 0:
        G += T.ring(0.08 + 0.55 * ease_out(esmaga, 2), 0.04, 0, 0.3, squash=2.6) * (1 - esmaga) * 1.4
        G += T.gauss(0, 0.05, 0.25, 0.08 * (1 - esmaga) + 0.02) * (1 - esmaga) * 1.4
        q = np.random.default_rng(14)
        for k in range(6):
            a = math.pi * (k / 5)
            G += T.polyline(jagged(q, 0, 0.3, 0.7 * esmaga * math.cos(a), 0.3 + 0.15 * esmaga * math.sin(a), 3, 0.3), 0.01) * (1 - rel(t, 0.8, 1))
        H += T.gauss(0, 0.1, 0.12) * pulso(esmaga, 0, 0.3) * 1.6
    return G * env, H * env


# =================================================================== Frieren
def _circulo_magico(T, cx, cy, r, ang, sq=1.0):
    """O círculo mágico: dois anéis, as runas (traços curtos) entre eles e a estrela de seis pontas."""
    out = T.ring(r, r * 0.04, cx, cy, squash=sq) + T.ring(r * 0.78, r * 0.03, cx, cy, squash=sq)
    runas = []
    for k in range(16):
        a = ang + TAU * k / 16
        x, y = cx + r * 0.89 * math.cos(a), cy + r * 0.89 * math.sin(a) / sq
        runas.append((x - r * 0.03 * math.sin(a), y + r * 0.03 * math.cos(a) / sq, x + r * 0.03 * math.sin(a), y - r * 0.03 * math.cos(a) / sq, 1.0))
    out += T.lines(runas, r * 0.035)
    est = [(cx + r * 0.75 * math.cos(-ang + TAU * k / 6 * 2 + math.pi / 2), cy + r * 0.75 * math.sin(-ang + TAU * k / 6 * 2 + math.pi / 2) / sq) for k in range(4)]
    est2 = [(cx + r * 0.75 * math.cos(-ang + TAU * k / 6 * 2 - math.pi / 2), cy + r * 0.75 * math.sin(-ang + TAU * k / 6 * 2 - math.pi / 2) / sq) for k in range(4)]
    out += T.polyline(est, r * 0.03) + T.polyline(est2, r * 0.03)
    return out


def analise_de_mana(T, t, rng):
    """O círculo mágico gira no chão do rival (os anéis de runas), o feixe fino varre o corpo de baixo para
    cima, e a chama de mana dele aparece; os buffs saem voando em faíscas para fora."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    surge = ease_out(rel(t, 0.0, 0.25), 2)
    C = _circulo_magico(T, 0, 0.4, 0.55 * surge + 0.01, t * 3, sq=3.0)
    G += C * 1.1 * (1 - rel(t, 0.8, 0.95))
    varre = rel(t, 0.2, 0.55)
    if 0 < varre < 1:
        y = 0.4 - 0.9 * varre
        G += T.lines([(-0.45, y, 0.45, y, 1.0)], 0.012) * 1.3
        H += T.lines([(-0.35, y, 0.35, y, 1.0)], 0.006) * 0.8
    chama = pulso(t, 0.4, 1.0)
    if chama > 0:
        pts = []
        for lado in (1, -1):
            rng_ = range(13) if lado == 1 else range(12, -1, -1)
            for k in rng_:
                u = k / 12
                w = 0.25 * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.7
                pts.append((lado * w + 0.04 * math.sin(t * 20 + 6 * u) * u, 0.3 - 0.75 * u))
        F = T.polys([(pts, 1.0)])
        G += np.clip(F - T.blur(F, 0.012) * 1.1, 0, 1) * 1.2 * chama + F * 0.15 * chama
    sai = rel(t, 0.5, 0.9)
    if sai > 0:
        sub = np.random.default_rng(2)
        pts = [(math.cos(a) * (0.2 + 0.6 * sai), -0.1 + math.sin(a) * (0.2 + 0.6 * sai), 1 - sai) for a in sub.uniform(0, TAU, 14)]
        G += T.splats(pts, 0.016) * 1.2
    return G * env, H * env


def frieren_preparo(T, t, rng):
    """O Preparo da Magia preparada: três círculos mágicos empilhados (de lado, achatados) girando em
    sentidos alternados (laço)."""
    G, H = vazio(T)
    for k in range(3):
        C = _circulo_magico(T, 0, -0.25 + 0.25 * k, 0.32 - 0.04 * k, TAU * t * (1 if k % 2 else -1), sq=3.0)
        G += C * (0.8 - 0.1 * k)
    G += T.gauss(0, 0, 0.12, 0.4) * 0.3
    return G, H


def magia_preparada(T, t, rng):
    """A Magia preparada: os círculos mágicos se abrem no ar em volta do rival (de frente, um depois do
    outro) e disparam juntos feixes finos que convergem nele, com o clarão."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    posicoes = [(0.72 * math.cos(a), 0.6 * math.sin(a) - 0.05) for a in np.linspace(math.pi * 0.9, math.pi * 2.1, 6)]
    for k, (x, y) in enumerate(posicoes):
        abre = ease_out(rel(t, 0.03 + 0.05 * k, 0.25 + 0.05 * k), 2)
        if abre <= 0:
            continue
        C = _circulo_magico(T, x, y, 0.13 * abre, t * 6 + k)
        G += C * 1.0 * (1 - rel(t, 0.75, 0.9))
        dispara = rel(t, 0.45, 0.6)
        if 0 < dispara and t < 0.75:
            G += T.lines([(x, y, x + (0 - x) * dispara, y + (0 - y) * dispara, 1.0)], 0.014) * 1.3
            H += T.lines([(x, y, x + (0 - x) * dispara, y + (0 - y) * dispara, 1.0)], 0.006) * 0.8
    acerta = pulso(t, 0.55, 0.85)
    G += T.gauss(0, 0, 0.2) * acerta * 1.4
    H += (T.flare(0, 0, 0.9 * acerta + 0.01, 0.2, 0.015) + T.gauss(0, 0, 0.06) * 1.5) * acerta
    return G * env, H * env


# =================================================================== Anya
def _interrogacao(cx, cy, s):
    pts = []
    for a in np.linspace(math.pi * 1.1, math.pi * 2.4, 14):
        pts.append((cx + 0.08 * s * math.cos(a), cy - 0.06 * s + 0.08 * s * math.sin(a)))
    pts += [(cx + 0.0, cy + 0.06 * s)]
    return pts


def leitura_mental(T, t, rng):
    """A telepatia: as ondas saem do alto à esquerda (arcos), o balão de pensamento aparece sobre o rival
    (as bolinhas e a nuvem) com o "?" dentro, e as estrelinhas giram em volta (Confuso)."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    for k in range(3):
        u = rel(t, 0.0 + 0.08 * k, 0.4 + 0.08 * k)
        if 0 < u < 1:
            G += T.arc_band(0.15 + 0.7 * u, 0.025, -0.5, 1.0, cx=-0.8, cy=-0.8, taper=0.0) * (1 - u) * 1.1
    balao = back(rel(t, 0.3, 0.5), 1.4)
    if balao > 0:
        nuvem = sum(T.gauss(0.0 + dx * 1.6, -0.45 + dy * 1.6, 0.17 * balao) for dx, dy in ((-0.12, 0.0), (0.0, -0.05), (0.12, 0.0), (-0.06, 0.06), (0.06, 0.06)))
        borda = np.clip(np.clip(nuvem * 1.6, 0, 1) - np.clip(T.blur(nuvem, 0.012) * 1.9, 0, 1) + 0.0, 0, 1)
        G += np.clip(nuvem, 0, 1) * 0.25 + T.splats([(-0.18, -0.2, balao), (-0.25, -0.1, balao * 0.7)], 0.02) * 1.2
        G += T.ring(0.32 * balao, 0.016, 0, -0.45, squash=1.4) * 1.1
        G += T.polyline(_interrogacao(0, -0.5, 2.6 * balao), 0.03) * 1.4 + T.gauss(0, -0.3, 0.022) * 1.4 * balao
    tonto = pulso(t, 0.45, 1.0)
    if tonto > 0:
        estrelas = [(estrela(0.3 * math.cos(TAU * (k / 5 + t * 1.5)), 0.05 + 0.08 * math.sin(TAU * (k / 5 + t * 1.5)), 0.04, t * 5, 5, 0.45), 1.0) for k in range(5)]
        G += T.polys(estrelas) * tonto
    return G * env, H * env


def alerta_urgente(T, t, rng):
    """O alerta: os pontos de exclamação pulam em volta do aliado (um depois do outro), e a bolha-escudo
    redonda se fecha nele, com as estrelinhas brilhando na superfície."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    for k, (x, y) in enumerate(((-0.5, -0.45), (0.5, -0.5), (-0.6, 0.15), (0.6, 0.1))):
        pula = back(rel(t, 0.02 + 0.06 * k, 0.2 + 0.06 * k), 2.0) * (1 - rel(t, 0.55, 0.7))
        if pula <= 0:
            continue
        G += T.polys([([(x - 0.03, y - 0.15 * pula), (x + 0.03, y - 0.15 * pula), (x + 0.015, y + 0.03 * pula), (x - 0.015, y + 0.03 * pula)], 1.0)]) * 1.3
        G += T.gauss(x, y + 0.08 * pula, 0.022) * 1.4 * pula
    fecha = back(rel(t, 0.3, 0.55), 1.3)
    if fecha > 0:
        r = 0.48 * fecha
        G += T.ring(r, 0.03) * 1.1 + T.gauss(0, 0, r * 0.8 + 0.01) * 0.15
        H += T.arc_band(r * 0.85, 0.02, 3.6, 4.4, taper=0.0) * 0.8
        est = [(estrela(r * 0.7 * math.cos(a), r * 0.7 * math.sin(a), 0.035, a, 4, 0.35), 1.0) for a in np.linspace(0, TAU, 6, endpoint=False) + t * 2]
        G += T.polys(est) * 1.1 * pulso(t, 0.35, 1.0)
    return G * env, H * env


def plano_secreto(T, t, rng):
    """O plano secreto: as linhas tracejadas do plano se desenham em volta do rival (os traços, as setas
    e o círculo do alvo), e o carimbo de "X" bate no meio com o tranco."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    desenha = ease_out(rel(t, 0.0, 0.4), 1.6)
    trilhas = [((-0.85, 0.5), (-0.3, 0.1), (0.0, 0.0)), ((0.85, 0.55), (0.4, 0.3), (0.0, 0.0)), ((0.0, -0.9), (-0.1, -0.45), (0.0, 0.0))]
    for k, (a, b, c) in enumerate(trilhas):
        pts = []
        for u in np.linspace(0, 1, 40):
            if u > desenha:
                break
            x = (1 - u) ** 2 * a[0] + 2 * (1 - u) * u * b[0] + u * u * c[0]
            y = (1 - u) ** 2 * a[1] + 2 * (1 - u) * u * b[1] + u * u * c[1]
            pts.append((x, y))
        segs = [(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 1.0) for i in range(0, len(pts) - 1, 2)]
        if segs:
            G += T.lines(segs, 0.012) * 1.1 * (1 - rel(t, 0.8, 0.95))
    G += T.ring(0.22, 0.012) * desenha * 1.0 * (1 - rel(t, 0.8, 0.95))
    bate = rel(t, 0.45, 0.55)
    if bate > 0:
        s = 1 + 0.6 * (1 - ease_out(bate, 3))
        X = T.lines([(-0.2 * s, -0.2 * s, 0.2 * s, 0.2 * s, 1.0), (-0.2 * s, 0.2 * s, 0.2 * s, -0.2 * s, 1.0)], 0.07)
        G += X * 1.3 * (1 - rel(t, 0.85, 0.98))
        H += np.clip(X - T.blur(X, 0.01), 0, 1) * 0.4
        G += T.ring(0.3 + 0.3 * rel(t, 0.5, 0.8), 0.02) * (1 - rel(t, 0.5, 0.8)) * (t > 0.5) * 1.2
    return G * env, H * env


REGISTRO = [
    ("puxar_a_corda", puxar_a_corda, GRANDE, "Denji · a cordinha, a fumaça e a serra saltando", False),
    ("frenesi_de_sangue", frenesi_de_sangue, GRANDE, "Denji · três motosserras cortando e o sangue", False),
    ("lanca_de_sangue", lanca_de_sangue, GRANDE, "Power · as gotas viram a lança e cravam", False),
    ("power_preparo", power_preparo, MEDIA, "Power · o sangue girando e os chifres (Preparo, laço)", True),
    ("premio_de_sangue", premio_de_sangue, GRANDE, "Power · a coroa de espinhos de sangue", False),
    ("olhar_de_comando", olhar_de_comando, GRANDE, "Makima · o olho de anéis e a ordem", False),
    ("corrente_de_obediencia", corrente_de_obediencia, GRANDE, "Makima · a guia e a coleira que fecha", False),
    ("controle_total", controle_total, GRANDE, "Makima · o bang e a pressão que esmaga", False),
    ("analise_de_mana", analise_de_mana, GRANDE, "Frieren · o círculo, o feixe e a chama de mana", False),
    ("frieren_preparo", frieren_preparo, MEDIA, "Frieren · os círculos empilhados (Preparo, laço)", True),
    ("magia_preparada", magia_preparada, GRANDE, "Frieren · os círculos no ar e os feixes juntos", False),
    ("leitura_mental", leitura_mental, GRANDE, "Anya · as ondas, o balão com ? e as estrelinhas", False),
    ("alerta_urgente", alerta_urgente, GRANDE, "Anya · os ! pulando e a bolha-escudo", False),
    ("plano_secreto", plano_secreto, GRANDE, "Anya · o plano tracejado e o carimbo de X", False),
]
