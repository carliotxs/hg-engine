# Plano do rom hack HeartGold

Base: hg-engine (Gen 1 a 9 disponíveis, Megas, Fairy, batalhas modernas). Pipeline e regras em `hack/README.md`.

Legenda: ✅ feito · 🔨 em curso · ⏳ por fazer · 🔬 precisa de investigação

## Visão: uma viagem por várias regiões

Direção definida pelo dono do projeto (2026-11-12):

- **Personagem personalizável**: nome, género e cores do sprite
- **De Kanto a Unova**: o jogo começa em Kanto e segue região a região
- **Equipa nova em cada região**: ao chegar a uma região, o jogador deposita todos os Pokémon e vai recuperando o acesso a eles à medida que ganha insígnias, com os mesmos níveis da obediência (um Pokémon só fica disponível quando a insígnia que o faria obedecer estiver ganha)
- **Iniciais da região**: cada região oferece o seu trio
- **História base + eventos aleatórios**: cada região segue a sua história original, com eventos soltos por cima (por exemplo, a Equipa Rocket a assaltar um Poké Mart; vencê-los dá um Elixir)

O que isto muda no plano: as Fases 1 a 4 continuam válidas como "a região de Johto bem feita"; as Fases 5 a 7, no fim deste documento, tratam das mecânicas multi-região e das regiões novas. A pesquisa de suporte está em `hack/docs/PESQUISA.md`.

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
- ✅ Iniciais da região: o jogo voltou ao trio de Johto (Chikorita, Cyndaquil, Totodile), com o rival, os scripts e os textos originais. O trio alternativo (Dratini, Beldum, Larvitar) fica desligado em `HACK_ALT_STARTERS`; na visão multi-região cada região dá o seu trio
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

1. ✅ Líderes de Johto, Elite Four e Lance: equipas novas com golpes e itens, tipos originais, ás 2 a 4 níveis acima do original (`hack/scripts/gen_trainer_teams.py`). Testado em jogo o Falkner; faltam os líderes de Kanto, o Blue, o Red e as desforras
2. ✅ Equipa Rocket reforçada: executivos e Giovanni com equipas completas (+3 níveis), 38 recrutas melhorados automaticamente e 5 recrutas novos (Route 43, Lago da Fúria, Mahogany e 2 em Goldenrod durante a tomada da Radio Tower). Testados em jogo, por capítulos, 4 dos 5 recrutas novos; os executivos e o Giovanni continuam por jogar. Falta um confronto novo com um executivo no Lago da Fúria, se se quiser mais do que recrutas
   - ✅ testado **Giovanni na história principal**: depois de libertares a Radio Tower, o obstáculo invisível da gruta escondida de Tohjo Falls desaparece (chega-se lá com Surf e Waterfall, ou seja, depois da 8.ª insígnia). O Giovanni está lá, a ouvir o rádio; luta, deixa a Kangaskhanite e vai-se embora de vez. O evento do Celebi não foi tocado
3. ✅ testado Korrina no Farol: aparece na sala da luz depois de a Jasmine voltar ao ginásio, luta (Mienfoo, Hawlucha e Lucario com Lucarionite), liga a Mega Evolução (flag 2518) e dá a Key Stone e a Ampharosite (`hack/scripts/gen_korrina.py`). Usa o sprite e a classe de uma treinadora existente (Battle Girl). Falta espalhar as outras Mega Pedras
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

Um especialista por cada Pokémon de evolução final ou de fase única, só desafiável com a mesma espécie, em 1 contra 1.

- ✅ Sistema e geração: 389 especialistas colocados por `hack/scripts/gen_specialists.py`, em zonas onde a família aparece, com nível relativo à zona, item da espécie como recompensa e contador de vitórias. Testado em jogo o do Mantine em Cherrygrove (com e sem Mantine na equipa)
- ⏳ Prémios por marcos do contador (por exemplo 50, 150 e todos) e um NPC que diga quantos faltam
- ⏳ Os 5 sem zona com chão livre (Shuckle, Magmortar, Ninetales, Weezing, Centiskorch) e as espécies que só vierem a existir por estáticos, ofertas ou side quests (lendários incluídos)
- ⏳ 6 especialistas (Tohjo Falls e Ice Path B1F) estão em sítios inalcançáveis por falta de chão válido no mapa deles; mudar de mapa
- ⏳ Afinações: sprites e falas variados por tipo, ver os 388 restantes no sítio (posições calculadas, não vistas); depois da batalha o Pokémon seguidor fica a ser o que lutou até mudar de mapa

## Fase 5: mecânicas multi-região, ainda em Johto e Kanto

Tudo isto pode ser feito e testado no jogo atual, antes de existir uma terceira região.

- ✅ **Regras de "quem aparece quando"** (`src/hack_story.c`): objetos da história aparecem e desaparecem por flags de história, dia da semana e hora, sem editar os scripts de carga dos mapas. É a base dos eventos aleatórios e dos visitantes
- 🔨 **Eventos aleatórios**: ✅ testado o primeiro, um recruta Rocket a assaltar um Poké Mart (Cherrygrove à segunda e quinta, Violet à terça e sexta, Azalea à quarta e sábado), uma vez por dia, com um Elixir de recompensa. ⏳ Mais eventos e sorteio verdadeiro (hoje a rotação é pelo dia da semana)
- 🔨 **Visitantes famosos em certos dias e horas**: ✅ testado o Crasher Wake no Lago da Fúria aos sábados, das 10h às 20h, uma batalha por dia, com uma Mystic Water. ⏳ Os outros líderes de Sinnoh, a Cynthia e o Steven: o HeartGold já tem os sprites de batalha dos líderes de Sinnoh e da Cynthia, e overworlds dos oito líderes, do Steven e da Cynthia (o Steven e o Cyrus não têm sprite de batalha)
- ⏳ **Depósito e desbloqueio por insígnias**: ao entrar numa região, a equipa e as caixas ficam bloqueadas; cada insígnia desbloqueia os Pokémon até ao nível de obediência correspondente. Para já pode ser prototipado na passagem Johto → Kanto. Os patamares do jogo original para Pokémon trocados são nível 10 sem insígnias, 30, 50 e 70 com a 2.ª, 4.ª e 6.ª (a confirmar no código antes de implementar) e todos com a 8.ª. A decidir: se o bloqueio é só por nível ou também por região de origem
- 🔬 **Acessos alternativos a zonas**: a gruta escondida de Tohjo Falls mostrou o padrão: zonas que o jogo original fecha com um obstáculo invisível podem abrir por regra (flag de história, dia, hora), sem mexer nos mapas. Candidatas a rever com o mesmo método: zonas só de evento (Sinjoh Ruins, Embedded Tower), salas fechadas de grutas e atalhos entre rotas. Cada uma precisa de ser vista nos dados de colisão antes de se prometer
- 🔬 **Personagem personalizável**: nome e género já existem; as cores do sprite pedem paletas alternativas para o overworld e para o sprite de batalha do jogador, e um ecrã ou NPC para as escolher
- 🔬 **Começar em Kanto**: inverter a ordem (Kanto primeiro, Johto depois) mexe no início do jogo, na ordem dos ginásios, nos níveis de tudo e na Liga. É a maior mudança dentro das duas regiões existentes; convém decidir cedo se é mesmo para fazer ou se a viagem começa em Johto

## Fase 6: assets de personagens novas

Resumo da pesquisa (detalhes e fontes em `hack/docs/PESQUISA.md`):

- **Korrina**: existe um sprite de batalha 80x80 (Gnomowladny, no índice de treinadores do Pokémon Showdown), de uso livre com crédito, mas tem 46 cores e o autor pede para não editar sem autorização; reduzir a 16 cores conta como edição, por isso é preciso pedir. Não foi encontrado nenhum overworld dela em estilo Gen 4: é preciso desenhar ou encomendar
- **Outras personagens**: o mesmo índice tem a Diantha, o Sycamore, o Steven e quase toda a liga de Kalos, além do N, Ghetsis, Cyrus e Crasher Wake oficiais; quase todos passam das 16 cores. Há overworlds do N e do Ghetsis num pacote de estilo Gen 4, com condição de não redistribuir
- **Como entram no jogo**: o hg-engine constrói classes de treinador e overworlds a partir de PNG e JSON, sem editores binários (páginas "Adding New Trainer Classes" e "hgss-new_overworlds")
- ⏳ Tarefas: pedir autorização aos autores, converter a Korrina para 16 cores, criar a classe de treinador dela, desenhar o overworld; manter a lista de créditos em `CREDITS.md`

## Fase 7: regiões novas

O que a pesquisa encontrou:

- Não há nenhum hack publicado que acrescente uma terceira região ao HeartGold ou que porte Sinnoh, Hoenn ou Kalos para ele. O projeto mais próximo (duas regiões feitas de raiz em hg-engine) está em desenvolvimento desde 2024 e em fase de demo
- A capacidade bruta (número de mapas, matrizes, tamanho da ROM) não é o problema. Os bloqueios são: o campo de região do mapa tem 1 bit (Johto ou Kanto), as secções de mapa têm 8 bits e 235 das 256 já estão usadas, e o Pokégear e o Fly usam uma única grelha de 64x64 com 20 pré-visualizações de cidades. A folga do save não foi verificada
- Os mapas do Platinum usam os mesmos formatos, mas os dados de área do HGSS diferem e não há importação documentada. Mapas de raiz fazem-se com o Pokémon DS Map Studio e o DSPRE
- Ordem de grandeza: mapas novos isolados são semanas; uma mini-região com os tilesets do HGSS são meses; uma terceira região completa, com mapa e Fly próprios, é um esforço de vários anos

Caminho proposto, do mais barato para o mais caro:

1. ⏳ Fazer primeiro as mecânicas multi-região (Fase 5) com Johto e Kanto, que já existem
2. 🔬 Prova de conceito: uma zona pequena de uma terceira região (por exemplo um porto e uma cidade) com tilesets do HGSS, ligada por barco, para medir o esforço real e os limites do Pokégear e do save
3. 🔬 Só depois decidir quantas regiões e por que ordem; Sinnoh é a candidata mais barata por partilhar o motor com o Platinum

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
- Por partes: a ROM de debug arranca em capítulos (pontos da história com flags, insígnias e equipa), tanto para os testes automáticos como para jogar à mão com `hack/scripts/play.sh <capítulo>`. Cada parte nova da história deve trazer o seu capítulo
- Automático em jogo: `hack/scripts/test.sh` corre os cenários descritos em `hack/README.md` numa ROM de debug (Exp Share, loja, Bottle Caps, Shiny Charm). Cada feature nova traz o seu cenário
- Manual por fase: jogar um save real em pontos-chave (antes do 1.º ginásio, Goldenrod, Olivine) para ver o que os cenários não cobrem: ritmo de EXP, texto, a loja no mapa real

Por testar na Fase 1: curva de EXP ao longo de um jogo real; HMs apagáveis e TMs reutilizáveis (opções do engine, sem cenário próprio); a loja aberta pelo balconista real do 4.º andar (o cenário abre a mesma tabela por script).
