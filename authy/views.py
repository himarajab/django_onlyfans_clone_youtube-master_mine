from post.models import Post
from tier.models import Tier,Subscription
from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm,NewListForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from authy.models import Profile,PeopleList
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.core.paginator import Paginator

from django.urls import resolve

def side_nav_info(request):
	user = request.user
	nav_profile = None
	fans = None
	follows = None

	if user.is_authenticated:
		nav_profile = Profile.objects.get(user=user)
		fans = Subscription.objects.filter(subscribed=user).count()
		follows = Subscription.objects.filter(subscriber=user).count()
	return {'nav_profile': nav_profile, 'fans': fans, 'follows': follows}
	

def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	tiers = Tier.objects.filter(user=user)

	posts_count = Post.objects.filter(user=user).count()

	# select favourite people list 
	favorite_list = PeopleList.objects.filter(user=request.user)


	# new favourie list form 
	if request.method == 'POST':
		form = NewListForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data.get('title')
			PeopleList.objects.create(title=title,user=request.user)
			return HttpResponseRedirect(reverse('profile',args=[username]))
	else:
  		form = NewListForm()


	template = loader.get_template('profile.html')

	context = {
	'profile':profile,'tiers':tiers,'posts_count':posts_count,'form':form,
	'favorite_list':favorite_list,
	}

	return HttpResponse(template.render(context, request))




def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('login')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'registration/signup.html', context)


@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'registration/change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'registration/change_password_done.html')


@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	user_basic_info =User.objects.get(id=user)

	if request.method == 'POST':
		# when open the form populate it with profile data 
		form = EditProfileForm(request.POST, request.FILES,instance=profile)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.banner = form.cleaned_data.get('banner')
			# we get the first and last name from the user model not the profile
			user_basic_info.first_name = form.cleaned_data.get('first_name')
			user_basic_info.last_name = form.cleaned_data.get('last_name')
			# 
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			user_basic_info.save()
			return redirect('index')
	else:
		form = EditProfileForm(instance=profile)

	context = {
		'form':form,
	}

	return render(request, 'registration/edit_profile.html', context)


