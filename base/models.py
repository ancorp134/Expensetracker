from django.db import models
import uuid
# Create your models here.

class Employee(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    contract_no = models.CharField(unique=True,max_length=15,)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    phone_number = models.CharField(unique=True,max_length=10)
    state = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)