"""Sons dos ataques básicos, lote c (veja tools/vfx/familias_v2/basicos_c.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _boing, _brilho, _faiscas, _tom, _whoosh, _z, nota  # noqa: F401
from som import (CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, graos, modal, n_de, passa, poe,  # noqa: F401
                 reverb, rosa, ruido, satura, seno, sobe_e_some, varre)


# ------------------------------------------------------------------ ajudantes
def _serra(f, n, harm=10):
    f = np.broadcast_to(np.asarray(f, float), (n,))
    fase = 2 * math.pi * np.cumsum(f) / SR
    return sum(np.sin(k * fase) / k for k in range(1, harm + 1)) * 0.6


def _clique(rng, f=3200, queda=0.0025, g=1.0):
    """Clique mecânico: estalo curtíssimo com uma ressonância aguda."""
    n = n_de(0.03)
    t = np.arange(n) / SR
    return (passa(ruido(rng, n), 1500, 9000, 2) * env(n, 0.0002, queda) * 0.8
            + np.sin(2 * math.pi * f * t) * np.exp(-t / (queda * 1.6)) * 0.6) * g


def _pingo(rng, f0, g=0.1):
    """Gota pingando: um "plip" com o tom subindo rápido (bolha), curtinho."""
    n = n_de(0.06)
    return seno(varre(f0, f0 * 1.9, n, 2.0), n) * env(n, 0.001, 0.014) * g


def _chiado(rng, seg, lo, hi, ataque=0.01, queda=0.1, g=0.3):
    n = n_de(seg)
    return passa(ruido(rng, n), lo, hi, 2) * env(n, ataque, queda) * g


# ------------------------------------------------------------------ Gon
def jajanken(rng, v):
    """Jajanken: a aura carregando (zumbido que sobe e treme), o ar puxado, e o soco que
    estoura com um baque grande e pedrinhas caindo."""
    x = _z(1.35)
    n = n_de(0.55)
    t = np.arange(n) / SR
    f = varre(nota(40), nota(55), n, 0.8)
    zumbe = passa(_serra(f * (1 + 0.012 * np.sin(2 * math.pi * 9 * t)), n, 12), 80, 4000, 2)
    poe(x, zumbe * sobe_e_some(n, 0.92, 1.2) * 0.6, 0.0)
    poe(x, assobio(rng, n, 300, 3500, 0.7) * sobe_e_some(n, 0.95, 1.6) * 0.8, 0.0)
    poe(x, _faiscas(rng, n, 10, 60, 2500, 9000, 0.5) * np.linspace(0, 1, n) * 0.25, 0.0)
    poe(x, _whoosh(rng, 0.14, 500, 4000, 0.85, g=0.6), 0.42)
    poe(x, B.soco_pesado(rng, v) * 1.1, 0.53)
    poe(x, baque(n_de(0.8), 85, 32, 0.3, 0.6) * 0.9, 0.53)
    m = n_de(0.7)
    poe(x, satura(passa(rosa(rng, m), 120, 2500, 2) * env(m, 0.002, 0.16), 2.0) * 0.6, 0.53)
    poe(x, graos(rng, n_de(0.7), 22, 0.05, 0.55, 900, 5000, 0.007) * 0.35, 0.55)
    return reverb(x, 0.55, 0.22, 6000)


# ------------------------------------------------------------------ Killua
def garras_de_killua(rng, v):
    """Garras de Killua: três cortes rapidíssimos (fio agudo), cada um com um estalo de choque,
    e o crepitar elétrico zumbindo depois."""
    x = _z(1.0)
    for k, t0 in enumerate((0.0, 0.075, 0.15)):
        poe(x, _whoosh(rng, 0.07, 2000, 8000, 0.85, g=0.45), t0)
        poe(x, _chiado(rng, 0.08, 3000, 11000, 0.0005, 0.018, 0.75), t0 + 0.055)
        poe(x, B._lamina_curta(rng, n_de(0.12), rng.uniform(3000, 3800)) * 0.12, t0 + 0.055)
        poe(x, _faiscas(rng, n_de(0.12), 300, 80, 1200, 10000, 1.0) * 0.55, t0 + 0.055)
    n = n_de(0.6)
    t = np.arange(n) / SR
    zum = satura(_serra(rng.uniform(110, 130) * (1 + 0.02 * np.sin(2 * math.pi * 23 * t)), n, 14), 2.5)
    cint = np.clip(passa(ruido(rng, n), None, 35, 2) * 12 + 0.4, 0, 1)
    poe(x, passa(zum * cint, 150, 6000, 2) * env(n, 0.005, 0.18) * 0.18, 0.2)
    poe(x, _faiscas(rng, n, 120, 15, 1500, 11000, 0.8) * env(n, 0.002, 0.25) * 0.5, 0.2)
    return reverb(x, 0.35, 0.15, 9000)


# ------------------------------------------------------------------ Edward
def punho_transmutado(rng, v):
    """Punho transmutado: as mãos batem no chão (tapa), a reação de alquimia estala em arcos
    azuis com um zumbido que sobe, a pedra se ergue roncando e acerta com um baque de rocha;
    no fim, cascalho caindo."""
    x = _z(1.35)
    poe(x, B._tapa(rng, n_de(0.1), 900, 4500, 0.012) * 0.7, 0.0)
    n = n_de(0.5)
    t = np.arange(n) / SR
    poe(x, _faiscas(rng, n, 90, 260, 1500, 11000, 1.0) * sobe_e_some(n, 0.7, 0.6) * 1.4, 0.02)
    f = varre(nota(50), nota(62), n, 1.0)
    poe(x, passa(satura(_serra(f, n, 12), 2.0), 200, 6000, 2) * sobe_e_some(n, 0.8, 1.2) * 0.25, 0.02)
    poe(x, _brilho(rng, 0.4, nota(88), 0.08), 0.05)
    m = n_de(0.32)
    ronco = passa(rosa(rng, m), 60, 700, 2) * np.linspace(0.2, 1, m) ** 1.5 * 0.9
    poe(x, satura(ronco, 2.0) * 0.7, 0.28)
    poe(x, graos(rng, m, 30, 0.0, 0.3, 500, 3500, 0.008) * 0.4, 0.28)
    poe(x, B.soco_pesado(rng, v), 0.55)
    poe(x, baque(n_de(0.6), 95, 40, 0.18, 0.5) * 0.8, 0.55)
    poe(x, _chiado(rng, 0.2, 600, 3000, 0.001, 0.04, 0.5), 0.55)
    poe(x, graos(rng, n_de(0.8), 28, 0.25, 0.75, 700, 4500, 0.008) * 0.4, 0.55)
    return reverb(x, 0.5, 0.2, 7000)


# ------------------------------------------------------------------ Roy
def estalo_de_dedos(rng, v):
    """Estalo de dedos: o "snap" seco da luva, o chiado da faísca correndo pelo ar e a
    explosão de chamas que ruge e crepita."""
    x = _z(1.35)
    n = n_de(0.05)
    t = np.arange(n) / SR
    snap = passa(ruido(rng, n), 1800, 7000, 2) * env(n, 0.0002, 0.004) * 1.2
    snap += np.sin(2 * math.pi * 1250 * t) * np.exp(-t / 0.006) * 0.35
    poe(x, snap, 0.0)
    poe(x, _clique(rng, 4200, 0.002, 0.4), 0.004)
    m = n_de(0.3)
    sibilo = assobio(rng, m, 2500, 7000, 1.0, 0.35) * np.linspace(0.3, 1, m) * 0.35
    poe(x, sibilo + _faiscas(rng, m, 60, 200, 2500, 9000, 0.4) * 0.3, 0.04)
    poe(x, B.explosao(rng, v) * 0.85, 0.32)
    poe(x, B.fogo(rng, v) * 0.8, 0.3)
    k = n_de(0.25)
    poe(x, passa(rosa(rng, k), 300, 3000, 2) * env(k, 0.004, 0.06) * 0.6, 0.32)    # o "fuuf" do ar pegando fogo
    return reverb(x, 0.5, 0.2, 6500)


# ------------------------------------------------------------------ Guts
def matadora_de_dragoes(rng, v):
    """Matadora de Dragões: o ar pesado cortado por uma placa de ferro enorme (whoosh grave e
    lento), o choque de ferro bruto (clang abafado e grave, sem brilho de espada fina) e o
    baque que treme o chão, com faíscas e entulho."""
    x = _z(1.4)
    n = n_de(0.34)
    poe(x, assobio(rng, n, 120, 1100, 1.6, 0.6) * sobe_e_some(n, 0.85, 1.6) * 1.0, 0.0)
    poe(x, passa(rosa(rng, n), 40, 200, 2) * sobe_e_some(n, 0.9, 2.0) * 0.6, 0.0)
    t0 = 0.32
    poe(x, B.esmagar(rng, v) * 0.9, t0)
    poe(x, baque(n_de(0.9), 70, 28, 0.35, 0.7) * 1.1, t0)
    m = n_de(0.9)
    clang = modal(m, rng.uniform(150, 175), rng=rng, desafina=0.02, **METAL) * env(m, 0.001, 0.22)
    clang += modal(m, rng.uniform(610, 680), rng=rng, desafina=0.03, **METAL) * env(m, 0.001, 0.08) * 0.5
    poe(x, satura(passa(clang, 100, 4000, 2), 1.8) * 0.45, t0)
    poe(x, _chiado(rng, 0.15, 1500, 7000, 0.0005, 0.02, 0.6), t0)
    poe(x, graos(rng, n_de(0.6), 35, 0.0, 0.4, 2500, 10000, 0.003) * 0.3, t0 + 0.01)
    poe(x, graos(rng, n_de(0.9), 26, 0.1, 0.8, 500, 3000, 0.009) * 0.35, t0 + 0.05)
    return reverb(x, 0.7, 0.26, 5000)


# ------------------------------------------------------------------ Jotaro
def soco_do_stand(rng, v):
    """Soco do Stand: um sopro fantasma que puxa o ar ao contrário, o soco pesado e seco e o
    eco espectral: o mesmo golpe repetindo, mais longe e abafado, sobre um coro de tons
    desafinados que somem."""
    x = _z(1.4)
    n = n_de(0.28)
    rev = reverb(assobio(rng, n, 600, 3000, 1.0, 0.5) * env(n, 0.002, 0.08), 0.8, 0.8)[::-1]
    poe(x, rev * np.linspace(0, 1, n) ** 1.5 * 0.6, 0.0)
    poe(x, _whoosh(rng, 0.12, 400, 3500, 0.85, g=0.5), 0.14)
    golpe = B.soco_pesado(rng, v)
    poe(x, golpe * 1.1, 0.25)
    poe(x, baque(n_de(0.5), 90, 40, 0.15, 0.4) * 0.6, 0.25)
    for k, (dt, g, corte) in enumerate(((0.16, 0.45, 2500), (0.32, 0.28, 1500), (0.5, 0.16, 900))):
        poe(x, passa(golpe, 120, corte, 2) * g, 0.25 + dt)
    m = n_de(1.1)
    t = np.arange(m) / SR
    coro = sum(seno(np.full(m, nota(mm)) * (1 + 0.006 * np.sin(2 * math.pi * (3.5 + k * 1.3) * t)), m) for k, mm in enumerate((57, 58, 64, 70)))
    poe(x, coro * env(m, 0.05, 0.35) * 0.05, 0.27)
    return reverb(x, 0.85, 0.42, 5500)


# ------------------------------------------------------------------ Giorno
def soco_da_vida(rng, v):
    """Soco da vida: o soco e, dele, a vida brotando: madeira estalando e esticando, folhas
    se abrindo (farfalhar), um arpejo dourado de sinos que sobe e um "plic" quando a
    joaninha pousa."""
    x = _z(1.4)
    poe(x, B.soco_leve(rng, v) * 1.1, 0.0)
    m = n_de(0.7)
    t = np.arange(m) / SR
    estica = passa(ruido(rng, m), 300, 1800, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * varre(18, 40, m) * t)) ** 4
    poe(x, estica * sobe_e_some(m, 0.4, 1.0) * 0.25, 0.12)
    poe(x, graos(rng, m, 26, 0.0, 0.55, 600, 3500, 0.006, 0.6) * 0.45, 0.12)              # galhos rangendo
    poe(x, passa(rosa(rng, m), 3000, 10000, 2) * sobe_e_some(m, 0.5, 1.3) * 0.18, 0.2)     # folhas
    for k, mm in enumerate((76, 79, 83, 88, 91)):
        poe(x, _brilho(rng, 0.6, nota(mm), 0.07, SINO), 0.14 + 0.07 * k)
    poe(x, _boing(0.12, nota(84), 0.12), 0.5)
    poe(x, _brilho(rng, 0.8, nota(96), 0.05, CRISTAL), 0.52)
    return reverb(x, 0.65, 0.3, 9000)


# ------------------------------------------------------------------ Power
def pancada_de_sangue(rng, v):
    """Pancada de sangue: o martelo pesado zunindo, a pancada molhada (baque + esguicho que
    "chapinha") e as gotas pingando em volta."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.26, 250, 2500, 0.85, g=0.75), 0.0)
    t0 = 0.26
    poe(x, B.soco_pesado(rng, v) * 1.0, t0)
    poe(x, baque(n_de(0.5), 80, 38, 0.16, 0.5) * 0.7, t0)
    m = n_de(0.35)
    t = np.arange(m) / SR
    molhado = ruido(rng, m)
    # o "splash": banda que desce rápido (o esguicho abrindo) com um borbulhar
    banda = sum(passa(molhado, c / 1.4, c * 1.4, 2) * np.exp(-((np.log2(varre(2400, 350, m, 0.6)) - math.log2(c)) / 0.5) ** 2)
                for c in (300, 500, 800, 1300, 2000, 3000))
    poe(x, satura(banda * env(m, 0.001, 0.09) * (1 + 0.5 * np.sin(2 * math.pi * 31 * t)), 1.6) * 0.8, t0)
    poe(x, B._carne(rng, n_de(0.2), 0.06, 3.0) * 0.9, t0)
    for _ in range(11):
        poe(x, _pingo(rng, rng.uniform(700, 1500), rng.uniform(0.05, 0.12)), t0 + rng.uniform(0.08, 0.7))
    return reverb(x, 0.4, 0.16, 6000)


# ------------------------------------------------------------------ Makima
def dedo_apontado(rng, v):
    """Dedo apontado: um silêncio que pesa (ronco grave que cresce e o ar sendo puxado), e um
    "bang" abafado e seco, sem eco de arma; fica um acorde dissonante grave, sinistro, e
    respingos."""
    x = _z(1.4)
    n = n_de(0.32)
    t = np.arange(n) / SR
    ronco = satura(_serra(np.full(n, 48.0) * (1 + 0.01 * np.sin(2 * math.pi * 5 * t)), n, 8), 1.5)
    poe(x, passa(ronco, 40, 600, 2) * np.linspace(0, 1, n) ** 2 * 0.35, 0.0)
    poe(x, assobio(rng, n, 400, 2200, 0.6, 0.5) * np.linspace(0, 1, n) ** 2.5 * 0.35, 0.0)
    t0 = 0.32
    m = n_de(0.4)
    bang = passa(ruido(rng, m), 80, 1400, 2) * env(m, 0.0004, 0.045)
    poe(x, satura(bang * 2.2, 2.5) * 0.7, t0)
    poe(x, baque(n_de(0.5), 75, 35, 0.12, 0.8) * 1.0, t0)
    poe(x, B._tapa(rng, n_de(0.05), 800, 3000, 0.006) * 0.5, t0)
    k = n_de(1.1)
    tt = np.arange(k) / SR
    acorde = sum(seno(np.full(k, nota(mm)) * (1 + 0.003 * np.sin(2 * math.pi * 0.7 * tt + mm)), k) for mm in (38, 39, 45))
    poe(x, passa(acorde, 50, 1200, 2) * env(k, 0.03, 0.45) * 0.12, t0 + 0.02)
    for _ in range(7):
        poe(x, _pingo(rng, rng.uniform(500, 900), rng.uniform(0.03, 0.06)), t0 + rng.uniform(0.1, 0.5))
    return reverb(x, 0.6, 0.18, 4000)


# ------------------------------------------------------------------ Frieren
def feitico_comum(rng, v):
    """Zoltraak: o círculo mágico acende (arpejo de cristal e um brilho que gira), o feixe
    dispara num "piuu" limpo com zumbido de energia e acerta com um estalo de luz."""
    x = _z(1.4)
    for k, mm in enumerate((84, 88, 91, 95)):
        poe(x, _brilho(rng, 0.5, nota(mm), 0.08, CRISTAL), 0.0 + 0.045 * k)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 5000, 12000, 2) * sobe_e_some(n, 0.8, 1.5) * 0.12, 0.0)
    t0 = 0.24
    m = n_de(0.25)
    piu = seno(varre(2600, 520, m, 0.5), m) * env(m, 0.001, 0.09) * 0.3
    piu += seno(varre(5200, 1040, m, 0.5), m) * env(m, 0.001, 0.05) * 0.1
    poe(x, piu, t0)
    k = n_de(0.3)
    tt = np.arange(k) / SR
    feixe = passa(_serra(np.full(k, 220.0) * (1 + 0.01 * np.sin(2 * math.pi * 40 * tt)), k, 12), 200, 6000, 2)
    poe(x, feixe * env(k, 0.005, 0.1) * 0.12, t0)
    poe(x, _chiado(rng, 0.2, 2000, 9000, 0.001, 0.05, 0.3), t0)
    poe(x, B.impacto_energia(rng, v) * 0.8, t0 + 0.1)
    poe(x, _brilho(rng, 0.8, nota(100), 0.06, CRISTAL), t0 + 0.1)
    return reverb(x, 0.6, 0.28, 10000)


# ------------------------------------------------------------------ Anya
def golpe_de_panico(rng, v):
    """Golpe de pânico: tapinhas rápidos e desajeitados (com assobios de desenho), um "boing"
    de mola e o tilintar das estrelinhas tontas."""
    x = _z(1.3)
    for k, t0 in enumerate((0.0, 0.07, 0.15, 0.24)):
        poe(x, _whoosh(rng, 0.05, 1500, 5000, 0.8, g=0.25), t0)
        poe(x, B._tapa(rng, n_de(0.08), 1500, 6500, 0.01) * 0.9, t0 + 0.04)
        poe(x, B._carne(rng, n_de(0.08), 0.02) * 0.35, t0 + 0.04)
        m = n_de(0.06)
        poe(x, seno(varre(nota(84 + 2 * k), nota(90 + 2 * k), m), m) * env(m, 0.002, 0.02) * 0.08, t0 + 0.04)
    poe(x, _boing(0.45, nota(55), 0.3), 0.34)
    m = n_de(0.3)
    poe(x, seno(varre(nota(91), nota(79), m, 1.0), m) * env(m, 0.005, 0.12) * 0.07, 0.3)     # apito que cai
    for k, mm in enumerate((96, 100, 98, 103)):
        poe(x, _brilho(rng, 0.3, nota(mm), 0.06, SINO), 0.58 + 0.08 * k)
    return reverb(x, 0.35, 0.14, 9000)


# ------------------------------------------------------------------ Loid
def golpe_do_espiao(rng, v):
    """Golpe do espião: os cliques da mira travando (tic… tic-tic e um bipe curto), um sopro
    rápido e o golpe de mão seco e preciso, com um brilho fino no fim."""
    x = _z(1.0)
    poe(x, _clique(rng, 3000, 0.002, 0.6), 0.0)
    poe(x, _clique(rng, 3300, 0.002, 0.5), 0.12)
    poe(x, _clique(rng, 3600, 0.002, 0.6), 0.17)
    m = n_de(0.07)
    poe(x, seno(np.full(m, 2350.0), m) * env(m, 0.001, 0.025) * 0.12, 0.2)
    poe(x, _whoosh(rng, 0.09, 1500, 7000, 0.9, g=0.55), 0.26)
    t0 = 0.34
    poe(x, B._tapa(rng, n_de(0.1), 1300, 6000, 0.008) * 1.2, t0)
    poe(x, B._carne(rng, n_de(0.12), 0.03, 2.6) * 0.9, t0)
    poe(x, B._baque_seco(rng, n_de(0.2), 120, 0.05) * 0.6, t0)
    poe(x, _brilho(rng, 0.4, nota(98), 0.06, VIDRO), t0 + 0.02)
    return reverb(x, 0.25, 0.1, 9000)


# ------------------------------------------------------------------ Yor
def agulha_de_espinho(rng, v):
    """Agulha de espinho: dois "tsk" afiados (o estilete cortando o ar e cravando com um
    tilintar de aço fino) e depois um sussurro de ar e pétalas que se assenta."""
    x = _z(1.4)
    for t0, f in ((0.0, 3400), (0.09, 3900)):
        poe(x, _whoosh(rng, 0.1, 3000, 9000, 0.9, g=0.35), t0)
        poe(x, _chiado(rng, 0.05, 4000, 12000, 0.0003, 0.008, 0.9), t0 + 0.09)
        poe(x, B._carne(rng, n_de(0.06), 0.015) * 0.35, t0 + 0.09)
        m = n_de(0.35)
        poe(x, modal(m, f, rng=rng, **METAL) * env(m, 0.0005, 0.06) * 0.08, t0 + 0.09)
    n = n_de(0.9)
    t = np.arange(n) / SR
    sopro = passa(rosa(rng, n), 1800, 7000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 2.3 * t) ** 2)
    poe(x, sopro * sobe_e_some(n, 0.3, 1.4) * 0.22, 0.28)
    poe(x, graos(rng, n, 18, 0.1, 0.8, 3000, 9000, 0.005, 0.8) * 0.12, 0.28)
    return reverb(x, 0.55, 0.25, 9000)


# nome do arquivo (com hífen) → (função, descrição)
SONS: dict = {
    "jajanken": (jajanken, "básico de Gon: aura carregando que sobe e soco que estoura com pedrinhas"),
    "garras-de-killua": (garras_de_killua, "básico de Killua: três cortes rápidos com estalos de choque e crepitar elétrico"),
    "punho-transmutado": (punho_transmutado, "básico de Edward: estalo azul de transmutação, pedra roncando e baque de rocha"),
    "estalo-de-dedos": (estalo_de_dedos, "básico de Roy: snap dos dedos, faísca chiando e explosão de chamas"),
    "matadora-de-dragoes": (matadora_de_dragoes, "básico de Guts: whoosh grave de ferro enorme, clang abafado e baque que treme"),
    "soco-do-stand": (soco_do_stand, "básico de Jotaro: soco pesado com eco fantasmagórico"),
    "soco-da-vida": (soco_da_vida, "básico de Giorno: soco, galhos brotando e arpejo dourado"),
    "pancada-de-sangue": (pancada_de_sangue, "básico de Power: pancada molhada, esguicho e gotas pingando"),
    "dedo-apontado": (dedo_apontado, "básico de Makima: silêncio pesado e um 'bang' abafado e sinistro"),
    "feitico-comum": (feitico_comum, "básico de Frieren: arpejo de cristal e o 'piuu' do Zoltraak"),
    "golpe-de-panico": (golpe_de_panico, "básico de Anya: tapinhas cômicos, 'boing' e estrelinhas"),
    "golpe-do-espiao": (golpe_do_espiao, "básico de Loid: cliques da mira e golpe de mão preciso"),
    "agulha-de-espinho": (agulha_de_espinho, "básico de Yor: dois 'tsk' afiados e um sussurro de pétalas"),
}
