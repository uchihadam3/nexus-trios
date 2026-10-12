"""Os sons da rodada 34 das habilidades próprias (veja tools/vfx/familias_v2/rodada34.py)."""
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


def _pavio(rng, seg, g=0.2):
    """O pavio queimando (o chiado de faíscas)."""
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 3000, 10000, 2) * (0.6 + 0.4 * np.abs(np.sin(2 * math.pi * 17 * t))) * env(n, 0.02, 0.05) * g


def _redemoinho(rng, seg, g=0.35, vel=12.0):
    """O redemoinho do Taz (o ronco que gira)."""
    n = n_de(seg)
    t = _t(n)
    return satura(passa(rosa(rng, n), 150, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * vel * t) ** 2), 2) * sobe_e_some(n, 0.3, 1.2) * g


# ------------------------------------------------------------------ Iroh

def cha_de_jasmim(rng, v):
    """Iroh: o chá caindo na xícara, o "tim" da porcelana e o suspiro calmo."""
    x = _z(2.1)
    n = n_de(0.5)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 800, 4000, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 30 * t)) * env(n, 0.03, 0.15) * 0.25, 0.15)
    poe(x, _sino(rng, 2093, 0.5, 0.03, CRISTAL), 0.0)
    poe(x, _sopro(rng, 0.8, 200, 1500, 0.12, 0.4), 0.5)
    poe(x, _acorde((294, 370, 440, 587), 1.2, 0.03, 0.2, 0.9), 0.45)
    return reverb(x, 0.7, 0.35)


def redirecionar_do_iroh(rng, v):
    """Iroh: o raio chegando, o zumbido dando a volta na barriga e saindo."""
    x = _z(2.0)
    poe(x, _trovao(rng, 0.3, 0.3), 0.0)
    n = n_de(0.35)
    t = _t(n)
    poe(x, seno(150 + 100 * np.sin(2 * math.pi * 3 * t), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 60 * t)) * env(n, 0.03, 0.2) * 0.05, 0.15)
    poe(x, _trovao(rng, 0.5, 0.5), 0.45)
    poe(x, _baque(110, 45, 0.3, 0.6), 0.5)
    return reverb(x, 0.6, 0.3)


def iroh_preparo(rng, v):
    """Iroh (Preparo): a respiração funda (o ar entrando) e as brasas estalando."""
    x = _z(1.4)
    poe(x, _sopro(rng, 0.7, 300, 2500, 0.2, 0.8), 0.0)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.004) * 0.35, 0.15 * k)
    return reverb(x, 0.5, 0.25)


def dragao_do_oeste(rng, v):
    """Iroh: o sopro de fogo do dragão (o rugido de chamas enorme)."""
    x = _z(2.3)
    n = n_de(0.8)
    poe(x, satura(passa(rosa(rng, n), 80, 3000, 2), 3) * sobe_e_some(n, 0.15, 1.3) * 0.5, 0.05)
    poe(x, satura(seno(varre(110, 70, n), n), 2) * sobe_e_some(n, 0.15, 1.3) * 0.05, 0.05)
    poe(x, _baque(80, 35, 0.4, 0.7), 0.3)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Patolino

def exijo_atencao(rng, v):
    """Patolino: o holofote ligando ("tchunc") e o "hu-hu! hu-hu!" pulando."""
    x = _z(2.0)
    poe(x, _baque(150, 140, 0.1, 0.4), 0.0)
    poe(x, estalo(rng, n_de(0.03), 800, 3000, 0.006), 0.0)
    for k in range(4):
        n = n_de(0.1)
        f = 700 if k % 2 == 0 else 950
        poe(x, satura(seno(varre(f, f * 1.2, n), n), 3) * env(n, 0.005, 0.08) * 0.04, 0.2 + 0.15 * k)
    poe(x, _piu(900, 1500, 0.12, 0.03), 0.85)
    return reverb(x, 0.5, 0.25)


def bico_afiado(rng, v):
    """Patolino: os bicos estalando (os "clac-clac") em todos."""
    x = _z(1.8)
    q = np.random.default_rng(3)
    for j in range(3):
        for m in range(3):
            poe(x, estalo(rng, n_de(0.03), 1200, 5000, 0.006) * 0.8, 0.08 * j + 0.15 + 0.2 * m * 0.5 + q.uniform(0, 0.02))
        poe(x, _baque(170, 90, 0.1, 0.3), 0.08 * j + 0.2)
    return reverb(x, 0.4, 0.2)


def patolino_preparo(rng, v):
    """Patolino (Preparo): o pavio da bomba chiando."""
    x = _z(1.4)
    poe(x, _pavio(rng, 1.0, 0.22), 0.0)
    return reverb(x, 0.3, 0.15)


def desastre_anunciado(rng, v):
    """Patolino: o pavio acabando, o "KABUM" e o bico voando com o assobio."""
    x = _z(2.3)
    poe(x, _pavio(rng, 0.3, 0.2), 0.0)
    poe(x, _baque(50, 20, 0.9, 1.0, 3.2), 0.3)
    poe(x, _explosao(rng, 1.0, 50), 0.3)
    poe(x, _piu(1500, 500, 0.4, 0.035), 0.45)
    for k in range(3):
        poe(x, _sino(rng, 1568 + 220 * k, 0.3, 0.02, CRISTAL), 0.85 + 0.07 * k)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Taz

def redemoinho_taz(rng, v):
    """Taz: o redemoinho rosnando e o choque no rival."""
    x = _z(1.9)
    poe(x, _redemoinho(rng, 0.7, 0.4, 14), 0.0)
    n = n_de(0.5)
    poe(x, satura(seno(varre(140, 110, n), n) + passa(rosa(rng, n), 100, 1200, 2) * 0.5, 4) * env(n, 0.05, 0.4) * 0.05, 0.05)
    poe(x, _baque(130, 55, 0.3, 0.6), 0.42)
    return reverb(x, 0.4, 0.2)


def mastigar(rng, v):
    """Taz: a mastigação ("nhac-nhac-nhac") e o grunhido satisfeito."""
    x = _z(1.9)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.04), 600, 3000, 0.01) * 0.8, 0.05 + 0.11 * k)
        poe(x, _baque(200, 120, 0.06, 0.25), 0.05 + 0.11 * k)
    n = n_de(0.4)
    poe(x, satura(seno(varre(130, 170, n), n), 3) * env(n, 0.05, 0.3) * 0.05, 0.75)
    poe(x, _brilho(rng, 0.4, 1047, 0.025, CRISTAL), 0.8)
    return reverb(x, 0.4, 0.2)


def taz_preparo(rng, v):
    """Taz (Preparo): o redemoinho começando a girar (o ronco que cresce)."""
    x = _z(1.4)
    poe(x, _redemoinho(rng, 1.0, 0.3, 10), 0.0)
    return reverb(x, 0.3, 0.15)


def fome_sem_fim(rng, v):
    """Taz: o tornado sugando tudo (o vento e as coisas voando) e a mordida enorme."""
    x = _z(2.3)
    poe(x, _redemoinho(rng, 0.7, 0.45, 16), 0.0)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 500, 6000, 2) * sobe_e_some(n, 0.8, 1.2) * 0.3, 0.0)
    q = np.random.default_rng(5)
    for k in range(6):
        poe(x, _baque(q.uniform(200, 350), 120, 0.05, 0.2), 0.1 + q.uniform(0, 0.45))
    poe(x, estalo(rng, n_de(0.06), 500, 3000, 0.012), 0.68)
    poe(x, _baque(90, 40, 0.5, 0.8, 2.6), 0.68)
    return reverb(x, 0.5, 0.25)


# ------------------------------------------------------------------ Coiote

def encomenda_acme(rng, v):
    """Coiote: o assobio da caixa caindo, o "POC" e o tique-taque da bomba."""
    x = _z(2.0)
    n = n_de(0.3)
    poe(x, seno(varre(1400, 600, n), n) * env(n, 0.02, 0.25) * 0.035, 0.0)
    poe(x, _baque(160, 80, 0.2, 0.55), 0.3)
    poe(x, estalo(rng, n_de(0.06), 400, 2500, 0.012) * 0.8, 0.3)
    for k in range(5):
        n = n_de(0.03)
        poe(x, seno(1800 if k % 2 == 0 else 1500, n) * env(n, 0.002, 0.025) * 0.03, 0.5 + 0.1 * k)
    return reverb(x, 0.4, 0.2)


def armadilha_montada(rng, v):
    """Coiote: a mola soltando ("boing!"), a luva batendo e as estrelinhas."""
    x = _z(1.9)
    n = n_de(0.4)
    t = _t(n)
    poe(x, seno(varre(200, 500, n), n) * (1 + 0.6 * np.sin(2 * math.pi * 25 * t)) * env(n, 0.005, 0.35) * 0.05, 0.2)
    poe(x, _baque(130, 55, 0.35, 0.7, 2.4), 0.38)
    for k in range(3):
        poe(x, _sino(rng, 1760 + 220 * k, 0.3, 0.02, CRISTAL), 0.5 + 0.07 * k)
    return reverb(x, 0.4, 0.2)


def coiote_preparo(rng, v):
    """Coiote (Preparo): o pavio do foguete chiando e o tique nervoso."""
    x = _z(1.4)
    poe(x, _pavio(rng, 1.0, 0.2), 0.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.02), 1000, 3000, 0.004) * 0.3, 0.25 * k)
    return reverb(x, 0.3, 0.15)


def plano_infalivel(rng, v):
    """Coiote: o foguete ACME rugindo, a batida em todos e o "puf" no fim."""
    x = _z(2.4)
    n = n_de(0.45)
    poe(x, satura(passa(rosa(rng, n), 100, 2500, 2), 3) * env(n, 0.03, 0.1) * 0.45, 0.0)
    poe(x, _whoosh(rng, 0.4, 300, 5000, 0.8, 1.4, 0.5), 0.0)
    poe(x, _baque(50, 20, 1.0, 1.0, 3.2), 0.4)
    poe(x, _explosao(rng, 1.0, 50), 0.4)
    poe(x, passa(rosa(rng, n_de(0.2)), 400, 3000, 2) * env(n_de(0.2), 0.005, 0.18) * 0.3, 0.95)
    poe(x, _piu(600, 300, 0.25, 0.03), 1.0)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Papa-Léguas

def bip_bip(rng, v):
    """Papa-Léguas: "bip-bip!" e o "zum" de passar num instante."""
    x = _z(1.7)
    for k in range(2):
        n = n_de(0.08)
        poe(x, (seno(1100, n) + _quadrada(1100, n) * 0.2) * env(n, 0.005, 0.06) * 0.05, 0.12 * k)
    poe(x, _whoosh(rng, 0.15, 1500, 10000, 0.5, 1.4, 0.5), 0.05)
    poe(x, _baque(150, 70, 0.2, 0.45), 0.17)
    return reverb(x, 0.4, 0.2)


def poeira_na_pista(rng, v):
    """Papa-Léguas: o "zum" passando e a nuvem de poeira se espalhando."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.25, 1000, 9000, 0.5, 1.4, 0.45), 0.0)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 200, 2500, 2) * sobe_e_some(n, 0.2, 1.3) * 0.3, 0.1)
    for k in range(2):
        n = n_de(0.08)
        poe(x, seno(1100, n) * env(n, 0.005, 0.06) * 0.04, 0.6 + 0.12 * k)
    return reverb(x, 0.5, 0.25)


def velocidade_impossivel(rng, v):
    """Papa-Léguas: os pés girando (o "brrrrr") e as voltas em alta velocidade."""
    x = _z(2.0)
    n = n_de(0.8)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.3, 0.0)
    for k in range(4):
        poe(x, _whoosh(rng, 0.12, 1500, 9000, 0.5, 1.4, 0.3), 0.05 + 0.15 * k)
    for k in range(2):
        n = n_de(0.08)
        poe(x, seno(1100, n) * env(n, 0.005, 0.06) * 0.04, 0.75 + 0.12 * k)
    return reverb(x, 0.4, 0.2)


# ------------------------------------------------------------------ Marvin

def modulador_illudium(rng, v):
    """Marvin: o Modulador Illudium Q-36 (os bipes marcianos e o zumbido de mira)."""
    x = _z(2.0)
    for k, f in enumerate((1568, 1175, 1760, 1319)):
        n = n_de(0.06)
        poe(x, seno(f, n) * env(n, 0.003, 0.05) * 0.03, 0.08 * k)
    n = n_de(0.5)
    t = _t(n)
    poe(x, seno(varre(300, 900, n), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 12 * t)) * env(n, 0.05, 0.1) * 0.03, 0.3)
    poe(x, _sino(rng, 2637, 0.4, 0.025, CRISTAL), 0.55)
    return reverb(x, 0.5, 0.25)


def mira_marciana(rng, v):
    """Marvin: a pistola de raios marciana (o "piu-uuu" ondulado) e o impacto."""
    x = _z(1.9)
    n = n_de(0.5)
    t = _t(n)
    poe(x, seno(varre(1600, 400, n) * (1 + 0.1 * np.sin(2 * math.pi * 25 * t)), n) * env(n, 0.01, 0.4) * 0.05, 0.15)
    poe(x, _baque(130, 55, 0.3, 0.6), 0.3)
    poe(x, _brilho(rng, 0.4, 1319, 0.025, CRISTAL), 0.32)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "cha-de-jasmim": (cha_de_jasmim, "Iroh: o chá de jasmim"),
    "redirecionar-do-iroh": (redirecionar_do_iroh, "Iroh: redirecionar"),
    "iroh-preparo": (iroh_preparo, "Iroh: a respiração funda (Preparo)"),
    "dragao-do-oeste": (dragao_do_oeste, "Iroh: o Dragão do Oeste"),
    "exijo-atencao": (exijo_atencao, "Patolino: exijo atenção"),
    "bico-afiado": (bico_afiado, "Patolino: o bico afiado"),
    "patolino-preparo": (patolino_preparo, "Patolino: o pavio (Preparo)"),
    "desastre-anunciado": (desastre_anunciado, "Patolino: o desastre anunciado"),
    "redemoinho-taz": (redemoinho_taz, "Taz: o redemoinho"),
    "mastigar": (mastigar, "Taz: mastigar"),
    "taz-preparo": (taz_preparo, "Taz: o redemoinho começando (Preparo)"),
    "fome-sem-fim": (fome_sem_fim, "Taz: a fome sem fim"),
    "encomenda-acme": (encomenda_acme, "Coiote: a encomenda ACME"),
    "armadilha-montada": (armadilha_montada, "Coiote: a armadilha montada"),
    "coiote-preparo": (coiote_preparo, "Coiote: o pavio do foguete (Preparo)"),
    "plano-infalivel": (plano_infalivel, "Coiote: o plano infalível"),
    "bip-bip": (bip_bip, "Papa-Léguas: bip-bip"),
    "poeira-na-pista": (poeira_na_pista, "Papa-Léguas: a poeira na pista"),
    "velocidade-impossivel": (velocidade_impossivel, "Papa-Léguas: a velocidade impossível"),
    "modulador-illudium": (modulador_illudium, "Marvin: o Modulador Illudium"),
    "mira-marciana": (mira_marciana, "Marvin: a mira marciana"),
}
