---
name: daily-contas-medicas-sync-pre-daily
description: Contas Médicas · 10h00 — Varredura pré-daily: captura o que o time respondeu nas threads do Slack e leva para a página da daily no Notion, antes da reunião das 10h30. Tarefa silenciosa: não publica no Slack e não cria Decision Log nem Action Log.
---

Sincroniza a daily de Contas Médicas no modo **pré-daily**: antes da reunião, captura o que o
time respondeu nas threads e leva para a **página** da daily no Notion, para a daily síncrona
começar com a página já em pé.

É uma tarefa **silenciosa**: **não posta nada no Slack** e **não cria registro formal** —
Decision Log e Action Log ficam para os syncs das 15h e 19h, depois da daily, quando a decisão é
real. Aqui é só captura.

Roda às 10h00 porque a daily síncrona de Contas Médicas começa ~10h30. Se o horário da reunião
mudar, mova esta tarefa, não o conteúdo.

Leia antes de começar: `shared/00-identificadores.md`, `shared/01-regras-de-registro.md`.

Inputs fixos — não pergunte:
- **Operação:** Contas Médicas — https://app.notion.com/p/37cf0f13146a8023b8ebe67185557704
- **Execuções de Rotina:** `collection://00d00405-31e2-4670-abd1-168e986e55e9`
- **Decision Log** (só leitura, para contexto): `collection://b619a21c-a5f8-4701-a477-f5d150f03066`
- **Action Log** (só leitura, para contexto): `collection://39ff0f13-146a-8001-b289-000b5fb3961c`
- **Canal Slack:** `C0BH03QKUKY`
- **Executor:** buscar via `notion-search` pelo email juliana.borges@alice.com.br

**Alinhamento:** a estrutura da página é a de `02-notion-page/SKILL.md`; o report de origem, a
de `01-report-slack/SKILL.md`.

---

## O que fazer

### 1. Localizar a página da daily de hoje

Execuções de Rotina, `Título da execução` = `Daily - Contas Médicas - DD/MM/AAAA`.
**Se não existir, pare e registre no log** — a página é criada pelas tarefas 01/02. Não crie a
página aqui.

Se a página existir mas ainda estiver no formato enxuto (a tarefa das 09h15 não rodou), capture
o que der nos campos que existem e registre no marcador que a página não estava canônica. Não
tente montar os 5 blocos aqui.

### 2. Ler as threads do report no Slack (só leitura)

Mensagens de hoje: cada vermelho 🔴, a Mensagem 4 (sinalizações) e a Mensagem 6 (pendências),
se existirem.

### 3. Idempotência — rastreio pela página, não pelo Slack

Capture só **resposta humana nova** ainda não refletida na página. Se a informação já está no
bloco correspondente, pule. Não reprocesse.

### 4. Atualizar o Bloco 2 (deep dives) — cada info no sub-bloco do seu desvio

- **`Causa raiz` por entidade:** preencher a coluna `Causa raiz` das linhas ⏳ com a causa que o
  responsável respondeu na thread, **casando pela entidade** (nome do prestador, grupo
  econômico, motivo de glosa, nº da fatura). Manter ⏳ nas linhas que ainda não tiveram resposta.
  Se a resposta for genérica ("é o de sempre nos hospitais"), não distribua por linha: escreva
  no campo `💬 Resposta do responsável` e mantenha as linhas em ⏳.
- **`💬 Resposta do responsável`** (nível do desvio): preencher
  `Isolado ou padrão · Plano de ação · Owner · Prazo` com o respondido; manter ⏳ no que faltar.
  Owner vazio → escrever exatamente `A DEFINIR`.
- Não criar seção separada — tudo vive no sub-bloco do desvio.

### 5. Atualizar o Bloco 3 (Sinalizações)

Substituir o ⏳ pelo conteúdo das respostas da thread da Mensagem 4; manter ⏳ se ainda não veio.
Encaixar cada resposta na sub-seção certa (4.1 casos · 4.2 bugs com tech/dados · 4.3 problemas
na operação) e **sempre preencher a coluna `Leitura`** (`→ Decisão` / `→ Ação` / `→ Escalar` /
`→ Monitorar` / `→ Sem dono`). Se a pessoa não disse o que precisa, inferir pela descrição e
marcar; se não der, `→ Sem dono`.

**Antes de criar item no Bloco 3, checar o Bloco 4.** Se a resposta é sobre assunto que **já é
pendência** (mesmo prestador, mesmo bug, mesmo problema), não crie sinalização nova: atualize o
`Status` daquela linha do Bloco 4. O Bloco 3 só recebe o que é **novo hoje**.

### 6. Atualizar o Bloco 4 (Pendências)

Se alguém respondeu numa thread de pendência, **anotar a resposta na coluna `Status`** da tabela
da página (ex: `✅ concluído`, `🔄 novo prazo DD/MM`, `❌ bloqueado: {motivo}`,
`em andamento — aguardando tech`). **Não** alterar o Decision Log nem o Action Log agora — o
registro formal é dos syncs das 15h/19h.

**Conclusão dita em texto livre conta** (§6 de `01-regras-de-registro.md`): se a pessoa escreveu
que apurou, resolveu ou encerrou o item — mesmo sem responder a nenhuma proposta —, marque
`✅ concluído — {nome}, DD/MM` no `Status`. Isso não fecha nada nos logs, mas é o sinal que o
fechamento das 19h vai ler para fechar de verdade. Texto ambíguo ("vamos acompanhar") não é
conclusão: mantenha o status como está.

### 7. Conflito entre respostas

Sinalizar no sub-bloco do desvio uma linha `⚠️ respostas divergentes: {quem} diz {X}, {quem} diz
{Y}`. Não tentar resolver, não escolher lado.

### 8. Marca de rastreabilidade

Ao terminar, deixar/atualizar na página o marcador **Varredura da manhã · `[dl-sync]`** com a
data/hora da varredura — é o ponto de corte que os syncs seguintes usam para saber o que já foi
capturado.

---

**Esta tarefa NÃO:** posta no Slack · cria ou edita Decision Log / Action Log · recalcula
Metabase · monta blocos que a tarefa 02 deveria ter montado.

## Ao terminar

Responda apenas um resumo de uma linha: quantas threads lidas, quantas respostas humanas novas
capturadas, quantos conflitos sinalizados.
