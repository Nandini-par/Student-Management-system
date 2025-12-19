from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User



class Course(models.Model):
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)   
    fee = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name



class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    age = models.IntegerField()

    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{10}$', 'Invalid phone number.')],
        blank=True,
        null=True
    )

 
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="students",
        null=True,
        blank=True
    )

 
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )


    teachers = models.ManyToManyField(
        Teacher,
        blank=True,
        related_name="students"
    )

    class Meta:
        permissions = [
            ("can_update_student", "Can update student"),
        ]

    def __str__(self):
        return self.name
