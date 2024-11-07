from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")

    name = models.CharField(max_length=100, verbose_name="ФИО")

    comment = models.CharField(max_length=100, verbose_name="Комментарий")

    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Владелец", **NULLABLE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Тема письма")

    message_body = models.TextField(verbose_name="Тело письма")

    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Владелец", **NULLABLE
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


DAILY = "DAILY"
WEEKLY = "WEEKLY"
MONTHLY = "MONTHLY"

CHOICES_PERIODICITY = (
    (DAILY, "Ежедневно"),
    (WEEKLY, "Еженедельно"),
    (MONTHLY, "Ежемесячно"),
)

CREATED = "CREATED"
STARTED = "STARTED"
COMPLETED = "COMPLETED"

CHOICES_STATUS = (
    (CREATED, "Создана"),
    (STARTED, "Запущена"),
    (COMPLETED, "Завершена"),
)


class MailListSetting(models.Model):
    first_send = models.DateTimeField(
        verbose_name="Дата и время первой рассылки", **NULLABLE
    )

    next_send = models.DateTimeField(
        verbose_name="Дата и время следующей рассылки", **NULLABLE
    )

    last_send = models.DateTimeField(
        verbose_name="Дата и время последней рассылки", **NULLABLE
    )

    periodicity = models.CharField(
        max_length=20, choices=CHOICES_PERIODICITY, verbose_name="периодичность"
    )

    status = models.CharField(
        max_length=20, choices=CHOICES_STATUS, verbose_name="Статус рассылки"
    )

    message_to_send = models.OneToOneField(
        Message,
        verbose_name="Сообщение",
        related_name="Рассылка",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )

    receivers = models.ManyToManyField(
        Client, verbose_name="Получатели", related_name="Рассылка"
    )

    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Владелец рассылки", **NULLABLE
    )

    def __str__(self):
        return f"Время первой рассылки{self.first_send}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ('set_active_status', 'Can activate mailing'),
        ]


class MailingAttempt(models.Model):
    last_attempt = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время последней рассылки"
    )

    attempt_status = models.BooleanField(verbose_name="Статус попытки рассылки")

    server_response = models.TextField(verbose_name="Ответ сервера", **NULLABLE)

    parent_mail = models.ForeignKey(
        MailListSetting, verbose_name="Рассылка", on_delete=models.SET_NULL, **NULLABLE
    )

    def __str__(self):
        return self.last_attempt

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
