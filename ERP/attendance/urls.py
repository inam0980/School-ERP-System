from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Main pages
    path('take/',                     views.take_attendance,       name='take'),
    path('report/',                   views.attendance_report,     name='report'),
    path('student/<int:pk>/calendar/',views.student_calendar,      name='student_calendar'),
    path('export/',                   views.export_attendance,     name='export'),

    # AJAX / API
    path('api/session/',              views.api_attendance_session, name='api_session'),
    path('api/submit/',               views.submit_attendance,      name='submit'),
    path('api/summary/',              views.api_today_summary,      name='api_summary'),
]
