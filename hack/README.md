# Rom hack HeartGold: pipeline

Fork do [hg-engine](https://github.com/BluRosie/hg-engine). Todo o trabalho do hack vive no branch `hack/main`, por cima do engine.

## Fluxo

```
ROM base (HeartGold U, IPKE, nunca vai para o git)
   │
   ├─ include/hack_config.h      toggles de todas as features do hack (HACK_*)
   ├─ include/config.h           opções do engine (EXP, shinies, level cap, HMs...)
   ├─ src/                       mecânicas em C (cada alteração dentro de #ifdef HACK_*)
   ├─ data/*.c                   Pokémon, encontros, treinadores, itens, lojas
   ├─ data/text/*.txt            textos
   ├─ data/scr_seq/*.s           scripts (comuns agora; história na Fase 2)
   │
   ▼
hack/scripts/release.sh  =  build.sh  →  verify.py  →  package.sh
   │                          make        arranque no     .zip + .xdelta
   │                                      DeSmuME
   ▼
hack/out/HeartGold-hack-<versão>.zip / .xdelta
```

## Comandos

```bash
# primeira vez (macOS): dependências do README do hg-engine (brew + gcc-arm-embedded + rustup)
hack/scripts/release.sh ~/ROMs/HeartGold_US.nds fase1   # pipeline completo
hack/scripts/build.sh                                   # só compilar (usa o rom.nds já copiado)
.venv/bin/python hack/scripts/verify.py                 # só o teste de arranque
hack/scripts/package.sh fase1                           # só empacotar
```

Para partilhar o hack, usa só o `.xdelta` (aplica-se com Delta Patcher ou xdelta UI sobre a ROM original). Nunca distribuas o `.nds`. As regras do hg-engine proíbem qualquer tipo de monetização e obrigam a replicar `CREDITS.md`.

## Regras do repositório

- Cada feature do hack tem um `#define HACK_*` em `include/hack_config.h` e o código fica dentro de `#ifdef`. Assim é fácil desligar, rever e fazer merge com o upstream.
- Flags e variáveis novas ficam registadas na tabela abaixo antes de serem usadas.
- Atualizar o engine: `git fetch upstream && git merge upstream/main` dentro de `hack/main`.

## Flags, variáveis e scripts usados

| Recurso | Valor | Uso |
|---|---|---|
| Flag | 2600, 2601 | engine: hidden abilities |
| Flag | 2602 | `FLAG_EXP_SHARE_DISABLED` (Exp Share de Kalos desligada) |
| Var | 0x416F | `LEVEL_CAP_VARIABLE`: se for diferente de 0, substitui o cap por insígnias |
| Script comum | 2074 | liga/desliga a Exp Share |
| Texto 040 | 121, 122 | mensagens da Exp Share |
| Texto 300 | 226 | mensagem dos Bottle Caps |
| Field use func | 36 | `ItemMenuUseFunc_ExpShare` |
