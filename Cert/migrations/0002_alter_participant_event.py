# Generated by Django 5.1.4 on 2025-01-04 14:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cert', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant_records', to='Cert.event'),
        ),
    ]
