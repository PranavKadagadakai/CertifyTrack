# Generated by Django 5.1.4 on 2025-01-05 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cert', '0004_alter_profile_mentor_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]