WITH lab AS (
  SELECT
    guide_number,
    CASE WHEN provider_economic_group IN ('DASA', 'FLEURY', 'FEMME') THEN provider_economic_group ELSE 'OUTROS' END AS grupo,
    invoice_date,
    disallowance_date,
    appeal_date,
    appeal_status,
    presented_value,
    disallowance_value,
    appeal_value,
    CASE
      WHEN LEFT(TRIM(disallowance_reason), 3) IN ('7DL', '7DK', '7DD', '7DM', '7F8', '7F9', '7EY', '7EZ', '7EL') THEN 'Autorizacao'
      WHEN LEFT(TRIM(disallowance_reason), 3) IN ('7EI', '7G9') THEN 'Local/unidade'
      WHEN LEFT(TRIM(disallowance_reason), 3) IN ('7DY', '7DX', '7G4', '7G3', '7EE') THEN 'Duplicidade'
      WHEN LEFT(TRIM(disallowance_reason), 3) = '7EK' THEN 'Execucao'
      WHEN LEFT(TRIM(disallowance_reason), 3) = '7F6' THEN 'Data'
      WHEN disallowance_reason IS NULL THEN NULL
      ELSE 'Outros'
    END AS familia
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice'
    AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
    AND institution_type ILIKE '%Laboratorio%'
)
SELECT
  grupo,
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  CASE
    WHEN DATEADD(day, 60, disallowance_date)::date < '2026-09-29' THEN 'a_prazo_vencido'
    WHEN DATEADD(day, 60, disallowance_date)::date < '2026-10-01' THEN 'b_vence_set'
    WHEN DATEADD(day, 60, disallowance_date)::date < '2026-11-01' THEN 'c_vence_out'
    ELSE 'd_vence_nov'
  END AS prazo,
  SUM(disallowance_value) AS glosado_sem_recurso,
  COUNT(DISTINCT guide_number) AS guias
FROM lab
WHERE disallowance_date >= '2026-07-01' AND disallowance_value > 0 AND appeal_value IS NULL
GROUP BY 1, 2, 3
