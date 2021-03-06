# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 14:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orgs', '0002_auto_20161026_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='Project title')),
                ('description', models.TextField(blank=True, max_length=255, verbose_name='A short description of your project')),
                ('slug', models.SlugField(blank=True, max_length=30, unique=True)),
                ('members', models.ManyToManyField(related_name='project_members', to='orgs.Membership')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_org', to='orgs.Org')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_owner', to='orgs.Membership')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
