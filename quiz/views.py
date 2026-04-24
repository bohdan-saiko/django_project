from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import QuizCreateForm, QuestionForm
from .models import Quiz

@login_required
def quiz_create(request):
    if request.method != 'POST':
        form = QuizCreateForm()
        return render(request, 'quiz/create.html', {'form': form})

    form = QuizCreateForm(request.POST)

    if not form.is_valid():
        return render(request, 'quiz/create.html', {'form': form})

    quiz = form.save(commit=False)
    quiz.author = request.user
    quiz.save()

    return redirect('add_questions', quiz_id=quiz.id)

@login_required
def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)

    if request.method != 'POST':
        return render(request, 'quiz/add_questions.html', {
            'quiz': quiz, 
            'form': QuestionForm()
        })

    form = QuestionForm(request.POST)
    
    if not form.is_valid():
        return render(request, 'quiz/add_questions.html', {
            'quiz': quiz, 
            'form': form
        })

    question = form.save(commit=False)
    question.quiz = quiz
    question.save()

    if 'finish' in request.POST:
        return redirect('quiz_detail', quiz_id=quiz.id)
        
    return redirect('add_questions', quiz_id=quiz.id)