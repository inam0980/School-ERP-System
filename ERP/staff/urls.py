from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    # Module dashboard
    path('',                              views.staff_dashboard,            name='dashboard'),

    # Staff profiles
    path('list/',                         views.staff_list,                 name='staff_list'),
    path('new/',                          views.staff_form,                 name='staff_add'),
    path('<int:pk>/',                     views.staff_profile,              name='profile'),
    path('<int:pk>/edit/',                views.staff_form,                 name='staff_edit'),
    path('<int:pk>/delete/',              views.staff_delete,               name='staff_delete'),

    # Teacher assignments
    path('assignments/',                  views.teacher_assignment_list,    name='teacher_assignment_list'),
    path('assignments/add/',              views.teacher_assignment_form,    name='teacher_assignment_add'),
    path('assignments/<int:pk>/edit/',    views.teacher_assignment_form,    name='teacher_assignment_edit'),
    path('assignments/<int:pk>/delete/',  views.teacher_assignment_delete,  name='teacher_assignment_delete'),

    # Vacation requests
    path('vacations/',                    views.vacation_list,              name='vacation_list'),
    path('vacations/new/',                views.vacation_form,              name='vacation_add'),
    path('vacations/<int:pk>/edit/',      views.vacation_form,              name='vacation_edit'),
    path('vacations/<int:pk>/approve/',   views.vacation_approve,           name='vacation_approve'),

    # MOE / regulatory approvals
    path('moe/',                          views.moe_list,                   name='moe_list'),
    path('moe/add/',                      views.moe_form,                   name='moe_add'),
    path('moe/<int:pk>/edit/',            views.moe_form,                   name='moe_edit'),
    path('moe/<int:pk>/delete/',          views.moe_delete,                 name='moe_delete'),

    # Teacher dashboard
    path('teacher/',                      views.teacher_dashboard,          name='teacher_dashboard'),

    # Staff attendance (read-only)
    path('attendance/',                   views.staff_attendance_view,      name='staff_attendance'),
]

