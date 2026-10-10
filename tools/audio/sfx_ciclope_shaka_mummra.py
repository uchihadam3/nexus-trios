"""Os sons do Ciclope, do Shaka de Virgem e do Mumm-Ra (veja tools/vfx/familias_v2/ciclope_shaka_mummra.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, nota
from som import (CRISTAL, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, ruido, satura, seno,
                 serra_suave, sobe_e_some, varre)


def _t(n):
    return np.arange(n) / SR


def _raio_optico(rng, seg, g=1.0, f=180.0):
    """O raio do Ciclope: um zumbido grosso e quente (dente-de-serra grave) com o chiado do ar
    queimando por cima."""
    n = n_de(seg)
    t = _t(n)
    z = serra_suave(f * (1 + 0.01 * np.sin(2 * math.pi * 11 * t)), n, 14) * 0.35 + seno(f * 2, n) * 0.1
    ch = passa(ruido(rng, n), 2500, 9000, 2) * 0.18
    return satura(passa(z, 60, 4000, 2) + ch, 1.4) * g


def _coro_dourado(rng, seg, g=1.0, base=50):
    """Um coro sagrado: vozes graves e quentes em quinta, crescendo devagar."""
    n = n_de(seg)
    t = _t(n)
    x = sum(seno(nota(nn) * (1 + 0.003 * np.sin(2 * math.pi * 0.6 * t + k)), n) * gg for k, (nn, gg) in enumerate(((base, 0.12), (base + 7, 0.1), (base + 12, 0.08), (base + 19, 0.05))))
    return x * sobe_e_some(n, 0.85, 1.2) * g


def _sino_tibetano(rng, seg, f0, g=1.0):
    """O gongo do templo: um modal metálico grave que soa longo e oscila."""
    n = n_de(seg)
    t = _t(n)
    return modal(n, f0, rng=rng, **CRISTAL) * env(n, 0.002, seg * 0.7) * (0.85 + 0.15 * np.sin(2 * math.pi * 3 * t)) * g


def _vozes_mortas(rng, seg, g=1.0):
    """Um lamento grave e rouco (vozes de múmia): ruído em vogais oscilando."""
    n = n_de(seg)
    t = _t(n)
    b = rosa(rng, n)
    v = passa(b, 300, 600, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 0.7 * t)) + passa(b, 800, 1100, 2) * 0.5 * (0.6 + 0.4 * np.sin(2 * math.pi * 1.1 * t + 1))
    return v * sobe_e_some(n, 0.5, 1.5) * g


# =================================================================== Ciclope
def rajada_de_contencao(rng, v):
    """Rajada de contenção: o visor abrindo, o raio grosso varrendo a fileira (o zumbido que corre de
    um lado ao outro) e o estalo das faíscas onde ele passa."""
    x = _z(1.5)
    poe(x, estalo(rng, n_de(0.06), 1500, 6000, 0.01) * 0.6, 0.0)
    r = _raio_optico(rng, 0.8, 0.9, 170)
    poe(x, r * env(len(r), 0.02, 0.4, segura=0.4), 0.03)
    poe(x, graos(rng, n_de(0.7), 24, 0.0, 0.65, 1500, 7000, 0.004, 0.7) * 0.4, 0.1)
    return reverb(x, 0.4, 0.2, 6000)


def ricochete_optico(rng, v):
    """Ricochete óptico: o raio batendo e quicando — três golpes do raio, cada um com o seu estalo e
    um tom subindo."""
    x = _z(1.5)
    for k in range(4):
        r = _raio_optico(rng, 0.14, 0.7, 170 + 25 * k)
        poe(x, r * env(len(r), 0.005, 0.1), 0.1 * k)
        poe(x, estalo(rng, n_de(0.06), 1500, 7000, 0.012) * 0.8, 0.1 * k + 0.12)
        poe(x, baque(n_de(0.25), 180, 90, 0.06, 0.6) * 0.4, 0.1 * k + 0.12)
    return reverb(x, 0.4, 0.2, 6500)


def visor_carregando(rng, v):
    """O visor carregando: o zumbido do raio crescendo atrás do visor, pulsando."""
    n = n_de(1.3)
    t = _t(n)
    r = _raio_optico(rng, 1.3, 0.6, 120) * (0.6 + 0.4 * np.sin(2 * math.pi * (4 + 6 * t / t[-1]) * t)) * sobe_e_some(n, 0.9, 1.3)
    return reverb(r, 0.35, 0.18, 6000)


def feixe_concentrado(rng, v):
    """Feixe concentrado: o raio grosso saindo de uma vez (o "VRUUM"), o impacto empurrando e o corte
    seco do golpe interrompido."""
    x = _z(1.6)
    r = _raio_optico(rng, 0.7, 1.1, 140)
    poe(x, r * env(len(r), 0.01, 0.3, segura=0.4), 0.0)
    poe(x, B.explosao(rng, v) * 0.6, 0.35)
    poe(x, baque(n_de(0.5), 100, 40, 0.15, 0.8) * 0.9, 0.35)
    poe(x, B.interrupcao(rng, v) * 0.6, 0.6)
    return reverb(x, 0.45, 0.2, 6000)


# =================================================================== Shaka
def tesouro_do_ceu(rng, v):
    """Tesouro do Céu: o gongo do templo, o lótus abrindo (o coro), e cinco toques que somem um a um
    — os sentidos se apagando."""
    x = _z(2.1)
    poe(x, _sino_tibetano(rng, 1.8, nota(38), 0.5), 0.0)
    poe(x, _coro_dourado(rng, 1.4, 0.6, 52), 0.1)
    for k, nn in enumerate((79, 76, 72, 69, 64)):
        poe(x, _brilho(rng, 0.5, nota(nn), 0.16 * (1 - 0.12 * k)), 0.45 + 0.1 * k)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 200, 1200, 2) * env(m, 0.05, 0.4) * 0.15, 1.05)
    return reverb(x, 0.7, 0.35, 6000)


def todo_poderoso(rng, v):
    """Todo-poderoso: a esfera dourada fechando (um zumbido que sobe e trava) com o coro e o gongo
    curto."""
    x = _z(1.6)
    m = n_de(0.6)
    poe(x, (seno(varre(110, 330, m, 1.2), m) * 0.2 + seno(varre(165, 495, m, 1.2), m) * 0.1) * sobe_e_some(m, 0.85, 1.3), 0.0)
    poe(x, B.escudo(rng, v) * 0.6, 0.55)
    poe(x, _sino_tibetano(rng, 1.0, nota(50), 0.3), 0.55)
    poe(x, _coro_dourado(rng, 1.0, 0.3, 57), 0.5)
    return reverb(x, 0.6, 0.3, 6500)


def lotus_shaka(rng, v):
    """A meditação do Preparo: o coro grave sagrado crescendo, um gongo no início e o ar parado."""
    n = n_de(2.6)
    x = _coro_dourado(rng, 2.6, 0.9, 45)
    poe(x, _sino_tibetano(rng, 2.0, nota(33), 0.4), 0.0)
    x += passa(rosa(rng, n), 100, 600, 2) * sobe_e_some(n, 0.9, 1.3) * 0.06
    return reverb(x, 0.75, 0.35, 5500)


def seis_mundos(rng, v):
    """Rendição dos Seis Mundos: seis gongos rodando (um por portal), o vento sendo puxado para o
    centro e o estrondo quando tudo fecha."""
    x = _z(2.4)
    for k in range(6):
        poe(x, _sino_tibetano(rng, 0.8, nota(38 + 2 * k), 0.25), 0.08 * k)
    m = n_de(1.0)
    puxa = passa(rosa(rng, m), 100, 2000, 2) * np.linspace(0.1, 1, m) ** 2
    poe(x, puxa * 0.7, 0.9)
    poe(x, B.explosao(rng, v) * 0.8, 1.9)
    poe(x, baque(n_de(0.8), 60, 25, 0.35, 0.9) * 1.1, 1.9)
    return reverb(x, 0.7, 0.32, 5500)


# =================================================================== Mumm-Ra
def antigos_espiritos(rng, v):
    """Antigos Espíritos: os quatro espíritos gemendo e uivando enquanto voam (vozes que sobem e
    descem), e o impacto escuro."""
    x = _z(1.6)
    for k in range(4):
        m = n_de(0.5)
        f0 = rng.uniform(300, 450)
        uivo = seno(varre(f0, f0 * 0.6, m, 1.0) * (1 + 0.04 * np.sin(2 * math.pi * 6 * _t(m))), m) * 0.1
        poe(x, (uivo + _vozes_mortas(rng, 0.5, 0.3)) * env(m, 0.08, 0.35), 0.07 * k)
    poe(x, B.sombra(rng, v) * 0.8, 0.45)
    poe(x, baque(n_de(0.5), 80, 35, 0.16, 0.7) * 0.8, 0.45)
    return reverb(x, 0.6, 0.3, 4500)


def forma_desperta(rng, v):
    """Forma desperta: o grito rouco do Mumm-Ra ("as forças do mal…"), as faixas rasgando, o trovão
    vermelho e a aura subindo."""
    x = _z(1.9)
    m = n_de(0.9)
    t = _t(m)
    f = 90 + 40 * np.sin(math.pi * t / t[-1])
    grito = satura((passa(serra_suave(f, m, 20), 300, 900, 2) + passa(ruido(rng, m), 400, 3000, 2) * 0.5) * sobe_e_some(m, 0.4, 1.3), 2.0) * 0.6
    poe(x, grito, 0.0)
    for k in range(6):
        poe(x, passa(ruido(rng, n_de(0.12)), 1500, 6000, 2) * env(n_de(0.12), 0.002, 0.08) * 0.4, 0.2 + 0.08 * k)
    poe(x, B.raio(rng, v) * 0.5, 0.5)
    poe(x, B.transformacao(rng, v) * 0.5, 0.7)
    return reverb(x, 0.6, 0.3, 4500)


def sarcofago_preparo(rng, v):
    """Os hieróglifos acendendo: o lamento das vozes mortas, um ronco grave de pedra e o vento de
    tumba."""
    n = n_de(2.0)
    x = _vozes_mortas(rng, 2.0, 0.6)
    x += passa(rosa(rng, n), 30, 150, 2) * sobe_e_some(n, 0.8, 1.3) * 0.5
    return reverb(x, 0.7, 0.32, 4000)


def retorno_ao_sarcofago(rng, v):
    """Retorno ao sarcófago: a pedra pesada subindo do chão (ronco e cascalho), o rangido da tampa, o
    lamento e o baque surdo quando a escuridão fecha."""
    x = _z(2.3)
    m = n_de(0.9)
    poe(x, satura(passa(rosa(rng, m), 30, 300, 2) * np.linspace(0.2, 1, m), 1.6) * 0.8, 0.0)
    poe(x, graos(rng, m, 30, 0.0, 0.85, 300, 2500, 0.01, 0.6) * 0.4, 0.0)
    r = n_de(0.6)
    rangido = passa(serra_suave(varre(70, 55, r, 1.0) * (1 + 0.15 * np.sin(2 * math.pi * 23 * _t(r))), r, 16), 200, 2000, 2) * env(r, 0.05, 0.5) * 0.3
    poe(x, rangido, 0.8)
    poe(x, _vozes_mortas(rng, 1.0, 0.4), 0.9)
    poe(x, baque(n_de(0.9), 50, 22, 0.4, 0.8) * 1.3, 1.6)
    poe(x, B.sombra(rng, v) * 0.6, 1.6)
    return reverb(x, 0.7, 0.32, 4000)


SONS: dict = {
    "rajada-de-contencao": (rajada_de_contencao, "Rajada de contenção: o raio varrendo a fileira"),
    "ricochete-optico": (ricochete_optico, "Ricochete óptico: o raio quicando"),
    "visor-carregando": (visor_carregando, "o visor do Ciclope carregando"),
    "feixe-concentrado": (feixe_concentrado, "Feixe concentrado: o raio grosso e o golpe cortado"),
    "tesouro-do-ceu": (tesouro_do_ceu, "Tesouro do Céu: o gongo e os sentidos se apagando"),
    "todo-poderoso": (todo_poderoso, "Todo-poderoso: a esfera dourada fechando"),
    "lotus-shaka": (lotus_shaka, "a meditação do Shaka no Preparo"),
    "seis-mundos": (seis_mundos, "Rendição dos Seis Mundos: os seis portais"),
    "antigos-espiritos": (antigos_espiritos, "Antigos Espíritos: os espíritos uivando"),
    "forma-desperta": (forma_desperta, "Forma desperta: o grito e as faixas rasgando"),
    "sarcofago-preparo": (sarcofago_preparo, "os hieróglifos acendendo"),
    "retorno-ao-sarcofago": (retorno_ao_sarcofago, "Retorno ao sarcófago: a pedra e a escuridão"),
}
