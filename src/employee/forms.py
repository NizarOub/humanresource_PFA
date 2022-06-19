from django import forms
from employee.models import Role, Department, Employee, Announcement
from django.contrib.auth.models import User


class EmployeeCreateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'onchange': 'previewImage(this);'}))

    class Meta:
        model = Employee
        exclude = ['is_blocked', 'is_deleted', 'created', 'updated']
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 5, 'rows': 5})
        }

class DepartmentCreateForm(forms.ModelForm):
    class Meta:
        model = Department
        exclude = ['created', 'updated']

class RoleCreateForm(forms.ModelForm):
    class Meta:
        model = Role
        exclude = ['created', 'updated']

# create annoucement form with name, description, date debut, date fin


class AnnouncementCreateForm(forms.ModelForm):
    class Meta:
        model = Announcement
        exclude = ['created', 'updated']
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 5, 'rows': 5})
        }
