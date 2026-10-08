"""Ferramentas comuns às famílias novas (além das de luz.py e generate_families.py)."""
from __future__ import annotations

import math

import numpy as np

from luz import Tela, apaga, ease_in, ease_out, jagged, janela, pulso, smooth, some  # noqa: F401
from generate_families import (FAIXA, GRANDE, MEDIA, PEQUENA, TAU, _cauda_de_particulas, _subindo,  # noqa: F401
                               faiscas, vazio)


def back(t: float, s: float = 1.7) -> float:
    """Sai do zero, passa um pouco do ponto e volta (o "pop" de um desenho animado)."""
    t = min(max(t, 0.0), 1.0) - 1
    return t * t * ((s + 1) * t + s) + 1


def rel(t: float, a: float, b: float) -> float:
    """Tempo local entre a e b (0..1, preso)."""
    return min(1.0, max(0.0, (t - a) / max(b - a, 1e-4)))


def estrela(cx, cy, r, ang=0.0, n=5, interno=0.45, sq=1.0):
    """Polígono de estrela de n pontas (contorno alternando raio externo e interno)."""
    pts = []
    for k in range(2 * n):
        rr = r if k % 2 == 0 else r * interno
        a = ang + math.pi * k / n
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * sq))
    return pts


def lamina(x1, y1, x2, y2, larg, prog=1.0, inicio=0.0, n=24):
    """Lente afiada de (x1,y1) a (x2,y2): fina nas pontas, larga no meio.

    `prog` revela da origem até a ponta; `inicio` come a cauda (o corte some
    do começo para o fim, como uma lâmina que passou).
    """
    dx, dy = x2 - x1, y2 - y1
    comp = math.hypot(dx, dy) or 1
    nx, ny = -dy / comp, dx / comp
    a, b = inicio, max(inicio + 1e-3, prog)
    cima, baixo = [], []
    for k in range(n + 1):
        u = a + (b - a) * k / n
        w = larg * math.sin(math.pi * min(1, max(0, u))) ** 0.8
        x, y = x1 + dx * u, y1 + dy * u
        cima.append((x + nx * w, y + ny * w))
        baixo.append((x - nx * w, y - ny * w))
    return cima + baixo[::-1]


def girado(T, ang, cx=0.0, cy=0.0):
    """Coordenadas (ao longo, de lado) num eixo girado por `ang`."""
    du, dv = T.U - cx, T.V - cy
    c, s = math.cos(ang), math.sin(ang)
    return du * c + dv * s, -du * s + dv * c


def forma(campo, a=0.5, b=0.62):
    """Campo suave → silhueta cheia (o "corpo" de uma forma feita de gaussianas)."""
    return smooth(campo, a, b)


def contorno(campo, a=0.5, b=0.62, dentro=0.78, fim=0.95):
    """Só a borda de uma silhueta: cheia menos o miolo."""
    return smooth(campo, a, b) * (1 - smooth(campo, dentro, fim))


def poeira(T, rng, t, n, cx, cy, espalha, sobe, sigma=0.03, inicio=0.0):
    """Nuvem de poeira: bolotas que crescem, sobem um pouco e esmaecem."""
    tt = rel(t, inicio, 1.0)
    pts = []
    for _ in range(n):
        a = rng.uniform(-math.pi, 0) if sobe else rng.uniform(0, TAU)
        d = rng.uniform(0.2, 1.0) * espalha * ease_out(tt, 2)
        pts.append((cx + math.cos(a) * d, cy + math.sin(a) * d * 0.5 - sobe * tt, (1 - tt) ** 1.3 * rng.uniform(0.4, 1)))
    return T.splats(pts, sigma * (1 + tt))


def rastro_de_velocidade(T, rng, n, ang, comprimento, espalha, avanco, cx=0.0, cy=0.0, largura=0.012, seed=9):
    """Linhas de velocidade paralelas a `ang`, terminando perto do centro."""
    sub = np.random.default_rng(seed)
    c, s = math.cos(ang), math.sin(ang)
    segs = []
    for _ in range(n):
        off = sub.uniform(-espalha, espalha)
        comp = sub.uniform(0.4, 1.0) * comprimento
        d0 = sub.uniform(0.05, 0.35) + avanco
        hx, hy = cx - c * d0 - s * off, cy - s * d0 + c * off
        segs.append((hx - c * comp, hy - s * comp, hx, hy, sub.uniform(0.5, 1)))
    return T.tapered(segs, largura)
