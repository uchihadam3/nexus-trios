"""Rodada 15 das habilidades próprias: Professor Xavier, Venom, Carnificina, Doutor Destino e Loki (Marvel).

Professor Xavier
- coordenacao_mental: as ondas saem da cabeça do Professor e ligam os três aliados por fios psíquicos que
  pulsam, com as setas de Acelerado subindo e o brilho da limpeza.
- bloqueio_mental: os dois dedos na têmpora, os anéis psíquicos voam até a cabeça do rival e a intenção dele
  (a seta) bate num bloqueio e quebra; as espirais de Confuso ficam.
- cerebro_preparo: o Preparo da Paralisia mental — o capacete do Cérebro (as faixas curvas e os fios) com as
  ondas de varredura girando em volta (laço).
- paralisia_mental: a onda psíquica enorme varre o campo, os rivais ficam presos no contorno roxo e as faixas
  de Silenciado cortam a boca de cada um.

Venom
- mordida_predatoria: a bocarra do simbionte (as duas fileiras de dentes compridos e a língua) se abre enorme e
  fecha no rival; a gosma preta pinga e o verde da cura volta para o Venom.
- venom_preparo: o Preparo do Simbionte faminto — a gosma preta borbulhando com os dois olhos brancos
  pontudos aparecendo e os fios se esticando (laço).
- simbionte_faminto: a massa do simbionte explode em tentáculos de todos os lados, engole o rival e a aranha
  branca do peito pisca no meio.

Carnificina
- ferida_aberta: dois chicotes vermelhos de simbionte cortam em X, a ferida abre com o sangue espirrando e a
  marca aparece.
- carnificina_preparo: o Preparo da Carnificina total — os tentáculos vermelhos se debatendo em volta em
  espiral, virando lâminas nas pontas (laço).
- carnificina_total: as lâminas e machados vermelhos vêm de todos os lados em sequência rápida, os cortes se
  cruzam no rival e o sangue espirra para todo lado.

Doutor Destino
- armadura_de_doom: a grade verde de análise varre o rival, o alvo trava e a manopla dispara o raio; o escudo
  verde fecha em volta do Destino.
- ritual_latveriano: o círculo místico verde com as runas se abre sob o rival e os raios verdes sobem e o
  travam (Paralisado); o escudo verde fecha.
- destino_preparo: o Preparo do Plano de contingência — a máscara de ferro (as frestas dos olhos e a grade da
  boca) com a energia mística verde girando em volta (laço).
- plano_de_contingencia: tecnologia e magia juntas — os lasers caem do alto em grade enquanto o círculo
  místico gira no chão, e tudo explode junto.

Loki
- troca_de_lugar: o Loki e o rival viram silhuetas verdes, trocam de lugar num redemoinho de fumaça verde e
  faíscas douradas, e a mira do rival se perde.
- loki_preparo: o Preparo do Engano perfeito — o elmo de chifres dourado no alto e as cópias de ilusão
  piscando em volta (laço).
- engano_perfeito: as cópias do Loki cercam o rival, quebram como vidro uma a uma, e o verdadeiro surge por
  trás com a adaga dourada.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, ease_in, ease_out, jagged, lamina, pulso, rel, vazio
from .rodada13 import _borda, _contorno, _gira


def _cabeca(cx, cy, s):
    """O perfil da cabeça careca virado para a direita (o Professor)."""
    pts = [(cx + s * (0.14 * math.cos(a)), cy + s * (0.17 * math.sin(a))) for a in np.linspace(math.radians(110), math.radians(400), 26)]
    pts += [(cx + 0.15 * s, cy + 0.04 * s), (cx + 0.12 * s, cy + 0.08 * s), (cx + 0.1 * s, cy + 0.16 * s), (cx + 0.02 * s, cy + 0.2 * s)]
    return pts


def _silhueta(cx, cy, s, chifres=False):
    meia = [(0.05, -0.33), (0.13, -0.28), (0.14, -0.18), (0.08, -0.12), (0.22, -0.06), (0.25, 0.22), (0.17, 0.22), (0.15, 0.0),
            (0.13, 0.5), (0.03, 0.5), (0.0, 0.25)]
    corpo = [(cx + x * s, cy + y * s) for x, y in meia] + [(cx - x * s, cy + y * s) for x, y in reversed(meia[:-1])]
    linhas = _contorno(corpo)
    if chifres:
        for lado in (-1, 1):
            linhas += [(cx + lado * 0.08 * s, cy - 0.3 * s, cx + lado * 0.2 * s, cy - 0.5 * s, 1.0), (cx + lado * 0.2 * s, cy - 0.5 * s, cx + lado * 0.16 * s, cy - 0.62 * s, 1.0)]
    return corpo, linhas


# =================================================================== Professor Xavier
def coordenacao_mental(T, t, rng):
    """A coordenação mental: as ondas saem da cabeça do Professor e os fios psíquicos ligam os três aliados, pulsando
    em sequência; as setas de Acelerado sobem e cada um brilha limpo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    cab = (0.0, -0.45)
    ondas = pulso(t, 0.0, 0.5)
    if ondas > 0:
        G += T.lines(_contorno(_cabeca(cab[0], cab[1], 1.0)), 0.012) * ondas * 1.2
        for k in range(3):
            u = ((t * 3) + k / 3) % 1
            G += T.ring(0.12 + 0.3 * u, 0.012, cab[0], cab[1]) * (1 - u) * ondas
    aliados = [(-0.6, 0.25), (0.0, 0.3), (0.6, 0.25)]
    liga = ease_out(rel(t, 0.2, 0.45), 2)
    if liga > 0:
        b = 1 - rel(t, 0.8, 0.95)
        for x, y in aliados:
            pts = [(cab[0] + (x - cab[0]) * u, cab[1] + (y - cab[1]) * u + 0.05 * math.sin(u * 12 + t * 20)) for u in np.linspace(0, liga, 24)]
            G += T.polyline(pts, 0.01) * b * 1.1
            pul = ((t * 2) % 1)
            if pul < liga:
                H += T.gauss(cab[0] + (x - cab[0]) * pul, cab[1] + (y - cab[1]) * pul, 0.025) * b * 1.2
        for k, (x, y) in enumerate(aliados):
            c = pulso(t, 0.4 + 0.08 * k, 0.8 + 0.08 * k)
            if c > 0:
                G += T.ring(0.13, 0.016, x, y) * c * 1.2
                H += T.gauss(x, y, 0.08) * c * 0.6
                sy = y - 0.05 - 0.2 * rel(t, 0.4 + 0.08 * k, 0.8 + 0.08 * k)
                G += T.lines([(x - 0.06, sy + 0.05, x, sy - 0.01, 1.0), (x + 0.06, sy + 0.05, x, sy - 0.01, 1.0), (x, sy + 0.12, x, sy, 1.0)], 0.014) * c
    return G * env, H * env


def bloqueio_mental(T, t, rng):
    """O bloqueio mental: os dedos na têmpora, os anéis psíquicos voam até a cabeça do rival, a intenção dele (a seta
    carregando) bate no bloqueio e quebra; as espirais de Confuso ficam girando."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    dedos = pulso(t, 0.0, 0.45)
    if dedos > 0:
        cx, cy = -0.72, -0.1
        G += T.lines(_contorno(_cabeca(cx, cy, 0.9)), 0.011) * dedos * 1.1
        G += T.lines([(cx + 0.12, cy + 0.0, cx + 0.2, cy - 0.06, 1.0), (cx + 0.12, cy + 0.03, cx + 0.2, cy - 0.02, 1.0)], 0.014) * dedos
        H += T.gauss(cx + 0.04, cy - 0.05, 0.03) * dedos * 1.4
    for k in range(4):
        t0 = 0.08 + 0.06 * k
        u = rel(t, t0, t0 + 0.25)
        if 0 < u < 1:
            x = -0.6 + 0.6 * ease_in(u, 1.3)
            G += T.ring(0.09 + 0.06 * u, 0.018, x, -0.1, squash=1.6) * math.sin(math.pi * u) * 1.4
            H += T.ring(0.09 + 0.06 * u, 0.006, x, -0.1, squash=1.6) * math.sin(math.pi * u) * 0.6
    seta = rel(t, 0.25, 0.5)
    if 0 < seta < 1:
        x = 0.55 - 0.35 * ease_out(seta, 2)
        G += T.lines([(x + 0.4, 0.1, x, 0.1, 1.0), (x, 0.1, x + 0.12, 0.0, 1.0), (x, 0.1, x + 0.12, 0.2, 1.0)], 0.028) * 1.3
        H += T.gauss(x + 0.4, 0.1, 0.05) * 1.0
    quebra = rel(t, 0.5, 0.8)
    if 0 < quebra < 1:
        hexa = [(0.05 + 0.32 * math.cos(a) * 0.45, 0.1 + 0.32 * math.sin(a)) for a in np.linspace(-math.pi / 2, math.pi / 2, 4)]
        G += T.arc_band(0.32, 0.05, -1.2, 1.2, cx=-0.05, cy=0.1, crescente=True) * (1 - quebra) * 1.4 + T.lines(_contorno(hexa)[:-1], 0.01) * (1 - quebra)
        q = np.random.default_rng(31)
        cacos = [(_gira([(-0.05, -0.025), (0.05, 0.0), (0.0, 0.04)], q.uniform(0, 6) + quebra * 5, 0.25 + 0.45 * quebra * q.uniform(0.5, 1), 0.1 + 0.4 * quebra * q.uniform(-1, 1) + 0.2 * quebra * quebra), 1 - quebra) for _ in range(12)]
        G += T.polys(cacos) * 1.2
        H += T.gauss(0.2, 0.1, 0.06) * (1 - quebra) ** 2 * 1.5
    tonto = pulso(t, 0.5, 1.0)
    if tonto > 0:
        for k in range(3):
            a0 = t * 10 + TAU * k / 3
            ex, ey = 0.22 * math.cos(a0), -0.35 + 0.05 * math.sin(a0)
            pts = [(ex + 0.07 * (j / 30) * math.cos(t * 20 + TAU * 2 * j / 30), ey + 0.05 * (j / 30) * math.sin(t * 20 + TAU * 2 * j / 30)) for j in range(31)]
            G += T.polyline(pts, 0.011) * tonto * 1.2
    return G * env, H * env


def cerebro_preparo(T, t, rng):
    """O Preparo da Paralisia mental: o capacete do Cérebro (as faixas curvas sobre a cabeça e os fios descendo) e as
    ondas de varredura girando em volta (laço)."""
    G, H = vazio(T)
    G += T.lines(_contorno(_cabeca(0, 0.05, 1.6)), 0.013) * 1.0
    for k in range(4):
        G += T.arc_band(0.26 + 0.035 * k, 0.012, math.pi * 1.1, math.pi * 1.9, squash=1.0, cx=0.0, cy=0.05, crescente=True) * 1.2
    for lado in (-1, 1):
        G += T.polyline([(lado * 0.25, -0.05 + 0.03 * j * j / 4, ) if False else (lado * (0.24 + 0.03 * j), -0.05 + 0.1 * j) for j in range(6)], 0.008) * 0.9
    a = TAU * t
    for k in range(2):
        G += T.arc_band(0.55 + 0.1 * k, 0.025, a + k * math.pi, a + k * math.pi + 1.4, cx=0, cy=0.05, taper=0.4) * 1.1
    H += T.gauss(0, -0.15, 0.06) * (0.6 + 0.4 * math.sin(TAU * t * 2))
    return G, H


def paralisia_mental(T, t, rng):
    """A paralisia mental: a onda psíquica enorme sai e varre o campo, os três rivais ficam presos no contorno roxo
    que treme, e as faixas de Silenciado cruzam a boca de cada um."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    onda = rel(t, 0.0, 0.45)
    if 0 < onda < 1:
        for k in range(3):
            u = rel(onda, 0.15 * k, 0.7 + 0.15 * k)
            if 0 < u < 1:
                r = 0.2 + 1.9 * ease_out(u, 1.6)
                A = T.arc_band(r, 0.06 * (1 - u) + 0.015, -0.9, 0.9, cx=-1.1, cy=0.0, crescente=True)
                G += (A * 1.3 + T.blur(A, 0.03) * 0.5) * (1 - u)
                H += A * (1 - u) * 0.5
    rivais = [(-0.55, -0.1), (0.0, -0.15), (0.55, -0.1)]
    preso = pulso(t, 0.3, 1.0)
    if preso > 0:
        for k, (x, y) in enumerate(rivais):
            tr = 0.006 * math.sin(t * 70 + k)
            corpo, linhas = _silhueta(x + tr, y, 0.8)
            G += T.lines(linhas, 0.01) * preso * 1.2
            H += T.lines(linhas, 0.004) * preso * 0.6
            G += T.polys([(corpo, 1.0)]) * preso * 0.25
            G += T.lines([(x - 0.1, y - 0.19, x + 0.1, y - 0.15, 1.0), (x - 0.1, y - 0.15, x + 0.1, y - 0.19, 1.0)], 0.02) * preso * 1.4
    return G * env, H * env


# =================================================================== Venom
def _bocarra(T, cx, cy, s, abre, ang=0.0):
    """A boca do Venom: os lábios em arco e as fileiras de dentes compridos de cima e de baixo."""
    cima = [(cx + s * 0.5 * math.cos(a), cy - s * (0.08 + 0.35 * abre) * math.sin(a)) for a in np.linspace(0, math.pi, 20)]
    baixo = [(cx + s * 0.5 * math.cos(a), cy + s * (0.06 + 0.3 * abre) * math.sin(a)) for a in np.linspace(0, math.pi, 20)]
    lab = T.polyline(cima, 0.022 * s) + T.polyline(baixo, 0.022 * s)
    dentes = []
    for k in range(9):
        a = math.pi * (k + 0.5) / 9
        x = cx + s * 0.5 * math.cos(a) * 0.95
        y0 = cy - s * (0.08 + 0.35 * abre) * math.sin(a)
        y1 = cy + s * (0.06 + 0.3 * abre) * math.sin(a)
        L = s * (0.06 + 0.1 * math.sin(a))
        dentes.append((lamina(x, y0, x, y0 + L, 0.02 * s), 1.0))
        dentes.append((lamina(x, y1, x, y1 - L * 0.9, 0.02 * s), 1.0))
    return lab, T.polys(dentes)


def mordida_predatoria(T, t, rng):
    """A mordida predatória: a bocarra do simbionte se abre enorme sobre o rival (os dentes compridos e a língua
    balançando), fecha com força, a gosma preta pinga e o verde da cura volta para o Venom."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    abre = ease_out(rel(t, 0.0, 0.25), 2) * (1 - ease_in(rel(t, 0.3, 0.38), 2))
    if t < 0.55:
        some = 1 - rel(t, 0.45, 0.55)
        lab, dentes = _bocarra(T, 0.0, -0.05, 1.3, abre)
        G += (lab * 1.1 + dentes * 1.2) * some
        H += dentes * 0.4 * some
        if abre > 0.3:
            lin = [(0.05 * u + 0.1 * math.sin(u * 6 + t * 25) * u, -0.05 + 0.4 * u * abre) for u in np.linspace(0, 1, 16)]
            G += T.polyline(lin, 0.03) * some * abre
    fecha = rel(t, 0.36, 0.6)
    if 0 < fecha < 1:
        H += T.gauss(0, 0, 0.1) * (1 - fecha) ** 2 * 1.8
        G += T.ring(0.08 + 0.3 * ease_out(fecha, 3), 0.03, 0, 0) * (1 - fecha) * 1.2
    gosma = rel(t, 0.4, 0.95)
    if 0 < gosma < 1:
        q = np.random.default_rng(41)
        for k in range(7):
            x = q.uniform(-0.4, 0.4)
            y = -0.05 + 0.6 * gosma * gosma * q.uniform(0.5, 1)
            G += (T.gauss(x, y, 0.025) + T.lines([(x, y - 0.12 * gosma, x, y, 1.0)], 0.01)) * (1 - gosma) * 0.9
    cura = rel(t, 0.55, 0.95)
    if 0 < cura < 1:
        pts = [(-0.05 - 0.75 * min(1, cura * 1.3 - u * 0.3), -0.1 * math.sin(math.pi * u) - 0.05, (1 - u) * (1 - cura)) for u in np.linspace(0, 1, 12)]
        H += T.splats(pts, 0.02) * 1.3
    return G * env, H * env


def _olho_venom(cx, cy, s, lado):
    """O olho branco pontudo do Venom (a gota curva virada para fora)."""
    cima = [(cx + lado * 0.2 * s * u, cy - 0.05 * s - 0.1 * s * math.sin(math.pi * u * 0.8) * (1 - 0.3 * u)) for u in np.linspace(0, 1, 10)]
    baixo = [(cx + lado * 0.2 * s * u, cy - 0.05 * s + 0.13 * s * math.sin(math.pi * (1 - u)) * (1 - u) ** 0.5) for u in np.linspace(1, 0, 10)]
    return cima + baixo


def venom_preparo(T, t, rng):
    """O Preparo do Simbionte faminto: a gosma preta borbulhando (as bolhas que crescem e estouram), os dois olhos
    brancos pontudos abrindo e os fios se esticando em volta (laço)."""
    G, H = vazio(T)
    q = np.random.default_rng(51)
    for k in range(10):
        f = (t * q.uniform(0.8, 1.5) + q.uniform(0, 1)) % 1
        x, y = q.uniform(-0.45, 0.45), q.uniform(0.0, 0.4)
        G += T.ring(0.02 + 0.06 * f, 0.01, x, y) * (1 - f) * 1.1
    abre = 0.75 + 0.25 * math.sin(TAU * t)
    for lado in (-1, 1):
        O = T.polys([(_olho_venom(0.04 * lado, -0.2, 1.3 * abre, lado), 1.0)])
        G += O * 1.2
        H += O * 0.7
    for k in range(6):
        a = TAU * k / 6 + t * 2
        pts = [(0.45 * u * math.cos(a) + 0.05 * math.sin(u * 8 + t * 10), 0.1 + 0.35 * u * math.sin(a)) for u in np.linspace(0.3, 1, 12)]
        G += T.polyline(pts, 0.014) * (0.6 + 0.4 * math.sin(TAU * t + k))
    return G, H


def simbionte_faminto(T, t, rng):
    """O simbionte faminto: a massa do simbionte explode em tentáculos de todos os lados, eles se fecham e engolem o
    rival, e a aranha branca do peito pisca no meio."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    vem = ease_out(rel(t, 0.0, 0.35), 2.2)
    fecha = ease_in(rel(t, 0.35, 0.55), 2)
    if vem > 0 and t < 0.75:
        some = 1 - rel(t, 0.62, 0.75)
        for k in range(10):
            a = TAU * k / 10 + 0.2
            R = 0.95 - 0.55 * vem - 0.3 * fecha
            pts = []
            for j in range(18):
                u = j / 17
                r = R + (1.2 - R) * u
                pts.append((r * math.cos(a + 0.4 * math.sin(u * 4 + t * 12 + k)), r * math.sin(a + 0.4 * math.sin(u * 4 + t * 12 + k)) * 0.8))
            Tn = T.polyline(pts, 0.05 * (1 - 0.5 * fecha))
            G += (Tn * 0.25 + _borda(T, Tn, 0.008) * 1.3) * some
    engole = rel(t, 0.5, 0.95)
    if 0 < engole < 1:
        b = math.sin(math.pi * engole)
        G += T.gauss(0, 0, 0.22) * b * 0.5 + T.ring(0.25, 0.03, 0, 0) * b * 1.0
        aranha = [(0, -0.12, 0, 0.12, 1.0)]
        for lado in (-1, 1):
            aranha += [(0, -0.04, lado * 0.16, -0.14, 1.0), (lado * 0.16, -0.14, lado * 0.2, -0.04, 1.0), (0, 0.02, lado * 0.18, 0.12, 1.0), (lado * 0.18, 0.12, lado * 0.22, 0.22, 1.0)]
        A = T.lines(aranha, 0.02)
        pisca = 0.5 + 0.5 * math.cos(t * 40)
        G += A * b * 1.3
        H += A * b * pisca * 0.9
    return G * env, H * env


# =================================================================== Carnificina
def _chicote(T, x0, y0, x1, y1, curva, prog, larg=0.03, seed=0):
    pts = []
    for j in range(24):
        u = j / 23 * prog
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u + curva * math.sin(math.pi * u)
        pts.append((x, y))
    return T.polyline(pts, larg)


def ferida_aberta(T, t, rng):
    """A ferida aberta: dois chicotes vermelhos de simbionte cortam em X sobre o rival, a ferida abre (o rasgo
    claro com as bordas) e o sangue espirra; a marca aparece em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    for k, (x0, y0, x1, y1, cv, t0) in enumerate(((-0.9, -0.5, 0.45, 0.4, -0.2, 0.05), (-0.9, 0.5, 0.45, -0.4, 0.2, 0.15))):
        p = ease_out(rel(t, t0, t0 + 0.12), 2.5)
        some = 1 - rel(t, t0 + 0.15, t0 + 0.35)
        if p > 0 and some > 0:
            C = _chicote(T, x0, y0, x1, y1, cv, p, 0.03)
            G += (C * 0.5 + _borda(T, C, 0.006) * 1.3) * some
            for j in range(4):
                u = 0.3 + 0.17 * j
                if u < p:
                    x = x0 + (x1 - x0) * u
                    y = y0 + (y1 - y0) * u + cv * math.sin(math.pi * u)
                    G += T.lines([(x, y, x + 0.04, y - 0.05, 1.0)], 0.008) * some
    ferida = pulso(t, 0.25, 0.85)
    if ferida > 0:
        for (x1, y1, x2, y2) in ((-0.18, -0.15, 0.18, 0.15), (-0.18, 0.15, 0.18, -0.15)):
            L = T.polys([(lamina(x1, y1, x2, y2, 0.03), 1.0)])
            G += L * ferida * 1.2
            H += L * ferida * 0.7
    q = np.random.default_rng(61)
    u = rel(t, 0.25, 0.7)
    if 0 < u < 1:
        pts = []
        for _ in range(26):
            a = q.uniform(0, TAU)
            d = q.uniform(0.1, 0.5) * ease_out(u, 2)
            pts.append((d * math.cos(a), d * math.sin(a) + 0.3 * u * u, (1 - u) * q.uniform(0.5, 1)))
        G += T.splats(pts, 0.018)
    marca = pulso(t, 0.55, 1.0)
    if marca > 0:
        G += T.ring(0.32, 0.012, 0, 0) * marca + T.lines([(0.32, 0, 0.42, 0, 1.0), (-0.32, 0, -0.42, 0, 1.0), (0, 0.32, 0, 0.42, 1.0), (0, -0.32, 0, -0.42, 1.0)], 0.012) * marca
    return G * env, H * env


def carnificina_preparo(T, t, rng):
    """O Preparo da Carnificina total: os tentáculos vermelhos se debatendo em espiral em volta e virando lâminas nas
    pontas, com as gotas voando (laço)."""
    G, H = vazio(T)
    for k in range(7):
        a0 = TAU * k / 7 + t * TAU * 0.5
        pts = []
        for j in range(16):
            u = j / 15
            a = a0 + 1.5 * u + 0.3 * math.sin(TAU * t * 2 + k + u * 4)
            r = 0.1 + 0.5 * u
            pts.append((r * math.cos(a), r * math.sin(a) * 0.85))
        G += T.polyline(pts, 0.025) * 0.9
        a = a0 + 1.5 + 0.3 * math.sin(TAU * t * 2 + k + 4)
        tx, ty = 0.6 * math.cos(a), 0.6 * math.sin(a) * 0.85
        P = T.polys([(lamina(tx, ty, tx + 0.16 * math.cos(a + 1.3), ty + 0.16 * math.sin(a + 1.3), 0.03), 1.0)])
        G += P * 1.2
        H += P * 0.5
    H += T.gauss(0, 0, 0.1) * 0.4
    return G, H


def carnificina_total(T, t, rng):
    """A carnificina total: as lâminas e os machados vermelhos vêm de todos os lados um atrás do outro, os cortes se
    cruzam no rival em leque e o sangue espirra para todo lado."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = np.random.default_rng(71)
    for k in range(9):
        t0 = 0.04 + 0.05 * k
        a = q.uniform(0, TAU)
        x1, y1 = 0.8 * math.cos(a), 0.7 * math.sin(a)
        x2, y2 = -0.35 * math.cos(a + q.uniform(-0.4, 0.4)), -0.35 * math.sin(a + q.uniform(-0.4, 0.4))
        p = ease_out(rel(t, t0, t0 + 0.08), 3)
        ini = rel(t, t0 + 0.1, t0 + 0.28)
        if p > 0 and ini < 1:
            L = T.polys([(lamina(x1, y1, x2, y2, 0.035, prog=p, inicio=ini), 1.0)])
            G += L * 1.3
            H += L * 0.5
            if k % 3 == 0 and p < 1:
                hx, hy = x1 + (x2 - x1) * p, y1 + (y2 - y1) * p
                ma = _gira([(-0.02, -0.08), (0.08, -0.06), (0.1, 0.02), (0.02, 0.06), (-0.02, 0.0)], a + t * 30, hx, hy)
                M = T.polys([(ma, 1.0)])
                G += M * 0.6 + _borda(T, M, 0.006) * 1.3
    u = rel(t, 0.2, 0.9)
    if 0 < u < 1:
        pts = []
        for _ in range(45):
            a = q.uniform(0, TAU)
            d = q.uniform(0.1, 0.75) * ease_out(u, 2)
            pts.append((d * math.cos(a), d * math.sin(a) * 0.8 + 0.4 * u * u, (1 - u) * q.uniform(0.5, 1)))
        G += T.splats(pts, 0.02)
    H += T.gauss(0, 0, 0.12) * pulso(t, 0.15, 0.6) * 1.2
    return G * env, H * env


# =================================================================== Doutor Destino
def _mascara(T, cx, cy, s):
    """A máscara de ferro do Destino: o contorno, as frestas dos olhos, o nariz e a grade da boca."""
    rosto = [(cx - 0.17 * s, cy - 0.22 * s), (cx + 0.17 * s, cy - 0.22 * s), (cx + 0.2 * s, cy + 0.05 * s), (cx + 0.12 * s, cy + 0.26 * s), (cx - 0.12 * s, cy + 0.26 * s), (cx - 0.2 * s, cy + 0.05 * s)]
    linhas = _contorno(rosto)
    linhas += [(cx - 0.13 * s, cy - 0.07 * s, cx - 0.04 * s, cy - 0.05 * s, 1.0), (cx + 0.13 * s, cy - 0.07 * s, cx + 0.04 * s, cy - 0.05 * s, 1.0)]
    linhas += [(cx, cy - 0.04 * s, cx, cy + 0.08 * s, 0.7)]
    for k in range(5):
        x = cx + (-0.08 + 0.04 * k) * s
        linhas.append((x, cy + 0.13 * s, x, cy + 0.2 * s, 0.8))
    linhas.append((cx - 0.1 * s, cy + 0.13 * s, cx + 0.1 * s, cy + 0.13 * s, 0.8))
    return T.lines(linhas, 0.012 * s), [(cx - 0.085 * s, cy - 0.06 * s), (cx + 0.085 * s, cy - 0.06 * s)]


def _escudo_verde(T, t, t0, t1, cx, cy, r):
    u = pulso(t, t0, t1)
    if u <= 0:
        return T.zero(), T.zero()
    hexs = []
    for k in range(6):
        a = TAU * k / 6
        hx, hy = cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a)
        hexs += _contorno([(hx + r * 0.32 * math.cos(b), hy + r * 0.32 * math.sin(b)) for b in np.linspace(0, TAU, 6, endpoint=False)])
    return T.ring(r, 0.02, cx, cy) * u * 1.2 + T.lines(hexs, 0.007) * u, T.ring(r, 0.008, cx, cy) * u * 0.6


def armadura_de_doom(T, t, rng):
    """A armadura de Doom: a grade verde de análise varre o rival de cima a baixo, a mira trava, a manopla dispara o
    raio verde e o escudo de hexágonos fecha em volta do Destino."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    varre = rel(t, 0.0, 0.3)
    if 0 < varre < 1 or t < 0.45:
        b = 1 - rel(t, 0.35, 0.45)
        linhas = [(-0.42 + 0.12 * k, -0.48, -0.42 + 0.12 * k, 0.48, 0.5) for k in range(8)] + [(-0.42, -0.48 + 0.12 * k, 0.42, -0.48 + 0.12 * k, 0.5) for k in range(9)]
        G += T.lines(linhas, 0.005) * b * 0.8
        y = -0.48 + 0.96 * min(1, varre)
        G += T.lines([(-0.48, y, 0.48, y, 1.0)], 0.018) * b * 1.3
        H += T.lines([(-0.48, y, 0.48, y, 1.0)], 0.006) * b
    trava = pulso(t, 0.25, 0.5)
    if trava > 0:
        s = 0.25 - 0.08 * rel(t, 0.25, 0.35)
        for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            G += T.lines([(sx * s, sy * s, sx * s - sx * 0.08, sy * s, 1.0), (sx * s, sy * s, sx * s, sy * s - sy * 0.08, 1.0)], 0.014) * trava * 1.3
    raio = pulso(t, 0.38, 0.62)
    if raio > 0:
        R = T.lines([(-0.85, 0.05, 0.0, 0.0, 1.0)], 0.04)
        G += (R * 0.9 + T.blur(R, 0.03) * 0.6) * raio
        H += T.lines([(-0.85, 0.05, 0.0, 0.0, 1.0)], 0.012) * raio * 1.3 + T.gauss(0, 0, 0.08) * raio * 1.4
    g, h = _escudo_verde(T, t, 0.55, 1.0, -0.72, 0.05, 0.25)
    G += g
    H += h
    return G * env, H * env


def _circulo_runico(T, cx, cy, r, giro, sq=0.35):
    G = T.ring(r, 0.014, cx, cy, squash=1 / sq) + T.ring(r * 0.78, 0.01, cx, cy, squash=1 / sq)
    linhas = []
    for k in range(5):
        a1 = giro + TAU * k / 5
        a2 = giro + TAU * (k + 2) / 5
        linhas.append((cx + r * 0.78 * math.cos(a1), cy + r * 0.78 * sq * math.sin(a1), cx + r * 0.78 * math.cos(a2), cy + r * 0.78 * sq * math.sin(a2), 1.0))
    for k in range(12):
        a = -giro * 1.5 + TAU * k / 12
        x, y = cx + r * 0.89 * math.cos(a), cy + r * 0.89 * sq * math.sin(a)
        s = 0.022
        linhas += [(x - s, y, x + s, y, 0.8), (x, y - s * 0.6, x + s * 0.5, y + s * 0.6, 0.8)]
    return G + T.lines(linhas, 0.008)


def ritual_latveriano(T, t, rng):
    """O ritual latveriano: o círculo místico verde com o pentagrama e as runas gira sob o rival, os raios verdes
    sobem dele e prendem o rival (Paralisado), e o escudo verde fecha em volta do Destino."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2.5)
    b = 1 - rel(t, 0.75, 0.9)
    if abre > 0:
        G += _circulo_runico(T, 0, 0.35, 0.55 * abre, t * 3) * b * 1.2
        H += T.gauss(0, 0.35, 0.15 * abre, 0.05) * b * 0.8
    q = np.random.default_rng(int(t * 22) % 8 + 81)
    sobe = pulso(t, 0.3, 0.8)
    if sobe > 0:
        for k in range(5):
            a = TAU * k / 5 + t * 3
            x0, y0 = 0.45 * math.cos(a), 0.35 + 0.16 * math.sin(a)
            R = T.polyline(jagged(q, x0, y0, 0.03 * math.cos(a), -0.1, 4, 0.25), 0.012)
            G += (R * 1.3 + T.blur(R, 0.02) * 0.6) * sobe
            H += R * 0.6 * sobe
        H += T.gauss(0, -0.05, 0.1) * sobe * 0.9
    g, h = _escudo_verde(T, t, 0.55, 1.0, -0.72, 0.05, 0.25)
    G += g
    H += h
    return G * env, H * env


def destino_preparo(T, t, rng):
    """O Preparo do Plano de contingência: a máscara de ferro com os olhos acesos e a energia mística verde girando
    em volta em dois anéis de runas (laço)."""
    G, H = vazio(T)
    M, olhos = _mascara(T, 0, -0.05, 1.5)
    G += M * 1.1
    pis = 0.7 + 0.3 * math.sin(TAU * t * 2)
    H += T.splats([(x, y, 1.0) for x, y in olhos], 0.02) * 1.6 * pis
    G += _circulo_runico(T, 0, -0.02, 0.62, TAU * t, 0.9) * 0.9
    for k in range(3):
        a = TAU * t + TAU * k / 3
        H += T.gauss(0.62 * math.cos(a), -0.02 + 0.56 * math.sin(a), 0.035) * 1.2
    return G, H


def plano_de_contingencia(T, t, rng):
    """O plano de contingência: tecnologia e magia ao mesmo tempo — os lasers caem do alto cruzados em grade
    enquanto o círculo místico gira no chão sob os rivais, e tudo explode junto numa onda verde."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2.5)
    b = 1 - rel(t, 0.55, 0.7)
    if abre > 0:
        G += _circulo_runico(T, 0, 0.4, 0.85 * abre, t * 2.5, 0.3) * b * 1.1
    for k in range(6):
        t0 = 0.12 + 0.04 * k
        u = rel(t, t0, t0 + 0.12)
        some = 1 - rel(t, t0 + 0.15, t0 + 0.3)
        if u > 0 and some > 0:
            x0 = -0.9 + 0.36 * k
            x1 = 0.6 - 0.24 * k
            y1 = -0.9 + 1.3 * ease_in(min(1, u), 1.5)
            R = T.lines([(x0, -0.9, x0 + (x1 - x0) * min(1, u), y1, 1.0)], 0.03)
            G += (R * 1.0 + T.blur(R, 0.025) * 0.6) * some
            H += T.lines([(x0, -0.9, x0 + (x1 - x0) * min(1, u), y1, 1.0)], 0.009) * some * 1.3
    bum = rel(t, 0.42, 0.95)
    if 0 < bum < 1:
        e = ease_out(bum, 3)
        G += T.ring(0.1 + 1.0 * e, 0.05, 0, 0.3, squash=1.8) * (1 - bum) * 1.4
        H += T.gauss(0, 0.2, 0.15 + 0.3 * e, 0.1 + 0.15 * e) * (1 - bum) ** 2 * 2.2
        q = np.random.default_rng(91)
        raios = [(0.0, 0.25, (0.3 + 0.8 * e) * math.cos(a), 0.25 + (0.2 + 0.5 * e) * math.sin(a), 1 - bum) for a in q.uniform(-math.pi, 0, 14)]
        G += T.tapered(raios, 0.03) * 1.1
    return G * env, H * env


# =================================================================== Loki
def troca_de_lugar(T, t, rng):
    """A troca de lugar: o Loki e o rival viram silhuetas verdes, trocam de lugar girando num redemoinho de fumaça
    verde com as faíscas douradas, e a mira do rival se perde (a cruz que treme e escorrega)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = ease_in(rel(t, 0.1, 0.5), 1.8)
    vis = pulso(t, 0.0, 0.75)
    if vis > 0:
        for k, (x0, x1, ch) in enumerate(((-0.6, 0.15, True), (0.15, -0.6, False))):
            x = x0 + (x1 - x0) * u
            y = -0.25 * math.sin(math.pi * u) * (1 if k == 0 else -1)
            corpo, linhas = _silhueta(x, y, 0.6, ch)
            G += T.lines(linhas, 0.011) * vis * 1.2
            G += T.polys([(corpo, 1.0)]) * vis * 0.2
    fumo = pulso(t, 0.1, 0.65)
    if fumo > 0:
        q = np.random.default_rng(101)
        pts = []
        for k in range(30):
            a = q.uniform(0, TAU) + t * 8
            r = q.uniform(0.1, 0.45)
            pts.append((-0.22 + r * math.cos(a), r * math.sin(a) * 0.5, q.uniform(0.4, 1)))
        G += T.splats(pts, 0.045) * fumo * 0.5
        H += T.splats([(-0.22 + 0.4 * math.cos(q.uniform(0, TAU) + t * 12), 0.2 * math.sin(q.uniform(0, TAU) + t * 12), 1.0) for _ in range(12)], 0.012) * fumo * 1.4
    mira = pulso(t, 0.45, 1.0)
    if mira > 0:
        mx = 0.3 + 0.25 * rel(t, 0.5, 0.9) + 0.02 * math.sin(t * 50)
        my = -0.2 + 0.1 * rel(t, 0.5, 0.9)
        G += T.ring(0.08, 0.01, mx, my) * mira + T.lines([(mx - 0.12, my, mx + 0.12, my, 1.0), (mx, my - 0.12, mx, my + 0.12, 1.0)], 0.008) * mira
    return G * env, H * env


def _elmo(T, cx, cy, s):
    """O elmo dourado do Loki com os dois chifres compridos curvos."""
    linhas = _contorno([(cx - 0.1 * s, cy + 0.05 * s), (cx - 0.12 * s, cy - 0.1 * s), (cx, cy - 0.16 * s), (cx + 0.12 * s, cy - 0.1 * s), (cx + 0.1 * s, cy + 0.05 * s)])
    chifres = []
    for lado in (-1, 1):
        fio = [(cx + lado * (0.09 + 0.3 * math.sin(math.pi * u * 0.78)) * s, cy - (0.08 + 0.62 * u) * s) for u in np.linspace(0, 1, 16)]
        borda_a = [(x + lado * 0.035 * s * (1 - j / 15), y) for j, (x, y) in enumerate(fio)]
        borda_b = [(x - lado * 0.035 * s * (1 - j / 15), y) for j, (x, y) in enumerate(fio)]
        chifres.append((borda_a + list(reversed(borda_b)), 1.0))
    C = T.polys(chifres)
    return T.lines(linhas, 0.016 * s) + C * 0.5 + _borda(T, C, 0.006) * 1.2


def loki_preparo(T, t, rng):
    """O Preparo do Engano perfeito: o elmo de chifres dourado brilha no alto e as cópias de ilusão do Loki piscam
    em volta, uma de cada vez (laço)."""
    G, H = vazio(T)
    E = _elmo(T, 0, -0.25, 1.4)
    G += E * 1.1
    H += E * 0.6 * (0.6 + 0.4 * math.sin(TAU * t * 2))
    for k in range(4):
        a = TAU * k / 4 + TAU * t / 4
        x, y = 0.55 * math.cos(a), 0.15 + 0.25 * math.sin(a)
        pisca = max(0.0, math.sin(TAU * (t * 2 + k / 4)))
        corpo, linhas = _silhueta(x, y, 0.4, True)
        G += T.lines(linhas, 0.008) * pisca * 1.1
    return G, H


def engano_perfeito(T, t, rng):
    """O engano perfeito: as cópias do Loki cercam o rival, quebram como vidro uma a uma, e o verdadeiro aparece por
    trás e crava a adaga dourada."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    copias = [(-0.45, 0.0), (-0.2, -0.3), (0.25, -0.3), (0.45, 0.0)]
    for k, (x, y) in enumerate(copias):
        aparece = ease_out(rel(t, 0.02 * k, 0.15 + 0.02 * k), 2)
        quebra = rel(t, 0.25 + 0.06 * k, 0.5 + 0.06 * k)
        if aparece > 0 and quebra <= 0:
            corpo, linhas = _silhueta(x, y, 0.45, True)
            G += T.lines(linhas, 0.009) * aparece * 1.1 + T.polys([(corpo, 1.0)]) * aparece * 0.15
        elif 0 < quebra < 1:
            q = np.random.default_rng(111 + k)
            cacos = [(_gira([(-0.03, -0.02), (0.035, -0.01), (0.0, 0.03)], q.uniform(0, 6) + quebra * 6, x + q.uniform(-0.1, 0.1) * (1 + 3 * quebra), y + q.uniform(-0.2, 0.2) + 0.3 * quebra * quebra), 1 - quebra) for _ in range(9)]
            G += T.polys(cacos) * 1.1
            H += T.gauss(x, y, 0.05) * (1 - quebra) ** 2
    real = rel(t, 0.55, 0.7)
    if real > 0 and t < 0.9:
        b = 1 - rel(t, 0.8, 0.9)
        corpo, linhas = _silhueta(0.35, 0.15, 0.55, True)
        G += T.lines(linhas, 0.012) * b * 1.3
        p = ease_out(min(1, real), 3)
        L = T.polys([(lamina(0.25, 0.05, 0.25 - 0.25 * p, -0.02, 0.03), 1.0)])
        G += L * b * 1.3
        H += L * b * 0.8 + T.flare(0.0, -0.02, 0.4 * b, 0.4, 0.012) * pulso(t, 0.62, 0.85)
    return G * env, H * env


REGISTRO = [
    ("coordenacao_mental", coordenacao_mental, GRANDE, "Professor Xavier · as ondas e os fios ligando o trio", False),
    ("bloqueio_mental", bloqueio_mental, GRANDE, "Professor Xavier · os anéis psíquicos e a intenção quebrando", False),
    ("cerebro_preparo", cerebro_preparo, MEDIA, "Professor Xavier · o capacete do Cérebro (Preparo, laço)", True),
    ("paralisia_mental", paralisia_mental, GRANDE, "Professor Xavier · a onda e os rivais presos e calados", False),
    ("mordida_predatoria", mordida_predatoria, GRANDE, "Venom · a bocarra, a gosma e a cura", False),
    ("venom_preparo", venom_preparo, MEDIA, "Venom · a gosma e os olhos brancos (Preparo, laço)", True),
    ("simbionte_faminto", simbionte_faminto, GRANDE, "Venom · os tentáculos engolindo e a aranha", False),
    ("ferida_aberta", ferida_aberta, GRANDE, "Carnificina · os chicotes em X e a ferida", False),
    ("carnificina_preparo", carnificina_preparo, MEDIA, "Carnificina · os tentáculos-lâmina (Preparo, laço)", True),
    ("carnificina_total", carnificina_total, GRANDE, "Carnificina · as lâminas e os machados de todo lado", False),
    ("armadura_de_doom", armadura_de_doom, GRANDE, "Doutor Destino · a grade, a mira e o raio", False),
    ("ritual_latveriano", ritual_latveriano, GRANDE, "Doutor Destino · o círculo místico e os raios verdes", False),
    ("destino_preparo", destino_preparo, MEDIA, "Doutor Destino · a máscara e as runas (Preparo, laço)", True),
    ("plano_de_contingencia", plano_de_contingencia, GRANDE, "Doutor Destino · os lasers e o círculo explodindo", False),
    ("troca_de_lugar", troca_de_lugar, GRANDE, "Loki · as silhuetas trocando e a mira perdida", False),
    ("loki_preparo", loki_preparo, MEDIA, "Loki · o elmo e as cópias (Preparo, laço)", True),
    ("engano_perfeito", engano_perfeito, GRANDE, "Loki · as cópias quebrando e a adaga", False),
]
