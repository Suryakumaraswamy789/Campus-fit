from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password

# --- UPDATED THIS LIST ---
ALLOWED_DOMAINS = ['college.edu', 'university.ac.in', 'gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com']

class LearnerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = User
        fields = ['full_name', 'email']

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name) < 4:
            raise forms.ValidationError("Full name must be at least 4 characters long.")
        return full_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            domain = email.split('@')[-1]
            if domain not in ALLOWED_DOMAINS:
                raise forms.ValidationError(f"Please use an approved email provider. Allowed: {', '.join(ALLOWED_DOMAINS)}")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match.")
        
        if password:
            try:
                validate_password(password, self.instance)
            except forms.ValidationError as e:
                self.add_error('password', e)
        
        return cleaned_data

class MentorSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = User
        fields = ['full_name', 'email']
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name) < 4:
            raise forms.ValidationError("Full name must be at least 4 characters long.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            domain = email.split('@')[-1]
            if domain not in ALLOWED_DOMAINS:
                raise forms.ValidationError(f"Please use an approved email provider. Allowed: {', '.join(ALLOWED_DOMAINS)}")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match.")

        if password:
            try:
                validate_password(password, self.instance)
            except forms.ValidationError as e:
                self.add_error('password', e)
        
        return cleaned_data