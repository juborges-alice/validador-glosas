WITH lab AS (
  SELECT
    CASE WHEN provider_economic_group IN ('DASA', 'FLEURY', 'FEMME') THEN provider_economic_group ELSE 'OUTROS' END AS grupo,
    DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
    CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 1 ELSE 0 END AS alvo,
    disallowance_date,
    disallowance_value,
    CASE WHEN provider_economic_group = 'DASA' AND appeal_date >= '2026-09-22' THEN NULL ELSE appeal_date END AS rec_date,
    CASE WHEN provider_economic_group = 'DASA' AND appeal_date >= '2026-09-22' THEN NULL ELSE appeal_value END AS rec_value,
    appeal_status
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice'
    AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
    AND institution_type ILIKE '%Laboratorio%'
    AND disallowance_date >= '2026-01-01'
    AND disallowance_value > 0
)
SELECT
  grupo,
  mes_glosa,
  alvo,
  DATE_TRUNC('month', rec_date)::date AS mes_rec,
  CASE WHEN rec_value IS NULL THEN NULL ELSE LEAST(FLOOR((rec_date - disallowance_date) / 5.0) * 5, 180) END AS lag_bin,
  COUNT(*) AS itens,
  SUM(disallowance_value) AS glosado,
  SUM(CASE WHEN rec_value IS NOT NULL THEN rec_value ELSE 0 END) AS recursado,
  SUM(CASE WHEN rec_value IS NOT NULL AND appeal_status IN ('Autorizado', 'Autorizado Parcialmente') THEN rec_value ELSE 0 END) AS acatado,
  SUM(CASE WHEN rec_value IS NOT NULL AND appeal_status IN ('Autorizado', 'Autorizado Parcialmente', 'Negado') THEN rec_value ELSE 0 END) AS analisado
FROM lab
GROUP BY 1, 2, 3, 4, 5
