"""Sons dos ataques básicos, lote m (veja tools/vfx/familias_v2/basicos_m.py).

A maletada e os papéis, o corte com o sussurro das pétalas, o leque de aço que zune e volta, a marreta e o
chão rachando, a barrigada e o ronco, o tapão molhado do Patrick, a metralhadora de socos do Flecha, o raio
de mana, o chute com o choque da Viúva, a flecha que assobia e estoura, a Godslayer, as duas facas, o soco
elétrico, o chicote e as unhas, e o chiado do gás com os gritos abafados.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_k import _acerto, _mola, _splash
from sfx_basicos_l import _estrelinhas
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _zap(rng, seg, g=0.3):
    n = n_de(seg)
    pisca = (np.sin(2 * math.pi * 47 * _t(n)) > 0.2).astype(float) * 0.6 + 0.4
    return satura(passa(rosa(rng, n), 1200, 9000, 2) * pisca, 2.5) * sobe_e_some(n, 0.2, 1.3) * g


def maletada(rng, v):
    """A maletada: o giro da maleta (o "vuup" pesado), o "TOC" de couro e metal e os papéis farfalhando."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.3, 300, 1500, 0.85, 1.3, 0.5), 0.0)
    poe(x, modal(n_de(0.15), 480, rng=rng, razoes=[1.0, 2.2, 3.9], quedas=[0.06, 0.04, 0.02], ganhos=[1, 0.5, 0.3]) * 0.4, 0.28)
    poe(x, _acerto(rng, 0.9, 110), 0.28)
    poe(x, graos(rng, n_de(0.5), 30, 0.0, 0.45, 2500, 8000, 0.004) * 0.25, 0.32)
    return reverb(x, 0.3, 0.15)


def senbonzakura_corte(rng, v):
    """O corte do Byakuya: o corte limpo e fino (o "shiiin" longo e frio) e o sussurro das mil pétalas se
    espalhando (o chiado cintilante)."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.15, 2000, 7000, 0.7, 1.2, 0.4), 0.03)
    poe(x, B._lamina_curta(rng, n_de(0.6), 3200) * env(n_de(0.6), 0.001, 0.3) * 0.25, 0.1)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 4000, 11000, 2) * sobe_e_some(n, 0.25, 1.3) * 0.2, 0.15)
    poe(x, graos(rng, n, 60, 0.0, 0.8, 5000, 11000, 0.002, 0.8) * 0.2, 0.15)
    return reverb(x, 0.55, 0.28)


def leque_de_aco(rng, v):
    """O leque da Kitana: o leque abrindo (o "tchac" metálico), o zunido girando que vai e volta, e os dois
    cortes ao passar."""
    x = _z(1.2)
    poe(x, modal(n_de(0.15), 2600, rng=rng, **METAL) * env(n_de(0.15), 0.0005, 0.04) * 0.3, 0.0)
    n = n_de(0.75)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * np.abs(np.sin(2 * math.pi * 16 * t)) * np.sin(math.pi * t / 0.75) * 0.35, 0.0)
    for t0 in (0.3, 0.38):
        poe(x, B._lamina_curta(rng, n_de(0.2), 3000) * env(n_de(0.2), 0.001, 0.07) * 0.22, t0)
    poe(x, _acerto(rng, 0.45, 150, 2000, 7000), 0.32)
    return reverb(x, 0.35, 0.18)


def martelo_do_imperador(rng, v):
    """A marretada do Shao Kahn: a marreta subindo (o vento grave), descendo com tudo e o estrondo no chão, com
    as pedras rachando."""
    x = _z(1.4)
    poe(x, _whoosh(rng, 0.35, 200, 1000, 0.85, 1.3, 0.6), 0.0)
    poe(x, baque(n_de(0.6), 65, 30, 0.22, 1.0) * 1.0, 0.35)
    poe(x, _acerto(rng, 0.8, 90), 0.35)
    poe(x, graos(rng, n_de(0.6), 30, 0.0, 0.5, 500, 3500, 0.012) * 0.5, 0.37)
    return reverb(x, 0.5, 0.22)


def esmagada_do_snorlax(rng, v):
    """A barrigada do Snorlax: o assobio da queda, o "BLOMF" fofo e pesado, o chão tremendo e o ronco de sono."""
    x = _z(1.5)
    n = n_de(0.3)
    poe(x, seno(varre(900, 300, n, 1.0), n) * sobe_e_some(n, 0.7, 1.3) * 0.05, 0.0)
    poe(x, passa(baque(n_de(0.6), 60, 30, 0.25, 0.4), None, 800, 2) * 1.0, 0.28)
    poe(x, passa(rosa(rng, n_de(0.5)), 40, 400, 2) * env(n_de(0.5), 0.005, 0.3) * 0.5, 0.3)
    m = n_de(0.6)
    t = _t(m)
    ronco = satura(np.sin(2 * math.pi * np.cumsum(70 + 15 * t) / SR) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 25 * t))), 3)
    poe(x, passa(ronco, 60, 1200, 2) * sobe_e_some(m, 0.5, 1.3) * 0.1, 0.8)
    return reverb(x, 0.45, 0.22)


def tapao_estrela(rng, v):
    """O tapão do Patrick: o "flap" mole da mão de estrela, o tapa molhado e achatado, o "boing" da tremedeira e
    as estrelinhas."""
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.25, 500, 1500, 0.8, 1.3, 0.35), 0.0)
    poe(x, B._tapa(rng, n_de(0.1), 600, 3000, 0.03) * 1.1, 0.26)
    poe(x, _splash(rng, 0.2, 0.3, 300, 2500), 0.26)
    poe(x, _mola(0.4, 180, 0.5, 9, 0.18), 0.32)
    _estrelinhas(rng, 0.4, x)
    return reverb(x, 0.35, 0.18)


def socos_supersonicos(rng, v):
    """Os socos do Flecha: o "vwip" de chegada supersônica e a metralhadora de socos (os acertos colados em
    rajada)."""
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.15, 800, 5000, 0.9, 1.2, 0.5), 0.0)
    for k in range(9):
        poe(x, _acerto(rng, 0.45, 130 + 6 * k), 0.15 + 0.045 * k)
    return reverb(x, 0.25, 0.12)


def raio_de_mana(rng, v):
    """O raio de mana da Gwen: o zumbido mágico agudo (o tom cristalino que vibra) e os hexágonos estourando como
    vidro."""
    x = _z(1.1)
    n = n_de(0.45)
    t = _t(n)
    poe(x, (seno(880, n) + seno(1320, n) * 0.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 25 * t)) * sobe_e_some(n, 0.2, 1.3) * 0.08, 0.0)
    poe(x, passa(rosa(rng, n), 2500, 8000, 2) * sobe_e_some(n, 0.2, 1.3) * 0.15, 0.0)
    for k in range(5):
        poe(x, _brilho(rng, 0.3, 2000 + 350 * k, 0.05, VIDRO), 0.22 + 0.04 * k)
    poe(x, _acerto(rng, 0.4, 150), 0.2)
    return reverb(x, 0.45, 0.22)


def chute_da_viuva(rng, v):
    """O chute da Viúva Negra: o giro rápido, o pé acertando e o "bzzt" da Mordida da Viúva."""
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.25, 500, 3000, 0.8, 1.3, 0.5), 0.0)
    poe(x, _acerto(rng, 0.9, 120), 0.26)
    poe(x, _zap(rng, 0.35, 0.3), 0.3)
    return reverb(x, 0.3, 0.15)


def flecha_do_gaviao(rng, v):
    """A flecha do Gavião: a corda do arco soltando (o "tuang"), a flecha assobiando, o "toc" cravando e a
    ponta-surpresa estourando."""
    x = _z(1.1)
    n = n_de(0.2)
    poe(x, seno(varre(180, 140, n, 1.0), n) * env(n, 0.001, 0.12) * 0.25 + estalo(rng, n, 1000, 4000, 0.004) * 0.4, 0.0)
    m = n_de(0.22)
    poe(x, seno(varre(2600, 1800, m, 1.0), m) * sobe_e_some(m, 0.6, 1.3) * 0.05 + passa(rosa(rng, m), 2000, 8000, 2) * sobe_e_some(m, 0.6, 1.3) * 0.15, 0.02)
    poe(x, B._tapa(rng, n_de(0.05), 1500, 6000, 0.006) * 0.9, 0.22)
    poe(x, baque(n_de(0.4), 90, 45, 0.12, 0.8) * 0.7, 0.3)
    poe(x, passa(rosa(rng, n_de(0.3)), 300, 6000, 2) * env(n_de(0.3), 0.001, 0.12) * 0.4, 0.3)
    return reverb(x, 0.4, 0.2)


def godslayer(rng, v):
    """A Godslayer: o "clac-shiiing" da lâmina esticando e o corte largo."""
    x = _z(1.0)
    poe(x, modal(n_de(0.1), 2000, rng=rng, **METAL) * env(n_de(0.1), 0.0005, 0.03) * 0.3, 0.05)
    poe(x, B._lamina_curta(rng, n_de(0.4), 2800) * env(n_de(0.4), 0.01, 0.2) * 0.25, 0.08)
    poe(x, _whoosh(rng, 0.25, 800, 4500, 0.8, 1.3, 0.5), 0.05)
    poe(x, _acerto(rng, 0.7, 130, 2000, 7000), 0.26)
    return reverb(x, 0.4, 0.2)


def facas_de_drax(rng, v):
    """As facas do Drax: as duas facadas, uma atrás da outra (o "tchk" grosso de cada uma)."""
    x = _z(1.0)
    for t0 in (0.18, 0.3):
        poe(x, _whoosh(rng, 0.12, 1000, 4000, 0.8, 1.2, 0.3), t0 - 0.08)
        poe(x, _acerto(rng, 0.7, 140, 900, 4500), t0)
        poe(x, B._lamina_curta(rng, n_de(0.15), 2400) * env(n_de(0.15), 0.001, 0.05) * 0.15, t0)
    return reverb(x, 0.3, 0.15)


def soco_bioeletrico(rng, v):
    """O soco da Mulher-Aranha: o zumbido elétrico carregando na mão, o soco e a descarga estalando."""
    x = _z(1.0)
    n = n_de(0.28)
    poe(x, satura(seno(120, n) + seno(240, n) * 0.5, 3) * sobe_e_some(n, 0.8, 1.3) * 0.08, 0.0)
    poe(x, _zap(rng, 0.25, 0.15), 0.0)
    poe(x, _acerto(rng, 0.9, 120), 0.25)
    poe(x, _zap(rng, 0.35, 0.35), 0.27)
    return reverb(x, 0.35, 0.18)


def arranhao_felino(rng, v):
    """O arranhão da Mulher-Gato: o estalo do chicote e as três unhadas rasgando (o "shrrk" triplo)."""
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.15, 800, 4000, 0.8, 1.2, 0.3), 0.0)
    poe(x, estalo(rng, n_de(0.04), 2500, 10000, 0.005) * 1.0, 0.17)
    for k in range(3):
        n = n_de(0.1)
        poe(x, passa(rosa(rng, n), 2000, 8000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.4, 0.25 + 0.03 * k)
    poe(x, _acerto(rng, 0.5, 150, 2000, 7000), 0.26)
    return reverb(x, 0.35, 0.18)


def gas_do_medo(rng, v):
    """O gás do medo: o borrifo pressurizado (o "pssssh"), a nuvem girando e os gritos de pavor, abafados e
    distorcidos, que aparecem e somem."""
    x = _z(1.4)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 3000, 10000, 2) * sobe_e_some(n, 0.15, 1.3) * 0.4, 0.0)
    m = n_de(0.8)
    poe(x, passa(rosa(rng, m), 200, 1500, 2) * sobe_e_some(m, 0.4, 1.3) * 0.2, 0.2)
    for k in range(3):
        g = n_de(0.4)
        tt = _t(g)
        f = (500 + 120 * k) * (1 + 0.1 * np.sin(2 * math.pi * (5 + k) * tt))
        grito = satura(np.sin(2 * math.pi * np.cumsum(f) / SR), 2.5) * passa(rosa(rng, g), 400, 3000, 2) * 2
        poe(x, passa(grito, 300, 2500, 2) * sobe_e_some(g, 0.4, 1.3) * 0.04, 0.4 + 0.12 * k)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "maletada": (maletada, "básico do Leorio: a maleta e os papéis"),
    "senbonzakura-corte": (senbonzakura_corte, "básico do Byakuya: o corte e as pétalas"),
    "leque-de-aco": (leque_de_aco, "básico da Kitana: o leque girando"),
    "martelo-do-imperador": (martelo_do_imperador, "básico do Shao Kahn: a marreta no chão"),
    "esmagada-do-snorlax": (esmagada_do_snorlax, "básico do Snorlax: a barrigada e o ronco"),
    "tapao-estrela": (tapao_estrela, "básico do Patrick: o tapão mole"),
    "socos-supersonicos": (socos_supersonicos, "básico do Flecha: a rajada de socos"),
    "raio-de-mana": (raio_de_mana, "básico da Gwen: o raio e os hexágonos"),
    "chute-da-viuva": (chute_da_viuva, "básico da Viúva Negra: o chute e o choque"),
    "flecha-do-gaviao": (flecha_do_gaviao, "básico do Gavião: o arco, a flecha e o estouro"),
    "godslayer": (godslayer, "básico da Gamora: a lâmina esticando"),
    "facas-de-drax": (facas_de_drax, "básico do Drax: as duas facadas"),
    "soco-bioeletrico": (soco_bioeletrico, "básico da Mulher-Aranha: o soco elétrico"),
    "arranhao-felino": (arranhao_felino, "básico da Mulher-Gato: o chicote e as unhas"),
    "gas-do-medo": (gas_do_medo, "básico do Espantalho: o gás e os gritos"),
}
