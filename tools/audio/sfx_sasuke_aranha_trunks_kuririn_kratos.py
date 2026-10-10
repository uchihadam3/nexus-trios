"""Os sons do Sasuke, do Homem-Aranha, do Trunks, do Kuririn e do Kratos
(veja tools/vfx/familias_v2/sasuke_aranha_trunks_kuririn.py)."""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z, nota
from som import SR, assobio, baque, env, estalo, graos, n_de, passa, poe, reverb, rosa, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _passaros(rng, seg, g=1.0):
    """O canto do Chidori: muitos estalos elétricos bem agudos e rápidos, como mil pássaros
    piando, com o chiado da eletricidade por baixo."""
    n = n_de(seg)
    x = passa(rosa(rng, n), 3000, 9000, 2) * (0.5 + 0.5 * (rng.uniform(size=n) > 0.7)) * 0.25
    x += graos(rng, n, int(seg * 90), 0.0, seg, 3500, 9000, 0.002, 0.9) * 0.6
    for k in range(int(seg * 14)):
        m = n_de(0.035)
        f0 = rng.uniform(2600, 4200)
        poe(x, seno(varre(f0, f0 * 1.35, m, 1.0), m) * env(m, 0.002, 0.025) * 0.12, rng.uniform(0, seg - 0.04))
    return x * sobe_e_some(n, 0.15, 1.2) * g


# =================================================================== Sasuke
def chidori_sasuke_mao(rng, v):
    """O Chidori juntando na mão: os mil pássaros cantando cada vez mais forte."""
    x = _passaros(rng, 1.3, 1.0)
    n = n_de(1.3)
    x += seno(varre(80, 140, n, 1.0), n) * sobe_e_some(n, 0.9, 1.0) * 0.15
    return reverb(x, 0.35, 0.2, 8000)


def chidori_sasuke(rng, v):
    """O Chidori atravessando: a corrida com o canto, o estalo do raio entrando e o trovão curto."""
    x = _z(1.5)
    poe(x, _passaros(rng, 0.3, 0.9), 0.0)
    poe(x, _whoosh(rng, 0.15, 800, 3000, 0.9, g=0.5), 0.05)
    poe(x, B.raio(rng, v) * 0.9, 0.22)
    poe(x, estalo(rng, n_de(0.08), 1500, 9000, 0.01) * 0.8, 0.22)
    poe(x, baque(n_de(0.5), 90, 40, 0.15, 0.6) * 0.7, 0.24)
    return reverb(x, 0.45, 0.22, 7000)


def mangekyo_sasuke(rng, v):
    """O Mangekyō acendendo: o tom grave e frio que gira e o "chiin" do olho abrindo."""
    n = n_de(1.1)
    t = _t(n)
    x = (seno(55, n) * 0.25 + seno(82.4 * (1 + 0.004 * np.sin(2 * math.pi * 3 * t)), n) * 0.12) * sobe_e_some(n, 0.6, 1.3)
    poe(x, _brilho(rng, 0.6, nota(74), 0.18), 0.35)
    return reverb(x, 0.55, 0.3, 6000)


def amaterasu(rng, v):
    """Amaterasu: a chama pegando de uma vez (o "fwump") e o fogo grave que não para de queimar,
    rugindo baixo, sem o estalar alegre do fogo comum."""
    x = _z(2.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 60, 900, 2) * env(n, 0.005, 0.3) * 1.0, 0.0)
    poe(x, baque(n_de(0.5), 70, 35, 0.2, 0.6) * 0.7, 0.0)
    m = n_de(1.8)
    t = _t(m)
    ronco = passa(rosa(rng, m), 40, 500, 2) * (0.7 + 0.3 * np.sin(2 * math.pi * 1.7 * t)) * sobe_e_some(m, 0.1, 1.6) * 0.8
    poe(x, ronco, 0.1)
    poe(x, seno(49, m) * sobe_e_some(m, 0.2, 1.4) * 0.12, 0.1)
    return reverb(x, 0.55, 0.3, 4000)


def genjutsu_sasuke(rng, v):
    """O Genjutsu: o olho abre com o "chiin", o mundo distorce (o tom que entorta e gira) e o eco
    confuso."""
    x = _z(1.9)
    poe(x, _brilho(rng, 0.5, nota(76), 0.2), 0.0)
    n = n_de(1.5)
    t = _t(n)
    f = 220 * (1 + 0.08 * np.sin(2 * math.pi * 1.3 * t) + 0.03 * np.sin(2 * math.pi * 5 * t))
    entorta = seno(f, n) * 0.14 + seno(f * 1.498, n) * 0.08 + seno(f * 0.5, n) * 0.1
    poe(x, entorta * sobe_e_some(n, 0.3, 1.3), 0.15)
    poe(x, B.interrupcao(rng, v) * 0.5, 0.2)
    return reverb(x, 0.75, 0.4, 5000)


# =================================================================== Homem-Aranha
def _thwip(rng, g=1.0):
    """O "thwip" do lança-teias: o clique, o jato curto que sobe e o fio zunindo."""
    x = _z(0.35)
    poe(x, estalo(rng, n_de(0.02), 2000, 8000, 0.004) * 0.6, 0.0)
    n = n_de(0.18)
    poe(x, passa(rosa(rng, n), 1200, 6000, 2) * env(n, 0.003, 0.12) * 0.7, 0.01)
    poe(x, seno(varre(900, 1800, n, 1.0), n) * env(n, 0.003, 0.1) * 0.12, 0.01)
    return x * g


def lancar_teia(rng, v):
    """Lançar teia: o thwip, o zunido da bola voando e o "splat" grudento abrindo a rede."""
    x = _z(1.3)
    poe(x, _thwip(rng), 0.0)
    poe(x, _whoosh(rng, 0.3, 1500, 500, 0.6, g=0.35), 0.1)
    n = n_de(0.35)
    poe(x, passa(rosa(rng, n), 200, 2500, 2) * env(n, 0.003, 0.25) * 0.9, 0.5)
    for k in range(6):
        poe(x, estalo(rng, n_de(0.03), 600, 3000, 0.01) * 0.25, 0.55 + 0.04 * k)
    return reverb(x, 0.35, 0.2, 7000)


def salvamento_aranha(rng, v):
    """O Salvamento: o thwip, ele passa balançando (o vento que vai e volta), pousa e a teia fecha
    o escudo."""
    x = _z(1.7)
    poe(x, _thwip(rng), 0.0)
    poe(x, _whoosh(rng, 0.45, 300, 1600, 0.5, g=0.7), 0.1)
    poe(x, baque(n_de(0.25), 140, 80, 0.05, 0.4) * 0.5, 0.6)
    poe(x, _thwip(rng, 0.7), 0.65)
    poe(x, B.escudo(rng, v) * 0.6, 0.75)
    return reverb(x, 0.45, 0.22, 7000)


def teia_de_impacto(rng, v):
    """Teia de impacto: dois thwips grossos, o tiro voando e o "SPLAT" pesado que trava o rival."""
    x = _z(1.4)
    poe(x, _thwip(rng, 1.1), 0.0)
    poe(x, _thwip(rng, 0.9), 0.08)
    poe(x, _whoosh(rng, 0.25, 1200, 400, 0.6, g=0.4), 0.15)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 100, 2000, 2) * env(n, 0.002, 0.3) * 1.1, 0.45)
    poe(x, baque(n_de(0.35), 120, 60, 0.08, 0.5) * 0.7, 0.45)
    poe(x, B.interrupcao(rng, v) * 0.4, 0.55)
    return reverb(x, 0.4, 0.2, 7000)


# =================================================================== Trunks
def espada_do_futuro(rng, v):
    """A Espada do futuro: oito cortes rápidos em sequência (o "shing" de cada um) e o brilho de
    todos juntos no fim."""
    x = _z(1.7)
    for k in range(8):
        poe(x, B.corte(rng, v) * (0.45 + 0.05 * k), 0.06 * k * 1.0)
    poe(x, _brilho(rng, 0.6, nota(84), 0.2), 0.55)
    poe(x, baque(n_de(0.4), 150, 70, 0.1, 0.5) * 0.5, 0.55)
    return reverb(x, 0.45, 0.22, 7500)


def selo_burning(rng, v):
    """Os gestos do Burning Attack: os movimentos rápidos das mãos (quatro "fup" curtos) e o ki
    juntando."""
    x = _z(0.9)
    for k in range(4):
        poe(x, _whoosh(rng, 0.08, 500, 2000, 0.8, g=0.35), 0.1 * k)
    n = n_de(0.5)
    poe(x, seno(varre(200, 500, n, 1.0), n) * sobe_e_some(n, 0.9, 1.0) * 0.15, 0.35)
    return reverb(x, 0.35, 0.2, 7000)


def burning_attack(rng, v):
    """Burning Attack: a bola de ki saindo com o rugido, voando, e a explosão de fogo."""
    x = _z(1.8)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 150, 2500, 2) * env(n, 0.01, 0.4) * 0.6, 0.0)
    poe(x, _whoosh(rng, 0.35, 400, 1200, 0.6, g=0.5), 0.05)
    poe(x, B.explosao(rng, v) * 0.9, 0.45)
    poe(x, B.fogo(rng, v) * 0.35, 0.5)
    return reverb(x, 0.5, 0.25, 6000)


def aura_trunks(rng, v):
    """A aura de Super Saiyajin: o zumbido elétrico do ki subindo e as faíscas estalando."""
    n = n_de(1.4)
    t = _t(n)
    x = passa(rosa(rng, n), 100, 1200, 2) * (0.75 + 0.25 * np.sin(2 * math.pi * 11 * t)) * 0.4
    x += seno(varre(90, 180, n, 1.0), n) * 0.12
    for _ in range(5):
        poe(x, estalo(rng, n_de(0.05), 2000, 8000, 0.01) * 0.3, rng.uniform(0.1, 1.3))
    return reverb(x * sobe_e_some(n, 0.5, 1.2), 0.4, 0.2, 7000)


def corte_final(rng, v):
    """O Corte final: o silêncio de um instante, o corte vertical enorme ("SHIIING" longo) e a luz
    rachando com o estrondo."""
    x = _z(1.8)
    n = n_de(0.5)
    poe(x, assobio(rng, n, 3000, 900, 1.0, 0.4) * env(n, 0.005, 0.4) * 0.6, 0.05)
    poe(x, B.corte_pesado(rng, v) * 1.1, 0.1)
    poe(x, _brilho(rng, 0.9, nota(86), 0.22), 0.2)
    poe(x, baque(n_de(0.8), 70, 30, 0.3, 0.9) * 0.9, 0.25)
    return reverb(x, 0.6, 0.3, 6500)


# =================================================================== Kuririn
def kienzan(rng, v):
    """Kienzan: o disco girando (o zumbido agudo de serra que sobe), voando, e o corte limpo."""
    x = _z(1.6)
    n = n_de(0.9)
    t = _t(n)
    serra = seno(varre(600, 1400, n, 1.0) * (1 + 0.01 * np.sin(2 * math.pi * 60 * t)), n) * 0.18
    serra += passa(rosa(rng, n), 2500, 7000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 30 * t)) * 0.2
    poe(x, serra * sobe_e_some(n, 0.6, 1.2), 0.0)
    poe(x, B.corte(rng, v) * 0.9, 0.8)
    poe(x, estalo(rng, n_de(0.05), 3000, 9000, 0.01) * 0.4, 0.82)
    return reverb(x, 0.4, 0.2, 7500)


def taiyoken_flash(rng, v):
    """As mãos no rosto: o grito curto (o tom subindo) antes do clarão."""
    n = n_de(0.5)
    x = (seno(varre(300, 700, n, 1.2), n) * 0.18 + seno(varre(600, 1400, n, 1.2), n) * 0.06) * env(n, 0.02, 0.4)
    return reverb(x, 0.3, 0.18, 7000)


def taiyoken(rng, v):
    """Taiyoken: o clarão branco ("FWAAAH" brilhante, como luz estourando) e o zumbido no ouvido de
    quem ficou cego."""
    x = _z(1.9)
    n = n_de(0.7)
    poe(x, passa(rosa(rng, n), 2000, 9000, 2) * env(n, 0.003, 0.6) * 0.9, 0.0)
    for k, nn in enumerate((84, 88, 91, 96)):
        poe(x, _brilho(rng, 0.7, nota(nn), 0.12), 0.02 * k)
    m = n_de(1.3)
    poe(x, seno(3800, m) * sobe_e_some(m, 0.2, 1.2) * 0.05, 0.4)
    return reverb(x, 0.55, 0.3, 9000)


def kame_kuririn_carga(rng, v):
    """O Kamehameha juntando nas mãos: o "ka-me-ha-me" do ki (o tom subindo em quatro degraus) e o
    zumbido."""
    x = _z(1.4)
    for k, f in enumerate((180, 220, 270, 330)):
        n = n_de(0.32)
        poe(x, (seno(f, n) * 0.14 + seno(f * 2, n) * 0.04) * env(n, 0.03, 0.2), 0.3 * k)
    n = n_de(1.3)
    poe(x, passa(rosa(rng, n), 300, 2500, 2) * sobe_e_some(n, 0.9, 1.0) * 0.25, 0.0)
    return reverb(x, 0.4, 0.2, 7000)


def kame_kuririn(rng, v):
    """O Kamehameha saindo: o "HAAA" do feixe (o rugido de energia) e a explosão azul."""
    x = _z(1.9)
    n = n_de(1.0)
    t = _t(n)
    feixe = passa(rosa(rng, n), 200, 3000, 2) * (0.85 + 0.15 * np.sin(2 * math.pi * 9 * t)) * 0.6 + seno(110, n) * 0.12
    poe(x, feixe * sobe_e_some(n, 0.05, 1.2), 0.0)
    poe(x, B.explosao(rng, v) * 0.8, 0.75)
    return reverb(x, 0.5, 0.25, 6500)


# =================================================================== Kratos
def laminas_kratos(rng, v):
    """As Lâminas do Caos: as correntes chacoalhando, as duas lâminas zunindo com fogo, os dois cortes
    e o sangue."""
    x = _z(1.6)
    for k in range(10):
        poe(x, estalo(rng, n_de(0.03), 1500, 6000, 0.01) * 0.25, 0.02 * k + rng.uniform(0, 0.02))
    poe(x, _whoosh(rng, 0.25, 300, 1400, 0.7, g=0.7), 0.0)
    poe(x, B.fogo(rng, v) * 0.3, 0.05)
    poe(x, B.corte_pesado(rng, v) * 0.8, 0.2)
    poe(x, _whoosh(rng, 0.25, 300, 1400, 0.7, g=0.6), 0.2)
    poe(x, B.corte_pesado(rng, v) * 0.7, 0.38)
    n = n_de(0.2)
    poe(x, passa(rosa(rng, n), 200, 1500, 2) * env(n, 0.003, 0.15) * 0.4, 0.4)
    return reverb(x, 0.45, 0.22, 6500)


def furia_kratos(rng, v):
    """A Fúria espartana: o urro grave (a voz rasgada) e o coração batendo forte."""
    x = _z(1.3)
    n = n_de(0.8)
    t = _t(n)
    f = 95 * (1 + 0.05 * np.sin(2 * math.pi * 6 * t))
    urro = (seno(f, n) * 0.3 + seno(f * 2, n) * 0.15 + seno(f * 3, n) * 0.08) * (0.7 + 0.3 * rng.uniform(size=n)) * env(n, 0.05, 0.5)
    poe(x, passa(urro, 60, 1500, 2) * 1.2, 0.0)
    for k in range(2):
        poe(x, baque(n_de(0.2), 60, 40, 0.06, 0.4) * 0.8, 0.5 + 0.3 * k)
    return reverb(x, 0.45, 0.22, 5000)


def furia_espartana(rng, v):
    """A pancada da Fúria: o avanço rápido e o soco pesado estalando."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.15, 400, 1800, 0.9, g=0.6), 0.0)
    poe(x, B.soco_pesado(rng, v) * 1.0, 0.12)
    poe(x, estalo(rng, n_de(0.05), 800, 5000, 0.01) * 0.5, 0.12)
    return reverb(x, 0.35, 0.18, 6000)


def ira_kratos(rng, v):
    """A raiva juntando antes da Ira dos deuses: o fogo crescendo e o rosnado grave subindo."""
    n = n_de(1.4)
    x = passa(rosa(rng, n), 60, 1200, 2) * 0.6
    x += seno(varre(55, 90, n, 1.0), n) * 0.18
    return reverb(x * sobe_e_some(n, 0.9, 1.0), 0.45, 0.22, 5000)


def ira_dos_deuses(rng, v):
    """A Ira dos deuses: o golpe no chão, a terra rachando e as colunas de fogo subindo rugindo."""
    x = _z(2.2)
    poe(x, baque(n_de(1.0), 55, 22, 0.4, 1.0) * 1.3, 0.0)
    poe(x, B.terremoto(rng, v) * 0.7, 0.02)
    poe(x, B.explosao(rng, v) * 0.7, 0.15)
    n = n_de(1.5)
    poe(x, passa(rosa(rng, n), 80, 2500, 2) * sobe_e_some(n, 0.2, 1.3) * 0.8, 0.2)
    poe(x, B.fogo(rng, v) * 0.5, 0.3)
    return reverb(x, 0.6, 0.3, 5000)


SONS: dict = {
    "chidori-sasuke-mao": (chidori_sasuke_mao, "o Chidori juntando na mão (mil pássaros)"),
    "chidori-sasuke": (chidori_sasuke, "Chidori: a lança de raio atravessando"),
    "mangekyo-sasuke": (mangekyo_sasuke, "o Mangekyō acendendo"),
    "amaterasu": (amaterasu, "Amaterasu: as chamas negras que não se apagam"),
    "genjutsu-sasuke": (genjutsu_sasuke, "Genjutsu: o mundo se torcendo"),
    "lancar-teia": (lancar_teia, "Lançar teia: o thwip e a rede grudando"),
    "salvamento-aranha": (salvamento_aranha, "Salvamento: o balanço na teia e o escudo"),
    "teia-de-impacto": (teia_de_impacto, "Teia de impacto: o tiro grosso e o splat"),
    "espada-do-futuro": (espada_do_futuro, "Espada do futuro: os oito cortes"),
    "selo-burning": (selo_burning, "os gestos do Burning Attack"),
    "burning-attack": (burning_attack, "Burning Attack: a bola de ki e a explosão"),
    "aura-trunks": (aura_trunks, "a aura de Super Saiyajin"),
    "corte-final": (corte_final, "Corte final: o corte vertical gigante"),
    "kienzan": (kienzan, "Kienzan: o disco serrando"),
    "taiyoken-flash": (taiyoken_flash, "as mãos no rosto antes do Taiyoken"),
    "taiyoken": (taiyoken, "Taiyoken: o clarão que cega"),
    "kame-kuririn-carga": (kame_kuririn_carga, "o Kamehameha juntando"),
    "kame-kuririn": (kame_kuririn, "Kamehameha: o feixe e a explosão"),
    "laminas-kratos": (laminas_kratos, "Lâminas do Caos: as correntes e os dois cortes"),
    "furia-kratos": (furia_kratos, "a Fúria espartana: o urro"),
    "furia-espartana": (furia_espartana, "a pancada da Fúria"),
    "ira-kratos": (ira_kratos, "a raiva juntando"),
    "ira-dos-deuses": (ira_dos_deuses, "Ira dos deuses: o chão racha e o fogo sobe"),
}
