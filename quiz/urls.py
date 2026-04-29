from django.urls import path
from .views import quiz_create, add_questions, quizzes_by_category, quiz_detail, take_quiz, check_answer, get_final_score

urlpatterns = [
    path('create/', quiz_create, name='quiz_create'),
    path('<int:quiz_id>/add-questions/', add_questions, name='add_questions'),
    path('category/<int:category_id>/', quizzes_by_category, name='category_quizzes'),
    path('<int:quiz_id>/', quiz_detail, name="quiz_detail"),
    path('<int:quiz_id>/take/', take_quiz, name="take_quiz"),
    path('check-answer/', check_answer, name='check_answer'),
    path('<int:quiz_id>/final-score/', get_final_score, name='get_final_score'),
]