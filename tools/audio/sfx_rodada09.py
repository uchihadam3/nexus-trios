"""Os sons da rodada 9: Roy, Griffith, Jotaro, Dio e Giorno (veja tools/vfx/familias_v2/rodada09.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _fogo_vuf(rng, seg=0.5, g=0.5):
    """O "vuuf" de fogo acendendo: o ruído grave que cresce rápido e crepita."""
    n = n_de(seg)
    x = passa(rosa(rng, n), 80, 2500, 2) * sobe_e_some(n, 0.2, 1.5) * 0.7
    x += graos(rng, n, 14, 0.05, seg * 0.9, 1500, 6000, 0.004, 0.6) * 0.3
    return x * g


def _estalo_de_dedos(rng, g=0.6):
    n = n_de(0.1)
    return (estalo(rng, n, 1200, 5000, 0.01) * 1.0 + passa(rosa(rng, n), 800, 4000, 2) * env(n, 0.001, 0.03) * 0.5) * g


def _lamina(rng, seg=0.3, f0=2600, g=0.6):
    n = n_de(seg)
    x = passa(rosa(rng, n), 2000, 11000, 2) * sobe_e_some(n, 0.2, 1.6) * 0.6
    x += modal(n, f0, rng=rng, **METAL) * env(n, 0.001, seg * 0.7) * 0.12
    return x * g


def _soco(rng, g=0.5):
    n = n_de(0.25)
    return (baque(n, 100, 50, 0.08, 0.7) * 0.8 + passa(rosa(rng, n), 300, 3000, 2) * env(n, 0.001, 0.04) * 0.5) * g


def _tempo_para(rng, g=0.4):
    """O tempo parando: o som de tudo sendo sugado (o "fwoom" ao contrário) e o silêncio grave."""
    n = n_de(0.7)
    t = _t(n)
    x = passa(rosa(rng, n), 100, 4000, 2) * (t / t[-1]) ** 2.5 * 0.6
    x += seno(varre(800, 60, n, 0.6), n) * sobe_e_some(n, 0.8, 1.2) * 0.15
    return x * g


# =================================================================== Roy
def chuva_de_fogo(rng, v):
    """A Chuva de fogo: o estalo dos dedos, as bolas de fogo assobiando ao cair e as três explosões de
    labareda no chão, uma depois da outra."""
    x = _z(1.8)
    poe(x, _estalo_de_dedos(rng, 0.7), 0.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.28, 1800, 500, 0.8, 1.4, 0.35), 0.03 + 0.12 * k)
        poe(x, _fogo_vuf(rng, 0.5, 0.6), 0.3 + 0.12 * k)
        poe(x, baque(n_de(0.3), 80, 40, 0.12, 0.5) * 0.4, 0.3 + 0.12 * k)
    return reverb(x, 0.5, 0.25)


def ignicao_preparo(rng, v):
    """O Preparo do Campo incendiado: a luva roçando (o atrito do tecido) e o chiado do ar esquentando."""
    x = _z(1.2)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * env(n, 0.01, 0.25) * 0.2, 0.0)
    m = n_de(1.0)
    poe(x, passa(rosa(rng, m), 3000, 9000, 2) * sobe_e_some(m, 0.8, 1.1) * 0.12 + graos(rng, m, 10, 0.1, 0.9, 2000, 6000, 0.004, 0.6) * 0.1, 0.1)
    return reverb(x, 0.4, 0.2)


def campo_incendiado(rng, v):
    """O Campo incendiado: o estalo, o fogo correndo pelo chão (o "fsssh" que dá a volta) e a detonação
    da coluna de fogo (o estrondo grave e o rugido)."""
    x = _z(2.0)
    poe(x, _estalo_de_dedos(rng, 0.8), 0.0)
    n = n_de(0.6)
    t = _t(n)
    corre = passa(rosa(rng, n), 400, 5000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.6, 1.2) * 0.45
    poe(x, corre, 0.05)
    poe(x, B.explosao(rng, v)[: n_de(1.0)] * 0.8, 0.65)
    poe(x, _fogo_vuf(rng, 0.9, 0.6), 0.65)
    return reverb(x, 0.55, 0.3)


# =================================================================== Griffith
def visao_de_falcao(rng, v):
    """A Visão de falcão: o grito agudo do falcão (o "kriii" descendo), o mergulho no ar e o "tlin" da mira
    fechando."""
    x = _z(1.6)
    n = n_de(0.5)
    t = _t(n)
    grito = seno(varre(2600, 1700, n, 0.7) * (1 + 0.015 * np.sin(2 * math.pi * 35 * t)), n) * sobe_e_some(n, 0.2, 1.3) * 0.12
    grito += passa(rosa(rng, n), 2500, 6000, 2) * sobe_e_some(n, 0.2, 1.3) * 0.05
    poe(x, grito, 0.0)
    poe(x, _whoosh(rng, 0.4, 600, 2800, 0.85, 1.6, 0.4), 0.15)
    poe(x, _brilho(rng, 0.5, 2400, 0.08, CRISTAL), 0.55)
    return reverb(x, 0.5, 0.25)


def comando_da_banda(rng, v):
    """O Comando da Banda: a bandeira estalando ao vento (o pano batendo), a corneta curta do Bando e o
    brado dos soldados (o coro grave)."""
    x = _z(1.9)
    n = n_de(0.6)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 2500, 2) * (0.4 + 0.6 * np.abs(np.sin(2 * math.pi * 6 * t))) * sobe_e_some(n, 0.3, 1.3) * 0.4, 0.0)
    m = n_de(0.7)
    corneta = sum(seno(f, m) * a for f, a in ((392, 1), (784, 0.5), (1176, 0.3), (1568, 0.15)))
    poe(x, satura(corneta, 1.5) * env(m, 0.03, 0.5, segura=0.2) * 0.07, 0.3)
    k = n_de(0.8)
    coro = sum(passa(rosa(rng, k), f * 0.85, f * 1.15, 2) for f in (500, 900, 2400)) * sobe_e_some(k, 0.3, 1.3) * 0.25
    poe(x, coro, 0.6)
    return reverb(x, 0.6, 0.3)


def eclipse_preparo(rng, v):
    """O Preparo do Destino: o zumbido grave do eclipse crescendo e o vento escuro."""
    x = _z(1.3)
    n = n_de(1.2)
    t = _t(n)
    poe(x, (seno(55, n) + seno(58, n) * 0.8) * sobe_e_some(n, 0.8, 1.1) * 0.2, 0.0)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 1.5 * t)) * sobe_e_some(n, 0.8, 1.1) * 0.25, 0.0)
    return reverb(x, 0.65, 0.35)


def destino_ascendente(rng, v):
    """O Eclipse: o sino grave do sacrifício, as asas escuras se abrindo (o "vuump" enorme) e a onda escura
    passando com o coro sinistro."""
    x = _z(2.2)
    poe(x, modal(n_de(1.5), 110, rng=rng, **SINO) * env(n_de(1.5), 0.005, 1.2) * 0.25, 0.0)
    poe(x, _whoosh(rng, 0.6, 120, 500, 0.6, 1.4, 0.7), 0.4)
    poe(x, baque(n_de(0.8), 45, 25, 0.4, 0.3) * 0.7, 0.9)
    n = n_de(1.0)
    coro = sum(passa(rosa(rng, n), f * 0.9, f * 1.1, 2) for f in (300, 700, 2000)) * sobe_e_some(n, 0.3, 1.3) * 0.2
    poe(x, coro, 0.9)
    return reverb(x, 0.7, 0.4)


# =================================================================== Jotaro
def precisao_absoluta(rng, v):
    """A Precisão: o "fwip" agudíssimo do dedo estelar, o tilintar das estrelinhas e o impacto seco e
    exato."""
    x = _z(1.3)
    poe(x, _whoosh(rng, 0.15, 3000, 7000, 0.7, 1.3, 0.45), 0.1)
    for k in range(4):
        poe(x, _brilho(rng, 0.2, 2600 + 300 * k, 0.04, CRISTAL), 0.15 + 0.03 * k)
    poe(x, _soco(rng, 0.9), 0.3)
    poe(x, estalo(rng, n_de(0.02), 2000, 8000) * 0.5, 0.3)
    return reverb(x, 0.45, 0.22)


def star_preparo(rng, v):
    """O Preparo do The World: o zumbido do Star Platinum e as estrelas brilhando em volta."""
    x = _z(1.3)
    n = n_de(1.2)
    poe(x, satura(seno(146, n) + seno(219, n) * 0.6, 1.5) * sobe_e_some(n, 0.8, 1.1) * 0.08, 0.0)
    for k in range(5):
        poe(x, _brilho(rng, 0.3, 1800 + 400 * k, 0.03, CRISTAL), 0.1 + 0.2 * k)
    return reverb(x, 0.55, 0.3)


def the_world_jotaro(rng, v):
    """O tempo para: o som sugado e o silêncio grave (com o tique de relógio parado), e quando o tempo
    volta, os golpes todos de uma vez (a rajada "ora-ora")."""
    x = _z(2.0)
    poe(x, _tempo_para(rng, 0.6), 0.0)
    for k in range(3):
        n = n_de(0.04)
        poe(x, seno(1800, n) * env(n, 0.001, 0.03) * 0.06, 0.75 + 0.18 * k)
    for k in range(9):
        poe(x, _soco(rng, 0.45 + 0.03 * k), 1.25 + 0.045 * k)
    return reverb(x, 0.5, 0.25)


# =================================================================== Dio
def facas_do_dio(rng, v):
    """As facas: o tempo parado (o zumbido baixo), as facas aparecendo uma a uma ("tlin" de aço), e de
    repente todas voando juntas (o "swwish" múltiplo) e cravando."""
    x = _z(1.7)
    n = n_de(0.6)
    poe(x, seno(70, n) * sobe_e_some(n, 0.5, 1.2) * 0.1, 0.0)
    for k in range(8):
        poe(x, modal(n_de(0.2), 3200 + 150 * k, rng=rng, **METAL) * env(n_de(0.2), 0.001, 0.08) * 0.06, 0.02 + 0.045 * k)
    for k in range(5):
        poe(x, _whoosh(rng, 0.2, 2500, 5500, 0.8, 1.3, 0.2), 0.75 + 0.012 * k)
    for k in range(6):
        poe(x, _soco(rng, 0.25), 0.95 + 0.02 * k)
        poe(x, modal(n_de(0.2), 2000 + 100 * k, rng=rng, **METAL) * env(n_de(0.2), 0.001, 0.08) * 0.08, 0.95 + 0.02 * k)
    return reverb(x, 0.5, 0.25)


def za_warudo_preparo(rng, v):
    """O Preparo do O Mundo: o tique-taque do relógio, cada vez mais alto, e o coração batendo."""
    x = _z(1.3)
    for k in range(6):
        n = n_de(0.05)
        poe(x, seno(1400 if k % 2 == 0 else 1100, n) * env(n, 0.001, 0.04) * (0.04 + 0.01 * k), 0.05 + 0.2 * k)
    for k in range(3):
        poe(x, baque(n_de(0.2), 60, 40, 0.08, 0.1) * 0.4, 0.15 + 0.4 * k)
    return reverb(x, 0.5, 0.3)


def za_warudo(rng, v):
    """O Mundo: o som sugado do tempo parando, o tique do relógio que trava, o silêncio — e o rolo
    compressor caindo (o assobio que desce e o estrondo metálico enorme)."""
    x = _z(2.2)
    poe(x, _tempo_para(rng, 0.7), 0.0)
    n = n_de(0.05)
    poe(x, seno(1300, n) * env(n, 0.001, 0.04) * 0.08, 0.72)
    poe(x, _whoosh(rng, 0.45, 1600, 300, 0.85, 1.4, 0.5), 0.85)
    poe(x, baque(n_de(1.0), 55, 25, 0.5, 0.8) * 1.0, 1.32)
    poe(x, modal(n_de(1.0), 180, rng=rng, **METAL) * env(n_de(1.0), 0.001, 0.6) * 0.3, 1.32)
    poe(x, B.terremoto(rng, v)[: n_de(0.7)] * 0.4, 1.35)
    return reverb(x, 0.55, 0.3)


# =================================================================== Giorno
def reflexo_de_dano(rng, v):
    """A Gold Experience: as vinhas brotando (o estalar de galhos crescendo), as folhas abrindo (o
    farfalhar), o tom dourado da joaninha e o "ping" do dano voltando."""
    x = _z(1.7)
    for k in range(10):
        poe(x, estalo(rng, n_de(0.015), 600, 3000) * 0.25, 0.02 + 0.045 * k)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 2000, 8000, 2) * sobe_e_some(n, 0.4, 1.4) * 0.2, 0.3)
    m = n_de(1.0)
    poe(x, (seno(523.25, m) + seno(659.25, m) * 0.6 + seno(783.99, m) * 0.4) * sobe_e_some(m, 0.2, 1.4) * 0.05, 0.45)
    for k in range(3):
        poe(x, _brilho(rng, 0.25, 2200 + 300 * k, 0.06, METAL), 0.95 + 0.05 * k)
    return reverb(x, 0.55, 0.3)


def ouro_preparo(rng, v):
    """O Preparo da Experiência dourada: o acorde dourado subindo, suave, e o brilho."""
    x = _z(1.3)
    n = n_de(1.2)
    poe(x, (seno(392, n) + seno(493.88, n) * 0.6 + seno(587.33, n) * 0.4) * sobe_e_some(n, 0.8, 1.1) * 0.05, 0.0)
    poe(x, _brilho(rng, 0.8, 1568, 0.04, CRISTAL), 0.6)
    return reverb(x, 0.6, 0.35)


def experiencia_dourada(rng, v):
    """A vida criada: as flores desabrochando (os "plim" suaves em escala que sobe), o acorde dourado
    cheio e as pétalas voando (o vento leve)."""
    x = _z(2.0)
    escala = (523.25, 587.33, 659.25, 783.99, 880.0, 1046.5, 1174.7, 1318.5, 1568.0)
    for k, f in enumerate(escala):
        poe(x, _brilho(rng, 0.5, f, 0.045, SINO), 0.05 + 0.05 * k)
    n = n_de(1.2)
    poe(x, sum(seno(f, n) * a for f, a in ((261.63, 1), (329.63, 0.7), (392.0, 0.6), (523.25, 0.4))) * sobe_e_some(n, 0.3, 1.3) * 0.05, 0.5)
    m = n_de(0.8)
    poe(x, passa(rosa(rng, m), 800, 4000, 2) * sobe_e_some(m, 0.4, 1.3) * 0.12, 0.9)
    return reverb(x, 0.65, 0.35)


SONS: dict = {
    "chuva-de-fogo": (chuva_de_fogo, "Roy: o estalo e a chuva de fogo"),
    "ignicao-preparo": (ignicao_preparo, "Roy: a luva e o ar esquentando (antes do golpe)"),
    "campo-incendiado": (campo_incendiado, "Roy: o fogo correndo e a detonação"),
    "visao-de-falcao": (visao_de_falcao, "Griffith: o grito do falcão e a mira"),
    "comando-da-banda": (comando_da_banda, "Griffith: a bandeira, a corneta e o brado"),
    "eclipse-preparo": (eclipse_preparo, "Griffith: o eclipse crescendo (antes do golpe)"),
    "destino-ascendente": (destino_ascendente, "Griffith: o sino, as asas e a onda escura"),
    "precisao-absoluta": (precisao_absoluta, "Jotaro: o dedo estelar e o impacto exato"),
    "star-preparo": (star_preparo, "Jotaro: o Star Platinum e as estrelas (antes do golpe)"),
    "the-world-jotaro": (the_world_jotaro, "Jotaro: o tempo parado e a rajada"),
    "facas-do-dio": (facas_do_dio, "Dio: as facas no tempo parado"),
    "za-warudo-preparo": (za_warudo_preparo, "Dio: o relógio e o coração (antes do golpe)"),
    "za-warudo": (za_warudo, "Dio: o tempo para e o rolo compressor cai"),
    "reflexo-de-dano": (reflexo_de_dano, "Giorno: as vinhas, as folhas e o dano voltando"),
    "ouro-preparo": (ouro_preparo, "Giorno: o acorde dourado (antes do golpe)"),
    "experiencia-dourada": (experiencia_dourada, "Giorno: as flores desabrochando"),
}
