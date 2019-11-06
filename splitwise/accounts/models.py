from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class profile(models.Model):
	# name = models.CharField(max_length = 100)
	# password = models.CharField(max_length = 150)
	user = models.OneToOneField(User,on_delete=models.PROTECT)
	firstname = models.CharField(max_length = 100,blank=True,)
	secondname = models.CharField(max_length = 100,blank=True)
	email =models.EmailField(default="",blank=True)
	number = models.IntegerField(default=0,blank=True)
	city = models.CharField(max_length = 100,blank=True)
	image = models.ImageField(upload_to='images/',blank=True)

	def __str__(self):
		return self.user.username

def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)