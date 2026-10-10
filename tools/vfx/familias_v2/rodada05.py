"""Rodada 5 das habilidades próprias: Tanjiro, Nezuko, Zenitsu, Inosuke e Muzan (Demon Slayer).

Tanjiro
- olfato_tanjiro: o "fio da abertura" — o cheiro vira um fio vermelho que serpenteia até o ponto
  fraco do rival, o ponto acende e o fio estica e vibra.
- respiracao_da_agua: a Roda d'Água — o corte gira num círculo inteiro de água, com as ondas
  curvas do desenho japonês (as cristas enroladas) e a espuma espirrando.
- hinokami_preparo: o Preparo da Dança do Deus do Fogo — as chamas sobem em volta da lâmina e a
  brasa gira (laço).
- hinokami_kagura: a Dança do Deus do Fogo — o arco de fogo enorme gira em volta do rival como o
  halo do sol, a lâmina corta e as chamas sobem em línguas.

Nezuko
- sangue_nezuko: o chute demoníaco — o pé desce com o rastro rosa, o impacto e as gotas de sangue.
- explosao_de_sangue: a Arte do Sangue Explosivo — as gotas no rival acendem e explodem em chamas
  rosa, uma depois da outra.
- despertar_nezuko: a forma desperta — as vinhas da marca crescem pelo corpo, o chifre, a aura
  rosa e o chute.

Zenitsu
- audicao_zenitsu: a audição — as ondas de som saem do ouvido em arcos, acham o rival e o raio
  amarelo corta num risco só.
- primeira_postura: a Primeira Postura no aliado — o relâmpago em zigue-zague chega e vira uma
  cúpula elétrica dourada em volta dele.
- seis_dobras: as Seis Dobras — seis riscos de raio em zigue-zague de seis lados diferentes, um
  depois do outro, e o clarão que paralisa.

Inosuke
- percepcao_espacial: a pele que sente — as vibrações em linhas finas espalhando do chão, acham
  o rival (o ponto pisca) e o golpe corta o Preparo.
- presas_rasgantes: as Presas — duas lâminas lascadas (dentes de serra) cruzam em X e rasgam.
- investida_inosuke: a investida do javali — a cabeça do javali avança com a poeira e os cortes
  loucos em todas as direções.

Muzan
- chicotes_de_carne: os chicotes de carne saem do chão com espinhos e estalam no rival.
- sangue_corruptor: o sangue de Muzan — as veias escuras se espalham pelo rival a partir do furo
  e pulsam.
- adaptacao_demoniaca: a carne se adapta — os tentáculos fecham o corpo, as bocas e o olho de
  demônio acendem e o pulso vermelho.
"""
from __future__ import annotations

import math

import numpy as np

from .base import GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, janela, lamina, pulso, rel, vazio


def _quadro(t, seed=0):
    return np.random.default_rng(seed + int(t * 997) % 9973)


def _faiscas(T, t, seed, n, t0, alcance=0.7, tam=0.012, cx=0.0, cy=0.0, a0=0.0, a1=TAU):
    sub = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        a = sub.uniform(a0, a1)
        d = 0.08 + alcance * ease_out(rel(t, t0, t0 + 0.5), 2) * sub.uniform(0.3, 1)
        pts.append((cx + d * math.cos(a), cy + d * math.sin(a), pulso(t, t0, 0.9) * sub.uniform(0.4, 1)))
    return T.splats(pts, tam)


def _chama(cx, base, alt, larg, fase, ondula=0.3):
    pts = []
    for lado in (1, -1):
        rng = range(13) if lado == 1 else range(12, -1, -1)
        for k in rng:
            u = k / 12
            w = larg * math.sin(math.pi * u) ** 0.6 * (1 - u) ** 0.9
            pts.append((cx + lado * w + ondula * larg * math.sin(fase + 6 * u) * u, base - alt * u))
    return pts


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _raio(T, q, x1, y1, x2, y2, larg=0.012, depth=4, rough=0.3):
    return T.polyline(jagged(q, x1, y1, x2, y2, depth, rough), larg)


# =================================================================== Tanjiro
def olfato_tanjiro(T, t, rng):
    """O fio da abertura: o cheiro vem de fora como um fio vermelho que serpenteia até o rival, o
    ponto fraco acende (o anel que fecha) e o fio fica esticado, vibrando, antes de sumir."""
    G, H = vazio(T)
    vem = ease_out(rel(t, 0.0, 0.4), 1.6)
    env = apaga(t, 0.82, 1)
    pts = []
    n = 40
    for k in range(n):
        u = k / (n - 1)
        if u > vem:
            break
        x = -0.95 + 1.0 * u
        ond = 0.12 * math.sin(u * 10 + t * 8) * (1 - u) * (1 - rel(t, 0.4, 0.55))
        pts.append((x, -0.35 + 0.42 * u + ond))
    fio = T.polyline(pts, 0.012) if len(pts) > 1 else T.zero()
    alvo = (0.05, 0.07)
    acende = pulso(t, 0.35, 0.85)
    anel = T.ring(0.2 * (1 - 0.6 * ease_out(rel(t, 0.35, 0.55), 2)) + 0.05, 0.015, *alvo) * acende
    ponto = T.gauss(*alvo, 0.03, 0.03) * acende * 1.5
    cheiro = []
    sub = np.random.default_rng(3)
    for k in range(10):
        f = (sub.uniform() + t * 1.2) % 1
        cheiro.append((-0.9 + 0.9 * f + sub.uniform(-0.05, 0.05), -0.4 + 0.45 * f + 0.1 * math.sin(f * 9 + k), math.sin(math.pi * f) * 0.6))
    G += (fio * 1.3 + T.blur(fio, 0.02) * 0.6 + anel * 1.2 + ponto + T.splats(cheiro, 0.02) * 0.4) * env
    H += (fio * 0.6 + ponto * 1.2 + T.flare(*alvo, 0.3 * acende + 0.01, thin=0.02) * acende) * env
    return G, H


def _onda_japonesa(cx, cy, r, a0, larg):
    """A crista enrolada da onda (o desenho japonês): um gancho que curva para dentro."""
    pts = []
    for u in np.linspace(0, 1, 18):
        a = a0 + u * 4.2
        rr = r * (1 - 0.75 * u)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def respiracao_da_agua(T, t, rng):
    """A Roda d'Água: o corte de água dá a volta inteira em torno do rival (a lâmina abrindo o
    círculo), as cristas das ondas se enrolam na borda, a espuma espirra e a água escorre."""
    G, H = vazio(T)
    gira = ease_out(rel(t, 0.05, 0.5), 1.8)
    env = apaga(t, 0.78, 1)
    a0 = -math.pi / 2
    roda = T.arc_band(0.55, 0.07, a0, a0 + TAU * gira + 0.01, taper=0.4) if gira > 0 else T.zero()
    fio = T.arc_band(0.55, 0.018, a0, a0 + TAU * gira + 0.01) if gira > 0 else T.zero()
    cristas = T.zero()
    for k in range(8):
        a = a0 + TAU * k / 8
        if (k / 8) > gira:
            continue
        cx, cy = 0.55 * math.cos(a), 0.55 * math.sin(a)
        cristas += T.polyline(_onda_japonesa(cx + 0.08 * math.cos(a), cy + 0.08 * math.sin(a), 0.11, a + 1.0, 0.02), 0.016) * (1 - rel(t, 0.6, 0.8))
    espuma = []
    sub = np.random.default_rng(14)
    for _ in range(30):
        a = sub.uniform(0, TAU)
        d = 0.55 + 0.3 * ease_out(rel(t, 0.3, 0.8), 2) * sub.uniform(0.2, 1)
        espuma.append((d * math.cos(a), d * math.sin(a) + 0.15 * rel(t, 0.5, 1.0), pulso(t, 0.3, 0.95) * sub.uniform(0.3, 1)))
    corte = T.polys([(lamina(-0.5, 0.35, 0.5, -0.35, 0.05, prog=ease_out(rel(t, 0.42, 0.55), 2), inicio=rel(t, 0.6, 0.75)), 1.0)], 0.006)
    G += (roda * 1.1 + T.blur(roda, 0.03) * 0.5 + cristas * 1.1 + T.splats(espuma, 0.013) + corte * 1.2) * env
    H += (fio * 1.3 + cristas * 0.5 + T.splats(espuma, 0.006) + corte * 0.8) * env
    return G, H


def hinokami_preparo(T, t, rng):
    """O Preparo da Dança do Deus do Fogo: as chamas sobem em volta da lâmina erguida, a brasa gira em
    círculo e o calor tremula (laço)."""
    G, H = vazio(T)
    fase = t * TAU
    chamas = []
    for k in range(9):
        x = -0.35 + 0.7 * k / 8
        alt = (0.5 + 0.2 * math.sin(fase * 2 + k * 1.7)) * (1 - abs(x) * 0.9)
        chamas.append((_chama(x, 0.4, alt, 0.1, fase * 2 + k, 0.4), 0.8))
    C = T.polys(chamas, 0.015)
    brasas = [(0.35 * math.cos(fase + k * TAU / 8), -0.05 + 0.35 * math.sin(fase + k * TAU / 8) * 0.5, 0.8) for k in range(8)]
    lam = T.polys([(lamina(0.0, 0.3, 0.0, -0.6, 0.03), 1.0)], 0.004)
    G += C * 0.9 + T.splats(brasas, 0.016) + lam * 0.6
    H += C * 0.15 + T.splats(brasas, 0.008) + lam * 0.8
    return G, H


def hinokami_kagura(T, t, rng):
    """A Dança do Deus do Fogo: o arco de fogo nasce e dá a volta no rival como o halo do sol (largo,
    com as línguas de chama saindo para fora), a lâmina corta na diagonal por dentro do halo e a
    explosão de brasas sobe."""
    G, H = vazio(T)
    gira = ease_out(rel(t, 0.0, 0.45), 1.7)
    env = apaga(t, 0.8, 1)
    a0 = math.pi * 0.75
    halo = T.arc_band(0.6, 0.09, a0, a0 + TAU * gira + 0.01, taper=0.5) if gira > 0 else T.zero()
    linguas = []
    for k in range(18):
        a = a0 + TAU * k / 18
        if k / 18 > gira:
            continue
        x, y = 0.6 * math.cos(a), 0.6 * math.sin(a)
        alt = 0.16 + 0.06 * math.sin(t * 30 + k)
        pts = _gira(_chama(0, 0, alt, 0.05, t * 20 + k, 0.5), a + math.pi / 2, x, y)
        linguas.append((pts, 0.8 * (1 - rel(t, 0.65, 0.9))))
    L = T.polys(linguas, 0.01)
    corte = T.polys([(lamina(-0.55, -0.45, 0.55, 0.45, 0.07, prog=ease_out(rel(t, 0.4, 0.52), 2), inicio=rel(t, 0.6, 0.78)), 1.0)], 0.008)
    fio = T.polys([(lamina(-0.55, -0.45, 0.55, 0.45, 0.02, prog=ease_out(rel(t, 0.4, 0.52), 2), inicio=rel(t, 0.6, 0.78)), 1.0)], 0.003)
    sobe = []
    sub = np.random.default_rng(21)
    for _ in range(26):
        f = rel(t, 0.45, 1.0)
        x = sub.uniform(-0.5, 0.5)
        sobe.append((x + 0.05 * math.sin(f * 8 + x * 9), 0.3 - 0.9 * f * sub.uniform(0.5, 1), math.sin(math.pi * f) * sub.uniform(0.4, 1)))
    G += (halo * 1.2 + T.blur(halo, 0.04) * 0.6 + L + corte * 1.3 + T.splats(sobe, 0.014) + T.gauss(0, 0, 0.3, 0.3) * pulso(t, 0.42, 0.62) * 0.7) * env
    H += (halo * 0.35 + fio * 1.5 + T.splats(sobe, 0.006)) * env
    return G, H


# =================================================================== Nezuko
def sangue_nezuko(T, t, rng):
    """O chute demoníaco: o pé desce do alto com o rastro rosa em arco, o impacto estoura com o
    anel e as gotas de sangue espirram e caem."""
    G, H = vazio(T)
    desce = ease_in(rel(t, 0.0, 0.3), 1.8)
    env = apaga(t, 0.8, 1)
    a = -math.pi * 0.85 + math.pi * 0.6 * desce
    px, py = 0.55 * math.cos(a) + 0.0, 0.55 * math.sin(a) + 0.4
    rastro = T.arc_band(0.55, 0.06, -math.pi * 0.85, a + 0.01, cy=0.4, taper=0.3) * (1 - rel(t, 0.3, 0.5)) if desce > 0 else T.zero()
    pe = T.polys([(lamina(px - 0.08, py - 0.06, px + 0.1, py + 0.06, 0.06), 1.0)], 0.01) * (1 - rel(t, 0.3, 0.38))
    bate = pulso(t, 0.28, 0.6)
    anel = T.ring(0.1 + 0.55 * ease_out(rel(t, 0.28, 0.6), 2), 0.03) * (1 - rel(t, 0.28, 0.65))
    gotas = []
    sub = np.random.default_rng(9)
    for _ in range(18):
        ang = sub.uniform(0, TAU)
        f = rel(t, 0.3, 0.95)
        d = 0.1 + 0.55 * ease_out(f, 2) * sub.uniform(0.4, 1)
        gotas.append((d * math.cos(ang), d * math.sin(ang) + 0.4 * f * f, (1 - f) * sub.uniform(0.5, 1)))
    G += (rastro * 1.2 + pe + T.gauss(0, 0, 0.25, 0.25) * bate + anel * 1.2 + T.splats(gotas, 0.016)) * env
    H += (rastro * 0.4 + T.flare(0, 0, 0.6 * bate + 0.01, thin=0.02) * bate + T.splats(gotas, 0.007) * 0.8) * env
    return G, H


def explosao_de_sangue(T, t, rng):
    """A Arte do Sangue Explosivo: as gotas de sangue grudam no rival e acendem uma depois da outra,
    cada uma estoura numa chama rosa que sobe, e o fogo fica queimando."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    sub = np.random.default_rng(31)
    gotas = [(sub.uniform(-0.4, 0.4), sub.uniform(-0.35, 0.35)) for _ in range(7)]
    for k, (x, y) in enumerate(gotas):
        t0 = 0.1 + 0.06 * k
        cola = rel(t, 0.0, t0)
        G += T.gauss(x, y, 0.03, 0.03) * cola * (1 - rel(t, t0, t0 + 0.05)) * 1.5
        ex = rel(t, t0, t0 + 0.35)
        if ex > 0:
            G += T.ring(0.03 + 0.2 * ease_out(ex, 2), 0.02, x, y) * (1 - ex) * 1.2
            G += T.gauss(x, y, 0.08 + 0.06 * ex, None) * (1 - ex) * 1.2
            H += T.gauss(x, y, 0.04, None) * (1 - ex) ** 2 * 1.5
    chamas = []
    for k in range(10):
        x = -0.45 + 0.1 * k
        alt = (0.35 + 0.12 * math.sin(t * 25 + k * 1.7)) * pulso(t, 0.3, 1.0)
        chamas.append((_chama(x, 0.45, alt, 0.07, t * 20 + k, 0.4), 0.8))
    C = T.polys(chamas, 0.012)
    G += C * env
    H += C * 0.15 * env
    return G, H


def despertar_nezuko(T, t, rng):
    """A forma desperta: as vinhas da marca crescem em espiral pelo corpo (os galhos se abrindo), o
    chifre aparece em cima, a aura rosa sobe e o chute desperto estoura no rival."""
    G, H = vazio(T)
    cresce = ease_out(rel(t, 0.0, 0.4), 1.6)
    env = apaga(t, 0.82, 1)
    vinhas = T.zero()
    for k in range(5):
        a0 = TAU * k / 5
        pts = []
        for u in np.linspace(0, cresce, 16):
            a = a0 + u * 3.0
            r = 0.1 + 0.45 * u
            pts.append((r * math.cos(a), r * math.sin(a) * 0.9))
        if len(pts) > 1:
            vinhas += T.polyline(pts, 0.014)
            for j in range(2, len(pts) - 1, 4):
                x, y = pts[j]
                vinhas += T.polys([(lamina(x, y, x * 1.2 + 0.05, y * 1.2 - 0.06, 0.015), 1.0)], 0.004) * 0.8
    chifre = T.polys([(lamina(0.08, -0.32, 0.18, -0.62, 0.035), 1.0)], 0.006) * rel(t, 0.25, 0.35)
    aura = T.gauss(0, -0.05, 0.38, 0.55) * pulso(t, 0.2, 0.9) * 0.6
    bate = pulso(t, 0.5, 0.75)
    anel = T.ring(0.1 + 0.6 * ease_out(rel(t, 0.5, 0.8), 2), 0.035) * (1 - rel(t, 0.5, 0.82))
    G += (vinhas * 1.1 + chifre + aura + anel * 1.2 + T.gauss(0, 0, 0.2, 0.2) * bate) * env
    H += (vinhas * 0.4 + T.flare(0, 0, 0.7 * bate + 0.01, thin=0.02) * bate) * env
    G += _faiscas(T, t, 5, 16, 0.5, 0.7) * env
    return G, H


# =================================================================== Zenitsu
def audicao_zenitsu(T, t, rng):
    """A audição do Zenitsu: as ondas de som saem em arcos (vindo de longe, do lado), acham o rival
    — os arcos se fecham nele — e o raio amarelo corta num risco só, de lado a lado."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    ondas = T.zero()
    for k in range(4):
        f = rel(t, 0.0 + 0.06 * k, 0.4 + 0.06 * k)
        if 0 < f < 1:
            ondas += T.arc_band(0.9 * (1 - f) + 0.08, 0.02, math.pi * 0.7, math.pi * 1.3, cx=0.0) * (1 - f) * 1.2
    q = _quadro(t, 5)
    risco = rel(t, 0.42, 0.5)
    R = _raio(T, q, -0.9, 0.12, -0.9 + 1.8 * risco, -0.12, 0.016, 5, 0.25) * (1 - rel(t, 0.55, 0.75)) if risco > 0 else T.zero()
    cl = pulso(t, 0.46, 0.66)
    G += (ondas + R * 1.3 + T.blur(R, 0.03) * 0.8 + T.gauss(0, 0, 0.3, 0.2) * cl * 0.8) * env
    H += (R * 1.4 + T.flare(0, 0, 0.7 * cl + 0.01, ang=-0.13, thin=0.015) * cl) * env
    G += _faiscas(T, t, 17, 14, 0.48, 0.6, 0.01) * env
    return G, H


def primeira_postura(T, t, rng):
    """A Primeira Postura no aliado: o relâmpago chega em zigue-zague de lado, bate nele e vira uma
    cúpula elétrica dourada com os raios correndo pela borda; fica e se desfaz em faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    q = _quadro(t, 11)
    chega = rel(t, 0.0, 0.2)
    R = _raio(T, q, -0.95, -0.4, -0.95 + 0.95 * chega, -0.4 + 0.4 * chega, 0.015, 4, 0.35) * (1 - rel(t, 0.2, 0.32)) if chega > 0 else T.zero()
    forma = ease_out(rel(t, 0.18, 0.4), 2)
    cupula = T.ring(0.55 * forma + 0.01, 0.03, 0, 0.0, squash=1.0) * rel(t, 0.18, 0.22)
    dentro = T.gauss(0, 0, 0.5 * forma + 0.01, None) * 0.25 * rel(t, 0.18, 0.22)
    borda = T.zero()
    for k in range(3):
        a = t * 9 + k * TAU / 3
        x1, y1 = 0.55 * forma * math.cos(a), 0.55 * forma * math.sin(a)
        x2, y2 = 0.55 * forma * math.cos(a + 0.8), 0.55 * forma * math.sin(a + 0.8)
        borda += _raio(T, _quadro(t, 30 + k), x1, y1, x2, y2, 0.01, 3, 0.4)
    G += (R * 1.3 + cupula * 1.1 + dentro + borda * rel(t, 0.25, 0.3)) * env
    H += (R * 1.3 + borda * 0.9 * rel(t, 0.25, 0.3) + cupula * 0.4) * env
    G += _faiscas(T, t, 13, 18, 0.7, 0.8) * env
    return G, H


def seis_dobras(T, t, rng):
    """As Seis Dobras: seis riscos de raio, cada um de um lado diferente, atravessam o rival um depois
    do outro (cada um acende e some), e no fim o clarão amarelo que o deixa paralisado."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    for k in range(6):
        t0 = 0.05 + 0.08 * k
        f = rel(t, t0, t0 + 0.09)
        if f <= 0 or f >= 1:
            # o rastro que fica: fino, sumindo
            resto = 1 - rel(t, t0 + 0.09, t0 + 0.3)
            if f >= 1 and resto > 0:
                a = TAU * k / 6 + 0.3
                c, s_ = math.cos(a), math.sin(a)
                R = _raio(T, np.random.default_rng(50 + k), -0.75 * c, -0.75 * s_, 0.75 * c, 0.75 * s_, 0.008, 3, 0.1)
                G += R * resto * 0.8 * env
                H += R * resto * 0.6 * env
            continue
        a = TAU * k / 6 + 0.3
        c, s_ = math.cos(a), math.sin(a)
        # o risco: um traço curto e reto (pouco tremido) que atravessa de um lado ao outro
        cab = -0.9 + 1.8 * f
        R = _raio(T, np.random.default_rng(50 + k), (cab - 0.55) * c, (cab - 0.55) * s_, cab * c, cab * s_, 0.02, 3, 0.1)
        G += (R * 1.4 + T.blur(R, 0.03) * 0.9) * env
        H += (R * 1.5 + T.gauss(cab * c, cab * s_, 0.04, None) * 1.2) * env
    cl = pulso(t, 0.55, 0.85)
    G += (T.gauss(0, 0, 0.32, 0.32) * cl + T.ring(0.15 + 0.5 * rel(t, 0.55, 0.85), 0.025) * cl) * env
    H += T.flare(0, 0, 0.9 * cl + 0.01, thin=0.015) * cl * env
    G += _faiscas(T, t, 23, 20, 0.55, 0.75) * env
    return G, H


# =================================================================== Inosuke
def percepcao_espacial(T, t, rng):
    """A pele do Inosuke sente tudo: as vibrações correm do chão em linhas finas e tremidas, convergem
    no rival (o ponto pisca), e as duas lâminas cortam o Preparo dele num X rápido."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    linhas = T.zero()
    for k in range(9):
        a = math.pi * (0.1 + 0.8 * k / 8)
        f = ease_out(rel(t, 0.0 + 0.02 * k, 0.35), 1.5)
        pts = []
        for u in np.linspace(0, 1, 14):
            r = 0.95 - 0.85 * u * f
            pts.append((r * math.cos(a) + 0.02 * math.sin(u * 30 + t * 40), r * math.sin(a) * 0.5 + 0.15))
        linhas += T.polyline(pts, 0.008) * (1 - rel(t, 0.35, 0.5))
    pisca = pulso(t, 0.3, 0.5)
    corta = ease_out(rel(t, 0.45, 0.58), 2)
    some_ = rel(t, 0.62, 0.78)
    X = T.polys([(lamina(-0.45, -0.4, 0.45, 0.4, 0.05, prog=corta, inicio=some_), 1.0), (lamina(0.45, -0.4, -0.45, 0.4, 0.05, prog=corta, inicio=some_), 1.0)], 0.006)
    G += (linhas * 1.1 + T.gauss(0, 0.1, 0.06, 0.06) * pisca * 1.4 + X * 1.2 + T.ring(0.1 + 0.3 * pisca, 0.015, 0, 0.1) * pisca) * env
    H += (T.gauss(0, 0.1, 0.03, 0.03) * pisca * 1.5 + X * 0.7) * env
    return G, H


def _lamina_lascada(x1, y1, x2, y2, larg, prog, inicio, dentes=9):
    """Uma lâmina lascada (os dentes de serra das espadas do Inosuke)."""
    base = lamina(x1, y1, x2, y2, larg, prog=prog, inicio=inicio, n=dentes * 2)
    meio = len(base) // 2
    cima = base[:meio]
    cima = [(x + (0.025 if i % 2 else 0.0) * -(y2 - y1) / math.hypot(x2 - x1, y2 - y1), y + (0.025 if i % 2 else 0.0) * (x2 - x1) / math.hypot(x2 - x1, y2 - y1)) for i, (x, y) in enumerate(cima)]
    return cima + base[meio:]


def presas_rasgantes(T, t, rng):
    """As Presas: as duas lâminas lascadas cruzam em X ao mesmo tempo, os dentes de serra deixam o
    rasgo irregular, e as lascas e o sangue espirram dos dois lados."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    corta = ease_out(rel(t, 0.1, 0.32), 2)
    some_ = rel(t, 0.45, 0.65)
    A = T.polys([(_lamina_lascada(-0.65, -0.55, 0.65, 0.55, 0.06, corta, some_), 1.0), (_lamina_lascada(0.65, -0.55, -0.65, 0.55, 0.06, corta, some_), 1.0)], 0.006)
    cl = pulso(t, 0.25, 0.45)
    G += (A * 1.2 + T.blur(A, 0.03) * 0.5 + T.gauss(0, 0, 0.25, 0.25) * cl * 0.8) * env
    H += (np.clip(A - T.blur(A, 0.01), 0, 1) * 1.2 + T.flare(0, 0, 0.6 * cl + 0.01, ang=0.7, thin=0.015) * cl) * env
    G += _faiscas(T, t, 44, 22, 0.28, 0.8, 0.011) * env
    return G, H


def investida_inosuke(T, t, rng):
    """A investida do javali: a cabeça do javali (a máscara: o focinho, as presas e as orelhas) avança
    de lado com a poeira, bate no rival, e os cortes loucos riscam em todas as direções."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    vem = ease_in(rel(t, 0.0, 0.3), 1.6)
    x0 = -0.9 + 0.9 * vem
    vis = 1 - rel(t, 0.32, 0.45)
    E = 1.7
    cab = [(x0 + x * E, y * E) for x, y in ((-0.18, -0.12), (0.05, -0.18), (0.18, -0.08), (0.24, 0.04), (0.16, 0.14), (-0.05, 0.16), (-0.2, 0.06))]
    orelhas = [[(x0 + x * E, y * E) for x, y in o] for o in ([(-0.14, -0.12), (-0.2, -0.3), (-0.05, -0.15)], [(-0.02, -0.16), (0.0, -0.34), (0.08, -0.17)])]
    presas = [lamina(x0 + 0.16 * E, 0.08 * E, x0 + 0.32 * E, -0.04 * E, 0.035), lamina(x0 + 0.12 * E, 0.12 * E, x0 + 0.3 * E, 0.06 * E, 0.03)]
    olhos = [(x0 + 0.08 * E, -0.04 * E, vis), (x0 - 0.04 * E, -0.05 * E, vis)]
    focinho = [(x0 + (0.22 + 0.07 * math.cos(u)) * E, (0.04 + 0.08 * math.sin(u)) * E) for u in np.linspace(0, TAU, 16, endpoint=False)]
    J = T.polys([(cab, 1.0), (focinho, 1.0)] + [(o, 1.0) for o in orelhas], 0.008) * vis
    narinas = T.gauss(x0 + 0.23 * E, 0.01 * E, 0.012, 0.018) + T.gauss(x0 + 0.23 * E, 0.08 * E, 0.012, 0.018)
    P = T.polys([(p, 1.0) for p in presas], 0.004) * vis
    poeira = []
    sub = np.random.default_rng(7)
    for _ in range(18):
        f = sub.uniform()
        poeira.append((x0 - 0.3 - 0.4 * f, 0.25 + sub.uniform(-0.05, 0.1), (1 - f) * vis * 0.7))
    cortes = T.zero()
    for k in range(7):
        t0 = 0.32 + 0.04 * k
        f = ease_out(rel(t, t0, t0 + 0.08), 2)
        s_ = rel(t, t0 + 0.12, t0 + 0.25)
        if f <= 0:
            continue
        a = 0.9 * k + 0.4
        cortes += T.polys([(lamina(-0.6 * math.cos(a), -0.6 * math.sin(a), 0.6 * math.cos(a), 0.6 * math.sin(a), 0.035, prog=f, inicio=s_), 1.0)], 0.005)
    G += (J * 0.6 + P * 1.1 + T.splats(poeira, 0.04) * 0.5 + cortes * 1.2) * env
    G -= narinas * vis * 0.8 * env
    H += (P * 0.8 + np.clip(J - T.blur(J, 0.01), 0, 1) * 0.6 + cortes * 0.7 + T.splats(olhos, 0.015) * 1.5) * env
    G += _faiscas(T, t, 77, 16, 0.32, 0.7) * env
    return G, H


# =================================================================== Muzan
def chicotes_de_carne(T, t, rng):
    """Os chicotes de carne: saem do chão de dois lados, se curvam por cima do rival com os espinhos
    e estalam nele (o estalo acende), depois recolhem."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    W = T.zero()
    esp = []
    for lado in (-1, 1):
        sai = ease_out(rel(t, 0.0, 0.32), 1.6) * (1 - ease_in(rel(t, 0.6, 0.9), 1.5))
        pts = []
        for u in np.linspace(0, sai, 20):
            a = math.pi * u
            x = lado * (0.75 - 0.75 * u) + lado * 0.1 * math.sin(a * 2)
            y = 0.5 - 0.95 * math.sin(a * 0.8) + 0.3 * u * u
            pts.append((x, y))
        if len(pts) > 1:
            W += T.polyline(pts, 0.035)
            for j in range(3, len(pts), 3):
                x, y = pts[j]
                esp.append((lamina(x, y, x + lado * 0.05, y - 0.07, 0.015), 1.0))
    E = T.polys(esp, 0.004)
    estalo = pulso(t, 0.3, 0.5)
    G += (W * 1.1 + E + T.gauss(0, 0, 0.2, 0.2) * estalo) * env
    H += (np.clip(W - T.blur(W, 0.01), 0, 1) * 0.5 + T.flare(0, 0, 0.5 * estalo + 0.01, thin=0.02) * estalo) * env
    return G, H


def sangue_corruptor(T, t, rng):
    """O sangue de Muzan: o furo acende no rival e as veias escuras se espalham dele em galhos, pulsando
    (tum… tum…), enquanto o sangue escorre."""
    G, H = vazio(T)
    env = apaga(t, 0.85, 1)
    furo = pulso(t, 0.0, 0.3)
    espalha = ease_out(rel(t, 0.1, 0.6), 1.5)
    bate = 0.7 + 0.3 * (0.5 + 0.5 * math.sin(t * TAU * 4)) ** 3
    sub = np.random.default_rng(12)
    veias = T.zero()
    for k in range(7):
        a = TAU * k / 7 + sub.uniform(-0.2, 0.2)
        q = np.random.default_rng(100 + k)
        comp = 0.6 * espalha
        if comp < 0.02:
            continue
        veias += T.polyline(jagged(q, 0, 0, comp * math.cos(a), comp * math.sin(a), 4, 0.35), 0.016)
        bx, by = comp * 0.55 * math.cos(a), comp * 0.55 * math.sin(a)
        veias += T.polyline(jagged(q, bx, by, bx + comp * 0.4 * math.cos(a + 0.6), by + comp * 0.4 * math.sin(a + 0.6), 3, 0.35), 0.01)
    gotas = [(sub.uniform(-0.3, 0.3), -0.1 + 0.7 * ((sub.uniform() + t) % 1), 0.7) for _ in range(6)]
    G += (veias * 1.1 * bate + T.gauss(0, 0, 0.06, 0.06) * (furo + 0.4) * 1.5 + T.splats(gotas, 0.014)) * env
    H += (T.gauss(0, 0, 0.03, 0.03) * furo * 1.5 + veias * 0.15) * env
    return G, H


def adaptacao_demoniaca(T, t, rng):
    """A carne do Muzan se adapta: os tentáculos se enrolam no corpo e fecham as feridas, as bocas
    se abrem na carne (os dentes), o olho de demônio acende e o pulso vermelho sai em anel."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    enrola = ease_out(rel(t, 0.0, 0.4), 1.6)
    T_ = T.zero()
    for k in range(5):
        a0 = TAU * k / 5
        pts = []
        for u in np.linspace(0, enrola, 18):
            a = a0 + u * 5
            r = 0.75 - 0.5 * u
            pts.append((r * math.cos(a), r * math.sin(a) * 0.9))
        if len(pts) > 1:
            T_ += T.polyline(pts, 0.03)
    bocas = T.zero()
    for k, (x, y) in enumerate(((-0.25, 0.15), (0.25, 0.05), (0.0, 0.32))):
        ab = pulso(t, 0.35 + 0.05 * k, 0.75)
        bocas += T.polys([([(x - 0.08, y), (x, y - 0.05 * ab), (x + 0.08, y), (x, y + 0.05 * ab)], 1.0)], 0.006) * ab
    olho = rel(t, 0.45, 0.55)
    O = T.polys([([(0.18 * math.cos(a), -0.2 + 0.07 * olho * math.sin(a)) for a in np.linspace(0, TAU, 24, endpoint=False)], 1.0)], 0.006)
    Pu = T.polys([([(0.022 * math.cos(a), -0.2 + 0.065 * olho * math.sin(a)) for a in np.linspace(0, TAU, 14, endpoint=False)], 1.0)], 0.003)
    anel = T.ring(0.1 + 0.7 * rel(t, 0.55, 0.9), 0.03) * (1 - rel(t, 0.55, 0.9)) * (t > 0.55)
    G += (T_ * 0.9 * (1 - rel(t, 0.5, 0.7)) + bocas * 0.9 + O * olho + anel * 1.2 + T.gauss(0, 0, 0.35, 0.4) * pulso(t, 0.4, 0.9) * 0.5) * env
    G -= Pu * 0.8 * env
    H += (np.clip(O - T.blur(O, 0.008), 0, 1) * 0.8 * olho + bocas * 0.3) * env
    return G, H


REGISTRO = [
    ("olfato_tanjiro", olfato_tanjiro, GRANDE, "Tanjiro · o fio da abertura (o cheiro até o ponto fraco)", False),
    ("respiracao_da_agua", respiracao_da_agua, GRANDE, "Tanjiro · a Roda d'Água com as ondas japonesas", False),
    ("hinokami_preparo", hinokami_preparo, MEDIA, "Tanjiro · as chamas subindo na lâmina (Preparo, laço)", True),
    ("hinokami_kagura", hinokami_kagura, GRANDE, "Tanjiro · a Dança do Deus do Fogo: o halo de chamas e o corte", False),
    ("sangue_nezuko", sangue_nezuko, GRANDE, "Nezuko · o chute demoníaco e o sangue", False),
    ("explosao_de_sangue", explosao_de_sangue, GRANDE, "Nezuko · as gotas que explodem em chamas rosa", False),
    ("despertar_nezuko", despertar_nezuko, GRANDE, "Nezuko · as vinhas da forma desperta e o chute", False),
    ("audicao_zenitsu", audicao_zenitsu, GRANDE, "Zenitsu · as ondas de som e o risco de raio", False),
    ("primeira_postura", primeira_postura, GRANDE, "Zenitsu · a cúpula elétrica no aliado", False),
    ("seis_dobras", seis_dobras, GRANDE, "Zenitsu · seis riscos de raio de seis lados", False),
    ("percepcao_espacial", percepcao_espacial, GRANDE, "Inosuke · as vibrações do chão e o X", False),
    ("presas_rasgantes", presas_rasgantes, GRANDE, "Inosuke · as duas lâminas lascadas em X", False),
    ("investida_inosuke", investida_inosuke, GRANDE, "Inosuke · a cabeça do javali e os cortes loucos", False),
    ("chicotes_de_carne", chicotes_de_carne, GRANDE, "Muzan · os chicotes de carne com espinhos", False),
    ("sangue_corruptor", sangue_corruptor, GRANDE, "Muzan · as veias escuras se espalhando", False),
    ("adaptacao_demoniaca", adaptacao_demoniaca, GRANDE, "Muzan · a carne fecha, as bocas e o olho", False),
]
