"""Os sons da rodada 18: Shazam, Tifa Lockhart, Sephiroth, Link e Zelda (veja
tools/vfx/familias_v2/rodada18.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada14 import _trovao
from sfx_rodada15 import _coro_mistico
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _soco(rng, g=0.6, f0=110):
    """O soco de luva: o baque seco com o estalo do couro."""
    n = n_de(0.25)
    return (satura(baque(n, f0, f0 * 0.45, 0.07, 1.0), 1.8) * 0.8 + estalo(rng, n, 1500, 6000, 0.006) * 0.4) * g


def _corte(rng, seg=0.3, lo=2500, hi=11000, g=0.5):
    """O corte da lâmina: o assobio fino e agudo que corta o ar."""
    n = n_de(seg)
    return passa(rosa(rng, n), lo, hi, 2) * sobe_e_some(n, 0.35, 2.5) * g


def _penas(rng, seg, g=0.15):
    """As penas caindo: o farfalhar suave e intermitente."""
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 1500, 6000, 2) * (0.4 + 0.6 * np.abs(np.sin(2 * math.pi * 3.3 * t))) * sobe_e_some(n, 0.3, 1.2) * g


def _harpa(notas, passo, g=0.05, tipo=CRISTAL):
    """O arpejo de luz (a harpa de Hyrule): notas cristalinas em sequência."""
    total = _z(passo * len(notas) + 0.8)
    for k, f in enumerate(notas):
        m = n_de(0.8)
        poe(total, modal(m, f, **tipo) * env(m, 0.002, 0.4) * g, passo * k)
    return total


# =================================================================== Shazam
def raio_magico(rng, v):
    """O raio mágico: o "SHAZAM!" em trovão — o estalo do raio caindo, o ronco e o brilho dourado da aura."""
    x = _z(2.0)
    poe(x, passa(rosa(rng, n_de(0.12)), 2000, 9000, 2) * sobe_e_some(n_de(0.12), 0.9, 1.0) * 0.3, 0.0)
    poe(x, _trovao(rng, 1.4, 0.9), 0.1)
    poe(x, satura(baque(n_de(0.5), 70, 30, 0.2, 1.0), 1.8) * 0.6, 0.12)
    for k in range(3):
        poe(x, _brilho(rng, 0.5, 784 * (1.26 ** k), 0.05, SINO), 0.55 + 0.06 * k)
    return reverb(x, 0.6, 0.3)


def forca_de_hercules(rng, v):
    """A força de Hércules: o punho erguido (o "vum" grave que sobe), o pulso de força e o escudo fechando com o
    acorde dourado."""
    x = _z(1.6)
    n = n_de(0.35)
    poe(x, seno(varre(60, 140, n, 1.0), n) * sobe_e_some(n, 0.8, 1.2) * 0.25, 0.0)
    for k in range(3):
        poe(x, satura(baque(n_de(0.25), 80, 50, 0.08, 0.3), 1.4) * 0.35, 0.25 + 0.12 * k)
    m = n_de(0.9)
    poe(x, (seno(392, m) + seno(494, m) * 0.7 + seno(587, m) * 0.5) * env(m, 0.01, 0.5) * 0.05, 0.5)
    poe(x, modal(n_de(0.6), 784, rng=rng, **SINO) * env(n_de(0.6), 0.002, 0.3) * 0.1, 0.5)
    return reverb(x, 0.6, 0.3)


def shazam_preparo(rng, v):
    """O Preparo da Sabedoria de Salomão: as seis letras acendendo (seis "tim" que sobem) e as faíscas elétricas."""
    x = _z(1.4)
    for k, f in enumerate((523, 587, 659, 698, 784, 880)):
        poe(x, modal(n_de(0.3), f, rng=rng, **SINO) * env(n_de(0.3), 0.002, 0.15) * 0.07, 0.05 + 0.18 * k)
    n = n_de(1.3)
    poe(x, graos(rng, n, 40, 0.0, 1.2, 3000, 9000, 0.003) * 0.25, 0.05)
    return reverb(x, 0.6, 0.3)


def sabedoria_de_salomao(rng, v):
    """A sabedoria de Salomão: o pergaminho desenrolando, a runa voando (o tom que sobe) e o Preparo do rival
    quebrando como vidro."""
    x = _z(1.8)
    m = n_de(0.3)
    poe(x, passa(rosa(rng, m), 800, 4000, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 9 * _t(m)))) * sobe_e_some(m, 0.4, 1.2) * 0.2, 0.0)
    n = n_de(0.2)
    poe(x, seno(varre(600, 1600, n, 1.0), n) * env(n, 0.005, 0.15) * 0.05, 0.25)
    poe(x, modal(n_de(0.8), 1800, rng=rng, **VIDRO) * env(n_de(0.8), 0.0005, 0.25) * 0.2, 0.42)
    poe(x, graos(rng, n_de(0.6), 40, 0.0, 0.5, 3000, 10000, 0.008) * 0.4, 0.42)
    poe(x, satura(baque(n_de(0.3), 100, 50, 0.08, 0.8), 1.6) * 0.4, 0.42)
    return reverb(x, 0.6, 0.3)


# =================================================================== Tifa
def golpe_de_abertura(rng, v):
    """O golpe de abertura: dois jabs rápidos, o gancho pesado e a guarda trincando (o estalo que racha)."""
    x = _z(1.3)
    poe(x, _soco(rng, 0.45, 140), 0.08)
    poe(x, _soco(rng, 0.45, 130), 0.18)
    poe(x, _whoosh(rng, 0.12, 300, 2000, 0.8, 1.3, 0.3), 0.2)
    poe(x, _soco(rng, 0.8, 95), 0.3)
    poe(x, graos(rng, n_de(0.3), 25, 0.0, 0.25, 1500, 6000, 0.01) * 0.6 + estalo(rng, n_de(0.3), 800, 4000, 0.03) * 0.5, 0.33)
    return reverb(x, 0.4, 0.2)


def chuva_de_socos(rng, v):
    """A chuva de socos: oito socos rápidos em ritmo, cada um com o "tuf", e o fôlego do ar no fim."""
    x = _z(1.5)
    for k in range(8):
        poe(x, _soco(rng, 0.38 + 0.03 * k, 120 + 10 * (k % 3)), 0.06 + 0.06 * k)
    poe(x, _whoosh(rng, 0.25, 500, 3000, 0.4, 1.3, 0.2), 0.55)
    return reverb(x, 0.4, 0.2)


def tifa_preparo(rng, v):
    """O Preparo da Explosão final: os punhos apertando (o couro rangendo), a energia vermelha subindo e o chão
    tremendo grave."""
    x = _z(1.4)
    m = n_de(0.3)
    poe(x, passa(rosa(rng, m), 400, 2000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 25 * _t(m))) * env(m, 0.02, 0.2) * 0.2, 0.0)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 30, 200, 2) * sobe_e_some(n, 0.8, 1.0) * 0.5, 0.15)
    poe(x, satura(seno(varre(80, 220, n, 1.0), n), 1.5) * sobe_e_some(n, 0.9, 1.0) * 0.05, 0.15)
    return reverb(x, 0.5, 0.25)


def explosao_final(rng, v):
    """A explosão final: o soco descendo (o "vum"), o golpe no chão (o estrondo), a coluna de energia rugindo e os
    destroços caindo."""
    x = _z(2.2)
    poe(x, _whoosh(rng, 0.2, 200, 1500, 0.9, 1.3, 0.5), 0.0)
    poe(x, satura(baque(n_de(1.0), 55, 22, 0.35, 1.0), 2.0) * 1.0, 0.2)
    n = n_de(0.7)
    poe(x, satura(passa(rosa(rng, n), 100, 3000, 2), 1.8) * sobe_e_some(n, 0.15, 1.3) * 0.5, 0.2)
    poe(x, graos(rng, n_de(0.9), 50, 0.1, 0.8, 300, 3000, 0.012) * 0.6, 0.35)
    return reverb(x, 0.7, 0.35)


# =================================================================== Sephiroth
def corte_sombrio(rng, v):
    """O corte sombrio: a lâmina longuíssima cortando o ar (o assobio que dura), o golpe seco e as penas caindo, com o
    tom grave do coro."""
    x = _z(1.8)
    poe(x, _corte(rng, 0.35, 2500, 12000, 0.55), 0.06)
    poe(x, modal(n_de(0.6), 2200, rng=rng, **METAL) * env(n_de(0.6), 0.0005, 0.2) * 0.15, 0.2)
    poe(x, satura(baque(n_de(0.3), 120, 60, 0.06, 0.8), 1.6) * 0.4, 0.2)
    poe(x, _penas(rng, 1.0, 0.12), 0.35)
    m = n_de(1.0)
    poe(x, _coro_mistico(m, 110, 0.04) * sobe_e_some(m, 0.3, 1.3), 0.25)
    return reverb(x, 0.7, 0.35)


def sephiroth_preparo(rng, v):
    """O Preparo do Heartless Angel: a asa negra abrindo (o "fuup" grave das penas) e o coro sombrio que sobe."""
    x = _z(1.4)
    poe(x, passa(rosa(rng, n_de(0.5)), 150, 1500, 2) * sobe_e_some(n_de(0.5), 0.6, 1.3) * 0.35, 0.0)
    n = n_de(1.3)
    poe(x, _coro_mistico(n, 98, 0.05) * sobe_e_some(n, 0.6, 1.0), 0.05)
    poe(x, _penas(rng, 1.2, 0.1), 0.2)
    return reverb(x, 0.8, 0.4)


def heartless_angel(rng, v):
    """O Heartless Angel: a asa enorme abrindo, o coro dissonante crescendo, a luz sendo sugada (o tom que cai) de
    todos os rivais e o silêncio pesado no fim."""
    x = _z(2.4)
    poe(x, passa(rosa(rng, n_de(0.6)), 100, 1200, 2) * sobe_e_some(n_de(0.6), 0.5, 1.3) * 0.45, 0.0)
    n = n_de(1.4)
    poe(x, (_coro_mistico(n, 110, 0.04) + _coro_mistico(n, 116.5, 0.03)) * sobe_e_some(n, 0.5, 1.2), 0.15)
    for k in range(3):
        m = n_de(0.5)
        poe(x, seno(varre(1600 - 200 * k, 200, m, 1.5), m) * env(m, 0.01, 0.35) * 0.05, 0.4 + 0.07 * k)
    poe(x, satura(baque(n_de(0.8), 50, 25, 0.3, 0.5), 1.6) * 0.5, 0.85)
    poe(x, _penas(rng, 1.2, 0.08), 0.6)
    return reverb(x, 0.9, 0.45)


# =================================================================== Link
def escudo_hyliano(rng, v):
    """O escudo hyliano: o escudo erguido, o golpe batendo no metal (o "tchang") com as faíscas e o contra-ataque
    da espada."""
    x = _z(1.4)
    poe(x, _whoosh(rng, 0.15, 300, 1200, 0.7, 1.3, 0.25), 0.0)
    poe(x, modal(n_de(0.7), 520, rng=rng, **METAL) * env(n_de(0.7), 0.0005, 0.25) * 0.4, 0.25)
    poe(x, satura(baque(n_de(0.3), 110, 60, 0.05, 1.0), 1.5) * 0.4, 0.25)
    poe(x, graos(rng, n_de(0.3), 20, 0.0, 0.2, 3000, 10000, 0.004) * 0.4, 0.26)
    poe(x, _corte(rng, 0.22, 2500, 10000, 0.45), 0.48)
    return reverb(x, 0.5, 0.25)


def link_preparo(rng, v):
    """O Preparo do Golpe giratório: a espada carregando (o zumbido que sobe) com os "tilim" da energia."""
    x = _z(1.4)
    n = n_de(1.3)
    poe(x, seno(varre(300, 1200, n, 1.3), n) * sobe_e_some(n, 0.9, 1.0) * 0.05, 0.0)
    poe(x, (seno(varre(450, 1800, n, 1.3), n)) * sobe_e_some(n, 0.9, 1.0) * 0.02, 0.0)
    for k in range(4):
        poe(x, _brilho(rng, 0.3, 1568 + 200 * k, 0.03, CRISTAL), 0.2 + 0.3 * k)
    return reverb(x, 0.5, 0.25)


def golpe_giratorio(rng, v):
    """O golpe giratório: o grito curto do esforço (o "hyaa" em tom), o giro da espada (o assobio que dá a volta) e o
    estouro de energia."""
    x = _z(1.6)
    m = n_de(0.18)
    poe(x, passa(satura(seno(varre(520, 380, m, 1.0), m), 1.8), 300, 3000, 2) * env(m, 0.01, 0.12) * 0.07, 0.0)
    n = n_de(0.4)
    giro = passa(rosa(rng, n), 1500, 9000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 5 * _t(n)) ** 2) * sobe_e_some(n, 0.5, 1.2)
    poe(x, giro * 0.5, 0.05)
    poe(x, satura(baque(n_de(0.5), 90, 40, 0.12, 0.8), 1.6) * 0.6, 0.4)
    poe(x, _brilho(rng, 0.6, 1047, 0.06, CRISTAL), 0.42)
    return reverb(x, 0.6, 0.3)


# =================================================================== Zelda
def selo_da_luz(rng, v):
    """O selo da luz: o círculo se desenhando (o arpejo da harpa), as faixas de luz prendendo e o clarão."""
    x = _z(1.8)
    poe(x, _harpa((587, 740, 880, 1175, 1480), 0.06, 0.05), 0.0)
    n = n_de(0.5)
    poe(x, seno(varre(400, 1600, n, 1.0), n) * sobe_e_some(n, 0.8, 1.2) * 0.04, 0.2)
    poe(x, passa(rosa(rng, n_de(0.4)), 3000, 12000, 2) * env(n_de(0.4), 0.002, 0.2) * 0.3, 0.35)
    poe(x, modal(n_de(0.8), 2349, rng=rng, **CRISTAL) * env(n_de(0.8), 0.001, 0.4) * 0.08, 0.35)
    return reverb(x, 0.7, 0.35)


def barreira_sagrada(rng, v):
    """A barreira sagrada: os cristais se formando um a um (três "tching" de vidro) e o acorde sagrado."""
    x = _z(1.8)
    for k, f in enumerate((1319, 1568, 1976)):
        poe(x, modal(n_de(0.8), f, rng=rng, **VIDRO) * env(n_de(0.8), 0.001, 0.35) * 0.14, 0.05 + 0.05 * k)
    m = n_de(1.2)
    poe(x, (seno(587, m) + seno(740, m) * 0.7 + seno(880, m) * 0.6) * sobe_e_some(m, 0.3, 1.4) * 0.03, 0.2)
    poe(x, graos(rng, n_de(0.6), 20, 0.0, 0.5, 4000, 10000, 0.004) * 0.2, 0.5)
    return reverb(x, 0.8, 0.4)


def zelda_preparo(rng, v):
    """O Preparo da Flecha de luz: o arco de luz se formando, a corda esticando (o rangido) e a flecha acendendo."""
    x = _z(1.4)
    poe(x, _harpa((880, 1109, 1319), 0.08, 0.04), 0.0)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 600, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 30 * _t(n))) * sobe_e_some(n, 0.9, 1.0) * 0.08, 0.3)
    poe(x, seno(varre(800, 1600, n, 1.0), n) * sobe_e_some(n, 0.9, 1.0) * 0.03, 0.3)
    return reverb(x, 0.6, 0.3)


def flecha_de_luz(rng, v):
    """A flecha de luz: a corda soltando (o "tuong"), a flecha cruzando (o assobio brilhante), o impacto de luz e o
    sino do selo que cala."""
    x = _z(1.8)
    poe(x, satura(seno(varre(180, 120, n_de(0.2), 1.0), n_de(0.2)), 1.6) * env(n_de(0.2), 0.002, 0.1) * 0.2, 0.1)
    n = n_de(0.2)
    poe(x, (passa(rosa(rng, n), 3000, 12000, 2) * 0.3 + seno(varre(1800, 2600, n, 1.0), n) * 0.03) * sobe_e_some(n, 0.8, 1.2), 0.12)
    poe(x, satura(baque(n_de(0.4), 130, 60, 0.08, 0.8), 1.5) * 0.4, 0.3)
    poe(x, modal(n_de(0.8), 1760, rng=rng, **CRISTAL) * env(n_de(0.8), 0.001, 0.3) * 0.12, 0.3)
    poe(x, modal(n_de(1.0), 660, rng=rng, **SINO) * env(n_de(1.0), 0.002, 0.5) * 0.1, 0.5)
    return reverb(x, 0.7, 0.35)


SONS: dict = {
    "raio-magico": (raio_magico, "Shazam: o raio caindo e o trovão"),
    "forca-de-hercules": (forca_de_hercules, "Shazam: o punho e o escudo dourado"),
    "shazam-preparo": (shazam_preparo, "Shazam: as seis letras acendendo (antes do golpe)"),
    "sabedoria-de-salomao": (sabedoria_de_salomao, "Shazam: o pergaminho e o Preparo quebrando"),
    "golpe-de-abertura": (golpe_de_abertura, "Tifa: os jabs, o gancho e a guarda trincando"),
    "chuva-de-socos": (chuva_de_socos, "Tifa: os oito socos rápidos"),
    "tifa-preparo": (tifa_preparo, "Tifa: os punhos apertando e o chão tremendo (antes do golpe)"),
    "explosao-final": (explosao_final, "Tifa: o soco no chão e a coluna de energia"),
    "corte-sombrio": (corte_sombrio, "Sephiroth: o corte longo e as penas"),
    "sephiroth-preparo": (sephiroth_preparo, "Sephiroth: a asa abrindo e o coro (antes do golpe)"),
    "heartless-angel": (heartless_angel, "Sephiroth: o coro e a luz sendo sugada"),
    "escudo-hyliano": (escudo_hyliano, "Link: o golpe no escudo e o contra-ataque"),
    "link-preparo": (link_preparo, "Link: a espada carregando (antes do golpe)"),
    "golpe-giratorio": (golpe_giratorio, "Link: o grito, o giro e o estouro"),
    "selo-da-luz": (selo_da_luz, "Zelda: a harpa e o clarão"),
    "barreira-sagrada": (barreira_sagrada, "Zelda: os cristais e o acorde"),
    "zelda-preparo": (zelda_preparo, "Zelda: o arco de luz se formando (antes do golpe)"),
    "flecha-de-luz": (flecha_de_luz, "Zelda: a flecha, o impacto e o sino"),
}
