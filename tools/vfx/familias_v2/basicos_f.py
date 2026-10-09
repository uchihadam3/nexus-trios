"""Ataques básicos com animação própria, lote f.

Rogue (o toque que suga), Professor X (ondas psíquicas na cabeça), Venom (tentáculos
que chicoteiam e agarram), Carnificina (lâminas vivas retorcidas), Loki (a adaga que
se divide em ilusões), Galactus (a mão cósmica que desfaz a matéria), Senhor das
Estrelas (dois blasters alternando), Rocket (o canhão grande), Aquaman (o tridente),
Ciborgue (o canhão sônico), Pantera Negra (garras de vibranium e o pulso cinético),
Darkseid (o punho com o Efeito Ômega) e Hellboy (a Mão Direita da Perdição).
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


def _move(pts, dx, dy, esc=1.0):
    return [(dx + x * esc, dy + y * esc) for x, y in pts]


def _clarao(T, k, cx=0.0, cy=0.0, r=0.3, tam=0.7, ang=0.3):
    g = T.gauss(cx, cy, r, r) * k * 1.5
    h = (T.flare(cx, cy, tam * k + 0.01, ang=ang, thin=0.016) + T.flare(cx, cy, tam * 0.65 * k + 0.01, ang=ang + math.pi / 4, thin=0.012)) * k * 1.6
    return g, h


def _tubo(pts, w0, w1, pot=1.0):
    """Contorno de um tubo que afina de w0 (começo) a w1 (ponta) ao longo dos pontos."""
    n = len(pts)
    esq, dir_ = [], []
    for i, (x, y) in enumerate(pts):
        ax, ay = pts[max(i - 1, 0)]
        bx, by = pts[min(i + 1, n - 1)]
        L = math.hypot(bx - ax, by - ay) or 1
        nx, ny = -(by - ay) / L, (bx - ax) / L
        u = i / max(n - 1, 1)
        w = w0 + (w1 - w0) * u ** pot
        esq.append((x + nx * w, y + ny * w))
        dir_.append((x - nx * w, y - ny * w))
    return esq + dir_[::-1]


def _desloca(pts, d0, d1=None):
    """A mesma linha deslocada para o lado (o reflexo num tubo brilhante)."""
    d1 = d0 if d1 is None else d1
    n = len(pts)
    out = []
    for i, (x, y) in enumerate(pts):
        ax, ay = pts[max(i - 1, 0)]
        bx, by = pts[min(i + 1, n - 1)]
        L = math.hypot(bx - ax, by - ay) or 1
        nx, ny = -(by - ay) / L, (bx - ax) / L
        d = d0 + (d1 - d0) * i / max(n - 1, 1)
        out.append((x + nx * d, y + ny * d))
    return out


def _corta_caminho(pts, frac):
    """Só o começo de uma linha (até `frac` do comprimento)."""
    if frac >= 1:
        return pts
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    tot = sum(seg) * max(frac, 0.0)
    out = [pts[0]]
    acc = 0.0
    for (a, b), s in zip(zip(pts, pts[1:]), seg):
        if acc + s >= tot:
            u = (tot - acc) / (s or 1)
            out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
            break
        out.append(b)
        acc += s
    return out if len(out) > 1 else [pts[0], pts[0]]


def _mao(T, cx, cy, ang, esc, curl=0.0, aberto=1.0, dedo=0.055):
    """Mão aberta apontando para +x (girada por `ang`): palma + quatro dedos de três
    falanges que dobram por `curl` + polegar. Devolve (preenchimento, pontas dos dedos)."""
    palma = [(-0.13, -0.12), (0.06, -0.135), (0.12, -0.1), (0.13, 0.1), (0.07, 0.13), (-0.13, 0.12), (-0.17, 0.0)]
    dedos = []
    pontas = []
    for k, (y0, comp) in enumerate(((-0.095, 0.2), (-0.032, 0.235), (0.032, 0.225), (0.095, 0.18))):
        a = (k - 1.5) * 0.09 * aberto
        x, y = 0.11, y0
        pts = [(x, y)]
        for j, f in enumerate((0.45, 0.33, 0.22)):
            a += curl * (0.6 if j == 0 else 1.0)
            x += math.cos(a) * comp * f
            y += math.sin(a) * comp * f
            pts.append((x, y))
        dedos.append(pts)
        pontas.append((x, y))
    # polegar: sai de cima da palma, para a frente
    a = -0.95 * aberto
    x, y = 0.0, -0.12
    pol = [(x, y)]
    for f in (0.12, 0.1):
        a += curl * 0.8
        x += math.cos(a) * f
        y += math.sin(a) * f
        pol.append((x, y))
    dedos.append(pol)

    def mundo(p):
        return _move(_gira([(px * esc, py * esc) for px, py in p], ang), cx, cy)

    fill = T.polys([(mundo(palma), 1.0)])
    for d in dedos:
        fill = fill + T.polyline(mundo(d), dedo * esc)
        tx, ty = mundo([d[-1]])[0]
        fill = fill + T.gauss(tx, ty, dedo * esc * 0.42, dedo * esc * 0.42) * 1.2
    fill = np.minimum(T.blur(fill, 0.004), 1.0)
    return fill, [mundo([p])[0] for p in pontas]


def _quadradinho(cx, cy, r, ang):
    return [(cx + math.cos(ang + k * math.pi / 2) * r, cy + math.sin(ang + k * math.pi / 2) * r) for k in range(4)]


def _pedra(sub, cx, cy, r, ang):
    n = 6
    return [(cx + math.cos(ang + TAU * k / n) * r * sub.uniform(0.65, 1.1), cy + math.sin(ang + TAU * k / n) * r * sub.uniform(0.65, 1.1)) for k in range(n)]


def _gota(cx, cy, r, ang, cauda=2.4):
    """Gota d'água: bolinha com rabo apontando para trás de `ang` (o sentido do voo)."""
    pts = []
    for k in range(16):
        a = TAU * k / 16
        rr = r * (1 + (cauda - 1) * max(0.0, -math.cos(a)) ** 3)
        pts.append((math.cos(a) * rr, math.sin(a) * r * (1 - 0.35 * max(0.0, -math.cos(a)))))
    return _gira(pts, ang, cx, cy)


def _anel_torto(T, cx, cy, r, w, fase, amp=0.06, lobos=6):
    """Anel que ondula (raio modulado pelo ângulo): onda psíquica/sonora."""
    du, dv = T.U - cx, T.V - cy
    rr = np.hypot(du, dv)
    ang = np.arctan2(dv, du)
    rm = r * (1 + amp * np.sin(lobos * ang + fase))
    return np.exp(-(((rr - rm) / max(w, 1e-4)) ** 2))


def _entorta(T, a, cx, cy, forca, t, freq=28, vel=45):
    """Distorção radial que corre para fora (o ar tremendo)."""
    if forca <= 0:
        return a
    du, dv = T.U - cx, T.V - cy
    rr = np.hypot(du, dv) + 1e-3
    onda = 0.035 * forca * np.sin(rr * freq - t * vel) * np.exp(-rr * 1.2)
    return T.warp(a, onda * du / rr, onda * dv / rr)


# ------------------------------------------------------------------ Rogue
def toque_absorvente(T, t, rng):
    """Toque (Vampira): a mão nua chega e encosta no alvo; do corpo dele saem fios de vida
    ondulando que correm até os dedos, com contas de luz sendo sugadas, e a mão acende."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    chega = ease_out(rel(t, 0.0, 0.2), 2.5)
    hx = -1.15 + 0.6 * chega
    mao, pontas = _mao(T, hx, 0.03, 0.0, 1.45, curl=0.12 + 0.12 * chega, aberto=0.8)
    suga = janela(t, 0.22, 0.32) * (1 - rel(t, 0.8, 0.96))
    carga = janela(t, 0.3, 0.75)
    toque = pulso(t, 0.16, 0.42)
    contato = T.gauss(0.0, 0.03, 0.1) * toque * 1.6 + T.ring(0.05 + 0.32 * ease_out(rel(t, 0.16, 0.42), 2), 0.035, 0, 0.03) * toque
    # o alvo "esvaziando": um miolo que brilha e encolhe
    vida = T.gauss(0.28, 0.0, 0.22 * (1 - 0.5 * carga) + 0.02, 0.3 * (1 - 0.5 * carga) + 0.02) * suga * 0.6
    sub = np.random.default_rng(1101)
    fios = T.zero()
    contas = []
    destino = (hx + 0.3, 0.03)
    for k in range(6):
        a = -1.9 + 3.8 * k / 5 + sub.uniform(-0.1, 0.1)
        r0 = 0.5 + 0.12 * sub.uniform()
        sx, sy = 0.3 + math.cos(a) * r0 * 0.75, math.sin(a) * r0 * 1.05
        fase = sub.uniform(0, TAU)
        pts = []
        for j in range(28):
            u = j / 27
            x = sx + (destino[0] - sx) * u
            y = sy + (destino[1] - sy) * u ** 1.3
            bojo = math.sin(math.pi * u) * 0.1 * math.copysign(1, sy if abs(sy) > 0.05 else 1)
            onda = 0.045 * math.sin(u * 9 + t * 32 + fase) * math.sin(math.pi * u)
            pts.append((x, y - bojo + onda))
        cresce = ease_out(rel(t, 0.22 + 0.025 * k, 0.4 + 0.025 * k), 2)
        if cresce > 0:
            fios += T.polyline(_corta_caminho(pts, cresce), 0.02)
        for c in range(3):
            u = ((t - 0.3) * 2.6 + c / 3 + k * 0.11) % 1.0
            p = pts[min(27, int(u * 27))]
            contas.append((p[0], p[1], suga * (0.6 + 0.4 * math.sin(math.pi * u))))
    C = T.splats(contas, 0.032)
    aura = T.gauss(hx + 0.12, 0.03, 0.3, 0.28) * carga * suga * 0.6
    G += (mao * (0.75 + 0.4 * carga) + T.glow(fios, 0.9, 1.2, 0.025) * suga + C * 1.8 + contato + vida + aura) * env
    H += (contorno(T.blur(mao, 0.01), 0.3, 0.5, 0.6, 0.85) * 0.5 + mao * 0.5 * carga + fios * 0.4 * suga + C * 1.3 + contato * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Professor X
def golpe_psiquico(T, t, rng):
    """Golpe psíquico (Professor X): ondas em arco atravessam o ar até a cabeça do alvo,
    anéis concêntricos se fecham sobre ela, e o golpe estoura num pulso que entorta o ar."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    cx, cy = 0.05, -0.3
    ondas = T.zero()
    for k in range(3):
        a0 = 0.06 * k
        p = rel(t, a0, a0 + 0.24)
        if 0 < p < 1:
            x = -0.95 + (cx + 0.95) * ease_in(p, 1.2)
            R = 0.26 + 0.08 * k + 0.1 * p
            ondas += T.arc_band(R, 0.07, -1.0, 1.0, cx=x - R, cy=cy, crescente=True) * (0.7 + 0.5 * math.sin(math.pi * p))
    fecha = T.zero()
    for k in range(3):
        p = rel(t, 0.18 + 0.06 * k, 0.4 + 0.06 * k)
        if 0 < p < 1:
            r = 0.62 * (1 - ease_in(p, 1.4)) + 0.04
            fecha += _anel_torto(T, cx, cy, r, 0.04, t * 20 + k, 0.05) * math.sin(math.pi * p) ** 0.6
    k2 = pulso(t, 0.44, 0.92)
    abre = ease_out(rel(t, 0.44, 0.9), 2.2)
    pulso_ = (_anel_torto(T, cx, cy, 0.08 + 0.6 * abre, 0.05, t * 26, 0.08) * 1.2 + _anel_torto(T, cx, cy, 0.04 + 0.38 * abre, 0.035, -t * 30, 0.1, 5) * 0.8) * k2
    g, h = _clarao(T, pulso(t, 0.4, 0.66), cx, cy, 0.16, 0.6, 0.0)
    cabeca = T.gauss(cx, cy, 0.09, 0.09) * janela(t, 0.2, 0.42) * (1 - rel(t, 0.5, 0.8)) * 1.4
    g_ = ondas * 1.3 + fecha * 1.3 + pulso_ + g + cabeca
    h_ = ondas * 0.6 + fecha * 0.6 + pulso_ * 0.5 + h + cabeca
    dist = pulso(t, 0.3, 0.95)
    G += _entorta(T, g_, cx, cy, dist, t) * env
    H += _entorta(T, h_, cx, cy, dist, t) * env
    return G, H


# ------------------------------------------------------------------ Venom
def tentaculo_simbionte(T, t, rng):
    """Tentáculo simbionte (Venom): três tentáculos grossos e lisos, com o reflexo branco
    correndo pelo dorso, chicoteiam da esquerda; o do meio estala no alvo e os outros dois
    se enrolam em volta dele e apertam antes de recolher."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, reflexo = T.zero(), T.zero()
    R = 0.34 - 0.06 * janela(t, 0.45, 0.65)
    planos = ((-0.5, -2.35, 2.9, 0.06), (0.05, None, 0.0, 0.0), (0.5, 2.35, -2.9, 0.1))
    estalo = pulso(t, 0.14, 0.38)
    for k, (y0, ac, span, atraso) in enumerate(planos):
        e = ease_out(rel(t, atraso, atraso + 0.2), 2) * (1 - ease_in(rel(t, 0.74, 0.98), 1.6))
        if e <= 0.01:
            continue
        sx, sy = -1.08, y0
        if ac is None:
            ex, ey = 0.02, 0.02
        else:
            ex, ey = math.cos(ac) * R, math.sin(ac) * R
        pts = []
        for j in range(30):
            u = j / 29
            onda = 0.13 * math.sin(math.pi * u) * math.sin(u * 7.5 - t * 22 + k * 2) * (1 - janela(t, 0.3, 0.5) * 0.7)
            pts.append((sx + (ex - sx) * u, sy + (ey - sy) * u + onda))
        if ac is not None:
            enrola = ease_out(rel(t, atraso + 0.16, atraso + 0.42), 2)
            for j in range(1, 22):
                a = ac + span * enrola * j / 21
                pts.append((math.cos(a) * R, math.sin(a) * R * 0.92))
        pts = _corta_caminho(pts, e)
        if len(pts) < 3:
            continue
        w0 = 0.095 if ac is None else 0.085
        corpo += T.polys([(_tubo(pts, w0, 0.025, 0.9), 1.0)], 0.004)
        reflexo += T.polyline(_desloca(pts, -w0 * 0.45, -0.01), 0.016)
    aperto = pulso(t, 0.42, 0.8)
    anel = T.ring(R, 0.06, squash=1 / 0.92) * aperto * 0.6
    g, h = _clarao(T, estalo, 0.02, 0.02, 0.14, 0.55)
    G += (corpo * 0.95 + T.blur(corpo, 0.03) * 0.5 + anel + g) * env
    H += (reflexo * 1.6 + T.blur(reflexo, 0.01) * 0.4 + corpo * 0.08 + h) * env
    return G, H


# ------------------------------------------------------------------ Carnificina
def _lamina_torta(x1, y1, x2, y2, larg, torce, prog=1.0, inicio=0.0, n=30, fase=0.0):
    """Lâmina de simbionte: lente afiada com a espinha ondulada (retorcida)."""
    dx, dy = x2 - x1, y2 - y1
    comp = math.hypot(dx, dy) or 1
    nx, ny = -dy / comp, dx / comp
    a, b = inicio, max(inicio + 1e-3, prog)
    cima, baixo, espinha = [], [], []
    for k in range(n + 1):
        u = a + (b - a) * k / n
        w = larg * math.sin(math.pi * min(1, max(0, u))) ** 0.8 * (1 + 0.35 * math.sin(u * 13 + fase))
        desvio = torce * math.sin(u * TAU * 1.2 + fase) * math.sin(math.pi * u)
        x, y = x1 + dx * u + nx * desvio, y1 + dy * u + ny * desvio
        espinha.append((x, y))
        cima.append((x + nx * w, y + ny * w))
        baixo.append((x - nx * w * 0.6, y - ny * w * 0.6))
    return cima + baixo[::-1], espinha, (nx, ny)


def lamina_viva(T, t, rng):
    """Lâmina viva (Carnificina): lâminas vermelhas de simbionte, tortas e cheias de farpas,
    rasgam o alvo em quatro ângulos seguidos; os talhos ficam abertos e respingam."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    cortes = ((-0.75, 0.0, 0.55), (0.6, 0.1, 0.6), (-1.45, 0.2, 0.5), (0.15, 0.3, 0.62))
    sub = np.random.default_rng(1303)
    lam, nucleo, farpas, gotas = T.zero(), T.zero(), [], []
    for k, (ang, a0, raio) in enumerate(cortes):
        c, s = math.cos(ang), math.sin(ang)
        x1, y1, x2, y2 = -c * raio * 1.45, -s * raio * 1.45, c * raio * 1.45, s * raio * 1.45
        p = ease_out(rel(t, a0, a0 + 0.12), 2)
        fim = ease_in(rel(t, a0 + 0.16, a0 + 0.55), 1.4)
        if p <= 0 or fim >= 1:
            continue
        pts, esp, (nx, ny) = _lamina_torta(x1, y1, x2, y2, 0.085, 0.07, p, fim, fase=k * 1.7)
        lam += T.polys([(pts, 1.0)], 0.004)
        nucleo += T.polyline(esp[2:-2], 0.01)
        # farpas: ganchos saindo do fio de cima
        for j in range(4):
            u = 0.2 + 0.18 * j
            if fim < u < p:
                i = int((u - fim) / max(p - fim, 1e-3) * 30)
                bx, by = esp[min(i, 30)]
                farpas.append(([(bx - c * 0.03 + nx * 0.05, by - s * 0.03 + ny * 0.05), (bx + c * 0.06 + nx * 0.13, by + s * 0.06 + ny * 0.13),
                                (bx + c * 0.04 + nx * 0.04, by + s * 0.04 + ny * 0.04)], 1.0))
        # respingos grossos quando a lâmina sai
        q = rel(t, a0 + 0.1, a0 + 0.45)
        if 0 < q < 1:
            for j in range(4):
                d = sub.uniform(0.15, 0.5) * ease_out(q, 2)
                lado = 1 if j % 2 else -1
                ox, oy = nx * lado * d + c * sub.uniform(-0.2, 0.2), ny * lado * d + s * sub.uniform(-0.2, 0.2) + 0.3 * q * q
                gotas.append((_gota(ox, oy, 0.03, math.atan2(oy, ox)), (1 - q) * 0.9))
    F = T.polys(farpas, 0.004) if farpas else T.zero()
    D = T.polys(gotas, 0.004) if gotas else T.zero()
    k = pulso(t, 0.0, 0.45)
    G += (lam * 1.1 + T.blur(lam, 0.03) * 0.6 + F * 1.1 + D * 1.2 + T.gauss(0, 0, 0.25) * k * 0.4) * env
    H += (nucleo * 1.3 + lam * 0.18 + F * 0.3 + D * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Loki
def _adaga(cx, cy, ang, esc=1.0):
    """Adaga de Loki apontando para +x: lâmina longa, guarda com chifres para trás e cabo."""
    lam = lamina(-0.02, 0.0, 0.34, 0.0, 0.05)
    guarda = [(0.0, -0.03), (-0.05, -0.1), (-0.1, -0.13), (-0.04, -0.03), (-0.04, 0.03), (-0.1, 0.13), (-0.05, 0.1), (0.0, 0.03)]
    cabo = [(-0.04, -0.022), (-0.17, -0.022), (-0.17, 0.022), (-0.04, 0.022)]
    pomo = estrela(-0.19, 0.0, 0.035, 0.0, 4, 0.55)
    return [(_move(_gira([(x * esc, y * esc) for x, y in q], ang), cx, cy), 1.0) for q in (lam, guarda, cabo, pomo)]


def adaga_ilusoria(T, t, rng):
    """Adaga ilusória (Loki): uma adaga voa e se parte em cinco cópias que se abrem em leque;
    as falsas tremulam, viram fumaça e somem antes de chegar — só a verdadeira (que faz a
    curva por cima) crava no alvo, com o brilho de um corte."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    falso, real = T.zero(), T.zero()
    sub = np.random.default_rng(1505)
    p0 = ease_out(rel(t, 0.0, 0.16), 1.5)
    if t < 0.17:
        real += T.polys(_adaga(-1.0 + 0.4 * p0, 0.0, 0.0, 1.25), 0.003)
    racha = pulso(t, 0.13, 0.27)
    split = T.gauss(-0.6, 0.0, 0.12) * racha * 1.4 + T.ring(0.05 + 0.25 * ease_out(rel(t, 0.13, 0.3), 2), 0.03, -0.6, 0.0) * racha
    fumaca = []
    p = rel(t, 0.16, 0.42)
    for k, ay in enumerate((-0.7, -0.35, 0.0, 0.35, 0.7)):
        if p <= 0:
            break
        if k == 1:
            # a verdadeira: curva por cima e desce até o alvo
            x = -0.6 + 0.4 * ease_in(p, 1.3)
            y = -0.34 * math.sin(math.pi * p)
            ang = -0.55 * math.cos(math.pi * p)
            if t < 0.43:
                real += T.polys(_adaga(x, y, ang, 1.25), 0.003)
            continue
        x = -0.6 + 0.42 * ease_in(p, 1.2)
        y = ay * ease_out(min(1.0, p * 1.8), 2) * (1 - 0.3 * p)
        ang = math.atan2(-ay * 0.5, 1.0) * ease_in(p, 1.5)
        d0 = 0.33 + 0.02 * k
        some_ = rel(t, d0, d0 + 0.12)
        if some_ < 1:
            treme = 0.55 + 0.45 * math.sin(t * 90 + k * 2.1)
            falso += T.polys(_adaga(x + 0.03 * math.sin(t * 70 + k), y, ang, 1.25 * (1 - 0.3 * some_)), 0.006) * treme * (1 - some_)
        q = rel(t, d0, 0.75)
        if 0 < q < 1:
            for _ in range(5):
                a = sub.uniform(0, TAU)
                d = 0.05 + 0.2 * ease_out(q, 2) * sub.uniform(0.4, 1)
                fumaca.append((x + 0.12 + math.cos(a) * d, y + math.sin(a) * d - 0.12 * q, (1 - q) * 0.7))
    # a verdadeira acerta
    k2 = pulso(t, 0.4, 0.72)
    cravada = (1 - rel(t, 0.62, 0.82)) * janela(t, 0.41, 0.43)
    real += T.polys(_adaga(-0.3, 0.0, 0.0, 1.25), 0.003) * cravada
    corte = T.polys([(lamina(-0.45, 0.35, 0.45, -0.35, 0.05, ease_out(rel(t, 0.42, 0.52), 2), ease_in(rel(t, 0.55, 0.8))), 1.0)], 0.004)
    g, h = _clarao(T, k2, 0.15, 0.0, 0.18, 0.6)
    Fm = T.splats(fumaca, 0.04) if fumaca else T.zero()
    G += (falso * 0.9 + T.blur(falso, 0.025) * 0.5 + real * 1.2 + T.blur(real, 0.02) * 0.6 + split + Fm * 0.8 + corte * 1.3 + g) * env
    H += (real * 0.9 + corte * 1.2 + split * 0.6 + h) * env
    return G, H


# ------------------------------------------------------------------ Galactus
def toque_do_devorador(T, t, rng):
    """Toque do Devorador (Galactus): uma mão cósmica enorme, cheia de estrelas, desce do alto
    e fecha os dedos em volta do alvo; a matéria dele se parte em fragmentos que giram e
    são sugados para a palma."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    chega = ease_out(rel(t, 0.0, 0.26), 2.2)
    ang = math.pi / 4 + 0.1
    px, py = -1.4 + 0.72 * chega, -1.4 + 0.72 * chega
    fecha = ease_out(rel(t, 0.22, 0.5), 2) * (1 - 0.4 * rel(t, 0.8, 1))
    mao, _ = _mao(T, px, py, ang, 2.6, curl=0.06 + 0.42 * fecha, aberto=1.9, dedo=0.06)
    borda = contorno(T.blur(mao, 0.008), 0.3, 0.5, 0.62, 0.9)
    sub = np.random.default_rng(1707)
    estrelas = [(px + sub.uniform(-0.9, 0.9), py + sub.uniform(-0.9, 0.9), sub.uniform(0.3, 1) * (0.6 + 0.4 * math.sin(t * 20 + i))) for i in range(55)]
    E = T.splats(estrelas, 0.012) * mao
    # o alvo: um corpo de matéria que racha e se desfaz em fragmentos
    desfaz = rel(t, 0.36, 0.95)
    alvo = T.gauss(0.12, 0.12, 0.24, 0.3) * janela(t, 0.15, 0.3) * (1 - ease_out(desfaz, 1.5)) * 0.7
    cacos = []
    cx_, cy_ = px + 0.25, py + 0.25
    for i in range(26):
        a0 = sub.uniform(0, TAU)
        r0 = sub.uniform(0.04, 0.36)
        x0, y0 = 0.12 + math.cos(a0) * r0 * 0.8, 0.12 + math.sin(a0) * r0
        inicio = 0.36 + 0.25 * (1 - r0 / 0.36) * sub.uniform(0.6, 1)
        tam0 = sub.uniform(0.04, 0.07)
        q = ease_in(rel(t, inicio, inicio + 0.38), 1.7)
        if q >= 1 or t < 0.3:
            continue
        gira = q * 2.5
        x = x0 + (cx_ - x0) * q + math.sin(gira + a0) * 0.12 * q * (1 - q) * 4
        y = y0 + (cy_ - y0) * q - math.cos(gira + a0) * 0.12 * q * (1 - q) * 4
        cacos.append((_quadradinho(x, y, tam0 * (1 - 0.7 * q), a0 + t * 12), 1.0 - 0.5 * q))
    C = T.polys(cacos, 0.003) if cacos else T.zero()
    rach = T.zero()
    k = pulso(t, 0.28, 0.6)
    if k > 0:
        for j in range(6):
            a = TAU * j / 6 + 0.3
            rach += T.polyline(jagged(np.random.default_rng(1708 + j), 0.12, 0.12, 0.12 + math.cos(a) * 0.32, 0.12 + math.sin(a) * 0.36, 4, 0.3), 0.016)
    palma = T.gauss(cx_, cy_, 0.16, 0.16) * janela(t, 0.45, 0.7) * (1 - rel(t, 0.85, 1)) * 1.2
    G += (mao * 0.28 + borda * 1.1 + E * 1.3 + alvo + C * 1.2 + T.blur(C, 0.02) * 0.5 + rach * k * 1.3 + palma) * env
    H += (borda * 0.55 + E * 1.2 + C * 0.6 + rach * k * 1.0 + palma * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Senhor das Estrelas
def blasters_elementais(T, t, rng):
    """Blasters elementais (Senhor das Estrelas): os dois blasters disparam alternados, um
    de cima e um de baixo; cada tiro é uma cápsula de plasma que estoura no alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    tiros = ((0.0, -0.22, -0.08), (0.16, 0.2, 0.08), (0.32, -0.22, -0.02), (0.48, 0.2, 0.05))
    B, Bh, flash, estouro, estouro_h = T.zero(), T.zero(), T.zero(), T.zero(), T.zero()
    sub = np.random.default_rng(1909)
    fa = []
    for k, (s, y0, yh) in enumerate(tiros):
        ox = -0.88
        m = pulso(t, s - 0.02, s + 0.12)
        if m > 0:
            flash += T.flare(ox, y0, 0.45 * m + 0.01, ang=0.0, thin=0.035) * m + T.gauss(ox, y0, 0.09) * m * 1.6
        p = rel(t, s, s + 0.16)
        if 0 < p < 1:
            hx = ox + (0.0 - ox) * p
            hy = y0 + (yh - y0) * p
            ang = math.atan2(yh - y0, -ox)
            ca, sa = math.cos(ang), math.sin(ang)
            B += T.polys([(lamina(hx - ca * 0.48, hy - sa * 0.48, hx, hy, 0.075), 1.0)], 0.01)
            Bh += T.polys([(lamina(hx - ca * 0.36, hy - sa * 0.36, hx - ca * 0.04, hy - sa * 0.04, 0.032), 1.0)], 0.004)
        e = pulso(t, s + 0.14, s + 0.36)
        if e > 0:
            r = 0.06 + 0.24 * ease_out(rel(t, s + 0.14, s + 0.36), 2)
            estouro += T.polys([(estrela(0.0, yh, 0.24 * e + 0.01, k * 0.5, 6, 0.42), 1.0)], 0.006) * e + T.ring(r, 0.025, 0.0, yh) * e
            estouro_h += T.polys([(estrela(0.0, yh, 0.11 * e + 0.01, k * 0.5, 6, 0.42), 1.0)], 0.004) * e
            q = rel(t, s + 0.14, s + 0.38)
            for _ in range(5):
                a = sub.uniform(-2.2, 2.2)
                d = 0.1 + 0.32 * ease_out(q, 2) * sub.uniform(0.5, 1)
                fa.append((math.cos(a) * d, yh + math.sin(a) * d, (1 - q) * 0.9))
    S = T.splats(fa, 0.016) if fa else T.zero()
    G += (B * 1.3 + T.blur(B, 0.03) * 0.8 + flash + estouro * 1.2 + T.blur(estouro, 0.04) * 0.6 + S * 1.4) * env
    H += (Bh * 1.6 + flash * 0.7 + estouro_h * 1.4 + estouro * 0.3 + S * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Rocket
def arma_grande(T, t, rng):
    """Rajada da arma grande (Rocket): o canhão carrega (luz se juntando na boca), dá o
    tranco com um clarão enorme e solta uma bola de plasma gorda que explode no alvo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    bx = -0.78 - 0.08 * pulso(t, 0.2, 0.42)  # o tranco: a boca recua
    carga = janela(t, 0.0, 0.2) * (1 - rel(t, 0.2, 0.24))
    bola0 = T.gauss(bx, 0.0, 0.03 + 0.07 * carga) * carga * 1.6
    junta = T.zero()
    if carga > 0:
        sub = np.random.default_rng(2102)
        segs = []
        for _ in range(10):
            a = sub.uniform(0, TAU)
            d = 0.06 + 0.3 * (1 - carga) + 0.1 * sub.uniform()
            segs.append((bx + math.cos(a) * (d + 0.14), math.sin(a) * (d + 0.14), bx + math.cos(a) * d, math.sin(a) * d, 0.8))
        junta = T.tapered(segs, 0.018) * carga
    tranco = pulso(t, 0.19, 0.36)
    boca = T.flare(bx + 0.05, 0.0, 0.6 * tranco + 0.01, ang=0.0, thin=0.04) * tranco + T.gauss(bx + 0.1, 0.0, 0.16, 0.12) * tranco * 1.5
    cone = T.polys([([(bx, 0.0), (bx + 0.32, -0.16), (bx + 0.42, 0.0), (bx + 0.32, 0.16)], 1.0)], 0.03) * tranco
    voo = rel(t, 0.2, 0.34)
    bola, rastro = T.zero(), T.zero()
    if 0 < voo < 1:
        x = bx + (0.0 - bx) * ease_in(voo, 1.3)
        bola = T.gauss(x, 0.0, 0.11, 0.1) * 1.8
        rastro = T.polys([(lamina(bx, 0.0, x, 0.0, 0.11), 1.0)], 0.02) * 0.8
    ex = rel(t, 0.33, 0.95)
    fogo, choque, detritos = T.zero(), T.zero(), []
    if ex > 0:
        sub = np.random.default_rng(2103)
        R = 0.12 + 0.36 * ease_out(ex, 2.4)
        for j in range(8):
            a = TAU * j / 8 + sub.uniform(-0.3, 0.3)
            d = R * sub.uniform(0.45, 0.95)
            rr = R * sub.uniform(0.3, 0.45)
            fogo += T.gauss(math.cos(a) * d, math.sin(a) * d - 0.12 * ex, rr, rr)
        fogo = fogo + T.gauss(0, -0.05 * ex, R * 0.45) * 0.9
        ruido = T.noise(np.random.default_rng(2104), 0.06, 2)
        cheio = forma(fogo * (1 + 0.3 * ruido), 0.45 + 0.5 * ex, 0.7 + 0.5 * ex)
        fogo = cheio * (1 - ex) ** 0.5 * 1.1 + contorno(fogo * (1 + 0.3 * ruido), 0.3, 0.4, 0.5, 0.7) * (1 - ex) * 0.6 + T.gauss(0, 0, R * 0.4) * (1 - ex) ** 2 * 1.5
        choque = T.ring(0.15 + 0.75 * ease_out(ex, 2), 0.04) * (1 - ex) * 1.3
        for _ in range(10):
            a = sub.uniform(0, TAU)
            d = 0.15 + 0.6 * ease_out(ex, 2) * sub.uniform(0.6, 1)
            detritos.append((_pedra(sub, math.cos(a) * d, math.sin(a) * d + 0.25 * ex * ex, 0.035, a + t * 8), (1 - ex)))
    D = T.polys(detritos, 0.003) if detritos else T.zero()
    g, h = _clarao(T, pulso(t, 0.32, 0.55), 0.0, 0.0, 0.3, 1.0)
    G += (bola0 + junta + boca + cone * 0.8 + bola + rastro + fogo + choque + D * 1.2 + g) * env
    H += (bola0 * 1.2 + junta * 0.5 + boca * 0.8 + bola * 0.9 + rastro * 0.3 + fogo * (1 - ex) * 0.7 + choque * 0.3 + D * 0.4 + h) * env
    return G, H


# ------------------------------------------------------------------ Aquaman
def _tridente(x, y, ang):
    """Tridente apontando para +x, com a ponta central em (x, y)."""
    pts = [(lamina(-0.3, 0.0, 0.0, 0.0, 0.035), 1.0)]
    for s in (-1, 1):
        pts.append((lamina(-0.26, 0.11 * s, -0.04, 0.115 * s, 0.03), 1.0))
        pts.append(([(-0.08, 0.115 * s), (-0.13, 0.17 * s), (-0.1, 0.115 * s)], 1.0))  # farpa
    pts.append(([(-0.04, 0.0), (-0.12, -0.05), (-0.12, 0.05)], 1.0))
    u = [(-0.2, -0.13), (-0.28, -0.12), (-0.33, -0.06), (-0.34, 0.06), (-0.28, 0.12), (-0.2, 0.13),
         (-0.2, 0.095), (-0.27, 0.085), (-0.3, 0.04), (-0.3, -0.04), (-0.27, -0.085), (-0.2, -0.095)]
    pts.append((u, 1.0))
    pts.append(([(-0.33, -0.02), (-1.8, -0.02), (-1.8, 0.02), (-0.33, 0.02)], 1.0))
    return [(_move(_gira(p, ang), x, y), w) for p, w in pts]


def tridente(T, t, rng):
    """Golpe do tridente (Aquaman): o tridente de três pontas avança numa estocada com uma
    espiral de água em volta da haste e explode o alvo num respingo de gotas grossas."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    ida = ease_out(rel(t, 0.02, 0.22), 3)
    volta = ease_in(rel(t, 0.55, 0.85), 2)
    x = -0.85 + 0.97 * ida - 0.6 * volta
    vis = 1 - rel(t, 0.7, 0.86)
    tri = T.polys(_tridente(x, 0.0, 0.0), 0.003) * vis
    esp = T.zero()
    agua_on = pulso(t, 0.02, 0.55)
    if agua_on > 0:
        pts = []
        for j in range(60):
            u = j / 59
            pts.append((x - 0.25 - 0.9 * u, 0.075 * math.sin(u * 14 - t * 40) * (1 - u * 0.4)))
        esp = T.polyline(pts, 0.022) * agua_on + T.polyline([(a, -b) for a, b in pts], 0.014) * agua_on * 0.6
    impacto = rel(t, 0.18, 0.75)
    k = pulso(t, 0.17, 0.42)
    g, h = _clarao(T, k, 0.08, 0.0, 0.18, 0.7, 0.0)
    sub = np.random.default_rng(2303)
    gotas = []
    if impacto > 0:
        for _ in range(14):
            a = sub.uniform(-2.6, 2.6)
            v = sub.uniform(0.55, 1.0)
            r = sub.uniform(0.7, 1.2)
            d = 0.1 + 0.62 * ease_out(impacto, 1.8) * v
            gx = 0.08 + math.cos(a) * d * 0.9 + 0.12 * impacto
            gy = math.sin(a) * d * 0.8 - 0.25 * impacto + 0.75 * impacto * impacto
            vx, vy = math.cos(a), math.sin(a) - 0.6 + 2.0 * impacto
            gotas.append((_gota(gx, gy, 0.04 * (1 - 0.4 * impacto) * r, math.atan2(vy, vx)), (1 - impacto) ** 0.7))
    Gt = T.polys(gotas, 0.004) if gotas else T.zero()
    onda = T.arc_band(0.16 + 0.42 * ease_out(rel(t, 0.18, 0.6), 2), 0.07, -1.7, 1.7, crescente=True) * pulso(t, 0.18, 0.62)
    anel = T.ring(0.1 + 0.5 * ease_out(rel(t, 0.18, 0.55), 2), 0.03, 0.08) * pulso(t, 0.18, 0.55) * 0.7
    G += (tri * 1.1 + T.blur(tri, 0.02) * 0.4 + esp * 1.2 + T.blur(esp, 0.02) * 0.5 + Gt * 1.3 + onda * 1.1 + anel + g) * env
    H += (tri * 0.6 + esp * 0.6 + Gt * 0.6 + onda * 0.5 + h) * env
    return G, H


# ------------------------------------------------------------------ Ciborgue
def canhao_sonico(T, t, rng):
    """Canhão sônico (Ciborgue): da boca do canhão à esquerda saem arcos de onda sonora,
    um atrás do outro, abrindo em cone; cada um bate no alvo e faz o ar tremer em anéis."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    ox = -0.9
    arcos, arcos_h, batidas = T.zero(), T.zero(), T.zero()
    for k in range(6):
        s = 0.065 * k
        p = rel(t, s, s + 0.2)
        if 0 < p < 1:
            frente = ox + (0.05 - ox) * p
            R = 0.16 + 0.42 * p
            a = T.arc_band(R, 0.065, -0.95, 0.95, cx=frente - R, cy=0.0, crescente=True)
            arcos += a * (0.7 + 0.3 * math.sin(math.pi * p))
            arcos_h += a * 0.6
        q = rel(t, s + 0.18, s + 0.42)
        if 0 < q < 1:
            batidas += _anel_torto(T, 0.05, 0.0, 0.08 + 0.45 * ease_out(q, 2), 0.035, k * 1.3 + t * 30, 0.05, 8) * (1 - q)
    feixe = T.gauss(-0.4, 0.0, 0.5, 0.05) * pulso(t, 0.0, 0.55) * 0.5
    boca = T.gauss(ox, 0.0, 0.07) * pulso(t, 0.0, 0.5) * (0.7 + 0.3 * math.sin(t * 60)) * 1.6
    k = pulso(t, 0.18, 0.7)
    nucleo = T.gauss(0.05, 0.0, 0.12) * k * (0.8 + 0.2 * math.sin(t * 70))
    g_ = arcos * 1.3 + T.blur(arcos, 0.025) * 0.5 + batidas * 1.1 + feixe + boca + nucleo
    h_ = arcos_h + batidas * 0.5 + boca * 0.8 + nucleo * 0.8
    dist = pulso(t, 0.2, 0.9)
    G += _entorta(T, g_, 0.05, 0.0, dist, t, 34, 60) * env
    H += _entorta(T, h_, 0.05, 0.0, dist, t, 34, 60) * env
    return G, H


# ------------------------------------------------------------------ Pantera Negra
def garras_cineticas(T, t, rng):
    """Corte cinético (Pantera Negra): três garras de vibranium rasgam na diagonal, outras três
    cruzam em X; os talhos se enchem de energia roxa e estouram num pulso cinético."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    talhos, fio = T.zero(), T.zero()
    for a0, ang in ((0.0, 0.75), (0.13, -0.75 + math.pi)):
        c, s = math.cos(ang), math.sin(ang)
        nx, ny = -s, c
        p = ease_out(rel(t, a0, a0 + 0.1), 2)
        fim = ease_in(rel(t, 0.42, 0.56), 1.2)
        if p <= 0:
            continue
        for j in (-1, 0, 1):
            off = 0.13 * j
            L = 0.62 - 0.08 * abs(j)
            x1, y1 = -c * L + nx * off, -s * L + ny * off
            x2, y2 = c * L + nx * off, s * L + ny * off
            talhos += T.polys([(lamina(x1, y1, x2, y2, 0.045, p, fim), 1.0)], 0.003)
            fio += T.polys([(lamina(x1, y1, x2, y2, 0.014, p, fim), 1.0)], 0.002)
    enche = janela(t, 0.24, 0.42) * (1 - rel(t, 0.44, 0.56))
    ex = rel(t, 0.42, 0.95)
    k = pulso(t, 0.4, 0.95)
    onda = (T.ring(0.08 + 0.75 * ease_out(ex, 2.2), 0.06) * 1.2 + T.ring(0.04 + 0.48 * ease_out(ex, 2.6), 0.03) * 0.8) * k
    raios = T.zero()
    if k > 0:
        segs = []
        for j in range(12):
            a = TAU * j / 12 + 0.13
            r0 = 0.12 + 0.55 * ease_out(ex, 2)
            segs.append((math.cos(a) * (r0 - 0.24), math.sin(a) * (r0 - 0.24), math.cos(a) * r0, math.sin(a) * r0, 1.0))
        raios = T.tapered(segs, 0.03) * k
    hexa = T.polyline([(math.cos(TAU * j / 6) * 0.2, math.sin(TAU * j / 6) * 0.2) for j in range(7)], 0.02) * pulso(t, 0.36, 0.62)
    g, h = _clarao(T, pulso(t, 0.38, 0.62), 0, 0, 0.22, 0.8)
    G += (talhos * (1.1 + 0.8 * enche) + T.blur(talhos, 0.03) * (0.4 + 1.2 * enche) + onda + raios * 1.2 + hexa * 1.3 + g) * env
    H += (fio * 1.5 + talhos * 0.3 * enche + onda * 0.4 + raios * 0.6 + hexa + h) * env
    return G, H


# ------------------------------------------------------------------ Darkseid
def _omega(cx, cy, r):
    pts = []
    for j in range(31):
        a = math.pi / 2 + 0.6 + (TAU - 1.2) * j / 30
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r * 1.05))
    pe0 = (pts[0][0] - r * 0.42, pts[0][1] + r * 0.12)
    pe1 = (pts[-1][0] + r * 0.42, pts[-1][1] + r * 0.12)
    return [pe0] + pts + [pe1]


def punho_de_apokolips(T, t, rng):
    """Punho de Apokolips (Darkseid): um punho pesado vem da esquerda e afunda no alvo;
    o impacto racha tudo em volta, o símbolo Ômega acende e os feixes Ômega saem
    serpenteando em zigue-zague."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    vem = ease_in(rel(t, 0.0, 0.16), 2.2)
    sai = ease_in(rel(t, 0.3, 0.6), 1.5)
    fx = -1.3 + 1.05 * vem - 0.5 * sai
    vis = 1 - rel(t, 0.42, 0.6)
    punho = [(-0.45, -0.22), (0.08, -0.27), (0.22, -0.22), (0.27, -0.08), (0.27, 0.1), (0.22, 0.22), (0.05, 0.27), (-0.45, 0.22)]
    P = T.polys([(_move(punho, fx, 0.0), 1.0)], 0.005) * vis
    dobras = T.lines([(fx + 0.08, -0.26 + 0.13 * j, fx + 0.26, -0.26 + 0.13 * j, 1.0) for j in range(1, 4)]
                     + [(fx - 0.05, -0.2, fx + 0.12, -0.05, 1.0)], 0.016) * vis
    vel = rastro_de_velocidade(T, rng, 9, 0.0, 0.5, 0.2, 0.25, fx, 0.0, 0.016, seed=2501) * pulso(t, 0.0, 0.22)
    imp = rel(t, 0.15, 0.9)
    k = pulso(t, 0.14, 0.42)
    g, h = _clarao(T, k, 0.1, 0.0, 0.26, 0.9, 0.0)
    choque = T.ring(0.1 + 0.7 * ease_out(imp, 2.4), 0.05, 0.1) * (1 - imp) * 1.2
    rach = T.zero()
    cresce = ease_out(rel(t, 0.15, 0.36), 2)
    if cresce > 0:
        for j in range(6):
            a = TAU * j / 6 + 0.5
            pts = jagged(np.random.default_rng(2510 + j), 0.1 + math.cos(a) * 0.28, math.sin(a) * 0.28, 0.1 + math.cos(a) * 0.72, math.sin(a) * 0.72, 3, 0.25)
            rach += T.polyline(_corta_caminho(pts, cresce), 0.022)
        rach *= 1 - rel(t, 0.55, 0.85)
    om = pulso(t, 0.24, 0.8)
    O = T.polyline(_omega(0.1, -0.03, 0.2), 0.045) * om
    feixes = T.zero()
    q = rel(t, 0.3, 0.75)
    if 0 < q < 1:
        for j in range(4):
            a0 = -2.4 + 1.6 * j
            pts = []
            for i in range(30):
                u = i / 29 * ease_out(q, 1.5)
                r = 0.18 + 0.62 * u
                a = a0 + 0.9 * u + 0.25 * (1 if (i // 4) % 2 else -1) * u
                pts.append((0.1 + math.cos(a) * r, math.sin(a) * r))
            feixes += T.polyline(pts, 0.016)
        feixes *= 1 - q
    G += (P * 0.85 + dobras * 0.3 + vel * 0.8 + choque + T.glow(rach, 1.2, 0.9, 0.02) + O * 1.3 + T.blur(O, 0.03) * 1.0 + T.glow(feixes, 1.2, 1.0, 0.02) + g) * env
    H += (contorno(T.blur(P, 0.006), 0.3, 0.5, 0.65, 0.9) * 0.6 + dobras * 0.6 + rach * 0.8 + O * 1.1 + feixes * 0.9 + h) * env
    return G, H


# ------------------------------------------------------------------ Hellboy
def mao_da_perdicao(T, t, rng):
    """Mão Direita da Perdição (Hellboy): o punho enorme de pedra, de placas e juntas, desce
    do alto e esmaga o alvo; o chão racha e voa cascalho com poeira."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    desce = ease_in(rel(t, 0.0, 0.2), 2.4)
    sobe = ease_in(rel(t, 0.58, 0.88), 1.6)
    fy = -1.35 + 1.43 * desce - 0.9 * sobe   # base do punho
    sq = 1 - 0.1 * pulso(t, 0.19, 0.32)
    w = 0.3 / sq
    vis = 1 - rel(t, 0.72, 0.88)
    # o punho visto de frente, apontando para baixo: bloco arredondado de pedra,
    # quatro dedos com os nós embaixo, o polegar atravessado e o pulso com a braçadeira
    bloco = []
    for j in range(40):
        a_ = TAU * j / 40
        c_, s_ = math.cos(a_), math.sin(a_)
        bloco.append((w * math.copysign(abs(c_) ** 0.4, c_), fy - 0.3 + 0.27 * sq * math.copysign(abs(s_) ** 0.4, s_)))
    pulso_ = [(-0.2, fy - 0.5), (0.2, fy - 0.5), (0.18, fy - 1.4), (-0.18, fy - 1.4)]
    nos = [(-w * 0.75 + w * 0.5 * j, fy - 0.075) for j in range(4)]
    fill = T.polys([(bloco, 1.0), (pulso_, 1.0)]) + sum(T.gauss(x_, y_, 0.075, 0.07) for x_, y_ in nos) * 1.6
    P = np.minimum(T.blur(np.minimum(fill, 1.0), 0.006), 1.0) * vis
    juntas = T.splats([(x_, y_ + 0.01, 1.0) for x_, y_ in nos], 0.03) * vis
    placas = (T.lines([(-w * 0.5, fy - 0.03, -w * 0.5, fy - 0.24, 1.0), (0.0, fy - 0.03, 0.0, fy - 0.24, 1.0), (w * 0.5, fy - 0.03, w * 0.5, fy - 0.24, 1.0),
                       (-0.24, fy - 0.6, 0.24, fy - 0.6, 1.0), (-0.22, fy - 0.7, 0.22, fy - 0.7, 1.0)], 0.016)
              + T.polyline([(-w * 0.95, fy - 0.36), (-w * 0.4, fy - 0.33), (0.05, fy - 0.3), (0.12, fy - 0.24)], 0.03)
              + T.polyline(jagged(np.random.default_rng(2720), w * 0.3, fy - 0.5, w * 0.8, fy - 0.36, 3, 0.3), 0.012)
              + T.polyline(jagged(np.random.default_rng(2721), -0.1, fy - 0.85, 0.05, fy - 1.1, 3, 0.3), 0.012)) * vis
    vel = T.lines([(sx_ * (w + 0.06 + 0.07 * j), fy - 0.35 - 0.06 * j, sx_ * (w + 0.06 + 0.07 * j), fy - 1.0 - 0.06 * j, 0.7) for j in range(3) for sx_ in (-1, 1)], 0.012) * pulso(t, 0.02, 0.24)
    chao = 0.12
    imp = rel(t, 0.19, 0.9)
    k = pulso(t, 0.18, 0.42)
    choque = T.ring(0.1 + 0.75 * ease_out(imp, 2.2), 0.05, 0.0, chao, squash=2.6) * (1 - imp) * 1.4
    flash = T.gauss(0.0, chao, 0.38, 0.08) * k * 1.0
    rach = T.zero()
    cresce = ease_out(rel(t, 0.2, 0.4), 2)
    if cresce > 0:
        for j in range(7):
            a = math.pi * (j + 0.5) / 7
            lado = math.cos(a)
            pts = jagged(np.random.default_rng(2710 + j), lado * 0.2, chao, lado * 0.9, chao + 0.06 + 0.14 * math.sin(a), 4, 0.25)
            rach += T.polyline(_corta_caminho(pts, cresce), 0.016)
        rach *= 1 - rel(t, 0.65, 0.95)
    sub = np.random.default_rng(2703)
    pedras = []
    if imp > 0:
        for _ in range(14):
            a = sub.uniform(-math.pi + 0.25, -0.25)
            v = sub.uniform(0.5, 1.0)
            r = sub.uniform(0.03, 0.055)
            d = 0.25 + 0.65 * ease_out(imp, 1.6) * v
            pedras.append((_pedra(sub, math.cos(a) * d, chao + math.sin(a) * d * 0.9 + 0.9 * imp * imp, r, a + imp * 6 * v), (1 - imp) ** 0.6))
    Pd = T.polys(pedras, 0.003) if pedras else T.zero()
    po = poeira(T, rng, t, 26, 0.0, chao, 0.85, 0.3, 0.05, inicio=0.2)
    G += (P * 0.8 + juntas * 0.4 + vel * 0.6 + choque + flash + T.glow(rach, 1.2, 0.8, 0.02) + Pd * 1.2 + po * 0.6) * env
    H += (contorno(T.blur(P, 0.006), 0.3, 0.5, 0.65, 0.9) * 0.55 + placas * 0.6 + juntas * 0.5 + flash * 0.9 + rach * 0.8 + Pd * 0.35) * env
    return G, H


REGISTRO = [
    ("toque_absorvente", toque_absorvente, GRANDE, "Vampira: a mão toca e suga fios de vida do alvo", False),
    ("golpe_psiquico", golpe_psiquico, GRANDE, "Professor X: ondas psíquicas fecham na cabeça e estouram", False),
    ("tentaculo_simbionte", tentaculo_simbionte, GRANDE, "Venom: tentáculos lisos chicoteiam e enrolam o alvo", False),
    ("lamina_viva", lamina_viva, GRANDE, "Carnificina: lâminas vivas retorcidas rasgam em quatro ângulos", False),
    ("adaga_ilusoria", adaga_ilusoria, GRANDE, "Loki: a adaga se divide em ilusões; só a verdadeira crava", False),
    ("toque_do_devorador", toque_do_devorador, GRANDE, "Galactus: mão cósmica fecha e suga a matéria em fragmentos", False),
    ("blasters_elementais", blasters_elementais, GRANDE, "Senhor das Estrelas: dois blasters alternando tiros de plasma", False),
    ("arma_grande", arma_grande, GRANDE, "Rocket: carga, tranco e bola de plasma que explode", False),
    ("tridente", tridente, GRANDE, "Aquaman: estocada do tridente com espiral e respingo de água", False),
    ("canhao_sonico", canhao_sonico, GRANDE, "Ciborgue: arcos de onda sonora em sequência", False),
    ("garras_cineticas", garras_cineticas, GRANDE, "Pantera Negra: garras em X e pulso cinético", False),
    ("punho_de_apokolips", punho_de_apokolips, GRANDE, "Darkseid: punho pesado, rachaduras, Ômega e feixes", False),
    ("mao_da_perdicao", mao_da_perdicao, GRANDE, "Hellboy: o punho de pedra desce e esmaga com cascalho", False),
]
