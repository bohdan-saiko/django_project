from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Test
from .forms import TestFrom

def test_view(request):
    tests = Test.objects.all()
    return render(request, "test/index.html", { "tests": tests })

@login_required
def create_test_view(request):
    if request.method == 'POST':
        form = TestFrom(request.POST)
        if form.is_valid():
            test_item = form.save(commit=False)
            
            test_item.author = request.user
            
            test_item.save()
            
            return redirect("home") 
    else:
        form = TestFrom()
        
    return render(request, "test/create-test.html", {"form": form})


    