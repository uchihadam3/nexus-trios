"""Sons dos ataques básicos, lote a (veja tools/vfx/familias_v2/basicos_a.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _tom, _whoosh, _z, nota  # noqa: F401
from som import (CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, graos, modal, n_de, passa, poe,  # noqa: F401
                 reverb, rosa, ruido, satura, seno, sobe_e_some, varre)

# nome do arquivo (com hífen) → (função, descrição)
SONS: dict = {}


def _fwip(rng, seg=0.12, f0=900, f1=4200, g=0.6):
    """Disparo de ki: sopro curto que sobe + um "piu" tonal."""
    x = _whoosh(rng, seg, f0, f1, 0.35, 1.4, g)
    poe(x, _tom(nota(84), nota(72), seg * 0.8, seg * 0.35, g * 0.35), 0)
    return x


def _estouro(rng, tam=1.0):
    """Estouro de ki com baforada (baque + sopro de ruído)."""
    n = n_de(0.35)
    x = baque(n, 140 / tam, 60, 0.07 * tam, 0.35) * 0.7
    x += passa(rosa(rng, n), 300, 5000, 2) * env(n, 0.002, 0.06 * tam) * 0.8
    x += estalo(rng, n, 2500, 10000, 0.005) * 0.4
    return x


def _ziz(rng, seg, lo=1500, hi=10000, taxa=0.006, g=0.7):
    """Crepitar elétrico: pulsos aleatórios bem curtos (o "zzt")."""
    n = n_de(seg)
    z = np.zeros(n)
    k = 0
    while k < n:
        larg = max(1, int(rng.uniform(0.0003, 0.0015) * SR))
        z[k:k + larg] += rng.choice([-1, 1]) * rng.uniform(0.4, 1)
        k += max(8, int(rng.exponential(taxa) * SR))
    return passa(z, lo, hi, 2) * g


def ki_dourado(rng, v):
    x = _z(0.95)
    for k in range(3):
        poe(x, _fwip(rng, 0.13, 900 + 150 * k, 4200, 0.55), 0.13 * k * 0.85)
        poe(x, _estouro(rng, 1.0 + 0.35 * (k == 2)), 0.13 * k * 0.85 + 0.13, 0.9 + 0.25 * (k == 2))
    return reverb(x, 0.45, 0.2)


def rajada_continua(rng, v):
    x = _z(1.5)
    t0, k = 0.0, 0
    while t0 < 0.95 and k < 40:
        poe(x, _fwip(rng, 0.07, 1200, 5000, 0.35), t0)
        poe(x, _estouro(rng, 0.7), t0 + 0.06, rng.uniform(0.45, 0.75))
        t0 += max(0.02, 0.05 - 0.0012 * k + rng.uniform(-0.006, 0.006))
        k += 1
    n = n_de(1.3)
    ronco = satura(passa(rosa(rng, n), 50, 600, 2), 2.0) * np.linspace(0.05, 1.0, n) ** 1.5 * env(n, 0.3, 0.4, segura=0.85) * 0.9
    poe(x, ronco, 0.05)
    poe(x, B.explosao(rng, v), 0.95, 0.7)
    return reverb(x, 0.55, 0.22)


def golpe_do_potencial(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.14, 500, 3500, 0.85, g=0.6), 0)
    poe(x, B.soco_pesado(rng, v), 0.11, 1.1)
    poe(x, _tom(nota(48), nota(36), 0.4, 0.2, 0.3), 0.11)
    n = n_de(0.8)
    buzz = satura(seno(varre(160, 120, n), n) * (0.6 + 0.4 * seno(np.full(n, 33.0), n)), 3) * env(n, 0.005, 0.3) * 0.18
    chiado = passa(ruido(rng, n), 4000, 12000, 2) * env(n, 0.003, 0.25) * 0.25
    poe(x, _ziz(rng, 0.8, 1800, 11000, 0.012, 0.8) * env(n, 0.002, 0.35) + buzz + chiado, 0.12)
    poe(x, assobio(rng, n_de(0.5), 600, 3000, 0.7) * env(n_de(0.5), 0.01, 0.15) * 0.35, 0.12)
    return reverb(x, 0.45, 0.2)


def braco_namekiano(rng, v):
    x = _z(1.0)
    n = n_de(0.28)
    t = np.arange(n) / SR
    estica = seno(varre(140, 520, n, 0.7) * (1 + 0.04 * np.sin(2 * math.pi * 18 * t)), n) * sobe_e_some(n, 0.8, 1.4) * 0.3
    carne = passa(rosa(rng, n), 250, 1400, 2) * sobe_e_some(n, 0.6, 1.5) * (0.6 + 0.4 * np.sin(2 * math.pi * 23 * t)) * 0.5
    poe(x, estica + carne + _whoosh(rng, 0.28, 300, 1600, 0.85, g=0.4), 0)
    poe(x, B.soco_pesado(rng, v), 0.25, 1.0)
    n = n_de(0.22)
    t = np.arange(n) / SR
    volta = seno(varre(480, 160, n, 1.2) * (1 + 0.05 * np.sin(2 * math.pi * 20 * t)), n) * sobe_e_some(n, 0.4, 1.5) * 0.25
    poe(x, volta + passa(rosa(rng, n), 300, 1200, 2) * sobe_e_some(n, 0.5, 1.5) * 0.35, 0.58)
    poe(x, baque(n_de(0.12), 260, 150, 0.03, 0.4) * 0.3, 0.8)
    return reverb(x, 0.3, 0.14)


def punho_lendario(rng, v):
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.17, 150, 1500, 0.9, g=0.8), 0)
    poe(x, B.esmagar(rng, v), 0.14, 1.1)
    n = n_de(1.0)
    poe(x, satura(baque(n, 62, 26, 0.35, 0.6), 3.5) * 0.9, 0.14)
    ruge = satura(passa(rosa(rng, n), 60, 900, 2) * env(n, 0.01, 0.35), 3.0) * 0.6
    poe(x, ruge, 0.15)
    poe(x, graos(rng, n_de(0.8), 22, 0.0, 0.5, 400, 3000, 0.008) * 0.4, 0.2)
    return reverb(x, 0.7, 0.25, 3500)


def toque_da_destruicao(rng, v):
    x = _z(1.2)
    n = n_de(0.06)
    tic = estalo(rng, n, 4000, 14000, 0.002) * 0.9 + seno(np.full(n, 3200.0), n) * env(n, 0.0005, 0.008) * 0.4
    poe(x, tic, 0.08)
    n = n_de(0.55)
    t = np.arange(n) / SR
    hum = satura(seno(varre(70, 95, n), n) * (0.7 + 0.3 * np.sin(2 * math.pi * 7.5 * t)), 2.5) * sobe_e_some(n, 0.6, 1.2) * 0.35
    canta = seno(varre(nota(76), nota(88), n, 1.6), n) * sobe_e_some(n, 0.9, 2.0) * 0.08
    poe(x, hum + canta, 0.12)
    n = n_de(0.32)
    suga = passa(rosa(rng, n), 300, 8000, 2) * np.linspace(0, 1, n) ** 3 * 0.9
    suga = faixa_sobe(rng, n) * 0.6 + suga * 0.5
    poe(x, suga, 0.45)
    n = n_de(0.5)
    poe(x, baque(n, 90, 40, 0.06, 0.6) * 0.8 + estalo(rng, n, 800, 6000, 0.004) * 0.5, 0.77)
    poe(x, graos(rng, n_de(0.4), 14, 0.0, 0.3, 4000, 12000, 0.003) * np.linspace(1, 0, n_de(0.4)) * 0.3, 0.8)
    return reverb(x, 0.6, 0.18)


def faixa_sobe(rng, n):
    """Ruído cujo filtro desce do agudo ao grave enquanto cresce (algo sendo sugado)."""
    return assobio(rng, n, 9000, 300, 1.5, 0.5) * np.linspace(0, 1, n) ** 2.5


def rei_gun(rng, v):
    x = _z(1.0)
    n = n_de(0.17)
    carga = seno(varre(300, 1300, n, 0.8), n) * np.linspace(0.1, 1, n) * 0.2
    poe(x, carga + assobio(rng, n, 1500, 6000, 1.0) * np.linspace(0, 1, n) * 0.25, 0)
    n = n_de(0.3)
    pew = satura(seno(varre(950, 110, n, 0.35), n) * env(n, 0.001, 0.09), 2.2) * 0.65
    poe(x, pew + baque(n, 120, 55, 0.08, 0.5) * 0.6 + estalo(rng, n, 1500, 7000, 0.006) * 0.5, 0.16)
    poe(x, _whoosh(rng, 0.14, 800, 3000, 0.9, g=0.35), 0.17)
    poe(x, B.impacto_energia(rng, v), 0.3, 1.0)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 200, 2500, 2) * env(n, 0.01, 0.15) * 0.45, 0.31)
    return reverb(x, 0.5, 0.22)


def soco_casual(rng, v):
    x = _z(1.55)
    poe(x, B.soco_leve(rng, v), 0, 0.8)
    n = n_de(1.15)
    vento = assobio(rng, n, 5500, 140, 0.55, 0.6) * env(n, 0.03, 0.45) * 1.2
    vento += passa(rosa(rng, n), 60, 500, 2) * env(n, 0.02, 0.4) * 0.6
    poe(x, vento, 0.4)
    poe(x, baque(n_de(0.9), 55, 28, 0.4, 0.3) * 1.1, 0.38)
    poe(x, graos(rng, n_de(0.9), 40, 0.05, 0.7, 800, 4500, 0.005) * 0.25, 0.45)
    return reverb(x, 0.8, 0.28, 4000)


def infinito(rng, v):
    x = _z(1.25)
    poe(x, _whoosh(rng, 0.18, 400, 2600, 0.95, g=0.6), 0)
    n = n_de(0.55)
    t = np.arange(n) / SR
    # tempo esticado: o tom desce e o tremolo vai ficando lento
    trem = 0.6 + 0.4 * np.sin(2 * math.pi * np.cumsum(np.linspace(22, 3, n)) / SR)
    estica = seno(varre(520, 70, n, 0.6), n) * trem * env(n, 0.01, 0.4) * 0.35
    abafado = passa(rosa(rng, n), 60, 450, 2) * trem * env(n, 0.02, 0.35) * 0.5
    brilho = modal(n, 1600, rng=rng, **CRISTAL) * env(n, 0.002, 0.3) * 0.08 * (1 - t / t[-1])
    poe(x, estica + abafado + brilho, 0.16)
    n = n_de(0.08)
    poe(x, estalo(rng, n, 2500, 12000, 0.004) * 1.1 + seno(np.full(n, 1800.0), n) * env(n, 0.0005, 0.01) * 0.3, 0.7)
    n = n_de(0.5)
    poe(x, baque(n, 110, 45, 0.12, 0.3) * 0.8 + assobio(rng, n, 400, 2500, 0.6) * env(n, 0.005, 0.15) * 0.5, 0.71)
    return reverb(x, 0.6, 0.25)


def punho_amaldicoado(rng, v):
    x = _z(0.9)
    poe(x, _whoosh(rng, 0.11, 600, 3000, 0.9, g=0.5), 0)
    poe(x, B.soco_pesado(rng, v), 0.09, 1.0)
    n = n_de(0.5)
    crack = satura(passa(ruido(rng, n), 800, 9000, 2) * env(n, 0.0005, 0.03), 6) * 0.6
    # "bit crush": amostra-e-segura, o espaço quebrado
    passo = 14
    q = _ziz(rng, 0.5, 300, 6000, 0.01, 0.9) * env(n, 0.002, 0.12)
    q = np.repeat(q[::passo], passo)[:n]
    q = np.round(q * 6) / 6
    grave = satura(seno(varre(90, 45, n), n), 5) * env(n, 0.002, 0.15) * 0.4
    poe(x, crack + q * 0.5 + grave, 0.095)
    return reverb(x, 0.45, 0.2)


def desmanche(rng, v):
    x = _z(0.9)
    tempos = np.cumsum([0.0] + list(rng.uniform(0.018, 0.034, 8)))
    for k, t0 in enumerate(tempos):
        n = n_de(0.2)
        shink = passa(ruido(rng, n), 4500, 14000, 2) * env(n, 0.0005, 0.012) * 0.8
        shink += modal(n, rng.uniform(3500, 6500), rng=rng, **METAL) * env(n, 0.0005, 0.05) * 0.18
        shink += seno(varre(rng.uniform(6000, 8000), rng.uniform(2500, 3500), n, 0.5), n) * env(n, 0.0005, 0.03) * 0.06
        poe(x, shink, 0.02 + t0, rng.uniform(0.7, 1.0))
    poe(x, _whoosh(rng, 0.35, 2000, 8000, 0.3, g=0.25), 0.0)
    return reverb(x, 0.4, 0.2)


def choque_do_pikachu(rng, v):
    x = _z(1.0)
    poe(x, estalo(rng, n_de(0.05), 2000, 12000, 0.003) * 0.9, 0.02)
    n = n_de(0.8)
    t = np.arange(n) / SR
    zz = _ziz(rng, 0.8, 2000, 14000, 0.004, 0.9)
    zz *= (0.55 + 0.45 * np.sin(2 * math.pi * 31 * t) ** 2) * env(n, 0.005, 0.35, segura=0.25)
    buzz = satura(seno(np.full(n, 330.0) * (1 + 0.02 * np.sin(2 * math.pi * 9 * t)), n), 3) * env(n, 0.01, 0.3, segura=0.2) * 0.14
    chi = passa(ruido(rng, n), 6000, 15000, 2) * env(n, 0.005, 0.3) * 0.15
    poe(x, zz + buzz + chi, 0.03)
    poe(x, graos(rng, n_de(0.7), 35, 0.0, 0.6, 3000, 12000, 0.003) * 0.5, 0.05)
    return reverb(x, 0.35, 0.16)


def soco_relampago(rng, v):
    x = _z(1.1)
    n = n_de(0.16)
    zum = seno(varre(1800, 7500, n, 0.6), n) * sobe_e_some(n, 0.85, 1.5) * 0.18
    poe(x, zum + _whoosh(rng, 0.16, 2000, 10000, 0.9, g=0.7), 0)
    poe(x, estalo(rng, n_de(0.2), 800, 9000, 0.006) * 1.0 + baque(n_de(0.2), 130, 60, 0.05, 0.5) * 0.4, 0.15)
    t0, k = 0.18, 0
    while t0 < 0.58 and k < 30:
        poe(x, B.soco_leve(rng, v)[: n_de(0.1)] * env(n_de(0.1), 0.0005, 0.03), t0, rng.uniform(0.8, 1.1))
        t0 += max(0.015, rng.uniform(0.022, 0.032))
        k += 1
    poe(x, _ziz(rng, 0.45, 2000, 12000, 0.01, 0.35) * env(n_de(0.45), 0.01, 0.2), 0.16)
    poe(x, B.soco_pesado(rng, v), 0.6, 1.0)
    return reverb(x, 0.4, 0.18)


SONS.update({
    "ki-dourado": (ki_dourado, "básico de Goku: três disparos de ki \"fwip\" e os estouros com baforada"),
    "rajada-continua": (rajada_continua, "básico de Vegeta: rajada metralhada de ki com ronco crescente e explosão"),
    "golpe-do-potencial": (golpe_do_potencial, "básico de Gohan: soco pesado com chiado elétrico do SSJ2"),
    "braco-namekiano": (braco_namekiano, "básico de Piccolo: esticar elástico e orgânico, pancada e o braço voltando"),
    "punho-lendario": (punho_lendario, "básico de Broly: soco grave, saturado e esmagador, com pedras caindo"),
    "toque-da-destruicao": (toque_da_destruicao, "básico de Beerus: \"tic\" do peteleco, zumbido da esfera e implosão sugada"),
    "rei-gun": (rei_gun, "básico de Yusuke: carga curta e o disparo \"pew\" grave do Rei Gun"),
    "soco-casual": (soco_casual, "básico de Saitama: soco seco, pausa e o vendaval \"whoosh\""),
    "infinito": (infinito, "básico de Gojo: o tempo esticando abafado e o estalo do pulso"),
    "punho-amaldicoado": (punho_amaldicoado, "básico de Yuji: impacto com estalo distorcido do Black Flash"),
    "desmanche": (desmanche, "básico de Sukuna: vários \"shink\" agudos rapidíssimos"),
    "choque-do-pikachu": (choque_do_pikachu, "básico de Pikachu: choque elétrico crepitante agudo"),
    "soco-relampago": (soco_relampago, "básico de Flash: zunido supersônico e uma série de socos ultrarrápidos"),
})
