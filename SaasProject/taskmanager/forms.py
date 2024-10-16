from django import forms
from .models import Task, RoleRequest

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'assigned_to']

'''
class RoleRequestForm(forms.ModelForm):
    class Meta:
        model = RoleRequest
        fields = ['requested_role']
'''

from .models import UserProfile  # Adjust this to your actual user profile model

class RoleRequestForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # Assuming UserProfile is the model for user profiles
        fields = ['role']  # Fields you want users to fill out for a role request
