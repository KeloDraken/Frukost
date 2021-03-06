# Generated by Django 3.2.4 on 2022-05-22 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(max_length=11)),
                ('title', models.CharField(max_length=140)),
                ('image', imagekit.models.fields.ProcessedImageField(null=True, upload_to='uploads/communities/banners/')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
