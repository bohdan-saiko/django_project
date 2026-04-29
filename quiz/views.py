import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

from .models import Quiz, Question, Choice, Category
from .forms import QuizCreateForm, QuestionForm, ChoiceForm

ChoiceFormSet = inlineformset_factory(
    Question, 
    Choice, 
    form=ChoiceForm, 
    extra=4, 
    min_num=2, 
    validate_min=True
)

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
            'form': QuestionForm(),
            'choice_formset': ChoiceFormSet()
        })

    form = QuestionForm(request.POST)
    choice_formset = ChoiceFormSet(request.POST)
    
    if not form.is_valid() or not choice_formset.is_valid():
        return render(request, 'quiz/add_questions.html', {
            'quiz': quiz, 
            'form': form,
            'choice_formset': choice_formset
        })

    question = form.save(commit=False)
    question.quiz = quiz
    question.save()

    choice_formset.instance = question
    choice_formset.save()

    if 'finish' in request.POST:
        return redirect('users/profile') 
        
    return redirect('add_questions', quiz_id=quiz.id)

def quizzes_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    quizzes = category.quizzes.all()
    
    return render(request, 'quiz/quizzes_list.html', {
        'category': category,
        'quizzes': quizzes
    })

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(
        Quiz.objects.prefetch_related('questions__choices'), 
        pk=quiz_id
    )
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    request.session[f'quiz_score_{quiz_id}'] = 0
    
    questions = quiz.questions.prefetch_related('choices').all()
    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions})

def check_answer(request):
    data = json.loads(request.body)
    q_id = data.get('question_id')
    c_id = data.get('choice_id')
    
    choice = get_object_or_404(Choice, pk=c_id, question_id=q_id)
    quiz_id = choice.question.quiz.id
    session_key = f'quiz_score_{quiz_id}'
    
    if choice.is_correct:
        current_score = request.session.get(session_key, 0)
        request.session[session_key] = current_score + 1
    
    correct_ids = list(Choice.objects.filter(question_id=q_id, is_correct=True).values_list('id', flat=True))
    
    return JsonResponse({
        'is_correct': choice.is_correct,
        'correct_ids': correct_ids
    })

def get_final_score(request, quiz_id):
    score = request.session.get(f'quiz_score_{quiz_id}', 0)
    total = Quiz.objects.get(pk=quiz_id).questions.count()
    
    return JsonResponse({'score': score, 'total': total})