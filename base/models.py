from django.db import models
import uuid
import os
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
        return str(self.Emp_name)

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
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, null = True)
    allocated_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)
    from_date = models.DateField(null = True)
    to_date = models.DateField(null = True)
    remaining_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)



class Expense(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null = True)
    from_date = models.DateField(null = True)
    to_date = models.DateField(null = True)
    ope_budget_used = models.DecimalField(decimal_places=2,default=0,max_digits = 10)
    travel_budget_used = models.DecimalField(decimal_places=2,default=0,max_digits = 10)
    flight_budget_used = models.DecimalField(decimal_places=2,default=0,max_digits = 10)
    flight_ticket = models.FileField(upload_to=get_upload_path, blank = True)
    flight_return_ticket = models.FileField(upload_to=get_upload_path, blank = True)
    train_ticket = models.FileField(upload_to=get_upload_path, blank = True)
    train_return_ticket = models.FileField(upload_to=get_upload_path, blank = True)
    local_conveyance = models.DecimalField(decimal_places=2,default=0,max_digits = 10)
    departure = models.CharField(max_length = 30,null = True)
    place_of_visit = models.CharField(max_length = 30,null = True)
    taxi_bill = models.DecimalField(max_digits=10, decimal_places=2,default = 0)
    taxi_bill_proof = models.FileField(upload_to=get_upload_path, blank = True)

class OPEBudget(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, null = True)
    allocated_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)
    from_date = models.DateField(null = True)
    to_date = models.DateField(null = True)
    remaining_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)

class TravelBudget(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, null = True)
    allocated_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)
    from_date = models.DateField(null = True)
    to_date = models.DateField(null = True)
    remaining_budget = models.DecimalField(decimal_places=2,default = 0,max_digits = 10)

    

def update_budgets(sender, instance, created, **kwargs):
    if created:
        # If a new Expense object is created, update the budgets
        employee = instance.employee

        flight_budget, _ = FlightBudget.objects.get_or_create(employee=employee)
        flight_budget.remaining_budget -= instance.flight_budget_used
        flight_budget.save()

        # Update TravelBudget
        travel_budget, _ = TravelBudget.objects.get_or_create(employee=employee)
        travel_budget.remaining_budget -= instance.travel_budget_used
        travel_budget.remaining_budget -= instance.taxi_bill
        travel_budget.save()

        # Update OPEBudget
        ope_budget, _ = OPEBudget.objects.get_or_create(employee=employee)
        ope_budget.remaining_budget -= instance.ope_budget_used
        ope_budget.remaining_budget -= instance.local_conveyance
        ope_budget.save()


post_save.connect(update_budgets, sender=Expense)





@receiver(pre_save, sender=Expense)
def update_budgets_on_expense_change(sender, instance, **kwargs):
    # Check if the instance is being created (it doesn't have a primary key yet)
    if instance._state.adding:
        employee = instance.employee

        # Update FlightBudget for new expenses
        flight_budget, _ = FlightBudget.objects.get_or_create(employee=employee)
        flight_budget.remaining_budget -= instance.flight_budget_used
        flight_budget.save()

        # Update TravelBudget for new expenses
        travel_budget, _ = TravelBudget.objects.get_or_create(employee=employee)
        travel_budget.remaining_budget -= instance.travel_budget_used
        travel_budget.remaining_budget -= instance.taxi_bill
        travel_budget.save()

        # Update OPEBudget for new expenses
        ope_budget, _ = OPEBudget.objects.get_or_create(employee=employee)
        ope_budget.remaining_budget -= instance.ope_budget_used
        ope_budget.remaining_budget -= instance.local_conveyance
        ope_budget.save()
    else:
        try:
            original_expense = Expense.objects.get(pk=instance.pk)

            # Calculate the difference between the original and new expense amount
            diff_flight = original_expense.flight_budget_used - instance.flight_budget_used
            diff_travel = original_expense.travel_budget_used - instance.travel_budget_used
            diff_ope = original_expense.ope_budget_used - instance.ope_budget_used
            diff_local_con = original_expense.local_conveyance - instance.local_conveyance
            diff_taxi_bill = original_expense.taxi_bill - instance.taxi_bill

            # Update the budget based on the difference
            employee = instance.employee

            # Update FlightBudget for updated expenses
            flight_budget, _ = FlightBudget.objects.get_or_create(employee=employee)
            flight_budget.remaining_budget += diff_flight
            flight_budget.save()

            # Similar updates for TravelBudget and OPEBudget
            travel_budget, _ = TravelBudget.objects.get_or_create(employee=employee)
            travel_budget.remaining_budget += diff_travel
            travel_budget.remaining_budget += diff_taxi_bill
            travel_budget.save()

            # Update OPEBudget for updated expenses
            ope_budget, _ = OPEBudget.objects.get_or_create(employee=employee)
            ope_budget.remaining_budget += diff_ope
            ope_budget.remaining_budget += diff_local_con
            ope_budget.save()



            
            # You can calculate utilization percentages and send emails here as well if needed
            smtp_server = 'smtp.gmail.com'
            smtp_port = 465  # The port number for SSL
            smtp_username = 'inductus.un@gmail.com'
            smtp_password = 'eqjzucqlyzwzvfxr'
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp_conn:
    # Log in to your email account
                smtp_conn.login(smtp_username, smtp_password)

    # Create an email message
                subject = f'Budget Utilization Alert for Employee: {employee.Emp_name}'
                body = f'Employee {employee.Emp_name} has exceeded the 70% budget utilization threshold.'
                sender_email = 'inductus.un@gmail.com'
                recipient_email = 'brijesh.sharma@inductusgroup.com'

                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

    # Send the email
    


                flight_budget_utilization = (flight_budget.allocated_budget - flight_budget.remaining_budget) / flight_budget.allocated_budget
                travel_budget_utilization = (travel_budget.allocated_budget - travel_budget.remaining_budget) / travel_budget.allocated_budget
                ope_budget_utilization = (ope_budget.allocated_budget - ope_budget.remaining_budget) / ope_budget.allocated_budget

                if (flight_budget_utilization >= 0.7 or travel_budget_utilization >= 0.7 or ope_budget_utilization >= 0.7):
                   

                    smtp_conn.sendmail(sender_email, [recipient_email], msg.as_string())

        except ObjectDoesNotExist:
            # Handle the case where the original expense does not exist
            pass

pre_save.connect(update_budgets_on_expense_change, sender=Expense)


