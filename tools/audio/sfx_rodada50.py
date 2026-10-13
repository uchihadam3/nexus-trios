"""Os sons da rodada 50 das habilidades próprias (veja tools/vfx/familias_v2/rodada50.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _corvo(rng, g=0.03):
    """O grasnado do corvo ("crá")."""
    n = n_de(0.18)
    return satura(seno(varre(700, 500, n), n) + passa(rosa(rng, n), 600, 3000, 2) * 0.8, 6) * env(n, 0.01, 0.15) * g


def _uivo(rng, seg, g=0.03):
    n = n_de(seg)
    t = _t(n)
    f = 300 + 250 * np.sin(np.pi * t / seg) ** 0.6
    return satura(seno(f, n) + seno(f * 2.01, n) * 0.3, 2) * (0.85 + 0.15 * np.sin(2 * math.pi * 6 * t)) * env(n, seg * 0.3, seg * 0.5) * g


def _rasgo(rng, seg=0.09, g=0.3):
    n = n_de(seg)
    return satura(passa(rosa(rng, n), 1200, 9000, 2), 2) * env(n, 0.004, seg * 0.85) * g


def _vento_frio(rng, seg, g=0.2):
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 500, 4000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 0.8 * t)) * sobe_e_some(n, 0.4, 1.2) * g


def _respira(rng, seg, g=0.3, entra=True):
    n = n_de(seg)
    return passa(rosa(rng, n), 300, 2000 if entra else 1500, 2) * sobe_e_some(n, 0.6 if entra else 0.3, 1.3) * g


def _caixinha(rng, notas, passo, g=0.022):
    """A caixinha de música (o sino agudo e frágil)."""
    x = _z(len(notas) * passo + 0.8)
    for k, f in enumerate(notas):
        poe(x, _sino(rng, f, 0.6, g, CRISTAL), k * passo)
    return x


# ------------------------------------------------------------------ Odin

def gungnir_de_odin(rng, v):
    """Odin: a Gungnir arremessada (o zunido das runas) e o estrondo ao cravar."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, (seno(varre(150, 400, n), n) + seno(varre(225, 600, n), n) * 0.4) * env(n, 0.25, 0.05) * 0.025, 0.0)
    poe(x, _whoosh(rng, 0.3, 800, 8000, 0.9, 1.3, 0.5), 0.05)
    poe(x, _baque(80, 30, 0.6, 0.9, 2.8), 0.32)
    poe(x, _sino(rng, 330, 1.0, 0.04, METAL), 0.32)
    poe(x, _sino(rng, 1319, 0.5, 0.015, CRISTAL), 0.5)
    return reverb(x, 0.7, 0.35)


def corvos_de_odin(rng, v):
    """Odin: os dois corvos grasnando e batendo as asas até o rival."""
    x = _z(2.2)
    for k in range(2):
        poe(x, _corvo(rng, 0.03), 0.05 + 0.25 * k)
    for k in range(10):
        n = n_de(0.05)
        poe(x, passa(rosa(rng, n), 300, 2500, 2) * env(n, 0.01, 0.04) * 0.25, 0.1 + 0.07 * k)
    poe(x, _corvo(rng, 0.025), 0.75)
    return reverb(x, 0.7, 0.35)


def sabedoria_de_asgard(rng, v):
    """Odin: o olho abrindo e as runas tocando sobre o trio (o coro nórdico)."""
    x = _z(2.3)
    n = n_de(0.3)
    poe(x, seno(varre(150, 300, n), n) * env(n, 0.2, 0.08) * 0.025, 0.05)
    poe(x, _acorde((147, 220, 294, 440), 1.2, 0.025), 0.25)
    for k in range(5):
        poe(x, _sino(rng, (587, 659, 784, 880, 988)[k], 0.4, 0.012, CRISTAL), 0.35 + 0.08 * k)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Fenrir

def mordida_de_fenrir(rng, v):
    """Fenrir: o rosnado e as mandíbulas fechando ("CLAC")."""
    x = _z(1.9)
    n = n_de(0.35)
    poe(x, satura(passa(rosa(rng, n), 60, 500, 2), 3) * env(n, 0.05, 0.25) * 0.4, 0.0)
    poe(x, estalo(rng, n_de(0.04), 800, 5000, 0.01) * 1.2, 0.33)
    poe(x, _baque(140, 60, 0.3, 0.6), 0.33)
    for m in range(2):
        poe(x, _rasgo(rng, 0.1, 0.25), 0.36 + 0.03 * m)
    return reverb(x, 0.5, 0.25)


def uivo_de_fenrir(rng, v):
    """Fenrir: o uivo longo para a lua e o vento frio."""
    x = _z(2.4)
    poe(x, _uivo(rng, 1.3, 0.04), 0.05)
    poe(x, _vento_frio(rng, 1.4, 0.15), 0.1)
    return reverb(x, 1.0, 0.5)


def fenrir_preparo(rng, v):
    """Fenrir (Preparo): a corrente esticando e um elo estalando (em laço)."""
    x = _z(1.4)
    for k in range(4):
        poe(x, _sino(rng, 1760 + 120 * (k % 2), 0.12, 0.012, METAL), 0.18 * k)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.006) * 0.8, 0.78)
    poe(x, _sino(rng, 2349, 0.3, 0.02, METAL), 0.78)
    n = n_de(1.0)
    poe(x, satura(passa(rosa(rng, n), 60, 400, 2), 3) * sobe_e_some(n, 0.5, 1.2) * 0.2, 0.0)
    return reverb(x, 0.6, 0.3)


def ragnarok(rng, v):
    """Fenrir: o salto do lobo gigante, as mandíbulas e o mundo tremendo."""
    x = _z(2.4)
    poe(x, _uivo(rng, 0.4, 0.03), 0.0)
    poe(x, _whoosh(rng, 0.4, 200, 3000, 0.85, 1.3, 0.5), 0.0)
    poe(x, estalo(rng, n_de(0.05), 600, 4000, 0.012) * 1.3, 0.4)
    poe(x, _baque(38, 15, 1.2, 1.0, 3.4), 0.42)
    poe(x, _explosao(rng, 0.9, 38), 0.42)
    n = n_de(0.5)
    poe(x, seno(varre(250, 600, n), n) * env(n, 0.1, 0.3) * 0.018, 0.6)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Hel

def toque_da_morte(rng, v):
    """Hel: o toque gelado (o sopro frio) e a maldição grave."""
    x = _z(2.0)
    poe(x, _vento_frio(rng, 0.5, 0.2), 0.0)
    poe(x, _baque(150, 70, 0.2, 0.4), 0.3)
    n = n_de(0.9)
    poe(x, (seno(varre(110, 90, n), n) + seno(varre(117, 95, n), n)) * sobe_e_some(n, 0.2, 1.2) * 0.025, 0.35)
    return reverb(x, 0.9, 0.45)


def exercito_dos_mortos(rng, v):
    """Hel: o portal de Helheim abrindo e os mortos gemendo ao subir."""
    x = _z(2.4)
    n = n_de(0.4)
    poe(x, seno(varre(60, 90, n), n) * env(n, 0.2, 0.15) * 0.05, 0.0)
    for k in range(4):
        n2 = n_de(0.6)
        f = 150 + 30 * k
        poe(x, satura(seno(varre(f, f * 0.8, n2), n2), 2) * passa(rosa(rng, n2), 100, 1200, 2) * env(n2, 0.2, 0.35) * 0.35, 0.2 + 0.12 * k)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.04), 300, 2500, 0.012) * 0.4, 0.25 + 0.1 * k)
    return reverb(x, 0.9, 0.45)


def hel_preparo(rng, v):
    """Hel (Preparo): a névoa fria girando (o vento e o tinido de gelo em laço)."""
    x = _z(1.4)
    poe(x, _vento_frio(rng, 1.0, 0.16), 0.0)
    for k in range(3):
        poe(x, _sino(rng, 2637 + 200 * k, 0.3, 0.008, CRISTAL), 0.3 * k + 0.1)
    return reverb(x, 0.8, 0.4)


def frio_de_helheim(rng, v):
    """Hel: a névoa avançando e o gelo estalando ao prender cada rival."""
    x = _z(2.4)
    poe(x, _vento_frio(rng, 1.2, 0.3), 0.0)
    for k in range(3):
        for m in range(4):
            poe(x, estalo(rng, n_de(0.02), 2000, 9000, 0.004) * 0.4, 0.4 + 0.08 * k + 0.02 * m)
        poe(x, _sino(rng, 1976 + 200 * k, 0.5, 0.02, CRISTAL), 0.45 + 0.08 * k)
    poe(x, _baque(80, 35, 0.4, 0.6), 0.55)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Jason

def facao_de_jason(rng, v):
    """Jason: o facão descendo pesado e o corte."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.3, 400, 5000, 0.9, 1.3, 0.55), 0.05)
    poe(x, _baque(110, 45, 0.35, 0.75, 2.5), 0.32)
    poe(x, _rasgo(rng, 0.15, 0.35), 0.33)
    return reverb(x, 0.5, 0.25)


def volta_do_lago(rng, v):
    """Jason: a água do lago borbulhando e a máscara emergindo ("splash")."""
    x = _z(2.2)
    q = np.random.default_rng(9)
    for k in range(8):
        f = q.uniform(300, 700)
        poe(x, _piu(f, f * 1.8, 0.05, 0.015), 0.05 + 0.06 * k)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 500, 6000, 2) * env(n, 0.02, 0.45) * 0.35, 0.5)
    poe(x, _baque(120, 70, 0.3, 0.4), 0.5)
    n2 = n_de(0.8)
    poe(x, seno(varre(110, 82, n2), n2) * sobe_e_some(n2, 0.3, 1.2) * 0.03, 0.6)
    return reverb(x, 0.8, 0.4)


def jason_preparo(rng, v):
    """Jason (Preparo): o "ki-ki-ki... ma-ma-ma" sussurrado em eco (em laço)."""
    x = _z(1.4)
    for k in range(3):
        n = n_de(0.05)
        poe(x, passa(rosa(rng, n), 3000, 8000, 2) * env(n, 0.003, 0.04) * 0.3, 0.08 * k)
    for k in range(3):
        n = n_de(0.09)
        poe(x, passa(rosa(rng, n), 300, 1500, 2) * env(n, 0.01, 0.07) * 0.3, 0.45 + 0.1 * k)
    return reverb(x, 1.0, 0.5)


def sexta_feira_13(rng, v):
    """Jason: os golpes de facão em sequência e o acorde de terror."""
    x = _z(2.3)
    for k in range(4):
        poe(x, _whoosh(rng, 0.15, 800, 7000, 0.7, 1.3, 0.35), 0.15 + 0.1 * k)
        poe(x, _baque(110, 45, 0.2, 0.55), 0.22 + 0.1 * k)
        poe(x, _rasgo(rng, 0.1, 0.25), 0.22 + 0.1 * k)
    n = n_de(0.9)
    poe(x, (seno(220, n) + seno(233, n) + seno(311, n) * 0.6) * env(n, 0.05, 0.6) * 0.02, 0.0)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Freddy

def cancao_de_ninar(rng, v):
    """Freddy: a canção de ninar na caixinha ("um, dois, Freddy vem te pegar") e o rival adormecendo."""
    x = _z(2.4)
    poe(x, _caixinha(rng, (988, 1175, 988, 1175, 1319, 1175, 988, 880), 0.16, 0.025), 0.0)
    n = n_de(0.8)
    poe(x, seno(varre(400, 200, n), n) * sobe_e_some(n, 0.3, 1.2) * 0.008, 1.0)
    return reverb(x, 0.9, 0.45)


def garra_de_laminas(rng, v):
    """Freddy: as quatro lâminas rasgando e o tinido metálico."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 1500, 9000, 0.85, 1.3, 0.45), 0.0)
    for m in range(4):
        poe(x, _rasgo(rng, 0.1, 0.25), 0.22 + 0.012 * m)
        poe(x, _sino(rng, 2093 + 150 * m, 0.25, 0.012, METAL), 0.22 + 0.012 * m)
    poe(x, _baque(150, 70, 0.2, 0.45), 0.24)
    return reverb(x, 0.6, 0.3)


def freddy_preparo(rng, v):
    """Freddy (Preparo): a luva raspando no metal ("skreeee") e a risada baixa (em laço)."""
    x = _z(1.4)
    n = n_de(0.5)
    t = _t(n)
    poe(x, satura(seno(2200 + 300 * np.sin(2 * math.pi * 3 * t), n) + passa(rosa(rng, n), 2000, 7000, 2) * 0.5, 3) * sobe_e_some(n, 0.4, 1.2) * 0.02, 0.0)
    for k in range(3):
        n2 = n_de(0.1)
        poe(x, satura(seno(varre(180, 150, n2), n2), 3) * env(n2, 0.01, 0.08) * 0.02, 0.65 + 0.12 * k)
    return reverb(x, 0.7, 0.35)


def pesadelo_de_freddy(rng, v):
    """Freddy: o pesadelo distorcido e a garra gigante saindo do escuro."""
    x = _z(2.4)
    poe(x, _caixinha(rng, (988, 932, 880, 831), 0.1, 0.015), 0.0)
    n = n_de(0.5)
    poe(x, seno(varre(120, 60, n), n) * env(n, 0.1, 0.4) * 0.04, 0.2)
    poe(x, _whoosh(rng, 0.25, 500, 6000, 0.9, 1.3, 0.5), 0.25)
    for m in range(4):
        poe(x, _rasgo(rng, 0.12, 0.3), 0.42 + 0.012 * m)
    poe(x, _baque(70, 28, 0.6, 0.9, 2.8), 0.45)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Michael Myers

def faca_de_cozinha(rng, v):
    """Michael Myers: o acorde agudo do tema e a faca descendo."""
    x = _z(2.0)
    for k in range(4):
        poe(x, _sino(rng, 1568 if k % 2 == 0 else 1480, 0.18, 0.018, SINO), 0.05 + 0.1 * k)
    poe(x, _whoosh(rng, 0.15, 1000, 8000, 0.7, 1.3, 0.4), 0.3)
    poe(x, _baque(110, 45, 0.35, 0.7, 2.5), 0.42)
    poe(x, _rasgo(rng, 0.12, 0.3), 0.42)
    return reverb(x, 0.6, 0.3)


def respiracao_na_mascara(rng, v):
    """Michael Myers: a respiração pesada dentro da máscara."""
    x = _z(2.4)
    for k in range(2):
        poe(x, _respira(rng, 0.45, 0.35, True), 0.6 * k)
        poe(x, _respira(rng, 0.4, 0.3, False), 0.6 * k + 0.4)
    return reverb(x, 0.7, 0.35)


def myers_preparo(rng, v):
    """Michael Myers (Preparo): o tema em 5/4 no piano agudo (em laço)."""
    x = _z(1.4)
    for k in range(5):
        poe(x, _sino(rng, 1568 if k % 2 == 0 else 1480, 0.18, 0.014, SINO), 0.2 * k)
    n = n_de(1.0)
    poe(x, seno(110, n) * sobe_e_some(n, 0.5, 1.2) * 0.015, 0.0)
    return reverb(x, 0.7, 0.35)


def noite_de_halloween(rng, v):
    """Michael Myers: as abóboras acendendo, o tema e o golpe final."""
    x = _z(2.4)
    for k in range(5):
        poe(x, _sino(rng, 1568 if k % 2 == 0 else 1480, 0.18, 0.018, SINO), 0.04 * k)
    poe(x, _whoosh(rng, 0.2, 800, 7000, 0.85, 1.3, 0.5), 0.2)
    poe(x, _baque(60, 22, 0.8, 1.0, 3.0), 0.38)
    poe(x, _explosao(rng, 0.5, 60), 0.38)
    n = n_de(0.9)
    poe(x, (seno(110, n) + seno(117, n)) * env(n, 0.05, 0.6) * 0.025, 0.4)
    return reverb(x, 0.8, 0.4)


SONS: dict = {
    "gungnir-de-odin": (gungnir_de_odin, "Odin: a Gungnir"),
    "corvos-de-odin": (corvos_de_odin, "Odin: os corvos de Odin"),
    "sabedoria-de-asgard": (sabedoria_de_asgard, "Odin: a sabedoria de Asgard"),
    "mordida-de-fenrir": (mordida_de_fenrir, "Fenrir: a mordida"),
    "uivo-de-fenrir": (uivo_de_fenrir, "Fenrir: o uivo"),
    "fenrir-preparo": (fenrir_preparo, "Fenrir: a corrente esticando (Preparo)"),
    "ragnarok": (ragnarok, "Fenrir: Ragnarök"),
    "toque-da-morte": (toque_da_morte, "Hel: o toque da morte"),
    "exercito-dos-mortos": (exercito_dos_mortos, "Hel: o exército dos mortos"),
    "hel-preparo": (hel_preparo, "Hel: a névoa fria (Preparo)"),
    "frio-de-helheim": (frio_de_helheim, "Hel: o frio de Helheim"),
    "facao-de-jason": (facao_de_jason, "Jason: o facão"),
    "volta-do-lago": (volta_do_lago, "Jason: a volta do lago"),
    "jason-preparo": (jason_preparo, "Jason: o ki-ki-ki ma-ma-ma (Preparo)"),
    "sexta-feira-13": (sexta_feira_13, "Jason: Sexta-feira 13"),
    "cancao-de-ninar": (cancao_de_ninar, "Freddy: a canção de ninar"),
    "garra-de-laminas": (garra_de_laminas, "Freddy: a garra de lâminas"),
    "freddy-preparo": (freddy_preparo, "Freddy: a luva raspando (Preparo)"),
    "pesadelo-de-freddy": (pesadelo_de_freddy, "Freddy: o pesadelo"),
    "faca-de-cozinha": (faca_de_cozinha, "Michael Myers: a faca de cozinha"),
    "respiracao-na-mascara": (respiracao_na_mascara, "Michael Myers: a respiração na máscara"),
    "myers-preparo": (myers_preparo, "Michael Myers: o tema (Preparo)"),
    "noite-de-halloween": (noite_de_halloween, "Michael Myers: a noite de Halloween"),
}
