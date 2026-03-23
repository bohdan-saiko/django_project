from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def auth(request):
    form = UserRegisterForm() 
    return render(request, 'users/auth.html', {'form': form})

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

def profile(request):
    return render(request, 'users/profile.html')