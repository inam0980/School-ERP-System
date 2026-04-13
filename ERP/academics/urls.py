from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'academics'

urlpatterns = [
    # Root redirect → exam list
    path('', lambda req: redirect('academics:exam_list'), name='index'),

    # Exam types
    path('exam-types/',                    views.exam_type_list,   name='exam_type_list'),
    path('exam-types/add/',                views.exam_type_form,   name='exam_type_add'),
    path('exam-types/<int:pk>/edit/',      views.exam_type_form,   name='exam_type_edit'),
    path('exam-types/<int:pk>/delete/',    views.exam_type_delete, name='exam_type_delete'),

    # Exams
    path('exams/',                         views.exam_list,        name='exam_list'),
    path('exams/add/',                     views.exam_form,        name='exam_add'),
    path('exams/<int:pk>/edit/',           views.exam_form,        name='exam_edit'),
    path('exams/<int:pk>/delete/',         views.exam_delete,      name='exam_delete'),

    # Marks workflow
    path('exams/<int:exam_pk>/marks/',     views.marks_entry,      name='marks_entry'),
    path('exams/<int:exam_pk>/approve/',   views.approve_marks,    name='approve_marks'),
    path('exams/<int:exam_pk>/unlock/',    views.unlock_marks,     name='unlock_marks'),
    path('exams/<int:exam_pk>/results/',   views.exam_results,     name='exam_results'),
    path('exams/<int:exam_pk>/export/',    views.export_marks_excel, name='export_marks'),

    # Marks approval queue
    path('marks/pending/',                 views.marks_approval,   name='marks_approval'),

    # Report cards
    path('report-card/<int:student_pk>/',  views.report_card_view, name='report_card'),
    path('report-card/<int:student_pk>/pdf/', views.report_card_pdf, name='report_card_pdf'),
    path('report-cards/bulk/',             views.bulk_report_cards, name='bulk_report_cards'),

    # Noor export
    path('export/noor/',                   views.noor_export,      name='noor_export'),

    # Grade configs
    path('grade-configs/',                 views.grade_config_list, name='grade_config_list'),
    path('grade-configs/add/',             views.grade_config_form, name='grade_config_add'),
    path('grade-configs/<int:pk>/edit/',   views.grade_config_form, name='grade_config_edit'),

    # JSON APIs
    path('api/subjects/',  views.api_subjects_by_section,    name='api_subjects'),
    path('api/exams/',     views.api_exams_by_subject_section, name='api_exams'),
]
