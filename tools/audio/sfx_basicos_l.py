"""Sons dos ataques básicos, lote l (veja tools/vfx/familias_v2/basicos_l.py).

A mordida e o "slurp" da Marceline, o "clac-clac" do bastão retrátil, o "boing" do pulo do Luigi, o tapa
estalado da Peach, os três cortes do Zoro, o trovãozinho da nuvem da Nami, o chute do Sanji, a chifrada e o
tropel do Chopper, os dois tiros juntos da Blue Rose, o giro da capoeira, o tiro tremido do Morty, a hélice
das caudas do Tails, o soco de luva com as pedras, o "tum" do livro e a ombrada com a rede caindo.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_k import _acerto, _mola, _splash
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _tiro(rng, g=0.7):
    n = n_de(0.35)
    return satura(baque(n, 150, 60, 0.07, 1.0) * 0.8 + passa(rosa(rng, n), 400, 9000, 2) * env(n, 0.0005, 0.05) * 1.1, 1.6) * g


def _estrelinhas(rng, t0, x, g=0.05):
    for k, f in enumerate((2093, 2637, 3136)):
        poe(x, _brilho(rng, 0.3, f, g, SINO), t0 + 0.05 * k)


# =================================================================== Marceline
def mordida_vampira(rng, v):
    """A mordiscada: o "nhac" dos dentes fechando, e o vermelho sendo chupado (o "sssslurp" que sobe e some)."""
    x = _z(1.1)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.006) * 0.8, 0.28)
    poe(x, _acerto(rng, 0.5, 150), 0.28)
    n = n_de(0.55)
    t = _t(n)
    poe(x, (passa(rosa(rng, n), 800, 4000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 14 * t)) + seno(varre(300, 900, n, 1.0), n) * 0.15) * sobe_e_some(n, 0.6, 1.3) * 0.3, 0.38)
    return reverb(x, 0.45, 0.22)


# =================================================================== Robin
def bastao_do_robin(rng, v):
    """O bastão do Robin: o giro no ar (o "vup-vup"), o "clac-clac-clac" dos gomos travando ao esticar e a
    estocada seca."""
    x = _z(1.0)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 600, 3500, 2) * np.abs(np.sin(2 * math.pi * 8 * _t(n))) * sobe_e_some(n, 0.6, 1.2) * 0.4, 0.0)
    for k in range(3):
        poe(x, modal(n_de(0.08), 2400 + 300 * k, rng=rng, **METAL) * env(n_de(0.08), 0.0005, 0.02) * 0.25, 0.25 + 0.035 * k)
    poe(x, _acerto(rng, 0.8, 130), 0.36)
    return reverb(x, 0.3, 0.15)


# =================================================================== Luigi
def pulo_do_luigi(rng, v):
    """O pulo do Luigi: o "boing" alto do pulo (o tom que sobe e treme), as pernas batendo no ar (os "flap" rápidos)
    e a pisada em cima do rival com o plim das estrelinhas."""
    x = _z(1.2)
    n = n_de(0.35)
    poe(x, seno(varre(300, 1100, n, 0.7) * (1 + 0.02 * np.sin(2 * math.pi * 30 * _t(n))), n) * sobe_e_some(n, 0.3, 1.3) * 0.12, 0.0)
    for k in range(5):
        m = n_de(0.04)
        poe(x, passa(rosa(rng, m), 1000, 4000, 2) * env(m, 0.002, 0.025) * 0.15, 0.2 + 0.04 * k)
    poe(x, _acerto(rng, 0.9, 120), 0.45)
    _estrelinhas(rng, 0.5, x)
    return reverb(x, 0.35, 0.18)


# =================================================================== Peach
def tapa_real(rng, v):
    """O tapa real: a mão vindo (o "fwip" rápido), o tapa estalado bem agudo e os brilhinhos de princesa."""
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.2, 1200, 4000, 0.8, 1.2, 0.35), 0.05)
    poe(x, B._tapa(rng, n_de(0.1), 1500, 8000, 0.02) * 1.3, 0.25)
    poe(x, B._carne(rng, n_de(0.1), 0.03, 2.0) * 0.5, 0.25)
    _estrelinhas(rng, 0.32, x, 0.06)
    return reverb(x, 0.4, 0.2)


# =================================================================== Zoro
def corte_santoryu(rng, v):
    """O corte de três espadas: as três lâminas saindo juntas (o "shing" triplo, um colado no outro) e o corte
    que passa."""
    x = _z(1.0)
    for k in range(3):
        poe(x, B._lamina_curta(rng, n_de(0.35), 2600 + 400 * k) * env(n_de(0.35), 0.001, 0.15) * 0.25, 0.08 + 0.02 * k)
        poe(x, _whoosh(rng, 0.15, 1500, 6000, 0.7, 1.2, 0.25), 0.07 + 0.02 * k)
    poe(x, _acerto(rng, 0.6, 140, 2000, 7000), 0.15)
    return reverb(x, 0.4, 0.2)


# =================================================================== Nami
def clima_tact(rng, v):
    """O Clima-Tact: o "pop" da bolinha de nuvem saindo, o chiado dela inflando e o raiozinho estalando em cima
    do rival."""
    x = _z(1.1)
    m = n_de(0.06)
    poe(x, seno(varre(500, 900, m, 1.0), m) * env(m, 0.002, 0.04) * 0.12, 0.0)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 300, 1500, 2) * sobe_e_some(n, 0.7, 1.3) * 0.2, 0.05)
    poe(x, estalo(rng, n_de(0.06), 1500, 9000, 0.012) * 1.0, 0.4)
    poe(x, graos(rng, n_de(0.2), 15, 0.0, 0.18, 2500, 9000, 0.003) * 0.4, 0.4)
    m = n_de(0.4)
    poe(x, passa(rosa(rng, m), 40, 500, 2) * env(m, 0.005, 0.25) * 0.4, 0.41)
    return reverb(x, 0.5, 0.22)


# =================================================================== Sanji
def chute_de_sanji(rng, v):
    """O chute do Sanji: a perna varrendo o ar (o "fwooom" largo), a pancada forte do sapato e o sopro da fumaça."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.3, 300, 2000, 0.85, 1.3, 0.6), 0.0)
    poe(x, _acerto(rng, 1.1, 105), 0.26)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 800, 3500, 2) * sobe_e_some(m, 0.4, 1.3) * 0.08, 0.45)
    return reverb(x, 0.35, 0.18)


# =================================================================== Chopper
def chifrada_do_chopper(rng, v):
    """A chifrada: os cascos correndo (o tropel leve), a cabeçada com os chifres (o "toc" de osso e o baque)."""
    x = _z(1.0)
    for k in range(6):
        poe(x, passa(baque(n_de(0.05), 220, 140, 0.02, 0.3), None, 2500, 2) * 0.2, 0.03 + 0.045 * k)
    poe(x, modal(n_de(0.12), 900, rng=rng, razoes=[1.0, 2.6, 4.4], quedas=[0.05, 0.03, 0.02], ganhos=[1, 0.4, 0.2]) * 0.4, 0.29)
    poe(x, _acerto(rng, 0.9, 115), 0.29)
    return reverb(x, 0.3, 0.15)


# =================================================================== Nero
def blue_rose(rng, v):
    """A Blue Rose: os dois tiros juntos (dois estampidos colados, quase um só), o tambor girando (o clique) e os
    dois furos batendo."""
    x = _z(1.0)
    poe(x, _tiro(rng, 0.8), 0.0)
    poe(x, _tiro(rng, 0.6), 0.025)
    poe(x, modal(n_de(0.1), 2200, rng=rng, **METAL) * env(n_de(0.1), 0.0005, 0.03) * 0.25, 0.3)
    poe(x, _acerto(rng, 0.45, 150, 2000, 7000), 0.16)
    poe(x, _acerto(rng, 0.35, 160, 2000, 7000), 0.19)
    return reverb(x, 0.45, 0.2)


# =================================================================== L
def chute_capoeira(rng, v):
    """O chute de capoeira: o giro de ponta-cabeça (o "fwoom" que dá a volta inteira) e o pé batendo de cima."""
    x = _z(1.0)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 400, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * _t(n))) * sobe_e_some(n, 0.7, 1.3) * 0.45, 0.0)
    poe(x, _acerto(rng, 0.9, 120), 0.33)
    return reverb(x, 0.3, 0.15)


# =================================================================== Morty
def tiro_nervoso(rng, v):
    """O tiro nervoso: o "aw jeez" (o gemidinho que treme), o primeiro raio que erra (o "piu" que passa longe) e
    o segundo de raspão."""
    x = _z(1.1)
    m = n_de(0.25)
    poe(x, seno(varre(420, 330, m, 1.0) * (1 + 0.05 * np.sin(2 * math.pi * 12 * _t(m))), m) * sobe_e_some(m, 0.3, 1.3) * 0.05, 0.0)
    for k, t0 in enumerate((0.08, 0.3)):
        n = n_de(0.18)
        poe(x, seno(varre(2400, 700, n, 1.0), n) * env(n, 0.002, 0.12) * (0.08 if k == 0 else 0.1), t0)
    poe(x, _acerto(rng, 0.45, 160), 0.44)
    return reverb(x, 0.4, 0.2)


# =================================================================== Tails
def caudas_giratorias(rng, v):
    """As caudas do Tails: a hélice das duas caudas (o "vuvuvuvu" que acelera) e os dois golpes de cauda."""
    x = _z(1.1)
    n = n_de(0.7)
    t = _t(n)
    f = 10 + 20 * t
    poe(x, passa(rosa(rng, n), 500, 3000, 2) * np.abs(np.sin(2 * math.pi * np.cumsum(f) / SR)) * sobe_e_some(n, 0.6, 1.2) * 0.4, 0.0)
    poe(x, _acerto(rng, 0.55, 140), 0.3)
    poe(x, _acerto(rng, 0.55, 150), 0.45)
    return reverb(x, 0.3, 0.15)


# =================================================================== Knuckles
def punho_espinhoso(rng, v):
    """O soco de luva: o punho cortando o ar, a pancada pesada e as pedrinhas caindo."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.22, 300, 2000, 0.85, 1.3, 0.5), 0.02)
    poe(x, _acerto(rng, 1.2, 95), 0.25)
    poe(x, graos(rng, n_de(0.6), 14, 0.05, 0.55, 600, 3000, 0.01) * 0.4, 0.28)
    return reverb(x, 0.35, 0.18)


# =================================================================== Velma
def livro_na_cabeca(rng, v):
    """O livro na cabeça: o livro girando no ar (as páginas batendo, "flflfl"), o "TUM" seco na cabeça e as
    estrelinhas."""
    x = _z(1.1)
    n = n_de(0.28)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * np.abs(np.sin(2 * math.pi * 14 * _t(n))) * sobe_e_some(n, 0.6, 1.2) * 0.25, 0.0)
    poe(x, B._baque_seco(rng, n_de(0.2), 140, 0.05) * 0.9, 0.28)
    poe(x, B._tapa(rng, n_de(0.06), 800, 3500, 0.01) * 0.8, 0.28)
    _estrelinhas(rng, 0.35, x)
    return reverb(x, 0.35, 0.18)


# =================================================================== Fred
def ombrada(rng, v):
    """A ombrada do Fred: os passos correndo, a trombada (o baque cheio) e a rede caindo (o chiado de corda e o
    "fump" no chão)."""
    x = _z(1.1)
    for k in range(4):
        poe(x, passa(baque(n_de(0.06), 160, 100, 0.03, 0.3), None, 2000, 2) * 0.25, 0.03 + 0.06 * k)
    poe(x, _acerto(rng, 1.1, 100), 0.27)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.7, 1.2) * 0.2, 0.42)
    poe(x, passa(baque(n_de(0.15), 120, 80, 0.04, 0.2), None, 1500, 2) * 0.35, 0.62)
    return reverb(x, 0.35, 0.18)


SONS: dict = {
    "mordida-vampira": (mordida_vampira, "básico da Marceline: a mordida e o vermelho chupado"),
    "bastao-do-robin": (bastao_do_robin, "básico do Robin: o giro, os gomos e a estocada"),
    "pulo-do-luigi": (pulo_do_luigi, "básico do Luigi: o pulo e a pisada"),
    "tapa-real": (tapa_real, "básico da Peach: o tapa estalado e os brilhos"),
    "corte-santoryu": (corte_santoryu, "básico do Zoro: os três cortes"),
    "clima-tact": (clima_tact, "básico da Nami: a nuvenzinha e o raio"),
    "chute-de-sanji": (chute_de_sanji, "básico do Sanji: o chute e a fumaça"),
    "chifrada-do-chopper": (chifrada_do_chopper, "básico do Chopper: o tropel e a chifrada"),
    "blue-rose": (blue_rose, "básico do Nero: os dois tiros juntos"),
    "chute-capoeira": (chute_capoeira, "básico do L: o giro e o chute"),
    "tiro-nervoso": (tiro_nervoso, "básico do Morty: o tiro que erra e o de raspão"),
    "caudas-giratorias": (caudas_giratorias, "básico do Tails: a hélice e os golpes"),
    "punho-espinhoso": (punho_espinhoso, "básico do Knuckles: o soco e as pedras"),
    "livro-na-cabeca": (livro_na_cabeca, "básico da Velma: o livro e o tum"),
    "ombrada": (ombrada, "básico do Fred: a trombada e a rede"),
}
