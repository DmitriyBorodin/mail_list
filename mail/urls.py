from django.urls import path

from mail.apps import MailConfig
from mail.views import (
    MailListView,
    MailDetailView,
    MailCreateView,
    MailUpdateView,
    MailDeleteView,
    ClientListView,
    ClientDetailView,
    IndexView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    MessageCreateView,
    MessageListView,
    MessageDetailView,
    MessageUpdateView,
    MessageDeleteView,
    MailingAttemptListView,
    MailingAttemptDetailView,
)

app_name = MailConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index_page"),

    path("mail/", MailListView.as_view(), name="mail_list"),
    path("mail/<int:pk>/", MailDetailView.as_view(), name="mail_detail"),
    path("mail/create/", MailCreateView.as_view(), name="mail_create"),
    path("mail/<int:pk>/update/", MailUpdateView.as_view(), name="mail_update"),
    path("mail/<int:pk>/delete/", MailDeleteView.as_view(), name="mail_delete"),
    path("client/", ClientListView.as_view(), name="client_list"),

    path("client/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client/create/", ClientCreateView.as_view(), name="client_create"),
    path("client/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("client/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),

    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),

    path("report/", MailingAttemptListView.as_view(), name="report_list"),
    path("report/<int:pk>/", MailingAttemptDetailView.as_view(), name="report_detail"),
]
