# Generated by Django 3.2.23 on 2024-01-18 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0023_auto_20240118_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergoal',
            name='created_date',
        ),
    ]
