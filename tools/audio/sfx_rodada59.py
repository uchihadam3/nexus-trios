"""Os sons da rodada 59 das habilidades próprias (veja tools/vfx/familias_v2/rodada59.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _tiro(rng, g=0.5, grave=180):
    n = n_de(0.35)
    return (satura(passa(rosa(rng, n), 300, 8000, 2) * env(n, 0.001, 0.06), 3) * 0.8 + satura(seno(varre(grave, 60, n), n), 2) * env(n, 0.001, 0.1) * 0.5) * g


def _corrente(rng, seg, g=0.2):
    x = _z(seg + 0.1)
    q = np.random.default_rng(59)
    for k in range(int(seg * 25)):
        poe(x, _sino(rng, q.uniform(2500, 4500), 0.08, 0.01 * g * 10, METAL), q.uniform(0, seg))
    return x


def _agua(rng, seg, g=0.3):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 300, 5000, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 9 * t)) * sobe_e_some(n, 0.4, 1.3) * g


def _palmada(rng, g=0.3):
    n = n_de(0.08)
    return (passa(rosa(rng, n), 400, 5000, 2) * env(n, 0.001, 0.04) + seno(varre(220, 120, n), n) * env(n, 0.001, 0.05) * 0.3) * g


def _zumbido_eletrico(rng, seg, g=0.02):
    n = n_de(seg)
    t = _t(n)
    return satura(seno(120, n) * (0.6 + 0.4 * np.sin(2 * math.pi * 50 * t)), 3) * sobe_e_some(n, 0.4, 1.2) * g


# ------------------------------------------------------------------ Rem

def maca_de_ferro(rng, v):
    """Rem: a corrente tilintando, a maça girando ("vum-vum") e a pancada de ferro."""
    x = _z(2.1)
    poe(x, _corrente(rng, 0.35, 0.15), 0.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 150, 1500, 0.6, 1.3, 0.35), 0.03 + 0.1 * k)
    poe(x, _baque(60, 25, 0.6, 1.0, 3.0), 0.42)
    poe(x, _sino(rng, 220, 0.6, 0.04, METAL), 0.42)
    return reverb(x, 0.7, 0.35)


def cura_de_agua_rem(rng, v):
    """Rem: a água girando em volta do aliado e o brilho da cura."""
    x = _z(2.0)
    poe(x, _agua(rng, 0.9, 0.18), 0.0)
    poe(x, _acorde((659, 784, 988), 0.9, 0.025), 0.35)
    poe(x, _brilho(rng, 0.6, 1319, 0.03, CRISTAL), 0.45)
    return reverb(x, 0.9, 0.45)


def rem_preparo(rng, v):
    """Rem (Preparo): o chifre acendendo e o rosnado da oni (em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, satura(seno(90, n) * (1 + 0.1 * np.sin(2 * math.pi * 20 * t)) + passa(rosa(rng, n), 80, 600, 2) * 0.6, 4) * sobe_e_some(n, 0.5, 1.2) * 0.03, 0.0)
    poe(x, _sino(rng, 1568, 0.5, 0.015, CRISTAL), 0.3)
    return reverb(x, 0.7, 0.35)


def forma_de_oni(rng, v):
    """Rem: o rugido da oni e a maça esmagando o chão."""
    x = _z(2.5)
    n = n_de(0.5)
    poe(x, satura(seno(varre(160, 100, n), n) + passa(rosa(rng, n), 100, 1500, 2), 5) * env(n, 0.05, 0.3) * 0.05, 0.0)
    poe(x, _corrente(rng, 0.3, 0.12), 0.2)
    poe(x, _whoosh(rng, 0.25, 100, 1500, 0.9, 1.3, 0.6), 0.2)
    poe(x, _baque(32, 12, 1.4, 1.0, 3.6), 0.42)
    poe(x, _explosao(rng, 0.7, 40), 0.42)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Kirito

def vorpal_strike(rng, v):
    """Kirito: a espada carregando o brilho da skill e a estocada ("VSHHH")."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, seno(varre(400, 1200, n), n) * env(n, 0.25, 0.05) * 0.025, 0.0)
    poe(x, _whoosh(rng, 0.18, 1000, 8000, 0.8, 1.3, 0.6), 0.25)
    poe(x, _sino(rng, 1760, 0.5, 0.035, METAL), 0.38)
    poe(x, _baque(100, 50, 0.3, 0.6), 0.38)
    return reverb(x, 0.7, 0.35)


def parry_kirito(rng, v):
    """Kirito: as duas espadas defendendo ("TING-TING-TING")."""
    x = _z(1.9)
    for k in range(3):
        poe(x, _sino(rng, 1568 + 220 * k, 0.4, 0.035, METAL), 0.25 + 0.15 * k)
        for j in range(3):
            poe(x, estalo(rng, n_de(0.02), 3000, 9000, 0.004) * 0.2, 0.26 + 0.15 * k + 0.01 * j)
    return reverb(x, 0.6, 0.3)


def kirito_preparo(rng, v):
    """Kirito (Preparo): as duas espadas zumbindo com o brilho da skill (em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, (seno(523, n) + seno(784, n) * 0.6 + seno(1047, n) * 0.3) * (0.6 + 0.4 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.012, 0.0)
    return reverb(x, 0.7, 0.35)


def starburst_stream(rng, v):
    """Kirito: "STARBURST STREAM!" — as 16 estocadas em sequência e o último golpe."""
    x = _z(2.8)
    for k in range(16):
        poe(x, _whoosh(rng, 0.08, 1500, 8000, 0.5, 1.3, 0.25), 0.1 + 0.042 * k)
        poe(x, _sino(rng, 1400 + 120 * (k % 4), 0.15, 0.012, METAL), 0.14 + 0.042 * k)
    poe(x, _baque(60, 25, 0.6, 0.9, 2.8), 0.78)
    poe(x, _sino(rng, 2093, 0.7, 0.04, METAL), 0.78)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Spike

def jeet_kune_do(rng, v):
    """Spike: o "vem" com a mão, o pé raspando e o chute."""
    x = _z(1.9)
    n = n_de(0.15)
    poe(x, passa(rosa(rng, n), 800, 4000, 2) * env(n, 0.02, 0.1) * 0.08, 0.05)
    poe(x, _whoosh(rng, 0.15, 400, 4000, 0.8, 1.3, 0.5), 0.2)
    poe(x, _baque(110, 50, 0.3, 0.8, 2.4), 0.34)
    return reverb(x, 0.6, 0.3)


def esquiva_spike(rng, v):
    """Spike: o corpo inclinando e as balas zunindo de raspão."""
    x = _z(1.9)
    for k in range(3):
        n = n_de(0.15)
        poe(x, seno(varre(2500, 1200, n), n) * env(n, 0.01, 0.1) * 0.02, 0.15 + 0.08 * k)
        poe(x, _whoosh(rng, 0.1, 2000, 7000, 0.5, 1.3, 0.2), 0.15 + 0.08 * k)
    poe(x, _whoosh(rng, 0.3, 200, 1500, 0.5, 1.3, 0.3), 0.1)
    return reverb(x, 0.6, 0.3)


def spike_preparo(rng, v):
    """Spike (Preparo): o cão da Jericho armando e o isqueiro (em laço)."""
    x = _z(1.4)
    poe(x, estalo(rng, n_de(0.03), 1000, 5000, 0.005) * 0.5, 0.1)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.005) * 0.4, 0.18)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 1000, 5000, 2) * env(n, 0.05, 0.4) * 0.05, 0.5)
    return reverb(x, 0.6, 0.3)


def tiro_final(rng, v):
    """Spike: "Bang." — o tiro único da Jericho e o eco."""
    x = _z(2.3)
    poe(x, _tiro(rng, 0.8, 160), 0.3)
    poe(x, _baque(80, 35, 0.4, 0.6), 0.42)
    return reverb(x, 1.2, 0.55)


# ------------------------------------------------------------------ Vash

def tiro_desarmante(rng, v):
    """Vash: o tiro certeiro e a arma do rival caindo no chão ("clang")."""
    x = _z(2.1)
    poe(x, _tiro(rng, 0.6, 200), 0.22)
    poe(x, _sino(rng, 880, 0.3, 0.03, METAL), 0.34)
    poe(x, _sino(rng, 660, 0.4, 0.03, METAL), 0.85)
    return reverb(x, 0.8, 0.4)


def tufao_humanoide(rng, v):
    """Vash: o casaco girando e as balas passando zunindo."""
    x = _z(2.0)
    n = n_de(0.9)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.15, 0.0)
    for k in range(5):
        n = n_de(0.15)
        poe(x, seno(varre(3000, 1400, n), n) * env(n, 0.01, 0.1) * 0.015, 0.1 + 0.1 * k)
    return reverb(x, 0.6, 0.3)


def vash_preparo(rng, v):
    """Vash (Preparo): o braço virando canhão (o zumbido subindo) e as penas caindo (em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, (seno(220 + 100 * t, n) + seno(330 + 150 * t, n) * 0.5) * sobe_e_some(n, 0.6, 1.2) * 0.02, 0.0)
    poe(x, _brilho(rng, 0.8, 1976, 0.015, CRISTAL), 0.2)
    return reverb(x, 0.9, 0.45)


def braco_de_anjo(rng, v):
    """Vash: as asas abrindo (o coro de anjo) e o raio gigante."""
    x = _z(2.9)
    poe(x, _acorde((392, 494, 587, 784), 1.2, 0.03, 0.2, 0.8), 0.0)
    n = n_de(1.2)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 300, 7000, 2) + seno(110, n) * 0.5, 3) * (0.8 + 0.2 * np.sin(2 * math.pi * 30 * t)) * env(n, 0.05, 0.6) * 0.35, 0.35)
    poe(x, _baque(30, 12, 1.4, 1.0, 3.6), 0.4)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Senku

def remedio_senku(rng, v):
    """Senku: o frasco borbulhando ("10 bilhões por cento!") e o brilho da cura."""
    x = _z(1.9)
    q = np.random.default_rng(591)
    for k in range(6):
        poe(x, _piu(q.uniform(400, 700), q.uniform(900, 1400), 0.04, 0.015), 0.05 + 0.06 * k)
    poe(x, _sino(rng, 1047, 0.3, 0.02, CRISTAL), 0.4)
    poe(x, _acorde((523, 659, 784), 0.8, 0.022), 0.45)
    return reverb(x, 0.8, 0.4)


def bateria_senku(rng, v):
    """Senku: a bateria ligando, a corrente correndo nos fios e o estalo no rival."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.03), 1000, 5000, 0.005) * 0.4, 0.05)
    poe(x, _zumbido_eletrico(rng, 0.8, 0.025), 0.15)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.02), 2500, 9000, 0.003) * 0.25, 0.5 + 0.06 * k)
    return reverb(x, 0.6, 0.3)


def senku_preparo(rng, v):
    """Senku (Preparo): o frasco borbulhando e as contas (os bipes da ciência em laço)."""
    x = _z(1.4)
    q = np.random.default_rng(592)
    for k in range(8):
        poe(x, _piu(q.uniform(400, 800), q.uniform(900, 1500), 0.04, 0.01), 0.05 + 0.16 * k)
    for k in range(3):
        poe(x, _piu(1500 + 200 * k, 1500 + 200 * k, 0.05, 0.008), 0.2 + 0.4 * k)
    return reverb(x, 0.6, 0.3)


def polvora_senku(rng, v):
    """Senku: o pavio chiando correndo pelo chão e as três explosões."""
    x = _z(2.8)
    n = n_de(0.45)
    poe(x, passa(rosa(rng, n), 2000, 9000, 2) * env(n, 0.02, 0.05, 1.0, 0.35) * 0.15, 0.08)
    for k in range(3):
        poe(x, _baque(45 - 5 * k, 18, 0.7, 0.8, 2.8), 0.45 + 0.05 * k)
        poe(x, _explosao(rng, 0.45, 50), 0.45 + 0.05 * k)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Hinata

def punho_suave(rng, v):
    """Hinata: a palma suave (o "tap" abafado) e o chakra se fechando."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.2, 300, 2500, 0.8, 1.3, 0.4), 0.05)
    poe(x, _palmada(rng, 0.4), 0.3)
    poe(x, _baque(140, 70, 0.2, 0.3), 0.3)
    n = n_de(0.4)
    poe(x, seno(varre(800, 400, n), n) * env(n, 0.02, 0.3) * 0.015, 0.35)
    poe(x, _zumbido_eletrico(rng, 0.5, 0.012), 0.4)
    return reverb(x, 0.6, 0.3)


def rotacao_hinata(rng, v):
    """Hinata: a cúpula de chakra girando ("VUUUUM") e o golpe ricocheteando."""
    x = _z(2.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 8 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.25, 0.05)
    poe(x, (seno(330, n) + seno(495, n) * 0.4) * sobe_e_some(n, 0.4, 1.2) * 0.012, 0.05)
    poe(x, _sino(rng, 1319, 0.3, 0.025, METAL), 0.52)
    poe(x, _sino(rng, 1568, 0.3, 0.025, METAL), 0.67)
    return reverb(x, 0.7, 0.35)


def hinata_preparo(rng, v):
    """Hinata (Preparo): o Byakugan ativando (as veias pulsando) e o trigrama girando (em laço)."""
    x = _z(1.4)
    n = n_de(0.3)
    poe(x, seno(varre(300, 900, n), n) * env(n, 0.25, 0.05) * 0.015, 0.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(392, n) + seno(587, n) * 0.4) * (0.6 + 0.4 * np.sin(2 * math.pi * 2 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.01, 0.2)
    return reverb(x, 0.7, 0.35)


def sessenta_e_quatro_palmas(rng, v):
    """Hinata: "OITO TRIGRAMAS: 64 PALMAS!" — as palmas cada vez mais rápidas e a última."""
    x = _z(2.6)
    for k in range(16):
        poe(x, _palmada(rng, 0.2), 0.12 + 0.04 * k)
    poe(x, _palmada(rng, 0.5), 0.78)
    poe(x, _baque(80, 35, 0.5, 0.8, 2.6), 0.78)
    poe(x, _zumbido_eletrico(rng, 0.6, 0.015), 0.82)
    return reverb(x, 0.7, 0.35)


SONS: dict = {
    "maca-de-ferro": (maca_de_ferro, "Rem: maça de ferro"),
    "cura-de-agua-rem": (cura_de_agua_rem, "Rem: cura de água"),
    "rem-preparo": (rem_preparo, "Rem: o chifre de oni (Preparo)"),
    "forma-de-oni": (forma_de_oni, "Rem: forma de oni"),
    "vorpal-strike": (vorpal_strike, "Kirito: Vorpal Strike"),
    "parry-kirito": (parry_kirito, "Kirito: parry"),
    "kirito-preparo": (kirito_preparo, "Kirito: as duas espadas (Preparo)"),
    "starburst-stream": (starburst_stream, "Kirito: Starburst Stream"),
    "jeet-kune-do": (jeet_kune_do, "Spike: Jeet Kune Do"),
    "esquiva-spike": (esquiva_spike, "Spike: esquiva"),
    "spike-preparo": (spike_preparo, "Spike: a Jericho armando (Preparo)"),
    "tiro-final": (tiro_final, "Spike: tiro final"),
    "tiro-desarmante": (tiro_desarmante, "Vash: tiro desarmante"),
    "tufao-humanoide": (tufao_humanoide, "Vash: tufão humanoide"),
    "vash-preparo": (vash_preparo, "Vash: o braço-canhão (Preparo)"),
    "braco-de-anjo": (braco_de_anjo, "Vash: braço de anjo"),
    "remedio-senku": (remedio_senku, "Senku: remédio"),
    "bateria-senku": (bateria_senku, "Senku: bateria"),
    "senku-preparo": (senku_preparo, "Senku: a ciência (Preparo)"),
    "polvora-senku": (polvora_senku, "Senku: pólvora"),
    "punho-suave": (punho_suave, "Hinata: punho suave"),
    "rotacao-hinata": (rotacao_hinata, "Hinata: rotação"),
    "hinata-preparo": (hinata_preparo, "Hinata: o Byakugan (Preparo)"),
    "sessenta-e-quatro-palmas": (sessenta_e_quatro_palmas, "Hinata: 64 palmas"),
}
