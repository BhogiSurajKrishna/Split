from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import profileform,SignUpForm,groupform,transform
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from accounts.models import Friend,Transactions#,add_debt

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
				if tran.current_user == x and tran.status == 0:
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
	trans1 = Transactions.objects.all()
	# trans1 = Transactions.objects.get(desc="Kriti",current_user=request.user)

	# trans2=trans1
	args = {'user': request.user,'users': users,'friends':friends,'friend':friend}
	# friends(request)
	# return redirect('/accounts/friends')
	return render(request,'friends.html',args)

@login_required
def friend_detail(request,pk):
	users = User.objects.exclude(id=request.user.id)
	new_friend = User.objects.get(pk=pk)
	trans1 = Transactions.objects.all()
	trans=trans1
	#trans = trans1.users.all()

	args = {'new_friend':new_friend,'trans':trans}
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
			# Transactions.add_transaction()
			new_friend = User.objects.get(pk=pk)
			Transactions.add_transaction(request.user,new_friend,amount,type,desc,tag)
			return redirect('/accounts/friends/'+ pk)

	else:
		form = transform()
		args = {'form' : form}
		return render(request, 'new_trans.html', args)

@login_required
def create_group(request):
	friend = Friend.objects.get(current_user=request.user)
	friends = friend.users.all()
	groups = request.user.groups.all()
	args = {'user':request.user,'friends':friends,'groups':groups}
	return render(request,'groups.html',args)

@login_required
def settle(request,pk1,pk2,pk):
	tran1 = Transactions.objects.get(pk=pk1)
	tran1.status = 1
	tran1.save()
	tran2 = Transactions.objects.get(pk=pk2)
	tran2.status = 1
	tran2.save()
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

# def add_friends_to_group_new(request,pk):
# 	friend = Friend.objects.get(current_user=request.user)
# 	friends = friend.users.all()
# 	#new_friend = User.objects.get(pk=pk2)
# 	group = request.user.groups.get(pk=pk)
# 	group.user_set.add(new_friend)
# 	group.save()
# 	#groups = new_friend.user_set.all()
# 	args = {'user': request.user,'friends':friends,'groups':groups}
# 	return render(request,'in_group.html',args)

@login_required
def add_friends_to_group_new(request,pk1,pk2):
	friend = Friend.objects.get(current_user=request.user)
	friends = friend.users.all()
	new_friend = User.objects.get(pk=pk2)
	group = request.user.groups.get(pk=pk1)
	group.user_set.add(new_friend)
	group.save()
	groups = group.user_set.all()
	args = {'user': request.user,'friends':friends,'new_friend':new_friend,'groups':groups}
	return render(request,'in_group.html',args)


