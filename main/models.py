from django.db import models
from users.models import *

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default ="N/A", blank = True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank = True, null=True)
    date_modified = models.DateTimeField(auto_now=True,  blank = True, null=True)

    def __str__(self):
        return f"{self.name}"
    

class ClassSchedule(models.Model):
    REPEAT_FREQUENCIES = (
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    )
    MEETING_TYPES = (
        ('CLASS_SESSION', 'Class Session'),
        ('WELLNESS_SESSION', 'Wellness Session'),
        ('GUEST_LECTURE', 'Guest Lecture'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date_and_time = models.DateTimeField()
    end_date_and_time = models.DateTimeField()
    is_repeated = models.BooleanField(default=False)
    repeat_frequency = models.CharField(max_length=20, choices=REPEAT_FREQUENCIES, blank=True, null=True)
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    organizer = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name="organizer")
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, blank=True, null=True, related_name="class_schedule")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, related_name="course")
    facilitator = models.ForeignKey(IMUser, on_delete=models.SET_NULL, blank=True, null=True, related_name="facilitator")
    venue = models.TextField(max_length=225, blank=True)

    def __str__(self):
        return f"{self.title}(Submitted by: {self.cohort.name})"


class ClassAttendance(models.Model):
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    attendee = models.ForeignKey(IMUser, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    author = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='class_attendance_author')


class Query(models.Model):
    RESOLUTION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('DECLINED', 'Declined'),
        ('RESOLVED', 'Resolved')
    ]

    QUERY_TYPES = (
        ("FACILITY", "Facility"),
        ("LOGISTICS", "Logistics"),
        ("KITCHEN", "Kitchen"),
        ("IT", "IT"),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    submitted_by = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='query_submitter')
    assigned_to = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='query_assignee')
    resolution_status = models.CharField(max_length=50, choices=RESOLUTION_STATUS_CHOICES)
    query_type = models.CharField(max_length=30, choices=QUERY_TYPES, default='FACILITY', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='query_author')


class QueryComment(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='query_comment_author')
