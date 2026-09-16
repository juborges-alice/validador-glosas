---
name: daily-contas-medicas-sync-fechamento
description: Contas Médicas · 19h00 — Fechamento do dia (EOD): lê as validações nas threads e SÓ ENTÃO registra no Decision Log / Action Log, abre pendências de Deep dive, sinaliza pendências D+1 na thread única e consolida o rodapé de fechamento na página.
---

Sincroniza a daily de Contas Médicas no modo **fechamento (EOD)**: varredura final, **registro**
no Decision Log / Action Log **apenas do que foi validado** (pela pessoa responsável ou pela OM),
sinalização de pendências para D+1, e consolidação do rodapé de fechamento na página.

Leia antes de começar: `shared/00-identificadores.md`, `shared/01-regras-de-registro.md`.

Inputs fixos — não pergunte:
- **Operação:** Contas Médicas — https://app.notion.com/p/37cf0f13146a8023b8ebe67185557704
- **Execuções de Rotina:** `collection://00d00405-31e2-4670-abd1-168e986e55e9`
- **Decision Log:** `collection://b619a21c-a5f8-4701-a477-f5d150f03066`
- **Action Log (Log Melhoria Contínua):** `collection://39ff0f13-146a-8001-b289-000b5fb3961c`
- **Canal Slack:** `C0BH03QKUKY`
- **Transcrição da daily:** buscar no Drive por título (ver `00-identificadores.md`)
- **Executor:** buscar via `notion-search` pelo email juliana.borges@alice.com.br

---

## 1. Varredura final das threads

Capturar as últimas respostas humanas novas desde o marcador **Resumo da daily ·
`[meet-sync DD/MM]`** (ou a última varredura). Atualizar a página igual aos syncs anteriores:
`Causa raiz` das linhas ⏳, `💬 Resposta do responsável`, Blocos 4 e 5. Se a transcrição ainda não
tiver sido processada (sem `[meet-sync DD/MM]` no Bloco 6), buscá-la no Drive e distribuir nos
blocos como a tarefa 04.

## 2. Registro — SÓ o que foi validado

As propostas (estruturadas, marcadas como **Decisão** ou **Ação**, com **o quê · quem · quando**)
foram postadas nas threads pela tarefa 04, marcando o responsável e a OM. A validação pode vir de
**qualquer um dos dois**. Para **cada proposta**, leia a thread e aja:

| Validação (responsável OU OM) | O que fazer |
|---|---|
| **OK / confirmado** | Registrar como proposto. |
| **Correção** (ajustou o quê / quem / quando / tipo / classe) | Registrar **com as correções aplicadas**. |
| **Recusado** | **Não** registrar; anotar na página o descarte e o motivo. Se houver entrada no Decision Log, marcar `Veredito sobre a proposta` = `Recusada`, `Tipo` = `Não-ação registrada`, `Decisão tomada` = o motivo, `Status de execução` = `Cancelada`. |
| **Sem confirmação** até o fechamento | **Não** registrar; vira **pendência D+1** (passo 4). |

**Registrar exige campos completos.** Se veio validação mas falta campo obrigatório (ação sem
prazo ou sem responsável), **não registre** — sinalize o que falta como pendência D+1.

Ao registrar:
- **Decisão** → **Decision Log**, campos de `01-regras-de-registro.md` §3.
  Quando a validação vem de um humano na thread, aplique também o mapeamento:
  - aceitou → `Veredito sobre a proposta` = `Aceita`, `Estado de complemento` = `Aprovada`,
    `Decisão tomada` = o texto da `Proposta original do agente`, `Status` = `Vigente`,
    `Status de execução` = `Em curso`;
  - alterou → `Veredito` = `Complementada`, `Estado de complemento` = `Complementada por OM`,
    `Decisão tomada` = o texto alterado, `Status` = `Vigente`, `Status de execução` = `Em curso`;
  - recusou → `Veredito` = `Recusada`, `Tipo` = `Não-ação registrada`, `Decisão tomada` = o
    motivo, `Status de execução` = `Cancelada`.

  Em todos os casos, anote no fim de `Decisão tomada`:
  `— revisado por {nome} via Slack em DD/MM`. `Owner da ação` (person) = quem revisou, a menos
  que a resposta nomeie outro owner. **Não sobrescreva `Autor`.** Se a resposta trouxer prazo,
  preencha `date:Prazo:start`. Faça `notion-fetch` na entrada antes de atualizar, para ler
  `Proposta original do agente` e `Autor` atuais.
- **Ação** → **Action Log (Log Melhoria Contínua)**, campos obrigatórios de
  `01-regras-de-registro.md` §3. Atenção: `Status` = `A iniciar` (os valores válidos são
  `A iniciar` / `Em andamento` / `Atrasada` / `Concluída` / `Cancelada`).
- **Dedup 14d:** se já há decisão aberta do mesmo KPI nos últimos 14 dias, **anexe** a ocorrência
  em vez de criar nova.
- **Vermelho persistente:** KPI 🔴 por 5 dias seguidos → encerre as diárias e abra **uma** decisão
  estrutural (`Mudança de processo` ou `Escalonamento`) + a ação correspondente — **também**
  sujeita ao OK; se ninguém validou, vai como pendência D+1.
- Ligue cada decisão criada no campo `Decisões geradas` da Execução de Rotina, e cada ação à sua
  decisão via `Decisão de origem`. Preencha o **link do registro** nos blocos da página (Bloco 2
  `💬`, Bloco 4, Bloco 5, Bloco 6).
- Marque cada proposta processada com `[dl-sync]` na thread para não reprocessar:
```
[dl-sync] ✓ Registrado — {Decisão|Ação}, {veredito}: {resumo em 1 linha}
{URL da entrada}
```
- **Conflito não resolvido → não registre e não confirme.** Deixe sem marcador, para reprocessar
  quando houver consenso, e liste o conflito no rodapé de fechamento.

## 2b. Desvio 🔴 não analisado → pendência de Deep dive (não é ação nem decisão)

Verifique cada 🔴 do dia. Se ao fim do dia — **mesmo após as cobranças** — algum ficou **sem deep
dive** (sem causa raiz, sem plano de ação, sem decisão), registre-o como **pendência de Deep
dive** — é a etapa de **diagnóstico**, anterior a decisão/ação:

- **Não** crie entrada no Decision Log nem no Action Log — não é ação nem decisão.
- Registre na tabela do **Bloco 5** uma linha com `Fonte` = `Deep dive`, `Pendência` =
  `Deep dive: {KPI} (desvio de DD/MM)`, `Responsável` = a pessoa do bloco de mapeamento,
  `Status` = `Pendente`.
- **Rola todo dia:** o report e os syncs re-incluem os Deep dives pendentes até serem feitos. Na
  thread de pendências aparece com o rótulo `[Deep dive]`, marcando o responsável.
- **Some** quando o deep dive for feito (causa raiz + plano de ação ou decisão registrados).
- **Dedup:** desvio que já tem Deep dive pendente aberto (mesmo KPI + data) não gera outro.

## 3. Atualizar a tabela do Bloco 5 (Pendências)

Deixar a tabela (`Pendência | Fonte | Responsável | Venceu | Status`) com o estado final do dia:
itens registrados com seu link e fonte, itens fechados como ✅, e os que viram D+1.

**Migração do Bloco 4 → Bloco 5 (é aqui que acontece).** Sinalizações de hoje com `Leitura` =
`→ Decisão`, `→ Ação` ou `→ Escalar` que seguem abertas viram linha de pendência: `Fonte` =
`Bloco 4`, `Venceu` = data em que foram sinalizadas, `Responsável` = quem ficou (ou `A DEFINIR`).
A partir de agora o item é **pendência** e não volta a aparecer no Bloco 4 nos próximos dias.
`→ Monitorar` não migra. Sinalização que já virou registro entra com a `Fonte` do registro, não
como `Bloco 4`.

**Dedup:** antes de criar qualquer linha, conferir se o assunto já tem pendência aberta. Se tiver,
atualizar o `Status` da linha existente — nunca uma segunda linha.

**Atualizar também o resumão de pendências no topo do Bloco 1** (contagem de decisões/ações em
aberto e vencidas).

## 4. Fechamento de pendências no Slack — na thread ÚNICA (D+1)

**Não crie mensagem nova de pendência.** Poste o fechamento **na thread da Mensagem 6** (mesmo
`ts` do dia), prefixo `[eod-sync DD/MM]`, com o estado final e o que rola para amanhã. Uma
cobrança por item, marcando o responsável.

Entram como D+1: itens **sem validação** (proposta sem OK), **sem resolução** (thread sem resposta
ou conflito) e os do **backlog** (Decision Log / Action Log) que seguem em aberto. **Não** criar
registro formal do que não foi validado.

Formato (reply na thread da Msg 6, **citando os números**, **sem emojis**):

```
[eod-sync DD/MM] — fechamento do dia · Pendências para amanhã ({N})
Pendência {N} - <@responsável> — [{Decisão|Ação|Deep dive}] {título} → {link} · {o que falta}
```

Quando não houver: `[eod-sync DD/MM] Sem pendências para amanhã.` na thread.

- **Marque o responsável DEFINIDO.** A OM só quando `A DEFINIR` / alçada / escalonamento.
- **Sem emojis.** Sem itálico. Não truncar. Links só os permitidos.
- Se a thread de pendências não existir hoje e houver itens D+1, abra a mensagem top-level no
  formato da Mensagem 6 da tarefa 01.

## 5. Rodapé de Fechamento na página

Preencher o callout **Fechamento do dia · `[eod-sync DD/MM]`** que a tarefa 02 reservou no rodapé
(substituir o ⏳):

- Threads processadas no dia: N
- Decisões registradas (Decision Log): N · Ações registradas (Action Log): N
- Propostas recusadas: N · Sem validação (→ D+1): N
- Conflitos não resolvidos (não registrados): lista, ou "nenhum"
- Deep dives pendentes abertos hoje: lista, ou "nenhum"
- Transcrição da daily: processada / não encontrada
- Pendências para D+1: lista, ou "nenhuma"

Se a `Status da execução` da Execução de Rotina ainda estiver `Pendente`, feche-a como
`Publicada` / `Parcial` conforme o report do dia.

---

**Esta tarefa:** registra **só** o que foi validado por humano; publica **só** a mensagem de
pendências D+1 (pendência-primeiro).

## Ao terminar

Responda apenas um resumo de uma linha: decisões registradas, ações registradas, recusadas,
conflitos, e pendências D+1.
