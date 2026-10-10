"""As habilidades do Charizard e do Mega Man, desenhadas para eles.

Pedido do jogador: "faz as três habilidades do Charizard, do Mega Man e do
Super-Homem. Muito bem feita… se for de perto, é perto; se for de longe, é
longe; se for projétil, é projétil, saindo do personagem".

Charizard
- chamas_faixa: o jato de fogo saindo da boca dele até o rival, abrindo e
  ondulando (faixa, laço).
- lanca_chamas_impacto: o fogo batendo no rival — as línguas de chama subindo,
  as brasas e a fumaça.
- garra_de_dragao: as três garras de energia de dragão rasgando de cima para
  baixo, com as brasas.
- fogo_no_peito: o fogo juntando na boca dele no Preparo (laço).
- bola_do_charizard: a bola de fogo voando com a cauda de chamas (laço, viagem).
- explosao_de_fogo: a explosão em cinco braços (a estrela de fogo do
  Charizard) que cresce no rival e vira fumaça.

Mega Man
- buster_bala: os três tiros do Mega Buster voando em fila (laço, viagem).
- buster_impacto: os três estouros pequenos, um depois do outro.
- troca_de_arma: os quadradinhos de dados juntando no braço e o clarão da
  troca de cor (nele).
- raio_copiado: a esfera elétrica da arma copiada voando (laço, viagem).
- raio_copiado_impacto: a esfera estoura em raios e fica crepitando.
- buster_carga: a carga do Buster juntando — as linhas entrando e os anéis
  girando (Preparo, laço).
- carga_maxima_bala: o tiro carregado, grande, com a frente em meia-lua
  (laço, viagem).
- carga_maxima_impacto: a explosão grande do tiro carregado.
"""
from __future__ import annotations

import math

import numpy as np

from .base import FAIXA, GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _quadro(t, seed=0):
    return np.random.default_rng(seed + int(t * 997) % 9973)


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _lingua(cx, cy, larg, alto, fase, ang=-math.pi / 2, n=12):
    """Uma língua de chama: larga na base, ondulando até a ponta fina (aponta para `ang`)."""
    esq, dir_ = [], []
    for k in range(n + 1):
        f = k / n
        w = larg * (1 - f) ** 0.8 * (0.6 + 0.4 * math.sin(math.pi * min(1, f * 1.6)))
        torce = 0.25 * larg * math.sin(TAU * (f * 1.2 + fase)) * f
        esq.append((torce - w, alto * f))
        dir_.append((torce + w, alto * f))
    pts = esq + dir_[::-1]
    return _gira([(y, x) for x, y in pts], ang, cx, cy)  # (ao longo, de lado), girado para `ang`


_RUIDOS: dict = {}


def _ruido(T, seed, escala=0.06, oitavas=3):
    """Ruído suave guardado (o mesmo para todos os quadros, para poder rolar sem tremer)."""
    chave = (T.W, T.H, seed, escala, oitavas)
    if chave not in _RUIDOS:
        _RUIDOS[chave] = T.noise(np.random.default_rng(seed), escala, oitavas)
    return _RUIDOS[chave]


def _fogo(T, t, cx, base, larg, altura, seed, vel=1.2):
    """Fogo de verdade subindo de uma base: o ruído rola para cima com o tempo e "come" a borda
    das chamas; mais forte embaixo, some no alto. Devolve (fogo, miolo)."""
    up = base - T.V
    env_x = np.exp(-((T.U - cx) / larg) ** 2)
    n = np.roll(_ruido(T, seed), -int((t * vel % 1) * T.H), axis=0)
    n2 = np.roll(_ruido(T, seed + 1, 0.025, 2), -int((t * vel * 1.7 % 1) * T.H), axis=0)
    corpo = np.clip(1 - up / altura, 0, 1) * (up > -0.04) * np.clip((up + 0.04) / 0.06, 0, 1)
    base_f = env_x * corpo
    f = np.clip(base_f * (1.35 + 0.45 * n + 0.25 * n2) - 0.3 * (1 - corpo) - 0.15, 0, 1) ** 1.2
    return f, f ** 3


def _brasas(T, t, seed, n, cx=0.0, cy=0.0, espalha=0.5, sobe=0.6, tam=0.012):
    sub = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        f = (sub.uniform() + t * sub.uniform(0.8, 1.4)) % 1
        x = cx + sub.normal(0, espalha * 0.5) + 0.08 * math.sin(TAU * (f * 2 + sub.uniform()))
        pts.append((x, cy - sobe * f, (1 - f) * sub.uniform(0.4, 1)))
    return T.splats(pts, tam)


# =================================================================== Charizard
def chamas_faixa(T, t, rng):
    """O jato do Lança-chamas: sai fino da boca do Charizard (−x) e abre até o rival (+x), com o
    fogo ondulando (o ruído correndo junto com o jato) e o miolo mais claro."""
    G, H = vazio(T)
    alto = T.H / T.W
    f = (T.U + 1) / 2                          # 0 na boca, 1 no rival
    larg = alto * (0.12 + 0.75 * f ** 0.8)
    q = np.random.default_rng(7)
    ru = T.noise(q, 0.05, 3)
    # o ruído "corre" para a frente: desloca em x conforme o tempo
    desl = int((t * 0.5 % 1) * T.W)
    ru = np.roll(ru, desl, axis=1)
    ondula = 0.12 * alto * np.sin(TAU * (f * 3 - t * 2))
    d = np.abs(T.V - ondula) / larg
    jato = np.clip(1.15 - d + 0.35 * ru, 0, 1) ** 1.5
    miolo = np.clip(1 - d * 2.2 + 0.2 * ru, 0, 1) ** 1.5 * (1 - 0.4 * f)
    boca = T.gauss(-0.95, 0, 0.05, alto * 0.25)
    G += jato * 1.2 + miolo * 0.8 + boca
    H += miolo * 1.3 + boca * 0.9 + jato * 0.25
    return G, H


def lanca_chamas_impacto(T, t, rng):
    """O fogo batendo no rival (vem de −x): o clarão, as línguas de chama subindo do corpo dele, as
    brasas pulando e a fumaça no fim."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    k = pulso(t, 0.0, 0.3)
    clarao = T.gauss(-0.1, 0, 0.25) * k * 1.4
    respingo = T.zero()
    sub = np.random.default_rng(31)
    for _ in range(10):
        a = sub.normal(0, 0.6)
        comp = 0.4 * ease_out(rel(t, 0.0, 0.3), 2) * sub.uniform(0.5, 1)
        respingo += T.tapered([(-0.1, 0, -0.1 + comp * math.cos(a) + 1e-3, comp * math.sin(a), 1.0)], 0.05)
    respingo *= 1 - rel(t, 0.2, 0.45)
    vive = rel(t, 0.05, 0.25) * (1 - rel(t, 0.65, 0.95))
    chamas, miolo = _fogo(T, t, 0.0, 0.45, 0.32, 0.9 * (0.5 + 0.5 * vive), 33)
    chamas, miolo = chamas * vive, miolo * vive
    fumaca = T.splats([(np.random.default_rng(j).normal(0, 0.2), -0.2 - 0.5 * rel(t, 0.5, 1.0) - 0.04 * j, 0.8) for j in range(8)], 0.09) * pulso(t, 0.5, 1.0) * 0.5
    G += (clarao + respingo * 1.1 + chamas * 1.2 + T.blur(chamas, 0.03) * 0.5 + _brasas(T, t, 35, 18, 0, 0.3, 0.6, 0.9) + fumaca) * env
    H += (clarao * 1.1 + respingo * 0.6 + miolo * 1.2) * env
    return G, H


def garra_de_dragao(T, t, rng):
    """Garra de dragão: a mão do Charizard acende e as três garras de energia rasgam o rival na
    diagonal, uma depois da outra, deixando o rastro de fogo e as brasas."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    acende = pulso(t, 0.0, 0.22)
    G += T.gauss(-0.55, -0.55, 0.12) * acende * 1.3
    H += T.gauss(-0.55, -0.55, 0.05) * acende
    garras = T.zero()
    for j, off in enumerate((-0.2, 0.0, 0.2)):
        ini = 0.1 + 0.05 * j
        prog = ease_out(rel(t, ini, ini + 0.14), 2)
        come = rel(t, ini + 0.18, ini + 0.55)
        if prog <= 0:
            continue
        garras += T.polys([(lamina(-0.6 + off, -0.65 - off * 0.3, 0.55 + off, 0.6 - off * 0.3, 0.06, prog, come), 1.0)], 0.004)
    rastro = T.blur(garras, 0.03)
    k = pulso(t, 0.15, 0.5)
    clarao = T.gauss(0, 0, 0.22) * k * 1.2
    vive = pulso(t, 0.25, 0.95)
    chamas, miolo = _fogo(T, t, 0.05, 0.35, 0.25, 0.55, 41)
    chamas, miolo = chamas * vive, miolo * vive
    G += (garras * 1.4 + rastro * 1.1 + clarao + chamas * 0.9 + _brasas(T, t, 43, 22, 0, 0.2, 0.8, 0.9)) * env
    H += (garras * 1.1 + clarao * 0.9 + miolo) * env
    return G, H


def fogo_no_peito(T, t, rng):
    """O fogo juntando na boca do Charizard: a bola de fogo pulsando e as chamas girando para dentro
    dela."""
    G, H = vazio(T)
    pul = 0.85 + 0.15 * math.sin(TAU * t * 4)
    bola = T.gauss(0, 0, 0.17 * pul)
    sub = np.random.default_rng(51)
    fa = []
    for _ in range(60):
        a0 = sub.uniform(0, TAU)
        f = (sub.uniform() + t * sub.uniform(1.2, 2.0)) % 1
        r = 0.85 * (1 - f) + 0.1
        a = a0 + 2.5 * f
        fa.append((r * math.cos(a), r * math.sin(a), f ** 0.6 * sub.uniform(0.4, 1)))
    F = T.splats(fa, 0.016) + T.blur(T.splats(fa, 0.01), 0.02) * 0.6
    chamas, _ = _fogo(T, t, 0, 0.12, 0.13, 0.4, 53, 1.8)
    G += bola * 1.6 + F * 0.8 + chamas + T.ring(0.2, 0.05) * 0.3
    H += bola * 1.6 + F * 0.3
    return G, H


def bola_do_charizard(T, t, rng):
    """A bola de fogo voando para +x: o miolo claro, a cauda de chamas para trás, ondulando, e as
    brasas soltando."""
    G, H = vazio(T)
    nucleo = T.gauss(0.35, 0, 0.13)
    atras = np.clip(0.35 - T.U, 0, None)               # distância para trás da bola
    larg = 0.1 + 0.25 * atras
    n = np.roll(_ruido(T, 63, 0.05, 3), int((t % 1) * T.W), axis=1)
    corpo = np.exp(-(T.V / larg) ** 2) * np.clip(1 - atras / 1.0, 0, 1)
    cauda = np.clip(corpo * (1.3 + 0.5 * n) - 0.2, 0, 1) * (T.U < 0.4)
    G += nucleo * 1.6 + cauda * 1.1 + T.blur(cauda, 0.02) * 0.4 + _brasas(T, t, 61, 14, -0.25, 0.0, 0.3, -0.1, 0.012) * 0.8
    H += nucleo * 1.5 + cauda ** 3 * 0.8
    return G, H


def explosao_de_fogo(T, t, rng):
    """A Explosão de fogo: a bola bate e abre a estrela de cinco braços de fogo (um para cima, dois
    para os lados e dois para baixo), que cresce, queima um tempo e vira fumaça."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    k = pulso(t, 0.0, 0.25)
    clarao = T.gauss(0, 0, 0.3) * k * 2.0 + T.flare(0, 0, 1.3 * k + 1e-3, 0.4, 0.01) * k
    abre = back(rel(t, 0.05, 0.35), 1.4)
    angs = (-math.pi / 2, math.pi * 0.03, math.pi * 0.97, math.pi * 0.64, math.pi * 0.36)
    n = np.roll(_ruido(T, 71, 0.05, 3), -int((t * 0.8 % 1) * T.H), axis=0)
    braços = T.zero()
    for j, a in enumerate(angs):
        comp = 0.78 * abre * (0.9 if j == 0 else 1.0)
        if comp <= 0.01:
            continue
        ao_longo = T.U * math.cos(a) + T.V * math.sin(a)
        de_lado = -T.U * math.sin(a) + T.V * math.cos(a)
        f = np.clip(ao_longo / comp, 0, 1.2)
        w = 0.15 * (1 - 0.55 * f) + 0.02
        braços = np.maximum(braços, np.exp(-(de_lado / w) ** 2) * np.clip(1.15 - f, 0, 1) * (ao_longo > -0.05))
    queima = 1 - rel(t, 0.6, 0.85)
    braços = np.clip(braços * (1.35 + 0.45 * n) - 0.15, 0, 1) * queima
    miolo = T.gauss(0, 0, 0.16) * (0.6 + 0.4 * queima) * rel(t, 0.05, 0.15)
    sub = np.random.default_rng(73)
    fumaca = T.splats([(sub.normal(0, 0.3), sub.normal(0, 0.25) - 0.3 * rel(t, 0.55, 1.0), 0.7) for _ in range(12)], 0.09) * pulso(t, 0.55, 1.0) * 0.6
    anel = T.ring(0.2 + 0.7 * ease_out(rel(t, 0.02, 0.45), 2), 0.04) * pulso(t, 0.02, 0.5)
    G += (clarao + braços * 1.3 + miolo * 1.2 + fumaca + anel * 0.8 + _brasas(T, t, 75, 26, 0, 0.3, 0.9, 0.9)) * env
    H += (clarao * 1.1 + braços ** 3 * 1.1 + miolo * 1.2 + anel * 0.3) * env
    return G, H


# =================================================================== Mega Man
def buster_bala(T, t, rng):
    """Os três tiros do Mega Buster voando em fila para +x: cada um uma bolinha clara e achatada com
    um risco curto atrás."""
    G, H = vazio(T)
    for j, x in enumerate((0.55, 0.05, -0.45)):
        osc = 0.03 * math.sin(TAU * (t * 2 + j * 0.3))
        b = T.gauss(x, osc, 0.09, 0.06)
        risco = T.tapered([(x - 0.4, osc, x, osc, 1.0)], 0.07)
        G += b * 1.6 + risco * 0.6
        H += T.gauss(x, osc, 0.05, 0.035) * 1.6 + risco * 0.2
    return G, H


def buster_impacto(T, t, rng):
    """Os três tiros estourando no rival, um depois do outro, cada um com o seu anelzinho e as
    faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    for j, (x, y) in enumerate(((-0.1, -0.12), (0.05, 0.1), (0.15, -0.02))):
        ini = 0.12 * j
        k = pulso(t, ini, ini + 0.3)
        G += (T.gauss(x, y, 0.14) * k * 1.4 + T.flare(x, y, 0.6 * k + 1e-3, 0.3 * j, 0.012) * k
              + T.ring(0.05 + 0.3 * ease_out(rel(t, ini, ini + 0.35), 2), 0.025, x, y) * k) * env
        H += T.gauss(x, y, 0.06) * k * 1.4 * env
        sub = np.random.default_rng(80 + j)
        fa = []
        for _ in range(8):
            a = sub.uniform(-1.2, 1.2) + (0 if j % 2 else math.pi * 0.1)
            d = 0.05 + 0.35 * ease_out(rel(t, ini, ini + 0.4), 2) * sub.uniform(0.4, 1)
            fa.append((x + d * math.cos(a), y + d * math.sin(a), pulso(t, ini, ini + 0.45) * sub.uniform(0.5, 1)))
        G += T.splats(fa, 0.01) * 1.2 * env
    return G, H


def troca_de_arma(T, t, rng):
    """A troca de arma no braço do Mega Man: os quadradinhos de dados vindo de todo lado até o
    braço, o anel que fecha e o clarão da cor nova."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    sub = np.random.default_rng(91)
    quadrados = []
    for _ in range(26):
        a = sub.uniform(0, TAU)
        d0 = sub.uniform(0.45, 0.95)
        f = ease_in(rel(t, sub.uniform(0, 0.2), 0.55), 1.5)
        d = d0 * (1 - f)
        x, y = d * math.cos(a), d * math.sin(a)
        s = 0.035 * sub.uniform(0.6, 1.2)
        quadrados.append(([(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)], (1 - rel(t, 0.5, 0.6)) * sub.uniform(0.5, 1)))
    Q = T.polys(quadrados, 0.003)
    anel = T.ring(0.7 * (1 - ease_out(rel(t, 0.2, 0.55), 2)) + 0.08, 0.02) * pulso(t, 0.2, 0.6)
    k = pulso(t, 0.5, 0.85)
    clarao = T.gauss(0, 0, 0.2) * k * 1.8 + T.flare(0, 0, 0.9 * k + 1e-3, 0.0, 0.012) * k
    G += (Q * 1.2 + anel * 1.2 + clarao) * env
    H += (Q * 0.4 + clarao * 1.1) * env
    return G, H


def _arco(T, q, x1, y1, x2, y2, larg=0.01, depth=4, rough=0.35):
    return T.polyline(jagged(q, x1, y1, x2, y2, depth, rough), larg)


def raio_copiado(T, t, rng):
    """A arma copiada: a esfera elétrica voando para +x, os arcos pulando dela a cada quadro e o
    rastro de faíscas."""
    G, H = vazio(T)
    q = _quadro(t, 101)
    cx = 0.3
    esfera = T.gauss(cx, 0, 0.14) * (0.9 + 0.1 * math.sin(TAU * t * 8))
    R = T.zero()
    for _ in range(5):
        a = q.uniform(0, TAU)
        comp = q.uniform(0.18, 0.35)
        R += _arco(T, q, cx, 0, cx + comp * math.cos(a), comp * math.sin(a), 0.01, 3, 0.4)
    sub = np.random.default_rng(103)
    fa = []
    for _ in range(14):
        f = (sub.uniform() + t * 2) % 1
        fa.append((cx - 0.9 * f, sub.normal(0, 0.06) * (1 + f), (1 - f) * sub.uniform(0.4, 1)))
    G += esfera * 1.6 + R * 1.2 + T.blur(R, 0.02) * 0.6 + T.splats(fa, 0.012)
    H += T.gauss(cx, 0, 0.07) * 1.6 + R * 0.8
    return G, H


def raio_copiado_impacto(T, t, rng):
    """A esfera estoura no rival: o clarão, os raios abrindo em volta, o anel elétrico e o choque
    que continua crepitando nele um tempo (a lentidão)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    q = _quadro(t, 111)
    k = pulso(t, 0.0, 0.4)
    clarao = T.gauss(0, 0, 0.24) * k * 1.8 + T.flare(0, 0, 1.2 * k + 1e-3, 0.2, 0.01) * k
    R = T.zero()
    for j in range(7):
        a = TAU * j / 7 + q.uniform(-0.3, 0.3)
        comp = q.uniform(0.35, 0.7) * (0.6 + 0.4 * k)
        R += _arco(T, q, 0, 0, comp * math.cos(a), comp * math.sin(a), 0.012, 4, 0.35)
    R *= 1 - rel(t, 0.35, 0.55)
    crepita = T.zero()
    if 0.35 < t < 0.85:
        for _ in range(3):
            a = q.uniform(0, TAU)
            crepita += _arco(T, q, 0.2 * math.cos(a), 0.25 * math.sin(a), 0.3 * math.cos(a + 1), 0.35 * math.sin(a + 1), 0.008, 3, 0.4)
    anel = T.ring(0.12 + 0.6 * ease_out(rel(t, 0.0, 0.5), 2), 0.03) * pulso(t, 0.0, 0.55)
    G += (clarao + R * 1.3 + T.blur(R, 0.02) * 0.8 + crepita * 1.1 + anel) * env
    H += (clarao * 1.1 + R * 0.9 + crepita * 0.7 + anel * 0.3) * env
    return G, H


def buster_carga(T, t, rng):
    """A carga do Mega Buster: a bola de energia crescendo no cano, as linhas de luz entrando de
    todos os lados e os dois anéis girando em volta dela (em pé e deitado)."""
    G, H = vazio(T)
    pul = 0.85 + 0.15 * math.sin(TAU * t * 6)
    bola = T.gauss(0, 0, 0.14 * pul)
    sub = np.random.default_rng(121)
    linhas = []
    for j in range(12):
        a = TAU * j / 12 + sub.uniform(-0.2, 0.2)
        f = (sub.uniform() + t * 2) % 1
        r1 = 0.85 * (1 - f) + 0.18
        r2 = r1 - 0.2
        linhas.append((r1 * math.cos(a), r1 * math.sin(a), max(r2, 0.15) * math.cos(a), max(r2, 0.15) * math.sin(a), f))
    L = T.tapered(linhas, 0.025)
    a1 = T.arc_band(0.28, 0.025, TAU * t * 2, TAU * t * 2 + 4.5, 0.35, 0.0)
    a2 = T.arc_band(0.28, 0.025, -TAU * t * 2, -TAU * t * 2 + 4.5, 0.35, math.pi / 2)
    G += bola * 1.7 + L * 0.9 + (a1 + a2) * 1.1
    H += bola * 1.7 + (a1 + a2) * 0.4
    return G, H


def carga_maxima_bala(T, t, rng):
    """O tiro carregado voando para +x: a bola grande e clara, a frente em meia-lua (a onda de
    energia empurrando o ar) e a cauda larga que pisca."""
    G, H = vazio(T)
    cx = 0.3
    bola = T.gauss(cx, 0, 0.19)
    frente = T.arc_band(0.27, 0.035, -1.2, 1.2, 1.0, 0.0, cx - 0.05, 0.0, 1.0, True)
    cauda = T.tapered([(cx - 0.95, 0.0, cx, 0.0, 1.0)], 0.36) * (0.8 + 0.2 * math.sin(TAU * t * 6))
    risca = T.tapered([(cx - 0.8, y, cx - 0.1, y * 0.6, 1.0) for y in (-0.16, 0.16)], 0.02)
    G += bola * 1.8 + frente * 1.3 + T.blur(cauda, 0.02) * 0.9 + risca * 0.8
    H += T.gauss(cx, 0, 0.1) * 1.8 + frente * 0.5 + cauda * 0.25
    return G, H


def carga_maxima_impacto(T, t, rng):
    """A explosão do tiro carregado: o clarão enorme, os raios de luz retos saindo, dois anéis (um
    rápido, um lento) e as faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    k = pulso(t, 0.0, 0.45)
    clarao = T.gauss(0, 0, 0.35) * k * 2.0 + T.flare(0, 0, 1.6 * k + 1e-3, 0.0, 0.009) * k
    raios = T.zero()
    sub = np.random.default_rng(131)
    for j in range(10):
        a = TAU * j / 10 + sub.uniform(-0.15, 0.15)
        comp = (0.5 + 0.4 * sub.uniform()) * ease_out(rel(t, 0.0, 0.3), 2)
        raios += T.tapered([(0.05 * math.cos(a), 0.05 * math.sin(a), comp * math.cos(a) + 1e-3, comp * math.sin(a), 1.0)], 0.05)
    raios *= 1 - rel(t, 0.2, 0.5)
    a1 = T.ring(0.1 + 0.8 * ease_out(rel(t, 0.0, 0.35), 2), 0.04) * pulso(t, 0.0, 0.4)
    a2 = T.ring(0.1 + 0.5 * ease_out(rel(t, 0.1, 0.8), 2), 0.06) * pulso(t, 0.1, 0.85) * 0.6
    fa = []
    for _ in range(24):
        a = sub.uniform(0, TAU)
        d = 0.1 + 0.8 * ease_out(rel(t, 0.02, 0.75), 2) * sub.uniform(0.3, 1)
        fa.append((d * math.cos(a), d * math.sin(a), pulso(t, 0.02, 0.85) * sub.uniform(0.4, 1)))
    G += (clarao + raios * 1.2 + a1 * 1.2 + a2 + T.splats(fa, 0.012) * 1.2) * env
    H += (clarao * 1.2 + raios * 0.6 + a1 * 0.4) * env
    return G, H


REGISTRO = [
    ("chamas_faixa", chamas_faixa, FAIXA, "Charizard · o jato do Lança-chamas até o rival (faixa)", True),
    ("lanca_chamas_impacto", lanca_chamas_impacto, GRANDE, "Charizard · o fogo batendo e as chamas subindo no rival", False),
    ("garra_de_dragao", garra_de_dragao, GRANDE, "Charizard · as três garras de dragão rasgando", False),
    ("fogo_no_peito", fogo_no_peito, MEDIA, "Charizard · o fogo juntando na boca no Preparo (laço)", True),
    ("bola_do_charizard", bola_do_charizard, MEDIA, "Charizard · a bola de fogo voando (laço)", True),
    ("explosao_de_fogo", explosao_de_fogo, GRANDE, "Charizard · a estrela de fogo de cinco braços", False),
    ("buster_bala", buster_bala, MEDIA, "Mega Man · os três tiros do Buster voando (laço)", True),
    ("buster_impacto", buster_impacto, GRANDE, "Mega Man · os três tiros estourando", False),
    ("troca_de_arma", troca_de_arma, MEDIA, "Mega Man · os dados juntando no braço e a troca de cor", False),
    ("raio_copiado", raio_copiado, MEDIA, "Mega Man · a esfera elétrica da arma copiada voando (laço)", True),
    ("raio_copiado_impacto", raio_copiado_impacto, GRANDE, "Mega Man · a esfera estoura e fica crepitando", False),
    ("buster_carga", buster_carga, MEDIA, "Mega Man · a carga do Buster juntando (laço)", True),
    ("carga_maxima_bala", carga_maxima_bala, MEDIA, "Mega Man · o tiro carregado voando (laço)", True),
    ("carga_maxima_impacto", carga_maxima_impacto, GRANDE, "Mega Man · a explosão do tiro carregado", False),
]
