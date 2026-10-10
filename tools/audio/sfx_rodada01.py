"""Os sons da rodada 1: Vegeta, Gojo, Light, Pikachu e Saitama (veja tools/vfx/familias_v2/rodada01.py).

Cada habilidade tem o som do impacto (o nome da família); as que juntam energia antes têm o som de
"antes" (sai junto com a folha de ergue) e as de feixe têm o som da "saída" (o feixe rugindo)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, nota
from som import CRISTAL, SR, assobio, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, serra_suave, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _zumbido_eletrico(rng, seg, f=60.0, g=1.0):
    """O zumbido de energia elétrica: a serra grave saturada que treme, com o chiado por cima."""
    n = n_de(seg)
    t = _t(n)
    z = serra_suave(f * (1 + 0.01 * np.sin(2 * math.pi * 7 * t)), n, 12) * 0.5
    z = passa(satura(z, 2.0), None, 2500, 2) * 0.6
    z += passa(rosa(rng, n), 2500, 9000, 2) * (0.5 + 0.5 * (rng.uniform(size=n) > 0.6)) * 0.12
    return z * g


def _estalos(rng, x, n, t0, t1, g=0.3, f0=1500, f1=8000):
    for _ in range(n):
        poe(x, estalo(rng, n_de(0.04), f0, f1, 0.01) * g * rng.uniform(0.5, 1), rng.uniform(t0, t1))


# =================================================================== Vegeta
def galick_gun_carga(rng, v):
    """A Galick Gun juntando: o zumbido roxo, grave e escuro, subindo, e os estalos dos raios em volta."""
    n = n_de(1.0)
    t = _t(n)
    x = _zumbido_eletrico(rng, 1.0, 55.0, 0.8) * sobe_e_some(n, 0.85, 1.0)
    x += seno(varre(110, 220, n, 1.2), n) * sobe_e_some(n, 0.9, 1.0) * 0.12
    _estalos(rng, x, 10, 0.1, 0.95, 0.3)
    _ = t
    return reverb(x, 0.35, 0.2, 6000)


def galick_gun_feixe(rng, v):
    """A Galick Gun saindo: o "GALICK… HAAA" — o feixe rugindo grave com a eletricidade crepitando."""
    n = n_de(1.1)
    t = _t(n)
    x = passa(rosa(rng, n), 100, 2200, 2) * (0.85 + 0.15 * np.sin(2 * math.pi * 11 * t)) * 0.65
    x += _zumbido_eletrico(rng, 1.1, 50.0, 0.5)
    _estalos(rng, x, 14, 0.0, 1.0, 0.25)
    return reverb(x * sobe_e_some(n, 0.04, 1.2), 0.45, 0.22, 6000)


def galick_gun(rng, v):
    """A Galick Gun no rival: a explosão roxa e os raios estalando saindo dela."""
    x = _z(1.6)
    poe(x, B.explosao(rng, v) * 0.9, 0.0)
    poe(x, B.raio(rng, v) * 0.45, 0.02)
    _estalos(rng, x, 8, 0.05, 0.6, 0.3)
    return reverb(x, 0.5, 0.25, 6000)


def nao_vou_cair(rng, v):
    """"Não vou cair": o grito do Vegeta virando Super Saiyajin — o chão roncando, a aura subindo
    num "vuum" que cresce, os raios estalando e o estouro final do ki."""
    x = _z(2.0)
    n = n_de(1.5)
    t = _t(n)
    poe(x, passa(rosa(rng, n), 30, 300, 2) * sobe_e_some(n, 0.6, 1.2) * 0.8, 0.0)
    f = varre(120, 200, n, 1.0)
    grito = (seno(f, n) * 0.3 + seno(f * 2, n) * 0.14 + seno(f * 3, n) * 0.07) * (0.75 + 0.25 * rng.uniform(size=n)) * sobe_e_some(n, 0.5, 1.3)
    poe(x, passa(grito, 80, 2200, 2) * 0.6, 0.1)
    poe(x, assobio(rng, n_de(1.2), 200, 1500, 1.0, 0.4) * sobe_e_some(n_de(1.2), 0.8, 1.2) * 0.5, 0.2)
    _estalos(rng, x, 10, 0.4, 1.6, 0.35)
    poe(x, B.transformacao(rng, v) * 0.6, 1.1)
    return reverb(x, 0.55, 0.28, 5500)


def final_flash_carga(rng, v):
    """O Final Flash juntando: dois zumbidos, um em cada mão, correndo um para o outro (os tons se
    aproximando até virar um só) e o brilho crescendo."""
    n = n_de(1.2)
    t = _t(n)
    junta = np.clip(t / 0.8, 0, 1)
    f1, f2 = 220 * (1 - 0.25 * junta), 330 * (1 - 0.5 * junta)
    x = (seno(f1, n) * 0.16 + seno(f2, n) * 0.12) * sobe_e_some(n, 0.7, 1.1)
    x += passa(rosa(rng, n), 600, 5000, 2) * sobe_e_some(n, 0.9, 1.0) * 0.25
    poe(x, _brilho(rng, 0.5, nota(86), 0.18, CRISTAL), 0.8)
    return reverb(x, 0.4, 0.22, 7000)


def final_flash_feixe(rng, v):
    """O Final Flash saindo: o "FLAAASH" enorme — o rugido largo, grave e brilhante, e o ar tremendo."""
    n = n_de(1.3)
    t = _t(n)
    x = passa(rosa(rng, n), 60, 4000, 2) * (0.85 + 0.15 * np.sin(2 * math.pi * 7 * t)) * 0.9
    x += seno(55, n) * 0.18 + seno(110, n) * 0.08
    x += passa(rosa(rng, n), 3000, 9000, 2) * 0.15
    return reverb(x * sobe_e_some(n, 0.03, 1.2), 0.5, 0.25, 6000)


def final_flash(rng, v):
    """O Final Flash no rival: a explosão gigante, o estrondo que rola e o chiado da luz sumindo."""
    x = _z(2.2)
    poe(x, B.explosao(rng, v) * 1.1, 0.0)
    poe(x, baque(n_de(1.2), 50, 20, 0.5, 1.2) * 1.2, 0.0)
    n = n_de(1.6)
    poe(x, passa(rosa(rng, n), 40, 600, 2) * sobe_e_some(n, 0.05, 1.4) * 0.7, 0.05)
    return reverb(x, 0.6, 0.3, 5000)


# =================================================================== Gojo
def azul_gojo(rng, v):
    """O Azul: o som sendo sugado — um "vuuup" ao contrário que cresce para dentro, o tom grave que
    desce e se aperta, e o "tum" seco quando tudo se junta no ponto."""
    x = _z(1.6)
    n = n_de(0.9)
    t = _t(n)
    puxa = passa(rosa(rng, n), 200, 4000, 2) * (t / t[-1]) ** 2.5 * 0.8
    poe(x, puxa, 0.0)
    poe(x, seno(varre(400, 90, n, 0.7), n) * (t / t[-1]) ** 1.5 * 0.18, 0.0)
    poe(x, baque(n_de(0.4), 90, 45, 0.08, 0.5) * 0.9, 0.88)
    poe(x, _brilho(rng, 0.5, nota(81), 0.12, CRISTAL), 0.9)
    return reverb(x, 0.45, 0.25, 7000)


def vermelho_gojo_saida(rng, v):
    """O Vermelho saindo do dedo: o estalo seco e o zumbido apertado da bola voando."""
    x = _z(0.6)
    poe(x, estalo(rng, n_de(0.04), 1000, 7000, 0.006) * 0.8, 0.0)
    n = n_de(0.5)
    poe(x, seno(varre(700, 900, n, 1.0), n) * env(n, 0.005, 0.4) * 0.15 + passa(rosa(rng, n), 800, 4000, 2) * env(n, 0.005, 0.4) * 0.2, 0.0)
    return reverb(x, 0.3, 0.15, 7000)


def vermelho_gojo(rng, v):
    """O Vermelho estourando: o "BUUM" que empurra (o estrondo seco e grave), o ar sendo jogado para
    fora num "fuuush" e as lascas batendo longe."""
    x = _z(1.6)
    poe(x, baque(n_de(0.7), 70, 28, 0.2, 0.8) * 1.3, 0.0)
    poe(x, B.explosao(rng, v) * 0.7, 0.0)
    poe(x, _whoosh(rng, 0.45, 1500, 300, 0.4, g=0.7), 0.03)
    _estalos(rng, x, 8, 0.25, 0.8, 0.25, 300, 3000)
    return reverb(x, 0.5, 0.25, 6000)


def vazio_infinito_selo(rng, v):
    """O sinal de mão do Domínio: o estalo dos dedos cruzando e o silêncio que se abre (o ar sumindo)."""
    x = _z(1.0)
    poe(x, estalo(rng, n_de(0.05), 600, 5000, 0.008) * 0.7, 0.0)
    n = n_de(0.8)
    poe(x, passa(rosa(rng, n), 300, 3000, 2) * np.linspace(1, 0, n) ** 2 * 0.4, 0.02)
    poe(x, seno(varre(400, 200, n, 1.0), n) * env(n, 0.05, 0.6) * 0.1, 0.1)
    return reverb(x, 0.6, 0.35, 7000)


def vazio_infinito(rng, v):
    """O Vazio Infinito: o acorde do infinito (muitas vozes graves e agudas, paradas no ar), o brilho
    das estrelas piscando e a informação correndo em ondas de chiado — ninguém se mexe."""
    n = n_de(2.4)
    t = _t(n)
    x = sum(seno(nota(nn) * (1 + 0.003 * np.sin(2 * math.pi * 0.3 * t + k)), n) * g for k, (nn, g) in enumerate(((36, 0.16), (43, 0.1), (55, 0.07), (74, 0.05), (79, 0.04), (86, 0.03))))
    x = x * sobe_e_some(n, 0.2, 1.1)
    x += graos(rng, n, 30, 0.1, 2.3, 3000, 9000, 0.004, 0.5) * 0.25
    for k in range(4):
        m = n_de(0.5)
        poe(x, passa(rosa(rng, m), 1500, 7000, 2) * sobe_e_some(m, 0.5, 1.5) * 0.15, 0.4 + 0.45 * k)
    return reverb(x, 0.85, 0.45, 6000)


# =================================================================== Light
def investigacao_light(rng, v):
    """A Investigação: o "tic" da mira fechando, a leitura varrendo (um tom fino que desce devagar),
    as teclas dos dados e o "plim" grave de quando acha."""
    x = _z(1.7)
    for k in range(4):
        poe(x, estalo(rng, n_de(0.02), 2500, 7000, 0.003) * 0.35, 0.04 * k)
    n = n_de(0.7)
    poe(x, seno(varre(1600, 900, n, 1.0), n) * env(n, 0.05, 0.4) * 0.06, 0.3)
    for k in range(10):
        poe(x, estalo(rng, n_de(0.015), 3000, 8000, 0.002) * 0.15, 0.25 + 0.06 * k + rng.uniform(0, 0.03))
    poe(x, _brilho(rng, 0.6, nota(67), 0.16), 1.1)
    return reverb(x, 0.4, 0.22, 7000)


def xeque_light(rng, v):
    """"Tudo conforme o plano": a peça de madeira batendo no tabuleiro ("toc" seco e oco), o tom
    sombrio de piano que desce e o carimbo da marca."""
    x = _z(1.9)
    poe(x, modal(n_de(0.35), 180, [1.0, 2.33, 5.0], [0.06, 0.04, 0.02], [1.0, 0.5, 0.25]) * 0.8, 0.22)
    poe(x, estalo(rng, n_de(0.03), 1500, 5000, 0.005) * 0.5, 0.22)
    for k, nn in enumerate((57, 53, 50)):
        m = n_de(0.8)
        tt = _t(m)
        f = nota(nn)
        poe(x, (seno(f, m) + seno(f * 2, m) * 0.3 + seno(f * 3, m) * 0.1) * np.exp(-tt * 3.5) * 0.18, 0.5 + 0.2 * k)
    poe(x, baque(n_de(0.25), 140, 80, 0.04, 0.4) * 0.5, 1.15)
    return reverb(x, 0.55, 0.3, 5000)


# =================================================================== Pikachu
def bochechas_pikachu(rng, v):
    """As bochechas carregando: estalinhos elétricos curtos, cada vez mais rápidos e altos, e o zumbido
    fino subindo ("pika… pika…")."""
    n = n_de(1.0)
    x = _z(1.0)
    tt = 0.0
    passo = 0.18
    while tt < 0.95:
        poe(x, estalo(rng, n_de(0.03), 2500, 9000, 0.004) * (0.2 + 0.4 * tt), tt)
        tt += passo
        passo = max(0.03, passo * 0.82)
    poe(x, seno(varre(800, 2400, n, 1.0), n) * sobe_e_some(n, 0.9, 1.0) * 0.06, 0.0)
    return reverb(x, 0.3, 0.15, 8000)


def trovao_feixe(rng, v):
    """O Choque do Trovão saindo: a descarga contínua, o zumbido elétrico alto e os estalos."""
    n = n_de(0.9)
    x = _zumbido_eletrico(rng, 0.9, 90.0, 0.8)
    _estalos(rng, x, 16, 0.0, 0.85, 0.35, 2000, 9000)
    return reverb(x * sobe_e_some(n, 0.03, 1.3), 0.35, 0.18, 8000)


def choque_do_trovao(rng, v):
    """O Choque do Trovão no rival: o trovão estalando seco e forte, o ronco depois e os estalos
    dançando no corpo."""
    x = _z(1.7)
    poe(x, B.raio(rng, v) * 1.0, 0.0)
    poe(x, baque(n_de(0.9), 60, 30, 0.3, 0.9) * 0.9, 0.02)
    n = n_de(1.1)
    poe(x, passa(rosa(rng, n), 40, 400, 2) * sobe_e_some(n, 0.1, 1.4) * 0.5, 0.08)
    _estalos(rng, x, 12, 0.1, 0.9, 0.3, 2000, 9000)
    return reverb(x, 0.5, 0.25, 6500)


def onda_de_choque_saida(rng, v):
    """A Onda de Choque saindo: o "uuóm" elétrico que ondula, mais leve que o trovão."""
    n = n_de(0.6)
    t = _t(n)
    x = seno(300 * (1 + 0.15 * np.sin(2 * math.pi * 9 * t)), n) * env(n, 0.01, 0.45) * 0.18
    x += _zumbido_eletrico(rng, 0.6, 110.0, 0.25) * env(n, 0.01, 0.45)
    return reverb(x, 0.3, 0.15, 7000)


def onda_de_choque_pikachu(rng, v):
    """A Onda de Choque prendendo: os anéis zumbindo e apertando (o tom pulsando cada vez mais rápido)
    e os estalos de quem ficou paralisado."""
    n = n_de(1.4)
    t = _t(n)
    vel = 6 + 14 * t / t[-1]
    fase = 2 * math.pi * np.cumsum(vel) / SR
    x = seno(220, n) * (0.5 + 0.5 * np.sin(fase)) * sobe_e_some(n, 0.2, 1.3) * 0.2
    x += _zumbido_eletrico(rng, 1.4, 80.0, 0.3) * sobe_e_some(n, 0.2, 1.3)
    _estalos(rng, x, 10, 0.3, 1.3, 0.3)
    return reverb(x, 0.35, 0.18, 7000)


def agilidade_pikachu(rng, v):
    """A Agilidade: três "fiuu" rápidos passando em volta (como algo correndo em círculo), o brilho e
    um estalinho elétrico."""
    x = _z(1.3)
    for k in range(3):
        poe(x, _whoosh(rng, 0.16, 800, 3000, 0.9, g=0.55), 0.12 * k)
    poe(x, _brilho(rng, 0.5, nota(84), 0.12, CRISTAL), 0.4)
    poe(x, estalo(rng, n_de(0.03), 3000, 9000, 0.004) * 0.3, 0.45)
    return reverb(x, 0.4, 0.2, 8000)


# =================================================================== Saitama
def passo_lateral(rng, v):
    """O Passo lateral: o passo leve no chão, a capa batendo no vento (o "flap" de pano) e o escudo
    firmando com um "tum" calmo."""
    x = _z(1.3)
    poe(x, baque(n_de(0.15), 160, 100, 0.03, 0.4) * 0.5, 0.0)
    for k in range(3):
        m = n_de(0.09)
        poe(x, passa(rosa(rng, m), 300, 2500, 2) * env(m, 0.005, 0.07) * (0.6 - 0.12 * k), 0.08 + 0.07 * k)
    poe(x, _whoosh(rng, 0.3, 400, 1500, 0.6, g=0.5), 0.05)
    poe(x, B.escudo(rng, v) * 0.5, 0.55)
    return reverb(x, 0.35, 0.2, 6000)


SONS: dict = {
    "galick-gun-carga": (galick_gun_carga, "Galick Gun: a energia roxa juntando"),
    "galick-gun-feixe": (galick_gun_feixe, "Galick Gun: o feixe saindo"),
    "galick-gun": (galick_gun, "Galick Gun: a explosão roxa"),
    "nao-vou-cair": (nao_vou_cair, "Não vou cair: o grito e a aura de Super Saiyajin"),
    "final-flash-carga": (final_flash_carga, "Final Flash: as duas mãos juntando a energia"),
    "final-flash-feixe": (final_flash_feixe, "Final Flash: o feixe gigante"),
    "final-flash": (final_flash, "Final Flash: a explosão gigante"),
    "azul-gojo": (azul_gojo, "Azul: tudo sendo sugado"),
    "vermelho-gojo-saida": (vermelho_gojo_saida, "Vermelho: o estalo do dedo"),
    "vermelho-gojo": (vermelho_gojo, "Vermelho: o estouro que empurra"),
    "vazio-infinito-selo": (vazio_infinito_selo, "Vazio Infinito: o sinal de mão"),
    "vazio-infinito": (vazio_infinito, "Vazio Infinito: o acorde do infinito"),
    "investigacao-light": (investigacao_light, "Investigação: a mira e a leitura"),
    "xeque-light": (xeque_light, "Tudo conforme o plano: a peça no tabuleiro"),
    "bochechas-pikachu": (bochechas_pikachu, "Pikachu: as bochechas carregando"),
    "trovao-feixe": (trovao_feixe, "Choque do Trovão: a descarga"),
    "choque-do-trovao": (choque_do_trovao, "Choque do Trovão: o trovão no rival"),
    "onda-de-choque-saida": (onda_de_choque_saida, "Onda de Choque: a onda saindo"),
    "onda-de-choque-pikachu": (onda_de_choque_pikachu, "Onda de Choque: os anéis prendendo"),
    "agilidade-pikachu": (agilidade_pikachu, "Agilidade: os rastros correndo em volta"),
    "passo-lateral": (passo_lateral, "Passo lateral: a capa e o escudo"),
}
