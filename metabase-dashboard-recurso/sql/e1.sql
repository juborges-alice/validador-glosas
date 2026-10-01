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
, ei AS (
  SELECT
    DATE_TRUNC('month', appeal_date)::date AS mes_recurso,
    TRIM(COALESCE(SPLIT_PART(motivo, '|', 1), '(sem motivo)')) AS motivo_glosa,
    COUNT(DISTINCT invoice_guide_item_key) AS itens
  FROM base
  WHERE appeal_value IS NOT NULL AND excluido = 0
    AND appeal_status IN ('Autorizado', 'Autorizado Parcialmente') AND tipo_erro = 'EI'
    AND appeal_date >= '2026-03-01'
  GROUP BY 1, 2
),
rk AS (
  SELECT motivo_glosa, RANK() OVER (ORDER BY SUM(itens) DESC) AS r FROM ei GROUP BY motivo_glosa
)
SELECT
  e.mes_recurso,
  CASE WHEN k.r <= 8 THEN e.motivo_glosa ELSE 'Outros motivos' END AS motivo_glosa,
  SUM(e.itens) AS itens_acatados_ei
FROM ei e
JOIN rk k ON k.motivo_glosa = e.motivo_glosa
GROUP BY 1, 2
ORDER BY 1, 3 DESC
