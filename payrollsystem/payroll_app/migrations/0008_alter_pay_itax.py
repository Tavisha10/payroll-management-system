# Generated by Django 5.2.4 on 2025-07-21 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0007_alter_pay_other_allw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pay',
            name='ITAX',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Income Tax'),
        ),
    ]
