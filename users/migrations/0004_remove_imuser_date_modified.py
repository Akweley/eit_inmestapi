# Generated by Django 5.0.1 on 2024-02-15 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_course_remove_imuser_date_updated_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imuser',
            name='date_modified',
        ),
    ]
