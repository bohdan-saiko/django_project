from django.urls import path
from .views import category_create, category_list

urlpatterns = [
    path('', category_list, name='category_list'),
    path('add/', category_create, name='category_create'),
]