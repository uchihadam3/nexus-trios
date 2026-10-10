"""Magia e mente: olho, hipnose, tempo, runas, ilusão, portais, sorte, invocação, lua vermelha."""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, TAU, _subindo, apaga, back, ease_in, ease_out, estrela, faiscas, girado, jagged, janela,
                   lamina, poeira, pulso, rel, smooth, some, vazio)


def olho(T, t, rng):
    """Olho: um olho gigante se abre sobre o alvo, a íris gira e fixa, e fecha num piscar."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0, 0.25), 2) * (1 - ease_in(rel(t, 0.75, 0.9), 2))
    h = 0.32 * abre + 0.005
    w = 0.7
    # pálpebras: duas parábolas
    cima = -h * (1 - (T.U / w) ** 2)
    baixo = h * (1 - (T.U / w) ** 2)
    dentro = smooth(T.V - cima, 0, 0.02) * smooth(baixo - T.V, 0, 0.02) * (np.abs(T.U) < w)
    borda = (np.exp(-((T.V - cima) / 0.015) ** 2) + np.exp(-((T.V - baixo) / 0.015) ** 2)) * (np.abs(T.U) < w) * smooth(w - np.abs(T.U), 0, 0.1)
    iris = (T.ring(0.2, 0.025) + T.ring(0.12, 0.012)) * dentro
    marcas = (np.abs(np.cos(3 * (T.ANG - t * 6))) ** 12) * smooth(T.RAD, 0.11, 0.13) * smooth(0.19 - T.RAD, 0, 0.02) * dentro
    pupila = T.gauss(0, 0, 0.05) * dentro * 1.5
    raios = (np.abs(np.cos(T.ANG * 10)) ** 20) * smooth(T.RAD, 0.35, 0.5) * np.exp(-T.RAD * 2) * abre * 0.8
    G += dentro * 0.25 + borda * 1.5 + iris * 1.4 + marcas * 1.2 + pupila + raios
    H += borda * 0.8 + iris * 0.7 + pupila
    return G, H


def hipnose(T, t, rng):
    """Hipnose: espiral girando no alvo, anéis pulsando para dentro, estrelas tontas."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.7, 1)
    esp = (0.5 + 0.5 * np.cos(T.ANG - T.RAD * 18 + t * 18)) ** 6 * smooth(0.7 - T.RAD, 0, 0.15) * smooth(T.RAD, 0.03, 0.08)
    aneis = sum(T.ring(0.7 * (1 - ((t * 1.5 + k / 3) % 1)), 0.015) * math.sin(math.pi * ((t * 1.5 + k / 3) % 1)) for k in range(3))
    G += (esp * 1.4 + aneis * 0.9) * env
    H += esp * 0.6 * env
    return G, H


def relogio(T, t, rng):
    """Tempo: um mostrador de relógio surge, os ponteiros giram rápido e travam; a imagem ondula."""
    G, H = vazio(T)
    abre = back(rel(t, 0, 0.25), 1.2)
    env = apaga(t, 0.75, 1)
    r = 0.6 * abre + 0.01
    aro = T.ring(r, 0.02) * 1.3 + T.ring(r * 0.9, 0.006) * 0.6
    marcas = []
    for k in range(12):
        a = TAU * k / 12
        l = 0.12 if k % 3 == 0 else 0.06
        marcas.append((math.cos(a) * r * 0.88, math.sin(a) * r * 0.88, math.cos(a) * (r * 0.88 - l * abre), math.sin(a) * (r * 0.88 - l * abre), 1))
    gira = ease_out(rel(t, 0.1, 0.55), 3) * TAU * 3
    pont = [(0, 0, math.cos(gira - math.pi / 2) * r * 0.75, math.sin(gira - math.pi / 2) * r * 0.75, 1),
            (0, 0, math.cos(gira / 12 - math.pi / 2 + 1) * r * 0.5, math.sin(gira / 12 - math.pi / 2 + 1) * r * 0.5, 1)]
    m = T.lines(marcas, 0.012, 0.002)
    p = T.lines(pont, 0.02, 0.002)
    onda = T.ring(r * (1 + 0.4 * rel(t, 0.55, 0.9)), 0.03) * pulso(t, 0.55, 0.9) * 1.4
    trava = T.gauss(0, 0, 0.06) * 2 * janela(t, 0.5, 0.55)
    G += (T.glow(aro + m + p, 1.2, 1, 0.02) + trava) * env + onda
    H += (aro * 0.5 + p + trava) * env
    return G, H


def runas(T, t, rng):
    """Runas: um círculo de símbolos se acende em volta do alvo e as runas sobem uma a uma."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    sq = 0.35
    aro = (T.ring(0.65, 0.012, cy=0.35, squash=1 / sq) + T.ring(0.55, 0.008, cy=0.35, squash=1 / sq)) * janela(t, 0, 0.2) * 1.3
    sub = np.random.default_rng(601)
    simb = T.zero()
    for k in range(8):
        a = TAU * k / 8 + t * 0.6
        x, y = math.cos(a) * 0.6, 0.35 + math.sin(a) * 0.6 * sq
        sobe = ease_out(rel(t, 0.15 + k * 0.05, 0.6 + k * 0.05), 2) * 0.55
        y -= sobe
        segs = []
        for _ in range(3):
            x1, y1 = x + sub.uniform(-0.05, 0.05), y + sub.uniform(-0.06, 0.06)
            segs.append((x1, y1, x1 + sub.uniform(-0.05, 0.05), y1 + sub.uniform(-0.06, 0.06), 1))
        simb += T.lines(segs, 0.011, 0.002) * janela(t, 0.1 + k * 0.04, 0.2 + k * 0.04)
    G += (aro + T.glow(simb, 1.4, 1.2, 0.02)) * env
    H += (aro * 0.4 + simb) * env
    return G, H


def sarcofago(T, t, rng):
    """Sarcófago: uma caixa escura se fecha em volta do alvo, as faces se encaixam e ela racha em luz."""
    G, H = vazio(T)
    fecha = ease_out(rel(t, 0, 0.3), 2.5)
    env = apaga(t, 0.8, 1)
    w, h = 0.3, 0.55
    d = (1 - fecha) * 0.6
    faces = []
    faces.append(([(-w - d, -h), (-w * 0.2 - d, -h), (-w * 0.2 - d, h), (-w - d, h)], 1))
    faces.append(([(w * 0.2 + d, -h), (w + d, -h), (w + d, h), (w * 0.2 + d, h)], 1))
    faces.append(([(-w * 0.2, -h - d), (w * 0.2, -h - d), (w * 0.2, -h * 0.3 - d), (-w * 0.2, -h * 0.3 - d)], 1))
    f = T.polys(faces, 0.004)
    contorno = f * (1 - smooth(T.blur(f, 0.02), 0.8, 0.97))
    sub = np.random.default_rng(611)
    rach = sum(T.polyline(jagged(sub, sub.uniform(-0.2, 0.2), -h, sub.uniform(-0.2, 0.2), h, 4, 0.2), 0.012, 1) for _ in range(3)) * janela(t, 0.45, 0.55)
    luz = T.gauss(0, 0, 0.22, 0.4) * pulso(t, 0.6, 0.85) * 1.6
    G += (f * 0.35 + contorno * 1.4 + T.glow(rach, 1.4, 1.4, 0.02)) * env + luz
    H += (contorno * 0.5 + rach * 1.2) * env + luz * 0.8
    return G, H


def encanto(T, t, rng):
    """Encanto: brilhos de estrela giram em espiral e pousam no alvo com um tilintar de luz."""
    G, H = vazio(T)
    env = apaga(t, 0.7, 1)
    est = []
    for k in range(10):
        u = rel(t, k * 0.03, 0.55 + k * 0.03)
        a = TAU * k / 10 + u * 5
        r = 0.8 * (1 - u) + 0.08
        x, y = math.cos(a) * r, math.sin(a) * r * 0.8
        est.append((estrela(x, y, 0.06 * (1 - 0.4 * u), u * 4, 4, 0.35), math.sin(math.pi * u) + 0.01))
    e = T.polys(est, 0.003)
    rastro = []
    for _ in range(40):
        u = rng.uniform(0, 1)
        a = rng.uniform(0, TAU) + u * 3
        r = 0.8 * u
        rastro.append((math.cos(a) * r, math.sin(a) * r * 0.8, (1 - u) * pulso(t, 0, 0.8) * rng.uniform(0.3, 1)))
    pouso = T.gauss(0, 0, 0.12) * pulso(t, 0.45, 0.8) * 2 + T.flare(0, 0, 1.2, 0.4) * pulso(t, 0.5, 0.75) * 1.4
    G += (T.glow(e, 1.4, 1, 0.02) + T.splats(rastro, 0.008) * 1.2) * env + pouso
    H += (e + T.splats(rastro, 0.006) * 0.6) * env + pouso
    return G, H


def caveira(T, t, rng):
    """Caveira: uma caveira de luz surge sobre o alvo, abre a boca e se desfaz em fumaça."""
    G, H = vazio(T)
    s = 0.5 + 0.5 * back(rel(t, 0, 0.3), 1.4)
    env = apaga(t, 0.6, 1)
    u, v = T.U / s, T.V / s
    cranio = smooth(1 - ((u / 0.42) ** 2 + ((v + 0.1) / 0.38) ** 2), 0, 0.1)
    mand = smooth(1 - ((u / 0.25) ** 2 + ((v - 0.28 - 0.06 * pulso(t, 0.3, 0.6)) / 0.13) ** 2), 0, 0.15)
    olhos = smooth(1 - (((np.abs(u) - 0.16) / 0.1) ** 2 + ((v + 0.05) / 0.11) ** 2), 0, 0.15)
    nariz = smooth(1 - ((u / 0.04) ** 2 + ((v - 0.12) / 0.06) ** 2), 0, 0.2)
    corpo = np.clip(cranio + mand - olhos - nariz, 0, 1)
    borda = corpo * (1 - smooth(T.blur(corpo, 0.02), 0.75, 0.95))
    fumo = _subindo(T, 621, t, 0.06, 1)
    some_ = rel(t, 0.55, 1)
    desfaz = corpo * np.clip(1 - some_ * 1.5 + 0.4 * fumo, 0, 1)
    G += (desfaz * 0.6 + borda * 1.4 * (1 - some_)) * env + T.gauss(0, 0, 0.3) * pulso(t, 0.25, 0.6) * 0.4
    H += (borda * 0.6 * (1 - some_)) * env
    return G, H


def clones(T, t, rng):
    """Clones: silhuetas iguais aparecem em leque em volta do alvo, piscam e somem uma a uma."""
    G, H = vazio(T)
    acc = T.zero()
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * 0.55
        d = 0.5 * ease_out(rel(t, k * 0.04, 0.3 + k * 0.04), 2)
        x, y = math.cos(a) * d, 0.1 + math.sin(a) * d * 0.4
        vida = janela(t, k * 0.04, 0.1 + k * 0.04) * apaga(t, 0.5 + k * 0.08, 0.7 + k * 0.08)
        cabeca = T.gauss(x, y - 0.25, 0.07)
        tronco = T.gauss(x, y + 0.02, 0.1, 0.18)
        sil = smooth(cabeca + tronco, 0.45, 0.6)
        acc += (sil * 0.35 + sil * (1 - smooth(T.blur(sil, 0.015), 0.8, 0.97)) * 1.4) * vida
    puff = sum(poeira(T, rng, t, 8, math.cos(-math.pi / 2 + (k - 2) * 0.55) * 0.5, 0.1, 0.2, 0.1, 0.03, inicio=0.5 + k * 0.08) for k in range(5))
    G += acc + puff * 0.6
    H += acc * 0.4
    return G, H


def teleporte(T, t, rng):
    """Teleporte: a luz implode num risco vertical, some, e reaparece explodindo do lado."""
    G, H = vazio(T)
    fecha = ease_in(rel(t, 0, 0.25), 2)
    risco = np.exp(-(T.U / (0.25 * (1 - fecha) + 0.01)) ** 2) * smooth(0.5 - np.abs(T.V), 0, 0.2) * (t < 0.3) * (0.4 + fecha)
    tt = rel(t, 0.35, 1)
    volta = (T.ring(0.05 + 0.6 * ease_out(tt, 2.5), 0.02) * (1 - tt) * 1.6 + T.gauss(0, 0, 0.1) * some(t, 0.35, 0.6) * 2.5) * (t > 0.35)
    linhas = []
    for k in range(10):
        a = TAU * k / 10
        r0, r1 = 0.1 + 0.4 * tt, 0.2 + 0.6 * tt
        linhas.append((math.cos(a) * r0, math.sin(a) * r0, math.cos(a) * r1, math.sin(a) * r1, (1 - tt) * (t > 0.35)))
    G += risco * 1.6 + volta + T.lines(linhas, 0.012, 0.002)
    H += risco + volta
    return G, H


def fenda(T, t, rng):
    """Fenda dimensional: o ar rasga numa linha que se abre em olho, borda acesa e vazio dentro."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0.1, 0.4), 2) * (1 - ease_in(rel(t, 0.7, 0.95), 2))
    risca = ease_out(rel(t, 0, 0.12), 2)
    al, la = girado(T, -0.5)
    comp = 0.75 * risca
    perfil = (0.2 * abre + 0.01) * np.sqrt(np.clip(1 - (al / max(comp, 0.01)) ** 2, 0, 1))
    dentro = smooth(perfil - np.abs(la), 0, 0.02)
    borda = np.exp(-((np.abs(la) - perfil) / 0.012) ** 2) * (np.abs(al) < comp)
    n = T.noise(np.random.default_rng(631), 0.04, 2)
    estrelas = (n > 1.8).astype(np.float32) * dentro
    fa = faiscas(T, rng, t, 14, 0.5, 0.025, inicio=0.05)
    G += borda * 1.8 + dentro * 0.25 + estrelas + fa * 0.7
    H += borda * 1.2 + estrelas * 0.6
    return G, H


def sorte(T, t, rng):
    """Sorte: dois dados rolam e quicam, trevos e estrelinhas pulam quando param."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    dados, pontos = [], T.zero()
    for k, x0 in enumerate((-0.25, 0.22)):
        u = rel(t, 0, 0.5)
        x = x0 - 0.5 * (1 - u)
        y = 0.2 - abs(math.sin(u * math.pi * 3)) * 0.35 * (1 - u)
        a = (1 - ease_out(u, 2)) * 8 + k
        s = 0.16
        c, sn = math.cos(a), math.sin(a)
        dados.append(([(x + c * px - sn * py, y + sn * px + c * py) for px, py in ((-s, -s), (s, -s), (s, s), (-s, s))], 1))
        for px, py in ((0, 0), (-0.08, -0.08), (0.08, 0.08))[: 2 + k]:
            pontos += T.gauss(x + c * px - sn * py, y + sn * px + c * py, 0.022)
    d = T.polys(dados, 0.003)
    contorno = d * (1 - smooth(T.blur(d, 0.012), 0.8, 0.97))
    pula = []
    for _ in range(14):
        a = rng.uniform(-math.pi, 0)
        u = rel(t, 0.5, 1)
        pula.append((math.cos(a) * 0.6 * u, 0.1 + math.sin(a) * 0.5 * u + 0.4 * u * u, (1 - u) * (t > 0.5)))
    G += (d * 0.4 + contorno * 1.4 + T.splats(pula, 0.02) * 1.2) * env
    H += (contorno * 0.5 + pontos * 0.5) * env
    G -= pontos * 0.3 * env
    return G, H


def confete(T, t, rng):
    """Confete: um estouro de festa, pedacinhos girando e caindo devagar, serpentinas."""
    G, H = vazio(T)
    tt = rel(t, 0, 1)
    pedacos = []
    for _ in range(50):
        a = rng.uniform(-math.pi, 0)
        v = rng.uniform(0.4, 1)
        x = math.cos(a) * v * ease_out(tt, 2.5)
        y = math.sin(a) * v * ease_out(tt, 2.5) + 0.6 * tt * tt
        g = rng.uniform(0, 6) + tt * rng.uniform(6, 14)
        w = 0.025 * abs(math.cos(g)) + 0.004
        pedacos.append(([(x - w, y - 0.02), (x + w, y - 0.02), (x + w, y + 0.02), (x - w, y + 0.02)], (1 - tt * 0.7) * rng.uniform(0.5, 1)))
    p = T.polys(pedacos, 0.002)
    serp = sum(T.polyline([(math.cos(a0) * u * 0.7 + 0.05 * math.sin(u * 20), math.sin(a0) * u * 0.6 + 0.3 * u * u) for u in np.linspace(0, ease_out(tt, 2), 20)], 0.01, 1) for a0 in (-2.4, -1.6, -0.8)) * (1 - tt)
    estouro = T.gauss(0, 0, 0.12) * some(t, 0, 0.25) * 2.5
    G += p * 1.5 + serp + estouro
    H += p * 0.6 + estouro
    return G, H


def confusao(T, t, rng):
    """Confusão: pontos de interrogação e estrelinhas giram em volta da cabeça do alvo."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.75, 1)
    acc = T.zero()
    for k in range(3):
        a = TAU * k / 3 + t * TAU * 1.2
        x, y = math.cos(a) * 0.4, -0.4 + math.sin(a) * 0.12
        s = 0.11 * (0.8 + 0.25 * (math.sin(a) > 0))
        pts = [(x + s * 0.6 * math.cos(b), y - s * 0.4 + s * 0.6 * math.sin(b)) for b in np.linspace(math.pi, TAU + 0.6, 14)]
        pts += [(x + s * 0.1, y + s * 0.5)]
        acc += T.polyline(pts, 0.02, 1) + T.gauss(x + s * 0.1, y + s * 0.95, 0.018) * 1.5
    est = T.polys([(estrela(math.cos(a) * 0.4, -0.4 + math.sin(a) * 0.12, 0.05, a, 5), 1) for a in (TAU * (k + 0.5) / 3 + t * TAU * 1.2 for k in range(3))], 0.003)
    G += (T.glow(acc, 1.3, 1, 0.02) + est * 1.2) * env
    H += (acc * 0.8 + est * 0.6) * env
    return G, H


def pentagrama(T, t, rng):
    """Pentagrama: um círculo infernal se desenha no chão, as pontas acendem e chamas sobem."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    sq = 0.4
    prog = rel(t, 0, 0.4)
    aro = T.ring(0.68, 0.014, cy=0.3, squash=1 / sq) * janela(t, 0, 0.15) * 1.4
    pts = []
    for k in range(6):
        a = -math.pi / 2 + TAU * (k * 2 % 5) / 5
        pts.append((math.cos(a) * 0.66, 0.3 + math.sin(a) * 0.66 * sq))
    tracado = []
    n_tot = 5 * 10
    n = int(prog * n_tot)
    for k in range(5):
        (ax, ay), (bx, by) = pts[k], pts[k + 1]
        for j in range(10):
            if len(tracado) <= n:
                u = j / 9
                tracado.append((ax + (bx - ax) * u, ay + (by - ay) * u))
    linha = T.polyline(tracado, 0.012, 1)
    chamas = T.zero()
    for k in range(5):
        x, y = pts[k]
        c = np.exp(-((T.U - x) / 0.05) ** 2) * smooth(y - T.V, 0, 0.02) * smooth(T.V - y + 0.3 * janela(t, 0.4, 0.55), 0, 0.15)
        chamas += c * (0.6 + 0.4 * _subindo(T, 641 + k, t, 0.04, 1.5).clip(-1, 1))
    G += (aro + T.glow(linha, 1.3, 1.2, 0.02) + chamas * 1.2) * env
    H += (linha + chamas * 0.4) * env
    return G, H


def invocacao(T, t, rng):
    """Invocação: um círculo se abre no chão e uma silhueta de luz sobe dele, com faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    abre = ease_out(rel(t, 0, 0.25), 2)
    circ = (T.ring(0.6 * abre, 0.016, cy=0.45, squash=3.5) + T.ring(0.48 * abre, 0.01, cy=0.45, squash=3.5)) * 1.4
    sobe = ease_out(rel(t, 0.2, 0.6), 2)
    y0 = 0.45 - 0.65 * sobe
    sil = smooth(T.gauss(0, y0 - 0.22, 0.09) + T.gauss(0, y0 + 0.08, 0.15, 0.22), 0.45, 0.6) * smooth(0.45 - T.V, 0, 0.05)
    contorno = sil * (1 - smooth(T.blur(sil, 0.015), 0.8, 0.97))
    coluna = np.exp(-(T.U / 0.3) ** 2) * smooth(0.45 - T.V, 0, 0.05) * smooth(T.V + 0.6, 0, 0.4) * pulso(t, 0.15, 0.7) * 0.6
    fa = faiscas(T, rng, t, 18, 0.6, 0.025, cone=(-math.pi + 0.4, -0.4), cy=0.45, inicio=0.2)
    G += (circ + sil * 0.4 + contorno * 1.5 + coluna + fa) * env
    H += (circ * 0.4 + contorno * 0.8) * env
    return G, H


def lua_vermelha(T, t, rng):
    """Lua vermelha: o céu escurece, uma lua cheia com o desenho de um olho domina tudo."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0, 0.35), 2)
    env = apaga(t, 0.75, 1)
    r = 0.55 * abre + 0.01
    disco = smooth(r - T.RAD, -0.01, 0.02)
    padrao = (np.abs(np.cos(3 * (T.ANG - t * 1.5))) ** 10) * smooth(T.RAD, r * 0.25, r * 0.3) * smooth(r * 0.7 - T.RAD, 0, 0.02) + T.ring(r * 0.72, 0.012) + T.gauss(0, 0, r * 0.15 + 0.01)
    halo = T.ring(r * 1.15, 0.08) * 0.5
    G += (disco * 0.9 + padrao * disco * 0.9 + halo) * env
    H += (disco * 0.3 - padrao * disco * 0.2).clip(0) * env
    return G, H


def susanoo(T, t, rng):
    """Susanoo: costelas e um braço espectral se erguem em volta do alvo, em chamas frias."""
    G, H = vazio(T)
    sobe = ease_out(rel(t, 0, 0.4), 2)
    env = apaga(t, 0.75, 1)
    costelas = T.zero()
    for k in range(4):
        y = 0.35 - k * 0.18 * sobe
        costelas += T.arc_band(0.45 - k * 0.04, 0.03, math.pi * 1.05, math.pi * 1.95, cy=y + 0.3, squash=1.6)
    coluna = np.exp(-(T.U / 0.04) ** 2) * smooth(0.5 - T.V, 0, 0.05) * smooth(T.V - 0.5 + 0.9 * sobe, 0, 0.1)
    cranio = T.ring(0.17, 0.03, 0, 0.5 - 0.95 * sobe) * janela(t, 0.25, 0.4)
    n = _subindo(T, 651, t, 0.05, 1.2)
    aura = smooth(0.62 - np.hypot(T.U / 0.9, (T.V - 0.05) / 1.1) + 0.08 * n, 0, 0.12) * 0.4 * sobe
    G += (costelas * 1.4 + coluna * 1.2 + cranio * 1.4 + aura * (0.6 + 0.4 * np.clip(n, -1, 1))) * env
    H += (costelas * 0.6 + cranio * 0.5) * env
    return G, H


def asa_negra(T, t, rng):
    """Asa negra: uma asa única se abre e penas escuras caem cortando o ar em volta do alvo."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0, 0.3), 2)
    env = apaga(t, 0.75, 1)
    asa = T.zero()
    for k in range(6):
        a = -1.9 + k * 0.25
        comp = (0.7 - k * 0.05) * abre
        asa += T.polys([(lamina(0.15, -0.1, 0.15 + math.cos(a) * comp, -0.1 + math.sin(a) * comp, 0.07), 1)], 0.006)
    penas = []
    for _ in range(18):
        f = (rng.uniform(0, 1) + t * 0.9) % 1
        x = rng.uniform(-0.8, 0.8) + 0.1 * math.sin(f * 8)
        y = -0.8 + f * 1.5
        a = 0.6 * math.sin(f * 10 + x * 5)
        penas.append((lamina(x - math.cos(a) * 0.07, y - math.sin(a) * 0.07, x + math.cos(a) * 0.07, y + math.sin(a) * 0.07, 0.025), math.sin(math.pi * f) * janela(t, 0.15, 0.35)))
    G += (asa * 1.1 + T.polys(penas, 0.003) * 1.2) * env
    H += asa * 0.3 * env
    return G, H


REGISTRO = [
    ("olho", olho, GRANDE, "olho gigante se abrindo", False),
    ("hipnose", hipnose, GRANDE, "espiral hipnótica", False),
    ("relogio", relogio, GRANDE, "mostrador de relógio", False),
    ("runas", runas, GRANDE, "círculo de runas", False),
    ("sarcofago", sarcofago, GRANDE, "caixa negra fechando", False),
    ("encanto", encanto, GRANDE, "estrelas de encanto", False),
    ("caveira", caveira, GRANDE, "caveira de luz", False),
    ("clones", clones, GRANDE, "silhuetas em leque", False),
    ("teleporte", teleporte, GRANDE, "implode e reaparece", False),
    ("fenda", fenda, GRANDE, "rasgo dimensional", False),
    ("sorte", sorte, GRANDE, "dados rolando", False),
    ("confete", confete, GRANDE, "estouro de festa", False),
    ("confusao", confusao, GRANDE, "interrogações girando", False),
    ("pentagrama", pentagrama, GRANDE, "pentagrama infernal", False),
    ("invocacao", invocacao, GRANDE, "silhueta invocada", False),
    ("lua_vermelha", lua_vermelha, GRANDE, "lua com olho", False),
    ("susanoo", susanoo, GRANDE, "guerreiro espectral", False),
    ("asa_negra", asa_negra, GRANDE, "asa e penas negras", False),
]
