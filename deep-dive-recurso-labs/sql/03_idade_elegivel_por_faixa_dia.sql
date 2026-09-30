WITH lab AS (
  SELECT
    CASE WHEN provider_economic_group IN ('DASA', 'FLEURY', 'FEMME') THEN provider_economic_group ELSE 'OUTROS' END AS grupo,
    DATE_TRUNC('month', disallowance_date)::date AS mes_glosa,
    CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 1 ELSE 0 END AS alvo,
    disallowance_date,
    disallowance_value,
    CASE WHEN provider_economic_group = 'DASA' AND appeal_date >= '2026-09-22' THEN NULL ELSE appeal_date END AS rec_date,
    CASE WHEN provider_economic_group = 'DASA' AND appeal_date >= '2026-09-22' THEN NULL ELSE appeal_value END AS rec_value
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
  CASE WHEN EXTRACT(day FROM disallowance_date) <= 10 THEN 'd01-10'
       WHEN EXTRACT(day FROM disallowance_date) <= 20 THEN 'd11-20'
       ELSE 'd21-31' END AS faixa_dia,
  SUM(disallowance_value) AS glosado,
  SUM(CASE WHEN disallowance_date <= '2026-08-16' THEN disallowance_value ELSE 0 END) AS glos_eleg40,
  SUM(CASE WHEN disallowance_date <= '2026-08-16' AND rec_value IS NOT NULL AND rec_date - disallowance_date <= 40 THEN rec_value ELSE 0 END) AS rec40,
  SUM(CASE WHEN disallowance_date <= '2026-08-06' THEN disallowance_value ELSE 0 END) AS glos_eleg50,
  SUM(CASE WHEN disallowance_date <= '2026-08-06' AND rec_value IS NOT NULL AND rec_date - disallowance_date <= 50 THEN rec_value ELSE 0 END) AS rec50,
  SUM(CASE WHEN disallowance_date <= '2026-07-27' THEN disallowance_value ELSE 0 END) AS glos_eleg60,
  SUM(CASE WHEN disallowance_date <= '2026-07-27' AND rec_value IS NOT NULL AND rec_date - disallowance_date <= 60 THEN rec_value ELSE 0 END) AS rec60
FROM lab
GROUP BY 1, 2, 3, 4
