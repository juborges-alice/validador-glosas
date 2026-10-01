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
, rec AS (
  SELECT grupo, DATE_TRUNC('month', appeal_date)::date AS mes_recurso, (appeal_date - disallowance_date) AS dias
  FROM base
  WHERE appeal_value IS NOT NULL AND excluido = 0 AND appeal_date >= '2026-04-01' AND disallowance_date IS NOT NULL
)
SELECT
  grupo AS grupo_prestador,
  mes_recurso,
  COUNT(*) AS itens_recursados,
  MEDIAN(dias) AS mediana_dias_glosa_ate_recurso,
  SUM(CASE WHEN dias > 60 THEN 1 ELSE 0 END)::float / COUNT(*) AS pct_itens_apos_60_dias
FROM rec
GROUP BY 1, 2
HAVING COUNT(*) >= 30
ORDER BY 2 DESC, 3 DESC
