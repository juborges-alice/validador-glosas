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
Se não achar, registre a ausência no Bloco 5 e siga — não trave a execução.

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
| 5 | Contas Médicas - SLA Recurso de Glosa - HI | 60527 | diária |
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
| 19 | Contas Médicas - Ciclo de processamento Cassi | 65831 (sem card próprio) | **semanal — pergunta na terça, ver seção do ciclo Cassi** |

**⚠️ `Tempo para Resolução de Críticas - HS`: metade do limiar é inverificável.** O limiar diz
`Tempo médio de resolução > 3 dias; ou crítica específica > 10 dias sem resolução`. Sem drill
cadastrado, **só a média mensal é apurável** — a segunda cláusula nunca pode ser checada. Reporte
o KPI pela primeira cláusula e escreva no Caveat, todo dia:
`segunda cláusula do limiar (crítica > 10 dias) não verificável — sem card de drill`.
Quando um drill for cadastrado, esta nota sai.

Conferido contra o catálogo em 22/09/2026 (as 19 linhas da tabela acima batem com o `ID Card
metabase` do Notion). A única divergência encontrada era o card do `SLA Recurso de Glosa - HI`,
corrigido aqui de 65858 para **60527** — a troca de fonte foi decidida em 18/09 para o KPI bater
com o que o dashboard mostra, e o catálogo já estava certo.

Conferido antes disso em 16/09/2026. Desde a primeira versão (19/08) entrou o KPI
`Recursos de Glosa Próximos do Vencimento (≤3 dias)` (card 73490, criado em 10/09) e foram
recalibrados os limiares de `% Glosa por Tipo de HI` e `PEGs por Status de Análise no SLA - HI`
(ambos em 09/09). O `PEGs por Status de Análise no SLA - HI` foi recalibrado de novo em 22/09,
saindo da proporção sobre o total em aberto para duas contagens absolutas de prazo: 7 du exatos na
meta (🟡) e ≥13 du no limiar (🔴). A meta de 90% de aderência que ele carregava passou a viver só
no `SLA de Análise de conta - HI`.
Os limiares novos são lidos do Notion a cada execução, e as condições que eles carregam estão
resumidas em `01-regras-de-registro.md` §1.

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

### Drill em cascata — quando o drill devolve outro KPI de operação

A tabela acima tem **um nível**. Três linhas dela apontam para um KPI que é ele próprio de
operação — `% Glosa por Tipo de HI` (50815), `PEGs por Status no SLA` (32465) e
`Status das Críticas` (66766). Quando um drill desses identifica **onde** está o desvio, ele
ainda não disse **por quê**: pare aí é entregar meia investigação.

**Regra:** se o drill de um KPI 🔴 for outro KPI de operação e ele concentrar o desvio num
recorte, execute também os drills **desse** KPI, limitados ao recorte encontrado. A cascata tem
no máximo dois níveis — não continue além disso.

| KPI 🔴 | nível 1 (onde) | nível 2 obrigatório (por quê) |
|---|---|---|
| % Glosa Geral - HI | 50815 (% glosa por tipo) | **52038** (motivo · Laboratórios) · **52037** (motivo · Clínicas) · **31223** (motivo · Hospitais) · **66204** (motivo × prestador, aceita `invoice_date` e `institution_type`) |
| % Glosa por Tipo de HI | 52038 · 52037 · 31223 | 66204, filtrado pelo tipo que concentra |
| PEGs por Status no SLA - HI | 32465 | 73390 (faixas de dias úteis) |
| Status das Críticas - HS | 66766 | 38203 (% críticas acatadas) |

O 54617 (motivo **agregado**, sem tipo) e o 50815 (tipo **sem** motivo) não se substituem: rodar
os dois e não cruzar responde "qual tipo" e "qual motivo" sem nunca responder "qual motivo em
qual tipo", que é a única forma acionável. O cruzamento são o 52038/52037/31223.

### Nível ≠ variação — as duas leituras são obrigatórias, e podem ter donos diferentes

Um KPI agregado responde a duas perguntas que quase nunca têm a mesma resposta:

- **Nível** — quem está acima da linha/meta hoje. Sai de comparar cada recorte contra o limiar.
- **Variação** — quem fez o indicador se mover contra o mês anterior. Sai da **decomposição
  do delta**, nunca do nível.

Em 23/09/2026 as duas divergiram por completo em `% Glosa Geral - HI`: o excedente acima da
linha de 5% era **100% de Laboratório** (nível), mas do crescimento de +0,797pp contra Ago/26,
**43,2% veio de Hospital**, 40,9% de Laboratório e 19,1% de puro mix. O report saiu só com o
nível e roteou o vermelho para a Fernanda, quando a maior parcela do que mudou era da Alana.

**Decomposição obrigatória do delta (shift-share).** Para cada tipo `t`, com taxa `r` e peso no
faturado `w`:

```
efeito taxa (t) = (r_atual − r_anterior) × w_atual      → o recorte piorou de verdade
efeito mix  (t) = (w_atual − w_anterior) × (r_anterior − agregado_anterior)
                                                        → a composição mudou, a taxa não
Σ (efeito taxa + efeito mix) = Δ do agregado
```

**O efeito mix não é detalhe técnico: em Contas Médicas ele é a Cassi.** O Centro de
Diagnósticos glosa 0% e é bloco grande do faturado. Quando a remessa da Cassi atrasa, o peso
dele cai, o denominador perde faturamento sem glosa e o percentual agregado **sobe sozinho**.
Em 23/09 o peso caiu de 9,41% para 6,28% (série parada desde 15/09) e isso respondeu por
+0,152pp — quase um quinto do crescimento — **sem nada ter piorado na operação**. Sempre
separe esse pedaço antes de acionar alguém.

**Normalize antes de comparar motivos.** O mês corrente é parcial e o anterior é fechado:
comparar R$ bruto enviesa para baixo. Converta cada motivo em **pp da taxa de glosa do próprio
tipo** (`glosado_motivo / faturado_do_tipo`) e compare os pp. Sem isso, motivo que cresceu
aparece estável e motivo estável aparece em queda.

**Roteamento:** a linha `Concentração:` do vermelho sai da cláusula do limiar que **acendeu**.
Se acendeu a de nível, é concentração do excedente; se acendeu a de variação, é concentração do
delta. Quando as duas leituras apontam tipos diferentes, marque **as duas** pessoas e diga qual
leitura corresponde a cada uma.

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
   pendência** (Mensagem 6 e Bloco 4), com o rótulo `[Fila]`, e rola todo dia até zerar.
4. **Não entra na análise de desvios** do Bloco 2 da página como deep dive. A lista completa
   dos dois horizontes fica no Bloco 2 como sub-toggle próprio, sem pedido de plano de ação.
5. **O farol continua saindo do `Limiar de alerta` do catálogo**, como qualquer KPI. Hoje o
   limiar olha só a janela de ≤3 dias; se a OM quiser que o estoque vencido também dispare
   sozinho, é editar o texto do limiar no Notion — a rotina obedece o que estiver escrito lá.

**A classe existe desde 16/09 e nunca foi aplicada.** Verificado em 17/09/2026: toda entrada do
Decision Log para `Recursos de Glosa Próximos do Vencimento`, desde pelo menos 14/09, usa o
formato normal de hipótese e causa-decidida, e abre página — violando as regras 1 e 3 acima. Se
você está prestes a escrever "Hipótese:" ou a criar uma página do Decision Log para um KPI desta
tabela, **pare**: é sinal de que você caiu no tratamento padrão sem perceber. Fila não tem
hipótese; tem lista e dono.

Para incluir outro KPI nesta classe, acrescente-o à tabela acima. Nada mais precisa mudar.

## KPIs do tipo "monitoramento" — leem, publicam, não acendem 🔴

| KPI | Card | Classe |
|---|---|---|
| Contas Médicas - R$ Faturado Cassi | 65831 | **Monitoramento** (decisão da OM, 22/09/2026) |

**Por que esta classe existe.** O valor faturado da Cassi soma três coisas: a Cassi enviar as
contas (dependência externa), o uso da rede no período (ninguém controla) e nós subirmos as
contas no sistema (o único pedaço nosso). Alertar no valor acende vermelho pelos três, e em dois
deles não existe ação — o KPI vira ruído.

Havia ainda um defeito aritmético: o valor é **acumulado no mês** e fica parado entre uma remessa
semanal e outra, enquanto a média de 3 meses do card **cresce a cada dia do mês**. Em 18–21/09 a
variação foi de −0,82% → −8,34% → −16,89% → −21,29% **sem nada ter mudado na operação**. Num KPI
de cadência semanal lido todo dia, o vermelho era garantido por construção.

Regras desta classe:

1. **Nunca acende 🔴 e nunca abre episódio no Decision Log.** Sai no report com número, série e
   tendência, farol ⚪ (monitoramento), sem hipótese e sem plano de ação.
2. **Dois checkpoints por mês, e só neles o limiar vale:** **dia 15** e **último dia útil do
   mês**. Nesses dias, Δ>10% contra a média de 3 meses abre uma **pergunta à OM** na thread —
   não um vermelho na daily. A comparação é válida em qualquer dia porque o card casa a média
   pelo **dia do mês** (em 16/09 usou "média do dia 16").
3. **O acionável não está aqui, está no ciclo semanal** — seção abaixo.

## Ciclo de processamento Cassi — o indicador acionável (decisão da OM, 22/09/2026)

A Cassi envia as contas **semanalmente** e a operação tem **a semana** para subir. O único desvio
que é nosso é: chegou a conta e não subimos. É isso, e só isso, que este indicador mede.

Não precisa de tabela nova: o ciclo **é uma ação no Action Log**, com dono e prazo, e a
governança sai de graça do bloco de pendências que já existe.

| Quando | O que acontece | Quem |
|---|---|---|
| **Terça**, no report das 06h30 | Pergunta na thread: *"Chegaram contas da Cassi? Valor e data de chegada."*, marcando a Fernanda | rotina pergunta |
| Terça | Resposta: `Chegou R$X em DD/MM` ou `Não chegou` | **Fernanda Jerônimo** |
| Terça, fechamento das 19h | Cria a ação `Processar as contas da Cassi recebidas em DD/MM (R$X)`, `Responsável` = Fernanda, `date:Prazo:start` = **data de chegada + 7 dias corridos** | rotina registra |
| Todo dia | A ação aparece no bloco de pendências como qualquer outra | rotina |
| Todo dia | Calcula o **processado acumulado** (fórmula abaixo) e escreve na página da ação | rotina |
| No 7º dia | `processado ≥ 98% do declarado` **e** lacuna `< R$50.000` → fecha 🟢 sozinha. Caso contrário → expõe a lacuna em reais e marca 🔴 **nosso** | rotina |

**O relógio conta da data de chegada, não da terça.** Se a remessa chegou quinta, a terça
seguinte já queimou 5 dos 7 dias. A terça é o dia da pergunta; o prazo nasce da data informada.

**Semana sem remessa não é vermelho nosso.** É cobrança externa: vira sinalização com
`Responsável` = Fernanda (é ela quem cobra a Cassi), contando os dias de espera pela guarda de 3
dias úteis. **Duas ou mais semanas seguidas sem remessa** é o sinal estrutural — escale à OM.

**Critério duplo de fechamento, e por quê.** A série tem revisão retroativa: em 21/09 um
incremento de R$350.351,33 apareceu na série no dia 16, depois do fato. Por isso o corte é 98%,
não 100% exato — arredondamento não pode virar alarme falso. Mas 2% de uma remessa grande é
dinheiro: 2% de R$3 milhões são R$60 mil. Daí a segunda trava, o piso de materialidade de
R$50.000 que a operação já usa desde 11/08. Acima dele, mesmo com 98%, quem fecha é a Fernanda.

### A fórmula do processado acumulado — e a virada do mês

O card 65831 calcula o mês corrente e a baseline de 3 meses sozinho, a partir de `CURRENT_DATE`:
ele **só devolve o mês atual**, e no dia 1º o acumulado zera. Um ciclo que atravesse a virada
leria delta negativo. A correção é aritmética, com duas âncoras gravadas na página da ação:

- **`V0`** — valor do `R$ Faturado Cassi` no dia da declaração. Gravado quando a ação é criada.
- **`Vf`** — valor lido no **último dia útil do mês**. Gravado **só** quando há ciclo aberto na
  virada.

```
Ciclo não cruza a virada:   processado = V_hoje − V0
Ciclo cruza a virada:       processado = (Vf − V0) + V_hoje
```

Exemplo: declaração em 26/09 de R$1.200.000, `V0` = R$2.800.000. Em 30/09 a leitura é
R$3.500.000 (grava `Vf`). Em 03/10 o acumulado de outubro está em R$500.000 →
`(3.500.000 − 2.800.000) + 500.000 = R$1.200.000`. Ciclo fechado.

As duas âncoras são leituras que a rotina **já faz todo dia** — só precisam ser escritas na
página da ação. Nenhum dado novo, nenhum card novo.

**Se `Vf` não existir** (a rotina não rodou no último dia útil), use a última leitura disponível,
escreva o caveat de imprecisão na página, e **mande o fechamento para confirmação da Fernanda** —
não feche sozinha.

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

Nesses **dez** KPIs o responsável **não é fixo**: depende de onde o desvio está concentrado. Você
só descobre isso **depois de executar o drill**, então o roteamento é a última coisa que se
decide, não a primeira.

**O drill de concentração não é opcional.** No teste de 17/09/2026 o `SLA Recurso de Glosa - HI`
saiu 🔴 sem ninguém ter quebrado o número por tipo — e quando se quebra, o resultado é gritante:
Hospital 34/35 dentro do SLA (97,1%), Laboratório 0/13 (0%). **13 das 14 fora do SLA são de
Laboratório (92,9%)**, muito acima do corte de 70%. O KPI tinha dono claro — Fernanda — e passou
dias sem ser roteado para ninguém. Um KPI roteável que sai sem a linha `Concentração:` é uma
execução incompleta, mesmo que a cor esteja certa.

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

**Casos conhecidos — cards que não devolvem tipo de instituição.** Enquanto forem estes, os KPIs
que dependem deles marcam **as duas** e escrevem a frase do passo 5:

| Card | KPI | O que devolve no lugar |
|---|---|---|
| **73490** | Recursos de Glosa Próximos do Vencimento | `institution_name`, `provider_economic_group` |
| **32465** | PEGs por Status de Análise no SLA - HI | status e contagem, sem dimensão de prestador |
| **73390** | PEGs Abertas por Dias Úteis (drill do 32465) | aging, sem dimensão de prestador |

Verificado em 17/09/2026. Quando qualquer um passar a devolver o tipo, tire a linha da tabela.

## OM

`<@U03A4SS2P1Q>` — Juliana Borges. Dona dos itens `A DEFINIR`, dos escalonamentos e do
mapeamento de responsáveis. **Não marcar por padrão** nas cobranças: só quando o item é
`A DEFINIR`, é da alçada dela, ou é escalonamento.
