from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from common.models import BaseModelWithUID
from accountio.models import UserManager
from accountio.models import User

# Create your models here.
class Employee(AbstractBaseUser, BaseModelWithUID):
    name = models.CharField(max_length=200, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='employee')
    designation = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_exp = models.PositiveIntegerField(blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    company_size = models.PositiveIntegerField(blank=True, null=True)
    industry_type = models.CharField(max_length=100,blank=True, null=True)  # we'll need a category choice field here.
    business_desc= models.TextField(blank=True, null=True)
    trade_number = models.PositiveIntegerField(blank=True, null=True)
    rl_number = models.PositiveIntegerField(blank=True, null=True)
    web_url = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return self.name
    

class category(BaseModelWithUID):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
    
    
class service_type(models.Model):
    service = models.CharField(max_length=100)
    
    def __str__(self):
        return self.service
    
      
class job_post(BaseModelWithUID):
    category = models.ForeignKey(category, max_length=100, on_delete=models.CASCADE)
    service_type = models.ForeignKey(service_type, max_length=100, on_delete=models.CASCADE)
    company_title = models.CharField(max_length=200)
    designation = models.CharField(max_length=100, null=True, blank=True)
    vacancy = models.PositiveIntegerField(null=True, blank=True)
    published = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    skill = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    requirements= models.TextField(null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    expertise = models.CharField(max_length=200,null=True, blank=True)
    employment_status = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    company_info = models.CharField(max_length=100, null=True, blank=True)
    compensation = models.CharField(max_length=100, null=True, blank=True)
    apply_procedure = models.CharField(max_length=100, null=True, blank=True)
    
    
    def __str__(self):
        return self.company_title
    