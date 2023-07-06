from django.http import HttpResponse
from django.shortcuts import redirect
from .models import UserWithUserType
from django.contrib.auth.decorators import login_required

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(request_role):
    def decorator(view_func):
        @login_required
        def wrapper_func(request, *args, **kwargs):
            role=UserWithUserType.objects.get(username=request.user.username).role
            if role == request_role:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

patient_required = allowed_users('patient')
doctor_required = allowed_users('doctor')