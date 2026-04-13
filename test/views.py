from django.shortcuts import render, redirect
from .models import Test
from .forms import TestFrom

def test_view(request):
    tests = Test.objects.all()
    return render(request, "test/index.html", { "tests": tests })

def create_test_view(request):
    if request.method != 'POST':
        form = TestFrom()
        return render(request, "test/create-test.html", { "form": form })
    
    form = TestFrom(request.POST)

    if not form.is_valid:
        return render(request, "test/create-test.html", { "form": form })

    form.save()
    return redirect("")


    