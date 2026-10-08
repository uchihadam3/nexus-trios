#!/usr/bin/env python3
"""
Efeitos de atuação (adendo, parte 2): o que acontece em quem age e em quem recebe.

Cada efeito é uma folha de 12 quadros (3 colunas × 4 linhas), desenhada como
luz que se soma — partículas como pontos de brilho espalhados por filtro
gaussiano, rastros riscados e desfocados, névoa feita de ruído suavizado e
torcido a cada quadro — e só no fim convertida em cor e transparência. Assim o
efeito brilha sobre a arena escura sem lavar a tela de branco.

Dois tipos:
- reações, com cor que já significa algo (golpe quente, cura verde, escudo
  azul, maldição roxa, preparo dourado);
- efeitos de quem age, desenhados em branco: no jogo eles ganham a cor do
  personagem (máscara tingida + núcleo claro por cima).

Determinístico: a mesma semente gera os mesmos quadros.

Uso: python3 tools/vfx/generate_acting.py   (gera public/assets/vfx/acting/*.webp)
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, map_coordinates

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public/assets/vfx/acting"
N = 160            # quadro final, px
SS = 2             # supersample
R = N * SS         # resolução de trabalho
COLS, ROWS, FRAMES = 3, 4, 12

Y, X = np.mgrid[0:R, 0:R]
U = (X + 0.5) / R * 2 - 1          # -1..1, esquerda→direita
V = (Y + 0.5) / R * 2 - 1          # -1..1, cima→baixo
RAD = np.hypot(U, V)
ANG = np.arctan2(V, U)


# ---------------------------------------------------------------- utilidades
def ease_out(t: float, p: float = 3) -> float:
    return 1 - (1 - t) ** p


def smooth(x: np.ndarray, a: float, b: float) -> np.ndarray:
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def gauss(cx: float, cy: float, sigma: float, rad=None) -> np.ndarray:
    d2 = (U - cx) ** 2 + (V - cy) ** 2
    return np.exp(-d2 / (2 * sigma * sigma))


def ring(radius: float, width: float, squash: float = 1.0, cy: float = 0.0) -> np.ndarray:
    r = np.hypot(U, (V - cy) * squash)
    return np.exp(-((r - radius) / max(width, 1e-4)) ** 2)


def splats(points, sigma: float) -> np.ndarray:
    """Pontos (x, y, intensidade) em -1..1 viram brilhos gaussianos de raio sigma."""
    img = np.zeros((R, R), np.float32)
    for x, y, w in points:
        ix, iy = int((x + 1) / 2 * R), int((y + 1) / 2 * R)
        if 0 <= ix < R and 0 <= iy < R:
            img[iy, ix] += w
    s = sigma * R / 2
    return gaussian_filter(img, s) * (2 * math.pi * s * s)


def strokes(lines, width: float, blur: float) -> np.ndarray:
    """Riscos (x1, y1, x2, y2, intensidade) desenhados e desfocados."""
    im = Image.new("F", (R, R), 0.0)
    d = ImageDraw.Draw(im)
    for x1, y1, x2, y2, w in lines:
        p = lambda x, y: ((x + 1) / 2 * R, (y + 1) / 2 * R)
        d.line([p(x1, y1), p(x2, y2)], fill=float(w), width=max(1, int(width * R / 2)))
    a = np.asarray(im, np.float32)
    return gaussian_filter(a, blur * R / 2) if blur > 0 else a


def polys(shapes) -> np.ndarray:
    im = Image.new("F", (R, R), 0.0)
    d = ImageDraw.Draw(im)
    for pts, w in shapes:
        d.polygon([((x + 1) / 2 * R, (y + 1) / 2 * R) for x, y in pts], fill=float(w))
    return np.asarray(im, np.float32)


def tint(layer: np.ndarray, color) -> np.ndarray:
    return layer[..., None] * np.asarray(color, np.float32)[None, None, :]


BORDA = smooth(-np.maximum(np.abs(U), np.abs(V)), -0.99, -0.82)


def tapered(lines, width: float) -> np.ndarray:
    """Rastros que afinam: grossos na cabeça (x2, y2), finos na cauda."""
    im = Image.new("F", (R, R), 0.0)
    d = ImageDraw.Draw(im)
    for x1, y1, x2, y2, w in lines:
        ang = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
        hw = width / 2
        ox, oy = math.cos(ang) * hw, math.sin(ang) * hw
        pts = [(x1, y1), (x2 + ox, y2 + oy), (x2 + ox * 0.4 + (x2 - x1) * 0.04, y2 + oy * 0.4 + (y2 - y1) * 0.04), (x2 - ox, y2 - oy)]
        d.polygon([((x + 1) / 2 * R, (y + 1) / 2 * R) for x, y in pts], fill=float(w))
    return np.asarray(im, np.float32)


def glow(layer: np.ndarray, core: float, halo: float, halo_sigma: float) -> np.ndarray:
    """Núcleo nítido mais halo largo: o que faz um risco parecer luz."""
    return layer * core + gaussian_filter(layer, halo_sigma * R / 2) * halo


def flare(cx: float, cy: float, size: float, ang: float = 0.0) -> np.ndarray:
    """Estrela de clarão de quatro pontas."""
    out = np.zeros((R, R), np.float32)
    for a in (ang, ang + math.pi / 2):
        pu = (U - cx) * math.cos(a) + (V - cy) * math.sin(a)
        pv = -(U - cx) * math.sin(a) + (V - cy) * math.cos(a)
        out += np.exp(-np.abs(pv) / (0.008 * size)) * np.exp(-np.abs(pu) / (0.35 * size))
    return out


def to_rgba(E: np.ndarray) -> Image.Image:
    """Luz somada → cor e alfa. O núcleo satura para claro; as bordas guardam a cor."""
    E = np.maximum(E, 0) * BORDA[..., None]
    T = 1 - np.exp(-E * 1.35)
    a = T.max(axis=2)
    rgb = np.where(a[..., None] > 1e-4, T / np.maximum(a[..., None], 1e-4), 0)
    rgb = np.clip(rgb, 0, 1) ** (1 / 1.08)
    a = np.clip(a, 0, 1)
    pre = np.dstack([rgb * a[..., None], a])            # pré-multiplicado para reduzir sem franja
    im = Image.fromarray((pre * 255 + 0.5).astype(np.uint8), "RGBA").resize((N, N), Image.LANCZOS)
    arr = np.asarray(im, np.float32) / 255
    al = arr[..., 3:4]
    out = np.dstack([np.where(al > 1e-3, arr[..., :3] / np.maximum(al, 1e-3), 0), al])
    return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")


def fade(t: float, a: float = 0.0, b: float = 1.0) -> float:
    """Envelope: entra rápido, some suave até o fim."""
    if t < a:
        return 0.0
    return float(max(0.0, 1 - ((t - a) / (b - a)) ** 1.6))


# ---------------------------------------------------------------- reações
WARM, WHITE = (1.0, 0.72, 0.42), (1.0, 1.0, 1.0)


def hit_spark(t, rng, heavy=False):
    k = 1.45 if heavy else 1.0
    E = np.zeros((R, R, 3), np.float32)
    E += tint(gauss(0, 0, 0.10 * k + 0.05 * t) * 3.2 * (1 - t) ** 3, WHITE)
    E += tint(ring(0.12 + 0.62 * k * ease_out(t), 0.035 * (1 - t) + 0.008) * 1.6 * (1 - t) ** 1.4, WARM)
    if heavy:
        E += tint(ring(0.08 + 0.85 * ease_out(min(1, t * 1.25), 2), 0.05 * (1 - t) + 0.01) * 1.0 * (1 - t) ** 1.2, (1.0, 0.55, 0.3))
    n = 34 if heavy else 22
    lines = []
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        sp = rng.uniform(0.55, 1.05) * k
        d = sp * ease_out(t, 2.2) * 0.82
        tail = max(0.05, 0.28 * (1 - t))
        lines.append((math.cos(a) * max(0, d - tail), math.sin(a) * max(0, d - tail), math.cos(a) * d, math.sin(a) * d, (1 - t) ** 1.3 * rng.uniform(0.7, 1.3)))
    E += tint(glow(tapered(lines, 0.034 * k), 1.2, 1.4, 0.025), (1.0, 0.8, 0.5))
    E += tint(flare(0, 0, 1.4 * k, 0.4) * 2.2 * (1 - t) ** 4, WHITE)
    if heavy:
        chunks = []
        for i in range(10):
            a = rng.uniform(math.pi * 0.9, math.pi * 2.1)
            d = rng.uniform(0.3, 0.75) * ease_out(t, 2)
            cx, cy = math.cos(a) * d, math.sin(a) * d + 0.45 * t * t
            s = rng.uniform(0.025, 0.05) * (1 - 0.5 * t)
            rot = rng.uniform(0, 6.28) + t * 6
            chunks.append(([(cx + s * math.cos(rot + j * 2.1), cy + s * math.sin(rot + j * 2.1)) for j in range(3)], (1 - t) ** 1.1))
        E += tint(gaussian_filter(polys(chunks), 1.0), (1.0, 0.5, 0.25)) * 1.4
    return E


def heal_rise(t, rng):
    E = np.zeros((R, R, 3), np.float32)
    env = math.sin(math.pi * min(1, t * 1.05)) ** 0.8
    G, G2 = (0.42, 1.0, 0.62), (0.75, 1.0, 0.85)
    E += tint(ring(0.35 + 0.35 * ease_out(t), 0.03, squash=3.2, cy=0.55) * 1.3 * (1 - t), G)
    pts = []
    for i in range(30):
        x = rng.uniform(-0.62, 0.62)
        ph = rng.uniform(0, 1)
        life = (t * 1.2 + ph) % 1.0
        y = 0.62 - life * 1.35
        pts.append((x + 0.05 * math.sin(life * 9 + i), y, math.sin(math.pi * life) * env * rng.uniform(0.6, 1.2)))
    E += tint(splats(pts, 0.022), G) * 0.9
    E += tint(splats(pts, 0.008), G2) * 0.9
    lines = []
    for i in range(4):
        cx, cy, start = rng.uniform(-0.45, 0.45), rng.uniform(-0.55, 0.25), rng.uniform(0, 0.5)
        w = math.sin(math.pi * np.clip((t - start) / 0.4, 0, 1)) * 1.3
        s = 0.07
        lines += [(cx - s, cy, cx + s, cy, w), (cx, cy - s, cx, cy + s, w)]
    E += tint(strokes(lines, 0.016, 0.004), G2) * 1.4
    for x in (-0.32, 0.05, 0.36):
        col = np.exp(-((U - x) / 0.05) ** 2) * smooth(-V, -0.65, 0.5) * (1 - smooth(-V, 0.5, 0.95))
        E += tint(col * 0.45 * env, G)
    E += tint(gauss(0, 0.3, 0.22) * 0.18 * env, G)
    return E


def _brasao(cx, cy, larg, alt, pontos=28):
    """Contorno de um escudo heráldico: topo reto com cantos, laterais que descem
    e se fecham numa ponta embaixo (o desenho que todo mundo lê como "escudo")."""
    pts = [(cx - larg, cy - alt * 0.62), (cx - larg * 0.55, cy - alt * 0.7), (cx, cy - alt * 0.6),
           (cx + larg * 0.55, cy - alt * 0.7), (cx + larg, cy - alt * 0.62)]
    for k in range(pontos + 1):
        u = k / pontos
        x = larg * (1 - u ** 2.2)
        y = -alt * 0.62 + (alt * 1.62) * u
        pts.append((cx + x * (1 - 0.15 * u), cy + y))
    for k in range(pontos, -1, -1):
        u = k / pontos
        x = larg * (1 - u ** 2.2)
        y = -alt * 0.62 + (alt * 1.62) * u
        pts.append((cx - x * (1 - 0.15 * u), cy + y))
    return pts


def _escudo_desenhado(cx, cy, esc, brilho=1.0):
    """O escudo inteiro em luz: placa translúcida, borda grossa, friso interno, a cruz e o umbo no meio."""
    fora = polys([(_brasao(cx, cy, 0.46 * esc, 0.5 * esc), 1.0)])
    dentro = polys([(_brasao(cx, cy + 0.02 * esc, 0.37 * esc, 0.41 * esc), 1.0)])
    friso = polys([(_brasao(cx, cy + 0.03 * esc, 0.33 * esc, 0.37 * esc), 1.0)])
    fora, dentro, friso = (gaussian_filter(a, 1.2) for a in (fora, dentro, friso))
    borda = fora - dentro
    linha = dentro - friso
    cruz = strokes([(cx, cy - 0.3 * esc, cx, cy + 0.42 * esc, 1), (cx - 0.3 * esc, cy - 0.06 * esc, cx + 0.3 * esc, cy - 0.06 * esc, 1)],
                   0.045 * esc, 0.006) * friso
    umbo = gauss(cx, cy - 0.06 * esc, 0.07 * esc)
    reflexo = np.exp(-(((U - cx) + (V - cy) * 0.6 + 0.12 * esc) / (0.05 * esc)) ** 2) * friso * 0.5
    return (friso * 0.28 + borda * 1.5 + linha * 0.8 + cruz * 0.7 + umbo * 1.2 + reflexo) * brilho


def _favo(escala=7.0, curva=0.8):
    """Favo de mel (a barreira de energia dos jogos), curvado como cúpula: as células
    encolhem perto da borda para parecer uma esfera vista de frente."""
    r = np.clip(RAD / curva, 0, 0.999)
    z = np.sqrt(1 - r ** 2)
    k = np.arcsin(r) / np.maximum(r, 1e-4)
    px, py = U * k * escala / curva, V * k * escala / curva
    sx, sy = 1.0, math.sqrt(3)
    ax, ay = np.mod(px, sx) - sx / 2, np.mod(py, sy) - sy / 2
    bx, by = np.mod(px - sx / 2, sx) - sx / 2, np.mod(py - sy / 2, sy) - sy / 2
    usa_a = ax * ax + ay * ay < bx * bx + by * by
    gx, gy = np.where(usa_a, ax, bx), np.where(usa_a, ay, by)
    d = np.maximum(np.abs(gx) * 0.5 + np.abs(gy) * (math.sqrt(3) / 2), np.abs(gx))
    aresta = np.exp(-((0.5 - d) / 0.045) ** 2)
    # cada célula tem um id para cintilar em tempos diferentes
    cid = np.floor(px - gx + 0.5) * 7.13 + np.floor(py - gy + 0.5) * 3.71
    return aresta, z, cid


def shield_bubble(t, rng):
    """Recebe escudo: o brasão aparece na frente, abre e vira uma cúpula de favo que
    fecha de baixo para cima em volta do personagem, segura cintilando e some."""
    B, B2 = (0.42, 0.76, 1.0), (0.86, 0.96, 1.0)
    E = np.zeros((R, R, 3), np.float32)
    # 1) o brasão: pula para a frente e depois se abre (fica maior e transparente)
    surge = ease_out(min(1, t / 0.18), 2.5)
    abre = smooth(np.array(t), 0.22, 0.45)
    esc = 0.75 + 0.25 * surge + 0.9 * float(abre)
    brasao = _escudo_desenhado(0, 0.05, esc, (1 - float(abre)) * surge)
    E += tint(brasao, B) + tint(brasao * 0.45, B2)
    # 2) a cúpula de favo fechando de baixo para cima
    Rb = 0.82
    dentro = smooth(Rb - RAD, -0.01, 0.02)
    aresta, z, cid = _favo(6.5, Rb)
    sobe = ease_out(float(np.clip((t - 0.22) / 0.3, 0, 1)), 2)
    frente = 0.95 - 1.95 * sobe
    revela = smooth(V, frente - 0.05, frente + 0.05)
    linha_frente = np.exp(-((V - frente) / 0.03) ** 2) * dentro * (0 < sobe < 1)
    sai = 1 - float(smooth(np.array(t), 0.72, 1.0))
    cint = 0.55 + 0.45 * np.sin(cid + t * 18)
    favo = aresta * dentro * (0.25 + 0.9 * (1 - z) ** 1.5) * cint
    borda = np.exp(-((RAD - Rb) / 0.03) ** 2) * 1.5 + dentro * (1 - z) ** 4 * 0.8
    brilho_passa = np.exp(-((U + V * 0.4 - (-1.4 + 2.8 * float(np.clip((t - 0.45) / 0.35, 0, 1)))) / 0.12) ** 2) * aresta * dentro
    cupula = (favo + borda + brilho_passa * 1.2) * revela * sai + linha_frente * 1.4 * sai
    E += tint(cupula, B) + tint(np.exp(-((RAD - Rb) / 0.012) ** 2) * revela * sai * 0.9 + brilho_passa * revela * sai * 0.5, B2)
    E += tint(gauss(-0.3, -0.5, 0.1) * 0.5 * sai * sobe, B2)                      # reflexo da cúpula
    return E


def block_shield(t, rng):
    """Bloqueio: o escudo levanta na frente num tranco, o golpe bate na face dele
    (clarão, faíscas raspando para os lados), o escudo treme e baixa."""
    B, B2, Q = (0.45, 0.78, 1.0), (0.9, 0.97, 1.0), (1.0, 0.85, 0.55)
    E = np.zeros((R, R, 3), np.float32)
    sobe = ease_out(min(1, t / 0.12), 3)
    bate = 0.14
    treme = 0.03 * math.sin(t * 90) * math.exp(-max(0.0, t - bate) * 9) * (t > bate)
    recua = 0.05 * math.exp(-max(0.0, t - bate) * 7) * (t > bate)
    sai = 1 - float(smooth(np.array(t), 0.6, 0.9))
    cx, cy = treme + recua * 0.3, 0.08 + (1 - sobe) * 0.35
    esc = 1.05 + 0.08 * (t > bate) * math.exp(-max(0.0, t - bate) * 8)
    E += tint(_escudo_desenhado(cx, cy, esc, sobe * sai * 1.2), B) + tint(_escudo_desenhado(cx, cy, esc, sobe * sai * 0.4), B2)
    if t >= bate:
        tt = (t - bate) / (1 - bate)
        flash = gauss(cx - 0.05, cy - 0.08, 0.1) * math.exp(-tt * 8) * 3.0
        onda = ring(0.08 + 0.5 * ease_out(tt, 2), 0.03, cy=cy - 0.08) * (1 - tt) ** 2 * 1.4
        E += tint(flash + onda, B2) + tint(flash * 0.5, Q)
        sub = np.random.default_rng(77)
        linhas = []
        for _ in range(26):
            lado = sub.choice((-1, 1))
            a = (math.pi if lado < 0 else 0) + sub.uniform(-0.75, 0.55) * lado
            v0 = sub.uniform(0.6, 1.4)
            d = v0 * ease_out(min(1, tt * 2.2), 2)
            x = cx - 0.05 + math.cos(a) * d * 0.7
            y = cy - 0.08 + math.sin(a) * d * 0.55 + 0.4 * tt * tt
            cauda = 0.05 + 0.12 * (1 - tt)
            w = max(0.0, 1 - tt * 1.6)
            linhas.append((x - math.cos(a) * cauda, y - math.sin(a) * cauda, x, y, w))
        fa = tapered(linhas, 0.022)
        E += tint(glow(fa, 1.2, 0.8, 0.012), Q) + tint(fa * 0.6, B2)
    return E


def buff_rise(t, rng):
    Gd, Gd2 = (1.0, 0.82, 0.38), (1.0, 0.95, 0.75)
    E = np.zeros((R, R, 3), np.float32)
    env = math.sin(math.pi * min(1, t * 1.02)) ** 0.7
    lines = []
    for col, x in enumerate((-0.42, 0.0, 0.42)):
        for k in range(2):
            life = (t * 1.1 + col * 0.18 + k * 0.5) % 1.0
            y = 0.55 - life * 1.25
            w = math.sin(math.pi * life) * env
            s = 0.13
            lines += [(x - s, y + s * 0.8, x, y, w), (x, y, x + s, y + s * 0.8, w)]
    E += tint(strokes(lines, 0.03, 0.01), Gd) * 1.5 + tint(strokes(lines, 0.012, 0.0), Gd2) * 0.8
    coluna = np.exp(-(U / (0.16 + 0.22 * smooth(V, -0.6, 0.6))) ** 2) * smooth(-V, -0.7, 0.2) * np.exp(-np.clip(-V, 0, 9) / 0.35)
    E += tint(coluna * 0.55 * env, Gd)
    return E


NOISE = None


def curse_mist(t, rng):
    global NOISE
    if NOISE is None:
        g = np.random.default_rng(77).normal(size=(R, R)).astype(np.float32)
        NOISE = gaussian_filter(g, 9) * 9
    P, P2 = (0.62, 0.32, 1.0), (0.9, 0.55, 1.0)
    rot = t * 1.4
    ca, sa = math.cos(rot), math.sin(rot)
    twist = 1.8 * RAD
    uu = U * np.cos(twist + rot) - V * np.sin(twist + rot)
    vv = U * np.sin(twist + rot) + V * np.cos(twist + rot)
    coords = np.stack([(vv + 1) / 2 * (R - 1), (uu + 1) / 2 * (R - 1)])
    f = map_coordinates(NOISE, coords, order=1, mode="wrap")
    env = math.sin(math.pi * min(1, t * 1.03)) ** 0.6
    dens = smooth(f, -0.1, 0.9) * smooth(-RAD, -0.85, -0.25) * env
    E = tint(dens * 1.3, P) + tint(dens ** 3 * 1.2, P2)
    marks = []
    for i in range(10):
        a = i / 10 * 2 * math.pi - rot * 0.8
        x, y = math.cos(a) * 0.72, math.sin(a) * 0.72
        s = 0.045
        marks += [(x - s, y, x + s, y, env), (x, y - s * 1.3, x, y + s * 1.3, env * 0.8)]
    E += tint(strokes(marks, 0.014, 0.004), P2) * 0.9
    E += tint(ring(0.72, 0.02) * 0.5 * env, P)
    return E


def prep_shatter(t, rng):
    Gd, W = (1.0, 0.82, 0.4), (1.0, 0.95, 0.8)
    E = tint(gauss(0, 0, 0.18) * 1.8 * max(0, 1 - t / 0.2), W)
    shards = []
    for i in range(16):
        a0 = i / 16 * 2 * math.pi + rng.uniform(-0.08, 0.08)
        d = 0.55 + 0.3 * ease_out(t, 2.5) * rng.uniform(0.7, 1.2)
        spin = rng.uniform(-4, 4) * t
        half = 0.17
        p1 = (math.cos(a0 - half + spin * 0.1) * d, math.sin(a0 - half + spin * 0.1) * d + 0.3 * t * t)
        p2 = (math.cos(a0 + half + spin * 0.1) * d, math.sin(a0 + half + spin * 0.1) * d + 0.3 * t * t)
        pm = (math.cos(a0) * (d + 0.05), math.sin(a0) * (d + 0.05) + 0.3 * t * t)
        shards.append(([p1, pm, p2, (pm[0] * 0.93, pm[1] * 0.93)], (1 - t) ** 1.2))
    sh = polys(shards)
    E += tint(glow(sh, 0.7, 1.6, 0.03), Gd) + tint(sh * 0.5, W)
    return E


def ko_dust(t, rng):
    D = (0.78, 0.8, 0.86)
    pts = []
    for i in range(46):
        a = rng.uniform(0, 2 * math.pi)
        sp = rng.uniform(0.3, 0.95)
        d = sp * ease_out(t, 2.4)
        x = math.cos(a) * d
        y = 0.45 + math.sin(a) * d * 0.32 - 0.25 * t * rng.uniform(0.2, 1)
        pts.append((x, y, (1 - t) ** 1.4 * rng.uniform(0.4, 1)))
    E = tint(splats(pts, 0.06), D) * 0.55
    E += tint(ring(0.2 + 0.7 * ease_out(t), 0.04, squash=3.0, cy=0.45) * 0.5 * (1 - t), D)
    return E


# ---------------------------------------------------------------- quem age (branco, tingido no jogo)
def dash_trail(t, rng):
    """Rastro do avanço, apontando para +x: as linhas ficam atrás (à esquerda)."""
    env = math.sin(math.pi * min(1, t * 1.05))
    lines = []
    for i in range(9):
        y = rng.uniform(-0.42, 0.42)
        L = rng.uniform(0.4, 0.85)
        x2 = rng.uniform(-0.2, 0.05) - t * 0.3
        lines.append((x2 - L, y, x2, y, env * (1 - abs(y) * 1.2) * rng.uniform(0.6, 1.1)))
    E = tint(glow(tapered(lines, 0.045), 0.9, 1.2, 0.03), WHITE)
    vulto = np.exp(-((V) / 0.36) ** 2) * np.exp(-((U + 0.15) / 0.55) ** 2) * smooth(U, -0.95, -0.3)
    E += tint(vulto * 0.5 * env, WHITE)
    return E


def muzzle_flash(t, rng):
    """Clarão do disparo, apontando para +x a partir do centro-esquerda."""
    x0 = -0.35
    env = (1 - t) ** 2.2
    cone = np.exp(-((V) / (0.06 + 0.25 * np.clip(U - x0, 0, 2))) ** 2) * smooth(U, x0 - 0.05, x0 + 0.1) * np.exp(-(np.clip(U - x0, 0, 9) / 0.62) ** 2)
    E = tint(cone * 2.2 * env, WHITE)
    E += tint(gauss(x0 + 0.05, 0, 0.12 + 0.1 * t) * 2.4 * env, WHITE)
    lines = []
    for i in range(9):
        a = rng.uniform(-0.55, 0.55)
        L = rng.uniform(0.3, 0.8) * (0.6 + 0.6 * t)
        lines.append((x0, 0, x0 + math.cos(a) * L, math.sin(a) * L, env * rng.uniform(0.6, 1.2)))
    E += tint(strokes(lines, 0.014, 0.005), WHITE) * 1.3
    return E


def cast_aura(t, rng):
    """Aura de preparo em laço: línguas de luz sobem em volta do medalhão."""
    global NOISE
    if NOISE is None:
        curse_mist(0, rng)
    ph = 2 * math.pi * t
    shift = (t * R * 0.5) % R
    coords = np.stack([((V + 1) / 2 * (R - 1) + shift) % (R - 1), (U + 1) / 2 * (R - 1)])
    f = map_coordinates(NOISE, coords, order=1, mode="wrap")
    band = np.exp(-((RAD - 0.7) / 0.13) ** 2)
    up = smooth(-V, -1.0, 0.6)
    flames = smooth(f + up * 0.6, 0.35, 1.2) * band
    E = tint(flames * 1.5 + ring(0.7, 0.025) * (0.8 + 0.2 * math.sin(ph)), WHITE)
    pts = [(math.cos(i * 0.9 + ph) * 0.72, math.sin(i * 0.9 + ph) * 0.72 - 0.15 * ((t + i * 0.13) % 1), 0.8) for i in range(7)]
    E += tint(splats(pts, 0.02), WHITE) * 0.8
    return E


def area_slam(t, rng):
    """Onda de choque no chão, em perspectiva."""
    env = (1 - t) ** 1.3
    E = tint(ring(0.1 + 0.85 * ease_out(t, 2.5), 0.045 * (1 - t) + 0.01, squash=2.8, cy=0.4) * 1.8 * env, WHITE)
    E += tint(ring(0.05 + 0.6 * ease_out(min(1, t * 1.3), 2.5), 0.03, squash=2.8, cy=0.4) * 1.0 * env, WHITE)
    E += tint(gauss(0, 0.4, 0.14) * 2.2 * (1 - t) ** 3, WHITE)
    lines = []
    for i in range(16):
        a = rng.uniform(0, 2 * math.pi)
        d = ease_out(t, 2) * rng.uniform(0.4, 0.9)
        x, y = math.cos(a) * d, 0.4 + math.sin(a) * d / 2.8
        lines.append((x, y, x, y - rng.uniform(0.08, 0.28) * (1 - t), env))
    E += tint(strokes(lines, 0.018, 0.006), WHITE) * 1.2
    return E


def support_pulse(t, rng):
    E = np.zeros((R, R, 3), np.float32)
    for k in range(3):
        tt = (t * 1.2 - k * 0.22)
        if 0 < tt < 1:
            E += tint(ring(0.15 + 0.75 * ease_out(tt, 2), 0.04, ) * (1 - tt) ** 1.3 * 1.3, WHITE)
    pts = [(rng.uniform(-0.7, 0.7), rng.uniform(-0.7, 0.7), math.sin(math.pi * np.clip(t * 1.6 - rng.uniform(0, 0.6), 0, 1))) for _ in range(14)]
    E += tint(splats(pts, 0.012), WHITE) * 1.1
    E += tint(gauss(0, 0, 0.14) * 0.45 * math.sin(math.pi * t), WHITE)
    return E


EFEITOS = {
    # reações
    "hit_spark": (lambda t, r: hit_spark(t, r), "reação: golpe"),
    "hit_heavy": (lambda t, r: hit_spark(t, r, heavy=True), "reação: golpe pesado"),
    "heal_rise": (heal_rise, "reação: cura"),
    "shield_bubble": (shield_bubble, "reação: recebe escudo (brasão e cúpula de favo)"),
    "block_shield": (block_shield, "reação: bloqueio no escudo"),
    "buff_rise": (buff_rise, "reação: buff"),
    "curse_mist": (curse_mist, "reação: debuff"),
    "prep_shatter": (prep_shatter, "reação: preparo interrompido"),
    "ko_dust": (ko_dust, "reação: nocaute"),
    # quem age (máscaras brancas)
    "dash_trail": (dash_trail, "age: rastro do avanço (+x)"),
    "muzzle_flash": (muzzle_flash, "age: clarão do disparo (+x)"),
    "cast_aura": (cast_aura, "age: aura do preparo (laço)"),
    "area_slam": (area_slam, "age: onda de choque no chão"),
    "support_pulse": (support_pulse, "age: pulso de apoio"),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifesto = {}
    for nome, (fn, descricao) in EFEITOS.items():
        sheet = Image.new("RGBA", (N * COLS, N * ROWS), (0, 0, 0, 0))
        for i in range(FRAMES):
            rng = np.random.default_rng(1000 + sum(map(ord, nome)))   # mesma semente em todos os quadros: as partículas continuam
            t = i / (FRAMES - 1) if nome != "cast_aura" else i / FRAMES
            sheet.paste(to_rgba(fn(t, rng)), ((i % COLS) * N, (i // COLS) * N))
        destino = OUT / f"{nome}.webp"
        sheet.save(destino, "WEBP", quality=88, method=6)
        manifesto[nome] = {"descricao": descricao, "quadros": FRAMES, "grade": [COLS, ROWS], "tamanho": N, "bytes": destino.stat().st_size}
        print(f"{nome:15s} {destino.stat().st_size/1024:6.1f} KB  {descricao}")
    (OUT / "manifest.json").write_text(json.dumps(manifesto, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
