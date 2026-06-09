from django.urls import path
from .views import created_quizzes_list, quiz_create, edit_quiz_metadata, delete_quiz, add_question, edit_question, delete_question, quizzes_by_category, quiz_detail, take_quiz, check_answer, get_final_score

urlpatterns = [
    path('verify-response/', check_answer, name='check_answer'),
    path('create/', quiz_create, name='quiz_create'), 
    path('created/', created_quizzes_list, name='created_quizzes'),
    path('category/<int:category_id>/', quizzes_by_category, name='category_quizzes'),
    path('<int:quiz_id>/', quiz_detail, name="quiz_detail"),
    path('<int:quiz_id>/add-question/', add_question, name='add_question'),
    path('<int:quiz_id>/edit-metadata/', edit_quiz_metadata, name='edit_quiz_metadata'),
    path('<int:quiz_id>/delete/', delete_quiz, name='delete_quiz'),
    path('<int:quiz_id>/edit-question/<int:question_id>/', edit_question, name='edit_question'),
    path('<int:quiz_id>/delete-question/<int:question_id>/', delete_question, name='delete_question'),
    path('<int:quiz_id>/take/', take_quiz, name="take_quiz"),
    path('<int:quiz_id>/final-score/', get_final_score, name='get_final_score'),
]