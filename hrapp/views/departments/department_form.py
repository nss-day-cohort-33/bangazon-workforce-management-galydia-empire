import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Department
from ..connection import Connection
from django.contrib.auth.decorators import login_required


def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select
                d.id,
                d.dept_name,
                d.budget
            from hrapp_department d
            """)

        return db_cursor.fetchall()

@login_required
def department_form(request):
    if request.method == 'GET':
        departments = get_departments()
        template = 'departments/department_form.html'
        context = {
            'all_departments': departments
        }
        return render(request, template, context)

