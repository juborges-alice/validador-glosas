SELECT
  CASE WHEN provider_economic_group IN ('DASA', 'FLEURY', 'FEMME') THEN provider_economic_group ELSE 'OUTROS' END AS grupo,
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  CASE WHEN payment_date IS NULL THEN 'sem_pgto' ELSE 'pago' END AS situacao,
  TRIM(financial_status) AS financial_status,
  COUNT(*) AS itens,
  COUNT(DISTINCT peg_code) AS pegs,
  SUM(disallowance_value) AS glosado,
  SUM(CASE WHEN appeal_value IS NOT NULL THEN appeal_value ELSE 0 END) AS recursado
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice'
  AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
  AND institution_type ILIKE '%Laboratorio%'
  AND disallowance_date >= '2026-05-01' AND disallowance_date < '2026-09-01'
  AND disallowance_value > 0
GROUP BY 1, 2, 3, 4
ORDER BY 1, 2, 3, 4
