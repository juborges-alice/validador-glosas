SELECT CASE WHEN disallowance_date < '2026-07-01' THEN 'abr-jun' ELSE 'jul' END AS coorte,
  LEFT(TRIM(disallowance_reason),3) AS cod,
  SUM(disallowance_value) AS glosado,
  SUM(CASE WHEN appeal_value IS NOT NULL AND appeal_date - disallowance_date <= 60 THEN appeal_value ELSE 0 END) AS rec60
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
  AND disallowance_value > 0 AND disallowance_date >= '2026-04-01' AND disallowance_date < '2026-08-01'
  AND NOT COALESCE(disallowance_reason ILIKE '%7F6%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01', FALSE)
GROUP BY 1,2
