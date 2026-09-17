# Regras compartilhadas — farol, registro e idempotência

Lido pelas 5 tarefas. As tarefas de sync não reimplementam nada disto.

---

## 0. Regra dura de execução — vale para as 5 tarefas

**Você tem UM único turno.** Quando ele termina, ninguém continua o trabalho por você: a sessão
é headless, sem humano acompanhando, e vai para `idle` no estado em que estiver.

- **Faça tudo em linha, você mesma.** Não delegue para subagentes (`Agent` / `Task`), nem em
  background nem em paralelo.
- **Não agende check-in para si mesma** (`ScheduleWakeup`, `send_later`), não inicie comando em
  background, não fique esperando resultado de nada que rode fora deste turno.
- **Não encerre o turno com a entrega por fazer.** Executar os cards do Metabase um a um, em
  sequência, é mais lento e está certo.
- Drill que falha ou demora: **siga sem ele** e escreva o motivo no Caveat do KPI. Entrega
  incompleta com a lacuna declarada é entrega; entrega não escrita não é.
- **Escreva primeiro, enriqueça depois.** Grave a versão mínima do que a tarefa produz assim que
  tiver o essencial, e só então acrescente drills e detalhamento. Nunca o contrário.

**Por que esta regra existe.** Em 17/09/2026, a tarefa 02 leu o report, achou a Execução de
Rotina, puxou o Decision Log dos 9 vermelhos — e então delegou os drills do Metabase a dois
subagentes em background, agendou um check-in e encerrou o turno. Os subagentes terminaram, mas
já não havia turno para usar o resultado. Dez minutos de trabalho, US$ 2,83, e **nenhuma linha
escrita** — nem a página, nem o aviso de falha que o SKILL manda postar quando algo dá errado.
O modo de falha é traiçoeiro justamente porque a sessão parece bem-sucedida: termina `idle`, sem
erro nenhum.

---

## 1. Farol

As cores respondem **"alguém precisa agir"**, não "está dentro da meta".

Para cada KPI com valor, primeiro determine a direção ("maior é melhor" ou "menor é melhor")
a partir da `Definição` / `Meta atual` / `Tipo de métrica`. Depois aplique:

- **🟢 Verde** — atinge ou supera a `Meta atual`.
- **🟡 Amarelo** — não atinge a meta, mas **não** cruzou o `Limiar de alerta`.
- **🔴 Vermelho** — cruzou o `Limiar de alerta`.
- **⚪** — KPI **sem dado** no dia. Não pontua no farol; registrar para correção da fonte.
  Também ⚪ o KPI que não tenha nem meta nem limiar — acompanhar tendência.

Casos de borda:

- Sem `Meta atual` mas com `Limiar de alerta`: só 🟢 (não cruzou) ou 🔴 (cruzou); **sem 🟡**.
- Sem `Limiar de alerta` mas com `Meta atual`: só 🟢 (bate) ou 🔴 (não bate); **sem 🟡**.
- **Limiar de tendência** (`crescimento > 1 p.p. vs. mês anterior`, `desvio > 20% vs. média
  histórica`): avalie contra a **série/tendência**, não contra o ponto isolado.
- **Meta e limiar medem grandezas diferentes**: acontece quando o limiar foi recalibrado e a meta
  não. Nesse caso **o limiar manda**, e o KPI só pode ser 🟢 ou 🔴 — **sem 🟡**, porque não existe
  "não atingiu a meta mas não cruzou o limiar" quando os dois não são comparáveis. Diga isso na
  coluna Contexto: `meta de {X} e limiar medem grandezas diferentes; farol pelo limiar`.
  **Caso vigente:** `PEGs por Status de Análise no SLA - HI` tem `Meta atual` = 90% (aderência ao
  SLA) e limiar que mede **% de PEGs em aberto em risco de estourar o SLA** — grandezas distintas
  desde a recalibração de 09/09. Se a meta for atualizada para a mesma grandeza do limiar, esta
  exceção sai.

**Regra de direção.** Variação na direção boa de um KPI "menor é melhor" nunca gera 🟡 nem 🔴 —
confirma 🟢, qualquer que seja a magnitude.

### O texto do limiar é a regra — leia-o inteiro

O `Limiar de alerta` de Contas Médicas é escrito em linguagem operacional e **carrega
condições dentro do próprio texto**. Aplique-o **exatamente como está escrito**; não reduza a
um número nem invente threshold genérico por tipo de métrica. As condições que já existem hoje
no catálogo, e que precisam ser respeitadas:

- **Piso de materialidade** — `% Glosa Alice por Prestador - HI`: o limiar de 10 p.p. só vale
  para prestadores com faturamento ≥ R$50.000 no mês. Prestador abaixo disso não entra no farol.
- **Piso de idade** — `% Faturas por Status - HS`: só contam faturas há **mais de 7 dias** no
  status, inclusive de meses passados. Fatura em trânsito normal não conta.
- **Regra de dois estágios por dia do mês** — `% Glosa por Tipo de HI`: do **dia 1 ao 19** do
  mês corrente, o critério de >1 p.p. é **tendência/informativo e NÃO dispara 🔴 sozinho** (o
  volume do mês ainda está em maturação); a partir do **dia 20**, o mesmo critério vale como
  alerta pleno e dispara 🔴. Reporte sempre o número; o que muda é a cor.
- **Janela de risco, não de volume** — `PEGs por Status de Análise no SLA - HI`: o limiar é
  PEGs em aberto com ≥5 dias úteis desde o `invoice_date` acima de 10% do total em aberto, **ou**
  qualquer PEG em aberto com >7 dias úteis (já vencida). O critério antigo de ">40% do total em
  aberto" foi descartado por disparar com volume normal de início de mês.

Quando um limiar for recalibrado no Notion, a mudança vale automaticamente: o catálogo é a
fonte, este arquivo é só o resumo do que existe hoje.

### Rebaixamento 🔴 → 🟡 por decisão vigente

Decisão do OM, 16/09/2026: **decisão vigente explicativa rebaixa 🔴 para 🟡**. A lógica de
cores em Contas Médicas passa a ter duas etapas.

**Etapa 1 — cor candidata**, pelo limiar e pela meta, como descrito acima.

**Etapa 2 — rebaixamento, a única exceção permitida.** Um KPI que a Etapa 1 deixou 🔴 vira 🟡
quando existe decisão vigente do Decision Log que **já explica exatamente este desvio**. Nesse
caso o KPI aparece 🟡, **com o link da decisão**, não abre deep dive no Slack e não gera entrada
nova no Decision Log — o detalhamento fica na página do Notion.

As duas classes de decisão agem de formas diferentes:

- **Metodológica** — muda a cor **pelo número**, não por exceção. Ela redefine a janela, o piso
  ou o filtro, você recalcula, e o farol sai do valor corrigido. Isso acontece na Etapa 1, não
  aqui. Exemplo real: excluir mai/26 da baseline do INCOR levou o desvio de -27,26 p.p. para
  +0,13 p.p. contra limiar de 10 p.p. — o KPI virou 🟢 porque o **número** mudou.
- **Explicativa** — nomeia a causa ou registra trade-off deliberado. É esta que rebaixa na
  Etapa 2. Exemplos vigentes: `SLA Recurso de Glosa - HI` (trade-off de 17/08 para proteger o
  SLA de análise de contas), `R$ Recurso de Glosa acumulado` (capacidade realocada, 17/08),
  `R$ Faturado Cassi` (atraso da própria Cassi).

  **Não confie nas datas deste parágrafo — abra as páginas.** Ele já carregou a citação falsa de
  "13/08, veredito Recusada" para o Cassi (ver guard-rail 1), que foi de onde ela se propagou.
  Os exemplos aqui servem para você entender a **classe** da decisão, nunca para ser copiados
  como referência num report.

**Guard-rails do rebaixamento — sem eles a regra vira desculpa para esconder vermelho:**

1. **Só rebaixa com decisão vigente citada por link — e o link tem que ter sido aberto.** Sem
   link, não rebaixa. Não existe rebaixamento por "parece pequeno", "é começo de mês" (isso é a
   regra de dois estágios, e só onde o limiar a define), "amostra baixa" ou hipótese sua.

   **Antes de citar qualquer decisão, abra a página e confira três coisas:** que ela existe, que
   a **data** que você vai escrever é a data dela, e que o `Status` dela não é `Revertida`,
   `Superada` ou `Cancelada`. Só então cite.

   **Isto não é formalidade.** Em 17/09/2026 descobriu-se que o report vinha citando, todos os
   dias desde pelo menos 11/09, uma "decisão de 13/08/2026, Veredito Recusada" para justificar
   não escalar o `R$ Faturado Cassi`. **Essa página não existe.** A entrada mais próxima é de
   **06/08**, e seu `Status` é **Revertida** — nem a data confere, nem está vigente. Uma citação
   inventada foi copiada de um dia para o outro por uma semana, com aparência perfeita de rigor:
   data, veredito e autor, tudo plausível, tudo falso.

   Uma referência que você não abriu é uma referência que você não tem. Se não achar a página,
   escreva `NÃO ENCONTRADO NO TEXTO` e **não rebaixe** — vermelho com causa por confirmar é
   honesto; amarelo apoiado em decisão inexistente não é.
2. **A decisão precisa cobrir ESTE desvio**, não o KPI em geral. Decisão sobre o grupo Fleury
   não rebaixa um desvio concentrado no Einstein.
3. **Fato novo cancela o rebaixamento.** Se a magnitude mudou materialmente em relação a quando
   a decisão foi tomada, ou se um KPI de processo trouxe achado novo, ou se o prazo da decisão
   estourou, o KPI **segue 🔴** e o report apresenta **apenas o fato novo**, formulado como
   pergunta ao OM. Foi assim que o Cassi virou pergunta de horizonte em 18/08: "eram 9 dias de
   estagnação, hoje são 14".

   **Espera por terceiro vence em 3 dias úteis** (decisão da OM, 17/09/2026). Quando a decisão
   vigente é do tipo "aguardando retorno de alguém de fora" — outro time, prestador, operadora —
   o rebaixamento vale por **3 dias úteis** contados da data da decisão. No 4º dia útil sem
   resolução, o **prazo da espera** é o fato novo: o KPI volta a 🔴 e a mensagem diz
   `aguardando {quem} há {N} dias úteis — prazo de 3 du estourado`, formulada como pergunta à OM.

   Isto existe porque o envelhecimento diário não disparava nada: em 17/09 o lote CARMINO passou
   de 5 para 6 dias úteis aguardando precificação e seguiu rebaixado, e sem uma régua qualquer
   incremento é sempre "pequeno demais" para reabrir. A contagem é da **decisão**, não do início
   do caso — decisão nova sobre o mesmo assunto reinicia o relógio, que é o comportamento certo:
   significa que alguém olhou de novo.

   Não confunda com o guard-rail 4: lá o KPI nunca rebaixa; aqui ele rebaixa e o rebaixamento
   expira.
4. **Tolerância zero — dois KPIs nunca rebaixam.** `SLA de Análise de conta - HI` e
   `PEGs por Status de Análise no SLA - HI` são compromisso de serviço: cruzaram o limiar, são 🔴
   mesmo com causa decidida. A decisão entra no texto, a cor não muda. Se a operação passar a ter
   um KPI de prazo regulatório ou contratual, acrescente-o aqui.
5. **Nunca sobe cor.** O rebaixamento só desce, e só de 🔴 para 🟡.

**Vermelho previsível.** Rebaixar não resolve a causa: quando o mesmo KPI cai no limiar dia após
dia pela mesma decisão, a proposta útil é perguntar ao OM o horizonte do trade-off e se o
`Limiar de alerta` deveria ser calibrado — ver §2.

O valor e a baseline usados aqui são os do cálculo **já com as decisões metodológicas vigentes
aplicadas**. Antes de fechar o farol de qualquer KPI, releia o mapa do §2 e confirme que nenhuma
decisão metodológica ficou de fora. Farol calculado sobre baseline que o OM já mandou corrigir é
alerta falso — e alerta falso queima a confiança da operação no ritual.

**Caveats.** Sempre cite os `Caveats` do KPI ao reportar o número. Caveat vazio → "sem caveats
registrados". Quando o farol só é o que é por causa de uma decisão metodológica vigente ou de uma
condição do limiar (piso, janela, estágio do mês), diga isso no Caveat da linha: o leitor precisa
saber qual régua foi usada.

**Período de comparação.** Acompanha a cadência do KPI: diário lê o dia (ou o acúmulo retroativo,
ver §5); semanal lê a semana. KPI com meta compara contra `Meta atual`. KPI sem meta compara
contra o baseline que o próprio `Limiar de alerta` nomeia (ex: "média dos últimos 3 meses", "mês
anterior") — nunca contra um baseline que você escolheu.

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
- **(b) Explicativa** — nomeia a causa do desvio ou registra trade-off deliberado. É a que
  **rebaixa 🔴 → 🟡** na Etapa 2 do farol (§1), respeitados os cinco guard-rails, e a que manda
  referenciar a decisão em vez de abrir investigação nova.
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

**Como procurar, na prática** — esta regra existia mas nunca foi aplicada, e a auditoria de
16/09/2026 encontrou dezenas de entradas duplicadas por KPI desde julho. O passo concreto:

1. Consulte o Decision Log filtrando `Operação` = Contas Médicas e `date:Data:start` nos últimos
   14 dias.
2. Procure entrada cujo `KPIs afetados` contenha o KPI de hoje **ou** cujo `Título da decisão`
   comece com o nome dele. O título segue o padrão `{Nome do KPI} — fora do limiar (DD/MM)`, então
   o casamento por prefixo funciona.
3. Achou → **não crie página nova**. Acrescente ao fim de `Contexto / problema` uma linha
   `DD/MM: {valor} ({variação})` e atualize `Fonte / evidência` para a Execução de Rotina de hoje.
   No Slack, a mensagem do 🔴 aponta para essa entrada existente.
4. Não achou → aí sim crie.

**Backlog herdado.** A tabela já tem dezenas de entradas duplicadas de antes desta regra passar a
valer. A rotina **não** deve tentar consolidá-las por conta própria: limpeza retroativa é decisão
da OM. Para efeito de dedup, considere apenas a **ocorrência mais recente** de cada KPI.

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
