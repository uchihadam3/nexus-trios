"""Os sons da rodada 5: Tanjiro, Nezuko, Zenitsu, Inosuke e Muzan (veja tools/vfx/familias_v2/rodada05.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z
from som import METAL, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _corte_de_espada(rng, g=0.6, f0=2600):
    """O "shhing" da lâmina: o ar cortado agudo e o tinido do aço."""
    n = n_de(0.35)
    x = passa(rosa(rng, n), 2000, 10000, 2) * sobe_e_some(n, 0.25, 1.6) * 0.6
    x += modal(n, f0, rng=rng, **METAL) * env(n, 0.001, 0.25) * 0.15
    return x * g


def _trovao_curto(rng, g=0.6):
    """O estalo de raio: o "crack" seco e o chiado elétrico."""
    n = n_de(0.4)
    x = estalo(rng, n_de(0.03), 2000, 9000) * 1.2
    y = np.zeros(n)
    y[: len(x)] += x
    y += passa(rosa(rng, n), 1500, 8000, 2) * env(n, 0.002, 0.3) * 0.4
    y += satura(seno(60 * (1 + 0.5 * np.sign(np.sin(2 * math.pi * 90 * _t(n)))), n), 3) * env(n, 0.002, 0.12) * 0.15
    return y * g


def _gosma(rng, g=0.3):
    n = n_de(0.16)
    return (passa(rosa(rng, n), 100, 900, 2) * 0.7 + seno(varre(300, 90, n, 1.0), n) * 0.5) * env(n, 0.004, 0.12) * g


# =================================================================== Tanjiro
def olfato_tanjiro(rng, v):
    """O cheiro: a fungada curta (o ar puxado pelo nariz), o fio esticando (um tom fino que sobe) e o
    "plim" do ponto fraco achado."""
    x = _z(1.3)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.6, 1.4) * 0.3, 0.0)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.6, 1.4) * 0.25, 0.22)
    m = n_de(0.45)
    poe(x, seno(varre(600, 1400, m, 0.8), m) * sobe_e_some(m, 0.8, 1.3) * 0.06, 0.4)
    poe(x, _brilho(rng, 0.5, 2100, 0.2), 0.8)
    return reverb(x, 0.4, 0.2)


def respiracao_da_agua(rng, v):
    """A Roda d'Água: a respiração funda (o "fuuu"), a água girando (o redemoinho que sobe de tom) e o
    corte molhado com o espirro da onda."""
    x = _z(1.6)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 300, 1800, 2) * sobe_e_some(n, 0.5, 1.5) * 0.3, 0.0)
    m = n_de(0.6)
    t = _t(m)
    agua = passa(rosa(rng, m), 400, 3000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * (8 + 10 * t) * t)) * sobe_e_some(m, 0.7, 1.3)
    poe(x, agua * 0.45, 0.25)
    poe(x, _corte_de_espada(rng, 0.7, 2400), 0.65)
    k = n_de(0.5)
    poe(x, passa(rosa(rng, k), 600, 6000, 2) * env(k, 0.003, 0.4) * 0.4, 0.7)
    return reverb(x, 0.5, 0.25)


def hinokami_preparo(rng, v):
    """O Preparo do Hinokami: o fogo acendendo na lâmina (o "vuuf" grave que cresce) e a respiração."""
    x = _z(1.2)
    poe(x, B.fogo(rng, v)[: n_de(1.0)] * 0.5, 0.0)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 300, 1500, 2) * sobe_e_some(n, 0.6, 1.5) * 0.25, 0.1)
    return reverb(x, 0.4, 0.2)


def hinokami_kagura(rng, v):
    """A Dança do Deus do Fogo: o arco de fogo girando (o rugido que dá a volta), o corte e a explosão
    de chamas com o estalar das brasas."""
    x = _z(2.0)
    n = n_de(0.7)
    t = _t(n)
    giro = passa(rosa(rng, n), 150, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.6, 1.3)
    poe(x, satura(giro, 2) * 0.45, 0.0)
    poe(x, _corte_de_espada(rng, 0.8, 2000), 0.6)
    poe(x, B.fogo(rng, v)[: n_de(1.0)] * 0.75, 0.65)
    poe(x, baque(n_de(0.5), 75, 40, 0.25, 0.3) * 0.6, 0.65)
    poe(x, graos(rng, n_de(0.9), 18, 0.0, 0.85, 1800, 6000, 0.004, 0.7) * 0.4, 0.8)
    return reverb(x, 0.55, 0.3)


# =================================================================== Nezuko
def sangue_nezuko(rng, v):
    """O chute da Nezuko: o assobio do pé descendo, a pancada pesada e o respingo."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.3, 400, 1600, 0.8, 1.4, 0.4), 0.0)
    poe(x, baque(n_de(0.45), 85, 45, 0.18, 0.5) * 0.9, 0.3)
    poe(x, B.corte(rng, v)[: n_de(0.2)] * 0.2, 0.3)
    for k in range(3):
        poe(x, _gosma(rng, 0.15), 0.38 + 0.08 * k)
    return reverb(x, 0.35, 0.2)


def explosao_de_sangue(rng, v):
    """O Sangue Explosivo: as gotas grudando (pling pling) e as explosões de fogo rosa em sequência,
    cada uma um "vuum" curto, e o fogo crepitando depois."""
    x = _z(2.0)
    for k in range(7):
        n = n_de(0.08)
        poe(x, seno(varre(900, 500, n, 1.0), n) * env(n, 0.002, 0.06) * 0.08, 0.02 + 0.05 * k)
    for k in range(7):
        n = n_de(0.35)
        poe(x, satura(passa(rosa(rng, n), 120, 2500, 2), 2) * env(n, 0.004, 0.28) * 0.35, 0.16 + 0.06 * k)
        poe(x, baque(n_de(0.25), 90, 50, 0.1, 0.2) * 0.3, 0.16 + 0.06 * k)
    poe(x, B.fogo(rng, v)[: n_de(1.0)] * 0.35, 0.6)
    return reverb(x, 0.45, 0.25)


def despertar_nezuko(rng, v):
    """A forma desperta: o rangido de galhos crescendo (as vinhas), o rosnado e o chute que estoura."""
    x = _z(2.0)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 600, 3500, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 14 * t))) * sobe_e_some(n, 0.8, 1.2) * 0.3, 0.0)
    m = n_de(0.5)
    poe(x, satura(passa(rosa(rng, m), 80, 900, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 30 * _t(m))), 2.5) * sobe_e_some(m, 0.5, 1.3) * 0.3, 0.45)
    poe(x, _whoosh(rng, 0.2, 500, 2000, 0.8, 1.4, 0.4), 0.85)
    poe(x, baque(n_de(0.6), 70, 35, 0.3, 0.55) * 1.0, 1.0)
    return reverb(x, 0.5, 0.25)


# =================================================================== Zenitsu
def audicao_zenitsu(rng, v):
    """A audição do Zenitsu: o zumbido agudo do ouvido atento (os arcos de som), o silêncio de um
    instante e o estalo do raio cortando num risco."""
    x = _z(1.5)
    n = n_de(0.6)
    t = _t(n)
    for k in range(4):
        poe(x, seno(3200 - 300 * k, n_de(0.12)) * env(n_de(0.12), 0.01, 0.1) * 0.04, 0.05 + 0.1 * k)
    poe(x, _trovao_curto(rng, 0.8), 0.62)
    poe(x, _corte_de_espada(rng, 0.5, 3000), 0.62)
    return reverb(x, 0.45, 0.25)


def primeira_postura(rng, v):
    """A Primeira Postura no aliado: o raio chegando (o estalo), a cúpula elétrica fechando (o zumbido
    que sobe e fica) e as faíscas estalando."""
    x = _z(1.6)
    poe(x, _trovao_curto(rng, 0.6), 0.0)
    n = n_de(1.0)
    t = _t(n)
    zum = seno(varre(120, 240, n, 0.6) * (1 + 0.02 * np.sin(2 * math.pi * 50 * t)), n) * sobe_e_some(n, 0.3, 1.3) * 0.12
    poe(x, zum + passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.3, 1.3) * 0.08, 0.25)
    poe(x, graos(rng, n_de(0.9), 14, 0.0, 0.85, 3000, 9000, 0.003, 0.7) * 0.4, 0.4)
    return reverb(x, 0.45, 0.25)


def seis_dobras(rng, v):
    """As Seis Dobras: seis estalos de raio, um depois do outro, cada vez mais rápido (crack-crack-
    crack…), e o trovão grosso no fim."""
    x = _z(1.8)
    for k in range(6):
        poe(x, _trovao_curto(rng, 0.6), 0.08 * k)
    poe(x, baque(n_de(0.8), 60, 30, 0.45, 0.4) * 0.7, 0.55)
    m = n_de(0.9)
    poe(x, passa(rosa(rng, m), 60, 1500, 2) * env(m, 0.005, 0.75) * 0.4, 0.55)
    return reverb(x, 0.6, 0.3)


# =================================================================== Inosuke
def percepcao_espacial(rng, v):
    """A pele que sente: o tremor grave do chão (as vibrações), o grunhido do javali e os dois cortes
    rápidos em X."""
    x = _z(1.5)
    n = n_de(0.5)
    t = _t(n)
    poe(x, seno(45, n) * (0.5 + 0.5 * np.sin(2 * math.pi * 18 * t)) * sobe_e_some(n, 0.6, 1.3) * 0.25, 0.0)
    m = n_de(0.25)
    poe(x, satura(passa(rosa(rng, m), 100, 900, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 40 * _t(m))), 3) * sobe_e_some(m, 0.4, 1.3) * 0.3, 0.35)
    poe(x, _corte_de_espada(rng, 0.55, 2200), 0.65)
    poe(x, _corte_de_espada(rng, 0.55, 2500), 0.72)
    return reverb(x, 0.4, 0.2)


def presas_rasgantes(rng, v):
    """As Presas: as duas lâminas lascadas raspando juntas (o "crrrrsh" serrilhado) e o rasgo."""
    x = _z(1.3)
    for k in range(2):
        n = n_de(0.3)
        t = _t(n)
        serra = passa(rosa(rng, n), 1500, 7000, 2) * (0.5 + 0.5 * np.sign(np.sin(2 * math.pi * 60 * t))) * sobe_e_some(n, 0.3, 1.5)
        poe(x, serra * 0.45, 0.1 + 0.03 * k)
    poe(x, B.corte_pesado(rng, v) * 0.6, 0.18)
    return reverb(x, 0.4, 0.2)


def investida_inosuke(rng, v):
    """A investida do javali: os passos galopando, o ronco do javali ("ARRGH"), a trombada e os
    cortes loucos em sequência."""
    x = _z(2.0)
    for k in range(5):
        poe(x, baque(n_de(0.12), 90, 60, 0.05, 0.3) * 0.35, 0.05 * k)
    m = n_de(0.45)
    poe(x, satura(passa(rosa(rng, m), 90, 1100, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 35 * _t(m))), 3) * sobe_e_some(m, 0.4, 1.3) * 0.4, 0.05)
    poe(x, baque(n_de(0.5), 70, 35, 0.25, 0.55) * 0.9, 0.3)
    for k in range(6):
        poe(x, _corte_de_espada(rng, 0.4, 2000 + 200 * k), 0.38 + 0.05 * k)
    return reverb(x, 0.45, 0.25)


# =================================================================== Muzan
def chicotes_de_carne(rng, v):
    """Os chicotes de carne: o rasgo úmido saindo do chão, o "vuuush" dos chicotes e o estalo."""
    x = _z(1.5)
    poe(x, _gosma(rng, 0.35), 0.0)
    for k in range(2):
        poe(x, _whoosh(rng, 0.3, 300, 1800, 0.7, 1.4, 0.35), 0.08 + 0.05 * k)
    poe(x, estalo(rng, n_de(0.04), 1500, 7000) * 0.8, 0.32)
    poe(x, baque(n_de(0.3), 80, 45, 0.12, 0.3) * 0.5, 0.32)
    return reverb(x, 0.4, 0.2)


def sangue_corruptor(rng, v):
    """O sangue de Muzan: a picada, o líquido grosso entrando (o "glub" grave) e o pulsar das veias."""
    x = _z(1.8)
    poe(x, estalo(rng, n_de(0.03), 2000, 7000) * 0.4, 0.0)
    n = n_de(0.5)
    poe(x, seno(varre(220, 70, n, 1.0), n) * env(n, 0.01, 0.4) * 0.25 + passa(rosa(rng, n), 80, 600, 2) * env(n, 0.01, 0.4) * 0.3, 0.05)
    for k in range(3):
        poe(x, baque(n_de(0.2), 62, 36, 0.08, 0.1) * 0.4, 0.55 + 0.35 * k)
    return reverb(x, 0.5, 0.3)


def adaptacao_demoniaca(rng, v):
    """A carne se adapta: o borbulhar da carne fechando, as bocas rosnando ao mesmo tempo (o rosnado
    grave e o sussurro) e o pulso vermelho."""
    x = _z(2.0)
    for k in range(6):
        poe(x, _gosma(rng, 0.2), 0.05 + 0.08 * k)
    m = n_de(0.8)
    t = _t(m)
    poe(x, satura(passa(rosa(rng, m), 60, 700, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 24 * t)), 3) * sobe_e_some(m, 0.4, 1.3) * 0.3, 0.5)
    poe(x, passa(rosa(rng, m), 1500, 4500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(m, 0.4, 1.3) * 0.08, 0.5)
    poe(x, baque(n_de(0.5), 55, 30, 0.3, 0.3) * 0.6, 1.1)
    return reverb(x, 0.55, 0.3)


SONS: dict = {
    "olfato-tanjiro": (olfato_tanjiro, "Tanjiro: a fungada e o fio do cheiro"),
    "respiracao-da-agua": (respiracao_da_agua, "Tanjiro: a Roda d'Água"),
    "hinokami-preparo": (hinokami_preparo, "Tanjiro: o fogo acendendo na lâmina (antes do golpe)"),
    "hinokami-kagura": (hinokami_kagura, "Tanjiro: a Dança do Deus do Fogo"),
    "sangue-nezuko": (sangue_nezuko, "Nezuko: o chute demoníaco"),
    "explosao-de-sangue": (explosao_de_sangue, "Nezuko: o Sangue Explosivo"),
    "despertar-nezuko": (despertar_nezuko, "Nezuko: a forma desperta"),
    "audicao-zenitsu": (audicao_zenitsu, "Zenitsu: o ouvido e o raio"),
    "primeira-postura": (primeira_postura, "Zenitsu: a cúpula elétrica no aliado"),
    "seis-dobras": (seis_dobras, "Zenitsu: as Seis Dobras"),
    "percepcao-espacial": (percepcao_espacial, "Inosuke: o tremor e o X"),
    "presas-rasgantes": (presas_rasgantes, "Inosuke: as lâminas lascadas"),
    "investida-inosuke": (investida_inosuke, "Inosuke: a investida do javali"),
    "chicotes-de-carne": (chicotes_de_carne, "Muzan: os chicotes de carne"),
    "sangue-corruptor": (sangue_corruptor, "Muzan: o sangue corruptor"),
    "adaptacao-demoniaca": (adaptacao_demoniaca, "Muzan: a carne se adapta"),
}
