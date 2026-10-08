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


REGISTRO = [
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
