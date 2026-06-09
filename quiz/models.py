from django.db import models
from django.contrib.auth.models import User
from category.models import Category

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='quizzes')

    def __str__(self):
        return self.title

class Question(models.Model):
    class QuestionType(models.TextChoices):
        SINGLE = "SINGLE", "Одна правильна відповідь"
        MULTI = "MULTI", "Кілька правильних відповідей"
        BOOLEAN = "BOOLEAN", "True/False"

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveBigIntegerField(default=0)
    q_type = models.CharField(
        max_length=10,
        choices=QuestionType.choices,
        default=QuestionType.SINGLE
    )

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:30]}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text