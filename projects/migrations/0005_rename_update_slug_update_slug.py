# Generated by Django 3.2.7 on 2021-09-08 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20210908_2051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='update',
            old_name='update_slug',
            new_name='slug',
        ),
    ]
