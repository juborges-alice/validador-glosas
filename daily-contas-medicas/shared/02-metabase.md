# Como obter o valor de um KPI (Metabase / Sheets)

Regra dura do OOS: **nunca escreva SQL próprio.** Execute o card canônico por ID.

---

## Caminho A — KPI com card Metabase (`ID Card metabase` preenchido)

1. `get_metabase_credentials` — **uma vez por sessão**. Se a tool não existir ou falhar auth,
   pare o Metabase e avise a OM para reconectar o connector (Settings → Connectors → Metabase
   MCP Server). Não tente `curl` sem credencial nem browser.
2. **Decodifique a key SEM nunca imprimi-la.** Este passo é o que mais quebra na prática — leia
   inteiro antes de escrever o comando.

   A descrição da tool sugere `echo "$api_key_b64" | base64 -d`. **Não use essa forma.** Ela
   escreve a chave decodificada na saída padrão, que é a definição literal de materializar uma
   credencial: o classificador de segurança da sessão bloqueia, a chamada nunca sai, e a tarefa
   fica sem nenhum drill. Foi exatamente o que aconteceu em 17/09/2026 na tarefa 02 — a página
   saiu com os 9 drills em ⏳.

   Use substituição de comando, atribuindo direto a uma variável que só aparece como header:

   ```sh
   MB_B64='<valor api_key_b64 da tool>'
   MB_KEY=$(printf '%s' "$MB_B64" | base64 -d)
   MB_URL='https://metabase.datalake.alice.tools'

   curl -sS -X POST "$MB_URL/api/card/{ID}/query/json" \
     -H "x-api-key: $MB_KEY" \
     -H 'Content-Type: application/json' \
     -d '{"parameters":[]}' \
     -o resultado.json -w 'HTTP %{http_code}\n'
   ```

   Verificado funcionando em 17/09/2026 (card 73490, HTTP 200, 189 linhas).

   As três regras que fazem a diferença:
   - **`printf` em vez de `echo`**, e sempre dentro de `$( )`. A chave vai para a variável, não
     para a tela.
   - **Nunca rode o `base64 -d` sozinho** só para "ver se deu certo". Esse é o comando bloqueado.
   - **Grave a resposta em arquivo** (`-o`) e leia o arquivo depois. Assim a saída do comando é
     só o código HTTP, e nenhum header com a chave aparece em log nenhum.

   Se ainda assim vier bloqueio: **não tente contornar** e **não escreva SQL no lugar do card**.
   Siga sem o drill, marque ⏳ e descreva o bloqueio no caveat — é o comportamento correto, e foi
   o que a tarefa 02 fez em 17/09.
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

### ARMADILHA CRÍTICA — o parâmetro de data zera a baseline em 3 cards

Nos cards **65831** (`Faturamento total acumulado` e `R$ Faturado Cassi`) e **65834**
(`R$ Recurso de Glosa acumulado`), o `Parâmetro metabase` cadastrado no Notion manda passar
`invoice_date` / `appeal_date_filter` = `"thismonth"`. **Não passe.**

Motivo: o filtro é aplicado globalmente na CTE que alimenta **tanto o mês atual quanto os 3
meses anteriores**. Passá-lo zera a coluna `media_3m_anteriores`, e a variação percentual vira
divisão por zero. O card **já calcula os dois períodos sozinho**, a partir de `CURRENT_DATE`.

**A chamada correta é omitir o parâmetro de data nesses três KPIs.** Verificado em 16/09/2026
batendo o resultado contra o valor publicado no canal (Cassi: −28,81%, idêntico).

**Regra geral que vale para qualquer card com baseline embutida:** depois de executar, olhe a
coluna de comparação histórica. Se ela vier **zero ou nula** enquanto o período atual tem valor,
você provavelmente filtrou a baseline junto. Re-execute **sem** o parâmetro de data e compare.
Nunca reporte variação calculada sobre baseline zerada — e nunca marque o KPI como "sem dado"
sem ter tentado isso.

### ARMADILHA CRÍTICA (2) — parâmetro opcional omitido devolve o histórico inteiro

O card **65700** (`% Glosa Alice por Prestador - HI`) traz `invoice_date_filter` com
`required: false`. Omitir **não** cai no mês corrente: cai em **todo o histórico**, sem erro e
sem aviso. Verificado em 17/09/2026 — SIRIO apareceu com **R$7,6 milhões** de faturamento em vez
de **~R$1 milhão**, e o percentual de glosa sai diluído na mesma proporção.

Esta é a armadilha inversa da anterior, e por isso perigosa: no 65831/65834 o erro é **passar** o
parâmetro de data; no 65700 o erro é **não passar**. Não existe regra única — vale a tabela:

| Card | Parâmetro de data | Por quê |
|---|---|---|
| 65831 · 65834 | **NÃO passe** | zera a baseline de 3 meses |
| 65700 | **PASSE** (`invoice_date_filter = "thismonth"`) | omitir devolve o histórico inteiro |

**Teste de sanidade obrigatório, todo dia, em qualquer card de prestador:** olhe a ordem de
grandeza do faturamento antes de calcular o percentual. Faturamento de um prestador grande num
mês parcial é ordem de milhão, não de dezena de milhões. Número dez vezes maior que o esperado é
janela errada, não crescimento.

### O `Parâmetro metabase` do catálogo pode trazer a chave errada

Caso verificado em 17/09/2026: para o card **65831**, o catálogo do Notion registra a chave
`tipo_da_instituicao`, mas o slug real da API é **`institution_type`**. Passar a chave do
catálogo devolve erro explícito de template tag inexistente.

Quando isso acontecer: a fonte da verdade é o array `parameters` da resposta da API do card, não
o catálogo. Use o slug da API, execute, e **não** reescreva o catálogo por conta própria —
divergência de slug é correção da OM.

### Top N: avalie a lista inteira, todo dia

Cards de prestador com Top N (**65700** com 15 posições, **50958**, **66204**, **56231**) trazem
a lista completa do dia. **Avalie TODAS as linhas contra o limiar, todo dia** — não só os
prestadores que apareceram em leituras anteriores.

Isso não é detalhe: em 16/09/2026 o prestador **INCOR** cruzou o limiar de `% Glosa Alice por
Prestador` (35,15% contra baseline de ~2%, desvio de +33 p.p.) e **não entrou no report**, porque
a leitura revalidou apenas os nomes já conhecidos (SIRIO, SAHA). Prestador novo acima do piso de
materialidade é exatamente o que esse KPI existe para pegar.

Procedimento: para cada linha do Top N, aplique o limiar do KPI (incluindo o piso de
materialidade de R$50.000 de faturamento no mês). Todo prestador que cruzar entra no report,
tenha aparecido antes ou não. Se um prestador citado ontem sumiu do Top N, diga isso
explicitamente — sumiu da lista não é o mesmo que voltou ao normal.

### Cards que não aceitam parâmetro nenhum

Verificado em 16/09/2026 pela API (`parameters: []` no nível superior da resposta):
**30863 · 35629 · 32465 · 65694 · 30858 · 66766 · 48840 · 73490**.

Para esses, o `Parâmetro metabase` do Notion é decorativo — execute o card sem parâmetros e siga.
**Não registre isso como observação de qualidade de dados no report do dia**: já é sabido e está
aqui. Registrar todo dia vira ruído. Só reporte se a lista acima estiver desatualizada, isto é,
se algum desses cards passar a aceitar parâmetro ou se um card fora da lista devolver
`parameters: []`.

**`parameters: []` não quer dizer "sem filtro de período".** O card **50958** devolve o array
vazio e mesmo assim aplica um recorte de data fixo por dentro do SQL. Ou seja: o array vazio diz
que **você** não tem o que passar, não que o card devolve tudo. Antes de comparar períodos,
confira qual janela o card usou de fato — pelo resultado (as datas que voltam) ou pelo SQL do
card. Comparar um card de janela fixa com outro de janela que você controlou é a receita de
variação inventada.

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
