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
    [[AND {{periodo}}]]
)
, rec AS (
  SELECT
    TRIM(COALESCE(SPLIT_PART(motivo, '|', 1), '(sem motivo)')) AS motivo_glosa,
    COUNT(DISTINCT invoice_guide_item_key) AS itens_recursados,
    COUNT(DISTINCT CASE WHEN appeal_status IN ('Autorizado', 'Autorizado Parcialmente') AND tipo_erro = 'EI' THEN invoice_guide_item_key END) AS itens_acatados_ei
  FROM base
  WHERE appeal_value IS NOT NULL AND excluido = 0
  GROUP BY 1
)
SELECT
  motivo_glosa,
  itens_acatados_ei,
  itens_acatados_ei::float / NULLIF(SUM(itens_acatados_ei) OVER (), 0) AS pct_do_total_ei,
  SUM(itens_acatados_ei) OVER (ORDER BY itens_acatados_ei DESC, motivo_glosa ROWS UNBOUNDED PRECEDING)::float
    / NULLIF(SUM(itens_acatados_ei) OVER (), 0) AS pct_acumulado,
  itens_recursados,
  itens_acatados_ei::float / NULLIF(itens_recursados, 0) AS pct_recursados_acatados_ei
FROM rec
WHERE itens_acatados_ei > 0
ORDER BY itens_acatados_ei DESC, motivo_glosa
