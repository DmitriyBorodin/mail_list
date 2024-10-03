from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DeleteView,
                                  CreateView, UpdateView, DetailView)

from mail.forms import MailListSettingForm
from mail.models import MailListSetting


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
