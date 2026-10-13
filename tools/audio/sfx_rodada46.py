"""Os sons da rodada 46 das habilidades próprias (veja tools/vfx/familias_v2/rodada46.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _choque(rng, seg, g=0.3, f0=1500, f1=7000):
    n = n_de(seg)
    t = _t(n)
    corte = (np.sin(2 * math.pi * 55 * t) > 0.2).astype(float)
    return satura(passa(rosa(rng, n), f0, f1, 2) * corte, 3) * env(n, 0.005, seg * 0.5) * g


def _rasgo(rng, seg=0.12, g=0.45):
    """O rasgo da garra (o chiado curto e áspero)."""
    n = n_de(seg)
    return satura(passa(rosa(rng, n), 1500, 9000, 2), 2) * env(n, 0.004, seg * 0.8) * g


def _gas(rng, seg, g=0.3):
    """O gás saindo do tubo (o chiado longo)."""
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 800, 6000, 2) * (0.8 + 0.2 * np.sin(2 * math.pi * 9 * t)) * sobe_e_some(n, 0.15, 1.2) * g


# ------------------------------------------------------------------ Mulher-Gato

def garras_felinas(rng, v):
    """Mulher-Gato: o miado-chiado e as garras rasgando duas vezes."""
    x = _z(1.8)
    n = n_de(0.25)
    poe(x, satura(seno(varre(700, 1100, n), n), 2) * env(n, 0.03, 0.2) * 0.02, 0.0)
    for k in range(2):
        for m in range(3):
            poe(x, _rasgo(rng, 0.1, 0.3), 0.08 + 0.17 * k + 0.015 * m)
        poe(x, _baque(170, 80, 0.15, 0.35), 0.15 + 0.17 * k)
    return reverb(x, 0.4, 0.2)


def chicote_da_gata(rng, v):
    """Mulher-Gato: o estalo do chicote, o enrolar e o buff quebrando."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 800, 6000, 0.85, 1.3, 0.4), 0.0)
    poe(x, estalo(rng, n_de(0.03), 2000, 10000, 0.004) * 1.4, 0.27)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 600, 3000, 2) * env(n, 0.03, 0.2) * 0.25, 0.32)
    for m in range(4):
        poe(x, _sino(rng, 2637 + 300 * m, 0.15, 0.012, CRISTAL), 0.52 + 0.025 * m)
    return reverb(x, 0.5, 0.25)


def mulher_gato_preparo(rng, v):
    """Mulher-Gato (Preparo): o ronronar no escuro e o chicote balançando (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 50, 300, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 24 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.35, 0.0)
    poe(x, _whoosh(rng, 0.5, 300, 2000, 0.5, 1.4, 0.15), 0.3)
    return reverb(x, 0.5, 0.25)


def grande_roubo(rng, v):
    """Mulher-Gato: as garras, a joia arrancada voando ("tlin") e o brilho voltando."""
    x = _z(2.1)
    for m in range(3):
        poe(x, _rasgo(rng, 0.1, 0.32), 0.05 + 0.015 * m)
    poe(x, _baque(150, 70, 0.25, 0.5), 0.15)
    poe(x, _sino(rng, 2093, 0.5, 0.03, CRISTAL), 0.32)
    poe(x, _whoosh(rng, 0.4, 1500, 7000, 0.5, 1.3, 0.3), 0.35)
    poe(x, _brilho(rng, 0.6, 1760, 0.025, CRISTAL), 0.75)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Espantalho

def nuvem_do_medo(rng, v):
    """Espantalho: o gás saindo em jatos e os sussurros distorcidos do medo."""
    x = _z(2.3)
    for k in range(3):
        poe(x, _gas(rng, 0.6, 0.3), 0.15 * k)
    for k in range(4):
        n = n_de(0.4)
        f = 180 + 40 * k
        poe(x, satura(seno(varre(f, f * 0.7, n), n), 3) * passa(rosa(rng, n), 300, 2000, 2) * env(n, 0.1, 0.25) * 0.4, 0.4 + 0.15 * k)
    return reverb(x, 0.9, 0.45)


def foice_do_espantalho(rng, v):
    """Espantalho: a foice girando ("vuuum") e o corte com a palha voando."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.35, 400, 4000, 0.85, 1.3, 0.5), 0.0)
    poe(x, _sino(rng, 1319, 0.4, 0.02, METAL), 0.33)
    poe(x, _baque(130, 55, 0.3, 0.6), 0.35)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * env(n, 0.01, 0.35) * 0.15, 0.36)
    return reverb(x, 0.5, 0.25)


def espantalho_preparo(rng, v):
    """Espantalho (Preparo): a respiração pela máscara e o gás rodando (em laço)."""
    x = _z(1.4)
    for k in range(2):
        n = n_de(0.45)
        poe(x, passa(rosa(rng, n), 300, 1500, 2) * sobe_e_some(n, 0.4, 1.2) * 0.3, 0.5 * k)
    poe(x, _gas(rng, 1.0, 0.08), 0.0)
    return reverb(x, 0.7, 0.35)


def pesadelo_vivo(rng, v):
    """Espantalho: o rosto do pesadelo surgindo (o grito grave distorcido) e os tentáculos."""
    x = _z(2.4)
    n = n_de(1.0)
    grito = satura(seno(varre(90, 60, n), n) + seno(varre(140, 95, n), n) * 0.6 + passa(rosa(rng, n), 100, 1500, 2) * 0.6, 5)
    poe(x, grito * sobe_e_some(n, 0.3, 1.2) * 0.06, 0.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.3, 200, 2000, 0.6, 1.3, 0.35), 0.35 + 0.05 * k)
        poe(x, _baque(110, 45, 0.3, 0.55), 0.55 + 0.05 * k)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Asa Noturna

def bastoes_de_choque(rng, v):
    """Asa Noturna: os dois bastões batendo e o choque azul."""
    x = _z(1.8)
    for k in range(2):
        poe(x, _whoosh(rng, 0.15, 1000, 7000, 0.7, 1.3, 0.35), 0.15 * k)
        poe(x, _baque(170, 80, 0.15, 0.4), 0.17 + 0.15 * k)
        poe(x, _choque(rng, 0.15, 0.2), 0.17 + 0.15 * k)
    poe(x, _choque(rng, 0.5, 0.3), 0.35)
    return reverb(x, 0.5, 0.25)


def salto_mortal(rng, v):
    """Asa Noturna: os três mortais (os giros) e o pouso leve."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.22, 600, 5000, 0.5, 1.4, 0.35), 0.05 + 0.18 * k)
    poe(x, _baque(200, 120, 0.08, 0.25), 0.62)
    poe(x, _brilho(rng, 0.4, 1568, 0.015, CRISTAL), 0.65)
    return reverb(x, 0.5, 0.25)


def combo_do_asa_noturna(rng, v):
    """Asa Noturna: a sequência de bastonadas, o chute e a descarga final."""
    x = _z(2.1)
    for k in range(5):
        poe(x, _baque(160 + 20 * (k % 2), 75, 0.12, 0.4), 0.1 + 0.09 * k)
        poe(x, _choque(rng, 0.08, 0.12), 0.1 + 0.09 * k)
    poe(x, _whoosh(rng, 0.15, 600, 5000, 0.7, 1.3, 0.4), 0.48)
    poe(x, _baque(75, 30, 0.6, 0.9, 2.8), 0.6)
    poe(x, _choque(rng, 0.6, 0.38, 800, 7000), 0.6)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Dipper

def _pagina(rng, g=0.3):
    n = n_de(0.08)
    return passa(rosa(rng, n), 1500, 7000, 2) * env(n, 0.01, 0.07) * g


def consultar_o_diario(rng, v):
    """Dipper: o diário abrindo, as páginas virando e o tom de descoberta."""
    x = _z(2.0)
    poe(x, _baque(200, 140, 0.08, 0.25), 0.0)
    for k in range(4):
        poe(x, _pagina(rng, 0.3), 0.08 + 0.06 * k)
    for k, f in enumerate((587, 740, 880)):
        poe(x, _sino(rng, f, 0.5, 0.02, SINO), 0.45 + 0.08 * k)
    return reverb(x, 0.6, 0.3)


def lanterna_de_dipper(rng, v):
    """Dipper: o clique da lanterna e o zumbido da luz forte no rosto."""
    x = _z(1.9)
    poe(x, estalo(rng, n_de(0.015), 1500, 6000, 0.003) * 0.8, 0.0)
    poe(x, estalo(rng, n_de(0.015), 1500, 6000, 0.003) * 0.6, 0.06)
    n = n_de(0.7)
    poe(x, (seno(120, n) * 0.5 + seno(2400, n) * 0.2) * sobe_e_some(n, 0.2, 1.2) * 0.02, 0.1)
    poe(x, _brilho(rng, 0.6, 2093, 0.025, CRISTAL), 0.28)
    return reverb(x, 0.5, 0.25)


def dipper_preparo(rng, v):
    """Dipper (Preparo): as páginas do diário folheando (em laço)."""
    x = _z(1.4)
    for k in range(6):
        poe(x, _pagina(rng, 0.2), 0.16 * k)
    n = n_de(1.0)
    poe(x, seno(440, n) * sobe_e_some(n, 0.5, 1.2) * 0.006, 0.0)
    return reverb(x, 0.5, 0.25)


def misterio_resolvido(rng, v):
    """Dipper: a roda de símbolos girando (o tom misterioso) e o feixe que desvenda."""
    x = _z(2.3)
    n = n_de(0.5)
    t = _t(n)
    poe(x, (seno(330, n) + seno(415, n) * 0.6) * (0.6 + 0.4 * np.sin(2 * math.pi * 8 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.025, 0.0)
    poe(x, _whoosh(rng, 0.25, 1500, 8000, 0.7, 1.3, 0.4), 0.4)
    poe(x, _baque(110, 45, 0.4, 0.7, 2.5), 0.58)
    poe(x, _acorde((523, 659, 784, 1047), 0.8, 0.02), 0.6)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Mabel

def glitter(rng, v):
    """Mabel: o "puf" do canhão e a chuva de brilhinhos tilintando."""
    x = _z(2.0)
    poe(x, _baque(220, 130, 0.12, 0.4), 0.05)
    poe(x, _sopro(rng, 0.25, 800, 5000, 0.25, 0.3), 0.05)
    q = np.random.default_rng(5)
    for k in range(12):
        poe(x, _sino(rng, q.uniform(2000, 4200), 0.2, 0.01, CRISTAL), 0.12 + 0.05 * k)
    for k in range(3):
        poe(x, _piu(900 + 200 * k, 1500 + 200 * k, 0.1, 0.02), 0.55 + 0.08 * k)
    return reverb(x, 0.6, 0.3)


def mabel_mania(rng, v):
    """Mabel: o "uhuul!" alegre, as estrelas cadentes e os corações subindo."""
    x = _z(2.2)
    for k, f in enumerate((523, 659, 784, 1047, 1319)):
        poe(x, _sino(rng, f, 0.4, 0.022, CRISTAL), 0.04 * k)
    for k in range(5):
        poe(x, _piu(1500, 900, 0.18, 0.02), 0.2 + 0.08 * k)
    poe(x, _acorde((659, 784, 988), 0.8, 0.02), 0.4)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Yennefer

def raio_arcano_yen(rng, v):
    """Yennefer: a obsidiana zumbindo e o raio violeta estalando no rival."""
    x = _z(1.9)
    n = n_de(0.35)
    poe(x, (seno(varre(220, 660, n), n) + seno(varre(330, 990, n), n) * 0.4) * env(n, 0.3, 0.05) * 0.02, 0.0)
    poe(x, _choque(rng, 0.4, 0.33, 900, 6000), 0.25)
    poe(x, _baque(140, 55, 0.3, 0.55), 0.35)
    poe(x, _sino(rng, 1175, 0.6, 0.02, METAL), 0.35)
    return reverb(x, 0.7, 0.35)


def barreira_de_yennefer(rng, v):
    """Yennefer: as cúpulas fechando ("vuum") com as runas soando."""
    x = _z(2.1)
    for k in range(3):
        n = n_de(0.35)
        poe(x, seno(varre(200 + 50 * k, 400 + 50 * k, n), n) * env(n, 0.25, 0.08) * 0.022, 0.05 + 0.05 * k)
    poe(x, _acorde((392, 494, 587, 784), 1.0, 0.02), 0.4)
    poe(x, _brilho(rng, 0.6, 1568, 0.015, CRISTAL), 0.45)
    return reverb(x, 0.8, 0.4)


def yennefer_preparo(rng, v):
    """Yennefer (Preparo): o caos rodando nas mãos (o zumbido violeta em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(196, n) + seno(294, n) * 0.6 + seno(392.5, n) * 0.3) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.02, 0.0)
    poe(x, _choque(rng, 0.1, 0.08), 0.4)
    return reverb(x, 0.7, 0.35)


def dissipar_de_yennefer(rng, v):
    """Yennefer: as runas acendendo embaixo dos rivais e os buffs arrancados para cima."""
    x = _z(2.3)
    for k in range(3):
        poe(x, _sino(rng, 587 + 150 * k, 0.6, 0.02, SINO), 0.05 + 0.05 * k)
    for k in range(3):
        poe(x, _whoosh(rng, 0.45, 300, 6000, 0.3, 1.3, 0.35), 0.35 + 0.05 * k)
        for m in range(3):
            poe(x, _sino(rng, 2349 + 300 * m, 0.15, 0.01, CRISTAL), 0.45 + 0.05 * k + 0.03 * m)
    poe(x, _baque(80, 30, 0.6, 0.8, 2.6), 0.4)
    return reverb(x, 0.8, 0.4)


SONS: dict = {
    "garras-felinas": (garras_felinas, "Mulher-Gato: as garras"),
    "chicote-da-gata": (chicote_da_gata, "Mulher-Gato: o chicote"),
    "mulher-gato-preparo": (mulher_gato_preparo, "Mulher-Gato: o ronronar no escuro (Preparo)"),
    "grande-roubo": (grande_roubo, "Mulher-Gato: o grande roubo"),
    "nuvem-do-medo": (nuvem_do_medo, "Espantalho: o gás do medo"),
    "foice-do-espantalho": (foice_do_espantalho, "Espantalho: a foice"),
    "espantalho-preparo": (espantalho_preparo, "Espantalho: a respiração e o gás (Preparo)"),
    "pesadelo-vivo": (pesadelo_vivo, "Espantalho: o pesadelo vivo"),
    "bastoes-de-choque": (bastoes_de_choque, "Asa Noturna: os bastões elétricos"),
    "salto-mortal": (salto_mortal, "Asa Noturna: o salto mortal"),
    "combo-do-asa-noturna": (combo_do_asa_noturna, "Asa Noturna: o combo"),
    "consultar-o-diario": (consultar_o_diario, "Dipper: consultar o diário"),
    "lanterna-de-dipper": (lanterna_de_dipper, "Dipper: a lanterna"),
    "dipper-preparo": (dipper_preparo, "Dipper: o diário folheando (Preparo)"),
    "misterio-resolvido": (misterio_resolvido, "Dipper: mistério resolvido"),
    "glitter": (glitter, "Mabel: o glitter"),
    "mabel-mania": (mabel_mania, "Mabel: Mabel mania"),
    "raio-arcano-yen": (raio_arcano_yen, "Yennefer: o raio arcano"),
    "barreira-de-yennefer": (barreira_de_yennefer, "Yennefer: a barreira mágica"),
    "yennefer-preparo": (yennefer_preparo, "Yennefer: o caos nas mãos (Preparo)"),
    "dissipar-de-yennefer": (dissipar_de_yennefer, "Yennefer: Dissipar"),
}
