from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',    views.login_view,      name='login'),
    path('logout/',   views.logout_view,     name='logout'),
    path('profile/',  views.profile_view,    name='profile'),
    path('password/', views.password_change, name='password_change'),

    # User account management (Super Admin / Admin)
    path('users/',                          views.user_list,           name='user_list'),
    path('users/add/',                      views.user_add,            name='user_add'),
    path('users/<int:pk>/edit/',            views.user_edit,           name='user_edit'),
    path('users/<int:pk>/reset-password/',  views.user_reset_password, name='user_reset_password'),
    path('users/<int:pk>/toggle-active/',   views.user_toggle_active,  name='user_toggle_active'),
]
