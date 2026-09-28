-- Fila de trabalho: análise de recurso de glosa
-- Fonte: curated.totvs_procedure_invoice (1 linha por item de guia)
-- Traz, item a item, tudo que foi recursado e ainda não teve análise concluída
-- (appeal_status 'Protocolado' ou 'Em Analise').
-- Hospital segue outra regra e fica fora da fila (escopo: Labs e Clínicas).
-- A coluna "O que vc precisa verificar?" aplica a regra de cada motivo de glosa
-- conforme o "Fluxograma ouro — Análise de recurso de glosa".

with base as (
    select
        t.*,
        trim(t.institution_type) as tipo_prestador,
        left(trim(t.disallowance_reason), 3) as motivo_codigo_original
    from curated.totvs_procedure_invoice t
    where t.appeal_status in ('Protocolado', 'Em Analise')
      and coalesce(trim(t.institution_type), '') <> 'Hospital'
),

motivo as (
    select
        b.*,
        -- códigos que trocaram de nome: sempre usar o vigente
        case b.motivo_codigo_original
            when '7DL' then '7F8'
            when '7DK' then '7F9'
            when '7EI' then '7G9'
            when '7DX' then '7G3'
            when '7DY' then '7G4'
            when '7DS' then '7F7'
            else b.motivo_codigo_original
        end as motivo_codigo
    from base b
),

regra as (
    select
        m.*,
        case
            -- Não passíveis de recurso: nega automático
            when m.motivo_codigo = '7F8' and m.tipo_prestador = 'Clinica' then 'Não passível'
            when m.motivo_codigo = '7EL' and m.appeal_attempt >= 2 then 'Confere o documento'
            when m.motivo_codigo in ('7EZ', '7EL', '7DT', '7F7', '7DM', '526', '7DN', '505', '506') then 'Não passível'
            -- Consulta à base
            when m.motivo_codigo in ('7F8', '7F9', '7EY', '7G9') then 'Consulta à base'
            -- Confere o documento
            when m.motivo_codigo in ('7EK', '7G3', '7G4', '7D4', '7DU', '7F6', '7E3', '0TS', '701', '7ES') then 'Confere o documento'
            -- Escala
            when m.motivo_codigo in ('7E1', '7DR') then 'Escala'
            else 'Sem regra no fluxograma'
        end as grupo_motivo,

        case
            -- Não passíveis de recurso
            when m.motivo_codigo = '7F8' and m.tipo_prestador = 'Clinica'
                then 'NEGAR AUTOMÁTICO. Em clínica a autorização é 100% prévia. Devolutiva: procedimento exige autorização prévia.'
            when m.motivo_codigo = '7EZ'
                then 'NEGAR AUTOMÁTICO. Autorização pedida depois da janela de 72h conta como sem autorização (exceção: Cervicor, parametrizada no CSV).'
            when m.motivo_codigo = '7EL' and m.appeal_attempt >= 2
                then 'TRÉPLICA - ANÁLISE HUMANA. Código cobrado diferente do autorizado: analisar a tréplica do prestador.'
            when m.motivo_codigo = '7EL'
                then 'NEGAR AUTOMÁTICO. Código cobrado diferente do autorizado. Devolutiva: reapresentar com o código autorizado.'
            when m.motivo_codigo = '7DT'
                then 'NEGAR AUTOMÁTICO. Procedimento negociado como captation: item já remunerado dentro do modelo.'
            when m.motivo_codigo = '7F7'
                then 'NEGAR AUTOMÁTICO. Conta apresentada depois dos 90 dias contratuais, contados do evento.'
            when m.motivo_codigo = '7DM'
                then 'NEGAR AUTOMÁTICO. Autorização usada depois dos 180 dias de validade da guia.'
            when m.motivo_codigo = '526'
                then 'NEGAR AUTOMÁTICO. Nenhum valor informado para o Portal. Devolutiva: reapresentar com o valor preenchido; não é possível recursar R$ 0.'
            when m.motivo_codigo = '7DN'
                then 'NEGAR AUTOMÁTICO. Membro inativo na data de execução (Metabase é a fonte da verdade; nega mesmo com autorização prévia). EXCEÇÃO: recém-nascido com menos de 30 dias no plano da mãe ativa -> acatar como EI.'
            when m.motivo_codigo = '505'
                then 'NEGAR AUTOMÁTICO. Família bloqueada (titular e dependentes): impedido de ser atendido, glosa definitiva.'
            when m.motivo_codigo = '506'
                then 'NEGAR AUTOMÁTICO. Usuário bloqueado (só o indivíduo): glosa definitiva. Devolutiva: o restante da família segue ativo.'

            -- Consulta à base (TOTVS e Metabase)
            when m.motivo_codigo = '7F8'
                then 'CONSULTAR BASE. Existe senha ou guia autorizada na base, anterior à execução? Sim: acatar (EE). Não: negar.'
            when m.motivo_codigo = '7F9'
                then 'CONSULTAR BASE. Existe senha válida e autorizada, anterior à execução? Sim: acatar (EI se a base leu a senha errada; EE se o prestador enviou a senha errada no XML e a correta no recurso). Não: negar.'
            when m.motivo_codigo = '7EY'
                then 'CONSULTAR BASE. Existe segunda guia autorizada que cobre, item a item, o que foi glosado? Sim: acatar só os itens cobertos pela nova senha (EI). Sem segunda guia ou item não coberto: negar.'
            when m.motivo_codigo = '7G9'
                then 'CONSULTAR BASE. Laudo ou assinatura da unidade autorizada comprova que a execução ocorreu nela? Sim: acatar (EE). Não: negar e orientar reapresentação com a unidade correta.'

            -- Confere o documento (análise humana dos anexos)
            when m.motivo_codigo = '7EK'
                then 'CONFERIR DOCUMENTO. Chegou evidência de que o evento ocorreu (laudo, pedido assinado com data, prontuário, lista de presença ou carimbo com data e assinatura do membro)? Sim: acatar (EE). Não: negar.'
            when m.motivo_codigo = '7G3'
                then 'CONFERIR DOCUMENTO. Há evidência de que foram dois eventos distintos (repetição entre guias)? Sim: acatar (EE). Se a conta já foi paga em outra parcial ou sem evidência: negar.'
            when m.motivo_codigo = '7G4'
                then 'CONFERIR DOCUMENTO. Há evidência de execuções distintas dentro da mesma guia (repetição como quantidade)? Sim: acatar (EE). Não: negar.'
            when m.motivo_codigo = '7D4'
                then 'CONFERIR DOCUMENTO. RDA não autorizada para o plano: veio e-mail ou planilha de excepcionalidade da Alice e a senha foi confeccionada corretamente? Sim: acatar (EI). Não: negar.'
            when m.motivo_codigo = '7DU'
                then 'CONFERIR DOCUMENTO. Chegou a nota fiscal do item cobrado, dentro do prazo? Sim: acatar (EE). Não: negar.'
            when m.motivo_codigo = '7F6'
                then 'CONFERIR DOCUMENTO. Há comprovação de que o atendimento aconteceu na data cobrada? Sim: acatar (EE). Não: negar.'
            when m.motivo_codigo = '7E3'
                then 'CONFERIR DOCUMENTO. Reexecução excessiva (mesmo pedido, CRM e exame em até 7 dias): vieram dois ou mais pedidos médicos com datas de solicitação distintas? Sim: acatar (EE). Não: negar.'
            when m.motivo_codigo = '0TS'
                then 'CONFERIR DOCUMENTO. SADT conflitantes: o pedido médico traz os dois códigos? Sim: acatar (EE). Não: negar.'
            when m.motivo_codigo = '701'
                then 'CONFERIR DOCUMENTO. Exame incompatível com a idade: veio o pedido médico daquele procedimento para aquele membro? Sim: acatar (EE). Não: negar. (Glosa em espera; vale para recursos legados.)'
            when m.motivo_codigo = '7ES'
                then 'CONFERIR DOCUMENTO. Procedimento incompatível com o sexo: veio o pedido médico e o prontuário do membro confirma? Sim: acatar (EE). Não: negar. (Glosa em espera; vale para recursos legados.)'

            -- Escala
            when m.motivo_codigo = '7E1'
                then 'ESCALAR (Contas Médicas). A justificativa é válida e o contrato da base (HCDB) ou o enviado pelo prestador sustenta o valor cobrado? Sim: acatar (EI); base desatualizada -> acionar cadastro e HCDEV confirma. Justificativa inválida: negar sem abrir contrato; HCDEV não confirma: negar.'
            when m.motivo_codigo = '7DR'
                then 'ESCALAR (HCDEV). Veio contrato mostrando que o código inclui o item, ou e-mail de excepcionalidade? Sim: acatar (EI, roteamento HCDEV). Sem contrato ou excepcionalidade: negar.'

            else 'MOTIVO SEM REGRA NO FLUXOGRAMA. Análise manual.'
        end as o_que_verificar
    from motivo m
)

select
    trim(peg_code)                             as "PEG",
    trim(guide_number)                         as "guide number",
    trim(guide_item_number)                    as "item number",
    o_que_verificar                            as "O que vc precisa verificar?",
    trim(disallowance_reason)                  as "dissalowance reason",
    trim(institution_name)                     as "Institution name",
    trim(member_internal_code)                 as "member internal code",
    trim(tuss_code)                            as "TUSS code",
    trim(procedure_name)                       as "procedure name",
    execution_date                             as "execution date",
    invoice_date                               as "invoice date",
    trim(authorization_key)                    as "authorization key",
    disallowance_value                         as "dissalowance value",
    appeal_value                               as "appeal value",
    appeal_date                                as "appeal date",
    -- colunas de apoio à fila
    grupo_motivo                               as "grupo do motivo",
    motivo_codigo                              as "código vigente",
    case when motivo_codigo <> motivo_codigo_original
         then motivo_codigo_original || ' -> ' || motivo_codigo end
                                               as "código antigo -> vigente",
    tipo_prestador                             as "tipo de prestador",
    appeal_status                              as "status do recurso",
    appeal_object                              as "nível do recurso",
    appeal_attempt                             as "tentativa de recurso",
    working_days_from_appeal_to_analysis       as "dias úteis em aberto",
    disallowance_date                          as "dissalowance date",
    -- prazo de recurso: 60 dias corridos a partir da glosa (há casos excepcionais)
    datediff(day, disallowance_date, appeal_date)
                                               as "dias entre glosa e recurso",
    case when datediff(day, disallowance_date, appeal_date) > 60 then 'Sim' else 'Não' end
                                               as "recurso fora do prazo (60 dias)"
from regra
order by appeal_date, peg_code, guide_number, guide_item_number
