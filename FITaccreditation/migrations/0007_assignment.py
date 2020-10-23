# Generated by Django 2.1.5 on 2020-10-23 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FITaccreditation', '0006_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('due_date', models.DateTimeField()),
                ('complete', models.BooleanField(default=False)),
                ('date_completed', models.DateTimeField(blank=True)),
                ('advisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment_advisor', to=settings.AUTH_USER_MODEL)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment_assignee', to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FITaccreditation.Course')),
                ('outcome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FITaccreditation.Outcome')),
            ],
        ),
    ]
