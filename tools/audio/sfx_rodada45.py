"""Os sons da rodada 45 das habilidades próprias (veja tools/vfx/familias_v2/rodada45.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _choque(rng, seg, g=0.3, f0=1500, f1=7000):
    """O estalo elétrico picotado (bzzzt)."""
    n = n_de(seg)
    t = _t(n)
    corte = (np.sin(2 * math.pi * 55 * t) > 0.2).astype(float)
    return satura(passa(rosa(rng, n), f0, f1, 2) * corte, 3) * env(n, 0.005, seg * 0.5) * g


def _mana(rng, f, seg, g=0.03):
    """O tom de mana: acorde brilhante que oscila."""
    n = n_de(seg)
    t = _t(n)
    return (seno(f, n) + seno(f * 1.5, n) * 0.5 + seno(f * 2.01, n) * 0.3) * (0.7 + 0.3 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(n, 0.3, 1.2) * g


# ------------------------------------------------------------------ Gwen

def rajada_de_mana(rng, v):
    """Gwen: a mana carregando na mão e o feixe rosa zunindo até o rival."""
    x = _z(1.9)
    n = n_de(0.3)
    poe(x, seno(varre(400, 900, n), n) * env(n, 0.25, 0.05) * 0.025, 0.0)
    poe(x, _mana(rng, 784, 0.45, 0.03), 0.2)
    poe(x, _whoosh(rng, 0.25, 1500, 7000, 0.6, 1.3, 0.35), 0.2)
    poe(x, _baque(140, 60, 0.3, 0.5), 0.45)
    poe(x, _brilho(rng, 0.5, 1568, 0.02, CRISTAL), 0.45)
    return reverb(x, 0.6, 0.3)


def barreira_de_mana(rng, v):
    """Gwen: os hexágonos se encaixando ("tic-tic-tic" de vidro) e a barreira zumbindo."""
    x = _z(2.1)
    for k in range(9):
        poe(x, _sino(rng, 1568 + 110 * (k % 4), 0.25, 0.015, CRISTAL), 0.05 + 0.035 * k)
    poe(x, _mana(rng, 523, 1.0, 0.025), 0.3)
    poe(x, _brilho(rng, 0.6, 2093, 0.015, CRISTAL), 0.55)
    return reverb(x, 0.7, 0.35)


def gwen_preparo(rng, v):
    """Gwen (Preparo): o feitiço sendo recitado (o coro de mana girando em laço)."""
    x = _z(1.4)
    poe(x, _mana(rng, 440, 1.0, 0.02), 0.0)
    for k in range(3):
        poe(x, _sino(rng, 1319 + 220 * k, 0.4, 0.01, CRISTAL), 0.3 * k)
    return reverb(x, 0.7, 0.35)


def lucubra(rng, v):
    """Gwen: Lucubra — o círculo abrindo, as ondas de mana e os buffs quebrando como vidro."""
    x = _z(2.4)
    poe(x, _acorde((523, 659, 784, 1047), 1.0, 0.025), 0.0)
    for k in range(4):
        poe(x, _whoosh(rng, 0.3, 800, 6000, 0.6, 1.3, 0.35), 0.25 + 0.08 * k)
    for k in range(3):
        poe(x, _baque(150, 70, 0.2, 0.4), 0.45 + 0.08 * k)
        for m in range(4):
            poe(x, _sino(rng, 2637 + 300 * m, 0.15, 0.012, CRISTAL), 0.5 + 0.08 * k + 0.02 * m)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Viúva Negra

def mordida_da_viuva(rng, v):
    """Viúva Negra: os discos disparados ("pt-pt") e o choque prendendo o rival."""
    x = _z(2.0)
    for k in range(2):
        poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.006) * 0.7, 0.05 + 0.08 * k)
        poe(x, _whoosh(rng, 0.2, 2000, 9000, 0.6, 1.3, 0.25), 0.05 + 0.08 * k)
    poe(x, _choque(rng, 0.6, 0.32), 0.38)
    poe(x, _baque(160, 80, 0.15, 0.35), 0.38)
    return reverb(x, 0.5, 0.25)


def chave_de_pernas(rng, v):
    """Viúva Negra: o salto, o giro no pescoço e o rival batendo no chão."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 500, 4000, 0.6, 1.3, 0.35), 0.0)
    poe(x, _whoosh(rng, 0.25, 300, 3000, 0.7, 1.3, 0.4), 0.25)
    poe(x, _baque(65, 25, 0.6, 0.9, 2.8), 0.5)
    poe(x, estalo(rng, n_de(0.05), 300, 3000, 0.012) * 0.7, 0.5)
    poe(x, _sino(rng, 1760, 0.3, 0.015, METAL), 0.62)
    return reverb(x, 0.5, 0.25)


def viuva_preparo(rng, v):
    """Viúva Negra (Preparo): os bastões ligando e faiscando (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, satura(seno(120, n), 3) * sobe_e_some(n, 0.5, 1.2) * 0.02, 0.0)
    for k in range(4):
        poe(x, _choque(rng, 0.08, 0.15), 0.25 * k)
    return reverb(x, 0.5, 0.25)


def missao_cumprida(rng, v):
    """Viúva Negra: o avanço rápido e os dois bastões elétricos cruzando no rival."""
    x = _z(2.1)
    poe(x, _whoosh(rng, 0.25, 1000, 8000, 0.7, 1.3, 0.4), 0.0)
    for k in range(2):
        poe(x, _baque(110, 45, 0.35, 0.7, 2.5), 0.28 + 0.06 * k)
        poe(x, _choque(rng, 0.3, 0.3), 0.28 + 0.06 * k)
    poe(x, _explosao(rng, 0.4, 70), 0.35)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Gavião Arqueiro

def _soltar(rng):
    """A corda do arco soltando ("tuóng") e a flecha partindo."""
    x = _z(0.5)
    n = n_de(0.25)
    poe(x, seno(varre(220, 180, n), n) * env(n, 0.002, 0.2) * 0.05, 0.0)
    poe(x, estalo(rng, n_de(0.02), 600, 4000, 0.004) * 0.6, 0.0)
    poe(x, _whoosh(rng, 0.2, 2000, 9000, 0.6, 1.3, 0.3), 0.01)
    return x


def flecha_explosiva(rng, v):
    """Gavião: a flecha cravando e o bipe da carga armada."""
    x = _z(1.9)
    poe(x, _soltar(rng), 0.0)
    poe(x, _baque(200, 100, 0.12, 0.35), 0.3)
    for k in range(5):
        poe(x, _piu(1800, 1800, 0.05, 0.02), 0.4 + 0.125 * k)
    return reverb(x, 0.4, 0.2)


def flecha_de_rede(rng, v):
    """Gavião: a flecha voando, a rede abrindo ("fwump") e apertando."""
    x = _z(1.9)
    poe(x, _soltar(rng), 0.0)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * env(n, 0.02, 0.2) * 0.4, 0.3)
    poe(x, _baque(170, 90, 0.15, 0.35), 0.32)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.03), 1000, 4000, 0.008) * 0.3, 0.5 + 0.05 * k)
    return reverb(x, 0.4, 0.2)


def gaviao_preparo(rng, v):
    """Gavião (Preparo): o arco esticando (o rangido da corda em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 800, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 18 * t) ** 2) * sobe_e_some(n, 0.5, 1.2) * 0.08, 0.0)
    poe(x, seno(varre(150, 165, n), n) * sobe_e_some(n, 0.6, 1.2) * 0.012, 0.0)
    return reverb(x, 0.4, 0.2)


def chuva_de_flechas(rng, v):
    """Gavião: a rajada de flechas subindo e o chiado delas caindo em tudo."""
    x = _z(2.4)
    for k in range(5):
        poe(x, _soltar(rng) * 0.6, 0.04 * k)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 3000, 10000, 2) * sobe_e_some(n, 0.6, 1.2) * 0.25, 0.3)
    q = np.random.default_rng(3)
    for k in range(14):
        poe(x, _baque(q.uniform(180, 260), 100, 0.06, 0.25), 0.55 + q.uniform(0, 0.45))
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Gamora

def godslayer_corte(rng, v):
    """Gamora: a Godslayer abrindo ("clac-shiiing") e o corte."""
    x = _z(1.9)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.006) * 0.7, 0.0)
    poe(x, _sino(rng, 1568, 0.6, 0.035, METAL), 0.05)
    poe(x, _whoosh(rng, 0.2, 2000, 10000, 0.8, 1.3, 0.5), 0.2)
    poe(x, _baque(140, 60, 0.25, 0.5), 0.4)
    return reverb(x, 0.5, 0.25)


def golpe_acrobatico(rng, v):
    """Gamora: o mortal no ar (o giro) e o calcanhar descendo."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.4, 300, 3000, 0.5, 1.4, 0.4), 0.0)
    poe(x, _baque(110, 45, 0.4, 0.8, 2.6), 0.4)
    poe(x, estalo(rng, n_de(0.04), 500, 4000, 0.01) * 0.6, 0.4)
    return reverb(x, 0.5, 0.25)


def gamora_preparo(rng, v):
    """Gamora (Preparo): o brilho correndo pelo fio da espada (o tinido longo em laço)."""
    x = _z(1.4)
    poe(x, _sino(rng, 2093, 0.9, 0.012, METAL), 0.0)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 5000, 12000, 2) * sobe_e_some(n, 0.5, 1.2) * 0.05, 0.0)
    return reverb(x, 0.6, 0.3)


def execucao_de_gamora(rng, v):
    """Gamora: o vulto passando, o silêncio, e o corte abrindo de uma vez."""
    x = _z(2.2)
    poe(x, _whoosh(rng, 0.2, 2000, 12000, 0.8, 1.3, 0.5), 0.0)
    poe(x, _sino(rng, 2637, 0.4, 0.025, METAL), 0.22)
    poe(x, _baque(60, 22, 0.8, 1.0, 3.0), 0.52)
    poe(x, _whoosh(rng, 0.15, 3000, 12000, 0.5, 1.3, 0.4), 0.5)
    poe(x, _explosao(rng, 0.5, 55), 0.52)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Drax

def facas_gemeas(rng, v):
    """Drax: as duas facas raspando e cortando em X."""
    x = _z(1.8)
    for k in range(2):
        poe(x, _whoosh(rng, 0.18, 2000, 9000, 0.7, 1.3, 0.45), 0.1 + 0.03 * k)
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.025, METAL), 0.3 + 0.03 * k)
    poe(x, _baque(130, 55, 0.3, 0.6), 0.32)
    poe(x, _whoosh(rng, 0.3, 1500, 6000, 0.4, 1.3, 0.3), 0.55)
    return reverb(x, 0.5, 0.25)


def grito_de_drax(rng, v):
    """Drax: o grito de guerra grave e rouco ecoando."""
    x = _z(2.2)
    n = n_de(0.9)
    grito = satura(seno(varre(110, 90, n), n) + seno(varre(220, 180, n), n) * 0.4 + passa(rosa(rng, n), 200, 2000, 2) * 0.8, 5)
    poe(x, grito * env(n, 0.05, 0.4) * 0.07, 0.05)
    n2 = n_de(0.8)
    poe(x, seno(55, n2) * sobe_e_some(n2, 0.2, 1.2) * 0.05, 0.1)
    return reverb(x, 0.9, 0.45)


def drax_preparo(rng, v):
    """Drax (Preparo): o punho apertando e o chão rangendo (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 40, 400, 2), 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 2.5 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.35, 0.0)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.04), 200, 2000, 0.01) * 0.3, 0.3 * k + 0.1)
    return reverb(x, 0.5, 0.25)


def o_destruidor(rng, v):
    """Drax: a corrida pesada e o soco que racha o chão."""
    x = _z(2.3)
    for k in range(3):
        poe(x, _baque(90, 50, 0.15, 0.3), 0.08 * k)
    poe(x, _whoosh(rng, 0.25, 200, 2500, 0.8, 1.3, 0.45), 0.08)
    poe(x, _baque(40, 16, 1.2, 1.0, 3.4), 0.3)
    poe(x, _explosao(rng, 0.8, 40), 0.3)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.05), 150, 2500, 0.015) * 0.5, 0.34 + 0.05 * k)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Mulher-Aranha

def rajada_venenosa(rng, v):
    """Mulher-Aranha: a mão carregando e a rajada bioelétrica estalando no rival."""
    x = _z(1.9)
    n = n_de(0.3)
    poe(x, seno(varre(200, 800, n), n) * env(n, 0.25, 0.05) * 0.025, 0.0)
    poe(x, _choque(rng, 0.4, 0.35, 1000, 6000), 0.22)
    poe(x, _baque(150, 60, 0.25, 0.5), 0.32)
    n2 = n_de(0.5)
    poe(x, passa(rosa(rng, n2), 2000, 6000, 2) * env(n2, 0.02, 0.4) * 0.12, 0.4)
    return reverb(x, 0.5, 0.25)


def voo_planado(rng, v):
    """Mulher-Aranha: as asas abrindo ("fwap") e o vento do planeio."""
    x = _z(2.0)
    n = n_de(0.12)
    poe(x, passa(rosa(rng, n), 200, 2000, 2) * env(n, 0.005, 0.1) * 0.5, 0.0)
    poe(x, _sopro(rng, 0.8, 400, 3000, 0.2, 0.4), 0.1)
    poe(x, _whoosh(rng, 0.5, 600, 5000, 0.5, 1.3, 0.35), 0.15)
    return reverb(x, 0.5, 0.25)


def mulher_aranha_preparo(rng, v):
    """Mulher-Aranha (Preparo): a bioeletricidade estalando nas mãos (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, satura(seno(100, n) + seno(150, n) * 0.5, 3) * sobe_e_some(n, 0.5, 1.2) * 0.015, 0.0)
    for k in range(5):
        poe(x, _choque(rng, 0.06, 0.12, 2000, 8000), 0.2 * k + 0.05)
    return reverb(x, 0.5, 0.25)


def choque_total(rng, v):
    """Mulher-Aranha: o raio enorme caindo no rival e a estática presa nele."""
    x = _z(2.3)
    n = n_de(0.25)
    poe(x, seno(varre(150, 900, n), n) * env(n, 0.2, 0.05) * 0.025, 0.0)
    poe(x, _trovao(rng, 1.4), 0.2)
    poe(x, _choque(rng, 0.5, 0.4, 800, 7000), 0.22)
    poe(x, _baque(55, 20, 0.8, 1.0, 3.0), 0.22)
    for k in range(4):
        poe(x, _choque(rng, 0.06, 0.12), 0.6 + 0.1 * k)
    return reverb(x, 0.7, 0.35)


SONS: dict = {
    "rajada-de-mana": (rajada_de_mana, "Gwen: a rajada de mana"),
    "barreira-de-mana": (barreira_de_mana, "Gwen: a barreira de mana"),
    "gwen-preparo": (gwen_preparo, "Gwen: o feitiço recitado (Preparo)"),
    "lucubra": (lucubra, "Gwen: Lucubra"),
    "mordida-da-viuva": (mordida_da_viuva, "Viúva Negra: a mordida da viúva"),
    "chave-de-pernas": (chave_de_pernas, "Viúva Negra: a chave de pernas"),
    "viuva-preparo": (viuva_preparo, "Viúva Negra: os bastões faiscando (Preparo)"),
    "missao-cumprida": (missao_cumprida, "Viúva Negra: missão cumprida"),
    "flecha-explosiva": (flecha_explosiva, "Gavião Arqueiro: a flecha explosiva"),
    "flecha-de-rede": (flecha_de_rede, "Gavião Arqueiro: a flecha de rede"),
    "gaviao-preparo": (gaviao_preparo, "Gavião Arqueiro: o arco puxado (Preparo)"),
    "chuva-de-flechas": (chuva_de_flechas, "Gavião Arqueiro: a chuva de flechas"),
    "godslayer-corte": (godslayer_corte, "Gamora: a Godslayer"),
    "golpe-acrobatico": (golpe_acrobatico, "Gamora: o golpe acrobático"),
    "gamora-preparo": (gamora_preparo, "Gamora: o brilho na lâmina (Preparo)"),
    "execucao-de-gamora": (execucao_de_gamora, "Gamora: a execução"),
    "facas-gemeas": (facas_gemeas, "Drax: as facas gêmeas"),
    "grito-de-drax": (grito_de_drax, "Drax: o grito de guerra"),
    "drax-preparo": (drax_preparo, "Drax: os punhos apertando (Preparo)"),
    "o-destruidor": (o_destruidor, "Drax: O Destruidor"),
    "rajada-venenosa": (rajada_venenosa, "Mulher-Aranha: a rajada venenosa"),
    "voo-planado": (voo_planado, "Mulher-Aranha: o voo planado"),
    "mulher-aranha-preparo": (mulher_aranha_preparo, "Mulher-Aranha: as mãos estalando (Preparo)"),
    "choque-total": (choque_total, "Mulher-Aranha: o choque total"),
}
