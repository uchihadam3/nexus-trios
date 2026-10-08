"""
Ferramentas de luz compartilhadas pelos geradores de efeitos (adendo, parte 3).

Os efeitos são desenhados como LUZ que se soma, em dois campos:
- `brilho`: onde há efeito e com que força (vira transparência);
- `calor`: a parte quente, o núcleo que estoura para claro (vira o tom de cinza).

No jogo a folha é usada duas vezes: como máscara pintada com a cor do
personagem (o brilho) e por cima, em modo "screen", o próprio cinza (o calor).
Assim a mesma família serve para o Kamehameha azul e a Visão de calor
vermelha, sem uma folha por cor.

Tudo em coordenadas -1..1 (U para a direita, V para baixo), trabalhado em
resolução dobrada e reduzido no fim com o alfa pré-multiplicado, para a borda
não ganhar franja escura.
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, map_coordinates


class Tela:
    """Uma grade de trabalho (w × h quadros finais, com supersample)."""

    def __init__(self, w: int, h: int | None = None, ss: int = 2):
        self.w, self.h, self.ss = w, h or w, ss
        self.W, self.H = self.w * ss, self.h * ss
        y, x = np.mgrid[0:self.H, 0:self.W].astype(np.float32)
        # U vai de -1 a 1 na largura; V usa a mesma escala (pixels quadrados).
        s = 2 / self.W
        self.U = (x + 0.5) * s - 1
        self.V = (y + 0.5) * s - self.H / self.W
        self.RAD = np.hypot(self.U, self.V)
        self.ANG = np.arctan2(self.V, self.U)
        ext_v = self.H / self.W
        # Borda: tudo some suavemente antes da beirada do quadro.
        bu = smooth(-np.abs(self.U), -0.995, -0.86)
        bv = smooth(-np.abs(self.V) / ext_v, -0.995, -0.86)
        self.BORDA = bu * bv

    # -------------------------------------------------- conversões
    def px(self, x: float, y: float) -> tuple[float, float]:
        return ((x + 1) / 2 * self.W, (y + self.H / self.W) / 2 * self.W)

    def zero(self) -> np.ndarray:
        return np.zeros((self.H, self.W), np.float32)

    # -------------------------------------------------- primitivas
    def gauss(self, cx: float, cy: float, sx: float, sy: float | None = None) -> np.ndarray:
        sy = sx if sy is None else sy
        return np.exp(-((self.U - cx) ** 2 / (2 * sx * sx) + (self.V - cy) ** 2 / (2 * sy * sy)))

    def ring(self, radius: float, width: float, cx: float = 0, cy: float = 0, squash: float = 1.0) -> np.ndarray:
        r = np.hypot(self.U - cx, (self.V - cy) * squash)
        return np.exp(-(((r - radius) / max(width, 1e-4)) ** 2))

    def splats(self, points, sigma: float) -> np.ndarray:
        """Pontos (x, y, intensidade) viram brilhos gaussianos."""
        img = self.zero()
        for x, y, w in points:
            ix, iy = self.px(x, y)
            ix, iy = int(ix), int(iy)
            if 0 <= ix < self.W and 0 <= iy < self.H:
                img[iy, ix] += w
        s = sigma * self.W / 2
        return gaussian_filter(img, s) * (2 * math.pi * s * s)

    def lines(self, segs, width: float, blur: float = 0.0) -> np.ndarray:
        """Riscos (x1, y1, x2, y2, intensidade)."""
        im = Image.new("F", (self.W, self.H), 0.0)
        d = ImageDraw.Draw(im)
        for x1, y1, x2, y2, w in segs:
            d.line([self.px(x1, y1), self.px(x2, y2)], fill=float(w), width=max(1, int(width * self.W / 2)))
        a = np.asarray(im, np.float32)
        return gaussian_filter(a, blur * self.W / 2) if blur > 0 else a

    def polyline(self, pts, width: float, w: float = 1.0, blur: float = 0.0) -> np.ndarray:
        im = Image.new("F", (self.W, self.H), 0.0)
        d = ImageDraw.Draw(im)
        if len(pts) > 1:
            d.line([self.px(x, y) for x, y in pts], fill=float(w), width=max(1, int(width * self.W / 2)), joint="curve")
        a = np.asarray(im, np.float32)
        return gaussian_filter(a, blur * self.W / 2) if blur > 0 else a

    def polys(self, shapes, blur: float = 0.0) -> np.ndarray:
        """Polígonos ((pontos), intensidade). Sobrepostos somam."""
        out = self.zero()
        for pts, w in shapes:
            im = Image.new("F", (self.W, self.H), 0.0)
            ImageDraw.Draw(im).polygon([self.px(x, y) for x, y in pts], fill=float(w))
            out += np.asarray(im, np.float32)
        return gaussian_filter(out, blur * self.W / 2) if blur > 0 else out

    def tapered(self, segs, width: float) -> np.ndarray:
        """Rastros que afinam: grossos na cabeça (x2, y2), finos na cauda."""
        shapes = []
        for x1, y1, x2, y2, w in segs:
            ang = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
            ox, oy = math.cos(ang) * width / 2, math.sin(ang) * width / 2
            dx, dy = (x2 - x1) * 0.05, (y2 - y1) * 0.05
            shapes.append(([(x1, y1), (x2 + ox, y2 + oy), (x2 + dx, y2 + dy), (x2 - ox, y2 - oy)], w))
        im = Image.new("F", (self.W, self.H), 0.0)
        d = ImageDraw.Draw(im)
        for pts, w in shapes:
            d.polygon([self.px(x, y) for x, y in pts], fill=float(w))
        return np.asarray(im, np.float32)

    def blur(self, a: np.ndarray, sigma: float) -> np.ndarray:
        return gaussian_filter(a, sigma * self.W / 2)

    def glow(self, a: np.ndarray, core: float, halo: float, sigma: float) -> np.ndarray:
        """Núcleo nítido mais halo largo: o que faz um risco parecer luz."""
        return a * core + self.blur(a, sigma) * halo

    def flare(self, cx: float, cy: float, size: float, ang: float = 0.0, thin: float = 0.008) -> np.ndarray:
        """Estrela de clarão de quatro pontas."""
        out = self.zero()
        for a in (ang, ang + math.pi / 2):
            pu = (self.U - cx) * math.cos(a) + (self.V - cy) * math.sin(a)
            pv = -(self.U - cx) * math.sin(a) + (self.V - cy) * math.cos(a)
            out += np.exp(-np.abs(pv) / (thin * size)) * np.exp(-np.abs(pu) / (0.35 * size))
        return out

    def arc_band(self, radius: float, width: float, a0: float, a1: float, squash: float = 1.0, rot: float = 0.0,
                 cx: float = 0.0, cy: float = 0.0, taper: float = 1.0, crescente: bool = False) -> np.ndarray:
        """Faixa curva entre os ângulos a0→a1 (radianos), mais grossa na cabeça (a1).

        `taper` 1 = afina até zero na cauda; a cabeça também arredonda.
        `crescente` desenha meia-lua (as duas pontas finas), o formato de um corte.
        Desenhada numa elipse achatada por `squash` e girada por `rot`.
        """
        cu = (self.U - cx) * math.cos(-rot) - (self.V - cy) * math.sin(-rot)
        cv = (self.U - cx) * math.sin(-rot) + (self.V - cy) * math.cos(-rot)
        cv = cv / squash
        r = np.hypot(cu, cv)
        ang = np.arctan2(cv, cu)
        span = a1 - a0
        if abs(span) < 1e-4:
            return self.zero()
        # posição ao longo do arco, 0 na cauda, 1 na cabeça
        rel = np.mod((ang - a0) * np.sign(span), 2 * math.pi) / abs(span)
        dentro = (rel >= 0) & (rel <= 1)
        rc = np.clip(rel, 0, 1)
        if crescente:
            # meia-lua: fina nas duas pontas, mais grossa perto da cabeça
            perfil = np.where(dentro, (rc ** 1.2) * ((1 - rc) ** 0.3) / 0.62, 0)
        else:
            perfil = np.where(dentro, rc ** taper, 0)
        cabeca = smooth(1 - rel, 0, 0.06) if not crescente else 1.0
        w = width * np.maximum(perfil, 0.02)
        return np.where(dentro, np.exp(-(((r - radius) / np.maximum(w, 1e-4)) ** 2)) * cabeca * (0.35 + 0.65 * perfil), 0).astype(np.float32)

    def warp(self, a: np.ndarray, du: np.ndarray, dv: np.ndarray) -> np.ndarray:
        """Desloca a imagem por campos (em unidades -1..1)."""
        yy, xx = np.mgrid[0:self.H, 0:self.W].astype(np.float32)
        k = self.W / 2
        return map_coordinates(a, [yy - dv * k, xx - du * k], order=1, mode="constant").astype(np.float32)

    def noise(self, rng: np.random.Generator, scale: float, octaves: int = 3) -> np.ndarray:
        """Ruído suave (soma de oitavas), média 0, desvio ~1."""
        out = self.zero()
        amp, s = 1.0, scale
        for _ in range(octaves):
            n = gaussian_filter(rng.standard_normal((self.H, self.W)).astype(np.float32), s * self.W / 2, mode="wrap")
            out += amp * n / (n.std() + 1e-6)
            amp *= 0.5
            s *= 0.5
        return out / (out.std() + 1e-6)

    # -------------------------------------------------- saída
    def quadro(self, brilho: np.ndarray, calor: np.ndarray, ganho: float = 1.75) -> Image.Image:
        """Brilho + calor → RGBA (cinza = calor, alfa = brilho), reduzido ao tamanho final."""
        b = np.maximum(brilho, 0) * self.BORDA
        c = np.maximum(calor, 0) * self.BORDA
        a = 1 - np.exp(-b * ganho)
        h = np.minimum(1 - np.exp(-c * ganho), a)
        pre = np.dstack([h, h, h, a])                      # pré-multiplicado
        im = Image.fromarray((np.clip(pre, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")
        im = im.resize((self.w, self.h), Image.LANCZOS)
        arr = np.asarray(im, np.float32) / 255
        al = arr[..., 3:4]
        rgb = np.where(al > 1e-3, arr[..., :3] / np.maximum(al, 1e-3), 0)
        return Image.fromarray((np.clip(np.dstack([rgb, al]), 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")


# ------------------------------------------------------------------ curvas
def smooth(x, a: float, b: float):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def ease_out(t: float, p: float = 3) -> float:
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** p


def ease_in(t: float, p: float = 2) -> float:
    t = min(max(t, 0.0), 1.0)
    return t ** p


def janela(t: float, a: float, b: float) -> float:
    """0 antes de a, 1 depois de b, suave no meio."""
    if b <= a:
        return 1.0 if t >= a else 0.0
    x = min(max((t - a) / (b - a), 0.0), 1.0)
    return x * x * (3 - 2 * x)


def some(t: float, a: float = 0.0, b: float = 1.0, p: float = 1.6) -> float:
    """Envelope que entra no instante a e some suave até b."""
    if t < a:
        return 0.0
    return float(max(0.0, 1 - ((t - a) / max(b - a, 1e-4)) ** p))


def apaga(t: float, a: float, b: float = 1.0, p: float = 1.4) -> float:
    """Inteiro até o instante a, depois some suave até b."""
    if t <= a:
        return 1.0
    return float(max(0.0, 1 - ((t - a) / max(b - a, 1e-4)) ** p))


def pulso(t: float, a: float, b: float) -> float:
    """Sobe e desce entre a e b (seno)."""
    if t <= a or t >= b:
        return 0.0
    return math.sin(math.pi * (t - a) / (b - a))


def jagged(rng: np.random.Generator, x1, y1, x2, y2, depth: int = 5, rough: float = 0.28):
    """Linha quebrada por deslocamento de ponto médio (raio, rachadura)."""
    pts = [(x1, y1), (x2, y2)]
    amp = math.hypot(x2 - x1, y2 - y1) * rough
    for _ in range(depth):
        novo = [pts[0]]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            mx, my = (ax + bx) / 2, (ay + by) / 2
            nx, ny = -(by - ay), bx - ax
            n = math.hypot(nx, ny) or 1
            d = rng.normal(0, amp)
            novo += [(mx + nx / n * d, my + ny / n * d), (bx, by)]
        pts = novo
        amp *= 0.55
    return pts
