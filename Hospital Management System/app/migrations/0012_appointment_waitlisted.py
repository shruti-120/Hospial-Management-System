# Generated by Django 3.2.12 on 2023-06-20 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_userwithusertype_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='waitlisted',
            field=models.BooleanField(default=False),
        ),
    ]
