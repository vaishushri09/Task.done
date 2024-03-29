from django.db import models
from django.contrib.auth import get_user_model

class Task(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    time_of_completion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    recommendation = models.TextField(null=True, blank=True)
    work_recommendation = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.user)


# rooms/models.py
# todo_app/models.py
from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Assuming 1 is the default User ID

    
    def is_password_valid(self, entered_password):
        return self.password == entered_password