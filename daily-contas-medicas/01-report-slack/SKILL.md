---
name: daily-contas-medicas-report-slack
description: Contas Médicas · 06h30 — Report de KPIs no Slack (farol + vermelhos + sinalizações + pendências) e criação da Execução de Rotina enxuta no Notion. A página canônica da daily é montada pela tarefa daily-contas-medicas-notion-page.
---

Execute o report diário de KPIs da Operação Contas Médicas seguindo o padrão OOS.

**Esta tarefa faz o Slack + a Execução de Rotina enxuta no Notion.** A **página canônica**
da daily (6 blocos, drills completos, tabelas item-a-item) é responsabilidade da tarefa
`daily-contas-medicas-notion-page`, que roda às 09h15, lê estas mensagens do Slack e
**enriquece a mesma página** — não cria outra.

Por que a página enxuta nasce aqui: a Mensagem 1 traz a linha `Report completo: <link>`, que
o time já usa. O link tem que existir às 06h30. O que a tarefa das 09h15 faz é transformar
essa página no formato canônico.

Leia antes de começar, e siga integralmente:
- `daily-contas-medicas/shared/00-identificadores.md`
- `daily-contas-medicas/shared/01-regras-de-registro.md`
- `daily-contas-medicas/shared/02-metabase.md`

Inputs fixos — não pergunte, não peça confirmação:
- **Operação:** Contas Médicas — https://app.notion.com/p/37cf0f13146a8023b8ebe67185557704
- **Canal Slack:** `C0BH03QKUKY`
- **Executor:** juliana.borges@alice.com.br (resolver o Notion user ID por `notion-search`,
  `query_type: "user"`, antes de criar qualquer página)
- **Data de referência:** hoje

---

## Regra de forma — o report é uma série, não um texto novo por dia

O layout deste report **não é decisão sua**. Títulos, rótulos e blocos fixos são strings
literais deste arquivo e devem ser copiados caractere por caractere. Você decide o conteúdo
analítico (quais KPIs são 🔴, quais hipóteses, qual plano); nunca a forma. Se algum elemento
de formatação não estiver especificado aqui, use o formato da execução anterior no canal em
vez de inventar um novo.

**Ênfase.** No Slack, `_itálico_` é a ênfase usada hoje no nome do KPI e no cabeçalho —
mantenha exatamente como está nos modelos abaixo. Não acrescente bold onde os modelos não têm.

**Densidade.** Um único nível de parênteses por frase. Não repita nos vermelhos números que já
apareceram no cabeçalho.

**Nada é truncado.** Toda lista mostra todos os itens. Lista longa → encurte cada linha, nunca
corte itens.

**Links.** Só dois tipos: a página da daily no Notion e as entradas de Decision Log / Action
Log. Nenhum link de Metabase, dashboard ou thread no Slack (na página do Notion eles são
permitidos). Todo link fecha a linha. URLs do Notion sempre em `https://app.notion.com/p/<id>`.

**Menções.** Só por ID (`<@U044N26BETU>`). Nunca escreva o nome antes ou depois da menção.

---

## Passo 1 — KPIs do dia

Leia o catálogo de KPIs (`collection://4c8ffc67-b817-48db-ab8c-04cb5c0c731e`) e selecione as
linhas em que:

- `Operação` contém Contas Médicas, **e**
- `Priorizado para rotina?` contém a cadência do dia:
  - `Reportar diariamente` → entra todo dia
  - `Reportar semanalmente` → entra **apenas na sexta**, na mesma tabela, na posição que ocupa,
    com a coluna `Período` indicando que a linha é da semana
  - `Reportar mensalmente` → **nunca entra nesta rotina** (hoje: `% Recurso de Glosa`)
  - `Não priorizado` → nunca entra

Para cada KPI capture: `Nome do KPI`, `Definição`, `Meta atual`, `Limiar de alerta`, `Caveats`,
`Tipo de métrica`, `Escopo`, `ID Card metabase`, `Parâmetro metabase`, `Dashboard oficial`,
`Status instrumentação`.

Se nenhum KPI satisfizer o filtro, pare e avise a OM. Não invente KPIs.

Ordem de exibição: a lista 1–17 de `00-identificadores.md`. Não reordene por farol.

## Passo 2 — Decisões vigentes (ANTES de calcular qualquer valor)

Monte o mapa `KPI → decisões vigentes`, classificando em metodológica / explicativa, conforme
`01-regras-de-registro.md` §2. **Este passo vem antes do cálculo de propósito** — decisão
metodológica muda a janela do card, e farol calculado sobre baseline que a OM já mandou
corrigir é alerta falso.

## Passo 3 — Valor de cada KPI

Conforme `02-metabase.md`. Aplique a janela/filtro que a decisão metodológica vigente
determinar. Para todo KPI 🔴, execute também os cards de drill da tabela de
`00-identificadores.md`.

**Gate duro:** nunca escreva "usar o card X para investigar" como plano de ação sem já ter
executado o card X.

## Passo 4 — Farol

Conforme `01-regras-de-registro.md` §1. Confira, antes de publicar:

- **todo KPI 🟡 que cruzou o limiar tem o link da decisão vigente que o rebaixou** (§1, Etapa 2).
  Sem link citado, o KPI volta a ser 🔴. `SLA de Análise de conta - HI` e `PEGs por Status de
  Análise no SLA - HI` abaixo de 90% são 🔴 sempre, sem rebaixamento;
- **fato novo cancela o rebaixamento:** magnitude que mudou, achado novo em KPI de processo ou
  prazo estourado devolvem o KPI para 🔴, com o fato novo como pergunta ao OM;
- as condições escritas dentro do `Limiar de alerta` foram aplicadas — piso de materialidade
  (`% Glosa Alice por Prestador`), piso de idade (`% Faturas por Status - HS`), regra de dois
  estágios por dia do mês (`% Glosa por Tipo de HI`), janela de risco (`PEGs por Status no SLA`);
- a contagem do farol considera só os KPIs efetivamente exibidos no dia, e KPI sem dado (⚪) não
  pontua.

## Passo 5 — Análise e plano de ação (só 🔴)

Para cada 🔴: hipótese ancorada em evidência de drill + plano de ação (o quê, por quê,
resultado esperado) + `Classe da decisão`. KPI 🟡 não gera plano de ação nem entrada no
Decision Log — o contexto dele fica na página.

Se o 🔴 já tem causa decidida e não há fato novo, o plano de ação é **registrar que não há ação
nova** e referenciar a decisão vigente. Se houver fato genuinamente novo, apresente **apenas o
fato novo** e formule como pergunta à OM (magnitude que mudou, prazo estourado, achado novo em
KPI de processo).

Sem base para hipótese → escreva "hipótese a investigar". Não invente causa.

## Passo 6 — Execução de Rotina enxuta no Notion

Crie a página em `collection://00d00405-31e2-4670-abd1-168e986e55e9`. Guardrail de `parent` e
confirmação por SQL: `01-regras-de-registro.md` §3.

**Se já existir a página da daily de hoje, ATUALIZE** em vez de duplicar.

Properties:
- `Título da execução` = `Daily - Contas Médicas - DD/MM/AAAA`
- `Nome da rotina` = igual ao título
- `Operação` (relation) = `["https://app.notion.com/p/37cf0f13146a8023b8ebe67185557704"]`
- `Cadência` = `Daily`
- `Tipo de ritual` = `Máquina — relatório`
- `date:Data da execução:start` = data de referência (ISO)
- `Status da execução` = `Publicada` / `Parcial` / `Falhou`
- `Resumo` = `{n} KPIs · {v} verde / {a} amarelo / {r} vermelho. {headline}`
- `Insights gerados (count)` = nº de desvios
- `Executor` (person) = `["{user ID da OM}"]`
- `Página da execução` (url) = a URL da própria página
- `Decisões geradas` (relation) = preencher no Passo 7

Ícone da página: **📋** (fixo, sempre — nunca 📊).

Corpo da página nesta etapa (enxuto; a tarefa das 09h15 reescreve nos 6 blocos):

```
# Daily Contas Médicas — DD/MM/AAAA
Farol: 🟢 {v} · 🟡 {a} · 🔴 {r}   ·   Executor: {nome}
Referência: {descrição do período e datas}
## Resultado dos KPIs
(tabela: KPI | Resultado | Meta | Limiar | Farol | Caveats)
## Análise de desvios
### 🔴 {KPI}
- Resultado: {valor} vs meta {meta} (limiar: {limiar})
- Decisões vigentes que se aplicam: {referência com link, ou "nenhuma"}
- KPIs de processo executados: {nome}: {valor} …
- Hipóteses: {hipóteses ancoradas em evidência}
- Plano de ação sugerido: {plano} → Decision Log: {link}
### 🟡 {KPI}
- Resultado: {valor} vs meta {meta} (limiar: {limiar})
- Motivo do 🟡: {não cruzou o limiar} OU {rebaixado de 🔴 pela decisão vigente de DD/MM: link}
- Hipóteses: {hipóteses}
## KPIs verdes
{lista enxuta: nome + valor}
## KPIs sem dado
{nome + o que foi tentado e por que falhou}, se houver.
## ⏳ Página canônica
Os 6 blocos, os drills completos e as tabelas item-a-item são montados às 09h15 pela tarefa
daily-contas-medicas-notion-page nesta mesma página.
```

Use ⚪ para KPI sem dado. Público é OM/GM — objetivo, sem jargão.

## Passo 7 — Decision Log (1 entrada por 🔴)

Uma entrada por KPI vermelho, como rascunho, com os campos de `01-regras-de-registro.md` §3.
Aplique **dedup de 14 dias** e a regra de **vermelho persistente** antes de criar.

**Exceção: KPIs do tipo "alerta de trabalho"** (tabela em `00-identificadores.md`) **não geram
entrada no Decision Log**, nem quando 🔴. Fila de trabalho não é decisão. Eles viram linha de
pendência na Mensagem 6, com o rótulo `[Fila]`.

Depois de criar, volte na Execução de Rotina e preencha `Decisões geradas` com as URLs.

**Esta tarefa não cria ações no Action Log.** Às 06h30 ainda não existe conclusão validada —
as threads acabaram de ser abertas. Ação é registrada no fechamento (tarefa 05), só com o que
tiver OK humano.

---

## Passo 8 — Postagens no Slack

Poste no `C0BH03QKUKY`, direto (sem draft), **nesta ordem**. As mensagens 1, 4 e 6 vão sempre;
as 2 e 5 são condicionais.

### Mensagem 1 — cabeçalho e farol (sempre)

Formato literal, idêntico ao que o canal já recebe:

```
_Daily Contas Médicas — DD/MM/AAAA_
Farol: 🟢 {v} · 🟡 {a} · 🔴 {r}
{headline em 1 linha}
Report completo: {URL Notion}
```

A **headline** é uma linha e diz o que mudou, não o que existe. Padrão que já funciona:
quantos dos vermelhos são continuação de crônico já escalado sem decisão, e quais são alertas
**novos** — nomeando-os. Ex: `5 dos 7 vermelhos são continuações de problemas crônicos já
escalados sem decisão do OM (...); 1 alerta novo: SLA de Pagamento de HS.`

Quando houver cobertura retroativa, acrescente **uma única** linha `Referência: <período e
datas>` logo abaixo do cabeçalho. Não crie uma segunda linha de "cobertura retroativa".

**Guarde o `ts` desta mensagem** — a legenda, a página do Notion e a Mensagem 5 entram como
resposta nesta thread.

### Legenda do farol — resposta na thread da Mensagem 1 (sempre)

Para não poluir o panorama, a legenda **não** fecha a Mensagem 1. String literal imutável:

```
🟢 Dentro da meta · 🟡 Atenção, sem acionamento: dentro da meta com variação a monitorar, ou fora do limiar com o desvio já explicado por decisão vigente do OM · 🔴 Fora do limiar sem explicação vigente — acionamento imediato · ⚪ Sem dado ou sem meta — acompanhar tendência
```

### Mensagem 2 — uma mensagem solta por KPI 🔴 (condicional)

Mensagens **separadas no canal**, não em thread. Não poste para KPIs das listas SEM
RESPONSÁVEL. KPIs 🟡 **não** geram mensagem — o contexto deles fica na página.

```
🔴 _{KPI}_ — {valor} (meta {meta} · limiar {limiar})
Hipótese: {hipótese}
Ação sugerida: {plano}
Decision Log: {URL}
```

Quando o vermelho já tem causa decidida, **diga isso na própria mensagem** em vez de sugerir
ação nova:

```
🔴 _{KPI}_ — {valor} (meta {meta} · limiar {limiar})
Causa já decidida em {DD/MM}: {decisão}. Sem ação nova.
{fato novo, se houver, formulado como pergunta à OM}
Decision Log: {URL}
```

Marque o responsável do KPI (bloco de mapeamento) ao final da mensagem, pedindo retorno na
thread:

```
↩️ <@ID> responda nesta thread: causa raiz, plano de ação, responsável e prazo.
```

KPI 🔴 que não esteja em nenhuma seção do bloco de mapeamento: marque `<@U03A4SS2P1Q>` e
inclua no topo da mensagem a linha `*KPI sem responsável mapeado: {nome do KPI}*`.

Não escreva "possíveis impactos". Não inclua link de Metabase.

#### Formato próprio dos KPIs "alerta de trabalho"

Para os KPIs listados como **alerta de trabalho** em `00-identificadores.md`, a mensagem 🔴 é
outra: é fila, não análise. **Sem hipótese, sem "ação sugerida", sem link de Decision Log.**

Execute o card do KPI e separe o resultado em dois horizontes pela coluna `status_urgencia`:
o que **ainda dá pra salvar** (`Vence em ate 3 dias`) e o que **já perdeu o prazo mas segue em
aberto** (`Vencido (nao acionavel)` — escreva "vencido, ainda em aberto", nunca "não acionável").

**Parte 1 — mensagem solta no canal.** Exatamente estes elementos, nesta ordem:

```
🔴 _{KPI}_ — fila de trabalho do dia
Vencendo em até 3 dias: {N} recursos · R$ {valor}
Já vencidos, ainda em aberto: {M} recursos · R$ {valor}
Concentração dos vencidos: {grupo econômico} {n} recursos (R$ {valor}) · {grupo} {n} (R$ {valor})
↩️ <@ID> lista completa na thread. Priorize hoje o que ainda dá pra salvar.
```

A linha de **Concentração** é obrigatória e traz os grupos econômicos em ordem decrescente de
valor vencido, até cobrir 90% do valor. Ela é o que transforma uma pilha de recursos numa
conversa acionável — hoje, por exemplo, um único grupo responde por quase todo o valor vencido.

**Parte 2 — respostas na thread.** Duas listas, nesta ordem, cada uma numa resposta:

1. **Vencendo em até 3 dias** — lista **completa**, ordenada por `dias_restantes_vencimento`
   crescente (o mais urgente primeiro):
   `{dias} d · PEG {peg_code} · {institution_name} · R$ {appeal_value}`
2. **Vencidos, ainda em aberto** — **consolidado por grupo econômico**, ordenado por valor
   decrescente, mais os 10 maiores recursos individuais por valor:
   `{provider_economic_group}: {n} recursos · R$ {valor} · protocolados entre {data} e {data}`

Por que a segunda lista é consolidada e não item a item: o estoque vencido costuma ter dezenas
de recursos e a leitura útil é por prestador, não por PEG. **A lista completa item a item vai
para a página do Notion**, que é canônica e não tem limite de densidade.

Se um dos dois horizontes estiver vazio, escreva a linha mesmo assim com `0 recursos` — a
ausência é informação, e sumir com a linha quebra a leitura da série.

### Mensagem 3 — não existe nesta operação

Reservado. Contas Médicas não tem bloco de "outros indicadores" no Slack.

### Mensagem 4 — sinalizações de risco e bugs (sempre) — NOVA

String literal:

```
🚨 *Sinalizações de risco, bugs e alertas*
O que não aparece nos KPIs e o time precisa saber hoje. Responda nesta thread, um item por resposta:

• *Casos em andamento* — conta, prestador ou glosa que você está tratando e que vem sendo discutida fora deste canal (DM, outro canal, conversa com outra área): qual caso, onde está a conversa, o que falta.
• *Bugs abertos com tech* — bug já aberto com tech ou dados (n8n, TOTVS, PLS, motor de pertinência, Metabase): do que trata, impacto na operação, status e desde quando.
• *Problemas na operação* — pessoas off, absenteísmo, erro de execução, fluxo desalinhado, gargalo novo, fila acumulada: o que é, desde quando, quem está impactado.

↩️ Em cada item, diga se precisa de decisão, de ação (com dono) ou se é só monitorar.
Sem resposta = nada a sinalizar.
```

O que vier aqui é distribuído nas três sub-seções do **Bloco 4** da página e recebe a coluna
`Leitura` (`→ Decisão` / `→ Ação` / `→ Escalar` / `→ Monitorar` / `→ Sem dono`).

**Guarde o `ts` desta mensagem.**

### Mensagem 5 — KPIs sem instrumentação (condicional)

Antes de postar, verifique no catálogo os KPIs de Contas Médicas com `Status instrumentação`
diferente de `Produção`. Se não houver nenhum, **não poste**. Se houver, poste como resposta na
thread da Mensagem 1:

```
⚙️ *KPIs sem instrumentação em produção*
Os indicadores abaixo estão no catálogo mas ainda não entregam número confiável:

• {Nome do KPI} — {Status instrumentação}

Ajuste o status ou a fonte no catálogo e eles entram automaticamente no próximo report.
```

### Mensagem 6 — pendências (mensagem ÚNICA do dia, sempre que houver) — NOVA

É **a** mensagem de pendências do dia: headline no canal, detalhamento **na thread**, marcando
cada responsável e **cobrando** o que falta. Os syncs re-cobram **nesta mesma thread**, citando
os mesmos números — nunca criam mensagem nova.

Levante o que está **em aberto** (não é só o vencido):

- **Decision Log:** entradas de Contas Médicas com `Status de execução` = `Em curso`, **ou**
  incompletas (campos obrigatórios faltando), **ou** com `Estado de complemento` =
  `Rascunho Claude` há mais de 1 dia útil (proposta que ninguém respondeu).
- **Action Log (Log Melhoria Contínua):** ações de Contas Médicas com `Status` ∈
  {`A iniciar`, `Em andamento`, `Atrasada`}, ou incompletas.
- **Deep dives pendentes:** os `[Deep dive]` em aberto no Bloco 5 da página (`Fonte` =
  `Deep dive`), carregados dos dias anteriores até serem feitos.
- **Sinalizações de dias anteriores:** o que foi sinalizado no Bloco 4 em dias passados, tem
  `Leitura` = `→ Decisão`, `→ Ação` ou `→ Escalar` e segue aberto (`Fonte` = `Bloco 4`). Entra
  aqui **uma vez** — a partir da migração é pendência e não volta a ser sinalização.
- **KPI sem responsável mapeado:** KPI que desviou e não está no bloco de mapeamento. Dona: a
  OM. Cobrar: acrescentar o KPI → pessoa no bloco.
- **Fila de trabalho em aberto:** KPI do tipo **alerta de trabalho** que ficou 🔴. Rótulo
  `[Fila]`, responsável do bloco de mapeamento, contexto = `{N} vencendo em ≤3 dias · {M}
  vencidos ainda em aberto`. **Rola todo dia até zerar**, e o contexto é reescrito com os
  números do dia — nunca se abre uma segunda linha para o mesmo KPI.

O que conta como pendência:
- **Não iniciada** (`A iniciar`) ou **sem preenchimento completo** → falta info/preenchimento.
- **Em andamento**, mesmo dentro do prazo → cobrar update.
- **Vencida** (prazo < hoje) → cobrar conclusão ou novo prazo.
- **Risco/bug sinalizado sem tratativa** → cobrar dono e encaminhamento.
- **RFC pendente** (decisão que exigiu mudança de processo, mas o RFC no Catálogo de Processos
  Humanos ainda não foi aberto) → cobrar andamento.
- **Deep dive pendente do dia anterior** — 🔴 de um dia anterior que ainda **não teve deep
  dive** (sem causa raiz / plano de ação / decisão). **Não é ação nem decisão** — é a etapa
  anterior: falta o diagnóstico. Rótulo `[Deep dive]`, marca o responsável do KPI, e **rola
  todo dia** até ser feito.

Se não houver nenhuma, **não poste**.

**Parte 1 — mensagem top-level (headline + contagem, SEM emojis):**

```
*Pendências em aberto ({N})* — {D} decisões · {A} ações · {V} vencidas
Detalhe e cobrança na thread.
```

**Parte 2 — resposta na thread, UMA por item, ENUMERADA.** A numeração é a referência para a
pessoa responder ("Pendência 1 - escalado, ..."). Formato, sem emojis:

```
Pendência {N} - <@responsável> — [{Decisão|Ação|Deep dive|Fila}] {título} → {link}
{estado} · {status} · {contexto / o que falta}
```

Estado por tipo:
- **Não iniciada / incompleta** → `Não iniciada` ou `Incompleta: falta {campos}` · cobrar
  preenchimento e prazo.
- **Em andamento (no prazo)** → `Em andamento · prazo {DD/MM}` · cobrar update/bloqueio.
- **Vencida** → `Vencida (venceu {DD/MM})` · cobrar conclusão ou novo prazo.

Regras:
- **Numeração contínua e estável** (Pendência 1, 2, 3…) — o time responde citando o número.
- **Marque o responsável DEFINIDO** de cada item. **NÃO marque a OM por padrão.** A OM
  (`<@U03A4SS2P1Q>`) só entra quando o item está sem responsável (`A DEFINIR`), é da alçada
  dela, ou é escalonamento de item grave.
- **Sem emojis** — texto puro. Item grave → escreva `GRAVE` no início da linha.
- Todos os itens, sem truncar. Menção só por ID. Links só os permitidos.
- **Guarde o `ts` desta mensagem** e registre-o no corpo da Execução de Rotina (linha
  `ts pendências: <ts>`), para os syncs re-cobrarem na mesma thread.

---

## Tratamento de status

- Todos os KPIs puxaram → `Status da execução` = `Publicada`.
- Algum KPI não puxou → `Parcial`, e a página lista os KPIs sem dado com o motivo específico.
- Nenhum KPI puxou → `Falhou`; ainda assim **crie a Execução de Rotina registrando a falha**,
  **não poste vermelhos no Slack**, poste no canal apenas
  `⚠️ _Daily Contas Médicas — DD/MM/AAAA_ — falha ao obter os KPIs. {motivo}. Report não
  publicado.` marcando `<@U03A4SS2P1Q>`, e encerre.

## Ao terminar

Responda apenas um resumo de uma linha: farol do dia, nº de vermelhos, e os `ts` da Mensagem 1
e da Mensagem 6.
