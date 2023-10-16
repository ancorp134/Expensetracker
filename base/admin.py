from django.contrib import admin
from .models import Employee, AdvancedTravelPlan

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("Emp_name","email","contract_no","contract_start_date","contract_start_date")


class AdvancedTravelPlanAdmin(admin.ModelAdmin):
    list_display = ("employee","month","year","date_added")


admin.site.register(Employee,EmployeeAdmin)
admin.site.register(AdvancedTravelPlan,AdvancedTravelPlanAdmin)
