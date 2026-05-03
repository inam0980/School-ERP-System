from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Hub (landing page — choose Regular or External)
    path('',                                 views.student_hub,            name='hub'),

    # Regular Students
    path('regular/',                         views.student_list,           name='regular_list'),
    path('regular/export/csv/',              views.student_export_csv,     name='export_csv'),
    path('regular/import/',                  views.student_import,         name='import'),
    path('regular/import/template/',         views.download_import_template, name='import_template'),
    path('regular/add/',                     views.student_add,            name='add'),
    path('regular/<int:pk>/',               views.student_detail,         name='detail'),
    path('regular/<int:pk>/edit/',          views.student_edit,           name='edit'),
    path('regular/<int:pk>/delete/',        views.student_delete,         name='delete'),

    # Regular Student — Documents
    path('regular/<int:pk>/document/upload/', views.document_upload,       name='doc_upload'),
    path('document/<int:doc_pk>/delete/',    views.document_delete,        name='doc_delete'),

    # Regular Student — Siblings
    path('regular/<int:pk>/sibling/add/',   views.sibling_add,            name='sibling_add'),
    path('sibling/<int:sibling_pk>/delete/', views.sibling_delete,        name='sibling_delete'),

    # Regular Student — Authorized Pickup
    path('regular/<int:pk>/pickup/add/',    views.pickup_add,             name='pickup_add'),
    path('pickup/<int:pickup_pk>/delete/',   views.pickup_delete,         name='pickup_delete'),

    # Regular Student — ID Card
    path('regular/<int:pk>/id-card/',       views.student_id_card,        name='id_card'),

    # External Candidates
    path('external/',                        views.external_list,          name='external_list'),
    path('external/add/',                    views.external_add,           name='external_add'),
    path('external/<int:pk>/',              views.external_detail,        name='external_detail'),
    path('external/<int:pk>/edit/',         views.external_edit,          name='external_edit'),

    # ── backward-compat aliases ──
    path('list/',                            views.student_list,           name='list'),
]
