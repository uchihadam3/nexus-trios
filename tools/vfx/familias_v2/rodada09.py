"""Rodada 9 das habilidades próprias: Roy (Fullmetal Alchemist), Griffith (Berserk), Jotaro, Dio e
Giorno (JoJo).

Roy
- chuva_de_fogo: a Chuva de fogo — bolas de fogo descem em diagonal do alto, cada uma com a cauda,
  e explodem no chão em labaredas, uma depois da outra.
- ignicao_preparo: o Preparo do Campo incendiado — a luva com o círculo da salamandra (o círculo, o
  triângulo e a chama no meio) brilhando, faíscas no estalo (laço).
- campo_incendiado: o Campo incendiado — o rastro de fogo corre pelo chão, fecha um anel em volta do
  rival e detona numa coluna de fogo.

Griffith
- visao_de_falcao: o falcão mergulha (as asas para trás), a mira fecha e as penas caem.
- comando_da_banda: a bandeira do Bando do Falcão (o pano tremulando, o falcão no meio) e o brado em
  arcos que chegam aos aliados.
- eclipse_preparo: o Preparo do Destino — a lua tapando o sol, o anel de fogo escuro (laço).
- destino_ascendente: o Eclipse — o sol negro com a coroa, as asas escuras de Femto abrem por trás e
  a onda escura passa.

Jotaro
- precisao_absoluta: a Precisão — o dedo estelar: a estocada fina e muito rápida, as estrelinhas no
  rastro e o anel do impacto exato.
- star_preparo: o Preparo do The World — a aura do Star Platinum com as estrelas girando (laço).
- the_world_jotaro: o tempo para — a bolha que inverte tudo (o anel que cresce), as estrelas paradas
  no ar, e os golpes caindo de uma vez quando o tempo volta.

Dio
- facas_do_dio: as facas paradas no ar em leque em volta do rival (o tempo parado), e de repente
  todas voam juntas e cravam.
- za_warudo_preparo: o Preparo do O Mundo — o relógio dourado batendo (os ponteiros e o tique) (laço).
- za_warudo: O Mundo — a esfera dourada se abre com o mostrador do relógio, os ponteiros param, e o
  rolo compressor cai do alto e esmaga.

Giorno
- reflexo_de_dano: a Gold Experience — as vinhas douradas brotam e viram um escudo de folhas em volta
  do aliado, a joaninha brilha no meio, e o dano volta em faíscas para fora.
- ouro_preparo: o Preparo da Experiência — a aura dourada pulsando com a joaninha (laço).
- experiencia_dourada: a vida criada — flores de cinco pétalas desabrocham em volta do trio, a luz
  dourada sobe e as pétalas voam.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _chama(cx, base, alt, larg, fase, ondula=0.3):
    pts = []
    for lado in (1, -1):
        rng = range(13) if lado == 1 else range(12, -1, -1)
        for k in rng:
            u = k / 12
            w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9
            pts.append((cx + lado * w + ondula * larg * math.sin(fase + 6 * u) * u, base - alt * u))
    return pts


def _labareda(T, cx, base, alt, larg, t, seed):
    sub = np.random.default_rng(seed)
    shapes = []
    for k in range(5):
        dx = sub.uniform(-larg, larg) * 0.6
        shapes.append((_chama(cx + dx, base, alt * sub.uniform(0.6, 1.0), larg * sub.uniform(0.5, 0.9), t * 9 + k), 1.0))
    return T.polys(shapes)


# =================================================================== Roy
def chuva_de_fogo(T, t, rng):
    """Bolas de fogo descem em diagonal do alto à direita, cada uma com a cauda de fogo, e explodem no
    chão em labaredas (três pontos, um depois do outro), com as brasas subindo."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    alvos = (-0.55, 0.0, 0.55)
    for k, ax in enumerate(alvos):
        t0 = 0.05 + 0.12 * k
        cai = ease_in(rel(t, t0, t0 + 0.25), 1.6)
        if 0 < cai < 1:
            x, y = ax + 0.6 * (1 - cai), 0.4 - 1.25 * (1 - cai)
            G += T.gauss(x, y, 0.06) * 1.6 + T.tapered([(x + 0.35, y - 0.6, x, y, 1.0)], 0.1) * 0.9
            H += T.gauss(x, y, 0.03) * 1.4
        boom = rel(t, t0 + 0.25, t0 + 0.7)
        if 0 < boom < 1:
            L = _labareda(T, ax, 0.45, 0.55 * ease_out(boom, 2) * (1 - 0.5 * boom), 0.16, t, 10 + k)
            G += (L * 0.8 + T.blur(L, 0.03) * 0.6) * (1 - boom * 0.6)
            H += np.clip(L - T.blur(L, 0.02) * 1.3, 0, 1) * (1 - boom) * 0.6
            G += T.gauss(ax, 0.45, 0.15, 0.06) * (1 - boom) * 1.4
            H += T.gauss(ax, 0.42, 0.06, 0.03) * pulso(boom, 0, 0.4) * 1.5
    sub = np.random.default_rng(4)
    brasas = []
    for _ in range(24):
        t0 = sub.uniform(0.3, 0.7)
        f = rel(t, t0, t0 + 0.4)
        if 0 < f < 1:
            brasas.append((sub.choice(alvos) + sub.uniform(-0.15, 0.15), 0.4 - 0.6 * f, 1 - f))
    G += T.splats(brasas, 0.012) * 1.2
    return G * env, H * env


def _circulo_salamandra(T, cx, cy, r, ang):
    """O círculo da luva do Roy: o círculo, o triângulo invertido e a chama da salamandra no meio."""
    out = T.ring(r, r * 0.06, cx, cy)
    tri = [(cx + r * 0.85 * math.cos(ang + math.pi / 2 + TAU * k / 3), cy + r * 0.85 * math.sin(ang + math.pi / 2 + TAU * k / 3)) for k in range(4)]
    out += T.polyline(tri, r * 0.06)
    out += T.polys([(_chama(cx, cy + r * 0.3, r * 0.65, r * 0.25, ang * 3), 1.0)])
    return out


def ignicao_preparo(T, t, rng):
    """O Preparo do Campo incendiado: o círculo da salamandra da luva brilha e gira devagar, e saem
    faíscas do estalo (laço)."""
    G, H = vazio(T)
    C = _circulo_salamandra(T, 0, 0, 0.42, t * TAU * 0.25)
    G += C * (0.7 + 0.3 * math.sin(TAU * t * 2)) + T.blur(C, 0.03) * 0.5
    H += C * 0.3
    sub = np.random.default_rng(int(t * 8) + 3)
    pts = [(0.4 * math.cos(a), 0.4 * math.sin(a), sub.uniform(0.3, 1)) for a in sub.uniform(0, TAU, 6)]
    G += T.splats(pts, 0.015) * 1.2
    return G, H


def campo_incendiado(T, t, rng):
    """O Campo incendiado: o rastro de fogo corre pelo chão vindo de fora, dá a volta em anel em torno do
    rival, e detona: a coluna de fogo sobe com o anel de choque."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    corre = ease_out(rel(t, 0.0, 0.45), 1.6)
    if corre > 0:
        a0 = math.pi * 0.9
        anel = T.arc_band(0.5, 0.05, a0, a0 + TAU * corre, squash=0.32, cy=0.42, taper=0.3)
        G += anel * 1.4 * (1 - rel(t, 0.55, 0.75))
        sub = np.random.default_rng(7)
        chamas = []
        for k in range(18):
            u = k / 18
            if u > corre:
                break
            a = a0 + TAU * u
            x, y = 0.5 * math.cos(a), 0.42 + 0.16 * math.sin(a)
            chamas.append((_chama(x, y, 0.12 + 0.05 * math.sin(t * 20 + k), 0.04, t * 12 + k), 1.0))
        if chamas:
            G += T.polys(chamas) * 0.9 * (1 - rel(t, 0.55, 0.75))
    explode = rel(t, 0.45, 0.9)
    if explode > 0:
        coluna = _labareda(T, 0, 0.45, 1.1 * ease_out(explode, 2) * (1 - 0.3 * explode), 0.32, t, 55)
        G += (coluna * 0.9 + T.blur(coluna, 0.04) * 0.6) * (1 - explode * 0.7)
        H += np.clip(coluna - T.blur(coluna, 0.02) * 1.3, 0, 1) * (1 - explode) * 0.8
        G += T.ring(0.1 + 0.8 * ease_out(explode, 1.6), 0.04, 0, 0.42, squash=3) * (1 - explode) * 1.3
    H += T.gauss(0, 0.2, 0.2) * pulso(t, 0.43, 0.6) * 1.6
    return G * env, H * env


# =================================================================== Griffith
def _falcao(cx, cy, s, abre, ang=0.0):
    """O falcão de cima: o corpo afilado, as asas em V e a cauda em leque."""
    corpo = [(0, -0.3), (0.05, -0.1), (0.04, 0.2), (0, 0.32), (-0.04, 0.2), (-0.05, -0.1)]
    asa_d = [(0.04, -0.08), (0.55 * abre, 0.1 - 0.25 * abre), (0.7 * abre, 0.2), (0.35, 0.05), (0.05, 0.08)]
    asa_e = [(-x, y) for x, y in asa_d]
    cauda = [(-0.04, 0.2), (-0.12, 0.42), (0, 0.38), (0.12, 0.42), (0.04, 0.2)]
    return [(_gira([(x * s, y * s) for x, y in p], ang, cx, cy), 1.0) for p in (corpo, asa_d, asa_e, cauda)]


def visao_de_falcao(T, t, rng):
    """O falcão mergulha do alto (as asas fechando para trás), a mira de quatro pontas fecha no rival, e
    as penas caem girando."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    mergulha = ease_in(rel(t, 0.0, 0.45), 1.8)
    if mergulha < 1:
        x, y = -0.5 + 0.5 * mergulha, -0.9 + 0.9 * mergulha
        F = T.polys(_falcao(x, y, 0.5, 1 - 0.7 * mergulha, -0.55 * (1 - mergulha)))
        G += F * 1.0 + T.blur(F, 0.02) * 0.4
        H += np.clip(F - T.blur(F, 0.006), 0, 1) * 0.5
        G += T.tapered([(x - 0.3, y - 0.5, x, y, 0.6)], 0.06) * mergulha
    mira = ease_out(rel(t, 0.2, 0.5), 2)
    r = 0.45 - 0.2 * mira
    segs = []
    for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
        segs.append((r * math.cos(a), r * math.sin(a), (r - 0.12) * math.cos(a), (r - 0.12) * math.sin(a), 1.0))
    G += (T.lines(segs, 0.016) + T.ring(r, 0.012)) * pulso(t, 0.15, 0.9) * 1.1
    H += T.flare(0, 0, 0.6 * pulso(t, 0.45, 0.65) + 0.01, 0.0, 0.02) * pulso(t, 0.45, 0.65)
    sub = np.random.default_rng(12)
    penas = []
    cai = rel(t, 0.45, 1.0)
    for k in range(7):
        if cai <= 0:
            break
        x = sub.uniform(-0.4, 0.4) + 0.1 * math.sin(cai * 6 + k)
        y = -0.1 + 0.6 * cai * sub.uniform(0.5, 1)
        penas.append((lamina(x - 0.05, y - 0.05, x + 0.05, y + 0.05, 0.02), 1 - cai))
    if penas:
        G += T.polys(penas) * 1.0
    return G * env, H * env


def comando_da_banda(T, t, rng):
    """A bandeira do Bando do Falcão: o mastro e o pano tremulando (as ondas passando), o falcão no meio
    do pano, e o brado sai em arcos para os lados (os aliados)."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    sobe = ease_out(rel(t, 0.0, 0.25), 2)
    mastro = T.lines([(-0.35, 0.55, -0.35, 0.55 - 1.1 * sobe, 1.0)], 0.02)
    G += mastro * 1.0
    if sobe > 0.3:
        topo = 0.55 - 1.1 * sobe
        pano = []
        for u in np.linspace(0, 1, 20):
            pano.append((-0.35 + 0.7 * u, topo + 0.05 * math.sin(u * 6 - t * 14) * u))
        baixo = [(x, y + 0.42) for x, y in pano[::-1]]
        P = T.polys([(pano + baixo, 1.0)])
        G += P * 0.45 + np.clip(P - T.blur(P, 0.008) * 1.1, 0, 1) * 0.9
        F = T.polys(_falcao(0.0, topo + 0.21 + 0.03 * math.sin(t * 14), 0.32, 0.9))
        G += F * 0.9
        H += F * 0.4
    for k in range(3):
        u = rel(t, 0.35 + 0.1 * k, 0.8 + 0.1 * k)
        if 0 < u < 1:
            for lado in (-1, 1):
                a0 = 0 if lado > 0 else math.pi
                G += T.arc_band(0.2 + 0.6 * u, 0.025, a0 - 0.6, a0 + 0.6, cy=0.0, taper=0.0) * (1 - u) * 1.1
    return G * env, H * env


def eclipse_preparo(T, t, rng):
    """O Preparo do Destino ascendente: a lua tapa o sol (o disco escuro deslizando), sobra o anel de fogo
    da coroa, pulsando (laço)."""
    G, H = vazio(T)
    G += T.ring(0.3, 0.05) * (0.8 + 0.2 * math.sin(TAU * t * 2)) + T.blur(T.ring(0.3, 0.05), 0.04) * 0.6
    sub = np.random.default_rng(5)
    raios = []
    for k in range(16):
        a = TAU * k / 16 + t * 0.6
        L = 0.38 + 0.1 * (0.5 + 0.5 * math.sin(TAU * t * 2 + k))
        raios.append((0.33 * math.cos(a), 0.33 * math.sin(a), L * math.cos(a), L * math.sin(a), 0.8))
    G += T.tapered(raios, 0.03) * 0.8
    G -= T.gauss(0, 0, 0.25) * 0.5
    H += T.ring(0.3, 0.02) * 0.5
    return G, H


def destino_ascendente(T, t, rng):
    """O Eclipse: o sol negro com a coroa de fogo no alto, as asas escuras (de morcego, as de Femto) se
    abrem por trás dele, e a onda escura desce e passa em todos."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    cy = -0.35
    surge = ease_out(rel(t, 0.0, 0.3), 2)
    coroa = T.ring(0.24, 0.045, 0, cy) * surge
    G += coroa * 1.2 + T.blur(coroa, 0.05) * 0.7
    H += T.ring(0.24, 0.015, 0, cy) * surge * 0.7
    G -= T.gauss(0, cy, 0.17) * surge * 0.6
    abre = back(rel(t, 0.2, 0.5), 1.3)
    if abre > 0:
        membrana = []
        ossos = T.zero()
        for lado in (-1, 1):
            ombro = (0.2 * lado, cy - 0.02)
            pontas = []
            for k in range(5):
                a = (-0.15 - 0.42 * k) if lado > 0 else (math.pi + 0.15 + 0.42 * k)
                comp = (0.85 - 0.08 * k) * abre
                pontas.append((ombro[0] + comp * math.cos(a), ombro[1] + comp * math.sin(a) * 0.75 + 0.05 * k * abre))
            for (x, y) in pontas:
                ossos += T.polyline([ombro, (x, y)], 0.014)
            borda = [ombro, pontas[0]]
            for k in range(4):
                (x1, y1), (x2, y2) = pontas[k], pontas[k + 1]
                for u in np.linspace(0.15, 0.85, 6):
                    mx, my = x1 + (x2 - x1) * u, y1 + (y2 - y1) * u
                    puxa = 0.28 * math.sin(math.pi * u)
                    borda.append((mx + (ombro[0] - mx) * puxa, my + (ombro[1] - my) * puxa))
                borda.append((x2, y2))
            membrana.append((borda, 1.0))
        A = T.polys(membrana)
        contorno = np.clip(A - T.blur(A, 0.008) * 1.1, 0, 1)
        G += contorno * 1.8 + ossos * 1.2 + A * 0.25 + T.blur(A, 0.05) * 0.3
        H += contorno * 0.4 + ossos * 0.3
    onda = rel(t, 0.5, 0.95)
    if onda > 0:
        G += T.ring(0.1 + 1.1 * ease_out(onda, 1.6), 0.07, 0, cy) * (1 - onda) * 1.2
    return G * env, H * env


# =================================================================== Jotaro
def precisao_absoluta(T, t, rng):
    """O dedo estelar: a estocada finíssima e muito rápida vem da esquerda, deixa estrelinhas no rastro e
    acerta o ponto exato (o anel pequeno e o clarão em estrela)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.1, 0.3), 2.5)
    if 0.1 < t < 0.6:
        hx = -0.9 + 0.9 * vem
        L = T.polys([(lamina(-0.95, 0.05, hx, 0.0, 0.05, 1.0, rel(t, 0.32, 0.55)), 1.0)])
        G += L * 1.4 + T.blur(L, 0.015) * 0.5
        H += L * 0.9
    sub = np.random.default_rng(9)
    estrelas = []
    for k in range(7):
        x = -0.8 + 0.12 * k
        f = rel(t, 0.15 + 0.02 * k, 0.6 + 0.02 * k)
        if 0 < f < 1:
            estrelas.append((estrela(x, 0.03 + sub.uniform(-0.12, 0.12) * f, 0.065 * (1 - f) + 0.015, t * 6, 5, 0.45), 1 - f))
    if estrelas:
        G += T.polys(estrelas) * 1.2
    acerta = pulso(t, 0.28, 0.6)
    G += T.ring(0.12 + 0.3 * rel(t, 0.28, 0.6), 0.02) * acerta * 1.4 + T.gauss(0, 0, 0.12) * acerta * 1.2
    H += (T.polys([(estrela(0, 0, 0.32 * acerta + 0.01, 0.3, 5, 0.3), 1.0)]) * 1.2 + T.flare(0, 0, 0.8 * acerta + 0.01, 0.0, 0.015)) * acerta
    return G * env, H * env


def star_preparo(T, t, rng):
    """O Preparo do The World: a aura do Star Platinum sobe e as estrelas giram em volta (laço)."""
    G, H = vazio(T)
    G += T.gauss(0, 0.05, 0.28, 0.45) * (0.6 + 0.2 * math.sin(TAU * t * 2))
    shapes = []
    for k in range(6):
        a = TAU * (k / 6 + t)
        shapes.append((estrela(0.42 * math.cos(a), 0.05 + 0.3 * math.sin(a), 0.06, a * 2, 5, 0.45), 0.8 + 0.2 * math.sin(a)))
    S = T.polys(shapes)
    G += S * 1.1
    H += S * 0.5
    return G, H


def the_world_jotaro(T, t, rng):
    """O tempo para: a bolha cresce do centro e tudo dentro dela inverte (o anel claro e o miolo
    escurecido), as estrelas ficam paradas no ar, e quando o tempo volta os golpes caem todos juntos."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    cresce = ease_out(rel(t, 0.0, 0.35), 2)
    some = 1 - rel(t, 0.55, 0.65)
    if cresce > 0:
        r = 0.1 + 0.9 * cresce
        G += T.ring(r, 0.03) * 1.3 * some
        dentro = (T.RAD < r).astype(np.float32)
        G += dentro * 0.18 * some
        H += T.ring(r, 0.01) * 0.6 * some
    sub = np.random.default_rng(3)
    estrelas = [(estrela(sub.uniform(-0.7, 0.7), sub.uniform(-0.6, 0.6), 0.04, sub.uniform(0, 1), 5, 0.45), 1.0) for _ in range(9)]
    G += T.polys(estrelas) * pulso(t, 0.15, 0.62) * 1.0
    volta = rel(t, 0.6, 0.9)
    if volta > 0:
        for k, (x, y) in enumerate(((-0.5, -0.1), (0.0, 0.1), (0.5, -0.05))):
            u = rel(t, 0.6 + 0.03 * k, 0.85 + 0.03 * k)
            G += T.gauss(x, y, 0.1 + 0.1 * u) * (1 - u) * 1.6 * (u > 0)
            H += T.flare(x, y, 0.5 * (1 - u) + 0.01, 0.4, 0.02) * (1 - u) * (u > 0)
    return G * env, H * env


# =================================================================== Dio
def _faca(cx, cy, ang, comp=0.2):
    c, s = math.cos(ang), math.sin(ang)
    lam = lamina(cx, cy, cx + c * comp, cy + s * comp, 0.025)
    cabo = [(cx - c * 0.07 - s * 0.012, cy - s * 0.07 + c * 0.012), (cx - s * 0.012, cy + c * 0.012), (cx + s * 0.012, cy - c * 0.012), (cx - c * 0.07 + s * 0.012, cy - s * 0.07 - c * 0.012)]
    guarda = [(cx - s * 0.04, cy + c * 0.04), (cx - s * 0.04 + c * 0.01, cy + c * 0.04 + s * 0.01), (cx + s * 0.04 + c * 0.01, cy - c * 0.04 + s * 0.01), (cx + s * 0.04, cy - c * 0.04)]
    return [(lam, 1.0), (cabo, 0.8), (guarda, 1.0)]


def facas_do_dio(T, t, rng):
    """As facas aparecem paradas no ar em leque em volta do rival (o tempo parado, elas tremem de leve), e
    de repente todas voam juntas e cravam no centro, com o brilho."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    aparece = rel(t, 0.0, 0.35)
    voa = ease_in(rel(t, 0.45, 0.62), 2)
    shapes = []
    n = 10
    for k in range(n):
        if k / n > aparece * 1.2:
            continue
        a = math.pi * 1.05 + math.pi * 0.9 * k / (n - 1)
        r = 0.75 * (1 - voa) + 0.12
        x, y = r * math.cos(a), 0.15 + r * math.sin(a) * 0.9
        treme = 0.005 * math.sin(t * 80 + k) * (1 - voa)
        ang = math.atan2(0.15 - y, -x)
        shapes += _faca(x + treme, y, ang)
    if shapes and t < 0.75:
        F = T.polys(shapes)
        G += F * 1.0 + T.blur(F, 0.015) * 0.4
        H += np.clip(F - T.blur(F, 0.005), 0, 1) * 0.7
    crava = pulso(t, 0.6, 0.9)
    G += T.gauss(0, 0.15, 0.12) * crava * 1.5
    H += T.flare(0, 0.15, 0.7 * crava + 0.01, 0.3, 0.015) * crava
    return G * env, H * env


def _mostrador(T, cx, cy, r, ponteiro):
    out = T.ring(r, r * 0.04, cx, cy)
    marcas = []
    for k in range(12):
        a = TAU * k / 12
        marcas.append((cx + r * 0.85 * math.cos(a), cy + r * 0.85 * math.sin(a), cx + r * 0.97 * math.cos(a), cy + r * 0.97 * math.sin(a), 1.0))
    out += T.lines(marcas, r * 0.05)
    out += T.lines([(cx, cy, cx + r * 0.75 * math.cos(ponteiro), cy + r * 0.75 * math.sin(ponteiro), 1.0),
                    (cx, cy, cx + r * 0.5 * math.cos(ponteiro / 12), cy + r * 0.5 * math.sin(ponteiro / 12), 1.0)], r * 0.05)
    return out


def za_warudo_preparo(T, t, rng):
    """O Preparo do O Mundo: o relógio dourado batendo — os ponteiros andam aos saltos e o mostrador pulsa
    a cada tique (laço)."""
    G, H = vazio(T)
    tique = math.floor(t * 4) / 4
    M = _mostrador(T, 0, 0, 0.42, -math.pi / 2 + TAU * tique)
    bate = math.exp(-((t * 4) % 1) * 6)
    G += M * (0.8 + 0.4 * bate) + T.blur(M, 0.03) * 0.4
    H += M * 0.3 * bate
    return G, H


def _rolo(cx, cy, s):
    """O rolo compressor de lado: a cabine, o tambor da frente e a roda de trás."""
    cabine = [(cx - 0.35 * s, cy - 0.25 * s), (cx + 0.05 * s, cy - 0.25 * s), (cx + 0.1 * s, cy + 0.05 * s), (cx - 0.4 * s, cy + 0.05 * s)]
    corpo = [(cx - 0.45 * s, cy + 0.05 * s), (cx + 0.5 * s, cy + 0.05 * s), (cx + 0.5 * s, cy + 0.2 * s), (cx - 0.45 * s, cy + 0.2 * s)]
    return [(cabine, 1.0), (corpo, 1.0)]


def za_warudo(T, t, rng):
    """O Mundo: a esfera dourada cresce com o mostrador do relógio (os ponteiros param), tudo fica parado,
    e o rolo compressor cai do alto e esmaga o rival, com o estrondo e as rachaduras."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    cresce = ease_out(rel(t, 0.0, 0.3), 2)
    some = 1 - rel(t, 0.45, 0.55)
    if cresce > 0:
        G += (T.ring(0.15 + 0.85 * cresce, 0.04) * 1.2 + T.gauss(0, 0, 0.9 * cresce + 0.01) * 0.15) * some
        para = min(1.0, rel(t, 0.1, 0.35))
        M = _mostrador(T, 0, 0, 0.35 * cresce + 0.01, -math.pi / 2 + 4 * (1 - para))
        G += M * 0.9 * some
        H += M * 0.3 * some
    cai = ease_in(rel(t, 0.45, 0.62), 2.2)
    if 0.45 < t < 0.95:
        y = -1.0 + 0.95 * cai
        R = T.polys(_rolo(0, y, 1.0))
        tambor = T.ring(0.13, 0.02, 0.32, y + 0.2) + T.ring(0.11, 0.02, -0.3, y + 0.22)
        G += (R * 0.7 + np.clip(R - T.blur(R, 0.008) * 1.1, 0, 1) * 0.9 + tambor * 1.1) * (1 - rel(t, 0.8, 0.95))
    impacto = rel(t, 0.62, 0.95)
    if impacto > 0:
        G += T.ring(0.1 + 0.8 * ease_out(impacto, 1.6), 0.05, 0, 0.2, squash=2.0) * (1 - impacto) * 1.3
        q = np.random.default_rng(31)
        for k in range(6):
            a = math.pi * (0.1 + 0.8 * k / 5)
            G += T.polyline(jagged(q, 0, 0.3, 0.7 * impacto * math.cos(a), 0.3 + 0.2 * impacto * math.sin(a), 3, 0.3), 0.012) * (1 - rel(t, 0.85, 1))
        H += T.gauss(0, 0.2, 0.15) * pulso(impacto, 0, 0.3) * 1.6
    return G * env, H * env


# =================================================================== Giorno
def _joaninha(T, cx, cy, s):
    corpo = T.gauss(cx, cy, 0.09 * s, 0.1 * s)
    linha = T.lines([(cx, cy - 0.1 * s, cx, cy + 0.1 * s, 1.0)], 0.012 * s)
    pintas = sum(T.gauss(cx + dx * s, cy + dy * s, 0.018 * s) for dx, dy in ((-0.04, -0.03), (0.04, -0.03), (-0.045, 0.04), (0.045, 0.04)))
    return np.clip(corpo * 1.5, 0, 1), linha, pintas


def reflexo_de_dano(T, t, rng):
    """A Gold Experience: as vinhas douradas brotam do chão e sobem em curva, viram um escudo de folhas
    em volta do aliado, a joaninha brilha no meio, e o dano volta em faíscas para fora."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    cresce = ease_out(rel(t, 0.0, 0.45), 1.7)
    folhas = []
    for k in range(8):
        lado = 1 if k % 2 else -1
        a0 = math.pi / 2 + lado * (0.3 + 0.25 * (k // 2))
        pts = []
        for u in np.linspace(0, cresce, 16):
            a = a0 + lado * u * 2.2
            r = 0.5 + 0.05 * math.sin(u * 8)
            pts.append((r * math.cos(a), 0.05 + r * math.sin(a) * 0.9))
        if len(pts) > 1:
            G += T.polyline(pts, 0.016) * 1.0
            for j in range(2, len(pts), 4):
                x, y = pts[j]
                ang = math.atan2(y, x)
                folhas.append((lamina(x, y, x + 0.12 * math.cos(ang + 0.6 * lado), y + 0.12 * math.sin(ang + 0.6 * lado), 0.035), 1.0))
    if folhas:
        F = T.polys(folhas)
        G += F * 0.9
        H += np.clip(F - T.blur(F, 0.005), 0, 1) * 0.4
    corpo, linha, pintas = _joaninha(T, 0, 0.0, 1.3)
    brilha = pulso(t, 0.3, 0.95)
    G += (corpo * 0.9 - pintas * 0.5) * brilha
    H += (linha * 0.6 + T.flare(0, 0, 0.4 * brilha + 0.01, 0.0, 0.03)) * brilha
    volta = rel(t, 0.55, 0.9)
    if volta > 0:
        raios = [(0.4 * math.cos(a), 0.4 * math.sin(a), (0.5 + 0.4 * volta) * math.cos(a), (0.5 + 0.4 * volta) * math.sin(a), 1 - volta) for a in np.linspace(0, TAU, 12, endpoint=False)]
        G += T.tapered(raios, 0.035) * 1.2
    return G * env, H * env


def ouro_preparo(T, t, rng):
    """O Preparo da Experiência dourada: a aura dourada pulsa e a joaninha brilha no meio (laço)."""
    G, H = vazio(T)
    pulsa = 0.5 + 0.5 * math.sin(TAU * t * 2)
    G += T.gauss(0, 0, 0.35, 0.45) * (0.5 + 0.3 * pulsa)
    corpo, linha, pintas = _joaninha(T, 0, 0, 1.6)
    G += corpo * 0.9 - pintas * 0.4
    H += linha * 0.5 + T.ring(0.25 + 0.1 * pulsa, 0.012) * 0.6
    return G, H


def _flor(cx, cy, r, ang, abre):
    petalas = []
    for k in range(5):
        a = ang + TAU * k / 5
        petalas.append((lamina(cx, cy, cx + r * abre * math.cos(a), cy + r * abre * math.sin(a), r * 0.35 * abre), 1.0))
    return petalas


def experiencia_dourada(T, t, rng):
    """A vida criada: flores de cinco pétalas desabrocham em volta (uma depois da outra), a luz dourada
    sobe em coluna suave, e as pétalas voam para cima."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    sub = np.random.default_rng(21)
    flores = []
    miolos = []
    for k in range(9):
        a = TAU * k / 9 + 0.2
        r = 0.55 + 0.1 * (k % 2)
        cx, cy = r * math.cos(a), 0.1 + r * math.sin(a) * 0.6
        t0 = 0.05 + 0.05 * k
        abre = back(rel(t, t0, t0 + 0.25), 1.4)
        if abre > 0:
            flores += _flor(cx, cy, 0.15, sub.uniform(0, TAU), abre)
            miolos.append((cx, cy, 1.0))
    if flores:
        F = T.polys(flores)
        G += F * 0.8 + np.clip(F - T.blur(F, 0.006), 0, 1) * 0.6
        H += T.splats(miolos, 0.015) * 1.2
    luz = pulso(t, 0.3, 1.0)
    G += np.exp(-(T.U / 0.45) ** 2) * np.clip(0.6 - T.V, 0, 1.2) * luz * 0.4
    voa = []
    for _ in range(14):
        t0 = sub.uniform(0.4, 0.7)
        f = rel(t, t0, t0 + 0.4)
        if 0 < f < 1:
            voa.append((sub.uniform(-0.6, 0.6) + 0.1 * math.sin(f * 7), 0.3 - 0.8 * f, 1 - f))
    G += T.splats(voa, 0.018) * 1.0
    return G * env, H * env


REGISTRO = [
    ("chuva_de_fogo", chuva_de_fogo, GRANDE, "Roy · as bolas de fogo caindo e as labaredas", False),
    ("ignicao_preparo", ignicao_preparo, MEDIA, "Roy · o círculo da salamandra na luva (Preparo, laço)", True),
    ("campo_incendiado", campo_incendiado, GRANDE, "Roy · o anel de fogo e a coluna que detona", False),
    ("visao_de_falcao", visao_de_falcao, GRANDE, "Griffith · o falcão mergulhando e a mira", False),
    ("comando_da_banda", comando_da_banda, GRANDE, "Griffith · a bandeira do Bando do Falcão", False),
    ("eclipse_preparo", eclipse_preparo, MEDIA, "Griffith · o eclipse se formando (Preparo, laço)", True),
    ("destino_ascendente", destino_ascendente, GRANDE, "Griffith · o sol negro e as asas de Femto", False),
    ("precisao_absoluta", precisao_absoluta, GRANDE, "Jotaro · o dedo estelar e as estrelinhas", False),
    ("star_preparo", star_preparo, MEDIA, "Jotaro · a aura e as estrelas (Preparo, laço)", True),
    ("the_world_jotaro", the_world_jotaro, GRANDE, "Jotaro · a bolha do tempo parado e os golpes", False),
    ("facas_do_dio", facas_do_dio, GRANDE, "Dio · as facas paradas no ar que voam juntas", False),
    ("za_warudo_preparo", za_warudo_preparo, MEDIA, "Dio · o relógio dourado batendo (Preparo, laço)", True),
    ("za_warudo", za_warudo, GRANDE, "Dio · a esfera do relógio e o rolo compressor", False),
    ("reflexo_de_dano", reflexo_de_dano, GRANDE, "Giorno · as vinhas, as folhas e a joaninha", False),
    ("ouro_preparo", ouro_preparo, MEDIA, "Giorno · a aura dourada e a joaninha (Preparo, laço)", True),
    ("experiencia_dourada", experiencia_dourada, GRANDE, "Giorno · as flores desabrochando e a luz", False),
]
