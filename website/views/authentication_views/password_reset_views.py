from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import (
    SetPasswordForm
)
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import PasswordResetCompleteView
from api.views.authentication_views.auth_views import validate_password


class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
        'regex_failed': _('8~16자리를 사용해야 합니다.'),
    }
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
                'autocomplete': 'new-password',
                'class': 'form-control', 
                'placeholder': 'New Password',
                "id" : "new-password1"
            }),
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control', 
            'placeholder': 'Confirm Password',
            'id':'new-password2'
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            if not validate_password(password=password2):
                raise ValidationError(
                    self.error_messages['regex_failed'],
                    code='regex_failed',
                )
        return password2

class UserPasswordResetView(PasswordResetView):
    template_name = 'authentication/password_reset.html'
    success_url = reverse_lazy('website:password_reset_done')
    email_template_name = "authentication/password_reset_email.html"
    subject_template_name = "authentication/password_reset_subject.txt"
    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email"), profile__oauth_type='').exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'authentication/password_reset_done_fail.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('website:password_reset_complete')
    form_class = CustomSetPasswordForm
    template_name = 'authentication/password_reset_confirm.html'

            
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'authentication/password_reset_done.html'


class UserPasswordResetCompleteView(PasswordResetDoneView):
    template_name = 'authentication/password_reset_complete.html'
