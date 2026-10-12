"""Os sons da rodada 40 das habilidades próprias (veja tools/vfx/familias_v2/rodada40.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _fogo(rng, seg, g=0.3, pico=0.2):
    n = n_de(seg)
    return satura(passa(rosa(rng, n), 150, 3500, 2), 2.5) * sobe_e_some(n, pico, 1.3) * g


def _agua(rng, seg, g=0.3):
    """O som de água em movimento (o borbulhar e o chiado molhado)."""
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 400, 4000, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 11 * t + np.sin(2 * math.pi * 3 * t)))) * sobe_e_some(n, 0.3, 1.2) * g


def _bolhinhas(rng, seg, g=0.03, seed=3):
    x = _z(seg + 0.2)
    q = np.random.default_rng(seed)
    for k in range(int(seg * 16)):
        f = q.uniform(400, 1000)
        poe(x, _piu(f, f * 1.7, 0.035, g), k / 16)
    return x


def _gelo(rng, n_cristais=6, g=0.03):
    x = _z(0.6)
    q = np.random.default_rng(9)
    for k in range(n_cristais):
        poe(x, _sino(rng, q.uniform(2500, 4500), 0.2, g, CRISTAL), 0.06 * k)
        poe(x, estalo(rng, n_de(0.02), 3000, 9000, 0.004) * 0.4, 0.06 * k)
    return x


# ------------------------------------------------------------------ Orihime

def santen_kesshun(rng, v):
    """Orihime: "Santen Kesshun, eu rejeito!" — as três fadas e o escudo vibrando."""
    x = _z(2.0)
    for k, f in enumerate((1175, 1397, 1760)):
        poe(x, _sino(rng, f, 0.5, 0.03, CRISTAL), 0.05 + 0.05 * k)
    n = n_de(0.8)
    poe(x, (seno(392, n) + seno(588, n) * 0.4) * sobe_e_some(n, 0.3, 1.2) * 0.025, 0.25)
    poe(x, _sino(rng, 784, 0.8, 0.03, METAL), 0.3)
    return reverb(x, 0.7, 0.35)


def souten_kisshun(rng, v):
    """Orihime: a cúpula de cura (o zumbido suave e quente) e o brilho."""
    x = _z(2.2)
    for k, f in enumerate((1319, 1568)):
        poe(x, _sino(rng, f, 0.4, 0.025, CRISTAL), 0.05 * k)
    poe(x, _acorde((330, 415, 494, 659), 1.4, 0.03, 0.2, 1.0), 0.15)
    poe(x, graos(rng, n_de(1.0), 25, 0.0, 0.95, 3000, 9000, 0.003) * 0.25, 0.3)
    return reverb(x, 0.8, 0.4)


def orihime_preparo(rng, v):
    """Orihime (Preparo): os seis grampos brilhando em volta (os sininhos em laço)."""
    x = _z(1.4)
    for k in range(6):
        poe(x, _sino(rng, 1568 + 110 * (k % 3), 0.3, 0.015, CRISTAL), 0.16 * k)
    n = n_de(1.0)
    poe(x, seno(523, n) * sobe_e_some(n, 0.6, 1.2) * 0.012, 0.0)
    return reverb(x, 0.6, 0.3)


def rejeicao_total(rng, v):
    """Orihime: a rejeição total — o som rodando de trás para frente e o aliado voltando."""
    x = _z(2.4)
    n = n_de(0.8)
    poe(x, (_acorde((262, 330, 392, 523), 0.8, 0.04, 0.02, 0.7))[::-1], 0.0)
    poe(x, (passa(rosa(rng, n), 1000, 6000, 2) * env(n, 0.01, 0.7) * 0.2)[::-1], 0.0)
    poe(x, _acorde((330, 415, 494, 659), 1.0, 0.035, 0.05, 0.8), 0.85)
    poe(x, _brilho(rng, 0.6, 1760, 0.03, CRISTAL), 0.9)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Aerith

def cura_de_aerith(rng, v):
    """Aerith: a matéria verde (o "plim" clássico de cura) e as flores de luz."""
    x = _z(2.0)
    for k, f in enumerate((523, 659, 784, 1047, 1319)):
        poe(x, _sino(rng, f, 0.5, 0.025, CRISTAL), 0.07 * k)
    poe(x, _acorde((523, 659, 784), 0.9, 0.025, 0.1, 0.7), 0.4)
    return reverb(x, 0.7, 0.35)


def esna(rng, v):
    """Aerith: Esna — os anéis de luz subindo e o mal se desfazendo."""
    x = _z(2.0)
    for k in range(3):
        n = n_de(0.35)
        poe(x, seno(varre(600 + 100 * k, 1200 + 200 * k, n), n) * env(n, 0.05, 0.25) * 0.025, 0.05 + 0.1 * k)
    poe(x, graos(rng, n_de(0.6), 25, 0.0, 0.9, 3000, 9000, 0.003)[::-1] * 0.25, 0.3)
    poe(x, _sino(rng, 1047, 0.6, 0.03, SINO), 0.5)
    return reverb(x, 0.7, 0.35)


def aerith_preparo(rng, v):
    """Aerith (Preparo): a prece (o coro baixinho e a matéria branca pulsando)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(392, n) + seno(494, n) * 0.6 + seno(587, n) * 0.4) * (0.7 + 0.3 * np.sin(2 * math.pi * 1.5 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.018, 0.0)
    poe(x, _brilho(rng, 0.8, 2093, 0.015, CRISTAL), 0.3)
    return reverb(x, 0.8, 0.4)


def grande_bencao(rng, v):
    """Aerith: a Grande bênção — o coro sagrado, as penas caindo e o aliado levantando."""
    x = _z(2.5)
    poe(x, _acorde((294, 370, 440, 587, 740), 1.6, 0.04, 0.3, 1.1), 0.0)
    poe(x, graos(rng, n_de(1.2), 40, 0.0, 0.95, 2500, 9000, 0.003) * 0.25, 0.1)
    poe(x, _sino(rng, 1175, 1.0, 0.035, SINO), 0.5)
    poe(x, _brilho(rng, 0.8, 2349, 0.025, CRISTAL), 0.6)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Katara

def chicote_de_agua_katara(rng, v):
    """Katara: o chicote de água (o "chuá" que estala) e as gotas espirrando."""
    x = _z(1.9)
    poe(x, _agua(rng, 0.45, 0.35), 0.0)
    poe(x, _whoosh(rng, 0.3, 500, 4000, 0.7, 1.3, 0.3), 0.0)
    poe(x, passa(rosa(rng, n_de(0.2)), 1000, 8000, 2) * env(n_de(0.2), 0.003, 0.18) * 0.45, 0.42)
    poe(x, _baque(150, 70, 0.15, 0.35), 0.42)
    poe(x, _bolhinhas(rng, 0.3, 0.02), 0.5)
    return reverb(x, 0.5, 0.25)


def cura_com_agua(rng, v):
    """Katara: a água brilhando nas mãos (o zumbido calmo) e a cura escorrendo."""
    x = _z(2.1)
    poe(x, _agua(rng, 0.8, 0.2), 0.0)
    n = n_de(0.9)
    poe(x, (seno(440, n) + seno(660, n) * 0.4) * sobe_e_some(n, 0.4, 1.2) * 0.025, 0.1)
    poe(x, _acorde((440, 554, 659), 0.8, 0.03, 0.1, 0.6), 0.5)
    return reverb(x, 0.7, 0.35)


def katara_preparo(rng, v):
    """Katara (Preparo): a água subindo do chão em espiral (o redemoinho em laço)."""
    x = _z(1.4)
    poe(x, _agua(rng, 1.0, 0.25), 0.0)
    return reverb(x, 0.5, 0.25)


def prisao_de_gelo_katara(rng, v):
    """Katara: a água enrolando no rival e congelando (o estalo do gelo fechando)."""
    x = _z(2.1)
    poe(x, _agua(rng, 0.45, 0.3), 0.0)
    poe(x, estalo(rng, n_de(0.08), 1000, 6000, 0.012) * 1.0, 0.45)
    poe(x, _gelo(rng, 7, 0.03), 0.47)
    poe(x, _baque(120, 50, 0.3, 0.5), 0.45)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Sailor Mercury

def nevoa_de_bolhas(rng, v):
    """Sailor Mercury: "Névoa de bolhas de Mercúrio!" — as bolhas enchendo tudo."""
    x = _z(2.2)
    poe(x, _bolhinhas(rng, 0.9, 0.025, 4), 0.0)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 800, 5000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.2, 0.05)
    return reverb(x, 0.7, 0.35)


def spray_de_bolhas(rng, v):
    """Sailor Mercury: o jato de bolhas (o "pshhh" com as bolhas estourando) no rival."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 1500, 8000, 2) * env(n, 0.02, 0.4) * 0.3, 0.05)
    poe(x, _bolhinhas(rng, 0.45, 0.025, 7), 0.05)
    poe(x, _baque(150, 70, 0.2, 0.4), 0.3)
    return reverb(x, 0.5, 0.25)


def mercury_preparo(rng, v):
    """Sailor Mercury (Preparo): o anel de água girando e o tom cristalino em laço."""
    x = _z(1.4)
    poe(x, _agua(rng, 1.0, 0.15), 0.0)
    for k in range(4):
        poe(x, _sino(rng, 1760 + 220 * (k % 2), 0.3, 0.012, CRISTAL), 0.25 * k)
    return reverb(x, 0.7, 0.35)


def rapsodia_aquatica(rng, v):
    """Sailor Mercury: a harpa de água tocando (o arpejo) e a onda que congela."""
    x = _z(2.3)
    for k, f in enumerate((523, 659, 784, 988, 1175, 1568)):
        n = n_de(0.4)
        poe(x, seno(f, n) * env(n, 0.003, 0.35) * 0.03, 0.04 * k)
    poe(x, _agua(rng, 0.4, 0.35), 0.25)
    poe(x, _baque(110, 45, 0.3, 0.6), 0.52)
    poe(x, _gelo(rng, 8, 0.03), 0.55)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Kurama

def chicote_de_rosas(rng, v):
    """Kurama: o chicote de espinhos estalando e as pétalas voando."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.35, 600, 6000, 0.7, 1.3, 0.4), 0.0)
    poe(x, estalo(rng, n_de(0.04), 1500, 7000, 0.006) * 1.2, 0.38)
    poe(x, passa(rosa(rng, n_de(0.12)), 2000, 8000, 2) * env(n_de(0.12), 0.003, 0.1) * 0.35, 0.4)
    poe(x, graos(rng, n_de(0.5), 20, 0.0, 0.9, 2000, 7000, 0.003) * 0.25, 0.45)
    return reverb(x, 0.5, 0.25)


def planta_comedora(rng, v):
    """Kurama: a planta carnívora brotando e mordendo (o "nhac" molhado)."""
    x = _z(1.9)
    poe(x, satura(passa(rosa(rng, n_de(0.2)), 100, 1200, 2), 2) * env(n_de(0.2), 0.005, 0.18) * 0.3, 0.0)
    poe(x, _piu(300, 700, 0.2, 0.03), 0.05)
    poe(x, estalo(rng, n_de(0.06), 500, 3000, 0.012) * 1.0, 0.42)
    poe(x, _baque(170, 80, 0.15, 0.45), 0.42)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 300, 2000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 8 * _t(n)) ** 2) * env(n, 0.05, 0.4) * 0.2, 0.5)
    return reverb(x, 0.4, 0.2)


def kurama_preparo(rng, v):
    """Kurama (Preparo): a rosa girando e as pétalas no vento (o sopro em laço)."""
    x = _z(1.4)
    poe(x, _sopro(rng, 1.0, 800, 5000, 0.12, 0.5), 0.0)
    poe(x, graos(rng, n_de(1.0), 20, 0.0, 0.95, 2500, 8000, 0.003) * 0.2, 0.0)
    return reverb(x, 0.6, 0.3)


def arvore_da_ilusao(rng, v):
    """Kurama: a árvore crescendo (o rangido de galhos) e a ilusão ondulando."""
    x = _z(2.3)
    for k in range(6):
        n = n_de(0.12)
        poe(x, satura(seno(varre(200 + 30 * k, 150 + 30 * k, n), n) * (0.5 + 0.5 * np.sin(2 * math.pi * 30 * _t(n))), 3) * env(n, 0.01, 0.1) * 0.04, 0.08 * k)
    n = n_de(0.9)
    t = _t(n)
    poe(x, (seno(330 + 40 * np.sin(2 * math.pi * 3 * t), n) + seno(494 + 60 * np.sin(2 * math.pi * 2.3 * t), n) * 0.5) * sobe_e_some(n, 0.3, 1.2) * 0.025, 0.4)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Ken Masters

def hadouken_ken(rng, v):
    """Ken: "Hadouken!" — as mãos juntando a energia e a bola voando."""
    x = _z(2.0)
    n = n_de(0.25)
    poe(x, seno(varre(300, 900, n), n) * env(n, 0.2, 0.04) * 0.04, 0.0)
    n = n_de(0.35)
    poe(x, satura(seno(varre(500, 350, n), n) + passa(rosa(rng, n), 300, 3000, 2) * 0.4, 2.5) * env(n, 0.01, 0.3) * 0.06, 0.22)
    poe(x, _baque(110, 45, 0.4, 0.7), 0.55)
    poe(x, _explosao(rng, 0.4, 70), 0.55)
    return reverb(x, 0.5, 0.25)


def tatsumaki_ken(rng, v):
    """Ken: o chute giratório de fogo (o "vuvuvu" das chamas) e os acertos."""
    x = _z(2.0)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 300, 4000, 2) * (0.4 + 0.6 * np.sin(2 * math.pi * 10 * _t(n)) ** 2) * env(n, 0.02, 0.4) * 0.35, 0.0)
    poe(x, _fogo(rng, 0.6, 0.2, 0.3), 0.0)
    for k in range(3):
        poe(x, _baque(150, 65, 0.15, 0.45), 0.22 + 0.12 * k)
    return reverb(x, 0.5, 0.25)


def ken_preparo(rng, v):
    """Ken (Preparo): o punho pegando fogo (o chiado das chamas em laço)."""
    x = _z(1.4)
    poe(x, _fogo(rng, 1.0, 0.2, 0.5), 0.0)
    n = n_de(1.0)
    poe(x, satura(seno(varre(100, 140, n), n), 2) * sobe_e_some(n, 0.7, 1.2) * 0.03, 0.0)
    return reverb(x, 0.5, 0.25)


def shinryuken(rng, v):
    """Ken: "Shinryuken!" — o gancho subindo no redemoinho de fogo como um dragão."""
    x = _z(2.3)
    poe(x, _baque(80, 30, 0.6, 0.9, 2.8), 0.12)
    n = n_de(0.8)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 150, 4000, 2), 3) * (0.5 + 0.5 * np.sin(2 * math.pi * 12 * t) ** 2) * sobe_e_some(n, 0.25, 1.3) * 0.45, 0.05)
    poe(x, satura(seno(varre(100, 400, n), n), 2) * sobe_e_some(n, 0.3, 1.2) * 0.05, 0.05)
    poe(x, _explosao(rng, 0.5, 70), 0.15)
    return reverb(x, 0.7, 0.35)


SONS: dict = {
    "santen-kesshun": (santen_kesshun, "Orihime: Santen Kesshun"),
    "souten-kisshun": (souten_kisshun, "Orihime: Souten Kisshun"),
    "orihime-preparo": (orihime_preparo, "Orihime: os grampos brilhando (Preparo)"),
    "rejeicao-total": (rejeicao_total, "Orihime: a rejeição total"),
    "cura-de-aerith": (cura_de_aerith, "Aerith: Cura"),
    "esna": (esna, "Aerith: Esna"),
    "aerith-preparo": (aerith_preparo, "Aerith: a prece (Preparo)"),
    "grande-bencao": (grande_bencao, "Aerith: a Grande bênção"),
    "chicote-de-agua-katara": (chicote_de_agua_katara, "Katara: o chicote de água"),
    "cura-com-agua": (cura_com_agua, "Katara: a cura com água"),
    "katara-preparo": (katara_preparo, "Katara: a água em espiral (Preparo)"),
    "prisao-de-gelo-katara": (prisao_de_gelo_katara, "Katara: a prisão de gelo"),
    "nevoa-de-bolhas": (nevoa_de_bolhas, "Sailor Mercury: a névoa de bolhas"),
    "spray-de-bolhas": (spray_de_bolhas, "Sailor Mercury: o spray de bolhas"),
    "mercury-preparo": (mercury_preparo, "Sailor Mercury: o anel de água (Preparo)"),
    "rapsodia-aquatica": (rapsodia_aquatica, "Sailor Mercury: a rapsódia aquática"),
    "chicote-de-rosas": (chicote_de_rosas, "Kurama: o chicote de rosas"),
    "planta-comedora": (planta_comedora, "Kurama: a planta comedora"),
    "kurama-preparo": (kurama_preparo, "Kurama: a rosa girando (Preparo)"),
    "arvore-da-ilusao": (arvore_da_ilusao, "Kurama: a árvore da ilusão"),
    "hadouken-ken": (hadouken_ken, "Ken: Hadouken"),
    "tatsumaki-ken": (tatsumaki_ken, "Ken: Tatsumaki"),
    "ken-preparo": (ken_preparo, "Ken: o punho em chamas (Preparo)"),
    "shinryuken": (shinryuken, "Ken: Shinryuken"),
}
