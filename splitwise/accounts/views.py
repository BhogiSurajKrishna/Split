from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.views import login
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import profileform,SignUpForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def SignUp(request):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
# Create your views here.

def profile(request):
	# try:
	# 	profile_instance = profile.objects.get(user=request.User)
	# except:
	# 	profile_instance = profile(user=request.User)
	if request.method == 'POST':
	
		form = profileform(request.POST)
		if form.is_valid():
			form.save() 
			return redirect('/')

	else:
		form = profileform()
		args = {'form' : form}
		return render(request, 'profile.html', args)
		# return HttpResponse("<h1>enduku puttav ra"+s+"</h1>")

def SignUp(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home.html')
	else:
		form = SignUpForm()
		return render(request, 'signup.html', {'form': form})

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
