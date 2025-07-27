from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib import messages
from .models import Employee, Setter, Pay
from .forms import EmployeeForm, SetterForm, PayForm
from decimal import Decimal
from datetime import datetime

def home(request):
    return render(request, 'payroll_app/home.html')

def show_employees(request):
    employees = Employee.objects.all()
    return render(request, 'payroll_app/employee_list.html', {'employees': employees})

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Employee added successfully.")
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'payroll_app/add_employee.html', {'form': form})

def set_rates(request):
    if request.method == 'POST':
        form = SetterForm(request.POST)
        if form.is_valid():
            Setter.objects.all().delete()
            form.save()
            messages.success(request, "✅ Rates updated successfully.")
            return redirect('home')
    else:
        existing = Setter.objects.first()
        form = SetterForm(instance=existing)
    return render(request, 'payroll_app/set_rates.html', {'form': form})

def enter_salary(request):
    employees = Employee.objects.all()
    setter = Setter.objects.first()

    if not employees.exists():
        messages.warning(request, "⚠ No employee data available. Please add employees first.")
        return redirect('home')

    if not setter:
        messages.warning(request, "⚠ Please set DA and HRA rates first.")
        return redirect('set_rates')

    # Ensure Pay object exists for every employee
    for emp in employees:
        Pay.objects.get_or_create(ECODE=emp)

    PayFormSet = modelformset_factory(Pay, form=PayForm, extra=0)

    if request.method == 'POST':
        formset = PayFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)

            for inst in instances:
                emp = inst.ECODE

                # Set default values for missing fields
                inst.NODAYS = inst.NODAYS or 30
                inst.YEAR = inst.YEAR or datetime.now().year
                inst.OTHER_ALLW = inst.OTHER_ALLW or 0
                inst.ITAX = inst.ITAX or 0
                inst.LCFEE = inst.LCFEE or 0
                inst.ODEDUCT = inst.ODEDUCT or 0

                # Convert to Decimal
                basic = Decimal(emp.BASIC) / Decimal('30') * Decimal(inst.NODAYS)
                da = basic * Decimal(setter.DAP) / Decimal('100')
                data = Decimal(emp.TA) * Decimal(setter.DAP) / Decimal('100')
                hra = Decimal(emp.TA) * Decimal(setter.HRAP) / Decimal('100')
                nps_m = (basic + da) * Decimal('0.10')
                gross = basic + da + data + hra + nps_m + Decimal(inst.OTHER_ALLW)
                nps_o = nps_m
                gpf = basic * Decimal('0.06')
                total_deduc = Decimal(inst.ITAX) + nps_m + nps_o + gpf + Decimal(inst.ODEDUCT) + Decimal(inst.LCFEE)
                netsal = gross - total_deduc

                # Save values to DB
                inst.DA = int(da)
                inst.DATA = int(data)
                inst.HRA = int(hra)
                inst.NPS_M = int(nps_m)
                inst.GROSS = int(gross)
                inst.NPS_O = int(nps_o)
                inst.GPF = int(gpf)
                inst.TOT_DEDUC = int(total_deduc)
                inst.NETSAL = int(netsal)
                inst.save()

            messages.success(request, "✅ Salary data saved successfully.")
            return redirect('view_salary')
    else:
        formset = PayFormSet(queryset=Pay.objects.all())

    return render(request, 'payroll_app/enter_salary.html', {'formset': formset})

def view_salary(request):
    salaries = Pay.objects.select_related('ECODE').all()
    return render(request, 'payroll_app/view_salary.html', {'salaries': salaries})

