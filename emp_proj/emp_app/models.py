from django.db import models

# Create your models here.
class Employee(models.Model):
    eid=models.CharField(max_length=120,primary_key=True)
    profile_pic=models.ImageField(upload_to="profilepics",null=True)
    employee_name=models.CharField(max_length=120)
    designation = models.CharField(max_length=120)
    salary = models.IntegerField()
    email=models.EmailField(unique=True)
    experience=models.PositiveIntegerField(null=True)  #null value canbe possible

    def __str__(self):
        return self.employee_name