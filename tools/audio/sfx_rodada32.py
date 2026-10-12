"""Os sons da rodada 32 das habilidades próprias (veja tools/vfx/familias_v2/rodada32.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, SR, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _quack(rng, f=420, seg=0.12, g=0.06):
    """A voz de pato (o "quack" rouco): a quadrada com o nasal e o ruído."""
    n = n_de(seg)
    return satura(seno(varre(f, f * 0.75, n), n) * (1 + 0.6 * np.sin(2 * math.pi * 55 * _t(n))) + passa(rosa(rng, n), 800, 3000, 2) * 0.4, 4) * env(n, 0.005, seg * 0.8) * g


# ------------------------------------------------------------------ Mickey

def chapeu_de_feiticeiro(rng, v):
    """Mickey: o chapéu de feiticeiro (a magia cintilando e o acorde encantado)."""
    x = _z(2.1)
    poe(x, graos(rng, n_de(0.8), 40, 0.0, 0.95, 2500, 9000, 0.003) * 0.35, 0.0)
    poe(x, _acorde((349, 440, 523, 698), 1.2, 0.03, 0.2, 0.9), 0.15)
    for k, f in enumerate((1047, 1319, 1568, 2093)):
        poe(x, _sino(rng, f, 0.5, 0.02, CRISTAL), 0.3 + 0.07 * k)
    return reverb(x, 0.8, 0.4)


def mickey_preparo(rng, v):
    """Mickey (Preparo): a luva acenando e o "hot dog!" (a musiquinha alegre em laço)."""
    x = _z(1.4)
    for k, f in enumerate((523, 659, 784, 659)):
        n = n_de(0.18)
        poe(x, (seno(f, n) + seno(f * 2, n) * 0.2) * env(n, 0.01, 0.15) * 0.035, 0.22 * k)
    poe(x, graos(rng, n_de(1.0), 15, 0.0, 0.95, 3000, 9000, 0.003) * 0.2, 0.0)
    return reverb(x, 0.5, 0.25)


def alegria_contagiante(rng, v):
    """Mickey: a risada "ha-ha!", as notas pulando e o confete estourando."""
    x = _z(2.1)
    for k, f in enumerate((880, 1047)):
        n = n_de(0.1)
        poe(x, seno(varre(f, f * 0.85, n), n) * env(n, 0.005, 0.08) * 0.045, 0.12 * k)
    for k, f in enumerate((523, 587, 659, 784, 1047)):
        n = n_de(0.1)
        poe(x, seno(f, n) * env(n, 0.005, 0.09) * 0.035, 0.15 + 0.07 * k)
    poe(x, _baque(200, 90, 0.2, 0.4), 0.5)
    poe(x, graos(rng, n_de(0.5), 40, 0.0, 0.9, 2000, 8000, 0.004) * 0.4, 0.52)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Pato Donald

def ataque_de_furia(rng, v):
    """Donald: a nuvem de briga (os "quack" bravos e os socos em todo lugar)."""
    x = _z(2.0)
    q = np.random.default_rng(4)
    for k in range(6):
        poe(x, _quack(rng, q.uniform(380, 520), 0.1, 0.05), 0.12 * k)
    for k in range(8):
        poe(x, _baque(q.uniform(130, 200), 70, 0.1, 0.4), 0.05 + 0.09 * k)
    poe(x, passa(rosa(rng, n_de(0.8)), 300, 2500, 2) * sobe_e_some(n_de(0.8), 0.3, 1.2) * 0.25, 0.0)
    return reverb(x, 0.4, 0.2)


def grito_indignado(rng, v):
    """Donald: o grito indignado (o "quack-quack-QUACK!" rouco e as ondas)."""
    x = _z(1.8)
    for k, f in enumerate((440, 470, 560)):
        poe(x, _quack(rng, f, 0.13 if k < 2 else 0.3, 0.06), 0.15 * k)
    poe(x, _whoosh(rng, 0.3, 300, 2500, 0.5, 1.4, 0.3), 0.3)
    return reverb(x, 0.4, 0.2)


def explosao_de_raiva(rng, v):
    """Donald: o vapor saindo da cabeça (o apito da chaleira) e a explosão de raiva."""
    x = _z(2.3)
    n = n_de(0.4)
    poe(x, (seno(varre(1800, 2600, n), n) * 0.5 + passa(rosa(rng, n), 3000, 9000, 2)) * env(n, 0.05, 0.1) * 0.1, 0.0)
    poe(x, _quack(rng, 520, 0.2, 0.06), 0.3)
    poe(x, _baque(55, 22, 0.9, 1.0, 3.2), 0.42)
    poe(x, _explosao(rng, 1.0, 55), 0.42)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Pateta

def tropecao_do_pateta(rng, v):
    """Pateta: o escorregão (o "zíííp"), o tombo e as estrelinhas."""
    x = _z(1.9)
    poe(x, _piu(600, 1800, 0.18, 0.04), 0.0)
    poe(x, _baque(130, 55, 0.4, 0.7, 2.2), 0.3)
    poe(x, estalo(rng, n_de(0.05), 500, 3000, 0.01) * 0.6, 0.3)
    for k in range(3):
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.02, CRISTAL), 0.5 + 0.07 * k)
    return reverb(x, 0.4, 0.2)


def ai_ai_ai(rng, v):
    """Pateta: o grito "a-ai-ai-uuuuu!" caindo em espiral e o tombo enorme."""
    x = _z(2.0)
    n = n_de(0.55)
    t = _t(n)
    f = 900 - 500 * t / t[-1]
    fase = 2 * math.pi * np.cumsum(f * (1 + 0.04 * np.sin(2 * math.pi * 7 * t))) / SR
    poe(x, satura(np.sin(fase) + 0.3 * np.sin(2 * fase), 2) * env(n, 0.03, 0.2) * 0.05, 0.0)
    poe(x, _baque(60, 25, 0.8, 1.0, 3.0), 0.52)
    poe(x, estalo(rng, n_de(0.08), 300, 3000, 0.02) * 0.6, 0.52)
    for k in range(3):
        poe(x, _sino(rng, 1568 + 220 * k, 0.3, 0.02, CRISTAL), 0.65 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


def pateta_preparo(rng, v):
    """Pateta (Preparo): se equilibrando (o "uou-uou" e o chapéu balançando)."""
    x = _z(1.4)
    for k in range(3):
        poe(x, _piu(400 + 60 * (k % 2), 300, 0.2, 0.035), 0.3 * k)
    n = n_de(1.0)
    poe(x, seno(180, n) * (0.6 + 0.4 * np.sin(2 * math.pi * 1.5 * _t(n))) * sobe_e_some(n, 0.5, 1.2) * 0.02, 0.0)
    return reverb(x, 0.4, 0.2)


def acidente_feliz(rng, v):
    """Pateta: o assobio do piano caindo e o "BLAMMM" desafinado das teclas."""
    x = _z(2.3)
    n = n_de(0.4)
    poe(x, seno(varre(1600, 500, n), n) * env(n, 0.02, 0.35) * 0.04, 0.05)
    poe(x, _baque(60, 25, 0.8, 1.0, 3.0), 0.43)
    poe(x, _acorde((131, 139, 196, 208, 262, 277), 1.4, 0.05, 0.005, 1.2), 0.43)
    poe(x, estalo(rng, n_de(0.1), 300, 3000, 0.02) * 0.6, 0.43)
    for k in range(3):
        poe(x, _sino(rng, 1568 + 220 * k, 0.3, 0.02, CRISTAL), 0.7 + 0.08 * k)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Stitch

def quatro_bracos(rng, v):
    """Stitch: os quatro braços arranhando ao mesmo tempo."""
    x = _z(1.8)
    for k in range(4):
        poe(x, _whoosh(rng, 0.1, 2500, 10000, 0.5, 1.3, 0.35), 0.05 + 0.07 * k)
        poe(x, passa(rosa(rng, n_de(0.08)), 2000, 8000, 2) * env(n_de(0.08), 0.003, 0.07) * 0.4, 0.12 + 0.07 * k)
    poe(x, _baque(150, 70, 0.25, 0.5), 0.3)
    return reverb(x, 0.4, 0.2)


def mordida_de_stitch(rng, v):
    """Stitch: o rosnado alienígena e as mordidas em todos."""
    x = _z(1.9)
    n = n_de(0.4)
    poe(x, satura(seno(varre(160, 120, n), n) + passa(rosa(rng, n), 100, 1500, 2) * 0.7, 4) * (0.6 + 0.4 * np.sin(2 * math.pi * 25 * _t(n))) * env(n, 0.05, 0.3) * 0.06, 0.0)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.05), 600, 4000, 0.01), 0.38 + 0.06 * k)
        poe(x, _baque(170, 80, 0.12, 0.35), 0.38 + 0.06 * k)
    return reverb(x, 0.4, 0.2)


def stitch_preparo(rng, v):
    """Stitch (Preparo): as pistolas de plasma carregando (o zumbido que pulsa)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(varre(300, 700, n), n) + seno(varre(450, 1050, n), n) * 0.5) * (0.6 + 0.4 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(n, 0.7, 1.2) * 0.035, 0.0)
    poe(x, graos(rng, n, 20, 0.0, 0.95, 2000, 7000, 0.003) * 0.2, 0.0)
    return reverb(x, 0.5, 0.25)


def experimento_626(rng, v):
    """Stitch: a rajada das pistolas de plasma ("piu-piu-piu") e o impacto."""
    x = _z(2.0)
    for k in range(8):
        poe(x, _piu(1800 - 50 * k, 500, 0.08, 0.035), 0.03 * k)
    poe(x, _baque(110, 45, 0.5, 0.8, 2.6), 0.25)
    poe(x, _explosao(rng, 0.5, 70), 0.25)
    poe(x, _brilho(rng, 0.5, 1319, 0.03, CRISTAL), 0.3)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Buzz Lightyear

def laser_do_braco(rng, v):
    """Buzz: o "bip" da mira e o laser do braço (o zumbido vermelho pulsando)."""
    x = _z(1.9)
    for k in range(2):
        n = n_de(0.06)
        poe(x, seno(2000, n) * env(n, 0.003, 0.05) * 0.03, 0.05 + 0.1 * k)
    n = n_de(0.55)
    t = _t(n)
    poe(x, (_quadrada(880, n) * 0.4 + seno(880, n)) * (0.6 + 0.4 * np.sin(2 * math.pi * 30 * t)) * env(n, 0.01, 0.2) * 0.035, 0.25)
    poe(x, _brilho(rng, 0.4, 1760, 0.025, CRISTAL), 0.3)
    return reverb(x, 0.4, 0.2)


def modo_de_combate(rng, v):
    """Buzz: as asas abrindo com o estalo ("tchic!") e o pulso que atrapalha o Preparo."""
    x = _z(1.9)
    poe(x, estalo(rng, n_de(0.05), 1500, 6000, 0.008), 0.0)
    poe(x, _sino(rng, 1319, 0.3, 0.03, METAL), 0.02)
    poe(x, estalo(rng, n_de(0.05), 1500, 6000, 0.008), 0.08)
    for k in range(3):
        n = n_de(0.25)
        poe(x, seno(varre(600, 200, n), n) * env(n, 0.005, 0.2) * 0.05, 0.25 + 0.08 * k)
    poe(x, passa(rosa(rng, n_de(0.3)), 2000, 9000, 2) * env(n_de(0.3), 0.005, 0.25) * 0.25, 0.5)
    return reverb(x, 0.5, 0.25)


def buzz_preparo(rng, v):
    """Buzz (Preparo): o foguete das costas acendendo (o ronco que cresce)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 100, 1500, 2) * sobe_e_some(n, 0.7, 1.2) * 0.3, 0.0)
    poe(x, seno(varre(200, 400, n), n) * sobe_e_some(n, 0.7, 1.2) * 0.02, 0.0)
    return reverb(x, 0.4, 0.2)


def ao_infinito_e_alem(rng, v):
    """Buzz: "Ao infinito e além!" — o foguete, a fanfarra espacial e o impacto."""
    x = _z(2.4)
    poe(x, _whoosh(rng, 0.45, 300, 6000, 0.8, 1.4, 0.6), 0.0)
    poe(x, passa(rosa(rng, n_de(0.4)), 100, 1500, 2) * env(n_de(0.4), 0.02, 0.35) * 0.4, 0.0)
    poe(x, _acorde((392, 523, 659, 784), 1.0, 0.04, 0.03, 0.8), 0.35)
    poe(x, _baque(80, 30, 0.7, 0.9, 2.8), 0.4)
    poe(x, _explosao(rng, 0.7, 60), 0.4)
    poe(x, _brilho(rng, 0.6, 2093, 0.03, CRISTAL), 0.45)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Woody

def plano_do_xerife(rng, v):
    """Woody: "Tem uma cobra na minha bota!" — o violão de faroeste e a estrela de xerife."""
    x = _z(2.0)
    for k, f in enumerate((196, 247, 294, 392)):
        poe(x, _sino(rng, f, 0.7, 0.03, METAL), 0.04 * k)
    poe(x, _sino(rng, 1568, 0.6, 0.04, SINO), 0.3)
    poe(x, _brilho(rng, 0.6, 1175, 0.03, CRISTAL), 0.35)
    poe(x, _sopro(rng, 0.6, 200, 1500, 0.1, 0.3), 0.35)
    return reverb(x, 0.5, 0.25)


def woody_preparo(rng, v):
    """Woody (Preparo): a cordinha das costas sendo puxada (o "zíííp" e o clique)."""
    x = _z(1.4)
    for k in range(2):
        n = n_de(0.3)
        poe(x, passa(rosa(rng, n), 1500, 6000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 60 * _t(n)) ** 2) * env(n, 0.02, 0.25) * 0.2, 0.05 + 0.6 * k)
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.004) * 0.5, 0.38 + 0.6 * k)
    return reverb(x, 0.3, 0.15)


def todos_juntos(rng, v):
    """Woody: o laço de corda girando e o acorde de amizade no trio."""
    x = _z(2.2)
    n = n_de(0.45)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 400, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 10 * t) ** 2) * env(n, 0.02, 0.4) * 0.25, 0.0)
    poe(x, _acorde((262, 330, 392, 523), 1.2, 0.04, 0.05, 0.9), 0.4)
    for k in range(3):
        poe(x, _sino(rng, 1568 + 196 * k, 0.4, 0.02, CRISTAL), 0.5 + 0.08 * k)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "chapeu-de-feiticeiro": (chapeu_de_feiticeiro, "Mickey: o chapéu de feiticeiro"),
    "mickey-preparo": (mickey_preparo, "Mickey: a luva acenando (Preparo)"),
    "alegria-contagiante": (alegria_contagiante, "Mickey: a alegria contagiante"),
    "ataque-de-furia": (ataque_de_furia, "Pato Donald: o ataque de fúria"),
    "grito-indignado": (grito_indignado, "Pato Donald: o grito indignado"),
    "explosao-de-raiva": (explosao_de_raiva, "Pato Donald: a explosão de raiva"),
    "tropecao-do-pateta": (tropecao_do_pateta, "Pateta: o tropeção"),
    "ai-ai-ai": (ai_ai_ai, "Pateta: Ai-ai-ai!"),
    "pateta-preparo": (pateta_preparo, "Pateta: se equilibrando (Preparo)"),
    "acidente-feliz": (acidente_feliz, "Pateta: o acidente feliz"),
    "quatro-bracos": (quatro_bracos, "Stitch: os quatro braços"),
    "mordida-de-stitch": (mordida_de_stitch, "Stitch: a mordida"),
    "stitch-preparo": (stitch_preparo, "Stitch: as pistolas carregando (Preparo)"),
    "experimento-626": (experimento_626, "Stitch: Experimento 626"),
    "laser-do-braco": (laser_do_braco, "Buzz Lightyear: o laser do braço"),
    "modo-de-combate": (modo_de_combate, "Buzz Lightyear: o modo de combate"),
    "buzz-preparo": (buzz_preparo, "Buzz Lightyear: o foguete acendendo (Preparo)"),
    "ao-infinito-e-alem": (ao_infinito_e_alem, "Buzz Lightyear: Ao infinito e além!"),
    "plano-do-xerife": (plano_do_xerife, "Woody: o plano do xerife"),
    "woody-preparo": (woody_preparo, "Woody: a cordinha (Preparo)"),
    "todos-juntos": (todos_juntos, "Woody: todos juntos"),
}
