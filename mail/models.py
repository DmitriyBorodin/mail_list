from django.db import models

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    email = models.EmailField(
        unique=True, verbose_name="Email")

    name = models.CharField(
        max_length=100, verbose_name="ФИО")

    comment = models.CharField(
        max_length=100, verbose_name="Комментарий")


class Message(models.Model):
    subject = models.CharField(
        max_length=100,
        verbose_name="Тема письма")

    message_body = models.TextField(
        verbose_name="Тело письма")


DAILY = "DAILY"
WEEKLY = "WEEKLY"
MONTHLY = "MONTHLY"

CHOICES = (
    (DAILY, "Ежедневно"),
    (WEEKLY, "Еженедельно"),
    (MONTHLY, "Ежемесячно"),
)


class MailListSetting(models.Model):
    first_send = models.DateTimeField(
        verbose_name="Дата и время первой рассылки")

    periodicity = models.CharField(
        max_length=7,
        choices=CHOICES,
        verbose_name="периодичность")

    status = models.CharField(
        max_length=7,
        choices=CHOICES,
        verbose_name="Статус рассылки")

    message_to_send = models.OneToOneField(
        Message,
        verbose_name="Сообщение",
        related_name="Рассылка",
        on_delete=models.SET_NULL,
        **NULLABLE)

    receivers = models.ForeignKey(
        Client,
        verbose_name="Получатели",
        related_name="Рассылка",
        on_delete=models.SET_NULL,
        **NULLABLE)


class MailingAttempt(models.Model):
    last_attempt = models.DateTimeField(
        verbose_name="Дата и время последней рассылки")

    attempt_status = models.BooleanField(
        verbose_name="Статус попытки рассылки")

    server_response = models.TextField(
        verbose_name="Ответ сервера", **NULLABLE)

    parent_mail = models.OneToOneField(
        MailListSetting,
        verbose_name="Рассылка",
        on_delete=models.SET_NULL,
        **NULLABLE)




