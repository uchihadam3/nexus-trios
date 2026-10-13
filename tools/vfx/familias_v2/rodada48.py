"""Rodada 48 das habilidades próprias: Ártemis, Hermes, Afrodite, Medusa, Cronos e Hércules.

Ártemis
- flecha_de_prata: a flecha de prata com o rastro de luar cravando e a mira lunar no rival (Marcado).
- cervo_sagrado: o cervo de luz saltando em volta dela e as pegadas brilhando (Esquiva e Acelerado).
- artemis_preparo: o Preparo da Caçada da lua — a lua crescente atrás e o arco puxado (laço).
- cacada_da_lua: a lua cheia acesa no alto e o feixe de luar enorme no rival.

Hermes
- caduceu: o bastão com as duas serpentes girando e a pancada que deixa tonto (Confuso).
- mensagem_dos_deuses: as sandálias aladas, o pergaminho voando e as penas no trio (Carga e Adianta o ataque).
- roubo_divino: o vulto alado passando pelo rival e levando os buffs embora.

Afrodite
- encanto_de_afrodite: o beijo soprado virando corações que rodam na cabeça dos rivais (Confuso).
- abraco_do_amor: a concha e as pétalas de rosa caindo sobre o trio com o brilho rosado (Regeneração e Vida).
- afrodite_preparo: o Preparo do Desejo — o coração pulsando e as pétalas girando (laço).
- desejo: o coração gigante se fechando no rival e rachando (Enfraquecido).

Medusa
- mordida_de_serpente: as cobras do cabelo dando o bote e o veneno pingando (Envenenado).
- olhar_de_pedra: os olhos acendendo e o raio de olhar virando pedra no rival (Paralisado).
- medusa_preparo: o Preparo da Petrificação — as serpentes se agitando e os olhos piscando (laço).
- petrificacao: o olhar varrendo todos e a pedra subindo pelos rivais, rachando (Paralisado).

Cronos
- foice_do_tempo: a foice com os números do relógio cortando e o tempo arrastando (Lento).
- atraso_de_cronos: o relógio no rival com os ponteiros voltando (Atrasa o Preparo e Lento).
- cronos_preparo: o Preparo da Era de ouro — a ampulheta girando e as engrenagens (laço).
- era_de_ouro: o relógio dourado gigante e os ponteiros correndo para frente sobre o trio (Acelerado).

Hércules
- clava_de_hercules: a clava em chamas descendo no rival (Enfraquecido).
- desafio_de_hercules: a pele de leão, o punho erguido e o desafio em ondas (Provocado e Protegido).
- hercules_preparo: o Preparo da Força de semideus — os músculos acendendo e o chão afundando (laço).
- forca_de_semideus: o soco de semideus com a aura dourada e o estrondo.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .basicos_a import _punho
from .unicas_kit import (AMPULHETA, ASA, CHAMA, CORACAO, GOTA, PENA, anel, cheio, clarao, converge, corte, engrenagem, estouro,
                         flor, icone, onda_no_chao, particulas, poe, surge)


def _zap(T, seed, x1, y1, x2, y2, w=0.012, prof=4, rough=0.3):
    q = np.random.default_rng(seed)
    return T.polyline(jagged(q, x1, y1, x2, y2, prof, rough), w)


def _lua(T, cx, cy, r, k, cheia=False):
    if cheia:
        return T.gauss(cx, cy, r * 0.95) * k * 1.0 + T.ring(r, r * 0.08, cx, cy) * k * 1.3, T.gauss(cx, cy, r * 0.4) * k * 1.0
    G = T.arc_band(r, r * 0.35, math.pi * 0.55, math.pi * 1.45, 1.0, 0, cx, cy, 1.0, True) * k * 1.4
    return G, G * 0.3


def _flecha(T, x, y, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    G = T.lines([(x - c * s, y - sn * s, x, y, 1.0)], s * 0.05) * k * 1.3
    ponta = [(x + c * s * 0.25, y + sn * s * 0.25), (x - sn * s * 0.1, y + c * s * 0.1), (x + sn * s * 0.1, y - c * s * 0.1)]
    g, h = icone(T, ponta, k * 1.3, 0.6)
    bx, by = x - c * s, y - sn * s
    for lado in (-1, 1):
        G += T.lines([(bx + c * s * 0.2, by + sn * s * 0.2, bx - lado * sn * s * 0.12, by + lado * c * s * 0.12, 1.0)], s * 0.035) * k * 1.0
    return G + g, h


def _serpente(T, x0, y0, x1, y1, t, w, k, onda=0.05, fase=0.0):
    pts = []
    for u in np.linspace(0, 1, 22):
        pts.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u + onda * math.sin(u * 10 - t * 18 + fase) * math.sin(math.pi * u * 0.9 + 0.1)))
    G = T.polyline(pts, w) * k
    G += T.gauss(x1, y1, w * 1.6) * k * 1.3
    return G


def _relogio(T, cx, cy, r, k, ponteiro, minuto):
    G = T.ring(r, r * 0.08, cx, cy) * k * 1.3
    G += T.gauss(cx, cy, r * 0.8) * k * 0.25
    segs = []
    for j in range(12):
        a = TAU * j / 12
        segs.append((cx + r * 0.8 * math.cos(a), cy + r * 0.8 * math.sin(a), cx + r * 0.92 * math.cos(a), cy + r * 0.92 * math.sin(a), 1.0))
    G += T.lines(segs, r * 0.04) * k * 1.1
    G += T.lines([(cx, cy, cx + r * 0.5 * math.cos(ponteiro), cy + r * 0.5 * math.sin(ponteiro), 1.0)], r * 0.07) * k * 1.3
    G += T.lines([(cx, cy, cx + r * 0.75 * math.cos(minuto), cy + r * 0.75 * math.sin(minuto), 1.0)], r * 0.045) * k * 1.3
    return G, T.gauss(cx, cy, r * 0.08) * k * 1.4


# ------------------------------------------------------------------ Ártemis

def flecha_de_prata(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.28), 1.4)
    if 0 < u < 1:
        x = -0.75 + 1.15 * u
        g, h = _flecha(T, x, 0.0, 0.0, 0.42, 1.0)
        G, H = G + g, H + h
        G += T.tapered([(x - 0.9, 0.0, x - 0.4, 0.0, 0.8)], 0.035) * 0.9
        q = np.random.default_rng(int(t * 30))
        for _ in range(4):
            px = x - q.uniform(0.4, 1.0)
            H += T.gauss(px, q.uniform(-0.04, 0.04), 0.008) * 1.4
    k = 1 - rel(t, 0.88, 1)
    if t >= 0.28 and k > 0:
        g, h = _flecha(T, 0.4, 0.0, 0.0, 0.42, k)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.25, 0.45, 0.42, 0.0, 0.9, 1.1)
    G, H = G + g2, H + h2
    m = surge(t, 0.35, 0.6) * (1 - rel(t, 0.88, 1))
    if m > 0:
        g3, h3 = _lua(T, 0.45, -0.35, 0.08 * m, 1.0)
        G, H = G + g3, H + h3
        G += T.ring(0.2 * m, 0.012, 0.45, 0.0) * 1.2
        for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
            G += T.lines([(0.45 + 0.13 * m * math.cos(a), 0.13 * m * math.sin(a), 0.45 + 0.26 * m * math.cos(a), 0.26 * m * math.sin(a), 1.0)], 0.01) * 1.3
    return G * env, H * env


_CERVO = [(-0.6, 0.2), (-0.55, -0.1), (-0.2, -0.15), (0.3, -0.15), (0.45, -0.35), (0.55, -0.6), (0.7, -0.55), (0.6, -0.3), (0.65, -0.1),
          (0.45, 0.0), (0.4, 0.2), (0.45, 0.6), (0.35, 0.6), (0.25, 0.2), (-0.3, 0.2), (-0.35, 0.6), (-0.45, 0.6), (-0.45, 0.25)]
_CHIFRE = [[(0.55, -0.6), (0.5, -0.85), (0.4, -1.0)], [(0.5, -0.85), (0.65, -0.95)], [(0.62, -0.58), (0.75, -0.8), (0.85, -0.88)]]


def _cervo(T, cx, cy, s, k):
    g, h = icone(T, poe(_CERVO, cx, cy, s), k, 0.4)
    for p in _CHIFRE:
        g = g + T.polyline([(cx + x * s, cy + y * s) for x, y in p], s * 0.04) * k * 1.2
    return g, h


def cervo_sagrado(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    k = 1 - rel(t, 0.85, 1)
    s = surge(t, 0.0, 0.25)
    for m in range(4):
        tm = t - 0.05 * m
        a = -math.pi / 2 + tm * TAU * 1.1
        x, y = 0.4 * math.cos(a), 0.1 + 0.18 * math.sin(a) - 0.12 * abs(math.sin(tm * TAU * 2.2))
        km = k * s * (1 if m == 0 else 0.3 / m)
        if km > 0:
            g, h = _cervo(T, x, y, 0.27, km * 1.1)
            G, H = G + g, H + h
    for j in range(8):
        a = -math.pi / 2 + j * 0.6
        w = rel(t, 0.06 * j, 0.06 * j + 0.5)
        if 0 < w < 1:
            G += T.ring(0.02, 0.008, 0.4 * math.cos(a), 0.32 + 0.05 * math.sin(a), 2.0) * (1 - w) * 1.4
            H += T.gauss(0.4 * math.cos(a), 0.32 + 0.05 * math.sin(a), 0.01) * (1 - w) * 1.2
    G += particulas(T, t, 0.1, 1.0, 16, 62, 0.0, 0.1, 0.5, 0.4, 0.01)
    return G * env, H * env


def artemis_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = _lua(T, 0.0, 0.0, 0.3, 0.7 + 0.2 * math.sin(t * TAU))
    G, H = G + g, H + h
    treme = 0.005 * math.sin(t * 60)
    G += T.arc_band(0.3, 0.02, -1.1, 1.1, 1.0, 0, -0.1, 0.0, 0.0) * 1.2
    G += T.lines([(-0.1 + 0.3 * math.cos(-1.1), 0.3 * math.sin(-1.1), -0.22 + treme, 0.0, 1.0),
                  (-0.22 + treme, 0.0, -0.1 + 0.3 * math.cos(1.1), 0.3 * math.sin(1.1), 1.0)], 0.006) * 1.3
    g2, h2 = _flecha(T, 0.4, 0.0, 0.0, 0.62, 1.0)
    G, H = G + g2, H + h2
    H += T.gauss(0.45, 0.0, 0.02) * (1.2 + 0.5 * math.sin(t * TAU * 2))
    return G, H


def cacada_da_lua(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        g, h = _lua(T, -0.3, -0.55, 0.18 * s, 1.0, True)
        G, H = G + g, H + h
        G += T.gauss(-0.3, -0.55, 0.22 * s) * 0.2
    G += converge(T, t, 0.1, 0.35, 12, 63, -0.3, -0.55, 0.45, 0.008)
    u = rel(t, 0.3, 0.5)
    k = 1 - rel(t, 0.72, 0.85)
    if u > 0 and k > 0:
        e = min(1.0, ease_in(u) * 1.2)
        x2, y2 = -0.3 + 0.75 * e, -0.55 + 0.55 * e
        G += T.tapered([(-0.3, -0.55, x2, y2, 1.0)], 0.2) * k * 0.7
        G += T.lines([(-0.3, -0.55, x2, y2, 1.0)], 0.035) * k * 1.4
        H += T.lines([(-0.3, -0.55, x2, y2, 1.0)], 0.012) * k * 1.2
    g2, h2 = clarao(T, t, 0.45, 0.75, 0.45, 0.0, 1.8, 1.7)
    G, H = G + g2, H + h2
    G += anel(T, t, 0.48, 0.9, 0.05, 0.7, 0.04, 0.0, 1.0, 1.4)
    G += estouro(T, t, 0.48, 0.9, 16, 64, 0.45, 0.0, 0.6, 0.013)
    return G * env, H * env


# ------------------------------------------------------------------ Hermes

def _caduceu(T, x, y, ang, s, k, t):
    c, sn = math.cos(ang), math.sin(ang)
    hx, hy = x + c * s, y + sn * s
    G = T.lines([(x, y, hx, hy, 1.0)], s * 0.04) * k * 1.2
    for m in (0, 1):
        pts = []
        for u in np.linspace(0.1, 0.85, 20):
            off = s * 0.09 * math.sin(u * 14 + m * math.pi + t * 6)
            pts.append((x + c * s * u - sn * off, y + sn * s * u + c * off))
        G += T.polyline(pts, s * 0.03) * k * 1.2
    for lado in (-1, 1):
        g, _ = icone(T, poe(ASA, hx - sn * s * 0.05 * lado, hy + c * s * 0.05 * lado, s * 0.18, ang + (0 if lado > 0 else math.pi)), k, 0.35)
        G += g
    return G


def caduceu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.3), 1.8)
    k = 1 - rel(t, 0.45, 0.57)
    if k > 0:
        ang = -2.3 + 2.0 * u
        G += _caduceu(T, 0.0 + 0.05 * math.cos(ang), 0.3, ang, 0.7, k, t)
    g, h = clarao(T, t, 0.28, 0.5, 0.45, 0.0, 1.1, 1.2)
    G, H = G + g, H + h
    G += anel(T, t, 0.3, 0.7, 0.05, 0.4, 0.03, 0.0)
    for m in range(2):
        kk = pulso(t, 0.45, 1.0)
        if kk > 0:
            G += T.arc_band(0.08 + 0.04 * m, 0.014, t * 12 + m * 3, t * 12 + m * 3 + 3.5, 2.5, 0, 0.45, -0.28 + 0.03 * m, 1.0) * kk * 1.3
    return G * env, H * env


def mensagem_dos_deuses(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = rel(t, 0.0, 0.5)
    if 0 < u < 1:
        x = -0.85 + 1.7 * ease_in(u, 1.1)
        y = -0.35 - 0.08 * math.sin(u * TAU * 2)
        rolo = [(-1, -0.6), (1, -0.6), (1, 0.6), (-1, 0.6)]
        g, h = icone(T, poe(rolo, x, y, 0.09, 0.1 * math.sin(t * 20)), 1.2, 0.5)
        G, H = G + g, H + h
        for lado in (-1, 1):
            g2, _ = icone(T, poe(ASA, x - 0.04, y + lado * 0.02, 0.09, -math.pi / 2 + lado * (0.4 + 0.4 * math.sin(t * 40))), 1.0, 0.3)
            G += g2
        G += T.tapered([(x - 0.4, y, x - 0.08, y, 0.8)], 0.025) * 0.9
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        a0 = 0.15 + 0.15 * i
        w = rel(t, a0, a0 + 0.55)
        if 0 < w < 1:
            for m in range(3):
                g3, h3 = icone(T, poe(PENA, cx - 0.08 + 0.08 * m + 0.04 * math.sin(w * 8 + m), -0.3 + 0.55 * w, 0.065, 0.6 * math.sin(w * 6 + m)), (1 - rel(w, 0.75, 1)) * 1.1, 0.5)
                G, H = G + g3, H + h3
            G += T.gauss(cx, 0.2, 0.1) * pulso(w, 0.4, 1.0) * 0.6
            G += T.ring(0.12, 0.01, cx, 0.3, 3.0) * pulso(w, 0.4, 1.0) * 1.2
    return G * env, H * env


def roubo_divino(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = rel(t, 0.0, 0.35)
    if 0 < u < 1:
        x = -0.9 + 1.8 * ease_in(u, 1.2)
        G += T.gauss(x, 0.0, 0.06, 0.15) * 1.0
        for lado in (-1, 1):
            g, _ = icone(T, poe(ASA, x - 0.03, 0.15, 0.1, -math.pi / 2 + lado * 0.6), 1.0, 0.3)
            G += g
        for m in range(4):
            G += T.tapered([(x - 0.6, -0.15 + 0.1 * m, x - 0.05, -0.15 + 0.1 * m, 0.8)], 0.02) * 1.0
    g2, h2 = clarao(T, t, 0.15, 0.32, 0.45, 0.0, 0.9, 1.1)
    G, H = G + g2, H + h2
    for j in range(2):
        w = rel(t, 0.3 + 0.08 * j, 0.85 + 0.08 * j)
        if 0 < w < 1:
            x = 0.45 + 0.5 * ease_in(w)
            y = -0.1 - 0.3 * math.sin(math.pi * w) + 0.1 * j
            G += T.ring(0.05, 0.012, x, y) * (1 - rel(w, 0.8, 1)) * 1.3
            H += T.gauss(x, y, 0.02) * (1 - rel(w, 0.8, 1)) * 1.5
            G += T.tapered([(0.45, -0.05, x, y, 0.6)], 0.012) * (1 - w) * 0.8
    G += estouro(T, t, 0.18, 0.6, 10, 65, 0.45, 0.0, 0.35, 0.011)
    return G * env, H * env


# ------------------------------------------------------------------ Afrodite

def encanto_de_afrodite(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(9):
        a0 = 0.03 * j
        u = rel(t, a0, a0 + 0.45)
        if 0 < u < 1:
            alvo = (-0.55, 0.0, 0.55)[j % 3]
            x = -0.7 + (alvo + 0.7) * ease_out(u, 1.4)
            y = -0.1 - 0.2 * math.sin(math.pi * u) + 0.06 * math.sin(u * 12 + j)
            g, h = cheio(T, poe(CORACAO, x, y, 0.04 + 0.01 * math.sin(u * 15)), (1 - rel(u, 0.85, 1)) * 1.3)
            G, H = G + g, H + h
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        k = pulso(t, 0.4 + 0.05 * i, 1.0)
        if k > 0:
            for m in range(3):
                a = t * 7 + TAU * m / 3
                g, h = cheio(T, poe(CORACAO, cx + 0.12 * math.cos(a), -0.3 + 0.04 * math.sin(a), 0.03), k * 1.3)
                G, H = G + g, H + h
            G += T.gauss(cx, -0.05, 0.12) * k * 0.3
    return G * env, H * env


def abraco_do_amor(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.8, 0.92))
    if s > 0:
        concha = []
        for a in np.linspace(math.pi, TAU, 14):
            concha.append((0.18 * s * math.cos(a), -0.45 + 0.13 * s * math.sin(a)))
        concha.append((0.04 * s, -0.36))
        concha.append((-0.04 * s, -0.36))
        g, h = icone(T, concha, 1.1, 0.4)
        G, H = G + g, H + h
        for j in range(7):
            a = math.pi + math.pi * (j + 0.5) / 7
            G += T.lines([(0.0, -0.37, 0.17 * s * math.cos(a), -0.45 + 0.12 * s * math.sin(a), 1.0)], 0.005) * 1.0
    q = np.random.default_rng(66)
    for j in range(20):
        x = q.uniform(-0.8, 0.8)
        a0 = 0.15 + q.uniform(0, 0.35)
        w = rel(t, a0, a0 + 0.5)
        if 0 < w < 1:
            g2, h2 = icone(T, poe(flor(5, 1.0, 0.3), x + 0.06 * math.sin(w * 8 + j), -0.4 + 0.7 * w, 0.03, w * 5), (1 - rel(w, 0.8, 1)) * 1.1, 0.5)
            G, H = G + g2, H + h2
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        k = pulso(t, 0.35 + 0.05 * i, 1.0)
        G += T.gauss(cx, 0.1, 0.15, 0.2) * k * 0.5
        if k > 0:
            g3, h3 = cheio(T, poe(CORACAO, cx, 0.0 - 0.15 * rel(t, 0.35, 1.0), 0.05), k * 1.2)
            G, H = G + g3, H + h3
    return G * env, H * env


def afrodite_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    g, h = icone(T, poe(CORACAO, 0.0, 0.0, 0.14 + 0.02 * b), 1.0 + 0.4 * b, 0.55)
    G, H = G + g, H + h
    G += T.gauss(0, 0, 0.25) * (0.2 + 0.15 * b)
    for j in range(8):
        a = t * TAU + TAU * j / 8
        g2, h2 = icone(T, poe(flor(5, 1.0, 0.3), 0.35 * math.cos(a), 0.35 * 0.55 * math.sin(a), 0.03, a), 1.0, 0.5)
        G, H = G + g2, H + h2
    return G, H


def desejo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    fecha = ease_in(rel(t, 0.0, 0.4), 1.6)
    k = 1 - rel(t, 0.55, 0.7)
    if k > 0:
        s = 0.55 - 0.4 * fecha
        g, h = icone(T, poe(CORACAO, 0.45, 0.0, s), k * 1.2, 0.25)
        G, H = G + g, H + h
        G += T.gauss(0.45, 0.0, s * 0.6) * k * 0.3 * fecha
    racha = ease_out(rel(t, 0.42, 0.55), 2)
    if racha > 0 and k > 0:
        G += _zap(T, 67, 0.45, -0.12, 0.45, 0.15, 0.012, 3, 0.4) * racha * k * 1.4
    g2, h2 = clarao(T, t, 0.42, 0.65, 0.45, 0.0, 1.5, 1.4)
    G, H = G + g2, H + h2
    q = np.random.default_rng(68)
    for j in range(10):
        w = rel(t, 0.5, 0.95)
        if 0 < w < 1:
            a = q.uniform(0, TAU)
            d = 0.05 + 0.4 * ease_out(w)
            g3, h3 = cheio(T, poe(CORACAO, 0.45 + d * math.cos(a), d * math.sin(a) + 0.2 * w * w, 0.025 * (1 - 0.4 * w), a), (1 - w) * 1.2)
            G, H = G + g3, H + h3
    m = surge(t, 0.6, 0.78) * (1 - rel(t, 0.88, 1))
    if m > 0:
        for j in range(2):
            y0 = -0.3 + 0.1 * j + 0.1 * rel(t, 0.6, 0.95)
            G += T.polyline([(0.38, y0), (0.45, y0 + 0.07 * m), (0.52, y0)], 0.014) * m * 1.2
    return G * env, H * env


# ------------------------------------------------------------------ Medusa

def mordida_de_serpente(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(3):
        a0 = 0.05 * j
        u = ease_in(rel(t, a0, a0 + 0.3), 1.6)
        k = 1 - rel(t, 0.55, 0.68)
        if u > 0 and k > 0:
            y0 = -0.25 + 0.12 * j
            G += _serpente(T, -0.55, y0, -0.55 + 0.95 * u, y0 * 0.3, t, 0.032, k * 1.2, 0.06, j * 2.0)
            boca = 0.3 * pulso(t, a0 + 0.2, a0 + 0.4)
            x1, y1 = -0.55 + 0.95 * u, y0 * 0.3
            G += T.lines([(x1, y1, x1 + 0.06, y1 - boca * 0.15, 1.0), (x1, y1, x1 + 0.06, y1 + boca * 0.15, 1.0)], 0.008) * k * 1.3
    g, h = clarao(T, t, 0.28, 0.5, 0.45, 0.0, 0.9, 1.1)
    G, H = G + g, H + h
    for j in range(6):
        w = rel(t, 0.35 + 0.06 * j, 0.95)
        if 0 < w < 1:
            g2, h2 = cheio(T, poe(GOTA, 0.38 + 0.03 * j, 0.05 + 0.4 * w * w, 0.025), (1 - w) * 1.1)
            G, H = G + g2, H + h2
    G += particulas(T, t, 0.4, 1.0, 10, 69, 0.45, 0.0, 0.12, 0.3, 0.013)
    return G * env, H * env


def _olhos(T, cx, cy, s, k):
    G, H = 0.0, 0.0
    for lado in (-1, 1):
        pts = [(-1, 0), (-0.4, -0.45), (0.4, -0.45), (1, 0), (0.4, 0.45), (-0.4, 0.45)]
        g, h = icone(T, poe(pts, cx + lado * s * 1.4, cy, s), k, 0.6)
        G, H = G + g, H + h
        H = H + T.gauss(cx + lado * s * 1.4, cy, s * 0.25) * k * 2.0
    return G, H


def olhar_de_pedra(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    a = surge(t, 0.0, 0.25) * (1 - rel(t, 0.7, 0.85))
    if a > 0:
        g, h = _olhos(T, -0.55, -0.15, 0.07 * a, 1.2)
        G, H = G + g, H + h
        G += T.gauss(-0.55, -0.15, 0.2) * a * 0.3
    u = rel(t, 0.22, 0.42)
    k = 1 - rel(t, 0.6, 0.72)
    if u > 0 and k > 0:
        e = min(1.0, ease_in(u) * 1.2)
        for lado in (-1, 1):
            x0 = -0.55 + lado * 0.1
            G += T.tapered([(x0, -0.15, x0 + (0.45 - x0) * e, -0.15 + 0.15 * e, 1.0)], 0.035) * k * 0.9
            H += T.lines([(x0, -0.15, x0 + (0.45 - x0) * e, -0.15 + 0.15 * e, 1.0)], 0.006) * k
    pedra = ease_out(rel(t, 0.4, 0.65), 2)
    kk = 1 - rel(t, 0.88, 1)
    if pedra > 0 and kk > 0:
        topo = 0.3 - 0.55 * pedra
        G += T.polys([([(0.3, 0.3), (0.6, 0.3), (0.62, topo + 0.05), (0.52, topo), (0.38, topo + 0.03), (0.28, topo + 0.08)], 1.0)], 0.01) * kk * 0.5
        for j in range(4):
            y = 0.25 - 0.13 * j
            if y > topo:
                G += _zap(T, 70 + j, 0.32, y, 0.58, y - 0.03, 0.007, 3, 0.25) * kk * 1.2
    g2, h2 = clarao(T, t, 0.4, 0.6, 0.45, 0.0, 0.9, 1.0)
    return (G + g2) * env, (H + h2) * env


def medusa_preparo(T, t, rng):
    G, H = vazio(T)
    for j in range(7):
        a = math.pi + math.pi * (j + 0.5) / 7
        x1, y1 = 0.35 * math.cos(a), -0.05 + 0.3 * math.sin(a)
        G += _serpente(T, 0.0, -0.05, x1, y1, t, 0.016, 1.1, 0.04, j * 1.3)
    pisca = 1.0 if (t * 2) % 1 < 0.85 else 0.15
    g, h = _olhos(T, 0.0, 0.05, 0.05, pisca * 1.2)
    G, H = G + g, H + h
    return G, H


def petrificacao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    a = surge(t, 0.0, 0.25) * (1 - rel(t, 0.65, 0.8))
    if a > 0:
        g, h = _olhos(T, 0.0, -0.55, 0.09 * a, 1.3)
        G, H = G + g, H + h
        G += T.gauss(0.0, -0.55, 0.3) * a * 0.35
    varre = rel(t, 0.2, 0.5)
    k = 1 - rel(t, 0.55, 0.65)
    if 0 < varre and k > 0:
        x = -0.7 + 1.4 * varre
        G += T.polys([([(-0.1, -0.55), (0.1, -0.55), (x + 0.15, 0.1), (x - 0.15, 0.1)], 1.0)], 0.05) * k * 0.4
    kk = 1 - rel(t, 0.88, 1)
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        pedra = ease_out(rel(t, 0.3 + 0.1 * i, 0.55 + 0.1 * i), 2)
        if pedra > 0 and kk > 0:
            topo = 0.3 - 0.45 * pedra
            G += T.polys([([(cx - 0.13, 0.3), (cx + 0.13, 0.3), (cx + 0.14, topo + 0.05), (cx + 0.05, topo), (cx - 0.07, topo + 0.03), (cx - 0.15, topo + 0.07)], 1.0)], 0.01) * kk * 0.5
            for j in range(3):
                y = 0.22 - 0.12 * j
                if y > topo:
                    G += _zap(T, 80 + 3 * i + j, cx - 0.12, y, cx + 0.12, y - 0.03, 0.007, 3, 0.25) * kk * 1.2
        g2, h2 = clarao(T, t, 0.5 + 0.1 * i, 0.68 + 0.1 * i, cx, 0.0, 0.4, 0.8)
        G, H = G + g2, H + h2
    return G * env, H * env


# ------------------------------------------------------------------ Cronos

def _foice(T, px, py, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    hx, hy = px + c * s, py + sn * s
    G = T.lines([(px, py, hx, hy, 1.0)], s * 0.035) * k * 1.2
    G += T.arc_band(s * 0.42, s * 0.07, ang + math.pi / 2 + 0.2, ang + math.pi * 1.15, 1.0, 0, hx, hy, 1.0) * k * 1.2
    return G


def foice_do_tempo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.33), 1.6)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        ang = -2.4 + 2.6 * u
        G += _foice(T, 0.0, 0.25, ang, 0.55, k)
        if 0 < u < 1:
            for m in range(3):
                G += T.arc_band(0.75, 0.04, ang - 1.0 - 0.15 * m, ang - 0.15 * m, 1.0, 0, 0.0, 0.25, 1.0) * k * (0.6 - 0.15 * m)
    g, h = corte(T, t, 0.3, 0.55, -0.2, 1.3, 0.09, 0.45, 0.0, 0.25)
    G, H = G + g * 1.2, H + h
    g2, h2 = clarao(T, t, 0.33, 0.55, 0.45, 0.0, 1.0)
    G, H = G + g2, H + h2
    m = pulso(t, 0.45, 1.0)
    if m > 0:
        g3, h3 = _relogio(T, 0.45, -0.32, 0.15, m, -math.pi / 2 + t * 0.6, -math.pi / 2 + t * 2)
        G, H = G + g3, H + h3
    return G * env, H * env


def atraso_de_cronos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.05, 0.3) * (1 - rel(t, 0.85, 0.97))
    volta = ease_out(rel(t, 0.3, 0.8), 2)
    if s > 0:
        g, h = _relogio(T, 0.45, -0.05, 0.22 * s, 1.0, -math.pi / 2 + 1.5 - 1.5 * volta, -math.pi / 2 + 4.0 - TAU * 1.2 * volta)
        G, H = G + g, H + h
    if 0.3 < t < 0.85:
        for m in range(3):
            a0 = -math.pi / 2 - 0.4 * m - t * 6
            G += T.arc_band(0.3 + 0.04 * m, 0.012, a0 - 1.0, a0, 1.0, 0, 0.45, -0.05, 1.0) * 0.9
    G += converge(T, t, 0.0, 0.3, 10, 71, 0.45, -0.05, 0.4, 0.008)
    return G * env, H * env


def cronos_preparo(T, t, rng):
    G, H = vazio(T)
    g, h = icone(T, poe(AMPULHETA, 0.0, 0.0, 0.18, t * math.pi), 1.1, 0.4)
    G, H = G + g, H + h
    for lado, r, vel in ((-1, 0.14, 1.0), (1, 0.1, -1.4)):
        g2, h2 = icone(T, poe(engrenagem(8, 1.0, 0.75), lado * 0.32, 0.15, r, t * vel * 3), 0.9, 0.3)
        G, H = G + g2, H + h2
    q = (t * 2) % 1
    H += T.gauss(0.0, -0.1 + 0.2 * q, 0.012) * 1.5
    return G, H


def era_de_ouro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.82, 0.95))
    corre = ease_in(rel(t, 0.25, 0.85), 1.4)
    if s > 0:
        g, h = _relogio(T, 0.0, -0.4, 0.3 * s, 1.0, -math.pi / 2 + TAU * corre, -math.pi / 2 + TAU * 6 * corre)
        G, H = G + g, H + h
        G += T.gauss(0.0, -0.4, 0.45 * s) * 0.2
    for i, cx in enumerate((-0.55, 0.0, 0.55)):
        w = rel(t, 0.4 + 0.06 * i, 0.95)
        if 0 < w < 1:
            G += T.ring(0.1 + 0.05 * w, 0.012, cx, 0.25, 3.0) * (1 - w) * 1.3
            for m in range(3):
                x0 = cx - 0.25 + 0.5 * ((w * 2 + m / 3) % 1)
                G += T.lines([(x0 - 0.06, 0.1 + 0.05 * m, x0, 0.1 + 0.05 * m, 1.0)], 0.007) * (1 - w) * 1.3
    G += particulas(T, t, 0.3, 1.0, 18, 72, 0.0, -0.1, 0.7, 0.4, 0.011)
    return G * env, H * env


# ------------------------------------------------------------------ Hércules

def _clava(T, px, py, ang, s, k):
    c, sn = math.cos(ang), math.sin(ang)
    pts = []
    for u, w in ((0, 0.05), (0.4, 0.07), (0.75, 0.13), (1.0, 0.11)):
        pts.append((u, w))
    poly = [(px + c * s * u - sn * s * w, py + sn * s * u + c * s * w) for u, w in pts] + \
           [(px + c * s * u + sn * s * w, py + sn * s * u - c * s * w) for u, w in reversed(pts)]
    g, h = icone(T, poly, k * 1.1, 0.5)
    for j in range(3):
        u = 0.55 + 0.15 * j
        g = g + T.gauss(px + c * s * u + sn * s * 0.1 * (1 if j % 2 else -1), py + sn * s * u - c * s * 0.1 * (1 if j % 2 else -1), s * 0.025) * k * 1.3
    return g, h


def clava_de_hercules(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    u = ease_in(rel(t, 0.0, 0.35), 2.2)
    k = 1 - rel(t, 0.5, 0.62)
    if k > 0:
        ang = -2.2 + 1.85 * u
        g, h = _clava(T, -0.1, 0.35, ang, 0.65, k)
        G, H = G + g, H + h
        hx, hy = -0.1 + 0.6 * math.cos(ang), 0.35 + 0.6 * math.sin(ang)
        for m in range(3):
            g2, h2 = icone(T, poe(CHAMA, hx + 0.05 * (m - 1), hy - 0.05, 0.06 + 0.01 * math.sin(t * 30 + m), 0.0), k * 1.1, 0.7)
            G, H = G + g2, H + h2
    g3, h3 = clarao(T, t, 0.33, 0.55, 0.45, 0.1, 1.4, 1.4)
    G, H = G + g3, H + h3
    G += onda_no_chao(T, t, 0.33, 0.85, 0.8, 0.35, 1.5)
    G += estouro(T, t, 0.35, 0.85, 14, 73, 0.45, 0.1, 0.5, 0.014)
    G += particulas(T, t, 0.35, 0.95, 14, 74, 0.45, 0.0, 0.2, 0.5, 0.013)
    return G * env, H * env


_LEAO = [(-0.7, 0.2), (-0.8, -0.3), (-0.55, -0.75), (0.0, -0.95), (0.55, -0.75), (0.8, -0.3), (0.7, 0.2), (0.4, 0.55), (0.0, 0.7),
         (-0.4, 0.55)]


def desafio_de_hercules(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = surge(t, 0.0, 0.25) * (1 - rel(t, 0.82, 0.95))
    if s > 0:
        g, h = icone(T, poe(_LEAO, -0.55, -0.25, 0.16 * s), 1.1, 0.35)
        G, H = G + g, H + h
        for lado in (-1, 1):
            H += T.gauss(-0.55 + lado * 0.05, -0.27, 0.012) * s * 2.0
        P, nos = _punho(T, -0.55, -0.55 - 0.05 * s, 1.0 * s, -math.pi / 2)
        G += P * 0.9
        H += nos * 0.4
    for j in range(4):
        u = rel(t, 0.15 + 0.08 * j, 0.6 + 0.08 * j)
        if 0 < u < 1:
            G += T.arc_band(0.15 + 1.1 * u, 0.045 * (1 - 0.5 * u), -0.55, 0.55, 0.7, 0, -0.55, -0.05, 0.0) * (1 - u) * 1.3
    for i, cx in enumerate((0.0, 0.55)):
        m = surge(t, 0.45 + 0.06 * i, 0.62 + 0.06 * i) * (1 - rel(t, 0.88, 1))
        if m > 0:
            for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
                x, y = cx + 0.06 * math.cos(a + math.pi / 4), -0.3 + 0.06 * math.sin(a + math.pi / 4)
                G += T.arc_band(0.05 * m, 0.014, a + 0.4, a + 1.2, 1.0, 0, x, y, 0.0) * 1.3
    k2 = pulso(t, 0.3, 1.0)
    G += T.gauss(-0.55, 0.0, 0.3, 0.35) * k2 * 0.4
    G += T.ring(0.3, 0.015, -0.55, 0.0, 1.0) * k2 * 1.0
    return G * env, H * env


def hercules_preparo(T, t, rng):
    G, H = vazio(T)
    b = 0.5 + 0.5 * math.sin(t * TAU * 2)
    for lado in (-1, 1):
        P, nos = _punho(T, lado * 0.32, -0.1, 1.2, -math.pi / 2)
        G += P * 0.9
        H += nos * 0.3
        G += T.gauss(lado * 0.25, 0.05, 0.1, 0.07) * (0.5 + 0.4 * b)
    G += T.gauss(0.0, 0.0, 0.3, 0.35) * (0.25 + 0.2 * b)
    G += T.ring(0.15 + 0.3 * ((t * 2) % 1), 0.02, 0.0, 0.4, 3.0) * (1 - (t * 2) % 1) * 1.2
    q = np.random.default_rng(int(t * 8))
    for _ in range(4):
        x = q.uniform(-0.4, 0.4)
        G += T.gauss(x, 0.38 - q.uniform(0, 0.1), 0.012) * 1.2
    return G, H


def forca_de_semideus(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    c = pulso(t, 0.0, 0.4)
    G += T.gauss(-0.45, 0.0, 0.3, 0.35) * c * 0.5
    G += converge(T, t, 0.0, 0.3, 12, 75, -0.45, 0.0, 0.45, 0.009)
    u = ease_in(rel(t, 0.25, 0.42), 2)
    k = 1 - rel(t, 0.55, 0.65)
    if u > 0 and k > 0:
        P, nos = _punho(T, -0.3 + 0.6 * u, 0.0, 3.0, 0)
        G += P * k
        H += nos * 0.5 * k
        for m in range(3):
            G += T.tapered([(-0.8, -0.15 + 0.15 * m, -0.3 + 0.6 * u - 0.15, -0.15 + 0.15 * m, 0.8)], 0.025) * k
    g, h = clarao(T, t, 0.4, 0.7, 0.45, 0.0, 2.0, 1.8)
    G, H = G + g, H + h
    G += anel(T, t, 0.42, 0.85, 0.05, 0.8, 0.05, 0.0, 1.0, 1.5)
    G += anel(T, t, 0.48, 0.92, 0.05, 1.0, 0.03, 0.0, 1.0, 1.1)
    G += onda_no_chao(T, t, 0.42, 0.95, 1.0, 0.38, 1.6)
    G += estouro(T, t, 0.42, 0.9, 20, 76, 0.45, 0.0, 0.8, 0.015)
    return G * env, H * env


REGISTRO = [
    ("flecha_de_prata", flecha_de_prata, GRANDE, "Ártemis · a flecha de prata e a mira da lua", False),
    ("cervo_sagrado", cervo_sagrado, GRANDE, "Ártemis · o cervo de luz saltando", False),
    ("artemis_preparo", artemis_preparo, MEDIA, "Ártemis · a lua e o arco puxado (Preparo, laço)", True),
    ("cacada_da_lua", cacada_da_lua, GRANDE, "Ártemis · a lua cheia e o feixe de luar", False),
    ("caduceu", caduceu, GRANDE, "Hermes · o caduceu e a tontura", False),
    ("mensagem_dos_deuses", mensagem_dos_deuses, GRANDE, "Hermes · o pergaminho alado e as penas", False),
    ("roubo_divino", roubo_divino, GRANDE, "Hermes · o vulto alado levando os buffs", False),
    ("encanto_de_afrodite", encanto_de_afrodite, GRANDE, "Afrodite · os corações rodando nos rivais", False),
    ("abraco_do_amor", abraco_do_amor, GRANDE, "Afrodite · a concha e as pétalas", False),
    ("afrodite_preparo", afrodite_preparo, MEDIA, "Afrodite · o coração pulsando (Preparo, laço)", True),
    ("desejo", desejo, GRANDE, "Afrodite · o coração gigante rachando", False),
    ("mordida_de_serpente", mordida_de_serpente, GRANDE, "Medusa · o bote das serpentes", False),
    ("olhar_de_pedra", olhar_de_pedra, GRANDE, "Medusa · o olhar que vira pedra", False),
    ("medusa_preparo", medusa_preparo, MEDIA, "Medusa · as serpentes agitadas (Preparo, laço)", True),
    ("petrificacao", petrificacao, GRANDE, "Medusa · a pedra subindo em todos", False),
    ("foice_do_tempo", foice_do_tempo, GRANDE, "Cronos · a foice e o relógio", False),
    ("atraso_de_cronos", atraso_de_cronos, GRANDE, "Cronos · os ponteiros voltando", False),
    ("cronos_preparo", cronos_preparo, MEDIA, "Cronos · a ampulheta e as engrenagens (Preparo, laço)", True),
    ("era_de_ouro", era_de_ouro, GRANDE, "Cronos · o relógio dourado correndo", False),
    ("clava_de_hercules", clava_de_hercules, GRANDE, "Hércules · a clava em chamas", False),
    ("desafio_de_hercules", desafio_de_hercules, GRANDE, "Hércules · a pele de leão e o desafio", False),
    ("hercules_preparo", hercules_preparo, MEDIA, "Hércules · os músculos acendendo (Preparo, laço)", True),
    ("forca_de_semideus", forca_de_semideus, GRANDE, "Hércules · o soco de semideus", False),
]
