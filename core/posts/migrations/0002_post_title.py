# Generated by Django 3.2.4 on 2022-05-29 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='sting', max_length=200),
            preserve_default=False,
        ),
    ]
