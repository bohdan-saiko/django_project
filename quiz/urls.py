from django.urls import path
from .views import quiz_create, add_questions

urlpatterns = [
    path('create/', quiz_create, name='quiz_create'),
    path('<int:quiz_id>/add-questions/', add_questions, name='add_questions'),
]