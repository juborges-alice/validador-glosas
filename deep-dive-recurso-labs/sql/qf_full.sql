SELECT
  COALESCE(provider_economic_group, 'SEM GRUPO') AS grupo,
  DATE_TRUNC('month', invoice_date)::date AS mes_conta,
  invoice_step,
  COUNT(DISTINCT peg_code) AS pegs,
  COUNT(DISTINCT guide_number) AS guias,
  SUM(presented_value) AS apresentado,
  MAX(invoice_date) AS ult_data
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice'
  AND provider_class = 'Health Institution'
  AND institution_type ILIKE '%Laboratorio%'
  AND TRIM(guide_type_description) = 'GUIA DE RECURSO DE GLOSA'
  AND invoice_date >= '2026-03-01'
GROUP BY 1, 2, 3
