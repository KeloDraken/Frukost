# Generated by Django 3.2.4 on 2021-11-30 18:34

import core.accounts.models
import core.accounts.validators
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('object_id', models.CharField(blank=True, max_length=20, null=True)),
                ('is_fake_profile', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('gelt', models.IntegerField(default=500)),
                ('num_posts', models.PositiveIntegerField(default=0)),
                ('email', core.accounts.models.LowercaseCharField(error_messages={'unique': 'This email address already has an account associated with it'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=300, unique=True, validators=[core.accounts.validators.UnicodeEmailValidator()], verbose_name='email address')),
                ('display_name', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_pic', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='accounts/profile_pics/')),
                ('bio', models.TextField(blank=True, max_length=3000, null=True)),
                ('subscribers', models.PositiveBigIntegerField(default=1)),
                ('upvotes', models.PositiveBigIntegerField(default=0)),
                ('instagram', models.CharField(blank=True, max_length=60, null=True)),
                ('vsco', models.CharField(blank=True, max_length=60, null=True)),
                ('twitter', models.CharField(blank=True, max_length=60, null=True)),
                ('website', models.URLField(blank=True, max_length=300, null=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('datetime_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
