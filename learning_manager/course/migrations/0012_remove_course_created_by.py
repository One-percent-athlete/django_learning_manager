# Generated by Django 5.0.7 on 2024-07-17 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_course_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='created_by',
        ),
    ]