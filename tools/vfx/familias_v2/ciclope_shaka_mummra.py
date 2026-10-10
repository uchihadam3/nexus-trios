"""As habilidades do Ciclope, do Shaka de Virgem e do Mumm-Ra, desenhadas para eles.

Ciclope
- varredura_optica: a Rajada de contenção em cada rival — o feixe sai do
  Ciclope (feixe_ciclope, varrendo a fileira) e, quando passa por ele, o ponto
  quente corre e deixa o risco queimado e as faíscas.
- laser_curto: o tiro curto do Ricochete óptico voando (laço, viagem) — sai do
  Ciclope, bate no rival do meio e quica de um rival para o outro.
- ricochete_optico: o quique em cada rival — o clarão e as faíscas.
- visor_carregando: o visor acendendo — a linha vermelha crescendo e pulsando
  (Preparo, laço).
- feixe_ciclope: o Feixe concentrado — o raio largo e reto com as ondas de
  pressão correndo (faixa, laço).
- feixe_concentrado: o feixe batendo no rival e empurrando, com o X do golpe
  cortado.

Shaka
- tesouro_do_ceu: o lótus abrindo no rival e os cinco sentidos (cinco luzes)
  sendo puxados para fora e se apagando, um a um.
- khan_escudo: o Todo-poderoso (Khan) — a esfera dourada fechando em volta do
  aliado com o lótus e os raios.
- lotus_shaka: a mandala dourada girando atrás dele no Preparo (laço).
- seis_mundos: a Rendição dos Seis Mundos — os seis portais abrindo em roda no
  campo dos rivais e puxando tudo para o centro.

Mumm-Ra
- espiritos_antigos: os quatro espíritos antigos voando em espiral até o rival
  (fantasmas com caveira), e o impacto escuro.
- mumm_ra_desperta: a forma desperta — as faixas de múmia se soltando e voando,
  os raios vermelhos e a aura escura subindo.
- sarcofago_preparo: os hieróglifos acendendo em volta dele e a fumaça escura
  (Preparo, laço).
- sarcofago_maldito: o sarcófago gigante subindo no campo dos rivais, os olhos
  vermelhos, as faixas de hieróglifos e a escuridão fechando.
"""
from __future__ import annotations

import math

import numpy as np

from .base import FAIXA, GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _quadro(t, seed=0):
    return np.random.default_rng(seed + int(t * 997) % 9973)


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


# =================================================================== Ciclope
def varredura_optica(T, t, rng):
    """A Rajada de contenção em cada rival: o feixe (que sai do Ciclope e varre a fileira) passa por
    ele da esquerda para a direita — o ponto quente corre, deixa o risco queimado e as faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    varre = ease_out(rel(t, 0.0, 0.35), 1.6)
    px, py = -0.6 + 1.2 * varre, 0.04 * math.sin(TAU * t * 7)
    vivo = 1 - rel(t, 0.35, 0.5)
    ponto = T.gauss(px, py, 0.13) * vivo * 1.5
    marca = T.lines([(-0.6, 0.0, px, 0.0, 1.0)], 0.03) * (1 - rel(t, 0.45, 0.95))
    brasa = T.blur(marca, 0.03) * 0.6
    q = _quadro(t, 3)
    fa = T.splats([(px + q.normal(0, 0.06), py + q.uniform(-0.25, 0.08), q.uniform(0.5, 1)) for _ in range(12)], 0.012) * vivo
    G += (ponto + marca * 1.2 + brasa + fa * 1.2) * env
    H += (ponto * 1.1 + marca * 0.7) * env
    return G, H



def laser_curto(T, t, rng):
    """O tiro do Ricochete óptico voando para +x: um laser curto (não o feixe inteiro), a ponta
    clara, o rastro afinando e a borda tremendo."""
    G, H = vazio(T)
    tremor = 0.9 + 0.1 * math.sin(TAU * t * 9)
    corpo = T.tapered([(-0.55, 0.0, 0.35, 0.0, 1.0)], 0.12) * tremor
    miolo = T.tapered([(-0.35, 0.0, 0.35, 0.0, 1.0)], 0.04)
    ponta = T.gauss(0.33, 0, 0.07)
    G += T.blur(corpo, 0.03) * 0.8 + corpo * 0.5 + miolo * 1.3 + ponta * 1.4
    H += miolo * 1.2 + ponta * 1.2
    return G, H

def ricochete_optico(T, t, rng):
    """O Ricochete óptico em cada rival: o raio bate e quica — o clarão, a estrela de faíscas que
    espirra para o lado de onde o raio sai de novo e o anel."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    k = pulso(t, 0.0, 0.4)
    clarao = T.gauss(0, 0, 0.18) * k * 1.8 + T.flare(0, 0, 1.0 * k + 1e-3, 0.5, 0.01) * k
    anel = T.ring(0.1 + 0.45 * ease_out(rel(t, 0.0, 0.45), 2), 0.035) * pulso(t, 0.0, 0.5)
    sai = ease_out(rel(t, 0.0, 0.35), 2)
    raios = T.tapered([(0.08 * math.cos(a), 0.08 * math.sin(a), (0.12 + 0.5 * sai) * math.cos(a) + 1e-3, (0.12 + 0.5 * sai) * math.sin(a), 1.0) for a in (-0.5, -0.15, 0.2, 0.55, 2.6, 3.6)], 0.035) * pulso(t, 0.0, 0.5)
    q = _quadro(t, 7)
    fa = T.splats([(q.normal(0.25 * sai, 0.15), q.normal(0, 0.15), q.uniform(0.4, 1)) for _ in range(10)], 0.011) * pulso(t, 0.05, 0.7)
    G += (clarao + anel + raios * 1.1 + fa) * env
    H += (clarao * 1.1 + raios * 0.6) * env
    return G, H


def visor_carregando(T, t, rng):
    """O visor acendendo no Preparo: a linha vermelha horizontal crescendo e ficando mais forte,
    pulsando, com o brilho escapando pelas pontas."""
    G, H = vazio(T)
    pul = 0.75 + 0.25 * math.sin(TAU * t * 5)
    linha = T.lines([(-0.45, 0.0, 0.45, 0.0, 1.0)], 0.06)
    pontas = T.gauss(-0.48, 0, 0.06) + T.gauss(0.48, 0, 0.06)
    G += linha * 1.3 * pul + T.blur(linha, 0.05) * 0.8 * pul + pontas * pul
    H += T.lines([(-0.45, 0.0, 0.45, 0.0, 1.0)], 0.02) * 1.4 * pul
    return G, H


def feixe_ciclope(T, t, rng):
    """O Feixe concentrado: o raio largo e reto do visor (−x) até o rival, com as ondas de pressão
    (anéis achatados) correndo ao longo dele e o miolo muito claro."""
    G, H = vazio(T)
    alto = T.H / T.W
    corpo = np.exp(-(T.V / (alto * 0.32)) ** 2)
    miolo = np.exp(-(T.V / (alto * 0.1)) ** 2)
    ondas = T.zero()
    for j in range(5):
        x = -0.95 + 1.9 * ((t * 1.5 + j / 5) % 1)
        ondas += np.exp(-((T.U - x) / 0.025) ** 2) * np.exp(-(T.V / (alto * 0.55)) ** 2)
    G += corpo * 0.8 + miolo * 1.2 + ondas * 0.6 + T.gauss(-0.95, 0, 0.05, alto * 0.5)
    H += miolo * 1.4 + ondas * 0.2
    return G, H


def feixe_concentrado(T, t, rng):
    """O feixe batendo no rival: o clarão, o empurrão (as linhas de pressão saindo para +x), o anel
    e o X do golpe cortado aparecendo (Interrupção)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    k = pulso(t, 0.0, 0.45)
    clarao = T.gauss(-0.05, 0, 0.26) * k * 1.8 + T.flare(-0.05, 0, 1.1 * k + 1e-3, 0.0, 0.01) * k
    empurra = T.tapered([(0.0, y, 0.2 + 0.7 * ease_out(rel(t, 0.05, 0.5), 2), y * 1.4, 1.0) for y in (-0.25, -0.1, 0.1, 0.25)], 0.03) * pulso(t, 0.05, 0.6)
    anel = T.ring(0.12 + 0.6 * ease_out(rel(t, 0.0, 0.5), 2), 0.035, 0, 0, 1.0) * pulso(t, 0.0, 0.55)
    x = pulso(t, 0.35, 0.9)
    X = T.lines([(-0.2, -0.2, 0.2, 0.2, 1.0), (-0.2, 0.2, 0.2, -0.2, 1.0)], 0.05) * x
    G += (clarao + empurra * 0.9 + anel + X * 1.2) * env
    H += (clarao * 1.1 + anel * 0.3 + X * 0.7) * env
    return G, H


# =================================================================== Shaka
def _lotus(T, cx, cy, r, abre, n=8, giro=0.0, sq=1.0):
    """Um lótus visto de frente: pétalas pontudas em volta do centro, abrindo com `abre`."""
    formas = []
    for k in range(n):
        a = giro + TAU * k / n
        comp = r * (0.4 + 0.6 * abre)
        formas.append((lamina(cx + 0.15 * r * math.cos(a), cy + 0.15 * r * math.sin(a) * sq, cx + comp * math.cos(a), cy + comp * math.sin(a) * sq, r * 0.22), 1.0))
    return T.polys(formas, 0.005)


def tesouro_do_ceu(T, t, rng):
    """O Tesouro do Céu no rival: o lótus dourado abrindo atrás dele, as cinco luzes (os cinco
    sentidos) saindo do corpo em volta, uma a uma, e se apagando — o rival fica cego e marcado."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = ease_out(rel(t, 0.0, 0.35), 2)
    L = _lotus(T, 0, 0, 0.75, abre, 10, t * 0.6) * (0.5 + 0.5 * (1 - rel(t, 0.7, 1.0)))
    anel = T.ring(0.78 * abre + 1e-3, 0.015) * 0.7
    luzes = T.zero()
    for j in range(5):
        ini = 0.25 + 0.1 * j
        f = rel(t, ini, ini + 0.3)
        if f <= 0:
            continue
        a = -math.pi / 2 + TAU * j / 5
        d = 0.1 + 0.45 * ease_out(f, 2)
        luzes += T.gauss(d * math.cos(a), d * math.sin(a), 0.05) * (1 - rel(t, ini + 0.25, ini + 0.4)) * 1.4
    olho = T.zero()
    fecha = rel(t, 0.7, 0.85)
    if t > 0.65:
        olho += T.arc_band(0.18, 0.02, math.pi * 0.1, math.pi * 0.9, 1 / (0.6 * (1 - fecha) + 0.05), 0.0, 0, 0)
        olho += T.arc_band(0.18, 0.02, -math.pi * 0.9, -math.pi * 0.1, 1 / (0.6 * (1 - fecha) + 0.05), 0.0, 0, 0)
    G += (L * 0.4 + anel + luzes * 1.3 + olho * 1.1) * env
    H += (L * 0.2 + luzes * 0.9 + olho * 0.5) * env
    return G, H


def khan_escudo(T, t, rng):
    """O Todo-poderoso (Khan) no aliado: a esfera dourada fechando em volta dele (de baixo para
    cima), o lótus no chão e os raios saindo da esfera."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    fecha = ease_out(rel(t, 0.0, 0.45), 2)
    corte = 1 / (1 + np.exp(-(T.V - (0.6 - 1.3 * fecha)) / 0.02))
    esfera = (T.ring(0.6, 0.04) * 1.1 + np.clip(1 - T.RAD / 0.6, 0, 1) ** 0.5 * (T.RAD < 0.6) * 0.18) * corte
    L = _lotus(T, 0, 0.55, 0.5, rel(t, 0.1, 0.4), 8, 0.0, 0.3) * 0.8
    raios = T.zero()
    for j in range(12):
        a = TAU * j / 12 + t * 0.5
        raios += T.tapered([(0.62 * math.cos(a), 0.62 * math.sin(a), 0.85 * math.cos(a) + 1e-3, 0.85 * math.sin(a), 1.0)], 0.025)
    raios *= pulso(t, 0.4, 0.9)
    respira = 0.85 + 0.15 * math.sin(TAU * t * 3)
    G += (esfera * respira + L + raios * 0.8) * env
    H += (esfera * 0.3 + L * 0.2 + raios * 0.3) * env
    return G, H


def lotus_shaka(T, t, rng):
    """A mandala dourada girando atrás do Shaka no Preparo: dois anéis de lótus girando em sentidos
    contrários e o brilho no meio (ele meditando)."""
    G, H = vazio(T)
    pul = 0.85 + 0.15 * math.sin(TAU * t * 2)
    L1 = _lotus(T, 0, 0, 0.8, 1.0, 12, TAU * t / 6)
    L2 = _lotus(T, 0, 0, 0.5, 1.0, 8, -TAU * t / 4)
    aneis = T.ring(0.82, 0.012) + T.ring(0.52, 0.012) * 0.8
    G += (L1 * 0.6 + L2 * 0.8 + aneis * 0.8) * pul + T.gauss(0, 0, 0.18) * 0.9
    H += L2 * 0.3 + T.gauss(0, 0, 0.1) * 0.8
    return G, H


def seis_mundos(T, t, rng):
    """A Rendição dos Seis Mundos: os seis portais (círculos com espiral dentro) abrindo em roda no
    campo dos rivais, girando, e puxando tudo para o centro, que fecha num clarão."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = back(rel(t, 0.0, 0.35), 1.3)
    puxa = ease_in(rel(t, 0.55, 0.85), 1.5)
    portais = T.zero()
    for j in range(6):
        a = TAU * j / 6 + t * 1.2
        r = 0.62 * (1 - 0.8 * puxa)
        cx, cy = r * math.cos(a), r * math.sin(a) * 0.6
        rp = 0.15 * abre * (1 - 0.6 * puxa) + 1e-3
        portais += T.ring(rp, 0.02, cx, cy)
        portais += T.arc_band(rp * 0.7, 0.015, a, a + 4, 1.0, 0.0, cx, cy, 0.6)
    mandala = T.ring(0.62 * abre * (1 - 0.8 * puxa) + 1e-3, 0.012, 0, 0, 1 / 0.6) * 0.6
    k = pulso(t, 0.8, 1.0)
    clarao = T.gauss(0, 0, 0.3) * k * 1.8 + T.flare(0, 0, 1.2 * k + 1e-3, 0.0, 0.01) * k
    G += (portais * 1.2 + T.blur(portais, 0.02) * 0.5 + mandala + clarao) * env
    H += (portais * 0.5 + clarao * 1.0) * env
    return G, H


# =================================================================== Mumm-Ra
def _fantasma(T, x, y, r, ang):
    """Um espírito: a cabeça redonda com os olhos vazios e a cauda de fumaça para trás."""
    cabeca = T.gauss(x, y, r)
    olhos = T.gauss(x + 0.4 * r * math.cos(ang + 0.6), y + 0.4 * r * math.sin(ang + 0.6), r * 0.25) + T.gauss(x + 0.4 * r * math.cos(ang - 0.6), y + 0.4 * r * math.sin(ang - 0.6), r * 0.25)
    cauda = T.tapered([(x - 4 * r * math.cos(ang), y - 4 * r * math.sin(ang), x + 1e-3, y, 1.0)], r * 1.6)
    return np.clip(cabeca * 1.2 - olhos * 1.4, 0, None) + T.blur(cauda, 0.015) * 0.6


def espiritos_antigos(T, t, rng):
    """Os Antigos Espíritos: quatro fantasmas vêm de −x em espiral, cada um num caminho, e entram no
    rival um depois do outro; o impacto escuro abre."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    F = T.zero()
    for j in range(4):
        ini = 0.06 * j
        f = ease_in(rel(t, ini, ini + 0.45), 1.3)
        if f <= 0 or f >= 1:
            continue
        a = TAU * (f * 1.2 + j / 4)
        r = 0.6 * (1 - f)
        x = -0.9 * (1 - f) + r * math.cos(a) * 0.4
        y = r * math.sin(a) * 0.6
        F += _fantasma(T, x, y, 0.1, math.atan2(-y, -x + 1e-3) + math.pi)
    k = pulso(t, 0.35, 0.8)
    escuro = T.gauss(0, 0, 0.25) * k * 1.2
    anel = T.ring(0.1 + 0.6 * ease_out(rel(t, 0.4, 0.8), 2), 0.04) * pulso(t, 0.4, 0.85)
    G += (F * 1.1 + escuro + anel) * env
    H += (F * 0.3 + anel * 0.3) * env
    return G, H


def mumm_ra_desperta(T, t, rng):
    """A Forma desperta: as faixas de múmia se soltam do corpo e voam rodando para fora, os raios
    vermelhos estalam e a aura escura sobe."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sub = np.random.default_rng(61)
    faixas = T.zero()
    for j in range(8):
        a = TAU * j / 8 + sub.uniform(-0.3, 0.3)
        f = ease_out(rel(t, 0.05 + 0.03 * j, 0.7), 1.6)
        d = 0.15 + 0.7 * f
        pts = []
        for k in range(8):
            g = k / 7
            dd = d - 0.35 * g
            aa = a + 0.6 * g + 1.5 * f
            pts.append((dd * math.cos(aa), dd * math.sin(aa) - 0.2 * f * f))
        faixas += T.polyline(pts, 0.03) * (1 - rel(t, 0.6, 0.85))
    q = _quadro(t, 63)
    raios = T.zero()
    for _ in range(3):
        a = q.uniform(0, TAU)
        raios += T.polyline(jagged(q, 0.1 * math.cos(a), 0.1 * math.sin(a), 0.55 * math.cos(a), 0.55 * math.sin(a), 3, 0.35), 0.012)
    raios *= pulso(t, 0.1, 0.8)
    aura = T.zero()
    for j in range(14):
        x = sub.uniform(-0.45, 0.45)
        f = (sub.uniform() + t * 1.2) % 1
        aura += T.gauss(x, 0.5 - 1.1 * f, 0.08) * (1 - f) * 0.5
    aura *= rel(t, 0.2, 0.4)
    G += (faixas * 1.0 + raios * 1.2 + aura) * env
    H += (faixas * 0.3 + raios * 0.8) * env
    return G, H


def _hieroglifo(cx, cy, r, tipo):
    """Um hieróglifo simples (olho, cruz ansata ou pássaro estilizado), como segmentos."""
    if tipo == 0:   # o olho
        return [(cx - r, cy, cx, cy - 0.5 * r, 1.0), (cx, cy - 0.5 * r, cx + r, cy, 1.0), (cx - r, cy, cx + r, cy, 1.0), (cx, cy, cx - 0.3 * r, cy + 0.8 * r, 1.0)]
    if tipo == 1:   # a cruz ansata
        return [(cx, cy - 0.2 * r, cx, cy + r, 1.0), (cx - 0.5 * r, cy, cx + 0.5 * r, cy, 1.0), (cx - 0.3 * r, cy - 0.2 * r, cx, cy - r, 1.0), (cx, cy - r, cx + 0.3 * r, cy - 0.2 * r, 1.0)]
    return [(cx - r, cy + 0.6 * r, cx, cy - 0.6 * r, 1.0), (cx, cy - 0.6 * r, cx + r, cy, 1.0), (cx + r, cy, cx - 0.2 * r, cy + 0.2 * r, 1.0)]


def sarcofago_preparo(T, t, rng):
    """O Preparo do Retorno ao sarcófago: os hieróglifos acendendo em roda em volta do Mumm-Ra, um de
    cada vez, e a fumaça escura subindo."""
    G, H = vazio(T)
    segs = []
    for j in range(8):
        a = TAU * j / 8 + t * 0.4
        segs += _hieroglifo(0.62 * math.cos(a), 0.62 * math.sin(a) * 0.7, 0.12, j % 3)
    Hg = T.lines(segs, 0.018) * (0.7 + 0.3 * math.sin(TAU * t * 2))
    sub = np.random.default_rng(67)
    fumaca = T.splats([(sub.normal(0, 0.3), 0.5 - 1.0 * ((sub.uniform() + t * 0.7) % 1), sub.uniform(0.3, 0.8)) for _ in range(14)], 0.07) * 0.5
    G += Hg * 1.2 + fumaca + T.gauss(0, 0, 0.15) * 0.6
    H += Hg * 0.6
    return G, H


def sarcofago_maldito(T, t, rng):
    """O Retorno ao sarcófago no campo dos rivais: o sarcófago gigante sobe do chão (a forma com o
    rosto e os olhos vermelhos), as faixas de hieróglifos rodam em volta, a escuridão fecha e cai."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    sobe = back(rel(t, 0.0, 0.4), 1.2)
    base = 0.7
    alto = 1.4 * sobe
    contorno = [(-0.3, base), (-0.42, base - alto * 0.55), (-0.32, base - alto * 0.85), (-0.18, base - alto), (0.18, base - alto), (0.32, base - alto * 0.85), (0.42, base - alto * 0.55), (0.3, base)]
    S = T.polys([(contorno, 1.0)], 0.006) * 0.5
    borda = T.polyline(contorno + [contorno[0]], 0.025)
    oy = base - alto * 0.78
    olhos = (T.gauss(-0.09, oy, 0.035) + T.gauss(0.09, oy, 0.035)) * rel(t, 0.3, 0.45) * (0.8 + 0.2 * math.sin(TAU * t * 5))
    segs = []
    for j in range(10):
        a = TAU * j / 10 + t * 1.5
        segs += _hieroglifo(0.7 * math.cos(a), 0.0 + 0.25 * math.sin(a), 0.09, j % 3)
    Hg = T.lines(segs, 0.01) * pulso(t, 0.2, 0.9)
    k = pulso(t, 0.6, 0.95)
    escuro = T.gauss(0, 0, 0.6, 0.45) * k * 0.6
    G += (S + borda * 1.1 + olhos * 1.8 + Hg * 1.0 + escuro) * env
    H += (borda * 0.4 + olhos * 1.6 + Hg * 0.4) * env
    return G, H


REGISTRO = [
    ("varredura_optica", varredura_optica, GRANDE, "Ciclope · o feixe passando em cada rival", False),
    ("laser_curto", laser_curto, MEDIA, "Ciclope · o laser curto do Ricochete voando (laço)", True),
    ("ricochete_optico", ricochete_optico, GRANDE, "Ciclope · o quique do raio em cada rival", False),
    ("visor_carregando", visor_carregando, MEDIA, "Ciclope · o visor acendendo (laço)", True),
    ("feixe_ciclope", feixe_ciclope, FAIXA, "Ciclope · o Feixe concentrado (faixa)", True),
    ("feixe_concentrado", feixe_concentrado, GRANDE, "Ciclope · o feixe batendo e cortando o golpe", False),
    ("tesouro_do_ceu", tesouro_do_ceu, GRANDE, "Shaka · o lótus e os cinco sentidos se apagando", False),
    ("khan_escudo", khan_escudo, GRANDE, "Shaka · a esfera dourada do Khan no aliado", False),
    ("lotus_shaka", lotus_shaka, MEDIA, "Shaka · a mandala dourada girando (laço)", True),
    ("seis_mundos", seis_mundos, GRANDE, "Shaka · os seis portais puxando para o centro", False),
    ("espiritos_antigos", espiritos_antigos, GRANDE, "Mumm-Ra · os quatro espíritos entrando no rival", False),
    ("mumm_ra_desperta", mumm_ra_desperta, GRANDE, "Mumm-Ra · as faixas soltando e a aura escura", False),
    ("sarcofago_preparo", sarcofago_preparo, MEDIA, "Mumm-Ra · os hieróglifos acendendo (laço)", True),
    ("sarcofago_maldito", sarcofago_maldito, GRANDE, "Mumm-Ra · o sarcófago gigante no campo", False),
]
