from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from employee.models import *
from .forms import UserLogin, UserAddForm


def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            update_session_auth_hash(request, user)

            messages.success(request, 'Password changed successfully',
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('accounts:changepassword')
        else:
            messages.error(request, 'Error,changing password',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('accounts:changepassword')

    form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password_form.html', {'form': form})


def login_view(request):

    login_user = request.user
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                login(request, user)
                if login_user.is_authenticated:
                    return redirect('dashboard:announcements')
            else:
                messages.error(request, 'Account is invalid',
                               extra_tags='alert alert-error alert-dismissible show')
                return redirect('accounts:login')
        else:
            return HttpResponse('data not valid')

    dataset = dict()
    form = UserLogin()

    dataset['form'] = form
    return render(request, 'accounts/login.html', dataset)


def user_profile_view(request):
    user = request.user
    if user.is_authenticated:
        employee = Employee.objects.filter(user=user).first()

        dataset = dict()
        dataset['employee'] = employee
        return render(request, 'dashboard/employee_detail.html', dataset)
    return HttpResponse("Sorry , not authenticated for this,admin or whoever you are :)")


def logout_view(request):
    logout(request)
    return redirect('accounts:login')
