from django.contrib import admin

from mail.models import MailListSetting, Client, Message, MailingAttempt


@admin.register(MailListSetting)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("first_send", "periodicity", "status")


@admin.register(Client)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "comment")


@admin.register(Message)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("subject", "message_body")


@admin.register(MailingAttempt)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("last_attempt", "attempt_status", "server_response", "parent_mail")
