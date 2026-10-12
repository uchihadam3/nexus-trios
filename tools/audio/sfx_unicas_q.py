"""Os sons da rodada 16 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_q.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada08 import _corrente
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def polaridade(rng, v):
    """Magneto: o campo magnético zumbindo e os pedaços de metal batendo."""
    x = _z(2.1)
    n = n_de(1.2)
    t = _t(n)
    poe(x, satura(seno(60, n) + seno(120, n) * 0.5, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 4 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.08, 0.0)
    q = np.random.default_rng(3)
    for k in range(6):
        poe(x, _sino(rng, q.uniform(900, 2000), 0.25, 0.03, METAL), 0.4 + 0.08 * k)
    return reverb(x, 0.6, 0.3)


def empatia(rng, v):
    """Ravena: as asas da alma abrindo (o sopro escuro) e a cura passando (o tom claro)."""
    x = _z(2.1)
    poe(x, _sopro(rng, 0.6, 200, 1500, 0.3, 0.5), 0.0)
    poe(x, _acorde((147, 175, 220), 0.6, 0.04, 0.05, 0.5), 0.05)
    n = n_de(0.5)
    poe(x, seno(varre(500, 900, n), n) * env(n, 0.03, 0.4) * 0.04, 0.35)
    poe(x, _sino(rng, 1047, 0.6, 0.05, CRISTAL), 0.8)
    return reverb(x, 0.8, 0.4)


def doenca_terminal(rng, v):
    """Itachi: a tosse (os golpes secos) e os corvos batendo as asas."""
    x = _z(2.0)
    for k in range(2):
        n = n_de(0.12)
        poe(x, passa(rosa(rng, n), 300, 2000, 2) * env(n, 0.005, 0.1) * 0.35, 0.05 + 0.15 * k)
    for k in range(10):
        poe(x, passa(rosa(rng, n_de(0.05)), 800, 3500, 2) * env(n_de(0.05), 0.003, 0.03) * 0.25, 0.3 + 0.06 * k)
    for k in range(2):
        poe(x, _piu(1400, 900, 0.12, 0.03), 0.45 + 0.25 * k)
    return reverb(x, 0.7, 0.35)


def medica_de_campo(rng, v):
    """Sakura: o chakra verde da cura (o tom suave) e o losango de proteção (o sino)."""
    x = _z(2.0)
    n = n_de(0.8)
    t = _t(n)
    poe(x, seno(523 * (1 + 0.01 * np.sin(2 * math.pi * 6 * t)), n) * sobe_e_some(n, 0.4, 1.2) * 0.04, 0.0)
    poe(x, _acorde((523, 659, 784), 0.8, 0.035, 0.1, 0.6), 0.15)
    poe(x, _sino(rng, 1568, 0.6, 0.05, CRISTAL), 0.45)
    return reverb(x, 0.7, 0.35)


def ninguem_toca(rng, v):
    """Mikasa: o gancho disparando (o cabo), e as duas lâminas cruzando."""
    x = _z(1.9)
    poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.005), 0.0)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 2000, 8000, 2) * env(n, 0.005, 0.25) * 0.25, 0.0)
    for k in range(2):
        poe(x, _whoosh(rng, 0.15, 2500, 10000, 0.6, 1.4, 0.4), 0.28 + 0.07 * k)
        poe(x, _sino(rng, 3400 + 400 * k, 0.4, 0.05, METAL), 0.38 + 0.07 * k)
    return reverb(x, 0.5, 0.25)


def corte_na_nuca(rng, v):
    """Levi: o giro rapidíssimo (os cortes em sequência) e o corte final."""
    x = _z(1.9)
    for k in range(5):
        poe(x, _whoosh(rng, 0.1, 2000, 9000, 0.6, 1.4, 0.3), 0.04 + 0.07 * k)
    poe(x, _whoosh(rng, 0.15, 3000, 12000, 0.7, 1.3, 0.45), 0.42)
    poe(x, _sino(rng, 4000, 0.5, 0.06, METAL), 0.48)
    poe(x, _baque(150, 70, 0.2, 0.4), 0.48)
    return reverb(x, 0.5, 0.25)


def particulas_pym(rng, v):
    """Homem-Formiga: as partículas Pym (o zumbido que encolhe ou cresce)."""
    x = _z(2.0)
    n = n_de(0.6)
    poe(x, seno(varre(1600, 200, n, 0.7), n) * env(n, 0.02, 0.5) * 0.05, 0.0)
    poe(x, graos(rng, n_de(0.9), 60, 0.0, 0.9, 3000, 9000, 0.003) * 0.3, 0.0)
    poe(x, _piu(300, 1200, 0.15, 0.05), 0.5)
    poe(x, _baque(120, 60, 0.3, 0.5), 0.55)
    return reverb(x, 0.6, 0.3)


def sentido_radar(rng, v):
    """Demolidor: o mundo em ecos (os "pings" em anéis) e o batimento."""
    x = _z(2.0)
    for k in range(4):
        poe(x, _sino(rng, 1200, 0.4, 0.05 - 0.008 * k, VIDRO), 0.05 + 0.2 * k)
    for k in range(2):
        poe(x, _baque(60, 40, 0.2, 0.4, 1.6), 0.3 + 0.25 * k)
    return reverb(x, 0.9, 0.45)


def tempestade_pula(rng, v):
    """Tempestade: o raio estalando e pulando três vezes, e o trovão."""
    x = _z(2.0)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.05), 2000, 9000, 0.01), 0.15 + 0.18 * k)
        poe(x, graos(rng, n_de(0.15), 30, 0.0, 0.8, 3000, 10000, 0.002) * 0.4, 0.15 + 0.18 * k)
    poe(x, _trovao(rng, 0.9, 0.5), 0.2)
    return reverb(x, 0.6, 0.3)


def cerebro(rng, v):
    """Professor X: o Cérebro ligando (o tom que pulsa) e as ondas mentais."""
    x = _z(2.0)
    n = n_de(1.2)
    t = _t(n)
    poe(x, seno(varre(300, 600, n), n) * (0.6 + 0.4 * np.sin(2 * math.pi * 5 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.05, 0.0)
    poe(x, _acorde((330, 415, 494, 659), 1.0, 0.035, 0.1, 0.7), 0.3)
    for k in range(3):
        poe(x, seno(1200, n_de(0.1)) * env(n_de(0.1), 0.01, 0.08) * 0.03, 0.4 + 0.2 * k)
    return reverb(x, 0.8, 0.4)


def doze_por_cento(rng, v):
    """Senhor das Estrelas: o walkman (o botão e a musiquinha) e o plano rabiscado."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.03), 1000, 4000, 0.006), 0.0)
    for k, f in enumerate((392, 440, 494, 523, 494, 440)):
        n = n_de(0.1)
        poe(x, (_quadrada(f, n) * 0.4 + seno(f, n)) * env(n, 0.005, 0.08) * 0.03, 0.05 + 0.1 * k)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 2000, 7000, 2) * env(n, 0.01, 0.3) * 0.15, 0.4)
    poe(x, _piu(800, 1500, 0.1, 0.04), 0.75)
    return reverb(x, 0.4, 0.2)


def mares(rng, v):
    """Aquaman: a onda subindo e quebrando, e o tridente."""
    x = _z(2.2)
    n = n_de(1.4)
    poe(x, passa(rosa(rng, n), 150, 2500, 2) * sobe_e_some(n, 0.45, 1.3) * 0.4, 0.0)
    poe(x, _sino(rng, 784, 0.6, 0.05, METAL), 0.2)
    poe(x, _acorde((196, 247, 294, 392), 1.0, 0.04, 0.1, 0.7), 0.3)
    return reverb(x, 0.7, 0.35)


def selo_da_luz(rng, v):
    """Zelda: a Triforce brilhando (o arpejo mágico) e o selo fechando."""
    x = _z(2.1)
    for k, f in enumerate((587, 740, 880, 1175)):
        poe(x, _sino(rng, f, 0.5, 0.045, CRISTAL), 0.05 + 0.08 * k)
    poe(x, _acorde((587, 740, 880, 1175), 1.0, 0.04, 0.03, 0.7), 0.4)
    poe(x, _baque(200, 100, 0.15, 0.3), 0.4)
    return reverb(x, 0.8, 0.4)


def pod_042(rng, v):
    """2B: o Pod (o bipe) e o laser."""
    x = _z(1.9)
    for k in range(2):
        poe(x, seno(1800, n_de(0.06)) * env(n_de(0.06), 0.003, 0.05) * 0.04, 0.05 + 0.1 * k)
    n = n_de(0.4)
    poe(x, (seno(varre(1600, 600, n), n) * 0.05 + passa(rosa(rng, n), 3000, 9000, 2) * 0.15) * env(n, 0.005, 0.3), 0.35)
    return reverb(x, 0.5, 0.25)


def familiar(rng, v):
    """Alucard: a espada familiar girando (o zumbido de metal) e o morcego."""
    x = _z(2.0)
    n = n_de(0.7)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 12 * t) ** 2) * env(n, 0.02, 0.5) * 0.2, 0.0)
    poe(x, _sino(rng, 1600, 0.4, 0.04, METAL), 0.1)
    for k in range(4):
        poe(x, passa(rosa(rng, n_de(0.05)), 1000, 4000, 2) * env(n_de(0.05), 0.003, 0.03) * 0.25, 0.45 + 0.06 * k)
    poe(x, _piu(6000, 7000, 0.05, 0.02), 0.55)
    return reverb(x, 0.6, 0.3)


def corrente_intercepta(rng, v):
    """Shun: a corrente de Andrômeda girando e batendo no golpe."""
    x = _z(2.0)
    poe(x, _corrente(rng, 0.6, 12, 0.35), 0.0)
    poe(x, _sino(rng, 2400, 0.4, 0.05, METAL), 0.5)
    poe(x, _baque(200, 100, 0.15, 0.4), 0.5)
    return reverb(x, 0.6, 0.3)


def dois_lados(rng, v):
    """Saga: o acorde claro e o acorde escuro, um sobre o outro."""
    x = _z(2.2)
    poe(x, _acorde((392, 494, 587), 0.8, 0.04, 0.05, 0.6), 0.0)
    poe(x, _acorde((147, 175, 208), 0.9, 0.05, 0.05, 0.7), 0.35)
    poe(x, _sino(rng, 784, 0.6, 0.05, SINO), 0.35)
    return reverb(x, 0.8, 0.4)


def rendicao_sentidos(rng, v):
    """Shaka: o "om" grave da meditação e os sentidos se apagando (os sinos que somem)."""
    x = _z(2.4)
    n = n_de(1.6)
    t = _t(n)
    poe(x, (seno(98, n) + seno(196, n) * 0.4 + seno(294, n) * 0.15) * (1 + 0.1 * np.sin(2 * math.pi * 2 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.07, 0.0)
    for k in range(5):
        poe(x, _sino(rng, 1320 - 120 * k, 0.4, 0.04 - 0.006 * k, SINO), 0.4 + 0.1 * k)
    return reverb(x, 0.9, 0.45)


def areia(rng, v):
    """Gaara: a areia girando (o chiado que rodopia) e virando escudo (o baque fofo)."""
    x = _z(2.0)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.3, 0.0)
    poe(x, _baque(110, 60, 0.3, 0.5, 1.6), 0.6)
    return reverb(x, 0.5, 0.25)


def sem_esperanca(rng, v):
    """Darkseid: os olhos acendendo (o tom grave) e os raios ômega."""
    x = _z(2.1)
    n = n_de(0.8)
    poe(x, satura(seno(varre(55, 70, n), n), 3) * env(n, 0.05, 0.6) * 0.1, 0.0)
    for k in range(2):
        m = n_de(0.4)
        poe(x, seno(varre(400, 1200, m), m) * env(m, 0.005, 0.3) * 0.04, 0.3 + 0.05 * k)
    poe(x, _sino(rng, 300, 0.6, 0.06, SINO), 0.6)
    return reverb(x, 0.7, 0.35)


def necroplasma(rng, v):
    """Spawn: as correntes saindo, a capa esvoaçando e o necroplasma (o tom verde)."""
    x = _z(2.1)
    for k in range(2):
        poe(x, _corrente(rng, 0.4, 8, 0.3), 0.05 + 0.15 * k)
    poe(x, _whoosh(rng, 0.4, 300, 2500, 0.5, 1.4, 0.4), 0.2)
    n = n_de(0.8)
    poe(x, satura(seno(varre(110, 90, n), n), 2) * env(n, 0.05, 0.5) * 0.06, 0.4)
    return reverb(x, 0.7, 0.35)


def trio_unido(rng, v):
    """Leonardo: as três armas se juntando (os metais) e o grito de equipe (o acorde)."""
    x = _z(2.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.15, 1500, 6000, 0.6, 1.4, 0.3), 0.05 * k)
        poe(x, _sino(rng, 2200 + 300 * k, 0.4, 0.05, METAL), 0.33 + 0.03 * k)
    poe(x, _acorde((294, 370, 440, 587), 0.8, 0.045, 0.02, 0.6), 0.4)
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "mu-polaridade": (polaridade, "Magneto: a polaridade"),
    "mu-empatia": (empatia, "Ravena: a empatia"),
    "mu-doenca-terminal": (doenca_terminal, "Itachi: a doença"),
    "mu-medica-de-campo": (medica_de_campo, "Sakura: a médica"),
    "mu-ninguem-toca": (ninguem_toca, "Mikasa: ninguém toca neles"),
    "mu-corte-na-nuca": (corte_na_nuca, "Levi: o corte na nuca"),
    "mu-particulas-pym": (particulas_pym, "Homem-Formiga: as partículas"),
    "mu-sentido-radar": (sentido_radar, "Demolidor: o radar"),
    "mu-tempestade-pula": (tempestade_pula, "Tempestade: o raio"),
    "mu-cerebro": (cerebro, "Professor X: o Cérebro"),
    "mu-doze-por-cento": (doze_por_cento, "Senhor das Estrelas: 12%"),
    "mu-mares": (mares, "Aquaman: as marés"),
    "mu-selo-da-luz": (selo_da_luz, "Zelda: o selo"),
    "mu-pod-042": (pod_042, "2B: o Pod"),
    "mu-familiar": (familiar, "Alucard: o familiar"),
    "mu-corrente-intercepta": (corrente_intercepta, "Shun: a corrente"),
    "mu-dois-lados": (dois_lados, "Saga: os dois lados"),
    "mu-rendicao-sentidos": (rendicao_sentidos, "Shaka: os sentidos"),
    "mu-areia": (areia, "Gaara: a areia"),
    "mu-sem-esperanca": (sem_esperanca, "Darkseid: sem esperança"),
    "mu-necroplasma": (necroplasma, "Spawn: o necroplasma"),
    "mu-trio-unido": (trio_unido, "Leonardo: o trio unido"),
}
