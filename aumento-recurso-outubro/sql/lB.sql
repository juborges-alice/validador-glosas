WITH b AS (
  SELECT COALESCE(provider_economic_group, TRIM(institution_name)) || '|' || CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 'A' ELSE 'O' END AS grp,
    TRIM(institution_type) || '|' || CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 'A' ELSE 'O' END AS tipo,
    invoice_guide_item_key AS k, disallowance_date::date AS dg, disallowance_value AS g,
    appeal_date::date AS dr, appeal_value AS r
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
    AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
    AND disallowance_value > 0 AND disallowance_date >= '2026-01-01' AND disallowance_date <= '2026-10-06'
    AND NOT COALESCE(disallowance_reason ILIKE '%7F6%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01', FALSE)
)
SELECT grp, tipo, dg, COUNT(DISTINCT k) AS itens, SUM(g) AS glosado
FROM b
GROUP BY 1,2,3
