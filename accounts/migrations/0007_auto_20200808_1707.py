# Generated by Django 2.2 on 2020-08-08 15:07

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200808_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, null=True, quality=75, size=[200, 200], upload_to='static/images/'),
        ),
    ]
