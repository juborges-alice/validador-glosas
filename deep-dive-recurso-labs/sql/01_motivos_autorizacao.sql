SELECT
  TRIM(disallowance_reason) AS motivo,
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  SUM(disallowance_value) AS glosado,
  COUNT(DISTINCT guide_number) AS guias
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice'
  AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
  AND institution_type ILIKE '%Laboratorio%'
  AND disallowance_date >= '2026-04-01'
  AND disallowance_value > 0
  AND (disallowance_reason ILIKE '%autoriz%' OR disallowance_reason ILIKE '%senha%' OR disallowance_reason ILIKE '%localiz%')
GROUP BY 1, 2
ORDER BY 1, 2
