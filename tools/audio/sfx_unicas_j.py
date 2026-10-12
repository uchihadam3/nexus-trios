"""Os sons da rodada 9 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_j.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_f import _quadrada
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, VIDRO, env, estalo, graos, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def sem_folego(rng, v):
    """Cheetara: a corrida (o zunido), a freada e o fôlego acabando (a respiração ofegante)."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.4, 600, 7000, 0.4, 1.3, 0.6), 0.0)
    poe(x, passa(rosa(rng, n_de(0.25)), 1500, 6000, 2) * env(n_de(0.25), 0.005, 0.2) * 0.4, 0.4)
    for k in range(4):
        n = n_de(0.22)
        poe(x, passa(rosa(rng, n), 600 + 300 * (k % 2), 3000, 2) * sobe_e_some(n, 0.3, 1.3) * 0.3, 0.7 + 0.25 * k)
    return reverb(x, 0.3, 0.15)


def mais_poder(rng, v):
    """Mumm-Ra: "Espíritos do mal!" — o coro grave e as faixas girando no vento."""
    x = _z(2.2)
    n = n_de(1.8)
    t = _t(n)
    poe(x, (seno(73, n) + seno(87, n) * 0.7 + seno(110, n) * 0.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.06, 0.0)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.3, 0.0)
    poe(x, _sino(rng, 147, 1.2, 0.1, SINO), 0.8)
    return reverb(x, 0.8, 0.4)


def soneca(rng, v):
    """Homer: o "Mmm, rosquinha…" (o tom gostoso) e o ronco."""
    x = _z(2.0)
    n = n_de(0.6)
    poe(x, satura(seno(varre(180, 140, n), n), 1.5) * env(n, 0.05, 0.4) * 0.06, 0.0)
    for k in range(2):
        m = n_de(0.5)
        t = _t(m)
        poe(x, passa(rosa(rng, m), 60, 500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 30 * t)) * sobe_e_some(m, 0.6, 1.2) * 0.5, 0.75 + 0.6 * k)
    return reverb(x, 0.4, 0.2)


def nao_fui(rng, v):
    """Bart: o skate rolando e o "Eu não fui!" (o tom que sobe e desce)."""
    x = _z(1.9)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 18 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.35, 0.0)
    poe(x, _baque(300, 150, 0.08, 0.3), 0.45)
    poe(x, _piu(600, 900, 0.15, 0.05), 1.0)
    poe(x, _piu(900, 500, 0.2, 0.05), 1.15)
    return reverb(x, 0.4, 0.2)


def galo(rng, v):
    """Peter: a briga com o galo (pancadas, penas e o cocoricó)."""
    x = _z(2.0)
    q = np.random.default_rng(5)
    for k in range(8):
        poe(x, _baque(q.uniform(100, 200), 60, 0.15, 0.4, 2.0), 0.1 * k + q.uniform(0, 0.04))
    poe(x, _sopro(rng, 1.0, 2000, 7000, 0.15, 0.3), 0.2)
    n = n_de(0.5)
    t = _t(n)
    poe(x, satura(seno(varre(700, 1100, n, 0.5) * (1 + 0.04 * np.sin(2 * math.pi * 30 * t)), n), 2) * env(n, 0.02, 0.35) * 0.04, 1.0)
    return reverb(x, 0.4, 0.2)


def encolher(rng, v):
    """Stewie: o raio de encolher (o "uiuiui" que desce) e o alvo diminuindo."""
    x = _z(1.9)
    n = n_de(0.9)
    t = _t(n)
    poe(x, seno(varre(1200, 300, n) * (1 + 0.1 * np.sin(2 * math.pi * 12 * t)), n) * env(n, 0.01, 0.6) * 0.06, 0.0)
    poe(x, _piu(900, 2400, 0.3, 0.04), 1.0)
    return reverb(x, 0.5, 0.25)


def chantagem(rng, v):
    """Cartman: o envelope abrindo (o papel), a risadinha e as moedas caindo."""
    x = _z(1.9)
    poe(x, passa(rosa(rng, n_de(0.2)), 2000, 7000, 2) * env(n_de(0.2), 0.005, 0.12) * 0.4, 0.3)
    for k in range(3):
        n = n_de(0.1)
        poe(x, satura(seno(varre(330, 280, n), n), 1.6) * env(n, 0.01, 0.07) * 0.05, 0.55 + 0.12 * k)
    for k in range(8):
        poe(x, _sino(rng, 2400 + 300 * (k % 3), 0.25, 0.035, METAL), 0.6 + 0.07 * k)
    return reverb(x, 0.4, 0.2)


def acordo(rng, v):
    """Bill Cipher: o olho acendendo (o tom estranho ao contrário) e o aperto de mão em fogo azul."""
    x = _z(2.1)
    n = n_de(1.0)
    poe(x, seno(varre(200, 800, n, 3.0), n) * sobe_e_some(n, 0.95, 1.0) * 0.06, 0.0)
    poe(x, _sino(rng, 1661, 0.8, 0.05, VIDRO), 0.95)
    m = n_de(1.0)
    poe(x, satura(passa(rosa(rng, m), 300, 5000, 2), 1.6) * sobe_e_some(m, 0.2, 1.3) * 0.4, 1.0)
    poe(x, _baque(150, 70, 0.2, 0.4), 1.0)
    return reverb(x, 0.7, 0.35)


def formula(rng, v):
    """Plankton: o "A fórmula é minha!" (a risada fininha) e o frasco voando."""
    x = _z(1.9)
    for k in range(5):
        n = n_de(0.08)
        poe(x, satura(seno(varre(900, 760, n), n), 1.6) * env(n, 0.005, 0.06) * 0.04, 0.05 + 0.09 * k)
    poe(x, _whoosh(rng, 0.4, 800, 4000, 0.6, 1.3, 0.35), 0.5)
    poe(x, _sino(rng, 1800, 0.4, 0.05, VIDRO), 0.55)
    return reverb(x, 0.4, 0.2)


def robo_quebrou(rng, v):
    """Macaco Louco: o robô estourando (os metais voando e as molas)."""
    x = _z(2.0)
    poe(x, _explosao(rng, 0.6, 80), 0.0)
    for k in range(10):
        poe(x, _sino(rng, 500 + 180 * k, 0.3, 0.04, METAL), 0.1 + 0.06 * k)
    for k in range(3):
        n = n_de(0.3)
        t = _t(n)
        poe(x, seno(300 * (1 + 0.5 * np.sin(2 * math.pi * 25 * t) * np.exp(-t * 8)), n) * env(n, 0.005, 0.25) * 0.05, 0.3 + 0.2 * k)
    return reverb(x, 0.5, 0.25)


def cinco_aneis(rng, v):
    """Capitão Planeta: "Terra! Fogo! Vento! Água! Coração!" — os cinco toques e o planeta acendendo."""
    x = _z(2.2)
    for k, f in enumerate((262, 330, 392, 494, 587)):
        poe(x, _sino(rng, f * 2, 0.5, 0.05, SINO), 0.12 * k)
    poe(x, _acorde((262, 330, 392, 523, 659), 1.4, 0.06, 0.05, 0.8), 0.75)
    poe(x, _brilho(rng, 0.8, 2093, 0.04, CRISTAL), 0.8)
    return reverb(x, 0.7, 0.35)


def lamento(rng, v):
    """Danny Phantom: o Lamento fantasma (o grito longo que vibra e ecoa)."""
    x = _z(2.1)
    n = n_de(1.4)
    t = _t(n)
    grito = seno(500 * (1 + 0.08 * np.sin(2 * math.pi * 7 * t)), n) + seno(750 * (1 + 0.08 * np.sin(2 * math.pi * 7 * t)), n) * 0.5
    poe(x, satura(grito, 2) * env(n, 0.05, 0.9, segura=0.3) * 0.05, 0.0)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * env(n, 0.05, 0.9) * 0.25, 0.0)
    return reverb(x, 0.9, 0.45)


def aaaah(rng, v):
    """Coragem: o grito desesperado (agudo e trêmulo)."""
    x = _z(1.9)
    n = n_de(1.1)
    t = _t(n)
    f = 900 * (1 + 0.12 * np.sin(2 * math.pi * 11 * t)) * (1 + 0.2 * t)
    poe(x, satura(seno(f, n) + seno(f * 1.5, n) * 0.4, 2.5) * env(n, 0.02, 0.8, segura=0.4) * 0.04, 0.0)
    poe(x, passa(rosa(rng, n), 1000, 5000, 2) * env(n, 0.02, 0.6) * 0.15, 0.0)
    return reverb(x, 0.5, 0.25)


def coracao_gelo(rng, v):
    """Senhor Frio: o raio congelante (o chiado frio) e o coração de gelo estalando."""
    x = _z(2.0)
    n = n_de(0.6)
    poe(x, (passa(rosa(rng, n), 2500, 9000, 2) * 0.3 + seno(varre(2000, 1500, n), n) * 0.03) * env(n, 0.01, 0.4), 0.0)
    for k in range(8):
        poe(x, estalo(rng, n_de(0.03), 2500, 9000, 0.005) * 0.4, 0.5 + 0.05 * k)
    poe(x, _sino(rng, 1320, 1.0, 0.07, VIDRO), 0.6)
    m = n_de(0.8)
    poe(x, (seno(55, m) * 0.5) * env(m, 0.02, 0.5) * 0.12, 0.6)
    return reverb(x, 0.7, 0.35)


def plantas(rng, v):
    """Hera Venenosa: as vinhas crescendo (o rangido verde) e os esporos soltos."""
    x = _z(2.0)
    for k in range(5):
        n = n_de(0.4)
        poe(x, satura(seno(varre(120 + 30 * k, 260 + 30 * k, n), n), 1.8) * env(n, 0.05, 0.3) * 0.04, 0.05 + 0.1 * k)
        poe(x, passa(rosa(rng, n), 300, 2500, 2) * env(n, 0.05, 0.3) * 0.2, 0.05 + 0.1 * k)
    poe(x, graos(rng, n_de(0.9), 60, 0.0, 0.9, 2000, 7000, 0.003) * 0.25, 0.7)
    poe(x, _sopro(rng, 0.8, 1500, 6000, 0.15, 0.3), 0.7)
    return reverb(x, 0.5, 0.25)


def pele_gelo(rng, v):
    """Homem de Gelo: o gelo cobrindo o corpo (os estalos de cristal em sequência)."""
    x = _z(1.9)
    for k in range(14):
        poe(x, _sino(rng, 1800 + 120 * (k % 7), 0.25, 0.03, VIDRO), 0.03 * k)
        poe(x, estalo(rng, n_de(0.03), 3000, 9000, 0.004) * 0.3, 0.03 * k)
    poe(x, _sopro(rng, 1.0, 2500, 8000, 0.15, 0.3), 0.3)
    return reverb(x, 0.6, 0.3)


def fantasma(rng, v):
    """Gengar: a bola sombria crescendo (o zumbido escuro) e a risada fantasma."""
    x = _z(2.0)
    n = n_de(0.9)
    poe(x, (seno(varre(80, 140, n), n) * 0.1 + passa(rosa(rng, n), 100, 1000, 2) * 0.3) * sobe_e_some(n, 0.7, 1.0), 0.0)
    for k in range(4):
        m = n_de(0.13)
        poe(x, satura(seno(varre(440 - 20 * k, 360 - 20 * k, m), m), 1.4) * env(m, 0.01, 0.09) * 0.04, 0.85 + 0.14 * k)
    return reverb(x, 0.8, 0.4)


def kikoho(rng, v):
    """Tenshinhan: o triângulo das mãos (o tom que concentra), "KIKOHO!" e o esmagamento."""
    x = _z(2.0)
    n = n_de(0.7)
    poe(x, seno(varre(300, 900, n, 1.3), n) * sobe_e_some(n, 0.9, 1.0) * 0.05, 0.0)
    poe(x, _baque(55, 22, 0.8, 1.0, 3.0), 0.7)
    m = n_de(1.0)
    poe(x, satura(passa(rosa(rng, m), 40, 2000, 2) * env(m, 0.002, 0.5), 2.2) * 0.7, 0.7)
    return reverb(x, 0.7, 0.35)


def katsu(rng, v):
    """Deidara: os pássaros de argila batendo as asas, "Katsu!" e a explosão de arte."""
    x = _z(2.2)
    for k in range(6):
        poe(x, passa(rosa(rng, n_de(0.06)), 800, 4000, 2) * env(n_de(0.06), 0.003, 0.04) * 0.3, 0.05 + 0.08 * k)
    poe(x, estalo(rng, n_de(0.04), 1500, 5000, 0.006) * 0.8, 0.9)
    poe(x, _explosao(rng, 1.0, 50), 0.98)
    return reverb(x, 0.6, 0.3)


def sumiu(rng, v):
    """Violeta: o campo de força ligando (o zumbido roxo) e ela sumindo (o brilho que desaparece)."""
    x = _z(1.9)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(varre(200, 400, n), n) * 0.06 + seno(varre(300, 600, n), n) * 0.03) * (0.7 + 0.3 * np.sin(2 * math.pi * 20 * t)) * sobe_e_some(n, 0.4, 1.2), 0.0)
    m = n_de(0.7)
    poe(x, seno(varre(1600, 3000, m), m) * env(m, 0.02, 0.5) * 0.03, 0.6)
    return reverb(x, 0.6, 0.3)


def rejeitar(rng, v):
    """Orihime: as Seis Flores voando (os sininhos) e o escudo de luz se fechando."""
    x = _z(2.0)
    for k, f in enumerate((1568, 1760, 1976, 2349, 2637, 3136)):
        poe(x, _sino(rng, f, 0.4, 0.03, CRISTAL), 0.06 * k)
    poe(x, _acorde((440, 554, 659, 880), 1.1, 0.045, 0.1, 0.6), 0.5)
    return reverb(x, 0.7, 0.35)


def ultima_oracao(rng, v):
    """Aerith: a matéria branca descendo (o sino calmo), a oração (o coro) e as pétalas."""
    x = _z(2.4)
    poe(x, _sino(rng, 784, 1.4, 0.08, SINO), 0.0)
    poe(x, _acorde((392, 494, 587, 784, 988), 1.8, 0.05, 0.3, 1.0), 0.4)
    poe(x, _sopro(rng, 1.4, 2500, 8000, 0.1, 0.4), 0.6)
    return reverb(x, 0.9, 0.45)


def dobra_sangue(rng, v):
    """Katara: a dobra de sangue (o tom tenso e torcido) e as gotas girando."""
    x = _z(2.0)
    n = n_de(1.4)
    t = _t(n)
    poe(x, (seno(220 * (1 + 0.03 * np.sin(2 * math.pi * 4 * t)), n) + seno(233, n) * 0.8) * sobe_e_some(n, 0.4, 1.2) * 0.045, 0.0)
    poe(x, passa(rosa(rng, n), 150, 1200, 2) * sobe_e_some(n, 0.5, 1.2) * 0.25, 0.0)
    for k in range(3):
        poe(x, estalo(rng, n_de(0.04), 600, 3000, 0.01) * 0.4, 0.5 + 0.25 * k)
    return reverb(x, 0.6, 0.3)


def analise(rng, v):
    """Sailor Mercury: o visor ligando (o bipe) e a análise (os dados correndo)."""
    x = _z(1.9)
    poe(x, _piu(800, 1600, 0.12, 0.05), 0.0)
    q = np.random.default_rng(9)
    for k in range(14):
        m = n_de(0.035)
        poe(x, seno(q.choice([1200, 1600, 2000, 2400]), m) * env(m, 0.002, 0.025) * 0.035, 0.3 + 0.05 * k)
    poe(x, _sino(rng, 1760, 0.6, 0.05, VIDRO), 1.05)
    return reverb(x, 0.5, 0.25)


def semente(rng, v):
    """Kurama: a rosa, o chicote de espinhos estalando e a semente brotando."""
    x = _z(1.9)
    poe(x, _sino(rng, 1320, 0.5, 0.04, CRISTAL), 0.0)
    poe(x, _whoosh(rng, 0.3, 1000, 7000, 0.5, 1.4, 0.5), 0.3)
    poe(x, estalo(rng, n_de(0.05), 2000, 9000, 0.008), 0.6)
    n = n_de(0.5)
    poe(x, satura(seno(varre(150, 400, n), n), 1.6) * env(n, 0.05, 0.3) * 0.05, 0.85)
    return reverb(x, 0.5, 0.25)


def parry(rng, v):
    """Ken: o parry (o "tchiing" azul) e o Shoryuken em chamas."""
    x = _z(1.9)
    n = n_de(0.4)
    poe(x, (seno(1760, n) + seno(2640, n) * 0.5) * env(n, 0.002, 0.25) * 0.05, 0.0)
    poe(x, passa(rosa(rng, n_de(0.1)), 3000, 9000, 2) * env(n_de(0.1), 0.001, 0.05) * 0.5, 0.0)
    poe(x, _baque(140, 60, 0.4, 0.8, 2.4), 0.55)
    m = n_de(0.8)
    poe(x, satura(passa(rosa(rng, m), 150, 4000, 2), 1.8) * sobe_e_some(m, 0.2, 1.3) * 0.5, 0.55)
    return reverb(x, 0.5, 0.25)


SONS: dict = {
    "mu-sem-folego": (sem_folego, "Cheetara: sem fôlego"),
    "mu-mais-poder": (mais_poder, "Mumm-Ra: mais poder"),
    "mu-soneca": (soneca, "Homer: a soneca"),
    "mu-nao-fui": (nao_fui, "Bart: eu não fui"),
    "mu-galo": (galo, "Peter: a briga com o galo"),
    "mu-encolher": (encolher, "Stewie: o raio de encolher"),
    "mu-chantagem": (chantagem, "Cartman: a chantagem"),
    "mu-acordo": (acordo, "Bill Cipher: o acordo"),
    "mu-formula": (formula, "Plankton: a fórmula"),
    "mu-robo-quebrou": (robo_quebrou, "Macaco Louco: o robô quebrou"),
    "mu-cinco-aneis": (cinco_aneis, "Capitão Planeta: os cinco anéis"),
    "mu-lamento": (lamento, "Danny Phantom: o Lamento fantasma"),
    "mu-aaaah": (aaaah, "Coragem: o grito"),
    "mu-coracao-gelo": (coracao_gelo, "Senhor Frio: o coração de gelo"),
    "mu-plantas": (plantas, "Hera Venenosa: as plantas"),
    "mu-pele-gelo": (pele_gelo, "Homem de Gelo: a pele de gelo"),
    "mu-fantasma": (fantasma, "Gengar: o fantasma"),
    "mu-kikoho": (kikoho, "Tenshinhan: o Kikoho"),
    "mu-katsu": (katsu, "Deidara: Katsu!"),
    "mu-sumiu": (sumiu, "Violeta: sumiu"),
    "mu-rejeitar": (rejeitar, "Orihime: as Seis Flores"),
    "mu-ultima-oracao": (ultima_oracao, "Aerith: a Última oração"),
    "mu-dobra-sangue": (dobra_sangue, "Katara: a dobra de sangue"),
    "mu-analise": (analise, "Sailor Mercury: a análise"),
    "mu-semente": (semente, "Kurama: a semente"),
    "mu-parry": (parry, "Ken: o parry"),
}
