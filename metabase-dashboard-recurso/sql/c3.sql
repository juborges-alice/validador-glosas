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
    AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
    [[AND {{tipo_inst}}]]
    [[AND {{grupo}}]]
)
, ref AS (
  SELECT MAX(appeal_date) AS ult_recurso FROM base WHERE appeal_value IS NOT NULL
)
SELECT
  DATE_TRUNC('month', b.disallowance_date)::date AS mes_glosa,
  CASE WHEN DATEADD(day, 60, LAST_DAY(b.disallowance_date)) <= MAX(r.ult_recurso) THEN 'Fechada' ELSE 'Aberta' END AS situacao_coorte,
  COUNT(DISTINCT b.invoice_guide_item_key) AS itens_glosados,
  COUNT(DISTINCT CASE WHEN b.appeal_value IS NOT NULL AND b.excluido = 0 AND b.appeal_date - b.disallowance_date <= 60 THEN b.invoice_guide_item_key END) AS itens_recursados_60d,
  COUNT(DISTINCT CASE WHEN b.appeal_value IS NOT NULL AND b.excluido = 0 THEN b.invoice_guide_item_key END) AS itens_recursados_total,
  COUNT(DISTINCT CASE WHEN b.appeal_value IS NOT NULL AND b.excluido = 0 AND b.appeal_date - b.disallowance_date <= 60 THEN b.invoice_guide_item_key END)::float
    / NULLIF(COUNT(DISTINCT b.invoice_guide_item_key), 0) AS pct_itens_recursados_60d
FROM base b
CROSS JOIN ref r
WHERE b.disallowance_value > 0
  AND b.disallowance_date >= '2026-01-01'
GROUP BY 1, LAST_DAY(b.disallowance_date)
ORDER BY 1
