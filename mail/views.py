from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DeleteView, CreateView,
                                  UpdateView, DetailView, TemplateView)

from mail.forms import MailListSettingForm, ClientForm
from mail.models import MailListSetting, Client


class IndexView(TemplateView):
    template_name = "mail/index.html"


class MailListView(ListView):
    model = MailListSetting


class MailDetailView(DetailView):
    model = MailListSetting


class MailCreateView(CreateView):
    model = MailListSetting
    form_class = MailListSettingForm
    success_url = reverse_lazy('mail:mail_list')


class MailUpdateView(UpdateView):
    model = MailListSetting
    form_class = MailListSettingForm
    success_url = reverse_lazy('mail:mail_list')


class MailDeleteView(DeleteView):
    model = MailListSetting
    success_url = reverse_lazy('mail:mail_list')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mail:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mail:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mail:client_list')
