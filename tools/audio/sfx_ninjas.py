"""Os sons das habilidades do Kakashi, do Yusuke e do Killua (veja tools/vfx/familias_v2/ninjas_e_detetives.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, _zumbido_de_arco, nota
from som import (CRISTAL, SINO, SR, assobio, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, ruido,
                 satura, seno, sobe_e_some, varre)


def _passaros(rng, seg, densidade=70, f0=2600, f1=4800):
    """O "canto de mil pássaros" do Raikiri: piados curtos que caem de tom, em cima de um crepitar elétrico."""
    n = n_de(seg)
    x = np.zeros(n)
    for _ in range(int(densidade * seg)):
        em = rng.uniform(0, seg - 0.05)
        m = n_de(rng.uniform(0.02, 0.05))
        f = rng.uniform(f0, f1)
        piado = seno(varre(f, f * 0.55, m, 0.6), m) * env(m, 0.002, 0.018) * rng.uniform(0.3, 0.8)
        poe(x, piado, em)
    x += graos(rng, n, int(140 * seg), 0, seg, 1800, 9000, 0.003, 0.7) * 0.8
    x += _zumbido_de_arco(rng, n, 150) * 0.12
    return x


def _choque(rng, seg, g=1.0):
    """Um estalo de raio: o rasgo branco e o crepitar que fica."""
    n = n_de(seg)
    x = passa(ruido(rng, n), 900, 11000, 2) * env(n, 0.0008, 0.05) * 0.9
    x += graos(rng, n, 40, 0.01, seg * 0.8, 2000, 9000, 0.003, 0.6) * 0.6
    return x * g


def _trovao(rng, seg=1.0, g=1.0):
    n = n_de(seg)
    t = np.arange(n) / SR
    ronco = passa(rosa(rng, n), 40, 500, 2) * np.exp(-t / (seg * 0.35)) * (0.7 + 0.3 * np.sin(2 * math.pi * 7 * t))
    x = satura(ronco * 1.2, 1.6) * 0.8
    poe(x, B.raio(rng, 1.0) * 0.5, 0.0)
    return x * g


# --------------------------------------------------------------- Kakashi
def sharingan_kakashi(rng, v):
    """Sharingan: um tom agudo estranho que sobe enquanto o olho abre, o giro das vírgulas acelerando
    (um zunido que pulsa cada vez mais rápido) e o estouro do genjutsu num golpe grave com eco."""
    x = _z(1.7)
    n = n_de(0.9)
    t = np.arange(n) / SR
    giro = np.cumsum(2 + 14 * (t / t[-1]) ** 2) / SR
    zunido = (seno(nota(76), n) + 0.6 * seno(nota(76) * 1.5, n)) * (0.55 + 0.45 * np.sin(2 * math.pi * giro * 3)) * sobe_e_some(n, 0.85, 1.4) * 0.16
    poe(x, zunido, 0.0)
    poe(x, seno(varre(nota(60), nota(84), n_de(0.5), 1.5), n_de(0.5)) * env(n_de(0.5), 0.05, 0.4) * 0.12, 0.0)
    poe(x, _whoosh(rng, 0.4, 3000, 400, 0.85, g=0.6), 0.55)
    poe(x, baque(n_de(0.6), 120, 50, 0.22, 0.5) * 0.8, 0.85)
    poe(x, _brilho(rng, 0.9, nota(64), 0.18, SINO), 0.85)
    return reverb(x, 0.65, 0.35, 5000)


def raikiri_mao(rng, v):
    """O Raikiri na mão, no Preparo: o canto de mil pássaros crescendo."""
    x = _passaros(rng, 1.1, 60) * sobe_e_some(n_de(1.1), 0.9, 1.0) * 0.8
    return reverb(x, 0.3, 0.15, 8000)


def raikiri(rng, v):
    """Raikiri: o canto dos pássaros no auge enquanto ele corre, o golpe que atravessa (estocada com
    estalo de raio) e o trovão rolando atrás."""
    x = _z(1.8)
    poe(x, _passaros(rng, 0.55, 90) * np.linspace(0.6, 1, n_de(0.55)) * 0.8, 0.0)
    poe(x, _whoosh(rng, 0.25, 600, 4500, 0.8, g=0.7), 0.3)
    poe(x, B.estocada(rng, v) * 0.9, 0.5)
    poe(x, _choque(rng, 0.4, 1.0), 0.5)
    poe(x, baque(n_de(0.5), 110, 45, 0.18, 0.6) * 0.8, 0.5)
    poe(x, _trovao(rng, 1.1, 0.7), 0.58)
    return reverb(x, 0.55, 0.25, 6000)


def kamui(rng, v):
    """Kamui: um sopro grave e invertido que cresce (o espaço torcendo), um redemoinho subindo de tom
    que suga tudo, o estalo seco do vácuo fechando e o zumbido que some."""
    x = _z(1.9)
    n = n_de(1.0)
    t = np.arange(n) / SR
    torce = passa(rosa(rng, n), 60, 900, 2) * (t / t[-1]) ** 2 * 0.7
    poe(x, torce, 0.0)
    poe(x, assobio(rng, n, 300, 2600, 1.6, 0.4) * (t / t[-1]) ** 1.5 * 0.5, 0.0)
    poe(x, seno(varre(nota(40), nota(52), n, 1.4), n) * sobe_e_some(n, 0.9, 1.6) * 0.25, 0.0)
    poe(x, estalo(rng, n_de(0.08), 400, 4000, 0.02) * 1.1, 1.0)
    poe(x, baque(n_de(0.5), 70, 30, 0.2, 0.3) * 0.9, 1.0)
    m = n_de(0.8)
    poe(x, (seno(nota(57), m) + seno(nota(57) * 1.01, m)) * env(m, 0.01, 0.5) * 0.08, 1.02)
    return reverb(x, 0.75, 0.35, 4200)


# --------------------------------------------------------------- Yusuke
def soco_espiritual(rng, v):
    """Soco espiritual: o zumbido da energia acendendo no punho, o golpe muito pesado e a aura que
    estoura e chia em volta."""
    x = _z(1.4)
    n = n_de(0.35)
    poe(x, (seno(varre(nota(45), nota(57), n, 1.2), n) + 0.5 * seno(varre(nota(57), nota(69), n, 1.2), n)) * sobe_e_some(n, 0.9, 1.4) * 0.18, 0.0)
    poe(x, _whoosh(rng, 0.2, 400, 3000, 0.8, g=0.6), 0.15)
    poe(x, B.soco_pesado(rng, v) * 1.2, 0.3)
    poe(x, baque(n_de(0.6), 95, 40, 0.22, 0.6) * 1.0, 0.3)
    poe(x, B.impacto_energia(rng, v) * 0.6, 0.32)
    poe(x, passa(rosa(rng, n_de(0.7)), 800, 6000, 2) * env(n_de(0.7), 0.01, 0.35) * 0.3, 0.34)
    return reverb(x, 0.5, 0.22, 6000)


def reigun_carga(rng, v):
    """A energia juntando na ponta do dedo: um tom que sobe e um chiado que cresce."""
    n = n_de(1.0)
    x = (seno(varre(nota(52), nota(76), n, 1.3), n) * 0.2 + passa(rosa(rng, n), 1500, 8000, 2) * 0.12) * sobe_e_some(n, 0.95, 1.6)
    x += graos(rng, n, 30, 0.2, 0.95, 3000, 9000, 0.003, 0.6) * 0.3
    return reverb(x, 0.35, 0.15, 7000)


def reigun(rng, v):
    """Reigun: o disparo (um estampido grave com o tom subindo), a bala zunindo pelo ar e a explosão
    enorme com o ronco que fica."""
    x = _z(2.0)
    poe(x, B.disparo(rng, v) * 1.0, 0.0)
    poe(x, baque(n_de(0.4), 140, 60, 0.12, 0.8) * 0.8, 0.0)
    n = n_de(0.4)
    poe(x, (seno(varre(nota(70), nota(62), n, 1.0), n) * 0.18 + assobio(rng, n, 1200, 3500, 1.0) * 0.4) * env(n, 0.01, 0.35), 0.05)
    poe(x, B.explosao(rng, v) * 1.25, 0.42)
    poe(x, baque(n_de(1.0), 70, 28, 0.4, 0.7) * 1.0, 0.42)
    poe(x, passa(rosa(rng, n_de(1.0)), 60, 600, 2) * env(n_de(1.0), 0.02, 0.5) * 0.4, 0.5)
    return reverb(x, 0.7, 0.28, 4500)


def rei_shotgun(rng, v):
    """Shotgun: o soco que solta a rajada, e as balas estourando no rival uma atrás da outra."""
    x = _z(1.6)
    poe(x, B.soco_pesado(rng, v) * 0.8, 0.0)
    poe(x, _whoosh(rng, 0.25, 500, 4000, 0.7, g=0.6), 0.03)
    for k in range(8):
        em = 0.25 + 0.055 * k + rng.uniform(-0.012, 0.012)
        poe(x, B.disparo(rng, v)[: n_de(0.25)] * rng.uniform(0.45, 0.7), em)
        poe(x, baque(n_de(0.18), 150, 70, 0.05, 0.6) * 0.45, em)
    poe(x, B.impacto_energia(rng, v) * 0.6, 0.72)
    return reverb(x, 0.55, 0.22, 6000)


# --------------------------------------------------------------- Killua
def ritmo_eletrico(rng, v):
    """Ritmo elétrico: passos rápidos em ritmo (as imagens dele girando), o zumbido elétrico que
    acompanha e três cortes de garra secos com estalo de choque."""
    x = _z(1.6)
    for k in range(7):
        em = 0.04 * k ** 1.15 + 0.02
        poe(x, estalo(rng, n_de(0.05), 600, 3000, 0.012) * 0.55, em * 2.2)
        poe(x, _choque(rng, 0.08, 0.35), em * 2.2 + 0.01)
    poe(x, _zumbido_de_arco(rng, n_de(0.8), 140) * sobe_e_some(n_de(0.8), 0.6, 1.4) * 0.2, 0.0)
    for k, em in enumerate((0.78, 0.86, 0.94)):
        poe(x, B.corte(rng, v) * 0.7, em)
        poe(x, _choque(rng, 0.15, 0.6), em + 0.01)
    poe(x, baque(n_de(0.4), 110, 50, 0.12, 0.6) * 0.6, 0.95)
    return reverb(x, 0.45, 0.2, 7000)


def palma_relampago(rng, v):
    """Palma relâmpago: o raio rasga da palma até o rival — estalo branco, o trovão perto e o chiado
    do choque preso no corpo."""
    x = _z(1.6)
    poe(x, _zumbido_de_arco(rng, n_de(0.25), 180) * sobe_e_some(n_de(0.25), 0.9, 1.5) * 0.25, 0.0)
    poe(x, _choque(rng, 0.5, 1.2), 0.22)
    poe(x, B.raio(rng, v) * 0.9, 0.22)
    poe(x, _trovao(rng, 1.1, 0.8), 0.26)
    poe(x, graos(rng, n_de(0.6), 50, 0.0, 0.55, 2500, 9000, 0.003, 0.6) * 0.4, 0.5)
    return reverb(x, 0.6, 0.25, 6500)


def velocidade_divina(rng, v):
    """Velocidade divina: o zumbido elétrico subindo, os estalos de teletransporte (cada aparição um
    "tz"), os golpes secos em sequência e o trovão do golpe final."""
    x = _z(2.0)
    n = n_de(1.3)
    poe(x, _zumbido_de_arco(rng, n, 160) * sobe_e_some(n, 0.75, 1.3) * 0.22, 0.0)
    for k in range(6):
        em = 0.12 + 0.12 * k
        poe(x, _choque(rng, 0.09, 0.7), em)
        poe(x, B.soco_leve(rng, v) * 0.6, em + 0.04)
    poe(x, B.soco_pesado(rng, v) * 1.0, 0.92)
    poe(x, _trovao(rng, 1.0, 0.9), 0.92)
    poe(x, graos(rng, n_de(0.7), 70, 0.0, 0.65, 2500, 9000, 0.003, 0.6) * 0.45, 1.0)
    return reverb(x, 0.55, 0.25, 6000)


SONS: dict = {
    "sharingan-kakashi": (sharingan_kakashi, "Sharingan do Kakashi: o olho abre, as vírgulas giram e o genjutsu estoura"),
    "raikiri-mao": (raikiri_mao, "o Raikiri cantando na mão do Kakashi, no Preparo"),
    "raikiri": (raikiri, "Raikiri: os mil pássaros, o golpe que atravessa e o trovão"),
    "kamui": (kamui, "Kamui: o espaço torcendo, a sucção e o vácuo fechando"),
    "soco-espiritual": (soco_espiritual, "Soco espiritual do Yusuke: a energia no punho e o golpe pesado"),
    "reigun-carga": (reigun_carga, "o Reigun juntando na ponta do dedo"),
    "reigun": (reigun, "Reigun: o disparo, a bala zunindo e a explosão enorme"),
    "rei-shotgun": (rei_shotgun, "Shotgun: o soco e as balas estourando uma atrás da outra"),
    "ritmo-eletrico": (ritmo_eletrico, "Ritmo elétrico do Killua: os passos em ritmo e os cortes de garra"),
    "palma-relampago": (palma_relampago, "Palma relâmpago: o raio rasgando e o trovão"),
    "velocidade-divina": (velocidade_divina, "Velocidade divina: os teletransportes, os golpes e o trovão final"),
}
