# Generated by Django 3.1 on 2020-09-15 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbboard', '0003_auto_20200915_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='payment',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
