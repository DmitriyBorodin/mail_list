# Generated by Django 4.2.2 on 2024-11-03 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mail", "0006_maillistsetting_last_send_maillistsetting_next_send_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailingattempt",
            name="last_attempt",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата и время последней рассылки"
            ),
        ),
    ]