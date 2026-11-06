# SQL de referência dos cards do Metabase

Os cards canônicos da rotina vivem no Metabase (collection 3609). Este diretório guarda o **SQL
de referência versionado** deles, para que a régua de cada KPI tenha histórico em git e para que
uma alteração possa ser revisada antes de ir para o Metabase.

**O Metabase continua sendo a fonte de execução.** A rotina executa o card por ID, nunca este
arquivo. Se os dois divergirem, o card é o que está no ar — e a divergência é um bug a corrigir.

| Arquivo | Card | KPI |
|---|---|---|
| `79935-pegs-sem-nf-regua-30.sql` | 79935 | % PEGs sem NF — farol por competência |
| `79936-fila-nf-drill.sql` | 79936 | % PEGs sem NF — drill item a item |

## Pendente de aplicação no Metabase

O SQL de **79935** e **79936** neste diretório já contém a régua de 06/11/2026 (limiar de 30% e
piso de 2 dias úteis após a análise) e foi **testado contra o banco de produção** pelo endpoint
de query ad-hoc, com os dois cards reconciliando entre si.

Ele **ainda não foi gravado nos cards do Metabase**: a sessão que fez a alteração não tinha
permissão de escrita em card (a chamada de `PUT /api/card/{id}` foi bloqueada pelo sandbox).
Até que alguém cole este SQL nos cards 79935 e 79936, eles seguem rodando a régua de 27/10
(limiar de 29%, sem piso de maturação) e o número publicado pela rotina **não** reflete o que
este repositório e o catálogo do Notion descrevem.
