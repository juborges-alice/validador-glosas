SELECT DATE_TRUNC('month', invoice_date)::date AS mes, CASE WHEN institution_type ILIKE '%Hospital%' THEN 'H' ELSE 'L' END AS seg, CASE WHEN institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%' THEN 1 ELSE 0 END AS labclin, SUM(presented_value) AS apresentado
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada') AND invoice_date >= '2026-01-01' AND invoice_date <= '2026-11-09' GROUP BY 1,2,3
