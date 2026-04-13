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

    # Fee Structures
    path('structures/',                   views.fee_structure_list,    name='fee_structure_list'),
    path('structures/add/',               views.fee_structure_form,    name='fee_structure_add'),
    path('structures/<int:pk>/edit/',     views.fee_structure_form,    name='fee_structure_edit'),
    path('structures/<int:pk>/delete/',   views.fee_structure_delete,  name='fee_structure_delete'),

    # Bulk assign
    path('assign/',                       views.bulk_assign_fees,      name='bulk_assign'),

    # Student fee edit
    path('student-fee/<int:pk>/edit/',    views.student_fee_edit,      name='student_fee_edit'),

    # Collection
    path('collection/',                   views.fee_collection,        name='collection'),
    path('receipt/<int:payment_pk>/',     views.receipt_print,         name='receipt_print'),

    # Reports
    path('outstanding/',                  views.outstanding_report,    name='outstanding'),
    path('defaulters/',                   views.defaulters_list,       name='defaulters'),
    path('ledger/<int:student_pk>/',      views.student_ledger,        name='student_ledger'),

    # Invoices
    path('invoices/',                     views.invoice_list,          name='invoice_list'),
    path('invoices/generate/<int:student_pk>/', views.generate_invoice, name='generate_invoice'),
    path('invoices/<int:pk>/print/',      views.invoice_print,         name='invoice_print'),

    # Payroll
    path('payroll/',                      views.payroll_list,          name='payroll_list'),
    path('payroll/add/',                  views.salary_form,           name='salary_add'),
    path('payroll/<int:pk>/edit/',        views.salary_form,           name='salary_edit'),
    path('payroll/<int:pk>/delete/',      views.salary_delete,         name='salary_delete'),
    path('payroll/<int:pk>/mark-paid/',   views.mark_salary_paid,      name='salary_mark_paid'),

    # JSON API
    path('api/summary/',                  views.api_fees_summary,      name='api_summary'),
]
