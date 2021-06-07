from django.urls import path,include
from todoApp import views

urlpatterns = [
    path('',views.index)
]