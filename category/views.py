from django.shortcuts import render, redirect
from .models import Category
from .forms import CategoryForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/list.html', {'categories': categories})
