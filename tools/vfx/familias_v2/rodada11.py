"""Rodada 11 das habilidades próprias: Loid e Yor (Spy x Family), Sung Jinwoo (Solo Leveling), Ken Kaneki
(Tokyo Ghoul) e Yugi (Yu-Gi-Oh!).

Loid
- identidade_falsa: o disfarce — a máscara com o chapéu aparece, rasga ao meio (as metades caem para os
  lados) e por trás a mira do espião se fecha no rival (Marcado), com as setas de Enfraquecido.
- neutralizacao_silenciosa: o tiro com silenciador — a baforada pequena no cano, o traço fino da bala e
  o impacto preciso; a barra do Preparo do rival quebra ao meio e cai.
- plano_de_fuga: a bomba de fumaça cai, estoura numa nuvem grande, e as setas tracejadas da rota de
  fuga saem correndo de dentro dela.

Yor
- investida_elegante: o chute alto girando — a meia-lua comprida com o calcanhar aceso, as pétalas de
  rosa voando no rastro e o estalo que paralisa.
- espinho_preparo: o Preparo do Jardim — os ramos com espinhos girando em volta e o brilho correndo nos
  dois estiletes (laço).
- jardim_noturno: os dois estiletes dourados cruzam em X, a rosa escura desabrocha no rival (três
  camadas de pétalas abrindo) e as pétalas se espalham.

Jinwoo
- comando_avancem: a poça de sombra no chão, os pares de olhos dos soldados acendendo em fileiras, e
  todos avançam juntos em riscos escuros até o rival; um fiapo de vida volta.

Kaneki
- fome_de_ghoul: o kakugan abre (o olho com a íris vermelha), as veias pulsam saindo dele, e a vida é
  puxada de fora para dentro em espiral, com dois batimentos.
- kakuja_preparo: o Preparo do Centípede — os quatro tentáculos rinkaku saindo das costas e balançando
  (laço).
- centopeia: o kagune centopeia — o corpo segmentado, com as patas em cada gomo, serpenteia e crava no
  rival; o sangue volta pelo corpo (Vampirismo).

Yugi
- preparar_o_duelo: o Enigma do Milênio acende (o triângulo invertido com o olho), as cinco cartas
  abrem em leque, uma delas gira e voa no rival, e a Carga sobe em faíscas.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _desloca(T, a, dx, dy):
    return T.warp(a, np.full_like(a, dx), np.full_like(a, dy))


def _borda(T, a, s=0.008):
    return np.clip(a - T.blur(a, s), 0, 1)


def _petala(cx, cy, tam, ang):
    """A pétala: uma lente curta girada."""
    dx, dy = math.cos(ang) * tam, math.sin(ang) * tam
    return lamina(cx - dx, cy - dy, cx + dx, cy + dy, tam * 0.55)


def _petalas_voando(T, t, seed, n, t0, cx, cy, alcance, ang0, ang1, tam=0.045, dur=0.55):
    u = rel(t, t0, t0 + dur)
    if u <= 0 or u >= 1:
        return T.zero()
    sub = np.random.default_rng(seed)
    shapes = []
    for _ in range(n):
        a = sub.uniform(ang0, ang1)
        d = sub.uniform(0.3, 1.0) * alcance * ease_out(u, 2)
        gira = sub.uniform(-6, 6) * u + sub.uniform(0, TAU)
        x = cx + d * math.cos(a) + 0.05 * math.sin(gira * 2)
        y = cy + d * math.sin(a) + 0.25 * u * u
        shapes.append((_petala(x, y, tam * sub.uniform(0.7, 1.2), gira), (1 - u) * sub.uniform(0.6, 1)))
    return T.polys(shapes)


# =================================================================== Loid
def _mascara(T, cx, cy, s):
    """O rosto do disfarce: o contorno oval, os olhos e a boca em traço, e o chapéu (a aba e a copa)."""
    M = T.ring(0.3 * s, 0.022 * s, cx, cy, squash=0.74)
    M += T.lines([(cx - 0.17 * s, cy - 0.06 * s, cx - 0.06 * s, cy - 0.05 * s, 1.0),
                  (cx + 0.06 * s, cy - 0.05 * s, cx + 0.17 * s, cy - 0.06 * s, 1.0),
                  (cx - 0.08 * s, cy + 0.2 * s, cx + 0.08 * s, cy + 0.2 * s, 0.8)], 0.022 * s)
    aba = [(cx + 0.48 * s * math.cos(a), cy - 0.36 * s + 0.07 * s * math.sin(a)) for a in np.linspace(0, TAU, 30, endpoint=False)]
    copa = [(cx - 0.26 * s, cy - 0.38 * s), (cx - 0.22 * s, cy - 0.64 * s), (cx, cy - 0.58 * s),
            (cx + 0.22 * s, cy - 0.64 * s), (cx + 0.26 * s, cy - 0.38 * s)]
    C = T.polys([(aba, 1.0), (copa, 1.0)])
    return M, C


def identidade_falsa(T, t, rng):
    """O disfarce do Loid: a máscara com o chapéu aparece, rasga ao meio num corte em zigue-zague (as metades
    caem para os lados, girando), e por trás a mira do espião se fecha no rival (Marcado), com as setinhas
    de Enfraquecido descendo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    aparece = back(rel(t, 0.0, 0.2), 1.3)
    if aparece > 0 and t < 0.7:
        M, C = _mascara(T, 0, -0.08, 0.95 * aparece)
        F = M * 1.2 + C * 0.55 + _borda(T, C, 0.01) * 0.9
        rasga = ease_in(rel(t, 0.3, 0.6), 2)
        corte = 0.035 * np.sign(np.sin(T.V * 38))
        esq = F * (T.U < corte)
        dir_ = F * (T.U >= corte)
        if rasga > 0:
            esq = _desloca(T, esq, -0.45 * rasga, 0.35 * rasga * rasga)
            dir_ = _desloca(T, dir_, 0.45 * rasga, 0.4 * rasga * rasga)
        G += (esq + dir_) * (1 - rel(t, 0.45, 0.68))
        H += T.lines([(c, -0.7, c, 0.4, 1.0) for c in (0.0,)], 0.012) * pulso(t, 0.27, 0.4) * 1.2
    mira = ease_out(rel(t, 0.38, 0.65), 3)
    if mira > 0:
        r = 0.65 - 0.33 * mira
        gira = 1.2 * (1 - mira)
        G += T.ring(r, 0.016, 0, 0.0) * 1.3
        G += T.arc_band(r + 0.08, 0.02, gira, gira + 1.2, cx=0, cy=0, taper=0.3) * 1.0
        G += T.arc_band(r + 0.08, 0.02, gira + math.pi, gira + math.pi + 1.2, cx=0, cy=0, taper=0.3) * 1.0
        ticks = []
        for k in range(4):
            a = gira + k * math.pi / 2
            ticks.append((math.cos(a) * (r - 0.12), math.sin(a) * (r - 0.12), math.cos(a) * (r + 0.05), math.sin(a) * (r + 0.05), 1.0))
        G += T.lines(ticks, 0.02) * 1.3
        trava = pulso(t, 0.62, 0.82)
        H += (T.gauss(0, 0, 0.035) * 1.6 + T.flare(0, 0, 0.35 * trava + 0.01, 0.785, 0.012)) * (0.4 + trava)
    desce = rel(t, 0.66, 1.0)
    if desce > 0:
        setas = []
        for k, x in enumerate((-0.42, 0.42)):
            y = 0.15 + 0.3 * ease_out(desce, 2)
            setas.append((x - 0.07, y - 0.06, x, y + 0.02, 1 - desce))
            setas.append((x + 0.07, y - 0.06, x, y + 0.02, 1 - desce))
            setas.append((x, y - 0.2, x, y + 0.01, 1 - desce))
        G += T.lines(setas, 0.022) * 1.2
    return G * env, H * env


def neutralizacao_silenciosa(T, t, rng):
    """O tiro com silenciador: a baforada pequena e abafada no cano, o traço fino da bala atravessando, o
    impacto preciso (o anel justo e as rachaduras curtas), e a barra do Preparo do rival quebra ao meio
    e as metades caem."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    cano = (-0.88, -0.05)
    sopro = rel(t, 0.02, 0.4)
    if 0 < sopro < 1:
        sub = np.random.default_rng(31)
        pts = [(cano[0] + 0.05 + 0.18 * sopro * sub.uniform(0.3, 1), cano[1] - 0.12 * sopro * sub.uniform(-0.5, 1),
                (1 - sopro) * 0.6) for _ in range(7)]
        G += T.splats(pts, 0.045 + 0.04 * sopro) * 1.2
        G += T.ring(0.04 + 0.12 * sopro, 0.014, cano[0] + 0.08, cano[1]) * (1 - sopro) * 0.8
    H += T.gauss(cano[0] + 0.04, cano[1], 0.02) * pulso(t, 0.0, 0.12) * 1.4
    voo = rel(t, 0.06, 0.2)
    if 0 < voo and t < 0.36:
        x = cano[0] + 0.88 * voo
        some = 1 - rel(t, 0.2, 0.36)
        G += T.tapered([(cano[0], cano[1], x, -0.05, 1.0)], 0.02) * 1.4 * some
        H += T.gauss(x, -0.05, 0.02) * 1.4 * (voo < 1)
    acerta = rel(t, 0.2, 0.55)
    if 0 < acerta < 1:
        H += T.flare(0, -0.05, 0.45 * (1 - acerta) + 0.02, 0, 0.012) * (1 - acerta) * 1.5
        H += T.gauss(0, -0.05, 0.05) * (1 - acerta) ** 2 * 1.5
        G += T.ring(0.05 + 0.28 * ease_out(acerta, 3), 0.018, 0, -0.05) * (1 - acerta) * 1.4
        G += T.ring(0.03 + 0.14 * ease_out(acerta, 2), 0.012, 0, -0.05) * (1 - acerta) * 1.0
        q = np.random.default_rng(12)
        for k in range(5):
            a = TAU * k / 5 + 0.3
            G += T.polyline(jagged(q, 0.03 * math.cos(a), -0.05 + 0.03 * math.sin(a),
                                   0.32 * math.cos(a), -0.05 + 0.32 * math.sin(a), 3, 0.25), 0.011) * (1 - acerta) * 1.1
    # a barra do Preparo do rival: enche, a bala quebra e as metades caem
    enche = rel(t, 0.0, 0.2)
    quebra = rel(t, 0.25, 0.85)
    larg = 0.5
    y = -0.55
    if t < 0.85:
        h = 0.07
        moldura = T.lines([(-larg, y - h, larg, y - h, 1.0), (-larg, y + h, larg, y + h, 1.0),
                           (-larg, y - h, -larg, y + h, 1.0), (larg, y - h, larg, y + h, 1.0)], 0.016)
        cheio = T.lines([(-larg + 0.04, y, -larg + 0.04 + (2 * larg - 0.08) * 0.85 * enche, y, 1.0)], 0.07)
        B = moldura + cheio * 0.7
        if quebra > 0:
            cai = ease_in(quebra, 2)
            racha = 0.03 * np.sign(np.sin(T.V * 60))
            esq = _desloca(T, B * (T.U < racha), -0.15 * cai, 0.6 * cai)
            dir_ = _desloca(T, B * (T.U >= racha), 0.15 * cai, 0.7 * cai)
            B = (esq + dir_) * (1 - quebra)
        G += B * 1.2
    H += T.flare(0, y, 0.35 * pulso(t, 0.22, 0.42) + 0.01, 0.4, 0.012) * pulso(t, 0.22, 0.42) * 1.4
    return G * env, H * env


def plano_de_fuga(T, t, rng):
    """A bomba de fumaça: a bolinha cai em arco com o pavio faiscando, estoura numa nuvem grande que sobe e
    se espalha, e de dentro dela as setas tracejadas da rota de fuga saem correndo, com os riscos de
    velocidade (Acelerado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cai = rel(t, 0.0, 0.2)
    if t < 0.2:
        bx, by = -0.7 + 0.7 * cai, 0.3 - 0.9 * cai * (1 - cai) * 1.6
        G += T.gauss(bx, by, 0.05) * 1.2 + T.ring(0.06, 0.012, bx, by) * 1.0
        H += T.gauss(bx + 0.04, by - 0.06, 0.015) * (0.8 + 0.6 * math.sin(t * 90))
    estoura = rel(t, 0.2, 0.95)
    if estoura > 0:
        H += T.gauss(0, 0.3, 0.12) * pulso(t, 0.19, 0.3) * 1.6
        sub = np.random.default_rng(55)
        fum = []
        for _ in range(26):
            a = sub.uniform(math.pi, TAU) if sub.uniform() < 0.75 else sub.uniform(0, math.pi)
            d = sub.uniform(0.15, 0.7) * ease_out(estoura, 2.5)
            fum.append((d * math.cos(a) * 1.2, 0.3 + d * math.sin(a) * 0.8 - 0.15 * estoura, sub.uniform(0.5, 1) * (1 - estoura) ** 0.8))
        F = T.splats(fum, 0.07 + 0.08 * estoura)
        G += T.blur(F, 0.02) * 0.9 + _borda(T, F, 0.03) * 0.5
    corre = rel(t, 0.32, 0.9)
    if 0 < corre < 1:
        segs = []
        for k, (ang, comp) in enumerate(((-0.55, 0.95), (-0.05, 1.0), (0.35, 0.85))):
            prog = ease_out(rel(corre, 0.08 * k, 0.6 + 0.08 * k), 2)
            if prog <= 0:
                continue
            ux, uy = math.cos(ang), math.sin(ang)
            x0, y0 = 0.0, 0.2
            fim = comp * prog
            d = (t * 1.5) % 0.12
            while d < fim - 0.04:
                segs.append((x0 + ux * d, y0 + uy * d, x0 + ux * min(d + 0.06, fim), y0 + uy * min(d + 0.06, fim), 1.0))
                d += 0.12
            px, py = x0 + ux * fim, y0 + uy * fim
            for lado in (-1, 1):
                a2 = ang + math.pi + lado * 0.5
                segs.append((px, py, px + 0.1 * math.cos(a2), py + 0.1 * math.sin(a2), 1.0))
        G += T.lines(segs, 0.02) * 1.3 * (1 - rel(t, 0.8, 0.95))
    rapido = pulso(t, 0.5, 0.95)
    if rapido > 0:
        sub = np.random.default_rng(3)
        riscos = []
        for _ in range(8):
            y = sub.uniform(-0.6, 0.6)
            x = sub.uniform(-0.9, 0.3) + 1.2 * rel(t, 0.5, 0.95)
            riscos.append((x - 0.3, y, x, y, sub.uniform(0.5, 1)))
        G += T.tapered(riscos, 0.012) * rapido * 0.9
    return G * env, H * env


# =================================================================== Yor
def investida_elegante(T, t, rng):
    """O chute alto da Yor, girando: a meia-lua comprida corta por cima com o calcanhar aceso na ponta, as
    pétalas de rosa voam no rastro, o estalo no impacto e as faíscas curtas do Paralisado."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    gira = ease_out(rel(t, 0.0, 0.32), 2.2)
    a0, a1 = -2.9, -2.9 + 3.6 * gira
    if gira > 0 and t < 0.6:
        some = 1 - rel(t, 0.32, 0.6)
        A = T.arc_band(0.62, 0.09, a0 + 1.4 * rel(t, 0.25, 0.55), a1, squash=0.7, rot=-0.25, cx=-0.05, cy=0.0, crescente=True)
        G += (A * 1.3 + T.blur(A, 0.02) * 0.5) * some
        H += _borda(T, A, 0.006) * 0.6 * some
        cu = 0.62 * math.cos(a1)
        cv = 0.62 * 0.7 * math.sin(a1)
        hx = -0.05 + cu * math.cos(-0.25) - cv * math.sin(-0.25)
        hy = cu * math.sin(-0.25) + cv * math.cos(-0.25)
        H += T.gauss(hx, hy, 0.04) * 1.4 * some
        sub = np.random.default_rng(int(t * 40) % 7 + 70)
        rastro = []
        for k in range(6):
            aa = a0 + (a1 - a0) * sub.uniform(0.2, 0.95)
            cu2, cv2 = 0.66 * math.cos(aa), 0.66 * 0.7 * math.sin(aa)
            x = -0.05 + cu2 * math.cos(-0.25) - cv2 * math.sin(-0.25)
            y = cu2 * math.sin(-0.25) + cv2 * math.cos(-0.25)
            rastro.append((_petala(x, y + 0.04, 0.035, sub.uniform(0, TAU)), 0.8 * some))
        G += T.polys(rastro) * 1.0
    bate = rel(t, 0.3, 0.6)
    if 0 < bate < 1:
        H += T.flare(0.45, 0.05, 0.5 * (1 - bate) + 0.02, 0.3, 0.012) * (1 - bate) * 1.4
        G += T.ring(0.06 + 0.3 * ease_out(bate, 3), 0.02, 0.45, 0.05) * (1 - bate) * 1.3
    G += _petalas_voando(T, t, 21, 18, 0.3, 0.4, 0.05, 0.75, -2.8, 0.4, 0.065, 0.62) * 1.5
    para = pulso(t, 0.45, 0.95)
    if para > 0:
        q = np.random.default_rng(int(t * 30) % 5 + 11)
        for k in range(4):
            a = TAU * k / 4 + 0.6
            x0, y0 = 0.45 + 0.18 * math.cos(a), 0.05 + 0.18 * math.sin(a)
            G += T.polyline(jagged(q, x0, y0, x0 + 0.12 * math.cos(a), y0 + 0.12 * math.sin(a), 3, 0.5), 0.01) * para * 1.2
    return G * env, H * env


def _estilete(cx, cy, ang, comp, larg):
    """O estilete da Yor: a lâmina fina e comprida e a argolinha do cabo."""
    ux, uy = math.cos(ang), math.sin(ang)
    return lamina(cx - ux * comp * 0.5, cy - uy * comp * 0.5, cx + ux * comp * 0.5, cy + uy * comp * 0.5, larg)


def espinho_preparo(T, t, rng):
    """O Preparo do Jardim noturno: os ramos com espinhos girando em volta e o brilho correndo pelos dois
    estiletes cruzados no alto (laço)."""
    G, H = vazio(T)
    for k in range(2):
        fase = TAU * t + k * math.pi
        pts, espinhos = [], []
        for j in range(40):
            u = j / 39
            a = fase + u * 3.2
            r = 0.2 + 0.32 * u
            x, y = r * math.cos(a), 0.05 + r * math.sin(a) * 0.75
            pts.append((x, y))
            if j % 6 == 3:
                nx, ny = math.cos(a), math.sin(a) * 0.75
                espinhos.append(([(x - 0.02 * ny, y + 0.02 * nx), (x + 0.02 * ny, y - 0.02 * nx), (x + 0.07 * nx, y + 0.07 * ny)], 1.0))
        G += T.polyline(pts, 0.018) * 1.0 + T.polys(espinhos) * 1.1
        rx, ry = pts[-1]
        G += T.polys([(_petala(rx, ry, 0.04, fase), 1.0)]) * 1.1
    E = T.polys([(_estilete(0, -0.55, 0.7, 0.5, 0.03), 1.0), (_estilete(0, -0.55, -0.7 + math.pi, 0.5, 0.03), 1.0)])
    G += E * 0.9 + T.blur(E, 0.015) * 0.3
    u = (t * 2) % 1
    for ang in (0.7, math.pi - 0.7):
        gx = 0.25 * (2 * u - 1) * math.cos(ang)
        gy = -0.55 + 0.25 * (2 * u - 1) * math.sin(ang)
        H += T.flare(gx, gy, 0.12, 0.3, 0.01) * math.sin(math.pi * u) * 1.2
    return G, H


def jardim_noturno(T, t, rng):
    """O assassinato da Princesa dos Espinhos: os dois estiletes dourados vêm dos lados e cruzam em X no
    rival (os riscos do corte), a rosa escura desabrocha ali (três camadas de pétalas abrindo e girando) e
    as pétalas se espalham."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    vem = ease_in(rel(t, 0.0, 0.2), 2)
    if 0 < vem and t < 0.42:
        some = 1 - rel(t, 0.25, 0.42)
        shapes = []
        for lado, ang in ((-1, 0.75), (1, math.pi - 0.75)):
            ux, uy = math.cos(ang), math.sin(ang)
            d = 1.0 - vem
            cx, cy = -ux * d * 1.1, -uy * d * 1.1
            shapes.append((_estilete(cx, cy, ang, 0.6, 0.035), 1.0))
        E = T.polys(shapes)
        G += (E * 1.3 + T.blur(E, 0.02) * 0.4) * some
        H += _borda(T, E, 0.005) * 0.6 * some
    corte = rel(t, 0.18, 0.5)
    if 0 < corte < 1:
        X = T.polys([(lamina(-0.6, -0.55, 0.6, 0.55, 0.035, prog=min(1, corte * 3), inicio=max(0, corte * 1.4 - 0.4)), 1.0),
                     (lamina(0.6, -0.55, -0.6, 0.55, 0.035, prog=min(1, corte * 3), inicio=max(0, corte * 1.4 - 0.4)), 1.0)])
        G += X * 1.3
        H += X * 0.5 + T.flare(0, 0, 0.5 * (1 - corte), 0.785, 0.012) * (1 - corte)
    abre = rel(t, 0.3, 0.7)
    fecha = 1 - rel(t, 0.68, 0.85)
    if abre > 0 and fecha > 0:
        shapes = []
        for camada, (n, tam, atraso) in enumerate(((5, 0.18, 0.0), (6, 0.32, 0.15), (7, 0.48, 0.3))):
            f = back(rel(abre, atraso, atraso + 0.6), 1.4)
            if f <= 0:
                continue
            giro = 0.5 * camada + 0.8 * abre
            for k in range(n):
                a = giro + TAU * k / n
                r = tam * f
                shapes.append((lamina(0.0, 0.0, r * math.cos(a), r * math.sin(a) * 0.85, r * 0.42), 1.0))
        R = T.polys(shapes)
        G += (_borda(T, R, 0.012) * 1.6 + R * 0.25) * fecha
        H += T.gauss(0, 0, 0.05) * abre * fecha * 1.2
    G += _petalas_voando(T, t, 44, 22, 0.68, 0.0, 0.0, 0.85, 0, TAU, 0.05, 0.32) * 1.2
    return G * env, H * env


# =================================================================== Jinwoo
def comando_avancem(T, t, rng):
    """O comando do Monarca das Sombras: a poça de sombra se abre no chão, os pares de olhos dos soldados
    acendem em fileiras (os do fundo menores), e ao comando todos avançam juntos em riscos escuros até o
    rival, que leva o impacto e fica Marcado; um fiapo de vida volta para o Jinwoo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    poca = ease_out(rel(t, 0.0, 0.25), 2) * (1 - rel(t, 0.6, 0.9))
    G += T.ring(0.75 * poca, 0.03, 0, 0.55, squash=3.2) * 1.0 + T.gauss(0, 0.55, 0.6 * poca + 0.01, 0.06) * 0.5 * poca
    sub = np.random.default_rng(66)
    soldados = []
    for fila, (y, n, s) in enumerate(((0.45, 6, 1.0), (0.25, 7, 0.75), (0.08, 8, 0.55))):
        for k in range(n):
            x = (-0.75 + 1.5 * (k + 0.5) / n) * (1 - 0.15 * fila) + sub.uniform(-0.03, 0.03)
            soldados.append((x, y + sub.uniform(-0.02, 0.02), s, 0.05 + 0.04 * fila + sub.uniform(0, 0.12)))
    avanca = ease_in(rel(t, 0.42, 0.62), 2)
    alvo = (0.0, -0.2)
    olhos = []
    riscos = []
    corpos = T.zero()
    for x, y, s, t0 in soldados:
        acende = rel(t, t0, t0 + 0.08)
        if acende <= 0:
            continue
        pisca = 1.0 if t > t0 + 0.12 else (0.4 + 0.6 * (math.sin(t * 120 + x * 10) > 0))
        emerge = ease_out(rel(t, t0 - 0.05, t0 + 0.15), 2)
        y = y - 0.12 * s * emerge
        px, py = x + (alvo[0] - x) * avanca, y + (alvo[1] - y) * avanca
        if avanca < 1:
            for lado in (-1, 1):
                olhos.append((px + lado * 0.026 * s - 0.006, py, acende * pisca * (1 - avanca * 0.3)))
                olhos.append((px + lado * 0.026 * s + 0.006, py, acende * pisca * (1 - avanca * 0.3)))
            if avanca == 0:
                corpos += (T.gauss(px, py + 0.01, 0.05 * s, 0.045 * s) + T.gauss(px, py + 0.14 * s, 0.09 * s, 0.1 * s)) * emerge
        if 0 < avanca < 1:
            riscos.append((x + (alvo[0] - x) * max(0, avanca - 0.35), y + (alvo[1] - y) * max(0, avanca - 0.35), px, py, 1.0))
    G += _borda(T, np.clip(corpos, 0, 1), 0.015) * 0.9 + np.clip(corpos, 0, 1) * 0.15
    if olhos:
        O = T.splats(olhos, 0.012)
        G += O * 1.7 + T.blur(O, 0.02) * 0.9
        H += O * 0.9
    if riscos:
        G += T.tapered(riscos, 0.04) * 1.2 + T.blur(T.tapered(riscos, 0.04), 0.02) * 0.5
    bate = rel(t, 0.6, 0.95)
    if 0 < bate < 1:
        H += T.gauss(alvo[0], alvo[1], 0.1) * (1 - bate) ** 2 * 1.8
        G += T.ring(0.08 + 0.5 * ease_out(bate, 3), 0.035, alvo[0], alvo[1]) * (1 - bate) * 1.3
        q = np.random.default_rng(9)
        lascas = []
        for _ in range(12):
            a = q.uniform(0, TAU)
            d = 0.15 + 0.45 * ease_out(bate, 2)
            lascas.append((alvo[0] + d * 0.6 * math.cos(a), alvo[1] + d * 0.6 * math.sin(a),
                           alvo[0] + d * math.cos(a), alvo[1] + d * math.sin(a), 1 - bate))
        G += T.tapered(lascas, 0.016) * 1.1
    volta = rel(t, 0.7, 1.0)
    if 0 < volta < 1:
        pts = [(-0.2 - 0.6 * volta + 0.04 * math.sin(k + t * 20), -0.2 + 0.4 * volta + 0.04 * k, (1 - volta) * (1 - k / 6)) for k in range(6)]
        G += T.splats(pts, 0.025) * 1.0
    return G * env, H * env


# =================================================================== Kaneki
def _kakugan(T, cx, cy, larg, abre):
    pts = [(cx + larg * math.cos(a), cy + larg * 0.42 * abre * math.sin(a) * (1.25 if math.sin(a) > 0 else 0.9))
           for a in np.linspace(0, TAU, 44, endpoint=False)]
    O = T.polys([(pts, 1.0)])
    iris = T.ring(larg * 0.24 * min(1, abre * 1.6), larg * 0.05, cx, cy) + T.gauss(cx, cy, larg * 0.16) * 0.7
    pupila = T.gauss(cx, cy, larg * 0.05)
    return O, iris * O, pupila * O


def fome_de_ghoul(T, t, rng):
    """A fome do ghoul: o kakugan abre (o olho, a íris vermelha acesa e a pupila fina), as veias saltam
    pulsando a partir dele, e a vida é puxada de fora para dentro em espiral, com dois batimentos fortes
    (Regeneração)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = back(rel(t, 0.0, 0.25), 1.3)
    O, iris, pupila = _kakugan(T, 0.0, -0.25, 0.56, max(0.03, abre))
    borda = _borda(T, O, 0.012)
    G += borda * 1.3 + iris * 1.5 + O * 0.08
    H += iris * 0.8 * pulso(t, 0.1, 0.95) + pupila * 0.4
    veias = pulso(t, 0.15, 0.9)
    if veias > 0:
        q = np.random.default_rng(17)
        bate = 0.6 + 0.4 * max(math.sin(TAU * rel(t, 0.25, 0.85) * 2), 0)
        for ang in (2.6, 2.9, 3.3, 3.6, 0.5, 0.2, -0.2, -0.5, 1.9, 1.3):
            r0 = 0.56
            x0, y0 = r0 * math.cos(ang) * 0.95, -0.25 + 0.26 * math.sin(ang)
            cresce = ease_out(rel(t, 0.15, 0.4), 2)
            x1, y1 = x0 + 0.35 * cresce * math.cos(ang), y0 + 0.3 * cresce * math.sin(ang)
            G += T.polyline(jagged(q, x0, y0, x1, y1, 4, 0.35), 0.016) * veias * bate * 1.3
    puxa = rel(t, 0.25, 0.85)
    if 0 < puxa < 1:
        sub = np.random.default_rng(23)
        pts = []
        for k in range(30):
            fase = sub.uniform(0, 1)
            u = (puxa * 1.6 + fase) % 1
            a = sub.uniform(0, TAU) + 2.2 * u
            r = 0.95 * (1 - u) + 0.08
            pts.append((r * math.cos(a), 0.05 + r * math.sin(a) * 0.8, math.sin(math.pi * u) * 0.9))
        G += T.splats(pts, 0.02) * 1.3
    for tb in (0.45, 0.7):
        b = rel(t, tb, tb + 0.2)
        if 0 < b < 1:
            G += T.ring(0.2 + 0.5 * ease_out(b, 2), 0.04, 0, 0.05) * (1 - b) * 1.1
            H += T.gauss(0, 0.05, 0.18) * (1 - b) ** 2 * 0.8
    return G * env, H * env


def _tentaculo(T, bx, by, ang, comp, fase, larg, amp=0.12, n=20, segmentos=False, patas=True):
    """O tentáculo: um corpo que afina, ondulando; com `segmentos`, cada gomo ganha um anel e as patas."""
    cima, baixo, nos = [], [], []
    for j in range(n + 1):
        u = j / n
        onda = amp * math.sin(fase + u * 4.5) * u
        x = bx + math.cos(ang) * comp * u - math.sin(ang) * onda
        y = by + math.sin(ang) * comp * u + math.cos(ang) * onda
        nos.append((x, y))
    for j, (x, y) in enumerate(nos):
        u = j / n
        x2, y2 = nos[min(j + 1, n)] if j < n else nos[j]
        x1, y1 = nos[max(j - 1, 0)]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        w = larg * (1 - u) ** 0.7 + 0.004
        cima.append((x + nx * w, y + ny * w))
        baixo.append((x - nx * w, y - ny * w))
    corpo = T.polys([(cima + baixo[::-1], 1.0)])
    extra = T.zero()
    if segmentos:
        segs = []
        for j in range(1, n, 2):
            u = j / n
            x, y = nos[j]
            x2, y2 = nos[j + 1]
            d = math.hypot(x2 - x, y2 - y) or 1
            nx, ny = -(y2 - y) / d, (x2 - x) / d
            w = larg * (1 - u) ** 0.7
            segs.append((x - nx * w, y - ny * w, x + nx * w, y + ny * w, 1.0))
            for lado in ((-1, 1) if patas else ()):
                segs.append((x + lado * nx * w, y + lado * ny * w, x + lado * nx * (w + 0.06 * (1 - u) + 0.02) + (x2 - x) * 0.6,
                             y + lado * ny * (w + 0.06 * (1 - u) + 0.02) + (y2 - y) * 0.6, 0.9))
        extra = T.lines(segs, 0.01)
    return corpo, extra, nos


def kakuja_preparo(T, t, rng):
    """O Preparo do Centípede: os quatro tentáculos rinkaku saem das costas (de baixo, atrás) e balançam
    devagar, com o brilho do kakugan no meio (laço)."""
    G, H = vazio(T)
    for k, (ang, comp) in enumerate(((-2.4, 0.85), (-2.0, 0.95), (-1.15, 0.95), (-0.75, 0.85))):
        C, E, _ = _tentaculo(T, 0.0, 0.5, ang, comp, TAU * t + k * 1.3, 0.1, amp=0.16, n=18, segmentos=True, patas=False)
        G += _borda(T, C, 0.01) * 1.4 + C * 0.3 + E * C * 0.7
        H += C * 0.15
    H += T.gauss(0.05, 0.0, 0.03) * (0.8 + 0.4 * math.sin(TAU * t * 2)) * 1.2
    return G, H


def centopeia(T, t, rng):
    """O kagune centopeia: o corpo segmentado (os anéis em cada gomo e as patas dos dois lados) serpenteia de
    trás e crava no rival com tudo (o clarão e a cratera), e depois o sangue volta correndo pelo corpo
    (Vampirismo)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    estica = ease_out(rel(t, 0.0, 0.3), 2.4)
    recolhe = ease_in(rel(t, 0.65, 0.95), 2)
    comp = 1.35 * estica * (1 - 0.8 * recolhe)
    nos = []
    if comp > 0.05:
        C, P, nos = _tentaculo(T, -0.98, 0.6, -0.5, comp * 1.05, 6.5 * (1 - estica) + t * 3, 0.15, amp=0.2, n=24, segmentos=True)
        G += _borda(T, C, 0.012) * 1.4 + C * 0.3 + P * 1.2
        H += _borda(T, C, 0.005) * 0.3
    bate = rel(t, 0.28, 0.65)
    if 0 < bate < 1 and nos:
        hx, hy = nos[-1]
        H += T.gauss(hx, hy, 0.12) * (1 - bate) ** 2 * 1.8 + T.flare(hx, hy, 0.6 * (1 - bate) + 0.02, 0.2, 0.014) * (1 - bate)
        G += T.ring(0.1 + 0.5 * ease_out(bate, 3), 0.04, hx, hy) * (1 - bate) * 1.3
        q = np.random.default_rng(41)
        for k in range(7):
            a = TAU * k / 7 + 0.2
            G += T.polyline(jagged(q, hx, hy, hx + 0.45 * ease_out(bate, 2) * math.cos(a), hy + 0.45 * ease_out(bate, 2) * math.sin(a), 4, 0.3), 0.012) * (1 - bate) * 1.1
    volta = rel(t, 0.4, 0.85)
    if 0 < volta < 1 and len(nos) > 3:
        gotas = []
        for k in range(8):
            u = 1 - ((volta * 1.5 + k / 8) % 1)
            i = int(u * (len(nos) - 1))
            x, y = nos[i]
            gotas.append((x, y, math.sin(math.pi * volta)))
        G += T.splats(gotas, 0.025) * 1.5
        H += T.splats(gotas, 0.012) * 0.8
    return G * env, H * env


# =================================================================== Yugi
def _carta(cx, cy, larg, alt, ang):
    pts = [(-larg, -alt), (larg, -alt), (larg, alt), (-larg, alt)]
    dentro = [(-larg * 0.75, -alt * 0.8), (larg * 0.75, -alt * 0.8), (larg * 0.75, alt * 0.1), (-larg * 0.75, alt * 0.1)]
    return _gira(pts, ang, cx, cy), _gira(dentro, ang, cx, cy)


def _contorno_de(pts):
    return [(pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], 1.0) for i in range(len(pts))]


def preparar_o_duelo(T, t, rng):
    """É hora do duelo: o Enigma do Milênio acende no peito (o triângulo invertido com as divisões e o Olho
    de Wdjat), as cinco cartas abrem em leque por cima, a do meio gira e voa no rival, e a Carga sobe em
    faíscas (Fortalecido)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    acende = back(rel(t, 0.0, 0.22), 1.3)
    cx, cy, s = 0.0, 0.25, 0.36 * acende
    if s > 0.01:
        tri = [(cx - s, cy - s * 0.75), (cx + s, cy - s * 0.75), (cx, cy + s * 0.95)]
        linhas = _contorno_de(tri)
        for k in (1, 2):
            f = k / 3
            y = cy - s * 0.75 + (s * 1.7) * f
            meia = s * (1 - f)
            linhas.append((cx - meia, y, cx + meia, y, 0.6))
        G += T.lines(linhas, 0.018) * 1.2
        olho = [(cx + 0.11 * s / 0.3 * math.cos(a), cy - 0.32 * s + 0.045 * s / 0.3 * math.sin(a)) for a in np.linspace(0, TAU, 24, endpoint=False)]
        G += T.lines(_contorno_de(olho), 0.01) * 1.2
        G += T.lines([(cx, cy - 0.32 * s + 0.045 * s / 0.3, cx - 0.02, cy - 0.1 * s, 0.9),
                      (cx + 0.06 * s / 0.3, cy - 0.3 * s, cx + 0.12 * s / 0.3, cy - 0.12 * s, 0.9)], 0.009) * 1.1
        brilho = pulso(t, 0.05, 0.6)
        H += T.gauss(cx, cy - 0.32 * s, 0.025) * 1.6 * brilho + T.flare(cx, cy - 0.32 * s, 0.35 * brilho + 0.01, 0, 0.01) * brilho
        G += T.blur(T.polys([(tri, 1.0)]), 0.03) * 0.4 * brilho
    abre = ease_out(rel(t, 0.15, 0.42), 2.5)
    voa = ease_in(rel(t, 0.5, 0.72), 2)
    if abre > 0 and t < 0.92:
        some = 1 - rel(t, 0.72, 0.92)
        linhas = []
        for k in range(5):
            a = (k - 2) * 0.32 * abre
            px, py = 0.0 + 0.6 * math.sin(a), -0.2 - 0.6 * math.cos(a) * 0.6
            ang = a
            if k == 2 and voa > 0:
                px, py = px + 1.1 * voa, py + 0.2 * voa
                ang = a + 10 * voa
            fora, dentro = _carta(px, py, 0.13, 0.19, ang)
            w = 1.0 if k != 2 else 1.3
            linhas += [(a1, b1, a2, b2, w) for a1, b1, a2, b2, _ in _contorno_de(fora)]
            linhas += [(a1, b1, a2, b2, 0.5 * w) for a1, b1, a2, b2, _ in _contorno_de(dentro)]
            if k == 2 and 0 < voa < 1:
                H += T.gauss(px, py, 0.08) * 1.2 + T.polys([(fora, 1.0)]) * 0.5
                G += T.tapered([(px - 0.4 * voa, py - 0.08 * voa, px, py, 1.0)], 0.04) * 0.6
        G += T.lines(linhas, 0.014) * 1.2 * some
    bate = rel(t, 0.7, 0.95)
    if 0 < bate < 1:
        H += T.flare(0.95, 0.05, 0.3 * (1 - bate) + 0.01, 0.4, 0.012) * (1 - bate) * 1.2
    sobe = rel(t, 0.45, 1.0)
    if 0 < sobe < 1:
        sub = np.random.default_rng(81)
        pts = []
        for _ in range(16):
            f = (sobe + sub.uniform(0, 1)) % 1
            pts.append((sub.uniform(-0.5, 0.5), 0.6 - 0.9 * f, math.sin(math.pi * f) * (1 - sobe * 0.5)))
        G += T.splats(pts, 0.014) * 1.3
        H += T.splats(pts, 0.006) * 0.8
    return G * env, H * env


REGISTRO = [
    ("identidade_falsa", identidade_falsa, GRANDE, "Loid · a máscara rasga e a mira do espião fecha", False),
    ("neutralizacao_silenciosa", neutralizacao_silenciosa, GRANDE, "Loid · o tiro com silenciador e o Preparo quebrado", False),
    ("plano_de_fuga", plano_de_fuga, GRANDE, "Loid · a bomba de fumaça e as setas da fuga", False),
    ("investida_elegante", investida_elegante, GRANDE, "Yor · o chute alto girando e as pétalas", False),
    ("espinho_preparo", espinho_preparo, MEDIA, "Yor · os ramos de espinho e os estiletes (Preparo, laço)", True),
    ("jardim_noturno", jardim_noturno, GRANDE, "Yor · os estiletes em X e a rosa escura", False),
    ("comando_avancem", comando_avancem, GRANDE, "Jinwoo · os olhos das sombras e o avanço", False),
    ("fome_de_ghoul", fome_de_ghoul, GRANDE, "Kaneki · o kakugan, as veias e a vida puxada", False),
    ("kakuja_preparo", kakuja_preparo, MEDIA, "Kaneki · os quatro tentáculos rinkaku (Preparo, laço)", True),
    ("centopeia", centopeia, GRANDE, "Kaneki · o kagune centopeia crava e suga", False),
    ("preparar_o_duelo", preparar_o_duelo, GRANDE, "Yugi · o Enigma do Milênio e o leque de cartas", False),
]
