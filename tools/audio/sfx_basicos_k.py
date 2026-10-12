"""Sons dos ataques básicos, lote k (veja tools/vfx/familias_v2/basicos_k.py).

O chiado da arma congelante e o gelo estalando, o estalo da vinha, a bola de neve que espatifa, a lambida
molhada do Gengar com a risadinha, o "HA!" do kiai, o "Katsu!" da argila, o "vumm" da bolha de força, o
"tsiu" do Tsubaki, o cajado e o sininho da Cetra, a água estalando, as bolhas estourando, as pétalas
assobiando, o soco em chamas, o soco com trovão e o braço de borracha do Jake. Tudo sintetizado.
"""
from __future__ import annotations

import math

import numpy as np

import generate_sfx_v2 as B
from sfx_familias import _brilho, _whoosh, _z
from som import CRISTAL, METAL, SINO, SR, VIDRO, baque, env, estalo, graos, modal, n_de, passa, poe, reverb, rosa, satura, seno, sobe_e_some, varre


def _t(n):
    return np.arange(n) / SR


def _acerto(rng, g=1.0, f=110, lo=1200, hi=5200):
    """O contato de um golpe: o tapa, o corpo e o peso."""
    x = _z(0.25)
    poe(x, B._tapa(rng, n_de(0.08), lo, hi, 0.01) * 0.9 * g, 0.0)
    poe(x, B._carne(rng, n_de(0.12), 0.035, 2.4) * 0.8 * g, 0.0)
    poe(x, B._baque_seco(rng, n_de(0.2), f, 0.06) * 0.6 * g, 0.0)
    return x


def _splash(rng, seg=0.35, g=0.4, lo=400, hi=6000):
    n = n_de(seg)
    return (passa(rosa(rng, n), lo, hi, 2) * env(n, 0.002, seg * 0.5) + graos(rng, n, 30, 0.0, seg * 0.8, 1500, 7000, 0.004) * 0.5) * g


def _mola(seg, f0, prof=0.4, vel=11.0, g=0.15):
    n = n_de(seg)
    t = _t(n)
    f = f0 * (1 + prof * np.sin(2 * math.pi * vel * t) * np.exp(-t * 5))
    return np.sin(2 * math.pi * np.cumsum(f) / SR) * env(n, 0.003, seg * 0.6) * g


# =================================================================== Senhor Frio
def jato_criogenico(rng, v):
    """O jato da arma congelante: o chiado frio de gás sob pressão, e o gelo estalando e cristalizando no rival
    (os tinidos de vidro que crescem)."""
    x = _z(1.0)
    n = n_de(0.4)
    poe(x, passa(rosa(rng, n), 3000, 11000, 2) * sobe_e_some(n, 0.15, 1.3) * 0.4, 0.0)
    poe(x, seno(varre(1800, 1200, n, 1.0), n) * sobe_e_some(n, 0.2, 1.3) * 0.03, 0.0)
    poe(x, graos(rng, n_de(0.5), 30, 0.0, 0.4, 2500, 9000, 0.004) * 0.4, 0.2)
    for k in range(4):
        poe(x, _brilho(rng, 0.4, 2600 + 400 * k, 0.06, VIDRO), 0.22 + 0.05 * k)
    poe(x, _acerto(rng, 0.5, 140), 0.2)
    return reverb(x, 0.4, 0.2)


# =================================================================== Hera Venenosa
def chicote_de_vinha(rng, v):
    """O chicote de vinha: o farfalhar das folhas no ar, o estalo do chicote e o "puff" dos esporos."""
    x = _z(1.0)
    poe(x, graos(rng, n_de(0.3), 30, 0.0, 0.28, 2000, 7000, 0.004) * 0.3, 0.0)
    poe(x, _whoosh(rng, 0.25, 600, 3000, 0.8, 1.3, 0.4), 0.02)
    poe(x, estalo(rng, n_de(0.04), 2000, 9000, 0.006) * 0.9, 0.28)
    poe(x, _acerto(rng, 0.45, 150), 0.28)
    m = n_de(0.4)
    poe(x, passa(rosa(rng, m), 300, 2500, 2) * env(m, 0.01, 0.2) * 0.25, 0.32)
    return reverb(x, 0.35, 0.18)


# =================================================================== Homem de Gelo
def bola_de_neve(rng, v):
    """A bola de neve: o arremesso curto e o "pof" fofo e esmagado da neve espatifando."""
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.25, 900, 2200, 0.7, 1.3, 0.3), 0.02)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 200, 3500, 2) * env(n, 0.002, 0.12) * 0.7, 0.3)
    poe(x, graos(rng, n, 40, 0.0, 0.2, 1500, 6000, 0.005) * 0.4, 0.3)
    poe(x, B._baque_seco(rng, n_de(0.2), 120, 0.05) * 0.5, 0.3)
    return reverb(x, 0.3, 0.15)


# =================================================================== Gengar
def lambida_fantasma(rng, v):
    """A lambida do Gengar: o "slurp" molhado e comprido, a risadinha de fantasma (o "khe-khe-khe" agudo) e o
    arrepio (o tremolo frio)."""
    x = _z(1.1)
    n = n_de(0.35)
    t = _t(n)
    slurp = passa(rosa(rng, n), 300, 2500, 2) * (0.5 + 0.5 * np.sin(2 * math.pi * 18 * t)) + seno(varre(300, 700, n, 1.0), n) * 0.2
    poe(x, slurp * sobe_e_some(n, 0.5, 1.3) * 0.45, 0.05)
    for k in range(3):
        m = n_de(0.07)
        poe(x, (seno(varre(1100, 900, m, 1.0), m) + passa(rosa(rng, m), 1500, 4000, 2) * 0.4) * env(m, 0.004, 0.05) * 0.07, 0.45 + 0.09 * k)
    m = n_de(0.4)
    poe(x, seno(600 + 40 * np.sin(2 * math.pi * 16 * _t(m)), m) * sobe_e_some(m, 0.3, 1.3) * 0.03, 0.55)
    poe(x, _acerto(rng, 0.3, 130), 0.3)
    return reverb(x, 0.5, 0.25)


# =================================================================== Tenshinhan
def kiai_invisivel(rng, v):
    """O kiai: o "HA!" de ar comprimido (o estouro grave sem corpo), a onda invisível passando (o vento que
    entorta) e o baque abafado no rival."""
    x = _z(1.0)
    n = n_de(0.15)
    poe(x, passa(rosa(rng, n), 150, 1500, 2) * env(n, 0.002, 0.08) * 0.6 + seno(varre(220, 160, n, 1.0), n) * env(n, 0.002, 0.08) * 0.12, 0.08)
    poe(x, _whoosh(rng, 0.3, 250, 900, 0.7, 1.3, 0.5), 0.12)
    poe(x, passa(B._baque_seco(rng, n_de(0.25), 90, 0.07), None, 1200, 2) * 0.8, 0.4)
    return reverb(x, 0.4, 0.2)


# =================================================================== Deidara
def argila_explosiva(rng, v):
    """A argila explosiva: o passarinho batendo as asas (o "flap-flap" leve), um instante parado e o
    "Katsu!" (o estouro com o estalo seco e o crepitar)."""
    x = _z(1.1)
    for k in range(5):
        m = n_de(0.05)
        poe(x, passa(rosa(rng, m), 800, 4000, 2) * env(m, 0.003, 0.03) * 0.18, 0.03 + 0.07 * k)
    poe(x, baque(n_de(0.5), 80, 40, 0.15, 1.0) * 0.8, 0.42)
    m = n_de(0.5)
    poe(x, passa(rosa(rng, m), 200, 7000, 2) * env(m, 0.001, 0.2) * 0.6, 0.42)
    poe(x, graos(rng, n_de(0.5), 20, 0.05, 0.45, 2000, 8000, 0.005) * 0.3, 0.45)
    return reverb(x, 0.45, 0.22)


# =================================================================== Violeta
def empurrao_de_campo(rng, v):
    """O campo de força: a bolha se formando (o "vumm" que sobe, cheio) e o empurrão (o baque elástico, como
    uma bola de borracha enorme)."""
    x = _z(1.0)
    n = n_de(0.3)
    poe(x, (seno(varre(150, 300, n, 1.0), n) + seno(varre(300, 600, n, 1.0), n) * 0.3) * sobe_e_some(n, 0.7, 1.3) * 0.12, 0.0)
    poe(x, _whoosh(rng, 0.2, 400, 1200, 0.8, 1.3, 0.3), 0.2)
    poe(x, _mola(0.35, 140, 0.25, 9, 0.2), 0.42)
    poe(x, B._baque_seco(rng, n_de(0.2), 95, 0.06) * 0.7, 0.42)
    return reverb(x, 0.4, 0.2)


# =================================================================== Orihime
def tsubaki(rng, v):
    """O Tsubaki: o grampo brilhando (o sininho suave), "Koten Zanshun!" (a fadinha cortando o ar num "tsiu"
    fino) e o corte limpo de luz."""
    x = _z(1.0)
    poe(x, _brilho(rng, 0.5, 1760, 0.1, SINO), 0.0)
    m = n_de(0.2)
    poe(x, seno(varre(2400, 4200, m, 1.0), m) * sobe_e_some(m, 0.7, 1.3) * 0.06, 0.15)
    poe(x, _whoosh(rng, 0.18, 2000, 7000, 0.8, 1.2, 0.35), 0.16)
    poe(x, B._lamina_curta(rng, n_de(0.3), 3000) * env(n_de(0.3), 0.001, 0.12) * 0.25, 0.32)
    poe(x, _acerto(rng, 0.35, 160, 2000, 7000), 0.32)
    return reverb(x, 0.45, 0.22)


# =================================================================== Aerith
def cajado_da_cetra(rng, v):
    """O cajado da Aerith: o giro do cajado (o "vuup"), o "toc" de madeira e as luzinhas subindo (os sininhos
    em escada, suaves)."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.28, 500, 2200, 0.8, 1.3, 0.4), 0.0)
    n = n_de(0.12)
    poe(x, modal(n, 700, rng=rng, razoes=[1.0, 2.4, 4.3], quedas=[0.05, 0.03, 0.02], ganhos=[1, 0.5, 0.3]) * 0.4, 0.28)
    poe(x, _acerto(rng, 0.45, 140), 0.28)
    for k, f in enumerate((1319, 1568, 1760, 2093)):
        poe(x, _brilho(rng, 0.4, f, 0.05, SINO), 0.38 + 0.08 * k)
    return reverb(x, 0.5, 0.25)


# =================================================================== Katara
def chicote_de_agua(rng, v):
    """O jato de água: a água correndo no ar (o chiado líquido que serpenteia), o estalo molhado no rival e as
    gotas caindo."""
    x = _z(1.0)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 600, 4000, 2) * (0.6 + 0.4 * np.sin(2 * math.pi * 9 * _t(n))) * sobe_e_some(n, 0.6, 1.3) * 0.35, 0.0)
    poe(x, _splash(rng, 0.35, 0.5), 0.28)
    poe(x, _acerto(rng, 0.4, 130), 0.28)
    for k in range(5):
        m = n_de(0.05)
        poe(x, seno(varre(1200 + 150 * k, 600, m, 1.0), m) * env(m, 0.002, 0.03) * 0.04, 0.45 + 0.05 * k)
    return reverb(x, 0.35, 0.18)


# =================================================================== Sailor Mercury
def bolhas_de_mercurio(rng, v):
    """As bolhas: os "bloop" das bolhas saindo (tons redondos subindo), os estalinhos delas estourando e a névoa
    fria (o chiado suave)."""
    x = _z(1.1)
    for k in range(7):
        m = n_de(0.08)
        poe(x, seno(varre(400 + 60 * k, 900 + 60 * k, m, 1.0), m) * env(m, 0.004, 0.06) * 0.08, 0.02 * k * 3)
    for k in range(7):
        poe(x, estalo(rng, n_de(0.02), 2500, 8000, 0.003) * 0.3, 0.45 + 0.03 * k)
    n = n_de(0.5)
    poe(x, passa(rosa(rng, n), 3000, 9000, 2) * sobe_e_some(n, 0.3, 1.3) * 0.15, 0.5)
    return reverb(x, 0.45, 0.22)


# =================================================================== Kurama
def petalas_cortantes(rng, v):
    """As pétalas cortantes: o vento girando com as pétalas (o assobio que gira) e os cortes finos, três, rápidos
    (os "tsk" secos)."""
    x = _z(1.0)
    n = n_de(0.45)
    poe(x, passa(rosa(rng, n), 1500, 7000, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 7 * _t(n)))) * sobe_e_some(n, 0.5, 1.3) * 0.3, 0.0)
    for k in range(3):
        poe(x, B._lamina_curta(rng, n_de(0.15), 3500) * env(n_de(0.15), 0.001, 0.05) * 0.2, 0.2 + 0.06 * k)
        poe(x, B._tapa(rng, n_de(0.05), 2000, 8000, 0.006) * 0.5, 0.2 + 0.06 * k)
    return reverb(x, 0.4, 0.2)


# =================================================================== Ken
def punho_flamejante_ken(rng, v):
    """O soco do Ken: o soco cortando o ar com o "fwoosh" do fogo, o impacto forte e o crepitar das brasas."""
    x = _z(1.0)
    poe(x, _whoosh(rng, 0.25, 400, 2500, 0.85, 1.3, 0.5), 0.0)
    n = n_de(0.3)
    poe(x, passa(rosa(rng, n), 200, 3000, 2) * sobe_e_some(n, 0.6, 1.3) * 0.35, 0.0)
    poe(x, _acerto(rng, 1.0, 110), 0.25)
    poe(x, graos(rng, n_de(0.5), 25, 0.0, 0.45, 1500, 6000, 0.004) * 0.3, 0.3)
    return reverb(x, 0.35, 0.18)


# =================================================================== Heihachi
def punho_do_trovao(rng, v):
    """O soco do trovão: o gancho subindo com os estalos elétricos, o trovão caindo (o "crack" seco e o ronco) e
    o impacto pesado."""
    x = _z(1.1)
    poe(x, _whoosh(rng, 0.25, 300, 1800, 0.85, 1.3, 0.45), 0.0)
    poe(x, graos(rng, n_de(0.25), 25, 0.0, 0.22, 2500, 9000, 0.003) * 0.35, 0.02)
    poe(x, estalo(rng, n_de(0.05), 1500, 9000, 0.01) * 1.0, 0.26)
    m = n_de(0.6)
    poe(x, passa(rosa(rng, m), 40, 600, 2) * env(m, 0.005, 0.35) * 0.6, 0.27)
    poe(x, _acerto(rng, 1.0, 100), 0.27)
    return reverb(x, 0.5, 0.22)


# =================================================================== Jake
def punho_esticado(rng, v):
    """O braço do Jake: o elástico esticando (o "streeetch" que sobe, de borracha), o "boing" do punho batendo e
    o braço voltando (o "zip" que encolhe)."""
    x = _z(1.1)
    n = n_de(0.28)
    poe(x, seno(varre(200, 700, n, 1.0), n) * (0.7 + 0.3 * np.sin(2 * math.pi * 30 * _t(n))) * sobe_e_some(n, 0.8, 1.3) * 0.1, 0.0)
    poe(x, _mola(0.4, 220, 0.4, 12, 0.22), 0.28)
    poe(x, _acerto(rng, 0.6, 120), 0.28)
    m = n_de(0.2)
    poe(x, seno(varre(800, 250, m, 1.0), m) * sobe_e_some(m, 0.3, 1.3) * 0.08, 0.6)
    return reverb(x, 0.35, 0.18)


SONS: dict = {
    "jato-criogenico": (jato_criogenico, "básico do Senhor Frio: o jato frio e o gelo"),
    "chicote-de-vinha": (chicote_de_vinha, "básico da Hera: as folhas, o estalo e os esporos"),
    "bola-de-neve": (bola_de_neve, "básico do Homem de Gelo: a bola de neve espatifando"),
    "lambida-fantasma": (lambida_fantasma, "básico do Gengar: a lambida e a risadinha"),
    "kiai-invisivel": (kiai_invisivel, "básico do Tenshinhan: o kiai e o baque"),
    "argila-explosiva": (argila_explosiva, "básico do Deidara: as asas e o Katsu"),
    "empurrao-de-campo": (empurrao_de_campo, "básico da Violeta: a bolha e o empurrão"),
    "tsubaki": (tsubaki, "básico da Orihime: o sininho e o corte de luz"),
    "cajado-da-cetra": (cajado_da_cetra, "básico da Aerith: o cajado e as luzinhas"),
    "chicote-de-agua": (chicote_de_agua, "básico da Katara: a água e as gotas"),
    "bolhas-de-mercurio": (bolhas_de_mercurio, "básico da Sailor Mercury: as bolhas estourando"),
    "petalas-cortantes": (petalas_cortantes, "básico do Kurama: as pétalas cortando"),
    "punho-flamejante-ken": (punho_flamejante_ken, "básico do Ken: o soco em chamas"),
    "punho-do-trovao": (punho_do_trovao, "básico do Heihachi: o gancho e o trovão"),
    "punho-esticado": (punho_esticado, "básico do Jake: o elástico e o boing"),
}
