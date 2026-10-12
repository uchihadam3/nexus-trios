"""Sons dos ataques básicos, lote n (veja tools/vfx/familias_v2/basicos_n.py).

Os bastões elétricos estalando, o clique da lanterna e o "tonc", o gancho disparando na corda, a centelha
arcana, o soco pesado do Nêmesis com o grunhido, o trovão de Zeus, os três jatos do tridente, o escudo de
bronze, a lança com o grito de guerra, o raio de sol, o arco e a flecha de prata, o bater de asinhas de
Hermes, o beijo e os corações, o sibilo e a pedra estalando da Medusa, e o tique-taque que anda para trás.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_k import _acerto, _mola, _splash
from sfx_basicos_l import _estrelinhas
from sfx_basicos_m import _zap
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def bastoes_eletricos(rng, v):
    """Os bastões do Asa Noturna: dois golpes alternados, cada um com o "bzzt" da carga elétrica."""
    x = _z(1.0)
    for t0 in (0.18, 0.36):
        poe(x, _whoosh(rng, 0.12, 1000, 4000, 0.8, 1.2, 0.3), t0 - 0.1)
        poe(x, _acerto(rng, 0.6, 140), t0)
        poe(x, _zap(rng, 0.2, 0.25), t0)
    return reverb(x, 0.3, 0.15)


def lanternada(rng, v):
    """A lanternada do Dipper: o clique da lanterna ligando, o zumbidinho da luz e o "tonc" de plástico na cabeça."""
    x = _z(1.1)
    poe(x, estalo(rng, n_de(0.03), 2000, 7000, 0.003) * 0.6, 0.0)
    n = n_de(0.3)
    poe(x, seno(4000, n) * sobe_e_some(n, 0.3, 1.3) * 0.01, 0.02)
    poe(x, _whoosh(rng, 0.2, 600, 2000, 0.8, 1.3, 0.3), 0.18)
    poe(x, modal(n_de(0.12), 900, rng=rng, razoes=[1.0, 2.7, 4.6], quedas=[0.04, 0.03, 0.02], ganhos=[1, 0.4, 0.2]) * 0.4, 0.35)
    poe(x, _acerto(rng, 0.5, 150), 0.35)
    _estrelinhas(rng, 0.42, x)
    return reverb(x, 0.35, 0.18)


def gancho_de_mabel(rng, v):
    """O gancho da Mabel: o "pchoom" do disparo, a corda zunindo, o "clank" da garra enganchando, o puxão e o
    plim do glitter."""
    x = _z(1.1)
    poe(x, passa(rosa(rng, n_de(0.1)), 300, 3000, 2) * env(n_de(0.1), 0.001, 0.05) * 0.5, 0.0)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * sobe_e_some(n, 0.4, 1.2) * 0.2, 0.02)
    poe(x, modal(n_de(0.15), 1800, rng=rng, **METAL) * env(n_de(0.15), 0.0005, 0.05) * 0.35, 0.25)
    poe(x, _acerto(rng, 0.4, 150), 0.25)
    poe(x, _whoosh(rng, 0.2, 2000, 700, 0.6, 1.2, 0.3), 0.36)
    for k, f in enumerate((2637, 3136, 3520, 4186)):
        poe(x, _brilho(rng, 0.2, f, 0.04, SINO), 0.4 + 0.04 * k)
    return reverb(x, 0.35, 0.18)


def faisca_arcana(rng, v):
    """A faísca arcana: a centelha girando (o tom que treme e sobe) e o estalo de magia no rival."""
    x = _z(1.0)
    n = n_de(0.35)
    t = _t(n)
    poe(x, seno(varre(600, 1400, n, 1.0) * (1 + 0.05 * np.sin(2 * math.pi * 30 * t)), n) * sobe_e_some(n, 0.7, 1.3) * 0.07, 0.0)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.7, 1.3) * 0.12, 0.0)
    poe(x, _brilho(rng, 0.5, 1200, 0.12, CRISTAL), 0.35)
    poe(x, _acerto(rng, 0.45, 150), 0.35)
    return reverb(x, 0.45, 0.22)


def soco_do_nemesis(rng, v):
    """O soco do Nêmesis: o grunhido grave ("STARS..."), os tentáculos se mexendo molhados e o soco esmagador."""
    x = _z(1.2)
    n = n_de(0.35)
    t = _t(n)
    poe(x, passa(satura(np.sin(2 * math.pi * np.cumsum(75 + 8 * np.sin(2 * math.pi * 6 * t)) / SR), 3), 60, 1200, 2) * sobe_e_some(n, 0.4, 1.3) * 0.15, 0.0)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 9 * t))) * sobe_e_some(n, 0.5, 1.3) * 0.2, 0.05)
    poe(x, _whoosh(rng, 0.3, 200, 1200, 0.85, 1.3, 0.5), 0.05)
    poe(x, baque(n_de(0.5), 70, 32, 0.18, 1.0) * 0.9, 0.3)
    poe(x, _acerto(rng, 1.0, 90), 0.3)
    return reverb(x, 0.45, 0.2)


def faisca_de_zeus(rng, v):
    """A faísca de Zeus: o raio rasgando o ar no arremesso, o "CRACK" do trovão e o ronco que rola."""
    x = _z(1.2)
    poe(x, _zap(rng, 0.25, 0.2), 0.0)
    poe(x, estalo(rng, n_de(0.06), 1200, 10000, 0.015) * 1.1, 0.25)
    m = n_de(0.7)
    poe(x, passa(rosa(rng, m), 40, 500, 2) * env(m, 0.01, 0.4) * 0.5, 0.27)
    poe(x, _acerto(rng, 0.6, 120), 0.25)
    poe(x, _zap(rng, 0.4, 0.2), 0.3)
    return reverb(x, 0.55, 0.25)


def jato_do_tridente(rng, v):
    """O jato do tridente: a água saindo das três pontas (o chiado forte e o borbulhar) e o splash no rival."""
    x = _z(1.1)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 500, 6000, 2) * sobe_e_some(n, 0.3, 1.3) * 0.4, 0.08)
    for k in range(6):
        m = n_de(0.05)
        poe(x, seno(varre(500 + 80 * k, 300, m, 1.0), m) * env(m, 0.002, 0.04) * 0.05, 0.1 + 0.04 * k)
    poe(x, _splash(rng, 0.35, 0.5), 0.3)
    poe(x, _acerto(rng, 0.45, 130), 0.3)
    return reverb(x, 0.4, 0.2)


def escudada_de_atena(rng, v):
    """A escudada de Atena: o escudo de bronze avançando e o "BONG" metálico grave da batida."""
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.25, 300, 1200, 0.85, 1.3, 0.4), 0.02)
    poe(x, modal(n_de(0.8), 220, rng=rng, **SINO) * env(n_de(0.8), 0.001, 0.4) * 0.35, 0.28)
    poe(x, _acerto(rng, 0.8, 100), 0.28)
    return reverb(x, 0.45, 0.22)


def lanca_de_ares(rng, v):
    """A lança de Ares: o grito de guerra rouco, a fúria em chamas e a estocada metálica que crava."""
    x = _z(1.1)
    n = n_de(0.3)
    t = _t(n)
    poe(x, passa(satura(np.sin(2 * math.pi * np.cumsum(140 + 30 * t) / SR), 3) * (0.6 + 0.4 * np.abs(np.sin(2 * math.pi * 30 * t))), 100, 2500, 2) * sobe_e_some(n, 0.3, 1.3) * 0.08, 0.0)
    poe(x, passa(rosa(rng, n), 200, 3000, 2) * sobe_e_some(n, 0.6, 1.3) * 0.25, 0.05)
    poe(x, _whoosh(rng, 0.2, 600, 3500, 0.85, 1.2, 0.45), 0.1)
    poe(x, B._lamina_curta(rng, n_de(0.25), 2200) * env(n_de(0.25), 0.001, 0.08) * 0.2, 0.28)
    poe(x, _acerto(rng, 0.9, 120), 0.28)
    return reverb(x, 0.4, 0.2)


def raio_de_apolo(rng, v):
    """O raio de Apolo: o sol acendendo (o acorde dourado e brilhante), o feixe quente e o clarão."""
    x = _z(1.2)
    n = n_de(0.5)
    for f in (523, 659, 784):
        poe(x, seno(f, n) * sobe_e_some(n, 0.3, 1.3) * 0.04, 0.0)
    m = n_de(0.35)
    poe(x, passa(rosa(rng, m), 1500, 8000, 2) * sobe_e_some(m, 0.2, 1.3) * 0.25, 0.15)
    poe(x, _brilho(rng, 0.6, 1568, 0.12, CRISTAL), 0.28)
    poe(x, _acerto(rng, 0.5, 140), 0.28)
    return reverb(x, 0.5, 0.25)


def flecha_lunar(rng, v):
    """A flecha de Ártemis: a corda de prata (o "tuang" agudo e limpo), o assobio frio e o tinido da ponta de prata
    cravando."""
    x = _z(1.1)
    n = n_de(0.2)
    poe(x, seno(varre(330, 260, n, 1.0), n) * env(n, 0.001, 0.12) * 0.2 + estalo(rng, n, 1500, 5000, 0.004) * 0.3, 0.02)
    m = n_de(0.25)
    poe(x, seno(varre(3200, 2400, m, 1.0), m) * sobe_e_some(m, 0.6, 1.3) * 0.04 + passa(rosa(rng, m), 3000, 9000, 2) * sobe_e_some(m, 0.6, 1.3) * 0.12, 0.05)
    poe(x, _brilho(rng, 0.5, 2637, 0.1, VIDRO), 0.28)
    poe(x, _acerto(rng, 0.45, 160, 2000, 7000), 0.28)
    return reverb(x, 0.5, 0.25)


def chute_alado(rng, v):
    """O chute de Hermes: as asinhas batendo depressa (o "frrrr" de penas), o vento da velocidade e o chute."""
    x = _z(1.0)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * np.abs(np.sin(2 * math.pi * 30 * _t(n))) * sobe_e_some(n, 0.6, 1.2) * 0.3, 0.0)
    poe(x, _whoosh(rng, 0.2, 800, 5000, 0.9, 1.2, 0.45), 0.02)
    poe(x, _acerto(rng, 0.8, 130), 0.22)
    return reverb(x, 0.3, 0.15)


def beijo_soprado(rng, v):
    """O beijo soprado: o "smack" do beijo, o sopro suave, os coraçõezinhos (os "plim" doces) e o encanto."""
    x = _z(1.2)
    m = n_de(0.05)
    poe(x, passa(rosa(rng, m), 1500, 6000, 2) * env(m, 0.001, 0.02) * 0.5, 0.02)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 500, 3000, 2) * sobe_e_some(n, 0.3, 1.3) * 0.15, 0.06)
    for k, f in enumerate((1047, 1319, 1568, 1319)):
        poe(x, _brilho(rng, 0.3, f, 0.06, SINO), 0.12 + 0.07 * k)
    poe(x, _brilho(rng, 0.7, 2093, 0.08, CRISTAL), 0.45)
    return reverb(x, 0.55, 0.28)


def bote_da_medusa(rng, v):
    """O bote da Medusa: o sibilo da serpente, o bote (o "tchk" da mordida) e a pedra estalando e endurecendo."""
    x = _z(1.3)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 4000, 10000, 2) * sobe_e_some(n, 0.3, 1.3) * 0.35, 0.0)
    poe(x, _acerto(rng, 0.5, 160, 1500, 6000), 0.24)
    poe(x, graos(rng, n_de(0.6), 35, 0.0, 0.55, 400, 2500, 0.012) * 0.45, 0.32)
    poe(x, passa(baque(n_de(0.3), 110, 70, 0.08, 0.3), None, 1500, 2) * 0.35, 0.7)
    return reverb(x, 0.45, 0.22)


def toque_do_tempo(rng, v):
    """O toque de Cronos: o tique-taque que acelera ao contrário, o "vuum" do tempo voltando e a areia escorrendo."""
    x = _z(1.3)
    em = 0.05
    for k in range(10):
        poe(x, modal(n_de(0.05), 2200 if k % 2 else 1700, rng=rng, **METAL) * env(n_de(0.05), 0.0005, 0.015) * 0.2, em)
        em += 0.1 * (1 - 0.08 * k)
    n = n_de(0.6)
    poe(x, seno(varre(500, 200, n, 1.0), n) * sobe_e_some(n, 0.5, 1.3) * 0.06, 0.25)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.5, 1.3) * 0.08, 0.45)
    poe(x, passa(baque(n_de(0.3), 90, 50, 0.1, 0.2), None, 1200, 2) * 0.4, 0.55)
    return reverb(x, 0.55, 0.28)


SONS: dict = {
    "bastoes-eletricos": (bastoes_eletricos, "básico do Asa Noturna: os bastões e o choque"),
    "lanternada": (lanternada, "básico do Dipper: a lanterna e o tonc"),
    "gancho-de-mabel": (gancho_de_mabel, "básico da Mabel: o gancho e o glitter"),
    "faisca-arcana": (faisca_arcana, "básico da Yennefer: a centelha"),
    "soco-do-nemesis": (soco_do_nemesis, "básico do Nêmesis: o grunhido e o soco"),
    "faisca-de-zeus": (faisca_de_zeus, "básico de Zeus: o trovão"),
    "jato-do-tridente": (jato_do_tridente, "básico de Poseidon: os jatos de água"),
    "escudada-de-atena": (escudada_de_atena, "básico de Atena: o escudo de bronze"),
    "lanca-de-ares": (lanca_de_ares, "básico de Ares: o grito e a lança"),
    "raio-de-apolo": (raio_de_apolo, "básico de Apolo: o sol e o feixe"),
    "flecha-lunar": (flecha_lunar, "básico de Ártemis: a flecha de prata"),
    "chute-alado": (chute_alado, "básico de Hermes: as asinhas e o chute"),
    "beijo-soprado": (beijo_soprado, "básico de Afrodite: o beijo e os corações"),
    "bote-da-medusa": (bote_da_medusa, "básico da Medusa: o sibilo e a pedra"),
    "toque-do-tempo": (toque_do_tempo, "básico de Cronos: o relógio para trás"),
}
