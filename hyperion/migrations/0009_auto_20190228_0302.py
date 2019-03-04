# Generated by Django 2.1.5 on 2019-02-28 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hyperion', '0008_auto_20190225_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='origin',
            field=models.URLField(default='https://cmput404-front.herokuapp.com'),
        ),
        migrations.AddField(
            model_name='post',
            name='source',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(choices=[('text/plain', 'text/plain'), ('text/markdown', 'text/markdown'), ('image/png;base64', 'image/png;base64'), ('image/jpeg;base64', 'image/jpeg;base64'), ('application/base64', 'application/base64')], default='PUBLIC', max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('FOAF', 'FOAF'), ('FRIENDS', 'FRIENDS'), ('PRIVATE', 'PRIVATE'), ('SERVERONLY', 'SERVERONLY')], default='text/plain', max_length=20),
        ),
    ]
