# Generated by Django 2.0 on 2020-09-11 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FITaccreditation', '0002_userprofile_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_faculty',
            field=models.BooleanField(default=False),
        ),
    ]
