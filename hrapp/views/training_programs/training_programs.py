import sqlite3
from django.shortcuts import render
from hrapp.models import TrainingProgram
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from datetime import datetime



@login_required
def training_program_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                tp.id,
                tp.title,
                tp.start_date,
                tp.end_date,
                tp.capacity
            from hrapp_trainingprogram tp

            """)

            all_training_programs = []
            dataset = db_cursor.fetchall()



            for row in dataset:
                training_program = TrainingProgram()
                training_program.id = row['id']
                training_program.title = row['title']
                training_program.start_date = row['start_date']
                training_program.end_date = row['end_date']
                training_program.capacity = row['capacity']

                training_program.start_date = datetime.strptime(row['start_date'], '%m/%d/%Y')

                now = datetime.today()
                if training_program.start_date >= now:
                    # all_training_programs.append(training_program.start_date)

                    all_training_programs.append(training_program)

    template = 'training_programs/training_programs_list.html'
    context = {
        'training_programs': all_training_programs
    }

    return render(request, template, context)
