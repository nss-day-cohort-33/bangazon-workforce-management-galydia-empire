import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from hrapp.models import Department, Employee
from hrapp.models import model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required


def create_department(cursor, row):
    _row = sqlite3.Row(cursor, row)

    department = Department()
    department.id = _row["id"]
    department.dept_name = _row["dept_name"]
    department.budget = _row["budget"]

    # Note: You are adding a blank employees list to the department object
    # This list will be populated later (see below)
    department.employees = []

    employee = Employee()
    employee.id = _row ["employee_id"]
    employee.first_name = _row["first_name"]
    employee.last_name = _row["last_name"]
    employee.department_id = _row["department_id"]


    # Return a tuple containing the department and the
    # employee built from the data in the current row of
    # the data set
    return (department, employee)

@login_required
def department_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = create_department
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                d.id,
                d.dept_name,
                d.budget,
                e.id employee_id,
                e.first_name,
                e.last_name,
                e.department_id
                FROM hrapp_department d
                LEFT JOIN hrapp_employee e ON d.id = e.department_id
            """)

            all_departments = db_cursor.fetchall()

            department_groups = {}

            for department, employee in all_departments:
                if department.id not in department_groups:
                    department_groups[department.id] = department
                    if employee.first_name is not None:
                        department_groups[department.id].employees.append(employee)

                else:
                    if employee.first_name is not None:
                        department_groups[department.id].employees.append(employee)

        template_name = 'departments/department_list.html'
        context = {
            'all_departments': department_groups.values()
        }

        return render(request, template_name, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_department
            (
                dept_name, budget
            )
            VALUES (?, ?)
            """,
            (form_data['dept_name'], form_data['budget'])
            )

        return redirect(reverse('hrapp:department_list'))


