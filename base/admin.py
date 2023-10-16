from django.contrib import admin
<<<<<<< HEAD
from .models import *
=======
from .models import Employee, AdvancedTravelPlan
>>>>>>> 15098e4d04a533c32af2b11be055d9040d63c1e3

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("Emp_name","email","contract_no","contract_start_date","contract_start_date")


class AdvancedTravelPlanAdmin(admin.ModelAdmin):
    list_display = ("employee","month","year","date_added")


admin.site.register(Employee,EmployeeAdmin)
<<<<<<< HEAD
admin.site.register(FlightBudget)
admin.site.register(OPEBudget)
admin.site.register(TravelBudget)
admin.site.register(Expense)
=======
admin.site.register(AdvancedTravelPlan,AdvancedTravelPlanAdmin)
>>>>>>> 15098e4d04a533c32af2b11be055d9040d63c1e3
