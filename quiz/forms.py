from django import forms
from .models import Quiz, Question, Choice

class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Основи JavaScript'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Про що цей тест?',
                'rows': 3
            }),
            'category': forms.Select(attrs={
                'class': 'form-input'
            }),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['q_type', 'text']
        widgets = {
            'q_type': forms.Select(attrs={
                'class': 'form-input',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Введіть текст питання...',
                'rows': 3
            }),
        }
        labels = {
            'q_type': 'Тип питання',
            'text': 'Текст питання',
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Варіант відповіді'
            }),
            'is_correct': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }