from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
	body = models.TextField()
	image = models.ImageField(upload_to='media/uploads/post_photos', blank=True, null=True) 
	created_on = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, blank=True, related_name='likes')
	dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
	loves = models.ManyToManyField(User, blank=True, related_name='loves')
class Comment(models.Model):
	comment = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)
	author = author = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey('Post', on_delete=models.CASCADE)

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
	name = models.CharField(max_length=30, blank=True, null=True)
	bio = models.TextField(max_length=500, blank=True, null=True)
	birth_date = models.DateField(null=True, blank=True)
	location = models.CharField(max_length=100, blank=True, null=True)
	picture = models.ImageField(upload_to="media/uploads/profile_pictures/", default="media/uploads/profile_pictures/default.png")
	followers = models.ManyToManyField(User, blank=True, related_name='followers')
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
	instance.profile.save()

class Groups(models.Model):
    myuser = models.ForeignKey(User, related_name='groups')
    name = models.charField(max_length=30, blank=True, null=True)
    description = models.TextField(max_length=600, blank=True, null=True)
	
	
