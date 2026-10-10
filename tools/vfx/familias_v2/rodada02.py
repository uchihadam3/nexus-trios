"""Rodada 2 das habilidades próprias: Wolverine, Batman, Thor, Doutor Estranho e Flash.

Wolverine
- garras_adamantium: as três garras cortam em X duas vezes, o brilho de metal
  correndo nelas, as faíscas e o sangue (perto).
- garras_cruzadas: "Na minha frente" — ele cruza as garras em X na frente do
  aliado e o brilho de aço vira o escudo.
- fator_de_cura: "Não acabou" — os cortes no corpo dele se fecham (os riscos
  vermelhos encolhendo), o vapor sobe e o brilho pulsa.

Batman
- visao_de_detetive: a Análise tática — o contorno do rival acende azul, as
  miras pequenas marcam os pontos fracos e a grade de leitura varre.
- batarangue_eletrico_voo: o batarangue elétrico girando no ar com a luz piscando
  (laço, viagem; o do ataque básico é outro).
- batarangue_eletrico: crava no rival, descarrega os arcos e o X do golpe cortado.
- capa_de_contingencia: o Plano de contingência no aliado — a bomba de fumaça
  estoura e a capa de morcego abre na frente dele como escudo.

Thor
- mjolnir_voando: o Mjolnir girando no ar com os raios no rastro (laço, viagem).
- mjolnir_impacto: o martelo bate, o trovão estoura e os raios saem do ponto.
- trovao_chamado: o Thor ergue o martelo e os raios caem nele do céu (Preparo).
- tempestade_thor: a Tempestade em cada rival — a nuvem escura girando em cima
  dele e os raios descendo nele.
- deus_do_trovao: o raio dourado gigante que cai do céu no rival, o chão
  estoura e os arcos ficam prendendo (paralisado).

Doutor Estranho
- escudo_serafim: o escudo de Serafim no aliado — a mandala laranja de runas,
  dois anéis girando em sentidos opostos e os quadrados de luz.
- laco_temporal: o Olho de Agamotto — os anéis verdes de relógio girando para
  trás em volta do rival e os ponteiros voltando.
- portal_estranho: o portal de faíscas abrindo no aliado — o anel de faíscas
  laranja girando e as fagulhas saindo pela tangente.

Flash
- mil_golpes_flash: os socos rápidos — pancadas em pontos diferentes, os riscos
  de raio amarelo e os vultos (perto).
- resgate_flash: o raio dá a volta no aliado num rastro e vira o escudo de raio.
- forca_de_aceleracao: "Além do tempo" — os raios da Força de Aceleração
  correndo em volta do aliado.
"""
from __future__ import annotations

import math

import numpy as np

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


def _tres_garras(x1, y1, x2, y2, larg, prog, gap=0.09):
    """As três garras paralelas de um golpe (lâminas finas lado a lado)."""
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy) + 1e-9
    nx, ny = -dy / n, dx / n
    return [(lamina(x1 + nx * gap * k, y1 + ny * gap * k, x2 + nx * gap * k, y2 + ny * gap * k, larg, prog), 1.0) for k in (-1, 0, 1)]


# =================================================================== Wolverine
def garras_adamantium(T, t, rng):
    """As Garras de adamantium: dois golpes de três garras cruzando em X, o brilho de metal correndo ao
    longo das garras, as faíscas do aço e o sangue espirrando."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    formas = []
    for (x1, y1, x2, y2), t0 in (((-0.6, -0.55, 0.6, 0.55), 0.0), ((0.6, -0.55, -0.6, 0.55), 0.16)):
        p = ease_out(rel(t, t0, t0 + 0.12), 2.5)
        if p > 0:
            formas += [(pts, w * (1 - rel(t, t0 + 0.25, t0 + 0.55))) for pts, w in _tres_garras(x1, y1, x2, y2, 0.035, p)]
    L = T.polys(formas, 0.003)
    brilho = T.zero()
    for (x1, y1, x2, y2), t0 in (((-0.6, -0.55, 0.6, 0.55), 0.05), ((0.6, -0.55, -0.6, 0.55), 0.21)):
        f = rel(t, t0, t0 + 0.15)
        if 0 < f < 1:
            brilho += T.gauss(x1 + (x2 - x1) * f, y1 + (y2 - y1) * f, 0.06) * 1.5
    sub = np.random.default_rng(3)
    sangue = T.splats([(d * math.cos(a), d * math.sin(a) + 0.4 * rel(t, 0.3, 1) ** 2, pulso(t, 0.2, 0.95) * sub.uniform(0.5, 1)) for a, d in ((sub.uniform(-math.pi, math.pi), 0.1 + 0.55 * ease_out(rel(t, 0.18, 0.6), 2) * sub.uniform(0.3, 1)) for _ in range(14))], 0.022)
    G += (L * 1.3 + T.blur(L, 0.012) * 0.5 + brilho + _faiscas(T, t, 5, 14, 0.08, 0.5, 0.01) * 1.1 + sangue * 0.6) * env
    H += (L * 0.5 + brilho * 0.9 + sangue * 0.15) * env
    return G, H


def garras_cruzadas(T, t, rng):
    """Na minha frente: o Wolverine cruza as garras em X na frente do aliado (as duas mãos de três garras
    se cruzam com o clang), o brilho de aço corre nelas e fica um escudo em X brilhando."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    p = ease_out(rel(t, 0.0, 0.25), 2.5)
    formas = _tres_garras(-0.55, 0.45, -0.55 + 1.1 * p, 0.45 - 0.9 * p, 0.04, 1.0, 0.08) + _tres_garras(0.55, 0.45, 0.55 - 1.1 * p, 0.45 - 0.9 * p, 0.04, 1.0, 0.08)
    X = T.polys(formas, 0.003)
    k = pulso(t, 0.22, 0.5)
    clang = T.gauss(0, 0.0, 0.12) * k * 1.6 + T.flare(0, 0, 1.0 * k + 1e-3, 0.8, 0.008) * k
    escudo = T.arc_band(0.62, 0.04, -2.5, -0.64, 1.0, 0.0, 0, 0.1, 0.2) * rel(t, 0.3, 0.45)
    corre = T.zero()
    f = rel(t, 0.35, 0.75)
    if 0 < f < 1:
        corre = T.gauss(-0.55 + 1.1 * f, 0.45 - 0.9 * f, 0.07) * 1.3
    G += (X * 1.2 + clang + escudo + corre + _faiscas(T, t, 7, 10, 0.22, 0.4, 0.01)) * env
    H += (X * 0.4 + clang * 0.9 + corre * 0.8) * env
    return G, H


def fator_de_cura(T, t, rng):
    """Não acabou: o fator de cura — os cortes no corpo dele (riscos vermelhos) encolhem até sumir, a
    pele se fecha em brilho, o vapor sobe e o pulso do coração acende."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    fecha = ease_in(rel(t, 0.1, 0.7), 1.5)
    sub = np.random.default_rng(11)
    cortes = []
    for _ in range(6):
        cx, cy = sub.uniform(-0.35, 0.35), sub.uniform(-0.35, 0.4)
        a = sub.uniform(-0.6, 0.6) + math.pi / 4
        meio = 0.18 * (1 - fecha) + 1e-3
        cortes.append((cx - meio * math.cos(a), cy - meio * math.sin(a), cx + meio * math.cos(a), cy + meio * math.sin(a), 1.0))
    C = T.lines(cortes, 0.018) * (1 - rel(t, 0.65, 0.75))
    brilho = T.zero()
    for c in cortes:
        brilho += T.gauss((c[0] + c[2]) / 2, (c[1] + c[3]) / 2, 0.035) * pulso(t, 0.5, 0.85) * 0.7
    vapor = T.splats([(sub.normal(0, 0.25), 0.5 - 1.0 * ((sub.uniform() + t * 0.7) % 1), (1 - ((sub.uniform() + t * 0.7) % 1)) * 0.6) for _ in range(20)], 0.05) * rel(t, 0.05, 0.25)
    bate = abs(math.sin(TAU * t * 2.2)) ** 6
    coracao = T.ring(0.35 + 0.15 * bate, 0.03) * bate * 0.7
    G += (C * 1.2 + brilho * 1.2 + vapor * 0.35 + coracao) * env
    H += (C * 0.3 + brilho * 0.8) * env
    return G, H


# =================================================================== Batman
def visao_de_detetive(T, t, rng):
    """A Análise tática: a visão de detetive — o contorno do rival acende (o anel achatado do corpo), a
    grade de leitura varre de cima a baixo, as miras pequenas marcam três pontos fracos uma por vez e o
    morcego da marca fica no meio."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    contorno = T.ring(0.42, 0.018, 0, 0, 0.75) * rel(t, 0.0, 0.15)
    y = -0.6 + 1.2 * rel(t, 0.05, 0.45)
    grade = T.lines([(-0.7, y, 0.7, y, 1.0)], 0.008) * pulso(t, 0.05, 0.5) + np.exp(-((T.V - y) / 0.08) ** 2) * np.exp(-(T.U / 0.6) ** 2) * 0.25 * pulso(t, 0.05, 0.5)
    miras = T.zero()
    for j, (x, yy) in enumerate(((-0.18, -0.2), (0.2, 0.05), (-0.05, 0.3))):
        t0 = 0.3 + 0.1 * j
        f = ease_out(rel(t, t0, t0 + 0.12), 2)
        r = 0.16 - 0.08 * f
        miras += (T.ring(r, 0.01, x, yy) + T.lines([(x - r - 0.04, yy, x - r + 0.02, yy, 1.0), (x + r - 0.02, yy, x + r + 0.04, yy, 1.0)], 0.008)) * rel(t, t0, t0 + 0.05)
    asas = [(-0.22, 0.0), (-0.12, -0.06), (-0.05, -0.02), (0.0, -0.08), (0.05, -0.02), (0.12, -0.06), (0.22, 0.0), (0.1, 0.02), (0.04, 0.08), (0.0, 0.04), (-0.04, 0.08), (-0.1, 0.02)]
    morcego = T.polys([([(x * 1.4, y2 * 1.4) for x, y2 in asas], 1.0)], 0.004) * rel(t, 0.6, 0.7) * 0.5
    G += (contorno * 1.1 + grade + miras * 1.2 + morcego * 0.9) * env
    H += (contorno * 0.3 + miras * 0.5) * env
    return G, H


_BAT = [(-0.3, 0.0), (-0.16, -0.08), (-0.07, -0.03), (0.0, -0.11), (0.07, -0.03), (0.16, -0.08), (0.3, 0.0), (0.14, 0.03), (0.05, 0.11), (0.0, 0.05), (-0.05, 0.11), (-0.14, 0.03)]


def _batarangue(cx, cy, s, ang):
    c, sn = math.cos(ang), math.sin(ang)
    return [(cx + (x * c - y * sn) * s, cy + (x * sn + y * c) * s) for x, y in _BAT]


def batarangue_eletrico_voo(T, t, rng):
    """O batarangue elétrico voando para +x (diferente do batarangue do ataque básico): o morcego de
    metal girando, a luz do detonador piscando no meio e os estalos azuis saindo das pontas."""
    G, H = vazio(T)
    cx = 0.2
    giro = TAU * t * 3
    pts = _batarangue(cx, 0, 1.2, giro)
    B = T.polys([(pts, 1.0)], 0.004)
    pisca = 1.0 if (t * 6) % 1 < 0.5 else 0.25
    luz = T.gauss(cx, 0, 0.04) * pisca * 1.6
    q = _quadro(t, 61)
    R = T.zero()
    for k in (0, 6):
        x, y = pts[k]
        a = q.uniform(0, TAU)
        R += _raio(T, q, x, y, x + 0.18 * math.cos(a), y + 0.18 * math.sin(a), 0.006, 2, 0.4)
    rastro = T.tapered([(cx - 0.9, 0, cx - 0.3, 0, 1.0)], 0.03) * 0.4
    G += B * 1.1 + luz + R + rastro
    H += B * 0.3 + luz * 0.9 + R * 0.5
    return G, H


def batarangue_eletrico(T, t, rng):
    """O batarangue elétrico crava no rival: chega girando, para com o "clank", a luz pisca rápido e
    descarrega — os arcos elétricos prendem o rival e o X do golpe cortado aparece."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    chega = ease_in(rel(t, 0.0, 0.15), 1.5)
    cx = -0.8 + 0.8 * chega
    giro = TAU * 2 * chega + 0.5
    some = 1 - rel(t, 0.6, 0.8)
    B = T.polys([(_batarangue(cx, 0, 1.3, giro), 1.0)], 0.004) * some
    k = pulso(t, 0.14, 0.35)
    clank = T.gauss(0, 0, 0.1) * k * 1.4
    pisca = (1.0 if (t * 14) % 1 < 0.5 else 0.2) * rel(t, 0.15, 0.2) * (1 - rel(t, 0.38, 0.4))
    luz = T.gauss(cx, 0, 0.04) * pisca * 1.6
    q = _quadro(t, 67)
    arcos = T.zero()
    descarga = pulso(t, 0.38, 0.85)
    if descarga > 0:
        for _ in range(7):
            a = q.uniform(0, TAU)
            arcos += _raio(T, q, 0, 0, 0.6 * math.cos(a), 0.55 * math.sin(a), 0.01, 4, 0.35)
        arcos *= descarga
    estouro = T.gauss(0, 0, 0.2) * pulso(t, 0.38, 0.6) * 1.2
    X = T.lines([(-0.2, -0.2, 0.2, 0.2, 1.0), (-0.2, 0.2, 0.2, -0.2, 1.0)], 0.035) * pulso(t, 0.45, 0.92)
    G += (B * 1.1 + clank + luz + arcos * 1.2 + estouro + X) * env
    H += (B * 0.3 + luz + arcos * 0.7 + estouro * 0.8 + X * 0.4) * env
    return G, H


def capa_de_contingencia(T, t, rng):
    """O Plano de contingência no aliado: a bomba de fumaça estoura (a nuvem cinza que abre), e a capa
    de morcego abre na frente dele — as duas asas recortadas descendo e firmando como escudo."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    sub = np.random.default_rng(17)
    fumaca = T.splats([(d * math.cos(a), d * math.sin(a) * 0.7, pulso(t, 0.0, 0.8) * sub.uniform(0.4, 0.8)) for a, d in ((sub.uniform(0, TAU), 0.05 + 0.5 * ease_out(rel(t, 0.0, 0.5), 2) * sub.uniform(0.3, 1)) for _ in range(24))], 0.08)
    abre = ease_out(rel(t, 0.15, 0.45), 2.5)
    w = 0.65 * abre + 0.02
    asa = [(-w, -0.35), (-w * 0.55, -0.42), (0.0, -0.3), (w * 0.55, -0.42), (w, -0.35),
           (w * 0.92, 0.0), (w * 0.75, 0.4), (w * 0.5, 0.25), (w * 0.25, 0.45), (0.0, 0.3),
           (-w * 0.25, 0.45), (-w * 0.5, 0.25), (-w * 0.75, 0.4), (-w * 0.92, 0.0)]
    capa = T.polys([(asa, 1.0)], 0.006) * rel(t, 0.15, 0.25)
    borda = T.polyline(asa + [asa[0]], 0.012) * rel(t, 0.15, 0.25)
    G += (fumaca * 0.45 + capa * 0.45 + borda * 1.2 + T.gauss(0, 0, 0.3) * pulso(t, 0.4, 0.7) * 0.4) * env
    H += (borda * 0.4) * env
    return G, H


# =================================================================== Thor
def _martelo(cx, cy, s, ang):
    """O Mjolnir: a cabeça retangular e o cabo curto, girado."""
    cabeca = [(-0.16, -0.1), (0.16, -0.1), (0.16, 0.1), (-0.16, 0.1)]
    cabo = [(-0.03, 0.1), (0.03, 0.1), (0.03, 0.34), (-0.03, 0.34)]
    c, sn = math.cos(ang), math.sin(ang)
    gira = lambda pts: [(cx + (x * c - y * sn) * s, cy + (x * sn + y * c) * s) for x, y in pts]  # noqa: E731
    return gira(cabeca), gira(cabo)


def mjolnir_voando(T, t, rng):
    """O Mjolnir voando para +x: o martelo girando, os raios saindo dele e o rastro elétrico."""
    G, H = vazio(T)
    cx = 0.2
    cab, cabo = _martelo(cx, 0, 1.1, TAU * t * 2.5)
    M = T.polys([(cab, 1.0), (cabo, 0.8)], 0.004)
    q = _quadro(t, 19)
    R = T.zero()
    for _ in range(3):
        a = q.uniform(0, TAU)
        R += _raio(T, q, cx, 0, cx + 0.35 * math.cos(a), 0.35 * math.sin(a), 0.008, 3, 0.4)
    R += _raio(T, q, cx - 0.1, 0, cx - 0.95, q.uniform(-0.1, 0.1), 0.01, 4, 0.25) * 0.8
    G += M * 1.2 + R * 1.1 + T.gauss(cx, 0, 0.2) * 0.4
    H += M * 0.4 + R * 0.6
    return G, H


def mjolnir_impacto(T, t, rng):
    """O Mjolnir bate: o trovão estoura no ponto (o clarão e o anel), os raios saem em estrela e o
    golpe cortado (o rival perde o tempo)."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    k = pulso(t, 0.0, 0.4)
    clarao = T.gauss(0, 0, 0.22) * k * 2.0 + T.flare(0, 0, 1.3 * k + 1e-3, 0.0, 0.01) * k
    anel = T.ring(0.12 + 0.7 * ease_out(rel(t, 0.0, 0.45), 2), 0.04, 0, 0, 1.3) * pulso(t, 0.0, 0.5)
    q = _quadro(t, 23)
    R = T.zero()
    if t < 0.55:
        for _ in range(6):
            a = q.uniform(0, TAU)
            R += _raio(T, q, 0, 0, 0.75 * math.cos(a), 0.75 * math.sin(a), 0.012, 4, 0.3)
        R *= 1 - rel(t, 0.3, 0.55)
    G += (clarao + anel + R * 1.2) * env
    H += (clarao * 1.1 + R * 0.7) * env
    return G, H


def trovao_chamado(T, t, rng):
    """O Thor erguendo o martelo e chamando o trovão: os raios caem do céu nele (de cima, sempre novos),
    o martelo brilha no alto e a aura elétrica em volta."""
    G, H = vazio(T)
    q = _quadro(t, 29)
    R = T.zero()
    for _ in range(2):
        x = q.uniform(-0.3, 0.3)
        R += _raio(T, q, x, -1.0, 0.0, -0.45, 0.012, 5, 0.3)
    topo = T.gauss(0, -0.45, 0.1) * (0.8 + 0.4 * q.uniform())
    aura = T.ring(0.45, 0.03) * (0.6 + 0.4 * q.uniform())
    arcos = T.zero()
    for _ in range(2):
        a = q.uniform(0, TAU)
        b = a + q.uniform(0.6, 1.4)
        arcos += _raio(T, q, 0.45 * math.cos(a), 0.45 * math.sin(a), 0.45 * math.cos(b), 0.45 * math.sin(b), 0.008, 3, 0.3)
    G += R * 1.3 + T.blur(R, 0.02) * 0.5 + topo * 1.4 + aura * 0.6 + arcos
    H += R * 0.8 + topo
    return G, H


def tempestade_thor(T, t, rng):
    """A Tempestade em cada rival: a nuvem escura se junta em cima dele e gira (o miolo escuro e a borda
    acesa), e três raios descem nele um depois do outro, cada um com o estouro no corpo."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    junta = ease_out(rel(t, 0.0, 0.2), 2)
    n = np.roll(_ruido(T, 31, 0.07, 3), int((t * 0.5 % 1) * T.W), axis=1)
    forma = np.exp(-((T.V + 0.42) / 0.15) ** 2 - (T.U / (0.5 * junta + 0.05)) ** 2)
    nuvem = np.clip(forma * (0.75 + 0.6 * n) - 0.3, 0, 1)
    borda = np.clip(nuvem - T.blur(nuvem, 0.02) * 0.9, 0, 1) * 3
    raios = T.zero()
    estouros = T.zero()
    for j, x in enumerate((-0.12, 0.1, 0.0)):
        t0 = 0.18 + 0.17 * j
        vivo = pulso(t, t0, t0 + 0.16)
        if vivo <= 0:
            continue
        q = np.random.default_rng(37 + j + int(t * 40))
        raios += _raio(T, q, x * 2.5, -0.4, x, 0.0, 0.016, 5, 0.25) * vivo
        estouros += T.gauss(x, 0.0, 0.08) * vivo
    G += (nuvem * 0.4 + np.clip(borda, 0, 1) * 0.6 + raios * 1.4 + T.blur(raios, 0.02) * 0.6 + estouros * 1.2) * env
    H += (raios * 0.9 + estouros) * env
    return G, H


def deus_do_trovao(T, t, rng):
    """O Deus do Trovão: o raio gigante cai do céu no rival (a coluna larga e o miolo branco), o chão
    estoura num anel achatado, e os arcos ficam estalando em volta dele (paralisado)."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    desce = ease_in(rel(t, 0.0, 0.12), 1.5)
    fundo = -1.0 + 1.5 * desce
    vivo = 1 - rel(t, 0.35, 0.55)
    q = _quadro(t, 41)
    pts = []
    for k in range(14):
        y = -1.0 + (fundo + 1.0) * k / 13
        pts.append((q.normal(0, 0.04) if 0 < k < 13 else 0.0, y))
    coluna = T.polyline(pts, 0.06) * vivo
    miolo = T.polyline(pts, 0.02) * vivo
    k = pulso(t, 0.1, 0.45)
    clarao = T.gauss(0, 0.45, 0.22, 0.07) * k * 1.6 + T.gauss(0, 0.1, 0.12) * k * 0.8
    chao = T.ring(0.1 + 0.85 * ease_out(rel(t, 0.12, 0.5), 2), 0.04, 0, 0.5, 4.0) * pulso(t, 0.12, 0.6)
    arcos = T.zero()
    if t > 0.35:
        for _ in range(3):
            a = q.uniform(0, TAU)
            b = a + q.uniform(0.6, 1.5)
            arcos += _raio(T, q, 0.35 * math.cos(a), 0.3 * math.sin(a), 0.35 * math.cos(b), 0.3 * math.sin(b), 0.01, 3, 0.35)
    G += (coluna * 1.1 + T.blur(coluna, 0.04) * 0.6 + miolo * 1.4 + clarao + chao + arcos * 1.1) * env
    H += (miolo * 1.4 + clarao + arcos * 0.6) * env
    return G, H


# =================================================================== Doutor Estranho
def escudo_serafim(T, t, rng):
    """O Escudo de Serafim no aliado: a mandala laranja abre — o anel de fora com as runas (tracinhos),
    o anel de dentro girando ao contrário, os dois quadrados de luz cruzados e o brilho do meio."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = back(rel(t, 0.0, 0.3), 1.4)
    R = 0.6 * abre + 1e-3
    g1, g2 = TAU * t * 0.4, -TAU * t * 0.6
    fora = T.ring(R, 0.02) + T.ring(R * 0.88, 0.01)
    runas = T.lines([(R * 0.9 * math.cos(a), R * 0.9 * math.sin(a), R * 0.98 * math.cos(a), R * 0.98 * math.sin(a), 1.0) for a in np.linspace(0, TAU, 33)[:-1] + g1], 0.008)
    dentro = T.ring(R * 0.55, 0.012)
    quad = []
    for g in (g2, g2 + math.pi / 4):
        pts = [(R * 0.62 * math.cos(g + TAU * k / 4), R * 0.62 * math.sin(g + TAU * k / 4)) for k in range(4)]
        quad.append(pts + [pts[0]])
    Q = T.polyline(quad[0], 0.01) + T.polyline(quad[1], 0.01)
    G += (fora * 1.2 + runas + dentro + Q * 0.9 + T.gauss(0, 0, 0.25) * 0.3 * abre) * env
    H += (fora * 0.4 + Q * 0.3) * env
    return G, H


def laco_temporal(T, t, rng):
    """O Laço temporal: o Olho de Agamotto abre em cima e os anéis verdes de relógio aparecem em volta do
    rival girando para trás, com as marcas das horas, e os dois ponteiros voltando rápido."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = ease_out(rel(t, 0.0, 0.25), 2)
    volta = -TAU * t * 1.5
    A = T.zero()
    for j, (r, sq) in enumerate(((0.55, 0.45), (0.42, 0.75), (0.62, 1.0))):
        A += T.ring(r * abre + 1e-3, 0.012, 0, 0, 1 / sq if sq < 1 else 1.0) * (0.8 - 0.15 * j)
    horas = T.lines([(0.5 * abre * math.cos(a), 0.5 * abre * math.sin(a), 0.58 * abre * math.cos(a), 0.58 * abre * math.sin(a), 1.0) for a in np.linspace(0, TAU, 13)[:-1] + volta * 0.3], 0.01)
    ponteiros = T.lines([(0, 0, 0.4 * abre * math.cos(volta), 0.4 * abre * math.sin(volta), 1.0), (0, 0, 0.25 * abre * math.cos(volta / 12), 0.25 * abre * math.sin(volta / 12), 1.0)], 0.014)
    olho = (T.gauss(0, -0.75, 0.08, 0.04) + T.ring(0.08, 0.01, 0, -0.75, 2.0)) * rel(t, 0.0, 0.15)
    G += (A * 1.1 + horas + ponteiros * 1.2 + olho * 1.3 + T.gauss(0, 0, 0.12) * 0.6 * abre) * env
    H += (ponteiros * 0.4 + olho) * env
    return G, H


def portal_estranho(T, t, rng):
    """O portal de faíscas no aliado: o anel de faíscas laranja abre girando (pontinhos correndo no
    círculo) e as fagulhas saem pela tangente, como de uma roda."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    abre = back(rel(t, 0.0, 0.3), 1.5)
    R = 0.55 * abre + 1e-3
    sub = np.random.default_rng(43)
    pts = []
    for _ in range(70):
        a = sub.uniform(0, TAU) + TAU * t * 1.8
        r = R * sub.uniform(0.94, 1.06)
        pts.append((r * math.cos(a), r * math.sin(a) * 0.95, sub.uniform(0.5, 1)))
    anel = T.splats(pts, 0.012)
    tang = []
    for _ in range(14):
        a = sub.uniform(0, TAU) + TAU * t * 1.8
        f = (sub.uniform() + t * 2.5) % 1
        x0, y0 = R * math.cos(a), R * math.sin(a) * 0.95
        tx, ty = -math.sin(a), math.cos(a)
        tang.append((x0 + tx * 0.35 * f, y0 + ty * 0.35 * f + 0.2 * f * f, (1 - f) * 0.9))
    G += (anel * 1.2 + T.ring(R, 0.02) * 0.5 + T.splats(tang, 0.01) + T.gauss(0, 0, R * 0.8) * 0.15) * env
    H += anel * 0.5 * env
    return G, H


# =================================================================== Flash
def mil_golpes_flash(T, t, rng):
    """Mil golpes: o Flash bate em vários pontos rápido demais (cada pancada um clarão pequeno), os riscos
    de raio amarelo cruzando entre elas, os vultos dele em volta e o último golpe maior."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    pontos = [(-0.2, -0.2), (0.22, 0.05), (-0.1, 0.25), (0.15, -0.25), (-0.28, 0.08), (0.05, 0.0), (0.25, 0.22), (-0.15, -0.05)]
    P = T.zero()
    for j, (x, y) in enumerate(pontos):
        t0 = 0.05 * j
        k = pulso(t, t0, t0 + 0.1)
        if k > 0:
            P += T.gauss(x, y, 0.08) * k * 1.4
    q = _quadro(t, 47)
    R = T.zero()
    if t < 0.5:
        for _ in range(3):
            a, b = q.integers(0, len(pontos), 2)
            (x1, y1), (x2, y2) = pontos[a], pontos[b]
            R += _raio(T, q, x1, y1, x2 + 1e-3, y2, 0.008, 3, 0.35)
    vultos = T.zero()
    for j in range(3):
        a = TAU * j / 3 + t * 8
        vultos += T.gauss(0.55 * math.cos(a), 0.45 * math.sin(a), 0.07, 0.14) * 0.4 * (1 - rel(t, 0.4, 0.6))
    k = pulso(t, 0.42, 0.8)
    final = T.gauss(0, 0, 0.1) * k * 1.3 + T.ring(0.1 + 0.6 * ease_out(rel(t, 0.42, 0.8), 2), 0.03) * k
    G += (P + R * 1.2 + vultos + final) * env
    H += (P * 0.9 + R * 0.6 + final * 0.9) * env
    return G, H


def resgate_flash(T, t, rng):
    """O Resgate instantâneo: um rastro de raio dá a volta no aliado (a cabeça clara correndo no círculo,
    a cauda sumindo) e fecha num anel elétrico que vira o escudo."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    volta = ease_in(rel(t, 0.0, 0.35), 1.3)
    a = -math.pi / 2 + TAU * volta
    rastro = T.arc_band(0.55, 0.04, a - 2.2, a, 1.0, 0.0, 0, 0, 1.0) * (1 - rel(t, 0.35, 0.45))
    cabeca = T.gauss(0.55 * math.cos(a), 0.55 * math.sin(a), 0.07) * 1.5 * (1 - rel(t, 0.35, 0.4))
    q = _quadro(t, 53)
    anel = T.ring(0.55, 0.03) * rel(t, 0.35, 0.45)
    arcos = T.zero()
    if t > 0.35:
        for _ in range(3):
            b = q.uniform(0, TAU)
            arcos += _raio(T, q, 0.55 * math.cos(b), 0.55 * math.sin(b), 0.55 * math.cos(b + 0.8), 0.55 * math.sin(b + 0.8), 0.008, 3, 0.35)
    G += (rastro * 1.1 + cabeca + anel * 1.1 + arcos) * env
    H += (cabeca + arcos * 0.5) * env
    return G, H


def forca_de_aceleracao(T, t, rng):
    """Além do tempo: a Força de Aceleração no aliado — os raios amarelos correm em volta dele em duas
    órbitas (elipses que giram), estalando, e o brilho de velocidade sobe."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = _quadro(t, 59)
    R = T.zero()
    for j in range(2):
        a = TAU * t * 2.2 + math.pi * j
        pts = [(0.5 * math.cos(a - k * 0.18) + q.normal(0, 0.015), 0.32 * math.sin(a - k * 0.18) * (1 if j else -1) + q.normal(0, 0.015)) for k in range(12)]
        R += T.polyline(pts, 0.014)
        R += T.gauss(pts[0][0], pts[0][1], 0.05) * 1.3
    sobe = T.splats([(q.normal(0, 0.3), 0.5 - 1.0 * f, 1 - f) for f in q.uniform(0, 1, 12)], 0.01)
    G += (R * 1.2 + T.blur(R, 0.02) * 0.5 + sobe * 0.6) * env * rel(t, 0.0, 0.1)
    H += R * 0.6 * env
    return G, H


REGISTRO = [
    ("garras_adamantium", garras_adamantium, GRANDE, "Wolverine · as garras cortando em X", False),
    ("garras_cruzadas", garras_cruzadas, GRANDE, "Wolverine · as garras cruzadas na frente do aliado", False),
    ("fator_de_cura", fator_de_cura, GRANDE, "Wolverine · os cortes fechando (fator de cura)", False),
    ("visao_de_detetive", visao_de_detetive, GRANDE, "Batman · a visão de detetive no rival", False),
    ("batarangue_eletrico_voo", batarangue_eletrico_voo, MEDIA, "Batman · o batarangue elétrico voando (laço)", True),
    ("batarangue_eletrico", batarangue_eletrico, GRANDE, "Batman · o batarangue elétrico descarregando", False),
    ("capa_de_contingencia", capa_de_contingencia, GRANDE, "Batman · a fumaça e a capa de escudo", False),
    ("mjolnir_voando", mjolnir_voando, MEDIA, "Thor · o Mjolnir voando (laço)", True),
    ("mjolnir_impacto", mjolnir_impacto, GRANDE, "Thor · o martelo batendo e o trovão", False),
    ("trovao_chamado", trovao_chamado, MEDIA, "Thor · os raios caindo nele (Preparo, laço)", True),
    ("tempestade_thor", tempestade_thor, GRANDE, "Thor · a nuvem e os raios em cada rival", False),
    ("deus_do_trovao", deus_do_trovao, GRANDE, "Thor · o raio gigante do céu", False),
    ("escudo_serafim", escudo_serafim, GRANDE, "Doutor Estranho · a mandala do Escudo de Serafim", False),
    ("laco_temporal", laco_temporal, GRANDE, "Doutor Estranho · os anéis de relógio voltando", False),
    ("portal_estranho", portal_estranho, GRANDE, "Doutor Estranho · o portal de faíscas", False),
    ("mil_golpes_flash", mil_golpes_flash, GRANDE, "Flash · os socos rápidos com raios", False),
    ("resgate_flash", resgate_flash, GRANDE, "Flash · o raio dando a volta no aliado", False),
    ("forca_de_aceleracao", forca_de_aceleracao, GRANDE, "Flash · a Força de Aceleração no aliado", False),
]
