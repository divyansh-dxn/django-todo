from django.db import models

# Create your models here.

class Todo(models.Model):
    title = models.TextField(max_length = 256)
    desc = models.TextField(max_length = 512)
    isDone = models.BooleanField(False)
    timeStamp = models.DateTimeField(auto_now_add=False)