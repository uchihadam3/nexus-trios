"""As habilidades do Sasuke, do Homem-Aranha, do Trunks e do Kuririn, desenhadas para eles.

Sasuke
- chidori_sasuke_mao: o Chidori na mão — o raio cantando como pássaros, os
  estalos compridos para trás (Preparo, laço).
- chidori_sasuke: a lança de raio atravessando o rival e saindo pelas costas.
- mangekyo_sasuke: o Mangekyō do Sasuke acendendo nele (nele).
- amaterasu: as chamas negras pegando no rival — só a borda clara das chamas, o
  miolo escuro, e elas não se apagam.
- genjutsu_sasuke: o Sharingan gigante girando sobre o rival e as espirais
  que o deixam confuso.

Homem-Aranha
- teia_voando: a bola de teia girando no ar (laço, viagem).
- teia_prende: a rede de teia abrindo e grudando no rival (raios e anéis).
- salvamento_aranha: ele chega balançando na teia (o arco) e a teia cobre o
  aliado como um escudo.
- teia_impacto_bola: o tiro de teia grosso voando (laço, viagem).
- teia_de_impacto: o tiro estoura no rival em fios e corta o golpe (X).

Trunks
- espada_do_futuro: a espada cortando o rival muitas vezes em grade, rápido, e
  todos os cortes brilhando juntos no fim.
- selo_burning: os gestos rápidos das mãos do Burning Attack (nele).
- burning_bola: a bola de ki do Burning Attack voando (laço, viagem).
- burning_attack: a explosão da bola de ki.
- aura_trunks: a aura dourada de Super Saiyajin subindo (Preparo, laço).
- corte_final: o corte vertical gigante de cima a baixo, a luz rachando ao
  meio e as duas metades se afastando.

Kuririn
- kienzan_disco: o disco serrilhado e fininho girando (laço, viagem).
- kienzan_corte: o disco atravessando o rival — o corte fino e as faíscas.
- taiyoken_flash: as mãos no rosto acendendo (nele).
- taiyoken: o clarão solar enorme no campo dos rivais, com os raios e as
  espirais de quem ficou cego.
- kame_kuririn: a bola azul entre as mãos (Preparo, laço).
- kame_faixa_kuririn: o feixe azul com a onda em espiral (faixa, laço).
- kame_kuririn_impacto: a explosão azul do Kamehameha.

Kratos
- laminas_kratos: as duas Lâminas do Caos voando presas nas correntes, em
  arcos de fogo cruzados, e o sangue espirrando (perto).
- furia_kratos: a raiva espartana nele — a aura vermelha estourando, o vapor
  subindo e o tremor (nele).
- furia_espartana: a pancada rápida com o rastro vermelho (perto).
- ira_kratos: a raiva juntando antes da Ira dos deuses (Preparo, laço).
- ira_dos_deuses: o chão racha sob cada rival e a coluna de fogo sobe.
"""
from __future__ import annotations

import math

import numpy as np

from .charizard_megaman import _brasas, _fogo
from .base import FAIXA, GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _quadro(t, seed=0):
    return np.random.default_rng(seed + int(t * 997) % 9973)


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _raio(T, q, x1, y1, x2, y2, larg=0.01, depth=4, rough=0.32):
    return T.polyline(jagged(q, x1, y1, x2, y2, depth, rough), larg)


_RUIDOS: dict = {}


def _ruido(T, seed, escala=0.05, oitavas=3):
    chave = (T.W, T.H, seed, escala, oitavas)
    if chave not in _RUIDOS:
        _RUIDOS[chave] = T.noise(np.random.default_rng(seed), escala, oitavas)
    return _RUIDOS[chave]


# =================================================================== Sasuke
def chidori_sasuke_mao(T, t, rng):
    """O Chidori na mão do Sasuke: a bola de raio clara, os raios curtos para os lados e os estalos
    compridos arrastando para trás (−x), como asas — muda a cada quadro."""
    G, H = vazio(T)
    q = _quadro(t, 5)
    nucleo = T.gauss(0.15, 0, 0.12) * (0.85 + 0.15 * math.sin(TAU * t * 7))
    R = T.zero()
    for _ in range(6):
        a = q.uniform(0, TAU)
        R += _raio(T, q, 0.15, 0, 0.15 + 0.4 * math.cos(a), 0.4 * math.sin(a), 0.01, 3, 0.35)
    for _ in range(3):
        y = q.uniform(-0.35, 0.35)
        R += _raio(T, q, 0.1, 0, -0.85, y, 0.009, 4, 0.25) * 0.8
    G += nucleo * 1.5 + R * 1.2 + T.blur(R, 0.025) * 0.7
    H += nucleo * 1.5 + R * 0.8
    return G, H


def chidori_sasuke(T, t, rng):
    """A lança de raio atravessando: a mão entra (−x), o clarão, e os raios saem pelas costas do
    rival (+x) em feixe, com as faíscas e o anel."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    q = _quadro(t, 9)
    entra = ease_in(rel(t, 0.0, 0.14), 1.6)
    lanca = T.tapered([(-1.0, 0.0, -0.95 + 0.95 * entra, 0.0, 1.0)], 0.1) * (1 - rel(t, 0.14, 0.3))
    k = pulso(t, 0.12, 0.5)
    clarao = T.gauss(0, 0, 0.24) * k * 2.0 + T.flare(0, 0, 1.3 * k + 1e-3, 0.0, 0.01) * k
    saida = T.zero()
    if t > 0.12:
        for _ in range(4):
            a = q.uniform(-0.35, 0.35)
            comp = 0.5 + 0.45 * ease_out(rel(t, 0.12, 0.4), 2)
            saida += _raio(T, q, 0.05, 0, comp * math.cos(a), comp * math.sin(a), 0.014, 5, 0.3)
        saida *= 1 - rel(t, 0.55, 0.85)
    anel = T.ring(0.15 + 0.55 * ease_out(rel(t, 0.12, 0.6), 2), 0.03) * pulso(t, 0.12, 0.65)
    G += (lanca * 1.2 + clarao + saida * 1.3 + T.blur(saida, 0.02) + anel) * env
    H += (lanca + clarao * 1.1 + saida * 0.9) * env
    return G, H


def mangekyo_sasuke(T, t, rng):
    """O Mangekyō do Sasuke acendendo nele: a íris com as três pontas curvas (a estrela de seis
    pontas do Sasuke) girando e o brilho em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2)
    giro = TAU * t * 0.8
    iris = T.ring(0.3 * abre + 1e-3, 0.03)
    formas = []
    for k in range(3):
        a = giro + TAU * k / 3
        formas.append((lamina(0.0, 0.0, 0.28 * abre * math.cos(a) + 1e-3, 0.28 * abre * math.sin(a), 0.07), 1.0))
        a2 = a + TAU / 6
        formas.append((lamina(0.0, 0.0, 0.2 * abre * math.cos(a2) + 1e-3, 0.2 * abre * math.sin(a2), 0.04), 0.7))
    E = T.polys(formas, 0.004)
    G += (iris * 1.2 + E * 1.2 + T.gauss(0, 0, 0.4) * 0.3 * abre) * env
    H += (iris * 0.5 + E * 0.6) * env
    return G, H


def amaterasu(T, t, rng):
    """Amaterasu: as chamas negras pegam no rival de uma vez e ficam — línguas de fogo de verdade
    subindo, mas só a borda brilha (o miolo fica escuro, as chamas são negras), com as brasas
    escuras subindo, e o fogo não se apaga até o fim."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    pega = ease_out(rel(t, 0.0, 0.18), 2)
    fogo, _ = _fogo(T, t, 0.0, 0.6, 0.38 * pega + 0.03, 1.35 * pega + 0.05, 13, 1.4)
    liso = T.blur(fogo, 0.014)
    borda = np.exp(-((liso - 0.22) / 0.07) ** 2) * (liso > 0.06)
    k = pulso(t, 0.0, 0.22)
    clarao = T.gauss(0, 0.1, 0.25) * k
    brasas = _brasas(T, t, 17, 18, 0.0, 0.3, 0.6, 0.9, 0.013) * rel(t, 0.1, 0.3)
    G += (liso * 0.25 + borda * 1.1 + clarao + brasas * 0.6) * env
    H += (borda * 0.35) * env
    return G, H


def genjutsu_sasuke(T, t, rng):
    """O Genjutsu: o Sharingan gigante abre sobre o rival e gira (as três vírgulas), as espirais da
    confusão rodando em volta dele e o mundo se torcendo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = back(rel(t, 0.0, 0.3), 1.3)
    giro = TAU * t * 1.2
    iris = T.ring(0.55 * abre + 1e-3, 0.03) + T.ring(0.32 * abre + 1e-3, 0.015) * 0.7
    tomoes = []
    for k in range(3):
        a = giro + TAU * k / 3
        cx, cy = 0.32 * abre * math.cos(a), 0.32 * abre * math.sin(a)
        tomoes.append((cx, cy, 1.0))
    V = T.splats(tomoes, 0.05) * abre
    caudas = T.zero()
    for k in range(3):
        a = giro + TAU * k / 3
        caudas += T.arc_band(0.32 * abre + 1e-3, 0.03, a - 0.9, a, 1.0, 0.0, 0, 0, 1.0)
    espirais = T.zero()
    for j in range(3):
        cx, cy = 0.7 * math.cos(TAU * j / 3 + t), 0.5 * math.sin(TAU * j / 3 + t)
        espirais += T.arc_band(0.1, 0.012, giro * 2 + j, giro * 2 + j + 5, 1.0, 0.0, cx, cy, 0.5) * rel(t, 0.3, 0.45)
    G += (iris * 1.2 + V * 1.3 + caudas * 1.0 + espirais * 1.0 + T.gauss(0, 0, 0.6) * 0.2 * abre) * env
    H += (iris * 0.4 + V * 0.8) * env
    return G, H


# =================================================================== Homem-Aranha
def _rede(T, cx, cy, r, abre, raios=8, aneis=3, giro=0.0, sq=1.0):
    """A teia: os raios saindo do centro e os anéis ligando (em segmentos, como uma teia de verdade)."""
    segs = []
    for k in range(raios):
        a = giro + TAU * k / raios
        segs.append((cx, cy, cx + r * abre * math.cos(a), cy + r * abre * math.sin(a) * sq, 1.0))
    for j in range(1, aneis + 1):
        rr = r * abre * j / aneis
        for k in range(raios):
            a1 = giro + TAU * k / raios
            a2 = giro + TAU * (k + 1) / raios
            segs.append((cx + rr * math.cos(a1), cy + rr * math.sin(a1) * sq, cx + rr * math.cos(a2), cy + rr * math.sin(a2) * sq, 1.0))
    return T.lines(segs, 0.012)


def teia_voando(T, t, rng):
    """A bola de teia voando para +x: a teia fechada girando e o fio puxado para trás."""
    G, H = vazio(T)
    cx = 0.35
    W = _rede(T, cx, 0, 0.2, 1.0, 6, 2, TAU * t)
    fio = T.lines([(-1.0, 0.0, cx - 0.2, 0.0, 1.0)], 0.01) * 0.8
    G += W * 1.2 + T.gauss(cx, 0, 0.08) * 0.8 + fio
    H += W * 0.4
    return G, H


def teia_prende(T, t, rng):
    """A teia grudando no rival: a rede abre de uma vez, achata um pouco e fica presa, com os fios
    extras grudando nas pontas."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = back(rel(t, 0.0, 0.3), 1.6)
    W = _rede(T, 0, 0, 0.7, abre, 10, 4, 0.2)
    k = pulso(t, 0.0, 0.3)
    estalo = T.gauss(0, 0, 0.15) * k
    pontas = T.zero()
    for j in range(10):
        a = 0.2 + TAU * j / 10
        pontas += T.gauss(0.7 * abre * math.cos(a), 0.7 * abre * math.sin(a), 0.03) * rel(t, 0.25, 0.4)
    G += (W * 1.1 + estalo + pontas) * env
    H += (W * 0.4) * env
    return G, H


def salvamento_aranha(T, t, rng):
    """O Salvamento: ele chega balançando na teia (o arco que desce do alto à esquerda, com o fio
    preso lá em cima) e a teia cobre o aliado, fechando como um escudo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    f = ease_in(rel(t, 0.0, 0.35), 1.4)
    a = math.pi * (0.95 - 0.55 * f)
    ax, ay = -0.2, -1.2
    px, py = ax + 1.1 * math.cos(a), ay + 1.1 * math.sin(a)
    fio = T.lines([(ax, ay, px, py, 1.0)], 0.012) * (1 - rel(t, 0.35, 0.45))
    arco = T.arc_band(1.1, 0.04, math.pi * 0.95, a, 1.0, 0.0, ax, ay, 0.4) * (1 - rel(t, 0.35, 0.5))
    corpo = T.gauss(px, py, 0.07) * (1 - rel(t, 0.35, 0.45))
    escudo = _rede(T, 0, 0, 0.6, ease_out(rel(t, 0.3, 0.55), 2), 10, 3, 0.1) * rel(t, 0.3, 0.4)
    bolha = T.ring(0.6, 0.03) * rel(t, 0.5, 0.6)
    G += (fio * 0.9 + arco * 0.8 + corpo * 1.3 + escudo + bolha) * env
    H += (corpo * 0.8 + escudo * 0.3) * env
    return G, H


def teia_impacto_bola(T, t, rng):
    """O tiro de teia grosso voando: a bola densa de teia com os fios arrastando para trás."""
    G, H = vazio(T)
    cx = 0.35
    bola = T.gauss(cx, 0, 0.13)
    W = _rede(T, cx, 0, 0.15, 1.0, 8, 2, TAU * t * 2)
    fios = T.tapered([(cx - 0.9, y, cx - 0.1, y * 0.4, 1.0) for y in (-0.15, 0.0, 0.15)], 0.02)
    G += bola * 1.4 + W + fios * 0.7
    H += bola * 1.2
    return G, H


def teia_de_impacto(T, t, rng):
    """O tiro estourando no rival: o "splat" da teia em fios espirrados, a rede grudada e o X do golpe
    cortado."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    k = pulso(t, 0.0, 0.3)
    splat = T.gauss(0, 0, 0.2) * k * 1.4
    sub = np.random.default_rng(23)
    fios = T.zero()
    for _ in range(12):
        a = sub.uniform(0, TAU)
        comp = (0.3 + 0.4 * sub.uniform()) * ease_out(rel(t, 0.0, 0.25), 2)
        fios += T.tapered([(comp * math.cos(a) + 1e-3, comp * math.sin(a), 0, 0, 1.0)], 0.04)
    W = _rede(T, 0, 0, 0.45, ease_out(rel(t, 0.1, 0.35), 2), 8, 3, 0.3) * rel(t, 0.1, 0.2)
    X = T.lines([(-0.2, -0.2, 0.2, 0.2, 1.0), (-0.2, 0.2, 0.2, -0.2, 1.0)], 0.05) * pulso(t, 0.35, 0.9)
    G += (splat + fios * 0.9 + W + X * 1.2) * env
    H += (splat * 0.9 + X * 0.7) * env
    return G, H


# =================================================================== Trunks
def espada_do_futuro(T, t, rng):
    """A Espada do futuro: a espada cortando o rival muitas vezes, em grade (deitado, em pé e nas
    diagonais), cada corte uma lâmina fina e rápida, e no fim todos brilham juntos."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    cortes = [(-0.6, -0.1, 0.6, 0.1), (-0.1, -0.6, 0.1, 0.6), (-0.5, -0.5, 0.5, 0.5), (-0.5, 0.5, 0.5, -0.5),
              (-0.6, 0.25, 0.6, 0.3), (-0.6, -0.3, 0.6, -0.25), (0.25, -0.6, 0.3, 0.6), (-0.3, -0.6, -0.25, 0.6)]
    L = T.zero()
    for j, (x1, y1, x2, y2) in enumerate(cortes):
        ini = 0.045 * j
        prog = ease_out(rel(t, ini, ini + 0.08), 2)
        if prog <= 0:
            continue
        L += T.polys([(lamina(x1, y1, x2, y2, 0.03, prog), 1.0)], 0.003) * (0.4 + 0.6 * (1 - rel(t, ini + 0.1, ini + 0.25)))
    junto = pulso(t, 0.5, 0.8)
    todos = T.zero()
    if junto > 0:
        for x1, y1, x2, y2 in cortes:
            todos += T.lines([(x1, y1, x2, y2, 1.0)], 0.02)
    G += (L * 1.3 + T.blur(L, 0.015) * 0.5 + todos * junto * 1.3 + T.gauss(0, 0, 0.3) * junto * 0.8) * env
    H += (L * 0.9 + todos * junto * 0.8) * env
    return G, H


def selo_burning(T, t, rng):
    """Os gestos do Burning Attack: as mãos desenhando rápido no ar — três losangos e quadrados de
    luz piscando um depois do outro na frente dele — e as mãos se juntando."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    F = T.zero()
    for j in range(4):
        k = pulso(t, 0.1 * j, 0.1 * j + 0.3)
        x, y = 0.2 * math.cos(j * 2.1), 0.2 * math.sin(j * 2.1)
        r = 0.12
        pts = [(x, y - r), (x + r, y), (x, y + r), (x - r, y)] if j % 2 == 0 else [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)]
        F += T.polyline(pts + [pts[0]], 0.015) * k
    junta = T.gauss(0, 0, 0.12) * pulso(t, 0.45, 0.9) * 1.3
    G += (F * 1.2 + junta) * env
    H += (F * 0.5 + junta * 0.9) * env
    return G, H


def burning_bola(T, t, rng):
    """A bola do Burning Attack voando para +x: a esfera de ki com a borda em chamas e o rastro."""
    G, H = vazio(T)
    cx = 0.3
    nucleo = T.gauss(cx, 0, 0.12)
    borda = T.ring(0.16, 0.035, cx, 0) * (0.8 + 0.2 * math.sin(TAU * t * 6))
    rastro = T.tapered([(cx - 0.9, 0, cx - 0.1, 0, 1.0)], 0.28)
    G += nucleo * 1.6 + borda + T.blur(rastro, 0.025) * 0.8
    H += nucleo * 1.5
    return G, H


def burning_attack(T, t, rng):
    """A explosão do Burning Attack: o clarão, a bola de fogo de ki abrindo, o anel e as faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    k = pulso(t, 0.0, 0.45)
    clarao = T.gauss(0, 0, 0.3) * k * 2.0 + T.flare(0, 0, 1.3 * k + 1e-3, 0.3, 0.01) * k
    bola = T.gauss(0, 0, 0.2 + 0.2 * ease_out(rel(t, 0.0, 0.4), 2)) * pulso(t, 0.0, 0.7) * 0.8
    anel = T.ring(0.15 + 0.7 * ease_out(rel(t, 0.0, 0.5), 2), 0.04) * pulso(t, 0.0, 0.55)
    sub = np.random.default_rng(31)
    fa = T.splats([(d * math.cos(a), d * math.sin(a), pulso(t, 0.0, 0.8) * sub.uniform(0.4, 1)) for a, d in ((sub.uniform(0, TAU), 0.1 + 0.75 * ease_out(rel(t, 0.0, 0.7), 2) * sub.uniform(0.3, 1)) for _ in range(20))], 0.012)
    G += (clarao + bola + anel + fa * 1.2) * env
    H += (clarao * 1.1 + bola * 0.5 + anel * 0.3) * env
    return G, H


def aura_trunks(T, t, rng):
    """A aura de Super Saiyajin: as labaredas pontudas subindo em volta dele, piscando, e os raios
    finos de energia."""
    G, H = vazio(T)
    q = _quadro(t, 37)
    formas = []
    for j in range(14):
        x = -0.5 + j / 13
        alto = 0.6 + 0.35 * q.uniform() * (1 - abs(x))
        formas.append((lamina(x * 0.9, 0.55, x * 0.6 + q.normal(0, 0.05), 0.55 - alto, 0.07), q.uniform(0.5, 1)))
    A = T.polys(formas, 0.01)
    R = T.zero()
    for _ in range(2):
        x = q.uniform(-0.4, 0.4)
        R += _raio(T, q, x, 0.4, x + q.normal(0, 0.1), -0.3, 0.008, 3, 0.35)
    G += A * 0.9 + T.blur(A, 0.03) * 0.5 + R * 1.2
    H += A * 0.3 + R * 0.8
    return G, H


def corte_final(T, t, rng):
    """O Corte final: a lâmina desce num corte vertical gigante de cima a baixo, a luz racha ao meio
    no rival e as duas metades de luz se afastam para os lados, com as faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    prog = ease_out(rel(t, 0.0, 0.2), 2.5)
    L = T.polys([(lamina(0.05, -1.0, -0.05, 1.0, 0.06, prog, rel(t, 0.3, 0.6)), 1.0)], 0.003)
    k = pulso(t, 0.15, 0.55)
    clarao = T.gauss(0, 0, 0.12, 0.6) * k * 1.6
    abre = ease_out(rel(t, 0.25, 0.75), 2)
    metades = T.zero()
    for s in (-1, 1):
        metades += np.exp(-((T.U - s * 0.25 * abre) / 0.06) ** 2) * np.exp(-(T.V / 0.6) ** 2)
    metades *= pulso(t, 0.25, 0.9)
    sub = np.random.default_rng(41)
    fa = T.splats([(s * (0.05 + 0.6 * ease_out(rel(t, 0.2, 0.8), 2) * sub.uniform(0.3, 1)), sub.uniform(-0.7, 0.7), pulso(t, 0.2, 0.85) * sub.uniform(0.4, 1)) for s in (-1, 1) for _ in range(10)], 0.011)
    G += (L * 1.4 + T.blur(L, 0.02) * 0.6 + clarao + metades * 0.9 + fa * 1.1) * env
    H += (L * 1.1 + clarao * 1.0 + metades * 0.3) * env
    return G, H


# =================================================================== Kuririn
def kienzan_disco(T, t, rng):
    """O Kienzan voando: o disco fininho e chato (visto de lado, uma elipse fina) com a borda
    serrilhada girando e o zumbido de luz atrás."""
    G, H = vazio(T)
    cx = 0.3
    dentes = []
    for k in range(24):
        a = TAU * k / 24 + TAU * t * 3
        r = 0.32 if k % 2 == 0 else 0.27
        dentes.append((cx + r * math.cos(a), r * math.sin(a) * 0.22))
    D = T.polys([(dentes, 1.0)], 0.004)
    brilho = T.gauss(cx, 0, 0.3, 0.06) * 0.6
    rastro = T.tapered([(cx - 0.95, 0, cx - 0.3, 0, 1.0)], 0.06) * 0.6
    G += D * 1.2 + brilho + rastro
    H += D * 0.6
    return G, H


def kienzan_corte(T, t, rng):
    """O Kienzan atravessando: o disco passa (de −x para +x), deixa o corte fino e reto no rival,
    que brilha e depois some, com as faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    passa = ease_in(rel(t, 0.0, 0.3), 1.2)
    dx = -1.0 + 2.0 * passa
    disco = T.gauss(dx, 0, 0.18, 0.04) * (1 - rel(t, 0.3, 0.35)) * 1.3
    corte = T.lines([(-0.6, 0.02, min(0.6, dx), -0.02, 1.0)], 0.018) * (t > 0.08) * (1 - rel(t, 0.55, 0.9))
    k = pulso(t, 0.1, 0.45)
    clarao = T.gauss(0, 0, 0.6, 0.1) * k * 0.9
    sub = np.random.default_rng(43)
    fa = T.splats([(sub.uniform(-0.6, 0.6), sub.normal(0, 0.03) + 0.4 * rel(t, 0.2, 1.0) * sub.uniform(-1, 1), pulso(t, 0.1, 0.8) * sub.uniform(0.4, 1)) for _ in range(18)], 0.01)
    G += (disco + corte * 1.4 + clarao + fa * 1.1) * env
    H += (disco * 0.8 + corte * 1.0 + clarao * 0.5) * env
    return G, H


def taiyoken_flash(T, t, rng):
    """As mãos do Kuririn no rosto acendendo: a luz forte crescendo no meio, com os dedos abertos
    em leque marcados por riscos de luz."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    k = pulso(t, 0.0, 0.8)
    luz = T.gauss(0, 0, 0.18) * k * 1.6
    dedos = T.tapered([(0.1 * math.cos(a), 0.1 * math.sin(a), 0.5 * math.cos(a) + 1e-3, 0.5 * math.sin(a), 1.0) for a in np.linspace(-2.6, -0.5, 5)], 0.03) * k
    G += (luz + dedos * 0.9) * env
    H += (luz * 1.2 + dedos * 0.5) * env
    return G, H


def taiyoken(T, t, rng):
    """O Taiyoken no campo dos rivais: o clarão branco enorme que estoura, os raios de sol saindo
    em volta e, quando a luz baixa, as espirais de quem ficou cego girando."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    k = pulso(t, 0.0, 0.55)
    clarao = T.gauss(0, 0, 0.3) * k * 2.0 + T.flare(0, 0, 1.5 * k + 1e-3, 0.0, 0.006) * k
    raios = T.zero()
    for j in range(16):
        a = TAU * j / 16
        comp = 0.8 * ease_out(rel(t, 0.0, 0.3), 2)
        raios += T.tapered([(comp * math.cos(a) + 1e-3, comp * math.sin(a), 0.1 * math.cos(a), 0.1 * math.sin(a), 1.0)], 0.06)
    raios *= 1 - rel(t, 0.35, 0.6)
    espirais = T.zero()
    vivo = rel(t, 0.45, 0.6)
    for j, x in enumerate((-0.55, 0.0, 0.55)):
        g = TAU * t * 2 + j
        espirais += T.arc_band(0.1, 0.012, g, g + 5, 1.0, 0.0, x, -0.35, 0.5) * vivo
    G += (clarao + raios * 0.9 + espirais) * env
    H += (clarao * 1.3 + raios * 0.4) * env
    return G, H


def kame_kuririn(T, t, rng):
    """O Kamehameha juntando nas mãos do Kuririn: a bola azul pulsando entre as mãos, as faíscas
    entrando e o brilho."""
    G, H = vazio(T)
    pul = 0.85 + 0.15 * math.sin(TAU * t * 5)
    bola = T.gauss(0, 0, 0.13 * pul)
    sub = np.random.default_rng(47)
    pts = []
    for _ in range(22):
        a = sub.uniform(0, TAU)
        f = (sub.uniform() + t * 2) % 1
        r = 0.7 * (1 - f) + 0.15
        pts.append((r * math.cos(a), r * math.sin(a), f))
    G += bola * 1.7 + T.splats(pts, 0.012) + T.ring(0.2, 0.04) * 0.4 * pul
    H += bola * 1.7
    return G, H


def kame_faixa_kuririn(T, t, rng):
    """O feixe do Kamehameha do Kuririn: o raio azul com o miolo claro e uma onda em espiral
    enrolada nele, girando — mais fino que o do Goku."""
    G, H = vazio(T)
    alto = T.H / T.W
    corpo = np.exp(-(T.V / (alto * 0.22)) ** 2)
    miolo = np.exp(-(T.V / (alto * 0.08)) ** 2)
    onda = T.zero()
    pts1, pts2 = [], []
    for k in range(200):
        f = k / 199
        x = -0.98 + 1.96 * f
        ph = TAU * (f * 5 - t * 2)
        pts1.append((x, alto * 0.3 * math.sin(ph)))
        pts2.append((x, -alto * 0.3 * math.sin(ph)))
    onda = T.polyline(pts1, 0.008) + T.polyline(pts2, 0.008) * 0.6
    G += corpo * 0.9 + miolo * 1.3 + onda * 0.9 + T.gauss(-0.95, 0, 0.05, alto * 0.4)
    H += miolo * 1.4 + onda * 0.3
    return G, H


def kame_kuririn_impacto(T, t, rng):
    """A explosão azul do Kamehameha: o clarão, a esfera de energia abrindo, o anel duplo e as
    faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    k = pulso(t, 0.0, 0.5)
    clarao = T.gauss(0, 0, 0.32) * k * 2.0 + T.flare(0, 0, 1.4 * k + 1e-3, 0.0, 0.01) * k
    esfera = T.ring(0.1 + 0.5 * ease_out(rel(t, 0.0, 0.45), 2), 0.08) * pulso(t, 0.0, 0.65) * 0.6
    a1 = T.ring(0.15 + 0.75 * ease_out(rel(t, 0.05, 0.55), 2), 0.03) * pulso(t, 0.05, 0.6)
    sub = np.random.default_rng(53)
    fa = T.splats([(d * math.cos(a), d * math.sin(a), pulso(t, 0.0, 0.85) * sub.uniform(0.4, 1)) for a, d in ((sub.uniform(0, TAU), 0.1 + 0.8 * ease_out(rel(t, 0.0, 0.75), 2) * sub.uniform(0.3, 1)) for _ in range(22))], 0.012)
    G += (clarao + esfera + a1 + fa * 1.2) * env
    H += (clarao * 1.1 + esfera * 0.3 + a1 * 0.3) * env
    return G, H


# =================================================================== Kratos
def _corrente(T, x1, y1, x2, y2, curva, elos=12, tam=0.012):
    """A corrente: os elos em pontinhos ao longo de uma curva (a corrente frouxa entre a mão e a lâmina)."""
    pts = []
    for k in range(elos + 1):
        f = k / elos
        x = x1 + (x2 - x1) * f
        y = y1 + (y2 - y1) * f + curva * math.sin(math.pi * f)
        pts.append((x, y, 1.0))
    return T.splats(pts, tam)


def laminas_kratos(T, t, rng):
    """As Lâminas do Caos: as duas lâminas voam presas nas correntes e cortam o rival em dois arcos de
    fogo cruzados (uma de cima, outra de baixo), o fogo fica no rastro e o sangue espirra."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    L = T.zero()
    F = T.zero()
    for s, ini in ((1, 0.0), (-1, 0.18)):
        p = ease_out(rel(t, ini, ini + 0.22), 2)
        if p <= 0:
            continue
        a0, a1 = (-2.4, 0.6) if s > 0 else (2.4, -0.6)
        a = a0 + (a1 - a0) * p
        r = 0.7
        cx, cy = -0.35, 0.0
        bx, by = cx + r * math.cos(a), cy + r * math.sin(a)
        some = 1 - rel(t, ini + 0.3, ini + 0.45)
        F += T.arc_band(r, 0.06, a0, a, 1.0, 0.0, cx, cy, 0.8) * (1 - rel(t, ini + 0.25, ini + 0.55))
        ang = a + s * math.pi / 2
        L += T.polys([(lamina(bx - 0.17 * math.cos(ang), by - 0.17 * math.sin(ang), bx + 0.17 * math.cos(ang), by + 0.17 * math.sin(ang), 0.06), 1.0)], 0.004) * some
        L += _corrente(T, -1.0, 0.1 * s, bx, by, 0.1 * s, 14, 0.01) * some * 0.8
    k = pulso(t, 0.15, 0.55) + pulso(t, 0.33, 0.7)
    clarao = T.gauss(0, 0, 0.2) * k
    sub = np.random.default_rng(61)
    sangue = T.splats([(d * math.cos(a), d * math.sin(a) + 0.3 * rel(t, 0.2, 1) ** 2, pulso(t, 0.15, 0.9) * sub.uniform(0.5, 1)) for a, d in ((sub.uniform(-1.2, 1.2), 0.1 + 0.6 * ease_out(rel(t, 0.15, 0.7), 2) * sub.uniform(0.3, 1)) for _ in range(16))], 0.02)
    G += (F * 0.9 + T.blur(F, 0.03) * 0.6 + L * 1.4 + clarao + sangue * 0.7) * env
    H += (F * 0.9 + L * 0.8 + clarao * 0.8 + sangue * 0.15) * env
    return G, H


def furia_kratos(T, t, rng):
    """A Fúria espartana nele: a aura vermelha estoura do corpo (o anel e as labaredas curtas), o vapor
    da raiva subindo e o brilho pulsando como coração."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    k = pulso(t, 0.0, 0.35)
    anel = T.ring(0.15 + 0.6 * ease_out(rel(t, 0.0, 0.4), 2), 0.05) * k
    fogo, miolo = _fogo(T, t, 0.0, 0.55, 0.32, 1.1, 71, 1.6)
    bate = 0.7 + 0.3 * abs(math.sin(TAU * t * 2.5))
    vapor = _brasas(T, t, 73, 26, 0.0, 0.4, 0.6, 0.9, 0.018)
    G += (anel * 1.2 + fogo * 0.9 * bate * rel(t, 0.05, 0.25) + vapor * 0.5 + T.gauss(0, 0, 0.3) * k * 0.8) * env
    H += (anel * 0.6 + miolo * 0.8 + fogo * 0.4) * env
    return G, H


def furia_espartana(T, t, rng):
    """A pancada da Fúria: Kratos entra rápido (os riscos vermelhos vindo de −x), o golpe estala no rival
    e a onda curta."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    entra = ease_in(rel(t, 0.0, 0.15), 1.5)
    sub = np.random.default_rng(79)
    riscos = T.tapered([(-1.0, y, -1.0 + 0.95 * entra, y * 0.6, 1.0) for y in sub.uniform(-0.25, 0.25, 6)], 0.035) * (1 - rel(t, 0.15, 0.35))
    k = pulso(t, 0.12, 0.5)
    clarao = T.gauss(0, 0, 0.22) * k * 1.6 + T.flare(0, 0, 1.0 * k + 1e-3, 0.4, 0.01) * k
    onda = T.ring(0.12 + 0.55 * ease_out(rel(t, 0.12, 0.6), 2), 0.04, 0, 0, 1.25) * pulso(t, 0.12, 0.6)
    estilhas = T.tapered([(0.1 * math.cos(a), 0.1 * math.sin(a), (0.15 + 0.4 * ease_out(rel(t, 0.12, 0.45), 2)) * math.cos(a) + 1e-3, (0.15 + 0.4 * ease_out(rel(t, 0.12, 0.45), 2)) * math.sin(a), 1.0) for a in np.linspace(-1.2, 1.2, 7)], 0.03) * pulso(t, 0.12, 0.55)
    G += (riscos + clarao + onda + estilhas) * env
    H += (riscos * 0.6 + clarao * 1.1 + estilhas * 0.5) * env
    return G, H


def ira_kratos(T, t, rng):
    """A raiva juntando antes da Ira dos deuses: o fogo vermelho em volta dele girando mais forte e as
    brasas sendo puxadas para dentro."""
    G, H = vazio(T)
    fogo, miolo = _fogo(T, t, 0.0, 0.55, 0.42, 1.25, 83, 1.8)
    sub = np.random.default_rng(89)
    pts = []
    for _ in range(24):
        a = sub.uniform(0, TAU)
        f = (sub.uniform() + t * 1.5) % 1
        r = 0.8 * (1 - f) + 0.1
        pts.append((r * math.cos(a), r * math.sin(a), f))
    G += fogo * 0.9 + T.splats(pts, 0.014) + T.gauss(0, 0.1, 0.18) * (0.7 + 0.3 * math.sin(TAU * t * 3))
    H += miolo + fogo * 0.4
    return G, H


def ira_dos_deuses(T, t, rng):
    """A Ira dos deuses em cada rival: o golpe no chão, a rachadura de fogo abrindo embaixo dele e a
    coluna de fogo subindo com as brasas — e o fogo fica queimando."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    k = pulso(t, 0.0, 0.3)
    q = np.random.default_rng(97)
    rachas = T.zero()
    for _ in range(6):
        lado = 1 if q.uniform() < 0.5 else -1
        comp = (0.45 + 0.4 * q.uniform()) * ease_out(rel(t, 0.0, 0.2), 2)
        rachas += _raio(T, q, 0, 0.55, lado * comp + 1e-3, 0.55 + q.uniform(-0.08, 0.08) * comp, 0.012, 3, 0.12)
    sobe = ease_out(rel(t, 0.08, 0.35), 2)
    fogo, miolo = _fogo(T, t, 0.0, 0.55, 0.3, 1.5 * sobe + 0.05, 101, 1.7)
    brasas = _brasas(T, t, 103, 30, 0.0, 0.5, 0.7, 1.1, 0.014) * rel(t, 0.1, 0.3)
    choque = T.ring(0.1 + 0.8 * ease_out(rel(t, 0.0, 0.4), 2), 0.04, 0, 0.55, 4.0) * pulso(t, 0.0, 0.45)
    G += (rachas * 1.3 * (1 - rel(t, 0.6, 0.9)) + fogo * 1.0 + brasas * 0.8 + choque + T.gauss(0, 0.5, 0.3, 0.1) * k * 1.4) * env
    H += (rachas * 0.9 + miolo * 1.1 + fogo * 0.4 + brasas * 0.4) * env
    return G, H


REGISTRO = [
    ("chidori_sasuke_mao", chidori_sasuke_mao, MEDIA, "Sasuke · o Chidori na mão (laço)", True),
    ("chidori_sasuke", chidori_sasuke, GRANDE, "Sasuke · a lança de raio atravessando o rival", False),
    ("mangekyo_sasuke", mangekyo_sasuke, MEDIA, "Sasuke · o Mangekyō acendendo nele", False),
    ("amaterasu", amaterasu, GRANDE, "Sasuke · as chamas negras do Amaterasu", False),
    ("genjutsu_sasuke", genjutsu_sasuke, GRANDE, "Sasuke · o Sharingan gigante e a confusão", False),
    ("teia_voando", teia_voando, MEDIA, "Homem-Aranha · a bola de teia voando (laço)", True),
    ("teia_prende", teia_prende, GRANDE, "Homem-Aranha · a rede de teia grudando no rival", False),
    ("salvamento_aranha", salvamento_aranha, GRANDE, "Homem-Aranha · chega balançando e cobre o aliado de teia", False),
    ("teia_impacto_bola", teia_impacto_bola, MEDIA, "Homem-Aranha · o tiro de teia grosso (laço)", True),
    ("teia_de_impacto", teia_de_impacto, GRANDE, "Homem-Aranha · o tiro estourando e cortando o golpe", False),
    ("espada_do_futuro", espada_do_futuro, GRANDE, "Trunks · os cortes em grade da espada", False),
    ("selo_burning", selo_burning, MEDIA, "Trunks · os gestos do Burning Attack (nele)", False),
    ("burning_bola", burning_bola, MEDIA, "Trunks · a bola do Burning Attack voando (laço)", True),
    ("burning_attack", burning_attack, GRANDE, "Trunks · a explosão do Burning Attack", False),
    ("aura_trunks", aura_trunks, MEDIA, "Trunks · a aura dourada (laço)", True),
    ("corte_final", corte_final, GRANDE, "Trunks · o corte vertical gigante", False),
    ("kienzan_disco", kienzan_disco, MEDIA, "Kuririn · o disco do Kienzan girando (laço)", True),
    ("kienzan_corte", kienzan_corte, GRANDE, "Kuririn · o disco atravessando e o corte fino", False),
    ("taiyoken_flash", taiyoken_flash, MEDIA, "Kuririn · as mãos no rosto acendendo (nele)", False),
    ("taiyoken", taiyoken, GRANDE, "Kuririn · o clarão solar no campo", False),
    ("kame_kuririn", kame_kuririn, MEDIA, "Kuririn · a bola azul entre as mãos (laço)", True),
    ("kame_faixa_kuririn", kame_faixa_kuririn, FAIXA, "Kuririn · o feixe do Kamehameha (faixa)", True),
    ("kame_kuririn_impacto", kame_kuririn_impacto, GRANDE, "Kuririn · a explosão azul do Kamehameha", False),
    ("laminas_kratos", laminas_kratos, GRANDE, "Kratos · as Lâminas do Caos nas correntes", False),
    ("furia_kratos", furia_kratos, MEDIA, "Kratos · a aura da Fúria espartana (nele)", False),
    ("furia_espartana", furia_espartana, GRANDE, "Kratos · a pancada rápida da Fúria", False),
    ("ira_kratos", ira_kratos, MEDIA, "Kratos · a raiva juntando (laço)", True),
    ("ira_dos_deuses", ira_dos_deuses, GRANDE, "Kratos · a rachadura e a coluna de fogo", False),
]
