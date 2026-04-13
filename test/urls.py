from django.urls import path
from .views import test_view, create_test_view

urlpatterns = [
    path('', test_view, name="test"),
    path('create', create_test_view, name="test-create"),
]
