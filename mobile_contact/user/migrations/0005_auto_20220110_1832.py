# Generated by Django 3.2.7 on 2022-01-10 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_golbal_users_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='golbal_users',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
    ]
