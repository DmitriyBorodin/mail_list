# Generated by Django 4.2.2 on 2024-10-03 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mail", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="maillistsetting",
            name="periodicity",
            field=models.CharField(
                choices=[
                    ("DAILY", "Ежедневно"),
                    ("WEEKLY", "Еженедельно"),
                    ("MONTHLY", "Ежемесячно"),
                ],
                max_length=20,
                verbose_name="периодичность",
            ),
        ),
        migrations.AlterField(
            model_name="maillistsetting",
            name="status",
            field=models.CharField(
                choices=[
                    ("CREATED", "Создана"),
                    ("STARTED", "Запущена"),
                    ("COMPLETED", "Завершена"),
                ],
                max_length=20,
                verbose_name="Статус рассылки",
            ),
        ),
    ]
