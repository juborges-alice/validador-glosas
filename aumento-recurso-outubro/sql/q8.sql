SELECT COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
  DATE_TRUNC('month', appeal_date)::date AS mes_rec,
  COUNT(*) AS itens, SUM(appeal_value) AS vlr, MAX(appeal_value) AS maior
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
  AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  AND appeal_value IS NOT NULL AND appeal_date >= '2026-03-01'
  AND COALESCE(provider_economic_group, TRIM(institution_name)) IN ('DASA','FLEURY','FEMME','HCOR','EINSTEIN','CIP PACAEMBU FLEURY','AMERICAS','SANTA MARCELINA','SAHA','SIRIO','BP','HOSPITAL SÃO FRANCISCO','SMA - SERVIÇO MÉDICO ANESTESIA','GSH CORP PARTICIPACOES S.A.')
GROUP BY 1,2 ORDER BY 1,2
