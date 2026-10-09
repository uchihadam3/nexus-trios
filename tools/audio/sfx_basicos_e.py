"""Sons dos ataques básicos, lote e (veja tools/vfx/familias_v2/basicos_e.py).

Cada som segue o desenho da folha: o assobio que gira do batarangue e o "tchak" quando crava,
o estrondo sônico do Superman, o "thwip" da teia, o cristal da mandala do Estranho, o "clang"
dos braceletes, a carga e o "pew" do repulsor, o escudo que vibra, as asas do corvo da alma,
as seis joias da manopla, o caos distorcido da Wanda, o "zip" do Homem-Formiga, a luz da
Capitã Marvel e a corrente em chamas do Motoqueiro. Tudo sintetizado.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _tom, _whoosh, _z, nota  # noqa: F401
from som import (CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, graos, modal, n_de, passa, poe,  # noqa: F401
                 reverb, rosa, ruido, satura, seno, sobe_e_some, varre)


# nome do arquivo (com hífen) → (função, descrição)
SONS: dict = {}


def _t(n):
    return np.arange(n) / SR


def _giro(n, f0, f1):
    """Modulação de amplitude que acelera/desacelera: o "vup-vup-vup" de algo girando."""
    f = varre(f0, f1, n, 1.0)
    return 0.55 + 0.45 * np.sin(2 * math.pi * np.cumsum(f) / SR)


def _metal(rng, seg, f0, queda=0.35, g=0.3, tipo=METAL):
    n = n_de(seg)
    return modal(n, f0, rng=rng, **tipo) * env(n, 0.0005, queda) * g


def _elos(rng, seg, quantos, inicio, fim, g=0.12):
    """Chacoalhar de corrente: pinguinhos metálicos agudos e estalinhos espalhados."""
    x = _z(seg)
    for _ in range(quantos):
        m = n_de(0.06)
        f = rng.uniform(2600, 4800)
        ping = modal(m, f, rng=rng, **METAL) * env(m, 0.0003, 0.012) * 0.6 + estalo(rng, m, 3000, 9000, 0.002) * 0.5
        poe(x, ping * rng.uniform(0.5, 1.0) * g, rng.uniform(inicio, fim))
    return x


# ------------------------------------------------------------------ Batman
def batarangue(rng, v):
    """Assobio que gira (o batarangue cortando o ar, cada vez mais perto) e o "tchak" seco quando crava."""
    x = _z(0.75)
    n = n_de(0.24)
    vento = assobio(rng, n, 1800, 4200, 1.3, 0.35) * _giro(n, 18, 30) * sobe_e_some(n, 0.92, 1.6) * 0.9
    poe(x, vento, 0.0)
    poe(x, seno(varre(1500, 2300, n, 1.0), n) * _giro(n, 18, 30) * sobe_e_some(n, 0.9, 1.8) * 0.06, 0.0)
    em = 0.22
    m = n_de(0.4)
    tchak = estalo(rng, m, 1800, 9000, 0.004) * 1.2 + baque(m, 520, 260, 0.02, 0.5) * 0.45
    tchak += modal(m, rng.uniform(1700, 2000), rng=rng, **METAL) * env(m, 0.0004, 0.05) * 0.25
    # a lâmina presa vibrando um instante
    tt = _t(m)
    tchak += np.sin(2 * math.pi * 330 * tt) * np.exp(-tt / 0.09) * (0.5 + 0.5 * np.sin(2 * math.pi * 38 * tt)) * 0.12
    poe(x, tchak, em)
    return reverb(x, 0.3, 0.12)


# ------------------------------------------------------------------ Superman
def soco_de_aco(rng, v):
    """O ar rasgando, o estrondo sônico duplo ("ba-BUM") e o soco pesado com o ronco que fica."""
    x = _z(1.2)
    n = n_de(0.2)
    poe(x, assobio(rng, n, 300, 5000, 1.6, 0.5) * sobe_e_some(n, 0.95, 2.0) * 1.0, 0.0)
    em = 0.18
    for k, d in enumerate((0.0, 0.035)):
        m = n_de(0.5)
        estrondo = satura(passa(ruido(rng, m), 60, 2200, 2) * env(m, 0.0005, 0.03 + 0.03 * k), 2.5) * (0.7 if k == 0 else 1.0)
        poe(x, estrondo + baque(m, 75, 30, 0.18, 0.7) * (0.6 + 0.4 * k), em + d)
    poe(x, B.soco_pesado(rng, v), em + 0.035, 1.0)
    m = n_de(0.9)
    ronco = passa(rosa(rng, m), 40, 500, 2) * env(m, 0.01, 0.35) * 0.55
    poe(x, ronco, em + 0.04)
    return reverb(x, 0.75, 0.3, 4500)


# ------------------------------------------------------------------ Homem-Aranha
def teia_e_soco(rng, v):
    """"Thwip" (o disparo da teia), o "splat" grudando, e o soco que chega logo depois."""
    x = _z(0.9)
    n = n_de(0.09)
    thwip = assobio(rng, n, 7500, 2200, 0.8, 0.4) * env(n, 0.002, 0.03) * 1.3
    thwip += seno(varre(2600, 700, n, 0.6), n) * env(n, 0.001, 0.025) * 0.25
    poe(x, thwip, 0.0)
    m = n_de(0.2)
    splat = passa(ruido(rng, m), 400, 3000, 2) * env(m, 0.001, 0.035) * 0.55 + _tom(320, 160, 0.2, 0.05, 0.18)
    poe(x, splat, 0.11)
    # o puxão: um rangido curto do fio esticando
    k = n_de(0.08)
    poe(x, seno(varre(900, 1500, k, 1.0), k) * env(k, 0.01, 0.03) * 0.08, 0.27)
    poe(x, _whoosh(rng, 0.12, 500, 3500, 0.9, g=0.55), 0.3)
    poe(x, B.soco_leve(rng, v), 0.4, 1.05)
    poe(x, baque(n_de(0.25), 110, 55, 0.06, 0.3) * 0.5, 0.4)
    return reverb(x, 0.3, 0.12)


# ------------------------------------------------------------------ Doutor Estranho
def disparo_arcano(rng, v):
    """A mandala acende num acorde de cristal que sobe, as faíscas saem (quatro "tsing") e acertam
    num crepitar de energia arcana."""
    x = _z(1.2)
    n = n_de(0.32)
    poe(x, assobio(rng, n, 600, 3500, 1.0, 0.4) * sobe_e_some(n, 0.8, 1.4) * 0.35, 0.0)
    for k, m in enumerate((69, 76, 81, 88)):
        poe(x, _brilho(rng, 0.5, nota(m), 0.11, CRISTAL), 0.02 + k * 0.035)
    tt = _t(n)
    zumbido = seno(nota(57) * (1 + 0.004 * np.sin(2 * math.pi * 7 * tt)), n) * sobe_e_some(n, 0.7, 1.5) * 0.08
    poe(x, zumbido, 0.0)
    for k in range(4):
        m = n_de(0.1)
        tsing = seno(varre(nota(rng.uniform(86, 92)), nota(rng.uniform(79, 83)), m, 1.0), m) * env(m, 0.001, 0.04) * 0.12
        poe(x, tsing + estalo(rng, m, 3000, 10000, 0.003) * 0.25, 0.15 + 0.04 * k)
    em = 0.27
    m = n_de(0.6)
    poe(x, graos(rng, m, 45, 0.0, 0.4, 2200, 9000, 0.0025, 0.6) * 0.55, em)
    poe(x, baque(m, 140, 70, 0.06, 0.3) * 0.4 + passa(rosa(rng, m), 800, 5000, 2) * env(m, 0.002, 0.08) * 0.35, em)
    poe(x, _brilho(rng, 0.6, nota(84), 0.12, CRISTAL), em)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Mulher-Maravilha
def bracelete(rng, v):
    """O "clang" dos braceletes batendo em X (metal que soa e brilha), e o soco que vem atrás."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.09, 800, 4000, 0.9, g=0.4), 0.0)
    em = 0.07
    m = n_de(0.9)
    clang = modal(m, rng.uniform(780, 860), rng=rng, desafina=0.01, **METAL) * env(m, 0.0003, 0.45) * 0.42
    clang += modal(m, rng.uniform(1230, 1300), rng=rng, **METAL) * env(m, 0.0003, 0.25) * 0.22
    clang += estalo(rng, m, 2500, 11000, 0.005) * 0.9
    clang += baque(m, 300, 180, 0.03, 0.4) * 0.3
    poe(x, clang, em)
    poe(x, graos(rng, n_de(0.3), 12, 0.0, 0.15, 4000, 10000, 0.002) * 0.25, em + 0.01)
    poe(x, _whoosh(rng, 0.12, 400, 3000, 0.9, g=0.6), 0.25)
    poe(x, B.soco_pesado(rng, v), 0.36, 1.0)
    poe(x, _metal(rng, 0.4, 1100, 0.12, 0.12), 0.36)
    return reverb(x, 0.45, 0.2)


# ------------------------------------------------------------------ Homem de Ferro
def repulsor(rng, v):
    """A carga eletrônica que sobe zunindo na palma, o "pew" grave do repulsor e o estouro no alvo."""
    x = _z(1.0)
    n = n_de(0.2)
    f = varre(380, 1700, n, 0.9)
    carga = seno(f * (1 + 0.02 * seno(f * 0.5, n)), n) * 0.18 + seno(f * 2.01, n) * 0.05
    carga *= sobe_e_some(n, 0.97, 1.4) * (0.75 + 0.25 * np.sin(2 * math.pi * 55 * _t(n)))
    poe(x, carga, 0.0)
    em = 0.18
    m = n_de(0.32)
    pew = satura(seno(varre(1100, 95, m, 0.45), m) * env(m, 0.002, 0.11) * 1.2, 2.2) * 0.55
    pew += seno(varre(2200, 190, m, 0.45), m) * env(m, 0.001, 0.05) * 0.12
    pew += passa(ruido(rng, m), 1500, 9000, 2) * env(m, 0.001, 0.02) * 0.45
    poe(x, pew, em)
    poe(x, B.impacto_energia(rng, v), em + 0.08, 0.8)
    poe(x, baque(n_de(0.4), 90, 40, 0.12, 0.3) * 0.5, em + 0.08)
    return reverb(x, 0.5, 0.22)


# ------------------------------------------------------------------ Capitão América
def escudo_do_capitao(rng, v):
    """O escudo girando no ar ("vum-vum-vum"), o "CLANG" de metal que fica vibrando, e ele voltando."""
    x = _z(1.4)
    n = n_de(0.24)
    poe(x, assobio(rng, n, 500, 1800, 1.2, 0.4) * _giro(n, 11, 16) * sobe_e_some(n, 0.92, 1.4) * 0.8, 0.0)
    em = 0.22
    m = n_de(1.1)
    tt = _t(m)
    vibra = 1 + 0.35 * np.sin(2 * math.pi * 7 * tt)      # o metal batendo dois tons próximos
    clang = (modal(m, 520, rng=rng, **METAL) + modal(m, 527, rng=rng, **METAL) * 0.8) * env(m, 0.0003, 0.55) * vibra * 0.3
    clang += modal(m, 1630, rng=rng, **METAL) * env(m, 0.0003, 0.18) * 0.15
    clang += estalo(rng, m, 2000, 10000, 0.006) * 1.0 + baque(m, 160, 80, 0.06, 0.6) * 0.55
    poe(x, clang, em)
    k = n_de(0.35)
    poe(x, assobio(rng, k, 1600, 500, 1.0, 0.4) * _giro(k, 15, 9) * env(k, 0.02, 0.12) * 0.45, em + 0.12)
    return reverb(x, 0.55, 0.25)


# ------------------------------------------------------------------ Ravena
def corvo_da_alma(rng, v):
    """Asas grandes batendo ("fuóm-fuóm"), um sussurro sombrio de ar (sem voz) e o mergulho que
    envolve o alvo num baque abafado de sombra."""
    x = _z(1.3)
    for k in range(3):
        m = n_de(0.13)
        asa = passa(rosa(rng, m), 180, 1400, 2) * sobe_e_some(m, 0.35, 1.3) * (0.55 + 0.1 * k)
        poe(x, asa + passa(ruido(rng, m), 1500, 4000, 2) * env(m, 0.01, 0.03) * 0.08, k * 0.09)
    n = n_de(0.9)
    tt = _t(n)
    sopro = rosa(rng, n)
    sussurro = passa(sopro, 1800, 5200, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3.3 * tt + 1)) * sobe_e_some(n, 0.35, 1.3) * 0.28
    sussurro += passa(sopro, 700, 1100, 2) * sobe_e_some(n, 0.4, 1.2) * 0.12
    poe(x, sussurro, 0.05)
    grave = satura(seno(varre(nota(36), nota(31), n, 1.0), n), 1.8) * sobe_e_some(n, 0.3, 1.2) * 0.14
    poe(x, grave, 0.05)
    em = 0.3
    m = n_de(0.6)
    poe(x, _whoosh(rng, 0.2, 2500, 250, 0.3, g=0.6), em - 0.06)
    poe(x, baque(m, 85, 38, 0.2, 0.3) * 0.75 + passa(rosa(rng, m), 100, 900, 2) * env(m, 0.005, 0.15) * 0.4, em)
    return reverb(x, 0.8, 0.35, 3000)


# ------------------------------------------------------------------ Thanos
def manopla(rng, v):
    """O soco pesadíssimo da manopla e, logo depois, seis brilhos cristalinos (as joias) estourando."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.18, 150, 2000, 0.95, g=0.75), 0.0)
    em = 0.16
    poe(x, B.esmagar(rng, v), em, 1.0)
    poe(x, baque(n_de(0.5), 60, 28, 0.2, 0.5) * 0.6, em)
    poe(x, _metal(rng, 0.3, 420, 0.1, 0.12), em)
    for k, m in enumerate((79, 83, 86, 90, 93, 98)):
        poe(x, _brilho(rng, 0.45, nota(m + rng.uniform(-0.1, 0.1)), 0.11, CRISTAL), em + 0.07 + 0.035 * k)
    m = n_de(0.7)
    poe(x, passa(rosa(rng, m), 2000, 9000, 2) * env(m, 0.02, 0.25) * 0.08, em + 0.08)
    return reverb(x, 0.65, 0.3)


# ------------------------------------------------------------------ Feiticeira Escarlate
def magia_do_caos(rng, v):
    """Magia do caos: um acorde torto que oscila (dois tons desafinados com vibrato e modulação em
    anel), o rodamoinho apertando e o estouro distorcido."""
    x = _z(1.3)
    n = n_de(0.5)
    tt = _t(n)
    f = varre(nota(55), nota(62), n, 1.0) * (1 + 0.02 * np.sin(2 * math.pi * 6.5 * tt))
    torto = seno(f, n) * seno(f * 1.414 + 37, n) * 0.35 + seno(f * 0.5 * 1.012, n) * 0.18
    torto = satura(torto * 1.5, 2.0) * sobe_e_some(n, 0.9, 1.2)
    poe(x, torto * 0.5, 0.0)
    redemoinho = assobio(rng, n, 400, 2600, 1.5, 0.4) * (0.6 + 0.4 * np.sin(2 * math.pi * np.cumsum(varre(5, 20, n)) / SR)) * sobe_e_some(n, 0.95, 1.4) * 0.5
    poe(x, redemoinho, 0.0)
    em = 0.38
    m = n_de(0.8)
    tm = _t(m)
    estouro = satura(passa(ruido(rng, m), 150, 4000, 2) * env(m, 0.001, 0.07), 3) * 0.6
    estouro += baque(m, 95, 40, 0.18, 0.4) * 0.6
    queda = seno(varre(nota(62), nota(43), m, 0.7), m) * seno(varre(nota(62), nota(43), m, 0.7) * 1.5 + 23, m)
    estouro += satura(queda * env(m, 0.003, 0.25) * 1.4, 2.5) * 0.25 * (1 + 0.3 * np.sin(2 * math.pi * 9 * tm))
    poe(x, estouro, em)
    return reverb(x, 0.7, 0.32, 4000)


# ------------------------------------------------------------------ Homem-Formiga
def soco_de_pym(rng, v):
    """O "zip" agudo de encolher (o tom sobe rapidinho), a volta ao tamanho num "vrum" que desce
    grave, e o soco gigante."""
    x = _z(1.0)
    n = n_de(0.13)
    zip_ = seno(varre(500, 4200, n, 0.8), n) * env(n, 0.002, 0.08) * 0.22
    zip_ += assobio(rng, n, 2500, 9000, 1.0, 0.35) * env(n, 0.002, 0.06) * 0.4
    poe(x, zip_, 0.0)
    poe(x, graos(rng, n_de(0.2), 10, 0.0, 0.15, 5000, 11000, 0.002) * 0.2, 0.05)
    em = 0.22
    m = n_de(0.16)
    cresce = satura(seno(varre(3500, 70, m, 0.5), m) * env(m, 0.002, 0.1), 2.0) * 0.4
    cresce += assobio(rng, m, 6000, 300, 0.7, 0.45) * sobe_e_some(m, 0.3, 1.3) * 0.5
    poe(x, cresce, em)
    poe(x, B.soco_pesado(rng, v), em + 0.11, 1.1)
    poe(x, baque(n_de(0.5), 70, 30, 0.2, 0.4) * 0.6, em + 0.11)
    return reverb(x, 0.45, 0.2)


# ------------------------------------------------------------------ Capitã Marvel
def punho_fotonico(rng, v):
    """Zumbido de energia fotônica que cresce no punho, o soco, e a explosão de luz que brilha alto."""
    x = _z(1.2)
    n = n_de(0.2)
    tt = _t(n)
    f = varre(nota(52), nota(64), n, 1.0)
    zumbido = (seno(f, n) + seno(f * 2.003, n) * 0.5 + seno(f * 3.01, n) * 0.25) * (0.8 + 0.2 * np.sin(2 * math.pi * 40 * tt))
    poe(x, zumbido * sobe_e_some(n, 0.95, 1.3) * 0.16, 0.0)
    poe(x, assobio(rng, n, 600, 4500, 1.3, 0.45) * sobe_e_some(n, 0.95, 1.8) * 0.55, 0.0)
    em = 0.17
    poe(x, B.soco_pesado(rng, v), em, 0.8)
    poe(x, B.explosao(rng, v), em, 0.55)
    for k, m in enumerate((84, 88, 91, 96)):
        poe(x, _brilho(rng, 0.6, nota(m), 0.09, SINO), em + 0.01 + 0.02 * k)
    m = n_de(0.5)
    poe(x, passa(ruido(rng, m), 3000, 11000, 2) * env(m, 0.001, 0.12) * 0.3, em)
    return reverb(x, 0.6, 0.28)


# ------------------------------------------------------------------ Motoqueiro Fantasma
def corrente_flamejante(rng, v):
    """A corrente chacoalhando no chicote, o estalo da ponta, os elos enrolando no alvo e o fogo
    rugindo até estourar em brasas."""
    x = _z(1.3)
    n = n_de(0.24)
    poe(x, _whoosh(rng, 0.24, 300, 3500, 0.85, g=0.55), 0.0)
    poe(x, _elos(rng, 0.3, 26, 0.0, 0.22, 0.6), 0.0)
    em = 0.21
    m = n_de(0.15)
    estalo_ponta = passa(ruido(rng, m), 1800, 10000, 2) * env(m, 0.0003, 0.01) * 2.2 + baque(m, 700, 350, 0.015, 0.8) * 0.5
    poe(x, estalo_ponta, em)
    poe(x, _elos(rng, 0.4, 30, 0.0, 0.25, 0.5), em + 0.02)
    poe(x, baque(n_de(0.3), 120, 60, 0.07, 0.3) * 0.45, em + 0.03)
    poe(x, B.fogo(rng, v), em + 0.03, 0.6)
    m = n_de(0.7)
    rugido = satura(passa(rosa(rng, m), 70, 900, 2) * sobe_e_some(m, 0.55, 1.2) * 1.6, 2.2) * 0.4
    poe(x, rugido, em + 0.05)
    poe(x, graos(rng, n_de(0.6), 35, 0.0, 0.5, 2000, 9000, 0.003, 0.6) * 0.35, 0.45)
    poe(x, baque(n_de(0.4), 85, 40, 0.15, 0.4) * 0.45, 0.45)
    return reverb(x, 0.5, 0.22)


SONS["batarangue"] = (batarangue, "básico de Batman: assobio do batarangue girando e o \"tchak\" quando crava")
SONS["soco-de-aco"] = (soco_de_aco, "básico de Superman: estrondo sônico duplo e o soco pesado")
SONS["teia-e-soco"] = (teia_e_soco, "básico de Homem-Aranha: \"thwip\" da teia, o splat e o soco")
SONS["disparo-arcano"] = (disparo_arcano, "básico de Doutor Estranho: acorde de cristal da mandala e crepitar arcano")
SONS["bracelete"] = (bracelete, "básico de Mulher-Maravilha: \"clang\" dos braceletes e o soco")
SONS["repulsor"] = (repulsor, "básico de Homem de Ferro: carga eletrônica e o \"pew\" grave do repulsor")
SONS["escudo-do-capitao"] = (escudo_do_capitao, "básico de Capitão América: escudo girando e o clang metálico que vibra")
SONS["corvo-da-alma"] = (corvo_da_alma, "básico de Ravena: asas batendo e sussurro sombrio de ar")
SONS["manopla"] = (manopla, "básico de Thanos: soco pesado da manopla e seis brilhos cristalinos")
SONS["magia-do-caos"] = (magia_do_caos, "básico de Feiticeira Escarlate: magia do caos distorcida e sinistra")
SONS["soco-de-pym"] = (soco_de_pym, "básico de Homem-Formiga: \"zip\" de encolher e o soco que cresce")
SONS["punho-fotonico"] = (punho_fotonico, "básico de Capitã Marvel: energia fotônica e explosão de luz")
SONS["corrente-flamejante"] = (corrente_flamejante, "básico de Motoqueiro Fantasma: corrente chacoalhando e fogo rugindo")
