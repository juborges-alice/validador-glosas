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

Para cada KPI com valor, primeiro leia a direção ("maior é melhor", "menor é melhor" ou
"bidirecional") **na tabela de direção de `00-identificadores.md`**. A direção é **declarada,
nunca inferida** — ver a regra de direção mais abaixo. Depois aplique:

- **🟢 Verde** — atinge ou supera a `Meta atual`.
- **🟡 Amarelo** — não atinge a meta, mas **não** cruzou o `Limiar de alerta`.
- **🔴 Vermelho** — cruzou o `Limiar de alerta`.
- **⚪** — KPI **sem dado** no dia. Não pontua no farol; registrar para correção da fonte.
  Também ⚪ o KPI que não tenha nem meta nem limiar — acompanhar tendência.
  Também ⚪ o KPI da classe **monitoramento** (`00-identificadores.md`), que por decisão da OM
  nunca acende 🔴 — hoje só o `R$ Faturado Cassi`. Ele sai com número, série e tendência, e o
  limiar dele só vale nos dois checkpoints do mês (dia 15 e último dia útil), onde vira
  **pergunta à OM**, não vermelho.

Casos de borda:

- Sem `Meta atual` mas com `Limiar de alerta`: só 🟢 (não cruzou) ou 🔴 (cruzou); **sem 🟡**.
- Sem `Limiar de alerta` mas com `Meta atual`: só 🟢 (bate) ou 🔴 (não bate); **sem 🟡**.
- **Limiar de tendência** (`crescimento > 1 p.p. vs. mês anterior`, `desvio > 20% vs. média
  histórica`): avalie contra a **série/tendência**, não contra o ponto isolado.
- **Meta e limiar medem grandezas diferentes**: acontece quando o limiar foi recalibrado e a meta
  não. Nesse caso **o limiar manda**, e o KPI só pode ser 🟢 ou 🔴 — **sem 🟡**, porque não existe
  "não atingiu a meta mas não cruzou o limiar" quando os dois não são comparáveis. Diga isso na
  coluna Contexto: `meta de {X} e limiar medem grandezas diferentes; farol pelo limiar`.
  **Nenhum caso vigente hoje.** `PEGs por Status de Análise no SLA - HI` era o caso desde 09/09,
  com `Meta atual` = 90% de aderência contra um limiar de risco de prazo. Em 22/09 a OM passou a
  meta para a mesma grandeza do limiar (contagem de PEGs em aberto por dias úteis), então a
  exceção saiu e o KPI voltou a ter 🟡 normal. A meta de 90% de aderência não se perdeu: ela vive
  em `SLA de Análise de conta - HI`, que é quem mede % de PEGs finalizadas dentro do SLA.

### Regra de direção — a direção é DECLARADA, nunca inferida

**A direção de cada KPI está na tabela "Direção de cada KPI" de `00-identificadores.md`. Leia-a.**
Não deduza a direção da `Definição`, do nome do KPI nem do seu próprio raciocínio sobre o que
seria bom para a operação. Se o KPI não estiver na tabela, ele é **bidirecional** até a OM
declarar — isto é, cruza o limiar para cima e para baixo.

Com a direção em mãos:

- **"menor é melhor"** — variação **para cima** cruza o limiar e gera 🔴. Variação **para baixo**
  é a direção boa e **nunca** gera 🔴, mas pode gerar 🟡 — ver a regra da variação favorável
  atípica, logo abaixo.
- **"maior é melhor"** — o inverso: variação **para baixo** cruza e gera 🔴; variação para cima é
  a direção boa, sujeita à mesma regra de 🟡.
- **"bidirecional"** — cruza nos dois sentidos e gera 🔴 nos dois, conforme o texto do limiar.

### Variação favorável atípica — direção boa não é motivo para ficar calado

Decisão da OM, 07/10/2026: *"quando a variação para baixo é grande, também deveria apontar. É bom
mas é um sinal de desvio do padrão que gostaria de ter visibilidade para entender se é um
potencial erro estrutural ou se de fato é melhoria."*

Variação na direção boa não é acionamento — ninguém precisa corrigir nada hoje —, mas é anomalia.
O lugar dela no farol é **🟡**, que a própria legenda do canal define como "atenção, sem
acionamento: dentro da meta com variação a monitorar".

**Gatilho.** O KPI sai 🟡 quando a variação na direção boa tem **a mesma magnitude do próprio
`Limiar de alerta`**. Não existe número novo para calibrar: se o limiar é "desvio > 20% vs média
histórica", uma melhora de mais de 20% dispara. A régua é espelhada de propósito — recalibrar o
limiar move os dois lados juntos, e ninguém precisa lembrar de um segundo parâmetro.

**Só vale com comparação homogênea.** A regra compara coisas comparáveis, e isso é pré-requisito,
não detalhe:

- **Vale** quando a baseline é casada pelo mesmo ponto da série — acumulado do dia 7 contra a
  média do dia 7 dos 3 meses anteriores (cards 65831 e 65834), mês fechado contra mês fechado,
  fila de hoje contra fila de ontem. É aqui que a OM quer o sinal.
- **Não vale** quando o mês corrente parcial é lido contra um mês fechado. `% Glosa Geral - HI` a
  1,84% no 5º dia útil contra 5,26% de Set/26 fechado não é melhoria de 3,41 p.p.: é um mês em
  que a glosa ainda não foi aplicada. Diferença de maturidade não é variação de desempenho, e
  publicar isso como anomalia enche a primeira semana de todo mês de falso positivo. Nesses
  casos o KPI sai 🟢 e a incompletude vai no Caveat, como já vai hoje.

Na dúvida sobre a homogeneidade, pergunte: *se eu congelasse a operação, os dois lados da conta
teriam o mesmo tamanho?* Se não, a comparação não é homogênea.

**Nunca vira 🔴.** Variação favorável não abre episódio no Decision Log, não gera mensagem solta
no canal e não pede plano de ação. Ela gera **uma linha na thread da Mensagem 1** (formato no
Passo 8 de `01-report-slack/SKILL.md`) e o detalhamento na página.

**A pergunta é obrigatória e é sempre a mesma:** erro estrutural ou melhoria real? Antes de
publicar, rode o **teste de sanidade** — são três checagens e todas saem de dados que a execução
já tem na mão:

1. **O denominador/volume existe?** Queda do numerador com denominador intacto é melhoria
   candidata; os dois caindo juntos é carga incompleta.
2. **O dia tem carga?** Entradas e saídas zeradas ao mesmo tempo, na mesma data, é assinatura de
   ETL que não rodou — não de operação que parou.
3. **O drill reconcilia com o agregado?** Se a soma do drill não bate, o número de cima não está
   descrevendo o que parece descrever.

**Se qualquer uma das três falhar, não é melhoria: é falha de fonte.** Nesse caso o KPI sai **⚪**
(sem dado confiável), com o que foi tentado e o que falhou escrito na linha, e a falha entra como
item de **bug de dado na Mensagem 4**, com dono — não como desvio de operação. Publicar um número
que a fonte não sustenta é pior do que publicar ⚪.

**Supressão segue os mesmos guard-rails do rebaixamento 🔴→🟡 (§1, Etapa 2).** O 🟡 favorável só
vira 🟢 quando existe decisão vigente que explica **exatamente esta** variação, citada por link e
com a página aberta. O caso vigente hoje é o artefato de calendário dos KPIs acumulados, que
comparam o acumulado do mês contra uma média casada **pelo dia do mês** e não pelo dia útil: a OM
examinou em 05/10 e decidiu manter a régua ("isso é normal do mês, não tem nada demais"). Essa
decisão cobre a janela de início de mês que ela examinou — **não** cobre uma queda equivalente no
dia 25, que é outro desvio e volta a ser 🟡. Guard-rail 2 vale igual nos dois sentidos.

> #### ⚠️ Incidente de 07/10/2026 — por que esta regra foi reescrita
>
> Em 07/10 o `R$ Recurso de Glosa acumulado` marcou **R$826.363,99 no dia 7 contra média de 3
> meses de R$361.433,89, +128,65%**, e **saiu 🟢**. Deveria ter saído 🔴. A execução classificou
> o KPI como "maior é melhor" por conta própria — raciocinando que recursar mais seria recuperar
> mais dinheiro — e aplicou a regra de direção para suprimir o vermelho.
>
> **A OM corrigiu no mesmo dia: este indicador NUNCA é "quanto maior melhor". Ele é "quanto
> MENOR melhor".** O valor recursado é o que os prestadores contestam das glosas da Alice; volume
> subindo é mais contestação, mais trabalho e mais risco de devolver glosa, não conquista.
>
> Dois agravantes que esta reescrita fecha:
> 1. A rotina já havia disparado 🔴 para este KPI em 30/09 (−20,54%) e 05/10 (−25,50%), lendo o
>    limiar nos dois sentidos — e em 07/10 leu só para baixo. Incoerência com a própria série.
>    Sob a direção correta, **aqueles dois vermelhos eram falsos como vermelho**, porque queda é
>    a direção boa — mas não eram ruído: pela regra da variação favorável atípica eram **🟡**, com
>    a pergunta de erro estrutural × melhoria real. O erro foi de classe, nos dois sentidos.
> 2. O histórico do episódio `R$ Recurso de Glosa acumulado · desvio desde 05/10` registra, em
>    06/10, que o episódio foi encerrado por o KPI estar "59,4% ACIMA da média de 3 meses", como
>    se subir fosse resolução. **Essa nota está errada e não deve ser usada como precedente.**
>    Este arquivo manda; a nota da página, não.
>
> **Nenhuma decisão vigente rebaixa um desvio para cima deste KPI.** Os episódios de 21/09, 30/09
> e 05/10 explicam desvios **para baixo** (déficit de volume, efeito de calendário de dia útil
> contra dia do mês). Guard-rail 2 do rebaixamento: a decisão precisa cobrir ESTE desvio. Desvio
> de sinal oposto e mecanismo oposto não é o mesmo desvio — **não cite esses episódios para
> rebaixar uma alta, e abra episódio novo.**

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
- **Degraus de prazo, não proporção** — `PEGs por Status de Análise no SLA - HI`: recalibrado em
  22/09/2026 (decisão da OM). O farol sai de **duas contagens absolutas** de PEGs ainda em aberto,
  pela idade em dias úteis desde o `invoice_date`, e o total em aberto do dia **não entra mais**
  no cálculo:
  - `Meta atual` = **0 PEGs em exatamente 7 du**. Havendo alguma, o KPI é 🟡 — é o último dia para
    fechar dentro do SLA interno, ainda dá para salvar, então é aviso e não acionamento.
  - `Limiar de alerta` = **qualquer PEG com ≥13 du**, 2 du antes do SLA externo contratual de 15
    du. Havendo alguma, o KPI é 🔴.
  - **PEGs entre 8 e 12 du já perderam o SLA interno** e não são mais salváveis por ação do dia:
    entram no report como contexto do bloco de 13 du, e **não mexem na cor** até chegarem lá.

  Duas réguas anteriores foram descartadas por acender com fila normal: a de 09/09 (≥5 du acima de
  10% do total em aberto, ou qualquer PEG >7 du), que em 22/09 disparou com 85 de 252 PEGs (33,73%)
  sem nenhuma PEG vencida e com o time analisando a 722% da capacidade esperada; e, antes dela, a
  de ">40% do total em aberto", que disparava com volume normal de início de mês.
- **Alvo capado pela fila, lido em 5 dias úteis** — `Qnt de guias analisadas por dia`:
  recalibrado em 28/09/2026 (decisão da OM). Fonte passa a ser o card **76259**, grão **linha
  (procedimento)**, escopo **Hospital**, janela de mês corrente + mês anterior.
  - `alvo do dia = MIN(teto do time, base cobrável)`, com **metas e réguas separadas por time**.
    Teto = máximo que cada um já analisou num dia útil: **11.210** Hospital, **4.311** Clínica.
    Laboratório está fora do KPI (analisado em massa).
    - **Hospital**: base cobrável = **fila total** do dia. Régua original, inalterada.
    - **Clínica**: base cobrável = **fila vencida**, o que entrou há 3 dias úteis ou mais e segue
      aberto. Sob a fila total ela acendia em 79% dos dias contra 56% de Hospital, e janela, teto
      e corte foram testados sem resolver — o alvo "zerar a fila inteira" fica acima do que aquele
      time entrega. Com a fila vencida cai para 44%. Não se cobra mais do que existe para analisar, nem mais do que o
    time consegue fazer. É o que faz o alvo cair sozinho no fim do mês, sem tabela de sazonalidade.
  - `alvo_5du = MIN(5 × teto, disponíveis_5du)`, onde `disponíveis_5du` = fila de abertura do 1º dia
    da janela + entradas dos 5 dias. **Nunca a soma dos alvos diários**, que contaria a mesma fila
    parada cinco vezes.
  - ⚪ **sem fila** (`alvo_5du = 0`) → não avalia, sai com número e série, sem farol e sem episódio.
  - 🔴 `analisadas_5du < 80% do alvo_5du`; 🟢 caso contrário. **O farol é o `veredito_5du`**
    (decisão da OM, 28/09/2026); o `veredito_dia` do card fica como leitura de apoio, fora do farol.
    O alarme não é diário porque o tempo mediano entre a chegada da conta e a análise é de 3 dias:
    a fila de um dia carrega três dias de trabalho, e 80% dela num dia só seria ciclo de um dia.
  - **Prazo não entra neste KPI.** PEGs vencendo em 7 du saem do `PEGs por Status de Análise no
    SLA - HI` (32465 / 73390), que é canônico. Os dois não compartilham farol. A linha diária de
    PEGs vencendo hoje sai do card **76260**, **sem filtro de tipo** — o escopo Hospital vale só
    para a produtividade.
  - **Este KPI não roteia por concentração.** Com escopo Hospital, o responsável é fixo:
    `<@U073Z4ENBNW>`. Ele sai da lista de KPIs roteáveis por tipo de instituição, que passa de dez
    para nove.
  Detalhamento, evidência e o que foi testado e descartado em `00-identificadores.md`.
- **Mês corrente, e o número oficial é o do 35629** — `SLA de Pagamento de HS`, recalibrado em
  28-29/09/2026 (decisões da OM). Card **35629** é a fonte do percentual; o **76484** reproduz o
  mesmo número e acrescenta linhas de complemento que **não entram no percentual**.
  - **Lê o mês corrente, não o fechado.** No fechado não há ação possível. A leitura do corrente é
    otimista por construção (só classifica fatura já paga), então o caveat de parcialidade é
    obrigatório todo dia, e abaixo de 100 faturas classificadas sai ⚪ sem farol.
  - **Régua do 35629, que é a canônica:** marco inicial = `invoice_binding_date` (vínculo da NF no
    eita), marco final = pagamento, medida em dias úteis (`working_days_from_note_binding_to_payment`),
    corte em 5 DU, universo só de faturas **com NF vinculada e já pagas**, mês de referência é o de
    `invoice_date`. **O limiar de 3% continua valendo** — o número oficial não mudou.
  - **Fatura sem NF do HS não entra no cálculo** (`RECEIVED`, `WAITING_INVOICE`): sem NF não há como
    pagar, logo não é atraso da Alice. Isso o 35629 já fazia via `invoice_binding_date is not null`.
  - **O atraso em aberto sai em linha separada, nunca no percentual.** A OM pediu visibilidade do
    atraso real; o 76484 entrega isso em `complemento - em aberto, ja estourou`,
    `complemento - a vencer` e `complemento - sem NF do HS`. Visibilidade não pode custar a
    comparabilidade do número oficial.
  - ⚠️ **A linha `em aberto, ja estourou` é TETO do atraso, não fato.** `invoice_payment_date` entra
    na base com até ~8 DU de atraso: entre 28 e 29/09/2026 as abertas estouradas de Set/26 caíram de
    157 para 57 porque 103 tinham sido pagas em 17/09 — e dentro do prazo. Nunca afirmar que elas
    *estão* atrasadas, nunca abrir episódio só com base nelas, e nunca ler a queda como melhora da
    operação. O farol e o limiar valem **só** para o percentual oficial.
  - **Por que uma fatura fica fora** sai de `check_sla_payment_reason` (herdado do 35629):
    `atraso pagamento` = total > 5 DU; `atraso operacao` = vínculo→lote PLS > 2 DU;
    `atraso operacao e pagamento` = as duas. Atenção: `atraso operacao` dispara mesmo quando o total
    ficou dentro dos 5 DU — o motivo diz onde o tempo foi gasto, não substitui o veredito.
  - **Os 5 DU têm duas etapas, e o acionável do time é a primeira** (esclarecimento da OM,
    29/09/2026): etapa 1 = vínculo da NF → lote PLS, **2 DU, ação do time de Contas Médicas**;
    etapa 2 = PLS → pagamento, 3 DU, Contas a Pagar. **O KPI não se divide** — segue sendo a visão
    geral dos 5 DU, com um dono só e o roteamento que já existe. Quando ele desviar, o deep dive vai
    para a etapa 1, que o card 76484 expõe na coluna `motivo`. O `atraso operacao` em fatura
    classificada como `no prazo` é aviso antecipado: a etapa 1 estourou e a etapa 2 absorveu.
    Contexto: a etapa 1 roda a **8-9%** fora do prazo enquanto o oficial fica em 1,4-3,9%; **Ago/26
    é o único desvio real, a 22,51%**, com 190 faturas recebendo PLS acima de 2 DU contra 12-35 nos
    outros meses.
  - ⚠️ **`pls_batch_date IS NULL` não significa que o lote não foi gerado.** Em Set/26 há 96 faturas
    **pagas** com esse campo nulo, 92 dentro dos 5 DU. Para medir a etapa 1: conte como falha só
    `pls_batch_date` preenchido com > 2 DU, mais as **sem PLS e sem pagamento** há mais de 2 DU; a
    paga sem `pls_batch_date` é **não mensurável** e fica fora do numerador e do denominador. E
    agrupe por `eita_code`: o 35629 e o 35583 contam **linhas**, não faturas (104 linhas = 88
    faturas em Set/26).
  - O card **35588** não serve para contar o que não tem PLS: `working_days_from_binding_to_pls` é
    NULL em 100% das linhas sem lote e `AVG` ignora nulo, então essas faturas nunca entram na média.
    Ele mede a velocidade de quem passou pela etapa, não quantos não passaram.
  - A cauda de faturas **travadas** (sem PLS, sem pagamento, acima de 2 DU) fica em 63-71 por mês em
    todos os meses, com R$ 0,00 em aberto nos fechados. É **estrutural, não acionável** — não
    reportar como achado; só vira assunto se sair dessa faixa.
  - ❌ **Descartado (erro meu, 29/09/2026):** usar `note_date` (emissão da NF) como marco inicial e
    somar as faturas em aberto dentro do percentual. As duas coisas juntas levaram Set/26 de 1,43%
    para 29,60% — não por piora da operação, mas por troca de régua. Se reaparecer em algum card ou
    registro, está errado.

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

   **Não confunda com o 🟡 de 7 du do `PEGs por Status de Análise no SLA - HI`.** Aquele amarelo
   nasce na **Etapa 1**, da meta do próprio KPI (0 PEGs em 7 du exatos), e é o comportamento
   correto — não é rebaixamento. A tolerância zero aqui proíbe outra coisa: transformar em 🟡, por
   causa já decidida, um 🔴 que a Etapa 1 produziu. PEG com ≥13 du é 🔴 e continua 🔴.
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

### O registro é o EPISÓDIO de desvio, não o dia (decisão da OM, 18/09/2026)

Duas exigências legítimas se chocaram e a solução é distinguir o objeto registrado:

- **Todo KPI 🔴 gera log de desvio**, inclusive quando a conclusão é não fazer nada. É o
  requisito de rastreabilidade da operação: nenhum vermelho pode passar sem registro.
- **A lista tem que ser acionável.** Uma entrada por KPI por dia produziu 86 registros abertos
  em dois meses e tornou o log inútil para responder "o que está pendente".

**O que resolve:** um KPI vermelho por 8 dias pela mesma causa não é 8 desvios — é **um desvio
com 8 dias de história**.

**Episódio de desvio** = sequência contínua de dias em que o mesmo KPI está 🔴 pela mesma causa.
Um episódio = **uma página** no Decision Log, que acumula o histórico dentro de si.

| Situação | O que fazer |
|---|---|
| KPI fica 🔴 e **não há episódio aberto** para ele | **Criar** a página do desvio |
| KPI segue 🔴, **mesma causa** | **Acrescentar uma linha de histórico** ao `Contexto / problema`. Não criar página. |
| KPI segue 🔴 e a **causa mudou** | **Fechar** o episódio atual (`Status de execução` = `Concluída`, nota do motivo) e **abrir** outro |
| KPI volta a 🟢 ou 🟡 | **Fechar** o episódio |

**Linha de histórico** é uma frase dentro do campo, não uma página nova:

```
Desvio aberto em 15/09. SLA em 63,89% (limiar <80%).
Causa: time perdeu acesso ao drive do Fleury. E-mail enviado ao parceiro em 16/09.

16/09: 71,43% — sem retorno do Fleury
17/09: 72,92% — sem retorno do Fleury
18/09: 70,83% — 3º dia útil de espera
```

Quatro dias vermelhos, quatro linhas de texto, **uma página**. Nada deixou de ser registrado; o
que deixou de existir foi a repetição de páginas.

**Como saber se há episódio aberto:** consulte o Decision Log filtrando `Operação` = Contas
Médicas, `Status de execução` = `Em curso`, e o KPI na relation `KPIs afetados`. Achou → é
append. Não achou → é página nova.

**Teto de 14 dias — episódio não vive para sempre (decisão da OM, 18/09/2026).** Se o episódio
aberto tiver **mais de 14 dias corridos** desde a data de abertura, **não dê append**: feche e
abra um novo.

- Fecha o atual: `Status de execução` = `Concluída`, e última linha de histórico
  `DD/MM: {valor} — episódio encerrado por tempo (14 dias); desvio persiste e vai para nova
  análise`.
- Abre o novo com título `{KPI} · desvio desde DD/MM (continuação)` e, na primeira linha do
  `Contexto / problema`, o link do episódio anterior e um resumo de uma linha do que já se
  tentou. **A história não se perde — ela é referenciada, não recopiada.**
- O episódio de continuação nasce **sem causa confirmada**, mesmo que o anterior tivesse uma.
  Isso é o ponto da regra: ele entra em **Aguardando definição da OM** no Bloco 3 e obriga a
  operação a olhar de novo.

Por que o teto existe: um KPI vermelho há 15 dias pela "mesma causa" provavelmente **já não tem
a mesma causa** — ou a causa original deixou de explicar sozinha o tamanho do desvio. O append
indefinido esconderia isso atrás de um registro que ninguém reabre. Quinze dias é um número
arbitrário e assumido como tal: serve para forçar reanálise em intervalo previsível, não porque
14 seja diferente de 13.

**`Data de efeito` é o campo que separa vermelho esperado de vermelho que virou problema.**
Quando uma ação é definida, preencha ali **quando se espera ver o efeito no indicador**. Enquanto
essa data não chegar, o KPI continuar vermelho é o comportamento previsto — não é fato novo e
não vira cobrança. Passou a data e o KPI segue 🔴: **isso** é fato novo, e a pergunta certa é
"a ação de {DD/MM} deveria ter surtido efeito em {DD/MM} e não surtiu".

**Exceção:** KPI do tipo "alerta de trabalho" (`00-identificadores.md`) **nunca** abre episódio.
É fila de trabalho, não desvio a explicar.

### Títulos: o Decision Log indexa por indicador, a daily mostra a ação

Os dois logs têm convenções **diferentes**, de propósito, porque servem a leituras diferentes.

**Decision Log — o título é o indicador.** Ele é um log de desvios por KPI, e é assim que fica
navegável: quem abre a base quer achar "o que já aconteceu com o SLA Recurso de Glosa".

```
{Nome do KPI sem o prefixo} · desvio desde DD/MM
```

Ex.: `SLA Recurso de Glosa - HI · desvio desde 15/09`. O sufixo de data distingue episódios do
mesmo KPI ao longo do tempo — sem ele, dois desvios separados por meses ficam indistinguíveis.

**Action Log — o título é a ação**, começando por **verbo no infinitivo** e descrevendo algo
verificável: `Obter do Fleury a recuperação do acesso ao drive`.

**Na daily, a pendência é sempre a ação** — nunca o título do registro de desvio. O Bloco 3 da
página e a Mensagem 6 têm coluna própria de `Indicador`, então repetir o KPI no texto da
pendência é redundância que rouba a linha do que importa. De onde sai o texto:

1. Existe ação no Action Log ligada ao episódio → use o **título da ação**.
2. Não existe ação, mas o episódio tem `Decisão tomada` → componha a partir dela, começando por
   verbo (ex.: decisão "aguardar retorno do Fleury" → `Aguardar retorno do Fleury sobre o acesso
   ao drive`).
3. **Não existe ação nem decisão** → a pendência é a ausência delas:
   `Definir a ação para {KPI} — desvio sem causa nem ação definida`. Esta é a linha mais
   importante do bloco: um vermelho que ninguém assumiu é mais urgente que qualquer ação em
   andamento, e por isso entra em **Aguardando definição da OM**, no topo.

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

## 4. Não-duplicação e vermelho persistente

**A regra de não-duplicação é o modelo de episódio da §3.** Não existe outra. Um KPI 🔴 tem no
máximo **um** episódio aberto por vez; enquanto ele estiver aberto e a causa for a mesma, o dia de
hoje vira uma **linha de histórico** dentro dele, nunca uma página nova. Releia a §3 antes de
criar qualquer entrada — esta seção só trata do que ela não cobre.

O que decide é a **causa**, não a idade do registro. Episódio velho com a mesma causa continua
sendo o mesmo episódio; episódio de ontem com causa nova já é outro. O teto de 14 dias corridos
existe só como salvaguarda: força uma **continuação** para que um desvio crônico volte à mesa da
OM, e está descrito na §3.

Isso importa principalmente para os crônicos de Contas Médicas — `% Faturas por Status - HS`,
`SLA Recurso de Glosa - HI`, `% PEGs sem NF` e `R$ Faturado Cassi` —, que disparam quase todo dia
e, sob o modelo antigo de um registro por dia, produziram dezenas de páginas por KPI desde julho.

**Histórico — por que esta seção mudou.** Até 17/09/2026 a regra era um "dedup de 14 dias" que
casava entradas pelo prefixo do título `{Nome do KPI} — fora do limiar (DD/MM)`. Ela nunca foi
aplicada de fato, e a auditoria de 16/09/2026 encontrou 88 páginas abertas para 15 KPIs. Em
18/09/2026 a OM substituiu o modelo: o registro passou a ser o episódio (§3), o título passou a
ser `{KPI sem prefixo} · desvio desde DD/MM`, e o log foi consolidado em um episódio aberto por
KPI. **O padrão antigo de título não vale mais** — não o use para casar nem para criar.

**Backlog herdado.** Entradas anteriores a 18/09/2026 seguem no banco com `Status de execução`
= `Concluída`. A rotina **não** deve reabri-las nem tentar consolidá-las por conta própria:
limpeza retroativa é decisão da OM. Para efeito de busca de episódio, só conta o que está
`Em curso`.

**Vermelho persistente (5 dias).** Se um KPI ficar 🔴 por 5 dias consecutivos, o alerta diário
parou de informar. **Não abra outro episódio** — o episódio em curso continua sendo o registro do
desvio. Proponha, dentro dele, uma decisão estrutural (`Classe` = `Mudança de processo` ou
`Escalonamento`, `Tipo` = `Decisão estrutural`), com a ação correspondente no Action Log.
Sinalize a mudança de tratamento no report. A decisão estrutural também depende de validação
humana (ver tarefa 05).

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
| `Resumo da daily · [meet-sync DD/MM]` | Bloco 5 da página | tarefa 04 | ata já distribuída |
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

### O humano dizer que acabou É validação (decisão da OM, 22/09/2026)

**A validação não precisa ser resposta à sua proposta.** Se a pessoa responsável escreve na
thread, com todas as letras, que o item está concluído / resolvido / encerrado / não tem mais
pendência, **isso fecha o item** — mesmo que ela não tenha citado a proposta, não tenha
escrito "ok", e o texto seja um comentário solto.

Aplique a qualquer pendência: linha do Bloco 4, ação no Action Log (`Status` = `Concluída`),
episódio do Decision Log (`Status de execução` = `Concluída`). Registre sempre **quem disse e
quando**: `— concluída por {nome} via Slack em DD/MM`.

**A recíproca continua valendo, e é o limite da regra:** a pessoa **abrir** trabalho novo,
mudar escopo, definir prazo ou dono continua exigindo a proposta estruturada e o OK. Esta
regra só **fecha** o que já existe; ela nunca cria nem altera nada.

**Na dúvida, pergunte — não feche.** "Vamos acompanhar", "estamos olhando", "acho que já era"
não fecham nada. Fechar exige afirmação inequívoca de conclusão. Quando o texto for ambíguo,
responda na thread pedindo confirmação e deixe o item aberto.

**O incidente que originou a regra (22/09/2026).** Em 21/09 a causa raiz da glosa do Hospital
São Francisco e do Santa Mônica foi apurada e escrita na thread pela responsável, que
registrou a decisão de **apenas acompanhar**. A rotina não fechou nada, porque o texto não era
resposta formal a uma proposta — e no dia seguinte o item reapareceu como pendência aberta,
com a própria rotina sugerindo "fechar plano de ação, dono e prazo". Na daily de 22/09 a OM
teve que explicar ao time que era preciso ir à thread e escrever "concluída" de novo. Exigir
que a pessoa repita, no formato certo, algo que ela já disse claramente é atrito que desgasta
o ritual — e é o time pagando pela rigidez da rotina.

---

## 7. Fronteira entre sinalização e pendência

O mesmo item **nunca** aparece nos dois lugares:

- **D0 (dia em que foi sinalizado):** vive só no Bloco 3 da página. Ainda não é pendência.
- **No fechamento (tarefa 05):** item com `Leitura` = `→ Decisão`, `→ Ação` ou `→ Escalar`
  que continua aberto **migra** para o Bloco 4 como pendência (`Fonte` = `Bloco 3`,
  `Venceu` = data em que foi sinalizado). `→ Monitorar` não migra.
- **D+1 em diante:** aparece **apenas** no Bloco 4. Não recriar linha no Bloco 3 mesmo que
  alguém volte a falar do assunto.
- **Item já em pendência que volta a ser comentado:** atualize o `Status` da linha existente
  no Bloco 4. Nunca abra sinalização nova nem segunda pendência. Vale para qualquer sync.

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
