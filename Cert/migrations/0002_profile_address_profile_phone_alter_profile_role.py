# Generated by Django 5.1.4 on 2024-12-16 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cert', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('club', 'Club'), ('mentor', 'Mentor')], default='student', max_length=20),
        ),
    ]
