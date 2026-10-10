"""O Renascer de cada um (pedido do jogador: "os personagens que têm renascer, todos usam a mesma
coisa… de Fênix… cada um renasce de uma forma diferente").

Para cada personagem com Renascer, duas folhas:
- espera_<id> (laço): sobre o medalhão caído, enquanto a barrinha enche;
- volta_<id>: o momento em que ele volta.

Ikki ........ nas cinzas a Fênix respira; volta: a Ave Fênix de fogo sobe e abre as asas.
Jean Grey ... o halo telecinético dourado e as estrelas; volta: a Força Fênix cósmica, asas abertas
              na horizontal e a explosão de estrelas.
Deadpool .... os pedaços tremendo e se arrastando, o balão "…"; volta: os pedaços voam e grudam, o
              estouro de quadrinho e as duas katanas cruzadas.
Majin Boo ... a poça de gosma rosa borbulhando e as gotas voltando; volta: as gotas se juntam numa
              bola que estica para cima e o vapor sai pelos furos da cabeça.
Mumm-Ra ..... o sarcófago em pé com as frestas acesas e os espíritos subindo; volta: a tampa se
              abre ao meio, as faixas se desenrolam e a fumaça sobe.
Cell ........ uma célula só, pulsando e se dividindo; volta: as células se multiplicam (1, 2, 4, 8…)
              e formam o corpo, com as pintas e a aura.
Mario ....... o cogumelo de 1 vida pulando, com as pintas; volta: o cogumelo cresce, estoura, sobe o
              "1UP", moedas girando e estrelas.
Wolverine ... o vapor da cura e os pontos se fechando; volta: as três garras saem (snikt) com o
              brilho do metal e o anel de cura.
Alucard ..... a névoa vermelha girando e os morcegos em volta; volta: a névoa se fecha em espiral, os
              morcegos mergulham e a capa se abre.
Muzan ....... a carne pulsando, os tentáculos se contorcendo e o sangue; volta: os tentáculos chicoteiam
              de todos os lados, se juntam e o olho de demônio acende.
Pain ........ os anéis do Rinnegan ondulando e as hastes de chakra fincadas; volta: o Rinnegan abre
              grande, os seis corpos acendem em roda e a onda do Shinra Tensei.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, vazio
from generate_families import _subindo


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _circulo(cx, cy, r, n=28, sq=1.0, ond=0.0, fase=0.0, k=5):
    return [(cx + r * (1 + ond * math.sin(k * a + fase)) * math.cos(a), cy + r * sq * (1 + ond * math.sin(k * a + fase)) * math.sin(a)) for a in np.linspace(0, TAU, n, endpoint=False)]


def _sobe(rng_seed, t, n, x0, x1, y0, alt, vel=1.0):
    """Partículas que sobem em laço: (x, y, peso)."""
    sub = np.random.default_rng(rng_seed)
    pts = []
    for _ in range(n):
        f = (sub.uniform() + t * vel * sub.uniform(0.7, 1.3)) % 1
        x = sub.uniform(x0, x1) + 0.05 * math.sin(TAU * (f + sub.uniform()))
        pts.append((x, y0 - alt * f, math.sin(math.pi * f) * sub.uniform(0.4, 1)))
    return pts


# =================================================================== a Fênix (Ikki e Jean)
def _fenix(T, cx, cy, esc, abre, bate, horizontal=False):
    """A ave de fogo: corpo em gota, a cabeça com bico e crista, as asas de penas compridas e a cauda
    de plumas que cai e se enrola. `abre` (0→1) estende as asas; `horizontal` abre para os lados."""
    formas, fios = [], []
    S = lambda pts: [(cx + x * esc, cy + y * esc) for x, y in pts]
    formas.append((S(_circulo(0, 0.02, 0.07, 16, 1.9)), 1.0))
    formas.append((S([(-0.04, -0.12), (0.0, -0.2), (0.05, -0.17), (0.11, -0.15), (0.05, -0.12), (0.03, -0.08)]), 1.0))
    for k in range(3):
        formas.append((S(lamina(0.0, -0.17, -0.06 - 0.03 * k, -0.3 + 0.02 * k, 0.012)), 0.9))
    for lado in (-1, 1):
        for k in range(8):
            if horizontal:
                a = -math.pi / 2 + lado * (0.85 + k * 0.11) - lado * bate
            else:
                a = -math.pi / 2 + lado * (0.18 + k * 0.17) - lado * bate
            comp = (0.62 - 0.035 * k) * abre
            x1, y1 = lado * 0.04, -0.04
            x2, y2 = x1 + math.cos(a) * comp, y1 + math.sin(a) * comp * 0.9
            formas.append((S(lamina(x1, y1, x2, y2, 0.05 - 0.003 * k)), 1 - 0.06 * k))
            fios.append((S(lamina(x1, y1, x1 + (x2 - x1) * 0.8, y1 + (y2 - y1) * 0.8, 0.012)), 1))
    for k in range(5):
        off = (k - 2) * 0.05
        pts = [(off * 0.3, 0.12)]
        for u in np.linspace(0, 1, 10)[1:]:
            pts.append((off * (0.3 + 1.6 * u) + 0.05 * math.sin(u * 5 + k), 0.12 + 0.42 * u))
        fios.append((S(lamina(pts[0][0], pts[0][1], pts[-1][0], pts[-1][1], 0.018)), 0.8))
        formas.append((S(lamina(pts[0][0], pts[0][1], pts[-1][0], pts[-1][1], 0.03)), 0.7))
    return T.polys(formas, 0.01), T.polys(fios, 0.004)


def espera_ikki(T, t, rng):
    """Ikki caído: o monte de cinzas no chão com o miolo em brasa respirando, a silhueta pequena da
    Fênix aparecendo e sumindo dentro do fogo, e as faíscas de pena subindo."""
    G, H = vazio(T)
    resp = 0.6 + 0.4 * math.sin(t * TAU)
    monte = T.gauss(0, 0.38, 0.32, 0.07) * 0.8 + T.gauss(0, 0.33, 0.14, 0.06) * resp
    ave, fio = _fenix(T, 0, 0.1, 0.45, 0.6 + 0.1 * math.sin(t * TAU), 0.0)
    n = _subindo(T, 31, t, 0.06, 1.0)
    chama = T.gauss(0, 0.15, 0.16, 0.3) * (0.6 + 0.4 * np.clip(n, -1, 1)) * resp * 0.7
    fa = _sobe(5, t, 22, -0.4, 0.4, 0.35, 0.8)
    G += monte + chama + ave * 0.45 * resp + T.splats(fa, 0.013) * 1.1
    H += T.gauss(0, 0.33, 0.1, 0.04) * resp + fio * 0.3 * resp + T.splats(fa, 0.006) * 0.8
    return G, H


def volta_ikki(T, t, rng):
    """A Ave Fênix: as cinzas giram e se juntam, a coluna de fogo estoura para cima e de dentro dela
    a Fênix sobe, abre as asas inteiras e bate uma vez, soltando penas de brasa."""
    G, H = vazio(T)
    junta = rel(t, 0, 0.3)
    cinzas = []
    for k in range(30):
        a = k / 30 * TAU + junta * 5
        r = 0.08 + 0.72 * (1 - ease_in(junta, 1.6))
        cinzas.append((math.cos(a) * r, 0.25 + math.sin(a) * r * 0.4, (0.4 + 0.6 * junta) * (1 - rel(t, 0.28, 0.36))))
    est = pulso(t, 0.26, 0.6)
    n = _subindo(T, 977, t, 0.06, 1.6)
    coluna = T.gauss(0, -0.1, 0.14, 0.6) * (0.75 + 0.25 * np.clip(n, -1, 1)) * est * 1.6
    sobe = ease_out(rel(t, 0.3, 0.6), 2)
    ave, fio = _fenix(T, 0, 0.25 - 0.3 * sobe, 1.25, back(rel(t, 0.34, 0.66), 1.4), 0.14 * math.sin(rel(t, 0.62, 0.95) * math.pi))
    env = apaga(t, 0.8, 1)
    penas = _sobe(9, t, 26, -0.7, 0.7, 0.45, 1.0, 1.2)
    penas = [(x, y, w * rel(t, 0.4, 0.6)) for x, y, w in penas]
    G += T.splats(cinzas, 0.016) * 1.4 + (coluna + T.glow(ave, 1.1, 1.1, 0.03) * (0.75 + 0.25 * np.clip(n, -1, 1)) * (sobe > 0) + T.splats(penas, 0.012)) * env
    H += T.splats(cinzas, 0.008) + (coluna * 0.7 + fio * 1.3 * (sobe > 0)) * env
    return G, H


def espera_jeangrey(T, t, rng):
    """Jean caída: o halo telecinético dourado gira em volta do medalhão (dois anéis inclinados em
    sentidos contrários), estrelas pequenas piscam e línguas de fogo cósmico lambem por baixo."""
    G, H = vazio(T)
    resp = 0.6 + 0.4 * math.sin(t * TAU)
    a1 = T.arc_band(0.5, 0.025, t * TAU, t * TAU + 4.2, squash=0.35, rot=0.3)
    a2 = T.arc_band(0.46, 0.02, -t * TAU, -t * TAU + 3.6, squash=0.35, rot=-0.35)
    sub = np.random.default_rng(12)
    estrelas = [(sub.uniform(-0.7, 0.7), sub.uniform(-0.6, 0.4), (0.5 + 0.5 * math.sin(TAU * (t * 2 + sub.uniform()))) ** 3) for _ in range(16)]
    fogo = T.gauss(0, 0.34, 0.42, 0.07) * resp * 0.6
    for k in range(9):
        x = -0.4 + 0.1 * k
        alt = 0.12 + 0.08 * math.sin(TAU * (t * 2 + k * 0.31))
        fogo += T.gauss(x, 0.34 - alt * 0.6, 0.035, alt) * 0.5
    G += (a1 + a2) * 1.1 + fogo + T.splats(estrelas, 0.01) * 1.2
    H += (a1 + a2) * 0.4 + T.splats(estrelas, 0.005) * 1.5
    return G, H


def volta_jeangrey(T, t, rng):
    """A Força Fênix: o ponto de luz no peito cresce, explode numa nuvem de estrelas, e a ave de fogo
    cósmica abre as asas enormes na horizontal (como o emblema), com o anel dourado se expandindo."""
    G, H = vazio(T)
    nucleo = ease_out(rel(t, 0.0, 0.25), 2) * (1 - rel(t, 0.3, 0.45))
    cl = pulso(t, 0.24, 0.5)
    abre = back(rel(t, 0.3, 0.62), 1.3)
    ave, fio = _fenix(T, 0, -0.05, 1.3, abre, 0.1 * math.sin(rel(t, 0.6, 0.95) * math.pi), horizontal=True)
    anel = T.ring(0.2 + 0.75 * ease_out(rel(t, 0.28, 0.7), 2), 0.03, squash=2.4) * pulso(t, 0.28, 0.85)
    sub = np.random.default_rng(77)
    est = []
    for _ in range(40):
        a = sub.uniform(0, TAU)
        d = (0.1 + 0.8 * sub.uniform()) * ease_out(rel(t, 0.26, 0.7), 2)
        est.append((math.cos(a) * d, math.sin(a) * d * 0.7, sub.uniform(0.3, 1) * pulso(t, 0.26, 1.0)))
    n = _subindo(T, 53, t, 0.06, 1.4)
    env = apaga(t, 0.8, 1)
    G += (T.gauss(0, 0, 0.06 + 0.1 * nucleo, None) * nucleo * 2 + T.gauss(0, 0, 0.4, 0.3) * cl + T.glow(ave, 1.0, 1.1, 0.03) * (0.75 + 0.25 * np.clip(n, -1, 1)) + anel * 1.2 + T.splats(est, 0.011)) * env
    H += (T.gauss(0, 0, 0.05, None) * nucleo * 2 + T.flare(0, 0, 0.9 * cl + 0.01, thin=0.02) * cl + fio * 1.2 + T.splats(est, 0.005) * 1.4) * env
    return G, H


# =================================================================== Deadpool
_PEDACOS = [(-0.42, 0.3, 0.09), (0.38, 0.32, 0.08), (-0.18, 0.4, 0.07), (0.15, 0.42, 0.075), (0.45, 0.05, 0.06), (-0.5, 0.0, 0.065), (0.0, 0.36, 0.1)]


def espera_deadpool(T, t, rng):
    """Deadpool caído: os pedaços espalhados tremem e se arrastam devagar para o meio (o fator de cura
    trabalhando), as gotas pulsam vermelhas e o balão de fala com "…" balança em cima."""
    G, H = vazio(T)
    formas = []
    for k, (x, y, r) in enumerate(_PEDACOS):
        tr = 0.012 * math.sin(TAU * (t * 4 + k * 0.37))
        perto = 0.12 * (0.5 + 0.5 * math.sin(TAU * t + k))
        formas.append((_circulo(x * (1 - perto) + tr, y * (1 - perto * 0.3), r, 14, 0.8, 0.15, t * 9 + k, 3), 1.0))
    P = T.polys(formas, 0.01)
    pulsa = 0.6 + 0.4 * abs(math.sin(t * TAU * 2))
    bal = _circulo(0.0, -0.55, 0.2, 30, 0.6)
    bico = [(-0.05, -0.45), (0.0, -0.36), (0.04, -0.46)]
    B = T.polys([(bal, 1.0), (bico, 1.0)], 0.006) * 0.55
    pontos = [(-0.08 + 0.08 * k, -0.55, 1.0 if (t * 3) % 1 > k / 3 else 0.2) for k in range(3)]
    G += P * pulsa + B + T.splats(pontos, 0.014) * 0.5
    H += P * 0.15 + T.splats(pontos, 0.012) * 1.6 + (B - T.blur(B, 0.01)).clip(0) * 1.2
    return G, H


def volta_deadpool(T, t, rng):
    """Deadpool volta: os pedaços voam para o meio e grudam (cada um com um estalo de brilho), o corpo
    pulsa, estoura o balão de quadrinho em estrela com as linhas de ação e as duas katanas aparecem
    cruzadas atrás, girando e parando com o brilho na lâmina."""
    G, H = vazio(T)
    junta = ease_in(rel(t, 0.0, 0.3), 1.8)
    formas = []
    for k, (x, y, r) in enumerate(_PEDACOS):
        formas.append((_circulo(x * (1 - junta), (y - 0.1) * (1 - junta) + 0.1 * (1 - junta), r * (1 - 0.3 * junta), 14, 0.8), 1 - rel(t, 0.3, 0.38)))
    P = T.polys(formas, 0.01)
    corpo = T.gauss(0, 0, 0.18, 0.24) * pulso(t, 0.28, 0.5) * 1.3
    est = back(rel(t, 0.32, 0.5), 1.6)
    burst = estrela(0, 0, 0.62 * est + 0.01, 0.2, 12, 0.62)
    B = T.polys([(burst, 1.0)], 0.008)
    borda = np.clip(B - T.blur(B, 0.012), 0, 1)
    linhas = T.zero()
    for k in range(16):
        a = k / 16 * TAU + 0.1
        r0 = 0.66 * est
        linhas += T.polys([(lamina(math.cos(a) * r0, math.sin(a) * r0, math.cos(a) * (r0 + 0.25), math.sin(a) * (r0 + 0.25), 0.012), 1.0)], 0.004)
    gira = (1 - ease_out(rel(t, 0.4, 0.62), 2)) * 2.4
    kat = []
    for lado in (-1, 1):
        a = -math.pi / 2 + lado * 0.6 + gira * lado
        kat.append((lamina(-math.cos(a) * 0.55, -math.sin(a) * 0.55, math.cos(a) * 0.75, math.sin(a) * 0.75, 0.03), 1.0))
    K = T.polys(kat, 0.006) * rel(t, 0.4, 0.46)
    env = apaga(t, 0.8, 1)
    G += P * 1.2 + corpo + (B * 0.35 + borda * 1.2 + linhas * 0.9 * pulso(t, 0.34, 0.75) + K * 0.9) * env
    H += T.splats([(x * (1 - junta), y * (1 - junta), janela(t, 0.22, 0.3)) for x, y, _ in _PEDACOS], 0.02) + (borda * 0.8 + K * 0.6 + T.flare(0.2, -0.35, 0.3 * pulso(t, 0.6, 0.8) + 0.01) * pulso(t, 0.6, 0.8)) * env
    return G, H


# =================================================================== Majin Boo
def espera_majinbuu(T, t, rng):
    """Majin Boo caído: a poça de gosma rosa no chão, mole, borbulhando (bolhas que crescem e estouram),
    e as gotinhas espalhadas que rastejam de volta para a poça, com um fio de vapor."""
    G, H = vazio(T)
    poca = T.polys([(_circulo(0, 0.32, 0.36, 40, 0.3, 0.06, t * TAU * 2, 5), 1.0)], 0.02)
    bolhas = []
    sub = np.random.default_rng(3)
    for k in range(6):
        f = (sub.uniform() + t * 1.5) % 1
        x = sub.uniform(-0.25, 0.25)
        bolhas.append(T.ring(0.015 + 0.05 * f, 0.008, x, 0.3 - 0.04 * f) * (1 - f ** 4))
    gotas = []
    for k in range(7):
        a = k / 7 * TAU
        f = (t + k / 7) % 1
        d = 0.75 - 0.4 * f
        gotas.append((_circulo(math.cos(a) * d, 0.32 + math.sin(a) * d * 0.25, 0.045, 12, 0.8, 0.2, t * 15 + k, 3), 1 - f))
    vap = _sobe(21, t, 10, -0.2, 0.2, 0.2, 0.6, 0.6)
    G += poca * 0.9 + sum(bolhas, T.zero()) * 1.1 + T.polys(gotas, 0.01) + T.splats(vap, 0.04) * 0.25
    H += T.gauss(-0.1, 0.27, 0.08, 0.025) * 0.5 + sum(bolhas, T.zero()) * 0.4
    return G, H


def volta_majinbuu(T, t, rng):
    """Majin Boo se refaz: gotas de gosma voam de todos os lados e se juntam numa bola, a bola
    balança, estica para cima no formato do corpo (barriga e cabeça), e o vapor sai com força pelos
    furos da cabeça — dois jatos de fumaça em forma de nuvem."""
    G, H = vazio(T)
    junta = ease_in(rel(t, 0.0, 0.3), 1.7)
    gotas = []
    sub = np.random.default_rng(8)
    for k in range(16):
        a = k / 16 * TAU + sub.uniform(-0.2, 0.2)
        d = 0.85 * (1 - junta) + 0.05
        gotas.append((_circulo(math.cos(a) * d, math.sin(a) * d * 0.8, 0.05 + 0.03 * sub.uniform(), 12, 1.0, 0.2, t * 20 + k, 3), 1 - rel(t, 0.28, 0.34)))
    estica = back(rel(t, 0.3, 0.55), 1.8)
    bal = math.sin(rel(t, 0.3, 0.7) * TAU * 2) * (1 - rel(t, 0.3, 0.7)) * 0.08
    barriga = _circulo(0, 0.12, 0.26 * (0.6 + 0.4 * estica) * (1 + bal), 36, 0.85 - bal)
    cabeca = _circulo(0, 0.12 - 0.38 * estica, 0.15 * estica + 0.01, 30, 0.95, 0.04, 0, 3)
    antena = lamina(0, 0.12 - 0.5 * estica, 0.08, 0.12 - 0.66 * estica, 0.03 * estica + 0.001)
    corpo = T.polys([(barriga, 1.0), (cabeca, 1.0), (antena, 1.0)], 0.012) * rel(t, 0.26, 0.32)
    jato = []
    for lado in (-1, 1):
        for k in range(7):
            f = (k / 7 + t * 2.5) % 1
            u = rel(t, 0.55, 0.62) * (1 - rel(t, 0.85, 0.98))
            jato.append((lado * (0.1 + 0.22 * f), -0.3 - 0.4 * f, (1 - f * 0.7) * u))
    env = apaga(t, 0.85, 1)
    G += T.polys(gotas, 0.01) * 1.1 + (corpo + T.splats(jato, 0.055) * 0.6) * env
    H += (T.gauss(-0.07, 0.03, 0.07, 0.04) * 0.6 * rel(t, 0.32, 0.4) + T.splats(jato, 0.025) * 0.5 + np.clip(corpo - T.blur(corpo, 0.012), 0, 1) * 0.5) * env
    return G, H


# =================================================================== Mumm-Ra
def _sarcofago(abre=0.0):
    """O sarcófago (as duas metades da tampa): contorno de seis lados, mais largo nos ombros."""
    meio = [(0.0, -0.62), (0.0, 0.5)]
    esq = [(0.0, -0.62), (-0.2, -0.56), (-0.26, -0.3), (-0.2, 0.42), (0.0, 0.5)]
    dir_ = [(x * -1, y) for x, y in esq]
    return [(x - abre, y) for x, y in esq], [(x + abre, y) for x, y in dir_], meio


def espera_mummra(T, t, rng):
    """Mumm-Ra caído: o sarcófago em pé atrás do medalhão, com as frestas acesas pulsando (a luz por
    dentro), os hieróglifos piscando na tampa e os espíritos subindo em fumaça torcida."""
    G, H = vazio(T)
    e, d, _ = _sarcofago()
    S = T.polys([(e, 1.0), (d, 1.0)], 0.01) * 0.45
    resp = 0.6 + 0.4 * math.sin(t * TAU)
    fresta = T.polyline([(0.0, -0.6), (0.0, 0.48)], 0.012) * resp + T.polyline([(-0.2, -0.3), (0.2, -0.3)], 0.008) * resp * 0.6
    sub = np.random.default_rng(4)
    hier = [(sub.uniform(-0.15, 0.15), sub.uniform(-0.4, 0.35), (0.5 + 0.5 * math.sin(TAU * (t * 2 + sub.uniform()))) ** 4) for _ in range(12)]
    esp = []
    for k in range(3):
        f = (t + k / 3) % 1
        pts = [(0.25 * math.sin(f * 6 + u * 4 + k) * u + (k - 1) * 0.25, 0.3 - f * 0.9 - u * 0.25) for u in np.linspace(0, 1, 8)]
        esp.append(T.polyline(pts, 0.03) * math.sin(math.pi * f))
    G += S + fresta + sum(esp, T.zero()) * 0.5 + T.splats(hier, 0.012) * 0.8
    H += fresta * 0.9 + T.splats(hier, 0.006) * 1.2
    return G, H


def volta_mummra(T, t, rng):
    """Mumm-Ra volta: a fresta do sarcófago racha em luz, a tampa se abre ao meio (as duas metades
    deslizando para os lados), o clarão sai de dentro, as faixas de múmia se desenrolam ondulando para
    fora e a fumaça dos espíritos sobe torcida."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0.22, 0.5), 2)
    e, d, _ = _sarcofago(0.32 * abre)
    some_ = 1 - rel(t, 0.6, 0.8)
    S = T.polys([(e, 1.0), (d, 1.0)], 0.01) * 0.55 * some_
    racha = T.polyline([(0.0, -0.6), (0.0, 0.48)], 0.01 + 0.03 * rel(t, 0.05, 0.22)) * (1 - rel(t, 0.3, 0.4)) * rel(t, 0.02, 0.1)
    luz = T.gauss(0, -0.05, 0.04 + 0.16 * abre, 0.42) * pulso(t, 0.22, 0.7) * 1.3
    faixas = T.zero()
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.5
        u = ease_out(rel(t, 0.3 + 0.02 * k, 0.65), 1.6)
        pts = [(math.cos(a) * 0.85 * s * u + 0.03 * math.sin(s * 5 + t * 8) * -math.sin(a), -0.05 + math.sin(a) * 0.75 * s * u + 0.03 * math.sin(s * 5 + t * 8) * math.cos(a)) for s in np.linspace(0, 1, 14)]
        faixas += T.polyline(pts, 0.045) * u
        faixas -= T.polyline(pts, 0.006) * u * 0.5        # a dobra no meio da faixa
    fum = _sobe(19, t, 18, -0.45, 0.45, 0.3, 1.0, 0.8)
    env = apaga(t, 0.8, 1)
    G += S + racha * 1.3 + (luz + faixas * 0.9 + T.splats([(x, y, w * rel(t, 0.35, 0.5)) for x, y, w in fum], 0.04) * 0.45) * env
    H += racha * 1.3 + (luz * 0.6 + np.clip(faixas - T.blur(faixas, 0.01), 0, 1) * 0.6 + T.flare(0, -0.1, 0.8 * pulso(t, 0.25, 0.5) + 0.01, ang=0, thin=0.015) * pulso(t, 0.25, 0.5)) * env
    return G, H


# =================================================================== Cell
def _celula(T, cx, cy, r, fase, divide=0.0):
    """Uma célula: a membrana ondulada, o citoplasma claro e o núcleo. `divide` (0→1) estica em duas."""
    if divide <= 0:
        mem = _circulo(cx, cy, r, 28, 1.0, 0.05, fase, 6)
        return [(mem, 1.0)], [(cx + r * 0.2, cy - r * 0.1, 1.0)]
    off = r * 0.75 * divide
    a = _circulo(cx - off, cy, r * (1 - 0.15 * divide), 24, 1.0, 0.05, fase, 6)
    b = _circulo(cx + off, cy, r * (1 - 0.15 * divide), 24, 1.0, 0.05, fase + 1, 6)
    return [(a, 1.0), (b, 1.0)], [(cx - off, cy, 1.0), (cx + off, cy, 1.0)]


def espera_cell(T, t, rng):
    """Cell caído: sobrou uma célula só, verde, pulsando no meio; a cada laço ela estica e quase se
    divide em duas, e as bolinhas de energia orbitam em volta."""
    G, H = vazio(T)
    div = max(0.0, math.sin(t * TAU)) ** 2
    formas, nuc = _celula(T, 0, 0.12, 0.17 * (1 + 0.06 * math.sin(t * TAU * 2)), t * TAU * 2, div)
    C = T.polys(formas, 0.012)
    borda = np.clip(C - T.blur(C, 0.015), 0, 1)
    orb = [(math.cos(t * TAU + k * TAU / 6) * 0.42, 0.12 + math.sin(t * TAU + k * TAU / 6) * 0.18, 0.7) for k in range(6)]
    G += C * 0.45 + borda * 1.2 + T.splats(nuc, 0.045) * 0.9 + T.splats(orb, 0.014) * 0.8
    H += borda * 0.5 + T.splats(nuc, 0.025) * 0.8 + T.splats(orb, 0.007)
    return G, H


def volta_cell(T, t, rng):
    """Cell se refaz de uma célula: ela se divide em 2, 4, 8, 16 — as células se espalham e enchem a
    silhueta do corpo — então tudo se funde num clarão com as pintas do Cell aparecendo e a aura verde
    subindo em chamas."""
    G, H = vazio(T)
    passos = min(4, int(rel(t, 0.0, 0.4) * 5))
    sub = np.random.default_rng(16)
    centros = [(0.0, 0.1)]
    for _ in range(passos):
        novos = []
        for x, y in centros:
            a = sub.uniform(0, TAU)
            d = 0.09
            novos += [(x + math.cos(a) * d, y + math.sin(a) * d * 1.3), (x - math.cos(a) * d, y - math.sin(a) * d * 1.3)]
        centros = [(max(-0.45, min(0.45, x)), max(-0.55, min(0.45, y))) for x, y in novos]
    r = 0.17 / (1.35 ** passos)
    formas, nuc = [], []
    vis = 1 - rel(t, 0.42, 0.5)
    for k, (x, y) in enumerate(centros):
        f, n = _celula(T, x, y, r, t * 12 + k, 0.0)
        formas += [(p, w * vis) for p, w in f]
        nuc += [(a, b, w * vis) for a, b, w in n]
    C = T.polys(formas, 0.01)
    funde = pulso(t, 0.4, 0.62)
    corpo = T.gauss(0, -0.05, 0.22, 0.45) * funde * 1.3
    pintas = [(sub.uniform(-0.2, 0.2), sub.uniform(-0.4, 0.3), rel(t, 0.48, 0.56) * (1 - rel(t, 0.8, 0.95))) for _ in range(14)]
    aura = (T.gauss(0, -0.1, 0.3, 0.55) * 0.5 + sum((T.ring(0.25 + 0.5 * ((t * 2 + k / 3) % 1), 0.02, 0, -0.05, squash=0.7) * (1 - (t * 2 + k / 3) % 1) for k in range(3)), T.zero())) * pulso(t, 0.45, 1.0)
    env = apaga(t, 0.85, 1)
    G += C * 0.5 + np.clip(C - T.blur(C, 0.012), 0, 1) * 1.1 + T.splats(nuc, 0.02) * 0.8 + (corpo + aura + T.splats(pintas, 0.025) * 0.6) * env
    H += T.splats(nuc, 0.01) * 0.7 + (corpo * 0.6 + T.splats(pintas, 0.016) * 1.2 + T.flare(0, -0.05, 0.9 * funde + 0.01, thin=0.015) * funde) * env
    return G, H


# =================================================================== Mario
def _cogumelo(T, cx, cy, esc):
    """O cogumelo de uma vida: o chapéu em cúpula com as três pintas (claras), o pé com os dois olhos."""
    S = lambda pts: [(cx + x * esc, cy + y * esc) for x, y in pts]
    chapeu = [(math.cos(a) * 0.3, -0.02 + math.sin(a) * 0.26) for a in np.linspace(math.pi, TAU, 24)] + [(0.3, 0.02), (-0.3, 0.02)]
    pe = [(-0.17, 0.02), (0.17, 0.02), (0.19, 0.12), (0.14, 0.24), (-0.14, 0.24), (-0.19, 0.12)]
    C = T.polys([(S(chapeu), 1.0), (S(pe), 0.85)], 0.008)
    pintas = [(cx + x * esc, cy + y * esc, 1.0) for x, y in ((0.0, -0.16), (-0.19, -0.06), (0.19, -0.06))]
    olhos = [(cx + x * esc, cy + y * esc, 1.0) for x, y in ((-0.05, 0.1), (0.05, 0.1))]
    return C, T.splats(pintas, 0.055 * esc), T.splats(olhos, 0.018 * esc)


def espera_mario(T, t, rng):
    """Mario caído: o cogumelo de uma vida pula no ar em cima do medalhão (sobe e quica no chão,
    amassando na queda), com as pintas claras e brilhinhos em volta."""
    G, H = vazio(T)
    f = (t * 2) % 1
    alt = 4 * f * (1 - f)
    C, P, O = _cogumelo(T, 0, 0.08 - 0.35 * alt, 0.9)
    sombra = T.gauss(0, 0.42, 0.18 * (1 - 0.4 * alt), 0.03) * 0.5
    sub = np.random.default_rng(2)
    brilho = sum((T.flare(sub.uniform(-0.5, 0.5), sub.uniform(-0.55, 0.2), 0.06 * (0.5 + 0.5 * math.sin(TAU * (t * 2 + k / 4)))) for k in range(4)), T.zero())
    G += C + sombra + brilho * 0.6
    H += P * 1.6 + O * 1.4 + brilho
    return G, H


def _texto_1up(cx, cy, s):
    """O "1UP" em traços (o 1, o U e o P), para desenhar com polyline."""
    um = [(-0.42, -0.08), (-0.34, -0.16), (-0.34, 0.16)]
    u = [(-0.18, -0.16), (-0.18, 0.08)] + [(math.cos(a) * 0.09 - 0.09, 0.08 + math.sin(a) * 0.08) for a in np.linspace(math.pi, 0, 8)][1:] + [(0.0, -0.16)]
    p = [(0.14, 0.16), (0.14, -0.16), (0.26, -0.16)] + [(0.26 + math.cos(a) * 0.08, -0.08 + math.sin(a) * 0.08) for a in np.linspace(-math.pi / 2, math.pi / 2, 8)] + [(0.14, 0.0)]
    return [[(cx + x * s, cy + y * s) for x, y in tr] for tr in (um, u, p)]


def volta_mario(T, t, rng):
    """Mario volta com 1 vida: o cogumelo sobe e cresce, pisca, estoura em estrelas, o "1UP" sobe
    grande e some, e as moedas giram para cima (as faces estreitando e alargando)."""
    G, H = vazio(T)
    cresce = back(rel(t, 0.0, 0.25), 1.8)
    pisca = 1.0 if rel(t, 0.25, 0.4) == 0 or int(t * 40) % 2 == 0 else 0.4
    vis = 1 - rel(t, 0.38, 0.44)
    C, P, O = _cogumelo(T, 0, 0.15 - 0.15 * cresce, 0.5 + 0.7 * cresce)
    est = []
    sub = np.random.default_rng(5)
    for k in range(10):
        a = k / 10 * TAU
        d = 0.15 + 0.6 * ease_out(rel(t, 0.38, 0.75), 2)
        est.append((estrela(math.cos(a) * d, math.sin(a) * d * 0.8, 0.06, a, 5, 0.45), pulso(t, 0.38, 0.9)))
    sobe = ease_out(rel(t, 0.4, 0.7), 2)
    txt = sum((T.polyline(tr, 0.035) for tr in _texto_1up(0, 0.05 - 0.32 * sobe, 1.15)), T.zero()) * rel(t, 0.4, 0.46) * (1 - rel(t, 0.85, 1))
    moedas = []
    for k in range(5):
        f = rel(t, 0.42 + 0.04 * k, 0.9)
        x = (k - 2) * 0.28
        y = 0.35 - 0.9 * ease_out(f, 1.5)
        larg = abs(math.cos(t * 30 + k)) * 0.06 + 0.012
        moedas.append((_circulo(x, y, 0.08, 18, 1.0), math.sin(math.pi * f)))
        moedas[-1] = ([(x + (px - x) * larg / 0.08, py) for px, py in moedas[-1][0]], moedas[-1][1])
    M = T.polys(moedas, 0.006)
    G += (C * vis * pisca + T.polys(est, 0.006) * 1.1 + txt * 1.2 + M * 0.9)
    H += (P * 1.5 + O * 1.4) * vis * pisca + txt * 0.9 + T.polys(est, 0.006) * 0.5 + np.clip(M - T.blur(M, 0.01), 0, 1) * 0.8
    return G, H


# =================================================================== Wolverine
def espera_wolverine(T, t, rng):
    """Wolverine caído: o vapor da cura subindo do corpo, as costuras de luz (os cortes se fechando
    em zigue-zague, um de cada vez) e o brilho do metal correndo pelo osso de adamantium."""
    G, H = vazio(T)
    vap = _sobe(31, t, 16, -0.35, 0.35, 0.3, 0.9, 0.7)
    cortes = T.zero()
    for k, (x0, y0, a) in enumerate(((-0.25, -0.1, 0.6), (0.2, 0.05, -0.5), (-0.05, 0.25, 0.1))):
        f = (t + k / 3) % 1
        fecha = 1 - f
        pts = []
        for j in range(9):
            u = j / 8
            pts.append((x0 + math.cos(a) * 0.3 * u + (0.025 * fecha if j % 2 else -0.025 * fecha) * -math.sin(a), y0 + math.sin(a) * 0.3 * u + (0.025 * fecha if j % 2 else -0.025 * fecha) * math.cos(a)))
        cortes += T.polyline(pts, 0.01) * math.sin(math.pi * f)
    osso = T.polyline([(0, -0.45), (0, 0.35)], 0.025) * 0.2 + T.gauss(0, -0.45 + 0.8 * t, 0.05, 0.08) * 0.7
    G += T.splats(vap, 0.07) * 0.18 + cortes * 1.3 + osso
    H += cortes * 0.8 + T.gauss(0, -0.45 + 0.8 * t, 0.025, 0.05) * 0.8
    return G, H


def volta_wolverine(T, t, rng):
    """Wolverine levanta: o anel de cura fecha no corpo, o punho se fecha e as três garras de
    adamantium saem de uma vez (SNIKT) — longas, com o brilho do metal correndo da base à ponta — e
    as faíscas saltam."""
    G, H = vazio(T)
    anel = T.ring(0.75 * (1 - ease_in(rel(t, 0.0, 0.28), 1.5)) + 0.08, 0.03) * (1 - rel(t, 0.26, 0.32))
    sai = back(rel(t, 0.3, 0.42), 2.0)
    garras, fios = [], []
    for k in range(3):
        x = (k - 1) * 0.13
        comp = 0.8 * sai
        garras.append((lamina(x, 0.25, x + 0.05 * (k - 1), 0.25 - comp, 0.035), 1.0))
        fios.append((lamina(x, 0.25, x + 0.05 * (k - 1), 0.25 - comp, 0.008), 1.0))
    Gr = T.polys(garras, 0.006)
    Fi = T.polys(fios, 0.003)
    punho = T.polys([(_circulo(0, 0.32, 0.16, 20, 0.7), 1.0)], 0.01) * rel(t, 0.25, 0.32)
    corre = T.gauss(0.0, 0.25 - 0.8 * rel(t, 0.42, 0.62), 0.25, 0.05) * pulso(t, 0.42, 0.65)
    fa = []
    sub = np.random.default_rng(9)
    for _ in range(20):
        a = sub.uniform(-math.pi, 0)
        d = 0.1 + 0.5 * ease_out(rel(t, 0.36, 0.6), 2)
        fa.append((math.cos(a) * d, 0.1 + math.sin(a) * d, pulso(t, 0.36, 0.7) * sub.uniform(0.4, 1)))
    env = apaga(t, 0.82, 1)
    G += anel * 1.2 + (Gr * 1.1 + punho * 0.6 + T.splats(fa, 0.01)) * env
    H += anel * 0.5 + (Fi * 1.2 + corre * Gr * 2 + T.flare(0, 0.25 - 0.8 * sai, 0.3 * pulso(t, 0.38, 0.55) + 0.01) * pulso(t, 0.38, 0.55)) * env
    return G, H


# =================================================================== Alucard
def _morcego(cx, cy, s, bate):
    """Morcego de frente (este sim é morcego): asas de membrana recortada em arcos, as orelhas."""
    w = 0.06 * math.sin(bate)
    meia = [(0.0, -0.02), (0.05, -0.05 - w), (0.12, -0.07 - w * 1.5), (0.2, -0.03 - w * 2), (0.16, 0.0 - w), (0.12, 0.02 - w * 0.5), (0.08, 0.0), (0.04, 0.03), (0.0, 0.04)]
    pts = meia + [(-x, y) for x, y in meia[::-1]]
    orelhas = [(-0.02, -0.02), (-0.03, -0.06), (-0.005, -0.03), (0.005, -0.03), (0.03, -0.06), (0.02, -0.02)]
    return [([(cx + x * s, cy + y * s) for x, y in pts], 1.0), ([(cx + x * s, cy + y * s) for x, y in orelhas], 1.0)]


def espera_alucardcv(T, t, rng):
    """Alucard caído: o corpo virou névoa vermelha que gira devagar em volta do medalhão, e uns
    morcegos pequenos voam em roda, batendo as asas."""
    G, H = vazio(T)
    n = _subindo(T, 71, t, 0.05, 0.4)
    gir = T.zero()
    for k in range(3):
        a0 = t * TAU + k * TAU / 3
        gir += T.arc_band(0.35 + 0.08 * k, 0.07, a0, a0 + 2.4, squash=0.55, cy=0.1)
    nevoa = T.blur(gir, 0.04) * (0.6 + 0.4 * np.clip(n, -1, 1)) * 0.8
    mor = []
    for k in range(4):
        a = -t * TAU + k * TAU / 4
        mor += _morcego(math.cos(a) * 0.55, -0.05 + math.sin(a) * 0.22, 1.3, t * TAU * 6 + k)
    M = T.polys(mor, 0.004)
    G += nevoa + M * 1.1
    H += np.clip(M - T.blur(M, 0.01), 0, 1) * 0.5 + T.gauss(0, 0.1, 0.1, 0.06) * 0.2
    return G, H


def volta_alucardcv(T, t, rng):
    """Alucard se refaz: a névoa vermelha se fecha em espiral no medalhão, os morcegos mergulham de
    todos os lados para dentro dela, e a capa se abre larga (as pontas recortadas) com o clarão."""
    G, H = vazio(T)
    fecha = ease_in(rel(t, 0.0, 0.35), 1.5)
    esp = T.zero()
    for k in range(4):
        a0 = t * 9 + k * TAU / 4
        esp += T.arc_band(0.75 * (1 - fecha) + 0.08, 0.06, a0, a0 + 2.0, squash=0.7)
    nev = T.blur(esp, 0.035) * (1 - rel(t, 0.33, 0.42))
    mor = []
    for k in range(10):
        a = k / 10 * TAU
        d = 0.95 * (1 - ease_in(rel(t, 0.05 + 0.02 * k, 0.38), 1.4)) + 0.05
        mor += [(p, w * (1 - rel(t, 0.36, 0.4))) for p, w in _morcego(math.cos(a) * d, math.sin(a) * d * 0.8, 1.2, t * 50 + k)]
    abre = back(rel(t, 0.38, 0.6), 1.5)
    w = 0.72 * abre
    capa = [(-0.2, -0.55), (-0.14, -0.36), (-0.22, -0.3)]
    capa += [(-0.22 - (w - 0.22) * u, -0.3 + 0.72 * u ** 0.8) for u in np.linspace(0.1, 1, 6)]
    for k in range(9):
        x = -w + 2 * w * k / 8
        capa.append((x, 0.42 + (0.0 if k % 2 == 0 else -0.08)))
    capa += [(0.22 + (w - 0.22) * u, -0.3 + 0.72 * u ** 0.8) for u in np.linspace(1, 0.1, 6)]
    capa += [(0.22, -0.3), (0.14, -0.36), (0.2, -0.55), (0.0, -0.4)]
    Cp = T.polys([(capa, 1.0)], 0.01) * rel(t, 0.38, 0.42)
    cl = pulso(t, 0.36, 0.58)
    env = apaga(t, 0.8, 1)
    G += nev * 1.1 + T.polys(mor, 0.004) * 1.1 + (Cp * 0.75 + T.gauss(0, -0.05, 0.3, 0.3) * cl) * env
    H += (np.clip(Cp - T.blur(Cp, 0.012), 0, 1) * 0.7 + T.flare(0, -0.1, 0.7 * cl + 0.01, thin=0.015) * cl) * env
    return G, H


# =================================================================== Muzan
def _tentaculo(x0, y0, x1, y1, curva, fase, larg):
    pts = []
    for u in np.linspace(0, 1, 16):
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u
        nx, ny = -(y1 - y0), (x1 - x0)
        n = math.hypot(nx, ny) or 1
        o = curva * math.sin(math.pi * u) + 0.04 * math.sin(u * 9 + fase)
        pts.append((x + nx / n * o, y + ny / n * o))
    esq = [(x - larg * (1 - u) * 0.0, y) for (x, y), u in zip(pts, np.linspace(0, 1, 16))]
    return pts, larg


def espera_muzan(T, t, rng):
    """Muzan caído: a massa de carne pulsando no chão (como um coração), os tentáculos se contorcendo
    devagar para cima e as gotas de sangue caindo."""
    G, H = vazio(T)
    bate = (0.5 + 0.5 * math.sin(t * TAU * 2)) ** 3
    massa = T.polys([(_circulo(0, 0.3, 0.2 * (1 + 0.1 * bate), 30, 0.55, 0.12, t * 8, 4), 1.0)], 0.015)
    ten = T.zero()
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * 0.5
        comp = 0.45 + 0.1 * math.sin(t * TAU + k)
        pts, _ = _tentaculo(0, 0.28, math.cos(a) * comp, 0.28 + math.sin(a) * comp, 0.08 * math.sin(t * TAU + k * 1.7), t * TAU + k, 0.03)
        ten += T.polyline(pts, 0.03 - 0.0 * k)
    gotas = []
    for k in range(6):
        f = (t * 1.5 + k / 6) % 1
        gotas.append(((k - 2.5) * 0.15, -0.2 + 0.6 * f, math.sin(math.pi * f)))
    G += massa * (0.8 + 0.4 * bate) + ten * 0.9 + T.splats(gotas, 0.014)
    H += T.gauss(0, 0.28, 0.08, 0.04) * bate * 0.8 + np.clip(ten - T.blur(ten, 0.01), 0, 1) * 0.3
    return G, H


def volta_muzan(T, t, rng):
    """Muzan se remonta: os tentáculos de carne chicoteiam de todos os lados para o centro, se
    enroscam numa massa que pulsa, a massa se fecha e o olho de demônio (a pupila vertical) acende
    no meio, com os espinhos saindo em volta."""
    G, H = vazio(T)
    vem = ease_in(rel(t, 0.0, 0.3), 1.6)
    ten = T.zero()
    for k in range(8):
        a = k / 8 * TAU + 0.2
        d = 0.95 * (1 - vem) + 0.1
        pts, _ = _tentaculo(math.cos(a) * d, math.sin(a) * d, math.cos(a) * (d + 0.4), math.sin(a) * (d + 0.4), 0.1 * math.sin(t * 20 + k), t * 25 + k, 0.035)
        ten += T.polyline(pts, 0.035)
    ten *= 1 - rel(t, 0.3, 0.38)
    massa = T.polys([(_circulo(0, 0, 0.25 * pulso(t, 0.25, 0.6) + 0.01, 30, 1.0, 0.1, t * 20, 5), 1.0)], 0.012)
    olho = rel(t, 0.42, 0.52)
    amend = [(math.cos(a) * 0.3, math.sin(a) * 0.12 * olho) for a in np.linspace(0, TAU, 30, endpoint=False)]
    pupila = [(math.cos(a) * 0.035, math.sin(a) * 0.11 * olho) for a in np.linspace(0, TAU, 16, endpoint=False)]
    O = T.polys([(amend, 1.0)], 0.008)
    Pu = T.polys([(pupila, 1.0)], 0.004)
    esp = []
    for k in range(14):
        a = k / 14 * TAU
        sai = back(rel(t, 0.48, 0.62), 1.6)
        esp.append((lamina(math.cos(a) * 0.32, math.sin(a) * 0.32, math.cos(a) * (0.32 + 0.35 * sai), math.sin(a) * (0.32 + 0.35 * sai), 0.03), 1.0))
    E = T.polys(esp, 0.005) * rel(t, 0.48, 0.52)
    env = apaga(t, 0.8, 1)
    G += ten * 1.1 + massa * (1 - rel(t, 0.5, 0.6)) + (O * 0.9 + E * 0.9 + T.gauss(0, 0, 0.35, 0.3) * pulso(t, 0.45, 0.7) * 0.6) * env
    H += (np.clip(O - T.blur(O, 0.01), 0, 1) * 0.8 + Pu * -0.0 + np.clip(E - T.blur(E, 0.008), 0, 1) * 0.5) * env
    G -= Pu * 0.6 * env
    return G, H


# =================================================================== Pain
def _rinnegan(T, cx, cy, r, aberto=1.0):
    """O Rinnegan: o olho com os anéis concêntricos (as ondas), a pupila no meio."""
    A = T.zero()
    for k in range(1, 5):
        A += T.ring(r * k / 4.5, 0.012, cx, cy, squash=aberto)
    return A + T.gauss(cx, cy, r * 0.08, r * 0.08 * max(aberto, 0.1)) * 1.5


def espera_pain(T, t, rng):
    """Pain caído: os anéis do Rinnegan ondulam no chão em volta do medalhão (a onda saindo do centro
    em laço) e as hastes de chakra negras fincadas em roda, com a ponta piscando."""
    G, H = vazio(T)
    ondas = T.zero()
    for k in range(4):
        f = (t + k / 4) % 1
        ondas += T.ring(0.08 + 0.55 * f, 0.02, 0, 0.3, squash=3.2) * (1 - f)
    hastes, pontas = [], []
    for k in range(6):
        a = k / 6 * TAU + 0.3
        x, y = math.cos(a) * 0.55, 0.3 + math.sin(a) * 0.18
        hastes.append((lamina(x, y, x + 0.05 * math.cos(a), y - 0.35, 0.02), 1.0))
        pontas.append((x + 0.05 * math.cos(a), y - 0.35, (0.5 + 0.5 * math.sin(TAU * (t * 2 + k / 6))) ** 2))
    olho = _rinnegan(T, 0, 0.0, 0.3, 1.0) * (0.35 + 0.15 * math.sin(t * TAU))
    G += ondas * 1.1 + T.polys(hastes, 0.006) * 0.8 + olho
    H += T.splats(pontas, 0.012) * 1.5 + ondas * 0.3
    return G, H


def volta_pain(T, t, rng):
    """Outro corpo assume (os Seis Caminhos): o Rinnegan abre enorme no centro (os anéis crescendo e
    girando), seis silhuetas acendem em roda uma depois da outra, e a onda do Shinra Tensei empurra
    tudo para fora com o chão."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0.0, 0.3), 2)
    olho = _rinnegan(T, 0, -0.05, 0.6 * abre + 0.01, 0.35 + 0.65 * abre) * (1 - rel(t, 0.55, 0.75))
    corpos = []
    for k in range(6):
        a = -math.pi / 2 + k / 6 * TAU
        x, y = math.cos(a) * 0.62, -0.05 + math.sin(a) * 0.5
        acende = rel(t, 0.25 + 0.04 * k, 0.3 + 0.04 * k)
        sil = [(x - 0.04, y + 0.12), (x - 0.05, y - 0.02), (x - 0.03, y - 0.06), (x, y - 0.12), (x + 0.03, y - 0.06), (x + 0.05, y - 0.02), (x + 0.04, y + 0.12)]
        corpos.append((sil, acende * (1 - rel(t, 0.7, 0.85))))
        corpos.append((_circulo(x, y - 0.17, 0.04, 12), acende * (1 - rel(t, 0.7, 0.85))))
    Cs = T.polys(corpos, 0.006)
    onda = rel(t, 0.5, 0.85)
    sh = T.ring(0.1 + 0.95 * onda, 0.05 * (1 - onda) + 0.008) * (1 - onda) * (onda > 0)
    env = apaga(t, 0.85, 1)
    G += olho * 1.1 + Cs * 0.9 + (sh * 1.4 + T.gauss(0, 0, 0.3, 0.3) * pulso(t, 0.48, 0.65)) * env
    H += olho * 0.4 + np.clip(Cs - T.blur(Cs, 0.008), 0, 1) * 0.8 + sh * 0.6 * env + T.flare(0, -0.05, 0.6 * pulso(t, 0.48, 0.62) + 0.01, thin=0.015) * pulso(t, 0.48, 0.62)
    return G, H


REGISTRO = [
    ("espera_ikki", espera_ikki, GRANDE, "Ikki caído: as cinzas em brasa e a Fênix respirando (laço)", True),
    ("volta_ikki", volta_ikki, GRANDE, "Ikki volta: a Ave Fênix sobe das cinzas e abre as asas", False),
    ("espera_jeangrey", espera_jeangrey, GRANDE, "Jean caída: o halo telecinético dourado e as estrelas (laço)", True),
    ("volta_jeangrey", volta_jeangrey, GRANDE, "Jean volta: a Força Fênix cósmica de asas abertas", False),
    ("espera_deadpool", espera_deadpool, GRANDE, "Deadpool caído: os pedaços tremendo e o balão \"…\" (laço)", True),
    ("volta_deadpool", volta_deadpool, GRANDE, "Deadpool volta: os pedaços grudam, o estouro de quadrinho e as katanas", False),
    ("espera_majinbuu", espera_majinbuu, GRANDE, "Majin Boo caído: a poça de gosma rosa borbulhando (laço)", True),
    ("volta_majinbuu", volta_majinbuu, GRANDE, "Majin Boo se refaz: as gotas se juntam e o vapor sai da cabeça", False),
    ("espera_mummra", espera_mummra, GRANDE, "Mumm-Ra caído: o sarcófago aceso e os espíritos (laço)", True),
    ("volta_mummra", volta_mummra, GRANDE, "Mumm-Ra volta: a tampa do sarcófago abre e as faixas se soltam", False),
    ("espera_cell", espera_cell, GRANDE, "Cell caído: uma célula só, pulsando e se dividindo (laço)", True),
    ("volta_cell", volta_cell, GRANDE, "Cell se refaz: as células se multiplicam e formam o corpo", False),
    ("espera_mario", espera_mario, GRANDE, "Mario caído: o cogumelo de uma vida pulando (laço)", True),
    ("volta_mario", volta_mario, GRANDE, "Mario volta: o cogumelo, o 1UP, as moedas e as estrelas", False),
    ("espera_wolverine", espera_wolverine, GRANDE, "Wolverine caído: o vapor e os cortes se fechando (laço)", True),
    ("volta_wolverine", volta_wolverine, GRANDE, "Wolverine levanta: as três garras saem (snikt)", False),
    ("espera_alucardcv", espera_alucardcv, GRANDE, "Alucard caído: a névoa vermelha e os morcegos em roda (laço)", True),
    ("volta_alucardcv", volta_alucardcv, GRANDE, "Alucard se refaz: a névoa fecha, os morcegos mergulham, a capa abre", False),
    ("espera_muzan", espera_muzan, GRANDE, "Muzan caído: a carne pulsando e os tentáculos (laço)", True),
    ("volta_muzan", volta_muzan, GRANDE, "Muzan se remonta: os tentáculos se juntam e o olho acende", False),
    ("espera_pain", espera_pain, GRANDE, "Pain caído: os anéis do Rinnegan e as hastes de chakra (laço)", True),
    ("volta_pain", volta_pain, GRANDE, "Pain volta: o Rinnegan abre, os seis corpos e o Shinra Tensei", False),
]
