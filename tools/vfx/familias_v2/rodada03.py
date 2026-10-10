"""Rodada 3 das habilidades próprias: Mulher-Maravilha, Homem de Ferro, Capitão América, Magneto e Deadpool.

Mulher-Maravilha
- laco_dourado_voo: o Laço da Verdade voando, a laçada girando aberta e a corda
  dourada atrás (laço, viagem).
- laco_da_verdade: a laçada dourada cai em volta do rival e aperta em três
  voltas, brilhando (preso e marcado), e o golpe cortado.
- braceletes_amazona: os dois braceletes cruzam em X na frente do aliado, as
  balas batem neles e ricocheteiam em faíscas, e fica o escudo dourado.
- impeto_amazona: ela chega com o escudo e a espada — a pancada do escudo, o
  corte da espada e a estrela dourada estourando (perto).

Homem de Ferro
- repulsor_stark_voo: o disparo do repulsor voando — o disco branco-azulado
  com os anéis de pressão em volta (laço, viagem).
- repulsores_stark: o repulsor estoura no rival em anéis de pressão e a
  armadura dele fica com as rachaduras (Exposto).
- protocolo_de_protecao: as placas hexagonais de nanotecnologia vermelhas e
  douradas se montam em volta do aliado até fechar o escudo.
- unibeam_carga: o reator no peito carregando — o anel e o triângulo do reator
  acendendo (Preparo, laço).
- unibeam_faixa: o feixe largo do peito, o miolo branco e os anéis correndo
  pelo feixe (faixa, laço).
- unibeam_impacto: o feixe estoura no rival.

Capitão América
- escudo_ricochete_voo: o escudo girando com a estrela e o rastro (laço, viagem
  da cadeia; o do ataque básico é outro).
- escudo_ricochete: o escudo bate e quica (o "clang", as linhas de impacto e o
  golpe cortado).
- dia_todo: "Eu posso o dia todo" — o escudo de estrela se ergue na frente do
  aliado, os anéis vermelho-branco-azul e o brilho verde de cura subindo.
- avante: "Avante!" — a estrela sobe no aliado e as linhas de vento correm para
  a frente.

Magneto
- prisao_magnetica: os aros de metal se fecham em volta do rival (três anéis
  achatados apertando) e as linhas de campo roxas, e o golpe cortado.
- muralha_de_metal: as vigas de metal voam e se empilham na frente do aliado
  formando a muralha, com o brilho do campo.
- campo_magneto: o Magneto erguendo o campo — as linhas de força roxas em volta
  e os pedaços de metal flutuando (Preparo, laço).
- colapso_magneto: os pedaços de metal vêm de todos os lados e esmagam o rival,
  com a onda roxa (Lento).

Deadpool
- plano_que_plano: o caos — os tiros das pistolas, a granada quicando e o
  "BUM" de desenho animado com estrelinhas.
- quarta_parede: o quadro de gibi em volta do rival racha e quebra (a quarta
  parede), e o ponto de interrogação gira.
- so_um_arranhao: um band-aid cola nele, descola e cai, e as bolhas de
  regeneração sobem.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _quadro(t, seed=0):
    return np.random.default_rng(seed + int(t * 997) % 9973)


def _raio(T, q, x1, y1, x2, y2, larg=0.01, depth=4, rough=0.32):
    return T.polyline(jagged(q, x1, y1, x2, y2, depth, rough), larg)


def _faiscas(T, t, seed, n, t0, alcance=0.7, tam=0.012, cx=0.0, cy=0.0, a0=0.0, a1=TAU):
    sub = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        a = sub.uniform(a0, a1)
        d = 0.08 + alcance * ease_out(rel(t, t0, t0 + 0.5), 2) * sub.uniform(0.3, 1)
        pts.append((cx + d * math.cos(a), cy + d * math.sin(a), pulso(t, t0, 0.9) * sub.uniform(0.4, 1)))
    return T.splats(pts, tam)


def _elipse(cx, cy, rx, ry, a0=0.0, a1=TAU, n=40):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * k / (n - 1)), cy + ry * math.sin(a0 + (a1 - a0) * k / (n - 1))) for k in range(n)]


# =================================================================== Mulher-Maravilha
def laco_dourado_voo(T, t, rng):
    """O Laço da Verdade voando para +x: a laçada aberta girando na frente e a corda dourada ondulando
    atrás, até a mão dela."""
    G, H = vazio(T)
    cx = 0.35
    g = TAU * t * 2
    lacada = T.polyline(_elipse(cx, 0, 0.2, 0.2 * (0.5 + 0.5 * abs(math.cos(g)))), 0.014)
    corda = [(cx - 0.2 - 1.0 * k / 20, 0.05 * math.sin(TAU * (k / 20 * 2 - t * 2))) for k in range(21)]
    C = T.polyline(corda, 0.01)
    brilho = T.gauss(cx + 0.2 * math.cos(g), 0.1 * math.sin(g), 0.04)
    G += lacada * 1.2 + C + brilho
    H += lacada * 0.4 + brilho * 0.8
    return G, H


def laco_da_verdade(T, t, rng):
    """O Laço da Verdade no rival: a laçada cai de cima em volta dele e aperta em três voltas que
    brilham uma de cada vez, a corda sai para a esquerda, e o brilho da verdade pulsa."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cai = ease_out(rel(t, 0.0, 0.2), 2)
    aperta = ease_in(rel(t, 0.2, 0.4), 1.5)
    r = 0.6 - 0.22 * aperta
    voltas = T.zero()
    for j, y in enumerate((-0.12, 0.0, 0.12)):
        acende = 0.6 + 0.6 * pulso(t, 0.35 + 0.08 * j, 0.6 + 0.08 * j)
        voltas += T.polyline(_elipse(0, y - 0.6 * (1 - cai), r, r * 0.28), 0.016) * acende
    corda = T.polyline([(-r, 0.0), (-0.7, 0.05), (-1.0, 0.0)], 0.012) * rel(t, 0.2, 0.3)
    verdade = T.gauss(0, 0, 0.3) * pulso(t, 0.4, 0.9) * 0.45
    G += (voltas * 1.2 + corda + verdade + _faiscas(T, t, 3, 10, 0.35, 0.45, 0.01)) * env
    H += (voltas * 0.4 + verdade * 0.5) * env
    return G, H


def braceletes_amazona(T, t, rng):
    """Os braceletes na frente do aliado: os dois braceletes (as faixas largas) cruzam em X, três balas
    batem neles uma depois da outra e ricocheteiam em faíscas, e fica o escudo dourado."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    p = ease_out(rel(t, 0.0, 0.2), 2.5)
    a = 0.75 * p
    B = T.zero()
    for s in (-1, 1):
        c, sn = math.cos(s * a), math.sin(s * a)
        pts = [(x * c - y * sn, x * sn + y * c + 0.05) for x, y in ((-0.07, -0.32), (0.07, -0.32), (0.07, 0.32), (-0.07, 0.32))]
        B += T.polys([(pts, 1.0)], 0.004)
    batidas = T.zero()
    for j, (x, y) in enumerate(((0.05, -0.15), (-0.08, 0.05), (0.06, 0.18))):
        t0 = 0.25 + 0.1 * j
        k = pulso(t, t0, t0 + 0.12)
        batidas += T.gauss(x, y, 0.05) * k * 1.6
        batidas += _faiscas(T, t, 7 + j, 6, t0, 0.35, 0.008, x, y, -2.6, -0.6) * 0.9
    escudo = T.arc_band(0.55, 0.035, -2.6, -0.54, 1.0, 0.0, 0, 0.1, 0.2) * rel(t, 0.25, 0.4)
    G += (B * 1.1 + batidas + escudo) * env
    H += (B * 0.4 + batidas * 0.8) * env
    return G, H


def impeto_amazona(T, t, rng):
    """O Ímpeto amazona: a pancada do escudo (o clarão redondo e o anel), o corte da espada atravessando
    e a estrela dourada de cinco pontas estourando no fim."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    k = pulso(t, 0.0, 0.3)
    pancada = T.gauss(0, 0, 0.14) * k * 1.6 + T.ring(0.1 + 0.5 * ease_out(rel(t, 0.0, 0.3), 2), 0.035) * k
    p = ease_out(rel(t, 0.18, 0.32), 2.5)
    corte = T.polys([(lamina(-0.65, 0.4, 0.65, -0.45, 0.05, p), 1.0)], 0.003) * (1 - rel(t, 0.45, 0.7))
    s = ease_out(rel(t, 0.35, 0.6), 2)
    est = T.polys([(estrela(0, 0, 0.12 + 0.3 * s, -math.pi / 2, 5, 0.42), 1.0)], 0.006) * pulso(t, 0.35, 0.9)
    G += (pancada + corte * 1.2 + est * 0.8 + _faiscas(T, t, 11, 12, 0.36, 0.6, 0.012)) * env
    H += (pancada * 0.9 + corte * 0.5 + est * 0.4) * env
    return G, H


# =================================================================== Homem de Ferro
def repulsor_stark_voo(T, t, rng):
    """O disparo do repulsor voando para +x: o disco branco-azulado e os anéis de pressão saindo dele
    para trás, um atrás do outro."""
    G, H = vazio(T)
    cx = 0.35
    nucleo = T.gauss(cx, 0, 0.07, 0.09) * 1.6
    aneis = T.zero()
    for j in range(3):
        f = (t * 2 + j / 3) % 1
        aneis += T.ring(0.08 + 0.1 * f, 0.012, cx - 0.6 * f, 0, 2.6) * (1 - f)
    rastro = T.tapered([(cx - 0.9, 0, cx - 0.05, 0, 1.0)], 0.05) * 0.5
    G += nucleo + aneis + rastro
    H += nucleo * 0.9 + rastro * 0.3
    return G, H


def repulsores_stark(T, t, rng):
    """O repulsor no rival: o estouro branco, os anéis de pressão abrindo um atrás do outro e as
    rachaduras na armadura dele (Exposto) ficando acesas."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    k = pulso(t, 0.0, 0.35)
    estouro = T.gauss(0, 0, 0.16) * k * 1.8
    aneis = T.zero()
    for j in range(3):
        t0 = 0.05 * j
        f = ease_out(rel(t, t0, t0 + 0.45), 2)
        aneis += T.ring(0.1 + 0.6 * f, 0.025, 0, 0, 1.0) * (1 - f) * (f > 0)
    q = np.random.default_rng(5)
    rach = T.zero()
    for _ in range(5):
        a = q.uniform(0, TAU)
        rach += _raio(T, q, 0.05 * math.cos(a), 0.05 * math.sin(a), 0.38 * math.cos(a), 0.38 * math.sin(a), 0.008, 3, 0.3)
    rach *= rel(t, 0.25, 0.35)
    G += (estouro + aneis * 1.1 + rach) * env
    H += (estouro * 0.9 + rach * 0.4) * env
    return G, H


def _hexagono(cx, cy, r):
    return [(cx + r * math.cos(math.pi / 6 + TAU * k / 6), cy + r * math.sin(math.pi / 6 + TAU * k / 6)) for k in range(6)]


def protocolo_de_protecao(T, t, rng):
    """O Protocolo de proteção no aliado: as placas hexagonais da nanotecnologia aparecem uma por uma
    num círculo em volta dele (cada uma acende ao encaixar) até fechar o escudo, e o brilho corre."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    placas = []
    bordas = T.zero()
    sub = np.random.default_rng(13)
    centros = []
    r = 0.11
    for i in range(-3, 4):
        for j in range(-3, 4):
            x = (i + 0.5 * (j % 2)) * r * 1.75
            y = j * r * 1.52
            if math.hypot(x, y * 1.05) < 0.6:
                centros.append((x, y))
    ordem = sorted(centros, key=lambda c: math.atan2(c[1], c[0]) + sub.uniform(0, 0.4))
    for n, (x, y) in enumerate(ordem):
        t0 = 0.02 + 0.4 * n / len(ordem)
        f = ease_out(rel(t, t0, t0 + 0.08), 2)
        if f <= 0:
            continue
        pts = _hexagono(x, y, r * 0.92 * f)
        placas.append((pts, 0.35))
        bordas += T.polyline(pts + [pts[0]], 0.006) * (0.7 + 0.8 * pulso(t, t0, t0 + 0.15))
    P = T.polys(placas, 0.004) if placas else T.zero()
    corre = T.gauss(-0.6 + 1.2 * rel(t, 0.5, 0.8), 0, 0.12, 0.5) * pulso(t, 0.5, 0.8) * 0.6
    G += (P + bordas + corre) * env
    H += (bordas * 0.3) * env
    return G, H


def unibeam_carga(T, t, rng):
    """O reator no peito carregando: o anel do reator e o triângulo de dentro acendendo, o brilho
    pulsando cada vez mais forte e as linhas de energia entrando."""
    G, H = vazio(T)
    b = 0.7 + 0.3 * math.sin(TAU * t * 3)
    anel = T.ring(0.16, 0.025) * b
    tri = T.polyline([(0.11 * math.cos(-math.pi / 2 + TAU * k / 3), 0.11 * math.sin(-math.pi / 2 + TAU * k / 3)) for k in range(4)], 0.012) * b
    miolo = T.gauss(0, 0, 0.08) * (1.2 + 0.4 * b)
    entra = []
    for k in range(10):
        a = TAU * k / 10 + 0.3
        f = (t * 2 + k * 0.37) % 1
        d = 0.6 - 0.4 * f
        entra.append((d * math.cos(a), d * math.sin(a), d * math.cos(a) * 0.9 + 0.001, d * math.sin(a) * 0.9, f))
    L = T.lines([(x1, y1, x1 * 0.85, y1 * 0.85, w) for x1, y1, _, _, w in entra], 0.008)
    G += anel + tri + miolo + L * 0.7
    H += miolo + anel * 0.4
    return G, H


def unibeam_faixa(T, t, rng):
    """O Unibeam: o feixe largo saindo do peito (borda azulada, miolo branco) com os anéis de pressão
    correndo por ele e o tremor do feixe."""
    G, H = vazio(T)
    tremor = 1 + 0.06 * math.sin(TAU * t * 9)
    corpo = np.exp(-(T.V / (0.2 * tremor)) ** 2)
    miolo = np.exp(-(T.V / (0.07 * tremor)) ** 2)
    aneis = T.zero()
    for j in range(3):
        x = -1.0 + 2.0 * ((t * 1.5 + j / 3) % 1)
        aneis += T.ring(0.2, 0.01, x, 0, 0.35) * 0.35
    G += corpo * 0.8 + miolo * 1.2 + aneis
    H += miolo * 1.1 + corpo * 0.2
    return G, H


def unibeam_impacto(T, t, rng):
    """O Unibeam no rival: o clarão enorme, o anel de choque achatado e as faíscas espalhando."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    k = pulso(t, 0.0, 0.5)
    clarao = T.gauss(0, 0, 0.25) * k * 2.0 + T.flare(0, 0, 1.2 * k + 1e-3, 0.0, 0.01) * k
    anel = T.ring(0.1 + 0.75 * ease_out(rel(t, 0.05, 0.55), 2), 0.04, 0, 0, 1.4) * pulso(t, 0.05, 0.6)
    G += (clarao + anel + _faiscas(T, t, 17, 18, 0.05, 0.7, 0.012) * 1.1) * env
    H += clarao * 1.1 * env
    return G, H


# =================================================================== Capitão América
def _escudo_cap(T, cx, cy, s, giro):
    """O escudo redondo de cima: os anéis concêntricos e a estrela do meio girando."""
    A = T.ring(0.22 * s, 0.028, cx, cy) + T.ring(0.15 * s, 0.022, cx, cy) * 0.8
    E = T.polys([(estrela(cx, cy, 0.09 * s, giro, 5, 0.42), 1.0)], 0.003)
    return A, E


def escudo_ricochete_voo(T, t, rng):
    """O escudo voando no ricochete: o escudo girando de lado (achatado e esticando no giro), o brilho
    do metal passando e o rastro de vento atrás."""
    G, H = vazio(T)
    cx = 0.3
    A, E = _escudo_cap(T, cx, 0, 1.0, TAU * t * 3)
    glint = T.gauss(cx + 0.18 * math.cos(TAU * t * 3), -0.1, 0.04) * 1.2
    rastro = T.tapered([(cx - 0.95, 0.12, cx - 0.2, 0.12, 0.6), (cx - 0.95, -0.12, cx - 0.2, -0.12, 0.6)], 0.025)
    G += A * 1.1 + E * 1.2 + glint + rastro * 0.5
    H += E * 0.4 + glint * 0.8
    return G, H


def escudo_ricochete(T, t, rng):
    """O escudo bate e quica: o "clang" (o clarão e as linhas de impacto em estrela, como num gibi), o
    escudo de lado saindo para cima e o golpe cortado."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    k = pulso(t, 0.0, 0.3)
    clang = T.gauss(0, 0, 0.12) * k * 1.7
    linhas = []
    for j in range(10):
        a = TAU * j / 10 + 0.2
        d0 = 0.18 + 0.1 * ease_out(rel(t, 0.0, 0.3), 2)
        linhas.append((d0 * math.cos(a), d0 * math.sin(a), (d0 + 0.22) * math.cos(a), (d0 + 0.22) * math.sin(a), 1.0))
    L = T.tapered(linhas, 0.025) * pulso(t, 0.0, 0.45)
    sobe = ease_out(rel(t, 0.1, 0.5), 2)
    A, E = _escudo_cap(T, 0.4 * sobe, -0.5 * sobe, 0.9, TAU * t * 4)
    quica = (A + E) * (1 - rel(t, 0.35, 0.55))
    G += (clang + L * 1.1 + quica) * env
    H += (clang * 0.9 + L * 0.4) * env
    return G, H


def dia_todo(T, t, rng):
    """Eu posso o dia todo: o escudo se ergue na frente do aliado (os anéis e a estrela crescendo com o
    "clang"), o anel de luz ao redor e o brilho de cura subindo em cruzinhas."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = back(rel(t, 0.0, 0.3), 1.5)
    A, E = _escudo_cap(T, 0, 0.05, 2.2 * s + 0.01, -math.pi / 2)
    k = pulso(t, 0.2, 0.45)
    clang = T.gauss(0, 0.05, 0.15) * k * 1.2
    sub = np.random.default_rng(23)
    cruzes = []
    for _ in range(9):
        x = sub.uniform(-0.5, 0.5)
        f = (sub.uniform() + t * 0.8) % 1
        y = 0.5 - 1.0 * f
        a = (1 - f) * rel(t, 0.3, 0.45)
        cruzes += [(x - 0.03, y, x + 0.03, y, a), (x, y - 0.03, x, y + 0.03, a)]
    C = T.lines(cruzes, 0.01)
    G += (A * 1.1 + E * 1.2 + clang + C * 0.8) * env
    H += (E * 0.4 + clang) * env
    return G, H


def avante(T, t, rng):
    """Avante!: a estrela branca sobe no aliado girando, o anel abre no pé e as linhas de vento correm
    para a frente, cada vez mais rápidas."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    y = 0.3 - 0.75 * ease_out(rel(t, 0.0, 0.5), 2)
    est = T.polys([(estrela(0, y, 0.14, -math.pi / 2 + t * 2, 5, 0.42), 1.0)], 0.005) * rel(t, 0.0, 0.1)
    brilho = T.gauss(0, y, 0.12) * 0.7
    anel = T.ring(0.1 + 0.5 * ease_out(rel(t, 0.0, 0.4), 2), 0.025, 0, 0.45, 3.5) * pulso(t, 0.0, 0.5)
    sub = np.random.default_rng(29)
    vento = []
    for _ in range(10):
        yy = sub.uniform(-0.5, 0.5)
        f = (sub.uniform() + t * 2.2) % 1
        x = -0.9 + 1.8 * f
        vento.append((x - 0.25, yy, x, yy, (1 - abs(2 * f - 1)) * rel(t, 0.15, 0.3)))
    V = T.tapered(vento, 0.012)
    G += (est * 1.2 + brilho + anel + V * 0.7) * env
    H += (est * 0.5 + brilho * 0.6) * env
    return G, H


# =================================================================== Magneto
def prisao_magnetica(T, t, rng):
    """A Prisão magnética: três aros de metal vêm de longe e se fecham em volta do rival (anéis
    achatados apertando, um em cima do outro), as linhas de campo roxas curvam em volta e o golpe é
    cortado com o estalo."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    A = T.zero()
    for j, y in enumerate((-0.25, 0.0, 0.25)):
        t0 = 0.05 * j
        f = ease_in(rel(t, t0, t0 + 0.25), 1.6)
        r = 0.95 - 0.55 * f
        A += T.ring(r, 0.03, 0, y, 1 / 0.3) * rel(t, t0, t0 + 0.05)
        A += T.ring(r, 0.012, 0, y - 0.015, 1 / 0.3) * 0.6 * rel(t, t0, t0 + 0.05)
    campo = T.zero()
    for j in range(4):
        r = 0.45 + 0.08 * j
        campo += T.arc_band(r, 0.008, -math.pi * 0.9 + t, -math.pi * 0.1 + t, 0.8, 0.0, 0, 0, 1.0) * 0.5
        campo += T.arc_band(r, 0.008, math.pi * 0.1 + t, math.pi * 0.9 + t, 0.8, 0.0, 0, 0, 1.0) * 0.5
    campo *= rel(t, 0.25, 0.4)
    k = pulso(t, 0.28, 0.5)
    estalo = T.gauss(0, 0, 0.18) * k * 1.2
    G += (A * 1.1 + campo + estalo) * env
    H += (A * 0.35 + estalo * 0.8) * env
    return G, H


def muralha_de_metal(T, t, rng):
    """A Muralha de metal no aliado: as vigas de metal voam de fora e se empilham na frente dele, uma por
    vez (cada uma com o baque), formando a parede; o campo roxo brilha nas bordas."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    vigas = []
    bordas = T.zero()
    baques = T.zero()
    sub = np.random.default_rng(31)
    for j in range(5):
        t0 = 0.05 + 0.08 * j
        f = ease_out(rel(t, t0, t0 + 0.12), 2.5)
        if f <= 0:
            continue
        lado = -1 if j % 2 else 1
        y = 0.4 - 0.18 * j
        x = lado * 1.2 * (1 - f)
        ang = sub.uniform(-0.08, 0.08) * f + lado * 0.6 * (1 - f)
        c, s = math.cos(ang), math.sin(ang)
        pts = [(x + px * c - py * s, y + px * s + py * c) for px, py in ((-0.5, -0.07), (0.5, -0.07), (0.5, 0.07), (-0.5, 0.07))]
        vigas.append((pts, 0.55))
        bordas += T.polyline(pts + [pts[0]], 0.008)
        baques += T.gauss(0, y, 0.25, 0.06) * pulso(t, t0 + 0.1, t0 + 0.25)
    V = T.polys(vigas, 0.004) if vigas else T.zero()
    campo = T.ring(0.68, 0.02, 0, -0.0, 1.2) * rel(t, 0.45, 0.6) * (0.6 + 0.3 * math.sin(TAU * t * 2))
    G += (V + bordas + baques * 0.8 + campo) * env
    H += (bordas * 0.3 + baques * 0.4) * env
    return G, H


def campo_magneto(T, t, rng):
    """O Magneto erguendo o campo: as linhas de força roxas em laços dos dois lados dele, girando, e os
    pedaços de metal flutuando em volta, subindo e descendo."""
    G, H = vazio(T)
    L = T.zero()
    for j in range(3):
        r = 0.18 + 0.1 * j
        for s in (-1, 1):
            L += T.polyline(_elipse(s * r, 0, r, r * 0.55, n=36), 0.008) * (0.7 - 0.15 * j)
    L *= 0.7 + 0.3 * math.sin(TAU * t * 2)
    sub = np.random.default_rng(37)
    pedacos = []
    for k in range(7):
        a = TAU * k / 7 + TAU * t * 0.5
        d = 0.65 + 0.05 * math.sin(TAU * (t + k * 0.3))
        cx, cy = d * math.cos(a), d * 0.7 * math.sin(a)
        w = sub.uniform(0.03, 0.06)
        g = TAU * t + k
        c, s = math.cos(g), math.sin(g)
        pedacos.append(([(cx + px * c - py * s, cy + px * s + py * c) for px, py in ((-w, -w * 0.6), (w, -w * 0.4), (w * 0.8, w * 0.6), (-w * 0.7, w * 0.5))], 0.9))
    P = T.polys(pedacos, 0.004)
    G += L + P * 1.1 + T.gauss(0, 0, 0.15) * 0.5
    H += P * 0.3
    return G, H


def colapso_magneto(T, t, rng):
    """O Colapso no rival: os pedaços de metal vêm de todos os lados e se esmagam nele (convergindo e
    girando), o estouro, a onda roxa achatada e as linhas de campo puxando para baixo (Lento)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    f = ease_in(rel(t, 0.0, 0.3), 2)
    sub = np.random.default_rng(41)
    pedacos = []
    for k in range(12):
        a = TAU * k / 12 + sub.uniform(-0.2, 0.2)
        d = 1.0 - 0.85 * f
        cx, cy = d * math.cos(a), d * 0.8 * math.sin(a)
        w = sub.uniform(0.04, 0.08)
        g = a + TAU * t * 2
        c, s = math.cos(g), math.sin(g)
        pedacos.append(([(cx + px * c - py * s, cy + px * s + py * c) for px, py in ((-w, -w * 0.5), (w, -w * 0.6), (w * 0.9, w * 0.6), (-w, w * 0.4))], 1.0))
    P = T.polys(pedacos, 0.004) * (1 - rel(t, 0.35, 0.5))
    k = pulso(t, 0.28, 0.6)
    estouro = T.gauss(0, 0, 0.2) * k * 1.6
    onda = T.ring(0.1 + 0.8 * ease_out(rel(t, 0.3, 0.75), 2), 0.035, 0, 0.1, 2.2) * pulso(t, 0.3, 0.8)
    puxa = T.lines([(x, -0.3 + 0.5 * ((t * 1.5 + j * 0.3) % 1), x, -0.15 + 0.5 * ((t * 1.5 + j * 0.3) % 1), 1.0) for j, x in enumerate((-0.3, -0.1, 0.1, 0.3))], 0.01) * rel(t, 0.45, 0.6) * 0.6
    G += (P * 1.1 + estouro + onda + puxa) * env
    H += (estouro * 0.9 + P * 0.3) * env
    return G, H


# =================================================================== Deadpool
def plano_que_plano(T, t, rng):
    """Plano? Que plano?: o caos — os tiros das duas pistolas acertando em pontos diferentes (cada um
    com o clarão pequeno), a granada caindo e quicando e o "BUM" de desenho animado (a nuvem de bolinhas
    com o anel e as estrelinhas)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    tiros = T.zero()
    for j, (x, y) in enumerate(((-0.25, -0.1), (0.2, 0.15), (-0.05, -0.3), (0.3, -0.2))):
        t0 = 0.04 * j * 1.6
        k = pulso(t, t0, t0 + 0.08)
        tiros += (T.gauss(x, y, 0.05) * 1.6 + T.flare(x, y, 0.25 * k + 1e-3, 0.5, 0.006)) * k
    g = rel(t, 0.15, 0.4)
    gx, gy = -0.5 + 0.5 * g, -0.4 + 0.75 * g - 0.5 * math.sin(math.pi * g) * 0.6
    granada = T.gauss(gx, gy, 0.035) * (1 - rel(t, 0.38, 0.42)) * (g > 0) * 1.4
    k = pulso(t, 0.4, 0.85)
    sub = np.random.default_rng(43)
    bolas = []
    for _ in range(10):
        a = sub.uniform(0, TAU)
        d = 0.25 * ease_out(rel(t, 0.4, 0.6), 2) * sub.uniform(0.3, 1)
        bolas.append((d * math.cos(a), 0.15 + d * math.sin(a) * 0.8, k))
    bum = T.splats(bolas, 0.1) * 0.9 + T.ring(0.15 + 0.5 * ease_out(rel(t, 0.4, 0.8), 2), 0.03, 0, 0.15) * k
    estrelinhas = T.polys([(estrela(0.55 * math.cos(a), 0.15 + 0.45 * math.sin(a), 0.05, a, 5, 0.42), k) for a in (0.4, 1.7, 2.9, 4.2, 5.4)], 0.003) * rel(t, 0.5, 0.6)
    G += (tiros + granada + bum + estrelinhas) * env
    H += (tiros * 0.9 + bum * 0.5) * env
    return G, H


def quarta_parede(T, t, rng):
    """A Quarta parede: o quadro de gibi aparece em volta do rival, racha do canto e quebra em cacos que
    caem, e o ponto de interrogação fica girando em cima dele (confuso)."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    quebra = rel(t, 0.35, 0.8)
    q = np.random.default_rng(47)
    W2, H2 = 0.55, 0.6
    if quebra <= 0:
        quadro = T.polyline([(-W2, -H2), (W2, -H2), (W2, H2), (-W2, H2), (-W2, -H2)], 0.025) * rel(t, 0.0, 0.1)
        rach = T.zero()
        if t > 0.2:
            for _ in range(4):
                a = q.uniform(math.pi * 0.6, math.pi * 1.4)
                rach += _raio(T, q, W2, -H2, W2 + 0.9 * math.cos(a), -H2 - 0.9 * math.sin(a) * -1, 0.008, 4, 0.3)
            rach *= rel(t, 0.2, 0.3)
        G += (quadro + rach) * env
        H += quadro * 0.3 * env
    else:
        cacos = []
        lados = [((-W2, -H2), (W2, -H2)), ((W2, -H2), (W2, H2)), ((W2, H2), (-W2, H2)), ((-W2, H2), (-W2, -H2))]
        for (x1, y1), (x2, y2) in lados:
            for k in range(4):
                u0, u1 = k / 4, (k + 1) / 4
                ax, ay = x1 + (x2 - x1) * u0, y1 + (y2 - y1) * u0
                bx, by = x1 + (x2 - x1) * u1, y1 + (y2 - y1) * u1
                dx, dy = q.uniform(-0.3, 0.3) * quebra, 0.6 * quebra ** 2 + q.uniform(0, 0.2) * quebra
                cacos.append((ax + dx, ay + dy, bx + dx, by + dy + q.uniform(-0.05, 0.05) * quebra, 1 - quebra))
        G += T.lines(cacos, 0.022) * env
    s = 0.2
    cy = -0.25 + 0.03 * math.sin(TAU * t * 2)
    gira = TAU * t * 1.2
    arco = [(0.09 * math.cos(a) * math.cos(gira), cy - 0.1 + 0.09 * math.sin(a)) for a in np.linspace(-math.pi, 0.4 * math.pi, 14)]
    interr = T.polyline(arco + [(0.0, cy + 0.04)], 0.018) + T.gauss(0, cy + 0.12, 0.022) * 1.5
    G += interr * rel(t, 0.3, 0.45) * env * (1 + s * 0)
    H += interr * 0.4 * rel(t, 0.3, 0.45) * env
    return G, H


def so_um_arranhao(T, t, rng):
    """Só um arranhão: um band-aid só (a fita com a almofadinha no meio) cola no corpo dele com o "pop",
    descola e cai girando, e as bolhas de regeneração sobem com o brilho."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = back(rel(t, 0.0, 0.2), 2.0)
    cai = ease_in(rel(t, 0.45, 0.85), 2)
    cx, cy = 0.15 * cai, -0.05 + 0.8 * cai
    aa = -0.5 + 4.0 * cai
    c, sn = math.cos(aa), math.sin(aa)
    gira = lambda pts: [(cx + px * c - py * sn, cy + px * sn + py * c) for px, py in pts]  # noqa: E731
    fita = gira([(-0.3 * s, -0.07 * s), (0.3 * s, -0.07 * s), (0.34 * s, 0.0), (0.3 * s, 0.07 * s), (-0.3 * s, 0.07 * s), (-0.34 * s, 0.0)])
    almofada = gira([(-0.09 * s, -0.055 * s), (0.09 * s, -0.055 * s), (0.09 * s, 0.055 * s), (-0.09 * s, 0.055 * s)])
    some = 1 - rel(t, 0.75, 0.9)
    F = T.polys([(fita, 0.55 * some)], 0.004) + T.polys([(almofada, 1.0 * some)], 0.003)
    borda = T.polyline(fita + [fita[0]], 0.008) * some
    pop = T.ring(0.1 + 0.3 * ease_out(rel(t, 0.0, 0.25), 2), 0.02) * pulso(t, 0.0, 0.3)
    sub = np.random.default_rng(53)
    bolhas = []
    for _ in range(16):
        x = sub.normal(0, 0.22)
        f = (sub.uniform() + t * 0.9) % 1
        bolhas.append((x, 0.45 - 0.9 * f, (1 - f) * rel(t, 0.3, 0.5)))
    B = T.splats(bolhas, 0.025)
    G += (F * 1.1 + borda + pop + B * 0.9 + T.gauss(0, 0, 0.3) * pulso(t, 0.4, 0.9) * 0.3) * env
    H += (F * 0.3 + B * 0.4) * env
    return G, H


REGISTRO = [
    ("laco_dourado_voo", laco_dourado_voo, MEDIA, "Mulher-Maravilha · o Laço da Verdade voando (laço)", True),
    ("laco_da_verdade", laco_da_verdade, GRANDE, "Mulher-Maravilha · a laçada apertando o rival", False),
    ("braceletes_amazona", braceletes_amazona, GRANDE, "Mulher-Maravilha · os braceletes defendendo o aliado", False),
    ("impeto_amazona", impeto_amazona, GRANDE, "Mulher-Maravilha · escudo, espada e a estrela", False),
    ("repulsor_stark_voo", repulsor_stark_voo, MEDIA, "Homem de Ferro · o repulsor voando (laço)", True),
    ("repulsores_stark", repulsores_stark, GRANDE, "Homem de Ferro · o repulsor estourando", False),
    ("protocolo_de_protecao", protocolo_de_protecao, GRANDE, "Homem de Ferro · as placas hexagonais no aliado", False),
    ("unibeam_carga", unibeam_carga, MEDIA, "Homem de Ferro · o reator carregando (Preparo, laço)", True),
    ("unibeam_faixa", unibeam_faixa, MEDIA, "Homem de Ferro · o feixe do Unibeam (faixa, laço)", True),
    ("unibeam_impacto", unibeam_impacto, GRANDE, "Homem de Ferro · o Unibeam no rival", False),
    ("escudo_ricochete_voo", escudo_ricochete_voo, MEDIA, "Capitão América · o escudo quicando (laço)", True),
    ("escudo_ricochete", escudo_ricochete, GRANDE, "Capitão América · o clang do escudo", False),
    ("dia_todo", dia_todo, GRANDE, "Capitão América · o escudo erguido e a cura", False),
    ("avante", avante, GRANDE, "Capitão América · a estrela e o vento do Avante", False),
    ("prisao_magnetica", prisao_magnetica, GRANDE, "Magneto · os aros de metal prendendo", False),
    ("muralha_de_metal", muralha_de_metal, GRANDE, "Magneto · as vigas formando a muralha", False),
    ("campo_magneto", campo_magneto, MEDIA, "Magneto · o campo e os pedaços de metal (Preparo, laço)", True),
    ("colapso_magneto", colapso_magneto, GRANDE, "Magneto · o metal esmagando o rival", False),
    ("plano_que_plano", plano_que_plano, GRANDE, "Deadpool · tiros, granada e o BUM", False),
    ("quarta_parede", quarta_parede, GRANDE, "Deadpool · o quadro do gibi quebrando", False),
    ("so_um_arranhao", so_um_arranhao, GRANDE, "Deadpool · o band-aid e a regeneração", False),
]
