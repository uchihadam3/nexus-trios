"""As três habilidades do Kakashi, do Yusuke e do Killua, desenhadas para eles.

Pedido do jogador: "faz as três habilidades do Kakashi, do Yusuke Urameshi e do
Killua muito bem feitas… se é à distância, à distância; se é de perto, de perto;
se manda um projétil, o projétil vai até lá… com o efeito sonoro correto".

Kakashi
- sharingan_kakashi: o olho abre sobre o rival, a íris vermelha com as três
  vírgulas (tomoe) gira cada vez mais rápido e o genjutsu estoura em anéis.
- sharingan_ator: o olho dele acende quando ele usa (em quem age).
- raikiri_mao: o Raikiri crepitando na mão durante o Preparo (laço).
- raikiri_impacto: a mão de raio entra no rival e os raios saem pelas costas.
- kamui: o Mangekyō dele (as três lâminas curvas) gira e o espaço torce numa
  espiral que suga tudo para o centro.

Yusuke
- soco_espiritual: o punho com a aura azul entra e a energia espiritual estoura.
- reigun_carga: a energia juntando na ponta do dedo (laço, no Preparo).
- reigun_bala: a bala espiritual voando com a cauda (laço, viagem).
- reigun_explosao: a bala explode numa esfera azul enorme.
- shotgun_rajada: o leque de balas espirituais voando (laço, viagem).
- shotgun_impacto: as balas pipocando no rival, uma atrás da outra.

Killua
- ritmo_eletrico: as imagens dele giram em volta do rival deixando rastro
  elétrico e fecham nele com as garras.
- palma_faixa: o raio que sai da palma até o rival (faixa, laço).
- palma_impacto: o raio estoura no rival.
- velocidade_divina: ele aparece num ponto e noutro em clarões de raio, batendo
  de todos os lados, e fecha com o golpe final que paralisa.
- velocidade_aura: a aura elétrica crepitando nele quando ativa.
"""
from __future__ import annotations

import math

import numpy as np

from .base import FAIXA, GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _gira(pts, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def _quadro(t, seed=0):
    """Um gerador diferente a cada quadro (o raio muda de forma), mas igual entre renders."""
    return np.random.default_rng(int(round(t * 12)) * 7919 + seed)


def _raio(T, rng, x1, y1, x2, y2, larg=0.012, depth=5, rough=0.3, galhos=3):
    """Um raio com galhos: a linha quebrada principal e ramos curtos saindo dela."""
    pts = jagged(rng, x1, y1, x2, y2, depth, rough)
    R = T.polyline(pts, larg).copy()
    for _ in range(galhos):
        k = int(rng.integers(2, max(3, len(pts) - 2)))
        bx, by = pts[k]
        ang = math.atan2(y2 - y1, x2 - x1) + rng.choice([-1, 1]) * rng.uniform(0.5, 1.1)
        comp = math.hypot(x2 - x1, y2 - y1) * rng.uniform(0.15, 0.3)
        R += T.polyline(jagged(rng, bx, by, bx + comp * math.cos(ang), by + comp * math.sin(ang), 3, 0.35), larg * 0.6) * 0.75
    return R


# =================================================================== Kakashi
def _tomoe(r_anel, ang, cab=0.062):
    """Uma vírgula do Sharingan: a cabeça redonda no anel e a cauda curva afinando ao longo dele."""
    cx, cy = r_anel * math.cos(ang), r_anel * math.sin(ang)
    cabeca = [(cx + cab * math.cos(a), cy + cab * math.sin(a)) for a in np.linspace(0, TAU, 18, endpoint=False)]
    fora, dentro = [], []
    for k in range(10):
        u = k / 9
        a = ang - 0.9 * u
        w = cab * (1 - u) ** 1.1
        r = r_anel + 0.25 * cab * u
        fora.append(((r + w) * math.cos(a), (r + w) * math.sin(a)))
        dentro.append(((r - w) * math.cos(a), (r - w) * math.sin(a)))
    return cabeca, fora + dentro[::-1]


def _iris(T, giro, raio=0.32, cx=0.0, cy=0.0, esc=1.0):
    """A íris do Sharingan: disco vermelho com a pupila, o anel e as três vírgulas vazados (pretos)."""
    disco = T.polys([([(cx + raio * esc * math.cos(a), cy + raio * esc * math.sin(a)) for a in np.linspace(0, TAU, 48, endpoint=False)], 1.0)], 0.004)
    furos = T.gauss(cx, cy, 0.07 * esc) * 1.6 + T.ring(0.19 * esc, 0.012 * esc, cx=cx, cy=cy) * 0.85
    for k in range(3):
        cab, cauda = _tomoe(0.19 * esc, giro + TAU * k / 3, 0.06 * esc)
        furos += T.polys([([(cx + x, cy + y) for x, y in cab], 1.0), ([(cx + x, cy + y) for x, y in cauda], 1.0)], 0.003) * 1.4
    borda = T.ring(raio * esc, 0.02 * esc, cx=cx, cy=cy)
    return np.clip(disco - furos, 0, None), borda


def sharingan_kakashi(T, t, rng):
    """O olho abre sobre o rival, as vírgulas giram cada vez mais rápido, o olho brilha e o genjutsu
    estoura em anéis vermelhos que se espalham, com estilhaços de chakra."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    abre = back(rel(t, 0.0, 0.2), 1.4)
    giro = TAU * (0.4 * t + 2.2 * ease_in(rel(t, 0.15, 0.6), 2.2))
    # pálpebras: amêndoa que abre de uma linha
    alto = 0.36 * abre + 0.004
    olho = [(0.62 * math.cos(a), alto * math.sin(a) * (1.0 if math.sin(a) < 0 else 0.92)) for a in np.linspace(0, TAU, 60, endpoint=False)]
    mascara = T.polys([(olho, 1.0)], 0.006)
    contorno = T.polyline(olho + [olho[0]], 0.012)
    iris, borda = _iris(T, giro, 0.3)
    G += (iris * mascara * 1.25 + borda * mascara * 0.8 + contorno * 0.9 + T.blur(contorno, 0.03) * 0.6) * env
    H += (contorno * 0.5 + borda * mascara * 0.3) * env
    # o genjutsu estoura: clarão no olho e anéis vermelhos que se espalham, com estilhaços
    k = pulso(t, 0.55, 0.8)
    G += (T.gauss(0, 0, 0.18, 0.12) * k * 1.6 + sum(T.ring(0.2 + 0.75 * ease_out(rel(t, 0.55 + 0.06 * j, 0.95), 2), 0.03 - 0.006 * j) * pulso(t, 0.55 + 0.06 * j, 0.98) for j in range(3))) * env
    H += T.gauss(0, 0, 0.1, 0.06) * k * 1.4 * env
    sub = np.random.default_rng(21)
    cacos = []
    for _ in range(14):
        a = sub.uniform(0, TAU)
        d = 0.25 + 0.6 * ease_out(rel(t, 0.58, 0.95), 2) * sub.uniform(0.5, 1)
        cacos.append((estrela(d * math.cos(a), d * math.sin(a), 0.03, a, 3, 0.3), pulso(t, 0.58, 0.95) * sub.uniform(0.5, 1)))
    C = T.polys(cacos, 0.003)
    G += C * 1.2 * env
    H += C * 0.5 * env
    return G, H


def sharingan_ator(T, t, rng):
    """O olho do Kakashi acende nele: a íris aparece, as vírgulas giram rápido e somem num clarão."""
    G, H = vazio(T)
    env = pulso(t, 0.0, 0.85) ** 0.6
    giro = TAU * 2.5 * t
    esc = 0.75 * back(rel(t, 0.0, 0.25), 1.6)
    iris, borda = _iris(T, giro, 0.32, esc=max(esc, 0.01))
    fl = T.flare(0, 0, 0.9 * pulso(t, 0.1, 0.5) + 1e-3, 0.35, 0.012)
    G += (iris * 1.2 + borda * 0.8 + T.blur(borda, 0.04) * 0.7 + fl * 0.6) * env
    H += (borda * 0.4 + fl * 0.8) * env
    return G, H


def raikiri_mao(T, t, rng):
    """O Raikiri na mão: a bola de raio branco-azulada crepitando, os raios curtos mudando a cada
    quadro e as faíscas pulando, como um bando de pássaros cantando."""
    G, H = vazio(T)
    q = _quadro(t, 3)
    nucleo = T.gauss(0, 0, 0.13) * (0.85 + 0.15 * math.sin(TAU * t * 6))
    R = T.zero()
    for k in range(7):
        a = TAU * k / 7 + q.uniform(-0.4, 0.4)
        comp = q.uniform(0.35, 0.75)
        R += _raio(T, q, 0.05 * math.cos(a), 0.05 * math.sin(a), comp * math.cos(a), comp * math.sin(a), 0.012, 4, 0.35, 1)
    sub = np.random.default_rng(5)
    fa = []
    for _ in range(18):
        a = sub.uniform(0, TAU)
        f = (sub.uniform() + t * 2) % 1
        d = 0.15 + 0.6 * f
        fa.append((d * math.cos(a), d * math.sin(a), (1 - f) * sub.uniform(0.4, 1)))
    G += nucleo * 1.4 + R * 1.2 + T.blur(R, 0.03) * 0.9 + T.splats(fa, 0.012) * 1.2 + T.ring(0.22, 0.05) * 0.4
    H += nucleo * 1.6 + R * 0.9
    return G, H


def raikiri_impacto(T, t, rng):
    """A mão de raio entra no rival (vem de −x), o clarão branco no ponto do golpe e os raios saem
    pelas costas dele (+x), compridos e com galhos; faíscas e o anel elétrico abrindo."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    q = _quadro(t, 11)
    entra = ease_in(rel(t, 0.0, 0.14), 1.6)
    lanca = T.tapered([(-1.0, 0.0, -0.95 + 0.95 * entra, 0.0, 1.0)], 0.12) * (1 - rel(t, 0.14, 0.3))
    bola = T.gauss(-0.95 + 0.95 * entra, 0, 0.1) * (1 - rel(t, 0.16, 0.34)) * 1.6
    k = pulso(t, 0.12, 0.5)
    clarao = T.gauss(0, 0, 0.24) * k * 2.0 + T.flare(0, 0, 1.4 * k + 1e-3, 0.0, 0.01)
    # os raios atravessam e saem pelas costas
    saida = T.zero()
    if t >= 0.12:
        for j in range(5):
            ang = q.uniform(-0.55, 0.55)
            comp = 0.55 + 0.4 * ease_out(rel(t, 0.12, 0.4), 2)
            saida += _raio(T, q, 0.05, 0, comp * math.cos(ang) + 0.1, comp * math.sin(ang), 0.016, 5, 0.32, 2)
        saida *= 1 - rel(t, 0.55, 0.85)
    anel = T.ring(0.15 + 0.6 * ease_out(rel(t, 0.12, 0.6), 2), 0.035) * pulso(t, 0.12, 0.7)
    fa = []
    sub = np.random.default_rng(13)
    for _ in range(20):
        a = sub.normal(0, 0.9)
        d = 0.1 + 0.75 * ease_out(rel(t, 0.14, 0.8), 2) * sub.uniform(0.4, 1)
        fa.append((d * math.cos(a), d * math.sin(a), pulso(t, 0.14, 0.85) * sub.uniform(0.4, 1)))
    G += (lanca * 1.3 + bola + clarao + saida * 1.3 + T.blur(saida, 0.025) + anel + T.splats(fa, 0.012) * 1.3) * env
    H += (lanca + bola + clarao * 1.1 + saida * 0.9 + anel * 0.3 + T.splats(fa, 0.008) * 0.8) * env
    return G, H


def _mangekyo(T, giro, esc=1.0):
    """O Mangekyō do Kakashi: três lâminas curvas, como um cata-vento, em volta da pupila."""
    formas = []
    for k in range(3):
        a0 = giro + TAU * k / 3
        fora, dentro = [], []
        for j in range(14):
            u = j / 13
            a = a0 + 1.5 * u
            r = (0.08 + 0.34 * u) * esc
            w = 0.09 * esc * math.sin(math.pi * u) ** 0.7
            fora.append(((r + w) * math.cos(a), (r + w) * math.sin(a)))
            dentro.append(((r - w * 0.4) * math.cos(a - 0.25), (r - w * 0.4) * math.sin(a - 0.25)))
        formas.append((fora + dentro[::-1], 1.0))
    return T.polys(formas, 0.004)


def kamui(T, t, rng):
    """Kamui: o Mangekyō aparece girando sobre o rival, o espaço torce numa espiral que gira cada
    vez mais rápido e suga os estilhaços para o centro, até tudo sumir num ponto e estourar."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    aparece = back(rel(t, 0.0, 0.2), 1.3)
    giro = TAU * (0.5 * t + 1.6 * ease_in(rel(t, 0.15, 0.7), 2))
    some = 1 - ease_in(rel(t, 0.55, 0.72), 2)
    M = _mangekyo(T, giro, 0.85 * aparece * some + 0.001)
    disco = T.ring(0.42 * aparece * some + 0.01, 0.03)
    # a espiral de distorção: braços logarítmicos girando para dentro
    espiral = T.zero()
    forca = pulso(t, 0.15, 0.8)
    if forca > 0.01:
        for b in range(4):
            pts = []
            for j in range(40):
                u = j / 39
                r = 0.85 * (1 - u) * (1 - 0.6 * rel(t, 0.5, 0.75)) + 0.02
                a = giro * 1.4 + TAU * b / 4 + 4.5 * u
                pts.append((r * math.cos(a), r * math.sin(a)))
            espiral += T.polyline(pts, 0.022) * forca
    # os estilhaços sugados
    sub = np.random.default_rng(31)
    cacos = []
    for _ in range(22):
        a0, d0 = sub.uniform(0, TAU), sub.uniform(0.5, 0.95)
        u = ease_in(rel(t, 0.2 + 0.2 * sub.uniform(), 0.72), 1.8)
        d = d0 * (1 - u)
        a = a0 + 3.5 * u
        cacos.append((estrela(d * math.cos(a), d * math.sin(a), 0.035 * (1 - 0.6 * u) + 0.005, a, 3, 0.35), (1 - u) * sub.uniform(0.5, 1) * pulso(t, 0.15, 0.75)))
    C = T.polys(cacos, 0.003)
    # o ponto que colapsa e estoura
    k = pulso(t, 0.68, 0.9)
    estouro = T.gauss(0, 0, 0.25 * k + 0.01) * k * 2 + T.ring(0.08 + 0.7 * ease_out(rel(t, 0.7, 0.98), 2), 0.03) * pulso(t, 0.7, 0.98)
    G += (M * 1.3 + disco * 0.8 + espiral * 1.0 + T.blur(espiral, 0.03) * 0.8 + C * 1.2 + estouro) * env
    H += (M * 0.45 + espiral * 0.35 + C * 0.5 + estouro * 0.9) * env
    return G, H


# =================================================================== Yusuke
def _punho(cx, cy, esc):
    """O punho fechado visto de lado, os nós dos dedos para +x."""
    pts = [(-0.3, -0.16), (0.1, -0.2), (0.16, -0.19), (0.2, -0.13), (0.24, -0.1), (0.26, -0.04), (0.27, 0.02), (0.26, 0.08),
           (0.22, 0.13), (0.14, 0.17), (0.02, 0.18), (-0.1, 0.22), (-0.22, 0.2), (-0.3, 0.12)]
    return [(cx + x * esc, cy + y * esc) for x, y in pts]


def soco_espiritual(T, t, rng):
    """O punho do Yusuke coberto da aura azul entra de −x e acerta o rival: a energia espiritual estoura
    em clarão, anel e chamas espirituais que sobem, com os riscos saindo para a frente."""
    G, H = vazio(T)
    env = apaga(t, 0.78, 1)
    vem = ease_in(rel(t, 0.0, 0.16), 1.8)
    px = -0.95 + 0.85 * vem
    vis = 1 - rel(t, 0.2, 0.36)
    P = T.polys([(_punho(px, 0.0, 1.15), 1.0)], 0.004)
    # os dedos dobrados (vincos) e o polegar por cima, para ler como punho
    vincos = sum(T.polyline([(px + 0.12, y), (px + 0.3, y)], 0.012) for y in (-0.1, -0.02, 0.06))
    polegar = T.polyline([(px - 0.05, 0.12), (px + 0.12, 0.1), (px + 0.2, 0.06)], 0.02)
    P = np.clip(P - vincos * 0.9, 0, None) * vis
    polegar = polegar * vis
    aura = T.blur(P, 0.06) * 1.6 + T.tapered([(px - 0.7, 0.0, px - 0.1, 0.0, 1.0)], 0.3) * 0.6 * vis
    k = pulso(t, 0.14, 0.5)
    clarao = T.gauss(0, 0, 0.26) * k * 2.0 + T.flare(0, 0, 1.2 * k + 1e-3, 0.4, 0.012)
    anel = T.ring(0.15 + 0.7 * ease_out(rel(t, 0.14, 0.6), 2.2), 0.045) * pulso(t, 0.14, 0.65)
    anel2 = T.ring(0.1 + 0.5 * ease_out(rel(t, 0.2, 0.7), 2), 0.025) * pulso(t, 0.2, 0.75)
    sub = np.random.default_rng(41)
    riscos = []
    for _ in range(12):
        a = sub.normal(0, 0.5)
        d0 = 0.15 + 0.7 * ease_out(rel(t, 0.15, 0.6), 2)
        riscos.append((d0 * 0.5 * math.cos(a), d0 * 0.5 * math.sin(a), d0 * math.cos(a), d0 * math.sin(a), pulso(t, 0.15, 0.7) * sub.uniform(0.5, 1)))
    R = T.tapered(riscos, 0.035)
    chamas = []
    for _ in range(16):
        x0 = sub.normal(0, 0.25)
        f = rel(t, 0.25 + 0.2 * sub.uniform(), 0.95)
        chamas.append((x0 + 0.05 * math.sin(f * 9 + x0 * 7), 0.2 - 0.8 * f, pulso(f, 0.0, 1.0) * sub.uniform(0.5, 1)))
    Ch = T.splats(chamas, 0.03)
    G += (P * 1.2 + polegar * 0.5 + aura + clarao + anel + anel2 * 0.7 + R * 1.2 + Ch * 1.2) * env
    H += (P * 0.6 + polegar * 0.4 + clarao * 1.1 + anel * 0.35 + R * 0.6 + Ch * 0.5) * env
    return G, H


def reigun_carga(T, t, rng):
    """A energia espiritual juntando na ponta do dedo: a esfera pulsando, o anel girando e as partículas
    sendo puxadas para dentro."""
    G, H = vazio(T)
    pul = 0.85 + 0.15 * math.sin(TAU * t * 2)
    nucleo = T.gauss(0, 0, 0.12 * pul) * 1.4
    anel = T.ring(0.28, 0.025, squash=2.2) * 0.9 + T.ring(0.2, 0.02) * 0.5 * (0.5 + 0.5 * math.sin(TAU * t))
    sub = np.random.default_rng(51)
    ps = []
    for _ in range(26):
        a = sub.uniform(0, TAU)
        f = (sub.uniform() + t) % 1
        d = 0.85 * (1 - f) + 0.1
        ps.append((d * math.cos(a + f), d * math.sin(a + f), f * sub.uniform(0.5, 1)))
    P = T.splats(ps, 0.014)
    G += nucleo + anel + P * 1.2 + T.flare(0, 0, 0.7 + 1e-3, TAU * t / 4, 0.012) * 0.6
    H += nucleo * 1.3 + P * 0.6
    return G, H


def reigun_bala(T, t, rng):
    """A bala espiritual do Reigun em voo: a esfera branca-azul enorme na frente, a cauda grossa que
    afina para trás, os anéis de pressão em volta e as faíscas soltando."""
    G, H = vazio(T)
    cx = 0.38
    pul = 1 + 0.06 * math.sin(TAU * t * 2)
    esfera = T.gauss(cx, 0, 0.17 * pul) * 1.5 + T.ring(0.2 * pul, 0.03, cx=cx) * 0.8
    cauda = T.tapered([(-0.95, 0.0, cx - 0.05, 0.0, 1.0)], 0.32) * 0.9 + T.tapered([(-0.7, 0.0, cx, 0.0, 1.0)], 0.14) * 0.8
    aneis = T.zero()
    for j in range(3):
        f = (j / 3 + t) % 1
        aneis += T.ring(0.14 + 0.06 * f, 0.02, cx=cx - 0.15 - 0.7 * f, squash=2.6) * (1 - f) * 0.9
    sub = np.random.default_rng(61)
    fa = []
    for _ in range(14):
        f = (sub.uniform() + t * 1.5) % 1
        fa.append((cx - 0.1 - 0.85 * f, sub.normal(0, 0.06) * (0.5 + f * 2), (1 - f) * sub.uniform(0.5, 1)))
    G += esfera + cauda + T.blur(cauda, 0.03) * 0.6 + aneis + T.splats(fa, 0.012) * 1.1
    H += T.gauss(cx, 0, 0.1) * 1.8 + cauda * 0.5 + T.splats(fa, 0.008) * 0.6
    return G, H


def reigun_explosao(T, t, rng):
    """A bala explode: a esfera azul cresce engolindo o rival, a casca de energia brilha, dois anéis
    de choque correm e os pedaços de energia voam; sobra a fumaça espiritual subindo."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    cresce = ease_out(rel(t, 0.0, 0.35), 2.4)
    r = 0.12 + 0.62 * cresce
    disco = T.blur(T.polys([([(r * math.cos(a), r * math.sin(a)) for a in np.linspace(0, TAU, 48, endpoint=False)], 1.0)]), 0.05)
    esfera = (T.gauss(0, 0, r * 0.42) * 1.2 + disco * 0.55) * pulso(t, 0.0, 0.7)
    casca = T.ring(r, 0.05) * pulso(t, 0.0, 0.75)
    choque = sum(T.ring(0.2 + 0.78 * ease_out(rel(t, 0.1 + 0.08 * j, 0.8), 2), 0.03) * pulso(t, 0.1 + 0.08 * j, 0.85) for j in range(2))
    sub = np.random.default_rng(71)
    pedacos = []
    for _ in range(24):
        a = sub.uniform(0, TAU)
        d = 0.2 + 0.75 * ease_out(rel(t, 0.1, 0.8), 2) * sub.uniform(0.5, 1)
        pedacos.append((d * math.cos(a), d * math.sin(a), pulso(t, 0.1, 0.85) * sub.uniform(0.4, 1)))
    fumo = []
    for _ in range(14):
        f = rel(t, 0.4 + 0.2 * sub.uniform(), 1.0)
        fumo.append((sub.normal(0, 0.25), 0.1 - 0.7 * f, pulso(f, 0.0, 1.0) * 0.8))
    G += (esfera + casca * 1.1 + choque + T.splats(pedacos, 0.015) * 1.2 + T.splats(fumo, 0.06) * 0.6) * env
    H += (T.gauss(0, 0, r * 0.4) * pulso(t, 0.0, 0.5) * 1.8 + casca * 0.5 + choque * 0.3 + T.splats(pedacos, 0.009) * 0.6) * env
    return G, H


def shotgun_rajada(T, t, rng):
    """O Shotgun em voo: o leque de balas espirituais saindo juntas, cada uma com a cauda própria."""
    G, H = vazio(T)
    sub = np.random.default_rng(81)
    balas, caudas = [], []
    for j in range(9):
        y = (j - 4) * 0.085 + sub.normal(0, 0.015)
        x = 0.3 + sub.uniform(-0.12, 0.12) + 0.03 * math.sin(TAU * (t + j / 9))
        balas.append((x, y, sub.uniform(0.7, 1)))
        caudas.append((x - 0.45 - sub.uniform(0, 0.2), y * 0.6, x, y, 1.0))
    B = T.splats(balas, 0.03)
    C = T.tapered(caudas, 0.05)
    G += B * 1.4 + C * 0.9 + T.blur(C, 0.02) * 0.5
    H += T.splats(balas, 0.015) * 1.6 + C * 0.4
    return G, H


def shotgun_impacto(T, t, rng):
    """As balas do Shotgun pipocam no rival uma atrás da outra: cada uma estoura numa estrelinha com
    anel, espalhadas pelo corpo, e no fim sobe um clarão geral."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    sub = np.random.default_rng(91)
    for j in range(9):
        x, y = sub.normal(0, 0.28), sub.normal(0, 0.24)
        t0 = 0.04 + 0.05 * j
        k = pulso(t, t0, t0 + 0.32)
        if k <= 0:
            continue
        est = T.polys([(estrela(x, y, 0.13 * k + 0.01, sub.uniform(0, TAU), 6, 0.35), 1.0)], 0.004) * k
        anel = T.ring(0.04 + 0.16 * ease_out(rel(t, t0, t0 + 0.32), 2), 0.018, cx=x, cy=y) * k
        G += (est * 1.2 + anel + T.gauss(x, y, 0.06) * k) * env
        H += (est * 0.8 + anel * 0.3) * env
    k = pulso(t, 0.45, 0.85)
    G += T.gauss(0, 0, 0.22) * k * 0.9 * env
    return G, H


# =================================================================== Killua
def ritmo_eletrico(T, t, rng):
    """Ritmo elétrico: as imagens do Killua (clarões em forma de vulto com as garras) giram em volta do
    rival deixando um rastro de raio, e fecham nele de três lados com cortes de garra que se cruzam."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    q = _quadro(t, 17)
    gira = ease_in(rel(t, 0.0, 0.55), 1.2)
    fecha = ease_in(rel(t, 0.45, 0.62), 1.6)
    vultos = T.zero()
    rastro = T.zero()
    for j in range(5):
        a = TAU * j / 5 + TAU * 1.2 * gira
        r = 0.62 * (1 - fecha) + 0.05
        x, y = r * math.cos(a), r * math.sin(a)
        vis = pulso(t, 0.02 * j, 0.66)
        # o vulto: um clarão alongado de pé, com as garras abertas
        v = T.gauss(x, y, 0.05, 0.11) * 1.3 + T.gauss(x, y - 0.1, 0.035) * 0.9
        for g in (-1, 0, 1):
            v += T.polyline([(x + 0.04, y + g * 0.03), (x + 0.11, y + g * 0.05 - 0.02)], 0.008) * 0.8
        vultos += v * vis
        # rastro elétrico atrás do vulto, no arco
        a2 = a - 0.8
        rastro += _raio(T, q, r * math.cos(a2), r * math.sin(a2), x, y, 0.01, 4, 0.25, 0) * vis * 0.9
    cortes = T.zero()
    for j, ang in enumerate((0.6, -0.5, 2.0)):
        k = pulso(t, 0.58 + 0.05 * j, 0.88)
        for g in (-1, 0, 1):
            dx, dy = -math.sin(ang) * g * 0.06, math.cos(ang) * g * 0.06
            cortes += T.polys([(lamina(-0.55 * math.cos(ang) + dx, -0.55 * math.sin(ang) + dy, 0.55 * math.cos(ang) + dx, 0.55 * math.sin(ang) + dy, 0.02, prog=ease_out(rel(t, 0.58 + 0.05 * j, 0.7 + 0.05 * j), 2), inicio=rel(t, 0.72, 0.9)), 1.0)], 0.003) * k
    k = pulso(t, 0.6, 0.85)
    estouro = T.gauss(0, 0, 0.2) * k * 1.5 + _raio(T, q, -0.5, 0.0, 0.5, 0.0, 0.012, 4, 0.4, 2) * k * 0.6
    G += (vultos + rastro * 1.2 + T.blur(rastro, 0.02) * 0.6 + cortes * 1.3 + estouro) * env
    H += (vultos * 0.6 + rastro * 0.8 + cortes + estouro * 0.8) * env
    return G, H


def palma_faixa(T, t, rng):
    """O raio da Palma relâmpago esticado da palma do Killua até o rival: o raio principal grosso e
    dois finos em volta, mudando de forma a cada quadro, com o brilho em volta."""
    G, H = vazio(T)
    q = _quadro(t, 23)
    alto = T.H / T.W
    R = T.zero()
    for j, (larg, amp) in enumerate(((0.012, 0.35), (0.006, 0.6), (0.006, 0.6))):
        pts = jagged(q, -0.98, 0.0, 0.98, q.normal(0, alto * 0.2), 6, amp * alto * 2.2)
        R += T.polyline(pts, larg) * (1.0 if j == 0 else 0.7)
    ponta = T.gauss(-0.93, 0, 0.035, alto * 0.25) * 0.9
    G += R * 1.3 + T.blur(R, 0.012) * 1.2 + ponta
    H += R * 1.0 + ponta * 0.8
    return G, H


def palma_impacto(T, t, rng):
    """O raio estoura no rival: o clarão, os raios que se abrem em volta dele presos no corpo, o anel
    elétrico e as faíscas; o choque fica crepitando um pouco antes de sumir."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    q = _quadro(t, 29)
    k = pulso(t, 0.0, 0.4)
    clarao = T.gauss(0, 0, 0.25) * k * 2 + T.flare(0, 0, 1.3 * k + 1e-3, 0.3, 0.01)
    R = T.zero()
    vivo = 1 - rel(t, 0.5, 0.85)
    for j in range(6):
        a = TAU * j / 6 + q.uniform(-0.3, 0.3)
        comp = q.uniform(0.35, 0.7)
        R += _raio(T, q, 0, 0, comp * math.cos(a), comp * math.sin(a), 0.013, 4, 0.35, 1)
    anel = T.ring(0.12 + 0.6 * ease_out(rel(t, 0.0, 0.55), 2), 0.03) * pulso(t, 0.0, 0.6)
    G += (clarao + R * vivo * 1.3 + T.blur(R, 0.02) * vivo + anel + faiscas_eletricas(T, t, 33)) * env
    H += (clarao * 1.1 + R * vivo * 0.9 + anel * 0.3) * env
    return G, H


def faiscas_eletricas(T, t, seed):
    sub = np.random.default_rng(seed)
    fa = []
    for _ in range(18):
        a = sub.uniform(0, TAU)
        d = 0.1 + 0.7 * ease_out(rel(t, 0.0, 0.8), 2) * sub.uniform(0.4, 1)
        fa.append((d * math.cos(a), d * math.sin(a), pulso(t, 0.0, 0.85) * sub.uniform(0.4, 1)))
    return T.splats(fa, 0.012) * 1.2


def velocidade_divina(T, t, rng):
    """Velocidade divina: o Killua some e aparece em volta do rival — cada aparição é um clarão de raio,
    ligado à anterior por um risco elétrico em zigue-zague — e de cada ponto sai um golpe até o
    centro. No fim, o golpe final estoura e o rival fica crepitando, paralisado."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    q = _quadro(t, 37)
    sub = np.random.default_rng(43)
    pontos = [(0.68 * math.cos(a), 0.62 * math.sin(a)) for a in [sub.uniform(0, TAU) for _ in range(6)]]
    for j, (x, y) in enumerate(pontos):
        t0 = 0.05 + 0.09 * j
        k = pulso(t, t0, t0 + 0.2)
        if k <= 0:
            continue
        # aparece: clarão e o vulto elétrico
        G += (T.gauss(x, y, 0.07, 0.12) * k * 1.4 + T.flare(x, y, 0.5 * k + 1e-3, 0.6, 0.012)) * env
        H += T.gauss(x, y, 0.035, 0.07) * k * 1.4 * env
        # o risco do ponto anterior até aqui (ele "se teleporta")
        if j > 0:
            px, py = pontos[j - 1]
            G += _raio(T, q, px, py, x, y, 0.01, 4, 0.3, 0) * k * 0.9 * env
        # o golpe até o centro
        g = pulso(t, t0 + 0.04, t0 + 0.16)
        G += T.polys([(lamina(x, y, x * 0.1, y * 0.1, 0.035, prog=1.0), 1.0)], 0.004) * g * 1.2 * env
        H += T.polys([(lamina(x, y, x * 0.1, y * 0.1, 0.018, prog=1.0), 1.0)], 0.003) * g * env
        G += T.gauss(0, 0, 0.08) * g * 1.2 * env
    # o golpe final e o rival paralisado crepitando
    k = pulso(t, 0.62, 0.86)
    final = T.gauss(0, 0, 0.3) * k * 2 + T.ring(0.12 + 0.7 * ease_out(rel(t, 0.62, 0.95), 2), 0.04) * pulso(t, 0.62, 0.95)
    crepita = T.zero()
    if t >= 0.62:
        for j in range(4):
            a = q.uniform(0, TAU)
            crepita += _raio(T, q, 0.15 * math.cos(a), 0.15 * math.sin(a), 0.38 * math.cos(a + 0.6), 0.38 * math.sin(a + 0.6), 0.008, 3, 0.4, 0)
    G += (final + crepita * pulso(t, 0.62, 0.98) * 1.2) * env
    H += (final * 0.9 + crepita * pulso(t, 0.62, 0.98) * 0.8) * env
    return G, H


def velocidade_aura(T, t, rng):
    """A aura da Velocidade divina no Killua: raios crepitando em volta do corpo, mudando a cada quadro."""
    G, H = vazio(T)
    env = pulso(t, 0.0, 0.95) ** 0.5
    q = _quadro(t, 47)
    R = T.zero()
    for j in range(8):
        a = TAU * j / 8 + q.uniform(-0.3, 0.3)
        r0, r1 = 0.3 + q.uniform(0, 0.1), 0.55 + q.uniform(0, 0.25)
        R += _raio(T, q, r0 * math.cos(a), r0 * math.sin(a), r1 * math.cos(a + 0.4), r1 * math.sin(a + 0.4), 0.012, 4, 0.35, 1)
    halo = T.ring(0.36, 0.08) * 0.6
    G += (R * 1.3 + T.blur(R, 0.03) * 0.8 + halo) * env
    H += R * 0.9 * env
    return G, H


REGISTRO = [
    ("sharingan_kakashi", sharingan_kakashi, GRANDE, "Kakashi · Sharingan: o olho abre e o genjutsu estoura", False),
    ("sharingan_ator", sharingan_ator, MEDIA, "Kakashi · o Sharingan acende nele", False),
    ("raikiri_mao", raikiri_mao, MEDIA, "Kakashi · o Raikiri crepitando na mão (laço)", True),
    ("raikiri_impacto", raikiri_impacto, GRANDE, "Kakashi · Raikiri: a mão de raio atravessa o rival", False),
    ("kamui", kamui, GRANDE, "Kakashi · Kamui: o Mangekyō e a espiral que suga", False),
    ("soco_espiritual", soco_espiritual, GRANDE, "Yusuke · Soco espiritual com a aura azul", False),
    ("reigun_carga", reigun_carga, MEDIA, "Yusuke · a energia juntando na ponta do dedo (laço)", True),
    ("reigun_bala", reigun_bala, MEDIA, "Yusuke · a bala do Reigun voando (laço)", True),
    ("reigun_explosao", reigun_explosao, GRANDE, "Yusuke · a bala do Reigun explodindo", False),
    ("shotgun_rajada", shotgun_rajada, MEDIA, "Yusuke · o leque de balas do Shotgun voando (laço)", True),
    ("shotgun_impacto", shotgun_impacto, GRANDE, "Yusuke · as balas do Shotgun pipocando no rival", False),
    ("ritmo_eletrico", ritmo_eletrico, GRANDE, "Killua · Ritmo elétrico: as imagens giram e fecham com as garras", False),
    ("palma_faixa", palma_faixa, FAIXA, "Killua · o raio da Palma relâmpago até o rival (faixa)", True),
    ("palma_impacto", palma_impacto, GRANDE, "Killua · o raio estourando no rival", False),
    ("velocidade_divina", velocidade_divina, GRANDE, "Killua · Velocidade divina: aparece em volta e bate de todos os lados", False),
    ("velocidade_aura", velocidade_aura, MEDIA, "Killua · a aura elétrica nele", False),
]
