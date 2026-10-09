"""Sons dos ataques básicos, lote j (veja tools/vfx/familias_v2/basicos_j.py).

Cada som conta o golpe do desenho: a barriga que faz "bloing", o elástico do
estilingue e o "tock" da pedra, a mola da luva do Bugiganga, o raio etéreo do
Danny, o esguicho que chia da flor do Coringa, o "crack" do taco da Arlequina,
os cinco anéis do Capitão Planeta e o "chomp" (com os dentes batendo de medo)
do Scooby e do Coragem. Tudo sintetizado.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _tom, _whoosh, _z, nota  # noqa: F401
from som import (CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, graos, modal, n_de, passa, poe,  # noqa: F401
                 reverb, rosa, ruido, satura, seno, sobe_e_some, varre)
from som import janela_suave, serra_suave


# ------------------------------------------------------------------ peças
def _fim(x, sai=0.04):
    """Some suave no fim do trecho (sem estalo de corte)."""
    return x * janela_suave(len(x), 0.0005, sai)


def _mola(seg, f0, prof=0.45, vel=10.0, queda_vib=5.0, g=0.3, harm=0.35):
    """O "boing/doing" de desenho: tom com vibrato largo que amortece."""
    n = n_de(seg)
    t = np.arange(n) / SR
    f = f0 * (1 + prof * np.exp(-t * queda_vib) * np.sin(2 * math.pi * vel * t))
    fase = 2 * math.pi * np.cumsum(f) / SR
    x = np.sin(fase) + harm * np.sin(2 * fase) + harm * 0.4 * np.sin(3 * fase)
    return _fim(x * env(n, 0.003, seg * 0.45) * g)


def _madeira(rng, n, f0, quedas=(0.06, 0.03, 0.018, 0.012), g_ruido=0.8):
    """Pancada seca em madeira/pedra: poucos modos curtos e um estalo de contato."""
    t = np.arange(n) / SR
    x = np.zeros(n)
    for (r, gg), q in zip(((1.0, 1.0), (2.41, 0.6), (3.93, 0.4), (5.6, 0.25)), quedas):
        f = f0 * r * rng.uniform(0.985, 1.015)
        if f < SR * 0.45:
            x += np.sin(2 * math.pi * f * t) * np.exp(-t / q) * gg
    return x + passa(ruido(rng, n), 1500, 9000, 2) * env(n, 0.0003, 0.006) * g_ruido


def _bolha(rng, f0, seg=0.06, g=0.2):
    """O "blup" de uma bolha: tom que sobe rápido e some."""
    n = n_de(seg)
    return _fim(seno(varre(f0, f0 * 2.2, n, 0.7), n) * env(n, 0.002, seg * 0.35) * g, 0.01)


def _clique_dente(rng, f0, g=0.5):
    """Dente batendo em dente: clique duro e agudo, com um corpo curtinho."""
    n = n_de(0.05)
    return _madeira(rng, n, f0, (0.012, 0.008, 0.006, 0.004), 1.0) * g


# ------------------------------------------------------------------ Homer
def barrigada(rng, v):
    """Barrigada: o ar do empurrão, o baque carnudo da pança e o "bloing" de gelatina que balança."""
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.2, 220, 1400, 0.85, g=0.55), 0)
    bate = 0.17
    poe(x, B.soco_pesado(rng, v), bate, 0.85)
    n = n_de(0.12)
    tapa = passa(ruido(rng, n), 500, 2600, 2) * env(n, 0.0005, 0.02)                   # o "plaft" da pele
    poe(x, satura(tapa, 2.5) * 0.7, bate)
    # bloing: tom grave e borrachudo, com vibrato que amortece (a barriga balançando)
    m = n_de(0.62)
    t = np.arange(m) / SR
    f = varre(rng.uniform(150, 165), 95, m, 1.0) * (1 + 0.3 * np.exp(-t * 6) * np.sin(2 * math.pi * 11 * t))
    fase = 2 * math.pi * np.cumsum(f) / SR
    bloing = satura((np.sin(fase) + 0.5 * np.sin(2 * fase) + 0.25 * np.sin(3 * fase)) * 0.8, 1.6)
    poe(x, _fim(bloing * env(m, 0.008, 0.22) * 0.45, 0.12), bate + 0.02)
    # a pança ainda tremendo: um "blub-blub" curto em cima
    for k in range(3):
        poe(x, _mola(0.09, 260 - 30 * k, 0.15, 30, 20, 0.12 * (1 - 0.25 * k), 0.2), bate + 0.12 + 0.08 * k)
    return reverb(x, 0.3, 0.14)


# ------------------------------------------------------------------ Bart
def estilingue(rng, v):
    """Estilingue: o elástico estica e solta ("twang"), a pedra assobia no ar, "TOCK" seco
    no alvo e a pedrinha quicando no chão."""
    x = _z(1.0)
    # o elástico esticando (rangido curtinho de borracha) e soltando
    n = n_de(0.12)
    t = np.arange(n) / SR
    estica = passa(ruido(rng, n), 600, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 55 * t)) * env(n, 0.04, 0.05) * 0.12
    poe(x, estica, 0)
    m = n_de(0.28)
    t = np.arange(m) / SR
    f = varre(rng.uniform(210, 240), 120, m, 1.4) * (1 + 0.04 * np.sin(2 * math.pi * 28 * t) * np.exp(-t * 10))
    twang = satura(serra_suave(f, m, 12), 1.8) * env(m, 0.001, 0.1) * 0.6
    poe(x, _fim(passa(twang, 90, 4000, 2), 0.06), 0.09)
    poe(x, estalo(rng, n_de(0.02), 1500, 7000, 0.003) * 0.5, 0.09)
    # a pedra cortando o ar
    poe(x, _whoosh(rng, 0.18, 2200, 900, 0.5, g=0.22), 0.11)
    # TOCK: pedra dura batendo
    bate = 0.28
    poe(x, _madeira(rng, n_de(0.25), rng.uniform(820, 900), (0.05, 0.03, 0.015, 0.01), 0.7) * 0.8, bate)
    poe(x, B.soco_leve(rng, v) * 0.45, bate)
    # quiques da pedrinha no chão
    for k, (dt, g) in enumerate(((0.2, 0.3), (0.32, 0.18), (0.4, 0.1))):
        poe(x, _madeira(rng, n_de(0.06), rng.uniform(1300, 1500), (0.015, 0.01, 0.007, 0.005), 0.8) * g, bate + dt)
    return reverb(x, 0.25, 0.12)


# ------------------------------------------------------------------ Bugiganga
def gadget_surpresa(rng, v):
    """Gadget surpresa: o clique da engenhoca, a mola disparando ("boing" que estica), o soco
    da luva, a mola balançando e o "zip" de recolher."""
    x = _z(1.1)
    # clique mecânico (trava soltando)
    n = n_de(0.05)
    poe(x, modal(n, rng.uniform(2400, 2800), rng=rng, **METAL) * env(n, 0.0005, 0.012) * 0.25, 0)
    poe(x, estalo(rng, n, 2500, 9000, 0.004) * 0.5, 0)
    # a mola esticando: boing que sobe
    m = n_de(0.2)
    t = np.arange(m) / SR
    f = varre(180, 520, m, 1.2) * (1 + 0.12 * np.sin(2 * math.pi * 32 * t))
    poe(x, _fim(seno(f, m) * env(m, 0.005, 0.1) * 0.3), 0.02)
    poe(x, _whoosh(rng, 0.16, 600, 3000, 0.8, g=0.4), 0.02)
    bate = 0.15
    poe(x, B.soco_pesado(rng, v), bate, 0.9)
    poe(x, passa(ruido(rng, n_de(0.06)), 700, 3500, 2) * env(n_de(0.06), 0.0005, 0.015) * 0.5, bate)   # o couro da luva
    # a mola balançando depois do soco: "doinnnng"
    poe(x, _mola(0.6, rng.uniform(240, 270), 0.4, 13, 4.5, 0.3), bate + 0.03)
    # recolhe: zip de mola enrolando
    m = n_de(0.18)
    zip_ = graos(rng, m, 18, 0.0, 0.16, 1800, 6000, 0.003) * 0.35
    poe(x, zip_ + _whoosh(rng, 0.18, 3000, 700, 0.3, g=0.25), 0.62)
    return reverb(x, 0.3, 0.13)


# ------------------------------------------------------------------ Danny Phantom
def raio_fantasma(rng, v):
    """Raio fantasma: o disparo de ectoplasma com um zumbido etéreo (tons que flutuam como um
    teremim) e, no fim, um "uuuu" fantasmagórico que se afasta."""
    x = _z(1.3)
    # disparo: "pew" grave e cheio
    n = n_de(0.25)
    f = varre(rng.uniform(1500, 1700), 220, n, 0.6)
    pew = seno(f, n) * env(n, 0.001, 0.07) * 0.55 + seno(f * 1.5, n) * env(n, 0.001, 0.05) * 0.15
    poe(x, pew, 0)
    poe(x, estalo(rng, n_de(0.03), 2000, 9000, 0.005) * 0.4, 0)
    # o raio: zumbido etéreo (duas vozes de seno levemente desafinadas, com vibrato lento)
    m = n_de(0.6)
    t = np.arange(m) / SR
    base = rng.uniform(330, 360)
    vib = 1 + 0.02 * np.sin(2 * math.pi * 5.5 * t)
    voz = seno(base * vib, m) + seno(base * 1.503 * vib, m) * 0.5 + seno(base * 2.01 * (1 + 0.02 * np.sin(2 * math.pi * 4.3 * t)), m) * 0.3
    ar = passa(rosa(rng, m), 900, 5000, 2) * 0.25 * (1 + 0.4 * np.sin(2 * math.pi * 9 * t))
    poe(x, (voz * 0.22 + ar) * janela_suave(m, 0.03, 0.25), 0.02)
    # o impacto: estouro de energia macio
    poe(x, B.impacto_energia(rng, v), 0.14, 0.7)
    # o "uuuu" fantasma que escapa e se afasta
    m = n_de(0.75)
    t = np.arange(m) / SR
    f = varre(rng.uniform(820, 880), 480, m, 0.8) * (1 + 0.035 * np.sin(2 * math.pi * 6 * t))
    uuu = seno(f, m) + 0.3 * seno(f * 2, m)
    poe(x, uuu * sobe_e_some(m, 0.25, 1.5) * 0.16, 0.3)
    return reverb(x, 0.8, 0.38, 7000)


# ------------------------------------------------------------------ Coringa
def flor_de_lapela(rng, v):
    """Flor de lapela: o apertinho de borracha da flor, o esguicho ("psssht") em jato, o
    respingo molhado no alvo e o ácido chiando e borbulhando."""
    x = _z(1.25)
    # o apertão na pera de borracha (guincho curto)
    n = n_de(0.07)
    poe(x, seno(varre(1100, 1500, n, 1), n) * env(n, 0.005, 0.03) * 0.12, 0)
    # o jato: ruído em banda com "tremor" de pressão
    m = n_de(0.32)
    t = np.arange(m) / SR
    jato = passa(ruido(rng, m), 1800, 7000, 2) * (1 + 0.35 * np.sin(2 * math.pi * 38 * t)) * env(m, 0.01, 0.2, segura=0.08)
    poe(x, _fim(jato * 0.45, 0.08), 0.05)
    poe(x, _whoosh(rng, 0.25, 900, 2600, 0.4, g=0.25), 0.05)
    # o respingo no alvo
    bate = 0.24
    m = n_de(0.25)
    splash = passa(ruido(rng, m), 300, 3000, 2) * env(m, 0.002, 0.05)
    poe(x, satura(splash, 2) * 0.6, bate)
    poe(x, B.soco_leve(rng, v) * 0.35, bate)
    for k in range(4):                                                                 # gotas caindo
        poe(x, _bolha(rng, rng.uniform(700, 1100), 0.04, 0.1), bate + 0.05 + rng.uniform(0, 0.15))
    # o chiado do ácido: ruído agudo com crepitar
    m = n_de(0.85)
    t = np.arange(m) / SR
    chiado = passa(ruido(rng, m), 4000, 11000, 2) * env(m, 0.04, 0.35) * 0.3
    chiado += graos(rng, m, 50, 0.0, 0.6, 2500, 9000, 0.003) * 0.3
    poe(x, _fim(chiado, 0.2), bate + 0.04)
    # as bolhas borbulhando
    for k in range(9):
        poe(x, _bolha(rng, rng.uniform(260, 520), rng.uniform(0.05, 0.08), 0.16 * rng.uniform(0.6, 1)), bate + 0.12 + k * 0.07 + rng.uniform(-0.02, 0.02))
    return reverb(x, 0.3, 0.15)


# ------------------------------------------------------------------ Arlequina
def taco_de_beisebol(rng, v):
    """Taco de beisebol: o giro cortando o ar ("vuuum"), o "CRACK" seco de madeira na pancada,
    o peso do golpe e um "plim" brincalhão (o coraçãozinho)."""
    x = _z(1.0)
    n = n_de(0.28)
    poe(x, assobio(rng, n, 250, 2200, 1.4, 0.55) * sobe_e_some(n, 0.85, 1.6) * 0.9, 0)
    bate = 0.24
    # crack: madeira maciça, estalo bem brilhante e curto
    poe(x, _madeira(rng, n_de(0.35), rng.uniform(560, 620), (0.09, 0.045, 0.025, 0.015), 1.0) * 0.8, bate)
    poe(x, satura(passa(ruido(rng, n_de(0.04)), 2000, 10000, 2) * env(n_de(0.04), 0.0002, 0.005), 2) * 0.8, bate)
    poe(x, B.soco_pesado(rng, v), bate, 0.55)
    # "plim": duas notinhas subindo (o coração)
    poe(x, _fim(_brilho(rng, 0.35, nota(88), 0.12, CRISTAL), 0.1), bate + 0.18)
    poe(x, _fim(_brilho(rng, 0.4, nota(93), 0.12, CRISTAL), 0.1), bate + 0.25)
    return reverb(x, 0.3, 0.14)


# ------------------------------------------------------------------ Capitão Planeta
def raio_de_gaia(rng, v):
    """Raio de Gaia: cinco notas de cristal (os cinco anéis) se juntam num acorde, o raio limpo
    sobe e acerta com um brilho largo e sem sujeira."""
    x = _z(1.3)
    escala = [72, 74, 76, 79, 81]                                   # pentatônica: cinco pontos de luz
    for k, m in enumerate(escala):
        poe(x, _fim(_brilho(rng, 0.5, nota(m), 0.07, CRISTAL), 0.1), 0.025 * k)
    # o raio: acorde de senos puros que sobe e brilha
    n = n_de(0.55)
    t = np.arange(n) / SR
    sobe = varre(1.0, 1.06, n, 1.5)
    acorde = sum(seno(nota(m) * sobe * (1 + 0.004 * np.sin(2 * math.pi * (5 + k) * t)), n) * g
                 for k, (m, g) in enumerate(((55, 0.5), (62, 0.35), (67, 0.3), (74, 0.2), (79, 0.12))))
    ar = passa(rosa(rng, n), 2500, 9000, 2) * 0.08
    poe(x, (acorde * 0.3 + ar) * janela_suave(n, 0.05, 0.25), 0.12)
    poe(x, _whoosh(rng, 0.2, 800, 4000, 0.9, g=0.25), 0.1)
    # o impacto limpo
    bate = 0.3
    poe(x, B.impacto_energia(rng, v), bate, 0.75)
    m = n_de(0.9)
    brilho = sum(modal(m, nota(k), rng=rng, **CRISTAL) for k in (84, 88, 91)) * env(m, 0.002, 0.35) * 0.06
    poe(x, _fim(brilho, 0.2), bate + 0.01)
    return reverb(x, 0.65, 0.3, 10000)


# ------------------------------------------------------------------ Scooby / Coragem
def mordida_cartoon(rng, v):
    """Mordida de desenho: o ar da boca abrindo, o CHOMP (dentões batendo e a mordida cheia)
    e os dentes batendo de medo logo depois."""
    x = _z(0.95)
    poe(x, _whoosh(rng, 0.16, 500, 2000, 0.6, g=0.35), 0)
    bate = 0.17
    # CHOMP: o estalo dos dentes, a bocada carnuda e um "nhac" de boca
    poe(x, _clique_dente(rng, rng.uniform(1700, 1900), 0.45), bate)
    m = n_de(0.22)
    chomp = baque(m, 210, 100, 0.07, 0.2) * 0.7 + satura(passa(ruido(rng, m), 350, 2600, 2) * env(m, 0.002, 0.05), 3) * 0.8
    poe(x, chomp, bate)
    n = n_de(0.12)
    nhac = seno(varre(520, 300, n, 1), n) * env(n, 0.003, 0.06) * 0.35                      # o tom "cômico" da bocada
    poe(x, _fim(satura(nhac, 2), 0.03), bate + 0.005)
    # tremedeira: os dentes batendo de medo (mais rápidos e fracos)
    t0 = bate + 0.2
    for k in range(6):
        poe(x, _clique_dente(rng, rng.uniform(2100, 2500), 0.3 * (1 - 0.1 * k)), t0 + k * 0.045)
        poe(x, _tom(nota(70 - k), nota(68 - k), 0.03, 0.012, 0.08), t0 + k * 0.045)
    return reverb(x, 0.22, 0.1)



def dardo_crescente(rng, v):
    """Dardos crescentes do Cavaleiro da Lua: três giros cortando o ar, cada um termina num "tchak"
    seco de lâmina cravando (sem metal ressoando), e um sopro grave e frio da lua no fim."""
    x = _z(1.15)
    for i in range(3):
        t0 = 0.04 + 0.1 * i
        n = n_de(0.2)
        tt = np.arange(n) / SR
        # o giro: um sopro que pulsa a cada volta do dardo e sobe de tom ao chegar
        giro = assobio(rng, n, 1400, 3200, 1.3, 0.35) * (0.55 + 0.45 * np.sin(2 * math.pi * (26 + 14 * tt / tt[-1]) * tt) ** 2)
        poe(x, giro * sobe_e_some(n, 0.85, 1.3) * 0.5, t0)
        # o cravar: estalo curto e abafado, com um baque pequeno de corpo
        poe(x, passa(estalo(rng, n_de(0.05), 900, 5200, 0.006), None, 6000, 2) * 0.9, t0 + 0.19)
        poe(x, baque(n_de(0.12), 190, 110, 0.03, 0.5) * 0.45, t0 + 0.19)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 180, 1200, 2) * sobe_e_some(n, 0.35, 1.6) * 0.12, 0.42)
    return reverb(x, 0.28, 0.12, 6000)

SONS: dict = {
    "barrigada": (barrigada, "básico do Homer: o ar do empurrão, o baque da pança e o \"bloing\" de gelatina"),
    "estilingue": (estilingue, "básico do Bart: twang do elástico, a pedra assobiando e o \"tock\" seco"),
    "gadget-surpresa": (gadget_surpresa, "básico do Bugiganga: clique, a mola \"boing\", o soco da luva e o zip de recolher"),
    "raio-fantasma": (raio_fantasma, "básico do Danny Phantom: disparo de ectoplasma com zumbido etéreo e um \"uuuu\" fantasma"),
    "flor-de-lapela": (flor_de_lapela, "básico do Coringa: o esguicho da flor, o respingo e o ácido chiando e borbulhando"),
    "taco-de-beisebol": (taco_de_beisebol, "básico da Arlequina: o giro do taco, o \"crack\" de madeira e um plim"),
    "raio-de-gaia": (raio_de_gaia, "básico do Capitão Planeta: cinco notas de cristal que viram um raio limpo e brilhante"),
    "dardo-crescente": (dardo_crescente, "básico do Cavaleiro da Lua: três dardos girando que cravam seco, e o sopro frio da lua"),
    "mordida-cartoon": (mordida_cartoon, "básico do Scooby e do Coragem: \"chomp\" de desenho e os dentes batendo de medo"),
}
