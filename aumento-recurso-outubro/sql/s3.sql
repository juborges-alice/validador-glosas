SELECT DATE_TRUNC('month', disallowance_date)::date AS mes, CASE WHEN institution_type ILIKE '%Hospital%' THEN 'H' ELSE 'L' END AS seg, CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 'A' ELSE 'O' END AS alvo,
  COUNT(DISTINCT invoice_guide_item_key) AS itens, SUM(disallowance_value) AS glosado
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada') AND disallowance_value > 0 AND disallowance_date >= '2026-01-01' AND disallowance_date <= '2026-10-06'
GROUP BY 1,2,3 ORDER BY 1,2,3
