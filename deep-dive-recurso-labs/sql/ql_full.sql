SELECT
  CASE WHEN provider_economic_group IN ('DASA', 'FLEURY', 'FEMME') THEN provider_economic_group ELSE 'OUTROS' END AS grupo,
  DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
  COUNT(*) AS itens_glosados,
  SUM(CASE WHEN TRIM(paid) = 'Sim' THEN 1 ELSE 0 END) AS itens_pagos,
  SUM(CASE WHEN payment_date IS NOT NULL THEN 1 ELSE 0 END) AS itens_com_data_pgto,
  MIN(payment_date) AS pgto_min,
  MAX(payment_date) AS pgto_max,
  AVG((payment_date - disallowance_date)::float) AS dias_glosa_ate_pgto,
  AVG(CASE WHEN appeal_date IS NOT NULL AND payment_date IS NOT NULL THEN (appeal_date - payment_date)::float END) AS dias_pgto_ate_recurso,
  MIN(invoice_due_date) AS venc_min,
  MAX(invoice_due_date) AS venc_max,
  MAX(batch_date) AS lote_pls_max,
  SUM(CASE WHEN batch_date IS NOT NULL THEN 1 ELSE 0 END) AS itens_com_lote_pls
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice'
  AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
  AND institution_type ILIKE '%Laboratorio%'
  AND disallowance_date >= '2026-03-01'
  AND disallowance_value > 0
GROUP BY 1, 2
ORDER BY 1, 2
