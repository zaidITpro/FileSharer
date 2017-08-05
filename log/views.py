from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from log.forms import signup_form,login_form
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
import requests
from bs4 import BeautifulSoup


def home(request):
	return render(request,"home.html")

def signup(request):
	if request.method=="POST":
		form=signup_form(request.POST or None)
		if form.is_valid():
			user_name=form.cleaned_data['user_name']
			try:
				User.objects.get(username=user_name)
				error="This username is already registered"
				return render(request,'signup.html',{'form':form,'error':error})
			except:
				IntegrityError
			useremail=request.POST.get('user_email')
			try:
				User.objects.get(email=useremail)
				error="User with this email already exist"
				return render(request,"signup.html",{'form':form,'error':error})
			except:
				ObjectDoesNotExist
			user_password=request.POST.get('user_password')
			if len(user_password)<8:
				error="Password length should not be less than 8"
				return render(request,"signup.html",{'form':form,'error':error})
			user_confirmpassword=request.POST.get('user_confirmpassword')
			if user_password!=user_confirmpassword:
				error="password do not match"
				return render(request,'signup.html',{'form':form,'error':error})
			user_email=form.cleaned_data['user_email']
			user_password=form.cleaned_data['user_password']
			user=User.objects.create_user(username=user_name,password=user_password,email=user_email)
			return redirect('loggedin')
	else:
		form=signup_form()
	args={}
	args.update(csrf(request))
	return render(request,"signup.html",{'form':form})




def signin(request):
	if request.method=="POST":
		form=login_form(request.POST)
		user=authenticate(username=request.POST.get('user_name'),password=request.POST.get('user_password'))
		if user is not None:
			login(request,user)
			return redirect('user')
		else:
			error="Username and password do not match"
			return render(request,'login.html',{'form':form,'error':error})
	form=login_form()
	return render(request,'login.html',{'form':form})


def user(request):
	if request.user.is_authenticated():
		rt_list=crawl_list()
		return render(request,'user/user.html',{"rt_list":rt_list})
	else:
		return redirect('signin')

def loggedin(request):
	return render(request,'loggedin.html')

def logout_view(request):
	logout(request)
	return redirect('signin')


#functions called by the user view
def crawl_list():
	url='https://www.rt.com'
	response=requests.get(url)
	html=response.content
	soup=BeautifulSoup(html)
	rt_news=soup.findAll('div',attrs={'class':'main-promobox__wrapper'})
	news_list=[]
	k=0
	for j in rt_news:

		news_list.insert(k,str(j))
		if k==5:
			break
		k+=1
	return news_list