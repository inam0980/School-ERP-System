from django import forms
from django.contrib.auth import password_validation

from .models import CustomUser

_INPUT = ('w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-700 '
          'focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/30 focus:border-[#1e3a5f] '
          'transition bg-white')


def style_form(form):
    """Apply the project's input styling to every widget of a form."""
    for field in form.fields.values():
        if not isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.setdefault('class', _INPUT)
    return form


def role_choices_for(actor):
    """Only a Super Admin may grant the Super Admin role."""
    if actor.role == CustomUser.SUPER_ADMIN:
        return CustomUser.ROLE_CHOICES
    return [c for c in CustomUser.ROLE_CHOICES if c[0] != CustomUser.SUPER_ADMIN]


class _RoleLimitedForm(forms.ModelForm):
    def __init__(self, *args, actor, **kwargs):
        super().__init__(*args, **kwargs)
        self.actor = actor
        self.fields['role'].choices = role_choices_for(actor)
        style_form(self)

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        clash = CustomUser.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if email and clash.exists():
            raise forms.ValidationError('Another account already uses this email address.')
        return email


class UserCreateForm(_RoleLimitedForm):
    password1 = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Confirm password', strip=False, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'role']
        help_texts = {'username': 'Used to log in. Letters, digits and . _ - only.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].initial = CustomUser.TEACHER

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'The two passwords do not match.')
        elif p1:
            # Validate against the would-be user so "too similar to username" works.
            candidate = CustomUser(username=cleaned.get('username', ''),
                                   full_name=cleaned.get('full_name', ''),
                                   email=cleaned.get('email', ''))
            try:
                password_validation.validate_password(p1, candidate)
            except forms.ValidationError as e:
                self.add_error('password1', e)
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserEditForm(_RoleLimitedForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk == self.actor.pk:
            # Changing your own role is how admins lock themselves out.
            self.fields['role'].disabled = True
            self.fields['role'].help_text = 'You cannot change your own role.'

    def clean_role(self):
        role = self.cleaned_data['role']
        target = self.instance
        if (target.role == CustomUser.SUPER_ADMIN and role != CustomUser.SUPER_ADMIN
                and is_last_active_super_admin(target)):
            raise forms.ValidationError('This is the last active Super Admin — the role cannot be changed.')
        return role


def is_last_active_super_admin(user):
    return (user.role == CustomUser.SUPER_ADMIN and user.is_active and not
            CustomUser.objects.filter(role=CustomUser.SUPER_ADMIN, is_active=True)
                              .exclude(pk=user.pk).exists())
