"""O som da entrega do apoio (src/presentation/entrega-de-apoio.ts): a esfera de cura, Escudo ou reforço saindo de
quem usou e voando até o aliado."""
from __future__ import annotations

import numpy as np

from sfx_familias import _brilho, _z
from som import CRISTAL, SINO, SR, env, graos, modal, n_de, passa, poe, reverb, rosa, seno, sobe_e_some, varre


def apoio_sai(rng, v):
    """A esfera se forma (o brilho que sobe), sai (o sopro macio) e voa (as faíscas cintilando no caminho)."""
    x = _z(1.1)
    n = n_de(0.3)
    poe(x, seno(varre(520, 1180, n, 1.0), n) * sobe_e_some(n, 0.7, 1.2) * 0.05, 0.0)
    for k, f in enumerate((1047, 1319, 1568)):
        poe(x, modal(n_de(0.35), f, rng=rng, **SINO) * env(n_de(0.35), 0.002, 0.2) * 0.035, 0.04 + 0.06 * k)
    m = n_de(0.55)
    poe(x, passa(rosa(rng, m), 900, 6000, 2) * sobe_e_some(m, 0.35, 1.3) * 0.16, 0.18)
    poe(x, graos(rng, n_de(0.5), 30, 0.0, 0.4, 2500, 9000, 0.012) * 0.35, 0.22)
    poe(x, _brilho(rng, 0.4, 1760, 0.03, CRISTAL), 0.3)
    return reverb(x, 0.55, 0.3)


SONS: dict = {
    "apoio-sai": (apoio_sai, "A esfera do apoio saindo para o aliado"),
}
