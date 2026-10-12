"""Rodada 8 das habilidades próprias: Levi (Attack on Titan), Hisoka, Kurapika (Hunter x Hunter),
Edward e Alphonse (Fullmetal Alchemist).

Levi
- leitura_de_abertura: a leitura — três marquinhas de ponto fraco piscam no rival (os pequenos X),
  uma acende mais e vira o corte certeiro.
- giro_de_levi: o Giro cortante — o redemoinho de lâminas avança em espiral (a broca de cortes) e
  atravessa o rival, com o gás.
- levi_preparo: o Preparo da Execução — as duas lâminas em pegada invertida brilham e o gás chia em
  volta (laço).
- execucao_relampago: a Execução relâmpago — o clarão branco, e dezenas de cortes aparecem de uma
  vez no rival (como se ele já tivesse passado), depois o sangue e o vapor.

Hisoka
- bungee_gum: o Bungee Gum — o fio rosa de chiclete sai, gruda no rival (a bolota) e estica e volta
  como elástico, puxando.
- textura_surpresa: a Textura Surpresa — a carta de baralho vem girando (o naipe de espadas),
  crava, e a superfície descasca revelando a marca escondida.

Kurapika
- corrente_de_captura: a Corrente de captura — os elos da corrente se enrolam em volta do rival,
  um anel por vez, e travam (o cadeado acende).
- corrente_do_julgamento: a Corrente do julgamento — a corrente reta com a ponta afiada crava no
  coração (o contorno do coração), e o anel da promessa fecha em volta.
- olhos_escarlates: os Olhos escarlates — os dois olhos vermelhos se abrem grandes, as íris acendem,
  e o pulso de pressão paralisa.

Edward
- lanca_de_pedra: as palmas batem (o clarão das mãos), os raios azuis da alquimia correm pelo chão
  e a lança de pedra sobe com as lascas.
- muralha_alquimica: o muro de pedra sobe tijolo por tijolo com os raios alquímicos, e os espinhos
  saem da frente dele.

Alphonse
- armadura_de_aco: as placas da armadura (retângulos de aço com rebites) chegam e se fecham no
  aliado, e o reflexo do metal passa.
- circulo_protetor: o círculo de transmutação desenhado — o círculo, o triângulo e o quadrado
  inscritos e as runas — acende no chão e a luz sobe protegendo.
- barreira_transmutada: as cúpulas de pedra sobem do chão em volta do trio (três abóbadas de lajes),
  com os raios alquímicos.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _xis(cx, cy, r, w=1.0):
    return [(cx - r, cy - r, cx + r, cy + r, w), (cx - r, cy + r, cx + r, cy - r, w)]


def _alquimia(T, t, seed, n, cx, cy, alcance, t0=0.0, t1=1.0):
    """Os raios azuis da alquimia: arcos curtos e tortos que pulam pelo chão em volta do ponto."""
    out = T.zero()
    vida = pulso(t, t0, t1)
    if vida <= 0:
        return out
    q = np.random.default_rng(seed + int(t * 24))
    for _ in range(n):
        a = q.uniform(0, TAU)
        r0 = q.uniform(0.05, alcance)
        x1, y1 = cx + r0 * math.cos(a), cy + r0 * math.sin(a) * 0.35
        x2, y2 = x1 + q.uniform(-0.2, 0.2), y1 + q.uniform(-0.18, 0.04)
        out += T.polyline(jagged(q, x1, y1, x2, y2, 3, 0.45), 0.008)
    return out * vida


# =================================================================== Levi
def leitura_de_abertura(T, t, rng):
    """Três marquinhas de ponto fraco (X pequenos) piscam no rival, uma depois da outra; a do meio acende
    mais forte, e o corte certeiro sai exatamente nela."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    pontos = ((-0.25, -0.3), (0.28, -0.05), (-0.05, 0.25))
    for k, (x, y) in enumerate(pontos):
        acende = pulso(t, 0.05 + 0.1 * k, 0.6)
        pisca = 0.6 + 0.4 * math.sin(t * 50 + k)
        X = T.lines(_xis(x, y, 0.085), 0.016)
        G += (X * 1.2 + T.ring(0.1, 0.01, x, y) * 0.8) * acende * pisca
    escolhido = pontos[1]
    mira = pulso(t, 0.35, 0.6)
    G += T.ring(0.14 - 0.06 * rel(t, 0.35, 0.5), 0.015, *escolhido) * mira * 1.4
    corta = ease_out(rel(t, 0.5, 0.6), 2)
    if corta > 0:
        x, y = escolhido
        L = T.polys([(lamina(x - 0.55, y + 0.35, x + 0.55, y - 0.35, 0.05, corta, rel(t, 0.62, 0.9)), 1.0)])
        G += L * 1.5 + T.blur(L, 0.02) * 0.5
        H += L * 0.9
    flash = pulso(t, 0.5, 0.7)
    H += T.flare(*escolhido, 0.8 * flash + 0.01, -0.6, 0.015) * flash
    return G * env, H * env


def giro_de_levi(T, t, rng):
    """O Giro cortante: o redemoinho de lâminas avança da esquerda em espiral (anéis de corte achatados,
    um atrás do outro, como uma broca), atravessa o rival e deixa os riscos e o gás."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    avanca = ease_in(rel(t, 0.0, 0.5), 1.4)
    cx = -0.9 + 1.4 * avanca
    for k in range(6):
        x = cx - 0.12 * k
        fase = t * 30 + k * 1.1
        if x < -0.95:
            continue
        a0 = fase % TAU
        G += T.arc_band(0.4 - 0.025 * k, 0.06, a0, a0 + 2.6, squash=0.32, rot=math.pi / 2, cx=x, taper=0.5) * (1 - 0.12 * k) * 1.5 * (1 - rel(t, 0.55, 0.8))
        H += T.arc_band(0.4 - 0.025 * k, 0.02, a0 + 1.6, a0 + 2.6, squash=0.32, rot=math.pi / 2, cx=x, taper=0.5) * (1 - 0.15 * k) * (1 - rel(t, 0.5, 0.7))
    passou = rel(t, 0.35, 0.8)
    if passou > 0:
        riscos = []
        sub = np.random.default_rng(14)
        for _ in range(7):
            y = sub.uniform(-0.3, 0.3)
            riscos.append((-0.35, y - 0.05, 0.35, y + 0.05, 1 - passou))
        G += T.tapered(riscos, 0.035) * 1.2
        H += T.tapered(riscos, 0.015) * (1 - passou)
    sub = np.random.default_rng(3)
    gas = [(cx - 0.3 - sub.uniform(0, 0.4), sub.uniform(-0.15, 0.15), 0.6) for _ in range(14)]
    G += T.splats(gas, 0.05) * 0.5 * (1 - rel(t, 0.5, 0.8))
    return G * env, H * env


def levi_preparo(T, t, rng):
    """O Preparo da Execução: as duas lâminas em pegada invertida (para baixo, cruzando), o brilho que
    corre pelo fio, e o gás chiando em volta (laço)."""
    G, H = vazio(T)
    for lado in (-1, 1):
        L = T.polys([(lamina(0.12 * lado, -0.1, 0.45 * lado, 0.5, 0.035, 1.0), 1.0)])
        G += L * 0.9 + T.blur(L, 0.02) * 0.4
        u = (t * 2 + (0.5 if lado > 0 else 0)) % 1
        H += T.gauss(0.12 * lado + 0.33 * lado * u, -0.1 + 0.6 * u, 0.03) * 1.2
    sub = np.random.default_rng(8)
    pts = []
    for _ in range(14):
        f = (sub.uniform() + t) % 1
        a = sub.uniform(0, TAU)
        pts.append((0.3 * math.cos(a) * (1 + f), 0.2 + 0.25 * math.sin(a) - 0.3 * f, 1 - f))
    G += T.splats(pts, 0.04) * 0.5
    return G, H


def execucao_relampago(T, t, rng):
    """A Execução relâmpago: o clarão branco (ninguém vê o movimento), e no instante seguinte o rival já
    está cheio de cortes — dezenas de riscos ao mesmo tempo, em todas as direções — que se abrem; depois
    o sangue e o vapor sobem."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    clarao = pulso(t, 0.0, 0.18)
    G += T.gauss(0, 0, 0.3) * clarao * 1.4
    H += (T.gauss(0, 0, 0.12) * 1.5 + T.flare(0, 0, 1.2 * clarao + 0.01, 0.3, 0.012)) * clarao
    aparece = rel(t, 0.15, 0.2)
    abre = ease_out(rel(t, 0.2, 0.55), 2)
    some = 1 - rel(t, 0.5, 0.8)
    if aparece > 0:
        sub = np.random.default_rng(29)
        shapes = []
        for _ in range(26):
            a = sub.uniform(0, math.pi)
            cx, cy = sub.uniform(-0.45, 0.45), sub.uniform(-0.5, 0.5)
            comp = sub.uniform(0.15, 0.45)
            shapes.append((lamina(cx - comp * math.cos(a), cy - comp * math.sin(a), cx + comp * math.cos(a), cy + comp * math.sin(a), 0.012 + 0.018 * abre), 1.0))
        C = T.polys(shapes)
        G += C * 1.4 * some
        H += C * (1.0 - 0.5 * abre) * some
    sub = np.random.default_rng(30)
    gotas = []
    for _ in range(30):
        a = sub.uniform(0, TAU)
        d = sub.uniform(0.1, 0.7) * abre
        gotas.append((d * math.cos(a), d * math.sin(a) + 0.2 * abre * abre, (1 - abre) * sub.uniform(0.4, 1)))
    G += T.splats(gotas, 0.013) * 1.1 * (aparece > 0)
    vapor = rel(t, 0.45, 1.0)
    if vapor > 0:
        pts = [(sub.uniform(-0.4, 0.4), 0.2 - 0.8 * vapor * sub.uniform(0.6, 1), (1 - vapor) * 0.7) for _ in range(16)]
        G += T.splats(pts, 0.07) * 0.7
    return G * env, H * env


# =================================================================== Hisoka
def bungee_gum(T, t, rng):
    """O Bungee Gum: o fio rosa sai da esquerda, gruda no rival (a bolota que achata), estica e volta
    como elástico, oscilando, e puxa (o rival treme)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    sai = ease_out(rel(t, 0.0, 0.25), 2)
    ox, oy = -0.95, 0.15
    alvo = (0.05, -0.05)
    oscila = math.sin(rel(t, 0.25, 0.85) * TAU * 3) * (1 - rel(t, 0.25, 0.85)) * 0.28
    pts = []
    for u in np.linspace(0, sai, 30):
        x = ox + (alvo[0] - ox) * u
        y = oy + (alvo[1] - oy) * u + math.sin(math.pi * u) * oscila
        pts.append((x, y))
    if len(pts) > 1:
        F = T.polyline(pts, 0.05)
        G += F * 1.1 + T.blur(F, 0.02) * 0.5
        H += T.polyline(pts, 0.01) * 0.6
    gruda = rel(t, 0.22, 0.3)
    if gruda > 0:
        achata = 1 + 0.4 * pulso(t, 0.22, 0.45)
        bolota = T.gauss(alvo[0], alvo[1], 0.09 * achata, 0.07 / achata)
        G += bolota * 1.4
        H += T.gauss(alvo[0] - 0.02, alvo[1] - 0.02, 0.03) * 0.8
        gotas = [(alvo[0] + 0.12 * math.cos(a), alvo[1] + 0.09 * math.sin(a), pulso(t, 0.22, 0.5)) for a in np.linspace(0, TAU, 7, endpoint=False)]
        G += T.splats(gotas, 0.02) * 0.9
    # o naipe de copas no fio, a marca do Hisoka
    copas = T.polys([(estrela(-0.45, 0.1 + oscila * 0.5, 0.0, 0, 1), 1.0)]) * 0
    G += copas
    return G * env, H * env


def _carta(cx, cy, larg, alt, ang):
    pts = [(-larg, -alt), (larg, -alt), (larg, alt), (-larg, alt)]
    return _gira(pts, ang, cx, cy)


def _espadas(cx, cy, s, ang=0.0):
    """O naipe de espadas: o coração de cabeça para baixo e o cabinho."""
    pts = []
    for a in np.linspace(0, TAU, 30, endpoint=False):
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((x / 17 * s, -y / 17 * s - 0.1 * s))
    pts += [(0.05 * s, 0.75 * s), (-0.05 * s, 0.75 * s)]
    return _gira(pts, ang, cx, cy)


def textura_surpresa(T, t, rng):
    """A Textura Surpresa: a carta vem girando (com o naipe de espadas no meio), crava no rival de lado,
    e a 'pele' descasca de cima para baixo revelando a marca escondida que acende."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.3), 1.6)
    cx, cy = -0.9 + 0.9 * vem, -0.5 + 0.45 * vem
    ang = t * 30 if t < 0.3 else 0.35
    if t >= 0.3:
        cx, cy = 0.0, -0.05
    C = T.polys([(_carta(cx, cy, 0.21, 0.3, ang), 1.0)])
    borda = np.clip(C - T.blur(C, 0.008) * 1.1, 0, 1)
    N = T.polys([(_espadas(cx, cy - 0.03, 0.14, ang), 1.0)])
    G += (C * 0.35 + borda * 1.1 + N * 0.9) * (1 - rel(t, 0.75, 0.95))
    H += borda * 0.5
    if t < 0.3:
        G += T.tapered([(cx - 0.4, cy - 0.25, cx, cy, 0.6)], 0.05) * vem
    crava = pulso(t, 0.28, 0.5)
    H += T.flare(0, -0.05, 0.6 * crava + 0.01, 0.35, 0.02) * crava
    descasca = rel(t, 0.4, 0.75)
    if descasca > 0:
        y0 = -0.4 + 0.8 * descasca
        aba = T.polys([([(-0.4, -0.4), (0.4, -0.4), (0.4, y0), (-0.4, y0)], 1.0)])
        G += aba * 0.18 * (1 - descasca)
        G += T.lines([(-0.42, y0, 0.42, y0 + 0.04, 1.0)], 0.012) * (1 - descasca) * 1.2
        marca = T.polys([(estrela(0.0, 0.05, 0.16, -math.pi / 2, 4, 0.35), 1.0)]) * (T.V < y0)
        G += marca * 1.2 * descasca
        H += marca * 0.6 * descasca
    return G * env, H * env


# =================================================================== Kurapika
def _elos(T, pts, tam=0.035):
    """A corrente: elos ovais alternando de lado (em pé e deitado) ao longo do caminho."""
    shapes = T.zero()
    for k in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[k], pts[k + 1]
        ang = math.atan2(y2 - y1, x2 - x1)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        achata = 0.45 if k % 2 == 0 else 0.2
        shapes += T.ring(tam, tam * 0.3, mx, my, squash=1.0) * 0 + T.arc_band(tam, tam * 0.35, 0, TAU - 0.01, squash=achata, rot=ang, cx=mx, cy=my, taper=0.0)
    return shapes


def corrente_de_captura(T, t, rng):
    """A Corrente de captura: a corrente chega e se enrola em volta do rival, anel por anel, apertando;
    no fim o cadeado (o arco e o corpo) acende no ponto em que ela fecha."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    enrola = ease_out(rel(t, 0.0, 0.6), 1.6)
    aperta = rel(t, 0.55, 0.75)
    pts = []
    n = 150
    for k in range(n):
        u = k / (n - 1)
        if u > enrola:
            break
        a = u * TAU * 2.6 - math.pi / 2
        r = (0.55 - 0.2 * u) * (1 - 0.15 * aperta)
        pts.append((r * math.cos(a), 0.05 + r * math.sin(a) * 0.55 + 0.3 * (u - 0.5)))
    if len(pts) > 2:
        E = _elos(T, pts, 0.032)
        G += E * 1.2 + T.blur(E, 0.015) * 0.4
        H += E * 0.3
    trava = pulso(t, 0.6, 1.0)
    if trava > 0:
        corpo = T.polys([([(-0.06, 0.32), (0.06, 0.32), (0.06, 0.44), (-0.06, 0.44)], 1.0)])
        arco = T.arc_band(0.045, 0.012, math.pi, TAU, cx=0, cy=0.32, taper=0.0)
        G += (corpo + arco * 1.2) * trava * 1.2
        H += T.flare(0, 0.38, 0.4 * trava + 0.01, 0.0, 0.03) * trava
    return G * env, H * env


def _coracao(cx, cy, s):
    pts = []
    for a in np.linspace(0, TAU, 40, endpoint=False):
        x = 16 * math.sin(a) ** 3
        y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        pts.append((cx + x / 17 * s, cy - y / 17 * s))
    return pts


def corrente_do_julgamento(T, t, rng):
    """A Corrente do julgamento: a corrente reta dispara com a ponta afiada, crava no coração do rival
    (o contorno do coração acende), e o anel da promessa fecha em volta dele, apertando."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_out(rel(t, 0.0, 0.3), 2)
    ox, oy = -0.95, -0.2
    tx, ty = 0.0, 0.0
    hx, hy = ox + (tx - ox) * vem, oy + (ty - oy) * vem
    pts = [(ox + (hx - ox) * u, oy + (hy - oy) * u) for u in np.linspace(0, 1, 12)]
    E = _elos(T, pts, 0.035)
    G += E * 1.1 * (1 - rel(t, 0.8, 0.95))
    ang = math.atan2(ty - oy, tx - ox)
    ponta = T.polys([(lamina(hx - 0.1 * math.cos(ang), hy - 0.1 * math.sin(ang), hx + 0.12 * math.cos(ang), hy + 0.12 * math.sin(ang), 0.04), 1.0)])
    G += ponta * 1.4
    H += ponta * 0.6
    cor = pulso(t, 0.28, 1.0)
    C = T.polyline(_coracao(0.0, 0.0, 0.22) + [_coracao(0.0, 0.0, 0.22)[0]], 0.016)
    G += C * cor * 1.3 + T.gauss(0, 0, 0.1) * cor * 0.6
    fecha = ease_out(rel(t, 0.4, 0.7), 2)
    if fecha > 0:
        G += T.ring(0.6 - 0.28 * fecha, 0.02) * (1 - rel(t, 0.75, 0.95)) * 1.3
    H += T.gauss(0, 0, 0.04) * pulso(t, 0.28, 0.5) * 1.5
    return G * env, H * env


def _olho(T, cx, cy, larg, abre):
    pts = [(cx + larg * math.cos(a), cy + larg * 0.42 * abre * math.sin(a)) for a in np.linspace(0, TAU, 36, endpoint=False)]
    return T.polys([(pts, 1.0)])


def olhos_escarlates(T, t, rng):
    """Os Olhos escarlates: os dois olhos se abrem grandes (as pálpebras), as íris vermelhas acendem com o
    brilho, e o pulso de pressão sai em anéis e prende o rival (Paralisado)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    abre = back(rel(t, 0.0, 0.3), 1.3)
    for lado in (-1, 1):
        cx, cy = 0.33 * lado, -0.15
        O = _olho(T, cx, cy, 0.22, max(0.02, abre))
        iris = T.gauss(cx, cy, 0.075 * min(1, abre * 1.2)) * O
        pupila = T.gauss(cx, cy, 0.025)
        borda = np.clip(O - T.blur(O, 0.01) * 1.1, 0, 1)
        G += borda * 1.1 + iris * 1.6 + O * 0.15
        G -= pupila * 0.6 * abre
        H += iris * 0.7 * pulso(t, 0.15, 0.9) + T.gauss(cx - 0.03, cy - 0.03, 0.015) * abre
    pulsa = rel(t, 0.35, 0.85)
    if pulsa > 0:
        for k in range(2):
            u = rel(t, 0.35 + 0.1 * k, 0.85 + 0.1 * k)
            G += T.ring(0.15 + 0.7 * ease_out(u, 1.6), 0.03, 0, 0.15) * (1 - u) * 1.2 * (u > 0)
    return G * env, H * env


# =================================================================== Edward
def lanca_de_pedra(T, t, rng):
    """A Lança de pedra: as palmas batem (o clarão das mãos à esquerda), os raios azuis da alquimia
    correm pelo chão até o rival, e a lança de pedra sobe de baixo, pontuda, com as lascas voando."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    palmas = pulso(t, 0.0, 0.18)
    G += T.gauss(-0.75, -0.2, 0.08) * palmas * 1.6
    H += T.flare(-0.75, -0.2, 0.5 * palmas + 0.01, 0.0, 0.03) * palmas
    corre = ease_out(rel(t, 0.1, 0.35), 2)
    if corre > 0:
        q = np.random.default_rng(int(t * 30))
        G += T.polyline(jagged(q, -0.75, 0.45, -0.75 + 0.75 * corre, 0.45, 5, 0.25), 0.012) * 1.3 * (1 - rel(t, 0.4, 0.6))
    G += _alquimia(T, t, 50, 8, 0.0, 0.45, 0.35, 0.25, 0.7) * 1.3
    sobe = back(rel(t, 0.32, 0.5), 1.3)
    if sobe > 0:
        alt = 1.0 * sobe
        lanca = T.polys([([(-0.13, 0.48), (-0.05, 0.48 - alt * 0.8), (0.03, 0.45 - alt), (0.13, 0.48)], 1.0)])
        faces = T.lines([(-0.02, 0.48, 0.0, 0.48 - alt * 0.85, 1.0)], 0.01)
        G += (lanca * 0.7 + T.blur(lanca, 0.02) * 0.4 + faces * 0.6) * (1 - rel(t, 0.75, 0.95))
        H += np.clip(lanca - T.blur(lanca, 0.008), 0, 1) * 0.6
    sub = np.random.default_rng(51)
    lascas = []
    voa = rel(t, 0.35, 0.9)
    for _ in range(16):
        a = sub.uniform(-math.pi * 0.9, -math.pi * 0.1)
        d = sub.uniform(0.2, 0.6) * ease_out(voa, 2)
        lascas.append((d * math.cos(a), 0.45 + d * math.sin(a) + 0.4 * voa * voa, (1 - voa) * (voa > 0)))
    G += T.splats(lascas, 0.016) * 1.1
    return G * env, H * env


def muralha_alquimica(T, t, rng):
    """A Muralha alquímica: os raios correm pelo chão, o muro de pedra sobe tijolo por tijolo (fileira
    a fileira), e os espinhos saem da frente dele."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    G += _alquimia(T, t, 60, 10, 0.0, 0.5, 0.6, 0.0, 0.6) * 1.2
    sobe = rel(t, 0.15, 0.55)
    tijolos = []
    for fila in range(5):
        if sobe * 5 < fila:
            break
        cresce = min(1.0, sobe * 5 - fila)
        y0 = 0.5 - 0.17 * fila
        off = 0.1 if fila % 2 else 0.0
        for k in range(5):
            x0 = -0.55 + off + 0.21 * k
            if x0 > 0.5:
                continue
            tijolos.append(([(x0, y0), (x0 + 0.19, y0), (x0 + 0.19, y0 - 0.15 * cresce), (x0, y0 - 0.15 * cresce)], 1.0))
    if tijolos:
        M = T.polys(tijolos)
        juntas = np.clip(M - T.blur(M, 0.006) * 1.1, 0, 1)
        some = 1 - rel(t, 0.8, 0.98)
        G += (M * 0.5 + juntas * 0.8) * some
        H += juntas * 0.3 * some
    espinhos = ease_out(rel(t, 0.5, 0.65), 2)
    if espinhos > 0:
        shapes = []
        for k in range(6):
            x = -0.45 + 0.18 * k
            y = 0.1 + 0.08 * (k % 2)
            shapes.append(([(x, y - 0.04), (x, y + 0.04), (x + 0.22 * espinhos, y)], 1.0))
        G += T.polys(shapes) * 1.2 * (1 - rel(t, 0.8, 0.98))
    return G * env, H * env


# =================================================================== Alphonse
def armadura_de_aco(T, t, rng):
    """A Armadura de aço: as placas retangulares de aço com rebites chegam de fora e se fecham em volta
    do aliado (peito, ombros, braços), e o reflexo do metal passa."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    placas = [(-0.22, -0.35, 0.44, 0.32), (-0.48, -0.35, 0.22, 0.2), (0.26, -0.35, 0.22, 0.2),
              (-0.5, -0.12, 0.2, 0.42), (0.3, -0.12, 0.2, 0.42), (-0.22, 0.0, 0.44, 0.22), (-0.18, 0.25, 0.36, 0.18)]
    sub = np.random.default_rng(4)
    todas = T.zero()
    rebites = []
    for k, (x, y, w, h) in enumerate(placas):
        t0 = 0.03 + 0.06 * k
        chega = ease_out(rel(t, t0, t0 + 0.2), 2)
        if chega <= 0:
            continue
        cx, cy = x + w / 2, y + h / 2
        ang = math.atan2(cy, cx) if (cx or cy) else -math.pi / 2
        d = 0.5 * (1 - chega)
        dx, dy = d * math.cos(ang), d * math.sin(ang)
        P = T.polys([([(x + dx, y + dy), (x + w + dx, y + dy), (x + w + dx, y + h + dy), (x + dx, y + h + dy)], 1.0)])
        todas += P
        for (rx, ry) in ((x + 0.03, y + 0.03), (x + w - 0.03, y + 0.03), (x + 0.03, y + h - 0.03), (x + w - 0.03, y + h - 0.03)):
            rebites.append((rx + dx, ry + dy, chega))
    bordas = np.clip(todas - T.blur(todas, 0.006) * 1.2, 0, 1)
    G += todas * 0.4 + bordas * 1.0 + T.splats(rebites, 0.008) * 1.2
    H += bordas * 0.4
    reflexo = rel(t, 0.5, 0.85)
    if reflexo > 0:
        banda = np.exp(-((T.U - T.V * 0.5 - (-1.0 + 2.2 * reflexo)) / 0.07) ** 2)
        H += banda * np.clip(todas, 0, 1) * 1.1
    return G * env, H * env


def circulo_protetor(T, t, rng):
    """O Círculo protetor: o círculo de transmutação se desenha no chão (o círculo de fora, o triângulo,
    o quadrado e o círculo de dentro, com as runas), acende, e a luz sobe em coluna protegendo."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    sq = 0.32
    cy = 0.42

    def chao(pts):
        return [(x, cy + y * sq) for x, y in pts]

    d1 = ease_out(rel(t, 0.0, 0.25), 2)
    if d1 > 0:
        G += T.arc_band(0.6, 0.02, -math.pi / 2, -math.pi / 2 + TAU * d1 + 0.01, squash=sq, cy=cy, taper=0.0) * 1.2
    d2 = ease_out(rel(t, 0.15, 0.4), 2)
    if d2 > 0:
        tri = [(0.58 * math.cos(-math.pi / 2 + TAU * k / 3), 0.58 * math.sin(-math.pi / 2 + TAU * k / 3)) for k in range(4)]
        qua = [(0.4 * math.cos(math.pi / 4 + TAU * k / 4), 0.4 * math.sin(math.pi / 4 + TAU * k / 4)) for k in range(5)]
        n_tri = max(2, int(len(tri) * d2 + 0.999))
        G += T.polyline(chao(tri[:n_tri]), 0.012) * 1.1
        G += T.polyline(chao(qua[:max(2, int(len(qua) * d2 + 0.999))]), 0.012) * 1.0
        G += T.ring(0.22, 0.012, 0, cy, squash=1 / sq) * d2
        runas = [(0.5 * math.cos(a), cy + 0.5 * math.sin(a) * sq, d2) for a in np.linspace(0, TAU, 10, endpoint=False)]
        G += T.splats(runas, 0.014) * 0.9
    acende = pulso(t, 0.35, 0.95)
    G += T.gauss(0, cy, 0.6, 0.2) * acende * 0.4
    coluna = rel(t, 0.4, 0.9)
    if coluna > 0:
        C = np.exp(-(T.U / 0.35) ** 4) * np.clip((cy - T.V) / 1.0, 0, 1) ** 0.6 * (T.V < cy) * (T.V > cy - 1.1 * ease_out(coluna, 2))
        G += C * 0.6 * (1 - rel(t, 0.75, 1))
        H += C * 0.2 * (1 - rel(t, 0.75, 1))
        sub = np.random.default_rng(6)
        pts = [(sub.uniform(-0.3, 0.3), cy - ((sub.uniform() + t) % 1) * 0.9, 0.7) for _ in range(14)]
        G += T.splats(pts, 0.015) * 0.8 * coluna
    return G * env, H * env


def barreira_transmutada(T, t, rng):
    """A Barreira transmutada: os raios correm pelo chão e três cúpulas de lajes de pedra sobem em volta do
    trio (as abóbadas com as juntas), uma depois da outra, e brilham na borda."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    G += _alquimia(T, t, 70, 12, 0.0, 0.5, 0.8, 0.0, 0.5) * 1.1
    for k, cx in enumerate((-0.55, 0.0, 0.55)):
        sobe = back(rel(t, 0.15 + 0.1 * k, 0.45 + 0.1 * k), 1.2)
        if sobe <= 0:
            continue
        r = 0.27
        alt = r * sobe
        cupula = T.zero()
        pts = [(cx + r * math.cos(a), 0.5 - alt * math.sin(a)) for a in np.linspace(0, math.pi, 24)]
        D = T.polys([(pts, 1.0)])
        juntas = T.zero()
        for j in range(1, 4):
            a = math.pi * j / 4
            juntas += T.lines([(cx, 0.5 - alt, cx + r * math.cos(a), 0.5 - alt * math.sin(a), 1.0)], 0.006) * 0
            yy = 0.5 - alt * j / 4
            ww = r * math.sqrt(max(0.0, 1 - (j / 4) ** 2))
            juntas += T.lines([(cx - ww, yy, cx + ww, yy, 1.0)], 0.007)
        for j in (-1, 0, 1):
            juntas += T.lines([(cx + j * r * 0.45, 0.5, cx + j * r * 0.25, 0.5 - alt * 0.85, 1.0)], 0.007)
        borda = np.clip(D - T.blur(D, 0.008) * 1.1, 0, 1)
        some = 1 - rel(t, 0.8, 0.98)
        G += (D * 0.35 + borda * 1.1 + juntas * D * 0.8) * some
        H += borda * 0.4 * some
    return G * env, H * env


REGISTRO = [
    ("leitura_de_abertura", leitura_de_abertura, GRANDE, "Levi · os pontos fracos piscam e o corte certeiro", False),
    ("giro_de_levi", giro_de_levi, GRANDE, "Levi · o redemoinho de lâminas em espiral", False),
    ("levi_preparo", levi_preparo, MEDIA, "Levi · as lâminas invertidas e o gás (Preparo, laço)", True),
    ("execucao_relampago", execucao_relampago, GRANDE, "Levi · o clarão e os cortes de uma vez", False),
    ("bungee_gum", bungee_gum, GRANDE, "Hisoka · o chiclete rosa que gruda e estica", False),
    ("textura_surpresa", textura_surpresa, GRANDE, "Hisoka · a carta que crava e descasca", False),
    ("corrente_de_captura", corrente_de_captura, GRANDE, "Kurapika · os elos que se enrolam e o cadeado", False),
    ("corrente_do_julgamento", corrente_do_julgamento, GRANDE, "Kurapika · a ponta no coração e o anel", False),
    ("olhos_escarlates", olhos_escarlates, GRANDE, "Kurapika · os olhos vermelhos e o pulso", False),
    ("lanca_de_pedra", lanca_de_pedra, GRANDE, "Edward · as palmas, os raios e a lança de pedra", False),
    ("muralha_alquimica", muralha_alquimica, GRANDE, "Edward · o muro de tijolos e os espinhos", False),
    ("armadura_de_aco", armadura_de_aco, GRANDE, "Alphonse · as placas de aço com rebites", False),
    ("circulo_protetor", circulo_protetor, GRANDE, "Alphonse · o círculo de transmutação e a luz", False),
    ("barreira_transmutada", barreira_transmutada, GRANDE, "Alphonse · as cúpulas de pedra em volta do trio", False),
]
