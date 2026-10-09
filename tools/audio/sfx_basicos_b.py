"""Sons dos ataques básicos, lote b (veja tools/vfx/familias_v2/basicos_b.py).

Cada receita segue a folha de animação no tempo (a folha dura ~0,8 s no jogo):
os "puf" dos clones antes dos chutes, o "shing" e o chiado de pássaros do
Chidori, o assobio girando das shurikens e o "tchak" de cada uma, o soco que
racha o chão, o sangue que acende em chamas, o trovão seco e a bainha do
Zenitsu, o rasgo áspero das lâminas lascadas, o "tink" dos pregos e a
ressonância, o "zip" do Hiraishin, a abanada do gunbai, a onda de pressão do
Shinra Tensei, o cabo e o gás do equipamento de manobra e o vapor do titã.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _tom, _whoosh, _z, nota  # noqa: F401
from som import (CENTROS, CRISTAL, METAL, SINO, SR, VIDRO, assobio, baque, env, estalo, graos, modal, n_de, passa, poe,  # noqa: F401
                 faixas, reverb, rosa, ruido, satura, seno, sobe_e_some, varre)


# ------------------------------------------------------------------ peças
def _puf(rng, g=1.0):
    """A baforada de fumaça do clone: um "pff" abafado de ar, com um tom que cai."""
    n = n_de(0.22)
    ar = passa(rosa(rng, n), 250, 2200, 2) * env(n, 0.003, 0.06) * 1.2
    sopro = passa(ruido(rng, n), 1200, 5000, 2) * env(n, 0.002, 0.025) * 0.35
    tom = seno(varre(420, 160, n, 0.7), n) * env(n, 0.002, 0.045) * 0.35
    return (ar + sopro + tom) * g


def _tchak(rng, f0=2600, g=1.0):
    """Metal que crava: estalo seco, um "tchak" de lâmina na madeira e um zunido curto de metal."""
    n = n_de(0.3)
    x = estalo(rng, n, 1500, 9000, 0.004) * 0.9
    x += baque(n, 420, 200, 0.025, 0.5) * 0.45
    x += modal(n, f0 * rng.uniform(0.92, 1.08), rng=rng, **METAL) * env(n, 0.0005, 0.06) * 0.25
    t = np.arange(n) / SR
    x += np.sin(2 * math.pi * 180 * t) * np.exp(-t / 0.06) * (0.5 + 0.5 * np.sin(2 * math.pi * 38 * t)) * 0.18   # treme cravada
    return x * g


def _zip(rng, seg=0.07, f0=400, f1=5200, g=0.5):
    """Varrida de tom muito rápida (teletransporte / sumir num instante)."""
    n = n_de(seg)
    tom = seno(varre(f0, f1, n, 0.6), n) * env(n, 0.002, seg * 0.6)
    ar = passa(ruido(rng, n), 2500, 10000, 2) * sobe_e_some(n, 0.7, 1.2) * 0.6
    return (tom + ar) * g


def _crepita(rng, seg, quantos, lo=2500, hi=10000, g=0.5):
    """Crepitar elétrico: estalos curtíssimos espalhados."""
    return graos(rng, n_de(seg), quantos, 0.0, seg * 0.9, lo, hi, 0.0018) * g


def _passaros(rng, seg, g=0.25):
    """O chiado do Chidori: trinados agudos repetidos (chilreio de mil pássaros)."""
    n = n_de(seg)
    x = np.zeros(n)
    em = 0.0
    while em < seg - 0.03:
        d = n_de(rng.uniform(0.018, 0.03))
        f = varre(rng.uniform(2600, 3300), rng.uniform(4200, 5200), d, 0.8)
        poe(x, seno(f, d) * env(d, 0.002, 0.012) * rng.uniform(0.6, 1.0), em)
        em += max(0.012, rng.uniform(0.016, 0.03))
    return x * sobe_e_some(n, 0.15, 1.0) * g


def _zumbido(n, f=110, sat=5.0, g=0.2):
    return satura(seno(varre(f, f * 0.95, n), n), sat) * env(n, 0.002, n / SR * 0.4) * g


def _rasgo_aspero(rng, seg=0.2, f_dente=95, g=1.0):
    """Rasgo de lâmina dentada: ruído picotado pelos dentes (um "rrrrasp")."""
    n = n_de(seg)
    t = np.arange(n) / SR
    dente = (0.5 + 0.5 * np.sign(np.sin(2 * math.pi * varre(f_dente * 1.4, f_dente, n) * t))) * 0.8 + 0.2
    x = passa(ruido(rng, n), 700, 5500, 2) * dente * sobe_e_some(n, 0.25, 1.3) * 1.2
    x = satura(x, 2.0)
    return x * g


# ------------------------------------------------------------------ Naruto
def combo_dos_clones(rng, v):
    x = _z(1.1)
    for k, em in enumerate((0.0, 0.05, 0.1)):
        poe(x, _puf(rng, 0.9), em)
        poe(x, _whoosh(rng, 0.09, 600, 3000, 0.85, g=0.35), em + 0.06)
        poe(x, B.soco_leve(rng, v), em + 0.14, 0.75 + 0.1 * k)
    poe(x, _puf(rng, 1.0), 0.29)
    poe(x, _whoosh(rng, 0.14, 300, 4000, 0.9, g=0.55), 0.33)
    poe(x, B.soco_pesado(rng, v), 0.42, 1.1)
    poe(x, assobio(rng, n_de(0.35), 900, 3500, 0.8, 0.4) * env(n_de(0.35), 0.005, 0.12) * 0.35, 0.43)   # sobe voando
    return reverb(x, 0.3, 0.12)


# ------------------------------------------------------------------ Sasuke
def kusanagi(rng, v):
    x = _z(0.95)
    poe(x, _whoosh(rng, 0.07, 2500, 9000, 0.8, g=0.6), 0.0)
    n = n_de(0.5)
    shing = B._lamina_curta(rng, n, rng.uniform(3000, 3600)) * 0.35
    shing += modal(n, rng.uniform(4200, 4800), rng=rng, **CRISTAL) * env(n, 0.001, 0.12) * 0.12
    poe(x, shing + estalo(rng, n, 3000, 11000, 0.005) * 0.8, 0.04)
    poe(x, _passaros(rng, 0.5, 0.22), 0.03)
    poe(x, _crepita(rng, 0.55, 45, g=0.55), 0.04)
    poe(x, _zumbido(n_de(0.5), 115, 5, 0.18), 0.04)
    poe(x, B.raio(rng, v)[: n_de(0.35)] * 0.35, 0.05)
    return reverb(x, 0.3, 0.14, 7000)


# ------------------------------------------------------------------ Itachi
def shuriken(rng, v):
    x = _z(0.9)
    for k, em in enumerate((0.0, 0.055, 0.11)):
        voo = 0.19
        n = n_de(voo)
        t = np.arange(n) / SR
        giro = 0.45 + 0.55 * np.abs(np.sin(2 * math.pi * varre(16, 26, n) * t)) ** 2
        assob = assobio(rng, n, 1600, 3400, 1.0, 0.25) * giro * sobe_e_some(n, 0.9, 1.6) * 0.55
        assob += seno(varre(2200, 2900, n), n) * giro * sobe_e_some(n, 0.9, 1.8) * 0.06
        poe(x, assob, em)
        poe(x, _tchak(rng, 2400 + 300 * k), em + voo, 0.95)
    return reverb(x, 0.25, 0.12)


# ------------------------------------------------------------------ Sakura
def soco_de_chakra(rng, v):
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.12, 300, 2600, 0.9, g=0.5), 0.0)
    poe(x, B.soco_pesado(rng, v), 0.1, 0.9)
    poe(x, baque(n_de(0.9), 70, 30, 0.35, 0.5) * 1.1, 0.1)
    poe(x, B.esmagar(rng, v), 0.11, 0.8)
    # o chão rachando: estalos secos em sequência e pedras rolando
    n = n_de(0.9)
    rach = np.zeros(n)
    em = 0.0
    while em < 0.45:
        m = n_de(0.05)
        poe(rach, satura(passa(ruido(rng, m), 600, 3500, 2) * env(m, 0.0005, 0.01), 2.5) * rng.uniform(0.5, 1.0), em)
        em += max(0.01, rng.exponential(0.035))
    rach += graos(rng, n, 30, 0.1, 0.8, 300, 2500, 0.01) * 0.45
    poe(x, rach * 0.7, 0.14)
    poe(x, _brilho(rng, 0.4, 900, 0.08, SINO), 0.1)                      # o chakra estourando
    return reverb(x, 0.55, 0.22, 4000)


# ------------------------------------------------------------------ Nezuko
def chute_demoniaco(rng, v):
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.16, 400, 3500, 0.85, g=0.6), 0.0)
    poe(x, B.soco_pesado(rng, v), 0.13, 0.9)
    # o sangue acendendo: "fwoomp" de chama que pega, uma gota atrás da outra
    for k in range(4):
        n = n_de(0.25)
        acende = passa(rosa(rng, n), 200, 2000, 2) * env(n, 0.012, 0.08) * 0.6
        acende += seno(varre(160, 320, n, 0.6), n) * env(n, 0.01, 0.06) * 0.15
        poe(x, acende, 0.26 + 0.035 * k + rng.uniform(-0.01, 0.01), 0.9 - 0.12 * k)
    poe(x, B.fogo(rng, v)[: n_de(0.8)] * 0.7, 0.27)
    poe(x, graos(rng, n_de(0.7), 30, 0.0, 0.6, 2000, 8000, 0.003) * 0.3, 0.3)
    return reverb(x, 0.4, 0.18)


# ------------------------------------------------------------------ Zenitsu
def saque_do_trovao(rng, v):
    x = _z(1.15)
    # o polegar solta a guarda: clique curto
    poe(x, estalo(rng, n_de(0.06), 2500, 8000, 0.002) * 0.4 + _brilho(rng, 0.06, 3800, 0.06, METAL), 0.0)
    # trovão seco: estalo enorme, rasgo elétrico e o estrondo
    n = n_de(0.7)
    crack = passa(ruido(rng, n), 1200, 12000, 2) * env(n, 0.0002, 0.012) * 1.6
    crack += satura(passa(ruido(rng, n), 300, 3000, 2) * env(n, 0.0005, 0.03), 3) * 0.8
    poe(x, crack, 0.04)
    poe(x, B.raio(rng, v) * 0.7, 0.04)
    poe(x, baque(n_de(0.8), 65, 28, 0.3, 0.6) * 0.8, 0.04)
    poe(x, _crepita(rng, 0.4, 30, g=0.4), 0.1)
    # a lâmina volta à bainha: deslize de metal e o "tac" final
    n = n_de(0.16)
    desliza = passa(ruido(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.7, 1.5) * 0.3
    desliza += modal(n, 3100, rng=rng, **METAL) * sobe_e_some(n, 0.8, 2.0) * 0.05
    poe(x, desliza, 0.66)
    poe(x, estalo(rng, n_de(0.06), 1500, 6000, 0.004) * 0.7 + baque(n_de(0.06), 700, 400, 0.01, 0.4) * 0.3, 0.82)
    return reverb(x, 0.45, 0.2)


# ------------------------------------------------------------------ Inosuke
def laminas_serrilhadas(rng, v):
    x = _z(0.85)
    for k, em in enumerate((0.0, 0.11)):
        poe(x, _whoosh(rng, 0.08, 800, 5000, 0.8, g=0.45), em)
        poe(x, _rasgo_aspero(rng, 0.2, 90 + 25 * k), em + 0.05, 0.9)
        poe(x, B._carne(rng, n_de(0.12), 0.03, 2.5) * 0.6, em + 0.06)
        poe(x, B._lamina_curta(rng, n_de(0.2), rng.uniform(1700, 2100)) * 0.15, em + 0.06)
    poe(x, graos(rng, n_de(0.4), 18, 0.0, 0.3, 1500, 6000, 0.004) * 0.3, 0.12)   # lascas
    return reverb(x, 0.25, 0.12)


# ------------------------------------------------------------------ Nobara
def martelo_e_prego(rng, v):
    x = _z(1.3)
    # três pregos: voam e cravam "tink"
    for k, em in enumerate((0.0, 0.03, 0.06)):
        poe(x, _whoosh(rng, 0.1, 2000, 6000, 0.8, g=0.2), em)
        m = n_de(0.35)
        tink = modal(m, rng.uniform(3200, 3900), rng=rng, **METAL) * env(m, 0.0005, 0.1) * 0.35
        tink += estalo(rng, m, 3000, 10000, 0.003) * 0.6 + baque(m, 600, 300, 0.012, 0.3) * 0.25
        poe(x, tink, em + 0.13)
    # a martelada: metal pesado batendo
    m = n_de(0.5)
    tonk = B._placa_de_metal(rng, m, 260, 3500, 40, 0.12) * 0.7 + baque(m, 160, 80, 0.08, 0.6) * 0.8
    tonk += estalo(rng, m, 1200, 6000, 0.006) * 0.7
    poe(x, _whoosh(rng, 0.12, 300, 2000, 0.9, g=0.4), 0.24)
    poe(x, tonk, 0.35)
    # ressonância: um estouro grave e vibrante em cada prego
    for k, em in enumerate((0.42, 0.49, 0.56)):
        m = n_de(0.55)
        t = np.arange(m) / SR
        ress = satura(np.sin(2 * math.pi * (95 - 10 * k) * t) * (1 + 0.6 * np.sin(2 * math.pi * 32 * t)), 3) * np.exp(-t / 0.18) * 0.45
        ress += passa(ruido(rng, m), 300, 3000, 2) * env(m, 0.001, 0.03) * 0.8
        ress += modal(m, 700 + 90 * k, rng=rng, **METAL) * env(m, 0.001, 0.2) * 0.12
        poe(x, ress, em, 0.9)
    return reverb(x, 0.5, 0.22, 4500)


# ------------------------------------------------------------------ Minato
def kunai_de_hiraishin(rng, v):
    x = _z(0.95)
    poe(x, _whoosh(rng, 0.14, 1500, 6000, 0.85, g=0.45), 0.0)
    poe(x, _tchak(rng, 2800), 0.14, 0.9)
    # o teletransporte: "zip" instantâneo com um brilho
    poe(x, _zip(rng, 0.06, 300, 6000, 0.6), 0.22)
    poe(x, _brilho(rng, 0.3, 2400, 0.1, CRISTAL), 0.25)
    # o golpe no mesmo instante
    poe(x, B.corte(rng, v), 0.24, 0.9)
    poe(x, B.soco_leve(rng, v), 0.31, 0.7)
    return reverb(x, 0.3, 0.14)


# ------------------------------------------------------------------ Madara
def leque_gunbai(rng, v):
    x = _z(1.4)
    n = n_de(0.32)
    poe(x, assobio(rng, n, 140, 900, 1.0, 0.6) * sobe_e_some(n, 0.75, 1.6) * 1.1, 0.0)    # a abanada pesada
    # o "fwump" do leque batendo no ar no fim da varrida
    m = n_de(0.3)
    fwump = B._baque_seco(rng, m, 75, 0.12) * 0.9 + satura(passa(rosa(rng, m), 90, 700, 2) * env(m, 0.004, 0.06) * 2.0, 1.8) * 0.9
    fwump += passa(ruido(rng, m), 600, 2500, 2) * env(m, 0.002, 0.03) * 0.5
    poe(x, fwump, 0.2)
    # a rajada: vento forte que passa e vai embora
    n = n_de(1.05)
    t = np.arange(n) / SR
    curva = 450 * 2 ** (1.5 * np.sin(math.pi * np.clip(t / 0.9, 0, 1)) ** 0.8)
    raj = faixas(rosa(rng, n), CENTROS, curva, 0.5) * sobe_e_some(n, 0.18, 1.0) * 1.2
    raj += faixas(rosa(rng, n), CENTROS, curva * 3, 0.25) * sobe_e_some(n, 0.25, 1.2) * 0.35
    raj += passa(rosa(rng, n), 50, 250, 2) * sobe_e_some(n, 0.15, 1.0) * 0.5 * (1 + 0.3 * np.sin(2 * math.pi * 6 * t))
    poe(x, raj * 0.85, 0.22)
    return reverb(x, 0.5, 0.2)


# ------------------------------------------------------------------ Pain
def rinnegan(rng, v):
    x = _z(1.4)
    # o ar sendo puxado antes da repulsão
    n = n_de(0.16)
    poe(x, assobio(rng, n, 3000, 600, 1.0, 0.4) * sobe_e_some(n, 0.9, 2.0) * 0.4, 0.0)
    # a onda de pressão: grave enorme, abafado, que empurra
    n = n_de(1.2)
    t = np.arange(n) / SR
    f = 34 + 70 * np.exp(-t / 0.08)
    fase = 2 * math.pi * np.cumsum(f) / SR
    grave = satura(np.sin(fase) * 1.4, 2.5) * np.exp(-t / 0.4) * 0.9
    pressao = passa(rosa(rng, n), 40, 700, 2) * env(n, 0.01, 0.35) * 1.0
    poe(x, grave + pressao, 0.14)
    poe(x, baque(n_de(0.6), 90, 32, 0.25, 0.7) * 0.8, 0.14)
    poe(x, assobio(rng, n_de(0.9), 2500, 200, 0.6, 0.6) * env(n_de(0.9), 0.005, 0.3) * 0.6, 0.15)   # ar empurrado
    # ecos das ondas seguintes
    for k in (1, 2):
        poe(x, baque(n_de(0.4), 70, 35, 0.15, 0.2) * (0.45 / k), 0.14 + 0.1 * k)
    poe(x, graos(rng, n_de(0.8), 30, 0.05, 0.6, 600, 3500, 0.008) * 0.3, 0.2)       # detritos
    return reverb(x, 0.7, 0.3, 3500)


# ------------------------------------------------------------------ Mikasa
def laminas_odm(rng, v):
    x = _z(1.1)
    # dois cabos disparando: estalo do gatilho, "fwip" do cabo e o arame vibrando
    for k, em in enumerate((0.0, 0.025)):
        m = n_de(0.3)
        tiro = estalo(rng, m, 1500, 7000, 0.003) * 0.7 + baque(m, 500, 250, 0.01, 0.4) * 0.3
        poe(tiro, _zip(rng, 0.09, 4500, 1200, 0.25), 0.0)
        poe(x, tiro, em)
        poe(x, modal(m, 900 + 150 * k, rng=rng, **METAL) * env(m, 0.001, 0.08) * 0.1, em + 0.11)   # arame crava
        poe(x, estalo(rng, n_de(0.05), 2000, 8000, 0.004) * 0.5, em + 0.11)
    # gás: "pssshh"
    n = n_de(0.32)
    poe(x, passa(ruido(rng, n), 2500, 11000, 2) * sobe_e_some(n, 0.1, 1.3) * 0.6, 0.07)
    # dois cortes em X
    poe(x, B.corte(rng, v), 0.17, 0.9)
    poe(x, B.corte(rng, v), 0.22, 1.0)
    # carretel recolhendo o cabo
    n = n_de(0.22)
    poe(x, graos(rng, n, 22, 0.0, 0.2, 2500, 7000, 0.0015) * 0.35 + assobio(rng, n, 1500, 3000, 1.0, 0.25) * sobe_e_some(n, 0.3, 1.0) * 0.25, 0.44)
    return reverb(x, 0.3, 0.14)


# ------------------------------------------------------------------ Eren
def soco_titanico(rng, v):
    x = _z(1.5)
    n = n_de(0.22)
    poe(x, assobio(rng, n, 120, 1200, 1.2, 0.6) * sobe_e_some(n, 0.9, 1.8) * 1.0, 0.0)     # o punho enorme vindo
    poe(x, B.esmagar(rng, v), 0.15, 1.1)
    poe(x, baque(n_de(1.0), 55, 22, 0.45, 0.6) * 1.3, 0.15)
    poe(x, B.explosao(rng, v)[: n_de(0.8)] * 0.45, 0.16)
    # vapor quente: chiado longo que sobe e some
    n = n_de(1.0)
    t = np.arange(n) / SR
    chiado = passa(ruido(rng, n), 3500, 12000, 2) * sobe_e_some(n, 0.3, 1.2) * (1 + 0.25 * np.sin(2 * math.pi * 11 * t)) * 0.45
    chiado += passa(rosa(rng, n), 900, 3500, 2) * sobe_e_some(n, 0.35, 1.2) * 0.25
    poe(x, chiado, 0.3)
    return reverb(x, 0.65, 0.25, 4000)


# nome do arquivo (com hífen) → (função, descrição)
SONS: dict = {
    "kusanagi": (kusanagi, "básico de Sasuke: \"shing\" da katana e o crepitar do Chidori"),
    "shuriken": (shuriken, "básico de Itachi: assobio girando de três shurikens e o \"tchak\" de cada uma"),
    "soco-de-chakra": (soco_de_chakra, "básico de Sakura: soco gigantesco e o chão rachando"),
    "chute-demoniaco": (chute_demoniaco, "básico de Nezuko: chute e o sangue acendendo em chamas"),
    "saque-do-trovao": (saque_do_trovao, "básico de Zenitsu: estalo de trovão seco e a lâmina voltando à bainha"),
    "laminas-serrilhadas": (laminas_serrilhadas, "básico de Inosuke: dois rasgos ásperos de lâmina dentada"),
    "martelo-e-prego": (martelo_e_prego, "básico de Nobara: \"tink\" dos pregos, martelada e ressonância"),
    "kunai-de-hiraishin": (kunai_de_hiraishin, "básico de Minato: kunai cravando, \"zip\" do teleporte e o golpe"),
    "leque-gunbai": (leque_gunbai, "básico de Madara: abanada pesada do gunbai e a rajada de vento"),
    "rinnegan": (rinnegan, "básico de Pain: onda de pressão grave do Shinra Tensei"),
    "laminas-odm": (laminas_odm, "básico de Mikasa: cabos disparando, gás e dois cortes"),
    "soco-titanico": (soco_titanico, "básico de Eren: soco de titã grave e pesado e o chiado do vapor"),
}
