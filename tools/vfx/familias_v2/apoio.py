"""Apoio e Status: curas, escudos com cara própria, gritos de guerra e os debuffs que se enxergam."""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, TAU, _subindo, apaga, back, ease_in, ease_out, estrela, faiscas, girado, jagged, janela, lamina,
                   poeira, pulso, rel, smooth, some, vazio)


def _cruz(cx, cy, s, w=0.32):
    a, b = s, s * w
    return [(cx - b, cy - a), (cx + b, cy - a), (cx + b, cy - b), (cx + a, cy - b), (cx + a, cy + b), (cx + b, cy + b),
            (cx + b, cy + a), (cx - b, cy + a), (cx - b, cy + b), (cx - a, cy + b), (cx - a, cy - b), (cx - b, cy - b)]


def cura_em_area(T, t, rng):
    """Cura em área: um anel verde se espalha no chão e cruzes de luz sobem em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.7, 1)
    abre = ease_out(rel(t, 0, 0.35), 2)
    anel = T.ring(0.75 * abre, 0.04, cy=0.45, squash=3.5) * 1.4 + T.ring(0.55 * abre, 0.015, cy=0.45, squash=3.5)
    cruzes = []
    sub = np.random.default_rng(701)
    for k in range(7):
        x = sub.uniform(-0.6, 0.6)
        a0 = sub.uniform(0, 0.4)
        u = rel(t, a0, a0 + 0.55)
        cruzes.append((_cruz(x, 0.4 - 0.9 * u, 0.06 * math.sin(math.pi * u) + 0.005), math.sin(math.pi * u)))
    c = T.polys(cruzes, 0.004)
    brilho = T.gauss(0, 0.45, 0.4, 0.1) * pulso(t, 0.1, 0.6) * 0.8
    G += (anel + T.glow(c, 1.3, 1, 0.02) + brilho) * env
    H += (anel * 0.4 + c * 0.9) * env
    return G, H


def regeneracao(T, t, rng):
    """Regeneração: folhas e pontos verdes sobem em espiral lenta em volta do corpo."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.75, 1)
    folhas = []
    for k in range(12):
        f = (k / 12 + t * 0.8) % 1
        a = f * TAU * 1.5 + k
        x, y = math.cos(a) * 0.38, 0.5 - f * 1.1
        ang = a + math.pi / 2
        folhas.append((lamina(x - math.cos(ang) * 0.05, y - math.sin(ang) * 0.05, x + math.cos(ang) * 0.05, y + math.sin(ang) * 0.05, 0.025), math.sin(math.pi * f) * (0.5 + 0.5 * (math.sin(a) > 0))))
    pts = []
    for _ in range(30):
        f = (rng.uniform(0, 1) + t * 0.7) % 1
        pts.append((rng.uniform(-0.3, 0.3), 0.45 - f * 1.0, math.sin(math.pi * f) * rng.uniform(0.3, 1)))
    G += (T.polys(folhas, 0.003) * 1.4 + T.splats(pts, 0.01) + T.gauss(0, 0.05, 0.22, 0.4) * 0.3) * env
    H += (T.polys(folhas, 0.003) * 0.5 + T.splats(pts, 0.008) * 0.6) * env
    return G, H


def grito_de_guerra(T, t, rng):
    """Grito de guerra: um estandarte de raios se abre, divisas sobem e o aliado brilha."""
    G, H = vazio(T)
    env = apaga(t, 0.7, 1)
    abre = back(rel(t, 0, 0.3), 1.4)
    raios = (np.abs(np.cos(T.ANG * 7)) ** 16) * np.exp(-(T.RAD / (0.5 * abre + 0.01)) ** 2) * smooth(T.RAD, 0.1, 0.2) * 1.3
    divisas = []
    for k in range(4):
        u = ((t * 1.3 + k / 4) % 1)
        y = 0.4 - u * 1.0
        divisas.append(([(-0.18, y + 0.08), (0, y - 0.04), (0.18, y + 0.08), (0.18, y + 0.14), (0, y + 0.02), (-0.18, y + 0.14)], math.sin(math.pi * u)))
    d = T.polys(divisas, 0.003)
    flash = T.gauss(0, 0, 0.18) * pulso(t, 0, 0.35) * 2.2
    G += (raios + d * 1.4 + flash) * env
    H += (raios * 0.4 + d * 0.9 + flash) * env
    return G, H


def velocidade(T, t, rng):
    """Velocidade: linhas de vento passam rápido pelo corpo, duas asinhas de luz batem."""
    G, H = vazio(T)
    env = janela(t, 0, 0.12) * apaga(t, 0.75, 1)
    linhas = []
    sub = np.random.default_rng(711)
    for k in range(12):
        y = sub.uniform(-0.6, 0.5)
        x = 0.9 - ((t * 2.5 + sub.uniform(0, 1)) % 1) * 2
        linhas.append((x + 0.4, y, x, y, sub.uniform(0.4, 1)))
    l = T.tapered(linhas, 0.018)
    bate = 0.25 * math.sin(t * TAU * 4)
    asas = T.zero()
    for lado in (-1, 1):
        for k in range(3):
            a = -math.pi / 2 - lado * (0.5 + k * 0.3 + bate)
            asas += T.polys([(lamina(lado * 0.15, -0.15, lado * 0.15 + math.cos(a) * (0.32 - k * 0.06), -0.15 + math.sin(a) * (0.32 - k * 0.06), 0.035), 1)], 0.004)
    G += (l * 1.2 + asas * 1.2) * env
    H += (l * 0.5 + asas * 0.6) * env
    return G, H


def escudo_tech(T, t, rng):
    """Escudo tecnológico: painéis hexagonais se encaixam um a um formando uma parede plana com varredura."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    s = 0.13
    paineis, bordas = [], []
    k = 0
    for i in range(-2, 3):
        for j in range(-3, 4):
            cx = j * s * 1.5
            cy = i * s * math.sqrt(3) + (j % 2) * s * math.sqrt(3) / 2
            if abs(cx) > 0.55 or abs(cy) > 0.62:
                continue
            u = back(rel(t, 0.03 * k % 0.35, 0.03 * k % 0.35 + 0.15), 1.3)
            k += 7
            hexa = [(cx + math.cos(TAU * m / 6) * s * 0.92 * u, cy + math.sin(TAU * m / 6) * s * 0.92 * u) for m in range(6)]
            paineis.append((hexa, 0.5))
            bordas.append(hexa + [hexa[0]])
    p = T.polys(paineis, 0.003)
    b = sum(T.polyline(h, 0.008, 1) for h in bordas)
    varre = np.exp(-((T.V - (-0.7 + 1.4 * ((t * 1.5) % 1))) / 0.04) ** 2) * smooth(0.6 - np.abs(T.U), 0, 0.05) * janela(t, 0.3, 0.4)
    G += (p * 0.6 + b * 1.2 + varre * 0.8 * (p > 0.1)) * env
    H += (b * 0.6 + varre * 0.4 * (p > 0.1)) * env
    return G, H


def barreira_magica(T, t, rng):
    """Barreira mágica: uma cúpula de runas gira em volta do aliado e pulsa quando fecha."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    abre = ease_out(rel(t, 0, 0.3), 2.5)
    r = 0.65 * abre + 0.01
    domo = smooth(r - T.RAD, -0.01, 0.03) * (0.15 + 0.6 * smooth(T.RAD, r * 0.6, r))
    borda = T.ring(r, 0.02) * 1.5
    runas = (np.abs(np.cos(T.ANG * 12 + t * 3)) ** 30) * np.exp(-((T.RAD - r * 0.86) / 0.025) ** 2) * 1.4
    pulsa = T.ring(r * (1 + 0.15 * rel(t, 0.3, 0.6)), 0.03) * pulso(t, 0.3, 0.6) * 1.3
    G += (domo + borda + runas + pulsa) * env
    H += (borda * 0.6 + runas * 0.8) * env
    return G, H


def escudo_fisico(T, t, rng):
    """Escudo de mão: um brasão grande aparece na frente, o golpe bate e faíscas desviam."""
    G, H = vazio(T)
    env = apaga(t, 0.65, 1)
    s = back(rel(t, 0, 0.2), 1.6)
    pts = [(-0.38 * s, -0.42 * s), (0.38 * s, -0.42 * s), (0.36 * s, 0.05 * s), (0, 0.48 * s), (-0.36 * s, 0.05 * s)]
    corpo = T.polys([(pts, 1)], 0.004)
    borda = T.polyline(pts + [pts[0]], 0.025, 1)
    emblema = T.polys([(estrela(0, -0.02 * s, 0.16 * s, -math.pi / 2, 5, 0.45), 1)], 0.003)
    tt = rel(t, 0.25, 1)
    choque = (T.flare(0, -0.05, 1.4, 0.7) * 2 + T.gauss(0, -0.05, 0.08) * 2) * some(t, 0.25, 0.55)
    fa = faiscas(T, rng, t, 18, 0.8, 0.03, cone=(-2.6, -0.5), gravidade=0.3, inicio=0.25)
    G += (corpo * 0.35 + borda * 1.5 + emblema * 0.9) * env + choque + fa
    H += (borda * 0.7 + emblema * 0.5) * env + choque + fa * 0.6
    return G, H


def armadura(T, t, rng):
    """Armadura: placas de metal fecham sobre o corpo de baixo para cima, com um reflexo correndo."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    placas, bordas = [], T.zero()
    for k in range(5):
        y = 0.45 - k * 0.2
        u = back(rel(t, k * 0.06, k * 0.06 + 0.2), 1.4)
        w = (0.34 - abs(k - 2) * 0.03) * u
        pl = [(-w, y), (w, y), (w * 0.92, y - 0.17), (-w * 0.92, y - 0.17)]
        placas.append((pl, 0.6))
        bordas += T.polyline(pl + [pl[0]], 0.012, 1)
    p = T.polys(placas, 0.003)
    reflexo = np.exp(-((T.U + T.V * 0.4 - (-0.8 + 1.6 * rel(t, 0.4, 0.7))) / 0.05) ** 2) * (p > 0.1) * 1.2
    G += (p * 0.5 + bordas * 1.3 + reflexo) * env
    H += (bordas * 0.6 + reflexo) * env
    return G, H


def resgate(T, t, rng):
    """Resgate: um rastro curvo mergulha até o aliado, o pega e sobe num brilho protetor."""
    G, H = vazio(T)
    p = ease_out(rel(t, 0, 0.35), 2)
    pts = []
    for k in range(40):
        u = k / 39 * p
        a = math.pi * 1.1 + u * math.pi * 0.9
        pts.append((math.cos(a) * 0.6, -0.1 + math.sin(a) * -0.5 + 0.4))
    rastro = T.polyline(pts, 0.03, 1) * apaga(t, 0.4, 0.8)
    pega = (T.ring(0.25 + 0.15 * rel(t, 0.35, 0.7), 0.025) + T.gauss(0, 0, 0.18) * 0.6) * pulso(t, 0.3, 0.85) * 1.4
    est = T.polys([(estrela(math.cos(a) * 0.35, math.sin(a) * 0.35, 0.05, a, 4, 0.35), 1) for a in (t * 4 + k * TAU / 4 for k in range(4))], 0.003) * pulso(t, 0.35, 0.9)
    G += T.glow(rastro, 1.2, 1, 0.02) + pega + est * 1.2
    H += rastro * 0.6 + pega * 0.4 + est * 0.6
    return G, H


def bencao(T, t, rng):
    """Bênção: penas de luz caem devagar do alto e um halo dourado se acende sobre o aliado."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    penas = []
    sub = np.random.default_rng(721)
    for k in range(12):
        f = rel(t, sub.uniform(0, 0.3), 1)
        x = sub.uniform(-0.6, 0.6) + 0.12 * math.sin(f * 6 + k)
        y = -0.9 + f * 1.3
        a = 0.6 * math.sin(f * 8 + k)
        penas.append((lamina(x - math.cos(a) * 0.08, y - math.sin(a) * 0.08, x + math.cos(a) * 0.08, y + math.sin(a) * 0.08, 0.03), math.sin(math.pi * f)))
    halo = T.ring(0.22, 0.02, cy=-0.55, squash=3.5) * janela(t, 0.15, 0.35) * 1.5
    luz = T.gauss(0, -0.1, 0.25, 0.5) * pulso(t, 0.1, 0.8) * 0.6
    G += (T.polys(penas, 0.004) * 1.3 + halo + luz) * env
    H += (T.polys(penas, 0.004) * 0.7 + halo * 0.7) * env
    return G, H


def lanche(T, t, rng):
    """Lanche: uma mordida de luz, migalhas pulando, vapor quentinho e um coraçãozinho subindo."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    mordida = T.ring(0.2, 0.05) * (1 - smooth(T.U + 0.05, 0, 0.1) * smooth(T.V - 0.05, -0.2, 0.2) * 0) * pulso(t, 0, 0.35) * 1.4
    migalhas = faiscas(T, rng, t, 14, 0.5, 0.03, cone=(-math.pi + 0.3, -0.3), gravidade=0.6)
    vapor = T.zero()
    for k in range(3):
        x = (k - 1) * 0.15
        pts = [(x + 0.04 * math.sin(v * 12 + t * 8 + k), 0.1 - v * 0.6) for v in np.linspace(0, 1, 20)]
        vapor += T.polyline(pts, 0.015, 1) * pulso(t, 0.1 + 0.05 * k, 0.8)
    u = rel(t, 0.3, 1)
    hx, hy, hs = 0, -0.2 - 0.5 * u, 0.12
    coracao = smooth(1 - (((T.U - hx) / hs) ** 2 + (-(T.V - hy) / hs - np.sqrt(np.abs((T.U - hx) / hs)) * 0.8 + 0.3) ** 2), 0, 0.3) * math.sin(math.pi * u)
    G += (mordida + migalhas + T.blur(vapor, 0.01) * 0.8 + coracao * 1.4) * env
    H += (coracao * 0.8 + migalhas * 0.5) * env
    return G, H


def purificar(T, t, rng):
    """Purificar: uma onda clara lava o corpo de cima a baixo e brilhos caem limpos."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    y = -0.8 + 1.4 * ease_out(rel(t, 0, 0.6), 1.6)
    onda = np.exp(-((T.V - y) / 0.06) ** 2) * smooth(0.5 - np.abs(T.U), 0, 0.15) * 1.4
    lavado = smooth(y - T.V, 0, 0.3) * smooth(0.45 - np.abs(T.U), 0, 0.15) * 0.25 * (1 - rel(t, 0.6, 1))
    bril = sum(T.flare(rng.uniform(-0.4, 0.4), rng.uniform(-0.6, 0.4), 0.3, 0.4) * pulso((t * 2 + rng.uniform(0, 1)) % 1, 0, 1) for _ in range(8))
    G += (onda + bril) * env
    H += (onda * 0.8 + bril * 0.8) * env
    return G, H


def enfraquecer(T, t, rng):
    """Enfraquecer: setas para baixo caem pelo corpo e uma névoa cinza pesa em volta."""
    G, H = vazio(T)
    env = janela(t, 0, 0.12) * apaga(t, 0.75, 1)
    setas = []
    for k in range(5):
        u = ((t * 1.2 + (0.1, 0.6, 0.3, 0.85, 0.45)[k]) % 1)
        x = (k - 2) * 0.17
        y = -0.5 + u * 1.0
        setas.append(([(x - 0.08, y), (x + 0.08, y), (x + 0.08, y + 0.06), (x + 0.15, y + 0.06), (x, y + 0.18), (x - 0.15, y + 0.06), (x - 0.08, y + 0.06)], math.sin(math.pi * u)))
    s = T.polys(setas, 0.003)
    nevoa = T.gauss(0, 0.2, 0.4, 0.3) * 0.35 * (0.7 + 0.3 * T.noise(np.random.default_rng(731), 0.08, 2))
    G += (s * 1.3 + nevoa) * env
    H += s * 0.5 * env
    return G, H


def lentidao(T, t, rng):
    """Lentidão: uma ampulheta aparece, a areia escorre devagar e ondas preguiçosas se arrastam."""
    G, H = vazio(T)
    env = janela(t, 0, 0.12) * apaga(t, 0.75, 1)
    s = 0.35 * back(rel(t, 0, 0.25), 1.3)
    vidro = [(-s * 0.6, -s), (s * 0.6, -s), (s * 0.05, 0), (s * 0.6, s), (-s * 0.6, s), (-s * 0.05, 0), (-s * 0.6, -s)]
    contorno = T.polyline(vidro, 0.016, 1)
    u = rel(t, 0.15, 1)
    cima = T.polys([([(-s * 0.5 * (1 - u), -s * 0.85 * (1 - u)), (s * 0.5 * (1 - u), -s * 0.85 * (1 - u)), (0, -0.02)], 0.7)], 0.004) if u < 1 else T.zero()
    baixo = T.polys([([(-s * 0.5 * u - 0.01, s * 0.95), (s * 0.5 * u + 0.01, s * 0.95), (0, s * 0.95 - s * 0.6 * u)], 0.7)], 0.004)
    fio = np.exp(-(T.U / 0.008) ** 2) * smooth(T.V, 0, 0.02) * smooth(s * 0.9 - T.V, 0, 0.02)
    ondas = sum(T.ring(0.45 + 0.1 * k + 0.05 * math.sin(t * 3 + k), 0.012) * 0.4 for k in range(3))
    G += (contorno * 1.3 + cima + baixo + fio + ondas) * env
    H += (contorno * 0.6 + fio * 0.5) * env
    return G, H


def marca(T, t, rng):
    """Marca: um alvo de mira carimba sobre o inimigo, gira e trava com um estalo."""
    G, H = vazio(T)
    s = 1.6 - 0.6 * back(rel(t, 0, 0.25), 1.4)
    env = apaga(t, 0.75, 1)
    gira = (1 - ease_out(rel(t, 0, 0.35), 2)) * 2
    aneis = T.ring(0.45 * s, 0.018) + T.ring(0.28 * s, 0.012)
    cantos = []
    for k in range(4):
        a = gira + TAU * k / 4 + math.pi / 4
        r = 0.55 * s
        cantos.append((math.cos(a - 0.25) * r, math.sin(a - 0.25) * r, math.cos(a) * r * 1.08, math.sin(a) * r * 1.08, 1))
        cantos.append((math.cos(a + 0.25) * r, math.sin(a + 0.25) * r, math.cos(a) * r * 1.08, math.sin(a) * r * 1.08, 1))
    c = T.lines(cantos, 0.02, 0.002)
    ponto = T.gauss(0, 0, 0.04) * 2
    trava = T.ring(0.55, 0.02) * pulso(t, 0.3, 0.55) * 1.4
    G += (aneis * 1.3 + c * 1.3 + ponto) * env + trava
    H += (aneis * 0.5 + c * 0.6 + ponto) * env
    return G, H


def silencio(T, t, rng):
    """Silêncio: ondas de som saem da boca e são cortadas por um risco; ficam paradas no ar."""
    G, H = vazio(T)
    env = janela(t, 0, 0.12) * apaga(t, 0.75, 1)
    ondas = sum(T.arc_band(0.18 + 0.12 * k, 0.02, -0.7, 0.7, cx=-0.2) * (1 - 0.2 * k) for k in range(3)) * (1 - 0.6 * janela(t, 0.3, 0.45))
    corte = T.polys([(lamina(-0.45, 0.4, 0.45, -0.4, 0.035, ease_out(rel(t, 0.25, 0.4), 2)), 1)], 0.003)
    aro = T.ring(0.55, 0.025) * janela(t, 0.25, 0.4)
    G += (ondas * 1.2 + corte * 1.5 + aro * 1.3) * env
    H += (corte * 0.9 + aro * 0.5) * env
    return G, H


def medo(T, t, rng):
    """Medo: sombras com olhos se aproximam do alvo, ele treme e uma gota de suor cai."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.75, 1)
    perto = ease_out(rel(t, 0, 0.6), 2)
    olhos = T.zero()
    for k in range(4):
        a = TAU * k / 4 + 0.6
        r = 0.85 - 0.35 * perto
        x, y = math.cos(a) * r, math.sin(a) * r * 0.8
        pisca = 1 if (t * 5 + k) % 1 > 0.1 else 0.1
        olhos += (T.gauss(x - 0.05, y, 0.022) + T.gauss(x + 0.05, y, 0.022)) * pisca
        olhos += T.gauss(x, y + 0.08, 0.12, 0.14) * 0.25
    treme = 0.02 * math.sin(t * 80)
    gota_y = -0.35 + 0.3 * rel(t, 0.3, 0.8)
    gota = T.gauss(0.22 + treme, gota_y, 0.03, 0.045) * pulso(t, 0.3, 0.85) * 1.5
    G += (olhos * 1.8 + gota) * env
    H += olhos * 1.2 * env
    return G, H


def exposto(T, t, rng):
    """Exposto: a guarda do alvo trinca como vidro e os cacos caem, deixando um brilho fraco."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    casca = T.ring(0.42, 0.025) * (1 - rel(t, 0.25, 0.4)) * 1.4
    sub = np.random.default_rng(741)
    rach = T.zero()
    for k in range(8):
        a = TAU * k / 8 + sub.uniform(-0.2, 0.2)
        rach += T.polyline(jagged(sub, 0, 0, math.cos(a) * 0.42, math.sin(a) * 0.42, 3, 0.25), 0.01, 1)
    rach *= janela(t, 0.1, 0.2) * (1 - rel(t, 0.3, 0.45))
    tt = rel(t, 0.3, 1)
    cacos = []
    for k in range(12):
        a = TAU * k / 12 + sub.uniform(-0.2, 0.2)
        x = math.cos(a) * (0.42 + 0.2 * tt)
        y = math.sin(a) * (0.42 + 0.2 * tt) + 0.9 * tt * tt
        s = 0.05
        g = a + tt * 6
        cacos.append(([(x + math.cos(g) * s, y + math.sin(g) * s), (x + math.cos(g + 2.3) * s, y + math.sin(g + 2.3) * s), (x + math.cos(g + 4) * s * 0.7, y + math.sin(g + 4) * s * 0.7)], (1 - tt) * (t > 0.3)))
    G += (casca + rach * 1.4 + T.polys(cacos, 0.003) * 1.3) * env
    H += (rach + casca * 0.4) * env
    return G, H


def estrela_invencivel(T, t, rng):
    """Estrela invencível: uma estrela grande pulsa e solta faíscas em arco-íris girando em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    s = 0.35 * back(rel(t, 0, 0.25), 1.6) * (1 + 0.08 * math.sin(t * 30))
    est = T.polys([(estrela(0, 0, s, -math.pi / 2, 5, 0.45), 1)], 0.004)
    borda = est * (1 - smooth(T.blur(est, 0.015), 0.8, 0.97))
    olhos = (T.gauss(-0.06 * s / 0.35, -0.02, 0.02, 0.04) + T.gauss(0.06 * s / 0.35, -0.02, 0.02, 0.04)) * (s > 0.1)
    fa = []
    for k in range(24):
        a = TAU * k / 24 + t * 6
        r = 0.45 + 0.15 * math.sin(t * 10 + k)
        fa.append((math.cos(a) * r, math.sin(a) * r, 0.5 + 0.5 * math.sin(t * 20 + k)))
    G += (est * 0.9 + borda * 1.3 + T.splats(fa, 0.014) * 1.3) * env
    H += (est * 0.8 + T.splats(fa, 0.01) * 0.6) * env
    G -= olhos * 0.6 * env
    return G, H



def ressurreicao(T, t, rng):
    """Reviver: um feixe de luz desce do alto sobre o aliado caído, um anel se acende no chão,
    penas de luz sobem e uma estrela se abre no instante em que ele se levanta."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    desce = ease_out(rel(t, 0, 0.32), 2)
    topo, chao = -1.05, 0.48
    fundo = topo + (chao - topo) * desce
    larg = 0.16 + 0.07 * pulso(t, 0.3, 0.75) + 0.08 * np.clip((T.V - topo) / (chao - topo), 0, 1) ** 2
    corpo_feixe = smooth(larg - np.abs(T.U), 0, larg * 0.7) * smooth(fundo - T.V, -0.02, 0.08) * smooth(T.V - topo, 0, 0.25)
    gradiente = 0.55 + 0.45 * np.clip((T.V - topo) / (chao - topo), 0, 1)
    feixe = corpo_feixe * gradiente * (1.35 - 0.5 * rel(t, 0.55, 1))
    nucleo = smooth(larg * 0.28 - np.abs(T.U), 0, larg * 0.2) * smooth(fundo - T.V, -0.02, 0.06) * smooth(T.V - topo, 0, 0.3)
    abre = ease_out(rel(t, 0.25, 0.65), 2)
    anel = (T.ring(0.18 + 0.55 * abre, 0.035, cy=chao, squash=3.6) * 1.3 + T.ring(0.1 + 0.35 * abre, 0.012, cy=chao, squash=3.6)) * janela(t, 0.22, 0.3)
    penas = []
    sub = np.random.default_rng(907)
    for k in range(16):
        a0 = sub.uniform(0.25, 0.55)
        f = rel(t, a0, a0 + 0.45)
        x = sub.uniform(-0.45, 0.45) + 0.08 * math.sin(f * 7 + k)
        y = chao - 0.05 - f * 1.25
        a = 0.7 * math.sin(f * 6 + k) + math.pi / 2
        penas.append((lamina(x - math.cos(a) * 0.06, y - math.sin(a) * 0.06, x + math.cos(a) * 0.06, y + math.sin(a) * 0.06, 0.022), math.sin(math.pi * f)))
    estrela_brilho = pulso(t, 0.5, 0.85)
    flare = (T.flare(0, 0.08, 0.75 * estrela_brilho + 0.01, ang=0.0, thin=0.014) + T.flare(0, 0.08, 0.45 * estrela_brilho + 0.01, ang=math.pi / 4, thin=0.01) * 0.6) * estrela_brilho * 2.2
    halo = T.gauss(0, 0.08, 0.26, 0.34) * estrela_brilho * 1.3
    G += (feixe + anel + T.polys(penas, 0.004) * 1.3 + flare + halo) * env
    H += (nucleo * 1.4 + anel * 0.5 + T.polys(penas, 0.004) * 0.6 + flare * 0.9) * env
    return G, H


def _arco(cx, cy, r, a0, a1, w, n=28):
    """Um arco grosso como polígono (borda de fora e de dentro)."""
    fora = [(cx + (r + w / 2) * math.cos(a0 + (a1 - a0) * i / (n - 1)), cy + (r + w / 2) * math.sin(a0 + (a1 - a0) * i / (n - 1))) for i in range(n)]
    dentro = [(cx + (r - w / 2) * math.cos(a1 - (a1 - a0) * i / (n - 1)), cy + (r - w / 2) * math.sin(a1 - (a1 - a0) * i / (n - 1))) for i in range(n)]
    return fora + dentro


def provocar(T, t, rng):
    """Provocar: dois anéis vermelhos se fecham sobre o rival (a atenção dele é puxada), a marca
    de raiva dos desenhos estoura em cima dele tremendo, e riscos de tensão saem em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.72, 1)
    aneis = 0
    for k, a0 in enumerate((0.0, 0.12)):
        f = ease_in(rel(t, a0, a0 + 0.34), 1.5)
        r = 0.95 - 0.7 * f
        aneis = aneis + T.ring(r, 0.03 + 0.025 * f) * pulso(t, a0, a0 + 0.38) * (1.2 - 0.3 * k)
    # a marca de raiva: quatro arcos se encarando, com pop e tremor
    pop = back(rel(t, 0.22, 0.42), 2.2)
    treme = 0.025 * math.sin(t * 90) * janela(t, 0.3, 0.36) * (1 - rel(t, 0.55, 0.8))
    cx, cy, esc = 0.0 + treme, -0.08, 0.36 * pop
    marca = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            ox, oy = cx + sx * 0.86 * esc, cy + sy * 0.86 * esc
            meio = math.atan2(-sy, -sx)
            marca.append((_arco(ox, oy, 0.6 * esc, meio - 0.72, meio + 0.72, 0.3 * esc), 1.0))
    brilho_marca = janela(t, 0.22, 0.28)
    # riscos de tensão: traços curtos que saem em volta, no instante do estouro
    riscos = []
    sai = ease_out(rel(t, 0.32, 0.6), 2)
    for k in range(10):
        a = k / 10 * TAU + 0.3
        r0 = 0.42 + 0.3 * sai
        riscos.append((lamina(cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + (r0 + 0.16) * math.cos(a), cy + (r0 + 0.16) * math.sin(a), 0.03), pulso(t, 0.3, 0.68)))
    halo = T.gauss(cx, cy, 0.3, 0.3) * pulso(t, 0.2, 0.6) * 0.9
    M = T.polys(marca, 0.006) * brilho_marca
    G += (aneis + M * 1.4 + T.polys(riscos, 0.004) * 1.2 + halo) * env
    H += (aneis * 0.45 + M * 0.8 + T.polys(riscos, 0.004) * 0.6) * env
    return G, H


def reflexo(T, t, rng):
    """Refletir: um escudo hexagonal de espelho estoura na frente de quem foi atingido, um brilho
    corre pela face e estilhaços de luz voltam para fora — o golpe foi devolvido."""
    G, H = vazio(T)
    env = apaga(t, 0.6, 1)
    pop = back(rel(t, 0.0, 0.22), 2.0)
    r = 0.62 * pop
    hexa = [(r * math.cos(k * TAU / 6 + math.pi / 6), r * math.sin(k * TAU / 6 + math.pi / 6) - 0.04) for k in range(6)]
    dentro = [(x * 0.84, (y + 0.04) * 0.84 - 0.04) for x, y in hexa]
    borda = T.polys([(hexa, 1.0)], 0.004) - T.polys([(dentro, 1.0)], 0.004)
    face = T.polys([(dentro, 1.0)], 0.01) * 0.28
    # o brilho que atravessa a face na diagonal
    corre = -0.9 + 1.8 * ease_out(rel(t, 0.12, 0.45), 2)
    faixa = smooth(0.09 - np.abs((T.U + T.V) * 0.7 - corre), 0, 0.06) * T.polys([(dentro, 1.0)], 0.01)
    # estilhaços: saem das arestas para fora
    sai = ease_out(rel(t, 0.18, 0.7), 2)
    cacos = []
    for k in range(12):
        a = k / 12 * TAU + 0.26
        d0 = 0.55 + 0.5 * sai
        cacos.append((lamina(d0 * math.cos(a), d0 * math.sin(a) - 0.04, (d0 + 0.13) * math.cos(a), (d0 + 0.13) * math.sin(a) - 0.04, 0.035), pulso(t, 0.16, 0.75)))
    flash = T.gauss(0, -0.04, 0.35, 0.35) * pulso(t, 0.0, 0.3) * 1.2
    G += (borda * 1.5 + face + faixa * 1.6 + T.polys(cacos, 0.004) * 1.2 + flash) * env
    H += (borda * 0.9 + faixa * 1.3 + T.polys(cacos, 0.004) * 0.7 + flash * 0.8) * env
    return G, H


def espinhos(T, t, rng):
    """Espinhos: pontas curvas brotam do corpo em todas as direções num estalo e recolhem —
    quem bateu se feriu nelas."""
    G, H = vazio(T)
    env = apaga(t, 0.55, 1)
    brota = back(rel(t, 0.0, 0.2), 2.6)
    recolhe = 1 - ease_in(rel(t, 0.55, 0.95), 2)
    pontas = []
    sub = np.random.default_rng(311)
    for k in range(16):
        a = k / 16 * TAU + sub.uniform(-0.12, 0.12)
        base = 0.3
        comp = (0.32 + sub.uniform(0, 0.2)) * brota * recolhe
        curva = sub.uniform(-0.25, 0.25)
        bx, by = base * math.cos(a), base * math.sin(a)
        px_, py_ = (base + comp) * math.cos(a + curva * 0.4), (base + comp) * math.sin(a + curva * 0.4)
        larg = 0.055
        n1 = (-math.sin(a) * larg, math.cos(a) * larg)
        pontas.append(([(bx + n1[0], by + n1[1]), (px_, py_), (bx - n1[0], by - n1[1])], 1.0))
    anel = T.ring(0.3, 0.05) * pulso(t, 0.0, 0.5) * 1.1
    estalo = T.gauss(0, 0, 0.28, 0.28) * pulso(t, 0.0, 0.22)
    P = T.polys(pontas, 0.003)
    G += (P * 1.4 + anel + estalo) * env
    H += (P * 0.6 + anel * 0.4 + estalo * 0.9) * env
    return G, H


def vampirismo(T, t, rng):
    """Vampirismo: gotas de sangue giram em espiral para dentro de quem bateu e um pulso de
    coração acende no centro quando a Vida volta."""
    G, H = vazio(T)
    env = apaga(t, 0.7, 1)
    gotas = []
    sub = np.random.default_rng(613)
    for k in range(18):
        a0 = sub.uniform(0, 0.35)
        f = ease_in(rel(t, a0, a0 + 0.5), 1.4)
        ang = k / 18 * TAU + 2.4 * f
        r = 0.92 - 0.82 * f
        x, y = r * math.cos(ang), r * math.sin(ang)
        tam = 0.075 * (1 - 0.45 * f)
        # gota: ponta para trás do movimento
        tx, ty = -math.sin(ang), math.cos(ang)
        vis = (min(1.0, f * 6) * (1 - f) ** 0.5) if 0 < f < 1 else 0.0
        gotas.append(([(x + tx * tam * 2.6, y + ty * tam * 2.6), (x + ty * tam, y - tx * tam), (x - tx * tam * 0.9, y - ty * tam * 0.9), (x - ty * tam, y + tx * tam)], vis))
        # rastro: uma segunda gota menor, um pouco atrás
        ang2 = ang - 0.22
        r2 = r + 0.06
        x2, y2 = r2 * math.cos(ang2), r2 * math.sin(ang2)
        t2 = tam * 0.55
        gotas.append(([(x2 + t2, y2), (x2, y2 + t2), (x2 - t2, y2), (x2, y2 - t2)], vis * 0.6))
    bate = pulso(t, 0.45, 0.62) + 0.7 * pulso(t, 0.64, 0.8)
    coracao = T.gauss(0, 0, 0.24, 0.24) * bate * 2.2 + T.gauss(0, 0, 0.36, 0.36) * bate * 0.4
    anel = T.ring(0.15 + 0.4 * rel(t, 0.45, 0.85), 0.03) * pulso(t, 0.45, 0.9)
    D = T.polys(gotas, 0.004)
    G += (D * 1.8 + coracao + anel * 1.3) * env
    H += (D * 0.5 + coracao * 1.1 + anel * 0.5) * env
    return G, H


def dissipar(T, t, rng):
    """Dissipar: o anel de proteção em volta do rival aparece, racha em arcos, os pedaços se
    afastam girando e a energia que ele tinha se desfaz em fagulhas para fora."""
    G, H = vazio(T)
    env = apaga(t, 0.65, 1)
    aparece = janela(t, 0.0, 0.12)
    racha = rel(t, 0.18, 0.7)
    abre = ease_out(racha, 2)
    arcos = []
    for k in range(6):
        a0 = k / 6 * TAU + 0.12
        meio = a0 + TAU / 12
        r = 0.55 + 0.16 * abre
        gira = 0.6 * abre * (1 if k % 2 else -1)
        ox, oy = 0.1 * abre * math.cos(meio), 0.1 * abre * math.sin(meio)
        larg = 0.07 * (1 - 0.5 * abre)
        arcos.append((_arco(ox, oy, r, a0 + 0.06 + gira, a0 + TAU / 6 - 0.06 + gira, larg, 16), 1.0 - 0.6 * abre))
    # runas: pequenos losangos no anel que piscam e apagam quando ele racha
    runas = []
    for k in range(6):
        a = k / 6 * TAU + 0.12 + TAU / 12
        x, y = 0.55 * math.cos(a), 0.55 * math.sin(a)
        rr = 0.05
        runas.append(([(x, y - rr), (x + rr * 0.7, y), (x, y + rr), (x - rr * 0.7, y)], (1 - racha) * aparece))
    fagulhas = []
    sub = np.random.default_rng(419)
    for k in range(22):
        a = sub.uniform(0, TAU)
        d = 0.3 + 0.5 * ease_out(rel(t, 0.2, 0.85), 1.6) * sub.uniform(0.6, 1.0)
        x, y = d * math.cos(a), d * math.sin(a)
        rr = 0.018
        fagulhas.append(([(x, y - rr), (x + rr, y), (x, y + rr), (x - rr, y)], pulso(t, 0.2, 0.9)))
    flash = T.gauss(0, 0, 0.3, 0.3) * pulso(t, 0.16, 0.34) * 1.1
    A = T.polys(arcos, 0.004) * aparece
    G += (A * 1.5 + T.polys(runas, 0.003) * 1.4 + T.polys(fagulhas, 0.004) * 1.4 + flash) * env
    H += (A * 0.7 + T.polys(runas, 0.003) * 1.0 + T.polys(fagulhas, 0.004) * 0.8 + flash) * env
    return G, H


def renascer(T, t, rng):
    """Renascer: brasas giram e se juntam no corpo caído, sobem numa coluna de fogo e um par de
    asas de chama se abre para o alto, soltando penas de brasa."""
    G, H = vazio(T)
    junta = rel(t, 0, 0.36)
    brasas = []
    for k in range(30):
        a0 = k / 30 * TAU
        r = 0.08 + 0.72 * (1 - ease_in(junta, 1.6))
        a = a0 + junta * 5
        vivo = 1 - rel(t, 0.34, 0.42)
        brasas.append((math.cos(a) * r, 0.18 + math.sin(a) * r * 0.42, (0.4 + 0.6 * junta) * vivo))
    estouro = pulso(t, 0.32, 0.62)
    n = _subindo(T, 977, t, 0.06, 1.6)
    coluna = T.gauss(0, -0.15, 0.13, 0.62) * (0.75 + 0.25 * np.clip(n, -1, 1)) * estouro * 1.7
    abre = back(rel(t, 0.38, 0.72), 1.4)
    bate = 0.12 * math.sin(rel(t, 0.62, 0.95) * math.pi)
    asas, fio = T.zero(), T.zero()
    for lado in (-1, 1):
        for k in range(8):
            # as penas de cima apontam para o alto; as de baixo abrem para o lado
            a = -math.pi / 2 + lado * (0.18 + k * 0.17) - lado * bate
            comp = (0.92 - 0.06 * k) * abre
            x1, y1 = lado * 0.05, 0.02
            x2, y2 = x1 + math.cos(a) * comp, y1 + math.sin(a) * comp * 0.9
            asas += T.polys([(lamina(x1, y1, x2, y2, 0.075 - 0.005 * k), 1 - 0.07 * k)], 0.012)
            fio += T.polys([(lamina(x1, y1, x1 + (x2 - x1) * 0.8, y1 + (y2 - y1) * 0.8, 0.02), 1)], 0.005)
    asas = asas * (0.7 + 0.3 * np.clip(n, -1, 1)) * apaga(t, 0.75, 1)
    fio = fio * apaga(t, 0.75, 1)
    penas = []
    for _ in range(26):
        f = (rng.uniform(0, 1) + t * 1.2) % 1
        penas.append((rng.uniform(-0.65, 0.65), -0.55 + f * 1.0, math.sin(math.pi * f) * rng.uniform(0.3, 1) * rel(t, 0.42, 0.6)))
    chao = T.ring(0.2 + 0.5 * ease_out(rel(t, 0.32, 0.7), 2), 0.03, cy=0.42, squash=3.6) * pulso(t, 0.32, 0.9) * 1.2
    G += T.splats(brasas, 0.016) * 1.4 + (coluna + T.glow(asas, 1.2, 1.2, 0.03) + T.splats(penas, 0.012) + chao) * apaga(t, 0.82, 1)
    H += T.splats(brasas, 0.009) + (coluna * 0.8 + fio * 1.2 + chao * 0.4) * apaga(t, 0.82, 1)
    return G, H


def brasas_renascendo(T, t, rng):
    """Renascendo (laço): brasas fracas sobem do corpo caído e um anel de fogo respira no chão."""
    G, H = vazio(T)
    respira = 0.6 + 0.4 * math.sin(t * TAU)
    pts = []
    for k in range(18):
        f = (k / 18 + t) % 1
        x = 0.35 * math.sin(k * 2.4 + f * 3)
        pts.append((x, 0.4 - f * 0.8, math.sin(math.pi * f) * (0.5 + 0.5 * ((k * 7) % 3 == 0))))
    anel = T.ring(0.42, 0.03, cy=0.42, squash=3.6) * respira
    G += T.splats(pts, 0.014) * 1.2 + anel + T.gauss(0, 0.3, 0.25, 0.12) * 0.35 * respira
    H += T.splats(pts, 0.007) * 0.8 + anel * 0.35
    return G, H

REGISTRO = [
    ("ressurreicao", ressurreicao, GRANDE, "feixe de luz que levanta o aliado caído", False),
    ("renascer", renascer, GRANDE, "asas de fogo: renasce das cinzas", False),
    ("dissipar", dissipar, GRANDE, "anel de proteção do rival que racha e se desfaz", False),
    ("reflexo", reflexo, GRANDE, "escudo de espelho hexagonal que devolve o golpe", False),
    ("espinhos", espinhos, GRANDE, "pontas que brotam do corpo e recolhem", False),
    ("vampirismo", vampirismo, GRANDE, "gotas de sangue em espiral e pulso de coração", False),
    ("provocar", provocar, GRANDE, "marca de raiva sobre o rival provocado, anéis se fechando", False),
    ("brasas_renascendo", brasas_renascendo, GRANDE, "brasas sobre quem vai renascer (laço)", True),
    ("cura_em_area", cura_em_area, GRANDE, "cura em área com cruzes", False),
    ("regeneracao", regeneracao, GRANDE, "folhas subindo em espiral", False),
    ("grito_de_guerra", grito_de_guerra, GRANDE, "estandarte de raios e divisas", False),
    ("velocidade", velocidade, GRANDE, "linhas de vento e asinhas", False),
    ("escudo_tech", escudo_tech, GRANDE, "parede de painéis hexagonais", False),
    ("barreira_magica", barreira_magica, GRANDE, "cúpula de runas", False),
    ("escudo_fisico", escudo_fisico, GRANDE, "brasão de escudo", False),
    ("armadura", armadura, GRANDE, "placas de armadura", False),
    ("resgate", resgate, GRANDE, "mergulho de resgate", False),
    ("bencao", bencao, GRANDE, "penas e halo", False),
    ("lanche", lanche, GRANDE, "mordida, vapor e coração", False),
    ("purificar_onda", purificar, GRANDE, "onda que lava", False),
    ("enfraquecer", enfraquecer, GRANDE, "setas para baixo", False),
    ("lentidao", lentidao, GRANDE, "ampulheta", False),
    ("marca", marca, GRANDE, "alvo travando", False),
    ("silencio", silencio, GRANDE, "som cortado", False),
    ("medo", medo, GRANDE, "olhos na sombra", False),
    ("exposto", exposto, GRANDE, "guarda trincando", False),
    ("estrela_invencivel", estrela_invencivel, GRANDE, "estrela invencível", False),
]
