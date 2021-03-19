# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-01-27 16:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContextTag',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('domain', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteColor',
            fields=[
                ('id', models.AutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID')),
                ('color', models.CharField(
                    choices=[
                        ('green', 'Green'),
                        ('gray', 'Gray'),
                        ('blue', 'Blue'),
                        ('grey', 'Grey')],
                    max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PersonContextTag',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('person', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='demo.Person')),
                ('tags', models.ManyToManyField(to='demo.ContextTag')),
            ],
        ),
        migrations.CreateModel(
            name='PersonTag',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('person', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='demo.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='persontag',
            name='tags',
            field=models.ManyToManyField(to='demo.Tag'),
        ),
        migrations.AddField(
            model_name='favoritecolor',
            name='person',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='demo.Person'),
        ),
    ]