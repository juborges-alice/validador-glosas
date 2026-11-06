-- Contas Médicas - % PEGs faturadas sem NF por competência (régua de 30% + piso de 2 du pós-análise)
-- Card 79935 · collection 3609 · sem parâmetros
--
-- ALTERAÇÃO DE 06/11/2026 (decisão da OM, Juliana Borges). Duas mudanças sobre a régua de 27/10:
--
-- 1. O LIMIAR PASSA A SER > 30%. O título do card já dizia "régua de 30%" desde 27/10, mas o SQL
--    cortava em 0.29 e o catálogo descrevia 29% — divergência corrigida aqui. Agora é 0.30 nos dois.
--
-- 2. PISO DE MATURAÇÃO DE 2 DIAS ÚTEIS APÓS A ANÁLISE. Entre a analista fechar a conta e a NF ser
--    gerada e vinculada passa pelo menos um dia útil. Sem piso, um dia de análise em volume alto
--    joga todas aquelas PEGs no denominador SEM que o prazo de vincular a NF tenha sequer começado
--    a correr — e o indicador estoura por construção no dia seguinte a qualquer lote.
--    Palavras da OM: "se ontem elas analisaram um volume muito grande de contas, hoje esse
--    indicador sempre iria estourar, sendo que na verdade hoje realmente é o prazo para que elas
--    vinculem a nota fiscal do que foi analisado ontem".
--
--    Logo, a população do farol passa a ser: PEG em status 4-Faturada E analisada há >= 2 dias
--    úteis. PEG analisada há menos que isso sai do numerador E do denominador — ela não está
--    atrasada, está dentro do prazo normal.
--
-- POR QUE 2 DU E NÃO 1. Medido em 06/11/2026: com piso de 1 du, Nov/26 dava os mesmos 66,88% da
-- régua sem piso, porque as 142 PEGs do lote do dia anterior têm exatamente 1 du desde a análise e
-- continuavam entrando. Com piso de 2 du, Nov/26 cai para 33,33% (5 de 15 maduras) e as 142 saem.
-- O piso de 1 du não filtra nada no caso que motivou a mudança.
--
-- ÂNCORA: administrative_analysis_date ("Data em que a análise administrativa foi realizada").
-- Medido em 06/11/2026, ela coincide com invoice_billed_step_date na esmagadora maioria das PEGs
-- (156 de 157 em Nov/26; 2.166 de 2.338 em Out/26) — é a própria conclusão da análise que avança a
-- PEG para a fase 4. Quando vem nula (1 PEG em Nov/26, 11 em Out/26), cai para invoice_billed_step_date
-- via COALESCE, em vez de a PEG sumir silenciosamente da população.
--
-- ⚪ SEM BASE ELEGÍVEL. Quando pegs_maduras = 0, pct_sem_nf vem NULL e o KPI sai ⚪, sem farol —
-- não 🟢. É a janela dos primeiros dias úteis do mês. A coluna pegs_no_piso diz quantas estão
-- esperando o piso.
--
-- Drill item a item: card 79936.

WITH du AS (
  SELECT date_actual, SUM(CASE WHEN weekend_indr=FALSE AND is_holiday=FALSE THEN 1 ELSE 0 END)
    OVER (ORDER BY date_actual ROWS UNBOUNDED PRECEDING) AS idx
  FROM curated.dim_date_public WHERE date_actual >= '2024-01-01'
), peg AS (
  SELECT peg_code, MIN(invoice_date) AS invoice_date, MIN(institution_code) AS institution_code,
         MIN(invoice_billed_step_date)::date AS billed_date,
         COALESCE(MAX(administrative_analysis_date)::date, MIN(invoice_billed_step_date)::date) AS analise_date,
         SUM(payment_value) AS peg_total_value,
         MAX(CASE WHEN invoice_step='4-Faturada' THEN 1 ELSE 0 END) AS tem_faturada,
         MAX(CASE WHEN payment_value<>0 THEN 1 ELSE 0 END) AS tem_pagamento,
         MAX(CASE WHEN invoice_number IS NOT NULL AND TRIM(invoice_number)<>'' THEN 1 ELSE 0 END) AS tem_nf
  FROM curated.totvs_procedure_invoice
  WHERE provider_class='Health Institution' AND typing_location='0002' AND fee_type<>'captation'
  GROUP BY peg_code
), f AS (
  SELECT p.*, dh.idx - da.idx AS du_desde_analise
  FROM peg p LEFT JOIN du da ON da.date_actual=p.analise_date LEFT JOIN du dh ON dh.date_actual=CURRENT_DATE
  WHERE p.tem_pagamento=1 AND p.tem_faturada=1
    AND p.institution_code NOT IN ('000446','000819','000823','000822','000813','001216','000814','000816','000815','000817','000820','000821','000818')
    AND p.peg_code NOT IN ('00064866','00062757')
    AND p.invoice_date >= DATE_TRUNC('year', CURRENT_DATE)
)
SELECT TO_CHAR(DATE_TRUNC('month', invoice_date),'MM/YYYY') AS competencia,
       COUNT(*) AS pegs_faturadas,
       SUM(CASE WHEN du_desde_analise < 2 THEN 1 ELSE 0 END) AS pegs_no_piso,
       SUM(CASE WHEN du_desde_analise >= 2 THEN 1 ELSE 0 END) AS pegs_maduras,
       SUM(CASE WHEN du_desde_analise >= 2 THEN 1-tem_nf ELSE 0 END) AS sem_nf,
       ROUND(SUM(CASE WHEN du_desde_analise >= 2 THEN 1-tem_nf ELSE 0 END)::numeric
             / NULLIF(SUM(CASE WHEN du_desde_analise >= 2 THEN 1 ELSE 0 END),0), 4) AS pct_sem_nf,
       SUM(CASE WHEN du_desde_analise >= 2 AND tem_nf=0 THEN peg_total_value ELSE 0 END) AS valor_sem_nf,
       SUM(CASE WHEN du_desde_analise BETWEEN 2 AND 5 AND tem_nf=0 THEN 1 ELSE 0 END) AS sem_nf_2a5du,
       SUM(CASE WHEN du_desde_analise > 5 AND tem_nf=0 THEN 1 ELSE 0 END) AS sem_nf_acima_5du,
       CASE WHEN DATE_TRUNC('month', invoice_date) = DATE_TRUNC('month', CURRENT_DATE)
            THEN 'Mes corrente (farol)' ELSE 'Competencia fechada (contexto)' END AS status,
       CASE WHEN SUM(CASE WHEN du_desde_analise >= 2 THEN 1 ELSE 0 END) = 0
              THEN 'SEM BASE ELEGIVEL - nenhuma PEG analisada ha 2+ du'
            WHEN ROUND(SUM(CASE WHEN du_desde_analise >= 2 THEN 1-tem_nf ELSE 0 END)::numeric
                 / NULLIF(SUM(CASE WHEN du_desde_analise >= 2 THEN 1 ELSE 0 END),0), 4) > 0.30
              THEN 'VERMELHO - acima de 30% das maduras sem NF'
            ELSE 'VERDE - dentro de 30%' END AS veredito
FROM f
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY DATE_TRUNC('month', invoice_date) DESC
