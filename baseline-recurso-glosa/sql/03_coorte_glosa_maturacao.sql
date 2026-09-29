WITH base AS (
  SELECT
    guide_number,
    invoice_date,
    disallowance_date,
    appeal_date,
    appeal_status,
    TRIM(disallowance_reason) AS motivo,
    presented_value,
    disallowance_value,
    appeal_value,
    accepted_value,
    CASE WHEN TRIM(appeal_operator_reason) LIKE 'EI%' THEN 'EI'
         WHEN TRIM(appeal_operator_reason) LIKE 'EE%' THEN 'EE'
         ELSE 'Outro' END AS tipo_erro,
    COALESCE(disallowance_reason ILIKE '%7F6%'
      AND ((appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01')
        OR (disallowance_date >= '2026-07-01' AND disallowance_date < '2026-09-01')), FALSE) AS exc_7f6,
    COALESCE(provider_economic_group = 'DASA' AND appeal_date >= '2026-09-01'
      AND disallowance_date < '2026-01-01', FALSE) AS exc_dasa
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice'
    AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
    AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
)
SELECT
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  SUM(CASE WHEN motivo LIKE '%7F6%' THEN disallowance_value ELSE 0 END) AS glosado_7f6,
  SUM(CASE WHEN motivo LIKE '%7F6%' AND appeal_value IS NOT NULL THEN appeal_value ELSE 0 END) AS rec_7f6,
  SUM(CASE WHEN motivo NOT LIKE '%7F6%' OR motivo IS NULL THEN disallowance_value ELSE 0 END) AS glosado_sem7f6,
  SUM(CASE WHEN (motivo NOT LIKE '%7F6%' OR motivo IS NULL) AND appeal_value IS NOT NULL AND appeal_date - disallowance_date <= 45 THEN appeal_value ELSE 0 END) AS rec_45d,
  SUM(CASE WHEN (motivo NOT LIKE '%7F6%' OR motivo IS NULL) AND appeal_value IS NOT NULL AND appeal_date - disallowance_date <= 60 THEN appeal_value ELSE 0 END) AS rec_60d,
  SUM(CASE WHEN (motivo NOT LIKE '%7F6%' OR motivo IS NULL) AND appeal_value IS NOT NULL AND appeal_date - disallowance_date <= 90 THEN appeal_value ELSE 0 END) AS rec_90d,
  SUM(CASE WHEN (motivo NOT LIKE '%7F6%' OR motivo IS NULL) AND appeal_value IS NOT NULL THEN appeal_value ELSE 0 END) AS rec_total,
  COUNT(DISTINCT CASE WHEN (motivo NOT LIKE '%7F6%' OR motivo IS NULL) THEN guide_number END) AS guias_glosadas,
  COUNT(DISTINCT CASE WHEN (motivo NOT LIKE '%7F6%' OR motivo IS NULL) AND appeal_value IS NOT NULL AND appeal_date - disallowance_date <= 60 THEN guide_number END) AS guias_rec_60d,
  COUNT(DISTINCT CASE WHEN (motivo NOT LIKE '%7F6%' OR motivo IS NULL) AND appeal_value IS NOT NULL THEN guide_number END) AS guias_rec_total,
  MAX(disallowance_date) AS max_glosa
FROM base
WHERE disallowance_date >= '2026-03-01' AND disallowance_value > 0
GROUP BY 1 ORDER BY 1
