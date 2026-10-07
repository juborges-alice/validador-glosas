SELECT COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  TRIM(institution_type) AS tipo,
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  COUNT(*) AS itens_glosados,
  SUM(disallowance_value) AS glosado,
  SUM(CASE WHEN appeal_value IS NOT NULL THEN appeal_value ELSE 0 END) AS recursado,
  SUM(CASE WHEN appeal_value IS NOT NULL AND appeal_date - disallowance_date <= 45 THEN appeal_value ELSE 0 END) AS rec45,
  SUM(CASE WHEN appeal_value IS NOT NULL AND appeal_date - disallowance_date <= 60 THEN appeal_value ELSE 0 END) AS rec60,
  MEDIAN(CASE WHEN appeal_value IS NOT NULL THEN appeal_date - disallowance_date END) AS mediana_dias,
  MIN(disallowance_date) AS min_glosa, MAX(disallowance_date) AS max_glosa
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND disallowance_value > 0 AND disallowance_date >= '2026-03-01'
  AND COALESCE(provider_economic_group, TRIM(institution_name)) IN ('DASA','FLEURY','FEMME','HCOR','EINSTEIN','CIP PACAEMBU FLEURY','AMERICAS','SANTA MARCELINA','SAHA','SIRIO','BP','HOSPITAL SÃO FRANCISCO')
GROUP BY 1,2,3 ORDER BY 1,2,3
