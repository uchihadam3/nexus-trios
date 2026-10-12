"""Os sons da rodada 16: Ultron, Duende Verde, Surfista Prateado, Galactus e Senhor das Estrelas (veja
tools/vfx/familias_v2/rodada16.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada14 import _vento
from sfx_rodada15 import _laser
from som import CRISTAL, METAL, SINO, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _bipes(f0, quantos, passo, g=0.05):
    """Os bipes de máquina: tons curtos subindo, um atrás do outro."""
    x = _z(quantos * passo + 0.1)
    for k in range(quantos):
        m = n_de(0.04)
        poe(x, seno(f0 * (1.06 ** k), m) * env(m, 0.002, 0.03) * g, k * passo)
    return x


def _servo(rng, seg, f0=300, f1=600, g=0.06):
    """O motor elétrico: o zumbido que sobe com o chiado das engrenagens."""
    n = n_de(seg)
    t = _t(n)
    x = seno(varre(f0, f1, n, 1.0) * (1 + 0.02 * np.sin(2 * math.pi * 60 * t)), n) * 0.8 + passa(rosa(rng, n), 2000, 6000, 2) * 0.2
    return x * sobe_e_some(n, 0.3, 1.3) * g


def _explosao(rng, g=0.8, grave=55):
    n = n_de(0.9)
    return (satura(baque(n, grave, 25, 0.3, 1.0), 1.8) + passa(rosa(rng, n), 80, 5000, 2) * env(n, 0.002, 0.35) * 0.9 + graos(rng, n, 30, 0.0, 0.5, 600, 4000, 0.008) * 0.4) * g


def _risada(rng, f0=420, vezes=4, g=0.05):
    """A risada aguda e maluca: sílabas curtas que sobem e descem."""
    x = _z(vezes * 0.11 + 0.2)
    for k in range(vezes):
        m = n_de(0.08)
        f = f0 * (1.08 if k % 2 else 0.95) * (1 + 0.03 * k)
        poe(x, satura(seno(varre(f, f * 0.85, m, 1.0), m), 2.0) * env(m, 0.01, 0.05) * g, k * 0.11)
    return x


# =================================================================== Ultron
def analise_preditiva(rng, v):
    """A análise preditiva: o olho abrindo (o tom eletrônico), a varredura (o tom que vai e volta), os bipes de
    dados e o "clack" da mira travando."""
    x = _z(1.4)
    n = n_de(0.4)
    poe(x, seno(varre(200, 900, n, 1.0), n) * sobe_e_some(n, 0.6, 1.3) * 0.05, 0.0)
    m = n_de(0.5)
    poe(x, seno(700 + 300 * np.sin(2 * math.pi * 2 * _t(m)), m) * sobe_e_some(m, 0.3, 1.3) * 0.03, 0.1)
    poe(x, _bipes(1600, 6, 0.05, 0.05), 0.3)
    poe(x, modal(n_de(0.15), 2000, rng=rng, **METAL) * env(n_de(0.15), 0.0005, 0.05) * 0.25 + estalo(rng, n_de(0.15), 1500, 6000, 0.005) * 0.4, 0.35)
    poe(x, seno(varre(500, 250, n_de(0.3), 1.0), n_de(0.3)) * env(n_de(0.3), 0.01, 0.2) * 0.05, 0.6)
    return reverb(x, 0.4, 0.2)


def drones_de_defesa(rng, v):
    """Os drones de defesa: os três drones zunindo pelo ar, os escudos de hexágonos fechando (os "plim" de energia)
    e o raio de um deles."""
    x = _z(1.5)
    for k in range(3):
        n = n_de(0.35)
        poe(x, seno(varre(500 + 80 * k, 900 + 80 * k, n, 1.0) * (1 + 0.02 * np.sin(2 * math.pi * 40 * _t(n))), n) * sobe_e_some(n, 0.6, 1.2) * 0.04, 0.03 * k)
        poe(x, _brilho(rng, 0.4, 1175 * (1.12 ** k), 0.05, CRISTAL), 0.32 + 0.03 * k)
    poe(x, _laser(rng, 0.25, 1800, 1100, 0.1), 0.38)
    return reverb(x, 0.5, 0.25)


def ultron_preparo(rng, v):
    """O Preparo da Evolução autônoma: o zumbido grave da máquina pensando, os servos e os bipes dos circuitos."""
    x = _z(1.4)
    n = n_de(1.4)
    poe(x, (seno(55, n) + seno(110, n) * 0.4) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * _t(n))) * sobe_e_some(n, 0.3, 1.0) * 0.07, 0.0)
    poe(x, _servo(rng, 0.5, 200, 500, 0.04), 0.2)
    poe(x, _bipes(1400, 5, 0.12, 0.03), 0.6)
    return reverb(x, 0.5, 0.25)


def evolucao_autonoma(rng, v):
    """A evolução autônoma: os circuitos se reescrevendo (o chiado digital que pisca), o raio do peito e o Preparo
    do rival quebrando."""
    x = _z(1.6)
    n = n_de(0.3)
    pisca = (np.sin(2 * math.pi * 23 * _t(n)) > 0).astype(float)
    poe(x, passa(rosa(rng, n), 2000, 8000, 2) * pisca * sobe_e_some(n, 0.5, 1.2) * 0.25, 0.0)
    poe(x, _laser(rng, 0.4, 1200, 500, 0.15), 0.25)
    poe(x, satura(baque(n_de(0.3), 110, 60, 0.08, 1.0), 1.6) * 0.5, 0.35)
    poe(x, graos(rng, n_de(0.4), 25, 0.0, 0.3, 2500, 8000, 0.004) * 0.5 + modal(n_de(0.4), 1700, rng=rng, **METAL) * env(n_de(0.4), 0.0005, 0.12) * 0.15, 0.38)
    return reverb(x, 0.5, 0.25)


# =================================================================== Duende Verde
def bomba_abobora(rng, v):
    """A bomba abóbora: o "fwip" do arremesso, a risada do Duende, o tique do pavio e a explosão."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.3, 500, 2000, 0.6, 1.3, 0.4), 0.0)
    poe(x, _risada(rng, 440, 4, 0.05), 0.05)
    for k in range(3):
        poe(x, seno(2200, n_de(0.02)) * env(n_de(0.02), 0.001, 0.01) * 0.06, 0.2 + 0.05 * k)
    poe(x, _explosao(rng, 0.8, 60), 0.36)
    return reverb(x, 0.6, 0.3)


def gas_do_duende(rng, v):
    """O gás do Duende: o "pssssh" do gás saindo, a nuvem rolando grave e os gemidos assustadores dentro dela."""
    x = _z(1.8)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 2500, 9000, 2) * sobe_e_some(n, 0.2, 1.3) * 0.3, 0.0)
    m = n_de(1.2)
    poe(x, passa(rosa(rng, m), 100, 900, 2) * sobe_e_some(m, 0.4, 1.2) * 0.3, 0.1)
    for k in range(3):
        g = n_de(0.5)
        poe(x, seno(varre(260 + 40 * k, 180 + 30 * k, g, 1.0) * (1 + 0.04 * np.sin(2 * math.pi * 5 * _t(g))), g) * sobe_e_some(g, 0.4, 1.3) * 0.03, 0.35 + 0.15 * k)
    return reverb(x, 0.7, 0.35)


def duende_preparo(rng, v):
    """O Preparo da Prancha armadilhada: os jatos do planador chiando e a risada maluca ao fundo."""
    x = _z(1.4)
    n = n_de(1.4)
    poe(x, passa(rosa(rng, n), 600, 5000, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 9 * _t(n))) * sobe_e_some(n, 0.3, 1.0) * 0.25, 0.0)
    poe(x, _risada(rng, 460, 5, 0.04), 0.5)
    return reverb(x, 0.5, 0.25)


def prancha_armadilhada(rng, v):
    """A prancha armadilhada: o rasante dos jatos, as lâminas saindo (o "shink"), o corte e a carga explodindo."""
    x = _z(1.8)
    poe(x, _whoosh(rng, 0.4, 300, 2500, 0.8, 1.3, 0.6), 0.0)
    poe(x, modal(n_de(0.3), 2800, rng=rng, **METAL) * env(n_de(0.3), 0.0005, 0.1) * 0.25, 0.18)
    poe(x, _whoosh(rng, 0.12, 2000, 7000, 0.8, 1.2, 0.3), 0.25)
    poe(x, _explosao(rng, 0.7, 70), 0.43)
    return reverb(x, 0.6, 0.3)


# =================================================================== Surfista Prateado
def rajada_cosmica(rng, v):
    """A rajada cósmica: o raio prateado (o tom brilhante com o chiado das estrelas) e o "tiim" da marca."""
    x = _z(1.5)
    n = n_de(0.45)
    poe(x, (seno(varre(1800, 1200, n, 1.0), n) * 0.5 + seno(varre(2700, 1800, n, 1.0), n) * 0.3) * sobe_e_some(n, 0.1, 1.3) * 0.08, 0.05)
    poe(x, graos(rng, n, 30, 0.0, 0.4, 4000, 10000, 0.003) * 0.25, 0.05)
    poe(x, _brilho(rng, 0.8, 1568, 0.08, SINO), 0.3)
    return reverb(x, 0.6, 0.3)


def transmutacao_estelar(rng, v):
    """A transmutação estelar: as partículas girando (o brilho que sobe em espiral) e as três cascas fechando, cada
    uma num acorde de cristal."""
    x = _z(1.6)
    n = n_de(0.5)
    poe(x, (seno(varre(600, 1500, n, 1.0), n) * (1 + 0.05 * np.sin(2 * math.pi * 12 * _t(n)))) * sobe_e_some(n, 0.6, 1.2) * 0.04, 0.0)
    poe(x, graos(rng, n, 30, 0.0, 0.45, 3000, 9000, 0.003) * 0.2, 0.0)
    for k in range(3):
        poe(x, modal(n_de(0.6), 1047 * (1.25 ** k), rng=rng, **CRISTAL) * env(n_de(0.6), 0.002, 0.3) * 0.1, 0.35 + 0.04 * k)
    return reverb(x, 0.6, 0.3)


def surfista_preparo(rng, v):
    """O Preparo do Surfe dimensional: o zumbido cósmico da prancha e o vento das estrelas passando."""
    x = _z(1.4)
    n = n_de(1.4)
    poe(x, (seno(220, n) + seno(330, n) * 0.5 + seno(440 * (1 + 0.01 * np.sin(2 * math.pi * 3 * _t(n))), n) * 0.3) * sobe_e_some(n, 0.3, 1.0) * 0.04, 0.0)
    poe(x, _vento(rng, 1.4, 1500, 6000, 0.12), 0.0)
    return reverb(x, 0.7, 0.35)


def surfe_dimensional(rng, v):
    """O surfe dimensional: a prancha passando rasgando o espaço (o "vuuush" que sobe e o rasgo brilhante) e o
    impacto."""
    x = _z(1.6)
    poe(x, _whoosh(rng, 0.4, 400, 4000, 0.85, 1.3, 0.7), 0.0)
    n = n_de(0.4)
    poe(x, (seno(varre(400, 2000, n, 1.0), n) * 0.06 + passa(rosa(rng, n), 3000, 9000, 2) * 0.1) * sobe_e_some(n, 0.8, 1.2), 0.0)
    poe(x, satura(baque(n_de(0.5), 80, 35, 0.15, 1.0), 1.6) * 0.8, 0.32)
    poe(x, _brilho(rng, 0.6, 1319, 0.06, CRISTAL), 0.34)
    return reverb(x, 0.6, 0.3)


# =================================================================== Galactus
def dreno_planetario(rng, v):
    """O dreno planetário: o planeta roncando, a energia subindo em espiral (o tom que sobe e oscila) e a mão
    enorme fechando (o grave pesado)."""
    x = _z(1.8)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 30, 200, 2) * sobe_e_some(n, 0.3, 1.2) * 0.4, 0.0)
    m = n_de(0.7)
    poe(x, seno(varre(150, 700, m, 1.0) * (1 + 0.05 * np.sin(2 * math.pi * 8 * _t(m))), m) * sobe_e_some(m, 0.7, 1.2) * 0.06, 0.15)
    poe(x, satura(baque(n_de(0.6), 45, 22, 0.25, 0.6), 1.5) * 0.8, 0.65)
    return reverb(x, 0.8, 0.4)


def rajada_do_poder_cosmico(rng, v):
    """A rajada do Poder Cósmico: a voz enorme do Galactus (o coro grave), o elmo acendendo e as colunas caindo em
    estrondos."""
    x = _z(2.0)
    n = n_de(0.9)
    poe(x, (satura(seno(65, n), 1.6) + seno(98, n) * 0.6 + seno(130, n) * 0.3) * sobe_e_some(n, 0.3, 1.2) * 0.08, 0.0)
    for k in range(3):
        t0 = 0.27 + 0.05 * k
        poe(x, satura(baque(n_de(0.6), 60, 25, 0.25, 1.0), 1.6) * 0.6, t0)
        poe(x, passa(rosa(rng, n_de(0.5)), 500, 6000, 2) * env(n_de(0.5), 0.002, 0.2) * 0.3, t0)
    return reverb(x, 0.9, 0.45)


def devorador_preparo(rng, v):
    """O Preparo do Toque do Devorador: o ronco cósmico grave e tudo sendo sugado (o vento que vai para dentro)."""
    x = _z(1.4)
    n = n_de(1.4)
    poe(x, (seno(45, n) + seno(67, n) * 0.6) * (0.7 + 0.3 * np.sin(2 * math.pi * 1.5 * _t(n))) * sobe_e_some(n, 0.3, 1.0) * 0.09, 0.0)
    poe(x, _vento(rng, 1.4, 200, 2000, 0.25), 0.0)
    return reverb(x, 0.8, 0.4)


# =================================================================== Senhor das Estrelas
def plano_improvisado(rng, v):
    """O plano improvisado: o "clack" do play na fita, os primeiros acordes de rock, o tiro rápido do blaster e o
    impulso do trio."""
    x = _z(1.6)
    poe(x, modal(n_de(0.1), 1500, rng=rng, **METAL) * env(n_de(0.1), 0.0005, 0.03) * 0.3 + estalo(rng, n_de(0.1), 800, 4000, 0.006) * 0.4, 0.0)
    for k, f in enumerate((196, 247, 294, 247)):
        m = n_de(0.18)
        poe(x, passa(satura((seno(f, m) + seno(f * 1.5, m) * 0.6), 3.0), None, 2500, 2) * env(m, 0.005, 0.12) * 0.05, 0.08 + 0.15 * k)
    poe(x, _laser(rng, 0.15, 2400, 1200, 0.1), 0.16)
    poe(x, _whoosh(rng, 0.3, 400, 2000, 0.6, 1.3, 0.3), 0.4)
    return reverb(x, 0.4, 0.2)


def danca_de_distracao(rng, v):
    """A dança de distração: a batida de disco (o bumbo e o chimbal), a linha de baixo e o tom tonto dos rivais."""
    x = _z(2.0)
    for k in range(8):
        poe(x, passa(baque(n_de(0.2), 90, 50, 0.08, 0.3), None, 900, 2) * 0.4, 0.1 + 0.22 * k)
        poe(x, passa(rosa(rng, n_de(0.05)), 6000, 12000, 2) * env(n_de(0.05), 0.001, 0.03) * 0.15, 0.21 + 0.22 * k)
    for k, f in enumerate((110, 110, 165, 147, 110, 131, 147, 165)):
        m = n_de(0.18)
        poe(x, seno(f, m) * env(m, 0.005, 0.12) * 0.08, 0.1 + 0.22 * k)
    m = n_de(0.8)
    poe(x, seno(varre(700, 350, m, 1.0) * (1 + 0.06 * np.sin(2 * math.pi * 7 * _t(m))), m) * sobe_e_some(m, 0.2, 1.4) * 0.03, 0.9)
    return reverb(x, 0.4, 0.2)


SONS: dict = {
    "analise-preditiva": (analise_preditiva, "Ultron: a varredura, os dados e a mira"),
    "drones-de-defesa": (drones_de_defesa, "Ultron: os drones e os escudos"),
    "ultron-preparo": (ultron_preparo, "Ultron: a máquina pensando (antes do golpe)"),
    "evolucao-autonoma": (evolucao_autonoma, "Ultron: os circuitos e o raio"),
    "bomba-abobora": (bomba_abobora, "Duende Verde: a risada e a explosão"),
    "gas-do-duende": (gas_do_duende, "Duende Verde: o gás e os gemidos"),
    "duende-preparo": (duende_preparo, "Duende Verde: os jatos e a risada (antes do golpe)"),
    "prancha-armadilhada": (prancha_armadilhada, "Duende Verde: o rasante, as lâminas e a carga"),
    "rajada-cosmica": (rajada_cosmica, "Surfista Prateado: o raio prateado"),
    "transmutacao-estelar": (transmutacao_estelar, "Surfista Prateado: as cascas de cristal"),
    "surfista-preparo": (surfista_preparo, "Surfista Prateado: a prancha zunindo (antes do golpe)"),
    "surfe-dimensional": (surfe_dimensional, "Surfista Prateado: o rasgo no espaço e o impacto"),
    "dreno-planetario": (dreno_planetario, "Galactus: o planeta sugado e a mão"),
    "rajada-do-poder-cosmico": (rajada_do_poder_cosmico, "Galactus: a voz e as colunas"),
    "devorador-preparo": (devorador_preparo, "Galactus: tudo sendo sugado (antes do golpe)"),
    "plano-improvisado": (plano_improvisado, "Senhor das Estrelas: a fita, o rock e o tiro"),
    "danca-de-distracao": (danca_de_distracao, "Senhor das Estrelas: a batida de disco"),
}
