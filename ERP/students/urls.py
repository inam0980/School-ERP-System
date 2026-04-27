from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # List & Import
    path('',                                 views.student_list,           name='list'),
    path('export/csv/',                      views.student_export_csv,     name='export_csv'),
    path('import/',                          views.student_import,         name='import'),
    path('import/template/',                 views.download_import_template, name='import_template'),
    # CRUD
    path('add/',                             views.student_add,            name='add'),
    path('<int:pk>/',                        views.student_detail,         name='detail'),
    path('<int:pk>/edit/',                   views.student_edit,           name='edit'),
    path('<int:pk>/delete/',                 views.student_delete,         name='delete'),
    # Documents
    path('<int:pk>/document/upload/',        views.document_upload,        name='doc_upload'),
    path('document/<int:doc_pk>/delete/',    views.document_delete,        name='doc_delete'),
    # Siblings
    path('<int:pk>/sibling/add/',            views.sibling_add,            name='sibling_add'),
    path('sibling/<int:sibling_pk>/delete/', views.sibling_delete,         name='sibling_delete'),
    # Authorized Pickup
    path('<int:pk>/pickup/add/',             views.pickup_add,             name='pickup_add'),
    path('pickup/<int:pickup_pk>/delete/',   views.pickup_delete,          name='pickup_delete'),
    # ID Card
    path('<int:pk>/id-card/',                views.student_id_card,        name='id_card'),
]
