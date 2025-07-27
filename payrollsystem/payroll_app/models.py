from django.db import models
from datetime import datetime

class Employee(models.Model):
    ECODE = models.CharField(primary_key=True, max_length=10, verbose_name="Employee Code")
    FNAME = models.CharField(max_length=30, verbose_name="First Name")
    LNAME = models.CharField(max_length=30, verbose_name="Last Name")
    DESIG = models.CharField(max_length=50, verbose_name="Designation")
    DOB = models.DateField(verbose_name="Date of Birth")
    DOJ = models.DateField(verbose_name="Date of Joining")
    MOB = models.CharField(max_length=20, verbose_name="Mobile Number")
    PAN = models.CharField(max_length=10, verbose_name="PAN Number")
    TA = models.IntegerField(verbose_name="Travel Allowance")
    BASIC = models.IntegerField(verbose_name="Basic Salary")
    EMAIL = models.EmailField(verbose_name="Email Address", max_length=254, blank=True)
    LEVEL = models.CharField(max_length=20, verbose_name="Job Level", blank=True)
    GENDER_CHOICES = [('Male', 'Male'),('Female', 'Female'),('Other', 'Other'),]
    GENDER = models.CharField(max_length=10,choices=GENDER_CHOICES,verbose_name="Gender", default= 'Other')



    def __str__(self):
        return f"{self.FNAME} {self.LNAME} ({self.ECODE})"

class Setter(models.Model):
    DAP = models.FloatField(verbose_name="DA Percentage")
    HRAP = models.FloatField(verbose_name="HRA Percentage")

    def __str__(self):
        return f"DA: {self.DAP}%, HRA: {self.HRAP}%"

class Pay(models.Model):
    ECODE = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    MONTH = models.CharField(max_length=15)
    YEAR = models.IntegerField(verbose_name="Year", default= datetime.now().year)
    NODAYS = models.IntegerField(verbose_name='Number of Days Worked', null=True, blank=True)
    OTHER_ALLW = models.FloatField(null=True, blank=True, default=0, verbose_name="Other Allowance")
    ITAX = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0, verbose_name="Income Tax")
    ODEDUCT = models.FloatField(null=True, blank=True, default=0,verbose_name="Other Deductions")
    LCFEE = models.FloatField(null=True, blank=True, default=0,verbose_name="Late/Convenience Fee")

    # Calculated fields
    DA = models.FloatField(default=0)
    DATA = models.FloatField(default=0)
    HRA = models.FloatField(default=0)
    GROSS = models.FloatField(default=0)
    NPS_M = models.FloatField(default=0)
    NPS_O = models.FloatField(default=0)
    GPF = models.FloatField(default=0)
    TOT_DEDUC = models.FloatField(default=0)
    NETSAL = models.FloatField(default=0)

    def __str__(self):
        return f"{self.ECODE} - {self.MONTH} {self.YEAR}"
