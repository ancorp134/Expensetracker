from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.db.models import Q
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
    search_query = request.GET.get('search_query', '')
    employees = Employee.objects.all()

    if search_query:
        employees = employees.filter(
            Q(Emp_name__icontains=search_query) |  # Search by employee name
            Q(contract_no__icontains=search_query) |  # Search by contract number
            Q(contract_start_date__icontains=search_query) |  # Search by start date
            Q(contract_end_date__icontains=search_query) |  # Search by end date
            Q(state__icontains=search_query) |  # Search by state
            Q(duty_station__icontains=search_query)  # Search by duty station
        )

    context = {
        'employees': employees,
        'search_query': search_query,
    }
    return render(request, 'employees.html', context)



@login_required(login_url='login')
def EmployeeProfileView(request, pk):
    try:
        employee = Employee.objects.get(uuid=pk)
        flight_budget, _ = FlightBudget.objects.get_or_create(employee=employee)
        travel_budget, _ = TravelBudget.objects.get_or_create(employee=employee)
        ope_budget, _ = OPEBudget.objects.get_or_create(employee=employee)
        remaining_budget_flight = float(flight_budget.allocated_budget) * 0.2
        remaining_budget_travel = float(travel_budget.allocated_budget) * 0.2
        remaining_budget_ope = float(ope_budget.allocated_budget) * 0.2
    except Employee.DoesNotExist:
        employee = None
        remaining_budget_flight = 0
        remaining_budget_travel = 0
        remaining_budget_ope = 0

    context = {
        'employee': employee,
        'flight_budget': flight_budget,
        'travel_budget': travel_budget,
        'ope_budget': ope_budget,
        'remaining_budget_flight': remaining_budget_flight,
        'remaining_budget_travel': remaining_budget_travel,
        'remaining_budget_ope': remaining_budget_ope,
    }
    return render(request, "profile.html", context)



@login_required(login_url='login')
def AdvancedTravelPlanView(request,pk):
    try:
        emp = Employee.objects.get(uuid=pk)
        
        atp = AdvancedTravelPlan.objects.filter(employee=emp)
        
    except:
        atp = None

    context = {
        'atp' : atp,
        'emp' : emp
    }
    
    return render(request,"advancedtravelplan.html",context)


@login_required(login_url='login')
def Search(request):
    search_query = request.GET.get('search_query')

    if search_query:
        employ = Employee.objects.filter( Q(Emp_name__icontains=search_query) | Q(contract_no__icontains=search_query))
    else:
        employ = Employee.objects.all()
    context = {
        'employ': employ,
        'search_query': search_query,
        }
    return render(request,'employees.html',context)


@login_required(login_url='login')
def ActualTravelPlan(request,pk):
    try:
        emp = Employee.objects.get(uuid=pk)
        tp = Expense.objects.filter(employee=emp)
        
    except:
        tp = None

    context = {
        'tp' : tp,
        'emp' : emp
    }
    
    return render(request,"actualtravelplan.html",context)

@login_required(login_url='login')
def ViewAtp(request,pk1,pk2):
    try:
        emp = Employee.objects.get(uuid=pk1)
        
        tp = Expense.objects.get(uuid=pk2)
        

    except:
        tp = None
    context = {
        'tp':tp,
        'emp':emp
    }
    return render(request,'viewatp.html',context)
        

