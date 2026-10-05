# Validação comportamental do elenco — 2026-10-05

As provas executam stepBattle em contextos preparados e registram eventos/efeitos reais. Para Yugi, Kaiba e Doctor Doom, as cargas dos personagens evoluem durante até 120 s; os demais começam com a habilidade testada pronta para isolar sua consequência. As sequências só contam quando a ação e pelo menos um efeito observável aparecem, nunca apenas pelo uso do botão/skill.

- Novos personagens: 76/76 avaliados; 12 sementes por contrato.
- Resultado por grupo: {"redesigned":{"count":21,"passed":21,"failed":[]},"adjusted":{"count":31,"passed":31,"failed":[]},"excellent":{"count":24,"passed":24,"failed":[]}}
- Campeonatos de jornada não são alvo desta validação.

## Vinte e um redesenhados

| Personagem | Sequência característica observada | Simulações | Identidade | Nota |
|---|---|---:|---|---|
| Piccolo | cast inimigo → leitura marca e enfraquece a ameaça | 12/12 | comprovada |  |
| Sakura Haruno | aliado ferido → Byakugou cura e regenera o trio | 12/12 | comprovada |  |
| Inosuke Hashibira | cast inimigo → instinto atrasa e confunde a ameaça | 12/12 | comprovada |  |
| Muzan Kibutsuji | ação → chicotes atingem e marcam os três inimigos | 12/12 | comprovada |  |
| Yuji Itadori | alvo vulnerável → Black Flash aplica a segunda onda | 12/12 | comprovada |  |
| Eren Yeager | Condição baixa → endurecimento protege Eren | 12/12 | comprovada |  |
| Griffith | aliado ameaçado → comando acelera/reposiciona o trio | 12/12 | comprovada |  |
| Giorno Giovanna | aliado ferido → Vida criada cura e regenera | 12/12 | comprovada |  |
| Power | Domínio em desvantagem → Prêmio de sangue explode e confunde | 12/12 | comprovada |  |
| Frieren | preparação inimiga → magia carregada atrasa e atinge o conjurador | 12/12 | comprovada |  |
| Loid Forger | preparação inimiga → neutralização cancela o cast | 12/12 | comprovada |  |
| Yugi Muto | preparar duelo → Mago Negro → invocação final (ordem obrigatória) | 12/12 | comprovada |  |
| Seto Kaiba | pressão direta → Dragão Branco → Ultimate Burst (ordem obrigatória) | 12/12 | comprovada |  |
| Black Panther | recebe impacto → armazena energia cinética → descarrega e zera o estoque | 12/12 | comprovada |  |
| Vision | faseia → reduz o impacto recebido → volta sólido e usa raio solar | 12/12 | comprovada |  |
| Ant-Man | inimigo ferido → formigas aceleram/reposicionam o trio | 12/12 | comprovada |  |
| Captain Marvel | absorve impacto → armazena energia → explosão binária a libera | 12/12 | comprovada |  |
| Professor Xavier | coordenação do trio: 6/6; interrupção mental: 6/6; dano básico configurado em 20 | 12/12 | comprovada |  |
| Doctor Doom | armadura tecnológica → ritual místico → contingência (ordem obrigatória) | 12/12 | comprovada |  |
| Silver Surfer | impacto recebido → transmutação vira proteção e mobilidade | 12/12 | comprovada |  |
| Green Lantern | escudo do aliado ameaçado: 4/4; prisão que cancela preparação: 4/4; arma ofensiva contra abertura: 4/4 | 12/12 | comprovada |  |

## Cobertura dos outros grupos

- Frieza: 12/12 probes do ajuste — comprovada. habilidade 2 (Raio mortal) emitiu efeito de damage/status.
- Kakashi Hatake: 12/12 probes do ajuste — comprovada. habilidade 3 (Cópia perfeita) emitiu efeito de damage/interrupt/status.
- Itachi Uchiha: 12/12 probes do ajuste — comprovada. habilidade 3 (Susanoo) emitiu efeito de damage/status.
- Nezuko Kamado: 12/12 probes do ajuste — comprovada. habilidade 2 (Explosão de sangue) emitiu efeito de damage/status.
- Ichigo Kurosaki: 12/12 probes do ajuste — comprovada. habilidade 2 (Máscara Hollow) emitiu efeito de status.
- Kenpachi Zaraki: 12/12 probes do ajuste — comprovada. habilidade 3 (Retirar o limitador) emitiu efeito de damage/status.
- Levi Ackerman: 12/12 probes do ajuste — comprovada. habilidade 3 (Execução relâmpago) emitiu efeito de damage.
- Gon Freecss: 12/12 probes do ajuste — comprovada. habilidade 3 (Jajanken: Papel) emitiu efeito de damage/status.
- Killua Zoldyck: 12/12 probes do ajuste — comprovada. habilidade 2 (Palma relâmpago) emitiu efeito de damage/interrupt/status.
- Alphonse Elric: 12/12 probes do ajuste — comprovada. habilidade 3 (Barreira transmutada) emitiu efeito de shield/status.
- Roy Mustang: 12/12 probes do ajuste — comprovada. habilidade 1 (Estalo de ignição) emitiu efeito de damage/status.
- Guts: 12/12 probes do ajuste — comprovada. habilidade 3 (Último esforço) emitiu efeito de damage/status.
- Denji: 12/12 probes do ajuste — comprovada. habilidade 2 (Puxar a corda) emitiu efeito de damage/status/heal.
- Yor Forger: 12/12 probes do ajuste — comprovada. habilidade 2 (Investida elegante) emitiu efeito de damage/status.
- Ken Kaneki: 12/12 probes do ajuste — comprovada. habilidade 3 (Centípede) emitiu efeito de damage/status.
- Scarlet Witch: 12/12 probes do ajuste — comprovada. habilidade 3 (Distorção do caos) emitiu efeito de damage/status.
- Daredevil: 12/12 probes do ajuste — comprovada. habilidade 1 (Radar sensorial) emitiu efeito de status.
- Punisher: 12/12 probes do ajuste — comprovada. habilidade 3 (Alvo confirmado) emitiu efeito de damage.
- Blade: 12/12 probes do ajuste — comprovada. habilidade 1 (Rastreio vampírico) emitiu efeito de status.
- Moon Knight: 12/12 probes do ajuste — comprovada. habilidade 3 (Julgamento de Khonshu) emitiu efeito de damage/status.
- Storm: 12/12 probes do ajuste — comprovada. habilidade 3 (Olho da tempestade) emitiu efeito de damage/status.
- Jean Grey: 12/12 probes do ajuste — comprovada. habilidade 3 (Fênix desperta) emitiu efeito de damage/status.
- Rogue: 12/12 probes do ajuste — comprovada. habilidade 3 (Memória emprestada) emitiu efeito de damage/heal/status.
- Gambit: 12/12 probes do ajuste — comprovada. habilidade 3 (Bastão cinético) emitiu efeito de damage/status.
- Venom: 12/12 probes do ajuste — comprovada. habilidade 2 (Mordida predatória) emitiu efeito de heal/status.
- Carnage: 12/12 probes do ajuste — comprovada. habilidade 1 (Lâminas vivas) emitiu efeito de damage/status.
- Loki: 12/12 probes do ajuste — comprovada. habilidade 2 (Troca de lugar) emitiu efeito de status.
- Ultron: 12/12 probes do ajuste — comprovada. habilidade 3 (Evolução autônoma) emitiu efeito de damage/interrupt.
- Star-Lord: 12/12 probes do ajuste — comprovada. habilidade 3 (Dança de distração) emitiu efeito de damage/status.
- Cyborg: 12/12 probes do ajuste — comprovada. habilidade 3 (Adaptação de sistema) emitiu efeito de interrupt/damage.
- Shazam: 12/12 probes do ajuste — comprovada. habilidade 3 (Sabedoria de Salomão) emitiu efeito de interrupt/damage.

- Gohan: 12/12 probes da ação característica — comprovada.
- Tanjiro Kamado: 12/12 probes da ação característica — comprovada.
- Zenitsu Agatsuma: 12/12 probes da ação característica — comprovada.
- Megumi Fushiguro: 12/12 probes da ação característica — comprovada.
- Nobara Kugisaki: 12/12 probes da ação característica — comprovada.
- Ryomen Sukuna: 12/12 probes da ação característica — comprovada.
- Rukia Kuchiki: 12/12 probes da ação característica — comprovada.
- Sosuke Aizen: 12/12 probes da ação característica — comprovada.
- Mikasa Ackerman: 12/12 probes da ação característica — comprovada.
- Hisoka Morow: 12/12 probes da ação característica — comprovada.
- Kurapika: 12/12 probes da ação característica — comprovada.
- Makima: 12/12 probes da ação característica — comprovada.
- Anya Forger: 12/12 probes da ação característica — comprovada.
- Jotaro Kujo: 12/12 probes da ação característica — comprovada.
- Dio Brando: 12/12 probes da ação característica — comprovada.
- Sung Jinwoo: 12/12 probes da ação característica — comprovada.
- Ghost Rider: 12/12 probes da ação característica — comprovada.
- Green Goblin: 12/12 probes da ação característica — comprovada.
- Galactus: 12/12 probes da ação característica — comprovada.
- Groot: 12/12 probes da ação característica — comprovada.
- Rocket Raccoon: 12/12 probes da ação característica — comprovada.
- Aquaman: 12/12 probes da ação característica — comprovada.
- Cyclops: 12/12 probes da ação característica — comprovada.
- Edward Elric: 12/12 probes da ação característica — comprovada.
