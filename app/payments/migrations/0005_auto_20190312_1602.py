# Generated by Django 2.1.7 on 2019-03-12 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_auto_20190312_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transferfundsorder',
            name='conversion_rate',
        ),
        migrations.AddField(
            model_name='transferfundsordertransaction',
            name='conversion_rate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='payments.CurrencyConversionRate'),
        ),
    ]