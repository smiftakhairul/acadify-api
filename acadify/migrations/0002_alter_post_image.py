# Generated by Django 5.0.4 on 2024-04-05 21:04

import acadify.api.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acadify', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=acadify.api.utils.UploadUtils.post),
        ),
    ]
