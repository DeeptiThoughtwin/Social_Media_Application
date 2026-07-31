from django.contrib import admin
from .models import Post, PostMedia, Like
# Register your models here.


admin.site.register(Post)
admin.site.register(PostMedia)
admin.site.register(Like)
