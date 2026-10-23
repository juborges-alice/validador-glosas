SELECT DATE_TRUNC('month', appeal_date)::date AS mes, CASE WHEN institution_type ILIKE '%Hospital%' THEN 'H' ELSE 'L' END AS seg,
  CASE WHEN (appeal_date::date - disallowance_date::date) <= 15 THEN '00-15' WHEN (appeal_date::date - disallowance_date::date) <= 30 THEN '16-30' WHEN (appeal_date::date - disallowance_date::date) <= 45 THEN '31-45' WHEN (appeal_date::date - disallowance_date::date) <= 60 THEN '46-60'
       WHEN (appeal_date::date - disallowance_date::date) <= 90 THEN '61-90' ELSE '91+' END AS faixa,
  COUNT(DISTINCT invoice_guide_item_key) AS itens, SUM(appeal_value) AS vlr
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND appeal_value IS NOT NULL AND appeal_date >= '2026-03-01' AND appeal_date <= '2026-10-22'
  AND NOT (COALESCE(provider_economic_group,'') = 'DASA' AND disallowance_date < '2026-01-01' AND appeal_date >= '2026-09-01')
  AND NOT COALESCE(disallowance_reason ILIKE '%7F6%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01', FALSE)
GROUP BY 1,2,3
