from django.shortcuts import redirect, render, HttpResponse
from .models import Todo
from io import BytesIO
from reportlab.pdfgen import canvas
import csv

# Create your views here.

def index(request):
    isSaved = False
    isEmpty = False
    allTodos = Todo.objects.all()
    if request.method == 'POST':
        note = request.POST['todo']
        if(note == ''):
            isEmpty = True
        else:
            todo = Todo(todo=note)
            todo.save()
            isSaved = True

    context = {
        'isSaved': isSaved,
        'isEmpty': isEmpty,
        'allTodos': allTodos
    }

    return render(request=request, template_name='index.html', context=context)


def deleteTodo(request,todoId):
    todo = Todo.objects.get(id=todoId)
    todo.delete()
    return redirect(index)


def toggleStatus(request):
    if request.method == 'POST':
        todoId = request.POST['id']
        todo = Todo.objects.get(id=todoId)
        todo.isDone = False if todo.isDone else True 
        todo.save()
    return redirect(index)