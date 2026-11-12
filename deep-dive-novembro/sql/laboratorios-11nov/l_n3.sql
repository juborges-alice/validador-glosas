SELECT CASE WHEN institution_type ILIKE '%Hospital%' THEN 'H' ELSE 'L' END AS seg, COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  LEFT(TRIM(disallowance_reason),3) AS cod,
  CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 'A' ELSE 'O' END AS alvo,
  COUNT(DISTINCT invoice_guide_item_key) AS itens, SUM(disallowance_value) AS glosado,
  SUM(CASE WHEN appeal_value IS NOT NULL AND appeal_date <= '2026-11-11' THEN appeal_value ELSE 0 END) AS recursado
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada') AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%') AND disallowance_value > 0 AND disallowance_date >= '2026-04-01' AND disallowance_date <= '2026-11-11'
GROUP BY 1,2,3,4,5
