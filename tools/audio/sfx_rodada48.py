"""Os sons da rodada 48 das habilidades próprias (veja tools/vfx/familias_v2/rodada48.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _sibilo(rng, seg, g=0.25):
    """O chiado da serpente (sssss)."""
    n = n_de(seg)
    return passa(rosa(rng, n), 4000, 11000, 2) * sobe_e_some(n, 0.2, 1.2) * g


def _tique(rng, g=0.4):
    return estalo(rng, n_de(0.012), 2000, 8000, 0.002) * g


def _pedra(rng, seg, g=0.3):
    """A pedra subindo e rangendo."""
    n = n_de(seg)
    t = _t(n)
    return satura(passa(rosa(rng, n), 100, 1500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 13 * t) ** 2), 3) * sobe_e_some(n, 0.4, 1.2) * g


# ------------------------------------------------------------------ Ártemis

def _corda(rng):
    x = _z(0.4)
    n = n_de(0.22)
    poe(x, seno(varre(230, 195, n), n) * env(n, 0.002, 0.2) * 0.045, 0.0)
    poe(x, estalo(rng, n_de(0.02), 600, 4000, 0.004) * 0.6, 0.0)
    return x


def flecha_de_prata(rng, v):
    """Ártemis: a corda soltando, a flecha de prata tilintando e a mira da lua."""
    x = _z(1.9)
    poe(x, _corda(rng), 0.0)
    poe(x, _whoosh(rng, 0.25, 2500, 11000, 0.8, 1.3, 0.35), 0.02)
    poe(x, _baque(200, 100, 0.12, 0.35), 0.28)
    poe(x, _sino(rng, 1976, 0.7, 0.03, CRISTAL), 0.3)
    poe(x, _sino(rng, 2637, 0.6, 0.015, CRISTAL), 0.4)
    return reverb(x, 0.7, 0.35)


def cervo_sagrado(rng, v):
    """Ártemis: o cervo de luz saltando (os cascos leves e o brilho)."""
    x = _z(2.0)
    for k in range(6):
        poe(x, _baque(300, 200, 0.05, 0.2), 0.1 + 0.13 * k)
        poe(x, _sino(rng, 1568 + 110 * (k % 3), 0.25, 0.01, CRISTAL), 0.1 + 0.13 * k)
    poe(x, _brilho(rng, 0.8, 1319, 0.015, CRISTAL), 0.2)
    return reverb(x, 0.7, 0.35)


def artemis_preparo(rng, v):
    """Ártemis (Preparo): o arco esticado sob a lua (o tom prateado em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(659, n) + seno(988, n) * 0.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.012, 0.0)
    poe(x, passa(rosa(rng, n), 800, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 16 * t) ** 2) * sobe_e_some(n, 0.5, 1.2) * 0.05, 0.0)
    return reverb(x, 0.7, 0.35)


def cacada_da_lua(rng, v):
    """Ártemis: a lua cheia acendendo e o feixe de luar descendo no rival."""
    x = _z(2.3)
    poe(x, _acorde((330, 494, 659, 988), 0.9, 0.022), 0.0)
    n = n_de(0.4)
    poe(x, seno(varre(400, 1600, n), n) * env(n, 0.35, 0.05) * 0.02, 0.1)
    poe(x, _whoosh(rng, 0.25, 2000, 10000, 0.7, 1.3, 0.4), 0.3)
    poe(x, _baque(80, 30, 0.6, 0.9, 2.8), 0.48)
    poe(x, _explosao(rng, 0.5, 70), 0.48)
    poe(x, _brilho(rng, 0.8, 1976, 0.02, CRISTAL), 0.5)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Hermes

def caduceu(rng, v):
    """Hermes: o caduceu girando (as asinhas batendo) e a pancada que deixa tonto."""
    x = _z(1.9)
    for k in range(5):
        n = n_de(0.04)
        poe(x, passa(rosa(rng, n), 800, 4000, 2) * env(n, 0.005, 0.03) * 0.3, 0.05 * k)
    poe(x, _whoosh(rng, 0.3, 500, 5000, 0.8, 1.3, 0.4), 0.0)
    poe(x, _baque(140, 60, 0.3, 0.6), 0.3)
    for k in range(3):
        poe(x, _piu(1200 - 150 * k, 800 - 100 * k, 0.12, 0.02), 0.5 + 0.12 * k)
    return reverb(x, 0.5, 0.25)


def mensagem_dos_deuses(rng, v):
    """Hermes: o pergaminho voando com as asinhas e as penas chegando no trio."""
    x = _z(2.1)
    for k in range(10):
        n = n_de(0.035)
        poe(x, passa(rosa(rng, n), 1000, 5000, 2) * env(n, 0.005, 0.03) * 0.22, 0.05 * k)
    poe(x, _whoosh(rng, 0.5, 800, 6000, 0.5, 1.3, 0.3), 0.0)
    for k, f in enumerate((784, 988, 1175)):
        poe(x, _sino(rng, f, 0.4, 0.02, CRISTAL), 0.4 + 0.12 * k)
    return reverb(x, 0.6, 0.3)


def roubo_divino(rng, v):
    """Hermes: o vulto passando zunindo e os buffs sendo levados ("plim-plim")."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.35, 1500, 10000, 0.7, 1.3, 0.5), 0.0)
    poe(x, _baque(170, 80, 0.15, 0.4), 0.2)
    for k in range(2):
        poe(x, _sino(rng, 2093 - 300 * k, 0.4, 0.025, CRISTAL), 0.35 + 0.08 * k)
        poe(x, _piu(1500, 2500, 0.15, 0.015), 0.4 + 0.08 * k)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Afrodite

def encanto_de_afrodite(rng, v):
    """Afrodite: o beijo soprado ("muah") e os coraçõezinhos tilintando nos rivais."""
    x = _z(2.0)
    n = n_de(0.1)
    poe(x, passa(rosa(rng, n), 800, 4000, 2) * env(n, 0.01, 0.08) * 0.3, 0.0)
    poe(x, _sopro(rng, 0.3, 500, 3000, 0.2, 0.3), 0.05)
    for k in range(6):
        poe(x, _sino(rng, (1047, 1319, 1568)[k % 3], 0.3, 0.015, CRISTAL), 0.2 + 0.06 * k)
    for k in range(3):
        poe(x, _piu(900, 1300, 0.15, 0.015), 0.5 + 0.1 * k)
    return reverb(x, 0.6, 0.3)


def abraco_do_amor(rng, v):
    """Afrodite: a concha abrindo (a harpa) e as pétalas caindo sobre o trio."""
    x = _z(2.2)
    for k, f in enumerate((523, 659, 784, 988, 1175, 1319)):
        poe(x, _sino(rng, f, 0.7, 0.022, SINO), 0.06 * k)
    poe(x, _acorde((523, 659, 784), 1.0, 0.018), 0.4)
    poe(x, _brilho(rng, 0.8, 1568, 0.012, CRISTAL), 0.5)
    return reverb(x, 0.8, 0.4)


def afrodite_preparo(rng, v):
    """Afrodite (Preparo): o coração batendo e as pétalas girando (em laço)."""
    x = _z(1.4)
    for k in range(2):
        poe(x, _baque(90, 60, 0.12, 0.35), 0.5 * k)
        poe(x, _baque(85, 55, 0.12, 0.25), 0.5 * k + 0.15)
    n = n_de(1.0)
    poe(x, (seno(659, n) + seno(830, n) * 0.6) * sobe_e_some(n, 0.5, 1.2) * 0.008, 0.0)
    return reverb(x, 0.6, 0.3)


def desejo(rng, v):
    """Afrodite: o coração gigante se fechando (o tom grave) e rachando ("crac")."""
    x = _z(2.1)
    n = n_de(0.45)
    poe(x, seno(varre(200, 400, n), n) * env(n, 0.35, 0.05) * 0.03, 0.0)
    poe(x, estalo(rng, n_de(0.06), 1500, 7000, 0.012) * 1.0, 0.45)
    poe(x, _sino(rng, 1760, 0.5, 0.03, CRISTAL), 0.45)
    poe(x, _baque(110, 45, 0.4, 0.7, 2.5), 0.47)
    for k in range(5):
        poe(x, _sino(rng, 2349 + 200 * k, 0.15, 0.01, CRISTAL), 0.52 + 0.03 * k)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Medusa

def mordida_de_serpente(rng, v):
    """Medusa: o sibilo das serpentes e os três botes."""
    x = _z(1.9)
    poe(x, _sibilo(rng, 0.4, 0.25), 0.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 1500, 7000, 0.7, 1.3, 0.25), 0.15 + 0.05 * k)
        poe(x, _baque(200, 100, 0.08, 0.3), 0.28 + 0.05 * k)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 1000, 4000, 2) * env(n, 0.05, 0.35) * 0.12, 0.45)
    return reverb(x, 0.5, 0.25)


def olhar_de_pedra(rng, v):
    """Medusa: os olhos acendendo ("vuung") e a pedra subindo, rangendo."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, (seno(varre(300, 900, n), n) + seno(varre(450, 1350, n), n) * 0.5) * env(n, 0.2, 0.08) * 0.025, 0.0)
    poe(x, _pedra(rng, 0.6, 0.35), 0.4)
    poe(x, _baque(90, 40, 0.3, 0.6), 0.65)
    return reverb(x, 0.7, 0.35)


def medusa_preparo(rng, v):
    """Medusa (Preparo): as serpentes sibilando agitadas (em laço)."""
    x = _z(1.4)
    for k in range(3):
        poe(x, _sibilo(rng, 0.35, 0.15), 0.33 * k)
    return reverb(x, 0.5, 0.25)


def petrificacao(rng, v):
    """Medusa: o olhar varrendo todos e a pedra cobrindo um por um."""
    x = _z(2.4)
    n = n_de(0.4)
    poe(x, (seno(varre(250, 800, n), n) + seno(varre(375, 1200, n), n) * 0.5) * env(n, 0.3, 0.08) * 0.025, 0.0)
    poe(x, _sibilo(rng, 0.5, 0.15), 0.1)
    for k in range(3):
        poe(x, _pedra(rng, 0.4, 0.3), 0.35 + 0.1 * k)
        poe(x, _baque(80, 35, 0.25, 0.5), 0.55 + 0.1 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Cronos

def foice_do_tempo(rng, v):
    """Cronos: a foice cortando e o tique-taque desacelerando."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.35, 400, 4000, 0.85, 1.3, 0.5), 0.0)
    poe(x, _baque(130, 55, 0.3, 0.6), 0.35)
    poe(x, _sino(rng, 988, 0.5, 0.02, METAL), 0.35)
    for k in range(5):
        poe(x, _tique(rng, 0.5), 0.5 + 0.08 * k + 0.02 * k * k)
    return reverb(x, 0.6, 0.3)


def atraso_de_cronos(rng, v):
    """Cronos: o relógio surgindo e o tique-taque andando para trás."""
    x = _z(2.0)
    poe(x, _sino(rng, 587, 0.8, 0.03, SINO), 0.05)
    for k in range(8):
        poe(x, _tique(rng, 0.5), 0.3 + 0.06 * k)
    n = n_de(0.5)
    poe(x, seno(varre(700, 300, n), n) * env(n, 0.05, 0.4) * 0.015, 0.3)
    return reverb(x, 0.7, 0.35)


def cronos_preparo(rng, v):
    """Cronos (Preparo): o tique-taque e as engrenagens girando (em laço)."""
    x = _z(1.4)
    for k in range(4):
        poe(x, _tique(rng, 0.55 if k % 2 == 0 else 0.35), 0.25 * k)
    n = n_de(1.0)
    poe(x, satura(passa(rosa(rng, n), 300, 1500, 2), 2) * sobe_e_some(n, 0.5, 1.2) * 0.05, 0.0)
    return reverb(x, 0.5, 0.25)


def era_de_ouro(rng, v):
    """Cronos: o relógio dourado tocando e os ponteiros correndo para frente."""
    x = _z(2.3)
    poe(x, _sino(rng, 523, 1.0, 0.04, SINO), 0.0)
    poe(x, _sino(rng, 784, 0.9, 0.025, SINO), 0.02)
    for k in range(14):
        poe(x, _tique(rng, 0.4), 0.25 + 0.05 * k - 0.0012 * k * k)
    poe(x, _acorde((523, 659, 784, 1047), 0.8, 0.02), 0.6)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Hércules

def clava_de_hercules(rng, v):
    """Hércules: a clava em chamas descendo e o estrondo."""
    x = _z(2.1)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 200, 3000, 2) * env(n, 0.05, 0.3) * 0.3, 0.0)
    poe(x, _whoosh(rng, 0.35, 120, 1500, 0.9, 1.3, 0.55), 0.0)
    poe(x, _baque(45, 18, 1.0, 1.0, 3.2), 0.33)
    poe(x, _explosao(rng, 0.6, 50), 0.33)
    return reverb(x, 0.7, 0.35)


def desafio_de_hercules(rng, v):
    """Hércules: o rugido de leão e o desafio ecoando."""
    x = _z(2.2)
    n = n_de(0.8)
    rugido = satura(seno(varre(120, 80, n), n) + passa(rosa(rng, n), 100, 1500, 2) * 1.0, 5)
    poe(x, rugido * env(n, 0.05, 0.5) * 0.06, 0.0)
    for k in range(2):
        poe(x, _baque(80, 40, 0.25, 0.6, 2.5), 0.35 + 0.2 * k)
    return reverb(x, 0.9, 0.45)


def hercules_preparo(rng, v):
    """Hércules (Preparo): o esforço grave e o chão afundando (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, satura(seno(65, n) + passa(rosa(rng, n), 40, 300, 2) * 0.6, 3) * sobe_e_some(n, 0.5, 1.2) * 0.05, 0.0)
    for k in range(2):
        poe(x, _baque(60, 30, 0.3, 0.5, 2.4), 0.5 * k + 0.1)
    return reverb(x, 0.5, 0.25)


def forca_de_semideus(rng, v):
    """Hércules: a força juntando (o zumbido dourado) e o soco de semideus."""
    x = _z(2.4)
    n = n_de(0.4)
    poe(x, seno(varre(80, 240, n), n) * env(n, 0.35, 0.05) * 0.04, 0.0)
    poe(x, _whoosh(rng, 0.2, 200, 3000, 0.85, 1.3, 0.5), 0.25)
    poe(x, _baque(35, 14, 1.3, 1.0, 3.6), 0.42)
    poe(x, _explosao(rng, 1.0, 35), 0.42)
    poe(x, _acorde((196, 294, 392), 0.8, 0.02), 0.45)
    return reverb(x, 0.8, 0.4)


SONS: dict = {
    "flecha-de-prata": (flecha_de_prata, "Ártemis: a flecha de prata"),
    "cervo-sagrado": (cervo_sagrado, "Ártemis: o cervo sagrado"),
    "artemis-preparo": (artemis_preparo, "Ártemis: o arco sob a lua (Preparo)"),
    "cacada-da-lua": (cacada_da_lua, "Ártemis: a caçada da lua"),
    "caduceu": (caduceu, "Hermes: o caduceu"),
    "mensagem-dos-deuses": (mensagem_dos_deuses, "Hermes: a mensagem dos deuses"),
    "roubo-divino": (roubo_divino, "Hermes: o roubo divino"),
    "encanto-de-afrodite": (encanto_de_afrodite, "Afrodite: o encanto"),
    "abraco-do-amor": (abraco_do_amor, "Afrodite: o abraço do amor"),
    "afrodite-preparo": (afrodite_preparo, "Afrodite: o coração batendo (Preparo)"),
    "desejo": (desejo, "Afrodite: o desejo"),
    "mordida-de-serpente": (mordida_de_serpente, "Medusa: a mordida de serpente"),
    "olhar-de-pedra": (olhar_de_pedra, "Medusa: o olhar de pedra"),
    "medusa-preparo": (medusa_preparo, "Medusa: as serpentes sibilando (Preparo)"),
    "petrificacao": (petrificacao, "Medusa: a petrificação"),
    "foice-do-tempo": (foice_do_tempo, "Cronos: a foice do tempo"),
    "atraso-de-cronos": (atraso_de_cronos, "Cronos: o atraso"),
    "cronos-preparo": (cronos_preparo, "Cronos: o tique-taque (Preparo)"),
    "era-de-ouro": (era_de_ouro, "Cronos: a era de ouro"),
    "clava-de-hercules": (clava_de_hercules, "Hércules: a clava"),
    "desafio-de-hercules": (desafio_de_hercules, "Hércules: o desafio"),
    "hercules-preparo": (hercules_preparo, "Hércules: o esforço (Preparo)"),
    "forca-de-semideus": (forca_de_semideus, "Hércules: a força de semideus"),
}
