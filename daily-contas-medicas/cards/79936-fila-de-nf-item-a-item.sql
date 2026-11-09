-- Contas Médicas - Fila de NF: PEGs faturadas sem vínculo de NF - HI
-- Card Metabase 79936 · collection 3609 · drill item a item do card 79935
--
-- RÉGUA VIGENTE: decisão da OM (Juliana Borges) de 06/11/2026, Data de efeito 06/11/2026.
-- https://app.notion.com/p/410f0f13146a811d9267f3d0e093672f
-- Mesmas definições do 79935: piso de maturação de 2 dias úteis após a análise, âncora em
-- administrative_analysis_date com COALESCE para invoice_billed_step_date, agregação por MAX.
--
-- O QUE ESTE CARD DEVOLVE: uma linha por PEG faturada SEM NF, do ano corrente.
--   horizonte  -> separa o resquício de competência fechada do mês corrente (farol)
--   maturidade -> dentro do mês corrente, separa o que entra no farol do que ainda está no piso
--   bloco      -> dentro das maduras, onde olhar primeiro
--
-- ⚠️ "Atrasada (>5 du)" NÃO É ATRASO CONFIRMADO. A curva medida em 27/10/2026 mostra que a NF
-- segue chegando até cerca de 18 du. É recorte de diagnóstico; quem fecha o diagnóstico é a
-- idade PEG a PEG, nas colunas du_desde_analise e du_desde_faturamento.
--
-- As PEGs com maturidade "Dentro do piso" saem na lista como VISIBILIDADE, nunca como cobrança:
-- o prazo delas não venceu.
--
-- A fila do resquício de competências fechadas continua publicada todo dia na thread do KPI,
-- como cobrança com dono, rolando até zerar (decisão da OM, 27/10/2026). Ordenação por valor do
-- grupo econômico — é a ordem de cobrança.
--
-- Reconciliação: a soma de peg_total_value das linhas com horizonte 'Mes corrente (farol)' e
-- maturidade 'Madura (>=2 du da analise)' tem que bater com valor_sem_nf do 79935 no mês corrente.
WITH du AS (
  SELECT date_actual, SUM(CASE WHEN weekend_indr=FALSE AND is_holiday=FALSE THEN 1 ELSE 0 END)
    OVER (ORDER BY date_actual ROWS UNBOUNDED PRECEDING) AS idx
  FROM curated.dim_date_public WHERE date_actual >= '2024-01-01'
), peg AS (
  SELECT peg_code, MIN(invoice_date) AS invoice_date, MIN(institution_code) AS institution_code,
         MIN(invoice_billed_step_date)::date AS billed_date,
         MAX(administrative_analysis_date)::date AS analysis_date,
         SUM(payment_value) AS peg_total_value,
         MIN(institution_name) AS institution_name, MIN(institution_type) AS institution_type,
         MIN(provider_economic_group) AS grupo_economico,
         MAX(CASE WHEN invoice_step='4-Faturada' THEN 1 ELSE 0 END) AS tem_faturada,
         MAX(CASE WHEN payment_value<>0 THEN 1 ELSE 0 END) AS tem_pagamento,
         MAX(CASE WHEN invoice_number IS NOT NULL AND TRIM(invoice_number)<>'' THEN 1 ELSE 0 END) AS tem_nf
  FROM curated.totvs_procedure_invoice
  WHERE provider_class='Health Institution' AND typing_location='0002' AND fee_type<>'captation'
  GROUP BY peg_code
), f AS (
  SELECT p.*,
         dh.idx - db.idx AS du_desde_faturamento,
         dh.idx - da.idx AS du_desde_analise,
         CASE WHEN DATE_TRUNC('month', p.invoice_date) = DATE_TRUNC('month', CURRENT_DATE)
              THEN 'Mes corrente (farol)' ELSE 'Resquicio de competencia fechada' END AS horizonte
  FROM peg p
  LEFT JOIN du db ON db.date_actual = p.billed_date
  LEFT JOIN du da ON da.date_actual = COALESCE(p.analysis_date, p.billed_date)
  LEFT JOIN du dh ON dh.date_actual = CURRENT_DATE
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
       CASE WHEN f.du_desde_analise IS NULL THEN 'Sem ancora de maturacao'
            WHEN f.du_desde_analise >= 2 THEN 'Madura (>=2 du da analise)'
            ELSE 'Dentro do piso (<2 du da analise)' END AS maturidade,
       CASE WHEN f.du_desde_analise IS NULL OR f.du_desde_analise < 2 THEN 'Fora do calculo do farol'
            WHEN f.du_desde_analise <= 5 THEN 'Recem-madura (2 a 5 du)'
            ELSE 'Atrasada (>5 du)' END AS bloco,
       TO_CHAR(DATE_TRUNC('month', f.invoice_date),'MM/YYYY') AS competencia,
       TRIM(f.grupo_economico) AS grupo_economico, TRIM(f.institution_name) AS institution_name,
       TRIM(f.institution_type) AS institution_type, f.peg_code, f.peg_total_value,
       f.billed_date AS data_faturamento, f.analysis_date AS data_analise,
       f.du_desde_analise, f.du_desde_faturamento,
       g.valor_total_grupo, g.pegs_do_grupo
FROM f JOIN g ON g.hz = f.horizonte AND g.ge = TRIM(f.grupo_economico)
ORDER BY CASE WHEN f.horizonte = 'Resquicio de competencia fechada' THEN 1 ELSE 2 END,
         CASE WHEN f.du_desde_analise IS NULL OR f.du_desde_analise < 2 THEN 2 ELSE 1 END,
         g.valor_total_grupo DESC, f.peg_total_value DESC
