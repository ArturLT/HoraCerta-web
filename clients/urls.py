from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.listar_clientes, name='cliente_list'),
    path('novo/', views.criar_cliente, name='cliente_create'),
    path('edit/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('delete/<int:pk>/', views.cliente_delete, name='cliente_delete'),
]
