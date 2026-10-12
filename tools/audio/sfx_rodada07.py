"""Os sons da rodada 7: Rukia, Aizen, Kenpachi, Eren e Mikasa (veja tools/vfx/familias_v2/rodada07.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _lamina(rng, seg=0.3, f0=2600, g=0.6):
    n = n_de(seg)
    x = passa(rosa(rng, n), 2000, 11000, 2) * sobe_e_some(n, 0.2, 1.6) * 0.6
    x += modal(n, f0, rng=rng, **METAL) * env(n, 0.001, seg * 0.7) * 0.12
    return x * g


def _gelo_estala(rng, g=0.5, f0=3200):
    """O gelo estalando: os cliques cristalinos e o tilintar."""
    n = n_de(0.4)
    y = graos(rng, n, 18, 0.0, 0.25, 3000, 10000, 0.004, 0.6) * 0.6
    y += modal(n, f0, rng=rng, **CRISTAL) * env(n, 0.001, 0.3) * 0.12
    return y * g


def _vapor(rng, seg, g=0.3):
    n = n_de(seg)
    return passa(rosa(rng, n), 1500, 9000, 2) * sobe_e_some(n, 0.15, 1.4) * g


# =================================================================== Rukia
def sode_no_shirayuki(rng, v):
    """A espada branca: a fita correndo no ar (o assobio fino que gira), os flocos tilintando e a geada
    que estala no golpe."""
    x = _z(1.5)
    n = n_de(0.5)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2500, 9000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 9 * t)) * sobe_e_some(n, 0.5, 1.4) * 0.35, 0.0)
    for k in range(6):
        poe(x, _brilho(rng, 0.3, 3000 + 420 * k, 0.05, CRISTAL), 0.08 + 0.06 * k)
    poe(x, _gelo_estala(rng, 0.8), 0.42)
    poe(x, B.gelo(rng, v)[: n_de(0.6)] * 0.4, 0.42)
    return reverb(x, 0.5, 0.3)


def circulo_de_gelo(rng, v):
    """A Primeira Dança: o círculo se desenhando no chão (o tom frio que gira), o silêncio, e a coluna de
    gelo que sobe de uma vez (o estalo grande, o ronco e os cristais caindo)."""
    x = _z(1.8)
    n = n_de(0.45)
    poe(x, seno(varre(900, 1500, n, 1.0), n) * sobe_e_some(n, 0.8, 1.2) * 0.05 + passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.8, 1.2) * 0.12, 0.0)
    poe(x, estalo(rng, n_de(0.04), 1500, 8000) * 0.9, 0.5)
    poe(x, baque(n_de(0.5), 90, 45, 0.2, 0.5) * 0.6, 0.5)
    poe(x, B.gelo(rng, v)[: n_de(0.8)] * 0.6, 0.5)
    poe(x, graos(rng, n_de(0.8), 26, 0.1, 0.7, 3500, 10000, 0.004, 0.6) * 0.3, 0.75)
    return reverb(x, 0.6, 0.3)


def hakka_preparo(rng, v):
    """O Preparo do Bankai da Rukia: o vento gelado girando e o chiado da geada crescendo."""
    x = _z(1.3)
    n = n_de(1.2)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1200, 6000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 2.5 * t)) * sobe_e_some(n, 0.7, 1.1) * 0.35, 0.0)
    poe(x, seno(varre(1200, 1800, n, 1.0), n) * sobe_e_some(n, 0.7, 1.1) * 0.03, 0.0)
    return reverb(x, 0.6, 0.35)


def hakka_no_togame(rng, v):
    """A Hakka no Togame: os cristais crescendo (os estalos se juntando, cada vez mais rápidos), o gelo
    fechando (o "crrrk" grave), o silêncio frio, e a flor trincando e caindo em pó."""
    x = _z(2.1)
    for k in range(10):
        poe(x, _gelo_estala(rng, 0.25 + 0.04 * k, 2600 + 150 * k), 0.02 + 0.08 * k * (1 - 0.04 * k))
    n = n_de(0.4)
    poe(x, satura(passa(rosa(rng, n), 100, 900, 2), 2) * env(n, 0.01, 0.3) * 0.5, 0.75)
    poe(x, modal(n_de(1.0), 1800, rng=rng, **VIDRO) * env(n_de(1.0), 0.001, 0.7) * 0.15, 0.8)
    poe(x, estalo(rng, n_de(0.04), 2000, 9000) * 0.8, 1.45)
    poe(x, graos(rng, n_de(0.6), 40, 0.0, 0.5, 2500, 10000, 0.005, 0.6) * 0.4, 1.47)
    return reverb(x, 0.65, 0.35)


# =================================================================== Aizen
def kyoka_suigetsu(rng, v):
    """A ilusão: o tom puro e calmo da lua, a gota caindo na água (o "plic" e as ondas), e o mundo
    entortando (o tom que desafina devagar), sereno e errado ao mesmo tempo."""
    x = _z(2.0)
    n = n_de(1.6)
    t = _t(n)
    tom = (seno(523.25, n) + seno(659.25 * (1 - 0.03 * t), n) * 0.6 + seno(784 * (1 + 0.02 * t), n) * 0.4) * sobe_e_some(n, 0.3, 1.3) * 0.06
    poe(x, tom, 0.0)
    m = n_de(0.25)
    poe(x, seno(varre(1800, 600, m, 2.0), m) * env(m, 0.001, 0.15) * 0.2, 0.25)
    for k in range(3):
        k_ = n_de(0.3)
        poe(x, passa(rosa(rng, k_), 300, 1500, 2) * env(k_, 0.01, 0.25) * 0.1, 0.3 + 0.18 * k)
    poe(x, _brilho(rng, 1.0, 1046, 0.05, SINO), 1.1)
    return reverb(x, 0.75, 0.45)


def plano_revelado(rng, v):
    """O plano revelado: o vidro trincando (os estalos correndo), o vidro estourando e caindo em
    pedaços, e a estocada por trás (o "shk" curto e certeiro)."""
    x = _z(1.6)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.02), 2500, 9000) * 0.4, 0.1 + 0.05 * k)
    poe(x, modal(n_de(0.7), 2600, rng=rng, **VIDRO) * env(n_de(0.7), 0.001, 0.4) * 0.25, 0.48)
    poe(x, graos(rng, n_de(0.8), 44, 0.0, 0.7, 2500, 9500, 0.006, 0.6) * 0.45, 0.5)
    poe(x, _lamina(rng, 0.25, 3200, 0.9), 0.78)
    poe(x, baque(n_de(0.3), 120, 60, 0.08, 0.5) * 0.4, 0.82)
    return reverb(x, 0.5, 0.25)


# =================================================================== Kenpachi
def _riso(rng, seg=0.7, g=0.2):
    """O riso de batalha: rajadas curtas e graves, ásperas (ha-ha-ha)."""
    x = np.zeros(n_de(seg))
    for k in range(4):
        n = n_de(0.1)
        voz = satura(passa(rosa(rng, n), 150, 1200, 2) + seno(varre(180, 140, n, 1.0), n) * 0.5, 2.5) * env(n, 0.008, 0.08)
        poe(x, voz * g, 0.02 + 0.14 * k)
    return x


def instinto_de_batalha(rng, v):
    """O Instinto de batalha: a espada lascada descendo pesada (o ar grave), o golpe (metal + baque) e
    a pressão espiritual que ri (o riso grave e áspero por baixo)."""
    x = _z(1.6)
    poe(x, _whoosh(rng, 0.3, 200, 900, 0.8, 1.6, 0.6), 0.0)
    poe(x, baque(n_de(0.5), 85, 38, 0.2, 0.6) * 0.9, 0.25)
    poe(x, modal(n_de(0.5), 900, rng=rng, **METAL) * env(n_de(0.5), 0.001, 0.25) * 0.15, 0.25)
    poe(x, _riso(rng, 0.7, 0.25), 0.45)
    return reverb(x, 0.5, 0.25)


def corte_selvagem(rng, v):
    """O Corte selvagem: três cortes brutos — o aço lascado arranhando (ruído áspero e serrilhado, não o
    "shing" limpo) — e o sangue espirrando."""
    x = _z(1.4)
    for k in range(3):
        n = n_de(0.22)
        t = _t(n)
        serra = satura(passa(rosa(rng, n), 800, 6000, 2) * (0.5 + 0.5 * np.sign(np.sin(2 * math.pi * 55 * t))), 2) * sobe_e_some(n, 0.25, 1.5) * 0.5
        poe(x, serra, 0.02 + 0.17 * k)
        poe(x, baque(n_de(0.2), 130, 70, 0.06, 0.4) * 0.35, 0.1 + 0.17 * k)
        poe(x, passa(rosa(rng, n_de(0.15)), 300, 2500, 2) * env(n_de(0.15), 0.002, 0.1) * 0.25, 0.12 + 0.17 * k)
    return reverb(x, 0.45, 0.2)


def limitador_preparo(rng, v):
    """O tapa-olho sai: o rugido da pressão subindo (o vento grave que cresce e treme)."""
    x = _z(1.3)
    n = n_de(1.2)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 50, 700, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 14 * t)), 2) * sobe_e_some(n, 0.8, 1.1) * 0.45, 0.0)
    return reverb(x, 0.5, 0.3)


def retirar_o_limitador(rng, v):
    """Retirar o limitador: a pressão explode (o estrondo que sobe), o riso, e o corte com as duas
    mãos — o ar rasgado enorme, o impacto que racha o chão e o ronco da terra."""
    x = _z(2.0)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 60, 2000, 2) * (np.linspace(0, 1, n) ** 2) * 0.6, 0.0)
    poe(x, _riso(rng, 0.7, 0.2), 0.15)
    poe(x, _whoosh(rng, 0.35, 150, 1200, 0.85, 1.6, 0.8), 0.5)
    poe(x, baque(n_de(0.9), 60, 26, 0.45, 0.7) * 1.0, 0.82)
    poe(x, B.terremoto(rng, v)[: n_de(0.9)] * 0.5, 0.85)
    return reverb(x, 0.55, 0.3)


# =================================================================== Eren
def endurecimento_titan(rng, v):
    """O endurecimento: as placas de cristal se encaixando (os "tlinc" cristalinos, cada vez mais
    juntos), o cristal fechando (o tom de vidro) e o brilho passando."""
    x = _z(1.6)
    sub = np.random.default_rng(3)
    for k in range(14):
        em = 0.02 + 0.6 * (k / 14) ** 0.8
        poe(x, _brilho(rng, 0.25, sub.uniform(1800, 3600), 0.05, CRISTAL), em)
        poe(x, estalo(rng, n_de(0.01), 2000, 7000) * 0.15, em)
    poe(x, modal(n_de(1.0), 1320, rng=rng, **VIDRO) * env(n_de(1.0), 0.01, 0.6) * 0.15, 0.7)
    poe(x, seno(varre(1500, 3000, n_de(0.3), 1.0), n_de(0.3)) * sobe_e_some(n_de(0.3), 0.5, 1.3) * 0.03, 0.9)
    return reverb(x, 0.55, 0.3)


def fundacao_preparo(rng, v):
    """O Preparo do Rugido: o trovão da transformação (o raio amarelo) e o vapor chiando em volta."""
    x = _z(1.4)
    poe(x, B.raio(rng, v)[: n_de(0.7)] * 0.6, 0.0)
    poe(x, baque(n_de(0.6), 50, 28, 0.35, 0.3) * 0.6, 0.05)
    poe(x, _vapor(rng, 1.0, 0.25), 0.2)
    return reverb(x, 0.6, 0.35)


def rugido_da_fundacao(rng, v):
    """O Rugido: os passos dos colossais (baques enormes e graves, um depois do outro, cada vez mais
    perto), o chão tremendo o tempo todo, o vapor e o choque final."""
    x = _z(2.4)
    n = n_de(2.0)
    poe(x, passa(rosa(rng, n), 25, 160, 2) * sobe_e_some(n, 0.5, 1.2) * 0.45, 0.0)
    for k in range(6):
        g = 0.55 + 0.08 * k
        poe(x, baque(n_de(0.7), 48, 24, 0.4, 0.5) * g, 0.05 + 0.18 * k)
        poe(x, passa(rosa(rng, n_de(0.3)), 80, 900, 2) * env(n_de(0.3), 0.003, 0.25) * 0.3 * g, 0.06 + 0.18 * k)
    poe(x, _vapor(rng, 1.0, 0.18), 0.6)
    poe(x, B.terremoto(rng, v)[: n_de(1.0)] * 0.6, 1.25)
    poe(x, B.explosao(rng, v)[: n_de(0.8)] * 0.5, 1.3)
    return reverb(x, 0.6, 0.3)


# =================================================================== Mikasa
def manobra_odm(rng, v):
    """O equipamento de manobra: os dois disparos dos cabos (o "ptchk" do gancho e o fio zunindo), o
    jato de gás chiando e o corte giratório."""
    x = _z(1.5)
    for k in range(2):
        poe(x, estalo(rng, n_de(0.02), 1200, 6000) * 0.6, 0.0 + 0.05 * k)
        m = n_de(0.2)
        poe(x, seno(varre(2400, 900, m, 1.0), m) * env(m, 0.002, 0.15) * 0.08, 0.0 + 0.05 * k)
        poe(x, modal(n_de(0.2), 2200, rng=rng, **METAL) * env(n_de(0.2), 0.001, 0.1) * 0.15, 0.18 + 0.05 * k)
    n = n_de(0.55)
    poe(x, passa(rosa(rng, n), 1500, 9000, 2) * sobe_e_some(n, 0.15, 1.2) * 0.5, 0.22)
    poe(x, _lamina(rng, 0.25, 2800, 0.6), 0.7)
    poe(x, _lamina(rng, 0.25, 3000, 0.5), 0.8)
    return reverb(x, 0.45, 0.22)


def laminas_em_x(rng, v):
    """As lâminas em X: dois cortes rápidos cruzados, o "tlénc" das pontas quebrando (o metal fino) e
    o pano do cachecol batendo."""
    x = _z(1.4)
    poe(x, _lamina(rng, 0.22, 2900, 0.8), 0.04)
    poe(x, _lamina(rng, 0.22, 3300, 0.8), 0.14)
    for k in range(2):
        poe(x, modal(n_de(0.4), 3800 + 300 * k, rng=rng, **METAL) * env(n_de(0.4), 0.001, 0.25) * 0.2, 0.3 + 0.06 * k)
    n = n_de(0.5)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 2000, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 7 * t))) * sobe_e_some(n, 0.4, 1.4) * 0.2, 0.35)
    return reverb(x, 0.45, 0.22)


def golpe_na_nuca(rng, v):
    """O golpe decisivo: o vento da queda girando (o assobio que desce), o corte fundo e certeiro (o
    "shk" pesado e o tinido) e o vapor quente chiando para fora."""
    x = _z(1.6)
    n = n_de(0.45)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 12 * t)) * (np.linspace(0, 1, n) ** 1.5) * 0.45, 0.0)
    poe(x, _lamina(rng, 0.35, 2600, 1.0), 0.42)
    poe(x, baque(n_de(0.3), 110, 55, 0.08, 0.5) * 0.5, 0.44)
    poe(x, _vapor(rng, 0.8, 0.35), 0.5)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "sode-no-shirayuki": (sode_no_shirayuki, "Rukia: a fita branca, os flocos e a geada"),
    "circulo-de-gelo": (circulo_de_gelo, "Rukia: o círculo e a coluna de gelo"),
    "hakka-preparo": (hakka_preparo, "Rukia: o vento gelado do Bankai (antes do golpe)"),
    "hakka-no-togame": (hakka_no_togame, "Rukia: a flor de gelo que fecha e trinca"),
    "kyoka-suigetsu": (kyoka_suigetsu, "Aizen: a lua, a gota na água e a ilusão"),
    "plano-revelado": (plano_revelado, "Aizen: o vidro que estoura e a estocada"),
    "instinto-de-batalha": (instinto_de_batalha, "Kenpachi: o golpe e o riso de batalha"),
    "corte-selvagem": (corte_selvagem, "Kenpachi: três cortes de lâmina lascada"),
    "limitador-preparo": (limitador_preparo, "Kenpachi: a pressão subindo (antes do golpe)"),
    "retirar-o-limitador": (retirar_o_limitador, "Kenpachi: a pressão explode e o corte com as duas mãos"),
    "endurecimento-titan": (endurecimento_titan, "Eren: as placas de cristal se encaixando"),
    "fundacao-preparo": (fundacao_preparo, "Eren: o raio da transformação e o vapor (antes do golpe)"),
    "rugido-da-fundacao": (rugido_da_fundacao, "Eren: os passos dos colossais e o choque"),
    "manobra-odm": (manobra_odm, "Mikasa: os cabos, o gás e o corte giratório"),
    "laminas-em-x": (laminas_em_x, "Mikasa: as lâminas em X que quebram"),
    "golpe-na-nuca": (golpe_na_nuca, "Mikasa: a queda e o corte na nuca"),
}
