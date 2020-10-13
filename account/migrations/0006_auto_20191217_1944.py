# Generated by Django 2.2.6 on 2019-12-17 10:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20191217_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='hokudai.ac.jp で終わるメールアドレスのみ登録できます', max_length=254, unique=True, validators=[django.core.validators.RegexValidator(message='hokudai.ac.jp で終わるメールアドレスのみ登録できます', regex='hokudai.ac.jp$'), django.core.validators.EmailValidator], verbose_name='email'),
        ),
    ]