from django import forms
from . import models
from django.forms import SelectDateWidget
import datetime

class PatientUserForm(forms.ModelForm):
    class Meta:
        model=models.UserWithUserType
        fields='__all__'
        exclude=['specialist_in']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'gender': forms.TextInput(attrs={'placeholder': 'Enter your gender'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date','placeholder': 'Enter your DOB'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'})
        }

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=models.UserWithUserType
        fields='__all__'
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'gender': forms.TextInput(attrs={'placeholder': 'Enter your gender'}),
            'specialist_in': forms.TextInput(attrs={'placeholder': 'Enter your speciality'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date','placeholder': 'Enter your DOB'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'})
            
        }

class TimeslotForm(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields = ['time_slot','waitlisted']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields = '__all__'
        exclude=['time_slot']
    
    department = forms.ChoiceField(choices=models.department_choice, widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = models.UserWithUserType.objects.filter(role='doctor')

        self.fields['department'].widget.choices.insert(0, ('', '---------'))
      
        if 'department' in self.data:
            department = self.data['department']
            self.fields['department'].initial = department
            self.fields['doctor'].queryset = models.UserWithUserType.objects.filter(specialist_in=department, role='doctor')

        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = '__all__'
        
