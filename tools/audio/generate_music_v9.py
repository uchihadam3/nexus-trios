#!/usr/bin/env python3
"""
Música v9: as 16 faixas do Caminho do Nexus, compostas nota a nota (substituem a v8).

Pedido do jogador: "as músicas ficaram muito ruins, nem ficaram no mesmo nível das outras; refaça e deixe muito
melhor, diferentes, não músicas genéricas". A v8 gerava as melodias por regra; aqui cada faixa tem o seu tema e o seu
hino escritos à mão (com pergunta e resposta, ponto alto e cadência), a sua harmonia e a sua assinatura de som, no
mesmo arranjo das faixas de batalha que o jogador aprovou (v4–v7): bateria de rock, baixo sintetizado, guitarras,
cordas correndo, supersaw, metais, coro, sinos e taikos, em três camadas (base, pulso e tema).

Cada faixa: Abertura (8) · Tema (16) · Ação (16) · Respiro (8) · Hino (8) · Refrão (8) · Volta (8) = 72 compassos;
o laço volta para o Tema. No Refrão o hino volta inteiro (nas regiões uma oitava acima, dobrado; nos chefes, meio
tom acima). Os temas são escritos em graus da escala ("grau/duração", "|" separa os compassos) e conferidos antes de
tocar: toda nota forte (tempo 1 e 3, ou longa) é nota do acorde.

  REGIÕES                                                  CHEFES (cada um com o seu tema)
  vila      fá maior, 158, power metal heroico              Guardião     fá menor, 160, fanfarra heroica
  floresta  ré dórico, 144, taikos, coro e guitarras        Rainha       ré menor harmônica, 148, serpente cromática
  neon      dó sustenido menor, 150, synthwave de batalha   General Aço  dó menor, 160, marcha de bigorna
  deserto   mi hijaz, 138, maqsum, alaúde e guitarras       Sultão       fá sustenido hijaz, 132, gênio das escalas
  templo    lá in-sen, 132, koto, taikos e guitarras        Assombração  sol sustenido menor, 144, terror pesado
  vulcao    mi frígio, 176, metal                           Titã         dó sustenido frígio, 184, metal mais pesado
  ceu       lá bemol lídio, 152, harpa, coro e metais       Panteão      mi bemol maior, 158, fanfarra do Olimpo
  trono     si menor harmônica, 168, órgão e coro           Imperador    lá menor harmônica, 176, o fim do caminho

Uso:  python3 tools/audio/generate_music_v9.py [checa] [reg-vila … chefe-trono | regioes | chefes]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_music_v4 as v4  # noqa: E402
from generate_music_v3 import pan  # noqa: E402
from generate_music_v4 import baixo, faisca, guitarra, pad, power, riser, supersaw, tom  # noqa: E402
from generate_music_v5 import Musica, coro, cordas, corrida, metais, sino_grande, taiko, timpano  # noqa: E402

ESCALAS = {
    "maior": [0, 2, 4, 5, 7, 9, 11], "lidio": [0, 2, 4, 6, 7, 9, 11], "dorico": [0, 2, 3, 5, 7, 9, 10],
    "menor": [0, 2, 3, 5, 7, 8, 10], "harmonica": [0, 2, 3, 5, 7, 8, 11], "frigio": [0, 1, 3, 5, 7, 8, 10],
    "hijaz": [0, 1, 4, 5, 7, 8, 10], "insen": [0, 1, 5, 7, 8],
}
# graus romanos: o grau da escala da faixa (o "b" só diz que ele é abaixado; se a escala já é, nada muda)
ROMANO = {"I": 0, "II": 1, "III": 2, "IV": 3, "V": 4, "VI": 5, "VII": 6}
MAIOR = ESCALAS["maior"]
SECOES = [("Abertura", 8), ("Tema", 16), ("Ação", 16), ("Respiro", 8), ("Hino", 8), ("Refrão", 8), ("Volta", 8)]
INICIO = {}
_i = 0
for _n, _t in SECOES:
    INICIO[_n] = _i
    _i += _t


def acorde(nome, tonica, escala):
    """'bVI', 'iv', 'V', 'vii°' → (raiz do baixo, notas do pad)."""
    bemol = nome.startswith("b")
    s = nome[1:] if bemol else nome
    dim = s.endswith("°")
    s = s.rstrip("°")
    menor = s.islower()
    esc = ESCALAS[escala]
    grau = ROMANO[s.upper()]
    if len(esc) == 7:
        off = esc[grau] - (1 if bemol and esc[grau] >= MAIOR[grau] else 0)
    else:  # escala de 5 notas: os graus da escala maior
        off = MAIOR[grau] - (1 if bemol else 0)
    raiz = tonica + off
    terca, quinta = (3, 6) if dim else (3, 7) if menor else (4, 7)
    baixo_ = 36 + (raiz - 36) % 12
    notas = sorted(52 + (raiz + i - 52) % 12 for i in (0, terca, quinta))
    return baixo_, notas


def melodia(texto, tonica_base, escala):
    """'grau/dur grau/dur | …' → [(início em tempos, duração, nota MIDI)]; graus com # ou b sobem/descem meio tom."""
    esc = ESCALAS[escala]
    L = len(esc)
    notas, t = [], 0.0
    for b, compasso in enumerate(texto.split("|")):
        soma = 0.0
        for tok in compasso.split():
            g, d = tok.split("/")
            d = float(d)
            if g != "r":
                alt = g.count("#") - g.count("b")
                gi = int(g.rstrip("#b"))
                m = tonica_base + esc[gi % L] + 12 * (gi // L) + alt
                notas.append((t, d, m))
            t += d
            soma += d
        assert abs(soma - 4) < 1e-6, f"compasso {b + 1} soma {soma}: {compasso}"
    return notas


class Faixa:
    def __init__(self, nome, bpm, tonica, escala, base, prog, tema, hino, groove, voz, abertura, acao="riff", chefe=False, semente=1, brilho=5600):
        self.nome, self.bpm, self.tonica, self.escala, self.base = nome, bpm, tonica, escala, base
        self.prog = {k: v.split() for k, v in prog.items()}
        # a Volta começa com os 4 acordes do Tema, para o tema voltar por cima
        self.prog["Volta"] = self.prog["Tema"][:4] + self.prog["Volta"][4:]
        self.prog["Refrão"] = list(self.prog["Hino"])
        self.tema_txt, self.hino_txt = tema, hino
        self.groove, self.voz, self.abertura, self.acao = groove, voz, abertura, acao
        self.chefe, self.semente, self.brilho = chefe, semente, brilho

    def lista(self):
        out = []
        for sec, tam in SECOES:
            p = self.prog[sec]
            assert len(p) in (4, 8, 16), (self.nome, sec, len(p))
            for k in range(tam):
                nome = p[k % len(p)]
                out.append(nome + ("^" if self.chefe and sec == "Refrão" else ""))
        return out

    def acordes(self):
        d = {}
        for nome in set(self.lista()):
            sobe = nome.endswith("^")
            b, n = acorde(nome.rstrip("^"), self.tonica + (1 if sobe else 0), self.escala)
            d[nome] = (b, n)
        return d


def checa(f):
    """Toda nota forte (tempo 1 ou 3, ou de 1,5 tempo ou mais) é nota do acorde do compasso."""
    erros = []
    prog = f.lista()
    for nome, txt, ini in (("tema", f.tema_txt, INICIO["Tema"]), ("hino", f.hino_txt, INICIO["Hino"])):
        for t, d, m in melodia(txt, f.base, f.escala):
            b = ini + int(t // 4)
            forte = (abs(t % 4) < 1e-6 or abs(t % 4 - 2) < 1e-6) or d >= 1.5
            if not forte:
                continue
            _, notas = acorde(prog[b], f.tonica, f.escala)
            if m % 12 not in {n % 12 for n in notas}:
                erros.append(f"{f.nome} {nome} compasso {b - ini + 1} tempo {t % 4 + 1:g}: nota {m} fora de {prog[b]}")
    for nome, txt in (("tema", f.tema_txt), ("hino", f.hino_txt)):
        ms = [m for _, _, m in melodia(txt, f.base, f.escala)]
        if min(ms) < 60 or max(ms) > 89:
            erros.append(f"{f.nome} {nome}: extensão {min(ms)}–{max(ms)} fora de 60–89")
    return erros


# ================================================================== as 16 faixas
def faixas():
    F = {}
    # ------------------------------------------------ REGIÕES
    F["reg-vila"] = Faixa("reg-vila", 158, 65, "maior", 65, {
        "Abertura": "I I IV IV vi vi V V",
        "Tema": "I V vi IV I V IV V vi IV I V IV V I I",
        "Ação": "vi IV I V vi IV I V ii V iii vi IV V V V",
        "Respiro": "IV I vi V IV I ii V",
        "Hino": "IV V iii vi IV V I I",
        "Volta": "I V vi IV I IV V V"},
        "4/.5 4/.5 7/1 7/.5 6/.5 4/1 | 8/1.5 7/.5 6/1 4/1 | 9/1 8/.5 7/.5 7/1 5/1 | 5/2 3/2 |"
        " 4/.5 4/.5 7/1 7/.5 9/.5 9/1 | 8/1.5 9/.5 8/1 6/1 | 5/1 7/.5 8/.5 10/1 9/1 | 8/3 6/1 |"
        " 9/1 7/1 12/1.5 11/.5 | 10/1 9/1 7/2 | 9/1 8/1 7/1 9/1 | 8/2 6/1 4/1 |"
        " 5/1 7/.5 8/.5 10/2 | 8/1 9/1 11/2 | 7/4 | r/4",
        "5/2 7/1 8/1 | 8/3 6/1 | 6/2 9/1 11/1 | 9/3 7/1 | 10/1 9/1 7/2 | 8/1 9/1 11/2 | 9/3 8/1 | 7/4",
        "metal", "ambos", "heroica", acao="metal", semente=901, brilho=5600)
    F["reg-floresta"] = Faixa("reg-floresta", 144, 62, "dorico", 62, {
        "Abertura": "i i IV IV i i bVII bVII",
        "Tema": "i IV i bVII i IV bVII bVII bIII bVII IV IV i IV v i",
        "Ação": "i bVII IV i i bVII IV i bIII IV v v bIII IV i i",
        "Respiro": "IV i bVII i IV i v v",
        "Hino": "bIII bVII IV i bIII bVII IV IV",
        "Volta": "i IV i bVII i IV v v"},
        "11/1.5 9/.5 7/2 | 10/1 12/1 14/2 | 11/1 12/1 11/1 9/1 | 10/3 r/1 |"
        " 11/1.5 9/.5 7/2 | 10/1 12/1 14/1.5 13/.5 | 13/2 10/1 8/1 | 8/4 |"
        " 9/1 11/1 13/2 | 10/1.5 12/.5 13/2 | 14/2 12/1 10/1 | 12/4 |"
        " 11/1 9/1 7/1 9/1 | 10/2 12/2 | 11/2 8/1 6/1 | 7/4",
        "13/2 11/1 9/1 | 10/3 12/1 | 14/2 12/2 | 11/4 | 9/1 11/1 13/2 | 13/1 12/1 10/2 | 12/1 14/1 12/1 10/1 | 10/4",
        "tribal", "coro", "floresta", semente=902, brilho=3400)
    F["reg-neon"] = Faixa("reg-neon", 150, 61, "menor", 61, {
        "Abertura": "i i VI VI III III VII VII",
        "Tema": "i VI III VII i VI III VII iv VI III VII iv VI V V",
        "Ação": "VI VII i i VI VII i i iv v VI VII iv VI V V",
        "Respiro": "VI III VII i VI III VII VII",
        "Hino": "VI VII III i VI VII V V",
        "Volta": "i VI III VII i VI III VII"},
        "11/.75 9/.75 7/.5 9/1 11/1 | 12/1.5 11/.5 9/2 | 9/.75 11/.75 13/.5 11/1 9/1 | 13/2 10/2 |"
        " 11/.75 9/.75 7/.5 9/1 14/1 | 14/1.5 12/.5 12/1 9/1 | 13/1 11/1 9/1 11/1 | 10/3 8/1 |"
        " 10/1 12/1 14/2 | 14/1 12/1 9/2 | 13/1.5 11/.5 9/1 11/1 | 13/2 10/2 |"
        " 12/1 10/1 7/1 10/1 | 12/2 14/2 | 11/1 13#/1 11/1 8/1 | 11/4",
        "12/2 14/1 12/1 | 13/3 10/1 | 11/2 13/1 11/1 | 9/1 11/1 14/2 | 14/2 12/1 14/1 | 13/1.5 12/.5 13/1 10/1 | 11/2 13#/1 11/1 | 11/4",
        "quatro", "saw", "neon", acao="arpejo", semente=903, brilho=7000)
    F["reg-deserto"] = Faixa("reg-deserto", 138, 64, "hijaz", 64, {
        "Abertura": "I I bII bII I I bvii I",
        "Tema": "I bII I I iv bII I I iv iv bvii bvii bII bII I I",
        "Ação": "I bII I bII I bII iv I iv bvii bII I iv bvii bII bII",
        "Respiro": "iv I bII I iv I bII I",
        "Hino": "iv bvii I I bII bII I I",
        "Volta": "I bII I bII I bII bII I"},
        "7/1 8/.25 7/.25 8/.5 9/2 | 8/1 10/1 12/1.5 10/.5 | 11/1 10/.5 9/.5 9/1 8/.5 7/.5 | 7/3 r/1 |"
        " 10/1 11/.5 12/.5 14/2 | 12/1 13/.5 12/.5 10/1 8/1 | 9/1 8/.25 9/.25 8/.5 7/2 | 7/4 |"
        " 10/2 12/2 | 14/1 12/1 10/2 | 13/1.5 12/.5 13/1 10/1 | 8/4 |"
        " 8/1 9/.5 10/.5 12/2 | 12/1 10/1 8/1 9/1 | 11/2 9/1 8/1 | 7/4",
        "10/2 12/1 14/1 | 13/3 12/1 | 11/2 9/1 11/1 | 14/4 | 12/2 10/1 12/1 | 10/3 8/1 | 9/1 8/.5 9/.5 11/2 | 7/4",
        "maqsum", "metal", "deserto", semente=904, brilho=4200)
    F["reg-templo"] = Faixa("reg-templo", 132, 57, "insen", 57, {
        "Abertura": "i i bII bII i i bII bII",
        "Tema": "i bII iv i bVI bII i i iv bVI i bII iv bII i i",
        "Ação": "i bII i bII iv bII i i bVI bII iv i bVI bII bII bII",
        "Respiro": "iv i bVI i iv i bII i",
        "Hino": "bVI bII iv i bVI bII i i",
        "Volta": "i bII i bII i bII bII bII"},
        "10/3 9/.5 8/.5 | 7/2 6/2 | 9/1 10/1 12/2 | 10/4 |"
        " 9/2 10/1 9/1 | 11/2 9/1 7/1 | 8/2 10/2 | 10/4 |"
        " 12/3 10/1 | 9/2 10/2 | 8/1 7/1 5/2 | 6/2 7/2 |"
        " 7/1 9/1 10/2 | 11/3 9/1 | 8/2 10/2 | 5/4",
        "9/2 10/2 | 11/3 12/1 | 12/2 10/2 | 8/4 | 10/1 9/1 10/2 | 11/2 9/2 | 8/2 10/2 | 10/4",
        "meio", "koto", "templo", semente=905, brilho=3600)
    F["reg-vulcao"] = Faixa("reg-vulcao", 176, 64, "frigio", 64, {
        "Abertura": "i i bII bII i i bvii bII",
        "Tema": "i bII i bvii i bII bVI bvii iv bVI bvii i iv bII i i",
        "Ação": "i bII i bII i bII bvii bII bVI bvii i i bVI bvii bII bII",
        "Respiro": "bVI bIII bvii i bVI bIII bII bII",
        "Hino": "bVI bvii i i bVI bvii bII bII",
        "Volta": "i bII i bII i bII bII bII"},
        "7/1 9/.5 11/.5 14/2 | 12/1 10/1 8/2 | 9/1 11/1 9/1 7/1 | 8/1 10/1 13/2 |"
        " 11/1 9/.5 11/.5 14/2 | 12/1 13/.5 12/.5 10/2 | 12/1 11/1 9/2 | 13/2 10/2 |"
        " 10/1 12/1 14/2 | 12/1.5 11/.5 9/2 | 13/1 12/1 10/1 8/1 | 7/4 |"
        " 10/1 12/1 10/1 7/1 | 8/2 10/1 12/1 | 11/2 9/2 | 7/4",
        "12/2 9/1 12/1 | 13/3 10/1 | 11/2 14/2 | 14/4 | 14/2 12/1 11/1 | 13/2 10/2 | 12/2 10/1 8/1 | 8/4",
        "metal", "ambos", "vulcao", acao="metal", semente=906, brilho=5400)
    F["reg-ceu"] = Faixa("reg-ceu", 152, 56, "lidio", 56, {
        "Abertura": "I II I II I II V V",
        "Tema": "I II vi V I II iii V vi II I V vi II V V",
        "Ação": "I II I II vi iii II V I II vi V vi II V V",
        "Respiro": "vi iii II I vi iii II V",
        "Hino": "II V vi I II V I I",
        "Volta": "I II I II I II V V"},
        "11/2 14/1 16/1 | 15/2 12/1 10/1 | 12/1 14/1 16/2 | 15/3 13/1 |"
        " 11/2 14/1 16/1 | 17/2 15/1 12/1 | 16/1 13/1 11/2 | 13/3 15/1 |"
        " 16/1.5 14/.5 12/2 | 15/1 17/1 15/2 | 14/2 11/1 9/1 | 13/2 15/2 |"
        " 12/1 14/1 16/2 | 17/1.5 15/.5 12/2 | 15/2 13/1 11/1 | 15/4",
        "12/2 15/2 | 13/3 11/1 | 14/2 16/2 | 16/3 14/1 | 17/2 15/1 17/1 | 18/2 15/2 | 16/2 14/2 | 14/4",
        "galope", "ambos", "ceu", semente=907, brilho=6600)
    F["reg-trono"] = Faixa("reg-trono", 168, 59, "harmonica", 59, {
        "Abertura": "i i VI VI iv iv V V",
        "Tema": "i iv V i VI iv V V i VI iv V VI iv V i",
        "Ação": "i VI iv V i VI iv V VI bIII iv V VI iv V V",
        "Respiro": "VI bIII iv i VI bIII V V",
        "Hino": "VI bIII iv i VI V i i",
        "Volta": "i VI iv V i VI V V"},
        "11/1 14/1 16/1.5 15/.5 | 14/2 12/1 10/1 | 13/1 11/1 8/2 | 9/3 7/1 |"
        " 12/1 14/1 16/2 | 14/1.5 12/.5 10/2 | 11/2 13/1 15/1 | 15/4 |"
        " 16/2 14/1 11/1 | 12/1 14/1 16/2 | 14/1 12/1 10/2 | 13/1 11/1 8/2 |"
        " 12/2 14/2 | 14/1 12/1 10/1 12/1 | 11/2 13/2 | 14/4",
        "14/2 16/2 | 16/2 13b/1 11/1 | 14/2 12/1 10/1 | 11/4 | 16/1 14/1 12/2 | 13/2 15/2 | 16/2 14/2 | 14/4",
        "galope", "ambos", "trono", semente=908, brilho=5800)
    # ------------------------------------------------ CHEFES
    F["chefe-vila"] = Faixa("chefe-vila", 160, 53, "menor", 53, {
        "Abertura": "i i VI VI iv iv V V",
        "Tema": "i VI III VII i VI iv V VI VII i i iv V i i",
        "Ação": "i VII VI V i VII VI V iv VI VII V iv VI V V",
        "Respiro": "VI III VII i VI III iv V",
        "Hino": "VI VII i i VI VII V V",
        "Volta": "i VII VI V i VII V V"},
        "11/.75 11/.25 14/1 16/1.5 14/.5 | 12/2 14/1 16/1 | 16/1.5 15/.5 13/2 | 13/1 15/1 17/2 |"
        " 11/.75 11/.25 14/1 16/1.5 18/.5 | 19/2 16/2 | 17/1 16/1 14/2 | 15/2 13#/1 11/1 |"
        " 12/1 14/1 16/2 | 17/1.5 15/.5 13/2 | 14/1 16/1 18/2 | 18/4 |"
        " 17/2 14/2 | 15/1 13#/1 11/2 | 14/2 11/2 | 14/4",
        "16/2 14/1 12/1 | 13/3 15/1 | 14/2 16/2 | 18/4 | 19/2 16/2 | 17/2 15/2 | 15/2 13#/1 15/1 | 18/4",
        "galope", "ambos", "fanfarra", semente=911, brilho=5600)
    F["chefe-floresta"] = Faixa("chefe-floresta", 148, 50, "harmonica", 50, {
        "Abertura": "i i bII bII i i V V",
        "Tema": "i bII i V i iv V V VI bII i V iv V i i",
        "Ação": "i bII V i i bII V i iv VI bII V iv bII V V",
        "Respiro": "VI iv bII V VI iv V V",
        "Hino": "VI bII V i VI iv V V",
        "Volta": "i bII i V i bII V V"},
        "18/1 17/.5 16/.5 16/1 14/1 | 15b/2 17/1 19/1 | 18/1 19/.5 18/.5 16/1 14/1 | 13/2 15/1 18/1 |"
        " 21/1 20/.5 19/.5 18/1 16/1 | 17/2 19/1 21/1 | 20/2 18/1 15/1 | 18/4 |"
        " 19/1 18/1 16/2 | 17/1 15b/1 12/2 | 14/1 16/1 18/2 | 20/1 18/1 15/2 |"
        " 17/1 19/1 21/2 | 20/2 18/2 | 16/2 14/2 | 14/4",
        "16/2 19/2 | 17/3 15b/1 | 15/2 18/1 20/1 | 21/4 | 21/2 19/1 16/1 | 17/2 19/2 | 20/1 18/1 15/1 13/1 | 18/4",
        "galope", "serpente", "veneno", semente=912, brilho=5000)
    F["chefe-neon"] = Faixa("chefe-neon", 160, 48, "menor", 48, {
        "Abertura": "i i iv iv VI VI V V",
        "Tema": "i VI iv V i VI III VII iv VI V V iv V i i",
        "Ação": "i III VII iv i III VII iv VI VII i i VI VII V V",
        "Respiro": "VI III iv i VI III iv V",
        "Hino": "VI VII i i VI VII V V",
        "Volta": "i VI VII V i VI V V"},
        "14/.75 14/.25 18/1 21/1.5 18/.5 | 19/1.5 21/.5 16/2 | 17/1 19/1 21/2 | 18/2 20#/1 22/1 |"
        " 14/.75 14/.25 18/1 21/2 | 19/1 21/1 23/2 | 20/1 18/1 16/2 | 17/2 15/2 |"
        " 17/1 19/1 21/1 19/1 | 16/2 21/2 | 22/1 20#/1 18/2 | 18/4 |"
        " 21/1.5 19/.5 17/2 | 18/1 20#/1 22/2 | 21/4 | r/4",
        "16/2 19/2 | 20/2 17/2 | 18/2 21/2 | 21/4 | 23/2 21/1 19/1 | 22/2 20/2 | 20#/2 22/2 | 18/4",
        "bigorna", "metal", "aco", semente=913, brilho=5200)
    F["chefe-deserto"] = Faixa("chefe-deserto", 132, 54, "hijaz", 54, {
        "Abertura": "I I bII bII I I bvii I",
        "Tema": "I bII I I bvii bII I I iv iv bII bII bvii bII I I",
        "Ação": "I bII I bII iv bII I I iv bvii bII I iv bvii bII bII",
        "Respiro": "iv I bII I iv I bII I",
        "Hino": "iv bII I I bvii bII I I",
        "Volta": "I bII I bII I bII bII I"},
        "14/.5 15/.25 14/.25 13/.5 14/.5 16/2 | 15/1 17/1 19/2 | 18/1 16/.5 15/.5 16/1 14/1 | 14/4 |"
        " 13/1 15/1 17/2 | 19/1 17/.5 15/.5 15/1 12/1 | 11/1 12/.25 11/.25 9/.5 9/1 7/1 | 7/4 |"
        " 10/1 12/1 14/2 | 17/1 14/1 12/2 | 15/2 17/1 19/1 | 19/4 |"
        " 17/1.5 15/.5 13/2 | 15/1 17/1 15/1 12/1 | 16/1 15/.5 16/.5 18/2 | 14/4",
        "17/2 14/1 12/1 | 15/3 17/1 | 16/2 18/2 | 18/4 | 17/2 15/1 13/1 | 19/2 17/2 | 16/1 15/.5 16/.5 14/2 | 14/4",
        "maqsum", "metal", "genio", semente=914, brilho=4800)
    F["chefe-templo"] = Faixa("chefe-templo", 144, 56, "harmonica", 56, {
        "Abertura": "i i i i VI VI V V",
        "Tema": "i iv i V VI iv V V i bII i V VI iv V i",
        "Ação": "i bII i bII VI iv V V i bII VI V iv bII V V",
        "Respiro": "i iv VI V i iv bII V",
        "Hino": "VI iv i i VI bII V V",
        "Volta": "i bII i V i bII V V"},
        "11/1 14/1 16/1 14/1 | 12/2 10/1 7/1 | 11/1 9/1 7/1 9/1 | 13/3 11/1 |"
        " 12/1 14/1 16/2 | 17/2 14/1 12/1 | 15/1 13/1 11/2 | 11/4 |"
        " 14/1 16/1 14/1 11/1 | 15b/2 12/2 | 11/1 14/1 16/2 | 15/1 13/1 11/2 |"
        " 16/2 14/2 | 12/1 14/1 17/2 | 15/2 13/2 | 14/4",
        "16/2 14/2 | 17/3 14/1 | 16/2 14/1 11/1 | 14/4 | 12/1 14/1 16/2 | 15b/2 17/2 | 15/2 13/1 15/1 | 11/4",
        "meio", "metal", "assombro", acao="metal", semente=915, brilho=4400)
    F["chefe-vulcao"] = Faixa("chefe-vulcao", 184, 49, "frigio", 49, {
        "Abertura": "i i bII bII i i bvii bII",
        "Tema": "i bII i bvii i bII bVI bvii iv bVI bvii i iv bII i i",
        "Ação": "i bII i bII i bII bvii bII bVI bvii i i bVI bvii bII bII",
        "Respiro": "bVI bIII bvii i bVI bIII bII bII",
        "Hino": "bVI bvii i i bVI bvii bII bII",
        "Volta": "i bII i bII i bII bII bII"},
        "14/1 16/1 18/2 | 19/1 17/1 15/2 | 16/1 14/1 11/2 | 13/1 15/1 17/2 |"
        " 18/1 21/1 18/1 16/1 | 19/1.5 17/.5 15/2 | 19/1 21/1 23/2 | 20/2 17/2 |"
        " 17/1 19/1 21/2 | 21/1 19/1 16/2 | 20/1 17/1 15/2 | 14/4 |"
        " 17/2 21/2 | 19/2 15/2 | 16/2 18/2 | 21/4",
        "19/2 21/2 | 20/3 17/1 | 18/2 21/2 | 21/4 | 23/2 21/1 19/1 | 22/2 20/2 | 19/2 17/1 15/1 | 15/4",
        "metal", "ambos", "magma", acao="metal", semente=916, brilho=5200)
    F["chefe-ceu"] = Faixa("chefe-ceu", 158, 51, "maior", 51, {
        "Abertura": "I I IV IV vi vi V V",
        "Tema": "I V vi IV I V bVII IV vi iii IV I ii IV V V",
        "Ação": "I bVII IV I I bVII IV I vi IV bVII V vi IV V V",
        "Respiro": "IV I vi V IV I ii V",
        "Hino": "IV V iii vi IV V I I",
        "Volta": "I bVII IV I I bVII V V"},
        "14/1 16/.5 18/.5 18/2 | 18/1.5 17/.5 15/2 | 16/1 19/1 21/2 | 19/3 17/1 |"
        " 14/1 16/.5 18/.5 21/2 | 20/2 18/1 15/1 | 17/2 20b/2 | 19/4 |"
        " 16/1 19/1 16/1 14/1 | 16/2 18/2 | 17/1 19/1 21/2 | 18/4 |"
        " 15/1 17/1 19/2 | 21/2 19/2 | 20/2 18/1 15/1 | 18/4",
        "17/2 19/2 | 18/3 20/1 | 20/2 18/2 | 19/4 | 21/2 19/1 17/1 | 18/2 15/2 | 16/2 18/2 | 21/4",
        "galope", "ambos", "olimpo", semente=917, brilho=6200)
    F["chefe-trono"] = Faixa("chefe-trono", 176, 45, "harmonica", 45, {
        "Abertura": "i i VI VI bII bII V V",
        "Tema": "i iv V i VI bII V V i VI iv V VI bII V i",
        "Ação": "i VI bII V i VI bII V iv VI bII V iv bII V V",
        "Respiro": "VI bIII iv i VI bIII bII V",
        "Hino": "VI bII i i VI bII V V",
        "Volta": "i bII i V i bII V V"},
        "21/1 20/1 21/1 18/1 | 19/1 21/1 24/2 | 22/1 20/1 18/2 | 21/4 |"
        " 23/1.5 21/.5 19/2 | 22b/2 24/1 22b/1 | 20/2 22/1 25/1 | 22/4 |"
        " 18/1 21/1 23/2 | 23/1 21/1 19/2 | 17/1 19/1 21/1 24/1 | 22/2 20/2 |"
        " 19/1 21/1 23/2 | 22b/1 21/1 19/1 17/1 | 20/2 18/2 | 21/4",
        "21/2 23/2 | 22b/3 24/1 | 23/2 21/2 | 25/4 | 23/2 21/1 19/1 | 22b/2 24/2 | 22/2 20/1 22/1 | 22/4",
        "galope", "ambos", "imperador", semente=918, brilho=5600)
    return F


# ================================================================== o arranjo
GALOPE = ((0, 2), (2, 1), (3, 1))
RIFF = ((0, 2), (3, 1), (4, 2), (6, 2), (8, 3), (11, 1), (12, 2), (14, 2))


def toca(m, f, frase, t0, forte=1.0, transp=0, dobra=None, ganho_dobra=0.42, terca=False, voz=None):
    """A melodia na voz da faixa (e, se pedido, dobrada uma oitava acima ou com a terça abaixo nos metais)."""
    voz = voz or f.voz
    for ini, dur, n in frase:
        n += transp
        em, d = t0 + ini * m.BEAT, dur * m.BEAT * 0.94
        if voz in ("saw", "ambos", "serpente"):
            m.poe(m.tema_eco, supersaw(n, d, forte, f.brilho, voz != "saw" or dur >= 1), em)
        if voz in ("metal", "ambos"):
            m.poe(m.tema, metais([n - 12], d, forte * (0.75 if voz == "ambos" else 1.05)), em)
        if voz == "metal":
            m.poe(m.tema_eco, supersaw(n, d, forte * 0.45, f.brilho * 0.8), em)
        if voz == "sino":
            m.poe(m.tema_eco, pan(v4.sino(n, 0.95 * forte), 0.12), em)
            m.poe(m.tema_eco, supersaw(n, d, 0.55 * forte, f.brilho, True), em)
        if voz == "coro":
            m.poe(m.tema, coro([n], d, 0.95 * forte), em)
            m.poe(m.tema_eco, supersaw(n - 12, d, 0.5 * forte, f.brilho * 0.8, True), em)   # a flauta grave junto
        if voz == "koto":
            m.poe(m.tema_eco, pan(faisca(n, 0.9 * forte), -0.1), em)
            m.poe(m.tema_eco, pan(faisca(n + 12, 0.35 * forte), 0.2), em + 0.012)
            if dur >= 2:
                m.poe(m.tema_eco, supersaw(n, d, 0.42 * forte, f.brilho * 0.7, True), em + m.BEAT * 0.25)
        if voz == "caixinha":
            m.poe(m.tema_eco, pan(v4.sino(n + 12, 0.75 * forte), 0.25), em)
            m.poe(m.tema_eco, pan(v4.sino(n + 12.15, 0.4 * forte), -0.25), em + 0.006)   # desafinada: a caixinha velha
            m.poe(m.tema_eco, supersaw(n, d, 0.6 * forte, f.brilho, True), em)
        if voz == "serpente":
            m.poe(m.tema_eco, pan(faisca(n + 12, 0.45 * forte), 0.3), em)
        if dobra is not None:
            m.poe(m.tema_eco, supersaw(n + dobra, d, forte * ganho_dobra, f.brilho * 0.8, False), em)
        if terca:
            m.poe(m.tema, metais([abaixo_terca(f, n) - 12], d, forte * 0.55), em)


def abaixo_terca(f, n):
    """A nota da escala uma terça abaixo (a segunda voz do refrão)."""
    esc = sorted({(f.tonica + i) % 12 for i in ESCALAS[f.escala]})
    menores = [k for k in range(n - 5, n) if k % 12 in esc]
    return menores[-2] if len(menores) >= 2 else n - 3


def faz(f):
    prog = f.lista()
    m = Musica(f.nome, f.bpm, prog, f.acordes(), [(s, INICIO[s]) for s, _ in SECOES], laco=8, semente=f.semente)
    assert m.compassos == 72
    S16, BAR, BEAT = m.S16, m.BAR, m.BEAT
    tema, hino = melodia(f.tema_txt, f.base, f.escala), melodia(f.hino_txt, f.base, f.escala)
    pesado = f.groove in ("metal", "galope", "bigorna") or f.chefe

    for b in range(m.compassos):
        sec, local = m.secao(b)
        t0 = m.t(b)
        raiz, notas = m.acorde(b)
        pc = power(raiz + 12 if raiz < 40 else raiz)
        refrao = sec == "Refrão"

        # ================================================ ABERTURA: a assinatura de cada lugar
        if sec == "Abertura":
            a = f.abertura
            m.poe(m.base_sala, pad(notas, BAR, 0.5 + 0.06 * local, 900 + 280 * local), t0)
            if a in ("caixinha", "assombro"):
                arp = [notas[0] + 24, notas[1] + 24, notas[2] + 24, notas[1] + 36, notas[2] + 24, notas[1] + 24]
                for k in range(8):
                    m.poe(m.tema_eco, pan(v4.sino(arp[k % 6] + (0.2 if a == "assombro" and k % 2 else 0), 0.5 + 0.04 * local), 0.35 * (1 if k % 2 else -1)), t0 + k * BEAT / 2)
                if a == "assombro":
                    for k in range(4):                                            # batida de coração
                        m.poe(m.base, taiko(0.5 + 0.06 * local), t0 + k * BEAT)
                        m.poe(m.base, taiko(0.3 + 0.05 * local), t0 + k * BEAT + S16 * 1.5)
                    if local in (3, 7):
                        m.poe(m.base, m.IMPACTO, t0 + BEAT * 3, 1.2)
                else:
                    for k in range(4):
                        m.poe(m.pulso, m.CHIMBAL, t0 + k * BEAT + BEAT / 2, 0.35 + 0.05 * local)
                    if local >= 4:
                        for k in range(8):
                            m.poe(m.pulso, pan(cordas(notas[k % 3] + 12, S16 * 1.2, 0.8), 0.3 * (1 if k % 2 else -1)), t0 + k * BEAT / 2)
            elif a in ("floresta",):
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.4 + 0.07 * local), t0)
                for k in range(3):                                                # pássaros
                    m.poe(m.tema_eco, pan(faisca(notas[(k + local) % 3] + 36, 0.35), 0.6 * (1 if (k + local) % 2 else -1)), t0 + (k * 5 + local % 3) * S16)
                for p, fz in ((0, 0.8), (3, 0.5), (6, 0.6), (8, 0.8), (11, 0.5), (14, 0.6)):
                    m.poe(m.base, taiko(fz * (0.6 + 0.05 * local)), t0 + p * S16)
            elif a == "neon":
                passos = 8 if local < 4 else 16
                seq = [notas[0] + 12, notas[1] + 12, notas[2] + 12, notas[1] + 24]
                for k in range(passos):
                    m.poe(m.pulso_eco, pan(faisca(seq[k % 4], 0.35 + 0.07 * local), 0.3 * (1 if k % 2 else -1)), t0 + k * BAR / passos)
                if local >= 4:
                    m.bat([0, 4, 8, 12], m.BUMBO, m.base, t0, 0.6 + 0.08 * (local - 4))
            elif a in ("deserto", "genio"):
                m.poe(m.base, baixo(raiz, BAR * 0.98, 0.7), t0)
                for p, fz, grave in ((0, 1.0, True), (3, 0.6, False), (6, 0.7, False), (8, 0.9, True), (12, 0.7, False)):
                    m.poe(m.base, taiko(fz * 0.7) if grave else tom(64, 0.5 * fz), t0 + p * S16)
                alaude = [notas[0] + 12, notas[0] + 13, notas[1] + 12, notas[0] + 12]
                for k in range(4):
                    m.poe(m.tema_eco, pan(faisca(alaude[k], 0.55 + 0.05 * local), -0.2), t0 + (k * 3 + 2) * S16)
                if a == "genio" and local in (3, 7):
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.5, 1.2), t0 + BEAT * 2)
            elif a == "templo":
                if local in (0, 4):
                    m.poe(m.base_sala, pan(sino_grande(raiz + 12, 0.9), -0.2), t0)
                for k in range(6):
                    m.poe(m.tema_eco, pan(faisca([notas[0], notas[2], notas[1]][k % 3] + 24, 0.4 + 0.05 * local), 0.3 * (1 if k % 2 else -1)), t0 + k * BEAT * 2 / 3)
                if local >= 2:
                    for p in ((0, 6, 10) if local < 6 else (0, 3, 6, 8, 10, 12, 14)):
                        m.poe(m.base, taiko(0.55 + 0.06 * local), t0 + p * S16)
            elif a in ("vulcao", "magma"):
                m.poe(m.base, timpano(raiz, 0.6 + 0.07 * local), t0)
                for k in range(4 if local < 4 else 8):
                    m.poe(m.base, taiko(0.45 + 0.07 * local), t0 + k * BAR / (4 if local < 4 else 8))
                if local >= 4:
                    for k in range(8):
                        m.poe(m.pulso, guitarra(pc, S16 * 0.8, 0.6 + 0.08 * (local - 4), abafada=True), t0 + k * BEAT / 2)
                if local in (0, 4) and a == "magma":
                    m.poe(m.tema, coro([n + 12 for n in notas], BAR * 2, 0.8), t0)
            elif a in ("ceu", "olimpo"):
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.45 + 0.07 * local), t0)
                harpa = sorted({n + 12 for n in notas} | {n + 24 for n in notas})
                for k, n in enumerate(harpa + harpa[::-1][1:-1]):
                    m.poe(m.tema_eco, pan(faisca(n, 0.4), -0.3 + 0.1 * k), t0 + k * S16)
                if local in (0, 4):
                    m.poe(m.base_sala, pan(sino_grande(raiz + 24, 0.55), 0.2), t0)
                if a == "olimpo" and local in (3, 5, 7):
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.5, 1.25), t0)
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.3, 1.15), t0 + BEAT * 2)
            elif a in ("trono", "imperador"):
                m.poe(m.tema, coro([n + 12 for n in notas] + [notas[0]], BAR, 0.5 + 0.07 * local), t0)
                m.poe(m.base_sala, pad([n + 12 for n in notas], BAR, 0.55, 3200), t0)      # o órgão
                if local % 2 == 0:
                    m.poe(m.base_sala, pan(sino_grande(raiz, 0.9), -0.15), t0)
                    m.poe(m.base, timpano(raiz, 1.1), t0)
                    m.poe(m.base, m.IMPACTO, t0, 0.9)
                if a == "imperador" and local in (3, 5):
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.6, 1.3), t0)
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.4, 1.1), t0 + BEAT * 2.5)
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.2, 1.2), t0 + BEAT * 3)
            elif a == "heroica":
                if local in (0, 4):
                    m.poe(m.base, timpano(raiz, 1.0), t0)
                    m.poe(m.base, m.IMPACTO, t0, 0.9)
                m.bat([0, 8] if local < 2 else [0, 3, 6, 8, 11, 14] if local < 6 else range(16), m.BUMBO_F, m.base, t0, 0.7 + 0.04 * local)
                if local >= 2:
                    m.bat([4, 12], m.CAIXA_F, m.base_sala, t0, 0.8)
                    for k in range(16):
                        aberto = k in (0, 6, 10)
                        m.poe(m.pulso, guitarra(pc, S16 * (2.6 if aberto else 0.7), (0.8 if aberto else 0.6) + 0.04 * local, abafada=not aberto), t0 + k * S16)
                if local % 2 == 1:
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.4, 1.1), t0)
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.4, 1.05), t0 + BEAT * 0.75)
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 2, 1.2), t0 + BEAT)
            elif a == "fanfarra":
                if local % 2 == 1:
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.4, 1.15), t0)
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 0.4, 1.1), t0 + BEAT * 0.75)
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 2, 1.25), t0 + BEAT)
                m.poe(m.base, m.rufo(1, 0.15 + 0.08 * local), t0)
                if local in (0, 4):
                    m.poe(m.base, timpano(raiz, 1.0), t0)
            elif a == "veneno":
                cromatico = [notas[0] + 24, notas[0] + 25, notas[0] + 24, notas[0] + 23]
                for k in range(8):
                    m.poe(m.tema_eco, pan(faisca(cromatico[k % 4], 0.45 + 0.05 * local), 0.4 * (1 if k % 2 else -1)), t0 + k * BEAT / 2)
                m.poe(m.tema, coro([notas[0] + 12, notas[0] + 13], BAR, 0.3 + 0.05 * local), t0)
                if local in (2, 6):
                    m.poe(m.base, riser(BAR * 2, 0.9), t0)
            elif a == "aco":
                for k in range(4):                                                # a bigorna
                    m.poe(m.pulso, tom(76, 0.6 + 0.05 * local), t0 + k * BEAT + BEAT / 2)
                    m.poe(m.base, m.BUMBO_F, t0 + k * BEAT, 0.6 + 0.05 * local)
                if local % 2 == 1:
                    m.poe(m.tema, metais([n + 12 for n in notas], BEAT * 1.5, 1.2), t0)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.15), t0)
                m.poe(m.base, riser(BAR * 2, 1.2), t0)
            if local == 7:
                m.poe(m.pulso, guitarra(pc, BAR * 0.9, 0.85), t0)
            continue

        # ================================================ pad e coro
        if sec == "Respiro":
            m.poe(m.base_sala, pad(notas, BAR, 0.9, 2000), t0)
            m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.9 if pesado else 0.75), t0)
        elif sec in ("Hino", "Refrão"):
            m.poe(m.base_sala, pad(notas, BAR, 0.6, 3300), t0)
            m.poe(m.tema, coro([n + 12 for n in notas] + [notas[0] + 24], BAR, 0.95 if sec == "Hino" else 1.1), t0)
        else:
            m.poe(m.base_sala, pad(notas, BAR, 0.45, 2600), t0)
            if sec == "Tema" and f.voz in ("coro", "ambos"):
                m.poe(m.tema, coro([n + 12 for n in notas], BAR, 0.45), t0)

        # ================================================ cordas correndo (o motor das faixas de batalha)
        if sec in ("Tema", "Ação", "Volta") or refrao:
            if f.groove not in ("quatro", "meio") or sec != "Tema":
                seq = [notas[0] + 12, notas[1] + 12, notas[2] + 12, notas[1] + 24, notas[2] + 12, notas[0] + 24, notas[1] + 12, notas[2] + 12]
                for k in range(16):
                    m.poe(m.base, pan(cordas(seq[k % 8], S16 * 0.8, (0.85 if pesado else 0.65) + 0.15 * (k % 4 == 0)), 0.3 * (1 if k % 2 else -1)), t0 + k * S16)

        # ================================================ baixo
        if sec == "Respiro":
            for p, d in ((0, 6), (6, 4), (10, 6)):
                m.poe(m.base, baixo(raiz, S16 * d * 0.9, 0.9), t0 + p * S16)
        elif sec == "Ação" and f.acao in ("riff", "metal"):
            for k in range(16):
                m.poe(m.base, baixo(raiz + (12 if k in (6, 14) else 0), S16 * 0.8, 1.05 if k in (0, 3, 6, 10, 13) else 0.82), t0 + k * S16)
        elif sec in ("Hino", "Refrão"):
            for k in range(8):
                m.poe(m.base, baixo(raiz + (12 if k in (3, 7) else 0), BEAT * 0.42, 1.0 + 0.1 * (k % 2 == 0)), t0 + k * BEAT / 2)
        elif f.groove == "marcha":
            for k in range(8):
                m.poe(m.base, baixo(raiz + (7 if k % 2 else 0) + (12 if k in (3, 7) else 0), BEAT * 0.4, 1.0 if k % 2 == 0 else 0.85), t0 + k * BEAT / 2)
        elif f.groove == "quatro":
            for k in range(16):
                m.poe(m.base, baixo(raiz + (12 if k % 2 else 0), S16 * 0.7, 1.0 if k % 4 == 0 else 0.8), t0 + k * S16)
        elif f.groove == "tribal":
            for p, d in ((0, 3), (3, 3), (6, 2), (10, 2), (12, 4)):
                m.poe(m.base, baixo(raiz + (12 if p == 12 else 0), S16 * d * 0.85, 1.0), t0 + p * S16)
        elif f.groove in ("maqsum", "meio"):
            m.poe(m.base, baixo(raiz, BEAT * 1.4, 0.95), t0)
            for p in (6, 10, 14):
                m.poe(m.base, baixo(raiz + (12 if p == 10 else 0), S16 * 1.6, 0.9), t0 + p * S16)
        elif f.groove == "metal" or f.groove == "bigorna":
            for k in range(16):
                m.poe(m.base, baixo(raiz, S16 * 0.8, 1.08 if k % 4 == 0 else 0.86), t0 + k * S16)
        else:  # galope
            for beat in range(4):
                for p, d in GALOPE:
                    m.poe(m.base, baixo(raiz + (12 if beat == 3 and p == 0 else 0), S16 * d * 0.85, 1.0), t0 + (beat * 4 + p) * S16)

        # ================================================ guitarras e acompanhamento (pulso)
        if sec == "Respiro":
            if local >= 6:
                m.poe(m.pulso, guitarra(pc, BAR * 0.95, 0.6 + 0.3 * (local - 6)), t0)
        elif sec in ("Hino", "Refrão"):
            for pos, dur in ((0, 3), (3, 3), (6, 4), (10, 2), (12, 4)):
                m.poe(m.pulso, guitarra(pc, dur * S16 * 0.9, 1.0 if pesado else 0.8), t0 + pos * S16)
        elif sec == "Ação" and f.acao == "arpejo":
            seq = [notas[0] + 12, notas[1] + 12, notas[2] + 12, notas[1] + 24, notas[2] + 12, notas[0] + 24, notas[2] + 24, notas[1] + 24]
            for k in range(16):
                m.poe(m.pulso_eco, pan(faisca(seq[k % 8], 0.6 + 0.15 * (k % 4 == 0)), 0.3 * (1 if k % 2 else -1)), t0 + k * S16)
            for pos, dur in ((0, 3), (3, 3), (6, 4), (10, 2), (12, 4)):
                m.poe(m.pulso, guitarra(pc, dur * S16 * 0.9, 0.7), t0 + pos * S16)
        elif sec == "Ação" or (sec == "Volta" and local < 6):
            for k in range(16):                                                   # o riff: acentos 3+3+3+3+2+2
                aberto = k in (0, 3, 6, 9, 12, 14)
                m.poe(m.pulso, guitarra(pc, S16 * (2.6 if aberto else 0.7), 1.0 if aberto else 0.76, abafada=not aberto), t0 + k * S16)
        elif sec == "Volta":
            passo = BEAT / 2 if local == 6 else S16
            for k in range(int(BAR / passo)):
                m.poe(m.pulso, guitarra(pc, passo * 0.5, 0.75 + 0.15 * (local - 6), abafada=True), t0 + k * passo)
        elif f.groove == "marcha":
            for k in range(4):
                m.poe(m.pulso, guitarra(pc, BEAT * 0.35, 0.65, abafada=True), t0 + k * BEAT + BEAT / 2)
            for k in range(8):
                m.poe(m.pulso, pan(cordas([notas[0], notas[2], notas[1], notas[2]][k % 4] + 12, S16 * 1.2, 0.9), 0.25 * (1 if k % 2 else -1)), t0 + k * BEAT / 2)
        elif f.groove == "tribal":
            seq = [notas[0] + 12, notas[2] + 12, notas[1] + 24, notas[2] + 12]
            for k in range(8):
                m.poe(m.pulso, pan(cordas(seq[k % 4], S16 * 1.2, 0.9 + 0.15 * (k % 2 == 0)), 0.25 * (1 if k % 2 else -1)), t0 + k * BEAT / 2)
            for k in range(16):
                aberto = k in (0, 3, 6, 8, 11, 14)
                m.poe(m.pulso, guitarra(pc, S16 * (2.6 if aberto else 0.7), 0.95 if aberto else 0.72, abafada=not aberto), t0 + k * S16)
        elif f.groove == "quatro":
            seq = [notas[0] + 12, notas[1] + 12, notas[2] + 12, notas[1] + 24, notas[2] + 12, notas[0] + 24, notas[2] + 24, notas[1] + 24]
            for k in range(16):
                m.poe(m.pulso_eco, pan(faisca(seq[k % 8], 0.55 + 0.15 * (k % 4 == 0)), 0.3 * (1 if k % 2 else -1)), t0 + k * S16)
            for k in (2, 6, 10, 14):                                              # o pad cortado, no contratempo
                m.poe(m.pulso, pad([n + 12 for n in notas], S16 * 1.6, 1.6, 4200), t0 + k * S16)
        elif f.groove in ("maqsum", "meio"):
            alaude = [notas[0] + 12, notas[2] + 12, notas[1] + 12, notas[0] + 24]
            for k, p in enumerate((0, 3, 6, 8, 11, 14)):
                m.poe(m.pulso, pan(faisca(alaude[k % 4], 0.7), -0.25), t0 + p * S16)
            for k in range(16):                                                   # as guitarras de batalha por baixo do sabor
                aberto = k in (0, 6, 10)
                m.poe(m.pulso, guitarra(pc, S16 * (2.6 if aberto else 0.7), (0.95 if aberto else 0.7) * (1.1 if f.chefe else 1), abafada=not aberto), t0 + k * S16)
        elif f.groove in ("metal", "bigorna"):
            for k in range(16):
                aberto = k in (0, 3, 6, 8, 11, 14)
                m.poe(m.pulso, guitarra(pc, S16 * (2.6 if aberto else 0.7), 1.05 if aberto else 0.8, abafada=not aberto), t0 + k * S16)
        else:  # galope
            for beat in range(4):
                for p, d in GALOPE:
                    aberto = beat == 0 and p == 0
                    m.poe(m.pulso, guitarra(pc, S16 * d * (2.5 if aberto else 0.8), 1.0 if aberto else 0.85, abafada=not aberto), t0 + (beat * 4 + p) * S16)

        # ================================================ bateria
        if sec == "Respiro":
            m.bat([0, 10], m.BUMBO, m.base, t0)
            m.bat([8], m.CAIXA, m.base_sala, t0)
            m.bat(range(0, 16, 4), m.CHIMBAL, m.pulso, t0)
            if local in (0, 4):
                m.poe(m.base, m.IMPACTO, t0, 0.85)
                m.poe(m.pulso, m.PRATO, t0, 0.7)
                m.poe(m.base_sala, pan(sino_grande(notas[0] + 12, 0.6), -0.2), t0)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.2), t0)
                m.poe(m.base, riser(BAR * 2, 1.3), t0)
        elif sec in ("Hino", "Refrão"):
            if sec == "Hino":
                m.bat([0, 3, 6, 8, 11, 14], m.BUMBO_F, m.base, t0)
            else:
                m.bat(range(16) if pesado else [0, 2, 3, 6, 8, 10, 11, 14], m.BUMBO_F, m.base, t0)
            m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
            for k in range(0, 16, 2):
                m.poe(m.pulso, m.CONDUCAO if refrao else m.CHIMBAL_ABERTO, t0 + k * S16)
            if local % (2 if refrao else 4) == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 1.2)
                m.poe(m.base, timpano(raiz, 1.0), t0)
            if sec == "Hino" and local == 7:                                      # a subida para o refrão
                m.poe(m.base, riser(BAR, 1.3), t0)
                m.virada_de_tons(t0, [59, 57, 55, 52, 50, 47, 45, 44])
        elif sec == "Ação" or (sec == "Volta" and local < 6):
            if f.acao == "arpejo":
                m.bat([0, 4, 8, 12], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(16):
                    m.poe(m.pulso, m.CHIMBAL_ABERTO if k % 4 == 2 else m.CHIMBAL, t0 + k * S16, 0.85 if k % 4 == 2 else 0.5)
            elif f.acao == "metal":
                m.bat(range(16), m.BUMBO_F if local >= 8 else m.BUMBO, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(0, 16, 2):
                    m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            else:
                m.bat([0, 3, 6, 9, 12, 14], m.BUMBO_F, m.base, t0)
                m.bat([4, 12] if local < 8 else [4, 10, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(16):
                    m.poe(m.pulso, m.CHIMBAL_F if k % 2 == 0 else m.CHIMBAL, t0 + k * S16, 0.9 if k % 4 == 0 else 0.6)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0)
            if local in (0, 8):
                m.poe(m.base, m.IMPACTO, t0, 1.0)
            if sec == "Ação" and local == 15:
                m.virada_de_tons(t0, [59, 57, 55, 54, 52, 50, 47, 45])
        elif sec == "Volta":
            m.bat([0, 4, 8, 12], m.BUMBO_F, m.base, t0)
            if local == 6:
                m.poe(m.base, m.rufo(2, 0.2), t0)
                m.poe(m.base, riser(BAR * 2, 1.3), t0)
        else:  # Tema
            g = f.groove
            if g == "marcha":
                m.bat([0, 6, 8, 14], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                m.bat([10], m.CAIXA_FANTASMA, m.base_sala, t0)
                m.bat(range(0, 16, 2), m.CHIMBAL_F, m.pulso, t0)
            elif g == "quatro":
                m.bat([0, 4, 8, 12], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(16):
                    m.poe(m.pulso, m.CHIMBAL_ABERTO if k % 4 == 2 else m.CHIMBAL, t0 + k * S16, 0.85 if k % 4 == 2 else 0.5)
            elif g == "tribal":
                for p, fz in ((0, 1.0), (3, 0.7), (6, 0.8), (8, 1.0), (10, 0.6), (11, 0.7), (14, 0.8)):
                    m.poe(m.base, taiko(0.75 * fz), t0 + p * S16)
                m.bat([0, 3, 6, 8, 11, 14], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(0, 16, 2):
                    m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            elif g == "maqsum":
                for p, fz, grave in ((0, 1.0, True), (3, 0.6, False), (6, 0.7, False), (8, 0.9, True), (12, 0.7, False)):
                    m.poe(m.base, taiko(fz) if grave else tom(64, 0.6 * fz), t0 + p * S16)
                m.bat([0, 3, 8, 11], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(0, 16, 2):
                    m.poe(m.pulso, m.CHIMBAL_F, t0 + k * S16, 0.8)
            elif g == "meio":
                m.bat([0, 3, 7, 10], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                m.poe(m.base, taiko(1.0), t0)
                m.poe(m.base, taiko(0.65), t0 + 10 * S16)
                m.bat(range(0, 16, 2), m.CHIMBAL, m.pulso, t0)
            elif g == "metal":
                m.bat(range(16), m.BUMBO, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(0, 16, 2):
                    m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            elif g == "bigorna":
                m.bat([0, 4, 8, 12], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(4):
                    m.poe(m.pulso, tom(76, 0.7), t0 + k * BEAT + BEAT / 2)
            else:  # galope
                m.bat([0, 2, 3, 6, 8, 10, 11, 14], m.BUMBO_F, m.base, t0)
                m.bat([4, 12], m.CAIXA_F, m.base_sala, t0)
                for k in range(0, 16, 2):
                    m.poe(m.pulso, m.CONDUCAO, t0 + k * S16)
            if local % 4 == 0:
                m.poe(m.pulso, m.PRATO, t0, 0.9)
            if local == 0:
                m.poe(m.base, m.IMPACTO, t0, 1.15 if f.chefe else 0.95)
                if f.chefe:
                    m.poe(m.base, timpano(raiz, 1.05), t0)
            if local in (7, 15):
                m.virada_de_tons(t0, [59, 57, 55, 52, 50, 47, 45, 43])

        # ================================================ melodias
        if sec == "Tema" and local == 0:
            toca(m, f, tema, t0, forte=1.0)
            if f.chefe:
                toca(m, f, tema, t0, forte=0.38, transp=-12, voz="metal")
        if sec == "Ação":
            if local < 8:
                for k, nota in enumerate(corrida(notas)):
                    m.poe(m.tema_eco, supersaw(nota, S16 * 0.9, 0.58 + 0.18 * (k % 4 == 0), f.brilho, False), t0 + k * S16)
            else:
                for pos, d in ((0, 2), (3, 2), (6, 2)):
                    m.poe(m.tema, metais([n + 12 for n in notas], S16 * d * 0.9, 1.15), t0 + pos * S16)
                topo = sorted(n + 24 for n in notas)
                for pos, d, nota in ((8, 2, topo[2]), (10, 2, topo[1]), (12, 4, topo[0] + (12 if topo[0] < 72 else 0))):
                    m.poe(m.tema_eco, supersaw(nota, S16 * d * 0.92, 0.95, f.brilho * 0.95), t0 + pos * S16)
        if sec == "Respiro":
            seq = [notas[0] + 24, notas[2] + 12, notas[1] + 24, notas[2] + 12]
            for k, nota in enumerate(seq):
                m.poe(m.tema_eco, pan(v4.sino(nota, 0.75), 0.3 * (1 if k % 2 else -1)), t0 + k * BEAT)
            m.poe(m.tema_eco, supersaw(max(notas) + 12, BAR * 0.95, 0.45, f.brilho * 0.5, True), t0)
            if local == 0:                                                        # o motivo do tema, devagar, nos sinos
                for ini, dur, n in tema[:4]:
                    m.poe(m.tema_eco, pan(v4.sino(n, 0.55), -0.2), t0 + BAR * 4 + ini * BEAT * 2)
        if sec == "Hino" and local == 0:
            toca(m, f, hino, t0, forte=1.08, dobra=-12)
            toca(m, f, hino, t0, forte=0.55, transp=-12, voz="metal")
        if sec == "Refrão" and local == 0:
            sobe = 1 if f.chefe else 0
            toca(m, f, hino, t0, forte=1.15, transp=sobe, dobra=12, ganho_dobra=0.42, terca=True)
            toca(m, f, hino, t0, forte=0.65, transp=sobe - 12, voz="metal")
        if sec == "Volta" and local == 0:
            toca(m, f, [x for x in tema if x[0] < 16], t0, forte=0.95)
        if sec == "Volta" and local >= 6:
            m.poe(m.tema_eco, supersaw(max(notas) + 12 + 2 * (local - 6), BAR * 0.95, 0.6 + 0.15 * (local - 6), 2600 + 1500 * (local - 6), False), t0)

    m.renderiza(f"caminho do nexus · {f.nome} (v9)")


if __name__ == "__main__":
    F = faixas()
    pedidos = sys.argv[1:] or ["regioes", "chefes"]
    erros = [e for f in F.values() for e in checa(f)]
    for e in erros:
        print("!!", e)
    if "checa" in pedidos:
        print(f"{len(erros)} problema(s) nas melodias")
        sys.exit(1 if erros else 0)
    assert not erros, "melodias com nota fora do acorde"
    for p in pedidos:
        alvo = [f for k, f in F.items() if (p == "regioes" and k.startswith("reg-")) or (p == "chefes" and k.startswith("chefe-")) or k == p]
        for f in alvo:
            faz(f)
