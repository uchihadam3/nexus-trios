"""Sons dos ataques básicos, lote r (veja tools/vfx/familias_v2/basicos_r.py).

Os ossos estalando do Jack, o tentáculo molhado da Úrsula, os raios do Full Cowl, o vendaval do Detroit Smash,
os estouros do Bakugo, o gelo rompendo do Todoroki, a vibração psíquica do Mob, o jato d'água do Rimuru, o
zumbido negativo do Ainz, o Geass e o tiro do Lelouch, as cinco garras do Inuyasha, o chicote de luz do
Sesshomaru, o saque do Kenshin, o fogo do Natsu e as espadas da Erza.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_k import _acerto, _mola, _splash
from sfx_basicos_l import _estrelinhas
from sfx_basicos_m import _zap
from sfx_basicos_o import _fogo, _voz
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def mao_ossuda(rng, v):
    """A mão do Jack: os ossos estalando ao esticar (os "crec" secos de xilofone), o agarrão e o vento de
    Halloween."""
    x = _z(1.3)
    for k, f in enumerate((660, 784, 880, 988, 1175)):
        poe(x, modal(n_de(0.1), f, rng=rng, razoes=[1.0, 3.9, 9.6], quedas=[0.05, 0.02, 0.01], ganhos=[1, 0.4, 0.2]) * 0.18, 0.03 + 0.06 * k)
    poe(x, _acerto(rng, 0.6, 140), 0.4)
    n = n_de(0.7)
    poe(x, passa(rosa(rng, n), 400, 2000, 2) * sobe_e_some(n, 0.4, 1.3) * 0.12, 0.3)
    return reverb(x, 0.55, 0.28)


def tentaculo_de_ursula(rng, v):
    """O tentáculo da Úrsula: o tentáculo molhado deslizando, o chicote gosmento e a tinta esguichando."""
    x = _z(1.3)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 9 * _t(n))) * sobe_e_some(n, 0.6, 1.3) * 0.35, 0.0)
    poe(x, B._tapa(rng, n_de(0.1), 500, 3000, 0.03) * 1.1, 0.28)
    poe(x, _splash(rng, 0.3, 0.3, 150, 2000), 0.29)
    poe(x, _acerto(rng, 0.5, 110), 0.28)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 200, 1200, 2) * env(m, 0.01, 0.3) * 0.2, 0.35)
    return reverb(x, 0.5, 0.25)


def full_cowl(rng, v):
    """O Full Cowl do Deku: os raios verdes zunindo pelo corpo, o soco e o "SMASH" estourando com os estalos."""
    x = _z(1.2)
    poe(x, _zap(rng, 0.35, 0.2), 0.0)
    poe(x, _whoosh(rng, 0.2, 400, 2500, 0.85, 1.3, 0.45), 0.12)
    poe(x, _acerto(rng, 1.1, 100), 0.3)
    poe(x, _zap(rng, 0.3, 0.25), 0.32)
    return reverb(x, 0.45, 0.2)


def detroit_smash(rng, v):
    """O Detroit Smash: o soco do All Might e o vendaval enorme que ele empurra (o rugido de vento que passa)."""
    x = _z(1.5)
    poe(x, _whoosh(rng, 0.25, 300, 1800, 0.85, 1.3, 0.5), 0.05)
    poe(x, baque(n_de(0.7), 60, 28, 0.25, 1.0) * 1.0, 0.28)
    poe(x, _acerto(rng, 1.0, 85), 0.28)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 100, 3000, 2) * sobe_e_some(n, 0.15, 1.4) * 0.6, 0.3)
    return reverb(x, 0.6, 0.28)


def explosao_de_bakugo(rng, v):
    """As explosões do Bakugo: dois estouros secos e fortes das palmas, com o crepitar e o chiado depois."""
    x = _z(1.3)
    for t0 in (0.1, 0.32):
        poe(x, baque(n_de(0.4), 90, 40, 0.12, 1.0) * 0.8, t0)
        m = n_de(0.35)
        poe(x, passa(rosa(rng, m), 300, 8000, 2) * env(m, 0.001, 0.15) * 0.5, t0)
        poe(x, graos(rng, n_de(0.4), 20, 0.02, 0.35, 2000, 8000, 0.004) * 0.3, t0)
    return reverb(x, 0.45, 0.2)


def gelo_e_fogo(rng, v):
    """O gelo do Todoroki: o gelo rompendo o chão em fila (os estalos de cristal que crescem e o rangido) e a chama
    acesa um instante."""
    x = _z(1.3)
    poe(x, _fogo(rng, 0.4, 0.15), 0.0)
    for k in range(7):
        poe(x, estalo(rng, n_de(0.04), 1500, 7000, 0.008) * 0.4, 0.05 + 0.05 * k)
        poe(x, _brilho(rng, 0.3, 1800 + 200 * k, 0.04, VIDRO), 0.06 + 0.05 * k)
    poe(x, _acerto(rng, 0.6, 130), 0.38)
    return reverb(x, 0.5, 0.25)


def empurrao_psiquico(rng, v):
    """O empurrão do Mob: a vibração psíquica crescendo (o zumbido que treme e sobe) e a onda empurrando o rival."""
    x = _z(1.3)
    n = n_de(0.45)
    t = _t(n)
    poe(x, seno(varre(180, 360, n, 1.2) * (1 + 0.03 * np.sin(2 * math.pi * 22 * t)), n) * sobe_e_some(n, 0.8, 1.3) * 0.1, 0.0)
    poe(x, _whoosh(rng, 0.3, 300, 1200, 0.8, 1.3, 0.5), 0.25)
    poe(x, passa(B._baque_seco(rng, n_de(0.25), 95, 0.07), None, 1500, 2) * 0.9, 0.45)
    return reverb(x, 0.5, 0.25)


def jato_do_slime(rng, v):
    """O jato do Rimuru: o "blop" do slime, o assobio fino da água em alta pressão e o respingo."""
    x = _z(1.1)
    m = n_de(0.1)
    poe(x, seno(varre(300, 500, m, 1.0), m) * env(m, 0.004, 0.07) * 0.12, 0.0)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 4000, 11000, 2) * sobe_e_some(n, 0.15, 1.3) * 0.35, 0.18)
    poe(x, _splash(rng, 0.3, 0.35), 0.27)
    poe(x, _acerto(rng, 0.4, 150), 0.27)
    return reverb(x, 0.4, 0.2)


def raio_negativo(rng, v):
    """O raio negativo do Ainz: o círculo de magia girando (o coro grave e sombrio), o raio escuro e a vida sendo
    sugada (o som ao contrário)."""
    x = _z(1.4)
    n = n_de(0.5)
    for f in (65, 98, 131):
        poe(x, seno(f, n) * sobe_e_some(n, 0.5, 1.3) * 0.05, 0.0)
    m = n_de(0.35)
    poe(x, passa(rosa(rng, m), 200, 2500, 2) * sobe_e_some(m, 0.3, 1.3) * 0.35, 0.18)
    poe(x, _acerto(rng, 0.5, 100), 0.25)
    s = n_de(0.5)
    poe(x, passa(rosa(rng, s), 500, 3000, 2) * np.linspace(0, 1, s) ** 2 * 0.25, 0.4)
    return reverb(x, 0.6, 0.3)


def geass_tiro(rng, v):
    """O Lelouch: o Geass acendendo (o acorde agudo e frio, como um comando) e o tiro de pistola."""
    x = _z(1.2)
    n = n_de(0.35)
    for f in (880, 1319):
        poe(x, seno(f, n) * sobe_e_some(n, 0.2, 1.3) * 0.04, 0.0)
    poe(x, _brilho(rng, 0.4, 1760, 0.06, CRISTAL), 0.0)
    m = n_de(0.3)
    poe(x, satura(baque(m, 160, 70, 0.06, 1.0) * 0.8 + passa(rosa(rng, m), 500, 9000, 2) * env(m, 0.0005, 0.04), 1.6) * 0.7, 0.3)
    poe(x, _acerto(rng, 0.5, 150), 0.37)
    return reverb(x, 0.5, 0.22)


def garras_de_ferro(rng, v):
    """As garras do Inuyasha: o "Sankon Tessō!" — os cinco rasgos de energia saindo quase juntos (o "shhk" agudo)."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.2, 800, 4000, 0.8, 1.2, 0.35), 0.0)
    for k in range(5):
        n = n_de(0.1)
        poe(x, passa(rosa(rng, n), 2500, 9000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.3, 0.1 + 0.015 * k)
    poe(x, _acerto(rng, 0.7, 140, 1500, 6000), 0.15)
    return reverb(x, 0.4, 0.2)


def chicote_de_luz(rng, v):
    """O chicote de luz do Sesshomaru: o zumbido de energia esticando, o estalo agudo e o chiado do veneno."""
    x = _z(1.3)
    n = n_de(0.28)
    poe(x, seno(varre(600, 1400, n, 1.0), n) * sobe_e_some(n, 0.7, 1.3) * 0.06 + passa(rosa(rng, n), 2000, 7000, 2) * sobe_e_some(n, 0.7, 1.3) * 0.15, 0.0)
    poe(x, estalo(rng, n_de(0.04), 2500, 10000, 0.006) * 0.9, 0.25)
    poe(x, _acerto(rng, 0.5, 150, 1500, 6000), 0.26)
    m = n_de(0.6)
    poe(x, passa(rosa(rng, m), 3000, 9000, 2) * sobe_e_some(m, 0.3, 1.3) * 0.15, 0.32)
    return reverb(x, 0.5, 0.25)


def sakabato(rng, v):
    """O saque do Kenshin: o clique da bainha, o "tchiiing" do batto mais rápido que o olho e a pancada da lâmina
    virada."""
    x = _z(1.1)
    poe(x, modal(n_de(0.06), 2800, rng=rng, **METAL) * env(n_de(0.06), 0.0005, 0.02) * 0.3, 0.05)
    poe(x, _whoosh(rng, 0.1, 2000, 7000, 0.9, 1.2, 0.5), 0.12)
    poe(x, B._lamina_curta(rng, n_de(0.4), 3400) * env(n_de(0.4), 0.001, 0.15) * 0.25, 0.14)
    poe(x, _acerto(rng, 0.9, 120), 0.2)
    return reverb(x, 0.45, 0.22)


def soco_flamejante_natsu(rng, v):
    """O punho de fogo do Natsu: o fogo acendendo na mão (o "fwoomp"), o soco e a bola de fogo estourando."""
    x = _z(1.3)
    m = n_de(0.2)
    poe(x, passa(rosa(rng, m), 100, 2500, 2) * env(m, 0.01, 0.15) * 0.5, 0.0)
    poe(x, _fogo(rng, 0.45, 0.3), 0.05)
    poe(x, baque(n_de(0.5), 75, 35, 0.16, 1.0) * 0.85, 0.3)
    poe(x, _acerto(rng, 0.9, 100), 0.3)
    poe(x, _fogo(rng, 0.6, 0.35), 0.32)
    return reverb(x, 0.5, 0.22)


def espadas_de_erza(rng, v):
    """As espadas da Erza: o requip (o brilho de troca, as espadas aparecendo com os "tching" em roda) e a chuva de
    lâminas cravando juntas."""
    x = _z(1.3)
    poe(x, _brilho(rng, 0.4, 1568, 0.08, SINO), 0.0)
    for k in range(6):
        poe(x, modal(n_de(0.3), 2200 + 200 * k, rng=rng, **METAL) * env(n_de(0.3), 0.0005, 0.1) * 0.08, 0.04 + 0.03 * k)
    poe(x, _whoosh(rng, 0.2, 800, 4000, 0.85, 1.2, 0.45), 0.3)
    for k in range(4):
        poe(x, _acerto(rng, 0.5, 130 + 10 * k, 1200, 5000), 0.47 + 0.02 * k)
    return reverb(x, 0.45, 0.22)


SONS: dict = {
    "mao-ossuda": (mao_ossuda, "básico do Jack Skellington: os ossos e o agarrão"),
    "tentaculo-de-ursula": (tentaculo_de_ursula, "básico da Úrsula: o tentáculo e a tinta"),
    "full-cowl": (full_cowl, "básico do Deku: os raios e o Smash"),
    "detroit-smash": (detroit_smash, "básico do All Might: o soco e o vendaval"),
    "explosao-de-bakugo": (explosao_de_bakugo, "básico do Bakugo: os dois estouros"),
    "gelo-e-fogo": (gelo_e_fogo, "básico do Todoroki: o gelo rompendo"),
    "empurrao-psiquico": (empurrao_psiquico, "básico do Mob: a vibração e o empurrão"),
    "jato-do-slime": (jato_do_slime, "básico do Rimuru: o blop e o jato"),
    "raio-negativo": (raio_negativo, "básico do Ainz: o círculo e o raio negativo"),
    "geass-tiro": (geass_tiro, "básico do Lelouch: o Geass e o tiro"),
    "garras-de-ferro": (garras_de_ferro, "básico do Inuyasha: as cinco garras"),
    "chicote-de-luz": (chicote_de_luz, "básico do Sesshomaru: o chicote e o veneno"),
    "sakabato": (sakabato, "básico do Kenshin: o saque"),
    "soco-flamejante-natsu": (soco_flamejante_natsu, "básico do Natsu: o punho de fogo"),
    "espadas-de-erza": (espadas_de_erza, "básico da Erza: as espadas em roda"),
}
