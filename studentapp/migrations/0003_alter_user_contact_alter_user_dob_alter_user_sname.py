# Generated by Django 5.1 on 2024-10-15 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentapp', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='sname',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
