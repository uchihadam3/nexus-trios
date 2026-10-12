"""Os sons da rodada 20: Master Chief, Doom Slayer, Solid Snake, Raiden (Metal Gear) e Leon S. Kennedy (veja
tools/vfx/familias_v2/rodada20.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada14 import _trovao
from som import CRISTAL, METAL, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _tiro(rng, g=0.5, f0=200):
    """O tiro: o estampido seco com o estalo agudo."""
    n = n_de(0.18)
    return (satura(baque(n, f0, f0 * 0.4, 0.03, 1.0), 2.5) * 0.6 + estalo(rng, n, 2000, 9000, 0.008) * 0.7) * g


def _abafado(rng, g=0.4):
    """O tiro com silenciador: o "tuf" curto e o clique do ferrolho."""
    n = n_de(0.15)
    return (passa(rosa(rng, n), 300, 2500, 2) * env(n, 0.001, 0.03) * 0.8 + estalo(rng, n, 3000, 9000, 0.004) * 0.25) * g


def _lamina(rng, seg=0.2, g=0.3):
    """A lâmina cortando o ar: o assobio agudo e curto."""
    n = n_de(seg)
    return passa(rosa(rng, n), 3500, 13000, 2) * sobe_e_some(n, 0.3, 2.5) * g


def _zap(rng, seg=0.2, g=0.2):
    """O estalo elétrico."""
    n = n_de(seg)
    return graos(rng, n, 30, 0.0, seg * 0.9, 2500, 10000, 0.002) * g + satura(passa(rosa(rng, n), 1500, 6000, 2) * env(n, 0.001, seg * 0.4), 3.0) * g * 0.4


# =================================================================== Master Chief
def escudo_de_energia(rng, v):
    """O escudo de energia: o zumbido que sobe quando a bolha fecha e o "tchiu" do escudo carregado."""
    x = _z(1.4)
    n = n_de(0.5)
    poe(x, seno(varre(220, 660, n, 0.8), n) * sobe_e_some(n, 0.7, 1.4) * 0.08, 0.0)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.7, 1.4) * 0.1, 0.0)
    m = n_de(0.6)
    poe(x, (seno(880, m) + seno(1320, m) * 0.6) * env(m, 0.005, 0.3) * 0.06, 0.35)
    poe(x, _brilho(rng, 0.5, 1760, 0.05, CRISTAL), 0.38)
    return reverb(x, 0.4, 0.2)


def fogo_de_supressao(rng, v):
    """O fogo de supressão: a rajada do fuzil (catorze tiros rápidos) e os cartuchos caindo no fim."""
    x = _z(1.3)
    for k in range(14):
        poe(x, _tiro(rng, 0.34, 240 + 15 * (k % 3)), 0.02 + 0.03 * k)
    for k in range(4):
        poe(x, modal(n_de(0.15), 3200 + 300 * k, rng=rng, **METAL) * env(n_de(0.15), 0.0005, 0.05) * 0.04, 0.5 + 0.06 * k)
    return reverb(x, 0.35, 0.2)


def masterchief_preparo(rng, v):
    """O Preparo da Posição firme: o escudo carregando (o bipe que acelera e o zumbido subindo)."""
    x = _z(1.5)
    n = n_de(1.3)
    poe(x, seno(varre(300, 900, n, 1.0), n) * sobe_e_some(n, 0.9, 1.0) * 0.05, 0.0)
    t0, passo = 0.0, 0.22
    while t0 < 1.3:
        m = n_de(0.05)
        poe(x, seno(1500, m) * env(m, 0.002, 0.03) * 0.05, t0)
        t0 += passo
        passo = max(0.05, passo * 0.82)
    return reverb(x, 0.4, 0.2)


def posicao_firme(rng, v):
    """A posição firme: o pisão pesado da armadura, o tremor que corre pelo chão e o escudo zumbindo."""
    x = _z(1.8)
    poe(x, satura(baque(n_de(0.5), 70, 30, 0.2, 1.0), 2.2) * 0.75, 0.05)
    poe(x, modal(n_de(0.4), 420, rng=rng, **METAL) * env(n_de(0.4), 0.001, 0.15) * 0.15, 0.05)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 30, 250, 2) * sobe_e_some(n, 0.15, 1.5) * 0.6, 0.1)
    m = n_de(0.7)
    poe(x, seno(varre(500, 300, m, 1.0), m) * env(m, 0.05, 0.4) * 0.05, 0.45)
    return reverb(x, 0.5, 0.25)


# =================================================================== Doom Slayer
def avanco_brutal(rng, v):
    """O avanço brutal: o vento da investida, o soco que esmaga e os grilhões estalando."""
    x = _z(1.5)
    poe(x, _whoosh(rng, 0.25, 200, 1500, 0.8, 1.3, 0.5), 0.0)
    poe(x, satura(baque(n_de(0.4), 90, 35, 0.12, 1.0), 2.6) * 0.8, 0.25)
    poe(x, passa(rosa(rng, n_de(0.2)), 400, 3000, 2) * env(n_de(0.2), 0.001, 0.08) * 0.4, 0.25)
    for k in range(3):
        poe(x, modal(n_de(0.25), 900 + 200 * k, rng=rng, **METAL) * env(n_de(0.25), 0.001, 0.1) * 0.07, 0.5 + 0.06 * k)
    return reverb(x, 0.45, 0.25)


def blindagem_de_combate(rng, v):
    """A blindagem de combate: as seis placas encaixando (seis "clanc" metálicos) e o zumbido verde."""
    x = _z(1.4)
    for k in range(6):
        poe(x, modal(n_de(0.25), 300 + 40 * k, rng=rng, **METAL) * env(n_de(0.25), 0.001, 0.08) * 0.12, 0.15 + 0.04 * k)
        poe(x, satura(baque(n_de(0.12), 160, 90, 0.03, 0.6), 1.8) * 0.18, 0.15 + 0.04 * k)
    m = n_de(0.7)
    poe(x, (seno(330, m) + seno(495, m) * 0.6) * env(m, 0.02, 0.4) * 0.05, 0.45)
    return reverb(x, 0.4, 0.2)


def doomslayer_preparo(rng, v):
    """O Preparo da Onda sísmica: o fogo crepitando no punho e o ronco grave crescendo."""
    x = _z(1.5)
    n = n_de(1.3)
    poe(x, graos(rng, n, 45, 0.0, 1.25, 800, 5000, 0.006) * 0.3, 0.0)
    poe(x, passa(rosa(rng, n), 40, 220, 2) * sobe_e_some(n, 0.85, 1.2) * 0.35, 0.0)
    poe(x, satura(seno(varre(45, 70, n, 1.0), n), 2.0) * sobe_e_some(n, 0.85, 1.2) * 0.08, 0.0)
    return reverb(x, 0.5, 0.25)


def onda_sismica(rng, v):
    """A onda sísmica: o soco no chão, as rachaduras correndo, o fogo subindo e as pedras caindo."""
    x = _z(2.0)
    poe(x, satura(baque(n_de(0.6), 60, 25, 0.25, 1.0), 2.4) * 0.8, 0.0)
    poe(x, _trovao(rng, 1.0, 0.5), 0.02)
    n = n_de(0.7)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * sobe_e_some(n, 0.3, 1.5) * 0.35, 0.15)
    poe(x, graos(rng, n_de(0.8), 25, 0.2, 0.75, 300, 2500, 0.02) * 0.6, 0.3)
    return reverb(x, 0.6, 0.3)


# =================================================================== Solid Snake
def camuflagem(rng, v):
    """A camuflagem: a caixa de papelão caindo (o "pof" seco), o zumbido da camuflagem óptica e o tiro abafado."""
    x = _z(1.4)
    poe(x, passa(rosa(rng, n_de(0.15)), 200, 1500, 2) * env(n_de(0.15), 0.001, 0.06) * 0.5, 0.18)
    n = n_de(0.5)
    t = _t(n)
    poe(x, seno(varre(1200, 600, n, 1.0), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 25 * t)) * sobe_e_some(n, 0.4, 1.3) * 0.05, 0.4)
    poe(x, _abafado(rng, 0.5), 0.62)
    return reverb(x, 0.35, 0.2)


def tiro_de_flanco(rng, v):
    """O tiro de flanco: o bipe da mira laser, o tiro abafado e o impacto seco."""
    x = _z(1.3)
    m = n_de(0.08)
    poe(x, seno(2400, m) * env(m, 0.002, 0.05) * 0.05, 0.05)
    poe(x, seno(2400, m) * env(m, 0.002, 0.05) * 0.05, 0.3)
    poe(x, _abafado(rng, 0.6), 0.38)
    poe(x, satura(baque(n_de(0.25), 140, 60, 0.06, 0.9), 2.0) * 0.4, 0.47)
    return reverb(x, 0.35, 0.2)


# =================================================================== Raiden
def corte_em_sequencia(rng, v):
    """O corte em sequência: sete cortes da lâmina de alta frequência e os estalos elétricos."""
    x = _z(1.3)
    for k in range(7):
        poe(x, _lamina(rng, 0.15, 0.3), 0.03 + 0.06 * k)
        poe(x, _zap(rng, 0.12, 0.12), 0.09 + 0.06 * k)
    n = n_de(0.6)
    poe(x, seno(varre(2000, 3000, n, 1.0), n) * env(n, 0.01, 0.3) * 0.02, 0.0)
    return reverb(x, 0.35, 0.2)


def raiden_preparo(rng, v):
    """O Preparo do Zandatsu: o Modo lâmina — o tempo desacelerando (o tom que desce e abafa) e a lâmina
    vibrando."""
    x = _z(1.5)
    n = n_de(1.3)
    poe(x, passa(rosa(rng, n), 100, 800, 2) * sobe_e_some(n, 0.3, 1.2) * 0.2, 0.0)
    m = n_de(1.2)
    poe(x, seno(varre(3000, 3200, m, 1.0), m) * (0.6 + 0.4 * np.sin(2 * math.pi * 40 * _t(m))) * env(m, 0.1, 0.8) * 0.02, 0.1)
    poe(x, _zap(rng, 0.4, 0.12), 0.5)
    return reverb(x, 0.6, 0.3)


def zandatsu(rng, v):
    """O Zandatsu: o plano do corte varrendo, a chuva de cortes e a explosão elétrica."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.25, 800, 5000, 0.5, 1.2, 0.35), 0.0)
    for k in range(10):
        poe(x, _lamina(rng, 0.1, 0.18), 0.12 + 0.02 * k)
    poe(x, _zap(rng, 0.6, 0.45), 0.45)
    poe(x, satura(baque(n_de(0.5), 80, 35, 0.15, 0.8), 2.0) * 0.5, 0.45)
    return reverb(x, 0.5, 0.25)


# =================================================================== Leon
def mira_firme(rng, v):
    """A mira firme: a respiração presa e o clique da trava da mira."""
    x = _z(1.2)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 300, 1500, 2) * sobe_e_some(n, 0.5, 1.5) * 0.08, 0.0)
    poe(x, modal(n_de(0.12), 2800, rng=rng, **METAL) * env(n_de(0.12), 0.0005, 0.03) * 0.15, 0.45)
    m = n_de(0.4)
    poe(x, seno(varre(400, 250, m, 1.0), m) * env(m, 0.01, 0.3) * 0.04, 0.6)
    return reverb(x, 0.3, 0.15)


def tiro_na_cabeca(rng, v):
    """O tiro na cabeça: o disparo da pistola, o impacto seco e o zumbido do rival zonzo."""
    x = _z(1.4)
    poe(x, _tiro(rng, 0.55, 210), 0.0)
    poe(x, satura(baque(n_de(0.2), 180, 80, 0.05, 1.0), 2.2) * 0.4, 0.2)
    for k in range(3):
        poe(x, _brilho(rng, 0.3, 1568 + 200 * k, 0.03, VIDRO), 0.45 + 0.1 * k)
    return reverb(x, 0.4, 0.2)


def leon_preparo(rng, v):
    """O Preparo da Faca de combate: a faca saindo da bainha (o raspar metálico) e o brilho na lâmina."""
    x = _z(1.2)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 2500, 9000, 2) * sobe_e_some(n, 0.6, 1.5) * 0.12, 0.05)
    poe(x, _brilho(rng, 0.6, 2093, 0.04, CRISTAL), 0.45)
    return reverb(x, 0.4, 0.2)


def faca_de_combate(rng, v):
    """A faca de combate: os dois cortes rápidos, o tinido do aparo e o Preparo quebrando como vidro."""
    x = _z(1.4)
    poe(x, _lamina(rng, 0.15, 0.35), 0.0)
    poe(x, _lamina(rng, 0.15, 0.35), 0.12)
    poe(x, modal(n_de(0.4), 1900, rng=rng, **METAL) * env(n_de(0.4), 0.0005, 0.15) * 0.2, 0.24)
    poe(x, modal(n_de(0.6), 1600, rng=rng, **VIDRO) * env(n_de(0.6), 0.0005, 0.25) * 0.15, 0.36)
    poe(x, graos(rng, n_de(0.5), 30, 0.0, 0.4, 3000, 10000, 0.006) * 0.3, 0.36)
    return reverb(x, 0.4, 0.2)


SONS: dict = {
    "escudo-de-energia": (escudo_de_energia, "Master Chief: a bolha do escudo fechando"),
    "fogo-de-supressao": (fogo_de_supressao, "Master Chief: a rajada do fuzil"),
    "masterchief-preparo": (masterchief_preparo, "Master Chief: o escudo carregando (antes do golpe)"),
    "posicao-firme": (posicao_firme, "Master Chief: o pisão e o tremor"),
    "avanco-brutal": (avanco_brutal, "Doom Slayer: a investida e o soco"),
    "blindagem-de-combate": (blindagem_de_combate, "Doom Slayer: as placas encaixando"),
    "doomslayer-preparo": (doomslayer_preparo, "Doom Slayer: o punho em chamas (antes do golpe)"),
    "onda-sismica": (onda_sismica, "Doom Slayer: o soco no chão e as pedras"),
    "camuflagem": (camuflagem, "Snake: a caixa, a camuflagem e o tiro abafado"),
    "tiro-de-flanco": (tiro_de_flanco, "Snake: a mira laser e o tiro abafado"),
    "corte-em-sequencia": (corte_em_sequencia, "Raiden: os cortes elétricos"),
    "raiden-preparo": (raiden_preparo, "Raiden: o Modo lâmina (antes do golpe)"),
    "zandatsu": (zandatsu, "Raiden: os cortes e a explosão elétrica"),
    "mira-firme": (mira_firme, "Leon: a respiração e a trava da mira"),
    "tiro-na-cabeca": (tiro_na_cabeca, "Leon: o tiro e o impacto"),
    "leon-preparo": (leon_preparo, "Leon: a faca saindo da bainha (antes do golpe)"),
    "faca-de-combate": (faca_de_combate, "Leon: os cortes, o aparo e o Preparo quebrando"),
}
