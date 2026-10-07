SELECT 'rec' AS v, DATE_TRUNC('month', appeal_date)::date AS mes, COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  COUNT(DISTINCT invoice_guide_item_key) AS itens, SUM(appeal_value) AS vlr,
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente') THEN appeal_value END) AS acatado,
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente','Negado') THEN appeal_value END) AS analisado
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada') AND institution_type ILIKE '%Hospital%'
  AND appeal_value IS NOT NULL AND appeal_date >= '2026-06-01' AND (disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%')
GROUP BY 1,2,3
UNION ALL
SELECT 'glosa', DATE_TRUNC('month', disallowance_date)::date, COALESCE(provider_economic_group, TRIM(institution_name)),
  COUNT(DISTINCT invoice_guide_item_key), SUM(disallowance_value), NULL, NULL
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada') AND institution_type ILIKE '%Hospital%'
  AND disallowance_value > 0 AND disallowance_date >= '2026-04-01' AND disallowance_date <= '2026-10-06' AND (disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%')
GROUP BY 1,2,3
