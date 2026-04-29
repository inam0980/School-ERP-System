from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'fees'

urlpatterns = [
    # Root → dashboard
    path('', views.fees_dashboard, name='dashboard'),

    # Fee Types
    path('fee-types/',                    views.fee_type_list,         name='fee_type_list'),
    path('fee-types/add/',                views.fee_type_form,         name='fee_type_add'),
    path('fee-types/<int:pk>/edit/',      views.fee_type_form,         name='fee_type_edit'),
    path('fee-types/<int:pk>/delete/',    views.fee_type_delete,       name='fee_type_delete'),

    # Fee Structures (individual)
    path('structures/',                   views.fee_structure_list,             name='fee_structure_list'),
    path('structures/export-csv/',        views.fee_structure_export_csv,       name='fee_structure_export_csv'),
    path('structures/export-group-csv/', views.fee_structure_export_group_csv,  name='fee_structure_export_group_csv'),
    path('structures/export-group-pdf/', views.fee_structure_export_group_pdf, name='fee_structure_export_group_pdf'),
    path('structures/add/',               views.fee_structure_form,             name='fee_structure_add'),
    path('structures/<int:pk>/edit/',     views.fee_structure_form,    name='fee_structure_edit'),
    path('structures/<int:pk>/delete/',   views.fee_structure_delete,  name='fee_structure_delete'),
    path('structures/<int:pk>/items/',    views.fee_structure_items_json, name='fee_structure_items'),

    # Bulk assign
    path('assign/',                       views.bulk_assign_fees,      name='bulk_assign'),

    # Student fee edit
    path('student-fee/<int:pk>/edit/',    views.student_fee_edit,      name='student_fee_edit'),

    # Collection
    path('collection/',                   views.fee_collection,        name='collection'),
    path('collection/adhoc-charge/',      views.charge_adhoc_fee,      name='adhoc_charge'),
    path('receipt/<int:payment_pk>/',     views.receipt_print,         name='receipt_print'),
    path('combined-receipt/',             views.combined_receipt,      name='combined_receipt'),

    # Reports
    path('outstanding/',                  views.outstanding_report,    name='outstanding'),
    path('defaulters/',                   views.defaulters_list,       name='defaulters'),
    path('ledger/<int:student_pk>/',      views.student_ledger,        name='student_ledger'),

    # Invoices
    path('invoices/',                     views.invoice_list,          name='invoice_list'),
    path('invoices/generate/<int:student_pk>/', views.generate_invoice, name='generate_invoice'),
    path('invoices/<int:pk>/print/',      views.invoice_print,         name='invoice_print'),

    # Bank verification
    path('payments/<int:payment_pk>/verify/', views.bank_verify_payment, name='bank_verify'),

    # Payroll
    path('payroll/',                      views.payroll_list,          name='payroll_list'),
    path('payroll/add/',                  views.salary_form,           name='salary_add'),
    path('payroll/<int:pk>/edit/',        views.salary_form,           name='salary_edit'),
    path('payroll/<int:pk>/delete/',      views.salary_delete,         name='salary_delete'),
    path('payroll/<int:pk>/mark-paid/',   views.mark_salary_paid,      name='salary_mark_paid'),

    # Tuition Fee Config (complete structured fee schedule)
    path('tuition/',                              views.tuition_config_list,       name='tuition_config_list'),
    path('tuition/add/',                          views.tuition_config_form,       name='tuition_config_add'),
    path('tuition/export/csv/',                   views.tuition_config_export_csv, name='tuition_config_export_csv'),
    path('tuition/<int:pk>/',                     views.tuition_config_detail,     name='tuition_config_detail'),
    path('tuition/<int:pk>/edit/',                views.tuition_config_form,       name='tuition_config_edit'),
    path('tuition/<int:pk>/delete/',              views.tuition_config_delete,     name='tuition_config_delete'),
    path('tuition/<int:pk>/print/',               views.tuition_config_print,      name='tuition_config_print'),

    # JSON API
    path('api/summary/',                  views.api_fees_summary,      name='api_summary'),

    # Installment Payment Plans (per student fee)
    path('payment-plan/<int:student_fee_pk>/setup/', views.setup_payment_plan, name='payment_plan_setup'),
    path('payment-plan/<int:plan_pk>/delete/',       views.delete_payment_plan, name='payment_plan_delete'),

    # ── Simplified Tax Invoice Entry ──────────────────────────
    path('tax-invoice/',                          views.tax_invoice_menu,        name='tax_invoice_menu'),
    path('tax-invoice/reservation/',              views.reservation_invoice,     name='reservation_invoice'),
    path('tax-invoice/credit-note/',              views.tax_credit_note,         name='tax_credit_note'),
    path('tax-invoice/invoice-credit-note/',      views.invoice_credit_note,     name='invoice_credit_note'),
]

