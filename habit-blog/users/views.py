from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdationForm
# Create your views here.


'''This register view creates an account and user and redirects to login which has to e done by user'''
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'You have successfully created an account. You can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


'''This new register view creates a new account for the user and logs in for them and redirects them to home page of website directly'''
def registerNew(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, f'You have successfully created an account.')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def updateProfile(request):
    if request.method == 'POST':
        form = UserUpdationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your details have been updated successfully')
            return redirect('profile')
    else:
        form = UserUpdationForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})