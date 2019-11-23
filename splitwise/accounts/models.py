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
('e',(
('1','paid by you and split by shares'),('2','paid by friend and split by shares'),('3','paid by you and split by percentages'),('4','paid by friend and split by percentages'),
)),
]


class Transactions(models.Model):
	users = models.ManyToManyField(User)
	current_user = models.ForeignKey(User, related_name='owners',null=True,on_delete=models.CASCADE)
	amount = models.IntegerField(default=0,blank=True)
	payable = models.IntegerField(default=0,blank=True)
	status = models.IntegerField(default=0,blank=True)
	pair = models.IntegerField(default=0,blank=True)
	# net = models.IntegerField(default=0,blank=True)
	type = models.CharField(max_length=5,choices=CHOICES,default='green')
	desc = models.CharField(max_length = 100,blank = False)
	tag = models.CharField(max_length = 100,blank = False)
	@classmethod
	def add_transaction(cls,current_user,new_friend,amount,type,desc,tag):
		if(type=='a'):
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=amount/2,type=type,desc=desc,tag=tag)
			tran1.users.add(new_friend)
			ulfa = Friend.objects.get(current_user=current_user)
			ulfa.debt =  ulfa.debt + (amount/2)
			ulfa.save()
			# var1 = add_debt.objects.get(current_user=current_user,users=new_friend)
			# var1.debt_between = var1.debt_between + (amount/2)
			# var1.save()
			# var2 = add_debt.objects.get(current_user=new_friend,users=current_user)
			# var2.debt_between = var2.debt_between - (amount/2)
			# var2.save()
			ulfa1 = Friend.objects.get(current_user=new_friend)
			ulfa1.debt =  ulfa1.debt - (amount/2)
			ulfa1.save()
			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=-amount/2,type=type,desc=desc,tag=tag)
			tran2.users.add(current_user)
			tran1.pair = tran2.pk
			tran1.save()
			tran2.pair = tran1.pk
			tran2.save()
		elif(type=='b'):
			tran,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=-amount/2,type=type,desc=desc,tag=tag)
			tran.users.add(new_friend)
			ulfa = Friend.objects.get(current_user=current_user)
			ulfa.debt =  ulfa.debt - (amount/2)
			ulfa.save()
			ulfa1 = Friend.objects.get(current_user=new_friend)
			ulfa1.debt =  ulfa1.debt + (amount/2)
			ulfa1.save()
			tran,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=amount/2,type=type,desc=desc,tag=tag)
			tran.users.add(current_user)
		elif(type=='c'):
			tran,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=-amount,type=type,desc=desc,tag=tag)
			tran.users.add(new_friend)
			ulfa = Friend.objects.get(current_user=current_user)
			ulfa.debt =  ulfa.debt - amount
			ulfa.save()
			ulfa1 = Friend.objects.get(current_user=new_friend)
			ulfa1.debt =  ulfa1.debt + amount
			ulfa1.save()
			tran,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=amount,type=type,desc=desc,tag=tag)
			tran.users.add(current_user)
		elif(type=='d'):
			tran,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=amount,type=type,desc=desc,tag=tag)
			tran.users.add(new_friend)
			ulfa = Friend.objects.get(current_user=current_user)
			ulfa.debt =  ulfa.debt + amount
			ulfa.save()

# class add_debt(models.Model):
# 	users = models.ManyToManyField(User)
# 	current_user = models.ForeignKey(User, related_name='owners_debts',null=True,on_delete=models.CASCADE)
# 	debt_between = models.IntegerField(default=0,blank=True)
# 	@classmethod
# 	def add_debting(cls,current_user,new_friend):
# 		balance,created = cls.objects.get_or_create(current_user = current_user,users = new_friend)
# 		balance.users.add(new_friend)
# 		balance,created = cls.objects.get_or_create(current_user = new_friend , users = current_user)
# 		balance.users.add(current_user)


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
