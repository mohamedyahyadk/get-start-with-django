from django.db.models.signals import post_save
from django.db import models 
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User (AbstractUser):
    is_organisor=models.BooleanField(default=True)
    is_agent=models.BooleanField(default=False)

class UserProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
        def __str__(self):
             return self.user.username

class Lead(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    age=models.IntegerField(default=0)
    organisation=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    agent=models.ForeignKey("Agent",null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name} "

class Agent(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    organisation=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username 
   


def Post_user_created_signal(sender,instance,created,**kwargs):
     if created:
          UserProfile.objects.create(user=instance)

post_save.connect(Post_user_created_signal,sender=User)
