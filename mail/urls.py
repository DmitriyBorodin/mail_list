from django.urls import path

from mail.apps import MailConfig
from mail.views import index

app_name = MailConfig.name

urlpatterns = [
    path("", index)
]