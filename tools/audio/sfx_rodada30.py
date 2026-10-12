"""Os sons da rodada 30 das habilidades próprias (veja tools/vfx/familias_v2/rodada30.py)."""
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


def _fogo(rng, seg, g=0.3, pico=0.2):
    n = n_de(seg)
    return satura(passa(rosa(rng, n), 150, 3500, 2), 2.5) * sobe_e_some(n, pico, 1.3) * g


# ------------------------------------------------------------------ Hellboy

def teimosia(rng, v):
    """Hellboy: o rosnado teimoso e a pedra cobrindo o corpo (os estalos de rocha)."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, satura(seno(varre(95, 75, n), n) + passa(rosa(rng, n), 100, 1200, 2) * 0.6, 3) * env(n, 0.05, 0.35) * 0.07, 0.0)
    for k in range(6):
        poe(x, _baque(220 + 20 * k, 140, 0.06, 0.25), 0.3 + 0.05 * k)
        poe(x, estalo(rng, n_de(0.03), 600, 3000, 0.008) * 0.4, 0.3 + 0.05 * k)
    return reverb(x, 0.5, 0.25)


def hellboy_preparo(rng, v):
    """Hellboy (Preparo): a Mão da Perdição erguida (o zumbido das runas)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(55, n) + seno(82, n) * 0.5, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.06, 0.0)
    poe(x, _sino(rng, 330, 0.8, 0.04, SINO), 0.2)
    return reverb(x, 0.6, 0.3)


def pancada_final(rng, v):
    """Hellboy: a mão de pedra descendo e o chão rachando."""
    x = _z(2.2)
    poe(x, _whoosh(rng, 0.3, 150, 2000, 0.9, 1.3, 0.5), 0.0)
    poe(x, _baque(45, 20, 0.9, 1.0, 3.2), 0.28)
    poe(x, _explosao(rng, 0.9, 0.5), 0.28)
    q = np.random.default_rng(4)
    for k in range(6):
        poe(x, _baque(q.uniform(150, 280), 90, 0.1, 0.2), 0.45 + q.uniform(0, 0.4))
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Pica-Pau

def risada_irritante(rng, v):
    """Pica-Pau: a risada "ha-ha-ha-HA-ha" (os tons agudos pulando)."""
    x = _z(1.9)
    for k, f in enumerate((700, 850, 1000, 1300, 900)):
        n = n_de(0.1)
        poe(x, satura(seno(varre(f, f * 0.8, n), n), 2) * env(n, 0.005, 0.07) * 0.05, 0.06 * k * 1.3)
    for k in range(3):
        poe(x, _piu(1600, 2100, 0.05, 0.02), 0.5 + 0.07 * k)
    return reverb(x, 0.4, 0.2)


def confusao_total(rng, v):
    """Pica-Pau: as bicadas rapidíssimas e o redemoinho de penas."""
    x = _z(2.0)
    for k in range(10):
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.004) * 0.5, 0.04 * k)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1000, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 8 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.25, 0.3)
    for k in range(3):
        poe(x, _piu(1500 + 200 * k, 2000 + 200 * k, 0.05, 0.02), 0.6 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Pernalonga

def buraco_de_coelho(rng, v):
    """Pernalonga: cavando rapidinho (a terra) e saindo do outro lado (o "pop")."""
    x = _z(1.9)
    for k in range(6):
        poe(x, passa(rosa(rng, n_de(0.06)), 200, 1500, 2) * env(n_de(0.06), 0.003, 0.05) * 0.35, 0.03 + 0.05 * k)
    poe(x, seno(varre(600, 200, n_de(0.25)), n_de(0.25)) * env(n_de(0.25), 0.01, 0.2) * 0.04, 0.3)
    poe(x, _piu(300, 900, 0.08, 0.06), 0.55)
    return reverb(x, 0.4, 0.2)


def disfarce_pernalonga(rng, v):
    """Pernalonga: a fumaça de troca de roupa (o "fuff") e o assobio galanteador."""
    x = _z(1.9)
    poe(x, passa(rosa(rng, n_de(0.3)), 500, 4000, 2) * env(n_de(0.3), 0.005, 0.25) * 0.35, 0.0)
    poe(x, _piu(900, 1500, 0.12, 0.04), 0.45)
    poe(x, _piu(1500, 900, 0.2, 0.04), 0.58)
    return reverb(x, 0.5, 0.25)


def que_que_ha_velhinho(rng, v):
    """Pernalonga: a mordida na cenoura, o assobio da bigorna caindo e o "BONK"."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.04), 800, 4000, 0.008), 0.0)
    poe(x, estalo(rng, n_de(0.04), 800, 4000, 0.008), 0.08)
    n = n_de(0.3)
    poe(x, seno(varre(1800, 600, n), n) * env(n, 0.01, 0.25) * 0.04, 0.25)
    poe(x, _baque(150, 70, 0.3, 0.7, 2.2), 0.55)
    poe(x, _sino(rng, 700, 0.8, 0.08, METAL), 0.55)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Ben 10

def chama_ben10(rng, v):
    """Ben 10: o Chama soltando as bolas de fogo em sequência."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _fogo(rng, 0.4, 0.25, 0.2), 0.08 * k)
        poe(x, _baque(140, 70, 0.2, 0.4), 0.43 + 0.08 * k)
        poe(x, _fogo(rng, 0.4, 0.2, 0.1), 0.45 + 0.08 * k)
    return reverb(x, 0.5, 0.25)


def ben10_preparo(rng, v):
    """Ben 10 (Preparo): o Omnitrix girando (os cliques e o zumbido verde)."""
    x = _z(1.4)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.02), 1200, 5000, 0.004) * 0.4, 0.12 * k)
    n = n_de(1.0)
    poe(x, seno(varre(300, 600, n), n) * sobe_e_some(n, 0.7, 1.2) * 0.03, 0.0)
    return reverb(x, 0.5, 0.25)


def xlr8(rng, v):
    """Ben 10: o XLR8 em alta velocidade (os "vups" em zigue-zague) e o impacto."""
    x = _z(1.8)
    for k in range(4):
        poe(x, _whoosh(rng, 0.1, 1500, 9000, 0.6, 1.4, 0.35), 0.03 + 0.1 * k)
    poe(x, _baque(140, 60, 0.3, 0.6), 0.42)
    return reverb(x, 0.4, 0.2)


# ------------------------------------------------------------------ Samurai Jack

def katana_magica(rng, v):
    """Samurai Jack: o corte limpo da espada mágica e o brilho."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.15, 3000, 12000, 0.8, 1.3, 0.5), 0.05)
    poe(x, _sino(rng, 2637, 0.8, 0.06, METAL), 0.15)
    poe(x, _brilho(rng, 0.6, 2093, 0.04, CRISTAL), 0.3)
    return reverb(x, 0.6, 0.3)


def postura_serena(rng, v):
    """Samurai Jack: a meditação (o vento suave e o sino de templo)."""
    x = _z(2.2)
    poe(x, _sopro(rng, 1.4, 300, 2000, 0.15, 0.4), 0.0)
    poe(x, _sino(rng, 196, 1.6, 0.1, SINO), 0.1)
    poe(x, _acorde((294, 392, 440), 1.2, 0.03, 0.3, 0.9), 0.3)
    return reverb(x, 0.9, 0.45)


def jack_preparo(rng, v):
    """Jack (Preparo): o silêncio antes do corte (o vento parando e o tom fino)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, seno(1800, n) * sobe_e_some(n, 0.8, 1.0) * 0.01, 0.0)
    poe(x, _sopro(rng, 0.8, 400, 2000, 0.08, 0.2), 0.0)
    return reverb(x, 0.8, 0.4)


def corte_decisivo(rng, v):
    """Samurai Jack: o corte num instante (o silvo) e o rival caindo depois."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.08, 4000, 14000, 0.9, 1.2, 0.5), 0.05)
    poe(x, _sino(rng, 3500, 0.9, 0.06, METAL), 0.08)
    poe(x, _baque(110, 50, 0.4, 0.7, 2.2), 0.75)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ He-Man

def espada_do_poder(rng, v):
    """He-Man: a espada erguida, os raios e o golpe."""
    x = _z(2.0)
    poe(x, _sino(rng, 1047, 0.8, 0.05, METAL), 0.0)
    poe(x, _trovao(rng, 0.6, 0.3), 0.05)
    poe(x, _whoosh(rng, 0.2, 800, 6000, 0.8, 1.4, 0.45), 0.4)
    poe(x, _baque(140, 60, 0.3, 0.6), 0.5)
    return reverb(x, 0.6, 0.3)


def heman_preparo(rng, v):
    """He-Man (Preparo): "Pelos poderes de Grayskull…" (o coro subindo e os raios)."""
    x = _z(1.5)
    poe(x, _acorde((196, 247, 294, 392), 1.2, 0.04, 0.4, 0.8), 0.0)
    n = n_de(1.0)
    poe(x, graos(rng, n, 30, 0.0, 0.95, 2000, 8000, 0.003) * 0.25, 0.1)
    return reverb(x, 0.7, 0.35)


def golpe_de_grayskull(rng, v):
    """He-Man: "Eu tenho a força!" (o acorde heroico) e o golpe enorme."""
    x = _z(2.3)
    poe(x, _acorde((262, 330, 392, 523), 0.9, 0.05, 0.02, 0.7), 0.0)
    poe(x, _whoosh(rng, 0.3, 300, 4000, 0.9, 1.3, 0.5), 0.25)
    poe(x, _baque(50, 22, 0.8, 1.0, 3.0), 0.48)
    poe(x, _explosao(rng, 1.0, 0.6), 0.48)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Popeye

def lata_de_espinafre(rng, v):
    """Popeye: a lata espremida, o "glup" e a musiquinha de força."""
    x = _z(2.1)
    poe(x, estalo(rng, n_de(0.05), 800, 4000, 0.01), 0.15)
    poe(x, _piu(300, 150, 0.12, 0.06), 0.35)
    for k, f in enumerate((392, 523, 659, 784)):
        n = n_de(0.12 if k < 3 else 0.4)
        poe(x, (_quadrada(f, n) * 0.3 + seno(f, n)) * env(n, 0.01, 0.1 if k < 3 else 0.35) * 0.035, 0.5 + 0.1 * k)
    return reverb(x, 0.5, 0.25)


def furacao_de_socos(rng, v):
    """Popeye: o braço girando como hélice e os socos em sequência."""
    x = _z(2.0)
    n = n_de(0.45)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 500, 4000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 18 * t) ** 2) * env(n, 0.01, 0.4) * 0.3, 0.0)
    for k in range(6):
        poe(x, _baque(150 + 10 * (k % 2), 70, 0.12, 0.45), 0.39 + 0.06 * k)
    return reverb(x, 0.4, 0.2)


SONS: dict = {
    "teimosia": (teimosia, "Hellboy: a teimosia"),
    "hellboy-preparo": (hellboy_preparo, "Hellboy: a Mão da Perdição (Preparo)"),
    "pancada-final": (pancada_final, "Hellboy: a pancada final"),
    "risada-irritante": (risada_irritante, "Pica-Pau: a risada"),
    "confusao-total": (confusao_total, "Pica-Pau: a confusão total"),
    "buraco-de-coelho": (buraco_de_coelho, "Pernalonga: o buraco de coelho"),
    "disfarce-pernalonga": (disfarce_pernalonga, "Pernalonga: o disfarce"),
    "que-que-ha-velhinho": (que_que_ha_velhinho, "Pernalonga: O que é que há, velhinho?"),
    "chama-ben10": (chama_ben10, "Ben 10: o Chama"),
    "ben10-preparo": (ben10_preparo, "Ben 10: o Omnitrix (Preparo)"),
    "xlr8": (xlr8, "Ben 10: o XLR8"),
    "katana-magica": (katana_magica, "Samurai Jack: a katana mágica"),
    "postura-serena": (postura_serena, "Samurai Jack: a postura serena"),
    "jack-preparo": (jack_preparo, "Samurai Jack: o silêncio (Preparo)"),
    "corte-decisivo": (corte_decisivo, "Samurai Jack: o corte decisivo"),
    "espada-do-poder": (espada_do_poder, "He-Man: a Espada do Poder"),
    "heman-preparo": (heman_preparo, "He-Man: Grayskull (Preparo)"),
    "golpe-de-grayskull": (golpe_de_grayskull, "He-Man: o golpe de Grayskull"),
    "lata-de-espinafre": (lata_de_espinafre, "Popeye: a lata de espinafre"),
    "furacao-de-socos": (furacao_de_socos, "Popeye: o furacão de socos"),
}
