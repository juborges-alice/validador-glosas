SELECT appeal_date::date AS dia,
  TRIM(institution_type) AS tipo,
  COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  COUNT(DISTINCT invoice_guide_item_key) AS itens,
  COUNT(DISTINCT guide_number) AS guias,
  COUNT(DISTINCT peg_code) AS pegs,
  SUM(appeal_value) AS vlr,
  SUM(disallowance_value) AS glosado
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND appeal_value IS NOT NULL AND appeal_date >= '2026-09-15'
GROUP BY 1,2,3,4 ORDER BY 1, vlr DESC
