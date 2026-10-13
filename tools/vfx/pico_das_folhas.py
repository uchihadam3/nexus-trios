"""
O pico de cada folha de efeito da Mecânica única (pedido do jogador: "o Deidara explode… só aparece o dano"):
muitas folhas têm uma chegada desenhada dentro delas (os pássaros do Katsu voam e só então explodem). O número de
dano tem de cair no estouro, não no primeiro quadro. Aqui se mede, em cada folha 3 × 4, o quadro em que a luz
(alfa × brilho) mais cresce e grava a fração do tempo em que ele acontece em src/presentation/pico-das-folhas.ts.

Uso: python3 tools/vfx/pico_das_folhas.py
"""
import re
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SAIDA = ROOT / "src/presentation/pico-das-folhas.ts"
EFEITOS = (ROOT / "src/presentation/unicas-efeitos.ts").read_text()
NOVAS = (ROOT / "src/presentation/vfx-familias-novas.ts").read_text()


def impacto_da(familia: str) -> str:
    m = re.search(rf"\b{familia}: n\(\{{[^}}]*impacto: '([a-z0-9_]+)'", NOVAS)
    return m.group(1) if m else familia


def pico(folha: Path) -> float:
    a = np.asarray(Image.open(folha).convert("RGBA"), dtype=np.float32) / 255
    h, w = a.shape[0] // 4, a.shape[1] // 3
    luz = []
    for i in range(12):
        q = a[(i // 3) * h:(i // 3 + 1) * h, (i % 3) * w:(i % 3 + 1) * w]
        luz.append(float((q[..., 3] * q[..., :3].mean(axis=2)).sum()))
    # o estouro é o maior salto de luz de um quadro para o seguinte (o quadro mais claro costuma ser o rastro depois)
    salto = [luz[0]] + [luz[i] - luz[i - 1] for i in range(1, 12)]
    k = int(np.argmax(salto))
    return round(k / 12, 3)


def main() -> None:
    familias = sorted(set(re.findall(r"familia: '([a-z0-9_]+)'", EFEITOS)))
    picos = {}
    for f in familias:
        folha = ROOT / f"public/assets/vfx/familias/{impacto_da(f)}.webp"
        if folha.exists():
            p = pico(folha)
            if p >= 0.15:  # só as que guardam a chegada dentro da folha
                picos[f] = p
    linhas = ",\n".join(f"  {k}: {v}" for k, v in picos.items())
    SAIDA.write_text(
        "/* Gerado por tools/vfx/pico_das_folhas.py — não editar à mão. */\n"
        "/** Em que fração da folha (1,5 s a 1×) o efeito da Mecânica única bate de verdade: o número espera esse quadro. */\n"
        f"export const PICO_DA_FOLHA: Record<string, number> = {{\n{linhas},\n}};\n"
    )
    print(f"{SAIDA.relative_to(ROOT)}: {len(picos)} de {len(familias)} folhas com a chegada dentro")


if __name__ == "__main__":
    main()
