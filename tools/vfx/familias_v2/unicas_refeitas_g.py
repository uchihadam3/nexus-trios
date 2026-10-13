"""Mecânicas únicas refeitas, lote g: o impacto conta o nome da mecânica.

- mu_tita (King Kong): os punhos batendo no peito e as ondas de choque;
- mu_hienas (Scar): três mordidas de hiena fechando, uma depois da outra;
- mu_presentes (Jack Esqueleto): a caixa de presente abrindo e a espiral da colina;
- mu_orgulho_youkai (Sesshomaru): a lua crescente acendendo e o chicote de luz;
- mu_battojutsu (Kenshin): a bainha, o saque relâmpago e a cicatriz em X;
- mu_anulou (Asta): o círculo mágico partido pela espada negra;
- mu_jogador_solo (Kirito): as duas espadas cruzando e a rajada de estrelas;
- mu_pacifista (Vash): a bala parando no ar e o símbolo da paz;
- mu_plano_mestre (Megamente): os três planos embaralhando e um sendo escolhido;
- mu_escudo_rosa (Steven): o escudo da Rosa abrindo em pétalas;
- mu_suprimentos (Ellie): a caixa de suprimentos com a cruz e as setas de Carga;
- mu_fus_ro_dah (Dovahkiin): as três palavras do grito e as ondas saindo;
- mu_quatro_bracos (Goro): os quatro braços travando o golpe;
- mu_tapa_olho (Kenpachi): o tapa-olho voando e a pressão espiritual explodindo;
- mu_futuro (Trunks): o relógio girando para trás e o portal do tempo;
- mu_previsao (Garnet): o terceiro olho abrindo e as linhas do futuro.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, pulso, rel, vazio
from .unicas_refeitas_d import _contorno, _gira, _maior, _oval


def tita(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    for k in range(4):
        a0 = 0.06 + 0.18 * k
        f = pulso(t, a0, a0 + 0.16)
        s = -1 if k % 2 else 1
        cx = s * (0.2 - 0.08 * f)
        punho = [(cx - 0.1, -0.1), (cx + 0.1, -0.1), (cx + 0.11, 0.08), (cx - 0.11, 0.08)]
        G += T.polys([(punho, 1.0)], 0.01) * (0.45 + 0.7 * f)
        for j in range(4):
            G += T.lines([(cx - 0.08 + 0.055 * j, -0.1, cx - 0.08 + 0.055 * j, -0.02, 1)], 0.008) * -0.4 * (0.45 + 0.7 * f)
        onda = rel(t, a0 + 0.08, a0 + 0.4)
        if 0 < onda < 1:
            G += T.ring(0.15 + 0.4 * onda, 0.03 * (1 - onda) + 0.008) * (1 - onda) * 1.3
        H += T.gauss(s * 0.06, 0, 0.05) * f * 1.6
    return np.clip(G, 0, None) * env, H * env


def _mordida(cx, cy, s, fecha):
    dentes = []
    for k in range(5):
        x = cx - 0.2 * s + 0.1 * s * k
        top = cy - 0.18 * s * (1 - fecha) - 0.02 * s
        bot = cy + 0.18 * s * (1 - fecha) + 0.02 * s
        dentes.append([(x - 0.04 * s, top - 0.06 * s), (x + 0.04 * s, top - 0.06 * s), (x, top + 0.04 * s)])
        dentes.append([(x - 0.04 * s, bot + 0.06 * s), (x + 0.04 * s, bot + 0.06 * s), (x, bot - 0.04 * s)])
    return dentes


def hienas(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for k, (cx, cy) in enumerate(((-0.22, -0.15), (0.2, 0.0), (-0.05, 0.22))):
        a0 = 0.05 + 0.25 * k
        fecha = ease_in(rel(t, a0, a0 + 0.15), 2)
        vis = rel(t, a0 - 0.05, a0) * (1 - rel(t, a0 + 0.25, a0 + 0.4))
        if vis <= 0:
            continue
        G += T.polys([(d, 1.0) for d in _mordida(cx, cy, 0.8, fecha)], 0.003) * vis * 1.2
        H += T.gauss(cx, cy, 0.05) * pulso(t, a0 + 0.12, a0 + 0.25) * 1.8
    return G * env, H * env


def presentes(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    caixa = [(-0.18, 0.0), (0.18, 0.0), (0.18, 0.3), (-0.18, 0.3)]
    G += T.polys([(caixa, 1.0)], 0.004) * 0.35 + _contorno(T, caixa, 0.014)
    G += T.lines([(0, 0.0, 0, 0.3, 1)], 0.02) * 0.9
    abre = ease_out(rel(t, 0.25, 0.55), 2)
    ly = -0.03 - 0.3 * abre
    tampa = _gira([(-0.21, -0.04), (0.21, -0.04), (0.21, 0.03), (-0.21, 0.03)], 0.6 * abre, 0.0, ly)
    G += T.polys([(tampa, 1.0)], 0.004) * 0.9
    for s in (-1, 1):
        G += T.ring(0.05, 0.012, cx=s * 0.05, cy=ly - 0.07) * (1 - rel(t, 0.7, 0.9))
    sai = rel(t, 0.45, 0.95)
    if sai > 0:
        pts = []
        for u in np.linspace(0, 1, 40):
            a = u * TAU * 2.2
            r = 0.04 + 0.3 * u * ease_out(sai, 2)
            pts.append((r * math.cos(a), -0.05 - 0.15 * u * sai + r * math.sin(a) * 0.6))
        G += T.polyline(pts, 0.016) * (1 - rel(t, 0.85, 0.97)) * 1.1
        G += sum(T.polys([(estrela(0.3 * math.cos(a), -0.2 + 0.2 * math.sin(a), 0.04), 1.0)]) for a in (0.4, 2.0, 3.6, 5.0)) * pulso(t, 0.55, 0.95)
    return G * env, H * env


def orgulho_youkai(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    acende = ease_out(rel(t, 0.0, 0.35), 2)
    G += T.arc_band(0.18, 0.06 * acende + 0.004, math.pi * 0.6, math.pi * 1.9, crescente=True, cy=-0.15) * 1.2
    H += T.gauss(-0.05, -0.15, 0.08) * acende * 1.2
    chicote = rel(t, 0.35, 0.85)
    if chicote > 0:
        pts = [(-0.45 + 0.9 * u, 0.2 - 0.25 * math.sin(math.pi * u) + 0.06 * math.sin(u * 10 - chicote * 12)) for u in np.linspace(0, ease_out(chicote, 2), 24)]
        if len(pts) > 1:
            G += T.polyline(pts, 0.02) * (1 - rel(t, 0.8, 0.95)) * 1.3
            H += T.polyline(pts, 0.006) * (1 - rel(t, 0.8, 0.95)) * 1.2
    return G * env, H * env


def battojutsu(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    G += T.lines([(-0.4, 0.08, 0.0, 0.03, 1)], 0.035) * (1 - rel(t, 0.4, 0.55)) * 0.8
    saque = rel(t, 0.15, 0.25)
    if saque > 0:
        G += T.arc_band(0.5, 0.05, math.pi * 0.95, math.pi * 0.95 + math.pi * 0.9 * saque, crescente=True, cy=0.25) * (1 - rel(t, 0.3, 0.5)) * 1.6
        H += T.gauss(0, -0.2, 0.15, 0.05) * pulso(t, 0.15, 0.4) * 1.8
    x = rel(t, 0.4, 0.6)
    if x > 0:
        for a0, a1 in (((-0.3, -0.3), (0.3, 0.3)), ((0.3, -0.3), (-0.3, 0.3))):
            G += T.tapered([(*a0, a0[0] + (a1[0] - a0[0]) * ease_out(x, 2), a0[1] + (a1[1] - a0[1]) * ease_out(x, 2), 1)], 0.035) * (1 - rel(t, 0.8, 0.95)) * 1.3
    return G * env, H * env


def anulou(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    gira = t * 2
    r = 0.34
    parte = rel(t, 0.4, 0.8)
    for s in (-1, 1):
        dx, dy = s * 0.15 * parte, s * 0.1 * parte
        G += T.ring(r, 0.015, cx=dx, cy=dy) * (1 - parte) * 1.1
        for k in range(6):
            a = gira + TAU * k / 6
            G += T.polys([(estrela(dx + 0.25 * math.cos(a), dy + 0.25 * math.sin(a), 0.035, a, 3), 1.0)]) * (1 - parte) * 0.9
    corte = rel(t, 0.3, 0.45)
    if corte > 0:
        pts = [(-0.45 + 0.9 * u, -0.38 + 0.76 * u + 0.04 * math.sin(u * 20)) for u in np.linspace(0, corte, 12)]
        G += T.polyline(pts, 0.07) * 0.8 * (1 - rel(t, 0.6, 0.8)) + T.polyline(pts, 0.025) * (1 - rel(t, 0.6, 0.8))
        H += T.gauss(0, 0, 0.1) * pulso(t, 0.35, 0.6) * 1.0
    return G * env, H * env


def jogador_solo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cruza = ease_out(rel(t, 0.0, 0.3), 2)
    for s in (-1, 1):
        a = s * (0.6 + 0.6 * (1 - cruza))
        x0, y0 = -s * 0.3 * math.cos(a - s * 0.6), 0.32
        G += T.lines([(x0, y0, x0 + 0.62 * math.sin(a), y0 - 0.62 * math.cos(a), 1)], 0.03) * (1 - rel(t, 0.75, 0.9)) * 1.2
        G += T.lines([(x0 - 0.06, y0 - 0.08, x0 + 0.06, y0 - 0.06, 1)], 0.025) * (1 - rel(t, 0.75, 0.9))
    for k in range(8):
        a0 = 0.3 + 0.07 * k
        f = pulso(t, a0, a0 + 0.12)
        a = k * 2.4
        x, y = 0.3 * math.cos(a), -0.05 + 0.25 * math.sin(a)
        G += T.polys([(estrela(x, y, 0.1 * f + 0.003, a, 4, 0.3), 1.0)]) * f * 1.4
        H += T.gauss(x, y, 0.03) * f * 1.5
    return G * env, H * env


def pacifista(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    vem = ease_out(rel(t, 0.0, 0.3), 3)
    bx = -0.5 + 0.35 * vem
    G += T.polys([(_oval(bx, -0.25, 0.09, 0.045), 1.0)]) * (1 - rel(t, 0.5, 0.65)) * 1.3
    G += T.tapered([(bx - 0.25 * (1 - vem), -0.25, bx, -0.25, 1)], 0.02) * (1 - vem)
    G += T.ring(0.05, 0.01, cx=bx, cy=-0.25) * pulso(t, 0.28, 0.5) * 1.5
    paz = ease_out(rel(t, 0.35, 0.65), 2)
    if paz > 0:
        r = 0.26 * paz
        G += T.ring(r, 0.025, cy=0.08) * 1.2
        G += T.lines([(0, 0.08 - r, 0, 0.08 + r, 1), (0, 0.08, r * 0.7, 0.08 + r * 0.7, 1), (0, 0.08, -r * 0.7, 0.08 + r * 0.7, 1)], 0.022) * 1.2
        H += T.gauss(0, 0.08, 0.1) * pulso(t, 0.4, 0.95) * 1.2
    return G * env, H * env


def plano_mestre(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    mistura = rel(t, 0.0, 0.5)
    escolhido = rel(t, 0.5, 0.75)
    for k in range(3):
        fase = TAU * k / 3 + TAU * 1.5 * ease_out(mistura, 2)
        x = 0.28 * math.sin(fase) * (1 - escolhido)
        y = -0.02 + 0.08 * math.cos(fase) * (1 - escolhido)
        cima = k == 1
        sobe = escolhido * (0.25 if cima else -0.0)
        brilho = 1.0 if (cima and escolhido > 0) else 0.5 * (1 - escolhido) + 0.15
        carta = [(x - 0.09, y - 0.13 - sobe), (x + 0.09, y - 0.13 - sobe), (x + 0.09, y + 0.13 - sobe), (x - 0.09, y + 0.13 - sobe)]
        G += T.polys([(carta, 1.0)], 0.003) * 0.35 * brilho + _contorno(T, carta, 0.012) * brilho
        if cima and escolhido > 0:
            G += T.gauss(x, y - 0.05 - sobe, 0.04) * 1.4
            G += T.lines([(x - 0.03, y + 0.05 - sobe, x + 0.03, y + 0.05 - sobe, 1)], 0.012)
            H += T.gauss(x, y - sobe, 0.08) * pulso(t, 0.55, 0.95) * 1.4
    return G * env, H * env


def escudo_rosa(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.4), 2)
    r = 0.4 * abre + 0.01
    G += T.ring(r, 0.03) * 1.2 + T.gauss(0, 0, r * 0.7) * 0.25
    for k in range(5):
        a = TAU * k / 5 + 0.3 * t
        for camada, rr in ((0, 0.12), (1, 0.22)):
            G += T.polys([(_oval(rr * math.cos(a + camada * 0.6) * abre, rr * math.sin(a + camada * 0.6) * abre, 0.07 * abre + 0.003, 0.04 * abre + 0.003, 12, a + camada * 0.6), 1.0)], 0.004) * (0.7 - 0.2 * camada)
    G += T.gauss(0, 0, 0.05 * abre + 0.003) * 1.2
    H += T.ring(r, 0.012) * pulso(t, 0.3, 0.95) * 1.2
    return G * env, H * env


def suprimentos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    caixa = [(-0.22, -0.05), (0.22, -0.05), (0.22, 0.25), (-0.22, 0.25)]
    G += T.polys([(caixa, 1.0)], 0.004) * 0.3 + _contorno(T, caixa, 0.014)
    abre = ease_out(rel(t, 0.15, 0.45), 2)
    G += T.lines([(-0.24, -0.06, -0.24 + 0.46 * math.cos(-1.1 * abre), -0.06 + 0.46 * math.sin(-1.1 * abre), 1)], 0.02)
    cruz = ease_out(rel(t, 0.35, 0.65), 2)
    cy = 0.0 - 0.35 * cruz
    G += T.polys([([(-0.04, cy - 0.12), (0.04, cy - 0.12), (0.04, cy + 0.12), (-0.04, cy + 0.12)], 1.0), ([(-0.12, cy - 0.04), (0.12, cy - 0.04), (0.12, cy + 0.04), (-0.12, cy + 0.04)], 1.0)], 0.003) * cruz * 1.3
    H += T.gauss(0, cy, 0.06) * cruz * 1.2
    setas = rel(t, 0.6, 0.95)
    if setas > 0:
        for x in (-0.3, 0.3):
            y = 0.2 - 0.4 * setas
            G += T.polys([([(x - 0.06, y), (x, y - 0.08), (x + 0.06, y)], 1.0)]) * (1 - setas) * 1.3
    return G * env, H * env


def fus_ro_dah(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for k in range(3):
        f = pulso(t, 0.05 + 0.1 * k, 0.4 + 0.1 * k)
        x = -0.36 + 0.14 * k
        y = -0.3
        G += T.lines([(x - 0.04, y - 0.09, x + 0.04, y + 0.09, 1), (x + 0.04, y - 0.09, x - 0.04, y, 1), (x - 0.04, y, x + 0.04, y + 0.03, 1)], 0.02) * f * 1.4
    for k in range(4):
        a0 = 0.25 + 0.12 * k
        f = rel(t, a0, a0 + 0.45)
        if f <= 0 or f >= 1:
            continue
        G += T.arc_band(0.1 + 0.45 * f, 0.04 * (1 - f) + 0.01, -0.9, 0.9, taper=0.0) * (1 - f) * 1.4
    H += T.gauss(0.15, 0, 0.12) * pulso(t, 0.25, 0.8) * 1.3
    return G * env, H * env


def quatro_bracos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    trava = ease_out(rel(t, 0.0, 0.4), 2)
    for k in range(4):
        a = math.pi / 4 + math.pi / 2 * k
        r = 0.45 - 0.15 * trava
        x, y = r * math.cos(a), r * math.sin(a)
        G += T.lines([(0.12 * math.cos(a), 0.12 * math.sin(a), x, y, 1)], 0.05) * 0.8
        G += T.gauss(x, y, 0.06) * 1.2
    seg = pulso(t, 0.4, 0.8)
    G += T.ring(0.22, 0.035) * seg * 1.3
    G += T.polys([(estrela(0, 0, 0.12 * seg + 0.003, 0.0, 6), 1.0)]) * seg * 1.2
    H += T.gauss(0, 0, 0.07) * seg * 1.6
    return G * env, H * env


def tapa_olho(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    voa = rel(t, 0.0, 0.5)
    cx, cy = 0.08 + 0.4 * voa, -0.12 - 0.3 * math.sin(math.pi * voa) + 0.2 * voa
    tapa = _gira(_oval(0, 0, 0.07, 0.05, 16), voa * 8, cx, cy)
    G += T.polys([(tapa, 1.0)], 0.003) * (1 - rel(t, 0.5, 0.65)) * 1.2
    G += T.lines([(cx - 0.07, cy, cx - 0.25, cy + 0.05, 1)], 0.008) * (1 - rel(t, 0.5, 0.65))
    explode = rel(t, 0.2, 0.95)
    if explode > 0:
        q = np.random.default_rng(8)
        for k in range(14):
            a = TAU * k / 14 + q.uniform(-0.1, 0.1)
            L = (0.2 + 0.35 * ease_out(explode, 2)) * q.uniform(0.7, 1.1)
            pts = [(0.08 * math.cos(a), 0.08 * math.sin(a))]
            for j in range(1, 4):
                rr = L * j / 3
                pts.append((rr * math.cos(a + 0.15 * (-1) ** j), rr * math.sin(a + 0.15 * (-1) ** j)))
            G += T.polyline(pts, 0.025) * (1 - rel(t, 0.75, 0.95)) * 1.1
        H += T.gauss(0, 0, 0.15) * pulso(t, 0.2, 0.9) * 1.6
    return G * env, H * env


def futuro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    surge = ease_out(rel(t, 0.0, 0.3), 2)
    G += T.ring(0.28 * surge + 0.01, 0.022) * 1.1
    for k in range(12):
        a = TAU * k / 12
        G += T.lines([(0.24 * surge * math.cos(a), 0.24 * surge * math.sin(a), 0.28 * surge * math.cos(a), 0.28 * surge * math.sin(a), 1)], 0.012) * surge
    volta = -TAU * 2 * ease_in(rel(t, 0.15, 0.7), 2)
    for L, w, vel in ((0.2, 0.025, 1), (0.14, 0.035, 0.25)):
        a = -math.pi / 2 + volta * vel
        G += T.lines([(0, 0, L * math.cos(a), L * math.sin(a), 1)], w) * surge * 1.2
    portal = rel(t, 0.55, 0.95)
    if portal > 0:
        G += T.ring(0.3 + 0.25 * portal, 0.05 * (1 - portal) + 0.01) * (1 - portal) * 1.4
        H += T.gauss(0, 0, 0.2 * portal + 0.02) * (1 - portal) * 1.8
    return G * env, H * env


def previsao(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.4), 2)
    alto = 0.12 * abre + 0.005
    olho = [(-0.22, -0.05)] + [(x, -0.05 - alto * math.sqrt(max(0.0, 1 - (x / 0.22) ** 2))) for x in np.linspace(-0.2, 0.2, 12)] + [(0.22, -0.05)] + [(x, -0.05 + alto * math.sqrt(max(0.0, 1 - (x / 0.22) ** 2))) for x in np.linspace(0.2, -0.2, 12)]
    G += _contorno(T, olho, 0.016) * 1.2
    G += T.gauss(0, -0.05, 0.06 * abre + 0.003) * 1.3
    H += T.gauss(0, -0.05, 0.03) * abre * 1.8
    linhas = rel(t, 0.35, 0.9)
    if linhas > 0:
        for k in range(5):
            a = -math.pi / 2 + (k - 2) * 0.35
            L = 0.15 + 0.35 * ease_out(linhas, 2)
            G += T.lines([(0.25 * math.cos(a), -0.05 + 0.25 * math.sin(a), L * 1.4 * math.cos(a), -0.05 + L * 1.4 * math.sin(a), 1)], 0.012) * (1 - linhas) * 1.2
        G += T.arc_band(0.38, 0.03, 0.4, math.pi - 0.4, taper=0.0, cy=-0.05) * pulso(t, 0.5, 0.95) * 1.1
    return G * env, H * env


REGISTRO = [
    ("mu_tita", lambda T, t, r: _maior(tita, T, t, r, 1.3), GRANDE, "King Kong · os punhos no peito e as ondas de choque", False),
    ("mu_hienas", lambda T, t, r: _maior(hienas, T, t, r, 1.6), GRANDE, "Scar · as três mordidas das hienas", False),
    ("mu_presentes", lambda T, t, r: _maior(presentes, T, t, r, 1.3), GRANDE, "Jack Esqueleto · o presente abrindo e a espiral", False),
    ("mu_orgulho_youkai", lambda T, t, r: _maior(orgulho_youkai, T, t, r, 1.2), GRANDE, "Sesshomaru · a lua crescente e o chicote de luz", False),
    ("mu_battojutsu", lambda T, t, r: _maior(battojutsu, T, t, r, 1.15), GRANDE, "Kenshin · o saque relâmpago e a cicatriz em X", False),
    ("mu_anulou", lambda T, t, r: _maior(anulou, T, t, r, 1.2), GRANDE, "Asta · o círculo mágico partido pela espada negra", False),
    ("mu_jogador_solo", lambda T, t, r: _maior(jogador_solo, T, t, r, 1.2), GRANDE, "Kirito · as duas espadas e a rajada de estrelas", False),
    ("mu_pacifista", lambda T, t, r: _maior(pacifista, T, t, r, 1.25), GRANDE, "Vash · a bala parando e o símbolo da paz", False),
    ("mu_plano_mestre", lambda T, t, r: _maior(plano_mestre, T, t, r, 1.35), GRANDE, "Megamente · os três planos e o escolhido", False),
    ("mu_escudo_rosa", lambda T, t, r: _maior(escudo_rosa, T, t, r, 1.15), GRANDE, "Steven · o escudo da Rosa abrindo em pétalas", False),
    ("mu_suprimentos", lambda T, t, r: _maior(suprimentos, T, t, r, 1.3), GRANDE, "Ellie · a caixa de suprimentos e a cruz", False),
    ("mu_fus_ro_dah", lambda T, t, r: _maior(fus_ro_dah, T, t, r, 1.6), GRANDE, "Dovahkiin · as três palavras e as ondas do grito", False),
    ("mu_quatro_bracos", lambda T, t, r: _maior(quatro_bracos, T, t, r, 1.15), GRANDE, "Goro · os quatro braços travando o golpe", False),
    ("mu_tapa_olho", lambda T, t, r: _maior(tapa_olho, T, t, r, 1.2), GRANDE, "Kenpachi · o tapa-olho voando e a pressão explodindo", False),
    ("mu_futuro", lambda T, t, r: _maior(futuro, T, t, r, 1.25), GRANDE, "Trunks · o relógio para trás e o portal do tempo", False),
    ("mu_previsao", lambda T, t, r: _maior(previsao, T, t, r, 1.3), GRANDE, "Garnet · o terceiro olho e as linhas do futuro", False),
]
