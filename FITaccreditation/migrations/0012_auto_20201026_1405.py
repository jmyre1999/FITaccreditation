# Generated by Django 2.1.5 on 2020-10-26 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FITaccreditation', '0011_artifact_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outcome',
            name='description',
            field=models.CharField(max_length=300),
        ),
    ]
