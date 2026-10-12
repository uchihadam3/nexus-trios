"""Os sons da rodada 17 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_r.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def chifres_serrados(rng, v):
    """Hellboy: o rosnado e o soco do punho de pedra."""
    x = _z(2.0)
    n = n_de(0.6)
    poe(x, satura(seno(varre(90, 70, n), n) + passa(rosa(rng, n), 100, 1200, 2) * 0.6, 3) * env(n, 0.05, 0.4) * 0.08, 0.0)
    poe(x, _whoosh(rng, 0.2, 300, 2500, 0.7, 1.4, 0.4), 0.3)
    poe(x, _baque(70, 30, 0.5, 0.9, 3.0), 0.45)
    poe(x, passa(rosa(rng, n_de(0.2)), 100, 2000, 2) * env(n_de(0.2), 0.002, 0.15) * 0.5, 0.45)
    return reverb(x, 0.5, 0.25)


def omnitrix(rng, v):
    """Ben 10: o Omnitrix girando (os cliques), apertando e o clarão verde da transformação."""
    x = _z(2.1)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.03), 1200, 5000, 0.005) * 0.5, 0.05 + 0.07 * k)
    poe(x, _baque(200, 100, 0.12, 0.3), 0.35)
    n = n_de(0.7)
    poe(x, (seno(varre(300, 1500, n, 0.6), n) * 0.06 + passa(rosa(rng, n), 2000, 9000, 2) * 0.2) * sobe_e_some(n, 0.2, 1.3), 0.45)
    poe(x, _brilho(rng, 0.8, 1760, 0.04, CRISTAL), 0.5)
    return reverb(x, 0.6, 0.3)


def pista_gelo(rng, v):
    """Gelado: a pista de gelo se formando (o chiado que corre) e os cristais."""
    x = _z(2.0)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 3000, 10000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.35, 0.0)
    poe(x, graos(rng, n, 50, 0.1, 0.9, 4000, 11000, 0.003) * 0.3, 0.1)
    for k in range(4):
        poe(x, _sino(rng, 2600 + 300 * k, 0.3, 0.03, VIDRO), 0.2 + 0.12 * k)
    poe(x, _whoosh(rng, 0.4, 800, 5000, 0.6, 1.4, 0.3), 0.2)
    return reverb(x, 0.6, 0.3)


def prodigio_instavel(rng, v):
    """Azula: o fogo azul acendendo e tremendo (o chiado instável) com os raios."""
    x = _z(2.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 300, 5000, 2), 2) * (0.6 + 0.4 * np.sign(np.sin(2 * math.pi * 11 * t))) * sobe_e_some(n, 0.2, 1.3) * 0.3, 0.0)
    poe(x, graos(rng, n_de(0.5), 40, 0.0, 0.9, 2500, 9000, 0.002) * 0.35, 0.3)
    poe(x, _acorde((233, 277, 349), 0.7, 0.035, 0.05, 0.5), 0.1)
    return reverb(x, 0.6, 0.3)


def penny(rng, v):
    """Bugiganga: o computador-livro da Penny (os bipes) e o "Uh-oh?" (o tom que sobe)."""
    x = _z(1.9)
    for k in range(5):
        poe(x, _quadrada(900 + 150 * (k % 3), n_de(0.05)) * env(n_de(0.05), 0.003, 0.04) * 0.02, 0.05 + 0.07 * k)
    poe(x, _piu(400, 700, 0.12, 0.05), 0.45)
    poe(x, _piu(500, 900, 0.15, 0.05), 0.6)
    return reverb(x, 0.4, 0.2)


def estica_jake(rng, v):
    """Jake: o corpo esticando (o "boing" elástico) e abraçando o aliado."""
    x = _z(1.9)
    n = n_de(0.5)
    t = _t(n)
    poe(x, seno(varre(150, 450, n) * (1 + 0.08 * np.sin(2 * math.pi * 14 * t)), n) * env(n, 0.01, 0.4) * 0.06, 0.0)
    m = n_de(0.3)
    poe(x, seno(varre(450, 200, m), m) * env(m, 0.01, 0.25) * 0.05, 0.5)
    poe(x, _baque(150, 90, 0.15, 0.3), 0.55)
    return reverb(x, 0.4, 0.2)


def sempre_junto(rng, v):
    """Robin: o bastão girando e o golpe em dupla."""
    x = _z(1.9)
    for k in range(3):
        poe(x, _whoosh(rng, 0.1, 1500, 6000, 0.6, 1.4, 0.3), 0.15 + 0.07 * k)
    poe(x, _baque(170, 80, 0.2, 0.5), 0.5)
    poe(x, _sino(rng, 1400, 0.3, 0.04, METAL), 0.5)
    return reverb(x, 0.5, 0.25)


def rumble_ball(rng, v):
    """Chopper: a Rumble Ball engolida ("gulp") e a transformação (o "puf" e o tom que muda)."""
    x = _z(2.0)
    poe(x, _piu(600, 300, 0.1, 0.05), 0.25)
    poe(x, _baque(150, 80, 0.15, 0.3), 0.3)
    poe(x, passa(rosa(rng, n_de(0.4)), 300, 4000, 2) * env(n_de(0.4), 0.005, 0.3) * 0.4, 0.35)
    for k, f in enumerate((262, 330, 392)):
        poe(x, _sino(rng, f * 2, 0.4, 0.04, SINO), 0.5 + 0.15 * k)
    return reverb(x, 0.5, 0.25)


def futuro_medico(rng, v):
    """Leorio: a maleta abrindo (o clique) e a cura em dobro (dois "plins")."""
    x = _z(1.9)
    poe(x, estalo(rng, n_de(0.03), 1000, 4000, 0.006), 0.05)
    poe(x, estalo(rng, n_de(0.03), 1200, 4500, 0.006), 0.12)
    poe(x, _sino(rng, 1047, 0.5, 0.05, CRISTAL), 0.35)
    poe(x, _sino(rng, 1319, 0.5, 0.05, CRISTAL), 0.5)
    poe(x, _acorde((523, 659, 784), 0.7, 0.03, 0.05, 0.5), 0.5)
    return reverb(x, 0.6, 0.3)


def asas_protetoras(rng, v):
    """Ísis: as asas abrindo (o bater grande) e a proteção (o acorde dourado)."""
    x = _z(2.1)
    for k in range(2):
        poe(x, _whoosh(rng, 0.35, 200, 2000, 0.5, 1.4, 0.45), 0.0 + 0.2 * k)
    poe(x, _acorde((330, 415, 494, 659), 1.1, 0.045, 0.1, 0.8), 0.3)
    poe(x, _sino(rng, 1319, 0.6, 0.04, CRISTAL), 0.35)
    return reverb(x, 0.8, 0.4)


def olho_de_horus(rng, v):
    """Hórus: o olho abrindo (o tom antigo) e o grito do falcão."""
    x = _z(2.0)
    poe(x, _acorde((220, 262, 330), 0.8, 0.04, 0.1, 0.6), 0.0)
    n = n_de(0.4)
    t = _t(n)
    poe(x, seno(varre(3000, 2200, n) * (1 + 0.03 * np.sin(2 * math.pi * 30 * t)), n) * env(n, 0.01, 0.3) * 0.035, 0.4)
    poe(x, seno(1800, n_de(0.08)) * env(n_de(0.08), 0.003, 0.06) * 0.04, 0.85)
    return reverb(x, 0.8, 0.4)


def cheiro_de_sangue(rng, v):
    """Sekhmet: as gotas, o farejar e o rugido da leoa com as garras."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _piu(1200, 600, 0.05, 0.03), 0.05 + 0.08 * k)
    for k in range(2):
        poe(x, passa(rosa(rng, n_de(0.08)), 1500, 5000, 2) * env(n_de(0.08), 0.01, 0.05) * 0.2, 0.3 + 0.1 * k)
    n = n_de(0.5)
    poe(x, satura(seno(varre(150, 100, n), n) + passa(rosa(rng, n), 200, 2000, 2) * 0.7, 3) * env(n, 0.03, 0.35) * 0.08, 0.45)
    for k in range(3):
        poe(x, _whoosh(rng, 0.1, 2000, 8000, 0.6, 1.4, 0.3), 0.5 + 0.04 * k)
    return reverb(x, 0.5, 0.25)


def implacavel(rng, v):
    """Jason: o "ki ki ki, ma ma ma" (o sussurro com eco) e o facão."""
    x = _z(2.1)
    for k in range(3):
        n = n_de(0.08)
        poe(x, passa(rosa(rng, n), 2500, 7000, 2) * env(n, 0.005, 0.06) * 0.3, 0.0 + 0.1 * k)
    for k in range(3):
        n = n_de(0.1)
        poe(x, passa(rosa(rng, n), 600, 2500, 2) * env(n, 0.01, 0.08) * 0.25, 0.3 + 0.1 * k)
    poe(x, _whoosh(rng, 0.2, 1500, 8000, 0.7, 1.4, 0.45), 0.42)
    poe(x, _baque(140, 60, 0.3, 0.5), 0.55)
    return reverb(x, 0.8, 0.4)


def exercito(rng, v):
    """Rambo: a rajada da metralhadora e a flecha explosiva."""
    x = _z(2.1)
    for k in range(8):
        n = n_de(0.08)
        poe(x, satura(passa(rosa(rng, n), 300, 7000, 2) * env(n, 0.0005, 0.04), 2.5) * 0.45, 0.1 + 0.05 * k)
    poe(x, _whoosh(rng, 0.2, 1000, 5000, 0.7, 1.4, 0.3), 0.45)
    poe(x, _explosao(rng, 1.0, 0.8), 0.62)
    return reverb(x, 0.5, 0.25)


def radiacao(rng, v):
    """Godzilla: as placas acendendo (o zumbido que sobe) e o raio atômico com o rugido."""
    x = _z(2.4)
    n = n_de(0.6)
    poe(x, seno(varre(100, 600, n), n) * sobe_e_some(n, 0.9, 1.0) * 0.05, 0.0)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.03), 1000, 5000, 0.006) * 0.4, 0.05 + 0.08 * k)
    m = n_de(1.2)
    t = _t(m)
    poe(x, satura(seno(varre(180, 120, m) * (1 + 0.04 * np.sin(2 * math.pi * 20 * t)), m) + passa(rosa(rng, m), 200, 3000, 2), 3) * env(m, 0.05, 0.8) * 0.1, 0.45)
    poe(x, graos(rng, n_de(0.8), 80, 0.0, 0.9, 2000, 9000, 0.002) * 0.3, 0.5)
    return reverb(x, 0.7, 0.35)


def explosoes(rng, v):
    """Bakugo: quatro explosões, cada uma maior que a outra."""
    x = _z(2.0)
    for k in range(4):
        n = n_de(0.3)
        poe(x, satura(passa(rosa(rng, n), 150, 6000, 2) * env(n, 0.001, 0.2), 2.5) * (0.35 + 0.15 * k), 0.05 + 0.18 * k)
        poe(x, _baque(110 - 15 * k, 40, 0.25, 0.3 + 0.15 * k, 2.4), 0.05 + 0.18 * k)
    return reverb(x, 0.5, 0.25)


def orgulho_youkai(rng, v):
    """Sesshomaru: a lua acendendo (o tom frio) e o chicote de luz."""
    x = _z(2.0)
    poe(x, _sino(rng, 1568, 0.8, 0.05, CRISTAL), 0.0)
    poe(x, _acorde((330, 392, 494), 0.7, 0.035, 0.1, 0.6), 0.05)
    n = n_de(0.4)
    poe(x, (seno(varre(1500, 2500, n), n) * 0.035 + passa(rosa(rng, n), 3000, 9000, 2) * 0.15) * env(n, 0.005, 0.3), 0.32)
    return reverb(x, 0.7, 0.35)


def reequipar(rng, v):
    """Erza: o clarão do reequipar e as espadas aparecendo em volta (os metais)."""
    x = _z(2.1)
    poe(x, _brilho(rng, 0.8, 2093, 0.05, CRISTAL), 0.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 2000, 9000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.25, 0.0)
    for k in range(8):
        poe(x, _sino(rng, 2000 + 150 * k, 0.3, 0.03, METAL), 0.3 + 0.04 * k)
    return reverb(x, 0.6, 0.3)


def furia_oni(rng, v):
    """Rem: o chifre de oni (o tom que sobe) e a bola de ferro girando na corrente."""
    x = _z(2.1)
    n = n_de(0.4)
    poe(x, seno(varre(300, 1200, n), n) * env(n, 0.02, 0.3) * 0.04, 0.0)
    m = n_de(0.7)
    t = _t(m)
    poe(x, passa(rosa(rng, m), 400, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 5 * t) ** 2) * env(m, 0.02, 0.5) * 0.3, 0.3)
    poe(x, _baque(80, 35, 0.5, 0.8, 2.8), 0.95)
    poe(x, _sino(rng, 700, 0.4, 0.05, METAL), 0.95)
    return reverb(x, 0.5, 0.25)


def jogador_solo(rng, v):
    """Kirito: as duas espadas saindo (os metais) e o brilho da conexão."""
    x = _z(2.0)
    for k in range(2):
        poe(x, _whoosh(rng, 0.15, 2000, 9000, 0.6, 1.4, 0.35), 0.05 + 0.12 * k)
        poe(x, _sino(rng, 3000 + 600 * k, 0.5, 0.05, METAL), 0.15 + 0.12 * k)
    poe(x, _brilho(rng, 0.7, 1760, 0.04, CRISTAL), 0.4)
    poe(x, _acorde((392, 494, 587, 784), 0.7, 0.035, 0.03, 0.5), 0.45)
    return reverb(x, 0.6, 0.3)


def plano_mestre(rng, v):
    """Megamente: o giz na lousa (os riscos), o plano e o riso malvado."""
    x = _z(2.1)
    for k in range(6):
        n = n_de(0.08)
        poe(x, passa(rosa(rng, n), 2500, 8000, 2) * env(n, 0.005, 0.06) * 0.25, 0.1 + 0.08 * k)
    poe(x, estalo(rng, n_de(0.03), 2000, 6000, 0.005), 0.7)
    for k in range(3):
        n = n_de(0.12)
        poe(x, satura(seno(varre(220, 180, n), n), 2) * env(n, 0.01, 0.1) * 0.06, 0.85 + 0.13 * k)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "mu-chifres-serrados": (chifres_serrados, "Hellboy: os chifres serrados"),
    "mu-omnitrix": (omnitrix, "Ben 10: o Omnitrix"),
    "mu-pista-gelo": (pista_gelo, "Gelado: a pista"),
    "mu-prodigio-instavel": (prodigio_instavel, "Azula: o prodígio"),
    "mu-penny": (penny, "Bugiganga: a Penny"),
    "mu-estica-jake": (estica_jake, "Jake: estica"),
    "mu-sempre-junto": (sempre_junto, "Robin: sempre junto"),
    "mu-rumble-ball": (rumble_ball, "Chopper: a Rumble Ball"),
    "mu-futuro-medico": (futuro_medico, "Leorio: o médico"),
    "mu-asas-protetoras": (asas_protetoras, "Ísis: as asas"),
    "mu-olho-de-horus": (olho_de_horus, "Hórus: o olho"),
    "mu-cheiro-de-sangue": (cheiro_de_sangue, "Sekhmet: o sangue"),
    "mu-implacavel": (implacavel, "Jason: implacável"),
    "mu-exercito": (exercito, "Rambo: o exército"),
    "mu-radiacao": (radiacao, "Godzilla: a radiação"),
    "mu-explosoes": (explosoes, "Bakugo: as explosões"),
    "mu-orgulho-youkai": (orgulho_youkai, "Sesshomaru: o orgulho"),
    "mu-reequipar": (reequipar, "Erza: reequipar"),
    "mu-furia-oni": (furia_oni, "Rem: a fúria"),
    "mu-jogador-solo": (jogador_solo, "Kirito: o solo"),
    "mu-plano-mestre": (plano_mestre, "Megamente: o plano"),
}
