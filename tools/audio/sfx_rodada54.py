"""Os sons da rodada 54 das habilidades próprias (veja tools/vfx/familias_v2/rodada54.py)."""
from __future__ import annotations

import math

import numpy as np

from sfx_familias import _brilho, _whoosh, _z
from sfx_rodada16 import _explosao
from sfx_unicas_d import _acorde, _baque, _sino, _sopro, _t
from sfx_unicas_i import _piu
from som import CRISTAL, METAL, SINO, env, estalo, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _tiro(rng, g=0.6, grave=150):
    x = _z(0.6)
    poe(x, estalo(rng, n_de(0.03), 500, 9000, 0.01) * g * 2.0, 0.0)
    poe(x, _baque(grave, grave * 0.4, 0.15, g * 0.7, 2.5), 0.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 300, 4000, 2) * env(n, 0.002, 0.35) * g * 0.4, 0.0)
    return x


def _servo(rng, seg=0.15, f0=400, f1=700, g=0.012):
    n = n_de(seg)
    return satura(seno(varre(f0, f1, n), n), 2) * env(n, 0.02, seg * 0.6) * g


def _feitico(rng, f0, f1, seg, g=0.03):
    """O feitiço saindo da varinha (o "fiuuu" brilhante)."""
    n = n_de(seg)
    x = (seno(varre(f0, f1, n), n) + seno(varre(f0 * 1.5, f1 * 1.5, n), n) * 0.4) * env(n, 0.01, seg * 0.7) * g
    return x + passa(rosa(rng, n), 2000, 9000, 2) * env(n, 0.01, seg * 0.6) * g * 4


def _corda(rng):
    x = _z(0.4)
    n = n_de(0.22)
    poe(x, seno(varre(230, 195, n), n) * env(n, 0.002, 0.2) * 0.045, 0.0)
    poe(x, estalo(rng, n_de(0.02), 600, 4000, 0.004) * 0.6, 0.0)
    return x


# ------------------------------------------------------------------ RoboCop

def auto_9(rng, v):
    """RoboCop: a pistola saindo da coxa (os servos) e a rajada de três tiros."""
    x = _z(2.0)
    poe(x, _servo(rng, 0.15, 300, 600, 0.015), 0.0)
    poe(x, estalo(rng, n_de(0.02), 1000, 5000, 0.004) * 0.6, 0.18)
    for k in range(3):
        poe(x, _tiro(rng, 0.5, 170), 0.25 + 0.07 * k)
    for k in range(2):
        poe(x, seno(1800, n_de(0.04)) * env(n_de(0.04), 0.002, 0.03) * 0.012, 0.6 + 0.08 * k)
    return reverb(x, 0.6, 0.3)


def proteger_o_inocente(rng, v):
    """RoboCop: as diretrizes no visor (os bipes) e o escudo ligando."""
    x = _z(2.2)
    for k in range(3):
        n = n_de(0.08)
        poe(x, seno(1400 + 200 * k, n) * env(n, 0.003, 0.06) * 0.012, 0.05 + 0.1 * k)
    n2 = n_de(0.5)
    poe(x, seno(varre(200, 500, n2), n2) * env(n2, 0.3, 0.15) * 0.025, 0.3)
    poe(x, _brilho(rng, 0.5, 1319, 0.012, CRISTAL), 0.55)
    return reverb(x, 0.6, 0.3)


def robocop_preparo(rng, v):
    """RoboCop (Preparo): o visor varrendo (o zumbido eletrônico em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, satura(seno(120 + 40 * np.sin(2 * math.pi * 1.5 * t), n), 2) * sobe_e_some(n, 0.5, 1.2) * 0.012, 0.0)
    for k in range(2):
        poe(x, _servo(rng, 0.12, 500, 800, 0.008), 0.5 * k)
    return reverb(x, 0.5, 0.25)


def vivo_ou_morto(rng, v):
    """RoboCop: a mira travando ("bip-bip-biiip") e a rajada pesada."""
    x = _z(2.2)
    for k in range(3):
        n = n_de(0.05 if k < 2 else 0.2)
        poe(x, seno(1600, n) * env(n, 0.002, 0.04) * 0.014, 0.05 + 0.1 * k)
    for k in range(5):
        poe(x, _tiro(rng, 0.55, 140), 0.3 + 0.06 * k)
    poe(x, _baque(60, 22, 0.6, 0.8, 2.8), 0.4)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Rambo

def flecha_explosiva_rambo(rng, v):
    """Rambo: o arco, a flecha cravando e o bipe da ponta explosiva."""
    x = _z(2.0)
    poe(x, _corda(rng), 0.05)
    poe(x, _whoosh(rng, 0.25, 2000, 10000, 0.8, 1.3, 0.35), 0.06)
    poe(x, _baque(200, 100, 0.12, 0.35), 0.3)
    for k in range(5):
        poe(x, _piu(2000, 2000, 0.04, 0.018), 0.4 + 0.12 * k)
    return reverb(x, 0.5, 0.25)


def faca_de_sobrevivencia(rng, v):
    """Rambo: a faca serrilhada girando e o corte."""
    x = _z(1.9)
    n = n_de(0.35)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 20 * t) ** 2) * env(n, 0.02, 0.3) * 0.25, 0.0)
    poe(x, _sino(rng, 1760, 0.3, 0.02, METAL), 0.33)
    poe(x, _baque(140, 60, 0.25, 0.5), 0.34)
    return reverb(x, 0.5, 0.25)


def rambo_preparo(rng, v):
    """Rambo (Preparo): a selva — os grilos e as folhas se mexendo (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, seno(4200, n) * (np.sin(2 * math.pi * 30 * t) > 0.6) * (np.sin(2 * math.pi * 2 * t) > 0) * sobe_e_some(n, 0.5, 1.2) * 0.006, 0.0)
    for k in range(3):
        n2 = n_de(0.15)
        poe(x, passa(rosa(rng, n2), 1500, 6000, 2) * env(n2, 0.03, 0.1) * 0.12, 0.3 * k + 0.1)
    return reverb(x, 0.6, 0.3)


def emboscada_na_selva(rng, v):
    """Rambo: as folhas caindo e as armadilhas fechando de uma vez nos rivais."""
    x = _z(2.3)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.2, 0.0)
    for k in range(3):
        poe(x, _whoosh(rng, 0.2, 400, 4000, 0.85, 1.3, 0.35), 0.28 + 0.07 * k)
        poe(x, estalo(rng, n_de(0.03), 600, 4000, 0.008) * 0.9, 0.45 + 0.07 * k)
        poe(x, _baque(150, 70, 0.15, 0.35), 0.45 + 0.07 * k)
    return reverb(x, 0.6, 0.3)


# ------------------------------------------------------------------ Indiana Jones

def chicotada(rng, v):
    """Indiana Jones: o estalo do chicote e o buff arrancado."""
    x = _z(1.9)
    poe(x, _whoosh(rng, 0.25, 800, 6000, 0.85, 1.3, 0.4), 0.0)
    poe(x, estalo(rng, n_de(0.03), 2000, 10000, 0.004) * 1.5, 0.26)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 600, 3000, 2) * env(n, 0.03, 0.2) * 0.25, 0.32)
    for m in range(4):
        poe(x, _sino(rng, 2637 + 300 * m, 0.15, 0.012, CRISTAL), 0.52 + 0.025 * m)
    return reverb(x, 0.5, 0.25)


def pedra_rolando(rng, v):
    """Indiana Jones: a pedra gigante rolando (o ronco grave crescendo) e passando por cima."""
    x = _z(2.4)
    n = n_de(1.4)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 30, 300, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 5 * t)), 2) * sobe_e_some(n, 0.5, 1.0) * 0.7, 0.0)
    for k in range(3):
        poe(x, _baque(60, 25, 0.3, 0.5, 2.5), 0.3 + 0.2 * k)
    return reverb(x, 0.7, 0.35)


def indy_preparo(rng, v):
    """Indiana Jones (Preparo): o ídolo brilhando (o coro do templo em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, (seno(220, n) + seno(277, n) * 0.6 + seno(330, n) * 0.4) * sobe_e_some(n, 0.5, 1.2) * 0.018, 0.0)
    poe(x, _sino(rng, 1319, 0.5, 0.01, CRISTAL), 0.3)
    return reverb(x, 0.9, 0.45)


def reliquia(rng, v):
    """Indiana Jones: o ídolo dourado acendendo e a fanfarra de aventura."""
    x = _z(2.3)
    for k, f in enumerate((392, 440, 494, 587, 784)):
        poe(x, _sino(rng, f, 0.5, 0.022, SINO), 0.06 * k)
    poe(x, _acorde((392, 494, 587, 784), 1.0, 0.022), 0.4)
    poe(x, _brilho(rng, 0.7, 1568, 0.015, CRISTAL), 0.45)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Jack Sparrow

def bussola_magica(rng, v):
    """Jack Sparrow: a bússola girando ("tic-tic-tic") até parar no rival."""
    x = _z(2.0)
    for k in range(10):
        poe(x, estalo(rng, n_de(0.012), 2000, 7000, 0.002) * 0.5, 0.05 + 0.04 * k + 0.003 * k * k)
    poe(x, _sino(rng, 1568, 0.6, 0.025, CRISTAL), 0.55)
    n = n_de(0.5)
    poe(x, (seno(330, n) + seno(415, n)) * env(n, 0.05, 0.4) * 0.012, 0.6)
    return reverb(x, 0.7, 0.35)


def pistola_de_um_tiro(rng, v):
    """Jack Sparrow: a pederneira, o tiro com fumaça e o eco."""
    x = _z(2.0)
    poe(x, estalo(rng, n_de(0.02), 1000, 5000, 0.004) * 0.6, 0.15)
    poe(x, _tiro(rng, 0.9, 110), 0.27)
    n = n_de(0.6)
    poe(x, passa(rosa(rng, n), 200, 2000, 2) * env(n, 0.05, 0.5) * 0.15, 0.3)
    return reverb(x, 0.9, 0.45)


def sparrow_preparo(rng, v):
    """Jack Sparrow (Preparo): o mar e o vento nas velas (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 200, 2000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 0.8 * t)) * sobe_e_some(n, 0.4, 1.2) * 0.25, 0.0)
    poe(x, _sopro(rng, 0.8, 300, 2000, 0.1, 0.4), 0.1)
    return reverb(x, 0.7, 0.35)


def perola_negra(rng, v):
    """Jack Sparrow: o navio rangendo e os três canhões disparando nos rivais."""
    x = _z(2.5)
    n = n_de(0.4)
    poe(x, satura(passa(rosa(rng, n), 100, 800, 2), 2) * env(n, 0.1, 0.3) * 0.2, 0.0)
    for k in range(3):
        poe(x, _baque(55, 22, 0.5, 0.8, 3.0), 0.3 + 0.07 * k)
        poe(x, _explosao(rng, 0.35, 70), 0.58 + 0.07 * k)
    return reverb(x, 0.8, 0.4)


# ------------------------------------------------------------------ Harry Potter

def expelliarmus_harry(rng, v):
    """Harry: "Expelliarmus!" — o raio vermelho e os buffs voando longe."""
    x = _z(2.0)
    poe(x, _feitico(rng, 600, 1400, 0.35, 0.025), 0.08)
    poe(x, _baque(150, 70, 0.2, 0.45), 0.32)
    for k in range(2):
        poe(x, _piu(1500, 2500, 0.2, 0.015), 0.4 + 0.06 * k)
    return reverb(x, 0.7, 0.35)


def protego(rng, v):
    """Harry: "Protego!" — o escudo brilhando na frente do trio."""
    x = _z(2.1)
    n = n_de(0.4)
    poe(x, (seno(varre(400, 800, n), n) + seno(varre(600, 1200, n), n) * 0.5) * env(n, 0.2, 0.15) * 0.022, 0.0)
    for k in range(3):
        poe(x, _sino(rng, 1319 + 150 * k, 0.6, 0.015, CRISTAL), 0.1 + 0.07 * k)
    return reverb(x, 0.8, 0.4)


def harry_preparo(rng, v):
    """Harry (Preparo): a névoa prateada juntando na varinha (em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(587, n) + seno(880, n) * 0.5) * (0.7 + 0.3 * np.sin(2 * math.pi * 3 * t)) * sobe_e_some(n, 0.5, 1.2) * 0.012, 0.0)
    poe(x, _sopro(rng, 0.8, 1000, 5000, 0.08, 0.5), 0.1)
    return reverb(x, 0.9, 0.45)


def expecto_patronum(rng, v):
    """Harry: "Expecto Patronum!" — o cervo prateado galopando e a luz limpando."""
    x = _z(2.4)
    poe(x, _feitico(rng, 400, 1200, 0.4, 0.025), 0.0)
    for k in range(6):
        poe(x, _baque(300, 200, 0.05, 0.15), 0.2 + 0.1 * k)
    poe(x, _acorde((587, 740, 880, 1175), 1.2, 0.025), 0.3)
    poe(x, _brilho(rng, 1.0, 1760, 0.018, CRISTAL), 0.4)
    return reverb(x, 0.9, 0.45)


# ------------------------------------------------------------------ Voldemort

def crucio(rng, v):
    """Voldemort: "Crucio!" — a dor estalando no rival."""
    x = _z(2.1)
    poe(x, _feitico(rng, 300, 600, 0.3, 0.025), 0.05)
    n = n_de(0.7)
    t = _t(n)
    poe(x, satura(passa(rosa(rng, n), 800, 6000, 2) * (np.sin(2 * math.pi * 40 * t) > 0.3), 3) * env(n, 0.02, 0.5) * 0.25, 0.2)
    n2 = n_de(0.6)
    poe(x, (seno(110, n2) + seno(116.5, n2)) * sobe_e_some(n2, 0.3, 1.2) * 0.025, 0.25)
    return reverb(x, 0.8, 0.4)


def imperius(rng, v):
    """Voldemort: "Imperio!" — os fios descendo e o tom hipnótico."""
    x = _z(2.2)
    poe(x, _feitico(rng, 500, 300, 0.3, 0.02), 0.05)
    n = n_de(1.0)
    t = _t(n)
    poe(x, (seno(330, n) + seno(331.5, n) + seno(495, n) * 0.4) * (0.6 + 0.4 * np.sin(2 * math.pi * 2 * t)) * sobe_e_some(n, 0.3, 1.2) * 0.018, 0.2)
    for k in range(4):
        poe(x, _sino(rng, 2093 + 100 * k, 0.15, 0.008, CRISTAL), 0.2 + 0.05 * k)
    return reverb(x, 0.9, 0.45)


def voldemort_preparo(rng, v):
    """Voldemort (Preparo): a Marca Negra no céu (o coro sombrio e o sibilo de cobra em laço)."""
    x = _z(1.4)
    n = n_de(1.0)
    poe(x, (seno(73.4, n) + seno(77.8, n) + seno(110, n) * 0.5) * sobe_e_some(n, 0.4, 1.2) * 0.02, 0.0)
    n2 = n_de(0.4)
    poe(x, passa(rosa(rng, n2), 4000, 10000, 2) * sobe_e_some(n2, 0.3, 1.2) * 0.08, 0.5)
    return reverb(x, 1.0, 0.5)


def avada_kedavra(rng, v):
    """Voldemort: "Avada Kedavra!" — o raio verde rasgando e o estrondo surdo."""
    x = _z(2.5)
    n = n_de(0.3)
    poe(x, seno(varre(150, 600, n), n) * env(n, 0.25, 0.05) * 0.03, 0.0)
    n2 = n_de(0.25)
    poe(x, satura(passa(rosa(rng, n2), 1000, 8000, 2), 3) * env(n2, 0.005, 0.2) * 0.4, 0.25)
    poe(x, _baque(45, 18, 1.0, 1.0, 3.2), 0.42)
    n3 = n_de(1.0)
    poe(x, (seno(55, n3) + seno(58.3, n3)) * sobe_e_some(n3, 0.1, 1.2) * 0.04, 0.42)
    return reverb(x, 1.0, 0.5)


# ------------------------------------------------------------------ Light (Mecânica única)

def pagina_no_relogio(rng, v):
    """Light: os quatro cliques da coroa do relógio, o fundo falso abrindo, a caneta riscando o nome e o coração do rival parando."""
    x = _z(2.6)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.012), 2500, 9000, 0.002) * 0.7, 0.03 + 0.05 * k)
    poe(x, _sino(rng, 2637, 0.3, 0.012, METAL), 0.22)
    n = n_de(0.1)
    poe(x, passa(rosa(rng, n), 1500, 6000, 2) * env(n, 0.01, 0.08) * 0.2, 0.25)
    n2 = n_de(0.5)
    t2 = _t(n2)
    poe(x, passa(rosa(rng, n2), 2500, 9000, 2) * (0.4 + 0.6 * np.abs(np.sin(2 * math.pi * 14 * t2))) * env(n2, 0.02, 0.05) * 0.15, 0.38)
    for k in range(3):
        poe(x, _baque(60, 40, 0.18, 0.7 - 0.2 * k, 2.2), 0.72 + 0.22 * k)
    n3 = n_de(1.2)
    poe(x, (seno(110, n3) + seno(116.5, n3) + seno(164.8, n3) * 0.5) * sobe_e_some(n3, 0.15, 1.2) * 0.022, 0.65)
    return reverb(x, 1.0, 0.5)


SONS: dict = {
    "auto-9": (auto_9, "RoboCop: a Auto-9"),
    "proteger-o-inocente": (proteger_o_inocente, "RoboCop: proteger o inocente"),
    "robocop-preparo": (robocop_preparo, "RoboCop: o visor varrendo (Preparo)"),
    "vivo-ou-morto": (vivo_ou_morto, "RoboCop: vivo ou morto"),
    "flecha-explosiva-rambo": (flecha_explosiva_rambo, "Rambo: a flecha explosiva"),
    "faca-de-sobrevivencia": (faca_de_sobrevivencia, "Rambo: a faca de sobrevivência"),
    "rambo-preparo": (rambo_preparo, "Rambo: a selva (Preparo)"),
    "emboscada-na-selva": (emboscada_na_selva, "Rambo: a emboscada na selva"),
    "chicotada": (chicotada, "Indiana Jones: a chicotada"),
    "pedra-rolando": (pedra_rolando, "Indiana Jones: a pedra rolando"),
    "indy-preparo": (indy_preparo, "Indiana Jones: o ídolo brilhando (Preparo)"),
    "reliquia": (reliquia, "Indiana Jones: a relíquia"),
    "bussola-magica": (bussola_magica, "Jack Sparrow: a bússola mágica"),
    "pistola-de-um-tiro": (pistola_de_um_tiro, "Jack Sparrow: a pistola de um tiro"),
    "sparrow-preparo": (sparrow_preparo, "Jack Sparrow: o mar e as velas (Preparo)"),
    "perola-negra": (perola_negra, "Jack Sparrow: a Pérola Negra"),
    "expelliarmus-harry": (expelliarmus_harry, "Harry Potter: Expelliarmus"),
    "protego": (protego, "Harry Potter: Protego"),
    "harry-preparo": (harry_preparo, "Harry Potter: a névoa prateada (Preparo)"),
    "expecto-patronum": (expecto_patronum, "Harry Potter: Expecto Patronum"),
    "crucio": (crucio, "Voldemort: Crucio"),
    "imperius": (imperius, "Voldemort: Imperius"),
    "voldemort-preparo": (voldemort_preparo, "Voldemort: a Marca Negra (Preparo)"),
    "avada-kedavra": (avada_kedavra, "Voldemort: Avada Kedavra"),
    "mu-pagina-no-relogio": (pagina_no_relogio, "Light: a página no relógio (Mecânica única)"),
}
