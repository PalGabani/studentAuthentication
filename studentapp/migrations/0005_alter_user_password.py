# Generated by Django 5.1 on 2024-10-17 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentapp', '0004_alter_user_managers_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(),
        ),
    ]
