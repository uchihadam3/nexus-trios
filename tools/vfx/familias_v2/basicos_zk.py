"""Ataques básicos com animação própria, lote zk: Sailor Moon, Donatello, Michelangelo, Zuko, Azula, Muzan, Pantera Negra e
Carnificina.

Os chutes ganham cara: a meia-lua e as estrelinhas da Sailor Moon, o chute com o bastão bo girando do Donatello, o chute
com a fatia de pizza girando do Michelangelo, o arco de fogo laranja do Zuko e o fogo azul com faísca da Azula. E as
garras: os chicotes de carne cheios de espinhos do Muzan, as garras de vibranium com o pulso cinético roxo do Pantera
Negra e as lâminas vermelhas de simbionte da Carnificina.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, back, ease_in, ease_out, estrela, janela, lamina, pulso, rel, vazio
from .basicos_a import _elipse_pts, _zigue
from .basicos_u import _anel, _estrela_de_contato, _riscos
from .basicos_x import _gotas
from .basicos_zj import _chute


def _arco_de_fogo(T, t, t0, t1, a0, a1, r, larg, cx=0.0, cy=0.0, n=7, ondula=0.03):
    """O rastro do chute em chamas: a faixa curva e as línguas de fogo subindo dela."""
    p = ease_out(rel(t, t0, t1), 2)
    sai = apaga(t, t1 + 0.1, t1 + 0.4)
    fim = a0 + (a1 - a0) * p + 0.01
    faixa = T.arc_band(r, larg, a0, fim, cx=cx, cy=cy, crescente=True) * sai
    linguas = []
    for k in range(n):
        a = a0 + (fim - a0) * (k + 0.5) / n
        bx, by = cx + math.cos(a) * r, cy + math.sin(a) * r
        alt = 0.1 + ondula * math.sin(t * 40 + k * 1.9)
        linguas.append(([(bx - 0.04, by), (bx, by - alt), (bx + 0.04, by)], 1.0))
    return faixa, T.polys(linguas, 0.01) * sai


# ------------------------------------------------------------------ Sailor Moon
def chute_lunar(T, t, rng):
    """Sailor Moon: o chute rápido de sapatinha vermelha e, no acerto, a meia-lua dourada brilha com estrelinhas em
    volta (em nome da Lua)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    pe, arco, px, py, vis = _chute(T, t, 0.2, 1.05)
    kl = pulso(t, 0.18, 0.62)
    lua = T.zero()
    if kl > 0:
        s = back(rel(t, 0.18, 0.3), 2.0)
        lua = (T.polys([(_elipse_pts(0, 0, 0.18 * s + 0.005, 0.18 * s + 0.005, 0.0, 24), 1.0)], 0.003) - T.polys([(_elipse_pts(0.08 * s, -0.04 * s, 0.15 * s, 0.15 * s, 0.0, 24), 1.0)], 0.003))
        lua = np.clip(lua, 0, 1) * kl
    estrelas = T.zero()
    for j in range(6):
        a = j * TAU / 6 + t * 3
        r = 0.3 + 0.05 * math.sin(t * 20 + j)
        estrelas += T.polys([(estrela(math.cos(a) * r, math.sin(a) * r, 0.04, a, 5, 0.45), 1.0)], 0.002) * pulso(t, 0.2, 0.7)
    G += (pe * 1.1 + arco + lua * 1.2 + estrelas * 1.2) * env
    H += (pe * 0.5 + lua * 0.9 + estrelas) * env
    return G, H


# ------------------------------------------------------------------ Donatello
def chute_e_bo_donatello(T, t, rng):
    """Donatello: o chute vem junto com o bastão bo girando como hélice, e o acerto solta faíscas de engrenagem (o gênio
    da tecnologia)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    pe, arco, px, py, vis = _chute(T, t, 0.22, 1.05)
    a = t * 30
    kb = janela(t, 0.0, 0.06) * (1 - rel(t, 0.4, 0.55))
    bo = T.lines([(-0.55 - math.cos(a) * 0.35, -0.3 - math.sin(a) * 0.35, -0.55 + math.cos(a) * 0.35, -0.3 + math.sin(a) * 0.35, 1.0)], 0.035) * kb
    borrao = T.ring(0.35, 0.02, -0.55, -0.3) * kb * 0.4
    kg = pulso(t, 0.22, 0.6)
    engrenagem = T.zero()
    if kg > 0:
        dentes = estrela(0, 0, 0.16, t * 6, 10, 0.78)
        engrenagem = (T.polyline(dentes + [dentes[0]], 0.016) + T.ring(0.06, 0.012)) * kg
    faiscas = _riscos(T, t, 0.22, 0.3, 8, 0.1, 0.4, 0.016, 31, 0.0, TAU)
    G += (pe * 1.1 + arco + bo + borrao + engrenagem + faiscas) * env
    H += (pe * 0.5 + bo * 0.6 + engrenagem * 0.8 + faiscas * 0.8) * env
    return G, H


# ------------------------------------------------------------------ Michelangelo
def chute_cowabunga(T, t, rng):
    """Michelangelo: o chute festeiro, e no acerto uma fatia de pizza sai girando para o alto, com as gotinhas de
    queijo, enquanto o nunchaku rodopia atrás."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    pe, arco, px, py, vis = _chute(T, t, 0.2, 1.05)
    kn = janela(t, 0.0, 0.06) * (1 - rel(t, 0.3, 0.45))
    a = t * 35
    nunchaku = (T.lines([(-0.7, -0.4, -0.7 + math.cos(a) * 0.3, -0.4 + math.sin(a) * 0.3, 1.0)], 0.045) + T.ring(0.3, 0.02, -0.7, -0.4) * 0.35) * kn
    u = rel(t, 0.2, 0.8)
    pizza = T.zero()
    if 0 < u < 1:
        cx, cy = 0.15 * u, -0.1 - 0.5 * u + 0.4 * u * u
        rot = u * 9
        tri = [(cx + math.cos(rot) * 0.24, cy + math.sin(rot) * 0.24), (cx + math.cos(rot + 2.4) * 0.2, cy + math.sin(rot + 2.4) * 0.2),
               (cx + math.cos(rot - 2.4) * 0.2, cy + math.sin(rot - 2.4) * 0.2)]
        pizza = T.polys([(tri, 1.0)], 0.003) * (1 - u ** 3)
        pizza += sum(T.gauss(cx + math.cos(rot + k) * 0.04, cy + math.sin(rot + k) * 0.04, 0.012) for k in range(3)) * (1 - u)
    est = _estrela_de_contato(T, t, 0.2, 0.24, 6, 0.32)
    G += (pe * 1.1 + arco + nunchaku + pizza * 1.2 + est) * env
    H += (pe * 0.5 + nunchaku * 0.5 + pizza * 0.8 + est) * env
    return G, H


# ------------------------------------------------------------------ Zuko
def chute_de_fogo_zuko(T, t, rng):
    """Zuko: o chute em arco solta uma lâmina de fogo laranja que segue o pé, com as línguas de chama subindo do
    rastro."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    pe, _, px, py, vis = _chute(T, t, 0.2, 1.05)
    faixa, linguas = _arco_de_fogo(T, t, 0.02, 0.22, 2.6, 0.2, 0.55, 0.14, cx=-0.35, cy=0.15)
    brasas = _gotas(T, t, 0.22, 0.5, 14, 73, tam=0.02, cai=-0.3, alcance=0.4)
    est = _estrela_de_contato(T, t, 0.2, 0.26, 7, 0.32)
    G += (pe * 1.1 + T.glow(faixa, 1.0, 0.8, 0.03) + linguas * 1.1 + brasas + est) * env
    H += (pe * 0.5 + faixa * 0.6 + linguas * 0.7 + brasas * 0.8 + est) * env
    return G, H


# ------------------------------------------------------------------ Azula
def chute_de_fogo_azul(T, t, rng):
    """Azula: o chute girando solta fogo azul em espiral (mais quente e mais preciso que o do irmão), e uma faísca de
    relâmpago estala no acerto."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    pe, _, px, py, vis = _chute(T, t, 0.2, 1.05, ang0=-1.2)
    faixa, linguas = _arco_de_fogo(T, t, 0.0, 0.24, -2.8, 0.3, 0.45, 0.12, n=9, ondula=0.05)
    raio = T.polyline(_zigue(-0.2, -0.45, 0.05, 0.0, 6, 0.05), 0.016) * pulso(t, 0.2, 0.36)
    est = _estrela_de_contato(T, t, 0.2, 0.24, 8, 0.32)
    G += (pe * 1.1 + T.glow(faixa, 1.0, 0.8, 0.03) + linguas * 1.1 + raio * 1.3 + est) * env
    H += (pe * 0.5 + faixa * 0.7 + linguas * 0.8 + raio * 1.2 + est) * env
    return G, H


# ------------------------------------------------------------------ Muzan
def chicotes_de_carne_muzan(T, t, rng):
    """Muzan: os braços viram chicotes de carne cheios de espinhos e açoitam o alvo de três direções ao mesmo tempo,
    rápido demais, e recolhem."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    chicotes = T.zero()
    for j, (x0, y0) in enumerate(((-0.95, -0.5), (-0.95, 0.1), (-0.8, 0.6))):
        vai = ease_out(rel(t, 0.0 + 0.03 * j, 0.16 + 0.03 * j), 2)
        volta = rel(t, 0.3, 0.5)
        alc = vai * (1 - volta)
        if alc > 0.02:
            pts = [(x0 + (0.0 - x0) * s * alc, y0 + (0.0 - y0) * s * alc + 0.08 * math.sin(s * 7 + j + t * 20) * (1 - s)) for s in np.linspace(0, 1, 18)]
            chicotes += T.polyline(pts, 0.035)
            for s in (0.3, 0.55, 0.8):
                x, y = pts[int(s * 17)]
                chicotes += T.polys([([(x - 0.02, y), (x, y - 0.05), (x + 0.02, y)], 1.0)], 0.003)
    est = _estrela_de_contato(T, t, 0.18, 0.26, 9, 0.3)
    sangue = _gotas(T, t, 0.18, 0.45, 12, 43, tam=0.025, cai=0.5, alcance=0.4)
    G += (chicotes * 1.1 + est + sangue) * env
    H += (chicotes * 0.5 + est + sangue * 0.3) * env
    return G, H


# ------------------------------------------------------------------ Pantera Negra
def garras_de_vibranio(T, t, rng):
    """Pantera Negra: as garras de vibranium riscam em dois tempos, e a energia cinética guardada no traje solta um
    pulso roxo em ondas hexagonais."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    garras = T.zero()
    for j, (t0, sobe) in enumerate(((0.0, 1), (0.1, -1))):
        k = rel(t, t0, t0 + 0.1)
        if k > 0:
            garras += T.polys([(lamina(-0.4, 0.3 * sobe + 0.1 * i - 0.1, 0.35, -0.25 * sobe + 0.1 * i - 0.1, 0.025, ease_out(k, 2.5), rel(t, 0.35, 0.55)), 1.0) for i in range(3)], 0.002)
    pulso_ = T.zero()
    for j in range(3):
        u = rel(t, 0.2 + 0.07 * j, 0.6 + 0.07 * j)
        if 0 < u < 1:
            r = 0.1 + 0.5 * ease_out(u, 2)
            pts = [(math.cos(a) * r, math.sin(a) * r) for a in np.linspace(0, TAU, 7) + math.pi / 6]
            pulso_ += T.polyline(pts, 0.02 * (1 - u) + 0.004) * (1 - u)
    G += (T.glow(garras, 1.1, 0.7, 0.02) + pulso_ * 1.2) * env
    H += (garras * 1.5 + pulso_ * 0.7) * env
    return G, H


# ------------------------------------------------------------------ Carnificina
def laminas_simbiontes(T, t, rng):
    """Carnificina: o simbionte vermelho brota em várias lâminas tortas e caóticas que cortam juntas, e respingos
    escuros voam para todo lado."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    laminas = T.zero()
    q = np.random.default_rng(97)
    for j in range(5):
        a = q.uniform(-0.8, 0.8) + math.pi
        k = rel(t, 0.0 + 0.03 * j, 0.14 + 0.03 * j)
        if k > 0:
            x0, y0 = math.cos(a) * 0.75, math.sin(a) * 0.6
            torto = q.uniform(-0.2, 0.2)
            laminas += T.polys([(lamina(x0, y0, x0 * -0.2 + torto, y0 * -0.2 - torto, 0.035, ease_out(k, 2), rel(t, 0.35 + 0.02 * j, 0.6)), 1.0)], 0.003)
    gosma = T.zero()
    if t < 0.4:
        for j in range(3):
            gosma += T.polyline([(-0.9 + 0.3 * s, -0.4 + 0.4 * j + 0.06 * math.sin(s * 10 + t * 30)) for s in np.linspace(0, 1, 10)], 0.03)
        gosma *= janela(t, 0.0, 0.06) * (1 - rel(t, 0.25, 0.4))
    respingos = _gotas(T, t, 0.16, 0.5, 18, 107, tam=0.024, cai=0.4, alcance=0.55, a0=-3.1, a1=3.1)
    G += (T.glow(laminas, 1.1, 0.6, 0.02) + gosma * 0.8 + respingos * 1.1) * env
    H += (laminas * 1.3 + gosma * 0.3 + respingos * 0.4) * env
    return G, H


REGISTRO = [
    ("chute_lunar", chute_lunar, GRANDE, "básico da Sailor Moon: o chute e a meia-lua com estrelinhas", False),
    ("chute_e_bo_donatello", chute_e_bo_donatello, GRANDE, "básico do Donatello: o chute e o bastão bo girando", False),
    ("chute_cowabunga", chute_cowabunga, GRANDE, "básico do Michelangelo: o chute e a fatia de pizza voando", False),
    ("chute_de_fogo_zuko", chute_de_fogo_zuko, GRANDE, "básico do Zuko: o chute com o arco de fogo laranja", False),
    ("chute_de_fogo_azul", chute_de_fogo_azul, GRANDE, "básico da Azula: o chute com o fogo azul e o relâmpago", False),
    ("chicotes_de_carne_muzan", chicotes_de_carne_muzan, GRANDE, "básico do Muzan: os chicotes de carne com espinhos", False),
    ("garras_de_vibranio", garras_de_vibranio, GRANDE, "básico do Pantera Negra: as garras e o pulso cinético", False),
    ("laminas_simbiontes", laminas_simbiontes, GRANDE, "básico da Carnificina: as lâminas de simbionte e os respingos", False),
]
