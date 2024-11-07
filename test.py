import os

from django.core.mail import send_mail
from main_app import settings

from main_app.settings import EMAIL_HOST_USER

from apscheduler.schedulers.background import BlockingScheduler

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_app.settings")
# send_mail(
#     subject="Тема письма",
#     message="Тело письма",
#     from_email=EMAIL_HOST_USER,
#     recipient_list=["di-laim@mail.ru"],
# )


# def test_print(msg):
#     print(f'Вывожу сообщение - {msg}')
#
#
# scheduler = BlockingScheduler()
# job_id = scheduler.add_job(test_print, 'interval', seconds=3, args=["пампам"])

# scheduler.start()

from pprint import pprint


def print_clients():
    from mail.models import Client

    clients = Client.objects.all()
    pprint(clients)


print_clients()
