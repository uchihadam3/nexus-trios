"""Os sons da rodada 60 das habilidades próprias (veja tools/vfx/familias_v2/rodada60.py)."""
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


def _giro(rng, seg, f=300, g=0.25):
    """O zumbido girando do Rasengan."""
    n = n_de(seg)
    t = _t(n)
    return (passa(rosa(rng, n), 400, 4000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 25 * t)) * 0.8 + seno(f, n) * 0.2) * sobe_e_some(n, 0.6, 1.2) * g


def _fumaca(rng, seg, g=0.3):
    n = n_de(seg)
    return passa(rosa(rng, n), 200, 3000, 2) * env(n, 0.01, seg * 0.7) * g


def _choque(rng, seg, g=0.2):
    x = _z(seg + 0.05)
    q = np.random.default_rng(60)
    for k in range(int(seg * 40)):
        poe(x, estalo(rng, n_de(0.012), 2500, 9000, 0.002) * g * q.uniform(0.3, 1.0), q.uniform(0, seg))
    return x


def _coaxar(rng, f=110, g=0.06):
    n = n_de(0.35)
    t = _t(n)
    return satura(seno(varre(f, f * 0.8, n), n) * (0.5 + 0.5 * np.sin(2 * math.pi * 35 * t)), 4) * env(n, 0.02, 0.25) * g


# ------------------------------------------------------------------ Jiraiya

def rasengan_jiraiya(rng, v):
    """Jiraiya: o Rasengan girando na palma e o estouro ("RASENGAN!")."""
    x = _z(2.1)
    poe(x, _giro(rng, 0.5, 300, 0.25), 0.0)
    poe(x, _whoosh(rng, 0.2, 300, 3000, 0.8, 1.3, 0.45), 0.2)
    poe(x, _baque(60, 25, 0.6, 0.9, 2.8), 0.4)
    poe(x, _explosao(rng, 0.45, 60), 0.4)
    return reverb(x, 0.7, 0.35)


def invocacao_gamabunta(rng, v):
    """Jiraiya: "KUCHIYOSE NO JUTSU!" — o selo batendo no chão, a fumaça e o sapo gigante."""
    x = _z(2.5)
    poe(x, _baque(90, 45, 0.3, 0.7, 2.4), 0.05)
    poe(x, _fumaca(rng, 0.8, 0.4), 0.25)
    poe(x, _baque(35, 14, 1.2, 1.0, 3.4), 0.4)
    poe(x, _coaxar(rng, 90, 0.07), 0.7)
    poe(x, _sino(rng, 1047, 0.4, 0.02, METAL), 0.6)
    return reverb(x, 0.9, 0.45)


def jiraiya_preparo(rng, v):
    """Jiraiya (Preparo): o sapinho coaxando e o óleo borbulhando (em laço)."""
    x = _z(1.4)
    poe(x, _coaxar(rng, 220, 0.03), 0.1)
    poe(x, _coaxar(rng, 240, 0.025), 0.75)
    q = np.random.default_rng(601)
    for k in range(8):
        poe(x, _piu(q.uniform(250, 500), q.uniform(600, 900), 0.04, 0.01), 0.05 + 0.16 * k)
    return reverb(x, 0.6, 0.3)


def oleo_de_sapo_em_chamas(rng, v):
    """Jiraiya: o jato de óleo e o fogo do sapo rugindo em todos os rivais."""
    x = _z(2.7)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * env(n, 0.03, 0.25) * 0.2, 0.05)
    poe(x, _fogo(rng, 1.2, 0.5, 100, 5000), 0.3)
    poe(x, _baque(50, 22, 0.6, 0.7, 2.6), 0.35)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Tsunade

def soco_de_cem_toneladas(rng, v):
    """Tsunade: o soco que racha o chão (o estrondo e as pedras)."""
    x = _z(2.3)
    poe(x, _whoosh(rng, 0.25, 100, 1500, 0.9, 1.3, 0.6), 0.05)
    poe(x, _baque(30, 10, 1.4, 1.0, 3.8), 0.32)
    poe(x, _explosao(rng, 0.7, 35), 0.32)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.05), 150, 2500, 0.015) * 0.4, 0.36 + 0.04 * k)
    return reverb(x, 0.9, 0.45)


def ninjutsu_medico(rng, v):
    """Tsunade: o chakra verde nas mãos (o zumbido suave) e a cura."""
    x = _z(2.0)
    n = n_de(1.1)
    t = _t(n)
    poe(x, (seno(392, n) + seno(587, n) * 0.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.015, 0.0)
    poe(x, _acorde((523, 659, 784), 0.8, 0.022), 0.45)
    poe(x, _brilho(rng, 0.5, 1319, 0.025, CRISTAL), 0.5)
    return reverb(x, 0.8, 0.4)


def tsunade_preparo(rng, v):
    """Tsunade (Preparo): o selo da testa se abrindo e as marcas correndo (em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, (seno(196 + 60 * t, n) + seno(294 + 90 * t, n) * 0.5) * sobe_e_some(n, 0.6, 1.2) * 0.018, 0.0)
    poe(x, _sino(rng, 784, 0.6, 0.015, CRISTAL), 0.2)
    return reverb(x, 0.8, 0.4)


def forca_de_cem_selos(rng, v):
    """Tsunade: "BYAKUGŌ NO IN!" — as marcas espalhando e a luz levantando o aliado (o coro subindo)."""
    x = _z(2.8)
    n = n_de(0.5)
    poe(x, seno(varre(200, 800, n), n) * env(n, 0.4, 0.05) * 0.02, 0.0)
    poe(x, _sino(rng, 523, 1.2, 0.05, SINO), 0.45)
    poe(x, _acorde((392, 494, 587, 784, 988), 1.6, 0.03, 0.2, 1.0), 0.5)
    poe(x, _brilho(rng, 1.0, 1568, 0.03, CRISTAL), 0.6)
    return reverb(x, 1.1, 0.55)


# ------------------------------------------------------------------ Sailor Mars

def fogo_de_marte(rng, v):
    """Sailor Mars: "FOGO DE MARTE, ACENDA!" — o fogo em espiral até o rival."""
    x = _z(2.1)
    poe(x, _fogo(rng, 0.7, 0.4, 150, 4500), 0.05)
    poe(x, _whoosh(rng, 0.4, 300, 3000, 0.6, 1.3, 0.35), 0.05)
    poe(x, _baque(80, 40, 0.3, 0.6), 0.38)
    poe(x, _fogo(rng, 0.6, 0.15), 0.45)
    return reverb(x, 0.7, 0.35)


def pergaminho_sagrado(rng, v):
    """Sailor Mars: os pergaminhos voando ("shff") e o sino sagrado protegendo o trio."""
    x = _z(2.1)
    for k in range(3):
        n = n_de(0.15)
        poe(x, passa(rosa(rng, n), 1500, 6000, 2) * env(n, 0.02, 0.1) * 0.1, 0.05 + 0.06 * k)
    poe(x, _sino(rng, 880, 1.0, 0.04, SINO), 0.4)
    poe(x, _acorde((587, 740, 880), 0.8, 0.02), 0.45)
    return reverb(x, 1.0, 0.5)


def sailormars_preparo(rng, v):
    """Sailor Mars (Preparo): o arco de fogo sendo puxado (a corda rangendo e o fogo em laço)."""
    x = _z(1.4)
    poe(x, _fogo(rng, 1.2, 0.15), 0.0)
    n = n_de(0.6)
    poe(x, seno(varre(150, 220, n), n) * env(n, 0.3, 0.2) * 0.02, 0.2)
    return reverb(x, 0.6, 0.3)


def flecha_flamejante_de_marte(rng, v):
    """Sailor Mars: a corda soltando ("TWANG"), a flecha de fogo zunindo e a explosão."""
    x = _z(2.5)
    n = n_de(0.2)
    poe(x, seno(varre(220, 180, n), n) * env(n, 0.001, 0.15) * 0.05, 0.28)
    poe(x, _whoosh(rng, 0.25, 600, 5000, 0.8, 1.3, 0.5), 0.28)
    poe(x, _fogo(rng, 0.3, 0.3), 0.3)
    poe(x, _baque(45, 18, 0.8, 0.9, 3.0), 0.5)
    poe(x, _explosao(rng, 0.6, 50), 0.5)
    poe(x, _fogo(rng, 0.7, 0.2), 0.55)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Steven

def escudo_da_rosa(rng, v):
    """Steven: o escudo abrindo ("plim"), a rosa e o acorde doce protegendo o trio."""
    x = _z(2.1)
    poe(x, _brilho(rng, 0.5, 1047, 0.03, CRISTAL), 0.05)
    n = n_de(0.4)
    poe(x, seno(varre(400, 900, n), n) * env(n, 0.05, 0.3) * 0.02, 0.1)
    poe(x, _acorde((523, 659, 784, 1047), 1.0, 0.028), 0.35)
    return reverb(x, 0.9, 0.45)


def saliva_curativa(rng, v):
    """Steven: o "ptu" da saliva e os brilhinhos da cura."""
    x = _z(1.9)
    n = n_de(0.08)
    poe(x, passa(rosa(rng, n), 1000, 5000, 2) * env(n, 0.005, 0.05) * 0.1, 0.05)
    poe(x, _piu(600, 1400, 0.15, 0.02), 0.08)
    for k in range(5):
        poe(x, _brilho(rng, 0.3, 1568 + 220 * k, 0.015, CRISTAL), 0.35 + 0.06 * k)
    poe(x, _acorde((659, 784, 988), 0.7, 0.02), 0.45)
    return reverb(x, 0.9, 0.45)


def steven_preparo(rng, v):
    """Steven (Preparo): a bolha crescendo (o som de bolha de sabão em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, seno(400 + 300 * t, n) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.012, 0.0)
    return reverb(x, 0.8, 0.4)


def bolha_de_steven(rng, v):
    """Steven: a bolha voando e fechando em volta do rival ("blop")."""
    x = _z(2.0)
    poe(x, _piu(400, 900, 0.3, 0.02), 0.05)
    poe(x, _whoosh(rng, 0.3, 500, 2500, 0.7, 1.3, 0.3), 0.1)
    n = n_de(0.15)
    poe(x, seno(varre(300, 700, n), n) * env(n, 0.005, 0.1) * 0.05, 0.4)
    poe(x, _sino(rng, 784, 0.6, 0.02, CRISTAL), 0.42)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Garnet

def futuro_previsto(rng, v):
    """Garnet: o terceiro olho abrindo e os futuros se espalhando (o acorde misterioso)."""
    x = _z(2.1)
    n = n_de(0.3)
    poe(x, seno(varre(200, 600, n), n) * env(n, 0.25, 0.05) * 0.02, 0.05)
    poe(x, _acorde((311, 392, 466, 622), 1.2, 0.022, 0.1, 0.8), 0.3)
    for k in range(5):
        poe(x, _brilho(rng, 0.3, 1245 + 150 * k, 0.012, CRISTAL), 0.35 + 0.05 * k)
    return reverb(x, 1.0, 0.5)


def manoplas_garnet(rng, v):
    """Garnet: as manoplas aparecendo, o soco duplo e o choque elétrico."""
    x = _z(2.0)
    poe(x, _sino(rng, 196, 0.3, 0.03, METAL), 0.0)
    poe(x, _whoosh(rng, 0.2, 150, 2000, 0.8, 1.3, 0.5), 0.1)
    poe(x, _baque(70, 30, 0.45, 0.9, 2.6), 0.3)
    poe(x, _baque(80, 35, 0.4, 0.7, 2.4), 0.34)
    poe(x, _choque(rng, 0.6, 0.18), 0.35)
    return reverb(x, 0.7, 0.35)


def garnet_preparo(rng, v):
    """Garnet (Preparo): as duas gemas girando e se juntando (o acorde de fusão em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, (seno(330, n) * (0.5 + 0.5 * np.sin(2 * math.pi * 2 * t)) + seno(494, n) * (0.5 - 0.5 * np.sin(2 * math.pi * 2 * t))) * sobe_e_some(n, 0.5, 1.2) * 0.015, 0.0)
    poe(x, _brilho(rng, 0.5, 988, 0.015, CRISTAL), 0.5)
    return reverb(x, 0.8, 0.4)


def fusao_perfeita(rng, v):
    """Garnet: as gemas se fundindo (o brilho), as manoplas gigantes e o soco com raios."""
    x = _z(2.6)
    poe(x, _acorde((330, 415, 494, 659), 0.5, 0.025), 0.0)
    poe(x, _brilho(rng, 0.4, 1319, 0.03, CRISTAL), 0.15)
    poe(x, _whoosh(rng, 0.3, 100, 1500, 0.9, 1.3, 0.6), 0.2)
    poe(x, _baque(35, 12, 1.2, 1.0, 3.6), 0.44)
    poe(x, _explosao(rng, 0.6, 40), 0.44)
    poe(x, _choque(rng, 0.7, 0.22), 0.46)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Johnny Bravo

def pose_johnny(rng, v):
    """Johnny Bravo: "Ei, gatinha!" — a pose, o brilho do topete e o assobio."""
    x = _z(2.1)
    n = n_de(0.5)
    poe(x, seno(varre(1200, 2400, n, 0.5), n) * env(n, 0.05, 0.1) * 0.025, 0.05)
    n = n_de(0.4)
    poe(x, seno(varre(2400, 1400, n), n) * env(n, 0.02, 0.3) * 0.025, 0.55)
    poe(x, _brilho(rng, 0.4, 2093, 0.03, CRISTAL), 0.25)
    poe(x, _acorde((392, 494, 587), 0.5, 0.02), 0.4)
    return reverb(x, 0.7, 0.35)


def soco_de_karate(rng, v):
    """Johnny Bravo: "HUAH!" e o golpe de karatê seco."""
    x = _z(1.9)
    n = n_de(0.25)
    t = _t(n)
    poe(x, satura(seno(varre(220, 160, n), n) * (1 + 0.2 * np.sin(2 * math.pi * 30 * t)) + passa(rosa(rng, n), 300, 2500, 2) * 0.4, 3) * env(n, 0.01, 0.18) * 0.05, 0.05)
    poe(x, _whoosh(rng, 0.15, 500, 5000, 0.8, 1.3, 0.5), 0.15)
    poe(x, _baque(110, 50, 0.3, 0.8, 2.4), 0.28)
    return reverb(x, 0.6, 0.3)


def johnny_preparo(rng, v):
    """Johnny Bravo (Preparo): os músculos flexionando ("hmpf, hmpf") e o brilho (em laço)."""
    x = _z(1.4)
    for k in range(3):
        n = n_de(0.12)
        poe(x, satura(seno(varre(130, 110, n), n), 3) * env(n, 0.01, 0.1) * 0.04, 0.1 + 0.45 * k)
    poe(x, _brilho(rng, 0.4, 2349, 0.02, CRISTAL), 0.3)
    return reverb(x, 0.6, 0.3)


def musculos_de_aco(rng, v):
    """Johnny Bravo: os músculos estalando de tão fortes e o soco que amassa o rival."""
    x = _z(2.4)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.04), 300, 2500, 0.01) * 0.4, 0.05 + 0.08 * k)
    poe(x, _brilho(rng, 0.3, 2093, 0.025, CRISTAL), 0.2)
    poe(x, _whoosh(rng, 0.25, 150, 2000, 0.85, 1.3, 0.6), 0.25)
    poe(x, _baque(40, 15, 1.0, 1.0, 3.2), 0.46)
    poe(x, _explosao(rng, 0.5, 45), 0.46)
    return reverb(x, 0.8, 0.4)


SONS: dict = {
    "rasengan-jiraiya": (rasengan_jiraiya, "Jiraiya: Rasengan"),
    "invocacao-gamabunta": (invocacao_gamabunta, "Jiraiya: invocação Gamabunta"),
    "jiraiya-preparo": (jiraiya_preparo, "Jiraiya: o sapinho e o óleo (Preparo)"),
    "oleo-de-sapo-em-chamas": (oleo_de_sapo_em_chamas, "Jiraiya: óleo de sapo em chamas"),
    "soco-de-cem-toneladas": (soco_de_cem_toneladas, "Tsunade: soco de cem toneladas"),
    "ninjutsu-medico": (ninjutsu_medico, "Tsunade: ninjutsu médico"),
    "tsunade-preparo": (tsunade_preparo, "Tsunade: o selo da testa (Preparo)"),
    "forca-de-cem-selos": (forca_de_cem_selos, "Tsunade: força de cem selos"),
    "fogo-de-marte": (fogo_de_marte, "Sailor Mars: fogo de Marte"),
    "pergaminho-sagrado": (pergaminho_sagrado, "Sailor Mars: pergaminho sagrado"),
    "sailormars-preparo": (sailormars_preparo, "Sailor Mars: o arco de fogo (Preparo)"),
    "flecha-flamejante-de-marte": (flecha_flamejante_de_marte, "Sailor Mars: flecha flamejante"),
    "escudo-da-rosa": (escudo_da_rosa, "Steven: escudo da Rosa"),
    "saliva-curativa": (saliva_curativa, "Steven: saliva curativa"),
    "steven-preparo": (steven_preparo, "Steven: a bolha crescendo (Preparo)"),
    "bolha-de-steven": (bolha_de_steven, "Steven: bolha"),
    "futuro-previsto": (futuro_previsto, "Garnet: futuro previsto"),
    "manoplas-garnet": (manoplas_garnet, "Garnet: manoplas"),
    "garnet-preparo": (garnet_preparo, "Garnet: as gemas se juntando (Preparo)"),
    "fusao-perfeita": (fusao_perfeita, "Garnet: fusão perfeita"),
    "pose-johnny": (pose_johnny, "Johnny Bravo: pose"),
    "soco-de-karate": (soco_de_karate, "Johnny Bravo: soco de karatê"),
    "johnny-preparo": (johnny_preparo, "Johnny Bravo: os músculos (Preparo)"),
    "musculos-de-aco": (musculos_de_aco, "Johnny Bravo: músculos de aço"),
}
