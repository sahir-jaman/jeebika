from django.contrib import admin
from applicants.models import Applicant
from employees.models import Employee, job_post, service_type, category, Industry_type
from .models import User


# Register your models here.
admin.site.register(User)
admin.site.register(Applicant)
admin.site.register(Industry_type)
admin.site.register(Employee)
admin.site.register(category)
admin.site.register(service_type)
admin.site.register(job_post)