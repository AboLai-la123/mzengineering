# Generated by Django 4.2.13 on 2024-05-15 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_order_order_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='violationCondition',
            field=models.BooleanField(default=False),
        ),
    ]
