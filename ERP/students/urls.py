from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # List & Import
    path('',                                 views.student_list,           name='list'),
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
    # ID Card
    path('<int:pk>/id-card/',                views.student_id_card,        name='id_card'),
]
