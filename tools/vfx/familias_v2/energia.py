"""Energia: ki, esferas em espiral, gravidade, cosmos, supernova, transformação, domínio."""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, TAU, _subindo, apaga, back, ease_in, ease_out, estrela, faiscas, jagged, janela, pulso,
                   rel, smooth, some, vazio)


def explosao_ki(T, t, rng):
    """Explosão de ki: domo de luz que incha, anel no chão, pedras subindo e um clarão que cega."""
    G, H = vazio(T)
    cresce = ease_out(rel(t, 0, 0.4), 2.2)
    n = T.noise(np.random.default_rng(301), 0.05, 3)
    domo = smooth(-np.hypot(T.U, (T.V - 0.1) * 1.1) + 0.2 + 0.55 * cresce + 0.04 * n, -0.04, 0.06)
    casca = np.exp(-((np.hypot(T.U, (T.V - 0.1) * 1.1) - 0.2 - 0.55 * cresce) / 0.03) ** 2)
    env = apaga(t, 0.4, 0.9)
    anel = T.ring(0.3 + 0.7 * ease_out(rel(t, 0.05, 1), 2), 0.035, cy=0.45, squash=3) * (1 - t) ** 1.2 * 1.5
    fa = faiscas(T, rng, t, 26, 1.0, 0.035, cone=(-math.pi + 0.3, -0.3), gravidade=0.5, cy=0.3)
    # clarão redondo e contido (um sigma largo batia na borda do quadro e virava um quadrado)
    flash = T.gauss(0, 0.1, 0.22) * some(t, 0, 0.18) * 3.0 * smooth(0.95 - T.RAD, 0, 0.3)
    G += (domo * 1.0 + casca * 1.5) * env + anel + T.glow(fa, 1, 1.2, 0.02) + flash
    H += (domo * 0.9 + casca) * env * (1 - rel(t, 0.2, 0.8)) + flash + fa * 0.6
    return G, H


def esfera_espiral(T, t, rng):
    """Esfera espiral (Rasengan): bola de vento girando com linhas em espiral, anel moendo o alvo."""
    G, H = vazio(T)
    s = 0.3 * (0.6 + 0.4 * ease_out(rel(t, 0, 0.2), 2)) * (1 + 0.15 * janela(t, 0.3, 0.5))
    env = apaga(t, 0.65, 1)
    rr = T.RAD / s
    dentro = smooth(1.05 - rr, 0, 0.1)
    espiral = (0.5 + 0.5 * np.cos(T.ANG * 3 - rr * 7 + t * 30)) ** 3 * dentro
    nucleo = T.gauss(0, 0, s * 0.45) * 2
    borda = T.ring(s, 0.02) * 1.4
    moenda = T.ring(s * 1.4 + 0.1 * rel(t, 0.3, 1), 0.04, squash=2.5) * pulso(t, 0.25, 0.9) * 1.3
    fa = faiscas(T, rng, t, 18, 0.8, 0.03, inicio=0.3)
    G += (espiral * 1.2 + nucleo + borda + dentro * 0.3) * env + moenda + T.glow(fa, 1, 1, 0.02)
    H += (nucleo + espiral * 0.5) * env + fa * 0.6
    return G, H


def buraco_negro(T, t, rng):
    """Buraco negro: disco de acreção girando, centro apagado e tudo sendo sugado em espiral."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0, 0.3), 2)
    env = apaga(t, 0.7, 1)
    sq = 2.6
    r = np.hypot(T.U, T.V * sq)
    ang = np.arctan2(T.V * sq, T.U)
    disco = np.exp(-((r - 0.45 * abre) / (0.16 * abre + 0.01)) ** 2) * (0.6 + 0.4 * np.cos(ang * 2 + r * 8 - t * 12))
    horizonte = T.ring(0.17 * abre, 0.025) * 1.6
    escuro = 1 - smooth(0.16 * abre - T.RAD, -0.02, 0.02)
    sugados = []
    for _ in range(36):
        f = (rng.uniform(0, 1) + t * 1.3) % 1
        a0 = rng.uniform(0, TAU)
        d = 0.9 * (1 - f) + 0.17
        a = a0 + f * 4
        sugados.append((math.cos(a) * d, math.sin(a) * d / 1.8, f * rng.uniform(0.4, 1)))
    G += ((disco * 1.3) * escuro + horizonte + T.splats(sugados, 0.012) * 1.2) * env
    H += (disco * 0.5 * escuro + horizonte * 0.6) * env
    return G, H


def gravidade(T, t, rng):
    """Gravidade: anéis caindo e achatando no chão, linhas de pressão descendo do alto."""
    G, H = vazio(T)
    env = apaga(t, 0.7, 1)
    aneis = T.zero()
    for k in range(4):
        u = ((t * 1.6 + k / 4) % 1)
        aneis += T.ring(0.7 - 0.35 * u, 0.018, cy=-0.5 + 0.85 * u, squash=3.5) * math.sin(math.pi * u)
    linhas = []
    for k in range(9):
        x = -0.6 + k * 0.15
        y0 = -0.95 + ((t * 2 + k * 0.37) % 1) * 0.6
        linhas.append((x, y0, x, y0 + 0.35, 1))
    l = T.tapered(linhas, 0.02)
    chao = T.ring(0.55, 0.05, cy=0.4, squash=3.5) * janela(t, 0.1, 0.3) * 1.2
    G += (aneis * 1.3 + l * 0.8 + chao) * env
    H += (aneis * 0.4 + chao * 0.4) * env
    return G, H


def cosmico(T, t, rng):
    """Cosmos: uma galáxia de dois braços gira no alvo, estrelas piscando em volta."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0, 0.35), 2)
    env = apaga(t, 0.65, 1)
    r = T.RAD / max(abre, 0.05)
    bracos = (0.5 + 0.5 * np.cos(2 * T.ANG - r * 6 + t * 5)) ** 4 * np.exp(-(r / 0.7) ** 2) * (r > 0.04)
    nucleo = T.gauss(0, 0, 0.1 * abre + 0.01) * 2.4
    sub = np.random.default_rng(311)
    est = T.zero()
    for k in range(14):
        x, y = sub.uniform(-0.85, 0.85), sub.uniform(-0.85, 0.85)
        est += T.flare(x, y, 0.25, 0.4) * pulso((t * 2 + sub.uniform(0, 1)) % 1, 0, 1) * 0.9
    G += (bracos * 1.5 + nucleo + est) * env
    H += (nucleo + bracos * 0.5 + est * 0.8) * env
    return G, H


def chuva_de_meteoros(T, t, rng):
    """Chuva de meteoros: riscos diagonais caem em sequência e cada um estoura onde bate."""
    G, H = vazio(T)
    sub = np.random.default_rng(321)
    acc = T.zero()
    for k in range(10):
        a0 = k * 0.06
        x, y = sub.uniform(-0.55, 0.55), sub.uniform(-0.1, 0.45)
        p = ease_in(rel(t, a0, a0 + 0.14), 1.5)
        if t < a0:
            continue
        if p < 1:
            hx, hy = x - 0.7 * (1 - p), y - 0.9 * (1 - p)
            acc += T.tapered([(hx - 0.25, hy - 0.32, hx, hy, 1)], 0.04) + T.gauss(hx, hy, 0.03) * 1.5
        else:
            u = rel(t, a0 + 0.14, a0 + 0.45)
            acc += (T.gauss(x, y, 0.06) * 2 + T.ring(0.04 + 0.16 * u, 0.012, x, y)) * (1 - u)
    G += T.glow(acc, 1.1, 1, 0.02)
    H += acc * 0.9
    return G, H


def supernova(T, t, rng):
    """Supernova: um sol branco nasce, raios longos giram e uma casca de luz se expande."""
    G, H = vazio(T)
    nasce = ease_out(rel(t, 0, 0.25), 2)
    env = apaga(t, 0.6, 1)
    sol = T.gauss(0, 0, 0.12 + 0.12 * nasce) * 2.8
    raios = (np.abs(np.cos(T.ANG * 8 + t * 2)) ** 30) * np.exp(-(T.RAD / (0.4 + 0.5 * nasce)) ** 2) * 1.5
    casca = T.ring(0.2 + 0.75 * ease_out(rel(t, 0.15, 1), 2), 0.05) * (1 - rel(t, 0.15, 1)) ** 1.2 * 1.6
    G += (sol + raios) * env + casca
    H += (sol * 1.1 + raios * 0.6) * env + casca * 0.5
    return G, H


def pulso_emp(T, t, rng):
    """Pulso eletromagnético: quadrados que crescem girando, barras de falha e estalos."""
    G, H = vazio(T)
    acc = T.zero()
    for k in range(3):
        u = rel(t, k * 0.1, 0.6 + k * 0.1)
        if u <= 0 or u >= 1:
            continue
        s = 0.1 + 0.75 * ease_out(u, 2)
        a = 0.2 * k + u * 0.5
        c, sn = math.cos(a), math.sin(a)
        pts = [(c * x - sn * y, sn * x + c * y) for x, y in ((-s, -s), (s, -s), (s, s), (-s, s), (-s, -s))]
        acc += T.polyline(pts, 0.016, 1) * (1 - u)
    sub = np.random.default_rng(int(t * 30) + 331)
    falhas = T.zero()
    for _ in range(4):
        y = sub.uniform(-0.6, 0.6)
        falhas += np.exp(-((T.V - y) / 0.015) ** 2) * smooth(0.5 - np.abs(T.U - sub.uniform(-0.3, 0.3)), 0, 0.05)
    falhas *= pulso(t, 0, 0.7)
    flash = T.gauss(0, 0, 0.15) * some(t, 0, 0.3) * 2.5
    G += T.glow(acc, 1.3, 1, 0.02) + falhas * 1.2 + flash
    H += acc * 0.6 + falhas * 0.6 + flash
    return G, H


def pilar(T, t, rng):
    """Pilar de energia: coluna nasce do chão e sobe além do quadro, anéis subindo por ela."""
    G, H = vazio(T)
    sobe = ease_out(rel(t, 0, 0.25), 2)
    env = apaga(t, 0.6, 1)
    larg = 0.16 + 0.04 * math.sin(t * 30)
    coluna = np.exp(-(T.U / larg) ** 2) * smooth(0.5 - T.V, 0, 0.05) * smooth(T.V - 0.5 + 1.6 * sobe, 0, 0.3)
    nucleo = np.exp(-(T.U / (larg * 0.35)) ** 2) * smooth(0.5 - T.V, 0, 0.05) * smooth(T.V - 0.5 + 1.6 * sobe, 0, 0.3)
    aneis = sum(T.ring(larg * 1.6, 0.015, cy=0.45 - ((t * 1.5 + k / 4) % 1) * 1.3, squash=4) for k in range(4)) * janela(t, 0.15, 0.3)
    base = T.ring(0.3 + 0.2 * sobe, 0.04, cy=0.48, squash=4) * 1.3
    fa = faiscas(T, rng, t, 20, 0.6, 0.03, cone=(-math.pi + 0.3, -0.3), cy=0.45)
    G += (coluna * 1.3 + nucleo * 1.2 + aneis * 1.1 + base) * env + fa
    H += (nucleo * 1.4 + aneis * 0.3) * env
    return G, H


def transformacao(T, t, rng):
    """Transformação: aura em chamas sobe em volta, anéis de poder se abrem e um estouro final."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    n = _subindo(T, 341, t, 0.05, 1.6)
    corpo = np.hypot(T.U / 0.38, (T.V - 0.05) / 0.62)
    aura = smooth(1.0 + 0.25 * n * smooth(-T.V, -0.3, 0.6) - corpo, -0.05, 0.15) * (1 - smooth(0.75 - corpo, 0, 0.2) * 0.6)
    aura *= (0.7 + 0.3 * np.clip(n, -1, 1)) * janela(t, 0, 0.2)
    aneis = sum(T.ring(0.2 + 0.7 * rel(t, k * 0.15, 0.5 + k * 0.15), 0.02, cy=0.4, squash=3.2) * pulso(t, k * 0.15, 0.5 + k * 0.15) for k in range(4))
    estouro = T.gauss(0, 0, 0.28) * pulso(t, 0.5, 0.75) * 2 + T.ring(0.2 + 0.7 * rel(t, 0.5, 0.9), 0.04) * pulso(t, 0.5, 0.95) * 1.4
    fa = []
    for _ in range(26):
        f = (rng.uniform(0, 1) + t * 1.4) % 1
        fa.append((rng.uniform(-0.4, 0.4), 0.5 - f * 1.3, (1 - f) * rng.uniform(0.4, 1)))
    G += (aura * 1.3 + T.splats(fa, 0.012)) * env + aneis * 1.2 + estouro
    H += (aura * 0.5 + T.splats(fa, 0.01) * 0.7) * env + estouro
    return G, H


def atracao(T, t, rng):
    """Atração (Azul): tudo é puxado em espiral para um ponto, que se aperta e pulsa."""
    G, H = vazio(T)
    env = apaga(t, 0.7, 1)
    pts, segs = [], []
    for _ in range(40):
        f = (rng.uniform(0, 1) + t * 1.5) % 1
        a0 = rng.uniform(0, TAU)
        d = 0.95 * (1 - f) ** 1.3 + 0.05
        a = a0 + f * 2.5
        d2 = 0.95 * (1 - max(0, f - 0.08)) ** 1.3 + 0.05
        a2 = a0 + max(0, f - 0.08) * 2.5
        segs.append((math.cos(a2) * d2, math.sin(a2) * d2, math.cos(a) * d, math.sin(a) * d, f))
    riscos = T.tapered(segs, 0.02)
    ponto = T.gauss(0, 0, 0.08 + 0.02 * math.sin(t * 40)) * 2.6 + T.ring(0.13, 0.02) * 1.2
    G += (T.glow(riscos, 1, 1.1, 0.02) + ponto) * env
    H += (riscos * 0.6 + ponto) * env
    return G, H


def repulsao(T, t, rng):
    """Repulsão (Vermelho): um ponto vermelho estoura para fora em ondas e espinhos de força."""
    G, H = vazio(T)
    tt = rel(t, 0.12, 1)
    ponto = T.gauss(0, 0, 0.07) * (1 + 2 * rel(t, 0, 0.12)) * (t < 0.2) * 2
    ondas = sum(T.ring(0.1 + 0.85 * ease_out(rel(t, 0.12 + k * 0.06, 0.8 + k * 0.06), 2.4), 0.04 - 0.01 * k) * pulso(t, 0.12 + k * 0.06, 0.85 + k * 0.06) for k in range(3)) * 1.5
    espinhos = (np.abs(np.cos(T.ANG * 6)) ** 20) * np.exp(-((T.RAD - 0.3 - 0.5 * ease_out(tt, 2)) / 0.15) ** 2) * (1 - tt) * 1.8 * (t > 0.12)
    flash = T.gauss(0, 0, 0.3) * some(t, 0.12, 0.35) * 3
    G += ponto + ondas + espinhos + flash
    H += ponto + ondas * 0.4 + espinhos * 0.6 + flash
    return G, H


def dominio(T, t, rng):
    """Domínio: um círculo de céu infinito se abre, estrelas correndo para o centro e a borda acesa."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0, 0.35), 2.5)
    env = apaga(t, 0.75, 1)
    r = 0.85 * abre
    dentro = smooth(r - T.RAD, -0.01, 0.03)
    borda = T.ring(r, 0.025) * 1.6 + T.ring(r * 0.94, 0.008) * 0.8
    sub = np.random.default_rng(351)
    est = []
    for _ in range(60):
        a = sub.uniform(0, TAU)
        f = (sub.uniform(0, 1) + t * 0.8) % 1
        d = r * (1 - f)
        est.append((math.cos(a) * d, math.sin(a) * d, f * sub.uniform(0.4, 1)))
    estrelas = T.splats(est, 0.008) * dentro
    veu = dentro * 0.15
    G += (borda + estrelas * 1.6 + veu) * env
    H += (borda * 0.7 + estrelas) * env
    return G, H


def desintegrar(T, t, rng):
    """Desintegrar (Hakai): o alvo se desfaz em grãos de luz que sobem e somem no ar."""
    G, H = vazio(T)
    sub = np.random.default_rng(371)
    graos = []
    for _ in range(140):
        x, y = sub.normal(0, 0.18), sub.normal(0.05, 0.28)
        atraso = 0.1 + 0.5 * (0.6 - y) / 1.2 + sub.uniform(0, 0.1)
        u = rel(t, atraso, atraso + 0.45)
        dx = sub.uniform(-0.2, 0.3) * u
        dy = -0.6 * u * u
        b = (1 if t < atraso else (1 - u) ** 1.2) * janela(t, 0, 0.12)
        graos.append((x + dx, y + dy, b * sub.uniform(0.4, 1)))
    g = T.splats(graos, 0.012)
    silhueta = T.gauss(0, 0.05, 0.2, 0.32) * (1 - rel(t, 0.1, 0.6)) * janela(t, 0, 0.12) * 0.6
    brilho = T.gauss(0, 0, 0.35) * pulso(t, 0, 0.25) * 1.2
    G += g * 1.4 + silhueta + brilho
    H += g * 0.9 + brilho * 0.5
    return G, H


REGISTRO = [
    ("explosao_ki", explosao_ki, GRANDE, "explosão de ki em domo", False),
    ("esfera_espiral", esfera_espiral, GRANDE, "esfera em espiral moendo", False),
    ("buraco_negro", buraco_negro, GRANDE, "buraco negro sugando", False),
    ("gravidade", gravidade, GRANDE, "pressão de gravidade", False),
    ("cosmico", cosmico, GRANDE, "galáxia girando", False),
    ("chuva_de_meteoros", chuva_de_meteoros, GRANDE, "meteoros caindo", False),
    ("supernova", supernova, GRANDE, "sol que explode", False),
    ("pulso_emp", pulso_emp, GRANDE, "pulso eletromagnético", False),
    ("pilar", pilar, GRANDE, "pilar de energia subindo", False),
    ("transformacao", transformacao, GRANDE, "aura de transformação", False),
    ("atracao", atracao, GRANDE, "tudo puxado para um ponto", False),
    ("repulsao", repulsao, GRANDE, "estouro para fora", False),
    ("dominio", dominio, GRANDE, "domínio de céu infinito", False),
    ("desintegrar", desintegrar, GRANDE, "desintegração em grãos", False),
]
