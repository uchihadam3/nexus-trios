"""Cortes: lâminas com caráter (vertical, saque rápido, mil cortes, foice, espadão, lâminas elementais)."""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, MEDIA, TAU, _subindo, apaga, ease_out, faiscas, jagged, janela, lamina, pulso, rel,
                   smooth, some, vazio)


def _rasgo(T, x1, y1, x2, y2, larg, p, fim):
    """Corpo e fio de um corte reto que aparece em `p` e se desfaz a partir de `fim`."""
    corpo = T.polys([(lamina(x1, y1, x2, y2, larg, p, inicio=fim), 1)], 0.004)
    fio = T.polys([(lamina(x1, y1, x2, y2, larg * 0.3, p, inicio=fim), 1)], 0.002)
    return corpo, fio


def corte_vertical(T, t, rng):
    """Corte vertical: a lâmina desce reto de cima a baixo, o rasgo fica e faíscas saem para os lados."""
    G, H = vazio(T)
    p = ease_out(rel(t, 0, 0.18), 2.5)
    corpo, fio = _rasgo(T, 0.05, -0.9, -0.05, 0.9, 0.09, p, rel(t, 0.3, 0.95))
    clarao = T.gauss(0, 0, 0.1, 0.4) * pulso(t, 0.08, 0.4) * 1.8
    fa = faiscas(T, rng, t, 22, 0.7, 0.03, cone=(-0.5, 0.5), gravidade=0.3, inicio=0.12) + faiscas(T, rng, t, 22, 0.7, 0.03, cone=(math.pi - 0.5, math.pi + 0.5), gravidade=0.3, inicio=0.12)
    G += T.glow(corpo, 1.1, 1.2, 0.025) + fio * 1.3 + clarao + T.glow(fa, 1, 1.1, 0.02)
    H += fio * 1.5 + corpo * 0.3 + clarao + fa * 0.6
    return G, H


def iaido(T, t, rng):
    """Saque rápido: um risco finíssimo aparece de uma vez; um instante depois o alvo se abre num clarão."""
    G, H = vazio(T)
    linha = np.exp(-((T.V + 0.1 * T.U) / 0.006) ** 2) * smooth(-np.abs(T.U), -0.95, -0.7) * (t < 0.42) * janela(t, 0, 0.04)
    tt = rel(t, 0.38, 1)
    on = t >= 0.38
    abre = 0.02 + 0.22 * ease_out(tt, 2)
    metades = (np.exp(-((T.V + 0.1 * T.U - abre) / 0.012) ** 2) + np.exp(-((T.V + 0.1 * T.U + abre) / 0.012) ** 2)) * smooth(-np.abs(T.U), -0.95, -0.6) * (1 - tt) ** 1.3 * on
    clarao = T.gauss(0, 0, 0.5, 0.08) * some(t, 0.38, 0.65) * 3.2 + T.flare(0, 0, 2.2, -0.1) * some(t, 0.38, 0.6) * 2.5
    fa = faiscas(T, rng, t, 26, 0.9, 0.03, cone=(-0.5, 0.5), gravidade=0.25, inicio=0.38)
    G += linha * 2.5 + metades * 1.6 + clarao + T.glow(fa, 1, 1.1, 0.02)
    H += linha * 2.5 + metades + clarao + fa * 0.6
    return G, H


def mil_cortes(T, t, rng):
    """Mil cortes: dezenas de riscos finos em todas as direções, um atrás do outro, e um X final."""
    G, H = vazio(T)
    sub = np.random.default_rng(91)
    acc = T.zero()
    for k in range(16):
        a0 = 0.03 + k * 0.035
        ang = sub.uniform(0, math.pi)
        r = sub.uniform(0.5, 0.85)
        cx, cy = sub.uniform(-0.2, 0.2), sub.uniform(-0.2, 0.2)
        x1, y1 = cx - math.cos(ang) * r, cy - math.sin(ang) * r
        x2, y2 = cx + math.cos(ang) * r, cy + math.sin(ang) * r
        p = ease_out(rel(t, a0, a0 + 0.06), 2)
        if p <= 0:
            continue
        acc += T.polys([(lamina(x1, y1, x2, y2, 0.025, p, inicio=rel(t, a0 + 0.08, a0 + 0.22)), 1)], 0.002)
    xp = ease_out(rel(t, 0.62, 0.72), 2)
    xis = sum(T.polys([(lamina(-0.75 * sx, -0.75, 0.75 * sx, 0.75, 0.07, xp, inicio=rel(t, 0.8, 1)), 1)], 0.003) for sx in (1, -1)) if xp > 0 else T.zero()
    clarao = T.gauss(0, 0, 0.25) * pulso(t, 0.6, 0.9) * 2.4
    G += T.glow(acc, 1.3, 1, 0.015) + T.glow(xis, 1.2, 1.3, 0.025) + clarao
    H += acc * 1.2 + xis + clarao
    return G, H


def foice(T, t, rng):
    """Foice: meia-lua enorme varrendo de cima, rastro de névoa e almas sendo puxadas."""
    G, H = vazio(T)
    p = ease_out(rel(t, 0, 0.32), 2)
    env = apaga(t, 0.45, 1)
    lam = T.arc_band(0.66, 0.14, -3.0, -3.0 + 2.9 * p + 0.01, cx=0.05, cy=0.05, crescente=True) * env
    nevoa = T.arc_band(0.56, 0.2, -3.0, -3.0 + 2.9 * p + 0.01, cx=0.05, cy=0.05) * env
    n = _subindo(T, 101, t, 0.07, 0.5)
    nevoa = nevoa * np.clip(0.5 + 0.5 * n, 0, 1)
    almas = []
    for _ in range(10):
        f = (rng.uniform(0, 1) + t * 0.8) % 1
        almas.append((rng.uniform(-0.5, 0.5), 0.5 - f * 1.1, math.sin(math.pi * f) * rng.uniform(0.4, 1) * janela(t, 0.2, 0.4)))
    a = T.splats(almas, 0.025)
    G += T.glow(lam, 1.2, 1.2, 0.025) + nevoa * 0.6 + a * 1.2
    H += lam * 0.7 + a * 0.4
    return G, H


def espadao(T, t, rng):
    """Espadão: arco largo e pesado, o chão racha embaixo e blocos voam."""
    G, H = vazio(T)
    p = ease_out(rel(t, 0, 0.25), 2.2)
    env = apaga(t, 0.4, 0.85)
    arco = T.arc_band(0.66, 0.2, -2.7, -2.7 + 2.9 * p + 0.01, squash=0.85, crescente=True) * env
    fio = T.arc_band(0.74, 0.03, -2.7, -2.7 + 2.9 * p + 0.01, squash=0.85) * env
    tt = rel(t, 0.22, 1)
    sub = np.random.default_rng(15)
    rach = T.zero()
    for k in range(5):
        pts = jagged(sub, 0.2, 0.55, 0.2 + sub.uniform(-0.8, 0.8), 0.55 + sub.uniform(-0.15, 0.2), 4, 0.25)
        rach += T.polyline(pts, 0.012, 1) * janela(t, 0.22, 0.32)
    blocos = []
    for _ in range(10):
        a = rng.uniform(-math.pi + 0.3, -0.3)
        d = rng.uniform(0.2, 0.7) * ease_out(tt, 2)
        x, y = 0.2 + math.cos(a) * d, 0.5 + math.sin(a) * d + 0.9 * tt * tt
        s = rng.uniform(0.03, 0.06)
        blocos.append(([(x - s, y - s), (x + s, y - s * 0.6), (x + s * 0.7, y + s), (x - s, y + s * 0.7)], (1 - tt) * (t > 0.22)))
    b = T.polys(blocos, 0.003)
    impacto = T.gauss(0.2, 0.5, 0.2, 0.1) * some(t, 0.22, 0.55) * 2.6
    G += T.glow(arco, 1, 1.2, 0.03) + fio * 1.5 + rach * apaga(t, 0.6, 1) + b * 1.2 + impacto
    H += fio * 1.5 + arco * 0.3 + rach * 0.6 * apaga(t, 0.6, 1) + impacto
    return G, H


def _arco_corte(T, t, a0=-2.4, span=2.6, raio=0.62, larg=0.12, dur=0.25):
    p = ease_out(rel(t, 0, dur), 2.2)
    return T.arc_band(raio, larg, a0, a0 + span * p + 0.01, squash=0.75, crescente=True), p


def lamina_de_fogo(T, t, rng):
    """Lâmina de fogo: o arco do corte pega fogo; as chamas sobem do rastro e brasas caem."""
    G, H = vazio(T)
    arco, p = _arco_corte(T, t)
    env = apaga(t, 0.5, 1)
    n = _subindo(T, 111, t, 0.05, 1.2)
    sobe = T.warp(arco, n * 0.0, -0.12 * rel(t, 0.1, 1) - 0.04 * np.abs(n))
    chama = np.maximum(arco, sobe * 0.9) * (0.7 + 0.3 * np.clip(n, -1, 1))
    brasas = []
    for _ in range(26):
        f = (rng.uniform(0, 1) + t * 1.3) % 1
        a = rng.uniform(-2.4, -2.4 + 2.6 * p)
        brasas.append((math.cos(a) * 0.62 + rng.uniform(-0.05, 0.05), math.sin(a) * 0.62 * 0.75 - f * 0.4, (1 - f) * rng.uniform(0.3, 1)))
    br = T.splats(brasas, 0.01)
    G += T.glow(chama, 1.2, 1.3, 0.03) * env + br * 1.2
    H += arco * 0.9 * env + br * 0.8
    return G, H


def lamina_eletrica(T, t, rng):
    """Lâmina elétrica: o corte corre com raios pulando ao longo do fio."""
    G, H = vazio(T)
    arco, p = _arco_corte(T, t, larg=0.09)
    env = apaga(t, 0.5, 1)
    sub = np.random.default_rng(int(t * 997) + 3)
    lin = T.zero()
    for k in range(5):
        a1 = -2.4 + 2.6 * p * sub.uniform(0, 0.8)
        a2 = a1 + sub.uniform(0.3, 0.7)
        x1, y1 = math.cos(a1) * 0.62, math.sin(a1) * 0.62 * 0.75
        x2, y2 = math.cos(a2) * 0.62, math.sin(a2) * 0.62 * 0.75
        lin += T.polyline(jagged(sub, x1, y1, x2, y2, 4, 0.35), 0.012, 1)
    clarao = T.gauss(0, -0.25, 0.14) * (0.4 + 0.6 * sub.uniform()) * pulso(t, 0.1, 0.5) * 1.3
    G += (T.glow(arco, 1, 1.1, 0.02) + T.glow(lin, 1.4, 1.6, 0.02)) * env + clarao
    H += (arco * 0.7 + lin * 1.4) * env + clarao * 0.6
    return G, H


def lamina_sombria(T, t, rng):
    """Lâmina sombria: meia-lua escura com bordas que se desfazem em fumaça e fiapos subindo."""
    G, H = vazio(T)
    arco, p = _arco_corte(T, t, larg=0.16)
    env = apaga(t, 0.5, 1)
    n = T.noise(np.random.default_rng(121), 0.04, 3)
    franja = T.warp(arco, n * 0.04, n * 0.04 - 0.08 * rel(t, 0.2, 1))
    fio = T.arc_band(0.66, 0.02, -2.4, -2.4 + 2.6 * p + 0.01, squash=0.75)
    fiapos = []
    for _ in range(18):
        f = (rng.uniform(0, 1) + t) % 1
        fiapos.append((rng.uniform(-0.6, 0.6), 0.1 - f * 0.7, math.sin(math.pi * f) * rng.uniform(0.3, 0.9)))
    G += (arco * 0.9 + franja * 0.8 * np.clip(0.6 + 0.4 * n, 0, 1) + fio * 1.4) * env + T.splats(fiapos, 0.02) * 0.9 * janela(t, 0.2, 0.4)
    H += fio * 1.1 * env
    return G, H


def motosserra(T, t, rng):
    """Motosserra: anel de dentes girando rápido, faíscas jorrando na tangente e clarão tremido."""
    G, H = vazio(T)
    env = janela(t, 0, 0.1) * apaga(t, 0.65, 1)
    giro = t * TAU * 4
    dentes = []
    for k in range(18):
        a = TAU * k / 18 + giro
        r0, r1 = 0.36, 0.5
        dentes.append(([(math.cos(a) * r0, math.sin(a) * r0), (math.cos(a + 0.22) * r1, math.sin(a + 0.22) * r1), (math.cos(a + 0.3) * r0, math.sin(a + 0.3) * r0)], 1))
    d = T.polys(dentes, 0.003)
    aro = T.ring(0.36, 0.02)
    sub = np.random.default_rng(int(t * 997) + 5)
    jorro = faiscas(T, sub, 0.5, 18, 0.7, 0.03, cone=(0.2, 1.2), cx=0.3, cy=-0.3, gravidade=0.3)
    tremido = T.gauss(sub.uniform(-0.03, 0.03), sub.uniform(-0.03, 0.03), 0.18) * (0.6 + 0.4 * sub.uniform()) * 1.6
    G += (T.glow(d + aro, 1.1, 1, 0.015) + T.glow(jorro, 1, 1.2, 0.02) + tremido) * env
    H += (d * 0.6 + jorro * 0.9 + tremido) * env
    return G, H


def lamina_de_agua(T, t, rng):
    """Lâmina de água: uma fita ondulada que gira em espiral com crista de espuma e gotas."""
    G, H = vazio(T)
    p = ease_out(rel(t, 0, 0.35), 2)
    env = apaga(t, 0.55, 1)
    pts, crista = [], []
    for k in range(80):
        u = k / 79 * p
        a = -2.8 + u * 6.0
        r = 0.78 - 0.5 * u + 0.04 * math.sin(u * 18 - t * 8)
        pts.append((math.cos(a) * r, math.sin(a) * r * 0.8))
        crista.append((math.cos(a) * (r + 0.06), math.sin(a) * (r + 0.06) * 0.8))
    fita = T.polyline(pts, 0.05, 1) + T.polyline([(x * 0.86, y * 0.86) for x, y in pts], 0.02, 0.6)
    esp = T.polyline(crista, 0.018, 1)
    gotas = []
    tt = rel(t, 0.15, 1)
    for _ in range(26):
        k = int(rng.uniform(0, 79) * p)
        x, y = pts[k]
        gotas.append((x * (1 + 0.3 * tt), y * (1 + 0.3 * tt) + 0.4 * tt * tt, (1 - tt) * rng.uniform(0.4, 1)))
    G += (T.glow(fita, 0.7, 1, 0.03) + esp * 1.5) * env + T.splats(gotas, 0.012) * 1.2
    H += (esp * 1.2 + fita * 0.2) * env + T.splats(gotas, 0.01) * 0.7
    return G, H


def disco(T, t, rng):
    """Disco arremessado em viagem: aro girando com borrão de movimento e faíscas atrás (aponta +x)."""
    G, H = vazio(T)
    giro = t * TAU * 3
    aro = T.ring(0.34, 0.035, squash=1.9) + T.ring(0.2, 0.02, squash=1.9) * 0.7
    raios = T.zero()
    for k in range(3):
        a = giro + TAU * k / 3
        raios += T.lines([(0, 0, math.cos(a) * 0.34, math.sin(a) * 0.34 / 1.9, 1)], 0.014, 0.003)
    borrao = T.blur(np.roll(aro, -6, axis=1), 0.02) * 0.6
    rastro = np.exp(-(T.V / 0.07) ** 2) * smooth(-T.U, 0.25, 0.95) * smooth(T.U + 1, 0, 0.3) * 0.5
    G += T.glow(aro + raios * 0.7, 1.2, 1, 0.02) + borrao + rastro
    H += aro * 0.8 + raios * 0.5
    return G, H


def ricochete(T, t, rng):
    """Ricochete: estalo metálico, anel rápido e faíscas em V, como algo que bate e volta."""
    G, H = vazio(T)
    clarao = T.flare(0, 0, 1.6, 0.8) * some(t, 0, 0.35) * 2.6 + T.gauss(0, 0, 0.1) * some(t, 0, 0.3) * 3
    anel = sum(T.ring(0.08 + 0.5 * ease_out(rel(t, k * 0.06, 0.5 + k * 0.06), 2.5), 0.015) * pulso(t, k * 0.06, 0.5 + k * 0.06) for k in range(3)) * 1.4
    fa = faiscas(T, rng, t, 18, 0.9, 0.032, cone=(-2.4, -1.6), gravidade=0.25) + faiscas(T, rng, t, 18, 0.9, 0.032, cone=(-1.2, -0.4), gravidade=0.25)
    G += clarao + anel + T.glow(fa, 1, 1.2, 0.02)
    H += clarao + anel * 0.4 + fa * 0.8
    return G, H


def florete(T, t, rng):
    """Florete: cinco estocadas finas e rápidas em ângulos diferentes, cada uma com um ponto de luz."""
    G, H = vazio(T)
    acc, pontos = T.zero(), T.zero()
    for k in range(5):
        a0 = k * 0.11
        ang = (k - 2) * 0.14
        p = ease_out(rel(t, a0, a0 + 0.08), 2)
        if p <= 0:
            continue
        tx, ty = 0.15 * math.cos(ang) + (k - 2) * 0.02, 0.15 * math.sin(ang) + (k - 2) * 0.12
        x1, y1 = tx - math.cos(ang) * 1.0, ty - math.sin(ang) * 1.0
        segs = [(x1, y1, x1 + (tx - x1) * p, y1 + (ty - y1) * p, apaga(t, a0 + 0.1, a0 + 0.3))]
        acc += T.tapered(segs, 0.04)
        pontos += (T.gauss(tx, ty, 0.05) * 2 + T.flare(tx, ty, 0.6, 0.6)) * pulso(t, a0 + 0.06, a0 + 0.3)
    G += T.glow(acc, 1.2, 1, 0.015) + pontos * 1.4
    H += acc * 0.9 + pontos
    return G, H


REGISTRO = [
    ("corte_vertical", corte_vertical, GRANDE, "corte vertical", False),
    ("iaido", iaido, GRANDE, "saque rápido com clarão atrasado", False),
    ("mil_cortes", mil_cortes, GRANDE, "mil cortes e X final", False),
    ("foice", foice, GRANDE, "foice em meia-lua", False),
    ("espadao", espadao, GRANDE, "espadão que racha o chão", False),
    ("lamina_de_fogo", lamina_de_fogo, GRANDE, "lâmina de fogo", False),
    ("lamina_eletrica", lamina_eletrica, GRANDE, "lâmina elétrica", False),
    ("lamina_sombria", lamina_sombria, GRANDE, "lâmina sombria", False),
    ("motosserra", motosserra, GRANDE, "dentes de serra girando", False),
    ("lamina_de_agua", lamina_de_agua, GRANDE, "fita de água em espiral", False),
    ("disco", disco, MEDIA, "disco girando em viagem (+x)", True),
    ("ricochete", ricochete, GRANDE, "estalo de ricochete", False),
    ("florete", florete, GRANDE, "estocadas finas em sequência", False),
]
