# Dashboard Metabase - Recurso de Glosa (acompanhamento por item)

Dashboard: https://metabase.datalake.alice.tools/dashboard/2774
Coleção: Recurso de Glosa - Acompanhamento (sandbox de Juliana Borges)

Escopo: Health Institution, totvs-alice, fases 1 a 4. Filtro "Tipo de instituição" com padrão Clínica + Laboratório
(limpe o filtro para incluir hospitais). Unidade: item (`invoice_guide_item_key`).

Filtros do painel: Tipo de instituição, Grupo do prestador, Período (cards diários, pareto EI e tabela por analista),
Horas de trabalho por dia (padrão 8) e % do tempo em recurso (padrão 50).

## Aba 1 - Volume de recurso
Exclusões: recursos 7F6 recebidos em jul-ago/26 e recursos DASA de 22 a 30/09/26.

| Card | SQL |
|---|---|
| KPIs (mês atual, baseline) e itens recursados por mês vs baseline | sql/c1.sql |
| Acumulado no mês vs média de 3 meses | sql/c2.sql |
| % de itens glosados que foram recursados (sem limite de prazo; madura após 60 dias) | sql/c3.sql |
| Autorização não localizada (7DL/7F8) | sql/c4.sql |
| Itens recursados por grupo | sql/c5.sql |
| Itens por guia | sql/c6.sql |
| Decisão por item (EI, EE, negado) | sql/c7.sql |
| Dias da glosa ao recurso por grupo | sql/c8.sql |
| Itens por motivo | sql/c9.sql |
| Acatados por erro interno, por motivo | sql/e1.sql |
| Pareto dos motivos acatados por erro interno | sql/e2.sql |

## Aba 2 - Esforço operacional e eficiência
Exclusão: recursos DASA de 22 a 30/09/26. Item analisado = Autorizado, Autorizado Parcialmente ou Negado com data de análise.
SLA = 7 dias úteis do recebimento até a análise, pelo status do TOTVS (`appeal_analysis_on_time`), mesma régua do painel Contas Médicas HI.

| Card | SQL |
|---|---|
| Itens analisados por dia | sql/t1.sql |
| Itens por dia com análise, média mensal vs baseline | sql/t2.sql |
| Distribuição das análises ao longo do mês | sql/t3.sql |
| Dias entre receber e analisar | sql/t4.sql |
| SLA por PEG (pior status entre os itens) | sql/t5.sql |
| SLA por item | sql/t6.sql |
| Itens analisados por analista | sql/t7.sql |
| Tabela por analista (itens/dia, % no prazo, minutos estimados) | sql/t8.sql |
| Tempo estimado por item, por mês | sql/t9.sql |
