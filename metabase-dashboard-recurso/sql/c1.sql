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
, mensal AS (
  SELECT
    DATE_TRUNC('month', appeal_date)::date AS mes_recurso,
    COUNT(DISTINCT CASE WHEN excluido = 0 THEN invoice_guide_item_key END) AS itens_recursados,
    COUNT(DISTINCT CASE WHEN excluido = 1 THEN invoice_guide_item_key END) AS itens_excluidos
  FROM base
  WHERE appeal_value IS NOT NULL
    AND appeal_date >= '2026-03-01'
  GROUP BY 1
)
SELECT
  mes_recurso,
  itens_recursados,
  itens_excluidos,
  (SELECT ROUND(AVG(itens_recursados)) FROM mensal WHERE mes_recurso BETWEEN '2026-06-01' AND '2026-08-01') AS baseline_jun_ago
FROM mensal
ORDER BY 1
