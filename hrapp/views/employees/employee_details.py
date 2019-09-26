import sqlite3
from django.shortcuts import render, redirect, reverse
from hrapp.models import Employee, model_factory, TrainingProgramEmployee, Department
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from datetime import date


@login_required
def employee_details(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)
        trainings = get_programs()

        old_trainings = list()
        new_trainings = list()

        for training in trainings:
            if training.employee_id == employee.id:
                if training.start_date <  date.today().strftime("%Y/%m/%d"):
                   
                    old_trainings.append(training)
                else:
                    new_trainings.append(training)

        template = 'employees/employees_details.html'
        context = {
            'employee': employee,
            'old_trainings': old_trainings,
            'new_trainings': new_trainings
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM hrapp_employee
                WHERE id = ?
                """, (employee_id,))

            return redirect(reverse('hrapp:employees'))

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "EDIT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                employee = get_employee(employee_id)

                departments = get_departments()

                template = "employees/employees_form.html"
                context = {
                    'employee': employee,
                    'departments': departments
                }

                return render(request, template, context)


def get_employee(employee_id):
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
            d.dept_name,
            ec.id comp_join_id,
            ec.computer_id,
            ec.employee_id,
            c.manufacturer,
            c.model
        from hrapp_employee e
        left join hrapp_department d on d.id = e.department_id
        left join hrapp_employeecomputer ec on ec.employee_id = e.id 
        left join hrapp_computer c on c.id = ec.computer_id
        where e.id = ?
        """, (employee_id,))
        return db_cursor.fetchone()


def get_programs():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgramEmployee)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            tpe.id,
            tpe.employee_id,
            tpe.training_program_id,
            tp.title,
            tp.start_date,
            tp.end_date,
            tp.capacity
        from hrapp_trainingprogramemployee tpe
        left join hrapp_trainingprogram tp on tp.id = tpe.training_program_id
        """)

        return db_cursor.fetchall()

def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select
            d.id,
            d.dept_name,
            d.budget
        from hrapp_department d
        """)
        return db_cursor.fetchall()