SELECT CASE WHEN institution_type ILIKE '%Hospital%' THEN 'H' ELSE 'L' END AS seg, COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  CASE WHEN disallowance_reason LIKE '%7DJ -%' THEN '7DJ' ELSE 'outro' END AS dj,
  COUNT(DISTINCT peg_code) AS pegs, COUNT(DISTINCT invoice_guide_item_key) AS itens, SUM(appeal_value) AS vlr
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND appeal_value IS NOT NULL AND appeal_date >= '2026-10-01' AND appeal_date <= '2026-10-22'
GROUP BY 1,2,3
