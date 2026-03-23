from django.urls import path
from .views import auth, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth, name="auth"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile, name="profile")
]
