"""Ataques básicos com animação própria, lote g.

Sephiroth (Masamune), Kratos (Lâminas do Caos), Link (Espada Mestra), Samus (canhão de braço),
Dante (Rebellion e Ebony), Vergil (corte dimensional), Snake (CQC), Wesker (golpe sobre-humano),
Lara (duas pistolas), Ezio (lâmina oculta), Sonic (Spin Attack), Mega Man (Mega Buster),
Zero (Z-Saber) e Mario (a pisada).
"""
from __future__ import annotations

import math

import numpy as np

from .base import (GRANDE, MEDIA, TAU, apaga, back, contorno, ease_in, ease_out, estrela, faiscas, forma, girado,  # noqa: F401
                   jagged, janela, lamina, poeira, pulso, rastro_de_velocidade, rel, smooth, some, vazio)


# ------------------------------------------------------------------ ajudantes
def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _clarao(T, k, cx=0.0, cy=0.0, r=0.3, tam=0.7, ang=0.3):
    """Clarão de impacto: bola de luz + estrela de quatro pontas."""
    if k <= 0:
        return T.zero(), T.zero()
    g = T.gauss(cx, cy, r, r) * k * 1.5
    h = (T.flare(cx, cy, tam * k + 0.01, ang=ang, thin=0.016) + T.flare(cx, cy, tam * 0.65 * k + 0.01, ang=ang + math.pi / 4, thin=0.012)) * k * 1.6
    return g, h


def _chord(R, ang, off, ext=1.08):
    """Corda de um círculo de raio R: direção `ang`, deslocada `off` do centro (passa um pouco da borda)."""
    c, s = math.cos(ang), math.sin(ang)
    meia = math.sqrt(max(R * R - off * off, 0.0)) * ext
    mx, my = -s * off, c * off
    return mx - c * meia, my - s * meia, mx + c * meia, my + s * meia


def _pena(cx, cy, ang, comp=0.2, larg=0.045):
    c, s = math.cos(ang), math.sin(ang)
    return lamina(cx - c * comp / 2, cy - s * comp / 2, cx + c * comp / 2, cy + s * comp / 2, larg)


def _chama(cx, base, alt, larg, fase, ondula=0.3):
    """Língua de fogo (gota que afina para cima com a ponta balançando)."""
    pts = []
    for lado in (1, -1):
        ks = range(13) if lado == 1 else range(12, -1, -1)
        for k in ks:
            u = k / 12
            y = base - alt * u
            w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9
            pts.append((cx + lado * w + ondula * larg * math.sin(fase + 6 * u) * u, y))
    return pts


# ------------------------------------------------------------------ Sephiroth
def masamune(T, t, rng):
    """Masamune: um risco finíssimo e longuíssimo atravessa o quadro de ponta a ponta num instante,
    um brilho corre pelo fio, o alvo se abre num clarão fino e penas caem devagar."""
    G, H = vazio(T)
    env = apaga(t, 0.72, 1)
    x1, y1, x2, y2 = -1.25, 0.42, 1.25, -0.42
    ang_c = math.atan2(y2 - y1, x2 - x1)
    p = ease_out(rel(t, 0.0, 0.13), 3)
    some_ = rel(t, 0.42, 0.9)
    corpo = T.polys([(lamina(x1, y1, x2, y2, 0.05, p, inicio=some_), 1)], 0.003)
    fio = T.polys([(lamina(x1, y1, x2, y2, 0.014, p, inicio=some_), 1)], 0.0015)
    ar = T.blur(corpo, 0.05) * 1.2
    # o reflexo que corre pela lâmina
    u = ease_out(rel(t, 0.1, 0.45), 1.6)
    gx, gy = x1 + (x2 - x1) * (0.15 + 0.75 * u), y1 + (y2 - y1) * (0.15 + 0.75 * u)
    reflexo = T.flare(gx, gy, 0.55, ang=ang_c, thin=0.02) * pulso(t, 0.1, 0.45) * 1.6
    # o alvo se abre: duas linhas paralelas que se afastam
    k = pulso(t, 0.16, 0.7)
    d = 0.02 + 0.09 * ease_out(rel(t, 0.16, 0.6), 2)
    nx, ny = 0.32, 0.95
    abre = sum(T.polys([(lamina(-0.55 + nx * d * s, 0.18 + ny * d * s, 0.55 + nx * d * s, -0.18 + ny * d * s, 0.02), 1)], 0.002) for s in (1, -1)) * k
    g, h = _clarao(T, pulso(t, 0.12, 0.5), r=0.18, tam=1.0, ang=ang_c)
    # penas que caem balançando
    penas = T.zero()
    for j, (px, py0, a0) in enumerate(((-0.35, -0.55, 0.4), (0.3, -0.75, -0.6), (0.05, -0.35, 1.2))):
        uu = rel(t, 0.25 + 0.06 * j, 1.0)
        if uu <= 0:
            continue
        px_ = px + 0.12 * math.sin(uu * 5 + j)
        py_ = py0 + 0.75 * uu
        ang = a0 + 0.6 * math.sin(uu * 5 + j)
        pena = T.polys([(_pena(px_, py_, ang, 0.22, 0.05), 1)], 0.003)
        espinha = T.polyline([(px_ - math.cos(ang) * 0.13, py_ - math.sin(ang) * 0.13), (px_ + math.cos(ang) * 0.11, py_ + math.sin(ang) * 0.11)], 0.007)
        penas += (pena * 0.9 + espinha * 0.6) * janela(uu, 0, 0.15) * (1 - uu) ** 0.8
    G += (T.glow(corpo, 1.2, 1.0, 0.02) + ar * 0.5 + fio * 1.5 + reflexo + abre * 1.4 + g * 0.8 + penas) * env
    H += (fio * 2.2 + corpo * 0.4 + reflexo * 1.2 + abre * 1.2 + h + penas * 0.25) * env
    return G, H


# ------------------------------------------------------------------ Kratos
def laminas_do_caos(T, t, rng):
    """Lâminas do Caos: duas lâminas presas a correntes chegam girando em arcos largos (uma por
    cima, outra por baixo), arrastando fogo, e cortam o alvo em X com brasas."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    ax, ay, R = -0.92, 0.05, 0.92
    total_g, total_h = T.zero(), T.zero()
    sub = np.random.default_rng(717)
    for a0, a1, t0, t1 in ((-1.7, 0.12, 0.0, 0.28), (1.7, -0.12, 0.2, 0.48)):
        p = rel(t, t0, t1)
        if p <= 0:
            continue
        vai = 1 - rel(t, t1 + 0.04, t1 + 0.22)
        a = a0 + (a1 - a0) * ease_in(p, 1.25)
        cos_, sin_ = math.cos(a), math.sin(a)
        lado = 1 if a1 > a0 else -1
        tx, ty = -sin_ * lado, cos_ * lado          # para onde a lâmina vai (frente do giro)
        # corrente: elos do ombro até a lâmina
        elos = [(ax + cos_ * r, ay + sin_ * r, 1.0) for r in np.arange(0.12, R - 0.2, 0.07)]
        corrente = (T.splats(elos, 0.016) * 0.8 + T.polyline([(ax + cos_ * 0.12, ay + sin_ * 0.12), (ax + cos_ * (R - 0.2), ay + sin_ * (R - 0.2))], 0.01) * 0.5) * vai
        # lâmina: lente larga ao longo do raio + o gancho na ponta
        b0 = (ax + cos_ * (R - 0.24), ay + sin_ * (R - 0.24))
        b1 = (ax + cos_ * (R + 0.26), ay + sin_ * (R + 0.26))
        gancho = [(b1[0], b1[1]), (b1[0] - cos_ * 0.17 + tx * 0.15, b1[1] - sin_ * 0.17 + ty * 0.15), (b1[0] - cos_ * 0.15, b1[1] - sin_ * 0.15)]
        lam = T.polys([(lamina(b0[0], b0[1], b1[0], b1[1], 0.1), 1), (gancho, 1)], 0.004) * vai
        # rastro de fogo: meia-lua atrás da lâmina, com línguas de chama subindo dela
        atras = a - (a1 - a0) * 0.55 * min(1.0, p * 2.5)
        trilha = T.arc_band(R + 0.02, 0.2, atras, a + 0.001 * lado, cx=ax, cy=ay, crescente=True) * vai
        chamas = []
        for f in np.linspace(0.15, 1.0, 6):
            af = atras + (a - atras) * f
            rf = R + sub.uniform(-0.1, 0.12)
            cxf, cyf = ax + math.cos(af) * rf, ay + math.sin(af) * rf
            chamas.append((_chama(cxf, cyf + 0.04, 0.12 + 0.16 * f, 0.055 + 0.03 * f, t * 45 + f * 7 + a0), 0.7))
        C = T.polys(chamas, 0.012) * vai
        total_g += corrente + lam * 1.4 + T.glow(trilha, 1.0, 0.8, 0.03) * 1.1 + C * 1.1
        total_h += corrente * 0.4 + lam * 0.9 + trilha * 0.45 + C * 0.35
    # o X de cortes no alvo e o estouro de brasas
    xg = T.zero()
    for (sx, tc) in ((1, 0.28), (-1, 0.48)):
        pc = ease_out(rel(t, tc - 0.03, tc + 0.06), 2)
        if pc > 0:
            xg += T.polys([(lamina(-0.42, -0.42 * sx, 0.42, 0.42 * sx, 0.06, pc, inicio=rel(t, tc + 0.15, tc + 0.45)), 1)], 0.003)
    k = max(pulso(t, 0.26, 0.52), pulso(t, 0.46, 0.78))
    g, h = _clarao(T, k, r=0.24, tam=0.8)
    brasas = faiscas(T, rng, t, 22, 0.7, 0.03, cone=(-math.pi, 0.2), gravidade=-0.15, inicio=0.3)
    G += (total_g + T.glow(xg, 1.2, 1.1, 0.025) + g + T.glow(brasas, 1, 1, 0.02)) * env
    H += (total_h + xg * 1.4 + h + brasas * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Link
def _triforce(lado):
    h = lado * math.sqrt(3) / 2
    topo, esq, dir_ = (0.0, -h * 2 / 3), (-lado / 2, h / 3), (lado / 2, h / 3)
    m_ed = ((topo[0] + esq[0]) / 2, (topo[1] + esq[1]) / 2)
    m_dd = ((topo[0] + dir_[0]) / 2, (topo[1] + dir_[1]) / 2)
    m_b = (0.0, h / 3)
    return [[topo, m_dd, m_ed], [m_ed, m_b, esq], [m_dd, dir_, m_b]]


def espada_mestra(T, t, rng):
    """Espada Mestra: um corte em arco largo por cima do alvo, de lâmina azul-clara; o fio deixa
    um reflexo de três triângulos (o brilho da Triforce) que gira de leve e cintila."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    p = ease_out(rel(t, 0.0, 0.22), 2.2)
    sai = apaga(t, 0.3, 0.6)
    a0, a1 = -2.5, 0.95
    arco = T.arc_band(0.62, 0.17, a0, a0 + (a1 - a0) * p + 0.01, cx=-0.05, cy=0.05, crescente=True) * sai
    fio = T.arc_band(0.66, 0.05, a0, a0 + (a1 - a0) * p + 0.01, cx=-0.05, cy=0.05, crescente=True) * sai
    # a lâmina na cabeça do arco
    ah = a0 + (a1 - a0) * p
    ca, sa = math.cos(ah), math.sin(ah)
    espada = T.polys([(lamina(-0.05 + ca * 0.2, 0.05 + sa * 0.2, -0.05 + ca * 0.85, 0.05 + sa * 0.85, 0.045), 1)], 0.003) * (1 - rel(t, 0.22, 0.3))
    # Triforce: surge com "pop", gira um pouco, uma faixa de reflexo passa por cima
    kt = back(rel(t, 0.22, 0.4), 2.0) * apaga(t, 0.62, 0.95)
    tri = T.zero()
    if kt > 0.01:
        rot = 0.25 * (1 - ease_out(rel(t, 0.22, 0.6), 2))
        formas = [(_gira([(x * kt, y * kt) for x, y in tr], rot, 0.0, -0.02), 1) for tr in _triforce(0.62)]
        tri = T.polys(formas, 0.004)
    passa_ = ease_out(rel(t, 0.38, 0.7), 1.5)
    du, _ = girado(T, -0.6)
    faixa = np.exp(-((du - (-0.5 + 1.0 * passa_)) / 0.07) ** 2) * pulso(t, 0.38, 0.72)
    cintila = sum(T.flare(x, y, 0.35, 0.2, 0.02) * pulso(t, a, a + 0.25) * 1.3
                  for x, y, a in ((0.0, -0.37, 0.36), (-0.32, 0.17, 0.44), (0.32, 0.17, 0.52), (0.5, -0.45, 0.15), (-0.55, -0.4, 0.1)))
    G += (T.glow(arco, 1.1, 0.9, 0.03) + fio * 1.2 + espada * 1.3 + T.glow(tri, 0.8, 0.8, 0.04) + tri * faixa * 1.5 + cintila) * env
    H += (fio * 1.6 + arco * 0.3 + espada * 1.2 + tri * 0.45 + tri * faixa * 2.0 + cintila * 1.1) * env
    return G, H


# ------------------------------------------------------------------ Samus
def canhao_de_braco(T, t, rng):
    """Canhão de braço: uma bola de plasma alongada voa da esquerda com rastro, bate no alvo,
    estoura numa explosão pequena e redonda e solta um anel que se abre."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    vem = ease_in(rel(t, 0.0, 0.27), 1.4)
    bx = -1.05 + 1.05 * vem
    voa = 1 - rel(t, 0.26, 0.3)
    bola = (T.gauss(bx, 0, 0.11, 0.07) * 1.4 + T.gauss(bx - 0.08, 0, 0.2, 0.05) * 0.6) * voa
    nucleo = T.gauss(bx + 0.02, 0, 0.05, 0.03) * voa
    rastro = T.tapered([(bx - 0.65, 0.0, bx, 0.0, 1.0), (bx - 0.45, -0.05, bx - 0.05, -0.02, 0.5), (bx - 0.45, 0.05, bx - 0.05, 0.02, 0.5)], 0.09) * voa * janela(t, 0.02, 0.08)
    # anéis de energia em volta da bola (espiral de plasma)
    espiral = sum(T.ring(0.07, 0.012, cx=bx - 0.12 - 0.13 * j, squash=0.45) * (0.7 - 0.2 * j) for j in range(3)) * voa * janela(t, 0.04, 0.1)
    # explosão
    tt = rel(t, 0.27, 0.75)
    k = pulso(t, 0.26, 0.6)
    bolo = T.gauss(0, 0, 0.12 + 0.18 * ease_out(tt, 2), None) * k * 1.6
    estr = T.polys([(estrela(0, 0, (0.18 + 0.2 * ease_out(tt, 2)) * k + 0.01, 0.3, 8, 0.42), 1)], 0.008) * k
    anel = T.ring(0.08 + 0.72 * ease_out(rel(t, 0.27, 0.8), 2.2), 0.04) * (1 - rel(t, 0.27, 0.85)) * janela(t, 0.27, 0.3) * 1.3
    anel2 = T.ring(0.05 + 0.45 * ease_out(rel(t, 0.32, 0.85), 2.2), 0.025) * (1 - rel(t, 0.32, 0.9)) * janela(t, 0.32, 0.36)
    fa = faiscas(T, rng, t, 18, 0.6, 0.03, inicio=0.27)
    G += (bola + T.blur(rastro, 0.015) * 1.1 + espiral + bolo + estr * 1.1 + anel + anel2 + T.glow(fa, 1, 1, 0.02)) * env
    H += (nucleo * 2.0 + bola * 0.4 + rastro * 0.4 + espiral * 0.4 + bolo * 0.7 + estr * 0.9 + anel * 0.5 + anel2 * 0.4 + fa * 0.6) * env
    return G, H


# ------------------------------------------------------------------ Dante / Lara
_PISTOLA = [(-0.3, -0.05), (0.0, -0.05), (0.0, 0.02), (-0.17, 0.02), (-0.2, 0.15), (-0.27, 0.15), (-0.26, 0.02), (-0.3, 0.02)]


def _pistola(T, t, t0, mx, my, ate=0.9):
    """A pistola de lado, com o cano em (mx, my), dando o coice no tiro."""
    coice = pulso(t, t0, t0 + 0.12)
    vis = janela(t, 0.0, 0.05) * (1 - rel(t, ate - 0.15, ate))
    pts = [(mx + x * 1.3 - 0.06 * coice, my + y * 1.3 - 0.05 * coice * (x + 0.3) / 0.3) for x, y in _PISTOLA]
    return T.polys([(pts, 1)], 0.004) * vis


def _tiro(T, t, t0, mx, my, hx, hy):
    """Um tiro de pistola: clarão na boca do cano, risco do projétil e estalo no alvo."""
    g, h = T.zero(), T.zero()
    kb = pulso(t, t0, t0 + 0.16)
    if kb > 0:
        cone = [(mx - 0.02, my - 0.04), (mx + 0.3 * kb, my - 0.13 * kb), (mx + 0.46 * kb, my), (mx + 0.3 * kb, my + 0.13 * kb), (mx - 0.02, my + 0.04)]
        boca = T.polys([(cone, 1)], 0.01) * kb + T.gauss(mx + 0.05, my, 0.12, 0.12) * kb
        f = T.flare(mx + 0.08, my, 0.7 * kb + 0.01, 0.0, 0.02) * kb
        g += boca * 1.4 + f
        h += boca * 0.8 + f * 1.3
    pr = rel(t, t0 + 0.01, t0 + 0.07)
    if 0 < pr and t < t0 + 0.12:
        risco = T.polys([(lamina(mx + 0.1, my, hx, hy, 0.028, pr, inicio=rel(t, t0 + 0.04, t0 + 0.12)), 1)], 0.002)
        g += risco * 1.5
        h += risco * 1.5
    ki = pulso(t, t0 + 0.05, t0 + 0.4)
    if ki > 0:
        st = T.polys([(estrela(hx, hy, 0.22 * ki + 0.01, 0.4, 6, 0.38), 1)], 0.005) * ki
        an = T.ring(0.05 + 0.3 * ease_out(rel(t, t0 + 0.05, t0 + 0.4), 2), 0.026, cx=hx, cy=hy) * ki
        g += st * 1.2 + an + T.gauss(hx, hy, 0.1, 0.1) * ki
        h += st * 0.9 + an * 0.4
    return g, h


def rebellion_e_ebony(T, t, rng):
    """Rebellion e Ebony: um corte largo e pesado de espadão em diagonal e, logo depois, dois tiros
    de pistola (clarões na boca do cano, riscos e estalos no alvo), um de cada altura."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    p = ease_out(rel(t, 0.0, 0.18), 2.4)
    sai = apaga(t, 0.24, 0.5)
    a0, a1 = -2.35, 0.75
    corte = T.arc_band(0.58, 0.28, a0, a0 + (a1 - a0) * p + 0.01, cx=-0.08, cy=0.0, crescente=True) * sai
    fio = T.arc_band(0.64, 0.08, a0, a0 + (a1 - a0) * p + 0.01, cx=-0.08, cy=0.0, crescente=True) * sai
    g1, h1 = _clarao(T, pulso(t, 0.08, 0.32), r=0.22, tam=0.8)
    ga, ha = _tiro(T, t, 0.36, -0.6, -0.26, 0.04, -0.12)
    gb, hb = _tiro(T, t, 0.56, -0.6, 0.2, -0.02, 0.12)
    arma = _pistola(T, t, 0.36, -0.6, -0.26) * janela(t, 0.26, 0.32) + _pistola(T, t, 0.56, -0.6, 0.2) * janela(t, 0.42, 0.5)
    G += (T.glow(corte, 1.1, 0.9, 0.03) + fio * 1.2 + g1 + ga + gb + arma * 0.9) * env
    H += arma * 0.25 * env
    H += (fio * 1.6 + corte * 0.3 + h1 + ha + hb) * env
    return G, H


# ------------------------------------------------------------------ Vergil
def corte_dimensional(T, t, rng):
    """Corte dimensional (Judgement Cut): o brilho do saque, uma esfera se forma em volta do alvo,
    dezenas de cortes finos riscam o espaço dentro dela e ela se parte em cacos que voam."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    R = 0.56
    saque = T.flare(-0.7, 0.45, 0.6 * pulso(t, 0.0, 0.14) + 0.01, 0.0, 0.012) * pulso(t, 0.0, 0.14) * 1.8
    forma_ = ease_out(rel(t, 0.06, 0.2), 2)
    vive = 1 - rel(t, 0.55, 0.6)
    esfera = T.ring(R * (0.6 + 0.4 * forma_), 0.028) * forma_ * vive * 1.2
    dentro = T.gauss(0, 0, R * 0.6, R * 0.6) * forma_ * vive * 0.35
    sub = np.random.default_rng(4242)
    cortes = T.zero()
    for k in range(14):
        a0 = 0.1 + k * 0.03
        ang = sub.uniform(0, math.pi)
        off = sub.uniform(-0.75, 0.75) * R
        x1, y1, x2, y2 = _chord(R, ang, off, 1.15)
        pc = ease_out(rel(t, a0, a0 + 0.04), 2)
        if pc <= 0:
            continue
        cortes += T.polys([(lamina(x1, y1, x2, y2, 0.02, pc, inicio=rel(t, 0.56, 0.7)), 1)], 0.0015)
    # estilhaços: a casca se parte em arcos e lascas que voam para fora
    tt = rel(t, 0.56, 1.0)
    cacos_g = T.zero()
    if t >= 0.56:
        sub2 = np.random.default_rng(99)
        arcos = T.zero()
        lascas = []
        for k in range(9):
            m = (k + 0.5) / 9 * TAU
            d = 0.45 * ease_out(tt, 2) * sub2.uniform(0.7, 1.2)
            dx, dy = math.cos(m) * d, math.sin(m) * d
            arcos += T.arc_band(R, 0.03, m - 0.3, m + 0.3, cx=dx, cy=dy, taper=0.0)
            for _ in range(2):
                b = m + sub2.uniform(-0.4, 0.4)
                dd = R * 0.7 + 0.5 * ease_out(tt, 2) * sub2.uniform(0.6, 1.3)
                lascas.append((_gira([(-0.05, -0.03), (0.06, 0.0), (-0.02, 0.04)], b + tt * 6, math.cos(b) * dd, math.sin(b) * dd), 1.0))
        cacos_g = (arcos + T.polys(lascas, 0.003)) * (1 - tt) ** 1.2
    k = pulso(t, 0.53, 0.8)
    g, h = _clarao(T, k, r=0.25, tam=1.1, ang=0.0)
    G += (saque + esfera + dentro + T.glow(cortes, 1.4, 0.8, 0.012) + T.glow(cacos_g, 1.1, 0.8, 0.02) + g) * env
    H += (saque * 1.4 + esfera * 0.5 + cortes * 1.6 + cacos_g * 0.8 + h) * env
    return G, H


# ------------------------------------------------------------------ Snake
def _silhueta(T, cx, cy, ang, esc=1.0):
    """Boneco de pessoa (cabeça, tronco, braços e pernas abertos), a cabeça na direção `ang`."""
    c, s = math.cos(ang), math.sin(ang)

    def p(u, v):            # u ao longo do corpo (para a cabeça), v de lado
        return (cx + (c * u - s * v) * esc, cy + (s * u + c * v) * esc)
    cab = p(0.36, 0.0)
    cabeca = T.gauss(cab[0], cab[1], 0.085 * esc, 0.085 * esc)
    linhas = [p(0.27, 0), p(-0.05, 0)]
    corpo = T.polyline(linhas, 0.075 * esc)
    membros = (T.polyline([p(-0.04, 0), p(-0.24, -0.12), p(-0.42, -0.14)], 0.05 * esc) + T.polyline([p(-0.04, 0), p(-0.25, 0.1), p(-0.43, 0.16)], 0.05 * esc)
               + T.polyline([p(0.22, 0), p(0.1, -0.17), p(0.0, -0.25)], 0.04 * esc) + T.polyline([p(0.22, 0), p(0.12, 0.17), p(0.24, 0.27)], 0.04 * esc))
    return np.clip(T.blur(cabeca * 1.8 + corpo + membros, 0.004), 0, 1.0)


def _caminho_cqc(gi):
    ang = -math.pi / 2 + 1.5 * math.pi * gi
    return 0.12 * gi, -0.36 * math.sin(math.pi * gi) + 0.42 * gi, ang


def cqc(T, t, rng):
    """CQC: o "!" de alerta salta, mãos agarram o alvo (marcas de pegada), o corpo é virado no ar
    num giro de 270° com rastro em arco e cai de costas no chão: tremor, poeira e estrelas."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    # "!" de alerta
    ke = back(rel(t, 0.0, 0.12), 2.2) * apaga(t, 0.3, 0.45)
    excl = T.zero()
    if ke > 0.01:
        excl = T.polys([([(-0.06 * ke, -0.92), (0.06 * ke, -0.92), (0.025 * ke, -0.92 + 0.3 * ke), (-0.025 * ke, -0.92 + 0.3 * ke)], 1)], 0.004)
        excl += T.gauss(0, -0.92 + 0.38 * ke, 0.035 * ke + 0.001, 0.035 * ke + 0.001) * 1.8
    # pegada: dois apertos em volta do tronco
    kg = pulso(t, 0.08, 0.3)
    pega = T.zero()
    if kg > 0:
        for cx, cy in ((-0.14, -0.15), (0.12, 0.08)):
            segs = [(cx + math.cos(a) * 0.06, cy + math.sin(a) * 0.06, cx + math.cos(a) * (0.06 + 0.12 * kg), cy + math.sin(a) * (0.06 + 0.12 * kg), 1.0) for a in np.linspace(0, TAU, 7)[:-1]]
            pega += T.lines(segs, 0.022) * kg
    # o giro: o corpo sobe, vira e cai deitado no chão
    gi = ease_in(rel(t, 0.18, 0.5), 1.4)
    cx, cy, ang = _caminho_cqc(gi)
    # o próprio boneco do alvo já está na tela: aqui só o vulto do arremesso (um borrão que gira no arco)
    corpo = T.zero()
    if 0 < gi < 1:
        for j in range(5):
            gj = gi - 0.06 * j
            if gj > 0:
                xj, yj, aj = _caminho_cqc(gj)
                ca, sa = math.cos(aj), math.sin(aj)
                corpo += T.gauss(xj + ca * 0.12, yj + sa * 0.12, 0.13, 0.13) * (0.7 - 0.12 * j)
        corpo = np.clip(corpo, 0, 1)
    giro = T.arc_band(0.5, 0.09, -2.4, -2.4 + 3.6 * gi + 0.01, cy=0.05, taper=1.3) * pulso(t, 0.18, 0.6) * 1.2
    # a queda
    k = pulso(t, 0.48, 0.8)
    chao = 0.55
    tremor = T.gauss(0.1, chao, 0.6 * (0.4 + 0.6 * ease_out(rel(t, 0.48, 0.7), 2)), 0.04) * k * 1.6
    choque = T.ring(0.1 + 0.6 * ease_out(rel(t, 0.48, 0.85), 2), 0.03, cx=0.1, cy=chao, squash=3.5) * k
    po = poeira(T, np.random.default_rng(321), t, 26, 0.1, chao, 0.75, 0.25, 0.045, inicio=0.48) if t > 0.48 else T.zero()
    estrelas = T.zero()
    if t > 0.5:
        for j in range(3):
            a = t * 9 + j * TAU / 3
            estrelas += T.polys([(estrela(0.1 + 0.35 * math.cos(a), chao - 0.32 + 0.08 * math.sin(a), 0.06, a, 5, 0.45), 1)], 0.004)
        estrelas *= pulso(t, 0.5, 1.0)
    G += (excl * 1.4 + pega * 1.3 + corpo * 0.9 + giro + tremor + choque + po * 0.8 + estrelas * 1.3) * env
    H += (excl * 1.2 + pega + T.blur(corpo, 0.01) * 0.25 + giro * 0.4 + tremor * 0.7 + choque * 0.5 + po * 0.2 + estrelas) * env
    return G, H


# ------------------------------------------------------------------ Wesker
def _palma(cx, cy, esc):
    """Mão aberta de frente (palma), dedos para cima."""
    pts = [(-0.13, 0.2), (-0.15, 0.0), (-0.135, -0.13), (-0.105, -0.13), (-0.095, -0.03), (-0.085, -0.25), (-0.045, -0.25), (-0.04, -0.06),
           (-0.025, -0.3), (0.02, -0.3), (0.025, -0.06), (0.04, -0.27), (0.08, -0.27), (0.08, -0.04), (0.095, -0.2), (0.13, -0.19),
           (0.125, 0.0), (0.2, -0.06), (0.23, -0.02), (0.14, 0.12), (0.12, 0.2)]
    return [(cx + x * esc, cy + y * esc) for x, y in pts]


def golpe_sobre_humano(T, t, rng):
    """Golpe sobre-humano: dois olhos vermelhos brilham, o corpo vira um borrão de velocidade com
    vultos que cruzam o quadro, e uma palma aberta acerta o alvo com uma onda de choque."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    # olhos
    olhos, olhos_f = T.zero(), T.zero()
    for ko, ox, oy, esc in ((pulso(t, 0.0, 0.3), -0.58, -0.4, 1.0), (pulso(t, 0.36, 0.85), 0.0, -0.62, 0.85)):
        if ko > 0:
            for ex in (ox - 0.1 * esc, ox + 0.1 * esc):
                olhos += T.polys([(lamina(ex - 0.09 * esc, oy + 0.015, ex + 0.09 * esc, oy - 0.03, 0.035 * esc), 1)], 0.004) * ko
                olhos_f += T.flare(ex, oy, 0.55 * esc * ko + 0.01, 0.0, 0.018) * ko
    # vultos do corpo correndo
    dash = rel(t, 0.12, 0.32)
    vultos, linhas = T.zero(), T.zero()
    if 0 < dash and t < 0.55:
        for j in range(4):
            u = dash - 0.12 * j
            if u <= 0:
                continue
            x = -0.7 + 0.55 * ease_out(u, 1.5)
            a = (0.55 - 0.12 * j) * (1 - rel(t, 0.34, 0.5))
            vultos += (T.gauss(x, -0.38, 0.07, 0.075) + T.gauss(x, -0.08, 0.1, 0.2) + T.gauss(x, 0.28, 0.08, 0.18) * 0.8) * a
        linhas = rastro_de_velocidade(T, rng, 14, 0.0, 0.7, 0.5, 0.05 + 0.2 * (1 - dash), seed=88) * (1 - rel(t, 0.32, 0.45))
    # a palma
    kp = back(rel(t, 0.3, 0.42), 2.0) * apaga(t, 0.55, 0.85)
    palma = T.polys([(_palma(0.0, 0.08, 1.7 * kp + 0.01), 1)], 0.006) if kp > 0.01 else T.zero()
    k = pulso(t, 0.3, 0.62)
    onda = T.ring(0.15 + 0.65 * ease_out(rel(t, 0.3, 0.85), 2.2), 0.05) * (1 - rel(t, 0.3, 0.92)) * janela(t, 0.3, 0.33) * 1.3
    sub = np.random.default_rng(55)
    raios = []
    for _ in range(12):
        a = sub.uniform(0, TAU)
        d0 = 0.35 + 0.35 * ease_out(rel(t, 0.32, 0.65), 2)
        raios.append((math.cos(a) * d0 * 0.6, math.sin(a) * d0 * 0.6, math.cos(a) * d0, math.sin(a) * d0, 1.0))
    R = T.tapered(raios, 0.03) * pulso(t, 0.32, 0.65)
    g, h = _clarao(T, k, r=0.26, tam=0.9)
    G += (olhos * 2.0 + olhos_f + vultos + linhas * 0.9 + palma * 1.1 + T.blur(palma, 0.03) * 0.8 + onda + R + g * 0.8) * env
    H += (olhos * 1.0 + olhos_f * 1.0 + vultos * 0.15 + linhas * 0.4 + palma * 0.7 + onda * 0.5 + R * 0.8 + h) * env
    return G, H


# ------------------------------------------------------------------ Lara
def duas_pistolas(T, t, rng):
    """Duas pistolas: clarão de uma pistola em cima, depois da outra embaixo, cada uma com o risco
    do tiro, o estalo no alvo e um cartucho que pula."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    ga, ha = _tiro(T, t, 0.06, -0.55, -0.3, 0.04, -0.14)
    gb, hb = _tiro(T, t, 0.3, -0.55, 0.24, -0.02, 0.12)
    armas = _pistola(T, t, 0.06, -0.55, -0.3) + _pistola(T, t, 0.3, -0.55, 0.24)
    cart = T.zero()
    for t0, my in ((0.08, -0.3), (0.32, 0.24)):
        u = rel(t, t0, t0 + 0.45)
        if 0 < u < 1:
            x, y = -0.68 - 0.2 * u, my - 0.05 - 0.5 * u + 0.8 * u * u
            cart += T.polys([(_gira([(-0.04, -0.018), (0.04, -0.018), (0.04, 0.018), (-0.04, 0.018)], u * 12, x, y), 1)], 0.003) * (1 - u)
    G += (ga + gb + armas * 0.9 + cart * 1.3) * env
    H += (ha + hb + armas * 0.25 + cart * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Ezio
def lamina_oculta(T, t, rng):
    """Lâmina oculta: o braço com a braçadeira avança, a lâmina salta do pulso num estalo e perfura
    o alvo; a visão de águia pulsa em ondas douradas e contorna o alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    vem = ease_out(rel(t, 0.0, 0.16), 2)
    bx = -1.05 + 0.6 * vem                     # frente da braçadeira
    vis = 1 - rel(t, 0.5, 0.7)
    braco = T.polys([(lamina(-1.3, 0.12, bx - 0.05, 0.03, 0.09), 1)], 0.01) * vis * 0.5
    bracadeira = T.polys([([(bx - 0.22, -0.035), (bx, -0.045), (bx, 0.1), (bx - 0.22, 0.11)], 1)], 0.005) * vis
    sai = ease_out(rel(t, 0.16, 0.21), 3)
    lam = T.zero()
    if sai > 0:
        ponta = bx + 0.02 + (0.12 - bx) * sai
        lam = T.polys([([(bx, -0.01), (ponta - 0.08, -0.018), (ponta, 0.0), (ponta - 0.08, 0.022), (bx, 0.02)], 1)], 0.002) * vis
    estalo = T.flare(bx + 0.02, 0.0, 0.35, 0.0, 0.02) * pulso(t, 0.15, 0.24) * 1.4
    kp = pulso(t, 0.2, 0.45)
    furo = T.polys([(estrela(0.08, 0.0, 0.16 * kp + 0.01, 0.0, 4, 0.25), 1)], 0.004) * kp
    g, h = _clarao(T, kp, cx=0.08, r=0.14, tam=0.6, ang=0.0)
    # visão de águia: ondas que saem do alvo e o contorno dourado dele
    ondas = T.zero()
    for t0 in (0.3, 0.45, 0.6):
        u = rel(t, t0, t0 + 0.4)
        if 0 < u < 1:
            ondas += T.ring(0.1 + 0.8 * ease_out(u, 1.8), 0.035 + 0.04 * u) * (1 - u) ** 1.2
    # o brilho dourado da visão de águia em volta do alvo (sem desenhar uma pessoa por cima do boneco)
    aura = T.blur(T.ring(0.42, 0.03), 0.02) * pulso(t, 0.3, 0.95) * (0.45 + 0.15 * math.sin(t * 30))
    G += (braco + bracadeira * 0.9 + lam * 1.6 + estalo + furo * 1.3 + g * 0.8 + ondas * 0.9 + aura * 1.2) * env
    H += (bracadeira * 0.3 + lam * 2.0 + estalo * 1.2 + furo + h + ondas * 0.35 + aura * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Sonic
def _bola_sonic(T, bx, by, giro, r=0.2, sq=1.0):
    """Bola azul girando: disco, aro e três espinhos curvos que rodam por dentro."""
    disco = T.gauss(bx, by, r * 0.8, r * 0.8 * sq) * 0.75
    aro = T.ring(r, 0.035, cx=bx, cy=by, squash=1 / sq)
    esp = T.zero()
    for k in range(3):
        a = giro + k * TAU / 3
        pts = [(bx + rr * math.cos(a + rr * 8), by + rr * math.sin(a + rr * 8) * sq) for rr in np.linspace(0.03, r * 0.95, 9)]
        esp += T.polyline(pts, 0.022)
    return disco, aro, esp


def _caminho_sonic(t, t_hit):
    if t < t_hit:
        u = ease_in(rel(t, 0.0, t_hit), 1.3)
        return -0.9 + 0.9 * u, -0.6 - 0.35 * math.sin(math.pi * u) + 0.55 * u
    u = ease_out(rel(t, t_hit + 0.06, 0.9), 1.6)
    return -0.7 * u, -0.05 - 0.95 * u + 0.25 * u * u


def spin_attack(T, t, rng):
    """Spin Attack: Sonic pula enrolado como uma bola azul que gira, desce em arco, quica em cima do
    alvo (a bola amassa, estrela de impacto e marcas de mola) e volta para cima e para trás."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    t_hit = 0.32
    bx, by = _caminho_sonic(t, t_hit)
    amassa = pulso(t, t_hit - 0.03, t_hit + 0.12)
    sq = 1 - 0.38 * amassa
    vis = 1 - rel(t, 0.8, 0.95)
    disco, aro, esp = _bola_sonic(T, bx, by, t * 55, 0.25 * (1 + 0.2 * amassa), sq)
    rastro = T.zero()
    for j in range(1, 5):
        xj, yj = _caminho_sonic(max(0.0, t - 0.04 * j), t_hit)
        rastro += T.gauss(xj, yj, 0.17, 0.17) * (0.42 - 0.08 * j)
    rastro *= janela(t, 0.03, 0.08)
    k = pulso(t, t_hit - 0.02, t_hit + 0.3)
    g, h = _clarao(T, k, cx=0.0, cy=0.2, r=0.22, tam=0.8)
    estr = T.polys([(estrela(0.0, 0.2, 0.3 * k + 0.01, 0.2, 6, 0.45), 1)], 0.006) * k
    # marcas de "mola": dois arcos que pulam embaixo do contato
    mola = sum(T.arc_band(0.18 + 0.12 * j + 0.15 * ease_out(rel(t, t_hit, t_hit + 0.3), 2), 0.035, 0.4, math.pi - 0.4, cy=0.05, taper=0.0) for j in range(2)) * pulso(t, t_hit, t_hit + 0.32)
    G += ((disco + aro * 1.2 + esp * 1.2) * vis + rastro + g * 0.7 + estr * 1.1 + mola) * env
    H += ((aro * 0.6 + esp * 1.0 + disco * 0.2) * vis + h + estr * 0.8 + mola * 0.5) * env
    return G, H


# ------------------------------------------------------------------ Mega Man


# ------------------------------------------------------------------ Zero
def z_saber(T, t, rng):
    """Z-Saber: o sabre de energia verde varre uma meia-lua enorme de cima para baixo pela frente,
    com o fio claro, a lâmina reta na cabeça do arco e um rastro que se desfaz em centelhas."""
    G, H = vazio(T)
    env = apaga(t, 0.75, 1)
    cx, cy, R = -0.32, 0.0, 0.5
    p = ease_out(rel(t, 0.0, 0.2), 2.6)
    a0, a1 = -2.2, 2.2
    ah = a0 + (a1 - a0) * p
    sai = apaga(t, 0.3, 0.7)
    lua = T.arc_band(R, 0.3, a0, ah + 0.01, cx=cx, cy=cy, crescente=True) * sai
    fio = T.arc_band(R + 0.08, 0.08, a0, ah + 0.01, cx=cx, cy=cy, crescente=True) * sai
    ca, sa = math.cos(ah), math.sin(ah)
    vis = 1 - rel(t, 0.2, 0.3)
    sabre = T.polys([(lamina(cx + ca * 0.1, cy + sa * 0.1, cx + ca * 0.85, cy + sa * 0.85, 0.05), 1)], 0.003) * vis
    punho = T.gauss(cx + ca * 0.06, cy + sa * 0.06, 0.05, 0.05) * vis
    g, h = _clarao(T, pulso(t, 0.08, 0.4), cx=0.1, r=0.2, tam=0.8, ang=0.0)
    # centelhas de energia saindo do arco
    sub = np.random.default_rng(616)
    cen = []
    for _ in range(18):
        a = sub.uniform(a0, a1)
        q = sub.uniform(0.4, 1)
        u = rel(t, 0.15 + 0.1 * (a - a0) / (a1 - a0), 0.9)
        if 0 < u < 1:
            d = R + 0.05 + 0.3 * ease_out(u, 2) * q
            cen.append((cx + math.cos(a) * d, cy + math.sin(a) * d - 0.1 * u, (1 - u) * 0.8))
    C = T.splats(cen, 0.014) if cen else T.zero()
    G += (T.glow(lua, 1.0, 1.0, 0.035) + fio * 1.3 + sabre * 1.4 + punho + g * 0.8 + C * 1.5) * env
    H += (fio * 1.7 + lua * 0.35 + sabre * 1.6 + h + C * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Mario
_BOTA = [(-0.24, 0.12), (0.27, 0.12), (0.33, 0.06), (0.32, -0.02), (0.25, -0.08), (0.06, -0.1), (0.04, -0.34),
         (-0.2, -0.34), (-0.22, -0.12), (-0.26, -0.02)]


def pisada_do_mario(T, t, rng):
    """Pisada do Mario: a bota desce do alto com linhas de queda, pisa o alvo (o impacto achata,
    faixa larga e baixa), quica de volta para cima; estrelinhas rodam e uma moeda sobe girando."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    t_hit = 0.24
    if t < t_hit:
        by = -0.95 + 0.87 * ease_in(rel(t, 0.0, t_hit), 1.3)
    else:
        u = rel(t, t_hit + 0.04, 0.7)
        by = -0.08 - 1.4 * ease_out(u, 1.8)
    amassa = pulso(t, t_hit - 0.02, t_hit + 0.12)
    vis = 1 - rel(t, 0.55, 0.7)
    sola_y = by + 0.12
    bota_pts = [(x * 1.45 * (1 + 0.15 * amassa), sola_y + (y - 0.12) * 1.45 * (1 - 0.25 * amassa)) for x, y in _BOTA]
    bota = T.polys([(bota_pts, 1)], 0.006) * vis
    borda = T.polyline(bota_pts + [bota_pts[0]], 0.02) * vis
    sola = T.polyline([(-0.35, sola_y), (0.4, sola_y)], 0.04) * vis
    queda = T.zero()
    if t < t_hit + 0.04:
        segs = [(x, by - 0.95, x, by - 0.5, 1.0) for x in (-0.26, -0.09, 0.1, 0.27)]
        queda = T.tapered(segs, 0.03) * janela(t, 0.02, 0.08)
    # o achatamento: faixa larga e baixa + anel achatado
    k = pulso(t, t_hit - 0.02, t_hit + 0.3)
    faixa = T.gauss(0, 0.06, 0.55 * (0.4 + 0.6 * ease_out(rel(t, t_hit, t_hit + 0.15), 2)), 0.05) * k * 1.6
    anel = T.ring(0.12 + 0.6 * ease_out(rel(t, t_hit, t_hit + 0.4), 2), 0.03, cy=0.06, squash=3.2) * k
    est_imp = T.zero()
    if k > 0:
        est_imp = sum(T.polys([(estrela(sx * (0.28 + 0.2 * ease_out(rel(t, t_hit, t_hit + 0.3), 2)), -0.04, 0.08 * k + 0.005, 0.3, 4, 0.35), 1)], 0.004) for sx in (-1, 1)) * k
    # estrelinhas girando
    estrelas = T.zero()
    if t > t_hit + 0.05:
        for j in range(3):
            a = t * 10 + j * TAU / 3
            estrelas += T.polys([(estrela(0.42 * math.cos(a), -0.3 + 0.1 * math.sin(a), 0.1, a * 0.5, 5, 0.45), 1)], 0.004)
        estrelas *= pulso(t, t_hit + 0.05, 1.0)
    # moeda que sobe girando
    um = rel(t, 0.36, 1.0)
    moeda_g, moeda_h = T.zero(), T.zero()
    if um > 0:
        mx, my = 0.5, -0.1 - 0.5 * ease_out(um, 2)
        larg = 0.13 * abs(math.cos(um * 12)) + 0.018
        a = janela(um, 0, 0.1) * (1 - rel(um, 0.75, 1))
        disco = (((T.U - mx) / larg) ** 2 + ((T.V - my) / 0.17) ** 2) < 1
        moeda = T.blur(disco.astype(np.float32), 0.006)
        fenda = T.polyline([(mx, my - 0.09), (mx, my + 0.09)], 0.024) * min(1.0, larg / 0.07)
        moeda_g = (moeda * 1.3 + T.blur(moeda, 0.03) * 0.6 - fenda * 0.9) * a
        moeda_h = (moeda * 0.35 + T.flare(mx + 0.04, my - 0.06, 0.3, 0.0, 0.02) * pulso(um, 0.2, 0.6)) * a
    G += (bota * 0.7 + borda * 1.1 + sola * 1.0 + queda + faixa + anel + est_imp * 1.2 + estrelas * 1.3 + moeda_g) * env
    H += (borda * 0.6 + sola * 0.8 + bota * 0.1 + queda * 0.5 + faixa * 0.8 + anel * 0.5 + est_imp + estrelas + moeda_h) * env
    return G, H


REGISTRO = [
    ("masamune", masamune, GRANDE, "Sephiroth: corte finíssimo e longo atravessando o quadro, penas caindo", False),
    ("laminas_do_caos", laminas_do_caos, GRANDE, "Kratos: duas lâminas em chamas presas a correntes cortam em X", False),
    ("espada_mestra", espada_mestra, GRANDE, "Link: arco de espada azul-claro e o reflexo dos três triângulos", False),
    ("canhao_de_braco", canhao_de_braco, GRANDE, "Samus: bola de plasma do canhão, explosão pequena e anel (+x)", False),
    ("rebellion_e_ebony", rebellion_e_ebony, GRANDE, "Dante: corte largo de espadão e dois tiros de pistola", False),
    ("corte_dimensional", corte_dimensional, GRANDE, "Vergil: esfera de cortes em volta do alvo que se parte", False),
    ("cqc", cqc, GRANDE, "Snake: '!' de alerta, agarrão, giro no ar e queda com poeira", False),
    ("golpe_sobre_humano", golpe_sobre_humano, GRANDE, "Wesker: olhos vermelhos, vultos de velocidade e palma aberta", False),
    ("duas_pistolas", duas_pistolas, GRANDE, "Lara: dois tiros alternados das duas pistolas (+x)", False),
    ("lamina_oculta", lamina_oculta, GRANDE, "Ezio: a lâmina salta do pulso e perfura, ondas da visão de águia", False),
    ("spin_attack", spin_attack, GRANDE, "Sonic: bola azul girando quica no alvo e volta", False),
    ("z_saber", z_saber, GRANDE, "Zero: meia-lua do sabre de energia", False),
    ("pisada_do_mario", pisada_do_mario, GRANDE, "Mario: a bota pisa, achata, estrelinhas e moeda", False),
]
