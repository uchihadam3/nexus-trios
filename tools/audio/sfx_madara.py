"""Os sons das três técnicas do Madara (veja tools/vfx/familias_v2/madara.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _tom, _whoosh, _z, nota  # noqa: F401
from som import (CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, graos, modal, n_de, passa, poe,  # noqa: F401
                 reverb, rosa, ruido, satura, seno, sobe_e_some, varre)


def _drone(n, f, grave=0.5):
    """Um zumbido grave com batimento lento (duas senoides quase iguais) — o chakra pesado."""
    t = np.arange(n) / SR
    return (seno(f, n) + 0.8 * seno(f * 1.006, n) + grave * 0.6 * seno(f / 2, n)) * (0.7 + 0.3 * np.sin(2 * math.pi * 0.8 * t))


def susanoo_perfeito(rng, v):
    """Susanoo Perfeito: o chakra acende num rugido grave que cresce, a espada gigante corta o ar
    num sopro enorme, o impacto pesado com estalo, e as chamas de chakra crepitando no fim."""
    x = _z(1.6)
    n = n_de(0.55)
    poe(x, satura(_drone(n, 55) * 0.5, 1.6) * sobe_e_some(n, 0.9, 1.5) * 0.35, 0.0)
    poe(x, passa(rosa(rng, n), 60, 600, 2) * sobe_e_some(n, 0.9, 1.6) * 0.25, 0.0)
    poe(x, _whoosh(rng, 0.35, 150, 2600, 0.8, g=0.9), 0.3)
    poe(x, B.soco_pesado(rng, v) * 1.1, 0.6)
    poe(x, baque(n_de(0.7), 70, 28, 0.3, 0.7) * 0.9, 0.6)
    poe(x, estalo(rng, n_de(0.12), 1200, 7000, 0.02) * 0.5, 0.6)
    poe(x, B.fogo(rng, v)[: n_de(0.8)] * 0.45, 0.66)
    return reverb(x, 0.55, 0.25, 5000)


def susanoo_manto(rng, v):
    """O Susanoo se forma em volta do Madara: chamas de chakra acendendo de baixo para cima, um
    rugido grave e o estalo da armadura se fechando."""
    x = _z(1.2)
    n = n_de(0.9)
    fogo = B.fogo(rng, v)[:n]
    poe(x, fogo * sobe_e_some(len(fogo), 0.6, 1.2) * 0.6, 0.0)
    poe(x, satura(_drone(n, 49, 0.8) * 0.5, 1.4) * sobe_e_some(n, 0.7, 1.4) * 0.35, 0.0)
    poe(x, modal(n_de(0.4), nota(43), rng=rng, **METAL) * env(n_de(0.4), 0.002, 0.15) * 0.18, 0.62)
    poe(x, baque(n_de(0.3), 90, 50, 0.1, 0.4) * 0.5, 0.62)
    return reverb(x, 0.5, 0.25, 5000)


def meteoro_madara(rng, v):
    """Meteoro: um ronco grave que cresce enquanto a rocha desce, o assobio do ar rasgado caindo
    de tom, a explosão enorme no chão e as pedras e a poeira chovendo depois."""
    x = _z(2.0)
    n = n_de(0.85)
    poe(x, passa(rosa(rng, n), 30, 300, 2) * np.linspace(0.1, 1, n) ** 1.6 * 0.55, 0.0)
    poe(x, assobio(rng, n, 3500, 500, 1.2, 0.3) * np.linspace(0.2, 1, n) ** 2 * 0.4, 0.0)
    poe(x, B.explosao(rng, v) * 1.25, 0.82)
    poe(x, baque(n_de(1.0), 55, 22, 0.5, 0.8) * 1.0, 0.82)
    poe(x, graos(rng, n_de(0.9), 30, 0.05, 0.85, 300, 3500, 0.01, 0.7) * 0.35, 0.95)
    return reverb(x, 0.7, 0.3, 4500)


def mugen_tsukuyomi(rng, v):
    """Mugen Tsukuyomi: um tom que sobe devagar e fica estranho (desafinado), o pulso do olho
    batendo como coração, três raios que descem em brilho, e as raízes rangendo no fim."""
    x = _z(2.1)
    n = n_de(1.0)
    poe(x, seno(varre(110, 220, n, 0.7), n) * sobe_e_some(n, 0.85, 1.4) * 0.22, 0.0)
    poe(x, seno(varre(116, 233, n, 0.7), n) * sobe_e_some(n, 0.85, 1.4) * 0.18, 0.0)
    for k in range(4):
        poe(x, baque(n_de(0.25), 70, 45, 0.08, 0.3) * 0.45, 0.35 + 0.18 * k)
    for i in range(3):
        poe(x, _brilho(rng, 0.7, nota(76 + 3 * i), 0.14, VIDRO), 0.95 + 0.07 * i)
        poe(x, _whoosh(rng, 0.25, 4000, 900, 0.6, g=0.2), 0.92 + 0.07 * i)
    n2 = n_de(0.7)
    poe(x, passa(ruido(rng, n2), 200, 1500, 2) * (0.5 + 0.5 * np.sin(np.arange(n2) / SR * 2 * math.pi * 9)) * sobe_e_some(n2, 0.4, 1.3) * 0.18, 1.25)
    return reverb(x, 0.75, 0.35, 6000)


SONS: dict = {
    "susanoo-perfeito": (susanoo_perfeito, "Susanoo Perfeito do Madara: o chakra que ruge, o corte gigante e as chamas"),
    "susanoo-manto": (susanoo_manto, "o Susanoo se formando em volta do Madara"),
    "meteoro-madara": (meteoro_madara, "Meteoro do Madara: o ronco da queda, a explosão e as pedras chovendo"),
    "mugen-tsukuyomi": (mugen_tsukuyomi, "Mugen Tsukuyomi: o tom estranho que sobe, o pulso do olho e os raios"),
}
