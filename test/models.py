from django.db import models
from django.contrib.auth.models import User

class Test(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class TestItem(models.Model):

    class QuestionType(models.TextChoices):
        ONE_RIGHT = "One right"
        MULTY_RIGHT = "Multy right"
        BOOLEAN = "True/False"  

    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    quiz_type = models.CharField(
        max_length=11,
        choices=QuestionType.choices,
        default=QuestionType.ONE_RIGHT
    )

    def __str__(self):
        return f"Item for {self.test.title}"

class Question(models.Model):
    test_item = models.ForeignKey(TestItem, on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return self.value

