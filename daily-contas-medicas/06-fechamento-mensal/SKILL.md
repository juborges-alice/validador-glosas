# 06 · Fechamento mensal dos Golden KPIs — comentários para o report da diretoria

Tarefa **mensal**, roda no **2º dia útil do mês** (10h BRT) e entrega por **DM no Slack da OM**
os comentários dos 2 Golden KPIs de Contas Médicas sobre o **mês que acabou de fechar**:

| Golden KPI (nome na planilha) | ID na planilha | Fonte oficial do Actual (coluna `Link`) | KPI equivalente na rotina diária (card) |
|---|---|---|---|
| Glosa (% Glosa geral) | `insurance_07` | question **65150** (glosa mensal instituições de saúde) | `% Glosa Geral - HI` (65942) |
| Resumo de Ganhos HS com crítica | `insurance_08` | question **30858** (% de resumos criticados) | `% Resumos Criticados - HS` (30858) |

**Atenção — a glosa tem duas fontes que NÃO batem.** O número oficial do report é o da question
linkada na planilha (65150). O card da daily (65942) mede um recorte diferente: em set/26 o
fechamento foi **5,30% no report** contra 5,25% na daily. Use sempre a fonte da coluna `Link` da
planilha para o Actual; o card da daily serve só para explicar a variação (drill por tipo,
motivo, prestador). Se a coluna `Link` mudar, siga o link novo.

O report é lido pelo **CEO e por toda a diretoria**. A tarefa **não publica nada**: só propõe.
Quem revisa, ajusta e cola na planilha é a OM.

Leia antes de começar, nesta ordem:
1. `daily-contas-medicas/shared/00-identificadores.md` — IDs de canal, datatables, cards.
2. `daily-contas-medicas/shared/02-metabase.md` — como executar card sem expor a API key.
3. `daily-contas-medicas/06-fechamento-mensal/estilo-comentarios.md` — **o padrão do texto**.
   É o arquivo mais importante desta tarefa.

---

## Passo 0 · Guard de data — só no 2º dia útil

A Routine dispara do dia 1 ao 6 de todo mês (seg–sex). Calcule, no fuso America/Sao_Paulo,
qual é o **2º dia útil do mês corrente**, pulando sábados, domingos e os feriados da lista de
`shared/01-regras-de-registro.md` §5 (nacionais fixos, móveis do ano, estaduais de SP).

- Hoje **não** é o 2º dia útil → responda só `pulado: hoje não é o 2º dia útil do mês` e encerre.
- Exceção: se houver uma mensagem extra, além do prompt da Routine, com `MODO TESTE`, ignore
  o guard (disparo manual pela OM). Se ela trouxer também `MÊS=Mmm/AA`, use esse mês como
  referência em vez do mês anterior.

**Por que o 2º dia útil e não o 1º:** a base de glosa sofre revisão retroativa nos primeiros dias
(em 22/09/2026 a mesma janela saltou +0,82pp de um dia para o outro). Um dia útil a mais de
maturação reduz o risco de o número do report mudar depois de enviado.

Mês de referência = **mês anterior ao de hoje** (ex.: rodando em out/26, o mês é set/26).

## Passo 1 · Planilha de Golden KPIs — BP, histórico e padrão de comentário

A planilha muda a cada quadrimestre (QD). Hoje é **`Golden KPIs Insurance QD3`** (file ID
`1tVdNwlDTqwKUjC0WFvbgnLSxNR282MmYN27W54Kk5Jg`, aba `6. Insurance`, colunas Set/26 a Dez/26).
O histórico de Mai/26 a Ago/26 está na planilha anterior, `QD2_26_Alice_Golden_KPIs`
(file ID `1kZaROFjPectFG-zUEwYzIzmVV5c4ZL9Lw7xzwD8Bng4`, aba `6. Insurance`).

Como achar a planilha certa:
1. Procure no Drive (`search_files`) por título contendo `Golden KPIs Insurance` e pegue a mais
   recente que tenha colunas `Actual (<Mmm/AA do mês de referência>)`.
2. Se não achar, use o file ID da QD3 acima. Se o mês de referência não estiver nela (virada de
   QD), avise na DM: `Planilha do novo QD não encontrada — me passe o link`.

Como ler:
- `read_file_content` **não traz** as linhas 13+ (só uma amostra). Use `download_file_content`
  com `exportMimeType` = `text/csv`: a planilha QD3 tem uma única aba e o CSV vem completo. Se
  vier mais de uma aba, use o export `.xlsx` (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`),
  grave no scratchpad e leia com `openpyxl` (`data_only=True`; `pip install openpyxl` se faltar).
- A **linha** de cada KPI pela coluna `ID` (`insurance_07`, `insurance_08`). Não fixe número de
  linha nem nome do KPI — o nome já mudou (`Disallowance` → `Glosa`).
- As **colunas** pelo cabeçalho: `Actual (Mmm/AA)`, `BP (Mmm/AA)`, `Variação (Mmm/AA)`,
  `Comentário (Mmm/AA)`, com o mês em PT e 3 letras (`Set/26`, `Out/26`).

Extraia por KPI:
- **BP do mês de referência** (QD3: Glosa 4,40% · Resumos HS 3,90% de set a dez/26). Se a
  célula estiver vazia, **não invente**: diga na DM `BP do mês não encontrado na planilha`.
- **Actual e Comentário dos 3 meses anteriores** (na planilha atual e, se preciso, na do QD
  anterior) — para a série e para o tom.
- `Direção`: os dois são `↓ menor melhor`.

Os comentários já publicados são **o padrão da operação**. Releia-os antes de escrever (ver
`estilo-comentarios.md`).

## Passo 2 · Valor fechado do mês

Execute as fontes oficiais seguindo **à risca** `shared/02-metabase.md` (key só em variável,
resposta em arquivo, nunca SQL próprio). Antes de executar, faça `GET /api/card/{ID}` e confira
o array `parameters`: se houver filtro de data, aponte para o mês de referência fechado.
- **65150** — Glosa, mês de referência fechado. **Este é o Actual do report.**
- **30858** — Resumos HS, mês de referência fechado: Actual, numerador (críticas) e
  denominador (resumos).

Para explicar a variação da glosa, leia o fechamento da daily (o card 65942 e os drills dele já
estão nas páginas de Execução de Rotina). Página da **Execução de Rotina do último dia útil do
mês de referência** (datatable Execuções de Rotina, `Nome da rotina` =
`Daily - Contas Médicas - DD/MM/AAAA`), Bloco 1 e Bloco 2.

Se o Metabase falhar ou for bloqueado: **não contorne**. Diga na DM que o Actual não pôde ser
puxado e traga o valor da daily (65942/30858) **marcado como fonte diferente da do report**.

Calcule como a planilha: `Variação = Actual / BP − 1` (ex.: 5,30% / 4,40% − 1 = +20,5%).
Calcule também o delta em pp contra o mês anterior (Actual do mês anterior na planilha).

## Passo 3 · O que explicou a variação — juntar os comentários do mês

O comentário mensal é a **síntese do que o time já discutiu e validou no mês**. Leia:

1. **Decision Log** (`collection://b619a21c-a5f8-4701-a477-f5d150f03066`), entradas com
   `date:Data:start` dentro do mês de referência cujo título ou `KPIs afetados` cite o KPI.
   Leia **`Contexto / problema`, `Decisão tomada` e `Insight de origem`** — a causa validada
   vive em `Decisão tomada`, não no contexto que a rotina escreveu. Considere só o que está
   `Vigente` ou foi confirmado pela OM/responsável; `Rascunho Claude` é hipótese.
2. **Decision Log de KPIs-filhos que explicam o pai**, no mesmo mês: para glosa, `% Glosa por
   Tipo de HI` e `% Glosa Alice por Prestador - HI`; para resumos HS, `Status das Críticas (por
   fatura) - HS` e `Tempo para Resolução de Críticas - HS`.
3. **Action Log** (Log Melhoria Contínua, `collection://39ff0f13-146a-8001-b289-000b5fb3961c`,
   `Operações` = Contas Médicas) — ações ligadas a essas decisões: o que foi concluído no mês e o
   que segue aberto com dono e prazo. É daí que sai o "próximo passo" do comentário.
4. **Slack `#daily_cm_ops_inteligentes` (`C0BH03QKUKY`)** — respostas **humanas** nas threads
   dos KPIs (buscar o nome do KPI no mês) e nas threads semanais de *Highlights e Lowlights*
   (tags `[HI]` = glosa/hospital/lab, `[HS]` = resumos de ganhos). Mensagens da própria rotina
   (`Sent using Claude`) são contexto, não validação.

Regras de síntese:
- **Uma causa só entra no texto se alguém do time a nomeou** (Decision Log com decisão humana,
  resposta na thread ou comentário da planilha). Hipótese da rotina não vira causa.
- **KPI que ficou verde o mês todo raramente tem episódio.** Nesse caso procure a causa nos
  Highlights e nos comentários dos meses anteriores da planilha — a causa estrutural costuma se
  repetir (ex.: automação do resumo de ganhos, citada em jul/26 e confirmada pela OM em out/26).
  Se nada explicar, escreva o comentário só com o resultado e coloque em "Pontos a conferir":
  `Causa não registrada no mês — confirmar antes de publicar`.
- Valor em R$ de um motivo de glosa é, por padrão, **total do motivo**, não de um prestador. Se
  o texto atribuir a um prestador, diga "concentrado em" — ou registre em "Pontos a conferir"
  que o valor é do motivo inteiro.
- **Nada de jargão interno de método** (régua, shift-share, baseline, guard-rail, episódio,
  card, farol). A diretoria lê resultado, causa e próximo passo.

## Passo 4 · Escrever e enviar a DM

Escreva os dois comentários seguindo `estilo-comentarios.md` e envie **uma única mensagem**
por DM para a OM com `slack_send_message`, `channel_id` = `U03A4SS2P1Q` (Juliana Borges).
Não poste no canal da daily.

Formato da DM (mrkdwn do Slack):

```
*Fechamento Golden KPIs — Contas Médicas · <Mmm/AA>*
Rascunho para o report mensal. Revise e cole na coluna `Comentário (<Mmm/AA>)` da aba 6. Insurance.

*Glosa* — Actual <x,xx%> · BP <x,xx%> · Variação <+x,x%> · vs. mês anterior <±x,xxpp>
> <comentário proposto>

*Resumo de Ganhos HS com crítica* — Actual <x,xx%> · BP <x,xx%> · Variação <±x,x%> · vs. mês anterior <±x,xxpp>
> <comentário proposto>

*Pontos a conferir antes de publicar*
• <só o que exige decisão ou checagem da OM — número revisado, BP ausente, causa sem registro,
  valor total vs. prestador, divergência de fonte. Se não houver nada, escreva "nenhum".>

Fontes: <links do Decision Log e das threads usadas, no máximo 5>
```

Formate porcentagem com vírgula e 2 casas (como a planilha: 5,30%, 2,75%). O comentário vai
dentro de `>` para a OM copiar e colar direto.

Ao terminar, responda só uma linha: `enviado: DM de fechamento <Mmm/AA> para a OM` — ou o motivo
de não ter enviado.

## Regras invioláveis

- Nunca escreva na planilha, no Notion ou no canal. Esta tarefa só lê e manda **uma** DM.
- Nunca SQL próprio para valor de KPI; nunca exiba, grave ou exporte a API key do Metabase.
- Informação ausente → diga que está ausente. Nunca invente BP, causa, dono ou prazo.
- Uma execução por mês: antes de enviar, leia a DM com a OM e, se já existir mensagem
  `Fechamento Golden KPIs — Contas Médicas · <Mmm/AA>` deste mês, **não reenvie** — responda
  `abortado: fechamento de <Mmm/AA> já enviado`. Em `MODO TESTE` essa trava não vale.
