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
    validate_min=True,
    can_delete=True
)

# --- HELPER FUNCTION ---

def save_question_logic(form, choice_formset, quiz):
    if form.is_valid() and choice_formset.is_valid():
        question = form.save(commit=False)
        
        choices_data = choice_formset.cleaned_data

        valid_choices = [c for c in choices_data if c and c.get('text') and not c.get('DELETE', False)]
        
        correct_count = sum(1 for c in valid_choices if c.get('is_correct'))
        total_count = len(valid_choices)

        error_msg = None
        match question.q_type:
            case 'BOOLEAN' if total_count != 2 or correct_count != 1:
                error_msg = "Для True/False має бути рівно 2 варіанти і 1 правильний."
            case 'SINGLE' if correct_count != 1:
                error_msg = "Для однієї відповіді має бути рівно 1 правильний варіант."
            case 'MULTI' if correct_count < 1:
                error_msg = "Для множинного вибору позначте хоча б одну правильну відповідь."

        if error_msg:
            return error_msg
        
        question.quiz = quiz
        question.save()
        choice_formset.instance = question
        choice_formset.save()
        return True
    return False

@login_required
def created_quizzes_list(request):
    quizzes = Quiz.objects.filter(author=request.user).prefetch_related('questions')
    
    return render(request, 'quiz/created_quizzes_list.html', {
        'quizzes': quizzes
    })

@login_required
def quiz_create(request):
    if request.method != 'POST':
        form = QuizCreateForm()
        return render(request, 'quiz/create.html', {'form': form})

    form = QuizCreateForm(request.POST)
    if form.is_valid():
        quiz = form.save(commit=False)
        quiz.author = request.user
        quiz.save()
        return redirect('add_question', quiz_id=quiz.id)
    return render(request, 'quiz/create.html', {'form': form})

@login_required
def edit_quiz_metadata(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)
    
    if request.method == 'POST':
        form = QuizCreateForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()

            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuizCreateForm(instance=quiz)
    
    return render(request, 'quiz/create.html', {
        'form': form, 
        'edit_mode': True, 
        'quiz': quiz
    })

@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)
    
    if request.method == 'POST':
        quiz.delete()
        return redirect('created_quizzes')
    
    return render(request, 'quiz/delete_confirm.html', {'quiz': quiz})

@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)
    existing_questions = quiz.questions.all().order_by('id')

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)
        
        result = save_question_logic(form, choice_formset, quiz)
        
        if result is True:
            if 'finish' in request.POST:
                return redirect('profile')
            return redirect('add_question', quiz_id=quiz.id)
        
        custom_error = result if isinstance(result, str) else None
    else:
        form = QuestionForm()
        choice_formset = ChoiceFormSet()
        custom_error = None

    return render(request, 'quiz/add_questions.html', {
        'quiz': quiz, 'form': form, 'choice_formset': choice_formset,
        'existing_questions': existing_questions, 'edit_mode': False,
        'custom_error': custom_error
    })

@login_required
def edit_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)
    question = get_object_or_404(Question, id=question_id, quiz=quiz)
    existing_questions = quiz.questions.all().order_by('id')

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        choice_formset = ChoiceFormSet(request.POST, instance=question)
        
        result = save_question_logic(form, choice_formset, quiz)
        
        if result is True:
            if 'finish' in request.POST:
                return redirect('profile')
            return redirect('add_question', quiz_id=quiz.id)
        
        custom_error = result if isinstance(result, str) else None
    else:
        form = QuestionForm(instance=question)
        choice_formset = ChoiceFormSet(instance=question)
        custom_error = None

    return render(request, 'quiz/add_questions.html', {
        'quiz': quiz, 'form': form, 'choice_formset': choice_formset,
        'existing_questions': existing_questions, 'edit_mode': True, 
        'question_id': question_id, 'custom_error': custom_error
    })

@login_required
def delete_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)
    question = get_object_or_404(Question, id=question_id, quiz=quiz)
    
    if request.method == 'POST':
        question.delete()
        return redirect('add_question', quiz_id=quiz.id)
    
    return redirect('add_question', quiz_id=quiz.id)

def quizzes_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    quizzes = category.quizzes.all()
    return render(request, 'quiz/quizzes_list.html', {'category': category, 'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions__choices'), pk=quiz_id)
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    request.session[f'quiz_score_{quiz_id}'] = 0
    questions = quiz.questions.prefetch_related('choices').all()
    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions})

def check_answer(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        q_id = data.get('question_id')
        user_choice_ids = [int(i) for i in data.get('choice_ids', [])]

        question = get_object_or_404(Question, pk=q_id)
        correct_ids = list(Choice.objects.filter(question_id=q_id, is_correct=True).values_list('id', flat=True))

        is_correct = set(user_choice_ids) == set(correct_ids)

        if is_correct:
            session_key = f'quiz_score_{question.quiz.id}'
            request.session[session_key] = request.session.get(session_key, 0) + 1
            request.session.modified = True
        
        return JsonResponse({'is_correct': is_correct, 'correct_ids': correct_ids})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_final_score(request, quiz_id):
    score = request.session.get(f'quiz_score_{quiz_id}', 0)
    total = Question.objects.filter(quiz_id=quiz_id).count()
    return JsonResponse({'score': score, 'total': total})