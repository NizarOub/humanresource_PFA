from django.db import models
import datetime


class EmployeeManager(models.Manager):

    def all_employees(self):
        '''
        Employee.objects.all_employee() -> returns all employees including deleted one's
        NB: don't specify filter. ***
        '''
        return super().get_queryset()
