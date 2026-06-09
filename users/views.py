import threading
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
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

def send_email_async(subject, message, recipient_list):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Помилка фонової відправки листа: {e}")

def register(request):
    if request.method != 'POST':
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    form = UserRegisterForm(request.POST)

    if not form.is_valid():
        return render(request, 'users/register.html', {'form': form})

    user = form.save() 
    
    from .models import Profile
    Profile.objects.create(user=user)

    username = form.cleaned_data.get('username')
    user_email = form.cleaned_data.get('email')

    if user_email:
        email_thread = threading.Thread(
            target=send_email_async,
            args=(
                'Успішна реєстрація!',
                f'Привіт, {username}!\nТвій акаунт успішно створено.',
                [user_email]
            )
        )

        email_thread.start()

    messages.success(request, f'Акаунт для {username} успішно створено!')
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'users/profile.html')