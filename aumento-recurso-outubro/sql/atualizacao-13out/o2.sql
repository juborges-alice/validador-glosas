SELECT DATE_TRUNC('month', appeal_date)::date AS mes,
  CASE WHEN EXTRACT(day FROM appeal_date) <= 13 THEN 'd01-13' ELSE 'd14+' END AS janela,
  COUNT(DISTINCT invoice_guide_item_key) AS itens, COUNT(DISTINCT peg_code) AS pegs, SUM(appeal_value) AS vlr
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
  AND appeal_value IS NOT NULL
  AND NOT (COALESCE(provider_economic_group,'') = 'DASA' AND disallowance_date < '2026-01-01' AND appeal_date >= '2026-09-01')
  AND NOT COALESCE(disallowance_reason ILIKE '%7F6%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01', FALSE) AND appeal_date >= '2026-03-01'
GROUP BY 1,2 ORDER BY 1,2
