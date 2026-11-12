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

## Testes em jogo

`hack/scripts/test.sh` compila uma ROM de debug (`make HACK_TEST=Y`, guardada em `hack/out/test-debug.nds`) e corre `hack/scripts/ingame_tests.py` no DeSmuME sem janela. A ROM de debug continua o save automaticamente (por omissão o save de testes público do hg-engine, descarregado para `hack/out/test.sav`; `HG_TEST_SAV` aponta para outro).

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
| Script comum | 2073 | engine: script de debug; em `HACK_TEST` lança a batalha de teste |
| Script comum | 2074 | liga/desliga a Exp Share |
| Script comum | 2075 | só em `HACK_TEST`: loja do 4.º andar de Goldenrod (o próximo script do hack é o 2076) |
| Texto 040 | 121, 122 | mensagens da Exp Share |
| Texto 830 | 217 | descrição da Exp Share (item-chave) |
| Texto 300 | 226 | mensagem dos Bottle Caps |
| Field use func | 36 | `ItemMenuUseFunc_ExpShare` |
| Hook arm9 | 0206CCC4 | `Daycare_GetCompatibility_Hack` (Oval Charm) |
| Hook arm9 | 0206C274 | `Daycare_SetPendingEgg_Hack` (Shiny Charm em ovos) |
| Bytes arm9 | 0205D674, 0205D678 | velocidades da bicicleta (`HACK_FAST_BIKE`, em `bytereplacement`) |
