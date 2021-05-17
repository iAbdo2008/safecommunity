from django.contrib import admin
from .models import Post, UserProfile, Notification

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Notification)
