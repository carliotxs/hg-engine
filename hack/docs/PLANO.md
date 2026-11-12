# Plano do rom hack HeartGold

Base: hg-engine (Gen 1 a 9 disponíveis, Megas, Fairy, batalhas modernas). Pipeline e regras em `hack/README.md`.

Legenda: ✅ feito · 🔨 em curso · ⏳ por fazer · 🔬 precisa de investigação

## Fase 1: mecânicas e qualidade de vida

| Feature | Estado | Notas |
|---|---|---|
| Curva de EXP da Gen 5 | ✅ | `EXPERIENCE_FORMULA_GEN 5`, com escala pela diferença de níveis |
| Exp Share de Kalos | ✅ testado | Item-chave; usar na mochila liga ou desliga. Começa ligada. Quem luta divide a EXP como na Gen 5; o resto da equipa ganha 50%. Recebe-se do Mr. Pokémon, como no original |
| Level caps por insígnias | ❌ removido | Decisão de design: o hack não tem level cap. O sistema do engine (`IMPLEMENT_LEVEL_CAP`) fica desligado |
| TMs reutilizáveis | ✅ | Já vinha ligado no engine |
| HMs apagáveis | ✅ | `DELETABLE_HMS` |
| Mints e Bottle Caps em Goldenrod (4.º andar) | ✅ testado | 21 Mints (20 000₽), Bottle Cap (20 000₽), Gold Bottle Cap (60 000₽). Bottle Caps só a partir do nível 50, como o hyper training |
| Odds de shiny 1/4096 | ✅ | `SHINY_ODDS 16` |
| Shiny Charm funcional | ✅ testado | +2 tentativas em selvagens, ofertas e ovos da Day Care (acumula com o método Masuda) |
| Oval Charm funcional | ✅ testado | Probabilidade de ovo a cada 256 passos: 20/50/70% passam a 40/80/88%, como na Gen 5+. `src/hack_daycare.c` |
| Bicicleta mais rápida | ✅ testado | Velocidade máxima a dobrar (2 frames por mosaico em vez de 4), com a mesma aceleração inicial. A rotina está no arm9 (0205D658), não no overlay; são 2 bytes em `bytereplacement`. Falta ver em jogo real as transições entre mapas a esta velocidade |
| Adicionar à equipa depois de apanhar | 🔬 | Prompt "adicionar à equipa / enviar para o PC" quando a equipa está cheia. Mexe na sequência pós-captura do overlay de batalha (pergunta Sim/Não e escolha do Pokémon que sai); fica para um PR próprio |

## Fase 2: Pokédex e mundo

- ✅ Encontros Gen 1 a 9 em Johto e Kanto, em mistura: 567 espécies selvagens (402 novas) em 129 zonas, por habitat e hora do dia, geradas por `hack/scripts/gen_encounters.py`. Falta: jogar as rotas para afinar o equilíbrio, atualizar as áreas da Pokédex (`data/PokedexArea.c`), Headbutt, Safari e swarms (ficaram originais)
- ✅ Iniciais alternativos: Dratini, Beldum e Larvitar (`HACK_ALT_STARTERS`). O rival fica com o seguinte na ordem (Beldum, Larvitar, Dratini) e as equipas dele seguem a linha evolutiva por nível. Testado com `newgame.py` até receber o inicial; falta jogar o primeiro combate com o rival
- ✅ História em texto no git: scripts, eventos e textos despejados com `make dump_scripts` e compilados com `BUILD_DUMPED_SCR_SEQ` e `BUILD_DUMPED_EVENTDATA`. Verificado byte a byte contra a ROM original
- 🔬 Encontros visíveis no overworld. Caminho realista: Pokémon estáticos visíveis em pontos fixos (eventos do mapa), com respawn diário. Spawns dinâmicos como no SwSh obrigariam a um sistema novo de overworld e são um projeto à parte

## Fase 3: história e batalhas

- ⏳ **Arco de Kalos/Megas**: Key Stone a meio do jogo (depois de Olivine) e Mega Pedras escondidas pelo mapa ou dadas em side quests
- ⏳ **Equipa Rocket reforçada**: admins e Giovanni com equipas novas e mais confrontos (Radio Tower, Lago da Fúria, Mahogany)
- ⏳ **Outras equipas na história**: por exemplo, a Equipa Galactic atrás das Ruínas de Sinjoh e do Unown, e a Equipa Plasma a roubar Pokémon em Ilex
- ⏳ **Líderes**: mantêm os tipos originais (sem trocas). Os tipos alternativos pensados (Sombrio, Água, etc.) ficam para os treinadores especiais
- ⏳ **Rival extra**: 2 a 3 confrontos novos com o Silver entre o 4.º e o 8.º ginásio
- ⏳ **Treinadores secretos**: opcionais, difíceis, com recompensas raras
- ⏳ **Bosses de história**: batalhas duplas e equipas com IVs/EVs

## Fase 4: side quests

- ⏳ **Shiny Charm** (sem ligação à Pokédex): vencer todos os treinadores secretos, por exemplo uma "Liga das Sombras" de 8 treinadores escondidos em Johto e Kanto; quem dá o charm é o último
- ⏳ **Oval Charm** (sem ligação à Pokédex): o casal da Day Care dá-o depois de chocares um número de ovos (ex.: 10)
- ⏳ Caça às Mega Pedras, com pistas por chamadas do Pokégear
- ⏳ Tutores de golpes modernos e loja de BP com Ability Patch / Ability Capsule

## Outras sugestões

- **Wild double battles** na erva alta (opção que já existe no engine)
- **Rock Smash sem HM** (o engine já tem a base em `rock_smash_item.c`), estendido a Cut e Strength com itens-chave, para combinar com os HMs apagáveis
- **Move Relearner e Move Deleter** juntos no Centro Pokémon de Goldenrod
- **Ability Capsule e Ability Patch** à venda no mesmo andar das Mints
- **Rematches semanais** com os líderes pelo Pokégear, com equipas de nível 70+
- **Modo difícil opcional** (flag escolhida no início): IVs 31 nos treinadores e itens proibidos em batalha (`DISABLE_ITEMS_IN_TRAINER_BATTLE`)
- **Estações do ano** já ligadas (Deerling e Sawsbuck): aproveitar para eventos sazonais

## Testes

- Automático: `verify.py` confirma que a ROM arranca
- Automático em jogo: `hack/scripts/test.sh` corre os cenários descritos em `hack/README.md` numa ROM de debug (Exp Share, loja, Bottle Caps, Shiny Charm). Cada feature nova traz o seu cenário
- Manual por fase: jogar um save real em pontos-chave (antes do 1.º ginásio, Goldenrod, Olivine) para ver o que os cenários não cobrem: ritmo de EXP, texto, a loja no mapa real

Por testar na Fase 1: curva de EXP ao longo de um jogo real; HMs apagáveis e TMs reutilizáveis (opções do engine, sem cenário próprio); a loja aberta pelo balconista real do 4.º andar (o cenário abre a mesma tabela por script).
