import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DeleteView,
    CreateView,
    UpdateView,
    DetailView,
    TemplateView,
)

from blog.models import Blog
from mail.forms import MailListSettingForm, ClientForm, MessageForm
from mail.models import MailListSetting, Client, Message, MailingAttempt
from mail.services import send_mailing


class FormValidMixin:
    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class OwnerPermissionMixin:
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class IndexView(TemplateView):
    template_name = "mail/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings_total'] = MailListSetting.objects.all().count()
        context['active_mailings_total'] = MailListSetting.objects.filter(status__in=['CREATED', 'STARTED']).count()
        context['clients_total'] = Client.objects.all().count()

        blog = Blog.objects.filter(is_published=True)
        random_blogs = random.sample(list(blog), min(3, len(blog)))
        context['random_blogs'] = random_blogs

        return context


class MailListView(LoginRequiredMixin, OwnerPermissionMixin, ListView):
    model = MailListSetting

    def get_queryset(self):
        return MailListSetting.objects.filter(owner=self.request.user)


class MailDetailView(OwnerPermissionMixin, DetailView):
    model = MailListSetting

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()
        send_mailing(mailing)
        logs = MailingAttempt.objects.filter(parent_mail=mailing).order_by(
            "-last_attempt"
        )

        if logs:
            messages.success(request, "Рассылка завершена")
        else:
            messages.error(request, "Ошибка рассылки, надо что-то менять")

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("mail:mail_detail", args=[self.kwargs.get("pk")])


class MailCreateView(LoginRequiredMixin, FormValidMixin, CreateView):
    model = MailListSetting
    form_class = MailListSettingForm
    success_url = reverse_lazy("mail:mail_list")


class MailUpdateView(LoginRequiredMixin, OwnerPermissionMixin, UpdateView):
    model = MailListSetting
    form_class = MailListSettingForm
    success_url = reverse_lazy("mail:mail_list")


class MailDeleteView(OwnerPermissionMixin, DeleteView):
    model = MailListSetting
    success_url = reverse_lazy("mail:mail_list")


class ClientListView(LoginRequiredMixin, OwnerPermissionMixin, ListView):

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)
    model = Client


class ClientDetailView(OwnerPermissionMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, FormValidMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mail:client_list")


class ClientUpdateView(LoginRequiredMixin, OwnerPermissionMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mail:client_list")


class ClientDeleteView(OwnerPermissionMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("mail:client_list")


class MessageCreateView(LoginRequiredMixin, FormValidMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mail:message_list")


class MessageListView(LoginRequiredMixin, OwnerPermissionMixin, ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(OwnerPermissionMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, OwnerPermissionMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mail:message_list")


class MessageDeleteView(OwnerPermissionMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mail:message_list")


class MailingAttemptListView(LoginRequiredMixin, OwnerPermissionMixin, ListView):
    model = MailingAttempt

    def get_queryset(self):
        return MailingAttempt.objects.filter(parent_mail__owner=self.request.user)


class MailingAttemptDetailView(DetailView):
    model = MailingAttempt

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.parent_mail.owner:
            return self.object
        raise PermissionDenied
