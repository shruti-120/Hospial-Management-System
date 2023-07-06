from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, time

def current_date():
    return datetime.now().date()

department_choice=(
        ('cardiology','cardiology'),
        ('dermatology','dermatology'),('pediatrics','pediatrics'),
        ('neurology','neurology'),('gastroenterology','gastroenterology'),
        ('eye-centre','eye-centre'),('ear-nose-throat','ear-nose-throat'),
        ('urology','urology'),('oncology','oncology')
    )

class UserWithUserType(models.Model):
    role_choice=(
        ('patient','patient'),
        ('doctor','doctor')
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    specialist_in = models.CharField(max_length=50,null=True,blank=True,choices=department_choice)
    medical_history = models.TextField(null=True,blank=True)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=3,null=True,blank=True)
    address = models.CharField(max_length=50,null=True,blank=True)
    date_of_birth = models.DateField(max_length=100,null=True,blank=True)
    phone_number = models.CharField(max_length=10, blank=True, unique=True,null=True)
    role= models.CharField(max_length=50,choices=role_choice,null=True)

    def __str__(self):
        return self.username

class Appointment(models.Model):
    department = models.CharField(max_length=50, choices=department_choice)
    doctor = models.ForeignKey(UserWithUserType, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'},default=1, related_name='doctor_appointments')
    appointment_date = models.DateField(default=current_date)
    time_slot = models.CharField(max_length=10,blank=False, null=False)
    patient = models.ForeignKey(UserWithUserType, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'}, related_name='patient_appointment',default=2)
    waitlisted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.department} - {self.appointment_date} {self.time_slot} Patient: {self.patient.first_name} {self.patient.last_name}"
        
class Feedback(models.Model):
    doctor = models.ForeignKey(UserWithUserType, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'},related_name='doctor_feedback')
    patient = models.ForeignKey(UserWithUserType, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'}, related_name='patient_feedback')
    rating = models.IntegerField(blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    response = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)











