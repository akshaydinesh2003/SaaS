from django.db import models
from django.contrib.auth.models import User
from userlogin.models import UserProfile

class Task(models.Model):
    # ... other fields ...
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


# Task Model
class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

# UserProfile Model for Role Management
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return self.user.username

# Role Request Model
class RoleRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_role = models.CharField(max_length=50, choices=[('manager', 'Manager')])
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending')
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.requested_role} ({self.status})"


from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='taskmanager_profile')
    role = models.CharField(max_length=20)
