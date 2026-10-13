"""Os sons da rodada 58 das habilidades próprias (veja tools/vfx/familias_v2/rodada58.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _fogo(rng, seg, g=0.3, f0=200, f1=3000):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), f0, f1, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 11 * t)) * sobe_e_some(n, 0.2, 1.2) * g


def _rasgo(rng, g=0.4):
    """O rasgo de garra: o chiado curto e áspero."""
    n = n_de(0.12)
    return satura(passa(rosa(rng, n), 1500, 9000, 2), 2) * env(n, 0.002, 0.08) * g


def _lamina_tine(rng, f=1800, g=0.035):
    return _sino(rng, f, 0.6, g, METAL)


def _bolhas(rng, seg, g=0.02):
    x = _z(seg + 0.1)
    q = np.random.default_rng(58)
    for k in range(int(seg * 14)):
        poe(x, _piu(q.uniform(300, 700), q.uniform(900, 1600), 0.04, g), q.uniform(0, seg))
    return x


def _chicote(rng, g=0.5):
    n = n_de(0.08)
    return (estalo(rng, n, 2000, 9000, 0.01) * 1.2 + seno(varre(3000, 800, n), n) * env(n, 0.001, 0.05) * 0.1) * g


# ------------------------------------------------------------------ Inuyasha

def garras_de_aco_inuyasha(rng, v):
    """Inuyasha: "SANKON TESSŌ!" — as garras rasgando em X duas vezes."""
    x = _z(2.0)
    for k in range(2):
        poe(x, _whoosh(rng, 0.15, 1000, 6000, 0.7, 1.3, 0.4), 0.06 + 0.16 * k)
        for j in range(5):
            poe(x, _rasgo(rng, 0.25), 0.14 + 0.16 * k + 0.012 * j)
    poe(x, _baque(110, 55, 0.25, 0.5), 0.3)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 300, 2000, 2) * env(n, 0.01, 0.2) * 0.12, 0.4)
    return reverb(x, 0.6, 0.3)


def tessaiga(rng, v):
    """Inuyasha: a espada velha pulsando e virando a Tessaiga gigante ("VUUM") e o corte."""
    x = _z(2.2)
    for k in range(2):
        poe(x, _baque(80, 50, 0.15, 0.4), 0.05 + 0.1 * k)
    n = n_de(0.3)
    poe(x, seno(varre(120, 300, n), n) * env(n, 0.1, 0.15) * 0.04, 0.1)
    poe(x, _whoosh(rng, 0.3, 300, 4000, 0.8, 1.3, 0.6), 0.25)
    poe(x, _baque(70, 30, 0.5, 0.8, 2.6), 0.4)
    poe(x, _lamina_tine(rng, 1175, 0.03), 0.4)
    return reverb(x, 0.7, 0.35)


def inuyasha_preparo(rng, v):
    """Inuyasha (Preparo): a Tessaiga erguida e o vento girando na lâmina (em laço)."""
    x = _z(1.4)
    n = n_de(1.2)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.2, 0.0)
    poe(x, _lamina_tine(rng, 880, 0.015), 0.3)
    return reverb(x, 0.7, 0.35)


def ferida_do_vento(rng, v):
    """Inuyasha: "KAZE NO KIZU!" — o corte da Tessaiga e as cinco garras de vento rasgando o chão."""
    x = _z(2.7)
    poe(x, _whoosh(rng, 0.3, 200, 3000, 0.8, 1.3, 0.6), 0.1)
    poe(x, _baque(55, 25, 0.6, 0.8, 2.8), 0.3)
    for k in range(5):
        poe(x, _whoosh(rng, 0.5, 300, 5000, 0.4, 1.3, 0.35), 0.32 + 0.03 * k)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 60, 1200, 2) * sobe_e_some(n, 0.3, 1.2) * 0.4, 0.4)
    poe(x, _explosao(rng, 0.5, 45), 0.6)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Sesshomaru

def garras_venenosas(rng, v):
    """Sesshomaru: a garra pingando veneno ("tss") e o rasgo."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * env(n, 0.05, 0.2) * 0.1, 0.0)
    poe(x, _whoosh(rng, 0.2, 800, 5000, 0.7, 1.3, 0.4), 0.15)
    for j in range(4):
        poe(x, _rasgo(rng, 0.25), 0.32 + 0.012 * j)
    poe(x, _bolhas(rng, 0.6, 0.015), 0.5)
    return reverb(x, 0.6, 0.3)


def chicote_de_luz_sesshomaru(rng, v):
    """Sesshomaru: o chicote de luz zumbindo, estalando e apertando o rival."""
    x = _z(2.0)
    n = n_de(0.4)
    poe(x, (seno(varre(600, 1400, n), n) + seno(varre(900, 2100, n), n) * 0.5) * env(n, 0.05, 0.3) * 0.02, 0.05)
    poe(x, _chicote(rng, 0.5), 0.32)
    for k in range(3):
        n = n_de(0.1)
        poe(x, seno(varre(400, 250, n), n) * env(n, 0.01, 0.08) * 0.03, 0.42 + 0.08 * k)
    return reverb(x, 0.7, 0.35)


def sesshomaru_preparo(rng, v):
    """Sesshomaru (Preparo): a Bakusaiga pulsando com o brilho verde (em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, (seno(330, n) + seno(495, n) * 0.4) * (0.6 + 0.4 * np.sin(2 * math.pi * 2 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.014, 0.0)
    poe(x, _bolhas(rng, 1.0, 0.008), 0.1)
    return reverb(x, 0.8, 0.4)


def bakusaiga(rng, v):
    """Sesshomaru: o corte da Bakusaiga e a carne se desfazendo (o chiado do veneno se espalhando)."""
    x = _z(2.5)
    poe(x, _whoosh(rng, 0.25, 800, 7000, 0.8, 1.3, 0.55), 0.1)
    poe(x, _lamina_tine(rng, 1568, 0.035), 0.27)
    poe(x, _baque(80, 35, 0.4, 0.7, 2.4), 0.27)
    n = n_de(1.0)
    poe(x, satura(passa(rosa(rng, n), 1500, 8000, 2), 2) * sobe_e_some(n, 0.2, 1.3) * 0.25, 0.42)
    poe(x, _bolhas(rng, 0.8, 0.02), 0.45)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Kenshin

def postura_kenshin(rng, v):
    """Kenshin: o polegar soltando a guarda ("tchk") e a respiração firme."""
    x = _z(1.9)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.005) * 0.6, 0.05)
    poe(x, _sopro(rng, 0.6, 300, 2000, 0.15, 0.4), 0.15)
    poe(x, _sino(rng, 523, 0.7, 0.02, METAL), 0.3)
    return reverb(x, 0.7, 0.35)


def batoujutsu(rng, v):
    """Kenshin: o silêncio, o saque mais rápido que o olho ("SHING!") e o choque."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.02), 1500, 6000, 0.004) * 0.5, 0.05)
    poe(x, _whoosh(rng, 0.1, 2000, 10000, 0.6, 1.3, 0.6), 0.18)
    poe(x, _lamina_tine(rng, 2093, 0.045), 0.25)
    poe(x, _baque(100, 50, 0.3, 0.6), 0.28)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 3000, 9000, 0.005) * 0.25, 0.45 + 0.08 * k)
    return reverb(x, 0.6, 0.3)


def kenshin_preparo(rng, v):
    """Kenshin (Preparo): o pé esquerdo deslizando à frente e a lâmina vibrando na bainha (em laço)."""
    x = _z(1.4)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 500, 3000, 2) * env(n, 0.05, 0.2) * 0.08, 0.05)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(1760, n) * (0.5 + 0.5 * np.sin(2 * math.pi * 8 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.006, 0.2)
    return reverb(x, 0.6, 0.3)


def amakakeru(rng, v):
    """Kenshin: "AMAKAKERU RYŪ NO HIRAMEKI!" — o passo, o corte e o vácuo puxando o ar."""
    x = _z(2.4)
    poe(x, _whoosh(rng, 0.25, 200, 6000, 0.9, 1.3, 0.6), 0.05)
    poe(x, _lamina_tine(rng, 1760, 0.045), 0.3)
    poe(x, _baque(60, 25, 0.6, 0.9, 2.8), 0.3)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 100, 2500, 2) * env(n, 0.3, 0.1) * 0.35, 0.45)
    poe(x, _baque(80, 40, 0.3, 0.5), 1.0)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Natsu

def punho_do_dragao_de_fogo(rng, v):
    """Natsu: o punho pegando fogo ("FUUSH") e o soco em chamas."""
    x = _z(2.0)
    poe(x, _fogo(rng, 0.4, 0.3), 0.0)
    poe(x, _whoosh(rng, 0.2, 200, 2500, 0.8, 1.3, 0.5), 0.1)
    poe(x, _baque(60, 25, 0.5, 0.9, 2.8), 0.28)
    poe(x, _explosao(rng, 0.35, 70), 0.28)
    poe(x, _fogo(rng, 0.6, 0.15), 0.4)
    return reverb(x, 0.7, 0.35)


def rugido_do_dragao_natsu(rng, v):
    """Natsu: o fôlego puxado e o rugido de fogo em todos ("GAAAH!")."""
    x = _z(2.5)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 500, 4000, 2) * env(n, 0.2, 0.05) * 0.15, 0.0)
    n = n_de(0.9)
    t = _t(n)
    voz = satura(seno(varre(180, 120, n), n) * (1 + 0.3 * np.sin(2 * math.pi * 30 * t)) + passa(rosa(rng, n), 200, 3000, 2) * 0.8, 4)
    poe(x, voz * env(n, 0.03, 0.5) * 0.05, 0.12)
    poe(x, _fogo(rng, 1.0, 0.45, 150, 5000), 0.15)
    return reverb(x, 0.8, 0.4)


def natsu_preparo(rng, v):
    """Natsu (Preparo): as chamas girando nas duas mãos (em laço)."""
    x = _z(1.4)
    poe(x, _fogo(rng, 1.2, 0.18), 0.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.1, 0.1)
    return reverb(x, 0.6, 0.3)


def lotus_carmesim(rng, v):
    """Natsu: "LÓTUS CARMESIM: PUNHO EXPLOSIVO DO DRAGÃO DE FOGO!" — a lótus abrindo e a explosão."""
    x = _z(2.8)
    poe(x, _whoosh(rng, 0.25, 150, 2000, 0.85, 1.3, 0.6), 0.05)
    poe(x, _baque(45, 18, 0.8, 1.0, 3.2), 0.28)
    poe(x, _fogo(rng, 0.5, 0.35), 0.3)
    poe(x, _baque(32, 12, 1.4, 1.0, 3.8), 0.58)
    poe(x, _explosao(rng, 1.0, 35), 0.58)
    poe(x, _fogo(rng, 0.9, 0.25), 0.65)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Erza

def armadura_do_ceu(rng, v):
    """Erza: a troca de armadura (o brilho), as asas abrindo e a chuva de espadas."""
    x = _z(2.5)
    poe(x, _brilho(rng, 0.6, 1568, 0.04, CRISTAL), 0.0)
    poe(x, _whoosh(rng, 0.35, 400, 3000, 0.6, 1.3, 0.35), 0.1)
    q = np.random.default_rng(580)
    for k in range(12):
        tq = 0.45 + q.uniform(0, 0.4)
        poe(x, _lamina_tine(rng, q.uniform(1400, 2400), 0.012), tq)
        poe(x, _baque(200, 100, 0.08, 0.15), tq)
    return reverb(x, 0.8, 0.4)


def armadura_de_adamantina(rng, v):
    """Erza: os dois escudos de adamantina se juntando ("CLANG!") na frente do trio."""
    x = _z(2.1)
    poe(x, _brilho(rng, 0.5, 1319, 0.03, CRISTAL), 0.0)
    poe(x, _whoosh(rng, 0.3, 200, 1500, 0.8, 1.3, 0.4), 0.1)
    poe(x, _sino(rng, 196, 1.2, 0.07, METAL), 0.4)
    poe(x, _baque(70, 40, 0.4, 0.8, 2.4), 0.4)
    return reverb(x, 0.9, 0.45)


def erza_preparo(rng, v):
    """Erza (Preparo): o círculo de troca de armadura e as espadas girando (os tinidos em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    poe(x, _brilho(rng, 1.0, 988, 0.02, CRISTAL), 0.0)
    for k in range(5):
        poe(x, _lamina_tine(rng, 1568 + 100 * k, 0.01), 0.1 + 0.25 * k)
    poe(x, _whoosh(rng, 1.0, 400, 2000, 0.5, 1.3, 0.15), 0.1)
    return reverb(x, 0.8, 0.4)


def armadura_do_purgatorio(rng, v):
    """Erza: a armadura negra fechando e a clava de espinhos esmagando o rival."""
    x = _z(2.5)
    poe(x, _sino(rng, 110, 0.8, 0.05, METAL), 0.0)
    poe(x, _whoosh(rng, 0.35, 80, 1500, 0.9, 1.3, 0.6), 0.1)
    poe(x, _baque(32, 12, 1.4, 1.0, 3.6), 0.38)
    poe(x, _explosao(rng, 0.7, 40), 0.38)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.05), 150, 2500, 0.015) * 0.5, 0.42 + 0.05 * k)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Asta

def matadora_de_demonios(rng, v):
    """Asta: a espada negra cortando o círculo de magia (o vidro quebrando) e o silêncio da antimagia."""
    x = _z(2.2)
    poe(x, _whoosh(rng, 0.25, 150, 2500, 0.8, 1.3, 0.6), 0.15)
    poe(x, _baque(60, 25, 0.5, 0.9, 2.8), 0.38)
    for k in range(10):
        poe(x, estalo(rng, n_de(0.04), 3000, 11000, 0.008) * 0.25, 0.4 + 0.025 * k)
    n = n_de(0.5)
    poe(x, seno(varre(400, 80, n), n) * env(n, 0.01, 0.4) * 0.04, 0.42)
    return reverb(x, 0.7, 0.35)


def golpe_antimagia(rng, v):
    """Asta: o golpe antimagia e os selos do rival se partindo."""
    x = _z(2.1)
    poe(x, _whoosh(rng, 0.2, 150, 3000, 0.8, 1.3, 0.55), 0.1)
    poe(x, _baque(70, 30, 0.45, 0.8, 2.6), 0.28)
    for k in range(3):
        poe(x, _sino(rng, 1319 + 200 * k, 0.3, 0.02, CRISTAL), 0.5 + 0.04 * k)
        for j in range(3):
            poe(x, estalo(rng, n_de(0.03), 3000, 10000, 0.006) * 0.2, 0.52 + 0.04 * k + 0.01 * j)
    return reverb(x, 0.6, 0.3)


def asta_preparo(rng, v):
    """Asta (Preparo): o braço do demônio e a asa negra (o zumbido grave e os estalos em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, satura(seno(65, n) + seno(98, n) * 0.5, 3) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.035, 0.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.02), 1000, 5000, 0.004) * 0.25, 0.15 + 0.3 * k)
    return reverb(x, 0.7, 0.35)


def black_asta(rng, v):
    """Asta: "BLACK ASTA!" — a asa negra abrindo, o salto e os cortes em todos os rivais."""
    x = _z(2.7)
    n = n_de(0.4)
    poe(x, satura(seno(varre(60, 110, n), n), 3) * env(n, 0.1, 0.25) * 0.05, 0.0)
    poe(x, _whoosh(rng, 0.3, 300, 2500, 0.7, 1.3, 0.4), 0.1)
    for k in range(3):
        poe(x, _whoosh(rng, 0.2, 200, 4000, 0.8, 1.3, 0.45), 0.32 + 0.04 * k)
        poe(x, _baque(70, 30, 0.35, 0.7, 2.6), 0.4 + 0.04 * k)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.04), 3000, 11000, 0.008) * 0.2, 0.55 + 0.03 * k)
    return reverb(x, 0.9, 0.45)


SONS: dict = {
    "garras-de-aco-inuyasha": (garras_de_aco_inuyasha, "Inuyasha: garras de aço"),
    "tessaiga": (tessaiga, "Inuyasha: Tessaiga"),
    "inuyasha-preparo": (inuyasha_preparo, "Inuyasha: a Tessaiga erguida (Preparo)"),
    "ferida-do-vento": (ferida_do_vento, "Inuyasha: Ferida do Vento"),
    "garras-venenosas": (garras_venenosas, "Sesshomaru: garras venenosas"),
    "chicote-de-luz-sesshomaru": (chicote_de_luz_sesshomaru, "Sesshomaru: chicote de luz"),
    "sesshomaru-preparo": (sesshomaru_preparo, "Sesshomaru: a Bakusaiga pulsando (Preparo)"),
    "bakusaiga": (bakusaiga, "Sesshomaru: Bakusaiga"),
    "postura-kenshin": (postura_kenshin, "Kenshin: postura"),
    "batoujutsu": (batoujutsu, "Kenshin: Batoujutsu"),
    "kenshin-preparo": (kenshin_preparo, "Kenshin: a lâmina na bainha (Preparo)"),
    "amakakeru": (amakakeru, "Kenshin: Amakakeru"),
    "punho-do-dragao-de-fogo": (punho_do_dragao_de_fogo, "Natsu: punho do dragão de fogo"),
    "rugido-do-dragao-natsu": (rugido_do_dragao_natsu, "Natsu: rugido do dragão"),
    "natsu-preparo": (natsu_preparo, "Natsu: as chamas nas mãos (Preparo)"),
    "lotus-carmesim": (lotus_carmesim, "Natsu: lótus carmesim"),
    "armadura-do-ceu": (armadura_do_ceu, "Erza: armadura do céu"),
    "armadura-de-adamantina": (armadura_de_adamantina, "Erza: armadura de adamantina"),
    "erza-preparo": (erza_preparo, "Erza: as espadas girando (Preparo)"),
    "armadura-do-purgatorio": (armadura_do_purgatorio, "Erza: armadura do purgatório"),
    "matadora-de-demonios": (matadora_de_demonios, "Asta: matadora de demônios"),
    "golpe-antimagia": (golpe_antimagia, "Asta: golpe antimagia"),
    "asta-preparo": (asta_preparo, "Asta: o braço do demônio (Preparo)"),
    "black-asta": (black_asta, "Asta: Black Asta"),
}
