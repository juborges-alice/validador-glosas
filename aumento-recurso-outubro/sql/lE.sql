SELECT DATE_TRUNC('month', disallowance_date)::date AS mes_glosa, COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  COUNT(DISTINCT invoice_guide_item_key) AS itens, SUM(appeal_value) AS vlr
FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
    AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%') AND appeal_value IS NOT NULL AND appeal_date >= '2026-10-01' AND (disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%')
GROUP BY 1,2 ORDER BY vlr DESC
