WITH lab AS (
  SELECT
    guide_number,
    peg_code,
    COALESCE(provider_economic_group, 'SEM GRUPO') AS grupo,
    invoice_date,
    invoice_step,
    disallowance_date,
    appeal_date,
    appeal_status,
    LEFT(TRIM(disallowance_reason), 3) AS cod,
    presented_value,
    disallowance_value,
    appeal_value
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice'
    AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
    AND institution_type ILIKE '%Laboratorio%'
)
SELECT
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  cod,
  SUM(disallowance_value) AS glosado,
  COUNT(DISTINCT guide_number) AS guias_glosadas,
  SUM(CASE WHEN appeal_value IS NOT NULL THEN appeal_value ELSE 0 END) AS recursado,
  SUM(CASE WHEN appeal_value IS NOT NULL
            AND appeal_date <= DATEADD(day, 24, DATEADD(month, 1, DATE_TRUNC('month', disallowance_date)))::date
           THEN appeal_value ELSE 0 END) AS rec_d25,
  COUNT(DISTINCT CASE WHEN appeal_value IS NOT NULL THEN guide_number END) AS guias_rec,
  COUNT(DISTINCT CASE WHEN appeal_value IS NOT NULL
            AND appeal_date <= DATEADD(day, 24, DATEADD(month, 1, DATE_TRUNC('month', disallowance_date)))::date
           THEN guide_number END) AS guias_rec_d25,
  SUM(CASE WHEN appeal_status IN ('Autorizado', 'Autorizado Parcialmente') THEN appeal_value ELSE 0 END) AS acatado
FROM lab
WHERE disallowance_date >= '2026-01-01' AND disallowance_value > 0
GROUP BY 1, 2
