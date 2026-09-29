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
  grupo,
  DATE_TRUNC('month', invoice_date)::date AS mes_conta,
  invoice_step,
  SUM(presented_value) AS apresentado,
  SUM(disallowance_value) AS glosado,
  COUNT(DISTINCT guide_number) AS guias,
  COUNT(DISTINCT peg_code) AS pegs
FROM lab
WHERE invoice_date >= '2026-03-01'
GROUP BY 1, 2, 3
