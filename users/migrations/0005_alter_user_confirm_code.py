# Generated by Django 4.2 on 2024-04-09 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirm_code',
            field=models.CharField(default='093083', max_length=6, verbose_name='Код'),
        ),
    ]