from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .decorators import login_excluded, role_required
from .forms import UserCreateForm, UserEditForm, is_last_active_super_admin, style_form
from .models import CustomUser

_ADMIN = ('SUPER_ADMIN', 'ADMIN')


def _safe_next(request, default='core:dashboard'):
    nxt = request.GET.get('next', '')
    if nxt and url_has_allowed_host_and_scheme(
            nxt, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return nxt
    return default


@login_excluded('core:dashboard')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(_safe_next(request))
            else:
                messages.error(request, 'Your account has been deactivated.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def password_change(request):
    """Any logged-in user changes their own password (old password required)."""
    form = style_form(PasswordChangeForm(request.user, request.POST or None))
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)          # stay logged in
        messages.success(request, 'Your password has been changed.')
        return redirect('accounts:profile')
    return render(request, 'accounts/user_form.html', {
        'form': form, 'title': 'Change My Password', 'back_url': 'accounts:profile',
        'submit_label': 'Change Password',
    })


# ════════════════════ USER MANAGEMENT (admins) ════════════════════

def _manageable(request, pk):
    """Fetch the target user, or None if the actor may not manage them."""
    target = get_object_or_404(CustomUser, pk=pk)
    if target.role == CustomUser.SUPER_ADMIN and request.user.role != CustomUser.SUPER_ADMIN:
        messages.error(request, 'Only a Super Admin can manage Super Admin accounts.')
        return None
    return target


@login_required
@role_required(*_ADMIN)
def user_list(request):
    users = CustomUser.objects.order_by('-is_active', 'role', 'full_name')
    q    = request.GET.get('q', '').strip()
    role = request.GET.get('role', '').strip()
    if q:
        users = users.filter(Q(full_name__icontains=q) | Q(username__icontains=q) | Q(email__icontains=q))
    if role:
        users = users.filter(role=role)
    return render(request, 'accounts/user_list.html', {
        'users': users, 'q': q, 'role': role, 'roles': CustomUser.ROLE_CHOICES,
    })


@login_required
@role_required(*_ADMIN)
def user_add(request):
    form = UserCreateForm(request.POST or None, actor=request.user)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(request, f'Account "{user.username}" created for {user.full_name}.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {
        'form': form, 'title': 'Add User Account', 'back_url': 'accounts:user_list',
        'submit_label': 'Create Account',
    })


@login_required
@role_required(*_ADMIN)
def user_edit(request, pk):
    target = _manageable(request, pk)
    if target is None:
        return redirect('accounts:user_list')
    form = UserEditForm(request.POST or None, instance=target, actor=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'{target.full_name} updated.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {
        'form': form, 'title': f'Edit {target.full_name}', 'back_url': 'accounts:user_list',
        'submit_label': 'Save', 'target': target,
    })


@login_required
@role_required(*_ADMIN)
def user_reset_password(request, pk):
    target = _manageable(request, pk)
    if target is None:
        return redirect('accounts:user_list')
    form = style_form(SetPasswordForm(target, request.POST or None))
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Password reset for {target.full_name}. Give them the new password securely.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {
        'form': form, 'title': f'Reset Password — {target.full_name}', 'back_url': 'accounts:user_list',
        'submit_label': 'Set New Password',
    })


@login_required
@role_required(*_ADMIN)
@require_POST
def user_toggle_active(request, pk):
    target = _manageable(request, pk)
    if target is None:
        return redirect('accounts:user_list')
    if target.pk == request.user.pk:
        messages.error(request, 'You cannot deactivate your own account.')
    elif target.is_active and is_last_active_super_admin(target):
        messages.error(request, 'This is the last active Super Admin and cannot be deactivated.')
    else:
        target.is_active = not target.is_active
        target.save(update_fields=['is_active'])
        state = 'reactivated' if target.is_active else 'deactivated — they can no longer log in'
        messages.success(request, f'{target.full_name} {state}.')
    return redirect('accounts:user_list')
