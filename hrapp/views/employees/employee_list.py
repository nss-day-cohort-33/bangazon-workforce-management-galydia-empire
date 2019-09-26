import sqlite3
from django.shortcuts import render, redirect, reverse
from hrapp.models import Employee
from django.contrib.auth.decorators import login_required
from ..connection import Connection



@login_required
def employee_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
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

            all_employees = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                employee = Employee()
                employee.id = row['id']
                employee.first_name = row['first_name']
                employee.last_name = row['last_name']
                employee.start_date = row['start_date']
                employee.is_supervisor = row['is_supervisor']
                employee.dept_name = row['dept_name']

                all_employees.append(employee)

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


# @login_required
# def create_employee(cursor, row):
#     _row = sqlite3.Row(cursor, row)

#     employee = Employee()
#     employee.id = _row["id"]
#     employee.first_name = _row["first_name"]
#     employee.last_name = _row["last_name"]
#     employee.start_date = _row["start_date"]
#     employee.is_supervisor = _row["is_supervisor"]
#     employee.dept_name = _row['dept_name']
#     employee.comp_manufacturer = _row['comp_manufacturer']
#     employee.comp_model = _row['comp_model']

#     training_programs = {}
#     librarian = Librarian()
#     librarian.id = _row["librarian_id"]
#     librarian.first_name = _row["first_name"]
#     librarian.last_name = _row["last_name"]
    

#     library = Library()
#     library.id = _row["library_id"]
#     library.start_date = _row["library_name"]

#     employee.librarian = librarian
#     employee.location = library

#     return employee
