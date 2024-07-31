# Generated by Django 5.0.7 on 2024-07-31 12:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_completed_date_studyhistory_completed_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyhistory',
            name='goal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.studygoal'),
        ),
        migrations.AlterField(
            model_name='studygroup',
            name='room_number',
            field=models.CharField(default='31e0ff261d1340bb8c8d05f168650946', max_length=255, unique=True),
        ),
    ]