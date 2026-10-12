"""Os sons da rodada 12 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_m.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada08 import _corrente
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def desequilibrio(rng, v):
    """Asa Noturna: os bastões girando e batendo, e o pássaro abrindo as asas."""
    x = _z(1.9)
    for k in range(6):
        poe(x, _whoosh(rng, 0.1, 1200, 6000, 0.4, 1.4, 0.3), 0.05 * k)
    poe(x, (seno(420, n_de(0.12)) * 0.5 + passa(rosa(rng, n_de(0.12)), 600, 3000, 2)) * env(n_de(0.12), 0.001, 0.05) * 0.5, 0.4)
    poe(x, passa(rosa(rng, n_de(0.3)), 300, 2000, 2) * sobe_e_some(n_de(0.3), 0.4, 1.4) * 0.4, 0.9)
    poe(x, _brilho(rng, 0.5, 1760, 0.04, CRISTAL), 1.0)
    return reverb(x, 0.5, 0.25)


def diario(rng, v):
    """Dipper: o diário abrindo (as páginas) e o mistério (a nota estranha que sobe)."""
    x = _z(2.0)
    for k in range(4):
        poe(x, passa(rosa(rng, n_de(0.08)), 2000, 7000, 2) * env(n_de(0.08), 0.003, 0.05) * 0.35, 0.05 * k)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(392 * (1 + 0.01 * np.sin(2 * math.pi * 5 * t)), n) + seno(587, n) * 0.5 + seno(554, n) * 0.4) * sobe_e_some(n, 0.4, 1.2) * 0.035, 0.4)
    poe(x, _sino(rng, 1568, 0.6, 0.04, VIDRO), 0.9)
    return reverb(x, 0.7, 0.35)


def alegria(rng, v):
    """Mabel: a estrela cadente, o brilho e a alegria (o arpejo animado)."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.4, 2000, 9000, 0.5, 1.3, 0.35), 0.0)
    for k, f in enumerate((523, 659, 784, 1047, 1319, 1568)):
        poe(x, _sino(rng, f, 0.35, 0.035, CRISTAL), 0.4 + 0.07 * k)
    poe(x, graos(rng, n_de(0.8), 50, 0.0, 0.9, 4000, 11000, 0.002) * 0.25, 0.4)
    return reverb(x, 0.6, 0.3)


def caos(rng, v):
    """Yennefer: a magia do caos girando (o sussurro roxo) e o estalo de poder."""
    x = _z(2.0)
    n = n_de(1.1)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 5 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.35, 0.0)
    poe(x, (seno(311, n) + seno(370, n) * 0.7) * sobe_e_some(n, 0.6, 1.2) * 0.04, 0.0)
    poe(x, _trovao(rng, 0.6, 0.5), 0.8)
    return reverb(x, 0.7, 0.35)


def stars(rng, v):
    """Nemesis: o lança-foguetes, a explosão e o rosnado ("STARS…")."""
    x = _z(2.0)
    poe(x, satura(passa(rosa(rng, n_de(0.3)), 200, 6000, 2) * env(n_de(0.3), 0.001, 0.15), 2.5) * 0.6, 0.0)
    poe(x, _whoosh(rng, 0.4, 500, 4000, 0.6, 1.3, 0.4), 0.05)
    poe(x, _explosao(rng, 0.9, 60), 0.45)
    n = n_de(0.7)
    t = _t(n)
    poe(x, satura(seno(varre(90, 70, n) * (1 + 0.1 * np.sin(2 * math.pi * 30 * t)), n) + passa(rosa(rng, n), 80, 900, 2), 3.5) * env(n, 0.05, 0.4) * 0.12, 1.0)
    return reverb(x, 0.5, 0.25)


def raio_olimpo(rng, v):
    """Zeus: o raio do Olimpo caindo (o assobio que desce) e o trovão divino."""
    x = _z(2.1)
    poe(x, _piu(3000, 800, 0.4, 0.04), 0.0)
    poe(x, _trovao(rng, 1.4, 1.1), 0.38)
    poe(x, _baque(60, 25, 0.8, 0.9, 2.6), 0.38)
    poe(x, _acorde((196, 294, 392), 1.0, 0.04, 0.05, 0.6), 0.6)
    return reverb(x, 0.8, 0.4)


def abalador(rng, v):
    """Poseidon: o tridente batendo e as ondas quebrando."""
    x = _z(2.1)
    poe(x, _baque(70, 30, 0.6, 1.0, 2.6), 0.35)
    poe(x, _sino(rng, 400, 0.8, 0.1, METAL), 0.35)
    n = n_de(1.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 150, 2500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 1.5 * t)) * sobe_e_some(n, 0.25, 1.2) * 0.55, 0.4)
    return reverb(x, 0.7, 0.35)


def sabedoria(rng, v):
    """Atena: o pio da coruja e o acorde sereno da sabedoria."""
    x = _z(2.0)
    for k in range(2):
        n = n_de(0.3)
        poe(x, seno(varre(520, 440, n), n) * env(n, 0.03, 0.2) * 0.05, 0.05 + 0.35 * k)
    poe(x, _acorde((294, 370, 440, 587), 1.2, 0.045, 0.15, 0.7), 0.7)
    return reverb(x, 0.8, 0.4)


def mais_guerra(rng, v):
    """Ares: a lança batendo no escudo (o clang de bronze), o fogo da guerra e o grito."""
    x = _z(2.0)
    poe(x, _sino(rng, 600, 1.0, 0.16, METAL), 0.05)
    poe(x, _baque(110, 50, 0.4, 0.7, 2.4), 0.05)
    m = n_de(1.0)
    poe(x, satura(passa(rosa(rng, m), 150, 3500, 2), 1.8) * sobe_e_some(m, 0.3, 1.3) * 0.45, 0.45)
    n = n_de(0.5)
    poe(x, satura(seno(varre(180, 130, n), n) + passa(rosa(rng, n), 200, 2000, 2) * 0.6, 3) * env(n, 0.03, 0.3) * 0.12, 0.6)
    return reverb(x, 0.6, 0.3)


def flechas_sol(rng, v):
    """Apolo: o sol (o acorde dourado), a flecha voando e a cura caindo."""
    x = _z(2.0)
    poe(x, _acorde((392, 494, 587, 784), 1.0, 0.045, 0.05, 0.6), 0.0)
    poe(x, _whoosh(rng, 0.3, 2000, 9000, 0.5, 1.3, 0.5), 0.6)
    for k in range(4):
        poe(x, _sino(rng, 1568 + 200 * k, 0.4, 0.03, CRISTAL), 1.1 + 0.08 * k)
    return reverb(x, 0.7, 0.35)


def flecha_certeira(rng, v):
    """Ártemis: o arco esticando (o rangido), o disparo e o acerto no centro."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, satura(seno(varre(150, 260, n), n), 1.6) * env(n, 0.05, 0.3) * 0.04, 0.1)
    poe(x, (seno(varre(320, 200, n_de(0.08)), n_de(0.08)) * 0.06 + passa(rosa(rng, n_de(0.08)), 1500, 6000, 2) * 0.3) * env(n_de(0.08), 0.001, 0.05), 0.75)
    poe(x, _whoosh(rng, 0.25, 2000, 9000, 0.6, 1.3, 0.5), 0.76)
    poe(x, _baque(300, 150, 0.15, 0.5, 1.8), 1.15)
    poe(x, _sino(rng, 2093, 0.5, 0.04, VIDRO), 1.15)
    return reverb(x, 0.6, 0.3)


def mensageiro(rng, v):
    """Hermes: as asinhas batendo (o vento rápido) e o caduceu (o tilintar)."""
    x = _z(1.8)
    for k in range(8):
        poe(x, passa(rosa(rng, n_de(0.05)), 1500, 6000, 2) * env(n_de(0.05), 0.003, 0.03) * 0.3, 0.05 + 0.06 * k)
    poe(x, _whoosh(rng, 0.4, 1000, 9000, 0.4, 1.3, 0.6), 0.6)
    poe(x, _sino(rng, 1760, 0.5, 0.05, CRISTAL), 0.1)
    return reverb(x, 0.5, 0.25)


def discordia(rng, v):
    """Afrodite: o pomo dourado quicando e os corações se partindo."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _sino(rng, 1320, 0.25, 0.05 * (1 - 0.25 * k), METAL), 0.15 + 0.2 * k * (1 - 0.15 * k))
    for k in range(2):
        poe(x, estalo(rng, n_de(0.05), 1500, 6000, 0.01) * 0.7, 0.9 + 0.08 * k)
    n = n_de(0.6)
    poe(x, seno(varre(660, 440, n), n) * env(n, 0.02, 0.4) * 0.04, 0.95)
    return reverb(x, 0.6, 0.3)


def virou_pedra(rng, v):
    """Medusa: as cobras sibilando e a pedra rachando."""
    x = _z(2.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 4000, 10000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t) ** 2) * sobe_e_some(n, 0.4, 1.2) * 0.3, 0.0)
    poe(x, seno(varre(800, 1600, n_de(0.4)), n_de(0.4)) * env(n_de(0.4), 0.02, 0.3) * 0.03, 0.6)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.05), 300, 2500, 0.02) * 0.5, 1.0 + 0.06 * k)
    poe(x, _baque(150, 70, 0.3, 0.4), 1.0)
    return reverb(x, 0.6, 0.3)


def tempo_voltou(rng, v):
    """Cronos: os ponteiros girando para trás (os tiques ao contrário) e a ampulheta virando."""
    x = _z(2.1)
    n = n_de(0.08)
    for k in range(10):
        poe(x, estalo(rng, n, 2000, 6000, 0.004)[::-1] * 0.6, 0.05 + 0.07 * k)
    m = n_de(1.0)
    t = _t(m)
    poe(x, seno(varre(200, 800, m), m) * (1 - np.exp(-t * 3)) * env(m, 0.4, 0.3) * 0.05, 0.3)
    poe(x, _sino(rng, 784, 1.0, 0.07, SINO), 1.0)
    return reverb(x, 0.8, 0.4)


def trabalhos(rng, v):
    """Hércules: os doze trabalhos (os toques que sobem um a um) e a clava."""
    x = _z(2.1)
    for k in range(12):
        poe(x, _sino(rng, 523 * 2 ** (k / 12), 0.25, 0.03, SINO), 0.05 + 0.04 * k)
    poe(x, _baque(80, 30, 0.6, 1.0, 2.8), 0.75)
    poe(x, _acorde((262, 330, 392, 523), 0.9, 0.05, 0.02, 0.5), 0.78)
    return reverb(x, 0.6, 0.3)


def alma_pesada(rng, v):
    """Anúbis: a balança rangendo e o julgamento (o gongo grave)."""
    x = _z(2.2)
    n = n_de(0.8)
    t = _t(n)
    poe(x, satura(seno(220 + 30 * np.sin(2 * math.pi * 1.5 * t), n), 1.6) * env(n, 0.1, 0.5) * 0.03, 0.1)
    poe(x, _sino(rng, 98, 1.6, 0.2, SINO), 0.8)
    poe(x, (seno(73, n_de(1.2)) * 0.5) * env(n_de(1.2), 0.02, 0.8) * 0.1, 0.8)
    return reverb(x, 0.9, 0.45)


def ciclo_sol(rng, v):
    """Rá: o disco do sol girando (o acorde quente que pulsa entre dia e noite)."""
    x = _z(2.2)
    n = n_de(1.6)
    t = _t(n)
    dia = 0.5 + 0.5 * np.cos(2 * math.pi * 1.0 * t)
    poe(x, (seno(220, n) + seno(277, n) * 0.7 + seno(330, n) * 0.5) * (0.4 + 0.6 * dia) * sobe_e_some(n, 0.4, 1.2) * 0.04, 0.0)
    poe(x, (seno(110, n) + seno(131, n) * 0.6) * (1 - dia) * sobe_e_some(n, 0.4, 1.2) * 0.04, 0.0)
    poe(x, _brilho(rng, 0.8, 1760, 0.04, CRISTAL), 0.2)
    return reverb(x, 0.8, 0.4)


def tempestade_areia(rng, v):
    """Set: a tempestade de areia (o vento uivando e os grãos batendo)."""
    x = _z(2.0)
    n = n_de(1.6)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 400, 4000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 2 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.5, 0.0)
    poe(x, graos(rng, n, 150, 0.0, 0.95, 3000, 10000, 0.002) * 0.3, 0.0)
    poe(x, seno(400 + 120 * np.sin(2 * math.pi * 0.8 * t), n) * sobe_e_some(n, 0.4, 1.2) * 0.02, 0.0)
    return reverb(x, 0.6, 0.3)


def corvos_odin(rng, v):
    """Odin: os corvos grasnando e a lança Gungnir brilhando."""
    x = _z(2.0)
    for k in range(3):
        n = n_de(0.25)
        t = _t(n)
        poe(x, satura(seno(varre(700, 500, n) * (1 + 0.1 * np.sin(2 * math.pi * 40 * t)), n) + passa(rosa(rng, n), 800, 3000, 2) * 0.5, 3) * env(n, 0.01, 0.18) * 0.04, 0.05 + 0.3 * k)
    poe(x, _sino(rng, 1320, 0.8, 0.06, METAL), 1.0)
    poe(x, _brilho(rng, 0.6, 2093, 0.04, CRISTAL), 1.05)
    return reverb(x, 0.7, 0.35)


def gleipnir(rng, v):
    """Fenrir: as correntes arrebentando e o uivo do lobo."""
    x = _z(2.2)
    poe(x, _corrente(rng, 0.4, 8, 0.4), 0.0)
    poe(x, _sino(rng, 900, 0.5, 0.12, METAL), 0.4)
    poe(x, estalo(rng, n_de(0.05), 800, 5000, 0.015), 0.4)
    n = n_de(1.3)
    t = _t(n)
    f = 300 + 250 * np.sin(math.pi * np.clip(t / 1.2, 0, 1)) ** 0.7
    poe(x, satura(seno(f * (1 + 0.01 * np.sin(2 * math.pi * 6 * t)), n), 1.6) * env(n, 0.1, 0.9) * 0.05, 0.6)
    return reverb(x, 0.9, 0.45)


def morto_vivo(rng, v):
    """Hel: as chamas frias, o chão rachando e a mão de osso saindo (os estalos secos)."""
    x = _z(2.0)
    n = n_de(1.4)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.3, 0.0)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.04), 600, 3000, 0.01) * 0.5, 0.45 + 0.07 * k)
    poe(x, (seno(65, n) + seno(69, n)) * sobe_e_some(n, 0.4, 1.2) * 0.08, 0.0)
    return reverb(x, 0.8, 0.4)


def sonho(rng, v):
    """Freddy: a canção de ninar distorcida e as lâminas raspando."""
    x = _z(2.0)
    for k, f in enumerate((523, 659, 523, 784)):
        n = n_de(0.25)
        t = _t(n)
        poe(x, seno(f * (1 + 0.02 * np.sin(2 * math.pi * 5 * t)), n) * env(n, 0.01, 0.2) * 0.035, 0.05 * 0 + 0.13 * k)
    for k in range(4):
        poe(x, _whoosh(rng, 0.12, 2500, 10000, 0.4, 1.4, 0.4), 0.6 + 0.03 * k)
        poe(x, _sino(rng, 3000 + 200 * k, 0.3, 0.025, METAL), 0.65 + 0.03 * k)
    return reverb(x, 0.7, 0.35)


def vitima(rng, v):
    """Michael Myers: a respiração pesada e a faca descendo."""
    x = _z(2.0)
    for k in range(2):
        n = n_de(0.45)
        poe(x, passa(rosa(rng, n), 200, 1500, 2) * sobe_e_some(n, 0.4, 1.4) * 0.35, 0.05 + 0.6 * k)
    poe(x, _whoosh(rng, 0.2, 1500, 8000, 0.7, 1.4, 0.5), 0.25)
    poe(x, (seno(1100, n_de(0.3)) + seno(1650, n_de(0.3)) * 0.5) * env(n_de(0.3), 0.003, 0.2) * 0.05, 0.42)
    return reverb(x, 0.6, 0.3)


def damballa(rng, v):
    """Chucky: o feitiço de vodu ("Damballa!", o canto grave) e os raios."""
    x = _z(2.1)
    for k in range(3):
        n = n_de(0.3)
        poe(x, satura(seno(varre(160, 140, n), n), 2) * env(n, 0.03, 0.2) * 0.06, 0.05 + 0.3 * k)
    poe(x, _trovao(rng, 1.0, 0.9), 0.75)
    return reverb(x, 0.7, 0.35)


def come_medo(rng, v):
    """Pennywise: o balão inflando (o chiado de borracha), a risada e as luzes mortas."""
    x = _z(2.1)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 800, 4000, 2) * sobe_e_some(n, 0.8, 1.0) * 0.25, 0.0)
    for k in range(4):
        m = n_de(0.12)
        poe(x, satura(seno(varre(600 - 30 * k, 480 - 30 * k, m), m), 1.6) * env(m, 0.01, 0.08) * 0.04, 0.7 + 0.13 * k)
    p = n_de(1.0)
    poe(x, (seno(311, p) + seno(330, p)) * sobe_e_some(p, 0.5, 1.2) * 0.035, 0.8)
    return reverb(x, 0.8, 0.4)


SONS: dict = {
    "mu-desequilibrio": (desequilibrio, "Asa Noturna: os bastões"),
    "mu-diario": (diario, "Dipper: o diário"),
    "mu-alegria": (alegria, "Mabel: a alegria"),
    "mu-caos": (caos, "Yennefer: o caos"),
    "mu-stars": (stars, "Nemesis: STARS"),
    "mu-raio-olimpo": (raio_olimpo, "Zeus: o raio do Olimpo"),
    "mu-abalador": (abalador, "Poseidon: o tridente"),
    "mu-sabedoria": (sabedoria, "Atena: a sabedoria"),
    "mu-mais-guerra": (mais_guerra, "Ares: a guerra"),
    "mu-flechas-sol": (flechas_sol, "Apolo: as flechas de sol"),
    "mu-flecha-certeira": (flecha_certeira, "Ártemis: a flecha certeira"),
    "mu-mensageiro": (mensageiro, "Hermes: o mensageiro"),
    "mu-discordia": (discordia, "Afrodite: a discórdia"),
    "mu-virou-pedra": (virou_pedra, "Medusa: virou pedra"),
    "mu-tempo-voltou": (tempo_voltou, "Cronos: o tempo voltou"),
    "mu-trabalhos": (trabalhos, "Hércules: os trabalhos"),
    "mu-alma-pesada": (alma_pesada, "Anúbis: a alma pesada"),
    "mu-ciclo-sol": (ciclo_sol, "Rá: o ciclo do sol"),
    "mu-tempestade-areia": (tempestade_areia, "Set: a tempestade de areia"),
    "mu-corvos-odin": (corvos_odin, "Odin: os corvos"),
    "mu-gleipnir": (gleipnir, "Fenrir: Gleipnir"),
    "mu-morto-vivo": (morto_vivo, "Hel: o morto-vivo"),
    "mu-sonho": (sonho, "Freddy: o sonho"),
    "mu-vitima": (vitima, "Michael Myers: a vítima"),
    "mu-damballa": (damballa, "Chucky: Damballa"),
    "mu-come-medo": (come_medo, "Pennywise: come medo"),
}
