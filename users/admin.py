from django.contrib import admin
from .models import IMUser, Cohort, CohortMember
from main.models import Course

# Register your models here.


admin.site.register(Course)
admin.site.register(IMUser)
admin.site.register(Cohort)
admin.site.register(CohortMember)