# Generated by Django 2.1.7 on 2019-03-24 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hyperion', '0014_auto_20190324_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='foreign_db_password',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='foreign_db_username',
            field=models.TextField(blank=True, null=True),
        ),
    ]
