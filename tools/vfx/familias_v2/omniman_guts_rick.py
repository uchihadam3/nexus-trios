"""As habilidades do Omni-Man, do Guts e do Rick Sanchez, desenhadas para eles.

Omni-Man (tudo de perto: ele voa até o rival)
- soco_viltrumita: o soco chega de −x com as linhas de velocidade, o clarão, as
  ondas de choque achatadas, o chão rachando e o sangue.
- voo_de_impacto: ele desce do alto em velocidade supersônica — o cone de vapor
  em volta, o rastro — e o estrondo sônico no contato.
- sem_piedade: a surra — uma pancada atrás da outra em pontos diferentes, o
  sangue espirrando, e a última, a maior.

Guts (perto)
- matadora_guts: a Matadora de Dragões — o arco enorme e grosso de ferro,
  pesado, com o borrão do movimento, as faíscas e o sangue.
- armadura_berserker: a Armadura Berserker fechando nele — as placas pontudas
  apertando em volta, os olhos vermelhos acesos e a fumaça escura.
- ultimo_esforco: o golpe de cima para baixo com tudo — a lâmina caindo, o chão
  afundando em cratera, a poeira e o sangue.

Rick Sanchez (longe)
- portal_bala: o tiro verde da pistola de portal voando, ondulando (laço, viagem).
- portal_rick: o portal verde abrindo no rival, girando, o estouro saindo dele e
  o portal fechando.
- gadget_rick: a invenção improvisada explodindo no meio dos rivais — o clarão
  verde, os raios, as engrenagens voando e as espirais da confusão.
- plano_b_faixa: o canhão de plasma do Plano B, grosso e estalando (faixa, laço).
- plano_b: a explosão enorme do plasma, com o X do golpe cortado.
"""
from __future__ import annotations

import math

import numpy as np

from .base import FAIXA, GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _quadro(t, seed=0):
    return np.random.default_rng(seed + int(t * 997) % 9973)


def _raio(T, q, x1, y1, x2, y2, larg=0.01, depth=4, rough=0.32):
    return T.polyline(jagged(q, x1, y1, x2, y2, depth, rough), larg)


_RUIDOS: dict = {}


def _ruido(T, seed, escala=0.05, oitavas=3):
    chave = (T.W, T.H, seed, escala, oitavas)
    if chave not in _RUIDOS:
        _RUIDOS[chave] = T.noise(np.random.default_rng(seed), escala, oitavas)
    return _RUIDOS[chave]


def _sangue(T, t, seed, n, t0, alcance=0.6, ang0=-1.2, ang1=1.2, tam=0.02):
    """Gotas de sangue espirrando de um ponto e caindo."""
    sub = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        a = sub.uniform(ang0, ang1)
        d = (0.08 + alcance * ease_out(rel(t, t0, t0 + 0.45), 2) * sub.uniform(0.3, 1))
        cai = 0.35 * rel(t, t0 + 0.1, 1.0) ** 2
        pts.append((d * math.cos(a), d * math.sin(a) + cai, pulso(t, t0, 0.95) * sub.uniform(0.5, 1)))
    return T.splats(pts, tam)


# =================================================================== Omni-Man
def soco_viltrumita(T, t, rng):
    """O Golpe viltrumita: o soco chega de −x com as linhas de velocidade, o clarão, duas ondas de
    choque achatadas, as rachaduras saindo do ponto e o sangue."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    entra = ease_in(rel(t, 0.0, 0.14), 1.6)
    sub = np.random.default_rng(3)
    linhas = T.tapered([(-1.0, y, -1.0 + 0.92 * entra, y * 0.5, 1.0) for y in sub.uniform(-0.3, 0.3, 7)], 0.03) * (1 - rel(t, 0.14, 0.3))
    k = pulso(t, 0.12, 0.45)
    clarao = T.gauss(0, 0, 0.22) * k * 1.8 + T.flare(0, 0, 1.2 * k + 1e-3, 0.0, 0.01) * k
    ondas = T.zero()
    for j, t0 in enumerate((0.12, 0.2)):
        ondas += T.ring(0.1 + 0.75 * ease_out(rel(t, t0, t0 + 0.45), 2), 0.035 - 0.01 * j, 0, 0, 1.6) * pulso(t, t0, t0 + 0.45)
    q = np.random.default_rng(5)
    rachas = T.zero()
    for _ in range(7):
        a = q.uniform(0, TAU)
        comp = (0.3 + 0.35 * q.uniform()) * ease_out(rel(t, 0.12, 0.3), 2)
        rachas += _raio(T, q, 0, 0, comp * math.cos(a) + 1e-3, comp * math.sin(a), 0.012, 3, 0.25)
    rachas *= 1 - rel(t, 0.55, 0.9)
    sangue = _sangue(T, t, 7, 14, 0.14, 0.6, -1.0, 1.0, 0.022)
    G += (linhas + clarao + ondas + rachas * 1.2 + sangue * 0.6) * env
    H += (linhas * 0.5 + clarao * 1.1 + rachas * 0.6 + sangue * 0.15) * env
    return G, H


def voo_de_impacto(T, t, rng):
    """O Voo de impacto: ele desce do alto à esquerda em velocidade supersônica — o corpo como um
    risco claro, o cone de vapor (os anéis achatados em volta da cabeça) e o rastro — e no contato o
    estrondo sônico: o clarão e o anel grande."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    f = ease_in(rel(t, 0.0, 0.28), 1.5)
    ax, ay = -0.95, -0.95
    hx, hy = ax + (0 - ax) * f, ay + (0 - ay) * f
    voando = 1 - rel(t, 0.28, 0.34)
    rastro = T.tapered([(ax, ay, hx + 1e-3, hy, 1.0)], 0.07) * voando
    ang = math.atan2(-ay, -ax)
    cone = T.zero()
    for j in range(3):
        r = 0.08 + 0.06 * j
        cx, cy = hx - math.cos(ang) * 0.06 * j, hy - math.sin(ang) * 0.06 * j
        cone += T.arc_band(r, 0.012, ang + math.pi / 2 + 0.3, ang + 3 * math.pi / 2 - 0.3, 1.0, 0.0, cx, cy, 0.5)
    cone *= voando
    k = pulso(t, 0.27, 0.6)
    clarao = T.gauss(0, 0, 0.25) * k * 2.0 + T.flare(0, 0, 1.4 * k + 1e-3, 0.8, 0.01) * k
    boom = T.ring(0.1 + 0.8 * ease_out(rel(t, 0.28, 0.75), 2), 0.03) * pulso(t, 0.28, 0.75)
    boom2 = T.ring(0.08 + 0.5 * ease_out(rel(t, 0.32, 0.75), 2), 0.02) * pulso(t, 0.32, 0.75)
    sub = np.random.default_rng(11)
    poeira = T.splats([(d * math.cos(a), d * math.sin(a), pulso(t, 0.28, 0.9) * sub.uniform(0.3, 0.8)) for a, d in ((sub.uniform(0, TAU), 0.1 + 0.6 * ease_out(rel(t, 0.28, 0.8), 2) * sub.uniform(0.4, 1)) for _ in range(18))], 0.03)
    G += (rastro * 1.1 + cone * 1.2 + clarao + boom * 1.2 + boom2 + poeira * 0.5) * env
    H += (rastro * 0.6 + clarao * 1.1 + boom * 0.4) * env
    return G, H


def sem_piedade(T, t, rng):
    """Sem piedade: a surra — seis pancadas, uma atrás da outra, em pontos diferentes do rival (cada
    uma com o seu clarão e o anel), o sangue espirrando, e a última, maior, no meio."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    pontos = [(-0.25, -0.15), (0.2, 0.1), (-0.1, 0.25), (0.25, -0.2), (-0.3, 0.1), (0.1, -0.05)]
    P = T.zero()
    for j, (x, y) in enumerate(pontos):
        t0 = 0.07 * j
        k = pulso(t, t0, t0 + 0.16)
        if k <= 0:
            continue
        P += T.gauss(x, y, 0.11) * k * 1.4 + T.ring(0.05 + 0.2 * rel(t, t0, t0 + 0.16), 0.02, x, y) * k
    k = pulso(t, 0.45, 0.85)
    final = T.gauss(0, 0, 0.26) * k * 2.0 + T.flare(0, 0, 1.4 * k + 1e-3, 0.3, 0.01) * k
    anel = T.ring(0.12 + 0.75 * ease_out(rel(t, 0.45, 0.85), 2), 0.04, 0, 0, 1.5) * k
    sangue = _sangue(T, t, 13, 22, 0.1, 0.7, -math.pi, math.pi, 0.02)
    G += (P + final + anel + sangue * 0.6) * env
    H += (P * 0.9 + final * 1.1 + sangue * 0.15) * env
    return G, H


# =================================================================== Guts
def matadora_guts(T, t, rng):
    """A Matadora de Dragões: o arco enorme e grosso, de ferro (brilho baixo, quase sem calor), vindo
    de cima à esquerda e descendo pesado; o borrão do movimento atrás, as faíscas no contato e o
    sangue espirrando para o lado do golpe."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    p = ease_in(rel(t, 0.0, 0.3), 1.4)
    a0 = -2.5
    a = a0 + 2.9 * p
    r = 0.62
    ferro = T.arc_band(r, 0.16, a - 0.6, a, 1.0, 0.0, -0.05, 0.0, 0.25) * (1 - rel(t, 0.32, 0.4))
    borrao = T.arc_band(r, 0.22, a0, a, 1.0, 0.0, -0.05, 0.0, 0.0) * (1 - rel(t, 0.3, 0.6))
    gume = T.arc_band(r + 0.08, 0.018, a - 0.6, a, 1.0, 0.0, -0.05, 0.0, 0.25) * (1 - rel(t, 0.32, 0.4))
    k = pulso(t, 0.2, 0.5)
    clarao = T.gauss(0.2, 0.1, 0.13) * k * 1.0
    q = np.random.default_rng(17)
    fa = T.splats([(0.2 + d * math.cos(b), 0.1 + d * math.sin(b), pulso(t, 0.2, 0.7) * q.uniform(0.4, 1)) for b, d in ((q.uniform(-0.8, 1.6), 0.05 + 0.5 * ease_out(rel(t, 0.2, 0.6), 2) * q.uniform(0.3, 1)) for _ in range(16))], 0.01)
    sangue = _sangue(T, t, 19, 20, 0.22, 0.8, -0.3, 1.4, 0.024)
    G += (ferro * 1.3 + borrao * 0.3 + gume * 1.2 + clarao + fa * 1.1 + sangue * 0.7) * env
    H += (gume * 0.5 + clarao * 0.8 + fa * 0.6 + sangue * 0.15) * env
    return G, H


def armadura_berserker(T, t, rng):
    """A Armadura Berserker fechando no Guts: as placas pontudas vêm de fora e apertam em volta dele, a
    fumaça escura sobe, e os dois olhos vermelhos do elmo acendem e ficam."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    fecha = ease_out(rel(t, 0.0, 0.4), 2.2)
    raio = 0.95 - 0.5 * fecha
    formas = []
    for k in range(10):
        a = TAU * k / 10 + 0.2
        cx, cy = raio * math.cos(a), raio * math.sin(a) * 0.95
        formas.append((lamina(cx * 0.7, cy * 0.7, cx * 1.35, cy * 1.35, 0.055), 1.0))
    placas = T.polys(formas, 0.004) * (0.6 + 0.4 * rel(t, 0.0, 0.4))
    estalo = T.ring(raio, 0.02) * pulso(t, 0.35, 0.6)
    n = np.roll(_ruido(T, 23, 0.06, 3), -int((t * 0.9 % 1) * T.H), axis=0)
    fumaca = np.clip(np.exp(-(T.RAD / 0.55) ** 2) * (0.6 + 0.6 * n) - 0.35, 0, 1) * rel(t, 0.1, 0.4)
    olhos = (T.gauss(-0.09, -0.12, 0.03) + T.gauss(0.09, -0.12, 0.03)) * rel(t, 0.38, 0.48) * (0.85 + 0.15 * math.sin(TAU * t * 4))
    G += (placas * 1.0 + estalo * 0.8 + fumaca * 0.5 + olhos * 2.0) * env
    H += (olhos * 2.2 + estalo * 0.3) * env
    return G, H


def ultimo_esforco(T, t, rng):
    """O Último esforço: a lâmina enorme cai de cima a baixo com tudo, o chão afunda em cratera (o anel
    achatado e as rachaduras), a poeira sobe e o sangue espirra."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    cai = ease_in(rel(t, 0.0, 0.22), 1.8)
    ponta = -1.0 + 1.45 * cai
    lamina_ = T.polys([(lamina(0.0, -1.0, 0.0, ponta + 1e-3, 0.16), 1.0)], 0.004) * (1 - rel(t, 0.3, 0.45))
    borrao = T.tapered([(0.0, -1.0, 0.0, ponta + 1e-3, 1.0)], 0.3) * (1 - rel(t, 0.22, 0.4)) * 0.35
    k = pulso(t, 0.2, 0.5)
    clarao = T.gauss(0, 0.45, 0.25, 0.1) * k * 1.8
    cratera = T.ring(0.1 + 0.7 * ease_out(rel(t, 0.2, 0.6), 2), 0.04, 0, 0.45, 4.0) * pulso(t, 0.2, 0.75)
    q = np.random.default_rng(29)
    rachas = T.zero()
    for _ in range(6):
        lado = 1 if q.uniform() < 0.5 else -1
        comp = (0.35 + 0.45 * q.uniform()) * ease_out(rel(t, 0.2, 0.35), 2)
        rachas += _raio(T, q, 0, 0.45, lado * comp + 1e-3, 0.45 + q.uniform(-0.1, 0.1) * comp, 0.012, 3, 0.15)
    rachas *= 1 - rel(t, 0.6, 0.95)
    sub = np.random.default_rng(31)
    poeira = T.splats([(sub.normal(0, 0.35), 0.45 - 0.5 * ease_out(rel(t, 0.22, 0.9), 2) * sub.uniform(0.2, 1), pulso(t, 0.22, 0.95) * sub.uniform(0.3, 0.7)) for _ in range(22)], 0.035)
    sangue = _sangue(T, t, 37, 18, 0.22, 0.7, -math.pi, 0.0, 0.022)
    G += (lamina_ * 1.2 + borrao + clarao + cratera + rachas * 1.1 + poeira * 0.45 + sangue * 0.6) * env
    H += (lamina_ * 0.5 + clarao * 1.0 + rachas * 0.5 + sangue * 0.15) * env
    return G, H


# =================================================================== Rick Sanchez
def portal_bala(T, t, rng):
    """O tiro da pistola de portal voando para +x: a bolha verde ondulando, com o miolo claro e as
    gotas ficando para trás."""
    G, H = vazio(T)
    cx = 0.3
    ang = np.arctan2(T.V, T.U - cx)
    r = np.hypot(T.U - cx, T.V)
    borda = 0.15 * (1 + 0.12 * np.sin(5 * ang + TAU * t * 2))
    bolha = np.clip(1 - r / borda, 0, 1) ** 0.6
    miolo = T.gauss(cx, 0, 0.06)
    sub = np.random.default_rng(41)
    gotas = T.splats([(cx - 0.2 - 0.7 * ((sub.uniform() + t * 1.5) % 1), sub.normal(0, 0.05), 1 - ((sub.uniform() + t * 1.5) % 1)) for _ in range(10)], 0.025)
    G += bolha * 1.1 + miolo * 1.2 + gotas * 0.7
    H += miolo * 1.2 + bolha * 0.3
    return G, H


def _portal(T, t, cx, cy, r, abre, giro, sq=0.55):
    """O portal do Rick: a borda grossa e ondulada, o redemoinho de braços curvos girando dentro e o
    brilho do meio."""
    U, V = T.U - cx, (T.V - cy) / sq
    rr = np.hypot(U, V)
    ang = np.arctan2(V, U)
    R = r * abre + 1e-3
    borda = np.exp(-((rr - R * (1 + 0.035 * np.sin(5 * ang + giro * 3) + 0.02 * np.sin(3 * ang - giro * 2))) / (0.035 + 0.02 * abre)) ** 2)
    dentro = np.clip(1 - rr / R, 0, 1)
    braco = (0.5 + 0.5 * np.sin(3 * ang + 10 * rr - giro * 4)) * dentro
    return borda, braco * 0.7 + dentro * 0.4


def portal_rick(T, t, rng):
    """A Pistola de portal no rival: o portal verde abre achatado sobre ele, gira, o estouro sai de
    dentro (o clarão e os raios curtos) e o portal fecha."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    abre = back(rel(t, 0.0, 0.2), 1.6) * (1 - ease_in(rel(t, 0.65, 0.85), 1.5))
    borda, miolo = _portal(T, t, 0, 0, 0.5, abre, TAU * t * 1.2)
    k = pulso(t, 0.25, 0.6)
    clarao = T.gauss(0, 0, 0.22) * k * 1.8
    raios = T.tapered([(0.05 * math.cos(a), 0.05 * math.sin(a), 0.55 * math.cos(a) + 1e-3, 0.4 * math.sin(a), 1.0) for a in np.linspace(0, TAU, 9)[:-1] + 0.3], 0.04) * k
    G += (borda * 1.2 + miolo * 0.6 + clarao + raios * 0.9) * env
    H += (borda * 0.4 + clarao * 1.1 + raios * 0.5) * env
    return G, H


def gadget_rick(T, t, rng):
    """A Invenção improvisada explodindo no meio dos rivais: o clarão verde, os raios estalando, as
    engrenagens e parafusos voando girando, a nuvem, e as espirais de quem ficou confuso."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    k = pulso(t, 0.0, 0.45)
    clarao = T.gauss(0, 0, 0.3) * k * 2.0 + T.flare(0, 0, 1.6 * k + 1e-3, 0.2, 0.008) * k
    nuvem = T.gauss(0, 0, 0.2 + 0.25 * ease_out(rel(t, 0.0, 0.5), 2)) * pulso(t, 0.0, 0.75) * 0.6
    anel = T.ring(0.12 + 0.8 * ease_out(rel(t, 0.0, 0.5), 2), 0.035, 0, 0, 1.4) * pulso(t, 0.0, 0.55)
    q = _quadro(t, 43)
    raios = T.zero()
    if t < 0.6:
        for _ in range(4):
            a = q.uniform(0, TAU)
            raios += _raio(T, q, 0, 0, 0.7 * math.cos(a), 0.5 * math.sin(a), 0.01, 4, 0.3)
        raios *= 1 - rel(t, 0.3, 0.6)
    sub = np.random.default_rng(47)
    formas = []
    for j in range(7):
        a = sub.uniform(0, TAU)
        d = 0.1 + 0.75 * ease_out(rel(t, 0.0, 0.7), 2) * sub.uniform(0.5, 1)
        cx, cy = d * math.cos(a), d * math.sin(a) + 0.2 * rel(t, 0.3, 1.0) ** 2
        rr = sub.uniform(0.04, 0.07)
        formas.append((estrela(cx, cy, rr, TAU * t * sub.uniform(1, 3), 8, 0.72), pulso(t, 0.02, 0.85)))
    eng = T.polys(formas, 0.003)
    espirais = T.zero()
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        g = TAU * t * 2 + j
        espirais += T.arc_band(0.09, 0.012, g, g + 5, 1.0, 0.0, x, -0.4, 0.5) * rel(t, 0.45, 0.6)
    G += (clarao + nuvem + anel + raios * 1.2 + eng * 1.1 + espirais) * env
    H += (clarao * 1.2 + raios * 0.8 + eng * 0.3) * env
    return G, H


def plano_b_faixa(T, t, rng):
    """O canhão de plasma do Plano B: o feixe verde grosso com o miolo claro, as bordas estalando em
    raios e os anéis correndo pelo feixe."""
    G, H = vazio(T)
    alto = T.H / T.W
    corpo = np.exp(-(T.V / (alto * 0.3)) ** 2)
    miolo = np.exp(-(T.V / (alto * 0.11)) ** 2)
    n = np.roll(_ruido(T, 53, 0.03, 2), int((t % 1) * T.W), axis=1)
    pulsa = 0.8 + 0.2 * n
    aneis = T.zero()
    for j in range(4):
        x = -0.95 + ((j / 4 + t) % 1) * 1.9
        aneis += np.exp(-((T.U - x) / 0.012) ** 2) * np.exp(-(T.V / (alto * 0.38)) ** 2)
    q = _quadro(t, 59)
    raios = T.zero()
    for _ in range(3):
        x = q.uniform(-0.8, 0.6)
        s = 1 if q.uniform() < 0.5 else -1
        raios += _raio(T, q, x, s * alto * 0.25, x + 0.3, s * alto * q.uniform(0.3, 0.45), 0.006, 3, 0.4)
    G += corpo * 0.9 * pulsa + miolo * 1.3 + aneis * 0.8 + raios * 0.9
    H += miolo * 1.4 + raios * 0.4
    return G, H


def plano_b(T, t, rng):
    """A explosão do Plano B no rival: o clarão enorme verde, a bola de plasma abrindo, dois anéis, os
    raios estalando e o X do golpe cortado."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    k = pulso(t, 0.0, 0.5)
    clarao = T.gauss(0, 0, 0.25) * k * 2.0 + T.flare(0, 0, 1.3 * k + 1e-3, 0.0, 0.01) * k
    bola = T.gauss(0, 0, 0.2 + 0.25 * ease_out(rel(t, 0.0, 0.45), 2)) * pulso(t, 0.0, 0.7) * 0.8
    a1 = T.ring(0.15 + 0.75 * ease_out(rel(t, 0.0, 0.5), 2), 0.04) * pulso(t, 0.0, 0.55)
    a2 = T.ring(0.1 + 0.5 * ease_out(rel(t, 0.08, 0.6), 2), 0.025) * pulso(t, 0.08, 0.6)
    q = _quadro(t, 61)
    raios = T.zero()
    if t < 0.55:
        for _ in range(5):
            a = q.uniform(0, TAU)
            raios += _raio(T, q, 0, 0, 0.75 * math.cos(a), 0.75 * math.sin(a), 0.01, 4, 0.3)
        raios *= 1 - rel(t, 0.3, 0.55)
    X = T.lines([(-0.22, -0.22, 0.22, 0.22, 1.0), (-0.22, 0.22, 0.22, -0.22, 1.0)], 0.05) * pulso(t, 0.4, 0.9)
    G += (clarao + bola + a1 + a2 + raios * 1.2 + X * 1.2) * env
    H += (clarao * 1.2 + bola * 0.5 + raios * 0.7 + X * 0.6) * env
    return G, H


REGISTRO = [
    ("soco_viltrumita", soco_viltrumita, GRANDE, "Omni-Man · o soco com as ondas de choque", False),
    ("voo_de_impacto", voo_de_impacto, GRANDE, "Omni-Man · o voo supersônico e o estrondo", False),
    ("sem_piedade", sem_piedade, GRANDE, "Omni-Man · a surra, pancada atrás de pancada", False),
    ("matadora_guts", matadora_guts, GRANDE, "Guts · o arco pesado da Matadora de Dragões", False),
    ("armadura_berserker", armadura_berserker, GRANDE, "Guts · a Armadura Berserker fechando", False),
    ("ultimo_esforco", ultimo_esforco, GRANDE, "Guts · a lâmina caindo e a cratera", False),
    ("portal_bala", portal_bala, MEDIA, "Rick · o tiro da pistola de portal (laço)", True),
    ("portal_rick", portal_rick, GRANDE, "Rick · o portal abrindo no rival", False),
    ("gadget_rick", gadget_rick, GRANDE, "Rick · a invenção explodindo no meio dos rivais", False),
    ("plano_b_faixa", plano_b_faixa, FAIXA, "Rick · o canhão de plasma (faixa, laço)", True),
    ("plano_b", plano_b, GRANDE, "Rick · a explosão do plasma", False),
]
