WITH base AS (
  SELECT
    invoice_guide_item_key,
    guide_number,
    COALESCE(provider_economic_group, 'SEM GRUPO') AS grupo,
    disallowance_date,
    TRIM(disallowance_reason) AS motivo,
    disallowance_value,
    appeal_date,
    appeal_value,
    appeal_status,
    CASE WHEN TRIM(appeal_operator_reason) LIKE 'EI%' THEN 'EI'
         WHEN TRIM(appeal_operator_reason) LIKE 'EE%' THEN 'EE'
         ELSE 'Outro' END AS tipo_erro,
    CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 1 ELSE 0 END AS motivo_alvo,
    CASE
      WHEN disallowance_reason LIKE '%7F6 -%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01' THEN 1
      WHEN provider_economic_group = 'DASA' AND appeal_date >= '2026-09-22' AND appeal_date < '2026-10-01' THEN 1
      ELSE 0
    END AS excluido
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice'
    AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
    [[AND {{tipo_inst}}]]
    [[AND {{grupo}}]]
)
, rec AS (
  SELECT DATE_TRUNC('month', appeal_date)::date AS mes_recurso, grupo, COUNT(DISTINCT invoice_guide_item_key) AS itens
  FROM base
  WHERE appeal_value IS NOT NULL AND excluido = 0 AND appeal_date >= '2026-03-01'
  GROUP BY 1, 2
),
rk AS (
  SELECT grupo, RANK() OVER (ORDER BY SUM(itens) DESC) AS r FROM rec GROUP BY grupo
)
SELECT
  r.mes_recurso,
  CASE WHEN k.r <= 5 THEN r.grupo ELSE 'Outros' END AS grupo_prestador,
  SUM(r.itens) AS itens_recursados
FROM rec r
JOIN rk k ON k.grupo = r.grupo
GROUP BY 1, 2
ORDER BY 1, 2
