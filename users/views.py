import secrets

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView

from mail.forms import StyleMixin
from main_app.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserPasswordResetView(PasswordResetView, StyleMixin):
    form_class = PasswordResetForm
    template_name = "users/password_reset.html"
    success_url = reverse_lazy("users:password_reset")

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user:
                password = User.objects.make_random_password(length=8)
                user.set_password(password)
                user.save()
                send_mail(
                    subject="Ресет пароля",
                    message=f"Ваш новый пароль - {password}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[email]
                )
            return redirect(reverse('users:login'))
        except:
            return redirect(reverse('users:mail_not_found'))


class NoMailView(TemplateView):
    template_name = "users/mail_not_found.html"


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
