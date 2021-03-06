# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_type', models.CharField(choices=[(b'SU', b'Super User'), (b'Company', b'Company User'), (b'Employe', b'Employe User'), (b'Supplier', b'Supplier User')], default=b'Employe', max_length=10, verbose_name=b'user_type')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name=b'username')),
                ('email', models.EmailField(max_length=255, verbose_name=b'email address')),
                ('date_of_birth', models.DateField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
