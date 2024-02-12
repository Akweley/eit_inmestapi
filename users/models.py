from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=1000)

class IMUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'first_name'  # Assuming first name as unique identifier
    REQUIRED_FIELDS = ['last_name']  # Other than first name, last name is required
    USER_TYPE = [
        ("EIT", "EIT"),
        ("TEACHING_FELLOW", "Teaching Fellow"),
        ("ADMIN_STAFF", "Admin Staff"),
        ("ADMIN", "Admin")
    ]

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Cohort(models.Model):
    name = models.CharField(max_length=100)
    year = models.DateTimeField()
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(IMUser, on_delete=models.CASCADE)


class CohortMember(models.Model):
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    member = models.ForeignKey(IMUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='cohort_member_author')