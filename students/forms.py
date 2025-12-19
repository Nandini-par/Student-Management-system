from django import forms
from .models import Student
from django.core.exceptions import ValidationError

class StudentForm(forms.ModelForm):

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(char.isdigit() for char in name):
            raise ValidationError("Name cannot contain numbers")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise ValidationError("Email must end with @gmail.com")
        return email

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 5 or age > 100:
            raise ValidationError("Age must be between 5 and 100")
        return age

    class Meta:
        model = Student
        fields = ['name', 'email', 'age', 'phone_number', 'course', 'teachers'] 
        widgets = {
            'teachers': forms.CheckboxSelectMultiple(), 
        }
