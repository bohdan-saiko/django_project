from django import forms
from .models import Test, TestItem, Question

class TestFrom(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title']
        widgets = {
            'date_created': forms.DateInput(attrs={'type': 'date'}),
        }
