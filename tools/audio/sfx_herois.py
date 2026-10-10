"""Os sons das habilidades do Charizard, do Mega Man, do Super-Homem e do Hyoga
(veja tools/vfx/familias_v2/charizard_megaman.py e superman_hyoga.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, nota
from som import (CRISTAL, METAL, SR, assobio, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, ruido,
                 satura, seno, serra_suave, sobe_e_some, varre)


def _t(n):
    return np.arange(n) / SR


def _fogo_rugindo(rng, seg, g=1.0, lo=150, hi=3500):
    """O rugido de um jato de fogo: ruído grave e médio que tremula, com estalinhos de brasa."""
    n = n_de(seg)
    t = _t(n)
    tremula = 0.7 + 0.3 * passa(ruido(rng, n), None, 18, 1) / 0.05
    x = passa(rosa(rng, n), lo, hi, 2) * np.clip(tremula, 0.3, 1.3)
    x += graos(rng, n, int(25 * seg), 0.0, seg, 1500, 6000, 0.004, 0.7) * 0.35
    return satura(x * 0.9, 1.4) * g


def _choque(rng, seg, g=1.0, f=95.0):
    """Zumbido elétrico com estalos (arco)."""
    n = n_de(seg)
    t = _t(n)
    z = serra_suave(f * (1 + 0.02 * np.sin(2 * math.pi * 7 * t)), n, 10) * 0.4
    z *= 0.6 + 0.4 * (passa(ruido(rng, n), None, 40, 1) > 0)
    return (z + graos(rng, n, int(40 * seg), 0.0, seg, 2000, 9000, 0.003, 0.8) * 0.5) * g


def _cristais(rng, seg, quantos, g=1.0, f0=88):
    """Tilintar de cristais de gelo."""
    x = _z(seg)
    for k in range(quantos):
        poe(x, _brilho(rng, 0.4, nota(f0 + rng.integers(-5, 8)), 0.12), rng.uniform(0, seg * 0.7))
    return x * g


def _vento_frio(rng, seg, g=1.0, f0=600, f1=2500):
    n = n_de(seg)
    return assobio(rng, n, f0, f1, 1.0, 0.35) * sobe_e_some(n, 0.4, 1.5) * g


# =================================================================== Charizard
def lanca_chamas(rng, v):
    """Lança-chamas: o "fuu" de puxar o ar, o jato de fogo rugindo um tempo e batendo no rival, com
    as brasas estalando no fim."""
    x = _z(1.7)
    poe(x, _whoosh(rng, 0.25, 900, 300, 0.6, g=0.35), 0.0)
    f = _fogo_rugindo(rng, 0.9, 0.8)
    poe(x, f * env(len(f), 0.04, 0.35, segura=0.5), 0.12)
    poe(x, B.fogo(rng, v) * 0.6, 0.55)
    poe(x, graos(rng, n_de(0.6), 14, 0.0, 0.55, 1500, 6000, 0.006, 0.6) * 0.45, 0.95)
    return reverb(x, 0.4, 0.18, 6000)


def garra_de_dragao(rng, v):
    """Garra de dragão: o rugido curto de energia, os três rasgos (cortes com fogo) e o baque."""
    x = _z(1.3)
    m = n_de(0.3)
    poe(x, serra_suave(varre(70, 110, m, 1.0), m, 8) * env(m, 0.03, 0.2) * 0.35, 0.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.16, 2500, 600, 0.3, g=0.6), 0.1 + 0.07 * k)
        poe(x, estalo(rng, n_de(0.08), 1500, 7000, 0.015) * 0.9, 0.2 + 0.07 * k)
        poe(x, _fogo_rugindo(rng, 0.2, 0.3), 0.2 + 0.07 * k)
    poe(x, baque(n_de(0.5), 110, 45, 0.15, 0.7) * 0.9, 0.22)
    return reverb(x, 0.4, 0.2, 6000)


def fogo_no_peito(rng, v):
    """O fogo juntando na boca: ronco grave subindo, o fogo sugado (ruído que cresce) e o crepitar."""
    n = n_de(1.5)
    x = passa(rosa(rng, n), 80, 1200, 2) * sobe_e_some(n, 0.85, 1.3) * 0.7
    x += seno(varre(55, 110, n, 1.0), n) * sobe_e_some(n, 0.85, 1.3) * 0.3
    poe(x, graos(rng, n, 30, 0.1, 1.4, 1500, 6000, 0.004, 0.6) * 0.35, 0.0)
    return reverb(x, 0.35, 0.18, 6000)


def explosao_de_fogo(rng, v):
    """Explosão de fogo: o "vuum" da bola saindo, o voo, o estouro enorme abrindo em cinco braços e
    as chamas rugindo até apagar."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.45, 200, 1200, 0.5, g=0.7), 0.0)
    poe(x, _fogo_rugindo(rng, 0.4, 0.4) * sobe_e_some(n_de(0.4), 0.8, 1.5), 0.05)
    poe(x, B.explosao(rng, v) * 1.1, 0.4)
    poe(x, baque(n_de(0.8), 70, 30, 0.3, 0.9) * 1.1, 0.4)
    f = _fogo_rugindo(rng, 0.9, 0.7, 100, 2500)
    poe(x, f * env(len(f), 0.02, 0.6), 0.45)
    return reverb(x, 0.55, 0.25, 5500)


# =================================================================== Mega Man
def _pew(rng, f0=1400, f1=500, seg=0.12, g=1.0):
    """O "pew" do Buster: um tom que cai rápido, com o clique da saída."""
    n = n_de(seg)
    q = (serra_suave(varre(f0, f1, n, 1.2), n, 5) * 0.5 + seno(varre(f0 * 2, f1 * 2, n, 1.2), n) * 0.2) * env(n, 0.002, seg * 0.7)
    return (q + estalo(rng, n, 3000, 9000, 0.004) * 0.3) * g


def tiro_do_buster(rng, v):
    """Mega Buster: três "pew" em fila e os três estalos pequenos no rival."""
    x = _z(1.1)
    for k in range(3):
        poe(x, _pew(rng, 1500 - 60 * k, 520, 0.12, 0.8), 0.0 + 0.1 * k)
        poe(x, estalo(rng, n_de(0.06), 1500, 6000, 0.01) * 0.8, 0.35 + 0.12 * k)
        poe(x, baque(n_de(0.15), 300, 140, 0.04, 0.6) * 0.35, 0.35 + 0.12 * k)
    return reverb(x, 0.3, 0.15, 8000)


def troca_de_arma(rng, v):
    """A troca de arma: os bipes subindo (os dados carregando) e o "tchim" da cor nova."""
    x = _z(0.9)
    for k, nn in enumerate((72, 76, 79, 84, 88)):
        m = n_de(0.05)
        poe(x, np.sign(seno(nota(nn), m)) * env(m, 0.001, 0.04) * 0.12, 0.05 * k)
    poe(x, _brilho(rng, 0.6, nota(91), 0.25, METAL), 0.3)
    return reverb(x, 0.3, 0.15, 9000)


def arma_adquirida(rng, v):
    """Arma adquirida: a esfera elétrica saindo (zumbido), o voo chiando e o estouro de raio no
    rival, que fica crepitando."""
    x = _z(1.5)
    poe(x, _pew(rng, 900, 300, 0.2, 0.6), 0.0)
    c = _choque(rng, 0.4, 0.5, 120)
    poe(x, c * sobe_e_some(len(c), 0.7, 1.4), 0.05)
    poe(x, B.raio(rng, v) * 0.9, 0.42)
    c2 = _choque(rng, 0.6, 0.4, 90)
    poe(x, c2 * env(len(c2), 0.01, 0.4), 0.55)
    return reverb(x, 0.4, 0.2, 7500)


def buster_carga(rng, v):
    """A carga do Buster: o tom subindo com o pulso cada vez mais rápido, até ficar cheio."""
    n = n_de(1.4)
    t = _t(n)
    f = varre(220, 880, n, 0.7)
    pulso = 0.6 + 0.4 * np.sin(2 * math.pi * np.cumsum(6 + 26 * (t / t[-1])) / SR)
    x = (serra_suave(f, n, 6) * 0.3 + seno(f * 2, n) * 0.1) * pulso * sobe_e_some(n, 0.9, 1.2)
    return reverb(x, 0.3, 0.15, 9000)


def carga_maxima(rng, v):
    """Carga máxima: o tiro grande saindo (um "buum" com o tom caindo), o voo e a explosão de energia
    em cada rival."""
    x = _z(1.6)
    poe(x, _pew(rng, 900, 120, 0.35, 1.0), 0.0)
    poe(x, baque(n_de(0.4), 160, 60, 0.12, 0.7) * 0.8, 0.0)
    poe(x, _whoosh(rng, 0.35, 400, 2500, 0.6, g=0.5), 0.05)
    poe(x, B.explosao(rng, v) * 0.9, 0.4)
    poe(x, _brilho(rng, 0.7, nota(84), 0.2), 0.4)
    return reverb(x, 0.5, 0.22, 7000)


# =================================================================== Super-Homem
def olhos_brilhando(rng, v):
    """Os olhos acendendo: um zumbido agudo que cresce e treme."""
    n = n_de(2.0)
    t = _t(n)
    f = varre(500, 1100, n, 0.8) * (1 + 0.01 * np.sin(2 * math.pi * 9 * t))
    x = (seno(f, n) * 0.25 + seno(f * 1.5, n) * 0.1) * sobe_e_some(n, 0.9, 1.2)
    x += passa(ruido(rng, n), 3000, 8000, 2) * sobe_e_some(n, 0.9, 1.2) * 0.05
    return reverb(x, 0.3, 0.15, 9000)


def visao_de_calor(rng, v):
    """Visão de calor: os dois raios chiando (o zumbido duplo e o ar fervendo) e o metal chiando e
    derretendo no rival."""
    x = _z(1.7)
    n = n_de(0.9)
    t = _t(n)
    z = (seno(1200 * (1 + 0.004 * np.sin(2 * math.pi * 30 * t)), n) * 0.18 + seno(1212, n) * 0.18
         + passa(ruido(rng, n), 2500, 9000, 2) * 0.2)
    poe(x, z * env(n, 0.02, 0.3, segura=0.5), 0.0)
    s = n_de(0.9)
    chiado = passa(ruido(rng, s), 1500, 7000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 13 * _t(s))) * env(s, 0.03, 0.6) * 0.55
    poe(x, chiado, 0.3)
    poe(x, graos(rng, n_de(0.6), 12, 0.0, 0.6, 1000, 5000, 0.008, 0.6) * 0.3, 0.6)
    return reverb(x, 0.4, 0.18, 7000)


def eu_te_seguro(rng, v):
    """Eu te seguro: ele chega voando (o vento forte passando), o tranco do abraço e a bolha de
    proteção fechando com um brilho."""
    x = _z(1.6)
    poe(x, _whoosh(rng, 0.5, 300, 1800, 0.75, g=0.9), 0.0)
    poe(x, baque(n_de(0.4), 130, 70, 0.1, 0.5) * 0.7, 0.32)
    poe(x, B.escudo(rng, v) * 0.7, 0.45)
    poe(x, _brilho(rng, 0.8, nota(79), 0.22), 0.5)
    return reverb(x, 0.45, 0.22, 7000)


def krypton_carga(rng, v):
    """A luz do sol juntando: um acorde que cresce, brilhante, com o vento subindo."""
    n = n_de(3.0)
    x = sum(seno(nota(nn), n) * g for nn, g in ((50, 0.12), (57, 0.1), (62, 0.08), (69, 0.06))) * sobe_e_some(n, 0.92, 1.1)
    x += assobio(rng, n, 300, 1500, 1.0, 0.4) * sobe_e_some(n, 0.9, 1.4) * 0.3
    return reverb(x, 0.5, 0.25, 8000)


def ultimo_filho_de_krypton(rng, v):
    """Último filho de Krypton: o estrondo sônico (o "crack" do ar), o soco gigante, o chão
    tremendo e os destroços caindo."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.3, 500, 3000, 0.85, g=0.7), 0.0)
    poe(x, estalo(rng, n_de(0.15), 600, 6000, 0.03) * 1.3, 0.22)
    poe(x, B.soco_pesado(rng, v) * 1.0, 0.25)
    poe(x, baque(n_de(1.0), 60, 25, 0.4, 1.0) * 1.2, 0.25)
    poe(x, B.terremoto(rng, v) * 0.6, 0.35)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.05), 400, 3000, 0.02) * 0.3, 0.8 + 0.12 * k + rng.uniform(-0.03, 0.03))
    return reverb(x, 0.6, 0.25, 5000)


# =================================================================== Hyoga
def poeira_de_diamante(rng, v):
    """Pó de Diamante: o vento gelado soprando forte e os cristais tilintando, depois o gelo
    estalando no rival."""
    x = _z(1.6)
    poe(x, _vento_frio(rng, 0.8, 0.8), 0.0)
    poe(x, _cristais(rng, 0.8, 10, 0.9), 0.05)
    poe(x, B.gelo(rng, v) * 0.7, 0.6)
    return reverb(x, 0.5, 0.25, 8000)


def aurora_preparo(rng, v):
    """Os braços juntos acima da cabeça: o acorde frio e brilhante subindo, com o vento girando."""
    n = n_de(2.3)
    t = _t(n)
    x = sum(seno(nota(nn) * (1 + 0.003 * np.sin(2 * math.pi * 0.7 * t + k)), n) * 0.08 for k, nn in enumerate((69, 74, 76, 81)))
    x = x * sobe_e_some(n, 0.9, 1.2)
    x += _vento_frio(rng, 2.3, 0.4, 400, 1500)
    poe(x, _cristais(rng, 2.0, 8, 0.6), 0.2)
    return reverb(x, 0.6, 0.3, 8000)


def execucao_aurora(rng, v):
    """Execução Aurora: o raio de frio saindo (o vento forte e o acorde), o gelo crescendo em volta
    do rival (estalos subindo) e o "tchim" quando ele fica preso."""
    x = _z(1.9)
    poe(x, _vento_frio(rng, 0.8, 1.0, 300, 2000), 0.0)
    m = n_de(0.8)
    poe(x, sum(seno(nota(nn), m) * 0.07 for nn in (64, 71, 76)) * env(m, 0.05, 0.5), 0.0)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.05), 2000, 8000, 0.01) * 0.5, 0.55 + 0.05 * k)
    poe(x, B.gelo(rng, v) * 0.8, 0.6)
    poe(x, _brilho(rng, 0.9, nota(88), 0.28, CRISTAL), 1.0)
    return reverb(x, 0.55, 0.25, 8000)


def zero_preparo(rng, v):
    """O frio girando em volta dele: vento rodando e tilintar."""
    n = n_de(2.3)
    t = _t(n)
    x = _vento_frio(rng, 2.3, 0.6, 300, 1200) * (0.7 + 0.3 * np.sin(2 * math.pi * 2 * t))
    poe(x, _cristais(rng, 2.0, 10, 0.5, 84), 0.1)
    return reverb(x, 0.6, 0.3, 7000)


def zero_absoluto(rng, v):
    """Zero Absoluto: o campo congelando — o estalo do gelo correndo pelo chão, as estacas subindo
    (uma série de estalos graves), o vento parando e o silêncio brilhante."""
    x = _z(2.2)
    s = n_de(0.6)
    poe(x, passa(ruido(rng, s), 2000, 9000, 2) * sobe_e_some(s, 0.3, 1.3) * 0.5, 0.0)
    for k in range(9):
        poe(x, estalo(rng, n_de(0.06), 1500, 7000, 0.012) * 0.7, 0.15 + 0.06 * k + rng.uniform(-0.01, 0.01))
        poe(x, baque(n_de(0.2), 200, 90, 0.05, 0.6) * 0.3, 0.15 + 0.06 * k)
    poe(x, B.gelo(rng, v) * 0.9, 0.3)
    poe(x, _cristais(rng, 1.0, 12, 0.7, 91), 0.8)
    m = n_de(1.2)
    poe(x, sum(seno(nota(nn), m) * 0.05 for nn in (76, 83, 88)) * env(m, 0.1, 0.8), 0.8)
    return reverb(x, 0.65, 0.3, 8000)


SONS: dict = {
    "lanca-chamas": (lanca_chamas, "Lança-chamas: o jato de fogo rugindo"),
    "garra-de-dragao": (garra_de_dragao, "Garra de dragão: os três rasgos com fogo"),
    "fogo-no-peito": (fogo_no_peito, "o fogo juntando na boca do Charizard"),
    "explosao-de-fogo": (explosao_de_fogo, "Explosão de fogo: a bola e o estouro enorme"),
    "tiro-do-buster": (tiro_do_buster, "Mega Buster: três tiros"),
    "troca-de-arma": (troca_de_arma, "a troca de arma do Mega Man"),
    "arma-adquirida": (arma_adquirida, "Arma adquirida: a esfera elétrica"),
    "buster-carga": (buster_carga, "a carga do Buster subindo"),
    "carga-maxima": (carga_maxima, "Carga máxima: o tiro carregado"),
    "olhos-brilhando": (olhos_brilhando, "os olhos do Super-Homem acendendo"),
    "visao-de-calor": (visao_de_calor, "Visão de calor: os raios chiando e o metal derretendo"),
    "eu-te-seguro": (eu_te_seguro, "Eu te seguro: chega voando e protege"),
    "krypton-carga": (krypton_carga, "a luz do sol juntando no Super-Homem"),
    "ultimo-filho-de-krypton": (ultimo_filho_de_krypton, "Último filho de Krypton: o soco supersônico"),
    "poeira-de-diamante": (poeira_de_diamante, "Pó de Diamante: o vento gelado e os cristais"),
    "aurora-preparo": (aurora_preparo, "os braços do Hyoga juntos acima da cabeça"),
    "execucao-aurora": (execucao_aurora, "Execução Aurora: o raio de frio e o gelo prendendo"),
    "zero-preparo": (zero_preparo, "o frio girando em volta do Hyoga"),
    "zero-absoluto": (zero_absoluto, "Zero Absoluto: o campo congelando"),
}
