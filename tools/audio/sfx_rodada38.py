"""Os sons da rodada 38 das habilidades próprias (veja tools/vfx/familias_v2/rodada38.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _estrelinhas(rng, x, em, n=3):
    for k in range(n):
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.02, CRISTAL), em + 0.07 * k)


def _blablabla(rng, seg, f=260, g=0.04):
    """A fala sem fim (as sílabas abafadas subindo e descendo)."""
    x = _z(seg + 0.2)
    q = np.random.default_rng(5)
    t0 = 0.0
    while t0 < seg:
        d = q.uniform(0.06, 0.12)
        n = n_de(d)
        fr = f * q.uniform(0.85, 1.25)
        poe(x, passa(_quadrada(fr, n) * 0.5 + seno(fr, n), 200, 1500, 2) * env(n, 0.005, d * 0.6) * g, t0)
        t0 += d + 0.02
    return x


def _gelo(rng, n_cristais=6, g=0.03):
    x = _z(0.6)
    q = np.random.default_rng(9)
    for k in range(n_cristais):
        poe(x, _sino(rng, q.uniform(2500, 4500), 0.2, g, CRISTAL), 0.06 * k)
        poe(x, estalo(rng, n_de(0.02), 3000, 9000, 0.004) * 0.4, 0.06 * k)
    return x


# ------------------------------------------------------------------ Macaco Louco

def robo_gigante_mojo(rng, v):
    """Macaco Louco: o robô gigante (os servos, o punho descendo e o estrondo)."""
    x = _z(2.2)
    n = n_de(0.3)
    poe(x, satura(seno(varre(120, 300, n), n), 3) * env(n, 0.02, 0.25) * 0.04, 0.0)
    poe(x, _whoosh(rng, 0.3, 150, 2000, 0.9, 1.3, 0.5), 0.05)
    poe(x, _baque(50, 20, 1.0, 1.0, 3.2), 0.3)
    poe(x, _explosao(rng, 0.8, 50), 0.3)
    poe(x, _sino(rng, 196, 0.8, 0.05, METAL), 0.32)
    return reverb(x, 0.6, 0.3)


def raio_adaptador(rng, v):
    """Macaco Louco: o capacete zumbindo, o raio colorido e o escudo no aliado."""
    x = _z(2.0)
    n = n_de(0.5)
    t = _t(n)
    poe(x, (seno(varre(500, 1500, n), n) + seno(varre(750, 2250, n), n) * 0.4) * (0.7 + 0.3 * np.sin(2 * math.pi * 25 * t)) * env(n, 0.02, 0.2) * 0.035, 0.12)
    poe(x, _baque(150, 70, 0.2, 0.45), 0.3)
    poe(x, _sino(rng, 880, 0.5, 0.03, METAL), 0.5)
    poe(x, _brilho(rng, 0.5, 1319, 0.025, CRISTAL), 0.55)
    return reverb(x, 0.5, 0.25)


def mojo_preparo(rng, v):
    """Macaco Louco (Preparo): o discurso começando (o blá-blá-blá em laço)."""
    x = _z(1.4)
    poe(x, _blablabla(rng, 1.0, 320, 0.035), 0.05)
    return reverb(x, 0.4, 0.2)


def discurso_interminavel(rng, v):
    """Macaco Louco: o discurso que não acaba (o falatório) e o bocejo dos rivais."""
    x = _z(2.4)
    poe(x, _blablabla(rng, 1.4, 300, 0.04), 0.0)
    n = n_de(0.6)
    poe(x, seno(varre(400, 200, n), n) * env(n, 0.15, 0.3) * 0.025, 1.1)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Capitão Planeta

def poder_dos_aneis(rng, v):
    """Capitão Planeta: os cinco anéis ("Terra! Fogo! Vento! Água! Coração!") e o escudo."""
    x = _z(2.2)
    for k, f in enumerate((392, 440, 494, 587, 659)):
        poe(x, _sino(rng, f, 0.5, 0.035, SINO), 0.06 * k)
        poe(x, _piu(f * 2, f * 2.5, 0.08, 0.015), 0.06 * k)
    poe(x, _acorde((294, 370, 440, 587), 1.0, 0.035, 0.1, 0.8), 0.45)
    poe(x, _brilho(rng, 0.6, 1568, 0.025, CRISTAL), 0.6)
    return reverb(x, 0.7, 0.35)


def forca_da_natureza(rng, v):
    """Capitão Planeta: o redemoinho de folhas (o farfalhar) e as raízes rompendo o chão."""
    x = _z(2.1)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 9 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.25, 0.0)
    for k in range(4):
        poe(x, satura(passa(rosa(rng, n_de(0.12)), 100, 1200, 2), 2) * env(n_de(0.12), 0.005, 0.1) * 0.35, 0.4 + 0.05 * k)
        poe(x, estalo(rng, n_de(0.03), 500, 3000, 0.008) * 0.6, 0.4 + 0.05 * k)
    poe(x, _baque(90, 40, 0.3, 0.5), 0.4)
    return reverb(x, 0.5, 0.25)


def capitao_preparo(rng, v):
    """Capitão Planeta (Preparo): os cinco raios se juntando (o acorde crescendo em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    for k, f in enumerate((196, 247, 294, 392, 494)):
        poe(x, seno(f, n) * sobe_e_some(n, 0.3 + 0.1 * k, 1.2) * 0.012, 0.0)
    poe(x, graos(rng, n, 25, 0.0, 0.95, 2000, 8000, 0.003) * 0.25, 0.0)
    return reverb(x, 0.6, 0.3)


def o_poder_e_de_voces(rng, v):
    """Capitão Planeta: "O poder é de vocês!" — a fanfarra heroica, a cura e o golpe."""
    x = _z(2.4)
    for k, f in enumerate((262, 330, 392, 523)):
        n = n_de(0.15 if k < 3 else 0.6)
        poe(x, satura(seno(f, n) + seno(f * 1.5, n) * 0.35, 2) * env(n, 0.01, 0.12 if k < 3 else 0.5) * 0.04, 0.12 * k)
    poe(x, _acorde((392, 494, 587, 784), 1.0, 0.03, 0.1, 0.8), 0.5)
    poe(x, _whoosh(rng, 0.3, 500, 5000, 0.8, 1.4, 0.4), 0.4)
    poe(x, _baque(110, 45, 0.4, 0.7), 0.6)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Inspetor Bugiganga

def braco_extensivel(rng, v):
    """Bugiganga: "Bugiganga braço!" — os gomos estendendo (o tléc-tléc) e a garra prendendo."""
    x = _z(2.0)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.025), 1500, 6000, 0.005) * 0.7, 0.05 * k)
        poe(x, _sino(rng, 880 + 110 * k, 0.15, 0.015, METAL), 0.05 * k)
    poe(x, _baque(200, 100, 0.1, 0.4), 0.42)
    poe(x, _sino(rng, 523, 0.4, 0.04, METAL), 0.42)
    return reverb(x, 0.4, 0.2)


def bugiganga_preparo(rng, v):
    """Bugiganga (Preparo): o chapéu abrindo e a hélice girando (o "vupt-vupt")."""
    x = _z(1.4)
    poe(x, estalo(rng, n_de(0.04), 1000, 4000, 0.008), 0.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * (0.4 + 0.6 * np.sin(2 * math.pi * 14 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.25, 0.05)
    return reverb(x, 0.4, 0.2)


def vai_vai_bugiganga(rng, v):
    """Bugiganga: as engenhocas saindo para todo lado (molas, buzinas, guarda-chuvas) e a bagunça."""
    x = _z(2.3)
    q = np.random.default_rng(6)
    for k in range(9):
        tipo = k % 3
        em = 0.03 * k + q.uniform(0, 0.05)
        if tipo == 0:
            n = n_de(0.25)
            poe(x, seno(varre(250, 600, n), n) * (1 + 0.6 * np.sin(2 * math.pi * 25 * _t(n))) * env(n, 0.005, 0.2) * 0.035, em)
        elif tipo == 1:
            poe(x, passa(rosa(rng, n_de(0.1)), 600, 4000, 2) * env(n_de(0.1), 0.005, 0.08) * 0.3, em)
        else:
            n = n_de(0.15)
            poe(x, _quadrada(440, n) * env(n, 0.005, 0.12) * 0.02, em)
    poe(x, _baque(120, 50, 0.4, 0.7), 0.45)
    _estrelinhas(rng, x, 0.6)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Danny Phantom

def intangibilidade(rng, v):
    """Danny Phantom: ficando intangível (o "uuu" fantasma ondulado) e o escudo no aliado."""
    x = _z(2.0)
    n = n_de(0.8)
    t = _t(n)
    poe(x, seno(600 + 80 * np.sin(2 * math.pi * 5 * t), n) * sobe_e_some(n, 0.3, 1.2) * 0.03, 0.0)
    poe(x, _sopro(rng, 0.8, 1000, 5000, 0.12, 0.3), 0.0)
    poe(x, _sino(rng, 1047, 0.5, 0.03, CRISTAL), 0.45)
    return reverb(x, 0.8, 0.4)


def danny_preparo(rng, v):
    """Danny Phantom (Preparo): "Hora de virar fantasma!" — os anéis da transformação passando."""
    x = _z(1.4)
    for k in range(2):
        n = n_de(0.5)
        poe(x, seno(varre(300, 900, n), n) * env(n, 0.1, 0.3) * 0.03, 0.6 * k)
        poe(x, _sopro(rng, 0.5, 1500, 6000, 0.1, 0.5), 0.6 * k)
    return reverb(x, 0.6, 0.3)


def lamento_fantasma(rng, v):
    """Danny Phantom: o lamento fantasma (o grito enorme com eco e o vento)."""
    x = _z(2.4)
    n = n_de(1.0)
    t = _t(n)
    f = 400 + 200 * np.sin(2 * math.pi * 0.8 * t) + 20 * np.sin(2 * math.pi * 7 * t)
    poe(x, satura(seno(f, n) + 0.5 * seno(f * 1.5, n), 2.5) * sobe_e_some(n, 0.15, 1.2) * 0.05, 0.05)
    poe(x, passa(rosa(rng, n), 300, 4000, 2) * sobe_e_some(n, 0.2, 1.2) * 0.35, 0.05)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Coragem

def grito_de_pavor(rng, v):
    """Coragem: o grito de pavor ("AAAAH!" tremido) e o carinho no aliado."""
    x = _z(2.0)
    n = n_de(0.6)
    t = _t(n)
    f = 900 * (1 + 0.08 * np.sin(2 * math.pi * 18 * t)) * (1 + 0.2 * t / t[-1])
    poe(x, satura(seno(f, n) + 0.4 * seno(f * 2, n), 2.5) * env(n, 0.02, 0.4) * 0.045, 0.0)
    poe(x, _acorde((392, 494, 587), 0.8, 0.03, 0.05, 0.6), 0.5)
    return reverb(x, 0.5, 0.25)


def correr_para_o_perigo(rng, v):
    """Coragem: os passinhos correndo tremidos e a bolha de proteção no trio."""
    x = _z(2.0)
    for k in range(12):
        poe(x, _baque(300 + 40 * (k % 2), 180, 0.03, 0.15), 0.035 * k)
    poe(x, _piu(700, 1100, 0.1, 0.03), 0.2)
    n = n_de(0.6)
    poe(x, seno(varre(300, 600, n), n) * env(n, 0.1, 0.4) * 0.025, 0.45)
    poe(x, _brilho(rng, 0.6, 1175, 0.03, CRISTAL), 0.5)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Senhor Frio

def pistola_de_gelo(rng, v):
    """Senhor Frio: o jato da pistola congelante e o gelo estalando em volta do rival."""
    x = _z(2.0)
    n = n_de(0.45)
    poe(x, passa(rosa(rng, n), 2500, 10000, 2) * env(n, 0.02, 0.3) * 0.35, 0.08)
    poe(x, seno(varre(2000, 1400, n), n) * env(n, 0.02, 0.3) * 0.015, 0.08)
    poe(x, _gelo(rng, 7, 0.03), 0.35)
    poe(x, estalo(rng, n_de(0.08), 1000, 6000, 0.012) * 0.8, 0.4)
    return reverb(x, 0.6, 0.3)


def armadura_de_gelo(rng, v):
    """Senhor Frio: as placas de cristal de gelo encaixando e a névoa fria."""
    x = _z(2.0)
    for k in range(10):
        poe(x, _sino(rng, 2093 + 150 * (k % 4), 0.25, 0.02, CRISTAL), 0.04 * k)
        poe(x, estalo(rng, n_de(0.02), 3000, 9000, 0.004) * 0.5, 0.04 * k)
    poe(x, _sopro(rng, 1.0, 1500, 6000, 0.12, 0.4), 0.1)
    return reverb(x, 0.7, 0.35)


def frio_preparo(rng, v):
    """Senhor Frio (Preparo): o traje chiando e a pistola carregando (o frio em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 1.5 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.15, 0.0)
    poe(x, seno(varre(600, 1200, n), n) * sobe_e_some(n, 0.8, 1.2) * 0.015, 0.0)
    return reverb(x, 0.6, 0.3)


def zero_absoluto_frio(rng, v):
    """Senhor Frio: a onda de frio absoluto (o vento gelado) e tudo congelando."""
    x = _z(2.4)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 600, 6000, 2) * sobe_e_some(n, 0.2, 1.2) * 0.4, 0.0)
    poe(x, seno(varre(200, 80, n), n) * sobe_e_some(n, 0.2, 1.2) * 0.04, 0.0)
    poe(x, _gelo(rng, 8, 0.03), 0.45)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.06), 1000, 6000, 0.01) * 0.7, 0.5 + 0.05 * k)
    return reverb(x, 0.8, 0.4)


SONS: dict = {
    "robo-gigante-mojo": (robo_gigante_mojo, "Macaco Louco: o robô gigante"),
    "raio-adaptador": (raio_adaptador, "Macaco Louco: o raio adaptador"),
    "mojo-preparo": (mojo_preparo, "Macaco Louco: o discurso começando (Preparo)"),
    "discurso-interminavel": (discurso_interminavel, "Macaco Louco: o discurso interminável"),
    "poder-dos-aneis": (poder_dos_aneis, "Capitão Planeta: o poder dos anéis"),
    "forca-da-natureza": (forca_da_natureza, "Capitão Planeta: a força da natureza"),
    "capitao-preparo": (capitao_preparo, "Capitão Planeta: os raios se juntando (Preparo)"),
    "o-poder-e-de-voces": (o_poder_e_de_voces, "Capitão Planeta: O poder é de vocês"),
    "braco-extensivel": (braco_extensivel, "Inspetor Bugiganga: o braço extensível"),
    "bugiganga-preparo": (bugiganga_preparo, "Inspetor Bugiganga: o chapéu-hélice (Preparo)"),
    "vai-vai-bugiganga": (vai_vai_bugiganga, "Inspetor Bugiganga: Vai, vai, Bugiganga!"),
    "intangibilidade": (intangibilidade, "Danny Phantom: a intangibilidade"),
    "danny-preparo": (danny_preparo, "Danny Phantom: a transformação (Preparo)"),
    "lamento-fantasma": (lamento_fantasma, "Danny Phantom: o lamento fantasma"),
    "grito-de-pavor": (grito_de_pavor, "Coragem: o grito de pavor"),
    "correr-para-o-perigo": (correr_para_o_perigo, "Coragem: correr para o perigo"),
    "pistola-de-gelo": (pistola_de_gelo, "Senhor Frio: a pistola de gelo"),
    "armadura-de-gelo": (armadura_de_gelo, "Senhor Frio: a armadura de gelo"),
    "frio-preparo": (frio_preparo, "Senhor Frio: a pistola carregando (Preparo)"),
    "zero-absoluto-frio": (zero_absoluto_frio, "Senhor Frio: o zero absoluto"),
}
