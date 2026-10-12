"""Rodada 13 das habilidades próprias: Capitã Marvel, Demolidor, Justiceiro, Motoqueiro Fantasma e Blade (Marvel).

Capitã Marvel
- absorcao_cosmica: os fios de energia chegam de todos os lados e são absorvidos, a aura dourada acende
  em chamas em volta, a estrela de oito pontas do peito brilha e o anel de proteção fecha.
- rajada_binaria: os dois raios de fóton saem dos punhos ondulando, com as contas de luz correndo, e se
  juntam no rival numa bola que estala (Eletrificado).
- binario_preparo: o Preparo da Explosão binária — o corpo em chamas cósmicas, a crista de fogo no alto e a
  estrela do peito pulsando (laço).
- explosao_binaria: a energia guardada se fecha num ponto e explode na estrela de oito pontas gigante, com
  os anéis e os raios, e os choques que travam todo mundo (Paralisado).

Demolidor
- radar_sensorial: as ondas do radar (vermelhas) passam pela arena e, onde batem, o contorno do rival
  aparece em linhas; o coração dele pulsa (tum-tum) e fica Marcado.
- bastoes_em_cruz: os dois bastões vêm girando de cima e de baixo, batem em X no rival e ricocheteiam.
- demolidor_preparo: o Preparo do Contra-ataque — os chifres do capuz no alto e as ondas do radar
  saindo em pulsos, com as batidas dos corações em volta (laço).
- contra_ataque_cego: a rajada de golpes de bastão de todos os lados, um atrás do outro (os arcos curtos
  e as estrelinhas), e o golpe final que corta o Preparo.

Justiceiro
- mira_fria: a luneta (o anel com a cruz e os pontos de medida) desliza e trava no rival, e a caveira do
  Justiceiro aparece no meio; as setas de Enfraquecido descem.
- sniper_preparo: o Preparo do tiro — a cruz da luneta balançando com a respiração, os riscos de distância
  e o brilho da lente (laço).
- alvo_confirmado: o clarão do cano lá atrás, a bala supersônica (o traço reto com os anéis de vapor
  abrindo pelo caminho) e o impacto enorme com a caveira carimbada.

Motoqueiro Fantasma
- olhar_de_penitencia: a caveira em chamas aparece grande no alto, os olhos acendem e a onda de fogo do
  inferno se espalha pelo chão; as almas sobem (Amaldiçoado).
- penitencia_preparo: o Preparo do Penance Stare — a caveira com as chamas subindo e os olhos pulsando
  (laço).
- penance_stare: os dois olhos em brasa disparam os raios em espiral nos olhos do rival, o redemoinho das
  almas gira dentro dele e as chamas sobem (Paralisado).

Blade
- rastreio_vampirico: os rastros de cheiro de sangue ondulando até o rival, as presas do vampiro
  aparecem e a marca do caçador corta por cima; as setas de Enfraquecido descem.
- lamina_de_prata: a espada de prata sai da bainha num corte reto e brilhante (os brilhos correndo pelo
  fio) e o sangue volta para o Blade (Roubo de vida).
- caca_preparo: o Preparo da Caçada — a glaive de duas lâminas girando rápido na frente da lua (laço).
- cacada_noturna: a lua no céu, a glaive voa girando em volta do rival cortando três vezes, e o golpe final
  em X.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _borda(T, a, s=0.008):
    return np.clip(a - T.blur(a, s), 0, 1)


def _contorno(pts, w=1.0):
    return [(pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], w) for i in range(len(pts))]


def _chamas(T, t, cx, cy, larg, alt, n, seed, ang=-math.pi / 2):
    """As línguas de fogo: lâminas que saem da base e tremulam, cada uma na sua fase. `ang` é a direção."""
    sub = np.random.default_rng(seed)
    shapes = []
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    for k in range(n):
        off = (k / max(1, n - 1) - 0.5) * larg * 2
        f = sub.uniform(6, 11)
        h = alt * (0.55 + 0.45 * abs(math.sin(TAU * t * f / 4 + sub.uniform(0, 6)))) * (1 - 0.5 * abs(off) / max(larg, 1e-3))
        bx, by = cx + nx * off, cy + ny * off
        sway = 0.25 * h * math.sin(TAU * t * 3 + k)
        tx, ty = bx + ux * h + nx * sway, by + uy * h + ny * sway
        shapes.append((lamina(bx, by, tx, ty, larg / max(1, n) * 1.6 + 0.01), 1.0))
    return T.polys(shapes)


def _caveira(cx, cy, s, dentes_longos=True):
    """A caveira de frente: o crânio, a mandíbula, as órbitas, o nariz e os dentes (compridos no Justiceiro)."""
    cranio = [(cx + 0.3 * s * math.cos(a), cy - 0.05 * s + 0.3 * s * math.sin(a)) for a in np.linspace(math.radians(160), math.radians(380), 20)]
    queixo = 0.42 if dentes_longos else 0.32
    cranio += [(cx + 0.2 * s, cy + 0.2 * s), (cx + 0.16 * s, cy + queixo * s), (cx - 0.16 * s, cy + queixo * s), (cx - 0.2 * s, cy + 0.2 * s)]
    linhas = _contorno(cranio)
    olhos = []
    for lado in (-1, 1):
        olhos.append([(cx + lado * 0.11 * s + 0.075 * s * math.cos(a), cy + 0.02 * s + 0.06 * s * math.sin(a)) for a in np.linspace(0, TAU, 14, endpoint=False)])
    for o in olhos:
        linhas += _contorno(o)
    linhas += _contorno([(cx - 0.035 * s, cy + 0.12 * s), (cx + 0.035 * s, cy + 0.12 * s), (cx, cy + 0.18 * s)])
    y0, y1 = cy + 0.22 * s, cy + (queixo - 0.02) * s
    for k in range(7):
        x = cx + (-0.12 + 0.04 * k) * s
        linhas.append((x, y0, x, y1, 0.8))
    return linhas, [(cx - 0.11 * s, cy + 0.02 * s), (cx + 0.11 * s, cy + 0.02 * s)]


def _silhueta(cx, cy, s):
    meia = [(0.05, -0.33), (0.22, -0.28), (0.27, 0.1), (0.21, 0.12), (0.17, -0.1), (0.14, 0.14), (0.16, 0.56),
            (0.05, 0.56), (0.0, 0.22)]
    corpo = [(cx + x * s, cy + y * s) for x, y in meia] + [(cx - x * s, cy + y * s) for x, y in reversed(meia[:-1])]
    return corpo


def _setas_para_baixo(T, u, xs=(-0.42, 0.42), y0=0.15):
    setas = []
    for x in xs:
        y = y0 + 0.3 * ease_out(u, 2)
        setas += [(x - 0.07, y - 0.06, x, y + 0.02, 1 - u), (x + 0.07, y - 0.06, x, y + 0.02, 1 - u), (x, y - 0.2, x, y + 0.01, 1 - u)]
    return T.lines(setas, 0.022)


# =================================================================== Capitã Marvel
def _estrela8(cx, cy, r, ang=0.0):
    return estrela(cx, cy, r, ang, 8, 0.42)


def absorcao_cosmica(T, t, rng):
    """A absorção cósmica: os fios de energia chegam curvos de todos os lados e entram no corpo, a aura dourada
    acende em chamas em volta, a estrela de oito pontas do peito brilha e o anel de proteção se fecha."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    entra = rel(t, 0.0, 0.45)
    if 0 < entra < 1:
        sub = np.random.default_rng(10)
        segs = []
        for k in range(12):
            a = TAU * k / 12 + sub.uniform(-0.2, 0.2)
            u = rel(entra, k / 24, k / 24 + 0.5)
            if u <= 0 or u >= 1:
                continue
            d1 = 0.95 * (1 - ease_in(u, 2)) + 0.1
            d0 = d1 + 0.3
            curva = 0.5 * (1 - u)
            segs.append((d0 * math.cos(a + curva), d0 * math.sin(a + curva), d1 * math.cos(a), d1 * math.sin(a), 1.0))
        G += T.tapered(segs, 0.022) * 1.3
    aura = pulso(t, 0.25, 0.95)
    if aura > 0:
        A = T.zero()
        for k in range(14):
            a = TAU * k / 14
            A += _chamas(T, t + k * 0.07, 0.36 * math.cos(a), 0.42 * math.sin(a), 0.05, 0.3, 2, 30 + k, a)
        G += (A * 1.0 + T.blur(A, 0.02) * 0.6) * aura
        G += T.gauss(0, 0, 0.35) * 0.4 * aura
    brilha = rel(t, 0.4, 0.75)
    if brilha > 0:
        E = T.polys([(_estrela8(0, -0.02, 0.16 * back(min(1, brilha * 2), 1.5)), 1.0)])
        G += E * 1.2 * (1 - rel(t, 0.85, 1))
        H += E * 0.6 + T.flare(0, -0.02, 0.5 * (1 - brilha) + 0.05, 0, 0.012) * (1 - brilha)
    fecha = back(rel(t, 0.55, 0.8), 1.4)
    if fecha > 0:
        G += T.ring(0.68 * fecha, 0.025, 0, 0) * 1.2 + T.ring(0.62 * fecha, 0.012, 0, 0) * 0.7
    return G * env, H * env


def rajada_binaria(T, t, rng):
    """A rajada binária: os dois raios de fóton saem dos punhos (na esquerda) ondulando um em volta do outro,
    com as contas de luz correndo por eles, e se juntam no rival numa bola de energia que estala em raios
    curtos (Eletrificado)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    vai = ease_out(rel(t, 0.0, 0.25), 2)
    some = 1 - rel(t, 0.45, 0.65)
    if vai > 0 and some > 0:
        for lado in (-1, 1):
            pts = []
            for j in range(40):
                u = j / 39 * vai
                x = -0.9 + 0.9 * u
                y = lado * 0.13 * (1 - u) * math.cos(TAU * u * 2.5 + t * 20)
                pts.append((x, y))
            R = T.polyline(pts, 0.03)
            G += (R * 1.2 + T.blur(R, 0.025) * 0.8) * some
            H += T.polyline(pts, 0.01) * 1.2 * some
        contas = [(-0.9 + 0.9 * ((t * 3 + k / 6) % 1) * vai, 0.0, 0.9) for k in range(6)]
        H += T.splats(contas, 0.02) * some
        for lado in (-1, 1):
            H += T.gauss(-0.88, lado * 0.13, 0.04) * some * 1.3
    bola = rel(t, 0.2, 0.85)
    if 0 < bola < 1:
        b = back(min(1, bola * 2.5), 1.4)
        G += T.gauss(0, 0, 0.12 * b + 0.01) * (1 - bola) * 1.6 + T.ring(0.15 * b + 0.25 * bola, 0.02, 0, 0) * (1 - bola) * 1.2
        H += T.gauss(0, 0, 0.06 * b + 0.01) * (1 - bola) * 1.6
        q = np.random.default_rng(int(t * 30) % 8 + 3)
        for k in range(5):
            a = q.uniform(0, TAU)
            G += T.polyline(jagged(q, 0.1 * math.cos(a), 0.1 * math.sin(a), 0.4 * math.cos(a), 0.4 * math.sin(a), 5, 0.4), 0.01) * (1 - bola) * 1.3
    return G * env, H * env


def binario_preparo(T, t, rng):
    """O Preparo da Explosão binária: o corpo envolto em chamas cósmicas (as línguas subindo dos dois lados), a
    crista de fogo no alto da cabeça e a estrela de oito pontas pulsando no peito (laço)."""
    G, H = vazio(T)
    for lado in (-1, 1):
        F = _chamas(T, t, 0.22 * lado, 0.5, 0.12, 0.7, 5, 40 + lado, -math.pi / 2 + 0.15 * lado)
        G += _borda(T, F, 0.01) * 1.3 + F * 0.3
    C = _chamas(T, t, 0.0, -0.45, 0.08, 0.35, 3, 44)
    G += C * 0.9 + T.blur(C, 0.02) * 0.5
    bate = 0.75 + 0.25 * math.sin(TAU * t * 2)
    E = T.polys([(_estrela8(0, 0.0, 0.14 * bate, TAU * t / 8), 1.0)])
    G += E * 1.2
    H += E * 0.6 * bate + T.gauss(0, 0, 0.05) * bate
    return G, H


def explosao_binaria(T, t, rng):
    """A Explosão binária: a energia se fecha num ponto (os anéis apertando), explode na estrela de oito pontas
    gigante que gira um pouco, com os anéis e os raios em volta, e depois os choques travam todo mundo
    (Paralisado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    fecha = rel(t, 0.0, 0.25)
    if fecha < 1:
        for k in range(3):
            u = rel(fecha, 0.2 * k, 0.6 + 0.2 * k)
            if 0 < u < 1:
                G += T.ring(0.8 * (1 - ease_in(u, 2)) + 0.02, 0.02, 0, 0) * math.sin(math.pi * u) * 1.2
        H += T.gauss(0, 0, 0.04) * fecha * 1.5
    bum = rel(t, 0.25, 0.92)
    if bum > 0:
        b = ease_out(bum, 3)
        E = T.polys([(_estrela8(0, 0, 0.15 + 0.85 * b, 0.4 * bum), 1.0)])
        G += _borda(T, E, 0.015) * 1.6 * (1 - bum) + E * 0.35 * (1 - bum)
        H += T.gauss(0, 0, 0.1 + 0.25 * b) * (1 - bum) ** 2 * 2.0
        for k in range(2):
            u = rel(bum, 0.1 * k, 0.7 + 0.1 * k)
            if 0 < u < 1:
                G += T.ring(0.2 + 0.8 * ease_out(u, 2), 0.04 * (1 - u) + 0.01, 0, 0) * (1 - u) * 1.3
        raios = []
        for k in range(16):
            a = TAU * k / 16 + 0.2
            L = 0.3 + 0.8 * b * (1.0 if k % 2 else 0.7)
            raios.append((0.15 * math.cos(a), 0.15 * math.sin(a), L * math.cos(a), L * math.sin(a), 1 - bum))
        G += T.tapered(raios, 0.03) * 1.1
    trava = pulso(t, 0.55, 1.0)
    if trava > 0:
        q = np.random.default_rng(int(t * 25) % 6 + 50)
        for k in range(6):
            a = TAU * k / 6 + 0.3
            x0, y0 = 0.55 * math.cos(a), 0.55 * math.sin(a)
            G += T.polyline(jagged(q, x0, y0, x0 + 0.15 * math.cos(a + 1.6), y0 + 0.15 * math.sin(a + 1.6), 4, 0.5), 0.012) * trava * 1.3
    return G * env, H * env


# =================================================================== Demolidor
def radar_sensorial(T, t, rng):
    """O radar do Demolidor: as ondas vermelhas saem da esquerda e passam pela arena; onde batem, o contorno do
    rival aparece em linhas (e some de novo), e o coração dele pulsa em dois "tum-tum" (Marcado)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    ox, oy = -1.0, 0.1
    revela = 0.0
    for k in range(4):
        u = rel(t, 0.0 + 0.12 * k, 0.55 + 0.12 * k)
        if 0 < u < 1:
            r = 0.2 + 1.7 * u
            G += T.ring(r, 0.018, ox, oy, squash=0.9) * (1 - u) * 1.2
            d = abs(r - 1.0)
            revela = max(revela, max(0, 1 - d / 0.25) * (1 - u * 0.5))
    corpo = _silhueta(0.0, 0.05, 1.15)
    S = T.lines(_contorno(corpo), 0.012) + T.ring(0.095, 0.012, 0.0, 0.05 - 0.5, squash=0.85)
    fica = max(revela, pulso(t, 0.45, 0.95) * 0.6)
    G += S * fica * 1.3
    for tb in (0.5, 0.68):
        b = rel(t, tb, tb + 0.18)
        if 0 < b < 1:
            G += T.ring(0.05 + 0.25 * ease_out(b, 2), 0.015, 0.03, -0.12) * (1 - b) * 1.2
            H += T.gauss(0.03, -0.12, 0.045) * (1 - b) ** 2 * 1.6
    return G * env, H * env


def _bastao(cx, cy, comp, larg, ang):
    """O bastão do Demolidor: a haste arredondada, com a pega mais grossa."""
    pts = []
    for k in range(20):
        a = math.pi / 2 + math.pi * k / 19
        pts.append((-comp / 2 + larg * math.cos(a), larg * math.sin(a)))
    for k in range(20):
        a = -math.pi / 2 + math.pi * k / 19
        pts.append((comp / 2 + larg * math.cos(a), larg * math.sin(a)))
    return _gira(pts, ang, cx, cy)


def bastoes_em_cruz(T, t, rng):
    """Os bastões em cruz: os dois bastões vêm girando (um de cima, um de baixo, pela esquerda), batem em X no
    rival ao mesmo tempo (o clarão em cruz) e ricocheteiam para longe; os riscos de Lento ficam."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for lado in (-1, 1):
        vem = ease_in(rel(t, 0.0, 0.3), 1.5)
        volta = ease_out(rel(t, 0.32, 0.7), 2)
        if vem <= 0:
            continue
        if volta <= 0:
            x = -1.0 + 1.0 * vem
            y = lado * 0.7 * (1 - vem)
            ang = lado * (0.785 + 12 * vem)
            if vem >= 1:
                ang = lado * 0.785
        else:
            x = -0.6 * volta
            y = lado * (0.1 + 0.9 * volta) - 0.3 * volta
            ang = lado * (0.785 + 14 * volta)
        some = 1 - rel(t, 0.55, 0.75)
        B = T.polys([(_bastao(x, y, 0.62, 0.04, ang), 1.0)])
        G += (B * 1.2 + _borda(T, B, 0.005) * 0.8) * some
        H += _borda(T, B, 0.004) * 0.3 * some
        if 0 < vem < 1:
            G += T.arc_band(0.31, 0.04, ang - 1.4, ang, cx=x, cy=y, taper=0.8) * 0.8
    bate = rel(t, 0.28, 0.6)
    if 0 < bate < 1:
        H += T.flare(0, 0, 0.8 * (1 - bate) + 0.02, 0.785, 0.02) * (1 - bate) * 1.6 + T.gauss(0, 0, 0.1) * (1 - bate) ** 2 * 1.6
        G += T.ring(0.1 + 0.5 * ease_out(bate, 3), 0.04, 0, 0) * (1 - bate) * 1.4
    lento = pulso(t, 0.55, 1.0)
    if lento > 0:
        G += T.lines([(-0.35, -0.3 + 0.15 * k, -0.15, -0.3 + 0.15 * k, 1.0) for k in range(5)], 0.012) * lento * 0.8
    return G * env, H * env


def demolidor_preparo(T, t, rng):
    """O Preparo do Contra-ataque cego: os dois chifres do capuz no alto, as ondas do radar saindo do meio em
    pulsos e os coraçõezinhos dos inimigos batendo em volta (laço)."""
    G, H = vazio(T)
    for lado in (-1, 1):
        chifre = [(0.12 * lado, -0.45), (0.3 * lado, -0.78), (0.2 * lado, -0.44)]
        G += T.polys([(chifre, 1.0)]) * 1.1
    for k in range(3):
        u = (t + k / 3) % 1
        G += T.ring(0.08 + 0.6 * u, 0.016, 0, 0.05) * (1 - u) * 1.2
    for k, a in enumerate((0.3, 2.4, 4.2)):
        bate = max(0, math.sin(TAU * (t * 2 + k / 3))) ** 4
        x, y = 0.6 * math.cos(a), 0.05 + 0.45 * math.sin(a)
        H += T.gauss(x, y, 0.025 + 0.015 * bate) * (0.4 + bate) * 1.2
    H += T.gauss(0, 0.05, 0.03) * 1.0
    return G, H


def contra_ataque_cego(T, t, rng):
    """O contra-ataque cego: a rajada de golpes de bastão de todos os lados, um atrás do outro (os arcos curtos
    batendo e as estrelinhas no ponto), e o golpe final de cima que corta o Preparo (o clarão grande e as
    linhas)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    golpes = ((0.0, 0.4), (0.08, 2.6), (0.16, 1.2), (0.24, 3.8), (0.32, 5.2), (0.4, 0.9))
    for t0, a in golpes:
        u = rel(t, t0, t0 + 0.14)
        if 0 < u < 1:
            cab = a - 1.8 + 2.2 * ease_out(u, 2)
            A = T.arc_band(0.42, 0.08, cab - 1.5, cab, cx=0.12 * math.cos(a), cy=0.12 * math.sin(a), crescente=True)
            G += (A * 1.5 + T.blur(A, 0.02) * 0.5) * (1 - u * 0.5)
        b = rel(t, t0 + 0.08, t0 + 0.22)
        if 0 < b < 1:
            x, y = 0.12 * math.cos(a), 0.12 * math.sin(a)
            H += T.flare(x, y, 0.32 * (1 - b) + 0.01, a, 0.012) * (1 - b) * 1.5
            G += T.ring(0.03 + 0.15 * b, 0.015, x, y) * (1 - b) * 1.2
    final = rel(t, 0.5, 0.95)
    if 0 < final < 1:
        desce = ease_in(min(1, final * 3), 2)
        G += T.polys([(lamina(0.3, -0.9, -0.05 + 0.1 * desce, -0.9 + 0.95 * desce, 0.05), 1.0)]) * (1 - final) * 1.3
        bate = rel(final, 0.3, 1.0)
        if bate > 0:
            H += T.gauss(0, 0.05, 0.12) * (1 - bate) ** 2 * 2.0 + T.flare(0, 0.05, 0.8 * (1 - bate), 0.2, 0.018) * (1 - bate)
            G += T.ring(0.1 + 0.6 * ease_out(bate, 3), 0.04, 0, 0.05) * (1 - bate) * 1.4
            raios = [(0.12 * math.cos(TAU * k / 10), 0.05 + 0.12 * math.sin(TAU * k / 10),
                      (0.3 + 0.4 * bate) * math.cos(TAU * k / 10), 0.05 + (0.3 + 0.4 * bate) * math.sin(TAU * k / 10), 1 - bate) for k in range(10)]
            G += T.tapered(raios, 0.025) * 1.2
    return G * env, H * env


# =================================================================== Justiceiro
def _luneta(T, cx, cy, r):
    L = T.ring(r, 0.02, cx, cy) + T.ring(r * 0.94, 0.008, cx, cy)
    segs = [(cx - r, cy, cx - r * 0.12, cy, 1.0), (cx + r * 0.12, cy, cx + r, cy, 1.0),
            (cx, cy - r, cx, cy - r * 0.12, 1.0), (cx, cy + r * 0.12, cx, cy + r, 1.0)]
    for k in range(1, 5):
        d = r * 0.18 * k
        segs += [(cx + d, cy - 0.02, cx + d, cy + 0.02, 0.8), (cx - d, cy - 0.02, cx - d, cy + 0.02, 0.8),
                 (cx - 0.02, cy + d, cx + 0.02, cy + d, 0.8), (cx - 0.02, cy - d, cx + 0.02, cy - d, 0.8)]
    return L + T.lines(segs, 0.009)


def mira_fria(T, t, rng):
    """A mira fria: a luneta (o anel, a cruz e os pontinhos de medida) desliza de lado, balança e trava no
    rival; a caveira do Justiceiro acende no meio, e as setas de Enfraquecido descem."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    chega = ease_out(rel(t, 0.0, 0.35), 2.5)
    trava = rel(t, 0.35, 0.45)
    cx = -0.7 * (1 - chega) + 0.05 * math.sin(t * 9) * (1 - trava)
    cy = 0.3 * (1 - chega) + 0.04 * math.cos(t * 7) * (1 - trava)
    G += _luneta(T, cx, cy, 0.55) * 1.2 * (1 - rel(t, 0.85, 1))
    H += T.flare(cx, cy, 0.25 * pulso(t, 0.38, 0.55) + 0.01, 0.785, 0.01) * pulso(t, 0.38, 0.55)
    cav = rel(t, 0.42, 0.62)
    if cav > 0:
        linhas, olhos = _caveira(cx, cy + 0.02, 0.75 * back(cav, 1.3))
        C = T.lines(linhas, 0.014)
        G += C * 1.3 * (1 - rel(t, 0.85, 1))
        H += C * 0.3 + T.splats([(x, y, 1.0) for x, y in olhos], 0.03) * pulso(t, 0.45, 0.9) * 0.8
    desce = rel(t, 0.62, 1.0)
    if desce > 0:
        G += _setas_para_baixo(T, desce, (-0.65, 0.65)) * 1.2
    return G * env, H * env


def sniper_preparo(T, t, rng):
    """O Preparo do Alvo confirmado: a cruz da luneta balançando devagar em oito com a respiração, os riscos de
    distância na lateral e o brilho correndo na lente (laço)."""
    G, H = vazio(T)
    a = TAU * t
    cx, cy = 0.06 * math.sin(a), 0.04 * math.sin(2 * a)
    G += _luneta(T, cx, cy, 0.5) * 1.1
    segs = [(0.62, -0.3 + 0.1 * k, 0.68 + 0.04 * (k % 2), -0.3 + 0.1 * k, 1.0) for k in range(7)]
    G += T.lines(segs, 0.008) * 0.9
    gx, gy = 0.35 * math.cos(a * 1 + 2.4), 0.35 * math.sin(a + 2.4)
    H += T.flare(gx, gy, 0.12, 0.785, 0.008) * 0.9 + T.gauss(cx, cy, 0.015) * 1.2
    return G, H


def alvo_confirmado(T, t, rng):
    """O tiro de precisão: o clarão do cano lá atrás (com a fumaça), a bala supersônica (o traço reto e os anéis
    de vapor abrindo pelo caminho), o impacto enorme no rival (o clarão, o anel, os estilhaços saindo pelo
    outro lado) e a caveira carimbada um instante."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cano = (-0.95, -0.05)
    clarao = pulso(t, 0.0, 0.12)
    H += (T.flare(cano[0], cano[1], 0.35 * clarao + 0.01, 0, 0.014) + T.gauss(cano[0], cano[1], 0.06) * clarao) * clarao * 1.4
    fum = rel(t, 0.05, 0.6)
    if 0 < fum < 1:
        sub = np.random.default_rng(2)
        pts = [(cano[0] + 0.1 + 0.25 * fum * sub.uniform(0.3, 1), cano[1] - 0.15 * fum * sub.uniform(-0.3, 1), (1 - fum) * 0.6) for _ in range(8)]
        G += T.splats(pts, 0.05 + 0.05 * fum)
    rastro = rel(t, 0.06, 0.6)
    if 0 < rastro < 1:
        vai = min(1, rastro * 6)
        x1 = cano[0] + (0.0 - cano[0]) * vai
        G += T.lines([(cano[0], cano[1], x1, -0.03, 1.0)], 0.012) * (1 - rastro) * 1.4
        for k in range(6):
            xk = cano[0] + 0.15 * (k + 1)
            if xk > x1:
                break
            u = rel(t, 0.06 + 0.012 * k, 0.5)
            G += T.ring(0.02 + 0.09 * ease_out(u, 2), 0.01, xk, -0.04, squash=0.5) * (1 - u) * 1.0
    bate = rel(t, 0.1, 0.65)
    if 0 < bate < 1:
        b = ease_out(bate, 3)
        H += T.gauss(0, -0.03, 0.08 + 0.1 * b) * (1 - bate) ** 2 * 2.0 + T.flare(0, -0.03, 0.7 * (1 - bate), 0, 0.016) * (1 - bate)
        G += T.ring(0.08 + 0.45 * b, 0.035, 0, -0.03) * (1 - bate) * 1.4
        q = np.random.default_rng(31)
        estilhacos = []
        for _ in range(16):
            a = q.uniform(-0.7, 0.7)
            d = (0.2 + 0.7 * b) * q.uniform(0.5, 1)
            estilhacos.append((0.1 * math.cos(a), -0.03 + 0.1 * math.sin(a), d * math.cos(a), -0.03 + d * math.sin(a), 1 - bate))
        G += T.tapered(estilhacos, 0.018) * 1.2
    cav = pulso(t, 0.22, 0.75)
    if cav > 0:
        linhas, _ = _caveira(0, -0.03, 0.85)
        G += T.lines(linhas, 0.016) * cav * 1.2
    return G * env, H * env


# =================================================================== Motoqueiro Fantasma
def _caveira_em_chamas(T, t, cx, cy, s, olho=1.0):
    linhas, olhos = _caveira(cx, cy, s, dentes_longos=False)
    C = T.lines(linhas, 0.014 * s / 0.8)
    F = _chamas(T, t, cx, cy - 0.3 * s, 0.25 * s, 0.45 * s, 7, 61)
    O = T.splats([(x, y, 1.0) for x, y in olhos], 0.035 * s) * olho
    return C, F, O


def olhar_de_penitencia(T, t, rng):
    """O olhar de penitência: a caveira em chamas aparece grande no alto, os olhos acendem em brasa, e a onda de
    fogo do inferno sai do chão e se espalha pela arena (o anel de chamas que corre); as almas sobem
    (Amaldiçoado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    aparece = back(rel(t, 0.0, 0.25), 1.3) * (1 - rel(t, 0.6, 0.85))
    if aparece > 0:
        C, F, O = _caveira_em_chamas(T, t, 0, -0.35, 0.8 * aparece, olho=pulso(t, 0.15, 0.7))
        G += C * 1.2 + _borda(T, F, 0.01) * 1.3 + F * 0.35
        H += O * 1.8 + F * 0.15
    onda = rel(t, 0.3, 0.95)
    if 0 < onda < 1:
        r = 0.1 + 1.0 * ease_out(onda, 2)
        A = T.zero()
        for k in range(18):
            a = TAU * k / 18
            x, y = r * math.cos(a), 0.45 + 0.3 * r * math.sin(a)
            A += _chamas(T, t + k * 0.13, x, y, 0.05, 0.22 * (1 - onda) + 0.04, 1, 70 + k)
        G += (A * 1.1 + T.blur(A, 0.02) * 0.5) * (1 - onda * 0.6)
        G += T.ring(r, 0.03, 0, 0.45, squash=3.3) * (1 - onda) * 1.0
    almas = rel(t, 0.45, 1.0)
    if 0 < almas < 1:
        sub = np.random.default_rng(5)
        pts = []
        for k in range(8):
            x = sub.uniform(-0.8, 0.8)
            y = 0.4 - 0.9 * ((almas + sub.uniform(0, 0.5)) % 1)
            for j in range(4):
                pts.append((x + 0.03 * math.sin(t * 15 + j + k), y + 0.04 * j, (1 - j / 4) * math.sin(math.pi * almas)))
        G += T.splats(pts, 0.022) * 1.0
    return G * env, H * env


def penitencia_preparo(T, t, rng):
    """O Preparo do Penance Stare: a caveira com as chamas subindo da cabeça e os olhos pulsando em brasa (laço)."""
    G, H = vazio(T)
    C, F, O = _caveira_em_chamas(T, t, 0, 0.1, 0.9, olho=0.7 + 0.3 * math.sin(TAU * t * 2))
    G += C * 1.1 + _borda(T, F, 0.01) * 1.3 + F * 0.35
    H += O * 1.6
    return G, H


def penance_stare(T, t, rng):
    """O Penance Stare: os dois olhos em brasa acendem na esquerda, disparam os raios em espiral até os olhos do
    rival, e dentro dele o redemoinho das almas gira (os pontos girando para o centro); as chamas sobem em volta
    e ele fica travado (Paralisado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    olhos = ((-0.8, -0.32), (-0.62, -0.32))
    acende = pulso(t, 0.0, 0.7)
    H += T.splats([(x, y, 1.0) for x, y in olhos], 0.035) * acende * 1.8
    G += T.splats([(x, y, 1.0) for x, y in olhos], 0.08) * acende * 0.8
    raio = ease_out(rel(t, 0.12, 0.35), 2)
    some = 1 - rel(t, 0.6, 0.8)
    if raio > 0 and some > 0:
        for k, (ox, oy) in enumerate(olhos):
            alvo = (-0.06 + 0.12 * k, -0.08)
            pts = []
            for j in range(50):
                u = j / 49 * raio
                x = ox + (alvo[0] - ox) * u
                y = oy + (alvo[1] - oy) * u + 0.06 * math.sin(TAU * u * 4 + t * 25 + k * math.pi)
                pts.append((x, y))
            R = T.polyline(pts, 0.016)
            G += (R * 1.3 + T.blur(R, 0.02) * 0.6) * some
            H += T.polyline(pts, 0.006) * some
    gira = rel(t, 0.3, 1.0)
    if 0 < gira < 1:
        pts = []
        for k in range(4):
            for j in range(30):
                u = j / 29
                a = TAU * (k / 4 + gira * 1.8) + 5 * u
                r = 0.5 * (1 - u) + 0.04
                pts.append((r * math.cos(a), 0.05 + r * 0.8 * math.sin(a), math.sin(math.pi * u) * math.sin(math.pi * gira)))
        G += T.splats(pts, 0.016) * 1.3
        F = _chamas(T, t, 0.0, 0.5, 0.45, 0.4 * math.sin(math.pi * gira), 8, 90)
        G += _borda(T, F, 0.01) * 1.2 + F * 0.3
    return G * env, H * env


# =================================================================== Blade
def rastreio_vampirico(T, t, rng):
    """O rastreio: os rastros do cheiro de sangue ondulando da esquerda até o rival, as presas do vampiro
    aparecem nele (as duas presas compridas), e a marca do caçador corta por cima num risco; as setas de
    Enfraquecido descem."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    vai = ease_out(rel(t, 0.0, 0.35), 2)
    if vai > 0 and t < 0.7:
        some = 1 - rel(t, 0.5, 0.7)
        for k, y0 in enumerate((-0.45, 0.0, 0.45)):
            pts = []
            for j in range(30):
                u = j / 29 * vai
                pts.append((-1.0 + 1.0 * u, y0 * (1 - u) + 0.06 * math.sin(TAU * (u * 3 + t * 2) + k)))
            G += T.polyline(pts, 0.012) * some * 1.1
            gotas = [(pts[j][0], pts[j][1], 0.9) for j in range(0, len(pts), 6)]
            G += T.splats(gotas, 0.018) * some
    presas = back(rel(t, 0.3, 0.5), 1.4)
    if presas > 0:
        shapes = []
        for lado in (-1, 1):
            x = 0.12 * lado
            shapes.append(([(x - 0.05, -0.15), (x + 0.05, -0.15), (x + 0.005 * lado, -0.15 + 0.32 * presas)], 1.0))
        P = T.polys(shapes)
        G += (P * 0.8 + _borda(T, P, 0.006) * 1.2) * (1 - rel(t, 0.85, 1))
        G += T.arc_band(0.22, 0.016, 0.3, math.pi - 0.3, squash=0.6, cx=0, cy=-0.22) * presas * 0.9 * (1 - rel(t, 0.85, 1))
    corta = rel(t, 0.5, 0.65)
    if corta > 0:
        G += T.polys([(lamina(-0.45, 0.35, 0.45, -0.4, 0.035, prog=corta), 1.0)]) * 1.3 * (1 - rel(t, 0.85, 1))
        H += T.flare(0, 0, 0.4 * pulso(t, 0.55, 0.7) + 0.01, -0.7, 0.012) * pulso(t, 0.55, 0.7)
    desce = rel(t, 0.65, 1.0)
    if desce > 0:
        G += _setas_para_baixo(T, desce, (-0.55, 0.55)) * 1.2
    return G * env, H * env


def lamina_de_prata(T, t, rng):
    """A lâmina de prata: a espada sai da bainha num corte reto, longo e brilhante (o fio aceso e os brilhos
    correndo por ele), o rival leva o corte, e o sangue volta em gotas para o Blade (Roubo de vida)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corta = ease_out(rel(t, 0.05, 0.22), 3)
    some = rel(t, 0.3, 0.6)
    if corta > 0 and some < 1:
        L = T.polys([(lamina(-0.95, 0.5, 0.85, -0.55, 0.06, prog=corta, inicio=some), 1.0)])
        G += L * 1.4 + T.blur(L, 0.025) * 0.6
        H += _borda(T, L, 0.004) * 1.0
        for k in range(4):
            u = (t * 4 + k / 4) % 1 * corta
            x, y = -0.95 + 1.8 * u, 0.5 - 1.05 * u
            H += T.flare(x, y, 0.1, 0.3, 0.007) * (u > some) * 0.9
    bate = rel(t, 0.15, 0.5)
    if 0 < bate < 1:
        H += T.flare(0, -0.03, 0.5 * (1 - bate) + 0.02, -0.53, 0.012) * (1 - bate) * 1.3
    volta = rel(t, 0.45, 0.95)
    if 0 < volta < 1:
        sub = np.random.default_rng(14)
        pts = []
        for k in range(14):
            u = (volta * 1.3 + k / 14) % 1
            x = 0.0 - 0.9 * u
            y = -0.03 + 0.3 * math.sin(math.pi * u) * (1 if k % 2 else -0.4) + sub.uniform(-0.03, 0.03)
            pts.append((x, y, math.sin(math.pi * u)))
        G += T.splats(pts, 0.02) * 1.3
    return G * env, H * env


def _glaive(T, cx, cy, r, ang, w=0.05):
    """A glaive do Blade: o cabo reto no meio e, em cada ponta, a lâmina curva que volta para trás."""
    ux, uy = math.cos(ang), math.sin(ang)
    out = T.lines([(cx - ux * r * 0.6, cy - uy * r * 0.6, cx + ux * r * 0.6, cy + uy * r * 0.6, 1.0)], w * 0.35)
    for lado in (1, -1):
        ex, ey = cx + lado * ux * r * 0.55, cy + lado * uy * r * 0.55
        a0 = ang + (0 if lado > 0 else math.pi) - 0.3
        out = out + T.arc_band(r * 0.45, w, a0, a0 + 2.3, cx=ex, cy=ey, crescente=True)
    return out + T.gauss(cx, cy, r * 0.1)


def caca_preparo(T, t, rng):
    """O Preparo da Caçada noturna: a glaive de duas lâminas girando rápido (com o borrão do giro) na frente da
    lua minguante (laço)."""
    G, H = vazio(T)
    lua = T.arc_band(0.42, 0.16, 1.7, 1.7 + 3.0, cx=0.1, cy=0.0, crescente=True)
    G += lua * 0.35 + T.blur(lua, 0.03) * 0.3
    ang = TAU * t * 3
    for k in range(3):
        G += _glaive(T, 0, 0.05, 0.4, ang - 0.25 * k) * (1.0 if k == 0 else 0.3 / k)
    H += T.gauss(0, 0.05, 0.03) * 1.0
    return G, H


def cacada_noturna(T, t, rng):
    """A caçada noturna: a lua minguante surge no céu, a glaive voa girando em volta do rival numa elipse e corta
    três vezes ao passar por ele (os riscos ficam), e o golpe final em X."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    lua = T.arc_band(0.2, 0.08, 1.7, 1.7 + 3.0, cx=-0.6, cy=-0.62, crescente=True)
    G += (lua * 0.8 + T.blur(lua, 0.03) * 0.5) * pulso(t, 0.0, 0.95)
    voa = rel(t, 0.05, 0.6)
    if 0 < voa < 1:
        a = -math.pi + TAU * 1.5 * voa
        gx, gy = 0.55 * math.cos(a), 0.3 * math.sin(a)
        if voa < 0.1:
            gx, gy = -1.0 + (gx + 1.0) * voa / 0.1, gy
        G += _glaive(T, gx, gy, 0.24, t * 40, 0.045) * 1.4
        H += T.gauss(gx, gy, 0.03) * 1.0
        rastro = []
        for k in range(1, 6):
            vv = max(0.0, voa - 0.025 * k)
            aa = -math.pi + TAU * 1.5 * vv
            rastro.append((0.55 * math.cos(aa), 0.3 * math.sin(aa), 1 - k / 6))
        G += T.splats(rastro, 0.03) * 0.6
    cortes = ((0.18, -0.6, -0.3, 0.6, 0.25), (0.35, -0.6, 0.3, 0.6, -0.25), (0.52, -0.65, 0.0, 0.65, 0.05))
    for t0, x1, y1, x2, y2 in cortes:
        u = rel(t, t0, t0 + 0.1)
        s = 1 - rel(t, t0 + 0.12, t0 + 0.4)
        if u > 0 and s > 0:
            G += T.polys([(lamina(x1, y1, x2, y2, 0.03, prog=u), 1.0)]) * 1.3 * s
    final = rel(t, 0.62, 0.95)
    if 0 < final < 1:
        p = min(1, final * 4)
        X = T.polys([(lamina(-0.6, -0.6, 0.6, 0.6, 0.05, prog=p), 1.0), (lamina(0.6, -0.6, -0.6, 0.6, 0.05, prog=p), 1.0)])
        G += X * 1.4 * (1 - final)
        H += X * 0.5 * (1 - final) + T.gauss(0, 0, 0.1) * (1 - final) ** 2 * 1.6
    return G * env, H * env


REGISTRO = [
    ("absorcao_cosmica", absorcao_cosmica, GRANDE, "Capitã Marvel · a energia absorvida e a aura", False),
    ("rajada_binaria", rajada_binaria, GRANDE, "Capitã Marvel · os dois raios de fóton e a bola", False),
    ("binario_preparo", binario_preparo, MEDIA, "Capitã Marvel · o corpo em chamas cósmicas (Preparo, laço)", True),
    ("explosao_binaria", explosao_binaria, GRANDE, "Capitã Marvel · a estrela de oito pontas gigante", False),
    ("radar_sensorial", radar_sensorial, GRANDE, "Demolidor · as ondas do radar e o contorno", False),
    ("bastoes_em_cruz", bastoes_em_cruz, GRANDE, "Demolidor · os dois bastões em X", False),
    ("demolidor_preparo", demolidor_preparo, MEDIA, "Demolidor · os chifres e o radar (Preparo, laço)", True),
    ("contra_ataque_cego", contra_ataque_cego, GRANDE, "Demolidor · a rajada de golpes e o final", False),
    ("mira_fria", mira_fria, GRANDE, "Justiceiro · a luneta trava e a caveira", False),
    ("sniper_preparo", sniper_preparo, MEDIA, "Justiceiro · a luneta respirando (Preparo, laço)", True),
    ("alvo_confirmado", alvo_confirmado, GRANDE, "Justiceiro · a bala supersônica e o impacto", False),
    ("olhar_de_penitencia", olhar_de_penitencia, GRANDE, "Motoqueiro · a caveira em chamas e a onda de fogo", False),
    ("penitencia_preparo", penitencia_preparo, MEDIA, "Motoqueiro · a caveira e as chamas (Preparo, laço)", True),
    ("penance_stare", penance_stare, GRANDE, "Motoqueiro · os olhos, as espirais e as almas", False),
    ("rastreio_vampirico", rastreio_vampirico, GRANDE, "Blade · o rastro de sangue, as presas e a marca", False),
    ("lamina_de_prata", lamina_de_prata, GRANDE, "Blade · o corte de prata e o sangue de volta", False),
    ("caca_preparo", caca_preparo, MEDIA, "Blade · a glaive girando e a lua (Preparo, laço)", True),
    ("cacada_noturna", cacada_noturna, GRANDE, "Blade · a glaive em volta e o X final", False),
]
