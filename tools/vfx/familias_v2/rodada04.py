"""Rodada 4 das habilidades próprias: Ravena, Thanos, Gohan, Freeza e Itachi.

Ravena (o Corvo da alma já era dela)
- azarath_canto: o Preparo do Azarath Metrion Zinthos — ela flutua com as mãos
  acesas em roxo e a aura negra subindo em chamas lentas (laço).
- azarath_metrion: os tentáculos de energia negra vêm de todos os lados e
  agarram o rival, a joia vermelha da testa acende em cima e a alma estoura.
- manto_de_sombras: o manto negro de capuz se fecha em volta do aliado e as
  faíscas roxas de cura sobem por dentro.

Thanos (a Manopla já era dele)
- joia_do_tempo: a Joia do Tempo verde acende em cima, as ondas de tempo
  achatadas abrem devagar e a areia cai em câmera lenta (Lento e golpe cortado).
- manopla_joias: o Preparo do Equilíbrio — as seis joias acendem uma a uma no
  arco da manopla e o brilho cresce (laço).
- estalo_thanos: o estalo — o clarão branco e o corpo do rival virando pó que
  voa de lado.

Gohan (o Golpe do potencial já era dele)
- masenko_carga: as mãos sobre a cabeça juntando a energia amarela (ergue).
- masenko: o Masenko estoura no rival em amarelo.
- masenko_guarda: no aliado, a barreira amarela da energia que sobrou.
- aura_besta: o Preparo do Despertar — a aura branca-prateada pontuda, os raios
  roxos e o cabelo de luz subindo (laço).
- despertar_gohan: o soco desperto (perto) — o impacto prateado, a onda de
  choque e o chão rachando.

Freeza
- crueldade_freeza: a mão invisível — a pressão roxa aperta o rival (os dedos
  de energia fechando), ergue e solta com a pancada.
- raio_mortal_faixa: o Raio mortal — o laser fininho rosa do dedo (faixa, laço).
- raio_mortal: o furo do raio atravessando o rival (Exposto).
- bola_da_morte_carga: a Bola da Morte crescendo no dedo erguido (ergue).
- bola_da_morte_voo: a bola enorme laranja voando com a coroa vermelha (laço).
- bola_da_morte: a explosão laranja enorme no rival.

Itachi (os Corvos e o Susanoo já eram dele)
- tsukuyomi: o Tsukuyomi — o céu vira vermelho, a lua vermelha atrás e o
  Mangekyō de três lâminas girando na frente do rival.
- corvos_itachi_voo: o bando de corvos pequenos voando (laço; o Corvo da alma
  da Ravena é outro).
"""
from __future__ import annotations

import math

import numpy as np

from .charizard_megaman import _brasas, _fogo
from .base import FAIXA, GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _quadro(t, seed=0):
    return np.random.default_rng(seed + int(t * 997) % 9973)


def _raio(T, q, x1, y1, x2, y2, larg=0.01, depth=4, rough=0.32):
    return T.polyline(jagged(q, x1, y1, x2, y2, depth, rough), larg)


_RUIDOS: dict = {}


def _ruido(T, seed, escala=0.05, oitavas=3):
    chave = (T.W, T.H, seed, escala, oitavas)
    if chave not in _RUIDOS:
        _RUIDOS[chave] = T.noise(np.random.default_rng(seed), escala, oitavas)
    return _RUIDOS[chave]


def _faiscas(T, t, seed, n, t0, alcance=0.7, tam=0.012, cx=0.0, cy=0.0, a0=0.0, a1=TAU):
    sub = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        a = sub.uniform(a0, a1)
        d = 0.08 + alcance * ease_out(rel(t, t0, t0 + 0.5), 2) * sub.uniform(0.3, 1)
        pts.append((cx + d * math.cos(a), cy + d * math.sin(a), pulso(t, t0, 0.9) * sub.uniform(0.4, 1)))
    return T.splats(pts, tam)


# =================================================================== Ravena
def azarath_canto(T, t, rng):
    """O Preparo do Azarath: as duas mãos acesas em roxo, a aura negra subindo em chamas lentas em volta
    dela e a joia vermelha da testa piscando."""
    G, H = vazio(T)
    aura, miolo = _fogo(T, t, 0, 0.55, 0.42, 1.1, 3, 0.6)
    borda = np.clip(aura - T.blur(aura, 0.02) * 0.9, 0, 1) * 3
    b = 0.7 + 0.3 * math.sin(TAU * t * 2)
    maos = (T.gauss(-0.32, 0.1, 0.07) + T.gauss(0.32, 0.1, 0.07)) * 1.3 * b
    joia = T.gauss(0, -0.42, 0.035) * (0.6 + 0.6 * abs(math.sin(TAU * t * 3)))
    G += aura * 0.55 + np.clip(borda, 0, 1) * 0.6 + maos + joia * 1.5 + _brasas(T, t, 5, 10, 0, 0.3, 0.6, 0.7, 0.01) * 0.6
    H += maos * 0.7 + joia
    return G, H


def azarath_metrion(T, t, rng):
    """Azarath Metrion Zinthos: seis tentáculos de energia negra vêm de fora curvando e agarram o rival,
    a joia vermelha acende em cima e a alma estoura em roxo no fim."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    f = ease_out(rel(t, 0.0, 0.35), 2)
    tent = T.zero()
    for j in range(6):
        a0 = TAU * j / 6 + 0.3
        pts = []
        for k in range(16):
            u = k / 15 * f
            r = 0.95 - 0.7 * u
            a = a0 + 1.2 * u + 0.15 * math.sin(TAU * (t * 2 + u * 2 + j * 0.3))
            pts.append((r * math.cos(a), r * math.sin(a) * 0.9))
        tent += T.polyline(pts, 0.03 * (1 - 0.5 * f) + 0.01)
    tent *= 1 - rel(t, 0.6, 0.8)
    aperta = T.ring(0.28 - 0.06 * rel(t, 0.35, 0.5), 0.03) * pulso(t, 0.3, 0.75)
    joia = (T.polys([([(0, -0.62), (0.05, -0.56), (0, -0.5), (-0.05, -0.56)], 1.0)], 0.004) + T.gauss(0, -0.56, 0.06) * 0.8) * pulso(t, 0.25, 0.85)
    k = pulso(t, 0.55, 0.9)
    alma = T.gauss(0, 0, 0.22) * k * 1.4 + T.ring(0.1 + 0.6 * ease_out(rel(t, 0.55, 0.9), 2), 0.03) * k
    G += (tent * 0.9 + T.blur(tent, 0.02) * 0.6 + aperta + joia * 1.2 + alma) * env
    H += (joia * 0.8 + alma * 0.8) * env
    return G, H


def manto_de_sombras(T, t, rng):
    """O Manto de sombras: o capuz e o manto negro descem e se fecham em volta do aliado (a borda acesa
    em roxo, o miolo escuro) e as faíscas de cura sobem por dentro."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    f = ease_out(rel(t, 0.0, 0.35), 2)
    w = 0.55 * f + 0.05
    pts = [(0, -0.72), (0.2, -0.62), (0.3, -0.42)]
    pts += [(w, 0.0 + 0.1 * k / 4 + 0.05 * math.sin(TAU * (t + k * 0.2))) for k in range(5)]
    pts += [(w * 0.8, 0.62), (0.0, 0.7), (-w * 0.8, 0.62)]
    pts += [(-w, 0.4 - 0.1 * k + 0.05 * math.sin(TAU * (t + k * 0.2))) for k in range(5)]
    pts += [(-0.3, -0.42), (-0.2, -0.62)]
    manto = T.polys([(pts, 0.35)], 0.01)
    borda = T.polyline(pts + [pts[0]], 0.016)
    sub = np.random.default_rng(7)
    cura = []
    for _ in range(14):
        x = sub.normal(0, 0.15)
        u = (sub.uniform() + t * 0.8) % 1
        cura.append((x, 0.45 - 0.9 * u, (1 - u) * rel(t, 0.25, 0.4)))
    G += (manto * 0.6 + borda * 1.1 + T.splats(cura, 0.016) + T.gauss(0, 0.05, 0.25) * 0.25 * f) * env
    H += (borda * 0.3) * env
    return G, H


# =================================================================== Thanos
def joia_do_tempo(T, t, rng):
    """A Joia do Tempo: a joia verde acende em cima com o brilho, as ondas de tempo achatadas abrem devagar
    em volta do rival e a areia cai em câmera lenta."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    joia = (T.polys([([(0, -0.7), (0.07, -0.62), (0, -0.54), (-0.07, -0.62)], 1.0)], 0.004) * 1.2 + T.gauss(0, -0.62, 0.1) * 0.7) * rel(t, 0.0, 0.1)
    ondas = T.zero()
    for j in range(3):
        u = (t * 0.7 + j / 3) % 1
        ondas += T.ring(0.1 + 0.6 * u, 0.02, 0, 0.1, 2.2) * (1 - u) * rel(t, 0.05, 0.2)
    sub = np.random.default_rng(11)
    areia = []
    for _ in range(40):
        x = sub.uniform(-0.45, 0.45)
        u = (sub.uniform() + t * 0.25) % 1
        areia.append((x, -0.4 + 0.9 * u, (1 - u) * 0.8 * rel(t, 0.1, 0.25)))
    G += (joia + ondas + T.splats(areia, 0.008) + T.gauss(0, 0.1, 0.25) * 0.2) * env
    H += joia * 0.6 * env
    return G, H


def manopla_joias(T, t, rng):
    """O Preparo do Equilíbrio: a manopla erguida — as seis joias num arco acendem uma a uma, girando, e o
    brilho no meio cresce até o estalo."""
    G, H = vazio(T)
    J = T.zero()
    for k in range(6):
        a = -math.pi * 0.9 + math.pi * 0.8 * k / 5
        x, y = 0.38 * math.cos(a), 0.38 * math.sin(a) + 0.12
        acende = 0.4 + 0.6 * (((t * 6) % 6) >= k)
        J += T.polys([([(x, y - 0.06), (x + 0.045, y), (x, y + 0.06), (x - 0.045, y)], 1.0)], 0.003) * acende + T.gauss(x, y, 0.05) * 0.5 * acende
    meio = T.gauss(0, 0.05, 0.12 + 0.05 * math.sin(TAU * t * 2)) * 1.1
    G += J + meio
    H += J * 0.6 + meio * 0.8
    return G, H


def estalo_thanos(T, t, rng):
    """O Equilíbrio no rival: o clarão branco do estalo, e o corpo dele vira pó — os grãos se soltam de
    baixo para cima e voam de lado, sumindo."""
    G, H = vazio(T)
    env = apaga(t, 0.92, 1)
    k = pulso(t, 0.0, 0.25)
    clarao = T.gauss(0, 0, 0.3) * k * 1.6 + T.flare(0, 0, 1.0 * k + 1e-3, 0.0, 0.008) * k
    sub = np.random.default_rng(13)
    po = []
    for _ in range(140):
        x0, y0 = sub.normal(0, 0.18), sub.uniform(-0.45, 0.45)
        sai = 0.15 + 0.5 * (0.45 - y0) / 0.9
        u = rel(t, sai, sai + 0.45)
        if u <= 0:
            continue
        po.append((x0 + 0.9 * u ** 1.3 + 0.08 * math.sin(TAU * (u + x0)), y0 - 0.25 * u, (1 - u) * 0.9))
    P = T.splats(po, 0.009) if po else T.zero()
    G += (clarao + P * 1.2) * env
    H += clarao * 0.9 * env
    return G, H


# =================================================================== Gohan
def masenko_carga(T, t, rng):
    """O Masenko juntando: as duas mãos sobre a cabeça e a bola de energia amarela crescendo entre elas,
    com os raios entrando."""
    G, H = vazio(T)
    f = ease_out(rel(t, 0.0, 0.8), 1.5)
    bola = T.gauss(0, 0, 0.06 + 0.12 * f) * (0.8 + 0.6 * f)
    q = _quadro(t, 17)
    R = T.zero()
    for _ in range(4):
        a = q.uniform(0, TAU)
        R += _raio(T, q, 0.5 * math.cos(a), 0.5 * math.sin(a), 0.12 * math.cos(a), 0.12 * math.sin(a), 0.006, 3, 0.35)
    G += bola * 1.4 + R * 0.7 + T.ring(0.2 * f + 0.05, 0.015) * 0.6
    H += bola
    return G, H


def masenko(T, t, rng):
    """O Masenko no rival: a explosão amarela grande (o clarão, a bola de fogo de luz e o anel) e as
    faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    k = pulso(t, 0.0, 0.5)
    bola = T.gauss(0, 0, 0.12 + 0.18 * ease_out(rel(t, 0.0, 0.3), 2)) * k * 1.6
    anel = T.ring(0.15 + 0.6 * ease_out(rel(t, 0.05, 0.55), 2), 0.035) * pulso(t, 0.05, 0.6)
    G += (bola + anel + _faiscas(T, t, 19, 16, 0.05, 0.65, 0.012)) * env
    H += bola * 0.9 * env
    return G, H


def masenko_guarda(T, t, rng):
    """No aliado: a barreira amarela da energia do Masenko (o arco da frente e os pontos subindo)."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    f = ease_out(rel(t, 0.1, 0.4), 2)
    arco = T.arc_band(0.6 * f + 0.05, 0.04, -2.7, -0.44, 1.0, 0.0, 0, 0.15, 0.25) * rel(t, 0.1, 0.2)
    sub = np.random.default_rng(23)
    sobe = [(sub.uniform(-0.5, 0.5), 0.45 - 0.9 * ((sub.uniform() + t) % 1), 0.7) for _ in range(12)]
    G += (arco * 1.1 + T.splats(sobe, 0.012) * rel(t, 0.15, 0.3)) * env
    return G, H


def aura_besta(T, t, rng):
    """O Preparo do Despertar: a aura branca-prateada pontuda subindo em labaredas, os raios roxos
    estalando e o cabelo de luz em ponta no alto (laço)."""
    G, H = vazio(T)
    aura, miolo = _fogo(T, t, 0, 0.55, 0.38, 1.25, 29, 1.6)
    borda = np.clip(aura - T.blur(aura, 0.015) * 0.85, 0, 1) * 3
    q = _quadro(t, 31)
    R = T.zero()
    for _ in range(2):
        x = q.uniform(-0.35, 0.35)
        R += _raio(T, q, x, 0.4, x + q.uniform(-0.2, 0.2), -0.4, 0.008, 4, 0.4)
    ponta = T.polys([([(-0.18, -0.35), (-0.05, -0.75), (0.0, -0.45), (0.06, -0.8), (0.18, -0.35)], 0.7)], 0.006)
    G += aura * 0.6 + miolo * 0.4 + np.clip(borda, 0, 1) * 0.6 + R + ponta * 0.6
    H += R * 0.6 + np.clip(borda, 0, 1) * 0.3
    return G, H


def despertar_gohan(T, t, rng):
    """O Despertar no rival (perto): o soco prateado estoura (o clarão e as linhas de força em estrela), a
    onda de choque achatada abre e o chão racha embaixo."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    k = pulso(t, 0.0, 0.35)
    soco = T.gauss(0, 0, 0.16) * k * 2.0 + T.flare(0, 0, 1.1 * k + 1e-3, 0.4, 0.01) * k
    linhas = []
    for j in range(12):
        a = TAU * j / 12
        d0 = 0.15 + 0.4 * ease_out(rel(t, 0.0, 0.35), 2)
        linhas.append((d0 * math.cos(a), d0 * math.sin(a), (d0 + 0.25) * math.cos(a), (d0 + 0.25) * math.sin(a), 1.0))
    L = T.tapered(linhas, 0.022) * pulso(t, 0.0, 0.45)
    onda = T.ring(0.1 + 0.85 * ease_out(rel(t, 0.05, 0.6), 2), 0.04, 0, 0.45, 3.5) * pulso(t, 0.05, 0.7)
    q = np.random.default_rng(37)
    rach = T.zero()
    for _ in range(5):
        x = q.uniform(-0.15, 0.15)
        rach += _raio(T, q, x, 0.45, x + q.uniform(-0.6, 0.6), 0.45 + q.uniform(-0.08, 0.12), 0.008, 3, 0.3)
    rach *= rel(t, 0.1, 0.25)
    G += (soco + L * 1.1 + onda + rach) * env
    H += (soco * 0.9 + L * 0.4) * env
    return G, H


# =================================================================== Freeza
def crueldade_freeza(T, t, rng):
    """Crueldade calculada: a mão invisível — cinco dedos de energia roxa fecham em volta do rival
    apertando, a pressão sobe, ergue um pouco e solta com a pancada."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    f = ease_in(rel(t, 0.0, 0.35), 1.5)
    sobe = -0.12 * pulso(t, 0.35, 0.65)
    dedos = T.zero()
    for j in range(5):
        a = -math.pi / 2 + (j - 2) * 0.55
        r1 = 0.75 - 0.35 * f
        dedos += T.arc_band(r1, 0.035, a - 0.35, a + 0.35, 1.0, 0.0, 0, sobe, 0.6) * (0.7 + 0.3 * f)
    pressao = T.ring(0.3, 0.02, 0, sobe) * pulso(t, 0.3, 0.65) + T.gauss(0, sobe, 0.25) * 0.4 * pulso(t, 0.3, 0.65)
    k = pulso(t, 0.62, 0.85)
    pancada = T.gauss(0, 0.1, 0.15) * k * 1.5 + T.ring(0.1 + 0.4 * rel(t, 0.62, 0.85), 0.03, 0, 0.1, 1.6) * k
    G += (dedos * (1 - rel(t, 0.6, 0.7)) + pressao + pancada) * env
    H += (pancada * 0.8 + pressao * 0.3) * env
    return G, H


def raio_mortal_faixa(T, t, rng):
    """O Raio mortal: o laser fininho e reto do dedo, com o miolo branco e a borda rosa tremendo um pouco."""
    G, H = vazio(T)
    w = 0.03 * (1 + 0.15 * math.sin(TAU * t * 12))
    corpo = np.exp(-(T.V / w) ** 2)
    miolo = np.exp(-(T.V / (w * 0.35)) ** 2)
    G += corpo * 0.9 + miolo * 1.3 + np.exp(-(T.V / 0.1) ** 2) * 0.2
    H += miolo * 1.2
    return G, H


def raio_mortal(T, t, rng):
    """O Raio mortal no rival: o furo — o ponto branco que atravessa, o anel pequeno e o feixe saindo do
    outro lado, e as rachaduras de luz em volta (Exposto)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    k = pulso(t, 0.0, 0.35)
    furo = T.gauss(0, 0, 0.05) * 2.0 * (0.4 + 0.6 * k)
    sai = T.tapered([(0.05, 0, 0.9, 0, 1.0)], 0.03) * pulso(t, 0.0, 0.3)
    anel = T.ring(0.08 + 0.25 * ease_out(rel(t, 0.0, 0.35), 2), 0.015) * k
    q = np.random.default_rng(41)
    rach = T.zero()
    for _ in range(5):
        a = q.uniform(0, TAU)
        rach += _raio(T, q, 0.04 * math.cos(a), 0.04 * math.sin(a), 0.3 * math.cos(a), 0.3 * math.sin(a), 0.006, 3, 0.3)
    rach *= rel(t, 0.15, 0.3)
    G += (furo + sai * 1.2 + anel + rach * 0.8) * env
    H += (furo * 0.9 + sai * 0.6) * env
    return G, H


def _sol(T, cx, cy, r, t, seed):
    """A bola laranja: o miolo quente, a borda mais escura e a coroa vermelha ondulando."""
    rr = np.hypot(T.U - cx, T.V - cy)
    ang = np.arctan2(T.V - cy, T.U - cx)
    coroa_r = r * (1.12 + 0.08 * np.sin(ang * 7 + TAU * t * 2 + seed))
    coroa = np.clip(1 - np.abs(rr - coroa_r) / (r * 0.12), 0, 1)
    disco = np.clip(1 - rr / r, 0, 1) ** 0.5
    return disco, coroa


def bola_da_morte_carga(T, t, rng):
    """A Bola da Morte crescendo no dedo erguido: começa um ponto e incha até ficar maior que ele, com a
    coroa vermelha ondulando."""
    G, H = vazio(T)
    f = ease_out(rel(t, 0.0, 0.9), 1.5)
    r = 0.06 + 0.32 * f
    disco, coroa = _sol(T, 0, 0, r, t, 1)
    G += disco * 1.1 + coroa * 0.7 + T.gauss(0, 0, r * 1.4) * 0.3
    H += disco * 0.9
    return G, H


def bola_da_morte_voo(T, t, rng):
    """A Bola da Morte voando para +x: a esfera enorme e lenta, a coroa ondulando e o rastro de calor."""
    G, H = vazio(T)
    disco, coroa = _sol(T, 0.25, 0, 0.38, t, 2)
    rastro = T.tapered([(-0.95, 0, -0.1, 0, 1.0)], 0.22) * 0.25
    G += disco * 1.1 + coroa * 0.7 + rastro
    H += disco * 0.9
    return G, H


def bola_da_morte(T, t, rng):
    """A Bola da Morte no rival: o clarão, a bola de fogo laranja inchando com a coroa e o anel de choque
    grande, e as brasas caindo."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    f = ease_out(rel(t, 0.0, 0.4), 2)
    disco, coroa = _sol(T, 0, 0, 0.15 + 0.5 * f, t, 3)
    fogo = (disco * 1.1 + coroa * 0.6) * (1 - rel(t, 0.45, 0.85))
    k = pulso(t, 0.0, 0.25)
    clarao = T.gauss(0, 0, 0.3) * k * 1.4
    anel = T.ring(0.2 + 0.75 * ease_out(rel(t, 0.1, 0.6), 2), 0.04, 0, 0, 1.2) * pulso(t, 0.1, 0.65)
    sub = np.random.default_rng(43)
    brasas = [(sub.uniform(-0.6, 0.6), -0.3 + 0.9 * rel(t, 0.4, 1.0) * sub.uniform(0.5, 1), (1 - rel(t, 0.5, 1)) * sub.uniform(0.4, 1)) for _ in range(20)]
    G += (fogo + clarao + anel + T.splats(brasas, 0.012) * rel(t, 0.35, 0.45)) * env
    H += (fogo * 0.7 + clarao) * env
    return G, H


# =================================================================== Itachi
def _mangekyo(T, cx, cy, r, giro):
    """O Mangekyō do Itachi: o círculo do meio e três lâminas curvas que saem dele (o cata-vento)."""
    formas = []
    for k in range(3):
        a = giro + TAU * k / 3
        pts = []
        for u in np.linspace(0, 1, 10):
            aa = a + 1.4 * u
            rr = r * (0.25 + 0.75 * u)
            pts.append((cx + rr * math.cos(aa), cy + rr * math.sin(aa)))
        for u in np.linspace(1, 0, 10):
            aa = a + 1.4 * u - 0.55 * (1 - u) - 0.25
            rr = r * (0.25 + 0.6 * u)
            pts.append((cx + rr * math.cos(aa), cy + rr * math.sin(aa)))
        formas.append((pts, 1.0))
    return formas


def tsukuyomi(T, t, rng):
    """O Tsukuyomi: o mundo fica vermelho (o fundo avermelhado subindo), a lua vermelha enorme atrás e o
    Mangekyō de três lâminas girando devagar na frente do rival, com o anel preto em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    f = ease_out(rel(t, 0.0, 0.3), 2)
    fundo = np.exp(-(T.RAD / 0.85) ** 4) * 0.35 * f
    lua = np.clip(1 - np.hypot(T.U - 0.25, T.V + 0.3) / 0.32, 0, 1) ** 0.4 * 0.6 * f
    giro = TAU * t * 0.35
    olho = T.polys(_mangekyo(T, 0, 0.05, 0.32 * f + 0.01, giro), 0.004)
    anel = T.ring(0.34 * f + 0.01, 0.02, 0, 0.05)
    G += (fundo + lua + olho * 0.9 + anel * 0.8) * env
    H += (olho * 0.2 + lua * 0.3) * env
    return G, H


def corvos_itachi_voo(T, t, rng):
    """O bando de corvos do Itachi voando para +x: seis corvos pequenos batendo as asas, em formação
    solta, com as penas soltas atrás."""
    G, H = vazio(T)
    sub = np.random.default_rng(47)
    formas = []
    for k in range(6):
        cx = 0.35 - 0.25 * (k % 3) + sub.uniform(-0.05, 0.05)
        cy = -0.25 + 0.25 * (k // 2) * 0.6 + sub.uniform(-0.05, 0.05)
        bate = math.sin(TAU * (t * 4 + k * 0.17))
        s = 0.09
        formas.append(([(cx - 2 * s, cy - bate * s), (cx - 0.6 * s, cy - 0.2 * s), (cx, cy - 0.35 * s), (cx + 0.6 * s, cy - 0.2 * s), (cx + 2 * s, cy - bate * s), (cx + 0.5 * s, cy + 0.25 * s), (cx, cy + 0.4 * s), (cx - 0.5 * s, cy + 0.25 * s)], 1.0))
    C = T.polys(formas, 0.003)
    penas = [(-0.6 + 0.3 * ((sub.uniform() + t * 1.5) % 1) * -1, sub.uniform(-0.35, 0.35), 0.5) for _ in range(10)]
    G += C * 1.2 + T.splats(penas, 0.01) * 0.6
    H += C * 0.2
    return G, H


REGISTRO = [
    ("azarath_canto", azarath_canto, MEDIA, "Ravena · o canto do Azarath (Preparo, laço)", True),
    ("azarath_metrion", azarath_metrion, GRANDE, "Ravena · os tentáculos negros agarrando", False),
    ("manto_de_sombras", manto_de_sombras, GRANDE, "Ravena · o manto de capuz no aliado", False),
    ("joia_do_tempo", joia_do_tempo, GRANDE, "Thanos · a Joia do Tempo e a areia lenta", False),
    ("manopla_joias", manopla_joias, MEDIA, "Thanos · as seis joias acendendo (Preparo, laço)", True),
    ("estalo_thanos", estalo_thanos, GRANDE, "Thanos · o estalo e o pó", False),
    ("masenko_carga", masenko_carga, MEDIA, "Gohan · o Masenko juntando (ergue)", False),
    ("masenko", masenko, GRANDE, "Gohan · o Masenko estourando", False),
    ("masenko_guarda", masenko_guarda, GRANDE, "Gohan · a barreira amarela no aliado", False),
    ("aura_besta", aura_besta, MEDIA, "Gohan · a aura do Despertar (Preparo, laço)", True),
    ("despertar_gohan", despertar_gohan, GRANDE, "Gohan · o soco desperto", False),
    ("crueldade_freeza", crueldade_freeza, GRANDE, "Freeza · a mão invisível apertando", False),
    ("raio_mortal_faixa", raio_mortal_faixa, FAIXA, "Freeza · o Raio mortal (faixa, laço)", True),
    ("raio_mortal", raio_mortal, GRANDE, "Freeza · o furo do Raio mortal", False),
    ("bola_da_morte_carga", bola_da_morte_carga, MEDIA, "Freeza · a Bola da Morte crescendo (ergue)", False),
    ("bola_da_morte_voo", bola_da_morte_voo, MEDIA, "Freeza · a Bola da Morte voando (laço)", True),
    ("bola_da_morte", bola_da_morte, GRANDE, "Freeza · a explosão da Bola da Morte", False),
    ("tsukuyomi", tsukuyomi, GRANDE, "Itachi · o Tsukuyomi e o Mangekyō", False),
    ("corvos_itachi_voo", corvos_itachi_voo, MEDIA, "Itachi · o bando de corvos voando (laço)", True),
]
