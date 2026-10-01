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
    [[AND {{periodo}}]]
)
SELECT
  appeal_analysis_date AS dia_analise,
  COUNT(DISTINCT invoice_guide_item_key) AS itens_analisados
FROM base
WHERE analisado = 1
  AND appeal_analysis_date >= '2026-03-01'
GROUP BY 1
ORDER BY 1
