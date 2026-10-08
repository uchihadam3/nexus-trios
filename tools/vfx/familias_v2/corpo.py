"""Golpes de corpo: chutes, pancadas de desenho animado, investidas, garras, mordidas."""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, TAU, apaga, back, contorno, ease_out, estrela, faiscas, forma, girado, jagged, janela,
                   lamina, poeira, pulso, rastro_de_velocidade, rel, smooth, some, vazio)


def chute_voador(T, t, rng):
    """Chute voador: rastro diagonal chegando do alto e estouro para a frente, em leque."""
    G, H = vazio(T)
    ang = math.atan2(0.55, 1.0)
    chega = ease_out(rel(t, 0, 0.22), 2)
    linhas = rastro_de_velocidade(T, rng, 9, ang, 0.7, 0.2, (1 - chega) * 0.55, seed=11) * apaga(t, 0.18, 0.5)
    tt = rel(t, 0.18, 1)
    clarao = T.flare(0, 0, 1.7, ang) * some(t, 0.18, 0.55, 1.1) * 2.6 + T.gauss(0, 0, 0.12) * some(t, 0.18, 0.5) * 2.5
    frente = T.arc_band(0.22 + 0.5 * ease_out(tt, 2.2), 0.07, ang - 1.1, ang + 1.1, crescente=True) * (1 - tt) ** 1.2 * 1.6 * (t > 0.18)
    fa = faiscas(T, rng, t, 22, 0.95, 0.035, cone=(ang - 0.75, ang + 0.75), gravidade=0.15, inicio=0.18)
    G += T.glow(linhas, 1, 1.2, 0.02) + clarao + frente + T.glow(fa, 1, 1.3, 0.02)
    H += linhas * 0.7 + clarao + fa * 0.8 + frente * 0.4
    return G, H


def chute_giratorio(T, t, rng):
    """Chute giratório: arco baixo dando volta e meia em perspectiva, poeira no chão."""
    G, H = vazio(T)
    giro = t * TAU * 1.5
    env = apaga(t, 0.6, 1)
    arco = T.arc_band(0.62, 0.11, -math.pi + giro, -math.pi + giro + 2.6, squash=0.32, cy=0.18, taper=1.4) * env
    eco = T.arc_band(0.5, 0.05, -math.pi + giro - 0.6, -math.pi + giro + 1.6, squash=0.32, cy=0.18) * env * 0.5
    ch = poeira(T, rng, t, 26, 0, 0.35, 0.8, 0.15, 0.035)
    clarao = T.gauss(0.45, 0.1, 0.13) * pulso(t, 0.25, 0.55) * 2.4 + T.flare(0.45, 0.1, 1.2, 0.3) * pulso(t, 0.25, 0.5) * 2
    G += T.glow(arco + eco, 1.2, 1.2, 0.02) + ch * 0.8 + clarao
    H += arco * 0.8 + clarao + ch * 0.2
    return G, H


def bonk(T, t, rng):
    """Pancada de desenho animado: achata, sobe um galo de luz e estrelinhas giram em volta."""
    G, H = vazio(T)
    clarao = T.gauss(0, 0, 0.12) * some(t, 0, 0.3) * 3
    anel = T.ring(0.15 + 0.45 * ease_out(t, 3), 0.035 * (1 - t) + 0.008, squash=1.8) * (1 - t) ** 1.4 * 1.5
    est = []
    sai = back(rel(t, 0.12, 0.4))
    for k in range(4):
        a = TAU * k / 4 + t * TAU * 1.2
        x, y = math.cos(a) * 0.42, -0.42 + math.sin(a) * 0.12
        est.append((estrela(x, y, 0.09 * sai * (0.8 + 0.3 * (math.sin(a) > 0)), a * 2), 1.0))
    estrelas = T.polys(est, 0.003) * apaga(t, 0.75, 1)
    orbita = T.ring(0.42, 0.012, cy=-0.42, squash=1 / 0.29) * 0.35 * janela(t, 0.12, 0.3) * apaga(t, 0.7, 1)
    G += clarao + anel + T.glow(estrelas, 1.3, 1, 0.02) + orbita
    H += clarao + estrelas * 0.9 + anel * 0.3
    return G, H



def _malho(cx, cy, ang, comp=0.78, cab=(0.27, 0.52), achata=1.0):
    """Marreta de desenho: cabo saindo da mão (cx, cy) na direção `ang` e a cabeça
    de madeira atravessada na ponta. `achata` < 1 amassa a cabeça contra o alvo."""
    c, s = math.cos(ang), math.sin(ang)
    nx, ny = -s, c
    hx, hy = cx + c * comp, cy + s * comp
    esp, larg = cab[0] * achata, cab[1] * (2 - achata) ** 0.6
    cabo = [(cx + nx * 0.035, cy + ny * 0.035), (hx + nx * 0.03, hy + ny * 0.03), (hx - nx * 0.03, hy - ny * 0.03),
            (cx - nx * 0.035, cy - ny * 0.035)]
    def ret(a0, a1, w):
        return [(hx + c * a0 + nx * w, hy + s * a0 + ny * w), (hx + c * a1 + nx * w, hy + s * a1 + ny * w),
                (hx + c * a1 - nx * w, hy + s * a1 - ny * w), (hx + c * a0 - nx * w, hy + s * a0 - ny * w)]
    cabeca = ret(-esp / 2, esp / 2, larg / 2)
    # as duas cintas de ferro perto das pontas da cabeça
    cintas = [(hx + nx * larg * k - c * esp / 2, hy + ny * larg * k - s * esp / 2, hx + nx * larg * k + c * esp / 2,
               hy + ny * larg * k + s * esp / 2, 1) for k in (-0.36, 0.36)]
    return cabo, cabeca, cintas, (hx + c * esp / 2, hy + s * esp / 2)


def marretada(T, t, rng):
    """Marretada de desenho animado: a marreta de madeira desce em arco (com rastro),
    bate, a cabeça amassa, um estouro em estrela sai do contato e estrelinhas giram."""
    G, H = vazio(T)
    mx, my = -0.6, 0.36
    a0, a1 = -1.62, -0.5
    bate = 0.24
    if t < bate:
        u = rel(t, 0, bate) ** 2.2                            # acelera ao descer
        ang = a0 + (a1 - a0) * u
        achata = 1.0
    else:
        u = rel(t, bate, 0.5)
        ang = a1 - 0.22 * math.sin(math.pi * min(1, u * 1.4)) * (1 - u)     # quica um pouco para cima
        achata = 1 - 0.32 * math.exp(-rel(t, bate, 1) * 9)
    some_ = apaga(t, 0.5, 0.72)
    cabo, cabeca, cintas, ponta = _malho(mx, my, ang, achata=achata)
    corpo = T.polys([(cabeca, 1.0)], 0.004)
    borda = corpo * (1 - smooth(T.blur(corpo, 0.025), 0.78, 0.97))
    pau = T.polys([(cabo, 1.0)], 0.004)
    aros = T.lines(cintas, 0.022, 0.002) * corpo
    # rastro: cópias fantasmas nos ângulos anteriores, só enquanto desce
    rastro = T.zero()
    if 0.05 < t < bate + 0.08:
        for k in range(1, 5):
            ua = max(0.0, rel(t - 0.025 * k, 0, bate)) ** 2.2
            _, cab_k, _, _ = _malho(mx, my, a0 + (a1 - a0) * ua)
            rastro += T.polys([(cab_k, 1.0)], 0.02) * (0.5 / k)
    marreta = (corpo * 0.55 + borda * 1.5 + pau * 0.7 - aros * 0.35).clip(0, None) * some_
    G += marreta + T.glow(rastro, 0.4, 0.8, 0.03) * 0.6
    H += corpo * 0.75 * some_ + pau * 0.5 * some_ + rastro * 0.15
    if t >= bate:
        tt = rel(t, bate, 1)
        cx, cy = ponta[0] * 0.3, ponta[1] * 0.3 + 0.05
        s_ = back(rel(t, bate, bate + 0.16), 2.4)
        sub = np.random.default_rng(57)
        raios = [sub.uniform(0.55, 0.85) for _ in range(9)]
        pts = []
        for k in range(18):
            a = TAU * k / 18 + 0.15
            r = (raios[k // 2] if k % 2 == 0 else 0.3) * s_ * (0.75 + 0.25 * tt)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r * 0.82))
        estouro = T.polys([(pts, 1.0)], 0.005)
        anel_e = estouro * (1 - smooth(T.blur(estouro, 0.03), 0.8, 0.97))
        ev = apaga(t, 0.42, 0.62)
        clarao = T.gauss(cx, cy, 0.14) * some(t, bate, bate + 0.25) * 3.2
        chao = T.ring(0.15 + 0.7 * ease_out(tt, 2.4), 0.04 * (1 - tt) + 0.008, cx=cx, cy=cy + 0.2, squash=3.4) * (1 - tt) ** 1.3 * 1.6
        acao = []
        for k in range(12):
            a = TAU * k / 12 + 0.26
            r0 = 0.62 * s_ + 0.06
            acao.append((cx + math.cos(a) * r0, cy + math.sin(a) * r0, cx + math.cos(a) * (r0 + 0.2), cy + math.sin(a) * (r0 + 0.2), 1))
        linhas = T.lines(acao, 0.016, 0.002) * pulso(t, bate + 0.02, 0.55)
        # estrelinhas girando em volta da "cabeça" de quem levou
        est = []
        sai = back(rel(t, 0.4, 0.62))
        for k in range(5):
            a = TAU * k / 5 + t * TAU * 1.4
            est.append((estrela(math.cos(a) * 0.38, -0.5 + math.sin(a) * 0.1, 0.075 * sai * (0.75 + 0.35 * (math.sin(a) > 0)), a * 2), 1.0))
        estrelas = T.polys(est, 0.003) * apaga(t, 0.85, 1) * (t > 0.4)
        G += (estouro * 0.45 + anel_e * 1.5) * ev + clarao + chao + linhas * 1.1 + T.glow(estrelas, 1.3, 1, 0.02)
        H += (estouro * 0.9 + anel_e * 0.4) * ev + clarao + linhas * 0.4 + estrelas * 0.9
    return G, H


def pow_cartoon(T, t, rng):
    """POW!: balão de estouro em zigue-zague que estala, com contorno e linhas de ação."""
    G, H = vazio(T)
    s = back(rel(t, 0, 0.22), 2.2) * (1 + 0.04 * math.sin(t * 40) * (t < 0.6))
    env = apaga(t, 0.6, 1)
    sub = np.random.default_rng(31)
    raios = [sub.uniform(0.62, 0.95) for _ in range(14)]
    pts, dentro = [], []
    for k in range(28):
        a = TAU * k / 28 + 0.1
        r = (raios[k // 2] if k % 2 == 0 else 0.42) * s
        pts.append((math.cos(a) * r, math.sin(a) * r))
        dentro.append((math.cos(a) * r * 0.62, math.sin(a) * r * 0.62))
    cheio = T.polys([(pts, 1.0)], 0.004)
    miolo = T.polys([(dentro, 1.0)], 0.004)
    borda = cheio * (1 - smooth(T.blur(cheio, 0.03), 0.8, 0.97))
    acao = []
    for k in range(16):
        a = TAU * k / 16 + 0.2
        r0 = 0.75 * s + 0.05
        acao.append((math.cos(a) * r0, math.sin(a) * r0, math.cos(a) * (r0 + 0.18), math.sin(a) * (r0 + 0.18), 1))
    linhas = T.lines(acao, 0.014, 0.002) * pulso(t, 0.05, 0.5)
    G += (cheio * 0.5 + borda * 1.6 + miolo * 0.9 + linhas * 1.2) * env
    H += (miolo * 1.1 + borda * 0.6 + linhas * 0.5) * env
    return G, H


def martelo(T, t, rng):
    """Martelada: risco que desce, onda achatada no chão, anéis metálicos e lascas para cima."""
    G, H = vazio(T)
    desce = ease_out(rel(t, 0, 0.16), 2)
    risco = T.polys([(lamina(0, -0.95, 0, -0.95 + 1.15 * desce, 0.07), 1)], 0.006) * apaga(t, 0.12, 0.35)
    tt = rel(t, 0.14, 1)
    chao = T.ring(0.12 + 0.75 * ease_out(tt, 2.2), 0.05 * (1 - tt) + 0.01, cy=0.22, squash=3.2) * (1 - tt) ** 1.2 * 1.8 * (t > 0.14)
    clang = sum(T.ring(0.08 + 0.25 * ease_out(rel(t, 0.14 + 0.07 * k, 0.6 + 0.07 * k), 2), 0.012) * pulso(t, 0.14 + 0.07 * k, 0.6 + 0.07 * k) for k in range(3))
    flare = T.flare(0, 0.2, 2.0, 0) * some(t, 0.14, 0.5) * 2.4
    fa = faiscas(T, rng, t, 26, 0.85, 0.035, cone=(-math.pi + 0.2, -0.2), gravidade=0.45, cy=0.2, inicio=0.14)
    G += T.glow(risco, 1.2, 1.2, 0.02) + chao + clang * 1.3 + flare + T.glow(fa, 1, 1.2, 0.02)
    H += risco * 0.8 + flare + fa * 0.8 + clang * 0.5
    return G, H


def investida(T, t, rng):
    """Investida: linhas de velocidade chegando da esquerda e um impacto que empurra para a frente."""
    G, H = vazio(T)
    chega = ease_out(rel(t, 0, 0.25), 2)
    linhas = rastro_de_velocidade(T, rng, 14, 0, 0.9, 0.35, (1 - chega) * 0.6 - 0.05, seed=21, largura=0.02) * apaga(t, 0.2, 0.55)
    tt = rel(t, 0.2, 1)
    on = t > 0.2
    clarao = T.gauss(0.05, 0, 0.16, 0.2) * some(t, 0.2, 0.55) * 3
    onda = T.arc_band(0.2 + 0.6 * ease_out(tt, 2), 0.09, -1.2, 1.2, crescente=True, cx=-0.1) * (1 - tt) ** 1.3 * 1.8 * on
    fa = faiscas(T, rng, t, 26, 1.0, 0.04, cone=(-0.8, 0.8), gravidade=0.2, inicio=0.2)
    G += T.glow(linhas, 1, 1.2, 0.02) + clarao + onda + T.glow(fa, 1, 1.2, 0.02)
    H += linhas * 0.6 + clarao + fa * 0.7 + onda * 0.4
    return G, H


def punho_gigante(T, t, rng):
    """Punho gigante: um punho de luz (dedos dobrados, polegar por cima) cresce até o alvo e estoura."""
    G, H = vazio(T)
    s = 0.35 + 0.7 * ease_out(rel(t, 0, 0.3), 2.5)
    env = apaga(t, 0.35, 0.7)
    u, v = T.U / s, T.V / s
    corpo = smooth(1 - ((u / 0.5) ** 4 + ((v - 0.05) / 0.42) ** 4), 0, 0.12)
    borda = corpo * (1 - smooth(1 - ((u / 0.44) ** 4 + ((v - 0.05) / 0.36) ** 4), 0, 0.12))
    divisas = T.zero()
    for k in range(1, 4):
        x = (-0.5 + k * 0.25) * s
        divisas += np.exp(-((T.U - x) / (0.012 * s)) ** 2) * smooth(-T.V, 0.02 * s, 0.1 * s) * corpo
    juntas = T.zero()
    for k in range(4):
        juntas += T.gauss((-0.375 + k * 0.25) * s, -0.3 * s, 0.06 * s, 0.035 * s)
    polegar = smooth(1 - (((u + 0.08) / 0.38) ** 2 + ((v - 0.12) / 0.1) ** 2), 0, 0.2)
    polegar_b = polegar * (1 - smooth(1 - (((u + 0.08) / 0.33) ** 2 + ((v - 0.12) / 0.06) ** 2), 0, 0.2))
    tt = rel(t, 0.3, 1)
    estouro = T.gauss(0, 0, 0.2 + 0.1 * tt) * some(t, 0.3, 0.65) * 3 + T.ring(0.2 + 0.65 * ease_out(tt, 2), 0.05 * (1 - tt) + 0.01) * (1 - tt) ** 1.3 * 1.6 * (t > 0.3)
    fa = faiscas(T, rng, t, 24, 0.95, 0.04, gravidade=0.2, inicio=0.3)
    G += (corpo * 0.35 + borda * 1.6 + divisas * 1.1 + juntas * 0.8 + polegar_b * 1.3) * env + estouro + T.glow(fa, 1, 1.2, 0.02)
    H += (borda * 0.7 + juntas * 0.5 + polegar_b * 0.5) * env + estouro + fa * 0.7
    return G, H


def soco_serio(T, t, rng):
    """Soco sério: um sopro gigante para a frente que abre o céu, anéis de pressão e nuvens rasgadas."""
    G, H = vazio(T)
    tt = ease_out(rel(t, 0, 0.5), 2)
    al, la = girado(T, 0)
    cone = np.exp(-(la / (0.12 + 0.35 * np.clip(al + 0.8, 0, 2) * 0.45)) ** 2) * smooth(al, -0.85, -0.6) * smooth(-al, -1.2, -0.6 + 1.6 * tt)
    nuvem = T.noise(np.random.default_rng(81), 0.08, 3)
    cone_n = cone * (0.55 + 0.45 * np.clip(nuvem * 0.5 + 0.5, 0, 1)) * apaga(t, 0.45, 1)
    aneis = T.zero()
    for k in range(4):
        u = rel(t, 0.05 + k * 0.08, 0.6 + k * 0.08)
        aneis += T.ring(0.15 + 0.55 * u, 0.025, cx=-0.6 + 1.3 * u, squash=0.55) * pulso(t, 0.05 + k * 0.08, 0.6 + k * 0.08)
    clarao = T.gauss(-0.55, 0, 0.18) * some(t, 0, 0.4) * 3
    G += cone_n * 1.6 + aneis * 1.4 + clarao
    H += cone_n * 0.7 + clarao + aneis * 0.4
    return G, H


def faisca_negra(T, t, rng):
    """Faísca negra: raios curtos e grossos estalando em volta, o espaço rachando no centro."""
    G, H = vazio(T)
    env = apaga(t, 0.5, 1)
    sub = np.random.default_rng(int(t * 997) + 7)
    lin = T.zero()
    for k in range(7):
        a = TAU * k / 7 + sub.uniform(-0.3, 0.3)
        r0, r1 = sub.uniform(0.12, 0.2), sub.uniform(0.55, 0.85)
        pts = jagged(sub, math.cos(a) * r0, math.sin(a) * r0, math.cos(a) * r1, math.sin(a) * r1, 4, 0.35)
        lin += T.polyline(pts, 0.026, 1)
    vazio_c = T.ring(0.16, 0.05) * 1.4 + T.gauss(0, 0, 0.1) * 0.2
    distorce = T.ring(0.2 + 0.6 * ease_out(t, 2), 0.02) * (1 - t) ** 1.6 * 1.5
    flash = T.gauss(0, 0, 0.32) * some(t, 0, 0.18) * 2.5
    G += T.glow(lin, 1.5, 1.8, 0.03) * env + vazio_c * env + distorce + flash
    H += lin * 1.2 * env + distorce * 0.5 + flash * 0.5
    return G, H


def chicote(T, t, rng):
    """Chicote: a corda se desenrola em onda e estala na ponta, com faíscas."""
    G, H = vazio(T)
    prog = ease_out(rel(t, 0, 0.32), 1.6)
    env = apaga(t, 0.5, 0.9)
    pts = []
    for k in range(60):
        u = k / 59 * prog
        x = -0.95 + 1.3 * u
        y = 0.25 * math.sin(u * 9 - t * 14) * (1 - u) ** 1.2 - 0.35 * u * (1 - u)
        pts.append((x, y))
    corda = T.polyline(pts, 0.022, 1) * env
    px, py = pts[-1]
    tt = rel(t, 0.3, 1)
    estalo = (T.flare(px, py, 1.2, 0.5) * 2.4 + T.gauss(px, py, 0.08) * 2.5) * some(t, 0.3, 0.6) + T.ring(0.05 + 0.4 * ease_out(tt, 2), 0.015, px, py) * (1 - tt) ** 1.5 * 1.4 * (t > 0.3)
    fa = faiscas(T, rng, t, 16, 0.6, 0.03, cx=px, cy=py, inicio=0.3)
    G += T.glow(corda, 1.2, 1, 0.015) + estalo + T.glow(fa, 1, 1.2, 0.02)
    H += corda * 0.6 + estalo + fa * 0.7
    return G, H


def garras(T, t, rng):
    """Garras: três rasgos paralelos em diagonal, um logo depois do outro."""
    G, H = vazio(T)
    rasgos, bordas = T.zero(), T.zero()
    for k in range(3):
        off = (k - 1) * 0.24
        a, b = 0.05 * k, 0.05 * k + 0.2
        p = ease_out(rel(t, a, b), 2)
        x1, y1, x2, y2 = -0.55 + off, -0.65 + off * 0.3, 0.45 + off, 0.6 + off * 0.3
        some_k = apaga(t, b + 0.15, 1, 1.3)
        corpo = T.polys([(lamina(x1, y1, x2, y2, 0.07, p, inicio=max(0, rel(t, b + 0.1, 0.9))), 1)], 0.004)
        rasgos += corpo * some_k
        bordas += T.polys([(lamina(x1, y1, x2, y2, 0.025, p), 1)], 0.002) * some_k
    fa = faiscas(T, rng, t, 20, 0.7, 0.03, gravidade=0.3, inicio=0.1)
    G += T.glow(rasgos, 1.1, 1.1, 0.02) + bordas * 1.2 + T.glow(fa, 1, 1, 0.02)
    H += bordas * 1.3 + rasgos * 0.3 + fa * 0.6
    return G, H


def mordida(T, t, rng):
    """Mordida: duas fileiras de dentes de luz fecham no alvo e estalam."""
    G, H = vazio(T)
    fecha = back(rel(t, 0.05, 0.3), 1.2)
    abre = 0.55 * (1 - fecha) + 0.08
    env = apaga(t, 0.45, 0.85)
    dentes = []
    for lado in (-1, 1):
        for k in range(6):
            x = -0.5 + k * 0.2
            y = lado * (abre + 0.06 * (x * x))
            dentes.append(([(x - 0.08, y), (x + 0.08, y), (x, y - lado * 0.2)], 1.0))
    d = T.polys(dentes, 0.004) * env
    maxilar = sum(T.arc_band(0.75, 0.025, a0, a1, squash=0.45, cy=lado * (abre + 0.3)) for lado, a0, a1 in ((-1, 0.5, 2.6), (1, -2.6, -0.5))) * env
    tt = rel(t, 0.3, 1)
    estalo = T.gauss(0, 0, 0.15) * some(t, 0.28, 0.6) * 2.8 + T.ring(0.1 + 0.5 * ease_out(tt, 2), 0.02) * (1 - tt) ** 1.4 * (t > 0.3) * 1.3
    fa = faiscas(T, rng, t, 14, 0.6, 0.03, inicio=0.3)
    G += T.glow(d, 1.2, 1, 0.02) + maxilar * 0.8 + estalo + T.glow(fa, 1, 1, 0.02)
    H += d * 0.8 + estalo + fa * 0.6
    return G, H


def bastao(T, t, rng):
    """Bastão: arco largo e cheio de cima para baixo, baque redondo e poeira."""
    G, H = vazio(T)
    p = ease_out(rel(t, 0, 0.28), 2)
    env = apaga(t, 0.35, 0.75)
    arco = T.arc_band(0.55, 0.13, -2.6, -2.6 + 3.0 * p + 0.01, squash=0.8, taper=0.6) * env
    eco = T.arc_band(0.42, 0.04, -2.6, -2.6 + 3.0 * p + 0.01, squash=0.8) * env * 0.6
    tt = rel(t, 0.26, 1)
    baque = T.gauss(0.3, 0.35, 0.14) * some(t, 0.26, 0.6) * 2.6 + T.ring(0.1 + 0.45 * ease_out(tt, 2), 0.03 * (1 - tt) + 0.01, 0.3, 0.35, squash=1.6) * (1 - tt) ** 1.3 * 1.5 * (t > 0.26)
    ch = poeira(T, rng, t, 18, 0.3, 0.4, 0.5, 0.2, 0.03, inicio=0.26)
    G += T.glow(arco, 1, 1.1, 0.02) + eco + baque + ch * 0.8
    H += arco * 0.5 + baque + ch * 0.2
    return G, H


def tentaculos(T, t, rng):
    """Tentáculos: cinco gavinhas grossas saem das bordas, chicoteiam o alvo e recolhem."""
    G, H = vazio(T)
    sub = np.random.default_rng(57)
    lin, pontas = T.zero(), []
    for k in range(5):
        a = TAU * k / 5 + 0.4
        atraso = k * 0.04
        alc = math.sin(math.pi * rel(t, atraso, 0.75 + atraso)) ** 0.7
        fase = sub.uniform(0, TAU)
        pts = []
        for j in range(30):
            u = j / 29
            r = 1.05 - (1.05 - 0.12) * u * alc
            w = 0.12 * math.sin(u * 6 + fase + t * 10) * u
            x, y = math.cos(a) * r - math.sin(a) * w, math.sin(a) * r + math.cos(a) * w
            pts.append((x, y))
        lin += T.polyline(pts, 0.035, 1)
        pontas.append((pts[-1][0], pts[-1][1], alc))
    pts_ = T.splats(pontas, 0.03)
    impacto = T.gauss(0, 0, 0.14) * pulso(t, 0.2, 0.55) * 2.2
    G += T.glow(lin, 0.9, 1.1, 0.025) + pts_ * 1.5 + impacto
    H += lin * 0.35 + pts_ + impacto
    return G, H


def pisao(T, t, rng):
    """Pisão: cratera no chão, rachaduras correndo para os lados e colunas de poeira subindo."""
    G, H = vazio(T)
    sub = np.random.default_rng(66)
    cres = ease_out(rel(t, 0, 0.3), 2)
    env = apaga(t, 0.6, 1)
    rach = T.zero()
    for k in range(9):
        a = TAU * k / 9 + sub.uniform(-0.2, 0.2)
        r = sub.uniform(0.45, 0.85) * cres
        pts = jagged(sub, 0, 0, math.cos(a) * r, math.sin(a) * r * 0.32, 4, 0.3)
        rach += T.polyline([(x, y + 0.3) for x, y in pts], 0.012, 1)
    cratera = T.ring(0.22, 0.04, cy=0.3, squash=3) * env * 1.4 + T.gauss(0, 0.3, 0.2, 0.06) * some(t, 0, 0.4) * 2.5
    colunas = poeira(T, rng, t, 30, 0, 0.3, 0.75, 0.45, 0.04, inicio=0.05)
    G += T.glow(rach, 1.2, 1, 0.02) * env + cratera + colunas * 0.9
    H += rach * 0.8 * env + cratera * 0.5 + colunas * 0.2
    return G, H


def esticar(T, t, rng):
    """Braço esticado: uma faixa elástica chega da borda, o punho bate e a faixa volta tremendo."""
    G, H = vazio(T)
    ida = ease_out(rel(t, 0, 0.22), 2.5)
    volta = ease_out(rel(t, 0.45, 0.85), 2)
    ponta = -1.0 + 1.0 * ida - 0.8 * volta
    mola = 0.05 * math.sin(t * 50) * (1 - rel(t, 0.2, 0.6))
    pts = [(-1.05 + (ponta + 1.05) * k / 30, mola * math.sin(k / 30 * math.pi * 3)) for k in range(31)]
    faixa = T.polyline(pts, 0.07, 1)
    punho = T.gauss(ponta, 0, 0.11) * 1.5
    tt = rel(t, 0.2, 1)
    bate = T.gauss(0, 0, 0.14) * some(t, 0.2, 0.5) * 2.8 + T.ring(0.12 + 0.5 * ease_out(tt, 2), 0.03 * (1 - tt) + 0.01) * (1 - tt) ** 1.4 * 1.4 * (t > 0.2)
    G += (T.glow(faixa, 0.9, 1, 0.02) + punho) * apaga(t, 0.8, 1) + bate
    H += (faixa * 0.3 + punho * 0.8) * apaga(t, 0.8, 1) + bate
    return G, H


REGISTRO = [
    ("chute_voador", chute_voador, GRANDE, "chute voador (diagonal)", False),
    ("chute_giratorio", chute_giratorio, GRANDE, "chute giratório baixo", False),
    ("bonk", bonk, GRANDE, "pancada de desenho com estrelinhas", False),
    ("pow_cartoon", pow_cartoon, GRANDE, "balão POW de quadrinho", False),
    ("martelo", martelo, GRANDE, "martelada no chão", False),
    ("marretada", marretada, GRANDE, "marreta de desenho batendo", False),
    ("investida", investida, GRANDE, "investida com linhas de velocidade", False),
    ("punho_gigante", punho_gigante, GRANDE, "silhueta de punho gigante", False),
    ("soco_serio", soco_serio, GRANDE, "sopro gigante para a frente", False),
    ("faisca_negra", faisca_negra, GRANDE, "faísca negra (raios grossos)", False),
    ("chicote", chicote, GRANDE, "chicote estalando", False),
    ("garras", garras, GRANDE, "três rasgos de garra", False),
    ("mordida", mordida, GRANDE, "dentes fechando", False),
    ("bastao", bastao, GRANDE, "golpe de bastão", False),
    ("tentaculos", tentaculos, GRANDE, "tentáculos chicoteando", False),
    ("pisao", pisao, GRANDE, "pisão com rachaduras", False),
    ("esticar", esticar, GRANDE, "braço elástico", False),
]
