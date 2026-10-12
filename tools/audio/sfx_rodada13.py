"""Os sons da rodada 13: Capitã Marvel, Demolidor, Justiceiro, Motoqueiro Fantasma e Blade (veja
tools/vfx/familias_v2/rodada13.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _fogo(rng, seg, g=0.3, lo=150, hi=3500):
    """O fogo rugindo: o ruído grave que ondula com os estalos das chamas."""
    n = n_de(seg)
    t = _t(n)
    x = passa(rosa(rng, n), lo, hi, 2) * (0.6 + 0.4 * np.abs(np.sin(2 * math.pi * 5 * t + rng.uniform(0, 6))))
    x += graos(rng, n, int(seg * 40), 0.0, seg, 1500, 6000, 0.004) * 0.6
    return x * sobe_e_some(n, 0.35, 1.3) * g


def _zap(rng, seg, g=0.3):
    """O estalo elétrico: o chiado áspero que pisca."""
    n = n_de(seg)
    t = _t(n)
    pisca = (np.sin(2 * math.pi * 47 * t) > 0.2).astype(float) * 0.6 + 0.4
    return satura(passa(rosa(rng, n), 1200, 9000, 2) * pisca, 2.5) * sobe_e_some(n, 0.2, 1.3) * g


def _batida(rng, g=0.5):
    x = _z(0.4)
    poe(x, passa(baque(n_de(0.22), 72, 42, 0.08, 0.05), None, 1000, 2) * g, 0.0)
    poe(x, passa(baque(n_de(0.22), 64, 40, 0.07, 0.04), None, 1000, 2) * g * 0.7, 0.15)
    return x


def _tiro(rng, g=0.8, grave=1.0):
    """O estampido: o estalo seco e o corpo grave, com a cauda que se espalha."""
    n = n_de(0.5)
    corpo = baque(n, 110 * grave, 45, 0.12, 1.0) * 0.9
    estouro = passa(rosa(rng, n), 300, 8000, 2) * env(n, 0.0005, 0.08) * 1.2
    return satura(corpo + estouro, 1.6) * g


def _bastao_bate(rng, g=0.5):
    """O bastão de madeira batendo: o "toc" seco, oco."""
    n = n_de(0.15)
    return (modal(n, 620, rng=rng, razoes=[1.0, 2.3, 4.1], quedas=[0.05, 0.03, 0.02], ganhos=[1, 0.5, 0.3]) * 0.8
            + estalo(rng, n, 1500, 6000, 0.006) * 0.6 + baque(n, 180, 110, 0.03, 0.3) * 0.4) * g


# =================================================================== Capitã Marvel
def absorcao_cosmica(rng, v):
    """A absorção cósmica: a energia sendo sugada (os "vuu" que vêm de todos os lados e entram), a aura
    acendendo (o fogo cósmico com o zumbido dourado) e o anel fechando (o sino cheio)."""
    x = _z(1.8)
    for k in range(8):
        m = n_de(0.2)
        poe(x, seno(varre(1400 - 80 * k, 400, m, 1.0), m) * sobe_e_some(m, 0.8, 1.3) * 0.04, 0.03 * k)
    poe(x, passa(rosa(rng, n_de(0.45)), 1500, 7000, 2) * np.linspace(0, 1, n_de(0.45)) ** 2 * 0.3, 0.0)
    poe(x, _fogo(rng, 1.0, 0.25, 300, 5000), 0.3)
    n = n_de(0.9)
    poe(x, (seno(220, n) + seno(330, n) * 0.6) * sobe_e_some(n, 0.3, 1.3) * 0.06, 0.35)
    poe(x, _brilho(rng, 1.0, 660, 0.15, SINO), 0.6)
    return reverb(x, 0.55, 0.28)


def rajada_binaria(rng, v):
    """A rajada binária: os dois raios de fóton (o zumbido duplo que bate entre si, um pouco desafinado), e a
    bola estalando no rival (os choques elétricos)."""
    x = _z(1.6)
    n = n_de(0.55)
    t = _t(n)
    duplo = (seno(310, n) + seno(318, n)) * 0.5 + passa(rosa(rng, n), 1500, 7000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 30 * t))
    poe(x, satura(duplo, 1.8) * sobe_e_some(n, 0.15, 1.4) * 0.3, 0.0)
    poe(x, _whoosh(rng, 0.25, 600, 3000, 0.8, 1.3, 0.4), 0.0)
    poe(x, baque(n_de(0.35), 120, 60, 0.1, 0.6) * 0.55, 0.22)
    for k in range(4):
        poe(x, _zap(rng, 0.12, 0.25), 0.3 + 0.1 * k)
    return reverb(x, 0.45, 0.22)


def binario_preparo(rng, v):
    """O Preparo da Explosão binária: o corpo em chamas cósmicas (o fogo grave que cresce) e o zumbido dourado
    subindo, com a estrela pulsando (os tons em acorde)."""
    x = _z(1.4)
    poe(x, _fogo(rng, 1.2, 0.3, 120, 3000), 0.0)
    n = n_de(1.2)
    for k, f in enumerate((165, 247, 330)):
        poe(x, seno(varre(f, f * 1.25, n, 1.0), n) * sobe_e_some(n, 0.85, 1.1) * 0.04, 0.0)
    return reverb(x, 0.55, 0.28)


def explosao_binaria(rng, v):
    """A Explosão binária: a energia se fechando (o som sugado que sobe), o estouro enorme (o estrondo com o
    brilho que abre e a cauda longa) e os choques travando (os estalos elétricos espalhados)."""
    x = _z(2.2)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 300, 6000, 2) * np.linspace(0, 1, n) ** 2 * 0.5, 0.0)
    poe(x, seno(varre(200, 900, n, 2.0), n) * np.linspace(0, 1, n) ** 2 * 0.08, 0.0)
    poe(x, baque(n_de(1.0), 58, 28, 0.38, 1.0) * 1.0, 0.27)
    m = n_de(1.1)
    poe(x, passa(rosa(rng, m), 50, 4000, 2) * env(m, 0.002, 0.55) * 0.6, 0.27)
    poe(x, _brilho(rng, 1.2, 880, 0.15, CRISTAL), 0.3)
    for k in range(6):
        poe(x, _zap(rng, 0.1, 0.2), 0.6 + 0.09 * k)
    return reverb(x, 0.7, 0.32)


# =================================================================== Demolidor
def radar_sensorial(rng, v):
    """O radar do Demolidor: o mundo em silêncio e as ondas de som passando (os "pings" graves e ocos que se
    espalham com eco), e o coração do rival batendo forte, perto."""
    x = _z(1.8)
    for k in range(4):
        m = n_de(0.5)
        poe(x, (seno(varre(700, 520, m, 1.0), m) * env(m, 0.003, 0.35) * 0.08), 0.12 * k)
        poe(x, passa(rosa(rng, m), 300, 1200, 2) * env(m, 0.003, 0.3) * 0.08, 0.12 * k)
    poe(x, _batida(rng, 0.7), 0.5)
    poe(x, _batida(rng, 0.7), 0.85)
    return reverb(x, 0.65, 0.35)


def bastoes_em_cruz(rng, v):
    """Os bastões em cruz: os dois bastões girando no ar (o "vupvupvup" rápido), batendo juntos no rival (dois
    "tocs" quase ao mesmo tempo e o baque) e ricocheteando (o toc mais leve e o assobio indo embora)."""
    x = _z(1.5)
    n = n_de(0.32)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 500, 3000, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 14 * t))) * sobe_e_some(n, 0.8, 1.2) * 0.35, 0.0)
    poe(x, _bastao_bate(rng, 0.6), 0.29)
    poe(x, _bastao_bate(rng, 0.55), 0.31)
    poe(x, baque(n_de(0.3), 130, 65, 0.08, 0.5) * 0.5, 0.3)
    poe(x, _whoosh(rng, 0.35, 1500, 600, 0.3, 1.3, 0.3), 0.36)
    poe(x, _bastao_bate(rng, 0.25), 0.62)
    return reverb(x, 0.4, 0.2)


def demolidor_preparo(rng, v):
    """O Preparo do Contra-ataque cego: o silêncio atento (o zumbido baixinho), os pings do radar em pulsos e as
    batidas dos corações em volta, cada uma num ritmo."""
    x = _z(1.4)
    n = n_de(1.2)
    poe(x, seno(60, n) * sobe_e_some(n, 0.5, 1.2) * 0.06, 0.0)
    for k in range(3):
        m = n_de(0.4)
        poe(x, seno(varre(650, 500, m, 1.0), m) * env(m, 0.003, 0.25) * 0.06, 0.33 * k)
    for k, t0 in enumerate((0.15, 0.55, 0.9)):
        poe(x, _batida(rng, 0.35), t0)
    return reverb(x, 0.6, 0.32)


def contra_ataque_cego(rng, v):
    """O contra-ataque cego: a rajada de golpes de bastão de todos os lados (os "tocs" secos, rápidos e cada um
    num tom), e o golpe final de cima (o assobio que desce e o estrondo)."""
    x = _z(1.8)
    for k in range(6):
        poe(x, _whoosh(rng, 0.1, 900, 2500, 0.6, 1.2, 0.18), 0.08 * k)
        poe(x, _bastao_bate(rng, 0.45), 0.08 * k + 0.07)
        poe(x, baque(n_de(0.15), 160 + 15 * k, 90, 0.04, 0.4) * 0.3, 0.08 * k + 0.07)
    poe(x, _whoosh(rng, 0.25, 2500, 500, 0.7, 1.3, 0.5), 0.5)
    poe(x, baque(n_de(0.6), 80, 38, 0.2, 0.9) * 0.95, 0.68)
    poe(x, _bastao_bate(rng, 0.7), 0.68)
    return reverb(x, 0.5, 0.25)


# =================================================================== Justiceiro
def mira_fria(rng, v):
    """A mira fria: a luneta girando no ajuste (os cliques do anel de foco), a respiração presa (o sopro que
    some), a trava (o clique metálico firme) e o tom frio e grave que fica."""
    x = _z(1.7)
    for k in range(7):
        n = n_de(0.04)
        poe(x, (estalo(rng, n, 2500, 8000, 0.003) * 0.4 + modal(n, 2800 + 100 * k, rng=rng, **METAL) * env(n, 0.0005, 0.012) * 0.2), 0.05 + 0.045 * k)
    m = n_de(0.4)
    poe(x, passa(rosa(rng, m), 400, 2000, 2) * sobe_e_some(m, 0.3, 1.3) * 0.12, 0.1)
    poe(x, modal(n_de(0.3), 1700, rng=rng, **METAL) * env(n_de(0.3), 0.0005, 0.08) * 0.3 + estalo(rng, n_de(0.3), 1500, 6000, 0.008) * 0.5, 0.42)
    n = n_de(0.9)
    poe(x, (seno(73, n) + seno(110, n) * 0.4) * sobe_e_some(n, 0.15, 1.4) * 0.12, 0.45)
    return reverb(x, 0.5, 0.25)


def sniper_preparo(rng, v):
    """O Preparo do Alvo confirmado: a respiração lenta (inspira e solta, abafada), o ferrolho sendo armado (o
    "tclac" metálico) e o vento passando lá fora."""
    x = _z(1.4)
    for k, (t0, seg) in enumerate(((0.0, 0.5), (0.6, 0.55))):
        n = n_de(seg)
        poe(x, passa(rosa(rng, n), 300, 1800, 2) * sobe_e_some(n, 0.5 if k == 0 else 0.25, 1.4) * 0.12, t0)
    poe(x, modal(n_de(0.2), 1300, rng=rng, **METAL) * env(n_de(0.2), 0.0005, 0.05) * 0.3 + estalo(rng, n_de(0.2), 1200, 6000, 0.006) * 0.4, 0.45)
    poe(x, modal(n_de(0.2), 1600, rng=rng, **METAL) * env(n_de(0.2), 0.0005, 0.05) * 0.3 + estalo(rng, n_de(0.2), 1200, 6000, 0.006) * 0.4, 0.55)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 150, 700, 2) * sobe_e_some(n, 0.5, 1.2) * 0.1, 0.0)
    return reverb(x, 0.5, 0.25)


def alvo_confirmado(rng, v):
    """O tiro de precisão: o estampido grande do rifle (com o eco longo), o estalo supersônico da bala cortando o
    ar, o impacto pesado no rival e o cartucho caindo (o tilintar)."""
    x = _z(2.0)
    poe(x, _tiro(rng, 1.0, 0.8), 0.0)
    m = n_de(0.08)
    poe(x, passa(rosa(rng, m), 3000, 10000, 2) * env(m, 0.0005, 0.03) * 0.6, 0.04)
    poe(x, baque(n_de(0.5), 95, 40, 0.15, 0.9) * 0.85, 0.11)
    poe(x, passa(rosa(rng, n_de(0.4)), 200, 4000, 2) * env(n_de(0.4), 0.001, 0.2) * 0.35, 0.11)
    for k in range(3):
        poe(x, modal(n_de(0.25), 3400 - 200 * k, rng=rng, **METAL) * env(n_de(0.25), 0.0005, 0.08) * (0.12 - 0.03 * k), 0.75 + 0.1 * k)
    return reverb(x, 0.7, 0.3)


# =================================================================== Motoqueiro Fantasma
def olhar_de_penitencia(rng, v):
    """O olhar de penitência: a caveira acendendo em chamas (o "fwoomp" do fogo pegando e o rugido), os olhos
    acesos (o tom grave e sombrio) e a onda de fogo do inferno correndo pelo chão; as almas gemendo baixinho."""
    x = _z(2.0)
    m = n_de(0.3)
    poe(x, passa(rosa(rng, m), 100, 2500, 2) * env(m, 0.01, 0.2) * 0.6, 0.0)
    poe(x, _fogo(rng, 1.4, 0.35, 120, 3500), 0.05)
    n = n_de(0.8)
    poe(x, satura(seno(55, n) + seno(82, n) * 0.5, 2) * sobe_e_some(n, 0.3, 1.3) * 0.12, 0.15)
    poe(x, _whoosh(rng, 0.6, 300, 1400, 0.5, 1.3, 0.45), 0.3)
    for k in range(3):
        g = n_de(0.5)
        t = _t(g)
        poe(x, seno(varre(420 - 40 * k, 300, g, 1.0) * (1 + 0.03 * np.sin(2 * math.pi * 6 * t)), g) * sobe_e_some(g, 0.4, 1.3) * 0.025, 0.5 + 0.15 * k)
    return reverb(x, 0.65, 0.32)


def penitencia_preparo(rng, v):
    """O Preparo do Penance Stare: o fogo da cabeça rugindo baixo e o motor da moto do inferno ao fundo (o
    ronco grave que pulsa)."""
    x = _z(1.4)
    poe(x, _fogo(rng, 1.2, 0.3), 0.0)
    n = n_de(1.2)
    t = _t(n)
    f = 45 + 5 * np.sin(2 * math.pi * 1.5 * t)
    ronco = satura(np.sin(2 * math.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * (np.sin(2 * math.pi * 18 * t) > 0)), 3)
    poe(x, passa(ronco, 60, 1200, 2) * sobe_e_some(n, 0.5, 1.2) * 0.15, 0.0)
    return reverb(x, 0.5, 0.25)


def penance_stare(rng, v):
    """O Penance Stare: os olhos acendendo (o "vwoom" grave), os raios em espiral (o tom que gira e treme), e
    dentro do rival as almas gritando em redemoinho (as vozes agudas e distorcidas que giram) com o fogo subindo."""
    x = _z(2.0)
    m = n_de(0.3)
    poe(x, seno(varre(80, 160, m, 1.0), m) * sobe_e_some(m, 0.4, 1.3) * 0.15, 0.0)
    n = n_de(0.6)
    t = _t(n)
    poe(x, seno(500 + 120 * np.sin(2 * math.pi * 8 * t), n) * sobe_e_some(n, 0.3, 1.3) * 0.05, 0.12)
    for k in range(4):
        g = n_de(0.6)
        tt = _t(g)
        f = (700 + 150 * k) * (1 + 0.08 * np.sin(2 * math.pi * (4 + k) * tt))
        grito = satura(np.sin(2 * math.pi * np.cumsum(f) / SR), 2) * passa(rosa(rng, g), 500, 4000, 2) * 2
        poe(x, grito * sobe_e_some(g, 0.4, 1.3) * 0.05, 0.35 + 0.08 * k)
    poe(x, _fogo(rng, 1.0, 0.3), 0.45)
    return reverb(x, 0.65, 0.32)


# =================================================================== Blade
def rastreio_vampirico(rng, v):
    """O rastreio: o farejar (duas inspiradas curtas pelo nariz), o rastro de sangue (o gotejar), as presas do
    vampiro aparecendo (o sibilo) e a marca do caçador (o corte seco de lâmina)."""
    x = _z(1.7)
    for k in range(2):
        m = n_de(0.12)
        poe(x, passa(rosa(rng, m), 1500, 6000, 2) * sobe_e_some(m, 0.6, 1.2) * 0.25, 0.02 + 0.16 * k)
    for k in range(5):
        g = n_de(0.08)
        poe(x, seno(varre(900 - 60 * k, 400, g, 1.0), g) * env(g, 0.002, 0.05) * 0.06, 0.3 + 0.07 * k)
    h = n_de(0.4)
    poe(x, passa(rosa(rng, h), 3500, 9000, 2) * sobe_e_some(h, 0.3, 1.3) * 0.2, 0.32)
    poe(x, _whoosh(rng, 0.15, 2000, 5000, 0.6, 1.2, 0.35), 0.5)
    poe(x, modal(n_de(0.4), 3100, rng=rng, **METAL) * env(n_de(0.4), 0.0005, 0.15) * 0.15, 0.6)
    return reverb(x, 0.5, 0.25)


def lamina_de_prata(rng, v):
    """A lâmina de prata: a espada saindo da bainha (o "shhhing" metálico comprido), o corte (o assobio seco e o
    tinido de prata) e o sangue sendo puxado de volta (o som molhado que volta)."""
    x = _z(1.7)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 3000, 10000, 2) * sobe_e_some(n, 0.6, 1.2) * 0.3 + modal(n, 3600, rng=rng, **METAL) * env(n, 0.05, 0.2) * 0.1, 0.0)
    poe(x, _whoosh(rng, 0.2, 1500, 6000, 0.7, 1.2, 0.6), 0.12)
    poe(x, _brilho(rng, 0.7, 2400, 0.2, VIDRO), 0.18)
    poe(x, estalo(rng, n_de(0.03), 2000, 8000, 0.006) * 0.5, 0.18)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 200, 1800, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 9 * _t(m))) * sobe_e_some(m, 0.6, 1.3) * 0.25, 0.5)
    return reverb(x, 0.5, 0.25)


def caca_preparo(rng, v):
    """O Preparo da Caçada noturna: a glaive girando na mão (o "vum-vum-vum" que acelera) e o vento da noite."""
    x = _z(1.4)
    n = n_de(1.2)
    t = _t(n)
    f = 4 + 6 * t
    gira = np.abs(np.sin(2 * math.pi * np.cumsum(f) / SR))
    poe(x, passa(rosa(rng, n), 600, 4000, 2) * gira * sobe_e_some(n, 0.8, 1.2) * 0.4, 0.0)
    poe(x, passa(rosa(rng, n), 200, 900, 2) * sobe_e_some(n, 0.5, 1.2) * 0.08, 0.0)
    return reverb(x, 0.55, 0.28)


def cacada_noturna(rng, v):
    """A caçada noturna: a glaive voando e girando em volta (o zumbido que passa de um lado para o outro), os três
    cortes ao passar (os "tching" metálicos) e o golpe final em X (dois cortes e o baque)."""
    x = _z(2.0)
    n = n_de(0.6)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 800, 5000, 2) * np.abs(np.sin(2 * math.pi * 22 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.35, 0.05)
    for k, t0 in enumerate((0.2, 0.37, 0.54)):
        poe(x, modal(n_de(0.35), 2600 + 300 * k, rng=rng, **METAL) * env(n_de(0.35), 0.0005, 0.12) * 0.2, t0)
        poe(x, _whoosh(rng, 0.12, 1500, 5000, 0.7, 1.2, 0.3), t0 - 0.04)
    for k in range(2):
        poe(x, _whoosh(rng, 0.15, 1200, 5500, 0.7, 1.2, 0.5), 0.62 + 0.04 * k)
        poe(x, estalo(rng, n_de(0.03), 2000, 9000, 0.008) * 0.6, 0.7 + 0.04 * k)
    poe(x, baque(n_de(0.45), 90, 42, 0.15, 0.7) * 0.8, 0.72)
    return reverb(x, 0.55, 0.28)


SONS: dict = {
    "absorcao-cosmica": (absorcao_cosmica, "Capitã Marvel: a energia sugada e a aura"),
    "rajada-binaria": (rajada_binaria, "Capitã Marvel: os dois raios de fóton e os choques"),
    "binario-preparo": (binario_preparo, "Capitã Marvel: as chamas cósmicas (antes do golpe)"),
    "explosao-binaria": (explosao_binaria, "Capitã Marvel: a estrela explodindo e os choques"),
    "radar-sensorial": (radar_sensorial, "Demolidor: as ondas do radar e o coração"),
    "bastoes-em-cruz": (bastoes_em_cruz, "Demolidor: os bastões girando e batendo"),
    "demolidor-preparo": (demolidor_preparo, "Demolidor: o radar e os corações (antes do golpe)"),
    "contra-ataque-cego": (contra_ataque_cego, "Demolidor: a rajada de golpes e o final"),
    "mira-fria": (mira_fria, "Justiceiro: a luneta ajustando e travando"),
    "sniper-preparo": (sniper_preparo, "Justiceiro: a respiração e o ferrolho (antes do tiro)"),
    "alvo-confirmado": (alvo_confirmado, "Justiceiro: o tiro de rifle e o impacto"),
    "olhar-de-penitencia": (olhar_de_penitencia, "Motoqueiro: a caveira em chamas e a onda de fogo"),
    "penitencia-preparo": (penitencia_preparo, "Motoqueiro: o fogo e o motor (antes do golpe)"),
    "penance-stare": (penance_stare, "Motoqueiro: os olhos, a espiral e as almas"),
    "rastreio-vampirico": (rastreio_vampirico, "Blade: o farejar, as presas e a marca"),
    "lamina-de-prata": (lamina_de_prata, "Blade: a espada de prata e o sangue de volta"),
    "caca-preparo": (caca_preparo, "Blade: a glaive girando (antes do golpe)"),
    "cacada-noturna": (cacada_noturna, "Blade: a glaive cortando e o X final"),
}
