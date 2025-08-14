from django import forms
from .models import LearnerProfile, MentorProfile, GOAL_CHOICES

class LearnerRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    roll_number = forms.CharField(max_length=20, required=False)
    goal = forms.ChoiceField(choices=GOAL_CHOICES)

class MentorRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    specialization = forms.CharField(max_length=100)
    experience = forms.IntegerField(min_value=0)
    bio = forms.CharField(widget=forms.Textarea, required=False)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)