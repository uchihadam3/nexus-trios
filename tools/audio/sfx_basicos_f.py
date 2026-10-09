"""Sons dos ataques básicos, lote f (veja tools/vfx/familias_v2/basicos_f.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _tom, _whoosh, _z, nota  # noqa: F401
from som import (CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, graos, modal, n_de, passa, poe,  # noqa: F401
                 reverb, rosa, ruido, satura, seno, sobe_e_some, varre)


def _t(n):
    return np.arange(n) / SR


def _corte_curto(rng, seg=0.14, lo=1500, hi=7000, g=0.7):
    """O "shk" de uma lâmina passando (ruído agudo com queda rápida)."""
    n = n_de(seg)
    return passa(ruido(rng, n), lo, hi, 2) * env(n, 0.002, seg * 0.3) * g


def _rasgo_molhado(rng, seg=0.2, g=0.7):
    """Rasgo orgânico: ruído médio, áspero (amplitude que trepida) e um pouco saturado."""
    n = n_de(seg)
    t = _t(n)
    trepida = 0.6 + 0.4 * np.sign(np.sin(2 * math.pi * rng.uniform(45, 70) * t))
    r = passa(ruido(rng, n), 600, 4000, 2) * env(n, 0.003, seg * 0.35) * trepida
    return satura(r * 1.4, 2.0) * g


def _squelch(rng, seg=0.18, f0=500, f1=180, g=0.5):
    """Som viscoso: ruído grave passando por um filtro que desce rápido, com bolha."""
    n = n_de(seg)
    x = assobio(rng, n, f0, f1, 1.5, 0.35) * env(n, 0.006, seg * 0.4) * 1.4
    bolha = seno(varre(f0 * 0.6, f1 * 0.5, n, 2.0), n) * env(n, 0.002, seg * 0.25) * 0.4
    return (x + bolha) * g


# ------------------------------------------------------------------ Vampira
def toque_absorvente(rng, v):
    x = _z(1.05)
    poe(x, B.soco_leve(rng, v), 0.1, 0.45)                                            # a mão encosta
    n = n_de(0.75)
    t = _t(n)
    # a sucção: ar sendo puxado, filtro descendo, com um tremor que acelera
    trem = 0.75 + 0.25 * np.sin(2 * math.pi * varre(8, 22, n) * t)
    suc = assobio(rng, n, 3200, 450, 0.8, 0.35) * sobe_e_some(n, 0.55, 1.2) * trem * 1.0
    # a energia indo para ela: tom que sobe com vibrato
    vib = 1 + 0.02 * np.sin(2 * math.pi * 9 * t)
    sobe = (seno(varre(260, 820, n, 0.8) * vib, n) * 0.25 + seno(varre(520, 1640, n, 0.8) * vib, n) * 0.1) * sobe_e_some(n, 0.8, 1.5)
    poe(x, suc + sobe, 0.16)
    poe(x, graos(rng, n_de(0.6), 18, 0.0, 0.5, 2500, 8000, 0.004) * 0.18, 0.25)        # centelhas de vida
    poe(x, _brilho(rng, 0.6, nota(88), 0.16, CRISTAL), 0.78)                           # o brilho que fica
    poe(x, _brilho(rng, 0.5, nota(95), 0.08, CRISTAL), 0.8)
    return reverb(x, 0.45, 0.25)


# ------------------------------------------------------------------ Professor X
def golpe_psiquico(rng, v):
    x = _z(1.1)
    n = n_de(0.5)
    t = _t(n)
    # o zumbido psíquico: dois tons quase iguais (batimento) com o tom ondulando
    f = 220 * (1 + 0.04 * np.sin(2 * math.pi * 5 * t))
    hum = (seno(f, n) + seno(f * 1.012, n) * 0.8 + seno(f * 2.003, n) * 0.35) * sobe_e_some(n, 0.85, 1.6) * 0.32
    hum += assobio(rng, n, 1500, 4500, 1.0, 0.25) * sobe_e_some(n, 0.9, 2.0) * 0.18
    poe(x, hum, 0.0)
    # o pulso na cabeça: "wum" que cai, baque abafado e anel que ressoa
    m = n_de(0.6)
    tm = _t(m)
    wum = seno(varre(900, 160, m, 1.8), m) * env(m, 0.002, 0.16) * 0.5
    anel = seno(330 * (1 + 0.03 * np.sin(2 * math.pi * 7 * tm)), m) * env(m, 0.004, 0.25) * (0.6 + 0.4 * np.sin(2 * math.pi * 14 * tm)) * 0.25
    poe(x, wum + anel, 0.36)
    poe(x, baque(n_de(0.4), 120, 50, 0.12, 0.2) * 0.6, 0.36)
    poe(x, passa(rosa(rng, n_de(0.3)), 800, 5000, 2) * env(n_de(0.3), 0.002, 0.06) * 0.3, 0.36)
    return reverb(x, 0.7, 0.35)


# ------------------------------------------------------------------ Venom
def tentaculo_simbionte(rng, v):
    x = _z(1.0)
    for k, em in enumerate((0.0, 0.05, 0.09)):
        poe(x, _squelch(rng, 0.22, 700 - 80 * k, 200, 0.55), em)                       # saem viscosos
        poe(x, _whoosh(rng, 0.16, 300, 3500, 0.85, 1.6, 0.4), em + 0.02)
    # a chicotada do tentáculo do meio
    n = n_de(0.12)
    crack = passa(ruido(rng, n), 2000, 10000, 2) * env(n, 0.0003, 0.008) * 0.7 + baque(n, 600, 300, 0.01, 0.4) * 0.25
    poe(x, crack, 0.15)
    poe(x, B.soco_leve(rng, v), 0.16, 0.6)
    # enrolando e apertando: estalos molhados e um rangido grave
    for k in range(4):
        poe(x, _squelch(rng, 0.14, rng.uniform(380, 520), 160, 0.35), 0.3 + 0.07 * k)
    m = n_de(0.4)
    tm = _t(m)
    range_ = satura(seno(70 + 8 * np.sin(2 * math.pi * 11 * tm), m) * 1.5, 2.5) * sobe_e_some(m, 0.5, 1.2) * 0.25
    poe(x, passa(range_, 90, 1200, 2), 0.36)
    return reverb(x, 0.35, 0.2, 3000)


# ------------------------------------------------------------------ Carnificina
def lamina_viva(rng, v):
    x = _z(0.95)
    for k, em in enumerate((0.0, 0.08, 0.16, 0.24)):
        poe(x, _whoosh(rng, 0.1, 900 + 200 * k, 5000, 0.8, 1.6, 0.4), em)
        poe(x, _corte_curto(rng, 0.12, 2000, 8000, 0.5), em + 0.06)
        poe(x, _rasgo_molhado(rng, 0.18, 0.55), em + 0.065)                            # carne rasgando
        poe(x, _squelch(rng, 0.12, 450, 150, 0.35), em + 0.08)
    poe(x, B.soco_leve(rng, v), 0.3, 0.5)
    for k in range(6):                                                                  # respingos
        d = n_de(0.05)
        poe(x, passa(ruido(rng, d), 500, 2500, 2) * env(d, 0.001, 0.01) * 0.25, 0.32 + rng.uniform(0, 0.3))
    return reverb(x, 0.3, 0.18, 4000)


# ------------------------------------------------------------------ Loki
def adaga_ilusoria(rng, v):
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.16, 800, 4500, 0.8, 1.6, 0.45), 0.0)                         # a adaga voa
    # a divisão: um brilho mágico, como um sino que se multiplica
    for k, f in enumerate((79, 83, 86, 91)):
        poe(x, _brilho(rng, 0.5, nota(f), 0.09, SINO), 0.11 + 0.015 * k)
    # as cópias: cortes fantasmas, cada um mais fraco, mais abafado e mais longe
    for k in range(4):
        eco = passa(_corte_curto(rng, 0.12, 1800, 6500, 0.5), 300, 4500 - 700 * k, 2)
        poe(x, eco, 0.2 + 0.045 * k, 0.6 * 0.7 ** k)
        d = n_de(0.18)
        puff = passa(rosa(rng, d), 1200, 5000, 2) * sobe_e_some(d, 0.2, 1.2) * 0.12
        poe(x, puff, 0.3 + 0.04 * k)                                                    # e somem em fumaça
    # a verdadeira: o "shink" metálico e o cravo
    poe(x, _corte_curto(rng, 0.14, 2500, 9000, 0.9), 0.36)
    poe(x, modal(n_de(0.5), 2600, rng=rng, **METAL) * env(n_de(0.5), 0.001, 0.12) * 0.18, 0.36)
    poe(x, B.soco_leve(rng, v), 0.37, 0.55)
    return reverb(x, 0.55, 0.3)


# ------------------------------------------------------------------ Galactus
def toque_do_devorador(rng, v):
    x = _z(1.45)
    n = n_de(1.3)
    t = _t(n)
    # o grave cósmico: um acorde muito baixo com batimento lento, e harmônicos para o celular
    f = 48 * (1 + 0.01 * np.sin(2 * math.pi * 0.7 * t))
    drone = sum(seno(f * k * (1 + 0.003 * k), n) / k for k in (1, 2, 3, 4, 6)) * 0.4
    drone = satura(drone * 1.4, 1.8) * sobe_e_some(n, 0.35, 1.2)
    coro = (seno(nota(57) * (1 + 0.004 * np.sin(2 * math.pi * 3 * t)), n) + seno(nota(64), n) * 0.7) * sobe_e_some(n, 0.4, 2.0) * 0.08
    poe(x, drone + coro, 0.0)
    poe(x, baque(n_de(0.6), 70, 30, 0.25, 0.3) * 0.9, 0.3)                              # a mão fecha
    # a desintegração: matéria estalando e sendo sugada (filtro que sobe), com cintilar cósmico
    m = n_de(0.9)
    poe(x, graos(rng, m, 70, 0.0, 0.75, 1500, 9000, 0.004, 0.7) * 0.45, 0.38)
    suga = assobio(rng, m, 300, 5500, 0.7, 0.35) * sobe_e_some(m, 0.75, 1.4) * 0.7
    poe(x, suga, 0.4)
    for k in range(5):
        poe(x, _brilho(rng, 0.4, nota(rng.choice([86, 89, 93, 98])), 0.05, CRISTAL), 0.45 + 0.12 * k)
    return reverb(x, 0.8, 0.35, 5000)


# ------------------------------------------------------------------ Senhor das Estrelas
def _pew(rng, f0, f1, seg=0.13):
    """O "pew" retrô: onda quase quadrada com o tom despencando."""
    n = n_de(seg)
    fr = varre(f0, f1, n, 1.6)
    fase = 2 * math.pi * np.cumsum(fr) / SR
    quadrada = np.tanh(np.sin(fase) * 4) * 0.6 + np.sin(fase * 2) * 0.15
    return passa(quadrada, 150, 7000, 2) * env(n, 0.001, seg * 0.45)


def blasters_elementais(rng, v):
    x = _z(0.95)
    for k, em in enumerate((0.0, 0.13, 0.26, 0.39)):
        alto = k % 2 == 0
        f0 = 2200 if alto else 1650
        poe(x, _pew(rng, f0 * rng.uniform(0.97, 1.03), 260 if alto else 200), em, 0.55)
        poe(x, estalo(rng, n_de(0.03), 2500, 9000, 0.003) * 0.4, em)
        # o estouro no alvo
        d = n_de(0.18)
        pop = baque(d, 180, 80, 0.04, 0.3) * 0.4 + passa(ruido(rng, d), 900, 5000, 2) * env(d, 0.001, 0.025) * 0.45
        poe(x, pop, em + 0.12)
    return reverb(x, 0.35, 0.18)


# ------------------------------------------------------------------ Rocket
def arma_grande(rng, v):
    x = _z(1.3)
    n = n_de(0.2)
    t = _t(n)
    # a carga: zumbido que sobe e engata
    carga = (seno(varre(180, 1300, n, 0.8), n) * 0.3 + seno(varre(360, 2600, n, 0.8), n) * 0.1) * sobe_e_some(n, 0.95, 1.4)
    carga *= 0.8 + 0.2 * np.sign(np.sin(2 * math.pi * 40 * t))
    poe(x, carga, 0.0)
    poe(x, estalo(rng, n_de(0.04), 1500, 6000, 0.004) * 0.6, 0.17)                      # trava
    # o tiro: tranco grave e o sopro do plasma
    poe(x, baque(n_de(0.5), 90, 35, 0.16, 0.6) * 1.0, 0.19)
    poe(x, satura(passa(ruido(rng, n_de(0.2)), 300, 3500, 2) * env(n_de(0.2), 0.001, 0.05), 2.2) * 0.6, 0.19)
    poe(x, _whoosh(rng, 0.14, 1800, 300, 0.4, 1.2, 0.5), 0.2)
    m = n_de(0.15)
    poe(x, seno(varre(700, 220, m, 1.5), m) * env(m, 0.002, 0.06) * 0.3, 0.19)
    # a explosão no alvo
    poe(x, B.explosao(rng, v), 0.31, 0.95)
    return x


# ------------------------------------------------------------------ Aquaman
def tridente(rng, v):
    x = _z(1.0)
    n = n_de(0.2)
    poe(x, assobio(rng, n, 400, 3200, 1.6, 0.4) * sobe_e_some(n, 0.85, 1.4) * 0.8, 0.0)  # a estocada
    poe(x, _corte_curto(rng, 0.1, 2500, 9000, 0.5), 0.12)
    poe(x, modal(n_de(0.6), 1900, rng=rng, **METAL) * env(n_de(0.6), 0.001, 0.15) * 0.14, 0.13)  # o "tim" das pontas
    poe(x, modal(n_de(0.6), 2850, rng=rng, **METAL) * env(n_de(0.6), 0.001, 0.12) * 0.08, 0.135)
    poe(x, B.soco_leve(rng, v), 0.14, 0.75)
    poe(x, B.agua(rng, v), 0.15, 1.0)                                                    # o respingo
    m = n_de(0.35)
    onda = passa(rosa(rng, m), 300, 2500, 2) * sobe_e_some(m, 0.2, 1.0) * 0.35
    poe(x, onda, 0.05)
    return reverb(x, 0.4, 0.2)


# ------------------------------------------------------------------ Ciborgue
def canhao_sonico(rng, v):
    x = _z(1.0)
    n = n_de(0.62)
    t = _t(n)
    # onda sônica: tom grave e áspero pulsando rápido (cada pulso é um arco do desenho)
    f = varre(150, 240, n, 1.0)
    fase = 2 * math.pi * np.cumsum(f) / SR
    corpo = np.tanh(np.sin(fase) * 3) * 0.5 + np.sin(fase * 3) * 0.15
    pulsos = np.clip(np.sin(2 * math.pi * 15 * t), 0, 1) ** 2
    som = corpo * (0.25 + 0.75 * pulsos) * env(n, 0.01, 0.4, segura=0.15)
    som += passa(rosa(rng, n), 1200, 6000, 2) * pulsos * env(n, 0.01, 0.3, segura=0.1) * 0.2
    poe(x, passa(som, 100, 6000, 2), 0.0)
    # o "wom" de cada arco chegando no alvo
    for k in range(6):
        d = n_de(0.12)
        poe(x, baque(d, 160, 90, 0.03, 0.1) * 0.25, 0.18 + 0.065 * k)
    m = n_de(0.4)
    poe(x, seno(varre(520, 120, m, 1.2), m) * env(m, 0.002, 0.12) * 0.25, 0.2)
    return reverb(x, 0.45, 0.22)


# ------------------------------------------------------------------ Pantera Negra
def garras_cineticas(rng, v):
    x = _z(1.05)
    for s, em in enumerate((0.0, 0.11)):
        for k in range(3):
            d = n_de(0.13)
            r = passa(ruido(rng, d), 1800, 8000, 2) * env(d, 0.001, 0.035) * 0.6
            r += modal(d, rng.uniform(2600, 3400), rng=rng, **METAL) * env(d, 0.001, 0.05) * 0.12   # vibranium
            poe(x, r, em + 0.022 * k)
        poe(x, _whoosh(rng, 0.1, 1200, 6000, 0.7, 1.5, 0.3), em)
    # a energia se acumulando nos talhos e estourando no pulso cinético
    n = n_de(0.24)
    poe(x, seno(varre(300, 1100, n, 0.7), n) * sobe_e_some(n, 0.95, 1.6) * 0.18, 0.14)
    m = n_de(0.6)
    vwum = seno(varre(520, 70, m, 1.6), m) * env(m, 0.002, 0.2) * 0.55
    poe(x, vwum + baque(m, 110, 45, 0.15, 0.3) * 0.7, 0.38)
    poe(x, B.impacto_energia(rng, v), 0.38, 0.7)
    return reverb(x, 0.45, 0.22)


# ------------------------------------------------------------------ Darkseid
def punho_de_apokolips(rng, v):
    x = _z(1.3)
    n = n_de(0.16)
    poe(x, assobio(rng, n, 150, 1400, 1.6, 0.45) * sobe_e_some(n, 0.9, 1.4) * 0.9, 0.0)   # o punho pesado
    poe(x, B.soco_pesado(rng, v), 0.13, 0.8)
    poe(x, baque(n_de(0.7), 60, 28, 0.3, 0.1) * 0.45, 0.14)
    poe(x, graos(rng, n_de(0.4), 20, 0.0, 0.25, 500, 3500, 0.007) * 0.3, 0.16)           # rachando
    # o zumbido sinistro do Efeito Ômega: grave áspero com batimento e um feixe chiando
    m = n_de(0.9)
    t = _t(m)
    f = 55 * (1 + 0.02 * np.sin(2 * math.pi * 3 * t))
    fase = 2 * math.pi * np.cumsum(f) / SR
    zumbido = (np.tanh(np.sin(fase) * 3) + np.tanh(np.sin(fase * 1.01 + 1) * 3) * 0.8 + np.sin(fase * 4) * 0.3) * 0.32
    zumbido = passa(zumbido, 60, 2500, 2) * sobe_e_some(m, 0.3, 1.0)
    chiado = passa(ruido(rng, m), 2500, 8000, 2) * sobe_e_some(m, 0.3, 1.3) * 0.12 * (0.6 + 0.4 * np.sin(2 * math.pi * 23 * t))
    poe(x, zumbido + chiado, 0.25)
    poe(x, seno(varre(1200, 300, n_de(0.5), 0.8), n_de(0.5)) * env(n_de(0.5), 0.02, 0.2) * 0.12, 0.3)
    return reverb(x, 0.7, 0.3, 3500)


# ------------------------------------------------------------------ Hellboy
def mao_da_perdicao(rng, v):
    x = _z(1.3)
    n = n_de(0.2)
    poe(x, assobio(rng, n, 120, 900, 1.8, 0.5) * sobe_e_some(n, 0.92, 1.6) * 1.0, 0.0)   # a mão de pedra desce
    em = 0.17
    poe(x, baque(n_de(0.8), 65, 26, 0.3, 0.3) * 0.85, em)                                  # pedra no chão
    poe(x, satura(passa(ruido(rng, n_de(0.25)), 250, 2500, 2) * env(n_de(0.25), 0.001, 0.06), 2.5) * 0.9, em)   # o "crack"
    poe(x, modal(n_de(0.3), 320, rng=rng, razoes=[1, 2.3, 3.9, 5.6], quedas=[0.06, 0.04, 0.03, 0.02]) * 0.35, em)  # pedra maciça
    poe(x, graos(rng, n_de(0.8), 45, 0.02, 0.7, 500, 4000, 0.008) * 0.75, em + 0.02)      # cascalho caindo
    m = n_de(0.7)
    poe(x, passa(rosa(rng, m), 40, 250, 2) * env(m, 0.01, 0.25) * 0.5, em)                # o chão treme
    poe(x, passa(rosa(rng, m), 600, 3000, 2) * sobe_e_some(m, 0.15, 1.0) * 0.15, em + 0.05)   # poeira
    return reverb(x, 0.55, 0.22, 3500)


# nome do arquivo (com hífen) → (função, descrição)
SONS: dict = {
    "toque-absorvente": (toque_absorvente, "básico de Vampira: toque leve, sucção de energia que sobe e brilho"),
    "golpe-psiquico": (golpe_psiquico, "básico de Professor X: zumbido psíquico que cresce e pulso que ressoa"),
    "tentaculo-simbionte": (tentaculo_simbionte, "básico de Venom: tentáculos viscosos, chicotada e aperto molhado"),
    "lamina-viva": (lamina_viva, "básico de Carnificina: quatro cortes orgânicos rasgando, com respingos"),
    "adaga-ilusoria": (adaga_ilusoria, "básico de Loki: adaga voando, brilho mágico, ecos ilusórios e o shink real"),
    "toque-do-devorador": (toque_do_devorador, "básico de Galactus: grave cósmico, a mão fecha e a matéria se desintegra"),
    "blasters-elementais": (blasters_elementais, "básico de Senhor das Estrelas: pew pew retrô alternado e estouros"),
    "arma-grande": (arma_grande, "básico de Rocket: carga, tranco de canhão pesado e explosão"),
    "tridente": (tridente, "básico de Aquaman: estocada metálica do tridente e respingo de água"),
    "canhao-sonico": (canhao_sonico, "básico de Ciborgue: onda sônica pulsante batendo no alvo"),
    "garras-cineticas": (garras_cineticas, "básico de Pantera Negra: garras de vibranium e pulso cinético"),
    "punho-de-apokolips": (punho_de_apokolips, "básico de Darkseid: soco grave e o zumbido sinistro do Ômega"),
    "mao-da-perdicao": (mao_da_perdicao, "básico de Hellboy: pedra pesada esmagando e cascalho"),
}
