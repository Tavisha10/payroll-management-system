from django import forms
from .models import Employee, Setter, Pay
import re

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'DOB': forms.DateInput(attrs={'type': 'date'}),
            'DOJ': forms.DateInput(attrs={'type': 'date'}),
            'MOB': forms.TextInput(attrs={'placeholder': 'e.g. 9876543210'}),
            'PAN': forms.TextInput(attrs={'placeholder': 'e.g. ABCDE1234F'}),
            'EMAIL': forms.EmailInput(attrs={'placeholder': 'e.g. user@example.com'}),
            'GENDER': forms.Select(attrs={'class': 'form-select'}),
        }
        def clean_MOB(self):
            mob = self.cleaned_data['MOB'].strip()

            # Remove all non-digit characters
            digits = re.sub(r'\D', '', mob)

            # If it starts with '91' and is 12+ digits, assume it's already formatted
            if digits.startswith('91') and len(digits) >= 12:
                return f"+{digits}"

            # If it's exactly 10 digits, assume it's an Indian number and add +91
            if len(digits) == 10:
                return f"+91{digits}"

            raise forms.ValidationError("Enter a valid 10-digit mobile number (Indian format)")
        def clean_PAN(self):
            pan = self.cleaned_data['PAN'].strip().upper()
            if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan):
                raise forms.ValidationError("Enter a valid PAN (e.g., ABCDE1234F)")
            return pan

        def clean(self):
            cleaned_data = super().clean()
            email = cleaned_data.get("EMAIL")
            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                self.add_error("EMAIL", "Enter a valid email address")
            return cleaned_data



class SetterForm(forms.ModelForm):
    class Meta:
        model = Setter
        fields = '__all__'


class PayForm(forms.ModelForm):
    class Meta:
        model = Pay
        exclude = [
            'DA', 'DATA', 'HRA', 'NPS_M', 'GROSS',
            'NPS_O', 'GPF', 'TOT_DEDUC', 'NETSAL'
        ]
        widgets = {
            'YEAR': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2024',
                'min': 2000,
                'max': 2100
            }),
            'NODAYS': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 22',
                'min': 0,
                'max': 31}),
            'OTHER_ALLW': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter additional allowance if any',
            'min': 0
            }),
        }
        def clean_YEAR(self):
            val = self.cleaned_data.get('YEAR')
            from datetime import datetime
            return val if val is not None else datetime.now().year
        def clean_NODAYS(self):
            nodays = self.cleaned_data.get('NODAYS')
            if nodays is None or nodays < 0:
                raise forms.ValidationError("Number of days cannot be empty or negative.")
            return nodays
        def clean_OTHER_ALLW(self):
            value = self.cleaned_data.get('OTHER_ALLW')
            if value is None:
                raise forms.ValidationError("Please enter Other Allowance (use 0 if none).")
            return value
        def clean_ITAX(self):
            val = self.cleaned_data.get('ITAX')
            if val is None:
                return 0  # Default fallback
            return val
        def clean_ODEDUCT(self):
            val = self.cleaned_data.get('ODEDUCT')
            return val if val is not None else 0
        def clean_LCFEE(self):
            val = self.cleaned_data.get('LCFEE')
            return val if val is not None else 0