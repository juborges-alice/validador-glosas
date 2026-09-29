WITH base AS (
  SELECT
    guide_number,
    invoice_date,
    disallowance_date,
    appeal_date,
    appeal_status,
    TRIM(disallowance_reason) AS motivo,
    presented_value,
    disallowance_value,
    appeal_value,
    accepted_value,
    CASE WHEN TRIM(appeal_operator_reason) LIKE 'EI%' THEN 'EI'
         WHEN TRIM(appeal_operator_reason) LIKE 'EE%' THEN 'EE'
         ELSE 'Outro' END AS tipo_erro,
    COALESCE(disallowance_reason ILIKE '%7F6%'
      AND ((appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01')
        OR (disallowance_date >= '2026-07-01' AND disallowance_date < '2026-09-01')), FALSE) AS exc_7f6,
    COALESCE(provider_economic_group = 'DASA' AND appeal_date >= '2026-09-01'
      AND disallowance_date < '2026-01-01', FALSE) AS exc_dasa
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice'
    AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
    AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
)
SELECT
  COALESCE(motivo, '(sem motivo)') AS motivo,
  COUNT(DISTINCT guide_number) AS guias_rec,
  SUM(appeal_value) AS vlr_rec,
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente','Negado') THEN appeal_value ELSE 0 END) AS vlr_analisado,
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente') THEN appeal_value ELSE 0 END) AS vlr_acatado,
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente') AND tipo_erro = 'EI' THEN appeal_value ELSE 0 END) AS acat_ei,
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente') AND tipo_erro = 'EE' THEN appeal_value ELSE 0 END) AS acat_ee
FROM base
WHERE appeal_value IS NOT NULL
  AND appeal_date >= '2026-06-01' AND appeal_date < '2026-09-01'
GROUP BY 1
