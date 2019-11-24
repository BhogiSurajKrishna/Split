from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms
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
	debt = models.IntegerField(default=0,blank=True)
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

CHOICES=[
('a','paid by you and split equally'),
('b','paid by your friend and split equally'),
('c','You owe to him completely'),
('d','He owe to you completely'),
('e','Split by percentages'), 
('f','Split by shares'),
]


class Transactions(models.Model):
	users = models.ManyToManyField(User)
	current_user = models.ForeignKey(User, related_name='owners',null=True,on_delete=models.CASCADE)
	amount = models.IntegerField(default=0,blank=True)
	payable = models.IntegerField(default=0,blank=True)
	status = models.IntegerField(default=0,blank=True)
	pair = models.IntegerField(default=0,blank=True)
	group = models.CharField(max_length = 100,default='none')
	# net = models.IntegerField(default=0,blank=True)
	type = models.CharField(max_length=10,choices=CHOICES,default='green')
	desc = models.CharField(max_length = 100,blank = False)
	tag = models.CharField(max_length = 100,blank = False)
	current_user_pk = models.IntegerField(default=0,blank=True)
	split = models.IntegerField(default=0,blank=True)
	amount_you = models.IntegerField(default=0,blank=True)
	amount_friend = models.IntegerField(default=0,blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	@classmethod
	def add_transaction(cls,current_user,new_friend,amount,type,desc,tag,split,amount_you,amount_friend):
		if(type=='a'):
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=amount/2,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=-amount/2,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran2.users.add(current_user)

			tran1.pair = tran2.pk
			tran1.current_user_pk = new_friend.pk
			tran1.save()

			tran2.pair = tran1.pk
			tran2.current_user_pk = current_user.pk
			tran2.save()
			return tran1.payable

		elif(type=='b'):
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=-amount/2,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=amount/2,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran2.users.add(current_user)

			tran1.pair = tran2.pk
			tran1.current_user_pk = new_friend.pk
			tran1.save()

			tran2.pair = tran1.pk
			tran2.current_user_pk = current_user.pk
			tran2.save()
			return tran1.payable

		elif(type=='c'):
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=-amount,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=amount,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran2.users.add(current_user)

			tran1.pair = tran2.pk
			tran1.current_user_pk = new_friend.pk
			tran1.save()

			tran2.pair = tran1.pk
			tran2.current_user_pk = current_user.pk
			tran2.save()
			return tran1.payable

		elif(type=='d'):
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=amount,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=-amount,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran2.users.add(current_user)

			tran1.pair = tran2.pk
			tran1.current_user_pk = new_friend.pk
			tran1.save()

			tran2.pair = tran1.pk
			tran2.current_user_pk = current_user.pk
			tran2.save()
			return tran1.payable

		elif(type=='e'):
			if(split == 0):
				x = int(-amount_friend * amount/100)
			elif(split == 1):
				x = int(amount_you*amount/100)
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=x,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=-x,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran2.users.add(current_user)

			tran1.pair = tran2.pk
			tran1.current_user_pk = new_friend.pk
			tran1.save()

			tran2.pair = tran1.pk
			tran2.current_user_pk = current_user.pk
			tran2.save()
			return tran1.payable

		elif(type=='f'):
			if(split == 0):
				x = int(-amount_friend)
			elif(split == 1):
				x = int(amount_you)
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=x,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=-x,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0)
			tran2.users.add(current_user)

			tran1.pair = tran2.pk
			tran1.current_user_pk = new_friend.pk
			tran1.save()

			tran2.pair = tran1.pk
			tran2.current_user_pk = current_user.pk
			tran2.save()
			return tran1.payable


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
