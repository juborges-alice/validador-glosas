WITH rg AS (
  SELECT
    COALESCE(provider_economic_group, 'SEM GRUPO') AS grupo,
    DATE_TRUNC('month', invoice_date)::date AS mes_rg,
    guide_number,
    LEFT(TRIM(original_guide_number), 24) AS orig_key,
    procedure_code,
    presented_value,
    disallowance_value,
    payment_value
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice'
    AND provider_class = 'Health Institution'
    AND institution_type ILIKE '%Laboratorio%'
    AND TRIM(guide_type_description) = 'GUIA DE RECURSO DE GLOSA'
    AND invoice_date >= '2026-03-01'
),
orig AS (
  SELECT
    TRIM(guide_reference_key) AS gkey,
    procedure_code,
    MAX(disallowance_date) AS glosa_dt,
    MAX(LEFT(TRIM(disallowance_reason), 3)) AS cod,
    SUM(disallowance_value) AS glosado,
    MAX(appeal_date) AS appeal_dt,
    SUM(appeal_value) AS appeal_vlr
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice'
    AND institution_type ILIKE '%Laboratorio%'
    AND TRIM(guide_type_description) <> 'GUIA DE RECURSO DE GLOSA'
    AND invoice_date >= '2025-10-01'
  GROUP BY 1, 2
)
SELECT
  rg.grupo,
  rg.mes_rg,
  COUNT(*) AS itens_rg,
  COUNT(DISTINCT rg.guide_number) AS guias_rg,
  SUM(rg.presented_value) AS apresentado_rg,
  SUM(rg.payment_value) AS pago_rg,
  SUM(rg.disallowance_value) AS glosado_rg,
  SUM(CASE WHEN o.gkey IS NOT NULL THEN 1 ELSE 0 END) AS itens_ligados,
  SUM(CASE WHEN o.glosado > 0 THEN 1 ELSE 0 END) AS itens_orig_glosados,
  SUM(CASE WHEN o.appeal_dt IS NOT NULL THEN 1 ELSE 0 END) AS itens_orig_com_appeal,
  SUM(CASE WHEN o.glosado > 0 AND o.appeal_dt IS NULL THEN rg.presented_value ELSE 0 END) AS vlr_sem_appeal,
  SUM(CASE WHEN o.cod = '7DL' THEN 1 ELSE 0 END) AS it_7dl,
  SUM(CASE WHEN o.cod = '7F8' THEN 1 ELSE 0 END) AS it_7f8,
  SUM(CASE WHEN o.cod = '7EY' THEN 1 ELSE 0 END) AS it_7ey,
  SUM(CASE WHEN o.cod = '7F6' THEN 1 ELSE 0 END) AS it_7f6,
  SUM(CASE WHEN o.cod = '7EK' THEN 1 ELSE 0 END) AS it_7ek,
  SUM(CASE WHEN o.cod = '7G4' THEN 1 ELSE 0 END) AS it_7g4,
  MIN(o.glosa_dt) AS glosa_min,
  MAX(o.glosa_dt) AS glosa_max
FROM rg
LEFT JOIN orig o ON o.gkey = rg.orig_key AND o.procedure_code = rg.procedure_code
GROUP BY 1, 2
ORDER BY 1, 2
