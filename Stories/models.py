from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.




class Story(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="stories")
    image = models.ImageField(upload_to = "stories/")
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.username

