"""Os sons da rodada 15: Professor Xavier, Venom, Carnificina, Doutor Destino e Loki (veja
tools/vfx/familias_v2/rodada15.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada11 import _molhado
from sfx_rodada13 import _zap
from sfx_rodada14 import _psi
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _rosnado_simbionte(rng, seg, f0=70, g=0.3):
    """O rosnado molhado do simbionte: o grave áspero que treme, com o chiado da saliva."""
    n = n_de(seg)
    t = _t(n)
    x = satura(seno(f0 * (1 + 0.08 * np.sin(2 * math.pi * 23 * t)), n) * (0.6 + 0.4 * np.abs(np.sin(2 * math.pi * 11 * t))), 3.0) * 0.7
    x += passa(rosa(rng, n), 1500, 6000, 2) * 0.25
    return passa(x, None, 2500, 2) * sobe_e_some(n, 0.25, 1.3) * g


def _corte_de_carne(rng, g=0.5):
    """O corte de lâmina na carne: o assobio curto e o rasgo molhado."""
    x = _z(0.35)
    poe(x, _whoosh(rng, 0.1, 1500, 6000, 0.8, 1.2, 0.3), 0.0)
    poe(x, passa(rosa(rng, n_de(0.2)), 400, 3500, 2) * env(n_de(0.2), 0.002, 0.08) * 0.8, 0.08)
    return x * g


def _laser(rng, seg, f0=1800, f1=900, g=0.08):
    """O laser de armadura: o tom limpo que desce com o chiado elétrico."""
    n = n_de(seg)
    return (seno(varre(f0, f1, n, 1.0), n) * 0.8 + seno(varre(f0 * 1.5, f1 * 1.5, n, 1.0), n) * 0.3) * env(n, 0.003, seg * 0.6) * g + passa(rosa(rng, n), 3000, 9000, 2) * env(n, 0.002, seg * 0.4) * g * 0.8


def _coro_mistico(n, f, g=0.05):
    """O acorde místico verde do Destino: o tom menor aberto que pulsa devagar."""
    t = _t(n)
    return (seno(f, n) + seno(f * 1.2, n) * 0.7 + seno(f * 1.5, n) * 0.6) * (0.75 + 0.25 * np.sin(2 * math.pi * 2.5 * t)) * g


# =================================================================== Professor Xavier
def coordenacao_mental(rng, v):
    """A coordenação mental: o zumbido da mente e os três "plim" de cada aliado ligando, subindo de tom."""
    x = _z(1.4)
    n = n_de(0.6)
    poe(x, _psi(n, 220, 330, 0.05) * sobe_e_some(n, 0.4, 1.2), 0.0)
    for k in range(3):
        poe(x, _brilho(rng, 0.5, 784 * (1.26 ** k), 0.07, CRISTAL), 0.4 + 0.08 * k)
    poe(x, seno(varre(600, 1200, n_de(0.3), 1.0), n_de(0.3)) * sobe_e_some(n_de(0.3), 0.8, 1.2) * 0.04, 0.55)
    return reverb(x, 0.6, 0.3)


def bloqueio_mental(rng, v):
    """O bloqueio mental: os anéis psíquicos indo (os "uom-uom"), a intenção batendo na barreira e quebrando como
    vidro, e o tom tonto."""
    x = _z(1.5)
    for k in range(4):
        n = n_de(0.2)
        poe(x, _psi(n, 400 - 30 * k, 300 - 30 * k, 0.05) * env(n, 0.01, 0.12), 0.08 + 0.06 * k)
    poe(x, modal(n_de(0.5), 2600, rng=rng, desafina=0.05, **VIDRO) * env(n_de(0.5), 0.0005, 0.2) * 0.25 + graos(rng, n_de(0.5), 20, 0.0, 0.3, 3000, 9000, 0.004) * 0.5, 0.5)
    poe(x, passa(baque(n_de(0.2), 140, 80, 0.05, 0.5), None, 1200, 2) * 0.5, 0.5)
    m = n_de(0.6)
    poe(x, seno(varre(700, 350, m, 1.0) * (1 + 0.06 * np.sin(2 * math.pi * 7 * _t(m))), m) * sobe_e_some(m, 0.2, 1.4) * 0.05, 0.6)
    return reverb(x, 0.55, 0.28)


def cerebro_preparo(rng, v):
    """O Preparo do Cérebro: a máquina ligando (o zumbido elétrico grave) e a varredura girando (o tom que vai e
    volta)."""
    x = _z(1.4)
    n = n_de(1.4)
    t = _t(n)
    poe(x, (seno(60, n) + seno(120, n) * 0.5) * sobe_e_some(n, 0.3, 1.0) * 0.06, 0.0)
    poe(x, seno(600 + 250 * np.sin(2 * math.pi * 1.0 * t), n) * sobe_e_some(n, 0.3, 1.0) * 0.035, 0.0)
    poe(x, _psi(n, 300, 300, 0.03) * sobe_e_some(n, 0.3, 1.0), 0.0)
    return reverb(x, 0.6, 0.3)


def paralisia_mental(rng, v):
    """A paralisia mental: a onda psíquica enorme (o "VUUUM" grave que varre) e o silêncio que corta (o tom que
    some de repente, com o zumbido parado)."""
    x = _z(1.8)
    n = n_de(0.7)
    poe(x, _psi(n, 120, 90, 0.1) * env(n, 0.02, 0.45), 0.0)
    poe(x, _whoosh(rng, 0.6, 200, 1500, 0.4, 1.3, 0.5), 0.0)
    poe(x, baque(n_de(0.5), 60, 35, 0.2, 0.4) * 0.5, 0.15)
    m = n_de(0.8)
    poe(x, seno(440, m) * env(m, 0.01, 0.5) * 0.04 * (np.arange(m) < m * 0.4), 0.5)
    poe(x, _brilho(rng, 0.5, 1047, 0.04, SINO), 0.55)
    return reverb(x, 0.7, 0.35)


# =================================================================== Venom
def mordida_predatoria(rng, v):
    """A mordida predatória: o rosnado do simbionte, a bocarra abrindo (o som molhado), a mordida (o estalo duro) e o
    chiado da cura subindo."""
    x = _z(1.6)
    poe(x, _rosnado_simbionte(rng, 0.45, 75, 0.45), 0.0)
    poe(x, _molhado(rng, 0.3, 0.3), 0.1)
    poe(x, satura(baque(n_de(0.4), 110, 50, 0.08, 1.0), 2.0) * 0.8 + estalo(rng, n_de(0.4), 800, 4000, 0.02) * 0.7, 0.36)
    poe(x, _molhado(rng, 0.4, 0.25, 200, 1500), 0.42)
    m = n_de(0.4)
    poe(x, seno(varre(400, 800, m, 1.0), m) * sobe_e_some(m, 0.4, 1.3) * 0.04, 0.6)
    return reverb(x, 0.5, 0.25)


def venom_preparo(rng, v):
    """O Preparo do Simbionte faminto: as bolhas da gosma estourando e o rosnado baixo crescendo."""
    x = _z(1.4)
    poe(x, _rosnado_simbionte(rng, 1.3, 60, 0.3), 0.05)
    for k in range(10):
        m = n_de(0.05)
        poe(x, seno(varre(200 + 30 * k, 500 + 30 * k, m, 1.0), m) * env(m, 0.003, 0.04) * 0.08, 0.1 + 0.12 * k)
    return reverb(x, 0.5, 0.25)


def simbionte_faminto(rng, v):
    """O simbionte faminto: os tentáculos chicoteando de todos os lados (os "fwap" molhados), o rugido "WE ARE
    VENOM" grave e o engolir pesado."""
    x = _z(2.0)
    for k in range(6):
        poe(x, _whoosh(rng, 0.15, 400, 2500, 0.8, 1.2, 0.3), 0.02 + 0.05 * k)
        poe(x, _molhado(rng, 0.15, 0.25), 0.1 + 0.05 * k)
    poe(x, _rosnado_simbionte(rng, 0.8, 55, 0.6), 0.3)
    poe(x, satura(baque(n_de(0.7), 50, 25, 0.3, 1.0), 1.8) * 0.9, 0.5)
    poe(x, _molhado(rng, 0.6, 0.4, 100, 1200), 0.5)
    return reverb(x, 0.6, 0.3)


# =================================================================== Carnificina
def ferida_aberta(rng, v):
    """A ferida aberta: os dois chicotes estalando, os cortes em X e o sangue espirrando."""
    x = _z(1.4)
    for k, t0 in enumerate((0.05, 0.15)):
        poe(x, satura(passa(rosa(rng, n_de(0.06)), 1500, 8000, 2) * env(n_de(0.06), 0.0005, 0.02), 2.5) * 0.6, t0 + 0.1)
        poe(x, _corte_de_carne(rng, 0.6), t0 + 0.05)
    poe(x, _molhado(rng, 0.4, 0.3), 0.3)
    poe(x, _brilho(rng, 0.4, 1568, 0.04, METAL), 0.6)
    return reverb(x, 0.45, 0.22)


def carnificina_preparo(rng, v):
    """O Preparo da Carnificina total: os tentáculos se debatendo (os "fwip" que não param) e a risada aguda e
    insana ao fundo."""
    x = _z(1.4)
    for k in range(8):
        poe(x, _whoosh(rng, 0.12, 600, 3000, 0.7, 1.2, 0.18), 0.05 + 0.16 * k)
    for k in range(5):
        m = n_de(0.09)
        f = 420 + 40 * math.sin(k)
        poe(x, satura(seno(varre(f, f * 0.85, m, 1.0), m), 2.0) * env(m, 0.01, 0.06) * 0.05, 0.4 + 0.1 * k)
    return reverb(x, 0.5, 0.25)


def carnificina_total(rng, v):
    """A carnificina total: a rajada de lâminas e machados de todos os lados (nove cortes colados) e o sangue
    espirrando no fim."""
    x = _z(1.8)
    for k in range(9):
        poe(x, _corte_de_carne(rng, 0.55 + 0.03 * k), 0.04 + 0.05 * k)
        if k % 3 == 0:
            poe(x, modal(n_de(0.2), 1500, rng=rng, **METAL) * env(n_de(0.2), 0.0005, 0.06) * 0.15, 0.08 + 0.05 * k)
    poe(x, _molhado(rng, 0.6, 0.45, 150, 2000), 0.3)
    poe(x, satura(baque(n_de(0.5), 70, 35, 0.15, 1.0), 1.8) * 0.6, 0.45)
    return reverb(x, 0.55, 0.28)


# =================================================================== Doutor Destino
def armadura_de_doom(rng, v):
    """A armadura de Doom: os bipes da análise varrendo, a trava da mira, o raio da manopla e o escudo fechando."""
    x = _z(1.6)
    for k in range(5):
        m = n_de(0.04)
        poe(x, seno(1800 + 200 * k, m) * env(m, 0.002, 0.03) * 0.05, 0.03 + 0.05 * k)
    poe(x, modal(n_de(0.12), 2200, rng=rng, **METAL) * env(n_de(0.12), 0.0005, 0.04) * 0.25, 0.3)
    poe(x, _laser(rng, 0.35, 1600, 700, 0.12), 0.38)
    poe(x, satura(baque(n_de(0.3), 120, 60, 0.07, 1.0), 1.6) * 0.5, 0.45)
    poe(x, modal(n_de(0.7), 520, rng=rng, **METAL) * env(n_de(0.7), 0.003, 0.35) * 0.12, 0.6)
    return reverb(x, 0.5, 0.25)


def ritual_latveriano(rng, v):
    """O ritual latveriano: o acorde místico abrindo, as runas girando (os toques) e os raios verdes estalando."""
    x = _z(1.8)
    n = n_de(1.1)
    poe(x, _coro_mistico(n, 147, 0.05) * sobe_e_some(n, 0.3, 1.2), 0.0)
    for k in range(5):
        poe(x, _brilho(rng, 0.3, 1175 * (1 + 0.12 * (k % 3)), 0.03, SINO), 0.05 + 0.08 * k)
    poe(x, _zap(rng, 0.45, 0.35), 0.3)
    poe(x, satura(passa(rosa(rng, n_de(0.1)), 1500, 9000, 2) * env(n_de(0.1), 0.0005, 0.04), 2.5) * 0.4, 0.32)
    poe(x, modal(n_de(0.7), 520, rng=rng, **METAL) * env(n_de(0.7), 0.003, 0.35) * 0.12, 0.6)
    return reverb(x, 0.65, 0.32)


def destino_preparo(rng, v):
    """O Preparo do Plano de contingência: o acorde místico baixo pulsando e o zumbido da armadura carregando."""
    x = _z(1.4)
    n = n_de(1.4)
    poe(x, _coro_mistico(n, 110, 0.05) * sobe_e_some(n, 0.3, 1.0), 0.0)
    poe(x, seno(varre(80, 160, n, 1.0), n) * sobe_e_some(n, 0.8, 1.0) * 0.05, 0.0)
    return reverb(x, 0.6, 0.3)


def plano_de_contingencia(rng, v):
    """O plano de contingência: o círculo místico abrindo, os seis lasers caindo um atrás do outro e a explosão
    verde enorme."""
    x = _z(2.2)
    n = n_de(0.8)
    poe(x, _coro_mistico(n, 131, 0.05) * sobe_e_some(n, 0.4, 1.2), 0.0)
    for k in range(6):
        poe(x, _laser(rng, 0.25, 2000 - 120 * k, 800, 0.08), 0.12 + 0.04 * k)
    poe(x, satura(baque(n_de(1.0), 50, 22, 0.35, 1.0), 1.8) * 1.0, 0.45)
    poe(x, passa(rosa(rng, n_de(0.9)), 100, 5000, 2) * env(n_de(0.9), 0.002, 0.4) * 0.7, 0.45)
    poe(x, _zap(rng, 0.4, 0.2), 0.5)
    return reverb(x, 0.8, 0.4)


# =================================================================== Loki
def troca_de_lugar(rng, v):
    """A troca de lugar: o "fsssh" da fumaça verde girando, o brilho dourado da magia e o "plop" da troca, com o tom
    que escorrega."""
    x = _z(1.5)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 800, 5000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 9 * _t(n))) * sobe_e_some(n, 0.5, 1.2) * 0.35, 0.1)
    for k in range(4):
        poe(x, _brilho(rng, 0.3, 1319 * (1.12 ** k), 0.04, CRISTAL), 0.15 + 0.07 * k)
    poe(x, seno(varre(900, 300, n_de(0.15), 1.0), n_de(0.15)) * env(n_de(0.15), 0.003, 0.1) * 0.08, 0.48)
    m = n_de(0.5)
    poe(x, seno(varre(600, 450, m, 1.0) * (1 + 0.04 * np.sin(2 * math.pi * 6 * _t(m))), m) * sobe_e_some(m, 0.2, 1.3) * 0.04, 0.55)
    return reverb(x, 0.55, 0.28)


def loki_preparo(rng, v):
    """O Preparo do Engano perfeito: o acorde dourado que brilha e os ecos das cópias aparecendo (os "plim" que
    pulam de lado)."""
    x = _z(1.4)
    n = n_de(1.4)
    poe(x, (seno(392, n) + seno(494, n) * 0.6 + seno(587, n) * 0.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 2 * _t(n))) * sobe_e_some(n, 0.3, 1.0) * 0.035, 0.0)
    for k in range(4):
        poe(x, _brilho(rng, 0.35, 1568 * (1.06 ** k), 0.04, CRISTAL), 0.15 + 0.3 * k)
    return reverb(x, 0.7, 0.35)


def engano_perfeito(rng, v):
    """O engano perfeito: as cópias quebrando como vidro (quatro, uma atrás da outra), a risada curta do Loki e a
    adaga entrando por trás."""
    x = _z(1.8)
    for k in range(4):
        poe(x, modal(n_de(0.4), 2400 + 200 * k, rng=rng, desafina=0.05, **VIDRO) * env(n_de(0.4), 0.0005, 0.15) * 0.18 + graos(rng, n_de(0.4), 15, 0.0, 0.25, 3000, 9000, 0.004) * 0.4, 0.25 + 0.06 * k)
    for k in range(3):
        m = n_de(0.08)
        poe(x, satura(seno(varre(330, 300, m, 1.0), m), 1.6) * env(m, 0.01, 0.05) * 0.05, 0.5 + 0.1 * k)
    poe(x, _whoosh(rng, 0.12, 2000, 7000, 0.8, 1.2, 0.3), 0.58)
    poe(x, _corte_de_carne(rng, 0.5), 0.62)
    poe(x, _brilho(rng, 0.5, 1760, 0.06, METAL), 0.64)
    return reverb(x, 0.55, 0.28)


SONS: dict = {
    "coordenacao-mental": (coordenacao_mental, "Professor Xavier: a mente ligando o trio"),
    "bloqueio-mental": (bloqueio_mental, "Professor Xavier: os anéis e a intenção quebrando"),
    "cerebro-preparo": (cerebro_preparo, "Professor Xavier: o Cérebro ligando (antes do golpe)"),
    "paralisia-mental": (paralisia_mental, "Professor Xavier: a onda e o silêncio"),
    "mordida-predatoria": (mordida_predatoria, "Venom: o rosnado e a mordida"),
    "venom-preparo": (venom_preparo, "Venom: a gosma borbulhando (antes do golpe)"),
    "simbionte-faminto": (simbionte_faminto, "Venom: os tentáculos e o rugido"),
    "ferida-aberta": (ferida_aberta, "Carnificina: os chicotes e o sangue"),
    "carnificina-preparo": (carnificina_preparo, "Carnificina: os tentáculos e a risada (antes do golpe)"),
    "carnificina-total": (carnificina_total, "Carnificina: a rajada de lâminas"),
    "armadura-de-doom": (armadura_de_doom, "Doutor Destino: a análise, o raio e o escudo"),
    "ritual-latveriano": (ritual_latveriano, "Doutor Destino: o acorde místico e os raios"),
    "destino-preparo": (destino_preparo, "Doutor Destino: a armadura carregando (antes do golpe)"),
    "plano-de-contingencia": (plano_de_contingencia, "Doutor Destino: os lasers e a explosão"),
    "troca-de-lugar": (troca_de_lugar, "Loki: a fumaça e a troca"),
    "loki-preparo": (loki_preparo, "Loki: o acorde dourado (antes do golpe)"),
    "engano-perfeito": (engano_perfeito, "Loki: as cópias quebrando e a adaga"),
}
