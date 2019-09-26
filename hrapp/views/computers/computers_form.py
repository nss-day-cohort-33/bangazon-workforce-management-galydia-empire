import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer, Employee
from hrapp.models import model_factory
# from .details import get_book
from ..connection import Connection


def get_computers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select
                c.id,
                c.manufacturer,
                c.model,
                c.purchase_date,
                c.decommission_date
            from hrapp_computer c
            """)

        return db_cursor.fetchall()

def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
        e.id,
            e.first_name,
            e.last_name
        from hrapp_employee e
        """)

        return db_cursor.fetchall()

@login_required
def computer_form(request):
    if request.method == 'GET':
        computers = get_computers()
        employees = get_employees()
        template = 'computers/computers_form.html'
        context = {
            'all_computers': computers,
            'all_employees': employees
        }

        return render(request, template, context)

# @login_required
# def book_edit_form(request, book_id):

#     if request.method == 'GET':
#         book = get_book(book_id)
#         libraries = get_libraries()

#         template = 'books/form.html'
#         context = {
#             'book': book,
#             'all_libraries': libraries
#         }

#         return render(request, template, context)