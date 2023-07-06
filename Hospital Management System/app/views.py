from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth, Group
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from app.decorators import *
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
# ------------------------------------------GENRAL VIEWS------------------------------------------------------
def Index(request):
    return render(request,'index.html')

def Login(request):

    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            role=UserWithUserType.objects.get(username=username).role
            if role=="doctor":
                return redirect('doctor_home')

            elif role=="patient":
                return redirect('patient_home')
            # import pdb;pdb.set_trace()
            else:
                return redirect('index')
        
    context = {}
    return render(request,'login.html', context)

def Logout(request):
    logout(request)
    return render(request,'index.html')


def user_signup(request,role):
    if role=='patient':
        form=forms.PatientUserForm(request.POST or None)

    elif role=='doctor':
        form=forms.DoctorUserForm(request.POST or None)
    
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        if form.is_valid():
            user=User.objects.create(
                username=form.cleaned_data.get('username'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=form.cleaned_data.get('email'),
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            form.save()
            messages.success(request,"Account was created ")
            return redirect('login')  
    
    form.fields['role'].initial = role          
    mydict={'form':form, 'role':role}
    return render(request, 'user_signup.html', context=mydict)


def doctor_list(request):
    doctors = UserWithUserType.objects.filter(role='doctor')
    
    for doctor in doctors:
        feedbacks = Feedback.objects.filter(doctor=doctor)
        ratings = [feedback.rating for feedback in feedbacks if feedback.rating is not None]
        if ratings:
            average_rating = sum(ratings) / len(ratings)
        else:
            average_rating = 0

        if average_rating == 0:
            given_by = 0
        else:
            given_by = len(ratings)
        
        doctor.average_rating = average_rating
        doctor.given_by = given_by
    
    context = {'doctors': doctors }
    return render(request, 'doctor_list.html', context)

def departments(request):
    return render(request,'departments.html')


def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')



# ----------------------------------DOCTOR RELATED VIEWS--------------------------------------------------


@doctor_required
def doctor_home(request):
    doctor= UserWithUserType.objects.get(username=request.user.username)
    doctor_appointments = Appointment.objects.filter(doctor=doctor)
    context = {'doctor_appointments': doctor_appointments}
    return render(request,'doctor_home.html', context)


@doctor_required
def doctor_profile(request):
    doctor = UserWithUserType.objects.get(username=request.user.username, role='doctor')
    context = {'doctor': doctor}
    return render(request, 'doctor_profile.html', context)


@doctor_required
def doctor_patients(request):
    doctor= UserWithUserType.objects.get(username=request.user.username)
    doctor_appointments = Appointment.objects.filter(doctor=doctor)
    patients = list(set(appointment.patient for appointment in doctor_appointments))
    male_count = 0
    female_count = 0

    for patient in patients:
        if patient.gender == 'M':
            male_count += 1
        elif patient.gender == 'F':
            female_count += 1

    gender_list = ['Male', 'Female']
    gender_count = [male_count, female_count]
    print(male_count)
    context = {'doctor': doctor, 'patients': patients, 'gender_list': gender_list, 'gender_count': gender_count}
    return render(request, 'doctor_patients.html', context)


@doctor_required
def edit_doctor_profile(request):
    doctor = UserWithUserType.objects.get(username=request.user.username, role='doctor')
    form = forms.DoctorUserForm(request.POST or None,instance=doctor)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('doctor_profile')

        else:
            print(form.errors)
            
    context = {'form': form}
    return render(request, 'edit_doctor_profile.html', context)


@doctor_required
def doctor_feedback(request):
    doctor= UserWithUserType.objects.get(username=request.user.username)
    feedbacks = Feedback.objects.filter(doctor=doctor)
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        response = request.POST.get('response')
        feedback = get_object_or_404(Feedback, id=feedback_id, doctor=doctor)
        feedback.response = response
        feedback.save()
        return redirect('doctor_feedback')

    context = {'doctor': doctor, 'feedbacks': feedbacks}
    return render(request, 'doctor_feedback.html', context)



# -------------------------------------PATIENT RELATED VIEWS-----------------------------------------------


@patient_required
def patient_home(request):
    patient= UserWithUserType.objects.get(username=request.user.username)
    patient_appointments = Appointment.objects.filter(patient=patient)
    context = {'patient_appointments': patient_appointments}
    return render(request,'patient_home.html',context)


@patient_required
def patient_feedback(request):
    patient= UserWithUserType.objects.get(username=request.user.username)
    form = forms.FeedbackForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('patient_home')
    
    print(form.errors)
    return render(request, 'patient_feedback.html', {"form":form, 'patient': patient,})


@patient_required
def patient_view_feedback(request):
    patient= UserWithUserType.objects.get(username=request.user.username)
    feedbacks = Feedback.objects.filter(patient=patient)
    context = {'patient': patient, 'feedbacks': feedbacks}
    return render(request,'patient_view_feedback.html', context)


@patient_required
def patient_appointment(request):
    patient= UserWithUserType.objects.get(username=request.user.username)
    patient_appointments = Appointment.objects.filter(patient=patient)

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = Appointment.objects.filter(id=appointment_id).first()
        if appointment:
            appointment.delete()
            notify_waitlisted()
        return redirect('patient_appointment')
        
    context = {'patient_appointments': patient_appointments}
    return render(request, 'patient_appointment.html', context)

    
@patient_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    form = forms.AppointmentForm(request.POST or None, instance=appointment)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            notify_waitlisted()
            return redirect('patient_appointment')

    context = {'form': form}
    return render(request, 'edit_appointment.html', context)


@patient_required
def book_appointment(request):
    form = forms.AppointmentForm(request.POST or None)
    patient = UserWithUserType.objects.get(username=request.user.username)
    
    if request.method == 'POST':
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.department = form.cleaned_data.get('department')
            appointment.save()
            request.session['appointment_id'] = appointment.id  
            return redirect('select_time') 
    else:
        print(form.errors)

    context = {
        'form': form,
        'patient': patient,
    }
    return render(request, 'book_appointment.html', context)


@patient_required
def select_time(request):
    appointment_id = request.session.get('appointment_id')
    appointment = Appointment.objects.get(id=appointment_id)  
    patient = UserWithUserType.objects.get(username=request.user.username)
    timeslot_form = forms.TimeslotForm(request.POST, instance=appointment)


    date = appointment.appointment_date
    doctor = appointment.doctor
    booked_appointments = Appointment.objects.filter(doctor=doctor, appointment_date=date)
    booked_time_slots = list(set(appointment.time_slot for appointment in booked_appointments))
    all_time_slots = ['09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM',
                      '12:30 PM', '01:00 PM', '01:30 PM', '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM',
                      '04:00 PM', '04:30 PM', '05:00 PM', '05:30 PM', '06:00 PM', '06:30 PM', '07:00 PM']
    available_time_slots = [slot for slot in all_time_slots if slot not in set(booked_time_slots)]

    if request.method == 'POST':
        print(timeslot_form.is_valid())
        if timeslot_form.is_valid():
            appointment = timeslot_form.save(commit=False)
            if appointment.time_slot in booked_time_slots:
                appointment.waitlisted = True
            appointment.patient = patient
            appointment.save()
            return redirect('patient_home')

        
    # print(available_time_slots)
    context = {
        'timeslot_form': timeslot_form,
        'patient': patient,
        'appointment': appointment,
        'available_time_slots': available_time_slots,
        'booked_time_slots':booked_time_slots
    }
    return render(request, 'select_time.html', context)

def notify_waitlisted():
    available_appointment = Appointment.objects.filter(waitlisted=True).first()

    if available_appointment:
        waitlisted_patients = Appointment.objects.filter(appointment_date=available_appointment.appointment_date,
                                                         time_slot=available_appointment.time_slot,
                                                         waitlisted=True)
        for patient in waitlisted_patients:
            subject = "Appointment Available"
            message = f"An appointment is available on {available_appointment.appointment_date} at {available_appointment.time_slot}. Book now!"
            from_email = "shrutisuman120@gmail.com" 
            to_email = ["shrutisuman120@gmail.com"]  
            send_mail(subject, message, from_email, to_email)

        available_appointment.waitlisted = False
        available_appointment.save()

    return redirect('patient_home')
# @patient_required
# def book_appointment(request):
#     form = forms.AppointmentForm(request.POST or None)
#     patient = UserWithUserType.objects.get(username=request.user.username)

#     if request.method == 'POST':
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             # appointment.user = request.user
#             appointment.patient = patient
#             appointment.save()
#             return redirect('patient_home')
#         else:
#             print(form.errors)

#     context = {'form': form, 'patient': patient}
#     return render(request, 'book_appointment.html', context)


# def book_appointment(request):
#     form = forms.AppointmentForm(request.POST or None)
#     patient = UserWithUserType.objects.get(username=request.user.username)
#     available_time_slots = []
    
#     if request.method == 'POST':
#         print('abc',form.is_valid())
#         date = form.cleaned_data.get('appointment_date')
#         doctor = form.cleaned_data.get('doctor')
#         if date and doctor:
#             booked_appointments = Appointment.objects.filter(doctor=doctor, appointment_date=date)
#             booked_time_slots = [appointment.time_slot.strftime('%I:%M %p') for appointment in booked_appointments]
#             print(booked_time_slots)
#             # import pdb;pdb.set_trace()

#             all_time_slots = ['09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM',
#                             '12:30 PM', '01:00 PM', '01:30 PM', '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM',
#                             '04:00 PM', '04:30 PM', '05:00 PM', '05:30 PM', '06:00 PM', '06:30 PM', '07:00 PM']

#             available_time_slots = [slot for slot in all_time_slots if slot not in set(booked_time_slots)]
#             print(available_time_slots)
#         if form.is_valid():
#             print('#', available_time_slots)

#             appointment = form.save()
#             appointment.patient = patient
#             appointment.save()
#             return redirect('patient_home')
            

#     else:
#         print(form.errors)

    
#     context = {'form': form, 'patient': patient, 'available_time_slots': available_time_slots}
#     return render(request, 'book_appointment.html', context)

# from django.http import JsonResponse
# import json

# def book_appointment(request):
#     patient = UserWithUserType.objects.get(username=request.user.username)

#     if request.method == 'POST':
#         form = forms.AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.patient = patient
#             appointment.save()
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'errors': form.errors})

#     departments = [choice[0] for choice in Appointment.department.field.choices]
#     doctors = UserWithUserType.objects.filter(role='doctor')
#     departments_json = json.dumps(departments)
#     doctors_json = json.dumps([{'id': doctor.id, 'name': doctor.first_name} for doctor in doctors])
#     # print(doctors_json)
#     context = {
#         'departments': departments_json,
#         'doctors': doctors_json,
#         'patient': patient
#     }
#     return render(request, 'book_appointment.html', context)

