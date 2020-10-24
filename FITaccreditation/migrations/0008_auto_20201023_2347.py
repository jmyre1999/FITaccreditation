# Generated by Django 2.1.5 on 2020-10-24 03:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FITaccreditation', '0007_assignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='SatisfiedOutcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='advisor',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='assignee',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='course',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='outcome',
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(blank=True, choices=[('FA', 'Faculty'), ('AD', 'Advisor'), ('RE', 'Reviewer')], max_length=25),
        ),
        migrations.DeleteModel(
            name='Assignment',
        ),
        migrations.AddField(
            model_name='satisfiedoutcome',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FITaccreditation.Course'),
        ),
        migrations.AddField(
            model_name='satisfiedoutcome',
            name='outcome',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FITaccreditation.Outcome'),
        ),
    ]
