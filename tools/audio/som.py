"""
Ferramentas de síntese para os efeitos sonoros (adendo, parte 6).

Tudo em NumPy/SciPy, determinístico, a 44,1 kHz. Os sons são montados em
camadas, como se faz com som de jogo:

- **transiente**: o clique/estalo dos primeiros milissegundos, que dá o "ataque";
- **corpo**: o que define o tipo (baque grave, chiado de fogo, sino de cura…);
- **cauda**: o que sobra no ar (reverberação curta, poeira, centelhas).

Alguns blocos:
- `modal`: soma de senoides amortecidas com razões inarmônicas — metal, vidro,
  cristal, sino. É o que dá o brilho do corte, do escudo e do gelo.
- `faixas`: ruído passando por várias bandas, com o peso de cada banda variando
  no tempo — um filtro que "varre" sem precisar de laço amostra a amostra.
- `reverb`: pequena sala (pentes + passa-tudo, à moda de Schroeder) com
  `scipy.signal.lfilter`.
- `limita`: deixa o pico em −1 dBFS, sem estourar.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.signal import butter, lfilter, sosfilt

SR = 44100


def n_de(seg: float) -> int:
    return max(1, int(round(seg * SR)))


def tempo(seg: float) -> np.ndarray:
    return np.arange(n_de(seg)) / SR


def cabe(x: np.ndarray, n: int) -> np.ndarray:
    """Corta ou completa com silêncio até n amostras."""
    if len(x) >= n:
        return x[:n]
    return np.concatenate([x, np.zeros(n - len(x))])


def poe(destino: np.ndarray, x: np.ndarray, em: float, ganho: float = 1.0) -> None:
    """Soma x dentro de destino a partir do instante `em` (s)."""
    i = int(round(em * SR))
    if i >= len(destino):
        return
    j = min(len(destino), i + len(x))
    destino[i:j] += x[: j - i] * ganho


# ------------------------------------------------------------------ envelopes
def env(n: int, ataque: float = 0.004, queda: float = 0.2, curva: float = 1.0, segura: float = 0.0) -> np.ndarray:
    """Ataque curto (seno), segura, e queda exponencial com constante `queda` (s)."""
    t = np.arange(n) / SR
    a = np.clip(t / max(ataque, 1e-4), 0, 1)
    sobe = np.sin(a * math.pi / 2) ** 2
    cai = np.exp(-np.maximum(0, t - ataque - segura) / max(queda, 1e-4)) ** curva
    return sobe * cai


def janela_suave(n: int, entra: float = 0.01, sai: float = 0.05) -> np.ndarray:
    t = np.arange(n) / SR
    dur = n / SR
    a = np.clip(t / max(entra, 1e-4), 0, 1)
    b = np.clip((dur - t) / max(sai, 1e-4), 0, 1)
    return (np.sin(a * math.pi / 2) ** 2) * (np.sin(b * math.pi / 2) ** 2)


def sobe_e_some(n: int, pico: float = 0.6, forma: float = 2.0) -> np.ndarray:
    """Cresce até `pico` (fração) e some — para subidas, cargas e redemoinhos."""
    x = np.linspace(0, 1, n)
    up = np.clip(x / pico, 0, 1) ** forma
    down = np.clip((1 - x) / (1 - pico), 0, 1) ** 1.2
    return np.where(x < pico, up, down)


# ------------------------------------------------------------------ fontes
def ruido(rng: np.random.Generator, n: int) -> np.ndarray:
    return rng.standard_normal(n)


def rosa(rng: np.random.Generator, n: int) -> np.ndarray:
    """Ruído rosa (−3 dB/oitava) pelo filtro de Paul Kellet simplificado."""
    b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
    a = [1, -2.494956002, 2.017265875, -0.522189400]
    x = lfilter(b, a, rng.standard_normal(n))
    return x / (np.std(x) + 1e-9)


def seno(freq, n: int, fase: float = 0.0) -> np.ndarray:
    """Senoide com frequência constante ou curva (array do tamanho n)."""
    f = np.broadcast_to(np.asarray(freq, float), (n,))
    return np.sin(fase + 2 * math.pi * np.cumsum(f) / SR)


def varre(f0: float, f1: float, n: int, forma: float = 1.0) -> np.ndarray:
    """Curva de frequência de f0 a f1 (exponencial; forma>1 chega rápido)."""
    x = np.linspace(0, 1, n) ** (1 / forma)
    return f0 * (f1 / f0) ** x


def serra_suave(freq, n: int, harm: int = 8) -> np.ndarray:
    """Dente de serra com poucos harmônicos (sem serrilhado áspero)."""
    f = np.broadcast_to(np.asarray(freq, float), (n,))
    fase = 2 * math.pi * np.cumsum(f) / SR
    return sum(np.sin(k * fase) / k for k in range(1, harm + 1)) * 0.6


def modal(n: int, f0: float, razoes, quedas, ganhos=None, rng=None, desafina: float = 0.0) -> np.ndarray:
    """Senoides amortecidas: metal, vidro, cristal, sino."""
    t = np.arange(n) / SR
    out = np.zeros(n)
    ganhos = ganhos or [1.0] * len(razoes)
    for r, q, g in zip(razoes, quedas, ganhos):
        f = f0 * r * (1 + (rng.uniform(-desafina, desafina) if rng is not None and desafina else 0))
        if f >= SR * 0.45:
            continue
        out += g * np.sin(2 * math.pi * f * t + (rng.uniform(0, 6.28) if rng is not None else 0)) * np.exp(-t / q)
    return out


METAL = dict(razoes=[1.0, 2.76, 5.40, 8.93, 13.34], quedas=[0.35, 0.22, 0.14, 0.09, 0.06], ganhos=[1, 0.7, 0.5, 0.35, 0.2])
VIDRO = dict(razoes=[1.0, 2.32, 4.25, 6.63, 9.38], quedas=[0.5, 0.35, 0.25, 0.16, 0.1], ganhos=[1, 0.6, 0.45, 0.3, 0.2])
SINO = dict(razoes=[0.5, 1.0, 1.19, 1.56, 2.0, 2.66, 3.01], quedas=[1.2, 0.9, 0.7, 0.55, 0.45, 0.32, 0.25], ganhos=[0.5, 1, 0.6, 0.5, 0.45, 0.3, 0.2])
CRISTAL = dict(razoes=[1.0, 2.01, 3.03, 4.7, 6.2], quedas=[0.6, 0.4, 0.3, 0.18, 0.12], ganhos=[1, 0.5, 0.4, 0.25, 0.18])


# ------------------------------------------------------------------ filtros
def passa(x: np.ndarray, lo: float | None, hi: float | None, ordem: int = 2) -> np.ndarray:
    if lo and hi:
        sos = butter(ordem, [lo, min(hi, SR * 0.45)], btype="bandpass", fs=SR, output="sos")
    elif lo:
        sos = butter(ordem, lo, btype="highpass", fs=SR, output="sos")
    elif hi:
        sos = butter(ordem, min(hi, SR * 0.45), btype="lowpass", fs=SR, output="sos")
    else:
        return x
    return sosfilt(sos, x)


def faixas(x: np.ndarray, centros, curva_centro: np.ndarray, largura: float = 0.5) -> np.ndarray:
    """Filtro que varre: soma de bandas fixas pesadas pela distância (em oitavas)
    entre o centro de cada banda e a curva de frequência pedida."""
    n = len(x)
    out = np.zeros(n)
    lc = np.log2(np.maximum(curva_centro, 20))
    for c in centros:
        banda = passa(x, c / 1.41, c * 1.41, 2)
        peso = np.exp(-((lc - math.log2(c)) / largura) ** 2)
        out += banda * peso
    return out


CENTROS = [120, 180, 260, 380, 560, 820, 1200, 1750, 2500, 3600, 5200, 7500, 10500]


def assobio(rng, n: int, f0: float, f1: float, forma: float = 1.0, largura: float = 0.45) -> np.ndarray:
    """Vento/whoosh: ruído rosa por um filtro que varre de f0 a f1."""
    return faixas(rosa(rng, n), CENTROS, varre(f0, f1, n, forma), largura)


# ------------------------------------------------------------------ peças prontas
def baque(n: int, f0: float = 90, f1: float = 45, queda: float = 0.12, clique: float = 0.4) -> np.ndarray:
    """Baque grave com o tom caindo (o "peso" de um golpe).

    Alto-falante de celular quase não toca abaixo de ~150 Hz. Por isso o baque
    passa por uma saturação suave, que cria harmônicos de 2 a 5 vezes a
    fundamental, e ganha um "toc" médio de 250–900 Hz: no fone o peso continua
    grave, e no celular o golpe ainda se ouve.
    """
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.035)
    fase = 2 * math.pi * np.cumsum(f) / SR
    corpo = np.sin(fase) * np.exp(-t / queda)
    harmonicos = (np.tanh(np.sin(fase) * 2.5) / math.tanh(2.5) - np.sin(fase) * 0.6) * np.exp(-t / (queda * 0.6))
    toc = np.sin(2 * math.pi * np.cumsum(f * 3.2) / SR) * np.exp(-t / min(0.03, queda * 0.4))
    estalo = np.exp(-t / 0.002) * clique
    # o sub-grave cede espaço: o peso fica, e sobra margem para o médio que o celular toca
    return passa(corpo, 45, None, 1) * 0.75 + harmonicos * 0.95 + toc * 0.75 + estalo


def estalo(rng, n: int, lo: float = 1500, hi: float = 6000, queda: float = 0.012) -> np.ndarray:
    """Estalo curto de ruído (o "tapa" do contato)."""
    return passa(ruido(rng, n), lo, hi, 2) * env(n, 0.0008, queda)


def graos(rng, n: int, quantos: int, inicio: float, fim: float, lo: float, hi: float, queda: float = 0.006, ganho_var: float = 0.5) -> np.ndarray:
    """Pequenos estalos espalhados no tempo: cascalho, crepitar, centelhas."""
    out = np.zeros(n)
    grao = n_de(queda * 6)
    for _ in range(quantos):
        em = rng.uniform(inicio, fim)
        g = passa(ruido(rng, grao), lo * rng.uniform(0.8, 1.2), hi, 2) * env(grao, 0.0005, queda) * rng.uniform(1 - ganho_var, 1)
        poe(out, g, em)
    return out


def satura(x: np.ndarray, drive: float = 2.0) -> np.ndarray:
    return np.tanh(x * drive) / math.tanh(drive)


def pente(x: np.ndarray, d: int, g: float) -> np.ndarray:
    """Filtro pente y[n] = x[n] + g·y[n−d], em blocos de d amostras (linear e rápido,
    em vez de um filtro IIR de ordem d amostra a amostra)."""
    n = len(x)
    y = np.zeros(n + d)
    y[d:] = 0
    for i in range(0, n, d):
        j = min(n, i + d)
        y[d + i:d + j] = x[i:j] + g * y[i:i + (j - i)]
    return y[d:]


def passa_tudo(x: np.ndarray, d: int, g: float) -> np.ndarray:
    """Passa-tudo de Schroeder y[n] = −g·x[n] + x[n−d] + g·y[n−d], em blocos."""
    n = len(x)
    xp = np.concatenate([np.zeros(d), x])
    y = np.zeros(n + d)
    for i in range(0, n, d):
        j = min(n, i + d)
        y[d + i:d + j] = -g * x[i:j] + xp[i:i + (j - i)] + g * y[i:i + (j - i)]
    return y[d:]


def reverb(x: np.ndarray, sala: float = 0.5, umido: float = 0.25, escuro: float = 6000, rng=None) -> np.ndarray:
    """Sala pequena: 4 pentes em paralelo + 2 passa-tudo (Schroeder)."""
    atrasos = [1116, 1188, 1277, 1356]
    fb = 0.72 + 0.22 * sala
    y = sum(pente(x, d, fb) for d in atrasos) / len(atrasos)
    for d, g in ((556, 0.5), (225, 0.5)):
        y = passa_tudo(y, d, g)
    y = passa(y, 150, escuro, 2)
    return x * (1 - umido * 0.4) + y * umido


def cauda_livre(x: np.ndarray, segundos: float) -> np.ndarray:
    """Acrescenta silêncio no fim para a reverberação ter onde soar."""
    return np.concatenate([x, np.zeros(n_de(segundos))])


def limita(x: np.ndarray, teto_db: float = -1.0) -> np.ndarray:
    """Normaliza o pico para o teto, com uma saturação suave nos excessos raros."""
    x = x - np.mean(x[: min(len(x), 64)]) * 0  # sem deslocar
    pico = np.max(np.abs(x)) + 1e-12
    teto = 10 ** (teto_db / 20)
    y = x / pico * teto
    return np.clip(y, -teto, teto)


def apara(x: np.ndarray, limiar_db: float = -60.0, sai: float = 0.03) -> np.ndarray:
    """Corta o silêncio do fim (com um fade curto)."""
    lim = 10 ** (limiar_db / 20) * (np.max(np.abs(x)) + 1e-12)
    idx = np.nonzero(np.abs(x) > lim)[0]
    fim = (idx[-1] + n_de(sai)) if len(idx) else len(x)
    y = x[: min(len(x), fim)].copy()
    k = min(len(y), n_de(sai))
    y[-k:] *= np.linspace(1, 0, k)
    return y


def rms_db(x: np.ndarray) -> float:
    return 20 * math.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


def volume_percebido(x: np.ndarray) -> float:
    """Volume como se ouve em média entre fone e celular: metade do RMS cheio,
    metade do RMS acima de 250 Hz (o que um alto-falante pequeno reproduz)."""
    return 0.5 * rms_db(x) + 0.5 * rms_db(passa(x, 250, None, 2))
