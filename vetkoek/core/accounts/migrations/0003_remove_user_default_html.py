# Generated by Django 3.2.4 on 2022-05-22 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_default_html'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='default_html',
        ),
    ]
