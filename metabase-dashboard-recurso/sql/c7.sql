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
SELECT
  DATE_TRUNC('month', appeal_date)::date AS mes_recurso,
  CASE
    WHEN appeal_status IN ('Autorizado', 'Autorizado Parcialmente') AND tipo_erro = 'EI' THEN '1. Acatado - erro interno (EI)'
    WHEN appeal_status IN ('Autorizado', 'Autorizado Parcialmente') AND tipo_erro = 'EE' THEN '2. Acatado - erro externo (EE)'
    WHEN appeal_status IN ('Autorizado', 'Autorizado Parcialmente') THEN '3. Acatado - sem classificacao'
    WHEN appeal_status = 'Negado' THEN '4. Negado'
    ELSE '5. Em analise / protocolado'
  END AS decisao,
  COUNT(DISTINCT invoice_guide_item_key) AS itens
FROM base
WHERE appeal_value IS NOT NULL AND excluido = 0 AND appeal_date >= '2026-03-01'
GROUP BY 1, 2
ORDER BY 1, 2
