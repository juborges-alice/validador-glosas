WITH base AS (
  SELECT
    invoice_guide_item_key,
    peg_code,
    COALESCE(NULLIF(TRIM(appeal_analysis_auditor_name), ''), '(sem analista)') AS analista,
    appeal_date,
    appeal_analysis_date,
    working_days_from_appeal_to_analysis AS dias_uteis_ate_analise,
    CASE
      WHEN working_days_from_appeal_to_analysis IS NULL THEN 'Sem informacao'
      WHEN appeal_analysis_date IS NOT NULL AND working_days_from_appeal_to_analysis <= 15 THEN 'Dentro do SLA'
      WHEN appeal_analysis_date IS NOT NULL THEN 'Fora do SLA'
      WHEN working_days_from_appeal_to_analysis <= 15 THEN 'A vencer'
      ELSE 'Fora do SLA'
    END AS status_sla,
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
    [[AND {{periodo}}]]
)
, dia AS (
  SELECT
    analista,
    DATE_TRUNC('month', appeal_analysis_date)::date AS mes_analise,
    appeal_analysis_date,
    COUNT(DISTINCT invoice_guide_item_key) AS itens,
    SUM(CASE WHEN status_sla = 'Dentro do SLA' THEN 1 ELSE 0 END) AS itens_no_prazo,
    COUNT(*) AS linhas
  FROM base
  WHERE analisado = 1 AND appeal_analysis_date >= '2026-03-01'
  GROUP BY 1, 2, 3
)
SELECT
  analista,
  mes_analise,
  SUM(itens) AS itens_analisados,
  COUNT(*) AS dias_com_analise,
  ROUND(SUM(itens)::float / COUNT(*), 1) AS itens_por_dia,
  SUM(itens_no_prazo)::float / NULLIF(SUM(linhas), 0) AS pct_no_prazo,
  ROUND((COUNT(*) * {{horas_dia}} * 60 * {{pct_recurso}} / 100.0) / NULLIF(SUM(itens), 0), 1) AS minutos_estimados_por_item
FROM dia
GROUP BY 1, 2
ORDER BY 2 DESC, 3 DESC
