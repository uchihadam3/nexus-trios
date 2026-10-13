"""Sons dos ataques básicos, lote u (veja tools/vfx/familias_v2/basicos_u.py).

Cada soco soa do personagem: o ki dourado chiando e a onda de ar do Goku, o estalo azul e o soco seco do Vegeta,
o "puf" de fumaça do Naruto, o zumbido que trava no Infinito do Gojo, os três tapas rápidos e o trovão do Flash,
o servo e o "clang" da manopla do Homem de Ferro, o soco grave e o brilho das Joias do Thanos e o soco limpo
com o eco de ar do Gohan. Tudo sintetizado.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, varre


def _t(n):
    return np.arange(n) / SR


def _acerto(rng, v, g=1.0, f=110):
    """O contato do soco: o tapa, o corpo e o peso (muda um pouco a cada versão)."""
    x = _z(0.3)
    poe(x, B.soco_leve(rng, v) * 0.7 * g, 0.0)
    poe(x, B.soco_pesado(rng, v) * 0.45 * g, 0.0)
    poe(x, baque(n_de(0.2), f - 6 * v, f * 0.5, 0.05, 0.5) * 0.5 * g, 0.0)
    return x


def _chiado(rng, seg, lo=1500, hi=9000, taxa=0.006, g=0.6):
    """Crepitar de energia: pulsos curtíssimos aleatórios."""
    n = n_de(seg)
    z = np.zeros(n)
    k = 0
    while k < n:
        larg = max(1, int(rng.uniform(0.0003, 0.0012) * SR))
        z[k:k + larg] += rng.choice([-1, 1]) * rng.uniform(0.4, 1)
        k += max(8, int(rng.exponential(taxa) * SR))
    return passa(z, lo, hi, 2) * env(n, 0.01, seg * 0.6) * g


def _sopro(rng, seg, lo, hi, g):
    n = n_de(seg)
    return passa(rosa(rng, n), lo, hi, 2) * env(n, 0.004, seg * 0.6) * g


def soco_saiyajin(rng, v):
    """Goku: o ki dourado chia em volta do punho, o soco entra e a onda de ar sopra a poeira."""
    x = _z(0.95)
    poe(x, _chiado(rng, 0.2, 2000, 9000, 0.004, 0.35), 0.0)
    poe(x, _whoosh(rng, 0.14, 500, 3600, 0.85, g=0.5), 0.0)
    poe(x, _acerto(rng, v, 1.0, 120), 0.14)
    poe(x, _sopro(rng, 0.45, 200, 1800, 0.35), 0.16)
    return reverb(x, 0.3, 0.14, 6000)


def soco_do_principe(rng, v):
    """Vegeta: estalos azuis de ki secos e um soco duro, curto e estalado."""
    x = _z(0.85)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.03), 3000, 10000, 0.004) * 0.35, 0.02 + 0.04 * k)
    poe(x, _whoosh(rng, 0.11, 700, 4200, 0.85, g=0.45), 0.01)
    poe(x, _acerto(rng, v, 1.05, 130), 0.12)
    poe(x, estalo(rng, n_de(0.05), 1800, 7000, 0.006) * 0.5, 0.12)
    poe(x, _chiado(rng, 0.25, 2500, 10000, 0.005, 0.25), 0.14)
    return reverb(x, 0.22, 0.1, 6500)


def soco_do_naruto(rng, v):
    """Naruto: soco de briga, o giro da espiral (um "fuuu" que gira) e o "puf" da fumaça."""
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.14, 450, 3000, 0.85, g=0.5), 0.0)
    poe(x, _acerto(rng, v, 0.95, 115), 0.14)
    n = n_de(0.35)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 600, 3000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 14 * t)) * env(n, 0.03, 0.2) * 0.3, 0.15)
    poe(x, _sopro(rng, 0.3, 250, 2500, 0.55), 0.3)
    poe(x, baque(n_de(0.15), 160, 90, 0.04, 0.4) * 0.3, 0.3)
    return reverb(x, 0.25, 0.12, 6000)


def soco_infinito(rng, v):
    """Gojo: o soco vem, o ar trava num zumbido que desce (o Infinito) e a pancada entra de uma vez, limpa."""
    x = _z(1.15)
    poe(x, _whoosh(rng, 0.12, 600, 3400, 0.6, g=0.45), 0.0)
    n = n_de(0.3)
    t = _t(n)
    zum = seno(varre(520, 180, n, 1.5), n) * (0.7 + 0.3 * np.sin(2 * math.pi * 30 * t))
    poe(x, zum * env(n, 0.03, 0.22) * 0.12, 0.11)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * env(n, 0.02, 0.25) * 0.08, 0.11)
    poe(x, _acerto(rng, v, 1.0, 140), 0.31)
    poe(x, _brilho(rng, 0.4, 1760, 0.05, CRISTAL), 0.31)
    return reverb(x, 0.3, 0.15, 7000)


def soco_veloz_flash(rng, v):
    """Flash: o zunido de quem chega antes do som, três tapas grudados e o estalo de trovão."""
    x = _z(0.9)
    poe(x, _whoosh(rng, 0.08, 1500, 8000, 0.7, g=0.5), 0.0)
    for k in range(3):
        poe(x, B.soco_leve(rng, (v + k) % 4) * (0.45 + 0.15 * k), 0.07 + 0.035 * k)
    poe(x, _chiado(rng, 0.3, 2500, 11000, 0.003, 0.45), 0.08)
    poe(x, estalo(rng, n_de(0.06), 1200, 9000, 0.008) * 0.6, 0.16)
    poe(x, baque(n_de(0.2), 110, 55, 0.05, 0.5) * 0.4, 0.16)
    return reverb(x, 0.25, 0.12, 7000)


def soco_de_armadura(rng, v):
    """Homem de Ferro: o servo zune, os propulsores sopram, a manopla bate com um "clang" e as faíscas chiam."""
    x = _z(1.0)
    n = n_de(0.14)
    poe(x, seno(varre(300, 900, n, 1.2), n) * env(n, 0.01, 0.1) * 0.08, 0.0)
    poe(x, _sopro(rng, 0.16, 800, 5000, 0.4), 0.02)
    poe(x, _acerto(rng, v, 0.8, 120), 0.14)
    poe(x, modal(n_de(0.5), 620 + 30 * v, rng=rng, **METAL) * 0.22, 0.14)
    poe(x, graos(rng, n_de(0.35), 40, 0.0, 0.3, 2500, 9000, 0.004) * 0.45, 0.15)
    return reverb(x, 0.25, 0.12, 6500)


def soco_da_manopla(rng, v):
    """Thanos: o soco lento e grave, o chão rachando com estalos e o brilho das Joias por cima."""
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.22, 220, 1800, 0.85, g=0.55), 0.0)
    poe(x, _acerto(rng, v, 1.2, 85), 0.2)
    poe(x, baque(n_de(0.45), 70, 35, 0.12, 0.6) * 0.6, 0.2)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.04), 900, 4000, 0.008) * 0.3, 0.22 + 0.035 * k)
    for k, f in enumerate((1047, 1319, 1568)):
        poe(x, _brilho(rng, 0.45, f, 0.035, SINO), 0.24 + 0.05 * k)
    return reverb(x, 0.4, 0.18, 5000)


def soco_do_gohan(rng, v):
    """Gohan: o soco calmo e firme e o ar que ecoa em dois tempos (os dois anéis)."""
    x = _z(0.95)
    poe(x, _whoosh(rng, 0.15, 450, 3000, 0.85, g=0.45), 0.0)
    poe(x, _acerto(rng, v, 1.0, 115), 0.16)
    poe(x, _sopro(rng, 0.25, 300, 2600, 0.3), 0.17)
    poe(x, _sopro(rng, 0.3, 200, 1600, 0.22), 0.27)
    return reverb(x, 0.3, 0.14, 6000)


SONS: dict = {
    "soco-saiyajin": (soco_saiyajin, "básico de Goku: o ki chiando no punho, o soco e a onda de ar"),
    "soco-do-principe": (soco_do_principe, "básico de Vegeta: estalos azuis de ki e o soco seco"),
    "soco-do-naruto": (soco_do_naruto, "básico de Naruto: o soco, a espiral girando e o puf de fumaça"),
    "soco-infinito": (soco_infinito, "básico de Gojo: o ar travando no Infinito e o soco entrando de uma vez"),
    "soco-veloz-flash": (soco_veloz_flash, "básico de Flash: três tapas grudados e o estalo do raio"),
    "soco-de-armadura": (soco_de_armadura, "básico de Homem de Ferro: servo, propulsor e o clang da manopla"),
    "soco-da-manopla": (soco_da_manopla, "básico de Thanos: soco grave, o chão rachando e o brilho das Joias"),
    "soco-do-gohan": (soco_do_gohan, "básico de Gohan: o soco calmo e o ar ecoando em dois tempos"),
}
