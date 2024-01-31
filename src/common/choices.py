from django.db import models


class GenderStatus(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    UNKNOWN = "UNKNOWN", "Unknown"
    OTHER = "OTHER", "Other"
    
    
class UserType(models.TextChoices):
    APPLICANT = "APPLICANT", "Applicant"
    EMPLOYEE = "EMPLOYEE", "Employee"
    
    