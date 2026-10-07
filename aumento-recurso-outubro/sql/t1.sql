SELECT DATE_TRUNC('month', disallowance_date)::date AS mes, CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 'autorizacao'
  WHEN disallowance_reason LIKE '%7G4 -%' OR disallowance_reason LIKE '%7G3 -%' OR disallowance_reason LIKE '%7DX -%' OR disallowance_reason LIKE '%7DY -%' OR disallowance_reason LIKE '%7EE -%' THEN 'duplicidade'
  WHEN disallowance_reason LIKE '%7G9 -%' OR disallowance_reason LIKE '%7EI -%' THEN 'local'
  WHEN disallowance_reason LIKE '%7F6 -%' THEN 'data'
  ELSE 'demais' END AS tema,
  CASE WHEN provider_economic_group IN ('DASA','FLEURY','FEMME') THEN provider_economic_group ELSE 'OUTROS' END AS grupo,
  COUNT(DISTINCT invoice_guide_item_key) AS itens, SUM(disallowance_value) AS glosado
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
  AND disallowance_value > 0 AND disallowance_date >= '2026-01-01' AND disallowance_date < '2026-10-01'
GROUP BY 1,2,3
