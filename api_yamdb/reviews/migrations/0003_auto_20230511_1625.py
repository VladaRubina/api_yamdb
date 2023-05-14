# Generated by Django 3.2 on 2023-05-11 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230511_1618'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='***', max_length=255, null=True, verbose_name='код подтверждения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('admin', 'admin'), ('moderator', 'moderator')], default='user', max_length=255, verbose_name='Группа пользователей'),
        ),
    ]