from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
# -----------------------------------------GENRAL URLS---------------------------------------------------------
    path('admin/', admin.site.urls),
    path('', views.Index,name='index'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('signup/<str:role>',views.user_signup,name='user_signup'),
    path('doctor_list/',views.doctor_list,name='doctor_list'),
    path('departments/',views.departments,name='departments'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),

# ---------------------------------------DOCTOR RELATED URLS---------------------------------------------------

    path('doctor_Home/',views.doctor_home,name='doctor_home'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('edit_doctor_profile/', views.edit_doctor_profile, name='edit_doctor_profile'),
    path('doctor_patients/', views.doctor_patients, name='doctor_patients'),
    path('doctor_feedback/', views.doctor_feedback, name='doctor_feedback'),

# ---------------------------------------PATIENT RELATED URLS--------------------------------------------------

    path('patient_Home/',views.patient_home,name='patient_home'),
    path('patient_view_feedback/', views.patient_view_feedback, name='patient_view_feedback'),
    path('book_appointment/',views.book_appointment,name='book_appointment'),
    path('patient_appointment/',views.patient_appointment,name='patient_appointment'),
    path('edit_appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('patient_feedback/', views.patient_feedback, name='patient_feedback'),
    path('select_time/', views.select_time, name='select_time'),
    # path('waitlist/', views.waitlist, name='waitlist'),
] 