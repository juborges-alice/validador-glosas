SELECT DATE_TRUNC('month', invoice_date)::date AS mes, SUM(presented_value) AS apresentado
FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
    AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%') AND invoice_date >= '2026-01-01' GROUP BY 1 ORDER BY 1
