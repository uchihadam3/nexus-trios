"""Os sons da rodada 14: Cavaleiro da Lua, Tempestade, Jean Grey, Vampira e Gambit (veja
tools/vfx/familias_v2/rodada14.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada11 import _carta
from sfx_rodada12 import _fio_magico, _zumbido
from sfx_rodada13 import _fogo, _zap
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _pano(rng, seg, g=0.3):
    """O pano da capa abrindo no vento: o farfalhar grave que estala."""
    n = n_de(seg)
    t = _t(n)
    x = passa(rosa(rng, n), 300, 2500, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 7 * t)))
    return x * sobe_e_some(n, 0.25, 1.3) * g


def _vento(rng, seg, lo=300, hi=2200, g=0.3, uivo=0.0):
    """O vento forte: o ruído que sobe e desce e, se pedido, o uivo (o tom que oscila)."""
    n = n_de(seg)
    t = _t(n)
    x = passa(rosa(rng, n), lo, hi, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 1.7 * t + rng.uniform(0, 6)))
    if uivo:
        x += seno(500 * (1 + 0.15 * np.sin(2 * math.pi * 0.9 * t)), n) * uivo
    return x * sobe_e_some(n, 0.4, 1.2) * g


def _trovao(rng, seg=1.2, g=0.8):
    """O trovão: o estalo seco do raio e o ronco que rola depois."""
    n = n_de(seg)
    x = satura(passa(rosa(rng, n), 800, 9000, 2) * env(n, 0.0005, 0.06), 2.5) * 0.8
    x += passa(rosa(rng, n), 30, 300, 2) * env(n, 0.03, seg * 0.6) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * _t(n))) * 1.4
    return x * g


def _psi(n, f0, f1, g=0.08):
    """O zumbido psíquico: dois tons perto um do outro que batem (o "uóóó" da mente)."""
    return (seno(varre(f0, f1, n, 1.0), n) + seno(varre(f0 * 1.012, f1 * 1.012, n, 1.0), n) + 0.4 * seno(varre(f0 * 2, f1 * 2, n, 1.0), n)) * g


def _estouro_rosa(rng, g=0.6):
    """O estouro cinético do Gambit: o estalo brilhante e o "pum" curto."""
    n = n_de(0.4)
    return (satura(baque(n, 150, 60, 0.07, 1.0), 1.8) * 0.7 + passa(rosa(rng, n), 600, 7000, 2) * env(n, 0.001, 0.08) * 0.9 + estalo(rng, n, 2000, 8000, 0.01) * 0.4) * g


# =================================================================== Cavaleiro da Lua
def manto_lunar(rng, v):
    """O manto lunar: a capa abre no vento, as faixas assobiam até o rival e o tom tonto (que oscila e cai) com o
    "tilim" do olho de Khonshu."""
    x = _z(1.6)
    poe(x, _pano(rng, 0.45, 0.45), 0.0)
    poe(x, _brilho(rng, 0.8, 659, 0.05, SINO), 0.02)
    for k in range(3):
        poe(x, _whoosh(rng, 0.25, 600, 2500, 0.8, 1.3, 0.25), 0.18 + 0.05 * k)
    n = n_de(0.8)
    poe(x, seno(varre(700, 350, n, 1.0) * (1 + 0.06 * np.sin(2 * math.pi * 7 * _t(n))), n) * sobe_e_some(n, 0.2, 1.4) * 0.06, 0.45)
    poe(x, _brilho(rng, 0.6, 1760, 0.08, CRISTAL), 0.55)
    return reverb(x, 0.6, 0.3)


def crescente_de_prata(rng, v):
    """Os dardos de prata: três zunidos girando que chegam um atrás do outro e os três estalos de prata."""
    x = _z(1.4)
    for k in range(3):
        n = n_de(0.28)
        zun = passa(rosa(rng, n), 2500, 8000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 30 * _t(n))) * sobe_e_some(n, 0.8, 1.2) * 0.22
        poe(x, zun, 0.05 + 0.07 * k)
        poe(x, modal(n_de(0.4), 2200 + 250 * k, rng=rng, **METAL) * env(n_de(0.4), 0.0005, 0.15) * 0.25 + estalo(rng, n_de(0.4), 2500, 9000, 0.006) * 0.5, 0.3 + 0.07 * k)
    poe(x, _brilho(rng, 0.6, 1319, 0.06, CRISTAL), 0.6)
    return reverb(x, 0.5, 0.25)


def khonshu_preparo(rng, v):
    """O Preparo do Julgamento: o coro grave e frio da lua (as quintas abertas) e os sinos girando devagar."""
    x = _z(1.4)
    n = n_de(1.4)
    poe(x, (seno(110, n) + seno(165, n) * 0.7 + seno(220, n) * 0.4) * (0.7 + 0.3 * np.sin(2 * math.pi * 1.5 * _t(n))) * sobe_e_some(n, 0.3, 1.0) * 0.05, 0.0)
    for k in range(4):
        poe(x, _brilho(rng, 0.5, 880 * (1.5 if k % 2 else 1.0), 0.04, SINO), 0.1 + 0.3 * k)
    return reverb(x, 0.7, 0.35)


def julgamento_de_khonshu(rng, v):
    """O Julgamento de Khonshu: a lua subindo (o tom que cresce e o coro), o grito do pássaro de Khonshu e as três
    colunas de luar caindo em estrondos."""
    x = _z(2.0)
    n = n_de(0.6)
    poe(x, (seno(varre(110, 220, n, 1.0), n) + seno(varre(165, 330, n, 1.0), n) * 0.6) * sobe_e_some(n, 0.8, 1.2) * 0.07, 0.0)
    m = n_de(0.35)
    poe(x, satura(seno(varre(1400, 900, m, 1.0) * (1 + 0.03 * np.sin(2 * math.pi * 25 * _t(m))), m), 2) * env(m, 0.02, 0.2) * 0.07, 0.2)
    for k in range(3):
        t0 = 0.4 + 0.06 * k
        poe(x, baque(n_de(0.6), 70, 30, 0.2, 1.0) * 0.7, t0)
        poe(x, _brilho(rng, 0.7, 1047 * (1 + 0.25 * k), 0.06, CRISTAL), t0)
        poe(x, passa(rosa(rng, n_de(0.5)), 1500, 8000, 2) * env(n_de(0.5), 0.002, 0.2) * 0.25, t0)
    return reverb(x, 0.8, 0.4)


# =================================================================== Tempestade
def rajada_de_vento(rng, v):
    """A rajada de vento: o vento forte que atravessa da esquerda para a direita, com o uivo e as folhas
    batendo."""
    x = _z(1.6)
    poe(x, _vento(rng, 1.2, 250, 2500, 0.6, 0.03), 0.0)
    poe(x, _whoosh(rng, 0.6, 300, 1800, 0.6, 1.2, 0.5), 0.05)
    poe(x, graos(rng, n_de(0.9), 30, 0.1, 0.8, 1500, 5000, 0.005) * 0.3, 0.1)
    return reverb(x, 0.6, 0.3)


def relampago_em_cadeia(rng, v):
    """O relâmpago em cadeia: o raio cai (o estalo e o trovão), e salta em dois estalos elétricos rápidos."""
    x = _z(1.8)
    poe(x, _trovao(rng, 1.2, 0.7), 0.05)
    for k in range(2):
        poe(x, _zap(rng, 0.25, 0.35), 0.18 + 0.1 * k)
        poe(x, satura(passa(rosa(rng, n_de(0.12)), 1500, 9000, 2) * env(n_de(0.12), 0.0005, 0.04), 2.5) * 0.5, 0.2 + 0.1 * k)
    return reverb(x, 0.7, 0.35)


def tempestade_preparo(rng, v):
    """O Preparo do Olho da tempestade: o vento girando em volta (o uivo que pulsa) e os trovões ao longe."""
    x = _z(1.4)
    poe(x, _vento(rng, 1.4, 200, 1500, 0.4, 0.02), 0.0)
    poe(x, passa(rosa(rng, n_de(1.0)), 30, 200, 2) * env(n_de(1.0), 0.1, 0.6) * 0.5, 0.35)
    poe(x, _zap(rng, 0.15, 0.12), 0.8)
    return reverb(x, 0.7, 0.35)


def olho_da_tempestade(rng, v):
    """O olho da tempestade: o furacão girando (o vento que sobe), o silêncio do olho e os raios caindo em fila
    com os trovões."""
    x = _z(2.2)
    poe(x, _vento(rng, 1.8, 200, 2200, 0.5, 0.04), 0.0)
    for k in range(5):
        poe(x, satura(passa(rosa(rng, n_de(0.15)), 1200, 9000, 2) * env(n_de(0.15), 0.0005, 0.05), 2.5) * 0.4, 0.3 + 0.07 * k)
    poe(x, _trovao(rng, 1.4, 0.8), 0.32)
    poe(x, _zap(rng, 0.5, 0.25), 0.35)
    return reverb(x, 0.8, 0.4)


# =================================================================== Jean Grey
def escudo_mental(rng, v):
    """O escudo mental: o zumbido psíquico que sobe e se abre num acorde, e a cúpula fechando (o "vuum" de cristal)."""
    x = _z(1.5)
    n = n_de(0.7)
    poe(x, _psi(n, 300, 600, 0.06) * sobe_e_some(n, 0.6, 1.2), 0.0)
    m = n_de(0.9)
    poe(x, (seno(523, m) + seno(659, m) * 0.7 + seno(784, m) * 0.5) * sobe_e_some(m, 0.2, 1.3) * 0.05, 0.35)
    poe(x, modal(n_de(0.7), 1047, rng=rng, **CRISTAL) * env(n_de(0.7), 0.002, 0.35) * 0.15, 0.45)
    return reverb(x, 0.7, 0.35)


def muralha_telecinetica(rng, v):
    """A muralha telecinética: a parede subindo (o zumbido que cresce) e os destroços parando no ar, cada um num
    baque abafado e um tremor."""
    x = _z(1.5)
    n = n_de(0.5)
    poe(x, _psi(n, 120, 260, 0.08) * sobe_e_some(n, 0.8, 1.2), 0.0)
    poe(x, passa(rosa(rng, n), 100, 1200, 2) * sobe_e_some(n, 0.8, 1.2) * 0.25, 0.0)
    for k in range(5):
        poe(x, passa(baque(n_de(0.2), 120, 70, 0.05, 0.4), None, 900, 2) * 0.35, 0.18 + 0.05 * k)
    m = n_de(0.6)
    poe(x, _zumbido(m, 200, 0.05, 12.0) * env(m, 0.01, 0.3), 0.45)
    return reverb(x, 0.6, 0.3)


def fenix_preparo(rng, v):
    """O Preparo da Fênix: o fogo subindo e rugindo baixo, e o grito distante da ave crescendo."""
    x = _z(1.4)
    poe(x, _fogo(rng, 1.4, 0.35), 0.0)
    n = n_de(1.0)
    poe(x, satura(seno(varre(700, 1100, n, 1.0) * (1 + 0.02 * np.sin(2 * math.pi * 18 * _t(n))), n), 1.8) * sobe_e_some(n, 0.8, 1.2) * 0.04, 0.3)
    return reverb(x, 0.6, 0.3)


def fenix_desperta(rng, v):
    """A Fênix desperta: o grito agudo da ave, o mergulho (o vento que desce) e a explosão de fogo enorme, com os
    choques no fim."""
    x = _z(2.2)
    n = n_de(0.5)
    poe(x, satura(seno(varre(1500, 1100, n, 1.0) * (1 + 0.025 * np.sin(2 * math.pi * 22 * _t(n))), n), 2.2) * env(n, 0.02, 0.3) * 0.08, 0.0)
    poe(x, _whoosh(rng, 0.4, 2000, 400, 0.85, 1.3, 0.6), 0.25)
    poe(x, satura(baque(n_de(1.0), 55, 25, 0.35, 1.0), 1.8) * 0.9, 0.42)
    poe(x, _fogo(rng, 1.2, 0.8, 100, 5000), 0.42)
    poe(x, _zap(rng, 0.4, 0.2), 0.62)
    return reverb(x, 0.8, 0.4)


# =================================================================== Vampira
def forca_roubada(rng, v):
    """A força roubada: o voo rasante (o vento), o soco carregado (o grave pesado com o zumbido verde) e os cacos do
    Preparo quebrando."""
    x = _z(1.5)
    poe(x, _whoosh(rng, 0.3, 300, 2000, 0.85, 1.3, 0.6), 0.0)
    n = n_de(0.3)
    poe(x, _psi(n, 180, 260, 0.05) * sobe_e_some(n, 0.9, 1.1), 0.0)
    poe(x, satura(baque(n_de(0.6), 65, 30, 0.2, 1.0), 1.8) * 0.9, 0.27)
    poe(x, passa(rosa(rng, n_de(0.3)), 400, 5000, 2) * env(n_de(0.3), 0.001, 0.08) * 0.6, 0.27)
    poe(x, modal(n_de(0.6), 2400, rng=rng, desafina=0.05, **VIDRO) * env(n_de(0.6), 0.0005, 0.25) * 0.2 + graos(rng, n_de(0.6), 25, 0.0, 0.4, 2500, 8000, 0.005) * 0.5, 0.3)
    return reverb(x, 0.5, 0.25)


def memoria_preparo(rng, v):
    """O Preparo da Memória emprestada: os ecos das vozes dos outros girando (os tons que vêm e vão) e o zumbido
    da mente."""
    x = _z(1.4)
    n = n_de(1.4)
    poe(x, _psi(n, 220, 240, 0.04) * sobe_e_some(n, 0.3, 1.0), 0.0)
    for k in range(4):
        poe(x, _fio_magico(rng, 0.4, 400 + 150 * k, 600 + 200 * k, 0.04), 0.1 + 0.3 * k)
    return reverb(x, 0.8, 0.4)


def memoria_emprestada(rng, v):
    """A memória emprestada: os poderes copiados em fila (o "snikt" das garras, o estalo do raio, o gelo trincando)
    e o golpe final que junta tudo."""
    x = _z(1.8)
    poe(x, modal(n_de(0.3), 3200, rng=rng, **METAL) * env(n_de(0.3), 0.0005, 0.1) * 0.25 + passa(rosa(rng, n_de(0.3)), 3000, 9000, 2) * env(n_de(0.3), 0.001, 0.05) * 0.4, 0.05)
    poe(x, _zap(rng, 0.25, 0.4), 0.22)
    poe(x, modal(n_de(0.4), 1800, rng=rng, desafina=0.06, **VIDRO) * env(n_de(0.4), 0.0005, 0.12) * 0.2 + graos(rng, n_de(0.4), 30, 0.0, 0.3, 2000, 7000, 0.004) * 0.4, 0.38)
    poe(x, satura(baque(n_de(0.7), 60, 28, 0.25, 1.0), 1.8) * 0.9, 0.55)
    poe(x, _brilho(rng, 0.6, 784, 0.06, SINO), 0.6)
    return reverb(x, 0.6, 0.3)


# =================================================================== Gambit
def carta_carregada(rng, v):
    """A carta carregada: o zumbido cinético subindo na carta, o "fwip" da carta voando, o "tak" dela grudando e os
    tiques da bomba."""
    x = _z(1.6)
    n = n_de(0.3)
    poe(x, (seno(varre(300, 1400, n, 1.0), n) * 0.06 + passa(rosa(rng, n), 2000, 7000, 2) * 0.05 * (0.5 + 0.5 * np.sin(2 * math.pi * 40 * _t(n)))) * sobe_e_some(n, 0.9, 1.1), 0.0)
    poe(x, _carta(rng, 0.35), 0.2)
    poe(x, _whoosh(rng, 0.18, 1500, 6000, 0.8, 1.2, 0.3), 0.22)
    poe(x, estalo(rng, n_de(0.06), 1500, 5000, 0.006) * 0.5, 0.38)
    for k in range(5):
        poe(x, seno(1800, n_de(0.03)) * env(n_de(0.03), 0.001, 0.015) * 0.1, 0.45 + 0.166 * k)
    return reverb(x, 0.45, 0.22)


def baralho_explosivo(rng, v):
    """O baralho explosivo: o leque de cartas se abrindo (o "frrrr" das cartas) e as cinco explosões em fila."""
    x = _z(1.6)
    n = n_de(0.25)
    poe(x, graos(rng, n, 18, 0.0, 0.22, 2000, 7000, 0.004) * 0.6, 0.0)
    for k in range(5):
        poe(x, _carta(rng, 0.15), 0.05 + 0.03 * k)
        poe(x, _estouro_rosa(rng, 0.45 + 0.05 * k), 0.33 + 0.03 * k + 0.02 * k)
    return reverb(x, 0.55, 0.28)


def gambit_preparo(rng, v):
    """O Preparo do Bastão cinético: as cartas embaralhando em cascata (o "frrrrr") e o zumbido cinético subindo."""
    x = _z(1.4)
    for k in range(3):
        poe(x, graos(rng, n_de(0.35), 28, 0.0, 0.33, 2500, 7000, 0.003) * 0.5, 0.05 + 0.45 * k)
    n = n_de(1.4)
    poe(x, seno(varre(200, 600, n, 1.0) * (1 + 0.01 * np.sin(2 * math.pi * 30 * _t(n))), n) * sobe_e_some(n, 0.8, 1.2) * 0.04, 0.0)
    return reverb(x, 0.5, 0.25)


def bastao_cinetico(rng, v):
    """O bastão cinético: o bastão girando (o "vuvuvu"), a pancada no chão e as cartas detonando em cadeia."""
    x = _z(2.0)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 14 * _t(n))) * sobe_e_some(n, 0.6, 1.2) * 0.45, 0.0)
    poe(x, satura(baque(n_de(0.6), 70, 30, 0.2, 1.0), 1.8) * 0.9 + estalo(rng, n_de(0.6), 600, 4000, 0.02) * 0.5, 0.33)
    for k in range(5):
        poe(x, _estouro_rosa(rng, 0.5), 0.4 + 0.06 * k)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "manto-lunar": (manto_lunar, "Cavaleiro da Lua: a capa, as faixas e o tom tonto"),
    "crescente-de-prata": (crescente_de_prata, "Cavaleiro da Lua: os três dardos de prata"),
    "khonshu-preparo": (khonshu_preparo, "Cavaleiro da Lua: o coro da lua (antes do golpe)"),
    "julgamento-de-khonshu": (julgamento_de_khonshu, "Cavaleiro da Lua: a lua, o grito e as colunas"),
    "rajada-de-vento": (rajada_de_vento, "Tempestade: o vento forte"),
    "relampago-em-cadeia": (relampago_em_cadeia, "Tempestade: o raio que salta"),
    "tempestade-preparo": (tempestade_preparo, "Tempestade: o vento girando (antes do golpe)"),
    "olho-da-tempestade": (olho_da_tempestade, "Tempestade: o furacão e os raios"),
    "escudo-mental": (escudo_mental, "Jean Grey: o zumbido e a cúpula"),
    "muralha-telecinetica": (muralha_telecinetica, "Jean Grey: a parede e os destroços parando"),
    "fenix-preparo": (fenix_preparo, "Jean Grey: o fogo subindo (antes do golpe)"),
    "fenix-desperta": (fenix_desperta, "Jean Grey: o grito da Fênix e a explosão"),
    "forca-roubada": (forca_roubada, "Vampira: o voo e o soco"),
    "memoria-preparo": (memoria_preparo, "Vampira: os ecos das memórias (antes do golpe)"),
    "memoria-emprestada": (memoria_emprestada, "Vampira: os poderes copiados em fila"),
    "carta-carregada": (carta_carregada, "Gambit: a carta carregada e os tiques"),
    "baralho-explosivo": (baralho_explosivo, "Gambit: o leque e as explosões"),
    "gambit-preparo": (gambit_preparo, "Gambit: as cartas embaralhando (antes do golpe)"),
    "bastao-cinetico": (bastao_cinetico, "Gambit: o bastão e as cartas detonando"),
}
