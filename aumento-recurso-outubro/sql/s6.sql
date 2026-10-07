SELECT CASE WHEN institution_type ILIKE '%Hospital%' THEN 'H' ELSE 'L' END AS seg, COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  COUNT(DISTINCT peg_code) AS pegs, COUNT(DISTINCT invoice_guide_item_key) AS itens
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada') AND appeal_value IS NOT NULL AND appeal_date >= '2026-03-01' AND appeal_date < '2026-10-01' AND NOT (COALESCE(provider_economic_group,'') = 'DASA' AND disallowance_date < '2026-01-01' AND appeal_date >= '2026-09-01')
  AND NOT COALESCE(disallowance_reason ILIKE '%7F6%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01', FALSE)
GROUP BY 1,2
