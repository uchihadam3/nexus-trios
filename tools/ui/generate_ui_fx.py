"""Animações de interface (remake das telas), desenhadas em Python.

Mesmo formato das famílias de efeito da batalha: folha 3×4 com 12 quadros,
neutra (brilho no alfa, "calor" no cinza). A tela pinta com a cor que quiser
(máscara) e soma o núcleo claro por cima. Assim a mesma explosão de pontos é
dourada na vitória e azul no ranking.

Folhas:
  raios      — leque de raios girando devagar atrás do medalhão (laço)
  pontos     — estouro de pontos: anel, faíscas e brilho central (uma vez)
  recorde    — estouro grande de recorde, com estrela de 8 pontas (uma vez)
  faiscas    — poeira de luz subindo, para fundos de destaque (laço)
  brilho     — faixa de luz atravessando um botão (laço, folha larga)

Uso: python3 tools/ui/generate_ui_fx.py [nomes...]
     (gera public/assets/ui/fx/*.webp e manifest.json)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "vfx"))
from luz import Tela, apaga, ease_out, janela, smooth, some  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public/assets/ui/fx"
COLS, ROWS, FRAMES = 3, 4, 12

GRANDE = Tela(256)
LARGA = Tela(384, 96)


def raios(T: Tela, t: float, rng):
    """Raios de vitória: 14 lâminas de luz que giram 1/14 de volta por laço (emenda perfeita)."""
    n = 14
    giro = t * 2 * math.pi / n
    a = (T.ANG - giro) * n / 2
    lamina = np.abs(np.cos(a)) ** 4.5
    # metade das lâminas mais curtas, para o leque não parecer um relógio
    longo = (np.cos((T.ANG - giro) * n / 2) > 0).astype(np.float32)
    alcance = smooth(-T.RAD, -(0.8 + 0.18 * longo), -0.12)
    perto = smooth(T.RAD, 0.05, 0.28)
    G = lamina * alcance * perto * 0.62 + T.gauss(0, 0, 0.26) * 0.5
    H = T.gauss(0, 0, 0.14) * 0.7 + lamina * smooth(-T.RAD, -0.45, -0.1) * perto * 0.22
    return G, H


def _faiscas_radiais(T: Tela, rng, t, n, alcance, sigma):
    pts = []
    for _ in range(n):
        ang = rng.uniform(0, 2 * math.pi)
        vel = rng.uniform(0.55, 1.0)
        d = alcance * vel * ease_out(t, 2.6)
        x, y = math.cos(ang) * d, math.sin(ang) * d + 0.25 * t * t  # um pouco de gravidade
        brilho = (1 - t) ** 1.4 * rng.uniform(0.6, 1.0)
        pts.append((x, y, brilho))
    G = T.zero()
    for x, y, b in pts:
        G += T.gauss(x, y, sigma) * b
    return G


def pontos(T: Tela, t: float, rng):
    """Estouro de pontos: clarão, anel que abre, faíscas que voam e caem."""
    clarao = T.gauss(0, 0, 0.18 + 0.1 * t) * apaga(t, 0.0, 0.55) * 1.4
    anel = T.ring(0.15 + 0.7 * ease_out(t, 2.2), 0.05 + 0.04 * t) * apaga(t, 0.1, 1.0)
    fa = _faiscas_radiais(T, rng, t, 46, 0.85, 0.022)
    cruz = (T.gauss(0, 0, 0.9, 0.018) + T.gauss(0, 0, 0.018, 0.9)) * apaga(t, 0.0, 0.45) * 0.9
    G = clarao + anel * 0.9 + fa + cruz
    H = clarao * 0.9 + fa * 0.7 + cruz * 0.6
    return G, H


def recorde(T: Tela, t: float, rng):
    """Recorde: estrela de 8 pontas que cresce e gira, dois anéis e chuva de faíscas."""
    giro = 0.4 * t
    pontas = np.abs(np.cos((T.ANG - giro) * 4)) ** 14
    raio = 0.25 + 0.55 * ease_out(t, 2.0)
    estrela = pontas * smooth(-T.RAD, -raio, -0.02) * smooth(T.RAD, 0.02, 0.12) * apaga(t, 0.15, 1.0)
    nucleo = T.gauss(0, 0, 0.2) * (0.6 + 0.6 * apaga(t, 0.0, 0.5))
    anel1 = T.ring(0.2 + 0.72 * ease_out(t, 2.4), 0.04) * apaga(t, 0.05, 0.9)
    anel2 = T.ring(0.1 + 0.55 * ease_out(max(0, t - 0.18) / 0.82, 2.4), 0.03) * janela(t, 0.18, 1.0) * apaga(t, 0.3, 1.0)
    fa = _faiscas_radiais(T, rng, t, 70, 0.95, 0.018)
    G = estrela * 1.1 + nucleo + anel1 + anel2 * 0.8 + fa
    H = nucleo * 0.9 + estrela * 0.5 + fa * 0.6
    return G, H


def faiscas_laco(T: Tela, t: float, rng):
    """Poeira de luz subindo devagar. Cada grão tem fase própria; o laço fecha em t=1."""
    G = T.zero()
    for _ in range(38):
        x0 = rng.uniform(-0.85, 0.85)
        fase = rng.uniform(0, 1)
        vel = rng.uniform(0.7, 1.0)
        tt = (t * vel + fase) % 1.0
        y = 0.85 - 1.7 * tt
        x = x0 + 0.05 * math.sin(2 * math.pi * (tt * 2 + fase))
        b = math.sin(math.pi * tt) ** 1.5 * rng.uniform(0.5, 1.0)
        G += T.gauss(x, y, rng.uniform(0.012, 0.024)) * b
    return G, G * 0.7


def brilho(T: Tela, t: float, rng):
    """Uma faixa inclinada que atravessa o botão da esquerda para a direita, depois descansa."""
    x = -1.4 + 2.8 * smooth(np.float32(t), 0.0, 0.55)
    faixa = np.exp(-(((T.U - x) + 0.45 * T.V) / 0.11) ** 2)
    fina = np.exp(-(((T.U - x - 0.16) + 0.45 * T.V) / 0.03) ** 2) * 0.6
    G = (faixa + fina) * janela(t, 0.0, 0.62)
    return G, G * 0.9


FOLHAS = {
    "raios": (raios, GRANDE, True, "raios de vitória girando"),
    "pontos": (pontos, GRANDE, False, "estouro de pontos"),
    "recorde": (recorde, GRANDE, False, "estouro de recorde"),
    "faiscas": (faiscas_laco, GRANDE, True, "poeira de luz subindo"),
    "brilho": (brilho, LARGA, True, "brilho atravessando o botão"),
}


def renderiza(nome: str) -> Image.Image:
    fn, T, laco, _ = FOLHAS[nome]
    folha = Image.new("RGBA", (T.w * COLS, T.h * ROWS), (0, 0, 0, 0))
    for i in range(FRAMES):
        rng = np.random.default_rng(4000 + sum(map(ord, nome)))  # mesma semente: as partículas continuam
        t = i / FRAMES if laco else i / (FRAMES - 1)
        G, H = fn(T, t, rng)
        folha.paste(T.quadro(G, H), ((i % COLS) * T.w, (i // COLS) * T.h))
    return folha


def main(argv):
    OUT.mkdir(parents=True, exist_ok=True)
    manifesto = {}
    for nome in argv or FOLHAS:
        _, T, laco, descricao = FOLHAS[nome]
        destino = OUT / f"{nome}.webp"
        renderiza(nome).save(destino, "WEBP", quality=84, method=6)
        manifesto[nome] = {"descricao": descricao, "quadros": FRAMES, "grade": [COLS, ROWS], "tamanho": [T.w, T.h], "laco": laco, "bytes": destino.stat().st_size}
        print(f"{nome:10s} {destino.stat().st_size / 1024:6.1f} KB  {descricao}")
    (OUT / "manifest.json").write_text(json.dumps(manifesto, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
