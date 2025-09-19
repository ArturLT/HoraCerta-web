from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.index, name='eventos_list'), 
    #path('adicionar/', views.evento_create, name='evento_create'),
]