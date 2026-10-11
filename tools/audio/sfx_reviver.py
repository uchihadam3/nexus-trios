"""Os sons do reviver de cada um (veja tools/vfx/familias_v2/reviver_proprio.py): quem levanta um
aliado caído toca o som dele, no volume dos golpes.

Hades ........ o ronco do submundo, os sussurros das almas subindo e o acorde quente dos Elísios.
Feiticeira ... a magia do caos ondulando (tons tremendo), os estalos e a realidade estalando de volta.
Pain ......... as almas caindo do céu como cometas (assobios que descem, um a um) e o eco grave.
Rick ......... o "vuorp" do portal girando, os bipes do escaneamento e o portal fechando.
Constantine .. o fósforo riscando e o cigarro, o canto grave do ritual e o clarão do pacto.
She-Ra ....... a espada descendo no ar, o metal cravando no chão e o acorde heroico subindo.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _whoosh, _z
from som import METAL, SR, baque, env, estalo, modal, n_de, passa, poe, reverb, rosa, satura, seno, serra_suave, sobe_e_some, varre
from som import CENTROS, assobio, faixas, ruido

nota = B.nota


def _t(n):
    return np.arange(n) / SR


def _acorde(raiz, ivs, seg, g=0.12, filtro=1800, ataque=0.04, harm=8):
    n = n_de(seg)
    x = sum(serra_suave(nota(raiz + iv) * (1 + 0.002 * k), n, harm) / (1 + 0.3 * k) for k, iv in enumerate(ivs))
    return passa(x, None, filtro, 2) * env(n, ataque, seg * 0.6) * g


def levanta_hadescz(rng, v):
    x = np.zeros(n_de(1.4))
    n = n_de(1.0)
    ronco = passa(serra_suave(np.full(n, 41.2), n, 10) + serra_suave(np.full(n, 43.6), n, 10), None, 400, 2) * sobe_e_some(n, 0.4, 1.4) * 0.35
    poe(x, ronco, 0.0)
    for k in range(4):
        m = n_de(0.5)
        sussurro = faixas(rosa(rng, m), CENTROS, varre(500 + 150 * k, 2200, m, 1.3), 0.35) * sobe_e_some(m, 0.6, 1.5) * 0.3
        poe(x, sussurro, 0.1 + 0.1 * k)
    poe(x, _acorde(64, (0, 4, 7, 12), 0.8, 0.16, 2600, 0.08), 0.55)
    return reverb(x, 0.75, 0.38, 4500)


def levanta_scarletwitch(rng, v):
    x = np.zeros(n_de(1.3))
    n = n_de(0.7)
    t = _t(n)
    for k, f0 in enumerate((330, 415, 494)):
        f = f0 * (1 + 0.06 * np.sin(2 * math.pi * (5 + 2 * k) * t + k))
        poe(x, (seno(f, n) * 0.6 + seno(f * 1.5, n) * 0.2) * sobe_e_some(n, 0.7, 1.6) * 0.09, 0.0)
    for k in range(7):
        poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.01) * 0.35, 0.08 + 0.07 * k + rng.uniform(0, 0.03))
    m = n_de(0.3)
    poe(x, assobio(rng, m, 400, 5000, 2.0) * np.linspace(0, 1, m) ** 3 * 0.6, 0.38)
    poe(x, estalo(rng, n_de(0.05), 800, 6000, 0.02) * 0.9, 0.68)
    poe(x, baque(n_de(0.5), 90, 40, 0.15, 0.3) * 0.8, 0.68)
    return reverb(x, 0.6, 0.3, 5000)


def levanta_pain(rng, v):
    x = np.zeros(n_de(1.5))
    for k in range(6):
        m = n_de(0.35)
        f0 = 1400 - 80 * k
        poe(x, seno(varre(f0, f0 * 0.45, m, 0.8), m) * env(m, 0.03, 0.25) * 0.08, 0.02 + 0.08 * k)
        poe(x, assobio(rng, m, 3000, 600, 0.8) * sobe_e_some(m, 0.8, 1.5) * 0.18, 0.02 + 0.08 * k)
        poe(x, baque(n_de(0.2), 110, 60, 0.05, 0.1) * 0.25, 0.3 + 0.08 * k)
    n = n_de(0.9)
    eco = modal(n, 82, razoes=[1, 2.0, 2.76, 3.9], quedas=[0.9, 0.6, 0.4, 0.25], ganhos=[1, 0.5, 0.3, 0.15]) * 0.4
    poe(x, passa(eco, None, 1500, 2), 0.62)
    return reverb(x, 0.7, 0.35, 4000)


def levanta_rick(rng, v):
    x = np.zeros(n_de(1.3))
    n = n_de(0.75)
    t = _t(n)
    f = 110 * (1 + 0.5 * np.sin(2 * math.pi * 6 * t) * np.linspace(1, 0.3, n))
    vuorp = faixas(serra_suave(f, n, 12), CENTROS, 600 + 1500 * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * t)), 0.5)
    poe(x, satura(vuorp, 1.5) * sobe_e_some(n, 0.3, 1.3) * 0.35, 0.0)
    for k in range(5):
        m = n_de(0.05)
        poe(x, seno(np.full(m, 1800 + 300 * (k % 2)), m) * env(m, 0.003, 0.03) * 0.12, 0.38 + 0.06 * k)
    m = n_de(0.25)
    poe(x, seno(varre(900, 120, m, 1.5), m) * env(m, 0.005, 0.18) * 0.25 + assobio(rng, m, 3000, 300, 1.5) * env(m, 0.005, 0.15) * 0.3, 0.8)
    return reverb(x, 0.45, 0.22, 6000)


def levanta_constantine(rng, v):
    x = np.zeros(n_de(1.5))
    poe(x, estalo(rng, n_de(0.05), 2000, 8000, 0.015) * 0.5, 0.0)
    m = n_de(0.35)
    poe(x, passa(ruido(rng, m), 1500, 7000, 2) * env(m, 0.01, 0.25) * 0.25, 0.03)
    n = n_de(0.9)
    canto = _acorde(45, (0, 3, 7), 0.9, 0.18, 900, 0.15)
    poe(x, canto, 0.15)
    poe(x, faixas(rosa(rng, n), CENTROS, np.full(n, 500.0), 0.3) * sobe_e_some(n, 0.6, 1.4) * 0.2, 0.15)
    m = n_de(0.35)
    poe(x, assobio(rng, m, 300, 4000, 2.0) * np.linspace(0, 1, m) ** 2 * 0.5, 0.45)
    poe(x, baque(n_de(0.6), 100, 40, 0.2, 0.3) * 0.8, 0.78)
    poe(x, _acorde(57, (0, 7, 12), 0.6, 0.12, 3000, 0.01), 0.78)
    return reverb(x, 0.7, 0.35, 4500)


def levanta_shera(rng, v):
    x = np.zeros(n_de(1.4))
    m = n_de(0.35)
    poe(x, assobio(rng, m, 4000, 900, 1.2) * np.linspace(0.2, 1, m) ** 2 * 0.5, 0.0)
    n = n_de(0.9)
    poe(x, modal(n, 520, rng=rng, **METAL) * env(n, 0.001, 0.5) * 0.35, 0.32)
    poe(x, baque(n_de(0.4), 120, 55, 0.12, 0.35) * 0.7, 0.32)
    for k, (iv, d) in enumerate(((0, 0.0), (7, 0.12), (12, 0.24))):
        poe(x, _acorde(55 + iv, (0, 4, 7), 0.6 - 0.1 * k, 0.1, 3500, 0.02, 10), 0.4 + d)
    return reverb(x, 0.65, 0.32, 6500)


SONS: dict = {
    "levanta-hadescz": (levanta_hadescz, "Hades revive: o submundo, as almas e os Elísios"),
    "levanta-scarletwitch": (levanta_scarletwitch, "Feiticeira revive: a magia do caos e o estalo"),
    "levanta-pain": (levanta_pain, "Pain revive: as almas caindo do céu (Rinne Tensei)"),
    "levanta-rick": (levanta_rick, "Rick revive: o portal, o escaneamento e o portal fechando"),
    "levanta-constantine": (levanta_constantine, "Constantine revive: o fósforo, o ritual e o pacto"),
    "levanta-shera": (levanta_shera, "She-Ra revive: a espada crava e o acorde heroico"),
}
ALVO = {nome: -15 for nome in SONS}
_ = _whoosh, _z
