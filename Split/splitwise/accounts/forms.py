from django import forms
from accounts.models import profile,Add_group,Transactions,Group_Transactions
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
		model = Add_group
		fields = ['GroupName','Description']
class transform(forms.ModelForm):
	class Meta:
		model = Transactions
		fields = ['amount','type','desc','tag','split','amount_you','amount_friend']
class editform(forms.ModelForm):
	class Meta:
		model = Transactions
		fields = ['desc','tag']
class grouptransform(forms.ModelForm):
	class Meta:
		model = Group_Transactions
		fields = ['Description','Tag','amt_paid_by_him','amt_for_him','split']

