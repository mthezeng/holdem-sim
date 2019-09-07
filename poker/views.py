from django.shortcuts import render, redirect
from poker.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def home(request):
	return render(request, 'poker/poker.html')

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/poker')
	else:
		form = RegistrationForm()
		args = {'form': form}
		return render(request, 'poker/register.html', args)

def view_profile(request):
	args = {'user': request.user}
	return render(request, 'poker/profile.html', args)

def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('/poker/profile')
	else:
		form = EditProfileForm(instance=request.user)
		args = {'form': form, 'user': request.user}
		return render(request, 'poker/edit_profile.html', args)

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect('/poker/profile')
	else:
		form = PasswordChangeForm(user=request.user)
		args = {'form': form, 'user': request.user}
		return render(request, 'poker/change_password.html', args)
