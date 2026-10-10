"""Golpes de assinatura: as habilidades famosas que ainda usavam um efeito genérico.

Pedido do jogador: "verifica todos os personagens… habilidades muito únicas…
cria [efeitos] para elas… tanto o efeito visual quanto o sonoro tem que ser
certinho com a habilidade". Cada folha aqui conta a cena da habilidade: o
caderno que escreve o nome e o coração que para (Death Note), o soco que sobe
girando (Shoryuken), o soco com o segundo impacto atrasado (Punho divergente),
o frasco que quebra em chamas sagradas (Água benta), a aura vermelha do
Kaioken, o brilho prateado do Instinto Superior, o Gear Fifth com nuvens e o
tambor, os corvos do Itachi, os golpes no escuro e o 天 do Shun Goku Satsu, a
bola azul do Spin Dash, os braços esticados do Gatling, o manto da Kurama com as
nove caudas, o Estado Avatar e o raio na espada do He-Man.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, jagged, janela, lamina, pulso, rel, some, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _move(pts, dx, dy, esc=1.0):
    return [(dx + x * esc, dy + y * esc) for x, y in pts]


def _clarao(T, k, cx=0.0, cy=0.0, r=0.3, tam=0.7):
    return T.gauss(cx, cy, r, r) * k * 1.5, (T.flare(cx, cy, tam * k + 0.01, ang=0.3, thin=0.016) + T.flare(cx, cy, tam * 0.65 * k + 0.01, ang=0.3 + math.pi / 2, thin=0.012)) * k * 1.6


def _chama(cx, base, alt, larg, fase, ondula=0.25):
    """Língua de fogo: gota que afina para cima, com a ponta balançando."""
    pts = []
    for k in range(13):
        u = k / 12
        a = math.pi * u
        y = base - alt * u
        w = larg * math.sin(a) ** 0.6 * (1 - u) ** 0.9
        balanco = ondula * larg * math.sin(fase + 6 * u) * u
        pts.append((cx + w + balanco, y))
    for k in range(12, -1, -1):
        u = k / 12
        a = math.pi * u
        y = base - alt * u
        w = larg * math.sin(a) ** 0.6 * (1 - u) ** 0.9
        balanco = ondula * larg * math.sin(fase + 6 * u) * u
        pts.append((cx - w + balanco, y))
    return pts


def _aura(T, t, seed, raio=0.55, alto=0.85, n=14, vel=9.0, base=0.55):
    """Aura de chamas em volta do corpo: línguas que sobem e tremem em volta do centro."""
    sub = np.random.default_rng(seed)
    formas = []
    for k in range(n):
        x = (k / (n - 1) * 2 - 1) * raio
        alt = alto * (0.55 + 0.45 * math.cos(x / raio * math.pi / 2)) * (0.85 + 0.25 * math.sin(t * vel + k * 1.7))
        formas.append((_chama(x, base, alt, 0.12 + 0.05 * sub.uniform(), t * vel * 1.3 + k), 0.55 + 0.25 * sub.uniform()))
    return T.polys(formas, 0.02)


# ------------------------------------------------------------------ Death Note
def death_note(T, t, rng):
    """Death Note: a página do caderno aparece, o nome é escrito linha por linha, o batimento
    do coração corre na tela, dá dois picos e vira uma linha reta; a luz se fecha no centro."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    pg = janela(t, 0.0, 0.1) * (1 - rel(t, 0.42, 0.55))
    ang = -0.08
    folha = _gira([(-0.42, -0.55), (0.42, -0.55), (0.42, 0.55), (-0.42, 0.55)], ang)
    borda = T.polyline(folha + [folha[0]], 0.012) * pg
    pautas = sum(T.polyline(_gira([(-0.34, -0.38 + 0.12 * k), (0.34, -0.38 + 0.12 * k)], ang), 0.004) for k in range(8)) * pg * 0.35
    escrita = T.zero()
    sub = np.random.default_rng(9)
    for linha in range(3):
        prog = rel(t, 0.06 + 0.1 * linha, 0.16 + 0.1 * linha)
        if prog <= 0:
            continue
        y = -0.32 + 0.24 * linha
        pts = []
        n = int(28 * prog) + 2
        for k in range(n):
            x = -0.3 + 0.6 * k / 27
            pts.append((x, y + 0.045 * math.sin(k * 2.3 + linha) + sub.uniform(-0.012, 0.012)))
        escrita += T.polyline(_gira(pts, ang), 0.016) * pg
    # batimento: corre da esquerda para a direita, dois picos e depois reto
    corre = rel(t, 0.42, 0.78)
    pts = []
    for k in range(int(80 * corre) + 2):
        x = -0.9 + 1.8 * k / 79
        y = 0.0
        for c in (-0.45, 0.05):
            d = (x - c) / 0.05
            if abs(d) < 1.6:
                y += -0.42 * math.exp(-d * d * 2) + 0.18 * math.exp(-(d - 0.9) ** 2 * 3)
        pts.append((x, y))
    linha_ecg = T.polyline(pts, 0.018) * janela(t, 0.42, 0.44) * (1 - rel(t, 0.88, 1.0))
    ponta = T.gauss(pts[-1][0], pts[-1][1], 0.04, 0.04) * janela(t, 0.42, 0.45) * (1 - rel(t, 0.78, 0.86)) * 2
    fecha = T.ring(0.75 * (1 - ease_in(rel(t, 0.72, 0.95), 1.6)) + 0.02, 0.05) * pulso(t, 0.72, 0.97) * 1.1
    G += (borda * 0.8 + pautas + escrita * 1.6 + T.blur(linha_ecg, 0.03) * 1.4 + linha_ecg * 0.8 + ponta + fecha) * env
    H += (borda * 0.6 + escrita * 0.6 + linha_ecg * 1.2 + ponta * 1.2 + fecha * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Shoryuken
def shoryuken(T, t, rng):
    """Shoryuken: o punho sobe de baixo, girando dentro de uma espiral de energia, acerta o alvo
    no meio da subida (estrela de impacto) e segue até o alto, deixando a coluna."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    sobe = ease_out(rel(t, 0.05, 0.55), 1.6)
    py = 0.85 - 1.65 * sobe
    coluna = T.polys([(lamina(0.0, 0.9, 0.0, py, 0.16), 1.0)], 0.03) * janela(t, 0.05, 0.12) * (1 - rel(t, 0.55, 0.9))
    helice = []
    for k in range(60):
        u = k / 59
        y = 0.9 - (0.9 - py) * u
        a = u * 5 * TAU - t * 30
        helice.append((0.14 * math.sin(a) * (0.4 + 0.6 * u), y))
    espiral = T.polyline(helice, 0.02) * janela(t, 0.05, 0.12) * (1 - rel(t, 0.5, 0.8))
    punho = [(-0.1, 0.06), (-0.12, -0.08), (-0.06, -0.16), (0.06, -0.16), (0.12, -0.08), (0.1, 0.06), (0.06, 0.22), (-0.06, 0.22)]
    P = T.polys([(_move(_gira(punho, math.sin(t * 25) * 0.2), 0.0, py), 1.0)], 0.006) * (1 - rel(t, 0.55, 0.7))
    chamas = sum(T.polys([(_chama(0.08 * math.sin(k * 2.0), py + 0.45, 0.45, 0.1, t * 30 + k), 0.6)], 0.02) for k in range(3)) * (1 - rel(t, 0.5, 0.75))
    k = pulso(t, 0.24, 0.5)
    g, h = _clarao(T, k, 0.0, 0.0, 0.28)
    estrela_ = T.polys([(estrela(0.0, 0.0, 0.32 * k + 0.01, 0.2, 8, 0.35), 1.0)], 0.006) * k
    sub = np.random.default_rng(31)
    fa = []
    for _ in range(14):
        a = sub.uniform(-math.pi, 0)
        d = 0.2 + 0.6 * ease_out(rel(t, 0.3, 0.8), 2) * sub.uniform(0.5, 1)
        fa.append((d * math.cos(a), d * math.sin(a) + 0.4 * rel(t, 0.3, 0.9) ** 2, pulso(t, 0.3, 0.9) * 0.6))
    G += (coluna * 0.9 + espiral * 1.3 + P * 1.2 + chamas + estrela_ * 1.2 + g + T.splats(fa, 0.012) * 1.5) * env
    H += (coluna * 0.5 + espiral * 0.6 + P * 0.5 + estrela_ * 0.8 + h + T.splats(fa, 0.008)) * env
    return G, H


# ------------------------------------------------------------ Punho divergente
def punho_divergente(T, t, rng):
    """Punho divergente: o soco acerta (estalo pequeno) e, um instante depois, a energia
    amaldiçoada atrasada estoura no mesmo ponto, maior, com faíscas tortas."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    k1 = pulso(t, 0.04, 0.26)
    soco = T.polys([(estrela(0.0, 0.0, 0.22 * k1 + 0.01, 0.4, 6, 0.4), 1.0)], 0.006) * k1
    anel1 = T.ring(0.08 + 0.25 * ease_out(rel(t, 0.04, 0.3), 2), 0.025) * k1
    # o eco atrasado: a energia que chega depois do punho
    espera = janela(t, 0.3, 0.42) * (1 - rel(t, 0.42, 0.46))
    nucleo = T.gauss(0, 0, 0.05 + 0.05 * espera, 0.05 + 0.05 * espera) * espera * 1.5
    k2 = pulso(t, 0.44, 0.85)
    anel2 = T.ring(0.12 + 0.62 * ease_out(rel(t, 0.44, 0.8), 2.4), 0.06) * k2 * 1.3
    sub = np.random.default_rng(77)
    arcos = []
    for k in range(9):
        a = k / 9 * TAU + sub.uniform(-0.2, 0.2)
        r = 0.2 + 0.5 * ease_out(rel(t, 0.44, 0.7), 2)
        pts = jagged(sub, 0.0, 0.0, r * math.cos(a), r * math.sin(a), 4, 0.35)
        arcos.append(T.polyline(pts, 0.014))
    A = sum(arcos) * pulso(t, 0.44, 0.78)
    g, h = _clarao(T, k2, r=0.32, tam=0.9)
    G += (soco + anel1 + nucleo + anel2 + A * 1.3 + g) * env
    H += (soco * 0.8 + anel1 * 0.4 + nucleo * 1.4 + A * 0.9 + anel2 * 0.5 + h) * env
    return G, H


# ------------------------------------------------------------------ Água benta
def agua_benta(T, t, rng):
    """Água benta: o frasco vem em arco, quebra no chão (cacos e respingo) e uma fileira de
    chamas sagradas sobe pelo chão, com uma cruz de luz no meio."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    voa = rel(t, 0.0, 0.28)
    fx, fy = -0.75 + 0.75 * voa, -0.6 + 1.0 * voa - 1.0 * voa * (1 - voa) * 1.2 + 0.2 * voa
    frasco = [(-0.04, -0.09), (0.04, -0.09), (0.04, -0.03), (0.08, 0.02), (0.08, 0.1), (-0.08, 0.1), (-0.08, 0.02), (-0.04, -0.03)]
    F = T.polys([(_move(_gira(frasco, voa * 6), fx, fy), 1.0)], 0.004) * (1 - rel(t, 0.27, 0.3))
    chao = 0.4
    quebra = pulso(t, 0.28, 0.55)
    sub = np.random.default_rng(13)
    cacos = []
    for _ in range(10):
        a = sub.uniform(-math.pi, 0)
        d = 0.08 + 0.4 * ease_out(rel(t, 0.28, 0.6), 2) * sub.uniform(0.5, 1)
        cacos.append((estrela(d * math.cos(a), chao + d * math.sin(a) + 0.3 * rel(t, 0.28, 0.7) ** 2, 0.03, a, 3, 0.4), quebra))
    respingo = T.ring(0.05 + 0.35 * ease_out(rel(t, 0.28, 0.5), 2), 0.03, cy=chao, squash=2.4) * quebra
    chamas = []
    for k in range(9):
        x = -0.7 + 1.4 * k / 8
        a0 = 0.32 + 0.03 * abs(k - 4)
        alt = 0.6 * ease_out(rel(t, a0, a0 + 0.2), 2) * (1 - 0.35 * abs(k - 4) / 4) * (0.75 + 0.3 * abs(math.sin(t * 23 + k * 2.1)))
        if alt > 0.01:
            chamas.append((_chama(x, chao + 0.05, alt, 0.09 + 0.03 * (k % 3) / 2, t * 35 + k * 1.3, 0.6), 0.8))
    C = T.polys(chamas, 0.015) * (1 - rel(t, 0.75, 0.95))
    cruz = (T.polys([([(-0.025, -0.35), (0.025, -0.35), (0.025, 0.15), (-0.025, 0.15)], 1.0), ([(-0.14, -0.22), (0.14, -0.22), (0.14, -0.17), (-0.14, -0.17)], 1.0)], 0.008)
            * pulso(t, 0.45, 0.9))
    G += (F * 1.2 + T.polys(cacos, 0.004) * 1.2 + respingo + C * 1.2 + T.blur(cruz, 0.04) * 1.4 + cruz * 0.5) * env
    H += (F * 0.6 + T.polys(cacos, 0.004) * 0.8 + C * 0.45 + cruz * 1.4) * env
    return G, H


# ------------------------------------------------------------------ Kaioken
def kaioken(T, t, rng):
    """Kaioken: um estouro vermelho e a aura de fogo carmesim que envolve o corpo e treme,
    com faíscas subindo e o chão rachando de leve."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    estouro = pulso(t, 0.0, 0.3)
    anel = T.ring(0.15 + 0.7 * ease_out(rel(t, 0.0, 0.3), 2), 0.06) * estouro * 1.3
    acende = janela(t, 0.05, 0.2)
    aura = _aura(T, t, 401, 0.5, 0.95, 13, 14.0, 0.55) * acende
    nucleo = T.gauss(0, 0.05, 0.32, 0.45) * acende * 0.55
    sub = np.random.default_rng(5)
    brasas = []
    for _ in range(26):
        x = sub.uniform(-0.55, 0.55)
        a0 = sub.uniform(0, 0.7)
        u = ((t - a0) * 1.8) % 1.0 if t > a0 else 0.0
        brasas.append((x + 0.04 * math.sin(u * 9), 0.55 - 1.2 * u, (1 - u) * 0.5 * acende))
    G += (anel + aura * 1.1 + nucleo + T.splats(brasas, 0.01) * 1.6) * env
    H += (anel * 0.6 + T.blur(aura, 0.01) * 0.35 + T.splats(brasas, 0.006)) * env
    return G, H


# ------------------------------------------------------------------ Instinto Superior
def instinto(T, t, rng):
    """Instinto Superior: calma prateada. Fios de aura finos sobem devagar, dois vultos
    escapam para os lados (o corpo desvia sozinho) e um brilho fino corta o centro."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    acende = janela(t, 0.0, 0.25)
    fios = []
    for k in range(9):
        x0 = (k / 8 * 2 - 1) * 0.45
        pts = [(x0 + 0.05 * math.sin(t * 6 + k + u * 5), 0.55 - 1.1 * u) for u in np.linspace(0, 1, 18)]
        fios.append(T.polyline(pts, 0.008) * (0.4 + 0.3 * math.sin(t * 8 + k)))
    F = sum(fios) * acende
    vultos = 0
    for lado, a0 in ((-1, 0.2), (1, 0.42)):
        d = ease_out(rel(t, a0, a0 + 0.2), 2)
        k = pulso(t, a0, a0 + 0.28)
        vultos = vultos + T.gauss(lado * 0.38 * d, -0.1, 0.12, 0.3) * k * 0.7 + T.gauss(lado * 0.38 * d, -0.45, 0.07, 0.07) * k * 0.7
    contorno = T.ring(0.48, 0.012, cy=0.0, squash=0.62) * acende * (0.5 + 0.3 * math.sin(t * 10))
    corte = T.flare(0, -0.05, 0.9 * pulso(t, 0.62, 0.86) + 0.01, ang=-0.5, thin=0.01) * pulso(t, 0.62, 0.86) * 1.8
    sub = np.random.default_rng(3)
    pts = [(sub.uniform(-0.6, 0.6), sub.uniform(-0.7, 0.6), 0.35 * max(0.0, math.sin(t * 12 + i))) for i in range(18)]
    G += (F * 1.4 + vultos * 1.4 + contorno * 0.0 + corte + T.splats(pts, 0.008) * acende) * env
    H += (F * 1.0 + vultos * 0.5 + corte * 1.2 + T.splats(pts, 0.005) * acende) * env
    return G, H


# ------------------------------------------------------------------ Gear Fifth
def gear_fifth(T, t, rng):
    """Gear Fifth: nuvens brancas fofas rodeiam o corpo como um sol, anéis de borracha
    pulam esticando e encolhendo no compasso do tambor (três batidas), e raios largos giram."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    acende = janela(t, 0.0, 0.2)
    nuvens = 0
    for k in range(14):
        a = k / 14 * TAU + t * 1.2
        r = 0.58 + 0.04 * math.sin(t * 9 + k)
        nuvens = nuvens + T.gauss(r * math.cos(a), r * math.sin(a), 0.09, 0.09) * 0.8
    raios = []
    for k in range(10):
        a = k / 10 * TAU - t * 2
        raios.append(([(0.25 * math.cos(a - 0.08), 0.25 * math.sin(a - 0.08)), (0.25 * math.cos(a + 0.08), 0.25 * math.sin(a + 0.08)),
                       (0.95 * math.cos(a + 0.03), 0.95 * math.sin(a + 0.03)), (0.95 * math.cos(a - 0.03), 0.95 * math.sin(a - 0.03))], 0.3))
    R = T.polys(raios, 0.03)
    aneis = 0
    for k, a0 in enumerate((0.12, 0.36, 0.6)):
        u = rel(t, a0, a0 + 0.3)
        estica = 1 + 0.35 * math.sin(u * math.pi * 3) * (1 - u)
        aneis = aneis + T.ring(0.15 + 0.45 * ease_out(u, 2), 0.035, squash=estica) * pulso(t, a0, a0 + 0.3) * 1.2
    batida = sum(T.gauss(0, 0, 0.3, 0.3) * pulso(t, a0, a0 + 0.1) for a0 in (0.12, 0.36, 0.6)) * 0.6
    G += (nuvens * acende + R * acende + aneis + batida) * env
    H += (nuvens * acende * 0.9 + aneis * 0.5 + batida * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Corvos
def corvos(T, t, rng):
    """Ilusão de corvos: o Sharingan acende no meio e o corpo se desfaz numa revoada de corvos de perfil
    (bico, cauda em leque, as penas da ponta da asa abertas) que saem para todos os lados batendo as
    asas, com os olhos acesos; penas pretas caem devagar."""
    from .rodada04 import corvo_de_lado
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    olho = pulso(t, 0.0, 0.3)
    O = (T.ring(0.1, 0.02) + T.gauss(0, 0, 0.03, 0.03) * 1.5) * olho * 1.4
    virgulas = [(estrela(0.07 * math.cos(a + t * 8), 0.07 * math.sin(a + t * 8), 0.025, a, 3, 0.5), olho) for a in (0, TAU / 3, 2 * TAU / 3)]
    sub = np.random.default_rng(66)
    aves, olhos = [], []
    for k in range(9):
        a = TAU * k / 9 + sub.uniform(-0.2, 0.2)
        a0 = 0.08 + sub.uniform(0, 0.18)
        u = ease_out(rel(t, a0, a0 + 0.65), 1.4)
        if u <= 0:
            continue
        d = 0.08 + 0.78 * u
        vis = 1 - rel(t, 0.72, 0.95)
        corpo, penas, o = corvo_de_lado(d * math.cos(a), d * math.sin(a) - 0.12 * u, 0.85 + 0.45 * u + 0.2 * sub.uniform(), t * 30 + k * 1.3, a)
        aves += [(f, w * vis) for f, w in corpo + penas]
        olhos.append((*o, vis))
    penas = []
    for k in range(10):
        x = sub.uniform(-0.6, 0.6)
        y = -0.3 + 0.9 * rel(t, 0.3, 1.0) + 0.1 * sub.uniform()
        penas.append((_gira([(-0.012, -0.04), (0.012, -0.04), (0.006, 0.04), (-0.006, 0.04)], math.sin(t * 6 + k) * 0.8, x + 0.05 * math.sin(t * 5 + k), y), pulso(t, 0.3, 1.0) * 0.7))
    nevoa = T.gauss(0, 0, 0.35, 0.35) * pulso(t, 0.1, 0.5) * 0.4
    A = T.polys(aves, 0.003)
    G += (O + T.polys(virgulas, 0.003) + A * 1.4 + T.polys(penas, 0.003) + nevoa) * env
    A = np.clip(A, 0, 1)
    borda = np.clip(A - T.blur(A, 0.01), 0, 1)
    H += (O * 1.2 + T.splats(olhos, 0.007) * 1.6 + borda * 0.7) * env
    return G, H


# ------------------------------------------------------------------ Shun Goku Satsu
def _tian(prog):
    """O ideograma 天 (céu), em quatro traços de pincel, revelado traço a traço."""
    tracos = [((-0.36, -0.42), (0.36, -0.44), 0.05), ((-0.58, -0.08), (0.58, -0.1), 0.06),
              ((0.02, -0.42), (-0.52, 0.62), 0.065), ((0.02, -0.06), (0.58, 0.6), 0.065)]
    out = []
    for k, ((x1, y1), (x2, y2), w) in enumerate(tracos):
        p = min(1.0, max(0.0, prog * 4 - k))
        if p > 0:
            out.append((lamina(x1, y1, x2, y2, w, prog=p), 1.0))
    return out


def shun_goku_satsu(T, t, rng):
    """Shun Goku Satsu: a tela some no escuro e só os clarões dos golpes aparecem, um atrás do
    outro em lugares diferentes; no fim o ideograma 天 se acende atrás do alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    sub = np.random.default_rng(15)
    golpes = 0
    for k in range(15):
        a0 = 0.04 + 0.033 * k
        x, y = sub.uniform(-0.45, 0.45), sub.uniform(-0.5, 0.45)
        kk = pulso(t, a0, a0 + 0.06)
        if kk > 0:
            golpes = golpes + T.flare(x, y, 0.45 * kk + 0.01, ang=sub.uniform(0, 3), thin=0.012) * kk * 1.8 + T.gauss(x, y, 0.08, 0.08) * kk
    cai = janela(t, 0.6, 0.66)
    letra = T.polys(_tian(rel(t, 0.6, 0.85)), 0.006) * cai
    fundo = T.gauss(0, 0, 0.6, 0.6) * pulso(t, 0.58, 1.0) * 0.35
    G += (golpes + T.blur(letra, 0.03) * 1.6 + letra * 0.8 + fundo) * env
    H += (golpes * 1.1 + letra * 1.1) * env
    return G, H


# ------------------------------------------------------------------ Spin Dash
def spin_dash(T, t, rng):
    """Spin Dash: uma bola azul girando chega rolando com rastro e anéis de velocidade, bate no
    alvo, e anéis dourados saltam para os lados."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    vem = ease_in(rel(t, 0.0, 0.38), 1.5)
    bx = -0.95 + 0.95 * vem
    giro = t * 60
    bola = T.ring(0.21, 0.035, cx=bx) + T.gauss(bx, 0, 0.15, 0.15) * 0.6
    espiral = sum(T.polyline([(bx + r * math.cos(giro + k * TAU / 3 + r * 9), r * math.sin(giro + k * TAU / 3 + r * 9)) for r in np.linspace(0.02, 0.2, 10)], 0.012) for k in range(3))
    ate = 1 - rel(t, 0.4, 0.48)
    rastro = sum(T.gauss(bx - 0.14 * j, 0, 0.12, 0.1) * (0.5 - 0.08 * j) for j in range(1, 6)) * ate
    velocidade = sum(T.ring(0.2, 0.012, cx=bx - 0.25 - 0.22 * j, squash=0.35) * (0.6 - 0.15 * j) for j in range(3)) * ate * janela(t, 0.05, 0.15)
    k = pulso(t, 0.36, 0.7)
    g, h = _clarao(T, k, r=0.26)
    sub = np.random.default_rng(626)
    aneis = 0
    for j in range(7):
        a = sub.uniform(-math.pi * 0.95, -math.pi * 0.05)
        u = rel(t, 0.38, 0.95)
        d = 0.75 * ease_out(u, 1.5) * sub.uniform(0.6, 1)
        aneis = aneis + T.ring(0.07, 0.016, cx=d * math.cos(a), cy=d * math.sin(a) + 0.7 * u * u, squash=0.5 + 0.5 * abs(math.cos(t * 30 + j))) * pulso(t, 0.38, 1.0)
    G += ((bola + espiral) * ate * 1.2 + rastro + velocidade + g + aneis * 1.3) * env
    H += ((bola * 0.5 + espiral * 0.8) * ate + h + aneis * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Gatling
def gatling(T, t, rng):
    """Gatling (Gomu Gomu): dezenas de braços de borracha esticados saem do mesmo lado e
    martelam o alvo, com vultos de punho e estrelinhas de impacto."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    sub = np.random.default_rng(56)
    bracos, punhos, est = [], [], []
    for k in range(26):
        a0 = 0.02 + 0.024 * k
        if t < a0 or t > a0 + 0.16:
            continue
        f = ease_out(rel(t, a0, a0 + 0.05), 2) * (1 - 0.6 * rel(t, a0 + 0.1, a0 + 0.16))
        ox, oy = -1.05, sub.uniform(-0.25, 0.25)
        tx, ty = sub.uniform(-0.25, 0.2), sub.uniform(-0.35, 0.35)
        px, py = ox + (tx - ox) * f, oy + (ty - oy) * f
        vis = 1 - rel(t, a0 + 0.11, a0 + 0.16)
        bracos.append(T.polyline([(ox, oy), ((ox + px) / 2, (oy + py) / 2 + 0.03 * math.sin(k)), (px, py)], 0.06) * vis)
        punhos.append((_move([(-0.06, -0.07), (0.07, -0.08), (0.11, 0.0), (0.07, 0.08), (-0.06, 0.07)], px, py, 1.7), vis))
        if f > 0.95:
            est.append((estrela(tx + 0.18, ty, 0.12, k, 5, 0.4), vis))
    B = sum(bracos) if bracos else T.zero()
    final = T.ring(0.1 + 0.55 * ease_out(rel(t, 0.66, 0.92), 2), 0.05) * pulso(t, 0.66, 0.95) * 1.2
    G += (B * 0.9 + T.polys(punhos, 0.005) * 1.3 + T.polys(est, 0.004) * 1.4 + final) * env
    H += (B * 0.25 + T.polys(punhos, 0.005) * 0.6 + T.polys(est, 0.004) + final * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Manto da Kurama
def manto_kurama(T, t, rng):
    """Manto da Kurama: o chakra laranja acende em chamas em volta do corpo, duas orelhas de
    raposa se erguem no alto e nove caudas ondulam atrás, abrindo em leque."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    acende = janela(t, 0.0, 0.22)
    aura = _aura(T, t, 909, 0.45, 0.9, 12, 11.0, 0.55) * acende
    orelhas = [(_gira(_chama(0.0, 0.0, 0.32 * acende, 0.09, t * 10 + lado, 0.1), lado * 0.35, lado * 0.2, -0.3), 1.0) for lado in (-1, 1)]
    abre = ease_out(rel(t, 0.1, 0.5), 2)
    caudas = []
    for k in range(9):
        base_ang = -math.pi / 2 + (k - 4) * 0.36 * abre
        meio, normais = [], []
        us = np.linspace(0, 1, 24)
        for u in us:
            r = 0.15 + 0.8 * u * abre
            a = base_ang + 0.35 * math.sin(t * 7 + k + u * 4) * u
            meio.append((r * math.cos(a) * 1.05, 0.35 + r * math.sin(a) * 0.95))
        esq, dir_ = [], []
        for i, u in enumerate(us):
            x0, y0 = meio[max(0, i - 1)]
            x1, y1 = meio[min(len(meio) - 1, i + 1)]
            dx, dy = x1 - x0, y1 - y0
            n = math.hypot(dx, dy) or 1
            w = (0.035 + 0.075 * math.sin(math.pi * min(1.0, 0.25 + u * 0.9))) * (1 - u) ** 0.4 * (0.6 + 0.4 * abre)
            esq.append((meio[i][0] - dy / n * w, meio[i][1] + dx / n * w))
            dir_.append((meio[i][0] + dy / n * w, meio[i][1] - dx / n * w))
        caudas.append((esq + dir_[::-1], 0.8))
    C = T.polys(caudas, 0.012) * janela(t, 0.08, 0.2) * 0.75
    estouro = T.ring(0.2 + 0.6 * ease_out(rel(t, 0.0, 0.3), 2), 0.05) * pulso(t, 0.0, 0.32)
    G += (aura * 1.1 + T.polys(orelhas, 0.02) * 1.2 + C * 0.9 + estouro) * env
    H += (T.blur(aura, 0.01) * 0.3 + C * 0.3 + estouro * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Estado Avatar
def estado_avatar(T, t, rng):
    """Estado Avatar: os olhos e as setas acendem em branco, uma esfera de vento gira em volta
    do corpo e quatro orbes (os quatro elementos) orbitam."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    acende = janela(t, 0.0, 0.2)
    olhos = (T.gauss(-0.08, -0.34, 0.03, 0.015) + T.gauss(0.08, -0.34, 0.03, 0.015)) * acende * 3
    seta = T.polys([([(0.0, -0.62), (0.05, -0.54), (0.015, -0.54), (0.015, -0.42), (-0.015, -0.42), (-0.015, -0.54), (-0.05, -0.54)], 1.0)], 0.004) * acende
    vento = 0
    for k in range(5):
        a0 = t * 7 + k * TAU / 5
        vento = vento + T.arc_band(0.5 + 0.03 * k, 0.02, a0, a0 + 1.6, squash=0.75, rot=0.2 * k) * 0.9
    esfera = T.ring(0.56, 0.02, squash=1.0) * 0.5
    orbes = 0
    for k in range(4):
        a = t * 4 + k * TAU / 4
        orbes = orbes + T.gauss(0.68 * math.cos(a), 0.68 * math.sin(a) * 0.6, 0.05, 0.05) * 1.6
    estouro = T.ring(0.15 + 0.7 * ease_out(rel(t, 0.0, 0.3), 2), 0.05) * pulso(t, 0.0, 0.32)
    G += (olhos + seta + (vento + esfera + orbes) * acende + estouro) * env
    H += (olhos * 1.5 + seta * 1.2 + vento * 0.4 * acende + orbes * acende * 0.9 + estouro * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Eu tenho a força
def tenho_a_forca(T, t, rng):
    """Pelo poder de Grayskull: a espada se ergue acima da cabeça, os raios descem do alto
    e caem na ponta, a lâmina se enche de luz e o poder desce num clarão."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    sobe = back(rel(t, 0.0, 0.25), 1.4)
    topo = -0.1 - 0.4 * sobe
    espada = [(-0.05, topo + 0.7), (0.05, topo + 0.7), (0.04, topo), (0.0, topo - 0.1), (-0.04, topo)]
    guarda = [(-0.18, topo + 0.7), (0.18, topo + 0.7), (0.18, topo + 0.76), (-0.18, topo + 0.76)]
    E = T.polys([(espada, 1.0), (guarda, 1.0)], 0.004)
    sub = np.random.default_rng(1983)
    raios = T.zero()
    for k in range(4):
        a0 = 0.22 + 0.07 * k
        kk = pulso(t, a0, a0 + 0.14)
        if kk > 0:
            x0 = sub.uniform(-0.7, 0.7)
            raios += T.polyline(jagged(sub, x0, -1.0, 0.0, topo - 0.1, 5, 0.25), 0.02) * kk
    carga = janela(t, 0.25, 0.55)
    lamina_cheia = T.blur(E, 0.02) * carga * 1.4
    k = pulso(t, 0.55, 0.85)
    g, h = _clarao(T, k, 0.0, topo, 0.3, 0.9)
    desce = T.ring(0.15 + 0.7 * ease_out(rel(t, 0.58, 0.9), 2), 0.05) * pulso(t, 0.58, 0.95)
    G += (E * 1.1 + T.blur(raios, 0.01) * 1.5 + raios * 0.8 + lamina_cheia + g + desce) * env
    H += (E * 0.6 + raios * 1.4 + lamina_cheia * 0.6 + h + desce * 0.5) * env
    return G, H


REGISTRO = [
    ("death_note", death_note, GRANDE, "Death Note: o nome escrito e o coração que para", False),
    ("shoryuken", shoryuken, GRANDE, "Shoryuken: o soco que sobe em espiral", False),
    ("punho_divergente", punho_divergente, GRANDE, "Punho divergente: o soco e o impacto atrasado", False),
    ("agua_benta", agua_benta, GRANDE, "Água benta: o frasco quebra em chamas sagradas", False),
    ("kaioken", kaioken, GRANDE, "Kaioken: aura de fogo carmesim", False),
    ("instinto", instinto, GRANDE, "Instinto Superior: aura prateada e vultos", False),
    ("corvos", corvos, GRANDE, "Ilusão de corvos: revoada que sai do corpo", False),
    ("shun_goku_satsu", shun_goku_satsu, GRANDE, "Shun Goku Satsu: golpes no escuro e o 天", False),
    ("spin_dash", spin_dash, GRANDE, "Spin Dash: bola azul girando e anéis", False),
    ("estado_avatar", estado_avatar, GRANDE, "Estado Avatar: olhos acesos, vento e quatro orbes", False),
    ("tenho_a_forca", tenho_a_forca, GRANDE, "Eu tenho a força: raios na espada erguida", False),
]
