"""Ataques básicos com animação própria, lote zd: Lion-O, Stewie, Macaco Louco, Danny Phantom, Akuma, Pato Donald, Jerry e
Majin Boo.

Golpes simples, cada um do personagem: o soco do Lion-O com a Garra de Thundera (as três pontas no dorso da mão), o
tapinha minúsculo do Stewie com o estalo desproporcional, a garra mecânica do robô do Macaco Louco, o punho
fantasma do Danny que atravessa transparente e fica sólido no acerto, o soco do Akuma com a aura do Satsui no Hado
em chamas escuras, os socos de moinho do Pato Donald furioso com as nuvens de raiva, o martelinho do Jerry com o
galo crescendo e o braço de borracha do Majin Boo esticando e balançando.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, TAU, apaga, ease_in, ease_out, estrela, jagged, janela, pulso, rel, vazio
from .basicos_a import _elipse_pts
from .basicos_u import _anel, _antebraco, _estrela_de_contato, _mao, _pts, _riscos, _vai_e_volta
from .basicos_w import _soco
from .basicos_x import _gotas


# ------------------------------------------------------------------ Lion-O
def soco_da_garra_thundera(T, t, rng):
    """Lion-O: a Garra de Thundera no dorso da mão (as três pontas curvas para a frente e o olho vermelho no meio) vem
    num soco e as pontas arranham o alvo, deixando três riscos."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.2, 0.18, 1.1, 'luva', faixa=(0.0, 0.1))
    garra = T.zero()
    if vis > 0.05:
        polys = []
        for k in range(3):
            y = -0.2 + 0.06 * k
            polys.append(([(px - 0.12, y + 0.03), (px + 0.1, y - 0.01), (px + 0.22, y + 0.03 * (k - 1)), (px + 0.06, y + 0.04)], 1.0))
        garra = T.polys(polys, 0.002) * vis
    olho = T.gauss(px - 0.06, -0.15, 0.025) * vis
    t0 = 0.2
    riscos = T.zero()
    kr = janela(t, t0, t0 + 0.04) * (1 - rel(t, t0 + 0.25, t0 + 0.45))
    if kr > 0:
        riscos = T.tapered([(-0.25, -0.3 + 0.12 * k, 0.25, -0.15 + 0.12 * k, 1.0) for k in range(3)], 0.026) * kr
    est = _estrela_de_contato(T, t, t0, 0.24, 6, 0.36)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + garra * 1.3 + riscos * 1.4 + est) * env
    H += (corpo * 0.3 + (d + B) * 0.7 + garra * 0.8 + olho * 2.0 + riscos * 1.0 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Stewie
def tapinha_do_stewie(T, t, rng):
    """Stewie: uma mãozinha de bebê, minúscula, dá um tapinha… e o estalo é enorme, com as linhas de quadrinho e o
    anel de choque de quem apanhou de um gênio do mal."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = ease_in(rel(t, 0.0, 0.18), 1.5)
    px = -0.8 + 0.7 * u - 0.4 * ease_in(rel(t, 0.3, 0.45), 1.5)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.4, 0.5))
    mao = T.polys([(_elipse_pts(px, 0.0, 0.07, 0.08, 0.0, 14), 1.0)] + [(_elipse_pts(px + 0.07, -0.06 + 0.03 * k, 0.04, 0.014, 0.0, 8), 1.0) for k in range(4)], 0.002)
    braco = T.polys([([(px - 0.06, -0.03), (px - 0.4, -0.04), (px - 0.4, 0.04), (px - 0.06, 0.03)], 0.85)], 0.002)
    corpo = np.clip(mao + braco, 0, 1) * vis
    t0 = 0.18
    estalo = T.polys([(estrela(0.0, 0.0, 0.24 * pulso(t, t0, t0 + 0.3) + 0.01, 0.2, 12, 0.5), 1.0)], 0.003) * pulso(t, t0, t0 + 0.3)
    linhas = _riscos(T, t, t0, 0.32, 8, 0.2, 0.42, 0.02, 7, 0.0, TAU)
    anel = _anel(T, t, t0, t0 + 0.45, 0.08, 0.42, 0.04, 1.0)
    G += (corpo * 1.1 + estalo * 1.2 + linhas * 1.3 + anel * 1.2) * env
    H += (corpo * 0.5 + estalo * 0.9 + linhas * 0.9 + anel * 0.4) * env
    return G, H


# ------------------------------------------------------------------ Macaco Louco
def soco_do_robo_mojo(T, t, rng):
    """Macaco Louco: o braço do robô (canos, rebites e a garra mecânica de três dedos) avança soltando vapor, fecha a
    garra no alvo com um aperto e solta faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    px = _vai_e_volta(t, 0.24, -1.0, -0.16, 0.18)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.52, 0.68))
    fecha = ease_out(rel(t, 0.2, 0.3), 2)
    garras = []
    for k, a0 in enumerate((-0.7, 0.0, 0.7)):
        a = a0 * (1 - 0.6 * fecha)
        x1, y1 = px + 0.14 * math.cos(a), 0.14 * math.sin(a)
        x2, y2 = x1 + 0.16 * math.cos(a * 0.5), y1 + 0.16 * math.sin(a * 0.5)
        garras += [(px, 0.0, x1, y1, 1.0), (x1, y1, x2, y2, 1.0)]
    G_garra = T.lines(garras, 0.05)
    palma = T.polys([(_elipse_pts(px, 0.0, 0.09, 0.12, 0.0, 14), 1.0)], 0.003)
    cano = T.polys([([(px - 0.08, -0.08), (px - 0.65, -0.1), (px - 0.65, 0.1), (px - 0.08, 0.08)], 0.85)], 0.003)
    corpo = np.clip(G_garra + palma + cano, 0, 1) * vis
    rebites = sum(T.gauss(px - 0.2 - 0.15 * k, s * 0.07, 0.012) for k in range(3) for s in (-1, 1)) * vis
    vapor = T.zero()
    kv = pulso(t, 0.05, 0.4)
    if kv > 0:
        for k in range(4):
            vapor += T.gauss(px - 0.55 - 0.06 * k, -0.15 - 0.08 * k, 0.05 + 0.02 * k)
        vapor *= kv * 0.7
    t0 = 0.26
    faiscas = _riscos(T, t, t0, 0.35, 9, 0.12, 0.45, 0.022, 81, 0.0, TAU)
    est = _estrela_de_contato(T, t, t0, 0.24, 6, 0.3)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + vapor + faiscas * 1.3 + est) * env
    H += (corpo * 0.3 + rebites * 1.5 + vapor * 0.4 + faiscas * 0.9 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Danny Phantom
def soco_fantasma_danny(T, t, rng):
    """Danny Phantom: o punho vem transparente, só o contorno brilhando (intangível), e fica sólido no último instante
    para acertar; o acerto solta um anel de ectoplasma que ondula."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    px = _vai_e_volta(t, 0.22, recua=0.18)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.48, 0.64))
    M, d = _mao(T, px, 0.0, 1.1, 'luva')
    A, B = _antebraco(T, px, 0.0, 1.1, 0.44, 0.1, (0.0, 0.08))
    cheio = np.clip(M + A, 0, 1)
    solido = janela(t, 0.17, 0.22)
    contorno = np.clip(T.blur(cheio, 0.012) * 2.4 - cheio * 1.8, 0, 1)
    corpo = (cheio * (0.2 + 0.8 * solido) + contorno * (1 - solido) * 1.4) * vis
    cauda = T.zero()
    if vis > 0.05:
        pts = [(px - 0.45 - 0.4 * s, 0.08 * math.sin(s * 8 - t * 25) * s) for s in np.linspace(0, 1, 16)]
        cauda = T.polyline(pts, 0.04) * (1 - solido * 0.7) * vis
    t0 = 0.22
    ecto = T.zero()
    ke = pulso(t, t0, t0 + 0.5)
    if ke > 0:
        r = 0.15 + 0.35 * rel(t, t0, t0 + 0.5)
        pts = [((r + 0.03 * math.sin(a * 6 + t * 20)) * math.cos(a), (r + 0.03 * math.sin(a * 6 + t * 20)) * math.sin(a)) for a in np.linspace(0, TAU, 40)]
        ecto = T.polyline(pts, 0.03) * ke
    est = _estrela_de_contato(T, t, t0, 0.24, 7, 0.4)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.4 + cauda * 0.9 + ecto * 1.3 + est) * env
    H += (corpo * 0.4 + d * vis * solido * 0.7 + cauda * 0.5 + ecto * 0.8 + est * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Akuma
def soco_do_satsui(T, t, rng):
    """Akuma: o punho fechado vem com a aura do Satsui no Hado, chamas escuras e pontudas tremendo em volta do braço,
    e o acerto estoura numa estrela de pontas finas com o kanji do céu riscado em luz por um instante (o 天)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    corpo, d, B, px, vis = _soco(T, t, 0.2, 0.16, 1.1, faixa=(0.0, 0.1))
    aura = T.zero()
    if vis > 0.05:
        segs = []
        for j in range(14):
            a = TAU * j / 14
            r0 = 0.18
            r1 = r0 + 0.1 + 0.06 * math.sin(t * 40 + j * 2.3)
            segs.append((px - 0.15 + r0 * math.cos(a) * 1.6, r0 * math.sin(a), px - 0.15 + r1 * math.cos(a) * 1.6, r1 * math.sin(a) - 0.04, 1.0))
        aura = T.tapered(segs, 0.04) * vis
    t0 = 0.2
    kk = pulso(t, t0 + 0.02, t0 + 0.45)
    kanji = T.zero()
    if kk > 0:
        kanji = T.lines([(-0.16, -0.16, 0.16, -0.16, 1.0), (-0.2, -0.02, 0.2, -0.02, 1.0), (0.0, -0.16, 0.0, -0.02, 1.0),
                         (0.0, -0.02, -0.2, 0.2, 1.0), (0.0, -0.02, 0.2, 0.2, 1.0)], 0.035) * kk
    est = _estrela_de_contato(T, t, t0, 0.34, 10, 0.2, 0.0, 0.3)
    G += (corpo * 1.0 + T.blur(corpo, 0.02) * 0.35 + aura * 1.2 + kanji * 1.3 + est * 1.1) * env
    H += (corpo * 0.3 + (d + B) * 0.6 + aura * 0.4 + kanji * 1.2 + est) * env
    return G, H


# ------------------------------------------------------------------ Pato Donald
def pancada_furiosa_donald(T, t, rng):
    """Pato Donald: furioso, ele gira os punhos como moinho (vários punhos borrados em volta de um eixo) e vai
    batendo; as nuvenzinhas de raiva saem em volta e o acerto é uma pancadaria de estrelas."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cx = -0.55 + 0.35 * ease_out(rel(t, 0.0, 0.2), 2)
    vis = janela(t, 0.0, 0.05) * (1 - rel(t, 0.6, 0.75))
    punhos = T.zero()
    for k in range(4):
        a = t * 30 + k * math.pi / 2
        x, y = cx + 0.22 * math.cos(a), 0.18 * math.sin(a)
        M, _ = _mao(T, x, y, 0.6, 'luva')
        punhos += M * (0.5 + 0.5 * (k == 0))
    giro = T.ring(0.22, 0.04, cx, 0.0, 1.2) * 0.4
    corpo = np.clip(punhos + giro, 0, 1) * vis
    nuvens = T.zero()
    kn = pulso(t, 0.05, 0.7)
    if kn > 0:
        for k in range(3):
            fase = (t * 2.5 + k / 3) % 1
            x, y = cx - 0.2 + 0.2 * k, -0.35 - 0.2 * fase
            nuvens += (T.gauss(x, y, 0.05) + T.gauss(x + 0.05, y - 0.02, 0.04) + T.gauss(x - 0.05, y, 0.04)) * (1 - fase)
        nuvens *= kn * 0.8
    estrelas = T.zero()
    for k in range(4):
        t0 = 0.14 + 0.1 * k
        ke = pulso(t, t0, t0 + 0.22)
        if ke > 0:
            a = 1.3 * k
            estrelas += T.polys([(estrela(0.12 * math.cos(a), 0.12 * math.sin(a), 0.15 * ke + 0.01, a, 5, 0.45), 1.0)], 0.002) * ke
    G += (corpo * 1.0 + nuvens + estrelas * 1.3) * env
    H += (corpo * 0.35 + nuvens * 0.5 + estrelas) * env
    return G, H


# ------------------------------------------------------------------ Jerry
def martelinho_do_jerry(T, t, rng):
    """Jerry: um martelinho de madeira, quase do tamanho dele, sobe e desce na cabeça do alvo; no "tonc" cresce um galo
    redondo e estrelinhas giram em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    sobe = ease_out(rel(t, 0.0, 0.14), 2)
    desce = ease_in(rel(t, 0.14, 0.26), 2.4)
    ang = -1.8 * sobe + 1.9 * desce - 0.1
    piv = (-0.55, 0.25)
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.5, 0.62))
    cabo = T.polyline([piv, (piv[0] + 0.55 * math.cos(ang - 1.2), piv[1] + 0.55 * math.sin(ang - 1.2))], 0.035)
    hx, hy = piv[0] + 0.6 * math.cos(ang - 1.2), piv[1] + 0.6 * math.sin(ang - 1.2)
    cabeca = T.polys([(_pts([(-0.08, -0.13), (0.08, -0.13), (0.08, 0.13), (-0.08, 0.13)], hx, hy, 1.0, ang - 1.2), 1.0)], 0.003)
    corpo = np.clip(cabo + cabeca, 0, 1) * vis
    t0 = 0.26
    kg = janela(t, t0, t0 + 0.12) * apaga(t, 0.7, 0.88)
    galo = T.polys([(_elipse_pts(0.0, -0.2 - 0.08 * ease_out(rel(t, t0, t0 + 0.15), 3), 0.07 + 0.03 * ease_out(rel(t, t0, t0 + 0.15), 3), 0.07 + 0.04 * ease_out(rel(t, t0, t0 + 0.15), 3), 0.0, 16), 1.0)], 0.003) * kg
    gira = T.zero()
    if kg > 0:
        for k in range(3):
            a = t * 10 + TAU * k / 3
            gira += T.polys([(estrela(0.22 * math.cos(a), -0.3 + 0.06 * math.sin(a), 0.05, a, 5, 0.45), 1.0)], 0.002)
        gira *= kg
    tonc = _estrela_de_contato(T, t, t0, 0.24, 8, 0.4, 0.0, 0.2)
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + galo * 1.1 + gira * 1.3 + tonc) * env
    H += (corpo * 0.35 + galo * 0.5 + gira * 1.0 + tonc * 0.9) * env
    return G, H


# ------------------------------------------------------------------ Majin Boo
def soco_de_borracha_buu(T, t, rng):
    """Majin Boo: o braço rosa de borracha estica até o alvo balançando como mola, o punho redondo acerta "boing" e o
    braço volta encolhendo; saem baforadas de vapor."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    u = ease_out(rel(t, 0.0, 0.22), 1.6)
    volta = ease_in(rel(t, 0.36, 0.62), 1.6)
    alcance = u * (1 - volta)
    px = -0.9 + 0.78 * alcance
    vis = janela(t, 0.0, 0.04) * (1 - rel(t, 0.58, 0.68))
    pts = []
    for s in np.linspace(0, 1, 24):
        x = -0.95 + (px + 0.95) * s
        pts.append((x, 0.06 * math.sin(s * 9 + t * 30) * (1 - s) * (0.3 + alcance)))
    braco = T.polyline(pts, 0.07)
    punho = T.polys([(_elipse_pts(px, 0.0, 0.14, 0.13, 0.0, 18), 1.0)], 0.003)
    corpo = np.clip(braco + punho, 0, 1) * vis
    t0 = 0.22
    boing = _anel(T, t, t0, t0 + 0.35, 0.08, 0.45, 0.05, 1.0) + _anel(T, t, t0 + 0.08, t0 + 0.42, 0.06, 0.3, 0.035, 1.0)
    vapor = T.zero()
    kv = pulso(t, t0, t0 + 0.6)
    if kv > 0:
        for k in range(3):
            fase = rel(t, t0 + 0.05 * k, t0 + 0.6)
            vapor += T.gauss(-0.1 + 0.12 * k, -0.25 - 0.3 * fase, 0.05 + 0.04 * fase) * (1 - fase)
        vapor *= kv
    G += (corpo * 1.05 + T.blur(corpo, 0.02) * 0.35 + boing * 1.3 + vapor * 0.8) * env
    H += (corpo * 0.4 + boing * 0.5 + vapor * 0.5) * env
    return G, H


REGISTRO = [
    ("soco_da_garra_thundera", soco_da_garra_thundera, GRANDE, "básico do Lion-O: a Garra de Thundera e os três riscos", False),
    ("tapinha_do_stewie", tapinha_do_stewie, GRANDE, "básico do Stewie: a mãozinha e o estalo desproporcional", False),
    ("soco_do_robo_mojo", soco_do_robo_mojo, GRANDE, "básico do Macaco Louco: a garra mecânica do robô e o vapor", False),
    ("soco_fantasma_danny", soco_fantasma_danny, GRANDE, "básico do Danny Phantom: o punho intangível que fica sólido", False),
    ("soco_do_satsui", soco_do_satsui, GRANDE, "básico do Akuma: a aura do Satsui no Hado e o kanji do céu", False),
    ("pancada_furiosa_donald", pancada_furiosa_donald, GRANDE, "básico do Pato Donald: os punhos de moinho e as nuvens de raiva", False),
    ("martelinho_do_jerry", martelinho_do_jerry, GRANDE, "básico do Jerry: o martelinho e o galo crescendo", False),
    ("soco_de_borracha_buu", soco_de_borracha_buu, GRANDE, "básico do Majin Boo: o braço de borracha esticando", False),
]
