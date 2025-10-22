from django.urls import path
from . import views

app_name = 'items_alugados' 

urlpatterns = [
    path('', views.listar_alugueis, name='listar_alugueis'),
    path('novo/', views.novo_aluguel, name='novo_aluguel'),
    path('aluguel/<int:pk>/', views.detalhe_aluguel, name='detalhe_aluguel'),
    path('aluguel/<int:pk>/editar/', views.editar_aluguel, name='editar_aluguel'),
    path('excluir/<int:pk>/', views.excluir_aluguel, name='excluir_aluguel'),
]