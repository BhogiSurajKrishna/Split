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

class Friend(models.Model):
	users = models.ManyToManyField(User)
	current_user = models.ForeignKey(User, related_name='owner',null=True,on_delete=models.CASCADE)
	@classmethod
	def make_friend(cls,current_user,new_friend):
		friend, created = cls.objects.get_or_create(
			current_user=current_user
		)
		friend.users.add(new_friend)
		friend, created = cls.objects.get_or_create(
			current_user=new_friend
		)
		friend.users.add(current_user)


def create_friend(sender,**kwargs):
	if kwargs['created']:
		user_friends = Friend(User)
		user_friends.user = kwargs['instance']

post_save.connect(create_friend, sender=User)

class add_group(models.Model):
	# name = models.CharField(max_length = 100)
	# password = models.CharField(max_length = 150)
	#user = models.ManyToManyField(User)
	#current_user = models.ForeignKey(User, related_name='owner',null=True,on_delete=models.CASCADE)
	#id = models.IntegerField(primary_key=True)
	GroupName = models.CharField(max_length = 100,blank=True,)
	Description = models.CharField(max_length = 100,blank=True)
	#group = models.ManyToManyField(GroupName)

	def __str__(self):
		return self.GroupName

class group_member(models.Model):
	group_members = models.ManyToManyField(add_group)
