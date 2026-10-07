WITH dup AS (
  SELECT invoice_guide_item_key AS k, person_id AS pid, procedure_code AS proc, execution_date::date AS dt,
    disallowance_value AS g, appeal_status, appeal_value, accepted_value, executed_quantity AS q,
    COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
    AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
    AND disallowance_value > 0 AND disallowance_reason LIKE '%7G4 -%'
    AND disallowance_date >= '2026-07-01' AND disallowance_date < '2026-10-01'
), oth AS (
  SELECT d.k, MIN(ABS(o.execution_date::date - d.dt)) AS dmin
  FROM dup d JOIN curated.totvs_procedure_invoice o
    ON o.person_id = d.pid AND o.procedure_code = d.proc AND o.invoice_guide_item_key <> d.k
   AND o.system_source = 'totvs-alice' AND o.execution_date BETWEEN DATEADD(day,-120,d.dt) AND DATEADD(day,120,d.dt)
  GROUP BY 1
)
SELECT CASE WHEN o.dmin IS NULL THEN 'sem outro item' WHEN o.dmin = 0 THEN '0 mesmo dia' WHEN o.dmin <= 7 THEN '1-7' WHEN o.dmin <= 30 THEN '8-30' WHEN o.dmin <= 90 THEN '31-90' ELSE '91-120' END AS faixa,
  COUNT(*) AS itens, SUM(d.g) AS glosado,
  SUM(CASE WHEN d.pid IS NULL THEN 1 ELSE 0 END) AS sem_pid,
  SUM(CASE WHEN d.appeal_value IS NOT NULL THEN 1 ELSE 0 END) AS recursados,
  SUM(CASE WHEN d.appeal_status IN ('Autorizado','Autorizado Parcialmente') THEN 1 ELSE 0 END) AS acatados,
  SUM(CASE WHEN d.appeal_status IN ('Autorizado','Autorizado Parcialmente') THEN d.accepted_value END) AS accepted_value,
  SUM(CASE WHEN d.appeal_status IN ('Autorizado','Autorizado Parcialmente') THEN d.appeal_value END) AS appeal_value_acat,
  AVG(d.q) AS q_media, MAX(d.q) AS q_max
FROM dup d LEFT JOIN oth o ON o.k = d.k
GROUP BY 1 ORDER BY 1
