"""Rodada 1 das habilidades próprias: Vegeta, Gojo, Light, Pikachu e Saitama.

Vegeta
- galick_carga: as duas mãos juntas de lado, a energia roxa juntando com os
  raios estalando (ergue: em quem age, antes do feixe sair).
- galick_faixa: o feixe roxo da Galick Gun, com raios enrolados nele (faixa).
- galick_impacto: a explosão roxa com os raios saindo.
- orgulho_saiyajin: "Não vou cair" — a aura dourada explode nele, as labaredas
  pontudas sobem, os raios, as pedras subindo e o chão afundando.
- final_flash_carga: os braços abertos, uma luz em cada mão, que se juntam
  numa bola enorme na frente dele (ergue).
- final_flash_faixa: o feixe dourado gigante, largo, com anéis de choque perto
  da boca (faixa).
- final_flash_impacto: a explosão enorme, com o domo e os raios de luz.

Gojo
- azul_gojo: o Azul — um ponto azul que suga tudo em espiral, os anéis
  fechando e o espaço entortando em volta.
- vermelho_bola: a bola vermelha do Vermelho voando (laço, viagem).
- vermelho_gojo: o Vermelho estourando — tudo empurrado para fora, os anéis
  abrindo rápido e os riscos saindo do centro.
- seis_olhos: os Seis Olhos acendendo nele (nele).
- vazio_infinito: o Vazio Infinito no meio dos rivais — a esfera escura com
  borda acesa, as estrelas, os braços de galáxia girando e a informação
  correndo para dentro.

Light Yagami
- investigacao_light: a mira fecha no rival, a linha de leitura varre de cima
  a baixo e as colunas de dados correm do lado.
- xeque_light: "Tudo conforme o plano" — a peça do rei do xadrez desce sobre o
  rival, bate, e a marca vermelha fica.

Pikachu
- bochechas_pikachu: as bochechas faiscando antes do Choque do Trovão (ergue).
- trovao_faixa: o raio grosso em zigue-zague, com galhos, piscando (faixa).
- trovao_pikachu: o raio estoura no rival e os arcos dançam no corpo.
- onda_choque_voo: os anéis elétricos voando (laço, viagem).
- onda_paralisa: os anéis fecham em volta do rival e prendem, com faíscas.
- agilidade_pikachu: os rastros amarelos girando em volta do aliado, os vultos
  e as faíscas.

Saitama
- passo_lateral: ele aparece na frente do aliado — a capa vermelha varre de
  lado, a poeira do passo e a capa vira o escudo.
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


def _faiscas(T, t, seed, n, t0, alcance=0.7, tam=0.012, cx=0.0, cy=0.0):
    sub = np.random.default_rng(seed)
    pts = []
    for _ in range(n):
        a = sub.uniform(0, TAU)
        d = 0.08 + alcance * ease_out(rel(t, t0, t0 + 0.55), 2) * sub.uniform(0.3, 1)
        pts.append((cx + d * math.cos(a), cy + d * math.sin(a), pulso(t, t0, 0.9) * sub.uniform(0.4, 1)))
    return T.splats(pts, tam)


# =================================================================== Vegeta
def galick_carga(T, t, rng):
    """As mãos do Vegeta juntas de lado e a energia roxa juntando: a bola cresce, os raios curtos
    estalam em volta (novos a cada quadro) e no fim ela brilha forte, pronta para sair."""
    G, H = vazio(T)
    cresce = ease_out(rel(t, 0.0, 0.8), 2)
    q = _quadro(t, 3)
    bola = T.gauss(0.1, 0, 0.05 + 0.12 * cresce)
    R = T.zero()
    for _ in range(5):
        a = q.uniform(0, TAU)
        r0 = 0.05 + 0.1 * cresce
        R += _raio(T, q, 0.1 + r0 * math.cos(a), r0 * math.sin(a), 0.1 + (r0 + 0.3) * math.cos(a), (r0 + 0.3) * math.sin(a), 0.009, 3, 0.4)
    maos = T.arc_band(0.22, 0.05, math.pi * 0.6, math.pi * 1.4, 1.0, 0.0, 0.18, 0.0, 0.3) * 0.45
    k = pulso(t, 0.82, 1.0)
    G += bola * (1.4 + k) + R * 1.1 + maos + T.gauss(0.1, 0, 0.3) * k * 0.8
    H += bola * 1.3 + R * 0.6
    return G, H


def galick_faixa(T, t, rng):
    """O feixe roxo da Galick Gun: o corpo com a borda irregular, o miolo claro, e raios finos
    enrolados correndo ao longo dele (novos a cada quadro)."""
    G, H = vazio(T)
    alto = T.H / T.W
    n = np.roll(_ruido(T, 7, 0.035, 3), int((t % 1) * T.W), axis=1)
    larg = alto * (0.34 + 0.07 * n)
    corpo = np.clip(1 - (np.abs(T.V) / larg) ** 2, 0, 1)
    miolo = np.exp(-(T.V / (alto * 0.1)) ** 2)
    q = _quadro(t, 9)
    R = T.zero()
    for _ in range(4):
        x = q.uniform(-0.95, 0.7)
        s = 1 if q.uniform() < 0.5 else -1
        R += _raio(T, q, x, s * alto * 0.3, x + 0.35, -s * alto * 0.3, 0.007, 3, 0.35)
    boca = T.gauss(-0.95, 0, 0.06, alto * 0.5)
    G += corpo * 0.85 + miolo * 1.3 + R * 1.1 + boca
    H += miolo * 1.3 + R * 0.6 + boca * 0.6
    return G, H


def galick_impacto(T, t, rng):
    """A Galick Gun estourando: o clarão roxo, a bola de energia abrindo, o anel e os raios saindo
    do centro para todos os lados."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    k = pulso(t, 0.0, 0.45)
    clarao = T.gauss(0, 0, 0.26) * k * 2.0 + T.flare(0, 0, 1.3 * k + 1e-3, 0.4, 0.01) * k
    bola = T.gauss(0, 0, 0.18 + 0.2 * ease_out(rel(t, 0.0, 0.45), 2)) * pulso(t, 0.0, 0.7) * 0.7
    anel = T.ring(0.15 + 0.7 * ease_out(rel(t, 0.0, 0.5), 2), 0.035) * pulso(t, 0.0, 0.55)
    q = _quadro(t, 11)
    R = T.zero()
    if t < 0.6:
        for _ in range(6):
            a = q.uniform(0, TAU)
            comp = 0.3 + 0.5 * ease_out(rel(t, 0.0, 0.35), 2)
            R += _raio(T, q, 0.05 * math.cos(a), 0.05 * math.sin(a), comp * math.cos(a), comp * math.sin(a), 0.01, 4, 0.3)
        R *= 1 - rel(t, 0.3, 0.6)
    G += (clarao + bola + anel + R * 1.2 + _faiscas(T, t, 13, 16, 0.0) * 0.9) * env
    H += (clarao * 1.1 + bola * 0.4 + R * 0.7) * env
    return G, H


def orgulho_saiyajin(T, t, rng):
    """"Não vou cair": a aura dourada de Super Saiyajin explode no Vegeta — o anel de choque achatado no
    chão, as labaredas pontudas subindo e tremendo, os raios finos, as pedrinhas subindo e o brilho."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    k = pulso(t, 0.0, 0.35)
    estouro = T.gauss(0, 0.05, 0.25) * k * 1.6
    choque = T.ring(0.1 + 0.85 * ease_out(rel(t, 0.0, 0.45), 2), 0.035, 0, 0.55, 4.0) * pulso(t, 0.0, 0.5)
    q = _quadro(t, 17)
    sobe = ease_out(rel(t, 0.05, 0.3), 2)
    formas = []
    for j in range(16):
        x = -0.45 + 0.9 * j / 15
        alto = (0.55 + 0.45 * q.uniform()) * (1 - 0.6 * abs(x)) * sobe
        formas.append((lamina(x * 0.95, 0.55, x * 0.55 + q.normal(0, 0.04), 0.55 - alto - 0.1, 0.075), q.uniform(0.55, 1)))
    aura = T.polys(formas, 0.01)
    R = T.zero()
    for _ in range(3):
        x = q.uniform(-0.4, 0.4)
        R += _raio(T, q, x, 0.45, x + q.normal(0, 0.12), -0.45, 0.008, 3, 0.4)
    sub = np.random.default_rng(19)
    pedras = T.splats([(sub.uniform(-0.6, 0.6), 0.55 - 0.9 * ((sub.uniform() + t * 0.8) % 1) * rel(t, 0.1, 0.3), sub.uniform(0.4, 0.9)) for _ in range(14)], 0.022)
    G += (estouro + choque * 1.1 + aura * 0.95 + T.blur(aura, 0.03) * 0.5 + R * 1.2 + pedras * 0.6) * env
    H += (estouro + aura * 0.45 + R * 0.7) * env
    return G, H


def final_flash_carga(T, t, rng):
    """O Final Flash juntando: os braços abertos, uma luz em cada mão (bem para os lados), que correm
    uma para a outra e se juntam numa bola enorme na frente dele, com o brilho estourando."""
    G, H = vazio(T)
    junta = ease_in(rel(t, 0.15, 0.65), 1.6)
    x = 0.75 * (1 - junta)
    lados = (T.gauss(x, 0, 0.08) + T.gauss(-x, 0, 0.08)) * (1 - rel(t, 0.62, 0.7))
    rastros = T.tapered([(0.8, 0.0, x + 1e-3, 0.0, 1.0), (-0.8, 0.0, -x - 1e-3, 0.0, 1.0)], 0.04) * rel(t, 0.15, 0.3) * (1 - rel(t, 0.6, 0.7))
    bola = T.gauss(0, 0, 0.08 + 0.18 * rel(t, 0.62, 0.95)) * rel(t, 0.6, 0.7)
    k = pulso(t, 0.62, 1.0)
    raios = T.tapered([(0.0, 0.0, 0.7 * math.cos(a) + 1e-3, 0.7 * math.sin(a), 1.0) for a in np.linspace(0, TAU, 13)[:-1] + t], 0.03) * k * 0.6
    G += lados * 1.6 + rastros * 0.6 + bola * 1.7 + raios
    H += lados * 1.4 + bola * 1.6
    return G, H


def final_flash_faixa(T, t, rng):
    """O feixe do Final Flash: dourado, muito largo, com o miolo branco, a borda ondulando para a frente
    e os anéis de choque perto da boca, que nascem e correm."""
    G, H = vazio(T)
    alto = T.H / T.W
    n = np.roll(_ruido(T, 23, 0.05, 3), int((t % 1) * T.W), axis=1)
    larg = alto * (0.44 + 0.05 * n)
    corpo = np.clip(1 - (np.abs(T.V) / larg) ** 2, 0, 1)
    miolo = np.exp(-(T.V / (alto * 0.18)) ** 2)
    aneis = T.zero()
    for j in range(3):
        f = (j / 3 + t) % 1
        x = -0.9 + 0.7 * f
        aneis += np.exp(-((T.U - x) / 0.015) ** 2) * np.exp(-(T.V / (alto * (0.45 + 0.1 * f))) ** 2) * (1 - f)
    boca = T.gauss(-0.95, 0, 0.08, alto * 0.6) * 1.3
    G += corpo * 0.95 + miolo * 1.4 + aneis * 0.9 + boca
    H += miolo * 1.5 + corpo * 0.25 + boca * 0.8
    return G, H


def final_flash_impacto(T, t, rng):
    """O Final Flash no rival: o clarão enorme, o domo de luz que cresce, os raios de luz saindo por
    trás e o anel largo varrendo."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    k = pulso(t, 0.0, 0.5)
    clarao = T.gauss(0, 0, 0.22) * k * 2.0 + T.flare(0, 0, 1.3 * k + 1e-3, 0.0, 0.01) * k
    domo = T.gauss(0, 0, 0.15 + 0.18 * ease_out(rel(t, 0.0, 0.5), 2)) * pulso(t, 0.0, 0.8) * 0.8
    raios = T.tapered([(0.1 * math.cos(a), 0.1 * math.sin(a), 0.85 * math.cos(a) + 1e-3, 0.85 * math.sin(a), 1.0) for a in np.linspace(0, TAU, 11)[:-1] + 0.2], 0.06) * pulso(t, 0.05, 0.6) * 0.7
    anel = T.ring(0.15 + 0.8 * ease_out(rel(t, 0.05, 0.6), 2), 0.05, 0, 0, 1.4) * pulso(t, 0.05, 0.65)
    G += (clarao + domo + raios + anel + _faiscas(T, t, 29, 20, 0.05, 0.8) * 0.8) * env
    H += (clarao * 1.2 + domo * 0.6 + raios * 0.4) * env
    return G, H


# =================================================================== Gojo
def azul_gojo(T, t, rng):
    """O Azul: um ponto azul muito forte no rival que puxa tudo — os riscos vêm de fora em espiral para
    dentro, os anéis fecham, e o espaço em volta entorta (o anel grosso e borrado)."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    nasce = ease_out(rel(t, 0.0, 0.2), 2)
    ponto = T.gauss(0, 0, 0.06 * nasce + 1e-3) * 1.8 + T.gauss(0, 0, 0.16) * 0.6 * nasce
    sub = np.random.default_rng(31)
    riscos = T.zero()
    for j in range(16):
        a0 = sub.uniform(0, TAU)
        f = (sub.uniform() + t * 1.6) % 1
        r1, r2 = 0.85 * (1 - f) + 0.08, 0.85 * (1 - f) * 0.7 + 0.06
        a1, a2 = a0 + 2.0 * f, a0 + 2.0 * f + 0.5
        riscos += T.tapered([(r1 * math.cos(a1), r1 * math.sin(a1), r2 * math.cos(a2) + 1e-3, r2 * math.sin(a2), 1.0)], 0.02) * (1 - f) * nasce
    aneis = T.zero()
    for j in range(3):
        f = (j / 3 + t * 1.2) % 1
        aneis += T.ring(0.75 * (1 - f) + 0.05, 0.015) * f * (1 - f) * 3
    lente = T.blur(T.ring(0.3, 0.06), 0.04) * 0.4 * nasce
    G += (ponto + riscos * 1.1 + aneis * 0.7 + lente) * env
    H += (ponto * 1.4 + riscos * 0.3) * env
    return G, H


def vermelho_bola(T, t, rng):
    """O Vermelho voando: uma bola vermelha pequena e densa, a borda pulsando para fora (ela empurra) e
    o brilho em volta."""
    G, H = vazio(T)
    cx = 0.25
    pul = 0.85 + 0.15 * math.sin(TAU * t * 8)
    bola = T.gauss(cx, 0, 0.09 * pul)
    for j in range(2):
        f = (j / 2 + t * 2) % 1
        G += T.ring(0.1 + 0.2 * f, 0.015, cx, 0) * (1 - f) * 0.8
    rastro = T.tapered([(cx - 0.8, 0, cx - 0.05, 0, 1.0)], 0.12)
    G += bola * 1.8 + T.gauss(cx, 0, 0.25) * 0.4 + T.blur(rastro, 0.02) * 0.5
    H += bola * 1.6
    return G, H


def vermelho_gojo(T, t, rng):
    """O Vermelho estourando no rival: tudo é empurrado para fora — o clarão, três anéis abrindo muito
    rápido, os riscos saindo do centro e as lascas voando para longe."""
    G, H = vazio(T)
    env = apaga(t, 0.82, 1)
    k = pulso(t, 0.0, 0.35)
    clarao = T.gauss(0, 0, 0.2) * k * 2.0
    aneis = T.zero()
    for j in range(3):
        t0 = 0.05 * j
        aneis += T.ring(0.08 + 0.9 * ease_out(rel(t, t0, t0 + 0.35), 3), 0.03 - 0.006 * j) * pulso(t, t0, t0 + 0.45)
    sai = ease_out(rel(t, 0.0, 0.3), 3)
    riscos = T.tapered([((0.15 + 0.6 * sai) * math.cos(a) + 1e-3, (0.15 + 0.6 * sai) * math.sin(a), (0.05 + 0.3 * sai) * math.cos(a), (0.05 + 0.3 * sai) * math.sin(a), 1.0) for a in np.linspace(0, TAU, 15)[:-1]], 0.035) * pulso(t, 0.0, 0.45)
    G += (clarao + aneis * 1.2 + riscos + _faiscas(T, t, 37, 18, 0.0, 0.9, 0.014) * 0.9) * env
    H += (clarao * 1.2 + aneis * 0.4) * env
    return G, H


def seis_olhos(T, t, rng):
    """Os Seis Olhos acendendo no Gojo: os dois olhos azuis brilhando forte e o brilho em volta."""
    G, H = vazio(T)
    env = apaga(t, 0.8, 1)
    k = pulso(t, 0.0, 0.6)
    olhos = (T.gauss(-0.12, -0.08, 0.035, 0.022) + T.gauss(0.12, -0.08, 0.035, 0.022)) * (0.4 + 1.6 * k)
    brilho = (T.gauss(-0.12, -0.08, 0.12, 0.06) + T.gauss(0.12, -0.08, 0.12, 0.06)) * k * 0.6
    risco = T.lines([(-0.35, -0.08, -0.18, -0.08, 1.0), (0.18, -0.08, 0.35, -0.08, 1.0)], 0.008) * k * 0.6
    G += (olhos + brilho + risco) * env
    H += olhos * 1.2 * env
    return G, H


def vazio_infinito(T, t, rng):
    """O Vazio Infinito no meio dos rivais: a esfera escura abre (só a borda acesa, o miolo escuro), as
    estrelas aparecem, os braços de galáxia giram devagar e a informação (riscos finos) corre de
    fora para dentro — ninguém consegue se mexer."""
    G, H = vazio(T)
    env = apaga(t, 0.9, 1)
    abre = ease_out(rel(t, 0.0, 0.3), 2)
    R = 0.85 * abre + 1e-3
    borda = np.exp(-((T.RAD - R) / 0.03) ** 2) * 1.3 + np.exp(-((T.RAD - R) / 0.1) ** 2) * 0.3
    dentro = np.clip(1 - T.RAD / R, 0, 1)
    ang = np.arctan2(T.V, T.U)
    giro = TAU * t * 0.25
    galaxia = (0.5 + 0.5 * np.cos(2 * ang - 6 * T.RAD + giro * 4)) ** 4 * dentro * np.exp(-(T.RAD / 0.5) ** 2) * 0.6
    sub = np.random.default_rng(41)
    estrelas = T.splats([(r * math.cos(a), r * math.sin(a), sub.uniform(0.3, 1) * (0.6 + 0.4 * math.sin(TAU * (t * 2 + sub.uniform())))) for a, r in ((sub.uniform(0, TAU), 0.8 * math.sqrt(sub.uniform())) for _ in range(40))], 0.008) * abre
    info = T.zero()
    for j in range(12):
        a = sub.uniform(0, TAU)
        f = (sub.uniform() + t * 1.3) % 1
        r1, r2 = 0.8 * (1 - f) + 0.1, 0.8 * (1 - f) - 0.08
        info += T.lines([(r1 * math.cos(a), r1 * math.sin(a), max(0.02, r2) * math.cos(a), max(0.02, r2) * math.sin(a), 1.0)], 0.006) * (1 - f) * rel(t, 0.25, 0.4)
    G += (borda + galaxia + estrelas * 1.2 + info * 0.9) * env
    H += (borda * 0.4 + estrelas * 0.6) * env
    return G, H


# =================================================================== Light
def investigacao_light(T, t, rng):
    """A Investigação: a mira fecha no rival (os quatro cantos vindo de fora), a linha de leitura varre
    de cima a baixo, as colunas de dados correm dos lados e no fim um círculo fecha: achou."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    fecha = ease_out(rel(t, 0.0, 0.3), 2)
    r = 0.75 - 0.3 * fecha
    cantos = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            cantos += [(sx * r, sy * r, sx * (r - 0.15), sy * r, 1.0), (sx * r, sy * r, sx * r, sy * (r - 0.15), 1.0)]
    mira = T.lines(cantos, 0.014)
    y = -0.45 + 0.9 * rel(t, 0.25, 0.65)
    leitura = T.lines([(-0.45, y, 0.45, y, 1.0)], 0.01) * (rel(t, 0.25, 0.3) * (1 - rel(t, 0.65, 0.7))) + T.gauss(0, y, 0.45, 0.03) * 0.3 * pulso(t, 0.25, 0.7)
    sub = np.random.default_rng(43)
    dados = []
    for x in (-0.68, -0.6, 0.6, 0.68):
        for j in range(9):
            yy = -0.5 + ((j / 9 + t * 0.8 * (1 if x < 0 else -1)) % 1)
            w = sub.uniform(0.02, 0.05)
            dados.append((x - w, yy, x + w, yy, sub.uniform(0.4, 1)))
    colunas = T.lines(dados, 0.008) * rel(t, 0.15, 0.3)
    achou = T.ring(0.18, 0.015) * pulso(t, 0.65, 1.0)
    G += (mira * 1.1 + leitura + colunas * 0.6 + achou * 1.2) * env
    H += (mira * 0.4 + leitura * 0.5 + achou * 0.6) * env
    return G, H


def _rei_xadrez(cx, cy, s):
    """O contorno da peça do rei do xadrez (a base larga, o corpo, a coroa e a cruz em cima)."""
    pts = [(-0.32, 0.5), (0.32, 0.5), (0.32, 0.42), (0.2, 0.36), (0.13, -0.05), (0.22, -0.12), (0.2, -0.2),
           (0.08, -0.22), (0.05, -0.3), (0.12, -0.3), (0.12, -0.36), (0.04, -0.36), (0.04, -0.45), (-0.04, -0.45),
           (-0.04, -0.36), (-0.12, -0.36), (-0.12, -0.3), (-0.05, -0.3), (-0.08, -0.22), (-0.2, -0.2), (-0.22, -0.12),
           (-0.13, -0.05), (-0.2, 0.36), (-0.32, 0.42)]
    return [(cx + x * s, cy + y * s) for x, y in pts]


def xeque_light(T, t, rng):
    """"Tudo conforme o plano": a peça do rei do xadrez desce de cima sobre o rival, bate (o anel no
    chão), fica um instante, e no lugar dela fica a marca vermelha (a mira) — o trio sabe em quem
    bater."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    cai = ease_in(rel(t, 0.0, 0.25), 2)
    cy = -1.2 + 1.2 * cai
    peca = _rei_xadrez(0, cy, 1.0)
    vivo = 1 - rel(t, 0.55, 0.7)
    cheio = T.polys([(peca, 1.0)], 0.004) * 0.35 * vivo
    contorno = T.polyline(peca + [peca[0]], 0.014) * vivo
    k = pulso(t, 0.24, 0.5)
    batida = T.ring(0.1 + 0.6 * ease_out(rel(t, 0.25, 0.6), 2), 0.03, 0, 0.5, 4.0) * k
    marca = (T.ring(0.3, 0.02) + T.lines([(-0.45, 0, -0.15, 0, 1.0), (0.15, 0, 0.45, 0, 1.0), (0, -0.45, 0, -0.15, 1.0), (0, 0.15, 0, 0.45, 1.0)], 0.014) + T.gauss(0, 0, 0.04)) * rel(t, 0.5, 0.65)
    G += (cheio + contorno * 1.2 + batida + marca * 1.2) * env
    H += (contorno * 0.4 + marca * 0.6) * env
    return G, H


# =================================================================== Pikachu
def bochechas_pikachu(T, t, rng):
    """As bochechas do Pikachu faiscando antes do Choque do Trovão: os dois círculos acendendo e os
    estalos pequenos saindo deles, cada vez mais fortes."""
    G, H = vazio(T)
    forca = ease_in(rel(t, 0.0, 0.9), 1.3)
    q = _quadro(t, 47)
    boch = (T.gauss(-0.2, 0.08, 0.06) + T.gauss(0.2, 0.08, 0.06)) * (0.6 + 0.8 * forca)
    R = T.zero()
    for cx in (-0.2, 0.2):
        for _ in range(2 + int(3 * forca)):
            a = q.uniform(0, TAU)
            comp = 0.12 + 0.25 * forca * q.uniform(0.5, 1)
            R += _raio(T, q, cx, 0.08, cx + comp * math.cos(a), 0.08 + comp * math.sin(a), 0.008, 3, 0.45)
    G += boch * 1.3 + R * 1.2 + T.gauss(0, 0.05, 0.4) * 0.2 * forca
    H += boch * 1.2 + R * 0.7
    return G, H


def _zigue(q, x0, x1, amp, n=14):
    """Um caminho em zigue-zague de x0 a x1, preso no meio (y=0) nas pontas."""
    xs = np.linspace(x0, x1, n)
    ys = [0.0] + [q.uniform(-amp, amp) for _ in range(n - 2)] + [0.0]
    return list(zip(xs, ys))


def trovao_faixa(T, t, rng):
    """O Choque do Trovão: um raio grosso em zigue-zague de ponta a ponta (sempre dentro da faixa), com
    galhos finos saindo, que muda de forma a cada quadro e pisca — e o brilho em volta."""
    G, H = vazio(T)
    alto = T.H / T.W
    q = _quadro(t, 53)
    principal = T.polyline(_zigue(q, -1.0, 1.0, alto * 0.28, 16), 0.022)
    galhos = T.zero()
    for _ in range(5):
        x = q.uniform(-0.8, 0.7)
        pts = [(x + px * q.uniform(0.15, 0.3), py) for px, py in _zigue(q, 0.0, 1.0, alto * 0.12, 5)]
        s_ = q.choice([-1, 1])
        galhos += T.polyline([(px, s_ * alto * 0.4 * (px - x) / 0.3 + py) for px, py in pts], 0.008)
    pisca = 0.75 + 0.25 * q.uniform()
    brilho = np.exp(-(T.V / (alto * 0.35)) ** 2) * 0.3
    G += (principal * 1.5 + T.blur(principal, 0.02) * 0.8 + galhos * 0.8 + brilho) * pisca
    H += (principal * 1.2 + galhos * 0.4) * pisca
    return G, H


def trovao_pikachu(T, t, rng):
    """O Choque do Trovão no rival: o estouro de luz, os arcos elétricos dançando em volta do corpo
    (novos a cada quadro), as faíscas e o anel."""
    G, H = vazio(T)
    env = apaga(t, 0.84, 1)
    k = pulso(t, 0.0, 0.4)
    clarao = T.gauss(0, 0, 0.22) * k * 2.0 + T.flare(0, 0, 1.2 * k + 1e-3, 0.0, 0.01) * k
    q = _quadro(t, 59)
    arcos = T.zero()
    vivo = 1 - rel(t, 0.55, 0.85)
    for _ in range(5):
        a = q.uniform(0, TAU)
        b = a + q.uniform(0.8, 2.0)
        r = q.uniform(0.25, 0.45)
        arcos += _raio(T, q, r * math.cos(a), r * math.sin(a), r * math.cos(b), r * math.sin(b), 0.012, 3, 0.4)
    anel = T.ring(0.12 + 0.6 * ease_out(rel(t, 0.0, 0.45), 2), 0.03) * pulso(t, 0.0, 0.5)
    G += (clarao + arcos * 1.2 * vivo + anel + _faiscas(T, t, 61, 16, 0.0) * 0.9) * env
    H += (clarao * 1.1 + arcos * 0.7 * vivo) * env
    return G, H


def onda_choque_voo(T, t, rng):
    """A Onda de Choque voando para +x: anéis elétricos finos (com estalos pequenos) saindo um atrás do
    outro, como uma onda."""
    G, H = vazio(T)
    q = _quadro(t, 67)
    W = T.zero()
    for j in range(3):
        f = (j / 3 + t * 1.5) % 1
        x = -0.4 + 0.75 * f
        W += T.arc_band(0.22, 0.02, -1.0, 1.0, 1.0, 0.0, x - 0.22, 0, 0.0) * (1 - f) * 1.2
        W += _raio(T, q, x, -0.18, x + 0.03, 0.18, 0.006, 3, 0.4) * (1 - f) * 0.6
    G += W + T.gauss(0.3, 0, 0.12) * 0.5
    H += W * 0.4
    return G, H


def onda_paralisa(T, t, rng):
    """A Onda de Choque prende o rival: os anéis elétricos fecham em volta dele e ficam apertando, os
    estalos entre eles, e as faíscas que pulam."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    q = _quadro(t, 71)
    A = T.zero()
    for j in range(3):
        r = 0.7 - 0.38 * ease_out(rel(t, 0.05 * j, 0.3 + 0.05 * j), 2) - 0.08 * j
        A += T.ring(max(0.12, r), 0.018, 0, 0, 1.3) * (0.7 + 0.3 * math.sin(TAU * (t * 6 + j)))
    R = T.zero()
    for _ in range(3):
        a = q.uniform(0, TAU)
        R += _raio(T, q, 0.18 * math.cos(a), 0.14 * math.sin(a), 0.38 * math.cos(a), 0.3 * math.sin(a), 0.008, 3, 0.4)
    G += (A * 1.1 + R * rel(t, 0.25, 0.35) + _faiscas(T, t, 73, 10, 0.25, 0.5, 0.01) * 0.8) * env
    H += (A * 0.4 + R * 0.5) * env
    return G, H


def agilidade_pikachu(T, t, rng):
    """A Agilidade no aliado: dois rastros amarelos correndo em volta dele (elipses que giram, com a
    cabeça clara e a cauda sumindo), os vultos que ficam para trás e as faíscas."""
    G, H = vazio(T)
    env = apaga(t, 0.86, 1)
    entra = rel(t, 0.0, 0.15)
    R = T.zero()
    for j in range(2):
        a = TAU * (t * 1.8) + math.pi * j
        R += T.arc_band(0.55, 0.035, a - 2.2, a, 0.5, 0.0, 0, 0, 1.0) * 1.0
        R += T.gauss(0.55 * math.cos(a), 0.55 * math.sin(a) * 0.5, 0.05) * 1.5
    R *= entra
    vultos = T.zero()
    for j in range(3):
        vultos += T.ring(0.3 + 0.05 * j, 0.012, 0, 0, 1.2) * pulso(t, 0.1 * j, 0.4 + 0.1 * j) * 0.5
    G += (R + vultos + _faiscas(T, t, 79, 12, 0.1, 0.6, 0.01) * 0.8) * env
    H += R * 0.5 * env
    return G, H


# =================================================================== Saitama
def passo_lateral(T, t, rng):
    """O Passo lateral: o Saitama aparece na frente do aliado sem esforço — a capa vermelha entra de lado
    varrendo (um pano largo, a barra de baixo ondulando e as dobras), para na frente dele balançando,
    e a capa vira o escudo: o meio círculo firme que fica. A poeirinha do passo no chão."""
    G, H = vazio(T)
    env = apaga(t, 0.88, 1)
    entra = ease_out(rel(t, 0.0, 0.3), 2.5)
    dx = -1.1 * (1 - entra)
    some = 1 - rel(t, 0.5, 0.65)
    topo, base = -0.5, 0.45
    pts_topo = [(dx + x, topo + 0.04 * x * x) for x in np.linspace(-0.4, 0.4, 9)]
    pts_base = []
    for x in np.linspace(0.45, -0.45, 19):
        onda = 0.06 * math.sin(10 * x + TAU * t * 3) * (0.3 + entra)
        pts_base.append((dx + x - 0.15 * (1 - entra), base + onda))
    capa = pts_topo + pts_base
    pano = T.polys([(capa, 1.0)], 0.006) * some
    borda = T.polyline(capa + [capa[0]], 0.012) * some
    dobras = T.lines([(dx + x, topo + 0.05, dx + x * 1.15 - 0.1 * (1 - entra), base - 0.05, 1.0) for x in (-0.25, -0.08, 0.1, 0.27)], 0.008) * some
    sub = np.random.default_rng(83)
    poeira = T.splats([(sub.uniform(-0.5, 0.5), 0.6 - 0.15 * ease_out(rel(t, 0.0, 0.6), 2) * sub.uniform(0.3, 1), pulso(t, 0.0, 0.8) * sub.uniform(0.3, 0.7)) for _ in range(12)], 0.04)
    escudo = T.arc_band(0.6, 0.05, -2.5, -0.64, 1.0, 0.0, 0.0, 0.1, 0.2) * rel(t, 0.5, 0.62)
    brilho = T.gauss(0, 0, 0.35) * pulso(t, 0.45, 0.7) * 0.5
    G += (pano * 0.55 + borda * 1.1 + dobras * 0.5 + poeira * 0.4 + escudo * 1.2 + brilho) * env
    H += (borda * 0.3 + escudo * 0.4) * env
    return G, H


REGISTRO = [
    ("galick_carga", galick_carga, MEDIA, "Vegeta · a Galick Gun juntando nas mãos (ergue)", False),
    ("galick_faixa", galick_faixa, FAIXA, "Vegeta · o feixe roxo da Galick Gun (faixa)", True),
    ("galick_impacto", galick_impacto, GRANDE, "Vegeta · a explosão roxa da Galick Gun", False),
    ("orgulho_saiyajin", orgulho_saiyajin, GRANDE, "Vegeta · a aura dourada de Não vou cair", False),
    ("final_flash_carga", final_flash_carga, MEDIA, "Vegeta · os braços abertos juntando o Final Flash (ergue)", False),
    ("final_flash_faixa", final_flash_faixa, FAIXA, "Vegeta · o feixe gigante do Final Flash (faixa)", True),
    ("final_flash_impacto", final_flash_impacto, GRANDE, "Vegeta · a explosão do Final Flash", False),
    ("azul_gojo", azul_gojo, GRANDE, "Gojo · o Azul puxando tudo", False),
    ("vermelho_bola", vermelho_bola, MEDIA, "Gojo · a bola do Vermelho voando (laço)", True),
    ("vermelho_gojo", vermelho_gojo, GRANDE, "Gojo · o Vermelho empurrando tudo", False),
    ("seis_olhos", seis_olhos, MEDIA, "Gojo · os Seis Olhos acendendo (nele)", False),
    ("vazio_infinito", vazio_infinito, GRANDE, "Gojo · o Vazio Infinito", False),
    ("investigacao_light", investigacao_light, GRANDE, "Light · a mira e a leitura do rival", False),
    ("xeque_light", xeque_light, GRANDE, "Light · o rei do xadrez e a marca", False),
    ("bochechas_pikachu", bochechas_pikachu, MEDIA, "Pikachu · as bochechas faiscando (ergue)", False),
    ("trovao_faixa", trovao_faixa, FAIXA, "Pikachu · o raio do Choque do Trovão (faixa)", True),
    ("trovao_pikachu", trovao_pikachu, GRANDE, "Pikachu · o Choque do Trovão no rival", False),
    ("onda_choque_voo", onda_choque_voo, MEDIA, "Pikachu · a Onda de Choque voando (laço)", True),
    ("onda_paralisa", onda_paralisa, GRANDE, "Pikachu · os anéis prendendo o rival", False),
    ("agilidade_pikachu", agilidade_pikachu, GRANDE, "Pikachu · os rastros de Agilidade no aliado", False),
    ("passo_lateral", passo_lateral, GRANDE, "Saitama · a capa varrendo e virando escudo", False),
]
