from django.urls import path,include
from todoApp import views

urlpatterns = [
    path('',views.index),
    path('toggleStatus/',views.toggleStatus),
    path('<int:todoId>/deleteTodo',views.deleteTodo,name='deleteTodo'),
    path('print/',views.write_pdf_view,name='print')
]