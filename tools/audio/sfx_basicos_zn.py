"""Sons dos ataques básicos, lote zn (veja tools/vfx/familias_v2/basicos_zn.py).

O tapão de gorila e o chão tremendo do Donkey Kong, o estrondo supersônico do Omni-Man, o braço esticando e o "boing"
da Mulher-Elástica, o raio das trevas do Mumm-Ra, o giro do Sharingan e a kunai do Kakashi, o gelo subindo da Rukia, o
raio cósmico do Surfista Prateado, o choramingo e a mordida do Coragem, e o "bip-bip" com a poeira do Papa-Léguas.
Tudo sintetizado.
"""
from __future__ import annotations

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_f import _corte_curto
from sfx_basicos_u import _acerto, _chiado, _sopro
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def tapa_de_gorila_dk(rng, v):
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.2, 200, 1500, 0.85, g=0.5), 0.0)
    poe(x, B._tapa(rng, n_de(0.06), 600, 5000, 0.005) * 0.9, 0.2)
    poe(x, satura(baque(n_de(0.5), 70, 35, 0.2, 0.8), 2.0) * 0.6, 0.2)
    poe(x, baque(n_de(0.15), 300, 200, 0.05, 0.3) * 0.2, 0.6)
    return reverb(x, 0.4, 0.18, 6000)


def pancada_viltrumita(rng, v):
    x = _z(1.2)
    n = n_de(0.12)
    poe(x, satura(passa(rosa(rng, n), 100, 4000, 2) * env(n, 0.001, 0.08), 2.4) * 0.6, 0.06)
    poe(x, _acerto(rng, v, 1.0, 70), 0.16)
    poe(x, satura(baque(n_de(0.5), 60, 30, 0.2, 1.0), 2.4) * 0.6, 0.16)
    poe(x, graos(rng, n_de(0.3), 14, 0.0, 0.5, 300, 2500, 0.012) * 0.3, 0.2)
    return reverb(x, 0.4, 0.18, 6000)


def tapa_elastico(rng, v):
    x = _z(1.2)
    n = n_de(0.18)
    poe(x, seno(varre(200, 700, n) + 30 * np.sin(np.arange(n) / SR * 60), n) * env(n, 0.005, 0.15) * 0.12, 0.0)
    poe(x, B._tapa(rng, n_de(0.05), 1200, 7000, 0.004) * 0.7, 0.16)
    m = n_de(0.3)
    poe(x, seno(varre(500, 150, m) + 40 * np.sin(np.arange(m) / SR * 80), m) * env(m, 0.005, 0.25) * 0.12, 0.42)
    return reverb(x, 0.3, 0.14, 8000)


def raio_do_ankh(rng, v):
    x = _z(1.3)
    n = n_de(0.4)
    poe(x, (seno(110, n) + seno(117, n)) * sobe_e_some(n, 0.3, 1.2) * 0.1, 0.0)
    poe(x, _chiado(rng, 0.35, 800, 5000, 0.008, 0.45), 0.12)
    m = n_de(0.5)
    poe(x, satura(passa(rosa(rng, m), 80, 1500, 2) * sobe_e_some(m, 0.2, 1.4), 1.8) * 0.4, 0.22)
    return reverb(x, 0.6, 0.28, 5500)


def kunai_do_sharingan(rng, v):
    x = _z(1.1)
    n = n_de(0.25)
    poe(x, seno(varre(600, 1200, n), n) * sobe_e_some(n, 0.6, 1.2) * 0.05, 0.0)
    poe(x, _whoosh(rng, 0.12, 1200, 6000, 0.85, g=0.4), 0.12)
    poe(x, estalo(rng, n_de(0.04), 3000, 9000, 0.004) * 0.5, 0.26)
    poe(x, _acerto(rng, v, 0.45, 170), 0.26)
    return reverb(x, 0.3, 0.14, 8500)


def danca_da_lua_branca(rng, v):
    x = _z(1.4)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 2000, 9000, 2) * sobe_e_some(n, 0.6, 1.3) * 0.2, 0.0)
    for k in range(6):
        poe(x, modal(n_de(0.35), 2200 + 300 * k, rng=rng, **VIDRO) * env(n_de(0.35), 0.001, 0.2) * 0.05, 0.2 + 0.03 * k)
    m = n_de(0.6)
    poe(x, passa(rosa(rng, m), 500, 4000, 2) * sobe_e_some(m, 0.15, 1.5) * 0.2, 0.22)
    return reverb(x, 0.55, 0.26, 9500)


def raio_da_prancha(rng, v):
    x = _z(1.3)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 600, 6000, 2) * sobe_e_some(n, 0.5, 1.2) * 0.25, 0.0)
    m = n_de(0.3)
    poe(x, (seno(varre(1800, 900, m), m) + seno(varre(2700, 1350, m), m) * 0.4) * env(m, 0.003, 0.22) * 0.12, 0.14)
    for k, f in enumerate((2093, 2637, 3136)):
        poe(x, _brilho(rng, 0.3, f, 0.04, CRISTAL), 0.26 + 0.04 * k)
    return reverb(x, 0.55, 0.26, 9500)


def mordida_corajosa(rng, v):
    x = _z(1.1)
    n = n_de(0.3)
    poe(x, seno(varre(900, 1300, n) + 50 * np.sin(np.arange(n) / SR * 70), n) * env(n, 0.01, 0.25) * 0.06, 0.0)
    poe(x, estalo(rng, n_de(0.04), 1500, 6000, 0.006) * 0.8, 0.22)
    poe(x, _acerto(rng, v, 0.45, 160), 0.22)
    return reverb(x, 0.3, 0.14, 8000)


def poeira_do_papaleguas(rng, v):
    x = _z(1.2)
    for k in range(2):
        n = n_de(0.08)
        poe(x, seno(1300, n) * env(n, 0.005, 0.05) * 0.1, 0.0 + 0.12 * k)
    poe(x, _whoosh(rng, 0.14, 800, 6000, 0.6, g=0.45), 0.0)
    poe(x, B._tapa(rng, n_de(0.04), 1500, 7000, 0.004) * 0.5, 0.1)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 150, 1800, 2) * sobe_e_some(m, 0.1, 1.6) * 0.35, 0.12)
    return reverb(x, 0.35, 0.16, 7000)


SONS: dict = {
    "tapa-de-gorila-dk": (tapa_de_gorila_dk, "básico de Donkey Kong: o tapão de gorila e o chão tremendo"),
    "pancada-viltrumita": (pancada_viltrumita, "básico de Omni-Man: o estrondo supersônico"),
    "tapa-elastico": (tapa_elastico, "básico de Mulher-Elástica: o braço esticando e o boing"),
    "raio-do-ankh": (raio_do_ankh, "básico de Mumm-Ra: o raio das trevas do ankh"),
    "kunai-do-sharingan": (kunai_do_sharingan, "básico de Kakashi: o Sharingan e a kunai"),
    "danca-da-lua-branca": (danca_da_lua_branca, "básico de Rukia: o gelo branco subindo"),
    "raio-da-prancha": (raio_da_prancha, "básico de Surfista Prateado: o raio cósmico"),
    "mordida-corajosa": (mordida_corajosa, "básico de Coragem: o choramingo e a mordida"),
    "poeira-do-papaleguas": (poeira_do_papaleguas, "básico de Papa-Léguas: o bip-bip e a poeira"),
}
