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

-- Itens com recurso de glosa protocolado e ainda sem decisão (Autorizado, Autorizado Parcialmente ou Negado)
itens_em_recurso as (
    select
        peg_code,
        appeal_date,
        appeal_value,
        disallowance_value,
        disallowance_reason,
        institution_code,
        institution_name,
        institution_type,
        provider_economic_group,
        guide_type_description,
        guide_number
    from curated.totvs_procedure_invoice
    where invoice_date >= '2024-01-01'
      and appeal_status = 'Protocolado'
      -- Recurso já pago na PEG 00039294 (jan/2025); status da PEG original não foi atualizado no TOTVS
      and peg_code <> '00034545'
),

itens_classificados as (
    select
        *,
        case
            -- Home Doctor, Lar e Saúde e Visclin ficam sempre em Laboratórios e Clínicas
            when institution_code in ('000013', '002788', '001254') then 'Recurso de Glosa - Laboratórios e Clínicas'
            -- Capeante: glosa 7DJ (conta não localizada no capeante) ou 7E0 (valor divergente do capeante),
            -- com as mesmas regras da fila Capeante
            when (coalesce(disallowance_reason, '') like '%7DJ%' or coalesce(disallowance_reason, '') like '%7E0%')
             and coalesce(trim(provider_economic_group), '') not in ('EINSTEIN', 'SANTA JOANA', 'SIRIO')
             and (
                institution_code in ('001262', '001443')  -- Blanc SP e SMA, qualquer tipo de guia
                or (trim(guide_type_description) = 'GUIA DE RESUMO DE INTERNACAO' and institution_code in (
                    '000836', '000837',  -- BP Paulista e Mirante
                    '001142',            -- HNIPO (Beneficência Nipo Brasileira)
                    '001084',            -- HCor
                    '002886', '000973',  -- Leforte Liberdade e Morumbi
                    '000360',            -- Samaritano Higienópolis
                    '000129',            -- Alvorada
                    '001137',            -- InCor
                    '001041',            -- Santa Catarina
                    '001185',            -- Edmundo Vasconcelos
                    '000811',            -- HAOC
                    '000830'             -- Sabará
                ))
             ) then 'Recurso de Glosa - Capeante'
            -- Demais recursos: mesma divisão das filas de análise
            when trim(institution_type) = 'Hospital' then 'Recurso de Glosa - Hospitais'
            else 'Recurso de Glosa - Laboratórios e Clínicas'
        end as fila
    from itens_em_recurso
),

recursos_por_peg as (
    select
        fila,
        peg_code,
        min(appeal_date) as data_recurso,
        trim(max(institution_name)) as prestador,
        trim(max(institution_type)) as tipo_prestador,
        sum(appeal_value) as valor_em_recurso,
        sum(disallowance_value) as valor_glosado,
        count(*) as qtd_itens
    from itens_classificados
    group by 1, 2
),

-- Contas (guias distintas) com itens em recurso, por fila e PEG
guias_em_recurso as (
    select
        fila,
        peg_code,
        guide_number
    from itens_classificados
    group by 1, 2, 3
),

qtd_guias_em_recurso as (
    select
        fila,
        peg_code,
        count(*) as qtd_guias
    from guias_em_recurso
    group by 1, 2
),

feriados_no_periodo as (
    select
        r.fila,
        r.peg_code,
        count(*) as n_feriados
    from recursos_por_peg r
    join feriados f
      on f.holiday_date > r.data_recurso
     and f.holiday_date <= current_date
     and date_part('dow', f.holiday_date) not in (0, 6)
    group by 1, 2
),

dias_uteis as (
    select
        r.*,
        g.qtd_guias,
        (datediff('day', r.data_recurso, current_date)
          - datediff('week', r.data_recurso, current_date) * 2
          - case when date_part('dow', r.data_recurso) = 0 then 1 else 0 end
          - case when date_part('dow', current_date) = 6 then 1 else 0 end
          - coalesce(fp.n_feriados, 0)) as dias_uteis_na_fila
    from recursos_por_peg r
    left join feriados_no_periodo fp
      on r.fila = fp.fila
     and r.peg_code = fp.peg_code
    left join qtd_guias_em_recurso g
      on r.fila = g.fila
     and r.peg_code = g.peg_code
),

final as (
    select
        fila,
        case
            when dias_uteis_na_fila >= 7 then '1. Vence hoje ou vencido (7+ du)'
            when dias_uteis_na_fila >= 4 then '2. Atenção (4 a 6 du)'
            else '3. No prazo (0 a 3 du)'
        end as faixa_sla,
        peg_code as peg,
        prestador,
        tipo_prestador,
        valor_em_recurso,
        valor_glosado,
        qtd_guias,
        qtd_itens,
        data_recurso,
        dias_uteis_na_fila,
        7 - dias_uteis_na_fila as dias_uteis_para_vencer
    from dias_uteis
)

select
    faixa_sla,
    peg,
    prestador,
    tipo_prestador,
    valor_em_recurso,
    valor_glosado,
    qtd_guias,
    qtd_itens,
    data_recurso,
    dias_uteis_na_fila,
    dias_uteis_para_vencer
from final
where fila = 'Recurso de Glosa - Hospitais'
order by dias_uteis_na_fila desc, data_recurso, prestador, peg