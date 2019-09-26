from django.urls import path
from django.conf.urls import include, url
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('employees/', employee_list, name='employees'),
    path('employees/form/', employee_form, name='employee_form'),
    path('employees/<int:employee_id>/', employee_details, name='employee'),
    path('departments/', department_list, name='department_list'),
    path('department/form', department_form, name='department_form'),
    path('departments/<int:department_id>', department_details, name='department'),
    path('computers/', computer_list, name='computer_list'),
    path('computer/form/', computer_form, name='computer_form'),
    path('computer/<int:computer_id>/', computer_details, name='computer'),
    path('training_programs/', training_program_list, name='training_program_list'),
    url(r'^training_program/form$', training_program_form, name='training_program_form'),
]
