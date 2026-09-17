---
name: daily-contas-medicas-notion-page
description: Contas Médicas · 09h15 — Transforma a Execução de Rotina do dia na página canônica da daily (6 blocos), puxando os drills completos, e posta o link na thread da Mensagem 1. O horário fica no agendamento, não no texto.
---

Transforma a **Execução de Rotina de hoje** na **página canônica** da daily de Contas Médicas,
a partir do report que a tarefa `daily-contas-medicas-report-slack` postou no Slack às 06h30.

**Papel da página (canônica) × Slack (acionamento).** A página é a fonte oficial e completa; o
Slack é o canal de acionamento. Consequências:

- **Nada é truncado na página** — todos os KPIs, todos os prestadores, todas as pendências.
- Os limites de densidade valem **só para o Slack**; a página pode ser longa (é consultada,
  não lida no meio do turno).
- **Links de Metabase e de thread do Slack são permitidos na página**, de forma discreta. No
  Slack continuam proibidos.

**Regra base:** não recalcular Metabase para os valores de farol — use os valores já publicados
no Slack às 06h30. **Exceções (é para isso que esta tarefa roda 2h45 depois):**
1. os drills item-a-item dos 🔴 (a lista completa de prestadores/motivos que não cabe no Slack);
2. o detalhamento dos 🟡 — os que não cruzaram o limiar e os rebaixados de 🔴 por decisão vigente — que não vai para o Slack;
3. o **repuxe de ETL** (Passo 4).

Leia antes de começar: `shared/00-identificadores.md`, `shared/01-regras-de-registro.md`,
`shared/02-metabase.md`.

Inputs fixos — não pergunte:
- **Operação:** Contas Médicas — https://app.notion.com/p/37cf0f13146a8023b8ebe67185557704
- **Execuções de Rotina:** `collection://00d00405-31e2-4670-abd1-168e986e55e9`
- **Decision Log:** `collection://b619a21c-a5f8-4701-a477-f5d150f03066`
- **Action Log (Log Melhoria Contínua):** `collection://39ff0f13-146a-8001-b289-000b5fb3961c`
- **Canal Slack:** `C0BH03QKUKY`
- **Executor:** buscar via `notion-search` pelo email juliana.borges@alice.com.br
- **Data de referência:** hoje

**Regras de forma da página:**
- **Bold é a única ênfase; nunca itálico.** O que seria itálico (notas de contexto, referência
  de período, ressalva de amostra) vira texto simples.
- **Sem emoji nos títulos dos blocos** (`Bloco 1 · Resumo geral`, não `📊 Bloco 1 · …`).
  Continuam os emojis de farol 🔴 🟡 🟢 ⚪ (são informação) e o ícone dos callouts.
- **Cor só no título; nunca cor de fundo em toggle.** Não usar `gray_bg`, `red_bg`, `blue_bg`.
- **Um único separador `---`**, imediatamente antes do bloco de Fechamento do dia.
- **Ícone da página: 📋** (fixo, sempre).
- Largura total: **ajuste manual** — a API do Notion não seta essa preferência. A rotina não
  tenta setar.

---

## Passo 1 — Ler o report no Slack

No canal `C0BH03QKUKY`, localizar as mensagens do report de hoje e guardar os `ts` (os syncs
usam):

- **Mensagem 1:** cabeçalho + farol + headline + link do report. A legenda do farol está numa
  resposta na thread.
- **Vermelhos:** uma mensagem solta por KPI 🔴, com valor/meta/limiar, hipótese, ação sugerida e
  link do Decision Log. **Guarde o `ts` de cada uma** — é a thread onde o responsável responde.
- **Mensagem 4** (Sinalizações de risco e bugs) — guarde o `ts`.
- **Mensagem 5** (KPIs sem instrumentação), se houver.
- **Mensagem 6** (Pendências), se houver — **guarde o `ts`**: os syncs re-cobram nessa thread.

Se o report de hoje não existir no canal, **pare** e poste no canal
`⚠️ Página da daily não montada: report das 06h30 não encontrado no canal.` marcando
`<@U03A4SS2P1Q>`. Não invente números.

## Passo 2 — Localizar a Execução de Rotina de hoje

Query no data source de Execuções de Rotina por `Título da execução` = `Daily - Contas Médicas
- DD/MM/AAAA`. **ATUALIZE essa página** — não crie outra. Se não existir (o report das 06h30
falhou ao criá-la), crie com as properties do Passo 6 da tarefa 01 e siga.

Ao atualizar, confirme/complete as properties: `Status da execução`, `Resumo`,
`Insights gerados (count)`, `Executor`, `Página da execução`, `Decisões geradas`.

## Passo 3 — Reescrever o corpo nos 6 blocos

Substitua o corpo enxuto pela estrutura abaixo: **6 blocos (toggles) + Fechamento do dia
(callout no rodapé)**.

**Introdução (padronizada — o mesmo cabeçalho do Slack).** Sem parágrafo de objetivo variável:
título, data, referência do período e, quando houver, cobertura retroativa.

**Callout de Links de apoio (formato fixo — sempre os mesmos itens, na mesma ordem):**
Catálogo de KPIs · Dashboard Metabase (painel 1996) · Página da Operação · Mensagem 1 do report
no Slack. Não alternar entre linha corrida e lista — sempre o mesmo formato.

### Bloco 1 · Resumo geral

- Rótulo do placar, string fixa: **`Farol do dia`** (nunca "Placar de farol").
  Ex: `Farol do dia: 6 🔴 · 0 🟡 · 10 🟢 · 0 ⚪`.
- **Resumão de pendências**, logo abaixo do farol — uma linha de contagem, para decidir na
  daily se vale abrir o Bloco 5. Formato:
  `Pendências: {N} decisões · {M} ações em aberto ({V} vencidas)`. Se tudo zero:
  `✅ Sem pendências em aberto`. Vem do mesmo levantamento do Bloco 5; os syncs mantêm
  atualizada. O **detalhe** fica no Bloco 5 — aqui é só o número.
- A **tabela completa** de KPIs — todos os exibidos no dia, nada parcial. Colunas fixas:
  `KPI | Resultado | MTD | Meta | Limiar | Variação | Farol | Contexto`
  - **KPI:** nome do Notion sem o prefixo `Contas Médicas - `
  - **Resultado:** valor do período da cadência (ou acúmulo retroativo)
  - **MTD:** acumulado do mês até a data. A maioria dos cards de Contas Médicas já é
    `thismonth`, então MTD = Resultado nesses casos — escreva `= Resultado` em vez de repetir o
    número. Para os que têm janela diária, rode o **card agregado do próprio KPI** com a janela
    do mês. Se o card não aceitar janela de datas, exiba `—`.
  - **Meta:** `Meta atual` do Notion, ou `—`
  - **Limiar:** `Limiar de alerta`, encurtado para caber, sem mudar a condição
  - **Variação:** contra a meta, ou contra o baseline que o limiar nomeia. **Sempre indicar
    qual.**
  - **Farol:** conforme a classificação
  - **Contexto:** uma frase. **Obrigatória** quando o farol é 🟡 ou 🔴.
  - Ordem 1–17 de `00-identificadores.md`, sem seções. Semanais entram na sexta, na posição que
    ocupam, com a coluna `Período`.
- **Quando o farol de um KPI só é o que é por causa de decisão metodológica vigente**, diga isso
  na coluna Contexto, com o link da decisão. O leitor precisa saber qual régua foi usada.
- **Legenda do farol** (igual à do Slack):
  ```
  🟢 Dentro da meta · 🟡 Atenção, sem acionamento: dentro da meta com variação a monitorar, ou fora do limiar com o desvio já explicado por decisão vigente do OM · 🔴 Fora do limiar sem explicação vigente — acionamento imediato · ⚪ Sem dado ou sem meta — acompanhar tendência
  ```
- KPIs sem instrumentação (se houve Msg 5) ao final, com nota.

### Bloco 2 · Deep dives dos desvios

Um sub-toggle por KPI com desvio.

**Deep dive 🔴** — título (bold só no nome do KPI; contexto e responsável fora do bold):

```
🔴 **{KPI}** · {contexto curto} · {responsável}
```

Responsável = a pessoa do bloco de mapeamento (`00-identificadores.md`). Para os nove KPIs
roteados **por tipo de instituição**, o responsável sai da concentração do desvio no drill —
siga o procedimento de roteamento daquele arquivo e registre a linha
`Concentração: {tipo} ({%} do desvio) → {responsável}` logo abaixo do título. Enquanto um KPI
estiver `A DEFINIR`, escreva `A DEFINIR — alçada da OM`. Conteúdo:

- **Tabela resumo (horizontal):** `Indicador | Resultado | Meta | Limiar | Variação | Farol`.
- **Decisões vigentes que se aplicam:** link + 1 linha do que a decisão determina, ou
  `nenhuma`. Se houver decisão metodológica, diga qual janela/filtro foi usada no cálculo.
- **Tabela de drill — lista COMPLETA, puxada do card de drill** (não copiar do Slack: a página
  é canônica). Execute os cards de drill do KPI listados em `00-identificadores.md`, com os
  parâmetros da própria linha de processo no Notion. Nunca escreva SQL. Colunas conforme o que
  o card devolve, com **`Causa raiz` como última coluna** (só existe na página). Padrões:
  - **Glosa por prestador** (50958, 65700): `Prestador | Grupo econômico | R$ Faturado | R$ Glosado | % Glosa | % histórico | Desvio | Causa raiz`
  - **Glosa por motivo** (54617, 31223, 52037, 52038, 66204): `Motivo | R$ Glosado | % do total | Tipo de instituição | Causa raiz`
  - **Recurso de glosa** (54662, 54677, 65835): `Prestador ou Motivo | R$ Recursado | Qnt | % do total | Causa raiz`
  - **PEGs sem NF** (56231, 49800): `Prestador | Qnt PEGs sem NF | R$ | Dias no status | Causa raiz`
  - **Guias analisadas / SLA** (65837, 65839, 32465): `Tipo de instituição ou Status | Qnt | Capacidade esperada | % | Causa raiz`
  - **Faturamento** (65831, 26655, 50631): `Prestador ou Tipo | R$ do mês | Média histórica | Variação | Causa raiz`
  - **Críticas HS** (66766, 38203): `Fatura | Status da crítica | Dias no status | Motivo | Causa raiz`
  - **Etapas de pagamento HS** (35588): `Etapa | Dias úteis médios | Referência | Variação | Causa raiz`

  Ao agrupar por prestador, **consolide por grupo econômico** (Fleury/Delboni, rede Oswaldo
  Cruz, Einstein e unidades) e mostre as duas leituras: por unidade e por grupo.
  Onde o card não devolver uma coluna, deixe `—`. **Não invente coluna.**
- **Preenchimento da `Causa raiz`:** ⏳ em todas as linhas. Os syncs preenchem com o que o
  responsável responder na thread, casando pela entidade (prestador, motivo, fatura).
- **Linha final fixa:** `Decision Log: {link}`. Quando a entrada ainda não existir:
  `Decision Log: pendente de registro no sync`.
- **Campos que os syncs preenchem** (deixe com ⏳ agora):
  `💬 Resposta do responsável: Isolado ou padrão · Plano de ação · Owner · Prazo`
  `🗣️ Da daily síncrona: ⏳`
- **Sem "Hipótese" e sem "Possíveis impactos"** como seções próprias — a hipótese já está no
  Slack e no Decision Log; aqui o que interessa é a evidência do drill.

**Desvio 🟡 (só na página).** Não gera thread no Slack, existe apenas aqui. São dois tipos, e o
título diz qual é. Entrada própria, **sem** pedido de plano de ação.

**🟡 que não cruzou o limiar:**

```
🟡 **{KPI}** · fora da meta, dentro do limiar · sem acionamento

| Indicador | Resultado | Meta | Limiar | Variação | Farol |
|---|---|---|---|---|---|
| … | … | … | … | … | 🟡 |

{tabela de drill com as colunas do card, quando o KPI tiver drill}

Fora da meta, mas o limiar de acionamento não foi cruzado. Sem necessidade de deep dive humano com plano de ação.
```

**🟡 rebaixado de 🔴 por decisão vigente:**

```
🟡 **{KPI}** · cruzou o limiar, causa já decidida em {DD/MM} · sem acionamento

| Indicador | Resultado | Meta | Limiar | Variação | Farol |
|---|---|---|---|---|---|
| … | … | … | … | … | 🟡 |

Decisão vigente que rebaixou o farol: {link} — {o que ela determina}

{tabela de drill com as colunas do card}

O desvio está dentro do que a operação já decidiu. Sem necessidade de deep dive humano com plano de ação.
```

O drill do rebaixado é puxado **aqui** — é a razão de a página existir: o Slack só mostra a cor,
e é na página que se confere se o desvio continua sendo o mesmo que a decisão explicou.

**Quando a magnitude mudou**, o KPI não deveria ter sido rebaixado. Troque a frase final por:

```
O desvio tem causa decidida, mas a magnitude mudou de {valor de então} para {valor de hoje}. Isto é fato novo: o KPI deveria estar 🔴. Levar à OM como pergunta de horizonte, não como investigação nova.
```

e registre a divergência no rodapé de fechamento, para a OM conferir o farol do dia.

**Tolerância zero.** `SLA de Análise de conta - HI` e `PEGs por Status de Análise no SLA - HI`
nunca aparecem como 🟡 rebaixado. Abaixo de 90% eles são deep dive 🔴, com a decisão vigente na
linha `Decisões vigentes que se aplicam`.

**KPI do tipo "alerta de trabalho" (tabela em `00-identificadores.md`).** Não é deep dive: não
tem hipótese, não tem plano de ação, não tem link de Decision Log. É sub-toggle próprio, e é
**aqui que mora a lista completa item a item** — o Slack só leva o resumo e o consolidado.

```
📋 **{KPI}** · fila de trabalho · {responsável}

| Horizonte | Recursos | Valor | Leitura |
|---|---|---|---|
| Vencendo em até 3 dias | {N} | R$ {valor} | ainda dá pra salvar |
| Já vencidos, ainda em aberto | {M} | R$ {valor} | perderam o prazo de 15 dias, seguem abertos |
| Dentro do prazo (>3 dias) | {K} | R$ {valor} | contexto, sem ação hoje |
```

Depois, **duas tabelas completas**, sem truncar, direto do card:

- **Vencendo em até 3 dias**, ordenada por dias restantes crescente:
  `Dias restantes | PEG | Prestador | Grupo econômico | Protocolado em | Valor | Tratativa`
- **Vencidos, ainda em aberto**, ordenada por valor decrescente:
  `Dias vencido | PEG | Prestador | Grupo econômico | Protocolado em | Valor | Tratativa`

A coluna `Tratativa` nasce ⏳ e é preenchida pelos syncs com o que o time responder na thread,
casando por `PEG`. É o equivalente da `Causa raiz` dos deep dives.

Acrescente, abaixo das tabelas, a **consolidação por grupo econômico** do estoque vencido
(`Grupo | Recursos | Valor | Protocolados entre`) — é a leitura que mostra se o problema está
espalhado ou concentrado num prestador.

Escreva "vencido, ainda em aberto" e nunca "não acionável", que é o rótulo do card: o recurso
perdeu o prazo de 15 dias corridos, mas continua aberto e continua sendo trabalho.

**Tendência que ainda não é alerta.** `% Glosa por Tipo de HI` entre os dias 1 e 19 do mês
reporta a variação como tendência sem disparar 🔴 (regra de dois estágios do próprio limiar).
Nesses dias o KPI aparece no Bloco 1 com o número e a nota `tendência — estágio 1 (até dia 19)`,
e **não** abre entrada no Bloco 2.

### Bloco 3 · Cassi e faturamento — leitura de volume

Os dois KPIs de faturamento — `Faturamento total acumulado` e `R$ Faturado Cassi` — **têm
responsável e abrem deep dive normalmente no Bloco 2** quando 🔴. Este bloco não substitui o
deep dive: ele existe porque o número de faturamento só faz sentido com a leitura de volume ao
lado, e é dinheiro. Uma tabela:
`Indicador | Resultado | Média histórica | Variação | Dias sem movimento | Decisão vigente`.

A coluna **`Dias sem movimento`** existe porque o padrão de falha do Cassi é **estagnação** —
valor idêntico por dias consecutivos, que é incompatível com operação normal e já foi a
evidência que abriu a discussão em 13/08. Calcule pela série do card 65831 e reporte o número
de dias corridos com o mesmo total. Referencie a decisão vigente (11/08: atraso no envio pela
própria Cassi; 13/08: veredito Recusada) em vez de reabrir a causa.

### Bloco 4 · Sinalizações de risco e bugs

⏳ aguardando respostas na thread da Mensagem 4 e a daily síncrona — os syncs preenchem.

**Objetivo:** dar visibilidade ao que **não** está nos KPIs e ainda assim pode virar decisão ou
ação. Todo item entra com uma **leitura**.

**Só sinalizações NOVAS do dia.** O que foi sinalizado antes e continua aberto já virou
pendência e vive no Bloco 5 (ver `01-regras-de-registro.md` §7).

Três sub-seções **fixas** (sempre presentes; se vazia, `⚪ Nada sinalizado hoje`). Cada uma é
uma tabela, e a **última coluna de todas é `Leitura`**.

**4.1 · Casos e discussões em andamento**
Conta, prestador ou glosa que alguém está tratando com discussão paralela não centralizada
neste canal. O valor é trazer à superfície o que está sendo resolvido fora do canal oficial.
`Caso / prestador | Onde está a discussão | Quem está tratando | Situação | O que falta | Leitura`

**4.2 · Bugs abertos com tech ou dados**
Só os abertos **hoje**; os de dias anteriores estão no Bloco 5.
`Bug | Sistema (n8n / TOTVS / PLS / pertinência / Metabase) | Do que trata | Impacto na operação | Status | Aberto desde | Responsável | Leitura`

**4.3 · Problemas identificados na operação**
Pessoas off, absenteísmo, erro de execução, fluxo desalinhado, gargalo novo, fila acumulada.
`Problema | Tipo | Impacto | Desde | Responsável | Leitura`

**Coluna `Leitura` — valores fixos:**
- `→ Decisão` — precisa de alçada. Vira proposta de Decisão na thread (sync das 15h) e entra no
  Bloco 5.
- `→ Ação` — o caminho já está claro, falta executar. Vira proposta de Ação **com dono e
  prazo** e entra no Bloco 5.
- `→ Escalar` — passa da alçada da operação (tech, dados, jurídico, outra área). Nomear a quem.
- `→ Monitorar` — sem acionamento hoje. Não vira pendência; fica só na página do dia.
- `→ Sem dono` — ninguém assumiu. Dona por padrão: a OM. Nunca deixe item sem uma das cinco.

**Dedup antes de escrever:** confira se o assunto já está aberto no Bloco 5. Se estiver, é
atualização da pendência, não sinalização nova.

### Bloco 5 · Pendências

Vem **antes** do Resumo da daily de propósito: é o bloco lido em voz alta na daily síncrona.

**Tabela** (não bullets), colunas fixas: `Pendência | Fonte | Responsável | Venceu | Status`.
`Fonte` ∈ `Decision Log` · `Action Log` · `Deep dive` · `Bloco 4`. Varrer:

- **Decision Log:** `Status de execução` = `Em curso` **sem `Prazo` preenchido**; entradas com
  `Estado de complemento` = `Rascunho Claude` há mais de 1 dia útil, **apenas a ocorrência mais
  recente por KPI**; `Prazo` anterior a hoje. Os dois filtros são os mesmos da Mensagem 6 — ver
  **"Dois filtros obrigatórios no Decision Log"** em `01-report-slack/SKILL.md`. Bloco 5 e
  Mensagem 6 têm que listar **o mesmo conjunto**: se divergirem, a página e o canal contam
  histórias diferentes no mesmo dia. Havendo entradas omitidas por dedup, escreva sob a tabela
  `{X} entradas anteriores do mesmo KPI omitidas por dedup.`
- **Action Log:** `Status` = `Atrasada`, ou `Prazo` anterior a hoje com `Status` diferente de
  `Concluída` e `Cancelada`, ou `Status` = `A iniciar` sem prazo.
- **Deep dive:** 🔴 de dia anterior sem causa raiz / plano de ação / decisão (criado pela
  tarefa 05).
- **Bloco 4:** sinalizações de **dias anteriores** com `Leitura` = `→ Decisão` / `→ Ação` /
  `→ Escalar` que seguem abertas. `Venceu` = data em que foram sinalizadas. As de **hoje** não
  entram aqui — ficam no Bloco 4 até o fechamento.

Responsável vazio: escrever exatamente `A DEFINIR` (nenhuma outra variação).

**Uma linha por assunto.** Item que já está aqui não gera segunda linha nem volta ao Bloco 4 —
novidade sobre ele atualiza o `Status` desta linha. Vale também quando o assunto chega por outra
fonte (a sinalização virou ação no Action Log): mantenha **uma** linha, com a `Fonte` mais
específica e o link do registro.

Registre também, ao final do bloco, a linha `ts da thread de pendências no Slack: {ts}` — é
como os syncs acham a thread.

### Bloco 6 · Resumo da daily

**Último bloco da página** — fecha tudo, depois de todos os outros já terem sido lidos.

⏳ aguardando a daily síncrona. Preenchido pelo sync das 15h, marcador
**Resumo da daily · `[meet-sync DD/MM]`**. No topo: participantes + link da transcrição.
Registra o que a daily discutiu e não encaixa em outro bloco (decisões gerais, mudanças de
fluxo), cada item com responsável · prazo · link do Decision Log ou Action Log.

---

**Fechamento do dia** (callout, **não** toggle — único bloco após o separador `---`):
**Fechamento do dia · `[eod-sync DD/MM]`** — ⏳ aguardando fechamento, preenchido pelo sync das
19h.

**Cobertura retroativa:** se a Msg 1 indicar datas retroativas, refletir no título/introdução e
nas colunas por data do Bloco 1.

---

## Passo 4 — Link no Slack + repuxe de ETL

Postar o link da página como **resposta na thread da Mensagem 1**:

```
📋 Página da daily no Notion: {link}
```

**Repuxe de ETL (é aqui, às 09h15, que ele acontece).** Se algum 🔴 ficou às 06h30 com a lista
de drill **pendente por defasagem de ETL** (o agregado tinha o dado, o card de drill não),
agora — ao puxar o drill para montar a página — o ETL já costuma ter carregado. Poste a lista
como **resposta na thread daquele vermelho**, corrigindo a nota de pendência:

```
Drill repuxado às 09h15 — a lista completa está na página. Top concentradores: {…}
```

Nunca escreva SQL; só card por ID. Se mesmo às 09h15 o drill vier vazio, **mantenha a
pendência** e diga isso na thread (a `04-sync-pos-daily` tenta de novo como fallback).

**Se o valor do agregado mudou entre 06h30 e 09h15** (ETL fechou o dia anterior depois do
report): use o valor novo na página, e acrescente na coluna `Contexto` da linha
`Valor às 06h30: {X}; revisado às 09h15 para {Y} após fechamento do ETL.` Se a revisão **muda o
farol**, poste no canal uma correção na thread da Mensagem 1 — não reescreva a Mensagem 1 nem
poste um vermelho novo solto.

## Ao terminar

Responda apenas um resumo de uma linha: quantos blocos preenchidos, quantos drills puxados,
quantos repuxes de ETL, e o link da página.
