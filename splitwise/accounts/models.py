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
	userid = models.CharField(max_length=100,blank=True,default="")

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
	group = models.CharField(default='none',max_length=100)
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
	def add_transaction(cls,current_user,new_friend,amount,type,desc,tag,split,amount_you,amount_friend,group):
		if(type=='a'):
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=amount/2,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=-amount/2,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
			tran2.users.add(current_user)

			tran1.pair = tran2.pk
			tran1.current_user_pk = new_friend.pk
			tran1.save()

			tran2.pair = tran1.pk
			tran2.current_user_pk = current_user.pk
			tran2.save()
			return tran1.payable

		elif(type=='b'):
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=-amount/2,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=amount/2,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
			tran2.users.add(current_user)

			tran1.pair = tran2.pk
			tran1.current_user_pk = new_friend.pk
			tran1.save()

			tran2.pair = tran1.pk
			tran2.current_user_pk = current_user.pk
			tran2.save()
			return tran1.payable

		elif(type=='c'):
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=-amount,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=amount,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
			tran2.users.add(current_user)

			tran1.pair = tran2.pk
			tran1.current_user_pk = new_friend.pk
			tran1.save()

			tran2.pair = tran1.pk
			tran2.current_user_pk = current_user.pk
			tran2.save()
			return tran1.payable

		elif(type=='d'):
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=amount,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=-amount,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
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
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=x,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=-x,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
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
			tran1,created = cls.objects.get_or_create(current_user = current_user,amount = amount,payable=x,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
			tran1.users.add(new_friend)

			tran2,created = cls.objects.get_or_create(current_user = new_friend,amount = amount,payable=-x,type=type,desc=desc,tag=tag,split=0,amount_you=0,amount_friend=0,group=group)
			tran2.users.add(current_user)

			tran1.pair = tran2.pk
			tran1.current_user_pk = new_friend.pk
			tran1.save()

			tran2.pair = tran1.pk
			tran2.current_user_pk = current_user.pk
			tran2.save()
			return tran1.payable


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
class Pair(models.Model):
	current_user = models.ForeignKey(User, related_name='in_groups',null=True,on_delete=models.CASCADE)
	amount = models.IntegerField(default=0,blank=True)  

class Add_group(models.Model):
	
	GroupName = models.CharField(max_length=100,blank=True)
	Description = models.CharField(max_length = 100,blank=True)
	# Tag = models.CharField(max_length = 100,blank=True)
	group_pk = models.IntegerField(default=0,blank=True)  
	users = models.ManyToManyField(Pair)
	
	@classmethod 
	def creating_group(cls,current_user,desc,name,pk):
		group,created = cls.objects.get_or_create(group_pk=pk,Description=desc,GroupName=name)
		p = Pair(current_user=current_user)
		p.save()
		group.users.add(p)

	@classmethod
	def add_member(cls,current_user,pk):
		group,created = cls.objects.get_or_create(group_pk=pk)
		p = Pair(current_user=current_user)
		p.save()
		group.users.add(p)
		
	#group = models.ManyToManyField(GroupName)

	def __str__(self):
		return self.GroupName

class Group_Transactions(models.Model):
	group = models.ManyToManyField(Add_group)
	add_group_key = models.IntegerField(default=0,blank=True)
	Description = models.CharField(max_length = 100,blank=True)
	Tag = models.CharField(max_length = 100,blank=True)
	split = models.BooleanField(default=True)
	amt_paid_by_him = models.CharField(max_length = 10000000,blank=True)
	amt_for_him = models.CharField(max_length = 10000000,blank=True,default="")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	@classmethod
	def add_group_transaction(cls,desc,tag,split,str1,str2,d1,d2,pk):
		group_trans_obj,created = cls.objects.get_or_create(Description=desc,Tag=tag,split=split,amt_paid_by_him=str1,amt_for_him=str2)
		add_group_obj = Add_group.objects.get(group_pk=pk)
		group_trans_obj.group.add(add_group_obj)
		group_trans_obj.add_group_key = pk
		d3 = {}
		group_balance = {}
		g=[]
		activity = "Group: "+ add_group_obj.GroupName +" ; "
		for key,value in d1.items():
			d3[key] = value - d2[key]
			if d3[key] > 0:
				activity = activity +" " + key + " payed Rs." + str(value) + " to this group."
			elif d3[key] < 0:
				activity = activity + " " + key + " debted Rs." + str(value) + " into this group."
			else :
				activity = activity +" " + key + " got settled with this group."
		pairs = add_group_obj.users.all()
		for x in pairs:
			k = x.current_user.username
			v = x.amount
			group_balance[k] = v + d3[k]
			x.amount = group_balance[k]
			x.save()
		group_trans_obj.save()
		with open("test.txt", "a") as myfile:
			for key,value in d1.items():
				u = User.objects.get(username=key)
				myfile.write(str(u.pk)+","+ activity + "\n")
					#myfile.write(str(pk) + "," + request.user.username + " added " + desc + ". You borrowed " + str(x) + "\n")
			myfile.close()
		return d3



		# N = len(group_balance)
		# for key,value in group_balance.items():
		# 	g = g + [[key,value]]
		# # g=[[7,-10],[19,-10],[6,20]]
		# l1=[]
		# l2=[]
		# graph=[]
		# final={}
		# f={}
		# j=0
		# for i in g:
		# 	final[i[0]]=j
		# 	f[j]=final[i[0]]
		# 	j=j+1
		# for i in range(N):
		# 	l3=[]
		# 	for j in range(N):
		# 		l3=l3+[0]
		# 	graph=graph+[l3]
		# for i in g:
		# 	if(i[1] == 0):
		# 		continue
		# 	elif(i[1] > 0):
		# 		l1=l1+[i]
		# 	else:
		# 		l2=l2+[i]
		
		# def simplify(li1,li2,graph):
		# 	if(len(li1) == 0 or len(li2) == 0):
		# 		return
		# 	else:
		# 		y=li1[0]
		# 		if(y[1] + li2[0][1] == 0):
		# 			graph[final[y[0]]][final[li2[0][0]]] = graph[final[y[0]]][final[li2[0][0]]] + y[1]
		# 			simplify(li1[1:],li2[1:],graph)
		# 		elif(y[1] + li2[0][1] > 0):
		# 			graph[final[y[0]]][final[li2[0][0]]] = graph[final[y[0]]][final[li2[0][0]]] - li2[0][1]
		# 			y[1] = y[1]+li2[0][1]
		# 			simplify(li1,li2[1:],graph)
		# 		else:
		# 			graph[final[y[0]]][final[li2[0][0]]] = graph[final[y[0]]][final[li2[0][0]]] + y[1]
		# 			li2[0][1]=y[1]+li2[0][1]
		# 			simplify(li1[1:],li2,graph)
		# def f(l1,l2):
		# 	global graph
		# 	simplify(l1,l2,graph)

		# f(l1,l2)
		# l11=[]
		# # print(graph)
		# def getMin(arr): 	
		# 	minInd = 0
		# 	for i in range(1, N): 
		# 		if (arr[i] < arr[minInd]): 
		# 			minInd = i 
		# 	return minInd 
		# def getMax(arr): 
		# 	maxInd = 0
		# 	for i in range(1, N): 
		# 		if (arr[i] > arr[maxInd]): 
		# 			maxInd = i 
		# 	return maxInd 
		# def minOf2(x, y): 
		# 	return x if x < y else y 
		# def minCashFlowRec(amount): 
		# 	mxCredit = getMax(amount)
		# 	global l11
		# 	mxDebit = getMin(amount) 
		# 	if (amount[mxCredit] == 0 and amount[mxDebit] == 0): 
		# 		return 0
		# 	min = minOf2(-amount[mxDebit], amount[mxCredit]) 
		# 	amount[mxCredit] -=min
		# 	amount[mxDebit] += min
		# 	l11=l11+[[mxDebit,min,mxCredit]]
		# 	minCashFlowRec(amount) 
		# def minCashFlow(graph): 
		# 	amount = [0 for i in range(N)] 
		# 	for p in range(N): 
		# 		for i in range(N): 
		# 			amount[p] += (graph[i][p] - graph[p][i]) 
		# 	minCashFlowRec(amount)
		# minCashFlow(graph)
		# need = []
		# for i in range(N):
		# 	l3=[]
		# 	for j in range(N):
		# 		l3=l3+[0]
		# 	need = need + [l3]
		# for i in l11:
		# 	need[i[0]][i[2]] = i[1]

		# # print(need)