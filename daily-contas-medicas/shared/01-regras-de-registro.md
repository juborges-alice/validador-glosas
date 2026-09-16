# Regras compartilhadas — farol, registro e idempotência

Lido pelas 5 tarefas. As tarefas de sync não reimplementam nada disto.

---

## 1. Farol

As cores respondem **"alguém precisa agir"**, não "está dentro da meta".

| Farol | Significado |
|---|---|
| 🟢 | Dentro da meta / limiar não cruzado |
| 🟡 | Atenção sem acionamento: dentro da meta com variação a monitorar, **ou** fora do limiar com o desvio já explicado por decisão vigente do OM |
| 🔴 | Fora do limiar sem explicação vigente — acionamento imediato |
| ⚪ | Sem meta e sem limiar aplicável — acompanhar tendência |

**Regra do ⚪.** KPI **sem dado** no dia entra como ⚪ e **não pontua** no farol (registrar
para correção da fonte). KPI **sem meta nem limiar** é ⚪ normal e **pontua**.

### Ordem de avaliação — sem pular etapa

**Etapa 1 — cor candidata pelo catálogo.** O `Limiar de alerta` de Contas Médicas é escrito
em linguagem operacional e já traz a condição de disparo (ex: `% glosa > 5% no mês; ou
crescimento > 1 p.p. vs. mês anterior`). Aplique o limiar **como está escrito**. Não invente
threshold genérico por tipo de métrica.

- Cruzou o limiar → candidata 🔴.
- Tem `Meta atual` e não atinge, mas não cruzou o limiar → 🟡.
- Tem `Meta atual` e atinge, e não cruzou o limiar → 🟢.
- Sem `Meta atual`, só limiar → só 🟢 (não cruzou) ou 🔴 (cruzou). Sem 🟡 nesta etapa.

**Regra de direção.** Variação na direção boa de um KPI "menor é melhor" nunca gera 🟡 nem
🔴 — confirma 🟢, qualquer que seja a magnitude. Determine a direção pela `Definição` /
`Meta atual` / `Tipo de métrica`, nunca pelo nome.

**Etapa 2 — rebaixamento por decisão vigente (a única permitida).** Contas Médicas não tem
árvore clínica de classificação. O que rebaixa 🔴 → 🟡 aqui é **exclusivamente** uma decisão
vigente do Decision Log que já explica aquele desvio (ver §2). Nada mais rebaixa.

**Guard-rail — sem rebaixamento fora da decisão vigente.** Se a Etapa 1 deu 🔴 e não existe
decisão vigente explicativa para aquele KPI, o farol **é 🔴 e abre deep dive**. Não rebaixe
por "parece pequeno", "é começo de mês", "amostra baixa" ou hipótese própria. Antes de
publicar, confira: nenhum KPI 🟡 pode estar fora do limiar sem uma decisão vigente citada
por link.

**Tolerância zero — KPI com meta explícita.** `SLA de Análise de conta - HI` (meta 90%) e
`PEGs por Status de Análise no SLA - HI` (meta 90%) são compromisso de serviço: **qualquer**
valor abaixo da meta é 🔴, sem rebaixamento, mesmo com decisão vigente explicando a causa.
Nesse caso a decisão vigente entra no texto ("causa já decidida em DD/MM"), mas a cor
permanece 🔴. Se a operação passar a ter um KPI de prazo regulatório (ANS ou contratual),
acrescente-o aqui.

**Período de comparação.** Acompanha a cadência do KPI: diário lê o dia (ou o acúmulo
retroativo, ver §5); semanal lê a semana. KPI com meta compara contra `Meta atual`. KPI sem
meta compara contra o baseline que o próprio `Limiar de alerta` nomeia (ex: "média dos
últimos 3 meses", "mês anterior") — nunca contra um baseline que você escolheu.

**Caveats.** Sempre cite os `Caveats` do KPI ao reportar o número. Caveat vazio → "sem
caveats registrados". Quando o farol só é o que é por causa de uma decisão metodológica
vigente, diga isso no Caveat da linha: o leitor precisa saber qual régua foi usada.

---

## 2. Decisões vigentes — ler ANTES de calcular

Leia os ~20 registros mais recentes do Decision Log da operação. A query **deve** trazer,
além de `Título da decisão` e `Contexto / problema`, os campos:

`Decisão tomada` · `Estado de complemento` · `Veredito sobre a proposta` · `KPIs afetados` · `Status` · `date:Data:start`

Por que os três primeiros são obrigatórios: `Contexto / problema` é o texto do desvio que a
**própria rotina** escreveu ontem. A resposta humana vive em `Decisão tomada`. Ler só o
Contexto = ler a própria saída passada, não ver nada do lado humano e concluir que o assunto
segue aberto quando o OM já respondeu. Foi exatamente o erro de 18/08/2026.

**ARMADILHA CONHECIDA:** muitas entradas complementadas pelo OM têm `Status` **NULO**. Nunca
julgue existência de decisão vigente por `Status` isolado. É decisão vigente, mesmo com
`Status` nulo, quando:

- `Estado de complemento` = `Complementada por OM` ou `Aprovada`, **OU**
- `Veredito sobre a proposta` = `Recusada` — o OM avaliou e rejeitou o alerta; não reabra
  como se fosse novo.

Monte, antes de seguir, o mapa `KPI → decisões vigentes que o afetam`, classificando cada uma:

- **(a) Metodológica** — muda como o número é calculado ou comparado: excluir período da
  baseline, piso de materialidade, ajuste de limiar, mudança de filtro/proxy. **Aplica-se no
  cálculo** (janela do card) e no farol.
  Exemplos vigentes: desconsiderar mai/26 da média histórica do INCOR (17/08 → baseline
  Jun+Jul); piso de R$50.000 de faturamento no mês para `% Glosa Alice por Prestador`
  (11/08); piso de 7 dias no status para `% Faturas por Status - HS` (11/08).
- **(b) Explicativa** — nomeia a causa do desvio ou registra trade-off deliberado. Aplica-se
  na análise e no plano de ação, e é o que pode rebaixar 🔴 → 🟡 (exceto tolerância zero).
  Exemplos vigentes: atraso no envio pela própria Cassi (11/08, veredito Recusada em 13/08);
  SLA de Recurso de Glosa sacrificado de propósito para proteger o SLA de análise de contas
  (17/08); capacidade realocada para a competência 08 (17/08).

Aplicar a decisão só no texto e manter o número antigo é **erro**. Se a decisão diz "baseline
é Jun+Jul", execute o card com a janela de 2 meses.

**Nunca proponha ação que contradiga decisão vigente.** Se achar que a decisão deveria ser
revista, formule como **pergunta ao OM** — não escale por cima dela e nunca acione outro time
(tech, engenharia, dados) sobre causa que o OM já descartou.

**Vermelho previsível.** Quando o mesmo KPI cai 🔴 repetidamente por causa já decidida, a
proposta útil não é investigar de novo: é perguntar ao OM **o horizonte do trade-off** e se o
`Limiar de alerta` deveria ser calibrado para parar de gerar vermelho previsível.

---

## 3. Decisão × ação

**Decisão** responde "o que concluímos": diagnóstico, ajuste de limiar, escalonamento,
investigação ou não-ação. Vai para o **Decision Log**.

**Ação** responde "o que alguém precisa fazer": tarefa concreta, verificável, com dono
nomeado e prazo. Vai para o **Action Log (Log Melhoria Contínua)**.

Uma decisão pode gerar zero, uma ou várias ações. **Nunca registre tarefa executável como
decisão.** Quando a conclusão exigir mudar o processo em si, registre a decisão e sinalize a
necessidade de RFC no Catálogo de Processos Humanos, sem criar ação.

### Campos ao registrar decisão (Decision Log)

`Título da decisão` (title) · `Contexto / problema` · `Insight de origem` ·
`Proposta original do agente` · `Classe da decisão` ∈ {Investigação, Ajuste de limiar,
Mudança de processo, Escalonamento, Não-ação, A definir} · `Tipo` ∈ {Ação operacional,
Decisão estrutural, Não-ação registrada, Esperar mais um ciclo} · `Origem` = `Ritual diário` ·
`Estado de complemento` = `Rascunho Claude` · `date:Data:start` · `KPIs afetados` (relation) ·
`Operação` (relation) · `Fonte / evidência` (url da Execução de Rotina) ·
`Related to Execuções de Rotina (Decisões geradas)` (relation) · `Autor` (person = OM).

Deixe em branco (handoff do OM): `Decisão tomada`, `Veredito sobre a proposta`,
`Owner da ação`, `Prazo`, `Status`, `Status de execução`, `Data de efeito`.

### Campos ao registrar ação (Log Melhoria Contínua)

Obrigatórios: `Ação` (title, no infinitivo) · `Descrição` · `Tipo de Ação` (multi-select) ∈
{Gestão de Caso, Gestão de Resultado, Gestão de Projeto} · `Responsável` (person) ·
`date:Prazo:start` · `date:Data da Criação:start` · `Status` = `A iniciar` ·
`Operações` (relation) = Contas Médicas · `Alliance` = `Insurance` · `Origem` =
`Ritual diário` · `Decisão de origem` (relation) = a entrada do Decision Log que a gerou.

`Prioridade` = `Sim` só quando houver risco regulatório, assistencial ou de pagamento travado
a prestador. `Time responsável` só quando a ação é de outro time (Auditoria, Omissão, HCDev,
Jurídico, Agudo Hospitalar).

Atenção aos valores exatos: o `Status` do Action Log é `Em andamento` (não "Em curso"); o
`Status de execução` do Decision Log é que usa `Em curso`.

### Guardrail de criação de página (vale para as duas tabelas)

A chamada de criação **precisa** especificar explicitamente o `parent` como o
`data_source_id` da tabela correta. Sem `parent`, a página nasce solta no workspace: só o
título é salvo e as demais properties são descartadas **silenciosamente, sem erro**. Depois
de criar, confirme com uma query SQL contra o data source que a página aparece com as
properties preenchidas.

---

## 4. Dedup e vermelho persistente

**Dedup 14 dias.** Antes de criar entrada nova no Decision Log, procure decisão **aberta** do
mesmo KPI nos últimos 14 dias. Se existir, anexe a ocorrência do dia na entrada existente
(data + valor) em vez de criar linha nova. Isso importa principalmente para os crônicos de
Contas Médicas: `% Faturas por Status - HS`, `SLA Recurso de Glosa - HI`, `% PEGs sem NF` e
`R$ Faturado Cassi`, que disparam quase todo dia.

**Vermelho persistente (5 dias).** Se um KPI ficar 🔴 por 5 dias consecutivos, o alerta
diário parou de informar. Encerre as investigações diárias abertas do tema e abra **uma**
decisão estrutural (`Classe` = `Mudança de processo` ou `Escalonamento`, `Tipo` = `Decisão
estrutural`), com a ação correspondente no Action Log. Sinalize a mudança de tratamento no
report. A decisão estrutural também depende de validação humana (ver tarefa 05).

**Dedup de pendência.** Antes de criar qualquer linha de pendência, confira se o assunto já
tem pendência aberta (mesmo KPI, mesmo prestador, mesmo bug). Se tiver, **atualize o
`Status` da linha existente** — nunca uma segunda linha.

---

## 5. Cobertura retroativa — segunda-feira e pós-feriado

Antes de qualquer coisa, determine as datas de referência.

1. Verifique a data de hoje.
2. Liste os dias corridos sem cobertura desde o último dia útil anterior, exclusive:
   - Segunda-feira → sexta + sábado + domingo
   - Dia anterior foi feriado nacional ou estadual de SP → incluir esses dias
   - Caso contrário → nenhum dia retroativo

**Feriados nacionais fixos:** 01/01 · 21/04 · 01/05 · 07/09 · 12/10 · 02/11 · 15/11 · 25/12
**Móveis** (calcular para o ano): Carnaval (2ª e 3ª) · Sexta-Feira Santa · Corpus Christi
**Estaduais de SP:** 25/01 · 09/07

Quando houver dias retroativos: busque o dado de cada data, descreva as datas cobertas na
**única** linha de `Referência` da Mensagem 1 (não crie uma segunda linha de "cobertura
retroativa"), apresente colunas por data quando forem 2 ou 3 dias, e abra deep dive para
desvios de qualquer das datas com a data no título.

Boa parte dos KPIs de Contas Médicas é acumulada no mês (`thismonth`), então o retroativo
costuma não mudar o número — mas muda a leitura de variação diária. Diga qual dos dois é.

---

## 6. Idempotência — marcadores

Não há tool de reação emoji. O ponto de corte é sempre um **marcador em texto**:

| Marcador | Onde | Quem escreve | Significa |
|---|---|---|---|
| `[dl-sync]` | thread do Slack · Bloco de rastreabilidade da página | tarefas 03/04/05 | thread já processada |
| `Varredura da manhã · [dl-sync]` | rodapé da página | tarefa 03 | corte da pré-daily |
| `Resumo da daily · [meet-sync DD/MM]` | Bloco 6 da página | tarefa 04 | ata já distribuída |
| `Fechamento do dia · [eod-sync DD/MM]` | callout de rodapé | tarefa 05 | dia fechado |
| `[sync 15h DD/MM]` | thread da Msg de pendências | tarefa 04 | cobrança das 17h feita |
| `[eod-sync DD/MM]` | thread da Msg de pendências | tarefa 05 | pendências D+1 postadas |

Regras:

- Toda confirmação que você postar inclui o marcador literal no texto.
- Antes de processar qualquer thread/mensagem, verifique se já existe resposta com o marcador.
- **Já processado** = existe o marcador **E** nenhuma resposta humana com `ts` mais novo que a
  sua confirmação. Nesse caso, pule.
- Resposta humana mais nova que a última confirmação (o time mudou de ideia) → **reprocesse**
  e poste nova confirmação.
- Nunca atualize Decision Log ou Action Log sem, ao final, postar a confirmação — **exceto**
  no caso de conflito, onde você **não** confirma de propósito, para reprocessar quando
  houver consenso.

**Conflito.** Duas ou mais respostas humanas com intenções divergentes e decisivas na mesma
thread → não atualize nada, não confirme, e registre o conflito na saída (qual thread, quem
divergiu, o quê). Respostas que só comentam sem decidir não contam como conflito.

---

## 7. Fronteira entre sinalização e pendência

O mesmo item **nunca** aparece nos dois lugares:

- **D0 (dia em que foi sinalizado):** vive só no Bloco 4 da página. Ainda não é pendência.
- **No fechamento (tarefa 05):** item com `Leitura` = `→ Decisão`, `→ Ação` ou `→ Escalar`
  que continua aberto **migra** para o Bloco 5 como pendência (`Fonte` = `Bloco 4`,
  `Venceu` = data em que foi sinalizado). `→ Monitorar` não migra.
- **D+1 em diante:** aparece **apenas** no Bloco 5. Não recriar linha no Bloco 4 mesmo que
  alguém volte a falar do assunto.
- **Item já em pendência que volta a ser comentado:** atualize o `Status` da linha existente
  no Bloco 5. Nunca abra sinalização nova nem segunda pendência. Vale para qualquer sync.

---

## 8. Regras herdadas do OOS

- **Nunca escreva SQL próprio para valor de KPI.** Execute o card canônico pelo
  `ID Card metabase`. Sem card e sem Sheets mapeado: avise, não improvise métrica.
- **Anti-alucinação.** Informação obrigatória ausente em fonte canônica → `NÃO ENCONTRADO NO
  TEXTO`. Não inferir, completar nem estimar valores.
- **Você não decide.** `Estado de complemento` = `Rascunho Claude`; veredito e decisão são do
  OM. Nas tarefas de sync, você só registra decisão humana explícita — silêncio e emoji não
  são decisão.
- Decisão vigente do OM tem precedência sobre a leitura crua do card **e** sobre a sua própria
  análise do dia anterior.
- Tier 1 = menos crítico, Tier 4 = mais crítico (inverso do comum).
- Notion é índice canônico, não execução. O valor real vive em Metabase.
- **Segurança da API key do Metabase:** nunca exiba, nunca exporte, nunca grave em arquivo.
