SELECT peg_code, COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  CASE WHEN institution_type ILIKE '%Hospital%' THEN 'Hospital' ELSE 'Lab+Clinica' END AS tipo,
  MIN(appeal_date)::date AS dt_recurso, MIN(disallowance_date)::date AS glosa_min, MAX(disallowance_date)::date AS glosa_max,
  COUNT(DISTINCT invoice_guide_item_key) AS itens, COUNT(DISTINCT guide_number) AS guias, SUM(appeal_value) AS vlr,
  SUM(CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN appeal_value ELSE 0 END) AS vlr_autoriz
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND appeal_value IS NOT NULL AND appeal_date >= '2026-03-01'
  AND NOT (COALESCE(provider_economic_group,'') = 'DASA' AND disallowance_date < '2026-01-01' AND appeal_date >= '2026-09-01')
  AND NOT COALESCE(disallowance_reason ILIKE '%7F6%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01', FALSE) AND appeal_date >= '2026-10-01'
GROUP BY 1,2,3 ORDER BY vlr DESC
