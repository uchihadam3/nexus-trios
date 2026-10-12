"""Os sons da rodada 3 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_d.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada08 import _corrente
from sfx_rodada15 import _laser
from sfx_rodada16 import _explosao
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _acorde(fs, seg, g=0.04, ataque=0.03, queda=0.5):
    n = n_de(seg)
    return sum(seno(f, n) * (1 - 0.15 * k) for k, f in enumerate(fs)) * env(n, ataque, queda) * g


def _sino(rng, f, seg=0.6, g=0.06, tipo=SINO):
    n = n_de(seg)
    return modal(n, f, rng=rng, **tipo) * env(n, 0.002, seg * 0.5) * g


def _baque(f0, f1, seg=0.4, g=0.6, drive=2.0):
    return satura(baque(n_de(seg), f0, f1, seg * 0.3, 1.0), drive) * g


def _sopro(rng, seg, lo, hi, g=0.3, pico=0.5):
    n = n_de(seg)
    return passa(rosa(rng, n), lo, hi, 2) * sobe_e_some(n, pico, 1.3) * g


def mana(rng, v):
    """Frieren: o círculo abrindo (o tom místico) e as flores desabrochando (os sininhos em cascata)."""
    x = _z(2.0)
    poe(x, _acorde((294, 440, 587, 740), 1.4, 0.035, 0.2, 0.8), 0.0)
    for k, f in enumerate((1175, 1319, 1480, 1568, 1760, 1976, 2349)):
        poe(x, _sino(rng, f, 0.5, 0.035, CRISTAL), 0.25 + 0.08 * k)
    poe(x, _sopro(rng, 1.2, 2000, 8000, 0.12), 0.2)
    return reverb(x, 0.8, 0.4)


def waku(rng, v):
    """Anya: o "bip" da leitura de mente (as ondas que sobem e descem) e as estrelinhas do waku waku."""
    x = _z(1.7)
    for k in range(3):
        n = n_de(0.25)
        poe(x, seno(varre(700, 1400, n, 1.0) * (1 + 0.05 * np.sin(2 * math.pi * 20 * _t(n))), n) * env(n, 0.01, 0.15) * 0.05, 0.05 + 0.18 * k)
    for k, f in enumerate((1568, 2093, 1760, 2349, 2637)):
        poe(x, _sino(rng, f, 0.3, 0.03, CRISTAL), 0.5 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


def strix(rng, v):
    """Loid: a mira ajustando (os cliques da lente), a trava e as cargas enchendo (os tons que sobem)."""
    x = _z(1.8)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.03), 2500, 7000, 0.004) * 0.5, 0.05 + 0.08 * k)
    poe(x, _baque(500, 300, 0.12, 0.3, 1.5), 0.5)
    poe(x, estalo(rng, n_de(0.04), 1500, 5000, 0.006) * 0.8, 0.5)
    for k in range(3):
        n = n_de(0.2)
        poe(x, seno(varre(600 + 200 * k, 900 + 200 * k, n), n) * env(n, 0.01, 0.15) * 0.05, 0.85 + 0.12 * k)
    return reverb(x, 0.4, 0.2)


def espinho(rng, v):
    """Yor: o espinho cortando o ar, cravando (o metal fino e o baque) e as pétalas."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.25, 1500, 9000, 0.8, 1.6, 0.7), 0.1)
    poe(x, _sino(rng, 3200, 0.5, 0.06, METAL), 0.35)
    poe(x, _baque(180, 80, 0.3, 0.5), 0.35)
    poe(x, _sopro(rng, 0.8, 1500, 6000, 0.12, 0.2), 0.4)
    return reverb(x, 0.5, 0.25)


def nivel(rng, v):
    """Jinwoo: a janela do sistema (o "plim" de jogo), o arpejo do level up e as sombras subindo."""
    x = _z(1.9)
    poe(x, _sino(rng, 1047, 0.4, 0.05, VIDRO), 0.0)
    for k, f in enumerate((523, 659, 784, 1047, 1319)):
        n = n_de(0.18 if k < 4 else 0.6)
        poe(x, (seno(f, n) + seno(f * 2, n) * 0.3) * env(n, 0.005, 0.12 if k < 4 else 0.4) * 0.05, 0.2 + 0.08 * k)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 60, 500, 2) * sobe_e_some(n, 0.4, 1.2) * 0.35, 0.3)
    return reverb(x, 0.6, 0.3)


def kakuja(rng, v):
    """Kaneki: os tentáculos rasgando para fora (o som molhado e esticado) e o estalo do dedo."""
    x = _z(1.9)
    for k in range(4):
        n = n_de(0.35)
        poe(x, satura(passa(rosa(rng, n), 150, 1800, 2) * sobe_e_some(n, 0.3, 1.5), 2.0) * 0.4 + seno(varre(200, 80, n), n) * env(n, 0.01, 0.2) * 0.08, 0.05 + 0.08 * k)
    poe(x, estalo(rng, n_de(0.04), 1500, 5000, 0.006) * 0.9, 0.7)
    n = n_de(0.8)
    poe(x, (seno(55, n) * 0.6 + seno(58, n) * 0.6) * sobe_e_some(n, 0.3, 1.2) * 0.15, 0.7)
    return reverb(x, 0.5, 0.25)


def carta_yugi(rng, v):
    """Yugi: a carta saindo do deck (o papel), virando e o Enigma acendendo (o coro dourado)."""
    x = _z(1.9)
    n = n_de(0.12)
    poe(x, passa(rosa(rng, n), 2000, 8000, 2) * env(n, 0.002, 0.08) * 0.5, 0.1)
    poe(x, _whoosh(rng, 0.3, 800, 4000, 0.6, 1.4, 0.3), 0.2)
    poe(x, _acorde((220, 277, 330, 440), 1.2, 0.05, 0.1, 0.6), 0.5)
    poe(x, _brilho(rng, 0.8, 1760, 0.05, SINO), 0.55)
    return reverb(x, 0.7, 0.35)


def olhos_azuis(rng, v):
    """Kaiba: a carta batendo na mesa, o rugido do dragão e o Raio da Destruição."""
    x = _z(2.0)
    poe(x, _baque(300, 150, 0.15, 0.4, 1.5), 0.0)
    n = n_de(0.6)
    t = _t(n)
    poe(x, satura(seno(varre(220, 140, n), n) * (1 + 0.3 * np.sin(2 * math.pi * 30 * t)) + passa(rosa(rng, n), 300, 2500, 2), 2.5) * env(n, 0.03, 0.35) * 0.18, 0.2)
    m = n_de(1.0)
    poe(x, (passa(rosa(rng, m), 400, 7000, 2) * 0.5 + satura(seno(150, m), 2) * 0.1) * env(m, 0.01, 0.5, segura=0.3), 0.7)
    poe(x, _trovao(rng, 0.8, 0.4), 0.8)
    return reverb(x, 0.6, 0.3)


def cinetico(rng, v):
    """Pantera Negra: a energia entrando no traje (o zumbido que sobe), a onda cinética e as garras."""
    x = _z(1.9)
    n = n_de(0.7)
    poe(x, (seno(varre(80, 320, n, 1.4), n) * 0.12 + passa(rosa(rng, n), 300, 3000, 2) * 0.15) * sobe_e_some(n, 0.95, 1.0), 0.0)
    poe(x, _explosao(rng, 0.6, 70), 0.7)
    for k in range(3):
        poe(x, _whoosh(rng, 0.12, 2000, 9000, 0.5, 1.4, 0.45), 0.95 + 0.06 * k)
    return reverb(x, 0.5, 0.25)


def hex_(rng, v):
    """Feiticeira Escarlate: a magia do caos (o sussurro que gira) e o hex estalando."""
    x = _z(1.9)
    n = n_de(1.2)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 600, 4000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * t + np.sin(2 * math.pi * 0.7 * t) * 3)) * sobe_e_some(n, 0.5, 1.2) * 0.35, 0.0)
    poe(x, (seno(330, n) * 0.6 + seno(349, n) * 0.6) * sobe_e_some(n, 0.5, 1.2) * 0.05, 0.0)
    poe(x, estalo(rng, n_de(0.05), 1000, 6000, 0.012) * 0.8, 0.95)
    poe(x, _sino(rng, 880, 0.8, 0.05, VIDRO), 0.95)
    return reverb(x, 0.6, 0.3)


def joia_da_mente(rng, v):
    """Visão: a joia ressoando (o cristal limpo) e o leque de luz que limpa (o acorde claro subindo)."""
    x = _z(1.9)
    poe(x, _sino(rng, 1320, 1.0, 0.08, CRISTAL), 0.0)
    n = n_de(0.8)
    poe(x, seno(varre(440, 880, n, 1.0), n) * sobe_e_some(n, 0.6, 1.2) * 0.04, 0.3)
    poe(x, _acorde((659, 831, 988, 1319), 0.9, 0.035, 0.05, 0.5), 0.6)
    return reverb(x, 0.7, 0.35)


def energia_absorvida(rng, v):
    """Capitã Marvel: a energia sendo sugada, a estrela acendendo (o tom forte) e as chamas de fótons."""
    x = _z(1.9)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 800, 7000, 2) * sobe_e_some(n, 0.95, 1.0) * 0.35, 0.0)
    poe(x, _baque(140, 70, 0.3, 0.5), 0.6)
    poe(x, _acorde((330, 494, 659), 0.8, 0.05, 0.01, 0.5), 0.6)
    m = n_de(1.0)
    poe(x, satura(passa(rosa(rng, m), 150, 3500, 2), 1.6) * sobe_e_some(m, 0.2, 1.4) * 0.4, 0.65)
    return reverb(x, 0.5, 0.25)


def interrogatorio(rng, v):
    """Justiceiro: o "Fala!" grave (o soco na mesa), a arma engatilhando e os tiros."""
    x = _z(1.9)
    poe(x, _baque(110, 55, 0.4, 0.8, 2.2), 0.05)
    poe(x, estalo(rng, n_de(0.04), 1200, 4000, 0.006) * 0.6, 0.3)
    poe(x, estalo(rng, n_de(0.04), 1800, 6000, 0.006) * 0.6, 0.38)
    for k in range(5):
        n = n_de(0.25)
        poe(x, satura(passa(rosa(rng, n), 300, 8000, 2) * env(n, 0.0005, 0.05), 2.5) * 0.6 + _baque(150, 70, 0.25, 0.25), 0.55 + 0.08 * k)
    return reverb(x, 0.5, 0.25)


def pecados(rng, v):
    """Motoqueiro Fantasma: a corrente girando (os elos) e o fogo do inferno rugindo."""
    x = _z(2.0)
    poe(x, _corrente(rng, 0.9, 14, 0.4), 0.0)
    n = n_de(1.3)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 120, 3000, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 6 * t)), 1.8) * sobe_e_some(n, 0.3, 1.2) * 0.5, 0.1)
    poe(x, (seno(73, n) + seno(77, n)) * sobe_e_some(n, 0.4, 1.2) * 0.07, 0.1)
    return reverb(x, 0.6, 0.3)


def cacador(rng, v):
    """Blade: a glaive girando (o assobio que roda), os dois cortes e a névoa espirrando."""
    x = _z(1.8)
    n = n_de(0.55)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 14 * t) ** 2) * sobe_e_some(n, 0.8, 1.0) * 0.5, 0.0)
    for k in range(2):
        poe(x, _whoosh(rng, 0.15, 2000, 10000, 0.4, 1.4, 0.7), 0.5 + 0.08 * k)
        poe(x, _sino(rng, 2800 + 300 * k, 0.35, 0.05, METAL), 0.55 + 0.08 * k)
    poe(x, _sopro(rng, 0.5, 300, 3000, 0.25, 0.2), 0.65)
    return reverb(x, 0.4, 0.2)


def crescentes(rng, v):
    """Cavaleiro da Lua: os crescentes zunindo em volta e cravando um a um (os tilintares de prata)."""
    x = _z(1.9)
    n = n_de(0.9)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 9 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.3, 0.0)
    for k in range(5):
        poe(x, _sino(rng, 2400 + 150 * k, 0.4, 0.045, VIDRO), 0.95 + 0.05 * k)
        poe(x, estalo(rng, n_de(0.03), 2000, 7000, 0.005) * 0.4, 0.95 + 0.05 * k)
    poe(x, _acorde((392, 494, 587), 0.8, 0.03, 0.02, 0.4), 1.2)
    return reverb(x, 0.6, 0.3)


def raio_rubi(rng, v):
    """Ciclope: o raio escapando (o zumbido rasgado e alto) e a destruição em volta."""
    x = _z(1.9)
    n = n_de(1.3)
    t = _t(n)
    poe(x, satura(seno(140 + 30 * np.sin(2 * math.pi * 3 * t), n) + passa(rosa(rng, n), 600, 6000, 2) * 0.8, 2.4) * env(n, 0.01, 0.6, segura=0.5) * 0.25, 0.1)
    for k in range(4):
        poe(x, _explosao(rng, 0.25, 70 + 10 * k), 0.3 + 0.2 * k)
    return reverb(x, 0.5, 0.25)


def elo_mental(rng, v):
    """Jean Grey: a Fênix (o grito de ave de fogo e o fogo subindo) e o elo mental (o tom que vibra)."""
    x = _z(2.0)
    n = n_de(0.7)
    t = _t(n)
    poe(x, seno(varre(1400, 2200, n, 0.6) * (1 + 0.04 * np.sin(2 * math.pi * 12 * t)), n) * env(n, 0.03, 0.4) * 0.06, 0.05)
    m = n_de(1.0)
    poe(x, satura(passa(rosa(rng, m), 200, 3000, 2), 1.6) * sobe_e_some(m, 0.3, 1.3) * 0.4, 0.0)
    k = n_de(0.9)
    poe(x, (seno(523, k) * 0.6 + seno(527, k) * 0.6) * sobe_e_some(k, 0.5, 1.2) * 0.06, 0.8)
    return reverb(x, 0.7, 0.35)


def toque(rng, v):
    """Vampira: o poder sendo puxado (o som que corre e afina) e a absorção (o tom que incha)."""
    x = _z(1.8)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 500, 4000, 2) * sobe_e_some(n, 0.8, 1.0) * 0.35, 0.0)
    poe(x, seno(varre(900, 300, n, 1.2), n) * sobe_e_some(n, 0.8, 1.0) * 0.05, 0.0)
    m = n_de(0.8)
    poe(x, (seno(196, m) + seno(294, m) * 0.6) * env(m, 0.05, 0.5) * 0.08, 0.75)
    poe(x, _brilho(rng, 0.6, 1320, 0.03, CRISTAL), 0.8)
    return reverb(x, 0.5, 0.25)


def carta_carregada(rng, v):
    """Gambit: a carta carregando (o zumbido que sobe), o arremesso e a explosão."""
    x = _z(1.9)
    n = n_de(0.75)
    poe(x, seno(varre(400, 1600, n, 1.4), n) * sobe_e_some(n, 0.95, 1.0) * 0.05 + passa(rosa(rng, n), 2000, 7000, 2) * sobe_e_some(n, 0.95, 1.0) * 0.15, 0.0)
    poe(x, _whoosh(rng, 0.2, 1000, 6000, 0.6, 1.4, 0.5), 0.55)
    poe(x, _explosao(rng, 0.9, 65), 0.82)
    return reverb(x, 0.5, 0.25)


def simbionte(rng, v):
    """Venom: a gosma escorrendo (os sons molhados) e o rosnado grave do simbionte."""
    x = _z(1.9)
    for k in range(6):
        n = n_de(0.2)
        poe(x, passa(rosa(rng, n), 200, 1500, 2) * env(n, 0.01, 0.12) * 0.4 + seno(varre(300, 120, n), n) * env(n, 0.005, 0.1) * 0.05, 0.05 + 0.1 * k)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(65 + 8 * np.sin(2 * math.pi * 7 * t), n) + passa(rosa(rng, n), 80, 900, 2) * 0.7, 2.5) * sobe_e_some(n, 0.4, 1.2) * 0.2, 0.55)
    return reverb(x, 0.5, 0.25)


def carnificina(rng, v):
    """Carnificina: as lâminas explodindo do corpo (muitos cortes ao mesmo tempo) e a risada grave."""
    x = _z(1.9)
    poe(x, _baque(120, 60, 0.4, 0.5), 0.0)
    q = np.random.default_rng(4)
    for k in range(12):
        poe(x, _whoosh(rng, 0.12, 1500, 9000, 0.4, 1.5, 0.35), q.uniform(0.0, 0.3))
    for k in range(4):
        n = n_de(0.12)
        poe(x, satura(seno(varre(260, 200, n), n), 2.5) * env(n, 0.01, 0.08) * 0.07, 0.6 + 0.14 * k)
    return reverb(x, 0.5, 0.25)


def doombot(rng, v):
    """Doutor Destino: o Doombot ligando (o servo e o bipe), segurando o golpe (o clang) e se partindo."""
    x = _z(1.9)
    n = n_de(0.3)
    poe(x, seno(varre(300, 700, n), n) * env(n, 0.01, 0.2) * 0.05, 0.0)
    poe(x, _sino(rng, 400, 0.8, 0.12, METAL), 0.5)
    poe(x, _baque(200, 100, 0.25, 0.5), 0.5)
    for k in range(6):
        poe(x, _sino(rng, 800 + 300 * k, 0.25, 0.03, METAL), 0.6 + 0.05 * k)
    return reverb(x, 0.5, 0.25)


def ilusao(rng, v):
    """Loki: a imagem quebrando como vidro, a névoa e a risada que ecoa."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.05), 2000, 9000, 0.01), 0.1)
    for k in range(8):
        poe(x, _sino(rng, 2500 + 400 * (k % 4), 0.3, 0.03, VIDRO), 0.12 + 0.04 * k)
    poe(x, _sopro(rng, 1.0, 400, 3000, 0.25, 0.4), 0.3)
    for k in range(4):
        n = n_de(0.1)
        poe(x, seno(varre(520 - 30 * k, 440 - 30 * k, n), n) * env(n, 0.01, 0.07) * 0.03, 0.8 + 0.12 * k)
    return reverb(x, 0.8, 0.4)


def corpo_novo(rng, v):
    """Ultron: as peças voltando (os cliques de metal), a varredura (o tom que sobe) e os olhos ligando."""
    x = _z(1.9)
    q = np.random.default_rng(6)
    for k in range(10):
        poe(x, _sino(rng, q.uniform(1200, 3000), 0.15, 0.03, METAL), 0.05 + 0.04 * k)
    n = n_de(0.5)
    poe(x, seno(varre(300, 1200, n), n) * sobe_e_some(n, 0.8, 1.0) * 0.05, 0.5)
    poe(x, _baque(90, 45, 0.5, 0.6, 2.4), 1.0)
    poe(x, satura(seno(110, n_de(0.6)), 2) * env(n_de(0.6), 0.01, 0.4) * 0.08, 1.0)
    return reverb(x, 0.5, 0.25)


def abobora(rng, v):
    """Duende Verde: a bomba voando, os bipes acelerando e a explosão."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.45, 600, 3000, 0.6, 1.4, 0.4), 0.0)
    t0, passo = 0.5, 0.12
    while t0 < 0.95:
        m = n_de(0.04)
        poe(x, seno(1500, m) * env(m, 0.002, 0.03) * 0.06, t0)
        t0 += passo
        passo = max(0.04, passo * 0.7)
    poe(x, _explosao(rng, 1.0, 55), 1.0)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "mu-mana": (mana, "Frieren: o círculo e as flores de mana"),
    "mu-waku": (waku, "Anya: a leitura de mente"),
    "mu-strix": (strix, "Loid: a mira e as cargas"),
    "mu-espinho": (espinho, "Yor: o espinho cravando"),
    "mu-nivel": (nivel, "Jinwoo: subiu de nível"),
    "mu-kakuja": (kakuja, "Kaneki: os tentáculos de kagune"),
    "mu-carta-yugi": (carta_yugi, "Yugi: a carta e o Enigma"),
    "mu-olhos-azuis": (olhos_azuis, "Kaiba: o Dragão Branco"),
    "mu-cinetico": (cinetico, "Pantera Negra: a onda cinética"),
    "mu-hex": (hex_, "Feiticeira Escarlate: o hex"),
    "mu-joia-da-mente": (joia_da_mente, "Visão: a Joia da Mente"),
    "mu-energia-absorvida": (energia_absorvida, "Capitã Marvel: a energia absorvida"),
    "mu-interrogatorio": (interrogatorio, "Justiceiro: o interrogatório"),
    "mu-pecados": (pecados, "Motoqueiro Fantasma: a corrente em chamas"),
    "mu-cacador": (cacador, "Blade: a glaive"),
    "mu-crescentes": (crescentes, "Cavaleiro da Lua: os crescentes"),
    "mu-raio-rubi": (raio_rubi, "Ciclope: o raio sem controle"),
    "mu-elo-mental": (elo_mental, "Jean Grey: a Fênix e o elo"),
    "mu-toque": (toque, "Vampira: o poder roubado"),
    "mu-carta-carregada": (carta_carregada, "Gambit: a carta explodindo"),
    "mu-simbionte": (simbionte, "Venom: o simbionte"),
    "mu-carnificina": (carnificina, "Carnificina: as lâminas"),
    "mu-doombot": (doombot, "Doutor Destino: o Doombot"),
    "mu-ilusao": (ilusao, "Loki: a ilusão quebrando"),
    "mu-corpo-novo": (corpo_novo, "Ultron: o corpo novo"),
    "mu-abobora": (abobora, "Duende Verde: a bomba-abóbora"),
}
