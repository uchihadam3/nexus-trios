"""Os sons das habilidades da Toph (e do básico dela) e do Gon (veja tools/vfx/familias_v2/toph_e_gon.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, nota
from som import (CRISTAL, METAL, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, ruido, satura,
                 seno, sobe_e_some, varre)


def _pisada(rng, g=1.0):
    """A pisada da Toph: um baque seco no chão com o estalo da terra."""
    n = n_de(0.5)
    return (baque(n, 110, 40, 0.16, 0.7) * 1.1 + estalo(rng, n, 300, 2500, 0.03) * 0.6) * g


def _pedra_rachando(rng, seg=0.4, g=1.0):
    n = n_de(seg)
    return (graos(rng, n, 40, 0.0, seg * 0.6, 250, 3500, 0.01, 0.6) * 0.9 + passa(ruido(rng, n), 200, 2200, 2) * env(n, 0.002, 0.08) * 0.8) * g


def _rocha_subindo(rng, seg=0.4, g=1.0):
    """A terra subindo: um ronco grave que sobe, com cascalho."""
    n = n_de(seg)
    t = np.arange(n) / SR
    return (satura(passa(rosa(rng, n), 40, 400, 2) * (t / t[-1]), 1.5) * 0.8 + graos(rng, n, 30, 0.0, seg, 300, 2500, 0.01, 0.6) * 0.5) * g


# --------------------------------------------------------------- Toph
def pedra_da_toph(rng, v):
    """O básico da Toph: a pisada, o bloco saltando do chão, o vento dele voando e a pedra se
    espatifando no rival."""
    x = _z(1.3)
    poe(x, _pisada(rng, 0.8), 0.0)
    poe(x, _rocha_subindo(rng, 0.2, 0.6), 0.03)
    poe(x, _whoosh(rng, 0.3, 200, 1500, 0.7, g=0.5), 0.15)
    poe(x, _pedra_rachando(rng, 0.5, 1.1), 0.42)
    poe(x, baque(n_de(0.4), 120, 55, 0.12, 0.6) * 0.8, 0.42)
    return reverb(x, 0.4, 0.18, 5500)


def visao_sismica(rng, v):
    """Visão sísmica: a pisada, o tremor correndo pelo chão (um ronco que pulsa), um "tom" baixo
    quando ela sente o rival e a terra subindo e prendendo os pés."""
    x = _z(1.6)
    poe(x, _pisada(rng, 1.0), 0.0)
    n = n_de(0.6)
    t = np.arange(n) / SR
    poe(x, passa(rosa(rng, n), 30, 300, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 9 * t)) * env(n, 0.02, 0.4) * 0.8, 0.05)
    poe(x, seno(nota(43), n_de(0.5)) * env(n_de(0.5), 0.02, 0.3) * 0.2, 0.45)
    poe(x, _rocha_subindo(rng, 0.3, 0.9), 0.6)
    poe(x, _pedra_rachando(rng, 0.4, 0.7), 0.85)
    return reverb(x, 0.45, 0.2, 5000)


def muralha_de_terra(rng, v):
    """Muralha de terra: a pisada, a muralha rompendo o chão num estrondo de pedra e as lascas
    caindo de volta."""
    x = _z(1.8)
    poe(x, _pisada(rng, 0.9), 0.0)
    poe(x, _rocha_subindo(rng, 0.35, 1.1), 0.05)
    poe(x, B.terremoto(rng, v) * 0.6, 0.2)
    poe(x, B.soco_pesado(rng, v) * 0.8, 0.3)
    poe(x, _pedra_rachando(rng, 0.6, 0.8), 0.32)
    for k in range(5):
        poe(x, _pedra_rachando(rng, 0.1, 0.35), 0.7 + 0.1 * k + rng.uniform(-0.03, 0.03))
    return reverb(x, 0.5, 0.22, 5000)


def metal_preparo(rng, v):
    """As placas de metal girando em volta da Toph: zumbidos metálicos e o raspar das chapas."""
    n = n_de(1.3)
    t = np.arange(n) / SR
    x = passa(ruido(rng, n), 1500, 7000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t)) * 0.18
    for k in range(5):
        poe(x, modal(n_de(0.5), nota(62 + 2 * k), rng=rng, **METAL) * env(n_de(0.5), 0.002, 0.25) * 0.15, 0.2 * k)
    return reverb(x * sobe_e_some(n, 0.8, 1.2), 0.4, 0.2, 7000)


def metal_dobrado(rng, v):
    """Metal dobrado: as faixas de metal chiando ao se enrolar, o aperto (um rangido grave de aço) e
    o esmagamento, com o tinido das faíscas."""
    x = _z(1.8)
    n = n_de(0.5)
    poe(x, passa(ruido(rng, n), 2000, 8000, 2) * sobe_e_some(n, 0.8, 1.2) * 0.3, 0.0)
    m = n_de(0.5)
    t = np.arange(m) / SR
    rangido = satura(seno(varre(90, 60, m, 1.0), m) * (0.6 + 0.4 * np.sin(2 * math.pi * 35 * t)), 2.5) * env(m, 0.03, 0.3) * 0.5
    poe(x, rangido, 0.4)
    poe(x, B.esmagar(rng, v) * 1.0, 0.6)
    poe(x, baque(n_de(0.6), 90, 35, 0.22, 0.7) * 1.0, 0.6)
    poe(x, modal(n_de(1.0), nota(50), rng=rng, **METAL) * env(n_de(1.0), 0.002, 0.5) * 0.45, 0.62)
    poe(x, graos(rng, n_de(0.6), 35, 0.0, 0.5, 3000, 9000, 0.003, 0.6) * 0.4, 0.65)
    return reverb(x, 0.5, 0.22, 6000)


# --------------------------------------------------------------- Gon
def nen_gon(rng, v):
    """A aura do Gon juntando no punho: um zumbido que sobe e engrossa, com a pressão do ar."""
    n = n_de(1.3)
    x = (seno(varre(nota(40), nota(55), n, 1.4), n) * 0.25 + seno(varre(nota(47), nota(62), n, 1.4), n) * 0.12) * sobe_e_some(n, 0.95, 1.6)
    x += passa(rosa(rng, n), 200, 2500, 2) * sobe_e_some(n, 0.9, 1.4) * 0.25
    return reverb(x, 0.45, 0.2, 6000)


def jajanken_pedra(rng, v):
    """Jajanken: Pedra — a aura no auge, o soco enorme e o estouro com o eco do impacto."""
    x = _z(1.6)
    n = n_de(0.25)
    poe(x, seno(varre(nota(55), nota(67), n, 1.0), n) * env(n, 0.01, 0.2) * 0.2, 0.0)
    poe(x, _whoosh(rng, 0.2, 300, 3000, 0.8, g=0.6), 0.05)
    poe(x, B.soco_pesado(rng, v) * 1.4, 0.22)
    poe(x, baque(n_de(0.9), 80, 30, 0.35, 0.8) * 1.3, 0.22)
    poe(x, B.explosao(rng, v) * 0.6, 0.25)
    return reverb(x, 0.6, 0.25, 5000)


def jajanken_tesoura(rng, v):
    """Jajanken: Tesoura — dois cortes de aura afiados, um em cada direção, com o zumbido da lâmina."""
    x = _z(1.3)
    poe(x, seno(nota(74), n_de(0.5)) * env(n_de(0.5), 0.02, 0.3) * 0.08, 0.0)
    poe(x, B.lamina_energia(rng, v) * 0.9, 0.05)
    poe(x, B.corte(rng, v) * 0.8, 0.1)
    poe(x, B.lamina_energia(rng, v) * 0.9, 0.25)
    poe(x, B.corte(rng, v) * 0.9, 0.3)
    poe(x, _brilho(rng, 0.5, nota(86), 0.12, CRISTAL), 0.32)
    return reverb(x, 0.45, 0.2, 7000)


def jajanken_papel(rng, v):
    """Jajanken: Papel — a bola de aura sai com um estampido, zune pelo ar e explode enorme."""
    x = _z(2.0)
    poe(x, B.disparo(rng, v) * 0.9, 0.0)
    n = n_de(0.4)
    poe(x, (seno(varre(nota(64), nota(57), n, 1.0), n) * 0.15 + passa(rosa(rng, n), 300, 3000, 2) * 0.4) * env(n, 0.01, 0.35), 0.05)
    poe(x, B.explosao(rng, v) * 1.2, 0.42)
    poe(x, baque(n_de(1.0), 70, 28, 0.4, 0.7) * 1.0, 0.42)
    return reverb(x, 0.65, 0.28, 4800)


SONS: dict = {
    "pedra-da-toph": (pedra_da_toph, "básico da Toph: a pisada, o bloco voando e a pedra se partindo"),
    "visao-sismica": (visao_sismica, "Visão sísmica: a pisada, o tremor e a terra prendendo"),
    "muralha-de-terra": (muralha_de_terra, "Muralha de terra: a muralha rompendo o chão"),
    "metal-preparo": (metal_preparo, "as placas de metal girando no Preparo"),
    "metal-dobrado": (metal_dobrado, "Metal dobrado: as faixas chiando, o aperto e o esmagamento"),
    "nen-gon": (nen_gon, "a aura do Gon juntando no punho"),
    "jajanken-pedra": (jajanken_pedra, "Jajanken: Pedra, o soco enorme"),
    "jajanken-tesoura": (jajanken_tesoura, "Jajanken: Tesoura, os dois cortes de aura"),
    "jajanken-papel": (jajanken_papel, "Jajanken: Papel, a bola de aura explodindo"),
}
