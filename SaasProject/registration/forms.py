
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput  # Corrected import

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Ensure that the two passwords match
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# registration/forms.py

