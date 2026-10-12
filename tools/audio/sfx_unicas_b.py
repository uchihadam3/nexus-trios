"""Os sons da rodada 1 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_b.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada14 import _trovao
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def genki_dama(rng, v):
    """A Genki Dama: a energia do mundo sendo sugada (o zumbido que sobe e o coro), a esfera descendo e a explosão
    enorme."""
    x = _z(2.4)
    n = n_de(0.9)
    poe(x, (seno(varre(110, 330, n, 1.2), n) * 0.12 + passa(rosa(rng, n), 300, 3000, 2) * 0.2) * sobe_e_some(n, 0.9, 1.0), 0.0)
    m = n_de(0.8)
    poe(x, (seno(392, m) + seno(494, m) * 0.7 + seno(587, m) * 0.6) * sobe_e_some(m, 0.9, 1.0) * 0.04, 0.1)
    k = n_de(1.3)
    poe(x, satura(passa(rosa(rng, k), 25, 3500, 2) * env(k, 0.003, 0.65), 2.4) * 0.85, 0.85)
    poe(x, satura(baque(n_de(0.8), 50, 20, 0.3, 1.0), 2.6) * 0.8, 0.85)
    poe(x, _brilho(rng, 0.8, 1320, 0.05, CRISTAL), 0.9)
    return reverb(x, 0.8, 0.35)


def zenkai(rng, v):
    """O Zenkai: o grito de poder (o rugido grave que sobe), a aura explodindo e os raios estalando, e a cura."""
    x = _z(1.8)
    n = n_de(0.6)
    poe(x, satura(seno(varre(90, 180, n, 1.0), n), 2.5) * sobe_e_some(n, 0.6, 1.2) * 0.15, 0.0)
    poe(x, passa(rosa(rng, n), 200, 3000, 2) * sobe_e_some(n, 0.6, 1.2) * 0.35, 0.0)
    poe(x, graos(rng, n_de(0.8), 40, 0.0, 0.7, 2500, 10000, 0.003) * 0.35, 0.15)
    poe(x, _trovao(rng, 0.8, 0.35), 0.2)
    m = n_de(0.7)
    poe(x, (seno(523, m) + seno(659, m) * 0.7 + seno(784, m) * 0.5) * env(m, 0.02, 0.35) * 0.04, 0.6)
    return reverb(x, 0.6, 0.3)


def kage_bunshin(rng, v):
    """O Kage Bunshin: o selo de mãos (dois estalos) e os dois "puf" de fumaça dos clones aparecendo."""
    x = _z(1.4)
    for k in range(2):
        poe(x, estalo(rng, n_de(0.08), 1500, 6000, 0.005) * 0.4, 0.0 + 0.06 * k)
    for k in range(2):
        n = n_de(0.4)
        poe(x, passa(rosa(rng, n), 300, 2500, 2) * env(n, 0.003, 0.2) * 0.55 + seno(varre(300, 120, n, 1.0), n) * env(n, 0.003, 0.12) * 0.08, 0.15 + 0.12 * k)
    return reverb(x, 0.4, 0.2)


def sharingan(rng, v):
    """O Sharingan: o giro das vírgulas (o tom que gira e desacelera) e o brilho seco do olho."""
    x = _z(1.4)
    n = n_de(0.8)
    t = _t(n)
    poe(x, seno(varre(900, 500, n, 0.7), n) * (0.6 + 0.4 * np.sin(2 * math.pi * (25 - 20 * t) * t)) * sobe_e_some(n, 0.3, 1.5) * 0.05, 0.0)
    poe(x, modal(n_de(0.6), 1760, rng=rng, **METAL) * env(n_de(0.6), 0.001, 0.25) * 0.12, 0.65)
    poe(x, passa(rosa(rng, n_de(0.3)), 100, 600, 2) * env(n_de(0.3), 0.01, 0.2) * 0.25, 0.0)
    return reverb(x, 0.5, 0.25)


def borracha(rng, v):
    """A borracha: o "boing" esticado que vai e volta, duas vezes."""
    x = _z(1.3)
    for k in range(2):
        n = n_de(0.45)
        t = _t(n)
        f = 180 + 120 * np.sin(2 * math.pi * 6 * t) * np.exp(-t * 5)
        poe(x, seno(f, n) * env(n, 0.003, 0.3) * 0.18, 0.05 + 0.3 * k)
    return reverb(x, 0.35, 0.2)


def vazio_infinito(rng, v):
    """O Vazio Infinito: o silêncio que puxa tudo (o grave que some), o céu de estrelas cintilando e o anel."""
    x = _z(2.0)
    n = n_de(1.6)
    poe(x, passa(rosa(rng, n), 30, 200, 2) * sobe_e_some(n, 0.15, 1.5) * 0.5, 0.0)
    for k in range(10):
        poe(x, modal(n_de(0.5), 1800 + 220 * k, rng=rng, **CRISTAL) * env(n_de(0.5), 0.001, 0.25) * 0.025, 0.15 + 0.1 * k)
    m = n_de(1.4)
    poe(x, (seno(220, m) + seno(330, m) * 0.6) * sobe_e_some(m, 0.4, 1.2) * 0.04, 0.2)
    return reverb(x, 0.9, 0.4)


def bochechas(rng, v):
    """As bochechas elétricas: o "pika" das faíscas e os estalos que pulam."""
    x = _z(1.3)
    for k in range(5):
        n = n_de(0.12)
        poe(x, (graos(rng, n, 15, 0.0, 0.1, 3000, 10000, 0.002) * 0.4 + satura(passa(rosa(rng, n), 1500, 7000, 2) * env(n, 0.001, 0.04), 3.0) * 0.2), 0.05 + 0.13 * k)
    m = n_de(0.3)
    poe(x, seno(varre(1400, 2200, m, 1.0), m) * env(m, 0.01, 0.15) * 0.04, 0.0)
    return reverb(x, 0.3, 0.15)


def tedio(rng, v):
    """O tédio do herói: o bocejo (o tom que desce, abafado) e as bolhas estourando."""
    x = _z(1.6)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 200, 900, 2) * sobe_e_some(n, 0.4, 1.4) * 0.15 + seno(varre(260, 160, n, 1.0), n) * sobe_e_some(n, 0.4, 1.4) * 0.05, 0.05)
    for k in range(3):
        poe(x, modal(n_de(0.15), 900 + 200 * k, rng=rng, **VIDRO) * env(n_de(0.15), 0.001, 0.05) * 0.06, 0.6 + 0.15 * k)
    return reverb(x, 0.35, 0.2)


def modo_serio(rng, v):
    """O soco sério: o silêncio de meio segundo, o soco que rasga o ar e o estrondo que treme o chão."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.15, 300, 4000, 0.9, 1.2, 0.5), 0.0)
    k = n_de(1.2)
    poe(x, satura(passa(rosa(rng, k), 25, 4000, 2) * env(k, 0.002, 0.55), 2.6) * 0.9, 0.12)
    poe(x, satura(baque(n_de(0.9), 45, 18, 0.35, 1.0), 2.8) * 0.85, 0.12)
    return reverb(x, 0.8, 0.35)


def garras_regeneram(rng, v):
    """As garras: os dois "snikt" metálicos e o chiado suave da carne fechando."""
    x = _z(1.5)
    for k in range(2):
        poe(x, modal(n_de(0.3), 2600 + 300 * k, rng=rng, **METAL) * env(n_de(0.3), 0.001, 0.1) * 0.14, 0.0 + 0.08 * k)
        poe(x, passa(rosa(rng, n_de(0.12)), 4000, 12000, 2) * env(n_de(0.12), 0.001, 0.05) * 0.3, 0.0 + 0.08 * k)
    n = n_de(0.7)
    poe(x, passa(rosa(rng, n), 1500, 5000, 2) * sobe_e_some(n, 0.4, 1.4) * 0.08, 0.4)
    poe(x, _brilho(rng, 0.5, 1046, 0.04, SINO), 0.5)
    return reverb(x, 0.4, 0.2)


def gancho(rng, v):
    """O gancho: o disparo da arma de corda, o cabo assobiando e o escudo fechando."""
    x = _z(1.3)
    poe(x, estalo(rng, n_de(0.1), 1000, 5000, 0.008) * 0.5, 0.0)
    poe(x, _whoosh(rng, 0.3, 800, 4000, 0.6, 1.3, 0.3), 0.02)
    poe(x, modal(n_de(0.3), 1200, rng=rng, **METAL) * env(n_de(0.3), 0.001, 0.1) * 0.12, 0.3)
    poe(x, satura(baque(n_de(0.2), 140, 80, 0.05, 0.5), 1.5) * 0.25, 0.35)
    return reverb(x, 0.35, 0.2)


def bomba_de_fumaca(rng, v):
    """A bomba de fumaça: o "tic" da bomba no chão e o chiado da fumaça se espalhando."""
    x = _z(1.6)
    poe(x, modal(n_de(0.1), 2200, rng=rng, **METAL) * env(n_de(0.1), 0.001, 0.03) * 0.1, 0.15)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 800, 6000, 2) * sobe_e_some(n, 0.15, 1.6) * 0.35, 0.2)
    poe(x, satura(baque(n_de(0.2), 120, 60, 0.05, 0.4), 1.4) * 0.25, 0.2)
    return reverb(x, 0.5, 0.25)


def batarangue(rng, v):
    """O batarangue: o zumbido do giro que se aproxima e o impacto metálico."""
    x = _z(1.3)
    n = n_de(0.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 600, 4000, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 18 * t))) * sobe_e_some(n, 0.9, 1.0) * 0.3, 0.0)
    poe(x, modal(n_de(0.4), 1500, rng=rng, **METAL) * env(n_de(0.4), 0.001, 0.15) * 0.18, 0.38)
    poe(x, satura(baque(n_de(0.2), 160, 80, 0.05, 0.7), 1.8) * 0.3, 0.38)
    return reverb(x, 0.35, 0.2)


def sopro_congelante(rng, v):
    """O sopro congelante: a rajada de vento gelado e o gelo estalando."""
    x = _z(1.6)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 600, 6000, 2) * sobe_e_some(n, 0.3, 1.5) * 0.4, 0.0)
    for k in range(5):
        poe(x, modal(n_de(0.3), 2000 + 400 * k, rng=rng, **VIDRO) * env(n_de(0.3), 0.001, 0.12) * 0.06, 0.5 + 0.06 * k)
    poe(x, graos(rng, n_de(0.5), 30, 0.0, 0.4, 3000, 10000, 0.004) * 0.25, 0.5)
    return reverb(x, 0.6, 0.3)


def teia(rng, v):
    """A teia: o "thwip" do disparo e a rede se esticando com o rangido dos fios."""
    x = _z(1.3)
    n = n_de(0.15)
    poe(x, (passa(rosa(rng, n), 2000, 8000, 2) * env(n, 0.001, 0.06) * 0.4 + seno(varre(1800, 600, n, 1.0), n) * env(n, 0.001, 0.08) * 0.06), 0.0)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 400, 2000, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 12 * _t(m)))) * sobe_e_some(m, 0.3, 1.5) * 0.12, 0.15)
    return reverb(x, 0.35, 0.2)


def cada_vez_maior(rng, v):
    """O Hulk crescendo: o rugido grave, o coração batendo e o chão rachando."""
    x = _z(1.8)
    n = n_de(0.8)
    poe(x, satura(seno(varre(60, 95, n, 1.0), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 7 * _t(n))), 3.0) * sobe_e_some(n, 0.5, 1.3) * 0.15, 0.0)
    for k in range(3):
        poe(x, satura(baque(n_de(0.3), 70, 35, 0.1, 0.6), 2.0) * 0.4, 0.1 + 0.25 * k)
    poe(x, graos(rng, n_de(0.6), 25, 0.0, 0.5, 300, 2500, 0.02) * 0.4, 0.3)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "mu-genki-dama": (genki_dama, "Goku: a Genki Dama"),
    "mu-zenkai": (zenkai, "Vegeta: o Zenkai"),
    "mu-kage-bunshin": (kage_bunshin, "Naruto: os clones das sombras"),
    "mu-sharingan": (sharingan, "Sasuke: o Sharingan"),
    "mu-borracha": (borracha, "Luffy: a borracha"),
    "mu-vazio-infinito": (vazio_infinito, "Gojo: o Vazio Infinito"),
    "mu-bochechas": (bochechas, "Pikachu: as bochechas elétricas"),
    "mu-tedio": (tedio, "Saitama: o tédio"),
    "mu-modo-serio": (modo_serio, "Saitama: o soco sério"),
    "mu-garras-regeneram": (garras_regeneram, "Wolverine: as garras e a cura"),
    "mu-gancho": (gancho, "Batman: o gancho"),
    "mu-bomba-de-fumaca": (bomba_de_fumaca, "Batman: a bomba de fumaça"),
    "mu-batarangue": (batarangue, "Batman: o batarangue"),
    "mu-sopro-congelante": (sopro_congelante, "Superman: o sopro congelante"),
    "mu-teia": (teia, "Homem-Aranha: a teia"),
    "mu-cada-vez-maior": (cada_vez_maior, "Hulk: crescendo"),
}
