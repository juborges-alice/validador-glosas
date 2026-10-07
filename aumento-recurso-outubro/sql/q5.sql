SELECT COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  TRIM(institution_name) AS inst,
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  LEFT(TRIM(disallowance_reason), 70) AS motivo,
  appeal_attempt,
  COUNT(DISTINCT invoice_guide_item_key) AS itens,
  COUNT(DISTINCT guide_number) AS guias,
  SUM(appeal_value) AS vlr,
  MAX(appeal_value) AS maior_item
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND appeal_value IS NOT NULL AND appeal_date >= '2026-10-01'
GROUP BY 1,2,3,4,5 ORDER BY vlr DESC
