from django.shortcuts import redirect, render
from .models import Todo
from reportlab.pdfgen import canvas
import io
from django.http import FileResponse


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


def deleteTodo(request, todoId):
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


def export(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    allTodos = Todo.objects.all()
    y = 800
    for todo in allTodos:
        isDone = '✔' if todo.isDone else '✖'
        p.drawString(50, y,  todo.todo + '        ' + isDone)
        y -= 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='todos.pdf')
