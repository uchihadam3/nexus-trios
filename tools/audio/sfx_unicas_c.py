"""Os sons da rodada 2 das Mecânicas únicas (veja tools/vfx/familias_v2/unicas_c.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_ninjas import _trovao
from sfx_rodada08 import _corrente
from sfx_rodada09 import _estalo_de_dedos, _tempo_para
from sfx_rodada11 import _batida_de_coracao
from sfx_rodada15 import _laser
from sfx_rodada16 import _explosao
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _acorde(fs, seg, g=0.04, ataque=0.03, queda=0.5):
    n = n_de(seg)
    return sum(seno(f, n) * (1 - 0.15 * k) for k, f in enumerate(fs)) * env(n, ataque, queda) * g


def portal(rng, v):
    """O portal: o chiado das faíscas girando (o ronco que roda) e o acorde místico que abre."""
    x = _z(1.9)
    n = n_de(1.4)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 9 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.45, 0.0)
    poe(x, graos(rng, n, 120, 0.0, 0.9, 3000, 11000, 0.002) * 0.3, 0.0)
    poe(x, _acorde((220, 330, 440, 554), 1.2, 0.04, 0.2, 0.6), 0.15)
    poe(x, _brilho(rng, 0.7, 1760, 0.04, SINO), 0.35)
    return reverb(x, 0.7, 0.35)


def rastro_flash(rng, v):
    """O Flash: o zunido que passa raspando, os estalos elétricos e o tom do emblema."""
    x = _z(1.5)
    poe(x, _whoosh(rng, 0.35, 600, 7000, 0.4, 1.2, 0.8), 0.0)
    poe(x, _whoosh(rng, 0.3, 900, 8000, 0.4, 1.2, 0.6), 0.18)
    poe(x, graos(rng, n_de(0.6), 50, 0.0, 0.7, 2500, 10000, 0.002) * 0.4, 0.1)
    poe(x, _trovao(rng, 0.4, 0.3), 0.3)
    poe(x, _brilho(rng, 0.6, 1568, 0.05, CRISTAL), 0.32)
    return reverb(x, 0.5, 0.25)


def laco(rng, v):
    """O Laço: a corda zunindo no ar, o aperto (o rangido) e o tom dourado da verdade."""
    x = _z(1.9)
    n = n_de(0.6)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 400, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 6 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.5, 0.0)
    m = n_de(0.3)
    poe(x, passa(rosa(rng, m), 200, 1500, 2) * env(m, 0.01, 0.15) * 0.6 + satura(seno(varre(180, 110, m), m), 2) * env(m, 0.01, 0.2) * 0.1, 0.7)
    poe(x, _acorde((523, 659, 784, 1047), 1.0, 0.045, 0.02, 0.5), 0.75)
    poe(x, _brilho(rng, 0.7, 2093, 0.04, SINO), 0.8)
    return reverb(x, 0.6, 0.3)


def unibeam(rng, v):
    """O Unibeam: o reator carregando (o tom que sobe), o disparo e o feixe rugindo."""
    x = _z(2.0)
    n = n_de(0.75)
    poe(x, (seno(varre(200, 1400, n, 1.6), n) * 0.06 + seno(varre(400, 2800, n, 1.6), n) * 0.02) * sobe_e_some(n, 0.95, 1.0), 0.0)
    k = n_de(1.0)
    poe(x, satura(baque(n_de(0.4), 90, 40, 0.15, 1.0), 2) * 0.6, 0.75)
    poe(x, (passa(rosa(rng, k), 300, 5000, 2) * 0.5 + satura(seno(110, k), 2.0) * 0.12) * env(k, 0.01, 0.5, segura=0.4), 0.75)
    poe(x, _laser(rng, 0.9, 1400, 700, 0.06), 0.75)
    return reverb(x, 0.5, 0.25)


def lider(rng, v):
    """O Capitão: o escudo vibrando (o metal largo) e a fanfarra curta que sobe."""
    x = _z(1.8)
    poe(x, modal(n_de(1.0), 330, rng=rng, **METAL) * env(n_de(1.0), 0.002, 0.5) * 0.14, 0.0)
    for k, f in enumerate((392, 523, 659, 784)):
        poe(x, _acorde((f, f * 1.5), 0.35 if k < 3 else 0.8, 0.05, 0.01, 0.2 if k < 3 else 0.5), 0.45 + 0.12 * k)
    return reverb(x, 0.6, 0.3)


def fator_cura(rng, v):
    """Deadpool: as katanas saindo (o shing duplo), o coração batendo e a carne fechando (o borbulho)."""
    x = _z(1.9)
    for k in range(2):
        m = n_de(0.5)
        poe(x, modal(m, 2600 + 300 * k, rng=rng, **METAL) * env(m, 0.001, 0.25) * 0.07 + passa(rosa(rng, m), 3000, 9000, 2) * env(m, 0.002, 0.08) * 0.3, 0.05 + 0.12 * k)
    for k in range(3):
        poe(x, _batida_de_coracao(rng, 0.7), 0.45 + 0.3 * k)
    poe(x, graos(rng, n_de(0.8), 40, 0.0, 0.9, 300, 1500, 0.01) * 0.3, 0.5)
    poe(x, _brilho(rng, 0.6, 1320, 0.035, CRISTAL), 0.9)
    return reverb(x, 0.4, 0.2)


def joia(rng, v):
    """A Joia: a energia juntando (o sopro que sobe), o cristal ressoando e o encaixe."""
    x = _z(1.8)
    n = n_de(0.55)
    poe(x, passa(rosa(rng, n), 500, 5000, 2) * sobe_e_some(n, 0.9, 1.0) * 0.35, 0.0)
    poe(x, modal(n_de(1.0), 880, rng=rng, **CRISTAL) * env(n_de(1.0), 0.003, 0.6) * 0.08, 0.3)
    m = n_de(0.2)
    poe(x, satura(baque(m, 160, 80, 0.06, 1.0), 2) * 0.5 + modal(m, 1200, rng=rng, **METAL) * env(m, 0.001, 0.1) * 0.06, 0.75)
    poe(x, _acorde((294, 440, 587), 0.9, 0.04, 0.02, 0.5), 0.75)
    return reverb(x, 0.6, 0.3)


def estalo_thanos(rng, v):
    """O Estalo: as seis joias zumbindo, o estalo seco, o silêncio e o vento levando o pó."""
    x = _z(2.4)
    n = n_de(0.5)
    poe(x, sum(seno(f, n) for f in (220, 277, 330, 415, 494, 659)) * sobe_e_some(n, 0.9, 1.0) * 0.02, 0.0)
    poe(x, _estalo_de_dedos(rng, 1.0), 0.55)
    poe(x, satura(baque(n_de(0.6), 60, 25, 0.25, 0.8), 2) * 0.6, 0.56)
    m = n_de(1.5)
    poe(x, passa(rosa(rng, m), 600, 4000, 2) * sobe_e_some(m, 0.3, 1.4) * 0.35, 0.8)
    poe(x, graos(rng, m, 70, 0.0, 0.9, 2000, 7000, 0.004) * 0.25, 0.85)
    return reverb(x, 0.8, 0.4)


def potencial(rng, v):
    """O potencial despertado: o grito de poder subindo, a explosão da aura e os raios estalando."""
    x = _z(1.9)
    n = n_de(0.5)
    poe(x, satura(seno(varre(110, 260, n, 1.0), n), 2.5) * sobe_e_some(n, 0.8, 1.0) * 0.14, 0.0)
    poe(x, _explosao(rng, 0.7, 60), 0.4)
    k = n_de(1.2)
    poe(x, passa(rosa(rng, k), 300, 4000, 2) * env(k, 0.01, 0.6) * 0.35, 0.42)
    poe(x, graos(rng, n_de(1.0), 50, 0.0, 0.9, 3000, 11000, 0.002) * 0.4, 0.45)
    poe(x, _trovao(rng, 0.7, 0.3), 0.55)
    return reverb(x, 0.6, 0.3)


def treino(rng, v):
    """O treino do Piccolo: a capa pesada caindo (o baque fundo que faz a poeira subir) e o ki verde zumbindo."""
    x = _z(2.0)
    poe(x, _whoosh(rng, 0.4, 300, 1500, 0.8, 1.6, 0.4), 0.0)
    poe(x, satura(baque(n_de(0.7), 55, 28, 0.25, 0.9), 2.4) * 0.9, 0.38)
    m = n_de(0.9)
    poe(x, passa(rosa(rng, m), 80, 1200, 2) * env(m, 0.005, 0.4) * 0.5, 0.38)
    k = n_de(1.0)
    poe(x, (seno(165, k) * 0.7 + seno(247, k) * 0.5 + passa(rosa(rng, k), 600, 3000, 2) * 0.3) * sobe_e_some(k, 0.5, 1.4) * 0.12, 0.8)
    return reverb(x, 0.5, 0.3)


def sofrimento(rng, v):
    """Freeza: a Supernova crescendo (o ronco grave que sobe), a risada fria (os tons agudos) e o chicote da cauda."""
    x = _z(2.0)
    n = n_de(1.2)
    poe(x, (satura(seno(varre(55, 110, n, 1.2), n), 2) * 0.12 + passa(rosa(rng, n), 100, 1500, 2) * 0.2) * sobe_e_some(n, 0.8, 1.0), 0.0)
    for k in range(4):
        m = n_de(0.12)
        poe(x, seno(varre(1200 - 80 * k, 900 - 80 * k, m), m) * env(m, 0.005, 0.08) * 0.04, 0.3 + 0.13 * k)
    poe(x, _whoosh(rng, 0.25, 1500, 7000, 0.8, 1.5, 0.6), 0.85)
    poe(x, estalo(rng, n_de(0.05), 2000, 9000, 0.01) * 0.6, 1.08)
    return reverb(x, 0.6, 0.3)


def copia(rng, v):
    """Kakashi: o pergaminho desenrolando (o papel), os traços do pincel e o selo do jutsu."""
    x = _z(1.8)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.3, 1.5) * 0.4, 0.0)
    for k in range(6):
        m = n_de(0.08)
        poe(x, passa(rosa(rng, m), 2500, 8000, 2) * env(m, 0.002, 0.05) * 0.4, 0.35 + 0.07 * k)
    poe(x, satura(baque(n_de(0.25), 180, 90, 0.07, 0.8), 1.6) * 0.5, 0.85)
    poe(x, _acorde((349, 440, 523), 0.7, 0.04, 0.01, 0.4), 0.86)
    return reverb(x, 0.5, 0.25)


def fio(rng, v):
    """Tanjiro: o fio esticando (o tom fino e tenso), o corte de água e o respingo."""
    x = _z(1.8)
    n = n_de(0.6)
    poe(x, (seno(varre(1800, 2400, n), n) * 0.03 + seno(varre(3600, 4800, n), n) * 0.01) * sobe_e_some(n, 0.9, 1.0), 0.0)
    poe(x, _whoosh(rng, 0.3, 1200, 9000, 0.6, 1.4, 0.8), 0.55)
    m = n_de(0.5)
    poe(x, modal(m, 2900, rng=rng, **METAL) * env(m, 0.001, 0.2) * 0.06, 0.7)
    poe(x, passa(rosa(rng, m), 400, 5000, 2) * env(m, 0.005, 0.25) * 0.4 + graos(rng, m, 25, 0.0, 0.6, 1500, 6000, 0.006) * 0.3, 0.72)
    return reverb(x, 0.5, 0.25)


def sangue(rng, v):
    """Nezuko: o sangue pegando fogo (o "vuf" e as chamas rugindo) e as gotas chiando."""
    x = _z(1.8)
    n = n_de(0.9)
    poe(x, satura(passa(rosa(rng, n), 120, 3500, 2), 1.8) * sobe_e_some(n, 0.15, 1.4) * 0.6, 0.0)
    poe(x, graos(rng, n_de(1.0), 70, 0.0, 0.9, 1500, 8000, 0.004) * 0.35, 0.05)
    poe(x, satura(baque(n_de(0.3), 120, 60, 0.08, 0.8), 1.8) * 0.4, 0.0)
    for k in range(4):
        m = n_de(0.1)
        poe(x, passa(rosa(rng, m), 3000, 9000, 2) * env(m, 0.002, 0.07) * 0.3, 0.35 + 0.1 * k)
    return reverb(x, 0.5, 0.25)


def zzz(rng, v):
    """Zenitsu: o ronco (o zumbido grave em ondas), o silêncio e o trovão da Primeira postura."""
    x = _z(2.0)
    n = n_de(0.9)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 80, 600, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 1.6 * t) ** 2) * env(n, 0.05, 0.5, segura=0.4) * 0.35, 0.0)
    poe(x, _whoosh(rng, 0.2, 2000, 9000, 0.6, 1.2, 0.7), 0.75)
    poe(x, _trovao(rng, 1.0, 0.9), 0.85)
    poe(x, graos(rng, n_de(0.7), 60, 0.0, 0.6, 3000, 11000, 0.002) * 0.45, 0.85)
    return reverb(x, 0.6, 0.3)


def juntas(rng, v):
    """Inosuke: as correntes estalando, os ossos saindo do lugar (os estalos secos) e o grito de javali."""
    x = _z(1.8)
    poe(x, _corrente(rng, 0.5, 8, 0.4), 0.0)
    poe(x, satura(baque(n_de(0.2), 300, 150, 0.04, 1.0), 2) * 0.4, 0.42)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.04), 800, 4000, 0.008) * 0.8, 0.5 + 0.06 * k + 0.02 * (k % 2))
    m = n_de(0.5)
    poe(x, satura(seno(varre(260, 160, m), m) * 0.6 + passa(rosa(rng, m), 300, 2500, 2) * 0.6, 2.5) * env(m, 0.02, 0.3) * 0.18, 0.9)
    return reverb(x, 0.4, 0.2)


def bracos(rng, v):
    """Muzan: os braços saindo (os chicotes que estalam em sequência) e o ronco de carne."""
    x = _z(1.9)
    n = n_de(1.2)
    poe(x, passa(rosa(rng, n), 80, 700, 2) * sobe_e_some(n, 0.4, 1.2) * 0.4, 0.0)
    for k in range(7):
        poe(x, _whoosh(rng, 0.15, 800, 5000, 0.8, 1.4, 0.35), 0.1 + 0.07 * k)
        poe(x, estalo(rng, n_de(0.04), 2000, 9000, 0.008) * 0.5, 0.24 + 0.07 * k)
    poe(x, graos(rng, n_de(0.8), 30, 0.0, 0.8, 200, 1200, 0.015) * 0.3, 0.3)
    return reverb(x, 0.5, 0.25)


def black_flash(rng, v):
    """O Black Flash: o soco que distorce (o estalo enorme, o grave rasgado) e o espaço rachando."""
    x = _z(1.9)
    n = n_de(0.3)
    poe(x, seno(varre(300, 1200, n, 2), n) * sobe_e_some(n, 0.95, 1.0) * 0.05, 0.0)
    poe(x, satura(baque(n_de(0.8), 70, 25, 0.25, 1.0), 3.5) * 0.9, 0.3)
    poe(x, satura(passa(rosa(rng, n_de(0.6)), 200, 7000, 2) * env(n_de(0.6), 0.001, 0.2), 3.0) * 0.7, 0.3)
    poe(x, _trovao(rng, 0.8, 0.5), 0.33)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.04), 1500, 8000, 0.01) * 0.5, 0.4 + 0.05 * k)
    return reverb(x, 0.6, 0.3)


def mahoraga(rng, v):
    """Mahoraga: a roda girando (a catraca pesada), o clique de um dente e o sino da adaptação."""
    x = _z(1.9)
    for k in range(6):
        poe(x, satura(baque(n_de(0.08), 220, 160, 0.02, 1.0), 1.5) * 0.25, 0.05 + 0.07 * k)
        poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.005) * 0.3, 0.05 + 0.07 * k)
    poe(x, satura(baque(n_de(0.3), 120, 70, 0.08, 1.0), 2) * 0.7, 0.55)
    m = n_de(1.3)
    poe(x, modal(m, 196, rng=rng, **SINO) * env(m, 0.002, 0.8) * 0.18, 0.56)
    return reverb(x, 0.7, 0.35)


def boneca(rng, v):
    """Nobara: o prego na boneca e a martelada (o metal batendo), e a ressonância que ecoa."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 500, 3000, 0.8, 1.5, 0.4), 0.2)
    m = n_de(0.8)
    poe(x, modal(m, 1400, rng=rng, **METAL) * env(m, 0.0005, 0.3) * 0.12, 0.45)
    poe(x, satura(baque(n_de(0.25), 200, 100, 0.05, 1.0), 2) * 0.5, 0.45)
    k = n_de(1.2)
    t = _t(k)
    poe(x, seno(220, k) * (0.6 + 0.4 * np.sin(2 * math.pi * 5 * t)) * env(k, 0.01, 0.6) * 0.06 + seno(330, k) * env(k, 0.01, 0.5) * 0.03, 0.47)
    return reverb(x, 0.7, 0.35)


def santuario(rng, v):
    """O Santuário: o coro grave do domínio abrindo e a chuva de cortes."""
    x = _z(2.2)
    n = n_de(1.4)
    poe(x, (seno(73, n) + seno(110, n) * 0.6 + seno(87, n) * 0.5) * sobe_e_some(n, 0.3, 1.2) * 0.07, 0.0)
    poe(x, passa(rosa(rng, n), 60, 500, 2) * sobe_e_some(n, 0.3, 1.2) * 0.3, 0.0)
    q = np.random.default_rng(3)
    for k in range(14):
        m = n_de(0.12)
        poe(x, passa(rosa(rng, m), 2500, 11000, 2) * env(m, 0.001, 0.06) * 0.35 + modal(m, q.uniform(2400, 3600), rng=rng, **METAL) * env(m, 0.001, 0.05) * 0.03,
            0.3 + 0.05 * k + q.uniform(0, 0.03))
    return reverb(x, 0.6, 0.3)


SONS: dict = {
    "mu-portal": (portal, "Doutor Estranho: o portal de faíscas"),
    "mu-rastro-flash": (rastro_flash, "Flash: o rastro de velocidade"),
    "mu-laco": (laco, "Mulher-Maravilha: o Laço da verdade"),
    "mu-unibeam": (unibeam, "Homem de Ferro: o Unibeam"),
    "mu-lider": (lider, "Capitão América: o escudo e a fanfarra"),
    "mu-fator-cura": (fator_cura, "Deadpool: as katanas e a cura"),
    "mu-joia": (joia, "Thanos: a Joia do Infinito"),
    "mu-estalo": (estalo_thanos, "Thanos: o estalo"),
    "mu-potencial": (potencial, "Gohan: o potencial despertado"),
    "mu-treino": (treino, "Piccolo: a capa pesada e o ki"),
    "mu-sofrimento": (sofrimento, "Freeza: a Supernova e a cauda"),
    "mu-copia": (copia, "Kakashi: o pergaminho e o selo"),
    "mu-fio": (fio, "Tanjiro: o fio e o corte d'água"),
    "mu-sangue": (sangue, "Nezuko: o sangue pegando fogo"),
    "mu-zzz": (zzz, "Zenitsu: o ronco e o trovão"),
    "mu-juntas": (juntas, "Inosuke: as juntas soltando"),
    "mu-bracos": (bracos, "Muzan: os braços-chicote"),
    "mu-black-flash": (black_flash, "Yuji: o Black Flash"),
    "mu-mahoraga": (mahoraga, "Megumi: a roda de Mahoraga"),
    "mu-boneca": (boneca, "Nobara: a boneca e o prego"),
    "mu-santuario": (santuario, "Sukuna: o Santuário malevolente"),
}
