"""Os sons da rodada 2: Wolverine, Batman, Thor, Doutor Estranho e Flash (veja tools/vfx/familias_v2/rodada02.py).

Cada habilidade tem o som do impacto (o nome da família); as que voam ou preparam têm o som de "antes"."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z
from som import SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, serra_suave, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _shink(rng, g=1.0, f0=2600.0):
    """O "shink" do metal raspando: o tom agudo que desliza e o chiado do aço."""
    n = n_de(0.35)
    t = _t(n)
    tom = (seno(varre(f0, f0 * 1.5, n, 1.0), n) * 0.4 + seno(varre(f0 * 2.3, f0 * 3.1, n, 1.0), n) * 0.2) * np.exp(-t * 9)
    chiado = passa(rosa(rng, n), 3000, 11000, 2) * env(n, 0.002, 0.12) * 0.5
    return (tom + chiado) * g


def _trovao(rng, seg=1.6, g=1.0):
    """O trovão: o estalo seco do raio e o ronco grave que rola e some."""
    x = _z(seg)
    poe(x, estalo(rng, n_de(0.05), 800, 9000, 0.01) * 1.2, 0.0)
    n = n_de(seg - 0.05)
    t = _t(n)
    ronco = passa(rosa(rng, n), 25, 260, 2) * np.exp(-t * 2.2) * (0.7 + 0.3 * np.sin(2 * math.pi * 3.3 * t))
    poe(x, ronco * 1.4, 0.03)
    poe(x, baque(n_de(0.7), 70, 30, 0.25, 0.6) * 0.9, 0.0)
    return x * g


def _arcos(rng, x, quantos, t0, t1, g=0.3):
    for _ in range(quantos):
        poe(x, estalo(rng, n_de(0.04), 1500, 9000, 0.008) * g * rng.uniform(0.5, 1), rng.uniform(t0, t1))


def _zumbido(rng, seg, f=80.0, g=1.0):
    n = n_de(seg)
    t = _t(n)
    z = serra_suave(f * (1 + 0.01 * np.sin(2 * math.pi * 9 * t)), n, 10) * 0.5
    z = passa(satura(z, 1.8), None, 3000, 2) * 0.6 + passa(rosa(rng, n), 3000, 9000, 2) * 0.1
    return z * g


# =================================================================== Wolverine
def garras_adamantium(rng, v):
    """As Garras de adamantium: o "snikt" das garras saindo, dois cortes rasgando e o raspar do metal."""
    x = _z(1.4)
    n = n_de(0.08)
    poe(x, estalo(rng, n, 2000, 9000, 0.006) * 0.6 + seno(3200, n) * env(n, 0.001, 0.05) * 0.2, 0.0)
    for k, t0 in enumerate((0.05, 0.22)):
        poe(x, _whoosh(rng, 0.1, 1200, 6000, 0.7, g=0.5), t0 - 0.03)
        poe(x, B.corte(rng, v) * 0.9, t0)
        poe(x, _shink(rng, 0.5, 2400 + 400 * k), t0 + 0.01)
    return reverb(x, 0.4, 0.2, 7000)


def garras_cruzadas(rng, v):
    """Na minha frente: o "snikt" das duas mãos e o "CLANG" das garras cruzando, o metal tremendo."""
    x = _z(1.5)
    for t0 in (0.0, 0.06):
        n = n_de(0.08)
        poe(x, estalo(rng, n, 2000, 9000, 0.006) * 0.5 + seno(3000, n) * env(n, 0.001, 0.05) * 0.2, t0)
    n = n_de(1.1)
    t = _t(n)
    clang = modal(n, 520, [1.0, 2.76, 5.4, 8.9], [1.6, 2.4, 3.5, 5.0], [0.5, 0.3, 0.2, 0.1], rng=rng) * (1 + 0.15 * np.sin(2 * math.pi * 6 * t))
    poe(x, clang * 0.6, 0.22)
    poe(x, estalo(rng, n_de(0.05), 1500, 7000, 0.01) * 0.8, 0.22)
    poe(x, B.escudo(rng, v) * 0.4, 0.3)
    return reverb(x, 0.45, 0.22, 6500)


def fator_de_cura(rng, v):
    """Não acabou: o chiado da carne fechando, o vapor e o coração batendo forte, e o rosnado no fim."""
    x = _z(1.9)
    n = n_de(1.0)
    chiado = passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.3, 1.5) * 0.3
    poe(x, chiado, 0.05)
    for k in range(3):
        poe(x, baque(n_de(0.2), 60, 40, 0.08, 0.2) * 0.8, 0.25 + 0.45 * k)
        poe(x, baque(n_de(0.2), 55, 38, 0.07, 0.1) * 0.5, 0.25 + 0.45 * k + 0.14)
    poe(x, B.cura(rng, v) * 0.35, 0.4)
    m = n_de(0.6)
    tt = _t(m)
    f = 85 * (1 + 0.05 * np.sin(2 * math.pi * 6 * tt))
    rosnado = (seno(f, m) * 0.3 + seno(f * 2, m) * 0.15) * (0.7 + 0.3 * rng.uniform(size=m)) * sobe_e_some(m, 0.3, 1.2)
    poe(x, passa(rosnado, 50, 900, 2) * 0.7, 1.1)
    return reverb(x, 0.4, 0.2, 5500)


# =================================================================== Batman
def visao_de_detetive(rng, v):
    """A Análise tática: o bip do visor ligando, a varredura (o tom que desce e sobe) e três bips
    de mira travando."""
    x = _z(1.4)
    n = n_de(0.08)
    poe(x, seno(1400, n) * env(n, 0.002, 0.06) * 0.25, 0.0)
    m = n_de(0.45)
    poe(x, seno(varre(600, 1100, m, 1.0), m) * sobe_e_some(m, 0.5, 1.5) * 0.08 + passa(rosa(rng, m), 3000, 8000, 2) * sobe_e_some(m, 0.5, 1.5) * 0.05, 0.05)
    for k in range(3):
        b = n_de(0.07)
        poe(x, (seno(1800 + 200 * k, b) * 0.2 + seno(3600 + 400 * k, b) * 0.05) * env(b, 0.002, 0.05), 0.3 + 0.1 * k)
    b = n_de(0.25)
    poe(x, (seno(880, b) * 0.15 + seno(1320, b) * 0.1) * env(b, 0.003, 0.2), 0.62)
    return reverb(x, 0.3, 0.15, 8000)


def batarangue_eletrico_saida(rng, v):
    """O batarangue elétrico saindo: o arremesso cortando o ar e o bip do detonador."""
    x = _z(0.6)
    poe(x, _whoosh(rng, 0.25, 800, 4000, 0.6, g=0.7), 0.0)
    for k in range(3):
        b = n_de(0.04)
        poe(x, seno(2400, b) * env(b, 0.001, 0.03) * 0.12, 0.08 + 0.1 * k)
    return reverb(x, 0.3, 0.15, 7000)


def batarangue_eletrico(rng, v):
    """O batarangue elétrico: crava com o "tchak" de metal, apita rápido e descarrega o choque."""
    x = _z(1.5)
    poe(x, estalo(rng, n_de(0.05), 1200, 7000, 0.01) * 0.9, 0.0)
    n = n_de(0.3)
    poe(x, modal(n, 1300, [1.0, 2.4, 4.1], [8, 12, 18], [0.4, 0.2, 0.1], rng=rng) * 0.4, 0.0)
    for k in range(5):
        b = n_de(0.03)
        poe(x, seno(2800, b) * env(b, 0.001, 0.02) * 0.12, 0.12 + 0.045 * k)
    poe(x, B.interrupcao(rng, v) * 0.5, 0.36)
    m = n_de(0.5)
    poe(x, _zumbido(rng, 0.5, 95, 0.6) * env(m, 0.005, 0.45), 0.36)
    _arcos(rng, x, 10, 0.36, 0.85, 0.35)
    return reverb(x, 0.4, 0.2, 7000)


def capa_de_contingencia(rng, v):
    """O Plano de contingência: a bomba de fumaça estourando ("pof" e o chiado do gás) e a capa
    abrindo com o pano estalando."""
    x = _z(1.5)
    poe(x, baque(n_de(0.3), 140, 60, 0.08, 0.5) * 0.7, 0.0)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 500, 5000, 2) * env(n, 0.01, 0.7) * 0.5, 0.0)
    m = n_de(0.25)
    pano = passa(rosa(rng, m), 300, 3000, 2) * env(m, 0.01, 0.2)
    poe(x, pano * 0.8, 0.2)
    poe(x, estalo(rng, n_de(0.06), 300, 2500, 0.02) * 0.7, 0.4)
    poe(x, B.escudo(rng, v) * 0.35, 0.42)
    return reverb(x, 0.45, 0.22, 5000)


# =================================================================== Thor
def mjolnir_lanca(rng, v):
    """O Mjolnir arremessado: o martelo girando ("vum vum vum") e o zumbido elétrico."""
    x = _z(0.8)
    n = n_de(0.6)
    t = _t(n)
    giro = passa(rosa(rng, n), 150, 1500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 11 * t) ** 2) * sobe_e_some(n, 0.3, 1.2) * 0.8
    poe(x, giro, 0.0)
    poe(x, _zumbido(rng, 0.6, 70, 0.4) * sobe_e_some(n, 0.3, 1.2), 0.0)
    _arcos(rng, x, 4, 0.05, 0.5, 0.25)
    return reverb(x, 0.35, 0.18, 6000)


def mjolnir_impacto(rng, v):
    """O Mjolnir bate: a pancada de metal pesado, o trovão estourando e os raios estalando."""
    x = _z(1.8)
    poe(x, B.soco_pesado(rng, v) * 1.0, 0.0)
    n = n_de(0.8)
    poe(x, modal(n, 180, [1.0, 2.3, 3.9], [3, 5, 8], [0.4, 0.25, 0.1], rng=rng) * 0.35, 0.0)
    poe(x, _trovao(rng, 1.5, 0.8), 0.02)
    _arcos(rng, x, 8, 0.03, 0.5, 0.35)
    poe(x, B.interrupcao(rng, v) * 0.3, 0.1)
    return reverb(x, 0.55, 0.28, 5500)


def trovao_chamado(rng, v):
    """O Thor chamando o trovão: o céu roncando, o zumbido elétrico subindo e dois raios caindo no
    martelo."""
    x = _z(1.6)
    n = n_de(1.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 25, 200, 2) * sobe_e_some(n, 0.6, 1.5) * 1.2, 0.0)
    poe(x, _zumbido(rng, 1.4, 60, 0.5) * (t / t[-1]) ** 1.5, 0.0)
    for t0 in (0.35, 0.9):
        poe(x, estalo(rng, n_de(0.06), 800, 9000, 0.012) * 0.9, t0)
        _arcos(rng, x, 4, t0, t0 + 0.2, 0.3)
    return reverb(x, 0.5, 0.25, 5500)


def tempestade_thor(rng, v):
    """A Tempestade: o vento uivando, a chuva chiando e cinco raios caindo um atrás do outro, cada
    um com o trovão."""
    x = _z(2.4)
    n = n_de(2.2)
    t = _t(n)
    vento = passa(rosa(rng, n), 200, 1800, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 0.7 * t)) * sobe_e_some(n, 0.3, 1.5) * 0.5
    chuva = graos(rng, n, 400, 0.0, 2.2, 3000, 9000, 0.003, 0.8) * sobe_e_some(n, 0.3, 1.5) * 0.15
    poe(x, vento + chuva, 0.0)
    for j in range(5):
        poe(x, _trovao(rng, 1.2, 0.55 + 0.05 * j), 0.2 + 0.11 * j * 2)
    return reverb(x, 0.6, 0.3, 5000)


def deus_do_trovao(rng, v):
    """O Deus do Trovão: o raio gigante rasgando o céu (o "KRAK" e o chiado longo), o chão estourando
    e o choque que prende o rival estalando."""
    x = _z(2.2)
    poe(x, estalo(rng, n_de(0.08), 500, 10000, 0.02) * 1.5, 0.0)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 2000, 10000, 2) * env(n, 0.002, 0.45) * 0.6, 0.0)
    poe(x, B.explosao(rng, v) * 0.8, 0.08)
    poe(x, _trovao(rng, 2.0, 1.0), 0.02)
    m = n_de(1.0)
    poe(x, _zumbido(rng, 1.0, 110, 0.45) * env(m, 0.01, 0.9), 0.35)
    _arcos(rng, x, 12, 0.35, 1.3, 0.3)
    return reverb(x, 0.6, 0.3, 5500)


# =================================================================== Doutor Estranho
def escudo_serafim(rng, v):
    """O Escudo de Serafim: o acorde místico abrindo, as runas tilintando em volta e o zumbido do
    escudo firmando."""
    x = _z(1.8)
    n = n_de(1.5)
    for f, g in ((220, 0.12), (330, 0.09), (440, 0.07), (660, 0.04)):
        poe(x, seno(f * (1 + 0.003 * np.sin(2 * math.pi * 5 * _t(n))), n) * sobe_e_some(n, 0.25, 1.4) * g, 0.0)
    for k in range(8):
        poe(x, _brilho(rng, 0.4, 1200 + 180 * k, 0.08), 0.1 + 0.07 * k)
    poe(x, B.escudo(rng, v) * 0.5, 0.25)
    return reverb(x, 0.6, 0.3, 7000)


def laco_temporal(rng, v):
    """O Laço temporal: o tique-taque correndo para trás (cada vez mais rápido), o zumbido verde que
    sobe e desce e o golpe cortado."""
    x = _z(1.8)
    tq = 0.0
    passo = 0.14
    k = 0
    while tq < 1.0:
        b = n_de(0.03)
        poe(x, (seno(2000 if k % 2 else 1500, b) * 0.15 + estalo(rng, b, 3000, 8000, 0.003) * 0.15) * env(b, 0.001, 0.02), tq)
        tq += passo
        passo *= 0.88
        k += 1
    n = n_de(1.3)
    t = _t(n)
    poe(x, seno(varre(500, 250, n, 1.0) * (1 + 0.03 * np.sin(2 * math.pi * 4 * t)), n) * sobe_e_some(n, 0.4, 1.5) * 0.1, 0.0)
    poe(x, B.interrupcao(rng, v) * 0.45, 0.45)
    return reverb(x, 0.6, 0.3, 6500)


def portal_estranho(rng, v):
    """O portal de faíscas: o chiado das fagulhas girando (como um esmeril), o "vuum" do portal abrindo
    e as faíscas estalando."""
    x = _z(1.7)
    n = n_de(1.3)
    t = _t(n)
    esmeril = passa(rosa(rng, n), 2500, 9000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 18 * t)) * sobe_e_some(n, 0.2, 1.5) * 0.35
    poe(x, esmeril, 0.0)
    poe(x, seno(varre(90, 160, n, 1.0), n) * sobe_e_some(n, 0.25, 1.5) * 0.18, 0.0)
    poe(x, _whoosh(rng, 0.3, 300, 1800, 0.5, g=0.6), 0.05)
    _arcos(rng, x, 14, 0.05, 1.2, 0.18)
    return reverb(x, 0.5, 0.25, 6500)


# =================================================================== Flash
def mil_golpes_flash(rng, v):
    """Mil golpes: uma rajada de socos tão rápida que vira um "trrrr", os estalos de raio e o último
    soco forte."""
    x = _z(1.5)
    for k in range(14):
        poe(x, B.soco_pesado(rng, v) * 0.32 * rng.uniform(0.7, 1), 0.03 * k + rng.uniform(0, 0.01))
    _arcos(rng, x, 10, 0.0, 0.45, 0.25)
    poe(x, _whoosh(rng, 0.12, 800, 5000, 0.8, g=0.5), 0.36)
    poe(x, B.soco_pesado(rng, v) * 1.0, 0.45)
    return reverb(x, 0.4, 0.2, 6500)


def resgate_flash(rng, v):
    """O Resgate instantâneo: o "zuuum" do vulto dando a volta (passando de um lado ao outro), o
    estalo do raio e o zumbido do escudo elétrico."""
    x = _z(1.4)
    n = n_de(0.4)
    t = _t(n)
    voa = passa(rosa(rng, n), 600, 6000, 2) * sobe_e_some(n, 0.5, 1.5) * 0.6
    poe(x, voa + seno(varre(300, 900, n, 1.0), n) * sobe_e_some(n, 0.5, 1.5) * 0.06, 0.0)
    _arcos(rng, x, 5, 0.05, 0.4, 0.25)
    poe(x, B.escudo(rng, v) * 0.45, 0.35)
    m = n_de(0.7)
    poe(x, _zumbido(rng, 0.7, 120, 0.25) * env(m, 0.01, 0.6), 0.35)
    _ = t
    return reverb(x, 0.4, 0.2, 7000)


def forca_de_aceleracao(rng, v):
    """Além do tempo: o zumbido da Força de Aceleração subindo de tom, os raios estalando em volta e
    o "fuuu" de vento que corre em círculo."""
    x = _z(1.8)
    n = n_de(1.5)
    t = _t(n)
    poe(x, seno(varre(150, 600, n, 1.3), n) * sobe_e_some(n, 0.6, 1.3) * 0.08, 0.0)
    poe(x, _zumbido(rng, 1.5, 100, 0.35) * sobe_e_some(n, 0.5, 1.3), 0.0)
    vento = passa(rosa(rng, n), 400, 4000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.4, 1.3) * 0.4
    poe(x, vento, 0.0)
    _arcos(rng, x, 14, 0.05, 1.4, 0.25)
    return reverb(x, 0.45, 0.22, 6500)


SONS: dict = {
    "garras-adamantium": (garras_adamantium, "Garras de adamantium: o snikt e os dois cortes"),
    "garras-cruzadas": (garras_cruzadas, "Na minha frente: as garras cruzando com o clang"),
    "fator-de-cura": (fator_de_cura, "Não acabou: a carne fechando e o coração"),
    "visao-de-detetive": (visao_de_detetive, "Análise tática: o visor e as miras travando"),
    "batarangue-eletrico-saida": (batarangue_eletrico_saida, "Batarangue: o arremesso e o bip"),
    "batarangue-eletrico": (batarangue_eletrico, "Batarangue: crava e descarrega o choque"),
    "capa-de-contingencia": (capa_de_contingencia, "Plano de contingência: a fumaça e a capa"),
    "mjolnir-lanca": (mjolnir_lanca, "Mjolnir: o martelo girando no ar"),
    "mjolnir-impacto": (mjolnir_impacto, "Mjolnir: a pancada e o trovão"),
    "trovao-chamado": (trovao_chamado, "Thor chamando o trovão (Preparo)"),
    "tempestade-thor": (tempestade_thor, "Tempestade: o vento, a chuva e os raios"),
    "deus-do-trovao": (deus_do_trovao, "Deus do Trovão: o raio gigante"),
    "escudo-serafim": (escudo_serafim, "Escudo de Serafim: o acorde e as runas"),
    "laco-temporal": (laco_temporal, "Laço temporal: o tique-taque voltando"),
    "portal-estranho": (portal_estranho, "Portais: as faíscas girando"),
    "mil-golpes-flash": (mil_golpes_flash, "Mil golpes: a rajada de socos"),
    "resgate-flash": (resgate_flash, "Resgate instantâneo: o vulto e o escudo elétrico"),
    "forca-de-aceleracao": (forca_de_aceleracao, "Além do tempo: a Força de Aceleração"),
}
