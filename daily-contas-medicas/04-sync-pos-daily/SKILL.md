---
name: daily-contas-medicas-sync-pos-daily
description: Contas Médicas · 15h00 — Pós-daily: processa a transcrição da daily, PROPÕE as decisões/ações estruturadas nas threads (marcando o responsável ou a OM para o OK) e re-cobra as pendências na thread única (prazo 17h). É o único sync que publica no canal; o registro no Decision/Action Log é feito no fechamento (19h), só com o que for validado.
---

Sincroniza a daily de Contas Médicas no modo **pós-daily**: depois da reunião, processa a
transcrição, **propõe** as decisões/ações nas threads relacionadas e **re-cobra no Slack** os
itens em aberto (prazo 17h). É o **único sync que publica no canal**.

**Regra dura: nada entra no Decision Log ou no Action Log sem validação.** Quem valida: a
**pessoa responsável** pelo deep dive (quem propôs o plano) **ou** a OM — o OK de qualquer um dos
dois vale. O registro efetivo é feito no fechamento (`05-sync-fechamento`), com o que foi
validado (OK ou corrigido). Aqui só se **propõe**.

Leia antes de começar: `shared/00-identificadores.md`, `shared/01-regras-de-registro.md`,
`shared/02-metabase.md`.

Inputs fixos — não pergunte:
- **Operação:** Contas Médicas — https://app.notion.com/p/37cf0f13146a8023b8ebe67185557704
- **Execuções de Rotina:** `collection://00d00405-31e2-4670-abd1-168e986e55e9`
- **Decision Log:** `collection://b619a21c-a5f8-4701-a477-f5d150f03066`
- **Action Log (Log Melhoria Contínua):** `collection://39ff0f13-146a-8001-b289-000b5fb3961c`
- **Canal Slack:** `C0BH03QKUKY`
- **Transcrição da daily:** buscar no Google Drive por título (ver
  `00-identificadores.md` → Gravação da daily síncrona)
- **Executor:** buscar via `notion-search` pelo email juliana.borges@alice.com.br

---

## 1. Varredura das threads desde a Varredura da manhã

Reler as threads do report no Slack e capturar as **respostas humanas novas** desde o marcador
**Varredura da manhã · `[dl-sync]`** que a tarefa 03 deixou na página. Atualizar a página igual à
tarefa 03: `Causa raiz` das linhas ⏳ (casando por prestador / motivo / fatura),
`💬 Resposta do responsável`, Blocos 4 e 5.

**Repuxe de ETL (fallback).** O repuxe é feito pela tarefa 02 às 09h15. Só se algum deep dive
**ainda** estiver com a lista pendente nesta hora, re-execute o card de drill por ID e poste a
lista na thread. Nunca escreva SQL.

## 2. Processar a transcrição da daily

Busque no Drive por título:
`title contains 'Daily Contas Médicas' and title contains '{AAAA/MM/DD de hoje}'`.
Padrão do nome: `Daily Contas Médicas - AAAA/MM/DD HH:MM GMT-03:00 - Anotações do Gemini` (ou
`- Notes by Gemini`). Se houver mais de um, use o mais recente. Se não encontrar: registre a nota
no Bloco 5 (`transcrição não encontrada no Drive`) e continue — não trave.

Separe o conteúdo por **bloco de destino**:
- Sobre um desvio que tem sub-bloco no Bloco 2 → campo `🗣️ Da daily síncrona` daquele desvio.
- Sobre risco, bug, caso em andamento ou problema da operação → Bloco 3, na sub-seção certa
  (4.1 / 4.2 / 4.3), sempre com a coluna `Leitura` — **só se for novo hoje**. Se a daily falou de
  algo que já é pendência, atualize a linha do Bloco 4, sem criar item no Bloco 3 nem pendência
  duplicada.
- Decisões/ações gerais, não ligadas a um desvio → Bloco 5.
- Em aberto, sem definição → sinalizar no item; **não** vira registro ainda.

## 3. Distribuir a ata nos blocos (não criar seção separada)

- **Bloco 2:** preencher `🗣️ Da daily síncrona` de cada desvio discutido (substituir o ⏳).
- **Blocos 4/5:** inserir o que a daily falou. A daily costuma ser a hora em que a `Leitura` de
  um item muda (de `→ Monitorar` para `→ Ação`, de `→ Sem dono` para dono definido) — atualize a
  coluna.
- **Bloco 5 · Resumo da daily (último bloco):** resumo **breve** que referencia os outros blocos
  e registra o que **não encaixa** em nenhum outro (decisões gerais, mudanças de fluxo), cada
  item com responsável · prazo. O link do registro entra no fechamento. No topo: participantes +
  link da transcrição.
- **Idempotência:** marcar o Bloco 5 com **Resumo da daily · `[meet-sync DD/MM]`**. Se já
  existir e não houver conteúdo humano novo, não reprocessar.

## 4. Estruturar e PROPOR o registro nas threads — não registrar ainda

A partir do que o responsável respondeu na thread (causa raiz, plano de ação, quem, prazo) e do
que a daily decidiu, monte o item **já estruturado com todos os campos** e poste na thread
relacionada (o vermelho do desvio, ou o tema) para **confirmação**. **Não** escreva no Decision
Log nem no Action Log agora.

**Antes de propor, checar se o assunto já é pendência** (Bloco 4, incluindo as vindas do Bloco
4). Se já for, **não** proponha item novo: poste a **atualização** na thread da pendência e
atualize o `Status` da linha. Proposta nova só existe para assunto que ainda não tem pendência
aberta.

**Quem valida:** a **pessoa responsável** pelo deep dive **ou** a OM (`<@U03A4SS2P1Q>`) — o OK de
qualquer um vale. Marque no post, sem ambiguidade, se é **Decisão** ou **Ação**, e inclua
**o quê · quem · quando** + os demais campos obrigatórios:

- **Ação (Action Log — Log Melhoria Contínua):**
```
*Ação — confirmar registro* (<@ID responsável> ou <@U03A4SS2P1Q>)
• O quê: {ação no infinitivo}
• Quem (responsável): <@ID>
• Quando (prazo): {DD/MM}
• Tipo de Ação: {Gestão de Caso / Gestão de Resultado / Gestão de Projeto}
• Time responsável: {Auditoria / Omissão / HCDev / Jurídico / Agudo Hospitalar, ou — se for da própria operação}
• Prioridade: {Sim se risco regulatório, assistencial ou pagamento travado a prestador; senão Não}
Confirmem ou corrijam nesta thread.
```

- **Decisão (Decision Log):**
```
*Decisão — confirmar registro* (<@ID responsável> ou <@U03A4SS2P1Q>)
• O quê (conclusão): {texto}
• Classe: {Investigação / Ajuste de limiar / Mudança de processo / Escalonamento / Não-ação}
• Owner / Prazo: {se definidos; senão A DEFINIR — alçada da OM}
Confirmem ou corrijam nesta thread.
```

- Uma proposta por decisão/ação, na thread do desvio/tema. Campo sem valor = `A DEFINIR`.
- **Episódio aberto → referencie, não proponha nova** (§3 de `01-regras-de-registro.md`). Antes de
  propor qualquer decisão, procure no Decision Log o **episódio aberto** daquele KPI
  (`Operação` = Contas Médicas, `Status de execução` = `Em curso`, KPI na relation `KPIs afetados`).
  - **Achou e a causa é a mesma** → **referencie o episódio** na proposta, com o link. O que a daily
    trouxer de novo vira uma **linha de histórico** naquele episódio no fechamento das 19h, não
    uma decisão nova. Este é o caso normal dos crônicos de Contas Médicas.
  - **Achou mas a causa mudou** → proponha decisão nova e **diga na proposta que o episódio
    anterior será encerrado**, citando o link e a causa que caiu.
  - **Não achou** → proposta normal, é um episódio novo.

  O que decide não é a idade do registro, é a **causa**. Um episódio velho com a mesma causa segue
  sendo o mesmo episódio; um episódio de ontem com causa nova já é outro. O teto de 14 dias
  corridos existe e força uma continuação, mas quem aplica é o fechamento das 19h — aqui você só
  referencia o que está aberto.
- **Só 🔴 gera proposta.** 🟡 não gera nada — nem proposta, nem Decision Log. Vale também para o 🟡 rebaixado por decisão vigente: a decisão que o rebaixou já existe e não é reaberta.
- **KPI do tipo "alerta de trabalho"** (`00-identificadores.md`) **não gera proposta de decisão**,
  mesmo 🔴. Se a thread trouxer tratativa por recurso, leve para a coluna `Tratativa` da página,
  casando por `PEG`. Se a daily decidir algo estrutural sobre a fila — renegociar prazo com um
  prestador, mudar a priorização — aí sim é decisão, e vale a proposta normal.
- **Nunca proponha ação que contradiga decisão vigente.** Se o KPI está 🔴 por trade-off já
  decidido, a proposta correta é a **pergunta de horizonte** à OM:
```
*Decisão — confirmar registro* (<@U03A4SS2P1Q>)
• O quê (conclusão): {KPI} segue fora do limiar pelo trade-off decidido em {DD/MM}. Definir até quando o trade-off vale e qual patamar é aceitável no período — ou calibrar o limiar do KPI para parar de gerar vermelho previsível.
• Classe: Ajuste de limiar
• Owner / Prazo: A DEFINIR — alçada da OM
Confirmem ou corrijam nesta thread.
```

O **registro efetivo** (só o validado, já ajustado) é feito no fechamento.

## 5. Re-cobrança de pendências no Slack — na thread ÚNICA (17h)

**Não crie mensagem nova de pendência.** Re-cobre **na thread da Mensagem 6 de pendências** (o
`ts` guardado no Bloco 4 da página), prefixo `[sync 15h DD/MM]`, cobrando o que ainda precisa
fechar até 17h, marcando o responsável.

Cubra, na **mesma thread**, uma cobrança por item:
- itens da daily de hoje ainda sem definição (proposta sem OK, plano de ação ⏳, conflito não
  resolvido);
- itens do backlog (Decision Log / Action Log) que seguem em aberto.

Formato (reply na thread da Msg 6, **citando os números**, **sem emojis**):

```
[sync 15h DD/MM] — cobrança 17h
Pendência {N} - <@responsável> — {o que falta} · fechar até 17h?
```

Se não houver nada em aberto: `[sync 15h DD/MM] Sem pendências para as 17h.` na thread.

- **Marque o responsável DEFINIDO.** A OM só quando `A DEFINIR` / alçada dela / escalonamento —
  **não** por padrão.
- **Sem emojis.** Sem itálico. Não truncar. Links só os permitidos.
- Se a thread de pendências **não existir** hoje (não houve Msg 6 de manhã porque não havia
  pendência, ou porque o report ainda é a versão local sem Msg 6) e agora surgiram itens, aí sim
  **abra** a mensagem de pendências top-level no formato da Mensagem 6 da tarefa 01, guarde o
  `ts` e registre-o no Bloco 4.

## Ao terminar

Responda apenas um resumo de uma linha: transcrição processada ou não, quantas propostas
postadas (decisões / ações), e quantos itens cobrados para as 17h.
