from django.contrib import admin
from .models import *

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("Emp_name","email","contract_no","contract_start_date","contract_start_date")


admin.site.register(Employee,EmployeeAdmin)
admin.site.register(FlightBudget)
admin.site.register(OPEBudget)
admin.site.register(TravelBudget)
admin.site.register(Expense)