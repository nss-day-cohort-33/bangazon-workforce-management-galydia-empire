from django.urls import path
from django.conf.urls import include, url
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('employees/', employee_list, name='employee_list'),
    path('training_programs/', training_program_list, name='training_program_list'),
    url(r'^training_program/form$', training_program_form, name='training_program_form'),
    path('departments/', department_list, name='department_list'),
    path('department/form', department_form, name='department_form'),
    path('training_programs/<int:training_program_id>/', training_program_details, name='training_program_details'),

]
