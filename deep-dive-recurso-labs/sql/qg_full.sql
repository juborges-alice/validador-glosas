SELECT
  peg_code, guide_number, original_guide_number, main_guide_number, operator_guide_number,
  associated_guide_reference_key, guide_reference_key, invoice_date, invoice_step,
  guide_status, procedure_status, analysis_status, financial_status,
  procedure_code, presented_value, disallowance_value, disallowance_reason, payment_value, paid,
  appeal_date, appeal_value, appeal_status, execution_date, import_file_name
FROM curated.totvs_procedure_invoice
WHERE system_source = 'totvs-alice'
  AND provider_economic_group = 'FLEURY'
  AND TRIM(guide_type_description) = 'GUIA DE RECURSO DE GLOSA'
  AND invoice_date >= '2026-09-01'
LIMIT 8
