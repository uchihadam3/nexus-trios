"""Sons dos ataques básicos, lote d (veja tools/vfx/familias_v2/basicos_d.py).

Cada receita segue o tempo da animação: os dois "shink" das adagas do Jinwoo com o
sussurro da sombra, a carne e as perfurações da kagune, a carta que vira e a magia do
Yugi, a carta e o raio do dragão do Kaiba, a rajada de socos do Seiya, o gancho e o
vento do dragão do Shiryu, o gelo cristalino do Hyoga, os elos e o estalo da corrente
do Shun, a fênix do Ikki, o sino tibetano do Shaka, o disco girando da tiara lunar,
as garras de fogo do Charizard e a chama azul estranha do Bill Cipher.
Tudo sintetizado, sem vozes.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _tom, _whoosh, _z, nota  # noqa: F401
from sfx_familias import _tilim
from som import (CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, graos, modal, n_de, passa, poe,  # noqa: F401
                 reverb, rosa, ruido, satura, seno, sobe_e_some, varre)
from som import CENTROS, faixas, janela_suave, serra_suave

# nome do arquivo (com hífen) → (função, descrição)
SONS: dict = {}


# ------------------------------------------------------------------ peças
def _shink(rng, f0=3000, g=1.0):
    """Um corte rápido de lâmina curta: assobio curtíssimo, o fio passando e o brilho de metal."""
    x = _z(0.3)
    w = assobio(rng, n_de(0.08), 1800, 8000, 1.5, 0.4) * sobe_e_some(n_de(0.08), 0.85, 1.3)
    poe(x, w, 0.0, 0.7 * g)
    n = n_de(0.1)
    poe(x, passa(ruido(rng, n), 2800, 10000, 2) * env(n, 0.0004, 0.02) * 0.8 * g, 0.06)
    poe(x, B._lamina_curta(rng, n_de(0.22), f0 * rng.uniform(0.95, 1.05)) * 0.28 * g, 0.06)
    poe(x, B._carne(rng, n_de(0.08), 0.018) * 0.3 * g, 0.065)
    return x


def _papel(rng, g=0.5):
    """O "fwip" de uma carta virando no ar: dois sopros curtos de papel."""
    x = _z(0.12)
    for k in range(2):
        n = n_de(0.05)
        poe(x, passa(ruido(rng, n), 1800 + 1500 * k, 9000, 2) * sobe_e_some(n, 0.3, 1.0) * g * (1 - 0.3 * k), 0.035 * k)
    return x


def _squelch(rng, seg=0.18, f0=500, f1=180, g=0.6):
    """Som molhado de carne: ruído por um filtro que desce rápido, saturado."""
    n = n_de(seg)
    s = faixas(rosa(rng, n), CENTROS, varre(f0, f1, n, 0.6), 0.35) * env(n, 0.004, seg * 0.35)
    return satura(s * 2.0, 2.2) * g


# ------------------------------------------------------------------ Jinwoo
def adaga_de_kamish(rng, v):
    x = _z(1.2)
    poe(x, _shink(rng, 3200), 0.0)
    poe(x, _shink(rng, 3700, 1.1), 0.13)
    # sussurro da sombra: ar soprado por dois "formantes" que se movem, com tremor; sem palavra nenhuma
    n = n_de(0.9)
    t = np.arange(n) / SR
    ar = rosa(rng, n)
    f1 = 650 + 180 * np.sin(2 * math.pi * 1.7 * t)
    f2 = 1900 + 500 * np.sin(2 * math.pi * 1.1 * t + 1)
    sus = faixas(ar, CENTROS, f1, 0.3) + faixas(ar, CENTROS, f2, 0.3) * 0.7 + passa(ar, 4500, 9000, 2) * 0.35
    sus *= sobe_e_some(n, 0.35, 1.6) * (0.75 + 0.25 * np.sin(2 * math.pi * 7 * t)) * 0.45
    poe(x, sus, 0.22)
    poe(x, _tom(nota(38), nota(34), 0.9, 0.5, 0.18) + passa(rosa(rng, n), 60, 350, 2) * env(n, 0.08, 0.35) * 0.35, 0.2)
    return reverb(x, 0.6, 0.3, 3500)


# ------------------------------------------------------------------ Kaneki
def kagune(rng, v):
    x = _z(1.0)
    # os tentáculos se esticando: um rangido elástico que sobe
    n = n_de(0.35)
    t = np.arange(n) / SR
    estica = satura(seno(varre(70, 160, n, 1.0) * (1 + 0.04 * np.sin(2 * math.pi * 23 * t)), n), 3) * sobe_e_some(n, 0.8, 1.4) * 0.25
    poe(x, passa(estica, 80, 1800, 2), 0.0)
    for k in range(4):
        em = 0.11 + 0.055 * k
        poe(x, _whoosh(rng, 0.07, 900, 3000, 0.9, g=0.35), em - 0.06)
        poe(x, B._carne(rng, n_de(0.12), 0.04, 2.8) * 0.9, em)
        poe(x, B._tapa(rng, n_de(0.08), 900, 4000, 0.008) * 0.6, em)
        poe(x, _squelch(rng, 0.2, rng.uniform(700, 900), 160, 0.55), em + 0.01)
    poe(x, B._baque_seco(rng, n_de(0.3), 80, 0.1) * 0.7, 0.28)
    # o recuo molhado
    poe(x, _squelch(rng, 0.3, 300, 900, 0.35), 0.6)
    return reverb(x, 0.3, 0.14, 4000)


# ------------------------------------------------------------------ Yugi
def carta_magica(rng, v):
    x = _z(1.3)
    poe(x, _papel(rng, 0.6), 0.0)
    poe(x, _papel(rng, 0.4), 0.09)
    # a carta brilha: arpejo de sininhos subindo
    for k, m in enumerate((79, 83, 86, 91)):
        poe(x, _brilho(rng, 0.5, nota(m), 0.12, CRISTAL), 0.14 + 0.045 * k)
    # a estrela mágica estoura
    poe(x, B.impacto_energia(rng, v) * 0.8, 0.34)
    poe(x, _whoosh(rng, 0.25, 600, 5000, 0.85, g=0.4), 0.12)
    poe(x, graos(rng, n_de(0.7), 30, 0.0, 0.6, 4000, 11000, 0.003) * 0.3, 0.36)
    poe(x, _tom(nota(62), nota(74), 0.5, 0.3, 0.12), 0.34)
    return reverb(x, 0.6, 0.3, 8000)


# ------------------------------------------------------------------ Kaiba
def carta_dragao(rng, v):
    x = _z(1.35)
    poe(x, _papel(rng, 0.7), 0.0)
    # a carga: zumbido que sobe rápido
    n = n_de(0.22)
    poe(x, seno(varre(300, 1400, n, 1.4), n) * sobe_e_some(n, 0.95, 1.4) * 0.15 + assobio(rng, n, 600, 5000, 1.5, 0.4) * sobe_e_some(n, 0.95, 1.6) * 0.3, 0.06)
    # o raio branco: rugido de energia grosso (sem voz), com batimento lento
    n = n_de(0.6)
    t = np.arange(n) / SR
    rug = satura(passa(rosa(rng, n), 150, 2500, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 17 * t)), 2.4) * 0.6
    zum = satura(serra_suave(nota(40) * (1 + 0.01 * np.sin(2 * math.pi * 6 * t)), n, 12), 1.6) * 0.3
    poe(x, (rug + zum) * janela_suave(n, 0.02, 0.2), 0.22)
    poe(x, B.feixe(rng, v)[: n_de(0.55)] * 0.5, 0.22)
    poe(x, B.explosao(rng, v)[: n_de(0.8)] * 0.75, 0.34)
    return reverb(x, 0.55, 0.25)


# ------------------------------------------------------------------ Seiya
def meteoros_de_pegaso(rng, v):
    x = _z(1.1)
    # zunido de fundo da rajada
    n = n_de(0.62)
    t = np.arange(n) / SR
    poe(x, assobio(rng, n, 1500, 4500, 1.0, 0.35) * (0.6 + 0.4 * np.sin(2 * math.pi * 21 * t) ** 2) * sobe_e_some(n, 0.2, 1.0) * 0.4, 0.0)
    poe(x, seno(varre(nota(84), nota(88), n), n) * sobe_e_some(n, 0.3, 1.0) * 0.05, 0.0)
    em = 0.06
    k = 0
    while em < 0.6 and k < 40:
        poe(x, _whoosh(rng, 0.05, 2500, 7000, 0.9, g=0.18), em - 0.04)
        poe(x, B.soco_leve(rng, v)[: n_de(0.12)] * rng.uniform(0.35, 0.6), em)
        em += max(0.012, rng.uniform(0.018, 0.03))
        k += 1
    poe(x, B.soco_pesado(rng, v) * 0.9, 0.62)
    poe(x, B.impacto_energia(rng, v)[: n_de(0.45)] * 0.5, 0.62)
    return reverb(x, 0.35, 0.15)


# ------------------------------------------------------------------ Shiryu
def punho_do_dragao(rng, v):
    x = _z(1.35)
    # o gancho subindo
    n = n_de(0.24)
    poe(x, assobio(rng, n, 250, 3500, 1.6, 0.45) * sobe_e_some(n, 0.9, 1.6) * 0.8, 0.0)
    poe(x, B.soco_pesado(rng, v), 0.2)
    # o dragão subindo: rugido de vento que sobe em espiral (tremolo), sem voz
    n = n_de(0.95)
    t = np.arange(n) / SR
    giro = 0.6 + 0.4 * np.sin(2 * math.pi * (5 + 6 * t) * t) ** 2
    vento = assobio(rng, n, 300, 1800, 0.8, 0.5) * giro * sobe_e_some(n, 0.45, 1.4) * 0.8
    rugido = satura(passa(rosa(rng, n), 90, 900, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 12 * t)), 2.6) * sobe_e_some(n, 0.55, 1.3) * 0.5
    poe(x, vento + rugido, 0.12)
    return reverb(x, 0.6, 0.28)


# ------------------------------------------------------------------ Hyoga
def po_de_diamante(rng, v):
    x = _z(1.35)
    # vento frio que sopra
    n = n_de(0.9)
    t = np.arange(n) / SR
    poe(x, assobio(rng, n, 2500, 6000, 0.9, 0.35) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.45, 0.0)
    poe(x, assobio(rng, n, 500, 1200, 1.0, 0.5) * sobe_e_some(n, 0.3, 1.4) * 0.25, 0.0)
    # o pó de cristais: muitos tilintares cristalinos agudos
    for _ in range(26):
        f = nota(rng.choice([88, 91, 93, 95, 96, 98, 100]))
        poe(x, modal(n_de(0.35), f, rng=rng, **CRISTAL) * env(n_de(0.35), 0.0008, 0.07) * rng.uniform(0.04, 0.09), rng.uniform(0.02, 0.5))
    # congela
    poe(x, B.gelo(rng, v) * 0.7, 0.3)
    poe(x, estalo(rng, n_de(0.1), 3000, 12000, 0.006) * 0.6, 0.3)
    return reverb(x, 0.6, 0.3, 10000)


# ------------------------------------------------------------------ Shun
def corrente_de_andromeda(rng, v):
    x = _z(1.0)
    n = n_de(0.32)
    poe(x, assobio(rng, n, 700, 4000, 1.3, 0.5) * sobe_e_some(n, 0.8, 1.3) * 0.35, 0)
    # elos tilintando no voo, apertando no fim (zigue-zague: em ondas)
    for k in range(34):
        em = rng.uniform(0.0, 0.3) ** 0.9
        onda = 0.6 + 0.4 * abs(math.sin(em * 30))
        poe(x, _tilim(rng) * rng.uniform(0.1, 0.24) * onda, em)
    # o estalo da ponta cravando
    n = n_de(0.15)
    crack = passa(ruido(rng, n), 2000, 11000, 2) * env(n, 0.0003, 0.007) * 1.3 + baque(n, 900, 400, 0.01, 0.6) * 0.3
    poe(x, crack, 0.27)
    poe(x, B._placa_de_metal(rng, n_de(0.3), 400, 5000, 26, 0.07) * 0.35, 0.28)
    poe(x, B._baque_seco(rng, n_de(0.25), 120, 0.05) * 0.45, 0.28)
    # recolhendo
    for _ in range(14):
        poe(x, _tilim(rng, 0.05, 2500, 6500) * rng.uniform(0.06, 0.14), 0.5 + rng.uniform(0, 0.25))
    return reverb(x, 0.3, 0.15)


# ------------------------------------------------------------------ Ikki
def punho_da_fenix(rng, v):
    x = _z(1.35)
    poe(x, _whoosh(rng, 0.17, 350, 3000, 0.9, g=0.7), 0.0)
    poe(x, B.soco_pesado(rng, v), 0.15)
    # a chama explodindo
    poe(x, B.explosao(rng, v)[: n_de(0.7)] * 0.45, 0.16)
    poe(x, B.fogo(rng, v) * 0.85, 0.18)
    # o "grito" de vento da fênix: assobio agudo e estreito que sobe e desce (não é voz)
    n = n_de(0.7)
    t = np.arange(n) / SR
    curva = varre(1400, 3200, n, 0.5) * (1 - 0.25 * np.clip((t - 0.35) / 0.35, 0, 1))
    grito = faixas(rosa(rng, n), CENTROS, curva, 0.18) * sobe_e_some(n, 0.35, 1.3) * 0.7
    grito += seno(curva * (1 + 0.015 * np.sin(2 * math.pi * 9 * t)), n) * sobe_e_some(n, 0.35, 1.3) * 0.07
    poe(x, grito, 0.24)
    return reverb(x, 0.6, 0.28)


# ------------------------------------------------------------------ Shaka
def rendicao(rng, v):
    x = _z(1.42)
    # sino tibetano (tigela que canta): parciais inarmônicos com batimento lento
    n = n_de(1.4)
    t = np.arange(n) / SR
    f0 = nota(rng.uniform(66, 68))
    tig = np.zeros(n)
    for r, q, g in ((1.0, 1.4, 1.0), (2.71, 0.9, 0.55), (5.15, 0.5, 0.3), (8.2, 0.3, 0.15)):
        for d in (1.0, 1.0035):
            tig += g * np.sin(2 * math.pi * f0 * r * d * t + rng.uniform(0, 6)) * np.exp(-t / q)
    tig *= env(n, 0.002, 2.0) * 0.18
    poe(x, tig, 0.0)
    poe(x, B._tapa(rng, n_de(0.03), 2000, 7000, 0.003) * 0.25, 0.0)
    # o pulso de luz: um "vum" grave que cresce e solta
    n = n_de(0.6)
    vum = seno(varre(nota(45), nota(52), n, 1.0), n) * sobe_e_some(n, 0.6, 1.8) * 0.35
    vum += passa(rosa(rng, n), 200, 1500, 2) * sobe_e_some(n, 0.6, 2.0) * 0.18
    poe(x, vum, 0.15)
    poe(x, B.impacto_energia(rng, v)[: n_de(0.5)] * 0.35, 0.5)
    poe(x, graos(rng, n_de(0.6), 14, 0.0, 0.5, 5000, 11000, 0.003) * 0.15, 0.5)
    return reverb(x, 0.7, 0.35, 7000)


# ------------------------------------------------------------------ Sailor Moon
def tiara_lunar(rng, v):
    x = _z(1.2)
    # o disco girando e se aproximando: "uom-uom" cada vez mais rápido e mais agudo
    n = n_de(0.32)
    t = np.arange(n) / SR
    taxa = 14 + 30 * t / (n / SR)
    giro = 0.45 + 0.55 * np.sin(2 * math.pi * np.cumsum(taxa) / SR) ** 2
    zum = seno(varre(nota(76), nota(81), n), n) * 0.12 + assobio(rng, n, 1500, 4500, 1.0, 0.35) * 0.4
    poe(x, zum * giro * sobe_e_some(n, 0.95, 1.4), 0.0)
    # acerta: pancada leve + brilho mágico
    poe(x, B.soco_leve(rng, v) * 0.6, 0.3)
    poe(x, estalo(rng, n_de(0.08), 3000, 12000, 0.005) * 0.6, 0.3)
    for k, m in enumerate((84, 88, 91, 96)):
        poe(x, _brilho(rng, 0.6, nota(m), 0.11, CRISTAL), 0.31 + 0.035 * k)
    poe(x, graos(rng, n_de(0.6), 24, 0.0, 0.5, 5000, 12000, 0.003) * 0.25, 0.33)
    return reverb(x, 0.55, 0.28, 9000)


# ------------------------------------------------------------------ Charizard
def garra_flamejante(rng, v):
    x = _z(1.1)
    for k in range(3):
        n = n_de(0.16)
        r = passa(ruido(rng, n), 1200, 6500, 2) * env(n, 0.002, 0.05) * 0.75
        r += B._carne(rng, n, 0.03) * 0.35
        poe(x, _whoosh(rng, 0.08, 700, 3500, 0.8, g=0.3), 0.025 * k)
        poe(x, r, 0.05 + 0.03 * k)
    poe(x, B._baque_seco(rng, n_de(0.25), 95, 0.07) * 0.6, 0.06)
    # a chama acende nos riscos: "fuum" e o crepitar
    n = n_de(0.25)
    poe(x, assobio(rng, n, 200, 1800, 0.8, 0.5) * sobe_e_some(n, 0.25, 1.0) * 0.6, 0.1)
    poe(x, B.fogo(rng, v) * 0.75, 0.12)
    return reverb(x, 0.4, 0.18)


# ------------------------------------------------------------------ Bill Cipher
def chama_do_triangulo(rng, v):
    x = _z(1.4)
    # aparece: um "pling" invertido (cresce do nada) e um tilintar de caixinha de música desafinado
    n = n_de(0.3)
    rev = (modal(n, nota(81), rng=rng, **VIDRO) * env(n, 0.001, 0.12))[::-1] * 0.2
    poe(x, rev, 0.0)
    notas = [rng.choice([76, 77, 80, 83, 84, 86]) for _ in range(6)]
    for k, m in enumerate(notas):
        nn = n_de(0.35)
        tt = np.arange(nn) / SR
        f = nota(m) * (1 + 0.03 * np.sin(2 * math.pi * 5.5 * tt + k))                 # desafinando, oscilando
        tl = (seno(f, nn) + 0.4 * seno(f * 2.76, nn) + 0.2 * seno(f * 5.4, nn)) * env(nn, 0.001, 0.09)
        passo = 3 + (k % 3)                                                             # "bitcrush": segura amostras
        tl = np.repeat(tl[::passo], passo)[:nn]
        poe(x, tl * 0.12, 0.06 + 0.07 * k + rng.uniform(-0.01, 0.01))
    # a chama azul: fogo com modulação em anel (metálica, estranha) e tremolo
    n = n_de(1.0)
    t = np.arange(n) / SR
    fg = B.fogo(rng, v)
    fg = np.concatenate([fg, np.zeros(max(0, n - len(fg)))])[:n]
    anel = fg * np.sin(2 * math.pi * (230 + 60 * np.sin(2 * math.pi * 0.8 * t)) * t)
    chama = (fg * 0.55 + anel * 0.6) * (0.8 + 0.2 * np.sin(2 * math.pi * 9 * t))
    poe(x, chama, 0.3)
    poe(x, _tom(nota(45), nota(39), 0.9, 0.45, 0.15), 0.3)
    return reverb(x, 0.6, 0.3, 6000)


SONS["adaga-de-kamish"] = (adaga_de_kamish, "básico de Jinwoo: dois cortes de adaga e o sussurro da sombra")
SONS["kagune"] = (kagune, "básico de Kaneki: tentáculos de carne esticando e quatro perfurações")
SONS["carta-magica"] = (carta_magica, "básico de Yugi: carta virando, sininhos e a estrela mágica estourando")
SONS["carta-dragao"] = (carta_dragao, "básico de Kaiba: carta, carga e o rugido de energia do raio do dragão")
SONS["meteoros-de-pegaso"] = (meteoros_de_pegaso, "básico de Seiya: rajada de dezenas de socos com zunido")
SONS["punho-do-dragao"] = (punho_do_dragao, "básico de Shiryu: gancho subindo e o rugido de vento do dragão")
SONS["po-de-diamante"] = (po_de_diamante, "básico de Hyoga: cristais tilintando, vento frio e gelo estalando")
SONS["corrente-de-andromeda"] = (corrente_de_andromeda, "básico de Shun: elos tilintando e o estalo da ponta")
SONS["punho-da-fenix"] = (punho_da_fenix, "básico de Ikki: soco, chama explodindo e o grito de vento da fênix")
SONS["rendicao"] = (rendicao, "básico de Shaka: sino tibetano e o pulso de luz")
SONS["tiara-lunar"] = (tiara_lunar, "básico de Sailor Moon: disco girando que acerta com brilho mágico")
SONS["garra-flamejante"] = (garra_flamejante, "básico de Charizard: três garras e a chama acendendo")
SONS["chama-do-triangulo"] = (chama_do_triangulo, "básico de Bill Cipher: tilintar distorcido e chama azul estranha")
