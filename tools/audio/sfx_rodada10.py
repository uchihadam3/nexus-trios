"""Os sons da rodada 10: Denji, Power, Makima, Frieren e Anya (veja tools/vfx/familias_v2/rodada10.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _motor(rng, seg, f0=38.0, f1=62.0, g=0.4):
    """O motor da motosserra: o ronco de dois tempos (o pulso rápido e áspero) que acelera."""
    n = n_de(seg)
    t = _t(n)
    f = np.linspace(f0, f1, n)
    fase = 2 * math.pi * np.cumsum(f) / SR
    pulsos = (0.5 + 0.5 * np.sign(np.sin(fase))) ** 1
    x = satura(passa(rosa(rng, n), 80, 2500, 2) * (0.3 + 0.7 * pulsos) + np.sin(fase * 2) * 0.3, 3)
    return x * sobe_e_some(n, 0.15, 1.3) * g


def _corrente_serra(rng, seg, g=0.3):
    """A corrente da serra correndo: o chiado metálico rápido."""
    n = n_de(seg)
    t = _t(n)
    return passa(rosa(rng, n), 2000, 9000, 2) * (0.6 + 0.4 * np.abs(np.sin(2 * math.pi * 90 * t))) * sobe_e_some(n, 0.2, 1.3) * g


def _respingo(rng, g=0.3):
    n = n_de(0.2)
    return passa(rosa(rng, n), 200, 2500, 2) * env(n, 0.002, 0.15) * g


# =================================================================== Denji
def puxar_a_corda(rng, v):
    """A cordinha: o "zip" da corda sendo puxada, o motor engasgando e pegando (o "bru-bru-BRRRAAAM") e a
    serra saltando com o chiado da corrente."""
    x = _z(1.8)
    n = n_de(0.2)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * sobe_e_some(n, 0.6, 1.4) * 0.4 + seno(varre(300, 900, n, 1.0), n) * env(n, 0.01, 0.18) * 0.06, 0.0)
    for k in range(2):
        poe(x, _motor(rng, 0.12, 25, 30, 0.35), 0.22 + 0.13 * k)
    poe(x, _motor(rng, 1.1, 35, 70, 0.55), 0.48)
    poe(x, _corrente_serra(rng, 0.9, 0.2), 0.55)
    return reverb(x, 0.4, 0.2)


def frenesi_de_sangue(rng, v):
    """O frenesi: a motosserra a toda (o ronco alto o tempo todo) e três cortes rasgando (o "rrrnnngg"
    quando a serra morde) com o sangue espirrando."""
    x = _z(1.7)
    poe(x, _motor(rng, 1.5, 60, 72, 0.45), 0.0)
    for k in range(3):
        n = n_de(0.25)
        morde = satura(passa(rosa(rng, n), 300, 4000, 2) * (0.5 + 0.5 * np.sign(np.sin(2 * math.pi * 70 * _t(n)))), 3) * sobe_e_some(n, 0.3, 1.4) * 0.45
        poe(x, morde, 0.08 + 0.18 * k)
        poe(x, _respingo(rng, 0.3), 0.18 + 0.18 * k)
    return reverb(x, 0.45, 0.2)


# =================================================================== Power
def lanca_de_sangue(rng, v):
    """A lança de sangue: as gotas se juntando (o borbulhar líquido que se aperta), a lança disparando
    (o "fwip" molhado) e cravando com o espirro."""
    x = _z(1.5)
    for k in range(8):
        n = n_de(0.08)
        poe(x, seno(varre(400 + 60 * k, 200, n, 1.0), n) * env(n, 0.002, 0.06) * 0.07, 0.02 + 0.04 * k)
    poe(x, _whoosh(rng, 0.25, 600, 2500, 0.8, 1.4, 0.5), 0.4)
    poe(x, baque(n_de(0.3), 120, 60, 0.08, 0.6) * 0.5, 0.58)
    poe(x, _respingo(rng, 0.5), 0.58)
    return reverb(x, 0.45, 0.22)


def power_preparo(rng, v):
    """O Preparo do Prêmio: o sangue girando (o líquido rodando) e o riso convencido da Power (o "hehe"
    agudo, em sílabas)."""
    x = _z(1.3)
    n = n_de(1.1)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.7, 1.1) * 0.3, 0.0)
    for k in range(3):
        m = n_de(0.08)
        poe(x, (seno(varre(900, 700, m, 1.0), m) + passa(rosa(rng, m), 1500, 4000, 2) * 0.3) * env(m, 0.005, 0.06) * 0.06, 0.5 + 0.12 * k)
    return reverb(x, 0.45, 0.25)


def premio_de_sangue(rng, v):
    """O Prêmio de sangue: os espinhos de sangue rompendo o chão em volta (os "tchuk" molhados em roda), as
    gotas caindo e o assobio tonto que gira."""
    x = _z(1.8)
    for k in range(12):
        poe(x, baque(n_de(0.15), 160, 90, 0.05, 0.6) * 0.3, 0.05 + 0.025 * k)
        poe(x, _respingo(rng, 0.15), 0.05 + 0.025 * k)
    for k in range(8):
        n = n_de(0.06)
        poe(x, passa(rosa(rng, n), 600, 3000, 2) * env(n, 0.002, 0.04) * 0.12, 0.5 + 0.05 * k)
    m = n_de(0.9)
    t = _t(m)
    poe(x, seno(900 + 200 * np.sin(2 * math.pi * 3 * t), m) * sobe_e_some(m, 0.3, 1.3) * 0.04, 0.6)
    return reverb(x, 0.5, 0.25)


# =================================================================== Makima
def olhar_de_comando(rng, v):
    """O Olhar de comando: o silêncio pesado (o tom grave baixíssimo), o olho abrindo (o tom que sobe
    devagar) e a ordem que bate (dois pulsos de pressão)."""
    x = _z(1.8)
    n = n_de(1.4)
    poe(x, seno(48, n) * sobe_e_some(n, 0.4, 1.2) * 0.2, 0.0)
    m = n_de(0.6)
    poe(x, seno(varre(300, 520, m, 1.2), m) * sobe_e_some(m, 0.8, 1.3) * 0.06, 0.05)
    for k in range(2):
        poe(x, baque(n_de(0.4), 65, 35, 0.2, 0.1) * 0.6, 0.6 + 0.2 * k)
        poe(x, _whoosh(rng, 0.35, 200, 900, 0.2, 1.4, 0.2), 0.6 + 0.2 * k)
    return reverb(x, 0.6, 0.35)


def corrente_de_obediencia(rng, v):
    """A Corrente de obediência: a guia correndo (o fio de metal fino zunindo), a coleira fechando (o
    "clic" metálico seco) e o silêncio imposto (o som cortado)."""
    x = _z(1.5)
    n = n_de(0.35)
    poe(x, seno(varre(3200, 2200, n, 1.0), n) * env(n, 0.01, 0.3) * 0.04 + passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.4, 1.3) * 0.15, 0.0)
    poe(x, modal(n_de(0.4), 2400, rng=rng, **METAL) * env(n_de(0.4), 0.001, 0.2) * 0.3, 0.45)
    poe(x, estalo(rng, n_de(0.015), 2000, 8000) * 0.7, 0.45)
    m = n_de(0.4)
    poe(x, passa(rosa(rng, m), 100, 800, 2) * env(m, 0.001, 0.3) * 0.2, 0.55)
    return reverb(x, 0.5, 0.25)


def controle_total(rng, v):
    """O "bang": a palavra seca (o estalo de dedo apontado, como um tiro abafado), a pressão descendo (o
    zumbido grave que aperta) e o esmagamento (o baque enorme e o estalo das rachaduras)."""
    x = _z(1.8)
    poe(x, estalo(rng, n_de(0.03), 600, 3000) * 0.8, 0.0)
    n = n_de(0.5)
    poe(x, seno(varre(200, 50, n, 0.7), n) * sobe_e_some(n, 0.8, 1.2) * 0.25, 0.25)
    poe(x, baque(n_de(0.8), 55, 26, 0.4, 0.7) * 1.0, 0.75)
    poe(x, graos(rng, n_de(0.5), 18, 0.0, 0.4, 600, 3500, 0.006, 0.6) * 0.4, 0.78)
    return reverb(x, 0.5, 0.25)


# =================================================================== Frieren
def analise_de_mana(rng, v):
    """A Análise de mana: o círculo mágico acendendo (o acorde de sino suave), o feixe varrendo (o tom fino
    que sobe) e os buffs saindo (os "plim" que se espalham)."""
    x = _z(1.8)
    poe(x, _brilho(rng, 1.0, 784, 0.06, SINO), 0.0)
    poe(x, _brilho(rng, 1.0, 1175, 0.04, SINO), 0.08)
    n = n_de(0.5)
    poe(x, seno(varre(1200, 2600, n, 1.0), n) * sobe_e_some(n, 0.6, 1.3) * 0.04, 0.3)
    for k in range(5):
        poe(x, _brilho(rng, 0.25, 2000 + 350 * k, 0.04, CRISTAL), 0.75 + 0.05 * k)
    return reverb(x, 0.65, 0.35)


def frieren_preparo(rng, v):
    """O Preparo da Magia: os círculos girando (o zumbido mágico em camadas, leve) e o sopro de mana."""
    x = _z(1.3)
    n = n_de(1.2)
    t = _t(n)
    camadas = sum(seno(f * (1 + 0.003 * np.sin(2 * math.pi * 4 * t)), n) * a for f, a in ((392, 1), (588, 0.6), (784, 0.4)))
    poe(x, camadas * sobe_e_some(n, 0.8, 1.1) * 0.04, 0.0)
    poe(x, passa(rosa(rng, n), 1500, 5000, 2) * sobe_e_some(n, 0.8, 1.1) * 0.08, 0.0)
    return reverb(x, 0.65, 0.35)


def magia_preparada(rng, v):
    """A Magia preparada: os círculos abrindo um a um (os "tlin" mágicos subindo), a carga (o tom que
    cresce) e os feixes disparando juntos (o "pshhh" afinado e o estouro)."""
    x = _z(1.9)
    for k in range(6):
        poe(x, _brilho(rng, 0.4, 880 * 2 ** (k / 6), 0.05, CRISTAL), 0.04 + 0.06 * k)
    n = n_de(0.4)
    poe(x, seno(varre(400, 1200, n, 1.4), n) * sobe_e_some(n, 0.9, 1.1) * 0.06, 0.35)
    poe(x, B.feixe(rng, v)[: n_de(0.6)] * 0.45, 0.75)
    poe(x, B.impacto_energia(rng, v)[: n_de(0.6)] * 0.5, 0.95)
    return reverb(x, 0.6, 0.3)


# =================================================================== Anya
def leitura_mental(rng, v):
    """A telepatia: as ondas (o "uu-uu-uu" ondulante e agudo), o "pop" do balão aparecendo e o "?"
    (o tom que sobe como pergunta), e as estrelinhas girando."""
    x = _z(1.6)
    n = n_de(0.45)
    t = _t(n)
    poe(x, seno(1200 + 300 * np.sin(2 * math.pi * 9 * t), n) * sobe_e_some(n, 0.4, 1.3) * 0.05, 0.0)
    m = n_de(0.08)
    poe(x, seno(varre(500, 900, m, 1.0), m) * env(m, 0.002, 0.07) * 0.15, 0.42)
    k = n_de(0.25)
    poe(x, seno(varre(600, 1100, k, 0.6), k) * env(k, 0.01, 0.2) * 0.07, 0.55)
    for j in range(4):
        poe(x, _brilho(rng, 0.2, 2400 + 300 * j, 0.03, CRISTAL), 0.8 + 0.08 * j)
    return reverb(x, 0.45, 0.22)


def alerta_urgente(rng, v):
    """O alerta: os "!" pulando (os bipes agudos de susto, rápidos) e a bolha-escudo fechando (o "bloop"
    redondo e o brilho)."""
    x = _z(1.5)
    for k in range(4):
        n = n_de(0.07)
        poe(x, seno(1800 + 150 * k, n) * env(n, 0.002, 0.05) * 0.08, 0.02 + 0.06 * k)
    m = n_de(0.3)
    poe(x, seno(varre(250, 600, m, 0.8), m) * env(m, 0.01, 0.25) * 0.2, 0.32)
    poe(x, _brilho(rng, 0.6, 1568, 0.05, CRISTAL), 0.5)
    return reverb(x, 0.45, 0.22)


def plano_secreto(rng, v):
    """O plano secreto: a caneta riscando o plano (os arranhados curtos tracejados) e o carimbo batendo
    (o "TUM" de borracha e madeira) — o tema de espião num toque."""
    x = _z(1.5)
    for k in range(9):
        n = n_de(0.04)
        poe(x, passa(rosa(rng, n), 2500, 8000, 2) * env(n, 0.002, 0.03) * 0.15, 0.02 + 0.045 * k)
    poe(x, baque(n_de(0.3), 140, 80, 0.06, 0.8) * 0.8, 0.5)
    poe(x, passa(rosa(rng, n_de(0.08)), 300, 2000, 2) * env(n_de(0.08), 0.001, 0.05) * 0.5, 0.5)
    m = n_de(0.5)
    tema = np.zeros(m)
    for j, f in enumerate((220.0, 261.63, 220.0, 196.0)):
        k = n_de(0.1)
        poe(tema, seno(f, k) * env(k, 0.005, 0.08) * 0.08, 0.1 * j)
    poe(x, tema, 0.7)
    return reverb(x, 0.45, 0.22)


SONS: dict = {
    "puxar-a-corda": (puxar_a_corda, "Denji: a corda, o motor pegando e a serra"),
    "frenesi-de-sangue": (frenesi_de_sangue, "Denji: a motosserra a toda e os cortes"),
    "lanca-de-sangue": (lanca_de_sangue, "Power: as gotas, a lança e o espirro"),
    "power-preparo": (power_preparo, "Power: o sangue girando e o riso (antes do golpe)"),
    "premio-de-sangue": (premio_de_sangue, "Power: os espinhos de sangue em roda"),
    "olhar-de-comando": (olhar_de_comando, "Makima: o silêncio, o olho e a ordem"),
    "corrente-de-obediencia": (corrente_de_obediencia, "Makima: a guia e a coleira"),
    "controle-total": (controle_total, "Makima: o bang e o esmagamento"),
    "analise-de-mana": (analise_de_mana, "Frieren: o círculo, o feixe e os buffs saindo"),
    "frieren-preparo": (frieren_preparo, "Frieren: os círculos girando (antes do golpe)"),
    "magia-preparada": (magia_preparada, "Frieren: os círculos e os feixes juntos"),
    "leitura-mental": (leitura_mental, "Anya: a telepatia e o balão com ?"),
    "alerta-urgente": (alerta_urgente, "Anya: os ! e a bolha-escudo"),
    "plano-secreto": (plano_secreto, "Anya: o plano riscado e o carimbo"),
}
