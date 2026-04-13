from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # ── Academic Years ──────────────────────────────────────────
    path('school-setup/academic-years/',                  views.academic_year_list,   name='academic_year_list'),
    path('school-setup/academic-years/add/',              views.academic_year_add,    name='academic_year_add'),
    path('school-setup/academic-years/<int:pk>/edit/',    views.academic_year_edit,   name='academic_year_edit'),
    path('school-setup/academic-years/<int:pk>/delete/',  views.academic_year_delete, name='academic_year_delete'),

    # ── Divisions ───────────────────────────────────────────────
    path('school-setup/divisions/',                 views.division_list,   name='division_list'),
    path('school-setup/divisions/add/',             views.division_add,    name='division_add'),
    path('school-setup/divisions/<int:pk>/edit/',   views.division_edit,   name='division_edit'),
    path('school-setup/divisions/<int:pk>/delete/', views.division_delete, name='division_delete'),

    # ── Grades ──────────────────────────────────────────────────
    path('school-setup/grades/',                 views.grade_list,   name='grade_list'),
    path('school-setup/grades/add/',             views.grade_add,    name='grade_add'),
    path('school-setup/grades/<int:pk>/edit/',   views.grade_edit,   name='grade_edit'),
    path('school-setup/grades/<int:pk>/delete/', views.grade_delete, name='grade_delete'),

    # ── Sections ────────────────────────────────────────────────
    path('school-setup/sections/',                 views.section_list,   name='section_list'),
    path('school-setup/sections/add/',             views.section_add,    name='section_add'),
    path('school-setup/sections/<int:pk>/edit/',   views.section_edit,   name='section_edit'),
    path('school-setup/sections/<int:pk>/delete/', views.section_delete, name='section_delete'),

    # ── Subjects ────────────────────────────────────────────────
    path('school-setup/subjects/',                 views.subject_list,   name='subject_list'),
    path('school-setup/subjects/add/',             views.subject_add,    name='subject_add'),
    path('school-setup/subjects/<int:pk>/edit/',   views.subject_edit,   name='subject_edit'),
    path('school-setup/subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),

    # ── API endpoints ───────────────────────────────────────────
    path('api/grades/',   views.api_grades,   name='api_grades'),
    path('api/sections/', views.api_sections, name='api_sections'),
]

