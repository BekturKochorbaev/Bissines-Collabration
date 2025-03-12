from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import *

POSITIONS = (
    ("Manager", "Manager"),
    ("Accountant", "Accountant"),
    ("Auditor", "Auditor"),
    ("Organizer", "Organizer"),
    ("Supervisor", "Supervisor")
)

DEPARTMENTS = (
    ("CRM", "CRM"),
    ("Halal Management", "Halal Management"),
    ("Event Organizer", "Event Organizer"),
    ("Accountancy", "Accountancy")
)


class Personal(models.Model):

    employee = models.ForeignKey(UserSimple, models.CASCADE, related_name="hr_personal")
    post = models.CharField(max_length=25, choices=POSITIONS, null=True, blank=True)
    department = models.CharField(max_length=25, choices=DEPARTMENTS)
    date_of_employment = models.DateField(auto_now_add=True)
    marital_status = models.CharField(max_length=10, choices=[('Married', 'Married'), ('Single', 'Single')])
    address = models.CharField(max_length=150)
    emergency_contacts = PhoneNumberField(null=True, blank=True)
    education = models.CharField(max_length=250)
    university_college = models.CharField(max_length=250)
    skills = models.TextField()
    employment_type = models.CharField(max_length=15, choices=[("Full time", "Full time")], default="Full time")
    passport_number = models.CharField(max_length=150)
    health_history = models.FileField(upload_to='health_history_files/', null=True, blank=True)
    pay = models.IntegerField(null=True, blank=True)


class VisitHistory(models.Model):
    STATUS_CHOICES = (
        ('working', 'Working'),
        ('lunch', 'Lunch'),
        ('rest', 'Rest'),
        ('vacation', 'Vacation'),
        ('sick_leave', 'Sick_leave'),
        ('left_work', 'Left_work'),
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    personal_status = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name="personal_status")

    def __str__(self):
        return str(self.personal_status)


class VisitHistoryComment(models.Model):
    user = models.OneToOneField(Personal, on_delete=models.CASCADE, related_name="personal")
    comment = models.TextField()
    visit = models.ForeignKey(VisitHistory, on_delete=models.CASCADE, related_name='comment')


class VacationRequest(models.Model):
    VACATION_TYPE = (
        ('Paid vacation', 'Paid vacation'),
        ('Service note', 'Service note'),
        ('Maternity leave', 'Maternity leave'),
        ('Sick leave', 'Sick leave'),
    )
    VACATION_STATUS = (
        ('approved', 'approved'),
        ('rejected', 'rejected'),
        ('waiting', 'waiting'),
    )
    status = models.CharField(max_length=15, choices=VACATION_STATUS)
    type = models.CharField(max_length=15, choices=VACATION_TYPE)
    from_who = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='leave_status')
    manager = models.ForeignKey(Personal, related_name='manager', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    document = models.FileField(upload_to='vacation_request_document/', null=True, blank=True)


class Sticker(models.Model):
    image = models.ImageField(upload_to='stickers/')

    def __str__(self):
        return str(self.image)


class Award(models.Model):
    manager = models.ForeignKey(Personal, related_name='comments_given', on_delete=models.CASCADE)
    employee = models.ForeignKey(Personal, related_name='comments_received', on_delete=models.CASCADE)
    sticker = models.ForeignKey(Sticker, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.manager} to {self.employee}"


class Vacancy(models.Model):
    vacancy_name = models.CharField(max_length=65)
    STATUS = (
        ('active', 'active'),
        ('close', 'close')
    )
    status = models.CharField(choices=STATUS, max_length=8)
    salary = models.IntegerField(null=True, blank=True)
    description = models.TextField()






