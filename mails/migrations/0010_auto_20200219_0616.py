# Generated by Django 3.0 on 2020-02-19 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mails", "0009_auto_20200210_1253"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="internal_date",
            field=models.DateTimeField(verbose_name="Received Date (EST)"),
        ),
    ]
