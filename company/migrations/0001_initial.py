# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-28 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField(default=b'{}', null=True)),
                ('crunchbase', models.TextField(default=b'{}', null=True)),
                ('description', models.CharField(max_length=1024, null=True)),
                ('domain', models.CharField(max_length=1024, null=True)),
                ('domainAliases', models.CharField(max_length=1024, null=True)),
                ('similarDomains', models.CharField(max_length=1024, null=True)),
                ('emailProvider', models.NullBooleanField()),
                ('facebook', models.TextField(default=b'{}', null=True)),
                ('foundedYear', models.IntegerField(null=True)),
                ('geo', models.TextField(default=b'{}', null=True)),
                ('api_id', models.CharField(max_length=1024, null=True)),
                ('indexedAt', models.CharField(max_length=1024, null=True)),
                ('legalName', models.CharField(max_length=1024, null=True)),
                ('linkedin', models.TextField(default=b'{}', null=True)),
                ('location', models.CharField(max_length=1024, null=True)),
                ('logo', models.CharField(max_length=1024, null=True)),
                ('metrics', models.TextField(default=b'{}', null=True)),
                ('name', models.CharField(max_length=1024, null=True)),
                ('phone', models.TextField(default=b'{}', null=True)),
                ('site', models.TextField(default=b'{}', null=True)),
                ('tags', models.CharField(max_length=1024, null=True)),
                ('tech', models.CharField(max_length=1024, null=True)),
                ('ticker', models.TextField(default=b'{}', null=True)),
                ('timeZone', models.CharField(max_length=1024, null=True)),
                ('twitter', models.TextField(default=b'{}', null=True)),
                ('type', models.CharField(max_length=1024, null=True)),
                ('utcOffset', models.IntegerField(null=True)),
            ],
        ),
    ]
