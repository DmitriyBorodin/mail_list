# Generated by Django 4.2.2 on 2024-11-06 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mail", "0007_alter_mailingattempt_last_attempt"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="maillistsetting",
            name="receivers",
        ),
        migrations.AddField(
            model_name="maillistsetting",
            name="receivers",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="Рассылка",
                to="mail.client",
                verbose_name="Получатели",
            ),
        ),
    ]