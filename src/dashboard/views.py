from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from employee.forms import EmployeeCreateForm, DepartmentCreateForm, RoleCreateForm
from employee.models import *
# from leave.forms import CommentForm


def dashboard(request):
    '''
    Summary of all apps - display here with charts etc.
    eg.lEAVE - PENDING|APPROVED|RECENT|REJECTED - TOTAL THIS MONTH or NEXT MONTH
    EMPLOYEE - TOTAL | GENDER 
    CHART - AVERAGE EMPLOYEE AGES
    '''
    dataset = dict()
    user = request.user

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    employees = Employee.objects.all()
    departments = Department.objects.all()
    roles = Role.objects.all()

    dataset['employees'] = employees
    dataset['departments'] = departments
    dataset['roles'] = roles
    dataset['title'] = 'summary'

    return render(request, 'dashboard/dashboard_index.html', dataset)


def dashboard_employees(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    dataset = dict()
    departments = Department.objects.all()
    employees = Employee.objects.all()

    # pagination
    query = request.GET.get('search')
    if query:
        employees = employees.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query)
        )

    paginator = Paginator(employees, 10)  # show 10 employee lists per page

    page = request.GET.get('page')
    employees_paginated = paginator.get_page(page)

    dataset['employee_list'] = employees_paginated
    dataset['departments'] = departments
    dataset['all_employees'] = Employee.objects.all_employees()

    blocked_employees = Employee.objects.all_blocked_employees()

    dataset['blocked_employees'] = blocked_employees
    dataset['title'] = 'Employees list view'
    return render(request, 'dashboard/employee_app.html', dataset)


def dashboard_employees_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.POST.get('user')
            assigned_user = User.objects.get(id=user)

            instance.user = assigned_user

            instance.title = request.POST.get('title')
            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')
            instance.sex = request.POST.get('sex')
            instance.bio = request.POST.get('bio')
            instance.birthday = request.POST.get('birthday')

            department_id = request.POST.get('department')
            department = Department.objects.get(id=department_id)
            instance.department = department

            instance.position = request.POST.get('position')
            instance.ssnitnumber = request.POST.get('cinnumber')

            role = request.POST.get('role')
            role_instance = Role.objects.get(id=role)
            instance.role = role_instance

            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')

            instance.save()

            return redirect('dashboard:employees')
        else:
            messages.error(request, 'Trying to create dublicate employees with a single user account ',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:employeecreate')

    dataset = dict()
    form = EmployeeCreateForm()
    dataset['form'] = form
    dataset['title'] = 'register employee'
    return render(request, 'dashboard/employee_create.html', dataset)


def employee_edit_data(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeCreateForm(
            request.POST or None, request.FILES or None, instance=employee)
        if form.is_valid():
            instance = form.save(commit=False)

            user = request.POST.get('user')
            assigned_user = User.objects.get(id=user)

            instance.user = assigned_user

            instance.title = request.POST.get('title')
            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')
            instance.sex = request.POST.get('sex')
            instance.bio = request.POST.get('bio')
            instance.birthday = request.POST.get('birthday')

            department_id = request.POST.get('department')
            department = Department.objects.get(id=department_id)
            instance.department = department

            instance.position = request.POST.get('position')
            instance.ssnitnumber = request.POST.get('cinnumber')

            role = request.POST.get('role')
            role_instance = Role.objects.get(id=role)
            instance.role = role_instance

            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')

            instance.save()
            messages.success(request, 'Account Updated Successfully !!!',
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:employees')

        else:

            messages.error(request, 'Error Updating account',
                           extra_tags='alert alert-warning alert-dismissible show')
            return HttpResponse("Form data not valid")

    dataset = dict()
    form = EmployeeCreateForm(request.POST or None,
                              request.FILES or None, instance=employee)
    dataset['form'] = form
    dataset['title'] = 'edit - {0}'.format(employee.get_full_name)
    return render(request, 'dashboard/employee_create.html', dataset)


def dashboard_employee_info(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    employee = get_object_or_404(Employee, id=id)

    dataset = dict()
    dataset['employee'] = employee
    dataset['title'] = 'profile - {0}'.format(employee.get_full_name)
    return render(request, 'dashboard/employee_detail.html', dataset)

# function add departement


def dashboard_department_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    if request.method == 'POST':
        form = DepartmentCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = request.POST.get('name')
            instance.save()
            return redirect('dashboard:departments')
        else:
            messages.error(request, 'Trying to create dublicate department',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:departmentcreate')

    dataset = dict()
    form = DepartmentCreateForm()
    dataset['form'] = form
    dataset['title'] = 'register department'
    return render(request, 'dashboard/department_create.html', dataset)

# function dashboard_departments view


def dashboard_departments(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    dataset = dict()
    dataset['title'] = 'departments'
    dataset['departments'] = Department.objects.all()
    return render(request, 'dashboard/departments.html', dataset)

# function dashboard_department_edit_data view


def dashboard_department_edit_data(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    department = get_object_or_404(Department, id=id)
    if request.method == 'POST':
        form = DepartmentCreateForm(request.POST, instance=department)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = request.POST.get('name')
            instance.save()
            return redirect('dashboard:departments')
        else:
            messages.error(request, 'Trying to create dublicate department',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:departmentcreate')

    dataset = dict()
    form = DepartmentCreateForm(request.POST or None, instance=department)
    dataset['form'] = form
    dataset['title'] = 'edit - {0}'.format(department.name)
    return render(request, 'dashboard/department_create.html', dataset)

# function add role


def dashboard_role_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    if request.method == 'POST':
        form = RoleCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = request.POST.get('name')
            instance.save()
            return redirect('dashboard:roles')
        else:
            messages.error(request, 'Trying to create dublicate role',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:rolecreate')

    dataset = dict()
    form = RoleCreateForm()
    dataset['form'] = form
    dataset['title'] = 'register role'
    return render(request, 'dashboard/role_create.html', dataset)

# function dashboard_role view


def dashboard_roles(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    dataset = dict()
    dataset['title'] = 'roles'
    dataset['roles'] = Role.objects.all()
    return render(request, 'dashboard/roles.html', dataset)


# function dashboard_role_edit_data view
def dashboard_role_edit_data(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    role = get_object_or_404(Role, id=id)
    if request.method == 'POST':
        form = RoleCreateForm(request.POST, instance=role)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = request.POST.get('name')
            instance.save()
            return redirect('dashboard:roles')
        else:
            messages.error(request, 'Trying to create dublicate role',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:rolecreate')

    dataset = dict()
    form = RoleCreateForm(request.POST or None, instance=role)
    dataset['form'] = form
    dataset['title'] = 'edit - {0}'.format(role.name)
    return render(request, 'dashboard/role_edit.html', dataset)


# function dashboard_role__delete data view
def dashboard_role_delete(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    role = get_object_or_404(Role, id=id)
    role.delete()
    return redirect('dashboard:roles')

# function dashboard_departement__delete view
def dashboard_department_delete(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    department = get_object_or_404(Department, id=id)
    department.delete()
    return redirect('dashboard:departments')

# function dashboard_employee__delete view
def dashboard_employee_delete(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('dashboard:employees')