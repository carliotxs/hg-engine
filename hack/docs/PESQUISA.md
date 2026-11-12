# Pesquisa: sprites de treinadores, overworlds, multi-região e eventos temporais (HeartGold / hg-engine)

Data da pesquisa: 2026-11-12. Âmbito: hack não comercial de Pokémon HeartGold sobre o hg-engine.

Convenções deste documento:

- Cada afirmação tem a fonte ao lado. "Local:" indica um ficheiro do próprio repositório hg-engine (verificado em disco, só leitura), com o URL equivalente no GitHub quando existe.
- "Não verificado" significa que não consegui confirmar numa fonte primária. Não é um palpite disfarçado.
- Limitações de acesso: o PokéCommunity e o The Spriters Resource devolveram HTTP 403 a pedidos automáticos, por isso o que digo sobre esses sites vem de resumos de motores de busca e não da leitura direta das páginas. Duas páginas do TCRF (tcrf.net) devolveram texto com instruções dirigidas a agentes automáticos (pagamentos, criar ficheiros); ignorei esse conteúdo e não usei essas páginas como fonte.
- Não foram descarregados ROMs nem packs de recursos. Só descarreguei cinco PNG individuais de 80x80 do índice público do Pokémon Showdown para medir dimensões e número de cores.

---

## 1. Sprites de treinadores para personagens que não existem no HeartGold

### 1.1 Resposta curta para a Korrina

| Asset | Existe em estilo Gen 4/5 (DS)? | Onde | Termos |
|---|---|---|---|
| Sprite de batalha (frente) 80x80 | **Sim** | `korrina.png` no índice de treinadores do Pokémon Showdown, creditado a **Gnomowladny**. https://play.pokemonshowdown.com/sprites/trainers/ (ficheiro: https://play.pokemonshowdown.com/sprites/trainers/korrina.png) | Showdown: "Credit must be given to the appropriate artist if used elsewhere. DO NOT EDIT without permission." (mesma página). O original no DeviantArt (100x100, 2014) diz: "Feel free to use it if you like, but don't forget to give me credit". https://www.deviantart.com/gnomowladny/art/Korrina-Sprite-488498591 |
| Sprite de batalha, versão Pokémon Masters | Sim (`korrina-masters.png`, por kyledove) | https://play.pokemonshowdown.com/sprites/trainers/ | Mesma regra do Showdown |
| Overworld 32x32, 4 direções, estilo Gen 4 | **Não encontrei nenhum** | Procurei em Eevee Expo, DeviantArt, PokéCommunity (via pesquisa) e packs de Kalos. O pack de Kalos mais próximo (Taiga) não lista a Korrina. https://eeveeexpo.com/resources/1125/ | n/a |

Notas técnicas sobre o sprite de batalha da Korrina (medido por mim no PNG público):

- É 80x80 com paleta indexada, mas usa **46 cores**. O formato Gen 4 exige 16 cores (15 mais transparência), por isso é preciso reduzir a paleta. Reduzir cores é uma edição, e a regra do Showdown pede autorização para editar. O texto do artista no DeviantArt é mais permissivo (uso livre com crédito), mas não fala explicitamente de edições. Recomendo pedir autorização ao Gnomowladny por nota no DeviantArt antes de publicar. Fontes: https://play.pokemonshowdown.com/sprites/trainers/ e https://www.deviantart.com/gnomowladny/art/Korrina-Sprite-488498591
- É uma única pose. No HGSS o sprite de treinador tem vários frames de animação (o exemplo local da Cynthia é uma folha de 80x400, ou seja 5 frames). Um sprite de um só frame funciona se a animação repetir o mesmo frame. Local: `data/graphics/trainer_gfx/137.png`; guia: https://github.com/BluRosie/hg-engine/wiki/Adding-New-Trainer-Classes

Conclusão para a Korrina: a batalha está resolvida com crédito (e idealmente um pedido de autorização para a redução de cores). O overworld tem de ser feito de raiz ou encomendado. A via mais barata é editar um overworld Gen 4 existente de rapariga loura com rabo de cavalo, ou usar como base os overworlds de Kalos do pack da Taiga (ver 1.3), respeitando os créditos.

### 1.2 Fontes de sprites de batalha (frente, 80x80)

**A. Índice de treinadores do Pokémon Showdown (a melhor fonte única)**
https://play.pokemonshowdown.com/sprites/trainers/

- Conteúdo: cerca de 1500 sprites de treinador em PNG 80x80, misturando sprites oficiais (Gen 1 a 5) com sprites feitos por fãs em estilo Gen 5 para personagens das gerações 6 a 9. Contagem por artista feita por mim na página: kyledove 619, Brumirage 75, Beliot419 57, ZacWeavile 47, Gnomowladny 27, Horo 9, Grapo 7, hyo-oppa 4, e cerca de 650 sem crédito (os oficiais).
- Formato: PNG 80x80 indexado. O número de cores varia (medi 18 na Diantha, 19 no Lysandre, 24 no Sycamore, 34 no Steven Gen 6, 46 na Korrina), logo quase todos precisam de redução para 16 cores.
- Termos (texto da própria página): "Many of these sprites are not from the games. Credit must be given to the appropriate artist if used elsewhere. DO NOT EDIT without permission."
- Só batalha, sem overworlds.

Personagens pedidas, tal como aparecem nesse índice:

| Personagem | Ficheiro e crédito no índice | Observação |
|---|---|---|
| Korrina | `korrina` por Gnomowladny; `korrina-masters` por kyledove | Feito por fã |
| Diantha | `diantha` por Brumirage; `diantha-masters`, `diantha-masters2` por kyledove | Feito por fã |
| Sycamore | `sycamore` por kyledove; `sycamore-masters` por kyledove | Feito por fã |
| Steven | `steven` e `steven-gen3` sem crédito (oficiais); `steven-gen6` por ZacWeavile; cinco variantes Masters por kyledove | O HG original não tem sprite de batalha do Steven (ver 1.5) |
| Cynthia | `cynthia`, `cynthia-gen4` sem crédito (oficiais); `cynthia-gen7` e `cynthia-masters` por Brumirage; outras por kyledove | Já existe no HG (classe 137) |
| N | `n` sem crédito (oficial Gen 5); `n-masters` 1 a 3 por kyledove | Oficial Gen 5, 80x80 |
| Ghetsis | `ghetsis`, `ghetsis-gen5bw` sem crédito (oficiais Gen 5) | Oficial Gen 5 |
| Cyrus | `cyrus` sem crédito (oficial Gen 4); `cyrus-masters` por kyledove | Não existe no HG (ver 1.5) |
| Crasher Wake | `crasherwake` sem crédito (oficial Gen 4) | Já existe no HG (classe 132) |
| Outros Kalos | Viola, Ramos, Valerie, Olympia, Wulfric, Malva, Siebold, Wikstrom, Drasna, AZ, Tierno por Gnomowladny; Grant, Lysandre, Serena, Trevor por kyledove; Calem por Brumirage; Shauna, Emma por ZacWeavile; Clemont sem crédito | Liga de Kalos praticamente completa |

Fonte de toda a tabela: https://play.pokemonshowdown.com/sprites/trainers/

Aviso: os sprites "sem crédito" são rips dos jogos oficiais (propriedade da Nintendo/Game Freak). A regra de crédito do Showdown não os cobre. Isto é o risco normal de qualquer rom hack e não muda por virem deste índice.

**B. Galerias dos próprios artistas (para pedir autorização ou obter o original)**

- Gnomowladny (DeviantArt): galeria de sprites de treinadores, com a Korrina de 2014 e ligações a Viola, Malva, Wallace, entre outros. Termo no post da Korrina: uso livre com crédito. https://www.deviantart.com/gnomowladny/art/Korrina-Sprite-488498591
- kyledove, Brumirage, Beliot419, ZacWeavile: não consegui abrir as páginas individuais com os termos de cada um. Não verificado para além da regra geral do Showdown acima.

**C. Mr. Gela, "Gen 4 and 5 Trainer sprites and PBS" (Eevee Expo)**
https://eeveeexpo.com/resources/391/

- Conteúdo: 179 tipos de treinador de DP até B2W2 (sprites oficiais organizados), com ficheiro PBS para Pokémon Essentials. Exclui a maior parte dos protagonistas e algumas personagens; revisores apontam sprites em falta.
- Formato: PNG para RPG Maker XP. Dimensões não indicadas na página.
- Termos: creditar "Mr. Gela/theo#7722"; **não redistribuir** o pack noutro local (ligar à página).
- Utilidade para este hack: baixa. São sprites oficiais Gen 4/5 que o HG já tem ou que se obtêm do Showdown. Não tem Kalos.

**D. Poltergeist / Coffee Cup, pack de personalização Gen 4 (Eevee Expo)**
https://www.eeveeexpo.com/resources/317

- Conteúdo: peças modulares (roupa, cabelo, pele) para montar personagens em estilo Gen 4, com frente, costas e overworld (andar, correr, bicicleta). Não tem personagens nomeadas.
- Termos: "freely edit, use and share the files"; crédito "appreciated but not necessary".
- Utilidade: boa base livre para construir um overworld e um sprite de batalha originais com o mesmo estilo, sem restrições de edição.

**E. "DS-style 64x64 Trainer Sprite Resource" e "L96's 64x64 Trainer Sprite Resource" (PokéCommunity)**
https://www.pokecommunity.com/threads/the-ds-style-64x64-trainer-sprite-resource.308798/ e https://www.pokecommunity.com/threads/l96s-64x64-trainer-sprite-resource.312440/

- São projetos de sprites de treinador em estilo DS **reduzidos para 64x64**, pensados para hacks de GBA (Gen 3). O segundo pede crédito ao autor.
- Não verificado diretamente (403). Pelo título e pelos resumos, o tamanho 64x64 não serve para o Gen 4, que usa 80x80. Só serviriam ampliados, o que degrada a qualidade. Não os recomendo.

**F. Smogon Sprite Project**
https://www.smogon.com/forums/threads/the-gen-4-style-gen-5-and-beyond-backsprite-resource.3687625/ e https://github.com/smogon/sprites

- O projeto de sprites do Smogon trata de sprites de Pokémon, não de treinadores. O recurso "Gen 4-Style Gen 5 and Beyond Backsprite" (PorousMist) é de backsprites de Pokémon em estilo Gen 4. Os sprites de treinador do Showdown são a parte relevante (fonte A).

**G. The Spriters Resource (HGSS e Platinum)**
https://www.spriters-resource.com/ds_dsi/pokemonheartgoldsoulsilver/

- Tem folhas com os treinadores e os overworlds oficiais de HGSS (40 assets segundo o resumo da pesquisa). Não verificado diretamente (403). São rips oficiais, sem licença de reutilização. Para este hack são redundantes: o hg-engine já extrai tudo do ROM para `data/graphics/` (ver 2).

**H. Encomendas**
Há vendedores no Fiverr que fazem folhas de overworld Gen 4 por encomenda, por exemplo https://fiverr.com/ejayfernandez/create-gen-4-custom-pokemon-overworld-trainer-sprite-sheet. Não avaliei qualidade nem preços.

### 1.3 Fontes de overworlds em estilo Gen 4

| Fonte | Conteúdo | Formato | Termos |
|---|---|---|---|
| VanillaSunshine, "ALL Official Gen 4 Overworld Sprites" https://www.eeveeexpo.com/resources/404 | Todos os overworlds de treinadores e NPC de HGSS e DPPt (inclui líderes e Elite Four), mais overworlds originais para treinadores cujo overworld oficial não corresponde ao sprite de batalha | RMXP (folhas 4x4) | Creditar todos (Neo-Spriteman, VanillaSunshine, PurpleZaffre e Maicerochico, AtomicReactor); **não redistribuir** |
| DiegoWT, "Gen 5 Characters in Gen 4 OW style 2.0" https://eeveeexpo.com/resources/370/ | Personagens de Unova em estilo Gen 4: **N, Ghetsis**, Colress, Shadow Triad, Alder, Marshal, Roxie, Elesa, Cilan, Hugh, Bianca, Cheren, protagonistas, Yancy, Curtis | RMXP; duas organizações de ficheiros | Crédito obrigatório mesmo usando só partes; **não redistribuir** |
| Taiga, "Trainer Collection (X/Y)" https://eeveeexpo.com/resources/1125/ | Overworlds de treinadores e NPC de **Kalos**. Nomes citados nos créditos: Grant, Olympia, Lysandre, Calem, Serena, AZ, Viola, **Diantha**, Ramos. Em falta segundo o autor: Mãe, Mega Evolution Guru, Battle Chatelaines. **Korrina e Sycamore não são mencionados** | RMXP; download externo | Sem licença explícita; lista de créditos por personagem (izzyvicious, Mademoiselle--Serena, PizzaSun, tebited15, Wolfgang62, Somersault, mais os autores do pack Gen 4). Estilo declarado: não indicado na página, mas cita o pack Gen 4 como base. Abrir o ficheiro para confirmar o conteúdo real |
| TwentyExEx / Horo, "Pokémon World Summit Overworlds" https://eeveeexpo.com/resources/996/ | Protagonistas, líderes, Elite Four, campeões e outros treinadores das gerações 4 a 8 | **Estilo FRLG (Gen 3)**, não Gen 4 | Crédito obrigatório a Horo e à equipa World Summit |
| Mega Greninja, "Pokemon Recruitment Resource Pack" https://www.eeveeexpo.com/resources/1192 | Overworlds, battlers, retratos e tilesets Gen 4 (floresta, gruta, QG Galáctico) de um fangame | Não indicado | Sem termos explícitos; créditos a quatro autores |
| Lime029 (DeviantArt), "Kalos Punk Guy Overworld Sprite (Gen IV Style)" https://www.deviantart.com/lime029/art/Kalos-Punk-Guy-Overworld-Sprite-Gen-IV-Style-901998571 | Um NPC de Kalos em estilo Gen 4 | PNG | Não verificado |

Ponto importante sobre o formato: estes packs são para RPG Maker XP (folha 4 colunas por 4 linhas). O HGSS guarda cada overworld como uma tira vertical de frames 32x32 numa ordem fixa. O Steven local (`0059.png`) é uma imagem 32x384 de 4 bits com 16 nomes de frame. É preciso reorganizar os frames e reduzir a 16 cores. Local: `data/graphics/overworlds/0059.png` e `0059.json`; guia: https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/hgss-new_overworlds

Sobre "não redistribuir": os autores proíbem republicar o pack. Incluir sprites convertidos dentro de um patch de rom hack com crédito é a prática habitual, mas não está escrito nessas páginas que é permitido. Em caso de dúvida, perguntar ao autor.

### 1.4 Resumo por personagem

| Personagem | Batalha 80x80 | Overworld estilo Gen 4 |
|---|---|---|
| Korrina | Sim, fã (Gnomowladny), Showdown | **Não encontrado** |
| Diantha | Sim, fã (Brumirage), Showdown | Provável no pack da Taiga (citada nos créditos); confirmar no ficheiro |
| Sycamore | Sim, fã (kyledove), Showdown | Não encontrado |
| Steven | Oficial Gen 3 e fã Gen 6 (ZacWeavile), Showdown | **Já existe no HG** (`0059-daigo`) |
| Cynthia | **Já existe no HG** (classe 137) | **Já existe no HG** (`0060-champion`) |
| N | Oficial Gen 5 80x80, Showdown | Sim, DiegoWT |
| Ghetsis | Oficial Gen 5 80x80, Showdown | Sim, DiegoWT |
| Cyrus | Oficial Gen 4 (DPPt), Showdown | Oficial DPPt no pack do VanillaSunshine; não existe no HG |
| Crasher Wake e restantes líderes de Sinnoh | **Já existem no HG** (classes 129 a 136) | Existem ficheiros `leader1` a `leader8` no HG (ver 1.5) |

Fontes: https://play.pokemonshowdown.com/sprites/trainers/ , https://eeveeexpo.com/resources/370/ , https://eeveeexpo.com/resources/1125/ , https://www.eeveeexpo.com/resources/404 , e ficheiros locais indicados em 1.5.

### 1.5 Personagens de Sinnoh e Hoenn que já estão nos dados do HeartGold

A fonte mais fiável é a própria lista de classes de treinador extraída do jogo. Local: `include/constants/trainerclass.h`; no GitHub: https://github.com/BluRosie/hg-engine/blob/main/include/constants/trainerclass.h

Classes de treinador com sprite de batalha presentes (cada uma tem `NNN_enc.png` em `data/graphics/trainer_gfx/`, classes 0 a 137):

- Líderes de Sinnoh: Roark (129), Gardenia (130), Maylene (131), **Crasher Wake (132)**, Fantina (133), Byron (134), Candice (135), Volkner (136).
- **Campeã Cynthia (137)**.
- Parceiros de Sinnoh: Cheryl (90), Riley (91), Marley (92), Buck (93), Mira (94).
- Protagonistas de Sinnoh: Lucas e Dawn em versão Frontier (95, 96), DP (125, 126) e Pt (127, 128).
- Cérebros da Battle Frontier: Tower Tycoon (97), Hall Matron (99), Factory Head (100), Arcade Star (101), Castle Valet (102).

Não aparecem nessa lista: Steven, Cyrus, Team Galactic, Elite Four de Sinnoh. Ou seja, **o HG original não tem sprite de batalha para Steven nem Cyrus**. Fonte: mesma lista.

Overworlds presentes no arquivo a/0/8/1 (nomes internos dos ficheiros de paleta, local: `data/graphics/overworlds/`; no GitHub: https://github.com/BluRosie/hg-engine/tree/main/data/graphics/overworlds):

- `0059-daigo` (Daigo é o nome japonês do Steven) e `0060-champion` (vi a imagem: cabelo louro comprido e roupa preta, é a Cynthia). O jogo usa-os: existem as flags `FLAG_HIDE_VERMILION_CITY_STEVEN`, `FLAG_HIDE_PEWTER_CITY_STEVEN` e `FLAG_HIDE_SINJOH_MYSTRI_SHRINE_CYNTHIA` nos scripts (local: `data/scr_seq/scr_seq_0149.s`).
- `0061-towerboss`, `0103` a `0106` (`brains1` a `brains4`), `0062` a `0066` (`seven1` a `seven5`, os cinco parceiros de Sinnoh).
- `0215` a `0222` (`leader1` a `leader8`), distintos dos `gsleader1` a `gsleader16` (Johto e Kanto). Pelo nome herdado de DP devem ser os oito líderes de Sinnoh. Abri o `0218` e mostra uma personagem de cabelo rosa, compatível com a Maylene. Não confirmei os oito um a um.
- Não há ficheiro com nome associado ao Cyrus ou à Team Galactic entre os primeiros 265 overworlds (não verificado para além dos nomes dos ficheiros).

Para que servem as classes de Sinnoh no HG (batalhas por ligação, Frontier, ou simples herança do Platinum): não verificado.

---

## 2. Como se adicionam overworlds e sprites de batalha num hack de HeartGold

### 2.1 Com o hg-engine (o caminho recomendado para este projeto)

O hg-engine tem documentação própria para ambos os casos e compila os gráficos a partir de PNG e JSON, sem editores binários.

**Nova classe de treinador com sprite próprio**
Guia oficial: https://github.com/BluRosie/hg-engine/wiki/Adding-New-Trainer-Classes (cópia local: `documentation/wiki/Adding-New-Trainer-Classes.md`)

- O engine tem espaço para cerca de 120 classes novas, cada uma com sprite próprio, sem substituir classes existentes.
- Passos em alto nível:
  1. Definir a constante `TRAINERCLASS_*` em `include/constants/trainerclass.h` e em `armips/include/constants.s`.
  2. Dar nome à classe em `data/text/730.txt` e `data/text/731.txt` (nome com artigo).
  3. Acrescentar entradas nas tabelas: género (`sTrainerGenders` em `src/pokemon.c`), prémio (`PrizeMoney` em `src/trainermoney.c`), música e animação de introdução (`src/music_tables.c`), e ajustar os tamanhos correspondentes em `bytereplacement`.
  4. Colocar os gráficos em `data/graphics/trainer_gfx/` com o número da classe: `NNN_enc.png` (imagem de encontro, 160x80, dois primeiros frames, indexada), `NNN_enc.png.key` (copiado de outro sprite), `NNN.png` (todos os frames em tiles, 80 de largura por 80 vezes o número de frames), `NNN_cell.json` (dados NCER) e `NNN_anim.json` (dados NANR). Os JSON podem ser copiados de um sprite existente.
  5. `make`.
- Ferramentas: Aseprite para indexar, `./tools/nitrogfx` (incluído) para converter NCGR/NCLR/NCER/NANR, Tinke para ver e ajustar células OAM. O guia recomenda manter frames de 80x80.
- Ajuda: o guia remete para os servidores Discord KoDSH e DSMC.

**Novo overworld (NPC)**
Guia: https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/hgss-new_overworlds (referido no rodapé de https://github.com/BluRosie/hg-engine/wiki/Overworld-System-Documentation; cópia local: `documentation/wiki/Overworld-System-Documentation.md`)

- O engine extrai todos os overworlds para `data/graphics/overworlds/` como `NNNN.png`, `NNNN.json` e `NNNN-nome.pal` (JASC-PAL), e reconstrói o arquivo `a/0/8/1` (`pokemonow.narc`).
- O número que o DSPRE mostra não é o índice no arquivo: há uma tabela de "tags" `gOWTagToFileNum` em `src/field/overworld_table.c`, com `tag`, `gfx` e `callback_params` por entrada.
- Passos em alto nível:
  1. Desenhar a folha e indexar a 16 cores (PNG de 4 bits, obrigatório; cor 0 transparente).
  2. Copiar o JSON e o PNG de um overworld existente para uma subpasta própria, com número novo, e exportar a paleta por cima do `.pal`. Manter a ordem dos frames; nomes de frame e paleta têm no máximo 16 caracteres ASCII.
  3. Em `overworld_table.c`, definir `NEW_NPC_START` (sugestão do guia: 7000, máximo 8192), `NEW_NPC_GFX_START` (primeiro gfx livre; à data do guia o último usado era 1457) e acrescentar `NEW_NPC_ENTRY(n)`.
  4. Acrescentar as regras em `narcs.mk` para a subpasta (variáveis `OVERWORLDS_<NOME>_SRCS` e `_OBJS`).
  5. `make`, e colocar o NPC no mapa pelo número da tag (no DSPRE ou diretamente nos ficheiros de eventos).
- Frames: 32x32 nos NPC normais (o engine também tem 64x64 para Pokémon grandes). Largura e altura têm de ser potências de 2.

### 2.2 Sem hg-engine (edição binária clássica)

Guia: https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/overworld_sprites

- Ferramentas: Tinke 0.9.2 (extrair e repor BTX), BTX Editor 2.0 (PNG para BTX), DSPRE (Overworld Editor e overlays), editor hexadecimal.
- Arquivos: overworlds em `a/0/8/1` no HGSS e `mmodel/mmodel.narc` em DPPt.
- O DSPRE só importa PNG com as mesmas dimensões e número de frames do original. Mudar tamanho ou frames exige editar a tabela de propriedades no Overlay 1 (offset `0x21BA8` na versão US).
- O guia diz que **adicionar** overworlds novos por esta via exige ASM e sugere reaproveitar sprites não usados. É exatamente o que o hg-engine resolve.
- Sprites de batalha por via binária: são quatro ficheiros por classe (NCGR, NCLR, NCER, NANR) editados com Tinke ou NitroPaint (https://github.com/Garhoogin/NitroPaint). O VSMaker2 (https://github.com/Chvlkie/VSMaker2) é a ferramenta listada para batalhas de treinador. Lista de ferramentas: https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/getting_started/

### 2.3 DSPRE e hg-engine

O DSPRE declara suporte **parcial** para ROMs hg-engine, com alguns editores desativados. Serve para mapas, eventos, matrizes e cabeçalhos, mas os dados que o hg-engine compila a partir de texto (treinadores, Pokémon, overworlds) devem ser editados no repositório e não no DSPRE. https://github.com/DS-Pokemon-Rom-Editor/DSPRE

### 2.4 Melhores tutoriais

- Classes de treinador (hg-engine): https://github.com/BluRosie/hg-engine/wiki/Adding-New-Trainer-Classes
- Overworlds novos (hg-engine): https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/hgss-new_overworlds
- Sistema de overworlds (hg-engine): https://github.com/BluRosie/hg-engine/wiki/Overworld-System-Documentation
- Substituição de overworlds (binário): https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/overworld_sprites
- Ferramentas Gen 4: https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/getting_started/

---

## 3. Hacks multi-região em Gen 4

### 3.1 Precedentes

- **Pokémon Iridium**: hack sobre HeartGold construído com hg-engine, com duas regiões novas feitas de raiz e história nova. Em desenvolvimento desde pelo menos 2024, com demo anunciada em 2025 a cobrir apenas o primeiro ginásio (cerca de 25 combates) e um plano de 12 a 14 divisões entre as duas regiões. O próprio autor estimou "mais de um ano". Fonte: publicações do autor (u/InsipidAxiom) em r/PokemonROMhacks, por exemplo https://www.reddit.com/r/PokemonROMhacks/comments/1kqnzdl/ e https://www.reddit.com/r/PokemonROMhacks/comments/1fgbwqe/ (li resumos de espelhos, não as páginas originais). É o precedente mais próximo, mas **substitui** Johto e Kanto por duas regiões novas; não é uma terceira região.
- **Pokémon Light Platinum DS** (Mikelan98): recriação em HeartGold do hack de GBA Light Platinum (regiões Zhery e Lauren no original). Ficou em beta (referência a uma versão 0.2.1) e o link oficial foi retirado a pedido do autor. https://gamebrew.org/wiki/Pokemon_Light_Platinum_DS e https://www.pokecommunity.com/threads/english-beta-released-pok%C3%A9mon-light-platinum-nds.305765/ (o segundo não verificado diretamente)
- **Mapa de Hoenn no Pokégear do HGSS**: o guia de edição do Town Map (autor BluRose, o mesmo do hg-engine) usa como exemplo a substituição de Johto e parte de Kanto por Hoenn, com rotas por fazer. Prova que redesenhar o mapa da região é viável, mas reaproveitando a grelha existente. https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/hgss-town_map
- **pokemon-apocrypha**: projeto que planeou várias regiões sobre a decompilação `pokeheartgold`, fez uma auditoria dos pressupostos de região única e depois **abandonou o motor HGSS** (em 2026-09-10) a favor do pokeemerald-expansion (GBA). https://github.com/Davisfox5/pokemon-apocrypha/pull/2
- **Terceira região acrescentada a Johto mais Kanto, ou Sinnoh/Hoenn/Kalos portados para HGSS e lançados**: não encontrei nenhum hack lançado que o tenha feito. Não verificado que não exista; apenas não apareceu em nenhuma pesquisa.

### 3.2 Limites técnicos conhecidos

| Área | O que se sabe | Fonte |
|---|---|---|
| Cabeçalhos de mapa (headers) | No DSPRE, adicionar cabeçalhos exige o patch "Dynamic Headers". Na auditoria sobre a decompilação, o número de cabeçalhos não tem teto (`sMapHeaders[]` cresce livremente, `mapId` é `u32`) | https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/mapping/mapping_faqs ; https://github.com/DS-Pokemon-Rom-Editor/DSPRE ; https://github.com/Davisfox5/pokemon-apocrypha/pull/2 |
| Matrizes | `MAP_MATRIX_MAX_SIZE = 799` é por matriz, não global. O DSPRE tem o patch "Expand Matrix 0" para a matriz do mundo | mesmas fontes |
| Identidade de região | O cabeçalho tem **1 bit** de região (`regionNo : 1` na decompilação atual; a auditoria chama-lhe `isKanto`). Uma terceira região obriga a alargar o campo e rever o código que o lê | https://github.com/pret/pokeheartgold/blob/master/include/map_header.h ; https://github.com/Davisfox5/pokemon-apocrypha/pull/2 |
| Secções de mapa (mapsec: nomes de local, local de captura) | Campo de **8 bits**. Na decompilação as constantes vão até 234 (`MAPSEC_CLIFF_EDGE_GATE`), ou seja 235 de 256 usadas, cerca de 21 livres. A auditoria nota que as secções de Sinnoh já existem por herança do motor DP, e classifica este limite como a alteração estrutural mais grave para acrescentar outras regiões | https://github.com/pret/pokeheartgold/blob/master/include/constants/map_sections.h ; https://github.com/pret/pokeheartgold/blob/master/include/map_header.h ; https://github.com/Davisfox5/pokemon-apocrypha/pull/2 |
| Town Map, Fly e Pokégear | `worldMapX` e `worldMapY` têm 6 bits cada (grelha única de 64x64). Cada célula selecionável do Pokégear corresponde a um bloco de mapa 32x32, e o Kanto original já foi comprimido para caber. Gráficos em `/a/1/4/4`, 20 slots de pré-visualização de cidade, tabelas no Overlay 101 (cidades e seleção) e tabela `FlyRespawnPosition` no ARM9 (`0xF9E80`), limitadores de área no Overlay 10. O guia não explica como passar da grelha existente nem dos 20 slots | https://github.com/pret/pokeheartgold/blob/master/include/map_header.h ; https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/hgss-town_map |
| Ferramenta de mapa e Fly | Raven Town Map Editor, para mapas personalizados e destinos de Fly em D/P/Pt/HG/SS | https://github.com/RavenDS/town-map-editor |
| Area data e tilesets | Cada cabeçalho aponta para um "area data" que referencia o pack de texturas de mapa (`.nsbtx`), o pack de texturas de edifícios e, só em HGSS, um ficheiro de animação global (`.nsbta`). `areaDataBank` é `u8` na decompilação, logo no máximo 256 entradas (quantas estão usadas: não verificado) | https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/mapping ; https://github.com/pret/pokeheartgold/blob/master/include/map_header.h |
| Desempenho 3D por mapa | Orientação: menos de 1000 polígonos por mapa, 2000 no total com edifícios e sprites; até quatro mapas adjacentes carregados em simultâneo; cada mapa é um modelo 32x32 células | https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/mapping |
| Dados por cabeçalho no HGSS | Ficheiros de headbutt estão indexados pelo cabeçalho, e as tabelas de enxames guardam IDs de cabeçalho. Cabeçalhos novos precisam dos ficheiros correspondentes | https://github.com/DS-Pokemon-Rom-Editor/DSPRE/issues/297 ; https://github.com/DS-Pokemon-Rom-Editor/DSPRE/issues/270 |
| Tamanho do ROM | Cartuchos DS vão de 8 a 512 MB (Wikipedia). O ROM base local tem 128 MiB (`rom.nds`, 134217728 bytes) e existe um build local de 256 MiB (`test.nds`), portanto há margem. Não verifiquei como o hg-engine define a capacidade | https://en.wikipedia.org/wiki/Nintendo_game_card ; local |
| Dados de gravação | Flags e variáveis de eventos, registo de Fly e progresso por região vivem no save. Não encontrei documentação sobre margens livres no save do HGSS nem sobre o hg-engine o alargar. **Não verificado.** Estrutura geral: https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_IV) | |
| RAM e overlays | A auditoria do apocrypha deixou este ponto por medir | https://github.com/Davisfox5/pokemon-apocrypha/pull/2 |

Leitura dos limites: a capacidade bruta (número de mapas, cabeçalhos, tamanho do ROM) não é o obstáculo. O obstáculo é a **identidade de região** (1 bit), o **espaço de nomes de locais** (8 bits quase cheio) e o **mapa do Pokégear e Fly** (uma grelha, 20 pré-visualizações). O hg-engine, sendo injeção de código sobre o ROM e não a decompilação completa, torna mais caro alterar a estrutura do cabeçalho do que seria no `pokeheartgold`.

### 3.3 De onde podem vir os mapas

**Mapas do Platinum (Sinnoh)**
- O Platinum partilha o motor, a hierarquia cabeçalho, area data, matriz, mapa e os formatos (`.nsbmd`, `.bdhc`, permissões, edifícios). Mas o guia de mapeamento lista area data e alguns ficheiros de mapa como exclusivos do HGSS (animação global `.nsbta`, som de fundo `.bgs`), logo os mapas do Platinum não entram tal e qual. https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/mapping
- Não encontrei nenhum tutorial nem hack lançado que documente a importação de mapas do Platinum para o HGSS. **Não verificado** que funcione sem trabalho manual de texturas, edifícios, permissões e scripts.
- Seria preciso extrair os mapas de um ROM de Platinum próprio. Isso é material com direitos de autor da Nintendo e fica fora de qualquer licença de fãs.
- Referências de formato: decompilação do Platinum https://github.com/pret/pokeplatinum e do HGSS https://github.com/pret/pokeheartgold

**Mapas feitos de raiz**
- **Pokémon DS Map Studio (PDSMS)**: editor por tiles que gera o modelo 3D, para DP, Pt, HGSS, BW e B2W2. Não importa nem modifica mapas dos jogos originais. Requer Java 8 e, para exportar `.nsbmd`, os ficheiros `g3dcvtr.exe` e `xerces-c_2_5_0.dll` (do SDK da Nintendo, não distribuídos com a ferramenta). https://github.com/Trifindo/Pokemon-DS-Map-Studio . Forks com melhorias: https://github.com/AdAstra-LD/Pokemon-DS-Map-Studio e https://github.com/Trinsic64/Pokemon-DS-Map-Studio/releases . Licença: não a encontrei indicada na página do repositório (não verificado).
- **DSPRE**: importa os mapas no ROM e edita matrizes, cabeçalhos, eventos, edifícios, câmaras e Fly. https://github.com/DS-Pokemon-Rom-Editor/DSPRE
- **SDSME** (Spiky's DS Map Editor): o PDSMS foi pensado para ser usado com ele; o DSPRE atual descende dessa linha e substitui-o na prática. https://github.com/Trifindo/Pokemon-DS-Map-Studio
- **Tilesets**: o PDSMS inclui alguns tilesets pré-feitos por jogo; outros são partilhados na comunidade, sobretudo no Discord Kingdom of DS ROM Hacking (KoDSH), e existe uma pasta Google Drive de tiles curada por Monkeyboy0 ligada no guia. Tilesets feitos no fork do AdAstra não abrem na versão base. https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/mapping/tiles_and_tilesets ; https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/mapping ; https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/mapping/mapping_faqs
- **Licenças e crédito**: não encontrei termos escritos para os tilesets da comunidade. A expectativa normal é creditar o autor de cada tileset e perguntar no Discord antes de usar. Não verificado caso a caso.
- Exemplo de projeto com mapas refeitos em HeartGold: Heartfelt Gold (repositório sem ROM). https://github.com/Trinsic64/Heartfelt-Gold

### 3.4 O que é realista

| Âmbito | Esforço para equipa pequena | Porquê |
|---|---|---|
| Personagens de outras regiões como NPC e combates em mapas existentes de Johto/Kanto | Dias a semanas | Só sprites, classes, scripts. É o que o projeto já faz |
| Um ou poucos mapas novos fechados (interior, ilha, gruta) ligados por warp ou barco, usando um nome de local livre | Semanas | Há cerca de 21 mapsec livres; não mexe no Town Map nem no bit de região |
| "Mini-região" de 5 a 15 mapas exteriores com tileset existente do HGSS, sem Fly próprio ou com um único ponto de Fly | Poucos meses | Mapeamento em PDSMS mais matriz e cabeçalhos novos; Town Map pode ficar com um ícone único |
| Sinnoh completo importado do Platinum | Muitos meses, risco alto | Sem precedente documentado; cabeçalhos, area data, edifícios, scripts e encontros refeitos à mão para dezenas de mapas |
| Terceira região completa com Town Map, Fly e identidade de região próprios | Vários anos | Exige alargar campos do cabeçalho, o espaço de nomes de locais e reescrever o Pokégear. O Iridium (duas regiões de raiz, com hg-engine) está em desenvolvimento há mais de dois anos e o apocrypha desistiu do motor |

---

## 4. Eventos por hora ou dia da semana e desforras

### 4.1 O que o hg-engine documenta

- A wiki do hg-engine não tem nenhuma página sobre eventos temporais, dia da semana ou desforras. As páginas existentes cobrem Pokémon, formas, itens, movimentos, evoluções, encontros selvagens, classes de treinador, overworlds e estrutura das equipas. https://github.com/BluRosie/hg-engine/wiki (lista confirmada na cópia local `documentation/wiki/`)
- Não encontrei nenhum "helper" novo do hg-engine para batalhas semanais. Não verificado que não exista em ramos ou forks; no ramo local não há.

### 4.2 O que o jogo original já oferece (e o hg-engine expõe)

Comandos de script vanilla disponíveis nas macros do repositório. Local: `asm/include/scriptmacros.inc`; no GitHub: https://github.com/BluRosie/hg-engine/blob/main/asm/include/scriptmacros.inc

- `get_weekday` / `GetDayOfWeek` (comando 484): devolve o dia da semana numa variável; constantes `DAY_SUNDAY = 0`, `DAY_MONDAY = 1`, etc. É usado em scripts originais, por exemplo `data/scr_seq/scr_seq_0859_T22GYM0101.s`.
- `get_phone_book_rematch` / `GetPokeGearRematch` (comando 142) e `get_rematch_msg_params` / `TrainerRematchMsgCheck` (comando 216): sistema de desforras por telefone.
- `set_phone_call` e `run_phone_call` (comandos 430 e 431), e a macro `phone_call`: chamadas do Pokégear disparadas por script.
- Constantes de mensagens de desforra em `include/trainer_data.h` (`TRMSG_PHONE_REMATCH_INTRO`, etc.) e em `armips/include/constants.s` (`TEXT_REMATCH_IN_OVERWORLD`, etc.).

Do lado de C, o relógio está exposto em `include/rtc.h`: `GF_RTC_CopyDateTime`, `GF_RTC_CopyDate`, `GF_RTC_CopyTime`, `GF_RTC_GetTimeOfDay`, o enum `RTCWeek` (domingo = 0) e o enum de período do dia (manhã, dia, tarde, noite, madrugada). No GitHub: https://github.com/BluRosie/hg-engine/blob/main/include/rtc.h

### 4.3 Modelo de design já existente no HGSS

- As desforras dos líderes funcionam assim: regista-se o número do líder no Pokégear, liga-se numa janela semanal específica (dia e período), e o líder desloca-se ao Fighting Dojo em Saffron. https://bulbapedia.bulbagarden.net/wiki/Rematch e https://bulbapedia.bulbagarden.net/wiki/Fighting_Dojo/Generation_IV
- Pormenor a copiar com cuidado: o jogo trata das 00:00 às 03:59 como "noite", por isso uma janela noturna atravessa a mudança de dia. https://bulbapedia.bulbagarden.net/wiki/Rematch
- Tabelas de horários por líder: https://www.serebii.net/heartgoldsoulsilver/gym-rematch.shtml e https://pokemondb.net/heartgold-soulsilver/gym-rematch (as duas fontes divergem em alguns casos)
- Outros eventos diários e semanais do HGSS: https://serebii.net/heartgoldsoulsilver/dailyevent.shtml

Conclusão: para combates semanais com NPC famosos não é preciso código novo no motor. Basta `get_weekday` mais uma flag de "já combateu hoje" (o jogo tem flags que são repostas diariamente; quais estão livres no hg-engine: não verificado) e, se se quiser, o período do dia. O padrão do Fighting Dojo serve de modelo pronto.

---

## Recomendações

Ordenadas do menor para o maior esforço e risco.

1. **Batalha da Korrina com o sprite do Gnomowladny** (esforço: horas; risco: baixo). Reduzir a 16 cores, montar `NNN_enc.png` e a folha de frames, creditar "Gnomowladny". Enviar-lhe uma nota no DeviantArt a pedir autorização para a redução de cores, por causa da regra "DO NOT EDIT without permission" do Showdown.
2. **Reutilizar o que o HG já traz** (esforço: horas; risco: nulo em termos de créditos de fãs). Cynthia, os oito líderes de Sinnoh (incluindo Crasher Wake), os cinco parceiros de Sinnoh e os cérebros da Frontier têm classe e sprite de batalha; Steven e Cynthia têm overworld. Confirmar visualmente os overworlds `0215` a `0222`.
3. **Combates semanais com `get_weekday`** (esforço: horas a dias; risco: baixo). Seguir o padrão do Fighting Dojo, com atenção à janela noturna que atravessa a meia-noite.
4. **Overworld da Korrina feito à mão** (esforço: um a três dias; risco: baixo). Editar um overworld Gen 4 existente ou usar as peças livres do pack do Poltergeist (uso e edição livres). Alternativa: encomendar.
5. **Steven, Diantha, Sycamore, N, Ghetsis, Cyrus** (esforço: um a dois dias por personagem; risco: baixo a médio). Batalha: Showdown, com crédito ao artista indicado em 1.2 e pedido de autorização quando houver edição. Overworld: N e Ghetsis do DiegoWT, Diantha provavelmente do pack da Taiga, Cyrus dos rips DPPt; Sycamore não tem fonte e teria de ser feito. Risco médio só porque os packs de overworld dizem "não redistribuir" e não esclarecem o uso em rom hacks.
6. **Mapas novos isolados** (esforço: semanas; risco: médio). Interiores ou uma ilha, com PDSMS mais DSPRE, usando um dos cerca de 21 nomes de local livres e sem tocar no Town Map. Testar cedo a compatibilidade do DSPRE com o ROM hg-engine, que é parcial.
7. **Mini-região com tilesets do HGSS** (esforço: meses; risco: médio a alto). Viável se aceitar um único ponto de Fly e não mexer na identidade de região.
8. **Sinnoh importado do Platinum** (esforço: muitos meses; risco: alto). Sem precedente documentado e com material extraído de outro jogo comercial.
9. **Terceira região completa com Town Map e Fly próprios** (esforço: anos; risco: muito alto). Os limites estruturais (1 bit de região, mapsec de 8 bits, grelha única do Pokégear) e a experiência de outros projetos indicam que não é realista para uma equipa pequena neste motor.
