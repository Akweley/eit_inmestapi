# Generated by Django 5.0.1 on 2024-03-12 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_classschedule_course_classschedule_facilitator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='query_type',
            field=models.CharField(blank=True, choices=[('FACILITY', 'Facility'), ('LOGISTICS', 'Logistics'), ('KITCHEN', 'Kitchen'), ('IT', 'IT')], default='FACILITY', max_length=30, null=True),
        ),
    ]
