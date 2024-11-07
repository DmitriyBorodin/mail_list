import smtplib
from time import sleep

import pytz
from django.core.mail import send_mail
from datetime import datetime, timedelta

from main_app import settings
from mail.models import MailingAttempt


def send_mailing(mailing):
    """Функция для рассылки писем клиентам"""

    # Получаем текущую дату и время
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    # Если у рассылки нет даты последней рассылки, то отправляем рассылку
    if mailing.last_send is None:
        # Проверяем статус у рассылки и дату запланированной первой рассылки
        if (
            mailing.status in ["CREATED", "STARTED"]
            and mailing.first_send <= current_datetime
        ):
            try:
                # Отправляем письма
                send_mail(
                    subject=mailing.message_to_send.subject,
                    message=mailing.message_to_send.message_body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.receivers.all()],
                    fail_silently=False,
                )

                # Меняем статус на завершено после отправки
                mailing.status = "completed"
                mailing.save()

                # Логируем успешную попытку рассылки
                MailingAttempt.objects.create(
                    attempt_status=True,
                    server_response="Рассылка успешна",
                    parent_mail=mailing,
                )

            except smtplib.SMTPException as e:
                print(f"Ошибка при отправке {mailing}: {e}")
                # Логируем провальную попытку рассылки
                MailingAttempt.objects.create(
                    attempt_status=False, server_response=str(e), parent_mail=mailing
                )
            return

        # Проверяем дату завершения рассылки, если наступила - меняем статус
        if mailing.last_send is not None and mailing.last_send <= current_datetime:
            if mailing.status != "COMPLETED":
                mailing.status = "COMPLETED"
                mailing.save()
            return

    # Проверяем была ли отправка этой рассылки ранее
    mailing_log = (
        MailingAttempt.objects.filter(parent_mail=mailing)
        .order_by("-last_attempt")
        .first()
    )

    # Если была рассылка, то проверяем прошло ли нужное кол-во времени после отправки
    if mailing_log:
        time_delta = current_datetime - mailing_log.last_attempt

        if mailing.periodicity == "DAILY" and time_delta.days >= 1:
            mailing.next_send = mailing_log.last_attempt + timedelta(days=1)
            mailing.status = "STARTED"
            mailing.save()

        if mailing.periodicity == "WEEKLY" and time_delta.days >= 7:
            mailing.next_send = mailing_log.last_attempt + timedelta(days=7)
            mailing.status = "STARTED"
            mailing.save()

        if mailing.periodicity == "MONTHLY" and time_delta.days >= 30:
            mailing.next_send = mailing_log.last_attempt + timedelta(days=30)
            mailing.status = "STARTED"
            mailing.save()

    # Проверяем готовы ли рассылки к отправке
    if (
        mailing.status in ["CREATED", "STARTED"]
        and mailing.first_send <= current_datetime
    ):
        try:
            # Отправляем письма
            send_mail(
                subject=mailing.message_to_send.subject,
                message=mailing.message_to_send.message_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.receivers.all()],
                fail_silently=False,
            )

            # Меняем статус на завершено после отправки
            mailing.status = "completed"
            mailing.save()

            # Логируем успешную попытку рассылки
            MailingAttempt.objects.create(
                attempt_status=True,
                server_response="Рассылка успешна",
                parent_mail=mailing,
            )

        except Exception as e:
            print(f"Ошибка при отправке {mailing}: {e}")
            # Логируем провальную попытку рассылки
            MailingAttempt.objects.create(
                attempt_status=False, server_response=str(e), parent_mail=mailing
            )
        return


def start_mailing():
    """Функция для начала автоматической рассылки"""
    from mail.models import MailListSetting
    from apscheduler.schedulers.background import BackgroundScheduler

    scheduler = BackgroundScheduler()
    mailings = MailListSetting.objects.all()

    for mailing in mailings:
        scheduler.add_job(send_mailing, "interval", seconds=10, args=[mailing])

    scheduler.start()

    while True:
        sleep(1)
