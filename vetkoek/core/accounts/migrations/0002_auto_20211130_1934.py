# Generated by Django 3.2.9 on 2021-11-30 17:34

import core.accounts.models
import core.accounts.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='datetime_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='display_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gelt',
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name='user',
            name='instagram',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_fake_profile',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='num_posts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='object_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='subscribers',
            field=models.PositiveBigIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='twitter',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='upvotes',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='vsco',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='website',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=core.accounts.models.LowercaseCharField(error_messages={'unique': 'This email address already has an account associated with it'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=300, unique=True, validators=[core.accounts.validators.UnicodeEmailValidator()], verbose_name='email address'),
        ),
    ]
