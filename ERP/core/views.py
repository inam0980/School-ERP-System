from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
        'role': user.role,
    }
    return render(request, 'core/dashboard.html', context)
