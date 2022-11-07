from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.db.models.deletion import SET_NULL
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    class yearChoice(models.IntegerChoices):
        I = 1
        II = 2
        III = 3
        IV = 4
    M = 'Male'
    F = 'Female'
    name = models.CharField(max_length=30)
    dob = models.DateField(auto_now=False,blank=True)
    email = models.EmailField(max_length=100)
    gender_Choices = [
        (M, 'Male'),
        (F, 'Female')
    ]
    gender = models.CharField(max_length=6,choices=gender_Choices,blank=True)
    year = models.IntegerField(choices=yearChoice.choices,default=1,blank=True)
    studentUser = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    def __str__(self):
        return self.name

class Exam(models.Model):
    examName = models.CharField(max_length=200)
    examCode = models.CharField(max_length=7)
    examDate = models.DateField(auto_now=False,auto_now_add=False)
    is_selected = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.examName

class RegisteredExam(models.Model):
    student = models.ForeignKey(Student,null=True,on_delete=SET_NULL)
    exam = models.ForeignKey(Exam,null=True, on_delete=SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
