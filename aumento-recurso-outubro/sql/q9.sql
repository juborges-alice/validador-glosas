SELECT COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  TRIM(institution_type) AS tipo,
  COUNT(*) AS itens, SUM(appeal_value) AS vlr,
  MIN(appeal_date - disallowance_date) AS dmin,
  MAX(appeal_date - disallowance_date) AS dmax,
  SUM(CASE WHEN appeal_date - disallowance_date > 60 THEN appeal_value ELSE 0 END) AS vlr_acima60,
  SUM(CASE WHEN appeal_attempt > 1 THEN appeal_value ELSE 0 END) AS vlr_tentativa2
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND appeal_value IS NOT NULL AND appeal_date >= '2026-10-01'
GROUP BY 1,2 ORDER BY vlr DESC
