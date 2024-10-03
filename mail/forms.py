from django import forms
from django.forms import BooleanField, ModelForm

from mail.models import MailListSetting, Client


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class MailListSettingForm(StyleMixin, ModelForm):
    class Meta:
        model = MailListSetting
        fields = ('first_send', 'periodicity',
                  'message_to_send', 'receivers')

        widgets = {
            'first_send': forms.TextInput(attrs={'type': 'datetime-local'}),
        }


class ClientForm(StyleMixin, ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'comment')
