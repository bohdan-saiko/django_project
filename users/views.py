from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method != 'POST':
        form = UserLoginForm()
        return render(request, 'users/login.html', {'form': form})

    form = UserLoginForm(data=request.POST)
    
    if not form.is_valid():
        return render(request, 'users/login.html', {'form': form})

    user = form.get_user()
    auth_login(request, user)
    messages.success(request, f'Вітаємо, {user.username}!')
    return redirect('home')

def register(request):
    if request.method != 'POST':
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    form = UserRegisterForm(request.POST)

    if not form.is_valid():
        return render(request, 'users/register.html', {'form': form})

    form.save()
    username = form.cleaned_data.get('username')
    messages.success(request, f'Акаунт для {username} успішно створено!')
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'users/profile.html')