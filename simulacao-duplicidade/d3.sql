WITH dup AS (
  SELECT invoice_guide_item_key AS k, person_id AS pid, procedure_code AS proc, MAX(TRIM(procedure_name)) AS proc_name, MAX(LEFT(TRIM(disallowance_reason),3)) AS cod,
    execution_date::date AS dt, disallowance_date::date AS dg,
    COALESCE(provider_economic_group, TRIM(institution_name)) AS grupo,
    SUM(disallowance_value) AS g, SUM(presented_value) AS apres, MAX(executed_quantity) AS q,
    MAX(appeal_status) AS st, SUM(appeal_value) AS rec, SUM(accepted_value) AS acc, MAX(appeal_date)::date AS dr
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice' AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
    AND (institution_type ILIKE '%Clinica%' OR institution_type ILIKE '%Laboratorio%')
    AND disallowance_value > 0 AND (disallowance_reason LIKE '%7G4 -%' OR disallowance_reason LIKE '%7DX -%' OR disallowance_reason LIKE '%7DY -%' OR disallowance_reason LIKE '%7EE -%')
    AND disallowance_date >= '2026-05-01' AND disallowance_date < '2026-08-01'
  GROUP BY 1,2,3,6,7,8
), n AS (
  SELECT d.k, SUM(o.executed_quantity) AS n_dia, COUNT(DISTINCT o.invoice_guide_item_key) AS itens_dia
  FROM dup d JOIN curated.totvs_procedure_invoice o
    ON o.person_id = d.pid AND o.procedure_code = d.proc AND o.execution_date::date = d.dt
   AND o.system_source = 'totvs-alice' AND o.invoice_step IN ('1-Digitacao','2-Conferencia','3-Pronta','4-Faturada')
  GROUP BY 1
)
SELECT d.*, n.n_dia, n.itens_dia FROM dup d LEFT JOIN n ON n.k = d.k
