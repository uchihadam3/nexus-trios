"""Projéteis com cara própria: flecha, teia, cartas, facas, foguete, bomba, bala de canhão, laser — e os impactos deles."""
from __future__ import annotations

import math

import numpy as np

from .base import (FAIXA, GRANDE, MEDIA, TAU, _cauda_de_particulas, _subindo, apaga, back, ease_out,
                   faiscas, jagged, janela, lamina, poeira, pulso, rel, smooth, some, vazio)


# ------------------------------------------------------------------ viagens (laço, apontam +x)
def flecha(T, t, rng):
    """Flecha: haste fina, ponta triangular clara e penas atrás, com um risco de ar."""
    G, H = vazio(T)
    vib = 0.008 * math.sin(TAU * t * 4)
    haste = T.lines([(-0.45, vib, 0.42, 0, 1)], 0.018, 0.002)
    ponta = T.polys([([(0.38, -0.06), (0.62, 0), (0.38, 0.06)], 1)], 0.003)
    penas = T.polys([([(-0.45, 0), (-0.32, -0.09), (-0.22, -0.09), (-0.33, 0)], 0.8), ([(-0.45, 0), (-0.32, 0.09), (-0.22, 0.09), (-0.33, 0)], 0.8)], 0.003)
    ar = np.exp(-(T.V / 0.03) ** 2) * smooth(-T.U, 0.4, 0.95) * smooth(T.U + 1, 0, 0.4) * 0.35
    G += haste * 1.3 + ponta * 1.8 + penas + ar + T.gauss(0.55, 0, 0.05) * 1.2
    H += ponta * 1.4 + haste * 0.5
    return G, H


def teia_bola(T, t, rng):
    """Bola de teia em viagem: raios e anéis de fio girando devagar, fiapos atrás."""
    G, H = vazio(T)
    cx, r = 0.25, 0.2
    giro = t * TAU / 8
    segs = [(cx, 0, cx + math.cos(giro + TAU * k / 8) * r, math.sin(giro + TAU * k / 8) * r, 1) for k in range(8)]
    raios = T.lines(segs, 0.012, 0.002)
    aneis = T.ring(r * 0.5, 0.008, cx) + T.ring(r * 0.9, 0.01, cx)
    fiapos = _cauda_de_particulas(T, rng, t, 18, cx - 0.1, -0.9, 0.04, 0.012) + np.exp(-(T.V / 0.012) ** 2) * smooth(-T.U, -cx + 0.1, 0.9) * 0.6
    G += raios * 1.2 + aneis * 1.2 + fiapos
    H += raios * 0.6 + aneis * 0.5
    return G, H


def cartas_voando(T, t, rng):
    """Três cartas girando em leque, cada uma com um brilho de energia na borda."""
    G, H = vazio(T)
    cartas, brilho = [], T.zero()
    for k in range(3):
        cx, cy = 0.35 - k * 0.25, (k - 1) * 0.18
        a = t * TAU + k * 2.1
        w, h = 0.09 * abs(math.cos(a)) + 0.015, 0.13
        cartas.append(([(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy + h), (cx - w, cy + h)], 1 - 0.25 * k))
        brilho += T.gauss(cx, cy, 0.12) * (0.6 - 0.15 * k)
    c = T.polys(cartas, 0.003)
    rastro = _cauda_de_particulas(T, rng, t, 20, 0.0, -0.9, 0.12, 0.014)
    G += c * 1.4 + brilho + rastro * 0.8
    H += c * 0.6 + brilho * 0.4
    return G, H


def facas_voando(T, t, rng):
    """Três facas finas em formação, girando de leve, com riscos atrás."""
    G, H = vazio(T)
    lam, segs = [], []
    for k in range(3):
        cx, cy = 0.4 - abs(k - 1) * 0.18, (k - 1) * 0.2
        a = 0.06 * math.sin(TAU * t + k)
        dx, dy = math.cos(a), math.sin(a)
        lam.append((lamina(cx - dx * 0.22, cy - dy * 0.22, cx + dx * 0.16, cy + dy * 0.16, 0.035), 1))
        segs.append((cx - 0.75, cy, cx - 0.25, cy, 0.5))
    lam_ = T.polys(lam, 0.002)
    G += lam_ * 1.6 + T.tapered(segs, 0.02) * 0.8
    H += lam_ * 1.1
    return G, H


def foguete(T, t, rng):
    """Foguete grande: corpo com aletas, chama longa tremendo e fumaça grossa enrolando atrás."""
    G, H = vazio(T)
    corpo = T.polys([([(0.05, -0.08), (0.45, -0.07), (0.62, 0), (0.45, 0.07), (0.05, 0.08)], 1),
                     ([(0.05, -0.08), (-0.06, -0.17), (0.12, -0.08)], 0.8), ([(0.05, 0.08), (-0.06, 0.17), (0.12, 0.08)], 0.8)], 0.004)
    chama_l = 0.35 + 0.08 * math.sin(TAU * t * 6)
    chama = T.polys([([(0.05, -0.06), (0.05 - chama_l, 0), (0.05, 0.06)], 1)], 0.02)
    fumo = _cauda_de_particulas(T, rng, t, 40, -0.2, -1.0, 0.07, 0.06, 1.0)
    G += corpo * 1.4 + T.glow(chama, 1.5, 1.3, 0.03) + fumo * 0.7 + T.gauss(0.03, 0, 0.1) * 1.4
    H += chama * 1.5 + corpo * 0.3 + T.gauss(0.03, 0, 0.06) * 1.5
    return G, H


def bomba(T, t, rng):
    """Bomba redonda girando com o pavio aceso soltando faíscas."""
    G, H = vazio(T)
    cx, cy = 0.2, 0.05 * math.sin(TAU * t)
    bola = T.gauss(cx, cy, 0.17) * 1.1 + T.ring(0.18, 0.02, cx, cy) * 0.9
    brilho = T.gauss(cx - 0.06, cy - 0.07, 0.05) * 0.8
    a = t * TAU
    px, py = cx + 0.12 + 0.03 * math.cos(a), cy - 0.2 + 0.03 * math.sin(a)
    pavio = T.lines([(cx + 0.06, cy - 0.15, px, py, 1)], 0.014, 0.002)
    sub = np.random.default_rng(int(t * 997) + 13)
    fagulha = (T.flare(px, py, 0.5, sub.uniform(0, 3)) * 1.6 + T.gauss(px, py, 0.035) * 2)
    for _ in range(6):
        b = sub.uniform(0, TAU)
        fagulha += T.gauss(px + math.cos(b) * sub.uniform(0.03, 0.1), py + math.sin(b) * sub.uniform(0.03, 0.1), 0.012) * 0.8
    G += bola + brilho + pavio + fagulha
    H += brilho + fagulha * 1.1
    return G, H


def bala_de_canhao(T, t, rng):
    """Bala de canhão: esfera pesada com borrão de movimento e ar rasgado atrás."""
    G, H = vazio(T)
    bola = T.gauss(0.25, 0, 0.15) * 1.2 + T.ring(0.16, 0.025, 0.25) * 0.9
    borrao = np.exp(-(T.V / 0.13) ** 2) * smooth(-T.U, -0.25, 0.6) * smooth(T.U + 0.9, 0, 0.6) * 0.6
    linhas = np.exp(-((np.abs(T.V) - 0.16) / 0.012) ** 2) * smooth(-T.U, -0.1, 0.8) * smooth(T.U + 1, 0, 0.5) * (0.6 + 0.4 * np.sin(T.U * 20 + t * TAU * 2))
    G += bola + borrao + linhas * 0.9
    H += T.gauss(0.2, -0.05, 0.06) * 0.9
    return G, H


def bola_ki(T, t, rng):
    """Bola de ki (Hadouken): esfera com aura em chamas ondulando para trás."""
    G, H = vazio(T)
    cx = 0.25
    n = np.roll(T.noise(np.random.default_rng(131), 0.05, 3), int(t * T.W), axis=1)
    al = (T.U - cx)
    aura = np.exp(-((T.V / (0.17 + 0.25 * np.clip(-al, 0, 1) * 0.6)) ** 2)) * smooth(-al, -0.22, 0.05) * smooth(al + 0.85, 0, 0.6)
    aura = aura * (0.6 + 0.4 * np.clip(n * 0.6 + 0.5, 0, 1))
    nucleo = T.gauss(cx, 0, 0.11) * 2.2
    casca = T.ring(0.17, 0.03, cx) * 1.1
    G += aura * 1.4 + nucleo + casca
    H += nucleo * 1.1 + aura * 0.3
    return G, H


def carga_ki(T, t, rng):
    """Preparo de ki: esfera crescendo com arcos elétricos estalando e poeira sendo puxada (laço)."""
    G, H = vazio(T)
    pulsa = 1 + 0.06 * math.sin(TAU * t * 3)
    nucleo = T.gauss(0, 0, 0.13 * pulsa) * 2.4 + T.ring(0.2 * pulsa, 0.03) * 1.2
    sub = np.random.default_rng(int(t * 12) + 141)
    arcos = T.zero()
    for _ in range(3):
        a = sub.uniform(0, TAU)
        b = a + sub.uniform(0.6, 1.4)
        pts = jagged(sub, math.cos(a) * 0.22, math.sin(a) * 0.22, math.cos(b) * 0.24, math.sin(b) * 0.24, 4, 0.5)
        arcos += T.polyline(pts, 0.012, 1)
    puxa = []
    for _ in range(26):
        f = (rng.uniform(0, 1) + t) % 1
        a = rng.uniform(0, TAU)
        d = 0.85 - 0.6 * f
        puxa.append((math.cos(a) * d, math.sin(a) * d, f * rng.uniform(0.4, 1)))
    G += nucleo + T.glow(arcos, 1.3, 1.4, 0.02) + T.splats(puxa, 0.012)
    H += nucleo * 1.1 + arcos
    return G, H


# ------------------------------------------------------------------ faixas
def laser(T, t, rng):
    """Laser: linha reta e fina, núcleo branco tremendo e um halo estreito (faixa)."""
    G, H = vazio(T)
    sub = np.random.default_rng(int(t * 997) + 151)
    larg = 0.01 * (1 + 0.25 * sub.uniform(-1, 1))
    perfil = np.exp(-(T.V / larg) ** 2)
    halo = np.exp(-(T.V / 0.05) ** 2) * 0.5
    ponta = smooth(T.U, -0.99, -0.94) * smooth(-T.U, -0.99, -0.96)
    G += (perfil * 2.2 + halo) * ponta
    H += perfil * 2 * ponta
    return G, H


def feixe_ki(T, t, rng):
    """Feixe de ki: coluna grossa com faixas em hélice e estalos de energia na borda (faixa)."""
    G, H = vazio(T)
    n = np.roll(T.noise(np.random.default_rng(161), 0.03, 3), int(t * T.W), axis=1)
    larg = 0.055 * (1 + 0.1 * n)
    perfil = np.exp(-np.abs(T.V / larg) ** 2.6)
    halo = np.exp(-(T.V / (larg * 2.2)) ** 2)
    helice = T.zero()
    for k in range(3):
        fase = T.U * 10 - t * TAU * 3 + k * TAU / 3
        y = 0.065 * np.sin(fase)
        helice += np.exp(-((T.V - y) / 0.01) ** 2) * (0.5 + 0.5 * np.cos(fase))
    estalos = np.exp(-((np.abs(T.V) - larg * 1.4) / 0.008) ** 2) * np.clip(n, 0, None)
    ponta = smooth(T.U, -0.99, -0.88) * smooth(-T.U, -0.99, -0.94)
    G += (perfil * 2.2 + halo * 1.1 + helice * 0.9 + estalos) * ponta
    H += (np.clip(perfil * 1.7 - 0.2, 0, None) + helice * 0.6) * ponta
    return G, H


def canhao_de_energia(T, t, rng):
    """Canhão de energia: feixe muito largo com anéis de compressão correndo para o alvo (faixa)."""
    G, H = vazio(T)
    larg = 0.08
    perfil = np.exp(-np.abs(T.V / larg) ** 3)
    nucleo = np.exp(-(T.V / (larg * 0.45)) ** 2)
    aneis = T.zero()
    for k in range(5):
        x = -1 + ((t + k / 5) % 1) * 2
        aneis += np.exp(-((T.U - x) / 0.012) ** 2) * smooth(-np.abs(T.V), -larg * 1.6, -larg * 0.9) * 0.9
    ponta = smooth(T.U, -0.99, -0.9) * smooth(-T.U, -0.99, -0.95)
    G += (perfil * 1.6 + nucleo * 1.2 + aneis) * ponta
    H += (nucleo * 1.6 + aneis * 0.5) * ponta
    return G, H


# ------------------------------------------------------------------ impactos
def cravar(T, t, rng):
    """Cravar: um baque seco, a haste tremendo no alvo e lascas para trás."""
    G, H = vazio(T)
    treme = 0.03 * math.sin(t * 70) * (1 - t)
    haste = T.lines([(-0.55, treme, 0, 0, 1)], 0.02, 0.002) * apaga(t, 0.5, 0.9)
    baque = T.gauss(0, 0, 0.08) * some(t, 0, 0.3) * 3 + T.ring(0.06 + 0.35 * ease_out(t, 2.5), 0.015) * (1 - t) ** 1.6 * 1.4
    fa = faiscas(T, rng, t, 14, 0.5, 0.025, cone=(math.pi - 0.8, math.pi + 0.8), gravidade=0.3)
    G += haste * 1.2 + baque + T.glow(fa, 1, 1, 0.02)
    H += haste * 0.5 + baque + fa * 0.6
    return G, H


def tiro_preciso(T, t, rng):
    """Tiro de precisão: a mira trava num ponto, estala, e um furo de luz estoura."""
    G, H = vazio(T)
    fecha = ease_out(rel(t, 0, 0.25), 2.5)
    r = 0.6 - 0.35 * fecha
    mira = T.ring(r, 0.012) * apaga(t, 0.3, 0.6) * 1.3
    marcas = T.lines([(r + 0.08, 0, r - 0.05, 0, 1), (-r - 0.08, 0, -r + 0.05, 0, 1), (0, r + 0.08, 0, r - 0.05, 1), (0, -r - 0.08, 0, -r + 0.05, 1)], 0.014, 0.002) * apaga(t, 0.3, 0.6)
    tt = rel(t, 0.28, 1)
    furo = (T.gauss(0, 0, 0.05) * 3 + T.flare(0, 0, 1.2, 0.785)) * some(t, 0.28, 0.6) * 1.5
    anel = T.ring(0.05 + 0.4 * ease_out(tt, 3), 0.012) * (1 - tt) ** 1.5 * 1.5 * (t > 0.28)
    fa = faiscas(T, rng, t, 16, 0.6, 0.025, inicio=0.28)
    G += mira + marcas + furo + anel + T.glow(fa, 1, 1, 0.02)
    H += marcas * 0.6 + furo + fa * 0.6
    return G, H


def espingarda(T, t, rng):
    """Espingarda: nove impactos pequenos espalhados num cone, quase juntos, e fumaça."""
    G, H = vazio(T)
    sub = np.random.default_rng(171)
    acc = T.zero()
    for k in range(9):
        x, y = sub.uniform(-0.45, 0.45), sub.uniform(-0.4, 0.4)
        a0 = sub.uniform(0, 0.08)
        acc += (T.gauss(x, y, 0.05) * 2.2 + T.ring(0.04 + 0.12 * ease_out(rel(t, a0, 0.5), 2), 0.01, x, y)) * some(t, a0, 0.55)
    fumo = poeira(T, rng, t, 22, 0, 0, 0.6, 0.15, 0.04, inicio=0.1)
    G += acc * 1.2 + fumo * 0.6
    H += acc * 0.8
    return G, H


def teia_rede(T, t, rng):
    """Rede de teia: os fios se abrem do centro e prendem o alvo numa rede de anéis poligonais."""
    G, H = vazio(T)
    abre = back(rel(t, 0, 0.3), 1.2)
    env = apaga(t, 0.75, 1)
    n = 10
    segs = []
    for k in range(n):
        a = TAU * k / n + 0.15
        segs.append((0, 0, math.cos(a) * 0.8 * abre, math.sin(a) * 0.8 * abre, 1))
    for r in (0.2, 0.38, 0.56, 0.74):
        rr = r * abre
        for k in range(n):
            a1, a2 = TAU * k / n + 0.15, TAU * (k + 1) / n + 0.15
            # o fio cede um pouco no meio
            m = (a1 + a2) / 2
            segs.append((math.cos(a1) * rr, math.sin(a1) * rr, math.cos(m) * rr * 0.93, math.sin(m) * rr * 0.93, 0.8))
            segs.append((math.cos(m) * rr * 0.93, math.sin(m) * rr * 0.93, math.cos(a2) * rr, math.sin(a2) * rr, 0.8))
    rede = T.lines(segs, 0.01, 0.002) * env
    splat = T.gauss(0, 0, 0.12) * some(t, 0, 0.35) * 2.2
    G += T.glow(rede, 1.2, 0.8, 0.015) + splat
    H += rede * 0.6 + splat
    return G, H


def bolhas(T, t, rng):
    """Bolhas: dezenas de bolhas de tamanhos diferentes sobem, brilham na borda e estouram."""
    G, H = vazio(T)
    acc, estouros = T.zero(), T.zero()
    sub = np.random.default_rng(181)
    for _ in range(16):
        x0, r = sub.uniform(-0.55, 0.55), sub.uniform(0.04, 0.12)
        nasce, morre = sub.uniform(0, 0.3), sub.uniform(0.45, 0.95)
        if t < nasce:
            continue
        u = rel(t, nasce, morre)
        y = 0.45 - 0.9 * u
        x = x0 + 0.05 * math.sin(u * 8 + x0 * 10)
        if t < morre:
            acc += T.ring(r, 0.012, x, y) + T.gauss(x - r * 0.4, y - r * 0.4, r * 0.18) * 0.8
        else:
            e = rel(t, morre, morre + 0.15)
            estouros += T.ring(r * (1 + e), 0.008, x, y) * (1 - e) * 1.2
    G += acc * 1.3 + estouros
    H += acc * 0.4 + estouros * 0.5
    return G, H


def cartas_explosivas(T, t, rng):
    """Cartas explosivas: as cartas se espalham girando e cada uma estoura num clarão."""
    G, H = vazio(T)
    sub = np.random.default_rng(191)
    cartas, est = [], T.zero()
    for k in range(6):
        a = sub.uniform(0, TAU)
        d = 0.15 + 0.45 * ease_out(rel(t, 0, 0.35), 2)
        cx, cy = math.cos(a) * d, math.sin(a) * d
        g = t * 9 + k
        w, h = 0.05 * abs(math.cos(g)) + 0.01, 0.08
        if t < 0.4 + k * 0.04:
            cartas.append(([(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy + h), (cx - w, cy + h)], 1))
        est += (T.gauss(cx, cy, 0.04 + 0.04 * rel(t, 0.4 + k * 0.04, 0.8)) * 2.4 + T.ring(0.04 + 0.14 * rel(t, 0.4 + k * 0.04, 0.8), 0.012, cx, cy) * 1.3) * pulso(t, 0.4 + k * 0.04, 0.85 + k * 0.02)
    G += T.polys(cartas, 0.003) * 1.4 + est
    H += T.polys(cartas, 0.003) * 0.5 + est * 0.9
    return G, H


def explosao_grande(T, t, rng):
    """Explosão grande: bola de fogo que sobe em cogumelo, anel de choque no chão e destroços."""
    G, H = vazio(T)
    tt = ease_out(rel(t, 0, 0.45), 2)
    n = _subindo(T, 201, t, 0.06, 0.6)
    bola = smooth(-np.hypot(T.U * 0.9, T.V + 0.15 * t) + (0.2 + 0.42 * tt) + 0.06 * n, -0.05, 0.08)
    haste = smooth(-np.abs(T.U) + 0.12 + 0.03 * n, -0.03, 0.05) * smooth(T.V + 0.1, 0, 0.1) * smooth(0.5 - T.V, 0, 0.1) * janela(t, 0.25, 0.45)
    calor = bola * (1 - rel(t, 0.3, 1)) ** 1.2
    anel = T.ring(0.2 + 0.8 * ease_out(rel(t, 0.05, 1), 2), 0.04, cy=0.45, squash=3.2) * (1 - t) ** 1.2 * 1.5
    fa = faiscas(T, rng, t, 30, 1.0, 0.04, gravidade=0.5)
    flash = T.gauss(0, 0, 0.35) * some(t, 0, 0.2) * 3
    G += (bola * (0.8 + 0.3 * n) + haste * 0.8) * apaga(t, 0.45, 0.95) + anel + T.glow(fa, 1, 1.2, 0.02) + flash
    H += calor * 1.4 + flash + fa * 0.7
    return G, H


def explosao_cartoon(T, t, rng):
    """Explosão de desenho: bolotas de fumaça redondas saltam em volta de um clarão e murcham em puff."""
    G, H = vazio(T)
    sub = np.random.default_rng(211)
    cresce = max(0.05, back(rel(t, 0, 0.3), 1.5))
    murcha = 1 - 0.75 * ease_out(rel(t, 0.5, 1), 2)
    bolas, bordas = T.zero(), T.zero()
    for k in range(8):
        a = TAU * k / 8 + sub.uniform(-0.25, 0.25)
        d = sub.uniform(0.28, 0.5) * cresce
        r = sub.uniform(0.11, 0.17) * cresce * murcha
        x, y = math.cos(a) * d, math.sin(a) * d * 0.85 - 0.15 * rel(t, 0.3, 1)
        c = smooth(r - np.hypot(T.U - x, T.V - y), -0.01, 0.01)
        bolas = np.maximum(bolas, c)
        bordas += np.exp(-((np.hypot(T.U - x, T.V - y) - r) / 0.012) ** 2)
    centro = smooth(0.24 * cresce * murcha - T.RAD, -0.01, 0.01)
    flash = T.gauss(0, 0, 0.22) * some(t, 0, 0.35) * 3
    env = apaga(t, 0.6, 1)
    G += (bolas * 0.55 + bordas * 1.3 + centro * 0.8) * env + flash
    H += (bordas * 0.4 + centro * 0.6) * env + flash
    return G, H


def gas(T, t, rng):
    """Nuvem de gás: massa rolando e se espalhando, redemoinhos internos que demoram a sumir."""
    G, H = vazio(T)
    cresce = ease_out(rel(t, 0, 0.5), 2)
    n = T.noise(np.random.default_rng(221), 0.06, 3)
    gira = T.warp(n, np.sin(T.V * 4 + t * 3) * 0.06, np.cos(T.U * 4 + t * 3) * 0.06)
    massa = smooth(-T.RAD + 0.25 + 0.5 * cresce + 0.12 * gira, -0.05, 0.12)
    redemo = np.exp(-((np.mod(T.ANG + T.RAD * 6 - t * 4, TAU / 3) - 0.6) / 0.25) ** 2) * massa * 0.5
    env = apaga(t, 0.65, 1)
    G += (massa * (0.6 + 0.3 * np.clip(gira, -1, 1)) + redemo) * env
    H += redemo * 0.3 * env
    return G, H


def queimadura(T, t, rng):
    """Queimadura de laser: ponto incandescente, brilho que pulsa e fiapos de fumaça subindo."""
    G, H = vazio(T)
    ponto = T.gauss(0, 0, 0.06) * (2.2 + 0.6 * math.sin(t * 40)) * apaga(t, 0.6, 1)
    halo = T.gauss(0, 0, 0.2) * some(t, 0, 0.5) * 1.2
    fumo = []
    for _ in range(14):
        f = (rng.uniform(0, 1) + t) % 1
        fumo.append((0.05 * math.sin(f * 9 + rng.uniform(0, 6)), -f * 0.7, (1 - f) * rng.uniform(0.3, 0.8) * janela(t, 0.1, 0.3)))
    fa = faiscas(T, rng, t, 10, 0.4, 0.02, gravidade=0.3)
    G += ponto + halo + T.splats(fumo, 0.03) * 0.8 + fa
    H += ponto * 1.1 + halo * 0.5
    return G, H


REGISTRO = [
    ("flecha", flecha, MEDIA, "flecha em viagem (+x)", True),
    ("teia_bola", teia_bola, MEDIA, "bola de teia em viagem (+x)", True),
    ("cartas_voando", cartas_voando, MEDIA, "cartas girando em viagem (+x)", True),
    ("facas_voando", facas_voando, MEDIA, "facas em viagem (+x)", True),
    ("foguete", foguete, MEDIA, "foguete em viagem (+x)", True),
    ("bomba", bomba, MEDIA, "bomba com pavio em viagem (+x)", True),
    ("bala_de_canhao", bala_de_canhao, MEDIA, "bala de canhão em viagem (+x)", True),
    ("bola_ki", bola_ki, MEDIA, "bola de ki em viagem (+x)", True),
    ("carga_ki", carga_ki, MEDIA, "preparo: ki estalando", True),
    ("laser", laser, FAIXA, "laser fino (faixa)", True),
    ("feixe_ki", feixe_ki, FAIXA, "feixe de ki com hélice (faixa)", True),
    ("canhao_de_energia", canhao_de_energia, FAIXA, "canhão de energia (faixa)", True),
    ("cravar", cravar, GRANDE, "flecha cravando", False),
    ("tiro_preciso", tiro_preciso, GRANDE, "mira travando e tiro", False),
    ("espingarda", espingarda, GRANDE, "nove impactos espalhados", False),
    ("teia_rede", teia_rede, GRANDE, "rede de teia", False),
    ("bolhas", bolhas, GRANDE, "bolhas subindo e estourando", False),
    ("cartas_explosivas", cartas_explosivas, GRANDE, "cartas que estouram", False),
    ("explosao_grande", explosao_grande, GRANDE, "explosão em cogumelo", False),
    ("explosao_cartoon", explosao_cartoon, GRANDE, "explosão de desenho animado", False),
    ("gas", gas, GRANDE, "nuvem de gás", False),
    ("queimadura", queimadura, GRANDE, "ponto queimando", False),
]
