# Generated by Django 2.1.5 on 2020-10-21 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FITaccreditation', '0003_userprofile_is_faculty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('program', models.CharField(choices=[('CS', 'Computer Science'), ('SE', 'Software Engineering')], max_length=2)),
                ('code', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=1)),
                ('description', models.CharField(max_length=120)),
                ('program', models.CharField(choices=[('CS', 'Computer Science'), ('SE', 'Software Engineering')], max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='outcomes',
            field=models.ManyToManyField(blank=True, to='FITaccreditation.Outcome'),
        ),
    ]
