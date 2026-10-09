#!/usr/bin/env python3
"""
Famílias de efeitos visuais (adendo, parte 3).

Um roster de 250 lutadores não cabe em treze desenhos. Aqui ficam as folhas
reutilizáveis — impactos, cortes, projéteis, feixes, elementos, magia, apoio —
que o jogo combina por FAMÍLIA + VARIANTE + COR + ESCALA + DIREÇÃO +
INTENSIDADE + TEMPO + CAMADAS (src/presentation/vfxFamilies.ts).

Cada folha é luz em tons neutros (veja tools/vfx/luz.py): o jogo pinta o
brilho com a cor do personagem e põe o núcleo claro por cima. Física e
movimento saem de contas, não de desenho à mão: faíscas são balísticas com
gravidade, fumaça e chama são ruído suavizado e advectado, raios e
rachaduras são deslocamento de ponto médio, cortes varrem um arco com cabeça
grossa e cauda que afina.

Determinístico: a mesma semente gera os mesmos quadros.

Uso: python3 tools/vfx/generate_families.py [nome ...]
     (gera public/assets/vfx/familias/*.webp e manifest.json)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from luz import Tela, apaga, ease_in, ease_out, jagged, janela, pulso, smooth, some  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public/assets/vfx/familias"
COLS, ROWS, FRAMES = 3, 4, 12

GRANDE = Tela(192)      # impactos, área, elementos
MEDIA = Tela(160)       # projéteis em viagem e preparo
FAIXA = Tela(512, 96)   # feixes, raios e drenos, esticados entre dois pontos


def vazio(T: Tela):
    return T.zero(), T.zero()


def faiscas(T: Tela, rng, t, n, alcance, largura, cone=(0, 2 * math.pi), gravidade=0.0, cx=0.0, cy=0.0, cauda=0.3, inicio=0.0):
    """Faíscas balísticas: saem do centro, desaceleram e caem.

    O comprimento do risco é o borrão de movimento: longo enquanto a faísca
    voa rápido, curto quando ela perde velocidade. A cabeça ganha um ponto
    quente, para não virar uma "seta".
    """
    tt = max(0.0, (t - inicio) / max(1e-4, 1 - inicio))
    if tt <= 0:
        return T.zero()
    segs, cabecas = [], []
    for _ in range(n):
        a = rng.uniform(*cone)
        sp = rng.uniform(0.55, 1.05) * alcance
        vida = rng.uniform(0.65, 1.0)
        if tt > vida:
            continue
        u = tt / vida
        d = sp * ease_out(u, 2.4)
        d0 = sp * ease_out(max(0.0, u - cauda * 0.6), 2.4)
        d0 = min(d0, d - 0.03)
        g, g0 = gravidade * u * u, gravidade * max(0.0, u - cauda * 0.6) ** 2
        w = (1 - u) ** 1.1 * rng.uniform(0.7, 1.25)
        segs.append((cx + math.cos(a) * d0, cy + math.sin(a) * d0 + g0, cx + math.cos(a) * d, cy + math.sin(a) * d + g, w))
        cabecas.append((cx + math.cos(a) * d, cy + math.sin(a) * d + g, w))
    rastro = T.lines(segs, largura * 0.45, largura * 0.12)
    return rastro + T.splats(cabecas, largura * 0.35) * 0.9


# =================================================================== FÍSICO
def soco(T, t, rng):
    """Impacto leve: clarão curto, anel fino e faíscas rápidas."""
    G, H = vazio(T)
    flash = T.gauss(0, 0, 0.09 + 0.05 * t) * some(t, 0, 0.45, 1.2) * 3.0
    anel = T.ring(0.12 + 0.55 * ease_out(t, 2.5), 0.03 * (1 - t) + 0.006) * (1 - t) ** 1.5 * 1.4
    fa = faiscas(T, rng, t, 16, 0.85, 0.035, cauda=0.35)
    star = T.flare(0, 0, 1.1, 0.35) * some(t, 0, 0.35, 1) * 2.2
    G += flash + anel + T.glow(fa, 1.0, 1.3, 0.02) + star
    H += flash * 1.1 + fa * 0.8 + star * 0.9
    return G, H


def golpe_pesado(T, t, rng):
    """Impacto pesado: dois anéis, clarão grande, estilhaços com gravidade."""
    G, H = vazio(T)
    flash = T.gauss(0, 0, 0.13 + 0.08 * t) * some(t, 0, 0.5, 1.1) * 3.6
    a1 = T.ring(0.15 + 0.7 * ease_out(t, 2.2), 0.05 * (1 - t) + 0.008) * (1 - t) ** 1.3 * 1.6
    a2 = T.ring(0.08 + 0.5 * ease_out(max(0, t - 0.12) * 1.15, 2), 0.035 * (1 - t) + 0.006) * some(t, 0.12, 1) * 1.1
    fa = faiscas(T, rng, t, 28, 0.95, 0.045, gravidade=0.25, cauda=0.32)
    lasca = []
    for _ in range(12):
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(0.25, 0.8) * ease_out(t, 2)
        x, y = math.cos(a) * d, math.sin(a) * d + 0.5 * t * t
        s = rng.uniform(0.02, 0.045) * (1 - 0.5 * t)
        r0 = rng.uniform(0, 6.3) + t * rng.uniform(-8, 8)
        lasca.append(([(x + s * math.cos(r0 + k * 2.2), y + s * math.sin(r0 + k * 2.2)) for k in range(3)], (1 - t) ** 1.2))
    pedras = T.polys(lasca, blur=0.003)
    star = T.flare(0, 0, 1.7, 0.6) * some(t, 0, 0.4, 1.2) * 2.6
    G += flash + a1 + a2 + T.glow(fa, 1.0, 1.4, 0.025) + pedras * 1.2 + star
    H += flash * 1.2 + fa * 0.8 + star + a1 * 0.3
    return G, H


def esmagar(T, t, rng):
    """De cima para baixo: linhas de velocidade descendo, chão achatado e rachaduras."""
    G, H = vazio(T)
    chao = 0.32
    desce = ease_in(min(1, t / 0.28), 2)
    linhas = []
    for i in range(10):
        x = rng.uniform(-0.45, 0.45)
        y2 = -0.9 + (chao + 0.9) * desce
        linhas.append((x * 0.7, y2 - rng.uniform(0.3, 0.6), x * 0.35, y2, 0.8 * apaga(t, 0.18, 0.4)))
    vel = T.tapered(linhas, 0.03)
    bate = some(t, 0.26, 1)
    onda = T.ring(0.1 + 0.85 * ease_out(max(0, t - 0.26) / 0.74, 2.2), 0.05 * (1 - t) + 0.01, cy=chao, squash=3.2) * bate * 1.6
    flash = T.gauss(0, chao, 0.22, 0.07) * some(t, 0.26, 0.6) * 3.2
    rach = T.zero()
    if t > 0.26:
        cres = ease_out((t - 0.26) / 0.4, 2)
        for k in range(7):
            a = math.pi * (k / 6) + rng.uniform(-0.15, 0.15)
            alc = rng.uniform(0.45, 0.85) * cres
            pts = jagged(rng, 0, chao, math.cos(a) * alc, chao + math.sin(a) * alc * 0.28 * (1 if k % 2 else -1), 3, 0.12)
            rach += T.polyline(pts, 0.016, 1.0)
        rach *= apaga(t, 0.5, 1, 1.2)
    poeira = T.zero()
    if t > 0.26:
        tt = (t - 0.26) / 0.74
        pts = []
        for _ in range(26):
            lado = rng.choice([-1, 1])
            d = rng.uniform(0.2, 0.85) * ease_out(tt, 2)
            pts.append((lado * d, chao - rng.uniform(0, 0.25) * ease_out(tt, 1.5), (1 - tt) ** 1.4 * rng.uniform(0.4, 1)))
        poeira = T.splats(pts, 0.045)
    G += T.glow(vel, 1.0, 1.0, 0.02) + onda + flash + T.glow(rach, 0.9, 2.0, 0.018) + poeira * 0.5
    H += vel * 0.6 + flash * 1.1 + rach * 0.8
    return G, H


def gancho(T, t, rng):
    """Para cima: arco de baixo para o alto, faíscas subindo."""
    G, H = vazio(T)
    cab = 2.3 + 2.5 * ease_out(min(1, t / 0.38), 2.4)
    arco = T.arc_band(0.58, 0.15, max(2.3, cab - 2.0), cab, squash=0.85, rot=0.0, cx=0.18, cy=0.12) * apaga(t, 0.32, 1, 1.3)
    linhas = []
    for _ in range(9):
        x = rng.uniform(-0.5, 0.5)
        y = 0.7 - 1.6 * ease_out(t, 2) * rng.uniform(0.6, 1)
        linhas.append((x, y + 0.45, x, y, apaga(t, 0.1, 0.8) * 0.8))
    vel = T.tapered(linhas, 0.025)
    fa = faiscas(T, rng, t, 18, 0.9, 0.035, cone=(-math.pi * 0.9, -math.pi * 0.1), gravidade=0.5, cy=-0.25, inicio=0.25)
    flash = T.gauss(0.1, -0.35, 0.12) * pulso(t, 0.25, 0.6) * 3
    fio = T.arc_band(0.62, 0.025, max(2.3, cab - 2.0), cab, squash=0.85, cx=0.18, cy=0.12) * apaga(t, 0.32, 1, 1.3)
    G += T.glow(arco, 1.0, 1.2, 0.03) + T.glow(fio, 1.5, 0.6, 0.008) + T.glow(vel, 1, 1, 0.015) + T.glow(fa, 1, 1.3, 0.02) + flash
    H += arco * 0.3 + fio * 1.4 + fa * 0.8 + flash
    return G, H


def terremoto(T, t, rng):
    """Golpe no chão para área: anéis em perspectiva, rachaduras e pedras jogadas."""
    G, H = vazio(T)
    cy = 0.25
    for k, atraso in enumerate((0, 0.12, 0.26)):
        tt = max(0, t - atraso) / (1 - atraso)
        if tt > 0:
            G += T.ring(0.1 + 0.85 * ease_out(tt, 2.3), 0.05 * (1 - tt) + 0.01, cy=cy, squash=3.0) * (1 - tt) ** 1.4 * (1.6 - 0.4 * k)
    rach = T.zero()
    cres = ease_out(t / 0.5, 2)
    for k in range(12):
        a = 2 * math.pi * k / 12 + rng.uniform(-0.2, 0.2)
        alc = rng.uniform(0.5, 0.9) * cres
        pts = jagged(rng, 0, cy, math.cos(a) * alc, cy + math.sin(a) * alc / 3.0, 3, 0.12)
        rach += T.polyline(pts, 0.016, 1)
    rach *= apaga(t, 0.45, 1)
    pedras = []
    for _ in range(16):
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(0.15, 0.7)
        vx = math.cos(a) * d
        vy = -rng.uniform(0.8, 1.5)
        x = vx * ease_out(t, 1.5)
        y = cy + math.sin(a) * d / 3 + vy * t + 2.2 * t * t
        if y > cy + 0.15:
            continue
        s = rng.uniform(0.02, 0.045)
        r0 = rng.uniform(0, 6.3) + t * 7
        pedras.append(([(x + s * math.cos(r0 + j * 1.6), y + s * math.sin(r0 + j * 1.6)) for j in range(4)], (1 - t) ** 0.8))
    rock = T.polys(pedras, 0.003)
    flash = T.gauss(0, cy, 0.3, 0.09) * some(t, 0, 0.45) * 2.8
    poeira = T.splats([(math.cos(a) * 0.7 * ease_out(t, 2), cy + math.sin(a) * 0.23 * ease_out(t, 2) - 0.1 * t, (1 - t) ** 1.3) for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)], 0.07)
    G += T.glow(rach, 0.9, 2.0, 0.018) + rock * 1.1 + flash + poeira * 0.45
    H += rach * 0.9 + flash
    return G, H


def onda_de_choque(T, t, rng):
    """Anéis concêntricos finos, um atrás do outro, com marcas de pressão."""
    G, H = vazio(T)
    for k, atraso in enumerate((0, 0.1, 0.2, 0.3)):
        tt = max(0, t - atraso) / (1 - atraso)
        if tt > 0:
            r = 0.08 + 0.85 * ease_out(tt, 2.4)
            borda = T.ring(r, 0.018 + 0.02 * (1 - tt)) * (1 - tt) ** 1.3 * (1.5 - 0.25 * k)
            interno = T.ring(r - 0.07, 0.06) * (1 - tt) ** 2 * 0.35
            G += borda + interno
            H += borda * 0.6
    marcas = []
    for i in range(24):
        a = 2 * math.pi * i / 24 + rng.uniform(-0.05, 0.05)
        r = 0.15 + 0.8 * ease_out(t, 2.1)
        marcas.append((math.cos(a) * (r - 0.09), math.sin(a) * (r - 0.09), math.cos(a) * r, math.sin(a) * r, (1 - t) ** 1.6 * 0.9))
    m = T.tapered(marcas, 0.02)
    flash = T.gauss(0, 0, 0.1) * some(t, 0, 0.35) * 3
    G += T.glow(m, 1, 0.8, 0.012) + flash
    H += m * 0.5 + flash
    return G, H


def rajada_de_golpes(T, t, rng):
    """Vários golpes rápidos em pontos diferentes, um depois do outro."""
    G, H = vazio(T)
    pontos = [(rng.uniform(-0.45, 0.45), rng.uniform(-0.45, 0.45)) for _ in range(7)]
    for i, (x, y) in enumerate(pontos):
        a = i * 0.1
        tt = (t - a) / 0.38
        if 0 < tt < 1:
            fl = T.gauss(x, y, 0.06 + 0.03 * tt) * (1 - tt) ** 2 * 3
            an = T.ring(0.05 + 0.25 * ease_out(tt, 2), 0.02, cx=x, cy=y) * (1 - tt) ** 1.4 * 1.3
            st = T.flare(x, y, 0.6, rng.uniform(0, 1.5)) * (1 - tt) ** 3 * 2
            sub = np.random.default_rng(i + 7)
            fa = faiscas(T, sub, tt, 6, 0.32, 0.025, cx=x, cy=y, cauda=0.4)
            G += fl + an + st + T.glow(fa, 1, 1.2, 0.015)
            H += fl + st * 0.8 + fa * 0.7
    return G, H


# =================================================================== CORTES
def _corte(T, t, rng, rot=0.0, raio=0.86, squash=0.26, atraso=0.0, dur=0.42, largura=0.16, centelhas=True):
    G, H = vazio(T)
    tt = (t - atraso)
    if tt <= 0:
        return G, H
    var = ease_out(min(1, tt / dur), 2.6)
    a_ini, a_fim = math.pi * 0.98, math.pi * 2.08
    cab = a_ini + (a_fim - a_ini) * var
    # a cauda persegue a cabeça: o corte se fecha sozinho em vez de congelar
    recolhe = ease_in(min(1, max(0.0, tt - dur * 0.55) / 0.45), 1.6)
    cauda = max(a_ini, cab - 2.4 * (1 - recolhe))
    vida = apaga(tt, dur * 0.7, 1 - atraso, 1.3)
    # o arco passa pelo centro do alvo, não por cima dele
    oy = raio * squash * 0.85
    ox, oy = -oy * math.sin(rot), oy * math.cos(rot)
    banda = T.arc_band(raio, largura, cauda, cab, squash=squash, rot=rot, cx=ox, cy=oy, crescente=True) * vida
    fio = T.arc_band(raio + largura * 0.3, largura * 0.2, cauda, cab, squash=squash, rot=rot, cx=ox, cy=oy, crescente=True) * vida
    G += T.glow(banda, 1.0, 1.0, 0.03) + T.glow(fio, 1.6, 0.8, 0.008)
    H += fio * 1.6 + banda * 0.25
    if cab - cauda < 0.05:
        return G, H
    if centelhas and tt > dur * 0.8:
        hx = raio * math.cos(a_fim)
        hy = raio * math.sin(a_fim) * squash
        cx = hx * math.cos(rot) - hy * math.sin(rot) + ox
        cy = hx * math.sin(rot) + hy * math.cos(rot) + oy
        tangente = a_fim + math.pi / 2 + rot
        fa = faiscas(T, rng, (tt - dur * 0.8) / (1 - atraso - dur * 0.8), 10, 0.5, 0.025, cone=(tangente - 0.6, tangente + 0.6), cx=cx, cy=cy, gravidade=0.3)
        G += T.glow(fa, 1, 1.2, 0.015)
        H += fa * 0.8
    return G, H


def corte(T, t, rng):
    return _corte(T, t, rng, rot=-0.18)


def corte_cruzado(T, t, rng):
    g1, h1 = _corte(T, t, rng, rot=0.7, dur=0.34, centelhas=False, squash=0.2)
    g2, h2 = _corte(T, t, rng, rot=-0.7 + math.pi, atraso=0.16, dur=0.34, centelhas=False, squash=0.2)
    x = T.flare(0, 0, 0.9, 0.785) * pulso(t, 0.4, 0.8) * 1.6 + T.gauss(0, 0, 0.09) * pulso(t, 0.4, 0.8) * 2.0
    return g1 + g2 + x, h1 + h2 + x


def estocada(T, t, rng):
    """Perfuração: lança fina de trás para a frente (+x), com estouro na ponta."""
    G, H = vazio(T)
    ent = ease_out(min(1, t / 0.22), 3)
    ponta = -0.7 + 1.35 * ent
    vida = apaga(t, 0.25, 1, 1.4)
    corpo = T.polys([([(-0.9, -0.0), (ponta - 0.25, -0.05), (ponta, 0.0), (ponta - 0.25, 0.05)], 1.0)], blur=0.006) * vida
    fio = T.lines([(-0.85, 0, ponta, 0, 1)], 0.012, 0.003) * vida
    estouro = T.zero()
    if t > 0.18:
        tt = min(1.0, (t - 0.18) / 0.82)
        estouro += T.ring(0.05 + 0.32 * ease_out(tt, 2), 0.014, cx=ponta, squash=0.45) * (1 - tt) ** 1.8 * 1.0
        estouro += T.glow(faiscas(T, rng, tt, 14, 0.45, 0.025, cone=(-0.7, 0.7), cx=ponta), 1, 1.2, 0.015)
        estouro += T.gauss(ponta, 0, 0.07) * (1 - tt) ** 2.5 * 3
    G += T.glow(corpo, 1.3, 1.6, 0.03) + T.glow(fio, 1.8, 0.8, 0.008) + estouro
    H += fio * 1.4 + corpo * 0.3 + estouro * 0.7
    return G, H


def corte_giratorio(T, t, rng):
    """Giro completo: uma volta e meia de lâmina em perspectiva."""
    G, H = vazio(T)
    var = ease_out(min(1, t / 0.6), 2)
    cab = -math.pi / 2 + 3 * math.pi * var
    vida = apaga(t, 0.55, 1, 1.2)
    for k, (r, sq) in enumerate(((0.66, 0.38), (0.5, 0.38))):
        b = T.arc_band(r, 0.12 - 0.03 * k, cab - 3.6, cab, squash=sq, rot=-0.12, crescente=True) * vida
        f = T.arc_band(r + 0.03, 0.024, cab - 3.6, cab, squash=sq, rot=-0.12, crescente=True) * vida
        G += T.glow(b, 0.9, 1.0, 0.03) * (1 - 0.4 * k) + T.glow(f, 1.5, 0.7, 0.008)
        H += f * 1.4
    # o ar deslocado aparece depois que a lâmina passa
    vento = T.ring(0.7 + 0.12 * ease_out(max(0, t - 0.35) / 0.65), 0.05, squash=1 / 0.38) * some(t, 0.35, 1) * janela(t, 0.3, 0.4) * 0.5
    G += vento
    return G, H


def corte_de_energia(T, t, rng):
    """Lâmina de energia larga que cresce para a frente (+x)."""
    G, H = vazio(T)
    ex = ease_out(t, 1.6)
    cx = -0.75 + 0.85 * ex
    vida = apaga(t, 0.45, 1, 1.3)
    b = T.arc_band(0.5 + 0.1 * ex, 0.2, -1.2, 1.2, squash=1.0, cx=cx, crescente=True) * vida
    nucleo = T.arc_band(0.56 + 0.1 * ex, 0.05, -1.1, 1.1, squash=1.0, cx=cx, crescente=True) * vida
    pts = []
    for _ in range(40):
        a = rng.uniform(-1.0, 1.0)
        r = 0.6 + 0.1 * ex - rng.uniform(0, 0.35)
        pts.append((cx + r * math.cos(a), r * math.sin(a), vida * rng.uniform(0.2, 0.8)))
    rastro = T.splats(pts, 0.03)
    G += T.glow(b, 1, 1.3, 0.04) + T.glow(nucleo, 1.4, 1, 0.01) + rastro * 0.8
    H += nucleo * 1.5 + b * 0.3 + rastro * 0.2
    return G, H


# =================================================================== PROJÉTEIS (em laço, apontando para +x)
TAU = 2 * math.pi


def _cauda_de_particulas(T, rng, t, n, x0, x1, espalha, sigma, vel=1.0):
    """Partículas que escorrem para trás (−x) em laço perfeito."""
    pts = []
    for i in range(n):
        fase = (rng.uniform(0, 1) + t * vel) % 1.0
        x = x0 + (x1 - x0) * fase
        y = rng.normal(0, espalha) * (0.3 + fase)
        pts.append((x, y, (1 - fase) ** 1.3 * rng.uniform(0.5, 1.1)))
    return T.splats(pts, sigma)


def tiro(T, t, rng):
    """Bala traçante: cabeça quente, risco longo atrás."""
    G, H = vazio(T)
    tremor = 0.02 * math.sin(TAU * t * 3)
    cabeca = T.gauss(0.42, 0, 0.05, 0.03) * 2.6
    risco = T.polys([([(-0.85, 0), (0.38, -0.03 - tremor), (0.46, 0), (0.38, 0.03 + tremor)], 1)], blur=0.006)
    G += cabeca + T.glow(risco, 0.9, 1.2, 0.03)
    H += cabeca * 1.2 + risco * 0.7
    return G, H


def saraivada(T, t, rng):
    """Rajada múltipla: três traçantes em formação, defasados."""
    G, H = vazio(T)
    for k, (dy, dx) in enumerate(((-0.28, -0.25), (0, 0.15), (0.28, -0.1))):
        x = dx + 0.06 * math.sin(TAU * (t + k / 3))
        cab = T.gauss(x + 0.3, dy, 0.04, 0.025) * 2.4
        risco = T.polys([([(x - 0.55, dy), (x + 0.27, dy - 0.022), (x + 0.33, dy), (x + 0.27, dy + 0.022)], 1)], blur=0.005)
        G += cab + T.glow(risco, 0.9, 1.1, 0.025)
        H += cab + risco * 0.6
    return G, H


def missil(T, t, rng):
    """Míssil: corpo claro, jato de chama e fumaça que fica para trás."""
    G, H = vazio(T)
    corpo = T.polys([([(0.18, -0.05), (0.46, -0.035), (0.56, 0), (0.46, 0.035), (0.18, 0.05)], 1)], blur=0.004)
    jato_len = 0.32 + 0.05 * math.sin(TAU * t * 4)
    jato = T.polys([([(0.18, -0.045), (0.18 - jato_len, 0), (0.18, 0.045)], 1)], blur=0.02)
    fumo = _cauda_de_particulas(T, rng, t, 30, 0.05, -0.95, 0.05, 0.05)
    G += corpo * 1.6 + T.glow(jato, 1.4, 1.2, 0.03) + fumo * 0.55 + T.gauss(0.18, 0, 0.08) * 1.4
    H += jato * 1.4 + T.gauss(0.16, 0, 0.05) * 1.6 + corpo * 0.4
    return G, H


def orbe(T, t, rng):
    """Esfera de energia: núcleo, casca e arcos girando, centelhas em órbita."""
    G, H = vazio(T)
    r = 0.24 * (1 + 0.04 * math.sin(TAU * t * 2))
    nucleo = T.gauss(0.12, 0, r * 0.55) * 2.4
    casca = T.ring(r, 0.035, cx=0.12) * 1.3
    arcos = T.zero()
    for k in range(3):
        a0 = TAU * (t + k / 3)
        arcos += T.arc_band(r * 1.05, 0.03, a0, a0 + 1.6, squash=0.55 + 0.25 * k, rot=k * 1.1, cx=0.12)
    rastro = _cauda_de_particulas(T, rng, t, 26, 0.0, -0.85, 0.07, 0.03, vel=2)
    halo = T.gauss(0.12, 0, r * 1.6) * 0.8
    estrela = T.flare(0.12, 0, 0.9, TAU * t / 4) * 0.9
    G += nucleo + casca + T.glow(arcos, 1, 1, 0.02) + rastro * 0.9 + halo + estrela
    H += nucleo * 1.2 + arcos * 0.8 + estrela * 0.6
    return G, H


def crescente(T, t, rng):
    """Onda em meia-lua voando (Getsuga, lâmina de vento): convexa para a frente."""
    G, H = vazio(T)
    bate = 0.03 * math.sin(TAU * t * 2)
    banda = T.arc_band(0.5, 0.16, -1.25, 1.25, cx=-0.2 + bate, crescente=False, taper=0.0)
    fina = T.arc_band(0.55, 0.035, -1.15, 1.15, cx=-0.2 + bate, taper=0.0)
    pontas = (1 - smooth(np.abs(T.ANG), 0.7, 1.3))
    rastro = _cauda_de_particulas(T, rng, t, 40, 0.15, -0.9, 0.22, 0.03, vel=2)
    G += T.glow(banda * pontas, 1, 1.3, 0.04) + T.glow(fina, 1.6, 0.8, 0.01) + rastro * 0.7
    H += fina * 1.5 + banda * pontas * 0.3
    return G, H


def bola_de_fogo(T, t, rng):
    """Bola de fogo: núcleo quente e língua de chama que escorre para trás."""
    G, H = vazio(T)
    n = T.noise(np.random.default_rng(7), 0.06, 3)
    # a chama "corre" para trás: deslocamos o ruído em x ao longo do laço (período = largura do campo)
    k = int(t * T.W) % T.W
    n = np.roll(n, k, axis=1)
    forma = np.exp(-(((T.U - 0.2) / 0.22) ** 2 + (T.V / 0.2) ** 2))
    cauda = np.exp(-(T.V / (0.08 + 0.12 * np.clip(0.2 - T.U, 0, 1))) ** 2) * smooth(T.U, -0.9, 0.0) * (T.U < 0.25)
    chama = np.clip(forma * 1.2 + cauda * 0.9 + n * 0.25 * (forma + cauda), 0, None)
    G += chama * 1.6 + T.gauss(0.2, 0, 0.3) * 0.5
    H += np.clip(forma * 1.3 - 0.35, 0, None) * 2.2 + np.clip(cauda + n * 0.2 - 0.7, 0, None) * 1.0
    return G, H


def estilhaco(T, t, rng):
    """Lança de gelo: cristal em losango com facetas e rastro de geada."""
    G, H = vazio(T)
    face_a = T.polys([([(-0.25, 0), (0.15, -0.09), (0.55, 0), (0.15, 0)], 1.0)], 0.002)
    face_b = T.polys([([(-0.25, 0), (0.15, 0), (0.55, 0), (0.15, 0.09)], 0.55)], 0.002)
    aresta = T.lines([(-0.25, 0, 0.55, 0, 1)], 0.008, 0.002)
    brilho = T.flare(0.5 - 0.6 * ((t * 1.0) % 1), 0, 0.5, 0.3) * pulso(t, 0.0, 1.0)
    geada = _cauda_de_particulas(T, rng, t, 40, -0.2, -0.95, 0.06, 0.018, vel=1.5)
    G += T.glow(face_a + face_b, 1.1, 0.8, 0.03) + aresta * 1.4 + geada * 0.9 + brilho * 1.4
    H += aresta * 1.4 + face_a * 0.45 + brilho
    return G, H


def rocha(T, t, rng):
    """Pedra arremessada: bloco girando com poeira atrás."""
    G, H = vazio(T)
    a = TAU * t
    pts = []
    sub = np.random.default_rng(11)
    raios = sub.uniform(0.15, 0.24, 7)
    for i in range(7):
        ang = a + TAU * i / 7
        pts.append((0.15 + raios[i] * math.cos(ang), raios[i] * math.sin(ang)))
    bloco = T.polys([(pts, 1.0)], 0.003)
    luz = T.polys([([(0.15, 0)] + pts[1:4], 0.6)], 0.004)
    poeira = _cauda_de_particulas(T, rng, t, 34, -0.05, -0.95, 0.09, 0.05)
    G += bloco * 1.5 + luz * 0.4 + poeira * 0.45
    H += luz * 0.25
    return G, H


def carga(T, t, rng):
    """Preparo: partículas convergindo para um núcleo que cresce (em laço)."""
    G, H = vazio(T)
    segs = []
    for i in range(22):
        fase = (rng.uniform(0, 1) + t) % 1.0
        a = rng.uniform(0, TAU)
        r1 = 0.85 * (1 - fase) + 0.12
        r0 = r1 + 0.18 * (1 - fase)
        segs.append((math.cos(a) * r0, math.sin(a) * r0, math.cos(a) * r1, math.sin(a) * r1, fase ** 0.8))
    linhas = T.lines(segs, 0.016, 0.004)
    nucleo = T.gauss(0, 0, 0.12 + 0.02 * math.sin(TAU * t * 2)) * 2.0
    anel = T.ring(0.5 - 0.3 * ((t * 2) % 1), 0.03) * (1 - (t * 2) % 1) * 0.9
    G += T.glow(linhas, 1, 1.2, 0.015) + nucleo + anel
    H += linhas * 0.8 + nucleo * 1.2
    return G, H


# =================================================================== FAIXAS (feixe esticado de quem age até o alvo)
def _ruido_faixa(T, seed, escala):
    return T.noise(np.random.default_rng(seed), escala, 3)


def feixe(T, t, rng):
    """Feixe fino: núcleo branco, halo e pulsos correndo para o alvo."""
    G, H = vazio(T)
    n = np.roll(_ruido_faixa(T, 21, 0.04), int(t * T.W), axis=1)
    larg = 0.022 * (1 + 0.15 * n)
    perfil = np.exp(-(T.V / larg) ** 2)
    halo = np.exp(-(T.V / (larg * 3.2)) ** 2)
    ondas = 0.75 + 0.25 * np.sin((T.U * 9 - t * TAU * 3))
    ponta = smooth(T.U, -0.99, -0.9) * smooth(-T.U, -0.99, -0.92)
    G += (perfil * 1.8 + halo * 0.9 * ondas) * ponta
    H += perfil * 1.6 * ponta
    return G, H


def feixe_pesado(T, t, rng):
    """Feixe largo (Kamehameha): coluna grossa, fios em espiral e turbulência."""
    G, H = vazio(T)
    n = np.roll(_ruido_faixa(T, 23, 0.03), int(t * T.W), axis=1)
    larg = 0.06 * (1 + 0.12 * n)
    perfil = np.exp(-np.abs(T.V / larg) ** 2.4)
    halo = np.exp(-(T.V / (larg * 2.4)) ** 2)
    fios = T.zero()
    for k in range(2):
        y = 0.07 * np.sin(T.U * 14 - t * TAU * 2 + k * math.pi)
        fios += np.exp(-((T.V - y) / 0.012) ** 2) * (0.5 + 0.5 * np.cos(T.U * 14 - t * TAU * 2 + k * math.pi))
    ponta = smooth(T.U, -0.99, -0.88) * smooth(-T.U, -0.99, -0.94)
    G += (perfil * 2.0 + halo * 1.0 + fios * 0.9 + np.clip(n, 0, None) * halo * 0.3) * ponta
    H += (np.clip(perfil * 1.6 - 0.25, 0, None) + fios * 0.5) * ponta
    return G, H


def raio_faixa(T, t, rng):
    """Raio entre dois pontos: linha quebrada que muda a cada quadro, com galhos."""
    G, H = vazio(T)
    sub = np.random.default_rng(int(t * 1000) + 31)
    alto = T.H / T.W
    pts = jagged(sub, -0.97, 0, 0.97, 0, 7, 0.06)
    pts = [(x, max(-alto * 0.8, min(alto * 0.8, y))) for x, y in pts]
    tronco = T.polyline(pts, 0.012, 1.0)
    galhos = T.zero()
    for _ in range(4):
        i = sub.integers(10, len(pts) - 10)
        x, y = pts[i]
        g = jagged(sub, x, y, x + sub.uniform(0.1, 0.3), y + sub.choice([-1, 1]) * sub.uniform(0.05, alto * 0.7), 4, 0.15)
        galhos += T.polyline(g, 0.005, 0.7)
    ponta = smooth(T.U, -0.99, -0.95) * smooth(-T.U, -0.99, -0.95)
    G += T.glow(tronco + galhos, 1.6, 1.6, 0.012) * ponta
    H += (tronco * 1.6 + galhos * 0.8) * ponta
    return G, H


def dreno(T, t, rng):
    """Transferência: fios de partículas correndo do alvo (+x) até quem age."""
    G, H = vazio(T)
    pts = []
    for i in range(110):
        fase = (rng.uniform(0, 1) + t) % 1.0
        x = 0.95 - 1.9 * fase
        y = 0.08 * math.sin(fase * 9 + i) * math.sin(math.pi * fase)
        pts.append((x, y, math.sin(math.pi * fase) * rng.uniform(0.5, 1)))
    part = T.splats(pts, 0.006)
    fio = np.exp(-(T.V / 0.03) ** 2) * (0.5 + 0.5 * np.sin(T.U * 12 + t * TAU * 2)) * 0.35
    ponta = smooth(T.U, -0.99, -0.9) * smooth(-T.U, -0.99, -0.9)
    G += (T.glow(part, 1.2, 1.4, 0.02) + fio) * ponta
    H += part * 0.9 * ponta
    return G, H


# =================================================================== ENERGIA
def explosao(T, t, rng):
    """Explosão: bola que cresce com turbulência, anel, brasas; esfria e vira fumaça."""
    G, H = vazio(T)
    n = T.noise(np.random.default_rng(41), 0.09, 3)
    r = 0.12 + 0.6 * ease_out(t, 2.6)
    d = T.RAD / max(r, 1e-3) + n * 0.09
    bola = smooth(-d, -1.05, -0.55)
    casca = np.exp(-((d - 0.85) / 0.18) ** 2)
    quente = max(0.0, 1 - t * 1.6)
    fumo = bola * (0.4 + 0.3 * n) * janela(t, 0.25, 0.6) * (1 - t) ** 0.8
    G += bola * (1.8 * (1 - t) ** 0.9) + casca * (1 - t) * 1.2 + fumo * 0.8
    H += bola * quente * 2.4 + casca * quente * 0.8
    G += T.ring(0.15 + 0.8 * ease_out(t, 2.2), 0.04 * (1 - t) + 0.008) * (1 - t) ** 1.6 * 1.6
    fa = faiscas(T, rng, t, 26, 0.95, 0.03, gravidade=0.35, cauda=0.35)
    G += T.glow(fa, 1, 1.3, 0.02)
    H += fa * 0.8 + T.gauss(0, 0, 0.15) * some(t, 0, 0.3) * 3
    G += T.gauss(0, 0, 0.18) * some(t, 0, 0.3) * 3
    return G, H


def pulso_de_energia(T, t, rng):
    """Pulso: anel brilhante com faíscas elétricas na borda e disco que se dissolve."""
    G, H = vazio(T)
    r = 0.1 + 0.72 * ease_out(t, 2)
    anel = T.ring(r, 0.035 + 0.03 * (1 - t)) * (1 - t) ** 1.2 * 1.8
    disco = T.gauss(0, 0, r * 0.7) * (1 - t) ** 2 * 1.2
    crep = T.zero()
    sub = np.random.default_rng(int(t * 100) + 5)
    for k in range(6):
        a = sub.uniform(0, TAU)
        pts = jagged(sub, math.cos(a) * r, math.sin(a) * r, math.cos(a + 0.5) * r, math.sin(a + 0.5) * r, 3, 0.4)
        crep += T.polyline(pts, 0.008, 1)
    G += anel + disco + T.glow(crep, 1.2, 1.2, 0.01) * (1 - t)
    H += anel * 0.6 + crep * (1 - t) + disco * 0.5
    return G, H


# =================================================================== ELEMENTOS (no alvo)
def _subindo(T, seed, t, escala, vel):
    """Ruído que sobe: a base da chama, da fumaça e da névoa."""
    n = T.noise(np.random.default_rng(seed), escala, 3)
    return np.roll(n, -int(t * vel * T.H), axis=0)


def fogo(T, t, rng):
    """Chamas: línguas subindo da base, brasas, e um clarão quente no impacto.

    A silhueta é deformada por ruído de baixa frequência que sobe com o tempo
    (a chama dança), e o detalhe fino só modula o brilho, sem abrir buracos.
    """
    G, H = vazio(T)
    env = janela(t, 0, 0.12) * apaga(t, 0.55, 1, 1.3)
    n1 = _subindo(T, 51, t, 0.09, 0.8)
    n2 = _subindo(T, 52, t, 0.035, 1.3)
    base = 0.45
    cresce = 0.6 + 0.4 * ease_out(t, 2)
    chama, nucleo = T.zero(), T.zero()
    # cinco línguas de alturas diferentes; a do meio é a maior
    for cx, h, w in ((0.0, 0.85, 0.3), (-0.2, 0.55, 0.2), (0.21, 0.6, 0.2), (-0.36, 0.35, 0.13), (0.37, 0.38, 0.13)):
        altura = h * cresce
        yr = (base - T.V) / altura
        y = np.clip(yr, 0, 1)
        du = T.U - cx + n1 * 0.12 * y
        largura = w * (1 - y) ** 0.85 + 0.01
        topo = np.clip(1 - yr - 0.2 * n1 * y, 0, 1) * (yr < 1.3)
        lingua = np.exp(-(du / largura) ** 2) * smooth(base + 0.05 - T.V, 0, 0.08) * topo ** 0.6
        chama = np.maximum(chama, lingua)
        nucleo = np.maximum(nucleo, np.exp(-(du / (largura * 0.45)) ** 2) * smooth(base + 0.05 - T.V, 0, 0.08) * np.clip(1 - yr * 1.7, 0, 1))
    chama = chama * (0.85 + 0.15 * n2)
    pts = []
    for i in range(28):
        fase = (rng.uniform(0, 1) + t * 1.4) % 1.0
        x = rng.uniform(-0.35, 0.35) + 0.08 * math.sin(fase * 8 + i)
        pts.append((x, base - fase * 0.95, (1 - fase) * rng.uniform(0.4, 1)))
    brasas = T.splats(pts, 0.01)
    flash = T.gauss(0, 0.2, 0.17) * some(t, 0, 0.3) * 1.3
    G += (chama * 2.0 + brasas * 1.2) * env + flash
    H += (nucleo * 1.6 + brasas * 0.8) * env + flash
    return G, H


def gelo(T, t, rng):
    """Cristais crescendo para fora, geada em anel e brilhos nas pontas."""
    G, H = vazio(T)
    cres = ease_out(min(1, t / 0.3), 3)
    env = apaga(t, 0.55, 1, 1.2)
    cristais, arestas, pontas = [], [], []
    sub = np.random.default_rng(61)
    for i in range(11):
        a = TAU * i / 11 + sub.uniform(-0.2, 0.2)
        comp = sub.uniform(0.35, 0.75) * cres
        larg = sub.uniform(0.05, 0.09)
        bx, by = math.cos(a) * 0.08, math.sin(a) * 0.08
        tx, ty = math.cos(a) * comp, math.sin(a) * comp
        nx, ny = -math.sin(a) * larg, math.cos(a) * larg
        mx, my = math.cos(a) * comp * 0.65, math.sin(a) * comp * 0.65
        cristais.append(([(bx, by), (mx + nx, my + ny), (tx, ty), (mx - nx, my - ny)], 0.75))
        cristais.append(([(bx, by), (mx + nx, my + ny), (tx, ty)], 0.45))
        arestas.append((bx, by, tx, ty, 1))
        pontas.append((tx, ty, 1))
    corpo = T.polys(cristais, 0.002) * env
    aresta = T.lines(arestas, 0.008, 0.002) * env
    geada = T.ring(0.2 + 0.55 * ease_out(t, 2), 0.09) * (1 - t) ** 1.5 * 0.6
    brilho = T.zero()
    for k, (x, y, _) in enumerate(pontas[:6]):
        brilho += T.flare(x, y, 0.35, 0.4) * pulso(t, 0.2 + k * 0.06, 0.55 + k * 0.06)
    pts = [(rng.uniform(-0.8, 0.8), rng.uniform(-0.8, 0.8), pulso(t, 0.1, 1) * rng.uniform(0.3, 1)) for _ in range(24)]
    poeira = T.splats(pts, 0.008)
    G += T.glow(corpo, 1, 0.8, 0.03) + aresta * 1.2 + geada + brilho * 1.5 + poeira
    H += aresta * 1.2 + corpo * 0.35 + brilho + poeira * 0.6
    return G, H


def raio(T, t, rng):
    """Descarga: raios saindo do centro, trocando a cada quadro, com clarão."""
    G, H = vazio(T)
    env = apaga(t, 0.5, 1, 1.2)
    sub = np.random.default_rng(int(t * 1000) + 71)
    lin = T.zero()
    for k in range(6):
        a = sub.uniform(0, TAU)
        comp = sub.uniform(0.5, 0.88)
        pts = jagged(sub, 0, 0, math.cos(a) * comp, math.sin(a) * comp, 5, 0.22)
        lin += T.polyline(pts, 0.016, 1)
        i = len(pts) // 2
        g = jagged(sub, *pts[i], pts[i][0] + math.cos(a + 0.7) * 0.25, pts[i][1] + math.sin(a + 0.7) * 0.25, 4, 0.25)
        lin += T.polyline(g, 0.009, 0.8)
    flash = T.gauss(0, 0, 0.2) * (0.6 + 0.4 * sub.uniform()) * env * 2.8
    anel = T.ring(0.15 + 0.6 * ease_out(t, 2), 0.03) * (1 - t) ** 1.5 * 1.2
    G += T.glow(lin, 1.6, 2.2, 0.02) * env + flash + anel
    H += lin * 1.6 * env + flash
    return G, H


def vento(T, t, rng):
    """Redemoinho: arcos de ar girando para dentro, folhas e partículas levadas."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.6, 1, 1.3)
    gira = TAU * 0.9 * ease_out(t, 1.4)
    arcos = T.zero()
    for k in range(6):
        r = 0.22 + 0.1 * k
        a0 = gira * (1.4 - k * 0.15) + k * 1.3
        arcos += T.arc_band(r, 0.035, a0, a0 + 2.0, squash=0.5, rot=-0.1, crescente=True) * (1 - 0.08 * k)
    pts = []
    for i in range(20):
        a = rng.uniform(0, TAU) + gira * 1.6
        r = rng.uniform(0.2, 0.75)
        pts.append((math.cos(a) * r, math.sin(a) * r * 0.5 - 0.2 * t, rng.uniform(0.4, 1)))
    folhas = T.splats(pts, 0.012)
    G += (T.glow(arcos, 1, 1.0, 0.025) + folhas) * env
    H += (arcos * 0.8 + folhas * 0.5) * env
    return G, H


def agua(T, t, rng):
    """Respingo: coroa de gotas em arco balístico, ondulação e névoa."""
    G, H = vazio(T)
    chao = 0.3
    gotas = []
    for i in range(34):
        a = rng.uniform(math.pi * 1.05, math.pi * 1.95)
        v = rng.uniform(0.6, 1.3)
        x = math.cos(a) * v * 0.7 * t
        y = chao + math.sin(a) * v * 1.2 * t + 1.6 * t * t
        if y < chao + 0.05:
            gotas.append((x, y, (1 - t) ** 0.6 * rng.uniform(0.5, 1)))
    g = T.splats(gotas, 0.016)
    coroa = T.zero()
    if t < 0.6:
        h = 0.35 * math.sin(math.pi * t / 0.6)
        w = 0.15 + 0.3 * t
        coroa = T.polys([([(-w, chao), (-w * 1.25, chao - h), (-w * 0.8, chao - h * 0.6), (0, chao - h * 0.15), (w * 0.8, chao - h * 0.6), (w * 1.25, chao - h), (w, chao)], 1)], 0.02)
    ondas = T.zero()
    for k, atraso in enumerate((0, 0.15, 0.3)):
        tt = max(0, t - atraso) / (1 - atraso)
        if tt > 0:
            ondas += T.ring(0.1 + 0.75 * ease_out(tt, 2), 0.025, cy=chao, squash=3.0) * (1 - tt) ** 1.3
    G += T.glow(g, 1.2, 1.0, 0.02) + coroa * 1.1 + ondas * 1.3
    H += g * 0.9 + coroa * 0.4 + ondas * 0.5
    return G, H


def terra(T, t, rng):
    """Pontas de pedra rompendo o chão, lascas e poeira."""
    G, H = vazio(T)
    chao = 0.42
    sobe = ease_out(min(1, t / 0.25), 3) * apaga(t, 0.65, 1, 1.5)
    picos, bordas = [], []
    sub = np.random.default_rng(81)
    for i in range(7):
        x = -0.55 + 1.1 * i / 6 + sub.uniform(-0.05, 0.05)
        h = sub.uniform(0.35, 0.8) * sobe * (1 - abs(x) * 0.5)
        w = sub.uniform(0.08, 0.14)
        inc = sub.uniform(-0.15, 0.15)
        topo = (x + inc * h, chao - h)
        picos.append(([(x - w, chao), topo, (x + w, chao)], 1.0))
        picos.append(([(x - w, chao), topo, (x - w * 0.2, chao)], 0.5))
        bordas.append((x - w, chao, topo[0], topo[1], 1))
    rocha = T.polys(picos, 0.002)
    aresta = T.lines(bordas, 0.008, 0.002) * sobe
    lascas = faiscas(T, rng, t, 18, 0.7, 0.04, cone=(math.pi * 1.1, math.pi * 1.9), gravidade=0.9, cy=chao, cauda=0.2)
    poeira = T.splats([(rng.uniform(-0.8, 0.8), chao - rng.uniform(0, 0.25) * t, (1 - t) * rng.uniform(0.3, 1)) for _ in range(30)], 0.06)
    racha = T.lines([(-0.85 * ease_out(t / 0.2 if t < 0.2 else 1), chao, 0.85 * ease_out(t / 0.2 if t < 0.2 else 1), chao, 1)], 0.012, 0.006) * apaga(t, 0.3, 0.9)
    G += rocha * 1.3 + aresta * 0.8 + lascas * 0.9 + poeira * 0.5 + T.glow(racha, 1.2, 1.4, 0.02)
    H += aresta * 0.6 + racha * 1.2
    return G, H


def veneno(T, t, rng):
    """Nuvem tóxica: massa borbulhante e bolhas que sobem e estouram."""
    G, H = vazio(T)
    env = janela(t, 0, 0.18) * apaga(t, 0.55, 1, 1.3)
    n = _subindo(T, 91, t, 0.07, 0.4)
    r = 0.25 + 0.35 * ease_out(t, 2)
    nuvem = smooth(-(T.RAD / r + n * 0.22), -1.1, -0.45) * (0.7 + 0.3 * n)
    bolhas = T.zero()
    for i in range(14):
        nasce = rng.uniform(0, 0.7)
        vida = rng.uniform(0.2, 0.35)
        x0, y0 = rng.uniform(-0.4, 0.4), rng.uniform(-0.1, 0.35)
        u = (t - nasce) / vida
        if 0 < u < 1:
            raio_b = 0.03 + 0.05 * u
            bolhas += T.ring(raio_b, 0.01, cx=x0, cy=y0 - u * 0.3) * (1 if u < 0.85 else (1 - u) / 0.15)
        elif 1 <= u < 1.3:
            bolhas += T.ring(0.08 + (u - 1) * 0.3, 0.008, cx=x0, cy=y0 - 0.3) * (1.3 - u) / 0.3
    pingos = T.splats([(rng.uniform(-0.5, 0.5), 0.2 + 0.6 * ((rng.uniform() + t) % 1), 0.6) for _ in range(10)], 0.012)
    G += nuvem * 1.3 * env + bolhas * 1.4 + pingos * 0.6 * env
    H += bolhas * 0.9 + np.clip(nuvem - 0.6, 0, None) * env
    return G, H


def sombra(T, t, rng):
    """Tentáculos escuros fechando no alvo e fumaça negra; quase sem núcleo claro."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.55, 1, 1.2)
    tent = T.zero()
    sub = np.random.default_rng(101)
    for i in range(7):
        a = TAU * i / 7 + sub.uniform(-0.3, 0.3)
        alcance = 0.95 - 0.75 * ease_out(min(1, t / 0.45), 2)
        pts = []
        for j in range(16):
            u = j / 15
            r = 0.95 - (0.95 - alcance) * u
            curva = 0.35 * math.sin(u * 3 + i + t * 4) * u
            pts.append((math.cos(a + curva) * r, math.sin(a + curva) * r))
        tent += T.polyline(pts, 0.03 * (1 - 0.6 * ease_out(t)), 1)
    n = _subindo(T, 102, t, 0.06, 0.5)
    fumo = smooth(-(T.RAD / (0.35 + 0.3 * t) + n * 0.25), -1.1, -0.4) * (0.6 + 0.4 * n)
    olho = T.gauss(0, 0, 0.05) * pulso(t, 0.35, 0.8) * 2
    G += (T.glow(tent, 1.0, 1.2, 0.03) + fumo * 1.1) * env + olho
    H += tent * 0.15 * env + olho * 0.8
    return G, H


def luz(T, t, rng):
    """Luz sagrada: pilar descendo do alto, raios, anel no chão e centelhas."""
    G, H = vazio(T)
    chao = 0.38
    desce = ease_out(min(1, t / 0.25), 2.5)
    env = apaga(t, 0.6, 1, 1.4)
    topo = -1.0
    fundo = topo + (chao - topo) * desce
    larg = 0.16 + 0.06 * math.sin(t * 20)
    pilar = np.exp(-(T.U / larg) ** 2) * smooth(T.V, topo, topo + 0.2) * smooth(-T.V, -fundo - 0.02, -fundo + 0.08)
    nucleo = np.exp(-(T.U / (larg * 0.3)) ** 2) * smooth(T.V, topo, topo + 0.2) * smooth(-T.V, -fundo - 0.02, -fundo + 0.08)
    anel = T.ring(0.15 + 0.5 * ease_out(max(0, t - 0.2) / 0.8, 2), 0.03, cy=chao, squash=3.2) * janela(t, 0.2, 0.3) * (1 - t)
    raios = T.zero()
    for k in range(10):
        a = TAU * k / 10 + t
        raios += T.lines([(0, chao - 0.1, math.cos(a) * 0.8, chao - 0.1 + math.sin(a) * 0.5, 1)], 0.03, 0.03)
    pts = [(rng.uniform(-0.4, 0.4), chao - ((rng.uniform() + t) % 1) * 1.2, rng.uniform(0.4, 1)) for _ in range(24)]
    centelhas = T.splats(pts, 0.008) * janela(t, 0.2, 0.35)
    G += (pilar * 1.6 + nucleo * 1.5 + raios * 0.25 * janela(t, 0.2, 0.35) + centelhas) * env + anel * 1.4
    H += (nucleo * 1.8 + pilar * 0.4 + centelhas * 0.8) * env + anel * 0.5
    return G, H


# =================================================================== MAGIA E PSÍQUICO
def _poligono_estrela(n, r, ang):
    return [(math.cos(ang + TAU * k * 2 / n) * r, math.sin(ang + TAU * k * 2 / n) * r) for k in range(n + 1)]


def selo(T, t, rng):
    """Círculo mágico: anéis duplos, runas girando e estrela traçada aos poucos."""
    G, H = vazio(T)
    sq = 0.55
    abre = ease_out(min(1, t / 0.3), 2.5)
    env = apaga(t, 0.7, 1, 1.4)
    rot = t * 1.4
    aneis = (T.ring(0.68 * abre, 0.012, squash=1 / sq) + T.ring(0.58 * abre, 0.008, squash=1 / sq)) * 1.4
    runas = []
    for k in range(24):
        a = TAU * k / 24 + rot
        r1, r2 = 0.6 * abre, 0.66 * abre
        if k % 3:
            runas.append((math.cos(a) * r1, math.sin(a) * r1 * sq, math.cos(a + 0.08) * r2, math.sin(a + 0.08) * r2 * sq, 1))
    marcas = T.lines(runas, 0.01, 0.002)
    estrela = _poligono_estrela(5, 0.56 * abre, -math.pi / 2 - rot * 0.5)
    trac = min(1, max(0.0, (t - 0.12) / 0.4))
    n_seg = int(trac * 5 * 8)
    pts = []
    for k in range(5):
        (ax, ay), (bx, by) = estrela[k], estrela[k + 1]
        for j in range(8):
            if len(pts) <= n_seg:
                u = j / 8
                pts.append((ax + (bx - ax) * u, (ay + (by - ay) * u) * sq))
    linha = T.polyline(pts, 0.01, 1)
    flash = T.gauss(0, 0, 0.3, 0.17) * pulso(t, 0.5, 0.8) * 1.6
    G += (T.glow(aneis + marcas + linha, 1.2, 1.2, 0.015) + flash) * env
    H += (aneis * 0.6 + linha + flash * 0.7) * env
    return G, H


def prisao(T, t, rng):
    """Prisão: barras de luz descem e se fecham num cilindro, com anéis travando."""
    G, H = vazio(T)
    env = apaga(t, 0.7, 1, 1.4)
    barras = T.zero()
    for k in range(9):
        a = TAU * k / 9 + 0.2
        x = math.cos(a) * 0.45
        frente = math.sin(a) > 0
        atraso = k * 0.03
        desce = ease_out(min(1, max(0, t - atraso) / 0.25), 3)
        y1 = -0.75
        y2 = y1 + 1.4 * desce
        barras += T.lines([(x, y1, x, y2, 1.0 if frente else 0.45)], 0.022, 0.003)
    trava = janela(t, 0.3, 0.38)
    aneis = (T.ring(0.45, 0.014, cy=-0.72, squash=1 / 0.25) + T.ring(0.45, 0.014, cy=0.62, squash=1 / 0.25)) * trava * 1.4
    flash = T.gauss(0, 0, 0.5, 0.6) * pulso(t, 0.3, 0.55) * 0.8
    G += (T.glow(barras, 1.3, 1.1, 0.02) + aneis + flash) * env
    H += (barras * 0.9 + aneis * 0.6) * env
    return G, H


def distorcao(T, t, rng):
    """Distorção: anéis ondulados e fatias da imagem deslocadas (falha na realidade)."""
    G, H = vazio(T)
    env = apaga(t, 0.6, 1, 1.3)
    out = T.zero()
    for k in range(4):
        r = 0.15 + 0.17 * k + 0.12 * ease_out(t)
        mod = 1 + 0.12 * np.sin(T.ANG * (3 + k) + t * 8 + k)
        out += np.exp(-((T.RAD - r * mod) / 0.02) ** 2) * (1 - 0.15 * k)
    sub = np.random.default_rng(int(t * 12) + 111)
    fatias = T.zero()
    for _ in range(5):
        y = sub.uniform(-0.6, 0.6)
        h = sub.uniform(0.02, 0.06)
        dx = sub.uniform(-0.2, 0.2)
        fatias += np.exp(-((T.V - y) / h) ** 8) * np.exp(-((T.U - dx) / 0.5) ** 2) * 0.6
    G += (out * 1.3 + fatias) * env + T.gauss(0, 0, 0.12) * pulso(t, 0, 0.4) * 1.6
    H += (out * 0.5 + fatias * 0.5) * env
    return G, H


def portal(T, t, rng):
    """Portal: disco em espiral girando, borda acesa e centro escuro."""
    G, H = vazio(T)
    abre = ease_out(min(1, t / 0.3), 2.5) * apaga(t, 0.7, 1, 1.5)
    sq = 0.7
    r = np.hypot(T.U, T.V / sq)
    ang = np.arctan2(T.V / sq, T.U)
    R0 = 0.6 * abre + 1e-3
    espiral = 0.5 + 0.5 * np.cos(ang * 4 + r / R0 * 9 - t * TAU * 1.5)
    disco = smooth(-r / R0, -1.0, -0.6)
    borda = np.exp(-((r - R0) / 0.03) ** 2)
    G += disco * (0.5 + 0.9 * espiral) + borda * 1.8
    H += borda * 1.1 + disco * espiral * 0.25 * smooth(r / R0, 0.4, 0.9)
    return G, H


def telecinese(T, t, rng):
    """Telecinese: destroços erguidos girando e ondas de força ao redor."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.65, 1, 1.3)
    pedras = []
    sub = np.random.default_rng(121)
    for i in range(12):
        a = TAU * i / 12 + t * 2.2
        r = sub.uniform(0.35, 0.7)
        x, y = math.cos(a) * r, math.sin(a) * r * 0.45 - 0.35 * ease_out(t, 2)
        s = sub.uniform(0.025, 0.05)
        rr = sub.uniform(0, 6) + t * 6
        pedras.append(([(x + s * math.cos(rr + j * 1.9), y + s * math.sin(rr + j * 1.9)) for j in range(4)], 1))
    p = T.polys(pedras, 0.003)
    ondas = T.zero()
    for k in range(3):
        u = (t * 1.5 + k / 3) % 1
        ondas += T.ring(0.2 + 0.6 * u, 0.02, squash=1 / 0.45) * (1 - u) * 0.8
    G += (T.glow(p, 1.4, 1.2, 0.03) + ondas) * env
    H += (p * 0.5 + ondas * 0.3) * env
    return G, H


def maldicao(T, t, rng):
    """Maldição: sigilo triangular invertido girando, névoa espiral e gotas caindo."""
    G, H = vazio(T)
    env = janela(t, 0, 0.15) * apaga(t, 0.6, 1, 1.3)
    rot = t * 2
    tri = [(math.cos(math.pi / 2 + rot + TAU * k / 3) * 0.48, math.sin(math.pi / 2 + rot + TAU * k / 3) * 0.48 * 0.6) for k in range(4)]
    sig = T.polyline(tri, 0.012, 1) + T.ring(0.55, 0.012, squash=1 / 0.6)
    n = _subindo(T, 131, t, 0.05, -0.4)
    espiral = 0.5 + 0.5 * np.sin(T.ANG * 3 - T.RAD * 8 + t * 6)
    nevoa = smooth(-(T.RAD / 0.6 + n * 0.2), -1.0, -0.4) * espiral
    gotas = T.splats([(rng.uniform(-0.5, 0.5), -0.2 + ((rng.uniform() + t * 1.2) % 1) * 0.9, 0.7) for _ in range(14)], 0.012)
    G += (T.glow(sig, 1.4, 1.2, 0.02) * janela(t, 0.05, 0.25) + nevoa * 0.9 + gotas) * env
    H += sig * 0.7 * env
    return G, H


# =================================================================== APOIO
def cura(T, t, rng):
    """Cura: pétalas de luz abrindo, colunas subindo e cruzes de brilho."""
    G, H = vazio(T)
    abre = ease_out(min(1, t / 0.4), 2.5)
    env = apaga(t, 0.6, 1, 1.3)
    petalas = T.zero()
    for k in range(8):
        a = TAU * k / 8 + t * 0.6
        cx, cy = math.cos(a) * 0.3 * abre, math.sin(a) * 0.3 * abre * 0.55 + 0.15
        ca, sa = math.cos(a), math.sin(a)
        du, dv = (T.U - cx), (T.V - cy) / 0.55
        pu, pv = du * ca + dv * sa, -du * sa + dv * ca
        petalas += np.exp(-((pu / 0.17) ** 2 + (pv / 0.06) ** 2))
    pts = []
    for i in range(30):
        fase = (rng.uniform(0, 1) + t * 1.1) % 1.0
        pts.append((rng.uniform(-0.55, 0.55), 0.35 - fase * 1.1, math.sin(math.pi * fase) * rng.uniform(0.5, 1)))
    sobe = T.splats(pts, 0.012)
    cruzes = T.zero()
    for k in range(4):
        x, y = rng.uniform(-0.45, 0.45), rng.uniform(-0.55, 0.1)
        cruzes += T.flare(x, y, 0.3, 0) * pulso(t, 0.15 + 0.1 * k, 0.5 + 0.1 * k)
    G += (petalas * 1.2 * abre + sobe + cruzes * 1.4) * env + T.gauss(0, 0.15, 0.2) * pulso(t, 0, 0.5)
    H += (petalas * 0.4 + sobe * 0.6 + cruzes) * env
    return G, H


def escudo(T, t, rng):
    """Escudo: cúpula de hexágonos subindo da base, borda acesa e brilho no fecho."""
    G, H = vazio(T)
    sobe = ease_out(min(1, t / 0.35), 2.5)
    env = apaga(t, 0.7, 1, 1.4)
    r = 0.7
    dentro = smooth(-T.RAD, -r, -r + 0.05)
    # grade hexagonal
    s = 0.19
    q = (T.U * 2 / 3) / s
    rr = (-T.U / 3 + np.sqrt(3) / 3 * T.V) / s
    cq, cr = np.round(q), np.round(rr)
    dq, dr = q - cq, rr - cr
    d = np.maximum.reduce([np.abs(dq), np.abs(dr), np.abs(dq + dr)])
    grade = smooth(d, 0.4, 0.5)
    nivel = 0.75 - 1.5 * sobe
    revela = smooth(T.V, nivel - 0.05, nivel + 0.05)
    frente = np.exp(-((T.V - nivel) / 0.04) ** 2) * dentro
    bolha = (grade * 0.2 + 0.05 + smooth(T.RAD, r - 0.3, r) * 0.7) * dentro * revela
    borda = np.exp(-((T.RAD - r) / 0.02) ** 2) * revela
    flash = T.gauss(-0.2, -0.25, 0.15) * pulso(t, 0.35, 0.6) * 1.8
    G += (bolha * 1.2 + borda * 1.6 + frente * 1.3 + flash) * env
    H += (borda * 0.8 + frente + grade * dentro * revela * 0.15 + flash) * env
    return G, H


def reforco(T, t, rng):
    """Reforço: aura subindo em chamas claras e divisas (^) que sobem."""
    G, H = vazio(T)
    env = janela(t, 0, 0.12) * apaga(t, 0.6, 1, 1.3)
    n = _subindo(T, 141, t, 0.04, 1.2)
    contorno = np.exp(-((np.hypot(T.U, (T.V - 0.1) * 0.8) - 0.42) / (0.08 + 0.05 * n)) ** 2)
    aura = contorno * smooth(-T.V, -0.55, 0.6) * (0.6 + 0.5 * np.clip(n, -1, 2))
    divisas = []
    for k in range(3):
        u = (t * 1.3 + k / 3) % 1
        y = 0.35 - u * 0.9
        w = 0.16
        divisas.append((-w, y + 0.09, 0, y, math.sin(math.pi * u)))
        divisas.append((0, y, w, y + 0.09, math.sin(math.pi * u)))
    d = T.lines(divisas, 0.03, 0.003)
    G += (aura * 1.4 + T.glow(d, 1.2, 1.2, 0.02)) * env
    H += (np.clip(aura - 0.5, 0, None) + d * 0.9) * env
    return G, H


# =================================================================== ESPECIAL
def execucao(T, t, rng):
    """Execução: um traço de tinta diagonal que corta o alvo, respingos escuros e fio branco."""
    G, H = vazio(T)
    risca = ease_out(min(1, t / 0.18), 3)
    env = apaga(t, 0.55, 1, 1.2)
    a = math.radians(-35)
    x1, y1 = -0.8 * math.cos(a), -0.8 * math.sin(a)
    x2, y2 = x1 + 1.6 * math.cos(a) * risca, y1 + 1.6 * math.sin(a) * risca
    tinta = T.tapered([(x1, y1, x2, y2, 1)], 0.16)
    tinta = T.blur(tinta, 0.004)
    fio = T.lines([(x1, y1, x2, y2, 1)], 0.01, 0.002)
    resp = []
    for i in range(20):
        u = rng.uniform(0.1, 1) * risca
        px, py = x1 + (x2 - x1) * u, y1 + (y2 - y1) * u
        d = rng.normal(0, 0.15) * ease_out(t, 2)
        resp.append((px - d * math.sin(a), py + d * math.cos(a) + 0.2 * t * t, rng.uniform(0.4, 1)))
    gotas = T.splats(resp, 0.02)
    flash = T.gauss(0, 0, 0.25) * pulso(t, 0.15, 0.4) * 1.5
    G += (tinta * 1.8 + gotas * 1.2) * env + T.glow(fio, 2, 1, 0.01) * env + flash
    H += fio * 1.8 * env + flash * 0.6
    return G, H


# =================================================================== LINHA DE AÇÃO (quem vai atacar quem)
PEQUENA = Tela(128)


def cometa(T, t, rng):
    """A luz que corre pela linha de ação: cabeça brilhante, cauda que se desfaz, centelhas soltas (aponta +x)."""
    G, H = vazio(T)
    tremula = 1 + 0.08 * math.sin(TAU * t * 3)
    cabeca = T.gauss(0.42, 0, 0.07 * tremula, 0.05 * tremula) * 2.8
    cauda = T.polys([([(-0.95, 0), (0.36, -0.07), (0.46, 0), (0.36, 0.07)], 1)], blur=0.02)
    cauda *= smooth(T.U, -0.95, 0.3)
    estrela = T.flare(0.42, 0, 0.55, TAU * t / 6, thin=0.012) * 1.1
    pts = []
    for i in range(18):
        fase = (rng.uniform(0, 1) + t) % 1.0
        pts.append((0.35 - 1.2 * fase, rng.normal(0, 0.06) * (0.4 + fase), (1 - fase) ** 1.5 * rng.uniform(0.4, 1)))
    centelhas = T.splats(pts, 0.012)
    G += cabeca + T.glow(cauda, 0.8, 1.2, 0.04) + estrela + centelhas
    H += cabeca * 1.3 + cauda * 0.35 + estrela * 0.8 + centelhas * 0.6
    return G, H


def mira(T, t, rng):
    """Mira no alvo (laço): anel fino girando, quatro colchetes que respiram e marcas de leitura."""
    G, H = vazio(T)
    respira = 0.5 + 0.5 * math.sin(TAU * t)
    anel = T.ring(0.64, 0.012) * (0.6 + 0.4 * respira)
    marcas = []
    for k in range(36):
        a = TAU * k / 36 + TAU * t / 3
        r1, r2 = (0.69, 0.75) if k % 3 == 0 else (0.70, 0.72)
        marcas.append((math.cos(a) * r1, math.sin(a) * r1, math.cos(a) * r2, math.sin(a) * r2, 1 if k % 3 == 0 else 0.5))
    tique = T.lines(marcas, 0.009, 0.002)
    colch = T.zero()
    d = 0.53 - 0.05 * respira
    for k in range(4):
        a0 = TAU * k / 4 + math.pi / 4 - TAU * t / 6
        colch += T.arc_band(d, 0.022, a0 - 0.32, a0 + 0.32, taper=0.0)
    G += T.glow(anel + tique + colch * 1.4, 1.2, 1.0, 0.015)
    H += colch * 0.9 + tique * 0.5 + anel * 0.3
    return G, H


def chegada(T, t, rng):
    """O apoio chegou: anel que abre, luz que sobe do chão e centelhas subindo."""
    G, H = vazio(T)
    anel = T.ring(0.2 + 0.65 * ease_out(t, 2.5), 0.03 + 0.03 * (1 - t)) * (1 - t) ** 1.3 * 1.6
    chao = T.ring(0.25 + 0.5 * ease_out(t, 2), 0.04, cy=0.5, squash=3.2) * (1 - t) ** 1.5
    clarao = T.gauss(0, 0.05, 0.22) * some(t, 0, 0.45) * 1.8
    pts = []
    for i in range(26):
        x = rng.uniform(-0.55, 0.55)
        sobe = ease_out(t, 1.6) * rng.uniform(0.5, 1.1)
        pts.append((x, 0.45 - sobe, (1 - t) ** 1.2 * rng.uniform(0.4, 1)))
    cent = T.splats(pts, 0.01)
    G += anel + chao + clarao + cent * 1.2
    H += anel * 0.5 + clarao + cent * 0.7
    return G, H


# =================================================================== registro
# nome → (função, tela, em laço?, descrição)
FOLHAS: dict = {}


def registra(nome, fn, tela, descricao, laco=False):
    FOLHAS[nome] = (fn, tela, laco, descricao)


def _registro_base():
    registra("soco", soco, GRANDE, "impacto leve")
    registra("golpe_pesado", golpe_pesado, GRANDE, "impacto pesado")
    registra("esmagar", esmagar, GRANDE, "esmagar de cima")
    registra("gancho", gancho, GRANDE, "golpe para cima")
    registra("terremoto", terremoto, GRANDE, "golpe no chão, área")
    registra("onda_de_choque", onda_de_choque, GRANDE, "onda de choque")
    registra("rajada_de_golpes", rajada_de_golpes, GRANDE, "vários golpes")
    registra("corte", corte, GRANDE, "corte em arco")
    registra("corte_cruzado", corte_cruzado, GRANDE, "corte duplo em X")
    registra("estocada", estocada, GRANDE, "perfuração (+x)")
    registra("corte_giratorio", corte_giratorio, GRANDE, "corte giratório")
    registra("corte_de_energia", corte_de_energia, GRANDE, "lâmina de energia (+x)")
    registra("tiro", tiro, MEDIA, "traçante em viagem (+x)", laco=True)
    registra("saraivada", saraivada, MEDIA, "rajada múltipla em viagem (+x)", laco=True)
    registra("missil", missil, MEDIA, "míssil em viagem (+x)", laco=True)
    registra("orbe", orbe, MEDIA, "esfera de energia em viagem (+x)", laco=True)
    registra("crescente", crescente, MEDIA, "onda em meia-lua em viagem (+x)", laco=True)
    registra("bola_de_fogo", bola_de_fogo, MEDIA, "bola de fogo em viagem (+x)", laco=True)
    registra("estilhaco", estilhaco, MEDIA, "lança de gelo em viagem (+x)", laco=True)
    registra("rocha", rocha, MEDIA, "pedra em viagem (+x)", laco=True)
    registra("carga", carga, MEDIA, "preparo: energia convergindo", laco=True)
    registra("feixe", feixe, FAIXA, "feixe fino (faixa)", laco=True)
    registra("feixe_pesado", feixe_pesado, FAIXA, "feixe largo (faixa)", laco=True)
    registra("raio_faixa", raio_faixa, FAIXA, "raio entre dois pontos (faixa)", laco=True)
    registra("dreno", dreno, FAIXA, "transferência de energia (faixa)", laco=True)
    registra("explosao", explosao, GRANDE, "explosão")
    registra("pulso_de_energia", pulso_de_energia, GRANDE, "pulso de energia")
    registra("fogo", fogo, GRANDE, "chamas")
    registra("gelo", gelo, GRANDE, "cristais de gelo")
    registra("raio", raio, GRANDE, "descarga elétrica")
    registra("vento", vento, GRANDE, "redemoinho de vento")
    registra("agua", agua, GRANDE, "respingo de água")
    registra("terra", terra, GRANDE, "pedras rompendo o chão")
    registra("veneno", veneno, GRANDE, "nuvem tóxica")
    registra("sombra", sombra, GRANDE, "tentáculos de sombra")
    registra("luz", luz, GRANDE, "pilar de luz")
    registra("selo", selo, GRANDE, "círculo mágico")
    registra("prisao", prisao, GRANDE, "prisão de barras")
    registra("distorcao", distorcao, GRANDE, "distorção")
    registra("portal", portal, GRANDE, "portal")
    registra("telecinese", telecinese, GRANDE, "telecinese")
    registra("maldicao", maldicao, GRANDE, "maldição")
    registra("cura", cura, GRANDE, "cura")
    registra("escudo", escudo, GRANDE, "cúpula de escudo")
    registra("reforco", reforco, GRANDE, "reforço")
    registra("execucao", execucao, GRANDE, "execução")
    registra("cometa", cometa, PEQUENA, "luz que corre pela linha de ação (+x)", laco=True)
    registra("mira", mira, PEQUENA, "mira no alvo (laço)", laco=True)
    registra("chegada", chegada, PEQUENA, "apoio chegando ao aliado")
    # as famílias novas (tools/vfx/familias_v2)
    from familias_v2 import registra_todas
    registra_todas(registra)


def renderiza(nome):
    fn, T, laco, _ = FOLHAS[nome]
    sheet = Image.new("RGBA", (T.w * COLS, T.h * ROWS), (0, 0, 0, 0))
    for i in range(FRAMES):
        rng = np.random.default_rng(2000 + sum(map(ord, nome)))   # mesma semente em todo quadro: as partículas continuam
        t = i / FRAMES if laco else i / (FRAMES - 1)
        G, H = fn(T, t, rng)
        sheet.paste(T.quadro(G, H), ((i % COLS) * T.w, (i // COLS) * T.h))
    return sheet


def previa(nomes, destino, cor=(0.35, 0.65, 1.0)):
    """Como o jogo mostra: brilho pintado com a cor + núcleo em 'screen', sobre a arena escura."""
    linhas = []
    for nome in nomes:
        sheet = np.asarray(renderiza(nome), np.float32) / 255
        _, T, _, _ = FOLHAS[nome]
        quadros = []
        for i in range(FRAMES):
            q = sheet[(i // COLS) * T.h:(i // COLS + 1) * T.h, (i % COLS) * T.w:(i % COLS + 1) * T.w]
            a, g = q[..., 3:4], q[..., :3]
            fundo = np.ones_like(g) * np.array([0.05, 0.08, 0.1])
            base = fundo * (1 - a) + np.array(cor) * a
            nucleo = g * a * 0.85
            quadros.append(1 - (1 - base) * (1 - nucleo))
        if T.h != T.w:
            linhas.append(np.concatenate(quadros[::3], axis=0))
        else:
            linhas.append(np.concatenate(quadros[1::2] if len(nomes) > 1 else quadros, axis=1))
    largura = max(l.shape[1] for l in linhas)
    linhas = [np.pad(l, ((0, 4), (0, largura - l.shape[1]), (0, 0)), constant_values=0.02) for l in linhas]
    Image.fromarray((np.clip(np.concatenate(linhas, axis=0), 0, 1) * 255).astype(np.uint8)).save(destino)


def gif(nomes, destino, cor=(0.35, 0.65, 1.0), lado=192, ms=90, voltas=2):
    """GIF animado (para mostrar ao jogador): as folhas lado a lado, como o jogo pinta."""
    filmes = []
    for item in nomes:
        # "nome:#rrggbb" pinta com a cor que o jogo usa para a família
        nome, _, hexa = item.partition(":")
        cor_dela = tuple(int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5)) if hexa else cor
        sheet = np.asarray(renderiza(nome), np.float32) / 255
        _, T, _, _ = FOLHAS[nome]
        quadros = []
        for i in range(FRAMES):
            q = sheet[(i // COLS) * T.h:(i // COLS + 1) * T.h, (i % COLS) * T.w:(i % COLS + 1) * T.w]
            a, g = q[..., 3:4], q[..., :3]
            fundo = np.ones_like(g) * np.array([0.05, 0.08, 0.1])
            base = fundo * (1 - a) + np.array(cor_dela) * a
            im = Image.fromarray((np.clip(1 - (1 - base) * (1 - g * a * 0.85), 0, 1) * 255).astype(np.uint8))
            larg = lado * 2 if T.w != T.h else lado
            quadros.append(im.resize((larg, round(larg * T.h / T.w)), Image.LANCZOS))
        filmes.append(quadros)
    larg = sum(f[0].width for f in filmes) + 6 * (len(filmes) - 1)
    alto = max(f[0].height for f in filmes)
    saida = []
    for _ in range(voltas):
        for i in range(FRAMES):
            tela = Image.new("RGB", (larg, alto), (5, 5, 8))
            x = 0
            for f in filmes:
                tela.paste(f[i], (x, (alto - f[i].height) // 2))
                x += f[i].width + 6
            saida.append(tela)
        saida += [saida[-1]] * 3
    saida[0].save(destino, save_all=True, append_images=saida[1:], duration=ms, loop=0, optimize=True)


def main(argv):
    _registro_base()
    if argv and argv[0] == "--gif":
        gif(argv[2:], argv[1])
        return
    if argv and argv[0] == "--previa":
        previa(argv[2:] or list(FOLHAS), argv[1])
        return
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "manifest.json"
    manifesto = json.loads(manifest_path.read_text()) if manifest_path.exists() and argv else {}
    for nome in argv or FOLHAS:
        fn, T, laco, descricao = FOLHAS[nome]
        destino = OUT / f"{nome}.webp"
        renderiza(nome).save(destino, "WEBP", quality=84, method=6)
        manifesto[nome] = {"descricao": descricao, "quadros": FRAMES, "grade": [COLS, ROWS], "tamanho": [T.w, T.h], "laco": laco, "bytes": destino.stat().st_size}
        print(f"{nome:18s} {destino.stat().st_size / 1024:6.1f} KB  {descricao}")
    manifest_path.write_text(json.dumps(dict(sorted(manifesto.items())), indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
