WITH base AS (
  SELECT
    invoice_guide_item_key,
    guide_number,
    COALESCE(provider_economic_group, 'SEM GRUPO') AS grupo,
    disallowance_date,
    TRIM(disallowance_reason) AS motivo,
    disallowance_value,
    appeal_date,
    appeal_value,
    appeal_status,
    CASE WHEN TRIM(appeal_operator_reason) LIKE 'EI%' THEN 'EI'
         WHEN TRIM(appeal_operator_reason) LIKE 'EE%' THEN 'EE'
         ELSE 'Outro' END AS tipo_erro,
    CASE WHEN disallowance_reason LIKE '%7DL -%' OR disallowance_reason LIKE '%7F8 -%' THEN 1 ELSE 0 END AS motivo_alvo,
    CASE
      WHEN disallowance_reason LIKE '%7F6 -%' AND appeal_date >= '2026-07-01' AND appeal_date < '2026-09-01' THEN 1
      WHEN provider_economic_group = 'DASA' AND appeal_date >= '2026-09-22' AND appeal_date < '2026-10-01' THEN 1
      ELSE 0
    END AS excluido
  FROM curated.totvs_procedure_invoice
  WHERE system_source = 'totvs-alice'
    AND provider_class = 'Health Institution'
    AND invoice_step IN ('1-Digitacao', '2-Conferencia', '3-Pronta', '4-Faturada')
    [[AND {{tipo_inst}}]]
    [[AND {{grupo}}]]
)
, ref AS (
  SELECT DATE_TRUNC('month', MAX(appeal_date))::date AS mes_atual FROM base WHERE appeal_value IS NOT NULL
),
diario AS (
  SELECT
    DATE_TRUNC('month', appeal_date)::date AS mes,
    EXTRACT(day FROM appeal_date)::int AS dia,
    COUNT(DISTINCT invoice_guide_item_key) AS itens
  FROM base
  WHERE appeal_value IS NOT NULL
    AND excluido = 0
    AND appeal_date >= DATEADD(month, -3, (SELECT mes_atual FROM ref))
  GROUP BY 1, 2
),
dias AS (
  SELECT ROW_NUMBER() OVER (ORDER BY invoice_guide_item_key) AS dia FROM base LIMIT 31
),
meses AS (
  SELECT DISTINCT mes FROM diario
),
grade AS (
  SELECT m.mes, d.dia, COALESCE(x.itens, 0) AS itens
  FROM meses m CROSS JOIN dias d
  LEFT JOIN diario x ON x.mes = m.mes AND x.dia = d.dia
),
acum AS (
  SELECT mes, dia, SUM(itens) OVER (PARTITION BY mes ORDER BY dia ROWS UNBOUNDED PRECEDING) AS itens_acum
  FROM grade
)
SELECT
  dia AS dia_do_mes,
  MAX(CASE WHEN mes = (SELECT mes_atual FROM ref) THEN itens_acum END) AS mes_atual,
  ROUND(AVG(CASE WHEN mes < (SELECT mes_atual FROM ref) THEN itens_acum END)) AS media_3_meses_anteriores
FROM acum
GROUP BY 1
ORDER BY 1
