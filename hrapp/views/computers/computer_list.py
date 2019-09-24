import sqlite3
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from hrapp.models import Computer
from hrapp.models import model_factory
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from .computers_form import get_computers





from ..connection import Connection
from django.contrib.auth.decorators import login_required


@login_required
def computer_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # TODO: Add to query: c.department,
            db_cursor.execute("""
            select
                c.id,
                c.make,
                c.purchase_date,
                c.decommission_date
            from hrapp_computer c
            """)

            all_computers = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                computer = Computer()
                computer.id = row['id']
                computer.make = row['make']
                computer.purchase_date = row['purchase_date']
                computer.decommission_date = row['decommission_date']

                all_computers.append(computer)

        template = 'computers/computers_list.html'
        context = {
            'computers': all_computers
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_computer
            (
                make, purchase_date, decommission_date
            )
            VALUES (?, ?, ?)
            """,
            (form_data['make'], form_data['purchase_date'],
                form_data['decommission_date']))

            return redirect(reverse('hrapp:computer_list'))

@login_required
def computer_form(request):
    if request.method == 'GET':
        computers = get_computers()
        template = 'computers/computers_form.html'
        context = {
            'all_computers': computers
        }

        return render(request, template, context)