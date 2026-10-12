"""Os sons da rodada 10 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_k.py)."""
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


def tempestade(rng, v):
    """Thor: o Mjolnir erguido (o zumbido de metal) e os trovões caindo nele."""
    x = _z(2.1)
    poe(x, _sino(rng, 220, 1.2, 0.1, METAL), 0.0)
    poe(x, _trovao(rng, 1.3, 1.0), 0.35)
    poe(x, graos(rng, n_de(1.2), 120, 0.0, 0.9, 2500, 11000, 0.0015) * 0.45, 0.35)
    return reverb(x, 0.7, 0.35)


def hollow(rng, v):
    """Ichigo: a máscara se formando (o rangido de osso) e o rugido do Hollow."""
    x = _z(2.0)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.04), 600, 3000, 0.012) * 0.5, 0.05 + 0.07 * k)
    n = n_de(0.9)
    t = _t(n)
    poe(x, satura(seno(varre(140, 90, n) * (1 + 0.08 * np.sin(2 * math.pi * 33 * t)), n) + passa(rosa(rng, n), 100, 2000, 2) * 0.8, 3.5) * env(n, 0.05, 0.5) * 0.15, 0.45)
    poe(x, (seno(65, n) + seno(69, n)) * env(n, 0.05, 0.5) * 0.08, 0.45)
    return reverb(x, 0.7, 0.35)


def danca_branca(rng, v):
    """Rukia: o círculo no chão (o sino frio) e o pilar de gelo subindo."""
    x = _z(2.0)
    poe(x, _sino(rng, 1568, 0.8, 0.06, VIDRO), 0.0)
    n = n_de(0.9)
    poe(x, (passa(rosa(rng, n), 2000, 8000, 2) * 0.3 + seno(varre(800, 2400, n), n) * 0.03) * sobe_e_some(n, 0.4, 1.2), 0.35)
    for k in range(8):
        poe(x, _sino(rng, 2500 + 200 * (k % 4), 0.25, 0.025, VIDRO), 0.4 + 0.06 * k)
    return reverb(x, 0.8, 0.4)


def ilusao_aizen(rng, v):
    """Aizen: o espelho rachando (o vidro que estala em teia) e a ilusão derretendo (o tom que desce torto)."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.06), 1500, 9000, 0.015), 0.1)
    for k in range(8):
        poe(x, _sino(rng, 2000 + 300 * (k % 4), 0.3, 0.025, VIDRO), 0.12 + 0.03 * k)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(varre(660, 330, n) * (1 + 0.02 * np.sin(2 * math.pi * 5 * t)), n) * sobe_e_some(n, 0.3, 1.2) * 0.05, 0.6)
    return reverb(x, 0.8, 0.4)


def tapa_olho(rng, v):
    """Kenpachi: o tapa-olho arrebentando, os sininhos e a pressão espiritual explodindo."""
    x = _z(2.1)
    poe(x, estalo(rng, n_de(0.04), 1000, 5000, 0.01) * 0.6, 0.0)
    for k in range(3):
        poe(x, _sino(rng, 2600 + 200 * k, 0.4, 0.03, SINO), 0.1 + 0.08 * k)
    n = n_de(1.4)
    poe(x, satura(passa(rosa(rng, n), 50, 2000, 2), 2.0) * sobe_e_some(n, 0.3, 1.1) * 0.6, 0.35)
    poe(x, _baque(55, 25, 0.8, 0.8, 2.6), 0.35)
    return reverb(x, 0.6, 0.3)


def endurecer(rng, v):
    """Eren: os cristais endurecendo sobre a pele (os estalos) e o vapor de titã."""
    x = _z(2.0)
    for k in range(10):
        poe(x, _sino(rng, 1200 + 150 * (k % 5), 0.25, 0.035, VIDRO), 0.04 * k)
        poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.006) * 0.3, 0.04 * k)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 2500, 8000, 2) * sobe_e_some(n, 0.2, 1.3) * 0.35, 0.6)
    return reverb(x, 0.5, 0.25)


def pedra_papel(rng, v):
    """Gon: "Pedra, papel…" (a aura carregando, cada vez mais forte) e o soco."""
    x = _z(2.0)
    n = n_de(1.1)
    poe(x, (passa(rosa(rng, n), 200, 2500, 2) * 0.4 + seno(varre(100, 300, n, 1.3), n) * 0.08) * sobe_e_some(n, 0.95, 1.0), 0.0)
    for k in range(3):
        poe(x, _piu(500 + 150 * k, 520 + 150 * k, 0.12, 0.04), 0.1 + 0.35 * k)
    poe(x, _baque(80, 30, 0.7, 1.0, 3.0), 1.1)
    return reverb(x, 0.5, 0.25)


def relampago(rng, v):
    """Killua: o Godspeed (o crepitar elétrico rápido e os passos que somem)."""
    x = _z(1.9)
    poe(x, graos(rng, n_de(1.4), 200, 0.0, 0.95, 3000, 11000, 0.0012) * 0.5, 0.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 2000, 9000, 0.4, 1.4, 0.4), 0.1 + 0.12 * k)
    n = n_de(1.2)
    poe(x, satura(seno(90, n) + seno(180, n) * 0.5, 2) * sobe_e_some(n, 0.3, 1.2) * 0.05, 0.0)
    return reverb(x, 0.5, 0.25)


def bungee_gum(rng, v):
    """Hisoka: a goma esticando (o "boing" elástico) e as cartas embaralhando."""
    x = _z(1.9)
    n = n_de(0.8)
    t = _t(n)
    poe(x, seno(150 * (1 + 0.6 * np.sin(math.pi * t / 0.8)) * (1 + 0.05 * np.sin(2 * math.pi * 10 * t)), n) * env(n, 0.02, 0.5) * 0.07, 0.1)
    for k in range(6):
        poe(x, passa(rosa(rng, n_de(0.04)), 2500, 8000, 2) * env(n_de(0.04), 0.001, 0.02) * 0.35, 0.8 + 0.05 * k)
    return reverb(x, 0.5, 0.25)


def juramento(rng, v):
    """Kurapika: as correntes girando e os olhos escarlates (o tom firme)."""
    x = _z(2.0)
    poe(x, _corrente(rng, 1.0, 16, 0.4), 0.0)
    poe(x, _acorde((220, 277, 330), 1.0, 0.05, 0.05, 0.6), 0.75)
    poe(x, _sino(rng, 880, 0.7, 0.05, METAL), 0.8)
    return reverb(x, 0.6, 0.3)


def transmutacao(rng, v):
    """Edward: as palmas, as faíscas da transmutação correndo e as lanças de pedra subindo."""
    x = _z(2.0)
    poe(x, passa(rosa(rng, n_de(0.06)), 800, 5000, 2) * env(n_de(0.06), 0.001, 0.03) * 0.8, 0.0)
    poe(x, graos(rng, n_de(0.6), 80, 0.0, 0.8, 2500, 10000, 0.0015) * 0.5, 0.05)
    for k in range(5):
        poe(x, _baque(200 - 15 * k, 90, 0.2, 0.4, 2.0), 0.5 + 0.05 * k)
        poe(x, estalo(rng, n_de(0.05), 400, 2500, 0.02) * 0.4, 0.5 + 0.05 * k)
    return reverb(x, 0.5, 0.25)


def parede(rng, v):
    """Alphonse: a parede de pedra subindo do chão (o ronco e os blocos encaixando)."""
    x = _z(2.0)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 40, 600, 2) * sobe_e_some(n, 0.7, 1.0) * 0.6, 0.1)
    for k in range(4):
        poe(x, _baque(140 - 10 * k, 70, 0.2, 0.4, 2.0), 0.3 + 0.12 * k)
    poe(x, _sino(rng, 500, 0.6, 0.06, METAL), 1.0)
    return reverb(x, 0.5, 0.25)


def chamas_roy(rng, v):
    """Roy: o estalo de dedos e a fila de explosões."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.05), 1500, 6000, 0.006) * 1.0, 0.15)
    for k in range(5):
        poe(x, _explosao(rng, 0.35 + 0.08 * k, 80 - 6 * k), 0.4 + 0.12 * k)
    return reverb(x, 0.5, 0.25)


def berserker(rng, v):
    """Guts: a Marca sangrando (o zumbido grave), a armadura fechando e o rugido de fera."""
    x = _z(2.1)
    n = n_de(1.0)
    poe(x, (seno(55, n) + seno(58, n)) * sobe_e_some(n, 0.5, 1.2) * 0.1, 0.0)
    for k in range(4):
        poe(x, _sino(rng, 700 + 100 * k, 0.3, 0.06, METAL), 0.4 + 0.07 * k)
    m = n_de(0.8)
    t = _t(m)
    poe(x, satura(seno(varre(120, 80, m) * (1 + 0.1 * np.sin(2 * math.pi * 35 * t)), m) + passa(rosa(rng, m), 80, 1500, 2), 4) * env(m, 0.04, 0.45) * 0.15, 0.75)
    return reverb(x, 0.6, 0.3)


def eclipse(rng, v):
    """Griffith: o Eclipse (o coro sombrio e o grito do Behelit) e as penas caindo."""
    x = _z(2.3)
    poe(x, _acorde((110, 131, 156, 196), 1.8, 0.07, 0.4, 1.0), 0.0)
    n = n_de(0.8)
    t = _t(n)
    poe(x, seno(varre(900, 1300, n) * (1 + 0.04 * np.sin(2 * math.pi * 9 * t)), n) * env(n, 0.05, 0.5) * 0.03, 0.5)
    poe(x, _sopro(rng, 1.2, 2000, 7000, 0.12, 0.4), 0.7)
    return reverb(x, 0.9, 0.45)


def za_warudo_jotaro(rng, v):
    """Jotaro: o tempo parando (o "ZA WARUDO" grave que se expande e o tique que trava)."""
    x = _z(2.3)
    n = n_de(1.0)
    poe(x, satura(seno(varre(200, 60, n, 0.6), n), 2) * env(n, 0.01, 0.6) * 0.12, 0.0)
    poe(x, passa(rosa(rng, n), 200, 2500, 2) * sobe_e_some(n, 0.2, 1.3) * 0.4, 0.0)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 2000, 6000, 0.004) * 0.7, 0.4 + 0.15 * k)
    poe(x, _sino(rng, 1047, 1.0, 0.05, SINO), 1.0)
    return reverb(x, 0.9, 0.45)


def road_roller(rng, v):
    """Dio: as facas girando, "ROAD ROLLER DA!" e o rolo compressor esmagando."""
    x = _z(2.2)
    for k in range(6):
        poe(x, _whoosh(rng, 0.1, 2000, 8000, 0.5, 1.4, 0.3), 0.05 * k)
    poe(x, _whoosh(rng, 0.5, 100, 1500, 0.8, 1.6, 0.6), 0.4)
    poe(x, _baque(50, 20, 1.0, 1.0, 3.2), 0.95)
    for k in range(6):
        poe(x, _sino(rng, 300 + 100 * k, 0.5, 0.08, METAL), 0.95 + 0.02 * k)
    return reverb(x, 0.6, 0.3)


def vida_demais(rng, v):
    """Giorno: a vida brotando (o acorde dourado que sobe) e as asas das borboletas."""
    x = _z(2.0)
    for k, f in enumerate((392, 494, 587, 740, 880)):
        poe(x, _sino(rng, f * 2, 0.6, 0.035, CRISTAL), 0.1 * k)
    poe(x, _acorde((392, 494, 587, 784), 1.2, 0.045, 0.1, 0.7), 0.4)
    for k in range(6):
        poe(x, passa(rosa(rng, n_de(0.05)), 1500, 5000, 2) * env(n_de(0.05), 0.003, 0.03) * 0.15, 0.9 + 0.06 * k)
    return reverb(x, 0.7, 0.35)


def vrrrum(rng, v):
    """Denji: a corda puxada e as motosserras ligando (o motor que grita)."""
    x = _z(2.0)
    poe(x, passa(rosa(rng, n_de(0.15)), 800, 5000, 2) * env(n_de(0.15), 0.005, 0.1) * 0.5, 0.0)
    n = n_de(1.5)
    t = _t(n)
    f = 60 + 50 * np.clip(t / 0.3, 0, 1) + 8 * np.sin(2 * math.pi * 7 * t)
    poe(x, satura(np.sign(np.sin(2 * math.pi * np.cumsum(f) / 44100)) * 0.6 + passa(rosa(rng, n), 500, 6000, 2) * 0.5, 2.5) * env(n, 0.02, 1.0, segura=0.4) * 0.12, 0.2)
    return reverb(x, 0.4, 0.2)


def escondida(rng, v):
    """Power: o "Viu só?" convencido (o tom que sobe) e o martelo de sangue."""
    x = _z(1.9)
    poe(x, _piu(500, 750, 0.2, 0.05), 0.0)
    poe(x, _whoosh(rng, 0.35, 300, 2500, 0.8, 1.5, 0.5), 0.3)
    poe(x, _baque(100, 40, 0.5, 1.0, 2.8), 0.7)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 200, 1500, 2) * env(m, 0.01, 0.3) * 0.35, 0.72)
    return reverb(x, 0.4, 0.2)


def agora_e_meu(rng, v):
    """Makima: os olhos de anéis (o tom hipnótico) e a corrente prendendo."""
    x = _z(2.1)
    n = n_de(1.2)
    t = _t(n)
    poe(x, (seno(330, n) + seno(331.5, n) + seno(495, n) * 0.4) * (0.6 + 0.4 * np.sin(2 * math.pi * 2 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.04, 0.0)
    poe(x, _corrente(rng, 0.7, 10, 0.35), 0.6)
    poe(x, _sino(rng, 660, 0.6, 0.06, METAL), 1.3)
    return reverb(x, 0.7, 0.35)


def disable(rng, v):
    """Mewtwo: a psique travando (os anéis que vibram) e o "clique" do Disable."""
    x = _z(1.9)
    n = n_de(0.9)
    t = _t(n)
    poe(x, seno(varre(400, 800, n) * (1 + 0.05 * np.sin(2 * math.pi * 16 * t)), n) * sobe_e_some(n, 0.8, 1.0) * 0.05, 0.0)
    poe(x, _baque(300, 150, 0.1, 0.35, 1.5), 0.9)
    poe(x, (seno(1200, n_de(0.2)) + seno(900, n_de(0.2))) * env(n_de(0.2), 0.003, 0.15) * 0.04, 0.9)
    return reverb(x, 0.6, 0.3)


def penhasco(rng, v):
    """Heihachi: o soco elétrico e o rival voando longe (o assobio que sobe)."""
    x = _z(1.9)
    poe(x, graos(rng, n_de(0.4), 50, 0.0, 0.7, 2500, 10000, 0.002) * 0.5, 0.0)
    poe(x, _baque(100, 40, 0.5, 1.0, 2.8), 0.3)
    poe(x, _trovao(rng, 0.5, 0.4), 0.3)
    poe(x, _piu(600, 2200, 0.6, 0.04), 0.5)
    return reverb(x, 0.5, 0.25)


def rainha_vampira(rng, v):
    """Marceline: a mordida (o estalo das presas) e o vermelho sugado (o som de canudinho e o baixo)."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.04), 800, 4000, 0.01) * 0.7, 0.05)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 2000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 8 * t) ** 2) * sobe_e_some(n, 0.5, 1.2) * 0.3, 0.2)
    for k, f in enumerate((82, 98, 110, 98)):
        m = n_de(0.25)
        poe(x, satura(seno(f, m), 2.5) * env(m, 0.005, 0.2) * 0.1, 0.3 + 0.25 * k)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "mu-tempestade": (tempestade, "Thor: o Mjolnir e os trovões"),
    "mu-hollow": (hollow, "Ichigo: a máscara Hollow"),
    "mu-danca-branca": (danca_branca, "Rukia: a Dança branca"),
    "mu-ilusao-aizen": (ilusao_aizen, "Aizen: a ilusão"),
    "mu-tapa-olho": (tapa_olho, "Kenpachi: sem tapa-olho"),
    "mu-endurecer": (endurecer, "Eren: o endurecimento"),
    "mu-pedra-papel": (pedra_papel, "Gon: o Jajanken"),
    "mu-relampago": (relampago, "Killua: o Godspeed"),
    "mu-bungee-gum": (bungee_gum, "Hisoka: a Bungee Gum"),
    "mu-juramento": (juramento, "Kurapika: o juramento"),
    "mu-transmutacao": (transmutacao, "Edward: a transmutação"),
    "mu-parede": (parede, "Alphonse: a parede"),
    "mu-chamas-roy": (chamas_roy, "Roy: o estalo e as chamas"),
    "mu-berserker": (berserker, "Guts: o Berserker"),
    "mu-eclipse": (eclipse, "Griffith: o Eclipse"),
    "mu-za-warudo-jotaro": (za_warudo_jotaro, "Jotaro: Za Warudo"),
    "mu-road-roller": (road_roller, "Dio: ROAD ROLLER DA"),
    "mu-vida-demais": (vida_demais, "Giorno: a vida"),
    "mu-vrrrum": (vrrrum, "Denji: as motosserras"),
    "mu-escondida": (escondida, "Power: o martelo de sangue"),
    "mu-agora-e-meu": (agora_e_meu, "Makima: o domínio"),
    "mu-disable": (disable, "Mewtwo: o Disable"),
    "mu-penhasco": (penhasco, "Heihachi: do penhasco"),
    "mu-rainha-vampira": (rainha_vampira, "Marceline: a rainha vampira"),
}
