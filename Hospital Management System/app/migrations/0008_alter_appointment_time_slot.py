# Generated by Django 3.2.12 on 2023-06-17 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_appointment_time_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time_slot',
            field=models.CharField(default='09:00 AM', max_length=10),
        ),
    ]
