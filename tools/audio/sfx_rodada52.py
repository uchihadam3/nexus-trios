"""Os sons da rodada 52 das habilidades próprias (veja tools/vfx/familias_v2/rodada52.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _choque(rng, seg, g=0.3, f0=1500, f1=7000):
    n = n_de(seg)
    t = _t(n)
    corte = (np.sin(2 * math.pi * 55 * t) > 0.2).astype(float)
    return satura(passa(rosa(rng, n), f0, f1, 2) * corte, 3) * env(n, 0.005, seg * 0.5) * g


def _sabre_zumbido(rng, seg, f=95, g=0.04):
    """O zumbido do sabre de luz (o hum com o batimento)."""
    n = n_de(seg)
    t = _t(n)
    x = satura(seno(f, n) + seno(f * 1.02, n) * 0.8 + seno(f * 2, n) * 0.3, 2) + passa(rosa(rng, n), 200, 1500, 2) * 0.15
    return x * (0.85 + 0.15 * np.sin(2 * math.pi * 7 * t)) * sobe_e_some(n, 0.15, 1.2) * g


def _sabre_liga(rng, g=0.04):
    n = n_de(0.35)
    return satura(seno(varre(60, 110, n), n) + passa(rosa(rng, n), 300, 3000, 2) * 0.4, 3) * env(n, 0.01, 0.25) * g


def _respira_vader(rng, g=0.3):
    x = _z(1.5)
    n = n_de(0.55)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 30 * t)) * sobe_e_some(n, 0.5, 1.3) * g, 0.0)
    n2 = n_de(0.6)
    poe(x, passa(rosa(rng, n2), 200, 1500, 2) * sobe_e_some(n2, 0.3, 1.3) * g * 0.9, 0.65)
    return x


def _fogo(rng, seg, g=0.3):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 200, 3000, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 11 * t)) * sobe_e_some(n, 0.2, 1.2) * g


def _asas_morcego(rng, seg, g=0.2):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 500, 4000, 2) * (0.4 + 0.6 * np.sin(2 * math.pi * 22 * t) ** 2) * sobe_e_some(n, 0.2, 1.2) * g


def _sibilo_xeno(rng, seg, g=0.3):
    n = n_de(seg)
    t = _t(n)
    return satura(passa(rosa(rng, n), 2000, 9000, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 40 * t)), 2) * env(n, 0.05, seg * 0.6) * g


# ------------------------------------------------------------------ Valak

def aparicao_de_valak(rng, v):
    """Valak: o grito agudo distorcido de cada aparição e o coro sombrio."""
    x = _z(2.4)
    for k in range(3):
        n = n_de(0.3)
        poe(x, satura(seno(varre(1200, 900, n), n) + passa(rosa(rng, n), 1000, 6000, 2) * 0.6, 4) * env(n, 0.01, 0.25) * 0.025, 0.1 + 0.15 * k)
    n2 = n_de(1.2)
    poe(x, (seno(110, n2) + seno(116.5, n2) + seno(164.8, n2) * 0.6) * sobe_e_some(n2, 0.3, 1.2) * 0.02, 0.0)
    return reverb(x, 1.0, 0.5)


def sombra_profana(rng, v):
    """Valak: o hábito envolvendo (o sopro) e o canto gregoriano invertido."""
    x = _z(2.2)
    poe(x, _sopro(rng, 0.8, 150, 1500, 0.2, 0.4), 0.0)
    poe(x, _acorde((147, 175, 208, 247), 1.1, 0.02), 0.2)
    return reverb(x, 1.0, 0.5)


def valak_preparo(rng, v):
    """Valak (Preparo): o sussurro em latim e a cruz rangendo (em laço)."""
    x = _z(1.4)
    for k in range(4):
        n = n_de(0.18)
        poe(x, passa(rosa(rng, n), 1500, 6000, 2) * env(n, 0.04, 0.12) * 0.12, 0.22 * k)
    n2 = n_de(1.0)
    poe(x, (seno(98, n2) + seno(103.8, n2)) * sobe_e_some(n2, 0.5, 1.2) * 0.015, 0.0)
    return reverb(x, 1.0, 0.5)


def possessao(rng, v):
    """Valak: a sombra entrando no rival (o rugido grave) e o grito dele."""
    x = _z(2.4)
    poe(x, _sopro(rng, 0.5, 100, 1500, 0.25, 0.6), 0.2)
    n = n_de(0.6)
    poe(x, satura(seno(varre(150, 60, n), n) + passa(rosa(rng, n), 100, 1500, 2), 5) * env(n, 0.05, 0.45) * 0.05, 0.5)
    poe(x, _baque(60, 22, 0.8, 1.0, 3.0), 0.52)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Drácula

def mordida_do_conde(rng, v):
    """Drácula: a capa abrindo, a mordida e o sangue voltando."""
    x = _z(2.1)
    n = n_de(0.15)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * env(n, 0.01, 0.13) * 0.4, 0.0)
    poe(x, _whoosh(rng, 0.2, 400, 4000, 0.8, 1.3, 0.4), 0.15)
    poe(x, estalo(rng, n_de(0.03), 800, 5000, 0.008) * 1.0, 0.33)
    poe(x, _baque(120, 50, 0.3, 0.55), 0.33)
    n2 = n_de(0.5)
    poe(x, seno(varre(250, 600, n2), n2) * env(n2, 0.1, 0.35) * 0.018, 0.5)
    return reverb(x, 0.8, 0.4)


def nuvem_de_morcegos(rng, v):
    """Drácula: a nuvem de morcegos batendo asas e guinchando."""
    x = _z(2.2)
    poe(x, _asas_morcego(rng, 1.0, 0.25), 0.1)
    q = np.random.default_rng(15)
    for k in range(8):
        f = q.uniform(3500, 6000)
        poe(x, _piu(f, f * 1.15, 0.04, 0.008), 0.15 + 0.09 * k)
    return reverb(x, 0.7, 0.35)


def dracula_preparo(rng, v):
    """Drácula (Preparo): o órgão sombrio e o fogo girando (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, (seno(73.4, n) + seno(87.3, n) * 0.8 + seno(110, n) * 0.6 + seno(146.8, n) * 0.4) * sobe_e_some(n, 0.4, 1.2) * 0.018, 0.0)
    poe(x, _fogo(rng, 1.0, 0.12), 0.0)
    return reverb(x, 1.0, 0.5)


def fogo_infernal(rng, v):
    """Drácula: as colunas de fogo do inferno rugindo debaixo dos rivais."""
    x = _z(2.4)
    for k in range(3):
        poe(x, _baque(70, 30, 0.4, 0.6, 2.6), 0.15 + 0.08 * k)
        poe(x, _fogo(rng, 0.7, 0.3), 0.15 + 0.08 * k)
    poe(x, _explosao(rng, 0.7, 50), 0.2)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Xenomorfo

def segunda_mandibula(rng, v):
    """Xenomorfo: o sibilo, a segunda boca disparando ("TCHAC") e o ácido chiando."""
    x = _z(2.0)
    poe(x, _sibilo_xeno(rng, 0.35, 0.25), 0.0)
    poe(x, estalo(rng, n_de(0.04), 800, 6000, 0.01) * 1.3, 0.35)
    poe(x, _baque(150, 70, 0.2, 0.45), 0.35)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 3000, 10000, 2) * env(n, 0.05, 0.5) * 0.12, 0.42)
    return reverb(x, 0.6, 0.3)


def emboscada_xenomorfa(rng, v):
    """Xenomorfo: o sensor de movimento apitando cada vez mais perto."""
    x = _z(2.2)
    for k in range(5):
        n = n_de(0.08)
        poe(x, seno(1200, n) * env(n, 0.003, 0.07) * (0.015 + 0.004 * k), 0.15 + 0.16 * k - 0.01 * k * k)
    poe(x, _sibilo_xeno(rng, 0.4, 0.15), 0.6)
    return reverb(x, 0.7, 0.35)


def xenomorfo_preparo(rng, v):
    """Xenomorfo (Preparo): a respiração chiada e a baba pingando (em laço)."""
    x = _z(1.4)
    poe(x, _sibilo_xeno(rng, 0.6, 0.15), 0.0)
    poe(x, _piu(900, 400, 0.08, 0.015), 0.8)
    return reverb(x, 0.7, 0.35)


def cauda_perfurante(rng, v):
    """Xenomorfo: a cauda chicoteando e perfurando o rival."""
    x = _z(2.1)
    poe(x, _whoosh(rng, 0.3, 600, 6000, 0.9, 1.3, 0.5), 0.05)
    poe(x, _baque(90, 35, 0.5, 0.8, 2.6), 0.35)
    poe(x, estalo(rng, n_de(0.05), 500, 4000, 0.012) * 1.0, 0.35)
    poe(x, _sibilo_xeno(rng, 0.5, 0.18), 0.45)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Predador

def canhao_de_plasma(rng, v):
    """Predador: a mira de três pontos travando, o canhão carregando e o tiro de plasma."""
    x = _z(2.1)
    for k in range(3):
        poe(x, _piu(2200, 2200, 0.04, 0.012), 0.05 + 0.08 * k)
    n = n_de(0.25)
    poe(x, seno(varre(300, 1200, n), n) * env(n, 0.2, 0.05) * 0.025, 0.15)
    poe(x, _baque(110, 50, 0.3, 0.6), 0.38)
    n2 = n_de(0.2)
    poe(x, passa(rosa(rng, n2), 1000, 6000, 2) * env(n2, 0.01, 0.18) * 0.35, 0.38)
    poe(x, _explosao(rng, 0.4, 80), 0.53)
    return reverb(x, 0.6, 0.3)


def camuflagem_predador(rng, v):
    """Predador: a camuflagem ligando (o chiado elétrico ondulando) e os estalos de língua."""
    x = _z(2.0)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2000, 9000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 12 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.15, 0.1)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.015), 1500, 5000, 0.003) * 0.5, 0.9 + 0.06 * k)
    return reverb(x, 0.6, 0.3)


def predador_preparo(rng, v):
    """Predador (Preparo): o disco abrindo as lâminas e zumbindo (em laço)."""
    x = _z(1.4)
    for k in range(6):
        poe(x, _sino(rng, 2349 + 100 * (k % 3), 0.15, 0.01, METAL), 0.08 * k)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * sobe_e_some(n, 0.5, 1.2) * 0.06, 0.0)
    return reverb(x, 0.5, 0.25)


def trofeu(rng, v):
    """Predador: o disco voando zunindo, cortando e voltando à mão."""
    x = _z(2.2)
    n = n_de(1.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 25 * t) ** 2) * sobe_e_some(n, 0.5, 1.2) * 0.2, 0.05)
    poe(x, _baque(110, 45, 0.35, 0.7, 2.5), 0.38)
    poe(x, _sino(rng, 1568, 0.4, 0.025, METAL), 0.38)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.006) * 0.6, 1.25)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Darth Vader

def esganadura_da_forca(rng, v):
    """Darth Vader: a respiração, a mão fechando e o rival engasgando."""
    x = _z(2.4)
    poe(x, _respira_vader(rng, 0.2), 0.0)
    n = n_de(0.8)
    poe(x, (seno(55, n) + seno(58, n)) * sobe_e_some(n, 0.3, 1.2) * 0.04, 0.25)
    for k in range(3):
        n2 = n_de(0.1)
        poe(x, satura(passa(rosa(rng, n2), 300, 2000, 2), 3) * env(n2, 0.01, 0.08) * 0.25, 0.45 + 0.13 * k)
    return reverb(x, 0.7, 0.35)


def sabre_vermelho_vader(rng, v):
    """Darth Vader: o sabre vermelho ligando ("vshhhm") e o corte pesado."""
    x = _z(2.1)
    poe(x, _sabre_liga(rng, 0.05), 0.0)
    poe(x, _sabre_zumbido(rng, 0.6, 90, 0.035), 0.15)
    poe(x, _whoosh(rng, 0.2, 200, 2500, 0.8, 1.3, 0.45), 0.25)
    poe(x, _baque(110, 45, 0.35, 0.7, 2.5), 0.4)
    n = n_de(0.2)
    poe(x, satura(passa(rosa(rng, n), 1000, 6000, 2), 3) * env(n, 0.005, 0.18) * 0.3, 0.4)
    return reverb(x, 0.6, 0.3)


def vader_preparo(rng, v):
    """Darth Vader (Preparo): a respiração mecânica e o sabre zumbindo (em laço)."""
    x = _z(1.4)
    poe(x, _respira_vader(rng, 0.18), 0.0)
    poe(x, _sabre_zumbido(rng, 1.2, 90, 0.025), 0.0)
    return reverb(x, 0.6, 0.3)


def lado_sombrio(rng, v):
    """Darth Vader: os relâmpagos do lado sombrio, o sabre ligando e o golpe final."""
    x = _z(2.4)
    poe(x, _choque(rng, 0.45, 0.35, 1000, 8000), 0.0)
    poe(x, _sabre_liga(rng, 0.045), 0.3)
    poe(x, _whoosh(rng, 0.2, 200, 2500, 0.85, 1.3, 0.5), 0.42)
    poe(x, _baque(60, 22, 0.8, 1.0, 3.0), 0.55)
    poe(x, _explosao(rng, 0.4, 60), 0.55)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Yoda

def empurrao_da_forca(rng, v):
    """Yoda: a onda da Força (o "vuum" grave que avança) e o rival empurrado."""
    x = _z(2.0)
    n = n_de(0.5)
    poe(x, (seno(varre(80, 140, n), n) + passa(rosa(rng, n), 100, 1500, 2) * 0.5) * env(n, 0.15, 0.3) * 0.05, 0.05)
    poe(x, _whoosh(rng, 0.35, 200, 2500, 0.7, 1.3, 0.45), 0.1)
    poe(x, _baque(120, 50, 0.3, 0.6), 0.42)
    return reverb(x, 0.7, 0.35)


def escudo_da_forca(rng, v):
    """Yoda: as bolhas da Força fechando sobre o trio (o tom calmo e o brilho)."""
    x = _z(2.2)
    for k in range(3):
        n = n_de(0.3)
        poe(x, seno(varre(300 + 50 * k, 600 + 50 * k, n), n) * env(n, 0.2, 0.08) * 0.018, 0.1 + 0.08 * k)
    poe(x, _acorde((392, 494, 587, 784), 1.0, 0.02), 0.35)
    poe(x, _brilho(rng, 0.6, 1568, 0.012, CRISTAL), 0.45)
    return reverb(x, 0.8, 0.4)


def yoda_preparo(rng, v):
    """Yoda (Preparo): a meditação — o tom profundo e as pedras flutuando (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(130.8, n) + seno(196, n) * 0.6) * (0.8 + 0.2 * np.sin(2 * math.pi * 1 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.02, 0.0)
    for k in range(2):
        poe(x, estalo(rng, n_de(0.02), 300, 2000, 0.005) * 0.3, 0.5 * k + 0.2)
    return reverb(x, 0.8, 0.4)


def sabre_do_mestre(rng, v):
    """Yoda: o sabre verde girando (o zumbido indo e vindo) e os cortes."""
    x = _z(2.2)
    poe(x, _sabre_liga(rng, 0.04), 0.0)
    z = _sabre_zumbido(rng, 0.6, 110, 0.035)
    t = _t(len(z))
    poe(x, z * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t) ** 2), 0.1)
    for k in range(4):
        poe(x, _whoosh(rng, 0.1, 600, 5000, 0.7, 1.3, 0.3), 0.42 + 0.06 * k)
        poe(x, _baque(150, 70, 0.15, 0.4), 0.46 + 0.06 * k)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "aparicao-de-valak": (aparicao_de_valak, "Valak: a aparição"),
    "sombra-profana": (sombra_profana, "Valak: a sombra profana"),
    "valak-preparo": (valak_preparo, "Valak: o sussurro em latim (Preparo)"),
    "possessao": (possessao, "Valak: a possessão"),
    "mordida-do-conde": (mordida_do_conde, "Drácula: a mordida do conde"),
    "nuvem-de-morcegos": (nuvem_de_morcegos, "Drácula: a nuvem de morcegos"),
    "dracula-preparo": (dracula_preparo, "Drácula: o órgão sombrio (Preparo)"),
    "fogo-infernal": (fogo_infernal, "Drácula: o fogo infernal"),
    "segunda-mandibula": (segunda_mandibula, "Xenomorfo: a segunda mandíbula"),
    "emboscada-xenomorfa": (emboscada_xenomorfa, "Xenomorfo: a emboscada"),
    "xenomorfo-preparo": (xenomorfo_preparo, "Xenomorfo: o chiado (Preparo)"),
    "cauda-perfurante": (cauda_perfurante, "Xenomorfo: a cauda perfurante"),
    "canhao-de-plasma": (canhao_de_plasma, "Predador: o canhão de plasma"),
    "camuflagem-predador": (camuflagem_predador, "Predador: a camuflagem"),
    "predador-preparo": (predador_preparo, "Predador: o disco abrindo (Preparo)"),
    "trofeu": (trofeu, "Predador: o troféu"),
    "esganadura-da-forca": (esganadura_da_forca, "Darth Vader: a esganadura da Força"),
    "sabre-vermelho-vader": (sabre_vermelho_vader, "Darth Vader: o sabre vermelho"),
    "vader-preparo": (vader_preparo, "Darth Vader: a respiração (Preparo)"),
    "lado-sombrio": (lado_sombrio, "Darth Vader: o lado sombrio"),
    "empurrao-da-forca": (empurrao_da_forca, "Yoda: o empurrão da Força"),
    "escudo-da-forca": (escudo_da_forca, "Yoda: o escudo da Força"),
    "yoda-preparo": (yoda_preparo, "Yoda: a meditação (Preparo)"),
    "sabre-do-mestre": (sabre_do_mestre, "Yoda: o sabre do mestre"),
}
