"""Os sons da rodada 11 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_l.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def coragem_luigi(rng, v):
    """Luigi: a lanterna ligando (o clique), o medo (o assobio trêmulo) e a coragem (as notas que sobem)."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.005) * 0.7, 0.0)
    n = n_de(0.6)
    t = _t(n)
    poe(x, seno(700 * (1 + 0.05 * np.sin(2 * math.pi * 12 * t)), n) * env(n, 0.03, 0.4) * 0.04, 0.1)
    for k, f in enumerate((392, 494, 587, 784)):
        poe(x, _quadrada(f, n_de(0.12)) * env(n_de(0.12), 0.003, 0.1) * 0.03, 0.75 + 0.1 * k)
    return reverb(x, 0.4, 0.2)


def coracao_peach(rng, v):
    """Peach: a coroa brilhando e os corações (o arpejo doce)."""
    x = _z(2.0)
    poe(x, _brilho(rng, 0.6, 2093, 0.05, CRISTAL), 0.0)
    for k, f in enumerate((659, 784, 988, 1319)):
        poe(x, _sino(rng, f, 0.5, 0.04, SINO), 0.4 + 0.1 * k)
    poe(x, _acorde((659, 831, 988), 0.8, 0.035, 0.05, 0.5), 0.85)
    return reverb(x, 0.7, 0.35)


def nada_aconteceu(rng, v):
    """Zoro: os três cortes das três espadas e o "Nada aconteceu" (o silêncio pesado)."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.15, 2000, 10000, 0.4, 1.4, 0.6), 0.05 + 0.05 * k)
        poe(x, _sino(rng, 2600 + 250 * k, 0.4, 0.05, METAL), 0.12 + 0.05 * k)
    n = n_de(1.2)
    poe(x, (seno(98, n) + seno(147, n) * 0.5) * env(n, 0.1, 0.8) * 0.05, 0.6)
    return reverb(x, 0.6, 0.3)


def clima(rng, v):
    """Nami: as bolhas de clima, a nuvem juntando e o raio caindo com a chuva."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _piu(500 + 200 * k, 1000 + 200 * k, 0.08, 0.04), 0.05 + 0.1 * k)
    poe(x, _trovao(rng, 1.0, 0.8), 0.55)
    m = n_de(1.0)
    poe(x, passa(rosa(rng, m), 1500, 8000, 2) * sobe_e_some(m, 0.2, 1.2) * 0.2, 0.6)
    return reverb(x, 0.6, 0.3)


def refeicao(rng, v):
    """Sanji: a tampa do prato (o "plim" de servido), a comida chiando e a perna pegando fogo."""
    x = _z(2.0)
    poe(x, _sino(rng, 1568, 0.5, 0.06, METAL), 0.35)
    m = n_de(0.8)
    poe(x, passa(rosa(rng, m), 3000, 9000, 2) * sobe_e_some(m, 0.3, 1.2) * 0.2, 0.4)
    n = n_de(0.8)
    poe(x, satura(passa(rosa(rng, n), 150, 3500, 2), 1.7) * sobe_e_some(n, 0.2, 1.4) * 0.45, 1.0)
    return reverb(x, 0.5, 0.25)


def puxado(rng, v):
    """Nero: o braço demoníaco esticando (o zumbido fantasma), a pegada e o puxão."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, (seno(varre(150, 300, n), n) * 0.08 + passa(rosa(rng, n), 200, 2000, 2) * 0.3) * env(n, 0.02, 0.35), 0.0)
    poe(x, _baque(150, 70, 0.3, 0.6, 2.2), 0.5)
    poe(x, _whoosh(rng, 0.35, 300, 3000, 0.7, 1.4, 0.5), 0.75)
    return reverb(x, 0.6, 0.3)


def suspeita(rng, v):
    """L: o "É ele" (a nota de suspense) e a barra subindo."""
    x = _z(2.0)
    poe(x, _acorde((233, 277, 349), 1.0, 0.05, 0.02, 0.7), 0.0)
    n = n_de(0.8)
    poe(x, seno(varre(400, 700, n), n) * sobe_e_some(n, 0.9, 1.0) * 0.04, 0.6)
    poe(x, _sino(rng, 1175, 0.6, 0.05, VIDRO), 1.4)
    return reverb(x, 0.6, 0.3)


def tropecou(rng, v):
    """Morty: o tropeço (o "aw jeez" trêmulo) e o tombo leve."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.25, 500, 3000, 0.6, 1.4, 0.35), 0.0)
    poe(x, _baque(160, 80, 0.2, 0.4), 0.3)
    n = n_de(0.5)
    t = _t(n)
    poe(x, satura(seno(varre(500, 380, n) * (1 + 0.04 * np.sin(2 * math.pi * 14 * t)), n), 1.6) * env(n, 0.02, 0.35) * 0.04, 0.5)
    return reverb(x, 0.4, 0.2)


def carona(rng, v):
    """Tails: as caudas girando como hélice (o "vuvuvu") e o vento."""
    x = _z(1.9)
    n = n_de(1.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 18 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.5, 0.0)
    poe(x, _piu(600, 1200, 0.2, 0.03), 1.2)
    return reverb(x, 0.4, 0.2)


def soco_carregado(rng, v):
    """Knuckles: o soco carregando (o zumbido que sobe) e a pancada com as luvas de espinhos."""
    x = _z(1.9)
    n = n_de(0.9)
    poe(x, (seno(varre(100, 300, n, 1.3), n) * 0.07 + passa(rosa(rng, n), 200, 2000, 2) * 0.2) * sobe_e_some(n, 0.95, 1.0), 0.0)
    poe(x, _baque(80, 30, 0.6, 1.0, 3.0), 0.95)
    poe(x, _sino(rng, 900, 0.4, 0.05, METAL), 0.95)
    return reverb(x, 0.5, 0.25)


def desmascarar(rng, v):
    """Velma: a lupa (o "hmm"), a máscara caindo e o "Zoinks!" de descoberta (o acorde)."""
    x = _z(2.0)
    n = n_de(0.4)
    poe(x, satura(seno(varre(260, 240, n), n), 1.4) * env(n, 0.04, 0.3) * 0.05, 0.0)
    poe(x, _whoosh(rng, 0.3, 500, 3000, 0.7, 1.4, 0.35), 0.7)
    poe(x, _baque(250, 120, 0.15, 0.4), 1.05)
    poe(x, _acorde((523, 659, 784, 1047), 0.8, 0.04, 0.01, 0.5), 1.05)
    return reverb(x, 0.5, 0.25)


def armadilha(rng, v):
    """Fred: a rede caindo (o vento das cordas) e o "Pegamos você!" (o tom de vitória)."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.4, 300, 2000, 0.8, 1.5, 0.4), 0.15)
    poe(x, _baque(200, 100, 0.2, 0.4), 0.85)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.03), 600, 2500, 0.01) * 0.25, 0.85 + 0.03 * k)
    poe(x, _acorde((392, 494, 587), 0.6, 0.04, 0.01, 0.4), 1.0)
    return reverb(x, 0.4, 0.2)


def mil_laminas(rng, v):
    """Byakuya: "Dispersar, Senbonzakura" — o sussurro das mil pétalas-lâmina girando."""
    x = _z(2.0)
    n = n_de(1.6)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2000, 9000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.35, 0.0)
    poe(x, graos(rng, n, 160, 0.0, 0.95, 4000, 11000, 0.0015) * 0.3, 0.0)
    poe(x, _sino(rng, 1760, 1.0, 0.04, SINO), 0.0)
    return reverb(x, 0.8, 0.4)


def leque(rng, v):
    """Kitana: os leques de aço girando (o zunido metálico) e o vento que levanta."""
    x = _z(1.9)
    for k in range(2):
        n = n_de(0.5)
        t = _t(n)
        poe(x, passa(rosa(rng, n), 2000, 8000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 20 * t) ** 2) * env(n, 0.01, 0.35) * 0.35, 0.1 * k)
        poe(x, _sino(rng, 2400 + 300 * k, 0.4, 0.04, METAL), 0.45 + 0.1 * k)
    poe(x, _whoosh(rng, 0.5, 400, 4000, 0.4, 1.3, 0.5), 0.7)
    return reverb(x, 0.5, 0.25)


def fraco(rng, v):
    """Shao Kahn: "Você é fraco!" (o grito grave) e o martelo batendo no chão."""
    x = _z(2.0)
    n = n_de(0.5)
    t = _t(n)
    poe(x, satura(seno(varre(130, 100, n) * (1 + 0.05 * np.sin(2 * math.pi * 25 * t)), n) + passa(rosa(rng, n), 100, 1200, 2) * 0.6, 3) * env(n, 0.03, 0.3) * 0.14, 0.0)
    poe(x, _whoosh(rng, 0.3, 200, 2000, 0.8, 1.5, 0.5), 0.3)
    poe(x, _baque(60, 25, 0.8, 1.0, 3.0), 0.65)
    poe(x, _sino(rng, 300, 0.8, 0.1, METAL), 0.65)
    return reverb(x, 0.6, 0.3)


def soneca_pesada(rng, v):
    """Snorlax: o ronco pesado e o barrigão subindo e descendo."""
    x = _z(2.2)
    for k in range(2):
        n = n_de(0.7)
        t = _t(n)
        poe(x, passa(rosa(rng, n), 40, 400, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 25 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.7, 0.1 + 0.85 * k)
        m = n_de(0.5)
        poe(x, passa(rosa(rng, m), 300, 1500, 2) * sobe_e_some(m, 0.4, 1.3) * 0.2, 0.75 + 0.85 * k)
    return reverb(x, 0.4, 0.2)


def esconderijo(rng, v):
    """Patrick: a pedra levantando (o rangido) e o Patrick se escondendo (o "plof")."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, (satura(seno(varre(80, 140, n), n), 2) * 0.08 + passa(rosa(rng, n), 100, 1000, 2) * 0.3) * env(n, 0.05, 0.3), 0.1)
    poe(x, _piu(700, 300, 0.2, 0.05), 0.5)
    poe(x, _baque(110, 50, 0.4, 0.7, 2.2), 1.2)
    return reverb(x, 0.4, 0.2)


def rapido_demais(rng, v):
    """Flecha: a supervelocidade (o zunido que dá voltas)."""
    x = _z(1.9)
    n = n_de(1.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 800, 7000, 2) * (0.4 + 0.6 * np.sin(2 * math.pi * 3 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.5, 0.0)
    poe(x, seno(varre(600, 1400, n), n) * sobe_e_some(n, 0.3, 1.2) * 0.02, 0.0)
    return reverb(x, 0.4, 0.2)


def inversao(rng, v):
    """Gwen: o feitiço (as palavras mágicas em tom roxo) e a inversão (as notas que trocam de lugar)."""
    x = _z(2.0)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 800, 4000, 2) * sobe_e_some(n, 0.5, 1.2) * 0.25, 0.0)
    for k, f in enumerate((523, 784, 784, 523)):
        poe(x, _sino(rng, f * 2, 0.4, 0.04, CRISTAL), 0.5 + 0.15 * k)
    return reverb(x, 0.6, 0.3)


def disfarce(rng, v):
    """Viúva Negra: as pulseiras carregando (os estalos elétricos) e o disfarce caindo."""
    x = _z(1.9)
    poe(x, graos(rng, n_de(0.8), 80, 0.0, 0.9, 2500, 10000, 0.0015) * 0.45, 0.4)
    poe(x, _piu(400, 1200, 0.25, 0.04), 0.35)
    poe(x, passa(rosa(rng, n_de(0.2)), 1500, 6000, 2) * env(n_de(0.2), 0.005, 0.12) * 0.3, 0.05)
    return reverb(x, 0.5, 0.25)


def aljava(rng, v):
    """Gavião Arqueiro: as quatro flechas (os disparos do arco) e os truques de cada uma."""
    x = _z(2.0)
    for k in range(4):
        t0 = 0.05 + 0.15 * k * 1.9
        poe(x, (seno(varre(300, 180, n_de(0.08)), n_de(0.08)) * 0.05 + passa(rosa(rng, n_de(0.08)), 1500, 6000, 2) * 0.3) * env(n_de(0.08), 0.001, 0.05), t0)
        poe(x, _whoosh(rng, 0.2, 2000, 9000, 0.6, 1.3, 0.3), t0)
    poe(x, _baque(150, 70, 0.2, 0.4), 0.5)
    poe(x, graos(rng, n_de(0.3), 30, 0.0, 0.7, 3000, 10000, 0.002) * 0.4, 0.8)
    poe(x, _explosao(rng, 0.4, 80), 1.1)
    poe(x, passa(rosa(rng, n_de(0.2)), 300, 2000, 2) * env(n_de(0.2), 0.005, 0.15) * 0.3, 1.4)
    return reverb(x, 0.5, 0.25)


def perigosa(rng, v):
    """Gamora: os dois cortes da espada (o shing duplo)."""
    x = _z(1.8)
    for k in range(2):
        poe(x, _whoosh(rng, 0.2, 2000, 10000, 0.4, 1.4, 0.7), 0.1 + 0.4 * k)
        poe(x, _sino(rng, 2800 + 400 * k, 0.6, 0.07, METAL), 0.2 + 0.4 * k)
    poe(x, _brilho(rng, 0.5, 2349, 0.04, CRISTAL), 0.95)
    return reverb(x, 0.5, 0.25)


def vinganca(rng, v):
    """Drax: as facas cruzando e o grito de vingança (o rugido grave)."""
    x = _z(1.9)
    poe(x, _sino(rng, 2200, 0.5, 0.08, METAL), 0.3)
    poe(x, _sino(rng, 2500, 0.5, 0.06, METAL), 0.32)
    n = n_de(0.8)
    t = _t(n)
    poe(x, satura(seno(varre(150, 100, n) * (1 + 0.06 * np.sin(2 * math.pi * 22 * t)), n) + passa(rosa(rng, n), 100, 1500, 2) * 0.7, 3.2) * env(n, 0.04, 0.45) * 0.15, 0.6)
    return reverb(x, 0.5, 0.25)


def encanto(rng, v):
    """Mulher-Aranha: o feromônio (o tom doce que ondula) e a rajada de veneno."""
    x = _z(1.9)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(660 * (1 + 0.03 * np.sin(2 * math.pi * 4 * t)), n) + seno(990, n) * 0.4) * sobe_e_some(n, 0.4, 1.2) * 0.035, 0.0)
    m = n_de(0.5)
    poe(x, (satura(seno(varre(300, 900, m), m), 2) * 0.05 + passa(rosa(rng, m), 800, 5000, 2) * 0.3) * env(m, 0.01, 0.3), 0.85)
    return reverb(x, 0.6, 0.3)


def ladra(rng, v):
    """Mulher-Gato: as garras arranhando e as joias tilintando ao serem roubadas."""
    x = _z(1.9)
    for k in range(4):
        poe(x, _whoosh(rng, 0.1, 2500, 10000, 0.4, 1.4, 0.35), 0.05 + 0.04 * k)
    for k in range(5):
        poe(x, _sino(rng, 2600 + 250 * (k % 3), 0.3, 0.04, CRISTAL), 0.6 + 0.07 * k)
    n = n_de(0.3)
    poe(x, satura(seno(varre(700, 900, n), n), 1.6) * env(n, 0.02, 0.2) * 0.03, 1.1)
    return reverb(x, 0.5, 0.25)


def medo(rng, v):
    """Espantalho: o gás do medo chiando e os sussurros de pesadelo."""
    x = _z(2.1)
    n = n_de(1.6)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.3, 0.0)
    for k in range(4):
        m = n_de(0.4)
        t = _t(m)
        poe(x, seno(varre(400 + 50 * k, 300 + 50 * k, m) * (1 + 0.05 * np.sin(2 * math.pi * 7 * t)), m) * sobe_e_some(m, 0.4, 1.2) * 0.025, 0.3 + 0.2 * k)
    poe(x, (seno(55, n) + seno(58, n)) * sobe_e_some(n, 0.5, 1.2) * 0.07, 0.0)
    return reverb(x, 0.8, 0.4)


SONS: dict = {
    "mu-coragem-luigi": (coragem_luigi, "Luigi: a coragem"),
    "mu-coracao-peach": (coracao_peach, "Peach: os corações"),
    "mu-nada-aconteceu": (nada_aconteceu, "Zoro: nada aconteceu"),
    "mu-clima": (clima, "Nami: o clima"),
    "mu-refeicao": (refeicao, "Sanji: a refeição"),
    "mu-puxado": (puxado, "Nero: puxado"),
    "mu-suspeita": (suspeita, "L: a suspeita"),
    "mu-tropecou": (tropecou, "Morty: tropeçou"),
    "mu-carona": (carona, "Tails: a carona"),
    "mu-soco-carregado": (soco_carregado, "Knuckles: o soco carregado"),
    "mu-desmascarar": (desmascarar, "Velma: desmascarado"),
    "mu-armadilha": (armadilha, "Fred: a armadilha"),
    "mu-mil-laminas": (mil_laminas, "Byakuya: Senbonzakura"),
    "mu-leque": (leque, "Kitana: os leques"),
    "mu-fraco": (fraco, "Shao Kahn: você é fraco"),
    "mu-soneca-pesada": (soneca_pesada, "Snorlax: a soneca"),
    "mu-esconderijo": (esconderijo, "Patrick: debaixo da pedra"),
    "mu-rapido-demais": (rapido_demais, "Flecha: rápido demais"),
    "mu-inversao": (inversao, "Gwen: a inversão"),
    "mu-disfarce": (disfarce, "Viúva Negra: o disfarce"),
    "mu-aljava": (aljava, "Gavião Arqueiro: as flechas"),
    "mu-perigosa": (perigosa, "Gamora: os cortes"),
    "mu-vinganca": (vinganca, "Drax: a vingança"),
    "mu-encanto": (encanto, "Mulher-Aranha: o encanto"),
    "mu-ladra": (ladra, "Mulher-Gato: a ladra"),
    "mu-medo": (medo, "Espantalho: o medo"),
}
