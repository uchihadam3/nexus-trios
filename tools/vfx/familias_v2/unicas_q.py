"""Rodada 16 das Mecânicas únicas ativando como habilidade: Magneto, Ravena, Itachi, Sakura, Mikasa, Levi, Homem-Formiga,
Demolidor, Tempestade, Professor X, Senhor das Estrelas, Aquaman, Zelda, 2B, Alucard, Shun, Saga, Shaka, Gaara,
Darkseid, Spawn e Leonardo.

- polaridade: as linhas do campo magnético entre os dois polos, puxando ou empurrando os pedaços de metal.
- empatia: o corvo escuro de alma se abre e a luz da cura passa de um lado ao outro.
- doenca_terminal: a tosse de sangue (as gotas) e os corvos que se desfazem.
- medica_de_campo: a mão verde da cura e o losango de proteção.
- ninguem_toca: as duas lâminas do equipamento cruzam e o cabo do gancho.
- corte_na_nuca: o giro rapidíssimo (o redemoinho de cortes) e o corte na nuca.
- particulas_pym: as partículas vermelhas e o homem encolhendo ou crescendo (os anéis).
- sentido_radar: as ondas de som em anéis mostrando o rival no escuro.
- tempestade_pula: o raio pulando de um ponto para o outro entre as nuvens.
- cerebro: o capacete Cérebro e as ondas mentais.
- doze_por_cento: o walkman e o plano rabiscado, com a seta do "12%".
- mares: a onda subindo e descendo com o tridente.
- selo_da_luz: a Triforce dourada e o selo que bloqueia.
- pod_042: o Pod flutuando e o tiro de laser.
- familiar: a espada familiar girando e o morcego.
- corrente_intercepta: a corrente de Andrômeda em espiral defendendo.
- dois_lados: a máscara metade clara, metade escura.
- rendicao_sentidos: a flor de lótus e os sentidos se apagando (os orbes).
- areia: a areia girando em volta e virando escudo.
- sem_esperanca: os olhos vermelhos de Darkseid e a cura que se apaga.
- necroplasma: as correntes verdes e a capa esvoaçando.
- trio_unido: as três espadas/armas juntas num círculo.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, jagged, pulso, rel, vazio
from .unicas_kit import (ASA, CRUZ, ESPADA, GOTA, NOTA, SETA, anel, aura, cheio, clarao, converge, corte, estouro, flor, icone, particulas, poe,
                         runas, surge)


def _espiral(cx, cy, r0, r1, voltas, fase, n=40):
    return [(cx + (r0 + (r1 - r0) * u) * math.cos(fase + TAU * voltas * u), cy + (r0 + (r1 - r0) * u) * math.sin(fase + TAU * voltas * u)) for u in np.linspace(0, 1, n)]


def _quad(cx, cy, s, ang=0.0):
    return poe([(-1, -1), (1, -1), (1, 1), (-1, 1)], cx, cy, s, ang)


def polaridade(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        g, h = cheio(T, poe(circulo_pts(), lado * 0.55, -0.05, 0.1 * s, 0), 1.3 * s)
        G, H = G + g, H + h
    for j in range(5):
        k = (j - 2) * 0.12
        linha = [(-0.55 + 1.1 * v, -0.05 + k * 4 * math.sin(math.pi * v) * s) for v in np.linspace(0, 1, 24)]
        G += T.polyline(linha, 0.012) * 0.9 * s
    q = np.random.default_rng(4)
    for j in range(8):
        u = rel(t, 0.25, 0.95)
        x0, y0 = q.uniform(-0.9, 0.9), q.uniform(-0.6, 0.4)
        x, y = x0 * (1 - 0.6 * ease_in(u)), y0 * (1 - 0.6 * ease_in(u))
        g, h = icone(T, _quad(x, y, 0.035, u * 5 + j), (1 - rel(t, 0.85, 1)) * 1.1, 0.6)
        G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.0, 0.25, 0, -0.05, 0.6)
    return (G + g2) * env, (H + h2) * env


def circulo_pts(n=24):
    return [(math.cos(TAU * k / n), math.sin(TAU * k / n)) for k in range(n)]


def empatia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.35), 2) * (1 - rel(t, 0.85, 1))
    for lado in (-1, 1):
        asa = [(lado * x * 0.75 * s, -0.1 + y * 0.6 * s) for x, y in ASA]
        g, h = icone(T, asa, 0.9, 0.45)
        G, H = G + g, H + h
    G += T.gauss(0, -0.2, 0.05 * s + 0.001) * 1.2
    u = rel(t, 0.3, 0.85)
    if 0 < u < 1:
        x = -0.6 + 1.2 * ease_in(u)
        G += T.gauss(x, 0.15, 0.06) * 1.3
        H += T.gauss(x, 0.15, 0.03) * 1.6
        G += T.tapered([(x - 0.3, 0.15, x, 0.15, 0.6)], 0.04)
    g2, h2 = clarao(T, t, 0.75, 0.95, 0.6, 0.15, 0.5)
    return (G + g2) * env, (H + h2) * env


def doenca_terminal(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(3)
    for j in range(6):
        u = rel(t, 0.05 + 0.04 * j, 0.6 + 0.04 * j)
        if 0 < u < 1:
            x = q.uniform(-0.15, 0.15)
            g, h = cheio(T, poe(GOTA, x, -0.1 + 0.6 * ease_in(u), 0.08), (1 - u) * 1.4)
            G, H = G + g, H + h
    for j in range(5):
        u = rel(t, 0.25 + 0.06 * j, 0.95)
        if 0 < u < 1:
            a = -math.pi / 2 + (j - 2) * 0.5
            d = 0.2 + 0.7 * ease_out(u)
            x, y = d * math.cos(a), -0.1 + d * math.sin(a)
            bate = 0.4 * math.sin(t * 30 + j)
            corvo = [(x - 0.2, y - 0.06 * bate), (x - 0.06, y), (x, y - 0.06), (x + 0.06, y), (x + 0.2, y - 0.06 * bate), (x, y + 0.08)]
            g, h = cheio(T, corvo, (1 - u) * 1.3)
            G, H = G + g, H + h
            pts = [(x + q.normal(0, 0.05) * u, y + q.normal(0, 0.05) * u, (1 - u) * 0.6) for _ in range(6)]
            G += T.splats(pts, 0.012)
    return G * env, H * env


def medica_de_campo(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        mao = [(-0.12, 0.25), (-0.15, -0.05), (-0.12, -0.25), (-0.07, -0.05), (-0.05, -0.32), (0.0, -0.05), (0.03, -0.3), (0.06, -0.05),
               (0.11, -0.25), (0.12, 0.0), (0.2, -0.1), (0.15, 0.1), (0.1, 0.25)]
        g, h = icone(T, [(x * 1.4 * s, y * 1.4 * s + 0.05) for x, y in mao], 1.0, 0.45)
        G, H = G + g, H + h
    g2, h2 = aura(T, t, 0.15, 0.9, 0.35, 0.0, 1.0)
    G, H = G + g2, H + h2
    d = surge(t, 0.4, 0.65) * (1 - rel(t, 0.88, 1))
    if d > 0:
        G += T.polyline([(0, -0.55 * d), (0.45 * d, 0), (0, 0.55 * d), (-0.45 * d, 0), (0, -0.55 * d)], 0.03) * 1.3
    G += particulas(T, t, 0.2, 1.0, 30, 6, 0, 0, 0.5, 0.4, 0.013)
    return G * env, H * env


def ninguem_toca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.3), 2)
    cabo = 1 - rel(t, 0.3, 0.45)
    if cabo > 0:
        G += T.lines([(-0.9, -0.6, -0.9 + 0.9 * u, -0.6 + 0.6 * u, 1.0)], 0.016) * 1.4 * cabo
        H += T.gauss(-0.9 + 0.9 * u, -0.6 + 0.6 * u, 0.03) * 1.5 * cabo
    g, h = corte(T, t, 0.25, 0.6, 0.7, 1.5, 0.08, 0.1, 0.0)
    G, H = G + g, H + h
    g, h = corte(T, t, 0.32, 0.67, -0.7, 1.5, 0.08, 0.1, 0.0)
    G, H = G + g, H + h
    g2, h2 = clarao(T, t, 0.38, 0.55, 0.1, 0.0, 0.7)
    return (G + g2) * env, (H + h2) * env


def corte_na_nuca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    giro = rel(t, 0.0, 0.5)
    if 0 < giro < 1:
        for j in range(5):
            a0 = giro * TAU * 2 + j * TAU / 5
            G += T.arc_band(0.35 + 0.08 * j, 0.035, a0, a0 + 1.6, 0.5, 0, 0, 0, 1.0) * (1 - giro) * 2.0
    g, h = corte(T, t, 0.4, 0.75, -0.15, 1.6, 0.09, 0.0, -0.3)
    G, H = G + g * 1.3, H + h
    g2, h2 = clarao(T, t, 0.48, 0.65, 0.0, -0.3, 0.6)
    return (G + g2) * env, (H + h2) * env


def particulas_pym(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(4):
        G += anel(T, t, 0.05 + 0.1 * j, 0.6 + 0.08 * j, 0.6 - 0.12 * j, 0.05, 0.03, 0.0)
    G += converge(T, t, 0.0, 0.5, 30, 8, 0, 0, 0.8, 0.012)
    G += estouro(T, t, 0.45, 0.85, 20, 9, 0, 0, 0.7, 0.012)
    g, h = clarao(T, t, 0.4, 0.6, 0, 0, 0.8)
    return (G + g) * env, (H + h) * env


def sentido_radar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    for j in range(5):
        G += anel(T, t, 0.05 + 0.13 * j, 0.6 + 0.08 * j, 0.05, 0.95, 0.018, 0.0, 1.0, 1.4)
    for j, (x, y) in enumerate([(-0.5, -0.3), (0.55, -0.15), (0.2, 0.4)]):
        k = pulso(t, 0.25 + 0.15 * j, 0.95)
        G += T.ring(0.08, 0.012, x, y) * k * 1.3
        H += T.gauss(x, y, 0.03) * k * 1.8
    return G * env, H * env


def tempestade_pula(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    nuvem = pulso(t, 0.0, 0.95)
    for j in range(5):
        G += T.gauss(-0.6 + 0.3 * j, -0.7, 0.12, 0.06) * 0.6 * nuvem
    pontos = [(0.0, -0.65), (-0.45, 0.1), (0.4, -0.05), (0.0, 0.4)]
    for j in range(3):
        k = pulso(t, 0.15 + 0.18 * j, 0.35 + 0.18 * j)
        if k > 0:
            q = np.random.default_rng(int(t * 30) + j)
            (x0, y0), (x1, y1) = pontos[j], pontos[j + 1]
            bolt = jagged(q, x0, y0, x1, y1, 5, 0.12)
            G += T.polyline(bolt, 0.03) * k * 1.4
            H += T.polyline(bolt, 0.01) * k * 1.4
            G += T.gauss(x1, y1, 0.1) * k
    return G * env, H * env


def cerebro(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.arc_band(0.25 * s, 0.05, math.pi, TAU, 1.0, 0, 0, -0.1, 1.0) * 1.2
        for j in range(5):
            a = math.pi + math.pi * (j + 0.5) / 5
            G += T.lines([(0.25 * s * math.cos(a), -0.1 + 0.25 * s * math.sin(a), 0.4 * s * math.cos(a), -0.1 + 0.4 * s * math.sin(a), 1.0)], 0.018) * 1.2
    for j in range(4):
        G += anel(T, t, 0.25 + 0.12 * j, 0.75 + 0.06 * j, 0.25, 0.85, 0.02, -0.1, 1.0, 1.0)
    g, h = aura(T, t, 0.2, 1.0, 0.3, -0.1, 0.7)
    return (G + g) * env, (H + h) * env


def doze_por_cento(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    if s > 0:
        g, h = icone(T, [(-0.25 * s, -0.15), (0.25 * s, -0.15), (0.25 * s, 0.15), (-0.25 * s, 0.15)], 1.1, 0.45)
        G, H = G + g, H + h
        for lado in (-1, 1):
            G += T.ring(0.06 * s, 0.012, lado * 0.12 * s, 0.0) * 1.3
    rab = ease_out(rel(t, 0.25, 0.65), 2)
    if rab > 0:
        pts = [(-0.4 + 0.8 * v, -0.45 + 0.05 * math.sin(v * 20)) for v in np.linspace(0, rab, 24)]
        G += T.polyline(pts, 0.012) * 1.2 * (1 - rel(t, 0.88, 1))
    u = rel(t, 0.55, 0.9)
    if 0 < u < 1:
        g2, h2 = cheio(T, poe(SETA, -0.2 + 0.8 * ease_out(u), 0.4 - 0.4 * u, 0.12, -0.5), (1 - rel(u, 0.85, 1)) * 1.4)
        G, H = G + g2, H + h2
    for j in range(3):
        k = pulso(t, 0.3 + 0.1 * j, 0.7 + 0.08 * j)
        g3, h3 = cheio(T, poe(NOTA, -0.5 + 0.2 * j, -0.3 - 0.1 * j, 0.06 * k), k * 1.2)
        G, H = G + g3, H + h3
    return G * env, H * env


def mares(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    nivel = math.sin(math.pi * rel(t, 0.0, 0.85))
    for j in range(3):
        y0 = 0.45 - 0.35 * nivel - 0.08 * j
        pts = [(-0.95 + 1.9 * v, y0 + 0.05 * math.sin(v * 12 + t * 10 + j)) for v in np.linspace(0, 1, 40)]
        G += T.polyline(pts, 0.02) * (1.2 - 0.3 * j) * (1 - rel(t, 0.88, 1))
    s = surge(t, 0.1, 0.4) * (1 - rel(t, 0.88, 1))
    if s > 0:
        G += T.lines([(0, 0.4, 0, -0.45 * s, 1.0)], 0.02) * 1.3
        for dx in (-0.1, 0, 0.1):
            G += T.lines([(dx * s, -0.45 * s + 0.12, dx * s, -0.45 * s - 0.05 + (0.04 if dx else 0), 1.0)], 0.02) * 1.3
        G += T.lines([(-0.1 * s, -0.45 * s + 0.12, 0.1 * s, -0.45 * s + 0.12, 1.0)], 0.02) * 1.3
    G += particulas(T, t, 0.2, 1.0, 30, 3, 0, 0.3, 0.8, 0.4, 0.013)
    return G * env, H * env


def selo_da_luz(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.88, 1))
    tri = [(0, -1), (0.577, 0), (-0.577, 0)]
    for cx, cy in ((0, -0.2), (-0.17, 0.1), (0.17, 0.1)):
        g, h = icone(T, poe(tri, cx * s * 1.3, cy * s * 1.3 + 0.05, 0.3 * s, 0), 1.2, 0.55)
        G, H = G + g, H + h
    G += anel(T, t, 0.35, 0.8, 0.3, 0.7, 0.03, 0.0)
    g2, h2 = runas(T, t, 0.35, 1.0, 0.55, 8, 0.0, 1.0, 1.5)
    g3, h3 = clarao(T, t, 0.3, 0.5, 0, 0, 0.7)
    return (G + g2 * 0.6 + g3) * env, (H + h2 + h3) * env


def pod_042(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    y = -0.35 + 0.03 * math.sin(t * 12)
    if s > 0:
        pod = [(-0.12, -0.08), (0.12, -0.08), (0.16, 0.0), (0.12, 0.12), (-0.12, 0.12), (-0.16, 0.0)]
        g, h = icone(T, [(x * 1.4 * s - 0.4, yy * 1.4 * s + y) for x, yy in pod], 1.1, 0.5)
        G, H = G + g, H + h
        H += T.gauss(-0.4 + 0.18 * s, y + 0.02, 0.02) * 2 * s
    laser = pulso(t, 0.35, 0.7)
    if laser > 0:
        G += T.lines([(-0.2, y + 0.02, 0.95, y + 0.3, 1.0)], 0.035) * laser * 1.3
        H += T.lines([(-0.2, y + 0.02, 0.95, y + 0.3, 1.0)], 0.01) * laser * 1.4
    g2, h2 = clarao(T, t, 0.4, 0.6, 0.75, y + 0.25, 0.5)
    return (G + g2) * env, (H + h2) * env


def familiar(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    for j in range(3):
        a = t * 8 + j * TAU / 3
        g, h = icone(T, poe(ESPADA, 0.45 * math.cos(a) * s, -0.05 + 0.3 * math.sin(a) * s, 0.28 * s, a + math.pi / 2), 1.1, 0.5)
        G, H = G + g, H + h
    u = rel(t, 0.4, 0.9)
    if 0 < u < 1:
        x = 0.9 * ease_out(u)
        bate = math.sin(t * 40)
        morcego = [(x - 0.22, -0.35 - 0.08 * bate), (x - 0.08, -0.27), (x, -0.32), (x + 0.08, -0.27), (x + 0.22, -0.35 - 0.08 * bate), (x, -0.18)]
        g2, h2 = cheio(T, morcego, (1 - rel(u, 0.85, 1)) * 1.3)
        G, H = G + g2, H + h2
    return G * env, H * env


def corrente_intercepta(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    u = ease_out(rel(t, 0.0, 0.5), 2)
    if u > 0:
        pts = _espiral(0, 0, 0.05, 0.6, 2.2 * u, t * 3, 60)
        for i in range(0, len(pts) - 1, 2):
            G += T.ring(0.025, 0.008, pts[i][0], pts[i][1], 0.6) * (1 - rel(t, 0.88, 1)) * 1.4
    g, h = clarao(T, t, 0.45, 0.65, 0.55, -0.05, 0.6)
    G, H = G + g, H + h
    G += estouro(T, t, 0.45, 0.8, 10, 4, 0.55, -0.05, 0.4, 0.012)
    return G * env, H * env


def dois_lados(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.35) * (1 - rel(t, 0.88, 1))
    if s > 0:
        rosto = [(0.28 * s * math.cos(a), -0.05 + 0.36 * s * math.sin(a)) for a in np.linspace(-math.pi / 2, math.pi / 2, 16)]
        g, h = cheio(T, [(0, -0.05 - 0.36 * s)] + rosto + [(0, 0.31 * s - 0.05)], 1.3)
        G, H = G + g, H + h * 1.5
        G += T.polyline([(-x, y) for x, y in rosto], 0.02) * 1.0
        G += T.gauss(-0.1 * s, -0.12, 0.035) * 1.6
        H += T.gauss(-0.1 * s, -0.12, 0.02) * 2.0
    g2, h2 = aura(T, t, 0.2, 1.0, 0.45, -0.05, 0.7)
    return (G + g2) * env, (H + h2) * env


def rendicao_sentidos(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    s = ease_out(rel(t, 0.0, 0.4), 2) * (1 - rel(t, 0.88, 1))
    g, h = icone(T, poe(flor(8, 1.0, 0.3), 0, 0.2, 0.3 * s, t * 0.8), 1.0, 0.4)
    G, H = G + g, H + h
    for j in range(5):
        a = -math.pi / 2 + TAU * j / 5
        apaga_j = rel(t, 0.4 + 0.08 * j, 0.6 + 0.08 * j)
        k = s * (1 - apaga_j)
        G += T.gauss(0.55 * math.cos(a), -0.05 + 0.4 * math.sin(a), 0.06) * k * 1.3
        H += T.gauss(0.55 * math.cos(a), -0.05 + 0.4 * math.sin(a), 0.025) * k * 1.6
    g2, h2 = aura(T, t, 0.1, 1.0, 0.35, 0.0, 0.7)
    return (G + g2) * env, (H + h2) * env


def areia(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    q = np.random.default_rng(12)
    junta = ease_out(rel(t, 0.0, 0.6), 2)
    pts = []
    for j in range(260):
        a = q.uniform(0, TAU) + t * (3 + q.uniform(0, 2))
        r0 = q.uniform(0.3, 0.95)
        r = r0 + (0.5 - r0) * junta
        pts.append((r * math.cos(a), -0.05 + r * 0.75 * math.sin(a), q.uniform(0.4, 1) * (1 - rel(t, 0.88, 1))))
    G += T.splats(pts, 0.012) * 1.3
    G += T.ring(0.5, 0.04, 0, -0.05, 0.75) * surge(t, 0.45, 0.75) * (1 - rel(t, 0.88, 1)) * 1.1
    return G * env, H * env


def sem_esperanca(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = surge(t, 0.0, 0.3) * (1 - rel(t, 0.88, 1))
    for lado in (-1, 1):
        G += T.gauss(lado * 0.14, -0.2, 0.07 * s + 0.001, 0.035 * s + 0.001) * 1.6
        H += T.gauss(lado * 0.14, -0.2, 0.025 * s + 0.001) * 2.5
    u = rel(t, 0.3, 0.75)
    if 0 < u < 1:
        for lado in (-1, 1):
            G += T.lines([(lado * 0.14, -0.2, lado * 0.14 + 0.8 * ease_out(u), -0.2 + 0.2 * u * lado, 1.0)], 0.025) * (1 - rel(u, 0.8, 1)) * 1.4
    cr = surge(t, 0.5, 0.7) * (1 - rel(t, 0.75, 0.95))
    if cr > 0:
        g, h = cheio(T, poe(CRUZ, 0.6, 0.15, 0.13 * cr, 0), cr)
        G, H = G + g, H + h
        G += T.lines([(0.45, 0.0, 0.75, 0.3, 1.0)], 0.03) * cr * 1.4
    return G * env, H * env


def necroplasma(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    s = ease_out(rel(t, 0.0, 0.5), 2) * (1 - rel(t, 0.88, 1))
    for j in range(4):
        a = -math.pi / 2 + (j - 1.5) * 0.7
        pts = []
        for v in np.linspace(0, s, 18):
            pts.append((0.85 * v * math.cos(a) + 0.06 * math.sin(v * 14 + t * 8 + j), -0.05 + 0.85 * v * math.sin(a)))
        for i in range(0, len(pts) - 1, 2):
            G += T.ring(0.022, 0.008, pts[i][0], pts[i][1], 0.6) * 1.3
    capa = [(-0.35 * s, -0.25), (0.35 * s, -0.25), (0.5 * s + 0.05 * math.sin(t * 10), 0.45), (0.15 * s, 0.35), (0, 0.5), (-0.15 * s, 0.35),
            (-0.5 * s - 0.05 * math.sin(t * 10), 0.45)]
    g, h = icone(T, capa, 0.8, 0.4)
    G, H = G + g, H + h
    g2, h2 = aura(T, t, 0.2, 1.0, 0.3, 0.0, 0.8)
    return (G + g2) * env, (H + h2) * env


def trio_unido(T, t, rng):
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    for j in range(3):
        u = ease_out(rel(t, 0.05 * j, 0.35 + 0.05 * j), 2)
        a = -math.pi / 2 + TAU * j / 3
        d = 0.8 * (1 - u) + 0.15
        g, h = icone(T, poe(ESPADA, d * math.cos(a), -0.05 + d * math.sin(a), 0.25, a - math.pi / 2), (1 - rel(t, 0.88, 1)) * 1.1, 0.5)
        G, H = G + g, H + h
    G += anel(T, t, 0.35, 0.8, 0.15, 0.65, 0.035, -0.05)
    g2, h2 = clarao(T, t, 0.33, 0.5, 0, -0.05, 0.7)
    return (G + g2) * env, (H + h2) * env


REGISTRO = [
    ("mu_polaridade", polaridade, GRANDE, "Magneto · o campo magnético", False),
    ("mu_empatia", empatia, GRANDE, "Ravena · a cura empática", False),
    ("mu_doenca_terminal", doenca_terminal, GRANDE, "Itachi · o sangue e os corvos", False),
    ("mu_medica_de_campo", medica_de_campo, GRANDE, "Sakura · a mão que cura", False),
    ("mu_ninguem_toca", ninguem_toca, GRANDE, "Mikasa · as duas lâminas", False),
    ("mu_corte_na_nuca", corte_na_nuca, GRANDE, "Levi · o giro e o corte na nuca", False),
    ("mu_particulas_pym", particulas_pym, GRANDE, "Homem-Formiga · as partículas Pym", False),
    ("mu_sentido_radar", sentido_radar, GRANDE, "Demolidor · o radar", False),
    ("mu_tempestade_pula", tempestade_pula, GRANDE, "Tempestade · o raio que pula", False),
    ("mu_cerebro", cerebro, GRANDE, "Professor X · o Cérebro", False),
    ("mu_doze_por_cento", doze_por_cento, GRANDE, "Senhor das Estrelas · 12% de um plano", False),
    ("mu_mares", mares, GRANDE, "Aquaman · as marés", False),
    ("mu_selo_da_luz", selo_da_luz, GRANDE, "Zelda · a Triforce", False),
    ("mu_pod_042", pod_042, GRANDE, "2B · o Pod 042", False),
    ("mu_familiar", familiar, GRANDE, "Alucard · o familiar", False),
    ("mu_corrente_intercepta", corrente_intercepta, GRANDE, "Shun · a corrente de Andrômeda", False),
    ("mu_dois_lados", dois_lados, GRANDE, "Saga · os dois lados", False),
    ("mu_rendicao_sentidos", rendicao_sentidos, GRANDE, "Shaka · a rendição dos sentidos", False),
    ("mu_areia", areia, GRANDE, "Gaara · a areia", False),
    ("mu_sem_esperanca", sem_esperanca, GRANDE, "Darkseid · os olhos ômega", False),
    ("mu_necroplasma", necroplasma, GRANDE, "Spawn · as correntes e a capa", False),
    ("mu_trio_unido", trio_unido, GRANDE, "Leonardo · o trio unido", False),
]
