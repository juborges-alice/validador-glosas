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
)
, item AS (
  SELECT
    peg_code,
    invoice_guide_item_key,
    DATE_TRUNC('month', appeal_date)::date AS mes_recurso,
    CASE WHEN status_sla = 'Fora do SLA' THEN 4
         WHEN status_sla = 'A vencer' THEN 3
         WHEN status_sla = 'Sem informacao' THEN 2
         ELSE 1 END AS sev
  FROM base
  WHERE appeal_date >= '2026-03-01'
),
peg AS (
  SELECT mes_recurso, peg_code, MAX(sev) AS sev FROM item GROUP BY 1, 2
)
SELECT
  mes_recurso,
  CASE sev WHEN 4 THEN 'Fora do SLA' WHEN 3 THEN 'A vencer' WHEN 2 THEN 'Sem informacao' ELSE 'Dentro do SLA' END AS status_sla,
  COUNT(*) AS pegs
FROM peg
GROUP BY 1, 2
ORDER BY 1, 2
