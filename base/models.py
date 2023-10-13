from django.db import models
import uuid
import os
# Create your models here.

class Employee(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)
    Emp_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    contract_no = models.CharField(unique=True,max_length=15,)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    phone_number = models.CharField(unique=True,max_length=10)
    state = models.CharField(max_length=30)
    duty_station = models.CharField(max_length=40)

    def __str__(self):
        return str(self.name)


def get_upload_path(instance,filename):
    return os.path.join('Advance Trip Plans/' +  str(instance.employee.Emp_name),filename)

class AdvancedTravelPlan(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    month = models.CharField(choices = [
        ('January', 'January'),
        ('February', 'February'),
        ('March' , 'March'),
        ('April','April'),
        ('May','May'),
        ('June','June'),
        ('July','July'),
        ('August','August'),
        ('September','September'),
        ('October','October'),
        ('November','November'),
        ('December','December')
    ],default = "January",max_length=10)
    year = models.CharField(max_length=20,default = "2023",null=True)
    date_added = models.DateField(auto_now_add=True)
    trip_plan = models.FileField(upload_to=get_upload_path)

    def __str__(self):
        return str(self.employee)


class FlightBudget(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)

