from django import forms
from .models import Test

class TestFrom(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'content', 'create_at']
        widgets = {
            'date_created': forms.DateInput(attrs={'type': 'date'}),
        }