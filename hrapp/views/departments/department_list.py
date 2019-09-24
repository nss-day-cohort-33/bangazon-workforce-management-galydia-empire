import sqlite3
from django.shortcuts import render
from hrapp.models import Department
from ..connection import Connection


def department_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                d.id,
                d.dept_name,
                d.budget,
                e.id,
                e.first_name,
                e.last_name,
                e.department_id
                FROM hrapp_department d
                JOIN hrapp_employee e ON e.id = e.department_id
            """)


            all_departments = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                department = Department()
                department.id = row['id']
                department.dept_name = row['dept_name']
                department.budget = row['budget']

                all_departments.append(department)

        template = 'departments/department_list.html'
        context = {
            'all_departments': all_departments
        }

        return render(request, template, context)