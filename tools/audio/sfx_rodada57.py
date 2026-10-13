"""Os sons da rodada 57 das habilidades próprias (veja tools/vfx/familias_v2/rodada57.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _estouro_seco(rng, g=0.5):
    """A explosão curta e estalada do Bakugo (o "BAM" de nitroglicerina)."""
    n = n_de(0.5)
    return (satura(passa(rosa(rng, n), 200, 7000, 2) * env(n, 0.001, 0.12), 3) * 0.8 + satura(seno(varre(120, 40, n), n), 2) * env(n, 0.001, 0.15) * 0.5) * g


def _fogo(rng, seg, g=0.3, f0=200, f1=3000):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), f0, f1, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 11 * t)) * sobe_e_some(n, 0.2, 1.2) * g


def _gelo_cresce(rng, seg, g=0.3):
    x = _z(seg + 0.3)
    q = np.random.default_rng(57)
    for k in range(int(seg * 30)):
        poe(x, estalo(rng, n_de(0.015), 3000, 10000, 0.003) * g * q.uniform(0.3, 1.0), k / 30)
    return x


def _zumbido_psi(seg, f=220, g=0.02):
    n = n_de(seg)
    t = _t(n)
    return (seno(f, n) + seno(f * 1.5, n) * 0.5 + seno(f * 2.01, n) * 0.3) * (0.6 + 0.4 * np.sin(2 * math.pi * 5 * t)) * sobe_e_some(n, 0.5, 1.2) * g


def _agua(rng, seg, g=0.3, lo=300, hi=6000):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), lo, hi, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 17 * t)) * sobe_e_some(n, 0.3, 1.3) * g


def _tique(rng, g=0.3):
    return estalo(rng, n_de(0.03), 2500, 7000, 0.004) * g


# ------------------------------------------------------------------ Bakugo

def explosao_bakugo(rng, v):
    """Bakugo: o chiado do suor na palma e a explosão ("MORRE!")."""
    x = _z(2.0)
    n = n_de(0.2)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * env(n, 0.05, 0.1) * 0.15, 0.0)
    poe(x, _estouro_seco(rng, 0.7), 0.2)
    poe(x, _estouro_seco(rng, 0.45), 0.28)
    poe(x, _fogo(rng, 0.6, 0.18), 0.35)
    return reverb(x, 0.7, 0.35)


def granada_bakugo(rng, v):
    """Bakugo: o pino da manopla, o disparo, a explosão e o bipe da bomba marcada."""
    x = _z(2.2)
    poe(x, _sino(rng, 1760, 0.15, 0.02, METAL), 0.05)
    poe(x, _whoosh(rng, 0.25, 500, 4000, 0.7, 1.3, 0.4), 0.2)
    poe(x, _estouro_seco(rng, 0.6), 0.43)
    for k in range(4):
        poe(x, _piu(1800, 1800, 0.05, 0.02), 0.65 + 0.12 * k)
    return reverb(x, 0.7, 0.35)


def bakugo_preparo(rng, v):
    """Bakugo (Preparo): as explosõezinhas empurrando o giro ("pá-pá-pá") e o vento (em laço)."""
    x = _z(1.4)
    poe(x, _sopro(rng, 1.2, 300, 3000, 0.12, 0.5), 0.0)
    for k in range(5):
        poe(x, _estouro_seco(rng, 0.18), 0.05 + 0.22 * k)
    return reverb(x, 0.6, 0.3)


def howitzer_impact(rng, v):
    """Bakugo: "HOWITZER IMPACT!" — o tornado de explosões girando e a explosão gigante."""
    x = _z(2.9)
    for k in range(10):
        poe(x, _estouro_seco(rng, 0.12 + 0.03 * k), 0.03 + 0.045 * k)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 200, 3000, 2) * sobe_e_some(n, 0.8, 1.3) * 0.3, 0.0)
    poe(x, _baque(30, 10, 1.6, 1.0, 4.0), 0.46)
    poe(x, _explosao(rng, 1.0, 30), 0.46)
    poe(x, _fogo(rng, 1.0, 0.2), 0.55)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Todoroki

def muralha_de_gelo_todoroki(rng, v):
    """Todoroki: a geleira subindo pelo chão em estalos e o gelo prendendo o rival."""
    x = _z(2.2)
    poe(x, _gelo_cresce(rng, 0.5, 0.35), 0.05)
    for k in range(5):
        poe(x, _baque(150 - 10 * k, 80, 0.12, 0.3), 0.05 + 0.08 * k)
    poe(x, _sino(rng, 2093, 0.8, 0.03, CRISTAL), 0.4)
    poe(x, _baque(60, 30, 0.6, 0.7, 2.5), 0.4)
    return reverb(x, 0.9, 0.45)


def chama_esquerda(rng, v):
    """Todoroki: o fogo da mão esquerda acendendo ("FUUSH") e queimando o rival."""
    x = _z(2.0)
    n = n_de(0.15)
    poe(x, passa(rosa(rng, n), 500, 4000, 2) * env(n, 0.01, 0.1) * 0.3, 0.0)
    poe(x, _fogo(rng, 0.8, 0.4, 150, 4500), 0.05)
    poe(x, _baque(80, 40, 0.3, 0.5), 0.32)
    poe(x, _fogo(rng, 0.6, 0.15), 0.5)
    return reverb(x, 0.7, 0.35)


def todoroki_preparo(rng, v):
    """Todoroki (Preparo): o gelo estalando de um lado e o fogo crepitando do outro (em laço)."""
    x = _z(1.4)
    poe(x, _fogo(rng, 1.1, 0.12), 0.0)
    poe(x, _gelo_cresce(rng, 1.0, 0.12), 0.1)
    return reverb(x, 0.7, 0.35)


def ponto_de_fusao(rng, v):
    """Todoroki: o gelo cobrindo o chão, o fogo por cima e o estouro de vapor ("TSSSHH")."""
    x = _z(2.8)
    poe(x, _gelo_cresce(rng, 0.4, 0.3), 0.0)
    poe(x, _fogo(rng, 0.6, 0.3), 0.3)
    poe(x, _baque(45, 18, 1.0, 0.9, 3.0), 0.52)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 2000, 10000, 2) * env(n, 0.01, 0.8) * 0.45, 0.52)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Mob

def telecinese_mob(rng, v):
    """Mob: as pedras se soltando do chão, flutuando e se chocando no rival."""
    x = _z(2.0)
    poe(x, _zumbido_psi(0.6, 180, 0.02), 0.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.05), 150, 2000, 0.015) * 0.4, 0.04 * k)
        poe(x, _whoosh(rng, 0.15, 400, 3000, 0.7, 1.3, 0.3), 0.3 + 0.04 * k)
        poe(x, _baque(110, 50, 0.2, 0.5), 0.45 + 0.04 * k)
    poe(x, _piu(400, 900, 0.3, 0.015), 0.6)
    return reverb(x, 0.7, 0.35)


def barreira_psiquica_mob(rng, v):
    """Mob: a cúpula psíquica fechando (o zumbido e o "vuum")."""
    x = _z(2.0)
    n = n_de(0.4)
    poe(x, seno(varre(150, 450, n), n) * env(n, 0.2, 0.15) * 0.03, 0.05)
    poe(x, _zumbido_psi(1.0, 330, 0.018), 0.3)
    poe(x, _sino(rng, 660, 0.6, 0.025, CRISTAL), 0.35)
    poe(x, _piu(400, 900, 0.3, 0.015), 0.6)
    return reverb(x, 0.8, 0.4)


def mob_preparo(rng, v):
    """Mob (Preparo): a emoção subindo até 100% (o zumbido crescendo e o tremor em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, (seno(110 + 80 * t, n) + seno(165 + 120 * t, n) * 0.5) * (0.6 + 0.4 * np.sin(2 * math.pi * (6 + 6 * t) * t)) * sobe_e_some(n, 0.7, 1.2) * 0.025, 0.0)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.04), 150, 2000, 0.012) * 0.2, 0.2 + 0.35 * k)
    return reverb(x, 0.7, 0.35)


def cem_por_cento(rng, v):
    """Mob: "100%" — a coluna de energia estourando para o alto e as ondas psíquicas."""
    x = _z(2.9)
    n = n_de(0.4)
    poe(x, seno(varre(200, 1600, n), n) * env(n, 0.35, 0.03) * 0.03, 0.0)
    poe(x, _baque(35, 12, 1.4, 1.0, 3.5), 0.3)
    poe(x, _acorde((220, 277, 330, 440), 1.4, 0.03, 0.05, 0.8), 0.3)
    for k in range(4):
        poe(x, _whoosh(rng, 0.5, 200, 2000, 0.4, 1.3, 0.4), 0.35 + 0.07 * k)
    n = n_de(1.4)
    poe(x, passa(rosa(rng, n), 100, 3000, 2) * sobe_e_some(n, 0.2, 1.2) * 0.35, 0.35)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Rimuru

def devorar_rimuru(rng, v):
    """Rimuru: o slime abrindo a boca, o "glup" engolindo e o brilho da habilidade copiada."""
    x = _z(2.0)
    n = n_de(0.2)
    poe(x, seno(varre(200, 120, n), n) * env(n, 0.02, 0.15) * 0.05, 0.12)
    poe(x, _whoosh(rng, 0.4, 3000, 500, 0.7, 1.3, 0.3), 0.25)
    n = n_de(0.15)
    poe(x, satura(seno(varre(300, 90, n), n), 3) * env(n, 0.005, 0.1) * 0.08, 0.63)
    poe(x, _brilho(rng, 0.6, 1319, 0.03, CRISTAL), 0.68)
    return reverb(x, 0.7, 0.35)


def grande_sabio(rng, v):
    """Rimuru: a voz do Grande Sábio (os bipes de análise) e os painéis abrindo no trio."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _piu(1200 + 200 * k, 1200 + 200 * k, 0.06, 0.02), 0.1 + 0.08 * k)
        n = n_de(0.08)
        poe(x, passa(rosa(rng, n), 4000, 10000, 2) * env(n, 0.005, 0.05) * 0.05, 0.12 + 0.08 * k)
    poe(x, _acorde((523, 659, 784, 988), 0.9, 0.025), 0.45)
    return reverb(x, 0.8, 0.4)


def rimuru_preparo(rng, v):
    """Rimuru (Preparo): a água girando e a pressão subindo (o chiado fino em laço)."""
    x = _z(1.4)
    poe(x, _agua(rng, 1.2, 0.15), 0.0)
    n = n_de(1.1)
    t = _t(n)
    poe(x, seno(1800 + 600 * t, n) * sobe_e_some(n, 0.7, 1.2) * 0.008, 0.0)
    return reverb(x, 0.6, 0.3)


def corte_de_agua(rng, v):
    """Rimuru: a lâmina de água em alta pressão ("SHHIIK") e os respingos."""
    x = _z(2.0)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 4000, 12000, 2) * sobe_e_some(n, 0.6, 1.2) * 0.35, 0.1)
    poe(x, _whoosh(rng, 0.25, 2000, 9000, 0.8, 1.3, 0.5), 0.2)
    poe(x, _sino(rng, 2637, 0.4, 0.02, METAL), 0.4)
    poe(x, _agua(rng, 0.6, 0.3, 500, 7000), 0.42)
    for k in range(5):
        poe(x, _piu(900 + 150 * k, 600, 0.05, 0.012), 0.48 + 0.05 * k)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Ainz

def toque_da_morte_ainz(rng, v):
    """Ainz: os ossos da mão estalando, o aperto e o selo da maldição soando."""
    x = _z(2.1)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.03), 800, 4000, 0.006) * 0.35, 0.05 + 0.06 * k)
    poe(x, _baque(70, 35, 0.4, 0.6), 0.33)
    poe(x, _acorde((110, 117, 165), 1.0, 0.025, 0.02, 0.6), 0.4)
    poe(x, _sino(rng, 247, 0.8, 0.03, METAL), 0.5)
    return reverb(x, 0.9, 0.45)


def invocar_mortos(rng, v):
    """Ainz: o círculo de magia, a terra se abrindo e o rugido do Cavaleiro da Morte."""
    x = _z(2.5)
    poe(x, _acorde((147, 156, 220), 0.8, 0.02, 0.2, 0.5), 0.0)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 40, 600, 2) * sobe_e_some(n, 0.5, 1.2) * 0.4, 0.25)
    for k in range(3):
        poe(x, _baque(50, 25, 0.25, 0.5), 0.35 + 0.12 * k)
    n = n_de(0.7)
    t = _t(n)
    poe(x, satura(seno(varre(110, 70, n), n) * (1 + 0.2 * np.sin(2 * math.pi * 30 * t)) + passa(rosa(rng, n), 100, 1200, 2), 5) * env(n, 0.08, 0.4) * 0.05, 0.65)
    poe(x, _sino(rng, 196, 0.6, 0.03, METAL), 0.7)
    return reverb(x, 1.0, 0.5)


def ainz_preparo(rng, v):
    """Ainz (Preparo): o tique-taque do relógio e o coro dos mortos (em laço)."""
    x = _z(1.4)
    for k in range(5):
        poe(x, _tique(rng, 0.25 if k % 2 == 0 else 0.15), 0.05 + 0.27 * k)
    poe(x, _acorde((98, 117, 147), 1.2, 0.02, 0.3, 0.6), 0.0)
    return reverb(x, 0.9, 0.45)


def o_fim_de_toda_vida(rng, v):
    """Ainz: o relógio gigante tique-taqueando cada vez mais rápido, o sino e a onda da morte."""
    x = _z(3.0)
    tq = 0.0
    passo = 0.12
    while tq < 0.6:
        poe(x, _tique(rng, 0.3), tq)
        tq += passo
        passo *= 0.85
    poe(x, _sino(rng, 131, 1.6, 0.06, SINO), 0.62)
    poe(x, _baque(35, 12, 1.2, 0.9, 3.2), 0.62)
    n = n_de(1.5)
    poe(x, passa(rosa(rng, n), 60, 1500, 2) * sobe_e_some(n, 0.3, 1.2) * 0.4, 0.65)
    poe(x, _acorde((65, 98, 110, 147), 1.6, 0.03, 0.1, 0.9), 0.7)
    return reverb(x, 1.2, 0.55)


# ------------------------------------------------------------------ Lelouch

def geass_lelouch(rng, v):
    """Lelouch: o Geass acendendo no olho ("Lelouch vi Britannia ordena!") e o selo entrando no rival."""
    x = _z(2.2)
    n = n_de(0.3)
    poe(x, seno(varre(300, 1200, n), n) * env(n, 0.25, 0.05) * 0.02, 0.0)
    poe(x, _sino(rng, 988, 0.5, 0.03, CRISTAL), 0.2)
    poe(x, _whoosh(rng, 0.35, 800, 5000, 0.6, 1.3, 0.35), 0.2)
    poe(x, _acorde((311, 370, 466), 0.9, 0.025, 0.01, 0.5), 0.5)
    poe(x, _sino(rng, 1245, 0.6, 0.02, CRISTAL), 0.5)
    return reverb(x, 0.9, 0.45)


def xadrez(rng, v):
    """Lelouch: as peças pousando no tabuleiro ("toc-toc-toc") e o acorde da estratégia."""
    x = _z(2.0)
    for k in range(4):
        poe(x, _baque(600, 400, 0.05, 0.25, 1.5), 0.15 + 0.1 * k)
        poe(x, estalo(rng, n_de(0.02), 2000, 6000, 0.004) * 0.25, 0.15 + 0.1 * k)
    poe(x, _acorde((392, 494, 587, 784), 0.8, 0.025), 0.55)
    return reverb(x, 0.7, 0.35)


def lelouch_preparo(rng, v):
    """Lelouch (Preparo): o rei girando no tabuleiro e o zumbido do Geass (em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, (seno(311, n) + seno(466, n) * 0.5) * (0.6 + 0.4 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.012, 0.0)
    poe(x, _baque(600, 400, 0.05, 0.2, 1.5), 0.3)
    poe(x, _baque(600, 400, 0.05, 0.2, 1.5), 0.9)
    return reverb(x, 0.7, 0.35)


def xeque_mate(rng, v):
    """Lelouch: "Xeque-mate." — o rei avançando, o rei rival tombando e o feixe roxo."""
    x = _z(2.4)
    poe(x, _baque(500, 300, 0.08, 0.35, 1.5), 0.2)
    poe(x, _whoosh(rng, 0.3, 300, 3500, 0.7, 1.3, 0.5), 0.32)
    poe(x, _baque(60, 25, 0.6, 0.8, 2.6), 0.45)
    for k in range(3):
        poe(x, _baque(700 - 100 * k, 400, 0.05, 0.2, 1.5), 0.5 + 0.07 * k)
    poe(x, _acorde((233, 277, 311, 466), 1.0, 0.03, 0.02, 0.6), 0.55)
    return reverb(x, 0.9, 0.45)


SONS: dict = {
    "explosao-bakugo": (explosao_bakugo, "Bakugo: explosão"),
    "granada-bakugo": (granada_bakugo, "Bakugo: granada"),
    "bakugo-preparo": (bakugo_preparo, "Bakugo: girando nas explosões (Preparo)"),
    "howitzer-impact": (howitzer_impact, "Bakugo: Howitzer Impact"),
    "muralha-de-gelo-todoroki": (muralha_de_gelo_todoroki, "Todoroki: muralha de gelo"),
    "chama-esquerda": (chama_esquerda, "Todoroki: chama esquerda"),
    "todoroki-preparo": (todoroki_preparo, "Todoroki: gelo e fogo (Preparo)"),
    "ponto-de-fusao": (ponto_de_fusao, "Todoroki: ponto de fusão"),
    "telecinese-mob": (telecinese_mob, "Mob: telecinese"),
    "barreira-psiquica-mob": (barreira_psiquica_mob, "Mob: barreira psíquica"),
    "mob-preparo": (mob_preparo, "Mob: a emoção subindo (Preparo)"),
    "cem-por-cento": (cem_por_cento, "Mob: 100%"),
    "devorar-rimuru": (devorar_rimuru, "Rimuru: devorar"),
    "grande-sabio": (grande_sabio, "Rimuru: Grande Sábio"),
    "rimuru-preparo": (rimuru_preparo, "Rimuru: a água girando (Preparo)"),
    "corte-de-agua": (corte_de_agua, "Rimuru: corte de água"),
    "toque-da-morte-ainz": (toque_da_morte_ainz, "Ainz: toque da morte"),
    "invocar-mortos": (invocar_mortos, "Ainz: invocar mortos"),
    "ainz-preparo": (ainz_preparo, "Ainz: o relógio e o coro (Preparo)"),
    "o-fim-de-toda-vida": (o_fim_de_toda_vida, "Ainz: The Goal of All Life Is Death"),
    "geass-lelouch": (geass_lelouch, "Lelouch: Geass"),
    "xadrez": (xadrez, "Lelouch: xadrez"),
    "lelouch-preparo": (lelouch_preparo, "Lelouch: o rei e o Geass (Preparo)"),
    "xeque-mate": (xeque_mate, "Lelouch: xeque-mate"),
}
