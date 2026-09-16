# Como obter o valor de um KPI (Metabase / Sheets)

Regra dura do OOS: **nunca escreva SQL próprio.** Execute o card canônico por ID.

---

## Caminho A — KPI com card Metabase (`ID Card metabase` preenchido)

1. `get_metabase_credentials` — **uma vez por sessão**. Se a tool não existir ou falhar auth,
   pare o Metabase e avise a OM para reconectar o connector (Settings → Connectors → Metabase
   MCP Server). Não tente `curl` sem credencial nem browser.
2. Decodifique a key para `$MB_KEY` e use `$MB_URL="https://metabase.datalake.alice.tools"`.
   **Nunca exiba a key.**
3. Recupere o card: `GET /api/card/{ID}`. **Não confie apenas em
   `dataset_query.native.template_tags`** — costuma vir vazio. Os parâmetros que o card
   realmente aceita estão no array `parameters` de nível superior da resposta (cada um com
   `type`, `target` e `slug`). Sempre confira esse array antes de concluir que o card não
   aceita parâmetro.
4. Compare o `Parâmetro metabase` cadastrado no Notion com os slugs reais do passo 3. Já
   aconteceu de o JSON do Notion usar chaves antigas que não correspondem a nenhum parâmetro
   do card. Nesse caso **use os slugs reais** e registre a divergência como observação de
   qualidade de dados no report — não trave a execução por isso.
   Cuidado específico de Contas Médicas: vários cards têm valores de filtro com **padding de
   espaços** (`"Hospital                                "`). Reproduza o valor exatamente como
   o card devolve, incluindo os espaços.
5. Execute: `POST /api/card/{id}/query/json`, com
   `parameters: [{"type": "...", "target": ["dimension", ["template-tag", "<slug>"]], "value": "..."}]`.
   Capture **ponto + série**: a tendência é necessária para os limiares de tendência da
   operação (`crescimento > 1 p.p. vs. mês anterior`, `desvio > 20% vs. média histórica`).
6. **Comparação histórica é obrigatória tentar.** Se o limiar exige histórico (`vs. média dos
   últimos 3 meses`, `vs. mês anterior`) e o card só devolve o período atual: procure um
   parâmetro de data no array `parameters` e **execute o card de novo** apontando para o
   período histórico (ex: `thismonth` para o atual, `past3months` para a baseline), e calcule
   a comparação a partir dos dois resultados. Isso continua sendo "executar o card canônico".
   Se houver decisão metodológica vigente restringindo a baseline, use a janela dela
   (`past2months` em vez de `past3months`). Janelas relativas também permitem isolar um mês
   específico por subtração entre duas execuções do mesmo card — use isso em vez de SQL.
7. **LIMIT / TOP N.** Vários cards de Contas Médicas têm Top N embutido (`Top 12 HI`,
   `Top 10 prestadores`). Ao rodar o card duas vezes (atual vs. histórico), cada execução
   devolve o Top N **daquela** janela — só é válido comparar prestadores/motivos que aparecem
   nas duas listas. **Não amplie o LIMIT** (seria alterar a lógica do card). Registre no
   report quais entidades citadas em leituras anteriores não puderam ser confirmadas nem
   descartadas por esse motivo. Para confirmar uma entidade específica que caiu fora do Top N,
   use o filtro da própria entidade quando o card tiver — ex: `provider_economic_group_filter`
   no card 65700, `provider_economic_group` no 65834/65832/65858, `nome_prestador` no 65833.
8. Só marque **"sem dado"** depois de tentar 6 e 7. Quando acontecer, o report diz exatamente
   o que foi tentado e por que não funcionou (`card não tem parâmetro de data`, `LIMIT do card
   impede comparação completa mesmo após rodar as duas janelas`). Nunca marque "sem dado"
   porque a primeira chamada trouxe um snapshot de um único período.

### Cards que compartilham ID

`Faturamento total acumulado` e `R$ Faturado Cassi` usam **o mesmo card 65831**, diferenciados
só pelo `tipo_da_instituicao` no `Parâmetro metabase` (Cassi = `["Centro De Diagnosticos"]`).
Execute duas vezes com os filtros de cada linha do Notion. Nunca reaproveite o resultado de um
para o outro.

### Grupo econômico

Ao agrupar "por prestador", verifique se múltiplas linhas pertencem à **mesma rede/grupo
econômico** sob nomes de unidade diferentes (Fleury/Delboni, Oswaldo Cruz Vergueiro/Oswaldo
Cruz, Einstein e suas unidades). Concentração calculada por unidade subestima a real.

### Denominador pequeno

Ao ler percentual de concentração em KPI de processo, cheque antes se o volume total do
período está anormalmente baixo. Com denominador pequeno, percentual de concentração é
mecanicamente instável e **o valor absoluto é o dado confiável** — reporte os dois.

---

## Caminho B — KPI em Google Sheets (`ID Card metabase` vazio)

O valor vem de uma célula fixa:
- URL da planilha = `Dashboard oficial`
- Célula/range = `Parâmetro metabase` (ex: `Painel!B7`, ou só `B7`)

```
curl -s "https://docs.google.com/spreadsheets/d/SHEET_ID/gviz/tq?tqx=out:csv&sheet=ABA&range=CELULA"
```

Trate aspas e separador decimal (vírgula BR vs. ponto). Se o curl voltar HTML de login
(planilha restrita): tente o connector do Google Drive (`read_file_content`) e localize a
célula. Se ainda não conseguir, peça à OM para liberar a planilha por link na organização ou
colar o valor. **Não chute o valor.**

Hoje nenhum KPI diário de Contas Médicas está neste caminho — todos os 16 têm card. Mantido
para KPI novo que entre por planilha.

---

## Defasagem de ETL

O card agregado e os cards de drill saem da mesma fonte, mas podem carregar em horários
diferentes. Se o agregado acusa desvio e o drill volta vazio ou com contagem menor para a
mesma data, isso é **defasagem de ETL, não ausência de desvio**. Nesse caso:

- Não afirme que não há casos. Não escreva que "populam no próximo ciclo" como se fosse
  resolução.
- Escreva que a lista está pendente porque o drill ainda não carregou a data, e que será
  repuxada.
- Marque como pendência de repuxe: a tarefa `02-notion-page` (09h15) re-executa o card e posta
  a lista na mesma thread quando os dados aparecerem; a `04-sync-pos-daily` é o fallback.
- **Sanidade:** a soma do drill tem que reconciliar com o agregado. Se não reconciliar, o
  drill ainda está incompleto — diga isso.

Em Contas Médicas o risco de defasagem é maior no começo do dia porque quase todo card é
acumulado no mês (`thismonth`) e o fechamento do dia anterior entra de madrugada. O report das
06h30 é justamente o horário de risco.
