from django.db import models
from django.contrib.auth.models import User

class Test(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    create_at = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    