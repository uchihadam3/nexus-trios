"""Os sons da rodada 8: Levi, Hisoka, Kurapika, Edward e Alphonse (veja tools/vfx/familias_v2/rodada08.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _lamina(rng, seg=0.3, f0=2600, g=0.6):
    n = n_de(seg)
    x = passa(rosa(rng, n), 2000, 11000, 2) * sobe_e_some(n, 0.2, 1.6) * 0.6
    x += modal(n, f0, rng=rng, **METAL) * env(n, 0.001, seg * 0.7) * 0.12
    return x * g


def _gas(rng, seg, g=0.3):
    n = n_de(seg)
    return passa(rosa(rng, n), 1800, 9000, 2) * sobe_e_some(n, 0.1, 1.3) * g


def _corrente(rng, seg, elos=10, g=0.4):
    """A corrente: os elos batendo uns nos outros (tilintar metálico em sequência rápida)."""
    x = np.zeros(n_de(seg))
    sub = np.random.default_rng(5)
    for k in range(elos):
        n = n_de(0.08)
        poe(x, modal(n, sub.uniform(2400, 3600), rng=rng, **METAL) * env(n, 0.001, 0.05) * g * sub.uniform(0.5, 1), k * seg / (elos + 1))
    return x


def _alquimia(rng, seg, g=0.3):
    """Os raios alquímicos: estalinhos elétricos azuis correndo, com o zumbido."""
    n = n_de(seg)
    x = graos(rng, n, 30, 0.0, seg * 0.9, 2500, 9000, 0.003, 0.7) * 0.6
    x += satura(seno(120 + 40 * np.sin(2 * math.pi * 30 * _t(n)), n), 3) * sobe_e_some(n, 0.3, 1.3) * 0.06
    return x * g


def _pedra(rng, g=0.6):
    n = n_de(0.4)
    return (baque(n, 110, 55, 0.12, 0.6) * 0.8 + passa(rosa(rng, n), 200, 3000, 2) * env(n, 0.002, 0.15) * 0.5) * g


# =================================================================== Levi
def leitura_de_abertura(rng, v):
    """A leitura: três "tic" secos e agudos (os pontos achados), um respiro curto, e o corte certeiro
    (o "shk" limpo e rápido)."""
    x = _z(1.3)
    for k in range(3):
        n = n_de(0.05)
        poe(x, seno(3400 - 200 * k, n) * env(n, 0.001, 0.03) * 0.1, 0.05 + 0.1 * k)
    poe(x, _brilho(rng, 0.3, 2800, 0.06, CRISTAL), 0.35)
    poe(x, _lamina(rng, 0.25, 3100, 1.0), 0.5)
    return reverb(x, 0.4, 0.2)


def giro_de_levi(rng, v):
    """O Giro cortante: o gás disparando, o zumbido do giro (o "fffshh" que pulsa rápido, as lâminas
    rodando) avançando, e os cortes em rajada no rival."""
    x = _z(1.5)
    poe(x, _gas(rng, 0.6, 0.4), 0.0)
    n = n_de(0.55)
    t = _t(n)
    giro = passa(rosa(rng, n), 1500, 8000, 2) * (0.4 + 0.6 * np.abs(np.sin(2 * math.pi * 16 * t))) * (np.linspace(0.3, 1, n))
    poe(x, giro * 0.5, 0.05)
    for k in range(5):
        poe(x, _lamina(rng, 0.12, 2800 + 150 * k, 0.4), 0.4 + 0.06 * k)
    return reverb(x, 0.45, 0.22)


def levi_preparo(rng, v):
    """O Preparo da Execução: as lâminas girando na mão (o tinido) e o gás chiando baixo."""
    x = _z(1.2)
    poe(x, modal(n_de(0.5), 3000, rng=rng, **METAL) * env(n_de(0.5), 0.001, 0.3) * 0.1, 0.0)
    poe(x, _gas(rng, 1.0, 0.18), 0.1)
    return reverb(x, 0.4, 0.2)


def execucao_relampago(rng, v):
    """A Execução relâmpago: o silêncio cortado por um "fwip" só (rápido demais para ver), e no
    instante seguinte dezenas de cortes ao mesmo tempo (o "shhrrak" denso), o sangue e o vapor."""
    x = _z(1.8)
    n = n_de(0.12)
    poe(x, passa(rosa(rng, n), 2000, 10000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.6, 0.0)
    sub = np.random.default_rng(12)
    for _ in range(18):
        poe(x, _lamina(rng, sub.uniform(0.06, 0.12), sub.uniform(2500, 4200), sub.uniform(0.2, 0.4)), 0.18 + sub.uniform(0, 0.12))
    poe(x, baque(n_de(0.4), 90, 45, 0.15, 0.4) * 0.6, 0.2)
    poe(x, passa(rosa(rng, n_de(0.3)), 200, 2000, 2) * env(n_de(0.3), 0.005, 0.2) * 0.3, 0.3)
    poe(x, _gas(rng, 0.9, 0.25), 0.55)
    return reverb(x, 0.5, 0.25)


# =================================================================== Hisoka
def bungee_gum(rng, v):
    """O Bungee Gum: o fio saindo (o "tchwip" elástico), o "plop" pegajoso da bolota grudando e o
    elástico vibrando (o "boing" que oscila e para)."""
    x = _z(1.6)
    n = n_de(0.25)
    poe(x, seno(varre(400, 1400, n, 0.7), n) * env(n, 0.002, 0.2) * 0.12 + passa(rosa(rng, n), 1000, 5000, 2) * sobe_e_some(n, 0.3, 1.4) * 0.15, 0.0)
    m = n_de(0.15)
    poe(x, (passa(rosa(rng, m), 150, 1200, 2) * 0.6 + seno(varre(300, 120, m, 1.0), m) * 0.5) * env(m, 0.002, 0.1) * 0.4, 0.24)
    k = n_de(0.8)
    t = _t(k)
    boing = seno(180 * (1 + 0.25 * np.sin(2 * math.pi * 6 * t) * np.exp(-3 * t)), k) * np.exp(-3.5 * t) * 0.2
    poe(x, boing, 0.28)
    return reverb(x, 0.45, 0.22)


def textura_surpresa(rng, v):
    """A Textura Surpresa: a carta girando no ar (o "frrr" do papel), cravando (o "tchak"), o descascar
    (o papel rasgando devagar) e o "plim" da marca revelada, com uma risadinha de mágico no tom."""
    x = _z(1.5)
    n = n_de(0.32)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 24 * t))) * sobe_e_some(n, 0.6, 1.2) * 0.35, 0.0)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000) * 0.7, 0.3)
    m = n_de(0.45)
    poe(x, passa(rosa(rng, m), 1200, 6000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 40 * _t(m))) * env(m, 0.02, 0.35) * 0.25, 0.4)
    poe(x, _brilho(rng, 0.6, 1568, 0.08, SINO), 0.85)
    return reverb(x, 0.45, 0.22)


# =================================================================== Kurapika
def corrente_de_captura(rng, v):
    """A Corrente de captura: a corrente se enrolando (os elos tilintando em volta, girando), apertando
    (o rangido do metal) e o "clac" do cadeado travando."""
    x = _z(1.6)
    poe(x, _corrente(rng, 0.8, 14, 0.35), 0.0)
    n = n_de(0.3)
    poe(x, satura(seno(varre(220, 180, n, 1.0) * (1 + 0.08 * np.sign(np.sin(2 * math.pi * 45 * _t(n)))), n), 2) * env(n, 0.01, 0.25) * 0.08, 0.6)
    poe(x, modal(n_de(0.4), 1700, rng=rng, **METAL) * env(n_de(0.4), 0.001, 0.15) * 0.3, 0.85)
    poe(x, estalo(rng, n_de(0.02), 1500, 6000) * 0.6, 0.85)
    return reverb(x, 0.45, 0.22)


def corrente_do_julgamento(rng, v):
    """A Corrente do julgamento: a corrente disparando reta (os elos num assobio), a ponta cravando
    (o "tchunk"), o coração batendo uma vez forte e o anel fechando (o tom grave de promessa)."""
    x = _z(1.7)
    poe(x, _corrente(rng, 0.3, 8, 0.25), 0.0)
    poe(x, _whoosh(rng, 0.25, 1800, 3600, 0.8, 1.4, 0.3), 0.0)
    poe(x, baque(n_de(0.3), 130, 70, 0.08, 0.7) * 0.6 + modal(n_de(0.3), 1400, rng=rng, **METAL) * env(n_de(0.3), 0.001, 0.12) * 0.2, 0.3)
    for k, em in enumerate((0.5, 0.68)):
        poe(x, baque(n_de(0.25), 60, 40, 0.1, 0.1) * (0.6 if k == 0 else 0.4), em)
    n = n_de(0.9)
    poe(x, (seno(110, n) + seno(165, n) * 0.5) * sobe_e_some(n, 0.3, 1.3) * 0.1, 0.62)
    return reverb(x, 0.55, 0.3)


def olhos_escarlates(rng, v):
    """Os Olhos escarlates: o "vwoom" grave dos olhos acendendo (o tom subindo), o zumbido de raiva e
    o pulso de pressão (dois baques surdos e o anel)."""
    x = _z(1.7)
    n = n_de(0.45)
    poe(x, seno(varre(80, 220, n, 1.4), n) * sobe_e_some(n, 0.7, 1.3) * 0.25, 0.0)
    m = n_de(0.9)
    t = _t(m)
    poe(x, satura(seno(220 + 3 * np.sin(2 * math.pi * 7 * t), m) + seno(331, m) * 0.5, 2) * sobe_e_some(m, 0.3, 1.3) * 0.05, 0.25)
    for k in range(2):
        poe(x, baque(n_de(0.4), 70, 35, 0.2, 0.2) * 0.6, 0.45 + 0.12 * k)
        poe(x, _whoosh(rng, 0.4, 300, 1200, 0.2, 1.4, 0.2), 0.45 + 0.12 * k)
    return reverb(x, 0.55, 0.3)


# =================================================================== Edward
def lanca_de_pedra(rng, v):
    """A Lança de pedra: o "PLÁ" das palmas batendo, os raios da alquimia correndo pelo chão, e a lança
    de pedra rompendo para cima (o ronco e o estalo da rocha) com as lascas caindo."""
    x = _z(1.7)
    n = n_de(0.08)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * env(n, 0.001, 0.05) * 0.9, 0.0)
    poe(x, _alquimia(rng, 0.6, 0.6), 0.1)
    poe(x, _pedra(rng, 0.9), 0.45)
    poe(x, B.terra(rng, v)[: n_de(0.6)] * 0.45, 0.45)
    poe(x, graos(rng, n_de(0.6), 18, 0.05, 0.5, 1200, 5000, 0.006, 0.6) * 0.3, 0.6)
    return reverb(x, 0.5, 0.25)


def muralha_alquimica(rng, v):
    """A Muralha alquímica: os raios correndo, as pedras subindo em batidas (as fileiras de tijolo, um
    "toc" grave atrás do outro) e o "shkk" dos espinhos saindo da frente."""
    x = _z(1.8)
    poe(x, _alquimia(rng, 0.7, 0.55), 0.0)
    for k in range(5):
        poe(x, _pedra(rng, 0.5), 0.2 + 0.08 * k)
    for k in range(3):
        poe(x, _lamina(rng, 0.1, 2000 + 200 * k, 0.3), 0.68 + 0.03 * k)
    return reverb(x, 0.5, 0.25)


# =================================================================== Alphonse
def armadura_de_aco(rng, v):
    """A Armadura de aço: as placas de metal se encaixando (os "clang" ocos de armadura, cada uma), os
    rebites e o eco dentro da armadura vazia."""
    x = _z(1.6)
    sub = np.random.default_rng(8)
    for k in range(7):
        n = n_de(0.5)
        poe(x, modal(n, sub.uniform(380, 620), rng=rng, **METAL) * env(n, 0.001, 0.3) * 0.18, 0.03 + 0.06 * k)
        poe(x, estalo(rng, n_de(0.01), 2000, 7000) * 0.2, 0.03 + 0.06 * k)
    poe(x, modal(n_de(1.0), 220, rng=rng, **SINO) * env(n_de(1.0), 0.01, 0.8) * 0.08, 0.5)
    return reverb(x, 0.65, 0.35)


def circulo_protetor(rng, v):
    """O Círculo protetor: o giz desenhando no chão (o arranhado), o círculo acendendo (o "vuum" azul) e
    a luz subindo (o acorde calmo)."""
    x = _z(1.8)
    n = n_de(0.5)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2500, 8000, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 11 * t))) * env(n, 0.01, 0.45) * 0.2, 0.0)
    poe(x, _alquimia(rng, 0.5, 0.3), 0.4)
    m = n_de(1.1)
    poe(x, (seno(392, m) + seno(493.9, m) * 0.6 + seno(587.3, m) * 0.4) * sobe_e_some(m, 0.3, 1.3) * 0.07, 0.5)
    poe(x, _brilho(rng, 0.8, 1175, 0.05, CRISTAL), 0.7)
    return reverb(x, 0.6, 0.35)


def barreira_transmutada(rng, v):
    """A Barreira transmutada: os raios da alquimia, e as três cúpulas de pedra subindo uma depois da
    outra (o ronco de pedra arrastando e o "toc" de fechar)."""
    x = _z(1.9)
    poe(x, _alquimia(rng, 0.6, 0.5), 0.0)
    for k in range(3):
        n = n_de(0.35)
        poe(x, passa(rosa(rng, n), 60, 700, 2) * sobe_e_some(n, 0.6, 1.3) * 0.4, 0.2 + 0.12 * k)
        poe(x, _pedra(rng, 0.55), 0.48 + 0.12 * k)
    return reverb(x, 0.55, 0.3)


SONS: dict = {
    "leitura-de-abertura": (leitura_de_abertura, "Levi: os pontos achados e o corte certeiro"),
    "giro-de-levi": (giro_de_levi, "Levi: o gás e o giro de lâminas"),
    "levi-preparo": (levi_preparo, "Levi: as lâminas e o gás (antes do golpe)"),
    "execucao-relampago": (execucao_relampago, "Levi: os cortes de uma vez e o vapor"),
    "bungee-gum": (bungee_gum, "Hisoka: o chiclete que gruda e estica"),
    "textura-surpresa": (textura_surpresa, "Hisoka: a carta, o descascar e a surpresa"),
    "corrente-de-captura": (corrente_de_captura, "Kurapika: a corrente que enrola e trava"),
    "corrente-do-julgamento": (corrente_do_julgamento, "Kurapika: a ponta no coração e a promessa"),
    "olhos-escarlates": (olhos_escarlates, "Kurapika: os olhos acendendo e a pressão"),
    "lanca-de-pedra": (lanca_de_pedra, "Edward: as palmas e a lança de pedra"),
    "muralha-alquimica": (muralha_alquimica, "Edward: o muro subindo e os espinhos"),
    "armadura-de-aco": (armadura_de_aco, "Alphonse: as placas de armadura"),
    "circulo-protetor": (circulo_protetor, "Alphonse: o círculo de transmutação"),
    "barreira-transmutada": (barreira_transmutada, "Alphonse: as cúpulas de pedra"),
}
