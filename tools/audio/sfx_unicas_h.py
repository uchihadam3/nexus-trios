"""Os sons da rodada 7 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_h.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def cristal_prata(rng, v):
    """Sailor Moon: o Cristal de Prata (a caixinha de música subindo) e o brilho."""
    x = _z(2.0)
    for k, f in enumerate((1047, 1319, 1568, 2093, 1568, 2093, 2637)):
        poe(x, _sino(rng, f, 0.5, 0.035, CRISTAL), 0.1 * k)
    poe(x, _acorde((523, 659, 784, 1047), 1.2, 0.035, 0.2, 0.7), 0.4)
    poe(x, _sopro(rng, 1.0, 3000, 9000, 0.1, 0.4), 0.3)
    return reverb(x, 0.8, 0.4)


def hahaha(rng, v):
    """Coringa: a carta virando, a risada maluca (os tons que pulam) e o gás chiando."""
    x = _z(2.0)
    poe(x, passa(rosa(rng, n_de(0.1)), 2000, 8000, 2) * env(n_de(0.1), 0.002, 0.06) * 0.4, 0.0)
    for k in range(6):
        n = n_de(0.11)
        f = 520 + 60 * (k % 2) - 15 * k
        poe(x, satura(seno(varre(f, f * 0.85, n), n), 1.8) * env(n, 0.01, 0.08) * 0.05, 0.35 + 0.12 * k)
    m = n_de(1.2)
    poe(x, passa(rosa(rng, m), 2000, 7000, 2) * sobe_e_some(m, 0.3, 1.3) * 0.25, 0.5)
    return reverb(x, 0.6, 0.3)


def imprevisivel(rng, v):
    """Arlequina: o martelão girando (o vento pesado), a pancada (o "boing") e o confete."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.45, 300, 2500, 0.8, 1.6, 0.6), 0.0)
    poe(x, _baque(120, 50, 0.4, 0.9, 2.4), 0.55)
    n = n_de(0.5)
    t = _t(n)
    poe(x, seno(220 * (1 + 0.3 * np.sin(2 * math.pi * 12 * t) * np.exp(-t * 6)), n) * env(n, 0.005, 0.35) * 0.08, 0.57)
    poe(x, graos(rng, n_de(0.6), 40, 0.0, 0.7, 2500, 8000, 0.003) * 0.3, 0.6)
    return reverb(x, 0.5, 0.25)


def odio_herois(rng, v):
    """Lex Luthor: os cristais de kryptonita crescendo (os rangidos de vidro) e o zumbido radioativo."""
    x = _z(1.9)
    for k in range(6):
        poe(x, _sino(rng, 1400 + 200 * k, 0.4, 0.035, VIDRO), 0.05 * k)
    n = n_de(1.4)
    t = _t(n)
    poe(x, satura(seno(100, n) + seno(150, n) * 0.5, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 7 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.07, 0.3)
    poe(x, graos(rng, n, 60, 0.0, 0.9, 1500, 6000, 0.002) * 0.2, 0.3)
    return reverb(x, 0.6, 0.3)


def viltrumita(rng, v):
    """Invencível: a decolagem (o vento rasgando), o estrondo sônico e os pedaços caindo."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.5, 200, 6000, 0.8, 1.4, 0.7), 0.0)
    poe(x, _baque(80, 30, 0.6, 1.0, 3.0), 0.45)
    poe(x, satura(passa(rosa(rng, n_de(0.8)), 40, 3000, 2) * env(n_de(0.8), 0.001, 0.3), 2.5) * 0.6, 0.45)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.04), 500, 3000, 0.02) * 0.3, 0.8 + 0.1 * k)
    return reverb(x, 0.6, 0.3)


def orgulho_viltrumita(rng, v):
    """Omni-Man: o soco descendo (o vento) e o impacto que racha o chão."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.35, 150, 3000, 0.9, 1.6, 0.6), 0.0)
    poe(x, _baque(55, 22, 0.9, 1.0, 3.2), 0.38)
    poe(x, passa(rosa(rng, n_de(1.2)), 30, 500, 2) * env(n_de(1.2), 0.002, 0.7) * 0.6, 0.38)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.06), 300, 2500, 0.02) * 0.4, 0.45 + 0.05 * k)
    return reverb(x, 0.6, 0.3)


def bravo(rng, v):
    """Raphael: os sais girando e cruzando (o metal), e o rosnado de raiva."""
    x = _z(1.8)
    for k in range(2):
        poe(x, _whoosh(rng, 0.2, 1500, 8000, 0.5, 1.4, 0.4), 0.05 * k)
    poe(x, _sino(rng, 2400, 0.6, 0.1, METAL), 0.3)
    poe(x, _sino(rng, 2700, 0.6, 0.08, METAL), 0.32)
    n = n_de(0.6)
    poe(x, satura(seno(varre(160, 120, n), n) + passa(rosa(rng, n), 150, 1500, 2) * 0.7, 3) * env(n, 0.03, 0.35) * 0.12, 0.8)
    return reverb(x, 0.5, 0.25)


def contencao(rng, v):
    """Donatello: o bastão tecnológico ligando (os bipes) e o campo de força fechando (o zumbido que sobe)."""
    x = _z(1.9)
    for k in range(3):
        m = n_de(0.06)
        poe(x, seno(1500 + 300 * k, m) * env(m, 0.003, 0.05) * 0.05, 0.05 * k)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(varre(150, 450, n, 1.2), n) * 0.06 + satura(seno(60, n), 2) * 0.03) * (0.7 + 0.3 * np.sin(2 * math.pi * 30 * t)) * sobe_e_some(n, 0.8, 1.0), 0.2)
    poe(x, _sino(rng, 880, 0.6, 0.06, VIDRO), 1.15)
    return reverb(x, 0.5, 0.25)


def improviso(rng, v):
    """Michelangelo: o nunchaku girando (os zunidos rápidos) e a pizza (o "tchan" feliz)."""
    x = _z(1.8)
    for k in range(7):
        poe(x, _whoosh(rng, 0.1, 1500, 6000, 0.5, 1.4, 0.35), 0.06 * k)
    poe(x, _baque(300, 160, 0.1, 0.3), 0.45)
    for k, f in enumerate((523, 659, 784, 1047)):
        poe(x, _quadrada(f, n_de(0.1)) * env(n_de(0.1), 0.003, 0.08) * 0.03, 0.75 + 0.08 * k)
    return reverb(x, 0.4, 0.2)


def exorcismo(rng, v):
    """Constantine: o isqueiro, a fala em latim (o murmúrio grave) e o pentagrama acendendo."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.04), 2000, 7000, 0.006) * 0.8, 0.0)
    poe(x, passa(rosa(rng, n_de(0.3)), 500, 3000, 2) * env(n_de(0.3), 0.01, 0.2) * 0.3, 0.05)
    n = n_de(1.2)
    t = _t(n)
    poe(x, satura(seno(110 + 10 * np.sin(2 * math.pi * 3 * t), n), 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 5 * t) ** 2) * sobe_e_some(n, 0.4, 1.2) * 0.06, 0.3)
    poe(x, _sino(rng, 196, 1.2, 0.12, SINO), 0.9)
    return reverb(x, 0.8, 0.4)


def pica_pau(rng, v):
    """Pica-Pau: as bicadas na madeira (toques rápidos e secos) e a risada."""
    x = _z(1.9)
    for k in range(10):
        n = n_de(0.05)
        poe(x, (seno(900, n) * 0.5 + passa(rosa(rng, n), 800, 4000, 2)) * env(n, 0.001, 0.02) * 0.4, 0.04 + 0.055 * k)
    for k in range(5):
        n = n_de(0.1)
        poe(x, seno(varre(1100, 900, n), n) * env(n, 0.005, 0.07) * 0.05, 0.8 + 0.11 * k)
    return reverb(x, 0.4, 0.2)


def pernalonga(rng, v):
    """Pernalonga: o buraco abrindo, a cenoura saindo (o tom que sobe) e a mordida (o crec)."""
    x = _z(1.8)
    poe(x, passa(rosa(rng, n_de(0.3)), 200, 1500, 2) * env(n_de(0.3), 0.01, 0.2) * 0.4, 0.0)
    n = n_de(0.35)
    poe(x, seno(varre(300, 900, n), n) * env(n, 0.01, 0.25) * 0.06, 0.25)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.04), 1500, 6000, 0.008) * 0.6, 0.75 + 0.1 * k)
    for k in range(3):
        poe(x, _sino(rng, 2093 + 300 * k, 0.3, 0.025, CRISTAL), 0.95 + 0.07 * k)
    return reverb(x, 0.4, 0.2)


def planador(rng, v):
    """Aang: o ar girando (o vento em espiral) e o planador abrindo (o estalo do pano)."""
    x = _z(1.9)
    n = n_de(1.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 500, 4000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * (3 + 3 * t) * t)) * sobe_e_some(n, 0.4, 1.3) * 0.45, 0.0)
    poe(x, passa(rosa(rng, n_de(0.1)), 400, 3000, 2) * env(n_de(0.1), 0.002, 0.05) * 0.6, 0.4)
    poe(x, _sino(rng, 1760, 0.6, 0.035, CRISTAL), 0.45)
    return reverb(x, 0.6, 0.3)


def lamina_magica(rng, v):
    """Samurai Jack: o silêncio, o corte único (o shing longo) e os pedaços caindo."""
    x = _z(2.0)
    poe(x, _sino(rng, 3200, 0.4, 0.04, METAL), 0.0)
    poe(x, _whoosh(rng, 0.2, 2500, 11000, 0.3, 1.4, 0.8), 0.48)
    n = n_de(1.2)
    poe(x, (seno(3000, n) * 0.04 + seno(4500, n) * 0.015) * env(n, 0.002, 0.8), 0.5)
    for k in range(5):
        poe(x, _sino(rng, 900 + 150 * k, 0.2, 0.03, METAL), 1.0 + 0.06 * k)
    return reverb(x, 0.7, 0.35)


def grayskull(rng, v):
    """He-Man: "Eu tenho a força!" — a espada erguida, o raio e o acorde heroico."""
    x = _z(2.2)
    n = n_de(0.4)
    poe(x, seno(varre(400, 900, n), n) * env(n, 0.02, 0.3) * 0.05, 0.0)
    poe(x, _trovao(rng, 1.2, 1.0), 0.5)
    poe(x, _acorde((196, 294, 392, 494, 587), 1.4, 0.06, 0.02, 0.8), 0.6)
    return reverb(x, 0.7, 0.35)


def espinafre(rng, v):
    """Popeye: a lata espremida (o metal amassando), o espinafre engolido e a musiquinha do marinheiro."""
    x = _z(2.0)
    poe(x, _sino(rng, 700, 0.3, 0.08, METAL), 0.15)
    poe(x, passa(rosa(rng, n_de(0.2)), 300, 2000, 2) * env(n_de(0.2), 0.005, 0.12) * 0.4, 0.3)
    for k, f in enumerate((392, 523, 523, 659, 784, 1047)):
        n = n_de(0.12 if k < 5 else 0.5)
        poe(x, (seno(f, n) + seno(f * 2, n) * 0.3) * env(n, 0.005, 0.1 if k < 5 else 0.4) * 0.05, 0.75 + 0.1 * k)
    return reverb(x, 0.4, 0.2)


def matriz(rng, v):
    """Optimus: a Matriz abrindo (o mecanismo girando) e a luz sagrada (o coro claro)."""
    x = _z(2.1)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.005) * 0.5 + 0, 0.05 + 0.07 * k)
    n = n_de(0.5)
    poe(x, seno(varre(200, 500, n), n) * env(n, 0.02, 0.3) * 0.05, 0.1)
    poe(x, _acorde((262, 330, 392, 523, 659), 1.5, 0.05, 0.15, 0.9), 0.55)
    poe(x, _brilho(rng, 0.8, 2093, 0.04, CRISTAL), 0.6)
    return reverb(x, 0.8, 0.4)


def poder_escondido(rng, v):
    """Salsicha: o silêncio estranho e o 1% do poder subindo (o grave calmo que vira trovão)."""
    x = _z(2.2)
    n = n_de(1.5)
    poe(x, (seno(55, n) + seno(82, n) * 0.6) * sobe_e_some(n, 0.7, 1.0) * 0.12, 0.0)
    poe(x, passa(rosa(rng, n), 100, 2000, 2) * sobe_e_some(n, 0.7, 1.0) * 0.4, 0.0)
    poe(x, _trovao(rng, 1.0, 0.7), 1.0)
    poe(x, graos(rng, n_de(0.8), 40, 0.0, 0.8, 3000, 10000, 0.003) * 0.3, 1.0)
    return reverb(x, 0.7, 0.35)


def esponja(rng, v):
    """Bob Esponja: as bolhas subindo (os "blup") e a cura (o tom alegre)."""
    x = _z(1.9)
    q = np.random.default_rng(3)
    for k in range(10):
        n = n_de(0.08)
        f = q.uniform(400, 900)
        poe(x, seno(varre(f, f * 2.2, n), n) * env(n, 0.005, 0.05) * 0.05, 0.05 + 0.08 * k)
    poe(x, _acorde((523, 659, 784), 0.8, 0.04, 0.02, 0.5), 0.9)
    return reverb(x, 0.5, 0.25)


def scooby_lanche(rng, v):
    """Scooby-Doo: o biscoito voando, a bocada (o nhac) e o "hehehe" feliz."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.4, 800, 3000, 0.6, 1.3, 0.3), 0.0)
    poe(x, estalo(rng, n_de(0.05), 800, 4000, 0.01) * 0.8, 0.95)
    poe(x, _baque(200, 100, 0.1, 0.3), 0.95)
    for k in range(4):
        n = n_de(0.1)
        poe(x, satura(seno(varre(380, 300, n), n), 1.6) * env(n, 0.01, 0.07) * 0.05, 1.15 + 0.12 * k)
    return reverb(x, 0.4, 0.2)


def portal_rick(rng, v):
    """Rick: a arma de portal (o "piu") e o portal verde borbulhando."""
    x = _z(2.0)
    n = n_de(0.25)
    poe(x, seno(varre(1200, 400, n), n) * env(n, 0.003, 0.2) * 0.07, 0.0)
    m = n_de(1.5)
    t = _t(m)
    poe(x, passa(rosa(rng, m), 200, 2000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 8 * t)) * sobe_e_some(m, 0.2, 1.3) * 0.4, 0.15)
    for k in range(8):
        f = 300 + 80 * k
        b = n_de(0.06)
        poe(x, seno(varre(f, f * 1.8, b), b) * env(b, 0.005, 0.04) * 0.035, 0.3 + 0.12 * k)
    return reverb(x, 0.6, 0.3)


def heroi_finn(rng, v):
    """Finn: o "Ei, briga comigo!" (o grito curto), a espada saindo e o brilho."""
    x = _z(1.8)
    n = n_de(0.3)
    poe(x, satura(seno(varre(520, 620, n), n), 1.6) * env(n, 0.02, 0.2) * 0.06, 0.0)
    poe(x, _sino(rng, 2600, 0.6, 0.08, METAL), 0.35)
    poe(x, _whoosh(rng, 0.2, 2000, 8000, 0.5, 1.4, 0.4), 0.3)
    poe(x, _brilho(rng, 0.6, 2349, 0.05, CRISTAL), 0.75)
    return reverb(x, 0.5, 0.25)


def canhao_fusao(rng, v):
    """Megatron: o canhão de fusão carregando (o zumbido grave subindo) e o disparo."""
    x = _z(2.1)
    n = n_de(1.0)
    poe(x, (satura(seno(varre(60, 200, n, 1.3), n), 2.5) * 0.1 + passa(rosa(rng, n), 300, 3000, 2) * 0.2) * sobe_e_some(n, 0.95, 1.0), 0.0)
    m = n_de(0.9)
    poe(x, (satura(seno(80, m), 2.5) * 0.15 + passa(rosa(rng, m), 100, 6000, 2) * 0.5) * env(m, 0.005, 0.45, segura=0.2), 0.95)
    poe(x, _baque(60, 25, 0.6, 0.8, 2.6), 0.95)
    return reverb(x, 0.6, 0.3)


def briguenta(rng, v):
    """Docinho: o voo rasgando o céu e o soco que estoura."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.35, 600, 8000, 0.8, 1.3, 0.7), 0.0)
    poe(x, _baque(110, 45, 0.5, 1.0, 2.8), 0.65)
    poe(x, graos(rng, n_de(0.5), 40, 0.0, 0.5, 2000, 8000, 0.003) * 0.4, 0.66)
    return reverb(x, 0.4, 0.2)


def vassoura(rng, v):
    """Mickey: a magia do aprendiz (o tilintar), as vassouras marchando (o passo ritmado) e os baldes."""
    x = _z(2.0)
    for k, f in enumerate((1568, 2093, 2637)):
        poe(x, _sino(rng, f, 0.4, 0.04, CRISTAL), 0.08 * k)
    for k in range(8):
        poe(x, _baque(260 if k % 2 else 200, 140, 0.08, 0.25, 1.5), 0.45 + 0.15 * k)
        poe(x, passa(rosa(rng, n_de(0.05)), 2500, 7000, 2) * env(n_de(0.05), 0.002, 0.03) * 0.3, 0.45 + 0.15 * k)
    return reverb(x, 0.5, 0.25)


def quaaack(rng, v):
    """Pato Donald: o "QUAAACK" bravo (o som rasgado e nasal) e os socos para todo lado."""
    x = _z(1.9)
    n = n_de(0.6)
    t = _t(n)
    nasal = satura(seno(380 + 60 * np.sin(2 * math.pi * 9 * t), n) + seno(760, n) * 0.6 + passa(rosa(rng, n), 800, 3000, 2) * 0.5, 4)
    poe(x, passa(nasal, 300, 4000, 2) * env(n, 0.01, 0.4) * 0.08, 0.0)
    for k in range(3):
        poe(x, _baque(150, 70, 0.2, 0.6, 2.2), 0.6 + 0.18 * k)
    return reverb(x, 0.4, 0.2)


SONS: dict = {
    "mu-cristal-prata": (cristal_prata, "Sailor Moon: o Cristal de Prata"),
    "mu-hahaha": (hahaha, "Coringa: a risada"),
    "mu-imprevisivel": (imprevisivel, "Arlequina: o martelão"),
    "mu-odio-herois": (odio_herois, "Lex Luthor: a kryptonita"),
    "mu-viltrumita": (viltrumita, "Invencível: o estrondo sônico"),
    "mu-orgulho-viltrumita": (orgulho_viltrumita, "Omni-Man: o soco e a cratera"),
    "mu-bravo": (bravo, "Raphael: os sais e a raiva"),
    "mu-contencao": (contencao, "Donatello: o campo de contenção"),
    "mu-improviso": (improviso, "Michelangelo: o nunchaku e a pizza"),
    "mu-exorcismo": (exorcismo, "Constantine: o exorcismo"),
    "mu-pica-pau": (pica_pau, "Pica-Pau: as bicadas"),
    "mu-pernalonga": (pernalonga, "Pernalonga: a cenoura"),
    "mu-planador": (planador, "Aang: o ar"),
    "mu-lamina-magica": (lamina_magica, "Samurai Jack: o corte"),
    "mu-grayskull": (grayskull, "He-Man: o poder de Grayskull"),
    "mu-espinafre": (espinafre, "Popeye: o espinafre"),
    "mu-matriz": (matriz, "Optimus: a Matriz"),
    "mu-poder-escondido": (poder_escondido, "Salsicha: o poder escondido"),
    "mu-esponja": (esponja, "Bob Esponja: as bolhas"),
    "mu-scooby-lanche": (scooby_lanche, "Scooby: o Scooby-lanche"),
    "mu-portal-rick": (portal_rick, "Rick: o portal"),
    "mu-heroi-finn": (heroi_finn, "Finn: o herói"),
    "mu-canhao-fusao": (canhao_fusao, "Megatron: o canhão de fusão"),
    "mu-briguenta": (briguenta, "Docinho: o soco"),
    "mu-vassoura": (vassoura, "Mickey: as vassouras"),
    "mu-quaaack": (quaaack, "Pato Donald: QUAAACK"),
}
