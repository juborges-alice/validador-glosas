# Dashboard Metabase - Recurso de Glosa (acompanhamento por item)

Dashboard: https://metabase.datalake.alice.tools/dashboard/2774
Coleção: Recurso de Glosa - Acompanhamento (sandbox de Juliana Borges)

Escopo: Health Institution, Clínica + Laboratório, totvs-alice, fases 1 a 4.
Unidade: item recursado (`invoice_guide_item_key`); cada linha da tabela é um item.
Exclusões fixas: recursos 7F6 recebidos em jul-ago/26 e recursos DASA de 22 a 30/09/26.
Filtros: tipo de instituição e grupo do prestador.

| Card | SQL |
|---|---|
| KPIs (mês atual, baseline) e itens recursados por mês vs baseline | sql/c1.sql |
| Acumulado no mês vs média de 3 meses | sql/c2.sql |
| % de itens recursados em até 60 dias, por mês da glosa | sql/c3.sql |
| Autorização não localizada (7DL/7F8) | sql/c4.sql |
| Itens recursados por grupo | sql/c5.sql |
| Itens por guia | sql/c6.sql |
| Decisão por item (EI, EE, negado) | sql/c7.sql |
| Dias da glosa ao recurso por grupo | sql/c8.sql |
| Itens por motivo | sql/c9.sql |
