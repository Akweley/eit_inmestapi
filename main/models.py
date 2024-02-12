from django.db import models

from users.models import Cohort, IMUser

# Create your models here.
class ClassSchedule(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date_and_time = models.DateTimeField()
    end_date_and_time = models.DateTimeField()
    is_repeated = models.BooleanField(default=False)
    repeat_frequency = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    organizer = models.CharField(max_length=50)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    venue = models.TextField()


class ClassAttendance(models.Model):
    class_schedule = models.CharField(max_length=50)
    description = models.TextField()
    start_date_and_time = models.DateTimeField()
    end_date_and_time = models.DateTimeField()
    is_repeated = models.BooleanField(default=False)
    repeat_frequency = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    organizer =models.CharField(max_length=50)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    venue = models.TextField()