# Identificadores fixos — Daily Contas Médicas

Arquivo de referência lido pelas 5 tarefas da rotina. Quando algo muda (time, canal,
KPI novo, card novo), muda **aqui** — não dentro dos SKILL.md.

## Operação

| Item | Valor |
|---|---|
| Operação | Contas Médicas |
| Alliance | Insurance |
| Página da operação (Notion) | https://app.notion.com/p/37cf0f13146a8023b8ebe67185557704 |
| Canal do Slack | `C0BH03QKUKY` (#daily_cm_ops_inteligentes) |
| Executor / OM | juliana.borges@alice.com.br — resolver o Notion user ID com `notion-search` (`query_type: "user"`) a cada execução |
| Dashboard Metabase | https://metabase.datalake.alice.tools/dashboard/1996-contas-medicas-clinicas-labs-e-cassi |
| Daily síncrona | ~10h30–11h00 BRT, gravada com Anotações do Gemini |

## Datatables (globais do OOS — não trocar)

| Datatable | Data source | URL |
|---|---|---|
| Operações (hub) | `collection://764920f2-c8f4-409f-9452-bca186a2a1ad` | https://app.notion.com/p/3395d7113de345689453bfd0d5ddacfa |
| KPIs | `collection://4c8ffc67-b817-48db-ab8c-04cb5c0c731e` | https://app.notion.com/p/c40fb19eaba74d2ba452837e9e19a690 |
| Execuções de Rotina | `collection://00d00405-31e2-4670-abd1-168e986e55e9` | https://app.notion.com/p/6a214111ca244ea1a323a745440367f6 |
| Decision Log (Log de Desvios e Decisões) | `collection://b619a21c-a5f8-4701-a477-f5d150f03066` | https://app.notion.com/p/5498ab1053f94465a1c959fa6bde1480 |
| Action Log (Log Melhoria Contínua) | `collection://39ff0f13-146a-8001-b289-000b5fb3961c` | https://app.notion.com/p/39ff0f13146a80a98ffaee11d80038d8 |

O **Action Log de Contas Médicas é o `Log Melhoria Contínua`** (Seção 8 da página da operação),
filtrado por `Operações` = Contas Médicas. Não existe outra tabela de ações para esta operação.

Encadeamento canônico: Execução de Rotina → (`Decisões geradas`) → Decision Log → (`Decisão de origem`) → Action Log.
O Action Log **não** tem relation direta com Execuções de Rotina; ele se liga pela decisão.

## Gravação da daily síncrona (Drive)

Não existe uma pasta única: as anotações do Gemini nascem no Drive de quem gravou e são
compartilhadas. **Busque por título, não por pasta:**

```
title contains 'Daily Contas Médicas' and title contains '<AAAA/MM/DD de hoje>'
```

Padrão do nome: `Daily Contas Médicas - AAAA/MM/DD HH:MM GMT-03:00 - Anotações do Gemini`
(também aparece como `- Notes by Gemini`). Se houver mais de um, use o mais recente.
Se não achar, registre a ausência no Bloco 6 e siga — não trave a execução.

## KPIs de operação (ordem fixa da tabela do report)

Fonte da verdade é o catálogo no Notion, lido a cada execução (`Operação` = Contas Médicas
e `Priorizado para rotina?` contém a cadência do dia). A lista abaixo define **ordem e
agrupamento** de exibição, nunca meta nem card.

| # | KPI (nome completo no Notion) | Card | Cadência |
|---|---|---|---|
| 1 | Contas Médicas - % Glosa Geral - HI | 65942 | diária |
| 2 | Contas Médicas - % Glosa por Tipo de HI | 50815 | diária |
| 3 | Contas Médicas - % Glosa Alice por Prestador - HI | 65700 | diária |
| 4 | Contas Médicas - R$ Recurso de Glosa acumulado | 65834 | diária |
| 5 | Contas Médicas - SLA Recurso de Glosa - HI | 65858 | diária |
| 6 | Contas Médicas - Recursos de Glosa Próximos do Vencimento (≤3 dias) - HI | 73490 | diária |
| 7 | Contas Médicas - SLA de Análise de conta - HI | 65832 | diária |
| 8 | Contas Médicas - PEGs por Status de Análise no SLA - HI | 32465 | diária |
| 9 | Contas Médicas - Qnt de guias analisadas por dia | 65840 | diária |
| 10 | Contas Médicas - % PEGs sem NF | 65694 | diária |
| 11 | Contas Médicas - Faturamento total acumulado | 65831 | diária |
| 12 | Contas Médicas - R$ Faturado Cassi | 65831 | diária |
| 13 | Contas Médicas - % Resumos Criticados - HS | 30858 | diária |
| 14 | Contas Médicas - Status das Críticas (por fatura) - HS | 66766 | diária |
| 15 | Contas Médicas - Tempo para Resolução de Críticas - HS | 48840 | diária ⚠️ |
| 16 | Contas Médicas - % Faturas por Status - HS | 30863 | diária |
| 17 | Contas Médicas - SLA de Pagamento de HS | 35629 | diária |
| 18 | Contas Médicas - % Recurso de Glosa | 65833 | **mensal — nunca entra nesta rotina** |

**⚠️ `Tempo para Resolução de Críticas - HS`: metade do limiar é inverificável.** O limiar diz
`Tempo médio de resolução > 3 dias; ou crítica específica > 10 dias sem resolução`. Sem drill
cadastrado, **só a média mensal é apurável** — a segunda cláusula nunca pode ser checada. Reporte
o KPI pela primeira cláusula e escreva no Caveat, todo dia:
`segunda cláusula do limiar (crítica > 10 dias) não verificável — sem card de drill`.
Quando um drill for cadastrado, esta nota sai.

Conferido contra o catálogo em 16/09/2026. Desde a primeira versão (19/08) entrou o KPI
`Recursos de Glosa Próximos do Vencimento (≤3 dias)` (card 73490, criado em 10/09) e foram
recalibrados os limiares de `% Glosa por Tipo de HI` e `PEGs por Status de Análise no SLA - HI`
(ambos em 09/09) — os limiares novos são lidos do Notion a cada execução, e as condições que
eles carregam estão resumidas em `01-regras-de-registro.md` §1.

Ao exibir no Slack e no Notion, **corte o prefixo `Contas Médicas - `**. Case pelo nome
completo, exiba sem o prefixo.

KPI priorizado que apareça no Notion e **não** esteja nesta lista: inclua ao final da tabela
e avise `<@U03A4SS2P1Q>` numa resposta na thread da Mensagem 1, pedindo posição e responsável.

## Cards de drill por KPI (KPIs de processo)

A relation `KPIs operação <> processos` no catálogo é a fonte. A tabela abaixo é o atalho
verificado em 19/08/2026 — se divergir do Notion, o Notion ganha.

| KPI de operação | Cards de drill (ID Card metabase da linha de processo) |
|---|---|
| % Glosa Geral - HI | 50958 (R$ Glosado por Prestador Top 12) · 54617 (Glosa por Motivo Geral) · 50815 (% Glosa por Tipo de HI) |
| % Glosa por Tipo de HI | 52038 (Labs) · 52037 (Clínicas) · 31223 (Hospitais) · 66204 (Motivo Top 10 prestadores) |
| % Glosa Alice por Prestador - HI | 50958 (R$ Glosado por Prestador Top 12) |
| R$ Recurso de Glosa acumulado | 54662 (Valor Recursado por prestador) · 54677 (Valor Recursado por Motivo Geral) |
| SLA Recurso de Glosa - HI | 65835 (Qnt acumulada Recurso de Glosa) · 73490 (Recursos próximos do vencimento) |
| Recursos de Glosa Próximos do Vencimento (≤3 dias) - HI | — sem drill próprio; o card 73490 já é a lista item-a-item |
| SLA de Análise de conta - HI | 65837 (guias/dia Hospitais) · 65839 (guias/dia Labs+Clínicas) · 32465 (PEGs por Status no SLA) |
| PEGs por Status de Análise no SLA - HI | 65837 · 65839 |
| Qnt de guias analisadas por dia | 65837 (Hospitais) · 65839 (Labs+Clínicas) |
| % PEGs sem NF | 56231 (Top 10 prestadores com mais PEGs sem NF) · 49800 (Protocolos sem NF por valor e data) |
| Faturamento total acumulado | 65831 (R$ Faturado por tipo de instituição) · 50631 (Volumetria de Guias por Prestador) · 26655 (R$ Faturamento por Prestador) |
| R$ Faturado Cassi | — sem drill cadastrado |
| % Resumos Criticados - HS | 66766 (Status das Críticas por fatura) · 38203 (% Críticas Acatadas) |
| Status das Críticas (por fatura) - HS | 38203 |
| Tempo para Resolução de Críticas - HS | — sem drill cadastrado ⚠️ |
| % Faturas por Status - HS | — sem drill cadastrado |
| SLA de Pagamento de HS | 35588 (Média de Dias Úteis Entre Etapas de Pagamento) |

## KPIs do tipo "alerta de trabalho"

A maioria dos KPIs é termômetro: quando desvia, a rotina levanta hipótese e propõe plano de
ação. **Alerta de trabalho é outra coisa** — é fila. A causa é sempre a mesma (o prazo está
correndo), não há o que investigar, e o que o time precisa é a **lista para agir hoje**.

| KPI | Card | Classe |
|---|---|---|
| Contas Médicas - Recursos de Glosa Próximos do Vencimento (≤3 dias) - HI | 73490 | **Alerta de trabalho** |

Regras próprias desta classe, que sobrescrevem o tratamento normal de 🔴:

1. **A mensagem no Slack traz a lista, não a análise.** Sem hipótese, sem "ação sugerida". O
   formato está no Passo 8 de `01-report-slack/SKILL.md`.
2. **Mostra sempre os dois horizontes**, porque a visão útil é do todo:
   - **o que ainda dá pra salvar** — `status_urgencia` = `Vence em ate 3 dias`;
   - **o que já perdeu o prazo mas segue em aberto** — `status_urgencia` =
     `Vencido (nao acionavel)`. O rótulo "não acionável" é do card e se refere ao prazo de 15
     dias corridos, não ao recurso: ele continua aberto e continua sendo trabalho. **No report,
     escreva "vencido, ainda em aberto"** — nunca "não acionável", que faz o time ignorar.
3. **Não abre entrada no Decision Log.** Fila de trabalho não é decisão. Vira **linha de
   pendência** (Mensagem 6 e Bloco 5), com o rótulo `[Fila]`, e rola todo dia até zerar.
4. **Não entra na análise de desvios** do Bloco 2 da página como deep dive. A lista completa
   dos dois horizontes fica no Bloco 2 como sub-toggle próprio, sem pedido de plano de ação.
5. **O farol continua saindo do `Limiar de alerta` do catálogo**, como qualquer KPI. Hoje o
   limiar olha só a janela de ≤3 dias; se a OM quiser que o estoque vencido também dispare
   sozinho, é editar o texto do limiar no Notion — a rotina obedece o que estiver escrito lá.

Para incluir outro KPI nesta classe, acrescente-o à tabela acima. Nada mais precisa mudar.

## BLOCO DE MAPEAMENTO DE RESPONSÁVEIS — editar aqui quando o time mudar

Confirmado pela OM em 16/09/2026. A Larissa saiu do bloco: a Fernanda voltou de férias.

```
Fernanda Jerônimo  <@U044N26BETU>
  - % Resumos Criticados - HS
  - Status das Críticas (por fatura) - HS
  - Tempo para Resolução de Críticas - HS
  - % Faturas por Status - HS
  - SLA de Pagamento de HS
  - R$ Faturado Cassi
  - % PEGs sem NF

POR TIPO DE INSTITUIÇÃO — Hospital → Alana <@U073Z4ENBNW>
                          Laboratório ou Clínica → Fernanda <@U044N26BETU>
  - % Glosa Geral - HI
  - % Glosa por Tipo de HI
  - % Glosa Alice por Prestador - HI
  - R$ Recurso de Glosa acumulado
  - SLA Recurso de Glosa - HI
  - Recursos de Glosa Próximos do Vencimento (≤3 dias) - HI
  - SLA de Análise de conta - HI
  - PEGs por Status de Análise no SLA - HI
  - Qnt de guias analisadas por dia
  - Faturamento total acumulado
```

**Todos os KPIs têm responsável.** Não existe mais a categoria "sem responsável": todo 🔴 abre
deep dive e tem alguém marcado. Se um KPI novo entrar no catálogo e não estiver neste bloco, ele
cai na regra de `KPI sem responsável mapeado` — marca a OM e pede o mapeamento.

Marque sempre por ID (`<@U044N26BETU>`), nunca escreva o nome antes ou depois da menção.

### Como rotear os KPIs "por tipo de instituição"

Nesses nove KPIs o responsável **não é fixo**: depende de onde o desvio está concentrado. Você
só descobre isso **depois de executar o drill**, então o roteamento é a última coisa que se
decide, não a primeira.

1. Execute o drill do KPI (tabela de cards acima) e quebre o desvio **por tipo de instituição**.
2. Roteie pela concentração:
   - desvio concentrado em **Hospital** → marque **Alana** `<@U073Z4ENBNW>`;
   - desvio concentrado em **Laboratório** ou **Clínica** → marque **Fernanda** `<@U044N26BETU>`;
   - **Centro de Diagnósticos** → Fernanda (é o fluxo Cassi, que já é dela). Se essa leitura
     estiver errada, corrija aqui.
3. **Concentração** significa que um tipo responde por **mais de 70%** do desvio. Abaixo disso,
   ou quando o desvio aparece em mais de um tipo de forma relevante, **marque as duas** e diga na
   mensagem como o desvio se reparte, ex: `Hospitais 55% · Laboratórios 40%`.
   O corte de 70% é calibrável: se a rotina passar a marcar as duas quase sempre, baixe; se
   marcar uma quando o desvio claramente era das duas, suba. Mude aqui e vale na execução
   seguinte.
4. **Sempre diga por que marcou quem marcou.** Uma linha na mensagem:
   `Concentração: Hospital (78% do desvio) → <@U073Z4ENBNW>`. Sem essa linha, a pessoa marcada
   não sabe se é dela mesmo, e o roteamento vira loteria.
5. **Se o drill não devolver o tipo de instituição, marque as duas** e escreva
   `tipo de instituição não disponível no card — roteado para as duas`. Nunca chute.

**Caso conhecido:** o card **73490** (`Recursos de Glosa Próximos do Vencimento`) devolve
`institution_name` e `provider_economic_group`, mas **não** devolve o tipo de instituição. Até
que o card passe a devolver, esse KPI marca **as duas**. Quando for ajustado, esta nota sai.

## OM

`<@U03A4SS2P1Q>` — Juliana Borges. Dona dos itens `A DEFINIR`, dos escalonamentos e do
mapeamento de responsáveis. **Não marcar por padrão** nas cobranças: só quando o item é
`A DEFINIR`, é da alçada dela, ou é escalonamento.
