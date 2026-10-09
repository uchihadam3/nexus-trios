"""Sons dos ataques básicos, lote h (veja tools/vfx/familias_v2/basicos_h.py).

Cada som segue a folha do golpe no tempo (a animação dura ~0,8 s): a rajada de
chutes da Chun-Li, a kunai que voa, crava e é puxada, o chute com rugido de
chamas, o soco com o estalo elétrico grave, a chave-espada com o brilho mágico,
o "tink" de aparar e o corte, os cortes rápidos da Malenia, a lâmina gelada, o
"pshew" do plasma, o zumbido e o arremesso da arma da gravidade, o metal
arrastando e o golpe pesado, a areia do tempo correndo ao contrário e a espada
do Alucard com as asas dos morcegos. Tudo sintetizado.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _rugido, _tom, _whoosh, _z, nota  # noqa: F401
from som import (CENTROS, CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, faixas, graos, modal, n_de, passa,  # noqa: F401
                 poe, reverb, rosa, ruido, satura, seno, sobe_e_some, varre)

# nome do arquivo (com hífen) → (função, descrição)
SONS: dict = {}


# ------------------------------------------------------------------ peças
def _grave(x, fator):
    """Reamostra (fator < 1 deixa mais grave e mais longo)."""
    idx = np.arange(0, len(x) - 1, fator)
    return np.interp(idx, np.arange(len(x)), x)


def _shing(rng, seg=0.45, f0=2600.0, g=0.22, chiado=0.5):
    """O "shing" da lâmina: chiado agudo curto e o metal tinindo."""
    n = n_de(seg)
    x = assobio(rng, n, 2500, 9500, 0.6, 0.35) * env(n, 0.002, 0.045) * chiado
    x += modal(n, f0, rng=rng, **METAL) * env(n, 0.001, seg * 0.35) * g
    return x


def _tapa(rng, seg=0.12, g=0.5):
    """Contato curto e seco (pé, mão)."""
    n = n_de(seg)
    return (estalo(rng, n, 1200, 6000, 0.008) * 0.8 + baque(n, 160, 90, 0.035, 0.3) * 0.6) * g


def _zap(rng, seg, densidade=0.004, lo=300, hi=9000):
    """Crepitar elétrico: pulsos aleatórios de largura curta."""
    n = n_de(seg)
    z = np.zeros(n)
    k = 0
    while k < n:
        larg = max(1, int(rng.uniform(0.0004, 0.002) * SR))
        z[k:k + larg] += rng.choice([-1, 1]) * rng.uniform(0.4, 1)
        k += max(1, int(rng.exponential(densidade) * SR))
    return passa(z, lo, hi, 2)


# ================================================================== Chun-Li
def chute_relampago(rng, v):
    """Rajada de chutes muito rápidos: dezenas de sopros curtos e tapas secos, cada vez mais
    juntos, e o último chute mais forte."""
    x = _z(1.05)
    t, k = 0.02, 0
    while t < 0.56:
        poe(x, _whoosh(rng, 0.07, 900, 4200, 0.55, g=0.32), t)
        poe(x, _tapa(rng, 0.12, rng.uniform(0.35, 0.6)), t + 0.028)
        if k % 3 == 0:
            poe(x, passa(B.soco_leve(rng, v), 120, None, 1) * 0.35, t + 0.028)
        t += max(0.024, 0.048 - 0.0015 * k)
        k += 1
    poe(x, _whoosh(rng, 0.14, 500, 4500, 0.8, g=0.7), 0.5)
    poe(x, B.soco_pesado(rng, v) * 1.0, 0.6)
    poe(x, estalo(rng, n_de(0.06), 2000, 9000, 0.006) * 0.6, 0.6)
    return reverb(x, 0.3, 0.12, 7000)


# ================================================================== Scorpion
def kunai_do_inferno(rng, v):
    """A lança voa (sopro + a corda chiando), crava com um "tchac" metálico, a corda estica
    com um estalo grave, e o puxão volta com um sopro de fogo."""
    x = _z(1.3)
    # o arremesso: sopro e a corda correndo
    poe(x, _whoosh(rng, 0.24, 700, 3800, 0.85, g=0.7), 0.0)
    n = n_de(0.22)
    corda = passa(ruido(rng, n), 2500, 7000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 60 * np.arange(n) / SR)) * sobe_e_some(n, 0.7, 1.2) * 0.12
    poe(x, corda, 0.0)
    # crava: ponta de metal entrando e o baque
    poe(x, estalo(rng, n_de(0.05), 2500, 10000, 0.004) * 0.9, 0.2)
    poe(x, modal(n_de(0.25), rng.uniform(1700, 1900), rng=rng, **METAL) * env(n_de(0.25), 0.001, 0.05) * 0.25, 0.2)
    poe(x, baque(n_de(0.25), 150, 70, 0.07, 0.5) * 0.7, 0.2)
    poe(x, B._carne(rng, n_de(0.2)) * 0.5, 0.205)
    poe(x, B.fogo(rng, v) * 0.32, 0.22)
    # a corda estica: "tuum" grave de corda tensa
    m = n_de(0.35)
    tt = np.arange(m) / SR
    f = 98 * (1 + 0.06 * np.exp(-tt * 30))
    tensa = sum(seno(f * h, m) / h for h in (1, 2, 3, 4)) * env(m, 0.002, 0.11)
    poe(x, satura(tensa, 1.6) * 0.45, 0.37)
    poe(x, estalo(rng, n_de(0.04), 800, 4000, 0.006) * 0.5, 0.37)
    # o puxão
    poe(x, _whoosh(rng, 0.28, 3400, 500, 0.35, g=0.95), 0.44)
    poe(x, B.fogo(rng, v) * 0.3, 0.46)
    return reverb(x, 0.4, 0.18, 6500)


# ================================================================== Liu Kang
def chute_do_dragao(rng, v):
    """Chute voador: o sopro do salto pega fogo, o pé acerta e o dragão de chamas ruge."""
    x = _z(1.4)
    poe(x, _whoosh(rng, 0.28, 400, 3000, 0.85, g=0.75), 0.0)
    poe(x, B.fogo(rng, v) * 0.45, 0.02)
    poe(x, B.soco_pesado(rng, v) * 1.0, 0.25)
    poe(x, baque(n_de(0.4), 95, 40, 0.18, 0.5) * 0.6, 0.25)
    poe(x, _rugido(rng, 0.75, 48, 38, 0.33, 2.6), 0.22)
    poe(x, B.fogo(rng, v) * 0.9, 0.26)
    poe(x, graos(rng, n_de(0.7), 35, 0.0, 0.6, 1800, 8000, 0.003) * 0.25, 0.32)
    return reverb(x, 0.5, 0.22, 6000)


# ================================================================== Kazuya
def soco_do_diabo(rng, v):
    """Soco pesado com o estalo elétrico grave do Gene do Diabo: crepita no braço, o punho bate
    e um trovão curto e escuro com zumbido."""
    x = _z(1.2)
    n = n_de(0.16)
    poe(x, _whoosh(rng, 0.16, 500, 3000, 0.85, g=0.6), 0.0)
    poe(x, _zap(rng, 0.16, 0.006, 600, 7000) * sobe_e_some(n, 0.8, 1.2) * 0.25, 0.0)
    poe(x, B.soco_pesado(rng, v) * 1.0, 0.15)
    poe(x, _grave(B.raio(rng, v), 0.62) * 0.75, 0.15)
    m = n_de(0.55)
    zum = satura(sum(seno(np.full(m, 52.0 * h), m) / h for h in range(1, 7)), 2.5)
    poe(x, passa(zum, 60, 2500, 2) * env(m, 0.004, 0.18) * 0.28, 0.15)
    poe(x, _zap(rng, 0.55, 0.012, 300, 5000) * env(m, 0.002, 0.15) * 0.4, 0.17)
    poe(x, estalo(rng, n_de(0.05), 3000, 12000, 0.004) * 0.7, 0.15)
    return reverb(x, 0.5, 0.22, 5000)


# ================================================================== Sora
def keyblade(rng, v):
    """Golpe da chave-espada: o sopro do arco, o "tonc" metálico leve e o brilho mágico subindo
    em notas de cristal."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.2, 600, 3500, 0.8, g=0.65), 0.0)
    poe(x, B.soco_leve(rng, v) * 0.85, 0.15)
    poe(x, modal(n_de(0.4), rng.uniform(1150, 1300), rng=rng, **METAL) * env(n_de(0.4), 0.001, 0.09) * 0.22, 0.15)
    for k, mm in enumerate((84, 88, 91, 96, 100)):
        poe(x, _brilho(rng, 0.6, nota(mm), 0.11, CRISTAL), 0.18 + 0.055 * k)
    n = n_de(0.7)
    poe(x, passa(rosa(rng, n), 5000, 13000, 2) * sobe_e_some(n, 0.25, 1.2) * 0.08, 0.17)
    poe(x, graos(rng, n_de(0.7), 22, 0.0, 0.6, 5000, 12000, 0.002) * 0.15, 0.2)
    return reverb(x, 0.7, 0.32, 10000)


# ================================================================== Sekiro
def aparar_e_cortar(rng, v):
    """O "tink" seco e brilhante da deflexão (metal com metal) e, logo depois, o contra-corte."""
    x = _z(1.1)
    n = n_de(0.6)
    poe(x, estalo(rng, n, 3000, 13000, 0.003) * 1.0, 0.0)
    poe(x, modal(n, rng.uniform(2200, 2400), rng=rng, **METAL) * env(n, 0.0005, 0.2) * 0.45, 0.0)
    poe(x, modal(n, rng.uniform(3300, 3500), rng=rng, **VIDRO) * env(n, 0.0005, 0.12) * 0.15, 0.0)
    poe(x, baque(n_de(0.15), 260, 140, 0.03, 0.2) * 0.3, 0.0)
    poe(x, graos(rng, n_de(0.35), 18, 0.0, 0.25, 4000, 12000, 0.0015) * 0.25, 0.01)
    poe(x, _whoosh(rng, 0.12, 1200, 6500, 0.7, g=0.6), 0.28)
    poe(x, _shing(rng, 0.5, 2900, 0.18, 0.7), 0.36)
    poe(x, B._carne(rng, n_de(0.15)) * 0.35, 0.37)
    return reverb(x, 0.45, 0.2, 9000)


# ================================================================== Malenia
def lamina_protetica(rng, v):
    """Dança da Ave Aquática: cortes finíssimos em rajada, um sobre o outro, e um sopro longo de
    ar girando por baixo."""
    x = _z(1.3)
    t, k = 0.0, 0
    while t < 0.56:
        poe(x, _whoosh(rng, 0.09, 1600, 7500, 0.45, g=0.38), t)
        if k % 2 == 0:
            poe(x, _shing(rng, 0.2, rng.uniform(3000, 3800), 0.06, 0.35), t + 0.04)
        t += max(0.03, 0.05 - 0.002 * k)
        k += 1
    n = n_de(0.85)
    tt = np.arange(n) / SR
    curva = 500 * 2 ** (1.4 * np.sin(math.pi * tt / (n / SR)) ** 1.2) * (1 + 0.15 * np.sin(2 * math.pi * 5 * tt))
    sopro = faixas(rosa(rng, n), CENTROS, curva, 0.45) * sobe_e_some(n, 0.45, 1.3) * 0.55
    poe(x, sopro, 0.05)
    poe(x, graos(rng, n_de(0.6), 25, 0.0, 0.55, 2500, 7000, 0.003) * 0.08, 0.35)
    return reverb(x, 0.5, 0.25, 8000)


# ================================================================== Arthas
def frostmourne(rng, v):
    """A lâmina rúnica pesada corta o ar, o metal tine frio, o gelo estala e cristaliza e um
    vento gelado uiva baixo."""
    x = _z(1.5)
    poe(x, _whoosh(rng, 0.26, 300, 2600, 0.8, g=0.75), 0.0)
    poe(x, _shing(rng, 0.8, 1150, 0.22, 0.6), 0.16)
    poe(x, baque(n_de(0.3), 110, 50, 0.1, 0.3) * 0.45, 0.18)
    poe(x, B.gelo(rng, v) * 0.8, 0.2)
    n = n_de(0.9)
    tt = np.arange(n) / SR
    uivo = assobio(rng, n, 700, 950, 1.0, 0.18) * (1 + 0.2 * np.sin(2 * math.pi * 4 * tt)) * sobe_e_some(n, 0.35, 1.4) * 0.35
    poe(x, uivo, 0.25)
    poe(x, seno(np.full(n, nota(33)), n) * env(n, 0.05, 0.35) * 0.12, 0.18)
    return reverb(x, 0.7, 0.32, 8000)


# ================================================================== Isaac
def cortador_de_plasma(rng, v):
    """Os três bipes da mira, o "pshew" do plasma (tom que despenca com ruído chiado) e o chiado
    do metal derretido onde cortou."""
    x = _z(1.0)
    for k in range(3):
        m = n_de(0.035)
        poe(x, seno(np.full(m, 3100.0 + 120 * k), m) * env(m, 0.001, 0.012) * 0.12, 0.02 + 0.04 * k)
    n = n_de(0.24)
    tt = np.arange(n) / SR
    f = varre(2600, 260, n, 0.6)
    fm = seno(f * (1 + 0.5 * seno(f * 1.5, n)), n)
    pshew = satura(fm, 1.8) * env(n, 0.001, 0.07) * 0.5
    pshew += passa(ruido(rng, n), 1500, 9000, 2) * env(n, 0.001, 0.035) * 0.6
    poe(x, pshew, 0.26)
    poe(x, _whoosh(rng, 0.1, 4000, 900, 0.2, g=0.4), 0.27)
    m = n_de(0.55)
    poe(x, estalo(rng, m, 2000, 10000, 0.005) * 0.7, 0.35)
    poe(x, baque(n_de(0.2), 160, 80, 0.05, 0.3) * 0.45, 0.35)
    chia = passa(ruido(rng, m), 3500, 11000, 2) * env(m, 0.01, 0.22) * 0.14 + graos(rng, m, 40, 0.0, 0.45, 3000, 10000, 0.002) * 0.25
    poe(x, chia, 0.36)
    return reverb(x, 0.4, 0.18, 9000)


# ================================================================== Gordon
def arma_da_gravidade(rng, v):
    """O zumbido da arma da gravidade segurando o objeto, o tranco do disparo (baque + sopro) e o
    estrondo da caixa quebrando no alvo."""
    x = _z(1.3)
    n = n_de(0.34)
    tt = np.arange(n) / SR
    f = 72 * (1 + 0.04 * np.sin(2 * math.pi * 7 * tt)) * (1 + 0.15 * tt / tt[-1])
    fase = 2 * math.pi * np.cumsum(f) / SR
    zum = satura(sum(np.sin(h * fase) / h for h in range(1, 12)), 1.8)
    zum = passa(zum, 70, 3000, 2) * (0.75 + 0.25 * np.sin(2 * math.pi * 13 * tt))
    gira = passa(rosa(rng, n), 600, 2400, 2) * 0.25
    poe(x, (zum * 0.3 + gira) * sobe_e_some(n, 0.6, 0.8), 0.0)
    poe(x, baque(n_de(0.3), 220, 70, 0.06, 0.6) * 0.8, 0.31)
    poe(x, estalo(rng, n_de(0.05), 1500, 7000, 0.005) * 0.7, 0.31)
    poe(x, _whoosh(rng, 0.12, 500, 3500, 0.5, g=0.7), 0.31)
    poe(x, B.soco_pesado(rng, v) * 0.9, 0.41)
    m = n_de(0.6)
    madeira = modal(m, rng.uniform(320, 380), [1.0, 2.1, 3.4, 5.2], [0.05, 0.035, 0.025, 0.02], [1, 0.6, 0.4, 0.2], rng=rng) * 0.3
    poe(x, madeira, 0.41)
    poe(x, graos(rng, m, 30, 0.0, 0.35, 500, 4500, 0.006) * 0.45, 0.42)
    return reverb(x, 0.45, 0.2, 6500)


# ================================================================== Pyramid Head
def grande_faca(rng, v):
    """Metal enorme arrastado no chão (rangido áspero que pula), o sopro pesado do golpe e o
    impacto que faz o chão tremer, com o metal tinindo grave."""
    x = _z(1.5)
    n = n_de(0.34)
    tt = np.arange(n) / SR
    pula = np.clip(passa(ruido(rng, n), None, 35, 2) * 8 + 0.4, 0, 1)
    raspa = passa(ruido(rng, n), 900, 6000, 2) * (0.35 + 0.65 * pula)
    guincho = seno(1650 * (1 + 0.02 * passa(ruido(rng, n), None, 20, 1) * 20), n) * pula * 0.15
    ressoa = modal(n, 420, rng=rng, **METAL) * passa(ruido(rng, n), None, 200, 1) * 2.5
    arrasto = (raspa * 0.3 + guincho + ressoa * 0.15 + passa(rosa(rng, n), 60, 300, 2) * 0.25) * sobe_e_some(n, 0.3, 1.0) * 1.8
    poe(x, arrasto, 0.0)
    poe(x, graos(rng, n, 30, 0.0, 0.3, 2500, 9000, 0.002) * 0.2, 0.0)
    poe(x, _whoosh(rng, 0.14, 200, 1200, 0.8, g=0.8), 0.31)
    poe(x, baque(n_de(0.7), 75, 28, 0.35, 0.8) * 1.2, 0.43)
    poe(x, modal(n_de(0.9), 210, rng=rng, **METAL) * env(n_de(0.9), 0.001, 0.4) * 0.3, 0.43)
    poe(x, B.soco_pesado(rng, v) * 0.7, 0.43)
    poe(x, graos(rng, n_de(0.6), 40, 0.0, 0.5, 400, 3500, 0.007) * 0.35, 0.45)
    return reverb(x, 0.65, 0.28, 4500)


# ================================================================== Prince of Persia
def adaga_do_tempo(rng, v):
    """O corte curto da adaga e depois o tempo voltando: a areia escorrendo ao contrário (sobe em
    vez de cair), um brilho de cristal invertido e o tique-taque do relógio para trás."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.12, 1200, 6000, 0.6, g=0.6), 0.0)
    poe(x, _shing(rng, 0.35, 3300, 0.14, 0.6), 0.08)
    n = n_de(0.62)
    areia = graos(rng, n, 260, 0.0, 0.6, 2000, 9000, 0.0015, 0.8) * 0.4
    areia += passa(rosa(rng, n), 2500, 10000, 2) * 0.12
    areia *= env(n, 0.005, 0.2)
    poe(x, areia[::-1], 0.18)
    cr = modal(n, nota(91), rng=rng, **CRISTAL) * env(n, 0.001, 0.2) * 0.13
    poe(x, cr[::-1], 0.18)
    poe(x, _whoosh(rng, 0.45, 5000, 900, 0.85, g=0.4), 0.33)
    for k in range(4):
        m = n_de(0.03)
        poe(x, estalo(rng, m, 2500, 8000, 0.003) * 0.3, 0.24 + 0.13 * k)
    poe(x, modal(n_de(0.5), nota(96), rng=rng, **CRISTAL) * env(n_de(0.5), 0.001, 0.2) * 0.08, 0.8)
    return reverb(x, 0.65, 0.3, 9000)


# ================================================================== Alucard
def espada_de_alucard(rng, v):
    """O corte elegante da espada (sopro fino e o metal tinindo limpo) e a revoada de morcegos:
    asas batendo e chiados agudos."""
    x = _z(1.35)
    poe(x, _whoosh(rng, 0.16, 1200, 7000, 0.7, g=0.6), 0.0)
    poe(x, _shing(rng, 0.7, 3500, 0.2, 0.55), 0.1)
    poe(x, modal(n_de(0.7), 1760, rng=rng, **SINO) * env(n_de(0.7), 0.002, 0.25) * 0.05, 0.1)
    for _ in range(40):
        m = n_de(0.05)
        poe(x, passa(ruido(rng, m), 350, 2600, 2) * env(m, 0.004, 0.018) * rng.uniform(0.07, 0.18), 0.15 + rng.uniform(0, 0.75) ** 1.3)
    for k in range(5):
        m = n_de(0.045)
        f = varre(rng.uniform(7500, 9000), rng.uniform(5500, 6500), m, 1.0)
        poe(x, seno(f * (1 + 0.04 * seno(np.full(m, 180.0), m)), m) * env(m, 0.003, 0.012) * 0.05, 0.22 + 0.11 * k + rng.uniform(0, 0.04))
    return reverb(x, 0.6, 0.28, 8000)


SONS.update({
    "chute-relampago": (chute_relampago, "básico de Chun-Li: rajada de chutes muito rápidos e o último mais forte"),
    "kunai-do-inferno": (kunai_do_inferno, "básico de Scorpion: lança voando, crava, corda estica e puxão com fogo"),
    "chute-do-dragao": (chute_do_dragao, "básico de Liu Kang: chute voador e rugido de chamas"),
    "soco-do-diabo": (soco_do_diabo, "básico de Kazuya: soco pesado e estalo elétrico grave"),
    "keyblade": (keyblade, "básico de Sora: golpe da chave-espada e brilho mágico"),
    "aparar-e-cortar": (aparar_e_cortar, "básico de Sekiro: tink de deflexão e o contra-corte"),
    "lamina-protetica": (lamina_protetica, "básico de Malenia: cortes em rajada e sopro girando"),
    "frostmourne": (frostmourne, "básico de Arthas: lâmina rúnica, gelo estalando e vento frio"),
    "cortador-de-plasma": (cortador_de_plasma, "básico de Isaac: bipes da mira, pshew do plasma e chiado"),
    "arma-da-gravidade": (arma_da_gravidade, "básico de Gordon: zumbido da arma, tranco e caixa quebrando"),
    "grande-faca": (grande_faca, "básico de Pyramid Head: metal arrastando e golpe pesado"),
    "adaga-do-tempo": (adaga_do_tempo, "básico do Príncipe: corte e areia escorrendo ao contrário"),
    "espada-de-alucard": (espada_de_alucard, "básico de Alucard: espada elegante e asas de morcegos"),
})
