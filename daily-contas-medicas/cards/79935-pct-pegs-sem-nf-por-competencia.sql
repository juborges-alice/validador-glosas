-- Contas Médicas - % PEGs faturadas sem NF por competência (régua de 30%)
-- Card Metabase 79935 · collection 3609 · fonte do farol do KPI "Contas Médicas - % PEGs sem NF"
--
-- RÉGUA VIGENTE: decisão da OM (Juliana Borges) de 06/11/2026, Data de efeito 06/11/2026.
-- https://app.notion.com/p/410f0f13146a811d9267f3d0e093672f
--
-- Duas mudanças sobre a régua de 27/10:
--   1. O limiar passa a ser > 30% (antes 29%).
--   2. Entra um PISO DE MATURAÇÃO: só conta a PEG em status faturada que JÁ FOI ANALISADA
--      há pelo menos 2 dias úteis. PEG analisada há menos que isso fica fora do numerador
--      E do denominador — o prazo dela de vincular a NF ainda não começou a correr.
--
-- POR QUE O PISO. Entre a analista fechar a conta e a NF ser gerada e vinculada passa pelo
-- menos um dia útil. Sem piso, um dia de análise em volume alto joga todas aquelas PEGs no
-- denominador e o indicador estoura por construção no dia seguinte a qualquer lote. Palavras
-- da OM: "se ontem elas analisaram um volume muito grande de contas, hoje esse indicador
-- sempre iria estourar, sendo que na verdade hoje realmente é o prazo para que elas vinculem
-- a nota fiscal do que foi analisado ontem".
--
-- POR QUE 2 DU E NÃO 1: medido em 06/11/2026, com piso de 1 du Nov/26 daria os MESMOS 66,88%,
-- porque as 142 PEGs do lote tinham exatamente 1 du desde a análise e continuavam entrando.
--
-- ÂNCORA DO PISO: administrative_analysis_date, com COALESCE para invoice_billed_step_date
-- quando nula. As duas coincidem na esmagadora maioria das PEGs (156 de 157 em Nov/26,
-- 2.166 de 2.338 em Out/26), mas a da análise descreve o relógio real do processo.
--
-- AGREGAÇÃO DA ÂNCORA: MAX(administrative_analysis_date). A PEG só é madura quando a análise
-- INTEIRA tem 2 du, ou seja, pelo último item analisado. É o corte mais estrito dos dois
-- possíveis; trocar para MIN afrouxa o piso. Decisão de implementação, reversível pela OM.
--
-- pegs_sem_ancora existe para que nenhuma PEG suma em silêncio: é a PEG sem data de análise
-- E sem data de faturamento. Ela fica fora do numerador e do denominador, mas aparece contada.
--
-- O DENOMINADOR DO FAROL É pegs_maduras, NUNCA pegs_faturadas. Calcular sobre pegs_faturadas
-- reproduz exatamente o falso positivo que o piso existe para eliminar.
--
-- ⚪ SEM BASE ELEGÍVEL: quando pegs_maduras = 0, pct_sem_nf vem NULA e o KPI sai ⚪, sem farol
-- — não 🟢. É a janela dos primeiros dias úteis do mês.
--
-- Janela: ano corrente. Fora dela o número é artefato de base (invoice_number só passa a ser
-- preenchido de fato em Mar/2025). Se a janela for ampliada, o piso é 01/03/2025, nunca antes.
-- Grão: a PEG. Entra se QUALQUER item estiver em '4-Faturada'; tem NF se QUALQUER item tiver
-- invoice_number preenchido.
-- Filtros herdados e preservados: provider_class 'Health Institution', typing_location '0002',
-- fee_type <> 'captation', payment_value diferente de zero, exclusão dos 13 institution_code
-- internos e das 2 PEGs excluídas na mão.
--
-- Farol: a linha do MÊS CORRENTE. Competências fechadas saem como contexto e como fila de
-- cobrança, e não acendem farol de novo.
--
-- Drill item a item: card 79936.
WITH du AS (
  SELECT date_actual, SUM(CASE WHEN weekend_indr=FALSE AND is_holiday=FALSE THEN 1 ELSE 0 END)
    OVER (ORDER BY date_actual ROWS UNBOUNDED PRECEDING) AS idx
  FROM curated.dim_date_public WHERE date_actual >= '2024-01-01'
), peg AS (
  SELECT peg_code, MIN(invoice_date) AS invoice_date, MIN(institution_code) AS institution_code,
         MIN(invoice_billed_step_date)::date AS billed_date,
         MAX(administrative_analysis_date)::date AS analysis_date,
         SUM(payment_value) AS peg_total_value,
         MAX(CASE WHEN invoice_step='4-Faturada' THEN 1 ELSE 0 END) AS tem_faturada,
         MAX(CASE WHEN payment_value<>0 THEN 1 ELSE 0 END) AS tem_pagamento,
         MAX(CASE WHEN invoice_number IS NOT NULL AND TRIM(invoice_number)<>'' THEN 1 ELSE 0 END) AS tem_nf
  FROM curated.totvs_procedure_invoice
  WHERE provider_class='Health Institution' AND typing_location='0002' AND fee_type<>'captation'
  GROUP BY peg_code
), f AS (
  SELECT p.*,
         COALESCE(p.analysis_date, p.billed_date) AS ancora_piso,
         dh.idx - db.idx AS du_desde_faturamento,
         dh.idx - da.idx AS du_desde_analise
  FROM peg p
  LEFT JOIN du db ON db.date_actual = p.billed_date
  LEFT JOIN du da ON da.date_actual = COALESCE(p.analysis_date, p.billed_date)
  LEFT JOIN du dh ON dh.date_actual = CURRENT_DATE
  WHERE p.tem_pagamento=1 AND p.tem_faturada=1
    AND p.institution_code NOT IN ('000446','000819','000823','000822','000813','001216','000814','000816','000815','000817','000820','000821','000818')
    AND p.peg_code NOT IN ('00064866','00062757')
    AND p.invoice_date >= DATE_TRUNC('year', CURRENT_DATE)
)
SELECT TO_CHAR(DATE_TRUNC('month', invoice_date),'MM/YYYY') AS competencia,
       COUNT(*) AS pegs_faturadas,
       SUM(CASE WHEN du_desde_analise IS NOT NULL AND du_desde_analise < 2 THEN 1 ELSE 0 END) AS pegs_no_piso,
       SUM(CASE WHEN du_desde_analise IS NULL THEN 1 ELSE 0 END) AS pegs_sem_ancora,
       SUM(CASE WHEN du_desde_analise >= 2 THEN 1 ELSE 0 END) AS pegs_maduras,
       SUM(CASE WHEN du_desde_analise >= 2 AND tem_nf=0 THEN 1 ELSE 0 END) AS sem_nf,
       ROUND(SUM(CASE WHEN du_desde_analise >= 2 AND tem_nf=0 THEN 1 ELSE 0 END)::numeric
             / NULLIF(SUM(CASE WHEN du_desde_analise >= 2 THEN 1 ELSE 0 END),0),4) AS pct_sem_nf,
       SUM(CASE WHEN du_desde_analise >= 2 AND tem_nf=0 THEN peg_total_value ELSE 0 END) AS valor_sem_nf,
       SUM(CASE WHEN du_desde_analise BETWEEN 2 AND 5 AND tem_nf=0 THEN 1 ELSE 0 END) AS sem_nf_2a5du,
       SUM(CASE WHEN du_desde_analise > 5 AND tem_nf=0 THEN 1 ELSE 0 END) AS sem_nf_acima_5du,
       CASE WHEN DATE_TRUNC('month', invoice_date) = DATE_TRUNC('month', CURRENT_DATE)
            THEN 'Mes corrente (farol)' ELSE 'Competencia fechada (contexto)' END AS status,
       CASE WHEN SUM(CASE WHEN du_desde_analise >= 2 THEN 1 ELSE 0 END) = 0
            THEN 'SEM BASE ELEGIVEL - nenhuma PEG madura, sai branco e sem farol'
            WHEN ROUND(SUM(CASE WHEN du_desde_analise >= 2 AND tem_nf=0 THEN 1 ELSE 0 END)::numeric
                 / NULLIF(SUM(CASE WHEN du_desde_analise >= 2 THEN 1 ELSE 0 END),0),4) > 0.30
            THEN 'VERMELHO - acima de 30% das maduras sem NF'
            ELSE 'VERDE - dentro de 30%' END AS veredito
FROM f
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY DATE_TRUNC('month', invoice_date) DESC
