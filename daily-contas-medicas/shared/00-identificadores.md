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
| 6 | Contas Médicas - Recursos de Glosa Próximos do Vencimento (≤3 dias) - HI | 73490 | diária |
| 7 | Contas Médicas - SLA de Análise de conta - HI | 65832 | diária |
| 8 | Contas Médicas - PEGs por Status de Análise no SLA - HI | 32465 | diária |
| 9 | Contas Médicas - Qnt de guias analisadas por dia | **76259** (Hospital e Clínica, metas separadas) | diária ⚠️ |
| 10 | Contas Médicas - % PEGs sem NF | 65694 | diária |
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

**⚠️ `Qnt de guias analisadas por dia`: recalibrado em 28/09/2026 (decisão da OM).** Passou a ter
**escopo Hospital + Clínica com metas separadas** e **card novo 76259**, com alvo capado pela fila disponível e leitura em 5 dias úteis.
Regra completa na seção "Qnt de guias analisadas por dia" abaixo; o catálogo do Notion é a fonte.

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

| # | KPI | Direção | O que cruza o limiar |
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

**Consequência imediata para a próxima execução:** com a direção correta, o
`R$ Recurso de Glosa acumulado` em **+128,65% sobre a média de 3 meses** (R$826.363,99 no dia 7
de Out/26 contra R$361.433,89) **é 🔴**, e nenhum episódio vigente o rebaixa — os de 21/09, 30/09
e 05/10 tratam de desvio para baixo, de sinal e mecanismo opostos. Abra episódio novo.
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
| Recursos de Glosa Próximos do Vencimento (≤3 dias) - HI | — sem drill próprio; o card 73490 já é a lista item-a-item |
| SLA de Análise de conta - HI | 65837 (guias/dia Hospitais) · 65839 (guias/dia Labs+Clínicas) · 32465 (PEGs por Status no SLA) |
| PEGs por Status de Análise no SLA - HI | 65837 · 65839 |
| Qnt de guias analisadas por dia | 73390 (PEGs abertas por dias úteis — a linha de 7 du vencendo hoje) |
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

## Qnt de guias analisadas por dia — fila disponível e produtividade (decisão da OM, 28/09/2026)

Até 27/09 este KPI comparava o **consolidado** (Hospital + Labs + Clínicas, card 65840) do dia
contra a `capacidade_esperada`, que **não é meta de negócio**: o SQL a calcula como a média móvel
dos 20 dias úteis anteriores do **próprio output do time**, com metade na segunda. Comparar um
processo em lote contra a própria média acende em cerca de metade dos dias por construção — medido
em 28/09/2026: **60 de 104 dias úteis vermelhos entre Mai e Set/26**. Não media desvio, media
oscilação.

**Card novo: 76259** — `Contas Médicas - Produtividade de Análise vs Fila Disponível - HI`,
criado em 28/09/2026 (collection 3662). Substitui o 65840 e o 65837 na rotina diária.

### A pergunta que o indicador responde

"O time analisou tudo o que dava para analisar naquele dia?" — e ela tem duas metades que **não
compartilham farol**:

| Pergunta | Grão | Onde vive |
|---|---|---|
| **Prazo** — sobrou PEG que não podia sobrar? | PEG | `PEGs por Status de Análise no SLA - HI` (32465 / 73390) — canônico, régua da OM de 22/09 |
| **Produtividade** — dado o que havia, o time produziu? | **linha (procedimento)** | **card 76259**, este KPI |

O time analisa **linha a linha**, então produtividade é medida em linha. Prazo é por PEG, porque o
SLA de 7 dias úteis é da PEG. Não misture: o card 76259 **não** recalcula prazo, e a tentativa de
fazê-lo divergiu do `analysis_on_time` canônico (o fecho por `MAX` das linhas é mais estrito).

### Como o 76259 mede

- **Entrada na fila** = `invoice_date`, a chegada da conta — mesma âncora do SLA de PEG.
- **Saída da fila** = `COALESCE(administrative_analysis_date, invoice_billed_step_date,
  disallowance_date)`. Fecha sem resíduo: **0% de linha fantasma** nos meses fechados da janela.
- **Analisadas** = linhas com `administrative_analysis_date` no dia — o trabalho de análise de fato.
- **Teto diário**, por time = o máximo que aquele time já analisou num dia útil (série
  Mai/25–Set/26): **Hospital 11.210** (23/02/2026) · **Clínica 4.311**. É a produtividade máxima
  demonstrada, não a média. Parâmetros `teto_hospital` e `teto_clinica`, editáveis sem mexer no SQL.
- **ALVO DO DIA = MIN(teto do time, base cobrável)** — não se cobra do time mais do que existe,
  nem mais do que ele consegue fazer num dia. **A base cobrável é diferente para cada time**
  (decisão da OM, 28/09/2026):
  - **Hospital → fila total do dia.** "Analisou tudo o que dava para analisar." Régua original.
  - **Clínica → só a fila vencida**, ou seja, o que entrou há **3 dias úteis ou mais** e segue em
    aberto. "Analisou tudo o que já deveria ter saído." Parâmetro `ciclo_du` do card.
- `capacidade_media_movel` (média móvel de 20 du) fica como **coluna de referência**, fora do farol.
- **Janela de exibição**: mês corrente + **mês anterior** (decisão da OM, 28/09/2026).
- **O teto não sai da janela.** Ele vem da série completa e confiável (**Mai/2025 em diante**),
  porque "o máximo que o time já fez" não deve encolher só porque a tela mostra menos dias. O
  estoque de abertura da janela também é calculado desde Mai/2025 — sem isso a fila vai a negativo.

### Farol

Leitura no **acumulado de 5 dias úteis**, nunca no dia isolado — a análise é feita em lote e a
série tem dias de 334 e dias de 8.124 linhas, ambos normais.

**O alvo de 5 du NÃO é a soma dos alvos diários.** Somar `MIN(teto, fila)` de cada dia contaria a
mesma fila parada cinco vezes e inflaria o alvo. O certo é:

```
disponiveis_5du = fila de abertura do 1º dia da janela + tudo que entrou nos 5 dias
alvo_5du        = MIN(5 × teto diário, disponiveis_5du)
```

- ⚪ alvo = 0 → **sem fila, não avalia**. Não tinha o que analisar.
- 🔴 abaixo de **80%** do alvo → abaixo da capacidade **tendo fila disponível**.
- 🟢 caso contrário.

**O farol é o `veredito_5du`** — decisão da OM em 28/09/2026. Os números (fila, alvo, aderência)
são calculados **diariamente**, dia a dia; o que a janela de 5 dias úteis muda é só o momento em
que o alarme dispara. O card também entrega `veredito_dia`, que fica como leitura de apoio, fora
do farol.

**Por que o alarme não é diário.** Com o alvo sendo a fila inteira, 80% num único dia é
inalcançável: o tempo mediano entre a chegada da conta (`invoice_date`) e a análise é de **3 dias**,
então a fila de qualquer dia carrega cerca de três dias de trabalho, e pedir 80% dela num dia é
pedir ciclo de um dia. A aderência diária observada tem mediana de **32%** — o time faz cerca de um
terço da fila por dia, consistente com o ciclo de 3 dias. Em 5 dias úteis, que é mais que o ciclo,
os 80% passam a ser uma cobrança justa.

| Veredito | Como lê | Dias 🔴 em 84 dias úteis |
|---|---|---|
| `veredito_dia` (apoio) | `analisadas < 80% de MIN(teto, fila do dia)` | 94% |
| **`veredito_5du` (farol)** | `analisadas_5du < 80% do alvo_5du` | **51%** |

Se a OM quiser menos vermelho, o corte é a alavanca: 80% → 51% dos dias · 70% → 40% · 60% → 31%
· 50% → 14%.

**O teto é a trava para pilha grande, e ainda não precisou funcionar.** Medido em 28/09/2026: a
maior fila disponível numa janela de 5 du foi **30.674 linhas**, contra 5 × 11.210 = 56.050 de
teto — o teto limitou o alvo em **0 de 84 dias**. Ele existe para o dia em que acumular mais do que
o time tem como fazer; enquanto isso, quem manda no alvo é a fila.

**O alvo capado pela fila resolve a sazonalidade sozinho**, sem tabela de fatores: quando a fila
drena no fim do mês, o alvo cai junto. Medido — 31/07 alvo 351 em vez de 2.633; 31/08 alvo 450 em
vez de 1.263; 25/09 alvo 1.520 em vez de 2.722.

**Como a régua se comporta (84 dias úteis, Jun–Set/26, Hospital):** 51% dos dias ficam 🔴 e 49% 🟢.
É uma régua exigente de propósito — o alvo é limpar a fila disponível a cada 5 dias úteis, e o
tempo mediano de conta na fila é de 3 dias, então é coerente. Ela discrimina evento real: na série
recente ficou 🔴 de 15 a 21/09, durante e logo após o pico de 9.989 entradas de 18/09, e voltou a
🟢 em 22/09 quando o time recuperou — 88,6%, depois 91,2%, 92,5% e 91,8%.

Se a OM quiser menos vermelho, **o corte é a alavanca, não o teto**: 80% → 51% dos dias · 70% →
40% · 60% → 31% · 50% → 14%.

O caso que motivou a mudança: em 28/09 o report publicou 🔴 com 451 guias contra capacidade de
15.151 (2,98%); pelo 76259, o acumulado de 5 dias úteis de 25/09 foi de **13.348 linhas contra
alvo de 14.534 — 91,8%, Dentro do esperado**.

### Escopo: Hospital e Clínica, com metas SEPARADAS

**São times diferentes** (decisão da OM, 28/09/2026), então cada um tem a sua fila, o seu teto e o
seu farol. O card devolve uma linha por dia **e por tipo**.

| Time | Teto diário | Quando | Mediana/dia | Dias 🔴 em 39 du |
|---|---|---|---|---|
| Hospital | **11.210** | 23/02/2026 | 1.408 | 56% |
| Clínica | **4.311** | 13/03/2026 (sexta) | 470 | **79%** |

**Como o teto foi calculado:** maior número de linhas analisadas num único dia útil por aquele
time, sobre toda a série confiável (Mai/2025 em diante, 344 dias úteis para Hospital e 294 para
Clínica). Não é pico solto em nenhum dos dois — os maiores dias se agrupam perto do topo:
Hospital 11.210 · 11.079 · 10.971; Clínica 4.311 · 3.869 · 3.796 · 3.660 · 3.614.

Se algum dia a OM preferir o teto calculado só na janela de 2 meses, os valores seriam
Hospital 11.079 e Clínica 3.869 — praticamente os mesmos.

**Laboratório está fora** — passou a ser analisado **em massa**, o que torna a leitura de
produtividade por linha sem sentido para ele. Centro de Diagnósticos nunca entrou (é o fluxo Cassi).
Os cards 65840, 65837 e 65839 saem da rotina diária.

**Por que Clínica tem régua própria.** Sob a régua da fila total, Clínica acendia em **79%** dos
dias contra 56% de Hospital, e as três alavancas foram testadas em 28/09 sem resolver:

| Alavanca | Testado | Resultado em Clínica |
|---|---|---|
| Janela | 6, 7, 8 e 10 du | 77% · 77% · 77% · 69% — travado |
| Teto | 3.869 · 3.000 · 2.424 · 2.000 | 79% · 79% · 79% · 74% — o teto só trava o alvo em 3% dos dias |
| Corte | 70% · 60% · 50% | só empurra o número |

A causa não era nenhuma das três: o alvo "zerar a fila inteira" fica sistematicamente acima do que
aquele time entrega. Em 5 dias úteis Hospital limpa **76%** da sua fila e Clínica **60%**. Trocando
a base de Clínica para a fila vencida, o indicador cai para **44%** e volta a discriminar — em
24/09 a fila vencida era 0 e ele analisou 3.213 (111,9%); em 22/09 a fila vencida era 5.633 e ele
analisou 634 (19,4%).

**A fila de Clínica não está represada** — a mediana é de 4 dias contra 3 de Hospital.

**A concentração por grupo econômico é normal e esperada — não reportar como achado** (confirmado
pela OM em 28/09/2026). A quebra da fila de Clínica mostra B-ACTIVE com 30,3% do tempo de fila
(6.003 linhas em 5 unidades: Paulista, Morumbi, Higienópolis, Chácara Flora e Moema), SALUDIA com
17,1% e EQUILIBRYUM com 8,4% — 55,8% nos três maiores. É o perfil normal da carteira de Clínica,
que tem poucos grupos grandes. Fica registrado aqui só para evitar que uma execução futura da
rotina redescubra isso e abra episódio indevidamente.

### Roteamento: volta a depender do tipo

Com Hospital e Clínica no mesmo KPI, o responsável **não é fixo**: Hospital → Alana
`<@U073Z4ENBNW>`, Clínica → Fernanda `<@U044N26BETU>`. Como o card já separa por tipo, o
roteamento sai direto da linha que acendeu — não precisa de drill de concentração.

### Além disso: PEGs vencendo hoje saem todo dia

Pedido da OM em 28/09. Independentemente do farol deste KPI, o report publica **todo dia** a linha
de PEGs em aberto com exatamente **7 dias úteis** — é o último dia útil para fechar dentro do SLA
interno, e é o que ainda dá para salvar.

**SEM filtro de tipo de instituição.** O escopo Hospital vale só para a produtividade; para prazo,
a OM quer ver **qualquer PEG vencendo**, inclusive Laboratório, Clínica e Centro de Diagnósticos.
Fonte: card **76260** (`PEGs em Aberto por Dias Úteis e Tipo de Instituição - HI`), criado em
28/09/2026, mesmo universo do 73390 e com a quebra por tipo e o valor em R$.

Fila em 28/09 — **63 PEGs em aberto, 0 vencendo hoje**:

| du | Tipo | PEGs | Valor |
|---|---|---|---|
| 1 | Hospital | 9 | R$156.220,72 |
| 1 | Clínica | 7 | R$32.063,00 |
| 2 | Laboratório | 7 | R$66.169,22 |
| 2 | Hospital | 5 | R$511.826,05 |
| 3 | Clínica | 4 | R$45.900,00 |
| 3 | Hospital | 3 | R$201.567,15 |
| 4 | Centro de Diagnósticos | 23 | R$1.171.626,05 |
| 4 | Clínica | 4 | R$11.250,00 |
| 6 | Hospital | 1 | R$36.412,84 |

### Por que a fila não sai do 65837 nem do 65838

Ambos testados em 28/09/2026 e descartados como fonte de fila:

- **65838** (`Diagnóstico diário de análise`) já tem a ideia certa — ele classifica
  `OK - sem fila suficiente` —, mas a fila dele é só **a entrada do dia**, então ignora o estoque
  que sobrou de ontem. E a entrada dele é `invoice_ready_step_date`, que é a etapa "3-Pronta": em
  **17,3% das linhas de Hospital ela é posterior à análise**. Não é a chegada da conta.
- **65837**: `entraram_na_fila` conta toda linha com `invoice_ready_step_date` e
  `analisado_pelo_time` só as já em `4-Faturada` — populações diferentes. Reconciliam no agregado
  (gap de 1,4% em 5 meses) mas o resíduo intramensal oscila entre 200 e 12.800 e **nunca zera**,
  então um gate "sem fila" sobre ele jamais dispararia.
- Em grão de linha com `invoice_date` → `COALESCE(...)`, e **só dentro da janela de 4 meses**, a
  fila fecha limpa. Fora da janela não fecha: o `administrative_analysis_date` só começou a ser
  preenchido em **Mai/2025** (Jan–Mar/25 são 100% nulos), o que criaria fila fantasma permanente.
  É por isso que a janela é curta, e não por performance.

**Quando reavaliar:** se a operação mudar a janela de recebimento de contas, ou se Laboratório
voltar a ser analisado linha a linha, revisite o escopo e o corte de 80%.

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

POR TIPO, SEM DRILL — o card 76259 já separa as linhas por tipo, então o roteamento sai da linha
que acendeu: Hospital → Alana <@U073Z4ENBNW> · Clínica → Fernanda <@U044N26BETU>
  - Qnt de guias analisadas por dia   (escopo Hospital + Clínica desde 28/09/2026; Laboratório fora)
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
