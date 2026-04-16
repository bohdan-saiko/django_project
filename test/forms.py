from django import forms
from .models import Test, TestItem, Question

class TestFrom(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title']
        widgets = {
            'date_created': forms.DateInput(attrs={'type': 'date'}),
        }

class TestItemFrom(forms.ModelForm):
    class Meta:
        model = TestItem
        fields = ['quiz_type']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['value']
