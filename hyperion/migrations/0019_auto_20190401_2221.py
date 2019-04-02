# Generated by Django 2.1.7 on 2019-04-02 04:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hyperion', '0018_server_required_trailing_slash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='visible_to',
        ),
        migrations.AddField(
            model_name='post',
            name='visible_to',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, default=list, size=None),
        ),
    ]
