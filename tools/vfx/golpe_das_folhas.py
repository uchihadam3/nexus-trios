"""Em que quadro de cada folha o golpe acontece (pedido do jogador: "o dano tá aparecendo antes da animação …
tem que ser no impacto da animação o dano aparecer").

Muitas folhas contam o golpe inteiro: a onda sobe e só no quadro 6 quebra, o punho desce e só no quadro 3 bate no
chão. O número de dano sai no impacto do beat; para ele cair junto do golpe desenhado, a folha (e o som dela)
começa um pouco antes (src/presentation/director.ts: antecipaDoGolpe).

O golpe é o quadro em que a luz da folha mais cresce de uma vez (o clarão, a quebra, o corte). Se a folha já
começa forte (o soco que já chega batendo), o golpe é o quadro 0; se a maior subida é logo no quadro 0 mas ainda
fraca (o punho que voa crescendo), o golpe é o primeiro pico forte.

Uso: python3 golpe_das_folhas.py   (reescreve src/presentation/golpe-das-folhas.ts a partir das folhas .webp)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
FOLHAS = RAIZ / "public/assets/vfx/familias"
DESTINO = RAIZ / "src/presentation/golpe-das-folhas.ts"


def quadro_do_golpe(caminho: Path, cols: int = 3, linhas: int = 4) -> int:
    im = np.asarray(Image.open(caminho).convert("RGBA")).astype(float) / 255
    h, w = im.shape[0] // linhas, im.shape[1] // cols
    luz = []
    for k in range(cols * linhas):
        r, c = divmod(k, cols)
        q = im[r * h:(r + 1) * h, c * w:(c + 1) * w]
        luz.append(float((q[..., 3] * q[..., :3].mean(-1)).sum()))
    E = np.array(luz)
    m = E.max()
    if m <= 0 or E[0] >= 0.7 * m:
        return 0
    sobe = np.diff(np.concatenate([[0.0], E]))
    k = int(sobe.argmax())
    if k == 0:
        for j in range(1, len(E)):
            if E[j] >= 0.6 * m and E[j] >= E[j - 1] and (j == len(E) - 1 or E[j] >= E[j + 1]):
                return j
    return k


def main() -> None:
    manifesto = json.loads((FOLHAS / "manifest.json").read_text())
    quadros = {nome: quadro_do_golpe(FOLHAS / f"{nome}.webp", *v["grade"]) for nome, v in sorted(manifesto.items()) if not v["laco"]}
    corpo = ",\n".join(f"  {nome}: {k}" for nome, k in quadros.items())
    DESTINO.write_text(
        "// Gerado por tools/vfx/golpe_das_folhas.py: não edite à mão.\n"
        "/** Em que quadro (0–11) de cada folha de impacto o golpe acontece: o número de dano cai nesse quadro. */\n"
        f"export const QUADRO_DO_GOLPE: Record<string, number> = {{\n{corpo},\n}};\n"
    )
    print(f"{len(quadros)} folhas medidas → {DESTINO.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
