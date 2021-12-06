# Generated by Django 3.0 on 2020-01-21 18:51

import datetime
import django.contrib.postgres.fields.ranges
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mails", "0002_announcementviewmodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcementviewmodel",
            name="view_time",
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(
                default=datetime.timedelta(0)
            ),
        ),
    ]