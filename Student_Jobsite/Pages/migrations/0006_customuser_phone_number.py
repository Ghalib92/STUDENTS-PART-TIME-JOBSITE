# Generated by Django 5.2.1 on 2025-07-08 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pages', '0005_payrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
