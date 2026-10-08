#!/usr/bin/env python3
"""
Curvas de movimento da atuação (adendo, parte 2), simuladas e não desenhadas à mão.

Para cada estilo há um roteiro de para onde o medalhão "quer ir" ao longo do
beat (avançar até o alvo, segurar no impacto, voltar). Uma mola amortecida
persegue esse roteiro, resolvida com `scipy.integrate.solve_ivp`; é a física
que dá antecipação, aceleração, ultrapassagem no contato e assentamento. Da
velocidade sai o estica-e-achata (squash/stretch) e a inclinação.

O resultado são @keyframes CSS com dezenas de amostras, escritos em
src/presentation/acting-motion.css. O jogo só fornece, na hora, a direção e a
distância até o alvo (--act-dx, --act-dy, --act-ux, --act-uy).

O impacto acontece a 48% do beat (PRESENTATION.impactAt); quem age chega no
alvo nesse instante. As reações começam no impacto e duram o resto do beat.

Uso: python3 tools/vfx/generate_motion.py
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "src/presentation/acting-motion.css"
IMPACT = 0.48
AMOSTRAS = 40


def mola(roteiro, k: float, zeta: float, t_fim: float = 1.0, x0: float = 0.0, v0: float = 0.0):
    """x'' = k (alvo(t) − x) − 2 ζ √k x'.  Devolve tempos, posição e velocidade."""
    tt, alvo = zip(*roteiro)
    alvo_de = interp1d(tt, alvo, kind="linear", bounds_error=False, fill_value=(alvo[0], alvo[-1]))
    c = 2 * zeta * math.sqrt(k)

    def f(t, y):
        return [y[1], k * (float(alvo_de(t)) - y[0]) - c * y[1]]

    ts = np.linspace(0, t_fim, AMOSTRAS + 1)
    sol = solve_ivp(f, (0, t_fim), [x0, v0], t_eval=ts, max_step=1 / 400, rtol=1e-7, atol=1e-9)
    return sol.t, sol.y[0], sol.y[1]


def impulso(k: float, zeta: float, v0: float, t_fim: float = 1.0):
    """Mola em repouso que leva um empurrão: o recuo de quem é atingido."""
    return mola([(0, 0), (1, 0)], k, zeta, t_fim, 0.0, v0)


def fmt(x: float) -> str:
    s = f"{x:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def keyframes(nome: str, frames) -> str:
    linhas = [f"@keyframes {nome}{{"]
    for pct, transform, extra in frames:
        linhas.append(f"{fmt(pct * 100)}%{{transform:{transform}{(';' + extra) if extra else ''}}}")
    linhas.append("}")
    return "".join(linhas)


def ao_longo(p: float, s_par: float = 1.0, s_perp: float = 1.0, lado: float = 0.0, extra_rot: float = 0.0) -> str:
    """Desloca p × (dx, dy), mais `lado` px na perpendicular; estica na direção do movimento."""
    tx = f"calc(var(--act-dx) * {fmt(p)} + var(--act-uy) * {fmt(-lado)}px)"
    ty = f"calc(var(--act-dy) * {fmt(p)} + var(--act-ux) * {fmt(lado)}px)"
    sc = f"scale({fmt(s_perp)},{fmt(s_par)})" if abs(s_par - 1) > 1e-3 or abs(s_perp - 1) > 1e-3 else ""
    rot = f" rotate({fmt(extra_rot)}deg)" if abs(extra_rot) > 1e-3 else ""
    return f"translate({tx},{ty}){(' ' + sc) if sc else ''}{rot}"


def esticar(v: np.ndarray, quanto: float) -> np.ndarray:
    m = max(1e-6, float(np.abs(v).max()))
    return np.abs(v) / m * quanto


# ---------------------------------------------------------------- quem age
def melee(rapido: bool = False):
    """Recua, avança até o alvo, encosta no impacto, volta."""
    a0, a1 = (0.06, 0.16) if rapido else (0.08, 0.2)
    roteiro = [(0, 0), (a0, -0.14), (a1, -0.14), (IMPACT - 0.07, 1.0), (IMPACT + 0.09, 1.0), (0.78, 0.0), (1, 0)]
    t, x, v = mola(roteiro, k=900 if rapido else 650, zeta=0.62)
    st = esticar(v, 0.09)
    return [(ti, ao_longo(xi) + f" scale({fmt(1 + si)})", "") for ti, xi, si in zip(t, x, st)]


def ranged():
    """Inclina para o alvo carregando; no disparo, o tranco para trás; assenta."""
    roteiro = [(0, 0), (0.3, 0.55), (IMPACT - 0.06, 0.7), (IMPACT - 0.04, -1.1), (IMPACT + 0.08, -1.1), (0.7, 0.0), (1, 0)]
    t, x, v = mola(roteiro, k=1100, zeta=0.55)
    pulso = np.exp(-((t - (IMPACT - 0.03)) / 0.05) ** 2) * 0.08
    return [(ti, ao_longo(xi) + f" scale({fmt(1 + pi)})", "") for ti, xi, pi in zip(t, x, pulso)]


def area():
    """Sobe, fica no ar, desce batendo no chão (achata), assenta."""
    roteiro = [(0, 0), (0.12, 0.25), (0.34, -1.0), (IMPACT - 0.05, -1.0), (IMPACT, 0.35), (IMPACT + 0.12, 0.35), (0.75, 0), (1, 0)]
    t, y, v = mola(roteiro, k=1300, zeta=0.5)
    achata = np.clip(y, 0, None) * 0.28
    frames = []
    for ti, yi, ai in zip(t, y, achata):
        frames.append((ti, f"translateY({fmt(yi * 16)}px) scale({fmt(1 + ai)},{fmt(1 - ai)})", ""))
    return frames


def support():
    """Pulsa e se inclina para o aliado, entrega, volta."""
    roteiro = [(0, 0), (0.25, 0.5), (IMPACT, 1.0), (IMPACT + 0.1, 0.6), (0.8, 0), (1, 0)]
    t, x, v = mola(roteiro, k=420, zeta=0.7)
    pulso = 0.1 * np.exp(-((t - 0.4) / 0.13) ** 2)
    return [(ti, ao_longo(xi) + f" scale({fmt(1 + pi)})", "") for ti, xi, pi in zip(t, x, pulso)]


def curse():
    """Inclina para o inimigo e treme de leve, como quem lança uma maldição."""
    roteiro = [(0, 0), (0.3, 0.8), (IMPACT, 1.0), (0.75, 0), (1, 0)]
    t, x, v = mola(roteiro, k=500, zeta=0.65)
    treme = 2.2 * np.sin(t * 2 * math.pi * 11) * np.exp(-((t - 0.36) / 0.13) ** 2)
    return [(ti, ao_longo(xi, lado=si), "") for ti, xi, si in zip(t, x, treme)]


def cast():
    """Ergue-se e segura o Preparo, respirando."""
    roteiro = [(0, 0), (0.2, 1.0), (1, 1.0)]
    t, y, v = mola(roteiro, k=380, zeta=0.55)
    resp = 0.02 * np.sin(t * 2 * math.pi * 2)
    return [(ti, f"translateY({fmt(-y * 7)}px) scale({fmt(1 + 0.06 * y + ri)})", "") for ti, y, ri in zip(t, y, resp)]


# ---------------------------------------------------------------- quem recebe
def hit(pesado: bool = False):
    """Empurrão para longe de quem bateu, tremor perpendicular, assenta."""
    t, x, v = impulso(k=700 if pesado else 900, zeta=0.42, v0=38 if pesado else 26)
    amp = 9 if pesado else 6
    treme = amp * np.sin(t * 2 * math.pi * (9 if pesado else 12)) * np.exp(-t / 0.28)
    achata = 0.06 * np.exp(-((t - 0.04) / 0.06) ** 2) * (1.6 if pesado else 1)
    frames = []
    for ti, xi, si, ai in zip(t, x, treme, achata):
        tx = f"calc(var(--act-ux) * {fmt(xi)}px + var(--act-uy) * {fmt(-si)}px)"
        ty = f"calc(var(--act-uy) * {fmt(xi)}px + var(--act-ux) * {fmt(si)}px)"
        frames.append((ti, f"translate({tx},{ty}) scale({fmt(1 - ai)})", ""))
    return frames


def lift(altura: float, escala: float, k: float = 260):
    roteiro = [(0, 0), (0.35, 1.0), (0.7, 1.0), (1, 0)]
    t, y, v = mola(roteiro, k=k, zeta=0.6)
    return [(ti, f"translateY({fmt(-yi * altura)}px) scale({fmt(1 + yi * escala)})", "") for ti, yi in zip(t, y)]


def shield():
    t, x, v = impulso(k=900, zeta=0.35, v0=12)
    return [(ti, f"scale({fmt(1 + xi * 0.012)})", "") for ti, xi in zip(t, x)]


def broken():
    t = np.linspace(0, 1, AMOSTRAS + 1)
    treme = 5 * np.sin(t * 2 * math.pi * 14) * np.exp(-t / 0.3)
    _, s, _ = impulso(k=600, zeta=0.5, v0=-6)
    return [(ti, f"translateX({fmt(si)}px) scale({fmt(1 + ci * 0.01)})", "") for ti, si, ci in zip(t, treme, s)]


def curse_react():
    t = np.linspace(0, 1, AMOSTRAS + 1)
    treme = 2.5 * np.sin(t * 2 * math.pi * 16) * np.exp(-t / 0.4)
    return [(ti, f"translateX({fmt(si)}px)", "") for ti, si in zip(t, treme)]


def fall():
    roteiro = [(0, 0), (0.25, 1.0), (1, 1.0)]
    t, y, v = mola(roteiro, k=520, zeta=0.45)
    return [(ti, f"translateY({fmt(yi * 12)}px) rotate({fmt(yi * 7)}deg) scale({fmt(1 - yi * 0.1)})", "") for ti, yi in zip(t, y)]


def main() -> None:
    blocos = [
        "/* Gerado por tools/vfx/generate_motion.py — não editar à mão. */",
        "/* Curvas de mola amortecida simuladas com scipy.integrate.solve_ivp. */",
    ]
    for par in ("a", "b"):          # dois nomes idênticos: trocar de nome reinicia a animação a cada beat
        blocos.append(keyframes(f"act-melee-{par}", melee()))
        blocos.append(keyframes(f"act-interrupt-{par}", melee(rapido=True)))
        blocos.append(keyframes(f"act-ranged-{par}", ranged()))
        blocos.append(keyframes(f"act-area-{par}", area()))
        blocos.append(keyframes(f"act-support-{par}", support()))
        blocos.append(keyframes(f"act-curse-{par}", curse()))
        blocos.append(keyframes(f"act-cast-{par}", cast()))
    blocos.append(keyframes("react-hit", hit()))
    blocos.append(keyframes("react-hit-heavy", hit(pesado=True)))
    blocos.append(keyframes("react-heal", lift(6, 0.035)))
    blocos.append(keyframes("react-buff", lift(5, 0.05, k=320)))
    blocos.append(keyframes("react-shield", shield()))
    blocos.append(keyframes("react-curse", curse_react()))
    blocos.append(keyframes("react-broken", broken()))
    blocos.append(keyframes("react-fall", fall()))
    # Folhas de 12 quadros (3 × 4): a posição salta de quadro em quadro.
    for prop in ("background-position", "mask-position"):
        nome = "fx12-bg" if prop == "background-position" else "fx12-mask"
        q = []
        for i in range(12):
            col, lin = i % 3, i // 3
            q.append(f"{fmt(i / 12 * 100)}%{{{prop}:{fmt(col / 2 * 100)}% {fmt(lin / 3 * 100)}%;-webkit-{prop}:{fmt(col / 2 * 100)}% {fmt(lin / 3 * 100)}%}}" if prop == "mask-position" else f"{fmt(i / 12 * 100)}%{{{prop}:{fmt(col / 2 * 100)}% {fmt(lin / 3 * 100)}%}}")
        q.append(f"100%{{{prop}:100% 100%{(';-webkit-' + prop + ':100% 100%') if prop == 'mask-position' else ''}}}")
        blocos.append(f"@keyframes {nome}{{{''.join(q)}}}")
    OUT.write_text("\n".join(blocos) + "\n")
    print(f"{OUT.relative_to(ROOT)}: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
