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
| Adicionar à equipa depois de apanhar | ✅ testado | Com a equipa cheia, o Pokémon vai para o PC como sempre e, de volta ao campo, aparece a pergunta; com "Sim" escolhe-se o membro da equipa que troca de lugar com ele, e o Pokémon seguidor é atualizado. Um Pokémon com Mail não pode sair (como no PC). Não aparece no Safari, no Bug-Catching Contest nem no Pal Park. As ofertas não precisam: no HeartGold exigem sempre espaço na equipa. `src/hack_capture.c` e script comum 2076 |

## Fase 2: Pokédex e mundo

- ✅ Encontros Gen 1 a 9 em Johto e Kanto, em mistura: 567 espécies selvagens (402 novas) em 129 zonas, por habitat e hora do dia, geradas por `hack/scripts/gen_encounters.py`. Falta: jogar as rotas para afinar o equilíbrio, atualizar as áreas da Pokédex (`data/PokedexArea.c`), Headbutt, Safari e swarms (ficaram originais)
- ✅ Iniciais alternativos: Dratini, Beldum e Larvitar (`HACK_ALT_STARTERS`). O rival fica com o seguinte na ordem (Beldum, Larvitar, Dratini) e as equipas dele seguem a linha evolutiva por nível. Testado com `newgame.py` até receber o inicial; falta jogar o primeiro combate com o rival
- ✅ História em texto no git: scripts, eventos e textos despejados com `make dump_scripts` e compilados com `BUILD_DUMPED_SCR_SEQ` e `BUILD_DUMPED_EVENTDATA`. Verificado byte a byte contra a ROM original
- ✅ Encontros visíveis no overworld, primeira leva: 11 Pokémon estáticos em pontos fixos de Johto com respawn diário (`hack/scripts/gen_static_mons.py`, tabela em `hack/README.md`). Testado em jogo o de Cherrygrove; falta ver os outros 10 no sítio, confirmar a reposição à meia-noite e estender a Kanto. Spawns dinâmicos como no SwSh continuam fora do âmbito

## Fase 3: história e batalhas

Decisões de design fechadas:

- **Dificuldade**: equipas melhores e coerentes (espécies, golpes, itens) e +2 a 4 níveis em relação ao original, para compensar a Exp Share e a EXP da Gen 5. Sem level cap
- **Líderes**: todos mantêm os tipos originais, incluindo a Whitney (Normal). Os tipos alternativos ficam para os treinadores secretos
- **Arco de Kalos/Megas**: a Korrina aparece no topo do Farol de Olivine depois de curares a Amphy, desafia-te e entrega a Key Stone e a Ampharosite. As outras Mega Pedras ficam escondidas pelo mapa ou em side quests
- **Rival extra**: 3 confrontos novos: entrada do Farol de Olivine, Lago da Fúria depois do Gyarados vermelho e saída do Ice Path
- **Treinadores secretos**: 8 especialistas de tipo que os ginásios de Johto não cobrem (Fada, Sombrio, Água, Fogo, Erva, Elétrico, Psíquico, Terra), com equipas de 6, escondidos em sítios opcionais de Johto e Kanto. São a "Liga das Sombras" da Fase 4

Trabalho, por ordem:

1. ⏳ Líderes de Johto, Elite Four e Lance: equipas novas e níveis (`data/Trainers.c`)
2. ⏳ Equipa Rocket reforçada: grunts, admins e Giovanni com equipas novas e mais confrontos (Radio Tower, Lago da Fúria, Mahogany)
3. ⏳ Korrina no Farol: personagem, combate, Key Stone e Ampharosite; ativar a Mega Evolução (flag 2518)
4. ⏳ Rival: os 3 confrontos novos e equipas a condizer
5. ⏳ Outras equipas na história: Equipa Galactic nas Ruínas de Alph e de Sinjoh, Equipa Plasma em Ilex
6. ⏳ Treinadores secretos: os 8 especialistas, colocação e recompensas
7. ⏳ Bosses de história em batalhas duplas, com IVs e EVs

## Fase 4: side quests

- ⏳ **Shiny Charm** (sem ligação à Pokédex): vencer todos os treinadores secretos, por exemplo uma "Liga das Sombras" de 8 treinadores escondidos em Johto e Kanto; quem dá o charm é o último
- ⏳ **Oval Charm** (sem ligação à Pokédex): o casal da Day Care dá-o depois de chocares um número de ovos (ex.: 10)
- ⏳ Caça às Mega Pedras, com pistas por chamadas do Pokégear
- ⏳ Tutores de golpes modernos e loja de BP com Ability Patch / Ability Capsule

### Especialistas de espécie ("mirror match")

Pedido de design: existe um especialista para cada Pokémon de evolução final e para cada Pokémon de fase única, espalhados pelo mapa. Só se consegue desafiar um especialista levando o mesmo Pokémon que ele, e o combate é um mirror match de 1 contra 1.

- ⏳ Por desenhar antes de implementar: são várias centenas de espécies, por isso os treinadores e as equipas têm de ser gerados por script (como os encontros), e é preciso decidir como aparecem no mapa (um NPC por espécie não cabe nos limites de objetos de cada mapa), o nível do combate, como se escolhe o Pokémon do jogador e a recompensa

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
