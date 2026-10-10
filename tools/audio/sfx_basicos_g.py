"""Sons dos ataques básicos, lote g (veja tools/vfx/familias_v2/basicos_g.py).

Cada receita segue a folha do mesmo nome: a lâmina longa que canta (Masamune), as correntes
e o fogo (Lâminas do Caos), o tiro de plasma (canhão de braço), o "tchk" da bainha depois dos
cortes no espaço (Yamato), o "pew" de 8 bits (Buster), o zumbido do sabre (Z-Saber)… Tudo
sintetizado, sem trechos de som de jogo.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _tom, _whoosh, _z, nota  # noqa: F401
from som import (CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, graos, modal, n_de, passa, poe,  # noqa: F401
                 reverb, rosa, ruido, satura, seno, sobe_e_some, varre)

# nome do arquivo (com hífen) → (função, descrição)
SONS: dict = {}


# ------------------------------------------------------------------ peças
def _canto_de_lamina(rng, seg, f0, queda, g=0.3):
    """O "iiiing" que fica depois do fio: parciais altos quase puros, com batimento lento."""
    n = n_de(seg)
    t = np.arange(n) / SR
    x = (seno(f0 * (1 + 0.0015 * np.sin(2 * math.pi * 5 * t)), n) * 0.5 + seno(f0 * 1.006, n) * 0.4
         + seno(f0 * 1.5, n) * 0.18 + seno(f0 * 2.01, n) * 0.1)
    return x * env(n, 0.003, queda) * g


def _elos(rng, seg, quantos, inicio, fim, g=0.25):
    """Corrente chacoalhando: tinidos curtos de metal espalhados no tempo."""
    out = _z(seg)
    for _ in range(quantos):
        n = n_de(0.06)
        tin = modal(n, rng.uniform(2200, 4200), rng=rng, **METAL) * env(n, 0.0005, 0.018) * rng.uniform(0.5, 1)
        tin += passa(ruido(rng, n), 3000, 9000, 2) * env(n, 0.0003, 0.004) * 0.4
        poe(out, tin, rng.uniform(inicio, fim))
    return out * g


def _quadrada(freq, n):
    """Onda quadrada (o timbre dos consoles de 8 bits), levemente arredondada."""
    return np.tanh(seno(freq, n) * 6) * 0.8


def _tiro_de_pistola(rng, v, agudo=1.0):
    n = n_de(0.45)
    x = B.tiro(rng, v)[:n]
    x = np.concatenate([x, np.zeros(max(0, n - len(x)))])
    x += estalo(rng, n, 2500 * agudo, 9000, 0.004) * 0.7                         # o estalo seco do cano curto
    x += baque(n, 180 * agudo, 80, 0.04, 0.5) * 0.4
    return x


def _tilintar(rng, g=0.12):
    """Cartucho caindo no chão."""
    n = n_de(0.25)
    x = _z(0.25)
    for k in range(3):
        poe(x, modal(n_de(0.12), rng.uniform(4500, 6500), rng=rng, **METAL) * env(n_de(0.12), 0.0005, 0.03) * (0.8 - 0.25 * k), k * rng.uniform(0.05, 0.08))
    return x[:n] * g


# ------------------------------------------------------------------ Sephiroth
def masamune(rng, v):
    """Lâmina longuíssima: whoosh agudo e rápido, o fio rasgando o ar e um "shiiiing" longo e limpo."""
    x = _z(1.4)
    poe(x, _whoosh(rng, 0.16, 1500, 9500, 0.85, g=0.75), 0)
    n = n_de(0.14)
    poe(x, passa(ruido(rng, n), 3500, 12000, 2) * env(n, 0.0005, 0.035) * 0.9, 0.12)
    poe(x, B.corte(rng, v)[n_de(0.08):] * 0.6, 0.11)
    poe(x, _canto_de_lamina(rng, 1.25, rng.uniform(3000, 3300), 0.42, 0.32), 0.12)
    poe(x, modal(n_de(1.0), rng.uniform(1700, 1900), rng=rng, desafina=0.01, **METAL) * env(n_de(1.0), 0.001, 0.32) * 0.12, 0.12)
    return reverb(x, 0.75, 0.32, 9000)


# ------------------------------------------------------------------ Kratos
def laminas_do_caos(rng, v):
    """Correntes chacoalhando, duas lâminas girando com sopro de fogo, dois cortes e as chamas estalando."""
    x = _z(1.15)
    poe(x, _elos(rng, 0.5, 16, 0.0, 0.42, 0.3), 0)
    for k, em in enumerate((0.0, 0.15)):
        n = n_de(0.28)
        giro = assobio(rng, n, 250, 1800, 1.2, 0.55) * sobe_e_some(n, 0.8, 1.3) * 0.8
        poe(x, giro, em)
        poe(x, B.corte_pesado(rng, v) * (0.85 if k == 0 else 1.0), em + 0.2)
    fogo = B.fogo(rng, v)[: n_de(0.85)]
    poe(x, fogo * 0.55, 0.05)
    poe(x, graos(rng, n_de(0.7), 30, 0.15, 0.6, 1500, 7000, 0.003) * 0.35, 0.2)
    return reverb(x, 0.5, 0.22, 6000)


# ------------------------------------------------------------------ Link
def espada_mestra(rng, v):
    """Espada em arco (whoosh + corte limpo) e o brilho mágico: três toques de cristal subindo."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.22, 600, 5500, 0.8, g=0.8), 0)
    poe(x, B.corte(rng, v), 0.14, 1.0)
    poe(x, _canto_de_lamina(rng, 0.6, rng.uniform(2400, 2600), 0.18, 0.12), 0.18)
    base = rng.uniform(86, 88)
    for k, d in enumerate((0, 4, 7, 12)):
        poe(x, _brilho(rng, 0.6, nota(base + d), 0.11 - 0.015 * k, CRISTAL), 0.26 + 0.06 * k)
    poe(x, graos(rng, n_de(0.5), 14, 0.0, 0.4, 6000, 12000, 0.002) * 0.12, 0.28)
    return reverb(x, 0.65, 0.3, 9000)


# ------------------------------------------------------------------ Samus
def canhao_de_braco(rng, v):
    """Tiro de energia sci-fi: "tchiu" descendente com zumbido de plasma, voo curto e estouro com anel."""
    x = _z(1.1)
    n = n_de(0.28)
    f = varre(rng.uniform(1900, 2200), rng.uniform(320, 380), n, 0.55)
    tiro = satura(seno(f, n), 2.5) * env(n, 0.001, 0.09) * 0.45 + seno(f * 0.5, n) * env(n, 0.001, 0.12) * 0.35
    tiro += estalo(rng, n, 2500, 10000, 0.005) * 0.5
    poe(x, tiro, 0)
    n = n_de(0.22)
    t = np.arange(n) / SR
    zumbido = satura(seno(150 + 30 * np.sin(2 * math.pi * 40 * t), n), 3) * sobe_e_some(n, 0.5, 1.2) * 0.18
    poe(x, zumbido + assobio(rng, n, 1500, 3500, 1.0, 0.4) * sobe_e_some(n, 0.7, 1.2) * 0.35, 0.03)
    poe(x, B.explosao(rng, v)[: n_de(0.8)] * 0.7, 0.2)
    poe(x, _tom(nota(76), nota(64), 0.35, 0.15, 0.12), 0.21)
    return x


# ------------------------------------------------------------------ Dante
def rebellion_e_ebony(rng, v):
    """Espadão pesado cortando e, logo depois, dois tiros de pistola (o segundo um tom diferente)."""
    x = _z(1.15)
    poe(x, _whoosh(rng, 0.24, 250, 3000, 0.85, g=0.9), 0)
    poe(x, B.corte_pesado(rng, v), 0.12, 1.0)
    poe(x, _tiro_de_pistola(rng, v, 1.0), 0.3, 0.95)
    poe(x, _tiro_de_pistola(rng, v, 1.15), 0.45, 0.95)
    return reverb(x, 0.45, 0.18, 6000)


# ------------------------------------------------------------------ Vergil
def corte_dimensional(rng, v):
    """Saque rapidíssimo, uma rajada de cortes finos no espaço, o "tchk" da bainha fechando e o
    espaço se partindo como vidro."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.08, 3000, 10000, 0.7, g=0.5), 0)
    for k in range(9):
        n = n_de(0.07)
        em = 0.06 + k * 0.035 + rng.uniform(-0.008, 0.008)
        s = passa(ruido(rng, n), 4000, 12000, 2) * env(n, 0.0004, 0.012) * 0.55
        s += _canto_de_lamina(rng, 0.07, rng.uniform(3500, 5200), 0.02, 0.15)
        poe(x, s, em)
    # "tchk": a guarda batendo na bainha (dois cliques metálicos, o segundo mais grave)
    for em, f, g in ((0.44, 2600, 0.6), (0.47, 1500, 0.8)):
        n = n_de(0.08)
        clique = estalo(rng, n, 1500, 8000, 0.003) * g + modal(n, f, rng=rng, **METAL) * env(n, 0.0005, 0.025) * 0.25 * g
        poe(x, clique, em)
    # o espaço se parte
    n = n_de(0.7)
    vidro = modal(n, rng.uniform(1800, 2100), rng=rng, desafina=0.03, **VIDRO) * env(n, 0.001, 0.2) * 0.15
    vidro += passa(ruido(rng, n), 2000, 11000, 2) * env(n, 0.001, 0.07) * 0.55
    vidro += graos(rng, n, 30, 0.01, 0.35, 3500, 11000, 0.004) * 0.35
    poe(x, vidro + baque(n, 90, 45, 0.15, 0.3) * 0.6, 0.55)
    return reverb(x, 0.65, 0.28, 8000)


# ------------------------------------------------------------------ Snake
def cqc(rng, v):
    """Agarrão (pano e mãos), o corpo virando no ar (whoosh) e a queda pesada de costas no chão."""
    x = _z(1.1)
    n = n_de(0.18)
    pega = passa(ruido(rng, n), 1200, 6000, 2) * env(n, 0.003, 0.04) * 0.5 + B.soco_leve(rng, v)[:n] * 0.5
    poe(x, pega, 0.0)
    poe(x, passa(rosa(rng, n_de(0.2)), 2000, 7000, 2) * env(n_de(0.2), 0.01, 0.05) * 0.25, 0.06)
    n = n_de(0.3)
    poe(x, assobio(rng, n, 200, 1600, 1.0, 0.55) * sobe_e_some(n, 0.75, 1.3) * 0.85, 0.12)
    poe(x, B.esmagar(rng, v)[: n_de(0.65)] * 0.9, 0.38)
    poe(x, baque(n_de(0.4), 75, 38, 0.14, 0.5) * 0.7, 0.38)
    poe(x, graos(rng, n_de(0.5), 20, 0.02, 0.35, 600, 3000, 0.008) * 0.3, 0.4)
    return x


# ------------------------------------------------------------------ Wesker
def golpe_sobre_humano(rng, v):
    """Um "zip" rápido de deslocamento (ar rasgado e tom subindo) e a palma que acerta seco e pesado."""
    x = _z(0.95)
    n = n_de(0.16)
    zip_ = assobio(rng, n, 1200, 9000, 0.7, 0.35) * sobe_e_some(n, 0.6, 1.0) * 0.8
    zip_ += seno(varre(500, 2600, n, 0.6), n) * env(n, 0.002, 0.05) * 0.12
    poe(x, zip_, 0.0)
    poe(x, _whoosh(rng, 0.12, 2500, 6000, 0.4, g=0.35), 0.1)
    poe(x, B.soco_pesado(rng, v), 0.22, 1.05)
    n = n_de(0.05)
    poe(x, passa(ruido(rng, n), 1500, 7000, 2) * env(n, 0.0003, 0.008) * 0.9, 0.22)     # o tapa da palma
    poe(x, assobio(rng, n_de(0.5), 3500, 300, 0.7, 0.55) * env(n_de(0.5), 0.004, 0.15) * 0.5, 0.23)
    return reverb(x, 0.35, 0.15, 5000)


# ------------------------------------------------------------------ Lara
def duas_pistolas(rng, v):
    """Dois tiros rápidos de pistola, um de cada mão, e os cartuchos tilintando."""
    x = _z(1.0)
    poe(x, _tiro_de_pistola(rng, v, 1.1), 0.02, 1.0)
    poe(x, _tiro_de_pistola(rng, v, 0.95), 0.2, 1.0)
    poe(x, _tilintar(rng, 0.14), 0.42)
    poe(x, _tilintar(rng, 0.12), 0.56)
    return x


# ------------------------------------------------------------------ Ezio
def lamina_oculta(rng, v):
    """O mecanismo da lâmina oculta: estalo de mola "shkt" e a lâmina deslizando, a perfuração
    curta, e um zumbido grave e suave da visão de águia."""
    x = _z(1.1)
    n = n_de(0.12)
    mola = estalo(rng, n, 2500, 10000, 0.003) * 0.9
    mola += passa(ruido(rng, n), 4000, 11000, 2) * env(n, 0.002, 0.025) * 0.5
    mola += modal(n, rng.uniform(3200, 3600), rng=rng, **METAL) * env(n, 0.0005, 0.03) * 0.2
    poe(x, estalo(rng, n_de(0.03), 1000, 4000, 0.003) * 0.6, 0.08)
    poe(x, mola, 0.11)
    poe(x, B.estocada(rng, v), 0.15, 1.0)
    n = n_de(0.8)
    t = np.arange(n) / SR
    aguia = (seno(nota(45), n) * 0.5 + seno(nota(52), n) * 0.3 + seno(nota(57) * (1 + 0.003 * np.sin(2 * math.pi * 4 * t)), n) * 0.25)
    aguia *= sobe_e_some(n, 0.3, 1.5) * 0.18
    poe(x, aguia + assobio(rng, n, 400, 2000, 1.0, 0.5) * sobe_e_some(n, 0.35, 1.4) * 0.15, 0.25)
    return reverb(x, 0.55, 0.25, 6000)


# ------------------------------------------------------------------ Sonic
def spin_attack(rng, v):
    """A bola girando (whoosh que pulsa a cada volta, subindo) e o quique elástico no alvo."""
    x = _z(0.95)
    n = n_de(0.32)
    t = np.arange(n) / SR
    voltas = 18 + 14 * t / (n / SR)
    giro = assobio(rng, n, 700, 3500, 1.0, 0.4) * (0.35 + 0.65 * np.sin(math.pi * np.cumsum(voltas) / SR) ** 2)
    poe(x, giro * sobe_e_some(n, 0.8, 1.2) * 0.8, 0.0)
    poe(x, B.soco_leve(rng, v), 0.28, 0.9)
    n = n_de(0.4)
    t = np.arange(n) / SR
    f = 260 * (1 + 0.35 * np.exp(-t / 0.06)) * (1 + 0.12 * np.sin(2 * math.pi * 16 * t) * np.exp(-t / 0.15))
    boing = satura(seno(f, n), 1.6) * env(n, 0.002, 0.13) * 0.35
    poe(x, boing, 0.29)
    poe(x, _whoosh(rng, 0.2, 1000, 4000, 0.3, g=0.35), 0.36)
    return reverb(x, 0.3, 0.15)


# ------------------------------------------------------------------ Mega Man


# ------------------------------------------------------------------ Zero
def z_saber(rng, v):
    """Sabre de energia: o zumbido grave e elétrico que dá o "vwum" quando varre (o tom sobe e
    volta com o movimento), o chiado do corte e o zumbido sumindo."""
    x = _z(1.0)
    n = n_de(0.75)
    t = np.arange(n) / SR
    mov = np.exp(-((t - 0.13) / 0.08) ** 2)                      # o movimento do braço
    f = 118 * (1 + 0.5 * mov)
    zum = satura(seno(f, n) + seno(f * 2.003, n) * 0.7 + seno(f * 3.01, n) * 0.4 + seno(f * 4.02, n) * 0.25, 2.2)
    zum *= (0.35 + 0.65 * mov) * env(n, 0.01, 0.3, segura=0.12)
    poe(x, passa(zum, 80, 5000, 2) * 0.5, 0)
    poe(x, assobio(rng, n_de(0.3), 600, 4500, 0.9, 0.4) * sobe_e_some(n_de(0.3), 0.5, 1.2) * 0.55, 0.0)
    n = n_de(0.25)
    chiado = graos(rng, n, 25, 0.0, 0.2, 3000, 10000, 0.002) * 0.4 + passa(ruido(rng, n), 3000, 9000, 2) * env(n, 0.001, 0.04) * 0.5
    poe(x, chiado, 0.13)
    poe(x, B.corte(rng, v)[n_de(0.09):] * 0.5, 0.12)
    return reverb(x, 0.45, 0.2, 7000)


# ------------------------------------------------------------------ Mario
def pisada_do_mario(rng, v):
    """Pulo de desenho animado ("boing" que sobe), a pisada fofa que achata e um brilho de moeda."""
    x = _z(1.0)
    n = n_de(0.2)
    f = varre(220, 880, n, 0.6)
    pulo = _quadrada(f, n) * env(n, 0.002, 0.09) * 0.22 + seno(f, n) * env(n, 0.002, 0.1) * 0.2
    poe(x, pulo, 0.0)
    em = 0.19
    poe(x, B.soco_leve(rng, v), em, 0.8)
    n = n_de(0.22)
    achata = seno(varre(420, 90, n, 1.4), n) * env(n, 0.001, 0.07) * 0.45      # o "squish" que desce
    achata += passa(ruido(rng, n), 300, 1500, 2) * env(n, 0.002, 0.03) * 0.4
    poe(x, achata, em)
    poe(x, baque(n_de(0.3), 120, 60, 0.07, 0.3) * 0.5, em)
    for k in range(4):
        poe(x, _brilho(rng, 0.4, rng.uniform(2600, 3600), 0.06, CRISTAL), 0.36 + 0.05 * k)
    poe(x, _brilho(rng, 0.6, nota(rng.uniform(95, 97)), 0.08, SINO), 0.36)
    return reverb(x, 0.3, 0.15)


SONS["masamune"] = (masamune, "básico de Sephiroth: lâmina longa cortando o ar e o \"shiiing\" longo do fio")
SONS["laminas-do-caos"] = (laminas_do_caos, "básico de Kratos: correntes chacoalhando, giro com fogo e dois cortes")
SONS["espada-mestra"] = (espada_mestra, "básico de Link: corte de espada e um brilho de cristal subindo")
SONS["canhao-de-braco"] = (canhao_de_braco, "básico de Samus: tiro de plasma sci-fi e estouro pequeno")
SONS["rebellion-e-ebony"] = (rebellion_e_ebony, "básico de Dante: espadão pesado e dois tiros de pistola")
SONS["corte-dimensional"] = (corte_dimensional, "básico de Vergil: cortes múltiplos no espaço, \"tchk\" da bainha e o espaço se partindo")
SONS["cqc"] = (cqc, "básico de Snake: agarrão, giro e queda pesada no chão")
SONS["golpe-sobre-humano"] = (golpe_sobre_humano, "básico de Wesker: \"zip\" de velocidade e palma seca e pesada")
SONS["duas-pistolas"] = (duas_pistolas, "básico de Lara: dois tiros rápidos de pistola e cartuchos tilintando")
SONS["lamina-oculta"] = (lamina_oculta, "básico de Ezio: mola metálica \"shkt\", perfuração e o zumbido da visão de águia")
SONS["spin-attack"] = (spin_attack, "básico de Sonic: bola girando e quique elástico")
SONS["z-saber"] = (z_saber, "básico de Zero: \"vwum\" do sabre de energia e o chiado do corte")
SONS["pisada-do-mario"] = (pisada_do_mario, "básico de Mario: \"boing\" de pulo, pisada fofa e brilho de moeda")
