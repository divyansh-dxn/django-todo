from django.shortcuts import redirect, render
from .models import Todo
from reportlab.pdfgen import canvas
import io
from django.http import FileResponse


# this is the index function, it also performs adding a new todo 
def index(request):
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
        'allTodos': allTodos
    }
    return render(request=request, template_name='index.html', context=context)

#  getting id via request and deleting the requested to-do
def deleteTodo(request, todoId):
    todo = Todo.objects.get(id=todoId)
    todo.delete()
    return redirect(index)

#  getting id via post request and toggling the status
def toggleStatus(request):
    if request.method == 'POST':
        todoId = request.POST['id']
        todo = Todo.objects.get(id=todoId)
        todo.isDone = False if todo.isDone else True
        todo.save()
    return redirect(index)


#  exporting all todos from the database in a pdf format along with the isDone status
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
