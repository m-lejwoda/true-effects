# Generated by Django 3.2.23 on 2023-12-28 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_alter_exercise_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
    ]
