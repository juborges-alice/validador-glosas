WITH b AS (
  SELECT invoice_guide_item_key AS k, CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 'A' ELSE 'O' END AS alvo, TRIM(institution_type) AS tipo,
    disallowance_date, disallowance_value, appeal_date, appeal_value, appeal_status,
    provider_economic_group AS grupo, disallowance_reason
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
    AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
)
SELECT 'glosa' AS visao, DATE_TRUNC('month', disallowance_date)::date AS mes, alvo,
  COUNT(DISTINCT k) AS itens, SUM(disallowance_value) AS vlr, NULL::float AS acatado, NULL::float AS analisado
FROM b WHERE disallowance_value > 0 AND disallowance_date >= '2026-01-01' AND disallowance_date <= '2026-10-06'
GROUP BY 1,2,3
UNION ALL
SELECT 'recurso', DATE_TRUNC('month', appeal_date)::date, alvo,
  COUNT(DISTINCT k), SUM(appeal_value),
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente') THEN appeal_value END),
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente','Negado') THEN appeal_value END)
FROM b WHERE appeal_value IS NOT NULL AND appeal_date >= '2026-01-01'
  AND NOT (COALESCE(grupo,'') = 'DASA' AND disallowance_date < '2026-01-01' AND appeal_date >= '2026-09-01')
  AND NOT COALESCE(disallowance_reason ILIKE '%7F6%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01', FALSE)
GROUP BY 1,2,3
ORDER BY 1,2,3
