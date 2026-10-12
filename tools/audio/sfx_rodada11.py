"""Os sons da rodada 11: Loid, Yor, Jinwoo, Kaneki e Yugi (veja tools/vfx/familias_v2/rodada11.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _rasgo(rng, seg, lo=800, hi=6000, g=0.4):
    """Papel ou pano rasgando: o ruído áspero em fibras (pequenos estalos bem juntos)."""
    n = n_de(seg)
    fibras = graos(rng, n, int(seg * 260), 0.0, seg, lo, hi, 0.004, 0.7)
    return (fibras * 0.8 + passa(rosa(rng, n), lo, hi, 2) * 0.25) * sobe_e_some(n, 0.35, 1.2) * g


def _clique(rng, g=0.4, f=3200):
    n = n_de(0.05)
    return (estalo(rng, n, 2000, 9000, 0.004) + modal(n, f, rng=rng, **METAL) * env(n, 0.0005, 0.02) * 0.4) * g


def _batida_de_coracao(rng, g=0.6):
    """O "tum-tum": dois baques graves e abafados, o segundo mais fraco."""
    x = _z(0.45)
    poe(x, passa(baque(n_de(0.25), 70, 40, 0.09, 0.05), None, 900, 2) * g, 0.0)
    poe(x, passa(baque(n_de(0.25), 62, 38, 0.08, 0.04), None, 900, 2) * g * 0.7, 0.16)
    return x


def _molhado(rng, seg, g=0.3, lo=150, hi=1800):
    """O som orgânico e molhado: ruído grave com bolhas (pequenos tons que caem)."""
    n = n_de(seg)
    x = passa(rosa(rng, n), lo, hi, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 7 * _t(n) + rng.uniform(0, 6)))) * sobe_e_some(n, 0.5, 1.3) * g
    for _ in range(int(seg * 14)):
        m = n_de(0.05)
        poe(x, seno(varre(rng.uniform(250, 600), 120, m, 1.0), m) * env(m, 0.002, 0.04) * g * 0.35, rng.uniform(0, seg * 0.9))
    return x


def _carta(rng, g=0.3):
    """Uma carta estalando: o "flap" de papelão seco."""
    n = n_de(0.06)
    return (passa(rosa(rng, n), 1200, 7000, 2) * env(n, 0.001, 0.03) + estalo(rng, n, 3000, 9000, 0.003) * 0.6) * g


# =================================================================== Loid
def identidade_falsa(rng, v):
    """O disfarce caindo: o rasgo seco da máscara, o tique-tique da mira girando, o "bip-bip" da trava e o
    tom que desce (Enfraquecido)."""
    x = _z(1.7)
    m = n_de(0.25)
    poe(x, seno(varre(500, 700, m, 1.0), m) * sobe_e_some(m, 0.5, 1.4) * 0.05, 0.0)
    poe(x, _rasgo(rng, 0.32, 900, 7000, 0.55), 0.3)
    poe(x, _whoosh(rng, 0.3, 1500, 400, 0.3, 1.4, 0.25), 0.4)
    for k in range(6):
        poe(x, _clique(rng, 0.22 - 0.02 * k, 3800), 0.42 + 0.04 * k)
    for k in range(2):
        n = n_de(0.07)
        poe(x, seno(1760 if k else 1320, n) * env(n, 0.002, 0.06) * 0.1, 0.65 + 0.09 * k)
    m = n_de(0.5)
    poe(x, seno(varre(420, 210, m, 1.0), m) * sobe_e_some(m, 0.2, 1.3) * 0.06, 0.82)
    return reverb(x, 0.4, 0.2)


def neutralizacao_silenciosa(rng, v):
    """O tiro com silenciador: o "pft" abafado, o ferrolho voltando (o clique metálico), a bala zunindo
    curta, o impacto seco, e a barra do Preparo quebrando como vidro, os cacos caindo."""
    x = _z(1.6)
    n = n_de(0.12)
    pft = passa(rosa(rng, n), 300, 2600, 2) * env(n, 0.0008, 0.05) * 0.7 + passa(baque(n, 180, 90, 0.03, 0.1), None, 1200, 2) * 0.3
    poe(x, pft, 0.0)
    poe(x, _clique(rng, 0.35, 2600), 0.05)
    poe(x, _clique(rng, 0.25, 3100), 0.09)
    poe(x, _whoosh(rng, 0.12, 4000, 1800, 0.4, 1.2, 0.25), 0.07)
    poe(x, baque(n_de(0.18), 150, 80, 0.04, 0.6) * 0.45, 0.2)
    poe(x, estalo(rng, n_de(0.03), 2500, 8000) * 0.5, 0.2)
    q = n_de(0.6)
    poe(x, modal(q, 2900, rng=rng, desafina=0.04, **VIDRO) * env(q, 0.0005, 0.25) * 0.22, 0.26)
    poe(x, graos(rng, n_de(0.6), 14, 0.05, 0.5, 3000, 9000, 0.005) * 0.35, 0.3)
    return reverb(x, 0.35, 0.18)


def plano_de_fuga(rng, v):
    """A bomba de fumaça: o arremesso curto, o quique metálico com o pavio chiando, o "puff" fofo e grande,
    o chiado da fumaça saindo, e a fuga (os passos rápidos sumindo num "fwoosh")."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.2, 700, 1800, 0.5, 1.3, 0.25), 0.0)
    n = n_de(0.22)
    poe(x, passa(rosa(rng, n), 4000, 10000, 2) * sobe_e_some(n, 0.4, 1.2) * 0.12, 0.02)
    poe(x, modal(n_de(0.12), 1500, rng=rng, **METAL) * env(n_de(0.12), 0.001, 0.05) * 0.12, 0.18)
    m = n_de(0.8)
    puff = passa(rosa(rng, m), 80, 1400, 2) * env(m, 0.004, 0.35) * 0.75 + baque(m, 90, 45, 0.15, 0.1) * 0.35
    poe(x, puff, 0.2)
    h = n_de(0.9)
    poe(x, passa(rosa(rng, h), 2500, 8000, 2) * sobe_e_some(h, 0.2, 1.4) * 0.14, 0.28)
    for k in range(5):
        p = n_de(0.06)
        poe(x, passa(baque(p, 160, 100, 0.03, 0.3), None, 2500, 2) * (0.22 - 0.035 * k), 0.45 + 0.08 * k)
    poe(x, _whoosh(rng, 0.45, 600, 2600, 0.6, 1.4, 0.4), 0.8)
    return reverb(x, 0.45, 0.22)


# =================================================================== Yor
def investida_elegante(rng, v):
    """O chute alto girando: o vestido e a perna cortando o ar (o "fwiiish" que sobe e gira), o calcanhar
    acertando (o estalo seco e o baque), as pétalas farfalhando e o formigar do Paralisado."""
    x = _z(1.6)
    poe(x, _whoosh(rng, 0.38, 500, 3200, 0.75, 1.3, 0.75), 0.0)
    poe(x, baque(n_de(0.3), 140, 60, 0.06, 0.7) * 0.6, 0.32)
    poe(x, estalo(rng, n_de(0.03), 1800, 7000, 0.006) * 0.7, 0.32)
    poe(x, graos(rng, n_de(0.7), 40, 0.0, 0.6, 3000, 9000, 0.004, 0.8) * 0.25, 0.35)
    poe(x, graos(rng, n_de(0.5), 30, 0.0, 0.45, 5000, 11000, 0.002, 0.6) * 0.18, 0.5)
    return reverb(x, 0.45, 0.22)


def espinho_preparo(rng, v):
    """O Preparo do Jardim noturno: os ramos rangendo devagar (o ranger grave e fibroso) e o brilho fino
    dos estiletes (o "tsiing" agudo, baixinho)."""
    x = _z(1.3)
    n = n_de(1.1)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 1200, 2) * (0.4 + 0.6 * np.abs(np.sin(2 * math.pi * 2.2 * t))) * sobe_e_some(n, 0.5, 1.1) * 0.22, 0.0)
    poe(x, graos(rng, n, 30, 0.1, 1.0, 600, 2500, 0.008, 0.7) * 0.18, 0.0)
    for k in range(2):
        poe(x, _brilho(rng, 0.6, 4200 + 400 * k, 0.07, SINO), 0.3 + 0.4 * k)
        poe(x, _whoosh(rng, 0.2, 5000, 8000, 0.4, 1.2, 0.08), 0.28 + 0.4 * k)
    return reverb(x, 0.5, 0.25)


def jardim_noturno(rng, v):
    """O Jardim noturno: os dois estiletes voando (os "shhing" metálicos), o X cortando (dois cortes finos e
    secos), a rosa abrindo (o tom que se abre, suave e escuro) e as pétalas se espalhando."""
    x = _z(1.8)
    for k in range(2):
        poe(x, _whoosh(rng, 0.2, 1500, 5000, 0.8, 1.3, 0.35), 0.0 + 0.04 * k)
        poe(x, modal(n_de(0.5), 2600 + 500 * k, rng=rng, **METAL) * env(n_de(0.5), 0.001, 0.2) * 0.18, 0.18 + 0.04 * k)
        poe(x, estalo(rng, n_de(0.04), 2500, 9000, 0.01) * 0.6, 0.2 + 0.05 * k)
    m = n_de(0.9)
    t = _t(m)
    abre = (seno(varre(180, 260, m, 1.0), m) + seno(varre(270, 390, m, 1.0), m) * 0.6) * sobe_e_some(m, 0.4, 1.3) * 0.12
    poe(x, abre * (0.7 + 0.3 * np.sin(2 * math.pi * 5 * t)), 0.32)
    poe(x, _whoosh(rng, 0.6, 400, 1600, 0.4, 1.3, 0.25), 0.35)
    poe(x, graos(rng, n_de(0.8), 50, 0.0, 0.7, 3000, 10000, 0.003, 0.8) * 0.25, 0.7)
    poe(x, _brilho(rng, 0.8, 1900, 0.06, CRISTAL), 0.5)
    return reverb(x, 0.55, 0.28)


# =================================================================== Jinwoo
def comando_avancem(rng, v):
    """O comando do Monarca: o grave escuro da sombra se abrindo, os olhos acendendo em fileira (os
    "vmm" graves curtos, um atrás do outro), e o exército avançando (o tropel crescendo e o "whoosh") até
    o impacto pesado."""
    x = _z(1.9)
    n = n_de(1.1)
    t = _t(n)
    poe(x, (seno(55, n) + seno(82.5, n) * 0.5) * sobe_e_some(n, 0.4, 1.2) * 0.18 + passa(rosa(rng, n), 60, 500, 2) * sobe_e_some(n, 0.5, 1.2) * 0.12, 0.0)
    for k in range(9):
        m = n_de(0.14)
        f = 180 + 25 * (k % 3)
        poe(x, satura(seno(varre(f, f * 0.7, m, 1.0), m), 2) * env(m, 0.005, 0.1) * 0.08, 0.05 + 0.04 * k)
    trop = n_de(0.35)
    passos = np.zeros(trop)
    for k in range(18):
        p = n_de(0.05)
        poe(passos, passa(baque(p, 120, 70, 0.025, 0.2), None, 2000, 2) * (0.3 + 0.7 * k / 18) * rng.uniform(0.6, 1), 0.015 * k + rng.uniform(0, 0.01))
    poe(x, passos * 0.35, 0.4)
    poe(x, _whoosh(rng, 0.35, 300, 1600, 0.85, 1.4, 0.55), 0.4)
    poe(x, baque(n_de(0.5), 75, 38, 0.18, 0.5) * 0.85, 0.66)
    poe(x, passa(rosa(rng, n_de(0.4)), 100, 1500, 2) * env(n_de(0.4), 0.002, 0.25) * 0.3, 0.66)
    m = n_de(0.35)
    poe(x, seno(varre(500, 800, m, 1.0), m) * sobe_e_some(m, 0.5, 1.3) * 0.03, 1.1)
    return reverb(x, 0.6, 0.3)


# =================================================================== Kaneki
def fome_de_ghoul(rng, v):
    """A fome do ghoul: o olho abrindo (o "tchk" úmido), a respiração puxada de dentes cerrados (o ar
    sugado que desce), dois batimentos fortes, e a carne se fechando (o molhado baixo)."""
    x = _z(1.8)
    poe(x, _molhado(rng, 0.15, 0.35, 400, 3000), 0.0)
    poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.004) * 0.4, 0.04)
    n = n_de(0.7)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * sobe_e_some(n, 0.7, 1.2) * 0.25, 0.2)
    poe(x, _batida_de_coracao(rng, 0.75), 0.45)
    poe(x, _batida_de_coracao(rng, 0.85), 0.72)
    poe(x, _molhado(rng, 0.6, 0.2), 0.95)
    return reverb(x, 0.45, 0.22)


def kakuja_preparo(rng, v):
    """O Preparo do Centípede: os tentáculos saindo das costas (o rasgo carnudo), balançando molhados, e o
    rosnado baixo do Kaneki."""
    x = _z(1.3)
    poe(x, _molhado(rng, 1.1, 0.3), 0.0)
    poe(x, _rasgo(rng, 0.2, 300, 2500, 0.3), 0.02)
    n = n_de(0.9)
    t = _t(n)
    f = 85 + 6 * np.sin(2 * math.pi * 3 * t)
    rosnado = satura(np.sin(2 * math.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.abs(np.sin(2 * math.pi * 23 * t))), 3)
    poe(x, passa(rosnado, 80, 1600, 2) * sobe_e_some(n, 0.5, 1.2) * 0.12, 0.25)
    return reverb(x, 0.45, 0.22)


def centopeia(rng, v):
    """O kagune centopeia: os gomos estalando um atrás do outro cada vez mais rápido (o "tric-tric-tric"
    seco), o corpo chicoteando no ar, a ponta cravando (o baque e o rasgo molhado), e o sangue sendo
    sugado de volta pelo corpo."""
    x = _z(1.9)
    em = 0.0
    for k in range(16):
        poe(x, _clique(rng, 0.18 + 0.01 * k, 1400 + 60 * k), em)
        em += 0.03 * (1 - 0.5 * k / 16)
    poe(x, _whoosh(rng, 0.3, 300, 1800, 0.8, 1.4, 0.6), 0.05)
    poe(x, baque(n_de(0.45), 95, 42, 0.14, 0.8) * 0.9, 0.3)
    poe(x, _rasgo(rng, 0.25, 300, 3000, 0.4), 0.3)
    poe(x, _molhado(rng, 0.3, 0.3, 200, 2500), 0.32)
    n = n_de(0.55)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 11 * _t(n))) * sobe_e_some(n, 0.6, 1.3) * 0.22, 0.6)
    poe(x, seno(varre(600, 220, n, 1.0), n) * sobe_e_some(n, 0.6, 1.3) * 0.04, 0.6)
    return reverb(x, 0.5, 0.22)


# =================================================================== Yugi
def preparar_o_duelo(rng, v):
    """É hora do duelo: o Enigma do Milênio acendendo (o sino dourado com o brilho que sobe), as cartas se
    abrindo em leque (os estalinhos de papelão em sequência), a carta lançada (o "fwip" girando) e a Carga
    subindo (os brilhos em escada)."""
    x = _z(1.8)
    poe(x, _brilho(rng, 1.2, 520, 0.22, SINO), 0.0)
    n = n_de(0.5)
    poe(x, seno(varre(700, 1050, n, 1.0), n) * sobe_e_some(n, 0.6, 1.3) * 0.05, 0.05)
    for k in range(5):
        poe(x, _carta(rng, 0.3), 0.18 + 0.05 * k)
    m = n_de(0.25)
    giro = passa(rosa(rng, m), 1500, 7000, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 28 * _t(m)))) * sobe_e_some(m, 0.4, 1.2) * 0.35
    poe(x, giro, 0.5)
    poe(x, _carta(rng, 0.4), 0.72)
    poe(x, baque(n_de(0.15), 200, 120, 0.03, 0.6) * 0.25, 0.72)
    for k, f in enumerate((1047, 1319, 1568, 2093)):
        poe(x, _brilho(rng, 0.4, f, 0.08, CRISTAL), 0.8 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "identidade-falsa": (identidade_falsa, "Loid: a máscara rasgando e a mira travando"),
    "neutralizacao-silenciosa": (neutralizacao_silenciosa, "Loid: o tiro abafado e o Preparo quebrando"),
    "plano-de-fuga": (plano_de_fuga, "Loid: a bomba de fumaça e a fuga"),
    "investida-elegante": (investida_elegante, "Yor: o chute girando e as pétalas"),
    "espinho-preparo": (espinho_preparo, "Yor: os ramos e os estiletes (antes do golpe)"),
    "jardim-noturno": (jardim_noturno, "Yor: os estiletes em X e a rosa abrindo"),
    "comando-avancem": (comando_avancem, "Jinwoo: os olhos acendendo e o exército avançando"),
    "fome-de-ghoul": (fome_de_ghoul, "Kaneki: o kakugan, o ar puxado e o coração"),
    "kakuja-preparo": (kakuja_preparo, "Kaneki: os tentáculos saindo e o rosnado (antes do golpe)"),
    "centopeia": (centopeia, "Kaneki: os gomos estalando, a cravada e o sangue sugado"),
    "preparar-o-duelo": (preparar_o_duelo, "Yugi: o Enigma, o leque de cartas e a Carga"),
}
