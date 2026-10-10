"""As habilidades do Aiolia de Leão e do Arthas, desenhadas para eles.

Aiolia
- plasma_faixa: o Relâmpago de Plasma — dezenas de raios finos e retos saindo
  do punho dele até o rival, mudando a cada quadro (faixa, laço).
- relampago_de_plasma: os raios acertando o rival de vários ângulos, os
  estalos e o brilho dourado.
- velocidade_da_luz: a Velocidade da Luz no campo dos rivais — as linhas de
  plasma cruzando em grade, uma depois da outra, e os clarões nos cruzamentos.
- cosmo_leao: o cosmo dourado subindo nele, com os raios da juba do leão
  (Preparo, laço).
- leao_dourado: a bola de energia com a juba do leão voando (laço, viagem).
- rugido_do_leao: a explosão dourada com a juba abrindo e as faíscas
  (Paralisado).

Arthas
- ceifadora_de_almas: a Frostmourne corta na diagonal com o gelo e as runas, e
  a alma do rival é arrancada e puxada de volta para a espada (−x).
- erguer_os_mortos: no aliado, o círculo de runas no chão e as mãos de osso
  subindo em volta dele, fechando o escudo.
- runa_lich: as runas da Frostmourne girando em volta do Arthas e a névoa fria
  (Preparo, laço).
- praga_da_carne: a peste no campo dos rivais — a névoa doente rolando, as
  caveiras que se formam nela, os cristais de gelo caindo e a vida sugada
  voltando.
"""
from __future__ import annotations

import math

import numpy as np

from .base import FAIXA, GRANDE, MEDIA, TAU, apaga, back, ease_in, ease_out, estrela, jagged, lamina, pulso, rel, vazio


def _quadro(t, seed=0):
    return np.random.default_rng(seed + int(t * 997) % 9973)


_RUIDOS: dict = {}


def _ruido(T, seed, escala=0.05, oitavas=3):
    chave = (T.W, T.H, seed, escala, oitavas)
    if chave not in _RUIDOS:
        _RUIDOS[chave] = T.noise(np.random.default_rng(seed), escala, oitavas)
    return _RUIDOS[chave]


def _juba(T, cx, cy, r, n, giro, comp=0.35, larg=0.06):
    """A juba do leão: muitas mechas pontudas e curvas em volta do centro, de tamanhos diferentes,
    como chamas de cosmo (não pétalas)."""
    sub = np.random.default_rng(int(n * 7 + r * 100))
    formas = []
    for k in range(n * 2):
        a = TAU * k / (n * 2) + giro + sub.uniform(-0.08, 0.08)
        c = comp * sub.uniform(0.55, 1.15) * (1 + 0.2 * math.sin(3 * a + giro * 2))
        w = larg * sub.uniform(0.45, 0.75)
        curva = 0.35 * sub.uniform(0.5, 1)
        pts = []
        for j in range(9):
            f = j / 8
            rr = r + c * f
            aa = a + curva * f * f
            ww = w * (1 - f) ** 1.3
            nx, ny = -math.sin(aa), math.cos(aa)
            pts.append((cx + rr * math.cos(aa) + nx * ww, cy + rr * math.sin(aa) + ny * ww))
        volta = []
        for j in range(8, -1, -1):
            f = j / 8
            rr = r + c * f
            aa = a + curva * f * f
            ww = w * (1 - f) ** 1.3
            nx, ny = -math.sin(aa), math.cos(aa)
            volta.append((cx + rr * math.cos(aa) - nx * ww, cy + rr * math.sin(aa) - ny * ww))
        formas.append((pts + volta, sub.uniform(0.6, 1.0)))
    return T.polys(formas, 0.006)


# =================================================================== Aiolia
def plasma_faixa(T, t, rng):
    """O Relâmpago de Plasma: dezenas de raios finos e quase retos do punho (−x) até o rival (+x),
    abrindo um pouco no meio, cada quadro com outro desenho, e o brilho dourado em volta."""
    G, H = vazio(T)
    alto = T.H / T.W
    q = _quadro(t, 3)
    R = T.zero()
    for _ in range(5):
        y0 = q.normal(0, alto * 0.06)
        y1 = q.normal(0, alto * 0.35)
        pts = jagged(q, -0.98, y0, 0.98, y1, 4, 0.06)
        R += T.polyline(pts, 0.007) * q.uniform(0.6, 1)
    punho = T.gauss(-0.94, 0, 0.05, alto * 0.35)
    R = T.blur(R, 0.004)
    G += R * 1.3 + T.blur(R, 0.012) * 1.1 + punho
    H += R * 0.9 + punho * 0.9
    return G, H


def relampago_de_plasma(T, t, rng):
    """Os raios chegando no rival (de −x, em leque): muitos estalos em pontos diferentes do corpo,
    os riscos curtos e o clarão dourado que pulsa enquanto dura."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    q = _quadro(t, 7)
    vivo = 1 - rel(t, 0.55, 0.75)
    R = T.zero()
    pontos = []
    for _ in range(9):
        y = q.normal(0, 0.28)
        x = q.uniform(-0.25, 0.2)
        R += T.polyline(jagged(q, -1.0, y * 0.4, x, y, 4, 0.1), 0.006)
        pontos.append((x, y, q.uniform(0.6, 1.2)))
    R *= vivo
    estalos = T.splats(pontos, 0.03) * vivo
    k = pulso(t, 0.0, 0.7) * (0.8 + 0.2 * math.sin(TAU * t * 10))
    clarao = T.gauss(0, 0, 0.3) * k * 0.8
    sub = np.random.default_rng(9)
    fa = []
    for _ in range(20):
        a = sub.normal(0, 0.9)
        d = 0.1 + 0.7 * ease_out(rel(t, 0.1, 0.9), 2) * sub.uniform(0.3, 1)
        fa.append((d * math.cos(a), d * math.sin(a), pulso(t, 0.1, 0.95) * sub.uniform(0.4, 1)))
    G += (R * 1.3 + T.blur(R, 0.015) * 0.8 + estalos * 1.2 + clarao + T.splats(fa, 0.01) * 1.1) * env
    H += (R * 0.9 + estalos * 1.1 + clarao * 0.6) * env
    return G, H


def velocidade_da_luz(T, t, rng):
    """A Velocidade da Luz no campo dos rivais: as linhas de plasma cortando reto em grade (umas
    deitadas, outras em diagonal), uma depois da outra, os clarões onde elas se cruzam e o ar
    tremendo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    sub = np.random.default_rng(13)
    L = T.zero()
    cruzes = []
    for j in range(14):
        ini = 0.03 * j
        f = rel(t, ini, ini + 0.12)
        if f <= 0:
            continue
        a = sub.choice([0.0, 0.5, -0.5, 1.2, -1.2]) + sub.normal(0, 0.06)
        cx, cy = sub.uniform(-0.4, 0.4), sub.uniform(-0.35, 0.35)
        c, s = math.cos(a), math.sin(a)
        comp = 1.0 * ease_out(f, 2)
        x1, y1, x2, y2 = cx - c * comp, cy - s * comp, cx + c * comp, cy + s * comp
        L += T.lines([(x1, y1, x2, y2, 1.0)], 0.01) * (1 - rel(t, ini + 0.25, ini + 0.45))
        cruzes.append((cx, cy, pulso(t, ini + 0.05, ini + 0.35)))
    C = T.splats(cruzes, 0.035)
    k = pulso(t, 0.3, 0.7)
    fundo = T.gauss(0, 0, 0.5, 0.4) * k * 0.4
    G += (L * 1.4 + T.blur(L, 0.012) * 1.0 + C * 1.3 + fundo) * env
    H += (L * 1.0 + C * 1.2) * env
    return G, H


def cosmo_leao(T, t, rng):
    """O cosmo do Aiolia: o brilho dourado subindo em volta dele e a juba do leão girando devagar,
    as pontas pulsando como chamas."""
    G, H = vazio(T)
    pul = 0.85 + 0.15 * math.sin(TAU * t * 3)
    J = _juba(T, 0, 0, 0.32, 14, TAU * t / 3, 0.32 * pul, 0.06)
    nucleo = T.gauss(0, 0, 0.25) * 0.8
    sub = np.random.default_rng(17)
    sobe = T.splats([(sub.normal(0, 0.35), 0.6 - 1.2 * ((sub.uniform() + t) % 1), sub.uniform(0.3, 0.9)) for _ in range(24)], 0.014)
    G += J * 0.9 + T.blur(J, 0.02) * 0.6 + nucleo + sobe
    H += J * 0.3 + nucleo * 0.8
    return G, H


def leao_dourado(T, t, rng):
    """O Rugido do Leão voando (+x): a bola de cosmo com a juba em volta, girando, as duas orelhas na
    frente e o rastro dourado."""
    G, H = vazio(T)
    cx = 0.3
    J = _juba(T, cx, 0, 0.17, 12, TAU * t, 0.2, 0.05)
    bola = T.gauss(cx, 0, 0.16)
    orelhas = T.polys([(estrela(cx + 0.1, -0.2, 0.07, -1.2, 3, 0.3), 1.0), (estrela(cx + 0.1, 0.2, 0.07, 1.2, 3, 0.3), 1.0)], 0.004)
    rastro = T.tapered([(cx - 0.95, 0, cx - 0.1, 0, 1.0)], 0.3) * (0.8 + 0.2 * math.sin(TAU * t * 6))
    G += bola * 1.6 + J * 0.9 + orelhas * 0.7 + T.blur(rastro, 0.02) * 0.8
    H += T.gauss(cx, 0, 0.08) * 1.6 + J * 0.3
    return G, H


def rugido_do_leao(T, t, rng):
    """A explosão do Rugido do Leão: o clarão dourado, a juba enorme abrindo em volta do rival e
    sumindo, o anel e as faíscas elétricas que ficam um pouco (Paralisado)."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    k = pulso(t, 0.0, 0.45)
    clarao = T.gauss(0, 0, 0.32) * k * 2.0 + T.flare(0, 0, 1.5 * k + 1e-3, 0.3, 0.01) * k
    abre = back(rel(t, 0.03, 0.4), 1.3)
    J = _juba(T, 0, 0, 0.12 + 0.35 * abre, 16, 0.2, 0.25 + 0.25 * abre, 0.07) * (1 - rel(t, 0.45, 0.75))
    anel = T.ring(0.2 + 0.7 * ease_out(rel(t, 0.0, 0.5), 2), 0.04) * pulso(t, 0.0, 0.55)
    q = _quadro(t, 23)
    fa = T.zero()
    if 0.35 < t < 0.9:
        for _ in range(3):
            a = q.uniform(0, TAU)
            fa += T.polyline(jagged(q, 0.15 * math.cos(a), 0.15 * math.sin(a), 0.4 * math.cos(a), 0.4 * math.sin(a), 3, 0.35), 0.008)
    G += (clarao + J * 1.1 + T.blur(J, 0.02) * 0.6 + anel + fa * 1.1) * env
    H += (clarao * 1.1 + J * 0.4 + anel * 0.3 + fa * 0.7) * env
    return G, H


# =================================================================== Arthas
def _runa(cx, cy, r, ang):
    """Uma runa angulosa (segmentos) para os círculos da Frostmourne."""
    pts = [(-0.5, -1), (0.2, -0.3), (-0.3, 0.2), (0.5, 1)]
    c, s = math.cos(ang), math.sin(ang)
    out = []
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        out.append((cx + r * (x1 * c - y1 * s), cy + r * (x1 * s + y1 * c), cx + r * (x2 * c - y2 * s), cy + r * (x2 * s + y2 * c), 1.0))
    return out


def _caveira(cx, cy, r):
    """Uma caveira simples: o crânio, o maxilar e os dois olhos (que entram como buracos)."""
    cranio = [(cx + r * math.cos(a), cy - 0.1 * r + r * 0.95 * math.sin(a)) for a in np.linspace(math.pi * 0.85, math.pi * 2.15, 20)]
    maxilar = [(cx + 0.55 * r, cy + 0.35 * r), (cx + 0.45 * r, cy + 0.8 * r), (cx - 0.45 * r, cy + 0.8 * r), (cx - 0.55 * r, cy + 0.35 * r)]
    olhos = [(cx - 0.38 * r, cy, 0.22 * r), (cx + 0.38 * r, cy, 0.22 * r)]
    return cranio + maxilar, olhos


def ceifadora_de_almas(T, t, rng):
    """A Ceifadora de Almas: a Frostmourne corta o rival na diagonal (a lâmina de gelo com as runas
    acendendo no corte), e a alma dele — uma chama fantasma — é arrancada e puxada de volta para a
    espada (−x), deixando o rastro."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    prog = ease_out(rel(t, 0.0, 0.18), 2)
    come = rel(t, 0.22, 0.5)
    corte = T.polys([(lamina(-0.6, -0.6, 0.6, 0.55, 0.075, prog, come), 1.0)], 0.004)
    gelo = T.blur(corte, 0.025)
    runas = T.zero()
    if t > 0.1:
        for j in range(4):
            f = 0.2 + 0.2 * j
            runas += T.lines(_runa(-0.6 + 1.2 * f, -0.6 + 1.15 * f, 0.05, 0.8), 0.008) * pulso(t, 0.1 + 0.03 * j, 0.6)
    k = pulso(t, 0.1, 0.4)
    clarao = T.gauss(0, 0, 0.2) * k * 1.3
    # a alma: uma chama clara que sai do rival e voa para −x, ondulando
    puxa = ease_in(rel(t, 0.35, 0.85), 1.6)
    ax = 0.0 - 1.1 * puxa
    ay = -0.05 + 0.08 * math.sin(TAU * t * 2)
    alma = (T.gauss(ax, ay, 0.07, 0.09) + T.gauss(ax + 0.08, ay - 0.04, 0.05, 0.04) * 0.6) * pulso(t, 0.3, 0.92)
    rastro = T.tapered([(ax + 0.6, ay + 0.04, ax + 0.05, ay, 1.0)], 0.1) * pulso(t, 0.4, 0.9) * 0.5
    sub = np.random.default_rng(31)
    cristais = []
    for _ in range(16):
        a = sub.uniform(0, TAU)
        d = 0.1 + 0.6 * ease_out(rel(t, 0.1, 0.7), 2) * sub.uniform(0.3, 1)
        cristais.append((d * math.cos(a), d * math.sin(a) + 0.2 * rel(t, 0.3, 1.0), pulso(t, 0.1, 0.8) * sub.uniform(0.4, 1)))
    G += (corte * 1.3 + gelo * 0.8 + runas * 1.2 + clarao + alma * 1.4 + T.blur(rastro, 0.02) + T.splats(cristais, 0.011)) * env
    H += (corte * 1.0 + runas * 0.7 + clarao * 0.9 + alma * 1.1) * env
    return G, H


def erguer_os_mortos(T, t, rng):
    """Erguer os mortos no aliado: o círculo de runas acende no chão, as mãos de osso sobem em volta
    dele (os dedos abertos) e se fecham num escudo, e a névoa fria fica girando."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    chao = 0.45
    acende = ease_out(rel(t, 0.0, 0.25), 2)
    circ = T.ring(0.75 * acende + 1e-3, 0.03, 0, chao, 3.2) + T.ring(0.55 * acende + 1e-3, 0.015, 0, chao, 3.2) * 0.6
    runas = T.zero()
    for j in range(8):
        a = TAU * j / 8 + t * 0.8
        runas += T.lines(_runa(0.65 * math.cos(a), chao + 0.65 / 3.2 * math.sin(a), 0.04, a), 0.007)
    runas *= acende
    maos = T.zero()
    for j, x in enumerate((-0.55, -0.3, 0.3, 0.55)):
        sobe = back(rel(t, 0.15 + 0.05 * j, 0.45 + 0.05 * j), 1.4)
        if sobe <= 0:
            continue
        topo = chao - 0.75 * sobe * (1.0 if abs(x) > 0.4 else 0.8)
        inclina = -0.25 * np.sign(x) * rel(t, 0.5, 0.7)
        maos += T.polyline([(x, chao), (x + inclina * 0.5, (chao + topo) / 2), (x + inclina, topo)], 0.045)
        maos += T.gauss(x + inclina, topo, 0.045) * 1.2
        for d in (-0.6, -0.2, 0.2, 0.6):
            a = -math.pi / 2 + d + inclina
            maos += T.polyline([(x + inclina, topo), (x + inclina + 0.15 * math.cos(a), topo + 0.15 * math.sin(a)), (x + inclina + 0.2 * math.cos(a + 0.3 * d), topo + 0.2 * math.sin(a + 0.3 * d))], 0.018)
    fecha = pulso(t, 0.5, 0.9)
    escudo = (T.ring(0.55, 0.035, 0, 0.0, 1.05) * 1.1 + np.clip(1 - T.RAD / 0.55, 0, 1) ** 0.6 * (T.RAD < 0.55) * 0.12) * rel(t, 0.5, 0.65)
    sub = np.random.default_rng(37)
    nevoa = T.splats([(0.6 * math.cos(TAU * (sub.uniform() + t * 0.3)), chao - 0.1 + 0.15 * math.sin(TAU * (sub.uniform() + t * 0.3)), sub.uniform(0.3, 0.8)) for _ in range(14)], 0.06) * 0.35
    G += (circ * 1.1 + runas * 1.1 + maos * 1.0 + escudo + nevoa + T.flare(-0.25, -0.35, 0.7 * fecha + 1e-3, 0.0, 0.01) * fecha) * env
    H += (circ * 0.5 + runas * 0.6 + maos * 0.3 + escudo * 0.3) * env
    return G, H


def runa_lich(T, t, rng):
    """O Preparo da Praga: as runas da Frostmourne girando em volta do Arthas em dois anéis, a névoa
    fria subindo e o brilho no meio."""
    G, H = vazio(T)
    runas = T.zero()
    for anel, (r, vel, n) in enumerate(((0.45, 1.0, 8), (0.7, -0.6, 11))):
        for j in range(n):
            a = TAU * j / n + TAU * t * vel / 3
            runas += T.lines(_runa(r * math.cos(a), r * 0.55 * math.sin(a), 0.05, a + 1.0), 0.008) * (0.6 + 0.4 * anel)
    aneis = T.ring(0.45, 0.012, 0, 0, 1 / 0.55) * 0.6 + T.ring(0.7, 0.012, 0, 0, 1 / 0.55) * 0.5
    sub = np.random.default_rng(41)
    nevoa = T.splats([(sub.normal(0, 0.35), 0.5 - 1.0 * ((sub.uniform() + t * 0.6) % 1), sub.uniform(0.3, 0.8)) for _ in range(16)], 0.07) * 0.4
    nucleo = T.gauss(0, 0, 0.14) * (0.8 + 0.2 * math.sin(TAU * t * 3))
    G += runas * 1.2 + aneis + nevoa + nucleo
    H += runas * 0.6 + nucleo * 0.9
    return G, H


def praga_da_carne(T, t, rng):
    """A Praga da Carne no campo dos rivais: a névoa doente rolando (o ruído correndo), as caveiras
    que se formam nela e somem, os cristais de gelo caindo, e no fim os fios de vida sugados indo
    embora para −x (a cura do Arthas)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    vem = ease_out(rel(t, 0.0, 0.3), 2)
    n = np.roll(_ruido(T, 43, 0.09, 3), int((t * 0.6 % 1) * T.W), axis=1)
    campo = np.exp(-(T.U / (0.95 * vem + 0.05)) ** 2 * 0.8) * np.exp(-((T.V - 0.1) / 0.55) ** 2)
    nevoa = np.clip(campo * (1.0 + 0.4 * n) - 0.25, 0, 1) * (1 - rel(t, 0.8, 1.0))
    caveiras = T.zero()
    olhos = T.zero()
    for j, (x, y) in enumerate(((-0.45, -0.05), (0.1, -0.25), (0.45, 0.1))):
        vivo = pulso(t, 0.2 + 0.12 * j, 0.65 + 0.12 * j)
        if vivo <= 0:
            continue
        forma, buracos = _caveira(x, y, 0.17)
        caveiras += T.polys([(forma, 1.0)], 0.008) * vivo
        olhos += T.splats([(ox, oy, 1.0) for ox, oy, _ in buracos], 0.028) * vivo
    caveiras = np.clip(caveiras - olhos * 1.5, 0, None)
    sub = np.random.default_rng(47)
    gelo = []
    for _ in range(26):
        f = (sub.uniform() + t * 1.1) % 1
        gelo.append((sub.uniform(-0.9, 0.9), -0.9 + 1.7 * f, rel(t, 0.15, 0.3) * (1 - rel(t, 0.8, 0.95)) * sub.uniform(0.4, 1)))
    G_ = T.splats(gelo, 0.01)
    fios = T.zero()
    suga = rel(t, 0.6, 0.95)
    if suga > 0:
        for j, y in enumerate((-0.25, 0.0, 0.25)):
            x = 0.3 - 1.4 * ease_in(suga, 1.4)
            fios += T.tapered([(x + 0.5, y * 0.6, x, y, 1.0)], 0.04)
        fios *= 1 - rel(t, 0.9, 1.0)
    G += (nevoa * 0.8 + caveiras * 1.1 + G_ * 1.2 + T.blur(fios, 0.01) * 1.1) * env
    H += (nevoa ** 3 * 0.3 + caveiras * 0.3 + G_ * 0.8 + fios * 0.6) * env
    return G, H


REGISTRO = [
    ("plasma_faixa", plasma_faixa, FAIXA, "Aiolia · os raios do Relâmpago de Plasma (faixa)", True),
    ("relampago_de_plasma", relampago_de_plasma, GRANDE, "Aiolia · os raios acertando o rival", False),
    ("velocidade_da_luz", velocidade_da_luz, GRANDE, "Aiolia · a grade de plasma cruzando o campo", False),
    ("cosmo_leao", cosmo_leao, MEDIA, "Aiolia · o cosmo dourado e a juba do leão (laço)", True),
    ("leao_dourado", leao_dourado, MEDIA, "Aiolia · o Rugido do Leão voando (laço)", True),
    ("rugido_do_leao", rugido_do_leao, GRANDE, "Aiolia · a explosão dourada com a juba", False),
    ("ceifadora_de_almas", ceifadora_de_almas, GRANDE, "Arthas · a Frostmourne corta e arranca a alma", False),
    ("erguer_os_mortos", erguer_os_mortos, GRANDE, "Arthas · as mãos de osso sobem e fecham o escudo", False),
    ("runa_lich", runa_lich, MEDIA, "Arthas · as runas girando no Preparo (laço)", True),
    ("praga_da_carne", praga_da_carne, GRANDE, "Arthas · a névoa da peste com caveiras e gelo", False),
]
