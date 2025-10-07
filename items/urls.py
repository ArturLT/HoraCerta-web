from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.aluguel_list, name = 'aluguel_list'),
    path('formulario/', views.criar_item, name = 'criar_item'),
]
