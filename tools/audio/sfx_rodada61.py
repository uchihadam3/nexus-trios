"""Os sons da rodada 61 das habilidades próprias (veja tools/vfx/familias_v2/rodada61.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _choque(rng, seg, g=0.2):
    x = _z(seg + 0.05)
    q = np.random.default_rng(61)
    for k in range(int(seg * 40)):
        poe(x, estalo(rng, n_de(0.012), 2500, 9000, 0.002) * g * q.uniform(0.3, 1.0), q.uniform(0, seg))
    return x


def _raio_scifi(rng, seg, f0=1200, f1=300, g=0.04):
    """O raio de ficção científica ("piu-iu-iu" com zumbido)."""
    n = n_de(seg)
    t = _t(n)
    return (seno(varre(f0, f1, n), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 40 * t)) + passa(rosa(rng, n), 2000, 8000, 2) * 0.3) * env(n, 0.01, seg * 0.7) * g


def _maquina(rng, seg, g=0.2):
    """O motor do robô (o zumbido com os servos)."""
    n = n_de(seg)
    t = _t(n)
    return (satura(seno(80 + 20 * np.sin(2 * math.pi * 2 * t), n), 3) * 0.3 + passa(rosa(rng, n), 300, 2000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t)) * 0.5) * sobe_e_some(n, 0.4, 1.2) * g


def _puf(rng, g=0.3):
    """O "puf" mágico: o sopro curto e o brilhinho."""
    n = n_de(0.25)
    return passa(rosa(rng, n), 400, 4000, 2) * env(n, 0.005, 0.15) * g


def _bloco(rng, g=0.4):
    """O bloco de pedra pousando (o "toc" quadrado do jogo de blocos)."""
    n = n_de(0.12)
    return (satura(seno(varre(180, 120, n), n), 2) * env(n, 0.002, 0.06) * 0.5 + passa(rosa(rng, n), 200, 2500, 2) * env(n, 0.001, 0.04)) * g


# ------------------------------------------------------------------ Dexter

def raio_do_laboratorio(rng, v):
    """Dexter: a pistola de raio carregando e o choque elétrico no rival."""
    x = _z(2.0)
    n = n_de(0.2)
    poe(x, seno(varre(400, 1600, n), n) * env(n, 0.15, 0.05) * 0.02, 0.0)
    poe(x, _raio_scifi(rng, 0.4, 1600, 400, 0.04), 0.2)
    poe(x, _choque(rng, 0.5, 0.2), 0.32)
    return reverb(x, 0.6, 0.3)


def gerador_de_carga(rng, v):
    """Dexter: o gerador ligando (o zumbido subindo) e os raios indo para o trio."""
    x = _z(2.0)
    n = n_de(0.9)
    t = _t(n)
    poe(x, satura(seno(60 + 60 * t, n) * (0.6 + 0.4 * np.sin(2 * math.pi * 50 * t)), 3) * sobe_e_some(n, 0.5, 1.2) * 0.03, 0.0)
    for k in range(3):
        poe(x, _choque(rng, 0.2, 0.18), 0.2 + 0.07 * k)
    poe(x, _acorde((523, 659, 784), 0.6, 0.018), 0.5)
    return reverb(x, 0.6, 0.3)


def dexter_preparo(rng, v):
    """Dexter (Preparo): os botões do controle e os bipes do laboratório (em laço)."""
    x = _z(1.4)
    for k in range(6):
        poe(x, _piu(800 + 200 * (k % 3), 800 + 200 * (k % 3), 0.05, 0.012), 0.05 + 0.2 * k)
    poe(x, _maquina(rng, 1.1, 0.08), 0.0)
    return reverb(x, 0.5, 0.25)


def robo_gigante_dexter(rng, v):
    """Dexter: o robô gigante (os passos de metal, os servos) e o punho esmagando o rival."""
    x = _z(2.6)
    poe(x, _maquina(rng, 0.5, 0.2), 0.0)
    for k in range(2):
        poe(x, _baque(60, 30, 0.3, 0.6, 2.4), 0.05 + 0.15 * k)
        poe(x, _sino(rng, 147, 0.3, 0.02, METAL), 0.05 + 0.15 * k)
    poe(x, _whoosh(rng, 0.3, 80, 1500, 0.9, 1.3, 0.55), 0.15)
    poe(x, _baque(32, 12, 1.4, 1.0, 3.6), 0.4)
    poe(x, _sino(rng, 110, 0.8, 0.05, METAL), 0.4)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Aku

def olhos_de_laser_aku(rng, v):
    """Aku: a risada grave e os dois lasers dos olhos."""
    x = _z(2.1)
    for k in range(3):
        n = n_de(0.15)
        poe(x, satura(seno(varre(110, 95, n), n), 3) * env(n, 0.01, 0.1) * 0.04, 0.0 + 0.16 * k)
    n = n_de(0.5)
    t = _t(n)
    poe(x, (seno(varre(900, 600, n), n) + seno(varre(1350, 900, n), n) * 0.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 30 * t)) * env(n, 0.02, 0.35) * 0.04, 0.25)
    poe(x, _baque(80, 40, 0.3, 0.6), 0.35)
    return reverb(x, 0.9, 0.45)


def forma_sem_forma(rng, v):
    """Aku: o corpo de sombra se desfazendo em fumaça e voltando (o sopro grave)."""
    x = _z(2.0)
    poe(x, _sopro(rng, 0.8, 80, 800, 0.35, 0.4), 0.05)
    n = n_de(0.8)
    poe(x, seno(varre(220, 110, n), n) * sobe_e_some(n, 0.3, 1.2) * 0.02, 0.1)
    poe(x, _sopro(rng, 0.5, 100, 900, 0.25, 0.7), 0.6)
    return reverb(x, 1.0, 0.5)


def aku_preparo(rng, v):
    """Aku (Preparo): o redemoinho escuro girando e o coro grave (em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 100, 1200, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.2, 0.0)
    poe(x, _acorde((73, 87, 110), 1.1, 0.02, 0.3, 0.5), 0.0)
    return reverb(x, 0.9, 0.45)


def portal_do_tempo_aku(rng, v):
    """Aku: o portal do tempo abrindo (o redemoinho e o tique-taque) e puxando todos."""
    x = _z(2.9)
    n = n_de(1.2)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 100, 2000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * (3 + 4 * t) * t)) * sobe_e_some(n, 0.5, 1.2) * 0.3, 0.0)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.03), 2500, 7000, 0.004) * 0.25, 0.1 + 0.15 * k)
    poe(x, _acorde((65, 98, 123, 147), 1.4, 0.03, 0.2, 0.8), 0.4)
    poe(x, _baque(35, 14, 1.0, 0.9, 3.0), 0.55)
    return reverb(x, 1.1, 0.55)


# ------------------------------------------------------------------ Megamente

def arma_de_desidratar(rng, v):
    """Megamente: o "piu-piu-piu" da arma de desidratar e o rival virando cubinho ("plop")."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _raio_scifi(rng, 0.12, 1800, 900, 0.03), 0.2 + 0.06 * k)
    n = n_de(0.15)
    poe(x, seno(varre(600, 200, n), n) * env(n, 0.005, 0.1) * 0.05, 0.45)
    poe(x, _sino(rng, 1047, 0.3, 0.02, CRISTAL), 0.48)
    return reverb(x, 0.6, 0.3)


def disfarce_megamente(rng, v):
    """Megamente: o relógio do disfarce ("bip"), a imagem chiando e o rival confuso."""
    x = _z(2.0)
    poe(x, _piu(1500, 1500, 0.06, 0.02), 0.05)
    n = n_de(0.7)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2000, 9000, 2) * (0.5 + 0.5 * np.sign(np.sin(2 * math.pi * 15 * t))) * env(n, 0.05, 0.4) * 0.12, 0.15)
    poe(x, _piu(400, 900, 0.3, 0.015), 0.55)
    return reverb(x, 0.6, 0.3)


def megamente_preparo(rng, v):
    """Megamente (Preparo): as engrenagens girando e o "mwahaha" baixinho (em laço)."""
    x = _z(1.4)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.003) * 0.2, 0.05 + 0.16 * k)
    for k in range(3):
        n = n_de(0.12)
        poe(x, seno(varre(220, 200, n), n) * env(n, 0.01, 0.08) * 0.02, 0.4 + 0.15 * k)
    return reverb(x, 0.6, 0.3)


def robo_mecha(rng, v):
    """Megamente: o braço do robô mecha esticando (os servos) e a garra socando."""
    x = _z(2.3)
    poe(x, _maquina(rng, 0.4, 0.2), 0.0)
    n = n_de(0.25)
    poe(x, seno(varre(300, 900, n), n) * env(n, 0.02, 0.2) * 0.02, 0.1)
    poe(x, _baque(45, 18, 1.0, 1.0, 3.2), 0.35)
    poe(x, _sino(rng, 165, 0.6, 0.04, METAL), 0.35)
    poe(x, _explosao(rng, 0.45, 50), 0.36)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Vilgax

def tentaculos_vilgax(rng, v):
    """Vilgax: os tentáculos do rosto se esticando ("schlurp") e agarrando."""
    x = _z(2.1)
    for k in range(4):
        n = n_de(0.15)
        poe(x, satura(passa(rosa(rng, n), 200, 1500, 2), 3) * env(n, 0.02, 0.1) * 0.15, 0.05 + 0.08 * k)
    n = n_de(0.5)
    poe(x, satura(seno(varre(90, 60, n), n), 3) * env(n, 0.05, 0.3) * 0.05, 0.4)
    return reverb(x, 0.8, 0.4)


def armadura_de_batalha_vilgax(rng, v):
    """Vilgax: as placas da armadura fechando ("clank-clank-clank")."""
    x = _z(2.1)
    for k in range(5):
        poe(x, _sino(rng, 196 + 30 * k, 0.3, 0.03, METAL), 0.1 + 0.06 * k)
        poe(x, _baque(150, 80, 0.08, 0.25), 0.1 + 0.06 * k)
    poe(x, _acorde((147, 196, 247), 0.8, 0.02), 0.45)
    return reverb(x, 0.8, 0.4)


def vilgax_preparo(rng, v):
    """Vilgax (Preparo): o punho cerrando e o rosnado alienígena (em laço)."""
    x = _z(1.4)
    n = n_de(1.1)
    t = _t(n)
    poe(x, satura(seno(70, n) * (1 + 0.1 * np.sin(2 * math.pi * 18 * t)) + passa(rosa(rng, n), 80, 700, 2) * 0.6, 4) * sobe_e_some(n, 0.5, 1.2) * 0.03, 0.0)
    return reverb(x, 0.7, 0.35)


def soco_planetario(rng, v):
    """Vilgax: o soco que afunda o chão (o estrondo e a terra caindo)."""
    x = _z(2.6)
    poe(x, _whoosh(rng, 0.3, 60, 1200, 0.9, 1.3, 0.6), 0.1)
    poe(x, _baque(28, 10, 1.6, 1.0, 4.0), 0.37)
    poe(x, _explosao(rng, 0.9, 30), 0.37)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 40, 800, 2) * sobe_e_some(n, 0.2, 1.2) * 0.5, 0.4)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Cosmo e Wanda

def desejo_de_forca(rng, v):
    """Cosmo e Wanda: "Desejo concedido!" — as varinhas, os três "puf" e o brilho de força."""
    x = _z(2.1)
    poe(x, _brilho(rng, 0.4, 1568, 0.03, CRISTAL), 0.0)
    for k in range(3):
        poe(x, _puf(rng, 0.3), 0.25 + 0.06 * k)
        poe(x, _brilho(rng, 0.3, 1976 + 220 * k, 0.015, CRISTAL), 0.27 + 0.06 * k)
    poe(x, _acorde((392, 494, 587, 784), 0.7, 0.02), 0.5)
    return reverb(x, 0.8, 0.4)


def desejo_de_protecao(rng, v):
    """Cosmo e Wanda: os "puf" e as bolhas de proteção com o acorde doce."""
    x = _z(2.1)
    poe(x, _brilho(rng, 0.4, 1319, 0.03, CRISTAL), 0.0)
    for k in range(3):
        poe(x, _puf(rng, 0.28), 0.25 + 0.06 * k)
        n = n_de(0.15)
        poe(x, seno(varre(400, 800, n), n) * env(n, 0.01, 0.1) * 0.02, 0.35 + 0.06 * k)
    poe(x, _acorde((523, 659, 784), 0.8, 0.022), 0.5)
    return reverb(x, 0.9, 0.45)


def cosmowanda_preparo(rng, v):
    """Cosmo e Wanda (Preparo): as varinhas cintilando e as estrelinhas caindo (em laço)."""
    x = _z(1.4)
    for k in range(6):
        poe(x, _brilho(rng, 0.25, 1568 + 180 * (k % 4), 0.012, CRISTAL), 0.05 + 0.2 * k)
    return reverb(x, 0.8, 0.4)


def desejo_do_timmy(rng, v):
    """Cosmo e Wanda: o "PUF!" grande em todos os rivais e a bagunça que vem depois."""
    x = _z(2.5)
    for k in range(3):
        poe(x, _puf(rng, 0.45), 0.3 + 0.05 * k)
    for k in range(5):
        poe(x, _piu(300 + 150 * k, 1200 - 100 * k, 0.15, 0.015), 0.45 + 0.07 * k)
    poe(x, _acorde((311, 370, 466), 0.6, 0.02), 0.6)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Steve

def espada_de_diamante_steve(rng, v):
    """Steve: a espada de diamante cortando e o "uh" do dano de jogo de blocos."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.2, 600, 5000, 0.8, 1.3, 0.5), 0.1)
    poe(x, _bloco(rng, 0.5), 0.3)
    n = n_de(0.15)
    poe(x, satura(seno(varre(260, 200, n), n), 2) * env(n, 0.01, 0.1) * 0.03, 0.32)
    return reverb(x, 0.5, 0.25)


def muro_de_blocos(rng, v):
    """Steve: os blocos caindo e se empilhando ("toc-toc-toc")."""
    x = _z(2.0)
    for j in range(12):
        poe(x, _bloco(rng, 0.25), 0.18 + 0.05 * j)
    poe(x, _acorde((392, 494, 587), 0.5, 0.015), 0.85)
    return reverb(x, 0.5, 0.25)


def golem_de_ferro_steve(rng, v):
    """Steve: os blocos de ferro encaixando (os "clang") e o Golem acordando."""
    x = _z(2.2)
    for k in range(4):
        poe(x, _sino(rng, 220 + 20 * k, 0.3, 0.03, METAL), 0.15 + 0.08 * k)
        poe(x, _bloco(rng, 0.25), 0.15 + 0.08 * k)
    n = n_de(0.5)
    poe(x, satura(seno(varre(60, 90, n), n), 3) * env(n, 0.1, 0.3) * 0.05, 0.5)
    poe(x, _baque(60, 30, 0.4, 0.5), 0.55)
    return reverb(x, 0.8, 0.4)


SONS: dict = {
    "raio-do-laboratorio": (raio_do_laboratorio, "Dexter: raio do laboratório"),
    "gerador-de-carga": (gerador_de_carga, "Dexter: gerador de Carga"),
    "dexter-preparo": (dexter_preparo, "Dexter: o controle do robô (Preparo)"),
    "robo-gigante-dexter": (robo_gigante_dexter, "Dexter: robô gigante"),
    "olhos-de-laser-aku": (olhos_de_laser_aku, "Aku: olhos de laser"),
    "forma-sem-forma": (forma_sem_forma, "Aku: forma sem forma"),
    "aku-preparo": (aku_preparo, "Aku: o redemoinho escuro (Preparo)"),
    "portal-do-tempo-aku": (portal_do_tempo_aku, "Aku: portal do tempo"),
    "arma-de-desidratar": (arma_de_desidratar, "Megamente: arma de desidratar"),
    "disfarce-megamente": (disfarce_megamente, "Megamente: disfarce"),
    "megamente-preparo": (megamente_preparo, "Megamente: as engrenagens (Preparo)"),
    "robo-mecha": (robo_mecha, "Megamente: robô mecha"),
    "tentaculos-vilgax": (tentaculos_vilgax, "Vilgax: tentáculos"),
    "armadura-de-batalha-vilgax": (armadura_de_batalha_vilgax, "Vilgax: armadura de batalha"),
    "vilgax-preparo": (vilgax_preparo, "Vilgax: o punho cerrando (Preparo)"),
    "soco-planetario": (soco_planetario, "Vilgax: soco planetário"),
    "desejo-de-forca": (desejo_de_forca, "Cosmo e Wanda: desejo de força"),
    "desejo-de-protecao": (desejo_de_protecao, "Cosmo e Wanda: desejo de proteção"),
    "cosmowanda-preparo": (cosmowanda_preparo, "Cosmo e Wanda: as varinhas (Preparo)"),
    "desejo-do-timmy": (desejo_do_timmy, "Cosmo e Wanda: desejo do Timmy"),
    "espada-de-diamante-steve": (espada_de_diamante_steve, "Steve: espada de diamante"),
    "muro-de-blocos": (muro_de_blocos, "Steve: muro de blocos"),
    "golem-de-ferro-steve": (golem_de_ferro_steve, "Steve: golem de ferro"),
}
