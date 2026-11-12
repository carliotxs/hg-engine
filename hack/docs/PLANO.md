# Plano do rom hack HeartGold

Base: hg-engine (Gen 1 a 9 disponíveis, Megas, Fairy, batalhas modernas). Pipeline e regras em `hack/README.md`.

Legenda: ✅ feito · 🔨 em curso · ⏳ por fazer · 🔬 precisa de investigação

## Fase 1: mecânicas e qualidade de vida

| Feature | Estado | Notas |
|---|---|---|
| Curva de EXP da Gen 5 | ✅ | `EXPERIENCE_FORMULA_GEN 5`, com escala pela diferença de níveis |
| Exp Share de Kalos | ✅ testado | Item-chave; usar na mochila liga ou desliga. Começa ligada. Quem luta divide a EXP como na Gen 5; o resto da equipa ganha 50%. Recebe-se do Mr. Pokémon, como no original |
| Level caps por insígnias | ✅ testado (0 e 8 insígnias) | Tabela `sBadgeLevelCaps` em `src/pokemon.c`, a afinar com os treinadores novos. A var 0x416F substitui-a se for preciso |
| TMs reutilizáveis | ✅ | Já vinha ligado no engine |
| HMs apagáveis | ✅ | `DELETABLE_HMS` |
| Mints e Bottle Caps em Goldenrod (4.º andar) | ✅ testado | 21 Mints (20 000₽), Bottle Cap (20 000₽), Gold Bottle Cap (60 000₽). Bottle Caps só a partir do nível 50, como o hyper training |
| Odds de shiny 1/4096 | ✅ | `SHINY_ODDS 16` |
| Shiny Charm funcional | ✅ testado | +2 tentativas em selvagens, ofertas e ovos da Day Care (acumula com o método Masuda) |
| Oval Charm funcional | ✅ testado | Probabilidade de ovo a cada 256 passos: 20/50/70% passam a 40/80/88%, como na Gen 5+. `src/hack_daycare.c` |
| Bicicleta mais rápida | 🔬 | A rotina do jogo ainda não está descompilada; é preciso encontrar a tabela de velocidade no overlay do campo |
| Adicionar à equipa depois de apanhar | 🔬 | Prompt "adicionar à equipa / enviar para o PC" quando a equipa está cheia. Mexe na UI pós-captura |

## Fase 2: Pokédex e mundo

- ⏳ Encontros Gen 1 a 9 em Johto e Kanto (`data/Encounters.c`), por zona e por hora do dia, com a distribuição por tipos coerente com cada rota
- ⏳ Iniciais alternativos (`src/starters.c`)
- ⏳ Ativar os scripts e eventos dumpados (`make dump_scripts`, depois `BUILD_DUMPED_SCR_SEQ` e `BUILD_DUMPED_EVENTDATA`) para a história ficar toda em texto no git, em vez de edições binárias no DSPRE
- 🔬 Encontros visíveis no overworld. Caminho realista: Pokémon estáticos visíveis em pontos fixos (eventos do mapa), com respawn diário. Spawns dinâmicos como no SwSh obrigariam a um sistema novo de overworld e são um projeto à parte

## Fase 3: história e batalhas

- ⏳ **Arco de Kalos/Megas**: Key Stone a meio do jogo (depois de Olivine) e Mega Pedras escondidas pelo mapa ou dadas em side quests
- ⏳ **Equipa Rocket reforçada**: admins e Giovanni com equipas novas e mais confrontos (Radio Tower, Lago da Fúria, Mahogany)
- ⏳ **Outras equipas na história**: por exemplo, a Equipa Galactic atrás das Ruínas de Sinjoh e do Unown, e a Equipa Plasma a roubar Pokémon em Ilex
- ⏳ **Líderes com novos tipos**: proposta Whitney → Fairy; restantes a decidir
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
- Automático em jogo: `hack/scripts/test.sh` corre os cenários descritos em `hack/README.md` numa ROM de debug (Exp Share, level caps, loja, Bottle Caps, Shiny Charm). Cada feature nova traz o seu cenário
- Manual por fase: jogar um save real em pontos-chave (antes do 1.º ginásio, Goldenrod, Olivine) para ver o que os cenários não cobrem: ritmo de EXP, texto, a loja no mapa real

Por testar na Fase 1: curva de EXP e caps ao longo de um jogo real; HMs apagáveis e TMs reutilizáveis (opções do engine, sem cenário próprio); a loja aberta pelo balconista real do 4.º andar (o cenário abre a mesma tabela por script).
