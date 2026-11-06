-- Contas Médicas - Fila de NF: PEGs faturadas sem vínculo de NF - HI (drill da régua de 30% + piso de 2 du)
-- Card 79936 · collection 3609 · sem parâmetros
--
-- Drill item a item do card 79935. Mesma régua e mesmos filtros: PEG em status 4-Faturada, sem
-- nenhuma NF vinculada, janela do ano corrente, grão da PEG.
--
-- ALTERAÇÃO DE 06/11/2026 (decisão da OM, Juliana Borges). O card passa a trazer a ÂNCORA DE
-- ANÁLISE e a classificar cada PEG pela maturidade, acompanhando o piso de 2 dias úteis que o
-- 79935 passou a aplicar. O bloco antigo, que media dias úteis desde o FATURAMENTO, foi
-- substituído pela coluna `maturidade`, que mede dias úteis desde a ANÁLISE — é esse o relógio
-- que vale, porque é a partir da análise que o prazo de gerar e vincular a NF começa a correr.
--
-- TRÊS QUEBRAS:
--
-- horizonte   — separa a competência CORRENTE (que acende o farol de 30% no 79935) do RESQUÍCIO
--               DE COMPETÊNCIAS FECHADAS. A OM decidiu em 27/10/2026 que o resíduo das
--               competências anteriores CONTINUA publicado todo dia na thread do KPI, como fila
--               de cobrança com dono, mesmo não acendendo farol.
--
-- maturidade  — 'Dentro do piso (<2 du da analise)' são as PEGs que NÃO entram no cálculo do
--               farol: a análise foi há menos de 2 dias úteis e o prazo de vincular a NF ainda
--               não venceu. 'Madura (>=2 du da analise)' são as que entram.
--               ⚠️ Só as maduras contam para o percentual do 79935. As do piso saem na lista
--               como visibilidade, nunca como cobrança.
--
-- bloco       — dentro das maduras, separa 'Recem-madura (2 a 5 du)' de 'Atrasada (>5 du)'.
--               A curva medida em 27/10 mostra que a NF segue chegando até cerca de 18 du, então
--               'Atrasada' é recorte de diagnóstico, não atraso confirmado — o que fecha o
--               diagnóstico é a idade, que esta mesma lista devolve PEG a PEG.
--
-- ÂNCORA: administrative_analysis_date, com COALESCE para invoice_billed_step_date quando nula.
-- Mesma regra do 79935 — ver os comentários daquele card.

WITH du AS (
  SELECT date_actual, SUM(CASE WHEN weekend_indr=FALSE AND is_holiday=FALSE THEN 1 ELSE 0 END)
    OVER (ORDER BY date_actual ROWS UNBOUNDED PRECEDING) AS idx
  FROM curated.dim_date_public WHERE date_actual >= '2024-01-01'
), peg AS (
  SELECT peg_code, MIN(invoice_date) AS invoice_date, MIN(institution_code) AS institution_code,
         MIN(invoice_billed_step_date)::date AS billed_date, SUM(payment_value) AS peg_total_value,
         COALESCE(MAX(administrative_analysis_date)::date, MIN(invoice_billed_step_date)::date) AS analise_date,
         MIN(institution_name) AS institution_name, MIN(institution_type) AS institution_type,
         MIN(provider_economic_group) AS grupo_economico,
         MAX(CASE WHEN invoice_step='4-Faturada' THEN 1 ELSE 0 END) AS tem_faturada,
         MAX(CASE WHEN payment_value<>0 THEN 1 ELSE 0 END) AS tem_pagamento,
         MAX(CASE WHEN invoice_number IS NOT NULL AND TRIM(invoice_number)<>'' THEN 1 ELSE 0 END) AS tem_nf
  FROM curated.totvs_procedure_invoice
  WHERE provider_class='Health Institution' AND typing_location='0002' AND fee_type<>'captation'
  GROUP BY peg_code
), f AS (
  SELECT p.*, dh.idx - db.idx AS du_desde_faturamento, dh.idx - da.idx AS du_desde_analise,
         CASE WHEN DATE_TRUNC('month', p.invoice_date) = DATE_TRUNC('month', CURRENT_DATE)
              THEN 'Mes corrente (farol)' ELSE 'Resquicio de competencia fechada' END AS horizonte
  FROM peg p
    LEFT JOIN du db ON db.date_actual=p.billed_date
    LEFT JOIN du da ON da.date_actual=p.analise_date
    LEFT JOIN du dh ON dh.date_actual=CURRENT_DATE
  WHERE p.tem_pagamento=1 AND p.tem_faturada=1 AND p.tem_nf=0
    AND p.institution_code NOT IN ('000446','000819','000823','000822','000813','001216','000814','000816','000815','000817','000820','000821','000818')
    AND p.peg_code NOT IN ('00064866','00062757')
    AND p.invoice_date >= DATE_TRUNC('year', CURRENT_DATE)
), g AS (
  SELECT horizonte AS hz, TRIM(grupo_economico) AS ge,
         SUM(peg_total_value) AS valor_total_grupo, COUNT(*) AS pegs_do_grupo
  FROM f GROUP BY horizonte, TRIM(grupo_economico)
)
SELECT f.horizonte,
       CASE WHEN f.du_desde_analise < 2 THEN 'Dentro do piso (<2 du da analise)'
            ELSE 'Madura (>=2 du da analise)' END AS maturidade,
       CASE WHEN f.du_desde_analise < 2 THEN 'Fora do calculo do farol'
            WHEN f.du_desde_analise <= 5 THEN 'Recem-madura (2 a 5 du)'
            ELSE 'Atrasada (>5 du)' END AS bloco,
       TO_CHAR(DATE_TRUNC('month', f.invoice_date),'MM/YYYY') AS competencia,
       TRIM(f.grupo_economico) AS grupo_economico, TRIM(f.institution_name) AS institution_name,
       TRIM(f.institution_type) AS institution_type, f.peg_code, f.peg_total_value,
       f.billed_date AS data_faturamento, f.analise_date AS data_analise,
       f.du_desde_analise, f.du_desde_faturamento,
       g.valor_total_grupo, g.pegs_do_grupo
FROM f JOIN g ON g.hz = f.horizonte AND g.ge = TRIM(f.grupo_economico)
ORDER BY CASE WHEN f.horizonte = 'Resquicio de competencia fechada' THEN 1 ELSE 2 END,
         CASE WHEN f.du_desde_analise < 2 THEN 2 ELSE 1 END,
         g.valor_total_grupo DESC, f.peg_total_value DESC
