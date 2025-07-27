from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('employees/', views.show_employees, name='employee_list'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('set-rates/', views.set_rates, name='set_rates'),
    path('enter-salary/', views.enter_salary, name='enter_salary'),
    path('view-salary/', views.view_salary, name='view_salary'),
]