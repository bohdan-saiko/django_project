from django.shortcuts import render, redirect
from .models import Category
from .forms import CategoryForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/list.html', {'categories': categories})

def category_create(request):
    if request.method != 'POST':
        form = CategoryForm()
        return render(request, 'category/form.html', {'form': form})

    form = CategoryForm(request.POST)
    if not form.is_valid():
        return render(request, 'category/form.html', {'form': form})

    form.save()
    return redirect('category_list')