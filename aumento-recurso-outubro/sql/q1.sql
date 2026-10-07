SELECT DATE_TRUNC('week', appeal_date)::date AS semana,
  institution_type,
  COUNT(DISTINCT invoice_guide_item_key) AS itens,
  COUNT(DISTINCT guide_number) AS guias,
  SUM(appeal_value) AS vlr
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND appeal_value IS NOT NULL AND appeal_date >= '2026-07-27'
GROUP BY 1,2 ORDER BY 1,2
