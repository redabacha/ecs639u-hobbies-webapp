# Generated by Django 3.2.8 on 2021-12-07 03:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hobbies', '0003_auto_20211207_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
