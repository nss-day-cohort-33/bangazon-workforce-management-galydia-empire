import sqlite3
from django.shortcuts import render, redirect, reverse
from hrapp.models import Employee
from hrapp.models import model_factory
from django.contrib.auth.decorators import login_required
from ..connection import Connection


def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select
            e.id,
            e.first_name,
            e.last_name,
            e.start_date,
            e.is_supervisor,
            e.department_id
        from hrapp_employee e
        """)
        return db_cursor.fetchall()

@login_required
def employee_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Employee)
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                e.id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor,
                e.department_id,
                d.dept_name
            from hrapp_employee e
            join hrapp_department d on e.department_id = d.id
            """)

            all_employees = db_cursor.fetchall()

            # for row in dataset:
            #     employee = Employee()
            #     employee.id = row['id']
            #     employee.first_name = row['first_name']
            #     employee.last_name = row['last_name']
            #     employee.start_date = row['start_date']
            #     employee.is_supervisor = row['is_supervisor']
            #     employee.dept_name = row['dept_name']

            #     all_employees.append(employee)

        template = 'employees/employees_list.html'
        context = {
            'employees': all_employees
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_employee
            (
                first_name, last_name, start_date,
                is_supervisor, department_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (form_data['first_name'], form_data['last_name'],
                form_data['start_date'], form_data['is_supervisor'],
                form_data['department_id']))

        return redirect(reverse('hrapp:employees'))

