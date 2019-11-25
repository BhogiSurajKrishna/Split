from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import profileform,SignUpForm,groupform,transform,editform,grouptransform,groupeditform
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from accounts.models import Friend,Transactions,Add_group,Pair,Group_Transactions
import os
import sys
import fileinput
import csv
import operator

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
			user_id = form.cleaned_data.get('userid')
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			p = user.profile
			p.userid = user_id
			p.save()
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
	# global A
	# temp = []
	# for x in A:
	# 	if x[0] == request.user.pk:
	# 		temp = temp + [x[1]]
	# args = {'list' : temp }
	with open("test.txt") as f:
		lines = f.read().splitlines()
		lines.reverse()
		f.close()
	line1=[]
	l3=[]
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
		trans1 = Transactions.objects.all().order_by('-updated')
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
			x = Transactions.add_transaction(request.user,new_friend,amount,type,desc,tag,split,amount_you,amount_friend,"")
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
			return render(request,'new_trans.html',{'form':form})

	else:
		form = transform()
		args = {'form' : form}
		return render(request, 'new_trans.html', args)

@login_required
def group_trans(request,pk):
	if request.method == 'POST':

		form = grouptransform(request.POST)
		if form.is_valid():
			# form.save()
			g = Group.objects.get(pk=pk)
			users = g.user_set.all()
			desc = form.cleaned_data.get('Description')
			tag = form.cleaned_data.get('Tag')
			amt_paid_by_him = form.cleaned_data.get('amt_paid_by_him')
			amt_for_him = form.cleaned_data.get('amt_for_him')
			split = form.cleaned_data.get('split')
			u,v,w,g1,z = [],[],{},[],{}
			total,expense,count = 0,0,0
			s = str(amt_paid_by_him).split(', ')
			for i in s:
				j=i.split(' : ')
				#u=u+[j]
				v= v + [j[0]]
				try:
					w[j[0]] = int(j[1])
				except:
					return render(request,'group_trans.html',{'form':form,'users':users,'group':g})
				total = total + int(j[1])
			v.sort()
			if(not split):
				e = str(amt_for_him).split(', ')
				for i in e:
					j=i.split(' : ')
					#u=u+[j]
					u = u + [j[0]]
					try:
						z[j[0]] = int(j[1])
					except:
						return render(request,'group_trans.html',{'form':form,'users':users,'group':g})
					expense = expense + int(j[1])
				u.sort()

			for uv in users:
				g1 = g1 + [uv.username]
				count=count+1

			if(split):
				each = int(total/count)
				for uv in users:
					z[uv.username] = each
			g1.sort()


			if(v == g1 and u == g1 and total == expense and (not split)):
				Group_Transactions.add_group_transaction(desc,tag,split,amt_paid_by_him,amt_for_him,w,z,pk)
				return redirect('/accounts/groups/'+pk)


			elif(split and v==g1):
				Group_Transactions.add_group_transaction(desc,tag,split,amt_paid_by_him,amt_for_him,w,z,pk)
				return redirect('/accounts/groups/'+pk)


			else:
				return render(request,'group_trans.html',{'form':form,'users':users,'group':g})

		else:
			return render(request,'group_trans.html',{'form':form,'users':users,'group':g})

	else:
		form = grouptransform()
		g = Group.objects.get(pk=pk)
		users = g.user_set.all()
		args = {'form' : form,'users':users,'group':g}
		return render(request, 'group_trans.html', args)

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
def edit_group_trans(request,pk):
	if request.method == 'POST':

		form = groupeditform(request.POST)
		if form.is_valid():
			# form.save()
			Description = form.cleaned_data.get('Description')
			Tag = form.cleaned_data.get('Tag')
			# Transactions.add_transaction()
			# Transactions.add_transaction(request.user,new_friend,amount,type,desc,tag)
			group_trans_obj = Group_Transactions.objects.get(pk=pk)
			d = group_trans_obj.Description
			e = group_trans_obj.Tag
			x = group_trans_obj.group.all()#get(pk=group_trans_obj.add_group_key)
			y = group_trans_obj.add_group_key
			add_group_obj = 2
			for t in x:
				add_group_obj = t
			group_trans_obj.Description = Description
			group_trans_obj.Tag = Tag
			group_trans_obj.save()
			group = request.user.groups.get(pk=t.group_pk)
			with open("test.txt", "a") as myfile:
				for u in group.user_set.all():
					if u == request.user:
						myfile.write(str(u.pk) + ",You have changed detail of a transaction of " + group.name + " of description " + str(d) + " to " + Description + " and tag " + str(e) + " to " + Tag + "\n")
					else: 
						myfile.write(str(u.pk) + "," + request.user.username + " has changed a transaction detail in a " +group.name+" with description " + str(d) + " to " + Description + " and tag " + str(e) + " to " + Tag + "\n")
				myfile.close()
			return redirect('/accounts/groups/'+ str(group.pk))

	else:
		form = groupeditform()
		args = {'form' : form}
		return render(request, 'edit_group_trans.html', args)



@login_required
def create_group(request):
	friend = Friend.objects.get(current_user=request.user)
	friends = friend.users.all()
	groups = request.user.groups.all()
	group_details = []
	for group in groups:
		add_group_obj = Add_group.objects.get(group_pk=group.pk)
		pairs = add_group_obj.users.all()
		user_pair = pairs.get(current_user=request.user)
		count = user_pair.amount
		if count > 0:
			group_details = group_details + ["You are owed "+"Rs."+ str(count)]
		elif count < 0:
			group_details = group_details + ["You owe " +"Rs." + str(-count)]
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
			# form.save()
			GroupName = form.cleaned_data.get('GroupName')
			desc = form.cleaned_data.get('Description')
			g1,created = Group.objects.get_or_create(name=GroupName)
			perm = Permission.objects.all()
			g1.permissions.set(perm)
			g1.save()
			g1.user_set.add(request.user)

			Add_group.creating_group(request.user,desc,GroupName,g1.pk)

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
	trans_total = []
	strings = []
	all_group_trans = Group_Transactions.objects.all().order_by('-updated')
	for g in all_group_trans:
		fin={}
		if g.add_group_key == int(pk):
			v,w,total,count,z = [],{},0,0,{}
			str1 = g.amt_paid_by_him
			str2 = g.amt_for_him
			s = str(str1).split(', ')
			for i in s:
				j=i.split(' : ')
				#u=u+[j]
				v= v + [j[0]]
				w[j[0]] = int(j[1])
				total = total + int(j[1])
				count = count + 1
			e = str(str2)
			if(e == ""):
				for key,value in w.items():
					fin[key] = value - total/count
			else:
				e = str(str2).split(', ')
				for i in e:
					j=i.split(' : ')
					#u=u+[j]
					v= v + [j[0]]
					z[j[0]] = int(j[1])
				for key,value in w.items():
					fin[key] = value - z[key]
			strings=["Description: " + g.Description + " " + " "+" Tag: " + g.Tag]
			for key,value in fin.items():
				if(value > 0):
					strings = strings + [key + " has to get back Rs."+ str(value) + " from this group"]
				elif(value < 0):
					strings = strings + [key + " has to give Rs."+ str(-value) + " to this group"]
				else:
					strings = strings + [key + " has all settled up with this group"]
			trans_total = trans_total + [[g.pk,strings]]

	args = {'user': request.user,'friends':friends,'new_friend':new_friend,'groups':groups,'detail': trans_total}
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

	group_object = Add_group.objects.get(group_pk=pk1)
	group_object.add_member(new_friend,pk1)


	with open("test.txt", "a") as myfile:
		for u in group.user_set.all():
			if u == request.user:
				activity = "You added " + new_friend.username +" into " + group.name
			elif u == new_friend:
				activity = request.user.username + " added you "+" into " + group.name
			else:
				activity = request.user.username + " added "+ new_friend.username+" into " + group.name
			myfile.write(str(u.pk)+","+ activity + "\n")
					#myfile.write(str(pk) + "," + request.user.username + " added " + desc + ". You borrowed " + str(x) + "\n")
		myfile.close()
	args = {'user': request.user,'friends':friends,'new_friend':new_friend,'groups':groups}
	return redirect('/accounts/groups/'+pk1)


@login_required
def show_balances(request,pk):
	this_group = request.user.groups.get(pk=pk)
	# friends = this_group.user_set.all()
	# all_trans = Transactions.objects.all()
	# names = []
	# detail = []
	# total = 0
	# for f in friends:
	# 	if not f == request.user:
	# 		names = names + [f.username]
	# 		count = 0
	# 		for tran in all_trans:
	# 			if tran.current_user == request.user and tran.current_user_pk == f.pk and tran.group == this_group.name:
	# 				count = count + tran.payable
	# 		total = total + count
	# 		if count > 0:
	# 			detail = detail + ["You owe "+"Rs."+ str(count)]
	# 		elif count < 0:
	# 			detail = detail + ["owes you " +"Rs." + str(-count)]
	# 		elif count == 0:
	# 			detail = detail + ["Settled up"]
	names = []
	detail = []
	add_group_obj = Add_group.objects.get(group_pk=pk)
	pairs = add_group_obj.users.all()
	names = [request.user.username]
	user_pair = pairs.get(current_user=request.user)
	if user_pair.amount > 0:
		detail = detail + ["You are owed "+"Rs."+ str(user_pair.amount) + " from group"]
	elif user_pair.amount < 0:
		detail = detail + ["You owe "+"Rs."+ str(-user_pair.amount) + " to group"]
	else:
		detail = detail + ["You are Settled"]
	for p in pairs:
		if not p.current_user.username == request.user.username:
			names = names + [p.current_user.username]
			if p.amount > 0:
				detail = detail + ["Owed "+"Rs."+ str(p.amount) + " from group"]
			elif p.amount < 0:
				detail = detail + ["Owes "+"Rs."+ str(-p.amount) + " to group"]
			else:
				detail = detail + ["Settled"]
	args = {'user': request.user,'this_group':this_group,'names':names,'detail':detail}
	return render(request,'balances.html',args)


@login_required
def exit(request,pk):
	add_group_obj = Add_group.objects.get(group_pk=pk)
	gname = add_group_obj.GroupName
	pairs = add_group_obj.users.all()
	pair = add_group_obj.users.get(current_user=request.user)
	group = request.user.groups.get(name=gname)
	
	if(pair.amount == 0):
		group.user_set.remove(request.user)
		group.save()
		add_group_obj.users.remove(pair)
		add_group_obj.save()
		Pair.objects.filter(id=pair.pk).delete()
		# 
		Pair.save()
		with open("test.txt", "a") as myfile:
				myfile.write(str(request.user.pk) + ",You Have Exited from "+gname+"\n")
				myfile.close()
		return redirect('/accounts/groups/')
	else:
		return redirect('/accounts/groups/' + str(pk))

@login_required
def insights(request):

	# my_user = request.user
	# trans_objs = Transactions.objects.all()


	chart1 = {
		'chart':{'type':'pie'},
		'title':{'text':'Pie Chart for Expenditure with Tags'},
		'series': [{
			'name':'Total Transaction Amount',
			'data':list(map(lambda row1,row2:{'name':row1,'y':row2},l1,l2))
		}]
	}


def mincashflow(amount, answer):
    max_index = max(amount.items(), key=operator.itemgetter(1))[0]
    min_index = min(amount.items(), key=operator.itemgetter(1))[0]
    if amount[max_index] == 0 and amount[min_index] == 0:
        return answer

    small = min(-amount[min_index], amount[max_index])
    amount[max_index] -= small
    amount[min_index] += small
    answer + [[max_index, min_index, small]]
    mincashflow(amount, answer)
    return answer


@login_required
def settleup(request,pk):
		add_grp_obj = Add_group.objects.get(group_pk = pk)
		grp_name = add_grp_obj.GroupName
		grp_desc = ""
		grp_tag = ""
		grp_balances = add_grp_obj.users.all()
		g = {}
		for i in grp_balances:
			g[i.current_user.username] = int(i.amount)

		N = len(g)
		l1=[]
		l2=[]
		graph=[]
		final={}
		f={}
		j=0
		for k,v in g.items():
			final[k]=j
			f[j]=k
			j=j+1
		for i in range(N):
			l3=[]
			for j in range(N):
				l3=l3+[0]
			graph=graph+[l3]
		g1=g.copy()
		ans=mincashflow(g1,[])
		for i in ans:
			graph[final[i[0]]][final[i[1]]] = i[2]
		h=graph
		l5=[]
		for k,v in g.items():
			l5 = l5+[[k,v]]
		my_user_no = final[request.user.username]
		li3 = graph[my_user_no]
		for k in range(len(li3)):
			if(int(li3[k]) > 0):
				friend = f[k]
				user = User.objects.get(username = friend)
				tran1,created = Transactions.objects.get_or_create(current_user = request.user,amount = int(li3[k]),payable=int(li3[k]),type='d',desc=grp_desc,tag=grp_tag,split=0,amount_you=0,amount_friend=0,group=grp_name)
				tran1.users.add(user)
				tran2,created = Transactions.objects.get_or_create(current_user = user,amount = int(li3[k]),payable=-int(li3[k]),type='d',desc=grp_desc,tag=grp_tag,split=0,amount_you=0,amount_friend=0,group=grp_name)
				tran2.users.add(request.user)
				tran1.pair = tran2.pk
				tran1.current_user_pk = request.user.pk
				tran1.save()

				tran2.pair = tran1.pk
				tran2.current_user_pk = user.pk
				tran2.save()
				tran1.status = 1
				tran1.save()
				tran2.status = 1
				tran2.save()
				x = tran1.payable
				if x > 0:
					with open("test.txt", "a") as myfile:
						myfile.write(str(request.user.pk) + ",You Settled " + tran1.desc + " by paying " + str(x) + " .Rs to " + tran1.current_user.username + "\n")
						myfile.write(str(tran1.current_user.pk) + "," + request.user.username + " Settled " + tran1.desc + " by paying "+ str(x) + " .Rs to You" + "\n")
						myfile.close()
				elif x < 0:
					with open("test.txt", "a") as myfile:
						myfile.write(str(request.user.pk) + ",You Settled " + tran1.desc + " by receiving " + str(-x) + " .Rs from " + tran1.current_user.username + "\n")
						myfile.write(str(tran1.current_user.pk) + "," + request.user.username + " Settled " + tran1.desc + " by receiving " + str(-x) + " .Rs from You" + "\n")
						myfile.close()
				g[friend] = g[friend] - int(li3[k])
				g[request.user.username] = g[request.user.username] + int(li3[k])
		for i in range(N):
			if(int(graph[i][my_user_no]) > 0):
				amt=int(graph[i][my_user_no])
				friend = f[i]
				user = User.objects.get(username = friend)
				tran1,created = Transactions.objects.get_or_create(current_user = request.user,amount = amt,payable=-amt,type='c',desc=grp_desc,tag=grp_tag,split=0,amount_you=0,amount_friend=0,group=grp_name)
				tran1.users.add(user)

				tran2,created = Transactions.objects.get_or_create(current_user = user,amount = amt,payable=amt,type='c',desc=grp_desc,tag=grp_tag,split=0,amount_you=0,amount_friend=0,group=grp_name)
				tran2.users.add(request.user)

				tran1.pair = tran2.pk
				tran1.current_user_pk = request.user.pk
				tran1.save()

				tran2.pair = tran1.pk
				tran2.current_user_pk = user.pk
				tran2.save()
				tran1.status = 1
				tran1.save()
				tran2.status = 1
				tran2.save()
				x = tran1.payable
				if x > 0:
					with open("test.txt", "a") as myfile:
						myfile.write(str(request.user.pk) + ",You Settled " + tran1.desc + " by paying " + str(x) + " .Rs to " + tran1.current_user.username + "\n")
						myfile.write(str(tran1.current_user.pk) + "," + request.user.username + " Settled " + tran1.desc + " by paying "+ str(x) + " .Rs to You" + "\n")
						myfile.close()
				elif x < 0:
					with open("test.txt", "a") as myfile:
						myfile.write(str(request.user.pk) + ",You Settled " + tran1.desc + " by receiving " + str(-x) + " .Rs from " + tran1.current_user.username + "\n")
						myfile.write(str(tran1.current_user.pk) + "," + request.user.username + " Settled " + tran1.desc + " by receiving " + str(-x) + " .Rs from You" + "\n")
						myfile.close()
				g[friend] = g[friend] + graph[i][my_user_no]
				g[request.user.username] = g[request.user.username] - graph[i][my_user_no]
		pairs = add_grp_obj.users.all()
		
		for x in pairs:
			k = x.current_user.username
			# group_balance[k] = v + d3[k]
			x.amount = g[k]
			x.save()
		# group_trans_obj.save()
		# li4 = need[:][my_user_no] 
		g1 = g.keys()
		g2 = g.values()
		#args={'li3':li3,'a':a,'b':b,'c':c,'d':d,'g1':g1,'g2':g2}

		return render(request,'check.html',{'h':h,'l5':l5})
