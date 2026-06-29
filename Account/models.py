
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_picture = models.ImageField(upload_to="profile_pictures/",default="profile_pictures/default.png")
    bio = models.TextField(max_length=300,blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100,blank=True)
    birth_date = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username}'s Profile"


User = get_user_model()
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)