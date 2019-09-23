from django.db import models
from .computer import Computer
from .employee import Employee
# import datetime
from django.utils.timezone import now

class EmployeeComputer(models.Model):
    """
    Creates the join table for the many to many relationship between computers and employees
    Author: Joe Shep
    methods: none
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(default=now, editable=False)
    unassigned_date = models.DateTimeField(null=True, blank=True)