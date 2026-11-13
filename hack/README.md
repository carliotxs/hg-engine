# Rom hack HeartGold: pipeline

Fork do [hg-engine](https://github.com/BluRosie/hg-engine). Todo o trabalho do hack vive no branch `hack/main`, por cima do engine.

## Fluxo

```
ROM base (HeartGold U, IPKE, nunca vai para o git)
   │
   ├─ include/hack_config.h      toggles de todas as features do hack (HACK_*)
   ├─ include/config.h           opções do engine (EXP, shinies, HMs...)
   ├─ src/                       mecânicas em C (cada alteração dentro de #ifdef HACK_*)
   ├─ data/*.c                   Pokémon, encontros, treinadores, itens, lojas
   ├─ data/text/*.txt            textos
   ├─ data/scr_seq/*.s           scripts (comuns agora; história na Fase 2)
   │
   ▼
hack/scripts/release.sh  =  build.sh  →  verify.py  →  newgame.py  →  package.sh
   │                          make        arranque no     jogo novo até   .zip + .xdelta
   │                                      DeSmuME         ao inicial
   ▼
hack/out/HeartGold-hack-<versão>.zip / .xdelta
```

## Comandos

```bash
# primeira vez (macOS): dependências do README do hg-engine (brew + gcc-arm-embedded + rustup)
hack/scripts/release.sh ~/ROMs/HeartGold_US.nds fase1   # pipeline completo
hack/scripts/build.sh                                   # só compilar (usa o rom.nds já copiado)
.venv/bin/python hack/scripts/verify.py                 # só o teste de arranque
.venv/bin/python hack/scripts/newgame.py                # jogo novo: intro, New Bark, laboratório e escolha do inicial
hack/scripts/package.sh fase1                           # só empacotar
hack/scripts/test.sh                                    # testes em jogo (ROM de debug, ver abaixo)
hack/scripts/test.sh exp_share_on shop                  # só alguns cenários
hack/scripts/test.sh --speed 1 capture_prompt           # mais devagar: tempo real (por omissão a janela corre a 6x)
hack/scripts/test.sh --headless                         # sem janela
```

Define `HG_BASE_ROM` com o caminho da ROM para não o passares em cada comando. O `build.sh` acrescenta ao `PATH` o toolchain ARM em `~/.local/opt/arm-gnu-toolchain` e o rustup do Homebrew, para quem instalou sem sudo (o cask `gcc-arm-embedded` pede palavra-passe; em alternativa extrai-se o `.pkg` com `pkgutil --expand-full` para essa pasta).

Para partilhar o hack, usa só o `.xdelta` (aplica-se com Delta Patcher ou xdelta UI sobre a ROM original). Nunca distribuas o `.nds`. As regras do hg-engine proíbem qualquer tipo de monetização e obrigam a replicar `CREDITS.md`.

## História em texto

Os scripts de campo (`data/scr_seq/scr_seq_NNNN*.s`), os eventos de cada mapa (`data/eventdata/zone_event/`) e os textos (`data/text/custom/`) foram despejados da ROM original com `make dump_scripts DUMP_ROM=rom.nds` e são compilados para a ROM (`BUILD_DUMPED_SCR_SEQ` e `BUILD_DUMPED_EVENTDATA` em `include/config.h`). A história edita-se nesses ficheiros, com diffs normais no git; não se usa o DSPRE para scripts, eventos ou texto, porque o build passaria por cima.

- O despejo foi verificado: na ROM compilada, os únicos arquivos de scripts e eventos diferentes dos originais são os que o hack editou
- As duas linhas `#define BUILD_DUMPED_*` não podem ter comentários à frente: o Makefile só reconhece o `#define` sozinho na linha (com comentário, a história volta a vir da ROM original sem qualquer aviso)
- O `dump_scripts` reescreve `data/text/keys.csv` sem as chaves dos arquivos do engine (829 a 853); se o voltares a correr, repõe esse ficheiro com `git checkout data/text/keys.csv`
- Os scripts comuns e de treinadores do engine continuam nos ficheiros de cinco dígitos (`scr_seq_00003_commonscript.s`)

## Encontros selvagens

`data/Encounters.c` é gerado por `python3 hack/scripts/gen_encounters.py` a partir das tabelas originais (`hack/data/Encounters.vanilla.c`) e das listas de espécies por habitat que estão no topo do script. Não se edita o `.c` à mão: muda-se as listas ou as regras e volta-se a gerar (é determinístico e imprime um relatório).

- Erva: os 4 slots mais comuns (60%) ficam originais, incluindo as espécies de manhã/dia/noite de Johto; os slots 4 e 5 (10% cada) mudam com a hora do dia; os slots 6 a 9 seguem o habitat da zona; os slots 10 e 11 (1% cada) são raros (iniciais de todas as gerações, pseudo-lendários, fósseis nas Ruínas de Alph), a partir do nível 8
- Surf, canas e Rock Smash: os slots mais comuns ficam originais, os restantes são novos, com espécies de mar ou de água doce conforme a zona
- A fase evolutiva acompanha o nível do slot; nenhuma espécie original deixa de existir no jogo (o gerador devolve slots quando é preciso)
- Lendários, míticos, Ultra Beasts e paradoxos ficam de fora, reservados para encontros estáticos

## Pokémon estáticos visíveis

`hack/scripts/gen_static_mons.py` acrescenta aos mapas despejados Pokémon visíveis em pontos fixos: um objeto com o sprite de overworld da espécie (etiqueta 2500 + número da espécie), um script que inicia a batalha e uma flag diária que o esconde até ao dia seguinte. A posição é calculada a partir dos dados de colisão da ROM: o centro de um bloco 3x3 de chão livre, longe dos outros eventos, para nunca tapar um caminho. O script é idempotente; para acrescentar mais, junta-se uma linha a `STATIC_MONS` e corre-se outra vez.

| Mapa | Pokémon | Nível | Flag diária |
|---|---|---|---|
| Cherrygrove City | Yamper | 4 | 2910 |
| Route 31 | Rockruff | 6 | 2900 |
| Route 32 | Riolu | 8 | 2901 |
| Route 33 | Zorua | 10 | 2902 |
| Route 34 | Eevee | 12 | 2903 |
| Route 36 | Absol | 16 | 2904 |
| Route 38 | Mimikyu | 18 | 2905 |
| Route 42 | Goomy | 20 | 2906 |
| Route 44 | Axew | 25 | 2907 |
| Route 45 | Gible | 27 | 2908 |
| Route 47 | Drampa | 32 | 2909 |

Os objetos de um mapa vêm do save enquanto o jogador não sai e volta a entrar nesse mapa, por isso num save antigo um estático novo só aparece depois de recarregar o mapa.

## Especialistas de espécie (mirror match)

`hack/scripts/gen_specialists.py` coloca um especialista por cada Pokémon de evolução final ou de fase única cuja família aparece em estado selvagem (389 de 394; os 5 que faltam só existem em zonas sem chão livre e são listados pelo script). Cada um fica numa zona onde a família aparece, com nível igual ao do slot mais forte dessa família na zona mais 3 (e nunca abaixo do nível a que a espécie evolui).

- Só luta se tiveres a mesma espécie na equipa (viva e sem ser ovo). O combate é 1 contra 1: durante a batalha a tua equipa passa a ser só esse Pokémon e volta ao normal no fim, com a EXP, os PS e os PP que ele ganhou ou perdeu
- O Pokémon do especialista é gerado na hora (espécie e nível pedidos pelo script, IVs máximos), no treinador genérico 738 "Expert" de `data/Trainers.c`
- Vencer dá um item para a espécie (a Mega Pedra, se existir; senão um item competitivo em rotação) e soma 1 ao contador na var 0x416F. Cada especialista tem a sua flag de "vencido"
- Lógica em `src/hack_mirror.c` e no script comum 2077; os scripts dos mapas só passam espécie, nível, item e flag. O gerador é idempotente: quem já está colocado não muda de sítio nem de flag
- Correr depois de `gen_encounters.py`, porque as zonas vêm de `data/Encounters.c`

Atenção ao escrever C para o hack: a `struct Party` (e a `DaycareMon`) dos cabeçalhos do engine são maiores do que as do save por causa do alinhamento. Nunca copiar nem indexar `party->members[]` diretamente; usar `Party_GetMonByIndex`, `PokeCopyPPtoPP` e o tamanho real (8 + 6 x 236 bytes).

## Colocação de NPCs do hack nos mapas

Os geradores (`gen_specialists.py`, `gen_rocket.py`, `gen_korrina.py`) partilham a mesma regra, que está em `gen_specialists.py`: o centro de um bloco 3x3 de chão onde se pode estar (chão normal, chão de gruta ou Cycling Road; erva alta só em último caso), ligado por chão caminhável a uma porta ou a um evento original do mapa, e afastado dos outros eventos. A ligação é essencial: nos mapas interiores e nas grutas o valor 0 dos dados de colisão é o vazio à volta da sala, não chão.

`gen_specialists.py --fix-positions` verifica todos os objetos que o hack acrescentou (ids com `_hack_`) e move os que não cumprem a regra para o sítio válido mais próximo do mesmo mapa; só mudam coordenadas. Corre-se depois de qualquer mudança à regra. Ficam 6 especialistas sem sítio válido no mapa deles (Tohjo Falls e Ice Path B1F); estão no vazio, inalcançáveis, até serem mudados de mapa.

## Objetos da história que aparecem por regra

`src/hack_story.c` tem uma tabela de regras que liga e desliga as flags de esconder dos objetos que o hack acrescenta à história: uma flag de história que tem de estar ligada, uma flag de "já feito", dias da semana e horas. As regras são reavaliadas duas vezes por segundo no campo, e as flags de esconder são lidas quando um mapa carrega; por isso não é preciso editar o script de carga de cada mapa. `hack/scripts/gen_story.py` coloca os objetos e os scripts:

| Objeto | Onde | Aparece quando |
|---|---|---|
| Giovanni | gruta escondida de Tohjo Falls | depois de libertar a Radio Tower, até ser vencido (dá a Kangaskhanite) |
| Obstáculo da gruta | Tohjo Falls | desaparece depois de libertar a Radio Tower |
| Recruta a assaltar o Poké Mart | Cherrygrove (seg, qui), Violet (ter, sex), Azalea (qua, sáb) | nesses dias, até ser vencido nesse dia (dá um Elixir) |
| Crasher Wake | Lago da Fúria | aos sábados das 10h às 20h, uma batalha por dia (dá uma Mystic Water) |

Um evento novo é uma regra na tabela em C, uma entrada em `gen_story.py` e, para o testar, um capítulo (os capítulos podem fingir um dia da semana e uma hora).

## Equipas dos bosses

`python3 hack/scripts/gen_trainer_teams.py` escreve em `data/Trainers.c` as equipas dos treinadores listados na tabela `TEAMS` do script (líderes de Johto, Elite Four e Lance, por agora). A tabela é a fonte de verdade desses treinadores: edita-se lá e volta-se a correr; os nomes de espécies, golpes e itens são validados contra as constantes do engine. Os treinadores que não estão na tabela não são tocados, com uma exceção: os recrutas da Equipa Rocket recebem uma melhoria automática única (+2 níveis e, a partir do segundo Pokémon, espécies de uma lista Veneno/Sombrio em vez de Rattata e Zubat repetidos). A tabela `NEW_TRAINERS` cria treinadores que não existem no jogo original.

`hack/scripts/gen_rocket.py` coloca nos mapas os recrutas Rocket extra (treinadores 739 a 743): Route 43, Lago da Fúria e Mahogany até o esconderijo ser limpo, e dois em Goldenrod durante a tomada da Radio Tower. Lutam quando se fala com eles e desaparecem com as mesmas flags de história dos Rocket originais dessas zonas.

## Testar por partes: capítulos

A ROM de debug sabe arrancar em pontos da história, os capítulos: cada um é uma posição num mapa mais o estado que torna essa parte testável (insígnias, flags, variáveis de história e equipa). Assim não é preciso jogar do início para chegar ao Farol ou a Mahogany.

```bash
hack/scripts/play.sh --list                 # capítulos disponíveis
hack/scripts/play.sh lighthouse_korrina     # abre a janela nesse ponto, para jogares com o teclado
hack/scripts/test.sh korrina rocket_mahogany   # testes automáticos que arrancam num capítulo
```

No modo de jogo: setas para andar, X é o A, Z é o B, S é o X, Enter é o START; o rato toca no ecrã de baixo. O `play.sh` usa a ROM de debug da última corrida do `test.sh`.

Os capítulos estão na tabela `CHAPTERS` de `hack/scripts/gen_chapters.py`, que gera `include/hack_chapters.h` (estado) e `data/scr_seq/include/hack_chapters.inc` (teleportes). Um capítulo novo é uma linha na tabela: mapa, objeto ao lado do qual o jogador fica (`next_to`) ou coordenadas, flags a ligar e desligar, variáveis de história e equipa. Depois de mexer na tabela ou de mover objetos, volta-se a correr o script.

Coisas que aprendi a fazer isto e que convém saber:
- Muitos mapas decidem quem lá está a partir de variáveis de história quando carregam (Goldenrod lê `VAR_SCENE_ROCKET_TAKEOVER`), por isso mexer só nas flags não chega
- Um teleporte por script logo a seguir a carregar o save rebenta o jogo enquanto a faixa com o nome da cidade está no ecrã; a ROM de debug espera 300 frames antes de teleportar
- O relatório de testes é atualizado todos os frames e não pode alocar memória (por exemplo `Bag_GetQuantity`)
- Funções de `src/` chamadas a partir de `src/field/` ou `src/battle/` precisam de `LONG_CALL`
- Visto de sul, o sprite do jogador tapa o NPC do mosaico de cima; os capítulos põem o jogador ao lado

## Testes em jogo

`hack/scripts/test.sh` compila uma ROM de debug (`make HACK_TEST=Y`, guardada em `hack/out/test-debug.nds`) e corre `hack/scripts/ingame_tests.py` no DeSmuME, com a janela aberta a 6x para se ver o tester a jogar (`--headless` desliga a janela). A ROM de debug continua o save automaticamente (por omissão o save de testes público do hg-engine, descarregado para `hack/out/test.sav`; `HG_TEST_SAV` aponta para outro).

Como funciona: o runner escreve o número do cenário num endereço de memória; `src/hack_test.c` monta a equipa, a mochila e as insígnias desse cenário, lança o script comum 2073 (batalha) ou 2075 (loja) e mantém um relatório em memória que o runner lê no fim. Os menus são conduzidos por botões e toque, e cada passo fica em capturas em `hack/out/tests/<cenário>/`.

| Cenário | O que valida |
|---|---|
| `exp_share_on` | quem luta recebe a EXP da Gen 5 completa, o banco recebe 50%, desmaiados 0 |
| `exp_share_off` | com a Exp Share desligada só quem luta recebe EXP |
| `exp_share_switch`, `switch_no_share` | dois lutadores (Baton Pass) dividem a EXP; o banco recebe 50% ou nada |
| `no_level_cap` | não há level cap: com 0 insígnias todos ganham EXP e sobem de nível |
| `shop` | 4.º andar de Goldenrod: compra de Bottle Cap e Adamant Mint a 20 000 |
| `bottle_caps` | Bottle Cap (IV mais baixo), Gold Bottle Cap (todos), sem efeito abaixo do nível 50 |
| `exp_share_toggle` | usar a Exp Share na mochila liga e desliga a flag 2602 |
| `shiny_charm` | estatístico: 3 tentativas com o charm, em selvagens e ofertas (a ROM de teste usa odds 1/32) |
| `capture_prompt` e variantes `_no`, `_cancel`, `_mail` | apanhar com a equipa cheia: o Pokémon vai para o PC e o prompt aparece no campo. "Sim" troca com o membro escolhido (equipa, PC e Pokémon seguidor verificados); "Não" e cancelar deixam tudo igual; um Pokémon com Mail é recusado com mensagem |
| `mirror`, `mirror_no_mon` | o especialista do Mantine em Cherrygrove: com um Mantine na equipa luta 1 contra 1, a equipa volta igual, só o Mantine ganha EXP, o item e o contador sobem e não há segunda batalha; sem Mantine só explica a regra |
| `leader` | combate de treinador contra o Falkner com a equipa nova: três Pokémon vencidos (pela EXP) e dinheiro recebido |
| `korrina` | capítulo do Farol: batalha com a Korrina ganha, Key Stone e Ampharosite recebidas, Mega Evolução ligada, sem segunda batalha (nas capturas vê-se o Lucario dela mega evoluir) |
| `rocket_mahogany`, `rocket_lake`, `rocket_route43`, `rocket_goldenrod` | capítulos com a Rocket ativa: cada recruta novo luta quando se fala com ele, uma só vez |
| `giovanni` | capítulo da gruta de Tohjo Falls: batalha ganha, Kangaskhanite recebida, o Giovanni desaparece |
| `mart_robber` | capítulo do Poké Mart de Cherrygrove numa segunda-feira: batalha, Elixir, o assaltante desaparece |
| `visitor_wake` | capítulo do Lago da Fúria num sábado ao meio-dia: batalha com o Crasher Wake, que depois se vai embora |
| `boss_<nome>` (ou `bosses` para todos) | combate de treinador contra cada boss com equipa nova (13 líderes, Elite Four e Lance, 7 executivos, Giovanni, Korrina, Wake) com um Arceus de nível 100: a equipa carrega, luta e o combate termina com prémio. Bruno e Lance vencem o Pokémon de teste, por isso esses dois cenários falham por agora |
| `view_<capítulo>` | abre o capítulo e tira uma captura |
| `static_mon` | o Yamper de Cherrygrove: vê-se no mapa, bloqueia o mosaico, a batalha começa, a flag diária fica marcada e ele desaparece |
| `bike` | usar a Bicicleta na mochila e pedalar: acelera e chega a 2 frames por mosaico |
| `day_care` | estatístico: rotina de passos da Day Care com compatibilidade 50; Oval Charm sobe os ovos para 80% e o Shiny Charm aplica-se aos ovos |

`hack/scripts/newgame.py` é um teste à parte, na ROM normal: reproduz uma gravação de botões desde o ecrã de título até receber o inicial e falha se o jogo bloquear pelo caminho. As capturas em `hack/out/newgame/` mostram os três iniciais e a mensagem de receção. Se os scripts ou mapas de abertura mudarem, a gravação tem de ser refeita.

Duas armadilhas já conhecidas: o ecrã de escolha do inicial bloqueia se for aberto fora do laboratório (por isso não há cenário `HACK_TEST` para ele), e uma ROM normal compilada logo a seguir a uma de teste não arranca se a base não for reextraída (o `test.sh` trata disso ao tocar em `rom.nds`).

Uma feature nova deve trazer o seu cenário: um `HACK_TEST_*` em `include/hack_test.h`, o estado em `HackTest_Setup` e a função `test_*` no runner. Nada disto entra nas ROMs normais: está tudo dentro de `#ifdef HACK_TEST`.

## Regras do repositório

- Cada feature do hack tem um `#define HACK_*` em `include/hack_config.h` e o código fica dentro de `#ifdef`. Assim é fácil desligar, rever e fazer merge com o upstream.
- Flags e variáveis novas ficam registadas na tabela abaixo antes de serem usadas.
- Atualizar o engine: `git fetch upstream && git merge upstream/main` dentro de `hack/main`.

## Flags, variáveis e scripts usados

| Recurso | Valor | Uso |
|---|---|---|
| Flag | 2600, 2601 | engine: hidden abilities |
| Flag | 2602 | `FLAG_EXP_SHARE_DISABLED` (Exp Share de Kalos desligada) |
| Flag diária | 2900 a 2910 | Pokémon estáticos visíveis; são repostas à meia-noite com as outras flags diárias |
| Flag diária | 2911 | só nos testes: escolhe o combate de líder no script comum 2073 |
| Script comum | 2073 | engine: script de debug; em `HACK_TEST` lança a batalha de teste |
| Script comum | 2074 | liga/desliga a Exp Share |
| Script comum | 2075 | só faz algo em `HACK_TEST` (loja do 4.º andar de Goldenrod); na ROM normal é um script vazio, para a numeração ser igual |
| Flags | 2200 a 2399, 2522 a 2594, 2603 a 2719 | reserva para os especialistas de espécie (uma por especialista, atribuídas pelo gerador) |
| Flags | 2098 a 2199 | flags de "treinador vencido" dos treinadores novos (1360 + número do treinador): não usar para mais nada |
| Flags | 2595 a 2599 | recrutas Rocket extra (vencido) |
| Flags | 1340 a 1346 | objetos da história por regra (`include/hack_story.h`); 1347 a 1359 livres, 1311 a 1339 também sem uso no jogo original |
| Flags diárias | 2880, 2881 | assalto ao Poké Mart e Crasher Wake já feitos hoje |
| Treinadores | 745 a 748 | assaltantes dos Poké Marts e Crasher Wake |
| Scripts comuns | 2080, 2081 | assalto ao Poké Mart: antes e depois da batalha (o próximo livre é o 2082) |
| Texto 040 | 134 a 136 | assalto ao Poké Mart |
| Texto 131 | 28 a 31 | Giovanni em Tohjo Falls |
| Texto 626 | 36 a 39 | Crasher Wake no Lago da Fúria |
| Flag | 2594 | Korrina: Key Stone entregue |
| Treinador | 744 | Korrina |
| Texto 094 | 13 a 19 | Korrina no topo do Farol de Olivine |
| Treinadores | 739 a 743 | recrutas Rocket extra (`hack/scripts/gen_trainer_teams.py`) |
| Treinador | 738 | `TRAINER_HACK_MIRROR`: especialista genérico |
| Var | 0x416F | `HACK_VAR_MIRROR_WINS`: especialistas vencidos |
| Script comum | 2077 | especialista de espécie (chamado com `callstd` pelos scripts dos mapas) |
| Script comum | 2078, 2079 | falas dos recrutas Rocket extra, antes e depois da batalha |
| Script comum | 2076 | prompt "adicionar à equipa" depois de apanhar com a equipa cheia (o próximo livre é o 2077) |
| Comando de script | 690 (`day_care_sanitize_mon`) | operações do hack conforme o valor da var de resultado à entrada: 0x4843 troca do prompt pós-captura; 0x4D30 a 0x4D32 mirror match (procurar espécie, começar, terminar) |
| Texto 040 | 121, 122 | mensagens da Exp Share |
| Texto 040 | 131 a 133 | recrutas Rocket extra |
| Texto 040 | 126 a 130 | especialistas de espécie |
| Texto 040 | 123 a 125 | prompt pós-captura (pergunta, troca feita, recusa por Mail) |
| Texto 830 | 217 | descrição da Exp Share (item-chave) |
| Texto 300 | 226 | mensagem dos Bottle Caps |
| Field use func | 36 | `ItemMenuUseFunc_ExpShare` |
| Hook arm9 | 0206CCC4 | `Daycare_GetCompatibility_Hack` (Oval Charm) |
| Hook arm9 | 0206C274 | `Daycare_SetPendingEgg_Hack` (Shiny Charm em ovos) |
| Bytes arm9 | 0205D674, 0205D678 | velocidades da bicicleta (`HACK_FAST_BIKE`, em `bytereplacement`) |
