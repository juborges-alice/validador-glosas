SELECT DATE_TRUNC('month', disallowance_date)::date AS mes, CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 'autorizacao'
  WHEN disallowance_reason LIKE '%7G4 -%' OR disallowance_reason LIKE '%7G3 -%' OR disallowance_reason LIKE '%7DX -%' OR disallowance_reason LIKE '%7DY -%' OR disallowance_reason LIKE '%7EE -%' THEN 'duplicidade'
  WHEN disallowance_reason LIKE '%7G9 -%' OR disallowance_reason LIKE '%7EI -%' THEN 'local'
  WHEN disallowance_reason LIKE '%7F6 -%' THEN 'data'
  ELSE 'demais' END AS tema,
  SUM(disallowance_value) AS glosado,
  SUM(CASE WHEN appeal_value IS NOT NULL THEN appeal_value ELSE 0 END) AS recursado,
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente') THEN appeal_value ELSE 0 END) AS acatado,
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente','Negado') THEN appeal_value ELSE 0 END) AS analisado
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
  AND disallowance_value > 0 AND disallowance_date >= '2026-04-01' AND disallowance_date < '2026-10-01'
  AND NOT COALESCE(disallowance_reason ILIKE '%7F6%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01', FALSE)
GROUP BY 1,2
