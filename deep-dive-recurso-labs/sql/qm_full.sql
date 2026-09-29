SELECT
  CASE WHEN provider_economic_group IN ('DASA', 'FLEURY', 'FEMME') THEN provider_economic_group ELSE 'OUTROS' END AS grupo,
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  SUM(CASE WHEN payment_date <= '2026-09-10' THEN disallowance_value ELSE 0 END) AS glosado_elegivel_15d,
  SUM(CASE WHEN payment_date <= '2026-09-10' AND appeal_value IS NOT NULL AND appeal_date - payment_date <= 15 THEN appeal_value ELSE 0 END) AS rec_15d_pos_pgto,
  SUM(CASE WHEN payment_date <= '2026-09-15' THEN disallowance_value ELSE 0 END) AS glosado_elegivel_10d,
  SUM(CASE WHEN payment_date <= '2026-09-15' AND appeal_value IS NOT NULL AND appeal_date - payment_date <= 10 THEN appeal_value ELSE 0 END) AS rec_10d_pos_pgto,
  SUM(CASE WHEN payment_date <= '2026-08-26' THEN disallowance_value ELSE 0 END) AS glosado_elegivel_30d,
  SUM(CASE WHEN payment_date <= '2026-08-26' AND appeal_value IS NOT NULL AND appeal_date - payment_date <= 30 THEN appeal_value ELSE 0 END) AS rec_30d_pos_pgto
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice'
  AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
  AND institution_type ILIKE '%Laboratorio%'
  AND disallowance_date >= '2026-03-01'
  AND disallowance_value > 0
GROUP BY 1, 2
ORDER BY 1, 2
