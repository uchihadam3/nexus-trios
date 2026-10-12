"""Rodada 1 das Mecânicas únicas ativando como habilidade: Goku, Vegeta, Naruto, Sasuke, Luffy, Gojo, Pikachu,
Saitama, Wolverine, Batman, Superman, Homem-Aranha e Hulk.

- genki_dama: a esfera azul enorme desce do alto, crescendo, com a energia sendo sugada para ela, e explode no rival.
- zenkai: a aura dourada do Saiyajin explode em volta, os raios sobem e a cura verde pulsa (Zenkai!).
- kage_bunshin: as nuvens de fumaça "puf" e as duas silhuetas de clone surgem dos lados.
- sharingan: o olho vermelho com as três vírgulas gira, para e brilha ("Já vi essa").
- borracha: o corpo de borracha estica — os anéis elásticos que esticam e voltam, com as ondas de impacto.
- vazio_infinito: o domínio — o espaço vira um céu de estrelas, o anel do vazio se abre e tudo para.
- bochechas: as bochechas elétricas — os dois círculos de faísca e os raios que pulam em volta.
- tedio: o tédio do herói — as bolhas do bocejo e o "…" flutuando, a energia baixa.
- modo_serio: o soco sério — o clarão, a onda de choque gigante e as rachaduras de luz.
- garras_regeneram: as três garras cortam em X e as células verdes fecham as feridas.
- gancho: o gancho voa preso à corda e o escudo de couro do morcego fecha no aliado.
- bomba_de_fumaca: a bomba cai e a nuvem de fumaça cinza se espalha em volta.
- batarangue: o batarangue gira no ar e acerta o rival.
- sopro_congelante: o sopro gelado — a rajada azul que varre, os flocos e o gelo que estala.
- teia: a teia se abre em rede em volta do aliado, presa nos fios.
- cada_vez_maior: a fúria do Hulk — as ondas verdes de raiva, as rachaduras e o corpo crescendo.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .basicos_a import _punho
from .rodada13 import _borda, _gira


def genki_dama(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    desce = ease_in(rel(t, 0.0, 0.45), 1.6)
    if t < 0.5:
        y = -0.75 + 0.75 * desce
        r = 0.16 + 0.1 * desce
        G += T.gauss(0, y, r) * 1.4 + T.ring(r * 1.05, 0.025, 0, y) * 1.2
        H += T.gauss(0, y, r * 0.55) * 1.8
        q = np.random.default_rng(int(t * 30) % 9 + 1)
        segs = []
        for _ in range(14):
            a = q.uniform(0, TAU)
            d0, d1 = r * 3.2, r * 1.3
            segs.append((d0 * math.cos(a), y + d0 * math.sin(a), d1 * math.cos(a), y + d1 * math.sin(a), 1.0))
        G += T.tapered(segs, 0.014) * 0.9
    bum = rel(t, 0.45, 0.95)
    if bum > 0:
        g = ease_out(bum, 2.5)
        G += T.gauss(0, 0, 0.18 + 0.4 * g) * (1 - bum) * 1.6 + T.ring(0.12 + 0.62 * g, 0.045, 0, 0) * (1 - bum) * 1.4
        H += T.gauss(0, 0, 0.1 + 0.18 * g) * (1 - bum) * 2.0
        G += (T.flare(0, 0, 0.9 * (1 - bum) + 0.02, 0, 0.012) + T.flare(0, 0, 0.6 * (1 - bum) + 0.02, math.pi / 4, 0.012)) * 1.2
    return G * env, H * env


def zenkai(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sobe = ease_out(rel(t, 0.0, 0.3), 2.5)
    if sobe > 0:
        # a aura em chama: lâminas que sobem em volta
        for k in range(10):
            x = -0.32 + 0.064 * k + 0.02 * math.sin(t * 30 + k)
            alt = (0.45 + 0.2 * math.sin(k * 1.7 + t * 18)) * sobe
            G += T.polys([(lamina(x, 0.35, x + 0.03 * math.sin(k), 0.35 - alt, 0.045), 1.0)]) * 0.8
        G += T.gauss(0, 0.05, 0.3, 0.42) * sobe * 0.4
        H += T.gauss(0, 0.05, 0.1, 0.18) * sobe * 0.9
    raios = pulso(t, 0.1, 0.8)
    if raios > 0:
        q = np.random.default_rng(int(t * 22) % 7 + 3)
        for _ in range(3):
            x = q.uniform(-0.35, 0.35)
            G += T.polyline(jagged(q, x, 0.35, x + q.uniform(-0.1, 0.1), -0.45, 4, 0.25), 0.01) * raios * 1.3
    cura = pulso(t, 0.35, 0.95)
    if cura > 0:
        for k in range(5):
            y = 0.3 - 0.6 * ((t * 1.5 + k * 0.2) % 1)
            x = -0.25 + 0.12 * k
            G += T.lines([(x - 0.035, y, x + 0.035, y, 1.0), (x, y - 0.035, x, y + 0.035, 1.0)], 0.014) * cura
    return G * env, H * env


def _silhueta(cx, cy, s):
    """Uma silhueta de ninja (cabeça, tronco, braços e pernas)."""
    return [(cx - 0.05 * s, cy - 0.28 * s), (cx + 0.05 * s, cy - 0.28 * s), (cx + 0.06 * s, cy - 0.18 * s), (cx + 0.16 * s, cy - 0.1 * s),
            (cx + 0.14 * s, cy - 0.04 * s), (cx + 0.07 * s, cy - 0.08 * s), (cx + 0.08 * s, cy + 0.1 * s), (cx + 0.12 * s, cy + 0.3 * s),
            (cx + 0.05 * s, cy + 0.3 * s), (cx, cy + 0.14 * s), (cx - 0.05 * s, cy + 0.3 * s), (cx - 0.12 * s, cy + 0.3 * s),
            (cx - 0.08 * s, cy + 0.1 * s), (cx - 0.07 * s, cy - 0.08 * s), (cx - 0.14 * s, cy - 0.04 * s), (cx - 0.16 * s, cy - 0.1 * s),
            (cx - 0.06 * s, cy - 0.18 * s)]


def kage_bunshin(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k, x in enumerate((-0.48, 0.48)):
        puf = rel(t, 0.0 + 0.12 * k, 0.5 + 0.12 * k)
        if 0 < puf < 1:
            q = np.random.default_rng(7 + k)
            pts = [(x + q.normal(0, 0.06 + 0.12 * puf), q.normal(0, 0.06 + 0.12 * puf), (1 - puf) * q.uniform(0.5, 1)) for _ in range(30)]
            G += T.splats(pts, 0.05 + 0.03 * puf) * 0.9
        aparece = rel(t, 0.2 + 0.12 * k, 0.45 + 0.12 * k)
        if aparece > 0:
            S = T.polys([(_silhueta(x, 0.02, 1.25), 1.0)])
            G += (S * 0.35 + _borda(T, S, 0.007) * 1.2) * aparece * (1 - rel(t, 0.85, 0.98))
            H += _borda(T, S, 0.005) * aparece * 0.4
    return G * env, H * env


def sharingan(T, t, rng):
    """O Sharingan: o olho vermelho abre, as três vírgulas giram rápido, desaceleram e param, e o olho brilha."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.25), 3)
    if abre > 0:
        r = 0.4 * abre
        G += T.ring(r, 0.035, 0, 0) * 1.4 + T.gauss(0, 0, r * 0.85) * 0.3
        G += T.ring(r * 0.55, 0.012, 0, 0) * 0.9
        H += T.gauss(0, 0, r * 0.16) * 1.4
        gira = TAU * 2.5 * (1 - (1 - min(1, t / 0.7)) ** 3)
        shapes = []
        for k in range(3):
            a = gira + TAU * k / 3
            cx, cy = r * 0.55 * math.cos(a), r * 0.55 * math.sin(a)
            # a vírgula: a cabeça redonda e a cauda curva que segue o giro
            cabeca = [(cx + r * 0.14 * math.cos(j * TAU / 14), cy + r * 0.14 * math.sin(j * TAU / 14)) for j in range(14)]
            cauda = []
            for j in range(8):
                u = j / 7
                aa = a - 0.9 * u
                rr = r * (0.55 + 0.12 * u)
                cauda.append((rr * math.cos(aa) + r * 0.1 * (1 - u) * math.cos(aa + math.pi / 2), rr * math.sin(aa) + r * 0.1 * (1 - u) * math.sin(aa + math.pi / 2)))
            for j in range(7, -1, -1):
                u = j / 7
                aa = a - 0.9 * u
                rr = r * (0.55 + 0.12 * u)
                cauda.append((rr * math.cos(aa) - r * 0.03 * (1 - u) * math.cos(aa + math.pi / 2), rr * math.sin(aa) - r * 0.03 * (1 - u) * math.sin(aa + math.pi / 2)))
            shapes += [(cabeca, 1.0), (cauda, 1.0)]
        P = T.polys(shapes)
        G += P * 1.3
        H += P * 0.5
    brilha = pulso(t, 0.6, 0.95)
    G += T.flare(0, 0, 0.6 * brilha + 0.01, 0.3, 0.015) * brilha * 1.2
    return G * env, H * env


def borracha(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k in range(3):
        u = rel(t, 0.05 * k, 0.5 + 0.05 * k)
        if 0 < u < 1:
            # o anel que estica (achata para os lados) e volta, como borracha
            estica = 1 + 0.9 * math.sin(math.pi * u) * math.cos(u * 8)
            G += T.ring(0.18 + 0.1 * k, 0.025, 0, 0.05, 1.0 / max(0.4, estica)) * (1 - u) * 1.2
    volta = pulso(t, 0.35, 0.8)
    if volta > 0:
        for lado in (-1, 1):
            x = lado * (0.2 + 0.4 * rel(t, 0.35, 0.8))
            G += T.ring(0.08, 0.018, x, 0.05, 0.6) * volta + T.tapered([(lado * 0.1, 0.05, x, 0.05, 1.0)], 0.03) * volta * 0.7
    H += T.gauss(0, 0.05, 0.06) * pulso(t, 0.0, 0.35) * 1.2
    return G * env, H * env


def vazio_infinito(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.4), 2.5)
    if abre > 0:
        r = 0.85 * abre
        q = np.random.default_rng(31)
        pts = []
        for _ in range(90):
            a, d = q.uniform(0, TAU), r * math.sqrt(q.uniform(0, 1))
            pts.append((d * math.cos(a), d * math.sin(a), q.uniform(0.3, 1) * (0.6 + 0.4 * math.sin(t * 20 + a * 5))))
        H += T.splats(pts, 0.008) * 1.2
        G += T.ring(r, 0.04, 0, 0) * 1.3 + T.ring(r * 0.94, 0.012, 0, 0) * 0.8
        G += T.gauss(0, 0, 0.12) * 0.6 + T.ring(0.1, 0.015, 0, 0) * 0.9
    para = pulso(t, 0.45, 1.0)
    if para > 0:
        G += T.arc_band(0.5, 0.02, -math.pi / 2, -math.pi / 2 + TAU * 0.98, cx=0, cy=0, taper=0.0) * para * 0.6
    return G * env, H * env


def bochechas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for lado in (-1, 1):
        cx = lado * 0.28
        acende = pulso(t, 0.0, 0.9) * (0.7 + 0.3 * math.sin(t * 40 + lado))
        G += T.gauss(cx, 0.08, 0.11) * acende * 1.5 + T.ring(0.13, 0.02, cx, 0.08) * acende * 1.2
        H += T.gauss(cx, 0.08, 0.055) * acende * 1.8
    q = np.random.default_rng(int(t * 24) % 9 + 1)
    for k in range(4):
        if pulso(t, 0.1 + 0.1 * k, 0.4 + 0.1 * k) > 0:
            a = q.uniform(0, TAU)
            G += T.polyline(jagged(q, 0.22 * (-1 if k % 2 else 1), 0.08, 0.5 * math.cos(a), 0.5 * math.sin(a), 4, 0.35), 0.01) * 1.3
    return G * env, H * env


def tedio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    for k in range(3):
        u = rel(t, 0.1 + 0.15 * k, 0.75 + 0.1 * k)
        if 0 < u < 1:
            x = 0.12 + 0.12 * k + 0.03 * math.sin(u * 6)
            y = -0.15 - 0.45 * u
            G += T.ring(0.05 + 0.03 * k + 0.03 * u, 0.014, x, y) * (1 - u) * 1.3
    pontos = rel(t, 0.15, 0.5)
    for k in range(3):
        if pontos * 3 > k:
            G += T.gauss(-0.22 + 0.14 * k, -0.42, 0.035) * (1 - rel(t, 0.8, 0.98)) * 1.4
    gota = rel(t, 0.3, 0.9)
    if 0 < gota < 1:
        y = -0.15 + 0.25 * gota
        G += T.polys([([(0.32, y - 0.08), (0.36, y), (0.32, y + 0.04), (0.28, y)], 1.0)]) * (1 - gota) * 1.2
    G += T.ring(0.38, 0.01, 0, 0.05) * pulso(t, 0.0, 0.6) * 0.5
    return G * env, H * env


def modo_serio(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    H += T.gauss(0, 0, 0.15) * pulso(t, 0.0, 0.2) * 2.5
    clarao = pulso(t, 0.0, 0.35)
    G += (T.flare(0, 0, 1.1 * clarao + 0.01, 0, 0.01) + T.flare(0, 0, 0.7 * clarao + 0.01, math.pi / 4, 0.01)) * clarao * 1.4
    linhas = pulso(t, 0.0, 0.3)
    if linhas > 0:
        G += T.tapered([(-0.9, dy, -0.05, dy * 0.2, 0.8) for dy in (-0.18, -0.09, 0.0, 0.09, 0.18)], 0.03) * linhas
    onda = rel(t, 0.1, 0.8)
    if 0 < onda < 1:
        g = ease_out(onda, 2.2)
        G += T.ring(0.1 + 0.85 * g, 0.05, 0, 0) * (1 - onda) * 1.6 + T.ring(0.06 + 0.6 * g, 0.02, 0, 0) * (1 - onda)
        q = np.random.default_rng(17)
        for k in range(8):
            a = TAU * k / 8 + 0.2
            G += T.polyline(jagged(q, 0.08 * math.cos(a), 0.08 * math.sin(a), (0.2 + 0.5 * g) * math.cos(a), (0.2 + 0.5 * g) * math.sin(a), 3, 0.3), 0.01) * (1 - onda) * 1.2
    return G * env, H * env


def garras_regeneram(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k, a in enumerate((0.75, -0.75)):
        u = rel(t, 0.08 * k, 0.18 + 0.08 * k)
        if u > 0:
            b = 1 - rel(t, 0.3, 0.5)
            for j in (-1, 0, 1):
                c, s = math.cos(a), math.sin(a)
                ox, oy = -s * 0.06 * j, c * 0.06 * j
                G += T.polys([(lamina(-0.4 * c + ox, -0.4 * s + oy, 0.4 * c + ox, 0.4 * s + oy, 0.018, u), 1.0)]) * b * 1.3
    cura = pulso(t, 0.35, 1.0)
    if cura > 0:
        q = np.random.default_rng(5)
        pts = [(q.uniform(-0.3, 0.3), q.uniform(-0.3, 0.3) - 0.2 * rel(t, 0.35, 1.0), q.uniform(0.5, 1)) for _ in range(26)]
        G += T.splats(pts, 0.03) * cura * 0.9
        H += T.splats(pts, 0.012) * cura * 0.8
    return G * env, H * env


def _morcego(cx, cy, s, ang=0.0):
    pts = [(-0.3, 0.0), (-0.2, -0.08), (-0.12, -0.02), (-0.05, -0.1), (-0.03, -0.04), (0.0, -0.06), (0.03, -0.04), (0.05, -0.1),
           (0.12, -0.02), (0.2, -0.08), (0.3, 0.0), (0.18, 0.02), (0.12, 0.08), (0.05, 0.04), (0.0, 0.1), (-0.05, 0.04), (-0.12, 0.08), (-0.18, 0.02)]
    return _gira([(x * s, y * s) for x, y in pts], ang, cx, cy)


def gancho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    voa = rel(t, 0.0, 0.3)
    if t < 0.6:
        x, y = -0.85 + 0.85 * ease_out(voa, 2), -0.6 + 0.6 * ease_out(voa, 2)
        G += T.lines([(-0.9, -0.65, x, y, 1.0)], 0.008) * 0.9
        G += T.lines([(x, y, x - 0.06, y - 0.06, 1.0), (x, y, x + 0.02, y - 0.08, 1.0), (x, y, x - 0.08, y + 0.02, 1.0)], 0.012)
    fecha = ease_out(rel(t, 0.3, 0.6), 3)
    if fecha > 0:
        b = 1 - rel(t, 0.85, 0.98)
        G += T.ring(0.38 * fecha, 0.03, 0, 0.05) * b * 1.2
        M = T.polys([(_morcego(0, -0.3, 0.9 * fecha), 1.0)])
        G += (M * 0.5 + _borda(T, M, 0.006) * 1.2) * b
    return G * env, H * env


def bomba_de_fumaca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    cai = rel(t, 0.0, 0.2)
    if cai < 1:
        y = -0.6 + 0.6 * ease_in(cai, 2)
        G += T.gauss(0, y, 0.035) * 1.3
    bum = rel(t, 0.2, 1.0)
    if bum > 0:
        H += T.gauss(0, 0, 0.06) * pulso(t, 0.2, 0.35) * 2
        q = np.random.default_rng(13)
        pts = []
        for _ in range(60):
            a = q.uniform(0, TAU)
            d = q.uniform(0.1, 1) * (0.15 + 0.6 * ease_out(bum, 2))
            pts.append((d * math.cos(a), d * math.sin(a) * 0.7 - 0.1 * bum, q.uniform(0.4, 1) * (1 - bum ** 2)))
        G += T.splats(pts, 0.06 + 0.04 * bum) * 0.8
    return G * env, H * env


def batarangue(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    voa = rel(t, 0.0, 0.35)
    if voa < 1:
        x = -0.85 + 0.85 * ease_in(voa, 1.2)
        y = -0.15 * math.sin(math.pi * voa)
        M = T.polys([(_morcego(x, y, 1.0, t * 40), 1.0)])
        G += M * 0.8 + _borda(T, M, 0.005)
        G += T.arc_band(0.1, 0.02, t * 40, t * 40 + 2.5, cx=x, cy=y, taper=1.0) * 0.6
    bate = rel(t, 0.35, 0.75)
    if bate > 0:
        G += T.flare(0, 0, 0.35 * (1 - bate) + 0.02, 0.4, 0.02) * (1 - bate) * 1.5 + T.ring(0.05 + 0.3 * ease_out(bate, 3), 0.02, 0, 0) * (1 - bate)
        H += T.gauss(0, 0, 0.04) * (1 - bate) * 1.8
    return G * env, H * env


def sopro_congelante(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sopra = rel(t, 0.0, 0.6)
    if sopra > 0:
        b = 1 - rel(t, 0.55, 0.8)
        alc = 0.95 * ease_out(sopra, 2)
        for k in range(7):
            dy = (k - 3) * 0.035
            G += T.tapered([(-0.9, dy * 0.3, -0.9 + alc, dy * 3, 1.0)], 0.04) * b * 0.7
        q = np.random.default_rng(int(t * 16) % 7)
        segs = []
        for _ in range(10):
            x, y = -0.9 + alc * q.uniform(0.3, 1), q.uniform(-0.25, 0.25) * alc
            segs += [(x - 0.025, y, x + 0.025, y, 1.0), (x, y - 0.025, x, y + 0.025, 1.0), (x - 0.018, y - 0.018, x + 0.018, y + 0.018, 1.0)]
        H += T.lines(segs, 0.006) * b * 1.3
    gelo = pulso(t, 0.5, 1.0)
    if gelo > 0:
        shapes = [(estrela(x, 0.25, 0.08, 0.3, 6, 0.35), 1.0) for x in (-0.4, 0.0, 0.4)]
        P = T.polys(shapes)
        G += (P * 0.4 + _borda(T, P, 0.006)) * gelo
    return G * env, H * env


def teia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = ease_out(rel(t, 0.0, 0.4), 3)
    if abre > 0:
        r = 0.45 * abre
        segs = []
        for k in range(10):
            a = TAU * k / 10
            segs.append((0, 0, r * math.cos(a), r * math.sin(a), 1.0))
        for j in range(1, 5):
            rr = r * j / 4
            for k in range(10):
                a0, a1 = TAU * k / 10, TAU * (k + 1) / 10
                m = (a0 + a1) / 2
                segs.append((rr * math.cos(a0), rr * math.sin(a0), rr * 0.88 * math.cos(m), rr * 0.88 * math.sin(m), 1.0))
                segs.append((rr * 0.88 * math.cos(m), rr * 0.88 * math.sin(m), rr * math.cos(a1), rr * math.sin(a1), 1.0))
        G += T.lines(segs, 0.008) * (1 - rel(t, 0.85, 0.98)) * 1.2
    H += T.gauss(0, 0, 0.05) * pulso(t, 0.3, 0.6) * 1.2
    return G * env, H * env


def cada_vez_maior(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k in range(3):
        u = rel(t, 0.12 * k, 0.6 + 0.12 * k)
        if 0 < u < 1:
            G += T.ring(0.15 + 0.5 * ease_out(u, 2), 0.04, 0, 0.05) * (1 - u) * 1.3
    q = np.random.default_rng(11)
    for k in range(6):
        a = TAU * k / 6 + 0.4
        c = pulso(t, 0.1, 0.8)
        G += T.polyline(jagged(q, 0.12 * math.cos(a), 0.12 * math.sin(a), 0.42 * math.cos(a), 0.42 * math.sin(a), 3, 0.3), 0.012) * c
    H += T.gauss(0, 0.05, 0.12) * pulso(t, 0.0, 0.5) * 1.2
    for x in (-0.3, 0.3):
        y = 0.25 - 0.35 * rel(t, 0.4, 0.9)
        G += T.lines([(x - 0.07, y + 0.06, x, y - 0.01, 1.0), (x + 0.07, y + 0.06, x, y - 0.01, 1.0), (x, y + 0.14, x, y, 1.0)], 0.016) * pulso(t, 0.4, 1.0)
    return G * env, H * env


REGISTRO = [
    ("mu_genki_dama", genki_dama, GRANDE, "Goku · a Genki Dama descendo e explodindo", False),
    ("mu_zenkai", zenkai, GRANDE, "Vegeta · a aura dourada, os raios e a cura do Zenkai", False),
    ("mu_kage_bunshin", kage_bunshin, GRANDE, "Naruto · as nuvens de fumaça e os clones", False),
    ("mu_sharingan", sharingan, GRANDE, "Sasuke · o Sharingan girando", False),
    ("mu_borracha", borracha, GRANDE, "Luffy · os anéis de borracha esticando", False),
    ("mu_vazio_infinito", vazio_infinito, GRANDE, "Gojo · o céu de estrelas do domínio", False),
    ("mu_bochechas", bochechas, GRANDE, "Pikachu · as bochechas elétricas", False),
    ("mu_tedio", tedio, GRANDE, "Saitama · as bolhas do bocejo", False),
    ("mu_modo_serio", modo_serio, GRANDE, "Saitama · o soco sério e a onda gigante", False),
    ("mu_garras_regeneram", garras_regeneram, GRANDE, "Wolverine · as garras em X e a cura", False),
    ("mu_gancho", gancho, GRANDE, "Batman · o gancho e o escudo do morcego", False),
    ("mu_bomba_de_fumaca", bomba_de_fumaca, GRANDE, "Batman · a nuvem de fumaça", False),
    ("mu_batarangue", batarangue, GRANDE, "Batman · o batarangue girando e acertando", False),
    ("mu_sopro_congelante", sopro_congelante, GRANDE, "Superman · o sopro gelado", False),
    ("mu_teia", teia, GRANDE, "Homem-Aranha · a teia em rede", False),
    ("mu_cada_vez_maior", cada_vez_maior, GRANDE, "Hulk · as ondas de fúria e as rachaduras", False),
]
