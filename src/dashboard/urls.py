from django.urls import path
from . import views


app_name = 'dashboard'

urlpatterns = [
    path('welcome/', views.dashboard, name='dashboard'),

    # Employee
    path('employees/all/', views.dashboard_employees, name='employees'),
    path('employee/create/', views.dashboard_employees_create, name='employeecreate'),
    path('employee/profile/<int:id>/',
         views.dashboard_employee_info, name='employeeinfo'),
    path('employee/profile/edit/<int:id>/',
         views.employee_edit_data, name='edit'),
    path('employee/profile/delete/<int:id>/',
         views.dashboard_employee_delete, name='delete'),
    # Departement
    path('departments/all/', views.dashboard_departments, name='departments'),
    path('department/create/', views.dashboard_department_create,
         name='departmentcreate'),
    path('department/edit/<int:id>/',
         views.dashboard_department_edit_data, name='departmentedit'),
    path('department/delete/<int:id>/',
         views.dashboard_department_delete, name='departmentdelete'),
    # Role
    path('roles/all/', views.dashboard_roles, name='roles'),
    path('role/create/', views.dashboard_role_create, name='rolecreate'),
    path('role/edit/<int:id>/', views.dashboard_role_edit_data, name='roleedit'),
    path('role/delete/<int:id>/', views.dashboard_role_delete, name='roledelete'),
]
