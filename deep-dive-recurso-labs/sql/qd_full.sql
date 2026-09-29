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
  DATE_TRUNC('month', appeal_date)::date AS mes_rec,
  COUNT(DISTINCT guide_number) AS guias_rec,
  COUNT(DISTINCT peg_code) AS pegs_rec,
  SUM(appeal_value) AS vlr_rec,
  SUM(CASE WHEN cod = '7DL' THEN appeal_value ELSE 0 END) AS vlr_rec_7dl,
  COUNT(DISTINCT CASE WHEN disallowance_date < '2026-01-01' THEN guide_number END) AS guias_glosa_2025,
  MAX(appeal_date) AS ult_recurso
FROM lab
WHERE appeal_value IS NOT NULL AND appeal_date >= '2026-01-01'
GROUP BY 1, 2
