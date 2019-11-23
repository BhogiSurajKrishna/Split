from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import profileform,SignUpForm,groupform
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Friend
from django.http import HttpResponse
from django.contrib.auth.models import User

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

def home(request):
	return render(request,'home.html')

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

def friends(request):
	users = User.objects.exclude(id=request.user.id)
	try:
		friend,created = Friend.objects.get_or_create(current_user=request.user)
		friends = friend.users.all()
		args = {'user': request.user,'users': users,'friends':friends}
		return render(request,'friends.html',args)
	except Exception:
		"You have no friends :("

def add_friends(request,pk):
	users = User.objects.exclude(id=request.user.id)
	friend = Friend.objects.get(current_user=request.user)
	friends = friend.users.all()
	args = {'user': request.user,'users': users,'friends':friends}
	new_friend = User.objects.get(pk=pk)
	Friend.make_friend(request.user,new_friend)
	return render(request,'friends.html',args)

def create_group(request):
	friend = Friend.objects.get(current_user=request.user)
	friends = friend.users.all()
	groups = request.user.groups.all()
	args = {'user':request.user,'friends':friends,'groups':groups}
	return render(request,'groups.html',args)

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

def add_friends_to_group(request,pk):
	friend = Friend.objects.get(current_user=request.user)
	friends = friend.users.all()
	new_friend = request.user.groups.get(pk=pk)
	groups = new_friend.user_set.all()
	args = {'user': request.user,'friends':friends,'new_friend':new_friend,'groups':groups}
	return render(request,'in_group.html',args)

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


# def export_users_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="users.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['Username', 'First name', 'Last name', 'Email address'])

#     users = User.objects.all().values_list('username', 'first_name', 'last_name', 'last_login')
#     for user in users:
#         writer.writerow(user)

#     return response

