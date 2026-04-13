from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """
    Restrict view access to users with one of the specified roles.
    Usage: @role_required('ADMIN', 'SUPER_ADMIN')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.role not in roles:
                messages.error(request, "You don't have permission to access this page.")
                return redirect('core:dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def login_excluded(redirect_to='core:dashboard'):
    """Redirect already-authenticated users away from login page."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
