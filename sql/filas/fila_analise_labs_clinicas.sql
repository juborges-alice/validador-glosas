with feriados as (
    select date '2025-01-01' as holiday_date union all
    select date '2025-01-25' union all
    select date '2025-03-03' union all
    select date '2025-03-04' union all
    select date '2025-04-18' union all
    select date '2025-04-21' union all
    select date '2025-05-01' union all
    select date '2025-06-19' union all
    select date '2025-07-09' union all
    select date '2025-09-07' union all
    select date '2025-10-12' union all
    select date '2025-11-02' union all
    select date '2025-11-15' union all
    select date '2025-11-20' union all
    select date '2025-12-25' union all
    select date '2026-01-01' union all
    select date '2026-01-25' union all
    select date '2026-02-17' union all
    select date '2026-04-03' union all
    select date '2026-04-21' union all
    select date '2026-05-01' union all
    select date '2026-06-04' union all
    select date '2026-07-09' union all
    select date '2026-09-07' union all
    select date '2026-10-12' union all
    select date '2026-11-02' union all
    select date '2026-11-15' union all
    select date '2026-11-20' union all
    select date '2026-12-25' union all
    select date '2027-01-01' union all
    select date '2027-01-25' union all
    select date '2027-02-09' union all
    select date '2027-03-26' union all
    select date '2027-04-21' union all
    select date '2027-05-01' union all
    select date '2027-05-27' union all
    select date '2027-07-09' union all
    select date '2027-09-07' union all
    select date '2027-10-12' union all
    select date '2027-11-02' union all
    select date '2027-11-15' union all
    select date '2027-11-20' union all
    select date '2027-12-25'
),

procedimentos as (
    select
        peg_code,
        invoice_date,
        invoice_step,
        invoice_ready_step_date,
        invoice_billed_step_date,
        disallowance_date,
        institution_code,
        institution_name,
        institution_type,
        provider_class,
        provider_economic_group,
        guide_type_description,
        presented_value
    from curated.totvs_procedure_invoice
    where invoice_date >= dateadd('month', -6, current_date)
),

pegs as (
    select
        peg_code,
        max(invoice_date) as invoice_date,
        max(invoice_step) as invoice_step,
        max(invoice_ready_step_date) as invoice_ready_step_date,
        max(invoice_billed_step_date) as invoice_billed_step_date,
        max(disallowance_date) as disallowance_date,
        max(institution_code) as institution_code,
        trim(max(institution_name)) as institution_name,
        trim(max(institution_type)) as institution_type,
        max(provider_class) as provider_class,
        trim(max(provider_economic_group)) as provider_economic_group,
        trim(max(guide_type_description)) as guide_type_description,
        -- 1 só quando todas as guias da PEG são de resumo de internação (PEG mista fica em Hospitais)
        min(
            case
                when trim(guide_type_description) = 'GUIA DE RESUMO DE INTERNACAO' then 1
                else 0
            end
        ) as so_resumo_internacao,
        sum(presented_value) as peg_total_presented_value,
        count(*) as n_procedures
    from procedimentos
    group by peg_code
),

-- Fila: PEGs em conferência ou prontas, ainda sem faturamento nem glosa, com os mesmos recortes do card de SLA
pegs_em_aberto as (
    select
        *,
        case
            -- Home care e oftalmologia: Home Doctor, Lar e Saúde e Visclin vão para Laboratórios e Clínicas
            when institution_code in ('000013', '002788', '001254') then 'Análise de Laboratórios e Clínicas'
            -- Capeante: Einstein, Santa Joana e Sírio nunca entram
            when provider_economic_group in ('EINSTEIN', 'SANTA JOANA', 'SIRIO') then
                case when institution_type = 'Hospital' then 'Análise de Hospitais' else 'Análise de Laboratórios e Clínicas' end
            -- Capeante: Blanc SP e SMA, qualquer tipo de guia
            when institution_code in ('001262', '001443') then 'Análise Capeante'
            -- Capeante: PEGs só com guias de resumo de internação destes hospitais
            when so_resumo_internacao = 1 and institution_code in (
                '000836', '000837',  -- BP Paulista e Mirante
                '001142',            -- HNIPO (Beneficência Nipo Brasileira)
                '001084',            -- HCor (Cidade Jardim 001169 fica em Hospitais: só SP/SADT)
                '002886', '000973',  -- Leforte Liberdade e Morumbi
                '000360',            -- Samaritano Higienópolis
                '000129',            -- Alvorada
                '001137',            -- InCor
                '001041',            -- Santa Catarina
                '001185',            -- Edmundo Vasconcelos
                '000811',            -- HAOC
                '000830',            -- Sabará
                '001618',            -- Hospital Paulista
                '001533', '001530', '001497'  -- São Camilo Ipiranga, Pompeia e Santana
            ) then 'Análise Capeante'
            when institution_type = 'Hospital' then 'Análise de Hospitais'
            else 'Análise de Laboratórios e Clínicas'
        end as fila
    from pegs
    where invoice_step in ('2-Conferencia', '3-Pronta')
      and invoice_billed_step_date is null
      and disallowance_date is null
      and provider_class = 'Health Institution'
      and institution_type in ('Hospital', 'Laboratorio', 'Clinica', 'Centro De Diagnosticos')
      and lower(institution_name) not like '%alice%'
      and peg_total_presented_value is not null
      and peg_total_presented_value <> 0
      and guide_type_description <> 'GUIA DE RECURSO DE GLOSA'
),

feriados_no_periodo as (
    select
        p.peg_code,
        count(*) as n_feriados
    from pegs_em_aberto p
    join feriados f
      on f.holiday_date > p.invoice_date
     and f.holiday_date <= current_date
     and date_part('dow', f.holiday_date) not in (0, 6)
    group by p.peg_code
),

dias_uteis as (
    select
        p.*,
        (datediff('day', p.invoice_date, current_date)
          - datediff('week', p.invoice_date, current_date) * 2
          - case when date_part('dow', p.invoice_date) = 0 then 1 else 0 end
          - case when date_part('dow', current_date) = 6 then 1 else 0 end
          - coalesce(fp.n_feriados, 0)) as dias_uteis_na_fila
    from pegs_em_aberto p
    left join feriados_no_periodo fp
      on p.peg_code = fp.peg_code
),

final as (
    select
        fila,
        case
            when dias_uteis_na_fila >= 7 then '1. Vence hoje ou vencido (7+ du)'
            when dias_uteis_na_fila >= 4 then '2. Atenção (4 a 6 du)'
            else '3. No prazo (0 a 3 du)'
        end as faixa_sla,
        institution_name as prestador,
        institution_type as tipo_prestador,
        peg_code as peg,
        invoice_date as data_recebimento,
        dias_uteis_na_fila,
        7 - dias_uteis_na_fila as dias_uteis_para_vencer,
        peg_total_presented_value as valor_apresentado,
        n_procedures as qtd_procedimentos
    from dias_uteis
)

select
    faixa_sla,
    prestador,
    tipo_prestador,
    peg,
    data_recebimento,
    dias_uteis_na_fila,
    dias_uteis_para_vencer,
    valor_apresentado,
    qtd_procedimentos
from final
where fila = 'Análise de Laboratórios e Clínicas'
order by dias_uteis_na_fila desc, data_recebimento, prestador, peg