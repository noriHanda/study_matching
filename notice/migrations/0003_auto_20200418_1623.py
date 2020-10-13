# Generated by Django 3.0.2 on 2020-04-18 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0002_unreadnoticecount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='body',
            field=models.CharField(max_length=8192),
        ),
        migrations.AlterField(
            model_name='notice',
            name='image_url',
            field=models.URLField(),
        ),
    ]