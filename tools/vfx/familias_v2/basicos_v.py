"""Ataques básicos com animação própria, lote v: Saitama, Yuji, Megumi, Sukuna, Eren, Gon, Kurapika e Edward.

Golpes simples, cada um do personagem: o jab de luva vermelha do Saitama com o "POW" de quadrinho, o Punho
Divergente do Yuji (o soco e o segundo impacto atrasado da energia amaldiçoada), o soco do Megumi saindo da
sombra, a mão em faca do Sukuna, o punho do Eren que cristaliza no endurecimento, o soco do Gon com a aura de
Nen, o punho do Kurapika enrolado na corrente e o braço de automail do Edward com as faíscas da alquimia.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, janela, pulso, rastro_de_velocidade, rel, vazio
from .basicos_a import _elipse_pts, _nuvem
from .basicos_u import _anel, _antebraco, _estrela_de_contato, _mao, _pts, _riscos, _vai_e_volta


def _pow(T, t, t0, r=0.42, seed=3, dur=0.45):
    """O balão de impacto de quadrinho: estrela irregular de pontas desiguais que pula e encolhe."""
    k = pulso(t, t0, t0 + dur)
    if k <= 0:
        return T.zero(), T.zero()
    q = np.random.default_rng(seed)
    pts = []
    n = 11
    for j in range(2 * n):
        a = math.pi * j / n + 0.1
        rr = r * (1.0 if j % 2 == 0 else 0.55) * q.uniform(0.75, 1.15) * (0.6 + 0.4 * k)
        pts.append((rr * math.cos(a), rr * math.sin(a) * 0.85))
    cheio = T.polys([(pts, 1.0)], 0.004)
    borda = np.clip(cheio - T.blur(cheio, 0.012) * 0.8, 0, 1)
    return cheio * k, borda * k


# ------------------------------------------------------------------ Saitama
def jab_de_luva_vermelha(T, t, rng):
    """Saitama: a luva vermelha entra num jab sem esforço nenhum e o alvo leva um "POW" de quadrinho, com as
    linhas de susto em volta; nada de vendaval, só um soco normal (que dói)."""
    G, H = vazio(T)
    env = apaga(t, 0.76, 1)
    px = _vai_e_volta(t, 0.2, recua=0.24)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.44, 0.6))
    M, d = _mao(T, px, 0.0, 1.1, 'luva')
    A, B = _antebraco(T, px, 0.0, 1.1, 0.45, 0.1, (0.0, 0.1))
    corpo = np.clip(M + A, 0, 1) * vis
    t0 = 0.2
    cheio, borda = _pow(T, t, t0, 0.46, 9)
    susto = _riscos(T, t, t0 + 0.04, 0.42, 10, 0.4, 0.66, 0.022, 4, 0.0, TAU)
    G += (corpo * 1.1 + T.blur(corpo, 0.02) * 0.35 + cheio * 0.9 + susto * 1.2) * env
    H += (corpo * 0.3 + B * vis * 0.8 + d * vis * 0.6 + borda * 1.4 + cheio * 0.35 + susto * 0.7) * env
    return G, H


# ------------------------------------------------------------------ Yuji
def soco_divergente(T, t, rng):
    """Yuji: o Punho Divergente. O soco bate e, um instante depois, a energia amaldiçoada que ficou atrasada
    chega e explode no mesmo ponto: dois impactos, o segundo maior e com faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    px = _vai_e_volta(t, 0.2, recua=0.14)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.5, 0.66))
    M, d = _mao(T, px, 0.0, 1.1)
    A, B = _antebraco(T, px, 0.0, 1.1, 0.46, 0.11)
    corpo = np.clip(M + A, 0, 1) * vis
    # a energia que vem atrasada: um contorno que segue o punho com atraso
    atras = _vai_e_volta(max(0.0, t - 0.1), 0.2, recua=0.0)
    eco = T.zero()
    ke = janela(t, 0.04, 0.1) * (1 - rel(t, 0.3, 0.36))
    if ke > 0:
        Me, _ = _mao(T, atras, 0.0, 1.2)
        eco = np.clip(T.blur(Me, 0.02) * 2 - Me, 0, 1) * ke
    t0, t1 = 0.2, 0.31
    est1 = _estrela_de_contato(T, t, t0, 0.2, 8, 0.4, 0.2, 0.2)
    est2 = _estrela_de_contato(T, t, t1, 0.42, 6, 0.3, 0.5, 0.36)
    onda = _anel(T, t, t1, t1 + 0.45, 0.1, 0.62, 0.05, 1.2)
    fa = _riscos(T, t, t1, 0.4, 9, 0.22, 0.6, 0.026, 21, 0.0, TAU)
    clarao = T.gauss(0, 0, 0.17) * pulso(t, t1, t1 + 0.18) * 2.0
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + eco * 1.3 + est1 + est2 * 1.3 + onda * 1.3 + fa * 1.2 + clarao) * env
    H += (corpo * 0.3 + d * vis * 0.8 + eco * 0.8 + est1 * 0.8 + est2 * 1.0 + onda * 0.4 + fa * 0.8 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Megumi
def soco_das_sombras(T, t, rng):
    """Megumi: o punho sai de uma poça de sombra que se abre atrás dele, arrastando fiapos escuros, e o impacto
    espirra sombra como tinta, que escorre e volta para o chão."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    px = _vai_e_volta(t, 0.24, -0.9, -0.14, 0.18)
    vis = janela(t, 0.02, 0.08) * (1 - rel(t, 0.48, 0.64))
    M, d = _mao(T, px, 0.0, 1.05)
    A, _ = _antebraco(T, px, 0.0, 1.05, 0.4, 0.1)
    corpo = np.clip(M + A, 0, 1) * vis
    poca = T.zero()
    kp = pulso(t, 0.0, 0.4)
    if kp > 0:
        poca = T.ring(0.16 * (0.5 + kp), 0.05, -0.78, 0.0, 0.35) * kp + T.gauss(-0.78, 0.0, 0.1, 0.18) * kp * 0.8
    fiapos = T.zero()
    if vis > 0.05:
        segs = []
        for j in range(5):
            y = -0.12 + 0.06 * j
            onda = 0.04 * math.sin(t * 30 + j * 1.7)
            segs.append((px - 0.75, y + onda, px - 0.3, y * 0.6, 0.8))
        fiapos = T.tapered(segs, 0.03) * vis
    t0 = 0.24
    u = rel(t, t0, t0 + 0.6)
    tinta = T.zero()
    if 0 < u < 1:
        q = np.random.default_rng(61)
        pts = []
        for _ in range(14):
            a = q.uniform(-2.0, 2.0)
            r = q.uniform(0.15, 0.5) * ease_out(min(1, u * 2.2), 2)
            pts.append((r * math.cos(a), r * math.sin(a) + 0.35 * u * u, (1 - u) * q.uniform(0.6, 1.1)))
        tinta = T.splats(pts, 0.03)
    mancha = T.gauss(0, 0, 0.14, 0.12) * pulso(t, t0, t0 + 0.35) * 1.6
    est = _estrela_de_contato(T, t, t0, 0.24, 7, 0.4, 0.1, 0.3)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.4 + poca * 1.2 + fiapos * 0.9 + tinta * 1.4 + mancha + est) * env
    H += (corpo * 0.3 + d * vis * 0.8 + poca * 0.3 + tinta * 0.4 + est * 0.9 + mancha * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Sukuna
# a mão aberta em faca, de lado: o dorso, os quatro dedos juntos e esticados (pontas arredondadas) e o polegar dobrado
_MAO_FACA = [(-0.14, -0.1), (0.04, -0.11), (0.3, -0.1), (0.36, -0.08), (0.38, -0.05), (0.36, -0.02), (0.3, 0.0), (0.06, 0.03), (0.0, 0.08), (-0.1, 0.1), (-0.14, 0.08)]
_DEDOS = [((0.06, -0.075), (0.34, -0.075)), ((0.06, -0.045), (0.36, -0.045)), ((0.06, -0.018), (0.32, -0.018))]


def golpe_de_mao_sukuna(T, t, rng):
    """Sukuna: a mão aberta em faca, dedos juntos e esticados, desce em diagonal e deixa um risco fino e claro
    no ar; no alvo, um estalo seco e dois traços curtos, de quem bate sem nem se esforçar."""
    G, H = vazio(T)
    env = apaga(t, 0.76, 1)
    u = ease_in(rel(t, 0.0, 0.22), 1.5)
    ang = -0.6 + 0.7 * u
    px, py = -0.85 + 0.8 * u, -0.5 + 0.48 * u
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.36, 0.52))
    mao = T.polys([(_pts(_MAO_FACA, px, py, 1.5, ang), 1.0)], 0.004)
    braco = T.polys([(_pts([(-0.12, -0.1), (-0.6, -0.12), (-0.6, 0.12), (-0.12, 0.09)], px, py, 1.5, ang), 0.8)], 0.004)
    dedos = sum(T.polyline(_pts([a, b], px, py, 1.5, ang), 0.007) for a, b in _DEDOS)
    corpo = np.clip(mao + braco, 0, 1) * vis
    # as marcas do braço (as faixas do Sukuna)
    faixas = T.zero()
    for k in range(2):
        x0 = -0.3 - 0.12 * k
        faixas += T.polyline(_pts([(x0, -0.12), (x0 + 0.04, 0.12)], px, py, 1.5, ang), 0.016)
    risco = T.zero()
    kr = janela(t, 0.06, 0.12) * (1 - rel(t, 0.26, 0.5))
    if kr > 0:
        risco = T.tapered([(-0.75, -0.5, 0.2, 0.08, 1.0)], 0.03) * kr
    t0 = 0.22
    traco = T.zero()
    kt = janela(t, t0, t0 + 0.04) * (1 - rel(t, t0 + 0.2, t0 + 0.5))
    if kt > 0:
        traco = (T.tapered([(-0.3, -0.24, 0.32, 0.2, 1.0)], 0.035) + T.tapered([(-0.22, -0.32, 0.36, 0.08, 1.0)], 0.022)) * kt
    est = _estrela_de_contato(T, t, t0, 0.24, 4, 0.18, 0.6, 0.24)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + risco * 0.8 + traco * 1.4 + est * 1.2) * env
    H += (corpo * 0.35 + (faixas + dedos) * vis * 1.0 + risco * 0.5 + traco * 1.2 + est) * env
    return G, H


# ------------------------------------------------------------------ Eren
def soco_endurecido(T, t, rng):
    """Eren: no meio do soco a pele do punho cristaliza (o endurecimento do Titã de Ataque), as facetas brilham e
    o impacto solta lascas de cristal que caem."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    px = _vai_e_volta(t, 0.24, recua=0.16)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.48, 0.64))
    M, d = _mao(T, px, 0.0, 1.15)
    A, _ = _antebraco(T, px, 0.0, 1.15, 0.45, 0.11)
    corpo = np.clip(M + A, 0, 1) * vis
    cristal = janela(t, 0.1, 0.22)
    facetas = T.zero()
    if cristal > 0:
        segs = []
        for (x1, y1, x2, y2) in [(-0.12, -0.15, 0.06, 0.0), (0.06, 0.0, -0.1, 0.16), (0.06, 0.0, 0.16, -0.12), (0.06, 0.0, 0.16, 0.12),
                                 (-0.12, -0.15, -0.3, 0.0), (-0.3, 0.0, -0.1, 0.16)]:
            segs.append((px + x1 * 1.15, y1 * 1.15, px + x2 * 1.15, y2 * 1.15, 1.0))
        facetas = T.lines(segs, 0.02) * cristal * vis
    brilho = T.gauss(px + 0.1, -0.05, 0.05) * pulso(t, 0.14, 0.3) * 1.6
    t0 = 0.24
    u = rel(t, t0, t0 + 0.6)
    lascas = T.zero()
    if 0 < u < 1:
        q = np.random.default_rng(88)
        polys = []
        for _ in range(10):
            a = q.uniform(-2.2, 2.2)
            dist = q.uniform(0.22, 0.66) * ease_out(u, 1.8)
            cx, cy = dist * math.cos(a), dist * math.sin(a) + 0.4 * u * u
            s = q.uniform(0.06, 0.1) * (1 - 0.4 * u)
            rot = q.uniform(0, TAU) + u * 4
            polys.append((_pts([(0, -1), (0.55, 0), (0, 1.3), (-0.45, 0)], cx, cy, s, rot), 1 - u))
        lascas = T.polys(polys, 0.003)
    est = _estrela_de_contato(T, t, t0, 0.3, 6, 0.3, 0.3, 0.3)
    onda = _anel(T, t, t0, t0 + 0.4, 0.1, 0.5, 0.04, 1.2)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + facetas * 1.2 + lascas * 1.4 + est * 1.1 + onda + brilho) * env
    H += (corpo * 0.3 + d * vis * 0.6 + facetas * 1.3 + lascas * 0.9 + est + onda * 0.4 + brilho * 1.4) * env
    return G, H


# ------------------------------------------------------------------ Gon
def soco_do_gon(T, t, rng):
    """Gon: a aura de Nen sobe em labaredas em volta do punho fechado (a mesma pose da Pedra, mas sem carregar)
    e o soco acerta com um estouro redondo e as labaredas espalhando."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    px = _vai_e_volta(t, 0.24, recua=0.18)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.48, 0.64))
    M, d = _mao(T, px, 0.0, 1.1)
    A, B = _antebraco(T, px, 0.0, 1.1, 0.42, 0.11)
    corpo = np.clip(M + A, 0, 1) * vis
    aura = T.zero()
    ka = vis * janela(t, 0.0, 0.08)
    if ka > 0:
        segs = []
        for j in range(9):
            x0 = px - 0.4 + 0.065 * j
            alto = 0.1 + 0.08 * math.sin(t * 34 + j * 1.3) + 0.06 * (j > 5)
            segs.append((x0, -0.12, x0 - 0.06, -0.12 - alto, 1.0))
            segs.append((x0, 0.12, x0 - 0.06, 0.12 + alto * 0.6, 0.6))
        aura = T.tapered(segs, 0.04) * ka
    t0 = 0.24
    cheio = T.gauss(0, 0, 0.18) * pulso(t, t0, t0 + 0.24) * 1.6
    est = _estrela_de_contato(T, t, t0, 0.32, 8, 0.45, 0.0, 0.34)
    chamas = _riscos(T, t, t0, 0.45, 12, 0.2, 0.62, 0.04, 33, 0.0, TAU)
    onda = _anel(T, t, t0, t0 + 0.4, 0.12, 0.56, 0.045, 1.0)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + aura * 1.2 + cheio + est * 1.1 + chamas * 1.2 + onda) * env
    H += (corpo * 0.3 + d * vis * 0.8 + aura * 0.6 + cheio * 1.1 + est + chamas * 0.6 + onda * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Kurapika
def _elos(T, pts, tam=0.045, larg=0.011):
    """Uma corrente: elos ovais alternando de pé e deitado ao longo do caminho."""
    out = T.zero()
    for k in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[k], pts[k + 1]
        a = math.atan2(y2 - y1, x2 - x1)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        if k % 2 == 0:
            out += T.polyline(_elipse_pts(cx, cy, tam, tam * 0.5, a, 12) + [_elipse_pts(cx, cy, tam, tam * 0.5, a, 12)[0]], larg)
        else:
            out += T.lines([(cx - tam * math.cos(a), cy - tam * math.sin(a), cx + tam * math.cos(a), cy + tam * math.sin(a), 1.0)], larg * 1.6)
    return out


def soco_da_corrente(T, t, rng):
    """Kurapika: o punho direito enrolado na corrente vem num soco reto; a ponta da corrente balança atrás e,
    no impacto, os elos estalam e se espalham em volta do alvo por um instante."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    px = _vai_e_volta(t, 0.22, recua=0.18)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.48, 0.64))
    M, d = _mao(T, px, 0.0, 1.05)
    A, _ = _antebraco(T, px, 0.0, 1.05, 0.42, 0.1)
    corpo = np.clip(M + A, 0, 1) * vis
    # a corrente enrolada nos nós dos dedos e a ponta solta balançando atrás
    voltas = T.zero()
    for k in range(3):
        x = px - 0.05 - 0.08 * k
        voltas += T.polyline(_elipse_pts(x, 0.0, 0.035, 0.17, 0.0, 14) + [_elipse_pts(x, 0.0, 0.035, 0.17, 0.0, 14)[0]], 0.02)
    balanco = math.sin(t * 18) * 0.12
    ponta = [(px - 0.3 - 0.06 * j, 0.14 + 0.05 * j + balanco * (j / 6) ** 2) for j in range(7)]
    solta = _elos(T, ponta, 0.045, 0.015)
    t0 = 0.22
    ke = pulso(t, t0, t0 + 0.4)
    anel_elos = T.zero()
    if ke > 0:
        r = 0.2 + 0.25 * ease_out(rel(t, t0, t0 + 0.4), 2)
        circ = [(r * math.cos(TAU * j / 14 + t * 3), r * math.sin(TAU * j / 14 + t * 3) * 0.85) for j in range(15)]
        anel_elos = _elos(T, circ, 0.06, 0.018) * ke
    est = _estrela_de_contato(T, t, t0, 0.26, 8, 0.4)
    clarao = T.gauss(0, 0, 0.14) * pulso(t, t0, t0 + 0.16) * 1.8
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + (voltas + solta) * vis * 1.3 + anel_elos * 1.4 + est + clarao) * env
    H += (corpo * 0.25 + d * vis * 0.6 + (voltas + solta) * vis * 1.0 + anel_elos * 1.0 + est * 0.9 + clarao * 1.2) * env
    return G, H


# ------------------------------------------------------------------ Edward
def soco_de_automail(T, t, rng):
    """Edward: o braço de automail (placas de metal, juntas e parafusos) dá um soco seco; o impacto bate com
    faíscas de metal e os riscos azuis da alquimia estalando em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    px = _vai_e_volta(t, 0.22, recua=0.18)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.48, 0.64))
    e = 1.1
    M, d = _mao(T, px, 0.0, e)
    placas = T.polys([(_pts([(-0.12, -0.13), (-0.3, -0.12), (-0.3, 0.12), (-0.12, 0.13)], px, 0.0, e), 1.0),
                      (_pts([(-0.34, -0.12), (-0.55, -0.11), (-0.55, 0.11), (-0.34, 0.12)], px, 0.0, e), 1.0)], 0.003)
    corpo = np.clip(M + placas, 0, 1) * vis
    juntas = (T.ring(0.03, 0.012, px - 0.32 * e, 0.0) + T.gauss(px - 0.2 * e, -0.08 * e, 0.012) + T.gauss(px - 0.2 * e, 0.08 * e, 0.012)
              + T.gauss(px - 0.45 * e, -0.07 * e, 0.012) + T.gauss(px - 0.45 * e, 0.07 * e, 0.012)) * vis
    t0 = 0.22
    u = rel(t, t0, t0 + 0.5)
    fa = []
    if 0 < u < 1:
        q = np.random.default_rng(14)
        for _ in range(16):
            a = q.uniform(-2.3, 2.3)
            v = q.uniform(0.5, 1.1)
            x, y = math.cos(a) * v * ease_out(u, 1.6) * 0.7, math.sin(a) * v * ease_out(u, 1.6) * 0.55 + 0.45 * u * u
            fa.append((x - 0.06 * math.cos(a), y - 0.06 * math.sin(a), x, y, 1 - u))
    faiscas = T.tapered(fa, 0.032) if fa else T.zero()
    alq = T.zero()
    ka = pulso(t, t0 + 0.02, t0 + 0.4)
    if ka > 0:
        for j in range(5):
            a = TAU * j / 5 + 0.5
            alq += T.polyline(jagged(np.random.default_rng(140 + j + int(t * 20)), 0.12 * math.cos(a), 0.12 * math.sin(a),
                                     0.5 * math.cos(a), 0.5 * math.sin(a), 3, 0.2), 0.022)
        alq *= ka
    est = _estrela_de_contato(T, t, t0, 0.28, 8, 0.4)
    clarao = T.gauss(0, 0, 0.15) * pulso(t, t0, t0 + 0.16) * 2.0
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + faiscas * 1.8 + alq * 1.3 + est + clarao) * env
    H += (corpo * 0.3 + (d * 0.6 + juntas * 1.5) * 1.0 + faiscas * 1.2 + alq * 0.9 + est * 0.9 + clarao * 1.2) * env
    return G, H


REGISTRO = [
    ("jab_de_luva_vermelha", jab_de_luva_vermelha, GRANDE, "básico do Saitama: o jab de luva vermelha e o POW de quadrinho", False),
    ("soco_divergente", soco_divergente, GRANDE, "básico do Yuji: o Punho Divergente, com o segundo impacto atrasado", False),
    ("soco_das_sombras", soco_das_sombras, GRANDE, "básico do Megumi: o punho sai da sombra e espirra tinta escura", False),
    ("golpe_de_mao_sukuna", golpe_de_mao_sukuna, GRANDE, "básico do Sukuna: a mão em faca e o risco fino no ar", False),
    ("soco_endurecido", soco_endurecido, GRANDE, "básico do Eren: o punho cristaliza e solta lascas", False),
    ("soco_do_gon", soco_do_gon, GRANDE, "básico do Gon: a aura de Nen em labaredas e o estouro redondo", False),
    ("soco_da_corrente", soco_da_corrente, GRANDE, "básico do Kurapika: o punho enrolado na corrente e os elos estalando", False),
    ("soco_de_automail", soco_de_automail, GRANDE, "básico do Edward: o braço de automail, faíscas e a alquimia estalando", False),
]
