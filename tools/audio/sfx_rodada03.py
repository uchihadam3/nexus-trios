"""Os sons da rodada 3: Mulher-Maravilha, Homem de Ferro, Capitão América, Magneto e Deadpool
(veja tools/vfx/familias_v2/rodada03.py).

Cada habilidade tem o som do impacto (o nome da família); as que voam, preparam ou disparam um
feixe têm o som de "antes" (e a "saída" do feixe)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z
from som import SR, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, serra_suave, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _clang(rng, f0=480.0, seg=1.0, g=1.0):
    """O metal batendo e tremendo (escudo, bracelete, viga)."""
    n = n_de(seg)
    t = _t(n)
    x = modal(n, f0, [1.0, 2.71, 5.2, 8.6], [1.8, 2.6, 3.8, 5.5], [0.5, 0.3, 0.2, 0.1], rng=rng) * (1 + 0.12 * np.sin(2 * math.pi * 7 * t))
    e = estalo(rng, n, 1500, 7000, 0.01)
    x[:len(e)] += e[:len(x)] * 0.6
    return x * g


def _zumbido(rng, seg, f=90.0, g=1.0):
    n = n_de(seg)
    t = _t(n)
    z = serra_suave(f * (1 + 0.008 * np.sin(2 * math.pi * 8 * t)), n, 10) * 0.5
    return (passa(satura(z, 1.6), None, 3000, 2) * 0.6 + passa(rosa(rng, n), 3000, 9000, 2) * 0.08) * g


# =================================================================== Mulher-Maravilha
def laco_saida(rng, v):
    """O Laço da Verdade lançado: a corda girando no ar ("vum vum") e o brilho dourado."""
    x = _z(0.8)
    n = n_de(0.6)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * (0.4 + 0.6 * np.sin(2 * math.pi * 6 * t) ** 2) * sobe_e_some(n, 0.4, 1.2) * 0.6, 0.0)
    poe(x, _brilho(rng, 0.5, 1800, 0.12), 0.05)
    return reverb(x, 0.35, 0.18, 7000)


def laco_da_verdade(rng, v):
    """O Laço da Verdade: a corda apertando em três puxões (o estalo da corda), o brilho mágico subindo
    e o golpe cortado."""
    x = _z(1.7)
    for k in range(3):
        poe(x, _whoosh(rng, 0.08, 600, 2500, 0.8, g=0.35), 0.2 + 0.1 * k)
        poe(x, estalo(rng, n_de(0.04), 400, 3000, 0.015) * 0.6, 0.27 + 0.1 * k)
    n = n_de(1.1)
    for f, gg in ((880, 0.08), (1320, 0.06), (1760, 0.04)):
        poe(x, seno(f, n) * sobe_e_some(n, 0.3, 1.5) * gg, 0.35)
    poe(x, B.interrupcao(rng, v) * 0.4, 0.45)
    return reverb(x, 0.55, 0.28, 7500)


def braceletes_amazona(rng, v):
    """Os braceletes: o "tchang" dos dois braceletes cruzando e três balas ricocheteando neles
    ("pium"), e o escudo firmando."""
    x = _z(1.6)
    poe(x, _clang(rng, 620, 0.8, 0.5), 0.12)
    for k in range(3):
        t0 = 0.25 + 0.1 * k
        poe(x, estalo(rng, n_de(0.03), 2000, 9000, 0.006) * 0.6, t0)
        m = n_de(0.22)
        poe(x, seno(varre(3200, 1400, m, 1.0), m) * env(m, 0.002, 0.18) * 0.14, t0 + 0.01)
    poe(x, B.escudo(rng, v) * 0.4, 0.35)
    return reverb(x, 0.45, 0.22, 7000)


def impeto_amazona(rng, v):
    """O Ímpeto amazona: a pancada do escudo, a espada cortando e o estouro dourado."""
    x = _z(1.5)
    poe(x, B.soco_pesado(rng, v) * 0.8, 0.0)
    poe(x, _clang(rng, 300, 0.6, 0.35), 0.0)
    poe(x, _whoosh(rng, 0.12, 1000, 5000, 0.7, g=0.5), 0.12)
    poe(x, B.corte(rng, v) * 0.9, 0.2)
    poe(x, B.explosao(rng, v) * 0.35, 0.36)
    poe(x, _brilho(rng, 0.6, 1500, 0.12), 0.38)
    return reverb(x, 0.45, 0.22, 6500)


# =================================================================== Homem de Ferro
def repulsor_saida(rng, v):
    """O repulsor disparando: o carregar curtinho ("uííí") e o "pchú" do disparo."""
    x = _z(0.7)
    n = n_de(0.18)
    poe(x, seno(varre(800, 2400, n, 1.4), n) * sobe_e_some(n, 0.9, 1.0) * 0.12, 0.0)
    m = n_de(0.35)
    poe(x, (passa(rosa(rng, m), 300, 5000, 2) * 0.6 + seno(varre(500, 150, m, 1.0), m) * 0.3) * env(m, 0.003, 0.3), 0.17)
    return reverb(x, 0.35, 0.18, 7000)


def repulsores_stark(rng, v):
    """O repulsor no rival: o estouro com a onda de pressão (o "vum" grave) e os estalos da armadura
    rachando."""
    x = _z(1.4)
    poe(x, B.explosao(rng, v) * 0.6, 0.0)
    poe(x, baque(n_de(0.5), 90, 40, 0.15, 0.6) * 0.9, 0.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.04), 1500, 6000, 0.01) * 0.35, 0.25 + 0.05 * k)
    return reverb(x, 0.45, 0.22, 6500)


def protocolo_de_protecao(rng, v):
    """O Protocolo de proteção: as placas da nanotecnologia encaixando uma atrás da outra (clique
    metálico rápido, cada vez mais agudo) e o zumbido do escudo ligando."""
    x = _z(1.5)
    for k in range(14):
        m = n_de(0.05)
        tt = _t(m)
        poe(x, (seno(1500 + 70 * k, m) * 0.2 + seno(3100 + 110 * k, m) * 0.1) * np.exp(-tt * 70), 0.03 * k)
        poe(x, estalo(rng, m, 3000, 9000, 0.004) * 0.12, 0.03 * k)
    n = n_de(0.8)
    poe(x, seno(varre(220, 440, n, 1.0), n) * sobe_e_some(n, 0.3, 1.4) * 0.08, 0.4)
    poe(x, B.escudo(rng, v) * 0.45, 0.45)
    return reverb(x, 0.4, 0.2, 7500)


def unibeam_carga(rng, v):
    """O reator do peito carregando: o zumbido que sobe de tom sem parar e os bips de alerta."""
    n = n_de(1.4)
    t = _t(n)
    x = _z(1.5)
    poe(x, seno(varre(150, 900, n, 1.2), n) * (t / t[-1]) * 0.12 + _zumbido(rng, 1.4, 70, 0.5) * (t / t[-1]) ** 1.5, 0.0)
    for k in range(4):
        b = n_de(0.06)
        poe(x, seno(1800, b) * env(b, 0.002, 0.05) * 0.1, 0.4 + 0.25 * k)
    return reverb(x, 0.4, 0.2, 7000)


def unibeam_feixe(rng, v):
    """O Unibeam saindo: o feixe largo rugindo, grave e brilhante ao mesmo tempo."""
    m = n_de(1.1)
    t = _t(m)
    x = (passa(rosa(rng, m), 120, 5000, 2) * (0.8 + 0.2 * np.sin(2 * math.pi * 10 * t)) * 0.7 + seno(75, m) * 0.15 + seno(1100, m) * 0.03) * sobe_e_some(m, 0.04, 1.3)
    return reverb(x + graos(rng, m, 30, 0.0, 1.0, 2500, 9000, 0.003, 0.8) * 0.25, 0.45, 0.22, 6500)


def unibeam_impacto(rng, v):
    """O Unibeam no rival: a explosão grande e o chiado do metal derretendo."""
    x = _z(1.6)
    poe(x, B.explosao(rng, v) * 1.0, 0.0)
    n = n_de(1.0)
    poe(x, passa(rosa(rng, n), 2500, 8000, 2) * env(n, 0.02, 0.8) * 0.2, 0.1)
    return reverb(x, 0.55, 0.28, 6000)


# =================================================================== Capitão América
def escudo_ricochete_saida(rng, v):
    """O escudo arremessado no ricochete: o "fuuu" do disco girando."""
    n = n_de(0.5)
    t = _t(n)
    x = passa(rosa(rng, n), 500, 4000, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 14 * t) ** 2) * sobe_e_some(n, 0.3, 1.3) * 0.7
    return reverb(x, 0.3, 0.15, 7000)


def escudo_ricochete(rng, v):
    """O escudo quicando nos rivais: três "PLANG" de metal um atrás do outro (cada um num tom), e o
    golpe cortado."""
    x = _z(1.6)
    for k, f in enumerate((520, 600, 690)):
        poe(x, _clang(rng, f, 0.6, 0.55), 0.26 * k)
        poe(x, B.soco_pesado(rng, v) * 0.35, 0.26 * k)
    poe(x, B.interrupcao(rng, v) * 0.35, 0.1)
    return reverb(x, 0.5, 0.25, 6500)


def dia_todo(rng, v):
    """Eu posso o dia todo: o escudo erguido com o "CLANG" firme, o acorde que sobe (a determinação) e
    a cura brilhando."""
    x = _z(1.8)
    poe(x, _clang(rng, 420, 1.2, 0.7), 0.15)
    n = n_de(1.2)
    for f, gg in ((262, 0.08), (330, 0.06), (392, 0.06), (523, 0.04)):
        poe(x, seno(f, n) * sobe_e_some(n, 0.35, 1.4) * gg, 0.25)
    poe(x, B.cura(rng, v) * 0.35, 0.45)
    return reverb(x, 0.55, 0.28, 6500)


def avante(rng, v):
    """Avante!: a fanfarra curta (três notas de metal subindo), o vento correndo para a frente e o
    estalo da estrela."""
    x = _z(1.6)
    for k, f in enumerate((392, 523, 659)):
        m = n_de(0.35 if k < 2 else 0.7)
        nota = (serra_suave(f, m, 8) * 0.5) * env(m, 0.01, 0.3 if k < 2 else 0.6)
        poe(x, passa(nota, None, 3500, 2) * 0.18, 0.12 * k)
    n = n_de(0.9)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * sobe_e_some(n, 0.4, 1.3) * 0.4, 0.3)
    poe(x, _brilho(rng, 0.5, 2200, 0.1), 0.36)
    return reverb(x, 0.5, 0.25, 7000)


# =================================================================== Magneto
def prisao_magnetica(rng, v):
    """A Prisão magnética: o zumbido magnético (o "uóuóuó" grave) e os aros de metal fechando com três
    "clanc" secos, e o golpe cortado."""
    x = _z(1.6)
    n = n_de(1.2)
    t = _t(n)
    poe(x, seno(70 * (1 + 0.15 * np.sin(2 * math.pi * 6 * t)), n) * sobe_e_some(n, 0.3, 1.3) * 0.25 + _zumbido(rng, 1.2, 55, 0.3) * sobe_e_some(n, 0.3, 1.3), 0.0)
    for k in range(3):
        poe(x, _clang(rng, 260 + 30 * k, 0.5, 0.4), 0.22 + 0.05 * k)
    poe(x, B.interrupcao(rng, v) * 0.35, 0.3)
    return reverb(x, 0.5, 0.25, 5500)


def muralha_de_metal(rng, v):
    """A Muralha de metal: as vigas voando ("vuum") e empilhando uma a uma com baques metálicos
    pesados, e o zumbido do campo segurando."""
    x = _z(1.8)
    for k in range(5):
        t0 = 0.05 + 0.08 * k
        poe(x, _whoosh(rng, 0.12, 200, 1500, 0.8, g=0.3), t0)
        poe(x, _clang(rng, 180 + 15 * k, 0.5, 0.35), t0 + 0.11)
        poe(x, baque(n_de(0.3), 80, 40, 0.1, 0.4) * 0.5, t0 + 0.11)
    n = n_de(0.9)
    poe(x, _zumbido(rng, 0.9, 60, 0.25) * sobe_e_some(n, 0.3, 1.3), 0.5)
    poe(x, B.escudo(rng, v) * 0.3, 0.55)
    return reverb(x, 0.5, 0.25, 5500)


def campo_magneto(rng, v):
    """O Magneto erguendo o campo: o zumbido magnético que pulsa e os pedaços de metal rangendo e
    tilintando no ar."""
    n = n_de(1.6)
    t = _t(n)
    x = _z(1.7)
    poe(x, seno(60 * (1 + 0.2 * np.sin(2 * math.pi * 2 * t)), n) * sobe_e_some(n, 0.6, 1.3) * 0.25 + _zumbido(rng, 1.6, 48, 0.3) * sobe_e_some(n, 0.6, 1.3), 0.0)
    for k in range(8):
        m = n_de(0.15)
        tt = _t(m)
        poe(x, seno(rng.uniform(900, 2200), m) * np.exp(-tt * 25) * 0.05, rng.uniform(0.1, 1.4))
    return reverb(x, 0.5, 0.25, 5500)


def colapso_magneto(rng, v):
    """O Colapso: o metal rangendo enquanto vem (o "créééc" que sobe), o esmagamento enorme e a onda
    grave que deixa lento."""
    x = _z(2.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n) * (0.6 + 0.4 * np.sin(2 * math.pi * 30 * _t(n))), 300, 2500, 2) * sobe_e_some(n, 0.9, 1.0) * 0.5, 0.0)
    poe(x, _clang(rng, 150, 1.0, 0.6), 0.3)
    poe(x, _clang(rng, 230, 0.8, 0.4), 0.3)
    poe(x, B.soco_pesado(rng, v) * 1.0, 0.3)
    poe(x, B.terremoto(rng, v) * 0.5, 0.3)
    m = n_de(1.0)
    poe(x, seno(varre(110, 45, m, 1.0), m) * env(m, 0.01, 0.9) * 0.3, 0.4)
    return reverb(x, 0.6, 0.3, 5000)


# =================================================================== Deadpool
def plano_que_plano(rng, v):
    """Plano? Que plano?: quatro tiros de pistola, o "plim plim" da granada quicando, um assobio de
    desenho e o "BUM"."""
    x = _z(2.0)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.06), 400, 6000, 0.02) * 0.9, 0.064 * k)
        poe(x, baque(n_de(0.12), 160, 80, 0.04, 0.6) * 0.4, 0.064 * k)
    for k in range(2):
        m = n_de(0.12)
        poe(x, seno(1300 - 200 * k, m) * np.exp(-_t(m) * 30) * 0.15, 0.28 + 0.07 * k)
    m = n_de(0.25)
    poe(x, seno(varre(1600, 700, m, 1.0), m) * env(m, 0.01, 0.2) * 0.08, 0.36)
    poe(x, B.explosao(rng, v) * 0.9, 0.4)
    return reverb(x, 0.5, 0.25, 6500)


def quarta_parede(rng, v):
    """A Quarta parede: o vidro do quadro rachando ("créc"), estilhaçando, e o "boing" bobo de desenho
    animado que entorta (confuso)."""
    x = _z(1.7)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.04), 2500, 9000, 0.006) * 0.4, 0.2 + 0.03 * k)
    poe(x, graos(rng, n_de(0.6), 60, 0.0, 0.6, 3000, 11000, 0.004, 0.8) * 0.4, 0.35)
    m = n_de(0.7)
    t = _t(m)
    poe(x, seno(300 * (1 + 0.35 * np.sin(2 * math.pi * 7 * t) * np.exp(-t * 3)), m) * env(m, 0.005, 0.6) * 0.18, 0.75)
    poe(x, B.interrupcao(rng, v) * 0.2, 0.4)
    return reverb(x, 0.45, 0.22, 7000)


def so_um_arranhao(rng, v):
    """Só um arranhão: o "plec" do band-aid colando, o "rrrip" dele descolando e o borbulhar da
    regeneração."""
    x = _z(1.8)
    poe(x, estalo(rng, n_de(0.05), 500, 3000, 0.02) * 0.5, 0.02)
    poe(x, baque(n_de(0.1), 220, 120, 0.04, 0.3) * 0.3, 0.02)
    n = n_de(0.25)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.5 + 0.5 * (rng.uniform(size=n) > 0.5)) * env(n, 0.01, 0.2) * 0.4, 0.5)
    for k in range(10):
        m = n_de(0.07)
        poe(x, seno(varre(rng.uniform(400, 700), rng.uniform(900, 1400), m, 1.0), m) * env(m, 0.003, 0.05) * 0.1, 0.6 + 0.08 * k + rng.uniform(0, 0.03))
    poe(x, B.cura(rng, v) * 0.3, 0.7)
    return reverb(x, 0.4, 0.2, 6500)


SONS: dict = {
    "laco-saida": (laco_saida, "Laço da Verdade: a corda girando no ar"),
    "laco-da-verdade": (laco_da_verdade, "Laço da Verdade: a corda apertando e a magia"),
    "braceletes-amazona": (braceletes_amazona, "Braceletes: as balas ricocheteando"),
    "impeto-amazona": (impeto_amazona, "Ímpeto amazona: escudo, espada e o estouro"),
    "repulsor-saida": (repulsor_saida, "Repulsores: o disparo"),
    "repulsores-stark": (repulsores_stark, "Repulsores: o estouro no rival"),
    "protocolo-de-protecao": (protocolo_de_protecao, "Protocolo de proteção: as placas encaixando"),
    "unibeam-carga": (unibeam_carga, "Unibeam: o reator carregando"),
    "unibeam-feixe": (unibeam_feixe, "Unibeam: o feixe rugindo"),
    "unibeam-impacto": (unibeam_impacto, "Unibeam: a explosão no rival"),
    "escudo-ricochete-saida": (escudo_ricochete_saida, "Escudo ricochete: o arremesso"),
    "escudo-ricochete": (escudo_ricochete, "Escudo ricochete: os três clangs"),
    "dia-todo": (dia_todo, "Eu posso o dia todo: o escudo e a determinação"),
    "avante": (avante, "Avante: a fanfarra e o vento"),
    "prisao-magnetica": (prisao_magnetica, "Prisão magnética: o zumbido e os aros"),
    "muralha-de-metal": (muralha_de_metal, "Muralha de metal: as vigas empilhando"),
    "campo-magneto": (campo_magneto, "Magneto erguendo o campo (Preparo)"),
    "colapso-magneto": (colapso_magneto, "Colapso: o metal esmagando"),
    "plano-que-plano": (plano_que_plano, "Plano? Que plano?: tiros, granada e BUM"),
    "quarta-parede": (quarta_parede, "Quarta parede: o quadro quebrando"),
    "so-um-arranhao": (so_um_arranhao, "Só um arranhão: o band-aid e a regeneração"),
}
