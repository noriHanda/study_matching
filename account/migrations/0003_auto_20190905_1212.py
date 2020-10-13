# Generated by Django 2.2.4 on 2019-09-05 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20190905_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.TextField(blank=True, max_length=50, verbose_name='department'),
        ),
        migrations.AddField(
            model_name='user',
            name='faculty',
            field=models.TextField(blank=True, max_length=50, verbose_name='faculty'),
        ),
        migrations.AddField(
            model_name='user',
            name='hobby',
            field=models.TextField(blank=True, max_length=200, verbose_name='hobby'),
        ),
        migrations.AddField(
            model_name='user',
            name='school_year',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='school year'),
        ),
        migrations.AddField(
            model_name='user',
            name='want_to_know',
            field=models.TextField(blank=True, max_length=400, verbose_name='what want to know'),
        ),
        migrations.AddField(
            model_name='user',
            name='want_to_teach',
            field=models.TextField(blank=True, max_length=400, verbose_name='what want to teach'),
        ),
    ]
