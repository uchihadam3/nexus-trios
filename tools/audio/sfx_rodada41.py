"""Os sons da rodada 41 das habilidades próprias (veja tools/vfx/familias_v2/rodada41.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _estrelinhas(rng, x, em, n=3):
    for k in range(n):
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.02, CRISTAL), em + 0.07 * k)


def _fogo(rng, seg, g=0.3, pico=0.2):
    n = n_de(seg)
    return satura(passa(rosa(rng, n), 150, 3500, 2), 2.5) * sobe_e_some(n, pico, 1.3) * g


def _estica(rng, seg, f0, f1, g=0.04):
    n = n_de(seg)
    t = _t(n)
    return seno(varre(f0, f1, n), n) * (1 + 0.5 * np.sin(2 * math.pi * 22 * t)) * env(n, 0.01, seg * 0.7) * g


# ------------------------------------------------------------------ Heihachi

def punho_do_deus_do_trovao(rng, v):
    """Heihachi: o soco com o trovão enrolado (o estalo elétrico e o impacto)."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 300, 3000, 0.8, 1.3, 0.5), 0.0)
    poe(x, _baque(100, 40, 0.4, 0.8, 2.6), 0.28)
    poe(x, _trovao(rng, 0.45, 0.45), 0.28)
    return reverb(x, 0.5, 0.25)


def postura_demoniaca(rng, v):
    """Heihachi: a aura demoníaca (o rugido grave e os estalos) e as placas de defesa."""
    x = _z(2.1)
    n = n_de(0.8)
    poe(x, satura(seno(varre(70, 55, n), n) + passa(rosa(rng, n), 60, 600, 2) * 0.5, 3) * sobe_e_some(n, 0.3, 1.2) * 0.07, 0.0)
    for k in range(6):
        poe(x, _sino(rng, 440 + 60 * k, 0.25, 0.02, METAL), 0.35 + 0.04 * k)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.02), 2000, 8000, 0.004) * 0.5, 0.2 + 0.15 * k)
    return reverb(x, 0.6, 0.3)


def heihachi_preparo(rng, v):
    """Heihachi (Preparo): as faíscas juntando no punho (o zumbido elétrico em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (_quadrada(60, n) * 0.3 + seno(120, n)) * (0.6 + 0.4 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(n, 0.7, 1.2) * 0.03, 0.0)
    for k in range(10):
        poe(x, estalo(rng, n_de(0.02), 2000, 9000, 0.004) * 0.4, 0.09 * k)
    return reverb(x, 0.5, 0.25)


def raio_do_mishima(rng, v):
    """Heihachi: o Raio do Mishima — o trovão enorme rasgando até o rival."""
    x = _z(2.3)
    poe(x, _trovao(rng, 0.9, 0.7), 0.1)
    poe(x, _baque(60, 22, 0.8, 1.0, 3.0), 0.18)
    poe(x, _explosao(rng, 0.6, 55), 0.2)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Jake

def punho_gigante_jake(rng, v):
    """Jake: o punho inchando no caminho ("bluuum") e a pancada enorme."""
    x = _z(1.9)
    poe(x, _estica(rng, 0.35, 150, 500, 0.05), 0.0)
    poe(x, _baque(70, 28, 0.6, 1.0, 2.8), 0.33)
    poe(x, estalo(rng, n_de(0.05), 500, 3000, 0.012), 0.33)
    return reverb(x, 0.5, 0.25)


def escudo_elastico_jake(rng, v):
    """Jake: o corpo esticando em cúpula e balançando (o "boing" de borracha)."""
    x = _z(2.0)
    poe(x, _estica(rng, 0.4, 120, 380, 0.05), 0.0)
    for k in range(3):
        poe(x, _estica(rng, 0.15, 300 - 40 * k, 360 - 40 * k, 0.03), 0.4 + 0.12 * k)
    poe(x, _brilho(rng, 0.5, 1047, 0.025, CRISTAL), 0.4)
    return reverb(x, 0.5, 0.25)


def jake_preparo(rng, v):
    """Jake (Preparo): o corpo inchando e desinchando (o tom elástico em laço)."""
    x = _z(1.4)
    for k in range(3):
        poe(x, _estica(rng, 0.3, 120, 220, 0.04), 0.33 * k)
    return reverb(x, 0.4, 0.2)


def jake_gigante(rng, v):
    """Jake: a pata gigante pisando ("BUUUM") e o chão tremendo."""
    x = _z(2.3)
    poe(x, _whoosh(rng, 0.35, 100, 1500, 0.9, 1.3, 0.5), 0.0)
    poe(x, _baque(40, 16, 1.2, 1.0, 3.4), 0.33)
    poe(x, _explosao(rng, 0.9, 40), 0.33)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 40, 300, 2) * sobe_e_some(n, 0.1, 1.2) * 0.6, 0.35)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Marceline

def mordida_de_marceline(rng, v):
    """Marceline: a mordida (o "nhac" e o sibilo) e a vida sendo sugada."""
    x = _z(2.0)
    poe(x, passa(rosa(rng, n_de(0.2)), 3000, 9000, 2) * env(n_de(0.2), 0.05, 0.1) * 0.2, 0.0)
    poe(x, estalo(rng, n_de(0.05), 600, 4000, 0.01) * 1.0, 0.33)
    n = n_de(0.45)
    poe(x, seno(varre(500, 250, n), n) * env(n, 0.05, 0.35) * 0.03, 0.45)
    poe(x, _acorde((220, 262, 311), 0.6, 0.025, 0.05, 0.5), 0.6)
    return reverb(x, 0.6, 0.3)


def baixo_machado(rng, v):
    """Marceline: o baixo-machado girando e o acorde grave distorcido no golpe."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.35, 200, 2500, 0.85, 1.3, 0.5), 0.0)
    poe(x, _baque(80, 30, 0.5, 0.9, 2.8), 0.33)
    n = n_de(0.7)
    poe(x, satura(seno(55, n) + seno(82.4, n) * 0.6 + seno(110, n) * 0.4, 4) * env(n, 0.005, 0.6) * 0.06, 0.33)
    return reverb(x, 0.6, 0.3)


def marceline_preparo(rng, v):
    """Marceline (Preparo): as asas se formando e o sussurro vampiro em laço."""
    x = _z(1.4)
    for k in range(3):
        poe(x, _sopro(rng, 0.2, 300, 2000, 0.15, 0.3), 0.33 * k)
    n = n_de(1.0)
    poe(x, seno(varre(150, 180, n), n) * sobe_e_some(n, 0.6, 1.2) * 0.025, 0.0)
    return reverb(x, 0.7, 0.35)


def forma_de_morcego(rng, v):
    """Marceline: o morcego gigante (as asas batendo, o guincho e o sugar de vida)."""
    x = _z(2.3)
    for k in range(5):
        poe(x, _sopro(rng, 0.15, 200, 2000, 0.25, 0.3), 0.12 * k)
    n = n_de(0.3)
    poe(x, satura(seno(varre(2500, 1800, n), n), 3) * env(n, 0.01, 0.25) * 0.025, 0.3)
    poe(x, _baque(80, 35, 0.4, 0.7), 0.45)
    n = n_de(0.6)
    poe(x, seno(varre(600, 200, n), n) * env(n, 0.05, 0.5) * 0.03, 0.6)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Robin

def bastao_retratil(rng, v):
    """Robin: o bastão estendendo ("tchic-tchic") e a pancada."""
    x = _z(1.8)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.02), 2000, 7000, 0.004) * 0.7, 0.1 + 0.04 * k)
        poe(x, _sino(rng, 1760 + 220 * k, 0.15, 0.015, METAL), 0.1 + 0.04 * k)
    poe(x, _baque(150, 70, 0.25, 0.5), 0.27)
    return reverb(x, 0.4, 0.2)


def batarangue_robin(rng, v):
    """Robin: o bumerangue girando no ar (o zunido que vai e volta) e o acerto."""
    x = _z(2.0)
    n = n_de(0.85)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.4 + 0.6 * np.sin(2 * math.pi * 20 * t) ** 2) * (0.5 + 0.5 * np.sin(math.pi * t / t[-1])) * 0.25, 0.0)
    poe(x, _sino(rng, 1397, 0.3, 0.03, METAL), 0.4)
    poe(x, _baque(170, 80, 0.15, 0.4), 0.4)
    return reverb(x, 0.5, 0.25)


def robin_preparo(rng, v):
    """Robin (Preparo): os bumerangues prontos e a capa no vento (em laço)."""
    x = _z(1.4)
    poe(x, _sopro(rng, 1.0, 400, 3000, 0.12, 0.5), 0.0)
    for k in range(2):
        poe(x, _sino(rng, 2093, 0.2, 0.012, METAL), 0.1 + 0.5 * k)
    return reverb(x, 0.4, 0.2)


def ataque_em_dupla(rng, v):
    """Robin: os dois heróis cruzando em X (dois "zuuum") e o golpe junto."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.3, 600, 6000, 0.8, 1.3, 0.5), 0.0)
    poe(x, _whoosh(rng, 0.3, 500, 5000, 0.8, 1.3, 0.5), 0.08)
    poe(x, _baque(90, 35, 0.5, 0.9, 2.6), 0.25)
    poe(x, estalo(rng, n_de(0.05), 800, 4000, 0.012), 0.25)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Luigi

def bola_de_fogo_verde(rng, v):
    """Luigi: a bola de fogo quicando ("pin-pin-pin") e queimando o rival."""
    x = _z(1.9)
    for k in range(3):
        poe(x, _piu(900, 600, 0.06, 0.035), 0.1 + 0.18 * k)
    poe(x, _fogo(rng, 0.5, 0.25, 0.1), 0.55)
    poe(x, _baque(170, 80, 0.12, 0.3), 0.55)
    return reverb(x, 0.4, 0.2)


def poltergust(rng, v):
    """Luigi: o aspirador Poltergust sugando (o ronco e o vento)."""
    x = _z(2.0)
    n = n_de(0.9)
    t = _t(n)
    poe(x, (passa(rosa(rng, n), 200, 3000, 2) * 0.6 + _quadrada(90, n) * 0.08) * (0.8 + 0.2 * np.sin(2 * math.pi * 30 * t)) * sobe_e_some(n, 0.2, 1.2) * 0.4, 0.0)
    poe(x, seno(varre(200, 400, n), n) * sobe_e_some(n, 0.3, 1.2) * 0.02, 0.0)
    return reverb(x, 0.4, 0.2)


def luigi_preparo(rng, v):
    """Luigi (Preparo): o tremor carregando o míssil (o tom que sobe em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(varre(200, 700, n), n) * (0.7 + 0.3 * np.sin(2 * math.pi * 30 * t)) * sobe_e_some(n, 0.8, 1.2) * 0.025, 0.0)
    return reverb(x, 0.4, 0.2)


def missil_luigi(rng, v):
    """Luigi: o voo de cabeça ("uaaaah!") e o impacto enorme."""
    x = _z(2.2)
    n = n_de(0.32)
    poe(x, satura(seno(varre(400, 700, n), n), 2) * env(n, 0.02, 0.1) * 0.035, 0.0)
    poe(x, _whoosh(rng, 0.32, 500, 8000, 0.9, 1.4, 0.6), 0.0)
    poe(x, _baque(60, 22, 0.8, 1.0, 3.0), 0.32)
    poe(x, _explosao(rng, 0.7, 60), 0.32)
    _estrelinhas(rng, x, 0.55, 4)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Princesa Peach

def sombrinha(rng, v):
    """Peach: a sombrinha abrindo ("flup") e o brilho real."""
    x = _z(2.0)
    poe(x, passa(rosa(rng, n_de(0.15)), 800, 4000, 2) * env(n_de(0.15), 0.01, 0.12) * 0.3, 0.1)
    poe(x, _piu(600, 1100, 0.12, 0.03), 0.15)
    poe(x, _brilho(rng, 0.6, 1568, 0.03, CRISTAL), 0.35)
    poe(x, _acorde((523, 659, 784), 0.8, 0.025, 0.05, 0.6), 0.35)
    return reverb(x, 0.6, 0.3)


def bolo_de_cura(rng, v):
    """Peach: o bolo aparecendo (os sininhos), as velinhas e o coração de cura."""
    x = _z(2.1)
    for k, f in enumerate((784, 988, 1175, 1568)):
        poe(x, _sino(rng, f, 0.4, 0.025, CRISTAL), 0.06 * k)
    poe(x, _acorde((523, 659, 784, 1047), 1.0, 0.03, 0.1, 0.8), 0.45)
    return reverb(x, 0.6, 0.3)


def peach_preparo(rng, v):
    """Peach (Preparo): a coroa brilhando (os brilhos em laço)."""
    x = _z(1.4)
    for k in range(5):
        poe(x, _sino(rng, 2093 + 200 * (k % 3), 0.25, 0.012, CRISTAL), 0.2 * k)
    return reverb(x, 0.6, 0.3)


def vibe_da_princesa(rng, v):
    """Peach: a vibe da princesa (a melodia alegre) nas ondas cor-de-rosa."""
    x = _z(2.4)
    for k, f in enumerate((523, 659, 784, 1047, 784, 1047, 1319)):
        n = n_de(0.12 if k < 6 else 0.5)
        poe(x, (seno(f, n) + seno(f * 2, n) * 0.2) * env(n, 0.01, 0.1 if k < 6 else 0.45) * 0.035, 0.1 * k)
    poe(x, graos(rng, n_de(1.0), 30, 0.0, 0.9, 3000, 9000, 0.003) * 0.2, 0.2)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "punho-do-deus-do-trovao": (punho_do_deus_do_trovao, "Heihachi: o punho do deus do trovão"),
    "postura-demoniaca": (postura_demoniaca, "Heihachi: a postura demoníaca"),
    "heihachi-preparo": (heihachi_preparo, "Heihachi: as faíscas no punho (Preparo)"),
    "raio-do-mishima": (raio_do_mishima, "Heihachi: o raio do Mishima"),
    "punho-gigante-jake": (punho_gigante_jake, "Jake: o punho gigante"),
    "escudo-elastico-jake": (escudo_elastico_jake, "Jake: o escudo elástico"),
    "jake-preparo": (jake_preparo, "Jake: o corpo inchando (Preparo)"),
    "jake-gigante": (jake_gigante, "Jake: Jake gigante"),
    "mordida-de-marceline": (mordida_de_marceline, "Marceline: a mordida"),
    "baixo-machado": (baixo_machado, "Marceline: o baixo-machado"),
    "marceline-preparo": (marceline_preparo, "Marceline: as asas se formando (Preparo)"),
    "forma-de-morcego": (forma_de_morcego, "Marceline: a forma de morcego"),
    "bastao-retratil": (bastao_retratil, "Robin: o bastão retrátil"),
    "batarangue-robin": (batarangue_robin, "Robin: o batarangue"),
    "robin-preparo": (robin_preparo, "Robin: os bumerangues prontos (Preparo)"),
    "ataque-em-dupla": (ataque_em_dupla, "Robin: o ataque em dupla"),
    "bola-de-fogo-verde": (bola_de_fogo_verde, "Luigi: a bola de fogo verde"),
    "poltergust": (poltergust, "Luigi: o Poltergust"),
    "luigi-preparo": (luigi_preparo, "Luigi: carregando o míssil (Preparo)"),
    "missil-luigi": (missil_luigi, "Luigi: o Míssil Luigi"),
    "sombrinha": (sombrinha, "Princesa Peach: a sombrinha"),
    "bolo-de-cura": (bolo_de_cura, "Princesa Peach: o bolo de cura"),
    "peach-preparo": (peach_preparo, "Princesa Peach: a coroa brilhando (Preparo)"),
    "vibe-da-princesa": (vibe_da_princesa, "Princesa Peach: a vibe da princesa"),
}
