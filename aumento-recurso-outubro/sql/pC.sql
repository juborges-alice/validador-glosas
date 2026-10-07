SELECT DATE_TRUNC('month', appeal_date)::date AS mes, TRIM(institution_type) AS tipo,
  COUNT(DISTINCT invoice_guide_item_key) AS itens, SUM(appeal_value) AS vlr,
  COUNT(DISTINCT CASE WHEN NOT (provider_economic_group = 'DASA' AND disallowance_date < '2026-01-01' AND appeal_date >= '2026-09-01')
     AND NOT COALESCE(disallowance_reason ILIKE '%7F6%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01', FALSE)
     THEN invoice_guide_item_key END) AS itens_aj,
  SUM(CASE WHEN NOT (provider_economic_group = 'DASA' AND disallowance_date < '2026-01-01' AND appeal_date >= '2026-09-01')
     AND NOT COALESCE(disallowance_reason ILIKE '%7F6%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01', FALSE)
     THEN appeal_value END) AS vlr_aj
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND appeal_value IS NOT NULL AND appeal_date >= '2026-03-01'
GROUP BY 1,2 ORDER BY 1,2
