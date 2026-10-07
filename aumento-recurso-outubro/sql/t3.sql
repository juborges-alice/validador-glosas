SELECT LEFT(TRIM(disallowance_reason),3) AS cod, MAX(LEFT(TRIM(disallowance_reason),80)) AS descr,
  MIN(disallowance_date) AS primeira, MAX(disallowance_date) AS ultima
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
  AND disallowance_value > 0 AND disallowance_date >= '2026-01-01'
  AND LEFT(TRIM(disallowance_reason),3) IN ('7G4','7G3','7DX','7DY','7EE','7G9','7EI','7F6','7EZ','7DK','7G6','7G7','7F0')
GROUP BY 1
