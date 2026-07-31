from django.contrib import admin
from .models import Profile,Follow

# Register your models here.
admin.site.register(Profile)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at'] 
