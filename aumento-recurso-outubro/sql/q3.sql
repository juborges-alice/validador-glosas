SELECT DATE_TRUNC('month', appeal_date)::date AS mes,
  TRIM(institution_type) AS tipo,
  CASE WHEN EXTRACT(day FROM appeal_date) <= 6 THEN 'd01-06' ELSE 'd07+' END AS janela,
  CASE WHEN provider_economic_group = 'DASA' AND disallowance_date < '2026-01-01' THEN 1 ELSE 0 END AS dasa_antigo,
  COUNT(DISTINCT invoice_guide_item_key) AS itens,
  SUM(appeal_value) AS vlr
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND appeal_value IS NOT NULL AND appeal_date >= '2026-03-01'
GROUP BY 1,2,3,4 ORDER BY 1,2,3,4
