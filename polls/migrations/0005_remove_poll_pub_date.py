# Generated by Django 3.2.4 on 2021-07-30 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_poll_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='pub_date',
        ),
    ]