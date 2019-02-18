# Generated by Django 2.1.5 on 2019-02-18 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hyperion', '0005_auto_20190212_2116'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='visibleTo',
            new_name='visible_to',
        ),
        migrations.AddField(
            model_name='post',
            name='content_type',
            field=models.CharField(choices=[('1', 'text/plain'), ('2', 'text/markdown'), ('3', 'image/png;base64'), ('4', 'image/jpeg;base64'), ('5', 'application/base64')], default='1', max_length=1),
        ),
        migrations.AddField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('1', 'PUBLIC'), ('2', 'FOAF'), ('3', 'FRIENDS'), ('4', 'PRIVATE'), ('5', 'SERVERONLY')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='hyperion.UserProfile'),
        ),
    ]
