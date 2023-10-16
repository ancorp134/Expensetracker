from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

# Create your views here.

def loginview(request):
    
    if request.user.is_authenticated:
        return redirect('employees')

    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            context ={'user': user}
            return redirect(reverse('employees'),context)
        
        messages.error(request,"Invalid credentials")
        return render(request,"login.html")

    return render(request,"login.html")

@login_required(login_url='login')
def logoutview(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def EmployeeView(request):
    try:
        employees = Employee.objects.all()
        context = {
            'employees' : employees
        }
    except:
        pass
    return render(request,'employees.html',context)


def EmployeeProfileView(request,pk):
    flight_budget=0
    travel_budget=0
    ope_budget=0
    try:
        employee = Employee.objects.get(id=pk)
        flight_budget = FlightBudget.objects.get(employee=employee)
        travel_budget = TravelBudget.objects.get(employee=employee)
        ope_budget = OPEBudget.objects.get(employee=employee)
    except:
        pass
    context = {
        'flight_budget' : flight_budget,
        'travel_budget' : travel_budget,
        'ope_budget' : ope_budget
    }
    return render(request,"profile.html",context) 