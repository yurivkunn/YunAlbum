# Generated by Django 2.2.2 on 2019-07-10 17:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyAlbum', '0008_auto_20190710_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='alterTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 10, 17, 5, 22, 617698)),
        ),
        migrations.AlterField(
            model_name='email_checkcode',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 10, 17, 5, 22, 619694)),
        ),
        migrations.AlterField(
            model_name='storage',
            name='alterTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 10, 17, 5, 22, 615701)),
        ),
    ]
