"""Os sons da rodada 14 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_o.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def tita(rng, v):
    """King Kong: os punhos batendo no peito (quatro baques ocos) e o rugido."""
    x = _z(2.0)
    for k in range(4):
        poe(x, _baque(90, 50, 0.3, 0.7, 2.4), 0.08 + 0.12 * k)
        poe(x, passa(rosa(rng, n_de(0.1)), 100, 800, 2) * env(n_de(0.1), 0.002, 0.08) * 0.4, 0.08 + 0.12 * k)
    n = n_de(0.9)
    t = _t(n)
    poe(x, satura(seno(varre(110, 70, n) * (1 + 0.04 * np.sin(2 * math.pi * 25 * t)), n) + passa(rosa(rng, n), 100, 1500, 2) * 0.8, 3) * env(n, 0.05, 0.6) * 0.1, 0.6)
    return reverb(x, 0.6, 0.3)


def cebola(rng, v):
    """Shrek: as camadas descascando (os estalos úmidos) e o arroto grave."""
    x = _z(1.9)
    for k in range(4):
        n = n_de(0.12)
        poe(x, passa(rosa(rng, n), 500, 3000, 2) * env(n, 0.005, 0.08) * 0.35, 0.1 + 0.12 * k)
    m = n_de(0.6)
    t = _t(m)
    poe(x, satura(seno(varre(90, 70, m) * (1 + 0.08 * np.sin(2 * math.pi * 18 * t)), m), 3) * env(m, 0.03, 0.4) * 0.1, 0.75)
    return reverb(x, 0.4, 0.2)


def livre_estou(rng, v):
    """Elsa: o gelo se formando (os cristais) e o acorde que sobe, livre."""
    x = _z(2.2)
    n = n_de(1.4)
    poe(x, graos(rng, n, 80, 0.0, 0.9, 4000, 11000, 0.004) * 0.35, 0.0)
    poe(x, _brilho(rng, 1.2, 1568, 0.04, CRISTAL), 0.1)
    for k, f in enumerate((440, 554, 659, 880)):
        poe(x, _sino(rng, f * 2, 0.8, 0.04, CRISTAL), 0.2 + 0.12 * k)
    poe(x, _acorde((440, 554, 659, 880), 1.2, 0.04, 0.2, 0.7), 0.6)
    poe(x, _sopro(rng, 1.0, 2000, 8000, 0.12, 0.4), 0.3)
    return reverb(x, 0.8, 0.4)


def dragao_malevola(rng, v):
    """Malévola: o riso sombrio (o acorde menor) e o sopro de fogo do dragão."""
    x = _z(2.2)
    poe(x, _acorde((147, 175, 208, 294), 0.9, 0.05, 0.1, 0.6), 0.0)
    poe(x, _whoosh(rng, 0.4, 300, 2000, 0.8, 1.4, 0.5), 0.3)
    n = n_de(1.0)
    poe(x, satura(passa(rosa(rng, n), 150, 3000, 2), 2.5) * sobe_e_some(n, 0.2, 1.4) * 0.35, 0.4)
    m = n_de(0.8)
    poe(x, satura(seno(varre(120, 80, m), m), 3) * env(m, 0.05, 0.5) * 0.08, 0.4)
    return reverb(x, 0.6, 0.3)


def desejo(rng, v):
    """Gênio: a lâmpada esfregada (o chiado), a fumaça subindo e o brilho mágico."""
    x = _z(2.2)
    for k in range(3):
        n = n_de(0.1)
        poe(x, passa(rosa(rng, n), 2000, 7000, 2) * env(n, 0.01, 0.06) * 0.25, 0.04 + 0.08 * k)
    poe(x, _sopro(rng, 0.8, 400, 3000, 0.3, 0.4), 0.25)
    m = n_de(0.7)
    poe(x, seno(varre(300, 900, m), m) * sobe_e_some(m, 0.6, 1.4) * 0.04, 0.3)
    poe(x, _brilho(rng, 1.0, 2349, 0.05, CRISTAL), 0.55)
    poe(x, _acorde((523, 659, 784, 1047), 0.9, 0.035, 0.05, 0.6), 0.6)
    return reverb(x, 0.7, 0.35)


def hienas(rng, v):
    """Scar: as risadas das hienas no escuro e as garras."""
    x = _z(2.0)
    q = np.random.default_rng(9)
    for k in range(8):
        n = n_de(0.08)
        f = q.uniform(600, 1000)
        poe(x, satura(seno(varre(f, f * 0.8, n), n), 2) * env(n, 0.005, 0.06) * 0.05, 0.05 + 0.06 * k + q.uniform(0, 0.03))
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 2000, 8000, 0.6, 1.4, 0.4), 0.55 + 0.08 * k)
        poe(x, estalo(rng, n_de(0.03), 2000, 6000, 0.006) * 0.5, 0.65 + 0.08 * k)
    return reverb(x, 0.5, 0.25)


def presentes(rng, v):
    """Jack Esqueleto: os sininhos de Natal tortos e os presentes caindo."""
    x = _z(2.1)
    for k, f in enumerate((659, 622, 659, 494, 587)):
        poe(x, _sino(rng, f * 2, 0.3, 0.035, SINO), 0.05 + 0.12 * k)
    for k in range(3):
        poe(x, _baque(200, 120, 0.15, 0.3), 0.8 + 0.1 * k)
    n = n_de(0.8)
    poe(x, (seno(98, n) + seno(117, n)) * env(n, 0.05, 0.5) * 0.04, 0.2)
    return reverb(x, 0.7, 0.35)


def voz_roubada(rng, v):
    """Úrsula: a voz cantando (o tom puro) puxada para dentro da concha e o riso grave."""
    x = _z(2.2)
    n = n_de(0.8)
    t = _t(n)
    poe(x, seno(880 * (1 + 0.01 * np.sin(2 * math.pi * 5 * t)), n) * env(n, 0.05, 0.6) * 0.05, 0.0)
    m = n_de(0.5)
    poe(x, seno(varre(880, 300, m, 0.6), m) * env(m, 0.005, 0.4) * 0.05, 0.55)
    poe(x, _sopro(rng, 0.5, 400, 2500, 0.25, 0.7), 0.4)
    poe(x, _sino(rng, 523, 0.6, 0.05, CRISTAL), 0.95)
    for k in range(3):
        o = n_de(0.15)
        poe(x, satura(seno(varre(130, 110, o), o), 2) * env(o, 0.01, 0.12) * 0.07, 1.05 + 0.13 * k)
    return reverb(x, 0.7, 0.35)


def one_for_all(rng, v):
    """Deku: os raios verdes estalando no corpo e a força subindo (o tom que cresce)."""
    x = _z(2.0)
    n = n_de(1.3)
    poe(x, graos(rng, n, 160, 0.0, 0.9, 2500, 10000, 0.0015) * 0.45, 0.0)
    m = n_de(1.0)
    poe(x, satura(seno(varre(110, 330, m), m), 2) * sobe_e_some(m, 0.8, 1.2) * 0.07, 0.1)
    for k in range(5):
        poe(x, seno(440 * 2 ** (k / 5), n_de(0.08)) * env(n_de(0.08), 0.005, 0.06) * 0.04, 0.25 + 0.1 * k)
    return reverb(x, 0.5, 0.25)


def plus_ultra(rng, v):
    """All Might: o soco (o estrondo enorme) e o tornado de vento."""
    x = _z(2.3)
    poe(x, _whoosh(rng, 0.3, 300, 3000, 0.9, 1.3, 0.5), 0.0)
    poe(x, _explosao(rng, 1.2, 0.9), 0.28)
    poe(x, _baque(70, 30, 0.6, 0.9, 2.8), 0.28)
    n = n_de(1.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 2500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 7 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.4, 0.35)
    return reverb(x, 0.6, 0.3)


def choque_termico(rng, v):
    """Todoroki: o gelo estalando de um lado, o fogo do outro e o vapor chiando."""
    x = _z(2.1)
    n = n_de(0.5)
    poe(x, graos(rng, n, 50, 0.0, 0.8, 3000, 10000, 0.004) * 0.4, 0.0)
    for k in range(3):
        poe(x, _sino(rng, 2600 + 400 * k, 0.3, 0.03, VIDRO), 0.05 + 0.1 * k)
    m = n_de(0.8)
    poe(x, satura(passa(rosa(rng, m), 150, 2500, 2), 2) * sobe_e_some(m, 0.3, 1.3) * 0.3, 0.1)
    o = n_de(1.0)
    poe(x, passa(rosa(rng, o), 3000, 10000, 2) * sobe_e_some(o, 0.25, 1.4) * 0.35, 0.4)
    return reverb(x, 0.6, 0.3)


def cem_por_cento(rng, v):
    """Mob: o estouro psíquico de 100% (o acorde que racha) e os destroços."""
    x = _z(2.3)
    m = n_de(0.4)
    poe(x, seno(varre(200, 1600, m, 2), m) * sobe_e_some(m, 0.95, 1.0) * 0.05, 0.0)
    poe(x, _explosao(rng, 1.2, 0.8), 0.35)
    poe(x, _acorde((110, 165, 233, 330, 466), 1.4, 0.06, 0.01, 1.0), 0.35)
    q = np.random.default_rng(4)
    for k in range(8):
        poe(x, _baque(q.uniform(150, 300), 80, 0.12, 0.2), 0.7 + q.uniform(0, 0.8))
    return reverb(x, 0.7, 0.35)


def imune(rng, v):
    """Rimuru: o slime balançando (o som molhado) e o Grande Sábio analisando (os bipes)."""
    x = _z(2.0)
    for k in range(3):
        n = n_de(0.2)
        poe(x, seno(varre(200, 320, n), n) * env(n, 0.02, 0.15) * 0.06, 0.05 + 0.15 * k)
    for k in range(5):
        poe(x, seno(1600 + 200 * (k % 2), n_de(0.06)) * env(n_de(0.06), 0.003, 0.04) * 0.04, 0.55 + 0.08 * k)
    poe(x, _acorde((523, 659, 784), 0.7, 0.035, 0.03, 0.5), 1.0)
    return reverb(x, 0.6, 0.3)


def corpo_morto(rng, v):
    """Ainz: o círculo mágico (o acorde sombrio) e o crânio que não sente nada."""
    x = _z(2.3)
    poe(x, _acorde((73, 110, 147, 175, 220), 1.6, 0.06, 0.2, 1.0), 0.0)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * sobe_e_some(n, 0.4, 1.2) * 0.3, 0.1)
    poe(x, _sino(rng, 147, 1.2, 0.12, SINO), 0.35)
    return reverb(x, 0.9, 0.45)


def geass(rng, v):
    """Lelouch: o Geass acendendo (o tom agudo) e a ordem dada."""
    x = _z(2.0)
    n = n_de(0.5)
    poe(x, seno(varre(400, 1800, n), n) * env(n, 0.05, 0.3) * 0.04, 0.0)
    poe(x, _whoosh(rng, 0.3, 1500, 8000, 0.7, 1.4, 0.5), 0.4)
    poe(x, _acorde((294, 349, 440, 587), 1.0, 0.05, 0.01, 0.7), 0.5)
    poe(x, _baque(150, 70, 0.3, 0.5), 0.5)
    return reverb(x, 0.7, 0.35)


def bakuryuha(rng, v):
    """Inuyasha: a Tessaiga descendo e os redemoinhos da Ferida do Vento."""
    x = _z(2.1)
    poe(x, _whoosh(rng, 0.35, 400, 4000, 0.9, 1.4, 0.5), 0.0)
    poe(x, _sino(rng, 900, 0.5, 0.06, METAL), 0.28)
    poe(x, _baque(100, 45, 0.4, 0.7, 2.4), 0.28)
    n = n_de(1.1)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 4000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 9 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.4, 0.35)
    return reverb(x, 0.6, 0.3)


def battojutsu(rng, v):
    """Kenshin: o silêncio, o saque rapidíssimo (o corte) e a bainha fechando."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, seno(2000, n) * sobe_e_some(n, 0.9, 1.0) * 0.015, 0.0)
    poe(x, _whoosh(rng, 0.1, 3000, 12000, 0.8, 1.3, 0.3), 0.27)
    poe(x, _sino(rng, 3800, 0.6, 0.06, METAL), 0.3)
    poe(x, estalo(rng, n_de(0.04), 1500, 6000, 0.008) * 0.8, 0.85)
    return reverb(x, 0.6, 0.3)


def come_fogo(rng, v):
    """Natsu: as chamas sugadas para a boca e o rugido de fogo do dragão."""
    x = _z(2.2)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 300, 4000, 2) * sobe_e_some(n, 0.9, 1.0) * 0.4, 0.0)
    poe(x, _baque(200, 100, 0.15, 0.3), 0.45)
    m = n_de(1.1)
    poe(x, satura(passa(rosa(rng, m), 120, 3000, 2) + seno(varre(140, 90, m), m) * 0.5, 2.5) * sobe_e_some(m, 0.2, 1.3) * 0.35, 0.5)
    return reverb(x, 0.6, 0.3)


def anulou(rng, v):
    """Asta: a espada negra cortando e a magia se desfazendo (o som que se apaga)."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.3, 200, 2000, 0.9, 1.4, 0.5), 0.15)
    poe(x, _baque(80, 40, 0.4, 0.8, 2.8), 0.38)
    for k in range(3):
        n = n_de(0.5)
        poe(x, seno(varre(1200 - 200 * k, 150, n, 0.5), n) * env(n, 0.005, 0.4) * 0.04, 0.4 + 0.05 * k)
        poe(x, _sino(rng, 2000 + 300 * k, 0.3, 0.03, VIDRO), 0.4 + 0.05 * k)
    return reverb(x, 0.5, 0.25)


def seja_agua(rng, v):
    """Spike: a gota caindo, o "plim" na água e a calma (o jazz de leve)."""
    x = _z(2.1)
    poe(x, _piu(1400, 600, 0.08, 0.05), 0.22)
    poe(x, _sino(rng, 800, 0.5, 0.05, CRISTAL), 0.25)
    for k, f in enumerate((294, 349, 440, 523)):
        poe(x, _sino(rng, f, 0.7, 0.035, SINO), 0.45 + 0.12 * k)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 300, 2000, 2) * sobe_e_some(n, 0.4, 1.2) * 0.15, 0.4)
    return reverb(x, 0.7, 0.35)


def pacifista(rng, v):
    """Vash: o tiro, as balas parando no ar (o zumbido esticado) e as penas caindo."""
    x = _z(2.1)
    n = n_de(0.2)
    poe(x, satura(passa(rosa(rng, n), 300, 8000, 2) * env(n, 0.0005, 0.05), 2.5) * 0.6, 0.0)
    m = n_de(0.6)
    poe(x, seno(varre(1600, 400, m, 0.5), m) * env(m, 0.01, 0.4) * 0.04, 0.1)
    poe(x, _acorde((523, 659, 784, 1047), 1.2, 0.035, 0.2, 0.8), 0.4)
    poe(x, _sopro(rng, 1.0, 1500, 6000, 0.15, 0.4), 0.4)
    return reverb(x, 0.7, 0.35)


def invento(rng, v):
    """Senku: o frasco borbulhando, a engrenagem girando e o "dez bilhões de por cento" (o acorde que brilha)."""
    x = _z(2.1)
    q = np.random.default_rng(6)
    for k in range(8):
        poe(x, _piu(q.uniform(500, 900), q.uniform(900, 1400), 0.04, 0.03), 0.05 + 0.06 * k)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.004) * 0.4, 0.3 + 0.07 * k)
    poe(x, _brilho(rng, 0.9, 2093, 0.05, CRISTAL), 0.75)
    poe(x, _acorde((523, 659, 784, 1047), 0.9, 0.04, 0.02, 0.6), 0.8)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "mu-tita": (tita, "King Kong: o titã"),
    "mu-cebola": (cebola, "Shrek: a cebola"),
    "mu-livre-estou": (livre_estou, "Elsa: livre estou"),
    "mu-dragao-malevola": (dragao_malevola, "Malévola: o dragão"),
    "mu-desejo": (desejo, "Gênio: o desejo"),
    "mu-hienas": (hienas, "Scar: as hienas"),
    "mu-presentes": (presentes, "Jack Esqueleto: os presentes"),
    "mu-voz-roubada": (voz_roubada, "Úrsula: a voz roubada"),
    "mu-one-for-all": (one_for_all, "Deku: One For All"),
    "mu-plus-ultra": (plus_ultra, "All Might: Plus Ultra"),
    "mu-choque-termico": (choque_termico, "Todoroki: o choque térmico"),
    "mu-cem-por-cento": (cem_por_cento, "Mob: 100%"),
    "mu-imune": (imune, "Rimuru: imune"),
    "mu-corpo-morto": (corpo_morto, "Ainz: o corpo morto-vivo"),
    "mu-geass": (geass, "Lelouch: o Geass"),
    "mu-bakuryuha": (bakuryuha, "Inuyasha: Bakuryuha"),
    "mu-battojutsu": (battojutsu, "Kenshin: o battojutsu"),
    "mu-come-fogo": (come_fogo, "Natsu: come o fogo"),
    "mu-anulou": (anulou, "Asta: anulou"),
    "mu-seja-agua": (seja_agua, "Spike: seja água"),
    "mu-pacifista": (pacifista, "Vash: o pacifista"),
    "mu-invento": (invento, "Senku: o invento"),
}
