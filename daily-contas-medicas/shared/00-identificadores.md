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
| 5 | Contas Médicas - SLA Recurso de Glosa - HI | **76364** (prazo contratual por lote) | diária ⚠️ |
| 6 | Contas Médicas - Recursos de Glosa Próximos do Vencimento (≤3 dias) - HI | 73490 · resumo **79437** · drill **79438** | diária ⚠️ |
| 7 | Contas Médicas - SLA de Análise de conta - HI | 65832 | diária |
| 8 | Contas Médicas - PEGs por Status de Análise no SLA - HI | **76805** (fila viva, `invoice_date` ≥ 2025) | diária ⚠️ |
| 9 | Contas Médicas - Qnt de guias analisadas por dia | **65837** (escopo Hospital, dois gates + fator sazonal) | diária ⚠️ |
| 10 | Contas Médicas - % PEGs sem NF | **79935** (régua de 29%) · drill **79936** | diária ⚠️ |
| 11 | Contas Médicas - Faturamento total acumulado | 65831 | diária |
| 12 | Contas Médicas - R$ Faturado Cassi | 65831 | diária |
| 13 | Contas Médicas - % Resumos Criticados - HS | 30858 | diária |
| 14 | Contas Médicas - Status das Críticas (por fatura) - HS | 66766 | diária |
| 15 | Contas Médicas - Tempo para Resolução de Críticas - HS | 48840 | diária ⚠️ |
| 16 | Contas Médicas - % Faturas por Status - HS | 30863 | diária |
| 17 | Contas Médicas - SLA de Pagamento de HS | **35629** (oficial) · 76484 (mesmo número + complementos) | diária |
| 18 | Contas Médicas - % Recurso de Glosa | 65833 | **mensal — nunca entra nesta rotina** |
| 19 | Contas Médicas - Ciclo de processamento Cassi | 65831 (sem card próprio) | **semanal — pergunta na terça, ver seção do ciclo Cassi** |

**⚠️ `Tempo para Resolução de Críticas - HS`: metade do limiar é inverificável.** O limiar diz
`Tempo médio de resolução > 3 dias; ou crítica específica > 10 dias sem resolução`. Sem drill
cadastrado, **só a média mensal é apurável** — a segunda cláusula nunca pode ser checada. Reporte
o KPI pela primeira cláusula e escreva no Caveat, todo dia:
`segunda cláusula do limiar (crítica > 10 dias) não verificável — sem card de drill`.
Quando um drill for cadastrado, esta nota sai.

**⚠️ `% PEGs sem NF`: régua trocada em 27/10/2026 (decisão da OM) para os cards 79935 e 79936.**
O denominador deixou de ser "PEGs com PLS maduro" e passou a ser **PEGs em status faturado**
(`invoice_step = '4-Faturada'`); o numerador são as que não têm NF vinculada; o limiar é **>29%** e
**não há piso de maturação**. O farol sai da linha do **mês corrente**. Regra completa na seção
"% PEGs sem NF" abaixo; o catálogo do Notion é a fonte.

**⚠️ `Qnt de guias analisadas por dia`: a régua válida é a do card 65837, não a do 76259.** A
divergência foi resolvida pela OM em 30/09/2026: escopo **apenas Hospital**, fonte **65837**, com
**dois gates** (SLA de Análise abaixo de 100% no mês e ao menos 1 PEG em aberto na fila viva) e meta
= `capacidade_esperada × fator sazonal`, lida no acumulado de 5 dias úteis com corte de 80%.
O card 76259 chegou a ser criado em 28/09 e **foi descartado** — se aparecer em algum lugar
`veredito_5du`, `teto_hospital`, `teto_clinica` ou "fila vencida de Clínica" como régua deste KPI,
está desatualizado. Regra completa na seção abaixo; o catálogo do Notion é a fonte.

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

## Direção de cada KPI — declarada, nunca inferida

Esta tabela existe porque a execução de 07/10/2026 **inferiu** a direção do
`R$ Recurso de Glosa acumulado` como "maior é melhor" e usou a regra de direção de
`01-regras-de-registro.md` §1 para suprimir um 🔴 de **+128,65%** sobre a média de 3 meses.
A OM corrigiu no mesmo dia. Direção não se deduz do nome do KPI, da `Definição` nem de
raciocínio sobre o que seria bom para a operação: **lê-se aqui**.

A coluna **"O que gera 🔴"** diz em que sentido o desvio é acionamento. O sentido oposto nunca
gera 🔴, mas gera **🟡 de variação favorável atípica** quando tem a mesma magnitude do limiar —
regra completa em `01-regras-de-registro.md` §1. Nos KPIs bidirecionais os dois sentidos são 🔴 e
a regra de variação favorável não se aplica.

| # | KPI | Direção | O que gera 🔴 |
|---|---|---|---|
| 1 | % Glosa Geral - HI | menor é melhor | alta |
| 2 | % Glosa por Tipo de HI | menor é melhor | alta |
| 3 | % Glosa Alice por Prestador - HI | menor é melhor | alta |
| 4 | **R$ Recurso de Glosa acumulado** | **menor é melhor** | **alta** |
| 5 | SLA Recurso de Glosa - HI (aderência %) | maior é melhor | queda |
| 6 | Recursos de Glosa Próximos do Vencimento (≤3 dias) - HI | menor é melhor | alta |
| 7 | SLA de Análise de conta - HI | maior é melhor | queda |
| 8 | PEGs por Status de Análise no SLA - HI | menor é melhor | alta |
| 9 | Qnt de guias analisadas por dia | maior é melhor | queda |
| 10 | % PEGs sem NF | menor é melhor | alta |
| 11 | Faturamento total acumulado | **bidirecional** | alta e queda (o limiar diz "para cima ou para baixo") |
| 12 | R$ Faturado Cassi | bidirecional | alta e queda, e só nos dois checkpoints do mês (classe monitoramento) |
| 13 | % Resumos Criticados - HS | menor é melhor | alta |
| 14 | Status das Críticas (por fatura) - HS | menor é melhor | alta |
| 15 | Tempo para Resolução de Críticas - HS | menor é melhor | alta |
| 16 | % Faturas por Status - HS | menor é melhor | alta |
| 17 | SLA de Pagamento de HS (% fora do prazo) | menor é melhor | alta |

**A linha 4 é declaração direta da OM (Juliana Borges, 07/10/2026):** *"esse indicador nunca é
'quanto maior melhor'. Esse indicador é 'quanto MENOR melhor'."* O valor recursado é o que os
prestadores contestam das glosas aplicadas pela Alice — volume subindo é mais contestação, mais
trabalho e mais risco de devolver glosa. Não reinterprete.

**Direção boa não é silêncio.** Na mesma conversa a OM definiu que queda grande também aparece:
*"é bom mas é um sinal de desvio do padrão que gostaria de ter visibilidade para entender se é um
potencial erro estrutural ou se de fato é melhoria."* Daí a classe **🟡 de variação favorável
atípica** — mesma magnitude do limiar, no sentido bom, com teste de sanidade e pergunta
obrigatória. Ela nunca vira 🔴 e nunca abre episódio.

**Consequência imediata para a próxima execução:** com a direção correta, o
`R$ Recurso de Glosa acumulado` em **+128,65% sobre a média de 3 meses** (R$826.363,99 no dia 7
de Out/26 contra R$361.433,89) **é 🔴**, e nenhum episódio vigente o rebaixa — os de 21/09, 30/09
e 05/10 tratam de desvio para baixo, de sinal e mecanismo opostos. Abra episódio novo.

**O episódio novo abre com dois dias de história, não um.** A alta começou em **06/10**, quando o
KPI marcou +59,39% e a execução daquele dia fechou o episódio tratando a subida como resolução.
Sob a direção correta aquele dia já era 🔴. O `Contexto / problema` do episódio novo precisa
registrar os dois dias: 06/10 em +59,39% (não reportado) e 07/10 em +128,65% (não reportado), com
a nota de que a lacuna foi de leitura e não de dado.
O drill de 07/10 já está levantado e deve ser reaproveitado: Hospital +105,29% (R$564.307,88
contra R$274.880,31, 59,6% do excedente) e Laboratório +253,50% (R$273.359,27 contra R$77.328,95,
40,4%) — nenhum tipo passa de 70%, então roteia para as duas. Por motivo, o destaque é o
**7EL — código cobrado diferente do autorizado, R$86.448,03 em 7 dias úteis contra média mensal
de R$11.086,42 em Jul–Set**, quase 8× a média de um mês inteiro em uma semana; mais 7G4
duplicidade R$94.716,94 (média R$54.924,56) e dois motivos sem histórico nenhum no trimestre,
7F7 cobrança fora do prazo contratual R$32.477,09 e 7G1 sem cobertura pelo plano R$24.125,29.
Por prestador, é pulverizado: CIP Pacaembu Fleury 20,0%, Associação dos Médicos Einstein 14,0%
e HCOR 13,6% somam 47,7% de 32 prestadores no mês.

**Os demais KPIs desta tabela foram derivados do texto do `Limiar de alerta` do catálogo, não
declarados pela OM.** Se alguma linha estiver errada, a correção é aqui e vale na execução
seguinte — do mesmo jeito que a linha 4.

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
| Recursos de Glosa Próximos do Vencimento (≤3 dias) - HI | **79437** (linhas abertas por PEG, janela de 3 du) · **79438** (itens em aberto na janela de alerta) |
| SLA de Análise de conta - HI | 65837 (guias/dia Hospitais) · 65839 (guias/dia Labs+Clínicas) · 32465 (PEGs por Status no SLA) |
| PEGs por Status de Análise no SLA - HI | **76805** (fila viva por dias úteis e tipo de instituição) |
| Qnt de guias analisadas por dia | — sem drill próprio; o 65837 já devolve `entraram_na_fila`, `analisado_pelo_time` e `capacidade_esperada` |
| % PEGs sem NF | **79936** (fila de NF item a item, com `horizonte` e `bloco`) · 56231 e 49800 são complementares e não aplicam a régua |
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

**`% PEGs sem NF` SAIU desta classe em 27/10/2026.** Ele entrou em 21/10 porque o limiar zero o
tornava vermelho permanente, e com a régua de 29% voltou a ser termômetro: quando acender, abre
episódio no Decision Log com hipótese e plano de ação, como qualquer outro KPI.
**O que continua é a fila**, por decisão da OM na mesma data: o resíduo das competências fechadas
segue publicado todo dia na thread do KPI, como lista com dono, rolando até zerar — só que agora
como *contexto* do indicador, não como o próprio farol. Sob 29% as competências fechadas rodam entre
0,24% e 0,87% e nunca mais acendem sozinhas; sem a lista, a cobrança do estoque antigo se perderia
junto com o vermelho que a sustentava. Detalhe na seção "% PEGs sem NF" abaixo.

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

## SLA de Pagamento de HS — lê o mês corrente (decisão da OM, 28/09/2026)

Até 27/09 o KPI era lido sobre o **mês fechado**, e era vermelho previsível: o mês fechado não se
move mais, então não há ação possível sobre ele. Passa a ser lido sobre o **mês corrente**, que é
onde ainda dá para agir. Card **35629**, inalterado — muda a linha que a rotina lê, não a fonte.

Efeito imediato: Ago/26 fechado dá **3,29%** (38 fora de 1.156 classificadas), acima do limiar de
3%; Set/26 corrente dá **1,42%** (15 de 1.058). O KPI sai do 🟡 rebaixado e vai para 🟢.

> **Correção de 30/09/2026 — grão.** Em 28/09 eu registrei aqui 3,31% e 1,62%, contando
> `DISTINCT invoice_id`. O card 35629 conta **linhas** de um `SELECT DISTINCT` sobre
> (`eita_code`, `note_number`, `batch_pls`, datas…). A rotina compara contra o card, então os
> números desta seção são os do card. A decisão de ler o mês corrente não muda.

**O denominador não é problema.** As faturas HS chegam em lote no início do mês: até o dia 10 o mês
já tem praticamente todas. Medido (faturas com vínculo, por dia do mês):

| Mês | até dia 5 | até dia 10 | mês todo |
|---|---|---|---|
| Mai/26 | 6 | 1.163 | 1.167 |
| Jun/26 | 0 | 1.196 | 1.198 |
| Jul/26 | 0 | 1.209 | 1.211 |
| Ago/26 | 0 | 1.223 | 1.226 |
| Set/26 | 1.175 | 1.176 | 1.177 |

**Mas a leitura do mês corrente é OTIMISTA por construção, e isso precisa sair no caveat todo dia.**
O card só classifica a fatura depois que ela tem pagamento apurado. Em 30/09 o Set/26 tem 1.198
faturas com vínculo e **1.058 classificadas (88%)** — as restantes ainda não pagaram, e pagamento que
atrasa entra como "fora do prazo". Ou seja, o percentual do mês corrente tende a **subir** conforme o
mês liquida. Mesmo um mês fechado não classifica 100%: Ago/26 tem 1.156 classificadas de 1.229 com
vínculo.

**E a subida é lenta de enxergar**, porque `invoice_payment_date` entra na base com até ~8 DU de
atraso (ver aviso abaixo). Entre 28 e 29/09 o Set/26 saltou de 927 para 1.048 classificadas sem que
nada tenha sido pago naquele dia — era registro chegando.

**Guarda de materialidade:** enquanto o mês corrente tiver **menos de 100 faturas classificadas**,
não acenda farol — saia ⚪ com o número e cite o mês anterior como contexto. É a janela dos
primeiros dias do mês, antes de o lote ser processado.

**Caveat obrigatório na linha do KPI, todo dia:**
`mês corrente parcial — {n} de {N} faturas classificadas; o percentual tende a subir conforme os
pagamentos liquidam`.

**A segunda cláusula do limiar segue não verificável** (`prestador específico com > 2 faturas
consecutivas fora do prazo`): o card não devolve a sequência por prestador. Mantida a nota no
caveat até existir drill.

### A NF do HS é o marco inicial — fatura sem NF não entra no cálculo

O prazo de pagamento só começa a correr quando o **HS manda a nota fiscal**. Sem NF não há como
pagar, então fatura sem NF não é atraso da Alice e **não entra no cálculo** — nem no numerador nem
no denominador. Card **76484**, que substitui o 35629 na leitura da rotina.

**O que é "fatura sem NF válida"** (qualquer uma das três condições exclui):

| Condição | O que significa |
|---|---|
| `invoice_binding_date IS NULL` | a NF nunca foi vinculada à fatura |
| `note_date IS NULL` | não há data de emissão de NF |
| `invoice_status IN ('RECEIVED','WAITING_INVOICE','WAITING_RESEND_INVOICE')` | a fatura está aguardando o HS enviar (ou reenviar) a NF |

O `WAITING_RESEND_INVOICE` é o furo que o 35629 não fechava: a NF foi enviada, **rejeitada**, e a
fatura está esperando o HS reenviar. Ela tem `invoice_binding_date` preenchido, então passava pelo
filtro do 35629 e o relógio seguia correndo contra a Alice num período em que a bola estava com o
HS. São poucas (1 em Set/26, 1 em Ago/26, 2 em Jul/26) e nenhuma chegou a ser paga, então **nenhum
número histórico muda** — mas a regra fecha a porta.

**Nenhum percentual histórico se alterou** com a nova régua, porque o 35629 já filtrava
`invoice_binding_date is not null` e isso já excluía `RECEIVED` e `WAITING_INVOICE`. Conferido mês a
mês: Out/25 19,49% · Nov/25 2,85% · Dez/25 4,61% · Jan/26 29,95% · Fev/26 4,12% · Mar/26 1,82% ·
Abr/26 2,34% · Mai/26 2,72% · Jun/26 2,48% · Jul/26 3,70% · Ago/26 3,31% · Set/26 1,62%. O ganho é
de definição e de blindagem, não de número.

**A categoria `(fora do calculo) sem NF do HS` é só visibilidade — NÃO é achado.** O card devolve
essa linha para mostrar o volume represado, e o volume é alto por natureza: uma fatia dos HS fatura
no fim do mês. Medido na mesma altura do mês (dia 28), o represamento é estável:

| Mês | faturas sem NF no dia 28 | % do mês | sem NF até hoje (resíduo) |
|---|---|---|---|
| Mar/26 | 139 | 12,5% | 3 |
| Abr/26 | 133 | 11,6% | 14 |
| Mai/26 | 137 | 11,6% | 15 |
| Jun/26 | 136 | 11,2% | 11 |
| Jul/26 | 131 | 10,7% | 12 |
| Ago/26 | 73 | 5,8% | 31 |
| **Set/26** | **131** | **10,0%** | 131 (mês ainda corrente) |

Ou seja: os 131 de Set/26 são **o padrão, não uma anomalia** — e quase todos resolvem sozinhos até o
fechamento (o resíduo dos meses fechados fica entre 3 e 31). **Não reportar como achado, não abrir
episódio, não acender farol por esse número.** Ele só vira assunto se passar de ~15% do mês na
mesma altura, ou se o resíduo do mês fechado passar de ~40.

**Onde essas faturas devem ser acompanhadas:** no KPI **% Faturas por Status - HS** (card 30863),
que é o indicador do funil de faturamento do HS — não aqui. Esse é justamente o KPI da Pendência 7
(dono e horizonte a definir, prazo 29/09).

### O número oficial é o do card 35629 — os complementos ficam em linha separada

> **Correção de 29/09/2026.** Durante a recalibração eu mudei o marco inicial do KPI para
> `note_date` (emissão da NF) e misturei as faturas em aberto no percentual. As duas coisas juntas
> levaram o indicador de 1,43% para 29,60% em Set/26 — **isso estava errado** e a OM apontou. O
> número oficial é e continua sendo o do **35629**. O card 76484 agora o reproduz sem nenhuma
> alteração e trata o resto como complemento fora do percentual.

**Como o 35629 calcula** — e é essa a régua canônica:

| Elemento | Definição |
|---|---|
| Marco inicial | `invoice_binding_date` — o **vínculo da NF no eita**, quando a nota do HS entra no sistema |
| Marco final | `invoice_payment_date` — o pagamento efetivo na TOTVS |
| Medida | `working_days_from_note_binding_to_payment`, em **dias úteis** |
| Corte | `<= 5 DU` → `no prazo (<=5WD)`; acima → `fora do prazo (>5WD)` |
| Universo | só fatura **com NF vinculada** (`invoice_binding_date is not null`) e **já paga** (`payment_status = 'pago'`) |
| Mês de referência | mês de `invoice_date` (criação da fatura), **não** o mês do pagamento |
| Exceções | três ajustes de feriado fixos: pagamentos em 29/12/2025 descontam 2 DU; em 21/11 e 27/11/2025 descontam 1 DU |

`% fora = fora do prazo / (no prazo + fora do prazo)`.

**O que o 35629 deixa de fora, por construção** (medido em 29/09, grão `eita_code`):

| Mês | Total de resumos | Sem NF vinculada | Com NF, não pago | **Entra no gráfico** |
|---|---|---|---|---|
| Abr/26 | 1.149 | 14 | 66 | 1.069 |
| Mai/26 | 1.182 | 15 | 64 | 1.103 |
| Jun/26 | 1.209 | 11 | 69 | 1.129 |
| Jul/26 | 1.223 | 12 | 72 | 1.139 |
| Ago/26 | 1.257 | 28 | 76 | 1.153 |
| **Set/26** | **1.308** | **119** | **144** | **1.045** |

- **Sem NF vinculada** = `RECEIVED` + `WAITING_INVOICE`: o HS ainda não mandou a NF. Em Set/26 são
  99 + 20. Volume alto é normal no mês corrente (ver seção acima).
- **Com NF, não pago** = entrou no sistema mas ainda não liquidou. Em Set/26 são 144, sendo **104 sem
  lote PLS** e **40 com PLS e sem pagamento**, R$ 311.063,06 em aberto.

**Por que uma fatura fica "fora do prazo"** — o 35629 já traz o motivo em `check_sla_payment_reason`,
que o 76484 passa a expor:

| Motivo | Regra | Set/26 |
|---|---|---|
| `atraso pagamento` | total vínculo→pagamento > 5 DU | 8 |
| `atraso operacao` | vínculo→lote PLS > 2 DU | 6 |
| `atraso operacao e pagamento` | as duas coisas | 1 |

Cuidado ao ler: `atraso operacao` dispara por vínculo→PLS > 2 DU **mesmo quando o total ficou dentro
dos 5 DU** — em Set/26 há 19 faturas assim, classificadas como `no prazo` com motivo
`atraso operacao`. O motivo descreve onde o tempo foi gasto, não substitui o veredito.

**As três linhas de complemento do 76484** (`complemento - em aberto, ja estourou`,
`complemento - a vencer`, `complemento - sem NF do HS`) **não entram no percentual**. Elas existem
porque a OM pediu visibilidade do atraso real, e a visibilidade não pode custar a comparabilidade do
número oficial. Set/26 em 29/09: 58 em aberto já acima de 5 DU, 86 a vencer, 119 sem NF.

**O limiar de 3% continua válido**, porque o número oficial não mudou. Set/26 está em **1,43%** 🟢.

### As duas etapas dos 5 DU — o KPI é a visão geral, o acionável é a etapa 1

Esclarecimento da OM (29/09/2026): os 5 DU se dividem em duas etapas com times diferentes.

| Etapa | Trecho | Prazo | Quem executa |
|---|---|---|---|
| **1** | vínculo da NF no eita → **lote PLS** | **2 DU** | **time de Contas Médicas** |
| **2** | lote PLS → pagamento | 3 DU | Contas a Pagar |

**O KPI não se divide.** Continua sendo a visão geral dos 5 DU, com um dono só e o roteamento que já
existe. A etapa 1 é **o acionável do time quando o KPI desvia**, e o card 76484 a expõe na coluna
`motivo`.

Isso explica o `atraso operacao` em faturas classificadas como `no prazo`: a etapa 1 estourou os
2 DU mas a etapa 2 absorveu a folga. **É aviso antecipado, não erro de classificação.**

> ### ⚠️ `pls_batch_date IS NULL` **não** significa que o lote não foi gerado
>
> Correção de 30/09/2026, depois de a OM apontar o card **35588** como fonte da verdade do que tem
> ou não PLS. Em Set/26 há **96 faturas pagas com `pls_batch_date` nulo, 92 delas dentro dos 5 DU**.
> Elas fluíram normalmente — o campo simplesmente não está preenchido nessa base. **Contar todo
> `pls_batch_date IS NULL` como falha de etapa 1 está errado**, e foi o que eu fiz: reportei
> 14–17% de falha na etapa 1 quando o número real é **8–9%**.
>
> **E o 35588 não consegue desmentir nem confirmar isso sozinho**, por duas razões:
> `working_days_from_binding_to_pls` é **NULL em 100%** das linhas sem `pls_batch_date` (184 de 184
> em Set/26), e `AVG` ignora nulo — então fatura sem PLS **nunca entra na média**. O 35588 mede a
> velocidade de quem passou pela etapa, não quantos não passaram. As duas leituras são compatíveis:
> média de 1,19 DU em Set/26 **e** uma cauda de ~8% fora dos 2 DU.

**Como medir a etapa 1 corretamente** — grão **fatura** (`eita_code`), não o grão de linha do 35583:

- `e1_dentro` = tem `pls_batch_date` e `working_days_from_binding_to_pls <= 2`
- `e1_fora` = tem `pls_batch_date` e `> 2 DU`
- `e1_travada` = **sem PLS e sem pagamento**, há mais de 2 DU do vínculo
- **não mensurável** = paga sem `pls_batch_date` → fica **fora do numerador e do denominador**

| Mês | base | dentro 2 DU | fora c/ PLS | travada | **% fora etapa 1** | não mensurável | % fora oficial |
|---|---|---|---|---|---|---|---|
| Mar/26 | 1.112 | 950 | 12 | 67 | **7,68%** | 83 | 1,91% |
| Abr/26 | 1.135 | 951 | 21 | 65 | **8,29%** | 98 | 2,52% |
| Mai/26 | 1.167 | 999 | 14 | 63 | **7,16%** | 91 | 2,72% |
| Jun/26 | 1.198 | 1.004 | 30 | 68 | **8,89%** | 96 | 2,48% |
| Jul/26 | 1.211 | 1.011 | 35 | 71 | **9,49%** | 94 | 3,85% |
| **Ago/26** | 1.229 | 878 | **190** | 65 | **22,51%** | 93 | 3,30% |
| Set/26 | 1.198 | 987 | 27 | 67 | **8,70%** | 96 | 1,43% |

**Ago/26 é o único desvio real**: 190 faturas receberam lote PLS acima de 2 DU, contra 12 a 35 nos
outros meses. Bate com o 35588, onde Ago/26 tem a maior média de vínculo→PLS dos quatro meses
(1,75 DU contra 1,17–1,20).

**A cauda de "travadas" é estrutural, não acionável.** Fica em 63 a 71 faturas em todo mês, inclusive
nos fechados, e nos meses fechados soma **R$ 0,00** de valor em aberto — são faturas zeradas ou
canceladas que nunca completam o fluxo. Não reportar como achado; só vira assunto se sair dessa faixa.

**Situação de Set/26 em 30/09** (grão fatura):

| Grupo | Faturas | Acima de 2 DU | Valor em aberto |
|---|---|---|---|
| Aberta **sem** PLS | 88 | 67 | R$ 8.952,19 |
| Aberta **com** PLS | 55 | 53 | R$ 430.340,02 |
| Paga sem `pls_batch_date` | 96 | — | — (92 dentro dos 5 DU) |

Ou seja: o volume travado na etapa 1 é pequeno em dinheiro (R$ 8,9 mil); o dinheiro aberto está na
etapa 2, que não é ação do time.

> **Cuidado com o grão.** O 35629 e o 35583 contam linhas de um `SELECT DISTINCT` sobre
> (`eita_code`, `note_number`, `batch_pls`, datas…), não faturas. Em Set/26 são 104 **linhas** sem
> PLS para 88 **faturas**. As linhas de complemento do 76484 seguem o grão do card oficial, para o
> percentual bater; qualquer contagem de **faturas** precisa agrupar por `eita_code` antes.

### ⚠️ Latência de registro do pagamento — a linha "em aberto" é TETO, não fato

`invoice_payment_date` entra na base com atraso de até **~8 dias úteis**. Medido entre 28 e
29/09/2026, sem nada ter mudado na operação, as faturas de Set/26 em aberto e já estouradas caíram de
**157 para 57**: 103 delas tinham data de pagamento de **17/09** e só apareceram pagas na base no dia
29 — todas **dentro do prazo**.

**Consequências na leitura diária:**

1. Nunca afirmar que as faturas da linha de complemento *estão* atrasadas. Elas são o **teto** do
   atraso possível naquele dia.
2. Nunca abrir episódio no Decision Log com base só nessa linha.
3. Queda dessa linha entre dois dias **não é melhora da operação** — é registro chegando.
4. O farol e o limiar se aplicam **só** ao percentual oficial do 35629.

## SLA Recurso de Glosa - HI — prazo contratual por lote (decisão da OM, 28/09/2026)

O card **60527** aplica um prazo único de 15 dias a todo recurso. O lote do **DASA recebido entre
21 e 25/09/2026** tem prazo contratual de **30 dias úteis**, e sob a régua de 15 ele seria
marcado como "fora do prazo" a partir do 15º dia — derrubando a aderência do mês por erro de régua,
não por atraso da operação.

> **Correção de 29/09/2026.** A OM primeiro confirmou "corridos" e no mesmo dia corrigiu para
> **dias úteis**. O card 76364 foi implementado com `DATEDIFF(day, ...)` (corridos) e agora usa o
> índice de dias úteis de `curated.dim_date_public` — a mesma régua dos 15 DU padrão. Se aparecer
> em algum lugar "30 dias corridos" ou vencimento em 21–25/10, está desatualizado.

**Vencimento do lote, em 30 dias úteis:**

| Recurso recebido em | Vence em | (dias corridos equivalentes) |
|---|---|---|
| 21/09/2026 | **04/11/2026** | 44 |
| 22/09/2026 | **05/11/2026** | 44 |
| 23/09/2026 | **06/11/2026** | 44 |
| 24/09/2026 | **09/11/2026** | 46 |
| 25/09/2026 | **10/11/2026** | 46 |

A mudança de corridos para úteis **não altera nenhum número hoje** — sob as duas réguas o lote
inteiro ainda está "A vencer". Ela empurra o vencimento de 21–25/10 para 04–10/11, ou seja, dá mais
duas semanas de folga antes de o lote começar a pesar no indicador.

**Card novo: 76364** — `SLA Recurso de Glosa - HI (prazo contratual por lote)`. Idêntico ao 60527
em tudo (classificação recurso a recurso, contagem de PEGs distintas por balde, janela de 4 meses
por `appeal_date`, aderência = Dentro / (Dentro + Fora) com "A vencer" fora do denominador), com
uma única exceção: o lote DASA da janela recebe o prazo de 30 **dias úteis**. Parâmetros `dasa_ini`,
`dasa_fim` e `prazo_dasa`, editáveis sem mexer no SQL.

**A correção é neutra hoje e protetiva depois.** Medido em 28/09:

| | Aderência Set/26 |
|---|---|
| Card 60527 (atual) | 68,72% |
| Card 76364 (corrigido) | **68,72%** — idêntico |
| 76364 em ~10/10, lote no prazo de 30 DU | 68,72% |
| 60527 em ~10/10, lote virando "fora do prazo" | **33,09%** |

São **210 PEGs** do lote, contra 195 no denominador atual — por isso a queda seria de 35 pontos.

**Atenção: "filtrar fora" literalmente seria o movimento errado.** Excluir os recursos do DASA da
semana passada do cálculo **piora** a aderência de hoje, de 68,72% para 66,67%, porque os 12 que já
foram resolvidos estão todos dentro do prazo e sustentam o número. O que corrige é dar a eles o
prazo certo, não removê-los.

**Quando o lote expirar** (04–10/11), as PEGs que seguirem sem análise passam a contar como Fora do
SLA normalmente — o prazo é maior, não infinito. Se outro lote com prazo diferenciado chegar,
ajuste os três parâmetros ou acrescente uma cláusula análoga.

## Qnt de guias analisadas por dia — dois gates e meta sazonal (decisão da OM, 28 e 30/09/2026)

> ⚠️ **A régua válida é a do card 65837, confirmada pela OM em 30/09/2026.** Entre 28 e 30/09 este
> arquivo e o catálogo descreveram uma régua diferente — card 76259, escopo Hospital + Clínica, tetos
> e filas separadas, farol pela coluna `veredito_5du`, sem gate nenhum. **Essa régua foi descartada.**
> Se aparecer em algum lugar `card 76259`, `teto_hospital 11.210`, `teto_clinica 4.311`, `ciclo_du`,
> "fila vencida de Clínica" ou `veredito_5du` como régua deste KPI, está desatualizado.

**Escopo: apenas Hospital.** Laboratório e Clínica saem do indicador. Fonte: card **65837**, que
devolve `dia`, `entraram_na_fila`, `analisado_pelo_time` e `capacidade_esperada`, sem parâmetros.

### Dois gates antes de qualquer avaliação

Se **qualquer um dos dois** fechar, o KPI sai ⚪ — sem farol, sem hipótese, sem plano de ação e
**sem episódio** no Decision Log:

1. **Gate de SLA** — o KPI só é avaliado se `SLA de Análise de conta - HI` (card 65832) estiver
   **abaixo de 100%** no mês corrente. Em 100%, sai ⚪. A razão é o próprio sentido do indicador: se
   ninguém está perdendo prazo, quanto se analisou por dia é **capacidade**, não desvio. Este gate é
   o que impede o KPI de acender em dia de fila baixa, que foi o defeito da régua anterior.
2. **Gate de fila** — só é avaliado se houver ao menos **1 PEG em aberto** na fila viva (card
   **76805**, que substituiu o 73390 em 30/09/2026). Fila vazia não se cobra.

### A meta e o farol

`meta do dia = capacidade_esperada × fator sazonal da faixa do dia do mês`:

| Faixa do dia do mês | 01–07 | 08–14 | 15–21 | 22–24 | 25 ao fim |
|---|---|---|---|---|---|
| Fator | 1,0 | 1,0 | 0,9 | 0,3 | 0,3 |

O fator existe porque a fila drena no fim do mês: cobrar capacidade cheia no dia 28 é cobrar
trabalho que não existe.

**Leitura no acumulado de 5 dias úteis, nunca no dia isolado** — a análise é feita em lote e a série
tem dias de 334 e dias de 8.124 linhas, ambos normais. Dias sem `capacidade_esperada` (fim de semana
e feriado) ficam fora da janela.

- 🔴 `analisado_pelo_time` acumulado nos 5 du **< 80%** da meta acumulada nos mesmos 5 du;
- 🟢 caso contrário.

### Roteamento fixo

Com escopo Hospital, o responsável é sempre **Alana Beckmann** `<@U073Z4ENBNW>`. Este KPI **não**
roteia por concentração e saiu da lista de KPIs roteáveis por tipo de instituição, que passou de dez
para nove.

### Prazo não entra neste KPI

PEGs vencendo em 7 dias úteis saem de `PEGs por Status de Análise no SLA - HI` (card **76805**), que
é canônico para prazo. Os dois não compartilham farol.

### ⚠️ Defasagem de ETL

O card costuma **não ter a linha do dia corrente às 06h30**, e um dia que entra na janela com
`entraram_na_fila = 0` **e** `analisado_pelo_time = 0` é **carga incompleta, não parada da
operação** — se o time tivesse parado, as entradas teriam continuado a chegar. Aconteceu em 24/09 (o
repuxe das 09h15 corrigiu 6.436 para 6.954), 28/09 e 30/09. Leia sempre a janela dos 5 últimos dias
**com dado**, e reexecute às 09h15 antes de tratar queda como desvio.

### Por que a régua anterior (até 27/09) não funcionava

`capacidade_esperada` **não é meta de negócio** — o SQL a calcula como a média móvel dos 20 dias
úteis anteriores do **próprio output do time**, com metade na segunda. Comparar um processo em lote
contra a própria média, sem gate e sem fator sazonal, acende em cerca de metade dos dias por
construção: **60 de 104 dias úteis vermelhos entre Mai e Set/26**. Os dois gates e o fator sazonal
corrigem isso sem trocar a fonte.

### O que o descarte do 76259 custou, e por que está registrado aqui

Em 30/09/2026 a régua do 76259 produziu 🔴 (Hospital em 79,8% do alvo de 5 du) e a rotina publicou
esse vermelho. **Pela régua correta o KPI era ⚪**: o `SLA de Análise de conta - HI` estava em
100,00% no mês (2.169 de 2.169 PEGs finalizadas no prazo), o gate de SLA fecha e o indicador nem
chega a ser avaliado. E mesmo com o gate aberto o resultado seria 🟢 — acumulado de 5 du de 4.069
analisadas contra meta de 3.607,5, ou seja 112,8%, bem acima do corte de 80%. O episódio aberto
naquele dia foi encerrado por régua incorreta.

Fica registrado para que uma execução futura não redescubra o 76259 e volte a tratá-lo como
canônico. Os cards **65840** (consolidado) e **65839** (Labs + Clínicas) também estão fora da rotina
diária desde 28/09/2026.

### A concentração por grupo econômico na fila de Clínica não é achado

Confirmado pela OM em 28/09/2026. B-ACTIVE responde por 30,3% do tempo de fila de Clínica (6.003
linhas em 5 unidades), SALUDIA por 17,1% e EQUILIBRYUM por 8,4% — 55,8% nos três maiores. É o perfil
normal da carteira. Registrado aqui só para evitar que uma execução futura abra episódio indevido.
Clínica está fora do escopo deste KPI desde 30/09, mas a observação segue valendo para quem olhar a
fila.

### Além disso: PEGs vencendo hoje saem todo dia

Pedido da OM em 28/09. Independentemente do farol deste KPI, o report publica **todo dia** a linha
de PEGs em aberto com exatamente **7 dias úteis** — é o último dia útil para fechar dentro do SLA
interno, e é o que ainda dá para salvar. **Sem filtro de tipo de instituição**, do card **76805**.

### Quando reavaliar

Se a operação mudar a janela de recebimento de contas, ou se Laboratório voltar a ser analisado
linha a linha, revisite o escopo e o corte de 80%.

## % PEGs sem NF — PEGs faturadas sem vínculo de NF (decisão da OM, 27/10/2026)

O indicador responde a uma pergunta só: **das contas que já foram faturadas, quantas saíram sem a
nota fiscal vinculada?** O momento de referência é o avanço da PEG para a fase 4 (Faturada), que é
quando a análise é finalizada e a NF já deveria ser anexada.

| Elemento | Definição |
|---|---|
| População (denominador) | PEGs em status faturado — `invoice_step = '4-Faturada'` |
| Numerador | Dessas, as que não têm nenhuma NF vinculada (`invoice_number` vazio em todos os itens) |
| Limiar | **> 29% → 🔴** |
| Piso de maturação | **Não existe.** A régua é instantânea e vale todo dia |
| Janela | Ano corrente |
| Grão | A PEG |
| Farol | A linha do **mês corrente**. Competências fechadas saem como contexto e como fila |

**Cards: 79935** (`% PEGs faturadas sem NF por competência (régua de 29%)`) · **drill: 79936**
(`Fila de NF: PEGs faturadas sem vínculo de NF - HI`), os dois criados em 27/10/2026 na collection
3609. **Nenhum dos dois aceita parâmetro** — execute sem parâmetros.

### Por que 29%, e por que a régua anterior saiu

A régua de 21/10 (piso de 13 DU pós-PLS, limiar ZERO) acendia 🔴 em todas as competências de 2026
por construção. Palavras da OM em 27/10/2026: o alerta *"não tem ação prática do time"* — um resíduo
de 3 a 25 PEGs por competência é cobrança de documento, não desvio de operação.

O time levantou que **~70% das contas chegam já com a nota fiscal**. Nessas, ao finalizar a análise
a NF já deveria ser vinculada no ato. A fatia que legitimamente ainda não tem documento em mãos é,
portanto, da ordem de 30% — e a OM fixou o corte em **29%**, meio ponto abaixo do espelho direto do
estudo, para que o limiar fique estritamente **dentro** da faixa explicada pelo levantamento. Acima
disso não é mais falta de documento, é atraso de operação. Nas palavras da OM, o acionamento existe
*"para que a gente possa analisar e entender se realmente é só uma falta do documento fiscal ou se
não, se é um atraso ali da operação que a gente precisa atuar"*.

### O piso de maturação não é necessário, e isso foi medido

Curva de chegada da NF por dias úteis desde o faturamento, sobre as PEGs faturadas de 2026 (medida
em 27/10/2026):

| du | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 18 | 21+ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| % sem NF | 20,8 | 23,2 | 7,0 | 14,1 | 14,4 | 7,2 | 3,6 | 10,1 | 13,3 | 17,0 | 10,7 | 1,7 | 25,2 | 20,5 | 19,7 | 19,0 | 0,0 | 0,4 |

**Mesmo a coorte mais nova fica abaixo dos 29%** — o pico é 23,2%, em 2 du, com 5,8 p.p. de folga.
Uma leitura feita no começo do mês, com a competência cheia de PEGs recém-faturadas, **não** produz
vermelho falso. Era exatamente esse o defeito que derrubou o piso de 7 DU da régua de 07/10. Por
isso não há guarda de materialidade nem estado de "em maturação": a régua é instantânea.

### As duas colunas de contexto são o deep dive pronto

O 79935 devolve `sem_nf_ate_2du` (faturadas há até 2 du — prazo normal de emissão) e
`sem_nf_acima_2du` (faturadas há mais de 2 du). Quando o percentual cruzar os 29%, é a segunda
coluna que diz se a causa é documento ou operação.

> ⚠️ **"Acima de 2 du" não é, sozinho, atraso confirmado.** A curva acima mostra que a NF segue
> chegando até cerca de 18 du do faturamento. O recorte é de diagnóstico; quem fecha o diagnóstico é
> a idade dentro do bloco, que o 79936 devolve PEG a PEG em `du_desde_faturamento`.

### A fila do resquício continua saindo todo dia (decisão da OM, 27/10/2026)

Sob 29% as competências fechadas **nunca mais acendem farol sozinhas** — elas rodam entre 0,24% e
0,87%. Mesmo assim o resíduo delas continua sendo publicado todo dia **na thread do KPI**, como fila
de cobrança com dono, rolando até zerar. Palavras da OM: *"mantenha a fila do resíduo das
competências anteriores sendo trazida na thread"*.

Era o vermelho permanente que mantinha a lista viva na frente do time. Tirando o vermelho sem tirar
a lista, a cobrança do estoque antigo continua acontecendo — é a separação entre "o indicador está
sob controle" e "ainda há trabalho a fazer".

O card 79936 devolve a coluna `horizonte`, que separa `Resquicio de competencia fechada` de
`Mes corrente (farol)`. **A fila publicada na thread é o primeiro bloco**, consolidada por grupo
econômico em ordem decrescente de valor — a ordem de cobrança.

### Leitura de 27/10/2026, a primeira sob esta régua

- **Out/26** (mês corrente, farol): 244 de 2.046 PEGs faturadas sem NF = **11,93%** · R$3.837.414,57
  → 🟢, com 17 p.p. de folga. Composição: 28 PEGs até 2 du e 216 acima de 2 du.
- **Competências fechadas de 2026, todas 🟢:** Jan 0,24% · Fev 0,34% · Mar 0,27% · Abr 0,48% ·
  Mai 0,37% · Jun 0,87% · Jul 0,29% · Ago 0,26% · Set 0,30%.
- **Resquício para cobrança:** 57 PEGs · R$499.632,52 — ABA ABC 24 PEGs (R$314.093,60, 62,9%) ·
  PEDIAKINDER 8 (R$66.560,00) · HAOC 1 (R$59.313,09); os três somam 88,1%.

O KPI sai de 🔴 permanente por construção para 🟢 em todas as linhas.

**Pergunta deixada em aberto para a OM:** o sub-recorte de "acima de 2 du" merece limiar próprio? É
onde estão 216 das 244 PEGs de Out/26, somando R$3.462.314,67, e hoje ele sai como contexto e não
aciona nada.

### ⚠️ Histórico de fonte — cinco saltos, série não comparável ponta a ponta

- **até 05/10** — card 65694, sem piso de idade. Out/26 marcava 82,46% em 02/10.
- **06/10** — card 77275, piso de 7 DU pós-PLS, série mensal.
- **07/10** — cards 77507 e 77508, três horizontes sobre o ano corrente, piso de 7 DU.
- **20/10** — cards 78774 e 78778, coorte madura por competência, piso de 13 DU, limiar de 1% e
  depois zero (21/10).
- **27/10** — cards 79935 e 79936, % de PEGs **faturadas** sem NF, limiar de 29%, sem piso.

Nenhum dos cards anteriores é mais a fonte deste KPI.

**Não comparar números entre réguas.** Nas competências fechadas as duas últimas populações quase se
sobrepõem (Set/26 dá 0,30% nas duas), mas no mês corrente divergem muito: em 27/10 a régua antiga
dava 22,06% (75 de 340 maduras) e a nova dá 11,93% (244 de 2.046 faturadas). São perguntas
diferentes.

### ⚠️ A janela de ano corrente não é arbitrária

Fora dela o número não é fila, é **artefato de base**: `invoice_number` só passa a ser preenchido de
fato em **Mar/2025** (Jan/25 98,7% e Fev/25 93,8% sem NF; Mar/25 cai para 2,9%). Se a janela for
ampliada algum dia, **o piso é 01/03/2025, nunca antes**.

### Filtros herdados, preservados desde o card base 68915

`provider_class = 'Health Institution'` · `typing_location = '0002'` · `fee_type <> 'captation'` ·
`payment_value` diferente de zero · exclusão dos 13 `institution_code` internos e das 2 PEGs
excluídas na mão. A decisão é tomada **no grão da PEG** (entra se qualquer item estiver em
`4-Faturada`; tem NF se qualquer item tiver `invoice_number`), e o resultado é determinístico.

✅ **O bug de reconciliação de valor entre 78774 e 78778 não se repete aqui.** O 79935 e o 79936 usam
a mesma base de valor (`SUM(payment_value)` no grão da PEG), então o drill fecha com o agregado: o
resquício soma R$499.632,52 nos dois.

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
  - Faturamento total acumulado

ROTEAMENTO FIXO — escopo apenas Hospital desde 30/09/2026, então o responsável não depende de
concentração: Hospital → Alana <@U073Z4ENBNW>
  - Qnt de guias analisadas por dia   (escopo Hospital; Laboratório e Clínica fora)
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
