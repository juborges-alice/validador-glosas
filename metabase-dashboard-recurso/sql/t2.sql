WITH base AS (
  SELECT
    invoice_guide_item_key,
    peg_code,
    COALESCE(NULLIF(TRIM(appeal_analysis_auditor_name), ''), '(sem analista)') AS analista,
    appeal_date,
    appeal_analysis_date,
    working_days_from_appeal_to_analysis AS dias_uteis_ate_analise,
    TRIM(appeal_analysis_on_time) AS status_prazo,
    appeal_status,
    CASE WHEN appeal_status IN ('Autorizado', 'Autorizado Parcialmente', 'Negado') AND appeal_analysis_date IS NOT NULL THEN 1 ELSE 0 END AS analisado
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice'
    AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
    AND appeal_value IS NOT NULL
    AND NOT (COALESCE(provider_economic_group, '') = 'DASA' AND appeal_date >= '2026-09-22' AND appeal_date < '2026-10-01')
    [[AND {{tipo_inst}}]]
    [[AND {{grupo}}]]
)
, mensal AS (
  SELECT
    DATE_TRUNC('month', appeal_analysis_date)::date AS mes_analise,
    COUNT(DISTINCT invoice_guide_item_key) AS itens_analisados,
    COUNT(DISTINCT appeal_analysis_date) AS dias_com_analise
  FROM base
  WHERE analisado = 1 AND appeal_analysis_date >= '2026-03-01'
  GROUP BY 1
)
SELECT
  mes_analise,
  itens_analisados,
  dias_com_analise,
  ROUND(itens_analisados::float / NULLIF(dias_com_analise, 0)) AS itens_por_dia_com_analise,
  (SELECT ROUND(SUM(itens_analisados)::float / NULLIF(SUM(dias_com_analise), 0)) FROM mensal WHERE mes_analise BETWEEN '2026-06-01' AND '2026-08-01') AS baseline_jun_ago
FROM mensal
ORDER BY 1
