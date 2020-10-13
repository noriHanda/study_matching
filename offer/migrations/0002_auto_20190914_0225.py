# Generated by Django 2.2.4 on 2019-09-13 17:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, upload_to='offer', verbose_name=''),
        ),
        migrations.AlterField(
            model_name='offer',
            name='offerer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to=settings.AUTH_USER_MODEL),
        ),
    ]
