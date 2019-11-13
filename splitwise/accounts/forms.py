from django import forms
from accounts.models import profile,add_group
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,forms

class profileform(forms.ModelForm):
	class Meta:
		model = profile
		fields = ['firstname','secondname','email','number' , 'city','image']

class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=254,required=False)
	userid = forms.CharField(max_length=254,required=True)
	class Meta:
		model = User
		fields = ['username', 'userid','email', 'password1', 'password2']

class groupform(forms.ModelForm):
	class Meta:
		model = add_group
		fields = ['GroupName','Description']
