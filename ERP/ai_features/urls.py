from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('',                                    views.ai_dashboard,       name='dashboard'),
    path('attendance-risk/',                    views.attendance_risk,    name='attendance_risk'),
    path('grade-analytics/',                    views.grade_analytics,    name='grade_analytics'),
    path('fee-defaults/',                       views.fee_default_risk,   name='fee_default_risk'),
    path('performance/<int:student_pk>/',       views.performance_summary, name='performance_summary'),
    path('noor-validation/',                    views.noor_validation,    name='noor_validation'),
]

