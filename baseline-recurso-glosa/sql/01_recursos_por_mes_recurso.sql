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
  DATE_TRUNC('month', appeal_date)::date AS mes,
  COUNT(DISTINCT guide_number) AS guias_bruto,
  COUNT(DISTINCT CASE WHEN NOT exc_7f6 AND NOT exc_dasa THEN guide_number END) AS guias_ajust,
  COUNT(DISTINCT CASE WHEN exc_7f6 THEN guide_number END) AS guias_7f6,
  COUNT(DISTINCT CASE WHEN exc_dasa THEN guide_number END) AS guias_dasa,
  SUM(CASE WHEN NOT exc_7f6 AND NOT exc_dasa THEN appeal_value END) AS vlr_rec_ajust,
  SUM(CASE WHEN NOT exc_7f6 AND NOT exc_dasa AND appeal_status IN ('Autorizado','Autorizado Parcialmente','Negado') THEN appeal_value END) AS vlr_analisado,
  SUM(CASE WHEN NOT exc_7f6 AND NOT exc_dasa AND appeal_status IN ('Autorizado','Autorizado Parcialmente') THEN appeal_value END) AS vlr_acatado,
  SUM(CASE WHEN NOT exc_7f6 AND NOT exc_dasa AND appeal_status IN ('Autorizado','Autorizado Parcialmente') AND tipo_erro='EI' THEN appeal_value END) AS acat_ei,
  SUM(CASE WHEN NOT exc_7f6 AND NOT exc_dasa AND appeal_status IN ('Autorizado','Autorizado Parcialmente') AND tipo_erro='EE' THEN appeal_value END) AS acat_ee,
  SUM(CASE WHEN NOT exc_7f6 AND NOT exc_dasa AND appeal_status IN ('Autorizado','Autorizado Parcialmente') AND tipo_erro='Outro' THEN appeal_value END) AS acat_outro,
  COUNT(DISTINCT CASE WHEN NOT exc_7f6 AND NOT exc_dasa AND appeal_status IN ('Autorizado','Autorizado Parcialmente','Negado') THEN guide_number END) AS guias_analisadas,
  COUNT(DISTINCT CASE WHEN NOT exc_7f6 AND NOT exc_dasa AND appeal_status IN ('Autorizado','Autorizado Parcialmente') THEN guide_number END) AS guias_acatadas,
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente','Negado') THEN appeal_value END) AS vlr_analisado_bruto,
  SUM(CASE WHEN appeal_status IN ('Autorizado','Autorizado Parcialmente') THEN appeal_value END) AS vlr_acatado_bruto
FROM base
WHERE appeal_value IS NOT NULL AND appeal_date >= '2026-04-01'
GROUP BY 1 ORDER BY 1
