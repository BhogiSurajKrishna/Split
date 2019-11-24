from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import profileform,SignUpForm,groupform,transform,editform
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from accounts.models import Friend,Transactions#,add_debt
from django.contrib import messages
import os
import sys
import fileinput

def profile(request):

	if request.method == 'POST':

		form = profileform(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	else:
		form = profileform()
		args = {'form' : form}
		return render(request, 'profile.html', args)

def SignUp(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
		else:
			form = SignUpForm()
			return render(request, 'signup.html', {'form': form})
	else:
		form = SignUpForm()
		return render(request, 'signup.html', {'form': form})

@login_required
def home(request):
	return render(request,'home.html')

@login_required
def activity(request):
	with open("test.txt") as f:
		lines = f.read().splitlines()
		f.close()
	line1=[]
	l3=[]
	lines.reverse()
	for l in lines:
		u = l.split(',',1)
		#l[0]=int(l[0])
		line1=line1+[u]
	for l2 in line1:
		if l2[0] == str(request.user.pk):
			l3.append(l2[1])
	args = {'list' : l3 }
	return render(request,'activity.html',args)

@login_required
def edit_profile(request):
	try:
		prof = request.user.profile
	except ObjectDoesNotExist:
		prof = profile(user=request.user)
	if request.method == 'POST':

		form = profileform(request.POST,request.FILES,instance=prof)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()
			with open("test.txt", "a") as myfile:
				myfile.write(str(request.user.pk) + ",You edited the Personal Information \n")
				myfile.close()
			return redirect('/')

	else:
		form = profileform(instance=prof)
		args = {'form' : form}
		return render(request, 'profile.html', args)

@login_required
def friends(request):
	users = User.objects.exclude(id=request.user.id)
	try:
		friend,created = Friend.objects.get_or_create(current_user=request.user)
		friends = friend.users.all()
		trans1 = Transactions.objects.all()
		trans2=trans1
		exp = []
		pos=0
		neg=0
		for x in friends:
			count = 0
			for tran in trans1:
				if tran.current_user == x and tran.status == 0 and tran.current_user_pk == request.user.pk:
					count = count + tran.payable
			if count<0:
				neg=neg+count
				exp = exp + ["owes you " +"Rs." + str(-count)]
			elif count>0:
				pos=pos+count
				exp = exp + ["You owe "+"Rs."+ str(count)]
			elif count==0:
				exp = exp + ["Settled up"]
		args = {'user': request.user,'users': users,'friends':friends,'trans1':trans2,'friend':friend,'exp':exp,'pos':pos,'neg':-neg}
		return render(request,'friends.html',args)
	except Exception:
		"You have no friends :("

@login_required
def add_friends(request,pk):
	users = User.objects.exclude(id=request.user.id)
	friend = Friend.objects.get(current_user=request.user)
	friends = friend.users.all()
	new_friend = User.objects.get(pk=pk)
	Friend.make_friend(request.user,new_friend)
	#add_debt.add_debting(request.user,new_friend)
	trans1 = Transactions.objects.all().order_by('-updated')
	# trans1 = Transactions.objects.get(desc="Kriti",current_user=request.user)

	# trans2=trans1
	args = {'user': request.user,'users': users,'friends':friends,'friend':friend}
	# friends(request)
	with open("test.txt", "a") as myfile:
		myfile.write(str(request.user.pk) + ",You added " + new_friend.username + " to your's friend's list \n")
		myfile.write(str(pk) + "," + request.user.username + " added You to his friend's list \n")
		myfile.close()
	return redirect('/accounts/friends')
	# return render(request,'friends.html',args)

@login_required
def friend_detail(request,pk):
	users = User.objects.exclude(id=request.user.id)
	new_friend = User.objects.get(pk=pk)
	trans1 = Transactions.objects.all().order_by('-updated')
	trans=trans1
	current_user_pk = request.user.pk
	#trans = trans1.users.all()

	args = {'new_friend':new_friend,'trans':trans,'current_user_pk':current_user_pk}
	return render(request,'friend_detail.html',args)
	# return redirect('/accounts/friends')

@login_required
def new_trans(request,pk):
	if request.method == 'POST':

		form = transform(request.POST)
		if form.is_valid():
			# form.save()
			amount = form.cleaned_data.get('amount')
			type = form.cleaned_data.get('type')
			desc = form.cleaned_data.get('desc')
			tag = form.cleaned_data.get('tag')
			split = form.cleaned_data.get('split')
			amount_you = form.cleaned_data.get('amount_you')
			amount_friend = form.cleaned_data.get('amount_friend')
			new_friend = User.objects.get(pk=pk)
			if((type != 'e' and type != 'f') or (type == 'e' and amount_friend + amount_you == 100) or (type == 'f' and amount_friend + amount_you == amount)):
				x = Transactions.add_transaction(request.user,new_friend,amount,type,desc,tag,split,amount_you,amount_friend)
				if x < 0:
				#A = A + [[request.user.pk,"You added "+ desc + " .You borrowed " + str(x) ]] + [[pk,request.user.username +" added " + desc + ". You lent " + str(x)]]
					with open("test.txt", "a") as myfile:
						myfile.write(str(request.user.pk) + ",You added " + desc + " .You borrowed " + str(-x) + "\n" )
						myfile.write(str(pk) + "," + request.user.username + " added " + desc + ". You lent " + str(-x) + "\n")
						myfile.close()
				elif x > 0:
				#A = A + [[request.user.pk,"You added "+ desc + " .You lent " + str(-x) ]] + [[pk,request.user.username +" added " + desc + ". You borrowed " + str(-x)]]
					with open("test.txt", "a") as myfile:
						myfile.write(str(request.user.pk) + ",You added " + desc + " .You lent " + str(x) + "\n")
						myfile.write(str(pk) + "," + request.user.username + " added " + desc + ". You borrowed " + str(x) + "\n")
						myfile.close()			
				return redirect('/accounts/friends/'+ pk)
			else:
				# messages.error(request, 'Document deleted.')
				return render(request,'new_trans.html',{'form':form})
		else:
			# messages.error(request, 'Form not valid.')
			return render(request,'new_trans.html',{'form':form})

	else:
		form = transform()
		args = {'form' : form}
		return render(request, 'new_trans.html', args)

@login_required
def edit_trans(request,pk,pk1):
	if request.method == 'POST':

		form = editform(request.POST)
		if form.is_valid():
			# form.save()
			desc = form.cleaned_data.get('desc')
			tag = form.cleaned_data.get('tag')
			# Transactions.add_transaction()
			# Transactions.add_transaction(request.user,new_friend,amount,type,desc,tag)
			trans = Transactions.objects.get(pk=pk)
			d=trans.desc
			e=trans.tag
			trans.desc = desc
			trans.tag = tag
			trans.save()
			trans1 = Transactions.objects.get(pk=trans.pair)
			trans1.desc = desc
			trans1.tag = tag
			trans1.save()
			with open("test.txt", "a") as myfile:
				myfile.write(str(request.user.pk) + ",You have changed detail of a transaction with " + trans1.current_user.username + " of description " + str(d) + " to " + desc + " and tag " + str(e) + " to " + tag + "\n")
				myfile.write(str(trans1.current_user_pk) + "," + request.user.username + " has changed a transaction detail with description " + str(d) + " to " + desc + " and tag " + str(e) + " to " + tag + "\n")
				myfile.close()
			return redirect('/accounts/friends/'+ pk1)

	else:
		form = editform()
		args = {'form' : form}
		return render(request, 'edit_trans.html', args)

@login_required
def create_group(request):
	friend = Friend.objects.get(current_user=request.user)
	friends = friend.users.all()
	groups = request.user.groups.all()
	all_trans = Transactions.objects.all()
	group_details = []
	for group in groups:
		count = 0
		for tran in all_trans:
			if tran.group == group.name:
				count = count + tran.payable
		if count > 0:
			group_details = group_details + ["You owe "+"Rs."+ str(count)]
		elif count < 0:
			group_details = group_details + ["owes you " +"Rs." + str(-count)]
		elif count == 0:
			group_details = group_details + ["All Settled"]
	args = {'user':request.user,'friends':friends,'groups':groups , 'group_details': group_details}
	return render(request,'groups.html',args)

@login_required
def settle(request,pk1,pk2,pk):
	tran1 = Transactions.objects.get(pk=pk1)
	tran1.status = 1
	tran1.save()
	tran2 = Transactions.objects.get(pk=pk2)
	tran2.status = 1
	tran2.save()
	x = tran1.payable
	if x > 0:
		#A = A + [[request.user.pk,"You Settled "+ tran1.desc + " by paying " + str(x) + " .Rs to " + tran2.current_user.username
		#]] + [[tran2.current_user.pk,request.user.username +" Settled " + tran1.desc + " by paying "+ str(x)+ " .Rs to You" ]]
		with open("test.txt", "a") as myfile:
			myfile.write(str(request.user.pk) + ",You Settled " + tran1.desc + " by paying " + str(x) + " .Rs to " + tran1.current_user.username + "\n")
			myfile.write(str(tran1.current_user.pk) + "," + request.user.username + " Settled " + tran1.desc + " by paying "+ str(x) + " .Rs to You" + "\n")
			myfile.close()
	elif x < 0:
		#A = A + [[request.user.pk,"You Settled "+ tran1.desc + " by receiving " + str(-x) + " .Rs from " + tran2.current_user.username
		#]] + [[tran1.current_user.pk,request.user.username +" Settled " + tran1.desc + " by receiving "+ str(-x)+ " .Rs from You" ]]
		with open("test.txt", "a") as myfile:
			myfile.write(str(request.user.pk) + ",You Settled " + tran1.desc + " by receiving " + str(-x) + " .Rs from " + tran1.current_user.username + "\n")
			myfile.write(str(tran1.current_user.pk) + "," + request.user.username + " Settled " + tran1.desc + " by receiving " + str(-x) + " .Rs from You" + "\n")
			myfile.close()
	return redirect('/accounts/friends/'+ pk)

@login_required
def add_group(request):

	if request.method == 'POST':

		form = groupform(request.POST)
		if form.is_valid():
			form.save()
			GroupName = form.cleaned_data.get('GroupName')
			g1,created = Group.objects.get_or_create(name=GroupName)
			perm = Permission.objects.all()
			g1.permissions.set(perm)
			g1.save()
			g1.user_set.add(request.user)

			with open("test.txt", "a") as myfile:
				myfile.write(str(request.user.pk) + ",You created "+GroupName+"\n")
				myfile.close()		
			#request.user.groups.add(g1)
			return redirect('/accounts/groups')

	else:
		form = groupform()
		args = {'form' : form}
		return render(request, 'group_form.html', args)

@login_required
def add_friends_to_group(request,pk):
	#users = User.objects.exclude(id=request.user.id)
	friend = Friend.objects.get(current_user=request.user)
	friends = friend.users.all()
	new_friend = request.user.groups.get(pk=pk)
	groups = new_friend.user_set.all()
	#groups = request.user.groups.all()
	args = {'user': request.user,'friends':friends,'new_friend':new_friend,'groups':groups}
	#Friend.make_friend(request.user,new_friend)
	return render(request,'in_group.html',args)

@login_required
def add_friends_to_group_new(request,pk1,pk2):
	friend = Friend.objects.get(current_user=request.user)
	friends = friend.users.all()
	new_friend = User.objects.get(pk=pk2)
	group = request.user.groups.get(pk=pk1)
	group.user_set.add(new_friend)
	group.save()
	groups = group.user_set.all()
	with open("test.txt", "a") as myfile:
		myfile.write(str(request.user.pk) + ",You added "+new_friend.username+" into "+group.name+"\n")
		myfile.write(str(pk2) + ","+ request.user.username +" added you into "+group.name+"\n")
		myfile.close()	
	args = {'user': request.user,'friends':friends,'new_friend':new_friend,'groups':groups}
	return redirect('/accounts/groups/'+pk1)

@login_required
def settleup(request):
	
	return redirect('/accounts/groups/')

@login_required
def show_balances(request,pk):
	this_group = request.user.groups.get(pk=pk)
	friends = this_group.user_set.all()
	all_trans = Transactions.objects.all()
	names = []
	detail = []
	total = 0
	for f in friends:
		if not f == request.user:
			names = names + [f.username]
			count = 0
			for tran in all_trans:
				if tran.current_user == request.user and tran.current_user_pk == f.pk and tran.group == this_group.name:
					count = count + tran.payable
			total = total + count
			if count > 0:
				detail = detail + ["You owe "+"Rs."+ str(count)]
			elif count < 0:
				detail = detail + ["owes you " +"Rs." + str(-count)]
			elif count == 0:
				detail = detail + ["Settled up"]
	args = {'user': request.user,'this_group':this_group,'names':names,'detail':detail,'total':total}
	return render(request,'balances.html',args)

