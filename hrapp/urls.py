from django.urls import path
from django.conf.urls import url, include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('employees/', employee_list, name='employees'),
    path('employees/form/', employee_form, name='employee_form'),
    path('departments/', department_list, name='department_list'),
    path('department/form', department_form, name='department_form'),
    path('departments/<int:department_id>', department_details, name='department'),
]
