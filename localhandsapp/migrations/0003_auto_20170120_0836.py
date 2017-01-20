# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-20 08:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('localhandsapp', '0002_customer_driver'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('short_description', models.CharField(max_length=500)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='scooper',
            name='logo',
            field=models.ImageField(blank=True, upload_to='scooper_logo/'),
        ),
        migrations.AddField(
            model_name='task',
            name='scooper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localhandsapp.Scooper'),
        ),
    ]
