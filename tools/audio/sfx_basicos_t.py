"""Sons dos ataques básicos, lote t (veja tools/vfx/familias_v2/basicos_t.py).

O zumbido da pistola desidratadora do Megamente e o "plic" do cubo, o soco do Vilgax com o tremor, o "puf" das
varinhas de Cosmo e Wanda, a espada do Steve com o "ugh" do dano em blocos, o "ssss" do Creeper e a explosão,
o "wakka-wakka" do Pac-Man, o giro do Crash, o Dead Eye (o coração lento e os tiros em fila), o canivete da Ellie,
os ossos do Sans com o tom do olho azul, as ervilhas do Cuphead, o Fus Ro Dah, o Ferrão do Cavaleiro, os quatro
socos do Goro e a língua do Yoshi com o ovo.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_basicos_k import _acerto, _mola
from sfx_basicos_l import _estrelinhas
from sfx_basicos_m import _zap
from sfx_basicos_o import _voz
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _quadrada(f, n, duty=0.5):
    """A onda quadrada dos jogos antigos (o timbre de chip)."""
    fase = np.cumsum(np.broadcast_to(np.asarray(f, dtype=float), (n,)) / SR) % 1.0
    return np.where(fase < duty, 1.0, -1.0)


def pistola_de_megamente(rng, v):
    """A pistola do Megamente: o zumbido de ficção científica que sobe e oscila, o raio e o "plic" do cubinho caindo."""
    x = _z(1.3)
    n = n_de(0.45)
    f = varre(300, 1200, n, 1.0) * (1 + 0.08 * np.sin(2 * math.pi * 18 * _t(n)))
    poe(x, seno(f, n) * sobe_e_some(n, 0.3, 1.3) * 0.08, 0.0)
    poe(x, _zap(rng, 0.3, 0.2), 0.18)
    m = n_de(0.35)
    poe(x, seno(varre(900, 200, m, 1.0), m) * sobe_e_some(m, 0.2, 1.3) * 0.07, 0.38)
    poe(x, modal(n_de(0.2), 1800, rng=rng, **CRISTAL) * env(n_de(0.2), 0.0005, 0.06) * 0.2, 0.62)
    poe(x, B._baque_seco(rng, n_de(0.15), 400, 0.03) * 0.3, 0.85)
    return reverb(x, 0.45, 0.22)


def soco_de_vilgax(rng, v):
    """O soco do Vilgax: o rugido grave e molhado, o soco pesado e o chão tremendo por baixo."""
    x = _z(1.5)
    poe(x, _voz(rng, 0.35, 90, 75, 0.12, 4, 20), 0.0)
    poe(x, passa(rosa(rng, n_de(0.3)), 200, 1500, 2) * np.abs(np.sin(2 * math.pi * 9 * _t(n_de(0.3)))) * env(n_de(0.3), 0.02, 0.2) * 0.15, 0.05)
    poe(x, _whoosh(rng, 0.25, 200, 1000, 0.85, 1.3, 0.5), 0.1)
    poe(x, baque(n_de(0.6), 55, 25, 0.25, 1.0) * 1.0, 0.32)
    poe(x, _acerto(rng, 1.0, 85), 0.32)
    m = n_de(0.6)
    poe(x, passa(rosa(rng, m), 30, 180, 2) * env(m, 0.01, 0.4) * 0.6, 0.34)
    return reverb(x, 0.6, 0.28)


def puf_das_varinhas(rng, v):
    """As varinhas de Cosmo e Wanda: o "pling-pling" das duas estrelas, o brilho subindo e o "PUF!" de fumacinha."""
    x = _z(1.3)
    poe(x, _brilho(rng, 0.4, 1568, 0.08, SINO), 0.0)
    poe(x, _brilho(rng, 0.4, 2093, 0.08, SINO), 0.08)
    n = n_de(0.2)
    poe(x, seno(varre(800, 2400, n, 1.0), n) * sobe_e_some(n, 0.6, 1.2) * 0.05, 0.2)
    m = n_de(0.3)
    poe(x, passa(rosa(rng, m), 200, 3000, 2) * env(m, 0.003, 0.15) * 0.8 + baque(m, 160, 80, 0.06, 1.0) * 0.3, 0.38)
    _estrelinhas(rng, 0.42, x, 0.05)
    return reverb(x, 0.5, 0.25)


def espada_de_diamante(rng, v):
    """A espada do Steve: o golpe seco de jogo de blocos e o "ugh" curto do dano (o tom que cai), com os estalinhos."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.2, 600, 3000, 0.85, 1.3, 0.4), 0.08)
    poe(x, B._baque_seco(rng, n_de(0.2), 180, 0.05) * 0.8 + passa(rosa(rng, n_de(0.2)), 1000, 5000, 2) * env(n_de(0.2), 0.001, 0.04) * 0.4, 0.3)
    m = n_de(0.15)
    poe(x, passa(_quadrada(varre(320, 180, m, 1.0), m, 0.3) * env(m, 0.005, 0.1), None, 2500, 2) * 0.12, 0.31)
    for k in range(5):
        poe(x, estalo(rng, n_de(0.02), 1500, 5000, 0.003) * 0.3, 0.35 + 0.03 * k)
    return reverb(x, 0.35, 0.18)


def ssss_do_creeper(rng, v):
    """O Creeper: o "ssssss" do pavio que cresce e a explosão em blocos (o estrondo e as pedrinhas)."""
    x = _z(1.6)
    n = n_de(0.42)
    poe(x, passa(rosa(rng, n), 3500, 10000, 2) * sobe_e_some(n, 0.9, 1.0) * 0.4, 0.0)
    poe(x, satura(baque(n_de(0.8), 60, 25, 0.3, 1.0) + passa(rosa(rng, n_de(0.8)), 80, 4000, 2) * env(n_de(0.8), 0.002, 0.35) * 1.2, 2.2) * 0.8, 0.42)
    m = n_de(0.6)
    poe(x, graos(rng, m, 45, 0.0, 0.55, 600, 4000, 0.008) * 0.5, 0.45)
    return reverb(x, 0.6, 0.3)


def chomp_do_pacman(rng, v):
    """O Pac-Man: o "wakka-wakka" de chip (o tom que sobe e desce em cada pastilha) e a mordida final."""
    x = _z(1.2)
    for k in range(5):
        m = n_de(0.08)
        f = varre(200, 500, m, 1.0) if k % 2 == 0 else varre(500, 200, m, 1.0)
        poe(x, passa(_quadrada(f, m, 0.5), None, 3000, 2) * env(m, 0.003, 0.05) * 0.07, 0.02 + 0.085 * k)
    m = n_de(0.2)
    poe(x, passa(_quadrada(varre(600, 120, m, 1.0), m, 0.5), None, 3000, 2) * env(m, 0.003, 0.15) * 0.08, 0.44)
    poe(x, _acerto(rng, 0.8, 120), 0.46)
    return reverb(x, 0.3, 0.15)


def giro_do_crash(rng, v):
    """O giro do Crash: o "uuuuuí" do tornado (o vento que pulsa rápido), a pancada e a caixa de madeira quebrando."""
    x = _z(1.3)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 500, 3000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 16 * _t(n))) * sobe_e_some(n, 0.6, 1.2) * 0.5, 0.0)
    poe(x, seno(varre(400, 900, n, 1.0) * (1 + 0.1 * np.sin(2 * math.pi * 16 * _t(n))), n) * sobe_e_some(n, 0.6, 1.2) * 0.04, 0.0)
    poe(x, _acerto(rng, 0.9, 115), 0.36)
    m = n_de(0.35)
    poe(x, estalo(rng, m, 500, 4000, 0.01) * 0.8 + passa(rosa(rng, m), 250, 1200, 2) * env(m, 0.001, 0.06) * 0.5, 0.37)
    poe(x, _mola(0.3, 500, 0.4, 11.0, 0.08), 0.55)
    return reverb(x, 0.4, 0.2)


def dead_eye(rng, v):
    """O Dead Eye: o mundo desacelera (o grave abafado e o coração lento), as marcas ("tic" a cada X) e os três tiros
    em fila rápida."""
    x = _z(1.5)
    n = n_de(0.45)
    poe(x, passa(rosa(rng, n), 60, 400, 2) * sobe_e_some(n, 0.3, 1.3) * 0.4, 0.0)
    for t0 in (0.02, 0.24):
        poe(x, baque(n_de(0.2), 60, 40, 0.06, 1.0) * 0.5, t0)
    for k in range(3):
        poe(x, modal(n_de(0.06), 2600, rng=rng, **METAL) * env(n_de(0.06), 0.0005, 0.02) * 0.15, 0.07 + 0.07 * k)
    for k in range(3):
        m = n_de(0.3)
        tiro = satura(baque(m, 130, 55, 0.06, 1.0) * 0.8 + passa(rosa(rng, m), 300, 8000, 2) * env(m, 0.0005, 0.05) * 1.2, 1.6) * 0.6
        poe(x, tiro, 0.32 + 0.05 * k)
    return reverb(x, 0.6, 0.3)


def canivete_de_ellie(rng, v):
    """O canivete da Ellie: o "clic" da lâmina abrindo, o grunhido curto de esforço e as duas facadas."""
    x = _z(1.1)
    poe(x, modal(n_de(0.08), 3000, rng=rng, **METAL) * env(n_de(0.08), 0.0005, 0.02) * 0.3, 0.02)
    poe(x, _voz(rng, 0.1, 330, 280, 0.06, 3, 10), 0.16)
    for t0 in (0.22, 0.34):
        poe(x, _whoosh(rng, 0.08, 1500, 6000, 0.8, 1.2, 0.25), t0 - 0.04)
        poe(x, B._carne(rng, n_de(0.12), 0.02, 2.0) * 0.6, t0 + 0.02)
    poe(x, _acerto(rng, 0.6, 140, 1500, 5000), 0.36)
    return reverb(x, 0.35, 0.18)


def ossos_de_sans(rng, v):
    """Os ossos do Sans: o "uóóm" do olho acendendo, os ossos brotando do chão em fila (os toques secos de osso) e o
    osso azul passando."""
    x = _z(1.3)
    n = n_de(0.4)
    poe(x, (seno(varre(220, 330, n, 1.0), n) + 0.4 * seno(varre(440, 660, n, 1.0), n)) * sobe_e_some(n, 0.3, 1.3) * 0.06, 0.0)
    for k in range(6):
        poe(x, modal(n_de(0.08), 900 + 60 * k, rng=rng, desafina=0.03, **VIDRO) * env(n_de(0.08), 0.0005, 0.03) * 0.15 + estalo(rng, n_de(0.08), 1500, 5000, 0.003) * 0.25, 0.18 + 0.025 * k)
    poe(x, _whoosh(rng, 0.25, 800, 3000, 0.8, 1.2, 0.3), 0.3)
    poe(x, _acerto(rng, 0.6, 130), 0.28)
    return reverb(x, 0.45, 0.22)


def dedo_de_ervilha(rng, v):
    """As ervilhas do Cuphead: os "pew-pew" de desenho antigo (o tom que cai rápido) e os "ploc" de cada ervilha."""
    x = _z(1.1)
    for k in range(4):
        m = n_de(0.08)
        poe(x, seno(varre(1600, 600, m, 1.0), m) * env(m, 0.002, 0.06) * 0.08 + passa(rosa(rng, m), 2000, 6000, 2) * env(m, 0.001, 0.03) * 0.15, 0.12 + 0.07 * k)
        poe(x, B._baque_seco(rng, n_de(0.1), 300, 0.03) * 0.35 + passa(rosa(rng, n_de(0.1)), 500, 3000, 2) * env(n_de(0.1), 0.001, 0.04) * 0.3, 0.28 + 0.07 * k)
    return reverb(x, 0.4, 0.2)


def fus_ro_dah(rng, v):
    """O Fus Ro Dah: as três sílabas gritadas em voz grave (cada uma mais forte) e a onda de ar que empurra."""
    x = _z(1.6)
    for k, (f0, f1) in enumerate(((150, 140), (140, 130), (130, 100))):
        poe(x, _voz(rng, 0.12 + 0.04 * k, f0, f1, 0.1 + 0.03 * k, 4, 16), 0.03 + 0.1 * k)
    for k in range(3):
        m = n_de(0.4)
        poe(x, passa(rosa(rng, m), 80, 1500, 2) * env(m, 0.01, 0.25) * (0.3 + 0.2 * k), 0.06 + 0.1 * k)
    poe(x, baque(n_de(0.5), 70, 30, 0.2, 1.0) * 0.6, 0.3)
    return reverb(x, 0.7, 0.35)


def golpe_de_ferrao(rng, v):
    """O Ferrão do Cavaleiro: o corte curto e metálico (o "tchin" agudo), o acerto e a Alma voltando num brilho."""
    x = _z(1.2)
    poe(x, _whoosh(rng, 0.12, 1500, 7000, 0.8, 1.2, 0.35), 0.16)
    poe(x, B._lamina_curta(rng, n_de(0.25), 3500) * env(n_de(0.25), 0.0008, 0.08) * 0.25, 0.27)
    poe(x, _acerto(rng, 0.7, 130, 1500, 6000), 0.28)
    n = n_de(0.5)
    poe(x, seno(varre(600, 1200, n, 1.0), n) * sobe_e_some(n, 0.4, 1.3) * 0.04, 0.4)
    poe(x, _brilho(rng, 0.4, 1760, 0.05, CRISTAL), 0.72)
    return reverb(x, 0.6, 0.3)


def quatro_punhos(rng, v):
    """Os quatro socos do Goro: quatro pancadas pesadas em fila rápida e o rugido no fim."""
    x = _z(1.3)
    for k, t0 in enumerate((0.08, 0.12, 0.17, 0.22)):
        poe(x, _acerto(rng, 0.9, 95 - 4 * k), t0)
        poe(x, baque(n_de(0.25), 70, 40, 0.08, 1.0) * 0.5, t0)
    poe(x, _voz(rng, 0.3, 120, 90, 0.1, 4, 18), 0.32)
    return reverb(x, 0.45, 0.22)


def lingua_de_yoshi(rng, v):
    """A língua do Yoshi: o "thhp" da língua saindo, o estalo, o "yoshi!" agudo em dois tons e o ovo quicando e
    quebrando."""
    x = _z(1.3)
    n = n_de(0.15)
    poe(x, passa(rosa(rng, n), 1000, 4000, 2) * env(n, 0.005, 0.1) * 0.35, 0.04)
    poe(x, _acerto(rng, 0.6, 140), 0.2)
    poe(x, B._carne(rng, n_de(0.1), 0.02, 2.0) * 0.4, 0.38)
    poe(x, _voz(rng, 0.08, 700, 760, 0.04, 2, 6), 0.42)
    poe(x, _voz(rng, 0.1, 880, 820, 0.04, 2, 6), 0.5)
    for k, t0 in enumerate((0.6, 0.7)):
        poe(x, B._baque_seco(rng, n_de(0.1), 260, 0.03) * (0.4 - 0.15 * k), t0)
    poe(x, estalo(rng, n_de(0.2), 1500, 6000, 0.006) * 0.6 + modal(n_de(0.2), 1400, rng=rng, desafina=0.05, **VIDRO) * env(n_de(0.2), 0.0005, 0.05) * 0.1, 0.78)
    _estrelinhas(rng, 0.8, x, 0.04)
    return reverb(x, 0.4, 0.2)


SONS: dict = {
    "pistola-de-megamente": (pistola_de_megamente, "básico do Megamente: o raio e o cubinho"),
    "soco-de-vilgax": (soco_de_vilgax, "básico do Vilgax: o rugido e o soco"),
    "puf-das-varinhas": (puf_das_varinhas, "básico de Cosmo e Wanda: as varinhas e o puf"),
    "espada-de-diamante": (espada_de_diamante, "básico do Steve: a espadada em blocos"),
    "ssss-do-creeper": (ssss_do_creeper, "básico do Creeper: o pavio e a explosão"),
    "chomp-do-pacman": (chomp_do_pacman, "básico do Pac-Man: o wakka-wakka"),
    "giro-do-crash": (giro_do_crash, "básico do Crash: o tornado e a caixa"),
    "dead-eye": (dead_eye, "básico do Arthur Morgan: o Dead Eye"),
    "canivete-de-ellie": (canivete_de_ellie, "básico da Ellie: o canivete"),
    "ossos-de-sans": (ossos_de_sans, "básico do Sans: o olho e os ossos"),
    "dedo-de-ervilha": (dedo_de_ervilha, "básico do Cuphead: as ervilhas"),
    "fus-ro-dah": (fus_ro_dah, "básico do Dovahkiin: o Thu'um"),
    "golpe-de-ferrao": (golpe_de_ferrao, "básico do Cavaleiro: o Ferrão e a Alma"),
    "quatro-punhos": (quatro_punhos, "básico do Goro: os quatro socos"),
    "lingua-de-yoshi": (lingua_de_yoshi, "básico do Yoshi: a língua e o ovo"),
}
