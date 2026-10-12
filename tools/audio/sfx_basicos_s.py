"""Sons dos ataques básicos, lote s (veja tools/vfx/familias_v2/basicos_s.py).

A espada pesada do Asta com o chiado da antimagia, a corrente e a maça da Rem, os dois cortes do Kirito, o chute
do Spike com o isqueiro, o revólver girando do Vash, o vidro e a reação do Senku, a palma suave da Hinata, as
agulhas do Jiraiya, o soco que racha o chão da Tsunade, o ofuda pegando fogo, o escudo do Steven, as manoplas
da Garnet, o "hoo-ha" do Johnny Bravo, a arma de raio do Dexter e os olhos de laser do Aku com a risada.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_k import _acerto
from sfx_basicos_l import _estrelinhas
from sfx_basicos_m import _zap
from sfx_basicos_o import _fogo, _voz
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def espada_anti_magia(rng, v):
    """A espada do Asta: o grito ("NÃO VOU DESISTIR!" em tom), o chiado áspero da antimagia e a espadada pesada."""
    x = _z(1.3)
    poe(x, _voz(rng, 0.25, 300, 380, 0.08, 3, 12), 0.0)
    n = n_de(0.4)
    poe(x, satura(passa(rosa(rng, n), 200, 3000, 2), 3) * sobe_e_some(n, 0.6, 1.3) * 0.25, 0.05)
    poe(x, _whoosh(rng, 0.3, 200, 1200, 0.85, 1.3, 0.55), 0.08)
    poe(x, baque(n_de(0.5), 70, 32, 0.18, 1.0) * 0.9, 0.3)
    poe(x, _acerto(rng, 1.0, 95), 0.3)
    return reverb(x, 0.45, 0.22)


def maca_de_rem(rng, v):
    """A maça da Rem: a corrente tilintando e zunindo no giro e o esmagamento pesado da bola de espinhos."""
    x = _z(1.3)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 800, 4000, 2) * np.abs(np.sin(2 * math.pi * 6 * _t(n))) * sobe_e_some(n, 0.8, 1.2) * 0.35, 0.0)
    poe(x, graos(rng, n, 30, 0.0, 0.38, 3000, 8000, 0.003) * 0.25, 0.0)
    poe(x, baque(n_de(0.5), 75, 35, 0.16, 1.0) * 0.9, 0.4)
    poe(x, _acerto(rng, 1.0, 95), 0.4)
    poe(x, modal(n_de(0.3), 900, rng=rng, **METAL) * env(n_de(0.3), 0.0005, 0.1) * 0.15, 0.4)
    return reverb(x, 0.45, 0.22)


def espadas_duplas(rng, v):
    """As espadas do Kirito: dois cortes metálicos rápidos, um de cada lado, e o tinido do cruzamento."""
    x = _z(1.1)
    for t0 in (0.12, 0.22):
        poe(x, _whoosh(rng, 0.12, 1200, 6000, 0.8, 1.2, 0.35), t0 - 0.06)
        poe(x, B._lamina_curta(rng, n_de(0.3), 3000) * env(n_de(0.3), 0.001, 0.1) * 0.22, t0)
    poe(x, _brilho(rng, 0.5, 2349, 0.1, METAL), 0.24)
    poe(x, _acerto(rng, 0.6, 140, 1500, 6000), 0.24)
    return reverb(x, 0.45, 0.22)


def chute_de_spike(rng, v):
    """O chute do Spike: o clique do isqueiro, o chute leve e certeiro (o "fwip" rápido) e a baforada da fumaça."""
    x = _z(1.2)
    poe(x, modal(n_de(0.08), 2400, rng=rng, **METAL) * env(n_de(0.08), 0.0005, 0.03) * 0.3, 0.0)
    poe(x, passa(rosa(rng, n_de(0.1)), 2000, 6000, 2) * env(n_de(0.1), 0.003, 0.06) * 0.2, 0.03)
    poe(x, _whoosh(rng, 0.2, 700, 3500, 0.85, 1.2, 0.45), 0.18)
    poe(x, _acerto(rng, 0.9, 120), 0.36)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 500, 2500, 2) * sobe_e_some(m, 0.4, 1.3) * 0.1, 0.6)
    return reverb(x, 0.4, 0.2)


def tiro_de_vash(rng, v):
    """O tiro do Vash: o revólver girando no dedo (o "tic-tic-tic" do tambor), o tiro certeiro e a pena caindo (o
    brilho suave)."""
    x = _z(1.3)
    for k in range(6):
        poe(x, modal(n_de(0.04), 2600, rng=rng, **METAL) * env(n_de(0.04), 0.0005, 0.012) * 0.15, 0.02 + 0.035 * k)
    m = n_de(0.35)
    poe(x, satura(baque(m, 140, 60, 0.07, 1.0) * 0.8 + passa(rosa(rng, m), 400, 9000, 2) * env(m, 0.0005, 0.05) * 1.1, 1.6) * 0.75, 0.25)
    poe(x, _acerto(rng, 0.5, 150), 0.32)
    poe(x, _brilho(rng, 0.8, 1568, 0.05, SINO), 0.5)
    return reverb(x, 0.5, 0.25)


def frasco_de_senku(rng, v):
    """O frasco do Senku: o líquido chacoalhando no voo, o vidro quebrando e a reação química fervendo em bolhas."""
    x = _z(1.4)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 400, 2000, 2) * np.abs(np.sin(2 * math.pi * 10 * _t(n))) * sobe_e_some(n, 0.6, 1.3) * 0.15, 0.0)
    poe(x, modal(n_de(0.5), 2600, rng=rng, desafina=0.04, **VIDRO) * env(n_de(0.5), 0.0005, 0.2) * 0.2 + estalo(rng, n_de(0.5), 2500, 9000, 0.008) * 0.5, 0.32)
    for k in range(10):
        m = n_de(0.06)
        poe(x, seno(varre(400 + 50 * k, 900 + 60 * k, m, 1.0), m) * env(m, 0.003, 0.05) * 0.06, 0.4 + 0.05 * k)
    s = n_de(0.6)
    poe(x, passa(rosa(rng, s), 2000, 8000, 2) * sobe_e_some(s, 0.3, 1.3) * 0.12, 0.4)
    return reverb(x, 0.45, 0.22)


def palma_gentil(rng, v):
    """A palma da Hinata: o Byakugan ativando (o tom que vibra), a palma suave e firme (o "puf" abafado) e os pontos de
    chakra fechando (os tiques leves em sequência)."""
    x = _z(1.2)
    n = n_de(0.3)
    poe(x, seno(varre(500, 700, n, 1.0) * (1 + 0.02 * np.sin(2 * math.pi * 25 * _t(n))), n) * sobe_e_some(n, 0.3, 1.3) * 0.05, 0.0)
    poe(x, passa(B._baque_seco(rng, n_de(0.2), 120, 0.05), None, 1200, 2) * 0.7 + passa(rosa(rng, n_de(0.2)), 300, 1500, 2) * env(n_de(0.2), 0.002, 0.08) * 0.3, 0.3)
    for k in range(5):
        poe(x, _brilho(rng, 0.15, 2200 + 200 * k, 0.04, CRISTAL), 0.4 + 0.06 * k)
    return reverb(x, 0.45, 0.22)


def agulhas_de_cabelo(rng, v):
    """O ataque do Jiraiya: o cabelo endurecendo (o "shhhk" de fios), as agulhas disparando juntas e o soco no fim."""
    x = _z(1.2)
    n = n_de(0.2)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.7, 1.2) * 0.3, 0.0)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.02), 2000, 8000, 0.003) * 0.35, 0.25 + 0.02 * k)
    poe(x, _whoosh(rng, 0.15, 500, 2500, 0.85, 1.3, 0.35), 0.4)
    poe(x, _acerto(rng, 1.0, 110), 0.52)
    return reverb(x, 0.4, 0.2)


def soco_de_tsunade(rng, v):
    """O soco da Tsunade: o punho descendo, o estrondo enorme e o chão se abrindo (o rasgo de pedra e os escombros)."""
    x = _z(1.5)
    poe(x, _whoosh(rng, 0.25, 250, 1200, 0.85, 1.3, 0.5), 0.08)
    poe(x, baque(n_de(0.7), 55, 25, 0.28, 1.0) * 1.0, 0.32)
    poe(x, _acerto(rng, 1.0, 85), 0.32)
    m = n_de(0.7)
    poe(x, passa(rosa(rng, m), 200, 2500, 2) * env(m, 0.003, 0.35) * 0.4 + graos(rng, m, 50, 0.0, 0.6, 400, 3000, 0.012) * 0.5, 0.33)
    return reverb(x, 0.6, 0.28)


def pergaminho_de_fogo(rng, v):
    """O pergaminho da Sailor Mars: o papel voando (o farfalhar), o selo acendendo ("Akuryō Taisan!", o sino) e o fogo
    pegando no papel."""
    x = _z(1.4)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * np.abs(np.sin(2 * math.pi * 15 * _t(n))) * sobe_e_some(n, 0.6, 1.2) * 0.2, 0.0)
    poe(x, _brilho(rng, 0.6, 880, 0.12, SINO), 0.3)
    m = n_de(0.15)
    poe(x, passa(rosa(rng, m), 100, 2500, 2) * env(m, 0.01, 0.1) * 0.4, 0.42)
    poe(x, _fogo(rng, 0.6, 0.35), 0.45)
    return reverb(x, 0.5, 0.25)


def escudo_rosa(rng, v):
    """O escudo do Steven: o escudo aparecendo (o "plim" cristalino e o tom quente que abre) e a escudada (o "bong"
    de cristal)."""
    x = _z(1.3)
    poe(x, _brilho(rng, 0.5, 1319, 0.1, CRISTAL), 0.0)
    n = n_de(0.35)
    poe(x, (seno(330, n) + seno(415, n) * 0.6) * sobe_e_some(n, 0.3, 1.3) * 0.05, 0.0)
    poe(x, _whoosh(rng, 0.2, 400, 1500, 0.8, 1.3, 0.3), 0.2)
    poe(x, modal(n_de(0.6), 440, rng=rng, **CRISTAL) * env(n_de(0.6), 0.001, 0.3) * 0.25, 0.37)
    poe(x, _acerto(rng, 0.7, 110), 0.37)
    return reverb(x, 0.5, 0.25)


def manopla_de_garnet(rng, v):
    """As manoplas da Garnet: dois socos pesados colados (o "BAM-BAM" metálico e grave)."""
    x = _z(1.2)
    for t0 in (0.25, 0.33):
        poe(x, _whoosh(rng, 0.15, 300, 1500, 0.85, 1.3, 0.35), t0 - 0.12)
        poe(x, _acerto(rng, 1.0, 90), t0)
        poe(x, modal(n_de(0.2), 600, rng=rng, **METAL) * env(n_de(0.2), 0.0005, 0.06) * 0.2, t0)
    return reverb(x, 0.4, 0.2)


def soco_de_johnny(rng, v):
    """O Johnny Bravo: o "ping" do brilho nos óculos, o "hoo-ha" convencido (o grunhido em dois tons) e o soco."""
    x = _z(1.3)
    poe(x, _brilho(rng, 0.3, 3136, 0.08, SINO), 0.0)
    poe(x, _voz(rng, 0.1, 180, 200, 0.07, 3, 8), 0.08)
    poe(x, _voz(rng, 0.12, 240, 220, 0.07, 3, 8), 0.2)
    poe(x, _whoosh(rng, 0.15, 400, 2000, 0.85, 1.3, 0.35), 0.28)
    poe(x, _acerto(rng, 1.0, 110), 0.4)
    _estrelinhas(rng, 0.46, x, 0.05)
    return reverb(x, 0.4, 0.2)


def raio_de_dexter(rng, v):
    """A arma do Dexter: a carga do aparelho (o tom que sobe com os bipes de laboratório) e o raio científico que vibra
    em zigue-zague."""
    x = _z(1.2)
    n = n_de(0.25)
    poe(x, seno(varre(400, 1600, n, 1.0), n) * sobe_e_some(n, 0.9, 1.2) * 0.06, 0.0)
    for k in range(3):
        m = n_de(0.04)
        poe(x, seno(2000 + 300 * k, m) * env(m, 0.002, 0.03) * 0.05, 0.05 + 0.06 * k)
    s = n_de(0.3)
    poe(x, seno(900 + 300 * np.sign(np.sin(2 * math.pi * 30 * _t(s))), s) * sobe_e_some(s, 0.2, 1.3) * 0.06, 0.2)
    poe(x, _zap(rng, 0.3, 0.2), 0.38)
    poe(x, _acerto(rng, 0.4, 150), 0.38)
    return reverb(x, 0.4, 0.2)


def raio_de_aku(rng, v):
    """Os olhos do Aku: as chamas das sobrancelhas, a risada grave e cavernosa e os dois lasers disparando."""
    x = _z(1.4)
    poe(x, _fogo(rng, 0.5, 0.15), 0.0)
    for k in range(3):
        poe(x, _voz(rng, 0.12, 110 - 8 * k, 95, 0.1, 4, 15), 0.0 + 0.13 * k)
    n = n_de(0.35)
    poe(x, (satura(seno(220, n), 2) * 0.4 + passa(rosa(rng, n), 1500, 7000, 2)) * sobe_e_some(n, 0.2, 1.3) * 0.25, 0.18)
    poe(x, _acerto(rng, 0.6, 120), 0.3)
    return reverb(x, 0.55, 0.28)


SONS: dict = {
    "espada-anti-magia": (espada_anti_magia, "básico do Asta: a espada e a antimagia"),
    "maca-de-rem": (maca_de_rem, "básico da Rem: a corrente e a maça"),
    "espadas-duplas": (espadas_duplas, "básico do Kirito: os dois cortes"),
    "chute-de-spike": (chute_de_spike, "básico do Spike: o isqueiro e o chute"),
    "tiro-de-vash": (tiro_de_vash, "básico do Vash: o revólver e a pena"),
    "frasco-de-senku": (frasco_de_senku, "básico do Senku: o vidro e a reação"),
    "palma-gentil": (palma_gentil, "básico da Hinata: o Byakugan e a palma"),
    "agulhas-de-cabelo": (agulhas_de_cabelo, "básico do Jiraiya: as agulhas e o soco"),
    "soco-de-tsunade": (soco_de_tsunade, "básico da Tsunade: o soco e o chão rachando"),
    "pergaminho-de-fogo": (pergaminho_de_fogo, "básico da Sailor Mars: o selo e o fogo"),
    "escudo-rosa": (escudo_rosa, "básico do Steven: o escudo de cristal"),
    "manopla-de-garnet": (manopla_de_garnet, "básico da Garnet: as manoplas"),
    "soco-de-johnny": (soco_de_johnny, "básico do Johnny Bravo: o brilho e o soco"),
    "raio-de-dexter": (raio_de_dexter, "básico do Dexter: a arma de raio"),
    "raio-de-aku": (raio_de_aku, "básico do Aku: a risada e os lasers"),
}
