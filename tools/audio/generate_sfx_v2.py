#!/usr/bin/env python3
"""
Biblioteca de efeitos sonoros (adendo, parte 6).

Antes: 18 sons a 22 kHz, todos com o mesmo envelope, muitos parecidos. Agora:
famílias que conversam com as famílias visuais (soco, corte, feixe, fogo, gelo,
raio, cura, Escudo…), cada uma com 4 versões diferentes — tom, camada,
transiente, cauda — a 44,1 kHz, montadas em camadas (veja tools/audio/som.py).

Cada arquivo MP3 guarda as 4 versões em sequência, separadas por um respiro de
silêncio; o manifest diz onde cada uma começa e quanto dura. O jogo escolhe a
versão de forma determinística (replay e testes ouvem o mesmo), varia de leve o
tom e o volume, e posiciona no estéreo pela posição de quem age.

Uso: python3 tools/audio/generate_sfx_v2.py [nome ...]
     (gera public/assets/audio/sfx/*.mp3 e manifest.json)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from som import (CRISTAL, METAL, SINO, SR, VIDRO, apara, assobio, baque, cabe, cauda_livre, env, estalo,  # noqa: E402
                 faixas, CENTROS, graos, janela_suave, limita, modal, n_de, passa, poe, reverb, rms_db, rosa, volume_percebido,
                 ruido, satura, seno, serra_suave, sobe_e_some, tempo, varre)

ROOT = Path(__file__).resolve().parents[2]
import os
OUT = Path(os.environ.get("SAIDA_SFX", ROOT / "public/assets/audio/sfx"))
VERSOES = 4
RESPIRO = 0.08          # silêncio entre versões no mesmo arquivo


def nota(midi: float) -> float:
    return 440 * 2 ** ((midi - 69) / 12)


# =================================================================== FÍSICO

# ---- blocos de luta realistas (substituem as versões antigas) ----
def _tapa(rng, n, lo=1200, hi=5200, queda=0.012):
    """O "smack" do contato: ruído branco numa banda média-aguda, ataque instantâneo, some em ~20 ms."""
    return passa(ruido(rng, n), lo, hi, 2) * env(n, 0.0003, queda)


def _carne(rng, n, queda=0.045, sat=2.2):
    """O corpo carnudo do soco: ruído na banda 250–900 Hz, levemente saturado."""
    return satura(passa(ruido(rng, n), 250, 900, 2) * env(n, 0.0008, queda), sat)


def _baque_seco(rng, n, f=85, queda=0.09):
    """Peso do golpe SEM o tom descendo (que soa como bumbo): seno fixo curto + ruído grave."""
    t = np.arange(n) / SR
    corpo = np.sin(2 * math.pi * f * t) * np.exp(-t / queda)
    grave = passa(ruido(rng, n), 40, 280, 2) * env(n, 0.001, queda * 0.8)
    # harmônicos que o alto-falante de celular toca
    return satura(corpo * 0.5 + grave * 2.2, 1.6)


def _pano(rng, n, g=0.12):
    """Rastro de roupa/ar depois do golpe."""
    return passa(ruido(rng, n), 2500, 8000, 2) * env(n, 0.004, 0.06) * g


def soco_leve(rng, v):
    n = n_de(0.28)
    x = _baque_seco(rng, n, rng.uniform(95, 115), 0.06) * 0.75
    x += _carne(rng, n, 0.035) * 0.9
    x += _tapa(rng, n, 1400, 5500, 0.009) * 1.1
    x += _pano(rng, n)
    return reverb(x, 0.2, 0.08, 6000)


def soco_pesado(rng, v):
    n = n_de(0.5)
    x = _baque_seco(rng, n, rng.uniform(70, 85), 0.13) * 1.1
    x += _carne(rng, n, 0.07, 3.0) * 1.1
    x += _tapa(rng, n, 1000, 4500, 0.014) * 1.0
    # estalo de "osso" curto logo depois do contato
    poe(x, passa(ruido(rng, n_de(0.03)), 2500, 7000, 2) * env(n_de(0.03), 0.0003, 0.004) * 0.6, 0.006)
    x += _pano(rng, n, 0.16)
    return reverb(x, 0.3, 0.12, 5000)


def esmagar(rng, v):
    n = n_de(0.8)
    x = _baque_seco(rng, n, 60, 0.25) * 1.3
    x += _carne(rng, n, 0.12, 3.5) * 1.2
    x += _tapa(rng, n, 800, 3500, 0.02)
    x += graos(rng, n, 26, 0.03, 0.45, 700, 4500, 0.006) * 0.35                   # entulho caindo
    x += passa(rosa(rng, n), 50, 250, 2) * env(n, 0.01, 0.25) * 0.4               # chão tremendo
    return reverb(x, 0.55, 0.22, 4000)


def multi_golpe(rng, v):
    n = n_de(0.8)
    x = np.zeros(n)
    t = 0.0
    for k in range(rng.integers(5, 7)):
        m = n_de(0.12)
        g = _baque_seco(rng, m, rng.uniform(100, 130), 0.04) * 0.6 + _carne(rng, m, 0.025) * 0.8 + _tapa(rng, m, 1500, 6000, 0.007)
        poe(x, g, t, rng.uniform(0.6, 1.0) * (1.15 if k == 0 else 1))
        t += rng.uniform(0.065, 0.095)
    poe(x, soco_leve(rng, v)[: n_de(0.28)], t, 1.1)                               # o último fecha
    return reverb(x, 0.25, 0.1)


def _placa_de_metal(rng, n, grave=180, agudo=4200, quantos=34, queda=0.22):
    """Um escudo de metal batido: muitos modos inarmônicos curtos (placa), não um sino.

    Os parciais são densos e espalhados sem razão harmônica, os agudos morrem
    muito antes dos graves, e o conjunto todo é abafado (a mão segura o escudo),
    então soa como "tonc/clank" e não como "plim".
    """
    t = np.arange(n) / SR
    x = np.zeros(n)
    for _ in range(quantos):
        f = math.exp(rng.uniform(math.log(grave), math.log(agudo)))
        q = queda * (grave / f) ** 0.55 * rng.uniform(0.6, 1.2)
        x += np.sin(2 * math.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-t / q) * (f / grave) ** -0.35
    return x / quantos ** 0.5 * np.exp(-t / (queda * 1.4))


def bloqueio(rng, v):
    """O golpe bate no escudo: estalo, clangor abafado de metal e o baque de quem segura."""
    n = n_de(0.5)
    x = _placa_de_metal(rng, n, rng.uniform(170, 220), 4500, 70, 0.1) * 0.6
    x += _tapa(rng, n, 1800, 8000, 0.006) * 1.0
    x += _baque_seco(rng, n, 120, 0.05) * 0.55
    x += satura(passa(ruido(rng, n), 600, 2500, 2) * env(n, 0.0005, 0.03), 2) * 0.35  # o "tonc" do contato
    return reverb(x, 0.35, 0.15, 6000)


def escudo(rng, v):
    """O escudo se ergue: um sopro grave que fecha, energia correndo e um encaixe metálico curto."""
    n = n_de(0.8)
    x = assobio(rng, n, 300, 2500, 0.8, 0.5) * sobe_e_some(n, 0.35, 1.3) * 0.35
    zum = passa(satura(seno(varre(70, 110, n, 0.7), n), 2.5), None, 600, 2) * env(n, 0.04, 0.25) * 0.22
    x += zum
    poe(x, _placa_de_metal(rng, n_de(0.4), 220, 3500, 50, 0.08) * 0.45 + _baque_seco(rng, n_de(0.4), 110, 0.05) * 0.4, 0.22)
    return reverb(x, 0.45, 0.2, 6000)


def _lamina_curta(rng, n, f0):
    """O "shing" do fio: parciais altos de metal que morrem rápido (não ficam tocando)."""
    t = np.arange(n) / SR
    x = np.zeros(n)
    for k in range(10):
        f = f0 * rng.uniform(0.7, 2.6)
        x += np.sin(2 * math.pi * f * t + rng.uniform(0, 6)) * np.exp(-t / rng.uniform(0.025, 0.07))
    return x / 10 ** 0.5


def corte(rng, v):
    n = n_de(0.42)
    x = np.zeros(n)
    w = assobio(rng, n_de(0.12), 1200, 7000, 1.4, 0.4) * sobe_e_some(n_de(0.12), 0.8, 1.3)
    poe(x, w, 0.0, 0.8)
    corte_ = passa(ruido(rng, n_de(0.12)), 2500, 9000, 2) * env(n_de(0.12), 0.0005, 0.025) * 0.9   # o fio passando
    poe(x, corte_ + _carne(rng, n_de(0.12), 0.02) * 0.4, 0.1)
    poe(x, _lamina_curta(rng, n_de(0.2), rng.uniform(2600, 3400)) * 0.2, 0.1)
    return reverb(x, 0.25, 0.12, 7000)


def corte_pesado(rng, v):
    n = n_de(0.62)
    x = np.zeros(n)
    w = assobio(rng, n_de(0.2), 400, 4000, 1.3, 0.5) * sobe_e_some(n_de(0.2), 0.8, 1.6)
    poe(x, w, 0.0, 1.0)
    poe(x, _baque_seco(rng, n_de(0.3), 90, 0.08) * 0.8 + _carne(rng, n_de(0.3), 0.05, 2.6), 0.18)
    poe(x, passa(ruido(rng, n_de(0.15)), 2000, 8000, 2) * env(n_de(0.15), 0.0005, 0.035) * 0.9, 0.18)
    poe(x, _lamina_curta(rng, n_de(0.25), rng.uniform(1800, 2400)) * 0.25, 0.18)
    return reverb(x, 0.4, 0.18, 5500)


def estocada(rng, v):
    n = n_de(0.4)
    x = np.zeros(n)
    w = assobio(rng, n_de(0.09), 1500, 6500, 2.0, 0.35) * sobe_e_some(n_de(0.09), 0.9, 1.2)
    poe(x, w, 0.0, 0.7)
    poe(x, _carne(rng, n_de(0.2), 0.04, 2.5) + _tapa(rng, n_de(0.2), 1500, 6000, 0.01) * 0.8, 0.08)
    poe(x, _lamina_curta(rng, n_de(0.15), 3200) * 0.15, 0.08)
    return reverb(x, 0.22, 0.1)


def corte_giratorio(rng, v):
    n = n_de(0.7)
    t = np.arange(n) / SR
    voltas = rng.uniform(3.5, 4.5)
    x = assobio(rng, n, 800, 4500, 1.0, 0.45) * (0.3 + 0.7 * np.sin(math.pi * voltas * t / (n / SR)) ** 2)
    x *= sobe_e_some(n, 0.55, 1.2)
    poe(x, corte(rng, v)[n_de(0.08):] * 0.9, 0.4)
    return reverb(x, 0.3, 0.15)

def gancho(rng, v):
    n = n_de(0.5)
    x = np.zeros(n)
    w = assobio(rng, n_de(0.16), 500, 3200, 1.4) * sobe_e_some(n_de(0.16), 0.85, 1.5) * 0.6
    poe(x, w, 0.0)
    golpe = soco_pesado(rng, v)[: n - n_de(0.12)]
    poe(x, golpe, 0.12, 0.9)
    return x


def terremoto(rng, v):
    n = n_de(1.3)
    t = np.arange(n) / SR
    ronco = passa(rosa(rng, n), 40, 220, 3) * env(n, 0.05, 0.5) * 0.7
    ronco *= 1 + 0.4 * np.sin(2 * math.pi * 7 * t)                                # tremor
    x = baque(n, 55, 28, 0.4, 0.3) * 1.1 + ronco
    x += graos(rng, n, 40, 0.05, 0.9, 500, 3500, 0.008) * 0.32
    x += satura(passa(ruido(rng, n), 200, 1400, 2) * env(n, 0.003, 0.14), 2) * 0.9
    return reverb(x, 0.7, 0.25, 3500)


def onda_choque(rng, v):
    n = n_de(0.9)
    x = baque(n, 80, 35, 0.2, 0.3) * 0.9
    x += assobio(rng, n, 4500, 250, 0.7, 0.55) * env(n, 0.005, 0.25) * 0.9          # o ar sendo empurrado
    x += estalo(rng, n, 800, 3500, 0.02) * 0.4
    return reverb(x, 0.55, 0.3)


# =================================================================== CORTES
def _lamina(rng, n, f0, brilho=1.0):
    return modal(n, f0, rng=rng, desafina=0.01, **METAL) * env(n, 0.001, 0.25) * 0.25 * brilho


def lamina_energia(rng, v):
    n = n_de(0.65)
    t = np.arange(n) / SR
    f = varre(rng.uniform(500, 650), rng.uniform(1300, 1600), n, 1.6)
    tom = seno(f * (1 + 0.004 * np.sin(2 * math.pi * 30 * t)), n) * 0.35 + seno(f * 2.01, n) * 0.12
    x = tom * sobe_e_some(n, 0.25, 1.3)
    x += assobio(rng, n, 800, 6000, 1.2) * sobe_e_some(n, 0.3, 1.3) * 0.5
    return reverb(x, 0.5, 0.3)


# =================================================================== PROJÉTEIS E ENERGIA
def disparo(rng, v):
    n = n_de(0.32)
    f = varre(rng.uniform(1700, 2200), rng.uniform(260, 340), n, 0.6)
    x = seno(f, n) * env(n, 0.001, 0.08) * 0.6
    x += seno(f * 1.5, n) * env(n, 0.001, 0.05) * 0.2
    x += estalo(rng, n, 2000, 9000, 0.006) * 0.4
    return reverb(x, 0.3, 0.2)


def tiro(rng, v):
    n = n_de(0.45)
    x = satura(passa(ruido(rng, n), 200, 5000, 2) * env(n, 0.0005, 0.03), 2.5) * 0.8
    x += baque(n, 120, 50, 0.06, 0.2) * 0.6
    x += passa(rosa(rng, n), 300, 2500, 2) * env(n, 0.01, 0.12) * 0.25           # o eco curto
    return reverb(x, 0.5, 0.3, 5000)


def saraivada(rng, v):
    n = n_de(0.7)
    x = np.zeros(n)
    t = 0.0
    for _ in range(rng.integers(4, 6)):
        poe(x, disparo(rng, v)[: n_de(0.2)], t, rng.uniform(0.6, 0.9))
        t += rng.uniform(0.07, 0.11)
    return x


def missil(rng, v):
    n = n_de(0.75)
    x = assobio(rng, n, 400, 2400, 0.9, 0.5) * sobe_e_some(n, 0.7, 1.1) * 0.7
    x += passa(ruido(rng, n), 2000, 9000, 2) * sobe_e_some(n, 0.6, 1.0) * 0.25     # chiado do jato
    x += baque(n, 90, 45, 0.08, 0.3) * 0.5                                          # o disparo
    return reverb(x, 0.4, 0.2)


def explosao(rng, v):
    n = n_de(1.1)
    x = baque(n, 70, 28, 0.35, 0.5) * 1.2
    sopro = faixas(ruido(rng, n), CENTROS, varre(7000, 260, n, 0.5), 0.6) * env(n, 0.002, 0.3) * 1.0
    x += satura(sopro, 1.8)
    x += graos(rng, n, 50, 0.08, 0.9, 1200, 7000, 0.004) * 0.22                   # brasas estalando
    return reverb(x, 0.7, 0.3, 5000)


def carga_pequena(rng, v):
    n = n_de(0.6)
    t = np.arange(n) / SR
    f = varre(nota(rng.uniform(55, 58)), nota(rng.uniform(70, 73)), n, 1.0)
    fm = seno(f * (1 + 0.6 * seno(f * 2, n) * 0.02), n)
    x = (fm * 0.35 + seno(f * 2, n) * 0.12) * sobe_e_some(n, 0.85, 1.5)
    x += passa(rosa(rng, n), 2500, 9000, 2) * sobe_e_some(n, 0.9, 2.0) * 0.18 * (1 + 0.5 * np.sin(2 * math.pi * 18 * t))
    return reverb(x, 0.5, 0.3)


def carga_grande(rng, v):
    n = n_de(1.3)
    t = np.arange(n) / SR
    f = varre(nota(rng.uniform(38, 41)), nota(rng.uniform(60, 63)), n, 0.9)
    corpo = sum(seno(f * k * (1 + rng.uniform(-0.004, 0.004)), n) / k for k in (1, 2, 3, 4)) * 0.3
    x = corpo * sobe_e_some(n, 0.9, 1.8) * (1 + 0.15 * np.sin(2 * math.pi * varre(4, 16, n) * t))
    x += assobio(rng, n, 200, 5000, 0.8) * sobe_e_some(n, 0.92, 2.2) * 0.5
    x += passa(rosa(rng, n), 30, 120, 2) * sobe_e_some(n, 0.9, 1.5) * 0.5
    return reverb(x, 0.6, 0.3)


def feixe(rng, v):
    n = n_de(1.0)
    t = np.arange(n) / SR
    base = nota(rng.uniform(43, 47))
    vib = 1 + 0.01 * np.sin(2 * math.pi * 6 * t)
    zumbido = (serra_suave(base * vib, n, 10) + serra_suave(base * 1.006 * vib, n, 10)) * 0.25
    zumbido = passa(zumbido, 80, 3000, 2)
    rugido = passa(rosa(rng, n), 400, 6000, 2) * 0.35 * (1 + 0.3 * np.sin(2 * math.pi * 11 * t))
    x = (zumbido + rugido) * janela_suave(n, 0.04, 0.25)
    x += estalo(rng, n, 1500, 8000, 0.02) * 0.4
    return reverb(x, 0.55, 0.25)


def impacto_energia(rng, v):
    n = n_de(0.7)
    x = estalo(rng, n, 3000, 12000, 0.006) * 0.6
    x += baque(n, 110, 45, 0.15, 0.2) * 0.8
    floresce = passa(rosa(rng, n), 600, 5000, 2) * env(n, 0.004, 0.12) * 0.45
    x += floresce
    x += modal(n, rng.uniform(1300, 1700), rng=rng, **CRISTAL) * env(n, 0.002, 0.25) * 0.12
    return reverb(x, 0.55, 0.3)


# =================================================================== ELEMENTOS
def raio(rng, v):
    n = n_de(0.6)
    t = np.arange(n) / SR
    zap = np.zeros(n)
    k = 0
    while k < n:
        largura = int(rng.uniform(0.0004, 0.002) * SR)
        zap[k:k + largura] += rng.choice([-1, 1]) * rng.uniform(0.4, 1)
        k += int(rng.exponential(0.006) * SR) + 1
    zap = passa(zap, 300, 9000, 2) * env(n, 0.001, 0.18) * 0.8
    zumbido = satura(serra_suave(rng.uniform(95, 125), n, 14), 2) * env(n, 0.002, 0.15) * 0.25
    estrondo = baque(n, 70, 32, 0.25, 0.4) * 0.3
    x = zap + zumbido + estrondo + estalo(rng, n, 2500, 12000, 0.004) * 0.7
    return reverb(x, 0.5, 0.22)


def fogo(rng, v):
    n = n_de(0.85)
    t = np.arange(n) / SR
    sopro = faixas(rosa(rng, n), CENTROS, varre(250, 1400, n, 0.7), 0.55) * sobe_e_some(n, 0.3, 1.2) * 0.9
    rugido = passa(rosa(rng, n), 60, 400, 2) * sobe_e_some(n, 0.35, 1.3) * 0.6 * (1 + 0.25 * np.sin(2 * math.pi * 9 * t + 1))
    crepita = graos(rng, n, 45, 0.05, 0.8, 2000, 9000, 0.0025, 0.7) * 0.35
    return reverb(sopro + rugido + crepita, 0.45, 0.2)


def gelo(rng, v):
    n = n_de(0.9)
    x = estalo(rng, n, 2500, 11000, 0.008) * 0.6                                   # o estalo do gelo
    x += graos(rng, n, 12, 0.0, 0.08, 3000, 11000, 0.003) * 0.4
    for k in range(4):
        f = nota(rng.choice([84, 86, 88, 91, 93, 96]))
        poe(x, modal(n_de(0.7), f, rng=rng, **CRISTAL) * env(n_de(0.7), 0.001, 0.3) * 0.13, 0.02 + k * rng.uniform(0.03, 0.06))
    x += passa(rosa(rng, n), 5000, 14000, 2) * env(n, 0.03, 0.35) * 0.12            # brilho da geada
    return reverb(x, 0.6, 0.35, 9000)


def vento(rng, v):
    n = n_de(1.0)
    t = np.arange(n) / SR
    curva = 600 * 2 ** (1.6 * np.sin(math.pi * t / (n / SR)) ** 1.3) * rng.uniform(0.8, 1.2)
    x = faixas(rosa(rng, n), CENTROS, curva, 0.4) * sobe_e_some(n, 0.45, 1.2) * 1.1
    x += faixas(rosa(rng, n), CENTROS, curva * 2.7, 0.25) * sobe_e_some(n, 0.5, 1.5) * 0.35   # assobio alto
    return reverb(x, 0.5, 0.2)


def agua(rng, v):
    n = n_de(0.8)
    x = passa(ruido(rng, n), 300, 4500, 2) * env(n, 0.002, 0.08) * 0.7             # o respingo
    x += baque(n, 120, 60, 0.05, 0.1) * 0.35
    for _ in range(14):                                                             # gotas
        d = n_de(0.05)
        f = varre(rng.uniform(900, 1600), rng.uniform(1800, 3200), d, 1.0)
        poe(x, seno(f, d) * env(d, 0.001, 0.012) * rng.uniform(0.1, 0.25), rng.uniform(0.04, 0.55))
    x += passa(rosa(rng, n), 1500, 7000, 2) * env(n, 0.02, 0.25) * 0.15
    return reverb(x, 0.45, 0.25)


def terra(rng, v):
    n = n_de(0.9)
    x = baque(n, 75, 35, 0.2, 0.3) * 0.9
    x += satura(passa(ruido(rng, n), 250, 1800, 2) * env(n, 0.002, 0.1), 2.2) * 0.8
    x += graos(rng, n, 45, 0.02, 0.7, 400, 3000, 0.009) * 0.5                      # pedras rolando
    return reverb(x, 0.55, 0.22, 4000)


def veneno(rng, v):
    n = n_de(0.9)
    x = passa(rosa(rng, n), 1500, 7000, 2) * sobe_e_some(n, 0.25, 1.0) * 0.3       # chiado ácido
    for _ in range(18):                                                             # bolhas
        d = n_de(rng.uniform(0.03, 0.06))
        f = varre(rng.uniform(250, 500), rng.uniform(600, 1100), d, 1.2)
        poe(x, seno(f, d) * env(d, 0.002, 0.02) * rng.uniform(0.15, 0.35), rng.uniform(0.0, 0.75))
    return reverb(x, 0.4, 0.25)


# =================================================================== MAGIA
def psiquico(rng, v):
    n = n_de(0.9)
    t = np.arange(n) / SR
    f = nota(rng.uniform(64, 70)) * (1 + 0.03 * np.sin(2 * math.pi * varre(3, 9, n) * t))
    x = seno(f, n) * 0.3 * seno(f * 0.501, n) + seno(f * 1.5, n) * 0.12
    x *= sobe_e_some(n, 0.4, 1.4)
    x += assobio(rng, n, 3000, 700, 1.0) * sobe_e_some(n, 0.35, 1.2) * 0.3
    return reverb(x, 0.75, 0.4)


def sombra(rng, v):
    n = n_de(1.0)
    t = np.arange(n) / SR
    base = nota(rng.uniform(33, 36))
    drone = sum(seno(base * r * (1 + 0.003 * np.sin(2 * math.pi * 0.7 * t * k)), n) for k, r in enumerate((1, 1.007, 1.5, 2.01), 1)) * 0.18
    x = drone * sobe_e_some(n, 0.35, 1.3)
    x += assobio(rng, n, 1400, 160, 0.8, 0.5) * sobe_e_some(n, 0.3, 1.3) * 0.6        # whoosh que afunda
    x += passa(rosa(rng, n), 40, 140, 2) * env(n, 0.03, 0.3) * 0.4
    return reverb(x, 0.8, 0.35, 3500)


def luz(rng, v):
    n = n_de(1.2)
    x = np.zeros(n)
    raiz = rng.choice([72, 74, 76])
    for k, iv in enumerate((0, 4, 7, 12)):                                           # acorde maior em arpejo
        f = nota(raiz + iv)
        poe(x, modal(n_de(1.0), f, rng=rng, **SINO) * env(n_de(1.0), 0.002, 0.45) * 0.14, k * 0.045)
    x += passa(rosa(rng, n), 5000, 14000, 2) * sobe_e_some(n, 0.15, 1.0) * 0.12
    return reverb(x, 0.85, 0.45, 10000)


def portal(rng, v):
    n = n_de(1.0)
    t = np.arange(n) / SR
    curva = 900 * 2 ** (1.2 * np.sin(2 * math.pi * 2.2 * t))
    x = faixas(rosa(rng, n), CENTROS, curva, 0.35) * sobe_e_some(n, 0.5, 1.2) * 0.8
    x += seno(nota(rng.uniform(40, 43)) * (1 + 0.02 * np.sin(2 * math.pi * 2.2 * t)), n) * sobe_e_some(n, 0.5, 1.2) * 0.3
    return reverb(x, 0.75, 0.35)


def maldicao(rng, v):
    n = n_de(1.0)
    x = np.zeros(n)
    raiz = rng.uniform(62, 65)
    for k, iv in enumerate((0, -6, -13)):                                            # descendo em trítono
        d = n_de(0.5)
        f = nota(raiz + iv) * (1 + 0.01 * np.sin(2 * math.pi * 5 * np.arange(d) / SR))
        poe(x, (seno(f, d) * 0.25 + seno(f * 2.003, d) * 0.08) * env(d, 0.02, 0.2), k * 0.17)
    x += passa(rosa(rng, n), 800, 4000, 2) * sobe_e_some(n, 0.3, 1.0) * 0.2          # sussurro
    return reverb(x, 0.8, 0.4, 4500)


def prisao(rng, v):
    n = n_de(0.85)
    x = np.zeros(n)
    t = 0.0
    for _ in range(rng.integers(4, 7)):                                              # elos de corrente
        d = n_de(0.12)
        poe(x, modal(d, rng.uniform(2200, 3400), rng=rng, desafina=0.03, **METAL) * env(d, 0.0005, 0.03) * 0.3, t)
        t += rng.uniform(0.045, 0.075)
    trava = baque(n_de(0.3), 140, 70, 0.06, 0.5) * 0.7 + modal(n_de(0.3), 900, rng=rng, **METAL) * env(n_de(0.3), 0.001, 0.08) * 0.3
    poe(x, trava, t + 0.03)
    return reverb(x, 0.4, 0.2)


def selo(rng, v):
    n = n_de(1.1)
    x = np.zeros(n)
    raiz = rng.choice([76, 79, 81])
    for k, iv in enumerate((0, 5, 7, 12)):
        poe(x, modal(n_de(0.8), nota(raiz + iv), rng=rng, **CRISTAL) * env(n_de(0.8), 0.001, 0.3) * 0.13, k * 0.07)
    x += passa(rosa(rng, n), 100, 400, 2) * sobe_e_some(n, 0.3, 1.0) * 0.18          # base que vibra
    return reverb(x, 0.7, 0.4, 9000)


def distorcao(rng, v):
    n = n_de(0.85)
    t = np.arange(n) / SR
    f = nota(rng.uniform(55, 60))
    x = seno(f * (1 + 0.08 * np.sin(2 * math.pi * 13 * t)), n) * seno(f * 1.41, n) * 0.35  # anel modulado
    x *= sobe_e_some(n, 0.3, 1.2)
    cortes = (np.sin(2 * math.pi * rng.uniform(16, 22) * t) > 0.2).astype(float)
    x += passa(ruido(rng, n), 1500, 6000, 2) * cortes * sobe_e_some(n, 0.3, 1.2) * 0.12
    return reverb(x, 0.6, 0.3)


# =================================================================== APOIO
def cura(rng, v):
    n = n_de(1.1)
    x = np.zeros(n)
    raiz = rng.choice([72, 74, 77])
    for k, iv in enumerate((0, 4, 7, 11, 14)):                                       # arpejo subindo, suave
        poe(x, modal(n_de(0.8), nota(raiz + iv), rng=rng, **SINO) * env(n_de(0.8), 0.008, 0.35) * 0.1, k * 0.06)
    x += passa(rosa(rng, n), 3000, 11000, 2) * sobe_e_some(n, 0.3, 1.2) * 0.1
    return reverb(x, 0.85, 0.45, 9000)


def reforco(rng, v):
    n = n_de(1.0)
    x = np.zeros(n)
    raiz = rng.choice([60, 62, 65])
    for iv in (0, 7, 12):                                                             # acorde que cresce
        f = nota(raiz + iv)
        poe(x, (seno(f, n) + seno(f * 1.003, n) * 0.6) * sobe_e_some(n, 0.6, 1.6) * 0.1, 0)
    x += assobio(rng, n, 300, 4000, 1.0) * sobe_e_some(n, 0.7, 1.8) * 0.3
    x += graos(rng, n, 16, 0.4, 0.8, 4000, 12000, 0.002) * 0.25
    return reverb(x, 0.6, 0.3)



def renova_buff(rng, v):
    """O buff renovado em quem já tinha (pedido do jogador: o som de aplicar de novo era chato): curto e
    macio — um "fuu" de ar subindo e duas notas quentes e baixas que confirmam, sem chiado agudo."""
    n = n_de(0.55)
    x = np.zeros(n)
    m = n_de(0.25)
    poe(x, passa(rosa(rng, m), 300, 2200, 2) * np.linspace(0, 1, m) ** 2 * env(m, 0.2, 0.05) * 0.35, 0.0)
    for k, nn in enumerate((62, 69)):
        r = n_de(0.38)
        f = nota(nn)
        tom = (seno(f, r) + seno(f * 2, r) * 0.18 + seno(f * 1.002, r) * 0.5) * env(r, 0.015, 0.3)
        poe(x, tom * 0.16, 0.12 + 0.07 * k)
    return reverb(x, 0.4, 0.2, 5000)


def renova_debuff(rng, v):
    """O debuff renovado em quem já tinha: o mal apertando de novo — um "tum" abafado e grave e um ronco
    curto que fecha, bem mais leve que o debuff entrando."""
    n = n_de(0.5)
    x = np.zeros(n)
    poe(x, baque(n_de(0.35), 70, 38, 0.1, 0.2) * 0.8, 0.0)
    r = n_de(0.35)
    ronco = passa(serra_suave(np.full(r, 49.0), r, 8) * 0.6 + serra_suave(np.full(r, 51.9), r, 8) * 0.5, None, 600, 2) * env(r, 0.01, 0.28)
    poe(x, ronco * 0.35, 0.02)
    m = n_de(0.22)
    poe(x, passa(rosa(rng, m), 80, 700, 2) * np.linspace(1, 0, m) ** 2 * 0.3, 0.0)
    return reverb(x, 0.35, 0.18, 2200)

def enfraquecer(rng, v):
    """O debuff entrando no rival (pedido do jogador: "tá tipo um sininho… não faz sentido"): nada de
    nota aguda. Um "fuuum" escuro sendo sugado para baixo (ruído que fecha o filtro), a pancada abafada
    e grave quando o mal gruda, e um ronco dissonante bem grave que cai e some."""
    n = n_de(0.95)
    t = np.arange(n) / SR
    x = np.zeros(n)
    # o puxão: ruído rosa com o "brilho" fechando (de 1800 para 250 Hz), crescendo até o impacto
    m = n_de(0.32)
    puxa = passa(rosa(rng, m), 120, 1800, 2) * 0.6 + passa(rosa(rng, m), 120, 500, 2) * 0.6
    puxa *= np.linspace(0.15, 1.0, m) ** 2
    poe(x, puxa * 0.55, 0.0)
    # o impacto abafado
    poe(x, baque(n_de(0.5), 75, 32, 0.16, 0.25) * 0.9, 0.3)
    # o ronco dissonante grave (segunda menor), caindo de leve e saturado
    r = n_de(0.6)
    tr = np.arange(r) / SR
    queda = 1 - 0.12 * (tr / tr[-1])
    ronco = serra_suave(55 * queda, r, 10) * 0.5 + serra_suave(58.3 * queda, r, 10) * 0.45
    ronco = passa(satura(ronco, 1.8), None, 900, 2) * env(r, 0.01, 0.45)
    poe(x, ronco * 0.45, 0.3)
    # o resto do mal se espalhando: um chiado grave que some
    poe(x, passa(rosa(rng, n_de(0.5)), 60, 400, 2) * env(n_de(0.5), 0.02, 0.4) * 0.3, 0.34)
    _ = t
    return reverb(x, 0.5, 0.22, 2500)


def purificar(rng, v):
    n = n_de(0.8)
    x = np.zeros(n)
    for k in range(7):
        f = nota(rng.choice([84, 86, 88, 91, 93, 96, 98]))
        poe(x, modal(n_de(0.4), f, rng=rng, **CRISTAL) * env(n_de(0.4), 0.001, 0.12) * 0.09, k * 0.04 + rng.uniform(0, 0.02))
    x += assobio(rng, n, 1500, 9000, 1.2) * sobe_e_some(n, 0.4, 1.4) * 0.2
    return reverb(x, 0.7, 0.4, 11000)


def dreno(rng, v):
    n = n_de(0.9)
    t = np.arange(n) / SR
    x = assobio(rng, n, 5000, 300, 1.0, 0.45) * sobe_e_some(n, 0.75, 1.0) * 0.7      # sucção
    f = varre(nota(70), nota(52), n, 1.0)
    x += seno(f * (1 + 0.02 * np.sin(2 * math.pi * 8 * t)), n) * sobe_e_some(n, 0.7, 1.2) * 0.18
    return reverb(x, 0.6, 0.3)


# =================================================================== EVENTOS
def interrupcao(rng, v):
    n = n_de(0.8)
    x = baque(n, 150, 60, 0.07, 0.6) * 0.7
    for _ in range(18):                                                              # cacos
        d = n_de(0.25)
        poe(x, modal(d, rng.uniform(1800, 6000), rng=rng, desafina=0.05, **VIDRO) * env(d, 0.0005, 0.05) * rng.uniform(0.05, 0.14), rng.uniform(0.0, 0.18))
    x += passa(ruido(rng, n), 3000, 12000, 2) * env(n, 0.001, 0.06) * 0.5
    return reverb(x, 0.55, 0.3)


def pronto(rng, v):
    n = n_de(0.55)
    x = np.zeros(n)
    raiz = rng.choice([79, 81])
    poe(x, modal(n_de(0.45), nota(raiz), rng=rng, **SINO) * env(n_de(0.45), 0.002, 0.18) * 0.18, 0)
    poe(x, modal(n_de(0.45), nota(raiz + 7), rng=rng, **SINO) * env(n_de(0.45), 0.002, 0.2) * 0.16, 0.07)
    return reverb(x, 0.5, 0.3, 10000)


def preparo(rng, v):
    n = n_de(0.7)
    x = assobio(rng, n, 2500, 400, 1.0, 0.5) * sobe_e_some(n, 0.45, 1.3) * 0.5        # energia sendo puxada
    x += seno(varre(nota(48), nota(55), n, 1.0), n) * sobe_e_some(n, 0.8, 1.5) * 0.18
    return reverb(x, 0.6, 0.3)


def grand_carga(rng, v):
    n = n_de(1.6)
    t = np.arange(n) / SR
    x = assobio(rng, n, 150, 7000, 0.7, 0.55) * sobe_e_some(n, 0.94, 2.4) * 0.9
    f = varre(nota(36), nota(60), n, 0.8)
    x += sum(seno(f * k, n) / k for k in (1, 2, 3)) * sobe_e_some(n, 0.94, 2.2) * 0.25
    x += passa(rosa(rng, n), 30, 100, 2) * sobe_e_some(n, 0.9, 1.6) * 0.6 * (1 + 0.3 * np.sin(2 * math.pi * varre(3, 14, n) * t))
    return reverb(x, 0.7, 0.3)


def grand_impacto(rng, v):
    n = n_de(1.8)
    x = baque(n, 60, 24, 0.55, 0.6) * 1.3
    x += satura(faixas(ruido(rng, n), CENTROS, varre(9000, 200, n, 0.45), 0.65) * env(n, 0.002, 0.45), 2.0) * 1.0
    x += modal(n, 220, rng=rng, **METAL) * env(n, 0.002, 0.6) * 0.15
    x += graos(rng, n, 60, 0.1, 1.4, 1500, 8000, 0.004) * 0.18
    return reverb(cauda_livre(x, 0.3), 0.9, 0.4, 4500)


def nocaute(rng, v):
    n = n_de(1.1)
    x = baque(n, 70, 30, 0.3, 0.5) * 1.1
    f = varre(nota(60), nota(36), n, 0.7)
    x += (seno(f, n) * 0.18 + seno(f * 1.5, n) * 0.08) * env(n, 0.01, 0.4)
    x += passa(rosa(rng, n), 250, 2500, 2) * env(n, 0.02, 0.3) * 0.6               # poeira
    return reverb(x, 0.7, 0.35, 4000)


def vitoria(rng, v):
    n = n_de(1.8)
    x = np.zeros(n)
    for k, (iv, d) in enumerate(((0, 0.0), (4, 0.12), (7, 0.24), (12, 0.38))):
        f = nota(67 + iv)
        tom = (serra_suave(f, n_de(1.3), 6) * 0.5 + seno(f * 2, n_de(1.3)) * 0.2) * env(n_de(1.3), 0.015, 0.5)
        poe(x, passa(tom, 120, 5000, 2) * 0.18, d)
        poe(x, modal(n_de(1.2), f * 2, rng=rng, **SINO) * env(n_de(1.2), 0.002, 0.5) * 0.08, d)
    return reverb(x, 0.85, 0.4, 9000)


def derrota(rng, v):
    n = n_de(1.6)
    x = np.zeros(n)
    for k, iv in enumerate((0, -3, -7)):
        f = nota(57 + iv)
        tom = (serra_suave(f, n_de(1.2), 5) * 0.4 + seno(f / 2, n_de(1.2)) * 0.3) * env(n_de(1.2), 0.03, 0.5)
        poe(x, passa(tom, 80, 2200, 2) * 0.2, k * 0.28)
    return reverb(x, 0.85, 0.4, 3500)


def virada(rng, v):
    n = n_de(0.9)
    x = assobio(rng, n, 300, 5000, 1.2) * sobe_e_some(n, 0.35, 1.3) * 0.5
    for k, iv in enumerate((0, 7)):
        f = nota(rng.choice([67, 69]) + iv)
        poe(x, (seno(f, n_de(0.6)) * 0.22 + seno(f * 2, n_de(0.6)) * 0.07) * env(n_de(0.6), 0.005, 0.25), 0.2 + k * 0.11)
    return reverb(x, 0.6, 0.3)


def transformacao(rng, v):
    n = n_de(1.4)
    x = carga_grande(rng, v)[: n_de(0.9)]
    x = np.concatenate([x, np.zeros(n - len(x))])
    poe(x, explosao(rng, v)[: n_de(0.6)] * 0.8, 0.8)
    return x


def toque(rng, v):
    n = n_de(0.12)
    return modal(n, rng.uniform(1700, 2100), rng=rng, **VIDRO) * env(n, 0.0005, 0.03) * 0.4


# =================================================================== interface (remake das telas)
# Curtos, secos e afinados na mesma tonalidade (ré): tocar botões em sequência
# soa como parte do jogo, não como cliques soltos.

def _plink(midi, seg=0.25, queda=0.08, harm=6, brilho=1.0):
    """Nota de sintetizador limpa: harmônicos que somem do agudo para o grave
    (o "plin" macio de menu de jogo moderno — sem sino, sem vidro)."""
    n = n_de(seg)
    t = np.arange(n) / SR
    f = 440.0 * 2 ** ((midi - 69) / 12)
    x = np.zeros(n)
    for h in range(1, harm + 1):
        if f * h > SR * 0.45:
            break
        x += np.sin(2 * math.pi * f * h * t) / h ** (1.6 - 0.4 * brilho) * np.exp(-t / (queda / h ** 0.6))
    return x * np.minimum(1, t / 0.002)


def _baque_menu(n, f0=110, f1=55, queda=0.07):
    """O peso por baixo de um botão importante: seno curto que desce (sente mais do que ouve)."""
    t = np.arange(n) / SR
    return np.sin(2 * math.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-t / 0.03)) / SR) * np.exp(-t / queda)


# notas no tom da música (mi menor): mi, sol, si, ré
_MI5, _SOL5, _SI5, _RE6, _MI6, _SOL6, _SI6 = 76, 79, 83, 86, 88, 91, 95


def reacao(rng, v):
    """Um traço disparou no meio da ação de outro: um arranque de energia curto
    (zum que sobe), duas notas rápidas subindo no tom da música e um brilho."""
    n = n_de(0.55)
    x = np.zeros(n)
    m = n_de(0.16)
    t = np.arange(m) / SR
    zum = np.sin(2 * math.pi * np.cumsum(varre(180, 900, m, 0.8)) / SR + 1.5 * np.sin(2 * math.pi * 90 * t)) * np.minimum(1, t / 0.01) * np.exp(-t / 0.09)
    poe(x, satura(zum, 1.8) * 0.22, 0)
    poe(x, _plink(_SI5, 0.25, 0.08, 6, 1.3) * 0.32, 0.07)
    poe(x, _plink(_MI6, 0.35, 0.12, 6, 1.3) * 0.36, 0.12)
    poe(x, passa(ruido(rng, n_de(0.2)), 4000, 11000, 2) * sobe_e_some(n_de(0.2), 0.3, 1.5) * 0.08, 0.1)
    return reverb(x, 0.35, 0.2, 9000)


def ui_clique(rng, v):
    """Toque comum: um "tic" macio de sintetizador, curtinho e afinado."""
    n = n_de(0.12)
    x = np.zeros(n)
    poe(x, _plink(rng.choice([_MI6, _SOL6]), 0.12, 0.035, 4) * 0.5, 0)
    poe(x, passa(ruido(rng, n_de(0.01)), 3000, 9000, 2) * env(n_de(0.01), 0.0003, 0.002) * 0.12, 0)
    return x


def ui_abrir(rng, v):
    """Abre um cartão ou ficha: duas notas subindo rápidas (si → mi) com um sopro leve."""
    n = n_de(0.34)
    x = np.zeros(n)
    poe(x, _plink(_SI5, 0.2, 0.06, 5) * 0.4, 0)
    poe(x, _plink(_MI6, 0.28, 0.09, 5) * 0.45, 0.055)
    w = n_de(0.22)
    poe(x, assobio(rng, w, 1500, 6000, 0.9, 0.45) * sobe_e_some(w, 0.5, 1.6) * 0.12, 0)
    return reverb(x, 0.3, 0.16, 9000)


def ui_fechar(rng, v):
    """Fecha: as mesmas duas notas descendo (mi → si), mais macias."""
    n = n_de(0.28)
    x = np.zeros(n)
    poe(x, _plink(_MI6, 0.16, 0.05, 4) * 0.32, 0)
    poe(x, _plink(_SI5, 0.22, 0.07, 4) * 0.34, 0.05)
    return reverb(x, 0.25, 0.12, 8000)


def ui_alternar(rng, v):
    """Interruptor: um clique de encaixe e uma nota curta (sobe quando liga)."""
    n = n_de(0.16)
    x = np.zeros(n)
    poe(x, passa(ruido(rng, n_de(0.012)), 1500, 6000, 2) * env(n_de(0.012), 0.0003, 0.003) * 0.25, 0)
    poe(x, _plink(_SOL6, 0.12, 0.04, 4) * 0.35, 0.02)
    return x


def ui_confirma(rng, v):
    """Botão principal: arpejo rápido mi–si–mi subindo, com peso por baixo e um brilho que fica no ar."""
    n = n_de(0.6)
    x = np.zeros(n)
    for k, m in enumerate((_MI5, _SI5, _MI6)):
        poe(x, _plink(m, 0.45, 0.14 + 0.05 * k, 6, 1.2) * (0.32 + 0.06 * k), k * 0.045)
    poe(x, _plink(_SI6, 0.4, 0.12, 3) * 0.08, 0.12)
    poe(x, _baque_menu(n_de(0.2), 120, 60, 0.06) * 0.35, 0)
    return reverb(x, 0.4, 0.22, 9000)


def ui_escolher(rng, v):
    """Escolheu o personagem (travou no trio): um acorde de sintetizador que estala,
    o peso de um soco por baixo, um sopro e faíscas subindo — o "selecionado!" dos jogos de luta."""
    n = n_de(0.8)
    x = np.zeros(n)
    acorde = sum(_plink(m, 0.6, 0.22, 8, 1.4) for m in (_MI5, _SOL5, _SI5)) / 3
    poe(x, satura(acorde * 1.8, 1.6) * 0.42, 0.01)
    poe(x, _plink(_MI6, 0.5, 0.2, 6, 1.3) * 0.22, 0.01)
    poe(x, _baque_menu(n_de(0.3), 150, 50, 0.09) * 0.6, 0)
    poe(x, passa(ruido(rng, n_de(0.03)), 1500, 7000, 2) * env(n_de(0.03), 0.0003, 0.008) * 0.35, 0)
    w = n_de(0.18)
    poe(x, assobio(rng, w, 800, 5000, 1.3, 0.45) * sobe_e_some(w, 0.85, 1.5) * 0.18, 0)
    for k, m in enumerate((_SI6, _MI6 + 12)):                                    # duas faíscas subindo
        poe(x, _plink(m, 0.18, 0.05, 3) * 0.1, 0.09 + 0.06 * k)
    return reverb(x, 0.45, 0.24, 9000)


def ui_arena(rng, v):
    """Entrar na arena: a energia sobe (vento e um tom subindo), estoura num impacto
    grande com um acorde de mi poderoso e um brilho metálico — o "LUTEM!"."""
    n = n_de(1.6)
    x = np.zeros(n)
    sobe = n_de(0.42)
    poe(x, assobio(rng, sobe, 300, 7000, 0.7, 0.5) * np.linspace(0, 1, sobe) ** 2 * 0.4, 0)
    poe(x, seno(varre(nota(52), nota(76), sobe, 0.8), sobe) * np.linspace(0, 1, sobe) ** 2 * 0.1, 0)
    em = 0.42
    m = n_de(1.1)
    t = np.arange(m) / SR
    boom = np.sin(2 * math.pi * np.cumsum(38 + 90 * np.exp(-t / 0.06)) / SR) * np.exp(-t / 0.45)
    poe(x, satura(boom * 1.4, 1.5) * 0.6, em)
    poe(x, passa(rosa(rng, m), 60, 2500, 2) * env(m, 0.001, 0.2) * 0.35, em)
    acorde = sum(_plink(mm, 1.0, 0.5, 9, 1.4) for mm in (52, 59, 64, 71))  # mi3, si3, mi4, si4
    poe(x, satura(acorde * 0.9, 2.2) * 0.32, em)
    poe(x, _plink(_MI6, 0.9, 0.4, 6, 1.3) * 0.16, em + 0.01)
    poe(x, passa(ruido(rng, n_de(0.6)), 5000, 12000, 2) * env(n_de(0.6), 0.002, 0.18) * 0.18, em)   # o brilho do prato
    return reverb(x, 0.6, 0.28, 8000)


# =================================================================== registro
SONS = {
    # físico
    "soco-leve": (soco_leve, "soco leve"), "soco-pesado": (soco_pesado, "golpe pesado"), "esmagar": (esmagar, "esmagar"),
    "gancho": (gancho, "golpe para cima"), "multi-golpe": (multi_golpe, "rajada de golpes"), "terremoto": (terremoto, "golpe no chão"),
    "onda-choque": (onda_choque, "onda de choque"),
    # cortes
    "corte": (corte, "corte"), "corte-pesado": (corte_pesado, "corte pesado"), "estocada": (estocada, "perfuração"),
    "corte-giratorio": (corte_giratorio, "corte giratório"), "lamina-energia": (lamina_energia, "lâmina de energia"),
    # projéteis e energia
    "disparo": (disparo, "disparo de energia"), "tiro": (tiro, "tiro"), "saraivada": (saraivada, "rajada de tiros"),
    "missil": (missil, "míssil"), "explosao": (explosao, "explosão"), "carga-pequena": (carga_pequena, "carga pequena"),
    "carga-grande": (carga_grande, "carga grande"), "feixe": (feixe, "feixe"), "impacto-energia": (impacto_energia, "impacto de energia"),
    # elementos
    "raio": (raio, "raio"), "fogo": (fogo, "fogo"), "gelo": (gelo, "gelo"), "vento": (vento, "vento"), "agua": (agua, "água"),
    "terra": (terra, "terra"), "veneno": (veneno, "veneno"),
    # magia
    "psiquico": (psiquico, "psíquico"), "sombra": (sombra, "sombra"), "luz": (luz, "luz sagrada"), "portal": (portal, "portal"),
    "maldicao": (maldicao, "maldição"), "prisao": (prisao, "prisão/correntes"), "selo": (selo, "selo"), "distorcao": (distorcao, "distorção"),
    # apoio
    "cura": (cura, "cura"), "escudo": (escudo, "Escudo"), "bloqueio": (bloqueio, "bloqueio"), "reforco": (reforco, "reforço"),
    "enfraquecer": (enfraquecer, "debuff"), "renova-buff": (renova_buff, "buff renovado"), "renova-debuff": (renova_debuff, "debuff renovado"), "purificar": (purificar, "purificar"), "dreno": (dreno, "dreno"),
    # eventos
    "interrupcao": (interrupcao, "interrupção"), "pronto": (pronto, "habilidade pronta"), "preparo": (preparo, "início do preparo"),
    "grand-carga": (grand_carga, "grande habilidade carregando"), "grand-impacto": (grand_impacto, "grande habilidade"),
    "nocaute": (nocaute, "nocaute"), "vitoria": (vitoria, "vitória"), "derrota": (derrota, "derrota"), "virada": (virada, "virada"),
    "transformacao": (transformacao, "transformação"), "toque": (toque, "toque de interface"),
    # interface
    "ui-clique": (ui_clique, "toque num botão"), "ui-confirma": (ui_confirma, "botão principal"),
    "ui-abrir": (ui_abrir, "abrir cartão ou menu"), "ui-fechar": (ui_fechar, "fechar"), "ui-alternar": (ui_alternar, "interruptor"),
    "ui-escolher": (ui_escolher, "personagem escolhido"), "ui-arena": (ui_arena, "entrar na arena"),
    "reacao": (reacao, "traço disparou (reação)"),
}

# Volume final de cada som (dB de RMS alvo), pela prioridade da mixagem do adendo:
# grand > impacto importante > interrupção > básico > buff/debuff > interface.
ALVO_DB = {
    "grand-impacto": -13, "grand-carga": -17, "transformacao": -15, "explosao": -15, "terremoto": -13, "esmagar": -15, "nocaute": -15,
    "interrupcao": -14, "vitoria": -17, "derrota": -18, "virada": -19,
    "soco-pesado": -14, "corte-pesado": -16, "feixe": -17, "raio": -14, "onda-choque": -16,
    "soco-leve": -16, "corte": -18, "estocada": -16, "disparo": -19, "tiro": -18, "gancho": -15, "multi-golpe": -16,
    "saraivada": -18, "missil": -18, "impacto-energia": -15, "lamina-energia": -18, "corte-giratorio": -18,
    "fogo": -18, "gelo": -19, "vento": -23, "agua": -19, "terra": -15, "veneno": -23,
    "psiquico": -23, "sombra": -19, "luz": -23, "portal": -23, "maldicao": -23, "prisao": -19, "selo": -24, "distorcao": -23,
    "cura": -24, "escudo": -23, "bloqueio": -19, "reforco": -24, "enfraquecer": -24, "renova-buff": -27, "renova-debuff": -26, "purificar": -25, "dreno": -23,
    "carga-pequena": -24, "carga-grande": -19, "pronto": -24, "preparo": -25, "toque": -26,
    "ui-clique": -27, "ui-confirma": -23, "ui-abrir": -27, "ui-fechar": -28, "ui-alternar": -28,
    "ui-escolher": -21, "ui-arena": -18, "reacao": -21,
}


def versao(nome: str, v: int) -> np.ndarray:
    fn, _ = SONS[nome]
    rng = np.random.default_rng(73000 + sum(map(ord, nome)) * 97 + v * 7919)
    x = fn(rng, v)
    # leve variação de tom e duração por versão (reamostragem), sem mexer no caráter
    fator = [1.0, 0.965, 1.035, 0.985][v % 4]
    if fator != 1.0:
        idx = np.arange(0, len(x) - 1, fator)
        x = np.interp(idx, np.arange(len(x)), x)
    x = apara(x - np.mean(x), -58)
    x = limita(x, -1.0)
    # volume pela prioridade, sem passar do teto
    alvo = ALVO_DB.get(nome, -19)
    ganho = 10 ** ((alvo - volume_percebido(x)) / 20)
    pico = np.max(np.abs(x)) * ganho
    # Os picos de transiente podem passar até ~4 dB do teto: uma saturação
    # suave (tanh) só arredonda esses instantes, como no master de som de jogo,
    # e o corpo do som chega ao volume certo. O que passar disso, abaixa.
    if pico > 1.15:
        ganho *= 1.15 / pico
    x = x * ganho
    x = 0.78 * np.tanh(x / 0.78)
    entra = min(len(x), n_de(0.002))
    x[:entra] *= np.linspace(0, 1, entra)
    return x.astype(np.float32)


def _registra_novos():
    """As famílias novas de efeito (tools/audio/sfx_familias.py), uma receita por família."""
    import importlib
    import sfx_familias
    SONS.update(sfx_familias.SONS_NOVOS)
    ALVO_DB.update(sfx_familias.ALVO_NOVO)
    # o som próprio de cada ataque básico (tools/audio/sfx_basicos_*.py), um módulo por lote
    for modulo in [f"sfx_basicos_{letra}" for letra in "abcdefghij"] + ["sfx_madara", "sfx_viagens", "sfx_ninjas", "sfx_cloud_dk", "sfx_naruto_ikki_luffy", "sfx_toph_gon", "sfx_piccolo", "sfx_herois", "sfx_hulk", "sfx_aiolia_arthas", "sfx_aang_sakura", "sfx_ciclope_shaka_mummra", "sfx_sasuke_aranha_trunks_kuririn_kratos", "sfx_omniman_guts_rick"]:
        m = importlib.import_module(modulo)
        for nome, (fn, desc) in m.SONS.items():
            SONS[nome] = (fn, desc)
            ALVO_DB[nome] = -15


def main(argv):
    _registra_novos()
    OUT.mkdir(parents=True, exist_ok=True)
    caminho = OUT / "manifest.json"
    manifesto = json.loads(caminho.read_text()) if caminho.exists() and argv else {}
    sons = manifesto.get("sons", {}) if argv else {}
    total = 0
    for nome in argv or SONS:
        partes, offsets, duracoes = [], [], []
        pos = 0.0
        for v in range(VERSOES):
            x = versao(nome, v)
            offsets.append(round(pos, 4))
            duracoes.append(round(len(x) / SR, 4))
            partes += [x, np.zeros(n_de(RESPIRO), np.float32)]
            pos += len(x) / SR + RESPIRO
        audio = np.concatenate(partes)
        destino = OUT / f"{nome}.mp3"
        sf.write(destino, audio, SR, format="MP3", subtype="MPEG_LAYER_III", compression_level=0.45)
        total += destino.stat().st_size
        sons[nome] = {"arquivo": destino.name, "descricao": SONS[nome][1], "versoes": offsets, "duracoes": duracoes, "bytes": destino.stat().st_size}
        print(f"{nome:16s} {destino.stat().st_size / 1024:6.1f} KB  {max(duracoes):.2f} s  {SONS[nome][1]}")
    caminho.write_text(json.dumps({"taxa": SR, "versoes": VERSOES, "sons": dict(sorted(sons.items()))}, indent=1, ensure_ascii=False) + "\n")
    print(f"total {total / 1024:.0f} KB")


if __name__ == "__main__":
    main(sys.argv[1:])
