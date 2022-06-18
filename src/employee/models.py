import datetime
from django.db import models
from employee.managers import EmployeeManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


# Create your models here.
class Role(models.Model):
    '''
        Role Table eg. Staff,Manager,H.R ...
    '''
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)

    created = models.DateTimeField(
        verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['name', 'created']

    def __str__(self):
        return self.name


class Department(models.Model):
    '''
     Department Employee belongs to. eg. Transport, Engineering.
    '''
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)

    created = models.DateTimeField(
        verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name', 'created']

    def __str__(self):
        return self.name


class Employee(models.Model):

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    NOT_KNOWN = 'Not Known'

    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (NOT_KNOWN, 'Not Known'),
    )

    MR = 'Mr'
    MRS = 'Mrs'
    MSS = 'Mss'
    DR = 'Dr'
    SIR = 'Sir'
    MADAM = 'Madam'

    TITLE = (
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MSS, 'Mss'),
        (DR, 'Dr'),
        (SIR, 'Sir'),
        (MADAM, 'Madam'),
    )

    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    INTERN = 'Intern'

    EMPLOYEETYPE = (
        (FULL_TIME, 'Full-Time'),
        (PART_TIME, 'Part-Time'),
        (CONTRACT, 'Contract'),
        (INTERN, 'Intern'),
    )

    # PERSONAL DATA
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(_('Title'), max_length=4,
                             default=MR, choices=TITLE, blank=False, null=True)
    image = models.FileField(_('Profile Image'), upload_to='profiles', default='default.png', blank=True,
                             null=True, help_text='upload image size less than 2.0MB')  # work on path username-date/image
    firstname = models.CharField(
        _('Firstname'), max_length=125, null=False, blank=False)
    lastname = models.CharField(
        _('Lastname'), max_length=125, null=False, blank=False)
    othername = models.CharField(
        _('Othername (optional)'), max_length=125, null=True, blank=True)
    sex = models.CharField(_('Gender'), max_length=8,
                           default=MALE, choices=GENDER, blank=False)
    email = models.CharField(
        _('Email (optional)'), max_length=255, default=None, blank=True, null=True)
    tel = PhoneNumberField(default='+233240000000', null=False, blank=False,
                           verbose_name='Phone Number (Example +233240000000)', help_text='Enter number with Country Code Eg. +233240000000')
    bio = models.CharField(_('Bio'), help_text='your biography,tell me something about yourself eg. i love working ...',
                           max_length=255, default='', null=True, blank=True)
    birthday = models.DateField(_('Birthday'), blank=False, null=False)

    cinnumber = models.CharField(
        _('CIN Number'), max_length=30, null=True, blank=True)

    # COMPANY DATA
    department = models.ForeignKey(Department, verbose_name=_(
        'Department'), on_delete=models.SET_NULL, null=True, default=None)
    role = models.ForeignKey(Role, verbose_name=_(
        'Role'), on_delete=models.SET_NULL, null=True, default=None)
    startdate = models.DateField(
        _('Employement Date'), help_text='date of employement', blank=False, null=True)
    employeetype = models.CharField(_('Employee Type'), max_length=15,
                                    default=FULL_TIME, choices=EMPLOYEETYPE, blank=False, null=True)

    # app related
    is_blocked = models.BooleanField(
        _('Is Blocked'), help_text='button to toggle employee block and unblock', default=False)
    is_deleted = models.BooleanField(
        _('Is Deleted'), help_text='button to toggle employee deleted and undelete', default=False)

    created = models.DateTimeField(verbose_name=_(
        'Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(
        verbose_name=_('Updated'), auto_now=True, null=True)

    # PLUG MANAGERS
    objects = EmployeeManager()

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['-created']

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        fullname = ''
        firstname = self.firstname
        lastname = self.lastname
        othername = self.othername

        if (firstname and lastname) or othername is None:
            fullname = firstname + ' ' + lastname
            return fullname
        elif othername:
            fullname = firstname + ' ' + lastname + ' '+othername
            return fullname
        return

    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.birthday.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return
