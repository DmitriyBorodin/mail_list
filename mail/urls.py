from django.urls import path

from mail.apps import MailConfig
from mail.views import MailListView, MailDetailView, MailCreateView, \
    MailUpdateView, MailDeleteView

app_name = MailConfig.name


urlpatterns = [
    path("", MailListView.as_view(), name="mail_list"),
    path("<int:pk>/", MailDetailView.as_view(), name="mail_detail"),
    path("create/", MailCreateView.as_view(), name="mail_create"),
    path("<int:pk>/update/", MailUpdateView.as_view(), name="mail_update"),
    path("<int:pk>/delete/", MailDeleteView.as_view(), name="mail_delete"),
]
