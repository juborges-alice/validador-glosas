# Daily Ops — Contas Médicas (na nuvem)

Rotina de daily da Operação Contas Médicas, dividida em 5 tarefas que rodam **só em dias
úteis**, cada uma como uma **Routine do Claude Code na nuvem** (não launchd, não Mac local).

Adaptada do desenho da Operação Autorização (`rotinadailyopsprompts`, ago/2026).

---

## 1. As 5 tarefas

| Hora (BRT) | Cron (UTC) | Tarefa | O que faz | Publica no Slack? |
|---|---|---|---|---|
| 06h30 | `30 9 * * 1-5` | `01-report-slack` | Lê os KPIs, aplica o farol, posta o report e os vermelhos, cria a Execução de Rotina enxuta e as entradas de Decision Log | Sim — é o report |
| 09h30 | `30 12 * * 1-5` | `02-notion-page` | Transforma a Execução de Rotina na página canônica de 6 blocos, puxa os drills completos, repuxa o que o ETL não tinha às 06h30 | Só o link da página |
| 10h15 | `15 13 * * 1-5` | `03-sync-pre-daily` | Pré-daily: captura o que o time respondeu nas threads e leva pra página | Não (silenciosa) |
| 15h00 | `0 18 * * 1-5` | `04-sync-pos-daily` | Pós-daily: processa a transcrição, **propõe** decisões/ações nas threads, re-cobra pendências | Sim |
| 19h00 | `0 22 * * 1-5` | `05-sync-fechamento` | Fechamento: **registra** só o que foi validado, abre Deep dives pendentes, fecha o rodapé | Só pendências D+1 |

O cron das Routines é **UTC**. BRT = UTC-3, e nenhum horário cruza a meia-noite, então o
`day-of-week` continua `1-5`.

**10h15 e não 10h55.** O doc original usa 10h55 porque a daily da Autorização é mais tarde. A
daily de Contas Médicas começa ~10h30 — rodar 10h55 seria no meio da reunião, e a tarefa é
explicitamente **pré**-daily. Se o horário da reunião mudar, mova a Routine.

## 2. As sete decisões de desenho (valem mais que o texto dos prompts)

1. **Slack e Notion são tarefas separadas.** O report precisa sair 06h30, antes do time começar;
   montar a página canônica é lento (drills completos, tabelas prestador-a-prestador). A tarefa
   das 09h30 lê o Slack como fonte e **não recalcula** os valores de farol.
2. **Nada entra no Decision Log ou no Action Log sem validação humana.** Às 15h a rotina
   *propõe* o registro já estruturado na thread; às 19h ela *registra* só o que teve OK (ou
   correção). O que não foi validado vira pendência D+1, não vira linha no log.
3. **Idempotência por marcador.** Cada sync deixa um marcador (`[dl-sync]`,
   `[meet-sync DD/MM]`, `[eod-sync DD/MM]`) que é o ponto de corte do próximo. Sem isso, rodar
   duas vezes duplica tudo.
4. **Uma thread única de pendências por dia.** Os syncs re-cobram *na mesma thread*, citando os
   mesmos números (`Pendência 1`, `2`…). Nunca criam mensagem nova.
5. **A forma é string literal; o modelo decide só o conteúdo analítico.** Sem isso o layout muda
   todo dia e o report fica ilegível como série.
6. **A fonte da verdade é o catálogo de KPIs no Notion**, lido a cada execução. Nada de meta
   hardcoded no prompt.
7. **Só card canônico do Metabase por ID; nunca SQL.** Garante que o número do report é o mesmo
   número do dashboard.

## 3. O que é específico desta operação (× Autorização)

- **Não existe árvore clínica de classificação** (Sem fator / Fila médica / Habitual). O que
  rebaixa 🔴 → 🟡 aqui é **decisão vigente explicativa do Decision Log**, e nada mais — com cinco
  guard-rails: só com link citado, a decisão tem que cobrir aquele desvio, fato novo cancela o
  rebaixamento, `SLA de Análise de conta` e `PEGs por Status no SLA` nunca rebaixam (meta 90%),
  e nunca sobe cor. Decisão metodológica é outra coisa: muda a cor pelo número, ao redefinir a
  janela ou o piso. Ver `shared/01-regras-de-registro.md` §1 e §2.
- **As condições moram dentro do texto do `Limiar de alerta`** — piso de materialidade, piso de
  idade, regra de dois estágios por dia do mês, janela de risco. O catálogo do Notion é a fonte;
  quando um limiar é recalibrado lá, a rotina passa a usar o novo na execução seguinte, sem
  mexer em arquivo nenhum.
- **Existe uma classe "alerta de trabalho"** (`shared/00-identificadores.md`): KPI que é fila,
  não termômetro. Hoje só o `Recursos de Glosa Próximos do Vencimento`. Quando fica 🔴, o Slack
  recebe a **lista para agir hoje** em vez de hipótese e plano de ação, mostrando os dois
  horizontes — o que ainda dá pra salvar e o que já venceu mas segue em aberto — e vira
  pendência `[Fila]` em vez de entrada no Decision Log.
- **Action Log = `Log Melhoria Contínua`** (Seção 8 da página da operação), filtrado por
  `Operações` = Contas Médicas. O `Status` dele é `Em andamento`, não "Em curso".
- **A gravação da daily não vive numa pasta única** — as anotações do Gemini nascem no Drive de
  quem gravou. Os syncs buscam **por título**, não por pasta.
- **Quase todo card é acumulado no mês** (`thismonth`), então MTD ≈ Resultado e o risco de
  defasagem de ETL às 06h30 é maior.
- **Cards que compartilham ID:** `Faturamento total acumulado` e `R$ Faturado Cassi` são o
  mesmo card 65831 com filtros diferentes.
- **Padrão de falha do Cassi é estagnação**, não queda: valor idêntico por dias consecutivos.
  A página tem coluna `Dias sem movimento` por isso.

## 4. Estrutura dos arquivos

```
daily-contas-medicas/
├── README.md                        ← este arquivo
├── shared/
│   ├── 00-identificadores.md        ← operação, datatables, KPIs, drills, mapeamento de responsáveis
│   ├── 01-regras-de-registro.md     ← farol, decisões vigentes, decisão × ação, dedup, idempotência
│   └── 02-metabase.md               ← como executar card, comparação histórica, Top N, ETL
├── 01-report-slack/SKILL.md
├── 02-notion-page/SKILL.md
├── 03-sync-pre-daily/SKILL.md
├── 04-sync-pos-daily/SKILL.md
└── 05-sync-fechamento/SKILL.md
```

**Quando algo muda** (time, canal, KPI novo, card novo, horário da daily): muda em `shared/`,
não dentro dos SKILL.md. Os 5 SKILL.md leem os 3 arquivos de `shared/` no começo de cada
execução.

## 5. Como a Routine acha os arquivos

Cada Routine roda numa **sessão nova** do Claude Code na nuvem, com este repo clonado. O prompt
da Routine é um bootstrap curto que faz checkout desta branch e manda executar o SKILL.md:

```
Você está numa sessão headless do Claude Code na nuvem, com o repo
juborges-alice/validador-glosas clonado. Antes de qualquer coisa:

  git fetch origin claude/daily-contas-medicas-cloud-hp0u83 && git checkout claude/daily-contas-medicas-cloud-hp0u83

(se a branch não existir mais porque já foi mergeada, use main).

Leia e execute integralmente daily-contas-medicas/<PASTA>/SKILL.md, seguindo TODOS os passos na
ordem, sem pular nenhum, incluindo os arquivos de daily-contas-medicas/shared/ que ele manda ler.
Os inputs já estão fixos nos arquivos — não peça confirmação e não pergunte nada.

Guard de dia útil: se hoje for sábado ou domingo, ou feriado nacional / estadual de SP (lista em
shared/01-regras-de-registro.md §5), responda apenas "pulado: não é dia útil" e encerre sem
fazer nada.

Ao terminar, responda apenas um resumo de uma linha do que foi feito.
```

O guard de dia útil vive **no prompt**, não no cron, porque feriado não se expressa em cron.

## 6. Connectors por tarefa

Cada Routine recebe só o que usa:

| Tarefa | Notion | Slack | Metabase | Google Drive |
|---|---|---|---|---|
| `01-report-slack` | ✅ | ✅ | ✅ | ✅ (fallback de KPI em Sheets) |
| `02-notion-page` | ✅ | ✅ | ✅ (drills + repuxe) | — |
| `03-sync-pre-daily` | ✅ | ✅ | — | — |
| `04-sync-pos-daily` | ✅ | ✅ | ✅ (fallback de repuxe) | ✅ (transcrição) |
| `05-sync-fechamento` | ✅ | ✅ | — | ✅ (transcrição) |

## 7. Cuidados — o que quebrou na prática (Autorização) e como fica na nuvem

| Problema no desenho local | Na nuvem |
|---|---|
| **A falha é silenciosa** — ninguém é avisado quando o exit code não é 0. Era o maior buraco. | **Resolvido:** as Routines são criadas com `notifications: {push: true, email: true}`. Cada execução que termina com algo relevante notifica. Ainda assim, confira `/routines` de vez em quando. |
| **Sessão OAuth expirada derruba a tarefa** antes de começar | Não se aplica: a sessão na nuvem não depende do login local. Os **connectors** (Notion/Slack/Metabase/Drive) podem expirar — se uma tarefa relatar falha de auth, reconecte em claude.ai → Settings → Connectors. |
| **Mac dormindo = tarefa perdida.** 06h45 era o horário de risco. | Não se aplica. |
| **Catch-up à mão atropela o tick automático** | Não se aplica do mesmo jeito, mas continua valendo: se você disparar o report à mão perto de 09h30, os dois se atropelam. Pause a Routine antes (`/routines`) e religue depois. |
| **Sem marcador de idempotência, sync duplica** | Continua valendo integralmente. Os marcadores são a única proteção. |
| **Blocos que se sobrepõem duplicam trabalho** | Resolvido pela fronteira Bloco 4 × Bloco 5 (`01-regras-de-registro.md` §7): sinalização no dia em que aparece, pendência a partir do dia seguinte, nunca os dois. |
| **Ordem dos blocos segue a leitura da reunião** | Mantido: Pendências (Bloco 5) vem antes do Resumo da daily (Bloco 6), porque é o bloco lido em voz alta. |

Riscos novos, próprios da nuvem:

- **Duplo report.** A rotina que roda hoje é a Routine `Daily-contas-medicas`
  (`trig_01KZn3tEJKV2mrJDjyM3gjS4`, `0 9 * * 1-5` = 06h00 BRT) — ela **já é uma Routine na nuvem**,
  não um job local. Enquanto ela estiver ativa, ela e a `01-report-slack` postam as duas no canal.
  **Pause a `Daily-contas-medicas` antes de ativar a Routine 01.** Por isso a 01 nasce pausada.
  O mesmo vale para a `contas-medicas-decisions-sync` (`trig_01V64RC98PkPbgs3Yk7BrJ4S`,
  `0 21 * * 1-5` = 18h00 BRT): o que ela faz hoje passa a ser coberto pelas tarefas 04 e 05.
- **Cron em UTC.** O horário BRT não muda sozinho. Se o Brasil voltar a ter horário de verão, os
  5 crons precisam de -1h.
- **Branch.** Se esta branch for mergeada e deletada, o bootstrap cai para `main` — garanta que
  os arquivos existam lá antes de deletar a branch.

## 8. Ordem de ativação sugerida

1. Confirmar/ajustar o **bloco de mapeamento de responsáveis** em
   `shared/00-identificadores.md` (hoje é proposta, e o que estiver `A DEFINIR` cai no colo da
   OM todo dia — de propósito).
2. Deixar as tarefas 02–05 rodarem 2 ou 3 dias em cima do report da `Daily-contas-medicas` atual.
   A 02 enriquece a mesma página que a rotina atual já cria; as 03–05 só passam a ter Msg 4 e
   Msg 6 quando a Routine 01 entrar, e degradam sem elas (a 04 e a 05 abrem a thread de
   pendências se ela não existir).
3. Pausar a `Daily-contas-medicas` e a `contas-medicas-decisions-sync`, e ativar a
   Routine `01-report-slack`.
4. Rever o `Limiar de alerta` dos crônicos (`% Faturas por Status - HS`, `SLA Recurso de Glosa`,
   `% PEGs sem NF`, `R$ Faturado Cassi`): eles disparam 🔴 quase todo dia por causa já decidida,
   e vermelho previsível é a coisa que mais rápido queima a confiança no ritual.

## 9. Estado da implantação (19/08/2026)

### Routines criadas — todas PAUSADAS

| Routine | Trigger ID | Cron (UTC) | Notificação |
|---|---|---|---|
| 06h30 — report no Slack | `trig_019inz1AF7e4SqzTzwDADbGQ` | `30 9 * * 1-5` | push + email |
| 09h30 — página canônica no Notion | `trig_013rQQuCGtj9ufwEwEToptba` | `30 12 * * 1-5` | push + email |
| 10h15 — sync pré-daily | `trig_01Brwu1tgrin8o8TBJRtXP1b` | `15 13 * * 1-5` | silenciosa |
| 15h00 — sync pós-daily | `trig_013hz75WAmaXxN2GG64eACGN` | `0 18 * * 1-5` | push + email |
| 19h00 — fechamento | `trig_01HTuEWL5SuodHuXF8ZYEiE4` | `0 22 * * 1-5` | push + email |

### Dois bloqueios antes de ativar

**1. O push desta branch foi negado pelo GitHub.**
`403 Resource not accessible by integration` — a sessão do Claude Code tem leitura, não
escrita, neste repositório. Os arquivos estão commitados localmente (commit
`Adiciona rotina de Daily Ops de Contas Médicas em 5 tarefas para a nuvem`), mas não subiram.

Como resolver: um owner da organização libera escrita para este repo em
https://claude.ai/admin-settings/claude-tag ; ou a Juliana reconecta a autorização do GitHub
em claude.ai → Settings → Connectors. Alternativa sem depender disso: descompactar o tarball
entregue no chat e commitar à mão.

Enquanto os arquivos não estiverem na branch, **as Routines abortam de propósito** — o
bootstrap checa se o SKILL.md existe e responde `abortado: ... não encontrado no repositório`
em vez de improvisar o ritual de memória.

**2. Connectors — RESOLVIDO em 19/08.**
O `create_trigger` não aceitou o parâmetro `connectors` nesta organização, então as Routines
nasceram sem eles. A Juliana anexou os connectors pela interface do claude.ai. Verificado: as 5
Routines têm Notion, Slack, Metabase-MCP-Server, Google-Drive (e Google-Calendar).

### Checklist de ativação

1. [ ] Subir esta branch para o GitHub (bloqueio 1).
2. [x] Anexar connectors às 5 Routines — feito em 19/08.
3. [ ] Confirmar o bloco de mapeamento de responsáveis em `shared/00-identificadores.md`.
4. [ ] Ativar as Routines 02, 03, 04 e 05 e observar 2–3 dias em cima do report atual.
5. [ ] Pausar as Routines `Daily-contas-medicas` e `contas-medicas-decisions-sync`, e só então
       ativar a Routine 01 — senão o canal recebe o report duas vezes.
