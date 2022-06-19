from django.contrib import admin
from employee.models import Role, Department, Employee, Announcement


admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Announcement)
admin.site.register(Employee)
