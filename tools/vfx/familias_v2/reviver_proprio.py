"""O reviver de cada um (pedido do jogador: "faz o efeito para eles reviverem únicos pra eles… tem que
ter a ver com cada um"). Toca sobre o aliado que volta.

Hades ............ o portal do submundo abre no chão, as almas sobem em espiral e a flor dourada dos
                   Campos Elísios desabrocha no peito de quem volta.
Feiticeira ....... os fios de magia do caos vêm ondulando dos lados, fecham o hex (o círculo com o
                   símbolo girando) e a realidade estala de volta.
Pain ............. o Rinne Tensei: as almas caem do céu como cometas, uma depois da outra, e entram
                   no corpo; os anéis do Rinnegan ondulam no chão.
Rick ............. o portal verde gira em pé ao lado, o clone sai e as linhas de escaneamento descem
                   pelo corpo; o portal se fecha num ponto.
Constantine ...... o círculo ocultista acende no chão (dois anéis, as runas e o triângulo), a fumaça
                   do cigarro sobe em caracol e o clarão do pacto.
She-Ra ........... a Espada da Proteção desce do céu num feixe de luz, crava na frente de quem volta,
                   a joia acende e as estrelas se espalham.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, lamina, pulso, rel, vazio


def _circulo(cx, cy, r, n=28, sq=1.0):
    return [(cx + r * math.cos(a), cy + r * sq * math.sin(a)) for a in np.linspace(0, TAU, n, endpoint=False)]


def _brilho(T, A, s=0.008):
    """A borda acesa de uma forma (o "calor" do contorno)."""
    return np.clip(A - T.blur(A, s), 0, 1)


# =================================================================== Hades
def levanta_hadescz(T, t, rng):
    """O submundo devolve a alma: a fenda escura abre no chão (anéis achatados), as almas sobem em
    espiral com rabo de fumaça e se juntam no peito, e a flor dos Campos Elísios desabrocha."""
    G, H = vazio(T)
    abre = ease_out(rel(t, 0.0, 0.25), 2) * (1 - rel(t, 0.75, 1.0))
    chao = sum(T.ring(0.18 + 0.38 * abre * k / 3, 0.012, 0, 0.42, 3.0) for k in (1, 2, 3)) * abre
    almas = T.zero()
    for k in range(7):
        f = rel(t, 0.08 + 0.04 * k, 0.55 + 0.03 * k)
        if f <= 0 or f >= 1:
            continue
        pts = []
        for j in range(10):
            u = max(0.0, f - j * 0.035)
            a = k / 7 * TAU + u * 5.0
            r = 0.45 * (1 - u)
            pts.append((math.cos(a) * r, 0.42 - 0.62 * ease_out(u, 1.4) + math.sin(a) * r * 0.25))
        almas += T.polyline(pts, 0.035) * math.sin(math.pi * f)
        hx, hy = pts[0]
        almas += T.gauss(hx, hy, 0.05) * math.sin(math.pi * f) * 1.6
    flor = rel(t, 0.5, 0.75)
    petalas = []
    for k in range(8):
        a = -math.pi / 2 + k / 8 * TAU + 0.3 * flor
        comp = 0.38 * back(flor, 1.6)
        petalas.append((lamina(0, -0.2, math.cos(a) * comp, -0.2 + math.sin(a) * comp, 0.09), 1.0))
    P = T.polys(petalas, 0.004) * (1 - rel(t, 0.82, 1.0)) if flor > 0 else T.zero()
    G += chao * 0.9 + almas * 0.9 + P * 0.8 + T.gauss(0, -0.2, 0.2) * pulso(t, 0.48, 0.8)
    H += almas * 0.5 + _brilho(T, P) * 1.2 + T.flare(0, -0.2, 0.5 * pulso(t, 0.5, 0.7) + 0.01, thin=0.02) * pulso(t, 0.5, 0.7)
    return G, H


# =================================================================== Feiticeira Escarlate
def levanta_scarletwitch(T, t, rng):
    """Magia do caos: fios vermelhos ondulando chegam dos dois lados, enrolam no corpo, o hex (dois
    círculos e o símbolo de pontas) gira, e a realidade estala num clarão."""
    G, H = vazio(T)
    fios = T.zero()
    for k in range(6):
        lado = -1 if k % 2 else 1
        f = ease_out(rel(t, 0.0 + 0.03 * k, 0.45 + 0.03 * k), 1.6)
        pts = []
        for j in range(26):
            u = j / 25 * f
            x = lado * (1.0 - 1.0 * u)
            y = -0.55 + 0.2 * k + 0.12 * math.sin(u * 14 + k + t * 8) * (1 - u)
            pts.append((x, y * (1 - u) + (-0.1 + 0.25 * math.sin(u * 10 + k)) * u * 0.5))
        fios += T.polyline(pts, 0.016) * (1 - rel(t, 0.55, 0.7))
    hexo = rel(t, 0.35, 0.55)
    gira = t * 4
    simbolo = []
    for k in range(6):
        a = gira + k / 6 * TAU
        simbolo.append((lamina(0, -0.1, math.cos(a) * 0.42, -0.1 + math.sin(a) * 0.42, 0.03), 1.0))
    S = T.polys(simbolo, 0.004)
    aneis = T.ring(0.46, 0.012, 0, -0.1) + T.ring(0.34, 0.008, 0, -0.1)
    vis = hexo * (1 - rel(t, 0.78, 0.95))
    estalo = pulso(t, 0.62, 0.8)
    G += fios * 0.9 + (S * 0.7 + aneis * 0.9) * vis + T.gauss(0, -0.1, 0.35) * estalo * 1.2
    H += fios * 0.4 + (_brilho(T, S) + aneis * 0.4) * vis + T.flare(0, -0.1, 0.9 * estalo + 0.01, 0.4, 0.012) * estalo
    return G, H


# =================================================================== Pain
def levanta_pain(T, t, rng):
    """Rinne Tensei: as almas caem do céu como cometas (cabeça acesa, rabo comprido), uma depois da
    outra, e entram no corpo; no chão os anéis do Rinnegan ondulam e no fim o corpo acende."""
    G, H = vazio(T)
    sub = np.random.default_rng(11)
    cometas = T.zero()
    cabecas = T.zero()
    for k in range(9):
        x0 = sub.uniform(-0.75, 0.75)
        ini = 0.02 + 0.05 * k
        f = rel(t, ini, ini + 0.32)
        if f <= 0 or f >= 1:
            continue
        u = ease_in(f, 1.6)
        hx, hy = x0 * (1 - u), -1.0 + 0.95 * u
        tx, ty = x0 * (1 - max(0, u - 0.35)), -1.0 + 0.95 * max(0, u - 0.35)
        cometas += T.polyline([(tx, ty), (hx, hy)], 0.02) * (0.4 + 0.6 * u)
        cabecas += T.gauss(hx, hy, 0.035)
    onda = T.zero()
    for k in range(4):
        f = (t * 1.5 + k / 4) % 1
        onda += T.ring(0.1 + 0.5 * f, 0.012, 0, 0.42, 3.2) * (1 - f)
    acende = pulso(t, 0.55, 0.95)
    G += cometas * 0.9 + cabecas * 1.2 + onda * 0.7 * (1 - rel(t, 0.8, 1.0)) + T.gauss(0, -0.05, 0.28, 0.4) * acende
    H += cabecas * 0.9 + cometas * 0.3 + T.flare(0, -0.05, 0.7 * acende + 0.01, thin=0.014) * acende
    return G, H


# =================================================================== Rick
def levanta_rick(T, t, rng):
    """O portal do Rick: o disco verde em pé abre girando (bracos em espiral), o clone sai por ele, as
    linhas de escaneamento descem pelo corpo, e o portal encolhe até sumir num ponto."""
    G, H = vazio(T)
    abre = back(rel(t, 0.0, 0.25), 1.4) * (1 - ease_in(rel(t, 0.6, 0.85), 2))
    cx, cy = 0.0, -0.05
    bracos = []
    if abre > 0.01:
        for k in range(5):
            pts = []
            for j in range(30):
                u = j / 29
                a = k / 5 * TAU + u * 4.5 - t * 9
                r = 0.55 * abre * u
                pts.append((cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r))
            bracos.append(pts)
    B = sum((T.polyline(p, 0.03) for p in bracos), T.zero())
    # a borda é uma elipse em pé (o portal visto de frente, mais alto que largo), ondulando
    borda = T.polyline([(cx + math.cos(a) * 0.34 * abre * (1 + 0.05 * math.sin(7 * a + t * 20)), cy + math.sin(a) * 0.55 * abre) for a in np.linspace(0, TAU, 60)], 0.035) if abre > 0.01 else T.zero()
    disco = T.gauss(cx, cy, 0.22 * abre + 0.001, 0.4 * abre + 0.001)
    varre = rel(t, 0.35, 0.75)
    linhas = T.zero()
    if 0 < varre < 1:
        for k in range(3):
            y = -0.6 + 1.1 * ((varre + k * 0.08) % 1)
            linhas += T.polyline([(-0.45, y), (0.45, y)], 0.01) * math.sin(math.pi * varre)
    G += disco * 0.8 + B * 0.7 + borda * 1.0 + linhas * 0.9 + T.gauss(0, -0.05, 0.3, 0.45) * pulso(t, 0.7, 0.95) * 0.8
    H += B * 0.4 + borda * 0.6 + linhas * 0.8 + T.flare(cx, cy, 0.5 * pulso(t, 0.82, 0.92) + 0.01, thin=0.02) * pulso(t, 0.82, 0.92)
    return G, H


# =================================================================== Constantine
def levanta_constantine(T, t, rng):
    """O pacto: o círculo ocultista acende no chão (dois anéis, as runas em volta e o triângulo de
    invocação), a fumaça do cigarro sobe em caracol, e o clarão do pacto puxa o aliado de volta."""
    G, H = vazio(T)
    acende = ease_out(rel(t, 0.0, 0.3), 2) * (1 - rel(t, 0.8, 1.0))
    cy, sq = 0.42, 3.0
    aneis = (T.ring(0.55, 0.01, 0, cy, sq) + T.ring(0.45, 0.008, 0, cy, sq)) * acende
    runas = []
    for k in range(12):
        a = k / 12 * TAU + t * 0.8
        x, y = math.cos(a) * 0.5, cy + math.sin(a) * 0.5 / sq
        runas.append(([(x - 0.012, y - 0.02), (x + 0.012, y - 0.02), (x + 0.004, y + 0.02), (x - 0.004, y + 0.02)], acende))
    R = T.polys(runas, 0.002)
    tri = [(math.cos(-math.pi / 2 + k / 3 * TAU + t) * 0.42, cy + math.sin(-math.pi / 2 + k / 3 * TAU + t) * 0.42 / sq) for k in range(4)]
    Tr = T.polyline(tri, 0.008) * acende
    fumo = T.zero()
    for k in range(3):
        f = rel(t, 0.15 + 0.08 * k, 0.85)
        pts = []
        for j in range(20):
            u = j / 19 * f
            pts.append((-0.3 + 0.3 * k + 0.08 * math.sin(u * 9 + k * 2), cy - 0.05 - 0.9 * u))
        fumo += T.polyline(pts, 0.03, blur=0.01) * (1 - f) * 0.8
    pacto = pulso(t, 0.5, 0.78)
    coluna = T.gauss(0, -0.1, 0.12, 0.7) * pacto
    G += aneis * 1.0 + R * 0.9 + Tr * 0.9 + fumo * 0.6 + coluna * 1.2
    H += aneis * 0.4 + R * 0.6 + coluna * 0.6 + T.flare(0, -0.15, 0.7 * pacto + 0.01, thin=0.014) * pacto
    return G, H


# =================================================================== She-Ra
def _espada(cx, cy, esc):
    """A Espada da Proteção, ponta para baixo: lâmina, guarda larga com as asas e a joia."""
    S = lambda pts: [(cx + x * esc, cy + y * esc) for x, y in pts]
    lam = S([(-0.04, -0.25), (0.04, -0.25), (0.035, 0.45), (0.0, 0.58), (-0.035, 0.45)])
    guarda = S([(-0.22, -0.3), (-0.06, -0.24), (0.06, -0.24), (0.22, -0.3), (0.16, -0.22), (0.05, -0.18), (-0.05, -0.18), (-0.16, -0.22)])
    cabo = S([(-0.025, -0.3), (0.025, -0.3), (0.025, -0.48), (-0.025, -0.48)])
    joia = S(_circulo(0, -0.24, 0.035, 14))
    return lam, guarda, cabo, joia


def levanta_shera(T, t, rng):
    """Pela honra de Grayskull: o feixe de luz desce do céu, a Espada da Proteção cai nele e crava na
    frente de quem volta, a joia acende, e as estrelas se espalham num leque."""
    G, H = vazio(T)
    feixe = ease_out(rel(t, 0.0, 0.2), 2) * (1 - rel(t, 0.7, 0.9))
    luz = T.gauss(0, -0.4, 0.07, 0.9) * feixe
    cai = ease_in(rel(t, 0.1, 0.35), 2)
    y = -1.2 + 1.15 * cai
    vis = (cai > 0) * (1 - rel(t, 0.85, 1.0))
    lam, guarda, cabo, joia = _espada(0, y, 0.95)
    E = T.polys([(lam, 1.0), (guarda, 1.0), (cabo, 0.8)], 0.003) * vis
    J = T.polys([(joia, 1.0)], 0.003) * vis
    crava = pulso(t, 0.33, 0.6)
    est = []
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.33
        d = 0.15 + 0.6 * ease_out(rel(t, 0.35, 0.8), 2)
        est.append((estrela(math.cos(a) * d, -0.2 + math.sin(a) * d, 0.045, a, 4, 0.4), pulso(t, 0.35, 0.95)))
    St = T.polys(est, 0.004)
    G += luz * 1.1 + E * 0.9 + J * 1.3 * (1 + crava) + St * 1.0 + T.gauss(0, 0.35, 0.4, 0.08) * crava
    H += luz * 0.5 + _brilho(T, E) * 1.1 + J * crava * 1.2 + St * 0.5 + T.flare(0, y - 0.23 * 0.95, 0.6 * crava + 0.01, thin=0.014) * crava
    return G, H


REGISTRO = [
    ("levanta_hadescz", levanta_hadescz, GRANDE, "Hades revive: o portal do submundo, as almas em espiral e a flor dos Elísios", False),
    ("levanta_scarletwitch", levanta_scarletwitch, GRANDE, "Feiticeira revive: os fios do caos, o hex girando e a realidade estalando", False),
    ("levanta_pain", levanta_pain, GRANDE, "Pain revive (Rinne Tensei): as almas caem do céu como cometas e entram no corpo", False),
    ("levanta_rick", levanta_rick, GRANDE, "Rick revive: o portal verde gira, o clone sai e o escaneamento desce", False),
    ("levanta_constantine", levanta_constantine, GRANDE, "Constantine revive: o círculo ocultista, a fumaça do cigarro e o clarão do pacto", False),
    ("levanta_shera", levanta_shera, GRANDE, "She-Ra revive: a Espada da Proteção desce no feixe de luz e crava", False),
]
