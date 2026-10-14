SELECT appeal_date::date AS dia, COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa, LEFT(TRIM(disallowance_reason),3) AS cod,
  CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 'A' ELSE 'O' END AS alvo,
  COUNT(DISTINCT invoice_guide_item_key) AS itens, COUNT(DISTINCT peg_code) AS pegs, SUM(appeal_value) AS vlr,
  MIN(appeal_date::date - disallowance_date::date) AS dmin, MAX(appeal_date::date - disallowance_date::date) AS dmax,
  SUM(CASE WHEN appeal_date::date - disallowance_date::date > 60 THEN appeal_value ELSE 0 END) AS vlr60, MAX(appeal_attempt) AS tentativa
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND institution_type ILIKE '%Hospital%'
  AND appeal_value IS NOT NULL
  AND NOT (COALESCE(provider_economic_group,'') = 'DASA' AND disallowance_date < '2026-01-01' AND appeal_date >= '2026-09-01')
  AND NOT COALESCE(disallowance_reason ILIKE '%7F6%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01', FALSE) AND appeal_date >= '2026-10-01'
GROUP BY 1,2,3,4,5
