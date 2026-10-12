"""Ataques básicos com animação própria, lote r (personagens novos).

Jack Skellington, Úrsula, Deku, All Might, Bakugo, Todoroki, Mob, Rimuru, Ainz, Lelouch, Inuyasha, Sesshomaru,
Kenshin, Natsu e Erza: a mão de osso comprida, o tentáculo com ventosas e a tinta, o Full Cowl com os raios
verdes, o Detroit Smash com o vento, as explosões das palmas, o gelo que rompe o chão, a aura do Mob e o
empurrão, a lâmina d'água do slime, o círculo de magia negativa, o Geass no olho e o tiro, as cinco garras de
ferro, o chicote de luz com o veneno, o saque da sakabatō, o punho de fogo do dragão e as espadas da Erza em
roda.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio
from .basicos_a import _PUNHO, _move, _punho
from .basicos_k import _borda, _contorno, _estouro, _folha, _gira, _gotas
from .basicos_l import _estrelinhas
from .rodada13 import _chamas


def _raios_verdes(T, t, cx, cy, r, n, seed, intens=1.0):
    q = np.random.default_rng(int(t * 40) % 9 + seed)
    out = T.zero()
    for k in range(n):
        a = q.uniform(0, TAU)
        out += T.polyline(jagged(q, cx + r * 0.4 * math.cos(a), cy + r * 0.4 * math.sin(a), cx + r * math.cos(a + 0.5), cy + r * math.sin(a + 0.5), 3, 0.4), 0.01)
    return out * intens


# ================================================================== Jack Skellington
def mao_ossuda(T, t, rng):
    """A mão ossuda do Jack: a mão de esqueleto de dedos compridíssimos se estica da esquerda, agarra o rival e aperta
    (os dedos fechando), com a lua de Halloween atrás e os morceguinhos."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    lua = pulso(t, 0.0, 0.9)
    G += T.ring(0.15, 0.03, -0.55, -0.55) * lua * 0.5 + T.gauss(-0.55, -0.55, 0.13) * lua * 0.25
    estica = ease_out(rel(t, 0.0, 0.3), 2)
    fecha = ease_in(rel(t, 0.3, 0.45), 2)
    if estica > 0 and t < 0.75:
        some = 1 - rel(t, 0.6, 0.75)
        px = -0.95 + 0.75 * estica
        segs = [(-0.95, 0.05, px, 0.0, 1.0)]
        nos = []
        for k in range(5):
            a = (-0.6 + 0.3 * k) * (1 - 0.6 * fecha)
            j1 = (px + 0.18 * math.cos(a), 0.18 * math.sin(a))
            a2 = a + 0.9 * fecha * (1 if a < 0 else -1)
            j2 = (j1[0] + 0.16 * math.cos(a2), j1[1] + 0.16 * math.sin(a2))
            segs += [(px, 0.0, j1[0], j1[1], 1.0), (j1[0], j1[1], j2[0], j2[1], 1.0)]
            nos += [(j1[0], j1[1], 1.0), (j2[0], j2[1], 0.7)]
        G += T.lines(segs, 0.016) * 1.3 * some
        H += T.splats(nos, 0.012) * some
    g, h = _estouro(T, t, 0.4, 0.7, 0.05, 0, 0.25, 8, 3, 0.015)
    G += g * 0.8
    H += h * 0.7
    return G * env, H * env


# ================================================================== Úrsula
def tentaculo_de_ursula(T, t, rng):
    """O tentáculo da Úrsula: o tentáculo grosso de polvo (com as ventosas em fila) vem ondulando e chicoteia o rival,
    e a nuvem de tinta escura se espalha."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vai = ease_out(rel(t, 0.0, 0.3), 2)
    if vai > 0 and t < 0.6:
        some = 1 - rel(t, 0.45, 0.6)
        nos = []
        for j in range(30):
            u = j / 29 * vai
            nos.append((-0.95 + 0.95 * u, 0.4 * (1 - u) + 0.15 * math.sin(TAU * u * 1.5 + t * 8) * (1 - u)))
        cima, baixo = [], []
        for j, (x, y) in enumerate(nos):
            w = 0.09 * (1 - j / 30) + 0.015
            cima.append((x, y - w))
            baixo.append((x, y + w))
        C = T.polys([(cima + baixo[::-1], 1.0)])
        G += (C * 0.4 + _borda(T, C, 0.008) * 1.3) * some
        ventosas = [(nos[j][0], nos[j][1] + 0.04 * (1 - j / 30), 0.0) for j in range(2, len(nos) - 2, 3)]
        for x, y, _ in ventosas:
            G += T.ring(0.018 * (1 - x / 3), 0.006, x, y) * some * 1.1
    g, h = _estouro(T, t, 0.28, 0.55, 0, 0, 0.3, 8, 5)
    G += g
    H += h
    tinta = rel(t, 0.3, 1.0)
    if 0 < tinta < 1:
        q = np.random.default_rng(7)
        pts = [(q.uniform(-0.4, 0.4) * (0.4 + tinta), q.uniform(-0.3, 0.3) * (0.4 + tinta), (1 - tinta) * 0.6) for _ in range(16)]
        N = T.splats(pts, 0.07)
        G += _borda(T, np.clip(N, 0, 1), 0.03) * 0.8 + T.blur(N, 0.02) * 0.2
    return G * env, H * env


# ================================================================== Deku
def full_cowl(T, t, rng):
    """O soco do Deku: o Full Cowl acende (os raios verdes correndo pelo corpo e pelo punho), o soco avança e o "Smash"
    estoura com os raios saindo do ponto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vai = ease_in(rel(t, 0.1, 0.32), 2)
    if t < 0.5:
        x = -0.8 + 0.72 * vai
        P, nos = _punho(T, x, 0.0, 1.6)
        G += P * 0.6 + _borda(T, P, 0.006) * 1.1
        G += _raios_verdes(T, t, x, 0.0, 0.3, 5, 1) * 1.3
        G += _raios_verdes(T, t, -0.85, 0.15, 0.35, 4, 5) * pulso(t, 0.0, 0.3) * 1.1
    g, h = _estouro(T, t, 0.3, 0.65, 0.05, 0, 0.4, 10, 7)
    G += g
    H += h
    G += _raios_verdes(T, t, 0.05, 0, 0.5, 6, 9) * pulso(t, 0.3, 0.7) * 1.2
    return G * env, H * env


# ================================================================== All Might
def detroit_smash(T, t, rng):
    """O Detroit Smash do All Might: o punho enorme avança e a pressão do soco empurra o ar inteiro na frente (o cone
    de vento em camadas, as nuvens rasgando) e explode no rival."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    vai = ease_in(rel(t, 0.05, 0.3), 2.2)
    if t < 0.45:
        x = -0.85 + 0.55 * vai
        P, nos = _punho(T, x, 0.0, 2.6)
        G += P * 0.6 + _borda(T, P, 0.008) * 1.3
        H += nos * 0.5
    vento = rel(t, 0.25, 0.85)
    if 0 < vento < 1:
        for k in range(4):
            u = rel(vento, 0.08 * k, 0.6 + 0.08 * k)
            if 0 < u < 1:
                r = 0.2 + 0.9 * ease_out(u, 2)
                A = T.arc_band(r, 0.05 * (1 - u) + 0.01, -0.7, 0.7, cx=-0.45, cy=0.0, taper=0.0)
                G += A * (1 - u) * 1.3
        q = np.random.default_rng(11)
        riscos = []
        for _ in range(14):
            y = q.uniform(-0.6, 0.6)
            x0 = -0.3 + 1.3 * ease_out(vento, 2) * q.uniform(0.5, 1)
            riscos.append((x0 - 0.4, y * (0.3 + vento), x0, y * (0.3 + vento), 1 - vento))
        G += T.tapered(riscos, 0.02) * 1.1
    H += T.gauss(0, 0, 0.15) * pulso(t, 0.28, 0.5) * 2.0
    return G * env, H * env


# ================================================================== Bakugo
def explosao_de_bakugo(T, t, rng):
    """As explosões do Bakugo: a palma solta duas explosões seguidas (o estouro com as faíscas e a fumaça), uma de cada
    mão, em cima do rival."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    for k, (t0, dx, dy) in enumerate(((0.1, -0.05, -0.08), (0.32, 0.08, 0.06))):
        u = rel(t, t0, t0 + 0.4)
        if 0 < u < 1:
            b = ease_out(u, 3)
            H += T.gauss(dx, dy, 0.06 + 0.12 * b) * (1 - u) ** 2 * 2.0
            G += T.gauss(dx, dy, 0.12 + 0.2 * b) * (1 - u) * 1.2 + T.ring(0.06 + 0.35 * b, 0.03, dx, dy) * (1 - u) * 1.2
            q = np.random.default_rng(13 + k)
            fa = []
            for _ in range(12):
                a = q.uniform(0, TAU)
                d = (0.12 + 0.4 * b) * q.uniform(0.6, 1.1)
                fa.append((dx + d * 0.6 * math.cos(a), dy + d * 0.6 * math.sin(a), dx + d * math.cos(a), dy + d * math.sin(a), 1 - u))
            G += T.tapered(fa, 0.014) * 1.2
            fum = [(dx + q.uniform(-0.2, 0.2) * b, dy - 0.2 * u + q.uniform(-0.1, 0.1), (1 - u) * 0.5) for _ in range(8)]
            G += T.splats(fum, 0.06) * 0.6
    return G * env, H * env


# ================================================================== Todoroki
def gelo_e_fogo(T, t, rng):
    """O gelo do Todoroki: os espinhos de gelo rompem o chão em fila da esquerda até o rival (cada um maior que o
    anterior), e a chama do lado esquerdo dele tremula um instante."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    shapes = []
    for k in range(7):
        t0 = 0.05 + 0.05 * k
        sobe = back(rel(t, t0, t0 + 0.15), 1.5) * (1 - rel(t, 0.75, 0.95))
        if sobe <= 0:
            continue
        bx = -0.85 + 0.15 * k
        alt = (0.15 + 0.07 * k) * sobe
        shapes.append(([(bx - 0.06, 0.35), (bx + 0.06, 0.35), (bx + 0.02, 0.35 - alt)], 1.0))
        shapes.append(([(bx + 0.02, 0.35), (bx + 0.1, 0.35), (bx + 0.08, 0.35 - alt * 0.6)], 0.8))
    if shapes:
        E = T.polys(shapes)
        G += E * 0.5 + _borda(T, E, 0.005) * 1.4
        H += _borda(T, E, 0.003) * 0.4
    g, h = _estouro(T, t, 0.38, 0.65, 0.1, 0.05, 0.3, 8, 15, 0.015)
    G += g * 0.8
    H += h * 0.8
    chama = pulso(t, 0.0, 0.5)
    if chama > 0:
        F = _chamas(T, t, -0.85, -0.2, 0.06, 0.25, 3, 17)
        G += (F * 0.8 + T.blur(F, 0.015) * 0.4) * chama
    return G * env, H * env


# ================================================================== Mob
def empurrao_psiquico(T, t, rng):
    """O empurrão psíquico do Mob: a aura ondula em volta dele (os contornos tremendo), as pedrinhas flutuam, e a onda
    invisível empurra o rival com força."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    aura = pulso(t, 0.0, 0.6)
    if aura > 0:
        A = T.ring(0.22, 0.015, -0.7, 0.05, squash=0.6) + T.ring(0.28, 0.01, -0.7, 0.05, squash=0.6) * 0.6
        du = 0.025 * np.sin(T.V * 30 + t * 40)
        G += T.warp(A, du, du * 0) * aura * 1.2
        q = np.random.default_rng(19)
        pts = [(-0.7 + q.uniform(-0.35, 0.35), 0.3 - 0.3 * aura - q.uniform(0, 0.3) + 0.03 * math.sin(t * 10 + k), aura) for k in range(8)]
        G += T.splats(pts, 0.02) * 1.1
    onda = rel(t, 0.25, 0.75)
    if 0 < onda < 1:
        x = -0.5 + 0.6 * ease_out(onda, 2)
        A = T.arc_band(0.3 + 0.15 * onda, 0.05, -1.0, 1.0, cx=x - 0.3, cy=0.0, taper=0.0)
        du = 0.03 * np.sin(T.V * 25 + t * 30)
        G += T.warp(A, du, du * 0) * (1 - onda) * 1.3
    g, h = _estouro(T, t, 0.45, 0.75, 0.05, 0, 0.35, 9, 21)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Rimuru
def jato_do_slime(T, t, rng):
    """O jato do Rimuru: a gotinha de slime se forma (a bolha azul que balança), e dela sai a lâmina d'água em alta
    pressão — o traço fino e reto que corta o rival — e espirra."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    gota = pulso(t, 0.0, 0.55)
    if gota > 0:
        balanca = 1 + 0.15 * math.sin(t * 30)
        G += T.ring(0.1, 0.015, -0.75, 0.1, squash=balanca) * gota * 1.2 + T.gauss(-0.75, 0.1, 0.08) * gota * 0.4
        H += T.gauss(-0.78, 0.06, 0.02) * gota
    jato = rel(t, 0.18, 0.45)
    if 0 < jato < 1:
        vai = min(1, jato * 4)
        x1 = -0.65 + 0.8 * vai
        G += T.lines([(-0.65, 0.08, x1, -0.02, 1.0)], 0.018) * (1 - jato * 0.6) * 1.3
        H += T.lines([(-0.65, 0.08, x1, -0.02, 1.0)], 0.006) * (1 - jato * 0.6) * 1.4
    G += _gotas(T, t, 0.28, 0.55, 0.05, 0.0, 18, 0.5, 23, -1.0, 1.0, 0.016, 0.3) * 1.2
    g, h = _estouro(T, t, 0.25, 0.5, 0.05, 0, 0.22, 6, 25, 0.014)
    G += g * 0.7
    H += h * 0.7
    return G * env, H * env


# ================================================================== Ainz
def raio_negativo(T, t, rng):
    """O raio negativo do Ainz: o círculo de magia (dois anéis com as runas) se abre na mão de esqueleto, o raio de
    energia negativa escura dispara e o rival é envolto nas faíscas roxas que sugam."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    circ = pulso(t, 0.0, 0.55)
    if circ > 0:
        r = 0.2 * back(rel(t, 0.0, 0.2), 1.4)
        cx, cy = -0.7, 0.0
        G += (T.ring(r, 0.012, cx, cy, squash=0.5) + T.ring(r * 0.75, 0.008, cx, cy, squash=0.5)) * circ * 1.3
        runas = [(cx + r * 0.88 * math.cos(a), cy + r * 0.88 * math.sin(a) / 0.5 * 0.25, cx + r * 0.88 * math.cos(a) + 0.015, cy + r * 0.88 * math.sin(a) / 0.5 * 0.25 - 0.02, 1.0) for a in np.linspace(0, TAU, 12, endpoint=False) + t * 3]
        G += T.lines(runas, 0.008) * circ
    raio = rel(t, 0.18, 0.55)
    if 0 < raio < 1:
        vai = min(1, raio * 4)
        x1 = -0.7 + 0.7 * vai
        R = T.lines([(-0.7, 0.0, x1, 0.0, 1.0)], 0.05)
        G += _borda(T, R, 0.012) * 1.4 * (1 - raio * 0.5) + T.blur(R, 0.03) * 0.3
        H += T.lines([(-0.7, 0.0, x1, 0.0, 1.0)], 0.008) * 0.5 * (1 - raio)
    suga = rel(t, 0.3, 0.95)
    if 0 < suga < 1:
        q = np.random.default_rng(27)
        pts = []
        for _ in range(20):
            a = q.uniform(0, TAU)
            d = 0.45 * (1 - ((suga + q.uniform(0, 1)) % 1))
            pts.append((d * math.cos(a), d * math.sin(a), math.sin(math.pi * suga)))
        G += T.splats(pts, 0.016) * 1.2
        G += T.ring(0.12, 0.03, 0, 0) * math.sin(math.pi * suga) * 0.8
    return G * env, H * env


# ================================================================== Lelouch
def _geass(cx, cy, s):
    """O sinal do Geass: a ave estilizada (as duas asas em V e o corpo)."""
    return [(cx - 0.2 * s, cy - 0.05 * s, cx, cy + 0.1 * s, 1.0), (cx, cy + 0.1 * s, cx + 0.2 * s, cy - 0.05 * s, 1.0),
            (cx - 0.2 * s, cy - 0.05 * s, cx - 0.1 * s, cy - 0.12 * s, 1.0), (cx + 0.2 * s, cy - 0.05 * s, cx + 0.1 * s, cy - 0.12 * s, 1.0),
            (cx, cy + 0.1 * s, cx, cy + 0.2 * s, 1.0)]


def geass_tiro(T, t, rng):
    """O tiro do Lelouch: o sinal do Geass acende no olho (a ave vermelha que se abre), e a pistola dispara certeira
    no rival."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    geass = back(rel(t, 0.0, 0.2), 1.4) * (1 - rel(t, 0.45, 0.6))
    if geass > 0:
        G += T.lines(_geass(-0.6, -0.45, 1.4 * geass), 0.016) * 1.3
        H += T.gauss(-0.6, -0.43, 0.03) * geass * 1.4
        G += T.ring(0.25 * geass, 0.012, -0.6, -0.43) * 0.6
    cano = (-0.85, 0.05)
    c = pulso(t, 0.3, 0.4)
    H += T.flare(cano[0], cano[1], 0.3 * c + 0.01, 0, 0.012) * c * 1.4
    v = rel(t, 0.3, 0.38)
    if 0 < v and t < 0.55:
        x = cano[0] + (0.0 - cano[0]) * min(1, v)
        G += T.tapered([(cano[0], cano[1], x, cano[1] * (1 - min(1, v)), 1.0)], 0.016) * (1 - rel(t, 0.38, 0.55)) * 1.3
    g, h = _estouro(T, t, 0.37, 0.65, 0, 0, 0.25, 8, 29)
    G += g
    H += h
    return G * env, H * env


# ================================================================== Inuyasha
def garras_de_ferro(T, t, rng):
    """As garras de ferro do Inuyasha: os cinco rasgos de energia amarela das unhas cortam o rival de cima para baixo,
    abertos em leque."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    for k in range(5):
        t0 = 0.1 + 0.015 * k
        p = ease_out(rel(t, t0, t0 + 0.13), 3)
        ini = rel(t, t0 + 0.2, t0 + 0.55)
        if p > 0 and ini < 1:
            a = -1.9 + 0.12 * k
            dx = (k - 2) * 0.1
            x1, y1 = dx + 0.3, -0.5
            x2, y2 = dx - 0.25, 0.5
            L = T.polys([(lamina(x1, y1, x2, y2, 0.03, prog=p, inicio=ini), 1.0)])
            G += L * 1.4 + T.blur(L, 0.015) * 0.5
            H += L * 0.5
    g, h = _estouro(T, t, 0.18, 0.5, 0, 0, 0.25, 8, 31, 0.014)
    G += g * 0.7
    H += h * 0.6
    return G * env, H * env


# ================================================================== Sesshomaru
def chicote_de_luz(T, t, rng):
    """O chicote de luz do Sesshomaru: dos dedos sai o chicote de energia verde, longo e elegante, que estala no rival,
    e a névoa venenosa se solta."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vai = ease_out(rel(t, 0.0, 0.25), 2)
    if vai > 0 and t < 0.5:
        pts = []
        for j in range(40):
            u = j / 39 * vai
            pts.append((-0.85 + 0.9 * u, -0.3 * math.sin(math.pi * u * 1.1) + 0.08 * math.sin(TAU * u * 2 + t * 30) * (1 - u)))
        C = T.polyline(pts, 0.016)
        G += (C * 1.3 + T.blur(C, 0.015) * 0.6) * (1 - rel(t, 0.35, 0.5))
        H += T.polyline(pts, 0.005) * (1 - rel(t, 0.35, 0.5))
    g, h = _estouro(T, t, 0.25, 0.5, 0.05, 0, 0.25, 7, 33, 0.014)
    G += g
    H += h
    nevoa = rel(t, 0.3, 1.0)
    if 0 < nevoa < 1:
        q = np.random.default_rng(35)
        pts = [(q.uniform(-0.35, 0.35), q.uniform(-0.2, 0.2) - 0.2 * nevoa, math.sin(math.pi * nevoa) * 0.5) for _ in range(14)]
        G += T.splats(pts, 0.06) * 0.6
    return G * env, H * env


# ================================================================== Kenshin
def sakabato(T, t, rng):
    """O saque do Kenshin: a sakabatō sai da bainha num relâmpago (o batto rápido, a meia-lua fina e brilhante), com
    o brilho no fio virado ao contrário, e acerta o rival sem cortar — a pancada."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    saca = ease_out(rel(t, 0.12, 0.22), 3)
    if saca > 0 and t < 0.55:
        some = 1 - rel(t, 0.3, 0.55)
        A = T.arc_band(0.55, 0.05, -2.8, -2.8 + 2.6 * saca, cx=-0.15, cy=0.2, crescente=True)
        G += (A * 1.5 + T.blur(A, 0.015) * 0.6) * some
        H += _borda(T, A, 0.004) * 0.8 * some
    brilho = pulso(t, 0.0, 0.15)
    H += T.flare(-0.6, 0.15, 0.25 * brilho + 0.01, 0.785, 0.01) * brilho * 1.3
    g, h = _estouro(T, t, 0.2, 0.5, 0.15, -0.05, 0.3, 9, 37)
    G += g
    H += h
    cruz = pulso(t, 0.35, 0.8)
    if cruz > 0:
        G += T.lines([(-0.75, -0.55, -0.63, -0.45, 1.0), (-0.63, -0.55, -0.72, -0.43, 1.0)], 0.01) * cruz
    return G * env, H * env


# ================================================================== Natsu
def soco_flamejante_natsu(T, t, rng):
    """O punho de ferro do Dragão de Fogo: o punho do Natsu pega fogo inteiro (as chamas grandes saindo da mão),
    avança e explode no rival numa bola de fogo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    vai = ease_in(rel(t, 0.1, 0.32), 2)
    if t < 0.5:
        x = -0.8 + 0.72 * vai
        P, nos = _punho(T, x, 0.0, 1.6)
        G += P * 0.6 + _borda(T, P, 0.006) * 1.0
        F = _chamas(T, t, x - 0.05, 0.0, 0.12, 0.35, 6, 39, math.pi)
        G += F * 0.9 + T.blur(F, 0.02) * 0.6
        F2 = _chamas(T, t, x, -0.05, 0.1, 0.2, 4, 41)
        G += F2 * 0.8
    bum = rel(t, 0.3, 0.8)
    if 0 < bum < 1:
        b = ease_out(bum, 2.5)
        H += T.gauss(0.05, 0, 0.1 + 0.15 * b) * (1 - bum) ** 2 * 2.0
        F = _chamas(T, t, 0.05, 0.1, 0.25 * (0.5 + b), 0.4 * (1 - bum) + 0.05, 8, 43)
        G += F * 0.9 + T.blur(F, 0.02) * 0.5
        G += T.ring(0.1 + 0.4 * b, 0.03, 0.05, 0) * (1 - bum)
    return G * env, H * env


# ================================================================== Erza
def espadas_de_erza(T, t, rng):
    """As espadas da Erza: com o requip, as espadas aparecem em roda em volta dela, brilhando, e disparam todas juntas
    em cima do rival."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    surge = back(rel(t, 0.0, 0.2), 1.3)
    voa = ease_in(rel(t, 0.3, 0.48), 2)
    if surge > 0 and t < 0.55:
        cx, cy = -0.55, 0.0
        shapes = []
        for k in range(6):
            a = TAU * k / 6 + 0.5 * t
            sx, sy = cx + 0.35 * surge * math.cos(a), cy + 0.35 * surge * math.sin(a)
            x = sx + (0.0 - sx) * voa
            y = sy + (0.0 - sy) * voa
            ang = math.atan2(-y, -x) if voa > 0 else a + math.pi
            ux, uy = math.cos(ang), math.sin(ang)
            shapes.append((lamina(x - ux * 0.2, y - uy * 0.2, x + ux * 0.1, y + uy * 0.1, 0.025), 1.0))
            H += T.gauss(x - ux * 0.2, y - uy * 0.2, 0.012) * 0.8
        E = T.polys(shapes)
        G += (E * 1.0 + _borda(T, E, 0.004) * 0.8) * (1 - rel(t, 0.45, 0.55))
    g, h = _estouro(T, t, 0.47, 0.75, 0, 0, 0.35, 12, 45)
    G += g
    H += h
    return G * env, H * env


REGISTRO = [
    ("mao_ossuda", mao_ossuda, GRANDE, "Básico do Jack Skellington: a mão de osso agarrando", False),
    ("tentaculo_de_ursula", tentaculo_de_ursula, GRANDE, "Básico da Úrsula: o tentáculo e a tinta", False),
    ("full_cowl", full_cowl, GRANDE, "Básico do Deku: o Full Cowl e o soco", False),
    ("detroit_smash", detroit_smash, GRANDE, "Básico do All Might: o punho e o vento do Smash", False),
    ("explosao_de_bakugo", explosao_de_bakugo, GRANDE, "Básico do Bakugo: as duas explosões das palmas", False),
    ("gelo_e_fogo", gelo_e_fogo, GRANDE, "Básico do Todoroki: os espinhos de gelo e a chama", False),
    ("empurrao_psiquico", empurrao_psiquico, GRANDE, "Básico do Mob: a aura e a onda", False),
    ("jato_do_slime", jato_do_slime, GRANDE, "Básico do Rimuru: a gota e a lâmina d'água", False),
    ("raio_negativo", raio_negativo, GRANDE, "Básico do Ainz: o círculo e o raio negativo", False),
    ("geass_tiro", geass_tiro, GRANDE, "Básico do Lelouch: o Geass e o tiro", False),
    ("garras_de_ferro", garras_de_ferro, GRANDE, "Básico do Inuyasha: as cinco garras", False),
    ("chicote_de_luz", chicote_de_luz, GRANDE, "Básico do Sesshomaru: o chicote de luz e o veneno", False),
    ("sakabato", sakabato, GRANDE, "Básico do Kenshin: o saque da sakabatō", False),
    ("soco_flamejante_natsu", soco_flamejante_natsu, GRANDE, "Básico do Natsu: o punho de fogo", False),
    ("espadas_de_erza", espadas_de_erza, GRANDE, "Básico da Erza: as espadas em roda", False),
]
