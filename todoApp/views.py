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



def write_pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
    allTodos = Todo.objects.all()
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    i=0
    j=0
    for todo in allTodos:
         p.drawString(0, j, todo.todo)

         i+=10
         j+=10
   
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response




def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="todos.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row','C','Testing','Here\'s a quote'])

    return response