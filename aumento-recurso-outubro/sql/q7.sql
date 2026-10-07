SELECT DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  LEFT(TRIM(disallowance_reason), 3) AS cod,
  COUNT(*) AS itens_glosados,
  SUM(disallowance_value) AS glosado,
  SUM(CASE WHEN appeal_value IS NOT NULL AND NOT (appeal_date >= '2026-09-22' AND disallowance_date < '2026-01-01') THEN appeal_value ELSE 0 END) AS recursado,
  SUM(CASE WHEN appeal_value IS NOT NULL AND appeal_date - disallowance_date <= 60 THEN appeal_value ELSE 0 END) AS rec60
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND disallowance_value > 0 AND disallowance_date >= '2026-04-01'
  AND provider_economic_group = 'DASA'
GROUP BY 1,2 ORDER BY 1, glosado DESC
