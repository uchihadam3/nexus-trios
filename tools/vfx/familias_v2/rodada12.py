"""Rodada 12 das habilidades próprias: Kaiba (Yu-Gi-Oh!), Pantera Negra, Feiticeira Escarlate, Visão e
Homem-Formiga (Marvel).

Kaiba
- ultimate_preparo: o Preparo do Ultimate Burst — as três cabeças do Dragão Supremo de Olhos Azuis
  (contornos) com a luz se juntando na boca de cada uma (laço).
- explosao_ultimate: os três raios saem das três bocas e convergem no meio, a explosão branca enorme
  (anéis e raios) e as brasas caindo (Queimando).

Pantera Negra
- habito_cinetico: a malha de hexágonos de vibranium acende de dentro para fora, os golpes chegam e
  são absorvidos (as ondas correndo pela malha) e a casca de hexágonos fecha (Protegido).
- vibranio_preparo: o Preparo da Descarga — a energia cinética correndo para o peito em riscos roxos e
  os hexágonos piscando em volta (laço).
- descarga_real: a energia guardada se aperta numa esfera, explode em onda de choque com os cacos de
  hexágono voando e deixa o rival rachado (Exposto).

Feiticeira Escarlate
- hex_de_probabilidade: os fios do feitiço saem ondulando da mão, giram em volta do rival num redemoinho
  e o sinal do hex acende; as faíscas tontas (Confuso).
- telecinese_escarlate: as faixas de energia vermelha agarram o rival de vários lados e apertam; a névoa
  sobe e a barra de Preparo dele recua.
- caos_preparo: o Preparo da Distorção — a tiara da Feiticeira no alto e os fios girando em volta das
  mãos (laço).
- distorcao_do_caos: a onda de magia do caos rola, o espaço entorta em anéis ondulados e os cacos da
  realidade flutuam girando.

Visão
- faseamento: a mudança de densidade — o corpo fica fantasma (as cópias deslocadas, as linhas de
  varredura) e o golpe que chega atravessa sem acertar.
- raio_solar: a Joia da Mente acende (o losango com o clarão) e dispara o raio solar grosso, com a
  explosão de sol no rival.
- computacao_preparo: o Preparo da Computação — os anéis de circuito girando ao contrário, os dados
  correndo e a joia no meio (laço).
- computacao_sintetica: a grade de cálculo varre o rival, a trajetória pontilhada se desenha, o raio fino
  acerta o ponto exato e o anel do Preparo dele se parte.

Homem-Formiga
- encolhimento: os anéis de encolher se fecham num ponto com as partículas Pym, o pontinho corre em
  zigue-zague até o rival e acerta em vários golpes rápidos, deixando-o Lento.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _borda(T, a, s=0.008):
    return np.clip(a - T.blur(a, s), 0, 1)


def _contorno(pts, w=1.0):
    return [(pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], w) for i in range(len(pts))]


def _hexagono(cx, cy, r, ang=0.0):
    return [(cx + r * math.cos(ang + k * math.pi / 3), cy + r * math.sin(ang + k * math.pi / 3)) for k in range(6)]


def _malha_hex(cx, cy, cel, R, peso):
    """Os lados da malha de hexágonos dentro do raio R; `peso(d)` dá o brilho de cada lado pela distância."""
    segs = []
    n = int(R / cel) + 2
    for q in range(-n, n + 1):
        for r in range(-n, n + 1):
            x = cx + cel * math.sqrt(3) * (q + r / 2)
            y = cy + cel * 1.5 * r
            d = math.hypot(x - cx, y - cy)
            if d > R:
                continue
            w = peso(d)
            if w <= 0.01:
                continue
            segs += _contorno(_hexagono(x, y, cel * 0.92, math.pi / 6), w)
    return segs


def _fios(T, t, seed, n, x0, y0, x1, y1, prog, amp=0.12, larg=0.012):
    """Os fios do feitiço: linhas ondulando de (x0,y0) a (x1,y1), cada uma na sua fase."""
    sub = np.random.default_rng(seed)
    out = T.zero()
    for _ in range(n):
        fase = sub.uniform(0, TAU)
        a = sub.uniform(0.5, 1.2) * amp
        f = sub.uniform(2, 4)
        pts = []
        for j in range(30):
            u = j / 29 * prog
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u + a * math.sin(TAU * f * u + fase + t * 14) * math.sin(math.pi * min(1, u / max(prog, 1e-3)))
            pts.append((x, y))
        out += T.polyline(pts, larg) * sub.uniform(0.6, 1)
    return out


# =================================================================== Kaiba
_BOCAS = ((0.42, -0.5), (0.55, 0.0), (0.42, 0.5))


def _cabeca_de_dragao(cx, cy, s, ang):
    """O contorno da cabeça do dragão de olhos azuis, de perfil, olhando para `ang`: o focinho comprido, a
    mandíbula aberta e os chifres para trás."""
    pts = [(0.42, -0.02), (0.2, -0.06), (0.05, -0.1), (-0.1, -0.12), (-0.32, -0.24), (-0.18, -0.08), (-0.4, -0.06),
           (-0.2, 0.0), (-0.15, 0.1), (0.05, 0.08), (0.36, 0.1), (0.1, 0.03), (0.4, 0.02)]
    return _gira([(x * s, y * s) for x, y in pts], ang, cx, cy)


def ultimate_preparo(T, t, rng):
    """O Preparo do Ultimate Burst: as três cabeças do Dragão Supremo, em contorno aceso, cada uma de boca aberta
    para a direita, e a luz se juntando na boca de cada uma (as partículas caindo em espiral para dentro),
    com o brilho pulsando (laço)."""
    G, H = vazio(T)
    s = 1.0
    for k, (mx, my) in enumerate(_BOCAS):
        ang = math.atan2(my * 0.35, 1.0)
        cx, cy = mx - 0.42 * s * math.cos(ang), my - 0.42 * s * math.sin(ang)
        cab = _cabeca_de_dragao(cx, cy, s, ang)
        C = T.polys([(cab, 1.0)])
        G += _borda(T, C, 0.01) * 1.4 + C * 0.15
        olho = _gira([(-0.02, -0.06)], ang, cx, cy)[0]
        H += T.gauss(olho[0], olho[1], 0.014) * 1.6
        pts = []
        for j in range(10):
            u = (t * 2 + j / 10) % 1
            a = TAU * j / 10 + 3 * u
            r = 0.25 * (1 - u)
            pts.append((mx + r * math.cos(a), my + r * math.sin(a), math.sin(math.pi * u)))
        G += T.splats(pts, 0.016) * 1.2
        bate = 0.7 + 0.3 * math.sin(TAU * (t * 2 + k / 3))
        H += T.gauss(mx, my, 0.035 + 0.015 * bate) * 1.3 * bate
        G += T.gauss(mx, my, 0.08) * 0.6 * bate
    return G, H


def explosao_ultimate(T, t, rng):
    """O Ultimate Burst do Dragão Supremo: os três raios grossos saem das três bocas (da esquerda) e convergem
    no rival, a explosão branca enorme (o clarão, os anéis e os raios), e as brasas caindo (Queimando)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    origens = ((-1.0, -0.75), (-1.05, 0.0), (-1.0, 0.75))
    alvo = (0.2, 0.0)
    for k, (ox, oy) in enumerate(origens):
        vai = ease_in(rel(t, 0.0 + 0.03 * k, 0.22 + 0.03 * k), 1.6)
        some = 1 - rel(t, 0.4, 0.58)
        if vai <= 0 or some <= 0:
            continue
        x = ox + (alvo[0] - ox) * vai
        y = oy + (alvo[1] - oy) * vai
        R = T.tapered([(ox, oy, x, y, 1.0)], 0.09)
        G += (R * 1.2 + T.blur(R, 0.03) * 0.7) * some
        H += T.tapered([(ox, oy, x, y, 1.0)], 0.035) * 1.2 * some
        H += T.gauss(ox + 0.08, oy * 0.92, 0.07) * some * 1.2
    bum = rel(t, 0.22, 0.9)
    if bum > 0:
        b = ease_out(bum, 2.5)
        H += T.gauss(alvo[0], alvo[1], 0.1 + 0.3 * b) * (1 - bum) ** 1.5 * 2.0
        G += T.gauss(alvo[0], alvo[1], 0.2 + 0.45 * b) * (1 - bum) * 1.3
        for k in range(3):
            u = rel(bum, 0.1 * k, 0.6 + 0.1 * k)
            if 0 < u < 1:
                G += T.ring(0.15 + 0.85 * ease_out(u, 2), 0.04 * (1 - u) + 0.01, alvo[0], alvo[1]) * (1 - u) * 1.4
        raios = []
        q = np.random.default_rng(7)
        for k in range(16):
            a = TAU * k / 16 + q.uniform(-0.1, 0.1)
            L = (0.5 + 0.5 * q.uniform()) * (0.4 + 0.8 * b)
            raios.append((alvo[0] + 0.1 * math.cos(a), alvo[1] + 0.1 * math.sin(a),
                          alvo[0] + L * math.cos(a), alvo[1] + L * math.sin(a), (1 - bum)))
        G += T.tapered(raios, 0.03) * 1.2
    brasa = rel(t, 0.45, 1.0)
    if 0 < brasa < 1:
        sub = np.random.default_rng(42)
        pts = []
        for _ in range(30):
            x = alvo[0] + sub.uniform(-0.8, 0.8)
            y = -0.6 + sub.uniform(0, 0.5) + 1.2 * brasa * sub.uniform(0.6, 1.2)
            pts.append((x + 0.04 * math.sin(t * 20 + x * 9), y, (1 - brasa) * sub.uniform(0.5, 1)))
        G += T.splats(pts, 0.014) * 1.4
        H += T.splats(pts, 0.006) * 0.8
    return G * env, H * env


# =================================================================== Pantera Negra
def habito_cinetico(T, t, rng):
    """O hábito de vibranium: a malha de hexágonos acende de dentro para fora sobre o corpo, os golpes chegam de
    fora e são absorvidos (cada um vira uma onda roxa correndo pela malha) e a casca de hexágonos fecha em
    volta (Protegido)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    acende = ease_out(rel(t, 0.0, 0.3), 2)
    golpes = ((0.15, -0.75, -0.2), (0.25, 0.7, 0.1), (0.35, -0.6, 0.45), (0.45, 0.65, -0.4))

    def peso(d):
        w = 0.25 * (d < 0.65 * acende)
        for t0, gx, gy in golpes:
            u = rel(t, t0 + 0.05, t0 + 0.4)
            if 0 < u < 1:
                frente = 0.05 + 0.7 * u
                dd = abs(d - frente)
                w += max(0, 1 - dd / 0.12) * (1 - u) * 1.3
        return w

    segs = _malha_hex(0.0, 0.0, 0.08, 0.62, peso)
    if segs:
        M = T.lines(segs, 0.01)
        G += M * 1.2 + T.blur(M, 0.02) * 0.5
    for t0, gx, gy in golpes:
        vem = rel(t, t0 - 0.08, t0)
        if 0 < vem < 1:
            x, y = gx * (1 - vem) + gx * 0.6 * vem, gy * (1 - vem) + gy * 0.6 * vem
            G += T.tapered([(gx * 1.3, gy * 1.3, x, y, 1.0)], 0.02) * 1.1
        bate = rel(t, t0, t0 + 0.2)
        if 0 < bate < 1:
            px, py = gx * 0.6, gy * 0.6
            H += T.flare(px, py, 0.18 * (1 - bate) + 0.01, 0.3, 0.01) * (1 - bate) * 1.4
    casca = back(rel(t, 0.55, 0.8), 1.4)
    if casca > 0:
        r = 0.7 * casca
        aneis = []
        for k in range(12):
            a = TAU * k / 12 + 0.3 * t
            aneis += _contorno(_hexagono(r * math.cos(a), r * 0.95 * math.sin(a), 0.1, a), 1.0)
        C = T.lines(aneis, 0.014)
        G += C * 1.2 * (1 - rel(t, 0.85, 1.0)) + T.ring(r, 0.03, 0, 0) * 0.5
        H += C * 0.3 * pulso(t, 0.6, 0.9)
    return G * env, H * env


def vibranio_preparo(T, t, rng):
    """O Preparo da Descarga real: a energia cinética correndo para o peito em riscos roxos, de todos os lados, e
    os hexágonos em volta piscando um por um, com o brilho do peito crescendo (laço)."""
    G, H = vazio(T)
    sub = np.random.default_rng(12)
    riscos = []
    for k in range(14):
        a = sub.uniform(0, TAU)
        u = (t * 1.5 + k / 14) % 1
        r1 = 0.85 * (1 - u) + 0.08
        r0 = r1 + 0.18 * (1 - u)
        riscos.append((r0 * math.cos(a), r0 * math.sin(a), r1 * math.cos(a), r1 * math.sin(a), math.sin(math.pi * u)))
    G += T.tapered(riscos, 0.018) * 1.2
    hexes = []
    for k in range(8):
        a = TAU * k / 8
        pisca = max(0, math.sin(TAU * (t - k / 8)))
        hexes += _contorno(_hexagono(0.5 * math.cos(a), 0.5 * math.sin(a), 0.08, 0), 0.3 + 0.9 * pisca)
    G += T.lines(hexes, 0.012) * 1.1
    bate = 0.7 + 0.3 * math.sin(TAU * t * 2)
    H += T.gauss(0, 0, 0.06) * 1.3 * bate
    G += T.gauss(0, 0, 0.15) * 0.6 * bate + T.lines(_contorno(_hexagono(0, 0, 0.13, 0)), 0.014) * bate
    return G, H


def descarga_real(T, t, rng):
    """A Descarga real: a energia guardada se aperta numa esfera roxa (os riscos sugados), explode numa onda de
    choque grossa com os cacos de hexágono voando, e o rival fica rachado (Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    aperta = rel(t, 0.0, 0.3)
    if aperta < 1:
        r = 0.4 * (1 - ease_in(aperta, 2)) + 0.08
        G += T.ring(r, 0.03, 0, 0) * 1.2 + T.gauss(0, 0, r * 0.6) * 0.6
        sub = np.random.default_rng(4)
        riscos = []
        for k in range(12):
            a = sub.uniform(0, TAU)
            d = 0.9 * (1 - aperta) + 0.1
            riscos.append((d * 1.3 * math.cos(a), d * 1.3 * math.sin(a), d * math.cos(a), d * math.sin(a), 1.0))
        G += T.tapered(riscos, 0.016) * aperta * 1.2
    explode = rel(t, 0.3, 0.9)
    if explode > 0:
        e = ease_out(explode, 2.5)
        H += T.gauss(0, 0, 0.08 + 0.15 * e) * (1 - explode) ** 2 * 2.0 + T.flare(0, 0, 0.9 * (1 - explode) + 0.02, 0, 0.016) * (1 - explode)
        G += T.ring(0.1 + 0.85 * e, 0.07 * (1 - explode) + 0.015, 0, 0) * (1 - explode) * 1.5
        G += T.ring(0.05 + 0.55 * e, 0.03, 0, 0) * (1 - explode) * 0.8
        q = np.random.default_rng(19)
        cacos = []
        for k in range(14):
            a = TAU * k / 14 + q.uniform(-0.2, 0.2)
            d = 0.15 + 0.85 * e * q.uniform(0.6, 1.1)
            cacos += _contorno(_hexagono(d * math.cos(a), d * math.sin(a), 0.05 * (1 - 0.5 * explode), explode * 6 + k), 1 - explode)
        G += T.lines(cacos, 0.014) * 1.3
    racha = pulso(t, 0.5, 1.0)
    if racha > 0:
        q = np.random.default_rng(23)
        for k in range(6):
            a = TAU * k / 6 + 0.4
            G += T.polyline(jagged(q, 0, 0, 0.35 * math.cos(a), 0.35 * math.sin(a), 4, 0.3), 0.012) * racha * 1.1
    return G * env, H * env


# =================================================================== Feiticeira Escarlate
def hex_de_probabilidade(T, t, rng):
    """O hex de probabilidade: os fios vermelhos saem ondulando da mão (da esquerda), giram em volta do rival num
    redemoinho que se aperta, e o sinal do hex (os dois anéis com as pontas tortas) acende; as faíscas giram
    tontas (Confuso)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    vai = ease_out(rel(t, 0.0, 0.3), 2)
    if vai > 0 and t < 0.6:
        F = _fios(T, t, 3, 5, -0.95, 0.1, 0.0, 0.0, vai, 0.15, 0.011)
        G += (F * 1.2 + T.blur(F, 0.02) * 0.6) * (1 - rel(t, 0.4, 0.6))
    gira = rel(t, 0.25, 0.85)
    if 0 < gira < 1:
        pts = []
        for k in range(3):
            for j in range(40):
                u = j / 39
                a = TAU * (k / 3 + gira * 1.5) + 4.5 * u
                r = (0.65 - 0.4 * ease_out(gira, 2)) * (1 - 0.6 * u) + 0.05
                pts.append((r * math.cos(a), r * 0.8 * math.sin(a), math.sin(math.pi * u) * math.sin(math.pi * gira)))
        G += T.splats(pts, 0.016) * 1.2
    sinal = back(rel(t, 0.4, 0.6), 1.5) * (1 - rel(t, 0.82, 0.98))
    if sinal > 0:
        S = T.ring(0.28 * sinal, 0.014, 0, 0) + T.ring(0.2 * sinal, 0.01, 0, 0)
        pontas = []
        for k in range(6):
            a = TAU * k / 6 + 0.5 * t
            x0, y0 = 0.28 * sinal * math.cos(a), 0.28 * sinal * math.sin(a)
            x1, y1 = 0.42 * sinal * math.cos(a + 0.35), 0.42 * sinal * math.sin(a + 0.35)
            pontas.append((x0, y0, x1, y1, 1.0))
        S += T.lines(pontas, 0.014)
        G += S * 1.3
        H += S * 0.4 + T.gauss(0, 0, 0.05) * sinal
    tonto = pulso(t, 0.6, 1.0)
    if tonto > 0:
        est = []
        for k in range(4):
            a = TAU * (k / 4 + t * 1.3)
            est.append((estrela(0.3 * math.cos(a), -0.45 + 0.08 * math.sin(a), 0.045, a, 4, 0.4), 1.0))
        G += T.polys(est) * tonto * 1.1
    return G * env, H * env


def telecinese_escarlate(T, t, rng):
    """A telecinese: as faixas de energia vermelha chegam de vários lados e agarram o rival como mãos (as faixas
    curvas que se fecham), apertam com um tremor, a névoa vermelha sobe, e a barra do Preparo dele recua
    (empurrada para trás)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k in range(4):
        a0 = TAU * k / 4 + 0.6
        fecha = ease_out(rel(t, 0.05 * k, 0.3 + 0.05 * k), 2)
        if fecha <= 0:
            continue
        r = 0.75 - 0.4 * fecha
        tremor = 0.015 * math.sin(t * 90 + k) * pulso(t, 0.35, 0.75)
        A = T.arc_band(r + tremor, 0.06, a0, a0 + 1.5 * fecha + 0.3, squash=0.85, cx=0, cy=0, taper=0.6)
        G += A * 1.3 + T.blur(A, 0.025) * 0.5
        H += _borda(T, A, 0.005) * 0.4
    aperta = pulso(t, 0.35, 0.75)
    H += T.gauss(0, 0, 0.12) * aperta * 1.1
    G += T.ring(0.3 - 0.08 * aperta, 0.02, 0, 0) * aperta * 0.8
    nevoa = rel(t, 0.3, 1.0)
    if 0 < nevoa < 1:
        sub = np.random.default_rng(8)
        pts = [(sub.uniform(-0.5, 0.5), 0.3 - 0.8 * ((nevoa + sub.uniform(0, 1)) % 1), 0.5 * math.sin(math.pi * nevoa)) for _ in range(18)]
        G += T.splats(pts, 0.05) * 0.9
    recua = rel(t, 0.3, 0.75)
    y = -0.72
    if t < 0.95:
        cheio = 0.75 - 0.45 * ease_out(recua, 2)
        moldura = T.lines(_contorno([(-0.45, y - 0.06), (0.45, y - 0.06), (0.45, y + 0.06), (-0.45, y + 0.06)]), 0.014)
        barra = T.lines([(-0.42, y, -0.42 + 0.84 * cheio, y, 1.0)], 0.06)
        G += (moldura + barra * 0.7) * (1 - rel(t, 0.8, 0.95)) * 1.1
        if 0 < recua < 1:
            xs = -0.42 + 0.84 * cheio
            G += T.lines([(xs + 0.04, y - 0.08, xs + 0.12, y, 1.0), (xs + 0.04, y + 0.08, xs + 0.12, y, 1.0)], 0.016) * (1 - recua) * 1.2
    return G * env, H * env


def _tiara(cx, cy, s):
    """A tiara da Feiticeira: a ponta alta no meio e as duas pontas curvas para fora."""
    return [(cx - 0.45 * s, cy + 0.1 * s), (cx - 0.38 * s, cy - 0.3 * s), (cx - 0.2 * s, cy - 0.05 * s), (cx, cy - 0.5 * s),
            (cx + 0.2 * s, cy - 0.05 * s), (cx + 0.38 * s, cy - 0.3 * s), (cx + 0.45 * s, cy + 0.1 * s), (cx, cy + 0.02 * s)]


def caos_preparo(T, t, rng):
    """O Preparo da Distorção do caos: a tiara da Feiticeira acesa no alto e os fios de magia girando em volta das
    duas mãos, subindo e descendo (laço)."""
    G, H = vazio(T)
    C = T.lines(_contorno(_tiara(0, -0.5, 0.75)), 0.016)
    G += C * (0.9 + 0.2 * math.sin(TAU * t * 2)) + T.blur(C, 0.02) * 0.4
    for lado in (-1, 1):
        cx, cy = 0.38 * lado, 0.25
        pts = []
        for k in range(3):
            for j in range(26):
                u = j / 25
                a = TAU * (t * lado + k / 3) + 5 * u
                r = 0.08 + 0.18 * u
                pts.append((cx + r * math.cos(a), cy + r * 0.7 * math.sin(a) - 0.1 * u, math.sin(math.pi * u)))
        G += T.splats(pts, 0.013) * 1.2
        H += T.gauss(cx, cy, 0.03) * 1.2
    return G, H


def distorcao_do_caos(T, t, rng):
    """A Distorção do caos: a onda de magia rola da esquerda (as fitas vermelhas), e o espaço entorta — os anéis
    ondulados se abrem tremendo, e os cacos da realidade (os triângulos) flutuam girando e somem."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    rola = ease_out(rel(t, 0.0, 0.35), 1.8)
    if rola > 0 and t < 0.6:
        some = 1 - rel(t, 0.4, 0.6)
        for k in range(5):
            y0 = -0.6 + 0.3 * k
            F = _fios(T, t, 30 + k, 1, -1.0, y0, -1.0 + 1.6 * rola, y0 * 0.7, 1.0, 0.1, 0.02)
            G += (F * 1.1 + T.blur(F, 0.03) * 0.5) * some
    entorta = rel(t, 0.3, 0.95)
    if 0 < entorta < 1:
        A = T.zero()
        for k in range(4):
            u = rel(entorta, 0.1 * k, 0.55 + 0.1 * k)
            if 0 < u < 1:
                A += T.ring(0.1 + 0.8 * ease_out(u, 2), 0.025, 0, 0) * (1 - u)
        ang = np.arctan2(T.V, T.U)
        du = 0.04 * np.sin(ang * 6 + t * 20) * math.sin(math.pi * entorta)
        dv = 0.04 * np.cos(ang * 5 - t * 18) * math.sin(math.pi * entorta)
        A = T.warp(A, du, dv)
        G += A * 1.4 + T.blur(A, 0.02) * 0.5
        H += T.gauss(0, 0, 0.1) * (1 - entorta) ** 2 * 1.4
        q = np.random.default_rng(13)
        cacos = []
        for k in range(12):
            a = q.uniform(0, TAU)
            d = 0.2 + 0.6 * ease_out(entorta, 2) * q.uniform(0.6, 1)
            cx, cy = d * math.cos(a), d * math.sin(a) - 0.15 * entorta
            s = 0.06 * q.uniform(0.7, 1.3)
            giro = q.uniform(-6, 6) * entorta
            tri = _gira([(0, -s), (s * 0.9, s * 0.6), (-s * 0.8, s * 0.7)], giro, cx, cy)
            cacos += _contorno(tri, (1 - entorta))
        G += T.lines(cacos, 0.012) * 1.3
    return G * env, H * env


# =================================================================== Visão
def _silhueta(T, cx, cy, s):
    """O corpo do Visão em contorno: a cabeça, o pescoço, os ombros largos, os braços junto do corpo e as
    pernas."""
    meia = [(0.05, -0.33), (0.22, -0.28), (0.27, 0.1), (0.21, 0.12), (0.17, -0.1), (0.14, 0.14), (0.16, 0.56),
            (0.05, 0.56), (0.0, 0.22)]
    corpo = [(cx + x * s, cy + y * s) for x, y in meia] + [(cx - x * s, cy + y * s) for x, y in reversed(meia[:-1])]
    cabeca = T.ring(0.085 * s, 0.012, cx, cy - 0.43 * s, squash=0.85)
    return cabeca + T.lines(_contorno(corpo), 0.012), (cx, cy - 0.45 * s)


def faseamento(T, t, rng):
    """O faseamento: o corpo do Visão fica fantasma — as cópias deslocadas para os lados, as linhas de varredura
    correndo de cima para baixo — e o golpe que chega atravessa sem acertar; a Joia da Mente brilha na testa
    (Protegido)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    fase = pulso(t, 0.05, 0.9)
    S, (jx, jy) = _silhueta(T, 0, 0.05, 1.1)
    for k, dx in enumerate((-0.12, 0.12, -0.24, 0.24)):
        d = dx * ease_out(rel(t, 0.05, 0.35), 2) * (1 - rel(t, 0.7, 0.9))
        if abs(d) < 1e-3:
            continue
        Sk = T.warp(S, np.full_like(S, d), np.zeros_like(S))
        G += Sk * fase * (0.55 if k < 2 else 0.3)
    G += S * 1.1 * (1 - 0.5 * fase)
    var = (t * 2.5) % 1
    faixa = np.exp(-((T.V - (-0.7 + 1.5 * var)) / 0.04) ** 2) * (np.abs(T.U) < 0.35)
    G += faixa * fase * 0.8
    linhas = (0.5 + 0.5 * np.sin(T.V * 140)) * (np.abs(T.U) < 0.3) * (np.abs(T.V - 0.05) < 0.55)
    G += T.blur(S, 0.04) * linhas * fase * 1.5
    golpe = rel(t, 0.35, 0.7)
    if 0 < golpe < 1:
        x = -1.0 + 2.0 * golpe
        G += T.tapered([(x - 0.4, 0.0, x, 0.0, 1.0), (x - 0.3, 0.12, x + 0.05, 0.12, 0.7)], 0.025) * 1.2
        G += T.ring(0.15, 0.01, x, 0.05) * (abs(x) < 0.3) * 0.0
    H += (T.polys([(_gira([(0, -0.035), (0.03, 0), (0, 0.035), (-0.03, 0)], 0, jx, jy + 0.02), 1.0)]) * 1.2
          + T.flare(jx, jy + 0.02, 0.15 + 0.1 * fase, 0, 0.008) * 0.8)
    return G * env, H * env


def _joia(cx, cy, s):
    return [(cx, cy - s), (cx + s * 0.75, cy), (cx, cy + s), (cx - s * 0.75, cy)]


def raio_solar(T, t, rng):
    """O raio solar: a Joia da Mente acende na esquerda (o losango com o clarão em cruz), dispara o raio solar
    grosso com as faíscas girando em volta, e no rival abre a explosão de sol (os raios curtos em roda e o
    anel); a marca de Exposto fica."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    jx, jy = -0.8, -0.1
    carga = ease_out(rel(t, 0.0, 0.2), 2) * (1 - rel(t, 0.6, 0.8))
    if carga > 0:
        J = T.polys([(_joia(jx, jy, 0.09), 1.0)])
        G += J * 1.0 * carga + _borda(T, J, 0.006) * carga
        H += T.flare(jx, jy, 0.4 * carga + 0.01, 0, 0.012) * carga + T.gauss(jx, jy, 0.04) * carga * 1.4
    raio = rel(t, 0.15, 0.55)
    if 0 < raio < 1:
        vai = ease_out(rel(t, 0.15, 0.25), 2)
        some = 1 - rel(t, 0.45, 0.6)
        x1 = jx + (0.1 - jx) * vai
        larg = 0.08 * (0.6 + 0.4 * math.sin(t * 60))
        R = T.lines([(jx, jy, x1, 0.0, 1.0)], larg)
        G += (T.blur(R, 0.02) * 0.9 + R * 0.8) * some
        H += T.lines([(jx, jy, x1, 0.0, 1.0)], larg * 0.35) * 1.3 * some
        sub = np.random.default_rng(int(t * 40) % 9)
        pts = []
        for k in range(14):
            u = sub.uniform(0, 1) * vai
            x = jx + (x1 - jx) * u
            y = jy * (1 - u) + 0.1 * math.sin(TAU * (u * 3 + t * 4) + k)
            pts.append((x, y, 0.8))
        G += T.splats(pts, 0.012) * some * 1.2
    sol = rel(t, 0.25, 0.85)
    if 0 < sol < 1:
        s = ease_out(sol, 2.5)
        H += T.gauss(0.1, 0.0, 0.08 + 0.1 * s) * (1 - sol) ** 1.5 * 1.8
        G += T.ring(0.12 + 0.45 * s, 0.03, 0.1, 0.0) * (1 - sol) * 1.4
        raios = []
        for k in range(12):
            a = TAU * k / 12 + 0.15
            raios.append((0.1 + 0.15 * math.cos(a), 0.15 * math.sin(a), 0.1 + (0.2 + 0.3 * s) * math.cos(a), (0.2 + 0.3 * s) * math.sin(a), 1 - sol))
        G += T.tapered(raios, 0.03) * 1.2
    return G * env, H * env


def computacao_preparo(T, t, rng):
    """O Preparo da Computação sintética: os anéis de circuito (arcos tracejados) girando ao contrário, os dados
    correndo pelos anéis em pontinhos e a Joia da Mente no meio (laço)."""
    G, H = vazio(T)
    for k, (r, vel, n) in enumerate(((0.25, 1, 6), (0.42, -1, 9), (0.6, 1, 12))):
        for j in range(n):
            a0 = TAU * (j / n + vel * t / (k + 1))
            G += T.arc_band(r, 0.012, a0, a0 + TAU / n * 0.6, taper=0.0) * 1.0
        pts = [(r * math.cos(TAU * (vel * t * 2 + j / 4)), r * math.sin(TAU * (vel * t * 2 + j / 4)), 1.0) for j in range(4)]
        H += T.splats(pts, 0.012) * 1.2
    J = T.polys([(_joia(0, 0, 0.08), 1.0)])
    G += J * 0.9
    H += T.gauss(0, 0, 0.03) * (1.1 + 0.3 * math.sin(TAU * t * 2))
    return G, H


def computacao_sintetica(T, t, rng):
    """A computação sintética: a grade de cálculo varre o rival (as linhas que passam e a mira em cruz), a
    trajetória pontilhada se desenha da esquerda, o raio fino e exato acerta o ponto calculado, e o anel do
    Preparo do rival (o arco em volta dele) se parte em pedaços que caem."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    grade = pulso(t, 0.0, 0.5)
    if grade > 0:
        var = rel(t, 0.0, 0.35)
        segs = []
        for k in range(7):
            x = -0.45 + 0.15 * k
            segs.append((x, -0.45, x, 0.45, 0.35))
            segs.append((-0.45, x, 0.45, x, 0.35))
        G += T.lines(segs, 0.006) * grade
        yv = -0.45 + 0.9 * var
        G += T.lines([(-0.5, yv, 0.5, yv, 1.0)], 0.012) * grade * 1.2
        G += T.lines([(-0.1, 0, -0.03, 0, 1.0), (0.03, 0, 0.1, 0, 1.0), (0, -0.1, 0, -0.03, 1.0), (0, 0.03, 0, 0.1, 1.0)], 0.012) * grade * 1.4
    traj = rel(t, 0.15, 0.4)
    if traj > 0 and t < 0.6:
        pts = []
        for j in range(16):
            u = j / 15
            if u > traj:
                break
            pts.append((-0.95 + 0.95 * u, -0.25 * math.sin(math.pi * u) * 0.0 - 0.0, 0.9))
        G += T.splats(pts, 0.01) * 1.3 * (1 - rel(t, 0.45, 0.6))
    tiro = rel(t, 0.42, 0.6)
    if 0 < tiro < 1:
        G += T.lines([(-0.95, 0.0, 0.0, 0.0, 1.0)], 0.018) * (1 - tiro) * 1.3
        H += T.lines([(-0.95, 0.0, 0.0, 0.0, 1.0)], 0.006) * (1 - tiro) * 1.5
        H += T.flare(0, 0, 0.35 * (1 - tiro) + 0.02, 0.785, 0.01) * (1 - tiro) * 1.3
        G += T.ring(0.03 + 0.2 * ease_out(tiro, 3), 0.014, 0, 0) * (1 - tiro) * 1.3
    anel = 1 - rel(t, 0.85, 1.0)
    quebra = rel(t, 0.45, 0.95)
    for k in range(6):
        a0 = -math.pi / 2 + TAU * k / 6 * 0.75
        if quebra <= 0:
            G += T.arc_band(0.38, 0.025, a0, a0 + TAU / 6 * 0.75 * 0.85, taper=0.0) * 1.1 * rel(t, 0.0, 0.15)
        else:
            am = a0 + TAU / 12 * 0.75
            dx = 0.25 * quebra * math.cos(am)
            dy = 0.25 * quebra * math.sin(am) + 0.4 * quebra * quebra
            A = T.arc_band(0.38, 0.025, a0 + 0.3 * quebra, a0 + TAU / 6 * 0.75 * 0.85 + 0.3 * quebra, taper=0.0, cx=dx, cy=dy)
            G += A * (1 - quebra) * 1.2 * anel
    return G * env, H * env


# =================================================================== Homem-Formiga
def encolhimento(T, t, rng):
    """O encolhimento: os anéis de encolher se fecham num ponto (com as partículas Pym vermelhas sugadas junto),
    o pontinho dispara em zigue-zague até o rival (o rastro fino), acerta em vários golpes rápidos (os
    clarões pequenos em volta) e deixa a espiral lenta e a marca."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    px, py = -0.55, 0.2
    fecha = rel(t, 0.0, 0.28)
    if fecha < 1:
        for k in range(4):
            u = rel(fecha, 0.15 * k, 0.6 + 0.15 * k)
            if 0 < u < 1:
                G += T.ring(0.45 * (1 - ease_in(u, 2)) + 0.01, 0.018, px, py) * math.sin(math.pi * u) * 1.3
        sub = np.random.default_rng(6)
        pts = []
        for _ in range(16):
            a = sub.uniform(0, TAU)
            d = 0.5 * (1 - ease_in(fecha, 1.5)) * sub.uniform(0.5, 1)
            pts.append((px + d * math.cos(a), py + d * math.sin(a), 0.9))
        G += T.splats(pts, 0.016) * 1.5
    H += T.gauss(px, py, 0.025) * pulso(t, 0.2, 0.35) * 1.8 + T.flare(px, py, 0.25 * pulso(t, 0.22, 0.32) + 0.01, 0, 0.008) * pulso(t, 0.22, 0.32)
    corre = rel(t, 0.3, 0.5)
    if corre > 0 and t < 0.7:
        zig = []
        for j in range(9):
            u = j / 8
            zig.append((px + (0.0 - px) * u, py + (0.0 - py) * u + 0.12 * (1 if j % 2 else -1) * (0 < j < 8)))
        L = 0.0
        tot = sum(math.hypot(zig[i + 1][0] - zig[i][0], zig[i + 1][1] - zig[i][1]) for i in range(8))
        alvo = tot * corre
        pts = [zig[0]]
        for i in range(8):
            d = math.hypot(zig[i + 1][0] - zig[i][0], zig[i + 1][1] - zig[i][1])
            if L + d >= alvo:
                f = (alvo - L) / d
                pts.append((zig[i][0] + (zig[i + 1][0] - zig[i][0]) * f, zig[i][1] + (zig[i + 1][1] - zig[i][1]) * f))
                break
            pts.append(zig[i + 1])
            L += d
        some = 1 - rel(t, 0.5, 0.7)
        Z = T.polyline(pts, 0.016)
        G += (Z * 1.4 + T.blur(Z, 0.02) * 0.6) * some
        H += T.gauss(pts[-1][0], pts[-1][1], 0.03) * 1.8 * (corre < 1)
    for k in range(5):
        t0 = 0.48 + 0.05 * k
        b = rel(t, t0, t0 + 0.15)
        if 0 < b < 1:
            a = 1.3 * k + 0.4
            x, y = 0.16 * math.cos(a), 0.16 * math.sin(a)
            H += T.flare(x, y, 0.28 * (1 - b) + 0.01, a, 0.01) * (1 - b) * 1.5
            G += T.ring(0.03 + 0.16 * b, 0.016, x, y) * (1 - b) * 1.4
    lento = pulso(t, 0.65, 1.0)
    if lento > 0:
        pts = []
        for j in range(50):
            u = j / 49
            a = TAU * 2.2 * u + t * 3
            r = 0.08 + 0.35 * u
            pts.append((r * math.cos(a), r * 0.6 * math.sin(a) + 0.05, 0.6 * (1 - u)))
        G += T.splats(pts, 0.016) * lento * 1.4
    return G * env, H * env


REGISTRO = [
    ("ultimate_preparo", ultimate_preparo, MEDIA, "Kaiba · as três cabeças juntando a luz (Preparo, laço)", True),
    ("explosao_ultimate", explosao_ultimate, GRANDE, "Kaiba · os três raios e a explosão branca", False),
    ("habito_cinetico", habito_cinetico, GRANDE, "Pantera Negra · a malha de vibranium absorvendo", False),
    ("vibranio_preparo", vibranio_preparo, MEDIA, "Pantera Negra · a energia indo para o peito (Preparo, laço)", True),
    ("descarga_real", descarga_real, GRANDE, "Pantera Negra · a esfera e a onda com os hexágonos", False),
    ("hex_de_probabilidade", hex_de_probabilidade, GRANDE, "Feiticeira · os fios, o redemoinho e o sinal", False),
    ("telecinese_escarlate", telecinese_escarlate, GRANDE, "Feiticeira · as faixas agarrando e o Preparo recuando", False),
    ("caos_preparo", caos_preparo, MEDIA, "Feiticeira · a tiara e os fios nas mãos (Preparo, laço)", True),
    ("distorcao_do_caos", distorcao_do_caos, GRANDE, "Feiticeira · a onda do caos e o espaço entortando", False),
    ("faseamento", faseamento, GRANDE, "Visão · o corpo fantasma e o golpe atravessando", False),
    ("raio_solar", raio_solar, GRANDE, "Visão · a Joia da Mente e o raio solar", False),
    ("computacao_preparo", computacao_preparo, MEDIA, "Visão · os anéis de circuito (Preparo, laço)", True),
    ("computacao_sintetica", computacao_sintetica, GRANDE, "Visão · a grade, o raio exato e o anel partido", False),
    ("encolhimento", encolhimento, GRANDE, "Homem-Formiga · os anéis, o zigue-zague e os golpes", False),
]
