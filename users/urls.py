from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserRegisterView, email_verification, \
    UserPasswordResetView, NoMailView, ProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email_confirm'),
    path('password-reset/', UserPasswordResetView.as_view(),name='password_reset'),
    path("mail-not-found/", NoMailView.as_view(), name='no_mail'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
