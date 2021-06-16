from django.db import models

# Create your models here.

class Todo(models.Model):
    todo = models.TextField(max_length = 256)
    isDone = models.BooleanField(default=False)
    timeStamp = models.DateTimeField(auto_now_add=True)