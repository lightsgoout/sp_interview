# Generated by Django 2.1.7 on 2019-03-12 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20190312_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaccount',
            name='number',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
