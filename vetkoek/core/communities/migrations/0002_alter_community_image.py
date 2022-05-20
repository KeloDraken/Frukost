# Generated by Django 3.2.4 on 2022-05-20 19:20

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to='uploads/communities/banners/'),
        ),
    ]
